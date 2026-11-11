import asyncio
import copy
import unittest
from collections import Counter
from types import SimpleNamespace
from unittest.mock import patch

from server import chat, hierarchy
from server.evidence import EVIDENCE_STRENGTHS, EvidenceError, MapStrengthError, map_record
from server.models import AppServices
from test_file_chunks import make_deck
from test_map_requests import ControlledResponses


def scan_record():
    return {
        "covered_units": [4], "gaps": [],
        "findings": [{
            "statement": "Administrators may access active accounts.",
            "scope": "Account access", "strength": "explicit",
            "conditions": ["Administrator role"], "exceptions": ["Suspended accounts denied"],
            "sources": [{"unit": 4, "quote": "Administrators may access active accounts."}],
        }],
    }


class MapStrengthValidationTests(unittest.TestCase):
    def setUp(self):
        self.chunk = SimpleNamespace(
            index=3, start=4, end=4, source_regions=({"page": 4, "bottom": 10, "top": 200},),
        )

    def test_valid_strengths_preserve_their_meaning_and_server_provenance(self):
        for strength in EVIDENCE_STRENGTHS:
            with self.subTest(strength=strength):
                value = scan_record()
                value["findings"][0]["strength"] = strength
                self.assertIs(map_record(value, self.chunk, "api", 2), value)
                finding = value["findings"][0]
                self.assertEqual(finding["strength"], strength)
                self.assertEqual(finding["id"], "api:r2:c3:f1")
                self.assertEqual(value["chunk_id"], 3)
                if chat.REDUCE_LEVELS == 2:
                    self.assertEqual(finding["sources"][0]["region"], {"bottom": 10, "top": 200})

    def test_invalid_values_and_types_report_the_original_value_without_mutating_output(self):
        for strength in ("EXPLICIT", " explicit ", "", "strong", None, 1, True,
                         ["explicit"], {"label": "explicit"}):
            with self.subTest(strength=strength):
                value = scan_record()
                value["findings"][0]["strength"] = strength
                original = copy.deepcopy(value)
                with self.assertRaises(MapStrengthError) as raised:
                    map_record(value, self.chunk, "api", 1)
                self.assertEqual(raised.exception.issues, [
                    {"finding_index": 0, "missing": False, "value": strength},
                ])
                self.assertEqual(raised.exception.outcome, original)
                self.assertEqual(value, original)

    def test_missing_field_and_multiple_invalid_findings_are_distinguished(self):
        value = scan_record()
        value["findings"].append(copy.deepcopy(value["findings"][0]))
        value["findings"].append(copy.deepcopy(value["findings"][0]))
        del value["findings"][0]["strength"]
        value["findings"][2]["strength"] = None
        original = copy.deepcopy(value)
        with self.assertRaises(MapStrengthError) as raised:
            map_record(value, self.chunk, "api", 1)
        self.assertEqual(raised.exception.issues, [
            {"finding_index": 0, "missing": True, "value": None},
            {"finding_index": 2, "missing": False, "value": None},
        ])
        self.assertEqual(value, original)

    def test_other_schema_and_source_errors_remain_fatal_even_after_a_bad_strength(self):
        for invalid in (
            {"conditions": None}, {"sources": []},
            {"sources": [{"unit": 5, "quote": "Outside this chunk"}]},
            {"sources": [{"unit": 4, "quote": ""}]},
            {"statement": ""},
        ):
            with self.subTest(invalid=invalid):
                value = scan_record()
                value["findings"][0]["strength"] = "high"
                value["findings"].append({**copy.deepcopy(value["findings"][0]), **invalid})
                with self.assertRaises(EvidenceError) as raised:
                    map_record(value, self.chunk, "api", 1)
                self.assertNotIsInstance(raised.exception, MapStrengthError)


class RecordingResponses(ControlledResponses):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queries = []

    async def create_response(self, **kwargs):
        self.queries.append(kwargs)
        return await super().create_response(**kwargs)


