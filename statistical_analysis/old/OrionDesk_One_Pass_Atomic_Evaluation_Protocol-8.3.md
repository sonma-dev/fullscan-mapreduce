# OrionDesk AI — Practical Atomic Specification Evaluation Protocol

**Protocol version:** 8.3  
**Status:** Standalone evaluation procedure  
**Purpose:** Evaluate the completeness and factual fidelity of eight generated software-design specifications against one immutable, PDF-grounded reference.  
**Execution:** Nine ordered phases, one phase at a time, using shared retrieval, strong first-pass source coverage, bounded FN challenge, and auditable best-effort final classifications.  
**Output language:** **All authored files, including Markdown, JSON/JSONL values, program code/comments, explanations, and reports, must be written entirely in English.** Exact source quotations retain their source wording.

## 1. Objective and priorities

The evaluator must produce a **single best-effort determination** for each of TP, TN, FP, and FN, followed by Precision, Recall, and F1. **Do not replace the final counts with lower/upper bounds or uncertainty intervals.** Preserve uncertainty as a separate quality annotation on individual judgments and in the report.

Priorities, in order:

1. Keep the frozen benchmark untouched and use the original PDF as the semantic authority.
2. Assess actual meaning, including scope, exceptions, modality, actors, and consequences; avoid mere word matching.
3. Count a source-positive requirement once, and count a distinct unsupported generated proposition once across all eight specifications.
4. Make the main coverage pass semantically effective; use a separate, bounded FN challenge to correct likely misses without repeating the entire evaluation.
5. Finish each phase in a practical amount of work and retain enough evidence to reproduce the scores, without creating redundant audit files.

This is a **practical comparative evaluation**, not a certification that every interpretation or every Gold Set requirement is independently correct. Do not invent tests, searches, reviewers, source quotations, or verification results. Do not optimize labels to match a prior score.

### 1.1 Mandatory inputs

| Role | Canonical filename | Use |
|---|---|---|
| Positive reference (R) | `common_atomic_reqs.jsonl` | Frozen positive propositions, identified by `source_id` |
| Negative controls (N) | `common_negative_controls.jsonl` | Frozen counterfactual controls, identified by `negative_control_id` |
| Reference freeze metadata | `reference_freeze.json` | Expected digests, reference version, provenance and limitations |
| Original source | `OrionDesk_AI_Detailed_Design_Specification.pdf` | Normative authority for generated claims |
| Generated specification 1 | `01_screen_functions.md` | Screens |
| Generated specification 2 | `02_api.md` | APIs |
| Generated specification 3 | `03_data.md` | Data |
| Generated specification 4 | `04_batch_functions.md` | Background processing |
| Generated specification 5 | `05_business_rules.md` | Business rules |
| Generated specification 6 | `06_exception_handling.md` | Exceptions |
| Generated specification 7 | `07_processing_flows.md` | Processing flows |
| Generated specification 8 | `08_architecture_decision.md` | Adopted architecture commitments and unresolved decisions |

Upload-copy suffixes such as `(2)` are acceptable. Identify the exact supplied file for each role and hash its actual bytes. If multiple candidates are ambiguous, stop and report the ambiguity rather than choosing an old file. The eight generated files constitute **one evaluated corpus**. The operator handles any external experiment identification; the evaluator need not discover, label, infer, or write such an identification into any artifact.

### 1.2 Non-negotiable reference rules

- Before evaluation, calculate SHA-256 digests for the PDF and both reference JSONLs, and compare them against all corresponding expected digests in `reference_freeze.json`. A mismatch blocks the run.
- Freeze both JSONLs **by exact bytes and IDs**. Never edit, split, merge, normalize, filter, or repair their contents, including in a purported corrected working reference.
- Accept the positive inventory as complete **for this benchmark**. Do not run a separate Gold Set creation, completeness reconstruction, or upstream validation workflow during evaluation.
- Preserve the freeze record's provisional or verified status and stated limitations; do not silently upgrade its certification.
- A generated statement can be supported by the PDF without covering any frozen source ID. Label it `SUPPORTED_NONCOVERING`, **not FP**, and do not add an R atom.
- If a frozen atom materially contradicts the original PDF, record a `REFERENCE_EXCEPTION` with actual evidence and continue using the fixed ID and content. Disclose its effect; do not silently rewrite the benchmark.
- Recheck reference digests at final delivery. If the reference bytes changed, mark the run `INVALID_REFERENCE_CHANGED` and do not publish comparable metrics.

## 2. Evaluation objects and final decision policy

### 2.1 Counted objects

