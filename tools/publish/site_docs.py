#!/usr/bin/env python3
"""Publish translated FA docs (full nix.dev tree) into SvelteKit routes.

docs/fa/**/*.md → src/routes/pages/nix-dev/**/+page.md
Also writes src/lib/nix-dev-nav.json for the site sidebar.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from tools.lib.envutil import ROOT, env_path, load_dotenv

ADMON_LABELS = {
    "note": "نکته",
    "tip": "راهنمایی",
    "warning": "هشدار",
    "important": "مهم",
    "caution": "احتیاط",
    "dropdown": "جزئیات",
    "seealso": "همچنین ببینید",
    "admonition": "توجه",
    "error": "خطا",
    "danger": "خطر",
    "hint": "راهنمایی",
    "attention": "توجه",
    # MyST class-style divs used heavily in nixpkgs: :::{.example #id}
    "example": "مثال",
}

# English titles on generic `{admonition} Title` blocks → FA
ADMON_TITLE_FA = {
    "example": "مثال",
    "examples": "مثال‌ها",
    "counter-example": "ضد مثال",
    "counter example": "ضد مثال",
    "counterexample": "ضد مثال",
    "مثال نقض": "ضد مثال",
}


def translate_admon_title(title: str) -> str:
    t = (title or "").strip()
    if not t:
        return ""
    return ADMON_TITLE_FA.get(t.casefold(), t)

# Lines after ```{code-block} that are MyST options
CODE_OPT = re.compile(r"^(\s*(?:>\s*)*):[a-zA-Z][\w-]*:\s*")
# Fence open with optional blockquote prefix
FENCE_OPEN = re.compile(
    r"^(\s*(?:>\s*)*)```\{([^}\n]+)\}(?:\s+([^\n]*))?$"
)
FENCE_PLAIN = re.compile(r"^(\s*(?:>\s*)*)```([^\n`]*)$")
FENCE_CLOSE = re.compile(r"^(\s*(?:>\s*)*)```\s*$")
# MyST directive open:
#   :::{tip} title
#   ::::{grid} 2
#   :::{.warning}          (class-style — common in nixpkgs)
#   ::: {.note}
#   :::{.example #ex-foo}  (class + optional #ids inside braces)
DIR_OPEN = re.compile(
    r"^(\s*)(:{3,6})\s*\{\s*"
    r"\.?"  # optional leading dot (div class syntax)
    r"([A-Za-z0-9_-]+)"
    r"((?:\s+#[A-Za-z][\w:.-]*)*)"  # optional #ids inside braces
    r"\s*\}(.*)$"
)
DIR_CLOSE = re.compile(r"^(\s*)(:{3,6})\s*$")
DIR_OPT = re.compile(r"^(\s*):([a-zA-Z][\w-]*)\s*:\s*(.*)$")


def strip_frontmatter(md: str) -> str:
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end != -1:
            rest = md[end + 4 :]
            return rest.lstrip("\n")
    return md


# Cached Nix / Nixpkgs version map for @nix-latest@ style placeholders
_VERSION_SUBS: dict[str, str] | None = None


def resolve_manual_versions() -> dict[str, str]:
    """Resolve mutable manual channels to concrete version strings.

    Uses live redirects from nix.dev plus published nix.dev pin files so
    single-page links like nix-2.35.html work.
    """
    global _VERSION_SUBS
    if _VERSION_SUBS is not None:
        return _VERSION_SUBS

    import urllib.error
    import urllib.request

    versions: dict[str, str] = {
        "nix-latest": "2.35",
        "nix-rolling": "2.34",
        "nix-stable": "2.34",
        "nix-prev-stable": "2.31",
        "nixpkgs-stable": "26.05",
        "nixpkgs-prev-stable": "25.11",
    }

    def head_location(url: str) -> str | None:
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=20) as resp:
                final = resp.geturl()
                m = re.search(r"/manual/nix/([^/]+)/?", final)
                return m.group(1) if m else None
        except Exception:
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=20) as resp:
                    final = resp.geturl()
                    m = re.search(r"/manual/nix/([^/]+)/?", final)
                    return m.group(1) if m else None
            except Exception:
                return None

    for key, channel in (
        ("nix-latest", "latest"),
        ("nix-rolling", "rolling"),
        ("nix-stable", "stable"),
        ("nix-prev-stable", "prev-stable"),
    ):
        ver = head_location(f"https://nix.dev/manual/nix/{channel}/")
        if ver and ver not in {"latest", "rolling", "stable", "prev-stable", "development"}:
            versions[key] = ver

    try:
        with urllib.request.urlopen(
            "https://raw.githubusercontent.com/NixOS/nix.dev/master/nix/sources.json",
            timeout=20,
        ) as resp:
            data = json.loads(resp.read().decode())
        pins = data.get("pins") or data
        # keys are release strings like "26.05"
        sorted_rel = sorted(
            (k for k in pins if re.fullmatch(r"\d+\.\d+", k)),
            key=lambda s: tuple(int(p) for p in s.split(".")),
        )
        if len(sorted_rel) >= 1:
            versions["nixpkgs-stable"] = sorted_rel[-1]
        if len(sorted_rel) >= 2:
            versions["nixpkgs-prev-stable"] = sorted_rel[-2]
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        pass

    _VERSION_SUBS = versions
    return versions


def substitute_version_placeholders(md: str) -> str:
    """Replace @nix-latest@ / @nixpkgs-stable@ tokens used by nix.dev."""
    subs = resolve_manual_versions()
    for key, val in subs.items():
        md = md.replace(f"@{key}@", val)
    return md


def toctree_to_markdown(
    md: str, ref_map: dict[str, str], base_dir: Path | None = None
) -> str:
    """Turn ```{toctree} … ``` into a bullet list of inline Markdown links.

    Sphinx toctrees are the only navigation on pages like reference/index.md.
    Dropping them left an empty page; external entries (Nixpkgs/NixOS manuals)
    become absolute https:// URLs so they remain accessible.
    """

    def resolve_entry(entry: str) -> str | None:
        entry = entry.strip()
        if not entry or entry.startswith(":"):
            return None

        # Title <url-or-path>
        title = ""
        target = entry
        m = re.match(r"^(.+?)\s*<([^>]+)>\s*$", entry)
        if m:
            title = m.group(1).strip()
            target = m.group(2).strip()

        # Absolute URL or site path → keep as-is
        if target.startswith(("http://", "https://", "mailto:", "/")):
            label = title or target
            return f"- [{label}]({target})"

        # Local path / myst doc
        path_part = target
        frag = ""
        if "#" in path_part:
            path_part, frag = path_part.split("#", 1)
            frag = "#" + frag

        # Normalize path
        rel = path_part
        if rel.startswith("./"):
            rel = rel[2:]
        if rel.endswith(".md"):
            stem_path = rel[:-3]
        else:
            stem_path = rel

        key = Path(stem_path).name
        href: str | None = None

        # Prefer path relative to this document (avoids stem collisions like
        # reference/pinning-nixpkgs vs tutorials/.../pinning-nixpkgs)
        if base_dir is not None:
            try:
                parts = list(base_dir.resolve().parts)
                if "fa" in parts:
                    fi = parts.index("fa")
                    sub = Path(*parts[fi + 1 :]) if fi + 1 < len(parts) else Path()
                    resolved = sub / stem_path
                    norm_parts: list[str] = []
                    for p in resolved.parts:
                        if p == "..":
                            if norm_parts:
                                norm_parts.pop()
                        elif p != ".":
                            norm_parts.append(p)
                    cand = "/".join(norm_parts)
                    for trial in (
                        cand,
                        cand.replace("/", "-"),
                        Path(cand).name,
                    ):
                        if trial in ref_map:
                            href = ref_map[trial]
                            break
                    if not href:
                        route_parts = [p for p in cand.split("/") if p]
                        if route_parts and route_parts[-1] == "index":
                            route_parts = route_parts[:-1]
                        href = "/pages/nix-dev/" + "/".join(route_parts)
            except Exception:
                href = None

        if not href:
            href = (
                ref_map.get(stem_path)
                or ref_map.get(stem_path.replace("/", "-"))
                or ref_map.get(key)
                or ref_map.get(key.replace("_", "-"))
            )

        if not href:
            href = target if target.startswith("/") else f"/pages/nix-dev/{stem_path}"

        href = href + frag
        label = title or key.replace("-", " ").replace("_", " ")
        return f"- [{label}]({href})"

    def replace_block(m: re.Match) -> str:
        body = m.group(1)
        items: list[str] = []
        for line in body.splitlines():
            line = line.strip()
            if not line or line.startswith(":"):
                continue
            # skip glob-only noise
            if line in {"*", "**/*"}:
                continue
            row = resolve_entry(line)
            if row:
                items.append(row)
        if not items:
            return ""
        return "\n".join(items) + "\n"

    return re.sub(r"```\{toctree\}([\s\S]*?)```", replace_block, md)


def convert_myst_code_fences(md: str, base_dir: Path | None = None) -> str:
    """```{code-block} / ```{literalinclude} → fenced code for mdsvex.

    * ``:caption:`` becomes a bold label above the fence
    * ``literalinclude`` inlines file contents from *base_dir* (or CWD)
    """
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_code = False
    while i < len(lines):
        line = lines[i]
        if not in_code:
            m = FENCE_OPEN.match(line)
            if m:
                prefix, directive, rest = m.group(1), m.group(2).strip(), (m.group(3) or "").strip()
                # --- literalinclude: expand external file into a fence ---
                if directive == "literalinclude":
                    include_path = rest.split()[0] if rest.split() else ""
                    lang = "text"
                    caption = ""
                    i += 1
                    while i < len(lines) and (
                        CODE_OPT.match(lines[i]) or FENCE_CLOSE.match(lines[i])
                    ):
                        if FENCE_CLOSE.match(lines[i]):
                            i += 1
                            break
                        opt = lines[i]
                        lm = re.match(
                            r"^(\s*(?:>\s*)*):language:\s*(\S+)", opt
                        )
                        cm = re.match(
                            r"^(\s*(?:>\s*)*):caption:\s*(.*)$", opt
                        )
                        if lm:
                            lang = lm.group(2).strip()
                        if cm and cm.group(2).strip():
                            caption = cm.group(2).strip()
                        i += 1
                    else:
                        # consume until fence close if options loop exited differently
                        while i < len(lines) and not FENCE_CLOSE.match(lines[i]):
                            i += 1
                        if i < len(lines) and FENCE_CLOSE.match(lines[i]):
                            i += 1

                    if lang in {"shell-session", "console"}:
                        lang = "shell"
                    if lang in {"default", "text", "none", ""}:
                        # guess from extension
                        if include_path.endswith(".nix"):
                            lang = "nix"
                        elif include_path.endswith((".bash", ".sh")):
                            lang = "bash"
                        else:
                            lang = "text"

                    # resolve include relative to the markdown file
                    body = ""
                    if include_path and base_dir is not None:
                        cand = (base_dir / include_path).resolve()
                        try:
                            # stay under docs/ for safety
                            cand.relative_to(ROOT.resolve())
                            if cand.is_file():
                                body = cand.read_text(encoding="utf-8")
                        except (ValueError, OSError):
                            body = ""
                    if not body and include_path:
                        # last resort: search under docs/
                        for hit in ROOT.joinpath("docs").rglob(Path(include_path).name):
                            try:
                                body = hit.read_text(encoding="utf-8")
                                break
                            except OSError:
                                continue

                    if not caption and include_path:
                        caption = Path(include_path).name
                    if caption:
                        out.append(f"{prefix}**`{caption}`**")
                        out.append("")
                    out.append(f"{prefix}```{lang}")
                    if body:
                        # strip trailing newlines then emit
                        for bl in body.rstrip("\n").splitlines():
                            out.append(f"{prefix}{bl}" if prefix else bl)
                    else:
                        out.append(f"{prefix}# missing include: {include_path}")
                    out.append(f"{prefix}```")
                    out.append("")
                    continue

                # code-block / code → first word of rest is language
                if directive in {"code-block", "code", "sourcecode", "highlight"}:
                    parts = rest.split()
                    lang = parts[0] if parts else "text"
                elif directive in {"toctree", "eval-rst", "raw"}:
                    # drop entire fence block
                    i += 1
                    while i < len(lines) and not FENCE_CLOSE.match(lines[i]):
                        i += 1
                    if i < len(lines):
                        i += 1
                    continue
                else:
                    # ```{glossary} etc. → plain text fence or drop
                    lang = "text"
                if lang in {"shell-session", "console", "shell-session"}:
                    lang = "shell"
                if lang in {"default", "text", "none", ""}:
                    lang = "text"
                # Collect :caption: etc. before body (do not drop captions silently)
                caption = ""
                i += 1
                while i < len(lines) and CODE_OPT.match(lines[i]):
                    opt = lines[i]
                    cm = re.match(
                        r"^(\s*(?:>\s*)*):caption:\s*(.*)$", opt
                    )
                    if cm and cm.group(2).strip():
                        caption = cm.group(2).strip()
                    i += 1
                if caption:
                    # Visible file label above the fence (was MyST :caption:)
                    out.append(f"{prefix}**`{caption}`**")
                    out.append("")
                out.append(f"{prefix}```{lang}")
                in_code = True
                continue
            m2 = FENCE_PLAIN.match(line)
            if m2 and line.strip().startswith("```"):
                info = (m2.group(2) or "").strip()
                # normalize shell aliases on plain fences
                if info in {"shell-session", "console"}:
                    out.append(f"{m2.group(1)}```shell")
                else:
                    out.append(line)
                in_code = True
                i += 1
                continue
            out.append(line)
            i += 1
        else:
            if FENCE_CLOSE.match(line) or (
                line.strip().startswith("```") and line.strip().rstrip("`") == ""
            ) or re.match(r"^(\s*(?:>\s*)*)```\s*$", line):
                # close fence — keep only backticks (with quote prefix)
                pref = re.match(r"^(\s*(?:>\s*)*)", line)
                out.append(f"{pref.group(1) if pref else ''}```")
                in_code = False
            else:
                out.append(line)
            i += 1
    return "\n".join(out) + "\n"


def convert_grids_and_directives(md: str, ref_map: dict[str, str]) -> str:
    """Turn MyST grid/card/admonition/dropdown into simple markdown."""
    lines = md.splitlines()
    out: list[str] = []
    # stack of (colons_count, kind, title, options, body_lines)
    stack: list[dict] = []

    def flush_leaf(item: dict) -> list[str]:
        kind = item["kind"]
        title = item["title"].strip()
        opts = item["opts"]
        body = "\n".join(item["body"]).strip()
        anchor_ids: list[str] = list(item.get("ids") or [])
        rows: list[str] = []

        def prepend_anchors() -> None:
            for aid in anchor_ids:
                if aid:
                    rows.append(f'<a id="{aid}"></a>')

        if kind in {"grid", "grid-item", "grid-item-card", "card", "dropdown"} or kind.endswith(
            "-card"
        ):
            link = opts.get("link", "")
            if link:
                href = ref_map.get(link) or ref_map.get(link.replace("_", "-")) or link
                if not href.startswith("/") and not href.startswith("http"):
                    href = ref_map.get(href, f"/pages/nix-dev/{href}")
                label = title or link
                if body:
                    rows.append(f"- **[{label}]({href})** — {body}")
                else:
                    rows.append(f"- [{label}]({href})")
            else:
                if title:
                    rows.append(f"### {title}" if kind != "dropdown" else f"**{title}**")
                if body:
                    rows.append(body)
            return rows

        if kind in ADMON_LABELS or kind in {
            "note",
            "tip",
            "warning",
            "important",
            "caution",
            "seealso",
            "hint",
            "error",
            "danger",
            "attention",
            "admonition",
            "dropdown",
            "example",
        }:
            # Full blockquote (title + body) so the whole callout is highlighted
            # like nix.dev admonitions. Fenced code stays valid when every line
            # is prefixed with "> ".
            label = ADMON_LABELS.get(kind, kind)
            kind_cls = kind if kind in ADMON_LABELS else "note"
            title_fa = translate_admon_title(title)
            # Generic “Example” admonitions → just **مثال** (no “توجه: Example”)
            if title_fa and title_fa.casefold() in {
                v.casefold() for v in ADMON_TITLE_FA.values()
            }:
                head = f"**{title_fa}**"
            else:
                head = f"**{label}**" + (f": {title_fa}" if title_fa else "")
            # Structure (CommonMark blockquote):
            #   kind marker (own line) → title paragraph → body
            # so title + body share one highlighted blockquote.
            prepend_anchors()
            rows.append(f'> <span class="admonition-kind" data-kind="{kind_cls}"></span>')
            rows.append(">")
            rows.append(f"> {head}")
            rows.append(">")
            if body:
                for bl in body.splitlines():
                    if bl.strip() == "":
                        rows.append(">")
                    else:
                        rows.append(f"> {bl}")
            rows.append("")
            return rows

        # unknown directive: keep title + body
        prepend_anchors()
        if title:
            rows.append(f"**{title}**")
        if body:
            rows.append(body)
        rows.append("")
        return rows

    i = 0
    while i < len(lines):
        line = lines[i]
        # inside a collected body we still parse nested opens
        m_close = DIR_CLOSE.match(line)
        m_open = DIR_OPEN.match(line)

        if m_open:
            colons = len(m_open.group(2))
            kind = m_open.group(3).lower()
            ids_raw = (m_open.group(4) or "").strip()
            title = (m_open.group(5) or "").strip()
            ids = [x[1:] for x in re.findall(r"#[A-Za-z][\w:.-]*", ids_raw)]
            # skip pure layout grids wrapping — still open stack
            item = {
                "colons": colons,
                "kind": kind,
                "title": title,
                "ids": ids,
                "opts": {},
                "body": [],
            }
            i += 1
            # option lines immediately after open
            while i < len(lines):
                om = DIR_OPT.match(lines[i])
                if om and not lines[i].strip().startswith("```"):
                    item["opts"][om.group(2)] = om.group(3).strip()
                    i += 1
                    continue
                break
            stack.append(item)
            continue

        if m_close and stack:
            colons = len(m_close.group(2))
            # Close nested directives that are deeper than this closer
            while stack and stack[-1]["colons"] > colons:
                item = stack.pop()
                rendered = flush_leaf(item)
                if stack:
                    stack[-1]["body"].extend(rendered)
                else:
                    out.extend(rendered)
            if stack and stack[-1]["colons"] == colons:
                item = stack.pop()
                rendered = flush_leaf(item)
                if stack:
                    stack[-1]["body"].extend(rendered)
                else:
                    out.extend(rendered)
            i += 1
            continue

        if stack:
            stack[-1]["body"].append(line)
        else:
            out.append(line)
        i += 1

    # unclosed leftovers
    while stack:
        item = stack.pop()
        rendered = flush_leaf(item)
        if stack:
            stack[-1]["body"].extend(rendered)
        else:
            out.extend(rendered)

    return "\n".join(out) + "\n"


def svelte_escape_braces(text: str) -> str:
    """Emit literal braces for mdsvex→Svelte (HTML entities get decoded and break).

    Must use placeholders so the closing brace inside ``{'{'}`` is not
    re-escaped by a second ``.replace('}', …)`` pass.
    """
    return (
        text.replace("{", "\0OB\0")
        .replace("}", "\0CB\0")
        .replace("\0OB\0", "{'{'}")
        .replace("\0CB\0", "{'}'}")
    )


def escape_htmlish_tags(text: str) -> str:
    """Escape <tag>-like runs so Svelte/markdown don't treat them as DOM nodes.

    Protects intentional callout markers we inject and a few safe HTML tags
    (e.g. ``<cite>`` for paper attributions).
    """
    protected: list[str] = []

    def protect(m: re.Match) -> str:
        protected.append(m.group(0))
        return f"\0H{len(protected) - 1}\0"

    text = re.sub(
        r'<span class="admonition-kind"[^>]*></span>',
        protect,
        text,
    )
    # Real attribution markup from docs (keep as HTML for mdsvex)
    text = re.sub(
        r"</?cite\b[^>]*>",
        protect,
        text,
        flags=re.IGNORECASE,
    )
    # Section anchors from MyST labels: <a id="names-values"></a>
    text = re.sub(
        r'<a\s+id="[A-Za-z0-9_.:-]+"\s*></a>',
        protect,
        text,
        flags=re.IGNORECASE,
    )
    # XML prolog / processing instructions (`<?xml …?>`) — Svelte rejects `<?`
    text = re.sub(r"<\?", "&lt;?", text)
    text = re.sub(r"\?>", "?&gt;", text)
    # <bindings>, <body>, <nixpkgs>, etc.
    text = re.sub(r"<(/?[A-Za-z][\w:.-]*)([^>\n]*)>", r"&lt;\1\2&gt;", text)
    # Bare comparisons like `1.0 < 2.3` — Svelte treats `< 2` as an invalid tag
    # (do not allow bare `?` through either)
    text = re.sub(r"<(?![/A-Za-z!\0])", "&lt;", text)
    for i, html in enumerate(protected):
        text = text.replace(f"\0H{i}\0", html)
    return text


def escape_braces_outside_code(md: str) -> str:
    """Svelte treats { } as expressions — escape in prose only.

    Fenced code is left intact; mdsvex highlight() escapes braces for Svelte.
    """
    parts: list[str] = []
    chunks = re.split(r"(```[\s\S]*?```)", md)
    for i, chunk in enumerate(chunks):
        if i % 2 == 1:
            parts.append(chunk)
        else:
            segs = re.split(r"(`[^`\n]+`)", chunk)
            buf = []
            for j, s in enumerate(segs):
                if j % 2 == 1:
                    # inline code → keep readable; use Svelte brace exprs
                    inner = s[1:-1]
                    buf.append(
                        "`"
                        + svelte_escape_braces(escape_htmlish_tags(inner))
                        + "`"
                    )
                else:
                    buf.append(svelte_escape_braces(escape_htmlish_tags(s)))
            parts.append("".join(buf))
    return "".join(parts)


def _resolve_include_md(
    entry: str,
    *,
    base_dir: Path,
    content_root: Path | None,
) -> Path | None:
    """Resolve a MyST ``{=include=}`` entry to an on-disk markdown file."""
    name = entry.strip()
    if not name or name.startswith("#"):
        return None
    # Download renames *.chapter.md / *.section.md → *.md
    candidates = [name]
    for suffix in (".chapter.md", ".section.md"):
        if name.endswith(suffix):
            candidates.append(name[: -len(suffix)] + ".md")
    if name.endswith(".md") and not any(
        name.endswith(s) for s in (".chapter.md", ".section.md")
    ):
        stem = name[: -len(".md")]
        candidates.extend([f"{stem}.chapter.md", f"{stem}.section.md"])

    search_roots = [base_dir]
    if content_root is not None:
        search_roots.append(content_root)

    for cand in candidates:
        for root in search_roots:
            p = (root / cand).resolve()
            if p.is_file():
                return p
            # try basename match under root
            hits = list(root.rglob(Path(cand).name))
            if hits:
                return hits[0]
    return None


def expand_myst_equals_include(
    md: str,
    *,
    base_dir: Path | None,
    content_root: Path | None,
    site_prefix: str,
) -> str:
    """Turn Sphinx/MyST `` ```{=include=} … ``` `` into a markdown link list.

    Nixpkgs hub pages only list chapter files; without this the site shows raw
    English filenames after strip.
    """
    if base_dir is None:
        return md

    def repl(m: re.Match) -> str:
        body = m.group(1)
        lines_out: list[str] = []
        for raw_line in body.splitlines():
            entry = raw_line.strip()
            if not entry or entry.startswith("#"):
                continue
            path = _resolve_include_md(
                entry, base_dir=base_dir, content_root=content_root
            )
            if path is None:
                label = Path(entry).stem.replace(".chapter", "").replace(".section", "")
                lines_out.append(f"- `{label}`")
                continue
            try:
                if content_root is not None:
                    rel = path.resolve().relative_to(content_root.resolve())
                else:
                    rel = path.relative_to(base_dir)
            except ValueError:
                rel = Path(path.name)
            route = fa_rel_to_route(rel, site_prefix=site_prefix)
            try:
                title = extract_title(path.read_text(encoding="utf-8"), path.stem)
            except OSError:
                title = path.stem
            lines_out.append(f"- [{title}]({route})")
        if not lines_out:
            return ""
        return "\n".join(lines_out) + "\n"

    return re.sub(
        r"```\{=include=\}[^\n]*\n([\s\S]*?)```",
        repl,
        md,
    )


def strip_myst(
    md: str,
    ref_map: dict[str, str],
    base_dir: Path | None = None,
    *,
    site_prefix: str = "/pages/nix-dev",
    content_root: Path | None = None,
) -> str:
    md = strip_frontmatter(md)

    # Nixpkgs / Sphinx part pages: expand include lists to local TOC links
    md = expand_myst_equals_include(
        md,
        base_dir=base_dir,
        content_root=content_root,
        site_prefix=site_prefix,
    )

    # Drop HTML comments (mdBook TODOs / author notes). Multi-line comments that
    # contain list markers break CommonMark/mdsvex nesting and produce invalid
    # Svelte like `</p>` with no open tag.
    md = re.sub(r"<!--[\s\S]*?-->", "", md)

    # Collect in-document anchors:
    #   MyST labels: (names-values)=
    #   mdBook heading anchors: ### Title {#type-attrs}
    local_labels: set[str] = set(
        re.findall(r"(?m)^\(([a-zA-Z0-9_-]+)\)=\s*$", md)
    )
    local_labels.update(re.findall(r"\{#([a-zA-Z0-9_-]+)\}", md))

    # mdBook / rustdoc anchors MUST become real HTML ids before
    # svelte_escape_braces turns `{#id}` into the literal text `{'{'}#id{'}'}`.
    #   ### Title {#type-int}     →  ### Title <a id="type-int"></a>
    #   - [term]{#gloss-foo}      →  - [term]<a id="gloss-foo"></a>
    #   []{#sect-…}               →  <a id="sect-…"></a>
    def convert_mdbook_ids(chunk: str) -> str:
        # Empty markdown links used only for anchors: []{#id} → <a id="id"></a>
        chunk = re.sub(
            r"\[\]\{#([A-Za-z][\w:.-]*)\}",
            r'<a id="\1"></a>',
            chunk,
        )
        # Headings: put id first so the element is easy to find.
        # Use [ \t] not \s before $ — \s*$ would eat blank lines after the last
        # heading in a prose chunk, gluing the next ```fence onto the heading
        # (e.g. `postBuild````nix) and breaking mdsvex/Svelte.
        chunk = re.sub(
            r"^(#{1,6})[ \t]+(.+?)[ \t]*\{#([A-Za-z][\w:.-]*)\}[ \t]*$",
            lambda m: f'{m.group(1)} <a id="{m.group(3)}"></a> {m.group(2).rstrip()}',
            chunk,
            flags=re.M,
        )
        # Remaining {#id} (list items, mid-paragraph)
        chunk = re.sub(
            r"\{#([A-Za-z][\w:.-]*)\}",
            r'<a id="\1"></a>',
            chunk,
        )
        # Leftover empty [] before injected anchors
        chunk = re.sub(r"\[\](?=\s*<a\s+id=)", "", chunk)
        return chunk

    # Only outside fenced code
    _parts: list[str] = []
    for _i, _chunk in enumerate(re.split(r"(```[\s\S]*?```)", md)):
        if _i % 2 == 1:
            _parts.append(_chunk)
        else:
            _parts.append(convert_mdbook_ids(_chunk))
    md = "".join(_parts)

    # Merge label into the following heading so Markdown still parses the heading.
    # (label)=\n## Title  →  ## <a id="label"></a> Title
    # Bare labels with no following heading become a standalone anchor + blank line.
    def label_to_anchor(m: re.Match) -> str:
        lid = m.group(1)
        rest = m.group(2) or ""
        hm = re.match(r"(#{1,6})\s+(.+)", rest)
        if hm:
            return f"{hm.group(1)} <a id=\"{lid}\"></a> {hm.group(2)}"
        return f'<a id="{lid}"></a>\n'

    md = re.sub(
        r"(?m)^\(([a-zA-Z0-9_-]+)\)=\s*\n([^\n]*)",
        label_to_anchor,
        md,
    )
    # leftover labels with nothing on next line
    md = re.sub(
        r"(?m)^\(([a-zA-Z0-9_-]+)\)=\s*$",
        lambda m: f'<a id="{m.group(1)}"></a>\n',
        md,
    )

    # Version placeholders from nix.dev Sphinx preprocess (@nix-latest@, …)
    md = substitute_version_placeholders(md)

    # nix.dev/manual/nix/{ver}/… → local FA manual routes when we have the page
    md = rewrite_nix_manual_urls(md)

    # toctree → bullet list of inline links (keep external manuals accessible)
    md = toctree_to_markdown(md, ref_map, base_dir=base_dir)

    # 1) Normalize MyST code fences FIRST (before any `{word}` rewrites)
    #    Expand literalinclude using *base_dir* (directory of the source .md).
    md = convert_myst_code_fences(md, base_dir=base_dir)

    # 2) Grids / admonitions / dropdowns (body may contain normal fences)
    md = convert_grids_and_directives(md, ref_map)

    # 3) Re-run fence conversion (directives may have re-exposed nested fences)
    md = convert_myst_code_fences(md, base_dir=base_dir)

    def ref_sub(m: re.Match) -> str:
        inner = m.group(1).strip()
        if "<" in inner and ">" in inner:
            text, _, rest = inner.rpartition("<")
            rid = rest.replace(">", "").strip()
            text = text.strip() or rid
        else:
            rid = inner
            text = inner
        href = ref_map.get(rid) or ref_map.get(rid.replace("_", "-"))
        if not href:
            href = f"https://nix.dev/search.html?q={rid}"
        return f"[{text}]({href})"

    md = re.sub(r"\{ref\}`([^`]+)`", ref_sub, md)
    md = re.sub(r"\{term\}`([^`]+)`", r"*\1*", md)
    md = re.sub(r"\{doc\}`([^`]+)`", r"*\1*", md)
    md = re.sub(r"\{any\}`([^`]+)`", r"*\1*", md)
    md = re.sub(r"\{command\}`([^`]+)`", r"`\1`", md)
    md = re.sub(r"\{file\}`([^`]+)`", r"`\1`", md)
    md = re.sub(r"\{py:mod\}`([^`]+)`", r"`\1`", md)

    def role_sub(m: re.Match) -> str:
        """{download}`name <path>` / {guilabel}`X` → plain markdown."""
        _role, inner = m.group(1), m.group(2).strip()
        if "<" in inner and ">" in inner:
            text, _, rest = inner.rpartition("<")
            text = text.strip() or rest.replace(">", "").strip()
        else:
            text = inner
        return f"`{text}`"

    # Generic MyST roles: {name}`content` (not fence info strings)
    md = re.sub(r"\{([A-Za-z][\w:-]*)\}`([^`]+)`", role_sub, md)

    def link_sub(m: re.Match) -> str:
        text, target = m.group(1), m.group(2).strip().strip("<>")
        # Already absolute site or external URLs — do not remap
        if target.startswith(("http://", "https://", "mailto:", "/")):
            return m.group(0)
        # Pure in-page fragment: [text](#type-attrs) — never invent a path
        if target.startswith("#") or target == "":
            return m.group(0)
        # In-page MyST / mdBook label: [text](names-values) → [text](#names-values)
        if target in local_labels or target.lstrip("#") in local_labels:
            rid = target.lstrip("#")
            return f"[{text.strip() or rid}](#{rid})"
        if target in ref_map:
            return f"[{text.strip() or target}]({ref_map[target]})"
        t = target
        frag = ""
        if "#" in t:
            t, frag = t.split("#", 1)
            frag = "#" + frag
        # Fragment-only after split (e.g. malformed "#id" already handled above)
        if not t:
            return f"[{text}]({frag})" if frag else m.group(0)
        if t.endswith(".md"):
            t = t[:-3]
        if t.startswith("./"):
            t = t[2:]

        # Prefer path relative to content root (nix-dev tree or nix-manual tree)
        if base_dir is not None:
            try:
                if content_root is not None:
                    try:
                        sub = base_dir.resolve().relative_to(content_root.resolve())
                    except ValueError:
                        sub = Path()
                    resolved = (sub / t) if t else sub
                else:
                    parts = list(base_dir.resolve().parts)
                    if "fa" in parts:
                        fi = parts.index("fa")
                        sub = (
                            Path(*parts[fi + 1 :]) if fi + 1 < len(parts) else Path()
                        )
                    else:
                        sub = Path()
                    resolved = sub / t if t else sub
                norm: list[str] = []
                for p in resolved.parts:
                    if p == "..":
                        if norm:
                            norm.pop()
                    elif p not in {".", ""}:
                        norm.append(p)
                full = "/".join(norm)
                if full in ref_map:
                    return f"[{text.strip() or Path(full).name}]({ref_map[full]}{frag})"
                # build route from full relative path under this content tree
                rparts = [p for p in norm if p]
                # When resolving under docs/fa without content_root, drop a leading
                # nix-manual/ segment if site_prefix is the manual site root.
                if (
                    site_prefix.rstrip("/") == "/pages/nix-manual"
                    and rparts
                    and rparts[0] == "nix-manual"
                ):
                    rparts = rparts[1:]
                if rparts and rparts[-1] == "index":
                    rparts = rparts[:-1]
                href = site_prefix.rstrip("/") + (
                    ("/" + "/".join(rparts)) if rparts else ""
                )
                return f"[{text.strip() or (rparts[-1] if rparts else t)}]({href}{frag})"
            except Exception:
                pass

        if t in ref_map:
            return f"[{text.strip() or t}]({ref_map[t]}{frag})"
        # Bare path-like ref that is only a fragment id (no slash, no scheme)
        if re.fullmatch(r"[a-zA-Z0-9_-]+", t) and t in local_labels:
            return f"[{text.strip() or t}](#{t})"
        key = Path(t).name
        if key in ref_map:
            return f"[{text.strip() or key}]({ref_map[key]}{frag})"
        return m.group(0)

    md = re.sub(r"\[([^\]]*)\]\(\s*<?([^)\s]+)>?\s*\)", link_sub, md)

    def map_outside_fences(text: str, fn) -> str:
        """Apply fn only to non-fenced regions so Nix/code is never mangled."""
        parts: list[str] = []
        chunks = re.split(r"(```[\s\S]*?```)", text)
        for i, chunk in enumerate(chunks):
            if i % 2 == 1:
                parts.append(chunk)
            else:
                parts.append(fn(chunk))
        return "".join(parts)

    def clean_prose_myst(chunk: str) -> str:
        # Only drop trivial MyST single-token lines like `{glossary}` — NOT Nix
        # lines such as `{ pkgs ? import (fetchTarball "…") {}`.
        chunk = re.sub(r"(?m)^\{[A-Za-z][\w.-]*\}\s*$", "", chunk)
        # Broken/translated MyST code options that became lines like:
        #   {lineno-start=1}
        #   {lineno-start=1 emphasize-lines="2"}
        chunk = re.sub(
            r"(?m)^\{(?=[^\n]*(?:lineno-start|emphasize-lines|linenos|caption|name)\s*=)[^\n]+\}\s*$",
            "",
            chunk,
        )
        chunk = re.sub(
            r"(?m)^:(?:class|emphasize-lines|caption|name|linenos|lineno-start):[^\n]*$",
            "",
            chunk,
        )
        chunk = re.sub(r"(?m)^:{3,6}\s*\{?\s*$", "", chunk)
        chunk = re.sub(r"(?m)^:{3,6}\s*\{\.?[A-Za-z0-9_-]*\s*$", "", chunk)

        def leftover_dir(m: re.Match) -> str:
            kind = m.group(1).lower()
            title = translate_admon_title((m.group(2) or "").strip())
            label = ADMON_LABELS.get(kind, kind)
            if title and title.casefold() in {v.casefold() for v in ADMON_TITLE_FA.values()}:
                return f"> **{title}**"
            return f"> **{label}**" + (f": {title}" if title else "")

        # Named + class-style leftovers: :::{tip}, :::{.warning}, ::: {.note} Title
        chunk = re.sub(
            r"(?m)^:{3,6}\s*\{\s*\.?([A-Za-z0-9_-]+)(?:\s+#[A-Za-z][\w:.-]*)*\s*\}(.*)$",
            leftover_dir,
            chunk,
        )
        return chunk

    md = map_outside_fences(md, clean_prose_myst)

    # 4) Man-page synopsis → fenced text (before brace escape so `{` stay
    #    literal inside the fence; avoids broken multi-line MD paragraphs)
    from tools.publish.fix_md_escapes import fix_man_synopsis_blocks

    md = fix_man_synopsis_blocks(md)

    # 5) Svelte-safe braces in prose only (fences handled by highlighter)
    md = escape_braces_outside_code(md)
    # 6) Final pass: fences / broken inline code / stray < that mdsvex→Svelte reject
    md = sanitize_for_mdsvex(md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def sanitize_for_mdsvex(md: str) -> str:
    """Repair common translation/publish damage that breaks mdsvex → Svelte.

    - Normalize broken fences: `````nix` `` → ```` ```nix ````, ``````` → ```` ``` ````
    - Dedent fenced openers (leading space → fence not recognized → bare `{` in HTML)
    - Close odd inline backticks on a line (truncated AI output)
    - Escape ``<|`` / ``|>`` pipe ops and unclosed ``<path…`` fragments
    - Drop pure translator-meta lines (EN:/FA:/Line N:)
    """
    lines = md.splitlines()
    out: list[str] = []
    in_fence = False
    fence_bq = ""  # blockquote prefix active for current fence
    # optional blockquote prefix captured separately so fences stay valid
    bq_re = re.compile(r"^([ \t]*(?:>[ \t]*)*)")

    meta_line = re.compile(
        r"^(?:Line\s+\d+\s*:|Persian\s*:|English\s*:|\*\s+\*\*List\s+\d+|Check heading|"
        r"Table rows?\s+check|keep Latin terms|Glossary/Term)",
        re.I,
    )

    def split_bq(s: str) -> tuple[str, str]:
        m = bq_re.match(s)
        pref = m.group(1) if m else ""
        return pref, s[len(pref) :]

    for raw_line in lines:
        pref, rest = split_bq(raw_line)
        # Normalize broken fence markers on the content part
        # ```nix`  / ```shell`  (stray trailing backtick after lang)
        rest2 = re.sub(r"^(```[A-Za-z0-9_+-]*)`+\s*$", r"\1", rest)
        # ```` or more alone → ```
        if re.match(r"^`{3,}\s*$", rest2):
            rest2 = "```"
        # leading spaces before fence (1–3) — CommonMark ok, mdsvex flaky
        if re.match(r"^ {1,3}```", rest2):
            rest2 = rest2.lstrip(" ")

        is_fence_line = rest2.startswith("```")
        if is_fence_line:
            is_close = re.match(r"^```\s*$", rest2) is not None
            use_pref = pref or fence_bq
            if in_fence:
                # any ``` while open closes (including mistaken ```lang)
                out.append(f"{use_pref}```")
                in_fence = False
                fence_bq = ""
                if not is_close and rest2 != "```":
                    # was actually a new open — start it
                    lang = rest2[3:].strip().strip("`")
                    fence_bq = pref
                    out.append(f"{pref}```{lang}" if lang else f"{pref}```")
                    in_fence = True
                continue
            # opening
            lang = rest2[3:].strip().strip("`")
            fence_bq = pref
            out.append(f"{pref}```{lang}" if lang else f"{pref}```")
            in_fence = True
            continue

        if in_fence:
            # Keep blockquote fence continuous even on blank lines
            if rest.strip() == "" and fence_bq:
                out.append(fence_bq.rstrip() or ">")
            else:
                use_pref = pref if pref else fence_bq
                body = rest if pref else rest2 if rest2 != rest else rest
                out.append(f"{use_pref}{body}" if use_pref else raw_line)
            continue

        line = f"{pref}{rest2}" if rest2 != rest else raw_line

        # Drop translator scaffolding left in FA docs
        if meta_line.match(line.strip()):
            continue
        if re.match(r"^\*\s+\*\*(?:EN|FA):\*\*", line.strip()):
            continue

        # Close odd number of unescaped backticks on the line (truncated inline code)
        if line.count("`") % 2 == 1:
            line = line + "`"

        # Nix pipe operators must not look like HTML tags
        line = line.replace("<|", "&lt;|").replace("|>", "|&gt;")

        # Incomplete angle-bracket paths: <nixpkgs/foo  (no closing >)
        def fix_lt(m: re.Match) -> str:
            body = m.group(1)
            if ">" in body:
                return m.group(0)
            return "&lt;" + body

        line = re.sub(
            r"<(?![/!?]|\s)([A-Za-z0-9_./:#@+${}'\"-]{1,200})(?![^<\n]*>)",
            fix_lt,
            line,
        )

        out.append(line)

    if in_fence:
        out.append("```")

    text = "\n".join(out)
    # Ensure a blank line before a *fence open* when glued to a heading/prose line.
    # Do not insert blanks before fence *closes* (``` alone) — that breaks blockquotes.
    text = re.sub(
        r"(?m)([^\n`])\n((?:[ \t]*>[ \t]*)?```[A-Za-z0-9_+-][^\n]*)",
        r"\1\n\n\2",
        text,
    )
    # One more brace pass for anything sanitize re-introduced into prose
    text = escape_braces_outside_code(text)
    return text


