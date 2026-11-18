# OrionDesk AI — Evidence-First Atomic Specification Evaluation Protocol

**Protocol version:** 8.1  
**Design status:** Output-minimized revision of version 8.0. The evidence rules, semantic standards, metric definitions and twelve-phase dependencies are retained; only artifact packaging and redundant reporting are consolidated.  
**Purpose:** Evaluate how completely and faithfully eight AI-produced software design specifications represent a fixed, PDF-grounded reference of atomic requirements.  
**Execution model:** Twelve ordered phases, with traceable checkpoints and minimal mandatory file output. No fixed six-turn deadline.  
**Operator environment:** ChatGPT with access to the supplied files and ordinary local parsing/search scripts. A dedicated external coding agent is not required.  
**All authored file contents:** **English**, including Markdown, JSON/JSONL values, audit reasons, program comments, reports, and log messages. Exact quotations may preserve the original source language.  
**Top priority:** Evidence-grounded semantic accuracy over speed, phase count, estimated scores, or appearance of completion. Do not generate low-value auxiliary files.

## 0. Version 8.1 file-minimization policy

**Strict output budget:** Emit **one consolidated required artifact per phase in Phases 01–11**, and only **three essential artifacts in Phase 12** (a metrics calculator, machine-readable metrics, and a combined human-readable report). Thus, **14 mandatory deliverable files in total**, rather than version 8.0's 53 files. Do not produce separate search-receipt, unresolved, exclusion, duplication, equivalence, reconciliation, challenge, change-log, limitation, evidence-audit or delivery-manifest files; embed their necessary records in the designated consolidated artifact. All of their **checks and substantive evidence obligations remain mandatory**.

- **Only evidence-bearing data is worth writing.** Every frozen source ID, eligible generated occurrence, exclusion/coverage disposition, generated class, canonical residual, negative control and material challenge must remain traceable. The consolidation changes storage layout, **not** the evaluation population, source authority, semantic decisions, audit thresholds or scoring formulas.
- **Do not write repeated copies.** Do not replicate a completed three-shard source ledger in Phase 07, an earlier PDF ledger in Phase 09, or all pre-challenge ledgers in separate final files. Reference unique earlier IDs where the exact record already exists and build **one coherent, post-challenge final ledger** in Phase 11.
- **Compact serialization.** Use UTF-8 JSONL with one compact JSON object per row, stable IDs, a `record_type` discriminator, and no pretty-print whitespace. Include only evidence quotations needed to prove each decision, exact locators and enough context to recover qualifications. Use direct `source_id` references for already-frozen source evidence instead of duplicating its full text needlessly. Never omit a material predicate, necessary counterevidence, search scope, uncertainty reason, or complete occurrence-to-class link for brevity.
- **Inline audit data.** Store search query variants, corpus scope, inspected candidate IDs/locators, strongest selected quotations, rejected-candidate reasoning, bridge evidence, exclusions, reconciliation totals and open issues **inside the item or summary records**. No separate file is required merely to carry a `search_receipt_id`.
- **Temporary computation is allowed but not a deliverable.** Scripts, indexes, extracted PDF text, microbatch prompts/responses and working tables may exist in local temporary storage to support genuine checking. Do not export them as user deliverables, create ZIP archives, write narrative progress logs, or generate interim Markdown reports unless the operator explicitly requests them. Remove redundant temporary artifacts from the deliverable directory. Do not represent unavailable evidence as completed to save time.
- **Per-phase gate remains strict.** One consolidated phase file must include an explicit `PHASE_SUMMARY` (or its JSON equivalent for Phase 01) with input counts, output counts, ID completeness, acceptance-check results, unresolved items and phase status. Do not advance until the phase is truly complete under Section 8. For a phase that cannot finish in one interaction, keep a durable local checkpoint for resumption; expose only the required final phase artifact after the gate is met.
- **Immutability and final reproducibility remain strict.** Never modify the frozen positive/negative references or a previously completed phase artifact to hide a change. Phase 11 carries item-level corrected snapshots plus append-only `CHANGE` records with affected IDs. Phase 12 recomputes from that final ledger, validates reference hashes and original phase coverage, and includes a compact delivery inventory inside `12_metrics.json`.

## 1. Mission and non-negotiable boundaries

This protocol scores **generated specifications**, not the quality of the upstream Gold Set construction workflow. Its inputs are a frozen set of source-positive requirements, a frozen bounded set of negative controls, the authoritative source PDF, and eight generated Markdown specifications. It must not extract a new Gold Set, modify the supplied reference, or silently adapt requirements to make a method appear better or worse.

### 1.1 Mandatory inputs

| Role | Canonical name | Required interpretation |
| --- | --- | --- |
| Positive reference | `common_atomic_reqs.jsonl` | Frozen `R` atoms, keyed by `source_id`, with `actual_label=1` and PDF evidence |
| Negative controls | `common_negative_controls.jsonl` | Frozen `N` counterfactuals, keyed by `negative_control_id`, with `actual_label=0` |
| Reference metadata | `reference_freeze.json` | Reference version, recorded digests, provenance, freeze status and limitations |
| Authoritative PDF | `OrionDesk_AI_Detailed_Design_Specification.pdf` | Original semantic authority for evaluating generated statements |
| Generated specification 1 | `01_screen_functions.md` | Screen functions |
| Generated specification 2 | `02_api.md` | API contracts |
| Generated specification 3 | `03_data.md` | Data contracts |
| Generated specification 4 | `04_batch_functions.md` | Batch and background processing |
| Generated specification 5 | `05_business_rules.md` | Business rules |
| Generated specification 6 | `06_exception_handling.md` | Exceptions and failure handling |
| Generated specification 7 | `07_processing_flows.md` | Processing flows |
| Generated specification 8 | `08_architecture_decision.md` | Architecture decisions, including explicit unresolved proposals |

