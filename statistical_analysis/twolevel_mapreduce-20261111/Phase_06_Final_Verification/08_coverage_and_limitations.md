# Phase 6 — Coverage, Semantic Reliability and Limitations

**Final status:** `FINAL_BEST_EFFORT` — completed six-phase evaluation, not independently certified semantic correctness.  
**Source of truth:** 90-page original English OrionDesk AI Detailed Application Design Specification, `OD-AI-DDS-001`, baseline `R1.0 / revision 1.3`.  
**Method scope:** One current eight-file Markdown set; no other method was scored in this run.  
**Evaluation protocol:** Version 6.1.

## 1. Verified input scope and coverage

The authoritative PDF `OrionDesk_AI_Detailed_Design_Specification(3).pdf` has **90 physical pages**, all represented in `01_pdf_page_coverage_final.jsonl`. SHA-256 equals `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3` and is byte-identical to the previously used `fullload_cal` PDF source. The original `fullload_cal` source-positive and fixed-negative inventories were reused. The original source denominator is not derived from any previous score or aggregate JSON.

| Scored document role | Actual unmodified input filename | Physical lines | SHA-256 |
|---|---|---:|---|
| `01_screen_functions` | `01_screen_functions(3).md` | 437 | `b89b69e6b4b908c357f67c2f15cf9a4535043119af894a57e6cdbaa75baff514` |
| `02_api` | `02_api(3).md` | 482 | `db0e94dce9437a9d5b33346b85e0ee31f46df2d1bd4158948934bf39156d0dd3` |
| `03_data` | `03_data(3).md` | 411 | `f3eb127d819fca59285d46a0f2e75842c6039bdf899e8e9badaa71577332508c` |
| `04_batch_functions` | `04_batch_functions(3).md` | 274 | `a7b6927b273a03e4f878889bd2586e1a85f60ce2244f4bacde5b5f83fca1c72c` |
| `05_business_rules` | `05_business_rules(3).md` | 391 | `7d6934ccf8eb441c799f193066c1f0ef5344c27779073804cbbabf4cdc26167c` |
| `06_exception_handling` | `06_exception_handling(4).md` | 346 | `cebe3ad3538d3e5bac037f36ac8d0f2bbe6467b759203edb230536f95b40b6ff` |
| `07_processing_flows` | `07_processing_flows(4).md` | 369 | `0decb3f8128c7aef8b7dbef54836979a677eb927116136cfe8ca7cce2cebe41f` |
| `08_architecture_decision` | `08_architecture_decision(3).md` | 216 | `ed4804474726c338232ccca4d94641b64e8cb017c0225cfa218072bfef5ae6b3` |

The instruction document is not a ninth scored Markdown file. Original file names and physical-line locators are retained in evidence records. All eight input hashes and the recorded per-line inspection coverage were verified independently. The PDF contains **2561** verified text evidence quotations plus **3** figure-only assertions from page 8. Seven selected source pages (8, 23, 83, 85, 86, 87, 89) were additionally rendered for figure/table inspection; this visual spot check is distinct from the all-page text coverage ledger.

The generated corpus has **3810** definitive occurrences: **3792** from the Phase 2 occurrence ledger plus **18** recovered after an exclusion-eligibility challenge. They map to **3652** semantic classes, with an actual-file/line/table-cell locator per occurrence. **274** source exclusions and **2734** generated nondefinitive units are preserved in `09_excluded_units.jsonl`.

## 2. Final measured four-cell universe and its limits

| Canonical unit | Actual label | Predicted label | Count |
|---|---|---|---:|
| PDF-positive fully entailed (`TP`) | 1 | 1 | 979 |
| PDF-positive not fully demonstrated (`FN`) | 1 | 0 | 45 |
| PDF-negative counterfactual asserted (`FP` subset) | 0 | 1 | 0 |
| Unsupported generated-only definite propositions (`FP` subset) | 0 | 1 | 0 |
| Fixed PDF-negative counterfactual not asserted (`TN`) | 0 | 0 | 37 |

The canonical decision ledger has **1061** units, and all four cells reconcile to that single enumerated universe. `TP + FN = 1024`; `TN + asserted controls = 37`; `FP = asserted controls + generated-only unsupported classes`. The tested negative controls are a small, explicit and predetermined PDF-grounded set; TN is **bounded diagnostic evidence**, not a universal true-negative population.

Conventional effective-universe Precision is **100.00%**, Recall **95.61%**, F1 **97.75%**. These are **provisional evidence-grounded adjudication rates**. The raw-class positive count and the effective canonical positive count differ because generated universal statements can entail several independently meaningful PDF atoms; it would be mathematically wrong to force `TP + FP = G`. An unmatched generated class is not automatically an FP.

