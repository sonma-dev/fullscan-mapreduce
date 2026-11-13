# Phase 4: Generated Claim Validity and Four-Cell Confusion Matrix

**Protocol:** 6.1 | **Method:** fullload | **Status:** PHASE_COMPLETED_BEST_EFFORT

## Effective Canonical Universe

| Category | Count |
|---|---:|
| Fixed source-positive PDF atoms R | 1,024 |
| Fixed PDF-negative controls N | 37 |
| Distinct confidently demonstrated unsupported generated-only propositions F | 0 |
| Canonical decision units U = R + N + F | 1,061 |
| Effective predicted-positive units P = TP + FP | 495 |
| Eligible generated occurrences after Phase 4 extraction correction | 6,039 |
| Eligible raw generated semantic classes after correction | 5,986 |
| Removed nondefinitive Phase 2 extraction classes | 541 |

## Single-Universe Confusion Matrix

| | Predicted positive | Predicted negative |
|---|---:|---:|
| PDF-positive atom | TP = **495** | FN = **529** |
| PDF-negative or unsupported | FP = **0** | TN = **37** |

- **Precision (provisional):** 1.000000 (100.00%)
- **Recall (provisional):** 0.483398 (48.34%)
- **F1 (provisional):** 0.651745 (65.17%)
- **Raw semantic duplication (phase4-eligible provisional):** 0.008776 (0.88%)

Equations: TP+FN=1024=|R|; TN+asserted N=37=|N|; FP=|F|+asserted N=0; U=TP+TN+FP+FN=1061. **TP+FP is not the raw generated class count.**

## Critical Limits

The **FP=0** result means only that no unsupported definitive generated-only proposition was *confidently demonstrated* in this bounded pass. It does **not** certify that all 5,986 positive generated classes are correct. Exactly 1,102 low-signal and 2,586 weak-context classes remain subject to independent full-predicate audit. The validity ledger contains PDF candidates and status flags for each; an automatically retrieved paragraph is not a formal entailment proof. Therefore **provisional Precision=100% must not be reported as verified design correctness**.

Similarly, Phase 3's 495 TP candidates and 529 FN candidates are preserved without independent Phase 5 re-adjudication; calculated Recall is not certified completeness. The source denominator retains its historical 100-item atomization watchlist.

Negative-control TN=37 applies only to the bounded fixed counterfactual inventory; the null hypothesis across all imaginable absent features was not measured. Phase 2 extraction was revised using an explicit eligibility exclusion ledger; original Phase 2 files remain unchanged for provenance.

## Phase 5 Review Queue

3688 generated classes have weak or low-signal PDF source corroboration, retained in `04_generated_validity_review_queue_final.jsonl`. These labels are provisional rather than certified PDF entailment. This is the principal possible FP undercount risk. Original Phase 2 class IDs are fully partitioned between eligible claims and explicitly excluded non-predictions.

## Delivery Files

- `04_generated_claim_validity_final.jsonl` — one provisional PDF-support decision per eligible raw class.
- `04_generated_validity_review_queue_final.jsonl` — 3688 uncertain source-support candidates.
- `04_generated_eligibility_exclusions_final.jsonl` — Phase 2 nondefinitive extraction corrections.
- `02_generated_atoms_phase4_eligible.jsonl` and `02_generated_classes_phase4_eligible.jsonl` — Phase 4 eligibility projection for Phase 5.
- `04_negative_control_assertion_audit_final.jsonl` — 37 PDF-grounded controls and near-hit polarity review.
- `04_generated_only_unsupported_final.jsonl` — distinct convincingly unsupported propositions (empty in this provisional pass).
- `03_canonical_universe_final.jsonl` — final Phase 4 R/N/F enumeration.
- `04_atomic_judgments_final.jsonl` — one decision per canonical proposition.
- `04_reciprocal_pdf_candidates_working.jsonl` — 6,527 raw-class PDF search and evidence candidates.

**Next-phase boundary:** Phase 5, not performed here, independently re-challenges all residual FN, every TP predicate proof, generated validity support and source atomization, and recomputes metrics.
