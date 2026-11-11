import asyncio
import copy
import unittest
from collections import Counter
from unittest.mock import patch

from server import chat
from server.evidence import DecisionIdentifierError, EvidenceError, adjudication_record
from server.models import AppServices
from test_chat import FakeResponses
from test_file_chunks import make_deck
from test_relation_repairs import RecordingResponses, outcome, relation


class DecisionIdentifierValidationTests(unittest.TestCase):
    def test_reports_all_invalid_decisions_and_missing_ids_without_mutation(self):
        value = outcome(["f1", "f1", "unknown", "unknown"])
        value["decisions"].append({**value["decisions"][0], "finding_ids": ["other"]})
        original = copy.deepcopy(value)
        with self.assertRaises(DecisionIdentifierError) as raised:
            adjudication_record(value, {"f1", "f2"})
        self.assertEqual(raised.exception.issues, [
            {"decision_index": 0, "duplicate_finding_ids": ["f1", "unknown"], "unknown_finding_ids": ["unknown"]},
            {"decision_index": 1, "duplicate_finding_ids": [], "unknown_finding_ids": ["other"]},
        ])
        self.assertEqual(raised.exception.missing_finding_ids, ["f2"])
        self.assertEqual(raised.exception.outcome, original)
        self.assertEqual(value, original)

    def test_reusing_an_id_across_different_decisions_is_valid(self):
        value = outcome(["f1"])
        value["decisions"].append({**value["decisions"][0], "statement": "Another supported detail."})
        self.assertIs(adjudication_record(value, {"f1"}), value)

    def test_unknown_id_with_no_evidence_still_requires_a_replacement(self):
        value = outcome(["invented"])
        with self.assertRaises(DecisionIdentifierError) as raised:
            adjudication_record(value, set())
        self.assertEqual(raised.exception.missing_finding_ids, [])
        empty = outcome([])
        self.assertIs(adjudication_record(empty, set()), empty)

    def test_other_schema_and_relation_errors_remain_fatal(self):
        for field, invalid in (
            ("finding_ids", None), ("finding_ids", []), ("finding_ids", [1]),
            ("finding_ids", [True]), ("finding_ids", [["f1"]]),
            ("finding_ids", [{"id": "f1"}]), ("verdict", "invented"),
            ("statement", ""), ("rationale", None),
        ):
            with self.subTest(field=field, invalid=invalid):
                value = outcome(["f1", "f1"])
                value["decisions"].append({**value["decisions"][0], field: invalid})
                with self.assertRaises(EvidenceError) as raised:
                    adjudication_record(value, {"f1"})
                self.assertNotIsInstance(raised.exception, DecisionIdentifierError)
        for changes in (
            {"gaps": None}, {"summary": ""}, {"body": ""},
            {"relations": [relation(["unknown"])]},
            {"relations": [relation(["f1", "f1"])]},
        ):
            with self.subTest(changes=changes):
                value = {**outcome(["f1", "f1"]), "body": "## Details", **changes}
                with self.assertRaises(EvidenceError) as raised:
                    adjudication_record(value, {"f1"}, candidate=True)
                self.assertNotIsInstance(raised.exception, DecisionIdentifierError)

    def test_omitted_evidence_without_an_identifier_error_remains_fatal(self):
        with self.assertRaisesRegex(EvidenceError, "silently dropped evidence") as raised:
            adjudication_record(outcome(["f1"]), {"f1", "f2"})
        self.assertNotIsInstance(raised.exception, DecisionIdentifierError)


