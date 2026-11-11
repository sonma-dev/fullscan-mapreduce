import asyncio
import base64
import re
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from server.chat import generate_specifications
from server.models import AppServices


EXPECTED_TITLES = ["Screen Function Specification", "API Specification", "Data Specification", "Batch Function Specification", "Business Rules", "Exception Handling Specification", "Processing Flow Specification", "Architecture Decision Register"]
EXPECTED_KEYS = ["screen_functions", "api", "data", "batch_functions", "business_rules", "exception_handling", "processing_flows", "architecture_decision"]

EXPECTED_ENGLISH_TITLES = ['Screen Function Specification', 'API Specification', 'Data Specification', 'Batch Function Specification', 'Business Rules', 'Exception Handling Specification', 'Processing Flow Specification', 'Architecture Decision Register']
EXPECTED_SECTIONS = ['## Screen Inventory and Navigation', '## Interfaces by API', '## Data Field Definitions', '## Processing by Job', '## Decisions, Calculations, and State Transitions', '## Handling by Exception', '## Normal Processing', '## Unresolved Items']


class FullFileSpecificationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        environment = patch.dict('os.environ', {'LLM_MAX_OUTPUT_TOKENS': ''})
        environment.start()
        self.addCleanup(environment.stop)

    async def test_eight_stages_run_in_order_with_all_previous_specifications(self):
        data = b"%PDF-1.7\nbinary\x00\xff"
        calls = []
        active = 0

        async def create_response(query, assistant_instruction, input_file, max_output_tokens, json_output=False):
            nonlocal active
            self.assertEqual(max_output_tokens, 128000)
            active += 1
            self.assertEqual(active, 1)
            step = int(re.search(r"^Stage: (\d+)/8$", query, re.MULTILINE)[1])
            self.assertEqual(step, len(calls) + 1)
            self.assertIn(f"Specification key: {EXPECTED_KEYS[step - 1]}", query)
            self.assertIn(f"Specification title: {EXPECTED_TITLES[step - 1]}", query)
            self.assertIn(f"Specification prompt: stages/{EXPECTED_KEYS[step - 1]}.jinja2", query)
            self.assertIn(f"Specification name: {EXPECTED_ENGLISH_TITLES[step - 1]}", query)
            for index, section in enumerate(EXPECTED_SECTIONS, 1):
                if index == step:
                    self.assertIn(section, query)
                else:
                    self.assertNotIn(section, query)
            self.assertFalse(json_output)
            if step == 8:
                self.assertIsNone(input_file)
                self.assertIn('Phase: decision_register', query)
                for index, key in enumerate(EXPECTED_KEYS[:7], 1):
                    self.assertIn(f'{index:02d}_{key}.md', query)
            else:
                self.assertEqual(base64.b64decode(input_file["file_data"].split(",", 1)[1]), data)
                self.assertEqual(input_file["filename"], "source.pdf")
            for previous in range(1, 9):
                marker = f"Generated specification {previous}."
                if previous < step:
                    self.assertIn(marker, query)
                else:
                    self.assertNotIn(marker, query)
            calls.append(step)
            await asyncio.sleep(0)
            active -= 1
            return SimpleNamespace(
                output_text=f"## Details\nGenerated specification {step}.",
                usage=SimpleNamespace(input_tokens=step * 100, output_tokens=step * 10, total_tokens=step * 110),
            )

        with self.assertLogs("server.specifications", level="INFO") as logs:
            result = await generate_specifications(AppServices(responses=SimpleNamespace(create_response=create_response)), data, "source.pdf")
        self.assertEqual(calls, list(range(1, 9)))
        self.assertEqual(set(result), {"reply", "specifications", "usage"})
        self.assertEqual([s["title"] for s in result["specifications"]], EXPECTED_TITLES)
        self.assertEqual([s["key"] for s in result["specifications"]], EXPECTED_KEYS)
        self.assertEqual([s["step"] for s in result["specifications"]], list(range(1, 9)))
        for step, specification in enumerate(result["specifications"], 1):
            self.assertTrue(specification["content"].startswith(f"# {step}. {EXPECTED_TITLES[step - 1]}\n"))
            self.assertGreaterEqual(specification["elapsed_ms"], 0)
            self.assertIn(specification["content"], result["reply"])
        self.assertEqual(result["usage"], {"input_tokens": 3600, "output_tokens": 360, "total_tokens": 3960})
        self.assertEqual(sum("Specification stage started:" in line for line in logs.output), 8)
        self.assertEqual(sum("Specification stage completed:" in line for line in logs.output), 8)
        self.assertTrue(all(line.isascii() for line in logs.output))
        query_logs = [line for line in logs.output if "Specification LLM query submitting:" in line]
        self.assertEqual(len(query_logs), 8)
        for step, line in enumerate(query_logs, 1):
            self.assertIn(f"step={step}/8", line)
            self.assertIn(f'specification="{EXPECTED_ENGLISH_TITLES[step - 1]}"', line)
            self.assertIn(f"prompt=stages/{EXPECTED_KEYS[step - 1]}.jinja2", line)
            self.assertIn("phase=decision_register" if step == 8 else "phase=generation", line)
        self.assertTrue(any("stage=processing_flows" in line and "input_tokens=700 output_tokens=70 total_tokens=770" in line for line in logs.output))

    async def test_configured_output_limit_reaches_every_stage(self):
        for value, expected in (('96000', 96000), ('999999', 128000), ('invalid', 128000)):
            with self.subTest(value=value), patch.dict('os.environ', {'LLM_MAX_OUTPUT_TOKENS': value}):
                create_response = AsyncMock(return_value=SimpleNamespace(output_text='Specification', usage=None))
                with self.assertLogs('server', level='INFO'):
                    await generate_specifications(
                        AppServices(responses=SimpleNamespace(create_response=create_response)), b'pdf', 'source.pdf',
                    )
                self.assertEqual(create_response.await_count, 8)
                self.assertTrue(all(call.kwargs['max_output_tokens'] == expected for call in create_response.await_args_list))

    async def test_missing_usage_remains_unknown_without_losing_other_counts(self):
        calls = 0

        async def create_response(**kwargs):
            nonlocal calls
            calls += 1
            return SimpleNamespace(output_text="## Content\nNeeds confirmation", usage=SimpleNamespace(
                input_tokens=None if calls == 3 else 10, output_tokens=2, total_tokens=None if calls == 3 else 12,
            ))

        result = await generate_specifications(AppServices(responses=SimpleNamespace(create_response=create_response)), b"pdf", "source.pdf")
        self.assertEqual(calls, 8)
        self.assertEqual(result["usage"], {"input_tokens": None, "output_tokens": 16, "total_tokens": None})
        self.assertEqual(result["specifications"][0]["usage"]["input_tokens"], 10)
        self.assertIsNone(result["specifications"][2]["usage"]["input_tokens"])

    async def test_failure_stops_later_stages_and_logs_stage_identity(self):
        calls = 0

        async def create_response(**kwargs):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise RuntimeError("API failed")
            return SimpleNamespace(output_text="## Content\nConfirmed requirements", usage=None)

        with self.assertLogs("server.specifications", level="INFO") as logs:
            with self.assertRaisesRegex(RuntimeError, "API failed"):
                await generate_specifications(AppServices(responses=SimpleNamespace(create_response=create_response)), b"pdf", "source.pdf")
        self.assertEqual(calls, 3)
        self.assertTrue(any("Specification stage failed:" in line and "step=3/8 stage=data" in line for line in logs.output))
        self.assertFalse(any("step=4/8" in line for line in logs.output))

    async def test_blank_output_is_not_accepted_as_a_completed_specification(self):
        async def create_response(**kwargs):
            return SimpleNamespace(output_text=" \n", usage=None)

        with self.assertLogs("server.specifications", level="ERROR"):
            with self.assertRaisesRegex(RuntimeError, "Empty specification"):
                await generate_specifications(AppServices(responses=SimpleNamespace(create_response=create_response)), b"pdf", "source.pdf")


if __name__ == "__main__":
    unittest.main()
