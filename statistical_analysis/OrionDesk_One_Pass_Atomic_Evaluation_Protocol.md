# OrionDesk AI — Eight-Phase Evidence-Grounded Atomic Requirement Evaluation Protocol

**Protocol version:** 10.5  
**Purpose:** Evaluate eight generated design specifications against one authoritative PDF using a frozen benchmark, complete bidirectional evidence accounting, confidence-guided verification, and up to **4,096 selected item-level atomic LLM adjudications for `fullload`** or **2,048 for `onelevel` and `twolevel`**, transmitted in batches of at most **8 items** with at most **4 concurrent LLM requests**. The mandatory Phase 07 outcome, after a valid external handoff, is one deterministic best-effort TP/FP/FN/TN disposition for every canonical unit, with a separately recorded verification quality; Phase 08 reports one full-population arithmetic score, never a statistical sample estimate.  
**Method:** Evidence-first differential evaluation with full-population ledgers, verified proof-family reuse, confidence-guided adjudication priority, targeted original-file LLM review, and **automatic deterministic four-cell TP/TN/FP/FN closure in `semantic_decision_evaluator_10.5.py`** after the required batch handoff. Phase 08 independently recomputes canonical metrics.  
**Supported methods:** `fullload`, `onelevel`, `twolevel`.  
**Required operator input:** `spec_gen_method` must be explicitly supplied as exactly one of `fullload`, `onelevel`, or `twolevel`. Never infer or default this value.  
**Execution:** Exactly eight ordered phases; one phase per operator request and response. Finish the current phase before advancing.  
**Language:** Follow the operator's language for conversation. **All authored artifacts, script text, record values written as prose, and reports must be in English.**  
**Delivery:** Individual phase outputs. No archive or separate revision-history artifact unless explicitly requested.

## 1. Governing rules

1. **Source authority.** The original 90-physical-page *OrionDesk AI Detailed Application Design Specification* PDF alone determines source requirements, exclusions, and meaning. Generated specifications, model answers, historical scores, and prior ledgers are evidence or candidate predictions, not independent PDF authority. Inspect all pages, figures, tables, appendices, captions, and substantive generated text.
2. **Frozen reference.** When `common_atomic_reqs.jsonl`, `common_negative_controls.jsonl`, and `reference_freeze.json` are supplied, frozen-benchmark mode is mandatory. Verify identity, pages, SHA-256, ID uniqueness, references, and readable evidence; do not alter the reference bytes or denominator. In the absence of a frozen reference, construct and freeze `R` and `N` independently from the PDF in Phase 01 before any generated inspection. Never silently replace an invalid supplied benchmark.
3. **Complete populations, selective LLM, mandatory closure.** Process every source-positive requirement `R`, fixed negative control `N`, substantive generated occurrence `GO`, and generated semantic class `GC` through reproducible extraction, indexing, evidence matching, and item-level verification. **The method-specific selected LLM items (at most 4,096 for `fullload`, or 2,048 for `onelevel`/`twolevel`) are a bounded assistance set, not a substitute for closing the full population.** After a valid Phase 07 handoff, deterministically assign all effective R and N records to TP/FN and FP/TN respectively, and all effective GC claims to a definitive supported/unsupported/nondefinitive category using §§3.4–3.6. Separate `VERIFIED` from `BEST_EFFORT` decisions without assigning statistical weights. Each selected item receives an independent JSON judgment even when 8 items share one API request.
4. **Actual logical entailment.** Full coverage requires all relevant actor, target, action, modality, scope, conditions, exceptions, time, limits, version, and outcome. A single applicable universal rule or an explicit cross-file conjunction may satisfy several independent source requirements, but produces neither duplicated generated occurrences nor additional raw classes. Exact identifiers and similarity alone are insufficient.
5. **Two distinct directions.** `R → generated` measures source coverage. `generated → PDF` measures validity of definitive generated claims. A generated statement absent from frozen `R` is not automatically unsupported; a missing retrieval hit is not a verified FN.
6. **Conservative unsupportedness.** A generated commitment is an FP candidate only when the original PDF does not normatively support its full affirmative content and the unsupported predicate is specifically identified. Search the full PDF, including governing common rules and contextual tables, before this finding. Record supporting narrower content separately.
7. **Definitive statements only.** Unadopted proposals, `TBD`, `Needs confirmation`, unresolved alternatives, examples without normative adoption, headings, bare references, and purely explanatory text are not final positive predictions. Preserve any separable definitive claim within a mixed passage, with its actual inherited context.
8. **No artificial atom multiplication.** Split only independently testable complete obligations. Never create stand-alone claims from an isolated table cell, field label, HTTP code, ID, or citation. Merge semantic duplicates only with full mutual entailment; differences in API path, role, conditions, status, version, or consequence can make claims distinct.
9. **Evidence is inspectable and proof quality is explicit.** Every **verified** TP needs complete PDF/generated-original evidence and full-predicate proof; verified FN needs a reciprocal search and specific missing predicate; verified FP needs its exact unsupported residual and PDF countercheck; verified TN needs an audited generated nonassertion. A **best-effort** cell instead requires the strongest available original evidence, source/corpus search receipts, the precise unverified dimensions or unsupported predicate, and a deterministic decision-rule ID; it must never be mislabeled verified. Original filename, PDF physical page, Markdown line/row/cell and contextual scope must be recoverable wherever present.
10. **Mandatory deterministic best-effort adjudication.** Each R/N and effective GC record carries three distinct measures: `model_confidence_estimate`, `evidence_strength`, and `verified_confidence_level`, plus `decision_basis`, `verification_status`, `unreliable`, and `unreliable_reason_en` (§§3.4–3.6). Confidence is not a calibrated probability of correctness. **When the last required batch commits, the evaluator MUST invoke the deterministic full-population closure with non-null TP/FN for every R, FP/TN for every N, and a four-cell diagnostic classification for every GC; `G` counts contribute canonical FP only through deduplicated `FINAL_RESIDUAL` records. Phase 07 validates that committed closure, and Phase 08 independently recomputes the arithmetic.** `scoring_cell: null` is permissible only in Phases 01–06 or in an `INCOMPLETE` Phase 07 with a genuine missing/corrupt input blocker.
11. **No prior-result presumption.** Revisit earlier TP, TN, FP, FN and exclusions when evidence warrants. Inherited completed files are reusable as indexed evidence only after their source hashes, line locators, and relevant predicates are reverified. Earlier v10.1/v10.2/v10.3/v10.4 labels are not v10.5 verification. Existing earlier phase artifacts, batch journals, and queues remain immutable; a v10.5 Phase 06 queue must be issued as a new, separately hashed artifact, never silently relabeled or overwritten.
12. **Immutable, reproducible history.** Original scored documents, frozen `R/N`, and delivered phase files are immutable. Later corrections are appended as item-level supersession/adjudication records in the subsequent phase ledger. Preserve the prior ID and the effective replacement without rewriting earlier bytes. Do not create a separate revision-history document.
13. **One full-population score, never statistical estimation.** Structural checks, a high-confidence model claim, or a high rate of `FULL` results do not prove correctness. After the evaluator performs mandatory deterministic best-effort closure and Phase 07 checks it, Phase 08 computes **one** Precision, Recall, and F1 directly from the exhaustive canonical unit ledger, with mandatory `VERIFIED` versus `DETERMINISTIC_BEST_EFFORT` status and decision-quality counts. These are arithmetic rates of the recorded classifications, **not statistically estimated population metrics and not guaranteed ground truth when some classifications are best effort**. Never generate a second estimate, extrapolated counts, model-confidence-weighted rate, or confidence interval; never describe `DETERMINISTIC_BEST_EFFORT` rates as independently verified.
14. **One response, one phase.** Complete all records belonging to the requested phase or report a genuine input/platform blocker as `INCOMPLETE`. A fully enumerated phase with individually marked semantic uncertainty may be `PHASE_COMPLETED_BEST_EFFORT`. Do not start the next phase in the same turn.
15. **Manually specified generation method.** The operator must explicitly provide `spec_gen_method` as exactly one of `fullload`, `onelevel`, or `twolevel` for the eight specifications being evaluated. Do not infer it from filenames, document content, previous results, or the presence of method-specific artifacts. Validate and record the supplied value in Phase 01, and preserve it unchanged in subsequent phase outputs. If the value is missing, invalid, or ambiguous, report Phase 01 as `INCOMPLETE` and do not proceed.

## 2. Inputs, identity, and extraction

### 2.1 Required materials

