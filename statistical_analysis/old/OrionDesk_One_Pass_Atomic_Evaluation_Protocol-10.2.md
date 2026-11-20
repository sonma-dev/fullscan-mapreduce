# OrionDesk AI — Eight-Phase Evidence-Grounded Atomic Requirement Evaluation Protocol

**Protocol version:** 10.2  
**Purpose:** Evaluate eight generated design specifications against one authoritative PDF using a frozen benchmark, complete bidirectional evidence accounting, and a fixed **192 sequential, requirement-level LLM adjudications**.  
**Method:** Evidence-first differential evaluation with full-population ledgers, proof reuse only where valid, targeted original-file LLM adjudication, and independently recomputed canonical four-cell metrics.  
**Supported methods:** `fullload`, `onelevel`, `twolevel`.  
**Execution:** Exactly eight ordered phases; one phase per operator request and response. Finish the current phase before advancing.  
**Language:** Follow the operator's language for conversation. **All authored artifacts, script text, record values written as prose, and reports must be in English.**  
**Delivery:** Individual phase outputs. No archive or separate revision-history artifact unless explicitly requested.

## 1. Governing rules

1. **Source authority.** The original 90-physical-page *OrionDesk AI Detailed Application Design Specification* PDF alone determines source requirements, exclusions, and meaning. Generated specifications, model answers, historical scores, and prior ledgers are evidence or candidate predictions, not independent PDF authority. Inspect all pages, figures, tables, appendices, captions, and substantive generated text.
2. **Frozen reference.** When `common_atomic_reqs.jsonl`, `common_negative_controls.jsonl`, and `reference_freeze.json` are supplied, frozen-benchmark mode is mandatory. Verify identity, pages, SHA-256, ID uniqueness, references, and readable evidence; do not alter the reference bytes or denominator. In the absence of a frozen reference, construct and freeze `R` and `N` independently from the PDF in Phase 01 before any generated inspection. Never silently replace an invalid supplied benchmark.
3. **Complete populations, selective LLM.** Process every source-positive requirement `R`, fixed negative control `N`, substantive generated occurrence `GO`, and generated semantic class `GC` through reproducible extraction, indexing, evidence matching, or an explicit unresolved judgment. **The 192 LLM calls are an adjudication subset, not an excuse to omit the other items.**
4. **Actual logical entailment.** Full coverage requires all relevant actor, target, action, modality, scope, conditions, exceptions, time, limits, version, and outcome. A single applicable universal rule or an explicit cross-file conjunction may satisfy several independent source requirements, but produces neither duplicated generated occurrences nor additional raw classes. Exact identifiers and similarity alone are insufficient.
5. **Two distinct directions.** `R → generated` measures source coverage. `generated → PDF` measures validity of definitive generated claims. A generated statement absent from frozen `R` is not automatically unsupported; a missing retrieval hit is not a verified FN.
6. **Conservative unsupportedness.** A generated commitment is an FP candidate only when the original PDF does not normatively support its full affirmative content and the unsupported predicate is specifically identified. Search the full PDF, including governing common rules and contextual tables, before this finding. Record supporting narrower content separately.
7. **Definitive statements only.** Unadopted proposals, `TBD`, `Needs confirmation`, unresolved alternatives, examples without normative adoption, headings, bare references, and purely explanatory text are not final positive predictions. Preserve any separable definitive claim within a mixed passage, with its actual inherited context.
8. **No artificial atom multiplication.** Split only independently testable complete obligations. Never create stand-alone claims from an isolated table cell, field label, HTTP code, ID, or citation. Merge semantic duplicates only with full mutual entailment; differences in API path, role, conditions, status, version, or consequence can make claims distinct.
9. **Evidence is inspectable.** Every TP needs verified PDF and generated-original evidence and full-predicate proof. Every confirmed FN needs an audited reciprocal search and a specific missing predicate. Every FP needs its exact unsupported residual and PDF-check receipt. Every TN needs a frozen negative-control identity and verified generated nonassertion. Original filename, physical PDF page, Markdown line, table row/cell, and applicable context must be recoverable.
10. **Per-item uncertainty.** Every scored R/N and effective GC has `unreliable: true|false`, `unreliable_reason_en`, and an adjudication status. Unresolved judgments have `scoring_cell: null`. Never convert unresolved into FN, FP, or zero merely to complete a phase or a metric.
11. **No prior-result presumption.** Revisit earlier TP, TN, FP, FN and exclusions when evidence warrants. Inherited completed files are reusable as indexed evidence only after their source hashes, line locators, and relevant predicates are reverified. Earlier v10.1 labels are not v10.2 verification.
12. **Immutable, reproducible history.** Original scored documents, frozen `R/N`, and delivered phase files are immutable. Later corrections are appended as item-level supersession/adjudication records in the subsequent phase ledger. Preserve the prior ID and the effective replacement without rewriting earlier bytes. Do not create a separate revision-history document.
13. **No fabricated scores or confidence.** A successful structural check cannot certify semantic completeness. A model judgment is a proposal to be verified against original quotations. Report unresolved populations explicitly; only a closed canonical universe authorizes full-population Precision, Recall, and F1.
14. **One response, one phase.** Complete all records belonging to the requested phase or report a genuine input/platform blocker as `INCOMPLETE`. A fully enumerated phase with individually marked semantic uncertainty may be `PHASE_COMPLETED_BEST_EFFORT`. Do not start the next phase in the same turn.