# nix.dev/manual/nix/{ver}/… → local FA manual when we have the page
_NIX_MANUAL_URL_RE = re.compile(
    r"https?://nix\.dev/manual/nix/"
    r"(?:stable|latest|rolling|prev-stable|development|\d+\.\d+)/"
    r"([^\s)\]>\"']*)",
    re.IGNORECASE,
)
# URL path segment → local docs/fa/nix-manual path (no .md)
_NIX_MANUAL_ALIASES: dict[str, str] = {
    "command-ref/conf-file": "command-ref/conf-file-prefix",
    "language/builtins": "language/builtins-prefix",
    "language/builtin-constants": "language/builtins-prefix",
    "language/index": "language",
    "command-ref/new-cli/nix": "command-ref/experimental-commands",
    "tutorials/nix-language": "language",
}


def load_local_nix_manual_paths() -> set[str]:
    """Paths relative to docs/fa/nix-manual (no .md), '' = home."""
    root = ROOT / "docs/fa/nix-manual"
    keys: set[str] = {""}
    if not root.is_dir():
        return keys
    for p in root.rglob("*.md"):
        if p.name == "SUMMARY.md":
            continue
        rel = p.relative_to(root)
        if rel.name == "index.md":
            key = "" if rel.parent == Path(".") else str(rel.parent).replace("\\", "/")
        else:
            key = str(rel.with_suffix("")).replace("\\", "/")
        keys.add(key)
    return keys