class DecisionIdentifierRepairTests(unittest.IsolatedAsyncioTestCase):
    async def run_flow(self, fake, *, count=1, settings=None):
        with patch.dict("os.environ", {
            "FILE_CHUNK_MAX_SLIDES": "1", "LLM_MAX_QUERY_BYTES": "",
            "LLM_AUDIT_MAX_BYTES": "", "LLM_CHAPTER_INPUT_TOKEN_BUDGET": "",
            "LLM_MAP_INPUT_TOKEN_BUDGET": "", **(settings or {}),
        }):
            return await chat.generate_specifications(AppServices(responses=fake), make_deck(count), "sample.pptx")

    async def test_retries_only_the_affected_reducer_preserving_evidence_audit_and_usage(self):
        for target, invalid in ((target, invalid) for target in ("root_reduce", "onelevel_reduce")
                                for invalid in ("duplicate", "unknown")):
            with self.subTest(target=target, invalid=invalid):
                broken = False

                def mutate(phase, payload, value):
                    nonlocal broken
                    if phase == target and not broken:
                        broken = True
                        members = value["decisions"][0]["finding_ids"]
                        if invalid == "duplicate":
                            members.append(members[0])
                        else:
                            members[0] = "invented-finding"
                    return value

                fake = RecordingResponses(self, mutate=mutate)
                with self.assertLogs("server", level="INFO") as logs:
                    result = await self.run_flow(fake)
                self.assertEqual(len(result["specifications"]), 8)
                counts = Counter(phase for phase, _, _ in fake.calls)
                self.assertEqual(counts, {
                    "global_context": 1, "root_context": 7, "onelevel_context": 7, "map": 7,
                    "root_reduce": 7 + (target == "root_reduce"),
                    "onelevel_reduce": 7 + (target == "onelevel_reduce"),
                    "root_approval": 7, "decision_register": 1,
                })
                attempts = result["hierarchy"]["stages"][0]["attempts"]
                self.assertEqual(len(attempts), 1)
                failure, = attempts[0]["reduction_failures"]
                initial, repaired = [payload for phase, step, payload in fake.calls if phase == target and step == 1]
                self.assertEqual({key: value for key, value in repaired.items()
                                  if key != "decision_identifier_repair"}, initial)
                diagnostics = repaired["decision_identifier_repair"]
                self.assertEqual(diagnostics["allowed_finding_ids"], ["screen_functions:r1:c1:f1"])
                self.assertEqual(diagnostics["missing_finding_ids"],
                                 ["screen_functions:r1:c1:f1"] if invalid == "unknown" else [])
                self.assertEqual(diagnostics["invalid_decisions"][0]["decision"], failure["response"]["decisions"][0])
                self.assertEqual(diagnostics["invalid_decisions"][0][f"{invalid}_finding_ids"],
                                 ["invented-finding" if invalid == "unknown" else "screen_functions:r1:c1:f1"])
                self.assertEqual(failure["phase"], target)
                self.assertEqual(result["usage"]["total_tokens"], len(fake.calls) * 12)
                self.assertTrue(any("reduction_attempt=1/3" in line and "repair_exhausted=False" in line
                                    for line in logs.output))
                self.assertTrue(any("payload.decision_identifier_repair" in query["query"] for query in fake.queries))

    async def test_persistent_errors_stop_after_three_attempts_without_approval_or_rescan(self):
        for target in ("root_reduce", "onelevel_reduce"):
            with self.subTest(target=target):
                def mutate(phase, payload, value):
                    if phase == target:
                        value["decisions"][0]["finding_ids"].append("unknown")
                    return value

                fake = FakeResponses(self, mutate=mutate)
                with self.assertLogs("server", level="INFO") as logs:
                    with self.assertRaises(ExceptionGroup if target == "onelevel_reduce" else EvidenceError) as raised:
                        await self.run_flow(fake)
                error = raised.exception.exceptions[0] if target == "onelevel_reduce" else raised.exception
                self.assertIn("decision identifier validation failed after 3 attempts", str(error))
                self.assertIsInstance(error.__cause__, DecisionIdentifierError)
                self.assertEqual(sum(phase == target for phase, _, _ in fake.calls), 3)
                self.assertEqual(sum(phase == "map" for phase, _, _ in fake.calls), 1)
                self.assertFalse(any(phase == "root_approval" for phase, _, _ in fake.calls))
                self.assertTrue(any("repair_exhausted=True" in line for line in logs.output))

    async def test_identifier_and_relation_errors_share_the_attempt_limit_and_latest_feedback(self):
        calls = 0

        def mutate(phase, payload, value):
            nonlocal calls
            if phase == "root_reduce":
                calls += 1
                if calls == 2:
                    value["relations"] = [relation(value["decisions"][0]["finding_ids"])]
                else:
                    value["decisions"][0]["finding_ids"].append("unknown")
            return value

        fake = FakeResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            with self.assertRaisesRegex(EvidenceError, "after 3 attempts"):
                await self.run_flow(fake)
        reductions = [payload for phase, _, payload in fake.calls if phase == "root_reduce"]
        self.assertEqual(len(reductions), 3)
        self.assertIn("decision_identifier_repair", reductions[1])
        self.assertIn("relation_repair", reductions[2])
        self.assertNotIn("decision_identifier_repair", reductions[2])

    async def test_replacement_must_still_cover_every_finding(self):
        def mutate(phase, payload, value):
            if phase == "root_reduce":
                if "decision_identifier_repair" in payload:
                    value["decisions"] = []
                else:
                    value["decisions"][0]["finding_ids"].append("unknown")
            return value

        fake = FakeResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            with self.assertRaisesRegex(EvidenceError, "silently dropped evidence"):
                await self.run_flow(fake)
        self.assertEqual(sum(phase == "root_reduce" for phase, _, _ in fake.calls), 2)
        self.assertFalse(any(phase == "root_approval" for phase, _, _ in fake.calls))

    async def test_repair_feedback_respects_query_and_audit_budgets(self):
        for settings, message in (({"LLM_MAX_QUERY_BYTES": "50000"}, "LLM query budget exceeded"),
                                  ({"LLM_AUDIT_MAX_BYTES": "50000"}, "Evidence storage budget exceeded")):
            with self.subTest(settings=settings):
                def mutate(phase, payload, value):
                    if phase == "root_reduce":
                        value["decisions"][0]["finding_ids"].append("unknown")
                        value["decisions"][0]["rationale"] = "Original evidence detail. " * 4000
                    return value

                fake = FakeResponses(self, mutate=mutate)
                with self.assertLogs("server", level="INFO"):
                    with self.assertRaisesRegex(EvidenceError, message):
                        await self.run_flow(fake, settings=settings)
                self.assertEqual(sum(phase == "root_reduce" for phase, _, _ in fake.calls), 1)

    async def test_chapter_batch_repairs_reuse_the_same_evidence_and_aggregation(self):
        broken = False

        def mutate(phase, payload, value):
            nonlocal broken
            if phase == "map":
                value["findings"][0]["sources"][0]["quote"] += " Original evidence detail." * 200
            if phase == "onelevel_reduce" and "aggregation" in payload and not broken:
                broken = True
                value["decisions"][0]["finding_ids"].append("unknown")
            return value

        fake = FakeResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            result = await self.run_flow(fake, count=4, settings={"LLM_CHAPTER_BATCH_MAX_BYTES": "6500"})
        self.assertTrue(broken)
        initial = next(payload for phase, _, payload in fake.calls
                       if phase == "onelevel_reduce" and "aggregation" in payload)
        repaired = next(payload for phase, _, payload in fake.calls if "decision_identifier_repair" in payload)
        self.assertEqual({key: value for key, value in repaired.items()
                          if key != "decision_identifier_repair"}, initial)
        failure, = result["hierarchy"]["stages"][0]["attempts"][0]["reduction_failures"]
        self.assertEqual(failure["aggregation"], initial["aggregation"])
        self.assertEqual(sum(phase == "map" for phase, _, _ in fake.calls), 28)

    async def test_cancellation_during_repair_stops_without_another_attempt(self):
        def mutate(phase, payload, value):
            if phase == "root_reduce":
                if "decision_identifier_repair" in payload:
                    raise asyncio.CancelledError
                value["decisions"][0]["finding_ids"].append("unknown")
            return value

        fake = FakeResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            with self.assertRaises(asyncio.CancelledError):
                await self.run_flow(fake)
        self.assertEqual(sum(phase == "root_reduce" for phase, _, _ in fake.calls), 2)
        self.assertFalse(any(phase == "root_approval" for phase, _, _ in fake.calls))


if __name__ == "__main__":
    unittest.main()