- The original, readable 90-page English PDF (authoritative source).
- An explicit operator-supplied `spec_gen_method` value: `fullload`, `onelevel`, or `twolevel` (exactly one; no inferred/default value).
- Exactly eight original Markdown roles, mapped unambiguously: `01_screen_functions.md`, `02_api.md` (also `02_api_.md`), `03_data.md`, `04_batch_functions.md`, `05_business_rules.md`, `06_exception_handling.md`, `07_processing_flows.md`, and `08_architecture_decision.md`.
- In frozen mode: `common_atomic_reqs.jsonl`, `common_negative_controls.jsonl`, and `reference_freeze.json` (upload-copy suffixes accepted).
- For external adjudication: operator-maintained `semantic_decision_evaluator_10.5.py`, a newly committed selected JSONL queue of at most the method-specific limit (4,096 for `fullload`; 2,048 for `onelevel` or `twolevel`), and per-item `semantic_decisions.jsonl` plus batch journals and the submission-attempt ledger. The paired v10.5 evaluator implements the mandatory queue-evidence, candidate-label, and retry-budget safeguards below.

Recognizable method prefixes and copy suffixes are permitted only with unique role mapping. Preserve actual input filenames and bytes in every evidence ledger. A normalized role name is a lookup alias, not an alteration of the source. The protocol, earlier phase ledgers, and any aggregate JSON are not ninth scored Markdown inputs.

### 2.2 Frozen checks and source-atom rules

Read each frozen JSONL record and validate the declared positive key (`requirement_id` or `source_id`) and negative key (`control_id` or `negative_control_id`), no mixed keys or duplicates, original PDF SHA-256, expected reference hashes, physical page count, and evidence quotation availability. Fail on incompatible identity/hash or inaccessible required material. Record nonfatal benchmark atomization doubts as `REFERENCE_EXCEPTION`, leaving IDs and bytes unchanged.

`R` comprises smallest independently meaningful PDF-positive normative obligations; a PDF prohibition is itself a positive duty to enforce. General obligations must not be repeated arbitrarily for each endpoint. An endpoint with a distinct method, actor, response, condition, or timing can have independent atoms. Preserve original page, quote, actor, target, condition, constraint, version, outcome, and additional supporting locations.

`N` is a fixed bounded inventory of affirmative counterfactuals explicitly prohibited, excluded, or deferred in the PDF. It is not the set of every possible absent feature. Keep `R ∩ N = ∅`. Never add method-specific controls during scoring.

### 2.3 Generated inventories

`GO` is the set of complete, eligible definitive assertion occurrences, with stable `GEN-*` ID and actual Markdown file, line, row, cell, heading, and full inherited context. `GC` is the set of unique within-method semantic classes, with stable `GCLASS-*` ID and exactly one class assignment per eligible `GO`. Every substantive source line/row must be accounted for by eligible assertions, exclusions, or inherited context; excluded prose is indexed and re-examined in Phase 05. Recovered assertions use new stable IDs and original locators without altering prior files.

## 3. Evidence-first matching and semantic judgment

### 3.1 Reusable indexing, never similarity verdicts

Index original PDF pages, all eight Markdown lines and table rows, IDs, methods/paths, event names, data fields, numeric bounds, scope terms, negation, headings, exceptions, and universal-rule subjects. Use exact and alias lookup plus optional semantic retrieval to *discover* candidates. Preserve original context and a reciprocal generated-to-PDF index. **Before LLM selection, build a proof-family ledger** linking related R, N, and GC items to a canonical proposition and evidence. Store verified original PDF/generated hashes, the complete predicate, applicability and exception boundaries, and each potential transfer recipient. Reuse a validated full-predicate proof only after individually checking the recipient's actor, target, action, modality, scope, conditions, exceptions, time, limits, version, and outcome. A shared subject, high similarity, or repeated wording is not enough. Record a specific rejection reason for unsafe proof transfers; never replicate one G class into extra TP or FP units.

A filename-alias validator must resolve an LLM-provided filename by the uniquely identified eight-file role and verified SHA-256 source mapping, then verify the quoted text in the indicated actual original line range. For example, `03_data.md` and an unambiguous uploaded `03_data(1).md` may map to the same verified role. **Do not reject an accurate quotation solely because the model used a canonical versus uploaded copy suffix.** Reject an ambiguous role, inconsistent digest, wrong original line, or mismatched quotation. Log both reported and resolved names; never silently accept a quotation from a different file.

### 3.2 Bidirectional coverage decisions

For every `r ∈ R`:

1. Reconstruct the whole normative proposition from its PDF page, section and table context.
2. Search full generated text, eligible GO/GC, common clauses, and exclusions using direct wording, synonyms, identifiers, literal values, and reverse links.
3. Test direct equivalence, logically applicable universal rules, inherited context, and explicit conjunctions across files.
4. For every proposed TP, check the whole source predicate; cite a complete proof. For a provisional FN, challenge the strongest actual nearby candidate, document precisely what is missing, and revisit it from the generated-to-source direction.
5. Before Phase 07, label a `VERIFIED` TP only after complete `E3` direct or `E2` contextual/conjunctive entailment, and a `VERIFIED` FN only after demonstrating `TRUE_MISSING` or `PARTIAL_ENTAILMENT` in a reciprocal audit. Unverified items remain null **during earlier phases**, then receive the mandatory best-effort Phase 07 classification under §3.6 without falsely inheriting verified proof status.

For every definitive `g ∈ GC`, independently inspect whether the PDF supports its **entire** generated commitment; label `PDF_ENTAILED`, `SUPPORTED_NONCOVERING`, `PDF_UNSUPPORTED` with exact residual, or explicit unresolved. A statement supported by the PDF but not matched to a frozen source atom is `SUPPORTED_NONCOVERING`, not FP. A generated claim may entail several R atoms without being replicated as several GCs. After all K batches commit, the evaluator must close each GC to a deterministic binary diagnostic cell under §3.6 and preserve its source-support provenance separately; Phase 07 checks this classification against the complete source corpus.

For every `n ∈ N`, determine whether an eligible definitive generated assertion actually affirms the forbidden counterfactual. Affirmed means `FP` in the fixed N row; documented nonaffirmation means `TN`; evidence uncertainty means `UN` before Phase 07; under Phase 07 deterministic closure, apply §3.6 and retain uncertainty as `unreliable=true` rather than an unscored control. An explicit prohibition of the forbidden behavior is not its affirmation.

### 3.3 Entailment evidence grades

| Grade | Standard | Permissible conclusion |
|---|---|---|
| `E3` | Complete direct equivalence with verified original-file proof | Full entailment |
| `E2` | Complete universal/contextual/conjunctive logical proof with verified scope | Full entailment |
| `E1` | Relevant but materially incomplete predicates | Partial only; FN or FP solely with further defensible source/corpus review |
| `E0` | Explicit contradiction or evidenced complete nonentailment | Negative finding if scope and full review are verified |
| `EU` | Important evidence/meaning unresolved | Phases 01–06: `scoring_cell=null`; completed Phase 07: non-null §3.6 best-effort cell, `unreliable=true`, and explicit evidence limitations |

`E2` is as valid as `E3` for a **verified** TP. Neither `E1` nor a low retrieval score automatically proves a **verified** FN/FP; §3.6 may nonetheless assign a documented **best-effort** cell after the mandatory full search and deterministic tie-break. Direct-match exclusions, partial table rows, competing clauses, and source-atom overlap are mandatory audit flags.

### 3.4 Three distinct confidence measures (mandatory classification inputs)

Every effective R/N/GC item must retain **all three** measures, independently auditable in Phase 07:

- **Model confidence — `model_confidence_estimate`:** the external model's self-reported confidence in its own proposed judgment, numeric `[0,1]` or JSON `null` when absent. It is **not** `Pr(TP)` and applies equally to a `FULL`, `PARTIAL`, `NOT_FOUND` or contradiction judgment. Preserve `model_judgment` and original JSON. Never substitute a confidence from another item or a historical sample.
- **Evidence strength — `evidence_strength`:** ordinal `E3`, `E2`, `E1`, `E0`, `EU`, according to §3.3, with original-page/line locators, dimension-by-dimension support and any contrary evidence. `E3` is complete direct support, `E2` complete verified contextual/conjunctive support, `E1` relevant incomplete support, `E0` evidenced contradiction/complete nonentailment, and `EU` unresolved evidence. E0 means strong **negative** evidence, not low confidence by itself. Do not convert the ordinal grade into an invented probability.
- **Verified confidence — `verified_confidence_level`:** `HIGH`, `MEDIUM`, or `LOW`, independently derived from *original-file verification and audit completeness*, not from the model's confidence. `HIGH` requires hash-valid original quotations and a fully inspected eleven-dimension proof or complete contrary/nonassertion search; `MEDIUM` requires verified relevant quotations, inspected critical scope and no unresolved direct contradiction but some incomplete dimensions; `LOW` is retrieval-only, unverified, contradictory, or materially ambiguous. Record `verified_confidence_reason_en` and the exact checks passed/failed. Preserve legacy `evidence_confidence_level` as an alias only where necessary; it does not replace these three separate fields.

Confidence **directs** the order of review and contributes only through the fixed Phase 07 decision priority in §3.6. Higher model confidence never overrides a verified E2/E3 proof or verified E0 contradiction. A reported 0.99 for `PARTIAL` means confidence in a *partial* judgment, not a high likelihood of TP. Do not extrapolate the observed `FULL` fraction to the rest of the corpus or infer statistical probabilities. The fixed model-confidence threshold for an unverified tie-break is **`>= 0.80`**, and is a declared operational best-effort rule, **not a calibrated accuracy claim**.

