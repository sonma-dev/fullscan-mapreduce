# Phase 3 — PDF Positive Coverage and Reciprocal False-Negative Challenge

**Protocol:** 6.1  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method:** `supplied_eight_file_set`  

## Inputs and scope

- Authoritative 90-page PDF, inherited Phase-1 inventory: 1,024 positive atoms and 37 fixed negative controls.
- All eight actual scored Markdown files, inherited Phase-2 inventory: 5,922 generated occurrences, 5,855 raw semantic classes.
- Each PDF-positive atom was searched using both full-corpus forward TF-IDF (word and character) and a reverse generated-to-source index, plus untruncated exact identifier/path/event searches and original Markdown line/table context.
- No generated-only `F_m`, negative-control assertions `B_m`, or final TN/FP scores are asserted in this phase; these belong to Phase 4.

## Corrected source-positive adjudication (best effort)

| Measure | Count |
|---|---:|
| Source-positive atoms | 1,024 |
| Provisional TP | 384 |
| Provisional FN | 640 |
| Direct E3 proofs | 26 |
| E2 direct contextual/semantic/universal/conjunctive proofs | 358 |
| E1 partial | 430 |
| E0 not demonstrably entailed | 210 |
| Corrected initial FNs with actual source locators | 148 |
| Remaining `PARTIAL_ENTAILMENT` | 430 |
| Remaining provisional `TRUE_MISSING` | 67 |
| Remaining `CONSERVATIVE_UNRESOLVED` | 143 |
| Strong-candidate review exceptions | 0 |

## Corpus and eligible-claim extraction repair

The original eight scored Markdown inputs remain unchanged. Phase 3 exposed 29 unequivocally source-backed **selected-field table cells** that the Phase-2 extractor failed to classify as eligible independent generated occurrences; these cells were reinstated with explicit entity/table/field scope and original physical-row evidence. The field corrections and four recovered definitive independent prose clauses result in amended derived inventories containing 5,955 eligible occurrences and 5,888 raw classes, preserving the existing 67 excess occurrences. These amendments are separately enumerated and do **not** add new PDF obligations or change the shared 1,024 source inventory. Phase-4 and later processing must read the amended inventories instead of the original Phase-2 snapshots.

## Evidence and false-negative challenge

Each original PDF-positive atom received forward source-to-generated and generated-to-PDF retrieval against the full generated class corpus, exact method/path/field/event controls, actual physical Markdown row reconstruction, and a conservative full-predicate check. Separate in-phase corrections revisited synonyms, shared universal rules, Appendix A API method/path/status/action rows, Appendix B SQL and field catalogs, C.2 A2A properties, and Appendix E test scenarios. Exact field/context and test matches were not discarded simply because a source passage used a different heading, field-table identifier or word order. All 148 candidate-FN corrections have documented generated class/occurrence IDs and original-file line evidence. The root-cause audit preserves each initial provisional FN even after correction.

## Semantic limitations

These source-side TP/FN counts are **BEST_EFFORT** evidence judgments, not audited true coverage: exact structural proof can miss or overstate complex scope, actor, timing or exception predicates, and full independent human review of every E2/TP has not yet occurred. A conservative FN means complete entailment has not been demonstrated; it does not certify absence. Remaining semantic uncertainty and PDF source atomization (universal repeated boilerplate, summary/child counts, source test-vs-behavior overlaps) must be examined in Phase 5, with any common denominator correction applying identically across methods. The final four-cell universe is not yet complete: generated-only unsupported propositions F and negative-control assertions B must be handled in Phase 4. No final TN/FP/Precision/Recall/F1 is claimed here.

## English deliverables

- `03_canonical_universe_final.jsonl` — draft R ⊎ N; 37 negative controls have explicit Phase-4-pending predicted labels.
- `03_evidence_matches_final.jsonl` — 1,024 source-positive item decisions and evidence.
- `03_semantic_coverage_bridges_final.jsonl` — 358 cited E2 bridges.
- `03_fn_root_cause_audit_final.jsonl` — every initially flagged FN, with final disposition and corrections.
- `03_correction_delta.jsonl` — 148 in-phase corrections.
- `03_mandatory_semantic_review_exceptions.jsonl` — unresolved high-risk matches for later independent review.
- `02_generated_atoms_amended_phase3.jsonl` and `02_generated_classes_amended_phase3.jsonl` — corrected effective generated inventories after missing field-cell recovery.
- `04_duplicate_classes_amended_phase3.jsonl`, `02_reciprocal_lookup_keys_amended_phase3.jsonl` — matching derived-class ledgers.
- `03_generated_field_extraction_amendments.jsonl` — 29 recovered source-backed selected-field cells.
- `03_generated_clause_extraction_amendments.jsonl` — four additionally recovered definitive prose clauses.
- `03_phase3_validation.json` and `validate_phase3.py` — independent structural and original-line verification; all checks passed, without semantic certification.
- `03_phase3_status.json`, `03_reciprocal_regression_probes.json`, and reproduction scripts.
