# OrionDesk AI — One-Pass Atomic Specification Evaluation Protocol

**Version:** 9.0  
**Purpose:** Measure how well eight generated design specifications cover a frozen PDF-grounded benchmark without asserting unsupported requirements.  
**Execution:** Nine ordered phases; one phase per request–response where feasible.  
**Language:** All authored protocols, data files, scripts, comments, and reports must be in English.

## 1. Inputs and fixed rules

Required inputs:

- `common_atomic_reqs.jsonl`: frozen positive requirements (`R`, keyed by `source_id`).
- `common_negative_controls.jsonl`: frozen negative controls (`N`, keyed by `negative_control_id`).
- `reference_freeze.json`: expected hashes, reference version, status, and limitations.
- `OrionDesk_AI_Detailed_Design_Specification.pdf`: original authority for claim meaning and support.
- Eight generated Markdown files: `01_screen_functions.md`, `02_api.md`, `03_data.md`, `04_batch_functions.md`, `05_business_rules.md`, `06_exception_handling.md`, `07_processing_flows.md`, `08_architecture_decision.md`.

Resolve every input unambiguously; accept upload-copy suffixes but record actual filenames. Treat all eight generated files as **one corpus** per evaluated method. Preserve input files unchanged.

1. Before scoring, verify readability, unique R/N IDs, actual PDF page count, and SHA-256 hashes against every applicable expected digest in `reference_freeze.json`. A required mismatch or missing input **blocks** evaluation.
2. Freeze R and N by exact bytes and IDs. Do not construct, validate completeness of, correct, merge, split, supplement, or regenerate the Gold Set or controls during evaluation. Assume R is complete **for this benchmark**; preserve documented limitations.
3. Use the PDF to interpret R and to verify generated claims, **not** to amend R or N. Log material reference/PDF contradictions as `REFERENCE_EXCEPTION` without changing the reference.
4. Recheck reference hashes at delivery. If either frozen file changes, mark `INVALID_REFERENCE_CHANGED` and withhold comparable scores.
5. Compare `fullload`, `onelevel`, and `twolevel` only with the same frozen reference, PDF, eligibility rules, semantic criteria, and counting policy. Method identity is supplied by the operator, not inferred from perceived quality.

## 2. Units and semantic rules

- **R:** Each frozen source requirement is one scoring unit; final result: `COVERED` or `NOT_COVERED`.
- **N:** Each frozen counterfactual control is one scoring unit; final result: `ASSERTED` or `NOT_ASSERTED`.
- **GO:** Eligible definitive generated atomic *occurrences*, each with an original file/line/table locator.
- **GC:** Distinct generated semantic *classes*. Each eligible GO belongs to exactly one GC; one GC links all equivalent occurrences.
- **F_ONLY:** Distinct unsupported generated *residual propositions*, excluding propositions already represented by asserted N controls.

Extract independently testable, definitive commitments about operations, data, APIs, conditions, access, failures, constraints, timing, policies, and adopted decisions. Restore section/table/row/column context. Split independent obligations, not arbitrary words or headings. Exclude editorial text, pure references, illustrative examples, hypothetical tests without asserted behavior, questions, `TBD`, and unadopted alternatives/proposals. A claimed `Confirmed` status does not establish PDF support.

Evaluate **complete meaning**: actor, action, object, modality, polarity, scope, conditions, exceptions, timing, version, quantitative limits, and outcome where relevant.

- `COVERED` requires actual definitive generated evidence that entails **every material R predicate**. Check direct equivalence, aliases, universal-rule applicability, inherited context, and compatible cross-file conjunctions. One justified universal rule may cover several distinct R IDs; each R counts once.
- `NOT_COVERED` requires the strongest candidate and missing predicates, or a bounded eight-file absence-search receipt. Similar wording does not prove coverage; low similarity does not prove absence.
- Every effective GC receives `PDF_SUPPORTED` or `PDF_UNSUPPORTED` after checking the PDF. A PDF-supported GC covering no frozen R is `SUPPORTED_NONCOVERING`, **not FP**. A partially unsupported GC contributes only its distinct unsupported residuals.
- An N control is `ASSERTED` only by an affirmative, definitive generated commitment with the matching predicates. Prohibitions, quotations, unresolved options, and risk discussions are not assertions.
- Merge GO classes or FP residuals **only when their complete material propositions mutually entail one another**. Shared keywords, the same endpoint family, or general-versus-specific entailment alone do not establish equivalence.

For each binary decision record `basis` (`DIRECT`, `CONTEXTUAL`, or `BEST_EFFORT`), `confidence` (`HIGH`, `MEDIUM`, or `LOW`), actual evidence locators, and a short reason. A genuinely uncertain item still receives the most defensible evidence-based binary decision; never classify it as FP/FN solely for being uncertain. Never invent evidence, verification, or reviewers.

## 3. Efficient evidence processing

