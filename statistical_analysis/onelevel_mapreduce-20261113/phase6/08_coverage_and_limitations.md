# OrionDesk AI — Source Coverage, Evidence Quality, and Limitations

## 1. Baseline and method

Phase 6 evaluates the supplied original *OrionDesk AI Detailed Application Design Specification*, document ID OD-AI-DDS-001, R1.0 / revision 1.3 (90 physical PDF pages), against the eight supplied scored Markdown files. The same PDF-origin source atom inventory and bounded negative controls are used across methods; generated Markdown is **not** source evidence for inventing new PDF requirements. Exactly one scored corpus is present and its method label is not established by its filenames.

The final common source inventory includes **1020** PDF-positive atoms (five nonindependent parent summaries retired; a separately justified traceability child added) and **37** source-negative controls. The fixed negative controls are restricted to explicit exclusions, prohibitions and deferrals and cannot estimate all absent features.

## 2. Physical source and generated file coverage

- Authoritative PDF checksum (SHA-256): `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`. Original identity and 90-page extent match the Phase-1 source.
- All **90/90** physical pages contain readable extractable text. **31** pages contain raster diagrams/figures; Phase-1 visual coverage is retained. Figure 1.1 on physical page 8 was re-inspected in Phase 6 for three raster-only assertions.
- Exactly **2560** surviving PDF evidence locations were rechecked; **2560** match their cited physical pages; **0** do not. This count is lower than the Phase-1 total of 2,564 because Phase-5 atomization removed five parent rows and replaced one child.
- All eight current Markdown inputs are readable. Their total is **3123** physical lines and **4070** inspected Markdown table cells. Phase-2 line/table-cell enumeration is retained in `02_generated_line_and_cell_coverage_final.jsonl` and includes six Stage-8 editorial occurrences that Phase 5 correctly removed from eligible generated predictions. This is source-location coverage, not a verified proof that every meaningful assertion was atomized.
- **4217** eligible generated occurrences were checked against the actual file and physical line. **0** line-locator quotation discrepancies were detected. **87** normalized atomic fragments were not literal substrings; they require context-aware interpretation rather than being treated as quotation failures. Final TP quotations with unmatched cited lines: **0**.

## 3. Final canonical binary decision universe

- TP **981**; FN **39**; TN **37**; FP **0**; U **1057**.
- Precision **100.000000%**; Recall **96.176471%**; F1 **98.050975%**. These are valid numerical rates for the **present corrected ledger** only.
- Effective prediction positives **981** are **not** the number of distinct raw generated classes **4069**.
- All TN are scoped to the bounded PDF-negative control inventory. A missing assertion of a counterfactual is not proof of all possible negative requirements.

## 4. FN root-cause closure

- **5** TRUE_MISSING (best-effort corpus absence determination).
- **11** PARTIAL_ENTAILMENT (related text but unmet predicate).
- **23** CONSERVATIVE_UNRESOLVED (ambiguity after bounded challenge; not a certified omission).
- **917** initially nominated FN records were ultimately corrected to TP across the prior evaluation phases, according to the current root-cause ledger. The Phase-5 change delta specifically records **180** additional FN-to-TP changes.
- Every final FN is represented in `05_remaining_fn_recheck_final.jsonl` and `03_fn_root_cause_audit_final.jsonl` with source PDF evidence and generated candidate analysis. Exact/alias, context, universal and conjunction checks have varying independent evidence quality; search output alone is not a logical proof.

## 5. TP evidence and source atomization audit

- **981** TP evidence audit records exist with cited PDF and generated locators. **64** are explicitly marked HIGH_REVIEW_PRIORITY; **0** have an independently certified full-predicate proof. The remainder are best-effort structural/semantic judgments, not reviewed mathematical entailments.
- Source atomization audit: {'REMOVE_PARENT_OR_MERGE': 5, 'RETAIN_INDEPENDENT_BEST_EFFORT': 1019, 'NEW_SPLIT_CHILD': 1}. An audit row with no correction is not by itself evidence against over-splitting. Repeated universal boilerplate, acceptance-row overlap and parent/child restatements still require judgment-sensitive review.
- Phase 5 discarded six Stage-8 authoring workflow directives from definitive product predictions. That creates FP=0 in the current universe but does not prove the rest of the generated document corpus is wholly PDF-entailable.
- **3507** generated classes were labeled SUPPORTED_NONCOVERING. Their PDF-nearest matches and source scopes were identified; these are **not independently certified full entailments**. An unreviewed class must not be silently treated as proof of zero FP.

## 6. Duplicate checks

- Raw eligible occurrences **4217**, classes **4069**, excess **148**, within-file **12**, across-file **136**. Rate **3.509604%**.
- The raw class key uses a normalization plus scope/literal guard; unverified paraphrases may remain split. Conversely, some merged classes might differ in full predicates. The arithmetic partition is checkable, semantic equivalence is not independently certified.

## 7. Independent regression tests and residual blockers

The six search regression probes in `06_regression_probes_final.jsonl` cover case title, workspace retention class, identical idempotent case creation, transaction-pool tenant-context reset, exact review artifact hash and next-retrieval ACL revocation. Their located hits are **retrieval checks**, not unconditional promotions to TP. The original Phase-1/Phase-2 page and line coverage is retained for reproduction.

High-priority remaining work for external validation: independently prove **64** higher-risk TP bridges; substantively review **3507** generated-validity findings; challenge **23** conservative FNs and **11** partial FNs; inspect source over-splitting and repeated acceptance-test semantics; check remaining candidate-generation eligibility and equivalence.

**Certification status:** `NOT_INDEPENDENTLY_CERTIFIED_BEST_EFFORT`. Passing structural checks does not upgrade to verified semantic coverage. No invented confidence interval or lower-bound claim is made.

## 8. Individual-file reproducibility

The corrected item-level ledgers and scripts are provided as individual English files in one final directory. Run `python compute_metrics.py` in that directory to regenerate the Phase-6 metrics and validation reports. ZIP/TAR archives are not created under protocol 6.1.
