#!/usr/bin/env python3
"""Fetch nixcloud/tour_of_nix and export questions as Markdown under docs/en/tour-of-nix/.

Source: https://github.com/nixcloud/tour_of_nix (questions.json)
Live:   https://nixcloud.io/tour/
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

from tools.lib.envutil import ROOT, env_path, env_str, load_dotenv

QUESTIONS_URL = (
    "https://raw.githubusercontent.com/nixcloud/tour_of_nix/master/questions.json"
)
REPO_URL = "https://github.com/nixcloud/tour_of_nix"
TOUR_WEB = "https://nixcloud.io/tour/"


def fetch_questions(url: str) -> list[dict]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "nix-notes-tour-import/1.0"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not isinstance(data, list):
        raise SystemExit(f"Unexpected questions.json shape: {type(data)}")
    return data


def slug_path(path: str) -> str:
    """introduction/nix → introduction/nix (safe path segments)."""
    parts = [re.sub(r"[^\w.-]+", "-", p).strip("-") or "x" for p in path.split("/") if p]
    return "/".join(parts) if parts else "index"


def fence_nix(code: str) -> str:
    code = (code or "").rstrip() + "\n"
    # avoid breaking outer fence if code contains ```
    if "```" in code:
        return "````nix\n" + code + "````\n"
    return "```nix\n" + code + "```\n"


def question_to_markdown(item: dict, index: int, total: int) -> str:
    topic = (item.get("topic") or f"Lesson {index + 1}").strip()
    path = (item.get("path") or f"lesson-{index}").strip()
    question = (item.get("question") or "").strip() + "\n"
    code = item.get("code") or ""
    solution = item.get("solution") or ""
    youtube = (item.get("youtube") or "").strip()

    lines: list[str] = [
        f"# {topic}",
        "",
        f"> Lesson **{index + 1}** / {total} · path `{path}`",
        "",
        question.rstrip(),
        "",
    ]

    if code.strip():
        lines += [
            "## Starting code",
            "",
            fence_nix(code).rstrip(),
            "",
        ]

    if solution.strip():
        lines += [
            "## Solution",
            "",
            fence_nix(solution).rstrip(),
            "",
        ]

    if youtube:
        # original field may be a bare id or a full URL
        yt = youtube
        if not yt.startswith("http"):
            yt = f"https://www.youtube.com/watch?v={yt}"
        lines += [
            "## Video",
            "",
            f"[YouTube]({yt})",
            "",
        ]

    lines += [
        "---",
        "",
        f"Source: [A tour of Nix]({TOUR_WEB}?id={path}) · "
        f"[GitHub]({REPO_URL})",
        "",
    ]
    return "\n".join(lines)


def write_index(items: list[dict], out_dir: Path) -> None:
    lines = [
        "# A tour of Nix",
        "",
        "Interactive programming guide for the **Nix language** "
        f"(from [nixcloud/tour_of_nix]({REPO_URL})).",
        "",
        "This Farsi site presents each lesson as a static page with the "
        "prompt, starting code, and solution.",
        "",
        "## Lessons",
        "",
    ]
    for i, item in enumerate(items):
        path = (item.get("path") or f"lesson-{i}").strip()
        topic = (item.get("topic") or path).strip()
        slug = slug_path(path)
        lines.append(f"{i + 1}. [{topic}](./{slug}.md) — `{path}`")
    lines += [
        "",
        f"Original tour: <{TOUR_WEB}>",
        "",
    ]
    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    load_dotenv()
    out_dir = env_path("TOUR_OF_NIX_OUTPUT", "docs/en/tour-of-nix")
    url = env_str("TOUR_OF_NIX_QUESTIONS_URL", QUESTIONS_URL)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching {url} …", file=sys.stderr)
    items = fetch_questions(url)
    print(f"  {len(items)} questions", file=sys.stderr)

    # keep raw json for reference / republish
    (out_dir / "questions.json").write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    written = 0
    for i, item in enumerate(items):
        path = (item.get("path") or f"lesson-{i}").strip()
        slug = slug_path(path)
        dest = out_dir / f"{slug}.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            question_to_markdown(item, i, len(items)),
            encoding="utf-8",
        )
        written += 1
        print(f"  {path} → {dest.relative_to(ROOT)}", file=sys.stderr)

    write_index(items, out_dir)
    print(f"Wrote {written} lessons + index → {out_dir.relative_to(ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