A harmless upload-copy suffix such as `(3)` is allowed. Resolve each role **unambiguously**, record the exact actual filename, and hash the actual bytes. Do not use historical files just because their basename looks familiar. The eight-file bundle is evaluated as one corpus for one declared method. If the method (`fullload`, `onelevel`, `twolevel`) cannot be established from explicit operator input or trusted file provenance, label it `unattributed`; never infer the method from quality or file naming alone. Compare methods only when their reference version, evaluator, scoring policy and provenance are genuinely aligned.

### 1.2 Freeze and source authority

1. Before any classification, record SHA-256 of both reference JSONLs and of the PDF; compare with `reference_freeze.json`. Fail the phase if a required expected hash and actual hash disagree. A filename difference with identical bytes is acceptable only when documented.
2. From that point forward, `R`, `N`, their IDs, their text, and their exact bytes remain immutable. No normalization, merging, splitting, filtering, rewording, or repairs are permitted in the evaluation workspace, including temporary “corrected” copies.
3. Assume `R` is the complete positive requirement inventory for **this benchmark**, even if the upstream freeze record discloses unresolved validation limitations. Do not conduct an independent Gold Set completeness audit.
4. Nevertheless, consult the PDF to determine whether a **generated claim** is supported. A generated claim supported by the PDF but not matching a frozen `R` ID is `SUPPORTED_NONCOVERING`, not FP, and does not create a new TP or change `R`.
5. If a supplied frozen atom conflicts materially with the PDF while adjudicating a generated claim, create a `REFERENCE_EXCEPTION` record with the fixed ID, exact PDF evidence and the scoring impact. Do not edit the atom. Material exceptions may block verified scores.
6. Rehash all source files before the final report. If either reference ledger changes, classify the run `RUN_INVALID_REFERENCE_CHANGED`, do not publish comparable scores, and start a fresh run under an explicitly new reference version.

### 1.3 Accuracy rules

- A retrieval score, embedding similarity, text overlap, regex, matching number, or exact keyword search is **candidate discovery, not semantic judgment**.
- A claim is not FP because it has no one-to-one match in `R`; its complete meaning must be checked against the PDF.
- A source requirement is not FN because it lacks matching words; check universal rules, inherited context, aliases, tables, and combinations across all eight files.
- `UNRESOLVED` is **not automatically FP or confirmed FN**. It is an explicit unfinished judgment with quantified possible effect on the metrics.
- Different endpoints, objects, actors, conditions, error codes, timing, versions, exceptions or outcomes are not duplicates merely because their sentences look alike.
- A repeated statement across seven specifications does not become seven TPs or seven FPs. Preserve every occurrence, count the canonical proposition once in its proper scoring view, and classify why each excess occurrence exists.
- `TBD`, missing contracts, suggestions, examples, possible alternatives and unanswered architecture questions do not assert implemented behavior. An explicitly adopted and definitive architecture decision can be scored.
- Original evidence must be quoted or pinpointed; invented quotations, claimed searches that were not run, fictitious second reviewers and substituted evidence are prohibited.
- Do not optimize toward a prior score or method ranking. Prior charts may inform a **sanity investigation**, never labels or score targets.

## 2. Units, semantics and permitted outcomes

### 2.1 Objects

For a selected generated corpus `m`:

| Symbol | Meaning |
| --- | --- |
| `R` | Fixed source-positive atomic requirement records |
| `N` | Fixed, bounded source-negative control records |
| `GO_m` | Eligible generated **atomic commitment occurrences** from all eight files |
| `GC_m` | Distinct generated semantic proposition classes; each class retains every member occurrence |
| `COVERED_R` | Source atoms fully entailed by eligible generated evidence |
| `MISSING_R` | Source atoms not fully entailed **after completed reciprocal eight-file evidence search** |
| `UNKNOWN_R` | Source atoms whose coverage remains materially unresolved or whose search was incomplete |
| `SUPPORTED_G` | Generated classes whose complete material predicates are PDF-supported |
| `INVALID_G` | Generated classes with confirmed unsupported or contradictory material predicates |
| `UNKNOWN_G` | Generated classes whose full PDF support remains materially unresolved |
| `F_CONFIRMED` | Distinct canonical unsupported/contradicted generated residual propositions after corpus-wide deduplication |
| `F_UNKNOWN` | Distinct possible unsupported residual propositions awaiting resolution |
| `B` | Frozen negative-control IDs affirmatively asserted by definitive generated claims |

Each generated class is one **complete independently testable proposition**, including inherited qualifications. Normalize actor, action, object, logical polarity, modality, scope, precondition, exception, timing, version, quantity, error/outcome and authority. Split a sentence only when it actually makes independent testable commitments. Never create artificial atoms from headings or isolated table values; reattach the row/column/section context first. Preserve independent changes in actor or scope.

### 2.2 Three-valued evidence outcomes, not guessed binary labels

**Source-to-generated judgment for each `source_id`:**

- `COVERED`: every material source predicate is entailed by definitive generated content, supported by actual locators. Grade `E3` = direct complete match; `E2` = complete, explicitly proven universal/contextual/cross-file entailment.
- `MISSING_CONFIRMED`: exhaustive prescribed search and contextual review are complete; no eligible generated evidence fully entails the atom. Report the strongest partial evidence and missing predicates. Grade `E1` = incomplete overlap; `E0` = no valid entailment found after the full audit.
- `COVERAGE_UNRESOLVED`: incomplete search, unresolved scope, conflicting evidence or incomplete semantic judgment. Record what was checked and exactly what remains uncertain. Never describe it as a proven omission.

**Generated-to-PDF judgment for each `class_id`:**

- `PDF_SUPPORTED`: the PDF entails every material predicate; attach real quotations and context. The class may cover several `R` IDs or zero.
- `PDF_UNSUPPORTED`: at least one specific material predicate is not supported or contradicts the PDF, after a completed evidence search. List exactly which part fails and create appropriate canonical residual FP candidates.
- `PDF_UNRESOLVED`: material evidence is insufficient to make either decision. Keep the most relevant PDF evidence and a precise missing-proof statement; do not call it a fabrication.

