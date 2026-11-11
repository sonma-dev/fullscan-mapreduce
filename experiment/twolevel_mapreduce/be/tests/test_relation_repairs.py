import copy
import json
import re
import unittest
from collections import Counter
from unittest.mock import patch

from server import chat, hierarchy
from server.evidence import EvidenceError, RelationCardinalityError, adjudication_record
from server.models import AppServices
from test_chat import FakeResponses
from test_file_chunks import make_deck


def relation(members):
    return {"kind": "exception", "finding_ids": members,
            "rationale": "The suspended-account exception is stated within one finding.",
            "resolution": "Suspended accounts remain denied."}


def outcome(members):
    return {
        "summary": "Account access restrictions",
        "decisions": [{"finding_ids": members, "verdict": "qualified",
                       "statement": "Administrators are allowed; suspended accounts are denied.",
                       "rationale": "The source states the exception."}] if members else [],
        "relations": [], "gaps": [],
    }


class RelationValidationTests(unittest.TestCase):
    def test_zero_and_one_id_relations_report_exact_indices_without_mutating_output(self):
        value = outcome(["f1", "f2"])
        value["relations"] = [relation(["f1"]), relation([])]
        original = copy.deepcopy(value)
        with self.assertRaises(RelationCardinalityError) as raised:
            adjudication_record(value, {"f1", "f2"})
        self.assertEqual(raised.exception.issues, [
            {"relation_index": 0, "finding_ids": ["f1"], "minimum_findings": 2},
            {"relation_index": 1, "finding_ids": [], "minimum_findings": 2},
        ])
        self.assertEqual(raised.exception.outcome, original)
        self.assertEqual(value, original)

    def test_empty_relations_are_valid_with_zero_one_or_multiple_findings(self):
        for members in ([], ["f1"], ["f1", "f2"]):
            with self.subTest(members=members):
                value = outcome(members)
                self.assertIs(adjudication_record(value, set(members)), value)
        value["relations"] = [relation(["f1", "f2"])]
        self.assertIs(adjudication_record(value, {"f1", "f2"}), value)

    def test_other_schema_or_provenance_errors_are_not_repairable_short_relations(self):
        for malformed in (
            relation(["f1", "f1"]),
            relation(["unknown"]),
            {**relation(["f1"]), "finding_ids": None},
            {**relation(["f1"]), "kind": "invented"},
            {**relation(["f1"]), "rationale": ""},
        ):
            with self.subTest(malformed=malformed):
                value = outcome(["f1", "f2"])
                value["relations"] = [relation(["f1"]), malformed]
                with self.assertRaises(EvidenceError) as raised:
                    adjudication_record(value, {"f1", "f2"})
                self.assertNotIsInstance(raised.exception, RelationCardinalityError)

    def test_missing_evidence_and_malformed_gaps_remain_fatal(self):
        for field, invalid in (("decisions", []), ("gaps", None)):
            with self.subTest(field=field):
                value = outcome(["f1"])
                value["relations"] = [relation(["f1"])]
                value[field] = invalid
                with self.assertRaises(EvidenceError) as raised:
                    adjudication_record(value, {"f1"})
                self.assertNotIsInstance(raised.exception, RelationCardinalityError)


class RecordingResponses(FakeResponses):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queries = []

    async def create_response(self, **kwargs):
        self.queries.append(kwargs)
        return await super().create_response(**kwargs)


