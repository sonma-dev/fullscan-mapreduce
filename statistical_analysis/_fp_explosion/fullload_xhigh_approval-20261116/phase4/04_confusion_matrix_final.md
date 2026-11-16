# Phase 4 — Full Canonical Four-Cell Evaluation (Best Effort)

**Status:** `PHASE_COMPLETED_BEST_EFFORT` (not `FINAL_VERIFIED`)  
**Protocol:** 6.1  
**Method:** supplied unprefixed eight-document corpus  

## Single decision universe

| Set | Count |
|---|---:|
| PDF-positive source requirements, `R` | 1024 |
| Fixed PDF-negative counterfactual controls, `N` | 37 |
| Raw generated occurrence records, `GO` (including 70 Phase 3 recoveries) | 5296 |
| Raw generated semantic classes, `G` (working set) | 5265 |
| Covered source-positive requirements, `A` | 714 |
| Asserted negative controls, `B` | 0 |
| Distinct unsupported generated-only propositions, `F` | 1795 |
| Canonical universe `U = R ∪ N ∪ F` | 2856 |
| Effective predicted positives `P = A ∪ B ∪ F` | 2509 |

## Four-cell confusion matrix

| | Predicted positive | Predicted negative |
|---|---:|---:|
| Actual positive | **TP = 714** | **FN = 310** |
| Actual negative | **FP = 1795** | **TN = 37** |

- **Precision:** 28.46% (`TP / (TP + FP)`)
- **Recall:** 69.73% (`TP / (TP + FN)`)
- **F1:** 40.42% (`2TP / (2TP + FP + FN)`)
- **Raw duplicate rate (provisional):** 0.59% (`(|GO|-|G|)/|GO|`)

## Structural equalities

- `TP+FN = 714+310 = 1024 = |R|`
- `TN+|B| = 37+0 = 37 = |N|`
- `FP-|B| = 1795-0 = 1795 = |F|`
- `TP+TN+FP+FN = 2856 = |R|+|N|+|F|`
- `TP+FP = 2509 = |P|`; it is not required to equal the raw `|G|=5265`.

## Independent generated-class validity (provisional)

- `PDF_ENTAILED`: 2068; full logical predicate audit outstanding.
- `SUPPORTED_NONCOVERING`: 1402; PDF context exists but the class adds no separately evidenced source-atom coverage.
- `PDF_UNSUPPORTED`: 1795; candidate unentailed assertions conservatively scored, not necessarily PDF contradictions.
- Raw-class validity total: 5265.
- Eligibility/fragment challenges in raw classes must be resolved by Phase 5 rather than silently omitted.

## Important limitations

This confusion matrix is **arithmetic over a complete, enumerated working universe**, not a certified measurement of semantic specification completeness. The automated class-to-PDF search is insufficient to independently verify all nuances (scope, actor, exceptions, timing, outcome). Some `PDF_UNSUPPORTED` labels indicate *insufficient evidence of full support*, not proven false commitments; those could change substantially in Phase 5. Phase 3 TP and FN decisions were carried forward unchanged and are not fully independently certified. The PDF-positive inventory may require documented split/merge corrections. The 37 TN controls are a fixed, bounded diagnostic set, **not all possible absent requirements**. The raw class/occurrence counts include a 70-row Phase 3 recovery pending Phase 5 integration and an eligibility/duplication re-audit.

Phase 5 must audit source-atomization, every TP proof, every FN disposition, generated claims currently flagged unsupported or supported-noncovering, and duplicate merging; recalculate all four cells. No scored input Markdown, source PDF, or earlier phase ledger was modified.

### Audit exceptions

The output retains pending Phase 5 checks for five absent PDF quote candidates, 146 class-validity versus source-coverage review conflicts, and questionable eligibility of nondefinitive observations. Arithmetic PASS does not certify the semantic TP or FP decisions.
