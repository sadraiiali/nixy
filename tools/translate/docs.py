#!/usr/bin/env python3
"""Full-document EN→FA translation AFTER glossary review.

Optimizations:
- Injects only *approved* glossary terms into the system prompt
- Strong system prompt for Nix technical docs
- Never sends fenced code blocks to the model (reinserted unchanged)
- Supports multiple Markdown files (first-steps, etc.)

Gate: refuses to run until enough glossary terms are approved
(see TRANSLATE_MIN_APPROVED / TRANSLATE_REQUIRE_NO_PENDING in .env).
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

from openai import OpenAI

from tools.lib.envutil import (
    ROOT,
    env_bool,
    env_float,
    env_int,
    env_path,
    env_str,
    load_dotenv,
)
from tools.lib.fa_orthography import apply_fa_orthography
from tools.lib.glossary import (
    assert_ready_for_full_translate,
    format_glossary_for_prompt,
    glossary_review_stats,
    load_glossary,
)

FENCE_RE = re.compile(r"(```[^\n]*\n[\s\S]*?```)", re.MULTILINE)
# GFM tables (header + separator + rows) — keep whole tables as one unit.
TABLE_RE = re.compile(
    r"(?:^[ \t]*\|.+\|[ \t]*\n)+"
    r"(?:^[ \t]*\|[-:| \t]+\|[ \t]*\n)"
    r"(?:^[ \t]*\|.+\|[ \t]*\n?)*",
    re.MULTILINE,
)
# Prefer Gemini Flash Lite for FA docs; override with --model / TRANSLATE_MODEL / OPENAI_MODEL.
DEFAULT_TRANSLATE_MODEL = "google/gemini-3.5-flash-lite"

SYSTEM_PROMPT = """You are an expert technical translator EN→Persian (Farsi) for Nix and NixOS documentation (nix.dev style).

