#!/usr/bin/env python3
"""Download nix.dev documentation sources from GitHub.

Default: entire `source/` tree → docs/en/ (full site, not only first-steps).
Uses zipball (fast) by default.
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import zipfile
from pathlib import Path

import requests

from tools.lib.envutil import ROOT, env_int, env_path, env_str, load_dotenv


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


def download_via_zip(
    s: requests.Session,
    owner: str,
    repo: str,
    ref: str,
    subpath: str,
    dest: Path,
) -> list[Path]:
    url = f"https://codeload.github.com/{owner}/{repo}/zip/refs/heads/{ref}"
    print(f"Fetching zip {url} …", file=sys.stderr)
    r = s.get(url, timeout=180)
    r.raise_for_status()
    written: list[Path] = []
    sub = subpath.strip("/")
    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
        prefix = None
        for name in zf.namelist():
            parts = name.split("/", 1)
            if len(parts) == 2:
                prefix = parts[0] + "/"
                break
        if not prefix:
            raise RuntimeError("Unexpected zip layout")
        want = prefix + sub + "/" if sub else prefix
        for name in zf.namelist():
            if not name.startswith(want) or name.endswith("/"):
                continue
            rel = name[len(want) :]
            if not rel:
                continue
            # skip sphinx junk
            if any(
                part.startswith("_") and part not in ("_static",)
                for part in Path(rel).parts
            ):
                # keep content; skip conf-only paths
                pass
            if rel.endswith((".pyc", ".png", ".jpg", ".svg", ".gif", ".ico")):
                # skip most binary assets for now (can add later)
                if not rel.endswith((".md", ".rst", ".txt")):
                    continue
            if not rel.endswith((".md", ".rst", ".mdx", ".txt")):
                continue
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(zf.read(name))
            written.append(out)
    return written


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default=None)
    parser.add_argument("--repo", default=None)
    parser.add_argument("--ref", default=None)
    parser.add_argument(
        "--path",
        default=None,
        help="Path inside repo (default NIX_DEV_PATH or source)",
    )
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args(argv)

    owner = args.owner or env_str("NIX_DEV_OWNER", "NixOS")
    repo = args.repo or env_str("NIX_DEV_REPO", "nix.dev")
    ref = args.ref or env_str("NIX_DEV_REF", "master")
    path = args.path or env_str("NIX_DEV_PATH", "source")
    dest = args.output or env_path("NIX_DEV_OUTPUT", "docs/en")

    print(f"Downloading {owner}/{repo}@{ref}:{path} → {dest}", file=sys.stderr)
    s = session()
    written = download_via_zip(s, owner, repo, ref, path, dest)

    md = [p for p in written if p.suffix.lower() in {".md", ".mdx", ".rst"}]
    manifest = dest / "manifest.json"
    files_rel = sorted(str(p.relative_to(ROOT)) for p in written)
    md_rel = sorted(str(p.relative_to(ROOT)) for p in md)
    manifest.write_text(
        json.dumps(
            {
                "source": f"https://github.com/{owner}/{repo}/tree/{ref}/{path}",
                "web": env_str("NIX_DEV_WEB", "https://nix.dev/"),
                "ref": ref,
                "files": files_rel,
                "markdown": md_rel,
                "count": len(md_rel),
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
