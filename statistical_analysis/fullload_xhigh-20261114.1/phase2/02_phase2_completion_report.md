# OrionDesk AI — Phase 2 Completion Report

**Protocol:** Six-Turn Semantic-Entailment Atomic Requirement Evaluation, version 6.1  
**Phase:** 2 — Entire Generated Corpus and Raw Deduplication  
**Status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Language:** English for all authored deliverables.  
**Scored method:** One complete eight-file supplied set; no method-comparison label was inferred from filename copy suffixes.

## Input scope and source freeze

All eight supplied Markdown files were read in their entirety. Each substantive table row and cell was visited with row-key and table-column context. The two user-supplied Phase 1 inventories remain unchanged: **1024 PDF-positive atoms** and **37 PDF-negative controls**. This phase did not draw new PDF requirements from the Markdown or use Phase 1 JSONL as a generated document.

## Extracted claims and duplicate classes

| Check | Count |
|---|---:|
| Physical Markdown lines inspected | 8,330 |
| Table rows inspected (including headers/separators) | 3,849 |
| Table cells visited | 15,945 |
| Eligible definitive generated occurrences (`GO_m`) | 3,909 |
| Raw within-method semantic classes (`G_m`) | 3,818 |
| Duplicate excess occurrences | 91 |
| Repeated claim classes (two or more occurrences) | 69 |
| Repeated classes found across files | 65 |
| Within-file duplicate excess | 8 |
| Across-file duplicate excess | 83 |
| Excluded generated nondefinitive/illustrative units | 1,763 |
| Independently retained PDF exclusions | 6 |

These are Phase 2 structural/lexical-semantic counts, **not** coverage or correctness scores. The later Phase 5 duplicate review may change equivalence classes. Parent rows and headings are used as context, not a second scored occurrence solely because they summarize separately extracted child facts.

## Item-level evidence

Every eligible occurrence includes its actual unchanged Markdown filename, physical line, original exact cell or prose quote, heading scope, reconstructed row context, normalized assertion, and one raw semantic class. For table cells, `table_cell.column_index` is **one-based** and `table_cell.column_header_en` captures the source header. Each occurrence has method/path, identifier, literal, and common-field lookup keys for reciprocal retrieval in Phase 3. Repeated classes list their representative evidence, ordered members, and within-/across-file excess partition.

## Per-file inspection

| Actual scored input | Physical lines | Table rows | Table cells | Eligible occurrences |
|---|---:|---:|---:|---:|
| `01_screen_functions(1).md` | 864 | 467 | 2,585 | 582 |
| `02_api(1).md` | 1,201 | 590 | 2,892 | 661 |
| `03_data(1).md` | 1,034 | 607 | 2,757 | 529 |
| `04_batch_functions(1).md` | 1,323 | 532 | 1,617 | 463 |
| `05_business_rules(2).md` | 1,442 | 533 | 1,661 | 549 |
| `06_exception_handling(3).md` | 737 | 404 | 1,551 | 460 |
| `07_processing_flows(2).md` | 1,143 | 302 | 1,283 | 541 |
| `08_architecture_decision(2).md` | 586 | 414 | 1,599 | 124 |

## Explicit semantic-equivalence challenge

A word/bigram reciprocal candidate search over all 3,818 distinct classes generated 131 close candidates. Each candidate retains both original quotes and unchanged physical Markdown line references in `02_potential_duplicate_review.jsonl`. Of these, the 76 highest-ranked candidates were inspected, and 54 were judged equivalent under their actor/target/condition/exception/outcome context. The 55 lower-ranked candidates were not individually adjudicated, and the other examined nonmatches were conservatively retained as separate classes. The decisions are individually recorded in `02_manual_semantic_equivalence_decisions.jsonl`.

**Caution:** The sample is not a complete pairwise semantic equivalence certification. Several sentences still contain more than one independently testable predicate. Phase 5 explicitly audits and corrects these issues; the numerical duplicate summary is diagnostic, not a final verified rate.

## Eligibility and semantic treatment

- Definitive claims from confirmed contracts, field definitions, processing steps, decision tables, guards, file/data constraints, and operative prose were recorded.
- Standalone `TBD`, `Needs confirmation`, `NC`, open questions, unadopted `Proposal` rows and simple status/citation cells were not converted to affirmative implementation predictions. A definitive separable subclaim in a partly unresolved cell can still be eligible.
- The architecture-decision register is a scored eighth input, but its 110-plus open subjects do not become approved design commitments; only its independently definitive requirements remain eligible.
- Tables preserve the physical row and column context. A short `201`, `NOT NULL`, `Owner`, or `UUID` is interpreted together with the owning endpoint/table/field where a definitive assertion exists; absence of required context is excluded.
- The reference DDL was parsed as a source-supported SQL reference, not described as a complete production migration. Mermaid figures and sample JSON/HTTP envelopes were recorded as illustrative code where the same obligation is expressed elsewhere as a definitive requirement.

## Limitations and phase boundary

This is a documented best-effort extraction and **conservative** claim-equivalence classification. The script does not prove that every multi-clause Markdown sentence has been split at the smallest semantically independent testable boundary, nor can it certify every synonym/paraphrase pair. Some mixed confirmed/open sentences may need refinement during generated-claim validity and Phase 5 audits; these are **semantic quality limitations**, not unreadable-input blockers. The duplicated-claim count is provisional; no raw-class-to-source matching or TP/TN/FP/FN judgment is claimed here.

The phase is closed. Phase 3 has **not** been initiated.

## Individual deliverables

- `02_generated_atoms_final.jsonl`
- `02_generated_classes_final.jsonl`
- `04_duplicate_classes_final.jsonl`
- `09_excluded_units.jsonl`
- `02_generated_line_cell_coverage.jsonl`
- `02_reciprocal_lookup_index.jsonl`
- `02_potential_duplicate_review.jsonl`
- `02_manual_semantic_equivalence_decisions.jsonl`
- `02_phase2_validation_summary.json`
- `02_phase2_completion_report.md`

