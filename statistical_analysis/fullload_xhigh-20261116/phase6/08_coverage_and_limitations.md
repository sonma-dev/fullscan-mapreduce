# OrionDesk v6.1 — Coverage, Provenance, Reliability and Limitations

**Evaluation status:** `FINAL_BEST_EFFORT`. **Semantic completeness certification:** `NOT_CERTIFIED`.

## Input availability and inspected scope

The 90-page original fictional English *OrionDesk AI Detailed Application Design Specification* (R1.0/revision 1.3) was present and readable; all physical pages have a retained inspection record in `01_pdf_page_coverage.json`. Pages with diagrams, tables, figures and appendices were included in the source extraction. The PDF alone defines normative source-positive and source-negative propositions; generated Markdown and prior ledgers did not add source normative requirements.

All eight scored Markdown originals were present, with source names preserved:

| Scored original | Physical lines |
|---|---:|
| `01_screen_functions(1).md` | 864 |
| `02_api(1).md` | 1,201 |
| `03_data(1).md` | 1,034 |
| `04_batch_functions(1).md` | 1,323 |
| `05_business_rules(1).md` | 1,442 |
| `06_exception_handling(3).md` | 737 |
| `07_processing_flows(2).md` | 1,143 |
| `08_architecture_decision(2).md` | 586 |

Total physical lines: **8,330**. Retained row/cell inspection units: **19,636**. Generation status `Proposal`, `TBD`, `Needs confirmation`, and unapproved options were excluded where nondefinitive. A separable confirmed subclaim in a mixed row can remain eligible; unresolved details do not become implemented commitments. See `09_excluded_units.jsonl` and `02_line_cell_coverage_final.jsonl`.

## Evidence inventory and PDF provenance

Final PDF-positive atoms: **1,014**. Source-negative counterfactual controls: **37**. Source quotations checked against the actual PDF text by page: **1014** located, including 103 requiring punctuation/line-wrap or drawing-text normalization. This is provenance verification, not certification that each source clause was split at the correct logical granularity. `05_source_atomization_audit_final.jsonl` retains the source-level review; 10 source atoms were removed as redundant/nonnormative during Phase 5.

The source-negative controls derive only from explicitly prohibited, excluded or deferred source capabilities. TN=37 counts those 37 **bounded diagnostic controls**, not a hypothetical population of all absent features. Additional unasserted negative controls would inflate TN without affecting Precision/Recall/F1.

## Canonical labels and algebra

| Quantity | Count |
|---|---:|
| `R` | 1014 |
| `N` | 37 |
| `A` (fully evidenced generated source coverage, provisionally) | 456 |
| `B` (negative-control assertions found) | 0 |
| `F` (distinct generated-only unsupported propositions established) | 0 |
| `U = R ∪ N ∪ F` | 1051 |
| TP / FN | 456 / 558 |
| TN / FP | 37 / 0 |
| Precision / Recall / F1 | 100.0000% / 44.9704% / 62.0408% |

The raw generated classes **5,889** and raw eligible occurrences **5,956** are a different count from effective canonical predicted-positive propositions **456**. A supported universal rule may entail several genuinely independent PDF atoms, without creating synthetic generated occurrences. Conversely, merely mentioning a related identifier does not establish a full TP.

## FN root causes, bilateral search and corrective delta

Each of 558 remaining FN has a recorded source quote, actual generated candidate evidence, an E1/E0 predicate gap and a final root-cause disposition: **353 `PARTIAL_ENTAILMENT`**, **140 `CONSERVATIVE_UNRESOLVED`**, and **65 `TRUE_MISSING`**. `TRUE_MISSING` remains a best-effort determination rather than an independently certified exhaustive absence. In addition, 220 originally uncovered candidate rows are now documented as `MATCHER_FALSE_NEGATIVE_CORRECTED` across the earlier phases and Phase 6.

Seven explicit contextual matches were corrected in Phase 6, covering the case-title datum, workspace retention-class setting, WCAG 2.2 AA controls, the `UNIQUE (tenant_id, id)` case constraint, changed-fingerprint idempotency conflict, workspace-timezone business-calendar deadlines, and parallel search-index alias-swapping safeguards. The corrected records contain actual original-file quotations and proof links. The source denominator was unchanged in Phase 6. The change ledger also reconciles 148 formerly stale TP disposition fields.

An additional literal-token index searched the complete eight-file corpus and reverse-targeted the source inventory for all 558 remaining FN. It retained tested terms, real generated occurrence candidates and reverse source candidates in `06_reciprocal_regression_probes.jsonl`. Only lexical/search linkage is established; it must not be confused with independent semantic entailment. 16 final FN retain no positive source-link rank in the indexed reverse evidence. A particular retrieval hit may still fail on actor, action, condition, scope, exception, timing or outcome, and some coverage may remain missed.

## TP predicate review and raw-class uncertainty

All **456** current TP rows have a `05_tp_evidence_audit_final.jsonl` predicate map and actual source/generated locators. **28** are direct E3 matches; **428** are E2 equivalence, inherited-context, universal-instantiation, or conjunctive proof bridges. The audit is a best-effort documented predicate check, **not** independent exhaustive human entailment certification. Errors in shared-rule class membership and overlooked exceptions could create false TPs.

All **5,889** generated-class validity judgments are not independently certified. In particular, **3,973** have especially weak PDF retrieval/support confidence; **4,896** remain tagged `SUPPORTED_NONCOVERING` as provisional labels rather than defensible confirmed validity conclusions. The absence of a *proven* distinct `F` proposition in this pass does **not** establish the absence of unsupported generated commitments. Consequently calculated **FP=0** and **Precision=100.0000%** are not credible estimates of complete generated-specification correctness without further item-level semantic validation.

## Duplicate metrics and residual risk

Raw duplication is **1.1249%** = 67 excess of 5,956 eligible occurrences over 5,889 classes, partitioned as 7 within-file and 60 across-file excess; 57 repeated classes, 50 spanning files. Conservative class merging may undercount synonymous duplicates. Source atomization (including repeated chapter boilerplate, test-matrix overlap, and parent/child obligations) can still distort Recall. Neither provisional Recall nor its change since Phase 4 is a certified measurement of genuinely missing requirements. It is not a statistical lower bound; either numerator or denominator can be corrected.

## Structural checks and rerun instructions

`compute_metrics.py` reloads final JSONL ledgers and asserts unique IDs, full canonical U coverage, source/class/occurrence membership, actual/predicted polarity, source-versus-prediction equations, TP audit/E2 bridge presence, FN root-cause status, original generated line existence, PDF page inspection, all eight files, duplicate partitions and arithmetic reconciliation. It does **not** infer semantic correctness from exact strings, arithmetic, E2 labels or high similarity. Run `python compute_metrics.py --root . --write` to regenerate the machine report and `06_phase6_validation.json` from the item-level files.

Result: **structural reconciliation PASS; independent semantic certification NOT ACHIEVED; run closed as `FINAL_BEST_EFFORT`.**
