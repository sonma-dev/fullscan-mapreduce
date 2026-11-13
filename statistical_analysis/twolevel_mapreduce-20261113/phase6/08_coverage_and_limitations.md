# Phase 6 — Coverage, Evidence Quality, and Limitations

**Protocol:** OrionDesk AI One-Pass Atomic Evaluation Protocol v6.1  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`; **semantic-evidence certification: NOT ACHIEVED**.

## Evaluated source and generated corpus

The authoritative PDF is `OrionDesk_AI_Detailed_Design_Specification(10).pdf` (SHA-256 `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`), document `OD-AI-DDS-001`, R1.0 / design revision 1.3, with **90 physical pages**. Phase 1 provides a per-page inspection record for each page and 2,564 verified evidence excerpts. This final-phase script independently opened the PDF, checked its page count and digest, and rechecked each surviving source quotation. In addition, visual samples of the REST resource table on p.83 and reference DDL on p.86 were inspected.

The eight submitted Markdown files were read without modification: `01_screen_functions(8).md`, `02_api(8).md`, `03_data(8).md`, `04_batch_functions(8).md`, `05_business_rules(8).md`, `06_exception_handling(9).md`, `07_processing_flows(9).md`, `08_architecture_decision(8).md`. Their physical-line coverage contains **2,926 rows**, and the original per-table-cell coverage contains **3,769 rows**. All individual generated occurrences point to existing files and physical lines. The four prior occurrence quote-normalization discrepancies remain review warnings, not silently repaired source text.

The final cross-method PDF-positive inventory has **1,008 atoms** after 16 transparent Phase 5 removals from the original 1,024. The fixed PDF-negative set has **37** controls. Their IDs and PDF citations remain independent of the generation method. Any future evaluation of other methods must use the corrected shared PDF-positive inventory and exactly the same negative controls.

## Recomputed canonical scores (one universe)

TP=963, FN=45, TN=37, FP=0; Precision=100.00%, Recall=95.54%, F1=97.72%. The universe has 1045 canonical propositions, not 2349 raw generated classes. The raw duplication count is 2553 occurrences, 2349 classes, 204 excess, 1 within-file and 203 across-file: 7.99%.

**Note:** The canonical-universe file was stale at the start of Phase 6 (historical Phase 4: 1125 rows). It was regenerated from the final 1045 judgment rows; no scores, classifications or source atoms were changed in this repair.

## FN root cause and reciprocal challenges

| Final FN disposition | Count | Interpretation |
|---|---:|---|
| TRUE_MISSING | 13 | A documented best-effort corpus-wide search found no eligible full implementation commitment. |
| PARTIAL_ENTAILMENT | 20 | Relevant text exists, but material required predicates are missing. |
| CONSERVATIVE_UNRESOLVED | 12 | Semantic uncertainty persists; absence is not certified. |

Initial FN challenges number 565: 504 were ultimately corrected to TP, 16 were removed/merged from `R`, and the remaining 45 are disposed as shown. See `03_fn_root_cause_audit_final.jsonl` and `07_change_delta.jsonl` for actual identifiers, alternatives, citations and reasons.

## TP evidence audit and proof limitations

The 963 final TP rows have corresponding TP-audit and original Markdown physical-line locators; 950 have non-direct coverage bridges, while 13 are recorded direct. The prior TP-audit record count is 964 because one initially positive, non-independent source summary was removed. Audit classifications: 748 best-effort present and 215 qualified.

A normalized PDF text search matched 1005 of 1008 final PDF-positive excerpts contiguously. The other 3 are verbatim on page 8 Figure 1.1 and were visually checked against the high-resolution page render, leaving 0 unverified source quotes. The text-versus-figure verification method is recorded in `06_pdf_quote_recheck_final.jsonl`. Neither Phase 1 text verification nor current textual linkage proves logical entailment of every predicate in each TP. **Do not label the 963 TP as independently human-verified.**

## Generated-claim correctness uncertainty

The generated validity ledger classifies 636 classes as `PDF_ENTAILED` and 1713 as `SUPPORTED_NONCOVERING`, with zero currently scored `PDF_UNSUPPORTED` classes. Crucially, 1269 generated classes carry E1 partial-support evidence, including **36 classified as `PDF_ENTAILED`** despite E1 and **1233 `SUPPORTED_NONCOVERING` E1**. These are not independent affirmative full-predicate proofs and remain semantic-review exceptions in `06_validation_exceptions_final.jsonl`. Therefore FP=0 and Precision=100% cannot be certified as generated claim correctness, and should not be presented as an empirically bounded upper/lower accuracy estimate.

The 37 negative controls are an intentionally bounded set built from explicit PDF exclusions and prohibitions, **not** an exhaustive population of nonexistent requirements. Adding other absent propositions would change TN but not measure actual specificity.

## Source atomization audit and common-denominator corrections

The atomization audit examined 1,024 original source items. 16 were removed as non-independent or illustrative; the remaining 1008 retain source identifiers. These corrections apply to **all** generation methods in any controlled comparison, not just the method evaluated here. The exclusion ledger records these removals along with nonnormative PDF and non-definitive generated statements. Remaining potential splitting/merging and overlapping test-matrix assertions should be treated as review risks rather than suppressed by arithmetic reconciliation.

## Coverage, assertions and verdict

- PDF pages and input Markdown line/cell coverage are structurally complete.
- Canonical judgment consistency, source/negative IDs, raw occurrence/class memberships and within/across duplicate arithmetic pass independent checks.
- Representative regression probes for case title, workspace retention class, repeated idempotent case creation and case tenant uniqueness have recorded TP evidence. The probes are not complete manual semantic validation.
- The original canonical-universe-vs-judgments mismatch was repaired in Phase 6.
- E1 generated validity classes and noncontiguous PDF evidence excerpts prevent a `FINAL_VERIFIED` designation.

**Final designation: `FINAL_BEST_EFFORT`, `PHASE_COMPLETED_BEST_EFFORT`.** No Phase 7 exists in this six-phase protocol; no ZIP/TAR archive was generated.
