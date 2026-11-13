import asyncio
import logging
import time
from asyncio import sleep
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from server.utils import merge_usage


logger = logging.getLogger(__name__)
PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompt"
STAGE_INTERVAL_SECONDS = 240


@dataclass(frozen=True)
class SpecificationStage:
    step: int
    key: str
    title: str
    english_title: str

    @property
    def prompt_template(self) -> str:
        return f"stages/{self.key}.jinja2"


SPECIFICATION_STAGES = (
    SpecificationStage(1, "screen_functions", "Screen Function Specification", "Screen Function Specification"),
    SpecificationStage(2, "api", "API Specification", "API Specification"),
    SpecificationStage(3, "data", "Data Specification", "Data Specification"),
    SpecificationStage(4, "batch_functions", "Batch Function Specification", "Batch Function Specification"),
    SpecificationStage(5, "business_rules", "Business Rules", "Business Rules"),
    SpecificationStage(6, "exception_handling", "Exception Handling Specification", "Exception Handling Specification"),
    SpecificationStage(7, "processing_flows", "Processing Flow Specification", "Processing Flow Specification"),
    SpecificationStage(8, "architecture_decision", "Architecture Decision Register", "Architecture Decision Register"),
)

StageCompleted = Callable[[dict[str, Any]], Awaitable[None]]


def specification_result(specifications: list[dict]) -> dict[str, Any]:
    return {
        "reply": "\n\n---\n\n".join(spec["content"] for spec in specifications),
        "specifications": list(specifications),
        "usage": merge_usage(*(spec["usage"] for spec in specifications)),
    }


def completed_prefix(previous: list[dict] | None) -> list[dict]:
    """Validate stage order before a resumed run can issue any model requests."""
    specifications = list(previous or [])
    if len(specifications) > len(SPECIFICATION_STAGES):
        raise ValueError("Too many completed specifications")
    for stage, spec in zip(SPECIFICATION_STAGES, specifications):
        if (spec.get("step") != stage.step or type(spec.get("step")) is not int
                or spec.get("key") != stage.key
                or not isinstance(spec.get("content"), str) or not spec["content"].strip()):
            raise ValueError("Completed specifications must be a nonempty contiguous prefix starting at stage 01")
    return specifications


def prompt_environment() -> Environment:
    return Environment(loader=FileSystemLoader(str(PROMPT_DIR)), undefined=StrictUndefined)


def stage_context(stage: SpecificationStage, file_name: str, previous: list[dict]) -> dict:
    return {
        "stage": stage,
        "total_stages": len(SPECIFICATION_STAGES),
        "file_name": file_name,
        "previous_specifications": previous,
    }


def log_specification_query(
    stage: SpecificationStage,
    file_name: str,
    query: str,
    phase: str,
    chunk_index: int | None = None,
) -> None:
    logger.info(
        'Specification LLM query submitting: file_name=%s step=%d/%d stage=%s '
        'specification="%s" prompt=%s phase=%s chunk=%s query_chars=%d',
        file_name, stage.step, len(SPECIFICATION_STAGES), stage.key,
        stage.english_title, stage.prompt_template, phase,
        chunk_index if chunk_index is not None else "none", len(query),
    )


async def generate_stages(
    file_name: str,
    generate_stage: Callable[[SpecificationStage, list[dict]], Awaitable[tuple[str, dict]]],
    *,
    on_stage_completed: StageCompleted | None = None,
    previous_specifications: list[dict] | None = None,
) -> dict[str, Any]:
    specifications = completed_prefix(previous_specifications)
    for stage in SPECIFICATION_STAGES[len(specifications):]:
        started = time.perf_counter()
        logger.info(
            'Specification stage started: file_name=%s step=%d/%d stage=%s '
            'specification="%s" prompt=%s previous_stages=%d',
            file_name, stage.step, len(SPECIFICATION_STAGES), stage.key,
            stage.english_title, stage.prompt_template, len(specifications),
        )
        try:
            body, usage = await generate_stage(stage, specifications)
            if not body.strip():
                raise RuntimeError(f"Empty specification output for stage {stage.key}")
            elapsed_ms = max(0, int((time.perf_counter() - started) * 1000))
            specifications.append({
                "step": stage.step,
                "key": stage.key,
                "title": stage.title,
                "content": f"# {stage.step}. {stage.title}\n\n{body.strip()}",
                "usage": usage,
                "elapsed_ms": elapsed_ms,
            })
            if on_stage_completed is not None:
                await on_stage_completed(specification_result(specifications))
        except asyncio.CancelledError:
            logger.warning(
                'Specification stage cancelled: file_name=%s step=%d/%d stage=%s specification="%s" prompt=%s',
                file_name, stage.step, len(SPECIFICATION_STAGES), stage.key, stage.english_title, stage.prompt_template,
            )
            raise
        except Exception:
            logger.exception(
                'Specification stage failed: file_name=%s step=%d/%d stage=%s specification="%s" prompt=%s',
                file_name, stage.step, len(SPECIFICATION_STAGES), stage.key, stage.english_title, stage.prompt_template,
            )
            raise
        logger.info(
            'Specification stage completed: file_name=%s step=%d/%d stage=%s specification="%s" prompt=%s elapsed_ms=%d '
            "input_tokens=%s output_tokens=%s total_tokens=%s",
            file_name, stage.step, len(SPECIFICATION_STAGES), stage.key, stage.english_title, stage.prompt_template, elapsed_ms,
            usage["input_tokens"], usage["output_tokens"], usage["total_tokens"],
        )
        if len(specifications) < len(SPECIFICATION_STAGES):
            logger.info(
                "Specification stage interval: file_name=%s completed=%d/%d wait_seconds=%d",
                file_name, len(specifications), len(SPECIFICATION_STAGES), STAGE_INTERVAL_SECONDS,
            )
            await sleep(STAGE_INTERVAL_SECONDS)
    return specification_result(specifications)
