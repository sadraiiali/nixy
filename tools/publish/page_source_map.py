#!/usr/bin/env python3
"""Build a big route → upstream source map JSON for site pages.

Writes ``src/lib/page-source-map.json`` (override with ``--output`` / env
``PAGE_SOURCE_MAP_OUTPUT``).

Each entry maps a site route (e.g. ``/pages/nix-dev/install-nix``) to:

- ``github`` — blob URL in the upstream GitHub repo (when known)
- ``web`` — published docs URL (nix.dev / nixos.org / …)
- ``repo`` — ``owner/name``
- ``rel`` — path inside the upstream docs tree (or local legacy file)
- ``section`` — ``nix-dev`` | ``nix-manual`` | ``nixpkgs-manual`` | ``how-nix-works`` | …

Sources:

1. Existing nav JSONs under ``src/lib/*-nav.json`` (preferred order + titles)
2. Filesystem scan of ``src/routes/pages/{nix-dev,nix-manual,nixpkgs-manual,how-nix-works}``
   so pages missing from nav still appear

Run::

    uv run python -m tools.publish.page_source_map
    make page-source-map   # if wired in Makefile
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from tools.lib.envutil import ROOT, env_path, env_str, load_dotenv

# ---------------------------------------------------------------------------
# Upstream repo layout (defaults match tools/download/*)
# ---------------------------------------------------------------------------

SECTIONS: dict[str, dict[str, str]] = {
    "nix-dev": {
        "owner": "NixOS",
        "repo": "nix.dev",
        "ref": "master",
        # path of docs tree inside the repo
        "tree": "source",
        "web_base": "https://nix.dev",
        "nav": "src/lib/nix-dev-nav.json",
        "routes_root": "src/routes/pages/nix-dev",
        "site_prefix": "/pages/nix-dev",
    },
    "nix-manual": {
        "owner": "NixOS",
        "repo": "nix",
        "ref": "master",
        "tree": "doc/manual/source",
        "web_base": "https://nix.dev/manual/nix/stable",
        "nav": "src/lib/nix-manual-nav.json",
        "routes_root": "src/routes/pages/nix-manual",
        "site_prefix": "/pages/nix-manual",
    },
    "nixpkgs-manual": {
        "owner": "NixOS",
        "repo": "nixpkgs",
        "ref": "master",
        "tree": "doc",
        "web_base": "https://nixos.org/manual/nixpkgs/stable",
        "nav": "src/lib/nixpkgs-manual-nav.json",
        "routes_root": "src/routes/pages/nixpkgs-manual",
        "site_prefix": "/pages/nixpkgs-manual",
    },
    "how-nix-works": {
        "owner": "",
        "repo": "",
        "ref": "",
        "tree": "",
        "web_base": "https://nixos.org/guides/how-nix-works",
        "nav": "",
        "routes_root": "src/routes/pages/how-nix-works",
        "site_prefix": "/pages/how-nix-works",
    },
}


def norm_route(route: str) -> str:
    r = (route or "").strip()
    if not r:
        return "/"
    if not r.startswith("/"):
        r = "/" + r
    return r.rstrip("/") or "/"


def github_blob(owner: str, repo: str, ref: str, tree: str, rel: str) -> str | None:
    """Build raw GitHub blob URL for a markdown path inside the docs tree."""
    if not owner or not repo or not rel:
        return None
    rel = rel.replace("\\", "/").lstrip("/")
    # Nav uses SUMMARY.md for the manual index — still a real file in the tree
    if tree:
        path = f"{tree.rstrip('/')}/{rel}"
    else:
        path = rel
    return f"https://github.com/{owner}/{repo}/blob/{ref}/{path}"


def web_url(web_base: str, rel: str | None, *, section: str) -> str:
    """Published HTML URL for a docs page (mdBook / Sphinx-style)."""
    base = web_base.rstrip("/")
    if not rel:
        return base + ("/" if section != "how-nix-works" else "")

    rel = rel.replace("\\", "/").lstrip("/")

    if section == "how-nix-works":
        return base + "/"

    if rel in {"SUMMARY.md", "index.md"}:
        return base + "/"

    if rel.endswith("/index.md"):
        mid = rel[: -len("/index.md")]
        return f"{base}/{mid}/" if mid else base + "/"

    stem = rel[:-3] if rel.lower().endswith(".md") else rel
    return f"{base}/{stem}.html"


def route_from_rel(site_prefix: str, rel: str) -> str:
    """Mirror publish.site_docs fa_rel_to_route for index.md / SUMMARY."""
    rel = rel.replace("\\", "/").lstrip("/")
    if rel in {"SUMMARY.md", "index.md"}:
        return norm_route(site_prefix)
    if rel.endswith("/index.md"):
        mid = rel[: -len("/index.md")]
        return norm_route(f"{site_prefix}/{mid}" if mid else site_prefix)
    if rel.lower().endswith(".md"):
        mid = rel[:-3]
        return norm_route(f"{site_prefix}/{mid}")
    return norm_route(f"{site_prefix}/{rel}")


def rel_from_route(site_prefix: str, route: str) -> str:
    """Best-effort inverse: route → nav-style rel path ending in .md."""
    route = norm_route(route)
    prefix = norm_route(site_prefix)
    if route == prefix:
        # ambiguous (index vs SUMMARY); caller may override from nav
        return "index.md"
    if not route.startswith(prefix + "/"):
        return "index.md"
    rest = route[len(prefix) + 1 :]
    return f"{rest}.md"


def load_nav(nav_rel: str) -> list[dict[str, Any]]:
    if not nav_rel:
        return []
    path = ROOT / nav_rel
    if not path.is_file():
        print(f"  warn: missing nav {nav_rel}", file=sys.stderr)
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    pages = data.get("pages") or []
    if not isinstance(pages, list):
        return []
    return [p for p in pages if isinstance(p, dict)]


def scan_routes(routes_root: str, site_prefix: str) -> list[str]:
    """Return site routes for every +page.md under routes_root."""
    root = ROOT / routes_root
    if not root.is_dir():
        return []
    out: list[str] = []
    for page_md in sorted(root.rglob("+page.md")):
        rel_dir = page_md.parent.relative_to(root)
        if str(rel_dir) == ".":
            out.append(norm_route(site_prefix))
        else:
            out.append(norm_route(f"{site_prefix}/{rel_dir.as_posix()}"))
    return out


def entry_for(
    *,
    section: str,
    cfg: dict[str, str],
    route: str,
    rel: str | None,
    title: str | None = None,
    nav_source: str | None = None,
) -> dict[str, Any]:
    owner = cfg.get("owner") or ""
    repo = cfg.get("repo") or ""
    ref = cfg.get("ref") or "master"
    tree = cfg.get("tree") or ""
    web_base = cfg.get("web_base") or ""

    rel_s = (rel or "").replace("\\", "/") if rel else None
    if not rel_s:
        rel_s = rel_from_route(cfg["site_prefix"], route)
        if section == "nix-manual" and norm_route(route) == norm_route(
            cfg["site_prefix"]
        ):
            rel_s = "SUMMARY.md"

    gh = github_blob(owner, repo, ref, tree, rel_s) if owner and repo else None
    web = nav_source or web_url(web_base, rel_s, section=section)

    item: dict[str, Any] = {
        "route": norm_route(route),
        "section": section,
        "rel": rel_s,
        "web": web,
    }
    if title:
        item["title"] = title
    if gh:
        item["github"] = gh
        item["repo"] = f"{owner}/{repo}"
        item["ref"] = ref
        item["tree"] = tree
    elif web:
        # pages with only a public web source (e.g. how-nix-works)
        item["github"] = None
        item["repo"] = None
    return item


def build_section(section: str, cfg: dict[str, str]) -> dict[str, dict[str, Any]]:
    """Return route → entry for one section."""
    by_route: dict[str, dict[str, Any]] = {}

    # 1) Nav (authoritative title + rel + existing web source)
    for p in load_nav(cfg.get("nav") or ""):
        route = norm_route(str(p.get("route") or ""))
        if not route or not route.startswith(norm_route(cfg["site_prefix"])):
            continue
        rel = p.get("rel")
        rel_s = str(rel).replace("\\", "/") if rel else None
        title = p.get("title") or p.get("navTitle")
        nav_src = p.get("source")
        by_route[route] = entry_for(
            section=section,
            cfg=cfg,
            route=route,
            rel=rel_s,
            title=str(title) if title else None,
            nav_source=str(nav_src) if nav_src else None,
        )

    # 2) Filesystem: fill gaps
    for route in scan_routes(cfg["routes_root"], cfg["site_prefix"]):
        if route in by_route:
            continue
        by_route[route] = entry_for(
            section=section,
            cfg=cfg,
            route=route,
            rel=None,
        )

    return by_route


def build_map(
    sections: list[str] | None = None,
    *,
    overrides: dict[str, dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Build full map document."""
    wanted = sections or list(SECTIONS.keys())
    pages: dict[str, dict[str, Any]] = {}
    counts: dict[str, int] = {}

    for section in wanted:
        if section not in SECTIONS:
            print(f"  warn: unknown section {section!r}, skip", file=sys.stderr)
            continue
        cfg = dict(SECTIONS[section])
        if overrides and section in overrides:
            cfg.update({k: v for k, v in overrides[section].items() if v is not None})
        # env overrides for main two repos
        if section == "nix-dev":
            cfg["owner"] = env_str("NIX_DEV_OWNER", cfg["owner"])
            cfg["repo"] = env_str("NIX_DEV_REPO", cfg["repo"])
            cfg["ref"] = env_str("NIX_DEV_REF", cfg["ref"])
            cfg["tree"] = env_str("NIX_DEV_PATH", cfg["tree"])
        elif section == "nix-manual":
            cfg["owner"] = env_str("NIX_MANUAL_OWNER", cfg["owner"])
            cfg["repo"] = env_str("NIX_MANUAL_REPO", cfg["repo"])
            cfg["ref"] = env_str("NIX_MANUAL_REF", cfg["ref"])
            cfg["tree"] = env_str("NIX_MANUAL_PATH", cfg["tree"])
        elif section == "nixpkgs-manual":
            cfg["owner"] = env_str("NIXPKGS_MANUAL_OWNER", cfg["owner"])
            cfg["repo"] = env_str("NIXPKGS_MANUAL_REPO", cfg["repo"])
            cfg["ref"] = env_str("NIXPKGS_MANUAL_REF", cfg["ref"])
            cfg["tree"] = env_str("NIXPKGS_MANUAL_PATH", cfg["tree"])

        print(f"  section {section} …", file=sys.stderr)
        part = build_section(section, cfg)
        pages.update(part)
        counts[section] = len(part)
        print(f"    → {len(part)} pages", file=sys.stderr)

    # Stable key order: section order then route
    ordered_keys = sorted(
        pages.keys(),
        key=lambda r: (
            wanted.index(pages[r]["section"])
            if pages[r]["section"] in wanted
            else 99,
            r,
        ),
    )
    ordered = {k: pages[k] for k in ordered_keys}

    repos = {
        "nix-dev": "https://github.com/NixOS/nix.dev",
        "nix-manual": "https://github.com/NixOS/nix",
        "nixpkgs-manual": "https://github.com/NixOS/nixpkgs",
        "how-nix-works": "https://nixos.org/guides/how-nix-works/",
    }

    return {
        "version": 1,
        "description": (
            "Map of site routes to upstream GitHub blob + published web URLs. "
            "Generated by tools.publish.page_source_map."
        ),
        "repos": repos,
        "counts": counts,
        "count": len(ordered),
        "pages": ordered,
    }


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output JSON (default PAGE_SOURCE_MAP_OUTPUT or src/lib/page-source-map.json)",
    )
    parser.add_argument(
        "--sections",
        nargs="+",
        default=None,
        choices=sorted(SECTIONS.keys()),
        help="Only these sections (default: all)",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Minified JSON (no indent)",
    )
    args = parser.parse_args(argv)

    out = args.output or env_path(
        "PAGE_SOURCE_MAP_OUTPUT", "src/lib/page-source-map.json"
    )
    if not out.is_absolute():
        out = ROOT / out

    print("Building page source map …", file=sys.stderr)
    doc = build_map(args.sections)

    out.parent.mkdir(parents=True, exist_ok=True)
    if args.compact:
        text = json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n"
    else:
        text = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    out.write_text(text, encoding="utf-8")

    print(
        f"Wrote {doc['count']} pages → {out.relative_to(ROOT)} "
        f"({out.stat().st_size // 1024} KiB)",
        file=sys.stderr,
    )
    for sec, n in (doc.get("counts") or {}).items():
        print(f"  {sec}: {n}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
