# Phase 4 — Generated Correctness and Canonical Four-Cell Evaluation

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** OrionDesk One-Pass Atomic Evaluation v6.1  
**Scope:** One supplied set of eight scored Markdown files; PDF original `OD-AI-DDS-001`, R1.0 / revision 1.3.  
**Current phase only:** Phase 4. Phase 5 was not started.

## Canonical Confusion Matrix

| | Predicted positive | Predicted negative | Actual total |
|---|---:|---:|---:|
| PDF-positive source requirements | TP = 895 | FN = 129 | 1024 |
| PDF-negative controls plus generated-only unentailed claims | FP = 64 | TN = 37 | 101 |
| Decision totals | 959 | 166 | 1125 |

| Metric | Provisional value |
|---|---:|
| Precision | 0.933264 (93.33%) |
| Recall | 0.874023 (87.40%) |
| F1 | 0.902673 (90.27%) |
| Raw generated duplication | 0.031399 (3.14%) |

## Reconciliation and scoring unit

- The PDF-positive inventory `R` has 1024 independent source atoms and 895 source atoms currently covered by generated evidence.
- The bounded PDF-negative control set `N` has 37 controls, of which 0 are asserted by definitive generated commitments.
- The distinct generated-only unsupported set `F_m` has 64 provisional entries.
- The canonical universe has `|U_m| = |R| + |N| + |F_m| = 1024 + 37 + 64 = 1125` units.
- The predicted-positive count is `TP + FP = 895 + 64 = 959`. It **is not** required to equal the 2437 raw generated classes.
- Raw duplication remains `(2516 - 2437) / 2516 = 0.031399`; Phase 5 independently checks semantic equivalence and duplicate partitions.
- Every source atom and every negative control is represented once in the same decision ledger. Every provisional distinct unsupported generated commitment is added once as an FP, rather than counted per failed source match.

## Generated-corpus correctness

| Verdict | Classes |
|---|---:|
| PDF_ENTAILED | 486 |
| SUPPORTED_NONCOVERING | 1887 |
| PDF_UNSUPPORTED | 64 |
| **Raw classes examined** | **2437** |

Generated propositions that share source text but do not cover a separately retained PDF atom are assigned `SUPPORTED_NONCOVERING` only as a bounded, positive-source contextual judgment. The per-class ledger exposes original Markdown line and table context, PDF page evidence, match candidates, and verification grade. A low lexical score alone is not declared proof of a PDF contradiction.

## Reciprocal challenge of provisional generated false positives

All 593 initial unsupported-class candidates were subjected to a reciprocal generated-to-PDF candidate review. 529 candidates were reclassified as contextual source-supported, noncovering claims after targeted source-page review. 64 remain unsupported in this Phase 4 best-effort ledger; of these, 51 are traceability/interpretive statements that may prove ineligible when raw generated extraction is audited in Phase 5. The full audit history is in `04_generated_fp_reciprocal_challenge_final.jsonl`. A corrected false positive here is a *best-effort source-grounding decision*, not a certification that all source predicates were manually audited.

## Evidence quality and mandatory future re-audit

This is a **reproducible best-effort Phase 4 adjudication, not certified semantic completeness**. Some raw classes in Phase 2 encode traceability instructions or statements about the source's unresolved contracts. Treating those as positive implementation predictions is potentially inappropriate. Rather than silently removing historical raw classes here, the item-level ledger flags them as conservative provisional FP where no complete source entailment could be established. Phase 5 must challenge those labels and update the occurrence/class extraction and all four-cell figures when warranted. No source requirement was invented to absorb unmatched classes.

Likewise, Phase 3's 895 TP / 129 FN source coverage is carried into Phase 4 without re-scoring. Negative controls are bounded examples of explicit PDF prohibitions/deferrals; TN does not estimate the population of all absent features. The core source PDF remains the only normative authority. No proposed or `Needs confirmation` alternative is promoted as adopted policy.

## Deliverables and next step

See `04_generated_claim_validity_final.jsonl`, `04_negative_control_adjudication_final.jsonl`, `04_generated_only_fp_final.jsonl`, `04_atomic_judgments_final.jsonl`, `03_canonical_universe_final.jsonl`, and `04_confusion_matrix_final.json`. Phase 5 is reserved for source atomization, reciprocal FP/FN correction, independent TP-proof audit, duplicate reclassification and recalculation; it has not been executed here.
