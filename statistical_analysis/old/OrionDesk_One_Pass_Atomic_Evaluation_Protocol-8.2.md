# OrionDesk AI — Practical Atomic Specification Evaluation Protocol

**Protocol version:** 8.2  
**Status:** Standalone evaluation procedure  
**Purpose:** Evaluate the completeness and factual fidelity of eight generated software-design specifications against one immutable, PDF-grounded reference.  
**Execution:** Eight ordered phases, one phase at a time, using efficient retrieval, risk-weighted semantic adjudication, and auditable best-effort final classifications.  
**Output language:** **All authored files, including Markdown, JSON/JSONL values, program code/comments, explanations, and reports, must be written entirely in English.** Exact source quotations retain their source wording.

## 1. Objective and priorities

The evaluator must produce a **single best-effort determination** for each of TP, TN, FP, and FN, followed by Precision, Recall, and F1. **Do not replace the final counts with lower/upper bounds or uncertainty intervals.** Preserve uncertainty as a separate quality annotation on individual judgments and in the report.

Priorities, in order:

1. Keep the frozen benchmark untouched and use the original PDF as the semantic authority.
2. Assess actual meaning, including scope, exceptions, modality, actors, and consequences; avoid mere word matching.
3. Count a source-positive requirement once, and count a distinct unsupported generated proposition once across all eight specifications.
4. Finish each phase with a coherent result rather than pursuing unlimited verification. Apply deeper review where material error risk is high.
5. Retain enough source evidence and identifiers to explain, challenge, and reproduce the scores, without creating redundant audit files.

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

An uncertain decision **still contributes to final counts**. Never count an unresolved item automatically as FP or FN solely because it is unresolved. Instead, make an evidence-based best-effort choice and label its confidence. `BEST_EFFORT` means the verdict was selected with limited proof; it is not a claim of verification.

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

The evaluator must work in **one phase at a time**. The normal goal is to complete the requested phase in one request–response, without an artificial requirement to perform endless second reviews. A phase cannot be marked complete if a required input or complete ID population is missing; if a platform limit genuinely prevents finishing it, preserve a resumable checkpoint and continue **that same phase** on the next turn, never silently advance.

Use one shared retrieval preparation rather than repeatedly reading all eight documents for each item:

1. Parse the PDF into a physical-page/section search index, retaining table and figure references; inspect images only when visual meaning matters. Use existing PDF evidence in frozen atoms where helpful.
2. Parse the eight Markdown files once. Record headings, lines, table headers/cells, IDs, routes, error literals, numerical constraints, and inherited scope.
3. Build reusable lexical/identifier/alias indexes and optionally embeddings or approximate-nearest-neighbor candidates. These **find candidates**; they do not by themselves prove coverage, unsupported meaning, or equivalence.
4. Use short semantic adjudication on obvious direct or contextual matches, and deeper reasoning only for ambiguous, contradictory, high-impact, or highly duplicated cases.
5. For each item, inspect a small set of strongest candidates plus relevant universal/exception context. Expand the search **only if** conflicting evidence, ambiguous scope, or likely missed synonyms warrant it.
6. Reuse the same accepted evidence and normalized predicates across phases. Do not redo an entire analysis simply because an item appears in another phase.
7. Record a compact receipt (`searched_files`, key query/alias variants, strongest locators, decisive rejected candidate if necessary), **not exhaustive transcripts of every search hit**.

A fast exact match may be accepted with `DIRECT` only when the complete predicate and relevant context actually match. A single fuzzy score may **never** finalize a semantic judgment. For classes of repetitive claims with the same proven context and rule, adjudicate a representative, check applicability for each member, and reuse the reasoning; do not require a full essay per member.

### 3.1 Bounded review and audit policy

