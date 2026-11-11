import asyncio
import json
import re
import unittest
from collections import Counter
from unittest.mock import AsyncMock, patch

import httpx
from openai import AsyncAzureOpenAI

from plugins.talks_with_responses import talks_with_responses as responses_plugin
from server import chat
from server.models import AppServices
from test_chat import FakeResponses
from test_file_chunks import make_deck


class HierarchyResponseRetryTests(unittest.IsolatedAsyncioTestCase):
    async def run_approval_failure(self, failures, *, target_phase="root_approval", deadline_failure=False):
        fake = FakeResponses(self)
        submissions = Counter()
        reviews = []
        saved = AsyncMock()

        async def handle(request):
            if request.url.path.endswith("/cancel"):
                return httpx.Response(200, json={
                    "id": request.url.path.split("/")[-2], "object": "response",
                    "created_at": 1, "model": "test-model", "status": "cancelled", "output": [],
                })
            self.assertEqual(request.method, "POST")
            body = json.loads(request.content)
            content = body["input"][0]["content"]
            query = content[0]["text"]
            phase = re.search(r"^Phase: (\w+)$", query, re.M)[1]
            match = re.search(r"^Stage: (\d+)/8$", query, re.M)
            step = int(match[1]) if match else 0
            submissions[(phase, step)] += 1
            result = {
                "id": f"resp_{sum(submissions.values())}", "object": "response",
                "created_at": 1, "model": "test-model",
            }
            payload = {} if phase == 'decision_register' else json.loads(query.split('<payload>\n', 1)[1].rsplit('\n</payload>', 1)[0])
            selected_chapter = phase != "onelevel_reduce" or payload["jurisdiction"]["chunk_ids"][0] == 1
            if phase == target_phase and step == 2 and selected_chapter:
                reviews.append(body)
                if len(reviews) <= failures:
                    if deadline_failure:
                        return httpx.Response(200, json={**result, "status": "queued", "output": [], "usage": None})
                    return httpx.Response(200, json={
                        **result, "status": "failed", "output": [], "usage": None,
                        "error": {"code": "server_error", "message": "An error occurred while processing your request."},
                    })
            generated = await fake.create_response(
                query=query, assistant_instruction=body["instructions"],
                input_file=content[1] if len(content) > 1 else None,
                max_output_tokens=body["max_output_tokens"],
                json_output=body.get("text", {}).get("format", {}).get("type") == "json_object",
            )
            return httpx.Response(200, json={
                **result, "status": "completed",
                "output": [{"type": "message", "id": "msg_test", "role": "assistant", "status": "completed",
                            "content": [{"type": "output_text", "text": generated.output_text, "annotations": []}]}],
                "usage": {**vars(generated.usage), "input_tokens_details": {"cached_tokens": 0},
                          "output_tokens_details": {"reasoning_tokens": 0}},
            })

        client = AsyncAzureOpenAI(
            azure_endpoint="https://example.openai.azure.com", api_version="2025-03-01-preview",
            api_key="test-key", http_client=httpx.AsyncClient(transport=httpx.MockTransport(handle)),
        )
        with patch.object(responses_plugin, "AsyncAzureOpenAI", return_value=client):
            plugin = responses_plugin.TalksWithResponses(
                "https://example.openai.azure.com", lambda: "test-key", "test-model", "api_key",
            )
        real_timeout = asyncio.timeout
        deadlines = {}

        def create_deadline(seconds):
            deadline = real_timeout(seconds)
            if seconds == responses_plugin.RESPONSE_TIMEOUT_SECONDS:
                deadlines[asyncio.current_task()] = deadline
            return deadline

        async def sleep(seconds):
            if deadline_failure and seconds == 2:
                deadlines[asyncio.current_task()].reschedule(asyncio.get_running_loop().time())
                await asyncio.Event().wait()

        try:
            with patch.dict("os.environ", {"FILE_CHUNK_MAX_SLIDES": "1", "LLM_MAX_PARALLEL_CHUNK_REQUESTS": "2"}), patch(
                "asyncio.sleep", side_effect=sleep,
            ), patch.object(responses_plugin.asyncio, "timeout", side_effect=create_deadline):
                if failures > 3:
                    error_type = responses_plugin.ElapsedTimeException if deadline_failure else RuntimeError
                    marker = "timeout_retries_exhausted=True" if deadline_failure else "processing_retries_exhausted=True"
                    with self.assertRaisesRegex(error_type, marker):
                        await chat.generate_specifications(
                            AppServices(responses=plugin), make_deck(4), "sample.pptx", on_stage_completed=saved,
                        )
                    result = None
                else:
                    result = await chat.generate_specifications(
                        AppServices(responses=plugin), make_deck(4), "sample.pptx", on_stage_completed=saved,
                    )
        finally:
            await plugin.close()
        return result, submissions, reviews, saved

    async def test_api_stage_retries_only_approval_without_repeating_map_or_candidate(self):
        result, submissions, reviews, saved = await self.run_approval_failure(1)
        self.assertEqual(submissions[("root_approval", 2)], 2)
        self.assertEqual(reviews[0], reviews[1])
        for step in range(1, 8):
            self.assertEqual(submissions[("map", step)], 4)
            self.assertEqual(submissions[("root_reduce", step)], 1)
            self.assertEqual(submissions[("root_context", step)], 1)
        self.assertEqual(submissions[("decision_register", 8)], 1)
        self.assertEqual(len(result["specifications"]), 8)
        self.assertTrue(all(len(stage["attempts"]) == 1 for stage in result["hierarchy"]["stages"]))
        self.assertIsNone(result["specifications"][1]["usage"]["total_tokens"])
        self.assertIsNotNone(result["specifications"][0]["usage"]["total_tokens"])
        self.assertIsNotNone(result["specifications"][2]["usage"]["total_tokens"])
        self.assertEqual([len(call.args[0]["specifications"]) for call in saved.await_args_list], list(range(1, 9)))

    async def test_exhaustion_keeps_the_completed_stage_and_does_not_rescan(self):
        result, submissions, reviews, saved = await self.run_approval_failure(4)
        self.assertIsNone(result)
        self.assertEqual(submissions[("root_approval", 2)], 4)
        self.assertTrue(all(review == reviews[0] for review in reviews))
        self.assertEqual(submissions[("map", 1)], 4)
        self.assertEqual(submissions[("map", 2)], 4)
        self.assertEqual(submissions[("root_reduce", 2)], 1)
        self.assertFalse(any(step > 2 for _, step in submissions))
        saved.assert_awaited_once()
        self.assertEqual(len(saved.await_args.args[0]["specifications"]), 1)


    async def test_deadline_retries_only_the_affected_context_reduction_or_approval(self):
        phases = ["root_context", "root_reduce", "root_approval"]
        if chat.REDUCE_LEVELS == 2:
            phases.append("onelevel_reduce")
        for phase in phases:
            with self.subTest(phase=phase):
                result, submissions, requests, saved = await self.run_approval_failure(
                    3, target_phase=phase, deadline_failure=True,
                )
                self.assertEqual(len(requests), 4)
                self.assertTrue(all(request == requests[0] for request in requests))
                for step in range(1, 8):
                    self.assertEqual(submissions[("map", step)], 4)
                    for root_phase in ("root_context", "root_reduce", "root_approval"):
                        self.assertEqual(submissions[(root_phase, step)],
                                         4 if root_phase == phase and step == 2 else 1)
                    if chat.REDUCE_LEVELS == 2:
                        self.assertEqual(submissions[("onelevel_reduce", step)],
                                         5 if phase == "onelevel_reduce" and step == 2 else 2)
                self.assertEqual(len(result["specifications"]), 8)
                self.assertTrue(all(len(stage["attempts"]) == 1 for stage in result["hierarchy"]["stages"]))
                self.assertIsNone(result["specifications"][1]["usage"]["total_tokens"])
                self.assertIsNone(result["usage"]["total_tokens"])
                self.assertIsNotNone(result["specifications"][0]["usage"]["total_tokens"])
                self.assertIsNotNone(result["specifications"][2]["usage"]["total_tokens"])
                self.assertEqual([len(call.args[0]["specifications"]) for call in saved.await_args_list], list(range(1, 9)))

    async def test_deadline_exhaustion_keeps_completed_stages_and_stops_later_stages(self):
        result, submissions, requests, saved = await self.run_approval_failure(4, deadline_failure=True)
        self.assertIsNone(result)
        self.assertEqual(len(requests), 4)
        self.assertEqual(submissions[("map", 1)], 4)
        self.assertEqual(submissions[("map", 2)], 4)
        self.assertEqual(submissions[("root_reduce", 2)], 1)
        self.assertEqual(submissions[("root_approval", 2)], 4)
        self.assertFalse(any(step > 2 for _, step in submissions))
        saved.assert_awaited_once()
        self.assertEqual(len(saved.await_args.args[0]["specifications"]), 1)


if __name__ == "__main__":
    unittest.main()
