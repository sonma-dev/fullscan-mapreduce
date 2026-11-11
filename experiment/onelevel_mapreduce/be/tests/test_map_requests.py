import asyncio
import json
import re
import unittest
from collections import Counter
from unittest.mock import patch

from server import chat, hierarchy
from server.models import AppServices
from test_chat import FakeResponses
from test_file_chunks import make_deck


class ControlledResponses(FakeResponses):
    def __init__(self, test, before_request=None, after_request=None, **kwargs):
        super().__init__(test, **kwargs)
        self.before_request = before_request
        self.after_request = after_request
        self.requests = []

    async def create_response(self, **kwargs):
        query = kwargs['query']
        phase = re.search(r'^Phase: (\w+)$', query, re.M)[1]
        match = re.search(r'^Stage: (\d+)/8$', query, re.M)
        step = int(match[1]) if match else 0
        payload = {} if phase == 'decision_register' else json.loads(query.split('<payload>\n', 1)[1].rsplit('\n</payload>', 1)[0])
        self.requests.append((phase, step, payload))
        if self.before_request:
            await self.before_request(phase, step, payload)
        result = await super().create_response(**kwargs)
        if self.after_request:
            self.after_request(phase, step, payload)
        return result


class MapRequestTests(unittest.IsolatedAsyncioTestCase):
    async def generate(self, fake, *, timeout=5, count=2, parallel=2):
        with patch.dict('os.environ', {
            'FILE_CHUNK_MAX_SLIDES': '1',
            'LLM_MAX_PARALLEL_CHUNK_REQUESTS': str(parallel),
            'LLM_MAX_APPROVAL_ATTEMPTS': '2',
        }), patch.object(hierarchy, 'MAP_REQUEST_TIMEOUT_SECONDS', timeout):
            return await asyncio.wait_for(
                chat.generate_specifications(AppServices(responses=fake), make_deck(count), 'sample.pptx'),
                15,
            )

    async def test_three_timeouts_retry_only_the_straggler_and_count_it_once(self):
        requests = Counter()
        cancelled = 0

        async def delay(phase, step, payload):
            nonlocal cancelled
            if phase != 'map' or step != 1:
                return
            chunk = payload['chunk']['index']
            requests[chunk] += 1
            if chunk == 1 and requests[chunk] <= 3:
                try:
                    await asyncio.Event().wait()
                finally:
                    cancelled += 1

        fake = ControlledResponses(self, delay)
        with self.assertLogs('server', level='INFO') as logs:
            result = await self.generate(fake, timeout=0.5, parallel=1)
        self.assertEqual(requests, {1: 4, 2: 1})
        self.assertEqual(cancelled, 3)
        first_stage = [line for line in logs.output if 'stage=screen_functions ' in line]
        progress = [line for line in first_stage if 'Map completed ' in line]
        self.assertEqual(len(progress), 2)
        self.assertIn('Map completed 1/2:', progress[0])
        self.assertIn('chunk=2 ', progress[0])
        self.assertIn('Map completed 2/2:', progress[1])
        self.assertIn('chunk=1 request_attempt=4', progress[1])
        for retry in range(1, 4):
            self.assertTrue(any(f'retry={retry}/3' in line for line in first_stage))
        self.assertEqual(result['usage'], dict.fromkeys(('input_tokens', 'output_tokens', 'total_tokens')))
        self.assertIsNone(result['specifications'][0]['usage']['total_tokens'])
        self.assertIsNotNone(result['specifications'][1]['usage']['total_tokens'])
        scans = result['hierarchy']['stages'][0]['attempts'][0]['scans']
        self.assertEqual([scan['chunk_id'] for scan in scans], [1, 2])
        self.assertEqual(scans[0]['findings'][0]['id'], 'screen_functions:r1:c1:f1')

    async def test_fourth_timeout_fails_without_reducing_partial_results(self):
        active = 0
        requests = Counter()

        async def hang(phase, step, payload):
            nonlocal active
            if phase != 'map':
                return
            requests[payload['chunk']['index']] += 1
            active += 1
            try:
                await asyncio.Event().wait()
            finally:
                active -= 1

        fake = ControlledResponses(self, hang)
        with self.assertLogs('server', level='INFO') as logs:
            with self.assertRaises(ExceptionGroup) as raised:
                await self.generate(fake, timeout=0.05)
        self.assertTrue(all(isinstance(exc, TimeoutError) for exc in raised.exception.exceptions))
        self.assertEqual(max(requests.values()), 4)
        self.assertTrue(all(value <= 4 for value in requests.values()))
        self.assertEqual(active, 0)
        self.assertFalse(any(phase.endswith('_reduce') for phase, _, _ in fake.requests))
        self.assertFalse(any('Map completed ' in line for line in logs.output))
        self.assertTrue(any('Map retries exhausted:' in line for line in logs.output))

    async def test_caller_cancellation_does_not_retry(self):
        started = asyncio.Event()
        stopped = asyncio.Event()

        async def hang(phase, step, payload):
            if phase == 'map':
                started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    stopped.set()

        fake = ControlledResponses(self, hang)
        with self.assertLogs('server', level='INFO') as logs:
            task = asyncio.create_task(self.generate(fake, count=1))
            await asyncio.wait_for(started.wait(), 5)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertTrue(stopped.is_set())
        self.assertEqual(sum(phase == 'map' for phase, _, _ in fake.requests), 1)
        self.assertFalse(any('Map request timed out:' in line for line in logs.output))

    async def test_invalid_map_evidence_is_not_retried_or_counted(self):
        def invalidate(phase, payload, value):
            if phase == 'map':
                value['covered_units'] = []
            return value

        fake = ControlledResponses(self, mutate=invalidate)
        with self.assertLogs('server', level='INFO') as logs:
            with self.assertRaises(ExceptionGroup):
                await self.generate(fake, count=1)
        self.assertEqual(sum(phase == 'map' for phase, _, _ in fake.requests), 1)
        self.assertFalse(any('Map completed ' in line for line in logs.output))
        self.assertFalse(any('Map request timed out:' in line for line in logs.output))

    async def test_queue_wait_and_non_map_calls_do_not_consume_map_deadline(self):
        async def delay(phase, step, payload):
            if step == 1 and phase == 'root_context':
                await asyncio.sleep(1.1)
            if step == 1 and phase == 'map':
                await asyncio.sleep(0.55)

        fake = ControlledResponses(self, delay)
        with self.assertLogs('server', level='INFO') as logs:
            result = await self.generate(fake, timeout=1, count=3, parallel=1)
        self.assertEqual(len(result['specifications']), 8)
        self.assertEqual(sum(phase == 'map' for phase, _, _ in fake.requests), 21)
        self.assertFalse(any('Map request timed out:' in line for line in logs.output))

    async def test_root_and_fork_aggregation_can_exceed_the_leaf_map_deadline(self):
        delayed = Counter()

        async def delay(phase, step, payload):
            if step == 1 and phase.endswith('_reduce'):
                delayed[phase] += 1
                await asyncio.sleep(1.1)

        fake = ControlledResponses(self, delay)
        with self.assertLogs('server', level='INFO') as logs:
            result = await self.generate(fake, timeout=1, count=4, parallel=2)
        expected = {'root_reduce': 1}
        if chat.REDUCE_LEVELS == 2:
            expected['onelevel_reduce'] = 2
        self.assertEqual(delayed, expected)
        self.assertEqual(len(result['specifications']), 8)
        self.assertEqual(sum(phase == 'map' for phase, _, _ in fake.requests), 28)
        self.assertFalse(any('Map request timed out:' in line for line in logs.output))

    async def test_progress_tracks_completion_order_and_resets_for_each_full_scan(self):
        ready = {}
        completed = Counter()

        def gate(step, payload):
            return ready.setdefault((step, payload['attempt']), asyncio.Event())

        async def delay(phase, step, payload):
            if phase == 'map' and payload['chunk']['index'] == 1:
                await gate(step, payload).wait()

        def finish(phase, step, payload):
            if phase == 'map' and payload['chunk']['index'] != 1:
                key = (step, payload['attempt'])
                completed[key] += 1
                if completed[key] == 2:
                    gate(step, payload).set()

        fake = ControlledResponses(self, delay, finish, reject=1)
        with self.assertLogs('server', level='INFO') as logs:
            await self.generate(fake, count=3, parallel=3)
        scans = {}
        for line in logs.output:
            if 'Map completed ' not in line:
                continue
            match = re.search(
                r'Map completed (\d+)/(\d+): file_name=sample.pptx step=(\d+)/8 '
                r'stage=\w+ attempt=(\d+) chunk=(\d+) request_attempt=1',
                line,
            )
            self.assertIsNotNone(match, line)
            done, total, step, attempt, chunk = map(int, match.groups())
            self.assertEqual(total, 3)
            scans.setdefault((step, attempt), []).append((done, chunk))
        self.assertEqual(len(scans), 8)
        for progress in scans.values():
            self.assertEqual([done for done, _ in progress], [1, 2, 3])
            self.assertEqual({chunk for _, chunk in progress}, {1, 2, 3})
            self.assertEqual(progress[-1][1], 1)


if __name__ == '__main__':
    unittest.main()