- `R`: the frozen positive requirement IDs. Every ID receives exactly one final `COVERED` or `NOT_COVERED` result.
- `N`: the frozen negative-control IDs. Every ID receives exactly one final `ASSERTED` or `NOT_ASSERTED` result.
- `GO`: eligible **generated atomic commitment occurrences** extracted from the eight specifications, with their original locators.
- `GC`: distinct, complete generated semantic propositions; each class links to all its `GO` occurrences.
- `SUPPORTED_G`: generated classes whose material meaning is supported by the PDF, including classes that cover no `R` item.
- `UNSUPPORTED_G`: generated classes containing a confirmed or best-effort unsupported material claim relative to the PDF.
- `F_ONLY`: canonical unsupported generated **residual propositions** not already represented by asserted frozen negative controls. Each unique residual is counted once.

Retain the complete proposition: actor, action, target, modality, polarity, conditions, scope, exceptions, version, timing, quantitative limits, and outcome as applicable. Two statements are not identical merely because they use the same nouns or share an identifier.

### 2.2 Single-value best-effort rule

**Every eligible scoring item must receive a final binary judgment.** Use the evidence actually available, including direct text, inherited context, relevant cross-file rules, and targeted PDF checks. After a reasonable search and focused consideration, select the most defensible conclusion even when proof is not perfect.

For each final decision retain:

- `decision`: the required binary result;
- `basis`: `DIRECT`, `CONTEXTUAL`, or `BEST_EFFORT`;
- `confidence`: `HIGH`, `MEDIUM`, or `LOW`;
- `evidence`: real source/generated locators and concise relevant quotations or a referenced already-recorded evidence item;
- `reason_en`: short explanation of decisive predicates; for `LOW`, the specific remaining doubt.

Do not label every `NOT_COVERED` result `BEST_EFFORT` by default: select the basis from the actual inspection, and explain the decisive missing predicate or bounded absence search. An uncertain decision **still contributes to final counts**. Never count an unresolved item automatically as FP or FN solely because it is unresolved. Instead, make an evidence-based best-effort choice and label its confidence. `BEST_EFFORT` means the verdict was selected with limited proof; it is not a claim of verification.

**Conservative false-assertion rule:** Failure to match a frozen positive ID does not establish FP. Check the PDF before rejecting a generated proposition. Ambiguous text should not become FP merely because the PDF search returns no exact phrase; consider contextual or general support. Conversely, ambiguous or merely similar generated wording does not fully cover a source requirement if an essential predicate remains unestablished.

If a material input is unreadable, a required expected hash fails, or source identity cannot be resolved, stop as `BLOCKED`. These are actual execution blockers, not grounds for fabricating numeric scores.

### 2.3 Eligible generated commitments

**Include:** definite, independently testable design statements for behavior, fields, interfaces, constraints, access, time/order, errors, data, processing, policies, adopted decisions, and verification duties.

**Exclude:** titles, pure cross-references, editorial descriptions, unsupported inferences by the evaluator, example values without normative force, hypothetical tests without asserted behavior, `TBD`, explicit questions, unadopted proposals, alternatives not selected, and suggestions. A source-defined valid alternative may be represented as an **alternative**, not as both options being mandatory. Do not accept a generated author's label such as “Confirmed” as proof of PDF validity.

Restore table row/column headings and inherited section scope when a cell is not a complete statement. Split independent commitments, but do not mechanically split fields or phrases that are not independently testable. Preserve all original line/section/table locators for included claims.

### 2.4 Semantic entailment and equivalence

- `COVERED`: generated definitive evidence entails **all material predicates** of a frozen requirement. One applicable universal rule may cover several R atoms when its membership and relevant conditions are defensible; one atom still contributes only one TP.
- `NOT_COVERED`: complete entailment was not established after a proportionate eight-file candidate search. Partial coverage remains FN. Note the missing predicate briefly.
- `PDF_SUPPORTED`: source PDF supports the generated proposition's material meaning, including a differently phrased equivalent rule.
- `PDF_UNSUPPORTED`: a material generated assertion is contradicted or lacks defensible source support. Identify the unsupported **residual**, not the surrounding true clauses.
- `ASSERTED` control: an eligible definitive generated proposition affirmatively asserts the same forbidden/excluded/deferred behavior at the relevant scope and polarity. A quoted example, discussion of a risk, explicit prohibition, or unadopted proposal is **not** assertion.

Merge generated occurrences or residuals into one class **only where material predicates are mutually entailing**. Different endpoints, actors, preconditions, versions, error codes, quantifiers, time boundaries, and outcomes normally remain separate. General rules and specific rules are not automatically equivalent even where one entails the other.

## 3. Efficient execution and evidence economy

The evaluator works **one phase at a time**, normally finishing that phase in one request–response. A phase cannot claim completion with missing required input or an incomplete required ID population. If an actual platform limit prevents a complete population, save a resumable checkpoint, report `INCOMPLETE`, and continue the **same** phase on the next turn. Do not artificially prolong a phase in pursuit of certainty.

### 3.1 Shared indexes and semantic decision units

Build the reusable retrieval preparation **once** and reuse it in Phases 03–08:

