# OrionDesk AI — Coverage, limitations, and evidence certification

**Protocol:** v6.1. **Evaluation status:** `FINAL_BEST_EFFORT`. **Only one supplied complete eight-file generated method** was evaluated, identified as `supplied_eight_file_set`. No cross-method comparison is applicable. Original authored scored Markdown files are unchanged; only evaluation ledgers were corrected in earlier phases and one duplicated audit-history record in this final phase.

## 1. Ground truth and corpus provenance

The sole source of normative requirements is `OrionDesk_AI_Detailed_Design_Specification(9).pdf`, an English 90-page PDF (`OD-AI-DDS-001`, `R1.0 / revision 1.3`). The PDF is explicitly a fictional reference architecture; quoted capacity/availability figures are design assumptions, not observed production performance. See the source-atom ledger for page-specific original English quotations and Figure 1.1 for image-bound requirements.

| Scored role | Unchanged actual input file | Physical lines |
|---|---|---:|
| `01_screen_functions` | `01_screen_functions(7).md` | 437 |
| `02_api` | `02_api(7).md` | 482 |
| `03_data` | `03_data(9).md` | 411 |
| `04_batch_functions` | `04_batch_functions(20261115-043829).md` | 274 |
| `05_business_rules` | `05_business_rules(9).md` | 391 |
| `06_exception_handling` | `06_exception_handling(20261115-043822).md` | 346 |
| `07_processing_flows` | `07_processing_flows(20261115-043821).md` | 369 |
| `08_architecture_decision` | `08_architecture_decision(10).md` | 216 |


All **90** PDF pages are recorded in `01_pdf_page_coverage_final.json`. The **2,926** Markdown physical lines have a final line-by-line coverage ledger; `02_generated_corpus_coverage_final.json` updates the Phase 2 baseline to include 12 Phase 5 recovered occurrences. The original Phase 2 summary (`02_generated_corpus_coverage.json`) is historical and must not be substituted for final counts.

The frozen, corrected source-positive inventory has **1005** atoms; the predeclared negative-control diagnostic inventory has **37** controls. The 37 controls derive from explicit source prohibitions, exclusions, and release deferrals. `TN = 37` cannot measure the infinite population of unasserted requirements. `R` and `N` share neither proposition identity nor scoring unit.

## 2. Semantic coverage results and FN root causes

The final canonical universe contains **1042** entries: TP 977, FN 28, TN 37, FP 0 (established in the current ledger only). Canonical Precision 100.0000%, Recall 97.2139%, and F1 98.5873% depend on the validity of their underlying semantic adjudications. A shared generated rule can cover several distinct independently testable PDF atoms; therefore positive canonical predictions are not raw generated classes.

| Final FN disposition | Count | Interpretation |
|---|---:|---|
| `TRUE_MISSING` | 0 | No verified total omission assigned in the final ledger. |
| `PARTIAL_ENTAILMENT` | 8 | Actual related generated obligations were located, but at least one source-required predicate was not established. |
| `CONSERVATIVE_UNRESOLVED` | 20 | Candidate matches were searched, but complete logical implication was not demonstrated under the bounded review. These are not verified absences. |
| **Total final FN** | **28** | All have individual evidence/candidate records. |

The FN root-cause file has **923** unique source-origin review records, of which **895** are corrected matcher misses currently scored TP and **28** retain FN status. Full-corpus checks include exact target/quote checks, schema/API identifiers, universal constraints, table-row context and available conjunction bridges. An exact whole-quote probe for every final FN located no verbatim whole-quote hit; that absence **alone** does not prove semantic absence. The strongest candidate and specific unmet predicates remain in the FN ledger. The Phase 6 repair removed one obsolete `PDF-00613` corrected-to-TP record whose source had been downgraded to FN; the final `PARTIAL_ENTAILMENT` record was retained. See `07_change_delta.jsonl` and `06_regression_probe_evidence.jsonl`.

Regression cases verified by actual source IDs and real generated-line citations include case title (`PDF-00208`), workspace retention class (`PDF-00199`), same-key duplicate case/identical response (`PDF-00948`), revision conflict (`PDF-00222`), and immutable attachment lineage (`PDF-00442`). These are smoke checks for accidental matcher regressions, **not** a substitute for full entailment auditing.

## 3. TP evidence qualification

