# OrionDesk AI — Independent Final Metrics (Phase 6)

**Protocol version:** 6.1  
**Evaluation baseline:** `OrionDesk_AI_Detailed_Design_Specification(8).pdf`, R1.0 / revision 1.3, 90 physical pages  
**Generated corpus:** one complete unlabelled set of eight supplied Markdown specifications  
**Final status:** `FINAL_BEST_EFFORT` — structural recomputation passed; semantic entailment is **not** certified.

## Canonical four-cell result

| Cell | Count |
|---|---:|
| TP | 990 |
| TN | 37 |
| FP — detected | 0 |
| FN | 23 |

| Result | Value |
|---|---:|
| Precision — provisional | 100.00% |
| Recall — provisional | 97.73% |
| F1 — provisional | 98.85% |
| Duplicate rate — raw classes | 4.625% |

The single canonical universe contains **1050** units: 1013 PDF-positive normative atoms, 37 predeclared negative controls, and 0 currently identified unsupported-only generated residuals. Effective predicted-positive canonical units: 990. Raw generated occurrence/class counts (2400 / 2289) are not interchangeable with source-side predictions.

## Independent consistency results

- PDF physical pages available/recorded: **90**.
- Scored Markdown roles/files: **8**; documented coverage of **2926** physical lines and **4090** table cells.
- Source-positive atoms audited: **1013**; fixed controls: **37**.
- Final TP rows with an evidence-audit record: **990**; final FN rows with root-cause-audit record: **23**.
- Raw duplicate excess: **111** = 1 within-file + 110 across-file.
- Structural validation errors: **0**; detected diagnostic regression-probe exceptions: **0**. Automated checks cannot guarantee an absence of semantic mismatches.

## Evidence certification boundary

The full-predicate TP audit is present for all 990 final TP rows, but only **1** has a separately reconciled complete semantic certification flag in the item-level ledger; the remaining 989 rely on earlier best-effort entailment judgments. No generated semantic class has been independently certified end-to-end against all of its PDF predicates. **1412** raw classes were tagged `SUPPORTED_NONCOVERING` without independently completed proof of source support. Their labels cannot establish that the apparent FP=0 or 100% Precision is correct.

## Reproduction

Run from a directory containing the unchanged original PDF and eight Markdown inputs:

```sh
python compute_metrics.py --ledger-dir /path/to/phase6 --input-dir /path/to/original_uploads
```

The script reads item-level JSONL, reopens the original inputs, asserts the one-universe equations and raw-class partition, performs source/line/duplicate/probe validation, and writes `06_metrics_final.json`, `06_independent_checks.json`, `06_regression_probes_final.jsonl`, and `06_quote_recovery_exceptions_final.jsonl`. It never hardcodes the desired score counts. File digests for the inspected originals are in `06_independent_checks.json`.

**Conclusion:** The reported rates are reproducible arithmetic over the enumerated best-effort judgments. They are not certified actual generated-specification coverage, production safety, implementation quality, or code correctness.
