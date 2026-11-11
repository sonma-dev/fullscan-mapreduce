import asyncio
import base64
import json
import re
import unittest
from collections import Counter
from unittest.mock import AsyncMock, patch

import httpx
from openai import AsyncAzureOpenAI

from plugins.talks_with_responses import talks_with_responses as responses_plugin
from plugins.talks_with_responses.talks_with_responses import ElapsedTimeException, TalksWithResponses
from server.input_files import create_input_file
from server.utils import response_usage


AZURE_RETRY_MESSAGE = (
    "An error occurred while processing your request. You can retry your request, "
    "or contact us through an Azure support request if the error persists."
)


def failed(code="server_error", message="Temporary processing failure", **kwargs):
    return {"status": "failed", "error": {"code": code, "message": message}, **kwargs}


class ResponseRetryTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # SDK platform detection is unrelated to the mocked response lifecycle.
        platform = patch("openai._base_client.get_platform", return_value="Linux")
        platform.start()
        self.addCleanup(platform.stop)
        self.requests = []
        self.events = []
        self.submissions = 0

        def handle(request):
            self.requests.append(request)
            if request.url.path.endswith("/cancel"):
                response_id = request.url.path.split("/")[-2]
            elif request.method == "POST":
                self.submissions += 1
                response_id = f"resp_{self.submissions}"
            else:
                response_id = request.url.path.split("/")[-1]
            event = self.events.pop(0)
            return httpx.Response(200, json={
                "id": response_id, "object": "response", "created_at": 1,
                "model": "test-model", "status": "completed",
                "output": [{"type": "message", "id": "msg_test", "role": "assistant", "status": "completed",
                            "content": [{"type": "output_text", "text": "Specification", "annotations": []}]}],
                "usage": {"input_tokens": 10, "output_tokens": 3, "total_tokens": 13,
                          "input_tokens_details": {"cached_tokens": 2},
                          "output_tokens_details": {"reasoning_tokens": 1}},
                **event,
            })

        client = AsyncAzureOpenAI(
            azure_endpoint="https://example.openai.azure.com", api_version="2025-03-01-preview",
            api_key="test-key", http_client=httpx.AsyncClient(transport=httpx.MockTransport(handle)),
        )
        with patch.object(responses_plugin, "AsyncAzureOpenAI", return_value=client):
            self.plugin = TalksWithResponses("https://example.openai.azure.com", lambda: "test-key", "test-model", "api_key")
        self.options = {"max_output_tokens": 64000}

    async def asyncTearDown(self):
        await self.plugin.close()

    async def call(self, **kwargs):
        return await self.plugin.create_response(
            "Review the existing candidate and evidence", "Review instructions", **self.options, **kwargs,
        )

    async def test_failed_polled_job_resubmits_identical_input_and_polls_new_id(self):
        self.events = [{"status": "queued"}, failed(), {"status": "queued"}, {}]
        with patch("asyncio.sleep", new_callable=AsyncMock), patch.object(
            responses_plugin.random, "uniform", return_value=0,
        ), self.assertLogs(responses_plugin.logger, level="INFO") as logs:
            result = await self.call(input_file=create_input_file(b"original source bytes", "sample.pdf"))
        self.assertEqual([request.method for request in self.requests], ["POST", "GET", "POST", "GET"])
        self.assertEqual(self.requests[0].content, self.requests[2].content)
        self.assertTrue(self.requests[1].url.path.endswith("/responses/resp_1"))
        self.assertTrue(self.requests[3].url.path.endswith("/responses/resp_2"))
        self.assertEqual(result.id, "resp_2")
        self.assertEqual(result.output_text, "Specification")
        self.assertEqual(response_usage(result), {"input_tokens": 20, "output_tokens": 6, "total_tokens": 26})
        self.assertEqual(result.usage.input_tokens_details.cached_tokens, 4)
        self.assertEqual(result.usage.output_tokens_details.reasoning_tokens, 2)
        payload = json.loads(self.requests[2].content)
        self.assertEqual(payload["max_output_tokens"], 64000)
        self.assertEqual(payload["input"][0]["content"][1]["filename"], "sample.pdf")
        self.assertTrue(any("response_id=resp_1 error_code=server_error retry=1/3" in line for line in logs.output))
        self.assertTrue(any("response_id=resp_2" in line and "response_attempt=2" in line for line in logs.output))

    async def test_retryable_codes_and_code_less_azure_error(self):
        cases = [
            failed("server_error"), failed("rate_limit_exceeded"), failed("vector_store_timeout"),
            failed(None, AZURE_RETRY_MESSAGE),
        ]
        for event in cases:
            with self.subTest(event=event):
                self.requests.clear()
                self.events = [event, {}]
                with patch("asyncio.sleep", new_callable=AsyncMock):
                    result = await self.call()
                self.assertEqual(result.status, "completed")
                self.assertEqual([request.method for request in self.requests], ["POST", "POST"])

    async def test_fourth_submission_can_succeed_with_one_shared_deadline(self):
        self.events = [failed(), failed(), failed(), {}]
        real_timeout = asyncio.timeout
        with patch("asyncio.sleep", new_callable=AsyncMock) as sleep, patch.object(
            responses_plugin.random, "uniform", return_value=0,
        ), patch.object(responses_plugin.asyncio, "timeout", wraps=real_timeout) as timeout:
            result = await self.call()
        self.assertEqual(result.status, "completed")
        self.assertEqual(self.submissions, 4)
        self.assertEqual([call.args[0] for call in sleep.await_args_list], [2, 4, 8])
        timeout.assert_called_once_with(1200)
        self.assertEqual(response_usage(result)["total_tokens"], 52)

    async def test_retry_exhaustion_stops_after_four_submissions(self):
        self.events = [failed()] * 4
        with patch("asyncio.sleep", new_callable=AsyncMock) as sleep, self.assertLogs(
            responses_plugin.logger, level="WARNING",
        ) as logs:
            with self.assertRaisesRegex(RuntimeError, "resp_4.*server_error.*requests=4.*processing_retries_exhausted=True"):
                await self.call()
        self.assertEqual(self.submissions, 4)
        self.assertEqual(sleep.await_count, 3)
        self.assertTrue(any("retry=3/3" in line for line in logs.output))
        self.assertTrue(any("processing_retries_exhausted=True" in line for line in logs.output))

    async def test_permanent_unknown_and_non_failed_terminal_states_are_not_retried(self):
        cases = [
            failed("invalid_prompt", AZURE_RETRY_MESSAGE), failed("invalid_image"),
            failed("unknown_error", AZURE_RETRY_MESSAGE), failed(None, "Unknown failure"),
            {"status": "failed", "error": None},
            {"status": "incomplete", "incomplete_details": {"reason": "max_output_tokens"}},
            {"status": "incomplete", "error": {"code": "server_error", "message": AZURE_RETRY_MESSAGE}},
            {"status": "cancelled"},
        ]
        for event in cases:
            with self.subTest(event=event):
                self.requests.clear()
                self.events = [event]
                with patch("asyncio.sleep", new_callable=AsyncMock) as sleep:
                    with self.assertRaises(RuntimeError):
                        await self.call()
                self.assertEqual(len(self.requests), 1)
                sleep.assert_not_awaited()

    async def test_missing_failed_attempt_usage_is_reported_as_unknown(self):
        self.events = [failed(usage=None), {}]
        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await self.call()
        self.assertEqual(result.status, "completed")
        self.assertEqual(response_usage(result), dict.fromkeys(("input_tokens", "output_tokens", "total_tokens")))

    def track_deadlines(self):
        real_timeout = asyncio.timeout
        self.deadlines = []

        def create_timeout(seconds):
            deadline = real_timeout(seconds)
            if seconds == responses_plugin.RESPONSE_TIMEOUT_SECONDS:
                self.deadlines.append(deadline)
            return deadline

        return patch.object(responses_plugin.asyncio, "timeout", side_effect=create_timeout)

    async def expire_deadline(self, *_):
        # Expire the actual deadline only once the intended operation is reached.
        self.deadlines[-1].reschedule(asyncio.get_running_loop().time())
        await asyncio.Event().wait()

    async def test_deadline_includes_backoff_and_restarts_with_a_fresh_budget(self):
        self.events = [failed(), {}]
        with self.track_deadlines(), patch("asyncio.sleep", side_effect=self.expire_deadline):
            result = await self.call()
        self.assertEqual(self.submissions, 2)
        self.assertEqual(len(self.deadlines), 2)
        self.assertIsNot(self.deadlines[0], self.deadlines[1])
        self.assertTrue(self.deadlines[0].expired())
        self.assertFalse(self.deadlines[1].expired())
        self.assertEqual(self.requests[0].content, self.requests[1].content)
        self.assertEqual(response_usage(result), dict.fromkeys(("input_tokens", "output_tokens", "total_tokens")))

    async def test_three_deadlines_cancel_old_jobs_and_resubmit_identical_input(self):
        self.events = [{"status": "in_progress"}, {"status": "cancelled"}] * 3 + [{}]
        attachment = create_input_file(b"Original document bytes", "sample.pdf")
        with self.track_deadlines(), patch("asyncio.sleep", side_effect=self.expire_deadline), self.assertLogs(
            responses_plugin.logger, level="INFO",
        ) as logs:
            result = await self.call(input_file=attachment)
        self.assertEqual(self.submissions, 4)
        self.assertEqual(len(self.deadlines), 4)
        self.assertEqual([deadline.expired() for deadline in self.deadlines], [True, True, True, False])
        submissions = [request for request in self.requests if not request.url.path.endswith("/cancel")]
        self.assertTrue(all(request.content == submissions[0].content for request in submissions))
        self.assertEqual([request.url.path.rsplit("/", 2)[-2] for request in self.requests
                          if request.url.path.endswith("/cancel")], ["resp_1", "resp_2", "resp_3"])
        self.assertEqual(result.id, "resp_4")
        self.assertEqual(response_usage(result), dict.fromkeys(("input_tokens", "output_tokens", "total_tokens")))
        for retry in range(1, 4):
            self.assertTrue(any(f"retry={retry}/3" in line and "timeout_s=1200" in line for line in logs.output))
        self.assertTrue(any("response_attempt=4 deadline_attempt=4" in line for line in logs.output))

    async def test_fourth_deadline_fails_and_releases_the_request_slot(self):
        self.events = [{"status": "queued"}, {"status": "cancelled"}] * 4
        self.plugin._slots = asyncio.Semaphore(1)
        with self.track_deadlines(), patch("asyncio.sleep", side_effect=self.expire_deadline), self.assertLogs(
            responses_plugin.logger, level="WARNING",
        ) as logs:
            with self.assertRaisesRegex(ElapsedTimeException, "after 4 deadline attempts.*timeout_retries_exhausted=True"):
                await self.call()
        self.assertEqual(self.submissions, 4)
        self.assertEqual(len(self.deadlines), 4)
        self.assertEqual(sum(request.url.path.endswith("/cancel") for request in self.requests), 4)
        self.assertTrue(any("deadline_attempt=4" in line and "timeout_retries_exhausted=True" in line
                            for line in logs.output))
        self.events = [{}]
        self.assertEqual((await asyncio.wait_for(self.call(), 5)).status, "completed")

    async def test_processing_retries_do_not_reset_the_deadline_retry_budget(self):
        # Three processing failures and three deadlines can precede success.
        # A fourth deadline must stop even with processing errors between them.
        for succeeds in (True, False):
            with self.subTest(succeeds=succeeds):
                self.requests.clear()
                self.submissions = 0
                self.events = [failed(), {"status": "queued"}, {"status": "cancelled"}] * 3
                self.events += [{}] if succeeds else [{"status": "queued"}, {"status": "cancelled"}]
                backoffs = []

                async def expire_only_polling(delay):
                    if self.submissions % 2 == 0 or self.submissions == 7:
                        await self.expire_deadline()
                    backoffs.append(delay)

                with self.track_deadlines(), patch("asyncio.sleep", side_effect=expire_only_polling), patch.object(
                    responses_plugin.random, "uniform", return_value=0,
                ):
                    if succeeds:
                        result = await self.call()
                        self.assertIsNone(result.usage)
                    else:
                        with self.assertRaisesRegex(ElapsedTimeException, "requests=7.*timeout_retries_exhausted=True"):
                            await self.call()
                self.assertEqual(self.submissions, 7)
                self.assertEqual(len(self.deadlines), 4)
                self.assertEqual(backoffs, [2, 4, 8])

    async def test_deadlines_do_not_reset_the_processing_retry_budget(self):
        self.events = [failed(), {"status": "queued"}, {"status": "cancelled"}] * 3 + [failed()]

        async def expire_only_polling(_):
            if self.submissions % 2 == 0:
                await self.expire_deadline()

        with self.track_deadlines(), patch("asyncio.sleep", side_effect=expire_only_polling):
            with self.assertRaisesRegex(RuntimeError, "requests=7.*processing_retries_exhausted=True"):
                await self.call()
        self.assertEqual(self.submissions, 7)
        self.assertEqual(len(self.deadlines), 4)

    async def test_timeout_before_submission_returns_an_id_retries_without_cancelling_an_unknown_job(self):
        self.events = [{}]
        original_create = self.plugin._client.responses.create
        calls = 0

        async def create(**kwargs):
            nonlocal calls
            calls += 1
            if calls == 1:
                await self.expire_deadline()
            return await original_create(**kwargs)

        with self.track_deadlines(), patch(
            "openai.resources.responses.responses.AsyncResponses.create", side_effect=create,
        ):
            result = await self.call()
        self.assertEqual(calls, 2)
        self.assertEqual(len(self.deadlines), 2)
        self.assertEqual(len(self.requests), 1)
        self.assertIsNone(result.usage)

    async def test_timeout_during_retrieve_cancels_old_response_and_polls_the_replacement(self):
        self.events = [{"status": "queued"}, {"status": "cancelled"}, {"status": "queued"}, {}]
        original_retrieve = self.plugin._client.responses.retrieve
        polled = []

        async def retrieve(response_id):
            polled.append(response_id)
            if len(polled) == 1:
                await self.expire_deadline()
            return await original_retrieve(response_id)

        with self.track_deadlines(), patch("asyncio.sleep", new_callable=AsyncMock), patch(
            "openai.resources.responses.responses.AsyncResponses.retrieve", side_effect=retrieve,
        ):
            result = await self.call()
        self.assertEqual(polled, ["resp_1", "resp_2"])
        self.assertEqual(result.id, "resp_2")
        self.assertTrue(self.requests[1].url.path.endswith("/responses/resp_1/cancel"))
        self.assertTrue(self.requests[-1].url.path.endswith("/responses/resp_2"))

    async def test_sdk_timeout_before_the_deadline_is_not_retried_by_the_deadline_loop(self):
        from openai import APITimeoutError
        self.events = []
        error = APITimeoutError(request=httpx.Request("POST", "https://example.openai.azure.com"))
        with self.track_deadlines(), patch(
            "openai.resources.responses.responses.AsyncResponses.create", side_effect=error,
        ) as create:
            with self.assertRaises(ElapsedTimeException):
                await self.call()
        self.assertEqual(create.await_count, 1)
        self.assertFalse(self.deadlines[0].expired())

    async def test_remote_cleanup_timeout_is_bounded_before_retrying(self):
        self.events = [{"status": "in_progress"}, {}]

        async def hang(*args, **kwargs):
            await asyncio.Event().wait()

        with self.track_deadlines(), patch("asyncio.sleep", side_effect=self.expire_deadline), patch.object(
            responses_plugin, "BACKGROUND_CANCEL_TIMEOUT_SECONDS", 0.02,
        ), patch("openai.resources.responses.responses.AsyncResponses.cancel", side_effect=hang) as cancel:
            result = await asyncio.wait_for(self.call(), 5)
        self.assertEqual(result.status, "completed")
        self.assertEqual(self.submissions, 2)
        cancel.assert_awaited_once_with("resp_1")

    async def test_caller_cancellation_during_timeout_cleanup_does_not_resubmit(self):
        self.events = [{"status": "in_progress"}]
        cleaning = asyncio.Event()

        async def hang(*args, **kwargs):
            cleaning.set()
            await asyncio.Event().wait()

        with self.track_deadlines(), patch("asyncio.sleep", side_effect=self.expire_deadline), patch(
            "openai.resources.responses.responses.AsyncResponses.cancel", side_effect=hang,
        ):
            task = asyncio.create_task(self.call())
            try:
                await asyncio.wait_for(cleaning.wait(), 5)
            finally:
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await asyncio.wait_for(task, 5)
        self.assertEqual(self.submissions, 1)
        self.assertEqual(len(self.deadlines), 1)

    async def test_outer_map_deadline_cancels_without_starting_a_client_deadline_retry(self):
        self.events = [{"status": "queued"}, {"status": "cancelled"}]
        outer_deadline = asyncio.timeout(300)

        async def expire_outer(_):
            outer_deadline.reschedule(asyncio.get_running_loop().time())
            await asyncio.Event().wait()

        with self.track_deadlines(), patch("asyncio.sleep", side_effect=expire_outer):
            with self.assertRaises(TimeoutError):
                async with outer_deadline:
                    await self.call()
        self.assertEqual(self.submissions, 1)
        self.assertEqual(len(self.deadlines), 1)
        self.assertFalse(self.deadlines[0].expired())
        self.assertTrue(self.requests[-1].url.path.endswith("/responses/resp_1/cancel"))

    async def test_full_load_retries_only_current_specification_and_keeps_stage_output(self):
        from server.chat import generate_specifications
        from server.models import AppServices

        def output(step):
            return {"output": [{"type": "message", "id": "msg_test", "role": "assistant", "status": "completed",
                                "content": [{"type": "output_text", "text": f"Generated specification {step}.",
                                             "annotations": []}]}]}

        for succeeds in (True, False):
            with self.subTest(succeeds=succeeds):
                self.requests.clear()
                self.submissions = 0
                self.events = [output(1)] + [{"status": "queued"}, {"status": "cancelled"}] * (3 if succeeds else 4)
                if succeeds:
                    self.events.extend(output(step) for step in range(2, 9))
                saved = AsyncMock()
                data = b"%PDF-original document\x00\xff"
                with self.track_deadlines(), patch("asyncio.sleep", side_effect=self.expire_deadline):
                    if succeeds:
                        result = await generate_specifications(
                            AppServices(responses=self.plugin), data, "sample.pdf", on_stage_completed=saved,
                        )
                        self.assertEqual(len(result["specifications"]), 8)
                        self.assertIsNone(result["usage"]["total_tokens"])
                        self.assertIsNone(result["specifications"][1]["usage"]["total_tokens"])
                        self.assertIsNotNone(result["specifications"][0]["usage"]["total_tokens"])
                        self.assertIsNotNone(result["specifications"][2]["usage"]["total_tokens"])
                    else:
                        with self.assertRaisesRegex(ElapsedTimeException, "timeout_retries_exhausted=True"):
                            await generate_specifications(
                                AppServices(responses=self.plugin), data, "sample.pdf", on_stage_completed=saved,
                            )
                bodies = [json.loads(request.content) for request in self.requests if not request.url.path.endswith("/cancel")]
                steps = []
                for body in bodies:
                    content = body["input"][0]["content"]
                    step = int(re.search(r"^Stage: (\d+)/8$", content[0]["text"], re.M)[1])
                    steps.append(step)
                    if step == 8:
                        self.assertEqual(len(content), 1)
                    else:
                        self.assertEqual(base64.b64decode(content[1]["file_data"].split(",", 1)[1]), data)
                        self.assertEqual(content[1]["filename"], "sample.pdf")
                    for previous in range(1, step):
                        self.assertIn(f"Generated specification {previous}.", content[0]["text"])
                self.assertEqual(Counter(steps), {1: 1, 2: 4, **({step: 1 for step in range(3, 9)} if succeeds else {})})
                self.assertTrue(all(body == bodies[1] for body in bodies[1:5]))
                self.assertEqual([len(call.args[0]["specifications"]) for call in saved.await_args_list],
                                 list(range(1, 9)) if succeeds else [1])

    async def test_cancellation_during_backoff_does_not_resubmit(self):
        self.events = [failed()]
        waiting = asyncio.Event()

        async def wait_forever(_):
            waiting.set()
            await asyncio.Event().wait()

        with patch("asyncio.sleep", side_effect=wait_forever):
            task = asyncio.create_task(self.call())
            try:
                await asyncio.wait_for(waiting.wait(), 20)
            finally:
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await asyncio.wait_for(task, 10)
        self.assertEqual(self.submissions, 1)
        self.assertEqual(len(self.requests), 1)

    async def test_cancellation_after_resubmission_cancels_the_new_job(self):
        self.events = [failed(), {"status": "in_progress"}, {"status": "cancelled"}]
        polling = asyncio.Event()
        sleeps = 0

        async def wait_on_second_sleep(_):
            nonlocal sleeps
            sleeps += 1
            if sleeps == 2:
                polling.set()
                await asyncio.Event().wait()

        with patch("asyncio.sleep", side_effect=wait_on_second_sleep):
            task = asyncio.create_task(self.call())
            try:
                await asyncio.wait_for(polling.wait(), 20)
            finally:
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await asyncio.wait_for(task, 10)
        self.assertEqual(self.submissions, 2)
        self.assertEqual([request.method for request in self.requests], ["POST", "POST", "POST"])
        self.assertTrue(self.requests[-1].url.path.endswith("/responses/resp_2/cancel"))
        self.events = [{}]
        self.assertEqual((await asyncio.wait_for(self.call(), 10)).status, "completed")


if __name__ == "__main__":
    unittest.main()
