#!/usr/bin/env python3
"""Publish FA Tour of Nix pages into SvelteKit routes.

docs/fa/tour-of-nix/**/*.md → src/routes/pages/tour-of-nix/**/+page.md
Also writes src/lib/tour-of-nix-nav.json for sidebar + prev/next.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from tools.lib.envutil import ROOT, env_path, load_dotenv
from tools.publish.site_docs import extract_title, strip_myst

ROUTE_PREFIX = "/pages/tour-of-nix"


def rel_to_route(rel: Path) -> str:
    parts = list(rel.parts)
    if parts[-1] in {"index.md", "index.fa.md"}:
        parts = parts[:-1]
    else:
        stem = Path(parts[-1]).stem
        if stem.endswith(".fa"):
            stem = stem[:-3]
        parts[-1] = stem
    path = "/".join(parts)
    return ROUTE_PREFIX + (f"/{path}" if path else "")


def write_page(route: str, content: str, out_root: Path) -> Path:
    # /pages/tour-of-nix → +page.md
    # /pages/tour-of-nix/foo/bar → foo/bar/+page.md
    rel = route.strip("/").removeprefix("pages/tour-of-nix").strip("/")
    if not rel:
        dest = out_root / "+page.md"
    else:
        dest = out_root.joinpath(*rel.split("/")) / "+page.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    return dest


def section_of(rel: Path) -> str:
    if len(rel.parts) <= 1:
        return "root"
    return rel.parts[0]


def main() -> int:
    load_dotenv()
    fa_root = env_path("TOUR_OF_NIX_FA", "docs/fa/tour-of-nix")
    out_root = ROOT / "src/routes/pages/tour-of-nix"
    out_root.mkdir(parents=True, exist_ok=True)

    if not fa_root.is_dir():
        print(f"Missing {fa_root} — translate tour first", file=sys.stderr)
        return 1

    fa_files: list[tuple[Path, Path]] = []
    for p in sorted(fa_root.rglob("*.md")):
        if p.name in {"questions.json", "manifest.json"}:
            continue
        fa_files.append((p.relative_to(fa_root), p))

    if not fa_files:
        print("No FA tour markdown found", file=sys.stderr)
        return 1

    # minimal ref map (internal relative links between lessons)
    ref: dict[str, str] = {}
    for rel, _ in fa_files:
        route = rel_to_route(rel)
        stem = rel.stem.replace(".fa", "")
        ref[stem] = route
        ref[str(rel).replace("\\", "/").removesuffix(".md")] = route

    nav: list[dict] = []
    for rel, path in fa_files:
        route = rel_to_route(rel)
        raw = path.read_text(encoding="utf-8")
        clean = strip_myst(raw, ref)
        # rewrite relative ./foo.md links to site routes
        def rel_link(m: re.Match) -> str:
            text, target = m.group(1), m.group(2)
            t = target.split("#")[0].removesuffix(".md").lstrip("./")
            if t in ref:
                href = ref[t]
                if "#" in target:
                    href += "#" + target.split("#", 1)[1]
                return f"[{text}]({href})"
            return m.group(0)

        clean = re.sub(r"\[([^\]]*)\]\(([^)]+\.md(?:#[^)]*)?)\)", rel_link, clean)
        title = extract_title(clean, rel.stem)
        write_page(route, clean, out_root)
        nav.append(
            {
                "route": route,
                "title": title,
                "rel": str(rel).replace("\\", "/"),
                "section": section_of(rel),
            }
        )
        print(f"  {rel} → {route}", file=sys.stderr)

    # index first, then by path
    def sort_key(item: dict):
        if item["route"] == ROUTE_PREFIX:
            return (0, "")
        return (1, item["route"])

    nav.sort(key=sort_key)
    nav_path = ROOT / "src/lib/tour-of-nix-nav.json"
    nav_path.write_text(
        json.dumps({"pages": nav, "count": len(nav)}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(f"Published {len(nav)} tour pages; nav → {nav_path.relative_to(ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