1. Index the PDF by physical page/section, retaining actual source-text quotations and table/figure references. Use existing frozen evidence where applicable; inspect page images when their visual meaning affects a decision.
2. Parse the eight Markdown files once, preserving original file/line/heading/table-row/cell locators and inherited scope. Index both the extracted GO/GC propositions **and the original Markdown**, including statements excluded during Phase 02.
3. Build deterministic identifier, API-path, event, entity, number, role, action, polarity, and condition indexes; supplement with lexical and optionally semantic-neighbor retrieval. Precompute reverse GC-to-R candidates and frequent source-to-document identifier associations.
4. Distinguish **candidate retrieval** from **semantic entailment**. Lexical/fuzzy scores may rank or prioritize candidates but may never by themselves accept or reject a coverage claim.
5. Make reusable **rule families** for repeated cross-cutting obligations (authentication/tenancy, request validation, event audit/outbox, retries, component-specific tests, etc.). Evaluate the actual rule predicates and the membership/scope of each application, not just the presence of a generic phrase. Keep every frozen R ID and every distinct GC separate for scoring.
6. Cache adjudicated rule-family predicates, representative evidence, aliases, and source/target scope tests; reuse them for individual IDs only after verifying applicability. Resolve a small set of plausible candidates plus their inherited context, and inspect more only if the risk justifies it.
7. Retain compact, reproducible search receipts and proof locators; do not output exhaustive per-hit transcripts or require a separate full-document narrative per R ID.

A source-to-generated match may use one complete generated proposition or a **compatible conjunction** of genuinely applicable statements across files. A global rule plus a separately grounded entity-specific declaration may entail a source requirement; a mere common title, shared identifier, or vague generic sentence does not. Universal and specific propositions must **not** be merged as one GC merely because one entails the other.

### 3.2 Review budget and runtime discipline

- Prefer one batch candidate-generation pass over repeated eight-file scans for each requirement. Search all eight specifications through the shared index, not by reopening every file separately for every R.
- Evaluate easy direct and contextual families in batches; devote individual semantic attention to conditions, exception branches, exclusions, negations, numbers, security boundaries, apparent omissions, and conflicting evidence.
- Do not use a fixed lexical-similarity threshold as a rejection rule; if a candidate is weak lexically but matches a source identifier or plausible semantic alias, check its meaning before classifying it as absent.
- Phase 04 performs the **principal coverage adjudication**. Phase 05 reuses its candidates, decisions, and family proofs and is **not a second full-scale Phase 04**.
- Apply the explicit bounded review budget in Phase 05. Expand an affected family when a verified error pattern is found, using group applicability checks rather than independent rereads for every member. Do not require unlimited global re-search.
- A remaining nonblocking ambiguity receives a binary best-effort choice and a confidence annotation. Do not invent definitive evidence or silently treat unresolved items as FN.
- If time or computation is constrained, reduce redundant narrative and redundant search, **not** required R/N/GC population coverage, the semantic check for promising matches, or important authorization/approval/tenancy safeguards.

## 4. Nine ordered phases and deliverables

The normal deliverable set comprises **11 files**: one consolidated artifact for each of Phases 01–08 and a calculator, metrics JSON, and readable report for Phase 09. Temporary indexes/scripts are not deliverables. Every phase artifact includes a compact summary of processed populations, reconciliation, quality exceptions, low-confidence totals, and status.

| Phase | Task | Required artifact | Completion gate |
|---|---|---|---|
| **01 — Reference Lock** | Validate inputs, hashes, PDF page count, and frozen R/N IDs | `01_reference_lock.json` | All required inputs resolved; expected reference hashes match |
| **02 — Generated Extraction** | Extract eligible generated atomic commitments and preserve source locators | `02_generated_occurrences.jsonl` | Every substantive section/table examined; all occurrences uniquely identified |
| **03 — Semantic Deduplication** | Group equivalent occurrences and classify reuse/duplicate roles | `03_semantic_classes.jsonl` | Every eligible occurrence belongs to one class; counts reconcile |
| **04 — Source Coverage** | Strong semantic first-pass adjudication of every frozen R | `04_source_coverage.jsonl` | Each R ID has exactly one binary result, grounded candidate receipt, and decision rationale |
| **05 — FN Reassessment and Extraction Recovery** | Bounded, risk-weighted challenge of provisional FNs and targeted extraction repair | `05_fn_reassessment.jsonl` | Every Phase 04 FN screened; selected challenges completed; corrections and recovered classes reconciled |
| **06 — PDF Claim Validity** | Assess every effective GC against the PDF and isolate unsupported residuals | `06_pdf_validity.jsonl` | Exactly one PDF judgment per effective GC; residuals traceable |
| **07 — FP and Control Audit** | Deduplicate unsupported residuals and assess all frozen N without double counting | `07_fp_controls.jsonl` | All residuals assigned; every N adjudicated; FP/control crosswalk reconciled |
| **08 — Targeted Quality Audit** | Challenge highest-risk decisions and issue one final item-level ledger | `08_final_ledger.jsonl` | Corrections reconciled; all effective R/GC/N and FP clusters represented |
| **09 — Metrics and Delivery** | Compute and verify reproducible single-value scores, limitations, and provenance | `compute_metrics.py`, `09_metrics.json`, `09_report.md` | Hashes/identities/count equations verified or explicit blocked status |

