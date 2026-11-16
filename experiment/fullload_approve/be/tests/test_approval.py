import asyncio
import base64
import copy
import json
import re
import unittest
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from approval_fixtures import payload, pdf_bytes, pptx_bytes, revision_feedback
from server.approval import ApprovalCoverageError, ApprovalError, approval_record
from server.chat import generate_specifications
from server.input_files import source_manifest
from server.models import AppServices
from server.specifications import SPECIFICATION_STAGES, stage_context


def complete_review():
    return {"approved": True, "reviewed_source_unit_ids": [1, 2],
            "rationale": "Checked the original source against the candidate.", "feedback": []}


class ApprovalRecordTests(unittest.TestCase):
    def test_complete_approval_and_rejection_preserve_response(self):
        for approved in (True, False):
            review = complete_review()
            review.update(approved=approved, feedback=["Correct the access rule on source page 2."])
            review["reviewed_source_unit_ids"].reverse()
            self.assertIs(approval_record(review, [1, 2]), review)

    def test_missing_duplicate_unknown_ids_are_reported_without_modification(self):
        review = complete_review()
        review["reviewed_source_unit_ids"] = [1, 1, 999]
        original = copy.deepcopy(review)
        with self.assertRaises(ApprovalCoverageError) as raised:
            approval_record(review, [1, 2])
        self.assertEqual(review, original)
        self.assertEqual(raised.exception.review, original)
        self.assertEqual(raised.exception.coverage, {
            "reviewed_source_unit_count": 1, "expected_source_unit_count": 2,
            "missing_source_unit_ids": [2], "duplicate_source_unit_ids": [1], "unknown_source_unit_ids": [999],
        })

    def test_malformed_fields_are_fatal_even_when_coverage_is_invalid(self):
        for changes in (
            {"approved": "true"}, {"reviewed_source_unit_ids": [True]},
            {"reviewed_source_unit_ids": ["1"]}, {"reviewed_source_unit_ids": [1.0]},
            {"reviewed_source_unit_ids": None}, {"rationale": " "}, {"feedback": None},
            {"feedback": [""]}, {"feedback": [1]}, {"approved": False, "feedback": []},
        ):
            with self.subTest(changes=changes):
                review = {**complete_review(), "reviewed_source_unit_ids": [1, 1], **changes}
                with self.assertRaises(ApprovalError) as raised:
                    approval_record(review, [1, 2])
                self.assertNotIsInstance(raised.exception, ApprovalCoverageError)

    def test_source_manifest_counts_real_pages_and_slides(self):
        for data, name, kind in ((pdf_bytes(3), "source.PDF", "page"), (pptx_bytes(3), "source.PPTX", "slide")):
            with self.subTest(name=name):
                self.assertEqual(source_manifest(data, name), {
                    "file_name": name, "unit_kind": kind, "source_unit_ids": [1, 2, 3],
                })

    def test_invalid_and_zero_unit_documents_are_rejected(self):
        for data, name in ((b"invalid", "source.pdf"), (b"invalid", "source.pptx"),
                           (pdf_bytes(0), "source.pdf"), (pptx_bytes(0), "source.pptx")):
            with self.subTest(name=name, size=len(data)), self.assertRaises(HTTPException) as raised:
                source_manifest(data, name)
            self.assertEqual(raised.exception.status_code, 400)


class FullFileApprovalTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        settings = patch.dict("os.environ", {name: "" for name in (
            "LLM_MAX_OUTPUT_TOKENS", "LLM_INTERMEDIATE_MAX_OUTPUT_TOKENS", "LLM_MAX_APPROVAL_ATTEMPTS",
            "LLM_MAX_APPROVAL_REVIEW_ATTEMPTS", "LLM_MAX_QUERY_BYTES", "LLM_FINAL_MAX_BYTES",
            "LLM_INTERMEDIATE_MAX_BYTES", "LLM_AUDIT_MAX_BYTES",
        )})
        settings.start()
        self.addCleanup(settings.stop)
        self.requests = []
        self.saved = []

    async def run_flow(self, mutate=None, settings=None, data=None, filename="source.pdf"):
        data = pdf_bytes() if data is None else data

        async def create_response(**request):
            step = int(re.search(r"^Stage: (\d+)/8$", request["query"], re.M)[1])
            phase = "approval" if request.get("json_output") else "decision_register" if step == 8 else "generation"
            if phase == "approval":
                detail = payload(request["query"])
            elif phase == "generation":
                detail = {
                    "attempt": 1 + sum(prior_phase == "generation" and prior_step == step
                                       for prior_phase, prior_step, *_ in self.requests),
                    "feedback": revision_feedback(request["query"]),
                }
            else:
                detail = {}
            self.requests.append((phase, step, detail, request))
            if phase == "approval":
                value = complete_review()
                value["reviewed_source_unit_ids"] = detail["required_review"]["source_unit_ids"][:]
            else:
                value = f"## Content\nGenerated specification {step}, attempt {detail.get('attempt', 1)}."
            if mutate:
                value = mutate(phase, step, detail, value)
            return SimpleNamespace(output_text=json.dumps(value) if phase == "approval" and isinstance(value, dict) else value,
                                   usage=SimpleNamespace(input_tokens=1, output_tokens=2, total_tokens=3))

        async def save(result):
            self.saved.append(result)

        with patch.dict("os.environ", settings or {}), self.assertLogs("server", level="INFO") as logs:
            result = await generate_specifications(
                AppServices(responses=SimpleNamespace(create_response=create_response)), data, filename,
                on_stage_completed=save,
            )
        return result, logs.output

    async def test_initial_generation_matches_fullload_for_all_seven_stages(self):
        baseline_dir = Path(__file__).resolve().parents[3] / "fullload" / "be" / "prompt"
        baseline = Environment(loader=FileSystemLoader(str(baseline_dir)), undefined=StrictUndefined)
        result, _ = await self.run_flow()
        generation_requests = [(step, request) for phase, step, _, request in self.requests if phase == "generation"]
        self.assertEqual([step for step, _ in generation_requests], list(range(1, 8)))
        for step, request in generation_requests:
            with self.subTest(step=step):
                stage = SPECIFICATION_STAGES[step - 1]
                expected = baseline.get_template(stage.prompt_template).render(
                    **stage_context(stage, "source.pdf", result["specifications"][:step - 1]),
                )
                self.assertEqual(request["query"], expected)
                self.assertEqual(request["assistant_instruction"], baseline.get_template("specification_system.jinja2").render())
                self.assertNotIn("<payload>", request["query"])
                self.assertNotIn("<revision_feedback>", request["query"])
                self.assertFalse(request["json_output"])

    async def test_approval_reads_whole_attachment_and_optional_feedback_does_not_regenerate(self):
        def mutate(phase, step, detail, value):
            if phase == "approval":
                value["feedback"] = ["Optional: confirm the documented source gaps."]
            return value

        result, _ = await self.run_flow(mutate, data=pptx_bytes(3), filename="source.pptx")
        self.assertEqual(Counter(phase for phase, *_ in self.requests), {"generation": 7, "approval": 7, "decision_register": 1})
        self.assertEqual(result["usage"], {"input_tokens": 15, "output_tokens": 30, "total_tokens": 45})
        for phase, step, detail, request in self.requests:
            if step < 8:
                self.assertIn("base64,", request["input_file"]["file_data"])
                if phase == "approval":
                    self.assertEqual(detail["source"]["source_unit_ids"], [1, 2, 3])
                    self.assertEqual(detail["source"]["unit_kind"], "slide")
                    self.assertEqual(detail["candidate"], result["approval_audit"]["stages"][step - 1]["attempts"][0]["candidate"])
                    self.assertIn("Phase: approval", request["query"])
                else:
                    self.assertNotIn("<payload>", request["query"])
                    self.assertNotIn("<revision_feedback>", request["query"])
            else:
                self.assertIsNone(request["input_file"])
                self.assertNotIn("<payload>", request["query"])
        self.assertEqual(len(self.saved[0]["approval_audit"]["stages"]), 1)
        self.assertEqual([len(item["specifications"]) for item in self.saved], list(range(1, 9)))

    async def test_rejection_regenerates_only_current_stage_with_blocking_feedback(self):
        correction = "Source page 2 denies suspended administrators; replace the candidate's allow-all rule."

        def mutate(phase, step, detail, value):
            if phase == "approval" and step == 2 and detail["attempt"] == 1:
                value.update(approved=False, feedback=[correction])
            return value

        data = pdf_bytes()
        result, logs = await self.run_flow(mutate, data=data)
        stage_two = [(phase, detail) for phase, step, detail, _ in self.requests if step == 2]
        self.assertEqual([(phase, detail["attempt"]) for phase, detail in stage_two],
                         [("generation", 1), ("approval", 1), ("generation", 2), ("approval", 2)])
        self.assertEqual(stage_two[2][1]["feedback"], [correction])
        generation_queries = [request["query"] for phase, step, _, request in self.requests if phase == "generation" and step == 2]
        self.assertTrue(generation_queries[1].startswith(generation_queries[0] + "\n\n"))
        self.assertNotIn("<revision_feedback>", generation_queries[0])
        self.assertIn(correction, generation_queries[1])
        self.assertNotIn("<payload>", generation_queries[1])
        self.assertEqual(sum(phase == "generation" and step == 1 for phase, step, *_ in self.requests), 1)
        for phase, step, _, request in self.requests:
            if step < 8:
                self.assertEqual(base64.b64decode(request["input_file"]["file_data"].split(",", 1)[1]), data)
        attempts = result["approval_audit"]["stages"][1]["attempts"]
        self.assertEqual([item["approval"]["approved"] for item in attempts], [False, True])
        self.assertIn("attempt 2", result["specifications"][1]["content"])
        self.assertEqual(result["specifications"][1]["usage"]["total_tokens"], 12)
        self.assertTrue(any("Full-file rejected candidate:" in line for line in logs))

    async def test_missing_duplicate_unknown_ids_share_review_budget_and_keep_candidate(self):
        def mutate(phase, step, detail, value):
            if phase == "approval" and step == 1:
                if detail["review_attempt"] == 1:
                    value["reviewed_source_unit_ids"] = [1]
                elif detail["review_attempt"] == 2:
                    value["reviewed_source_unit_ids"] = [1, 2, 2, 999]
            return value

        result, logs = await self.run_flow(mutate)
        reviews = [detail for phase, step, detail, _ in self.requests if phase == "approval" and step == 1]
        self.assertEqual([item["review_attempt"] for item in reviews], [1, 2, 3])
        self.assertTrue(all(item["candidate"] == reviews[0]["candidate"] for item in reviews))
        self.assertEqual(reviews[1]["coverage_feedback"]["missing_source_unit_ids"], [2])
        self.assertEqual(reviews[2]["coverage_feedback"]["duplicate_source_unit_ids"], [2])
        self.assertEqual(reviews[2]["coverage_feedback"]["unknown_source_unit_ids"], [999])
        self.assertEqual(sum(phase == "generation" and step == 1 for phase, step, *_ in self.requests), 1)
        self.assertEqual(len(result["approval_audit"]["stages"][0]["attempts"][0]["approval_review_failures"]), 2)
        self.assertEqual(result["specifications"][0]["usage"]["total_tokens"], 12)
        self.assertEqual(sum("Full-file approval coverage invalid:" in line for line in logs), 2)

    async def test_rejection_with_invalid_ids_is_reviewed_again_before_regeneration(self):
        def mutate(phase, step, detail, value):
            if phase == "approval" and step == 1 and detail["attempt"] == 1:
                value.update(approved=False, feedback=["Correct the exception on page 2."])
                if detail["review_attempt"] == 1:
                    value["reviewed_source_unit_ids"] = [1, 999]
            return value

        result, _ = await self.run_flow(mutate)
        reviews = [detail for phase, step, detail, _ in self.requests if phase == "approval" and step == 1]
        self.assertEqual([(item["attempt"], item["review_attempt"]) for item in reviews], [(1, 1), (1, 2), (2, 1)])
        self.assertFalse(reviews[1]["coverage_feedback"]["previous_review"]["approved"])
        self.assertEqual([item["approval"]["approved"] for item in result["approval_audit"]["stages"][0]["attempts"]], [False, True])

    async def test_persistent_rejection_stops_at_configured_limit_without_saving(self):
        def mutate(phase, step, detail, value):
            if phase == "approval":
                value.update(approved=False, feedback=["Fix the source rule on page 1."])
            return value

        with self.assertRaisesRegex(ApprovalError, "after 2 full-file attempts"):
            await self.run_flow(mutate, settings={"LLM_MAX_APPROVAL_ATTEMPTS": "2"})
        self.assertEqual(Counter(phase for phase, *_ in self.requests), {"generation": 2, "approval": 2})
        self.assertEqual(self.saved, [])

    async def test_persistent_coverage_errors_stop_without_regeneration(self):
        def mutate(phase, step, detail, value):
            if phase == "approval":
                value["reviewed_source_unit_ids"].append(999)
            return value

        with self.assertRaisesRegex(ApprovalError, "after 3 review attempts"):
            await self.run_flow(mutate)
        self.assertEqual(Counter(phase for phase, *_ in self.requests), {"generation": 1, "approval": 3})
        self.assertEqual(self.saved, [])

    async def test_malformed_review_and_api_failure_stop_without_semantic_retries(self):
        for failure in ("not JSON", {"approved": "true"}, RuntimeError("Approval API failed"), asyncio.CancelledError()):
            with self.subTest(failure=repr(failure)):
                self.requests.clear()

                def mutate(phase, step, detail, value):
                    if phase == "approval":
                        if isinstance(failure, BaseException):
                            raise failure
                        return failure
                    return value

                expected = asyncio.CancelledError if isinstance(failure, asyncio.CancelledError) else RuntimeError
                with self.assertRaises(expected):
                    await self.run_flow(mutate)
                self.assertEqual(len(self.requests), 2)
                self.assertEqual(self.saved, [])

    async def test_query_output_and_audit_budgets_fail_without_saving(self):
        for settings, message in (
            ({"LLM_MAX_QUERY_BYTES": "1"}, "query budget"),
            ({"LLM_FINAL_MAX_BYTES": "1"}, "output exceeded"),
            ({"LLM_INTERMEDIATE_MAX_BYTES": "1"}, "output exceeded"),
            ({"LLM_AUDIT_MAX_BYTES": "1"}, "audit budget"),
        ):
            with self.subTest(settings=settings), self.assertRaisesRegex(ApprovalError, message):
                await self.run_flow(settings=settings)
            self.assertEqual(self.saved, [])