## 2. Inputs, identity, and extraction

### 2.1 Required materials

- The original, readable 90-page English PDF (authoritative source).
- Exactly eight original Markdown roles, mapped unambiguously: `01_screen_functions.md`, `02_api.md` (also `02_api_.md`), `03_data.md`, `04_batch_functions.md`, `05_business_rules.md`, `06_exception_handling.md`, `07_processing_flows.md`, and `08_architecture_decision.md`.
- In frozen mode: `common_atomic_reqs.jsonl`, `common_negative_controls.jsonl`, and `reference_freeze.json` (upload-copy suffixes accepted).
- For the external adjudication step: the existing `semantic_decision_evaluator.py`, a selected 192-item JSONL queue, and returned `semantic_decisions.jsonl`.

Recognizable method prefixes and copy suffixes are permitted only with unique role mapping. Preserve actual input filenames and bytes in every evidence ledger. A normalized role name is a lookup alias, not an alteration of the source. The protocol, earlier phase ledgers, and any aggregate JSON are not ninth scored Markdown inputs.

### 2.2 Frozen checks and source-atom rules

Read each frozen JSONL record and validate the declared positive key (`requirement_id` or `source_id`) and negative key (`control_id` or `negative_control_id`), no mixed keys or duplicates, original PDF SHA-256, expected reference hashes, physical page count, and evidence quotation availability. Fail on incompatible identity/hash or inaccessible required material. Record nonfatal benchmark atomization doubts as `REFERENCE_EXCEPTION`, leaving IDs and bytes unchanged.

`R` comprises smallest independently meaningful PDF-positive normative obligations; a PDF prohibition is itself a positive duty to enforce. General obligations must not be repeated arbitrarily for each endpoint. An endpoint with a distinct method, actor, response, condition, or timing can have independent atoms. Preserve original page, quote, actor, target, condition, constraint, version, outcome, and additional supporting locations.

`N` is a fixed bounded inventory of affirmative counterfactuals explicitly prohibited, excluded, or deferred in the PDF. It is not the set of every possible absent feature. Keep `R ∩ N = ∅`. Never add method-specific controls during scoring.

### 2.3 Generated inventories

`GO` is the set of complete, eligible definitive assertion occurrences, with stable `GEN-*` ID and actual Markdown file, line, row, cell, heading, and full inherited context. `GC` is the set of unique within-method semantic classes, with stable `GCLASS-*` ID and exactly one class assignment per eligible `GO`. Every substantive source line/row must be accounted for by eligible assertions, exclusions, or inherited context; excluded prose is indexed and re-examined in Phase 05. Recovered assertions use new stable IDs and original locators without altering prior files.

## 3. Evidence-first matching and semantic judgment

### 3.1 Reusable indexing, never similarity verdicts

Index original PDF pages, all eight Markdown lines and table rows, IDs, methods/paths, event names, data fields, numeric bounds, scope terms, negation, headings, exceptions, and universal-rule subjects. Use exact and alias lookup plus optional semantic retrieval to *discover* candidates. Preserve original context and a reciprocal generated-to-PDF index. Cache validated full-predicate proofs, with their source hashes and applicable scope; reuse only after checking every target's membership, exceptions, and conditions.

A filename-alias validator must resolve an LLM-provided filename by the uniquely identified eight-file role and verified SHA-256 source mapping, then verify the quoted text in the indicated actual original line range. For example, `03_data.md` and an unambiguous uploaded `03_data(1).md` may map to the same verified role. **Do not reject an accurate quotation solely because the model used a canonical versus uploaded copy suffix.** Reject an ambiguous role, inconsistent digest, wrong original line, or mismatched quotation. Log both reported and resolved names; never silently accept a quotation from a different file.