- Avoid all-pairs comparisons among thousands of claims. Use deterministic blocking (identifiers, normalized actor/action/object, paths, numeric values) and semantic candidate ranking to form plausible equivalence groups.
- Perform one principal semantic grouping pass and one **targeted cross-group collision check**, not an unrestricted global re-review.
- For each source requirement, conduct one indexed eight-file candidate search, with one focused expansion only where material uncertainty exists. No requirement for eight separate narrative search reports.
- For each generated class, start with direct source locators/cross-references and targeted PDF search. Expand to surrounding sections, exceptions, and relevant global rules only when needed.
- Treat the main evidence pass as the default. Deep challenge is reserved for consequential errors and a bounded representative sample, not every decision.
- If the quality of a judgment remains uncertain at the end of the permitted focused review, **choose a best-effort binary decision, mark `LOW`, and proceed**. This rule is not permission to invent missing evidence or to skip entire ID populations.

## 4. Eight ordered phases and deliverables

The required output is **one consolidated file for each of Phases 01–07**, plus a calculator, metrics JSON, and readable report in Phase 08. Thus the normal deliverable set contains **10 files**. Temporary scripts/indexes may be used locally but are not deliverables. Every phase includes a compact summary with processed counts, ID reconciliation, validation results, low-confidence totals, material exceptions, and `status`.

| Phase | Task | Required artifact | Completion gate |
|---|---|---|---|
| **01 — Reference Lock** | Validate and freeze inputs, hashes, PDF page count, and R/N IDs | `01_reference_lock.json` | All required inputs resolved; expected reference hashes match |
| **02 — Generated Extraction** | Extract eligible atomic commitments from all eight specifications, restoring context | `02_generated_occurrences.jsonl` | Every substantive section/table examined; all generated occurrences have unique IDs and locators |
| **03 — Semantic Deduplication** | Group equivalent generated occurrences and classify duplicate roles | `03_semantic_classes.jsonl` | Every eligible occurrence belongs to exactly one class; count reconciliation holds |
| **04 — Source Coverage** | Evaluate every frozen R against the complete eight-file corpus | `04_source_coverage.jsonl` | Exactly one binary, evidence-based decision for each R ID |
| **05 — PDF Claim Validity** | Check every GC against the original PDF; identify unsupported residuals | `05_pdf_validity.jsonl` | Exactly one binary PDF judgment for each GC; unsupported residuals traceable |
| **06 — FP and Control Audit** | Deduplicate residual FPs across all files; assess every frozen N; remove double counting | `06_fp_controls.jsonl` | All residuals assigned, every N adjudicated, no duplicate FP/control proposition counted twice |
| **07 — Targeted Quality Audit** | Challenge high-impact judgments and produce one corrected final item-level snapshot | `07_final_ledger.jsonl` | Corrections fully reconciled; all R/GC/N and final FP clusters represented |
| **08 — Metrics and Delivery** | Recompute reproducible single-value scores and report limitations | `compute_metrics.py`, `08_metrics.json`, `08_report.md` | Identity/hashes/count equations pass or an explicit blocked run is declared |

### Phase 01 — Reference Lock

- Read and validate all input files as UTF-8 or PDF, count physical PDF pages, and hash actual bytes.
- Parse every R and N record, reject malformed JSONL, missing IDs, duplicate IDs, label errors, or reference-digest mismatches.
- Record actual filenames, SHA-256, reference version/status, positive and negative counts, PDF pages, input problems, and preserved upstream limitations.
- Do **not** re-extract Gold Set requirements or check upstream Gold Set completeness.

### Phase 02 — Generated Extraction

- Read all eight Markdown specifications. Extract complete independent **definitive** commitments, including meaningful statements reconstructed from tables and supported inherited scope.
- Assign stable occurrence IDs (`GEN-000001`...) ordered by file, original line and cell position. Each row records source locator, text or normalized proposition, substantive context, and eligibility basis.
- Maintain **section/table-level** coverage summaries for every file. Log meaningful exclusions by range/category and the associated reason; do not emit an exhaustive record for every formatting-only line or cell.
- Separate open items from adopted decisions in the architecture register. Never turn a question, a hypothetical alternative, or a fictional example into an implemented requirement.
- Accept that this stage may retain a small number of questionable atoms flagged for Phase 03; avoid generating artificial standalone atoms from headings.

