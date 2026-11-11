import asyncio
import base64
import json
import re
import unittest
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import patch

from pptx import Presentation

from server import chat, hierarchy
from server.evidence import EvidenceError
from server.models import AppServices
from server.specifications import SPECIFICATION_STAGES
from test_file_chunks import make_deck


class FakeResponses:
    def __init__(self, test, *, reject=0, missing_usage=False, mutate=None):
        self.test = test
        self.reject = reject
        self.missing_usage = missing_usage
        self.mutate = mutate
        self.calls = []
        self.output_limits = []
        self.approved = []
        self.active = self.peak = 0

    async def create_response(self, query, assistant_instruction, input_file=None, max_output_tokens=None, json_output=False):
        t = self.test
        phase = re.search(r'^Phase: (\w+)$', query, re.M)[1]
        match = re.search(r'^Stage: (\d+)/8$', query, re.M)
        step = int(match[1]) if match else 0
        payload = {} if phase == 'decision_register' else json.loads(query.split('<payload>\n', 1)[1].rsplit('\n</payload>', 1)[0])
        self.calls.append((phase, step, payload))
        self.output_limits.append((phase, max_output_tokens))
        t.assertGreater(max_output_tokens, 0)
        if step:
            stage = SPECIFICATION_STAGES[step - 1]
            t.assertIn(f'Specification prompt: {stage.prompt_template}', query)
            t.assertIn(f'Specification name: {stage.english_title}', query)
            t.assertEqual(step, len(self.approved) + 1)
            for previous in range(1, step):
                t.assertIn(f'Generated specification {previous}.', query)
        if phase == 'decision_register':
            t.assertEqual(step, 8)
            t.assertEqual(self.approved, list(range(1, 8)))
            t.assertIsNone(input_file)
            t.assertFalse(json_output)
            t.assertNotIn('<payload>', query)
            t.assertNotIn('Global business constraints', query)
            for previous_stage in SPECIFICATION_STAGES[:7]:
                t.assertIn(f'{previous_stage.step:02d}_{previous_stage.key}.md', query)
        else:
            t.assertTrue(json_output)
            t.assertIn('Never use majority voting', assistant_instruction)
        if phase == 'decision_register':
            value = '## Unresolved Items\nGenerated specification 8.\n## Items Resolved by the Specifications\nNone'
        elif phase == 'global_context':
            t.assertIsNotNone(input_file)
            chunks = payload['chunks']
            value = {'global_context': 'Global business constraints and terminology', 'groups': [
                {'title': f'Chapter {index // 2 + 1}', 'basis': f'Source heading at slide {index + 1}',
                 'context': 'Source scope', 'chunk_ids': [item['index'] for item in chunks[index:index + 2]]}
                for index in range(0, len(chunks), 2)]}
        elif phase in ('root_context', 'onelevel_context'):
            t.assertIsNone(input_file)
            t.assertIn('Global business constraints', payload['global_context'])
            value = {'context': f'{phase} orientation', 'focus': ['Read every unit'], 'cross_scope_checks': ['Exceptions']}
        elif phase == 'map':
            chunk = payload['chunk']
            t.assertIn('root_context orientation', payload['root_context']['context'])
            expected = 'onelevel_context' if chat.REDUCE_LEVELS == 2 else 'root_context'
            t.assertIn(expected, payload['subglobal_context']['context'])
            data = base64.b64decode(input_file['file_data'].split(',', 1)[1])
            slides = Presentation(BytesIO(data)).slides
            t.assertEqual([slide.shapes.title.text for slide in slides], [f"Slide {i}" for i in range(chunk['start'], chunk['end'] + 1)])
            self.active += 1
            self.peak = max(self.peak, self.active)
            try:
                await asyncio.sleep(0.02)
            finally:
                self.active -= 1
            value = {'covered_units': list(range(chunk['start'], chunk['end'] + 1)), 'findings': [{
                'statement': 'Permitted for administrators only, except suspended accounts.',
                'scope': 'Account access', 'strength': 'explicit', 'conditions': ['Administrator role'],
                'exceptions': ['Suspended accounts denied'],
                'sources': [{'unit': chunk['start'], 'quote': f"Original evidence from slide {chunk['start']}: administrators are permitted; suspended accounts are denied, including privileged users."}],
            }], 'gaps': []}
        elif phase in ('onelevel_reduce', 'root_reduce'):
            if phase == 'onelevel_reduce':
                ids = [identifier for child in payload['children'] for identifier in (
                    [finding['id'] for finding in child['findings']] if 'findings' in child else
                    [key for decision in child['outcome']['decisions'] for key in decision['finding_ids']])]
                if 'aggregation' not in payload:
                    t.assertEqual([child['chunk_id'] for child in payload['children']], payload['jurisdiction']['chunk_ids'])
            else:
                t.assertEqual(self.active, 0)
                ids = list(payload['source_index'])
                if chat.REDUCE_LEVELS == 2:
                    t.assertTrue(all('outcome' in child and 'findings' not in child for child in payload['children']))
                else:
                    t.assertTrue(all('findings' in child for child in payload['children']))
            value = {'summary': 'Access restrictions', 'decisions': [{
                'finding_ids': ids, 'verdict': 'qualified', 'statement': 'Admins allowed; suspended denied.',
                'rationale': 'Explicit scoped exception overrides general permission.',
            }] if ids else [], 'relations': [{
                'kind': 'exception', 'finding_ids': ids[:2], 'rationale': 'Scoped override', 'resolution': 'Deny suspended accounts',
            }] if len(ids) > 1 else [], 'gaps': []}
            if phase == 'root_reduce':
                value['body'] = f'## Details\nGenerated specification {step}.\n## Consistency and Open Questions\nNone'
        elif phase == 'root_approval':
            t.assertTrue(all('Original evidence' in value['sources'][0]['quote'] for value in payload['evidence_ledger'].values()))
            t.assertEqual(payload['required_review']['chunk_ids'], [scan['chunk_id'] for scan in payload['scans']])
            t.assertEqual(payload['required_review']['finding_ids'], list(payload['evidence_ledger']))
            t.assertIn('Do not claim an item was reviewed merely by copying its ID.', query)
            approved = not (step == 1 and payload['attempt'] <= self.reject)
            value = {'approved': approved, 'reviewed_chunk_ids': [scan['chunk_id'] for scan in payload['scans']],
                     'reviewed_finding_ids': list(payload['evidence_ledger']), 'rationale': 'Checked original evidence, scope and exceptions',
                     'feedback': [] if approved else ['Re-read suspended-account exceptions in every chunk']}
        else:
            raise AssertionError(phase)
        if self.mutate:
            value = self.mutate(phase, payload, value)
        if (phase == 'root_approval' and value['approved']
                and len(value['reviewed_chunk_ids']) == len(payload['required_review']['chunk_ids'])
                and len(value['reviewed_finding_ids']) == len(payload['required_review']['finding_ids'])
                and set(value['reviewed_chunk_ids']) == set(payload['required_review']['chunk_ids'])
                and set(value['reviewed_finding_ids']) == set(payload['required_review']['finding_ids'])):
            self.approved.append(step)
        unknown = self.missing_usage and phase == 'map' and step == 2
        return SimpleNamespace(output_text=value if isinstance(value, str) else json.dumps(value), usage=SimpleNamespace(
            input_tokens=None if unknown else 10, output_tokens=2, total_tokens=None if unknown else 12))