class RelationRepairTests(unittest.IsolatedAsyncioTestCase):
    async def run_flow(self, fake, *, count=4, settings=None):
        environment = {
            "FILE_CHUNK_MAX_SLIDES": "1", "LLM_MAX_PARALLEL_CHUNK_REQUESTS": "2",
            "LLM_MAX_QUERY_BYTES": "", "LLM_AUDIT_MAX_BYTES": "",
            "LLM_CHAPTER_INPUT_TOKEN_BUDGET": "", "LLM_MAP_INPUT_TOKEN_BUDGET": "",
            **(settings or {}),
        }
        with patch.dict("os.environ", environment):
            return await chat.generate_specifications(AppServices(responses=fake), make_deck(count), "sample.pptx")

    async def test_repairs_only_the_affected_reducer_and_preserves_evidence_audit_and_usage(self):
        targets = ["root_reduce"] + (["onelevel_reduce"] if chat.REDUCE_LEVELS == 2 else [])
        for target in targets:
            with self.subTest(target=target):
                broken = False

                def mutate(phase, payload, value):
                    nonlocal broken
                    if phase == target and not broken:
                        broken = True
                        value["relations"] = [relation(value["decisions"][0]["finding_ids"][:1])]
                    elif phase == target and "relation_repair" in payload:
                        value["relations"] = []
                    return value

                fake = RecordingResponses(self, mutate=mutate)
                with self.assertLogs("server", level="INFO") as logs:
                    result = await self.run_flow(fake)
                counts = Counter(phase for phase, _, _ in fake.calls)
                self.assertEqual(counts["map"], 28)
                self.assertEqual(counts["global_context"], 1)
                self.assertEqual(counts["root_context"], 7)
                self.assertEqual(counts["root_approval"], 7)
                self.assertEqual(counts["root_reduce"], 7 + (target == "root_reduce"))
                first = result["hierarchy"]["stages"][0]["attempts"]
                self.assertEqual(len(first), 1)
                failures = first[0]["reduction_failures"]
                self.assertEqual(len(failures), 1)
                self.assertEqual(failures[0]["phase"], target)
                self.assertEqual(failures[0]["response"]["relations"][0]["resolution"],
                                 "Suspended accounts remain denied.")
                initial = next(payload for phase, step, payload in fake.calls if phase == target and step == 1)
                repaired = next(payload for phase, step, payload in fake.calls
                                if phase == target and step == 1 and "relation_repair" in payload)
                self.assertEqual({key: val for key, val in repaired.items() if key != "relation_repair"}, initial)
                self.assertEqual(repaired["relation_repair"]["invalid_relations"][0]["relation"],
                                 failures[0]["response"]["relations"][0])
                self.assertEqual(result["usage"]["total_tokens"], len(fake.calls) * 12)
                self.assertEqual(len(result["specifications"]), 8)
                self.assertTrue(any("reduction_attempt=1/3" in line and "repair_exhausted=False" in line
                                    for line in logs.output))
                self.assertFalse(any("Root rejected candidate:" in line for line in logs.output))
                for query in fake.queries:
                    if re.search(r"^Phase: (root_reduce|onelevel_reduce)$", query["query"], re.M):
                        self.assertIn("Each relation needs at least TWO DISTINCT supplied finding IDs", query["query"])

    async def test_single_and_empty_finding_scopes_can_repair_to_empty_relations(self):
        for empty in (False, True):
            with self.subTest(empty=empty):
                broken = False
                target = "onelevel_reduce" if chat.REDUCE_LEVELS == 2 else "root_reduce"

                def mutate(phase, payload, value):
                    nonlocal broken
                    if empty and phase == "map":
                        value["findings"] = []
                        value["gaps"] = ["No source facts for this specification."]
                    if phase == target and not broken:
                        broken = True
                        members = value["decisions"][0]["finding_ids"] if value["decisions"] else []
                        value["relations"] = [relation(members)]
                    return value

                fake = RecordingResponses(self, mutate=mutate)
                with self.assertLogs("server", level="INFO"):
                    result = await self.run_flow(fake, count=1)
                self.assertEqual(len(result["specifications"]), 8)
                first = result["hierarchy"]["stages"][0]["attempts"][0]
                self.assertEqual(first["reduction_failures"][0]["issues"][0]["finding_ids"],
                                 [] if empty else ["screen_functions:r1:c1:f1"])
                reviewed = first["nodes"][0]["outcome"] if chat.REDUCE_LEVELS == 2 else first["candidate"]
                self.assertEqual(reviewed["relations"], [])
                self.assertEqual(len(reviewed["decisions"]), 0 if empty else 1)
                if not empty:
                    self.assertIn("suspended denied", reviewed["decisions"][0]["statement"])

    async def test_persistent_short_relation_stops_after_three_attempts_without_rescanning(self):
        target = "onelevel_reduce" if chat.REDUCE_LEVELS == 2 else "root_reduce"

        def mutate(phase, payload, value):
            if phase == target:
                value["relations"] = [relation(value["decisions"][0]["finding_ids"][:1])]
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO") as logs:
            with self.assertRaises(ExceptionGroup if chat.REDUCE_LEVELS == 2 else EvidenceError) as raised:
                await self.run_flow(fake, count=1)
        error = raised.exception.exceptions[0] if chat.REDUCE_LEVELS == 2 else raised.exception
        self.assertIn("after 3 attempts", str(error))
        self.assertEqual(sum(phase == target for phase, _, _ in fake.calls), 3)
        self.assertEqual(sum(phase == "map" for phase, _, _ in fake.calls), 1)
        self.assertFalse(any(phase == "root_approval" for phase, _, _ in fake.calls))
        self.assertTrue(any("repair_exhausted=True" in line for line in logs.output))

    async def test_unknown_relation_id_fails_without_repair(self):
        def mutate(phase, payload, value):
            if phase == "root_reduce":
                value["relations"] = [relation(["invented-finding"])]
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            with self.assertRaisesRegex(EvidenceError, "unknown identifiers"):
                await self.run_flow(fake, count=1)
        self.assertEqual(sum(phase == "root_reduce" for phase, _, _ in fake.calls), 1)
        self.assertFalse(any("relation_repair" in payload for _, _, payload in fake.calls))

    async def test_repair_feedback_cannot_bypass_the_query_byte_budget(self):
        def mutate(phase, payload, value):
            if phase == "root_reduce":
                value["relations"] = [{**relation(value["decisions"][0]["finding_ids"]),
                                       "rationale": "Source-supported detail. " * 4000}]
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            with self.assertRaisesRegex(EvidenceError, "LLM query budget exceeded"):
                await self.run_flow(fake, count=1, settings={"LLM_MAX_QUERY_BYTES": "50000"})
        self.assertEqual(sum(phase == "root_reduce" for phase, _, _ in fake.calls), 1)

    async def test_chapter_batches_repair_in_place_and_preserve_the_same_batch(self):
        broken = False

        def mutate(phase, payload, value):
            nonlocal broken
            if phase == "map":
                value["findings"][0]["sources"][0]["quote"] += " Original evidence detail." * 200
            if phase == "onelevel_reduce" and "aggregation" in payload and not broken:
                broken = True
                value["relations"] = [relation(value["decisions"][0]["finding_ids"][:1])]
            elif phase == "onelevel_reduce" and "relation_repair" in payload:
                value["relations"] = []
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            result = await self.run_flow(fake, settings={"LLM_CHAPTER_BATCH_MAX_BYTES": "6500"})
        self.assertTrue(broken)
        first = result["hierarchy"]["stages"][0]["attempts"][0]
        failure = first["reduction_failures"][0]
        repaired = next(payload for phase, _, payload in fake.calls
                        if phase == "onelevel_reduce" and "relation_repair" in payload)
        self.assertEqual(repaired["aggregation"], failure["aggregation"])
        self.assertEqual(sum(phase == "map" for phase, _, _ in fake.calls), 28)
        self.assertEqual(len(first["nodes"]), 2)
        self.assertTrue(any(node.get("aggregation_calls") for node in first["nodes"]))

    async def test_chapter_input_budget_also_applies_to_repair_feedback(self):
        baseline = RecordingResponses(self)
        with self.assertLogs("server", level="INFO"):
            await self.run_flow(baseline, count=1)
        original = next(query for query in baseline.queries if "Phase: onelevel_reduce\n" in query["query"])
        ceiling = hierarchy.estimate_tokens(original["assistant_instruction"] + original["query"]) + 32

        def mutate(phase, payload, value):
            if phase == "onelevel_reduce":
                value["relations"] = [relation(value["decisions"][0]["finding_ids"][:1])]
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            with self.assertRaises(ExceptionGroup) as raised:
                await self.run_flow(fake, count=1, settings={"LLM_CHAPTER_INPUT_TOKEN_BUDGET": str(ceiling)})
        self.assertIn("LLM_CHAPTER_INPUT_TOKEN_BUDGET including repair feedback", str(raised.exception.exceptions[0]))
        self.assertEqual(sum(phase == "onelevel_reduce" for phase, _, _ in fake.calls), 1)


if __name__ == "__main__":
    unittest.main()
