"""Independent request limits for chapter workers and leaf Map workers."""

from server.utils import env_int


def level_concurrency_limits() -> tuple[int, int]:
    # Preserve existing installations until each level gets an explicit setting.
    legacy = env_int("LLM_MAX_PARALLEL_CHUNK_REQUESTS", 16, 16)
    return (
        env_int("LLM_MAX_PARALLEL_LEVEL1_REQUESTS", legacy, 16),
        env_int("LLM_MAX_PARALLEL_LEVEL2_REQUESTS", legacy, 16),
    )
