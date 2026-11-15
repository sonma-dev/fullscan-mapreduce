# OrionDesk R1.0 — Final Six-Phase Atomic-Requirement Evaluation

**Status:** `FINAL_BEST_EFFORT` (Phase 6 completed as `PHASE_COMPLETED_BEST_EFFORT`)  
**Protocol:** 6.1  
**Method:** `supplied_set_01`  
**Document scope:** Original 90-page English PDF versus eight supplied English Markdown specifications. 

## Final four-cell results

| Cell | Actual | Predicted | Count |
|---|---|---|---|
| TP | 1 | 1 | 584 |
| FN | 1 | 0 | 435 |
| FP | 0 | 1 | 571 |
| TN | 0 | 0 | 37 |
| Total | — | — | 1627 |

| Metric | Exact decimal | Display |
|---|---|---|
| Precision | 0.505627705628 | 50.56% |
| Recall | 0.573110893032 | 57.31% |
| F1 | 0.537258509660 | 53.73% |
| Semantic duplicate rate | 0.034051724138 | 3.41% |

The canonical decision universe has **1627** units: **1019** original-PDF-positive atoms, **37** bounded negative controls and **571** generated-only unsupported propositions. Positive predictions count **1155** effective units. The 37 TN are bounded PDF-derived controls, not a global TN population.

## Raw generated duplication

**2320** eligible generated occurrences, **2241** unique semantic classes, **79** excess occurrences = **3** within-file + **76** across-file. Duplicate rate **3.41%**.

## Key evidence and corrections

- Independently reopened all 90 original PDF pages and all **3,956** original Markdown lines. The **1019** retained source-atom quotes were located verbatim after whitespace normalization on their stated physical PDF pages.
- Audited **584** TP proof rows (396 E3 and 188 E2), and **435** remaining FN disposition rows.
- Remaining FN categories: **12** `TRUE_MISSING`, **106** `PARTIAL_ENTAILMENT`, and **317** `CONSERVATIVE_UNRESOLVED`.
- The Phase-5 source atomization correction removed five nonindependent parent atoms. Independent Phase-6 checks corrected ten additional semantic-matcher false negatives; 301 candidate-FN records are now documented as corrected across phases.
- Seven case/field/API/test regression probes pass, including the case-title field, workspace retention-class settings and idempotent repeat case creation with the same outcome.
- Original scored inputs were not edited. Source IDs and generated occurrence/class IDs remain stable. All corrections and metadata synchronization are traceable in the English delta ledgers.

## Final reliability statement

The computations satisfy the full single-universe equations and duplicate partition arithmetic, with no structural validation failures. They are **not** certified requirement completeness or implementation correctness. The **317** conservative FN judgments and **571** conservatively unsupported generated-only FP judgments may change with additional semantic evidence. The full limitations, input coverage, corrected-FN citations and negative-control scope are documented in `08_coverage_and_limitations.md`.

**Recomputation:** `python compute_metrics.py --base <final output folder> --inputs <original input folder> --write`.

No multi-method comparison is required: one eight-file input method was supplied. No ZIP, TAR or other archive was generated.
