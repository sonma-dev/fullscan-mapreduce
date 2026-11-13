# Final Independent Recalculation — OrionDesk AI

**Method:** `fullload`  
**Protocol:** v6.1  
**Final status:** `FINAL_BEST_EFFORT`  
**PDF authority:** *OrionDesk AI Detailed Application Design Specification* (`OD-AI-DDS-001`, R1.0 / revision 1.3)

## Final metrics

| Measure | Final |
|---|---:|
| PDF-positive source atoms | 1027 |
| Fixed PDF-negative controls | 37 |
| Canonical decision units | 1064 |
| TP | 576 |
| FN | 451 |
| FP | 0 |
| TN | 37 |
| Precision | 100.00% (provisional, not certified) |
| Recall | 56.09% (best effort) |
| F1 | 71.87% (best effort) |
| Semantic duplication | 1.46% (best effort) |

## Independent reconciliation

The recomputation reads individual canonical judgments rather than previous aggregate scores. TP+FN=576+451=1027; TN+asserted negatives=37+0=37; FP=0+0=0; and the four cells sum to 1064.

Raw occurrence/class accounting is 6080 minus 5991 = 89, partitioned into 2 within-file and 87 across-file excess. Canonical predicted positives are 576; they are not the raw generated class count.

## Additional Phase 6 corrections

- 55 specific initial false negatives were corrected to TP with source quotes and generated-file/line evidence.
- 20 definitive generated occurrences omitted from the preceding extraction were restored from the original, unchanged Markdown files.
- Six negative-control canonical identities were repaired after collision with the split source atoms `PDF-01025`–`PDF-01030`; no negative controls or source requirements were added or discarded by this identity repair.
- Missing method metadata for 23 directly reviewed generated-class validity rows was filled with the sole selected method, `fullload`.
- The source inventory remains 1027, incorporating three Phase-5 source-atomization corrections. The original PDF and all eight scored Markdown files remain unmodified.

## Outcome limitations

The independent checker validates record uniqueness, the entire canonical universe, PDF-page references, generated input quotation positions, FN root-cause membership, TP proof-audit presence, negative-control non-overlap and duplicate partitions. It does **not** certify semantic entailment for each claim. **5,093** generated classes retain uncertified original-PDF support assessments. A `FP=0` count is therefore an absence of *adjudicated* unsupported assertions, not proof that every generated statement is correct.

Final FN: **451** = 396 partial-entailment cases + 55 conservative unresolved cases. Neither category should be presented as a verified absence. The exact-quotation regression checker found 0 remaining full-line exact-match exceptions, but contextual/semantic misses could remain.

Details, original evidence, and uncertainties: `08_coverage_and_limitations.md`. Reproduction: `python compute_metrics.py` from this output directory.