class MapStrengthRepairTests(unittest.IsolatedAsyncioTestCase):
    async def run_flow(self, fake, *, count=1, settings=None, on_stage_completed=None):
        environment = {
            "FILE_CHUNK_MAX_SLIDES": "1", "LLM_MAX_PARALLEL_CHUNK_REQUESTS": "2",
            "LLM_MAX_QUERY_BYTES": "", "LLM_AUDIT_MAX_BYTES": "",
            "LLM_CHAPTER_INPUT_TOKEN_BUDGET": "", "LLM_MAP_INPUT_TOKEN_BUDGET": "",
            **(settings or {}),
        }
        with patch.dict("os.environ", environment):
            return await chat.generate_specifications(
                AppServices(responses=fake), make_deck(count), "sample.pptx",
                on_stage_completed=on_stage_completed,
            )

    async def test_repairs_only_the_affected_chunk_preserving_input_progress_audit_and_usage(self):
        broken = False

        def mutate(phase, payload, value):
            nonlocal broken
            if phase == "map" and len(fake.approved) == 1 and payload["chunk"]["index"] == 2:
                if not broken:
                    broken = True
                    value["findings"][0]["strength"] = {"label": "explicit"}
                else:
                    value["findings"][0]["strength"] = "inferred"
            return value

        snapshots = []

        async def saved(result):
            snapshots.append(copy.deepcopy(result))

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO") as logs:
            result = await self.run_flow(fake, count=3, on_stage_completed=saved)
        counts = Counter((step, payload["chunk"]["index"]) for phase, step, payload in fake.calls if phase == "map")
        self.assertEqual(counts[(2, 2)], 2)
        self.assertEqual(sum(counts.values()), 22)
        self.assertTrue(all(count == 1 for key, count in counts.items() if key != (2, 2)))
        self.assertEqual(sum(phase == "root_context" for phase, _, _ in fake.calls), 7)
        self.assertEqual(sum(phase == "root_approval" for phase, _, _ in fake.calls), 7)
        self.assertEqual(sum(phase == "root_reduce" for phase, _, _ in fake.calls), 7)
        self.assertEqual([len(snapshot["specifications"]) for snapshot in snapshots], list(range(1, 9)))
        audit = result["hierarchy"]["stages"][1]["attempts"][0]
        failure, = audit["map_failures"]
        self.assertEqual(failure["chunk_id"], 2)
        self.assertEqual(failure["strength_attempt"], 1)
        self.assertEqual(failure["response"]["findings"][0]["strength"], {"label": "explicit"})
        self.assertNotIn("id", failure["response"]["findings"][0])
        self.assertEqual(audit["scans"][1]["findings"][0]["strength"], "inferred")
        self.assertEqual(audit["scans"][1]["findings"][0]["id"], "api:r1:c2:f1")
        requests = [payload for phase, step, payload in fake.calls
                    if phase == "map" and step == 2 and payload["chunk"]["index"] == 2]
        self.assertEqual({key: value for key, value in requests[1].items() if key != "strength_repair"}, requests[0])
        self.assertEqual(requests[1]["strength_repair"]["allowed_strengths"], list(EVIDENCE_STRENGTHS))
        self.assertEqual(requests[1]["strength_repair"]["invalid_findings"][0]["finding"],
                         failure["response"]["findings"][0])
        query_pairs = [(request, query) for request, query in zip(fake.requests, fake.queries)
                       if request[0] == "map" and request[1] == 2 and request[2]["chunk"]["index"] == 2]
        self.assertEqual(query_pairs[0][1]["input_file"], query_pairs[1][1]["input_file"])
        self.assertIn("Return the COMPLETE Map JSON", query_pairs[1][1]["query"])
        self.assertEqual(result["usage"]["total_tokens"], len(fake.calls) * 12)
        progress = [line for line in logs.output if "Map completed " in line and "stage=api " in line]
        self.assertEqual(len(progress), 3)
        self.assertTrue(any("Map completed 3/3:" in line for line in progress))
        self.assertTrue(any("strength_attempt=1/3" in line and "label" in line
                            and "repair_exhausted=False" in line for line in logs.output))

    async def test_missing_strength_is_repaired_by_the_model(self):
        def mutate(phase, payload, value):
            if phase == "map" and not fake.approved:
                if "strength_repair" not in payload:
                    del value["findings"][0]["strength"]
                else:
                    value["findings"][0]["strength"] = "uncertain"
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO") as logs:
            result = await self.run_flow(fake)
        audit = result["hierarchy"]["stages"][0]["attempts"][0]
        self.assertTrue(audit["map_failures"][0]["issues"][0]["missing"])
        self.assertEqual(audit["scans"][0]["findings"][0]["strength"], "uncertain")
        self.assertTrue(any('"missing": true' in line for line in logs.output))

    async def test_persistent_bad_strength_stops_after_three_attempts(self):
        def mutate(phase, payload, value):
            if phase == "map":
                value["findings"][0]["strength"] = ["high"]
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO") as logs:
            with self.assertRaises(ExceptionGroup) as raised:
                await self.run_flow(fake)
        self.assertIn("after 3 attempts", str(raised.exception.exceptions[0]))
        self.assertEqual(sum(phase == "map" for phase, _, _ in fake.calls), 3)
        self.assertFalse(any(phase.endswith("_reduce") for phase, _, _ in fake.calls))
        self.assertFalse(any("Map completed " in line for line in logs.output))
        self.assertTrue(any("repair_exhausted=True" in line for line in logs.output))
        repairs = [payload["strength_repair"] for phase, _, payload in fake.calls
                   if phase == "map" and "strength_repair" in payload]
        self.assertEqual(repairs[0], repairs[1])

    async def test_repaired_output_must_still_pass_source_validation(self):
        def mutate(phase, payload, value):
            if phase == "map":
                if "strength_repair" not in payload:
                    value["findings"][0]["strength"] = "high"
                else:
                    value["findings"][0]["sources"][0]["unit"] = 999
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            with self.assertRaises(ExceptionGroup) as raised:
                await self.run_flow(fake)
        self.assertIn("Source outside worker jurisdiction", str(raised.exception.exceptions[0]))
        self.assertEqual(sum(phase == "map" for phase, _, _ in fake.calls), 2)

    async def test_timeout_and_strength_budgets_are_independent_and_never_reset(self):
        for exhaust_timeout in (False, True):
            with self.subTest(exhaust_timeout=exhaust_timeout):
                attempts = 0

                async def fail(phase, step, payload):
                    nonlocal attempts
                    if phase == "map" and step == 1:
                        attempts += 1
                        if attempts in (2, 4, 5) or (exhaust_timeout and attempts == 6):
                            raise TimeoutError("Simulated Map deadline")

                def mutate(phase, payload, value):
                    if phase == "map" and not fake.approved and attempts in (1, 3):
                        value["findings"][0]["strength"] = "high"
                    return value

                fake = RecordingResponses(self, before_request=fail, mutate=mutate)
                with self.assertLogs("server", level="INFO") as logs:
                    if exhaust_timeout:
                        with self.assertRaises(ExceptionGroup) as raised:
                            await self.run_flow(fake)
                        self.assertIsInstance(raised.exception.exceptions[0], TimeoutError)
                    else:
                        result = await self.run_flow(fake)
                        self.assertEqual(len(result["specifications"]), 8)
                        self.assertIsNone(result["usage"]["total_tokens"])
                        self.assertIsNotNone(result["specifications"][1]["usage"]["total_tokens"])
                self.assertEqual(attempts, 6)
                self.assertTrue(any("retry=3/3" in line for line in logs.output))
                self.assertEqual(sum("Map strength validation failed:" in line for line in logs.output), 2)
                stage_requests = [payload for phase, step, payload in fake.requests if phase == "map" and step == 1]
                self.assertTrue(all("strength_repair" in payload for payload in stage_requests[1:]))

    async def test_cancellation_during_repair_stops_without_retry(self):
        started = asyncio.Event()

        async def hang(phase, step, payload):
            if phase == "map" and "strength_repair" in payload:
                started.set()
                await asyncio.Event().wait()

        def mutate(phase, payload, value):
            if phase == "map":
                value["findings"][0]["strength"] = "high"
            return value

        fake = RecordingResponses(self, before_request=hang, mutate=mutate)
        with self.assertLogs("server", level="INFO") as logs:
            task = asyncio.create_task(self.run_flow(fake))
            try:
                await asyncio.wait_for(started.wait(), 10)
            finally:
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await task
        self.assertEqual(sum(phase == "map" for phase, _, _ in fake.requests), 2)
        self.assertFalse(any("Map completed " in line for line in logs.output))

    async def test_repair_feedback_respects_query_byte_budget(self):
        baseline = RecordingResponses(self)
        with self.assertLogs("server", level="INFO"):
            await self.run_flow(baseline)
        original = next(query for query in baseline.queries if "Phase: map\n" in query["query"])
        ceiling = len(original["query"].encode("utf-8")) + 32

        def mutate(phase, payload, value):
            if phase == "map":
                value["findings"][0]["strength"] = "high"
                value["findings"][0]["statement"] = "Supported detail. " * 800
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            with self.assertRaises(ExceptionGroup) as raised:
                await self.run_flow(fake, settings={"LLM_MAX_QUERY_BYTES": str(ceiling)})
        self.assertIn("LLM query budget exceeded", str(raised.exception.exceptions[0]))
        self.assertEqual(sum(phase == "map" for phase, _, _ in fake.calls), 1)

    @unittest.skipUnless(chat.REDUCE_LEVELS == 2, "Only twolevel has a Map input token estimate")
    async def test_repair_feedback_respects_map_input_token_budget(self):
        baseline = RecordingResponses(self)
        with self.assertLogs("server", level="INFO"):
            await self.run_flow(baseline)
        original = next(query for query in baseline.queries if "Phase: map\n" in query["query"])
        chunk = next(payload["chunk"] for phase, _, payload in baseline.calls if phase == "map")
        ceiling = hierarchy.estimate_tokens(original["assistant_instruction"] + original["query"]) + chunk["estimated_tokens"] + 32

        def mutate(phase, payload, value):
            if phase == "map":
                value["findings"][0]["strength"] = "high"
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            with self.assertRaises(ExceptionGroup) as raised:
                await self.run_flow(fake, settings={"LLM_MAP_INPUT_TOKEN_BUDGET": str(ceiling)})
        self.assertIn("LLM_MAP_INPUT_TOKEN_BUDGET", str(raised.exception.exceptions[0]))
        self.assertEqual(sum(phase == "map" for phase, _, _ in fake.calls), 1)


if __name__ == "__main__":
    unittest.main()

