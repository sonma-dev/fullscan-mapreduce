import asyncio
import logging
import random
import time
from typing import Callable

import httpx
import openai
from openai import AsyncAzureOpenAI
from openai.types.responses import ResponseInputFileParam

from server.concurrency import level_concurrency_limits


logger = logging.getLogger(__name__)
BACKGROUND_CANCEL_TIMEOUT_SECONDS = 5
RESPONSE_TIMEOUT_SECONDS = 1200
RESPONSE_MAX_RETRIES = 3
RESPONSE_TIMEOUT_MAX_RETRIES = 3
RETRYABLE_RESPONSE_ERROR_CODES = frozenset({
    "server_error", "rate_limit_exceeded", "vector_store_timeout",
})


def retryable_response_failure(status, code, message):
    if status != "failed":
        return False
    if code:
        return code in RETRYABLE_RESPONSE_ERROR_CODES
    # Some Azure failures omit the code but explicitly recommend resubmission.
    message = message.casefold()
    return (
        message.startswith("an error occurred while processing your request.")
        and "you can retry your request" in message
    )


def combined_response_usage(usages):
    # Never report only the successful attempt when a failed attempt had unknown usage.
    fields = ("input_tokens", "output_tokens", "total_tokens")
    details = (("input_tokens_details", "cached_tokens"), ("output_tokens_details", "reasoning_tokens"))
    if any(not isinstance(getattr(usage, field, None), int) for usage in usages for field in fields):
        return None
    totals = {field: sum(getattr(usage, field) for usage in usages) for field in fields}
    for field, key in details:
        values = [getattr(usage, field, None) for usage in usages]
        if any(not isinstance(getattr(value, key, None), int) for value in values):
            return None
        totals[field] = values[-1].model_copy(update={key: sum(getattr(value, key) for value in values)})
    return usages[-1].model_copy(update=totals)


class RateLimitException(Exception):
    pass


class ElapsedTimeException(Exception):
    pass