**Negative-control judgment for each `negative_control_id`:** `ASSERTED`, `NOT_ASSERTED_VERIFIED`, or `ASSERTION_UNRESOLVED`. Only an eligible, definitive generated assertion with the same material scope and polarity triggers `ASSERTED`. Mere mention, prohibition, quotation of a test counterexample, and discussion of an unadopted proposal do not trigger it.

### 2.3 Explicit entailment and contradiction tests

For every judgment, ask in order:

1. What is the full source or generated proposition after restoring table, heading, section and inherited universal-rule context?
2. Who acts, on which object, under which permission, precondition, scope, version and timing?
3. What outcome, field, status, failure behavior, limitation or exception is required?
4. Does cited evidence entail **all** these predicates, not just address the same topic?
5. Does any stronger contradictory or scoped exception elsewhere in the corpus change applicability?
6. For universal rules, where is the explicit membership proof that the particular endpoint/field/job/resource falls inside the rule?
7. Could the evidence establish a narrower rule but not the broader one? If so, do **not** mark full coverage or equivalence.

Use exact negative polarity. “Must reject self-approval” is an affirmative requirement to **enforce rejection**, not evidence that the system allows self-approval. An `OR` alternative does not establish both alternatives; an optional feature does not establish mandatory implementation. Do not infer a concrete HTTP error code from generic failure handling or a UI default from a database default.

## 3. Evidence discovery and model reasoning

### 3.1 Candidate retrieval (necessary but never sufficient)

Use scripts for exhaustive enumeration, UTF-8 decoding, offset preservation, inverted indexes, identifier and alias retrieval, source-page indexing, lexical/semantic candidate ranking and arithmetic. For each source atom, search **all eight** generated files by:

- Exact identifier, path/method, entity/field, event, status/error code, constraint and numerical value;
- Accepted aliases and terminology variants;
- Semantic paraphrases of actor/action/target/conditions;
- Relevant global/universal rules, shared preambles, appendices, table headers and cross-document conjunctions;
- Contradictory claims and exceptions.

For each generated class, search the **entire original PDF** for source support, both direct and paraphrased, plus common rules and the surrounding tables/sections. Retrieve enough surrounding text to preserve modality and scope. PDF page images/figures must be inspected when visual or table content materially governs a judgment. PDF citations use **physical 1-based page numbers** with section/table/figure identifiers and, when possible, exact extracts.

A top-k similarity result alone cannot certify absence. Retain **search receipts**: search queries, corpus files/pages examined, candidate IDs, candidate text/locations, any broad-rule retrieval, rejected candidates and why the predicates failed. Do not falsely write `searched_all_eight=true` if the check was not performed.

### 3.2 Required LLM semantic adjudication

An LLM must actually read the candidate evidence and apply the entailment questions in Section 2.3. This is the **decision step**, not a programmatic threshold test. Parsers and similarity scores are allowed to propose candidate links, never to assign final `COVERED`, `MISSING_CONFIRMED`, `PDF_SUPPORTED`, `PDF_UNSUPPORTED`, `ASSERTED`, or semantic-equivalence labels on their own.

Process the corpus in **small, traceable microbatches** (recommended 25–60 decisions per LLM context, reduced further for dense tables or complex claims). Give each microbatch a complete evidence pack and return **one judgment for every requested ID**. Scripts must reconcile input IDs against returned IDs, detect omissions and restart only incomplete microbatches. Do not silently mark unprocessed IDs `MISSING` or `PDF_UNSUPPORTED`.

For each nontrivial decision record: `item_id`, `evidence_ids`, actual quotations/locations, predicate-by-predicate reasoning, entailment/contradiction finding, confidence/uncertainty explanation, and `adjudication_origin` (`LLM_SEMANTIC` versus mechanical checks). If the model cannot inspect enough source context, mark it unresolved with a documented blocker or continue the **same phase**; do not manufacture a determination.

### 3.3 Decision quality and independence

- The primary LLM judge must be **source-blind to the prior result labels** for an item when feasible; prior numerical scores and the preferred comparison method must not be provided as adjudication evidence.
- For high-impact or disputed cases, obtain a fresh challenge assessment with the evidence and rubric but **without the first verdict**. Record the model/session/prompt or tool actually used. A differently worded self-check in the same context is not a genuinely independent reviewer.
- Where a separate reviewer/context is unavailable, record `INDEPENDENT_CHALLENGE_UNAVAILABLE`; a bounded adversarial self-check may still identify mistakes but must be labeled as nonindependent.
- Conflicts receive at most one focused evidence-based resolution pass per canonical decision group. If unresolved, retain uncertainty; never loop until a desired score appears.
- Repeated occurrences with genuinely identical material evidence can be challenged as one canonical group. Do not multiply review work by number of copies.

## 4. Twelve ordered phases and acceptance gates

**Execution policy:** Each phase remains a distinct work package. Finish its required population, actual semantic reviews and gates before moving forward. The twelve phases are logical milestones, not a promise of twelve chat turns. Resumable internal microbatches are permitted. **Only the essential consolidated output below is mandatory per phase**; absence of former auxiliary files is not a gate failure when all required fields and checks are preserved inside the consolidated file.

