# Phase 3 — Source Coverage and Reciprocal Entailment Challenge

**Status:** `PHASE_COMPLETED_BEST_EFFORT`

**Protocol:** 6.1

**Evaluated method:** supplied, unprefixed eight-document Markdown corpus

## Corrected source coverage disposition

- PDF-positive source atoms: **1,024**.
- Conservative TP candidates with referenced actual generated evidence: **714**.
- Remaining conservative FN candidates: **310**.
- Direct E3 (initial classifier): **13**.
- E2 source-scoped bridges: **701**.
- Matcher false negatives corrected in reciprocal review: **357**.
- FN remaining: TRUE_MISSING **0**, PARTIAL_ENTAILMENT **275**, CONSERVATIVE_UNRESOLVED **35**.
- Confirmed-looking original structured rows recovered as a separate Phase 3 eligibility addendum: **70**.

### Evidence and status qualifications

The original eight Markdown inputs and Phase 1's fixed 1,024 PDF-positive and 37 PDF-negative atoms were not edited. This phase enumerates **only the PDF-positive projection** of the canonical universe; unsupported generated-only predictions and the bounded negative controls remain Phase 4 work. Every remaining FN has original full-row and eligible-class search evidence, targeted explicit-identifier search and a recorded root-cause disposition. 

Revised matching explicitly inspects table headers and original Markdown rows for direct catalog requirements (API path, entity field, run/event envelope, screen and required test scenarios), not just matching string similarity. Inherited context and universal applicability are scored only where the original row/section and scoped generated assertion support the link. Every explicit correction has an English change entry in `03_bidirectional_matcher_corrections.jsonl`.

**Not independently semantically certified.** Rule-assisted candidate retrieval and source-predicate testing cannot establish that each logical predicate is fully entailed. Some scored rows are composites, and some source atoms duplicate repeated boilerplate or verification requirements. Review and correction of overpermissive bridges, missed cross-file entailments, raw occurrence/class alignment and source split/merge issues are still required in Phase 5. The provisional counts are not verified design coverage or a certified Recall result.

### Files

- `03_canonical_universe_final.jsonl`
- `03_evidence_matches_final.jsonl`
- `03_semantic_coverage_bridges_final.jsonl`
- `03_fn_root_cause_audit_final.jsonl`
- `03_bidirectional_matcher_corrections.jsonl`
- `03_generated_eligibility_recovered.jsonl`
- `03_generated_eligibility_recovery_trace.jsonl`
- `03_phase3_status_final.json`
- `03_qa_validation_final.json`
- `03_phase3_report.md`



## Targeted evidence-quality correction

- Source-positive universe: 1,024 fixed PDF atoms. Final provisional coverage: **714 TP**, **310 FN**. No Phase 4 negative controls or FP counts have been adjudicated.
- Corrected initial false-negative cases: **357**; provisional final FN root-cause counts: `{"PARTIAL_ENTAILMENT": 275, "CONSERVATIVE_UNRESOLVED": 35}`.
- Targeted high-risk TP evidence updates: 133 records, with original-table evidence and cross-file bridges in `03_targeted_proof_corrections_final.jsonl`. Earlier citation errors were explicitly corrected; candidate retrieval alone does not establish entailment.
- Generated-only correctness candidates remain **unscored**: 26 first-pass items in `03_generated_correctness_review_queue.jsonl`; Phase 4 must independently adjudicate every generated class.
- All source evidence and scored Markdown inputs remain unchanged. Recovered original Markdown rows from Phase 2 remain in a labeled addendum pending ledger reconciliation; this is not a Phase 4 FP decision.
- **Semantic certification: NOT VERIFIED.** Targeted proof auditing cannot replace independent review of each TP and FN. Phase 5 correction and Phase 6 independent recomputation are required before any verified coverage claim.
