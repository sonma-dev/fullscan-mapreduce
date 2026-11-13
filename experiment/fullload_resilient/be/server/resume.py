"""Stage checkpoints and explicit import of pre-checkpoint Markdown runs."""

import hashlib
import json
import os
import re
from pathlib import Path

from fastapi import HTTPException

from server.specifications import SPECIFICATION_STAGES, completed_prefix


CHECKPOINT_NAME = "checkpoint.json"
SCHEMA_VERSION = 1
MAX_CHECKPOINT_BYTES = 1024 * 1024
MAX_MARKDOWN_BYTES = 16 * 1024 * 1024 + 1024
BACKEND_DIR = Path(__file__).resolve().parents[1]
USAGE_KEYS = ("input_tokens", "output_tokens", "total_tokens")
SETTINGS = ("LLM_MAX_QUERY_BYTES", "LLM_MAX_OUTPUT_TOKENS", "LLM_FINAL_MAX_BYTES")
RUN_ID_PATTERN = r"fullload_[0-9]{14}_[a-zA-Z0-9_-]+"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_identity(file_bytes: bytes, file_name: str) -> dict:
    """Fingerprint code, prompts and non-secret settings; never persist credentials."""
    digest = hashlib.sha256()
    paths = [BACKEND_DIR / "requirements.txt"]
    for directory, pattern in (("server", "*.py"), ("plugins", "*.py"), ("prompt", "*.jinja2")):
        paths.extend((BACKEND_DIR / directory).rglob(pattern))
    for path in sorted(paths):
        digest.update(path.relative_to(BACKEND_DIR).as_posix().encode() + b"\0")
        digest.update(path.read_bytes() + b"\0")
    settings = {key: os.getenv(key, "").strip() for key in SETTINGS}
    settings["deployment"] = os.getenv("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "")
    settings["endpoint"] = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    return {
        "backend": "fullload", "source_sha256": sha256(file_bytes),
        "source_suffix": Path(file_name).suffix.lower(), "pipeline_sha256": digest.hexdigest(),
        "settings_sha256": sha256(json.dumps(settings, sort_keys=True).encode()),
    }


def checkpoint_bytes(identity: dict, payload: dict, markdown_hashes: dict) -> bytes:
    specifications = [
        {**{key: spec[key] for key in ("step", "key", "title", "usage", "elapsed_ms")},
         "sha256": markdown_hashes[f'{spec["step"]:02d}_{spec["key"]}.md']}
        for spec in payload["specifications"]
    ]
    state = {
        "schema_version": SCHEMA_VERSION, "identity": identity,
        "file_name": payload["file_name"], "specifications": specifications,
        "resume": payload.get("resume"),
    }
    data = (json.dumps(state, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
    if len(data) > MAX_CHECKPOINT_BYTES:
        raise ValueError("Checkpoint exceeds the storage budget")
    return data


def _read_file(path: Path, maximum: int) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing or unsafe resume file: {path.name}")
    with path.open("rb") as stream:
        data = stream.read(maximum + 1)
    if len(data) > maximum:
        raise ValueError(f"Resume file exceeds the storage budget: {path.name}")
    return data


def _validate_usage(usage):
    if not isinstance(usage, dict) or set(usage) != set(USAGE_KEYS):
        raise ValueError("Invalid checkpoint usage")
    if any(value is not None and (type(value) is not int or value < 0) for value in usage.values()):
        raise ValueError("Invalid checkpoint usage")


def load_resume(root: Path, run_id: str, identity: dict, *, allow_legacy: bool = False) -> dict:
    """Read a snapshot only. The original run directory is never modified."""
    if not re.fullmatch(RUN_ID_PATTERN, run_id):
        raise HTTPException(status_code=400, detail="resume_from must be a fullload run ID, not a path")
    directory = root / run_id
    if directory.is_symlink() or directory.resolve().parent != root.resolve():
        raise HTTPException(status_code=400, detail="Unsafe resume directory")
    if not directory.is_dir():
        raise HTTPException(status_code=404, detail="Resume run not found")
    try:
        manifest = directory / CHECKPOINT_NAME
        legacy = not manifest.exists() and not manifest.is_symlink()
        if legacy:
            if not allow_legacy:
                raise HTTPException(status_code=409, detail=(
                    "This run has no checkpoint. To import its completed Markdown, explicitly set "
                    "allow_legacy_resume=true; original input and settings cannot be verified."
                ))
            state = {"file_name": None, "resume": None}
            records = []
            missing = False
            for stage in SPECIFICATION_STAGES:
                path = directory / f"{stage.step:02d}_{stage.key}.md"
                if not path.exists() and not path.is_symlink():
                    missing = True
                    continue
                if missing:
                    raise ValueError("Legacy specifications have a gap; a contiguous prefix from 01 is required")
                records.append({"step": stage.step, "key": stage.key, "title": stage.title,
                                "usage": dict.fromkeys(USAGE_KEYS), "elapsed_ms": None})
        else:
            state = json.loads(_read_file(manifest, MAX_CHECKPOINT_BYTES))
            if not isinstance(state, dict) or state.get("schema_version") != SCHEMA_VERSION:
                raise ValueError("Unsupported checkpoint schema")
            if state.get("identity") != identity:
                raise HTTPException(status_code=409, detail="Resume input, code, prompts, model or settings do not match the checkpoint")
            if not isinstance(state.get("file_name"), str) or not state["file_name"]:
                raise ValueError("Invalid checkpoint file name")
            records = state["specifications"]
        if not isinstance(records, list) or not 1 <= len(records) <= len(SPECIFICATION_STAGES):
            raise ValueError("No valid completed specifications in the resume run")
        specifications = []
        for stage, record in zip(SPECIFICATION_STAGES, records):
            if record["step"] != stage.step or type(record["step"]) is not int or record["key"] != stage.key:
                raise ValueError("Checkpoint specifications are not a contiguous prefix")
            name = f"{stage.step:02d}_{stage.key}.md"
            data = _read_file(directory / name, MAX_MARKDOWN_BYTES)
            if not legacy and sha256(data) != record["sha256"]:
                raise ValueError(f"Saved specification has changed: {name}")
            content = data.decode("utf-8").removesuffix("\n")
            if not content.strip():
                raise ValueError(f"Saved specification is empty: {name}")
            _validate_usage(record["usage"])
            elapsed = record["elapsed_ms"]
            if elapsed is not None and (type(elapsed) is not int or elapsed < 0):
                raise ValueError("Invalid checkpoint elapsed time")
            specifications.append({"step": stage.step, "key": stage.key, "title": stage.title,
                                   "content": content, "usage": record["usage"], "elapsed_ms": elapsed})
        completed_prefix(specifications)
        prior_resume = state.get("resume")
        if prior_resume is None:
            prior_resume = {}
        if not isinstance(prior_resume, dict):
            raise ValueError("Invalid checkpoint resume history")
        unverified = ([spec["key"] for spec in specifications] if legacy
                      else prior_resume.get("unverified_stages", []))
        if not isinstance(unverified, list) or not set(unverified) <= {spec["key"] for spec in specifications}:
            raise ValueError("Invalid checkpoint import history")
        history = prior_resume.get("history", [])
        if not isinstance(history, list) or any(
            not isinstance(item, str) or not re.fullmatch(RUN_ID_PATTERN, item) for item in history
        ):
            raise ValueError("Invalid checkpoint resume history")
        return {
            "file_name": state["file_name"], "specifications": specifications,
            "resume": {"source_run_id": run_id, "reused_stages": [spec["key"] for spec in specifications],
                       "unverified_stages": unverified, "history": [*history, run_id]},
        }
    except HTTPException:
        raise
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid resume data: {exc}") from exc
