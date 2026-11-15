# Coverage, Evidence Quality, and Limitations — Phase 6

## Scope and final status

- **Protocol:** OrionDesk Six-Turn Semantic-Entailment Atomic Requirement Evaluation Protocol, version 6.1.
- **Method:** `supplied_set_01` (one unambiguously mapped eight-document set; no cross-method comparison is applicable).
- **Final status:** `FINAL_BEST_EFFORT`. All six phases were closed once, and this phase is complete. Full-predicate independent semantic certification is **NOT** claimed.
- **Authoritative requirements:** Original 90-page English `OrionDesk_AI_Detailed_Design_Specification(10).pdf` only. The eight scored Markdown files are generated outputs, not authorities for source requirements.
- **Original files were not modified.** Final deliverables are English-language individual files; no archive is supplied.

## Physical source and input coverage

The original PDF contains exactly **90 physical pages**. Every page yielded readable text in the final PyMuPDF check (90/90). The exact English source quotation for **1019 of 1019** retained PDF-positive atoms was found on its recorded original physical page. This verifies quotation location, not the claim's normative force or optimal atomization. Figures, tables, original page layout and reference diagrams were considered in the earlier page-level audit; a separate full independent multimodal human audit is not claimed.

| Role / supplied input | Physical lines |
|---|---|
| 01_screen_functions(9).md | 495 |
| 02_api(2).md | 696 |
| 03_data(10).md | 474 |
| 04_batch_functions(20261115-060045).md | 588 |
| 05_business_rules(10).md | 481 |
| 06_exception_handling(20261115-060054).md | 432 |
| 07_processing_flows(20261115-060053).md | 565 |
| 08_architecture_decision(20261115-060055).md | 225 |

The original eight scored Markdown files contain **3,956 physical lines** and the Phase-2 coverage ledger contains **3,956 physical line dispositions** with no omitted line. The Phase-2 table parser counted **6,308 table-cell positions** (a parser-specific measure; naïve pipe splitting is not an equivalent cell count). The Phase-6 recomputation reopened every used original generated line and confirmed **665 source-line quote matches** among final TP proofs. All **1541 TP PDF evidence page references** were within 1–90.

## Canonical universe and arithmetic

| Cell | Actual | Predicted | Count |
|---|---|---|---|
| TP | 1 | 1 | 584 |
| FN | 1 | 0 | 435 |
| FP | 0 | 1 | 571 |
| TN | 0 | 0 | 37 |
| Total | — | — | 1627 |

`|R|=1019`; `|N|=37`; `|F|=571`; `|B|=0`. Therefore `|U|=|R|+|N|+|F|=1627`. The bounded negative controls include only explicit PDF prohibitions, exclusions or release deferrals and do not represent the population of all possible negatives.

| Metric | Exact decimal | Display |
|---|---|---|
| Precision | 0.505627705628 | 50.56% |
| Recall | 0.573110893032 | 57.31% |
| F1 | 0.537258509660 | 53.73% |
| Semantic duplicate rate | 0.034051724138 | 3.41% |

A single universal generated rule can cover several independently testable PDF-positive requirements when its scope and conditions fully apply. Thus TP is **not** required to equal the number of raw generated classes. In this method `|GO|=2320`, `|G|=2241`, whereas effective predicted-positive canonical units `|P|=1155`. Do not use raw class-level denominators for conventional Precision, Recall or F1.

## FN correction, remaining root causes and source atomization

- Initial Phase-3 FN candidates reviewed: **741** records, including later corrected cases and removed source parents.
- Corrected initial matcher false negatives across Phases 3, 5 and 6: **301**. Phase 6 identified and corrected **10 additional explicit full-predicate matches** found during independent high-risk and regression review, documented in `06_phase6_corrected_retrieval_matches.jsonl`. Corresponding source-to-generated, bridge, FN, TP, validity, judgment and class metadata records were reconciled.
- Source atomization audit: **1025** decisions; **5** nonindependent parent/summary atoms removed in Phase 5 with prior/replacement IDs and original PDF quotations. The common positive inventory is **1019** after these changes, not a historical fixed total of 1,024.
- Final FN total: **435**. The dispositions remain deliberately distinct:

| Final FN root-cause disposition | Count | Interpretation |
|---|---|---|
| TRUE_MISSING | 12 | A scored-corpus obligation remains absent under recorded search. |
| PARTIAL_ENTAILMENT | 106 | Related definitive commitment exists but a substantive predicate is missing. |
| CONSERVATIVE_UNRESOLVED | 317 | Full entailment remains unproved despite retrieved alternatives; not a certified omission. |

