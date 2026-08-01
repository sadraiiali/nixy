#!/usr/bin/env python3
"""Rephrase Persian (Farsi) site copy via OpenRouter / Gemini.

Uses `.env` (`OPENAI_API_KEY`, `OPENAI_BASE_URL`, …). Default model:
`google/gemini-3.6-flash` (override with `--model` or `REPHRASE_FA_MODEL`).

Examples (from repo root):

  uv run python scripts/rephrase_fa.py --formal "می‌خواستم نیکس را…"
  uv run python scripts/rephrase_fa.py --informal --meaning "state license compliance" < draft.txt
  echo "…" | uv run python scripts/rephrase_fa.py --formal
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow `tools.*` imports when run as scripts/rephrase_fa.py
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from openai import OpenAI

from tools.lib.envutil import env_float, env_str, load_dotenv
from tools.lib.fa_orthography import apply_fa_orthography

DEFAULT_MODEL = "google/gemini-3.6-flash"

SYSTEM = """\
You are a native Persian (Farsi) writer for a documentation website.

Rules:
- Output ONLY the rephrased Persian text. No headings, labels, quotes, or commentary.
- Do NOT use em dashes (—), en dashes (–), or double hyphens (--). Ever.
- Do not invent facts. Keep the same meaning unless --meaning / instructions say otherwise.
- Keep the register consistent end-to-end: either fully formal or fully informal, never mixed.
- Orthography: always write ترجمه‌ی (heh + ZWNJ + ی; never hamza-ezafe on that word).
"""


def build_prompt(*, text: str, register: str, meaning: str) -> str:
    reg = (
        "fully formal (رسمی) written Persian; warm and clear, not bureaucratic or colloquial"
        if register == "formal"
        else "fully informal (غیررسمی) natural spoken-leaning Persian; still clear and polite"
    )
    parts = [
        f"Register: {reg}.",
        "Rephrase the following text.",
    ]
    if meaning.strip():
        parts.append(f"Intended meaning / constraints:\n{meaning.strip()}")
    parts.append(f"Text:\n{text.strip()}")
    return "\n\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description=__doc__)
    reg = parser.add_mutually_exclusive_group()
    reg.add_argument(
        "--formal",
        action="store_const",
        const="formal",
        dest="register",
        help="Fully formal Persian (default)",
    )
    reg.add_argument(
        "--informal",
        action="store_const",
        const="informal",
        dest="register",
        help="Fully informal Persian",
    )
    parser.set_defaults(register="formal")
    parser.add_argument(
        "--meaning",
        "-m",
        default="",
        help="Extra meaning / constraints for the model (English or Persian)",
    )
    parser.add_argument(
        "--model",
        default="",
        help=f"Model id (default: REPHRASE_FA_MODEL or {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Sampling temperature (default: OPENAI_TEMPERATURE or 0.5)",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="Text to rephrase (or pass via stdin)",
    )
    args = parser.parse_args(argv)

    text = " ".join(args.text).strip()
    if not text:
        if sys.stdin.isatty():
            print("Provide text as arguments or via stdin.", file=sys.stderr)
            return 2
        text = sys.stdin.read().strip()
    if not text:
        print("Empty input.", file=sys.stderr)
        return 2

    api_key = env_str("OPENAI_API_KEY", "")
    if not api_key:
        print(
            "OPENAI_API_KEY is not set. Add it to .env (see .env.example).",
            file=sys.stderr,
        )
        return 1

    base_url = env_str("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
    # Prefer 3.6-flash for Farsi copy; do not fall back to OPENAI_MODEL (often a lite model).
    model = args.model or env_str("REPHRASE_FA_MODEL", "") or DEFAULT_MODEL
    temperature = (
        args.temperature
        if args.temperature is not None
        else env_float("OPENAI_TEMPERATURE", 0.5)
    )

    headers: dict[str, str] = {}
    referer = env_str("OPENAI_HTTP_REFERER", "")
    title = env_str("OPENAI_APP_TITLE", "")
    if referer:
        headers["HTTP-Referer"] = referer
    if title:
        headers["X-Title"] = title

    print(f"Model: {model} @ {base_url}  register={args.register}", file=sys.stderr)

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers=headers or None,
    )
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": build_prompt(
                    text=text,
                    register=args.register,
                    meaning=args.meaning,
                ),
            },
        ],
    )
    out = (resp.choices[0].message.content or "").strip()
    if (out.startswith("«") and out.endswith("»")) or (
        len(out) >= 2 and out[0] == out[-1] and out[0] in "\"'"
    ):
        out = out[1:-1].strip()

    print(apply_fa_orthography(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
