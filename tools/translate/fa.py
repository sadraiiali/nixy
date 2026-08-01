#!/usr/bin/env python3
"""Translate Markdown without sending fenced code blocks to the model.

All API keys and settings come from `.env` (see `.env.example` and tools.lib.envutil).
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

from openai import OpenAI

from tools.lib.envutil import (
    env_bool,
    env_float,
    env_int,
    env_path,
    env_str,
    load_dotenv,
)
from tools.lib.fa_orthography import apply_fa_orthography
from tools.lib.glossary import format_glossary_for_prompt

# Fenced code blocks: ```lang?\n...\n```
FENCE_RE = re.compile(r"(```[^\n]*\n[\s\S]*?```)", re.MULTILINE)

SYSTEM_PROMPT = """You are a professional technical translator.
Translate the given Markdown fragment from English to Persian (Farsi).

Rules:
- Output ONLY the translated Markdown fragment, no preamble or explanation.
- Keep Markdown structure: headings (#), emphasis (* * / ** **), lists, blockquotes (>), links, images.
- Do NOT translate URLs, file paths, package names, command names that appear as plain technical identifiers when they are part of a path or monospaced-looking token — but you may translate surrounding prose.
- Preserve link syntax: translate the link text, keep the URL unchanged: [متن](url).
- Preserve image syntax: translate alt text only: ![متن](url).
- Keep inline code spans exactly as they appear (backtick content must not change).
- Use natural, clear Persian suitable for technical documentation.
- Keep product names like Nix, NixOS, Nixpkgs, Firefox, RPM, Glibc, OpenSSH, Bash, Haskell, Unix, Linux, macOS untranslated (or write them in Latin script).
- Persian orthography (mandatory): for "translation" ALWAYS write ترجمه‌ی
  (heh + ZWNJ + ی). NEVER use hamza-ezafe on heh for this word (no combining hamza,
  no heh-with-yeh-above). Correct: ترجمه‌ی فارسی.
- NEVER use em dashes (—), en dashes (–), or double hyphens (--) as punctuation.
  Prefer commas, periods, colons, parentheses, or «...».
"""


def split_markdown(text: str) -> list[tuple[str, bool]]:
    """Return (segment, is_code) pairs. Code fences are never sent to the model."""
    parts: list[tuple[str, bool]] = []
    last = 0
    for m in FENCE_RE.finditer(text):
        if m.start() > last:
            parts.append((text[last : m.start()], False))
        parts.append((m.group(1), True))
        last = m.end()
    if last < len(text):
        parts.append((text[last:], False))
    return parts


def chunk_text(text: str, max_chars: int = 3500) -> list[str]:
    """Split long prose on paragraph boundaries for smaller API calls."""
    text = text.strip("\n")
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    paragraphs = re.split(r"(\n{2,})", text)
    chunks: list[str] = []
    buf = ""
    for piece in paragraphs:
        if len(buf) + len(piece) > max_chars and buf.strip():
            chunks.append(buf)
            buf = piece
        else:
            buf += piece
    if buf.strip():
        chunks.append(buf)
    return chunks


def translate_fragment(
    client: OpenAI,
    model: str,
    fragment: str,
    *,
    temperature: float,
    target_lang: str,
    glossary_block: str = "",
) -> str:
    if not fragment.strip():
        return fragment

    lang_label = {
        "fa": "Persian (Farsi)",
        "en": "English",
    }.get(target_lang, target_lang)

    system = SYSTEM_PROMPT
    if glossary_block:
        system = (
            SYSTEM_PROMPT
            + "\n\n"
            + glossary_block
            + "\n\nYou MUST follow the glossary above for those terms."
        )

    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": (
                    f"Translate this Markdown fragment to {lang_label}. "
                    "Return only the translation:\n\n" + fragment
                ),
            },
        ],
    )
    content = resp.choices[0].message.content
    if content is None:
        raise RuntimeError("Empty response from model")
    out = content.strip() + ("\n" if fragment.endswith("\n") else "")
    return apply_fa_orthography(out)


def translate_markdown(
    client: OpenAI,
    model: str,
    source: str,
    *,
    temperature: float,
    target_lang: str,
    chunk_chars: int,
    pause_sec: float,
    glossary_block: str = "",
) -> str:
    parts = split_markdown(source)
    out: list[str] = []
    text_segments = sum(1 for _, is_code in parts if not is_code and _.strip())
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

        translated_chunks: list[str] = []
        for chunk in chunk_text(body, max_chars=chunk_chars):
            done += 1
            print(
                f"  translating segment {done}/{text_segments or '?'} "
                f"({len(chunk)} chars)…",
                file=sys.stderr,
            )
            translated_chunks.append(
                translate_fragment(
                    client,
                    model,
                    chunk,
                    temperature=temperature,
                    target_lang=target_lang,
                    glossary_block=glossary_block,
                )
            )
            if pause_sec > 0:
                time.sleep(pause_sec)

        mid = "\n\n".join(c.strip("\n") for c in translated_chunks)
        out.append(
            ("\n" * leading_nl) + mid + ("\n" * trailing_nl if trailing_nl else "\n")
        )

    return "".join(out)


def main(argv: list[str] | None = None) -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=None,
        help="Source Markdown (default: TRANSLATE_INPUT from .env)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output Markdown (default: TRANSLATE_OUTPUT from .env)",
    )
    parser.add_argument(
        "--site",
        type=Path,
        default=None,
        help="Site page path (default: TRANSLATE_SITE from .env; empty to skip)",
    )
    args = parser.parse_args(argv)

    api_key = env_str("OPENAI_API_KEY", "")
    if not api_key:
        print(
            "OPENAI_API_KEY is not set. Add it to .env (see .env.example).",
            file=sys.stderr,
        )
        return 1

    base_url = env_str("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
    model = env_str("OPENAI_MODEL", "google/gemini-3.5-flash-lite")
    temperature = env_float("OPENAI_TEMPERATURE", 0.2)
    pause_sec = env_float("OPENAI_REQUEST_PAUSE_SEC", 0.3)
    chunk_chars = env_int("TRANSLATE_CHUNK_CHARS", 3500)
    target_lang = env_str("TRANSLATE_TARGET_LANG", "fa")
    add_header = env_bool("TRANSLATE_ADD_HEADER", False)

    input_path = args.input or env_path("TRANSLATE_INPUT", "how-nix-works.md")
    output_path = args.output or env_path("TRANSLATE_OUTPUT", "how-nix-works.fa.md")

    if args.site is not None:
        site_raw = str(args.site)
    else:
        site_raw = env_str("TRANSLATE_SITE", "src/routes/pages/how-nix-works/+page.md")

    site_path: Path | None = None
    if site_raw and site_raw not in {"-", "none"}:
        site_path = Path(site_raw)
        if not site_path.is_absolute():
            from tools.lib.envutil import ROOT

            site_path = ROOT / site_path

    default_headers: dict[str, str] = {}
    referer = env_str("OPENAI_HTTP_REFERER", "")
    title = env_str("OPENAI_APP_TITLE", "")
    if referer:
        default_headers["HTTP-Referer"] = referer
    if title:
        default_headers["X-Title"] = title

    source = input_path.read_text(encoding="utf-8")
    parts = split_markdown(source)
    code_n = sum(1 for s, c in parts if c)
    text_n = sum(1 for s, c in parts if not c and s.strip())
    print(
        f"Input {input_path}: {len(source)} chars, "
        f"{text_n} text segment(s), {code_n} code fence(s) kept local",
        file=sys.stderr,
    )
    print(f"Model: {model} @ {base_url}", file=sys.stderr)

    use_glossary = env_bool("TRANSLATE_USE_GLOSSARY", True)
    glossary_block = format_glossary_for_prompt() if use_glossary else ""
    if use_glossary:
        n_terms = glossary_block.count("\n")  # header + lines
        print(
            f"Glossary: {max(0, n_terms - 1)} term(s) with translations "
            f"(from GLOSSARY_PATH)",
            file=sys.stderr,
        )
        if n_terms <= 1:
            print(
                "  (empty — fill /glossary-dev then re-run, or make glossary first)",
                file=sys.stderr,
            )

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers=default_headers or None,
    )
    translated = apply_fa_orthography(
        translate_markdown(
            client,
            model,
            source,
            temperature=temperature,
            target_lang=target_lang,
            chunk_chars=chunk_chars,
            pause_sec=pause_sec,
            glossary_block=glossary_block,
        )
    )

    if add_header and not translated.lstrip().startswith("<!--"):
        header = (
            f"<!-- lang: {target_lang} — translated by translate_fa.py; "
            "code fences left unchanged -->\n\n"
        )
        translated = header + translated.lstrip()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(translated, encoding="utf-8")
    print(f"Wrote {output_path} ({len(translated)} bytes)", file=sys.stderr)

    if site_path is not None:
        site_path.parent.mkdir(parents=True, exist_ok=True)
        site_path.write_text(translated, encoding="utf-8")
        print(f"Wrote site page {site_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
