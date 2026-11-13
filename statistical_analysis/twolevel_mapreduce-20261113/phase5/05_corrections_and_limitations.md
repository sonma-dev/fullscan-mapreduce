# Phase 5 Corrections, Evidence Audit, and Limitations

**Protocol:** v6.1  
**Phase:** 5/6  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Semantic certification:** Not established

## Scope and input lineage

Phase 5 reevaluates the same eight actual scored Markdown specifications and the same 90-page `OD-AI-DDS-001` R1.0 / revision 1.3 source PDF used earlier. All output evidence uses physical PDF page numbers or original Markdown filenames and line numbers. The source-negative-control universe (37 controls) is unchanged. This phase does not run Phase 6 recomputation or reporting.

## Corrected canonical counts

| Measure | Earlier provisional Phase 4 | Revised Phase 5 |
|---|---:|---:|
| PDF-positive independent atoms | 1,024 | 1,008 |
| Bounded source-negative controls | 37 | 37 |
| Raw eligible generated occurrences | 2,516 | 2,553 |
| Raw distinct generated classes | 2,437 | 2,349 |
| TP | 895 | 963 |
| FN | 129 | 45 |
| FP | 64 | 0 (provisional) |
| TN | 37 | 37 |
| Precision | 93.33% | 100.00% (provisional) |
| Recall | 87.40% | 95.54% (provisional) |
| F1 | 90.27% | 97.72% (provisional) |
| Duplicate rate | 3.14% | 7.99% (conservative estimate) |

A revised source inventory of 1,008 items replaces 1,024 for **every** comparable method. The common source universe must not be modified for a single method to improve its score.

## Source-atomization corrections

Sixteen source items were removed with their original IDs and PDF quotations preserved in `05_source_atomization_audit_final.jsonl` and `07_change_delta.jsonl`. The removals consist of duplicate or nonindependent parent summaries and illustrative-only A2A JSON keys. In particular, A2A identifiers in an illustrative example do not prove exact mandatory key names. The independent substantive A2A envelope requirements remain. The Phase 3 repairs to two PDF-normalized membership endpoint labels were preserved.

## Source coverage and reciprocal challenge

The Phase 5 reciprocal search corrected 69 additional previous false negatives to TP, using original Markdown line evidence. Remaining 45 FN judgments are distinguished as **13 true missing**, **20 partial entailment**, and **12 conservative unresolved**. These labels are best-effort outcomes, not proof of universal absence.

Each final TP has a generated line locator and source page record. Of 963 final TP audit rows, 748 passed the independent automated PDF-text phrase check and 215 require qualification under the current extraction/normalization rule. The latter are not silently certified. All 963 generated TP evidence locator quotations were found in the underlying scored Markdown lines after normalization.

## Generated correctness and FP eligibility

The 64 provisional Phase 4 generated-only FP records were traceability, open-question, or editorial statements, not definitive implementation commitments. Their classification was corrected to **excluded from the prediction universe**, with real file/line evidence retained in the change ledger. This produces a *provisional* FP count of zero, **not a proven absence of unsupported commitments**.

1269 surviving generated classes still bear earlier E1-level origin evidence flags. The required source-positive and generated-class audits are documented, but a mechanical structure pass does not demonstrate full semantic entailment for each one. The reported 100% Precision is therefore not a certified claim of perfect correctness.

## Generated occurrence and duplication re-audit

Phase 2 missed 101 independently substantive contextual occurrences: 88 register table cells and 13 other original-line duties. They are restored with original physical line positions and scope. The 190 potential duplicate pairs were challenged; 164 pairs were merged into 96 connected class clusters. Effective raw counts are 2553 occurrences and 2349 classes, with 204 excess occurrences (1 within-file and 203 across-file). Unchallenged paraphrase equivalences can still make this a conservative duplication estimate.

The independent Phase 5 validator reported 4 generated occurrence quotation-normalization warnings; original-file identifiers and physical line positions exist for all records. These warnings remain explicit, rather than being converted into semantic certification.

## Reconciliation and restrictions

- The single canonical universe contains 1,008 source positives + 37 source negatives + zero currently adjudicated definitive generated-only unsupported propositions = 1,045 units.
- TP + FN = 1,008; TN + asserted-negative-control FP = 37; FP = 0; TP + TN + FP + FN = 1,045.
- TP + FP counts effective canonical predictions, not the 2,349 raw generated classes.
- The independent validator passed structural links and arithmetic. It did **not** certify full semantic correctness, omitted requirements, or the complete originality of all class assignments.
- The source PDF, the eight scored Markdown inputs, and the 37 original negative controls were not altered.
- Phase 6 has not started.

## Primary machine-readable evidence

Use `01_source_atoms_final.jsonl`, `03_evidence_matches_final.jsonl`, `03_fn_root_cause_audit_final.jsonl`, `04_generated_claim_validity_final.jsonl`, `04_atomic_judgments_final.jsonl`, `04_duplicate_classes_final.jsonl`, `05_tp_evidence_audit_final.jsonl`, `05_source_atomization_audit_final.jsonl`, `07_change_delta.jsonl`, and `05_independent_validation_final.json`.