| Phase | Work package | Sole mandatory phase artifact | Gate to next phase |
| --- | --- | --- | --- |
| **01 — Freeze** | Verify all inputs, file hashes, PDF identity/page count, method attribution, frozen counts and fixed three-way source-ID sharding | `01_reference_lock.json` | All inputs readable, reference digests match and explicit shard ID lists cover every `R` once |
| **02 — Extract A** | Read generated files 01–04; restore table context; classify each substantive line/cell and extract definitive occurrences | `02_extraction_a.jsonl` | Every substantive file 01–04 line/cell accounted for as extracted, context, excluded or explicitly unresolved |
| **03 — Extract B** | Read files 05–08; distinguish adopted architecture from unadopted items; reconcile all eight-file extraction | `03_extraction_b.jsonl` | Complete eight-file line/cell accounting; no substantive unprocessed line concealed |
| **04 — Semantic classes** | LLM adjudicate full semantic equivalence, classify reused versus redundant occurrences, allocate fixed class shards for 08/09 | `04_generated_classes.jsonl` | Every eligible occurrence in exactly one proven class; complete equivalence and duplicate audit embedded |
| **05 — Source coverage A** | LLM source-to-eight-file semantic coverage decisions for source shard A | `05_source_a.jsonl` | Every shard A ID gets one sourced decision or precise unresolved finding |
| **06 — Source coverage B** | Same for shard B, with justified rather than inherited universal applicability | `06_source_b.jsonl` | Every shard B ID accounted for |
| **07 — Source coverage C** | Complete shard C and reciprocal missing-item search; reconcile all three source shards without copying their rows | `07_source_c.jsonl` | Every frozen `R` ID has exactly one decision across 05–07 |
| **08 — PDF validity A** | LLM check first deterministic class shard against original PDF; identify exact unsupported residual candidates | `08_pdf_a.jsonl` | Every allocated class judged or explicitly unresolved |
| **09 — PDF validity B** | Check remaining classes and reconcile the entire generated-class population without copying 08 rows | `09_pdf_b.jsonl` | Every `GC` class has exactly one PDF-validity judgment across 08–09 |
| **10 — FP and negative audit** | Both full-semantic residual dedup passes; fixed `N` assertion checks; remove control/FP double counting | `10_fp_controls.jsonl` | All candidate residuals and every `N` ID reconciled; provisional canonical universe derivable |
| **11 — Critical challenge** | Challenge material decisions, record independent-review limits, issue corrected post-challenge item-level ledger | `11_final_ledger.jsonl` | Every item, challenge and correction reconciled; one self-contained final scoring snapshot |
| **12 — Recompute and deliver** | Independently recompute from final ledger, check invariants and hashes, disclose bounded uncertainty, limitations, provenance and file inventory | `compute_metrics.py`, `12_metrics.json`, `12_report.md` | Accurate reproducible calculation or explicit blocked status, no fabricated verification |

**Required typed-record packaging:** For Phase 02/03, use `OCCURRENCE`, `EXCLUSION`, `LINE_DISPOSITION`, and `PHASE_SUMMARY` records, including original line totals and table-cell coverage. For Phase 04, use `CLASS`, `EQUIVALENCE_AUDIT`, `DUPLICATE`, and `PHASE_SUMMARY` records; embed per-member mutual-entailment proof when it is compact enough. For Phases 05–07, use **one `SOURCE_JUDGMENT` row per assigned `source_id`**, with its search receipt, grade, evidence and unresolved reason embedded, plus `PHASE_SUMMARY`. For Phases 08–09, use **one `PDF_JUDGMENT` per assigned `class_id`**, with PDF search details, evidence and unsupported residuals embedded, plus `PHASE_SUMMARY`. For Phase 10, use `FP_CLUSTER`, `FP_EQUIVALENCE_AUDIT`, `NEGATIVE_CONTROL`, `REFERENCE_EXCEPTION` as applicable, and `PHASE_SUMMARY`; the provisional proposition universe may be derived deterministically rather than written row by row. For Phase 11, use `FINAL_SOURCE`, `FINAL_CLASS`, `FINAL_DUPLICATE`, `FINAL_FP_CLUSTER`, `FINAL_CONTROL`, `FINAL_UNIVERSE`, `CRITICAL_CHALLENGE`, `CHANGE`, `REFERENCE_EXCEPTION` as applicable, and `FINAL_RECONCILIATION`. Reconstruct all final item-level statuses from these rows alone.

**Shard allocation:** At Phase 01, sort frozen `R` by earliest cited physical PDF page and stable `source_id`; partition into three near-equal groups. Store **all explicit IDs**, byte hashes, actual filenames, counts and provenance inside `01_reference_lock.json`. After Phase 04, sort complete generated `class_id` values, allocate alternating deterministic halves to Phases 08/09 and store all allocated IDs inside the `PHASE_SUMMARY` record of `04_generated_classes.jsonl`. Neither partition may change after scoring begins. When one LLM context cannot hold a phase's population, process bounded resumable microbatches inside that phase.

### 4.1 Phase 02–03 extraction criteria

Include: independently testable, definitive statements about screens, API actions, constraints, data, processing, failure behavior, authority, access, policy, performance, supported versions and adopted architecture. Extract conjunctions as separate claims only when each component is a genuine independent testable duty. Restore short table entries using their row/column headings and common section rules; retain `table_locator` and `context_source_locator`.

Exclude: document titles, lists of citations, cross-reference-only rows, editorial narration, illustrative data, unresolved `TBD`, unadopted alternatives, proposals, merely hypothetical errors and examples without normative force. A test assertion that independently commits to validation behavior can be included; a bare reference to a test ID is not a design commitment. **Do not treat the generator's self-reported word “Confirmed” as proof of PDF support**; it may establish whether the generator intended a definitive statement, not its truth.

Produce one per-line or per-table-cell **coverage disposition** (`EXTRACTED`, `CONTEXT_ONLY`, `EXCLUDED`, `REQUIRES_REVIEW`); keep total original line counts by file. `REQUIRES_REVIEW` cannot quietly count as extracted or excluded. Enforce inclusion/exclusion reconciliation before proceeding.

### 4.2 Phase 04 duplicate logic

Choose one deterministic representative occurrence per class (file order, line, table-cell position). Every other occurrence belongs to **exactly one** category:

- `EXPECTED_REUSE`: an identical proposition legitimately serves a distinct independent contractual/operational/verification role; record the specific role and location. Appearing in a different file is **not sufficient** on its own.
- `REDUNDANT_DUPLICATE`: an identical repetition adds no independently justified role; record why.