### 3.5 Full-population closure and proof reuse

Before external selection, and again after valid Phase 07 batch results, walk **every** R, N and effective GC, including items not selected for external review. Challenge the best original-file proof; check universal clauses, explicit cross-file conjunctions, permissions, negative wording, exceptions and exact PDF/Markdown locators. Re-examine exclusions, mixed table rows and original source context. Use a proof-family transfer only when the recipient's **eleven** dimensions have been individually checked and the proof is actually applicable. Preserve rejected transfers and reasons. Group unsupported residuals by mutually entailed affirmative meaning, and crosswalk affirmed N controls to prevent double counting.

First close all items that satisfy **verified** E3/E2 or complete E0 standards. **The external evaluator MUST invoke the mandatory deterministic best-effort fallback in §3.6 for all remaining items when the complete K handoff is valid; Phase 07 verifies the result. Do not leave a semantic `null` cell simply because proof is incomplete.** Record the candidate searched, missing/contested dimensions, proof ID if any, model confidence, evidence strength, verified confidence, decision-rule ID and `unreliable=true`. A best-effort FN is a decision under uncertainty, not a proven semantic absence. Distinguish an unresolved *proof* from an unresolved *classification*: the former may remain explicitly recorded even after the latter has been assigned a required best-effort cell.


### 3.6 Mandatory Phase 07 deterministic best-effort decision policy

**Precondition:** all original inputs/hash/role mappings are valid; all K required external results and their batch journals have passed schema and identity validation; full PDF and all eight Markdown roles have been searched in both directions; §3.5 proof transfer and duplicate checks have been attempted. Missing source files, a corrupt freeze or incomplete mandatory K handoff is `INCOMPLETE`, **not** permission to invent a result. An item not selected among K is **not** an incomplete handoff: it must be decided using its available original evidence and the policy below.

**Fixed priority (higher rows win, no stochastic selection):**

1. `D7-01_VERIFIED`: Complete original E3/E2 full predicate, or validated E0/fully audited nonassertion, wins regardless of model output. Assign the logically supported cell/category with `verification_status=VERIFIED`, `verified_confidence_level=HIGH`, `unreliable=false`.
2. `D7-02_MODEL_SUPPORTED`: Otherwise, if a valid *item-specific* LLM judgment has `model_confidence_estimate >= 0.80`, verified original quotations, `verified_confidence_level` at least `MEDIUM`, and no stronger contradictory original evidence, use that judgment **only for the proposition it actually evaluates**, with `verification_status=BEST_EFFORT` and `unreliable=true`. `FULL` maps to positive full coverage/affirmation for the item direction; `PARTIAL`, `CONTRADICTED` and `NOT_FOUND` are not full coverage. A model's `UNRESOLVED` never becomes `FULL` by threshold alone.
3. `D7-03_ORIGINAL_EVIDENCE`: Otherwise, use the best available independently inspected E1 original evidence and complete eleven-dimension comparison (including cross-file contextual candidates); select the **most substantively supported** branch in the direction-specific rules below. State exactly which dimensions remain unverified. Mark `BEST_EFFORT`, `unreliable=true`.
4. `D7-04_CONSERVATIVE_FALLBACK`: If all applicable evidence remains EU, the item has no reliable model judgment, or competing candidates cannot be ordered by the preceding rules, apply the direction-specific defaults below. Mark `verified_confidence_level=LOW`, `verification_status=BEST_EFFORT`, `unreliable=true`, and name the missing/contradictory predicates. **Never treat absent lexical retrieval alone as verified nonentailment.**

**Exhaustive, direction-specific decisions (no unresolved scoring cells):**

| Canonical unit | Verified or inspected positive criterion | Deterministic best-effort tie-break / fallback | Required final form |
|---|---|---|---|
| `R` | Source obligation fully entailed by applicable generated definitive content (`E3/E2`), or qualified `D7-02_MODEL_SUPPORTED` `FULL` with consistent inspected context | Otherwise `FN` after complete reciprocal search and predicate challenge; `PARTIAL`, `NOT_FOUND` or an unresolved conflict is **not** automatically a verified absence | Exactly one `TP` or `FN` per R; if fallback, `BEST_EFFORT` and specific uncertain predicates |
| `N` | Generated definitive affirmative statement **actually affirms** the forbidden counterfactual (`E3/E2`), or directionally qualified `D7-02_MODEL_SUPPORTED` affirmative `FULL` | Otherwise `TN` after corpus-wide polarity check. Prohibition of a counterfactual is **not** its affirmation; absence only supports a **best-effort** TN, not a verified one | Exactly one `FP` (asserted N / `B`) or `TN` per frozen N |
| Effective `GC` | PDF fully supports the complete definitive assertion (`PDF_ENTAILED`) or supports it outside frozen R (`SUPPORTED_NONCOVERING`); use original proof and directional qualified model `FULL` if applicable | If definitive content contains an identified unsupported affirmative residual after original-PDF countercheck, classify `PDF_UNSUPPORTED`. Under EU, examine the entire affirmative claim as the *candidate* residual; after the full original review, classify it **FP** as deterministic best-effort if PDF support cannot be substantiated, while preserving incomplete contrary checks. Pure nondefinitive text becomes `NONDEFINITIVE`, not FP | Every effective GC has exactly one four-cell diagnostic decision (supported claim `TP`, unsupported claim `FP`, nondefinitive abstention `TN`); do not count GC `TP/TN` as additional canonical R/N cells |

**Canonical FP consolidation:** An affirmative `PDF_UNSUPPORTED` residual is entered into `F` **once** per mutually entailed semantic predicate, unless its affirmative meaning is already counted as a frozen asserted N in `B`. A provisional candidate must have exact generated-original text and the identified unsupported clause (the **entire original assertion** may serve as the candidate clause if no narrower separable residual is defensible). E1/EU insufficient PDF proof means `BEST_EFFORT` support status, **not** a fabricated `E0` certificate. For unresolved semantic similarity, do **not** merge by score alone; preserve separate explicit predicates in deterministic original-file/line/cell order, with `merge_verification_status=BEST_EFFORT` and an overcount-risk warning. Distinct scope, API path, permission or outcome prevents merging without proven mutual entailment.

**Determinism and traceability:** Before evaluation freeze the code/rule version, original file hashes, source/GO/GC IDs, model results and source-locator sort order. Select candidate original quotes by: (i) proof grade E3/E2/E1/E0/EU as applicable to the proposed **direction**, (ii) number of inspected matching dimensions (descending), (iii) verified-confidence tier HIGH > MEDIUM > LOW, (iv) usable model confidence (descending; null last), (v) physical PDF page, original file-role order, Markdown line, table-cell index and stable item ID (ascending). If equal-strength positive and negative candidates conflict without complete proof, choose the conservative direction-specific fallback; record both. No random tie-breaks or unrecorded analyst discretion.

After the precondition passes, the **evaluator MUST emit** one closed, deterministic TP/FN disposition for each R, FP/TN for each N, and one four-cell diagnostic classification per GC; it MUST consolidate F, and Phase 07 must independently audit these outputs: `UR=UN=UG=0` at the **classification** level. Evidence verification may still be incomplete; count and disclose all `BEST_EFFORT` classifications. Never label them `VERIFIED` merely to close the ledger. A structural/input failure remains `INCOMPLETE` rather than a fabricated success. The resulting single Phase 08 score is an arithmetic **deterministic best-effort** full-ledger score when any `BEST_EFFORT` classification is present, not an independent factual certificate.

## 4. Method-specific LLM adjudication caps in 8-item batches with concurrency 4

### 4.1 Bounded, reproducible item selection

After Phase 03–06 complete source/GO/GC/N audits, first apply §3.5 to close all items with independently verified direct evidence or safe proof-family transfer. Collect the **actually remaining** pending/high-risk `R`, `N` and effective `GC` items with `unreliable: true` and/or `REVIEW_PENDING_EXTERNAL_SEQUENTIAL_LLM`, using §3.4 confidence solely for triage. This status denotes a pending individual item, not a scoring cell. Do not reopen reliable items merely to fill the cap, infer TP from a high `FULL` proportion in earlier logs, or convert remaining unresolved into negative cells. A previously resolved item may be challenged only on a documented evidence defect.

**The external atomic-adjudication item cap is method-specific, not a required item count:**

| Generation method | Method identifier | Maximum selected atomic adjudication items `L_m` | Maximum 8-item batches | Maximum submission attempts (`ceil(K / 8) + 8`) |
|---|---|---:|---:|---:|
| Full load | `fullload` | **4,096** | 512 | 520 |
| 1-level MapReduce | `onelevel` | **2,048** | 256 | 264 |
| 2-level MapReduce | `twolevel` | **2,048** | 256 | 264 |

