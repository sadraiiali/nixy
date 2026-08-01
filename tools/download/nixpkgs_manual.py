#!/usr/bin/env python3
"""Download the *Nixpkgs* manual sources (NixOS/nixpkgs doc/).

Uses the GitHub Trees API + raw file fetches (nixpkgs zipball is enormous).
Default output: docs/en/nixpkgs-manual/

Normalizes:
  *.chapter.md → *.md
  *.section.md → *.md
Skips release-notes by default; set NIXPKGS_MANUAL_INCLUDE_RELEASE_NOTES=true to keep.

Also writes SUMMARY.md from doc/manual.md.in include order for publish nav.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests

from tools.lib.envutil import ROOT, env_bool, env_path, env_str, load_dotenv

SKIP_NAMES = {
    "readme.md",
    "styleguide.md",
    "manpage-urls.json",
    "redirects.json",
    "default.nix",
    "shell.nix",
    "style.css",
    "anchor-use.js",
    "anchor.min.js",
}


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": env_str(
                "DOWNLOAD_USER_AGENT", "nix-notes-dl/0.1 (educational)"
            ),
            "Accept": "application/vnd.github+json",
        }
    )
    token = env_str("GITHUB_TOKEN", "")
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    return s


def normalize_rel(rel: str) -> str:
    """doc-relative path → site-friendly .md path."""
    rel = rel.replace("\\", "/")
    if rel.endswith(".md.in"):
        rel = rel[: -len(".in")]
    # chapter/section suffixes used by nixpkgs doc
    rel = re.sub(r"\.chapter\.md$", ".md", rel)
    rel = re.sub(r"\.section\.md$", ".md", rel)
    return rel


def list_doc_markdown(
    s: requests.Session, owner: str, repo: str, ref: str, subpath: str
) -> list[str]:
    """Return repo-relative paths of markdown under subpath."""
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{ref}?recursive=1"
    print(f"Listing tree {owner}/{repo}@{ref} …", file=sys.stderr)
    r = s.get(url, timeout=120)
    r.raise_for_status()
    tree = r.json().get("tree") or []
    prefix = subpath.strip("/") + "/"
    out: list[str] = []
    for item in tree:
        if item.get("type") != "blob":
            continue
        path = item.get("path") or ""
        if not path.startswith(prefix):
            continue
        name = path.rsplit("/", 1)[-1].lower()
        if name in SKIP_NAMES:
            continue
        if not (
            path.endswith((".md", ".md.in"))
            or path.endswith(".chapter.md")
            or path.endswith(".section.md")
        ):
            continue
        # skip internal tooling
        if "/doc-support/" in path or "/tests/" in path:
            continue
        out.append(path)
    return sorted(out)


def should_skip(path: str, *, include_release_notes: bool) -> bool:
    if not include_release_notes and (
        path.startswith("doc/release-notes/") or "/release-notes/" in path
    ):
        return True
    return False


def fetch_text(s: requests.Session, owner: str, repo: str, ref: str, path: str) -> str:
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}"
    r = s.get(raw_url, timeout=60)
    if r.status_code == 404:
        # fallback Contents API
        api = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}"
        r = s.get(api, timeout=60)
        r.raise_for_status()
        data = r.json()
        import base64

        return base64.b64decode(data["content"]).decode("utf-8")
    r.raise_for_status()
    return r.text


def build_summary_from_manual_in(text: str, available: set[str]) -> str:
    """Turn doc/manual.md.in include lists into a simple SUMMARY.md."""
    lines = ["# Nixpkgs Manual", ""]
    # collect include entries
    entries: list[str] = []
    for m in re.finditer(
        r"```\{=include=\}[^\n]*\n([\s\S]*?)```", text
    ):
        body = m.group(1)
        for raw in body.splitlines():
            item = raw.strip()
            if not item or item.startswith("#"):
                continue
            entries.append(item)

    # also preface-style single files from chapters lines
    for m in re.finditer(r"(?m)^\s*([A-Za-z0-9_./-]+\.(?:chapter\.)?md)\s*$", text):
        entries.append(m.group(1).strip())

    seen: set[str] = set()
    ordered: list[str] = []
    for e in entries:
        norm = normalize_rel(e)
        if norm in seen:
            continue
        seen.add(norm)
        ordered.append(norm)

    def title_from_path(p: str) -> str:
        stem = Path(p).stem
        if stem == "index":
            stem = Path(p).parent.name or "index"
        return stem.replace("-", " ").replace("_", " ")

    for rel in ordered:
        # try exact, or as directory index
        candidates = [rel]
        if not rel.endswith(".md"):
            candidates.append(rel + ".md")
            candidates.append(rel.rstrip("/") + "/index.md")
        hit = next((c for c in candidates if c in available), None)
        if not hit:
            # directory part file: using-nixpkgs.md
            if rel.endswith(".md") and rel.replace(".md", "/index.md") in available:
                hit = rel  # parent overview
            else:
                continue
        title = title_from_path(hit)
        lines.append(f"- [{title}](./{hit})")
    lines.append("")
    return "\n".join(lines)


def download_docs(
    s: requests.Session,
    owner: str,
    repo: str,
    ref: str,
    subpath: str,
    dest: Path,
    *,
    include_release_notes: bool,
) -> list[Path]:
    paths = list_doc_markdown(s, owner, repo, ref, subpath)
    written: list[Path] = []
    dest.mkdir(parents=True, exist_ok=True)

    total = len(paths)
    print(f"Downloading {total} markdown paths under {subpath}/ …", file=sys.stderr)

    for i, repo_path in enumerate(paths, 1):
        if should_skip(repo_path, include_release_notes=include_release_notes):
            continue
        rel = repo_path[len(subpath.strip("/")) + 1 :]  # relative to doc/
        out_rel = normalize_rel(rel)
        out = dest / out_rel
        try:
            text = fetch_text(s, owner, repo, ref, repo_path)
        except requests.RequestException as e:
            print(f"  skip {repo_path}: {e}", file=sys.stderr)
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        written.append(out)
        if i % 25 == 0 or i == total:
            print(f"  … {i}/{total}", file=sys.stderr)
        # be nice to GitHub
        time.sleep(0.03)

    return written


def ensure_index(dest: Path, written: list[Path]) -> Path:
    """Write SUMMARY.md + a short index.md if missing."""
    available = {str(p.relative_to(dest)).replace("\\", "/") for p in written}
    summary_path = dest / "SUMMARY.md"
    manual_in = dest / "manual.md"
    # manual.md may have been normalized from manual.md.in
    if (dest / "manual.md.in").is_file() and not manual_in.is_file():
        manual_in.write_text(
            (dest / "manual.md.in").read_text(encoding="utf-8"), encoding="utf-8"
        )

    if manual_in.is_file():
        summary = build_summary_from_manual_in(
            manual_in.read_text(encoding="utf-8"), available
        )
    else:
        lines = ["# Nixpkgs Manual", ""]
        for p in sorted(available):
            if p in {"SUMMARY.md", "manual.md", "README.md"}:
                continue
            lines.append(f"- [{Path(p).stem}](./{p})")
        summary = "\n".join(lines) + "\n"

    summary_path.write_text(summary, encoding="utf-8")
    written.append(summary_path)

    index = dest / "index.md"
    if not index.is_file():
        # thin index pointing at SUMMARY content
        index.write_text(
            "# Nixpkgs Manual\n\n"
            "Persian site route: `/pages/nixpkgs-manual`.\n\n"
            + summary
            + "\n",
            encoding="utf-8",
        )
        written.append(index)
    return summary_path


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default=None)
    parser.add_argument("--repo", default=None)
    parser.add_argument("--ref", default=None)
    parser.add_argument(
        "--path",
        default=None,
        help="Path inside repo (default NIXPKGS_MANUAL_PATH or doc)",
    )
    parser.add_argument("-o", "--output", type=Path, default=None)
    parser.add_argument(
        "--include-release-notes",
        action="store_true",
        help="Also download release-notes/*.md",
    )
    args = parser.parse_args(argv)

    owner = args.owner or env_str("NIXPKGS_MANUAL_OWNER", "NixOS")
    repo = args.repo or env_str("NIXPKGS_MANUAL_REPO", "nixpkgs")
    ref = args.ref or env_str("NIXPKGS_MANUAL_REF", "master")
    path = args.path or env_str("NIXPKGS_MANUAL_PATH", "doc")
    dest = args.output or env_path("NIXPKGS_MANUAL_OUTPUT", "docs/en/nixpkgs-manual")
    include_rn = args.include_release_notes or env_bool(
        "NIXPKGS_MANUAL_INCLUDE_RELEASE_NOTES", False
    )
    base_url = env_str(
        "NIXPKGS_MANUAL_WEB", "https://nixos.org/manual/nixpkgs/stable"
    )

    print(f"Downloading {owner}/{repo}@{ref}:{path} → {dest}", file=sys.stderr)
    s = session()

    if dest.exists():
        for old in dest.rglob("*.md"):
            old.unlink()

    written = download_docs(
        s, owner, repo, ref, path, dest, include_release_notes=include_rn
    )
    ensure_index(dest, written)

    md = [p for p in written if p.suffix.lower() == ".md"]
    manifest = dest / "manifest.json"
    files_rel = sorted(str(p.relative_to(ROOT)) for p in written if p.is_file())
    manifest.write_text(
        json.dumps(
            {
                "source": f"https://github.com/{owner}/{repo}/tree/{ref}/{path}",
                "web": base_url,
                "ref": ref,
                "files": files_rel,
                "markdown": sorted(
                    str(p.relative_to(ROOT)) for p in md if p.is_file()
                ),
                "count": len([p for p in md if p.is_file()]),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"Done: {len(written)} files, {len(md)} markdown → {dest}",
        file=sys.stderr,
    )
    print(f"Manifest: {manifest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
