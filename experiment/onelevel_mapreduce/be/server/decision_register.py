"""Generate the TBD register from completed Markdown specifications only."""

from server.models import AppServices
from server.specifications import (
    SpecificationStage, log_specification_query, prompt_environment, stage_context,
)
from server.utils import env_int, extract_response_text, response_usage


async def generate_decision_register(
    services: AppServices, stage: SpecificationStage, file_name: str, previous: list[dict],
) -> tuple[str, dict]:
    env = prompt_environment()
    system = env.get_template("decision_register_system.jinja2").render()
    query = env.get_template(stage.prompt_template).render(**stage_context(stage, file_name, previous))
    query_bytes = env_int("LLM_MAX_QUERY_BYTES", 8 * 1024 * 1024, 32 * 1024 * 1024)
    output_bytes = env_int("LLM_FINAL_MAX_BYTES", 1024 * 1024, 16 * 1024 * 1024)
    if len(query.encode("utf-8")) > query_bytes:
        raise RuntimeError("TBD query budget exceeded; completed specifications were not truncated")
    log_specification_query(stage, file_name, query, phase="decision_register")
    result = await services.responses.create_response(
        query=query, assistant_instruction=system, input_file=None,
        max_output_tokens=env_int("LLM_MAX_OUTPUT_TOKENS", 128000, 128000),
    )
    body = extract_response_text(result)
    if len(body.encode("utf-8")) > output_bytes:
        raise RuntimeError("TBD output exceeded the specification byte budget")
    return body, response_usage(result)
