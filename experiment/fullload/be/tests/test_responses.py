import base64
import json
import unittest
from unittest.mock import AsyncMock, patch

import httpx
from openai import AsyncAzureOpenAI

from plugins.talks_with_responses.talks_with_responses import TalksWithResponses
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
                    result = await self.plugin.create_response(
                        "Review attachment", "Review instructions", create_input_file(data, filename), max_output_tokens=128000,
                    )
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
                self.assertEqual(payload["max_output_tokens"], 128000)
                self.assertTrue(any("max_output_tokens=128000" in line for line in logs.output))
                self.assertEqual(result.output_text, "確認結果")
                self.assertTrue(any("input_tokens=10 output_tokens=3 total_tokens=13" in line for line in logs.output))

    async def test_text_only_synthesis_does_not_attach_file(self):
        await self.plugin.create_response("Merge reviews", "Instructions")
        payload = json.loads(self.requests[-1].content)
        self.assertEqual(payload["input"][0]["content"], [{"type": "input_text", "text": "Merge reviews"}])

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


if __name__ == "__main__":
    unittest.main()
