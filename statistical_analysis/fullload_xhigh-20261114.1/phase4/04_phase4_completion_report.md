# Phase 4 Completion Report

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Scope:** Phase 4 only; Protocol v6.1; original PDF and all eight scored Markdown inputs unchanged.

**Provisional four-cell result:** TP 582, TN 37, FP 481, FN 442. Precision 54.75%; Recall 56.84%; F1 55.77%. The canonical decision universe enumerates 1,542 propositions, with 1,024 source-positive atoms, 37 fixed controls, and 481 distinct generated-only propositions.

All 3,818 raw generated classes received recorded validity or eligibility dispositions. Every fixed negative control was checked for an affirmative unsafe assertion. Reciprocal PDF lookup used actual physical PDF pages and raw Markdown row/cell context. Results are **best-effort, not a semantic certification**; low-confidence generated-only claims and class-linkage anomalies must be re-audited in Phase 5.

## Files

- `04_generated_claim_validity_final.jsonl`: one raw class per evidence-backed or explicitly ineligible validity record.
- `04_atomic_judgments_final.jsonl`: one TP/TN/FP/FN record per canonical unit.
- `03_canonical_universe_final.jsonl`: same scored canonical universe with full provenance.
- `04_confusion_matrix_final.json` and `04_confusion_matrix_final.md`: counts, rates, structural equations, limitations.
- `04_negative_control_assertion_audit_final.jsonl`: all fixed NEG controls.
- `04_substantive_generated_only_findings.jsonl`: each provisional distinct F.
- `04_supported_noncovering_challenge.jsonl`: source-backed generated subclaims for reciprocal follow-up.
- `04_phase2_ineligibility_flags.jsonl`: extraction overreach to correct in Phase 5.
- `04_reciprocal_pdf_corrections.jsonl` and `04_targeted_evidence_corrections.jsonl`: Phase 4 reverse-lookup corrections.

**No Phase 5 artifact was created or Phase 5 work performed.**