### 3.2 Bidirectional coverage decisions

For every `r ∈ R`:

1. Reconstruct the whole normative proposition from its PDF page, section and table context.
2. Search full generated text, eligible GO/GC, common clauses, and exclusions using direct wording, synonyms, identifiers, literal values, and reverse links.
3. Test direct equivalence, logically applicable universal rules, inherited context, and explicit conjunctions across files.
4. For every proposed TP, check the whole source predicate; cite a complete proof. For a provisional FN, challenge the strongest actual nearby candidate, document precisely what is missing, and revisit it from the generated-to-source direction.
5. Resolve `TP` only on complete `E3` direct or `E2` bridged entailment; resolve `FN` only on demonstrated `TRUE_MISSING` or `PARTIAL_ENTAILMENT` after reciprocal review. Material ambiguity remains unreliable with a null cell.

For every definitive `g ∈ GC`, independently inspect whether the PDF supports its **entire** generated commitment; label `PDF_ENTAILED`, `SUPPORTED_NONCOVERING`, `PDF_UNSUPPORTED` with exact residual, or explicit unresolved. A statement supported by the PDF but not matched to a frozen source atom is `SUPPORTED_NONCOVERING`, not FP. A generated claim may entail several R atoms without being replicated as several GCs.

For every `n ∈ N`, determine whether an eligible definitive generated assertion actually affirms the forbidden counterfactual. Affirmed means `FP` in the fixed N row; documented nonaffirmation means `TN`; evidence uncertainty means `UN`. An explicit prohibition of the forbidden behavior is not its affirmation.

### 3.3 Entailment evidence grades

| Grade | Standard | Permissible conclusion |
|---|---|---|
| `E3` | Complete direct equivalence with verified original-file proof | Full entailment |
| `E2` | Complete universal/contextual/conjunctive logical proof with verified scope | Full entailment |
| `E1` | Relevant but materially incomplete predicates | Partial only; FN or FP solely with further defensible source/corpus review |
| `E0` | Explicit contradiction or evidenced complete nonentailment | Negative finding if scope and full review are verified |
| `EU` | Important evidence/meaning unresolved | `unreliable=true`, `scoring_cell=null` |

`E2` is as valid as `E3` for a TP. Neither `E1` nor a low retrieval score automatically proves FN/FP. Direct-match exclusions, partial table rows, competing clauses, and source-atom overlap are mandatory audit flags.

## 4. Exactly 192 sequential requirement-level LLM adjudications

### 4.1 Fixed selection contract

After complete deterministic/evidence-based Phase 03–06 population processing, form a candidate pool from unresolved or high-risk `R`, `N`, and effective `GC` items; previously resolved items may be selected for independent error-detection audits. **Commit an immutable queue of exactly 192 distinct, individually identified requirement-level items** *before* the first model result is read. Each item has a unique ID, direction (`R`, `N`, or `G`), normalized proposition, original evidence hints, preliminary cell when required by the evaluator, source hash references, and selection reason.

Select by the following fixed, reproducible allocation:

- **96** highest-risk individual items: possible false FNs, false FPs, direct-match conflicts, unsupported permissions, scope/condition/exception mismatches, high-impact authorization or publication claims, and frozen reference doubts.
- **48** representatives of different unresolved semantic proof families, including universal/shared requirements and multiple-file entailment, avoiding repeated identical claims.
- **48** SHA-256-seeded stratified audit items from the remaining pool, covering R/N/G directions, eight specification roles, PDF sections, substantive table contexts, and previously resolved decisions where available.

Choose without replacement. If a stratum is exhausted, transfer its unused slots by deterministic ranked/seeded order and record the reason. Seed with the frozen PDF digest, method name, and protocol version. Rank ties by stable item ID. Do not change the committed set because early responses were favorable. If fewer than 192 distinct eligible items exist, record `INCOMPLETE` and the shortfall rather than inventing items or quietly relaxing the 192-call requirement. The selected items remain one per request, **not multi-item batches**. No item is selected merely to obtain a desired TP/FP/FN rate.

### 4.2 Sequential invocation and the existing evaluator