### Phase 03 — Semantic Deduplication

- Normalize material predicates and use indexed candidate generation across **all eight** specifications.
- One class (`GC-000001`...) represents exactly one complete mutually entailing proposition. Keep a representative occurrence and all member occurrence IDs and locators.
- For each excess occurrence, classify `EXPECTED_REUSE` where it serves a concrete independent specification role, otherwise `REDUNDANT_DUPLICATE`. A different file alone does not prove useful reuse.
- Check likely cross-group paraphrase collisions, but do not spend unlimited cycles comparing all low-similarity pairs. Keep uncertain candidates separate; record low-confidence nonmerges or merges with a short reason.
- Remove any clear editorial/non-atomic extraction mistakes from scoring using explicit `RECLASSIFIED_EXCLUSION` entries; preserve their original extraction IDs and provenance without editing the previous phase file.
- Reconcile `GO = GC + EXPECTED_REUSE + REDUNDANT_DUPLICATE`, after documented reclassifications. This phase determines generated uniqueness, **not PDF truth**.

### Phase 04 — Source Coverage

- Evaluate **all** frozen `source_id` values against the full eight-file generated corpus, primarily through the shared indexes and current semantic classes.
- Restore each source atom's PDF context and test material predicates against definitive generated assertions, including relevant cross-document conjunctions and universal rules.
- Assign one binary `COVERED` or `NOT_COVERED` to every source atom. Link at least one generated class/occurrence and actual generated locator for each covered result. For not covered, retain the strongest partial candidate or a compact absence-search basis and the missing predicates.
- Apply a focused second candidate search only when ambiguous or contradicted. Where full entailment remains doubtful after a proportionate review, make a defensible best-effort verdict and record its confidence.
- A generated class can support multiple source IDs; a source ID counts at most once. Do not infer source coverage from shared keywords or a section title.

### Phase 05 — PDF Claim Validity

- Evaluate **every** generated class, not only classes linked to covered R atoms.
- Use the PDF as authority. Check complete predicates, especially negation, quantifiers, security scope, time, version, numerical thresholds, error behavior, and exceptions.
- Assign `PDF_SUPPORTED` or `PDF_UNSUPPORTED` as a best-effort binary judgment for every class. Cite real physical PDF pages (1-based), sections/tables/figures, and decisive short quotations or existing frozen evidence references.
- For unsupported classes, identify exact residual proposition(s) and classify them as `CONTRADICTION` or `UNSUPPORTED_ADDITION`; record class/occurrence provenance. Keep supported portions out of FP.
- A supported class with zero R matches is `SUPPORTED_NONCOVERING`, not FP. Do not add it to R or treat an absent Gold Set match as negative evidence.
- Do not manufacture source quotations. If support is incomplete after focused research, make the best-evidence judgment and flag lower confidence.

### Phase 06 — FP and Negative Controls

- Normalize residual propositions from unsupported classes. A residual is a **specific material unsupported assertion**, not an entire invalid paragraph.
- Deduplicate residuals across **all eight files** using mutually entailing full semantics. Keep distinct actors, scopes, prohibitions, exceptions, time windows, codes, and outcomes separate.
- Run one targeted cross-cluster collision audit to catch repeated FP paraphrases or incorrect merges. For every canonical cluster record one FP ID, full proposition, originating class/occurrence IDs, source evidence and a short equivalence reason.
- Evaluate every frozen negative control by searching the generated corpus for an **affirmative, definitive** assertion of its counterfactual proposition. Assign `ASSERTED` or `NOT_ASSERTED`; include the strongest evidence and confidence.
- If a canonical unsupported residual is semantically the same proposition as an asserted fixed control, attach the residual to that control and **do not count it again in generated-only FPs**. If there are additional independent unsupported predicates, preserve only those as separate residuals.
- Do not assume a broad class asserting several distinct N controls is one control, or that every reference-control phrase appearing in a prohibition is asserted.
- Reconcile the full residual universe, cluster memberships, all N IDs and the FP/control crosswalk.

