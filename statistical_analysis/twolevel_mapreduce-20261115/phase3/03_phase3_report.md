# OrionDesk AI — Phase 3 Semantic Source-Coverage Report

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** OrionDesk Six-Turn Semantic-Entailment Atomic Requirement Evaluation Protocol, v6.1  
**Current work package:** Phase 3 only; no Phase 4 correctness judgment or full confusion matrix has been computed.  
**Scored corpus:** Eight unchanged Markdown files and original 90-physical-page English PDF, `OD-AI-DDS-001`, R1.0 / revision 1.3.  
**Shared source-positive inventory:** The user-specified Phase 1 JSONL, unchanged in this phase.

## Scope and provisional results

| Item | Count | Interpretation |
|---|---:|---|
| Fixed PDF-positive source atoms | 1,024 | Shared universe from Phase 1; no source-denominator changes |
| Fixed PDF-negative controls | 37 | Carried into the draft canonical ledger, **not yet classified** as TN or FP |
| Eligible generated occurrences | 3,116 | Retained Phase 2 occurrence inventory |
| Raw generated semantic classes | 3,020 | Retained Phase 2 class inventory |
| Provisional source-side TP | 943 | Evidence-linked coverage decisions, not final independently certified semantic proofs |
| Conservative FN | 81 | Uncovered or not fully proven after reciprocal retrieval |
| Source-side draft coverage ratio | 92.0898% | **Not** the final/certified Recall and not a complete TP/TN/FP/FN result |
| Direct TP-grade evidence | 14 | Explicit source-to-generated statement matches |
| Contextual/semantic TP-grade evidence | 929 | Requires independent complete-predicate re-audit before semantic certification |
| Logged TP bridges | 929 | Scope membership and documented conjunctive/universal justification |
| Initially missed lexical-only candidates corrected | 861 | Corrections relative to this run's **deliberately narrow initial lexical threshold**, not corrections to a prior published score |

**Important:** The large lexical-correction count does not prove the corrected TP judgments are infallible. The source denominator itself still requires an independent atomization challenge. Both directions of error can move later results: an overlooked complete match may become TP, while an over-permissive bridge may become FN.

## Mandatory false-negative challenge

Every final FN has an evidence-bearing root-cause record with the strongest located actual generated candidates, original file/line/table coordinates, exact/alias search keys, a missing-predicate explanation, and the explicit limitation of universal/shared and conjunction alternatives.

| Root-cause disposition | Final FN |
|---|---:|
| `TRUE_MISSING` | 2 |
| `PARTIAL_ENTAILMENT` | 25 |
| `CONSERVATIVE_UNRESOLVED` | 54 |
| **Total** | **81** |

The two explicitly missing source paths concern `PUT /v1/workspaces/{workspaceId}/me`; these were not silently equated to the supplied membership endpoint. This is a source-inventory-specific observation, not a recommendation to add or invent a new endpoint. Other E1/E0 decisions remain conservative rather than certified negative statements.

## Bidirectional retrieval and regression probes

For each source atom the audit considered direct content matches, variants of API paths, data entities/fields, states/codes, registered events, formal tests, inherited Markdown table/row context, and explicitly applicable shared or universal rules. Generated-to-source review also considered class membership and candidate scope before making a conservative FN determination.

Three named high-risk regression patterns were explicitly checked from the **actual current input inventory**: the case title field, the workspace retention-class field, and same-key changed-body creation producing `409 IDEMPOTENCY_CONFLICT`. These have source evidence and generated-coverage references in `03_structural_validation.json`. No previous run's atom numbers were used as authoritative labels.

## Source atomization and generated-corpus limitations

102 source atoms are flagged for continued atomization scrutiny, including repeated cross-component verification language, event-wide logging clauses, common validation obligations, and the partly illustrative A2A JSON envelope. None was silently deleted or assigned a new PDF requirement. Full independent atomization correction belongs to the Phase 5 source audit; decisive matches found in the present turn were corrected in the present turn.

326 currently unassociated generated classes are **candidate checks only**, not unsupported claims and not FPs. Phase 4 must search each against the authoritative PDF and distinguish `PDF_ENTAILED`, `SUPPORTED_NONCOVERING`, and `PDF_UNSUPPORTED`, and then assess the 37 fixed negative controls and construct `F_m`.

The status is best effort because automated retrieval, contextual table joins, and representative manual spot checks cannot certify all 943 positive predicate proofs. In particular, generic-rule applicability, test-obligation versus behavior-obligation distinction, and register-family context require an independent exhaustive semantic audit. Structural arithmetic alone is not semantic certification.

## Phase 3 audit invariants

- Exactly one binary source-coverage judgment exists for every one of the 1,024 fixed PDF-positive atoms.
- Every TP points to an actual PDF quote and one or more unchanged generated Markdown file lines and class IDs.
- Every final FN has exactly one admissible final root-cause disposition; corrected candidate misses are retained separately without double-counting.
- All eight scored Markdown inputs are mounted, referenced file-line excerpts resolve exactly, and the PDF identity and 90-page extent were rechecked.
- The 37 fixed negative controls remain pending, rather than being misrepresented as automatically true negatives.
- **No full four-cell Precision, Recall or F1 has been calculated or certified in Phase 3.**

## Individually delivered files

1. `03_canonical_universe_final.jsonl` — draft canonical source-positive and fixed-negative units (negative prediction fields intentionally pending).
2. `03_evidence_matches_final.jsonl` — one source judgment per atom, with original quotes, generated evidence and predicate explanations.
3. `03_semantic_coverage_bridges_final.jsonl` — direct-source-independent E2 applicability and conjunction bridges.
4. `03_fn_root_cause_audit_final.jsonl` — final FN and corrected lexical candidate FN audit entries.
5. `03_source_atomization_review_candidates.jsonl` — phase-specific PDF atomization QA flags, not denominator changes.
6. `03_unmatched_generated_class_candidates.jsonl` — prospective Phase 4 correctness targets, not scored FPs.
7. `03_structural_validation.json` — item-level consistency checks and source-derived regression probes.
8. `03_phase3_validation.json` — current phase scope, counts and qualifications.

**Phase boundary:** Phase 3 closed once with `PHASE_COMPLETED_BEST_EFFORT`. Phase 4 was not run. Phase 4 will build the generated-claim validity ledger, distinguish source-negative assertions and generated-only unsupported propositions, and calculate all four cells on one canonical decision universe.