### Phase 01 — Reference Lock

- Read and validate all input files as UTF-8 or PDF, count physical PDF pages, and hash actual bytes.
- Parse every R and N record; reject malformed JSONL, missing IDs, duplicate IDs, label errors, or reference-digest mismatches.
- Record actual filenames, SHA-256, reference version/status, positive and negative counts, PDF pages, input problems, and preserved upstream limitations.
- Do **not** re-extract Gold Set requirements or audit upstream Gold Set completeness.

### Phase 02 — Generated Extraction

- Read all eight Markdown specifications. Extract complete independent **definitive** commitments, including meaningful statements reconstructed from tables and supported inherited scope.
- Assign stable occurrence IDs (`GEN-000001`...) ordered by file, original line and cell position. Each row records the original locator, text or normalized proposition, inherited context, and eligibility basis.
- Maintain section/table-level coverage summaries for every file. Record meaningful exclusions by range/category and reason, including **excluded substantive statements** that might be actionable in coverage; formatting-only lines require no separate records.
- Separate open items from adopted decisions in the architecture register. Do not turn questions, hypothetical alternatives, fictional examples, or unadopted proposals into implemented requirements.
- Avoid artificial standalone atoms from headings. Flag questionable atomicity without suppressing an independently testable behavior.

### Phase 03 — Semantic Deduplication

- Normalize material predicates and use indexed candidate generation across all eight specifications.
- One class (`GC-000001`...) represents one complete mutually entailing proposition. Keep a representative occurrence and all members and locators.
- Classify excess occurrences as `EXPECTED_REUSE` only when they perform a concrete independent specification role, otherwise `REDUNDANT_DUPLICATE`.
- Run a targeted cross-group paraphrase collision check. Do not perform unrestricted all-pairs comparisons; explain uncertain nonmerges briefly.
- Reclassify clear editorial/non-atomic extraction errors using `RECLASSIFIED_EXCLUSION` entries, preserving original IDs and provenance without rewriting Phase 02.
- Reconcile `GO = GC + EXPECTED_REUSE + REDUNDANT_DUPLICATE` after explicit reclassifications. This phase determines uniqueness, not PDF truth.

### Phase 04 — Source Coverage

**This is the principal semantic coverage pass, not merely a lexical candidate pass.** Evaluate every frozen source ID against the complete eight-file corpus using the prepared GO/GC and original-Markdown indexes.

1. **Prepare source predicates.** For every R, identify the specific actor, obligation, target, applicable component/API/event, polarity, conditions, exceptions, quantitative bounds, and outcomes from its frozen evidence and available PDF context. Do not regenerate or modify R.
2. **Retrieve complementary candidates once in batches.** Combine direct identifier/path/event matches, lexical variants, semantic paraphrases, and GC-to-R reverse candidates. Query source-specific statements and relevant cross-cutting rule families together. For high-risk or suspicious weak matches, include the best original-Markdown evidence even if Phase 02/03 excluded it.
3. **Apply shared rule families.** Verify a representative universal rule against source material, then check each member's actual scope, subject, exception, and test duty before reusing the entailment. Explicit generic rules may cover multiple R IDs; neither a universal heading nor an unrelated generic claim is sufficient.
4. **Adjudicate semantic coverage, not scores.** Accept `COVERED` only when direct, contextual, or compatible cross-file evidence entails all material predicates. Check the literal original Markdown and its table headers if a strong candidate is incomplete in GC. A high lexical score is not proof; a low score is not absence.
5. **Use a targeted absence challenge before FN.** For any plausible uncovered item, inspect its best candidate, likely alias/identifier, and relevant universal or exception rule. Specifically state which predicate is missing, or give a compact negative-search basis if no plausible candidate survives the shared index. Do not assign `BEST_EFFORT` or `NOT_COVERED` solely because candidate confidence or similarity is low.
6. **Record the verdict once per R.** `COVERED` includes actual GC/GO identifiers when present, generated locators, and concise entailment. If original-Markdown evidence fully covers an R but is absent from GO/GC, retain `COVERED` with its actual Markdown locator and flag `EXTRACTION_GAP_CANDIDATE` for Phase 05 recovery; do not fabricate a class. Also flag potential extraction gaps found on `NOT_COVERED` items. `NOT_COVERED` includes the strongest partial candidate and decisive missing predicate, or a bounded absence receipt. Preserve basis and confidence honestly.

