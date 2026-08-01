#!/usr/bin/env python3
"""Download an HTML page and convert the main content to Markdown.

Only depends on requests + beautifulsoup4 (see pyproject.toml).
HTML→Markdown conversion is implemented here (inspired by python-markdownify
patterns under ./context/, but without installing that package).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from tools.lib.envutil import env_int, env_path, env_str, load_dotenv

load_dotenv()

BLOCK_TAGS = frozenset(
    {
        "p",
        "div",
        "section",
        "article",
        "main",
        "header",
        "footer",
        "aside",
        "blockquote",
        "pre",
        "ul",
        "ol",
        "li",
        "dl",
        "dt",
        "dd",
        "table",
        "thead",
        "tbody",
        "tfoot",
        "tr",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "hr",
        "figure",
        "figcaption",
    }
)


def fetch_html(url: str, timeout: float | None = None) -> str:
    user_agent = env_str(
        "DOWNLOAD_USER_AGENT",
        "nix-guide-dl/0.1 (+local educational use; requests+bs4)",
    )
    if timeout is None:
        timeout = float(env_int("DOWNLOAD_TIMEOUT_SEC", 30))
    resp = requests.get(
        url,
        headers={"User-Agent": user_agent, "Accept": "text/html"},
        timeout=timeout,
    )
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or resp.encoding or "utf-8"
    return resp.text


def pick_content_root(soup: BeautifulSoup) -> Tag:
    """Prefer article / main body; fall back to body."""
    for selector in ("article", "main article", "main", '[role="main"]'):
        node = soup.select_one(selector)
        if node and node.get_text(strip=True):
            return node
    body = soup.body
    if body is None:
        raise RuntimeError("No body element found in HTML")
    return body


def strip_noise(root: Tag) -> None:
    for tag in root.find_all(["script", "style", "noscript", "svg", "iframe", "nav"]):
        tag.decompose()
    # Drop common chrome / skip links inside content
    for a in list(root.find_all("a")):
        text = a.get_text(" ", strip=True).lower()
        if text in {"← back", "back", "skip to content", "skip to main content"}:
            a.decompose()


def collapse_ws(text: str) -> str:
    return re.sub(r"[ \t\f\v]+", " ", text)


def escape_md_inline(text: str) -> str:
    # Light escaping so emphasis markers in prose don't break rendering.
    return text.replace("\\", "\\\\").replace("*", "\\*").replace("_", "\\_")


def convert_inline(node: Tag | NavigableString, base_url: str) -> str:
    if isinstance(node, NavigableString):
        return escape_md_inline(collapse_ws(str(node)))

    assert isinstance(node, Tag)
    name = (node.name or "").lower()

    if name in ("script", "style", "noscript"):
        return ""

    if name == "br":
        return "  \n"

    # Preserve HTML anchors (nix.conf option ids, glossary, etc.)
    id_attr = node.get("id")
    anchor_prefix = f'<a id="{id_attr}"></a>' if id_attr else ""

    if name in ("code", "kbd", "samp"):
        # Nested code inside pre is handled at block level.
        if node.find_parent("pre"):
            return anchor_prefix + node.get_text()
        inner = node.get_text()
        if "`" in inner:
            ticks = "``"
            return f"{anchor_prefix}{ticks}{inner}{ticks}"
        return f"{anchor_prefix}`{inner}`"

    if name in ("strong", "b"):
        inner = "".join(convert_inline(c, base_url) for c in node.children).strip()
        body = f"**{inner}**" if inner else ""
        return anchor_prefix + body

    if name in ("em", "i"):
        inner = "".join(convert_inline(c, base_url) for c in node.children).strip()
        body = f"*{inner}*" if inner else ""
        return anchor_prefix + body

    if name == "a":
        href = node.get("href") or ""
        if href.startswith(("#", "javascript:")):
            return anchor_prefix + "".join(
                convert_inline(c, base_url) for c in node.children
            )
        abs_href = urljoin(base_url, href)
        label = "".join(convert_inline(c, base_url) for c in node.children).strip()
        if not label:
            label = abs_href
        title = node.get("title")
        if title:
            return f'{anchor_prefix}[{label}]({abs_href} "{title}")'
        return f"{anchor_prefix}[{label}]({abs_href})"

    if name == "img":
        src = node.get("src") or ""
        if not src:
            return ""
        abs_src = urljoin(base_url, src)
        alt = node.get("alt") or ""
        return f"![{alt}]({abs_src})"

    if name in BLOCK_TAGS:
        # Should not normally appear as pure inline; join children.
        return anchor_prefix + "".join(
            convert_inline(c, base_url) for c in node.children
        )

    return anchor_prefix + "".join(convert_inline(c, base_url) for c in node.children)


def code_block_text(pre: Tag) -> str:
    # Prefer full <pre> text: some pages put the payload in a sibling <span>
    # next to an empty <code> shell (e.g. nixos.org store-path examples).
    code = pre.find("code")
    if code is not None:
        code_text = code.get_text()
        pre_text = pre.get_text()
        text = pre_text if len(pre_text.strip()) > len(code_text.strip()) else code_text
    else:
        text = pre.get_text()
    # Normalize newlines; keep internal indentation.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.startswith("\n"):
        text = text[1:]
    if text.endswith("\n"):
        text = text[:-1]
    return text


def fence_for(code: str) -> str:
    longest = 0
    for m in re.finditer(r"`+", code):
        longest = max(longest, len(m.group(0)))
    return "`" * max(3, longest + 1)


def convert_list(list_tag: Tag, base_url: str, ordered: bool, depth: int = 0) -> str:
    lines: list[str] = []
    index = 1
    indent = "  " * depth
    for li in list_tag.find_all("li", recursive=False):
        # Separate nested lists from item text
        nested: list[Tag] = []
        for child in list(li.children):
            if isinstance(child, Tag) and child.name in ("ul", "ol"):
                nested.append(child)
                child.extract()

        # Prefer block conversion so <p><span id=…> option anchors survive
        parts: list[str] = []
        for c in li.children:
            if isinstance(c, Tag) and (c.name or "").lower() in BLOCK_TAGS:
                part = convert_block(c, base_url)
                if part:
                    parts.append(part)
            else:
                parts.append(convert_inline(c, base_url))
        body = collapse_ws(" ".join(parts)).strip()
        # collapse_ws may wipe newlines between blocks; keep anchors intact
        marker = f"{index}." if ordered else "-"
        lines.append(f"{indent}{marker} {body}".rstrip())
        for nest in nested:
            lines.append(
                convert_list(nest, base_url, ordered=nest.name == "ol", depth=depth + 1)
            )
        index += 1
    return "\n".join(lines)


def convert_table(table: Tag, base_url: str) -> str:
    rows: list[list[str]] = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["th", "td"])
        rows.append(
            [
                collapse_ws(
                    "".join(convert_inline(c, base_url) for c in cell.children)
                ).strip()
                for cell in cells
            ]
        )
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    for r in rows:
        while len(r) < width:
            r.append("")
    header = rows[0]
    body = rows[1:] if len(rows) > 1 else []
    out = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for r in body:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def convert_block(node: Tag | NavigableString, base_url: str) -> str:
    if isinstance(node, NavigableString):
        text = collapse_ws(str(node)).strip()
        return text

    assert isinstance(node, Tag)
    name = (node.name or "").lower()

    if name in ("script", "style", "noscript", "nav"):
        return ""

    if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        level = int(name[1])
        hid = node.get("id")
        text = collapse_ws(
            "".join(convert_inline(c, base_url) for c in node.children)
        ).strip()
        if not text:
            return ""
        prefix = f'<a id="{hid}"></a> ' if hid else ""
        return f"{'#' * level} {prefix}{text}"

    if name == "p":
        # Collect ids on the paragraph or immediate children (nix.conf options)
        ids: list[str] = []
        if node.get("id"):
            ids.append(str(node.get("id")))
        for child in node.children:
            if isinstance(child, Tag) and child.get("id"):
                ids.append(str(child.get("id")))
        anchors = "".join(f'<a id="{i}"></a>' for i in ids)
        text = collapse_ws(
            "".join(convert_inline(c, base_url) for c in node.children)
        ).strip()
        if anchors and text:
            return f"{anchors}{text}"
        return anchors or text

    if name == "pre":
        code = code_block_text(node)
        fence = fence_for(code)
        return f"{fence}\n{code}\n{fence}"

    if name == "blockquote":
        inner_parts = [
            convert_block(c, base_url)
            for c in node.children
            if not (isinstance(c, NavigableString) and not str(c).strip())
        ]
        inner = "\n\n".join(p for p in inner_parts if p)
        quoted = "\n".join(
            ("> " + line if line else ">") for line in inner.splitlines()
        )
        return quoted

    if name in ("ul", "ol"):
        return convert_list(node, base_url, ordered=name == "ol")

    if name == "table":
        return convert_table(node, base_url)

    if name == "hr":
        return "---"

    if name in ("li", "dt", "dd"):
        # Handled by list/dl parent; as fallback treat as paragraph.
        return collapse_ws(
            "".join(convert_inline(c, base_url) for c in node.children)
        ).strip()

    if name == "figure":
        parts = [convert_block(c, base_url) for c in node.children]
        return "\n\n".join(p for p in parts if p)

    if name == "figcaption":
        text = collapse_ws(
            "".join(convert_inline(c, base_url) for c in node.children)
        ).strip()
        return f"*{text}*" if text else ""

    if name in ("div", "section", "article", "main", "header", "footer", "aside", "span"):
        # Walk block children; treat pure-inline containers as a paragraph.
        blocks: list[str] = []
        inline_buf: list[str] = []

        def flush_inline() -> None:
            nonlocal inline_buf
            if not inline_buf:
                return
            text = collapse_ws("".join(inline_buf)).strip()
            inline_buf = []
            if text:
                blocks.append(text)

        for child in node.children:
            if isinstance(child, NavigableString):
                if str(child).strip():
                    inline_buf.append(escape_md_inline(collapse_ws(str(child))))
                continue
            if not isinstance(child, Tag):
                continue
            cname = (child.name or "").lower()
            if cname in BLOCK_TAGS and cname != "span":
                flush_inline()
                part = convert_block(child, base_url)
                if part:
                    blocks.append(part)
            else:
                inline_buf.append(convert_inline(child, base_url))
        flush_inline()
        return "\n\n".join(blocks)

    # Unknown tag: prefer block conversion for block children, else inline.
    parts: list[str] = []
    for c in node.children:
        if isinstance(c, Tag) and (c.name or "").lower() in BLOCK_TAGS:
            part = convert_block(c, base_url)
            if part:
                parts.append(part)
        else:
            parts.append(convert_inline(c, base_url))
    joined = "\n\n".join(p for p in parts if p and p.strip())
    return joined


def html_to_markdown(html: str, base_url: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else ""
    root = pick_content_root(soup)
    strip_noise(root)

    body_md = convert_block(root, base_url).strip()
    # Collapse excessive blank lines
    body_md = re.sub(r"\n{3,}", "\n\n", body_md)

    parts: list[str] = []
    if title:
        parts.append(f"# {title.split('|')[0].strip()}")
        parts.append("")
        parts.append(f"> Source: [{base_url}]({base_url})")
        parts.append("")
        # Avoid duplicate H1 if article already starts with same heading
        first_line = body_md.splitlines()[0] if body_md else ""
        if first_line.lstrip("# ").strip().lower() == title.split("|")[0].strip().lower():
            # Drop the page H1 from body; keep rest
            rest = "\n".join(body_md.splitlines()[1:]).lstrip()
            parts.append(rest)
        else:
            parts.append(body_md)
    else:
        parts.append(body_md)

    return "\n".join(parts).rstrip() + "\n"


def default_output_path(url: str) -> Path:
    path = urlparse(url).path.rstrip("/") or "index"
    name = path.split("/")[-1] or "page"
    return Path(f"{name}.md")


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    default_url = env_str(
        "DOWNLOAD_URL", "https://nixos.org/guides/how-nix-works/"
    )
    default_out = env_path("DOWNLOAD_OUTPUT", "how-nix-works.md")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "url",
        nargs="?",
        default=None,
        help="Page URL (default: DOWNLOAD_URL from .env)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output markdown path (default: DOWNLOAD_OUTPUT from .env)",
    )
    args = parser.parse_args(argv)

    url = args.url or default_url
    out = args.output or default_out
    print(f"Fetching {url} …", file=sys.stderr)
    html = fetch_html(url)
    md = html_to_markdown(html, url)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"Wrote {out} ({len(md)} bytes, {md.count(chr(10))+1} lines)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