The **317 conservative FN** decisions and **106 partially covered FN** decisions are not proof that these requirements are absent from the generated specification. Their closest actual candidates, searched aliases, applicability checks and unmet predicate descriptions remain in `03_fn_root_cause_audit_final.jsonl`. More semantic review could move counts in either direction.

## TP proof and generated-claim validity

There are **584** final TP evidence-audit rows, one for each final TP; each includes an original PDF locator, a real generated-file/line excerpt, a predicate-check map, source scope and coverage mode. These consist of **396 E3** and **188 E2** graded records after Phase-6 corrections. `E2` denotes an evidenced contextual/universal/conjunctive entailment, not partial credit. The automated checks show that original evidence strings and file/line positions exist, but the map's `met` status is **not equivalent** to external human verification of every semantic predicate.

The **2241** generated classes are independently adjudicated in the generated-validity ledger:

| Generated-class validity | Class count |
|---|---|
| PDF_ENTAILED | 417 |
| SUPPORTED_NONCOVERING | 1253 |
| PDF_UNSUPPORTED | 571 |

A generated class labeled `SUPPORTED_NONCOVERING` may be backed by a narrower source rule without satisfying any independently retained source-positive atom. Its count (**1253**) is an audit signal about source-atomization and matching completeness. The **571** PDF-unsupported generated classes yield **571** conservatively scored generated-only FP units after distinct canonical merging and negative-control deduplication. These are **not** all confirmed design errors; a source-supported narrower alternative or implicit context could still change some of their classifications. No negative counterfactual control was asserted (`B=0`, `TN=37`).

## Diagnostic exact-match and reciprocal regression probes

The following tests check the corresponding live source Markdown line, case/field/API/test context and current canonical label. These probe identities were confirmed in this input corpus rather than imposed as a goldset.

| Probe | Source ID | Original input | Result |
|---|---|---|---|
| case_title_field | PDF-00208 | 01_screen_functions(9).md | PASS |
| workspace_retention_class | PDF-00199 | 01_screen_functions(9).md | PASS |
| replayed_case_create_same_outcome | PDF-00948 | 06_exception_handling(20261115-060054).md | PASS |
| tenant_case_unique_constraint | PDF-00886 | 03_data(10).md | PASS |
| long_running_post_idempotency | PDF-00473 | 01_screen_functions(9).md | PASS |
| idempotency_changed_fingerprint_conflict | PDF-00474 | 01_screen_functions(9).md | PASS |
| atomic_publication_gate | PDF-00393 | 06_exception_handling(20261115-060054).md | PASS |

In addition, an exact normalized full-quote/statement scan over every remaining FN and the full eight-file text found no verbatim sentence-copy conflict. This **does not** establish the absence of semantic equivalents; the Phase-6 high-risk challenge explicitly uncovered ten nonverbatim, context-dependent equivalents and corrected them. Other high-risk FNs, E2 bridges and FP residual predicates still require independent domain-specific validation for a `FINAL_VERIFIED` claim.

## Duplicate partition

The final raw claim inventory has **2320** occurrences and **2241** classes. Excess occurrences = **79** = **3** within-file + **76** across-file. Repeated classes: **61**, including **58** spanning multiple documents. Duplicate rate **3.41%**. Some unmerged meaning-preserving paraphrases may remain, so this rate is best-effort.

## Exclusions, reproducibility and interpretation

The consolidated `09_excluded_units.jsonl` records **5,616** excluded spans, including PDF context/headings and generated headings, source citations, open questions, unadopted proposals, table structure and examples without independent commitments. The Phase-6 generated-class metadata reconciliation changes only stale status labels, not raw occurrence identity, source atoms, negative controls, FP residuals or class membership.

Reproduce: `python compute_metrics.py --base <directory containing final ledgers> --inputs <directory containing the original PDF and eight scored Markdown inputs> --write`. The script verifies item-level counts, origin partitions, class/occurrence membership, duplicate partitions, audit coverage, source pages, original generated line evidence, original PDF quotations and seven live regression probes. The script was executed successfully with **zero structural validation errors**.

**Limitations:** Structural agreement, exact quotations, TF-IDF/BM25-like retrieval and recorded predicate flags do not certify complete semantic equivalence; many generated validity judgments use heuristic or contextual source evidence. Evaluation covers only the fictional R1.0 / revision 1.3 design baseline, not real implementation safety, performance, business value or deployment readiness. The resulting point estimates are provisional best-effort measures subject to future human semantic reassessment in either direction; no fabricated statistical confidence interval is attached.
