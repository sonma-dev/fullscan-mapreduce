# OrionDesk AI — Phase 1: PDF Source Requirements and Controls

**Protocol:** v6.1  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Scope:** Original source PDF only. Generated-corpus scoring has not begun.

## Identity and input coverage

- Uploaded authoritative PDF: `OrionDesk_AI_Detailed_Design_Specification(8).pdf`.
- Canonical evidence filename: `OrionDesk_AI_Detailed_Design_Specification.pdf` (byte-identical copy included with the deliverables).
- Document: `OD-AI-DDS-001`, release `R1.0`, design revision `1.3`.
- SHA-256: `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`.
- Physical source pages inspected: **90/90**; all pages contain readable extractable text.
- Embedded-image pages inspected: **31**, including the Figure 1.1 runtime assertions on physical page **8**.
- Scored Markdown inputs present and UTF-8 readable: **8/8**; eligible generated assertions are reserved for Phase 2.

## Common PDF-only inventories

| Inventory | Count | Provenance |
|---|---:|---|
| Source-positive atomic propositions (`R`) | 1,024 | Original `fullload_cal` ledger, copied unchanged and independently checked against this exact PDF |
| Source-negative controls (`N`) | 37 | Fixed PDF-grounded counterfactuals, copied unchanged and independently verified |
| Original PDF evidence locations | 2,564 | 2,561 normalized text matches and 3 independently inspected Figure 1.1 assertions |
| Unmatched PDF evidence quotations | 0 | Evidence verification enumerated in `01_pdf_quote_verification_final.jsonl` |
| Prior excluded text-block estimate | 274 | Page-level historical estimate, **not** item-by-item semantic certification |
| Atomization challenge records | 19 | 16 Appendix E test-overlap candidates; 3 grouped chapter boilerplate / verification / field-context challenges |

Source-positive IDs `PDF-00001`–`PDF-01024` and negative IDs `NEG-00001`–`NEG-00037` remain unchanged. All original English propositions, source quotations, page references, evidence types and fields are preserved byte-for-byte. Both inventories are common inputs to any supported method; neither Markdown-generated requirements nor historical scores determine the PDF denominator.

## Source atomization qualification

This phase preserves the user's requested common `fullload_cal` evidence universe while applying the protocol v6.1 source-access checks. **Matching a quotation does not certify that every retained proposition is independently meaningful.** The 19 recorded challenges include Appendix E acceptance-test overlap, repeated universal contract/verification language and inherited entity/table/DDL context. The 19 records are review groups, **not 19 confirmed incorrect source atoms**, and no unsupported denominator modification was silently applied.

The 274 historical excluded-text units are retained only as an aggregate page-estimate. `09_excluded_units.jsonl` contains current-source page-grouped exclusions plus explicitly grounded illustrative examples. It deliberately does not invent 274 item-level quotations. The original PDF excludes purely illustrative fixture values and example-only configuration from independently adopted implementation requirements. Figure 1.1's three actual cross-cutting runtime assertions remain positive source evidence rather than illustration-only exclusions.

## Phase closure and score interpretation

- This phase completed source inspection, PDF-positive / PDF-negative inventories, direct evidence verification, source identity checks and source-atomization risk recording.
- **No** generated occurrence/class extraction, TP/TN/FP/FN judgment, Precision, Recall, F1, Duplicate metric, or archive was produced.
- Phase 2 begins only on a subsequent user instruction. Source-atomization concerns remain explicitly visible for the designated correction phase; baseline stability does not imply semantic certification.

## Deliverable inventory

- `01_source_atoms_final.jsonl` — 1,024 preserved source-positive items with English PDF evidence.
- `01_source_negative_controls_final.jsonl` — 37 preserved bounded PDF-negative controls.
- `01_pdf_page_coverage_final.jsonl` — verified physical-page coverage and current extraction properties.
- `01_pdf_quote_verification_final.jsonl` — 2,564 verified evidence locators.
- `01_source_atomization_challenge_final.jsonl` — 19 real source-denominator review groups.
- `09_excluded_units.jsonl` — current PDF-only exclusion records and audit limitations.
- `01_source_evidence_verification_final.json` — independently recomputed evidence counts.
- `01_input_manifest_final.json` — exact attached file identity, hashes, roles and Phase 1 boundary.
- `01_phase_status_final.json` — explicit best-effort phase closure.
- `OrionDesk_AI_Detailed_Design_Specification.pdf` — identical canonical source evidence file.
- `verify_phase1.py` — English-only reproducibility script.