## 3. FN root causes, corrections and reciprocal retrieval

All **630** source atoms initially nominated as FN during the earlier matching stage have preserved root-cause records. **585** were subsequently corrected to TP (415 during the source coverage stage and 170 during the correction stage). The final FN set is **45**, precisely:

| Final FN disposition | Count | Interpretation |
|---|---:|---|
| `TRUE_MISSING` | 0 | Verified missing within scored corpus after checks |
| `PARTIAL_ENTAILMENT` | 11 | Related specification text exists, but one or more complete predicates are unproven |
| `CONSERVATIVE_UNRESOLVED` | 34 | Accessible evidence is ambiguous after bounded candidate inspection; no verified absence claim |

The entire set of **45 final FN** has undergone another Phase 6 source-key/alias scan of every scored Markdown file. Actual generated line candidates are saved to `06_fn_reciprocal_recheck_final.jsonl`, and `03_fn_root_cause_audit_final.jsonl` was supplemented with the real lookup terms and audit references. This resolves an evidence-recording gap found during the Phase 6 independent check; the scoring cells themselves did not change. No final FN was identified by a contiguous exact full-statement match in the corpus. That check is diagnostic: equivalent paraphrases or multi-file bridges can still be missed.

Representative final FN records (not the full ledger):

| Source atom | Disposition | Original reviewed candidates |
|---|---|---:|
| `PDF-00005` | `CONSERVATIVE_UNRESOLVED` | 10 |
| `PDF-00022` | `CONSERVATIVE_UNRESOLVED` | 10 |
| `PDF-00023` | `CONSERVATIVE_UNRESOLVED` | 10 |
| `PDF-00024` | `CONSERVATIVE_UNRESOLVED` | 10 |
| `PDF-00025` | `CONSERVATIVE_UNRESOLVED` | 10 |
| `PDF-00029` | `CONSERVATIVE_UNRESOLVED` | 10 |
| `PDF-00031` | `PARTIAL_ENTAILMENT` | 10 |
| `PDF-00045` | `CONSERVATIVE_UNRESOLVED` | 10 |
| `PDF-00046` | `CONSERVATIVE_UNRESOLVED` | 10 |
| `PDF-00074` | `PARTIAL_ENTAILMENT` | 10 |

The full **45** record-level dispositions are in `03_fn_root_cause_audit_final.jsonl`; these examples do not replace the complete audit.

## 4. TP full-predicate proof limitations

Each of the **979** final TP atoms has a source/target link in `05_tp_evidence_audit_final.jsonl`. They split into **15 E3 direct** and **964 E2** claims. E2 bridge types are:

| Entailment bridge | TP atoms |
|---|---:|
| `UNIVERSAL_INSTANTIATION` | 259 |
| `INHERITED_CONTEXT` | 321 |
| `CONJUNCTIVE_BRIDGE` | 179 |
| `SEMANTIC_EQUIVALENCE` | 205 |

All **1525** cited generated quotation locations were checked against unchanged original Markdown line text. Nonetheless, many predicate-check maps contain an explicit `not-applicable`/`null` field justified by broad contextual assumptions, and many E2 proofs are machine-assisted, not independent expert semantic review. **No TP has been certified as a human-verified full-predicate proof across all applicability conditions.** The report therefore does not promote Phase 5's `BEST_EFFORT` cells to `VERIFIED` merely because original citations exist.

High-risk areas for further independent human review include inherited role and resource authorization, approval-versus-publication, request acceptance-versus-completion, retry/timeout semantics, aggregate revision concurrency, and exact API method/status/table contexts. This is a risk categorization, not a claim that those individual TPs have failed.

## 5. Generated-only correctness and FP uncertainty

The generated claim validity ledger includes **3652** classes: **1691** provisionally labeled `PDF_ENTAILED`, **1961** labeled `SUPPORTED_NONCOVERING`, and **0** definitively labeled `PDF_UNSUPPORTED`. Their evidence grades are **8 E3**, **426 E2**, and **3218 E1_BEST_EFFORT**.

**This is the main reliability limitation:** 3218 classes lack independently certified full-source support, even though the ledger has not positively isolated an unsupported residual proposition. Therefore **FP=0 is an unproven best-effort estimate** and **Precision=100% must not be reported as verified correctness**. Fully supported noncovering classes require affirmative PDF entailment, not simply topical similarity. The current corpus includes short table cells that were checked with inherited row/column context; some may require more independent review.

## 6. Source atomization audit

