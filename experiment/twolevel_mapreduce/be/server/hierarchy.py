"""Full-scan semantic MapReduce with evidence retention and root approval."""

import asyncio
import copy
import json
import logging
import os
import time

from server.evidence import (
    ApprovalCoverageError, DecisionIdentifierError, EVIDENCE_STRENGTHS, EvidenceError, MapStrengthError, RelationCardinalityError,
    adjudication_record, approval_record, context_record, encode,
    map_record, plan_record, require,
)
from server.file_chunks import split_file
from server.chapter_reduction import reduce_chapter
from server.concurrency import level_concurrency_limits
from server.pdf_sections import estimate_tokens
from server.input_files import create_input_file, validate_file
from server.decision_register import generate_decision_register
from server.specifications import SPECIFICATION_STAGES, StageCompleted, completed_prefix, generate_stages, log_specification_query, prompt_environment, stage_context
from server.utils import env_int, extract_response_text, merge_usage, response_usage


logger = logging.getLogger(__name__)
MAP_REQUEST_TIMEOUT_SECONDS = 300
MAP_MAX_RETRIES = 3
MAP_STRENGTH_MAX_ATTEMPTS = 3
ADJUDICATION_MAX_ATTEMPTS = 3


async def parallel(items, operation):
    # Cancel and await siblings on any failure; never reduce a partial scan.
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(operation(item)) for item in items]
    return [task.result() for task in tasks]


def chunk_metadata(chunk):
    return {"index": chunk.index, "title": chunk.title, "file_name": chunk.file_name,
            "start": chunk.start, "end": chunk.end, "unit": chunk.unit,
            "section": chunk.section, "section_id": chunk.section_id, "headings": list(chunk.headings),
            "chapter": chunk.chapter, "chapter_id": chunk.chapter_id, "part": chunk.part,
            "source_regions": list(chunk.source_regions), "estimated_tokens": chunk.estimated_tokens,
            "continuation_context": list(chunk.continuation_context)}


