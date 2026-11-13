# Coverage, Evidence Quality, and Limitations

## Scope and authority

This is the final Phase-6 report for **one `fullload` method**, using the eight originally uploaded English Markdown specifications, the original English PDF of 90 physical pages, and the `OrionDesk_One_Pass_Atomic_Evaluation_Protocol` v6.1. All input filenames and record locators use their actual mounted names. The eight Markdown specifications are scored; the protocol document, prior goldsets, and historical scores are not scored source inputs. The PDF alone is authoritative for source-positive obligations and bounded negative counterfactuals.

The original PDF was re-opened, and all 90 pages had extractable text. The Phase-1 quote audit accounted for 1027 current scored source atoms; 1024 quotations matched independently extracted PDF page text verbatim after whitespace normalization. Three remaining PDF citations refer to visual/laid-out content reviewed in the earlier Phase-1 raster inspection; there are no missing PDF pages. This three-item distinction must not be mistaken for a complete visual semantic recertification in Phase 6.

All eight scored Markdown inputs were readable and hash-matched the Phase-1 manifest. The line-coverage ledger represents **8330 physical lines**, and the cell-coverage ledger contains **14882 table-cell records**. The checker verifies that generated TP quotations actually occur at their cited original file/line, including table-context locators; a matching string alone does not prove full semantic support.

## Final source and negative-control universes

- The corrected source-positive inventory contains **1027** individually scored PDF propositions. Phase 5 retired one non-independent overview atom and split two compound atoms into six more independently testable obligations (a net increase from 1,024 to 1,027). Old/new IDs are preserved in `05_source_atomization_audit_final.jsonl` and `07_change_delta.jsonl`.
- **37** controls were predeclared from explicit source exclusions, prohibitions and release deferrals. Their 37 TNs are only a bounded diagnostic collection: they are *not* all possible absent requirements and do not increase Precision/Recall/F1.
- **0** generated-only unsupported predictions and **0** asserted negative controls were confirmed in the current best-effort ledger. This produces FP=0 but is **not** independently complete generated-claim verification.
- Exactly **1064** distinct units have one actual label, one prediction, and one four-cell assignment. Six canonical-ID collisions between newly split source atoms and negative-control rows were fixed in Phase 6; the correction does not change source or negative-control content.

## TP evidence and FN reciprocal audit

- **576** final TP entries are represented one-to-one in `05_tp_evidence_audit_final.jsonl`, with source/page, generated/line/table, mode (E2/E3), and separate predicate fields. **662** generated evidence locations were directly validated against unchanged Markdown files. This is locator and bounded predicate validation, **not** exhaustive expert certification of logical entailment.
- The initial FN root ledger has 706 rows, comprising 252 previously corrected matcher false negatives, 3 corrected/retired source atomization items, and 451 final FN decisions. Its final FN dispositions reconcile to **396 `PARTIAL_ENTAILMENT`**, **55 `CONSERVATIVE_UNRESOLVED`**, and **0 `TRUE_MISSING`**.
- **55 additional explicit source-to-generated false negatives** were corrected in Phase 6. The original Phase-2 extractor had missed 20 definitive Markdown clauses; their actual input lines were restored without altering any scored Markdown input. Correction-by-correction proof is in `06_regression_corrections_final.jsonl` and the consolidated `07_change_delta.jsonl`.
- Diagnostic probes were executed for case title, workspace retention-class settings, replaying the same case-creation key, foreign-tenant non-disclosure, ACL, citations, and named event payloads. `06_regression_probes_final.jsonl` records their current TP/FN distributions. The exact normalized quote scanner reports **0 remaining full-quote-line FN exceptions**. This does not exclude other contextual false negatives.

## Generated claim validity, duplication and support risk

- There are **6080** eligible generated occurrences and **5991** provisional semantic classes. The raw excess is **89** (within-file 2; across-file 87), yielding **1.46%**. Structural partitions reconcile, but meaning-equivalence merging remains best effort.
- Of 5991 classes, **5093** still have `semantic_certification=NOT_VERIFIED` in their PDF-support audit. Historical labels such as `PDF_ENTAILED` for those classes signify a best-effort classification and **must not be represented as fully verified support**.
- There remain **22** source atoms in the corrected inventory using the pattern `... immutable derivative tracks SHA-256 source/revision provenance`. The original PDF's repeated boilerplate may have been over-atomized into component-specific instances. The source-denominator sensitivity is unresolved; the script does not silently merge or discard source requirements merely to improve scores.
- Sixteen source atoms explicitly mention `Test TST-*` scenarios, some of which may overlap substantive product obligations. Earlier source-atomization adjustments were applied, but exhaustive independent semantic deduplication of test scenarios is not claimed.
- The FP=0 / Precision=100% result is not proof that generated specifications contain no unsupported commitments. Some claims may be over-broad, unapproved, or wrongly treated as adopted; the residual source-support risk is material. The computed Recall=56.09% is likewise not certified completeness, and there is no justified statistical confidence interval or guaranteed upper/lower bound.

## Structural validity versus semantic certification

**Structural result: PASS, after Phase-6 repairs.** Input hashes, 90-page extent, line/cell coverage, ID noncollision, generated occurrence/class membership, one canonical four-cell universe, TP/FN evidence-ledger one-to-one relationships, duplicate partitions, and equations reconcile independently. In particular: TP+FN=1027; TN+asserted negative controls=37; FP=unsupported-only+asserted negatives=0; all four cells=1064; TP+FP=576, **not** 5991 raw classes.

**Semantic certification: NOT VERIFIED.** Thousands of generated claims and many TP E2 bridges still need deeper expert-level full-predicate corroboration; 55 final FNs remain conservative unresolved cases. Consequently, the run closes at `FINAL_BEST_EFFORT`, not `FINAL_VERIFIED`. This is an honest final deliverable, not a request to repeat an already completed phase.

## Exclusions, paths and delivery

`09_excluded_units.jsonl` retains nonnormative PDF illustrations and nondefinitive Markdown clauses from the extraction stages. `02_generated_line_coverage_final.jsonl` and `02_generated_table_cell_coverage_final.jsonl` provide line/cell-level coverage; `01_pdf_page_coverage_final.jsonl` and `01_pdf_quote_verification_final.jsonl` provide PDF inspection references. The scored inputs were not modified. All final outputs are individual files in `oriondesk_phase6`; **no ZIP/TAR archive** is created under the binding protocol. There is only one evaluated method, so cross-method comparison files are not applicable.