Do not merge just because a general rule subsumes a specific one, two claims refer to the same subject, or a table repeats a section title. Full equivalence requires mutual entailment of the material predicates. Use LLM-confirmed candidate clusters across **all eight** files; compare clusters against one another again after the first pass to catch paraphrases. Candidate retrieval may propose pairs, but no similarity threshold may decide the merge.

Require `eligible_occurrences = unique_generated_classes + expected_reuse_occurrences + redundant_duplicate_occurrences` and make each surplus occurrence traceable to its representative. Report both duplicate types and their rates independently. This stage deduplicates **all generated propositions**, not yet only FP.

### 4.3 Phase 05–07 source coverage standards

For each `source_id`, inspect every material predicate in the frozen record and its source citations. LLM-evaluate direct candidate matches, context, universal statements and cross-document conjunctions. An explicit universal assertion may satisfy many genuinely distinct source atoms **if** the proof demonstrates membership and all conditions for each; a source atom counts once no matter how often covered. Store every TP's evidence; E2 requires explicit bridge steps and relevant line locators.

For a source atom tentatively thought missing, **re-search all eight** generated files through the complete retrieval procedure. Inspect the strongest candidates and a separate universal/context search even if the nearest lexical match looks weak. `MISSING_CONFIRMED` requires an evidence-backed list of absent material predicates plus a complete search receipt. If search or interpretation is not complete, mark `COVERAGE_UNRESOLVED`, not confirmed FN.

### 4.4 Phase 08–09 PDF validity standards

Start with generated claims, **not** only source atoms that failed an `R` match. Each distinct generated class must receive a full-PDF semantic support review. Give the LLM the generated proposition, all material context, strongest PDF candidates, source page/section and any apparent exceptions. Test exact actor, target, modality, policy, conditions, timing, numbers, status, source authority and scope. A generated claim that expresses a global rule differently from the PDF can still be valid.

If PDF-supported but covering no frozen `R` atom, record `SUPPORTED_NONCOVERING` and the PDF proof; do not count an FP or manufacture a new gold atom. If PDF-unsupported, capture the **exact residual error** rather than classifying an entire surrounding true paragraph as fabricated. If uncertain, mark `PDF_UNRESOLVED`, not unsupported. A broad generated class may contain more than one independent unsupported residual, but split only genuinely independently testable propositions; retain linking provenance and do not count the same residue twice.

### 4.5 Phase 10 FP cluster audit: mandatory two passes

**Pass 1 — Validity and normalization:** Inspect every `PDF_UNSUPPORTED` generated class and each `PDF_UNRESOLVED` potential residual separately. Verify the original PDF evidence was searched. Normalize the precise unsupported proposition using actor, action, object, modality, logical polarity, preconditions, exceptions, version, scope, timing, codes, numerical constraints and outcome. Remove supported portions. Preserve `PDF_CONTRADICTION`, `UNSUPPORTED_ADDITION`, or `UNRESOLVED_POSSIBILITY` as diagnostic categories.

**Pass 2 — Global semantic equivalence:** Compare every normalized residual across **all eight** documents and generated classes. Merge **only mutually entailing** residuals; preserve all class/occurrence IDs, each exact locator and the semantic equivalence proof. Run a final cross-cluster challenge for high-likelihood pairs to detect missed paraphrase duplicates and over-merges. Keep related but nonidentical residuals separate. An unsupported claim repeated in seven files contributes one canonical FP cluster; a source requirement copied in seven files contributes no FP merely by repetition.

Compare all canonical residuals with each of the supplied `NEG-*` controls. If a generated assertion is exactly semantically equivalent at matching scope to a frozen control, link it to that control and **do not count that same proposition again as generated-only FP**. Record each negative control's asserted/not-asserted/unresolved decision based on actual generated text. Do not create, change, or add controls. Preserve one `FP_CLUSTER_ID -> class_ids -> occurrence_ids -> PDF_evidence` chain and a control-equivalence crosswalk. A broad assertion that entails several distinct controls requires a documented scope/predicate analysis; never automatically count one broad sentence several times merely by text matching.

### 4.6 Phase 11 critical audit and controlled changes

Critical cases include: suspiciously large FP groups, residual classes that look PDF-supported, directly matching candidates labeled missing, ambiguous universal-to-many coverage, a material change from merging/splitting one FP cluster, assertion of a forbidden control, and uncertain security/authorization/privacy/approval/irreversible-operation predicates. Every discovered counterexample must be considered even if it undermines an earlier score. Challenge each canonical decision once with a blinded second pass where possible; disagreements receive at most one targeted resolution. Record `INDEPENDENT_CHALLENGE_UNAVAILABLE` explicitly if a genuinely distinct context or reviewer cannot be obtained.

A correction must update **all dependent ledgers** consistently: source coverage links, generated class validity, residual cluster memberships, asserted controls, duplicate classifications and the final canonical universe. Preserve original phase outputs and embed append-only `CHANGE` records (old/new values, reason, evidence, adjudicator, affected IDs) in `11_final_ledger.jsonl`. Never use a summary-only correction that leaves the item-level final snapshot stale. Material unresolved judgments remain unresolved and may prevent verified point estimates.

## 5. Measurement policy: no “uncertain = FP” distortion

This protocol has **two primary measurement perspectives**, because one generated universal claim can cover several frozen source atoms and one source requirement can appear in several generated specifications. Do not pretend that generated occurrence count, generated class count, source-atom count and unsupported-residual count are interchangeable.

### 5.1 Source requirement coverage

Let:

```text
R_total   = |R|
R_TP      = count(COVERED)
R_FN      = count(MISSING_CONFIRMED)
R_UNKNOWN = count(COVERAGE_UNRESOLVED)
R_TP + R_FN + R_UNKNOWN = R_total

Recall_lower = R_TP / R_total
Recall_upper = (R_TP + R_UNKNOWN) / R_total
```

