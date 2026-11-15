# Phase 2 — Generated-Corpus Occurrences and Raw Semantic Classes

**Protocol:** OrionDesk One-Pass Atomic Evaluation Protocol v6.1  
**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Method:** supplied_eight_file_set; a single complete, unprefixed eight-file Markdown set.  
**Scope:** Phase 2 only. Original scored inputs were read without modification. The PDF-positive and fixed-negative inventories remain unchanged.

## Input coverage and extraction

| Actual scored input | Physical lines | Extracted occurrences | Excluded units |
|---|---:|---:|---:|
| `01_screen_functions(7).md` | 437 | 451 | 423 |
| `02_api(7).md` | 482 | 622 | 481 |
| `03_data(9).md` | 411 | 554 | 358 |
| `04_batch_functions(20261115-043829).md` | 274 | 434 | 246 |
| `05_business_rules(9).md` | 391 | 369 | 340 |
| `06_exception_handling(20261115-043822).md` | 346 | 293 | 300 |
| `07_processing_flows(20261115-043821).md` | 369 | 382 | 355 |
| `08_architecture_decision(10).md` | 216 | 11 | 205 |

All 2,926 physical Markdown lines have individual coverage records, including every table row and cell through the `table_cell` evidence fields. Physical line numbers are 1-based. Source quotes and original filenames are retained verbatim in the line and occurrence evidence. The complete table-row context is retained as `row_quote_en`, `row_key`, `column_index`, and `header`. A concise normalized requirement sentence is supplied separately.

## Raw generated occurrence/class partition

| Measure | Count |
|---|---:|
| Eligible generated occurrences `GO` | 3,116 |
| Unique within-method raw semantic classes `G` | 3,020 |
| Excess occurrences `GO − G` | 96 |
| Within-file excess | 1 |
| Across-file excess | 95 |
| Repeated semantic classes (2+ occurrences) | 72 |
| Repeated classes spanning multiple files | 72 |

**Structural checks:** Every eligible occurrence is assigned to exactly one raw semantic class. Every class has at least one eligible occurrence. `GO - G = within_file_excess + across_file_excess` was verified. This arithmetic is not proof of perfect semantic deduplication.

## Eligibility boundary

Definitive positive and negative implementation/design assertions are eligible, including inherited API method/path/scope/result, field declarations, guarded workflow behavior and explicit prohibitions. Table cells are read with their row key and column header, rather than as free-standing tokens. Source-register cells with explicit `Needs confirmation`, `TBD`, unselected alternatives, open questions, unresolved architecture decisions, illustrative values, diagram markup, citation-only lines, and bare reference IDs are excluded from positive predictions. The unresolved status of an entire section does not authorize choosing a missing production contract. Clear, separable confirmed subclaims are retained where safely identifiable.

### Important limitations

- **Atomicity:** Some sentences express more than one conjunctive obligation. Clause splitting is selective to avoid destroying preconditions or scope. Fields explicitly enumerated as physical names are separated in data inventory tables.
- **Context:** The `08_architecture_decision` input is scored, but unresolved rows are not adopted decisions; its resolved assertions may repeat earlier files and are retained only if substantive. Architecture commentary is not counted as an independently adopted configuration.
- **Deduplication:** Exact contextual proposition grouping and very strict near-equivalence merges were applied. Distinct paths, numbers, actors, conditions and polarity are kept separate. Some true synonyms may remain split; nonidentical propositions are not merged merely for topical similarity. A full independent human semantic audit is not claimed.
- **Reversibility:** For every candidate the full source line/row and its original location are preserved; coverage and exclusion ledgers allow line- and table-cell review. Lookup keys support the mandatory bidirectional Phase 3 searches.
- **Metrics:** `TP`, `FN`, `FP`, `TN`, Precision, Recall and F1 have not been calculated. The final duplicate rate and semantic corrections are reserved for the designated Phase 5. The counts above are raw ledger structure, not a verified coverage score.

## Deliverables

- `02_generated_atoms_final.jsonl` — eligible generated occurrences with original-file evidence.
- `02_generated_classes_final.jsonl` — raw semantic classes, occurrence membership and canonical lookup keys.
- `04_duplicate_classes_final.jsonl` — repeated and singleton classes with exact excess partitions and rationale.
- `02_generated_exclusions_final.jsonl` — noneligible or nondefinitive input fragments with reasons.
- `02_generated_line_coverage.jsonl` — line-by-line source-inspection evidence including table row/cell extraction.
- `02_verified_semantic_merges.jsonl` — reviewer-inspected equivalence joins with original class texts and explicit rationale.
- `02_generated_corpus_coverage.json` — input hashes, structural counts, checks, limitations and status.
- `02_generated_lookup_index.jsonl` — inverted structural identifiers, paths, fields, tests, and source locations for reciprocal search.
- `02_semantic_dedup_review_candidates.jsonl` — unmerged, evidence-linked close paraphrases for later semantic re-adjudication.
- `02_phase2_report.md` — this phase report.

340 unique reciprocal lookup keys were indexed and 589 distinct unmerged similarity candidates retained for subsequent review. Similarity candidates are not counted as duplicates without full-predicate equivalence. An independent structural inspection of original paths, physical line/table locators, membership and line coverage passed with zero structural errors.

No archive is created. No Phase 3 generated-vs-PDF coverage judgments were performed.
