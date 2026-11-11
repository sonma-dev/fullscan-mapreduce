"""Validate model records before allowing them to cross a hierarchy boundary."""

import json
from collections import Counter


class EvidenceError(RuntimeError):
    pass


EVIDENCE_STRENGTHS = ("explicit", "inferred", "uncertain")


class MapStrengthError(EvidenceError):
    def __init__(self, outcome, issues):
        self.outcome = outcome
        self.issues = issues
        indices = ", ".join(str(issue["finding_index"]) for issue in issues)
        super().__init__(f"Invalid evidence strength: finding_indices=[{indices}]")


class RelationCardinalityError(EvidenceError):
    def __init__(self, outcome, issues):
        self.outcome = outcome
        self.issues = issues
        indices = ", ".join(str(issue["relation_index"]) for issue in issues)
        super().__init__(f"Relation needs at least two findings: relation_indices=[{indices}]")


class ApprovalCoverageError(EvidenceError):
    def __init__(self, review, chunk_ids, finding_ids):
        self.review = review
        self.coverage = {}
        for kind, expected in (("chunk", set(chunk_ids)), ("finding", set(finding_ids))):
            counts = Counter(review[f"reviewed_{kind}_ids"])
            reported = set(counts)
            self.coverage.update({
                # Count only distinct allowed IDs; duplicates cannot inflate coverage.
                f"reviewed_{kind}_count": len(reported & expected),
                f"expected_{kind}_count": len(expected),
                f"missing_{kind}_ids": sorted(expected - reported),
                f"duplicate_{kind}_ids": sorted(key for key, count in counts.items() if count > 1),
                f"unknown_{kind}_ids": sorted(reported - expected),
            })
        invalid = {key: len(value) for key, value in self.coverage.items()
                   if key.startswith(("duplicate_", "unknown_")) and value}
        if invalid:
            message = "Root approval reported duplicate or unknown identifiers"
        else:
            message = "Root did not review all evidence" if self.coverage["missing_finding_ids"] else "Root did not review all chunks"
        super().__init__(
            f"{message}: reviewed_chunks={self.coverage['reviewed_chunk_count']}/{len(chunk_ids)} "
            f"reviewed_findings={self.coverage['reviewed_finding_count']}/{len(finding_ids)}"
            + (f" invalid_id_counts={invalid}" if invalid else "")
        )


def encode(value) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def require(condition: bool, message: str):
    if not condition:
        raise EvidenceError(message)


def record(value):
    require(isinstance(value, dict), "Expected a JSON object")
    return value


def string(value):
    require(isinstance(value, str) and bool(value.strip()), "Expected non-empty text")
    return value


def array(value):
    require(isinstance(value, list), "Expected a JSON array")
    return value


def strings(value):
    return [string(item) for item in array(value)]


def ids(value, allowed):
    values = array(value)
    require(all(type(item) is type(next(iter(allowed), "")) for item in values), "Invalid identifier type")
    require(len(values) == len(set(values)) and set(values) <= set(allowed), "Duplicate or unknown identifiers")
    return values


def plan_record(value, chunks):
    record(value)
    string(value.get("global_context"))
    groups = array(value.get("groups"))
    require(bool(groups), "Document plan has no semantic jurisdictions")
    covered = []
    for index, group in enumerate(groups, 1):
        record(group)
        string(group.get("title"))
        string(group.get("context"))
        string(group.get("basis"))
        members = ids(group.get("chunk_ids"), range(1, len(chunks) + 1))
        require(bool(members), "Empty semantic jurisdiction")
        require(members == list(range(members[0], members[-1] + 1)), "Jurisdictions must preserve document order")
        # Native sections cannot be split or mixed by the semantic planner.
        labels = {chunks[member - 1].section_id for member in members}
        require(len(labels) == 1, "Jurisdiction crosses a native section boundary")
        group["id"] = f"section-{index}"
        covered.extend(members)
    require(covered == list(range(1, len(chunks) + 1)), "Plan must cover every chunk exactly once in order")
    for section in {chunk.section_id for chunk in chunks if chunk.section_id}:
        owners = [group["id"] for group in groups if any(chunks[i - 1].section_id == section for i in group["chunk_ids"])]
        require(len(owners) == 1, "Native section must have a single adjudicator")
    return value