These caps apply to **the combined selected external review of R/N/GC atomic items**, not to the frozen R/N reference counts. Let `C` be the number of distinct, defensibly pending R/N/GC IDs **after** safe full-predicate reuse and crosswalk checks. Determine `L_m` strictly from the operator-supplied, Phase-01-validated `spec_gen_method`, then select exactly `K = min(C, L_m)`; when `C < L_m`, take all C without padding; when `C = 0`, explicitly record no handoff. When `C > L_m`, retain the unselected pending item IDs and evidence-confidence levels for mandatory post-handoff reconciliation under §3.5; never assume the reviewed items resolve the unselected remainder automatically.

When truncation is required, allocate method-specific limits for **highest-risk/lowest-evidence-confidence items**, **distinct proof-family representatives**, and **PDF-digest-seeded stratified items**, respectively: **`fullload`: 2,048 / 1,024 / 1,024**; **`onelevel` and `twolevel`: 1,024 / 512 / 512**. Transfer unused slots deterministically without replacement. Seed with PDF SHA-256 + selected method + protocol `10.5`; break ties by stable item ID. For `C ≤ L_m`, include all C in reproducible risk/family/seed order without artificial quotas. Preserve R/N/G, substantive table, PDF-section, and eight-file coverage where eligible items permit. Favor independent proofs and reuse reach rather than raw lexical duplicates; document risk, evidence-confidence, family, potential recipients, and selection reason. Never select to obtain favorable score rates.

Commit the ordered, SHA-256-hashed **new v10.5** Phase 06 queue before receiving model results, using one `LLM_QUEUE_ITEM` per independent selected item and an optional non-scoring `PHASE_SUMMARY`. Required fields: `item_id`, `queue_id`, `direction` (`R`/`N`/`G`), `normalized_proposition_en` (or legacy `statement_en`), `unreliable: true`, evidence-confidence fields (§3.4), proof-family and target-reuse identifiers, original provenance/evidence hints, source digests, selection reason, and stable sequence index. `current_cell` and `scoring_cell` may be JSON `null`; pending status is `REVIEW_PENDING_EXTERNAL_SEQUENTIAL_LLM`. Accept the legacy `UNRELIABLE_ITEM` record shape for parsing old queues without rewriting or treating them as v10.5 selected records. The existing `REVIEW_PENDING_EXTERNAL_SEQUENTIAL_LLM` status is a compatibility identifier, not an instruction to execute requests sequentially.

**Mandatory v10.5 queue-to-prompt contract:** Every selected item carries its full `normalized_proposition_en` without truncation and its source-digest map, plus the applicable evidence and predicate fields by direction: R: `original_pdf_evidence`, `required_source_predicates`, `original_generated_evidence_candidates`, `unverified_source_predicates_en`; N: `original_pdf_evidence`, `required_source_predicates`, `generated_original_candidates`; G: `original_generated_evidence`, `original_pdf_evidence_candidates`, `possible_unsupported_residual_en`, `negative_control_overlap_candidates`. The evaluator must normalize these exact field names and legacy equivalents into one explicit per-item prompt object containing original filename/line, PDF physical page and quote, eleven-dimensional uncertainty and direction, with deterministic per-field evidence caps. A cap may shorten *ancillary evidence hints* but must not trim the claim, suppress all evidence, omit source SHA-256 or silently drop unrecognized source evidence fields. If a required evidence family is missing from the selected queue item, fail before API submission rather than pretending a model inspected it. Validate the nested `source_digests.pdf_sha256` and `source_digests.eight_original_spec_sha256` against all nine original files; one queue cannot mix source versions. Record a prompt-hints hash in each journal for reproducible replay.

### 4.2 API batches of 8 items, maximum concurrency 4, and independent JSON results

Partition the committed queue in immutable order into consecutive batches of at most 8 selected items; the final batch contains the actual remaining 1–7 items, if any. For `K > 0`, primary submissions are `ceil(K / 8)` (**at most 512 for `fullload`, or 256 for `onelevel`/`twolevel`**). Send one Responses API request per batch with the original PDF and all eight unchanged Markdown files as nine `input_file` references, and precisely the batch's 1–8 independent item records in one `input_text`. Upload originals once, reuse their file IDs, and run at most **4 LLM requests concurrently**. Dispatch completion order is unrestricted; identify and commit results by immutable `batch_id` and reconstruct the final decisions in queue order. Never replace independent judgments with one combined conclusion.

For every batch, require strict structured JSON as one object with `batch_id` and a `results` array containing exactly one complete, independent result per input item **in input order** and matching `item_id`, `queue_id`, and `direction`. For every G result also require a separate `generated_support_category` from `PDF_ENTAILED`, `SUPPORTED_NONCOVERING`, `PDF_UNSUPPORTED`, `NONDEFINITIVE`, or `UNRESOLVED`; R and N must use `NOT_APPLICABLE`. Require a nonempty `eligibility_reason_en` and the original affirmative unsupported clause for `PDF_UNSUPPORTED`. A G `FULL` response is not automatically a canonical `NOT_FP`, `TP`, or `SUPPORTED_NONCOVERING`: the result must specify which supported category applies, with PDF evidence and a separately checked frozen-R connection. A `NONDEFINITIVE` model eligibility or `NOT_FOUND` relation is **not** sufficient to suppress a definitive generated assertion; require original-line evidence and an explicit eligibility reason. Inconsistent relation, eligibility, category, and residual fields invalidate the whole batch or remain pending, never create a silent scored exclusion. Validate exact count, membership, uniqueness, order and mandatory fields; no joint conclusion, voting result, or accepted partial batch. Each item retains eligibility, `FULL`/`PARTIAL`/`CONTRADICTED`/`NOT_FOUND`/`UNRESOLVED`, all eleven predicate dimensions, exact PDF quotations/pages, original Markdown line quotations, alternative searches, unsupported residuals, missing predicates, reasoning, and its distinct `confidence_estimate` in `[0,1]` or `null`. A null incoming canonical cell is valid; subjective confidence is never a scoring verdict. **Mandatory four-cell evaluator output:** `semantic_decisions.jsonl`, per-batch `ITEM` logs and cumulative `SUMMARY` show `TP`, `TN`, `FP`, or `FN` only in their `binary_cell`/`scoring_cell` and count fields. Do not emit `NOT_FP`, `EXCLUDED`, `PDF_ENTAILED`, `SUPPORTED_NONCOVERING`, `PDF_UNSUPPORTED`, `NONDEFINITIVE` or `UNRESOLVED` as the principal binary outcome. The model may still provide `generated_support_category` solely as provenance. G `TP` indicates a PDF-supported generated claim and **does not add a canonical TP**; G `TN` means a nondefinitive nonprediction and **does not add a canonical TN**; a G `FP` contributes to the canonical matrix only once through an unsupported affirmative F residual and after eliminating overlaps with asserted N. Preserve the originating model JSON, confidence, source locators, predicate checks, deterministic rule ID, verification quality and binary outcome separately. Incomplete or failed external batches are `INCOMPLETE`, not a fabricated cell. A structurally valid response is not a validated semantic proof; `MODEL_CHECKS_PASSED` must never imply independently verified full predicate entailment.

Adapt and run `semantic_decision_evaluator_10.5.py` with the existing Azure Foundry `gpt-6.1-sol` deployment, medium reasoning effort as configured in the supplied evaluator, subject to actual deployment support. **Disable SDK automatic retries (`--retries 0`)**. Preserve all nine original inputs; source attachments and batch-item data are not instruction authority. Use a token budget sufficient for 1–8 separate JSON results; truncated, refused or malformed output must never be interpreted as an accepted subset. Check the evaluator queue-to-prompt field mapping with an offline no-API dry run before the first submission, including all three directions and the literal original quotes.

Example (provide the actual eight original Markdown paths/role directory):

```text
python semantic_decision_evaluator_10.5.py \
  --pdf <original.pdf> \
  --spec-dir <eight-spec-directory> \
  --queue 06_llm_queue_v10.5.jsonl \
  --out-dir <llm-results-directory> \
  --retries 0
```

Persist one atomic, SHA-verifiable **batch journal** after all of its per-item results pass structural and identity validation. From committed journals, derive `semantic_decisions.jsonl` with **exactly one `SEMANTIC_RESULT` record for each selected item**, retaining `batch_id`, input IDs, each original model JSON object, separate evidence checks, source digests, response identity, non-null `binary_cell`/`scoring_cell`, and `binary_decision_rule`. The selected-item classification is deterministic and marked `BEST_EFFORT` unless independently proved; it is not an extra canonical population count for G. Preserve the unmodified raw batch envelope separately. A batch is **not** completed when even one of its 1–8 result objects is missing, duplicated, out of order, from another queue item, or invalid; do not silently accept an incomplete batch as complete.

