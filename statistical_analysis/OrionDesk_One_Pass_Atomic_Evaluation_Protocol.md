# OrionDesk AI — Nine-Phase Evidence-Grounded Atomic Requirement Evaluation Protocol

**Protocol version:** 10.6  
**Purpose:** Compare the `fullload`, `onelevel`, and `twolevel` generation methods with one frozen PDF reference, consistent semantic-entailment and counting definitions, complete source/generated inventory audits, and identical adjudication policy. The Phase 06 handoff uses the original Version 5.0 semantic judgment logic, transported in JSON batches of 8 or 16 items per Azure Responses request; a final partial batch is permitted.  
**Evaluation implementation:** `semantic_decision_evaluator_v10.6_unlimited.py` (operational derivative of supplied `semantic_decision_evaluator(3).py`, retaining the original Version 5.0 `SYSTEM_PROMPT`, `RESULT_SCHEMA`, and `suggest()` semantics while applying a strictly provenance-checked filename-alias correction inside the `check_evidence()` quotation verifier, and setting `PROTOCOL_VERSION="10.6"` and `EXECUTION_VERSION="10.6"`); **reasoning effort `high`**, protocol-approved batch size **8 or 16** (default **8**), configurable concurrent requests (default **4**), **three additional per-batch retries** where safe. Stdout uses elapsed-time event logs. Requests attach nine stable source files and place `prompt_cache_breakpoint={"mode":"explicit"}` only on the ninth `input_file` block, before per-batch input; do not pass `prompt_cache_options`. The script's output is evidence-checked item-level *suggestions*, not a fabricated closed confusion matrix. A separate, mandatory assistant-led Phase 07 completes classifications under a fixed evidence-based decision procedure without modifying the original v5 evaluator.  
**Supported generation methods:** `fullload`, `onelevel`, `twolevel`.  
**Required operator input:** Supply `spec_gen_method` explicitly; never infer it.  
**Execution:** Exactly nine ordered phases; complete the current phase before advancing. After the Phase 06 external handoff, Phase 07 obligatorily adjudicates every still-undecided item, Phase 08 reconciles the complete canonical population, and Phase 09 independently computes metrics. Apply the same frozen rules to every generation method.  
**Language:** Conversation follows the operator's requested language; authored files, records, script text and reports are English.  
**Delivery:** Phase outputs individually; no ZIP or revision-history document unless requested.

## 1. Governing rules

1. **Source authority:** The original 90-physical-page PDF determines the normative baseline. The eight Markdown files are the method-specific generated predictions. Previous model outputs and historical scores are not source authority.
2. **Frozen reference:** Validate and preserve the exact `common_atomic_reqs.jsonl`, `common_negative_controls.jsonl`, `reference_freeze.json`, and PDF SHA-256, when supplied. Never rewrite the reference or change a denominator during evaluation. Benchmark atomization concerns are recorded separately, not silently reclassified to improve scores.
3. **Cross-method measurement invariance:** Full Load, One-Level, and Two-Level use the same PDF and frozen R/N bytes, eligibility policy, semantic coverage/unsupportedness rules, source units, duplicate-consolidation policy, decision threshold, evaluator prompt/logic, model deployment, reasoning effort, batching contract and metric equations. If any of these differ, mark the runs noncomparable instead of silently mixing scores.
4. **Unlimited full-inventory processing:** No arbitrary numeric upper bound applies to R, N, GO, GC, unique residual F or the Phase 06 external queue K. Audit every frozen source/control and every eligible generated assertion/class. An item may be exempt from external adjudication only because its evidence-based decision is already independently accepted, never because a numerical budget is exhausted. Use a configured batch size of **8 or 16 items per request** (with a possibly smaller final batch); there is no total inventory or total API-request count cap. The executable separately accepts any positive integer up to its documented technical cap of 128, but values other than 8 or 16 are not protocol-approved for comparable experiment runs.
5. **Logical entailment, not lexical identity:** Direct equivalence, scope-valid universal rules and explicitly justified cross-file conjunctions may establish coverage. A shared keyword, candidate retrieval hit, or syntactic difference alone does not prove a positive or negative.
6. **Bidirectional evaluation:** `R -> generated` determines source coverage; `generated -> PDF` determines validity. A generated clause not in frozen R is not automatically unsupported.
7. **Eligibility:** Only definite affirmative generated implementation/test obligations enter GO/GC. Unadopted proposals, TBDs, alternatives, examples, headings and uncommitted commentary are nondefinitive. Audit separable definitive fragments of mixed passages.
8. **Atomization and duplicates:** Split independently testable complete obligations; preserve inherited row, heading and exception context. Merge generated occurrences only when mutually entailed as complete propositions. Never multiply FP by repeating the same unsupported obligation across files.
9. **Independent evidence and filename aliases:** Verify literal PDF quotations against physical pages and generated quotations against the SHA-256-verified, uniquely mapped actual original Markdown role and exact line range. Resolve model-reported canonical/copy-suffix names through the eight-file role map under §3.1; preserve the reported name, resolved actual name and source digest. Never reject an accurate quotation *solely* for an unambiguous canonical-versus-upload-copy suffix. Reject ambiguous role mapping, mismatched source hashes, wrong line ranges and mismatched quotations. Quote verification proves *quotation existence*, not semantic entailment.
10. **Original Version 5.0 decision logic is frozen, with an explicit evidence-name resolver exception:** Preserve the exact v5 `SYSTEM_PROMPT`, `RESULT_SCHEMA`, `suggest()`, confidence threshold, and substantive PDF-quote/generated-quote line-matching requirements. The implementation of `check_evidence()` **must** be amended only to resolve a verified eight-role filename alias *before* carrying out the original strict generated-quotation check. No evidence or decision is accepted on role similarity alone; the source digest and specified original line range must verify. This correction is authorized within Version 10.6 and is applied identically to all three methods. Do not introduce eleven-dimension checklists, `D7-*` fallback scores, `BEST_EFFORT` fields, forced `unreliable=true` outcome fields, or fabricated canonical cells. The Python prompt naturally describes the substantive features of a requirement; this is not an obligation to produce eleven separate classification dimensions.
11. **No automatic script fallback; mandatory later adjudication:** The original v5 judgment function may return `suggested_decision=null` or `decision_status=UNRESOLVED`. Preserve that original output exactly. In Phase 07, the assistant must independently resolve every undecided or unverified population item to the appropriate fixed binary cell after inspecting original evidence. This is an evidence-based adjudication, not a relabeling of an LLM uncertainty flag or an automatic negative default.
12. **Phase 07/08/09 division:** The v5 script only records immutable per-item suggestions. **Phase 07** independently and obligatorily assigns final item-level cells wherever the script or prior evidence leaves them undecided. **Phase 08** performs mechanical reconciliation, N/F semantic-equivalence consolidation and consistency verification **without issuing a competing item-level semantic judgment**. Contradictions are returned to Phase 07 for an evidence-recorded superseding decision; Phase 08 cannot silently relabel an item. **Phase 09** recomputes a single comparable Precision/Recall/F1 set. If mandatory originals are inaccessible, declare the phase `INCOMPLETE` with a concrete input blocker rather than fabricate evidence or metric counts.
13. **Immutable histories:** Freeze original documents, R/N ledgers, queues, per-batch result journals and already delivered phase files. Correct later phases by explicit supersession, preserving previous bytes. A v10.6 Phase 01–09 run starts with a new reference lock and separate output directory; v10.5 judgments may be inspected as historical evidence but are not silently relabeled as v10.6.
14. **One phase per turn:** Finish the requested phase's enumerated scope or report a genuine blocker as `INCOMPLETE`; never skip ahead. Do not assert that a phase or the experiment is complete solely because every requested LLM submission was attempted.
15. **Historical consistency is a diagnostic:** Large departures from earlier scores trigger investigation of denominator, extraction, classification, prompt, evidence and deduplication differences. Never tune thresholds or relabel cells to force agreement with historical results. Apply justified revisions equally to every method and restart all compared measurements under the new policy.

