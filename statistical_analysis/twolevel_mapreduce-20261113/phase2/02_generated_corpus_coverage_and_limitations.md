# Phase 2 — Generated-Corpus Atomic Occurrences and Raw Semantic Classes

**Phase status:** `PHASE_COMPLETED_BEST_EFFORT`  
**Protocol:** 6.1  
**Evaluated set:** One supplied complete eight-file set (`supplied_set_1`); the original user-provided file names are preserved and no generation-method label is inferred.  
**Shared Phase 1 inventory:** 1024 PDF-positive atoms and 37 PDF-grounded negative controls, copied without modification. These were not read as sources of generated claims.

## Enumerated Phase 2 results

| Measure | Count |
|---|---:|
| Scored Markdown inputs inspected | 8 |
| Physical Markdown lines inspected | 2,926 |
| Nonempty Markdown table cells inspected | 3,769 |
| Eligible generated claim occurrences (`GO_m`) | 2,516 |
| Raw generated semantic classes (`G_m`) | 2,437 |
| Excess duplicate occurrences (`GO_m - G_m`) | 79 |
| Within-file excess | 1 |
| Across-file excess | 78 |
| Repeated raw classes | 68 |
| Classes spanning multiple files | 67 |
| Generated exclusions / nondefinitive fragments | 3,477 |
| Potential semantic-paraphrase candidate pairs not merged | 190 |

**Provisional raw duplicate rate:** 0.031399, computed solely as `(GO_m - G_m) / GO_m`. This provisional figure is **not** the Phase 5 audited duplication metric.

## Input coverage

| Original scored file | Lines | Table cells | Eligible occurrences | Excluded fragments |
|---|---:|---:|---:|---:|
| `01_screen_functions(8).md` | 437 | 549 | 393 | 391 |
| `02_api(8).md` | 482 | 674 | 404 | 527 |
| `03_data(8).md` | 411 | 520 | 405 | 497 |
| `04_batch_functions(8).md` | 274 | 300 | 331 | 367 |
| `05_business_rules(8).md` | 391 | 423 | 273 | 440 |
| `06_exception_handling(9).md` | 346 | 342 | 289 | 514 |
| `07_processing_flows(9).md` | 369 | 367 | 333 | 509 |
| `08_architecture_decision(8).md` | 216 | 594 | 88 | 232 |

## Evidence, eligibility, and semantic grouping method

1. Retain the unchanged eight scored inputs. Scan every physical line and nonempty Markdown table cell, preserving original file names, line numbers, table row keys, column headings, and source quotations.
2. Form one candidate per conservative sentence/semicolon segment. Preserve shared section and table context and exact field/endpoint/status markers. The original cell is kept alongside the extracted segment to support review of under-splitting and scope.
3. Exclude citations, bare IDs, links, examples without adopted force, unresolved/TBD questions, unadopted alternatives, and purely structural headings. Retain every exclusion with its location, reason and covered text.
4. Group exact normalized predicates and only highly similar surface equivalents, while guarding endpoint method/path, literal errors, numeric constraints, actor labels and prohibition polarity. Preserve every raw occurrence ID exactly once in the class ledger.
5. Retain a reverse lookup index for methods/paths, field names, IDs, status codes and lexical features. Possible paraphrases not safely mergeable by this bounded procedure are separately enumerated, not silently forced into equivalence.

## Structural validation

- Eight distinct scored roles were present and readable, with no replacement of any original Markdown content.
- Every physical line has one line-coverage record. Every nonempty Markdown table body cell has one cell-coverage record, including reference/context-only cells.
- Every eligible `GEN-*` has an existing source file, physical line and table-cell context if applicable; every `GEN-*` belongs to exactly one `GCLASS-*`.
- The class occurrence-count sum equals `|GO_m|` and the duplicate partition sums to `|GO_m| - |G_m|`.
- The Phase 1 PDF-positive and negative-control ledgers are retained unchanged; generated files are not used as authority to add PDF requirements.

## Limitations, not deferred work in this phase

This is a **best-effort** eligible-claim inventory, not a verified independent semantic annotation of every predicate. Long clauses may contain multiple obligations; a context-dependent cell may be only partially independent; close paraphrases may remain separate; unresolved prose may contain eligible subclaims requiring further scrutiny. These material uncertainties are not hidden by arithmetic or source citations. Protocol Phase 5 is the designated correction/audit phase. Phase 3 was not started.