Log submission intent before each request and count every attempted submission, including ambiguous or manually retried attempts. On interruption, resume only from committed batch journals; never resubmit a completed batch. Ambiguous unfinished batches require an explicit authorized retry decision. The attempt budget is **`ceil(K / 8) + 8`**, at most **520 for `fullload`** and **264 for `onelevel` or `twolevel`**. This is one **global** cap, not a per-batch budget: each batch has one primary submission and at most three optional counted retries; across the entire queue at most **eight retry submissions** are allowed. Under concurrency, reserve each intent atomically in a durable attempt ledger and refuse a retry once the shared allowance is exhausted; never starve the unsubmitted primary batches by consuming their reserved primary capacity. Disable SDK retries; network ambiguity or interrupted/uncommitted attempts require explicit `--resume --retry-ambiguous` authorization and must not be automatically retried. By default `--batch-retries 0` performs no automatic resubmissions. If retrying known invalid outputs is explicitly enabled, use only the same global eight-retry allowance. Any exhausted, corrupt or incomplete handoff is `INCOMPLETE`, not success. Missing/rejected results stay `REVIEW_PENDING`, `unreliable: true`, `scoring_cell: null`; never treat a failed batch or platform limitation as success.

### 4.3 Per-item validation, family reuse and final authority

Independently validate each result's queue identity/direction, immutable digests, exact PDF quotation/page, actual Markdown file/line quotation, schema and all eleven predicate dimensions. Apply the alias-safe filename resolver in §3.1. The LLM judgment is only a proposal: `confidence_estimate` alone never forces a verified canonical cell; Phase 07 must apply the explicit, deterministic best-effort rule in §3.6 when full verification remains unavailable. A model `FULL` supports a **verified** TP only when its independent original E2/E3 proof is complete; otherwise it can affect a **best-effort** decision solely under the fixed §3.6 evidence/confidence gate. `PARTIAL`/`NOT_FOUND` requires reciprocal search before FN/TN; best-effort unsupported claims require an exact original affirmative candidate residual and a documented full-PDF countercheck, with uncertainties retained. Record evidence-confidence and model-confidence separately, including disagreement.

The evaluator must account for **all K selected IDs** and the complete unselected R/N/GC population. Once the mandatory inputs are valid, it **MUST execute §3.6 for every non-verified effective unit and classify all R/N/GC, not merely mark an uncertain remainder null**, then write the full-population `07_final_ledger.jsonl` and `07_binary_counts.json`. Phase 07 checks these outcomes rather than postponing binary conversion to a separate program. Once valid batch results arrive, **rerun §3.5 across all source and generated items**, using independently checked proof-family transfer to close unselected members; reassess missed direct matches, supported-noncovering classes, N/F overlap, and semantic FP duplicates. Record each resulting cell with its exact proof ID and full predicate audit. A reviewed representative does not automatically settle its family. No duplicate TP/FP multiplication and no contagion from one erroneous batch member. Full external handoff requires K individually valid results and the correct count and identities of committed batches; subsequent deterministic full-population closure (including all unselected IDs) is a **mandatory automatic evaluator gate**, not an optional postprocessing task. A valid handoff followed by semantic uncertainty is not grounds to skip §3.6.

Earlier v10.2, v10.3, and v10.4 queues, model responses and journals remain immutable historical evidence. A v10.5 evaluator must reject an old queue by default and must never silently resume a v10.4 state under v10.5; a distinctly labeled, explicitly authorized compatibility import, if implemented, must preserve old response and queue identities, verify every original digest and item, and must not imply that old incomplete batches were accepted. **Never relabel or silently reuse them as new v10.5 selection**. A new v10.5 selection requires a separately committed, immutable queue and manifest from its actual pending population. There is no obligation to pad to the method-specific limit (4,096 or 2,048), and no claim that the limit alone guarantees full-population closure.

### 4.4 Mandatory evaluator-produced final four-cell ledger

`semantic_decision_evaluator_10.5.py` is responsible for BOTH the K individual LLM adjudications and automatic deterministic best-effort closure over all effective R/N/GC after the final committed batch. `--phase-dir` identifies the immutable Phase 01-06 ledgers and frozen R/N reference and defaults to the directory of `--queue`. Missing ledgers, incomplete K results, changed SHA-256 identities, missing source evidence or corrupted journals cause a real `INCOMPLETE` error. `--skip-full-population-closure` is a narrowly scoped diagnostic option and must not be used for an officially completed evaluation.

**Every completed item has one primary `binary_cell` and `scoring_cell` drawn strictly from `TP`, `TN`, `FP`, `FN`.** Keep the model's richer directional evidence and source-support category in secondary provenance fields, NEVER as the final displayed outcome. The deterministic direction-specific rules are:

| Direction | Four-cell mapping | Actual canonical counting |
|---|---|---|
| `R` frozen source-positive | Complete verified/qualified full coverage: `TP`; otherwise `FN` after original reciprocal challenge; keep best-effort uncertainty | One `TP` or `FN` for each frozen R |
| `N` frozen negative control | Proven/qualified affirmation of the forbidden positive counterfactual: `FP`; otherwise `TN`; negated prohibitions are not affirmation | One `FP` or `TN` for each frozen N |
| `G` definitive generated class supported by PDF | Diagnostic `TP` (irrespective of whether it covers a frozen R) | **No additional canonical TP**; R coverage already counts source units |
| `G` definitive generated class unsupported by PDF | Diagnostic `FP`; record the exact affirmative residual, original locator and PDF countercheck | **One `FINAL_RESIDUAL` FP per distinct residual**, excluding any already counted asserted N |
| `G` nondefinitive-only claim | Diagnostic `TN`, with original quote and reason it is not an affirmative prediction | **No additional canonical TN**; frozen N controls supply TN units |
| `G` eligible but evidence unresolved | Deterministic `FP` best effort when PDF support is not substantiated after reciprocal examination; disclose the whole affirmative residual and `unreliable=true` | Candidate residual deduplicated and checked against N; never claim E0 verified evidence solely from absence |

**No `NOT_FP` / `EXCLUDED` / `UNRESOLVED` in the final decision field.** G claim provenance may continue to record `PDF_ENTAILED`, `SUPPORTED_NONCOVERING`, `PDF_UNSUPPORTED`, or `NONDEFINITIVE` internally; these are not output scoring cells. All confirmed and best-effort decisions retain distinct `model_confidence_estimate`, ordinal `evidence_strength`, `verified_confidence_level`, provenance, decision rule and unreliability. In case of a rare ill-formed mixed/ambiguous proposition, the evaluator must apply the explicit fallback without making it a verified factual conclusion.

The evaluator writes **`semantic_decisions.jsonl`**, **`07_final_ledger.jsonl`** and **`07_binary_counts.json`**, prints the single full-population `TP`, `TN`, `FP`, `FN` count quartet, and records Precision/Recall/F1 as arithmetic of those canonical units with `METRICS_DETERMINISTIC_BEST_EFFORT` if unverified predicates remain. All `FINAL_CLASS` rows also receive four-cell *diagnostic* labels but have `included_in_confusion_matrix=false`, preventing multiplication of true positives or true negatives by repeated specifications. Only R, N and the deduplicated F residual records enter the canonical confusion matrix. Phase 07 independently checks original evidence and the ledger, and Phase 08 independently recomputes the same arithmetic. This is a binary evaluation protocol, not a requirement that every generated GC count as a new TP.

**Existing run protection:** a change to the four-cell decision rules changes the journal `binary_rule_version`, and existing journals without the matching value are rejected rather than quietly reinterpreted. Keep old v10.4/v10.5 run folders intact; use a fresh result directory when changing scoring rules. Do not run time-consuming script tests unless the operator explicitly requests them.

## 5. Canonical scoring universe and independently computed metrics

### 5.1 Scoring units (one consistent binary universe)

For each evaluated method `m`, define:

```text
R_m = R  : fixed PDF-positive normative source atoms
N_m = N  : fixed predeclared PDF-negative counterfactual controls
GO_m     : eligible definitive generated occurrences
GC_m     : raw distinct definitive generated semantic classes
A_m      : {r in R : the entire generated corpus fully entails r}
B_m      : {n in N : the definitive generated corpus affirms n}
F_m      : mutually distinct unsupported generated-only affirmative propositions,
           after exact residual separation and semantic consolidation, excluding
           every proposition already counted as an asserted N control in B_m
U_m      : R disjoint_union N disjoint_union F_m
P_m      : A_m union B_m union F_m
```

Source-positive atoms are the actual-positive units. Fixed N controls and unique generated-only unsupported residuals are actual-negative units. A genuine unsupported G residual has predicted positive and counts once as FP; a supported generated class does **not** create an additional TP unless its evidence covers a previously retained R atom. A generated class can cover multiple distinct R atoms through proven applicability. Raw `|GC|` is therefore **not** the canonical predicted-positive count.

