"""Persian orthography fixes applied after AI translation (and via CLI).

Pipeline:
1. Project rules (ezafe after heh as ه‌ی, strip em/en dashes)
2. Wikipedia fa_bot.js *persianTools* port (`tools.lib.fa_bot`), adapted for this
   repo’s ezafe style, applied outside Markdown protected regions

Upstream bot:
  https://fa.wikipedia.org/wiki/ویکی‌پدیا:ویرایشگر_خودکار/ابرابزار/fa_bot.js

House style (differs from fa.wiki hamza-ezafe):
  ارائهٔ / ترجمه‌شدهٔ  →  ارائه‌ی / ترجمه‌شده‌ی   (heh + ZWNJ + yeh)
"""

from __future__ import annotations

import re
from pathlib import Path

from tools.lib.fa_bot import apply_fa_bot, replace_except

# Good ezafe after heh: heh + U+200C ZWNJ + yeh (ه‌ی)
_HEH_EZAFE_GOOD = "ه\u200cی"
# Bad: heh + U+0654 ARABIC HAMZA ABOVE; single-codepoint ۀ / ۂ / heh with yeh above
_HEH_HAMZA_EZAFE_RE = re.compile(
    r"ه\u0654"  # هٔ as heh + combining hamza
    r"|ۀ"  # U+06C0 ARABIC LETTER HEH WITH YEH ABOVE
    r"|ۂ"  # U+06C2
    r"|هٓ"  # heh + madda (nonstandard ezafe)
)
# U+2014 em dash, U+2013 en dash, U+2015 horizontal bar
_DASH_RE = re.compile(r"[\u2013\u2014\u2015]")

# Regions that must not be rewritten (Markdown / MyST / HTML / URLs)
_MD_EXCEPTIONS: list[re.Pattern[str]] = [
    # fenced code blocks (``` or ~~~)
    re.compile(r"(?m)^( {0,3})(`{3,}|~{3,}).*?\n[\s\S]*?^( {0,3})\2[^\n]*$", re.M),
    # indented code block (4 spaces / tab) — conservative: whole indented runs
    re.compile(r"(?m)(?:^(?: {4}|\t).*(?:\n|$))+"),
    # inline code
    re.compile(r"`+[^`\n]+`+"),
    # HTML comments
    re.compile(r"<!--[\s\S]*?-->"),
    # HTML tags (attributes often have English / digits / =)
    re.compile(r"</?[A-Za-z][^>\n]*>"),
    # autolinks / bare URLs
    re.compile(r"https?://[^\s)\]>\"']+"),
    re.compile(r"//[^\s)\]>\"']+"),
    # Markdown link/image destination: ](url) or ][ref]
    re.compile(r"\]\([^)]*\)"),
    re.compile(r"\]\[[^\]]*\]"),
    # reference-style link definitions
    re.compile(r"(?m)^\[[^\]]+\]:\s+\S+.*$"),
    # MyST / Sphinx roles with backticks: {term}`foo`, {ref}`...`
    re.compile(r"\{[a-zA-Z0-9_:-]+\}`[^`\n]*`"),
    # front-matter style (label) lines used in this repo: (install-nix)=
    re.compile(r"(?m)^\([A-Za-z0-9_./:-]+\)=\s*$"),
]


def fix_heh_ezafe(text: str) -> str:
    """House style: ezafe after heh is ه‌ی (ZWNJ+yeh), never hamza forms (هٔ / ۀ)."""
    if not text:
        return text
    return _HEH_HAMZA_EZAFE_RE.sub(_HEH_EZAFE_GOOD, text)


def fix_tarjome_ezafe(text: str) -> str:
    """Backward-compatible alias: all heh-ezafe forms use ZWNJ+yeh."""
    return fix_heh_ezafe(text)


def strip_em_dashes(text: str) -> str:
    """Replace em/en dashes with a comma (common Persian pause)."""
    if not text or not _DASH_RE.search(text):
        return text
    # "foo — bar" / "foo—bar" → "foo، bar"
    text = re.sub(r"\s*[\u2013\u2014\u2015]\s*", "، ", text)
    text = re.sub(r"،\s*،", "،", text)
    return text


