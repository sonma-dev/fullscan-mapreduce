# Phase 1 — Reuse and Verification of the fullload_cal Source Inventory

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** `6.1`  
**Phase boundary:** Phase 1 closed. Phase 2 not started. No evaluation metrics are calculated.

## Source authority and verified reuse

The sole authoritative source remains the supplied 90-physical-page *OrionDesk AI Detailed Application Design Specification*, document `OD-AI-DDS-001`, `R1.0 / revision 1.3`. The currently attached PDF is **byte-for-byte identical** to the original PDF used to construct the `fullload_cal` source inventory.

- Current PDF: `OrionDesk_AI_Detailed_Design_Specification(3).pdf`
- Original historical PDF SHA-256: `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`
- Current PDF SHA-256: `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`
- Physical pages: **90/90**, all with readable text; **31** pages contain embedded raster figures.
- The original source ledger and negative controls have been copied **unchanged at the byte level**, including `PDF-*` and `NEG-*` IDs, normalized English propositions, page numbers, original quotations, and their evidence locators.
- The evidence locator's historical filename `OrionDesk_AI_Detailed_Design_Specification.pdf` is retained intentionally because the source files are not rewritten. The PDF hash establishes exact equivalence with the newly uploaded `OrionDesk_AI_Detailed_Design_Specification(3).pdf`.

This is reuse of a previously extracted inventory from the **same authoritative PDF**, not use of a prior scoring judgment, aggregate JSON, or historical confusion matrix to invent PDF requirements. The extracted text quotations have been rechecked directly against the current PDF.

## Fixed common evidence universe

| Inventory | Count | Identifiers |
|---|---:|---|
| Normative PDF-positive requirements, `R` | **1,024** | `PDF-00001` through `PDF-01024` |
| PDF-negative counterfactual controls, `N` | **37** | `NEG-00001` through `NEG-00037` |
| Previously categorized source exclusion blocks | **274** | Current reconstruction: `EXCL-SRC-*` |

Each source-positive atom retains an original English passage, the physical page, scope and available obligation metadata. Every negative control retains its source PDF quote and rationale for exclusion, prohibition, or deferral. The negative controls are bounded and must not be interpreted as all possible non-requirements.

## Independent evidence validation

- PDF-text evidence quotations in the source-positive ledger: **2,524 / 2,524** matched the exact current physical page after whitespace/Unicode normalization.
- PDF-text evidence quotations for negative controls: **37 / 37** matched the exact current physical page.
- Figure-only quotations: **3 / 3**, checked against the embedded *Figure 1.1* runtime assertions on physical page **8**.
- Overall evidence locator matches: **2,564 / 2,564**.
- Source IDs: **1,024 unique**; negative control IDs: **37 unique**.
- Page-level source counts reconcile to **1,024**; page-level exclusion counts reconcile to **274**.
- No positive proposition is identical to a negative counterfactual in the two inventories.

The **literal original quotation** is preserved in the recovered ledgers. The source-only exclusions have been reconstructed as PDF block locators at the previously reported page-level exclusion counts. They are context/navigation/exemplar exclusions, not scores and not additional normative source propositions.

## Current scored-input mapping

All eight current Markdown files are present and readable as UTF-8. Their role mapping is unambiguous. These are future **Phase 2** scored inputs; they have not been used to modify, expand, or validate the common PDF requirement denominator.

| Role | Actual supplied filename | Lines | SHA-256 |
|---|---|---:|---|
| `01_screen_functions` | `01_screen_functions(3).md` | 437 | `b89b69e6b4b908c357f67c2f15cf9a4535043119af894a57e6cdbaa75baff514` |
| `02_api` | `02_api(3).md` | 482 | `db0e94dce9437a9d5b33346b85e0ee31f46df2d1bd4158948934bf39156d0dd3` |
| `03_data` | `03_data(3).md` | 411 | `f3eb127d819fca59285d46a0f2e75842c6039bdf899e8e9badaa71577332508c` |
| `04_batch_functions` | `04_batch_functions(3).md` | 274 | `a7b6927b273a03e4f878889bd2586e1a85f60ce2244f4bacde5b5f83fca1c72c` |
| `05_business_rules` | `05_business_rules(3).md` | 391 | `7d6934ccf8eb441c799f193066c1f0ef5344c27779073804cbbabf4cdc26167c` |
| `06_exception_handling` | `06_exception_handling(4).md` | 346 | `cebe3ad3538d3e5bac037f36ac8d0f2bbe6467b759203edb230536f95b40b6ff` |
| `07_processing_flows` | `07_processing_flows(4).md` | 369 | `0decb3f8128c7aef8b7dbef54836979a677eb927116136cfe8ca7cce2cebe41f` |
| `08_architecture_decision` | `08_architecture_decision(3).md` | 216 | `ed4804474726c338232ccca4d94641b64e8cb017c0225cfa218072bfef5ae6b3` |

The supplied protocol `OrionDesk_One_Pass_Atomic_Evaluation_Protocol(6).md` is an instruction file, not a ninth scored input.

## Atomization audit and bounded limitations

The original inventory has **no exact duplicate normalized atomic statements**. However, one original quote may legitimately support multiple independently testable duties (for example field type, nullability, default or key). Conversely, shared boilerplate and test rows can lead to over-atomization. The **19** high-priority same-passage cases in `01_atomization_review_candidates.jsonl` are provisional review candidates only; they are not declared errors and do not change the fixed `R` inventory.

Reusing source IDs and exact evidence across evaluation methods makes the denominator comparable. It does **not** prove that all 1,024 propositions have been perfectly atomized. Any demonstrable source split, duplication or nonnormative inclusion must be documented as an explicit, method-independent source correction during the protocol's designated correction phase.

## Individual deliverables

- `01_source_atoms_final.jsonl` — unchanged historical PDF-positive source ledger.
- `01_source_negative_controls_final.jsonl` — unchanged historical fixed negative controls.
- `01_pdf_page_coverage_final.jsonl` — unchanged historical physical-page coverage.
- `01_pdf_quote_verification_final.jsonl` — direct checks against the currently supplied PDF.
- `01_input_manifest_final.json` — actual eight Markdown filenames, sizes and hashes.
- `01_atomization_review_candidates.jsonl` — conservative independent review candidates.
- `09_excluded_units.jsonl` — source-only exclusion evidence locations, no generated scoring.
- `01_phase_status_final.json` — machine-readable phase completion evidence.

**Phase gate:** Phase 1 is complete at `BEST_EFFORT` evidence quality. No TP/TN/FP/FN, Precision, Recall, F1 or Duplicate result is asserted; no work on Phase 2 has been performed.