**Efficiency rule:** The normal path is one indexed retrieval and short predicate comparison per R, with rule-family reuse. Perform at most **one focused candidate expansion per ambiguous R** in Phase 04; do not scan all eight files separately per ID or repeatedly regenerate paraphrases. Heavier inspection is reserved for authorization, tenant isolation, approval/publication, irreversible actions, hard quantitative constraints, and contradictory evidence.

**Completion gate:** Exactly one binary, attributable decision for every R; original source locators resolve; family applicability checks and absence receipts are present; all extraction-gap candidates are identified for Phase 05; counts and IDs reconcile. This gate does **not** require all FNs to be marked `DIRECT`/`CONTEXTUAL` or a prescribed fraction of TP. Provide a compact table of decisions by basis/confidence and rule family. No Phase 05 work is silently performed here.

### Phase 05 — FN Reassessment and Extraction Recovery

**Purpose:** Correct likely misses from Phase 04 at a meaningful but bounded computational cost and reconcile its flagged extraction gaps, including those on already-covered R IDs. Treat Phase 04 decisions as the starting point. Do not redo all R-to-document semantic searches, independently reread eight files for every provisional FN, or require every FN to receive a second full semantic adjudication.

1. **Screen every provisional FN cheaply.** Assign each `NOT_COVERED` from Phase 04 to a diagnostic family, using its stored candidates and search receipts. Also collect every `EXTRACTION_GAP_CANDIDATE` from Phase 04, whether originally covered or uncovered. Detect probable issues such as an exact identifier hit, a near-direct paraphrase, missing generic-rule application, high-confidence partial coverage, a known extraction exclusion, a table-scope omission, or contradictions among similar judgments. This is an indexed **triage**, not a claim that every item received another deep semantic review.
2. **Select substantial challenges.** In the normal audit budget, deep-challenge **up to 120 risk-ranked FN groups and up to 40 reproducibly stratified FN groups** drawn across distinct files, sections, predicate families, and confidence bands. A group may contain several source IDs sharing the same decisive condition. Review at least one representative per selected group and independently verify whether its reasoning applies to other affected IDs. If fewer eligible groups exist, review them all; do not invent work to fill the budget. Record selection method and counts.
3. **Use evidence-first targeted expansion.** For selected groups, compare frozen R predicates with the strongest GO/GC evidence, universal-rule applicability, and **actual Markdown** at candidate locators. Use one targeted index expansion only if meaningful uncertainty remains. Inspect the relevant PDF passage where a source predicate or exception scope is unclear. Do not treat low similarity as decisive and do not replace semantic review with an arbitrary automatic acceptance rule.
4. **Correct confirmed misses and missing extraction.** Resolve every flagged `EXTRACTION_GAP_CANDIDATE`, including flags on Phase 04 `COVERED` IDs, and any additional extraction defect found during challenges. If a definitive source-covering statement exists but was omitted or wrongly excluded from GO/GC, first check whether an existing GC already represents it. If so, link to it. Otherwise append `RECOVERED_OCCURRENCE` and, when semantically distinct, `RECOVERED_CLASS`, using new non-colliding recovery IDs, original file/line/table evidence, and an equivalence/nonmerge reason. Reclassify the relevant prior exclusion in the overlay. Do **not** edit the frozen R/N, Phase 02, Phase 03, or Phase 04 artifacts. Reconcile effective GO/GC and reuse counts in this phase.
5. **Apply proven patterns to their affected family.** If a challenge reveals a systematic omission (for example, a general validation rule omitted for many named endpoints), search the affected **indexed family**, test applicability for its members, and change only those with complete grounded coverage. Do not assume every member is covered. This targeted family correction is not an unrestricted corpus-wide rescan.
6. **Conclude all provisional FN and flagged-gap records.** Each original Phase 04 FN receives a compact `FN_REASSESSMENT` result: `COVERED` or `NOT_COVERED`, `review_mode` (`SCREENED`, `CHALLENGED`, `FAMILY_APPLIED`, or `RECOVERED`), existing or recovered evidence IDs/locators, basis, confidence, and a meaningful decision rationale. For items screened but not deeply challenged, explicitly state that the Phase 04 decision was **retained**, not independently verified. For remaining FNs, link to the specific Phase 04 missing-predicate analysis; do not replace it with a bare phrase such as “not found.” For every Phase 04 extraction-gap flag on an already-covered R, emit an `EXTRACTION_GAP_REVIEW` with the resolved class/occurrence mapping or a documented evidence-based explanation of why no class should be recovered.
7. **Bound the work and preserve uncertainty.** After the planned challenge budget and targeted family corrections, complete the phase with binary best-effort results. Do not demand that all remaining FNs, `BEST_EFFORT` judgments, or LOW-confidence items disappear. Record unresolved semantic risks distinctly. A directly observed widespread scoring defect warrants a family correction if feasible within the same phase; if further global investigation would be open-ended, disclose the residual risk rather than claiming independent verification or silently stopping without a usable artifact.