_LOCAL_MANUAL_PATHS: set[str] | None = None


def local_nix_manual_paths() -> set[str]:
    global _LOCAL_MANUAL_PATHS
    if _LOCAL_MANUAL_PATHS is None:
        _LOCAL_MANUAL_PATHS = load_local_nix_manual_paths()
    return _LOCAL_MANUAL_PATHS


def resolve_nix_manual_route(path_after_version: str) -> str | None:
    """Map manual path (maybe with .html / query / #frag) to /pages/nix-manual/… or None.

    Returns full local path including #fragment when the page exists locally.
    """
    raw = (path_after_version or "").strip()
    frag = ""
    if "#" in raw:
        raw, frag = raw.split("#", 1)
        frag = "#" + frag
    # drop ?query=
    raw = raw.split("?", 1)[0]
    raw = raw.strip("/")
    if raw.endswith(".html"):
        raw = raw[: -len(".html")]
    # single-page print dumps: nix-2.34.html
    if re.fullmatch(r"nix-[\d.]+", raw or ""):
        raw = ""
    if raw.endswith("/index"):
        raw = raw[: -len("/index")]
    raw = raw.strip("/")

    local = local_nix_manual_paths()
    candidate = _NIX_MANUAL_ALIASES.get(raw, raw)

    if candidate in local:
        route = "/pages/nix-manual" + (f"/{candidate}" if candidate else "")
        return route + frag

    # Soft parent fallback only for generated store-type leaves we didn't ship
    # e.g. store/types/s3-binary-cache-store → store/types
    if candidate.startswith("store/types/") and "store/types" in local:
        return f"/pages/nix-manual/store/types{frag}"

    # new-cli docs weren't downloaded; nearest local page
    if candidate.startswith("command-ref/new-cli"):
        if "command-ref/experimental-commands" in local:
            return f"/pages/nix-manual/command-ref/experimental-commands{frag}"
        return None

    # release-notes not shipped — leave external
    if candidate.startswith("release-notes"):
        return None

    return None