class TalksWithResponses:
    def __init__(
        self,
        endpoint: str,
        token_provider: Callable[[], str],
        model_name: str,
        auth_mode: str,
        api_version: str = "2025-03-01-preview",
    ):
        self._model_name = model_name
        # Maps and chapter reductions can overlap under their own level limits.
        # Keep the existing shared capacity, including polling and retries; a
        # smaller legacy setting must not throttle an explicit level setting.
        self._slots = asyncio.Semaphore(max(level_concurrency_limits()))
        common = dict(azure_endpoint=endpoint, api_version=api_version, timeout=128.0)
        if auth_mode == "entra":
            self._client = AsyncAzureOpenAI(**common, azure_ad_token_provider=token_provider)
        else:
            self._client = AsyncAzureOpenAI(**common, api_key=token_provider())

    async def close(self) -> None:
        await self._client.close()

    def response_request_kwargs(
        self,
        query: str,
        assistant_instruction: str,
        input_file: ResponseInputFileParam | None = None,
        max_output_tokens: int | None = None,
        json_output: bool = False,
    ) -> dict:
        content = [{"type": "input_text", "text": query}]
        if input_file is not None:
            content.append(input_file)
        kwargs = {
            "model": self._model_name,
            "input": [{"role": "user", "content": content}],
            "instructions": assistant_instruction,
            "reasoning": {"effort": "low"},
            "truncation": "disabled",
            "store": True,
            "background": True,
        }
        if max_output_tokens is not None:
            kwargs["max_output_tokens"] = max_output_tokens
        if json_output:
            kwargs["text"] = {"format": {"type": "json_object"}}
        return kwargs

    async def create_response(
        self,
        query: str,
        assistant_instruction: str,
        input_file: ResponseInputFileParam | None = None,
        max_output_tokens: int | None = None,
        json_output: bool = False,
    ):
        async with self._slots:
            return await self._create_response(query, assistant_instruction, input_file, max_output_tokens, json_output)

    async def _create_response(self, query, assistant_instruction, input_file, max_output_tokens, json_output):
        client = self._client.with_options(
            timeout=httpx.Timeout(8.0, connect=2.0, read=8.0, write=4.0),
            max_retries=32,
        )
        started = time.perf_counter()
        response = None
        failed_usages = []
        request_kwargs = self.response_request_kwargs(query, assistant_instruction, input_file, max_output_tokens, json_output)
        # Deadline retries and processing-error retries have independent budgets.
        # Neither kind of failure resets the other counter.
        timeout_failures = processing_failures = response_attempt = 0
        while True:
            deadline = asyncio.timeout(RESPONSE_TIMEOUT_SECONDS)
            try:
                # Each deadline attempt includes submission, polling, HTTP retries,
                # and any remaining processing-error retries.
                async with deadline:
                    while True:
                        response_attempt += 1
                        response = None
                        logger.info(
                            "Responses request submitting: model=%s input_chars=%d file_name=%s "
                            "max_output_tokens=%s response_attempt=%d deadline_attempt=%d",
                            self._model_name, len(query),
                            input_file.get("filename", "") if input_file else "",
                            max_output_tokens, response_attempt, timeout_failures + 1,
                        )
                        response = await client.responses.create(**request_kwargs)
                        last_status = None
                        last_progress = -30.0
                        while True:
                            status = response.status
                            elapsed = time.perf_counter() - started
                            if status == "completed":
                                usage = getattr(response, "usage", None)
                                if failed_usages:
                                    usage = combined_response_usage([*failed_usages, usage])
                                    response = response.model_copy(update={"usage": usage})
                                logger.info(
                                    "Responses request completed: response_id=%s elapsed_s=%.1f "
                                    "input_tokens=%s output_tokens=%s total_tokens=%s response_attempt=%d deadline_attempt=%d",
                                    response.id, elapsed,
                                    getattr(usage, "input_tokens", None),
                                    getattr(usage, "output_tokens", None),
                                    getattr(usage, "total_tokens", None),
                                    response_attempt, timeout_failures + 1,
                                )
                                return response
                            if status not in {"queued", "in_progress"}:
                                error = getattr(response, "error", None)
                                code = (getattr(error, "code", None) or "").strip().lower()
                                message = getattr(error, "message", None) or ""
                                reason = getattr(getattr(response, "incomplete_details", None), "reason", "") or ""
                                retryable = retryable_response_failure(status, code, message)
                                if not retryable or processing_failures >= RESPONSE_MAX_RETRIES:
                                    logger.error(
                                        "Responses request stopped: response_id=%s status=%s error_code=%s "
                                        "response_attempt=%d processing_retries_exhausted=%s",
                                        response.id, status, code or "unknown", response_attempt, retryable,
                                    )
                                    raise RuntimeError(
                                        f"Response {response.id} ended with status {status}: "
                                        f"error_code={code or 'unknown'} {message} {reason} "
                                        f"(requests={response_attempt}, processing_retries_exhausted={retryable})"
                                    )
                                processing_failures += 1
                                failed_usages.append(getattr(response, "usage", None))
                                delay = 2 ** processing_failures + random.uniform(0, 1)
                                logger.warning(
                                    "Responses processing failed; retrying: response_id=%s error_code=%s "
                                    "retry=%d/%d delay_s=%.1f elapsed_s=%.1f error_message=%s",
                                    response.id, code or "unknown", processing_failures, RESPONSE_MAX_RETRIES,
                                    delay, elapsed, message,
                                )
                                await asyncio.sleep(delay)
                                break
                            if status != last_status or elapsed - last_progress >= 30:
                                logger.info(
                                    "Responses request polling: response_id=%s status=%s elapsed_s=%.1f response_attempt=%d deadline_attempt=%d",
                                    response.id, status, elapsed, response_attempt, timeout_failures + 1,
                                )
                                last_status, last_progress = status, elapsed
                            await asyncio.sleep(2)
                            response = await client.responses.retrieve(response.id)
            except asyncio.CancelledError:
                # Caller cancellation includes the hierarchy's 300-second leaf Map
                # deadline. It must never start a 1200-second deadline retry here.
                await self._cancel_background_response(response)
                raise
            except openai.RateLimitError as exc:
                raise RateLimitException() from exc
            except (openai.APITimeoutError, TimeoutError) as exc:
                if not deadline.expired():
                    # HTTP timeout retries remain the SDK's responsibility.
                    await self._cancel_background_response(response)
                    raise ElapsedTimeException() from exc
                timeout_failures += 1
                exhausted = timeout_failures > RESPONSE_TIMEOUT_MAX_RETRIES
                logger.log(
                    logging.ERROR if exhausted else logging.WARNING,
                    "Responses deadline exceeded: response_id=%s timeout_s=%s "
                    "deadline_attempt=%d retry=%d/%d response_attempt=%d elapsed_s=%.1f "
                    "timeout_retries_exhausted=%s",
                    getattr(response, "id", "unknown"), RESPONSE_TIMEOUT_SECONDS,
                    timeout_failures, min(timeout_failures, RESPONSE_TIMEOUT_MAX_RETRIES),
                    RESPONSE_TIMEOUT_MAX_RETRIES, response_attempt, time.perf_counter() - started, exhausted,
                )
                await self._cancel_background_response(response)
                if exhausted:
                    raise ElapsedTimeException(
                        f"Response exceeded {RESPONSE_TIMEOUT_SECONDS}s after {timeout_failures} deadline attempts "
                        f"(requests={response_attempt}, timeout_retries_exhausted=True)"
                    ) from exc
                # A timed-out attempt can consume tokens without reporting final usage.
                failed_usages.append(None)
                # Retry the identical request with a fresh deadline, after cleanup.


    async def _cancel_background_response(self, response) -> None:
        if response is None or response.status not in {"queued", "in_progress"}:
            return
        try:
            # Cancellation must not inherit the normal client's transport retries.
            client = self._client.with_options(max_retries=0, timeout=BACKGROUND_CANCEL_TIMEOUT_SECONDS)
            async with asyncio.timeout(BACKGROUND_CANCEL_TIMEOUT_SECONDS):
                await client.responses.cancel(response.id)
            logger.info("Responses cancellation requested: response_id=%s", response.id)
        except Exception as exc:
            logger.warning(
                "Responses cancellation failed: response_id=%s error_type=%s",
                response.id, type(exc).__name__,
            )
