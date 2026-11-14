# OrionDesk AI — v6.1 Independent Final Metrics

**Execution:** Phase 6 of 6; **final status: FINAL_BEST_EFFORT**. One supplied eight-file corpus (unlabeled method), no cross-method comparison.

## Recomputed effective-universe metrics

| Metric | Value |
|---|---:|
| Precision | **76.22%** |
| Recall | **65.72%** |
| F1 | **70.58%** |
| Duplicate (raw-class basis) | **3.94%** |
| True positive | 673 |
| True negative, fixed controls only | 37 |
| False positive | 210 |
| False negative | 351 |
| Canonical decision units | 1,271 |
| Source positives / source negatives / generated-only unsupported | 1,024 / 37 / 210 |

`Precision = TP/(TP+FP)`; `Recall = TP/(TP+FN)`; `F1 = 2TP/(2TP+FP+FN)`; `Duplicate = (|GO|-|GC|)/|GO|`.

The *effective canonical* predicted-positive count is 883, which is intentionally not the raw semantic-class count 3,218.

## Audit results and repairs

- Physical PDF pages: 90; generated Markdown files: 8; physical lines: 3,956; table cells: 6,308.
- Final confirmed-TP proof audit records: 673; final FN root-cause records: 351.
- FN dispositions: PARTIAL_ENTAILMENT=134, CONSERVATIVE_UNRESOLVED=217, TRUE_MISSING=0.
- Repaired explicit false negatives: PDF-01013 (`language`) and PDF-01014 (`classification`) based on `03_data.md:182` SearchChunk row.
- Synchronized the stale canonical universe (1,296 rows) to the current individual judgments (1,271 rows); 25 already-excluded generated-only FP entries were removed.
- Existing TP-audit predicate maps were copied into 82 E2 bridge rows; 7 incomplete ten-predicate maps were completed from source context. These are traceability repairs, not independent semantic proof.
- Figure-only PDF quotes not present in machine text extraction: PDF-00977, PDF-00978, PDF-00979; the original page 8 visual figure was checked separately.

## Reliability and interpretation

**NOT SEMANTICALLY CERTIFIED.** 722 nominally supported generated classes remain at source-support grade E1; 210 classified unsupported classes also have E1-grade ambiguity. 217 FNs are conservative unresolved and 134 are partial coverage. These figures do not support a confidence interval or proof of the true implementation-level recall.

The PDF and Markdown corpora are complete and available. Structural equations and locators pass the independent checker; machine-rechecked text cannot prove full logical entailment or that all source atomization splits are semantically correct. TN is only for the 37 predeclared source-negative controls. Scope is the *generated specifications*, not production software correctness.

Run `python compute_metrics.py --base /mnt/data/OrionDesk_v6_1 --inputs /mnt/data --check-final-files` to reproduce ledger-level structural checks and totals.
