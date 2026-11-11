import logging
import os
import secrets
from pathlib import PurePosixPath
from urllib.parse import unquote

from fastapi import HTTPException


MAX_BYTES = 50 * 1024 * 1024


def env_int(name, default, maximum):
    raw = os.getenv(name, "").strip()
    try:
        return min(maximum, max(1, int(raw))) if raw else default
    except ValueError:
        logging.getLogger(__name__).warning("Invalid integer environment value ignored: %s=%s", name, raw)
        return default


def safe_basename(name: str) -> str:
    name = (name or "").replace("\\", "/")
    base = PurePosixPath(name).name
    base = unquote(base).strip().strip("\x00")
    if not base or base in {".", ".."}:
        raise HTTPException(status_code=400, detail="Invalid file name")
    if "/" in base or "\\" in base:
        raise HTTPException(status_code=400, detail="Invalid file name")
    return base


def raise_internal_error() -> None:
    error_id = secrets.token_hex(8)
    logging.error("=== ERROR error_id=%s ===", error_id, exc_info=True)
    raise HTTPException(status_code=500, detail=f"Internal Server Error (error_id={error_id})")


def extract_response_text(result) -> str:
    text = getattr(result, "output_text", None)
    if isinstance(text, str) and text:
        return text
    raise RuntimeError("The Responses API did not return text output.")


def response_usage(result) -> dict[str, int | None]:
    usage = getattr(result, "usage", None)
    return {
        key: getattr(usage, key, None)
        for key in ("input_tokens", "output_tokens", "total_tokens")
    }


def merge_usage(*usages: dict[str, int | None]) -> dict[str, int | None]:
    merged: dict[str, int | None] = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    for usage in usages:
        for key, total in merged.items():
            value = usage.get(key)
            merged[key] = None if value is None or total is None else total + value
    return merged