## 2. Inputs, identity, and extraction

### 2.1 Required materials

- The original, readable 90-page English PDF (authoritative source).
- An explicit operator-supplied `spec_gen_method` value: `fullload`, `onelevel`, or `twolevel` (exactly one; no inferred/default value).
- Exactly eight original Markdown roles, mapped unambiguously: `01_screen_functions.md`, `02_api.md` (also `02_api_.md`), `03_data.md`, `04_batch_functions.md`, `05_business_rules.md`, `06_exception_handling.md`, `07_processing_flows.md`, and `08_architecture_decision.md`.
- In frozen mode: `common_atomic_reqs.jsonl`, `common_negative_controls.jsonl`, and `reference_freeze.json` (upload-copy suffixes accepted).
- For external adjudication: `semantic_decision_evaluator_v10.6_unlimited.py` (an operational derivative of the supplied `semantic_decision_evaluator(3).py`, preserving its Version 5.0 item-judgment logic, applying the required §3.1 evidence filename-alias fix, and aligning both executable version fields to 10.6), a frozen JSONL queue containing **every** eligible genuinely pending R/N/GC item, with **no method-specific or global item-count maximum**, and `semantic_decisions.jsonl` plus batch journals and the attempt ledger. The Version 5.0 judgment logic supplies suggestions, not final population-level classification.

Recognizable method prefixes and copy suffixes are permitted only with unique role mapping during phase-ledger creation. Preserve actual input filenames and bytes. The Version 10.6 execution derivative **must implement and test** the eight-role SHA-256-validated filename-alias resolver described in §3.1; do not retain the v5 filename-string equality defect. The reported filename may be the exact actual basename or a canonical/copy-suffix form for the same uniquely mapped, verified role. A normalized role name by itself does not confer quotation validity, and never changes the source bytes or their SHA-256 identity. The protocol, earlier phase ledgers, and any aggregate JSON are not ninth scored Markdown inputs.

### 2.2 Frozen checks and source-atom rules

Read each frozen JSONL record and validate the declared positive key (`requirement_id` or `source_id`) and negative key (`control_id` or `negative_control_id`), no mixed keys or duplicates, original PDF SHA-256, expected reference hashes, physical page count, and evidence quotation availability. Fail on incompatible identity/hash or inaccessible required material. Record nonfatal benchmark atomization doubts as `REFERENCE_EXCEPTION`, leaving IDs and bytes unchanged.

`R` comprises smallest independently meaningful PDF-positive normative obligations; a PDF prohibition is itself a positive duty to enforce. General obligations must not be repeated arbitrarily for each endpoint. An endpoint with a distinct method, actor, response, condition, or timing can have independent atoms. Preserve original page, quote, actor, target, condition, constraint, version, outcome, and additional supporting locations.

`N` is a fixed bounded inventory of affirmative counterfactuals explicitly prohibited, excluded, or deferred in the PDF. It is not the set of every possible absent feature. Keep `R ∩ N = ∅`. Never add method-specific controls during scoring.

### 2.3 Generated inventories

`GO` is the set of complete, eligible definitive assertion occurrences, with stable `GEN-*` ID and actual Markdown file, line, row, cell, heading, and full inherited context. `GC` is the set of unique within-method semantic classes, with stable `GCLASS-*` ID and exactly one class assignment per eligible `GO`. Every substantive source line/row must be accounted for by eligible assertions, exclusions, or inherited context; excluded prose is indexed and re-examined in Phase 05. Recovered assertions use new stable IDs and original locators without altering prior files.

## 3. Evidence-first matching and semantic judgment

### 3.1 Reusable indexing, never similarity verdicts

Index PDF pages and all eight Markdown files, including headings, table context, normativity, scope, exceptions and universal clauses. Search bidirectionally to identify the strongest original evidence for each R/N/GC. Proof-family transfers require independent applicability checking and must never replicate one generated class into multiple raw classes. Preserve the source digests and original locators of every accepted and rejected transfer.

**Mandatory filename-alias verification (authorized Version 10.6 execution-layer correction).** The original v5 verifier checks literal original text and precise line/page locators; retain those substantive checks. Its *filename equality lookup* must be replaced by the following deterministic resolver, identical for `fullload`, `onelevel` and `twolevel`:

1. Build exactly eight uniquely identified source roles from the **actual uploaded originals**: `01_screen_functions`, `02_api` (including the documented `02_api_` spelling), `03_data`, `04_batch_functions`, `05_business_rules`, `06_exception_handling`, `07_processing_flows`, `08_architecture_decision`. Permit only each role's canonical `<stem>.md` and recognized upload copy suffix `<stem>(N).md` (`N` a positive decimal integer); reject any path, unknown stem/extension or competing source-role assignment. An explicit source selection may bypass unrelated files but never bypass unique role validation.
2. Record each role's actual filename, immutable original file path, complete original lines and computed SHA-256. When a Phase 01 role manifest is supplied, pass `--source-lock 01_reference_lock.json` to compare its ordered eight original SHA-256 values before uploading any file. In all cases, verify the actual originals' SHA-256 against the evaluator's recorded upload/run-state digest. If the original file's bytes change, or the recorded role/digest is inconsistent, fail evidence validation; do not silently use a different file. The role-based alias is not a substitute for a verified source identity.
3. Resolve every LLM-provided `generated_evidence[].file` to **exactly one** hash-verified source role. `03_data.md` and `03_data(1).md`, for example, may resolve to one verified role when only one actual original is selected and its SHA matches. In the reverse direction, `02_api(2).md` reported against uploaded `02_api.md` may resolve likewise. When a separately existing filename matching the reported alias is available, its SHA-256 must match the selected original; otherwise reject `ALIAS_FILE_DIGEST_MISMATCH` even if the quoted sentence happens to match. Never silently accept content from a different original.
4. After resolving the role, verify the **reported** `line_start`/`line_end` are positive integer line numbers, `1 <= start <= end <= original line count`, and the literal normalized quotation exists inside **those exact original lines** of the resolved actual source. No fuzzy text matching, alternative-line search, unrelated-file fallback or semantic similarity can override a failed quotation or invalid range. Preserve the original v5 PDF physical-page quotation check and the exact `suggest()` rules.
5. In each `evidence_checks.generated[]` record and a concise stdout `ALIAS` event, log the **reported filename**, **resolved actual filename**, **role**, **verified SHA-256**, alias-resolution method, final quotation-verification Boolean and any explicit failure reason. The raw `model_json` remains byte-preserved. A successful role alias with an accurate original quotation sets `verified_original=true`; an ambiguous/invalid name, inconsistent digest, invalid line, or mismatched quote remains `false` and must never be promoted to a suggested TP merely by renaming.
6. Before any Azure request, test exact names, both alias directions, multi-line quotations, wrong role, ambiguous role, differing digest, wrong original line, altered quote, and changed original bytes. Compare `SYSTEM_PROMPT`, `RESULT_SCHEMA` and `suggest()` against the original supplied script to confirm no substantive judgment-policy changes. **Failure of any alias test blocks the handoff**, even when queue parsing and batch-size tests pass.

The source filename as named by a model is untrusted attribution, not its own evidence. Only the verified role/digest and exact original range establish its provenance. This is a prescribed filename-resolution implementation change, **not a change of protocol version or the v5 confidence/semantic decision policy**.

### 3.2 Bidirectional coverage decisions

For every `r in R`:

1. Reconstruct the normative proposition from PDF page, table and heading context.
2. Search all eight generated specifications, definitive occurrences, common clauses and exclusions using wording, aliases and reciprocal indices.
3. Check direct entailment, applicable universal rules and explicitly justified cross-file conjunctions.
4. Accept TP only when the *whole* required proposition is covered, with evidence. For an FN candidate, challenge the strongest nearby generated expression and record the actual unmet obligation.
5. If the evidence or model result fails the v5 acceptance conditions, preserve its provisional unresolved state and route it to Phase 07. Phase 07 independently decides TP/FN after source-grounded reciprocal inspection; the original v5 `suggest()` and semantic model prompt remain unchanged.