If `R_UNKNOWN=0`, report `Recall = R_TP/R_total` as a single resolved value. Otherwise display the interval `[Recall_lower, Recall_upper]`, both counts, and the reasons for uncertainty. `R_FN` means proven absence of **complete coverage in the scored eight-file corpus**, not proven absence of any related text anywhere.

### 5.2 Generated claim validity

Let:

```text
G_total     = |GC|
G_supported = count(PDF_SUPPORTED)
G_invalid   = count(PDF_UNSUPPORTED)
G_unknown   = count(PDF_UNRESOLVED)
G_supported + G_invalid + G_unknown = G_total

ClaimValidity_lower = G_supported / G_total
ClaimValidity_upper = (G_supported + G_unknown) / G_total
```

`ClaimValidity` is a **separate class-level metric**, not raw occurrence precision and not a substitute for source Recall. When `G_unknown=0`, report its resolved value. When unresolved, report only the interval and qualified counts. A PDF-supported generated class may have `SUPPORTED_NONCOVERING` status and **still contributes to `G_supported`**.

### 5.3 Canonical proposition projection: Precision, Recall, F1

For explicitly comparable semantic-projection scoring, use source-positive atoms as the reference-positive universe; negative-control assertions and unique PDF-unsupported generated-only residual propositions form the negative-prediction side. Count each canonical false proposition only once, not once per document, failed source match, or generated occurrence.

Let:

```text
B_asserted       = number of distinct N IDs definitively asserted
B_not_asserted   = number of N IDs verified not asserted
B_unknown        = number of N IDs with unresolved assertion
B_asserted + B_not_asserted + B_unknown = |N|

F_only_confirmed = count of unique confirmed unsupported residual propositions
                   NOT already represented by an asserted N control
F_only_unknown   = count of unique unresolved potential unsupported residuals
                   NOT already represented by a confirmed or potential N assertion

FP_confirmed = F_only_confirmed + B_asserted
FP_possible_extra = F_only_unknown + B_unknown
```

Only when **all** source, generated validity, negative-control and FP equivalence decisions affecting the metrics are resolved:

```text
TP = R_TP
FN = R_FN
TN = B_not_asserted       # bounded diagnostic controls only
FP = FP_confirmed

Projection_Precision = TP / (TP + FP)
Source_Recall        = TP / (TP + FN)
Projection_F1        = 2*TP / (2*TP + FP + FN)
```

These are rates on the disclosed **canonical semantic-proposition projection**. They are **not** generated-class precision: the TP side counts covered frozen source atoms, whereas the extra FP side counts unique unsupported semantic residuals and asserted fixed controls. Report `ClaimValidity` alongside them so a universal rule's multiple source-atom coverage does not conceal weak per-class validity. Explicitly state this measurement choice in every comparison.

If unresolved judgments remain, **do not issue one falsely precise “final FP” or Precision**. Show confirmed lower counts and conservative bounds instead:

```text
TP_min = R_TP
TP_max = R_TP + R_UNKNOWN
FN_min = R_FN
FN_max = R_FN + R_UNKNOWN
FP_min = FP_confirmed
FP_max = FP_confirmed + FP_possible_extra

Precision_lower = TP_min / (TP_min + FP_max)
Precision_upper = TP_max / (TP_max + FP_min)
Recall_lower    = TP_min / |R|
Recall_upper    = TP_max / |R|
F1_lower        = 2*TP_min / (2*TP_min + FP_max + FN_max)
F1_upper        = 2*TP_max / (2*TP_max + FP_min + FN_min)
```

These are **conservative uncertainty envelopes**, not probability confidence intervals and not an assertion that all extreme combinations are jointly attainable. Use JSON `null` for undefined denominators, with a written explanation. `TN` is limited to the predeclared controls; neither all possible absent behaviors nor population specificity/accuracy can be inferred from it. Explicitly separate an N-control alarm count from unique FP residuals in every report.

### 5.4 Duplicate metrics

```text
GO_count = number of eligible generated occurrences
GC_count = number of canonical generated classes
D_excess = GO_count - GC_count
D_expected = number of excess occurrences classified EXPECTED_REUSE
D_redundant = number of excess occurrences classified REDUNDANT_DUPLICATE

D_expected + D_redundant = D_excess
Expected_reuse_rate = D_expected / GO_count
Redundant_duplicate_rate = D_redundant / GO_count
```

For a zero denominator return `null`. Report two types separately. These are **occurrence-level** diagnostics and must not alter source TP or canonical FP merely because the same rule is repeated in several document roles.

### 5.5 Historical comparison restriction

Do not compare a new score numerically with historical Full Load/One-Level/Two-Level charts unless the **same frozen reference, eligible-claim definition, PDF version, semantic equivalence standard, handling of unresolved cases, and scoring projection** are used. If not, call the comparison `NOT_COMPARABLE`; historical results may still be described as context but never used to force label changes or claim an improvement/decline.

## 6. Minimum machine-readable record schemas

These are mandatory **field families**, not illustrative evidence or actual scoring outcomes. Additional fields are allowed, but required identifiers and decision vocabulary must be stable. Every row must be valid UTF-8 JSONL with JSON `null` for absent values. **In 8.1, store them as typed rows in the consolidated phase files; `record_type` is mandatory and separate legacy files are forbidden by default.**

### 6.1 Generated occurrence and exclusion

```json
{
  "occurrence_id": "GEN-000001", "method": "unattributed",
  "file": "01_screen_functions.md", "line_start": 1, "line_end": 1,
  "table_locator": null, "context_source_locator": null,
  "statement_en": "A real atomic commitment read from this location",
  "predicate_structure": {"actor": null, "action": null, "target": null, "scope": null,
    "modality": null, "conditions": [], "exceptions": [], "timing": null,
    "version": null, "outcome": null, "polarity": null},
  "eligibility": "DEFINITIVE", "extraction_evidence": [], "review_status": "LLM_REVIEWED"
}
```