Each `r` in R has one `FINAL_SOURCE` record with **exactly one** TP (actual=1, predicted=1) or FN (actual=1, predicted=0), and each `n` in N has one `FINAL_CONTROL` record with **exactly one** FP (actual=0, predicted=1) or TN (actual=0, predicted=0) after a completed Phase 07. These classifications can be `VERIFIED` or `BEST_EFFORT`, but never null after a valid handoff. Each distinct f in F has one `FINAL_RESIDUAL` record (actual=0, predicted=1), linked back to all supporting GCs. Every effective GC has exactly one `FINAL_CLASS` classification; supported classes are validity ledger rows, not extra canonical score units. Before Phase 07, unresolved candidate residuals are **not** counted as known F or zero F. After a valid Phase 07, §3.6 deterministically closes all eligible generated-only residuals and their N/F crosswalk, with `BEST_EFFORT` flagged when proof remains incomplete.

### 5.2 Confirmed four-cell definitions and equations

| Cell | Actual | Predicted | Evidence-grounded meaning |
|---|---:|---:|---|
| `TP` | 1 | 1 | Complete PDF-positive obligation covered by definitive generated commitments |
| `FN` | 1 | 0 | PDF-positive obligation demonstrably missing or only partially covered after reciprocal challenge |
| `FP` | 0 | 1 | Affirmed fixed PDF-negative control or one unique PDF-unsupported generated-only residual |
| `TN` | 0 | 0 | Fixed PDF-negative counterfactual not affirmed by definitive generated commitments |

For a **fully classified canonical universe** (verification quality is separately audited):

```text
TP = |A_m|
FN = |R| - |A_m|
TN = |N| - |B_m|
FP = |B_m| + |F_m|

|U_m| = |R| + |N| + |F_m|
|P_m| = |A_m| + |B_m| + |F_m| = TP + FP
TP + FN = |R|
TN + |B_m| = |N|
FP - |B_m| = |F_m|
TP + TN + FP + FN = |U_m|
TP + FP != |GC_m| in general; no equality is required.
```

**Never add a generated assertion of an N counterfactual to F as well.** An unsupported generated residual shared by seven or eight files still contributes one F after full semantic consolidation, not seven or eight FPs. Different independently testable unauthorized permissions or outcomes remain distinct residuals.

### 5.3 Precision, Recall, F1, and diagnostic rates

Compute one set of full-population metrics from **all enumerated final canonical decisions** after Phase 07, never from manually supplied totals, raw GO/GC counts, retrieval candidates or model votes alone. Report `VERIFIED` only if all contributing decisions are verified; otherwise attach `METRICS_DETERMINISTIC_BEST_EFFORT` and the exact number of best-effort units. These are **not** statistical estimates or ground-truth guarantees:

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN) = TP / |R|
F1        = 2 * TP / (2 * TP + FP + FN)

