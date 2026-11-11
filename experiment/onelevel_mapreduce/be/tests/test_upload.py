import asyncio
import os
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import httpx

os.environ.setdefault("API_KEY", "test-key-for-upload-authentication-123456789")
from server import application, output_files
from server.models import AppServices
from server.security import API_KEY
from server.services import get_services
from server.specifications import SPECIFICATION_STAGES


class UploadTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.output_base = Path(temporary.name)
        output_patch = patch.object(output_files, 'OUTPUT_DIR', self.output_base / 'res')
        output_patch.start()
        self.addCleanup(output_patch.stop)
        self.services = AppServices(responses=SimpleNamespace())
        app = application.create_app()
        app.dependency_overrides[get_services] = lambda: self.services
        self.client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver",
            headers={"Authorization": f"Bearer {API_KEY}"},
        )

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_upload_passes_binary_file_and_logs_total_usage(self):
        usage = {"input_tokens": 123, "output_tokens": 45, "total_tokens": 168}
        specifications = [{"step": stage.step, "key": stage.key, "title": stage.title,
                           "content": f"仕様本文{stage.step}", "usage": usage, "elapsed_ms": 1}
                          for stage in SPECIFICATION_STAGES]
        review = {"reply": "仕様書", "specifications": specifications, "usage": usage, "chunks": [], "hierarchy": {"reduce_levels": 1, "stages": []}}
        with patch.object(application, "generate_specifications", new_callable=AsyncMock, return_value=review) as examine:
            with self.assertLogs("server.application", level="INFO") as logs:
                response = await self.client.post("/upload", files={"file": ("sample.pdf", b"%PDF-test\x00\xff", "application/pdf")})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(examine.call_args.kwargs["file_bytes"], b"%PDF-test\x00\xff")
        self.assertEqual(response.json()["usage"], usage)
        self.assertEqual(response.json()["request"], "generate_specifications")
        self.assertEqual(response.json()["specifications"], specifications)
        files = response.json()['output_files']
        self.assertEqual(set(files), {"markdown"})
        directory = (self.output_base / files['markdown'][0]).parent
        self.assertEqual(directory.parent, self.output_base / 'res')
        self.assertTrue(directory.name.startswith(output_files.OUTPUT_PREFIX + '_'))
        self.assertEqual({path.suffix for path in directory.iterdir()}, {'.md'})
        self.assertEqual(Path(files['markdown'][-1]).name, '08_architecture_decision.md')
        self.assertEqual(len(files['markdown']), 8)
        for specification, filename in zip(specifications, files['markdown']):
            self.assertEqual((self.output_base / filename).read_text(encoding='utf-8'), specification['content'] + '\n')
        self.assertEqual(response.json()["hierarchy"], review["hierarchy"])
        self.assertEqual(set(response.json()["timing_ms"]), {"llm", "total"})
        self.assertNotIn("markdown", response.json())
        self.assertTrue(any("input_tokens=123 output_tokens=45 total_tokens=168" in line for line in logs.output))

    async def test_missing_usage_is_logged_without_format_error(self):
        usage = dict.fromkeys(("input_tokens", "output_tokens", "total_tokens"))
        with patch.object(application, "generate_specifications", new_callable=AsyncMock, return_value={"reply": "仕様書", "specifications": [], "usage": usage, "chunks": [], "hierarchy": {"reduce_levels": 1, "stages": []}}):
            with self.assertLogs("server.application", level="INFO") as logs:
                response = await self.client.post("/upload", files={"file": ("sample.pdf", b"%PDF-test")})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["usage"], usage)
        self.assertTrue(any("input_tokens=None output_tokens=None total_tokens=None" in line for line in logs.output))

    async def test_invalid_uploads_are_rejected_before_llm(self):
        with patch.object(application, "generate_specifications", new_callable=AsyncMock) as examine:
            for filename, data, status in (("empty.pdf", b"", 400), ("image.exe", b"data", 415), ("bad%2Fname.pdf", b"data", 400)):
                response = await self.client.post("/upload", files={"file": (filename, data)})
                self.assertEqual(response.status_code, status)
            with patch.object(application, "MAX_BYTES", 4), patch("server.input_files.MAX_BYTES", 4):
                response = await self.client.post("/upload", files={"file": ("large.pdf", b"12345")})
                self.assertEqual(response.status_code, 413)
            examine.assert_not_called()

    async def test_authentication_still_required(self):
        response = await self.client.post("/upload", headers={"Authorization": "Bearer wrong"}, files={"file": ("sample.pdf", b"data")})
        self.assertEqual(response.status_code, 401)

    async def test_concurrent_analysis_is_rejected_before_expanding_files(self):
        await self.services.analysis_slot.acquire()
        try:
            with patch.object(application, 'generate_specifications', new_callable=AsyncMock) as generate:
                response = await self.client.post('/upload', files={'file': ('sample.pdf', b'data')})
                self.assertEqual(response.status_code, 503)
                self.assertEqual(response.headers['retry-after'], '10')
                generate.assert_not_called()
        finally:
            self.services.analysis_slot.release()

    async def test_analysis_slot_is_released_after_failure(self):
        with patch.object(application, 'generate_specifications', side_effect=RuntimeError('failed')):
            response = await self.client.post('/upload', files={'file': ('sample.pdf', b'%PDF-test')})
        self.assertEqual(response.status_code, 500)
        self.assertFalse(self.services.analysis_slot.locked())

    def assert_saved_stages(self, count, specifications=None):
        directories = list((self.output_base / "res").glob("*"))
        if count == 0:
            self.assertEqual(directories, [])
            return
        self.assertEqual(len(directories), 1)
        paths = sorted(directories[0].iterdir())
        self.assertEqual([path.name for path in paths], [
            f"{stage.step:02d}_{stage.key}.md" for stage in SPECIFICATION_STAGES[:count]
        ])
        for step, path in enumerate(paths, 1):
            self.assertIn(f"Generated specification {step}.", path.read_text(encoding="utf-8"))
        if specifications is not None:
            for path, spec in zip(paths, specifications):
                self.assertEqual(path.read_text(encoding="utf-8"), spec["content"] + "\n")

    async def run_incremental_upload(self, failure=None, failure_step=3):
        from test_chat import FakeResponses
        from test_file_chunks import make_deck

        fake = FakeResponses(self)
        data = make_deck(2)
        model_response = fake.create_response

        observed_step = 0

        async def create_response(**kwargs):
            nonlocal observed_step
            match = re.search(r"^Stage: (\d+)/8$", kwargs["query"], re.M)
            step = int(match[1]) if match else 0
            if step > observed_step:
                observed_step = step
                self.assert_saved_stages(step - 1)
                if step == failure_step and failure is not None:
                    raise failure
            return await model_response(**kwargs)

        self.services = AppServices(responses=SimpleNamespace(create_response=create_response))
        with patch.dict(os.environ, {"FILE_CHUNK_MAX_SLIDES": "1"}):
            return await self.client.post("/upload", files={"file": ("sample.pptx", data)})

    async def test_completed_markdown_is_saved_before_next_stage_and_matches_response(self):
        with self.assertLogs("server", level="INFO") as logs:
            response = await self.run_incremental_upload()
        self.assertEqual(response.status_code, 200)
        self.assert_saved_stages(8, response.json()["specifications"])
        self.assertEqual(response.json()["status"], "completed")
        self.assertEqual(len(response.json()["output_files"]["markdown"]), 8)
        self.assertEqual(sum("Stage output saved:" in line for line in logs.output), 8)
        self.assertTrue(any("completed=2/8" in line and str(self.output_base / "res") in line for line in logs.output))

    async def test_architecture_decision_failure_preserves_all_seven_specifications(self):
        with self.assertLogs(level="INFO"):
            response = await self.run_incremental_upload(RuntimeError("Decision register failed"), failure_step=8)
        self.assertEqual(response.status_code, 500)
        self.assert_saved_stages(7)

    async def test_stage_three_failure_preserves_first_two_stages(self):
        with self.assertLogs(level="INFO"):
            response = await self.run_incremental_upload(RuntimeError("Stage three failed"))
        self.assertEqual(response.status_code, 500)
        self.assert_saved_stages(2)

    async def test_stage_three_cancellation_preserves_first_two_stages(self):
        with self.assertLogs(level="INFO"):
            with self.assertRaises(asyncio.CancelledError):
                await self.run_incremental_upload(asyncio.CancelledError())
        self.assert_saved_stages(2)

if __name__ == "__main__":
    unittest.main()