1. Parse and index the PDF and all eight original Markdown files **once**. Retain physical PDF pages, headings, tables, original lines/cells, aliases, IDs, API paths, fields, events, error codes, numbers, polarity, and inherited scope.
2. Index both GO/GC and original Markdown, including substantive excluded text. Build source-to-GC and GC-to-source candidate links in batches.
3. Use deterministic lookup and optional semantic ranking for **candidate discovery only**; no similarity threshold may decide entailment, PDF support, or equivalence.
4. Cache source evidence, checked aliases, universal-rule predicates, and rule-family proofs. Reuse a proof only after checking each item's scope, applicability, and exceptions.
5. Prefer representative family checks and targeted expansions over per-item full-document rescans or unrestricted all-pairs comparisons. Reuse adjudicated evidence across phases.
6. Record concise proof and search receipts, not exhaustive hit transcripts. Reduce redundant work and prose, **not** required R/N/GC population coverage.

## 4. Phases and required outputs

| Phase | Work | Artifact | Completion condition |
|---|---|---|---|
| **01 — Reference Lock** | Resolve inputs, verify hashes, PDF, and R/N IDs | `01_reference_lock.json` | All input identities and reference hashes verified |
| **02 — Generated Extraction** | Inspect eight files; extract GO, locators, substantive exclusions | `02_generated_occurrences.jsonl` | All substantive sections/tables accounted for |
| **03 — Semantic Classes** | Form GC and classify excess occurrences | `03_semantic_classes.jsonl` | Every effective GO maps to one GC; counts reconcile |
| **04 — Source Coverage** | Main semantic coverage judgment for every R | `04_source_coverage.jsonl` | Exactly one evidenced binary decision per R |
| **05 — FN Audit and Recovery** | Screen all provisional FN; challenge selected groups; repair extraction gaps through overlays | `05_fn_reassessment.jsonl` | Every provisional FN and flagged extraction gap resolved in records |
| **06 — PDF Validity** | Assess every effective GC; isolate unsupported residuals | `06_pdf_validity.jsonl` | One PDF decision per effective GC; residuals traceable |
| **07 — FP and Controls** | Deduplicate residuals across eight files; assess every N | `07_fp_controls.jsonl` | All residuals/N accounted for; no control/FP double count |
| **08 — Quality Audit** | Bounded risk audit; apply corrections; finalize item-level records | `08_final_ledger.jsonl` | All final R/GC/N/FP IDs and corrections reconcile |
| **09 — Metrics** | Independently recompute and report | `compute_metrics.py`, `09_metrics.json`, `09_report.md` | Hashes, identities, equations, and final counts verified |

Each phase includes a compact `PHASE_SUMMARY` with counts, status, issues, and confidence breakdown (inside its sole file). Previous phase outputs are immutable; subsequent corrections are linked overlays or `CHANGE` records. Produce no extra audit files or archive unless requested.

### Phase 04 — Main coverage pass

For **every R**, reconstruct material predicates from frozen evidence and relevant PDF context; search the full indexed eight-file corpus, including universal and cross-file rules. Judge the strongest candidates using original Markdown context. Before `NOT_COVERED`, test likely aliases, scope rules, and missing predicates. Permit one focused expansion per ambiguous R; extend checks for material security, authorization, approval, tenancy, irreversible-operation, numeric, or contradictory cases. Flag any original-Markdown proof missing from GO/GC as `EXTRACTION_GAP_CANDIDATE` without inventing a class. A complete Markdown proof may support `COVERED` with its real locator pending recovery in Phase 05.

### Phase 05 — Fixed FN audit budget

- **Screen every Phase 04 FN** using existing candidates/receipts; review every flagged extraction gap, including those on covered R IDs.
- Deep-challenge **up to 120 risk-ranked FN groups plus up to 40 reproducibly stratified groups** from the remaining eligible groups. If fewer exist, inspect all. Record selection, inspected evidence, and applicability to grouped IDs.
- Recover missed definitive occurrences/classes with new recovery IDs and original locators; never edit Phase 02–04 or R/N. Propagate a demonstrated error pattern to affected rule-family members **only after verifying each member's applicability**.
- Emit exactly one reassessment per provisional FN and one resolution per flagged extraction gap. Distinguish `SCREENED`, `CHALLENGED`, `FAMILY_APPLIED`, and `RECOVERED`; screening alone is **not** independent deep verification.
- Use this fixed budget for v9.0; do **not** adjust it according to observed error rates. Repair discovered errors; report remaining uncertainty. Audit-budget optimization belongs to a later protocol version.

### Phases 06–08 — Validity, FP, final audit