def context_record(value):
    record(value)
    string(value.get("context"))
    strings(value.get("focus"))
    strings(value.get("cross_scope_checks"))
    return value


def map_record(value, chunk, stage_key, attempt):
    record(value)
    covered = ids(value.get("covered_units"), range(chunk.start, chunk.end + 1))
    require(sorted(covered) == list(range(chunk.start, chunk.end + 1)), "Worker did not account for every source unit")
    strings(value.get("gaps"))
    findings = array(value.get("findings"))
    require(bool(findings) or bool(value["gaps"]), "An empty scan must explain missing evidence")
    strength_issues = []
    for index, finding in enumerate(findings, 1):
        record(finding)
        string(finding.get("statement"))
        string(finding.get("scope"))
        strength = finding.get("strength")
        if not isinstance(strength, str) or strength not in EVIDENCE_STRENGTHS:
            strength_issues.append({
                "finding_index": index - 1, "missing": "strength" not in finding, "value": strength,
            })
        strings(finding.get("conditions"))
        strings(finding.get("exceptions"))
        sources = array(finding.get("sources"))
        require(bool(sources), "A finding must retain source evidence")
        for source in sources:
            record(source)
            require(type(source.get("unit")) is int and chunk.start <= source["unit"] <= chunk.end, "Source outside worker jurisdiction")
            string(source.get("quote"))
    # Only strength errors in otherwise valid records are repairable. Preserve
    # the original output for diagnostics before adding server-owned metadata.
    if strength_issues:
        raise MapStrengthError(value, strength_issues)
    for index, finding in enumerate(findings, 1):
        finding["id"] = f"{stage_key}:r{attempt}:c{chunk.index}:f{index}"
    value["chunk_id"] = chunk.index
    return value


def adjudication_record(value, finding_ids, *, candidate=False):
    record(value)
    string(value.get("summary"))
    if candidate:
        string(value.get("body"))
    accounted = []
    for decision in array(value.get("decisions")):
        record(decision)
        members = ids(decision.get("finding_ids"), finding_ids)
        require(bool(members), "Decision must identify evidence")
        require(decision.get("verdict") in {"supported", "qualified", "contradicted", "unresolved"}, "Invalid adjudication verdict")
        string(decision.get("statement"))
        string(decision.get("rationale"))
        accounted.extend(members)
    require(set(accounted) == set(finding_ids), "Adjudicator silently dropped evidence")
    relation_issues = []
    for index, relation in enumerate(array(value.get("relations"))):
        record(relation)
        require(relation.get("kind") in {"support", "contradiction", "qualification", "exception"}, "Invalid evidence relation")
        members = ids(relation.get("finding_ids"), finding_ids)
        if len(members) < 2:
            relation_issues.append({"relation_index": index, "finding_ids": list(members), "minimum_findings": 2})
        string(relation.get("rationale"))
        string(relation.get("resolution"))
    strings(value.get("gaps"))
    # Other schema/provenance errors must remain fatal, even if a short relation
    # appeared earlier. Only otherwise-valid outcomes enter the repair loop.
    if relation_issues:
        raise RelationCardinalityError(value, relation_issues)
    return value


def approval_record(value, chunk_ids, finding_ids):
    record(value)
    require(type(value.get("approved")) is bool, "Root must explicitly approve or reject")
    chunk_ids, finding_ids = set(chunk_ids), set(finding_ids)
    reviewed_chunks = array(value.get("reviewed_chunk_ids"))
    reviewed_findings = array(value.get("reviewed_finding_ids"))
    require(all(type(item) is int for item in reviewed_chunks), "Invalid identifier type: reviewed_chunk_ids")
    require(all(type(item) is str for item in reviewed_findings), "Invalid identifier type: reviewed_finding_ids")
    string(value.get("rationale"))
    feedback = strings(value.get("feedback"))
    require(value["approved"] or bool(feedback), "Rejection must include actionable feedback")
    # Keep the submitted arrays intact. Membership, uniqueness, and completeness
    # failures all need a fresh approval review of the same candidate/evidence.
    if (set(reviewed_chunks) != chunk_ids or len(reviewed_chunks) != len(chunk_ids)
            or set(reviewed_findings) != finding_ids or len(reviewed_findings) != len(finding_ids)):
        raise ApprovalCoverageError(value, chunk_ids, finding_ids)
    return value
