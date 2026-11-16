# Final Coverage and Limitations - Phase 6

**Protocol:** OrionDesk Six-Turn Semantic-Entailment Atomic Requirement Evaluation Protocol v6.1  
**Method:** `supplied_unprefixed_set` (one complete, unprefixed eight-document method)  
**Completion:** `PHASE_COMPLETED_BEST_EFFORT`  
**Structural reconciliation:** `PASS`  
**Independent semantic certification:** `NOT_VERIFIED`

## 1. Authority, source material, and method isolation

The sole normative reference is the original, readable, 90-physical-page English PDF `OrionDesk_AI_Detailed_Design_Specification.pdf` (document `OD-AI-DDS-001`, release `R1.0`, design revision `1.3`). The two designated JSONL ledgers supplied by the user were the initial source-positive and source-negative inventories. The positive inventory was explicitly corrected in Phase 5 with retained IDs and recorded source evidence; the bounded negative inventory was kept unchanged.

Eight original scored Markdown files were present, readable and were not modified. Names are reproduced exactly, including supplied copy suffixes:

| Actual scored Markdown filename | Physical lines inspected | Table cells tracked |
|---|---:|---:|
| `01_screen_functions.md` | 709 | 2,293 |
| `02_api.md` | 1,286 | 3,032 |
| `03_data.md` | 1,051 | 3,255 |
| `04_batch_functions.md` | 1,133 | 1,707 |
| `05_business_rules.md` | 1,107 | 1,722 |
| `06_exception_handling(2).md` | 767 | 1,580 |
| `07_processing_flows(1).md` | 1,090 | 1,292 |
| `08_architecture_decision(1).md` | 555 | 1,696 |
| **Total** | **7,698** | **16,577** |

All 90 original PDF pages have Phase 1 page-coverage records and were independently reopened with a PDF parser in Phase 6. **1,023** retained positive atoms and **37** negative controls have physical-page evidence. The three distinct Figure 1.1 assertions on physical PDF page 8 (`PDF-00977`, `PDF-00978`, `PDF-00979`) were verified in the rendered page image, because the rasterized figure text is not present in ordinary PDF text extraction. Of **1,023** source-positive atom excerpts, **1,020** are found in same-page PDF text and three require page-8 visual reading. There were no unexplained text-locator mismatches in the Phase 6 check.

The Phase 6 program checked **16,557** Markdown evidence references and **9,520** PDF evidence references across source, validation, and audit ledgers; these are reference occurrences, **not** independent claim counts. No bad source file path, line range, or excerpt was detected by this text/location verification. PDF citation presence alone cannot certify the semantic truth of an entailment claim.

There is **one** selected generated set. There is no second method for a meaningful between-method comparison, and the optional `11_comparison_final.*` files are therefore not applicable. All original inputs remain immutable.

## 2. Common source atomization and exclusions

The initial supplied source-positive inventory had 1,024 entries. In Phase 5, two summary/metadata atoms were removed as non-independent and one composite source atom was split into two independently scored obligations: 1,024 - 2 + 1 = **1,023** retained source atoms. The newly allocated `PDF-01025` preserves the extra independent provenance/traceability predicate. The atomization audit contains **18** review records, and the change ledger contains **158** entries. The original exclusion ledger contains **2,763** records; these are not to be counted as additional requirements.

The Phase 5 review retained distinct endpoint, actor, result, and test obligations where they have different testable predicates; repeated paths alone were not treated as proof of duplication. The 16 Appendix E test scenarios were examined for whether they independently require executable verification rather than merely repeating implementation facts. This phase independently checked that removal and split links still reconcile with the scored common R inventory; it did not reopen source extraction or re-atomize all 90 pages from scratch.

The fixed 37 negative controls are explicit PDF-grounded counterfactual diagnostics. They are neither a random population sample nor a count of every possible absent requirement; there is no legitimate population-wide specificity estimate from their TN value.

## 3. Source requirement coverage: provisional TP and FN

- **TP = 715.** Of these, 13 are graded direct `E3`, while 702 are graded complete-bridge `E2` in the saved evidence-match ledger. The 702 E2 proof records include inherited context, semantic equivalence, universal instantiation, or explicit conjunction as appropriate.
- Every TP has one Phase 5 predicate-map audit record with original PDF and generated Markdown citations, and all required predicate slots were structurally populated with `met` or `not_applicable`. **None of the 715 proof records claims full independent semantic certification**. A populated map is not itself proof that `not_applicable` was a correct semantic choice.
- **FN = 308.** Remaining FN root causes are `PARTIAL_ENTAILMENT` **274** and `CONSERVATIVE_UNRESOLVED` **34**. `TRUE_MISSING` **0** is not used for final dispositions. Do not call all 308 verified omissions.
- The root-cause audit records the earlier 357 matcher false negatives corrected to TP, including actual candidate text and PDF/Markdown locators, and two initially listed items corrected by source atomization.

The independently checked regression probes are:

| Probe | Original source atom | Current cell | Actual generated citations |
|---|---|---|---:|
| `case_title_field` | `PDF-00208` | `TP` | 1 |
| `workspace_retention_class` | `PDF-00199` | `TP` | 1 |
| `idempotent_case_creation` | `PDF-00948` | `TP` | 1 |
| `source_citation_version_lineage` | `PDF-01025` | `TP` | 3 |
| `figure_runtime_tenancy_actor` | `PDF-00977` | `FN` | 0 |
| `figure_immutable_policy` | `PDF-00978` | `FN` | 0 |
| `figure_idempotent_trace` | `PDF-00979` | `FN` | 0 |

