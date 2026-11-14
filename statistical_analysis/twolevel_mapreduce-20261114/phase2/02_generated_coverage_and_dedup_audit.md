# Phase 2 — Generated Corpus Extraction and Raw Semantic Deduplication

**Protocol:** 6.1
**Status:** PHASE_COMPLETED_BEST_EFFORT
**Evaluation method:** One unlabeled eight-file set (no fullload/onelevel/twolevel label assumed).

## Input inspection

| Actual scored input | Physical lines | Nonempty lines | Inspected table cells | Eligible occurrences | Excluded units |
|---|---:|---:|---:|---:|---:|
| 01_screen_functions(8).md | 437 | 325 | 608 | 303 | 536 |
| 02_api(8).md | 482 | 366 | 726 | 584 | 481 |
| 03_data(8).md | 411 | 308 | 563 | 417 | 493 |
| 04_batch_functions(10).md | 274 | 204 | 323 | 273 | 302 |
| 05_business_rules(7).md | 391 | 301 | 468 | 235 | 459 |
| 06_exception_handling(9).md | 346 | 260 | 367 | 297 | 328 |
| 07_processing_flows(9).md | 369 | 280 | 395 | 320 | 445 |
| 08_architecture_decision(9).md | 216 | 175 | 640 | 11 | 618 |

## Raw occurrence and class integrity

- Eligible generated occurrences (GO): **2440**.
- Unique generated semantic classes (G): **2360**.
- Repeated classes: **64**.
- Duplicate-excess occurrences: **80**.
- Within-file excess: **1**; across-file excess: **79**.
- Repeated classes spanning multiple files: **63**.
- Input physical lines covered: **2926**; table cells audited (including headers): **4090**.
- Recorded noneligible units: **3662**.
- Similar but unmerged pairs requiring a full-predicate review: **223**.
- Manually reviewed source-quotation equivalence pairs incorporated into raw classes: **28**.
- Exact retrieval-index key entries: **542**.
- Every eligible occurrence has one class, and every exact quote was checked against its physical input line.
- Every eligible table occurrence retains the full table row key and column-heading context.

## Extraction and exclusion policy

Adopted definitive statements, conditional obligations, exact API/status commitments, data declarations, error/recovery rules, authorization restrictions and separately asserted acceptance tests were eligible. Unresolved, unadopted and illustrative material did not become predictions. Plain identifiers, document references, example fixture values and table cross-links were context or excluded units, unless an independent affirmative rule was explicit. Some complete predicates were kept together when splitting risked changing their force.

## Evidence files

- `02_generated_atoms_final.jsonl`: all eligible occurrence records, exact line/cell locators and canonical keys.
- `02_generated_classes_final.jsonl`: exactly one semantic class per occurrence, representatives and class membership.
- `04_duplicate_classes_final.jsonl`: repeated classes with evidence and within/across-file assignments.
- `02_line_cell_coverage_final.jsonl`: inspection/disposition for all physical lines.
- `02_table_cell_coverage_final.jsonl`: inspection/disposition for every parsed table cell.
- `02_generated_exclusions_final.jsonl` and `09_excluded_units.jsonl`: noneligible units with reasons.
- `02_retrieval_index_final.jsonl`: index of exact API/error/field/entity/test/trace keys and original locators.
- `02_semantic_merge_review_candidates.jsonl`: unresolved high-similarity candidate pairs, not counted as duplicates.
- `02_manually_reviewed_merge_decisions.jsonl`: individually examined confirmed paraphrase joins with actual quotations.
- `02_phase_status.json`: machine-readable inventory and structural checks.

## Limitations and next-phase boundary

- All eight submitted Markdown files were available and every physical line and parsed table cell was inspected using deterministic preprocessing; no semantic entailment versus the PDF was attempted in Phase 2.
- A bounded heuristic identified definitive assertions and excluded explicit TBD, Needs confirmation, Proposal, unadopted options, source-only citations and illustrative code/diagrams. Some dense mixed cells and multi-predicate sentences may be under- or over-atomized.
- Within-method raw semantic classes use normalized exact text plus conservatively high similarity with operation, status, error, field and test scope guards. Meaning-equivalent paraphrases that differ substantially in wording can remain separate classes; strong lexical similarity is not logical equivalence certification. Potential high-similarity unmerged pairs are recorded as review candidates without automatically changing counts.
- Architecture decision register AD-001 to AD-060 are unresolved and intentionally excluded as new commitments; explicit RES resolutions and definitive shared boundaries are eligible when separately stated.
- Each occurrence preserves actual file, physical line, exact quotation, and for tables row/column/header/key context. Source PDF-positive R and negative N ledgers remain unchanged.
- No TP/TN/FP/FN, source coverage or precision/recall/F1 metrics were produced. Deduplication will receive a distinct substantive review in the protocol-designated Phase 5.

**Phase 2 is closed.** No PDF-to-generated semantic entailment or confusion-matrix analysis was performed here.