For each generated class `g in GC`, determine whether the PDF entails the entire affirmative definitive claim. Keep `PDF_ENTAILED`, `SUPPORTED_NONCOVERING`, `PDF_UNSUPPORTED` and an unresolved state as **provenance categories**, not replacement v5 `suggested_decision` cells. A generated class absent from the fixed R list is not automatically an FP. Every genuine unsupported generated-only residual must be consolidated and cross-checked against the N inventory before counting.

For each negative control `n in N`, determine whether an eligible affirmative generated statement really asserts the forbidden counterfactual. Assertion -> FP; demonstrated nonassertion -> TN. A generated *prohibition* of the counterfactual is not affirmative assertion of that counterfactual. Incomplete evidence does not imply TN.

### 3.3 Entailment evidence grades (original-ledger diagnostics only)

| Grade | Meaning | Permissible conclusion |
|---|---|---|
| `E3` | Complete direct equivalence with original quotations | Full entailment |
| `E2` | Complete and applicable contextual/universal/conjunctive proof | Full entailment |
| `E1` | Relevant but incomplete predicate coverage | Partial evidence, not automatic FN/FP |
| `E0` | Inspected contradiction or established nonentailment | Negative finding if the relevant search is sufficient |
| `EU` | Materially unresolved evidence at the discovery or external-model stage | Mandatory Phase 07 independent adjudication; not an automatic negative |

`E2` and `E3` are equally valid substantive proof paths. These grades are recorded by the broader phase ledgers; the supplied v5 evaluator does not require or emit a separate eleven-dimensional predicate-check array or a `verified_confidence_level` column.

### 3.4 Frozen v5.0 item-level adjudication semantics

The external response fields are exactly the supplied script's per-item `RESULT_SCHEMA`: `item_id`, `direction`, `eligibility`, `relation`, `confidence_estimate`, `corpus_exhaustively_reviewed`, `pdf_evidence`, `generated_evidence`, `unsupported_residual_en`, `missing_predicates_en`, `alternative_checks_en`, `reason_en`. Keep the original `SYSTEM_PROMPT` substantive meaning unchanged; adding the batch envelope must not change the evaluation threshold or the relation/eligibility definitions.

The externally provided `confidence_estimate` is a self-report in `[0,1]`, not a calibrated probability. **The v5 threshold is `--confidence-threshold 0.90` by default**, and the supplied `suggest()` code is the controlling decision function. Its pertinent behavior is:

- Low confidence or `MIXED`/`UNRESOLVED` eligibility -> no committed item suggestion (`null`), `decision_status=UNRESOLVED`.
- `G` plus `NONDEFINITIVE` eligibility -> `EXCLUDED_NONDEFINITIVE` only if the original generated quotation verifies.
- `G` `FULL` plus both PDF/generated quote verification -> `NOT_FP`.
- `G` `CONTRADICTED` plus both quote verifications and a nonempty unsupported residual -> `FP_CANDIDATE`.
- `R` `FULL` plus verified source/generated quotations -> `TP`; `N` `FULL` plus verified quotations -> `FP`.
- `R`/`N` `NOT_FOUND` plus `full=True` and `corpus_exhaustively_reviewed=True` -> respectively `FN`/`TN` **as unresolved review suggestions**, not automatically verified final cells.
- Other cases, including `PARTIAL` -> `null` suggestion and unresolved status. Quote existence alone cannot establish semantic proof.

These exact v5 `suggest()` rules govern the evaluator. Do not substitute the v10.5 deterministic fallback thresholds (`0.80`), `D7-*` priority, or any per-predicate vote. Do not convert `NOT_FP`, `FP_CANDIDATE`, or `EXCLUDED_NONDEFINITIVE` into extra canonical cells without the Phase 07 independent review and Phase 08 canonical mapping. A v5 `UNRESOLVED` is a request for further decision, not a final label.

### 3.5 Proof-family reconciliation and completion

Before selecting external items, and again after external handoff, independently audit the full R/N/GC population. Transfer an item-specific proof to a related item only when all applicable substantive conditions are actually established. Preserve checked and rejected recipients, source locations and class/residual de-duplication. A batch of 8 or 16 distinct items is **not** one proof family.

Items without sufficient proof remain provisional through Phase 06 only. Phase 07 must inspect the entire available source corpus and make a documented final binary decision for every such eligible item under §7; no candidate may be left with a null cell when all mandatory inputs are readable. The original Version 5.0 evaluator's conservative uncertainty semantics are preserved **in its own outputs**, not imposed as a veto on the separate Phase 07 decision.

### 3.6 Separate decision authority of the new Phase 07

The v5 script emits item-level `suggested_decision`, `decision_status`, `review_reason_code`, model JSON and quotation checks, but does **not** commit final population-level TP/TN/FP/FN scores. Preserve the script result without modification. Phase 07 is a **separate, mandatory assistant adjudicator**, using §7's fixed rules and the original PDF and eight Markdown files, rather than an extra v5 model call or a forced substitution inside the evaluator.

Where a script suggestion is `null`, `UNRESOLVED`, `FN`/`TN` with `UNRESOLVED` status, otherwise insufficiently supported, or no valid v5 response exists after a failed or ambiguous submission, Phase 07 must issue and document its own final item decision. Independently accepted suggestions may be adopted with explicit evidence. All definitive generated classes also receive a supported/not-supported determination; their diagnostic cells do not multiply canonical R true positives. Missing/corrupt originals are a fatal **input blocker**, not semantic `UNRESOLVED` and not a license to invent facts. No eleven-dimensional checklists, `BEST_EFFORT`, or result-level `unreliable` flags are permitted.

## 4. Method-specific adjudication selection and 8-or-16-item Azure batches

### 4.1 Unbounded exhaustive selection and v5-compatible queue

**There are no source-atom, generated-atom, class, unresolved-case, queue-item, or total-batch count caps.** Full Load, One-Level and Two-Level follow the **same** selection rule. First enumerate the complete frozen R/N population and the entire effective eligible GC population, and resolve only those items with independently accepted, source-grounded proof already established in Phases 01–06. Let `C` be the number of remaining eligible genuinely pending R/N/GC adjudications. **Select `K=C`** without numerical sampling, top-K truncation, method-specific budgets or arbitrary `--limit`. This is an exhaustive queue of pending decisions, not a statistical sample.

Freeze item ordering deterministically: R by frozen source-ID order, N by frozen control-ID order, then effective GC by original role, line and stable class ID. Each pending eligible ID appears **exactly once** in `06_llm_queue_v10.6.jsonl`, unless a valid, separately recorded proof-family transfer has already closed it with independently checked applicability. Do not omit, pad, duplicate or silently truncate items. The full population and selected queue are separately enumerated and linked by ID in `06_queue_selection.json`, with `K=C` asserted as a hard integrity invariant. A valid pending item count of 4,096, 10,000 or greater is processed through additional batches rather than cut off; available memory, file-size and provider service limits remain practical execution constraints, **not permitted measurement-denominator limits**.

The execution-only derivative of the supplied v5 script rejects nonzero `--limit`; its default is zero. The Phase 06 queue requires `unreliable=true` on **every** included pending row; the execution wrapper rejects any inactive entry instead of silently dropping it. This change does not affect `SYSTEM_PROMPT`, `RESULT_SCHEMA`, `suggest()`, `confidence_threshold` or model `reasoning_effort`; the separately mandated §3.1 filename-alias resolver updates only the `check_evidence()` attribution lookup and preserves strict quotation validation. The original supplied script remains unmodified for provenance. The corrected Version 10.6 execution derivative is a separately named file and documents the alias policy in its resume fingerprint. The same full-population selection rule is used by all generation methods. **When `C=K=0`, create an empty Phase 06 queue and selection manifest, explicitly skip the external script (whose `read_queue()` rejects an empty queue), record zero batches and zero submissions, and continue to Phase 07 using independently accepted prior evidence.**