Exclusions have their own `exclusion_id`, exact file/line/table locator, original text, `exclusion_reason` and coverage disposition. The example is a **schema placeholder**, not an actual OrionDesk finding.

### 6.2 Generated semantic class and duplicate

`class_id`, `complete_normalized_proposition_en`, `predicate_structure`, `representative_occurrence_id`, `member_occurrence_ids`, and `equivalence_evidence` are mandatory. For each excess duplicate store `occurrence_id`, `class_id`, `representative_occurrence_id`, `duplicate_type`, `specific_role_evidence`, `reason_en`, and exact locators. Preserve every source occurrence even after normalization.

### 6.3 Source coverage

`source_id`, `judgment` (`COVERED`/`MISSING_CONFIRMED`/`COVERAGE_UNRESOLVED`), `grade` (`E3`/`E2`/`E1`/`E0`/`UNRESOLVED`), frozen PDF evidence, candidate generated occurrence IDs and actual locators, strongest candidate quotations, `all_material_predicates`, `entailed_predicates`, `missing_predicates`, applicability/exception proof, `search_receipt` (embedded object or compact array), and `adjudication_origin`. For E2 include an explicit universal membership bridge or multi-document proof. For missing, include completed reciprocal search evidence; for unresolved, specify the actual unfinished issue.

### 6.4 PDF validity and FP residual

Each generated class gets `class_id`, `pdf_judgment`, actual PDF `physical_page` and section/table/figure locators, exact quotation/context, predicate-level evidence, `supported_noncovering` flag, `covered_source_ids`, `unsupported_residual_ids`, `search_receipt` (embedded object or compact array), and `adjudication_origin`. Each FP residual cluster gets exactly one complete proposition, `fp_cluster_id`, support subtype, source class IDs, all occurrence IDs/locations, full equivalence reasoning, PDF counterevidence or absence-search evidence, negative-control crosswalk and `confirmation_state` (`CONFIRMED_UNSUPPORTED`/`UNRESOLVED_POTENTIAL`).

### 6.5 Negative controls and corrections

Every fixed `negative_control_id` has one `assertion_status`, generated-claim locators, predicate-level assertion explanation, matching canonical cluster IDs and full-search receipt. Corrections append `change_id`, target ledger row, old status, new status, reason, evidence, adjudicator, challenge outcome and dependent-file updates. Never erase older decisions from the audit trail.

## 7. Verification gates and script requirements

The Phase 12 `compute_metrics.py` must compute counts and rates **only from the typed final item-level records in `11_final_ledger.jsonl`**, cross-validating IDs against the frozen source inputs and Phases 02–10, not from any prior summary JSON. It must read the consolidated file types directly; separate legacy ledgers are not required. It must fail loudly on any of the following:

1. Missing or unreadable mandatory inputs; malformed JSON/JSONL or missing identifiers; hash mismatch with `01_reference_lock.json`.
2. Any generated document line/table cell without a coverage disposition, unresolved extraction incorrectly treated as clean, or unexplained missing generated occurrences.
3. Duplicate `source_id`/`negative_control_id`/`occurrence_id`/`class_id`/`fp_cluster_id`, or any generated occurrence belonging to zero/multiple classes.
4. `GO_count != GC_count + D_expected + D_redundant`, or an extra occurrence without one of the two permitted duplicate types.
5. Any source-positive ID not assigned exactly one of `COVERED`, `MISSING_CONFIRMED`, `COVERAGE_UNRESOLVED`.
6. A `COVERED` source atom without actual generated proof; an E2 source atom without an applicability bridge; a `MISSING_CONFIRMED` atom without complete eight-file reciprocal-search receipts.
7. Any generated class without exactly one PDF validity status, unsupported class with no identified residual, or PDF-supported class whose material predicates lack cited support.
8. Residual candidates lost between generated validity and final FP clustering, duplicated canonical residual semantics, overlapping identical negative-control and generated-only FP counts, or clusters missing member occurrence provenance.
9. Any frozen negative-control ID lacking exactly one assertion status, or `B_asserted + B_not_asserted + B_unknown != |N|`.
10. `R_TP + R_FN + R_UNKNOWN != |R|`, `G_supported + G_invalid + G_unknown != |GC|`, `FP_confirmed != F_only_confirmed + B_asserted`, or impossible interval bounds.
11. Claimed independent critical adjudications without verifiable independent-pass records, or corrections absent from the unified post-challenge final ledger.
12. Final metrics copied from a prior JSON instead of recomputed; numeric denominators not documented; historical incomparable runs presented as ranked equivalents.
13. Output/inputs sharing a path, an attempted reference mutation, or a reference hash change at the final gate.
14. Author-generated file prose not in English; evidence locators that cannot be resolved in the actual uploaded PDF/Markdown file; placeholder text misrepresented as real evidence.

The validation script must also reject missing `record_type` values, missing per-phase `PHASE_SUMMARY` or `FINAL_RECONCILIATION`, incomplete typed-record partitions and unreferenced changes or search receipts. Multiple record types inside one JSONL are intentional; a separate auxiliary file is never required solely for a schema family.

A script passing these gates proves **structural integrity**, not semantic correctness. The report must state that explicitly. Inspect a selected set of actual PDF page images, tables and generated context at critical disputed sites; mechanical checks alone cannot sign off on semantic entailment.

## 8. Completion statuses and release rules

| Status | Meaning |
| --- | --- |
| `PHASE_COMPLETE_EVIDENCE_REVIEWED` | All required phase artifacts and semantic evidence checks completed for that phase |
| `PHASE_COMPLETE_WITH_UNRESOLVED` | All phase items explicitly accounted for; unresolved cases and their impact enumerated |
| `PHASE_INCOMPLETE_CONTINUE_SAME_PHASE` | Required items or reviews have not been processed; do **not** advance |
| `PHASE_BLOCKED_INPUT` | Missing/unreadable mandatory input or PDF evidence; do **not** invent results |
| `RUN_INVALID_REFERENCE_CHANGED` | Reference bytes differ from the locked pair; abort comparable scoring |
| `FINAL_VERIFIED` | All items resolved, all mechanical checks pass, required critical challenges completed as independent assessments where available, and no material evidence exception remains |
| `FINAL_QUALIFIED` | All items accounted for with explicit unresolved decisions, bounded score ranges and review limitations; no unsupported point-estimate claim |
| `FINAL_BLOCKED` | Inputs or required ledger coverage insufficient for defensible scoring |