**Normal review budget:** 120 risk-ranked + 40 stratified groups, plus finite corrections triggered by confirmed shared rules. The cap governs **deep reviews**, not the required indexed screening of every provisional FN or propagation of a proven family rule. Smaller numbers are acceptable only if the eligible population is smaller or an actual platform limitation forces a resumable `INCOMPLETE` checkpoint. Do not perform an unrestricted all-FN second pass. Avoid repeated page opens and verbose logs; batch same-family reasoning.

**Completion gate:** All Phase 04 FN IDs occur once in Phase 05 results, and every Phase 04 extraction-gap flag is resolved once; `COVERED`/`NOT_COVERED` decisions reconcile with the complete Phase 04 R population; all changes have actual evidence and an explicit reason; recovered GO/GC are traceable and assigned exactly once; review-budget/sample coverage and remaining uncertainty are reported. Phase 05 does not claim an independently exhaustive FN audit. Every recovered GC becomes part of the effective class universe for Phases 06–09. If a required population or recovery mapping cannot be reconciled, mark `INCOMPLETE` and retain a checkpoint; do not advance.

### Phase 06 — PDF Claim Validity

- Evaluate **every effective generated class**, including recovered classes from Phase 05, not only classes linked to covered R atoms.
- Use the original PDF as authority, checking complete predicates, especially negation, quantifiers, security scope, time, versions, numerical thresholds, error behavior, and exceptions.
- Assign `PDF_SUPPORTED` or `PDF_UNSUPPORTED` as a best-effort binary judgment for every class. Cite real physical PDF pages (1-based), sections/tables/figures, and decisive short quotations or resolvable frozen evidence references.
- For unsupported classes isolate exact residuals and mark `CONTRADICTION` or `UNSUPPORTED_ADDITION`, preserving class/occurrence provenance. Exclude supported portions from FP.
- `SUPPORTED_NONCOVERING` is not FP merely because no R ID matches. Do not add R atoms.
- Use cached source evidence and targeted checks. Never invent quotations; lower confidence when necessary.

### Phase 07 — FP and Negative Controls

- Normalize unsupported residuals from **all effective classes**, including recovered ones. A residual is a specific material unsupported assertion, not an entire invalid paragraph.
- Deduplicate residual propositions across all eight documents using mutually entailing full semantics. Keep distinct actors, scopes, prohibitions, exceptions, time windows, codes, and outcomes separate.
- Perform one targeted cross-cluster collision audit. Record FP cluster ID, complete proposition, class/occurrence provenance, PDF counterevidence or search basis, and equivalence reason.
- Assess every fixed negative control by searching the effective generated corpus for an **affirmative, definitive** assertion of its counterfactual. Assign `ASSERTED` or `NOT_ASSERTED`, with strongest evidence and confidence.
- Attach a semantically identical unsupported residual to an asserted fixed control and do **not** count it again as generated-only FP. Preserve genuinely independent unsupported predicates separately.
- Reconcile all residuals, clusters, every N ID, and the FP/control crosswalk. A prohibition or rejected alternative is not an affirmative counterfactual assertion.

### Phase 08 — Targeted Quality Audit

- Review the highest-risk decisions: apparent FP clusters supported by the PDF; suspicious FP merges; near-direct matches still FN after Phase 05; questionable family-rule coverage; recovered-class linkage; tenant isolation, authorization, self-approval, privacy, irreversible operations, and disputed error/status/numeric semantics.
- Challenge a bounded selection: **up to 80 risk-ranked canonical groups plus up to 20 reproducibly sampled groups**. Reuse Phase 04/05 accepted evidence; do not repeat their entire coverage analysis. Beyond-budget review requires a concrete material inconsistency and explanation.
- A same-context self-check is not an independent reviewer; never claim independent verification without an actual distinct reviewer/context.
- Use `CHANGE` records for corrections with prior/new decision, actual evidence, affected R/GC/N/FP IDs. Prior phase artifacts remain immutable. Apply corresponding overlay reconciliations for recovered GO/GC and their dependent judgments.
- Produce exactly one `FINAL_SOURCE` per frozen R, one `FINAL_CLASS` per **effective** GC, one `FINAL_CONTROL` per frozen N, one `FINAL_FP_CLUSTER` per canonical generated-only FP, plus `FINAL_SUMMARY`, material `REFERENCE_EXCEPTION`, and applicable `CHANGE` rows. References may point to immutable earlier evidence.
- Ensure all corrections propagate to related classifications. Remaining LOW and `BEST_EFFORT` decisions retain defensible binary outcomes.

### Phase 09 — Metrics and Delivery

