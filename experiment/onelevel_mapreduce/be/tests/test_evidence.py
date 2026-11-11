import copy
import unittest

from server.evidence import ApprovalCoverageError, EvidenceError, approval_record


class ApprovalRecordTests(unittest.TestCase):
    def setUp(self):
        self.chunk_ids = list(range(1, 32))
        self.finding_ids = [
            f"screen_functions:r1:c{index % 31 + 1}:f{index // 31 + 1}"
            for index in range(447)
        ]
        self.review = {
            "approved": True,
            "reviewed_chunk_ids": list(self.chunk_ids),
            "reviewed_finding_ids": list(self.finding_ids),
            "rationale": "Checked all source evidence against the candidate.",
            "feedback": [],
        }

    def test_complete_review_accepts_all_447_findings_in_any_order(self):
        self.review["reviewed_finding_ids"].reverse()
        self.review["feedback"] = ["Optional: confirm documented source gaps and improve table formatting."]
        self.assertIs(approval_record(self.review, self.chunk_ids, self.finding_ids), self.review)
        self.assertTrue(self.review["approved"])
        self.assertEqual(len(self.review["feedback"]), 1)

    def test_missing_ids_report_exact_gaps_without_filling_the_review(self):
        self.review["reviewed_chunk_ids"].pop()
        self.review["reviewed_finding_ids"].pop()
        original = copy.deepcopy(self.review)
        with self.assertRaises(ApprovalCoverageError) as raised:
            approval_record(self.review, self.chunk_ids, self.finding_ids)
        error = raised.exception
        self.assertEqual(error.coverage, {
            "reviewed_chunk_count": 30, "expected_chunk_count": 31,
            "reviewed_finding_count": 446, "expected_finding_count": 447,
            "missing_chunk_ids": [31], "missing_finding_ids": [self.finding_ids[-1]],
            "duplicate_chunk_ids": [], "unknown_chunk_ids": [],
            "duplicate_finding_ids": [], "unknown_finding_ids": [],
        })
        self.assertEqual(error.review, original)
        self.assertEqual(self.review, original)
        self.assertIn("reviewed_findings=446/447", str(error))

    def test_malformed_reviews_are_not_classified_as_recoverable_coverage_gaps(self):
        for changes in (
            {"reviewed_chunk_ids": [True]},
            {"reviewed_chunk_ids": ["1"]},
            {"reviewed_chunk_ids": [1.0]},
            {"reviewed_chunk_ids": [[1]]},
            {"reviewed_finding_ids": None},
            {"reviewed_finding_ids": [1]},
            {"reviewed_finding_ids": [{"id": "f1"}]},
            {"reviewed_chunk_ids": [1, 1], "rationale": ""},
            {"reviewed_chunk_ids": [1, 1], "feedback": None},
            {"approved": "true"},
            {"approved": False, "reviewed_finding_ids": []},
        ):
            with self.subTest(changes=list(changes)):
                review = {**self.review, **changes}
                with self.assertRaises(EvidenceError) as raised:
                    approval_record(review, self.chunk_ids, self.finding_ids)
                self.assertNotIsInstance(raised.exception, ApprovalCoverageError)

    def test_missing_duplicate_and_unknown_ids_report_all_issues_without_mutation(self):
        self.review["reviewed_chunk_ids"] = [1, 1, 0, 32, 32]
        self.review["reviewed_finding_ids"] = [self.finding_ids[0], self.finding_ids[0], "invented", "invented"]
        original = copy.deepcopy(self.review)
        with self.assertRaises(ApprovalCoverageError) as raised:
            approval_record(self.review, self.chunk_ids, self.finding_ids)
        self.assertEqual(raised.exception.coverage, {
            "reviewed_chunk_count": 1, "expected_chunk_count": 31,
            "reviewed_finding_count": 1, "expected_finding_count": 447,
            "missing_chunk_ids": self.chunk_ids[1:],
            "missing_finding_ids": sorted(self.finding_ids[1:]),
            "duplicate_chunk_ids": [1, 32], "unknown_chunk_ids": [0, 32],
            "duplicate_finding_ids": sorted([self.finding_ids[0], "invented"]),
            "unknown_finding_ids": ["invented"],
        })
        self.assertEqual(self.review, original)
        self.assertEqual(raised.exception.review, original)
        self.assertIn("duplicate or unknown identifiers", str(raised.exception))

    def test_duplicates_are_invalid_even_when_all_required_ids_are_present(self):
        for field in ("reviewed_chunk_ids", "reviewed_finding_ids"):
            with self.subTest(field=field):
                review = copy.deepcopy(self.review)
                review[field].append(review[field][0])
                with self.assertRaises(ApprovalCoverageError) as raised:
                    approval_record(review, self.chunk_ids, self.finding_ids)
                self.assertEqual(raised.exception.coverage["missing_chunk_ids"], [])
                self.assertEqual(raised.exception.coverage["missing_finding_ids"], [])
                self.assertEqual(raised.exception.coverage["reviewed_chunk_count"], 31)
                self.assertEqual(raised.exception.coverage["reviewed_finding_count"], 447)

    def test_unknown_finding_with_an_empty_ledger_is_repairable_and_not_counted(self):
        self.review["reviewed_finding_ids"] = ["invented"]
        with self.assertRaises(ApprovalCoverageError) as raised:
            approval_record(self.review, self.chunk_ids, [])
        self.assertEqual(raised.exception.coverage["unknown_finding_ids"], ["invented"])
        self.assertEqual(raised.exception.coverage["reviewed_finding_count"], 0)
        self.assertEqual(raised.exception.coverage["expected_finding_count"], 0)

    def test_rejection_requires_coverage_and_preserves_substantive_feedback(self):
        self.review.update(approved=False, feedback=["Correct the unsupported access rule."])
        self.assertIs(approval_record(self.review, self.chunk_ids, self.finding_ids), self.review)
        self.review["reviewed_chunk_ids"].pop()
        with self.assertRaises(ApprovalCoverageError) as raised:
            approval_record(self.review, self.chunk_ids, self.finding_ids)
        self.assertEqual(raised.exception.coverage["missing_chunk_ids"], [31])
        self.assertEqual(raised.exception.coverage["missing_finding_ids"], [])
        self.assertFalse(raised.exception.review["approved"])
        self.assertEqual(raised.exception.review["feedback"], ["Correct the unsupported access rule."])

    def test_empty_finding_ledger_still_requires_all_chunks(self):
        self.review["reviewed_finding_ids"] = []
        self.assertIs(approval_record(self.review, self.chunk_ids, []), self.review)
        self.review["reviewed_chunk_ids"] = []
        with self.assertRaises(ApprovalCoverageError):
            approval_record(self.review, self.chunk_ids, [])


if __name__ == "__main__":
    unittest.main()