The three page-8 figure probes are **FN** after the previous adjudication; their PDF **source reality** was visually verified, but whether some cross-file universal generated wording could entail them remains a semantic question, not a file-location question. The case-title, retention-class, repeated-create and immutable-citation probes are TP in the retained adjudication with real generated locators. These probes were read from current input data and are not preapproved goldset labels.

## 4. Generated correctness and false-positive interpretation

There are **5,289** eligible generated occurrences grouped into **5,258** raw within-method semantic classes. Phase 5's reciprocal PDF-check classifications are:

| Generated raw-class category | Classes |
|---|---:|
| `PDF_ENTAILED` | 2,170 |
| `SUPPORTED_NONCOVERING` | 1,446 |
| `PDF_UNSUPPORTED` | 1,642 |

The generated-only canonical FP projection contains **1,642** distinct allegedly unsupported generated propositions; they map one-to-one to the provisional unsupported raw-class labels. The Phase 5 correction removed seven nondefinitive generated classes and resolved 146 previously inconsistent TP-support/unsupported-class labels. The Phase 6 checker found no remaining class that is simultaneously `PDF_UNSUPPORTED` and used as a TP evidence bridge.

**Important limitation:** The **1,642** false positives are provisional *absence of proven full PDF entailment*, not necessarily **1,642** false features or contradictions. A generated statement describing an open decision is not automatically a positive implementation commitment; ambiguous mixed text still creates extraction and eligibility risk. This uncertainty can materially change Precision and F1 in either direction.

## 5. Negative controls and one canonical scoring universe

The negative-control polarity check found zero affirmative generated assertions of the 37 predefined prohibited/deferred capabilities, yielding **TN = 37** and negative-control **FP = 0**. Negative controls are never added to the positive source denominator.

The corrected one-universe identities are:

```text
R = 1023; N = 37; F = 1642
A = 715; B = 0
U = R + N + F = 2702
P = A + B + F = 2357
TP = 715; FN = 308; TN = 37; FP = 1642
TP + FN = R = 1023
TN + B = N = 37
FP - B = F = 1642
TP + TN + FP + FN = U = 2702
TP + FP = P = 2357
```

The raw generated-class count (G = **5,258**) differs from the effective canonical positive prediction count (P = **2,357**). This is required when one definitive shared generated rule entails multiple independently testable source propositions, without cloning generated occurrences.

## 6. Raw semantic-duplication audit

- Eligible generated occurrences: **5,289**.
- Distinct raw semantic classes: **5,258**.
- Excess eligible occurrences: **31**.
- Reconstructed within-file excess: **0**; reconstructed across-file excess: **31**.
- Repeated classes: **27**; classes spanning two or more files: **27**.
- Duplicate rate: **0.5861%**.

This is a raw class-membership statistic and does not use the expanded canonical TP/FN/FP universe. Near-duplicate paraphrases not previously merged by a full semantic adjudication may lower the observed rate. A 0.5861% mechanical rate is **not** certified absence of semantic redundancy.

## 7. Independent computation, verification and residual risks

The shipped `compute_metrics.py` independently loads all final item-level files; verifies ID partitions, class membership, valid source/negative labels, canonical scoring, generated-only FP projection, duplication partitions, TP predicate maps, FN dispositions, corrected source mappings, and original source locations; and recomputes all headline counts and rates. It then cross-checks the previously saved Phase 5 summary files *after* calculating the item-level results, without using those summaries as metric inputs.

- Structural execution: **PASS**, with **0** detected failures and **0** locator warnings.
- The 90-page PDF exists and is readable. The original eight Markdown files and their line-coverage records are present.
- No ZIP, TAR or bundled archive is produced; deliverables are individual files with English-authored text.
- The original PDF quotes, recovered generation occurrences, and any applicable content excerpts are grounded in the actual supplied inputs.

**Remaining certification limitations:**

1. The Phase 6 script checks *document existence, quoted text, structured predicate proof fields, logic of counts, and provenance links*. It does **not** independently reproduce natural-language full-predicate semantic judgments or manually inspect every PDF figure/table for a second opinion.
2. All 715 TP entries retain a `BEST_EFFORT_PREDICATE_AUDIT_NOT_FULL_INDEPENDENT_SEMANTIC_CERTIFICATION` scope. Their exact conditional, exception and outcome applicability can still be disputed.
3. The 34 conservative FN require substantive expert adjudication before treating them as verified missing requirements. The 274 partial FN have recorded unmet predicates, but alternative cross-document bridges may be found under deeper review.
4. The generated validity tally has many `BEST_EFFORT` records; not every `SUPPORTED_NONCOVERING` claim has been independently re-adjudicated as a separately normalized full PDF predicate.
5. Source extraction and full-predicate atomization can still have hidden errors despite the audited 18 decisions and 90-page evidence-access check. Both numerator and denominator may change after a genuinely independent semantic audit.

**Conclusion:** This phase completes independent *structural* recomputation and reproducible individual delivery at `PHASE_COMPLETED_BEST_EFFORT`. It does **not** promote the provisional Precision, Recall, F1, Duplicate, TP/FN/FP semantic labels to `FINAL_VERIFIED`.