Every final TP has exactly one audit record (977 `CONFIRMED_TP` rows), and an additional corrected-to-FN history record exists for `PDF-00613`. Final coverage grades are **14 E3 direct matches** and **963 E2 bridges**; 8 E1 and 20 E0 are FN. The bridge ledger records universal-scope/section-inherited/conjunctive/semantic-equivalence evidence rather than merely the presence of a shared identifier. However all **978** TP-audit rows are explicitly `EXPLICIT_BEST_EFFORT_NOT_CERTIFIED`: predicate checks and locations are present, but no independent human-level full-predicate certification is claimed. This distinction is consequential: a programmatic structural pass cannot convert E2 into verified semantic equivalence.

PDF source evidence: **1002** atom quotes match the PDF text layer on their recorded page. The other **3** are exact labels in Figure 1.1 (p.8): "tenant_id and actor context at every boundary", "immutable evidence and versioned policy inputs", and "idempotent event processing with trace correlation". They were visually checked in the original page rendering. Figure captions and mockup values were not automatically promoted to new requirements.

## 4. Source atomization and corrections

`05_source_atomization_audit_final.jsonl` contains **115** records: **19** excluded independently nonnormative/overlapping atoms, **2** corrected line-wrap source references and **94** retained candidates after bounded context review. The removed units include illustrative A2A JSON fields and error-envelope example properties that were not presented as universal required schema fields, plus repeated summary/background claims. A PDF p.23 word-wrap that had split `/v1/workspaces/{workspaceId}/members` was corrected. The old-source/new-source mappings and original page quotes remain in this ledger and `07_change_delta.jsonl`. No new PDF requirements were inferred from a generated Markdown answer.

The final Phase 5 source inventory is not guaranteed to be perfectly atomized: the 94 retained review candidates did not receive independent expert certification, and inclusion/exclusion of test-matrix repetitions can still affect the Recall denominator. The Phase 6 audit-history dedup changed neither the `R` count nor any canonical score.

## 5. Generated correctness and false-positive uncertainty

The raw generated universe has **3128** eligible occurrences and **3018** same-method semantic classes. Class-validity labels in `04_generated_claim_validity_final.jsonl` are **1170** `PDF_ENTAILED` and **1848** `SUPPORTED_NONCOVERING` in the prior best-effort adjudication. Crucially, **2353** class PDF-support grades are `E1_UNCERTAIN`, **239** have possible nondefinitive extraction concerns, and **3018** have not been independently semantically certified. The `PDF_ENTAILED` and `SUPPORTED_NONCOVERING` labels must therefore be read as prior provisional dispositions, not finalized independent proofs.

No unsupported generated-only proposition (`F`) and no asserted negative control (`B`) were recorded, so the **currently enumerated** FP count is 0. This cannot be used to assert there are no unsupported generated commitments. `Precision=100%` and the derived `F1` are provisional and could change materially if an E1-uncertain generated class is found unsupported. Conversely, overly restrictive FN decisions may understate coverage. These are uncertainty sources in both directions, not a calculated confidence interval.

## 6. Raw duplication and class eligibility

Raw excess is **110** (within-file **1**, across-file **109**); duplication is **3.5166%**. **80** repeated classes exist and **80** span files. Only eligible definitive occurrences count; document titles, unapproved options and mapping-only citations do not create classes. The 589 candidate-pair review records preserve source-specific reasons why similar statements were or were not merged. Some remaining equivalences may be unmerged, so the computed duplication is not certified as the true semantic repetition rate.

## 7. Structural checks and unproven assertions

The independent `compute_metrics.py` checks IDs, one canonical decision per proposition, binary cell labels, TP and FN audit membership, class-to-occurrence partitions, no cross-method leakage, source-atom exclusions, generated quote/line positions, all physical Markdown line hashes, full final occurrence line coverage, 90 PDF pages, and relevant algebra. The current checker reports **zero** generated citation/line mismatches. It does **not** prove all source predicate entailments or generated-class PDF correctness, nor that an old quoted table context is semantically complete. It also does not independently rerun the initial source-atom extraction from scratch; it verifies final evidence and correct page references. No claim of independent external certification, actual implementation conformance, production reliability, or security is made.

## 8. Delivery and reproducibility

All final authored deliverables are English, with all retained input filenames unchanged in evidence locators. Required item-level outputs are placed individually in the `oriondesk_phase6` folder. No ZIP/TAR archive was created. Execute `python compute_metrics.py --ledger-dir . --original-dir .. --output-dir .` to independently recompute `06_metrics_final.json` and `06_validation_results.json`. If PyMuPDF is installed, the script verifies the original 90-page PDF and source quotations; p.8 embedded figure labels remain documented in `06_visual_pdf_evidence_audit.jsonl`.

**Final status: `FINAL_BEST_EFFORT` — structurally reproduced scores, not semantically certified quality metrics.**
