# Phase 2 — Generated Corpus Inventory and Raw Semantic Classes

**Protocol:** v6.1  
**Status:** PHASE_COMPLETED_BEST_EFFORT  
**Selected input set:** provided_eight_documents (one complete unlabeled eight-document set)

## Scope and provenance

- The exact Phase 1 PDF-positive inventory of **1,024** atoms and **37** negative controls is reused unchanged. Neither inventory was generated from the Markdown documents.
- All eight scored Markdown files were read in their entirety, including table rows and individual substantive cells. The original file basenames, physical line positions, table headers and row keys are recorded.
- Source PDF match grades, generated validity, FP/FN dispositions and the canonical binary decision universe remain outside this phase.

## Extraction and raw class counts

| Eligible generated occurrences (GO) | 2,523 |
| Raw semantic classes (G) | 2,475 |
| Raw duplicate excess occurrences | 48 |
| Diagnostic raw-duplicate proportion | 1.90% |
| Repeated raw classes | 40 |
| Raw classes observed in multiple input files | 37 |
| Within-file excess occurrences | 4 |
| Across-file excess occurrences | 44 |
| Generated exclusions and context annotations | 5,911 |

The duplicate proportion above is **a Phase 2 diagnostic of conservative context-preserving deduplication plus a constrained high-similarity pass, not the final semantically audited Duplicate metric**. Phase 5 will challenge paraphrase equivalences and invalid merges. The raw class count is distinct from the effective canonical predicted-positive count.

## Per-file evidence coverage

| Actual input file | Physical lines | Nonempty lines | Table cells checked | Extracted occurrences | Unclassified lines |
|---|---:|---:|---:|---:|---:|
| `01_screen_functions(6).md` | 495 | 382 | 660 | 310 | 0 |
| `02_api(6).md` | 696 | 558 | 1133 | 517 | 0 |
| `03_data(6).md` | 474 | 371 | 715 | 296 | 0 |
| `04_batch_functions(6).md` | 588 | 423 | 367 | 340 | 0 |
| `05_business_rules(6).md` | 481 | 383 | 686 | 371 | 0 |
| `06_exception_handling(7).md` | 432 | 336 | 495 | 339 | 0 |
| `07_processing_flows(7).md` | 565 | 442 | 390 | 335 | 0 |
| `08_architecture_decision(6).md` | 225 | 185 | 60 | 15 | 0 |

**High-confidence similarity merges:** 24 class-pair merges; **retained candidate comparisons:** 95. The separate candidate ledger preserves both statements and their evidence for the later Phase 5 audit.

## Evidence and exclusion handling

Every eligible occurrence includes an unchanged input filename, physical line, original quotation and an inherited section or table heading/row context. Each eligible occurrence maps to exactly one raw class; class representatives point to the actual input.
Unresolved (`TBD`, `Needs confirmation`), unadopted `Proposal`, noncommittal questions, evidence citations, code examples and Mermaid diagrams were excluded as independent positive predictions. The source-only exclusions from Phase 1 remain present in `09_excluded_units.jsonl`.

### Caveats that prevent semantic certification

The extraction and duplicate classification are conservative and normalized-exact with a narrowly constrained high-similarity merge pass. It is possible for a long cell to contain multiple independent predicates not perfectly separated or for equivalent paraphrases to remain in separate classes. These are acknowledged Phase 5 audit candidates and do not justify claiming exhaustive semantic equivalence now.
Architecture decision register unresolved rows are not promoted to implementation commitments. The narrow `RES-*` resolutions are eligible where they state actual definitive commitments.

### Deliverables

- `02_generated_atoms_final.jsonl` — original statement and real line/cell locator per eligible occurrence.
- `02_generated_classes_final.jsonl` — one raw class per exact normalized full-predicate context, with membership.
- `04_duplicate_classes_final.jsonl` — representative plus repeated occurrence and within/across partition.
- `02_generated_line_coverage_final.jsonl` — exhaustive line/cell coverage by file.
- `02_generated_exclusions_final.jsonl` — generated-side excluded text and reasons.
- `02_retrieval_index_final.jsonl` — identifier/API/field/event lookup index to support reciprocal searches in Phase 3.
- `02_semantic_duplicate_review_candidates_final.jsonl` — candidate paraphrases, evidence and bounded merge decisions.
- `09_excluded_units.jsonl` — carried Phase 1 source exclusions plus Phase 2 generated exclusions.
- `02_phase_status_final.json` — machine-readable counts, checks and limitations.

## Phase boundary

**Phase 2 is closed. Phase 3 has not started.** No TP, TN, FP, FN, Precision, Recall or F1 was computed.