def rewrite_nix_manual_urls(md: str) -> str:
    """Point nix.dev reference-manual URLs at local /pages/nix-manual when available.

    Version roots (…/stable/, …/prev-stable/, …/latest/, single-page dumps)
    map to the FA manual home — we host one translation, not every channel.
    """

    def repl_path(m: re.Match) -> str:
        tail = (m.group(1) or "").strip().strip("/")
        # Bare …/stable/ or …/latest/ or nix-2.34.html → local manual home
        if not tail or re.fullmatch(r"nix-[\d.]+(?:\.html)?", tail):
            if "" in local_nix_manual_paths():
                return "/pages/nix-manual"
            return m.group(0)
        route = resolve_nix_manual_route(tail)
        return route if route is not None else m.group(0)

    md = _NIX_MANUAL_URL_RE.sub(repl_path, md)
    return md


def fa_rel_to_route(rel: Path, *, site_prefix: str = "/pages/nix-dev") -> str:
    """tutorials/foo/index.md → /pages/nix-dev/tutorials/foo
    tutorials/foo.md → /pages/nix-dev/tutorials/foo

    For the Nix reference manual tree under docs/fa/nix-manual/, use
    site_prefix="/pages/nix-manual" and pass *rel relative to that folder*
    so introduction.md → /pages/nix-manual/introduction.
    """
    parts = list(rel.parts)
    if parts[-1] in {"index.md", "index.fa.md"}:
        parts = parts[:-1]
    else:
        parts[-1] = Path(parts[-1]).stem
        if parts[-1].endswith(".fa"):
            parts[-1] = parts[-1][:-3]
    path = "/".join(parts)
    return site_prefix.rstrip("/") + (f"/{path}" if path else "")


