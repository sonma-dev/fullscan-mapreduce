# Phase 3 — Revised Semantic Source Coverage (Protocol 6.1)

**Status:** `PHASE_COMPLETED_BEST_EFFORT`. Only Phase 3 has been rerun.

## Fixed source and generated inventory

- Original PDF-positive atoms: 1024.
- Source atomization audit: 16 named Appendix E tests retained as independent minimum-release verification obligations; no source atoms removed.
- Corrected PDF-positive requirement universe: **1024**.
- Fixed negative controls: 37; assertion checks deferred to Phase 4.
- Eligible generated occurrences: **3358**.
- Raw generated classes: **3229**.
- Targeted Phase-2 short-cell extraction repairs: **23** (recorded in `03_change_delta.jsonl`).

## Source-side semantic coverage decisions

- TP: **590**.
- FN: **434**.
- Draft source-side Recall: **57.62%**. This is not semantically certified and should not be used as a comparative final metric.
- Initially missed FN candidates challenged: 527.
- FN→TP source-coverage corrections: **93**.
- Source test-overlap/atomization changes: **0** (16 independent acceptance tests retained).
- E2 bridge proofs: **574**.
- Initial TP records audited: **497**.

## Remaining FN root-cause register

| Disposition | Count |
|---|---:|
| `CONSERVATIVE_UNRESOLVED` | 232 |
| `PARTIAL_ENTAILMENT` | 202 |

## Predicate and reciprocal evidence checks

Every initially uncovered PDF atom has one `03_fn_root_cause_audit_final.jsonl` entry, including corrected TPs and independently verified acceptance tests. Actual generated candidate locators and source quotations are preserved. New short-cell classes were created only where the original eight-file table row definitively declares an exact API success code, database default, actor grant, explicit field, wire type or state enumeration. Existing accepted test rows were combined as scenario-plus-outcome evidence without duplicating generated classes. No unadopted proposals were used. Every current TP is represented by a predicate-map and one or more original physical generated file/line citations.

## Numerator/denominator interpretation

The earlier 48.54% is superseded by the new source-to-generated judgments for the same original 1,024-atom source inventory. The new source-side ratio is a provisional semantic coverage assessment, not a verified measure of implementation completeness. Cases classified as `CONSERVATIVE_UNRESOLVED` do not establish real missing features; `PARTIAL_ENTAILMENT` denotes that a complete proof was not found under the finite evidence checks. The 16 explicitly named Appendix E verification scenarios remain in the shared R inventory because their execution/verification obligation is distinct from application functionality. No source denominator reduction was adopted; this decision must be applied to every method.

## Phase boundaries

This Phase 3 draft universe includes all source-positive units and unscored negative controls only. It does not include generated-only unsupported F propositions, asserted B controls, final TN/FP or final Precision/F1/Duplicate. Earlier Phase 4-6 judgments and scores remain invalid for the revised R and must be recalculated in their respective phases. No Phase 4 work was performed.

## Structural checks

- TP + FN = 590 + 434 = 1024.
- Initial FN root cause records: 527.
- Final TPs with predicate audit: 590.
- E2 bridge records: 574.
- Original Markdown evidence locators checked against actual line fragments.
- Each eligible generated occurrence is assigned to one generated semantic class.
- Negative controls are not prematurely scored as TN.
- Original input files are unchanged.

## Files

- `01_source_atoms_final.jsonl` (corrected shared R)
- `02_generated_atoms_final.jsonl` and `02_generated_classes_final.jsonl` (short-cell extraction repairs)
- `03_canonical_universe_final.jsonl`
- `03_evidence_matches_final.jsonl`
- `03_semantic_coverage_bridges_final.jsonl`
- `03_fn_root_cause_audit_final.jsonl`
- `03_tp_predicate_audit_draft.jsonl`
- `03_source_atomization_delta.jsonl`
- `03_change_delta.jsonl`
- `03_potential_generated_only_claims_review_queue.jsonl`
- `03_phase_status_final.json`
