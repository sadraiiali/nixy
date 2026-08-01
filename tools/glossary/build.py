#!/usr/bin/env python3
"""Build / update the translation glossary from Markdown documents.

- Extracts unique words (and known multi-word tech phrases)
- Skips fenced code blocks (never analyzed as prose)
- Flags software-development terms that often get mistranslated
- Merges into glossary.json without wiping user translations
- Works for the current guide and any future docs you pass in

Usage:
  uv run python -m tools.glossary.build
  uv run python -m tools.glossary.build path/to/doc.md another.md
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

from tools.lib.envutil import env_path, env_str, load_dotenv
from tools.lib.glossary import load_glossary, save_glossary
from tools.lib.tech_lexicon import MULTIWORD_TERMS, SINGLE_TERMS, STOPWORDS

FENCE_RE = re.compile(r"```[^\n]*\n[\s\S]*?```", re.MULTILINE)
# Markdown noise
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]+\)")
IMG_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
INLINE_CODE_RE = re.compile(r"`[^`]+`")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
URL_RE = re.compile(r"https?://\S+")
# Tokens: words with optional internal hyphens / apostrophes
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:['’-][A-Za-z0-9]+)*")


def strip_code_and_markup(md: str) -> str:
    text = FENCE_RE.sub(" ", md)
    text = HTML_COMMENT_RE.sub(" ", text)
    text = IMG_RE.sub(r"\1", text)
    text = LINK_RE.sub(r"\1", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    # drop markdown punctuation noise
    text = re.sub(r"[#>*_~|]+", " ", text)
    return text


def find_multiword(text: str) -> Counter[str]:
    lower = text.lower()
    found: Counter[str] = Counter()
    # longest phrases first
    phrases = sorted(MULTIWORD_TERMS.keys(), key=len, reverse=True)
    remaining = lower
    for phrase in phrases:
        # count non-overlapping
        start = 0
        n = 0
        plen = len(phrase)
        while True:
            i = remaining.find(phrase, start)
            if i < 0:
                break
            # word boundaries
            before_ok = i == 0 or not remaining[i - 1].isalnum()
            after = i + plen
            after_ok = after >= len(remaining) or not remaining[after].isalnum()
            if before_ok and after_ok:
                n += 1
                # mask so shorter phrases don't double-count inside
                remaining = remaining[:i] + (" " * plen) + remaining[after:]
                start = i + plen
            else:
                start = i + 1
        if n:
            found[phrase] = n
    return found


def find_words(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for m in WORD_RE.finditer(text):
        w = m.group(0)
        # skip pure numbers disguised, version-like handled as words
        if len(w) == 1 and w.lower() in STOPWORDS:
            continue
        counts[w.lower()] += 1
    return counts


def is_tech_word(word: str, multiword_hit: bool = False) -> bool:
    w = word.lower()
    if multiword_hit or w in MULTIWORD_TERMS or w in SINGLE_TERMS:
        return True
    if w in STOPWORDS or len(w) < 2:
        return False
    # acronyms (API, SSH) — original case check done on surface form separately
    if w.isupper() and 2 <= len(w) <= 6:
        return True
    if re.fullmatch(r"[a-z]+(?:-[a-z]+)+", w):  # multi-user, pre-built
        return True
    if re.search(
        r"(ware|pack|lang|script|config|server|client|daemon|kernel|module|binary|cache|hash|store|build|deploy|runtime|compile|install|package|depend)",
        w,
    ):
        return True
    return False


def surface_is_acronym(surface: str) -> bool:
    return bool(re.fullmatch(r"[A-Z]{2,6}", surface))


def suggestion_for(term: str) -> str:
    t = term.lower()
    if t in MULTIWORD_TERMS:
        return MULTIWORD_TERMS[t]
    if t in SINGLE_TERMS:
        return SINGLE_TERMS[t]
    return ""


def collect_from_doc(path: Path) -> tuple[Counter[str], Counter[str], set[str]]:
    """Returns (all_word_counts, tech_counts including multiword, tech_terms_set)."""
    raw = path.read_text(encoding="utf-8")
    prose = strip_code_and_markup(raw)

    multi = find_multiword(prose)
    words = find_words(prose)

    # Remove tokens that are only parts of counted multiword? keep both for inventory
    tech: Counter[str] = Counter()
    tech_set: set[str] = set()

    for phrase, n in multi.items():
        tech[phrase] += n
        tech_set.add(phrase)

    for w, n in words.items():
        if is_tech_word(w):
            tech[w] += n
            tech_set.add(w)

    # Also catch ALL-CAPS acronyms from original tokens
    for m in WORD_RE.finditer(prose):
        surface = m.group(0)
        if surface_is_acronym(surface):
            tech[surface.lower()] += 1
            tech_set.add(surface.lower())

    return words, tech, tech_set


def merge_into_glossary(
    glossary: dict,
    *,
    doc: str,
    all_words: Counter[str],
    tech_terms: set[str],
    tech_counts: Counter[str],
    include_non_tech: bool,
) -> tuple[int, int]:
    """Merge terms. Returns (new_entries, updated_docs)."""
    by_term = {e["term"].lower(): e for e in glossary["entries"]}
    if doc not in glossary["docs"]:
        glossary["docs"].append(doc)

    new = 0
    candidates: list[str]
    if include_non_tech:
        candidates = sorted(set(all_words) | tech_terms)
    else:
        candidates = sorted(tech_terms)

    for term in candidates:
        key = term.lower()
        is_tech = key in tech_terms or is_tech_word(key)
        if not include_non_tech and not is_tech:
            continue
        count = int(tech_counts.get(key, all_words.get(key, 0)))
        if key in by_term:
            e = by_term[key]
            docs = list(e.get("sources") or [])
            if doc not in docs:
                docs.append(doc)
            e["sources"] = docs
            e["count"] = max(int(e.get("count") or 0), count)
            e["is_tech"] = bool(e.get("is_tech")) or is_tech
            if not e.get("suggestion"):
                e["suggestion"] = suggestion_for(key)
            continue

        entry = {
            "term": key,
            "suggestion": suggestion_for(key),
            "translation": "",
            "notes": "",
            "sources": [doc],
            "count": count,
            "is_tech": is_tech,
            "status": "pending",  # pending | approved | skipped
        }
        glossary["entries"].append(entry)
        by_term[key] = entry
        new += 1

    return new, len(glossary["docs"])


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "docs",
        nargs="*",
        type=Path,
        help="Markdown files (default: GLOSSARY_SOURCE_DOCS or TRANSLATE_INPUT)",
    )
    parser.add_argument(
        "--all-words",
        action="store_true",
        help="Also list non-tech unique words (status=pending, is_tech=false)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="glossary.json path (default: GLOSSARY_PATH from .env)",
    )
    args = parser.parse_args(argv)

    out = args.output or env_path("GLOSSARY_PATH", "glossary.json")

    from tools.lib.envutil import ROOT

    if args.docs:
        docs = list(args.docs)
    else:
        raw = env_str("GLOSSARY_SOURCE_DOCS", "").strip()
        if raw in {"", "*", "all", "AUTO"}:
            en_root = env_path("NIX_DEV_OUTPUT", "docs/en")
            docs = sorted(en_root.rglob("*.md")) if en_root.is_dir() else []
            if not docs:
                print(f"No markdown under {en_root}", file=sys.stderr)
        else:
            docs = [Path(p.strip()) for p in raw.split(",") if p.strip()]

    glossary = load_glossary(out)
    total_new = 0

    for doc_path in docs:
        if not doc_path.is_file():
            alt = ROOT / doc_path
            if alt.is_file():
                doc_path = alt
            else:
                print(f"skip missing: {doc_path}", file=sys.stderr)
                continue

        # stable doc id = path relative to docs/en or filename
        try:
            en_root = env_path("NIX_DEV_OUTPUT", "docs/en")
            doc_id = str(doc_path.resolve().relative_to(en_root.resolve()))
        except Exception:
            doc_id = str(doc_path.name)

        all_words, tech_counts, tech_set = collect_from_doc(doc_path)
        new, _ = merge_into_glossary(
            glossary,
            doc=doc_id,
            all_words=all_words,
            tech_terms=tech_set,
            tech_counts=tech_counts,
            include_non_tech=args.all_words,
        )
        total_new += new
        print(
            f"{doc_path.name}: {len(all_words)} unique words, "
            f"{len(tech_set)} tech terms, +{new} new glossary entries",
            file=sys.stderr,
        )

    path = save_glossary(glossary, out)
    tech_n = sum(1 for e in glossary["entries"] if e.get("is_tech"))
    pending = sum(
        1
        for e in glossary["entries"]
        if e.get("is_tech") and e.get("status") == "pending" and not e.get("translation")
    )
    print(
        f"Wrote {path} — {len(glossary['entries'])} entries "
        f"({tech_n} tech, {pending} pending translation)",
        file=sys.stderr,
    )
    print(
        "Open /glossary-dev on the site to fill translations, then make translate.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