async def run_hierarchy(
    services, file_bytes, file_name, *, reduce_levels, on_stage_completed: StageCompleted | None = None,
    resume_state: dict | None = None,
):
    require(reduce_levels in (1, 2), "Supported reduce depths are one and two")
    resume_state = copy.deepcopy(resume_state or {})
    previous = completed_prefix(resume_state.get("specifications"))
    restored = resume_state.get("hierarchy") or {}
    # Stage 08 depends only on completed Markdown. Do not split the source,
    # regenerate context or issue any hierarchy calls when only 08 remains.
    if len(previous) >= 7:
        async def decision_stage(stage, completed):
            return await generate_decision_register(services, stage, file_name, completed)

        def finish(result):
            return {**result, "usage": merge_usage(result["usage"], restored.get("context_usage", {})),
                    "chunks": resume_state.get("chunks", []),
                    "hierarchy": restored or {"reduce_levels": reduce_levels, "global_context": None,
                                               "context_usage": dict.fromkeys(("input_tokens", "output_tokens", "total_tokens")),
                                               "stages": []}}

        async def save_decision(result):
            await on_stage_completed(finish(result))

        return finish(await generate_stages(
            file_name, decision_stage, previous_specifications=previous,
            on_stage_completed=save_decision if on_stage_completed else None,
        ))
    chunks = await asyncio.to_thread(
        split_file, file_bytes, file_name,
        max_pages=env_int("FILE_CHUNK_MAX_PAGES", 8, 100),
        max_slides=env_int("FILE_CHUNK_MAX_SLIDES", 8, 100),
    )
    for chunk in chunks:
        validate_file(chunk.data, chunk.file_name)
    metadata = [chunk_metadata(chunk) for chunk in chunks]
    if restored.get("global_context"):
        require(metadata == resume_state.get("chunks"), "Resume chunk layout differs from the checkpoint")
    level1_parallel, level2_parallel = level_concurrency_limits()
    level1_slots = asyncio.Semaphore(level1_parallel)
    level2_slots = asyncio.Semaphore(level2_parallel)
    root_slots = asyncio.Semaphore(1)
    max_attempts = env_int("LLM_MAX_APPROVAL_ATTEMPTS", 8, 8)
    max_review_attempts = env_int("LLM_MAX_APPROVAL_REVIEW_ATTEMPTS", 3, 5)
    intermediate_bytes = env_int("LLM_INTERMEDIATE_MAX_BYTES", 1024 * 1024, 16 * 1024 * 1024)
    query_bytes = env_int("LLM_MAX_QUERY_BYTES", 8 * 1024 * 1024, 32 * 1024 * 1024)
    audit_bytes = env_int("LLM_AUDIT_MAX_BYTES", 16 * 1024 * 1024, 64 * 1024 * 1024)
    intermediate_tokens = env_int("LLM_INTERMEDIATE_MAX_OUTPUT_TOKENS", 64000, 128000)
    final_tokens = env_int("LLM_MAX_OUTPUT_TOKENS", 128000, 128000)
    final_bytes = env_int("LLM_FINAL_MAX_BYTES", 1024 * 1024, 16 * 1024 * 1024)
    chapter_batch_bytes = env_int("LLM_CHAPTER_BATCH_MAX_BYTES", 128 * 1024, query_bytes)
    chapter_rounds = env_int("LLM_MAX_CHAPTER_REDUCE_ROUNDS", 8, 16)
    # Deployments have different context windows. Optional token estimates must
    # be configured with room for the requested output; the byte ceiling always applies.
    chapter_input_tokens = env_int("LLM_CHAPTER_INPUT_TOKEN_BUDGET", 128000, 1000000) if os.getenv("LLM_CHAPTER_INPUT_TOKEN_BUDGET", "").strip() else None
    map_input_tokens = env_int("LLM_MAP_INPUT_TOKEN_BUDGET", 128000, 1000000) if os.getenv("LLM_MAP_INPUT_TOKEN_BUDGET", "").strip() else None
    # Binary byte size is only an operational proxy for the paper's size bound.
    map_budget = min(intermediate_bytes, (sum(len(chunk.data) for chunk in chunks) - 1) // len(chunks))
    env = prompt_environment()
    system = env.get_template("hierarchy_system.jinja2").render()
    specification_rules = env.get_template("specification_system.jinja2").render()
    context_usage = [restored["context_usage"]] if restored.get("global_context") else []
    stage_audits = list(restored.get("stages", []))
    stored_bytes = 0

    def retain(value):
        nonlocal stored_bytes
        size = len(encode(value).encode("utf-8"))
        require(stored_bytes + size <= audit_bytes, "Evidence storage budget exceeded; analysis stopped without truncation")
        stored_bytes += size
        return value

    def render_query(phase, payload, stage, previous, limit):
        template_context = dict(phase=phase, payload=encode(payload), output_budget=limit)
        if stage is None:
            template = env.get_template("document_context.jinja2")
            query = template.render(file_name=file_name, **template_context)
        else:
            template = env.get_template(stage.prompt_template)
            query = template.render(**stage_context(stage, file_name, previous), **template_context)
        return query

    async def call(phase, payload, validator, usage, *, stage=None, previous=(),
                   attempt=0, node="root", chunk=None, limit=None, file_data=None, request_attempt=1):
        limit = intermediate_bytes if limit is None else limit
        query = render_query(phase, payload, stage, previous, limit)
        require(len(query.encode("utf-8")) <= query_bytes, "LLM query budget exceeded; analysis stopped without truncation")
        if phase == "map" and map_input_tokens is not None:
            require(estimate_tokens(system + specification_rules + query) + chunk.estimated_tokens <= map_input_tokens,
                    "Map input estimate exceeds LLM_MAP_INPUT_TOKEN_BUDGET including prompts and previous specifications")
        if phase == "onelevel_reduce" and chapter_input_tokens is not None:
            require(estimate_tokens(system + specification_rules + query) <= chapter_input_tokens,
                    "Chapter input estimate exceeds LLM_CHAPTER_INPUT_TOKEN_BUDGET including repair feedback")
        slots = (level2_slots if phase == "map" else
                 level1_slots if phase in ("onelevel_context", "onelevel_reduce") else root_slots)
        async with slots:
            if stage is not None:
                log_specification_query(stage, file_name, query, phase, chunk.index if chunk else None)
            logger.info(
                'Hierarchy query started: file_name=%s stage=%s specification="%s" phase=%s node=%s attempt=%d reduce_levels=%d output_budget_bytes=%d request_attempt=%d',
                file_name, stage.key if stage else "document_context",
                stage.english_title if stage else "Document Global Context", phase, node, attempt, reduce_levels, limit, request_attempt,
            )
            started = time.perf_counter()
            try:
                # Only leaf Map requests get this deadline, after acquiring a slot.
                # Root/fork aggregation uses the Responses client's 1200-second limit.
                async with asyncio.timeout(MAP_REQUEST_TIMEOUT_SECONDS if phase == "map" else None):
                    response = await services.responses.create_response(
                        query=query, assistant_instruction=system + "\n" + specification_rules,
                        input_file=create_input_file(*file_data) if file_data else None,
                        max_output_tokens=final_tokens if phase == "root_reduce" else intermediate_tokens,
                        json_output=True,
                    )
                tokens = response_usage(response)
                usage.append(tokens)
                text = extract_response_text(response)
                require(len(text.encode("utf-8")) <= limit, "Model output exceeded the evidence byte budget")
                try:
                    value = json.loads(text)
                except ValueError as exc:
                    raise EvidenceError("Model returned invalid evidence JSON") from exc
                value = validator(value)
                require(len(encode(value).encode("utf-8")) <= limit, "Validated evidence exceeded the byte budget")
                retain(value)
            except asyncio.CancelledError:
                logger.warning("Hierarchy query cancelled: file_name=%s phase=%s node=%s attempt=%d", file_name, phase, node, attempt)
                raise
            except (ApprovalCoverageError, DecisionIdentifierError, MapStrengthError, RelationCardinalityError):
                # Dedicated loops retain validation diagnostics and repair the affected call.
                raise
            except Exception:
                logger.error("Hierarchy query failed: file_name=%s phase=%s node=%s attempt=%d", file_name, phase, node, attempt)
                raise
            logger.info(
                "Hierarchy query completed: file_name=%s phase=%s node=%s attempt=%d elapsed_ms=%d "
                "input_tokens=%s output_tokens=%s total_tokens=%s result_bytes=%d",
                file_name, phase, node, attempt, int((time.perf_counter() - started) * 1000),
                tokens["input_tokens"], tokens["output_tokens"], tokens["total_tokens"], len(text.encode("utf-8")),
            )
            return value

    async def reduce_with_repair(phase, payload, finding_ids, usage, failures, *,
                                 stage, previous, attempt, node="root", limit=None):
        repair = {}
        for reduction_attempt in range(1, ADJUDICATION_MAX_ATTEMPTS + 1):
            request = {**payload, **repair}
            try:
                return await call(
                    phase, request,
                    lambda value: adjudication_record(value, finding_ids, candidate=phase == "root_reduce"),
                    usage, stage=stage, previous=previous, attempt=attempt, node=node, limit=limit,
                    request_attempt=reduction_attempt,
                )
            except (DecisionIdentifierError, RelationCardinalityError) as exc:
                identifier_error = isinstance(exc, DecisionIdentifierError)
                failures.append(retain({
                    "phase": phase, "node": node, "request_attempt": reduction_attempt,
                    "aggregation": payload.get("aggregation"), "issues": exc.issues, "response": exc.outcome,
                    **({"missing_finding_ids": exc.missing_finding_ids} if identifier_error else {}),
                }))
                exhausted = reduction_attempt == ADJUDICATION_MAX_ATTEMPTS
                if identifier_error:
                    logger.warning(
                        "Adjudication decision identifier validation failed: file_name=%s stage=%s phase=%s node=%s "
                        "attempt=%d reduction_attempt=%d/%d invalid_decisions=%d "
                        "issues_sample=%s missing_finding_ids_sample=%s repair_exhausted=%s",
                        file_name, stage.key, phase, node, attempt, reduction_attempt, ADJUDICATION_MAX_ATTEMPTS,
                        len(exc.issues), json.dumps(exc.issues, ensure_ascii=True)[:2000],
                        json.dumps(exc.missing_finding_ids[:20], ensure_ascii=True)[:2000], exhausted,
                    )
                else:
                    logger.warning(
                        "Adjudication relation validation failed: file_name=%s stage=%s phase=%s node=%s "
                        "attempt=%d reduction_attempt=%d/%d invalid_relations=%d "
                        "relation_indices=%s repair_exhausted=%s",
                        file_name, stage.key, phase, node, attempt, reduction_attempt, ADJUDICATION_MAX_ATTEMPTS,
                        len(exc.issues), [issue["relation_index"] for issue in exc.issues], exhausted,
                    )
                if exhausted:
                    kind = "decision identifier" if identifier_error else "relation"
                    raise EvidenceError(
                        f"Adjudication {kind} validation failed after {ADJUDICATION_MAX_ATTEMPTS} attempts: "
                        f"phase={phase} node={node}: {exc}"
                    ) from exc
                # Keep the original children and evidence. Send only the latest
                # malformed records as feedback, rather than nesting full outputs.
                field = "decision" if identifier_error else "relation"
                feedback = {
                    "allowed_finding_ids": sorted(finding_ids),
                    f"invalid_{field}s": [
                        {**issue, field: exc.outcome[f"{field}s"][issue[f"{field}_index"]]}
                        for issue in exc.issues
                    ],
                }
                if identifier_error:
                    feedback["missing_finding_ids"] = exc.missing_finding_ids
                repair = {"decision_identifier_repair" if identifier_error else "relation_repair": feedback}

    logger.info(
        "Full scan started: file_name=%s chunks=%d reduce_levels=%d level1_max_parallel=%d level2_max_parallel=%d",
        file_name, len(chunks), reduce_levels, level1_parallel, level2_parallel,
    )
    if restored.get("global_context"):
        plan = plan_record(restored["global_context"], chunks)
        retain(plan)
        for audit in stage_audits:
            retain(audit)
        logger.info("Resume global context restored: file_name=%s completed_stages=%d", file_name, len(previous))
    else:
        plan = await call("global_context", {"chunks": metadata}, lambda value: plan_record(value, chunks), context_usage,
                          file_data=(file_bytes, file_name))
    groups = plan["groups"]

    async def generate_stage(stage, previous):
        if stage.key == "architecture_decision":
            return await generate_decision_register(services, stage, file_name, previous)
        usage = []
        attempts = []
        feedback = []
        for attempt in range(1, max_attempts + 1):
            map_failures = []
            reduction_failures = []
            shared = {"global_context": plan["global_context"], "feedback": feedback,
                      "attempt": attempt, "chunks": metadata}
            root_context = await call("root_context", shared, context_record, usage, stage=stage,
                                      previous=previous, attempt=attempt)
            shared["root_context"] = root_context
            scopes = {}
            if reduce_levels == 2:
                async def prepare_scope(group):
                    return await call("onelevel_context", {**shared, "jurisdiction": group}, context_record, usage,
                                      stage=stage, previous=previous, attempt=attempt, node=group["id"])
                values = await parallel(groups, prepare_scope)
                scopes = dict(zip((group["id"] for group in groups), values))
            owners = {index: group for group in groups for index in group["chunk_ids"]}
            completed_chunks = 0

            async def scan(chunk):
                nonlocal completed_chunks
                owner = owners[chunk.index]
                payload = {**shared, "chunk": chunk_metadata(chunk), "jurisdiction": owner,
                           "subglobal_context": scopes.get(owner["id"], root_context)}
                request_attempt = timeout_failures = 0
                strength_attempt = 1
                repair = None
                while True:
                    request_attempt += 1
                    request = payload if repair is None else {**payload, "strength_repair": repair}
                    try:
                        value = await call(
                            "map", request, lambda value: map_record(value, chunk, stage.key, attempt), usage,
                            stage=stage, previous=previous, attempt=attempt, node=f"chunk-{chunk.index}",
                            chunk=chunk, limit=map_budget, file_data=(chunk.data, chunk.file_name),
                            request_attempt=request_attempt,
                        )
                    except TimeoutError:
                        # A timed-out remote request may have consumed unreported tokens.
                        usage.append(response_usage(None))
                        timeout_failures += 1
                        if timeout_failures > MAP_MAX_RETRIES:
                            logger.error(
                                "Map retries exhausted: file_name=%s step=%d/%d stage=%s attempt=%d "
                                "chunk=%d timeout_s=%s requests=%d",
                                file_name, stage.step, len(SPECIFICATION_STAGES), stage.key, attempt, chunk.index,
                                MAP_REQUEST_TIMEOUT_SECONDS, request_attempt,
                            )
                            raise
                        logger.warning(
                            "Map request timed out: file_name=%s step=%d/%d stage=%s attempt=%d "
                            "chunk=%d timeout_s=%s retry=%d/%d",
                            file_name, stage.step, len(SPECIFICATION_STAGES), stage.key, attempt, chunk.index,
                            MAP_REQUEST_TIMEOUT_SECONDS, timeout_failures, MAP_MAX_RETRIES,
                        )
                        # call() released its slot, so queued chunks can run before this retry.
                        continue
                    except MapStrengthError as exc:
                        logger.warning(
                            "Map strength validation failed: file_name=%s stage=%s attempt=%d chunk=%d "
                            "request_attempt=%d strength_attempt=%d/%d invalid_findings=%d "
                            "issues_sample=%s repair_exhausted=%s",
                            file_name, stage.key, attempt, chunk.index, request_attempt,
                            strength_attempt, MAP_STRENGTH_MAX_ATTEMPTS, len(exc.issues),
                            json.dumps(exc.issues, ensure_ascii=True)[:2000],
                            strength_attempt == MAP_STRENGTH_MAX_ATTEMPTS,
                        )
                        map_failures.append(retain({
                            "chunk_id": chunk.index, "request_attempt": request_attempt,
                            "strength_attempt": strength_attempt, "issues": exc.issues, "response": exc.outcome,
                        }))
                        if strength_attempt == MAP_STRENGTH_MAX_ATTEMPTS:
                            raise EvidenceError(
                                f"Map strength validation failed after {MAP_STRENGTH_MAX_ATTEMPTS} attempts: "
                                f"chunk={chunk.index}: {exc}"
                            ) from exc
                        # Reuse the original attachment and context. Only the latest
                        # malformed findings are feedback; never coerce their meaning.
                        repair = {
                            "allowed_strengths": list(EVIDENCE_STRENGTHS),
                            "invalid_findings": [
                                {**issue, "finding": exc.outcome["findings"][issue["finding_index"]]}
                                for issue in exc.issues
                            ],
                        }
                        strength_attempt += 1
                        continue
                    completed_chunks += 1
                    logger.info(
                        "Map completed %d/%d: file_name=%s step=%d/%d stage=%s attempt=%d "
                        "chunk=%d request_attempt=%d",
                        completed_chunks, len(chunks), file_name, stage.step, len(SPECIFICATION_STAGES), stage.key,
                        attempt, chunk.index, request_attempt,
                    )
                    return value

            if reduce_levels == 2:
                async def adjudicate(group):
                    # Only this chapter's complete, validated scans are needed.
                    # Await in source order even when Maps finish out of order.
                    children = [await map_tasks[index] for index in group["chunk_ids"]]
                    payload_base = {**shared, "jurisdiction": group, "subglobal_context": scopes[group["id"]]}

                    def fits(payload):
                        query = render_query("onelevel_reduce", payload, stage, previous, intermediate_bytes)
                        return (len(query.encode("utf-8")) <= query_bytes
                                and (chapter_input_tokens is None or estimate_tokens(system + specification_rules + query) <= chapter_input_tokens))

                    async def invoke(payload, identifiers, compact):
                        limit = min(intermediate_bytes, len(encode(payload).encode("utf-8")) - 1)
                        if compact:
                            limit = min(limit, max(1, chapter_batch_bytes // 3))
                        aggregation = payload.get("aggregation")
                        if aggregation:
                            logger.info("Chapter aggregation: file_name=%s stage=%s chapter=%s mode=%s round=%d batch=%d findings=%d",
                                        file_name, stage.key, group["id"], aggregation["mode"], aggregation["round"], aggregation["batch"], len(identifiers))
                        return await reduce_with_repair("onelevel_reduce", payload, identifiers, usage, reduction_failures,
                                          stage=stage, previous=previous, attempt=attempt, node=group["id"], limit=limit)

                    outcome, batches = await reduce_chapter(
                        children, payload_base=payload_base, fits=fits, invoke=invoke,
                        batch_bytes=chapter_batch_bytes, max_rounds=chapter_rounds,
                    )
                    return {"node": group["id"], "jurisdiction": group, "outcome": outcome, **({"aggregation_calls": batches} if batches else {})}
            # Keep all Maps and chapter reductions in one cancellation scope.
            # Chapters can reduce while other chapters are still scanning, but
            # Root must wait for every Map and chapter reduction to succeed.
            async with asyncio.TaskGroup() as work:
                map_tasks = {chunk.index: work.create_task(scan(chunk)) for chunk in chunks}
                node_tasks = [work.create_task(adjudicate(group)) for group in groups] if reduce_levels == 2 else []
                scans = [await task for task in map_tasks.values()]
                # Retain the full leaf ledger for independent approval, in the
                # same source order regardless of chapter completion order.
                ledger = {finding["id"]: {**finding, "chunk_id": scan["chunk_id"],
                          "source_file": file_name, "unit_kind": chunks[scan["chunk_id"] - 1].unit,
                          "chapter_id": chunks[scan["chunk_id"] - 1].chapter_id,
                          "section_id": chunks[scan["chunk_id"] - 1].section_id,
                          "part": chunks[scan["chunk_id"] - 1].part}
                          for scan in scans for finding in scan["findings"]}
                logger.info(
                    "Full scan coverage verified: file_name=%s stage=%s attempt=%d covered_chunks=%d/%d findings=%d",
                    file_name, stage.key, attempt, len(scans), len(chunks), len(ledger),
                )
            nodes = [task.result() for task in node_tasks]
            # Intermediate calls stay in the saved audit, not in every root prompt.
            root_nodes = [{key: value for key, value in node.items() if key != "aggregation_calls"} for node in nodes]
            sources = {key: {"source_file": item["source_file"], "unit_kind": item["unit_kind"],
                            "units": sorted({source["unit"] for source in item["sources"]}),
                            "chapter_id": item["chapter_id"], "section_id": item["section_id"], "part": item["part"],
                            "regions": [source.get("region") for source in item["sources"]]}
                       for key, item in ledger.items()}
            candidate = await reduce_with_repair(
                "root_reduce", {**shared, "children": root_nodes if reduce_levels == 2 else scans, "source_index": sources},
                set(ledger), usage, reduction_failures,
                stage=stage, previous=previous, attempt=attempt, limit=final_bytes,
            )
            approval_payload = {
                **shared, "candidate": candidate, "node_outcomes": root_nodes, "evidence_ledger": ledger,
                "scans": [{"chunk_id": scan["chunk_id"], "covered_units": scan["covered_units"], "gaps": scan["gaps"]} for scan in scans],
                "required_review": {"chunk_ids": list(range(1, len(chunks) + 1)), "finding_ids": list(ledger)},
            }
            approval_review_failures = []
            coverage_feedback = None
            for review_attempt in range(1, max_review_attempts + 1):
                try:
                    approval = await call(
                        "root_approval", {**approval_payload, "review_attempt": review_attempt,
                                          "coverage_feedback": coverage_feedback},
                        lambda value: approval_record(value, range(1, len(chunks) + 1), set(ledger)), usage,
                        stage=stage, previous=previous, attempt=attempt, request_attempt=review_attempt,
                    )
                except ApprovalCoverageError as exc:
                    coverage = exc.coverage
                    invalid_ids = {key: coverage[key][:20] for key in (
                        "duplicate_chunk_ids", "unknown_chunk_ids", "duplicate_finding_ids", "unknown_finding_ids",
                    )}
                    logger.warning(
                        "Root approval coverage invalid: file_name=%s stage=%s attempt=%d "
                        "review_attempt=%d/%d reviewed_chunks=%d/%d reviewed_findings=%d/%d "
                        "missing_chunk_ids_sample=%s missing_finding_ids_sample=%s "
                        "invalid_ids_sample=%s review_exhausted=%s",
                        file_name, stage.key, attempt, review_attempt, max_review_attempts,
                        coverage["reviewed_chunk_count"], coverage["expected_chunk_count"],
                        coverage["reviewed_finding_count"], coverage["expected_finding_count"],
                        coverage["missing_chunk_ids"][:20], coverage["missing_finding_ids"][:20],
                        json.dumps(invalid_ids, ensure_ascii=True)[:2000], review_attempt == max_review_attempts,
                    )
                    approval_review_failures.append(retain({
                        "review_attempt": review_attempt, "coverage": coverage, "response": exc.review,
                    }))
                    if review_attempt == max_review_attempts:
                        raise EvidenceError(
                            f"Root approval coverage failed after {max_review_attempts} review attempts: {exc}"
                        ) from exc
                    coverage_feedback = {**coverage, "previous_review": exc.review}
                    continue
                break
            attempts.append({"attempt": attempt, "root_context": root_context, "subglobal_contexts": scopes,
                             "scans": scans, "nodes": nodes, "candidate": candidate, "approval": approval,
                             "approval_review_failures": approval_review_failures,
                             **({"map_failures": map_failures} if map_failures else {}),
                             **({"reduction_failures": reduction_failures} if reduction_failures else {})})
            logger.info(
                'Root approval decision: file_name=%s stage=%s specification="%s" attempt=%d approved=%s feedback_items=%d',
                file_name, stage.key, stage.english_title, attempt, approval["approved"], len(approval["feedback"]),
            )
            if approval["approved"]:
                stage_audits.append({"key": stage.key, "attempts": attempts})
                return candidate["body"], merge_usage(*usage)
            feedback = approval["feedback"]
            logger.warning(
                "Root rejected candidate: file_name=%s stage=%s attempt=%d/%d reprocess_chunks=%d "
                "rationale=%s feedback=%s",
                file_name, stage.key, attempt, max_attempts, len(chunks),
                json.dumps(approval["rationale"], ensure_ascii=True),
                json.dumps(feedback, ensure_ascii=True),
            )
        raise EvidenceError(f"Root rejected {stage.key} after {max_attempts} full-scan attempts")

    def with_hierarchy(result):
        return {
            **result,
            "usage": merge_usage(result["usage"], *context_usage),
            "chunks": metadata,
            "hierarchy": {"reduce_levels": reduce_levels, "global_context": plan,
                          "context_usage": merge_usage(*context_usage), "stages": list(stage_audits)},
        }

    async def save_stage(result):
        await on_stage_completed(with_hierarchy(result))

    result = await generate_stages(
        file_name, generate_stage, on_stage_completed=save_stage if on_stage_completed is not None else None,
        previous_specifications=previous,
    )
    return with_hierarchy(result)
