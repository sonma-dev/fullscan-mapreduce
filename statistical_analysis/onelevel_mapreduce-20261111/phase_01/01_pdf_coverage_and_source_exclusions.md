# Phase 1 — PDF Source Inventory Reuse and Verification

**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** Version 6.0; only Phase 1 was executed.  
**Baseline:** OrionDesk AI `OD-AI-DDS-001`, `R1.0`, revision `1.3`.

## Reuse decision

The prior `fullload_cal` PDF-derived source-positive atomic ledger and fixed source-negative controls have been adopted **without any change to their atomic propositions, source IDs, English quotations, physical page numbers, or evidence records**. The source-positive and source-negative JSONL output files are **byte-for-byte identical** to those recovered prior ledgers.

The earlier baseline PDF `OrionDesk_AI_Detailed_Design_Specification.pdf` and the current uploaded PDF `OrionDesk_AI_Detailed_Design_Specification(1).pdf` are both available and binary-identical:

- SHA-256: `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3`
- Physical pages: **90 / 90**
- PDF-positive normative atoms (`R`): **1,024**
- PDF-negative bounded controls (`N`): **37**
- Excluded PDF text units in the original per-page coverage audit: **274**
- Previously recorded image-bearing PDF pages reviewed: **31**

The retained evidence locators name the unmodified canonical reference PDF (also available as an actual file), not an inferred filename for the new upload.

## Evidence validation performed in this turn

- All 90 physical pages are readable in the current PDF.
- **1,021** source-positive exact quotations agree with the current PDF's selectable text after whitespace normalization.
- **3** additional quotations (`PDF-00977`–`PDF-00979`) are visual figure assertions on physical page 8 and were checked against that figure directly.
- **37 / 37** fixed negative controls have their quoted PDF excerpts independently found on their cited physical pages.
- Reused source IDs and negative-control IDs are unique; the source and exclusion page counts reconcile to **1,024** and **274**, respectively.
- A contact-sheet visual review covered all **31** image-bearing pages listed in the recovered source coverage record.
- The source ledgers and page coverage ledger retain their source-filename and content bytes exactly.

## Input availability — scored files reserved for Phase 2

| Role | Actual unchanged filename | Mounted | Bytes |
|---|---|---|---:|
| `01` | `01_screen_functions(1).md` | Yes | 79519 |
| `02` | `02_api(1).md` | Yes | 68363 |
| `03` | `03_data(1).md` | Yes | 77230 |
| `04` | `04_batch_functions(1).md` | Yes | 54167 |
| `05` | `05_business_rules(1).md` | Yes | 59073 |
| `06` | `06_exception_handling(2).md` | Yes | 56525 |
| `07` | `07_processing_flows(2).md` | Yes | 59907 |
| `08` | `08_architecture_decision(1).md` | Yes | 53500 |

All eight scored Markdown files are mounted, but **they were not scored, atomized, altered, or used as PDF requirement evidence in this phase**.

## Reuse limitations

The reused source inventory was previously classified as best-effort, using conservative structural splitting. It is not certified as a freshly performed, manually exhaustive semantic atomization. This reuse preserves a single identical, PDF-grounded reference universe rather than secretly changing the denominator between methods.

The 274 excluded PDF text units are carried forward as per-page counts; `09_excluded_units.jsonl` gives page-level exclusion summaries, not 274 itemized exclusions. Illustrative UI numbers, fictional identifiers, image navigation examples, front matter, and unadopted configurations do not silently become normative source-positive atoms.

Reuse does **not** mean reusing historical goldset comparisons, generated-claim matches, TP, TN, FP, FN, Precision, Recall, F1, or duplication judgments. Such method-specific evaluation belongs in later phases under the current protocol.

## Delivered Phase 1 files

- `01_source_atoms_final.jsonl`: unchanged source-positive atoms and item-level PDF evidence.
- `01_source_negative_controls_final.jsonl`: unchanged fixed PDF-negative controls.
- `01_pdf_page_coverage_final.jsonl`: unchanged 90-page inspection and exclusion counts.
- `09_excluded_units.jsonl`: current page-level source exclusion summaries.
- `01_phase_status_final.json`: full current input mapping, binary PDF identity, verification and limitations.
- `01_pdf_coverage_and_source_exclusions.md`: this explanation.

**Phase gate:** Phase 1 is complete, with the bounded best-effort qualification noted above. No part of Phase 2 was performed.
