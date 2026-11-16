"""Validate full-document approval without repairing the model's review IDs."""

import json
from collections import Counter


class ApprovalError(RuntimeError):
    pass


class ApprovalCoverageError(ApprovalError):
    def __init__(self, review, source_unit_ids):
        self.review = review
        expected = set(source_unit_ids)
        counts = Counter(review["reviewed_source_unit_ids"])
        reported = set(counts)
        self.coverage = {
            "reviewed_source_unit_count": len(reported & expected),
            "expected_source_unit_count": len(expected),
            "missing_source_unit_ids": sorted(expected - reported),
            "duplicate_source_unit_ids": sorted(key for key, count in counts.items() if count > 1),
            "unknown_source_unit_ids": sorted(reported - expected),
        }
        super().__init__(
            "Full-file approval reported missing, duplicate, or unknown source unit IDs: "
            f"reviewed={self.coverage['reviewed_source_unit_count']}/{len(expected)}"
        )


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def require(condition, message):
    if not condition:
        raise ApprovalError(message)


def approval_record(value, source_unit_ids):
    require(isinstance(value, dict), "Approval must be a JSON object")
    require(type(value.get("approved")) is bool, "Reviewer must explicitly approve or reject")
    reviewed = value.get("reviewed_source_unit_ids")
    require(isinstance(reviewed, list), "reviewed_source_unit_ids must be a JSON array")
    require(all(type(item) is int for item in reviewed), "Invalid identifier type: reviewed_source_unit_ids")
    rationale = value.get("rationale")
    require(isinstance(rationale, str) and bool(rationale.strip()), "Approval rationale must be non-empty text")
    feedback = value.get("feedback")
    require(isinstance(feedback, list), "Approval feedback must be a JSON array")
    require(all(isinstance(item, str) and bool(item.strip()) for item in feedback),
            "Approval feedback items must be non-empty text")
    require(value["approved"] or bool(feedback), "Rejection must include actionable feedback")
    expected = set(source_unit_ids)
    if set(reviewed) != expected or len(reviewed) != len(expected):
        raise ApprovalCoverageError(value, expected)
    return value