Use the existing original-file `semantic_decision_evaluator.py` approach, retaining its per-item structured reasoning and evidence checks. **Execute 192 sequential requirement-level LLM calls: one queue item and one Responses API request at a time, in immutable queue order. No parallelism, batch adjudication, or multi-item prompt.** Attach the authoritative original PDF **and all eight unchanged generated Markdown specifications** as nine `input_file` references on **each** request; attach only the selected individual queue record as `input_text`. Files can be uploaded once and file IDs reused. Preserve the current evaluator's evidence-rich schema and the `gpt-6.1-sol` high-reasoning configuration, subject to the deployment actually being available.

Example execution pattern (names are role-mapped to the actual original file paths):

```text
python semantic_decision_evaluator.py \
  --pdf <original.pdf> \
  --spec-dir <eight-spec-directory> \
  --queue 06_llm_queue_192.jsonl \
  --out-dir <llm-results-directory> \
  --retries 0
```

A compatible wrapper may pass eight `--spec` arguments when the input directory contains other Markdown files. Preserve sequential processing and the nine-file, one-item judgment semantics. On interruption resume from validated persisted IDs; **never submit a successfully completed item a second time**. Disable automatic SDK retries for this bounded run (`--retries 0`) and count any deliberate manual retry/resume submission against the cap. If retry attempts are needed, limit the run to **200 actual API submission attempts**, reserving at most eight beyond the primary 192; do not reduce the number of distinct target items or silently substitute unknown results. A missing result is `REVIEW_PENDING` and the external handoff remains incomplete for that item.

The required response must contain item identity and direction, definitive eligibility, `FULL`/`PARTIAL`/`CONTRADICTED`/`NOT_FOUND`/`UNRESOLVED`, actor/target/action/scope/precondition/modality/timing/limit/exception/outcome/version checks, exact PDF page quotations, actual Markdown file/line quotations, missing/unsupported predicates, checked contrary evidence, justification, and source digests. Preserve the original evaluator's structured JSON and per-result metadata. Numeric confidence may rank manual scrutiny but never force a cell. Model `FULL` is not a verified TP until quotations and all predicates are checked; model `NOT_FOUND` alone does not prove complete absence.

### 4.3 Validation, family reuse, and final authority

Verify the returned schema, queue ID, direction, source hashes, PDF quotation/page and generated quotation/line using the alias-safe resolver in §3.1. Review the original passages and the complete predicate test. Record the final defensible decision, or retain an explicit null unresolved decision. A properly verified model result may support a proof family, but **may transfer to another item only after that item's distinct actor, target, scope, conditions, exceptions, limit and outcome are checked**. No family membership, similarity threshold, or model confidence authorizes unverified bulk TP assignments.

All 192 returned items must have an individual accepted result or an explicit failed/pending status; full handoff completion requires 192 distinct validated results. LLM calls do not replace Phase 04's all-TP review, Phase 05's all-GC review, or Phase 06's all-N review. Do not claim remaining unresolved items were adjudicated just because a representative was sampled.

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

Each `r` in R has one `FINAL_SOURCE` record and, if resolved, either TP (actual=1, predicted=1) or FN (actual=1, predicted=0). Each `n` in N has one `FINAL_CONTROL` record and, if resolved, either FP (actual=0, predicted=1) or TN (actual=0, predicted=0). Each distinct f in F has one `FINAL_RESIDUAL` record (actual=0, predicted=1), linked back to all supporting GCs. Every effective GC has exactly one `FINAL_CLASS` classification; supported classes are validity ledger rows, not extra canonical score units. Unresolved candidate residuals are **not** counted as known F or zero F.

### 5.2 Confirmed four-cell definitions and equations

| Cell | Actual | Predicted | Evidence-grounded meaning |
|---|---:|---:|---|
| `TP` | 1 | 1 | Complete PDF-positive obligation covered by definitive generated commitments |
| `FN` | 1 | 0 | PDF-positive obligation demonstrably missing or only partially covered after reciprocal challenge |
| `FP` | 0 | 1 | Affirmed fixed PDF-negative control or one unique PDF-unsupported generated-only residual |
| `TN` | 0 | 0 | Fixed PDF-negative counterfactual not affirmed by definitive generated commitments |

For a **fully resolved** universe:

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

Compute all metrics from the enumerated canonical units in the final ledger, **never from manually supplied totals, raw GO/GC class counts, retrieval candidates, or prior-model votes**:

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN) = TP / |R|
F1        = 2 * TP / (2 * TP + FP + FN)