def _md_path_to_site_route(
    rel: str,
    *,
    base_file: Path,
    content_root: Path,
    site_prefix: str,
) -> str:
    """Resolve a relative .md/.html path (optionally from former @docroot@) → site route."""
    rel = rel.strip().strip("<>").strip()
    if rel.endswith(".html"):
        rel = rel[:-5] + ".md"
    # normalize accidental leading ./ 
    while rel.startswith("./"):
        rel = rel[2:]
    try:
        root = content_root.resolve()
        # Book-root path: development/foo.md after @docroot@ strip, or any path
        # that exists under the content root as written (not starting with ..).
        cand = (content_root / rel).resolve()
        if not rel.startswith(".") and cand.is_file() and str(cand).startswith(str(root)):
            target = cand.relative_to(root)
        elif not rel.startswith(".") and (content_root / rel).is_file():
            target = Path(rel)
        else:
            target = (base_file.parent / rel).resolve().relative_to(root)
    except ValueError:
        target = Path(rel)
    parts = list(target.parts)
    if parts and parts[-1].endswith(".md"):
        stem = Path(parts[-1]).stem
        if stem == "index":
            parts = parts[:-1]
        else:
            parts[-1] = stem
    return site_prefix.rstrip("/") + ("/" + "/".join(parts) if parts else "")