- Phase 06 checks **all effective GC**, including recovered GC, against actual PDF evidence. Verify material predicates and separate unsupported additions/contradictions from valid parts. Absence of an R match alone is never FP proof.
- Phase 07 clusters **all unsupported residuals**, not unmatched R atoms or raw generated sentences. Run a targeted second cross-cluster check for missed paraphrases and over-merges; retain every class/occurrence locator. Crosswalk semantically identical asserted N propositions and remove them from `F_ONLY`.
- Phase 08 deep-challenges **up to 80 risk-ranked canonical groups plus up to 20 reproducibly sampled groups**. Prioritize likely false FN/FP, disputed merges, universal-rule scope, approval/authorization/privacy/tenancy, irreversible actions, and quantitative or error semantics. Reuse earlier evidence. A self-check in the same context is not an independent reviewer.
- Apply every discovered correction with real evidence, previous/new decisions, and affected IDs. Update **all dependent final records**, including recovered classes, FP clusters, controls, and source matches. Do not silently change a previous phase file.

## 5. Counting and metrics

Count from **Phase 08 final item-level records only**, never a manual summary:

```text
TP = count(FINAL_SOURCE == COVERED)
FN = count(FINAL_SOURCE == NOT_COVERED)
TN = count(FINAL_CONTROL == NOT_ASSERTED)
B_asserted = count(FINAL_CONTROL == ASSERTED)
F_only = count(unique generated-only FINAL_FP_CLUSTER)
FP = B_asserted + F_only

TP + FN = |R|
TN + B_asserted = |N|

Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1 = 2 * TP / (2 * TP + FP + FN)
```

Use JSON `null` for zero denominators and explain them. Do **not** substitute intervals for the single best-effort point estimates. Report confidence/remaining doubt separately.

**Interpretation and comparability:** The formulas are standard; the counting units are protocol-specific. TP/FN are frozen R atoms; FP consists of unique unsupported generated residuals plus asserted N controls. Compare generation methods only under identical references and scoring rules. Do not directly compare scores with benchmarks using different counting units. F1 is **not** the percentage of correct generated claims. **Do not calculate Generated Claim Validity.**

**Diagnostic counts, not additional performance metrics:**

```text
GO = GC + EXPECTED_REUSE + REDUNDANT_DUPLICATE
PDF_SUPPORTED_GC + PDF_UNSUPPORTED_GC = GC
```

An excess occurrence is `EXPECTED_REUSE` only when it serves a demonstrated independent specification role; otherwise it is `REDUNDANT_DUPLICATE`. A repeated claim does not increase TP or FP. TN applies **only** to frozen bounded negative controls; never infer population-wide accuracy or specificity.

## 6. Minimum records and verification

Every JSONL row has `record_type`, stable IDs, real locators, and sufficient evidence/reasoning to reproduce its decision. Include, as applicable:

- `OCCURRENCE`, `EXCLUSION`, `CLASS`, `DUPLICATE`, `RECLASSIFIED_EXCLUSION`.
- `SOURCE_JUDGMENT` with R ID, verdict, candidates, missing predicates or entailment proof, basis/confidence, and actual generated locator.
- `FN_REASSESSMENT`, `EXTRACTION_GAP_REVIEW`, `RECOVERED_OCCURRENCE`, `RECOVERED_CLASS`, and `FN_CHANGE` with provenance and effective-GO/GC reconciliation.
- `PDF_JUDGMENT` with GC ID, PDF physical page/section, support decision, and exact unsupported residuals.
- `FP_CLUSTER` with one complete residual proposition, all GC/GO provenance, equivalence proof, and N crosswalk; `NEGATIVE_CONTROL` with each frozen N ID and evidence.
- In Phase 08: exactly one `FINAL_SOURCE` per R, one `FINAL_CLASS` per effective GC, one `FINAL_CONTROL` per N, and one `FINAL_FP_CLUSTER` per generated-only FP, plus applicable `CHANGE`, `REFERENCE_EXCEPTION`, and `FINAL_SUMMARY`. Reference prior evidence by ID instead of copying it.

`compute_metrics.py` must fail on missing/duplicate IDs, invalid judgments, unresolved occurrence/class mappings, missing PDF decisions, unmatched unsupported residuals, double-counted FP/controls, failed reference hashes, and violated count equations. Check original evidence locators and all required artifacts. Include final input hashes, processed counts, audit budgets used, corrections, low-confidence totals, and method-comparison limitations in the English report.

These mechanical checks establish **reproducible accounting**, not perfect semantic correctness. Do not claim independent review or semantic certification unless actually performed.

## 7. Operating rule

Execute **only the next requested phase**, normally finishing it in one response. Do not advance with incomplete required item populations. If a real file/platform limit prevents completion, save a resumable checkpoint and mark `INCOMPLETE`; resume the same phase. Ordinary nonblocking semantic uncertainty receives a documented binary best-effort decision, not an endless review loop. Deliver only that phase's required English artifact(s) and a concise completion summary.

**Final objective:** Reproducible single-value **TP, TN, FP, FN, Precision, Recall, and F1**, based on frozen references, full eight-file coverage, semantic FP deduplication, bounded audits, and traceable best-effort judgments.