def apply_fa_orthography(
    text: str,
    *,
    digits: bool = False,
    do_punctuation: bool = True,
    use_bot: bool = True,
) -> str:
    """All post-translation Persian orthography fixes."""
    if not text:
        return text
    text = strip_em_dashes(fix_heh_ezafe(text))
    if use_bot:
        text = replace_except(
            text,
            lambda chunk: apply_fa_bot(
                chunk,
                digits=digits,
                do_punctuation=do_punctuation,
            ),
            _MD_EXCEPTIONS,
        )
        # re-assert house ezafe style after bot
        text = fix_heh_ezafe(text)
        text = strip_em_dashes(text)
    return text


def fix_path(path: Path, *, dry_run: bool = False) -> int:
    """Fix one UTF-8 text file in place. Returns 1 if content changed, else 0."""
    raw = path.read_text(encoding="utf-8")
    fixed = apply_fa_orthography(raw)
    if fixed == raw:
        return 0
    if not dry_run:
        path.write_text(fixed, encoding="utf-8")
    return 1


def fix_tree(
    root: Path,
    *,
    globs: tuple[str, ...] = ("**/*.md", "**/*.svelte", "**/*.ts", "**/*.py", "**/*.json"),
    dry_run: bool = False,
) -> tuple[int, int]:
    """Fix matching files under *root*. Returns (files_changed, total_subs).

    *total_subs* is the number of files changed (full-file rewrite), not
    per-match counts — the bot applies many overlapping transforms.
    """
    files_changed = 0
    total = 0
    seen: set[Path] = set()
    skip_dirs = {
        "node_modules",
        "build",
        "build-webxdc",
        ".git",
        "__pycache__",
        ".svelte-kit",
    }
    for pattern in globs:
        for path in root.glob(pattern):
            if not path.is_file():
                continue
            if skip_dirs.intersection(path.parts):
                continue
            rp = path.resolve()
            if rp in seen:
                continue
            seen.add(rp)
            n = fix_path(path, dry_run=dry_run)
            if n:
                files_changed += 1
                total += n
    return files_changed, total


def main(argv: list[str] | None = None) -> int:
    """CLI: apply Persian orthography (fa_bot + project rules) to paths."""
    import argparse
    import sys

    from tools.lib.envutil import ROOT

    parser = argparse.ArgumentParser(
        description=(
            "Apply Persian orthography (Wikipedia fa_bot.js persianTools + "
            "project rules) to files. Markdown code/URLs are protected."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Files or directories (default: docs/fa)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report files that would change; do not write",
    )
    parser.add_argument(
        "--digits",
        action="store_true",
        help="Also convert Western/Arabic-Indic digits to Persian digits",
    )
    parser.add_argument(
        "--no-punctuation",
        action="store_true",
        help="Skip punctuation normalization",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print each changed path",
    )
    args = parser.parse_args(argv)

    targets = args.paths or [ROOT / "docs" / "fa"]
    files_changed = 0
    total = 0

    def _fix_one(path: Path) -> int:
        raw = path.read_text(encoding="utf-8")
        fixed = apply_fa_orthography(
            raw,
            digits=args.digits,
            do_punctuation=not args.no_punctuation,
        )
        if fixed == raw:
            return 0
        if not args.dry_run:
            path.write_text(fixed, encoding="utf-8")
        if args.verbose:
            print(f"{'[dry] ' if args.dry_run else ''}{path}", file=sys.stderr)
        return 1

    for t in targets:
        path = t if t.is_absolute() else ROOT / t
        if path.is_file():
            n = _fix_one(path)
            if n:
                files_changed += 1
                total += n
        elif path.is_dir():
            skip_dirs = {
                "node_modules",
                "build",
                "build-webxdc",
                ".git",
                "__pycache__",
                ".svelte-kit",
            }
            for md in sorted(path.rglob("*.md")):
                if skip_dirs.intersection(md.parts):
                    continue
                n = _fix_one(md)
                if n:
                    files_changed += 1
                    total += n
        else:
            print(f"skip missing: {path}", file=sys.stderr)

    print(
        f"{'Would fix' if args.dry_run else 'Fixed'} {total} file(s) "
        f"({files_changed} changed).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