## Hard rules
1. Output ONLY the translated Markdown. No preamble, no commentary.
2. Preserve Markdown structure exactly: headings, lists, tables, blockquotes, links, images, emphasis.
3. NEVER modify fenced code blocks — they are removed before you see the text and must not be invented.
4. NEVER change content inside inline backticks `like this` — leave identifiers as-is if they appear outside code (commands, flags, paths often stay Latin).
5. Keep URLs, file paths, package attribute names, and CLI flags in Latin script.
6. Product names stay Latin: Nix, NixOS, Nixpkgs, Linux, macOS, Bash, Glibc, Flakes, etc.
7. Follow the GLOSSARY strictly when a term appears (case-insensitive in prose).
8. Natural, clear Persian suitable for developers; prefer consistency over word-for-word calques.
9. Preserve heading levels (# ## ###). Do not add or remove sections.
10. Persian orthography (mandatory): for the word "translation" ALWAYS write
    ترجمه + ZWNJ + ی  i.e. the form with final ی after a zero-width non-joiner
    (looks like: ترجمه‌ی). NEVER use hamza-ezafe on heh for this word
    (the spellings with Arabic hamza-above on heh, without ی).
    Correct: ترجمه‌ی فارسی / ترجمه‌ی کنترل‌شده.
11. NEVER use em dashes (—), en dashes (–), or double hyphens (--) as punctuation.
    Use commas, periods, colons, parentheses, or «...» instead.
"""


def split_markdown(text: str) -> list[tuple[str, bool]]:
    """Split into (segment, is_protected) where protected = code fence or GFM table.

    Tables must not be line-chopped or the model produces broken partial rows.
    Protected segments are still translated as a single unit (not skipped).
    """
    # First isolate fenced code (never translated).
    coarse: list[tuple[str, str]] = []  # text, kind: prose|code|table
    last = 0
    for m in FENCE_RE.finditer(text):
        if m.start() > last:
            coarse.append((text[last : m.start()], "prose"))
        coarse.append((m.group(1), "code"))
        last = m.end()
    if last < len(text):
        coarse.append((text[last:], "prose"))

    parts: list[tuple[str, bool]] = []
    for segment, kind in coarse:
        if kind == "code":
            parts.append((segment, True))  # protected: keep as-is
            continue
        # Split prose around tables; tables are translated whole (not protected-as-code).
        tlast = 0
        for tm in TABLE_RE.finditer(segment):
            if tm.start() > tlast:
                parts.append((segment[tlast : tm.start()], False))
            # False = still translate, but chunk_text will not line-split if we mark size
            parts.append((tm.group(0), False))
            tlast = tm.end()
        if tlast < len(segment):
            parts.append((segment[tlast:], False))
    return parts


def _split_oversized_piece(piece: str, max_chars: int) -> list[str]:
    """Hard-split a single piece (e.g. a long table) by lines when needed."""
    if len(piece) <= max_chars:
        return [piece] if piece else []
    lines = piece.splitlines(keepends=True)
    out: list[str] = []
    buf = ""
    for line in lines:
        if len(line) > max_chars:
            # pathological single line — hard cut
            if buf.strip():
                out.append(buf)
                buf = ""
            for i in range(0, len(line), max_chars):
                out.append(line[i : i + max_chars])
            continue
        if len(buf) + len(line) > max_chars and buf.strip():
            out.append(buf)
            buf = line
        else:
            buf += line
    if buf.strip():
        out.append(buf)
    return out


def chunk_text(text: str, max_chars: int) -> list[str]:
    text = text.strip("\n")
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    # Prefer heading boundaries so sections stay coherent.
    heading_bits = re.split(r"(?=^#{1,6}\s)", text, flags=re.MULTILINE)
    chunks: list[str] = []
    buf = ""
    for piece in heading_bits:
        if not piece:
            continue
        if len(piece) > max_chars:
            if buf.strip():
                chunks.append(buf)
                buf = ""
            # Tables: never hard-split mid-table (would break the model).
            if TABLE_RE.fullmatch(piece.strip("\n") + ("\n" if piece.endswith("\n") else "")) or (
                piece.lstrip().startswith("|") and "\n|" in piece
            ):
                chunks.append(piece)
                continue
            paragraphs = re.split(r"(\n{2,})", piece)
            pbuf = ""
            for para in paragraphs:
                if len(para) > max_chars and not para.lstrip().startswith("|"):
                    if pbuf.strip():
                        chunks.append(pbuf)
                        pbuf = ""
                    chunks.extend(_split_oversized_piece(para, max_chars))
                    continue
                if len(para) > max_chars:
                    # oversized table-ish block: keep whole
                    if pbuf.strip():
                        chunks.append(pbuf)
                        pbuf = ""
                    chunks.append(para)
                    continue
                if len(pbuf) + len(para) > max_chars and pbuf.strip():
                    chunks.append(pbuf)
                    pbuf = para
                else:
                    pbuf += para
            if pbuf.strip():
                chunks.append(pbuf)
            continue
        if len(buf) + len(piece) > max_chars and buf.strip():
            chunks.append(buf)
            buf = piece
        else:
            buf += piece
    if buf.strip():
        chunks.append(buf)
    return chunks


def max_tokens_for_fragment(fragment: str) -> int:
    """Cap completion size so OpenRouter credit checks don't reserve 65k tokens.

    Persian is often longer than English; estimate from input size and clamp
    hard so low-balance accounts still pass the preflight afford check.
    """
    # Input chars → output tokens: FA prose is often longer than EN.
    # OpenRouter bills by max_tokens reserved, so keep a firm upper bound.
    estimate = max(512, int(len(fragment) * 1.1) + 700)
    # Tables: need room for every row (do not mid-cut)
    if fragment.lstrip().startswith("|"):
        estimate = max(estimate, int(len(fragment) * 0.9) + 900)
    return min(8000, estimate)


def translate_fragment(
    client: OpenAI,
    model: str,
    fragment: str,
    *,
    temperature: float,
    glossary_block: str,
    max_tokens: int | None = None,
) -> str:
    if not fragment.strip():
        return fragment
    system = SYSTEM_PROMPT
    if glossary_block:
        system = (
            SYSTEM_PROMPT
            + "\n\n"
            + glossary_block
            + "\n\nYou MUST apply the glossary mappings above for those English terms."
        )
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens if max_tokens is not None else max_tokens_for_fragment(fragment),
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": (
                    "Translate this Markdown fragment to Persian (Farsi). "
                    "Code fences were removed on purpose — do not invent them. "
                    "If the fragment is a Markdown table, keep every row and pipe; "
                    "only translate human-readable cell text (e.g. Tier → سطح). "
                    "Do not invent extra rows or commentary.\n\n"
                    + fragment
                ),
            },
        ],
    )
    content = resp.choices[0].message.content
    if content is None:
        raise RuntimeError("Empty model response")
    out = content.strip() + ("\n" if fragment.endswith("\n") else "")
    return apply_fa_orthography(out)


def translate_markdown(
    client: OpenAI,
    model: str,
    source: str,
    *,
    temperature: float,
    chunk_chars: int,
    pause_sec: float,
    glossary_block: str,
) -> str:
    parts = split_markdown(source)
    out: list[str] = []
    text_n = sum(1 for s, c in parts if not c and s.strip())
    done = 0
    for segment, is_code in parts:
        if is_code:
            out.append(segment)
            continue
        leading_nl = len(segment) - len(segment.lstrip("\n"))
        trailing_nl = len(segment) - len(segment.rstrip("\n"))
        body = segment.strip("\n")
        if not body.strip():
            out.append(segment)
            continue
        pieces: list[str] = []
        for chunk in chunk_text(body, chunk_chars):
            done += 1
            print(
                f"    segment {done}/{text_n} ({len(chunk)} chars)…",
                file=sys.stderr,
            )
            pieces.append(
                translate_fragment(
                    client,
                    model,
                    chunk,
                    temperature=temperature,
                    glossary_block=glossary_block,
                )
            )
            if pause_sec > 0:
                time.sleep(pause_sec)
        mid = "\n\n".join(p.strip("\n") for p in pieces)
        out.append(
            ("\n" * leading_nl) + mid + ("\n" * trailing_nl if trailing_nl else "\n")
        )
    return "".join(out)


def resolve_inputs(cli_docs: list[Path]) -> list[Path]:
    if cli_docs:
        return cli_docs
    raw = env_str("TRANSLATE_DOCS", "")
    if raw.strip() and raw.strip() not in {"*", "all", "AUTO"}:
        return [Path(p.strip()) for p in raw.split(",") if p.strip()]
    # default: entire English tree
    d = env_path("NIX_DEV_OUTPUT", "docs/en")
    if d.is_dir():
        files = sorted(
            p
            for p in d.rglob("*.md")
            if p.name != "manifest.json" and "manifest" not in p.parts
        )
        # skip pure sphinx index noise? keep all
        if files:
            return files
    return [env_path("TRANSLATE_INPUT", "how-nix-works.md")]


def out_path_for(src: Path, out_dir: Path, en_root: Path) -> Path:
    """Mirror docs/en/.../foo.md → docs/fa/.../foo.md"""
    try:
        rel = src.resolve().relative_to(en_root.resolve())
    except ValueError:
        rel = Path(src.name)
    return out_dir / rel


def looks_translated_fa(path: Path, *, min_arabic: int = 8) -> bool:
    """True if *path* already has meaningful Persian (not just a copied EN stub)."""
    if not path.is_file() or path.stat().st_size < 20:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    # Ignore fenced code when scoring language
    prose = FENCE_RE.sub("", text)
    arabic = len(re.findall(r"[\u0600-\u06FF]", prose))
    if arabic >= min_arabic:
        return True
    # Short TOCs / titles: even a few Arabic letters count
    if arabic >= 3 and path.stat().st_size < 800:
        return True
    return False


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
# Fence open: ``` or ~~~~ optionally with lang; allow 3+ backticks
FENCE_LINE_RE = re.compile(r"^([`~]{3,})")


def _strip_heading_markup(title: str) -> str:
    """Normalize heading text for matching (drop anchors, links, backticks)."""
    t = title.strip()
    # {#id} / (label)= MyST
    t = re.sub(r"\s*\{#[^}]+\}\s*$", "", t)
    t = re.sub(r"^\([^)]+\)=\s*", "", t)
    # HTML anchors
    t = re.sub(r"<a\b[^>]*>.*?</a>\s*", "", t, flags=re.I | re.S)
    t = re.sub(r"<[^>]+>", "", t)
    # Markdown links [text](url) → text
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    # inline code / emphasis wrappers
    t = t.replace("`", "").replace("*", "").replace("_", "")
    return re.sub(r"\s+", " ", t).strip().casefold()


def prose_language_score(text: str) -> tuple[int, int, float]:
    """Return (arabic_chars, latin_chars, arabic_ratio) ignoring fenced code."""
    prose = FENCE_RE.sub("", text)
    # also strip MyST fences that use 4+ backticks if any leftover
    prose = re.sub(r"`{3,}[^\n]*\n[\s\S]*?`{3,}", "", prose)
    arabic = len(re.findall(r"[\u0600-\u06FF]", prose))
    latin = len(re.findall(r"[A-Za-z]", prose))
    total = arabic + latin
    ratio = (arabic / total) if total else 1.0
    return arabic, latin, ratio


def is_section_untranslated(
    text: str,
    *,
    min_latin: int = 60,
    max_arabic_ratio: float = 0.35,
) -> bool:
    """Heuristic: mostly Latin prose outside code → needs (re)translation."""
    arabic, latin, ratio = prose_language_score(text)
    if latin < min_latin:
        return False
    return ratio < max_arabic_ratio


def split_markdown_sections(text: str) -> list[dict]:
    """Split Markdown into heading-led sections (fence-aware).

    Each item: {
      level, title, title_key, start, end, body
    }
    start/end are character offsets into *text*; body includes the heading line.
    Preamble before the first heading is level 0 with title '(preamble)'.
    """
    lines = text.splitlines(keepends=True)
    # mark which line indices are inside fenced code
    in_fence = False
    fence_char = ""
    fence_len = 0
    line_in_code: list[bool] = []
    for line in lines:
        raw = line.rstrip("\n")
        m = FENCE_LINE_RE.match(raw)
        if m:
            ch = m.group(1)[0]
            n = len(m.group(1))
            rest = raw[n:].strip()
            if not in_fence:
                in_fence = True
                fence_char = ch
                fence_len = n
                line_in_code.append(True)
                continue
            # Close: same char, ≥3 ticks, empty info string. Lenient on count so
            # mangled FA fences (`````` open / ``` close) still close.
            if ch == fence_char and n >= 3 and rest == "":
                in_fence = False
                fence_char = ""
                fence_len = 0
                line_in_code.append(True)
                continue
        line_in_code.append(in_fence)

    # absolute offsets per line start
    offsets: list[int] = []
    pos = 0
    for line in lines:
        offsets.append(pos)
        pos += len(line)
    total_len = pos

    heading_lines: list[tuple[int, int, str]] = []  # line_idx, level, title
    for i, line in enumerate(lines):
        if line_in_code[i]:
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line.rstrip("\n"))
        if m:
            heading_lines.append((i, len(m.group(1)), m.group(2).strip()))

    sections: list[dict] = []
    if not heading_lines:
        sections.append(
            {
                "level": 0,
                "title": "(preamble)",
                "title_key": "(preamble)",
                "start": 0,
                "end": total_len,
                "body": text,
            }
        )
        return sections

    first_line = heading_lines[0][0]
    if first_line > 0:
        start = 0
        end = offsets[first_line]
        sections.append(
            {
                "level": 0,
                "title": "(preamble)",
                "title_key": "(preamble)",
                "start": start,
                "end": end,
                "body": text[start:end],
            }
        )

    for hi, (line_i, level, title) in enumerate(heading_lines):
        start = offsets[line_i]
        if hi + 1 < len(heading_lines):
            end = offsets[heading_lines[hi + 1][0]]
        else:
            end = total_len
        body = text[start:end]
        sections.append(
            {
                "level": level,
                "title": title,
                "title_key": _strip_heading_markup(title),
                "start": start,
                "end": end,
                "body": body,
            }
        )
    return sections


def _match_section_index(
    en_secs: list[dict],
    fa_secs: list[dict],
    en_idx: int,
) -> int | None:
    """Map EN section index → FA section index by title key or order.

    Prefer exact title match; when EN/FA have the same section count (common
    after partial translates), use the same index so broken FA headings still
    line up with EN content.
    """
    if en_idx < 0 or en_idx >= len(en_secs):
        return None
    en = en_secs[en_idx]
    key = en["title_key"]
    # exact key match (EN heading still present in FA)
    for j, fa in enumerate(fa_secs):
        if fa["title_key"] == key and key not in {"(preamble)", ""}:
            return j
    # same document shape → positional pairing (best for partial FA)
    if len(en_secs) == len(fa_secs) and en_idx < len(fa_secs):
        return en_idx
    # same level, same ordinal among that level
    en_level_ord = sum(1 for s in en_secs[: en_idx + 1] if s["level"] == en["level"])
    seen = 0
    for j, fa in enumerate(fa_secs):
        if fa["level"] == en["level"]:
            seen += 1
            if seen == en_level_ord:
                return j
    if en_idx < len(fa_secs):
        return en_idx
    return None


def _is_yaml_frontmatter(body: str) -> bool:
    b = body.lstrip()
    return b.startswith("---") and "\n---" in b[:800]


def select_en_section_indices(
    en_secs: list[dict],
    fa_secs: list[dict],
    *,
    section_names: list[str] | None,
    auto: bool,
) -> list[int]:
    """Which EN section indices to re-translate."""
    if section_names:
        wanted = {_strip_heading_markup(n) for n in section_names if n.strip()}
        # also allow raw substring match on original title
        raw_wanted = {n.strip().casefold() for n in section_names if n.strip()}
        idxs: list[int] = []
        for i, s in enumerate(en_secs):
            if s["title_key"] in wanted:
                idxs.append(i)
                continue
            if s["title"].strip().casefold() in raw_wanted:
                idxs.append(i)
                continue
            # substring: "Missing dependencies" matches title
            for w in raw_wanted:
                if w and w in s["title"].casefold():
                    idxs.append(i)
                    break
        return idxs

    if not auto:
        return list(range(len(en_secs)))

    idxs = []
    for i, en in enumerate(en_secs):
        if en["level"] == 0 and en["title_key"] == "(preamble)":
            # never auto-translate YAML frontmatter (keys stay English)
            if _is_yaml_frontmatter(en["body"]):
                continue
            j = _match_section_index(en_secs, fa_secs, i)
            if j is None:
                continue
            if is_section_untranslated(fa_secs[j]["body"], min_latin=40):
                idxs.append(i)
            continue
        j = _match_section_index(en_secs, fa_secs, i)
        if j is None:
            continue
        # Prefer FA body score; if FA heading is garbage (e.g. `# icat.nix`)
        # but index-aligned, still use FA body. Also catch EN-heavy FA titles.
        fa_body = fa_secs[j]["body"]
        if is_section_untranslated(fa_body):
            idxs.append(i)
            continue
        # Mixed residual English under a Persian heading
        _ar, lat, ratio = prose_language_score(fa_body)
        if lat >= 200 and ratio < 0.55:
            idxs.append(i)
    return idxs


def retranslate_sections(
    client: OpenAI,
    model: str,
    en_text: str,
    fa_text: str,
    *,
    section_names: list[str] | None,
    auto: bool,
    temperature: float,
    chunk_chars: int,
    pause_sec: float,
    glossary_block: str,
) -> tuple[str, list[str]]:
    """Replace selected FA sections with fresh translations of EN sections.

    Returns (new_fa_text, list of section titles translated).
    """
    en_secs = split_markdown_sections(en_text)
    fa_secs = split_markdown_sections(fa_text)
    indices = select_en_section_indices(
        en_secs, fa_secs, section_names=section_names, auto=auto
    )
    if not indices:
        return fa_text, []

    # Apply replacements from the end so offsets stay valid if we rebuild from pieces.
    # Rebuild FA from its section list with replacements.
    translated_titles: list[str] = []
    fa_bodies = [s["body"] for s in fa_secs]

    for en_i in indices:
        en = en_secs[en_i]
        fa_i = _match_section_index(en_secs, fa_secs, en_i)
        if fa_i is None:
            print(
                f"    skip unmatched section: {en['title']!r}",
                file=sys.stderr,
            )
            continue
        print(
            f"    section [{en['level']}] {en['title']!r} → FA {fa_secs[fa_i]['title']!r}",
            file=sys.stderr,
        )
        fa_new = apply_fa_orthography(
            translate_markdown(
                client,
                model,
                en["body"],
                temperature=temperature,
                chunk_chars=chunk_chars,
                pause_sec=pause_sec,
                glossary_block=glossary_block,
            )
        )
        # Ensure trailing newline between sections
        if not fa_new.endswith("\n") and fa_i + 1 < len(fa_bodies):
            fa_new += "\n"
        fa_bodies[fa_i] = fa_new
        translated_titles.append(en["title"])

    return "".join(fa_bodies), translated_titles


def load_jobs_json(path: Path) -> list[dict]:
    """Load section-translate jobs from JSON.

    Schema:
    {
      "jobs": [
        {
          "source": "docs/en/tutorials/foo.md",   # required
          "dest": "docs/fa/tutorials/foo.md",     # optional
          "sections": ["Missing dependencies", "Finding packages"],  # optional
          "auto": true,   # optional; if no sections, translate untranslated only
          "model": "google/gemini-3.5-flash-lite"  # optional override
        }
      ]
    }
    Or a bare list of job objects.
    """
    import json

    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        jobs = raw
    elif isinstance(raw, dict) and "jobs" in raw:
        jobs = raw["jobs"]
    else:
        raise ValueError("jobs JSON must be a list or {\"jobs\": [...]}")
    if not isinstance(jobs, list):
        raise ValueError("jobs must be a list")
    return jobs


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "docs",
        nargs="*",
        type=Path,
        help="Markdown files (default: TRANSLATE_DOCS or docs/en/first-steps/*.md)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default TRANSLATE_OUT_DIR)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip glossary readiness gate",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip files that already have a Persian FA output (not mere EN stubs)",
    )
    parser.add_argument(
        "--no-skip-existing",
        action="store_true",
        help="Force re-translate even when FA already looks translated",
    )
    parser.add_argument(
        "--model",
        default="",
        help=(
            "OpenRouter/OpenAI model id "
            f"(default: TRANSLATE_MODEL or {DEFAULT_TRANSLATE_MODEL})"
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max files this run (0 = all)",
    )
    parser.add_argument(
        "--jobs-json",
        type=Path,
        default=None,
        help=(
            "JSON file of section-level translate jobs "
            "(see tools/translate/jobs.example.json). "
            "When set, positional docs are ignored unless jobs are empty."
        ),
    )
    parser.add_argument(
        "--sections",
        default="",
        help=(
            "Comma-separated EN section titles to re-translate "
            "(matched against heading text). Implies patching existing FA."
        ),
    )
    parser.add_argument(
        "--auto-untranslated",
        action="store_true",
        help=(
            "Only re-translate FA sections that still look English "
            "(requires existing FA; patches in place)"
        ),
    )
    parser.add_argument(
        "--list-untranslated",
        action="store_true",
        help="List auto-detected untranslated FA sections and exit (no API calls)",
    )
    args = parser.parse_args(argv)

    api_key = env_str("OPENAI_API_KEY", "")
    if not api_key and not args.list_untranslated:
        print("OPENAI_API_KEY missing in .env", file=sys.stderr)
        return 1

    glossary = load_glossary()
    stats = glossary_review_stats(glossary)
    print(
        f"Glossary: tech={stats['tech']} approved={stats['approved']} "
        f"pending={stats['pending']} with_tr={stats['with_translation']}",
        file=sys.stderr,
    )

    if (
        not args.force
        and not args.list_untranslated
        and not env_bool("TRANSLATE_SKIP_GLOSSARY_GATE", False)
    ):
        assert_ready_for_full_translate(
            glossary,
            require_no_pending=env_bool("TRANSLATE_REQUIRE_NO_PENDING", False),
        )

    use_gl = env_bool("TRANSLATE_USE_GLOSSARY", True)
    glossary_block = format_glossary_for_prompt() if use_gl else ""
    n_terms = max(0, glossary_block.count("\n") - 1) if glossary_block else 0
    print(f"Using {n_terms} approved glossary term(s) in prompt", file=sys.stderr)

    base_url = env_str("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
    # Prefer --model, then TRANSLATE_MODEL, then DEFAULT_TRANSLATE_MODEL (Gemini 3.5 Flash Lite).
    model = (
        args.model
        or env_str("TRANSLATE_MODEL", "")
        or DEFAULT_TRANSLATE_MODEL
    )
    temperature = env_float("OPENAI_TEMPERATURE", 0.2)
    pause = env_float("OPENAI_REQUEST_PAUSE_SEC", 0.3)
    chunk_chars = env_int("TRANSLATE_CHUNK_CHARS", 3500)
    en_root = env_path("NIX_DEV_OUTPUT", "docs/en")
    out_dir = args.out_dir or env_path("TRANSLATE_OUT_DIR", "docs/fa")
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.no_skip_existing:
        skip_existing = False
    else:
        skip_existing = args.skip_existing or env_bool("TRANSLATE_SKIP_EXISTING", True)

    section_names = [
        s.strip() for s in args.sections.split(",") if s.strip()
    ] or None
    section_mode = bool(
        args.jobs_json
        or args.auto_untranslated
        or section_names
        or args.list_untranslated
    )

    headers = {}
    if env_str("OPENAI_HTTP_REFERER", ""):
        headers["HTTP-Referer"] = env_str("OPENAI_HTTP_REFERER", "")
    if env_str("OPENAI_APP_TITLE", ""):
        headers["X-Title"] = env_str("OPENAI_APP_TITLE", "")

    client = None
    if not args.list_untranslated:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            default_headers=headers or None,
        )

    # ── jobs-json / section patch mode ──────────────────────────────────
    if section_mode:
        jobs: list[dict] = []
        if args.jobs_json:
            jp = args.jobs_json if args.jobs_json.is_file() else ROOT / args.jobs_json
            jobs = load_jobs_json(jp)
            print(f"Loaded {len(jobs)} job(s) from {jp}", file=sys.stderr)
        else:
            docs = resolve_inputs(args.docs)
            for p in docs:
                src = p if p.is_file() else ROOT / p
                if not src.is_file():
                    print(f"skip missing: {p}", file=sys.stderr)
                    continue
                jobs.append(
                    {
                        "source": str(
                            src.relative_to(ROOT) if src.is_relative_to(ROOT) else src
                        ),
                        "sections": section_names,
                        "auto": bool(args.auto_untranslated or args.list_untranslated)
                        and not section_names,
                    }
                )

        if args.limit and args.limit > 0:
            jobs = jobs[: args.limit]

        done = 0
        skipped = 0
        failed = 0
        for i, job in enumerate(jobs, 1):
            src = Path(job["source"])
            if not src.is_file():
                src = ROOT / src
            if not src.is_file():
                print(f"[{i}/{len(jobs)}] missing source {job['source']}", file=sys.stderr)
                failed += 1
                continue
            dest = (
                Path(job["dest"])
                if job.get("dest")
                else out_path_for(src, out_dir, en_root)
            )
            if not dest.is_absolute():
                dest = ROOT / dest if not dest.is_file() else dest
            if not dest.is_file() and not args.list_untranslated:
                # no FA yet → full translate once
                print(
                    f"[{i}/{len(jobs)}] no FA yet, full translate {src.name}",
                    file=sys.stderr,
                )
                try:
                    assert client is not None
                    fa = apply_fa_orthography(
                        translate_markdown(
                            client,
                            job.get("model") or model,
                            src.read_text(encoding="utf-8"),
                            temperature=temperature,
                            chunk_chars=chunk_chars,
                            pause_sec=pause,
                            glossary_block=glossary_block,
                        )
                    )
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text(fa, encoding="utf-8")
                    print(f"  → {dest} ({len(fa)} bytes)", file=sys.stderr)
                    done += 1
                except Exception as exc:
                    failed += 1
                    print(f"  ERROR: {exc}", file=sys.stderr)
                continue

            en_text = src.read_text(encoding="utf-8")
            fa_text = dest.read_text(encoding="utf-8") if dest.is_file() else ""
            job_sections = job.get("sections")
            if isinstance(job_sections, str):
                job_sections = [job_sections]
            job_auto = bool(job.get("auto", False))
            if not job_sections and not job_auto:
                job_auto = True

            if args.list_untranslated:
                en_secs = split_markdown_sections(en_text)
                fa_secs = split_markdown_sections(fa_text)
                idxs = select_en_section_indices(
                    en_secs, fa_secs, section_names=None, auto=True
                )
                print(f"[{i}/{len(jobs)}] {src} → {dest}")
                if not idxs:
                    print("  (none — looks fully translated)")
                for ei in idxs:
                    j = _match_section_index(en_secs, fa_secs, ei)
                    fa_t = fa_secs[j]["title"] if j is not None else "?"
                    ar, lat, ratio = prose_language_score(
                        fa_secs[j]["body"] if j is not None else ""
                    )
                    print(
                        f"  - EN: {en_secs[ei]['title']!r}  FA: {fa_t!r}  "
                        f"ar={ar} lat={lat} ratio={ratio:.2f}"
                    )
                skipped += 1
                continue

            print(
                f"[{i}/{len(jobs)}] Section-patch "
                f"{src.relative_to(ROOT) if src.is_relative_to(ROOT) else src} …",
                file=sys.stderr,
            )
            try:
                assert client is not None
                new_fa, titles = retranslate_sections(
                    client,
                    job.get("model") or model,
                    en_text,
                    fa_text,
                    section_names=job_sections if job_sections else None,
                    auto=job_auto and not job_sections,
                    temperature=temperature,
                    chunk_chars=chunk_chars,
                    pause_sec=pause,
                    glossary_block=glossary_block,
                )
                if not titles:
                    print("  (no sections matched / needed)", file=sys.stderr)
                    skipped += 1
                    continue
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(new_fa, encoding="utf-8")
                print(
                    f"  → patched {len(titles)} section(s) → {dest.relative_to(ROOT) if dest.is_relative_to(ROOT) else dest}",
                    file=sys.stderr,
                )
                for t in titles:
                    print(f"     • {t}", file=sys.stderr)
                done += 1
            except Exception as exc:
                failed += 1
                print(f"  ERROR: {exc}", file=sys.stderr)

        print(
            f"Done. translated={done} skipped={skipped} failed={failed}",
            file=sys.stderr,
        )
        return 0 if failed == 0 else 1

    # ── full-document mode (original behaviour) ─────────────────────────
    docs = resolve_inputs(args.docs)
    resolved: list[Path] = []
    for p in docs:
        if p.is_file():
            resolved.append(p)
        elif (ROOT / p).is_file():
            resolved.append(ROOT / p)
        else:
            print(f"skip missing: {p}", file=sys.stderr)

    if not resolved:
        print("No input documents found.", file=sys.stderr)
        return 1

    if args.limit and args.limit > 0:
        resolved = resolved[: args.limit]

    print(
        f"Queue: {len(resolved)} file(s) → {out_dir}  model={model}",
        file=sys.stderr,
    )
    done = 0
    skipped = 0
    failed = 0

    for i, src in enumerate(resolved, 1):
        dest = out_path_for(src, out_dir, en_root)
        if skip_existing and looks_translated_fa(dest):
            print(
                f"[{i}/{len(resolved)}] skip existing FA {dest.relative_to(ROOT)}",
                file=sys.stderr,
            )
            skipped += 1
            continue
        if dest.is_file() and dest.stat().st_size > 40 and not looks_translated_fa(dest):
            print(
                f"[{i}/{len(resolved)}] re-translate (no Persian yet) "
                f"{dest.relative_to(ROOT)}",
                file=sys.stderr,
            )
        print(
            f"[{i}/{len(resolved)}] Translating "
            f"{src.relative_to(ROOT) if src.is_relative_to(ROOT) else src} …",
            file=sys.stderr,
        )
        try:
            source = src.read_text(encoding="utf-8")
            fa = apply_fa_orthography(
                translate_markdown(
                    client,
                    model,
                    source,
                    temperature=temperature,
                    chunk_chars=chunk_chars,
                    pause_sec=pause,
                    glossary_block=glossary_block,
                )
            )
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(fa, encoding="utf-8")
            print(f"  → {dest.relative_to(ROOT)} ({len(fa)} bytes)", file=sys.stderr)
            done += 1
        except Exception as exc:
            failed += 1
            print(f"  ERROR: {exc}", file=sys.stderr)

    print(
        f"Done. translated={done} skipped={skipped} failed={failed}",
        file=sys.stderr,
    )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
