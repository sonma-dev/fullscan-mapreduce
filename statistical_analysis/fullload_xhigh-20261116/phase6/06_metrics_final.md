# Phase 6 — Independent Final Recalculation

**Protocol:** OrionDesk Six-Turn Atomic Requirement Evaluation v6.1  
**Method:** One complete user-supplied eight-Markdown corpus  
**Final status:** `FINAL_BEST_EFFORT`  
**Semantic certification:** `NOT_CERTIFIED`  
**Source of truth:** Original 90-physical-page English PDF.

## Canonical one-universe results

| Measure | Final count or rate |
|---|---:|
| PDF-positive requirements (`R`) | 1014 |
| Fixed PDF-negative controls (`N`) | 37 |
| Unique raw generated classes (`G`) | 5889 |
| Eligible generated occurrences (`GO`) | 5956 |
| Canonical proposition universe (`U`) | 1051 |
| Canonical predicted positives (`P`) | 456 |
| TP | 456 |
| TN | 37 |
| FP | 0 |
| FN | 558 |
| Precision | 100.0000% (UNVERIFIED) |
| Recall | 44.9704% (PROVISIONAL) |
| F1 | 62.0408% (PROVISIONAL) |
| Semantic duplicate rate | 1.1249% (PROVISIONAL) |

### Exact derivation

`TP=|A|=456`; `FN=|R|-|A|=1014-456=558`; `TN=|N|-|B|=37-0=37`; `FP=|F|+|B|=0+0=0`.  
`|U|=|R|+|N|+|F|=1014+37+0=1051`.  
`|P|=TP+FP=456`; `GO-G=67=7+60`.

**Crucial interpretation:** `TP+FP` is the effective canonical predicted-positive count; it is not the raw generated-class count. Fixed source-negative controls do not represent all conceivable missing or forbidden capabilities.

## Phase 6 corrections and checks

- Seven explicit or complete contextual matches were discovered among the former FN set and reclassified as TP, with original Markdown line proof and change-delta entries. The source denominator was not changed in Phase 6.
- Earlier corrected candidate-FN histories were reconciled with canonical TP rows; 148 stale disposition records were corrected without changing their existing TP classifications.
- The independent ledger checker verified every source/canonical ID, all eight original Markdown file locations, raw-class membership, TP proof and bridge presence, FN root-cause disposition, negative-control polarity, duplicate partition and arithmetic identities.
- The original PDF opens as 90 physical pages. All 1014 current source-positive quotations were re-located in its page text: 911 after whitespace normalization, and 103 after additional PDF-layout normalization.
- A literal-token reciprocal-search sidecar was generated for every 558 remaining FN. This retrieval search is not semantic proof and must not automatically promote candidates.

## Semantic reliability limitations

- 5889 of 5889 raw class correctness judgments lack independent complete-predicate certification, including 3973 especially weak PDF support links. Consequently **FP=0 is not verified** and computed Precision=100% should not be interpreted as demonstrated generated-specification correctness.
- Of 558 final FNs: 353 are partially matched, 140 remain conservatively unresolved, and 65 are provisional missing judgments. They are not 558 certified omissions.
- Every 456 final TP has a structured predicate-check record, but full independent human semantic proof is not certified. The breakdown is 28 E3 direct and 428 E2 bridged cases.
- The source denominator underwent 10 removals in Phase 5. Additional atomization issues could shift the denominator in either direction, so Recall is not a guaranteed lower bound.

See `08_coverage_and_limitations.md` for exact evidence and remaining limitations. Reproduce the numbers by executing `python compute_metrics.py --write` in this directory.
