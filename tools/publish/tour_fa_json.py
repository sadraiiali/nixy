#!/usr/bin/env python3
"""Build static/tour-of-nix/questions.fa.json from EN questions + FA markdown.

Keeps original code/solution (Nix) and uses Farsi prose from docs/fa/tour-of-nix.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from tools.lib.envutil import ROOT, env_path, load_dotenv

SECTION_SPLIT = re.compile(
    r"^##\s+(?:کد شروع|Starting code|راه‌حل|Solution|Video|ویدیو)\s*$",
    re.M | re.I,
)


def slug_path(path: str) -> str:
    parts = [re.sub(r"[^\w.-]+", "-", p).strip("-") or "x" for p in path.split("/") if p]
    return "/".join(parts) if parts else "index"


def extract_fa_question(md: str) -> tuple[str, str]:
    """Return (topic, question_body_markdown)."""
    lines = md.splitlines()
    topic = "درس"
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            topic = line[2:].strip()
            body_start = i + 1
            break
    rest = "\n".join(lines[body_start:])
    # drop lesson meta blockquote
    rest = re.sub(r"^>\s*درس[^\n]*\n(?:^>\s*[^\n]*\n)*", "", rest, count=1, flags=re.M)
    # cut at first code/solution section
    m = SECTION_SPLIT.search(rest)
    if m:
        rest = rest[: m.start()]
    return topic, rest.strip() + "\n"


def main() -> int:
    load_dotenv()
    en_json = env_path("TOUR_OF_NIX_EN_JSON", "static/tour-of-nix/questions.en.json")
    if not en_json.is_file():
        en_json = env_path("TOUR_OF_NIX_OUTPUT", "docs/en/tour-of-nix") / "questions.json"
    fa_root = env_path("TOUR_OF_NIX_FA", "docs/fa/tour-of-nix")
    out = ROOT / "static/tour-of-nix/questions.fa.json"

    items = json.loads(en_json.read_text(encoding="utf-8"))
    out_items: list[dict] = []
    for i, item in enumerate(items):
        path = (item.get("path") or f"lesson-{i}").strip()
        slug = slug_path(path)
        md_path = fa_root / f"{slug}.md"
        topic = (item.get("topic") or path).strip()
        question = (item.get("question") or "").strip() + "\n"
        if md_path.is_file():
            t, q = extract_fa_question(md_path.read_text(encoding="utf-8"))
            if t:
                topic = t
            if q.strip():
                question = q
        else:
            print(f"  warn: missing FA md for {path}", file=sys.stderr)

        out_items.append(
            {
                "topic": topic,
                "path": path,
                "question": question,
                "code": item.get("code") or "",
                "solution": item.get("solution") or "",
                "youtube": item.get("youtube") or "",
            }
        )
        print(f"  {path} → {topic[:40]}", file=sys.stderr)

    text = json.dumps(out_items, ensure_ascii=False, indent=2) + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {len(out_items)} lessons → {out.relative_to(ROOT)}", file=sys.stderr)
    # Slim path+topic index for command palette (must live under src/ — Vite forbids importing /static)
    lessons = [{"path": it["path"], "topic": it["topic"]} for it in out_items]
    lib_out = ROOT / "src/lib/tour-of-nix-lessons.json"
    lib_out.parent.mkdir(parents=True, exist_ok=True)
    lib_out.write_text(json.dumps(lessons, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(lessons)} lesson ids → {lib_out.relative_to(ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