### Phase 07 — Targeted Quality Audit

- Review the highest-risk decisions: apparent FP clusters supported by the PDF; suspicious many-to-one FP merges; near-direct matches labeled FN; broad/universal coverage; tenant isolation; authorization; self-approval; privacy; irreversible operations; and contested error/status/threshold semantics.
- Challenge a **bounded prioritized selection**, plus a small reproducible sample of ordinary items. Deep-review up to 80 risk-ranked canonical groups plus up to 20 deterministically sampled other groups as the normal audit budget. Additional review is allowed only for a concrete material contradiction; explain any exception to this cap.
- Reuse earlier evidence. A single same-context self-check is **not** an independent reviewer; never claim independent adjudication without an actual distinct reviewer/context.
- Resolve discovered mistakes using new `CHANGE` records with old/new decisions, evidence and affected IDs. Preserve earlier phase outputs unchanged.
- Produce a compact but complete final item-level snapshot: one `FINAL_SOURCE` per R, one `FINAL_CLASS` per GC, one `FINAL_CONTROL` per N, one `FINAL_FP_CLUSTER` per canonical generated-only FP, plus `FINAL_SUMMARY`, material `REFERENCE_EXCEPTION`, and `CHANGE` rows. Each final row may point to a previous immutable evidence record rather than copy its text.
- Recompute all linked classifications after corrections. Remaining low-confidence items retain binary best-effort decisions, not an unknown scoring class.

### Phase 08 — Metrics and Delivery

- Derive all counts from the **Phase 07 final item-level ledger**, not a manually written summary or previous metrics.
- Verify every frozen R/N ID occurs exactly once with legal final status; every generated occurrence maps to one class; all classes have PDF outcomes; every unsupported residual maps to a canonical FP cluster or an asserted negative control; there is no FP/control double count.
- Independently calculate and write single-number TP, TN, FP, FN, Precision, Recall, F1, claim validity and duplicate metrics. Do not output score ranges or substitute ambiguous labels for a final count.
- Hash-check the original reference inputs again, verify all input file identities, and include a succinct artifact inventory and provenance.
- Report direct/contextual/best-effort counts, low-confidence decision totals, principal open limitations, audited corrections, and benchmark-scoring interpretation. Do not describe best-effort outcomes as independently verified facts.
- If a blocking input/hash invariant fails, emit an explicit `BLOCKED`/`INVALID_REFERENCE_CHANGED` report and **no invented valid scores**.

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
GO = count(eligible generated occurrences after explicit reclassifications)
GC = count(distinct generated classes)
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

Report confidence coverage separately, for example the number of final scoring judgments marked `BEST_EFFORT` and `LOW`. **Do not turn these annotations into metric bounds.** They indicate how much interpretation entered the point estimates.

## 6. Compact machine-readable record contract

All JSONL records are UTF-8 and contain `record_type`. Use JSON `null` for missing optional values. The examples below describe required *field families*, not invented actual findings.

