# Phase 1 — PDF Evidence-Backed Requirements and Fixed Negative Controls

**Protocol:** OrionDesk One-Pass Atomic Evaluation Protocol, version 6.1.  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`.  
**Scope:** Exactly Phase 1; no generated occurrences, source-to-generated judgments, or accuracy scores have been computed.  
**Source baseline:** OD-AI-DDS-001, R1.0 / design revision 1.3.

## Reuse decision and authoritative-source boundary

The uploaded `OrionDesk_AI_Detailed_Design_Specification(6).pdf` is a complete, readable 90-page English PDF. Its SHA-256 is `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`, matching the original `fullload_cal` source fingerprint. The PDF is the **sole source of normative obligations**. The original `fullload_cal` source-positive and fixed-negative JSONL files were recovered from its historical archive, independently compared with two other preserved ledger copies, and retained **byte for byte**; neither prior generated-document judgments nor historical scores were reused.

The original source ledger contains **1,024** positive atoms (`PDF-00001`–`PDF-01024`); the fixed bounded control set contains **37** controls (`NEG-00001`–`NEG-00037`). Both are stable across evaluation methods. The copied PDF alias `OrionDesk_AI_Detailed_Design_Specification.pdf` is byte-identical to the uploaded source and matches the PDF filenames recorded in the evidence locators. The actual uploaded filename and alias relationship are preserved in `01_input_manifest_final.json`.

## Evidence reconciliation

| Current source audit | Result |
|---|---:|
| Physical PDF pages checked | 90 / 90 |
| Positive source atoms | 1,024 |
| Fixed bounded negative controls | 37 |
| PDF-only exclusions | 274 |
| PDF evidence locations checked | 2,564 |
| Exact normalized page-text quotation matches | 2,561 |
| Embedded Figure 1.1 line quotations visually confirmed (page 8) | 3 |
| Unmatched evidence locations | 0 |
| PDF pages containing raster images/figures | 31 |

The three raster-only Figure 1.1 requirements are `PDF-00977` through `PDF-00979`. The source page-coverage register reconciles all 90 physical pages, 1,024 positive atoms and 274 PDF exclusions. The 31 image-bearing pages were rendered and checked as three visual contact sheets, with page 8 inspected separately at readable resolution. This is an evidence-access check, not a machine proof of independent atomicity.

The **37 negative controls are bounded PDF-grounded counterfactuals**, not a comprehensive catalog of everything absent from the design. A prohibited capability is recorded as a positive obligation when applicable; its affirmative counterfactual can separately serve as a negative control with distinct polarity and ID.

## Source atomization challenges and deliberate retention

The same source inventory is preserved as requested. Under protocol v6.1, **19 review records** identify possible overcount risks: 16 Appendix E acceptance-scenario records and three grouped checks covering repeated interface boilerplate, chapter contract/test overlap, and inherited Appendix B field/DDL context. These are **not findings of 19 confirmed duplicates**; a distinct obligation to execute an acceptance test can remain independent of the product behavior it tests. The challenge ledger names actual source IDs and PDF quotations, and no source IDs or values have been silently changed.

The retained 1,024-item denominator is thus an explicitly **best-effort historical source inventory**, not a newly certified count of independently meaningful obligations. If substantive duplicated test expectations or over-split universal duties are confirmed, later correction must preserve old/new IDs and be applied to all methods consistently. Quotation matching and arithmetic alone cannot eliminate such semantic risks.

## Input scope and phase boundary

All eight current scored Markdown roles were mounted, identified and decoded as UTF-8 without modification. Their exact filenames and SHA-256 hashes are in `01_input_manifest_final.json`. No generated requirements were used as PDF source evidence. The generation method was not explicitly named; exactly one complete eight-document set is present. Detailed generated line/table-cell extraction belongs **only to Phase 2**.

PDF exclusions retain headings and front matter, reference-only captions, nonnormative samples, unadopted options, and deferrals outside the positive inventory. `09_excluded_units.jsonl` includes the 274 original PDF-only exclusions, not generated-document exclusions from a historical multi-phase archive.

## Files and reproducibility

- `01_source_atoms_final.jsonl`: byte-identical `fullload_cal` PDF-positive ledger.
- `01_source_negative_controls_final.jsonl`: byte-identical fixed negative controls.
- `01_pdf_page_coverage_final.jsonl`: complete 90-page source coverage.
- `01_pdf_quote_verification_final.jsonl`: all 2,564 per-evidence verification records.
- `09_excluded_units.jsonl`: 274 PDF-only exclusion records.
- `01_source_atomization_challenge_final.jsonl`: 19 grounded audit candidates, no unadopted corrections.
- `01_input_manifest_final.json`: actual source and scored filenames, hashes and mapping.
- `01_source_evidence_verification_final.json`: numeric reconciliation and evidence-access checks.
- `01_phase_status_final.json`: Phase 1 closure and scope limits.
- `OrionDesk_AI_Detailed_Design_Specification.pdf`: exact PDF evidence locator target.

**Phase 1 is closed. Phase 2 has not started. No ZIP/TAR archives or accuracy metrics were produced.**
