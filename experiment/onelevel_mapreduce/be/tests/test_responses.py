import asyncio
import base64
import json
import unittest
from unittest.mock import AsyncMock, patch

import httpx
from openai import AsyncAzureOpenAI

from plugins.talks_with_responses.talks_with_responses import TalksWithResponses
from plugins.talks_with_responses import talks_with_responses as responses_plugin
from server.input_files import create_input_file


class ResponsesTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.requests = []
        self.statuses = ["completed"]

        def handle(request):
            self.requests.append(request)
            status = self.statuses.pop(0)
            return httpx.Response(200, json={
                "id": "resp_test", "object": "response", "created_at": 1,
                "model": "test-model", "status": status,
                "output": [{"type": "message", "id": "msg_test", "role": "assistant", "status": "completed",
                            "content": [{"type": "output_text", "text": "確認結果", "annotations": []}]}],
                "usage": {"input_tokens": 10, "output_tokens": 3, "total_tokens": 13,
                          "input_tokens_details": {"cached_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 0}},
                "incomplete_details": {"reason": "max_output_tokens"} if status == "incomplete" else None,
            })

        client = AsyncAzureOpenAI(
            azure_endpoint="https://example.openai.azure.com", api_version="2025-03-01-preview",
            api_key="test-key", http_client=httpx.AsyncClient(transport=httpx.MockTransport(handle)),
        )
        with patch("plugins.talks_with_responses.talks_with_responses.AsyncAzureOpenAI", return_value=client):
            self.plugin = TalksWithResponses("https://example.openai.azure.com", lambda: "test-key", "test-model", "api_key")

    async def asyncTearDown(self):
        await self.plugin.close()

    async def test_file_bytes_reach_sdk_request_and_usage_is_logged(self):
        for filename, mime in (("sample.pdf", "application/pdf"), ("sample.PPTX", "application/vnd.openxmlformats-officedocument.presentationml.presentation")):
            with self.subTest(filename=filename):
                self.statuses = ["completed"]
                data = b"binary file\x00\xff\n"
                with self.assertLogs("plugins.talks_with_responses.talks_with_responses", level="INFO") as logs:
                    result = await self.plugin.create_response("Review attachment", "Review instructions", create_input_file(data, filename))
                payload = json.loads(self.requests[-1].content)
                self.assertEqual(payload["input"][0]["content"][0], {"type": "input_text", "text": "Review attachment"})
                attachment = payload["input"][0]["content"][1]
                self.assertEqual(attachment["type"], "input_file")
                self.assertEqual(attachment["filename"], filename)
                header, encoded = attachment["file_data"].split(",", 1)
                self.assertEqual(header, f"data:{mime};base64")
                self.assertEqual(base64.b64decode(encoded), data)
                self.assertTrue(payload["background"])
                self.assertEqual(payload["truncation"], "disabled")
                self.assertEqual(result.output_text, "確認結果")
                self.assertTrue(any("input_tokens=10 output_tokens=3 total_tokens=13" in line for line in logs.output))

    async def test_text_only_synthesis_does_not_attach_file(self):
        await self.plugin.create_response("Merge reviews", "Instructions")
        payload = json.loads(self.requests[-1].content)
        self.assertEqual(payload["input"][0]["content"], [{"type": "input_text", "text": "Merge reviews"}])

    async def test_intermediate_json_and_output_budget_reach_responses_api(self):
        for limit in (64000, 128000):
            with self.subTest(limit=limit):
                self.statuses = ['completed']
                with self.assertLogs('plugins.talks_with_responses.talks_with_responses', level='INFO') as logs:
                    await self.plugin.create_response('Return JSON evidence', 'Instructions', max_output_tokens=limit, json_output=True)
                payload = json.loads(self.requests[-1].content)
                self.assertEqual(payload['max_output_tokens'], limit)
                self.assertEqual(payload['text']['format'], {'type': 'json_object'})
                self.assertTrue(any(f'max_output_tokens={limit}' in line for line in logs.output))

    async def test_background_response_is_polled_to_completion(self):
        self.statuses = ["queued", "in_progress", "completed"]
        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await self.plugin.create_response("Review", "Instructions")
        self.assertEqual(result.status, "completed")
        self.assertEqual([r.method for r in self.requests], ["POST", "GET", "GET"])
        self.assertTrue(self.requests[-1].url.path.endswith("/responses/resp_test"))

    async def test_incomplete_response_is_not_returned_as_success(self):
        self.statuses = ["incomplete"]
        with self.assertRaisesRegex(RuntimeError, "incomplete.*max_output_tokens"):
            await self.plugin.create_response("Review", "Instructions")

    async def cancel_during_polling(self):
        polling = asyncio.Event()

        async def wait_for_cancellation(_):
            polling.set()
            await asyncio.Event().wait()

        self.plugin._slots = asyncio.Semaphore(1)
        with patch('asyncio.sleep', side_effect=wait_for_cancellation):
            task = asyncio.create_task(self.plugin.create_response('Review', 'Instructions'))
            try:
                await asyncio.wait_for(polling.wait(), 10)
            finally:
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await asyncio.wait_for(task, 1)

    async def assert_slot_released(self):
        self.statuses = ['completed']
        result = await asyncio.wait_for(self.plugin.create_response('Next request', 'Instructions'), 1)
        self.assertEqual(result.status, 'completed')

    async def test_cancelled_polling_cancels_remote_response_and_releases_slot(self):
        self.statuses = ['in_progress', 'cancelled']
        await self.cancel_during_polling()
        self.assertEqual([request.method for request in self.requests], ['POST', 'POST'])
        self.assertTrue(self.requests[-1].url.path.endswith('/responses/resp_test/cancel'))
        await self.assert_slot_released()

    async def test_remote_cancellation_timeout_is_bounded_and_preserves_caller_cancellation(self):
        self.statuses = ['in_progress']

        async def hang(*args, **kwargs):
            await asyncio.Event().wait()

        with patch.object(responses_plugin, 'BACKGROUND_CANCEL_TIMEOUT_SECONDS', 0.02), patch(
            'openai.resources.responses.responses.AsyncResponses.cancel', side_effect=hang,
        ) as cancel:
            with self.assertLogs('plugins.talks_with_responses.talks_with_responses', level='INFO') as logs:
                await self.cancel_during_polling()
        cancel.assert_awaited_once_with('resp_test')
        self.assertTrue(any('Responses cancellation failed:' in line for line in logs.output))
        await self.assert_slot_released()


if __name__ == "__main__":
    unittest.main()
