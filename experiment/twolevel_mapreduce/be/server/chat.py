from server.hierarchy import run_hierarchy
from server.specifications import StageCompleted


REDUCE_LEVELS = 2


async def generate_specifications(
    services, file_bytes: bytes, file_name: str, *, on_stage_completed: StageCompleted | None = None,
    resume_state: dict | None = None,
) -> dict:
    return await run_hierarchy(
        services, file_bytes, file_name, reduce_levels=REDUCE_LEVELS, on_stage_completed=on_stage_completed,
        resume_state=resume_state,
    )
