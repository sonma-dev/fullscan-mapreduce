# OrionDesk AI — Phase 6 Final Recomputed Metrics

**Protocol:** 6.1  
**Scope:** One scored eight-document corpus against the 90-page authoritative PDF.  
**Status:** PHASE_COMPLETED_BEST_EFFORT  
**Semantic certification:** NOT INDEPENDENTLY CERTIFIED (BEST EFFORT)  
**Structural checks:** PASS

## Canonical binary confusion

| | Predicted positive | Predicted negative |
|---|---:|---:|
| Actual PDF positive | TP = 981 | FN = 39 |
| Actual PDF negative (fixed controls) | FP asserted N = 0 | TN = 37 |

PDF-positive inventory `R` = **1020**; bounded negative controls `N` = **37**; extra unsupported generated-only propositions `F` = **0**.  
Total canonical units `U` = **1057**; predicted positives = **981**.

- **Precision:** 100.000000%
- **Recall:** 96.176471%
- **F1:** 98.050975%

All confusion cells are counted from the **same canonical unit ledger**, not by mixing source-item TP with raw generated-class FP. A universal generated rule may cover multiple independently retained PDF atoms without changing raw class counts. TN is bounded to the 37 PDF-derived negative controls; it is not a population-wide specificity measurement.

## Raw semantic duplication

| Item | Count |
|---|---:|
| Eligible generated occurrences `GO` | 4217 |
| Unique raw semantic classes `G` | 4069 |
| Excess occurrences | 148 |
| Within-file excess | 12 |
| Across-file excess | 136 |
| Repeated claim classes | 91 |
| Repeated classes spanning files | 87 |
| Duplicate rate | 3.509604% |

The duplicate rate uses **raw eligible occurrences** and **raw classes**, never source coverage projections.

## Corrected inventory and uncertainty

Five parent/composite source atoms were retired and one separately retained split child was established in Phase 5, yielding 1,020 PDF-positive atoms. Phase 5 also excluded six nonproduct Stage-8 authoring directions rather than counting them as product-level false positives.

Final FN dispositions: 5 TRUE_MISSING, 11 PARTIAL_ENTAILMENT, 23 CONSERVATIVE_UNRESOLVED.

Every final TP has a PDF and generated locator, but **64** have higher-priority bridge review concerns. The **3507** supported-noncovering labels lack an independently completed proof audit. Equation checks and quote-location checks do **not** certify full-predicate entailment or classification correctness. The point estimates can move in either direction after substantive independent review.

See `08_coverage_and_limitations.md`, `06_validation_checks_final.json`, and `compute_metrics.py` for the reproducible evidence and limitations.