- Derive counts **only** from Phase 08's final item-level ledger, not a manual summary or earlier estimates.
- Verify every R/N ID occurs once with legal final status; base and recovered eligible occurrences each map to exactly one effective class; every effective GC has one PDF decision; every unsupported residual maps to an asserted N or one canonical generated-only FP; no FP/control double count.
- Calculate single-value TP, TN, FP, FN, Precision, Recall, F1, claim validity, and duplicate/reuse metrics. Do not replace them with intervals.
- Recheck original reference/input hashes and include input/artifact provenance. Reconcile Phase 05 overlay counts and all changes.
- Report the initial Phase 04 FN count; number screened and deeply challenged; FN-to-TP corrections; extraction recoveries; retained FN confidence distribution; uncorrected known limitations; audited changes; and benchmarks' scoring interpretation. Do not claim the screened-only FN population was independently semantically reviewed.
- If material input/hash/ID invariants fail, emit `BLOCKED` or `INVALID_REFERENCE_CHANGED` and no fabricated valid scores.

## 5. Exact scoring policy

The main scores are a **benchmark-specific canonical proposition projection**, not raw sentence-level precision and not an ordinary symmetric sample confusion matrix. This is necessary because one generated universal proposition can cover several frozen positive source atoms, while one unsupported proposition can appear in several documents.

Let:

```text
R_total = count(frozen source-positive IDs)
N_total = count(frozen negative-control IDs)

TP = count(FINAL_SOURCE.decision == "COVERED")
FN = count(FINAL_SOURCE.decision == "NOT_COVERED")
TN = count(FINAL_CONTROL.decision == "NOT_ASSERTED")
B_asserted = count(FINAL_CONTROL.decision == "ASSERTED")
F_only = count(unique FINAL_FP_CLUSTER not represented by an asserted N)
FP = B_asserted + F_only

TP + FN = R_total
TN + B_asserted = N_total

Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1 = 2 * TP / (2 * TP + FP + FN)
```

Return JSON `null` for a zero-denominator ratio and state the reason; do not invent a percentage. The final report must clearly distinguish `B_asserted` and `F_only` even though both contribute to FP. **TN counts only the bounded declared negative controls**, not all possible absent behaviors. No population-wide specificity or accuracy should be inferred from TN.

Additional quality metrics:

```text
GO = count(effective eligible generated occurrences, including Phase 05 recoveries after explicit reclassifications)
GC = count(effective distinct generated classes, including Phase 05 recoveries)
D_expected = count(excess occurrences with EXPECTED_REUSE)
D_redundant = count(excess occurrences with REDUNDANT_DUPLICATE)
GO = GC + D_expected + D_redundant

G_supported = count(FINAL_CLASS.pdf_decision == "PDF_SUPPORTED")
G_unsupported = count(FINAL_CLASS.pdf_decision == "PDF_UNSUPPORTED")
G_supported + G_unsupported = GC

ClaimValidity = G_supported / GC
ExpectedReuseRate = D_expected / GO
RedundantDuplicateRate = D_redundant / GO
```

Report confidence coverage separately, including FN review mode, the number of deep-challenged FNs, and the number of final scoring judgments marked `BEST_EFFORT` and `LOW`. **Do not turn these annotations into metric bounds.** They indicate how much interpretation entered the point estimates.

## 6. Compact machine-readable record contract

All JSONL records are UTF-8 and contain `record_type`. Use JSON `null` for missing optional values. The examples below describe required *field families*, not invented actual findings.