R_coverage_rate           = TP / |R|                   # equals Recall when fully resolved
negative_control_pass_rate = TN / |N|                  # bounded diagnostic only
GC_validity_rate          = PDF_supported_GC / definitive_GC
raw_duplicate_rate        = (|GO_m| - |GC_m|) / |GO_m|
```

`PDF_supported_GC` includes fully PDF-entailed and explicitly supported-noncovering definitive classes; it does not include ambiguous, nondefinitive, or unsupported classes. The full GC-validity rate is `null` while any effective GC support/eligibility is unresolved; likewise, the full R-coverage rate is `null` while UR is nonzero, and the full negative-control pass rate is `null` while UN is nonzero. Clearly identify the denominator of every diagnostic rate. `negative_control_pass_rate` is **not** true-negative population accuracy and does not enter Precision/Recall/F1 other than through the genuine FP count when a negative control is affirmed. Do not derive per-file source Recall by copying globally satisfied R atoms to each file; any file attribution is separately defined evidence contribution, not overall coverage.

Zero-denominator handling: return JSON `null` for Precision when `TP+FP=0`, Recall when `|R|=0`, the negative-control rate when `|N|=0`, GC-validity rate when its definitive denominator is zero, and duplicate rate when `|GO|=0`. Return F1 as `null` when `2TP+FP+FN=0`, otherwise its exact fraction (including `0` where appropriate). Store native numeric values, not rounded strings; reports may format a separately specified number of decimal places without changing underlying values.

### 5.4 Unresolved units and honest metric status

Maintain these unresolved sets independently:

- `UR`: source R atoms with no justified final TP/FN;
- `UN`: frozen N controls without a justified final TN/FP;
- `UG`: unresolved definitive-GC support/eligibility or unique generated-only FP residual candidates; linked duplicates are not presumed independent FPs.

The following **partial-state invariants are mandatory**:

```text
TP_confirmed + FN_confirmed + UR = |R|
TN_confirmed + B_confirmed + UN = |N|
FP_confirmed = B_confirmed + F_confirmed
UG does not contribute zero or a forced FP count.
```

If `UR > 0` or `UN > 0` or `UG > 0`, or residual clustering/evidence validity is incomplete, set **full-population** `Precision`, `Recall`, and `F1` to JSON `null` with `METRICS_PROVISIONAL_UNRESOLVED`. Report confirmed cell counts, unresolved counts, closed-population coverage percentages, and optionally a separately labeled **resolved-subset diagnostic**; never present such a diagnostic as the all-item score. A sampled 192-item adjudication cannot itself produce a verified 2,000-item full-population rate. Do not substitute `FP=0` for unresolved generated-only claims or `FN=0` for unreviewed R.

A fully enumerated but semantically unresolved run may be `FINAL_BEST_EFFORT`. `FINAL_VERIFIED` requires all complete evidence and population gates, not only arithmetic reconciliation or confident model text. Do not claim statistical confidence intervals without an explicit sampling model, sampling weights, variance method, and measured sampling outcomes. When GO/GC eligibility itself remains unresolved, mark the duplicate rate provisional (or `null` if the effective eligible denominators cannot be established); PDF-support uncertainty alone does not invalidate a structurally complete GO/GC duplicate count. The 48 stratified audit items provide error diagnostics; their raw success fraction is not an unbiased estimate of total accuracy without appropriate design/weights.

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
2. Confirmed `TP`, `FN`, `TN`, `B`, `F`, `FP`, unresolved `UR`, `UN`, `UG`, and closed versus unresolved coverage of each inventory.
3. Full-population Precision/Recall/F1 (number **only if** complete) plus raw Duplicate, GC validity, bounded N-pass rate, and the explicit metric calculation status.
4. FN-root-cause counts `TRUE_MISSING`, `PARTIAL_ENTAILMENT`, `MATCHER_FALSE_NEGATIVE_CORRECTED`, and `CONSERVATIVE_UNRESOLVED`, with cited strongest generated candidates.
5. TP evidence quality: counts of `E3`, `E2`, incomplete proof, direct-identifier exceptions, and verified universal/conditional/conjunctive bridges; reference exceptions do not silently reduce R.
6. FP provenance: asserted N controls, distinct generated-only residual classes, all original G evidence locators, scope differences, duplicate-cluster decisions and PDF contrary checks. Include a separate list of `SUPPORTED_NONCOVERING` GCs.
7. LLM audit: 192 unique selected IDs, direction/role/risk/stratum distribution, valid returns, quotation verification failures, review-pending items, result/ledger disagreements, and proof-family transfer recipients actually checked.
8. Per-file descriptive GO/GC occurrence and duplication totals (counting each original occurrence once), optional chapter/requirement-family coverage diagnostics with exact denominators, and cross-method comparisons only over identically frozen R/N.
9. Input/evidence validity flags, unsupported residual ambiguities, benchmark atomization exceptions, scope/permission high-risk unresolved items, and explicit limits on conclusions.

Never call a high Recall, a low FP count, or a structurally balanced confusion matrix proof of specification correctness without corresponding semantic evidence.

## 6. Eight ordered phases

Each phase must finish its entire specified non-LLM population within the current response. Only the external 192-call handoff is performed between Phase 06 and Phase 07; it is not a ninth phase. Each principal JSONL includes one `PHASE_SUMMARY` record (excluded from item counts) with totals, status, reliability counts, evidence problems, exact input digests, and unresolved limits.

| Phase | Required work | Output artifacts | Completion gate |
|---|---|---|---|
| **01 — Reference lock** | Verify original PDF identity, 90 pages, evidence images/tables, frozen R/N hashes and IDs; if no frozen reference, independently construct and lock before generated inspection. Record immutable source digests and reference exceptions. | `01_reference_lock.json`; construction-mode R/N files only when necessary | Stable verified benchmark and all eight scored inputs identified; reference blockers cannot advance |
| **02 — Complete GO/GC extraction** | Scan every substantive Markdown paragraph/table row and all actual cells with inherited context. Produce definitive complete GO, GC, exclusions, duplicate classification, and original-text index. | `02_generated_atoms_final.jsonl`, `02_generated_classes_final.jsonl`, `02_excluded_units.jsonl`, `02_duplicate_classes.jsonl`, `02_original_text_index.jsonl` | All substantive regions accounted for; every GO in exactly one GC; duplicate arithmetic reconciles |
| **03 — Full R initial coverage** | For every R, use direct/contextual/universal/conjunctive search across the full corpus, record actual PDF/Markdown candidates and complete predicates, and flag extraction gaps. | `03_source_coverage.jsonl`, `03_semantic_coverage_bridges.jsonl` | Exactly one provisional, evidence-linked R status per source atom |
| **04 — Reciprocal FN and TP audit** | Challenge **every** initial FN using both directions; audit **every** provisional TP predicate-by-predicate; identify false misses, partial obligations, reference exceptions and recovery opportunities. Preserve earlier records; add effective audited states. | `04_fn_root_cause_audit.jsonl`, `04_tp_evidence_audit.jsonl`, `04_coverage_audit.jsonl` | Entire R partition reconciled, all preliminary TP proofs inspected, no FN from retrieval absence alone |
| **05 — Full generated validity** | Re-examine **all substantive exclusions** for missed assertions; recover valid GO/GC; evaluate every effective definitive GC against original PDF, including supported-noncovering claims, unsupported residuals and explicit uncertainty. | `05_generated_claim_validity.jsonl`, `05_exclusion_reassessment.jsonl` | Every exclusion and effective GC accounted for; no unmatched-GC-to-FP shortcut |
| **06 — N controls, FP consolidation, and 192-item queue** | Adjudicate all frozen N; merge only genuinely equivalent unsupported residuals; crosswalk N/F to prevent double counting; rank/stratify the complete R/N/G audit pool and freeze **exactly 192 distinct queue items** under §4. | `06_fp_controls.jsonl`, `06_llm_queue_192.jsonl`, `06_queue_selection.json` | All N and residual candidates have status, no FP double counting; queue selection and hashes frozen |
| **07 — 192 sequential LLM reviews and final ledger** | Receive the operator's **192 item-level** `semantic_decisions.jsonl` from the existing evaluator. Verify all quotations with alias-safe original-file resolver; adjudicate every return, audit proof-family transfers, preserve unresolved states, and reconstruct a single effective R/N/GC/residual ledger. The model run is **external handoff**, not a separate phase. | **Input:** `semantic_decisions.jsonl`. **Outputs:** `07_final_ledger.jsonl`, `07_llm_review.jsonl`, `07_duplicate_metrics.json` | All 192 selected items have validated results or phase remains `INCOMPLETE`; all other R/N/GC items are individually resolved or explicitly unreliable |
| **08 — Independent canonical metrics and delivery** | Reconstruct effective states from actual Phase 01–07 records. Revalidate hashes, evidence, unique IDs, TP/FN and F/N accounting, FP-N separation, duplicates, and all equations in §5; calculate numeric full-population metrics only if all required populations are closed; explain unresolved limitations. | `compute_metrics.py`, `08_metrics.json`, `08_report.md`, `08_coverage_and_limitations.md` | Independent recomputation passes; no fabricated full-population metric, omitted item, silent duplicate or unsupported final quality claim |

**Operational handoff:** Phase 06 delivers `06_llm_queue_192.jsonl`; the operator runs the existing evaluator sequentially using the original PDF and eight original Markdown files, then supplies the resulting `semantic_decisions.jsonl` when requesting Phase 07. Phase 07 never treats missing Azure records as missing requirements. Earlier phase outputs are not overwritten. If the run fails before all 192 results are validated, preserve the checkpoint and resume the same immutable queue; do not launch Phase 08 as if the external audit were complete.

## 7. Item-level record and validation contracts

### 7.1 Required final record kinds

`07_final_ledger.jsonl` must contain exactly one effective `FINAL_SOURCE` per frozen R ID, one `FINAL_CONTROL` per frozen N ID, one `FINAL_CLASS` per raw GC ID (including recovered classes and records later judged ineligible, which are excluded from effective GC metrics), and one `FINAL_RESIDUAL` per confirmed unique generated-only unsupported proposition. Every unresolved potential residual has a distinct `RESIDUAL_CANDIDATE` record, rather than an invented scored FP. Each record carries stable ID, method, original input digests, PDF and generated locators, final status, `unreliable`, `unreliable_reason_en`, adjudication provenance, and links to prior superseded records if relevant. `PHASE_SUMMARY` is excluded from canonical counts.

All TP records must include a complete predicate-check map and source-to-generated evidence bridge, with a `TP_AUDIT` reference. Every FN includes an inspected strongest candidate, exact unsatisfied predicates, reciprocal search receipt, and `fn_review_disposition`. Confirmed FP residuals include the exact unsupported affirmative predicate and PDF search/contrary evidence; TN records identify the frozen negative control, relevant generated evidence checks, and nonassertion justification. Each effective GC records status `PDF_ENTAILED`, `SUPPORTED_NONCOVERING`, `PDF_UNSUPPORTED`, `NONDEFINITIVE`, or `UNRESOLVED`; for ambiguous mixed claims split only independently meaningful parts and retain links.

A model result is linked by selected queue ID and source digest, with reported and resolved filename aliases, verified page/line quotations, final reviewer decision, exact residual/bridge, and `REVIEW_PENDING` if incomplete. Prior cells in an external evaluator's `current_cell` field are provisional labels required for compatibility, **never** a final outcome or a metric input.

### 7.2 Example final source unit (schema illustration only)

```json
{
  "record_type": "FINAL_SOURCE",
  "source_id": "PDF-EXAMPLE",
  "method": "fullload",
  "scoring_cell": null,
  "unreliable": true,
  "unreliable_reason_en": "Specific source and generated predicates require further verification.",
  "entailment_grade": "EU",
  "coverage_mode": null,
  "pdf_evidence": [],
  "generated_evidence": [],
  "predicate_checks": [],
  "adjudication_status": "REVIEW_PENDING",
  "prior_record_ids": [],
  "llm_item_id": null
}
```

This is **not a finding**; all executed item IDs, quotes, locators and explanations must be drawn from originals. The example does not authorize an empty evidence array for a final verified TP or a decided FN/FP.

### 7.3 LLM-result acceptance

Accept each external decision only after checking: selected queue membership and uniqueness; expected direction; exact PDF/input digests; response completeness; original PDF page and literal quote; actual Markdown original line range and literal quote under unambiguous filename normalization; supported/contradicted predicate checks; and explicit documented final disposition. Store raw model JSON unchanged alongside the reviewer's evidence-grounded final assessment. Do not equate a model's numeric confidence to a probability of correctness.

## 8. Independent metric recomputation (mandatory Phase 08 implementation)

`compute_metrics.py` must implement and **fail fast** on the following in order:

1. **Load sources:** Open frozen R/N/reference manifest, original PDF identity record, original scored file digests, and every required Phase 01–07 JSON/JSONL artifact. Strictly parse each row; exclude summaries and non-scoring audit markers from units.
2. **Recheck identity:** SHA-256 of frozen R/N/PDF and the eight source files, 90 physical pages, exact role mapping, version, one selected method, and all fixed evidence locators. Mismatch is fatal; missing mandatory evidence is not E0.
3. **Reconstruct effective IDs:** Apply recorded item-level supersession in chronological phase order without editing immutable files. Check there is one current R, N, GC and supported residual-candidate status. No missing/duplicate IDs; all recovered GO map to exactly one effective GC.
4. **Check extraction scope:** Verify every substantive Markdown region and Phase 02 exclusion was assessed, with original source/line/table context and Phase 05 disposition. Verify all recovered assertions and class merges retain actual original passages.
5. **Check coverage:** Every confirmed TP has full PDF and generated evidence, actor/target/action/conditions/exception/timing/outcome check, and a TP audit. Every confirmed FN has a full-corpus reciprocal challenge and exact `TRUE_MISSING` or `PARTIAL_ENTAILMENT` reasoning. Direct complete matches mislabeled FN and invented universal bridges are hard validation errors.
6. **Check generated validity:** Every effective GC has one eligible support category or an explicit unresolved disposition. `PDF_UNSUPPORTED` must cite a real unentailed residual; `SUPPORTED_NONCOVERING` must cite PDF-positive evidence. No source-absence-only FP; no definitive assertion hidden in an exclusion.
7. **Check negative controls:** Exactly one R-independent N judgment per fixed ID. Asserted N controls contribute one FP each. Check all N-to-F crosswalks and forbid the same proposition in B and F. Count unsupported residual classes once after semantic merging; retain all original occurrences.
8. **Check external audit:** Verify immutable queue contains 192 distinct individually selected IDs with fixed selection seed/rules; verify each selected ID has one accepted result, sequential request order and complete response/evidence reviews. Verify no more than 200 actual submissions, replay/resume provenance and no double-accounting of retry attempts. Missing results block a claim of completed external adjudication.
9. **Check unresolved equations:** Recompute `UR`, `UN`, and `UG`, the partial-state identities in §5.4, and status for each affected unit. Do not introduce unknown F units into the finalized U. For a closed population, assert all identities in §5.2 and `|U|=TP+TN+FP+FN` exactly.
10. **Calculate counts and rates:** Derive four cells by enumerating final canonical IDs; calculate Precision, Recall, F1, raw Duplicate, per-file duplicates, GC validity and bounded N-pass with §5.3 denominators and null rules. Never force `TP+FP=|GC|`. Use exact arithmetic before report formatting.
11. **Cross-check report:** Compare all JSON totals/rates to the Markdown report. Require correct final metric status, unresolved counts, risk/source anomalies, supported-noncovering claims, FP canonicalization evidence, and transparent distinction between structural and semantic certification.
12. **Cross-method fairness:** When evaluating multiple methods, require same original PDF, R/N bytes, eligibility and adjudication policy. Recompute each method's independent GO/GC/F and canonical cells. Compare only like-named and like-defined metrics, not raw GC and canonical predicted positives interchangeably.

`compute_metrics.py` must exit with an error on a violated structural or evidence invariant, and must never print or write a fabricated Precision/Recall/F1. If records are all present but semantic ambiguity remains, output consistent confirmed counts, unresolved counts and `null` full-population metrics with `METRICS_PROVISIONAL_UNRESOLVED` rather than failing merely because a defensible unresolved judgment exists.

## 9. Completion statuses and reporting boundaries

- `PHASE_COMPLETED_VERIFIED`: the phase's input, population, integrity and mandated evidence checks are complete; this does not assert independent semantic certification.
- `PHASE_COMPLETED_BEST_EFFORT`: complete per-item processing, with specified unresolved semantic judgments and evidence limits.
- `INCOMPLETE`: required phase records, a mandatory original file, the selected 192-result handoff, or another essential processing step is missing.
- `BLOCKED_REFERENCE` / `INVALID_REFERENCE_CHANGED`: original source or required frozen benchmark identity/checksum failure; cannot advance or silently replace it.
- `FINAL_VERIFIED`: all eight phases complete, exact canonical unit accounting, full evidence, independent recomputation, no unresolved scored units or material known evidence defect.
- `FINAL_BEST_EFFORT`: all required phase populations and audit records are complete but material semantic uncertainty remains; full-population Precision/Recall/F1 are null and all open units are disclosed.

The final report must state clearly that the measures evaluate **generated design specifications against the fictional PDF baseline**, not implementation correctness, operational performance, or generalized model accuracy. The 192 sequential original-file LLM reviews improve selected semantic decisions but do not independently certify every unreviewed item. Preserve frozen R/N, actual original evidence, conservative FP/FN accounting, distinct duplication measures, and the same canonical scoring universe through final delivery.