**Mandatory exact v5 queue format:** The supplied `read_queue()` accepts one JSON object per line, *all* of `record_type="UNRELIABLE_ITEM"`. It does **not** accept a `PHASE_SUMMARY` line or a v10.5 `LLM_QUEUE_ITEM` row. Every selected item must include `item_id`, `direction` (`R`/`N`/`G`), `current_cell`, `statement_en`, `spec_name`, and the Boolean `unreliable` flag. For this evaluator, `unreliable=true` is **required on every submitted queue row** and is **only a queue selection flag**, not a post-evaluation `BEST_EFFORT` score or an additional decision-quality column. `current_cell` is required and provisional: R accepts `TP`/`FN`, N accepts `TN`/`FP`, and G accepts `FP`. It is never metric authority. Include original provenance/evidence hints as optional additional JSON keys; `generated_evidence` and `pdf_evidence_hints` must be arrays when present. Item IDs must be distinct. Do not truncate `statement_en`. **No `PHASE_SUMMARY` row inside the evaluator queue:** keep the separate `06_queue_selection.json` manifest.

The Phase 06 handoff artifact is `06_llm_queue_v10.6.jsonl`, together with `06_queue_selection.json`, frozen reference/source digests, and all applicable Phase 01–06 population ledgers. An old v10.5 queue must not be passed to this code merely because it contains similar fields: construct the new v5-compatible row schema while keeping original reference files immutable.

### 4.2 Batch envelope and Azure execution

Use `semantic_decision_evaluator_v10.6_unlimited.py` with `PROTOCOL_VERSION="10.6"` and `EXECUTION_VERSION="10.6"`, without modifying the original v5 `SYSTEM_PROMPT`, `RESULT_SCHEMA`, `suggest()` or scoring thresholds; `check_evidence()` is corrected only as specified in §3.1 to resolve unique role/verified-SHA filename aliases and then verify the exact original line quotation. The model deployment is `gpt-6.2-sol`; **`reasoning={"effort":"high"}`**, exactly as in the uploaded Python script. The evaluator attaches the original PDF and **all eight original Markdown source files** to each request using uploaded Azure Files IDs. The request transmits one JSON batch of **8 or 16 independently evaluated items**, except the final partial batch. This batch size is fixed and identical for all methods in a comparable experiment. The top-of-script defaults `BATCH_SIZE_DEFAULT=8` and `CONCURRENCY_DEFAULT=4` can be changed directly or overridden by CLI. The executable's technical `BATCH_SIZE_MAX=128` permits positive integer sizes 1..128 for testing; such other sizes require a separate explicit protocol revision before being used for comparable scores. The strict model output envelope is:

```json
{"batch_id":"B10.6-00001","batch_index":0,"batch_size":8,"results":[{"item_id":"...","direction":"R","eligibility":"DEFINITIVE","relation":"FULL","confidence_estimate":0.95,"corpus_exhaustively_reviewed":true,"pdf_evidence":[],"generated_evidence":[],"unsupported_residual_en":"","missing_predicates_en":[],"alternative_checks_en":[],"reason_en":"..."}]}
```

*The single sample result above is illustrative only; a full `batch_size=8` response requires exactly eight complete, ordered item objects, while a full `batch_size=16` response requires exactly sixteen. Only a final partial batch can have fewer than the configured size. Every real result must contain authentic evidence and preserve input order.* Batch ID, batch index, batch size and ordered result IDs must match the submitted queue segment. No other required result columns are added. No per-item eleven-dimensional checklist, `BEST_EFFORT`, `binary_cell`, or forced final score is included in the model schema.

**Operational defaults and limits:** Choose `--batch-size 8` **or** `--batch-size 16` consistently across compared methods; default `8`. `--concurrency 4` is the default and can be configured at the top of the Python script or through CLI (supported range 1..64); `--batch-retries 3` means **three additional attempts following the initial attempt**, at most four actual submissions **per batch**. The technical script accepts a natural-number batch size 1..128, but the governing protocol selects only 8 or 16. There is **no global total-request or total-retry ceiling** in this script. Azure SDK `max_retries=0` disables its hidden automatic retries. The external API request timeout defaults to 300 seconds; `--max-output-tokens` defaults to 32,000; the default confidence threshold is 0.90. Preserve the nine-file attachment identity and strict item-by-item output validation. `--dry-run` must be used to test queue parsing and partitioning without any paid request.

Example (use actual input paths and the supplied-source-derived unlimited script):

```bash
python "semantic_decision_evaluator_v10.6_unlimited.py" \
  --pdf original.pdf \
  --spec-dir ./original_markdown \
  --queue 06_llm_queue_v10.6.jsonl \
  --out-dir ./semantic_output_v10_6 \
  --concurrency 4 --batch-size 8 --batch-retries 3 \
  --confidence-threshold 0.90
```

**Prompt caching without request-wide options:** Upload the original PDF plus the eight original Markdown files once per execution and reuse their nine Azure Files IDs for every request. After constructing the nine `input_file` blocks, execute `inputs[-1]["prompt_cache_breakpoint"] = {"mode": "explicit"}` before appending the per-batch `input_text`. The marker applies to the end of the nine-file stable prefix. Do not include `prompt_cache_options` in `Responses.create()` or through an unvalidated keyword argument. Azure's default implicit caching behavior may coexist with this explicit block marker; do not promise explicit-only caching or a specific cache hit rate. Log actual `usage.input_tokens_details.cached_tokens` and `cache_write_tokens` when returned, and print `n/a` when absent instead of assuming zero. Cache reuse and pricing must be based on real Azure usage records. Explicit breakpoints require deployment support; a 400 structural rejection stops the run without blind retry.

**Required stdout format:** Print thread-safe elapsed-second events in `[elapsed=     1.3s] EVENT      | details` format. Emit `QUEUE`, `SCOPE`, `SOURCES`, `NOTICE`, `INITIAL`, per-file `UPLOAD`/`UPLOADED`, `CONFIG`, per-batch `START`/`COMPLETED`/`USAGE`, per-item `ITEM`, cumulative `SUMMARY`, and `FAILED`/`RETRY`/`ERROR`/`INTERRUPTED`/`FINISHED` as applicable. Include batch ID, position, item count, attempt, committed count, duration, journal and the actual token/cache fields. Log `ALIAS` events with reported/resolved source names, role, digest and verification result for every generated citation; do not print entire confidential quotation bodies. Summary counts are **v5 item suggestions**, not canonical TP/TN/FP/FN results. The sample console log is a formatting model only; its v10.5 `D7-*` judgments are not adopted. Continue to write the immutable JSON journals and output manifests regardless of console verbosity.

### 4.3 Retry, failure, and resume safeguards

The evaluator records its 10.6 configuration, selected batch size, nine-source explicit cache breakpoint, and **filename-alias policy identity** in resume identity, and each submission intent in `run_state.json` **before dispatch** and records each completed batch as an atomic, hash-validated JSON journal. The aggregate `semantic_decisions.jsonl` is reconstructed from committed journals in original queue order. Check source file hashes, queue hash, prompt hash, output-schema hash, model/endpoint, batch size, confidence threshold, **filename-alias policy identity** and run settings before resume. An old journal/run state using strict basename lookup must not be silently resumed with a new verifier; preserve the original journals and create separately identified corrected audit records or a fresh run. Reuse uploaded nine-file IDs when possible; do not silently resubmit a committed batch.

**Automatic retry is limited to explicit HTTP 429 and explicit invalid/incomplete model responses**, with bounded exponential backoff and remaining per-batch attempt capacity. A possibly billed network failure, ambiguous uncommitted response or interrupted submission is **never** automatically retried. Require an explicit `--resume --retry-ambiguous` authorization after examining `run_state.json`; even authorized resubmission consumes the batch's remaining attempts. Structural SDK/API or source errors stop submissions. An output with missing, duplicate, reordered, mismatched or malformed item results is invalid **as a whole batch**, not partially accepted. Once four attempts are exhausted, write a failure record with no invented LLM result, and mark the handoff incomplete.

