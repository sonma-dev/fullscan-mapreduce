import asyncio
import copy
import json
import os
import re
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import test_upload
from test_chat import FakeResponses
from test_file_chunks import make_deck
from server import application, chat, hierarchy, output_files, resume
from server.models import AppServices
from server.specifications import SPECIFICATION_STAGES, specification_result


class ResumeTests(unittest.IsolatedAsyncioTestCase):
    asyncSetUp = test_upload.UploadTests.asyncSetUp
    asyncTearDown = test_upload.UploadTests.asyncTearDown

    def configure(self, completed=0, fail_at=None, cancellation=False, response_type=FakeResponses):
        fake = response_type(self)
        fake.approved = list(range(1, completed + 1))

        async def create_response(**kwargs):
            match = re.search(r'^Stage: (\d+)/8$', kwargs['query'], re.M)
            if match and int(match[1]) == fail_at:
                if cancellation:
                    raise asyncio.CancelledError()
                raise RuntimeError('Injected stage failure')
            return await fake.create_response(**kwargs)

        self.services = AppServices(responses=SimpleNamespace(create_response=create_response))
        return fake

    async def upload(self, data, run_id=None, legacy=False, filename='source.pptx'):
        fields = {}
        if run_id is not None:
            fields['resume_from'] = run_id
        if legacy:
            fields['allow_legacy_resume'] = 'true'
        with patch.dict(os.environ, {'FILE_CHUNK_MAX_SLIDES': '1'}):
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

    async def partial_run(self, count, data=None, cancellation=False):
        data = make_deck(2) if data is None else data
        self.configure(fail_at=count + 1, cancellation=cancellation)
        before = self.directories()
        if cancellation:
            with self.assertRaises(asyncio.CancelledError):
                await self.upload(data)
        else:
            response = await self.upload(data)
            self.assertEqual(response.status_code, 500, response.text)
        directory, = self.directories() - before
        state = json.loads((directory / resume.CHECKPOINT_NAME).read_bytes())
        self.assertEqual(len(state['specifications']), count)
        return data, directory, state

    async def test_resume_restores_context_approved_prefix_usage_and_audits(self):
        data, directory, checkpoint = await self.partial_run(2)
        original = self.snapshot(directory)
        fake = self.configure(completed=2)
        response = await self.upload(data, directory.name, filename='renamed.pptx')
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertEqual(self.snapshot(directory), original)
        self.assertNotEqual(body['run_id'], directory.name)
        self.assertEqual(body['file_name'], checkpoint['file_name'])
        self.assertFalse(any(phase == 'global_context' or step < 3 for phase, step, _ in fake.calls))
        self.assertEqual(body['hierarchy']['global_context'], checkpoint['hierarchy']['global_context'])
        self.assertEqual(body['hierarchy']['stages'][:2], checkpoint['hierarchy']['stages'])
        self.assertEqual(len(body['hierarchy']['stages']), 7)
        self.assertEqual(body['resume']['unverified_stages'], [])
        self.assertEqual(body['resume']['history'], [directory.name])
        self.assertEqual(body['usage']['total_tokens'], sum(s['usage']['total_tokens'] for s in body['specifications'])
                         + checkpoint['hierarchy']['context_usage']['total_tokens'])
        for stage in SPECIFICATION_STAGES[:2]:
            name = f'{stage.step:02d}_{stage.key}.md'
            self.assertEqual((self.output_base / 'res' / body['run_id'] / name).read_bytes(), original[name][0])

    async def test_cancelled_run_resumes_and_a_second_failure_preserves_new_progress(self):
        data, original, _ = await self.partial_run(2, cancellation=True)
        self.configure(completed=2, fail_at=5)
        before = self.directories()
        response = await self.upload(data, original.name)
        self.assertEqual(response.status_code, 500)
        intermediate, = self.directories() - before
        state = json.loads((intermediate / resume.CHECKPOINT_NAME).read_bytes())
        self.assertEqual(len(state['specifications']), 4)
        fake = self.configure(completed=4)
        response = await self.upload(data, intermediate.name)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertTrue(all(step >= 5 for _, step, _ in fake.calls))
        self.assertEqual(response.json()['resume']['history'], [original.name, intermediate.name])

    async def test_pdf_resume_preserves_chapter_sections_regions_and_plan(self):
        from test_pdf_hierarchy import PDFResponses
        from test_pdf_sections import make_pdf

        data = make_pdf()
        self.configure(fail_at=3, response_type=PDFResponses)
        response = await self.upload(data, filename='chapters.pdf')
        self.assertEqual(response.status_code, 500)
        directory, = self.directories()
        checkpoint = json.loads((directory / resume.CHECKPOINT_NAME).read_bytes())
        fake = self.configure(completed=2, response_type=PDFResponses)
        response = await self.upload(data, directory.name, filename='renamed.pdf')
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()['chunks'], checkpoint['chunks'])
        self.assertEqual(len({chunk['chapter_id'] for chunk in response.json()['chunks']}), 2)
        self.assertTrue(all(step >= 3 for _, step, _ in fake.calls))

    async def test_only_stage_eight_needs_no_split_or_hierarchy_calls_and_completed_run_needs_no_llm(self):
        data, directory, _ = await self.partial_run(7)
        fake = self.configure(completed=7)
        with patch.object(hierarchy, 'split_file', side_effect=AssertionError('Must not split')):
            response = await self.upload(data, directory.name)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual([(phase, step) for phase, step, _ in fake.calls], [('decision_register', 8)])
        create = AsyncMock(side_effect=AssertionError('Must not call the model'))
        self.services = AppServices(responses=SimpleNamespace(create_response=create))
        with patch.object(hierarchy, 'split_file', side_effect=AssertionError('Must not split')):
            finished = await self.upload(data, response.json()['run_id'])
        self.assertEqual(finished.status_code, 200, finished.text)
        self.assertEqual(finished.json()['specifications'], response.json()['specifications'])
        create.assert_not_awaited()

    async def test_legacy_import_requires_opt_in_and_keeps_unknown_usage_and_provenance(self):
        directory = self.legacy_run(4)
        original = self.snapshot(directory)
        data = make_deck(2)
        self.configure(completed=4)
        denied = await self.upload(data, directory.name)
        self.assertEqual(denied.status_code, 409)
        self.assertIn('allow_legacy_resume=true', denied.json()['detail'])
        fake = self.configure(completed=4)
        response = await self.upload(data, directory.name, legacy=True)
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertEqual(self.snapshot(directory), original)
        self.assertEqual([phase for phase, step, _ in fake.calls if step == 0], ['global_context'])
        self.assertTrue(all(step == 0 or step >= 5 for _, step, _ in fake.calls))
        self.assertEqual(body['usage'], dict.fromkeys(resume.USAGE_KEYS))
        self.assertEqual(body['resume']['unverified_stages'], [s.key for s in SPECIFICATION_STAGES[:4]])
        self.assertTrue(all(spec['elapsed_ms'] is None for spec in body['specifications'][:4]))
        self.services = AppServices(responses=SimpleNamespace(create_response=AsyncMock(side_effect=AssertionError())))
        again = await self.upload(data, body['run_id'])
        self.assertEqual(again.status_code, 200, again.text)
        self.assertEqual(again.json()['resume']['unverified_stages'], body['resume']['unverified_stages'])

    async def test_legacy_stage_eight_import_also_skips_global_context(self):
        directory = self.legacy_run(7)
        fake = self.configure(completed=7)
        with patch.object(hierarchy, 'split_file', side_effect=AssertionError('Must not split')):
            response = await self.upload(b'%PDF-placeholder', directory.name, legacy=True, filename='source.pdf')
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual([(phase, step) for phase, step, _ in fake.calls], [('decision_register', 8)])
        self.assertIsNone(response.json()['hierarchy']['global_context'])

    async def test_mismatches_and_corruption_fail_before_generation(self):
        data, directory, checkpoint = await self.partial_run(2)
        marker = directory / resume.CHECKPOINT_NAME
        original_marker = marker.read_bytes()
        spec_path = directory / '01_screen_functions.md'
        original_spec = spec_path.read_bytes()
        with patch.object(application, 'generate_specifications', new_callable=AsyncMock) as generate:
            wrong_source = await self.upload(make_deck(3), directory.name, legacy=True)
            self.assertEqual(wrong_source.status_code, 409)
            with patch.dict(os.environ, {'LLM_MAX_OUTPUT_TOKENS': '1234'}):
                settings = await self.upload(data, directory.name)
            self.assertEqual(settings.status_code, 409)
            spec_path.write_bytes(b'Edited specification\n')
            changed = await self.upload(data, directory.name)
            self.assertEqual(changed.status_code, 400)
            spec_path.write_bytes(original_spec)
            for mutation in ('invalid JSON', json.dumps({**checkpoint, 'schema_version': 99}),
                             json.dumps({**checkpoint, 'hierarchy': {}})):
                marker.write_text(mutation)
                response = await self.upload(data, directory.name, legacy=True)
                self.assertEqual(response.status_code, 400, response.text)
            marker.write_bytes(original_marker)
            spec_path.unlink()
            missing = await self.upload(data, directory.name)
            self.assertEqual(missing.status_code, 400)
            generate.assert_not_awaited()
        self.assertEqual(self.directories(), {directory})

    async def test_unsafe_paths_symlinks_empty_and_gapped_legacy_are_rejected(self):
        directory = self.legacy_run(3)
        data = make_deck(2)
        with patch.object(application, 'generate_specifications', new_callable=AsyncMock) as generate:
            for run_id in ('../escape', str(directory), 'onelevel_20261111082915_abc', ''):
                response = await self.upload(data, run_id, legacy=True)
                self.assertEqual(response.status_code, 400, response.text)
            response = await self.upload(data, 'twolevel_20261111082915_absent')
            self.assertEqual(response.status_code, 404)
            alias = directory.parent / 'twolevel_20261111082915_alias'
            alias.symlink_to(directory, target_is_directory=True)
            response = await self.upload(data, alias.name, legacy=True)
            self.assertEqual(response.status_code, 400)
            (directory / '02_api.md').unlink()
            response = await self.upload(data, directory.name, legacy=True)
            self.assertEqual(response.status_code, 400)
            (directory / '03_data.md').unlink()
            (directory / '01_screen_functions.md').write_text(' \n')
            response = await self.upload(data, directory.name, legacy=True)
            self.assertEqual(response.status_code, 400)
            (directory / '01_screen_functions.md').unlink()
            (directory / '01_screen_functions.md').symlink_to(directory / 'not-present')
            response = await self.upload(data, directory.name, legacy=True)
            self.assertEqual(response.status_code, 400)
            generate.assert_not_awaited()

    async def test_checkpoint_commit_failure_rolls_back_only_new_markdown_and_orphans_are_not_reused(self):
        data, directory, checkpoint = await self.partial_run(2)
        identity = checkpoint['identity']
        state = resume.load_resume(directory.parent, directory.name, identity)
        payload = {**specification_result(state['specifications']), 'file_name': state['file_name'],
                   'chunks': state['chunks'], 'hierarchy': state['hierarchy']}
        writer = output_files.OutputFiles(identity=identity)
        writer.save(payload, complete=False)
        original = self.snapshot(writer.directory)
        next_payload = copy.deepcopy(payload)
        next_spec = {**next_payload['specifications'][-1], 'step': 3, 'key': 'data', 'title': 'Data'}
        next_payload['specifications'].append(next_spec)
        replace = Path.replace

        def fail_marker(source, target):
            if Path(target).name == resume.CHECKPOINT_NAME:
                raise OSError('Injected checkpoint failure')
            return replace(source, target)

        with patch.object(Path, 'replace', fail_marker), self.assertRaisesRegex(OSError, 'checkpoint failure'):
            writer.save(next_payload, complete=False)
        self.assertEqual(self.snapshot(writer.directory), original)
        # Simulate a crash after an .md rename, before its checkpoint commit.
        (writer.directory / '03_data.md').write_text('Uncommitted draft\n')
        restored = resume.load_resume(writer.directory.parent, writer.directory.name, identity)
        self.assertEqual(len(restored['specifications']), 2)
        self.assertEqual(restored['specifications'], state['specifications'])

    async def test_resume_authentication_and_busy_gate_still_apply(self):
        directory = self.legacy_run(1)
        with patch.object(application, 'load_resume') as load:
            response = await self.client.post('/upload', headers={'Authorization': 'Bearer invalid'},
                                              data={'resume_from': directory.name}, files={'file': ('source.pdf', b'data')})
            self.assertEqual(response.status_code, 401)
            await self.services.analysis_slot.acquire()
            try:
                response = await self.client.post('/upload', data={'resume_from': directory.name},
                                                  files={'file': ('source.pdf', b'data')})
                self.assertEqual(response.status_code, 503)
            finally:
                self.services.analysis_slot.release()
            load.assert_not_called()

    async def test_invalid_in_memory_prefix_is_rejected_before_splitting(self):
        with patch.object(hierarchy, 'split_file', side_effect=AssertionError('Must not split')):
            with self.assertRaises(ValueError):
                await chat.generate_specifications(self.services, b'data', 'source.pdf',
                    resume_state={'specifications': [{'step': 2, 'key': 'api', 'content': 'Body'}]})

    async def test_identity_checks_prompts_and_model_but_excludes_credentials_and_port(self):
        backend = self.output_base / 'backend'
        (backend / 'prompt').mkdir(parents=True)
        (backend / 'requirements.txt').write_text('dependency==1\n')
        prompt = backend / 'prompt' / 'test.jinja2'
        prompt.write_text('First prompt')
        with patch.object(resume, 'BACKEND_DIR', backend):
            original = resume.run_identity(b'source', 'source.pdf')
            with patch.dict(os.environ, {'AZURE_OPENAI_API_KEY': 'do-not-store', 'API_KEY': 'private', 'PORT': '9999'}):
                self.assertEqual(resume.run_identity(b'source', 'renamed.pdf'), original)
            with patch.dict(os.environ, {'AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME': 'another-model'}):
                self.assertNotEqual(resume.run_identity(b'source', 'source.pdf'), original)
            prompt.write_text('Second prompt')
            changed = resume.run_identity(b'source', 'source.pdf')
            self.assertNotEqual(changed['pipeline_sha256'], original['pipeline_sha256'])


if __name__ == '__main__':
    unittest.main()
