#!/usr/bin/env python3
"""Download the Nix *reference manual* sources (NixOS/nix doc/manual).

Default: GitHub zipball of NixOS/nix → docs/en/nix-manual/
Skips release-notes by default (huge changelog); set NIX_MANUAL_INCLUDE_RELEASE_NOTES=true
to keep them.

Also rewrites the overview page docs/en/reference/nix-manual.md placeholders
when NIX_MANUAL_SUBSTITUTE=true (default).
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import requests

from tools.lib.envutil import ROOT, env_bool, env_path, env_str, load_dotenv


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


def resolve_versions(s: requests.Session) -> dict[str, str]:
    """Map @nix-latest@ style keys to concrete versions (redirects + pins)."""
    versions: dict[str, str] = {
        "nix-latest": "2.35",
        "nix-rolling": "2.34",
        "nix-stable": "2.34",
        "nix-prev-stable": "2.31",
        "nixpkgs-stable": "26.05",
        "nixpkgs-prev-stable": "25.11",
    }
    for key, channel in (
        ("nix-latest", "latest"),
        ("nix-rolling", "rolling"),
        ("nix-stable", "stable"),
        ("nix-prev-stable", "prev-stable"),
    ):
        try:
            r = s.head(
                f"https://nix.dev/manual/nix/{channel}/",
                allow_redirects=True,
                timeout=20,
            )
            m = re.search(r"/manual/nix/([^/]+)/?", r.url)
            if m and m.group(1) not in {
                "latest",
                "rolling",
                "stable",
                "prev-stable",
                "development",
            }:
                versions[key] = m.group(1)
        except requests.RequestException:
            pass

    try:
        r = s.get(
            "https://raw.githubusercontent.com/NixOS/nix.dev/master/nix/sources.json",
            timeout=20,
        )
        r.raise_for_status()
        pins = (r.json().get("pins") or r.json())
        sorted_rel = sorted(
            (k for k in pins if re.fullmatch(r"\d+\.\d+", k)),
            key=lambda s: tuple(int(p) for p in s.split(".")),
        )
        if sorted_rel:
            versions["nixpkgs-stable"] = sorted_rel[-1]
        if len(sorted_rel) >= 2:
            versions["nixpkgs-prev-stable"] = sorted_rel[-2]
    except (requests.RequestException, ValueError, KeyError):
        pass
    return versions


def substitute_placeholders(text: str, versions: dict[str, str]) -> str:
    for key, val in versions.items():
        text = text.replace(f"@{key}@", val)
    return text


def download_via_zip(
    s: requests.Session,
    owner: str,
    repo: str,
    ref: str,
    subpath: str,
    dest: Path,
    *,
    include_release_notes: bool,
) -> list[Path]:
    url = f"https://codeload.github.com/{owner}/{repo}/zip/refs/heads/{ref}"
    print(f"Fetching zip {url} …", file=sys.stderr)
    r = s.get(url, timeout=300)
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
            # drop generated / binary noise
            if rel.endswith(
                (".pyc", ".png", ".jpg", ".svg", ".gif", ".ico", ".css", ".js")
            ):
                continue
            # keep markdown (and .md.in templates as .md)
            if not (
                rel.endswith((".md", ".md.in", ".mdx", ".txt"))
                or rel.endswith("SUMMARY.md.in")
            ):
                continue
            if not include_release_notes and (
                rel.startswith("release-notes/") or "/release-notes/" in rel
            ):
                continue
            # normalize .md.in → .md
            out_rel = rel
            if out_rel.endswith(".md.in"):
                out_rel = out_rel[: -len(".in")]
            out = dest / out_rel
            out.parent.mkdir(parents=True, exist_ok=True)
            raw = zf.read(name)
            # strip simple @var@ that mdBook uses for anchors when obvious
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                out.write_bytes(raw)
                written.append(out)
                continue
            out.write_text(text, encoding="utf-8")
            written.append(out)
    return written


def rewrite_overview(versions: dict[str, str]) -> None:
    """Replace placeholders in docs/*/reference/nix-manual.md with concrete versions.

    Also expand empty [](channel-branches) style refs to inline FAQ URLs so the
    page is usable outside Sphinx.
    """
    for lang in ("en", "fa"):
        path = ROOT / "docs" / lang / "reference" / "nix-manual.md"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        text = substitute_placeholders(text, versions)
        # Empty markdown links to channel-branches → FAQ anchor
        faq = (
            "https://nix.dev/concepts/faq.html#channel-branches"
            if lang == "en"
            else "/pages/nix-dev/concepts/faq#channel-branches"
        )
        text = re.sub(
            r"\[\]\(channel-branches\)",
            f"[channel branches]({faq})",
            text,
        )
        path.write_text(text, encoding="utf-8")
        print(f"  substituted placeholders → {path.relative_to(ROOT)}", file=sys.stderr)

    # reference/index.md: ensure external manuals stay as explicit list in source
    # (publish also converts toctree; this makes the EN/FA sources readable raw)
    for lang in ("en", "fa"):
        path = ROOT / "docs" / lang / "reference" / "index.md"
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "/pages/nixpkgs-manual" in text and "## " not in text:
            # inject a markdown list after the intro if only toctree has links
            extra = {
                "en": """
## Manuals and references

- [Glossary](./glossary.md)
- [Nix reference manual (versions)](./nix-manual.md)
- [Nixpkgs manual](/pages/nixpkgs-manual)
- [NixOS manual](https://nixos.org/manual/nixos/stable/)
- [Community projects](https://github.com/nix-community/)
- [Support tools (awesome-nix)](https://github.com/nix-community/awesome-nix)
- [Further reading](../recommended-reading.md)
- [Pinning Nixpkgs](./pinning-nixpkgs.md)
""",
                "fa": """
## راهنماها و مراجع

- [واژه‌نامه](./glossary.md)
- [راهنمای مرجع Nix (نسخه‌ها)](./nix-manual.md)
- [راهنمای Nixpkgs](/pages/nixpkgs-manual)
- [راهنمای NixOS](https://nixos.org/manual/nixos/stable/)
- [پروژه‌های جامعه](https://github.com/nix-community/)
- [ابزارهای پشتیبانی (awesome-nix)](https://github.com/nix-community/awesome-nix)
- [مطالعهٔ بیشتر](../recommended-reading.md)
- [قفل‌کردن Nixpkgs](./pinning-nixpkgs.md)
""",
            }[lang]
            # insert after first paragraph block (after toctree)
            if "```{toctree}" in text:
                text = re.sub(
                    r"(```\{toctree\}[\s\S]*?```)",
                    r"\1\n" + extra,
                    text,
                    count=1,
                )
                path.write_text(text, encoding="utf-8")
                print(f"  added inline manual links → {path.relative_to(ROOT)}", file=sys.stderr)


def collect_missing_docroot_targets(dest: Path) -> set[str]:
    """Paths (relative to dest, with .md) referenced via @docroot@ or SUMMARY but missing."""
    missing: set[str] = set()
    docroot_re = re.compile(
        r"(?:@docroot@|_at_docroot@)/([^\s\)\]#>\"']+\.md)", re.I
    )
    for md in dest.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for m in docroot_re.finditer(text):
            rel = m.group(1).lstrip("/")
            if not (dest / rel).is_file():
                missing.add(rel)
    # SUMMARY.md link targets
    summary = dest / "SUMMARY.md"
    if summary.is_file():
        for m in re.finditer(r"\(([^)#]+\.md)(?:#[^)]*)?\)", summary.read_text(encoding="utf-8")):
            rel = m.group(1).lstrip("./")
            if rel.startswith("release-notes/"):
                continue
            if not (dest / rel).is_file():
                missing.add(rel)
    return missing


def fetch_generated_pages_from_web(
    dest: Path,
    base_url: str,
    *,
    missing: set[str] | None = None,
) -> list[Path]:
    """Fetch build-generated manual pages (conf-file, builtins, store types, …)
    from the published HTML on nix.dev / nixos.org and convert to Markdown.

    These files are not present as plain .md in the Nix git tree.
    """
    from download_page import fetch_html, html_to_markdown

    targets = missing if missing is not None else collect_missing_docroot_targets(dest)
    # Always try conf-file / builtins if still absent
    for must in (
        "command-ref/conf-file.md",
        "language/builtins.md",
    ):
        if not (dest / must).is_file():
            targets.add(must)

    written: list[Path] = []
    base = base_url.rstrip("/")
    for rel in sorted(targets):
        if rel.startswith("release-notes/"):
            continue
        # map .md → online .html path
        url_path = rel[:-3] if rel.endswith(".md") else rel
        if url_path.endswith("/index"):
            url_path = url_path[: -len("/index")] + "/"
            url = f"{base}/{url_path}"
        else:
            url = f"{base}/{url_path}.html"
        out = dest / rel
        try:
            print(f"  fetch generated {rel} ← {url}", file=sys.stderr)
            html = fetch_html(url, timeout=60)
            md = html_to_markdown(html, url)
            # Prefer relative links for local publish
            md = re.sub(
                rf"\({re.escape(base)}/([^)#]+?)(?:\.html)?(#[^)]*)?\)",
                lambda m: f"(@docroot@/{m.group(1)}.md{m.group(2) or ''})",
                md,
            )
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(md, encoding="utf-8")
            written.append(out)
        except Exception as e:  # noqa: BLE001 — continue remaining pages
            print(f"  WARN: could not fetch {rel}: {e}", file=sys.stderr)
    return written


def rewrite_relative_links_to_absolute(dest: Path, base_url: str) -> int:
    """Turn (path.md) links into absolute https://nix.dev/manual/nix/stable/… URLs.

    Helps offline/webxdc readers open (or copy) a working URL.
    """
    n = 0
    link_re = re.compile(
        r"\[([^\]]*)\]\((?!https?://|mailto:|#|/)([^)]+\.md)(#[^)]*)?\)"
    )

    def sub(m: re.Match, file: Path) -> str:
        nonlocal n
        text, rel, frag = m.group(1), m.group(2), m.group(3) or ""
        # resolve relative to current file
        try:
            target = (file.parent / rel).resolve().relative_to(dest.resolve())
        except ValueError:
            target = Path(rel)
        # mdBook path without .md
        url_path = target.as_posix()
        if url_path.endswith(".md"):
            url_path = url_path[:-3]
        if url_path.endswith("/index"):
            url_path = url_path[: -len("/index")] + "/"
        href = f"{base_url.rstrip('/')}/{url_path}{frag}"
        n += 1
        return f"[{text}]({href})"

    for md in dest.rglob("*.md"):
        raw = md.read_text(encoding="utf-8")

        def repl(m: re.Match, _f=md) -> str:
            return sub(m, _f)

        new = link_re.sub(repl, raw)
        if new != raw:
            md.write_text(new, encoding="utf-8")
    return n


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default=None)
    parser.add_argument("--repo", default=None)
    parser.add_argument("--ref", default=None)
    parser.add_argument(
        "--path",
        default=None,
        help="Path inside repo (default NIX_MANUAL_PATH or doc/manual/source)",
    )
    parser.add_argument("-o", "--output", type=Path, default=None)
    parser.add_argument(
        "--include-release-notes",
        action="store_true",
        help="Also download release-notes/*.md",
    )
    parser.add_argument(
        "--no-absolute-urls",
        action="store_true",
        help="Keep relative .md links (default: rewrite to nix.dev stable URLs)",
    )
    args = parser.parse_args(argv)

    owner = args.owner or env_str("NIX_MANUAL_OWNER", "NixOS")
    repo = args.repo or env_str("NIX_MANUAL_REPO", "nix")
    ref = args.ref or env_str("NIX_MANUAL_REF", "master")
    path = args.path or env_str("NIX_MANUAL_PATH", "doc/manual/source")
    dest = args.output or env_path("NIX_MANUAL_OUTPUT", "docs/en/nix-manual")
    include_rn = args.include_release_notes or env_bool(
        "NIX_MANUAL_INCLUDE_RELEASE_NOTES", False
    )
    # Default False: keep relative links so publish can map them to local FA routes.
    # Set NIX_MANUAL_ABSOLUTE_URLS=true to point every link at nix.dev instead.
    do_abs = (not args.no_absolute_urls) and env_bool(
        "NIX_MANUAL_ABSOLUTE_URLS", False
    )
    base_url = env_str(
        "NIX_MANUAL_WEB", "https://nix.dev/manual/nix/stable"
    )

    print(f"Downloading {owner}/{repo}@{ref}:{path} → {dest}", file=sys.stderr)
    s = session()
    versions = resolve_versions(s)
    print(f"Versions: {versions}", file=sys.stderr)

    if dest.exists():
        # clean previous md tree lightly
        for old in dest.rglob("*.md"):
            old.unlink()

    written = download_via_zip(
        s, owner, repo, ref, path, dest, include_release_notes=include_rn
    )

    # conf-file.md, builtins.md, store/types/*, new-cli/* are generated at
    # doc-build time — pull missing ones from the published web manual.
    if env_bool("NIX_MANUAL_FETCH_GENERATED", True):
        missing = collect_missing_docroot_targets(dest)
        if missing:
            print(
                f"Fetching {len(missing)} generated/missing page(s) from {base_url} …",
                file=sys.stderr,
            )
            written.extend(
                fetch_generated_pages_from_web(dest, base_url, missing=missing)
            )

    if do_abs:
        n = rewrite_relative_links_to_absolute(dest, base_url)
        print(f"Rewrote {n} relative links → {base_url}/…", file=sys.stderr)

    if env_bool("NIX_MANUAL_SUBSTITUTE", True):
        rewrite_overview(versions)

    md = [p for p in written if p.suffix.lower() == ".md" and p.is_file()]
    manifest = dest / "manifest.json"
    files_rel = sorted(str(p.relative_to(ROOT)) for p in written)
    manifest.write_text(
        json.dumps(
            {
                "source": f"https://github.com/{owner}/{repo}/tree/{ref}/{path}",
                "web": base_url,
                "ref": ref,
                "versions": versions,
                "files": files_rel,
                "markdown": sorted(str(p.relative_to(ROOT)) for p in md),
                "count": len(md),
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
