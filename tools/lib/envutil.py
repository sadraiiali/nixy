"""Load project configuration from a local `.env` file.

All secrets and tunables for download/translate live in `.env`
(see `.env.example`). Environment variables already set in the shell
take precedence over file values.
"""

from __future__ import annotations

import os
from pathlib import Path

# Project root (…/tools/lib/envutil.py → parents[2])
ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"


def load_dotenv(path: Path | None = None, *, override: bool = False) -> Path | None:
    """Parse KEY=VALUE lines into os.environ. Returns path if loaded."""
    env_file = path or ENV_PATH
    if not env_file.is_file():
        return None

    for raw in env_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if not key:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if override or key not in os.environ:
            os.environ[key] = value
    return env_file


def env(key: str, default: str | None = None) -> str | None:
    load_dotenv()
    val = os.environ.get(key)
    if val is None or val == "":
        return default
    return val


def env_str(key: str, default: str = "") -> str:
    v = env(key, default)
    return default if v is None else v


def env_int(key: str, default: int) -> int:
    v = env(key)
    if v is None:
        return default
    return int(v)


def env_float(key: str, default: float) -> float:
    v = env(key)
    if v is None:
        return default
    return float(v)


def env_bool(key: str, default: bool = False) -> bool:
    v = env(key)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "on"}


def env_path(key: str, default: str | Path) -> Path:
    v = env(key)
    p = Path(v) if v else Path(default)
    if not p.is_absolute():
        p = ROOT / p
    return p
