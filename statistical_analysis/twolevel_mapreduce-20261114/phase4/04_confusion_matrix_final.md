# Phase 4 — Generated-Claim Validity and Canonical Four-Cell Evaluation

**Protocol:** v6.1  
**Evaluation scope:** one supplied, method-unlabelled, eight-document set  
**Status:** `PHASE_COMPLETED_BEST_EFFORT` — **not semantically verified**

## Provisional four-cell summary

| Cell | Count |
|---|---:|
| TP | 990 |
| TN (bounded PDF-negative controls only) | 37 |
| FP (definitive generated-only propositions + asserted controls, provisional) | 0 |
| FN | 34 |

| Metric | Provisional value |
|---|---:|
| Precision | 1.000000 |
| Recall | 0.966797 |
| F1 | 0.983118 |

## Enumerated universe

- `R = 1024` PDF-positive normative atoms, `N = 37` fixed PDF-negative controls.
- `G = 2340` retained generated semantic classes, `GO = 2420` retained eligible occurrences.
- `A = 990` covered PDF-positive atoms; `B = 0` asserted fixed negative controls; `F = 0` independently scored generated-only definitive unsupported propositions.
- `U = R ⊔ N ⊔ F = 1061` canonical decisions; `P = A ∪ B ∪ F = 990` effective predicted-positive decisions.
- `TP + FN = 990+34 = 1024`; `TN+B = 37+0 = 37`; `FP-B = 0-0 = 0`.
- The raw class count **need not** equal `TP+FP` under universal-rule projection.

## Generated validity and Phase-2 eligibility corrections

- 879 classes are provisionally linked to PDF-positive source-coverage evidence.
- 1461 classes have PDF context or narrower source support without a certified source-positive coverage claim.
- 841 reverse PDF support checks are low-confidence, not certified full entailment. They are evidence gaps that must not be interpreted as confirmed absence of generated-only FP.
- 38 previously extracted citation-only or metadata-only classes were excluded as non-definitive. 93 TP rows had redundant citation-only class references removed; each retains an eligible substantive class reference.
- No additional **positively demonstrated** unsupported definitive proposition was identified by the bounded current review. Consequently FP=0 is a provisional count, **not a finding of verified perfect correctness**. Phase 5 must directly challenge unproven class-level support and recalculate FP where necessary.

## Fixed negative controls

All 37 controls were checked for affirmative assertion versus mere quoted prohibition, exclusion, rejection, hypothetical test, or deferral. None was classified as an adopted affirmative generated capability in this best-effort pass. The controls are a bounded diagnostic set, not the population of everything absent from the PDF.

## Interpretive limitations

The Phase-3 TP/FN totals were carried forward without independent exhaustive re-proof. Phase 4's large source-context and reverse lookup ledger is a **best-effort** determination, not a certified proof for each generated predicate. Its lower-confidence cases should be treated as unconfirmed support, not as proved `PDF_ENTAILED`; the `SUPPORTED_NONCOVERING` label records provisional context support and cannot by itself certify semantic correctness. Therefore the reported Precision=1.0 must **not** be presented as a reliable claim of no false positives. The Phase-5 evidence audit may change FP, TP, FN, the source denominator, or duplication counts. Structural reconciliation passes do not validate the semantic judgments.

## Individual artifacts

- `04_generated_claim_validity_final.jsonl`: one provisional validity record per retained raw generated class, with original-PDF candidates and uncertainty flags.
- `04_negative_control_assertion_audit.jsonl`: control-by-control polarity assessment.
- `04_atomic_judgments_final.jsonl`: one complete four-cell judgment per canonical decision unit.
- `03_canonical_universe_final.jsonl`: the same scored canonical universe.
- `04_generated_eligibility_corrections.jsonl`: citation/reference-only extraction corrections, no change to original Markdown.
- `02_generated_atoms_final.jsonl`, `02_generated_classes_final.jsonl`: reconciled copies for Phase 5.
- `04_confusion_matrix_final.json` and this report.