R_coverage_rate           = TP / |R|                   # equals Recall when fully resolved
negative_control_pass_rate = TN / |N|                  # bounded diagnostic only
GC_validity_rate          = PDF_supported_GC / definitive_GC
raw_duplicate_rate        = (|GO_m| - |GC_m|) / |GO_m|
```

`PDF_supported_GC` includes definitive classes classified `PDF_ENTAILED` and `SUPPORTED_NONCOVERING` under the same final decision-quality rules; nondefinitive and unsupported classes are excluded from its numerator. Interim rates in Phases 01–06 are `null` while source/control/classification populations remain unresolved. After valid Phase 07 deterministic closure, all units have one final category and a documented decision-quality tier, so full-ledger metrics are numeric subject only to zero-denominator rules. Clearly identify the denominator of every diagnostic rate. `negative_control_pass_rate` is **not** true-negative population accuracy and does not enter Precision/Recall/F1 other than through the genuine FP count when a negative control is affirmed. Do not derive per-file source Recall by copying globally satisfied R atoms to each file; any file attribution is separately defined evidence contribution, not overall coverage.

Zero-denominator handling: return JSON `null` for Precision when `TP+FP=0`, Recall when `|R|=0`, the negative-control rate when `|N|=0`, GC-validity rate when its definitive denominator is zero, and duplicate rate when `|GO|=0`. Return F1 as `null` when `2TP+FP+FN=0`, otherwise its exact fraction (including `0` where appropriate). Store native numeric values, not rounded strings; reports may format a separately specified number of decimal places without changing underlying values.

### 5.4 Interim unresolved units and mandatory Phase 07 classification closure

Before Phase 07, retain `UR`, `UN`, `UG` as explicitly unresolved R, N and GC populations and enforce the partial-state invariants:

```text
TP_verified + FN_verified + UR = |R|
TN_verified + B_verified + UN = |N|
FP_verified = B_verified + F_verified
UG is unresolved, not assumed zero or FP before Phase 07.
```

After the **valid Phase 07 external handoff** and all-population reciprocal audit, **apply §3.6 without exception to each remaining semantic uncertainty**. `UR = UN = UG = 0` is then mandatory for **classification** (not a claim of unanimous verified proof). Every R belongs to TP/FN, every N belongs to asserted-N FP/TN, every definitive GC has a supported/unsupported category and every unsupported residual has a unique, deduplicated `F` identity. If original inputs, queue results, digests or batch journals are invalid/missing, report `INCOMPLETE` rather than fabricate a score.

All final decisions have `decision_quality = VERIFIED | BEST_EFFORT`. Record `model_confidence_estimate`, `evidence_strength`, `verified_confidence_level`, the rule ID, supported/unsupported clause, original locators and specific unresolved proof dimensions. A best-effort item is **classified** even though evidence uncertainty is preserved in `unreliable=true`. The canonical arithmetic equations in §5.2 must reconcile over **every** final classification. Confidence is **never** a score weight or an accuracy estimate.

**One metric set:** Phase 08 always computes numeric Precision/Recall/F1 from the closed deterministic ledger (except mathematically undefined zero denominators). If all contributing cells and residual merges are independently verified, status is `METRICS_VERIFIED`; otherwise status is `METRICS_DETERMINISTIC_BEST_EFFORT`. The latter is a complete arithmetic score over best-effort labels, **not a statistically estimated score, confidence bound, or claim of verified correctness**. Report the count of `BEST_EFFORT` decisions and evidence defects. Never issue a second estimated score or pretend a model confidence value is a measured accuracy probability.

### 5.5 Duplicate metrics, independent of correctness

For raw within-method semantic classes:

```text
eligible_occurrences = |GO_m|
unique_classes = |GC_m|
excess_duplicate_occurrences = eligible_occurrences - unique_classes
Duplicate = excess_duplicate_occurrences / eligible_occurrences
repeated_class_count = number of classes with >= 2 original occurrences
```

Choose each class's representative by original input-file order, physical line, then table cell. Label every excess occurrence `within_file` if a preceding occurrence of the same class is in that file; otherwise label `across_file`. Check:

```text
within_file_excess + across_file_excess = excess_duplicate_occurrences
```

Report cross-file repeated-class count separately. Keep `EXPECTED_REUSE` (legitimate parallel coverage) distinct from `REDUNDANT_DUPLICATE` (unnecessary repetition); both are excess occurrences for the raw duplication metric. Do not multiply TP or FP by repeated occurrences. Never use the source-matched count, evidence-bridge count, or unsupported residual count as the raw GC denominator.

### 5.6 Required metric views and error analysis

`08_metrics.json` and the report must separately present:

1. Source reference counts `|R|`, `|N|`, their SHA-256 and freeze status; generated `|GO|`, `|GC|`, raw duplicates, and all recovered occurrences/classes.
2. Final deterministic `TP`, `FN`, `TN`, asserted-N `B`, unique generated-only `F`, and `FP`, with `VERIFIED` versus `BEST_EFFORT` counts; pre-Phase-07 `UR`, `UN`, `UG` and final zero-classification-unresolved check.
3. A **single** numeric full-ledger Precision/Recall/F1 set after valid Phase 07 deterministic closure, with `METRICS_VERIFIED` or `METRICS_DETERMINISTIC_BEST_EFFORT`, plus raw Duplicate, GC validity and bounded N-pass rate; do not produce a statistical estimate.
4. FN-root-cause counts `TRUE_MISSING`, `PARTIAL_ENTAILMENT`, `MATCHER_FALSE_NEGATIVE_CORRECTED`, and `CONSERVATIVE_UNRESOLVED`, with cited strongest generated candidates.
5. TP evidence quality: counts of `E3`, `E2`, incomplete proof, direct-identifier exceptions, and verified universal/conditional/conjunctive bridges; reference exceptions do not silently reduce R.
6. FP provenance: asserted N controls, distinct generated-only residual classes, all original G evidence locators, scope differences, duplicate-cluster decisions and PDF contrary checks. Include a separate list of `SUPPORTED_NONCOVERING` GCs.
7. LLM audit: K distinct selected pending IDs (K ≤ L_m, where `L_m = 4096` for `fullload` and `2048` for `onelevel`/`twolevel`), the immutable queue SHA-256, exact `ceil(K/8)` batches (maximum concurrency 4), individual model-confidence values and evidence-confidence assessments, verified quotations, response/attempt journals (at most `ceil(K/8)+8` submissions), disagreements, pending items and individually checked proof-family transfer recipients.
8. Per-file descriptive GO/GC occurrence and duplication totals (counting each original occurrence once), optional chapter/requirement-family coverage diagnostics with exact denominators, and cross-method comparisons only over identically frozen R/N.
9. Input/evidence validity flags, three separate confidence measures (not estimated accuracy), original proof reuse and rejection counts, unsupported residual ambiguities, benchmark atomization exceptions, high-risk `BEST_EFFORT` items, and limitations of the final arithmetic scores.

Never call a high Recall, a low FP count, or a structurally balanced confusion matrix proof of specification correctness without corresponding semantic evidence.

## 6. Eight ordered phases

Each phase must finish its entire specified non-LLM population within the current response. Only the external K-item/ceiling(K/8)-batch handoff is performed between Phase 06 and Phase 07; it is not a ninth phase. Each principal JSONL includes one `PHASE_SUMMARY` record (excluded from item counts) with totals, status, reliability counts, evidence problems, exact input digests, and unresolved limits.

| Phase | Required work | Output artifacts | Completion gate |
|---|---|---|---|
| **01 — Reference lock** | Validate and record the explicitly operator-supplied `spec_gen_method` (`fullload`, `onelevel`, or `twolevel`); verify original PDF identity, 90 pages, evidence images/tables, frozen R/N hashes and IDs; if no frozen reference, independently construct and lock before generated inspection. Record immutable source digests and reference exceptions. | `01_reference_lock.json`; construction-mode R/N files only when necessary | Exactly one valid manual `spec_gen_method`, stable verified benchmark, and all eight scored inputs identified; missing/invalid method or reference blockers cannot advance |
| **02 — Complete GO/GC extraction** | Scan every substantive Markdown paragraph/table row and all actual cells with inherited context. Produce definitive complete GO, GC, exclusions, duplicate classification, and original-text index. | `02_generated_atoms_final.jsonl`, `02_generated_classes_final.jsonl`, `02_excluded_units.jsonl`, `02_duplicate_classes.jsonl`, `02_original_text_index.jsonl` | All substantive regions accounted for; every GO in exactly one GC; duplicate arithmetic reconciles |
| **03 — Full R initial coverage** | For every R, use direct/contextual/universal/conjunctive search across the full corpus, record actual PDF/Markdown candidates and complete predicates, and flag extraction gaps. | `03_source_coverage.jsonl`, `03_semantic_coverage_bridges.jsonl` | Exactly one provisional, evidence-linked R status per source atom |
| **04 — Reciprocal FN and TP audit** | Challenge **every** initial FN using both directions; audit **every** provisional TP predicate-by-predicate; identify false misses, partial obligations, reference exceptions and recovery opportunities. Preserve earlier records; add effective audited states. | `04_fn_root_cause_audit.jsonl`, `04_tp_evidence_audit.jsonl`, `04_coverage_audit.jsonl` | Entire R partition reconciled, all preliminary TP proofs inspected, no FN from retrieval absence alone |
| **05 — Full generated validity** | Re-examine **all substantive exclusions** for missed assertions; recover valid GO/GC; evaluate every effective definitive GC against original PDF, including supported-noncovering claims, unsupported residuals and explicit uncertainty. | `05_generated_claim_validity.jsonl`, `05_exclusion_reassessment.jsonl` | Every exclusion and effective GC accounted for; no unmatched-GC-to-FP shortcut |
| **06 — N controls, FP consolidation, and method-specific LLM queue** | Audit all N and definitive GC residuals; identify and reuse independently verified proof families before selection; assess evidence-confidence and N/F duplicates; select **K = min(actual eligible pending items, L_m)** (`L_m`: 4,096 `fullload`; 2,048 `onelevel`/`twolevel`) without padding, freeze ordered queue and batch boundaries, retain unselected pending IDs for post-handoff closure. | `06_fp_controls.jsonl`, `06_llm_queue_v10.5.jsonl`, `06_queue_selection.json` | All N/GC statuses, confidence assessments and safe proof transfers are recorded; no FP double count; selection and 1–8 item batches are immutable |
| **07 — Four-cell closure and evidence audit** | Validate evaluator-produced K item results, `07_final_ledger.jsonl` and `07_binary_counts.json`; independently challenge all selected/unselected R/N/GC and FP residual grouping, repair issues by traceable supersession only and preserve four-cell canonical totals. | **Evaluator inputs/outputs:** `semantic_decisions.jsonl`, batch journals, `07_final_ledger.jsonl`, `07_binary_counts.json`. **Phase audit:** `07_llm_review.jsonl`, `07_duplicate_metrics.json` | Correct K/batch validation or genuine `INCOMPLETE`; if valid, **all canonical classifications are non-null**, with `VERIFIED` or `BEST_EFFORT` quality and inspectable rule/evidence records |
| **08 — Deterministic canonical metrics and delivery** | Reconstruct effective Phase 01–07 classifications, verify R/N/GC/F and duplicate accounting; compute **one numeric** full-ledger Precision, Recall and F1 from Phase 07 closed labels, assigning `METRICS_VERIFIED` only when all proofs are verified and otherwise `METRICS_DETERMINISTIC_BEST_EFFORT`. No statistical substitutes or confidence weighting. | `compute_metrics.py`, `08_metrics.json`, `08_report.md`, `08_coverage_and_limitations.md` | Independent arithmetic passes, all valid Phase 07 labels are non-null, all best-effort evidence limits are disclosed, and no fabricated verified claim or duplicate count appears |

**Operational handoff:** Phase 06 delivers a newly hashed immutable `06_llm_queue_v10.5.jsonl` with the actual pending selection, never padded to the method-specific limit. The external evaluator returns K independently identified judgments in 8-item batches with up to 4 concurrent requests; once all are committed it automatically produces the canonical full-population four-cell ledger and count summary. The operator supplies these outputs, batch journals and attempt ledger for independent Phase 07 checking. The evaluator must preserve old v10.4 output directories and journals byte-for-byte; a v10.5 run requires a separately frozen queue, new queue SHA and a fresh output directory. A fresh v10.5 run is not a resume of a v10.4 run. Existing v10.4 results may be inspected read-only for recovery planning, but may not silently be promoted to accepted v10.5 item judgments. The evaluator must **deterministically best-effort classify every canonical unit** through individual verified proofs, validated reuse, and the obligatory §3.6 fallback for residual ambiguities; Phase 07 then validates that complete closure. Missing Azure records are not missing requirements. Preserve all earlier phase/legacy queue bytes; authorized retries count as attempts, and incomplete external batches block advancement.

## 7. Item-level record and validation contracts

### 7.1 Required final record kinds

The evaluator-generated `07_final_ledger.jsonl` must contain exactly one `FINAL_SOURCE` per frozen R ID, one `FINAL_CONTROL` per frozen N ID, one diagnostic `FINAL_CLASS` per raw GC ID (including recovered/nondefinitive classes), and one canonical `FINAL_RESIDUAL` per unique generated-only unsupported proposition. Before Phase 07 any unresolved potential residual is a `RESIDUAL_CANDIDATE`; completed Phase 07 **must resolve it into a final supported/unsupported/nondefinitive category**, with explicit `BEST_EFFORT` quality if unsupportedness remains incompletely proven, rather than leaving an unclassified scoring unit. Each record carries stable ID, method, original input digests, PDF and generated locators, non-null final classification, `decision_quality`, `decision_rule_id`, `model_confidence_estimate`, `evidence_strength`, `verified_confidence_level`, `unreliable`, `unreliable_reason_en`, adjudication provenance, and links to prior superseded records if relevant. `PHASE_SUMMARY` is excluded from canonical counts.

Verified TP records must include a complete predicate-check map and source-to-generated evidence bridge with a `TP_AUDIT` reference. Best-effort TP records must instead document the examined predicate dimensions, verified original locator(s), the §3.6 rule ID and the specific unverified parts; they cannot masquerade as fully proved TP. Every FN includes an inspected strongest candidate, exact missing or uncertain predicates, reciprocal search receipt, and `fn_review_disposition`; a best-effort FN must not be labeled `TRUE_MISSING` without proof. Confirmed FP residuals include the exact unsupported affirmative predicate and PDF search/contrary evidence; TN records identify the frozen negative control, relevant generated evidence checks, and nonassertion justification. Each effective GC records one **final** four-cell diagnostic status `TP`, `TN`, or `FP` (never extra R TP / N TN); PDF-support categories are retained only as explanatory provenance; for ambiguous mixed claims split only independently meaningful parts and retain links.

A model result is linked by selected queue ID and source digest, with reported and resolved filename aliases, verified page/line quotations, final reviewer decision, exact residual/bridge, and `REVIEW_PENDING` if incomplete. Prior cells in an external evaluator's `current_cell` field may be null and are provisional labels only, **never** final outcomes or metric inputs. `REVIEW_PENDING_EXTERNAL_SEQUENTIAL_LLM` and `unreliable: true` both denote eligible pending model-review items; neither is a scoring cell. Each final item links to its `batch_id` and single per-item JSON result.

### 7.2 Example final source unit (schema illustration only)

```json
{
  "record_type": "FINAL_SOURCE",
  "source_id": "PDF-EXAMPLE",
  "method": "fullload",
  "scoring_cell": "FN",
  "decision_quality": "BEST_EFFORT",
  "decision_rule_id": "D7-04_CONSERVATIVE_FALLBACK",
  "model_confidence_estimate": null,
  "evidence_strength": "EU",
  "verified_confidence_level": "LOW",
  "verification_status": "BEST_EFFORT",
  "unreliable": true,
  "unreliable_reason_en": "Whole-predicate support remains uncertain after reciprocal search; FN is the deterministic fallback, not verified absence.",
  "entailment_grade": "EU",
  "coverage_mode": null,
  "pdf_evidence": [],
  "generated_evidence": [],
  "predicate_checks": [],
  "adjudication_status": "DETERMINISTIC_BEST_EFFORT_CLASSIFIED",
  "prior_record_ids": [],
  "llm_item_id": null
}
```

This is **a schema illustration, not an actual finding**; all executed IDs, quotations, locators, search receipts and evidence assessments must come from originals. A low-confidence best-effort FN may be assigned by §3.6, but an empty evidence array in this illustration is **not** sufficient production audit evidence or verified nonentailment.

### 7.3 LLM-result acceptance

Accept each external decision only after checking: selected queue membership and uniqueness; batch ID and exact 1–8 per-item result count/order; expected direction and exact PDF/input digests; individual response completeness; original PDF page and literal quote; actual Markdown original line range and literal quote under unambiguous filename normalization; independently supported/contradicted predicate checks for each item; committed batch-journal identity; and an explicit documented final disposition. Store raw model JSON unchanged alongside the reviewer's evidence-grounded final assessment. Do not equate a model's numeric confidence to a probability of correctness. After accepting the item result, Phase 07 **MUST** apply §3.6 across the complete R/N/GC universe, including unselected IDs; classify all effective units deterministically and annotate best-effort judgments with missing proof conditions.

## 8. Independent metric recomputation (mandatory Phase 08 implementation)

`compute_metrics.py` must implement and **fail fast** on the following in order:

1. **Load sources:** Open frozen R/N/reference manifest, original PDF identity record, original scored file digests, and every required Phase 01–07 JSON/JSONL artifact. Strictly parse each row; exclude summaries and non-scoring audit markers from units.
2. **Recheck identity:** SHA-256 of frozen R/N/PDF and the eight source files, 90 physical pages, exact role mapping, version, the unchanged operator-supplied `spec_gen_method` validated in Phase 01, and all fixed evidence locators. Mismatch is fatal; missing mandatory evidence is not E0.
3. **Reconstruct effective IDs:** Apply recorded item-level supersession in chronological phase order without editing immutable files. Check there is one current R, N, GC and supported residual-candidate status. No missing/duplicate IDs; all recovered GO map to exactly one effective GC.
4. **Check extraction scope:** Verify every substantive Markdown region and Phase 02 exclusion was assessed, with original source/line/table context and Phase 05 disposition. Verify all recovered assertions and class merges retain actual original passages.
5. **Check coverage:** All final R have non-null TP/FN; verified TP claims have full PDF/generated evidence and eleven dimensions; verified FN claims have full-corpus reciprocal proof and exact `TRUE_MISSING` or `PARTIAL_ENTAILMENT`. Best-effort R decisions instead carry §3.6 rule IDs, original locators, challenged candidates, missing dimensions and `unreliable=true`; never assert verified absence from a weak search. Direct, complete verified TP mismarked FN is a hard error.
6. **Check generated validity:** Every effective GC has exactly one non-`UNRESOLVED` final category. Verified `PDF_UNSUPPORTED` cites proven residual; **best-effort** `PDF_UNSUPPORTED` cites the exact candidate affirmative residual and full-PDF countercheck attempt with uncertainties, marked `unreliable=true` rather than invented E0. Supported-noncovering claims require a traceable PDF connection. Exclusions remain audited; do not silently suppress definitive assertions.
7. **Check negative controls:** Exactly one non-null FP/TN for each frozen N, verified or best effort. Asserted N controls contribute one FP each. Validate polarity, full original search receipts, N-to-F crosswalk, and no duplicate between B/F; count unsupported residual classes once using §3.6 deterministic merge policy with any uncertain separation flagged.
8. **Check external audit:** Verify SHA-locked K unique pending IDs with `0 ≤ K ≤ L_m` (`L_m = 4096` for `fullload`; `2048` for `onelevel`/`twolevel`), pre-selection evidence-confidence, reproducible proof-family/risk/stratified priority and no padding. Require `ceil(K/8)` committed batches and exactly one valid JSON result per item, nine original file references, identities/order, individual original quotations and all predicate dimensions. Verify submission intents and authorized retries; at most `ceil(K/8)+8` attempts (**520 maximum for `fullload`; 264 for `onelevel`/`twolevel`**). Legacy v10.2/v10.3/v10.4 queues and committed journals remain distinct immutable evidence, never misrepresented as v10.5 selection.
9. **Check mandatory deterministic closure:** After full reassessment, require non-null final TP/FN for every R and FP/TN for every N, and one final GC category with complete F grouping. Assert `UR=UN=UG=0` **for classification** after a valid handoff; distinguish `BEST_EFFORT` evidence uncertainty from an unclassified cell. Check each `D7-*` branch, priority and deterministic tie-break, the three separate confidence values, every proof transfer, and all §5.2 identities including `|U|=TP+TN+FP+FN`. Confidence is not a metric weight.
10. **Calculate one set of counts and rates:** Enumerate all final canonical IDs; calculate Precision, Recall, F1, raw Duplicate, per-file duplicates, GC validity and bounded N-pass with §5.3 denominators and zero-denominator rules. Set `METRICS_VERIFIED` only if all contributing proof/merges are verified; otherwise set `METRICS_DETERMINISTIC_BEST_EFFORT`, reporting best-effort counts and no second or statistical score. Never force `TP+FP=|GC|`.
11. **Cross-check report:** Compare all JSON totals/rates to the Markdown report. Require correct final metric status, unresolved counts, risk/source anomalies, supported-noncovering claims, FP canonicalization evidence, and transparent distinction between structural and semantic certification.
12. **Cross-method fairness:** When evaluating multiple methods, require same original PDF, R/N bytes, eligibility and adjudication policy. Recompute each method's independent GO/GC/F and canonical cells. Compare only like-named and like-defined metrics, not raw GC and canonical predicted positives interchangeably.

`compute_metrics.py` must fail fast on genuine structural/input/mandatory-handoff violations and must not fabricate **verified** Precision, Recall or F1. With a valid Phase 07 closure, **compute one numerical full-ledger Precision/Recall/F1** from required best-effort canonical cells even when some proof uncertainties remain; use `METRICS_DETERMINISTIC_BEST_EFFORT` and disclose those units. No statistical sample estimate, confidence-weighted score, multiple competing scores or hidden omission is permitted. If the mandatory handoff/source gate is genuinely `INCOMPLETE`, do not present a finished score.

## 9. Completion statuses and reporting boundaries

- `PHASE_COMPLETED_VERIFIED`: the phase's input, population, integrity and mandated evidence checks are complete; this does not assert independent semantic certification.
- `PHASE_COMPLETED_BEST_EFFORT`: complete per-item processing, with specified unresolved semantic judgments and evidence limits.
- `INCOMPLETE`: required phase records, a mandatory original file, the selected K-result, batch-journal handoff, or another essential processing step is missing.
- `BLOCKED_REFERENCE` / `INVALID_REFERENCE_CHANGED`: original source or required frozen benchmark identity/checksum failure; cannot advance or silently replace it.
- `FINAL_VERIFIED`: all eight phases complete, exact canonical unit accounting, full evidence, independent recomputation, no unresolved scored units or material known evidence defect.
- `FINAL_BEST_EFFORT`: required inputs and handoff valid; **every R/N/GC and residual is deterministically classified**, all canonical identities reconcile, but some decisions lack independently complete semantic proof. One arithmetic Precision/Recall/F1 set is reported with `METRICS_DETERMINISTIC_BEST_EFFORT` and detailed uncertainty, **not null and not mislabeled verified**.

The final report must state that measures evaluate generated design specifications against the fictional PDF baseline, not implementation correctness, operational performance or generalized model accuracy. The K individually reviewed items support `METRICS_VERIFIED` **only when** every scored item, including unselected R/N/GC and F residuals, is independently verified. Otherwise, after valid Phase 07 §3.6 deterministic closure, the **one** reported arithmetic score has `METRICS_DETERMINISTIC_BEST_EFFORT` status and explicit item-level low-confidence limitations. Preserve frozen R/N, original evidence, separate model/evidence confidence, canonical TP/FN/FP/TN accounting and semantic duplicates. Never report statistical estimates of these metrics.