| Record | Essential fields |
|---|---|
| `OCCURRENCE` | `occurrence_id`, `file`, `line_start`, `line_end`, optional `table_locator`, `statement_en`, `context_locator`, `predicate_summary`, `basis` |
| `EXCLUSION` / `RECLASSIFIED_EXCLUSION` | ID, original file/line or occurrence ID, excluded text/category, concise `reason_en` |
| `CLASS` | `class_id`, `normalized_proposition_en`, `representative_occurrence_id`, `member_occurrence_ids`, predicate summary, evidence/confidence |
| `DUPLICATE` | `occurrence_id`, `class_id`, `duplicate_type`, role or redundancy reason |
| `SOURCE_JUDGMENT` | `source_id`, binary `decision`, matched class/occurrence IDs, generated locators, missing predicate if applicable, evidence/basis/confidence/reason |
| `FN_REASSESSMENT` | `source_id`, Phase 04 decision, current binary decision, `review_mode`, diagnostic family, selected candidate/evidence links, basis/confidence, missing predicate or correction reason |
| `EXTRACTION_GAP_REVIEW` | flagged `source_id`, original Phase 04 status, resolved class/occurrence mapping or documented non-recovery rationale, original Markdown locator |
| `FN_FAMILY` / `FN_CHALLENGE` | family ID, member IDs, risk or sample selection, representative review, applicability limits, search receipts, grouped outcomes |
| `RECOVERED_OCCURRENCE` / `RECOVERED_CLASS` | stable recovery ID, original generated file/line/table locator, exact claim, relevant prior exclusion, membership/equivalence evidence, effective GO/GC crosswalk |
| `FN_CHANGE` | `source_id`, old/new decisions, prior and repaired evidence IDs, reason, dependent class recovery when applicable |
| `PDF_JUDGMENT` | `class_id`, binary `pdf_decision`, PDF physical pages and quotations/locators, `supported_noncovering`, unsupported residuals, basis/confidence/reason |
| `FP_CLUSTER` | `fp_cluster_id`, complete unsupported proposition, originating class/occurrence IDs, PDF counterevidence or search basis, equivalence proof, asserted-control crosswalk |
| `NEGATIVE_CONTROL` | `negative_control_id`, binary `decision`, generated proof or absence-search basis, matching FP cluster IDs, basis/confidence/reason |
| `FINAL_SOURCE` / `FINAL_CLASS` / `FINAL_CONTROL` / `FINAL_FP_CLUSTER` | Final decision and all IDs necessary to reconstruct metrics; citations may refer to prior phase records |
| `CHANGE` | `change_id`, affected IDs, old/new decisions, actual evidence, reason and dependent correction |
| `PHASE_SUMMARY` / `FINAL_SUMMARY` | Counts, Phase 05 screening/challenge and recovery reconciliations, input digests/refs, issues, confidence breakdown, completion status |

A concise source quote or resolvable evidence reference is sufficient for clear routine matches. For consequential or disputed claims, include the decisive actual quotation and enough context to prove the scope. The evaluator must not assert `DIRECT` without an inspected text match, invent evidence, or use placeholder source IDs as real findings.

## 7. Quality gates and reproducibility checks

**Mandatory mechanical checks:**

1. All expected input roles are readable and unambiguous; required reference hashes match the freeze record.
2. The immutable R/N inputs are unchanged; source IDs and negative-control IDs are unique and complete.
3. All eight generated files were examined; every extracted eligible occurrence has a locatable origin.
4. Every base or recovered eligible generated occurrence belongs to exactly one effective generated class; exclusions and class additions remain traceable without rewriting earlier phases.
5. Every R has one Phase 04 binary verdict with real search/candidate receipts and a semantic reason; `NOT_COVERED` is never based solely on low lexical score.
6. Every Phase 04 FN receives one Phase 05 screening record and every Phase 04 extraction-gap flag is resolved; selected deep challenges, risk and stratified selection, corrected items, and extraction repairs are reconciled without claiming universal deep review.
7. Every effective class receives exactly one PDF-supported/unsupported decision with verifiable provenance; every unsupported residual is traceable.
8. Every frozen N receives one asserted/not-asserted result; generated residual FPs are canonically deduplicated without double counting controls.
9. Each final correction updates all dependent records and preserves the prior decision in a `CHANGE` or linked Phase 05 correction record.
10. The final numerical equations in Section 5 hold for the **effective** GO/GC universe; metrics derive from Phase 08 final records, not estimates in a report.
11. All deliverables are in English, all cited original file/page/line locators resolve, and every reported verification was actually performed.

**Semantic quality is best-effort, not mechanically certified.** The checks above establish structural reproducibility, not automatic logical correctness. Unreviewed or uncertain semantics must receive a documented `BEST_EFFORT` decision and lower confidence where warranted. Do not invent 100% certainty from completion of these gates.

## 8. Operator sequence and completion rule

1. Supply the fixed reference pair, freeze metadata, original PDF, and all eight generated specifications.
2. Execute only the next requested phase, following the nine-phase order in Section 4.
3. Do not advance before the current phase's ID population, required artifact, and mechanical acceptance checks are completed.
4. Prioritize strong Phase 04 semantic judgment and bounded Phase 05 FN challenges. Use shared indexes, rule families, deterministic sampling, and compact outputs. Do not spend an unbounded amount of effort chasing every borderline equivalence.
5. If nonblocking semantic uncertainty persists within the review budget, make a reasoned best-effort binary decision and report confidence/remaining risk. If a real input, platform, or required mapping blocker prevents population coverage, report the blocker and resumable incomplete checkpoint; do not claim completion.
6. Keep all inputs and previously completed phase artifacts immutable. Phase 05 recoveries are linked overlays; final revisions are recorded as corrections in Phase 08.
7. Deliver only the required artifact(s) for the current phase, along with a concise factual completion summary. Do not generate ZIP archives, auxiliary review files, or lengthy process logs unless the operator separately requests them.

**Final rule:** Produce one set of auditable, best-effort **point estimates** for TP, TN, FP, FN, Precision, Recall, and F1. Preserve fixed reference truth, semantic FP deduplication, and transparency about judgment confidence. Do not substitute interval estimates, unlimited audits, or invented certainty for a finished evaluation.
