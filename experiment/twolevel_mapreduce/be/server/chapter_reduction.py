"""Bounded calls within one chapter fork, with full evidence-ID accounting."""

import asyncio

from server.evidence import EvidenceError, encode, require


def finding_ids(children):
    return {
        identifier
        for child in children
        for identifier in (
            [finding["id"] for finding in child["findings"]] if "findings" in child else
            [key for decision in child["outcome"]["decisions"] for key in decision["finding_ids"]]
        )
    }


def _atoms(scan):
    """A large scan can span calls; original scans remain intact in the audit."""
    base = {key: value for key, value in scan.items() if key not in {"findings", "gaps"}}
    for finding in scan["findings"]:
        yield {**base, "findings": [finding], "gaps": []}
    for gap in scan["gaps"]:
        yield {**base, "findings": [], "gaps": [gap]}


async def reduce_chapter(children, *, payload_base, fits, invoke, batch_bytes, max_rounds):
    """`fits` measures the rendered prompt, including prior specs and contexts.

    `invoke` applies the usual adjudication validator to the exact input ID set.
    Batches in one round run concurrently; `invoke` supplies the shared level-1
    request limit. Every batch must finish before the next round or final judgment.
    No additional fork or Map layer is created.
    """
    expected = finding_ids(children)
    history = []

    def payload(items, mode, round_number, batch=1):
        return {**payload_base, "children": items, "aggregation": {
            "mode": mode, "round": round_number, "batch": batch,
            "input_kind": "findings" if round_number == 0 else "judgments",
        }}

    # Keep the ordinary one-call path and schema for chapters that already fit.
    direct = {**payload_base, "children": children}
    if len(encode(children).encode("utf-8")) <= batch_bytes and fits(direct):
        return await invoke(direct, expected, False), history
    require(fits(payload([], "batch", 0)), "Chapter context and previous specifications exceed the input budget before any evidence; increase the chapter input/query budget")
    current = children
    for round_number in range(max_rounds):
        final = payload(current, "final", round_number)
        if round_number and len(encode(current).encode("utf-8")) <= batch_bytes and fits(final):
            outcome = await invoke(final, expected, False)
            history.append({**final["aggregation"], "outcome": outcome})
            return outcome, history
        units = []
        for child in current:
            single = payload([child], "batch", round_number)
            if round_number == 0 and (len(encode(child).encode("utf-8")) > batch_bytes or not fits(single)):
                units.extend(_atoms(child))
            else:
                units.append(child)
        batches, batch = [], []
        for unit in units:
            proposed = [*batch, unit]
            request = payload(proposed, "batch", round_number)
            if batch and (len(encode(proposed).encode("utf-8")) > batch_bytes or not fits(request)):
                batches.append(batch)
                batch = []
            require(fits(payload([unit], "batch", round_number)), "A single chapter finding or judgment exceeds the input budget; increase the chapter input/query budget")
            batch.append(unit)
        if batch:
            batches.append(batch)
        require(bool(batches), "Chapter aggregation has no input records")

        async def reduce_batch(index, batch):
            request = payload(batch, "batch", round_number, index)
            outcome = await invoke(request, finding_ids(batch), True)
            return {**request["aggregation"], "outcome": outcome}

        # Cancel and await sibling batches on failure. Commit a complete round
        # in source order, regardless of the order in which requests finish.
        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(reduce_batch(index, batch))
                     for index, batch in enumerate(batches, 1)]
        round_history = [task.result() for task in tasks]
        history.extend(round_history)
        reduced = [{"outcome": item["outcome"]} for item in round_history]
        require(finding_ids(reduced) == expected, "Chapter batches lost evidence identifiers")
        if round_number and len(encode(reduced)) >= len(encode(current)):
            raise EvidenceError("Chapter aggregation made no compression progress; increase the chapter input/batch budget")
        current = reduced
    raise EvidenceError(f"Chapter aggregation exceeded {max_rounds} rounds; increase the chapter input/batch budget")
