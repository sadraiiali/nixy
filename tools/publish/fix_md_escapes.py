#!/usr/bin/env python3
"""Fix mangled mdsvex/Svelte escapes in published Markdown pages.

Problems this addresses (seen e.g. on nix-manual command-ref pages):

1. **Double-escaped braces** — publish ran ``svelte_escape_braces`` on text that
   already contained ``{'{'}`` / ``{'}'}``, producing
   ``{'{'}'{'{'}'{'}'}`` / ``{'{'}'{'}'}'{'}'}``. Collapse to a single escape.
2. **Entity-escaped ``<span id>``** — ``&lt;span id="…"&gt;…&lt;/span&gt;``
   renders as literal text; restore real span tags (mdsvex-safe).
3. **Broken callout fences** — fence opens outside the blockquote while body
   lines still start with ``> `` (common publish artifact).
4. **Split inline code across newlines** — e.g. `` `nix\\nshell` `` from source
   soft-wraps; join into one span when both halves are simple tokens.
5. **Man-page synopsis** — multi-line / brace-escaped «خلاصه» / Synopsis blocks
   are rewritten to fenced ``text`` so Markdown does not merge lines and break
   backticks. Also applied from ``site_docs`` on publish (before brace escape).

**Idempotent:** every transform matches only the *broken* form. Running the
script twice (or N times) is a no-op after the first successful pass —
``fix(fix(text)) == fix(text)``. Main verifies this before writing.

Examples::

  uv run python -m tools.publish.fix_md_escapes
  uv run python -m tools.publish.fix_md_escapes --dry-run
  uv run python -m tools.publish.fix_md_escapes --self-test
  uv run python -m tools.publish.fix_md_escapes src/routes/pages/nix-manual
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from tools.lib.envutil import ROOT

# Single Svelte/mdsvex brace escapes (what publish should emit once)
BRACE_OPEN = "{'{'}"
BRACE_CLOSE = "{'}'}"

# Result of applying svelte_escape_braces() *once* to BRACE_OPEN / BRACE_CLOSE.
# These strings never appear in correctly published prose (only the singles do).
DOUBLE_BRACE_OPEN = "{'{'}'{'{'}'{'}'}"
DOUBLE_BRACE_CLOSE = "{'{'}'{'}'}'{'}'}"

# Fenced code blocks — leave body alone for prose-only transforms
FENCE_SPLIT_RE = re.compile(r"(```[^\n]*\n[\s\S]*?```)")

# &lt;span id="foo"&gt;…&lt;/span&gt;  (broken entity form only; real <span> ignored)
ENTITY_SPAN_ID_RE = re.compile(
    r"&lt;span\s+id=\"([A-Za-z][\w:.-]*)\"\s*&gt;"
    r"(.*?)"
    r"&lt;/span&gt;",
    re.DOTALL,
)
# Hybrid / mangled open-or-close (publish partially re-escaped):
#   &lt;span id="x"&gt;…</span>
#   <span id="x">…&lt;/span&gt;
#   <span id="x">…&lt;span&gt;   (bogus closer)
HYBRID_SPAN_OPEN_ENTITY_RE = re.compile(
    r"&lt;span\s+id=\"([A-Za-z][\w:.-]*)\"\s*&gt;"
    r"(.*?)"
    r"(?:</span>|&lt;/span&gt;|&lt;span&gt;)",
    re.DOTALL,
)
HYBRID_SPAN_CLOSE_ENTITY_RE = re.compile(
    r"<span\s+id=\"([A-Za-z][\w:.-]*)\"\s*>"
    r"(.*?)"
    r"(?:&lt;/span&gt;|&lt;span&gt;)",
    re.DOTALL,
)

# Fence opens at column 0, every body line is blockquoted, closer is quoted.
# After a correct fix the open is `> ```…` so this pattern no longer matches.
BROKEN_CALLOUT_FENCE_RE = re.compile(
    r"(?m)^```([^\n`]*)\n"  # open fence at BOL (not already quoted)
    r"((?:^[ \t]*>[ \t]?.*\n)+?)"  # one or more blockquoted lines
    r"^[ \t]*>[ \t]?```[ \t]*$",  # quoted closer
)

# Soft-wrapped *simple* tokens only — never joins synopsis option lines.
_SIMPLE_CODE_TOKEN = r"[\w./@%+=:-]+"
# `nix\nshell`  (one open, one close, newline inside)
SPLIT_INLINE_CODE_RE = re.compile(
    rf"`({_SIMPLE_CODE_TOKEN})\n[ \t]*({_SIMPLE_CODE_TOKEN})`"
)
# `nix`\nshell`  (premature close, orphan second half)
BROKEN_SPLIT_INLINE_CODE_RE = re.compile(
    rf"`({_SIMPLE_CODE_TOKEN})`\n[ \t]*({_SIMPLE_CODE_TOKEN})`"
)


def map_outside_fences(text: str, fn) -> str:
    """Apply ``fn`` only to non-fenced segments (fenced code left byte-identical)."""
    parts = FENCE_SPLIT_RE.split(text)
    out: list[str] = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out.append(part)  # fence
        else:
            out.append(fn(part))
    return "".join(out)


def collapse_double_brace_escapes(text: str) -> str:
    """Collapse double-escaped braces → single escape. Idempotent.

    Only replaces the exact double-escape strings. Correct singles
    (``{'{'}`` / ``{'}'}``) and bare ``{{`` rendered as two singles are untouched.
    """
    # Loop for triple+ escapes; each pass peels one level; stops when stable.
    prev = None
    while prev != text:
        prev = text
        if DOUBLE_BRACE_OPEN not in text and DOUBLE_BRACE_CLOSE not in text:
            break
        text = text.replace(DOUBLE_BRACE_OPEN, BRACE_OPEN)
        text = text.replace(DOUBLE_BRACE_CLOSE, BRACE_CLOSE)
    return text


def restore_entity_span_ids(text: str) -> str:
    """Normalize entity / hybrid span anchors to real ``<span id>…</span>``.

    Fully correct real spans do not match and stay unchanged (idempotent).
    """

    def repl(m: re.Match[str]) -> str:
        return f'<span id="{m.group(1)}">{m.group(2)}</span>'

    # Full entity form first, then hybrids.
    text = ENTITY_SPAN_ID_RE.sub(repl, text)
    text = HYBRID_SPAN_OPEN_ENTITY_RE.sub(repl, text)
    text = HYBRID_SPAN_CLOSE_ENTITY_RE.sub(repl, text)
    return text


def fix_broken_callout_fences(text: str) -> str:
    """Re-quote fences that open at BOL while body/closer stay blockquoted.

    After fix, open line is ``> ```lang`` so a second run does not match.
    """

    def repl(m: re.Match[str]) -> str:
        lang = (m.group(1) or "").rstrip()
        body = m.group(2)
        lines: list[str] = []
        for raw in body.splitlines():
            line = re.sub(r"^[ \t]*>[ \t]?", "", raw)
            lines.append(line)
        while lines and not lines[-1].strip():
            lines.pop()
        if not lines:
            return m.group(0)  # nothing to rewrite — leave unchanged
        quoted = "\n".join(f"> {ln}" if ln else ">" for ln in lines)
        return f"> ```{lang}\n{quoted}\n> ```"

    return BROKEN_CALLOUT_FENCE_RE.sub(repl, text)


def join_split_inline_code(text: str) -> str:
    """Join soft-wrapped / broken simple tokens. Already-joined spans: no match."""

    def repl(m: re.Match[str]) -> str:
        return f"`{m.group(1)} {m.group(2)}`"

    # Broken form first (`` `a`\\nb` ``), then soft wrap (`` `a\\nb` ``).
    text = BROKEN_SPLIT_INLINE_CODE_RE.sub(repl, text)
    text = SPLIT_INLINE_CODE_RE.sub(repl, text)
    return text


def fix_trailing_orphan_backtick(text: str) -> str:
    """Drop a stray `` ` `` after sentence end when the line's backticks are odd.

    Even count (balanced code) is left alone — safe if run again.
    """

    def fix_line(line: str) -> str:
        if not re.search(r"[.。!?…]`\s*$", line):
            return line
        if line.count("`") % 2 == 0:
            return line  # balanced — not an orphan
        return re.sub(r"([.。!?…])`(\s*)$", r"\1\2", line)

    return "\n".join(fix_line(L) for L in text.split("\n"))


# Man-page “Synopsis” / «خلاصه» headings (optional space: خلاصه‌دستور)
SYNOPSIS_HEADING_RE = re.compile(
    r"^(#{1,6})\s+.*(?:خلاصه\s*دستور|خلاصه|Synopsis)\s*.*$",
    re.IGNORECASE,
)


def _decode_svelte_braces(s: str) -> str:
    """``{'{'}`` / ``{'}'}`` (any depth of double-escape) → literal braces."""
    s = collapse_double_brace_escapes(s)
    return s.replace(BRACE_OPEN, "{").replace(BRACE_CLOSE, "}")


def synopsis_md_lines_to_plain(lines: list[str]) -> str:
    """Turn mangled synopsis Markdown lines into plain man-page text."""
    plain_lines: list[str] = []
    for line in lines:
        # keep relative indent (usually 0 or 2 spaces)
        lead_m = re.match(r"^[ \t]*", line)
        lead = lead_m.group(0) if lead_m else ""
        # normalize tabs → two spaces for lead
        lead = lead.replace("\t", "  ")
        if len(lead) >= 2:
            lead = "  "
        else:
            lead = ""
        body = line.strip()
        body = _decode_svelte_braces(body)
        body = body.replace("`", "")
        # *placeholder* / _placeholder_ → placeholder
        body = re.sub(r"\*([^*\n]+)\*", r"\1", body)
        body = re.sub(r"(?<![A-Za-z0-9])_([^_\n]+)_(?![A-Za-z0-9])", r"\1", body)
        body = re.sub(r"[ \t]+", " ", body).strip()
        plain_lines.append(lead + body if body else "")
    # drop trailing empties
    while plain_lines and not plain_lines[-1].strip():
        plain_lines.pop()
    return "\n".join(plain_lines)


def _looks_like_synopsis_line(line: str) -> bool:
    """Continuation / body line of a man-page synopsis (not normal prose)."""
    s = line.strip()
    if not s:
        return False
    if s.startswith("```"):
        return False
    if s.startswith("#"):
        return False
    # indented option lines
    if line.startswith("  ") or line.startswith("\t"):
        return True
    # command name / options / brace groups
    if s.startswith("`") or s.startswith("[") or s.startswith("{"):
        return True
    if s.startswith(BRACE_OPEN) or BRACE_OPEN in s or BRACE_CLOSE in s:
        return True
    # already-decoded braces from a partial fix
    if re.match(r"^[`\w./+-]+.*[{[]", s):
        return True
    return False


def _synopsis_needs_fence(lines: list[str]) -> bool:
    """True if body still has MD/Svelte forms that break in a paragraph."""
    blob = "\n".join(lines)
    if "`" in blob or "*" in blob:
        return True
    if BRACE_OPEN in blob or BRACE_CLOSE in blob:
        return True
    if DOUBLE_BRACE_OPEN in blob or DOUBLE_BRACE_CLOSE in blob:
        return True
    # multi-line synopsis without fence still merges in Markdown
    nonempty = [L for L in lines if L.strip()]
    return len(nonempty) > 1


def fix_man_synopsis_blocks(text: str) -> str:
    """Rewrite man-page synopsis sections as fenced ``text`` blocks.

    Markdown joins consecutive synopsis lines into one paragraph, so backticks
    pair across options and the block renders broken. A `````text`` fence keeps
    line structure and literal ``{ }`` (no Svelte escapes needed inside fences).

    Idempotent: an existing `````text`` fence after the heading is left alone.
    """
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        if not SYNOPSIS_HEADING_RE.match(line):
            out.append(line)
            i += 1
            continue

        out.append(line)
        i += 1

        # optional blank line(s) after heading (preserve count for stability)
        blanks: list[str] = []
        while i < n and not lines[i].strip():
            blanks.append(lines[i])
            i += 1

        # Already a fence → copy blanks + fence through unchanged (idempotent)
        if i < n and lines[i].lstrip().startswith("```"):
            out.extend(blanks)
            out.append(lines[i])
            i += 1
            while i < n:
                out.append(lines[i])
                done = lines[i].strip() == "```"
                i += 1
                if done:
                    break
            continue

        body: list[str] = []
        while i < n:
            L = lines[i]
            if re.match(r"^#{1,6}\s+", L):
                break
            if not L.strip():
                break
            if not _looks_like_synopsis_line(L):
                break
            body.append(L)
            i += 1

        if not body:
            # heading had only blanks / nothing — put blanks back
            out.extend(blanks)
            continue

        if not _synopsis_needs_fence(body):
            out.extend(blanks)
            out.extend(body)
            continue

        plain = synopsis_md_lines_to_plain(body)
        # always one blank between heading and fence (stable shape)
        out.append("")
        out.append("```text")
        out.extend(plain.split("\n"))
        out.append("```")

    result = "\n".join(out)
    if text.endswith("\n") and not result.endswith("\n"):
        result += "\n"
    return result


def fix_markdown_escapes(text: str) -> str:
    """Apply all fixes. **Idempotent:** ``fix(fix(t)) == fix(t)``."""
    # Braces may appear in synopsis (prose); double form is never intentional
    # inside fences either, so whole-file collapse is safe and idempotent.
    text = collapse_double_brace_escapes(text)

    # Man synopsis → ```text (before other prose edits; braces become literal)
    text = fix_man_synopsis_blocks(text)

    # Prose-only: do not rewrite content inside ``` fences.
    def prose_fixes(prose: str) -> str:
        prose = restore_entity_span_ids(prose)
        prose = join_split_inline_code(prose)
        prose = fix_trailing_orphan_backtick(prose)
        return prose

    text = map_outside_fences(text, prose_fixes)

    # Callout fence repair spans block structure; match only the broken shape.
    text = fix_broken_callout_fences(text)

    # Final brace peel in case a earlier step reintroduced doubles (it shouldn't).
    text = collapse_double_brace_escapes(text)
    return text


def assert_idempotent(text: str) -> str:
    """Return fixed text; raise if a second pass would change it again."""
    once = fix_markdown_escapes(text)
    twice = fix_markdown_escapes(once)
    if twice != once:
        raise RuntimeError(
            "fix_markdown_escapes is not idempotent — second pass differs. "
            "Refusing to write (would thrash on re-runs)."
        )
    return once


DEFAULT_TARGETS = [
    ROOT / "src/routes/pages/nix-manual/command-ref/nix-shell/+page.md",
]


def iter_md_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(
            p
            for p in path.rglob("*.md")
            if not any(
                part
                in {"node_modules", "build", "build-webxdc", ".git", "__pycache__"}
                for part in p.parts
            )
        )
    return []


def _self_test() -> int:
    """Built-in checks: broken → fixed, fixed stays fixed, clean stays clean."""
    samples: list[tuple[str, str]] = [
        (
            # double-escaped open/close around `{`--attr` | `-A`}`
            "[{'{'}'{'{'}'{'}'}`--attr` | `-A`{'{'}'{'}'}'{'}'} *x*]",
            "[{'{'}`--attr` | `-A`{'}'} *x*]",
        ),
        (
            # already single-escaped `{{…}}` shape — must not change on re-run
            "{'{'}{'{'}`--packages` | `-p`{'}'} {'{'}*p*{'}'} … | [*path*]{'}'}",
            "{'{'}{'{'}`--packages` | `-p`{'}'} {'{'}*p*{'}'} … | [*path*]{'}'}",
        ),
        (
            '- &lt;span id="env-X"&gt;[`X`](#env-X)&lt;/span&gt;',
            '- <span id="env-X">[`X`](#env-X)</span>',
        ),
        (
            "- <span id=\"env-X\">[`X`](#env-X)</span>",
            "- <span id=\"env-X\">[`X`](#env-X)</span>",
        ),
        (
            # hybrid: entity open + real close
            '- &lt;span id="opt-a"&gt;[`--a`](#opt-a)</span>',
            '- <span id="opt-a">[`--a`](#opt-a)</span>',
        ),
        (
            # hybrid: real open + bogus &lt;span&gt; closer
            '- <span id="opt-b">[`--b`](#opt-b)&lt;span&gt;',
            '- <span id="opt-b">[`--b`](#opt-b)</span>',
        ),

        (
            "دستور `nix`\nshell` و `man\nnix3-env-shell` پایان.`",
            "دستور `nix shell` و `man nix3-env-shell` پایان.",
        ),
        (
            "دستور `nix shell` و `man nix3-env-shell` پایان.",
            "دستور `nix shell` و `man nix3-env-shell` پایان.",
        ),
        (
            # broken callout fence
            "> **مثال**\n>\n\n```nix\n  > let\n  >   x = 1;\n  > ```\n",
            "> **مثال**\n>\n\n> ```nix\n> let\n>   x = 1;\n> ```\n",
        ),
        (
            # already correct callout fence — stable
            "> **مثال**\n>\n> ```nix\n> let\n>   x = 1;\n> ```\n",
            "> **مثال**\n>\n> ```nix\n> let\n>   x = 1;\n> ```\n",
        ),
        (
            # fence with > prompts must NOT be treated as broken callout
            # (closer not quoted with >)
            "```shell\n> not a callout\n```\n",
            "```shell\n> not a callout\n```\n",
        ),
        (
            # multi-line synopsis → text fence
            "## خلاصه دستور\n"
            "`nix-shell`\n"
            "  [`--arg` *name* *value*]\n"
            f"  [{BRACE_OPEN}`--attr` | `-A`{BRACE_CLOSE} *attrPath*]\n"
            "\n"
            "## بعدی\n",
            "## خلاصه دستور\n"
            "\n"
            "```text\n"
            "nix-shell\n"
            "  [--arg name value]\n"
            "  [{--attr | -A} attrPath]\n"
            "```\n"
            "\n"
            "## بعدی\n",
        ),
        (
            # single-line synopsis with braces
            "## خلاصه‌دستور\n"
            f"`nix-channel` {BRACE_OPEN}`--add` url | `--list`{BRACE_CLOSE}\n"
            "\n"
            "## توصیف\n",
            "## خلاصه‌دستور\n"
            "\n"
            "```text\n"
            "nix-channel {--add url | --list}\n"
            "```\n"
            "\n"
            "## توصیف\n",
        ),
        (
            # already fenced — stable
            "## خلاصه\n"
            "\n"
            "```text\n"
            "nix-daemon\n"
            "```\n"
            "\n"
            "## x\n",
            "## خلاصه\n"
            "\n"
            "```text\n"
            "nix-daemon\n"
            "```\n"
            "\n"
            "## x\n",
        ),
    ]

    failed = 0
    for i, (src, want) in enumerate(samples):
        got = assert_idempotent(src)
        if got != want:
            failed += 1
            print(f"FAIL sample {i}:\n  want: {want!r}\n  got:  {got!r}", file=sys.stderr)
        # second pass absolute no-op
        if fix_markdown_escapes(got) != got:
            failed += 1
            print(f"FAIL sample {i}: not stable on re-run", file=sys.stderr)

    if failed:
        print(f"self-test: {failed} failure(s)", file=sys.stderr)
        return 1
    print("self-test: ok (idempotent)", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Files or directories (default: nix-shell man page)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report changes only; do not write",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print each changed path",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run idempotency unit checks and exit",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    targets = args.paths or DEFAULT_TARGETS
    files: list[Path] = []
    for t in targets:
        p = t if t.is_absolute() else ROOT / t
        files.extend(iter_md_files(p))

    if not files:
        print("No Markdown files found.", file=sys.stderr)
        return 1

    changed = 0
    for path in files:
        raw = path.read_text(encoding="utf-8")
        try:
            fixed = assert_idempotent(raw)
        except RuntimeError as e:
            print(f"error: {path}: {e}", file=sys.stderr)
            return 1
        if fixed == raw:
            if args.verbose:
                print(f"unchanged: {path}", file=sys.stderr)
            continue
        changed += 1
        if args.verbose or args.dry_run:
            n_brace = raw.count(DOUBLE_BRACE_OPEN) + raw.count(DOUBLE_BRACE_CLOSE)
            n_span = len(ENTITY_SPAN_ID_RE.findall(raw))
            rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
            print(
                f"{'[dry] ' if args.dry_run else ''}{rel}"
                f"  (double-braces~{n_brace}, entity-spans={n_span})",
                file=sys.stderr,
            )
        if not args.dry_run:
            path.write_text(fixed, encoding="utf-8")

    print(
        f"{'Would fix' if args.dry_run else 'Fixed'} {changed} file(s) "
        f"({len(files)} scanned).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
