#!/usr/bin/env python3
"""Translate ONLY glossary tech terms via the API (not full documents).

Fills entry.translation with model suggestions; leaves status=pending
so you can approve/reject on /glossary-dev before full-doc translation.

Does not send document body or code — only the list of English terms.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any

from openai import OpenAI

from tools.lib.envutil import env_bool, env_float, env_int, env_path, env_str, load_dotenv
from tools.lib.fa_orthography import apply_fa_orthography
from tools.lib.glossary import load_glossary, save_glossary

TERM_SYSTEM = """You are a bilingual EN→FA technical lexicographer for Nix / software engineering docs.

For each English term, propose a short Persian (Farsi) rendering for use in technical documentation.

Rules:
- Reply with a JSON array only (no markdown fences). Each item:
  {"term": "<exact english>", "fa": "<persian>", "note": "<optional short note>"}
- Keep product names Nix, NixOS, Nixpkgs, Linux, macOS, Bash, Glibc, etc. in Latin
  when that is standard; you may add a short Persian gloss in parentheses.
- Prefer concise, consistent terminology (one preferred form, not a paragraph).
- Do not invent new English; use the given term string exactly in "term".
- If the term should stay untranslated, set fa to the Latin form plus a short note.
- Persian orthography: if a gloss uses the word "translation", write ترجمه‌ی
  (heh + ZWNJ + ی only; never hamza-ezafe forms of that word).
- Never use em dashes (—), en dashes (–), or double hyphens (--) in Persian text.
"""


def pending_tech_entries(glossary: dict[str, Any], *, force: bool) -> list[dict]:
    out = []
    for e in glossary.get("entries") or []:
        if not e.get("is_tech"):
            continue
        if e.get("status") == "skipped":
            continue
        if e.get("status") == "approved" and not force:
            continue
        # Skip if already has user-approved translation unless force
        if e.get("status") == "approved" and (e.get("translation") or "").strip() and not force:
            continue
        if (e.get("translation") or "").strip() and e.get("status") == "pending" and not force:
            # already suggested once — skip unless --force
            continue
        if (e.get("translation") or "").strip() and not force:
            continue
        out.append(e)
    return out


def chunked(items: list, n: int):
    for i in range(0, len(items), n):
        yield items[i : i + n]


def call_batch(
    client: OpenAI,
    model: str,
    terms: list[str],
    *,
    temperature: float,
) -> list[dict]:
    payload = json.dumps(terms, ensure_ascii=False)
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": TERM_SYSTEM},
            {
                "role": "user",
                "content": (
                    "Translate these English technical terms to Persian for a Nix tutorial glossary. "
                    "Return JSON array only:\n" + payload
                ),
            },
        ],
    )
    content = (resp.choices[0].message.content or "").strip()
    if content.startswith("```"):
        content = content.strip("`")
        if content.startswith("json"):
            content = content[4:].strip()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # try extract array
        start, end = content.find("["), content.rfind("]")
        if start >= 0 and end > start:
            data = json.loads(content[start : end + 1])
        else:
            raise RuntimeError(f"Model did not return JSON: {content[:400]}")
    if not isinstance(data, list):
        raise RuntimeError("Expected JSON array from model")
    return data


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--glossary",
        default=None,
        help="glossary.json path",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-suggest even if translation already filled",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=None,
        help="Terms per API call (default GLOSSARY_SUGGEST_BATCH)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max terms this run (0 = all pending)",
    )
    args = parser.parse_args(argv)

    path = env_path("GLOSSARY_PATH", "glossary.json")
    if args.glossary:
        from pathlib import Path

        path = Path(args.glossary)

    api_key = env_str("OPENAI_API_KEY", "")
    if not api_key:
        print("OPENAI_API_KEY missing in .env", file=sys.stderr)
        return 1

    base_url = env_str("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
    model = env_str("OPENAI_MODEL", "google/gemini-3.5-flash-lite")
    temperature = env_float("OPENAI_TEMPERATURE", 0.2)
    pause = env_float("OPENAI_REQUEST_PAUSE_SEC", 0.3)
    batch_size = args.batch_size or env_int("GLOSSARY_SUGGEST_BATCH", 40)

    glossary = load_glossary(path)
    pending = pending_tech_entries(glossary, force=args.force or env_bool("GLOSSARY_SUGGEST_FORCE", False))
    if args.limit and args.limit > 0:
        pending = pending[: args.limit]

    if not pending:
        print("No pending tech terms to suggest. Nothing to do.", file=sys.stderr)
        print(
            f"Open /glossary-dev to review. Full translate needs approved terms.",
            file=sys.stderr,
        )
        return 0

    print(
        f"Suggesting FA for {len(pending)} terms via {model} (batch={batch_size})…",
        file=sys.stderr,
    )

    headers = {}
    if env_str("OPENAI_HTTP_REFERER", ""):
        headers["HTTP-Referer"] = env_str("OPENAI_HTTP_REFERER", "")
    if env_str("OPENAI_APP_TITLE", ""):
        headers["X-Title"] = env_str("OPENAI_APP_TITLE", "")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers=headers or None,
    )

    by_term = {e["term"].lower(): e for e in glossary["entries"]}
    updated = 0

    for batch in chunked(pending, batch_size):
        terms = [e["term"] for e in batch]
        print(f"  batch of {len(terms)}…", file=sys.stderr)
        try:
            results = call_batch(client, model, terms, temperature=temperature)
        except Exception as exc:
            print(f"  ERROR: {exc}", file=sys.stderr)
            return 1

        result_map: dict[str, dict] = {}
        for item in results:
            if not isinstance(item, dict):
                continue
            t = str(item.get("term") or "").strip().lower()
            fa = apply_fa_orthography(
                str(item.get("fa") or item.get("translation") or "").strip()
            )
            note = apply_fa_orthography(str(item.get("note") or "").strip())
            if t and fa:
                result_map[t] = {"fa": fa, "note": note}

        for e in batch:
            key = e["term"].lower()
            hit = result_map.get(key)
            if not hit:
                # fuzzy: model may change casing only
                continue
            target = by_term.get(key, e)
            target["translation"] = hit["fa"]
            # keep lexicon suggestion separate; store API note
            if hit["note"]:
                prev = (target.get("notes") or "").strip()
                api_note = f"API: {hit['note']}"
                target["notes"] = f"{prev}\n{api_note}".strip() if prev else api_note
            # leave status pending for human review
            if target.get("status") == "approved" and not args.force:
                pass
            else:
                target["status"] = "pending"
            # also fill suggestion if empty
            if not (target.get("suggestion") or "").strip():
                target["suggestion"] = hit["fa"]
            updated += 1

        if pause > 0:
            time.sleep(pause)

    save_glossary(glossary, path)
    print(
        f"Updated {updated} terms in {path}. Status remains pending — review at /glossary-dev.",
        file=sys.stderr,
    )
    print(
        "When happy: mark terms Approved (or use «تأیید همهٔ پرشده‌ها»), then: make translate-docs",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