def rewrite_md_links_to_routes(
    md: str, *, base_file: Path, content_root: Path, site_prefix: str
) -> str:
    """Convert relative Markdown links to site routes under site_prefix.

    Handles:
      - inline: [text](path.md#frag)
      - reference defs: [label]: path.md#frag   (mdBook often uses @docroot@/…)
      - @docroot@ book-root paths

    Absolute http(s) links and in-page #anchors are left alone.
    Also cleans mdBook directives ({{#include …}}).
    """
    # Drop mdBook preprocessor includes (often empty for our tree)
    md = re.sub(r"\{\{#include\s+[^}]+\}\}", "", md)
    md = re.sub(r"\{\{#.*?}\}", "", md)
    # @docroot@ is mdBook's book root — strip so relative paths resolve
    # (must happen before link rewrite so paths are normal)
    md = md.replace("@docroot@/", "").replace("@docroot@", "")
    # translation sometimes mangles @docroot@ → @_at_docroot@
    md = md.replace("@_at_docroot@/", "").replace("@_at_docroot@", "")

    # Relative .md links (and .html mirrors of the same pages)
    link_re = re.compile(
        r"\[([^\]]*)\]\((?!https?://|mailto:|/)([^)#?]+?\.(?:md|html))(#[^)]*)?\)"
    )

    def sub_inline(m: re.Match) -> str:
        text, rel, frag = m.group(1), m.group(2), m.group(3) or ""
        route = _md_path_to_site_route(
            rel, base_file=base_file, content_root=content_root, site_prefix=site_prefix
        )
        return f"[{text}]({route}{frag})"

    md = link_re.sub(sub_inline, md)

    # Reference-style definitions: [label]: path.md#frag
    # These were left as bare paths → browser resolved them under the *current*
    # page folder (e.g. store/file-system-object/development/… 404).
    ref_def_re = re.compile(
        r"^(\[[^\]]+\]:\s*)"
        r"(?!https?://|mailto:|/)"
        r"<?([^#\s>]+?\.(?:md|html))>?"
        r"(#[^\s]*)?"
        r"\s*$",
        re.MULTILINE,
    )

    def sub_ref(m: re.Match) -> str:
        prefix, rel, frag = m.group(1), m.group(2), m.group(3) or ""
        route = _md_path_to_site_route(
            rel, base_file=base_file, content_root=content_root, site_prefix=site_prefix
        )
        return f"{prefix}{route}{frag}"

    return ref_def_re.sub(sub_ref, md)


def write_site_page(route_path: str, content: str) -> Path:
    """Write /pages/foo/bar → src/routes/pages/foo/bar/+page.md"""
    rel = route_path.strip("/").removeprefix("pages/")
    dest = ROOT / "src/routes/pages" / Path(rel) / "+page.md"
    # if route is just /pages/foo → pages/foo/+page.md
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    return dest


