# Coverage, Semantic Evidence Quality, and Limitations

## 1. Final status and original sources

**Final evaluation status:** `FINAL_BEST_EFFORT`. All six designated phases have been closed. The Phase-6 recomputation passes the item-level structural assertions with **0** errors. Meaning-based verification has not reached certification quality; the confusion matrix must be read as provisional.

The only positive normative baseline is the supplied fictional English `OrionDesk_AI_Detailed_Design_Specification(8).pdf`, whose 90 physical pages were available and included in the physical-page coverage ledger. Figures and source tables remain relevant to the source interpretation. The scored generated corpus contains exactly the eight unmodified Markdown files:

1. `01_screen_functions(8).md`
2. `02_api(8).md`
3. `03_data(8).md`
4. `04_batch_functions(10).md`
5. `05_business_rules(7).md`
6. `06_exception_handling(9).md`
7. `07_processing_flows(9).md`
8. `08_architecture_decision(9).md`

The inspected physical-line coverage is **2926** and the table-cell ledger contains **4090** cells, including table headings. Open questions, `TBD`, and unadopted proposals are not definitive scoring commitments. Figure illustrations, nonoperative source metadata, and duplicate parent summaries are excluded where recorded in `09_excluded_units.jsonl`. Input bytes and filenames were not modified.

## 2. Shared source atomization and negative controls

The original PDF inventory had **1024** atom records. The source atomization audit removed **11** non-independent or nonnormative items, leaving **1013** common positive atoms. Exclusions included architecture-summary duplicates and illustrative error-envelope fields on physical PDF page 84. Appendix E test-execution obligations were not automatically conflated with implementation obligations. Retained source IDs and all removed-ID decisions are visible in the item-level atomization audit and change delta; there has been no method-dependent denominator substitution.

The **37** fixed PDF-grounded negative controls are affirmative prohibited/deferred/excluded counterfactuals. None was asserted by the eligible generated corpus in the current binary ledger. Therefore TN=37 on **this limited diagnostic set only**. An infinite or population-wide set of absent requirements was not sampled.

PDF evidence locator validation found **2513 / 2516** source-atom citation fragments directly recoverable in page text extraction. The remaining fragments are diagram-related and cannot be deemed false merely because ordinary text extraction omits visual text. These checks validate locators, not full modal or logical force.

## 3. Source coverage, TP audit and reverse FN challenge

The final source-positive scoring is TP=990, FN=23. Among the final TP, the source-corpus modes include E2 contextual, universal, conjunctive and semantic-equivalence bridges, along with direct E3 claims. Universal instantiation is allowed to cover several independently retained source atoms with a single raw generated class only if all actor, scope, timing, exception and outcome predicates hold. This is **not** a multiplier of generated occurrences.

A source-first automatic retrieval stage nominated **928** provisional FNs. The reconciled FN audit contains **894** records marked `MATCHER_FALSE_NEGATIVE_CORRECTED`, **11** `SOURCE_ATOMIZATION_ERROR_CORRECTED`, and **23** final FNs, classified as follows:

| Final FN root cause | Count | Interpretation |
|---|---:|---|
| `TRUE_MISSING` | 6 | No complete eligible source-target commitment found after the recorded bounded challenge |
| `PARTIAL_ENTAILMENT` | 7 | Related generated text lacks an identified required predicate |
| `CONSERVATIVE_UNRESOLVED` | 10 | Ambiguity remains; a negative score does not prove verified absence |

Phase 5 corrected one remaining explicit source-to-generated FN (`PDF-00762`) to TP. During Phase 6, an obsolete **unproven predicate map** for that existing TP was reconciled against the original PDF page 84 and generated source lines; its TP score did not change. Additionally, **17** final FN records had empty exact/alias-search-key histories. Full-corpus source-specific term searches were executed for all **23** final FNs across all eight original Markdown files and saved in `06_fn_full_corpus_search_final.jsonl`; the 17 empty records were repaired. No explicit full-predicate match was thereby proven and no FN score was silently promoted. The final root-cause ledgers now have nonempty reciprocal keys, actual source/candidate references and a specific unmet predicate.