| Record | Essential fields |
|---|---|
| `OCCURRENCE` | `occurrence_id`, `file`, `line_start`, `line_end`, optional `table_locator`, `statement_en`, `context_locator`, `predicate_summary`, `basis` |
| `EXCLUSION` / `RECLASSIFIED_EXCLUSION` | ID, original file/line or occurrence ID, excluded text/category, concise `reason_en` |
| `CLASS` | `class_id`, `normalized_proposition_en`, `representative_occurrence_id`, `member_occurrence_ids`, predicate summary, evidence/confidence |
| `DUPLICATE` | `occurrence_id`, `class_id`, `duplicate_type`, role or redundancy reason |
| `SOURCE_JUDGMENT` | `source_id`, binary `decision`, matched class/occurrence IDs, generated locators, missing predicate if applicable, evidence/basis/confidence/reason |
| `PDF_JUDGMENT` | `class_id`, binary `pdf_decision`, PDF physical pages and quotations/locators, `supported_noncovering`, unsupported residuals, basis/confidence/reason |
| `FP_CLUSTER` | `fp_cluster_id`, complete unsupported proposition, originating class/occurrence IDs, PDF counterevidence or search basis, equivalence proof, asserted-control crosswalk |
| `NEGATIVE_CONTROL` | `negative_control_id`, binary `decision`, generated proof or absence-search basis, matching FP cluster IDs, basis/confidence/reason |
| `FINAL_SOURCE` / `FINAL_CLASS` / `FINAL_CONTROL` / `FINAL_FP_CLUSTER` | Final decision and all IDs necessary to reconstruct metrics; citations may refer to prior phase records |
| `CHANGE` | `change_id`, affected IDs, old/new decisions, actual evidence, reason and dependent correction |
| `PHASE_SUMMARY` / `FINAL_SUMMARY` | Counts, reconciliation equations, input digests/refs, issues, confidence breakdown, completion status |

A concise source quote or resolvable evidence reference is sufficient for clear routine matches. For consequential or disputed claims, include the decisive actual quotation and enough context to prove the scope. The evaluator must not assert `DIRECT` without an inspected text match, invent evidence, or use placeholder source IDs as real findings.

## 7. Quality gates and reproducibility checks

**Mandatory mechanical checks:**

1. All expected input roles are readable and unambiguous; required reference hashes match the freeze record.
2. The immutable R/N inputs are unchanged; source IDs and negative-control IDs are unique and complete.
3. All eight generated files were examined; every extracted eligible occurrence has a locatable origin.
4. Every eligible generated occurrence belongs to exactly one generated class; documented removals remain traceable.
5. Every source-positive ID has one `COVERED`/`NOT_COVERED` decision with a stated rationale and confidence.
6. Every class has one PDF-supported/unsupported decision, and every unsupported residual has traceable provenance.
7. Every negative control has one asserted/not-asserted result; FP residuals are canonically deduplicated and not double-counted against controls.
8. Each audit correction updates all dependent final records and maintains its prior decision as a `CHANGE` entry.
9. The final numerical equations in Section 5 hold, and metrics come from final records, not estimates in a report.
10. All authored deliverables are in English, all cited file/page/line locators resolve, and every reported verification was actually performed.

**Semantic quality is best-effort, not mechanically certified.** The checks above establish structural reproducibility, not automatic logical correctness. Unreviewed or uncertain semantics must receive a documented `BEST_EFFORT` decision and lower confidence where warranted. Do not invent 100% certainty from completion of these gates.

## 8. Operator sequence and completion rule

1. Supply the fixed reference pair, freeze metadata, original PDF, and all eight generated specifications.
2. Execute only the next requested phase, following the order in Section 4.
3. Do not advance before the current phase's ID population, required artifact, and mechanical acceptance checks are completed.
4. Prefer efficient one-turn completion using the prepared indexes, representative judgments, selective deep review, and compact outputs. Do not spend an unbounded amount of effort chasing every borderline equivalence.
5. If a nonblocking semantic ambiguity persists, **make a clearly labeled best-effort binary decision and complete the phase**. If a real input or platform blocker prevents required population coverage, report the blocker, checkpoint, and incomplete status; do not claim success.
6. Keep all inputs and previously completed phase artifacts immutable. Revisions are appended as correction records in the final ledger.
7. Deliver only the required artifact(s) for the current phase, along with a concise factual completion summary. Do not generate ZIP archives, auxiliary review files, or lengthy process logs unless the operator separately requests them.

**Final rule:** Produce one set of auditable, best-effort **point estimates** for TP, TN, FP, FN, Precision, Recall, and F1. Preserve fixed reference truth, semantic FP deduplication, and transparency about judgment confidence. Do not substitute interval estimates, unlimited audits, or invented certainty for a finished evaluation.
