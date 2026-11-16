import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from server.decision_register import generate_decision_register
from server.models import AppServices
from server.specifications import SPECIFICATION_STAGES, generate_stages


class DecisionRegisterTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        environment = patch.dict('os.environ', {
            'LLM_MAX_QUERY_BYTES': '', 'LLM_FINAL_MAX_BYTES': '', 'LLM_MAX_OUTPUT_TOKENS': '',
        })
        environment.start()
        self.addCleanup(environment.stop)
        self.stage = SPECIFICATION_STAGES[-1]
        self.previous = [
            {'step': stage.step, 'key': stage.key, 'content': f'# {stage.title}\n\nNeeds confirmation: question-{stage.step}',
             'internal_evidence': 'INTERNAL_RECORD_MUST_NOT_BE_SENT'}
            for stage in SPECIFICATION_STAGES[:7]
        ]

    async def test_only_markdown_is_sent_and_usage_is_retained(self):
        body = '## Unresolved Items\nAD-001: Needs confirmation\n## Items Resolved by the Specifications\nSee confirmed statements'
        usage = {'input_tokens': 23, 'output_tokens': 11, 'total_tokens': 34}
        create = AsyncMock(return_value=SimpleNamespace(output_text=body, usage=SimpleNamespace(**usage)))
        result, actual_usage = await generate_decision_register(
            AppServices(responses=SimpleNamespace(create_response=create)), self.stage, 'source.pdf', self.previous,
        )
        create.assert_awaited_once()
        request = create.await_args.kwargs
        self.assertIsNone(request['input_file'])
        self.assertFalse(request.get('json_output', False))
        self.assertEqual(request['max_output_tokens'], 128000)
        self.assertEqual(result, body)
        self.assertEqual(actual_usage, usage)
        self.assertIn('08_architecture_decision.md', request['query'])
        self.assertNotIn('INTERNAL_RECORD_MUST_NOT_BE_SENT', request['query'])
        self.assertNotIn('<payload>', request['query'])
        for spec in self.previous:
            self.assertIn(spec['content'], request['query'])
            self.assertIn(f"{spec['step']:02d}_{spec['key']}.md", request['query'])

    async def test_query_and_output_budgets_fail_without_truncating(self):
        create = AsyncMock(return_value=SimpleNamespace(output_text='ああ', usage=None))
        services = AppServices(responses=SimpleNamespace(create_response=create))
        with patch.dict('os.environ', {'LLM_MAX_QUERY_BYTES': '1'}):
            with self.assertRaisesRegex(RuntimeError, 'TBD query budget exceeded'):
                await generate_decision_register(services, self.stage, 'source.pdf', self.previous)
        create.assert_not_awaited()
        with patch.dict('os.environ', {'LLM_FINAL_MAX_BYTES': '5'}):
            with self.assertRaisesRegex(RuntimeError, 'TBD output exceeded'):
                await generate_decision_register(services, self.stage, 'source.pdf', self.previous)
        create.assert_awaited_once()

    async def test_unknown_usage_and_configured_output_limit(self):
        create = AsyncMock(return_value=SimpleNamespace(output_text='## No unresolved items', usage=None))
        with patch.dict('os.environ', {'LLM_MAX_OUTPUT_TOKENS': '96000'}):
            _, usage = await generate_decision_register(
                AppServices(responses=SimpleNamespace(create_response=create)), self.stage, 'source.pdf', self.previous,
            )
        self.assertEqual(create.await_args.kwargs['max_output_tokens'], 96000)
        self.assertEqual(usage, {'input_tokens': None, 'output_tokens': None, 'total_tokens': None})

    async def test_invalid_or_failed_final_generation_keeps_seven_completed_stages(self):
        for failure in ('', ' \n', RuntimeError('TBD failed'), asyncio.CancelledError()):
            with self.subTest(failure=repr(failure)):
                create = AsyncMock()
                if isinstance(failure, BaseException):
                    create.side_effect = failure
                else:
                    create.return_value = SimpleNamespace(output_text=failure, usage=None)
                services = AppServices(responses=SimpleNamespace(create_response=create))
                saved = []

                async def save(result):
                    saved.append(len(result['specifications']))

                async def generate(stage, previous):
                    if stage.key == 'architecture_decision':
                        return await generate_decision_register(services, stage, 'source.pdf', previous)
                    return '## Content\nNeeds confirmation', {'input_tokens': 1, 'output_tokens': 1, 'total_tokens': 2}

                expected = asyncio.CancelledError if isinstance(failure, asyncio.CancelledError) else RuntimeError
                with self.assertLogs('server', level='INFO'), self.assertRaises(expected):
                    await generate_stages('source.pdf', generate, on_stage_completed=save)
                self.assertEqual(saved, list(range(1, 8)))
                create.assert_awaited_once()


if __name__ == '__main__':
    unittest.main()