There are **990** final TP records with physical source/generation references and item-level predicate maps, and one additional removed/merged prior-TP audit row. **Only 1 final TP proof is individually flagged as independently fully semantically certified** after a direct source/document audit. All other TP rows have line checks and review metadata but not an independent proof of complete logical implication. This limits the interpretation of a calculated Recall of 97.73% in either direction; it is not a certified lower bound or the proven fraction of requirements truly implemented.

## 4. Generated correctness and FP uncertainty

The raw definitive generated inventory contains **2400** eligible occurrences and **2289** unique within-method semantic classes. The generated validity ledger labels **877** classes `PDF_ENTAILED` and **1412** `SUPPORTED_NONCOVERING`. The supporting PDF quotations/context do **not** amount to independent full-predicate support certification for those classes. In particular, `SUPPORTED_NONCOVERING` may be an optimistic temporary classification when only topical overlap is evidenced. Do not use that classification to certify that a generated claim is valid.

Phase 5 separately recorded **185** generated-class candidate-quote fragment reconciliation exceptions under its own heuristic. Phase 6's more permissive independent PDF-page text-fragment diagnostic found **15** classes whose cited source quotation was not literally recoverable in ordinary PDF page-text extraction (all retained as review exceptions, not automatic invalidity). The two diagnostics use different methods and should not be compared as a corrected semantic error count. Visual figure interpretation, incomplete context, and unproven entailment remain relevant.

The computed **FP=0** is the number of currently identified and scored unsupported generated-only propositions plus asserted fixed negative controls, **not an affirmative finding that no unsupported generated proposition exists**. Consequently `Precision=100.00%` and F1=98.85% are arithmetic over currently adjudicated rows, not independently verified model correctness. The coverage projections and generated-class validity records are logically different directions of assessment.

## 5. Duplication, regression probes and arithmetic

The raw excess of **111** is partitioned into **1** within-file and **110** across-file occurrences. The rate is 4.625%, derived from raw classes rather than coverage bridges. Similar cases with differing tenant, actor, endpoint, error, status, retries or constraints were not merged without complete predicate equivalence.

Source-and-generated retrieval regression probes included case title, workspace retention class, same-key case-creation response, event envelope schema version, and reviewed artifact hash. The source atoms reached by these probes were TP, and the automated strict method/path check did not find an explicit high-risk FN collision. A term hit alone does not prove semantic entailment. The full-corpus FN search log is available for manual inspection. No performance or accuracy claims of the fictional application can be inferred from this benchmark.

Every canonical row was verified for a single 0/1 actual/predicted label and TP/TN/FP/FN cell. For the final counts:

```text
TP + FN = 990 + 23 = 1013 = |R|
TN + |B| = 37 + 0 = 37 = |N|
FP = |F| + |B| = 0 + 0 = 0
|U| = |R| + |N| + |F| = 1013 + 37 + 0 = 1050
|P| = TP + FP = 990
GO - G = 2400 - 2289 = 111
Within + Across = 1 + 110 = 111
```

`TP + FP` is **not** asserted equal to `|G|`. The scoring universe is a projected canonical proposition set, not raw extracted sentence count. The arithmetic and referential checks passed but are not a natural-language entailment proof.

## 6. Limits, reproducibility and completion classification

- No numerical uncertainty interval is invented. Unsupported generated-class correctness, over-broad TP bridges, missing source predicates, visual PDF layout, and atomization judgments can change the reported rates in either direction.
- Every source-positive atom is recorded, every final FN has root-cause review, and every final TP has an audit record, but full independent proof of meaning is not complete.
- No external content, historical score, earlier goldset or additional ninth Markdown file contributed new source-positive requirements.
- The single method has no method-to-method comparison; no `11_comparison_final.*` deliverable is required.
- Every final artifact is an individual English document or dataset. **No ZIP/TAR archive is created**, under protocol 6.1.

The reproducible source is `compute_metrics.py`, with a machine-readable proof/check report in `06_independent_checks.json`, actual source-file digests, item-level revisions in `07_change_delta.jsonl`, separate quote exceptions in `06_quote_recovery_exceptions_final.jsonl`, and specific regression findings in `06_regression_probes_final.jsonl`. These records support **`FINAL_BEST_EFFORT`**, not `FINAL_VERIFIED`.
