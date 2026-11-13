from typing import Any

from server.input_files import create_input_file
from server.decision_register import generate_decision_register
from server.models import AppServices
from server.specifications import (
    SPECIFICATION_STAGES, StageCompleted, completed_prefix, generate_stages,
    log_specification_query, prompt_environment, specification_result, stage_context,
)
from server.utils import env_int, extract_response_text, response_usage


async def generate_specifications(
    services: AppServices,
    file_bytes: bytes,
    file_name: str,
    *,
    on_stage_completed: StageCompleted | None = None,
    resume_state: dict | None = None,
) -> dict[str, Any]:
    previous = completed_prefix(resume_state["specifications"] if resume_state else None)
    if len(previous) == len(SPECIFICATION_STAGES):
        return specification_result(previous)
    env = prompt_environment()
    system = env.get_template("specification_system.jinja2").render()
    input_file = create_input_file(file_bytes, file_name) if len(previous) < 7 else None
    max_output_tokens = env_int("LLM_MAX_OUTPUT_TOKENS", 128000, 128000)

    async def generate_stage(stage, previous):
        if stage.key == "architecture_decision":
            return await generate_decision_register(services, stage, file_name, previous)
        query = env.get_template(stage.prompt_template).render(
            **stage_context(stage, file_name, previous),
        )
        log_specification_query(stage, file_name, query, phase="generation")
        result = await services.responses.create_response(
            query=query, assistant_instruction=system, input_file=input_file,
            max_output_tokens=max_output_tokens,
        )
        return extract_response_text(result), response_usage(result)

    return await generate_stages(
        file_name, generate_stage, on_stage_completed=on_stage_completed,
        previous_specifications=previous,
    )
