import copy
import unittest
from unittest.mock import patch

from server import chat, hierarchy
from server.evidence import EvidenceError, encode
from server.models import AppServices
from test_chat import FakeResponses
from test_file_chunks import make_deck


class RecordingResponses(FakeResponses):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queries = []

    async def create_response(self, **kwargs):
        self.queries.append(kwargs)
        return await super().create_response(**kwargs)


class ApprovalIdentifierRepairTests(unittest.IsolatedAsyncioTestCase):
    async def run_flow(self, fake, *, count=4, settings=None, on_stage_completed=None):
        environment = {
            "FILE_CHUNK_MAX_SLIDES": "1", "LLM_MAX_PARALLEL_CHUNK_REQUESTS": "2",
            "LLM_MAX_APPROVAL_ATTEMPTS": "2", "LLM_MAX_APPROVAL_REVIEW_ATTEMPTS": "",
            "LLM_MAX_QUERY_BYTES": "", "LLM_AUDIT_MAX_BYTES": "",
            "LLM_CHAPTER_INPUT_TOKEN_BUDGET": "", "LLM_MAP_INPUT_TOKEN_BUDGET": "",
            **(settings or {}),
        }
        with patch.dict("os.environ", environment):
            return await chat.generate_specifications(
                AppServices(responses=fake), make_deck(count), "sample.pptx",
                on_stage_completed=on_stage_completed,
            )

    async def test_repairs_only_approval_and_preserves_candidate_evidence_saved_stages_and_usage(self):
        for kind in ("duplicate_chunk", "unknown_chunk", "duplicate_finding", "unknown_finding"):
            with self.subTest(kind=kind):
                saved = []

                async def save(result):
                    saved.append(copy.deepcopy(result))

                def mutate(phase, payload, value):
                    if phase == "root_approval" and len(fake.approved) == 1 and payload["review_attempt"] == 1:
                        if kind == "duplicate_chunk":
                            value["reviewed_chunk_ids"].append(value["reviewed_chunk_ids"][0])
                        elif kind == "unknown_chunk":
                            value["reviewed_chunk_ids"].extend([0, 999])
                        elif kind == "duplicate_finding":
                            value["reviewed_finding_ids"].append(value["reviewed_finding_ids"][0])
                        else:
                            value["reviewed_finding_ids"].append("unknown\\nsource-id")
                    return value

                fake = RecordingResponses(self, mutate=mutate)
                with self.assertLogs("server", level="INFO") as logs:
                    result = await self.run_flow(fake, on_stage_completed=save)
                self.assertEqual([len(snapshot["specifications"]) for snapshot in saved], list(range(1, 9)))
                self.assertEqual(sum(phase == "map" for phase, _, _ in fake.calls), 28)
                self.assertEqual(sum(phase == "root_context" for phase, _, _ in fake.calls), 7)
                self.assertEqual(sum(phase == "root_reduce" for phase, _, _ in fake.calls), 7)
                self.assertEqual(sum(phase == "root_approval" for phase, _, _ in fake.calls), 8)
                if chat.REDUCE_LEVELS == 2:
                    self.assertEqual(sum(phase == "onelevel_reduce" for phase, _, _ in fake.calls), 14)
                reviews = [payload for phase, step, payload in fake.calls if phase == "root_approval" and step == 2]
                first, repaired = reviews
                self.assertEqual([review["review_attempt"] for review in reviews], [1, 2])
                self.assertEqual(
                    {key: value for key, value in first.items() if key not in ("coverage_feedback", "review_attempt")},
                    {key: value for key, value in repaired.items() if key not in ("coverage_feedback", "review_attempt")},
                )
                diagnostics = repaired["coverage_feedback"]
                self.assertTrue(diagnostics[kind + "_ids"])
                self.assertEqual(diagnostics["reviewed_chunk_count"], 4)
                self.assertEqual(diagnostics["reviewed_finding_count"], 4)
                self.assertTrue(diagnostics["previous_review"]["approved"])
                audit = result["hierarchy"]["stages"][1]["attempts"]
                self.assertEqual(len(audit), 1)
                failure, = audit[0]["approval_review_failures"]
                self.assertEqual(failure["response"], diagnostics["previous_review"])
                self.assertEqual(failure["coverage"][kind + "_ids"], diagnostics[kind + "_ids"])
                self.assertEqual(audit[0]["approval"]["reviewed_chunk_ids"], first["required_review"]["chunk_ids"])
                self.assertEqual(audit[0]["approval"]["reviewed_finding_ids"], first["required_review"]["finding_ids"])
                self.assertEqual(result["usage"]["total_tokens"], len(fake.calls) * 12)
                self.assertEqual(result["specifications"][1]["usage"]["total_tokens"],
                                 result["specifications"][0]["usage"]["total_tokens"] + 12)
                self.assertFalse(any("Root rejected candidate:" in line for line in logs.output))
                warning = next(line for line in logs.output if "Root approval coverage invalid:" in line)
                self.assertIn(kind + "_ids", warning)
                self.assertIn("review_exhausted=False", warning)
                self.assertTrue(warning.isascii())
                query = next(query["query"] for query in fake.queries
                             if "Phase: root_approval\n" in query["query"])
                self.assertIn("not original page numbers, chapter", query)

    async def test_missing_duplicate_and_unknown_ids_share_one_bounded_review_loop(self):
        def mutate(phase, payload, value):
            if phase == "root_approval" and not fake.approved:
                if payload["review_attempt"] == 1:
                    value["reviewed_chunk_ids"] = value["reviewed_chunk_ids"][1:] + [999]
                elif payload["review_attempt"] == 2:
                    value["reviewed_finding_ids"].extend([value["reviewed_finding_ids"][0], "invented"])
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            result = await self.run_flow(fake)
        reviews = [payload for phase, step, payload in fake.calls if phase == "root_approval" and step == 1]
        self.assertEqual([review["review_attempt"] for review in reviews], [1, 2, 3])
        self.assertEqual(reviews[1]["coverage_feedback"]["missing_chunk_ids"], [1])
        self.assertEqual(reviews[1]["coverage_feedback"]["unknown_chunk_ids"], [999])
        self.assertEqual(reviews[2]["coverage_feedback"]["missing_chunk_ids"], [])
        self.assertEqual(reviews[2]["coverage_feedback"]["unknown_finding_ids"], ["invented"])
        self.assertNotIn("coverage_feedback", reviews[2]["coverage_feedback"]["previous_review"])
        self.assertEqual(sum(phase == "map" for phase, _, _ in fake.calls), 28)
        self.assertEqual(len(result["hierarchy"]["stages"][0]["attempts"][0]["approval_review_failures"]), 2)

    async def test_persistent_duplicate_ids_stop_at_configured_review_limit(self):
        for limit in (1, 2, 3):
            with self.subTest(limit=limit):
                def mutate(phase, payload, value):
                    if phase == "root_approval":
                        value["reviewed_chunk_ids"].append(value["reviewed_chunk_ids"][0])
                    return value

                fake = RecordingResponses(self, mutate=mutate)
                with self.assertLogs("server", level="INFO") as logs:
                    with self.assertRaisesRegex(EvidenceError, f"after {limit} review attempts"):
                        await self.run_flow(fake, count=1,
                                            settings={"LLM_MAX_APPROVAL_REVIEW_ATTEMPTS": str(limit)})
                self.assertEqual(sum(phase == "root_approval" for phase, _, _ in fake.calls), limit)
                self.assertEqual(sum(phase == "root_reduce" for phase, _, _ in fake.calls), 1)
                self.assertEqual(sum(phase == "map" for phase, _, _ in fake.calls), 1)
                self.assertFalse(fake.approved)
                self.assertTrue(any("review_exhausted=True" in line for line in logs.output))
                self.assertFalse(any("Root approval decision:" in line for line in logs.output))

    async def test_semantic_rejection_after_identifier_repair_still_requires_full_rescan(self):
        def mutate(phase, payload, value):
            if phase == "root_approval" and payload["attempt"] == 1 and payload["review_attempt"] == 1 and not fake.approved:
                value["reviewed_chunk_ids"].append(999)
            return value

        fake = RecordingResponses(self, reject=1, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            result = await self.run_flow(fake, count=1)
        reviews = [payload for phase, step, payload in fake.calls if phase == "root_approval" and step == 1]
        self.assertEqual([(review["attempt"], review["review_attempt"]) for review in reviews],
                         [(1, 1), (1, 2), (2, 1)])
        attempts = result["hierarchy"]["stages"][0]["attempts"]
        self.assertFalse(attempts[0]["approval"]["approved"])
        self.assertTrue(attempts[1]["approval"]["approved"])
        self.assertFalse(attempts[0]["approval_review_failures"][0]["response"]["approved"])
        self.assertEqual(sum(phase == "map" and step == 1 for phase, step, _ in fake.calls), 2)

    async def test_query_budget_applies_to_identifier_repair_feedback(self):
        baseline = RecordingResponses(self)
        with self.assertLogs("server", level="INFO"):
            await self.run_flow(baseline, count=1)
        first_review = next(index for index, item in enumerate(baseline.queries)
                            if "Phase: root_approval\n" in item["query"])
        # Allow every initial prompt, regardless of which phase has more rules.
        ceiling = max(len(item["query"].encode("utf-8"))
                      for item in baseline.queries[:first_review + 1]) + 32

        def mutate(phase, payload, value):
            if phase == "root_approval":
                value["reviewed_finding_ids"].append("unknown-" + "x" * ceiling)
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO"):
            with self.assertRaisesRegex(EvidenceError, "LLM query budget exceeded"):
                await self.run_flow(fake, count=1, settings={"LLM_MAX_QUERY_BYTES": str(ceiling)})
        self.assertEqual(sum(phase == "root_approval" for phase, _, _ in fake.calls), 1)

    async def test_audit_limit_applies_to_invalid_approval_records(self):
        baseline = RecordingResponses(self)
        with self.assertLogs("server", level="INFO"):
            result = await self.run_flow(baseline, count=1)
        audit = result["hierarchy"]["stages"][0]["attempts"][0]
        stored = [result["hierarchy"]["global_context"], audit["root_context"],
                  *audit["subglobal_contexts"].values(), *audit["scans"],
                  *(node["outcome"] for node in audit["nodes"]), audit["candidate"]]
        ceiling = sum(len(encode(value).encode("utf-8")) for value in stored) + 1

        def mutate(phase, payload, value):
            if phase == "root_approval":
                value["reviewed_chunk_ids"].append(999)
            return value

        fake = RecordingResponses(self, mutate=mutate)
        with self.assertLogs("server", level="INFO") as logs:
            with self.assertRaisesRegex(EvidenceError, "Evidence storage budget exceeded"):
                await self.run_flow(fake, count=1, settings={"LLM_AUDIT_MAX_BYTES": str(ceiling)})
        self.assertEqual(sum(phase == "root_approval" for phase, _, _ in fake.calls), 1)
        self.assertTrue(any("unknown_chunk_ids" in line for line in logs.output))

    async def test_invalid_ids_outside_approval_never_enter_approval_repair(self):
        for target in ("map", "root_reduce"):
            with self.subTest(target=target):
                def mutate(phase, payload, value):
                    if phase == target:
                        if target == "map":
                            value["covered_units"].append(value["covered_units"][0])
                        else:
                            value["decisions"][0]["finding_ids"].append("invented")
                    return value

                fake = RecordingResponses(self, mutate=mutate)
                with self.assertLogs("server", level="INFO"):
                    with self.assertRaises(ExceptionGroup if target == "map" else EvidenceError):
                        await self.run_flow(fake, count=1)
                expected = 1 if target == "map" else hierarchy.ADJUDICATION_MAX_ATTEMPTS
                self.assertEqual(sum(phase == target for phase, _, _ in fake.calls), expected)
                self.assertFalse(any(phase == "root_approval" for phase, _, _ in fake.calls))


if __name__ == "__main__":
    unittest.main()

