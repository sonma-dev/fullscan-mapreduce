# Phase 5 - Evidence, Atomization, and Duplicate Audit (v6.1)

**Status:** `PHASE_COMPLETED_BEST_EFFORT`; semantic certification remains explicitly unavailable.

## Corrected canonical four-cell assessment

| Item | Count / provisional rate |
|---|---:|
| PDF-positive `R` | 1,024 |
| PDF-grounded, bounded negatives `N` | 37 |
| TP | 671 |
| TN | 37 |
| FP | 210 |
| FN | 353 |
| Precision | 76.16% |
| Recall | 65.53% |
| F1 | 70.45% |
| Duplicate | 3.94% |

This is a conventional binary confusion matrix over one canonical proposition universe, not a class-level precision score. `U=R+N+F=1271` with `F=210`, asserted controls `B=0`, and predicted positives `P=881`. Only 37 predeclared PDF-grounded negative controls contribute TN.

## Source coverage, bidirectional challenges and TP proof

In the v6.1 Phase 4 baseline, TP=590 and FN=434. The Phase 5 review found 82 additional **retained** false-negative corrections from actual generated files and line/table-cell locators. Four extra provisional promotions were retracted when their scope, ordering or actor/outcome predicate was not completely entailed; one original TP was separately downgraded. The net is TP=671 and FN=353. No source denominator was changed. Source and generated evidence is retained in `03_evidence_matches_final.jsonl`, the final bridge ledger, and `05_tp_evidence_audit_final.jsonl`.

Every final TP has one evidence-audit row. These are **bounded best-effort predicate checks**, not 671 independent specialist semantic certifications. Several original E2 checks relied on inherited table context or general shared rules. No proposition was promoted on mere textual similarity without cited generated evidence, but some previously accepted entailment claims still depend on judgment.

| Final FN root-cause disposition | Count |
|---|---:|
| `TRUE_MISSING` | 0 |
| `PARTIAL_ENTAILMENT` | 136 |
| `CONSERVATIVE_UNRESOLVED` | 217 |

Do **not** interpret all remaining FN as proven actual omissions. The reciprocal search stores candidate evidence and unmet predicates, but the unresolved subset still needs independent substantive scrutiny.

## Source atomization and acceptance tests

No incontrovertible common-denominator split or merge correction was established in this bounded phase. All 16 named Appendix E release-test scenarios were retained as separately testable verification duties because the PDF explicitly requires a release test pack; this is not permission to duplicate their functional implementation requirements. Shared tenant/actor/revision/timestamp obligations remain distinct only where individually testable, not copied for every chapter. `05_source_atomization_audit_final.jsonl` records the status and source evidence.

## Generated correctness and evidence uncertainty

Generated-only FP changed from 235 to 210 after 17 PDF-supported reclassifications and eight nondefinitive/documentation-only class exclusions. A further three complete-predicate duplicate class pairs were merged, and source-context alternatives that differed in target or condition were not merged.

A material limitation remains: **722 generated classes** currently carry an `E1` PDF-support grade while retaining the provisional `SUPPORTED_NONCOVERING` or `PDF_ENTAILED` label. This inconsistency is explicitly flagged in `05_unresolved_generated_support_audit_final.jsonl` and **precludes semantic certification**. It was not resolved by automatically labeling all 722 as FP, which would treat imperfect retrieval as evidence of invalidity. The previously identified generated-context support gap list also contains 125 entries. Both provisional source coverage and generated correctness can move after substantive independent review.

## Raw duplication

Eligible occurrences: 3350; unique raw semantic classes: 3218; duplicate excess: 132. Within-file excess=16; across-file excess=116; total reconciles. Repeated classes=86, of which 82 span multiple files. The Duplicate fraction is calculated on raw occurrences/classes, never on source-coverage bridges or canonical predictions.

## Phase closure and next verification gate

This phase delivers corrected item-level ledgers, the TP proof audit, source-atomization review, semantic duplicate class inventory, final Phase 5 duplication calculation and change deltas. Phase 6 must independently recompute all metrics, run concrete regression probes, and check language/files/coverage before final delivery. Passing arithmetic here does not constitute `FINAL_VERIFIED`.