def extract_title(md: str, fallback: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            # MyST / mdBook heading anchors: Title {#id}
            title = re.sub(r"\s*\{#[^}]+\}", "", title)
            # Strip anchors injected for MyST labels: <a id="…"></a>
            title = re.sub(r"<a\s+id=\"[^\"]*\"\s*></a>\s*", "", title, flags=re.I)
            title = re.sub(r"<[^>]+>", "", title)
            # Light markdown cleanup for nav labels
            title = title.replace("`", "").strip()
            return title or fallback
    return fallback


def build_ref_map(fa_files: list[tuple[Path, Path]]) -> dict[str, str]:
    """Map MyST labels and path stems to site routes.

    Also stores full relative paths (without .md) so toctree resolution can
    disambiguate same-named files in different folders.
    """
    ref: dict[str, str] = {}
    for rel, path in fa_files:
        route = fa_rel_to_route(rel)
        # full path keys (preferred)
        if rel.name in {"index.md", "index.fa.md"}:
            full = str(rel.parent).replace("\\", "/") if rel.parent != Path(".") else ""
        else:
            full = str(rel.with_suffix("")).replace("\\", "/")
            if full.endswith(".fa"):
                full = full[:-3]
        if full:
            ref[full] = route
            ref[full.replace("/", "-")] = route
        # path-based short key (last writer wins — fine for unique stems)
        stem = rel.stem
        if stem in {"index", "index.fa"}:
            key = rel.parent.name if rel.parent != Path(".") else "home"
        else:
            key = stem.replace(".fa", "")
        ref[key] = route
        ref[key.replace("-", "_")] = route
        # file content labels (label)=
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for m in re.finditer(r"^\(([a-zA-Z0-9_-]+)\)=\s*$", text, re.M):
            ref[m.group(1)] = route

    # Fallback: MyST labels often get stripped by translation. Re-harvest from
    # English sources so (label)= refs still resolve to the correct FA route.
    en_root = ROOT / "docs" / "en"
    if en_root.is_dir():
        for en_path in en_root.rglob("*.md"):
            try:
                en_text = en_path.read_text(encoding="utf-8")
            except Exception:
                continue
            rel = en_path.relative_to(en_root)
            # same route as FA counterpart would use
            if en_path.name in {"index.md"}:
                full = str(rel.parent).replace("\\", "/") if rel.parent != Path(".") else ""
            else:
                full = str(rel.with_suffix("")).replace("\\", "/")
            route = None
            if full and full in ref:
                route = ref[full]
            else:
                # reconstruct /pages/nix-dev/... from en relative path
                parts = list(rel.with_suffix("").parts)
                if parts and parts[-1] == "index":
                    parts = parts[:-1]
                route = "/pages/nix-dev" + (("/" + "/".join(parts)) if parts else "")
            for m in re.finditer(r"^\(([a-zA-Z0-9_-]+)\)=\s*$", en_text, re.M):
                lab = m.group(1)
                # don't overwrite an existing FA-sourced label
                ref.setdefault(lab, route)

    # known extras
    ref.setdefault("install-nix", "/pages/nix-dev/install-nix")
    ref.setdefault("first-steps", "/pages/nix-dev/tutorials/first-steps")
    ref.setdefault("module-system-tutorial", "/pages/nix-dev/tutorials/module-system")
    return ref


def write_page(route_path: str, content: str, out_root: Path) -> Path:
    # /pages/nix-dev/foo/bar → src/routes/pages/nix-dev/foo/bar/+page.md
    rel = route_path.strip("/").removeprefix("pages/")
    if not rel or rel == "nix-dev":
        dest = out_root / "+page.md"
    else:
        parts = rel.split("/")
        sub = "/".join(parts[1:]) if parts and parts[0] == "nix-dev" else "/".join(parts)
        if not sub:
            dest = out_root / "+page.md"
        else:
            dest = out_root.joinpath(*sub.split("/")) / "+page.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    return dest


def summary_md_order(summary_path: Path) -> list[str]:
    """Return relative .md paths in SUMMARY.md reading order."""
    return [e["rel"] for e in parse_summary_toc(summary_path)]


def parse_summary_toc(summary_path: Path) -> list[dict]:
    """Parse mdBook SUMMARY.md into ordered entries with hierarchical numbers.

    Example: command-ref/nix-collect-garbage.md → number \"8.4.2\",
    title \"nix-collect-garbage\" (from link text).
    """
    if not summary_path.is_file():
        return []

    # Stack of counters per depth (0 = chapter)
    counters: list[int] = []
    # indent width for one nesting step (detected from first indented item)
    step = 2
    entries: list[dict] = []
    seen: set[str] = set()

    # Match: optional indent, list marker, [title](path.md)
    line_re = re.compile(
        r"^(?P<indent>[ \t]*)[-*+]\s+"
        r"\[(?P<title>[^\]]*)\]\((?P<link>[^)]+)\)"
    )

    for raw in summary_path.read_text(encoding="utf-8").splitlines():
        m = line_re.match(raw)
        if not m:
            continue
        indent = m.group("indent").replace("\t", "    ")
        title = (m.group("title") or "").strip()
        link = m.group("link").strip()
        # only local markdown
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        path_part = link.split("#", 1)[0].strip().strip("<>").lstrip("./")
        if not path_part.endswith(".md"):
            continue
        if path_part in seen:
            continue
        seen.add(path_part)

        spaces = len(indent)
        if spaces > 0 and step == 2 and spaces % 2 == 0:
            # keep default 2 unless we see 4-space only patterns later
            pass
        depth = spaces // step if step else 0
        # grow/shrink counters
        if depth < len(counters):
            counters = counters[: depth + 1]
        while len(counters) < depth:
            counters.append(0)
        if len(counters) == depth:
            counters.append(1)
        else:
            counters[depth] += 1
            # reset deeper (already sliced)
        number = ".".join(str(n) for n in counters[: depth + 1])
        # strip backticks from SUMMARY titles like `post-build-hook`
        clean_title = title.replace("`", "").strip() or Path(path_part).stem
        entries.append(
            {
                "rel": path_part,
                "title": clean_title,
                "number": number,
                "depth": depth,
            }
        )
    return entries


GENERIC_H1 = {
    "name",
    "نام",
    "synopsis",
    "خلاصه",
    "description",
    "توضیحات",
    "index",
    "فهرست",
}

# Man-page section titles (EN + FA) — demoted under the numbered H1
MAN_SECTION_H1 = GENERIC_H1 | {
    "options",
    "گزینه‌ها",
    "examples",
    "مثال‌ها",
    "مثالها",
    "see also",
    "همچنین ببینید",
    "environment variables",
    "متغیرهای محیطی",
    "flags",
    "پرچم‌ها",
    "usage",
    "کاربرد",
    "arguments",
    "آرگومان‌ها",
}


def apply_numbered_page_header(
    md: str, *, number: str, nav_title: str, generic_only: bool = False
) -> str:
    """Put a custom H1 like ``# 8.4.2. nix-collect-garbage`` on the page.

    Mirrors mdBook numbered headings. Man-page stubs (Name / نام) stay as
    the next ``##`` section so the description line still reads naturally.
    """
    header = f"# {number}. {nav_title}".strip()
    m = re.search(r"(?m)^(#{1,6})\s+(.+?)\s*$", md)
    if not m:
        return header + "\n\n" + md.lstrip()
    level, text = m.group(1), m.group(2).strip()
    plain = re.sub(r"<[^>]+>", "", text).replace("`", "").strip()
    # Already has this number
    if plain.startswith(f"{number}.") or plain == f"{number}. {nav_title}":
        return md
    is_generic = plain.casefold() in GENERIC_H1 or plain in GENERIC_H1
    if generic_only and not is_generic and level == "#":
        return md
    start, end = m.span()
    rest = md[end:]
    if level == "#":
        block = header + "\n\n"
        if is_generic:
            # Keep man-page "Name" / "نام" subsection
            block += f"## {plain}\n\n"
        body = rest.lstrip("\n")
        if is_generic:
            # Man pages: single top-level H1 (numbered name); demote rest of H1 → H2
            body = re.sub(r"(?m)^#\s+(.+?)\s*$", r"## \1", body)
        else:
            # Demote known man-like section titles only
            def demote_man_h1(line_match: re.Match) -> str:
                t = re.sub(r"<[^>]+>", "", line_match.group(1)).replace("`", "").strip()
                if t.casefold() in MAN_SECTION_H1 or t in MAN_SECTION_H1:
                    return f"## {line_match.group(1)}"
                return line_match.group(0)

            body = re.sub(r"(?m)^#\s+(.+?)\s*$", demote_man_h1, body)
        return md[:start] + block + body
    # First heading is not h1 — prepend numbered title
    return header + "\n\n" + md


def manual_section_for(rel: Path) -> str:
    """Top-level section key for side nav (first path segment)."""
    parts = list(rel.parts)
    if not parts:
        return "root"
    if parts[0] in {"SUMMARY.md", "introduction.md", "quick-start.md", "c-api.md", "glossary.md"}:
        return "root"
    if parts[0].endswith(".md") and len(parts) == 1:
        return "root"
    return parts[0]


def publish_nix_manual_tree(fa_root: Path) -> int:
    """Publish docs/fa/nix-manual/** → /pages/nix-manual/** with local link rewrite."""
    manual_fa = fa_root / "nix-manual"
    if not manual_fa.is_dir():
        print("No docs/fa/nix-manual — skip Nix reference manual publish", file=sys.stderr)
        return 0

    files = sorted(
        p
        for p in manual_fa.rglob("*.md")
        if p.name != "manifest.json" and "manifest" not in p.parts
    )
    if not files:
        return 0

    web_base = "https://nix.dev/manual/nix/stable"
    try:
        man = (manual_fa.parent.parent / "en" / "nix-manual" / "manifest.json")
        if man.is_file():
            web_base = (
                json.loads(man.read_text(encoding="utf-8")).get("web") or web_base
            ).rstrip("/")
    except (OSError, json.JSONDecodeError):
        pass

    # Build ref map for this tree
    ref: dict[str, str] = {}
    for path in files:
        rel = path.relative_to(manual_fa)
        route = fa_rel_to_route(rel, site_prefix="/pages/nix-manual")
        key = rel.stem if rel.stem != "index" else (rel.parent.name or "home")
        ref[key] = route
        ref[str(rel.with_suffix("")).replace("\\", "/")] = route

    toc = parse_summary_toc(manual_fa / "SUMMARY.md")
    toc_by_rel = {e["rel"]: e for e in toc}

    published = 0
    by_rel: dict[str, dict] = {}
    for path in files:
        rel = path.relative_to(manual_fa)
        rel_s = str(rel).replace("\\", "/")
        # Skip SUMMARY as a content page (used only for TOC / ordering)
        if rel_s in {"SUMMARY.md"}:
            continue
        route = fa_rel_to_route(rel, site_prefix="/pages/nix-manual")
        raw = path.read_text(encoding="utf-8")
        raw = rewrite_md_links_to_routes(
            raw,
            base_file=path,
            content_root=manual_fa,
            site_prefix="/pages/nix-manual",
        )
        clean = strip_myst(
            raw,
            ref,
            base_dir=path.parent,
            site_prefix="/pages/nix-manual",
            content_root=manual_fa,
        )

        toc_e = toc_by_rel.get(rel_s)
        number = (toc_e or {}).get("number") or ""
        # Prefer SUMMARY link text (e.g. "nix-collect-garbage") over man-page "Name"
        nav_title = (toc_e or {}).get("title") or extract_title(clean, rel.stem)
        if number and nav_title:
            clean = apply_numbered_page_header(
                clean, number=number, nav_title=nav_title, generic_only=False
            )
            # Sidebar / chrome: always match mdBook style "8.4.2. nix-collect-garbage"
            page_title = f"{number}. {nav_title}"
        else:
            page_title = extract_title(clean, nav_title or rel.stem)

        dest = write_site_page(route, clean)
        # Source URL on nix.dev (mdBook): index.md → directory/, else .html
        if rel.name == "index.md":
            src_path = str(rel.parent).replace("\\", "/") if rel.parent != Path(".") else ""
            source = f"{web_base}/{src_path}/" if src_path else f"{web_base}/"
        else:
            src_path = str(rel.with_suffix("")).replace("\\", "/")
            source = f"{web_base}/{src_path}.html"
        by_rel[rel_s] = {
            "route": route,
            "title": page_title,
            "navTitle": nav_title,
            "number": number,
            "rel": rel_s,
            "section": manual_section_for(rel),
            "source": source,
        }
        published += 1
        print(f"  [manual] {rel} → {route} ({dest.relative_to(ROOT)})", file=sys.stderr)

    # Order nav following SUMMARY.md; append any leftovers alphabetically
    order = [e["rel"] for e in toc]
    nav: list[dict] = []
    seen: set[str] = set()
    for rel_s in order:
        item = by_rel.get(rel_s)
        if item:
            nav.append(item)
            seen.add(rel_s)
    for rel_s in sorted(by_rel.keys()):
        if rel_s not in seen:
            nav.append(by_rel[rel_s])

    # Always rebuild index from SUMMARY (mdBook TOC) so links stay current
    index_route = "/pages/nix-manual"
    summary = manual_fa / "SUMMARY.md"
    if summary.is_file():
        body = rewrite_md_links_to_routes(
            summary.read_text(encoding="utf-8"),
            base_file=summary,
            content_root=manual_fa,
            site_prefix="/pages/nix-manual",
        )
        body = strip_myst(body, ref, base_dir=manual_fa)
        body = re.sub(
            r"\{['\"]\{['\"]\}#include[^}\n]*\}['\"]\}['\"]\}",
            "",
            body,
        )
        body = re.sub(r"(?m)^\s*\{\s*\{.*#include.*\}\s*\}\s*$", "", body)
        body = re.sub(r"\n{3,}", "\n\n", body)
    else:
        lines = ["# راهنمای مرجع Nix", ""]
        for item in nav:
            lines.append(f"- [{item['title']}]({item['route']})")
        body = "\n".join(lines) + "\n"
    write_site_page(index_route, body)
    print(f"  [manual] index → {index_route}", file=sys.stderr)

    # Index entry for home (not a md file in by_rel as SUMMARY)
    home = {
        "route": index_route,
        "title": "فهرست مطالب",
        "rel": "SUMMARY.md",
        "section": "root",
        "source": f"{web_base}/",
    }
    # Put home first if not already
    nav = [home] + [p for p in nav if p["route"] != index_route]

    nav_path = ROOT / "src/lib/nix-manual-nav.json"
    nav_path.write_text(
        json.dumps(
            {
                "pages": nav,
                "count": len(nav),
                "webBase": web_base,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"Published {published} Nix manual pages; nav → {nav_path.relative_to(ROOT)}",
        file=sys.stderr,
    )
    return published


def nixpkgs_manual_section_for(rel: Path) -> str:
    parts = rel.parts
    if not parts:
        return "root"
    if parts[0] in {"SUMMARY.md", "index.md", "manual.md", "preface.md", "first-package.md"}:
        return "root"
    if parts[0].endswith(".md") and len(parts) == 1:
        return "root"
    return parts[0]


def publish_nixpkgs_manual_tree(fa_root: Path) -> int:
    """Publish docs/fa/nixpkgs-manual/** → /pages/nixpkgs-manual/**."""
    manual_fa = fa_root / "nixpkgs-manual"
    if not manual_fa.is_dir():
        # Fall back to EN if FA not translated yet (so UI can still host EN)
        en = ROOT / "docs/en/nixpkgs-manual"
        if en.is_dir():
            print(
                "No docs/fa/nixpkgs-manual — publishing EN tree as interim content",
                file=sys.stderr,
            )
            manual_fa = en
        else:
            print(
                "No docs/fa/nixpkgs-manual — skip Nixpkgs manual publish",
                file=sys.stderr,
            )
            return 0

    files = sorted(
        p
        for p in manual_fa.rglob("*.md")
        if p.name != "manifest.json" and "manifest" not in p.parts
    )
    if not files:
        return 0

    web_base = "https://nixos.org/manual/nixpkgs/stable"
    try:
        man = ROOT / "docs/en/nixpkgs-manual/manifest.json"
        if man.is_file():
            web_base = (
                json.loads(man.read_text(encoding="utf-8")).get("web") or web_base
            ).rstrip("/")
    except (OSError, json.JSONDecodeError):
        pass

    site_prefix = "/pages/nixpkgs-manual"
    ref: dict[str, str] = {}
    for path in files:
        rel = path.relative_to(manual_fa)
        route = fa_rel_to_route(rel, site_prefix=site_prefix)
        key = rel.stem if rel.stem != "index" else (rel.parent.name or "home")
        ref[key] = route
        ref[str(rel.with_suffix("")).replace("\\", "/")] = route

    toc = parse_summary_toc(manual_fa / "SUMMARY.md")
    toc_by_rel = {e["rel"]: e for e in toc}

    published = 0
    by_rel: dict[str, dict] = {}
    for path in files:
        rel = path.relative_to(manual_fa)
        rel_s = str(rel).replace("\\", "/")
        if rel_s in {"SUMMARY.md", "manual.md"}:
            continue
        route = fa_rel_to_route(rel, site_prefix=site_prefix)
        raw = path.read_text(encoding="utf-8")
        raw = rewrite_md_links_to_routes(
            raw,
            base_file=path,
            content_root=manual_fa,
            site_prefix=site_prefix,
        )
        # local FA Nix manual when referenced
        raw = rewrite_nix_manual_urls(raw)
        clean = strip_myst(
            raw,
            ref,
            base_dir=path.parent,
            site_prefix=site_prefix,
            content_root=manual_fa,
        )

        toc_e = toc_by_rel.get(rel_s)
        number = (toc_e or {}).get("number") or ""
        nav_title = (toc_e or {}).get("title") or extract_title(clean, rel.stem)
        if number and nav_title:
            clean = apply_numbered_page_header(
                clean, number=number, nav_title=nav_title, generic_only=False
            )
            page_title = f"{number}. {nav_title}"
        else:
            page_title = extract_title(clean, nav_title or rel.stem)

        dest = write_site_page(route, clean)
        if rel.name == "index.md":
            src_path = (
                str(rel.parent).replace("\\", "/") if rel.parent != Path(".") else ""
            )
            source = f"{web_base}/{src_path}/" if src_path else f"{web_base}/"
        else:
            src_path = str(rel.with_suffix("")).replace("\\", "/")
            source = f"{web_base}/{src_path}.html"
        by_rel[rel_s] = {
            "route": route,
            "title": page_title,
            "navTitle": nav_title,
            "number": number,
            "rel": rel_s,
            "section": nixpkgs_manual_section_for(rel),
            "source": source,
        }
        published += 1
        print(f"  [nixpkgs] {rel} → {route} ({dest.relative_to(ROOT)})", file=sys.stderr)

    order = [e["rel"] for e in toc]
    nav: list[dict] = []
    seen: set[str] = set()
    for rel_s in order:
        item = by_rel.get(rel_s)
        if item:
            nav.append(item)
            seen.add(rel_s)
    for rel_s in sorted(by_rel.keys()):
        if rel_s not in seen:
            nav.append(by_rel[rel_s])

    index_route = site_prefix
    summary = manual_fa / "SUMMARY.md"
    if summary.is_file():
        body = rewrite_md_links_to_routes(
            summary.read_text(encoding="utf-8"),
            base_file=summary,
            content_root=manual_fa,
            site_prefix=site_prefix,
        )
        body = strip_myst(body, ref, base_dir=manual_fa)
        body = re.sub(r"\n{3,}", "\n\n", body)
    else:
        lines = ["# راهنمای Nixpkgs", ""]
        for item in nav:
            lines.append(f"- [{item['title']}]({item['route']})")
        body = "\n".join(lines) + "\n"
    write_site_page(index_route, body)
    print(f"  [nixpkgs] index → {index_route}", file=sys.stderr)

    home = {
        "route": index_route,
        "title": "فهرست مطالب",
        "rel": "SUMMARY.md",
        "section": "root",
        "source": f"{web_base}/",
    }
    nav = [home] + [p for p in nav if p["route"] != index_route]

    nav_path = ROOT / "src/lib/nixpkgs-manual-nav.json"
    nav_path.write_text(
        json.dumps(
            {
                "pages": nav,
                "count": len(nav),
                "webBase": web_base,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"Published {published} Nixpkgs manual pages; nav → {nav_path.relative_to(ROOT)}",
        file=sys.stderr,
    )
    return published


def main() -> int:
    load_dotenv()
    fa_root = env_path("TRANSLATE_OUT_DIR", "docs/fa")
    # If TRANSLATE_OUT_DIR still points at first-steps only, prefer full tree
    if fa_root.name == "first-steps" and (ROOT / "docs/fa").is_dir():
        fa_root = ROOT / "docs/fa"
    out_root = ROOT / "src/routes/pages/nix-dev"
    out_root.mkdir(parents=True, exist_ok=True)

    if not fa_root.is_dir():
        print(f"Missing {fa_root} — run make translate-docs first", file=sys.stderr)
        return 1

    fa_files: list[tuple[Path, Path]] = []
    for p in sorted(fa_root.rglob("*.md")):
        if p.name == "manifest.json":
            continue
        rel = p.relative_to(fa_root)
        # Tour of Nix has its own publisher (/pages/tour-of-nix)
        if rel.parts and rel.parts[0] == "tour-of-nix":
            continue
        # Nix / Nixpkgs manuals published under their own /pages/* trees
        if rel.parts and rel.parts[0] in {"nix-manual", "nixpkgs-manual"}:
            continue
        fa_files.append((rel, p))

    if not fa_files:
        print("No FA markdown found for nix-dev tree", file=sys.stderr)
        # still try manuals
        publish_nix_manual_tree(fa_root)
        publish_nixpkgs_manual_tree(fa_root)
        return 1

    ref_map = build_ref_map(fa_files)
    # Prefer local FA Nix manual overview route, plus absolute external manuals
    ref_map.setdefault(
        "nix-manual",
        "/pages/nix-dev/reference/nix-manual",
    )
    nav: list[dict] = []
    published = 0

    for rel, path in fa_files:
        route = fa_rel_to_route(rel)
        raw = path.read_text(encoding="utf-8")
        clean = strip_myst(
            raw,
            ref_map,
            base_dir=path.parent,
            site_prefix="/pages/nix-dev",
            content_root=fa_root,
        )
        title = extract_title(clean, rel.stem)
        write_page(route, clean, out_root)
        nav.append(
            {
                "route": route,
                "title": title,
                "rel": str(rel).replace("\\", "/"),
                "section": rel.parts[0] if len(rel.parts) > 1 else "root",
            }
        )
        published += 1
        print(f"  {rel} → {route}", file=sys.stderr)

    # sort nav: root, tutorials, guides, concepts, reference, contributing, …
    section_order = [
        "root",
        "tutorials",
        "guides",
        "concepts",
        "reference",
        "contributing",
        "acknowledgements",
    ]

    def sort_key(item: dict):
        sec = item["section"]
        try:
            si = section_order.index(sec)
        except ValueError:
            si = 50
        return (si, item["route"])

    nav.sort(key=sort_key)
    nav_path = ROOT / "src/lib/nix-dev-nav.json"
    nav_path.write_text(
        json.dumps({"pages": nav, "count": len(nav)}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Published {published} nix.dev pages; nav → {nav_path.relative_to(ROOT)}", file=sys.stderr)

    manual_n = publish_nix_manual_tree(fa_root)
    nixpkgs_n = publish_nixpkgs_manual_tree(fa_root)
    print(
        f"Total published: nix-dev={published} nix-manual={manual_n} "
        f"nixpkgs-manual={nixpkgs_n}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
