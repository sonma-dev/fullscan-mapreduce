import asyncio
import unittest
from unittest.mock import patch

from server import chat
from server.models import AppServices
from test_file_chunks import make_deck
from test_map_requests import ControlledResponses


class ChapterPipelineTests(unittest.IsolatedAsyncioTestCase):
    async def generate(self, fake, saved):
        async def save(result):
            saved.append(result)

        with patch.dict('os.environ', {
            'FILE_CHUNK_MAX_SLIDES': '1',
            'LLM_MAX_PARALLEL_LEVEL1_REQUESTS': '2',
            'LLM_MAX_PARALLEL_LEVEL2_REQUESTS': '4',
            'LLM_CHAPTER_BATCH_MAX_BYTES': '',
            'LLM_CHAPTER_INPUT_TOKEN_BUDGET': '',
            'LLM_MAP_INPUT_TOKEN_BUDGET': '',
        }):
            return await chat.generate_specifications(
                AppServices(responses=fake), make_deck(4), 'sample.pptx', on_stage_completed=save,
            )

    async def test_chapter_reduces_before_other_maps_finish_and_root_waits_for_all_chapters(self):
        second_map_done = asyncio.Event()
        last_map_started, release_last_map = asyncio.Event(), asyncio.Event()
        first_chapter_started, release_first_chapter = asyncio.Event(), asyncio.Event()
        second_chapter_done = asyncio.Event()
        contexts, completed_maps, completed_chapters = set(), set(), set()

        async def before(phase, step, payload):
            if step != 1:
                return
            if phase == 'map':
                self.assertEqual(contexts, {1, 3})
                chunk = payload['chunk']['index']
                if chunk == 1:
                    # Force completion order to differ from source order.
                    await second_map_done.wait()
                elif chunk == 4:
                    last_map_started.set()
                    await release_last_map.wait()
            elif phase == 'onelevel_reduce':
                members = payload['jurisdiction']['chunk_ids']
                self.assertTrue(set(members) <= completed_maps)
                self.assertEqual([child['chunk_id'] for child in payload['children']], members)
                if members == [1, 2]:
                    self.assertNotIn(4, completed_maps)
                    first_chapter_started.set()
                    await release_first_chapter.wait()
            elif phase in ('root_reduce', 'root_approval'):
                self.assertEqual(completed_maps, {1, 2, 3, 4})
                self.assertEqual(completed_chapters, {1, 3})

        def after(phase, step, payload):
            if step != 1:
                return
            if phase == 'onelevel_context':
                contexts.add(payload['jurisdiction']['chunk_ids'][0])
            elif phase == 'map':
                chunk = payload['chunk']['index']
                completed_maps.add(chunk)
                if chunk == 2:
                    second_map_done.set()
            elif phase == 'onelevel_reduce':
                chapter = payload['jurisdiction']['chunk_ids'][0]
                completed_chapters.add(chapter)
                if chapter == 3:
                    second_chapter_done.set()

        fake = ControlledResponses(self, before, after)
        saved = []
        with self.assertLogs('server', level='INFO'):
            task = asyncio.create_task(self.generate(fake, saved))
            try:
                await asyncio.wait_for(first_chapter_started.wait(), 5)
                self.assertTrue(last_map_started.is_set())
                self.assertFalse(any(phase.startswith('root_') and phase != 'root_context'
                                     for phase, _, _ in fake.requests))
                self.assertEqual(saved, [])
                release_last_map.set()
                await asyncio.wait_for(second_chapter_done.wait(), 5)
                self.assertEqual(completed_maps, {1, 2, 3, 4})
                self.assertFalse(any(phase in ('root_reduce', 'root_approval')
                                     for phase, _, _ in fake.requests))
                release_first_chapter.set()
                result = await asyncio.wait_for(task, 10)
            finally:
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)

        self.assertEqual(len(result['specifications']), 8)
        self.assertEqual(len(fake.calls), 1 + 7 * (4 + 2 * 2 + 3) + 1)
        self.assertEqual(result['usage']['total_tokens'], len(fake.calls) * 12)
        self.assertEqual([len(item['specifications']) for item in saved], list(range(1, 9)))
        for step, stage in enumerate(result['hierarchy']['stages'], 1):
            attempt = stage['attempts'][0]
            scans, nodes = attempt['scans'], attempt['nodes']
            self.assertEqual([scan['chunk_id'] for scan in scans], [1, 2, 3, 4])
            self.assertEqual([node['jurisdiction']['chunk_ids'] for node in nodes], [[1, 2], [3, 4]])
            for node in nodes:
                payload = next(payload for phase, current_step, payload in fake.calls
                               if phase == 'onelevel_reduce' and current_step == step
                               and payload['jurisdiction']['id'] == node['node'])
                self.assertEqual(payload['children'], [scan for scan in scans
                                 if scan['chunk_id'] in node['jurisdiction']['chunk_ids']])
                self.assertEqual(payload['subglobal_context'], attempt['subglobal_contexts'][node['node']])
            root = next(payload for phase, current_step, payload in fake.calls
                        if phase == 'root_reduce' and current_step == step)
            approval = next(payload for phase, current_step, payload in fake.calls
                            if phase == 'root_approval' and current_step == step)
            identifiers = [finding['id'] for scan in scans for finding in scan['findings']]
            self.assertEqual(root['children'], nodes)
            self.assertEqual(list(root['source_index']), identifiers)
            self.assertEqual(approval['node_outcomes'], nodes)
            self.assertEqual(list(approval['evidence_ledger']), identifiers)
            self.assertEqual(approval['required_review'], {'chunk_ids': [1, 2, 3, 4], 'finding_ids': identifiers})
            for scan in scans:
                for finding in scan['findings']:
                    retained = approval['evidence_ledger'][finding['id']]
                    self.assertEqual({key: retained[key] for key in finding}, finding)

    async def test_map_or_chapter_failure_and_caller_cancellation_stop_all_overlapping_work(self):
        for failure in ('map', 'chapter', 'caller'):
            with self.subTest(failure=failure):
                map_started, chapter_started = asyncio.Event(), asyncio.Event()
                active, cancelled = set(), set()
                saved = []

                async def before(phase, step, payload):
                    if step != 1:
                        return
                    if phase == 'map' and payload['chunk']['index'] >= 3:
                        name = f"map-{payload['chunk']['index']}"
                        active.add(name)
                        try:
                            if name == 'map-3':
                                map_started.set()
                            if failure == 'map' and name == 'map-4':
                                await chapter_started.wait()
                                raise RuntimeError('Map failed during chapter aggregation')
                            await asyncio.Event().wait()
                        except asyncio.CancelledError:
                            cancelled.add(name)
                            raise
                        finally:
                            active.remove(name)
                    elif phase == 'onelevel_reduce':
                        self.assertEqual(payload['jurisdiction']['chunk_ids'], [1, 2])
                        active.add('chapter')
                        try:
                            await map_started.wait()
                            chapter_started.set()
                            if failure == 'chapter':
                                raise RuntimeError('Chapter failed while other Maps were running')
                            await asyncio.Event().wait()
                        except asyncio.CancelledError:
                            cancelled.add('chapter')
                            raise
                        finally:
                            active.remove('chapter')

                fake = ControlledResponses(self, before)
                with self.assertLogs('server', level='INFO'):
                    task = asyncio.create_task(self.generate(fake, saved))
                    try:
                        if failure == 'caller':
                            await asyncio.wait_for(chapter_started.wait(), 5)
                            task.cancel()
                            with self.assertRaises(asyncio.CancelledError):
                                await task
                        else:
                            with self.assertRaises(ExceptionGroup) as raised:
                                await asyncio.wait_for(task, 5)
                            self.assertTrue(all(isinstance(error, RuntimeError)
                                                for error in raised.exception.exceptions))
                    finally:
                        task.cancel()
                        await asyncio.gather(task, return_exceptions=True)
                self.assertEqual(active, set())
                expected = {'map-3', 'chapter'} if failure == 'map' else {'map-3', 'map-4'}
                if failure == 'caller':
                    expected.add('chapter')
                self.assertEqual(cancelled, expected)
                self.assertFalse(any(phase in ('root_reduce', 'root_approval') or step > 1
                                     for phase, step, _ in fake.requests))
                self.assertEqual(saved, [])


if __name__ == '__main__':
    unittest.main()