**Retry budget arithmetic:** Let `b` be the chosen protocol batch size (`b ∈ {8,16}`), and let K be the nonnegative full pending-item count. There are `ceil(K/b)` primary batches and at most `4*ceil(K/b)` actual submissions **if every batch uses all three additional retries**. The final batch may contain 1..`b` items. When `K=0`, there are zero batches and no external submissions. There is no fixed total-batch ceiling or cross-method total-submission ceiling. These are worst-case request counts for the actual K, not a desired usage target. Actual retries and Azure costs must be logged; never claim cached-token savings without usage data. Adjusting concurrency on resume is allowed; changing the source/queue/model/decision configuration is not.

### 4.4 External outputs versus canonical accounting

`semantic_decision_evaluator_v10.6_unlimited.py` writes `semantic_decisions.jsonl`, `semantic_summary.json`, `run_state.json`, `batch_journals/`, and, for failures, `failed_batches/` and `failed_batches.jsonl`. Each `SEMANTIC_RESULT` includes `batch_id`, `batch_index`, `batch_size`, `suggested_decision`, `decision_status`, `review_reason_code`, model JSON, evidence checks, source hashes and response identity. A v5 suggestion may be `TP`, `FP`, `FN`, `TN`, `NOT_FP`, `FP_CANDIDATE`, `EXCLUDED_NONDEFINITIVE`, or JSON null according to the unchanged `suggest()` rules.

`decision_status=PROPOSED` does not mean independently adjudicated population-level truth. `decision_status=UNRESOLVED` and `suggested_decision=null` must not be coerced into negative cells **inside the v5 script or by a blind post-processing rule**. Phase 07 must instead inspect the original files and make its own four-cell decision under §7. The script sets `final_cell_not_committed=true`, and its `semantic_summary.json` explicitly states `no_final_tp_tn_fp_fn_totals_produced=true`.

**Previously produced results affected by the filename defect:** Stop the defective process before further paid requests. When the original source bytes, recorded SHA-256 per source role, model JSON, queue ID and item identities are all available, run an **offline source-verified revalidation** over already committed `SEMANTIC_RESULT` model JSON. Never change the original journals, `semantic_decisions.jsonl`, raw `model_json`, or originally logged suggestion/status. Write a new independently named superseding *validation* artifact containing the old and corrected `check_evidence()` results, reported/resolved filenames, original/derived suggestion and reason code, complete immutable input hashes, and an explicit audit link to each original item. Recompute the v5 `suggest()` function on the original unchanged model JSON using unchanged threshold. This is a newly recorded technical correction, not a retroactive LLM output or a final Phase 07 cell. Rows with another evidence defect, subjective confidence below 0.90, or PARTIAL remain unresolved. If any source digest or role identity disagrees with the frozen execution, abort revalidation. Do **not** use a fresh execution with changed settings to `--resume` the original run or resubmit already billed items merely to repair filenames; separately document any new batch submissions needed for still-unrun items. **Do not demand Phase 07, Phase 08 or Phase 09 artifacts from this script.** Phase 07 independently creates assistant decisions; Phase 08 separately builds `08_final_ledger.jsonl` and `08_binary_counts.json`; Phase 09 computes metrics. All phases retain the same substantive entailment and canonical counting definitions as the original common evaluation policy.

## 5. Canonical scoring universe and metric rules

### 5.1 Scoring units (unchanged canonical definitions)

For each evaluated generation method `m` define:

```text
R_m = R  : frozen PDF-positive normative source requirements
N_m = N  : frozen PDF-negative affirmative counterfactual controls
GO_m     : eligible definitive generated occurrences
GC_m     : unique within-method definitive generated semantic classes
A_m      : {r in R : the entire generated corpus fully entails r}
B_m      : {n in N : generated corpus affirmatively asserts counterfactual n}
F_m      : distinct unsupported generated-only affirmative residuals after
           semantic consolidation, excluding overlaps with B_m
U_m      : R disjoint_union N disjoint_union F_m
P_m      : A_m union B_m union F_m
```

Supported generated classes do not add new canonical TP units. One generated clause may cover several independent source atoms when applicability is shown. Repeated unsupported text, even across eight Markdown files, yields one F residual. N/F overlap must be deduplicated, and every raw GO belongs to exactly one effective GC.

### 5.2 Four-cell meanings and equations

| Cell | Actual | Predicted | Meaning |
|---|---:|---:|---|
| `TP` | 1 | 1 | Whole source-positive requirement covered by definitive generated content |
| `FN` | 1 | 0 | Source-positive requirement substantively absent or only partially covered after adequate search |
| `FP` | 0 | 1 | Affirmed frozen negative control, or one distinct unsupported generated-only residual |
| `TN` | 0 | 0 | Frozen negative control not affirmatively asserted by generated content |

If and only if the canonical universe is fully classified:

```text
TP = |A_m|
FN = |R| - |A_m|
TN = |N| - |B_m|
FP = |B_m| + |F_m|
TP + FN = |R|
TN + |B_m| = |N|
FP - |B_m| = |F_m|
TP + TN + FP + FN = |U_m| = |R| + |N| + |F_m|
TP + FP != |GC_m| in general.
```

The v5 output `NOT_FP` only diagnoses a PDF-supported generated claim; it is **not** a new canonical TP. `FP_CANDIDATE` is a generated-only residual candidate, not an automatically counted FP until it is deduplicated and checked against the PDF/N controls. `EXCLUDED_NONDEFINITIVE` is not a negative control and adds no TN. Keep the exact original item outcome and provenance.