class HierarchicalSpecificationTests(unittest.IsolatedAsyncioTestCase):
    async def run_flow(self, *, count=4, parallel=2, settings=None, **options):
        fake = FakeResponses(self, **options)
        environment = {
            'FILE_CHUNK_MAX_SLIDES': '1', 'LLM_MAX_PARALLEL_CHUNK_REQUESTS': str(parallel),
            'LLM_MAX_APPROVAL_ATTEMPTS': '2', 'LLM_MAX_OUTPUT_TOKENS': '',
            'LLM_INTERMEDIATE_MAX_OUTPUT_TOKENS': '', 'LLM_MAX_APPROVAL_REVIEW_ATTEMPTS': '', **(settings or {}),
        }
        with patch.dict('os.environ', environment):
            with patch.object(hierarchy, 'split_file', wraps=hierarchy.split_file) as split:
                with self.assertLogs('server', level='INFO') as logs:
                    result = await chat.generate_specifications(AppServices(responses=fake), make_deck(count), 'sample.pptx')
        split.assert_called_once()
        return result, fake, logs.output

    async def test_large_chapters_use_multiple_calls_under_the_same_fork(self):
        def mutate(phase, payload, value):
            if phase == 'map':
                value['findings'][0]['sources'][0]['quote'] += ' Original evidence detail.' * 200
            return value
        result, fake, logs = await self.run_flow(count=4, mutate=mutate, settings={'LLM_CHAPTER_BATCH_MAX_BYTES': '6500'})
        self.assertEqual(len(result['specifications']), 8)
        for audit in result['hierarchy']['stages']:
            nodes = audit['attempts'][0]['nodes']
            self.assertEqual(len(nodes), 2)
            for node in nodes:
                calls = node['aggregation_calls']
                self.assertEqual([call['mode'] for call in calls], ['batch', 'batch', 'final'])
                self.assertEqual(calls[-1]['input_kind'], 'judgments')
                expected = {finding['id'] for scan in audit['attempts'][0]['scans']
                            if scan['chunk_id'] in node['jurisdiction']['chunk_ids'] for finding in scan['findings']}
                actual = {key for decision in node['outcome']['decisions'] for key in decision['finding_ids']}
                self.assertEqual(actual, expected)
        for phase, _, payload in fake.calls:
            if phase == 'root_reduce':
                self.assertTrue(all('aggregation_calls' not in child for child in payload['children']))
        self.assertEqual(result['usage']['total_tokens'], len(fake.calls) * 12)
        self.assertTrue(any('Chapter aggregation:' in line and 'mode=final' in line for line in logs))

    async def test_configured_map_input_estimate_stops_before_submitting_a_map(self):
        fake = FakeResponses(self)
        with patch.dict('os.environ', {'LLM_MAP_INPUT_TOKEN_BUDGET': '1'}):
            with self.assertLogs('server', level='INFO'):
                with self.assertRaises(ExceptionGroup) as raised:
                    await chat.generate_specifications(AppServices(responses=fake), make_deck(1), 'sample.pptx')
        self.assertTrue(any('LLM_MAP_INPUT_TOKEN_BUDGET' in str(error) for error in raised.exception.exceptions))
        self.assertFalse(any(phase == 'map' for phase, _, _ in fake.calls))

    async def test_eight_specs_actual_depth_context_coverage_provenance_logs_and_usage(self):
        result, fake, logs = await self.run_flow()
        per_stage = 4 + 3 + (4 if chat.REDUCE_LEVELS == 2 else 0)
        self.assertEqual(len(fake.calls), 1 + 7 * per_stage + 1)
        for phase, limit in fake.output_limits:
            self.assertEqual(limit, 128000 if phase in ('root_reduce', 'decision_register') else 64000)
        self.assertEqual(fake.peak, 2)
        self.assertEqual(result['hierarchy']['reduce_levels'], chat.REDUCE_LEVELS)
        self.assertEqual([spec['key'] for spec in result['specifications']], [stage.key for stage in SPECIFICATION_STAGES])
        self.assertEqual(result['usage'], {'input_tokens': len(fake.calls) * 10, 'output_tokens': len(fake.calls) * 2, 'total_tokens': len(fake.calls) * 12})
        self.assertEqual(result['hierarchy']['context_usage']['input_tokens'], 10)
        self.assertEqual(len(result['hierarchy']['stages']), 7)
        self.assertEqual([(phase, step) for phase, step, _ in fake.calls if step == 8], [('decision_register', 8)])
        self.assertEqual(result['specifications'][7]['usage']['total_tokens'], 12)
        self.assertIn(result['specifications'][7]['content'], result['reply'])
        for spec, audit in zip(result['specifications'], result['hierarchy']['stages']):
            self.assertIn(spec['content'], result['reply'])
            self.assertEqual(spec['usage']['total_tokens'], per_stage * 12)
            attempt = audit['attempts'][0]
            self.assertTrue(attempt['approval']['approved'])
            self.assertEqual([scan['chunk_id'] for scan in attempt['scans']], [1, 2, 3, 4])
            self.assertEqual(len(attempt['nodes']), 2 if chat.REDUCE_LEVELS == 2 else 0)
        self.assertTrue(all(line.isascii() for line in logs))
        self.assertEqual(sum('Root approval decision:' in line for line in logs), 7)
        self.assertEqual(sum('Full scan coverage verified:' in line for line in logs), 7)
        self.assertEqual(sum('Specification LLM query submitting:' in line for line in logs), 7 * per_stage + 1)
        for stage in SPECIFICATION_STAGES:
            self.assertTrue(any(f'specification="{stage.english_title}"' in line and 'input_tokens=' in line for line in logs))

    async def test_output_token_settings_apply_to_the_correct_phases(self):
        for final, intermediate, expected_final, expected_intermediate in (
            ('96000', '100000', 96000, 100000),
            ('999999', '999999', 128000, 128000),
            ('invalid', 'invalid', 128000, 64000),
        ):
            with self.subTest(final=final, intermediate=intermediate):
                _, fake, _ = await self.run_flow(count=1, settings={
                    'LLM_MAX_OUTPUT_TOKENS': final, 'LLM_INTERMEDIATE_MAX_OUTPUT_TOKENS': intermediate,
                })
                for phase, limit in fake.output_limits:
                    self.assertEqual(limit, expected_final if phase in ('root_reduce', 'decision_register') else expected_intermediate)

    async def test_larger_candidates_reach_approval_and_all_later_stages(self):
        def mutate(phase, payload, value):
            if phase == 'root_reduce':
                value['body'] += '\n' + 'x' * 220000
            return value
        result, _, _ = await self.run_flow(count=1, mutate=mutate, settings={
            'LLM_FINAL_MAX_BYTES': '', 'LLM_MAX_QUERY_BYTES': '',
        })
        self.assertEqual(len(result['specifications']), 8)
        self.assertTrue(all(len(spec['content'].encode('utf-8')) > 196608 for spec in result['specifications'][:7]))
        self.assertTrue(all(stage['attempts'][0]['approval']['approved'] for stage in result['hierarchy']['stages']))
        with self.assertRaisesRegex(EvidenceError, 'output exceeded'):
            await self.run_flow(count=1, mutate=mutate, settings={'LLM_FINAL_MAX_BYTES': '196608'})

    async def test_concurrency_never_exceeds_sixteen(self):
        _, fake, _ = await self.run_flow(count=20, parallel=99)
        self.assertEqual(fake.peak, 16)

    async def test_rejection_reprocesses_all_chunks_and_preserves_failed_attempt_usage(self):
        result, fake, logs = await self.run_flow(reject=1)
        attempts = result['hierarchy']['stages'][0]['attempts']
        self.assertEqual(len(attempts), 2)
        self.assertFalse(attempts[0]['approval']['approved'])
        self.assertTrue(attempts[1]['approval']['approved'])
        retried = [payload for phase, step, payload in fake.calls if phase == 'map' and step == 1 and payload['attempt'] == 2]
        self.assertEqual(len(retried), 4)
        self.assertTrue(all('Re-read suspended-account' in payload['feedback'][0] for payload in retried))
        self.assertEqual(result['specifications'][0]['usage']['total_tokens'], result['specifications'][1]['usage']['total_tokens'] * 2)
        self.assertEqual(result['usage']['total_tokens'], len(fake.calls) * 12)
        self.assertTrue(any('Root rejected candidate:' in line for line in logs))
        self.assertTrue(any('rationale="Checked original evidence, scope and exceptions"' in line for line in logs))
        self.assertTrue(any('feedback=["Re-read suspended-account exceptions in every chunk"]' in line for line in logs))

    async def test_persistent_rejection_stops_before_next_specification(self):
        with self.assertRaisesRegex(EvidenceError, 'after 2 full-scan attempts'):
            await self.run_flow(reject=2)

    async def test_unknown_tokens_propagate(self):
        result, _, _ = await self.run_flow(missing_usage=True)
        self.assertIsNone(result['usage']['input_tokens'])
        self.assertIsNone(result['specifications'][1]['usage']['total_tokens'])
        self.assertIsNotNone(result['specifications'][0]['usage']['input_tokens'])
        self.assertIsNotNone(result['usage']['output_tokens'])

    async def test_single_chunk_and_absent_specification_evidence_still_reach_approval(self):
        def mutate(phase, payload, value):
            if phase == 'map':
                value['findings'] = []
                value['gaps'] = ['No relevant facts on this slide; requested specification requires confirmation.']
            elif phase == 'root_reduce':
                value['gaps'] = ['Source details are unavailable and require confirmation.']
                value['body'] += '\nSource details: Needs confirmation. Dependencies: To be defined in a later stage.'
            elif phase == 'root_approval':
                value['feedback'] = ['Optional: confirm source gaps and refine wording when details become available.']
            return value
        result, fake, logs = await self.run_flow(count=1, mutate=mutate)
        self.assertEqual(len(result['specifications']), 8)
        self.assertTrue(all(stage['attempts'][0]['approval']['approved'] for stage in result['hierarchy']['stages']))
        self.assertTrue(all(len(stage['attempts']) == 1 for stage in result['hierarchy']['stages']))
        self.assertTrue(all(stage['attempts'][0]['approval']['feedback'] for stage in result['hierarchy']['stages']))
        self.assertEqual(sum(phase == 'map' for phase, _, _ in fake.calls), 7)
        self.assertFalse(any('Root rejected candidate:' in line for line in logs))

    async def test_intermediate_output_budget_is_enforced(self):
        def mutate(phase, payload, value):
            if phase == 'global_context':
                value['global_context'] += 'x' * 100000
            return value
        # A global context larger than the former maximum must reach all stages.
        with patch.dict('os.environ', {'LLM_INTERMEDIATE_MAX_BYTES': ''}):
            result, _, logs = await self.run_flow(count=1, mutate=mutate)
        self.assertEqual(len(result['specifications']), 8)
        self.assertTrue(any('phase=global_context' in line and 'output_budget_bytes=1048576' in line for line in logs))
        # Explicit smaller budgets still take effect.
        with patch.dict('os.environ', {'LLM_INTERMEDIATE_MAX_BYTES': '24000'}):
            with self.assertRaisesRegex(EvidenceError, 'output exceeded'):
                await self.run_flow(count=1, mutate=mutate)

    async def test_invalid_semantic_plan_is_not_allowed_to_skip_chunks(self):
        def mutate(phase, payload, value):
            if phase == 'global_context':
                value['groups'].pop()
            return value
        with self.assertRaisesRegex(EvidenceError, 'every chunk exactly once'):
            await self.run_flow(mutate=mutate)

    async def test_worker_missing_coverage_or_out_of_range_source_fails(self):
        for key in ('coverage', 'source'):
            def mutate(phase, payload, value):
                if phase == 'map':
                    if key == 'coverage':
                        value['covered_units'] = []
                    else:
                        value['findings'][0]['sources'][0]['unit'] = 999
                return value
            with self.subTest(key=key), self.assertRaises(ExceptionGroup):
                await self.run_flow(mutate=mutate)

    async def test_reducer_cannot_drop_findings(self):
        def mutate(phase, payload, value):
            if phase == 'root_reduce':
                value['decisions'] = []
            return value
        with self.assertRaisesRegex(EvidenceError, 'silently dropped evidence'):
            await self.run_flow(mutate=mutate)

    async def test_approval_must_explicitly_review_every_finding(self):
        reviews = []

        def mutate(phase, payload, value):
            if phase == 'root_approval':
                reviews.append(payload)
                value['reviewed_finding_ids'] = []
            return value
        with self.assertRaisesRegex(EvidenceError, 'after 2 review attempts: Root did not review all evidence'):
            await self.run_flow(mutate=mutate, settings={'LLM_MAX_APPROVAL_REVIEW_ATTEMPTS': '2'})
        self.assertEqual([review['review_attempt'] for review in reviews], [1, 2])
        self.assertTrue(all(review['attempt'] == 1 for review in reviews))
        self.assertEqual(reviews[1]['coverage_feedback']['missing_finding_ids'], sorted(reviews[0]['evidence_ledger']))

    async def test_missing_approval_ids_retry_same_candidate_and_preserve_audit_and_usage(self):
        omitted = False

        def mutate(phase, payload, value):
            nonlocal omitted
            if phase == 'root_approval' and not omitted:
                omitted = True
                value['reviewed_chunk_ids'] = value['reviewed_chunk_ids'][1:]
                value['reviewed_finding_ids'] = value['reviewed_finding_ids'][:-1]
            return value

        result, fake, logs = await self.run_flow(mutate=mutate)
        reviews = [payload for phase, step, payload in fake.calls if phase == 'root_approval' and step == 1]
        self.assertEqual([review['review_attempt'] for review in reviews], [1, 2])
        self.assertEqual(reviews[0]['candidate'], reviews[1]['candidate'])
        self.assertEqual(reviews[0]['evidence_ledger'], reviews[1]['evidence_ledger'])
        self.assertEqual(reviews[0]['required_review'], reviews[1]['required_review'])
        self.assertIsNone(reviews[0]['coverage_feedback'])
        feedback = reviews[1]['coverage_feedback']
        self.assertEqual(feedback['missing_chunk_ids'], [1])
        self.assertEqual(feedback['missing_finding_ids'], [reviews[0]['required_review']['finding_ids'][-1]])
        self.assertEqual(feedback['reviewed_finding_count'], 3)
        self.assertEqual(feedback['expected_finding_count'], 4)
        self.assertEqual(sum(phase == 'map' for phase, _, _ in fake.calls), 28)
        self.assertEqual(sum(phase == 'root_reduce' for phase, _, _ in fake.calls), 7)
        attempts = result['hierarchy']['stages'][0]['attempts']
        self.assertEqual(len(attempts), 1)
        failures = attempts[0]['approval_review_failures']
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0]['response'], feedback['previous_review'])
        self.assertEqual(failures[0]['coverage']['missing_finding_ids'], feedback['missing_finding_ids'])
        self.assertEqual(attempts[0]['approval']['reviewed_finding_ids'], reviews[0]['required_review']['finding_ids'])
        self.assertEqual(result['specifications'][0]['usage']['total_tokens'], result['specifications'][1]['usage']['total_tokens'] + 12)
        self.assertEqual(result['usage']['total_tokens'], len(fake.calls) * 12)
        self.assertTrue(any('review_attempt=1/3 reviewed_chunks=3/4 reviewed_findings=3/4' in line for line in logs))
        self.assertTrue(any(feedback['missing_finding_ids'][0] in line for line in logs))

    async def test_rejection_after_coverage_retry_still_requires_a_full_rescan(self):
        omitted = False

        def mutate(phase, payload, value):
            nonlocal omitted
            if phase == 'root_approval' and not omitted:
                omitted = True
                value['reviewed_finding_ids'] = []
            return value

        result, fake, _ = await self.run_flow(reject=1, mutate=mutate)
        attempts = result['hierarchy']['stages'][0]['attempts']
        self.assertEqual(len(attempts), 2)
        self.assertFalse(attempts[0]['approval']['approved'])
        self.assertTrue(attempts[1]['approval']['approved'])
        self.assertEqual(len(attempts[0]['approval_review_failures']), 1)
        self.assertFalse(attempts[0]['approval_review_failures'][0]['response']['approved'])
        reviews = [payload for phase, step, payload in fake.calls if phase == 'root_approval' and step == 1]
        self.assertEqual([(review['attempt'], review['review_attempt']) for review in reviews], [(1, 1), (1, 2), (2, 1)])
        self.assertEqual(reviews[1]['coverage_feedback']['previous_review']['feedback'], attempts[0]['approval']['feedback'])
        self.assertIsNone(reviews[2]['coverage_feedback'])
        self.assertTrue(all(':r2:' in finding for finding in reviews[2]['required_review']['finding_ids']))
        rescans = [payload for phase, step, payload in fake.calls if phase == 'map' and step == 1 and payload['attempt'] == 2]
        self.assertEqual(len(rescans), 4)
        self.assertTrue(all(payload['feedback'] == attempts[0]['approval']['feedback'] for payload in rescans))
        self.assertEqual(result['usage']['total_tokens'], len(fake.calls) * 12)

    async def test_persistent_unknown_approval_ids_exhaust_coverage_retries(self):
        reviews = []

        def mutate(phase, payload, value):
            if phase == 'root_approval':
                reviews.append(payload)
                value['reviewed_finding_ids'].append('invented-finding-id')
            return value

        with self.assertRaisesRegex(EvidenceError, 'after 3 review attempts: Root approval reported duplicate or unknown identifiers'):
            await self.run_flow(mutate=mutate)
        self.assertEqual(len(reviews), 3)
        self.assertEqual([review['review_attempt'] for review in reviews], [1, 2, 3])
        self.assertEqual(reviews[1]['coverage_feedback']['unknown_finding_ids'], ['invented-finding-id'])

    async def test_query_and_evidence_storage_budgets_fail_without_truncation(self):
        for setting in ('LLM_MAX_QUERY_BYTES', 'LLM_AUDIT_MAX_BYTES'):
            with self.subTest(setting=setting), patch.dict('os.environ', {setting: '1'}):
                with self.assertRaisesRegex(EvidenceError, 'budget exceeded'):
                    await self.run_flow()

    async def test_chunk_failure_cancels_siblings_and_never_reduces(self):
        fake = FakeResponses(self)
        original = fake.create_response
        started = asyncio.Event()
        cancelled = asyncio.Event()
        phases = []

        async def fail(**kwargs):
            phase = re.search(r'^Phase: (\w+)$', kwargs['query'], re.M)[1]
            phases.append(phase)
            if phase != 'map':
                return await original(**kwargs)
            payload = json.loads(kwargs['query'].split('<payload>\n')[1].rsplit('\n</payload>', 1)[0])
            if payload['chunk']['index'] == 1:
                await started.wait()
                raise RuntimeError('worker failed')
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                cancelled.set()

        with patch.dict('os.environ', {'FILE_CHUNK_MAX_SLIDES': '1', 'LLM_MAX_PARALLEL_CHUNK_REQUESTS': '2'}):
            with self.assertLogs('server', level='INFO'), self.assertRaises(ExceptionGroup):
                await asyncio.wait_for(chat.generate_specifications(AppServices(responses=SimpleNamespace(create_response=fail)), make_deck(2), 'sample.pptx'), 10)
        self.assertTrue(cancelled.is_set())
        self.assertNotIn('onelevel_reduce', phases)
        self.assertNotIn('root_reduce', phases)


if __name__ == '__main__':
    unittest.main()
