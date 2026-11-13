# Phase 5 Revised Canonical Confusion Matrix (Best Effort)

**Protocol:** v6.1 | **Status:** `PHASE_COMPLETED_BEST_EFFORT` | **Phase:** 5 of 6

| Actual / predicted | Predicted positive | Predicted negative |
|---|---:|---:|
| PDF-positive requirement | TP = 963 | FN = 45 |
| PDF-negative control / unsupported proposition | FP = 0 | TN = 37 |

| Metric | Computed value |
|---|---:|
| Precision | 100.000000% |
| Recall | 95.535714% |
| F1 | 97.716895% |
| Duplicate (raw occurrences/classes) | 7.990599% |

Canonical universe: `1008 source-positive + 37 fixed negatives + 0 generated-only unsupported = 1045`. `TP + FN = 1008`; `TN = 37`; `TP + FP = 963` (not necessarily `2349` raw classes).

These are structurally reconciled *provisional* metrics, not verified semantic accuracy. In particular, the computed Precision reaches 100% only because Phase 4's 64 supposed FPs are unapproved traceability/editorial/open-question remarks; this correction is valid eligibility bookkeeping, not proof that every remaining generated class is PDF-entailed. 1269 raw classes still have E1 evidence-grade origin flags, and all original TP bridges require independent verification before semantic certification. See `05_tp_evidence_audit_final.jsonl`, `05_source_atomization_audit_final.jsonl`, and `07_change_delta.jsonl`.

No Phase 6 steps have been executed.