A `PHASE_COMPLETE_WITH_UNRESOLVED` result may move forward **if** itemized uncertainty is preserved and the next phase can legitimately work with it. If an extraction or file-reading task itself is incomplete, use `PHASE_INCOMPLETE_CONTINUE_SAME_PHASE` and remain in the phase. **Never turn partial execution into success by relabeling everything as unresolved.**

`FINAL_VERIFIED` must not be awarded merely because a script passed or every file exists. If independent critical review was unavailable for material disputes, report `FINAL_QUALIFIED` unless those disputes are otherwise conclusively resolved with auditable evidence and the limitation is clearly disclosed. The final report must disclose the exact independent-review coverage.

## 9. Output layout and delivery

**Exactly the following 14 mandatory deliverables** (11 phase checkpoints, three Phase 12 outputs). **No additional JSONL audit logs, Markdown summaries, duplicated cumulative ledgers or standalone manifest files.** Each phase writes to the indicated file only; necessary evidence records are embedded, not omitted.

```text
oriondesk_evaluation_v8_1/
    01_reference_lock.json
    02_extraction_a.jsonl
    03_extraction_b.jsonl
    04_generated_classes.jsonl
    05_source_a.jsonl
    06_source_b.jsonl
    07_source_c.jsonl
    08_pdf_a.jsonl
    09_pdf_b.jsonl
    10_fp_controls.jsonl
    11_final_ledger.jsonl
    compute_metrics.py
    12_metrics.json
    12_report.md
```

The **single** `01_reference_lock.json` combines the old input manifest, reference lock and three source shards. `02`/`03` each combine occurrences, exclusions, line dispositions and their reconciliation. `04` combines classes, equivalence audits, duplicate labels and class shard allocation. `05`–`09` embed search receipts and uncertainty directly in judgment rows. `10` combines confirmed/potential FP clusters, equivalence audits, negative-control decisions and reconciliation. `11` contains the coherent corrected item-level scoring snapshot, its provenance and all actual challenges/changes; **it replaces every former `final/*.jsonl` file**. `12_metrics.json` contains computed metrics, verification results, source and output SHA-256, record counts, release status and a compact delivery inventory. `12_report.md` combines the old metrics report, evidence audit and limitations in one readable file.

Generate or update only the current phase's mandatory file(s). Do not pre-create empty files for later phases. Keep original inputs untouched, and maintain a separate root for each evaluated method. Do not produce ZIP archives or upload redundant copies by default. Show a direct download link only for completed mandatory artifacts. Do not make corrected copies of the frozen reference inputs in the output directory.

**Version migration:** Phase 01 outputs already produced using 8.0 may be imported **only after verifying the actual input hashes**, then consolidated into the 8.1 `01_reference_lock.json` with the same explicit shard membership and method attribution. Record the migration provenance. A previous file's name or a claimed completion is not sufficient; never silently assume the earlier phase passed. Versions 8.0 and 8.1 share the scoring semantics but have different artifact layouts.

## 10. Mandatory final report content

The English `12_report.md` must present these subjects concisely; machine-readable detail belongs in `11_final_ledger.jsonl` and `12_metrics.json`, not duplicate standalone audit reports:

1. Input files, PDF identity, reference version and hashes; actual method attribution; reference freeze limitations.
2. Eight-file extraction coverage, eligible/excluded counts, unresolved extraction count and evidence completeness.
3. Source coverage: `R_TP`, `R_FN`, `R_UNKNOWN`, direct E3 and bridged E2 counts, source evidence/bridge audit, Recall or its uncertainty interval.
4. Generated validity: `G_supported`, `G_invalid`, `G_unknown`, `SUPPORTED_NONCOVERING`, per-class support evidence and ClaimValidity or its interval.
5. **Confirmed FP**, **possible unresolved FP**, PDF contradiction/addition subtype counts, controls asserted and their dedup crosswalk; no invented “confirmed fabrications.”
6. Source-projection Precision/Recall/F1 only if resolved; otherwise lower/upper envelopes and why single point estimates are withheld.
7. `N` diagnostic counts (`ASSERTED`, `NOT_ASSERTED_VERIFIED`, `ASSERTION_UNRESOLVED`) without implying population-wide TN accuracy.
8. Both duplicate types, rates, occurrence/class reconciliation and major cross-document reuse examples.
9. Actual critical challenge coverage, first/second decision disagreements, correction count, unavailable independent reviews, unresolved material cases.
10. Mechanical verification outcomes, semantic limitations, source-exception effects, reproducibility steps and explicit `FINAL_*` status.

If several methods are evaluated under identical conditions, produce separate method-level results and a side-by-side comparison with the same uncertainty rules; rank methods only if the evidence supports a stable comparison. A larger or longer input-token budget is useful operational context, **not proof of better or worse specification quality**.

## 11. Final operating instruction

**Apply the frozen reference without changing it. Use scripts to locate evidence and check accounting, and LLM semantic reasoning to decide entailment. Evaluate the complete eight-document corpus in both directions. Confirm rather than assume omissions, and confirm rather than assume unsupported generated claims. Deduplicate unsupported propositions across all eight files by complete meaning, not surface wording. Never count a repeated FP more than once and never count an unreviewed candidate as confirmed FP. Preserve every source and generated item, every exception, every uncertainty and every actual change. Finish the twelve phases in order, continuing a phase when evidence work is incomplete. Publish verified point metrics only when defensible; otherwise publish explicit uncertainty ranges and the reasons verification remains incomplete.**
