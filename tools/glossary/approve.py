#!/usr/bin/env python3
"""Approve glossary terms that already have a translation (or suggestion).

Used after glossary-suggest when doing bulk site translation of all nix.dev.
Does NOT invent text — only flips status to approved when FA text exists.
"""

from __future__ import annotations

import argparse
import sys

from tools.lib.envutil import env_path, load_dotenv
from tools.lib.glossary import load_glossary, save_glossary


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--use-suggestion",
        action="store_true",
        help="If translation empty, copy suggestion → translation then approve",
    )
    args = parser.parse_args(argv)

    path = env_path("GLOSSARY_PATH", "glossary.json")
    g = load_glossary(path)
    n = 0
    for e in g.get("entries") or []:
        if not e.get("is_tech"):
            continue
        if e.get("status") == "skipped":
            continue
        tr = (e.get("translation") or "").strip()
        sug = (e.get("suggestion") or "").strip()
        if not tr and args.use_suggestion and sug:
            e["translation"] = sug
            tr = sug
        if tr:
            e["status"] = "approved"
            n += 1
    save_glossary(g, path)
    print(f"Approved {n} tech terms with translations → {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
