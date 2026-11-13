import asyncio
import copy
import json
import os
import re
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import httpx
from openai import RateLimitError

import test_upload
from server import application, chat, output_files, resume
from server.models import AppServices
from server.specifications import SPECIFICATION_STAGES, specification_result


class ResumeTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await test_upload.UploadTests.asyncSetUp(self)
        self.stage_sleep.side_effect = None

    asyncTearDown = test_upload.UploadTests.asyncTearDown

    def configure(self, completed=0, fail_at=None, failure=None):
        calls = []
        self.stage_sleep.reset_mock()

        async def create_response(**kwargs):
            step = int(re.search(r'^Stage: (\d+)/8$', kwargs['query'], re.M)[1])
            self.assertEqual(step, completed + len(calls) + 1)
            self.assertEqual(self.stage_sleep.await_count, len(calls))
            for previous in range(1, step):
                self.assertIn(f'Generated specification {previous}.', kwargs['query'])
            if step == 8:
                self.assertIsNone(kwargs['input_file'])
            else:
                self.assertIsNotNone(kwargs['input_file'])
            calls.append(step)
            if step == fail_at:
                raise failure if failure is not None else RuntimeError('Injected stage failure')
            return SimpleNamespace(output_text=f'Generated specification {step}.',
                                   usage=SimpleNamespace(input_tokens=10, output_tokens=20, total_tokens=30))

        self.services = AppServices(responses=SimpleNamespace(create_response=create_response))
        return calls

    async def upload(self, run_id=None, legacy=False, data=b'%PDF-source', filename='source.pdf'):
        fields = {}
        if run_id is not None:
            fields['resume_from'] = run_id
        if legacy:
            fields['allow_legacy_resume'] = 'true'
        return await self.client.post('/upload', files={'file': (filename, data)}, data=fields)

    def directories(self):
        return set((self.output_base / 'res').glob('*'))

    def snapshot(self, directory):
        return {path.name: (path.read_bytes(), path.stat().st_mtime_ns) for path in directory.iterdir()}

    def legacy_run(self, count):
        specs = [{'step': stage.step, 'key': stage.key, 'title': stage.title,
                  'content': f'# {stage.step}. {stage.title}\n\nGenerated specification {stage.step}.',
                  'usage': dict.fromkeys(resume.USAGE_KEYS), 'elapsed_ms': None}
                 for stage in SPECIFICATION_STAGES[:count]]
        writer = output_files.OutputFiles()
        writer.save(specification_result(specs), complete=False)
        return writer.directory

    async def partial_run(self, count, failure=None):
        self.configure(fail_at=count + 1, failure=failure)
        before = self.directories()
        if isinstance(failure, asyncio.CancelledError):
            with self.assertRaises(asyncio.CancelledError):
                await self.upload()
        else:
            response = await self.upload()
            self.assertEqual(response.status_code, 500, response.text)
        directory, = self.directories() - before
        state = json.loads((directory / resume.CHECKPOINT_NAME).read_bytes())
        self.assertEqual(len(state['specifications']), count)
        return directory, state

    async def test_rate_limit_after_first_specification_resumes_at_stage_two(self):
        error = RateLimitError('Token rate limit exceeded', body=None,
                              response=httpx.Response(429, request=httpx.Request('POST', 'https://example.test')))
        directory, checkpoint = await self.partial_run(1, error)
        original = self.snapshot(directory)
        calls = self.configure(completed=1)
        response = await self.upload(directory.name, filename='renamed.pdf')
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertEqual(calls, list(range(2, 9)))
        self.assertEqual(self.snapshot(directory), original)
        self.assertNotEqual(body['run_id'], directory.name)
        self.assertEqual(body['file_name'], checkpoint['file_name'])
        self.assertEqual(body['specifications'][0]['usage'], checkpoint['specifications'][0]['usage'])
        self.assertEqual(body['specifications'][0]['elapsed_ms'], checkpoint['specifications'][0]['elapsed_ms'])
        self.assertEqual(body['usage']['total_tokens'], 240)
        self.assertEqual(body['usage_scope'], 'completed_stages')
        self.assertEqual(body['resume']['reused_stages'], ['screen_functions'])
        self.assertEqual(body['resume']['unverified_stages'], [])
        self.assertEqual(body['resume']['history'], [directory.name])
        copied = self.output_base / 'res' / body['run_id'] / '01_screen_functions.md'
        self.assertEqual(copied.read_bytes(), original[copied.name][0])

    async def test_cancelled_run_and_repeated_failure_resume_from_latest_progress(self):
        original, _ = await self.partial_run(2, asyncio.CancelledError())
        self.configure(completed=2, fail_at=5)
        before = self.directories()
        response = await self.upload(original.name)
        self.assertEqual(response.status_code, 500)
        intermediate, = self.directories() - before
        state = json.loads((intermediate / resume.CHECKPOINT_NAME).read_bytes())
        self.assertEqual(len(state['specifications']), 4)
        calls = self.configure(completed=4)
        response = await self.upload(intermediate.name)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(calls, [5, 6, 7, 8])
        self.assertEqual(response.json()['resume']['history'], [original.name, intermediate.name])

    async def test_immediate_failure_keeps_copied_prefix_resumable(self):
        original = self.legacy_run(1)
        before = self.directories()
        self.configure(completed=1, fail_at=2)
        response = await self.upload(original.name, legacy=True)
        self.assertEqual(response.status_code, 500)
        intermediate, = self.directories() - before
        checkpoint = json.loads((intermediate / resume.CHECKPOINT_NAME).read_bytes())
        self.assertEqual(len(checkpoint['specifications']), 1)
        self.configure(completed=1)
        response = await self.upload(intermediate.name)
        self.assertEqual(response.status_code, 200, response.text)

    async def test_legacy_import_requires_same_opt_in_and_retains_unknown_usage(self):
        directory = self.legacy_run(1)
        original = self.snapshot(directory)
        calls = self.configure(completed=1)
        denied = await self.upload(directory.name)
        self.assertEqual(denied.status_code, 409)
        self.assertIn('allow_legacy_resume=true', denied.json()['detail'])
        self.assertEqual(calls, [])
        response = await self.upload(directory.name, legacy=True)
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertEqual(calls, list(range(2, 9)))
        self.assertEqual(self.snapshot(directory), original)
        self.assertEqual(body['usage'], dict.fromkeys(resume.USAGE_KEYS))
        self.assertIsNone(body['specifications'][0]['elapsed_ms'])
        self.assertEqual(body['resume']['unverified_stages'], ['screen_functions'])
        self.services = AppServices(responses=SimpleNamespace(create_response=AsyncMock(side_effect=AssertionError())))
        again = await self.upload(body['run_id'])
        self.assertEqual(again.status_code, 200, again.text)
        self.assertEqual(again.json()['specifications'], body['specifications'])
        self.assertEqual(again.json()['resume']['unverified_stages'], ['screen_functions'])

    async def test_stage_eight_and_completed_run_need_no_source_attachment(self):
        directory, _ = await self.partial_run(7)
        calls = self.configure(completed=7)
        with patch.object(chat, 'create_input_file', side_effect=AssertionError('Must not attach source')):
            response = await self.upload(directory.name)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(calls, [8])
        self.stage_sleep.assert_not_awaited()
        create = AsyncMock(side_effect=AssertionError('Must not call the model'))
        self.services = AppServices(responses=SimpleNamespace(create_response=create))
        with patch.object(chat, 'create_input_file', side_effect=AssertionError('Must not attach source')):
            finished = await self.upload(response.json()['run_id'])
        self.assertEqual(finished.status_code, 200, finished.text)
        self.assertEqual(finished.json()['specifications'], response.json()['specifications'])
        create.assert_not_awaited()

    async def test_pptx_legacy_run_resumes_with_original_binary_attachment(self):
        directory = self.legacy_run(6)
        calls = self.configure(completed=6)
        response = await self.upload(directory.name, legacy=True, data=b'PK-pptx-source', filename='source.pptx')
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(calls, [7, 8])

    async def test_input_settings_and_pipeline_mismatches_fail_before_generation(self):
        directory, state = await self.partial_run(1)
        with patch.object(application, 'generate_specifications', new_callable=AsyncMock) as generate:
            for data, filename in ((b'%PDF-other', 'source.pdf'), (b'%PDF-source', 'source.pptx')):
                response = await self.upload(directory.name, legacy=True, data=data, filename=filename)
                self.assertEqual(response.status_code, 409)
            for setting in resume.SETTINGS + ('AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME', 'AZURE_OPENAI_ENDPOINT'):
                with patch.dict(os.environ, {setting: 'changed-value'}):
                    response = await self.upload(directory.name)
                self.assertEqual(response.status_code, 409)
            state['identity']['pipeline_sha256'] = 'changed'
            (directory / resume.CHECKPOINT_NAME).write_text(json.dumps(state))
            response = await self.upload(directory.name, legacy=True)
            self.assertEqual(response.status_code, 409)
            generate.assert_not_awaited()
        self.assertEqual(self.directories(), {directory})

    async def test_corrupt_checkpoint_and_changed_or_missing_markdown_are_rejected(self):
        directory, state = await self.partial_run(1)
        marker = directory / resume.CHECKPOINT_NAME
        spec = directory / '01_screen_functions.md'
        original = spec.read_bytes()
        mutations = ['invalid JSON', json.dumps({**state, 'schema_version': 99}),
                     json.dumps({**state, 'specifications': []}),
                     json.dumps({**state, 'resume': {'history': '../bad'}})]
        for field, value in (('usage', {}), ('elapsed_ms', -1), ('step', 2), ('key', 'api')):
            broken = copy.deepcopy(state)
            broken['specifications'][0][field] = value
            mutations.append(json.dumps(broken))
        with patch.object(application, 'generate_specifications', new_callable=AsyncMock) as generate:
            for mutation in mutations:
                marker.write_text(mutation)
                response = await self.upload(directory.name, legacy=True)
                self.assertEqual(response.status_code, 400, response.text)
            marker.write_text(json.dumps(state))
            spec.write_bytes(b'Edited specification\n')
            response = await self.upload(directory.name)
            self.assertEqual(response.status_code, 400)
            spec.write_bytes(original)
            spec.unlink()
            response = await self.upload(directory.name)
            self.assertEqual(response.status_code, 400)
            generate.assert_not_awaited()

    async def test_unsafe_paths_empty_and_gapped_legacy_runs_are_rejected(self):
        directory = self.legacy_run(3)
        with patch.object(application, 'generate_specifications', new_callable=AsyncMock) as generate:
            for run_id in ('../escape', str(directory), 'twolevel_20261111082915_abc', ''):
                response = await self.upload(run_id, legacy=True)
                self.assertEqual(response.status_code, 400, response.text)
            response = await self.upload('fullload_20261111082915_absent')
            self.assertEqual(response.status_code, 404)
            response = await self.upload(legacy=True)
            self.assertEqual(response.status_code, 400)
            alias = directory.parent / 'fullload_20261111082915_alias'
            alias.symlink_to(directory, target_is_directory=True)
            response = await self.upload(alias.name, legacy=True)
            self.assertEqual(response.status_code, 400)
            (directory / '02_api.md').unlink()
            response = await self.upload(directory.name, legacy=True)
            self.assertEqual(response.status_code, 400)
            (directory / '03_data.md').unlink()
            spec = directory / '01_screen_functions.md'
            for data in (b' \n', b'\xff', b'x' * 100):
                spec.write_bytes(data)
                with patch.object(resume, 'MAX_MARKDOWN_BYTES', 50):
                    response = await self.upload(directory.name, legacy=True)
                self.assertEqual(response.status_code, 400)
            spec.unlink()
            response = await self.upload(directory.name, legacy=True)
            self.assertEqual(response.status_code, 400)
            spec.symlink_to(directory / 'missing')
            response = await self.upload(directory.name, legacy=True)
            self.assertEqual(response.status_code, 400)
            generate.assert_not_awaited()

    async def test_checkpoint_commit_failure_preserves_previous_prefix_and_ignores_orphans(self):
        directory, checkpoint = await self.partial_run(2)
        identity = checkpoint['identity']
        state = resume.load_resume(directory.parent, directory.name, identity)
        payload = {**specification_result(state['specifications']), 'file_name': state['file_name']}
        writer = output_files.OutputFiles(identity=identity)
        writer.save(payload, complete=False)
        original = self.snapshot(writer.directory)
        next_payload = copy.deepcopy(payload)
        next_payload['specifications'].append({**next_payload['specifications'][-1],
                                              'step': 3, 'key': 'data', 'title': 'Data Specification'})
        replace = Path.replace

        def fail_marker(source, target):
            if Path(target).name == resume.CHECKPOINT_NAME:
                raise OSError('Injected checkpoint failure')
            return replace(source, target)

        with patch.object(Path, 'replace', fail_marker), self.assertRaisesRegex(OSError, 'checkpoint failure'):
            writer.save(next_payload, complete=False)
        self.assertEqual(self.snapshot(writer.directory), original)
        (writer.directory / '03_data.md').write_text('Uncommitted draft\n')
        restored = resume.load_resume(writer.directory.parent, writer.directory.name, identity)
        self.assertEqual(restored['specifications'], state['specifications'])

    async def test_resume_still_requires_authentication(self):
        directory = self.legacy_run(1)
        with patch.object(application, 'generate_specifications', new_callable=AsyncMock) as generate:
            response = await self.client.post('/upload', headers={'Authorization': 'Bearer wrong'},
                                              files={'file': ('source.pdf', b'%PDF-source')},
                                              data={'resume_from': directory.name, 'allow_legacy_resume': 'true'})
            self.assertEqual(response.status_code, 401)
            generate.assert_not_awaited()


if __name__ == '__main__':
    unittest.main()
