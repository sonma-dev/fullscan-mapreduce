"""Persist completed Markdown specifications in the repository's res directory."""

import re
import shutil
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parents[4] / "res"
OUTPUT_PREFIX = "onelevel"
JST = timezone(timedelta(hours=9), "JST")


class OutputFiles:
    """One upload's output directory and stable JST timestamp, shared across stages."""

    def __init__(self):
        self.timestamp = datetime.now(JST).strftime("%Y%m%d%H%M%S")
        self.directory: Path | None = None
        self._saved_names: set[str] = set()

    def save(self, payload: dict, *, complete: bool = True, total_started_at: float | None = None) -> dict:
        markdown = []
        for specification in payload["specifications"]:
            step = specification["step"]
            key = specification["key"]
            if type(step) is not int or step < 1 or not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", key):
                raise ValueError("Invalid specification filename components")
            markdown.append((f"{step:02d}_{key}.md", specification["content"]))
        if len({name for name, _ in markdown}) != len(markdown):
            raise ValueError("Duplicate specification output filenames")

        if self.directory is None:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            # Unique across simultaneous requests and server processes.
            self.directory = Path(tempfile.mkdtemp(prefix=f"{OUTPUT_PREFIX}_{self.timestamp}_", dir=OUTPUT_DIR))
        directory = self.directory
        relative = Path(OUTPUT_DIR.name) / directory.name
        saved = {
            **payload,
            "status": "completed" if complete else "partial",
            "output_files": {
                "markdown": [(relative / name).as_posix() for name, _ in markdown],
            },
        }
        committed = []
        try:
            # Prepare all new Markdown files before committing them.
            # Previously completed Markdown files are immutable and stay in place.
            with tempfile.TemporaryDirectory(prefix=".pending_", dir=directory, ignore_cleanup_errors=True) as pending:
                pending = Path(pending)
                new_names = []
                for name, content in markdown:
                    if name not in self._saved_names:
                        (pending / name).write_text(content + "\n", encoding="utf-8")
                        new_names.append(name)
                if total_started_at is not None:
                    saved["timing_ms"] = {
                        **payload["timing_ms"],
                        "total": max(0, int((time.perf_counter() - total_started_at) * 1000)),
                    }
                for name in new_names:
                    (pending / name).replace(directory / name)
                    committed.append(name)
            self._saved_names.update(new_names)
        except BaseException:
            for name in committed:
                (directory / name).unlink(missing_ok=True)
            if not self._saved_names:
                shutil.rmtree(directory)
                self.directory = None
            raise
        return saved


def save_output_files(payload: dict, *, total_started_at: float | None = None) -> dict:
    return OutputFiles().save(payload, total_started_at=total_started_at)
