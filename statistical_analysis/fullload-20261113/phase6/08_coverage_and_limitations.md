# Final Coverage, Evidence Audit, Corrections and Limitations

**Document baseline:** *OrionDesk AI Detailed Application Design Specification*, 90 physical pages, OD-AI-DDS-001, R1.0 / revision 1.3.  
**Method:** the eight unchanged supplied Markdown specifications (`01_screen_functions(6).md` through `08_architecture_decision(6).md`).  
**Evaluation protocol:** v6.1; exactly six completed phases.  
**Status:** FINAL_BEST_EFFORT. There is **no independent semantic certification**.

## One canonical effective-proposition universe

- Independently maintained PDF-positive inventory R: **1024**. The same `fullload_cal` source IDs and original PDF quotations were retained.
- Predeclared, PDF-grounded, bounded negative controls N: **37**. These are explicit counterfactuals, not a general inventory of everything absent from the design.
- Unsupported generated-only canonical propositions F: **812**. No excluded-capability negative control is positively asserted.
- One binary universe U = R disjoint-union N disjoint-union F: **1873** rows.
- Actual/predicted totals: **TP 654; TN 37; FP 812; FN 370**.
- Precision **44.61%**, Recall **63.87%**, F1 **52.53%**.
- Raw generated classes **2550** and canonical predicted-positive units **1466** are intentionally different. The conventional Precision is calculated over the **effective canonical proposition universe**, not the raw generated-class denominator.

## Source PDF, input coverage and traceability

- Every one of the **90 physical PDF pages** contains readable extracted text. The complete page audit and 1024 source-positive quotations are retained. **1021** quotations match extracted text on their physical page; **three** come from Figure 1.1 on physical page 8 and were visually checked using a page render.
- All **eight** supplied scored Markdown roles are available and unchanged; **3956** physical lines are present. Their earlier full-line and table-cell audit reports zero substantive unclassified lines. This final phase verified every one of the 2618 active generated occurrence's quoted text at its original physical line and 872 / 872 source-coverage generated evidence locators.
- `08_architecture_decision(6).md` is scored only for definitive confirmed decisions. Unadopted proposals, TBDs and unresolved alternatives are not adopted predictions. Exclusions are itemized in `09_excluded_units.jsonl`.

## Reciprocal FN challenge and reliability

All remaining **370** FN source atoms have root-cause records, reverse-lookup candidates, and descriptions of missing predicates. Final distribution:

| Final FN disposition | Count | Interpretation |
|---|---:|---|
| TRUE_MISSING | 111 | No defensible full implementation commitment located in the bounded reviewed corpus |
| PARTIAL_ENTAILMENT | 68 | Related definitive evidence exists, but identified required predicates remain absent |
| CONSERVATIVE_UNRESOLVED | 191 | Semantic applicability remains inconclusive; not a certified absence |

The initial challenged-FN ledger contains **621** records, including **251** corrected to TP across Phase 3 and Phase 5. A recovered exact/complete match was not deliberately left scored FN in the targeted regression probes. However, the residual conservative set remains subject to semantic review; the computed Recall is **not certified actual requirement coverage**, a guaranteed lower bound, or a calibrated interval.

Regression probes include a case title field (TP), workspace retention class (TP), identical-replay case creation (TP), the `/members` schema/error predicate (FN; path alone is insufficient), and the transactional-outbox primary profile (conservative FN; further deployment-profile applicability proof remains necessary). The actual sources and generated locations are recorded in `06_reciprocal_regression_probes_final.jsonl`.

## TP evidence proof audit and limitations

All **654** final TP records appear once in `05_tp_evidence_audit_final.jsonl` with PDF and generated locators, declared E2/E3 grades, and ten predicate-check slots (target, action, actor, condition, scope, timing, constraint, exception, outcome and version). **22** previous TP proof candidates were downgraded to FN in Phase 5 because endpoint coincidence was not a complete schema/error guarantee.

The existence of a filled checklist does not certify that its semantic reasoning is sound. Some E2 bridge narratives are formulaic. Thus all final 654 TP proofs are best-effort, not independently expert-certified. An E2 universal or conjunctive bridge is counted as TP only when the recorded scope and predicates appear complete; residual errors can change either the numerator or denominator after expert review.

## Source atomization challenge

The audit holds **1024** source atomization records, preserving source IDs and original quotes. The 16 Appendix E release-test scenarios were checked as independently required verification actions rather than arbitrarily repeated implementation obligations. Repeated chapter-level interface boilerplate, field rows inheriting table scope, and parent/child overlap were challenged. The page-23 `/members` wrap normalization does **not** change the R denominator. No independently confirmed duplicate source atom was merged in this final phase; any unresolved source atomization ambiguity remains documented rather than assigned a new, method-specific denominator.

## Generated-claim validity and Phase-6 correction

- Class validity: `PDF_ENTAILED` **909**; `SUPPORTED_NONCOVERING` **829**; `PDF_UNSUPPORTED` **812**.
- This phase independently identified **27** complete PDF-grounded matches among earlier unsupported generated-only claims (e.g. authorized Reviewer decisions, signed/tenant-bound requests, exact 200/202 endpoint results, immutable review expiry, and Appendix E cases). Those canonical FP rows were removed and validity relabeled with source page quotations; each correction is in `06_direct_source_rescues_final.jsonl` and `07_change_delta.jsonl`.
- Supported-but-noncovering classifications require affirmative PDF entailment and do not create method-specific source atoms. Many of the **829** such classes rely on provisional contextual support. The **812** remaining PDF_UNSUPPORTED cases are *provisional unentailed generated propositions*, not certified design defects; source lookup can still have false positives/negatives.

## Semantic duplication

- Eligible raw occurrences **2618**; raw unique semantic classes **2550**; excess **68**; duplication **2.60%**.
- Within-file excess **6** and across-file excess **62** reconcile exactly; 54 classes repeat and 50 span multiple files.
- Source-coverage one-to-many projection never creates additional raw generated occurrences or artificially increases duplication.

## Status and interpretation

`compute_metrics.py` independently reconstructs the four cells from the final JSONL ledgers; validates unique IDs, binary labels, ledger links, reported FN root causes, TP proof-locator presence, negative-control polarity, raw duplicate partition, all eight input files, 90 PDF pages, and original generated quotation locations. This is a **structural and provenance verification pass**, not a semantic-evidence certification. `FINAL_BEST_EFFORT` is the appropriate terminal status; no later evaluation phase is implied, and individual English files are delivered without an archive.
