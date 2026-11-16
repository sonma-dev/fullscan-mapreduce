import asyncio
import copy
import json
import logging
from typing import Any

from server.approval import ApprovalCoverageError, ApprovalError, approval_record, encode, require
from server.input_files import create_input_file, source_manifest
from server.decision_register import generate_decision_register
from server.models import AppServices
from server.specifications import StageCompleted, generate_stages, log_specification_query, prompt_environment, stage_context
from server.utils import env_int, extract_response_text, merge_usage, response_usage


logger = logging.getLogger(__name__)


async def generate_specifications(
    services: AppServices,
    file_bytes: bytes,
    file_name: str,
    *,
    on_stage_completed: StageCompleted | None = None,
) -> dict[str, Any]:
    env = prompt_environment()
    system = env.get_template("specification_system.jinja2").render()
    approval_system = env.get_template("approval_system.jinja2").render()
    input_file = create_input_file(file_bytes, file_name)
    source = await asyncio.to_thread(source_manifest, file_bytes, file_name)
    max_output_tokens = env_int("LLM_MAX_OUTPUT_TOKENS", 128000, 128000)
    approval_tokens = env_int("LLM_INTERMEDIATE_MAX_OUTPUT_TOKENS", 64000, 128000)
    max_attempts = env_int("LLM_MAX_APPROVAL_ATTEMPTS", 8, 8)
    max_reviews = env_int("LLM_MAX_APPROVAL_REVIEW_ATTEMPTS", 3, 5)
    query_bytes = env_int("LLM_MAX_QUERY_BYTES", 8 * 1024 * 1024, 32 * 1024 * 1024)
    output_bytes = env_int("LLM_FINAL_MAX_BYTES", 1024 * 1024, 16 * 1024 * 1024)
    review_bytes = env_int("LLM_INTERMEDIATE_MAX_BYTES", 1024 * 1024, 16 * 1024 * 1024)
    audit_bytes = env_int("LLM_AUDIT_MAX_BYTES", 16 * 1024 * 1024, 64 * 1024 * 1024)
    audit = {"source": source, "stages": []}

    def check_audit():
        require(len(encode(audit).encode("utf-8")) <= audit_bytes,
                "Approval audit budget exceeded; analysis stopped without truncation")

    check_audit()

    async def call(stage, previous, phase, payload, usage):
        template = env.get_template(stage.prompt_template)
        context = stage_context(stage, file_name, previous)
        if phase == "approval":
            # Reuse the stage requirements without generation instructions.
            requirements = "".join(template.blocks["requirements"](template.new_context(context)))
            query = env.get_template("specification_approval_user.jinja2").render(
                **context, requirements=requirements, payload=encode(payload),
            )
        else:
            # Match fullload's initial generation prompt exactly.
            query = template.render(**context)
            if payload["feedback"]:
                query += "\n\n" + env.get_template("specification_revision.jinja2").render(
                    feedback=encode(payload["feedback"]),
                )
        require(len(query.encode("utf-8")) <= query_bytes,
                "LLM query budget exceeded; specifications were not truncated")
        log_specification_query(stage, file_name, query, phase=phase)
        result = await services.responses.create_response(
            query=query, assistant_instruction=approval_system if phase == "approval" else system,
            input_file=input_file,
            max_output_tokens=approval_tokens if phase == "approval" else max_output_tokens,
            json_output=phase == "approval",
        )
        usage.append(response_usage(result))
        text = extract_response_text(result)
        limit = review_bytes if phase == "approval" else output_bytes
        require(len(text.encode("utf-8")) <= limit, "Model output exceeded the specification or approval byte budget")
        return text

    async def generate_stage(stage, previous):
        if stage.key == "architecture_decision":
            return await generate_decision_register(services, stage, file_name, previous)
        usage = []
        attempts = []
        audit["stages"].append({"key": stage.key, "attempts": attempts})
        feedback = []
        for attempt in range(1, max_attempts + 1):
            shared = {"source": source, "attempt": attempt, "feedback": feedback}
            candidate = await call(stage, previous, "generation", shared, usage)
            require(bool(candidate.strip()), f"Empty specification output for stage {stage.key}")
            record = {"attempt": attempt, "candidate": candidate, "approval": None,
                      "approval_review_failures": []}
            attempts.append(record)
            check_audit()
            coverage_feedback = None
            for review_attempt in range(1, max_reviews + 1):
                payload = {**shared, "candidate": candidate,
                           "required_review": {"source_unit_ids": source["source_unit_ids"]},
                           "review_attempt": review_attempt, "coverage_feedback": coverage_feedback}
                text = await call(stage, previous, "approval", payload, usage)
                try:
                    review = json.loads(text)
                except ValueError as exc:
                    raise ApprovalError("Model returned invalid approval JSON") from exc
                try:
                    review = approval_record(review, source["source_unit_ids"])
                except ApprovalCoverageError as exc:
                    record["approval_review_failures"].append({
                        "review_attempt": review_attempt, "coverage": exc.coverage, "response": exc.review,
                    })
                    check_audit()
                    logger.warning(
                        "Full-file approval coverage invalid: file_name=%s stage=%s attempt=%d "
                        "review_attempt=%d/%d reviewed_units=%d/%d missing_ids_sample=%s "
                        "duplicate_ids_sample=%s unknown_ids_sample=%s review_exhausted=%s",
                        file_name, stage.key, attempt, review_attempt, max_reviews,
                        exc.coverage["reviewed_source_unit_count"], exc.coverage["expected_source_unit_count"],
                        exc.coverage["missing_source_unit_ids"][:20],
                        exc.coverage["duplicate_source_unit_ids"][:20],
                        exc.coverage["unknown_source_unit_ids"][:20], review_attempt == max_reviews,
                    )
                    if review_attempt == max_reviews:
                        raise ApprovalError(f"Full-file approval coverage failed after {max_reviews} review attempts: {exc}") from exc
                    coverage_feedback = {**exc.coverage, "previous_review": exc.review}
                    continue
                record["approval"] = review
                check_audit()
                break
            logger.info(
                "Full-file approval decision: file_name=%s stage=%s attempt=%d approved=%s feedback_items=%d",
                file_name, stage.key, attempt, review["approved"], len(review["feedback"]),
            )
            if review["approved"]:
                return candidate, merge_usage(*usage)
            feedback = review["feedback"]
            logger.warning(
                "Full-file rejected candidate: file_name=%s stage=%s attempt=%d/%d "
                "rationale=%s feedback=%s",
                file_name, stage.key, attempt, max_attempts,
                json.dumps(review["rationale"], ensure_ascii=True), json.dumps(feedback, ensure_ascii=True),
            )
        raise ApprovalError(f"Full-file reviewer rejected {stage.key} after {max_attempts} full-file attempts")

    def with_audit(result):
        return {**result, "approval_audit": copy.deepcopy(audit)}

    async def save_stage(result):
        await on_stage_completed(with_audit(result))

    result = await generate_stages(
        file_name, generate_stage, on_stage_completed=save_stage if on_stage_completed is not None else None,
    )
    return with_audit(result)