The frozen source inventory contains **1024** source positives and **37** fixed negatives, identical across the intended method-comparison basis. All 1024 positive atoms have a Phase 5 atomization decision. The dispositions are:

| Atomization decision | Count |
|---|---:|
| `HIGH_LEVEL_SUMMARY_RETAINED_WITH_PARENT_CHILD_RISK` | 1 |
| `INDEPENDENT_PREDICATE_CHILD_OR_REVIEWED_SHARED_PASSAGE` | 496 |
| `NORMATIVITY_BOUNDARY_RETAINED_WITH_UNCERTAINTY` | 2 |
| `NO_ATOMIZATION_CHANGE` | 523 |
| `PDF_LINE_WRAP_REPAIRED_NO_ATOM_COUNT_CHANGE` | 2 |


Two PDF line-wrap corrections restore the literal endpoint `/v1/workspaces/{workspaceId}/members` in source atom normalization without replacing the original PDF quotes or changing source IDs or the denominator. This was independently visualized on **physical page 23**. The source count delta is **0**. One high-level summary and two normativity-boundary cases remain explicitly uncertain; the retained parent/child and common-boilerplate analyses are *best-effort*, not certified proof that 1,024 is the uniquely correct atomic denominator. Any future correction must be applied across all evaluated methods.

The Phase 5 change ledger records **170** FN-to-TP corrections, **23** generated semantic-class merges, **41** TP-evidence relinks, and **2** source line-wrap fixes. Each category has case-level entries in `07_change_delta.jsonl`.

## 7. Raw semantic duplication and its scope

The duplication formula is `(GO − G) / GO`, using raw occurrence and class counts rather than expanded source coverage. Final raw Duplicate = **4.15%**, with excess occurrences **158**, across-file **158**, within-file **0**, repeated classes **123**, and multi-file repeated classes **123**.

The 23 Phase 5 class merges correct only the pairs that were adjudicated. Other semantically equivalent paraphrases may remain separate classes; this can understate duplication. Conversely, erroneous merges of slightly different actor/condition/outcome predicates would overstate duplication. The value is therefore reproducible for these ledger decisions but is not guaranteed to be unique under all reasonable interpretations.

## 8. Verification matrix and regression probes

The independent checker verifies all raw occurrence-class relationships, unique IDs, source and negative identities, exact four-cell equations, raw duplication partition, original eight-file hashes and recorded nonblank line coverage, PDF 90-page coverage and quotation pages, 979 TP audit entries and 45 FN root-cause records. It also crosschecks all 37 negative controls and validates source line-wrap and class-change delta relationships.

`06_regression_probes_final.jsonl` records full-corpus keyword and actual-location probes for: case title, workspace retention class, repeated same-key case creation, `/members` after PDF wrapping, case revision `If-Match`, `ApprovalDecisionRecorded` and separate publication, and cross-tenant denial. The probes are retrieval diagnostics, **not automatic semantic proof**. Every final FN was reciprocally re-searched and recorded in `06_fn_reciprocal_recheck_final.jsonl`.

The three pages 23, 83, and 85–87 provide especially important register/table inheritance cases; page 89 provides verification-test overlap. The checker confirmed the PDF bytes and text citations on their actual physical page, rather than using a derived summary as source authority.

## 9. Overall confidence and stop rule

**Structural confidence:** The enumerated ledger and all stated arithmetic invariants reconcile; every scored input is present and unchanged; source and generated evidence locators exist.  
**Semantic confidence:** `BEST_EFFORT`, not externally certified. The 34 conservative FN, 11 partial FN, 964 machine-adjudicated E2 TPs, 3,218 E1-grade generated-class validity records, and source atomization boundary cases limit interpretation. These uncertainties may move Precision, Recall, F1 or Duplicate in either direction; no error interval or guaranteed lower bound is claimed.  
**Production meaning:** This is an evaluation of generated specification coverage against one controlled fictional PDF; it is not a measurement of deployed software, security enforcement, production availability or provider accuracy.  
**Comparisons:** No comparison artifact is created because only one complete eight-file set was explicitly selected for scoring in this run.  
**Completion:** All six requested phases are closed. No archive is created; all JSONL, JSON, Markdown and Python outputs are individually available.

## Reproducibility

Execute `python compute_metrics.py` from this output directory with the unchanged original inputs mounted in the parent directory. The checker independently recomputes and rewrites the metrics and validation JSON files. `06_recheck_fn_retrieval.py` documents the additional full-corpus FN retrieval audit introduced in Phase 6. Full source and generated ledgers remain in their documented filenames. The original eight scored Markdown inputs are never rewritten.
