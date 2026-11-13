# OrionDesk AI — Phase 3 Semantic Source-Coverage Report

**Protocol:** version 6.1  
**Phase:** 3 only, completed  
**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Generated-set label:** `fullload` inherited from Phase 2 metadata; original method provenance not independently verified.  
**Primary PDF:** `OrionDesk_AI_Detailed_Design_Specification(3).pdf`, 90 physical pages.  
**Source baseline:** reused immutable Phase 1 positive (`R`) and bounded negative (`N`) inventories.

## Coverage-stage outputs (not a four-cell matrix)

| Phase 3 statistic | Provisional result |
|---|---:|
| PDF-positive source atoms | 1,024 |
| Source atoms with a documented TP-grade direct or logical bridge | 495 |
| Source atoms without a complete demonstrated bridge (conservative FN) | 529 |
| E3 direct source propositions | 25 |
| E2 equivalence, inherited-context, universal and conjunctive bridges | 470 |
| E1 partly matched / materially unproven | 470 |
| E0 no defensible source predicate bridge | 59 |
| Initial FN candidates challenged | 705 |
| Initial FN errors corrected to TP with actual evidence | 177 |
| Final PARTIAL_ENTAILMENT | 470 |
| Final CONSERVATIVE_UNRESOLVED | 59 |
| Final TRUE_MISSING | 0 |
| Fixed negative controls carried forward without prediction | 37 |

**Interpretation:** The ratio of evidenced source-positive TP records to the reused source inventory is **48.34%**. This is **only a provisional Phase 3 source-coverage fraction**, *not* the final audited Recall, not a complete confusion matrix, and not a verified rate of missing requirements. Its numerator and denominator remain subject to independent complete-predicate and source-atomization review in Phase 5. A conservative FN can be a retrieval/interpretation gap, and even an apparent TP can lack a full predicate if a contextual table row was overinterpreted.

## Retrieval and reciprocal evidence challenges

The phase consumed all eight unchanged Markdown files (8,330 physical lines and 14,882 table cells as inventoried in Phase 2), with 6,581 extracted occurrences and 6,527 conservative generated classes. Candidate retrieval combined word/character n-grams, uncapped exact route and identifier lookups, named field tables, original row/column context, shared requirements and explicit multiple-statement bridges. In addition, the source-atom-to-generated and generated-to-source meaning challenges inspected named endpoint, field, event, screen, state, test and DDL targets.

Full predicate scope is **not** assumed from a mere identifier match. For source-specific API requirements, the complete method/path and applicable actor, status and outcome were checked against the original generated API inventory row. For physical fields, the source entity and the DAT field row were checked together. Explicit shared rules were instantiated only where a matching resource-level membership witness was available. Unadopted proposals and the open architecture register were not promoted to positive implementation decisions.

Clear misses included the case-title data field, workspace retention class, cross-tenant/foreign-tenant equivalence, identical-response case replay, revised invariant negative tests, and screen-inventory rows. These were corrected to TP with actual file/line evidence and remain in the corrected-FN root-cause history.

## Quality and remaining uncertainty

- **Evidence completeness:** all 1,024 source-positive units have an item-level decision, original PDF citation, and retrieval outcome; all 529 remaining candidate FNs retain closest original generated evidence with a specific unmet requirement or conservative ambiguity.
- **Full-predicate proof:** Phase 3 records the predicate check and scope bridge for every candidate TP, but these are partly automated best-effort adjudications. No claim of independently certified semantic proof for every TP is made. Phase 5 must challenge each of them independently.
- **Source atomization:** the preserved historical PDF ledger has a 100-item watchlist including repeated cross-cutting context and acceptance-test overlap. It was retained as requested; its count has **not** been independently certified as the minimal meaningful denominator.
- **Conservative FN uncertainty:** labels `PARTIAL_ENTAILMENT` and `CONSERVATIVE_UNRESOLVED` do **not** certify semantic absence. They identify the best currently grounded judgment after attempted reciprocal retrieval. Any objectively located, complete match was corrected during this phase.
- **No Phase 4 leakage:** the 37 predeclared negative controls remain undecided; unsupported generated-only propositions, asserted controls, FP/TN classification and effective-universe metrics are **not** evaluated here.

## Selected regression cases

| Diagnostic probe | Source result |
|---|---|
| `case_title` | PDF-00208 TP |
| `workspace_retention_class` | PDF-00199 TP |
| `identical_case_replay` | PDF-00948 TP |
| `non_disclosing_foreign_id` | PDF-00184 TP |
| `indexed_source_revocation` | PDF-00951 TP |
| `stale_review_hash` | PDF-00953 TP |
| `source_not_authority` | PDF-00002 TP |

## Individual deliverables

- `03_canonical_universe_final.jsonl`: all 1,024 source-positive units and 37 fixed negative controls with **pending** Phase 4 labels. Generated-only unsupported units are deliberately not appended yet.
- `03_evidence_matches_final.jsonl`: one source-positive predicate/citation decision per source atom.
- `03_semantic_coverage_bridges_final.jsonl`: direct and contextual TP-grade claim bridges, including exact original generated file/line evidence and predicate checks.
- `03_fn_root_cause_audit_final.jsonl`: **all initially nominated FN candidates**, including those corrected to TP; each remaining FN has a named disposition and nearest actual generated evidence.
- `03_phase3_change_delta.jsonl`: per-item corrected matcher FN history and any explicit adverse proof corrections.
- `03_candidate_generated_validity_review.jsonl`: possible class-review leads; not validity judgments or FP counts.
- `03_regression_probes_final.jsonl`: actual requirement/field/test regression queries.
- `03_phase_status_final.json`: current phase metadata and limitation counts.
- `03_phase3_validation_final.json`: structural and citation-address integrity checks.
- `03_build_coverage.py`, `03_reciprocal_corrections.py`, `03_structural_final_pass.py`, `03_final_close.py`, `03_final_predicate_probe.py`, `03_finalize_and_verify.py`: reproducible local processing stages. 

## Phase boundary

Phase 3 is complete on a best-effort basis. **Phase 4 is not started**: no final Precision, Recall, F1, TP/TN/FP/FN four-cell confusion matrix, or independent generated-class validity ledger is claimed. The fixed source R/N denominators have not been modified in this phase.