### 5.3 Metric computation (single comparable scale)

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN) = TP / |R|
F1        = 2 * TP / (2 * TP + FP + FN)
negative_control_pass_rate = TN / |N|  # diagnostic, not all-world TN accuracy
GC_validity_rate = PDF_supported_GC / definitive_GC
Duplicate = (|GO_m| - |GC_m|) / |GO_m|
```

No statistical extrapolation or confidence-weighted score. JSON null denominators: Precision if TP+FP=0, Recall if |R|=0, F1 if 2TP+FP+FN=0, negative-control pass if |N|=0, GC-validity if definitive_GC=0, Duplicate if GO=0. Retain unrounded machine-readable values. **Do not calculate Precision/Recall/F1 over selected K alone** or treat the K-batch coverage rate as the full-population score. A valid complete population ledger, not the number of LLM calls, authorizes arithmetic scoring.

### 5.4 Pending decisions and required full closure

Before Phase 07, count provisional pending R, N and eligible GC determinations as `UR_pre`, `UN_pre` and `UG_pre` and preserve every item ID, including failed or ambiguous external submissions. Phase 06 must have queued every pending eligible ID; an unexplained omitted ID is a Phase 06 integrity error, not a permitted selection cap. A script `UNRESOLVED` is **not** a fifth confusion-matrix cell. The full pending population is an explicit input to Phase 07, which must assign each eligible item a final evidence-grounded cell by the end of that phase.

After Phase 07 and Phase 08, require:

```text
TP + FN = |R|
TN + B = |N|
FP = B + |F_m|
UR_final = UN_final = UG_final = 0
remaining_unclassified_residuals = 0
```

A completed `R` item has exactly `TP` or `FN`; a completed `N` item has exactly `FP` or `TN`; an eligible definitive generated class has a diagnostic `TP` (PDF-supported) or `FP` (PDF-unsupported) classification and a provenance category. The diagnostic `G:TP` contributes **zero** extra canonical TP because canonical TP comes exclusively from R. Generated-class FP is consolidated with N-positive FP in Phase 08, with one count per distinct unsupported residual. Excluded nondefinitive passages are not eligible predictions and are not assigned a fabricated TN.

The assistant's independent classification does not require the v5 model to reach confidence 0.90 or `FULL`: Phase 07 inspects original evidence and applies a deterministic written decision rule, documenting its conclusion even when the v5 model abstained. If original required materials are missing or corrupt, stop with `INCOMPLETE` and an exact blocker rather than emit arbitrary labels. Phase 09 may compute numeric metrics only from a fully classified, hash-consistent and deduplicated Phase 08 ledger; never calculate scores over selected external K alone.

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

For each method, `09_metrics.json` and the report show the fixed R/N counts and digests; GO/GC and duplicate totals; classified TP/FN/TN, affirmed N and generated-only residual FP; and the exact pre-Phase-07 unresolved R/N/GC/FP candidate counts and how each was adjudicated. Show **one** arithmetic Precision/Recall/F1 set from the complete Phase 08 canonical ledger; if inputs are genuinely missing or integrity checks fail, report a blocked run with no score. Include `TRUE_MISSING`, `PARTIAL_ENTAILMENT`, corrected matcher misses, and assistant-corrected v5 uncertainty as distinguishable audit categories; do not classify an item as FN solely because the script abstained. Include supported-noncovering GCs, original PDF/G support, N/F overlap exclusions, verified contextual/conjunctive bridges, and exact duplicate-class decisions.

Report the immutable Phase 06 queue SHA-256, K, batch size/concurrency, per-batch retries and actual submission counts, the actual reasoning effort `high`, the original v5 `confidence_estimate` and evidence checks, the original `suggested_decision`/`decision_status`, originally unresolved proposals, Phase 07 final decisions and all assigned canonical labels. The v5 model-confidence value is not measured correctness. Do not report a raw `GC` count as TP/FP or claim a historically high score proves the new run correct. For cross-method comparison, confirm exhaustive method-invariant external selection (`K=C`) and zero items omitted due to numerical budget; any unresolved external outputs are resolved by Phase 07 under an identical policy.

## 6. Nine ordered phases

| Phase | Required work | Principal outputs | Completion gate |
|---|---|---|---|
| **01 — Reference lock** | Validate explicitly supplied generation method, 90-page PDF, all eight original Markdown roles and digests; validate/freeze supplied R/N manifest; record atomization exceptions without changing frozen data | `01_reference_lock.json`, source/ref manifest | Fixed identity and scope; no generated coverage inference |
| **02 — GO/GC extraction** | Scan every substantive generated paragraph and table row with inherited context; extract eligible complete GO/GC, exclusions and duplicates | `02_generated_atoms_final.jsonl`, `02_generated_classes_final.jsonl`, `02_excluded_units.jsonl`, `02_duplicate_classes.jsonl`, `02_original_text_index.jsonl` | Each substantive original occurrence accounted for; duplicate grouping audited |
| **03 — R coverage discovery** | Search all eight specifications for every R; verify source and generated candidates, universal/contextual bridges | `03_source_coverage.jsonl`, `03_semantic_coverage_bridges.jsonl` | All R indexed with actual evidence or explicit uncertainty |
| **04 — TP/FN reciprocal audit** | Challenge every proposed miss and check every provisional TP for full predicate support | `04_coverage_audit.jsonl`, `04_tp_evidence_audit.jsonl`, `04_fn_root_cause_audit.jsonl` | No mere retrieval miss treated as proven FN |
| **05 — Generated validity** | Reassess exclusions, recover missed definitive assertions, inspect each effective GC against the PDF | `05_generated_claim_validity.jsonl`, `05_exclusion_reassessment.jsonl` | All GO/GC and source-to-generated evidence links accounted for |
| **06 — Negative controls, residual deduplication, exhaustive v5 external queue** | Validate the canonical/copy-suffix filename-alias regression suite and examine every N; merge equivalent unsupported residuals and eliminate N/F overlaps; freeze **every** still-pending eligible R/N/GC in a v5 `UNRELIABLE_ITEM` queue and deterministic 8-or-16-item batch boundaries | `06_fp_controls.jsonl`, `06_llm_queue_v10.6.jsonl`, `06_queue_selection.json` | `K=C` with no numerical cap, `read_queue()` compatibility, tested unique-role/digest/line/quote alias resolution, complete R/N/GC population reconciliation |
| **07 — Deterministic assistant adjudication of undecided items (NEW)** | Inspect original PDF and all eight generated Markdown files for **every** still-undecided, v5-unresolved or failed-request R/N/eligible GC; independently decide TP/FN, FP/TN and diagnostic G:TP/FP under fixed §7 rules; preserve the original v5 judgment separately | `07_assistant_adjudications.jsonl`, `07_decision_audit.jsonl`, `07_adjudication_summary.json`, `07_input_blockers.jsonl` | Every eligible pending ID has one source-grounded final binary decision; no semantic null remains; missing required originals -> `INCOMPLETE` |
| **08 — Independent semantic reconciliation (formerly Phase 07)** | Validate all v5 journals and Phase 07 decisions; reconcile immutable R/N/GC inventory, proof families, N/F overlap and unique unsupported residuals into canonical counts **without re-adjudicating Phase 07 item cells** or counting diagnostic G:TP as canonical TP | `08_final_ledger.jsonl`, `08_binary_counts.json`, `08_reconciliation_audit.jsonl` | Full canonical enumeration, crosswalk and deduplicated FP; TP+FN=R, TN+B=N; no unresolved eligible item |
| **09 — Independent metric computation and report (formerly Phase 08)** | Independently reconstruct Phase 08 counts and check source hashes, reference/GC/FP identities, equations and method comparability; compute one fully classified non-extrapolated score | `compute_metrics.py`, `09_metrics.json`, `09_report.md`, `09_coverage_and_limitations.md` | Completed population -> one numeric arithmetic score; input corruption or inconsistent counts -> stop without publishing a fabricated score |

**Operational handoff:** After Phase 06, if `K>0`, run the execution-only unbounded derivative of the supplied Version 5.0 batch evaluator against `06_llm_queue_v10.6.jsonl`, preserving per-batch journals and the original model JSON unchanged. If `K=0`, record a no-submission handoff in `06_queue_selection.json` and advance without invoking the evaluator. The evaluator is not itself an additional numbered phase. A filename-alias regression test against canonical and copy-suffixed original names is a mandatory external-handoff prerequisite; do not authorize paid evaluation merely because `read_queue()` and batching pass. The new numbered Phase 07 is performed **after** the external evaluator and **before** the previously defined reconciliation (now Phase 08). Its `protocol_version="10.6"` and `execution_version="10.6"` match the governing phase protocol. Version 5.0 refers only to the preserved decision algorithm, not to the executable version fields. Phase artifacts carry governing protocol version 10.6. Match external evidence by queue hash, source hashes, item IDs and execution fingerprint; do not fail solely because these two *explicitly different* version namespaces have different values.

## 7. Deterministic assistant adjudication (new Phase 07)

### 7.1 Meaning of unresolved and mandatory decision authority

For this protocol, **undecided** means the v5 script or earlier phase ledgers did not establish a final, accepted `TP`, `TN`, `FP` or `FN` for an eligible item. It covers `suggested_decision=null`, `decision_status=UNRESOLVED` even when a tentative `FN`/`TN` string exists, failed/ambiguous v5 responses, and any previously claimed cell rejected by independent evidence checking. The full Phase 06 queue must not omit eligible pending items merely to save API calls. It is **not** a new semantic class or a legitimate terminal score.

The assistant conducting Phase 07 **must decide**, rather than refer the case to the operator, ChatGPT in a different conversation, a second paid API, or a permanent review queue. For each pending ID, independently inspect the original 90-page PDF and all eight original generated Markdown files as relevant; use the already built full-text indices and proof-family evidence, inspect figures/tables when material, then write one final justified decision. The assistant is responsible for the decision, not merely for reporting what the v5 model proposed. Phase 07 must also detect and report any unexpected eligible pending item omitted from the externally frozen queue, as a Phase 06 selection-integrity defect; never silently call such an omission an accepted script result.

This is an **operationally deterministic adjudication policy**: the case universe, search order, evidence precedence, tie-breaking rule, label mapping and output schema are fixed, and every decision must be traceable. It does not claim that free-form semantic interpretation by an LLM is mathematically deterministic or that each decision is infallible. Do not use the model's subjective confidence score as the deciding threshold in this independent phase.

### 7.2 Fixed order of review and evidence precedence

Process the complete pending population deterministically: frozen R ID order, frozen N ID order, then eligible effective GC representative order (`01` through `08` role, physical line, row/cell, stable GCLASS ID). Resolve one item before proceeding to the next; record all examined candidates and the accepted strongest evidence. The assistant may reuse an applicable proven proof family, but each member's applicability must be checked independently.

Apply the following precedence, uniformly across all three generation methods:

1. **Original authority:** The source PDF controls what is required, prohibited or supported; generated Markdown does not change the PDF's meaning. Reconstruct the entire requirement including inherited heading/table context and applicable exceptions. The frozen R/N inventory remains unchanged.
2. **Eligible generated assertions:** Consider only definitive implementation/test claims. A negative prohibition is not an affirmative assertion of the prohibited behavior; examples, alternatives, deferred material and nondefinitive comments cannot create FP.
3. **Complete meaning, not a keyword match:** Accept direct semantic equivalence or a valid general-rule-plus-applicability or cross-file conjunction only where all essential premises are stated and effective. An unrelated mention, omitted exception, weakened scope, incompatible modality or missing required testing duty is not complete coverage.
4. **Conflicts and specificity:** Read the applicable exceptions and stronger specific rules before applying a general rule. For R, contradictory definitive generated requirements prevent an unqualified `TP` on that obligation. For N, a definitive affirmative prohibited behavior constitutes FP even if another generated paragraph says it is prohibited; do not erase the affirmative contradiction.
5. **Negative conclusion only after reciprocal inspection:** For a putative R omission, recheck the strongest candidate and all applicable other files. For a putative N nonassertion, search affirmative and negated alternatives, aliases and cross-file claims. For G unsupportedness, search the **entire PDF** rather than only the frozen R inventory.
6. **Stable ties:** If two surviving interpretations are both plausible, prefer the one supported by complete, explicit, scope-valid original statements and documented original locators over an inference requiring unstated premises. If no complete entailment survives after the full admissible search, apply the direction-specific noncoverage rule below, with the best near-match and exact unmet predicate documented. Never break a tie based on which method obtains the better historical metric.

### 7.3 Terminal direction-specific decisions

Apply these rules **after** the full review, not by mechanically converting `PARTIAL`, `NOT_FOUND`, `UNRESOLVED`, low confidence, or a failed request:

| Eligible item | Final Phase 07 decision rule | Required cell |
|---|---|---|
| `R` (frozen PDF-positive) | The eight generated files jointly and consistently entail the complete source obligation under valid scope and context. | `TP` |
| `R` (frozen PDF-positive) | After cross-file review, one or more essential source predicates remain absent, weaker, inapplicable or contradicted; explicitly record the best partial match and the gap. | `FN` |
| `N` (frozen PDF-negative control) | At least one definitive generated assertion affirmatively entails the prohibited counterfactual. | `FP` |
| `N` (frozen PDF-negative control) | No eligible definitive assertion affirms the counterfactual after complete reciprocal inspection. | `TN` |
| `G` (eligible definitive generated semantic class) | The complete generated proposition is entailed by the original PDF, whether or not it matches a frozen R atom. | Diagnostic `TP` (PDF-supported; **not** an additional canonical R-TP) |
| `G` (eligible definitive generated semantic class) | Its whole claim is not supported by the PDF, or a material affirmative residual is contradicted/unsupported after full original-PDF inspection. | Diagnostic `FP` (candidate for N/F consolidation in Phase 08) |

Every active `R`/`N` must end in one of the four genuine canonical cells according to its direction; every eligible `G` must end in a supported `TP` or unsupported `FP` **diagnostic** decision, and the Phase 08 deduplication contract controls counting. A nondefinitive generated passage is outside the scored GO/GC population, not a fabricated `TN`. A partial source requirement is `FN` only after its actual essential remainder is demonstrated; an unsupported generated class is `FP` only after the full PDF has been examined for support. Do not convert a source R absence into a generated FP or vice versa.

### 7.4 Evidence record and audit obligations

Write one final `ASSISTANT_ADJUDICATION` JSONL record per pending item with at least:

`item_id`, `direction`, `method`, `final_cell`, `canonical_counting_scope`, `decision_rule_id`, `source_pdf_sha256`, `generated_file_sha256`, `pdf_evidence`, `generated_evidence`, `examined_candidate_ids`, `support_bridge_ids`, `unmet_predicates_en`, `decision_reason_en`, `decision_origin="PHASE07_ASSISTANT"`, `prior_v5_suggested_decision`, `prior_v5_decision_status`, `was_external_llm_selected`, and `source_reference_unchanged=true`.

Additional required controls:

- Where the model reported a canonical/copy-suffixed Markdown alias, preserve that reported name and verify the unique actual role, frozen file SHA-256 and original line quotation before transferring a proof to Phase 07.
- Quote text must be verifiable against physical PDF pages and exact original Markdown file lines. In an absence decision, evidence includes the strongest inspected near-match and a specific missing obligation; do not invent a nonexistent quotation to prove absence.
- Explicitly log disagreement with the v5 suggestion and why the original evidence warrants the final label. Preserve immutable v5 model JSON and original scripts, and never overwrite the v5 journal to make it agree.
- Preserve fixed rule IDs: `P7-R-TP`, `P7-R-FN`, `P7-N-FP`, `P7-N-TN`, `P7-G-SUPPORTED`, `P7-G-UNSUPPORTED`. `G:TP` is tagged `G_DIAGNOSTIC_NOT_CANONICAL_TP`; `G:FP` is tagged `G_FP_CANDIDATE_NEEDS_PHASE08_DEDUP`.
- Never emit `BEST_EFFORT`, a mandatory eleven-dimensional predicate array, an `unreliable` outcome column, or a fifth scored class. Decision uncertainty can be explained in `decision_reason_en`, but must not be substituted for the required binary cell when source files are intact.
- Do not ask the user to choose the cell or delegate the decision back to them. The assistant carries out and records the full Phase 07 work during that phase, rather than promising asynchronous review.

### 7.5 Mandatory completion gate

Produce `07_assistant_adjudications.jsonl`, `07_decision_audit.jsonl`, `07_adjudication_summary.json` and `07_input_blockers.jsonl`. The summary enumerates all original R/N/eligible GC IDs, earlier accepted cells, initially pending cells, Phase 07 final decisions and source digests. Require exactly one final decision for every previously undecided eligible ID; no duplicated IDs, no missing items, and **zero final semantic `UNRESOLVED`/null cells**. Assert `TP+FN=|R|` and `FP_N+TN=|N|` at the item level before starting Phase 08.

If a required original source is unreadable, absent, wrong-hash or demonstrably corrupt, report the precise blocker in `07_input_blockers.jsonl`, mark Phase 07 `INCOMPLETE` and stop; **do not fake a cell without the materials needed for an evidence-grounded evaluation**. Semantic difficulty, model abstention, low confidence, a partial generated match or API retry exhaustion are not valid reasons to leave an otherwise reviewable item undecided. Complete Phase 07 in the active turn before advancing to Phase 08.

## 8. Phase 08 independent semantic reconciliation and record contracts

### 8.1 Required Phase 08 ledger kinds

- `FINAL_SOURCE`: exactly one row per frozen R ID; `scoring_cell=TP/FN` with original PDF/generated evidence, including the Phase 07 decision provenance where applicable.
- `FINAL_CONTROL`: exactly one row per frozen N ID; `scoring_cell=FP/TN`; confirm polarity and definitive affirmative generation before any FP.
- `FINAL_CLASS`: exactly one diagnostic row per effective eligible GC; `diagnostic_cell=TP/FP` plus `PDF_ENTAILED`, `SUPPORTED_NONCOVERING` or `PDF_UNSUPPORTED` provenance. Supported generated classes add **no** automatic canonical TP/TN; the class-level supported label is diagnostic only.
- `FINAL_RESIDUAL`: exactly one canonical FP row for each distinct unsupported generated-only affirmative residual, **excluding** semantic overlap with an asserted frozen N. Merge semantically equivalent unsupported residuals across files and classes before counting.

Every accepted source/support claim records its original IDs, PDF physical pages and quotations, actual Markdown filename and line context, source hashes and justification. Reconcile any inconsistent provisional source/candidate judgments by examining the fixed Phase 07 decision records, not by silently changing labels. If an item-level semantic inconsistency remains, Phase 08 must **stop**, issue an `08_reconciliation_audit.jsonl` contradiction record, and require an explicit source-grounded **Phase 07 superseding adjudication** (new immutable decision record referencing the old one). Phase 08 must never generate an independent replacement `TP`/`TN`/`FP`/`FN`, nor silently change a Phase 07 cell. After Phase 07 has been correctly superseded and verified, resume Phase 08 reconciliation. The final ledger may not contain null or contradictory active cells for one ID. Never add `BEST_EFFORT`, `D7-*` binary fallback or eleven-dimensional output columns. `reasoning_effort=high` is external execution metadata, not a decision-quality category.

### 8.2 Example Phase 08 source row (illustration only)

```json
{"record_type":"FINAL_SOURCE","source_id":"PDF-EXAMPLE","method":"twolevel","scoring_cell":"TP","decision_origin":"PHASE07_ASSISTANT","pdf_evidence":[{"physical_page":1,"quote_en":"<illustrative source quotation>"}],"generated_evidence":[{"file":"02_api.md","line_start":1,"line_end":1,"quote_en":"<illustrative generated quotation>"}],"llm_item_id":"PDF-EXAMPLE","note_en":"Illustration only: complete scoped entailment verified."}
```

This is an illustrative schema, **not** evidence that the quoted content exists. Real rows must contain authentic source quotations and verified locators, not placeholders. A complete classification must carry an auditable support trail.

### 8.3 External batch and Phase 07 decision acceptance

Accept only entire committed external journals matching source PDF/Markdown digests, queue SHA-256, batch ID/index/size, ordered IDs, `RESULT_SCHEMA` and verifiable original quotations. A batch requires exactly its declared number (8, 16, or a final partial batch) of distinct complete original model results; never silently discard a member or manufacture a failed response. Persist the original `suggested_decision`, `decision_status` and `review_reason_code` unchanged. An external model confidence estimate is not independently calibrated proof.

Independently validate each Phase 07 final decision, source quote, evidence bridge, scoped rule and target ID. Account for all items omitted from the external queue. For a failed batch, rely on a **separate Phase 07 assistant decision grounded in originals** rather than creating a fake LLM response or treating an API failure as FN/TN/FP. The complete Phase 08 ledger, not the external evaluator, is authoritative for counts.

## 9. Independent metric recomputation (Phase 09)

`compute_metrics.py` independently validates:

1. All frozen R/N/PDF SHA-256 values and eight Markdown file hashes, actual 90-page PDF count, role mapping, declared generation method and protocol 10.6 phase ledgers.
2. All effective R/N/GO/GC IDs and their immutable supersessions; each eligible GO mapped to one current GC and every substantive original passage accounted for.
3. Source-grounded Phase 07 decisions and final Phase 08 TP/FN, N FP/TN and consolidated generated-only residual FP classifications; checks that `TP+FN=|R|`, `FP_N+TN=|N|`, and `FP=FP_N+|F_m|`.
4. Every pending eligible item is queued exactly once, and every selected queue item and batch journal uses the **unchanged Version 5.0 per-item judgment contract**, including `K=C`, `ceil(K/b)` batches for a fixed `b ∈ {8,16}` (including the explicitly skipped `K=0` case), correct IDs/order and complete per-item model results **for committed batches**; at most four actual submissions per batch, hashes/prompt/config identity and explicit failure/ambiguous submission reasons. Failed batches are not fabricated as successful external model results; they must instead be covered by Phase 07 assistant decisions.
5. The original v5 `suggest()` semantics and default threshold `0.90`, with the §3.1 unique-role/SHA-256 filename-alias and original-line regression suite passing **within the 10.6 external script using unchanged v5 semantic judgment logic**; no hidden edit to `PARTIAL`/`UNRESOLVED` behavior, extra eleven-dimensional output or `BEST_EFFORT` gate. Distinguish the Phase 07 independent decisions, based on the fixed §7 rules, from original v5 suggestions.
6. N/F overlap, unique residual units, supported-noncovering claims, nondefinitive exclusions and within/across-file semantic deduplication. No raw GO/GC count substitutes for a canonical TP/FP unit; diagnostic `G:TP` adds no canonical TP.
7. Verify zero unclassified eligible items after Phase 07 and Phase 08, valid evidence trails, and complete residual reconciliation; then calculate the canonical equations in §5.2 and one non-extrapolated numeric Precision/Recall/F1 set according to §5.3. A source-corruption or integrity blocker stops the scoring phase with exact errors, rather than constructing a fake complete matrix.
8. The report and machine-readable results agree on totals and statuses. Historical comparisons require identical frozen R/N, Phase 07 decision rules, GC/FP deduplication and classification policy across `fullload`, `onelevel`, and `twolevel`.

The code must fail fast for corrupted originals or mandatory integrity failures. The v5 model's uncertainty is an **input** to the Phase 07 adjudication obligation, not a reason to skip final classification. A valid file upload or 100% API-call completion does not, by itself, constitute evidence of correctness.

## 10. Completion statuses and reporting boundaries

- `PHASE_COMPLETED`: All enumerated work, original-source inspection, required final decisions and artifacts for the current phase are complete. Phase 07 specifically requires **zero undecided eligible items**.
- `INCOMPLETE`: Mandatory input, source access, queue identity, journal integrity or phase execution is missing, corrupt or incompatible; record the specific blocker and do not fabricate a scoring cell.
- `BLOCKED_REFERENCE` / `INVALID_REFERENCE_CHANGED`: Original PDF/frozen benchmark identity or checksum failure; stop and never silently replace the frozen reference.
- `FINAL_COMPLETE`: All **nine** phases, every canonical R/N and eligible GC/residual item independently accounted for, Phase 07 adjudication complete, Phase 08 deduplication complete and Phase 09 computing one comparable numeric metric set.
- `FINAL_INCOMPLETE`: A genuine input/integrity blocker prevents Phase 07 completion or Phase 08 consistency. Do not mislabel ordinary v5 `UNRESOLVED` as a blocker; Phase 07 must resolve it from originals.

**Interpretation:** Metrics quantify comparison with the fictional OrionDesk PDF design baseline, not implementation correctness or general model accuracy. Strong historical MapReduce scores are a **measurement-consistency diagnostic**, not a target for label changes. The entire original v5.0 prompt and decision policy remain fixed across generation methods; **this revision retains the governing nine-phase workflow, removes all arbitrary atom/item-count and external-selection ceilings, and makes Phase 07 the exclusive item-level final-adjudication authority. The derived 10.6 evaluator disables `--limit` truncation, adds elapsed stdout logs, configurable 8/16 protocol batch size and concurrency, and marks the ninth input-file block with an explicit cache breakpoint; the supplied original evaluator remains untouched. `SYSTEM_PROMPT`, `RESULT_SCHEMA`, `suggest()`, the default 0.90 confidence threshold and `reasoning_effort="high"` remain unchanged. The `check_evidence()` filename lookup is amended only to accept unique-role, SHA-256-verified canonical/copy-suffix aliases while retaining exact page/line/quotation verification.**
