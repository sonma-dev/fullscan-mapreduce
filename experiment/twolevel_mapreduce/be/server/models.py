import asyncio
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AppServices:
    responses: Any
    # Binary chunks and their audit records stay in memory for an entire upload.
    # Admit one analysis per server process; leaf calls still run in parallel.
    analysis_slot: asyncio.Semaphore = field(default_factory=lambda: asyncio.Semaphore(1))
