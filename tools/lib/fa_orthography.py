"""Persian orthography fixes applied after AI translation (and via CLI).

Rules:
- Always prefer tarjome + ZWNJ + yeh (ترجمه‌ی) over hamza-ezafe forms of the same word.
- Strip em/en dashes from model output (prefer comma / plain hyphen phrasing).
"""

from __future__ import annotations

import re
from pathlib import Path

# Bad: heh + U+0654 ARABIC HAMZA ABOVE  (common hamza-ezafe spelling)
# Bad: U+06C0 ARABIC LETTER HEH WITH YEH ABOVE (single-codepoint form after mim)
# Good: heh + U+200C ZWNJ + yeh
_TARJOME_BAD_HAMZA = "ترجمه\u0654"
_TARJOME_BAD_HEH_YEH = "ترجم\u06c0"
_TARJOME_GOOD = "ترجمه\u200cی"

_TARJOME_RE = re.compile(r"ترجم(?:ه\u0654|\u06c0)")
# U+2014 em dash, U+2013 en dash, U+2015 horizontal bar
_DASH_RE = re.compile(r"[\u2013\u2014\u2015]")


def fix_tarjome_ezafe(text: str) -> str:
    """Replace hamza-ezafe spellings of «tarjome» with ZWNJ+yeh form."""
    if not text:
        return text
    return _TARJOME_RE.sub(_TARJOME_GOOD, text)


def strip_em_dashes(text: str) -> str:
    """Replace em/en dashes with a comma (common Persian pause)."""
    if not text or not _DASH_RE.search(text):
        return text
    # "foo — bar" / "foo—bar" → "foo، bar"
    text = re.sub(r"\s*[\u2013\u2014\u2015]\s*", "، ", text)
    text = re.sub(r"،\s*،", "،", text)
    return text


def apply_fa_orthography(text: str) -> str:
    """All post-translation Persian orthography fixes (extend here later)."""
    return strip_em_dashes(fix_tarjome_ezafe(text))


def fix_path(path: Path, *, dry_run: bool = False) -> int:
    """Fix one UTF-8 text file in place. Returns number of substitutions."""
    raw = path.read_text(encoding="utf-8")
    fixed = apply_fa_orthography(raw)
    if fixed == raw:
        return 0
    n = len(_TARJOME_RE.findall(raw))
    if not dry_run:
        path.write_text(fixed, encoding="utf-8")
    return n


def fix_tree(
    root: Path,
    *,
    globs: tuple[str, ...] = ("**/*.md", "**/*.svelte", "**/*.ts", "**/*.py", "**/*.json"),
    dry_run: bool = False,
) -> tuple[int, int]:
    """Fix matching files under *root*. Returns (files_changed, total_subs)."""
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
    """CLI: rewrite hamza-ezafe «tarjome» → ZWNJ+yeh form in the repo (or given paths)."""
    import argparse
    import sys

    from tools.lib.envutil import ROOT

    parser = argparse.ArgumentParser(
        description=(
            "Replace hamza-ezafe spellings of the Persian word for translation "
            f"with {_TARJOME_GOOD!r} (heh + ZWNJ + yeh)."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Files or directories (default: whole repo under project root)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Count matches only; do not write",
    )
    args = parser.parse_args(argv)

    targets = args.paths or [ROOT]
    files_changed = 0
    total = 0
    for t in targets:
        path = t if t.is_absolute() else ROOT / t
        if path.is_file():
            n = fix_path(path, dry_run=args.dry_run)
            if n:
                files_changed += 1
                total += n
                print(f"{'[dry] ' if args.dry_run else ''}{path}: {n}", file=sys.stderr)
        elif path.is_dir():
            fc, n = fix_tree(path, dry_run=args.dry_run)
            files_changed += fc
            total += n
        else:
            print(f"skip missing: {path}", file=sys.stderr)

    print(
        f"{'Would fix' if args.dry_run else 'Fixed'} {total} occurrence(s) in {files_changed} file(s).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
