"""Shared glossary load/save used by build, translate, and (via JSON) the web UI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.lib.envutil import ROOT, env_path, load_dotenv

GLOSSARY_VERSION = 1


def default_glossary_path() -> Path:
    load_dotenv()
    return env_path("GLOSSARY_PATH", "glossary.json")


def empty_glossary() -> dict[str, Any]:
    return {
        "version": GLOSSARY_VERSION,
        "docs": [],
        "entries": [],
    }


def load_glossary(path: Path | None = None) -> dict[str, Any]:
    p = path or default_glossary_path()
    if not p.is_file():
        return empty_glossary()
    data = json.loads(p.read_text(encoding="utf-8"))
    if "entries" not in data:
        data["entries"] = []
    if "docs" not in data:
        data["docs"] = []
    data.setdefault("version", GLOSSARY_VERSION)
    return data


def save_glossary(data: dict[str, Any], path: Path | None = None) -> Path:
    p = path or default_glossary_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    # Stable sort: pending tech first, then alpha
    entries = data.get("entries") or []
    entries.sort(
        key=lambda e: (
            0 if e.get("status") == "pending" else 1,
            0 if e.get("is_tech") else 1,
            (e.get("term") or "").lower(),
        )
    )
    data["entries"] = entries
    p.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return p


def approved_translations(
    data: dict[str, Any] | None = None,
    *,
    require_approved: bool = True,
) -> list[tuple[str, str]]:
    """Return (english_term, farsi_translation) for full-document translate.

    By default only status=approved terms are used (after your review).
    Set require_approved=False to also use any non-empty translation.
    """
    g = data if data is not None else load_glossary()
    out: list[tuple[str, str]] = []
    for e in g.get("entries") or []:
        if e.get("status") == "skipped":
            continue
        if require_approved and e.get("status") != "approved":
            continue
        term = (e.get("term") or "").strip()
        tr = (e.get("translation") or "").strip()
        if not tr:
            tr = (e.get("suggestion") or "").strip()
        if term and tr:
            out.append((term, tr))
    out.sort(key=lambda t: len(t[0]), reverse=True)
    return out


def glossary_review_stats(data: dict[str, Any] | None = None) -> dict[str, int]:
    g = data if data is not None else load_glossary()
    tech = [e for e in g.get("entries") or [] if e.get("is_tech")]
    approved = [e for e in tech if e.get("status") == "approved"]
    pending = [e for e in tech if e.get("status") == "pending"]
    skipped = [e for e in tech if e.get("status") == "skipped"]
    with_tr = [e for e in tech if (e.get("translation") or "").strip()]
    return {
        "tech": len(tech),
        "approved": len(approved),
        "pending": len(pending),
        "skipped": len(skipped),
        "with_translation": len(with_tr),
    }


def assert_ready_for_full_translate(
    data: dict[str, Any] | None = None,
    *,
    min_approved: int | None = None,
    require_no_pending: bool = False,
) -> None:
    """Raise SystemExit with a clear message if glossary is not review-ready."""
    g = data if data is not None else load_glossary()
    stats = glossary_review_stats(g)
    min_a = min_approved
    if min_a is None:
        from tools.lib.envutil import env_int

        min_a = env_int("TRANSLATE_MIN_APPROVED", 1)

    if stats["approved"] < min_a:
        raise SystemExit(
            f"Glossary not ready for full translation: "
            f"{stats['approved']} approved tech terms (need ≥ {min_a}). "
            f"Pending={stats['pending']}, with_translation={stats['with_translation']}. "
            f"Run: make glossary → make glossary-suggest → review /glossary-dev → approve → make translate-docs"
        )
    if require_no_pending and stats["pending"] > 0:
        raise SystemExit(
            f"Still {stats['pending']} pending tech terms. "
            f"Approve or skip them on /glossary-dev before full translate "
            f"(or set TRANSLATE_REQUIRE_NO_PENDING=false)."
        )


def format_glossary_for_prompt(
    pairs: list[tuple[str, str]] | None = None,
    *,
    require_approved: bool = True,
) -> str:
    pairs = (
        pairs
        if pairs is not None
        else approved_translations(require_approved=require_approved)
    )
    if not pairs:
        return ""
    lines = [
        "GLOSSARY — use these exact Farsi renderings for the English terms "
        "(case-insensitive match in prose; do not change code/backticks):",
    ]
    for en, fa in pairs:
        lines.append(f"- {en} → {fa}")
    return "\n".join(lines)
