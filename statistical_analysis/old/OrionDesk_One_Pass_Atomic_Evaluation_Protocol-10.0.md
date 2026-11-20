# OrionDesk AI — Eight-Phase Semantic-Entailment Atomic Requirement Evaluation Protocol

**Protocol version:** 10.0
**Core method:** Preserve v6.1 meaningful PDF/generated atomization, semantic class equivalence, full-predicate entailment, reciprocal FN challenge, and canonical four-cell universe.  
**Primary objective:** Measure TP, TN, FP, FN, Precision, Recall, and F1 for eight generated design specifications against a PDF-grounded benchmark without unsupported claim inflation.  
**Secondary objective:** Quantify semantic duplication independently of correctness and source coverage.  
**Execution:** Exactly eight ordered phases, one phase per user request–response. Complete the current phase before proceeding; do not perform later phases in the same turn.  
**Supported methods:** `fullload`, `onelevel`, `twolevel`.  
**Conversation language:** Follow the operator's request.  
**All authored files, scripts, comments, JSON/JSONL values written as prose, and reports:** English only.  
**Delivery:** Individual phase artifacts; no archive unless explicitly requested.  
**This revision is a protocol revision, not an evaluation phase.**

## 1. Binding instructions and evaluation scope

The evaluation compares the original 90-physical-page English *OrionDesk AI Detailed Application Design Specification* with eight supplied Markdown specification documents per selected method. The authoritative PDF may use a timestamped or untimestamped filename. Verify its identity, 90-page extent, and readable content rather than trusting its filename.

The **sole authority for what the source specification actually means is the PDF**. A verified, frozen, PDF-grounded `R`/`N` benchmark may be the fixed scoring inventory; its contents are data to verify, not independent proof of PDF truth. Generated Markdown, aggregate JSON, previous judgments, historical atom counts, and earlier scores cannot add PDF requirements or serve as evidence of their correctness. Inspect every physical PDF page, including diagrams, figures, tables, appendices, restrictions, exceptions, and captions, and inspect every substantive physical line and table cell of each scored Markdown document.

The evaluation's **primary matching rule is complete, justified semantic entailment**, not textual identity, one-to-one document-location identity, or syntactic similarity. A requirement may be satisfied by a generated universal/shared rule, a requirement stated elsewhere in the generated corpus, or a combination of explicit generated commitments, provided that the full target requirement—including relevant conditions, scope, actor, exception, timing, and outcome—follows logically from the cited statements.

**Important structural distinction:** A single generated class may cover several independently justified source-positive atoms, but that does not create extra generated occurrences or duplicate classes. Consequently, the positive-prediction count in the canonical decision universe is **not required to equal the number of raw generated semantic classes**. All four confusion cells must nevertheless be computed from the **same** explicitly enumerated decision universe.

### Non-negotiable rules

1. **Evidence before scores.** Support every source-positive atom with PDF evidence. Support every TP with generated evidence plus a complete logical applicability bridge. For FN, record a corpus-wide search and why plausible general rules fail or do not cover it. For FP, record the precise unentailed or contradicted generated commitment.
2. **No goldset leakage or reference drift.** In benchmark-construction mode, extract `R`/`N` from the PDF independently **before** inspecting generated predictions and lock them by the end of Phase 01. In frozen-benchmark mode, use the supplied byte-verified `R`/`N` as-is, and do not alter them during scoring. The PDF remains the source for interpretation. Reference or aggregate JSON is not a ninth scored input.
3. **Meaningful atomicity; no artificial multiplication.** Split genuinely independently testable obligations, fields, constraints, actors, endpoints, conditions, exceptions, outcomes, and limits. Do **not** manufacture multiple identical source atoms by repeating a universal boilerplate requirement for every endpoint or every chapter when the PDF does not establish a distinct testable obligation. Likewise, do not discard unique endpoint-specific duties merely because a common rule exists.
4. **Semantic entailment before absence.** Before labeling any PDF atom FN, examine exact matches, synonyms, universal/shared constraints, inherited section/table context, and explicit multi-document bridges. Missing lexical overlap is not proof of a missing requirement.
5. **No unsupported TP inflation.** Merely mentioning the same API, field, actor, or topic is insufficient. Generic validation does not establish a specific response code, timing requirement, revision predicate, or exception policy unless those conditions are explicitly entailed.
6. **Stable comparisons.** Apply exactly the same frozen PDF-positive inventory `R`, bounded source-negative inventory `N`, PDF identity, eligibility tests, and semantic/counting rules to every selected method. Generated occurrences, classes, bridges, and judgments remain method-specific. No method-specific source denominator changes.
7. **No fabricated evidence or scores.** Make an explicit, reproducible best-effort determination for normal semantic ambiguity. Missing, corrupted, or unreadable mandatory source material is a genuine input blocker; it must not be pretended to be an E0 finding or a fully audited score.
8. **One response, one phase.** Use as many internal actions as necessary to finish the current phase and its English deliverables. Never advance with incomplete required populations. If a real technical limit blocks completion, checkpoint the same phase with `INCOMPLETE` and resume it, rather than declaring success or skipping ahead. Resolve ordinary semantic uncertainty using §4.2 instead of endless review.
9. **Necessary controls only.** Require identity/hash checks for the frozen reference and original scored inputs; avoid unrelated registries, administrative sign-offs, repetitive rescans, or unsolicited archives. This does not eliminate substantive PDF requirements for product digests, audit proofs, or release signatures.
10. **Do not treat claims in unresolved registers as adopted decisions.** `Confirmed`, `TBD`, `Needs confirmation`, `Proposal`, `Unadopted proposal`, and `Resolved` are claim-status evidence, not substitutes for PDF verification or approval.
11. **Mandatory reciprocal FN challenge.** A retrieval miss is only a provisional FN. In Phase 04, challenge **every** provisional FN in both directions using identifiers, canonical targets, table context, aliases, universal rules, and cross-file conjunction. Correct an explicitly demonstrated complete match immediately by an evidence-linked `CHANGE` overlay, without rewriting earlier phase artifacts.
12. **All-TP and atomization audit.** Review **every provisional TP** for complete predicates and source applicability, plus source-atom artificial splits, repeated universal boilerplate, and duplicated test outcomes. Verify every extracted generated proposition is a meaningful assertion, not a free-floating cell. Structural arithmetic does not certify semantic correctness.
13. **No silent quality claims.** A plausible `BEST_EFFORT` matrix is not verified coverage. Report conservative judgments, extraction/atomization exceptions, low-confidence evidence, reference limitations, and any uncorrected issue. Neither high Recall nor arithmetic reconciliation proves semantic completeness.
14. **No silent omission.** Every substantive source region in all eight files must be accounted for as an eligible proposition, a nondefinitive/explanatory segment, or context attached to another recorded proposition. A count of `EXCLUSION` records is not a count of removed requirements; an unsupported, definitive assertion must not disappear into exclusions.

## 2. Inputs

**Authoritative reference:** The supplied original 90-page English PDF.

**Eight required scored Markdown roles per selected method:**

1. `01_screen_functions.md`
2. `02_api.md` (also accept `02_api_.md` when that is the actual supplied filename)
3. `03_data.md`
4. `04_batch_functions.md`
5. `05_business_rules.md`
6. `06_exception_handling.md`
7. `07_processing_flows.md`
8. `08_architecture_decision.md`

Accept recognizable method prefixes, timestamps, and copy suffixes only if each input can be mapped **unambiguously** to exactly one role. Retain the actual unchanged filename in every evidence locator. Do not substitute an arbitrary similarly named file.

`08_architecture_decision.md` is a scored input, but its unresolved questions and unadopted proposals are **not human-approved implementation commitments**. A genuine, explicitly resolved and definitively stated commitment may be scored if it meets §3.2; the status `Resolved` still does not override the PDF.

Evaluate explicitly selected methods, or all complete eight-file sets if no method is selected. Do not generate, silently correct, or modify the supplied scored Markdown inputs. The attached instruction document itself is not a scored input. An aggregate JSON file is not a ninth scored Markdown input.

**Reference input and precedence:**

- **Frozen-benchmark mode (mandatory when a frozen set is supplied):** Require `common_atomic_reqs.jsonl`, `common_negative_controls.jsonl`, and `reference_freeze.json`. Accept upload-copy suffixes but retain exact filenames; identify the positive key as the declared `requirement_id` or `source_id`, and the negative key as the declared `control_id` or `negative_control_id`. Reject mixed/ambiguous keys, duplicate IDs, malformed JSONL, or mismatched hashes. Check every applicable expected file digest, the original PDF SHA-256, physical page count, document identity, and evidence availability; record the reference status and limitations. The input records and bytes remain unchanged.
- **Benchmark-construction mode (only if no frozen reference is supplied):** Phase 01 applies **unchanged v6.1 source extraction principles in §§3.1 and 3.3** to the original PDF; inspects all pages/figures/tables; validates evidence and source deduplication; builds and locks new `R`/`N` *before* any generated claim extraction. Write their hashes to a Phase 01 reference lock. These new references are shared by every selected method and cannot change after Phase 01. This mode must be declared and must not silently replace a failed supplied frozen benchmark.
- Do not re-extract a competing scored source inventory when frozen mode applies. A v6.1-style read-only semantic/atomization examination may identify reference problems, but cannot modify or extend scored `R`/`N`. Record material disagreements as `REFERENCE_EXCEPTION`; mark affected interpretation/provisional quality transparently, and block scoring if a required identity/hash/evidence check fails.
- Both modes use the original PDF to interpret `R`, validate generated claims, and investigate source anomalies. Generated claims never decide what belongs in `R` or `N`.

## 3. Atomic universes and semantic alignment

### 3.1 PDF-positive normative requirement inventory `R`

In benchmark-construction mode, extract each smallest *independently meaningful and testable* normative PDF proposition as `PDF-00001`, etc.; in frozen mode, use the same atomization rubric only for read-only evidence and reference-exception checks. Preserve the exact English quote, physical page and section/table/figure locator, actor, target, required action or prohibition, scope, precondition, exception, applicable version, timing, modality, and outcome.

A negative obligation in the PDF, such as "do not publish a high-risk draft without required approval," is a **source-positive** obligation to enforce that prohibition. The prohibited counterfactual may separately qualify as a fixed negative control under §3.3, but the two have different logical polarity and IDs.

**Normalize repeated general requirements as follows:**

- A rule explicitly covering **all protected public endpoints** is one universally scoped source proposition, not an arbitrary copy for every path.
- Create separate endpoint atoms when the PDF supplies **distinct method/path, actor, input, success code, validation timing, exception, or outcome requirements** that can be tested independently.
- An exact database field can have separate testable type, nullability, key, default, and relationship constraints, but do not invent unsupported physical constraints or split meaningless fragments.
- A chapter's repeated interface boilerplate is not automatically a separate normative requirement for every subsection merely because it is printed repeatedly. Retain location references for repeated evidence.
- If a parent is only a summary of individually scored child obligations, retain the parent as context rather than scoring both parent and children.
- Verify that splitting and merging preserve the logical force of the original (especially "all", "only", "unless", "before", and "never").

Exclude headings, narrative background with no normative force, illustrative-only fixtures, example configuration not adopted as policy, unsupported proposed alternatives, and purely deferred capabilities from `R`. Record them as exclusions or negative-control evidence where appropriate. Do not reuse a historical source-atom total as a required denominator.

**Source counts must reflect meaningful independent obligations—not repeated prose frequency.** The same `R` inventory is used for all methods. In benchmark-construction mode, source-atom corrections occur **before the Phase 01 freeze**; after that lock, corrections require a separate new benchmark version and re-evaluation of every method. In frozen mode, no source-atom correction is permitted during scoring: log any PDF contradiction or possible over-split as `REFERENCE_EXCEPTION`.

**Mandatory atomization challenge:** For every scored source proposition, check whether the quoted PDF actually commits to the normalized actor/target/action/scope/outcome. A field such as `title` in a case aggregate is evaluated in the inherited case-storage context; a standalone keyword is not an arbitrary global obligation. Compare semantically identical duties at other PDF locations and retain their additional locators rather than counting them again. A verification-matrix row that merely repeats an already scored implementation rule is supporting test evidence, **not automatically an additional positive requirement**. Retain a separate test obligation only when the PDF independently requires execution, preservation, or a distinct testable outcome not subsumed by the implementation duty. Before a newly constructed benchmark is locked, any source split/merge/removal needs PDF evidence, old/new IDs, and application to all methods. After lock (including a supplied frozen reference), never mutate `R`/`N` from evaluation results; report a benchmark-revision recommendation separately without scoring it.

### 3.2 Generated definitive occurrences `G_O` and semantic classes `G_C`

Inspect all eight supplied Markdown documents line by line and table cell by table cell. Extract the smallest independent **definitive implementation or design commitment**. Include positive duties, prohibitions, exact API methods/statuses, required fields, DDL constraints, access rights, time limits, exceptions, processing outcomes, and approved rules.

Assign occurrence IDs `GEN-00001`, etc., with actual file, physical line range, and table row/column/cell locator. State all normalized propositions in English. Preserve scope inherited from the heading, table header, row key, full row, and linked definition. A short cell such as `NOT NULL`, `201`, or `Owner` is **never** an independent GO: reconstruct the meaningful field/API/permission proposition first. Split a row only where each resulting assertion is independently testable **and complete**. Do not create extra GO for IDs, columns, cells, actor names, numbers, status codes, citations, or locators that are merely predicates of the same assertion.

Assign every eligible occurrence to exactly **one raw within-method semantic class** in `G_C`. Two occurrences share a class only if their target, actor, required operation, scope, conditions, exceptions, version, and outcome are substantively identical. Stylistic differences such as `must not` versus `must never` can be equivalent; differing API IDs, success codes, resource types, or authorization scopes cannot be merged just because their text is similar.

**Status and eligibility:** Explicitly unapproved `Proposal`, `Unadopted proposal`, `TBD`, `Needs confirmation`, open questions, and undecided alternatives are not final positive predictions. A definitive, separable subclaim inside a partially unresolved section remains eligible. Do not treat a citation, section heading, bare reference, or repeated test mapping without an independent assertion as an eligible occurrence. Record nondefinitive material at coherent text-range/row level with its location and reason, rather than issuing separate exclusions for each cell of the same row. Every exclusion must point either to a genuinely nondefinitive item or to an equivalent eligible assertion with its GO ID (when the row is used only as context).

### 3.3 Fixed bounded source-negative controls `N`

When creating a new benchmark, construct `N` **before** reviewing generated predictions, using a deterministic rule from the original PDF's explicit prohibitions, explicit exclusions/non-goals, and explicit release deferrals. When an `N` inventory is supplied and frozen, use it unchanged; do not construct new or altered controls during scoring. Each `NEG-00001` control is an atomic, affirmative-sounding counterfactual that the PDF specifically excludes, such as "Release R1 implements cross-region active/active mutation."

For a prohibited behavior, use no more than one distinct canonical counterfactual per independently prohibited capability. A blank TBD, an unsupported invented feature, or mere absence of a word does **not** prove a valid negative control. Include the original PDF quote, physical page, scope, and construction rationale. Keep `R ∩ N = ∅`.

`N` is a **bounded diagnostic test set**. Its TN count is not a population-wide total of all possible absent requirements; disclose its size and derivation. Its members must remain identical across evaluated methods.

### 3.4 Two evidence layers: raw classes and effective canonical predictions

Do not conflate **raw generated class counting** with **the source-proposition coverage projection**.

For each method `m`, define:

```text
R       = fixed, semantically normalized PDF-positive normative atoms
N       = fixed, semantically normalized PDF-negative counterfactual controls
G_m     = raw unique definitive generated semantic classes (G_C)
GO_m    = all eligible generated occurrences (G_O)

A_m     = {r in R : the eligible generated corpus logically entails all predicates of r}
B_m     = {n in N : the eligible generated corpus asserts or logically entails n}
F_m     = distinct generated-only unsupported/contradicted definitive propositions
          that the PDF does not normatively entail in full, after canonical merging;
          propositions already represented by B_m are excluded from F_m.

U_m     = R disjoint-union N disjoint-union F_m
P_m     = A_m union B_m union F_m
```

`A_m` is the **effective PDF-positive coverage set**, not the literal string intersection `R ∩ G_m`. One universal generated class can be an evidence bridge for multiple distinct PDF requirements without creating additional `GEN-*` occurrences, additional raw generated classes, or duplicate occurrences.

`F_m` is scored once per distinct **unsupported generated proposition**, not once for every PDF atom that it fails to match. If a generated claim contains both an explicitly supported narrower obligation and an unsupported extra permission/exception, the supported obligation may cover an `R` atom **only if fully entailed**, while the unsupported residual commitment is retained in `F_m`. Record the relationship; do not delete unsupported qualifiers to manufacture a full TP.

A generated statement fully supported by the PDF but too narrow to entail any frozen source atom must be recorded as `SUPPORTED_NONCOVERING` in the generated-validity ledger. It is not automatically FP or a new, method-specific source atom. If source extraction appears to have missed a normative PDF atom, in frozen mode record a `REFERENCE_EXCEPTION` and preserve `R`; propose a distinct future benchmark version to be re-applied to all methods. In construction mode fix it before Phase 01 freeze.

**The canonical scoring unit is a normalized proposition in `U_m`, not a raw sentence or an occurrence.** For each `r in R`, assign actual `1`, predicted `1` exactly when `r in A_m`. For each `n in N`, assign actual `0`, predicted `1` exactly when `n in B_m`. For each `f in F_m`, assign actual `0`, predicted `1`.

The raw class count `|G_m|` and canonical predicted-positive count `|P_m|` **may differ**. This is expected and is not a reconciliation failure. Do not force them to equal by discarding universal-rule coverage, copying generated occurrences, or counting unsupported matches twice.

### 3.5 Mandatory semantic applicability and entailment rubric

Before deciding whether a source-positive atom is covered:

1. **Direct equivalent:** Check exact requirements and meaning-preserving paraphrases, including reordered clauses, capitalization, synonyms, and alternate Markdown/API representations.
2. **Explicit universal rule:** Check whether a generated statement applies to `all`, `every`, or an unambiguously defined class of operations/resources. Identify the particular source endpoint, field, actor, or workflow as a member of that class. Verify no exception removes it.
3. **Inherited context:** Include genuine document/section/table/header/row context; do not treat a lone short cell or bare identifier as an independent unsupported claim.
4. **Cross-section/cross-file conjunction:** Combine separately definitive generated claims only when their conjunction explicitly supplies all necessary predicates. Cite each actual source location and explain the bridge. Unstated architecture assumptions are not bridges.
5. **Full-predicate test:** Verify actor, target, action/modality, scope, preconditions, exception, timing, version, limit, and outcome as applicable. The generated evidence must entail the **whole** source atom; topical similarity or a related guard is insufficient.
6. **Polarity and absence:** Preserve `must` versus `may`, `only if` versus `if`, approval versus publication, acceptance versus completion, `before` versus eventual, and denial versus ordinary error.
7. **Generated correctness, separately:** Evaluate each definitive generated class against what the original PDF normatively supports. Universal coverage is not permission to make a broader unsupported claim.

**Coverage bridge record:** For every non-direct TP, record `coverage_mode` (`UNIVERSAL_INSTANTIATION`, `INHERITED_CONTEXT`, `CONJUNCTIVE_BRIDGE`, or `SEMANTIC_EQUIVALENCE`), full generated evidence locators, PDF requirement locator, `scope_membership_proof_en`, `predicate_check_en`, and any exclusions checked. A generic sentence alone is not a sufficient proof. For **every** TP, direct or bridged, record a source-predicate-by-predicate check (target, action, actor, condition, scope, timing, constraint, exception, outcome, and version wherever applicable). If a predicate is absent or contradicted, downgrade the result; do not use an identifier coincidence as proof.

**Table and acceptance-row normalization:** Reconstruct a meaningful proposition by combining table title, column heading, row label and cell. For a requirements-vs-tests comparison, compare the test's trigger, action, state change and expected outcome against the generated corpus; optional test IDs and paraphrased phrases do not need literal equality to demonstrate an otherwise complete obligation. Conversely, a generated statement about a similar test is not sufficient if it omits the substantive expected outcome.

**Illustrations (not pre-judged findings):**

| PDF requirement | Generated evidence | Decision rule |
|---|---|---|
| A specified case-creation endpoint requires a creation idempotency key. | "Every public long-running POST creation requires `Idempotency-Key`." | TP if the endpoint is explicitly within that class and all stated conditions match. |
| A case table requires `UNIQUE (tenant_id, id)`. | The same DDL constraint is stated in a field/table summary. | TP; prose-versus-DDL formatting does not matter. |
| Availability objective is 99.9% monthly. | `99.9% monthly` appears as a definitive objective. | TP if scope and measurement modality match. |
| A specific endpoint must validate **before allocating a job** and return a particular error code. | "All requests are validated." | Not a full TP unless timing and required error behavior are supported elsewhere. |
| A model may use only an approved equal-or-stronger fallback. | "Any fallback provider is allowed." | FP for the unsupported permission; it cannot establish the constrained source requirement. |

**Anti-inflation rule:** A common generated rule may project onto several distinct source-positive atoms only when the PDF's source atoms actually are independently testable obligations. It must not create extra source atoms or generated occurrences.

### 3.6 Mandatory bidirectional retrieval and false-negative challenge

Before a PDF-positive atom is finalized as FN, carry out **both** source-to-generated and generated-to-source candidate retrieval over the full eight-file corpus. Similarity-only top-k retrieval is insufficient: use deterministic exact indexes alongside semantic search, and do not cap retrieval in a way that silently drops a discovered exact structural match.

1. **PDF-to-generated keys:** Search the original PDF atom's exact target, normalized actor/action/outcome, API method and path, literal error/status, event name, data entity/field, rule ID, and test scenario. Preserve original spellings and ordinary aliases (e.g., `Case`/`cases`, `case title`/`title`, `workspace settings`/`retention class`, `identical response`/`original outcome`). Never assume an illustrative identifier must match for the behavior to be covered.
2. **Generated-to-PDF reverse links:** For each source atom classified as a provisional FN, inspect the generated classes and occurrences that mention the same target, endpoint, field, test condition, or shared rule. Revisit class membership and definitive-eligibility when an apparently complete commitment was previously ignored or excluded. This is a retrieval audit, not permission to promote unadopted proposals.
3. **Reconstruct table meaning:** Read the original Markdown table heading, column header, row key and full relevant cells, including cells elsewhere in the same row. Check references to earlier definitions and general requirements in other files. A short field, `201` status, or test expectation may be fully specified only through its inherited table context.
4. **Recheck semantic alternatives:** Test direct equivalence, synonyms, universal instantiation with explicit scope membership, inherited context and multi-file conjunction. Compare every relevant PDF predicate; reject merely topical coverage and document any missing predicate precisely.
5. **Adversarial FN challenge:** For every provisional `E1` and `E0` FN, actively attempt to prove it covered, using the strongest *actual* counterexample from the supplied corpus rather than accepting the prior matcher output. Preserve the best candidate quotation and the exact reason it fails, if it fails. A boolean flag such as `direct_equivalence_checked: true` or a search hit count alone is **not** proof that the candidate was inspected or rejected.
6. **Correct decisive errors immediately:** If the purported FN is completely entailed, change it to TP and provide direct/E2 evidence in the designated adjudication phase. If a source atom appears duplicated, nonnormative, or improperly split, verify the problem against the PDF. In construction mode repair it before Phase 01 locking; in frozen mode record `REFERENCE_EXCEPTION` for subsequent benchmark governance without altering the current denominator. Do not use a known missed generated match to inflate FN merely to satisfy a timetable.

**Diagnostic regression probes (not predefined TP labels):** Exercise searches for a case title field; workspace retention-class settings; and the idempotent repeated case-creation scenario yielding one case and an identical outcome. These are examples of *retrieval failure modes* seen in a prior evaluation, not a goldset, not fixed source-atom IDs, and not permission to label any current source or generated claim without re-reading the actual files. Include additional probes drawn from this run's own PDF and generated tables. If the input corpus changes, derive probes from the new inputs instead of relying on historical IDs.

**Required provisional-FN root-cause disposition:** Every source-positive candidate found by initial matching to be uncovered must receive exactly one final outcome, with real locators:

| `fn_review_disposition` | Meaning | Final handling |
|---|---|---|
| `MATCHER_FALSE_NEGATIVE_CORRECTED` | The generated corpus fully entails the source atom; the initial retrieval or semantic matcher missed it. | Change to TP; preserve proof and correction history. |
| `TRUE_MISSING` | No eligible definitive generated commitment covers the source duty after bidirectional and applicability checks. | FN; retain searches and nearest actual candidates. |
| `PARTIAL_ENTAILMENT` | Related definitive text exists but a specifically identified required predicate remains absent or contradicted. | FN; cite the strongest partial text and unmet predicate. |
| `CONSERVATIVE_UNRESOLVED` | Evidence is accessible but semantic ambiguity persists after bounded review; no full proof exists. | FN with `BEST_EFFORT_CONSERVATIVE` and explicit uncertainty; not a verified absence claim. |

Only `TRUE_MISSING`, `PARTIAL_ENTAILMENT`, and `CONSERVATIVE_UNRESOLVED` remain final FN. Possible frozen source-atom defects carry a **separate** `REFERENCE_EXCEPTION` flag and an ordinary defensible TP/FN judgment; they never replace a FN root-cause outcome or silently reduce the denominator. Distinguish a **verified absence within the scored corpus**, a **partial specification**, and an **unresolved semantic match** in the report; they must not be presented as the same kind of confirmed omission. Maintain one stable current version of the source, bridge and judgment ledgers after corrections.

### 3.7 Reciprocal generated-claim and TP proof audit

- A generated class lacking a matched source atom is **not inherently unsupported**. Search the PDF by generated target/operation, exact field and method/path, context, exceptions and semantic equivalents. `SUPPORTED_NONCOVERING` requires an affirmative, cited PDF entailment; it is not an unlabeled default for all otherwise unused generated classes.
- Before marking a generated claim `PDF_UNSUPPORTED`, check whether it is a restatement of an independently sourced acceptance case or a narrower supported subclaim. Score only the truly unsupported material; do not count the same underlying generated proposition once as an unsupported class and again as an asserted negative control.
- Re-evaluate each TP with the original PDF and actual generated quotations side by side. For E2 bridges, explicitly demonstrate class membership, predicate completeness, conjunction scope and absence of conflicting exceptions. Do not infer a condition simply because the generated text mentions the right identifier.
- Flag direct identifier/field/path exact hits classified as FN, and generated classes marked unsupported despite a complete source equivalent, as **mandatory semantic review exceptions**. Resolve clear errors within the designated adjudication phase. Remaining material uncertainty stays `BEST_EFFORT`, not `VERIFIED`.

### 3.8 Efficient indexing, audit scope, and exclusion safeguards

1. Parse the PDF and eight original Markdown inputs once per run; index PDF physical pages, headings, table rows/cells, literal IDs, method/path pairs, actors, events, constraints, numerals, polarity, and inherited context. Retain original line and physical-page evidence.
2. Maintain both an eligible GO/GC index **and the full original-text index including excluded and contextual segments**. Discovery may use deterministic lookup plus optional semantic ranking; retrieval similarity, a hit count, or a top-k cutoff must never decide entailment or PDF support.
3. Cache checked aliases, source locators, family/universal proofs, and supported predicate scopes. Reuse a proof only after verifying each target's specific conditions and exceptions. Search receipts may be concise but must identify checked real passages and relevant failed alternatives.
4. Phase 02 must reconcile every substantive Markdown heading, paragraph, list item, and table row to eligible GO, exclusion, or inherited-context records. Phase 05 must also re-examine **all substantive excluded text** for any affirmative definitive assertion, even when it matches no R atom, to prevent hidden generated-only FP omissions. A table row is not automatically one requirement, but atomization cannot treat its isolated cells as standalone claims. Report suspiciously large per-row fragment counts and inspect them, **without** imposing an arbitrary GO-to-line numerical limit.
5. Explicitly distinguish `EXPECTED_REUSE` (identical claim legitimately serving an independent specification role) from `REDUNDANT_DUPLICATE` (unneeded repetition). Both are excess GO occurrences for the v6.1 duplication rate. Preserve all representative and nonrepresentative locators.
6. Phase 04 reviews every provisional FN and TP; Phase 05 evaluates every effective GC **and every substantive excluded range for missed definitive predictions**; Phase 06 every unsupported residual and N. Additional bounded deep audits never replace these complete population checks: Phase 04 up to **120 risk-ranked plus 40 reproducibly stratified** FN groups; Phase 07 up to **80 risk-ranked plus 20 reproducibly sampled** canonical groups. If fewer are eligible, review all. These budgets are fixed, not adapted to observed score quality. Correct any clear defect outside the budgets when discovered.
7. All phase outputs are immutable once delivered. Later findings use explicit linked overlays (`CHANGE`, `RECOVERED_OCCURRENCE`, `RECOVERED_CLASS`, `REFERENCE_EXCEPTION`) and final effective-state reconstruction. Never silently rewrite earlier files or change frozen reference bytes.

## 4. Four-cell definitions, equations, and evidence grading

Use a **single canonical binary universe per method**. Every unit receives one actual label, one predicted label, and one of the four cells:

| Cell | Actual | Predicted | Meaning |
|---|---:|---:|---|
| `TP` | 1 | 1 | A PDF-positive atom is fully entailed by eligible generated commitments, including an evidenced universal/shared rule. |
| `FN` | 1 | 0 | A PDF-positive atom is not fully entailed after direct, universal, contextual, and conjunctive checks. |
| `FP` | 0 | 1 | A distinct unsupported generated proposition or an asserted PDF-negative control. |
| `TN` | 0 | 0 | A predeclared bounded PDF-negative control is not asserted or entailed by the generated corpus. |

### 4.1 Corrected four-cell equations

```text
TP = |A_m|
FN = |R| - |A_m|
TN = |N| - |B_m|
FP = |F_m| + |B_m|

|U_m| = |R| + |N| + |F_m|
|P_m| = TP + FP = |A_m| + |B_m| + |F_m|

TP + FN = |R|
TN + |B_m| = |N|
FP - |B_m| = |F_m|
TP + TN + FP + FN = |U_m|
TP + FP = |P_m|           NOT necessarily |G_m|

Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 * TP / (2 * TP + FP + FN)

Duplicate = (|GO_m| - |G_m|) / |GO_m|
```

Compute division-by-zero cases explicitly: a zero denominator gives JSON `null` for Precision, Recall, or Duplicate; F1 is `0` if its standard denominator is positive while TP is zero, otherwise `null`.

**Critical correction from v5.1:** Do not use the raw-class identity `TP + FP = |G_C|` after implementing one-to-many universal-rule coverage. That identity is valid only for a universe where predictions are exactly the raw generated classes, which would not correctly measure source-atom coverage under logically applicable shared commitments. `Precision`, `Recall`, and `F1` here are conventional binary rates **over the effective canonical proposition universe `U_m`**, not raw class-level prediction accuracy. Report this distinction plainly.

`TN` refers only to the fixed negative-control inventory. Adding more unasserted negative controls may increase TN but cannot increase Precision, Recall, or F1.

Never combine source-side TP with raw-class FP from different denominators; all four numbers must be reproducible by enumerating the rows of `U_m`. Never double-count an asserted `NEG-*` proposition in both `B_m` and `F_m`.

### 4.2 Entailment grades and bounded decision policy

| Grade | Evidence standard | Binary result |
|---|---|---|
| `E3` | Direct, complete semantic match with original-file evidence. | Fully entailed. |
| `E2` | Complete logical entailment through an explicitly verified universal-scope, contextual, or conjunctive bridge. | Fully entailed. |
| `E1` | Relevant overlap, but a material actor, condition, scope, exception, timing, or outcome is not established. | Not fully entailed. |
| `E0` | Contradiction, or no defensible entailment following the prescribed alternatives check. | Not entailed. |

`E2` is a **full TP-grade match** when the complete logical bridge is demonstrated; it is not a penalty grade. This is the key correction: an API-wide policy can satisfy endpoint-specific duties when the policy demonstrably applies to those endpoints and contains the complete duty.

For an FN, `E1` or `E0` describes **generated coverage** against a source-positive atom. For an FP, it describes **PDF support** for a generated claim. Do not swap these directions silently. Negative-control evidence must show an explicit PDF prohibition/deferral and a genuine generated assertion (or nonassertion).

**Bounded adjudication:** For ordinary semantic ambiguity, attempt (i) direct match, (ii) universal applicability, (iii) section/table context, (iv) multi-file conjunction, (v) contrary evidence, and (vi) the reciprocal full-corpus FN challenge in §3.6. If complete entailment remains unproved after actual candidate inspection, record `E1`, the strongest candidate's real locator, a specific unmet predicate, the checked alternatives and a conservative binary judgment. Move on. Do not reopen the phase or produce an endless "needs more analysis" cycle. Mark such decisions `BEST_EFFORT_CONSERVATIVE` and report their count in coverage limitations. **Known explicit matches, uninspected close candidates, or malformed atomization are actionable defects, not ordinary E1 ambiguity; fix them within its designated phase.**

**Never** use this fallback for an unreadable PDF page, missing scored Markdown file, corrupted artifact, or fabricated quotation. Those are genuine evidence-access blockers, not ordinary E0/E1 cases. Do not state that a machine check of identifiers proves manual semantic completeness.

### 4.3 Independent generated-claim validity

For every raw generated semantic class `g`, record one of:

- `PDF_ENTAILED`: the complete generated commitment is supported by the PDF, with direct or bridge evidence.
- `PDF_UNSUPPORTED`: the generated commitment has unsupported or contradictory material predicates; map its distinct unsupported canonical proposition to `F_m`, except where it already equals an asserted `N` control.
- `SUPPORTED_NONCOVERING`: the PDF supports a narrower generated commitment that does not entail any independently retained atom in frozen `R`; explain why it does not create a method-specific new PDF atom.

A raw claim can appear in several **source-atom coverage bridges** without being duplicated in the occurrence/class inventory. Source coverage and generated correctness must remain separate evidence directions even though they feed the same canonical binary ledger.

No class may be labeled `PDF_ENTAILED` or `SUPPORTED_NONCOVERING` solely because it is topically related to a PDF section. Preserve positive PDF quotation evidence and the complete generated predicate. `SUPPORTED_NONCOVERING` records must state *why* the correctly supported generated subclaim does not cover a frozen independent `R` atom. A high volume of such records is a mandatory source-atomization and candidate-match review signal, not proof by itself of a bad score.

### 4.4 Recall reliability and root-cause reporting

The computed `Recall = TP / |R|` is an arithmetic statistic over the **current adjudicated** source inventory. It is not automatically a certified measure of actual design-specification coverage. A poor matcher can manufacture FN; an over-split or duplicated `R` can distort the denominator; a permissive bridge can manufacture TP. Audit all three before interpreting the figure.

Report in `08_coverage_and_limitations.md` (a) final `TRUE_MISSING`, `PARTIAL_ENTAILMENT` and `CONSERVATIVE_UNRESOLVED` counts, (b) corrected false negatives and frozen reference exceptions or pre-freeze source-atomization changes with links to `07_change_delta.jsonl`, (c) the number of TP records with complete reviewed proof, (d) unsupported and supported-noncovering generated-class evidence gaps, and (e) any unresolved high-risk direct-match exceptions. Distinguish **structural reconciliation** from **semantic evidence certification** in every summary. An arithmetic pass does not upgrade `FINAL_BEST_EFFORT` to `FINAL_VERIFIED`.

Do not present conservative FN as verified absence, and do not assert that an earlier low Recall is a measurement of true missing requirements. If the evidence cannot support a reliable point estimate, show the calculated provisional result with explicit uncertainty and the types/counts of judgments likely to change. Do not invent an error interval or claim the provisional result is necessarily a statistical lower bound; both FN and TP and source-denominator defects can change it in either direction.

## 5. Semantic duplication

Every eligible generated occurrence belongs to exactly one same-method raw semantic class. Compare normalized full predicates, not only stripped text.

```text
eligible_generated_occurrences  = |GO_m|
unique_generated_claim_classes = |G_m|
duplicate_excess_occurrences    = |GO_m| - |G_m|
duplicate_rate                  = (|GO_m| - |G_m|) / |GO_m|
repeated_claim_class_count      = number of G_m classes with >= 2 occurrences
```

Count only independently eligible, **complete** substantive assertions. Do not count bare references, citations, test IDs, headings, actors, isolated statuses, numbers, or unadopted options as claim repetitions. Treat repeated table mappings as contextual references unless they independently assert an actionable proposition. Scope-changing changes are not duplicates: `API-001` and `API-002` should not merge merely because their wording matches.

For a reproducible **within-file versus across-file partition**, sort each class's eligible occurrences by input-file order, physical line, and table-cell position, then select the earliest as the representative. Classify each subsequent excess occurrence as `within_file` if an earlier occurrence of that class is in the same file; otherwise classify it as `across_file`. The partition must satisfy:

```text
within_file_excess + across_file_excess = duplicate_excess_occurrences
```

Report separately how many repeated classes span multiple files; that descriptive class count can overlap the within-file classification. `Duplicate` is calculated from **raw occurrences and raw classes**, never from `A_m`, `P_m`, or expanded coverage bridges. If `|GO_m|=0`, return `null`.

## 6. Eight phase-complete execution turns

**One operator request to proceed authorizes exactly the next phase.** A phase completes its entire required population in that response; no unfinished phase may be treated as complete and no later phase may begin early. Use as many internal tool calls as needed. Distinguish a genuine file/platform blocker (checkpoint `INCOMPLETE`) from resolvable semantic ambiguity (`BEST_EFFORT`).

| Phase | Work package | Required phase outputs | Gate to next phase |
|---|---|---|---|
| **01 — Source Inventory and Reference Lock** | Resolve all inputs; validate original PDF identity, 90 physical pages, readability, and relevant figure/table evidence. If frozen `R`/`N` and manifest are supplied, validate all applicable SHA-256 digests, ID uniqueness, evidence and declared limitations; **do not change their bytes**. Otherwise use v6.1 §§3.1/3.3 to extract, deduplicate and freeze source `R` and `N` independently before generated inspection. | `01_reference_lock.json`; in construction mode also `01_source_atoms_final.jsonl`, `01_source_negative_controls_final.jsonl`; reference exceptions/atomization findings within the lock | Same finalized `R`/`N` for every method; no missing/hash-mismatched required source; source inventory fixed |
| **02 — Generated Extraction and Raw Semantic Classes** | Inspect all eight original Markdown files, including coherent table rows/cells. Extract complete, definitive `GO`; classify contextual/nondefinitive exclusions with real locators; immediately form v6.1 semantic `GC` classes and label excess instances. No free-floating status, actor, path, number, or metadata GO. Index full original and excluded text. | `02_generated_atoms_final.jsonl`, `02_generated_classes_final.jsonl`, `02_excluded_units.jsonl`, `02_duplicate_classes.jsonl` | All substantive sections/rows accounted for; each GO complete and assigned to one GC; class/duplicate counts reconcile; suspicious row fragmentation inspected |
| **03 — Source Coverage Initial Pass** | For **every R**, reconstruct full predicates, search generated GO/GC and original text across all eight files, and record strongest actual evidence (including inherited/universal/conjunctive applicability) or closest candidate with missing predicates. Identify exact-source proof absent from GO as an extraction-gap candidate. Mark decisions provisional. | `03_source_coverage.jsonl`, `03_semantic_coverage_bridges.jsonl` | Exactly one evidenced provisional source judgment per R; every plausible gap recorded; no similarity-only verdict |
| **04 — Reciprocal FN Challenge and Complete TP Audit** | Challenge **every** provisional FN via direct, alias, universal, contextual, reverse, and conjunctive searches. Verify **every** provisional TP predicate-by-predicate against original source and generated passages; correct clear misses and recover extraction gaps through immutable overlays. Apply extra fixed 120+40 FN-group deep audit without replacing individual checks. | `04_fn_root_cause_audit.jsonl`, `04_tp_evidence_audit.jsonl`, `04_coverage_changes.jsonl` | Each provisional FN has one root-cause outcome; each provisional/final TP has a reviewed proof; every gap is resolved or documented; effective TP/FN population reconciles |
| **05 — PDF Support and Exclusion Recovery** | Re-examine **every substantive Phase 02 exclusion** for missed definitive assertions, including unmatched-to-R claims; recover them via immutable GO/GC overlays and evaluate all resulting effective GC. Then assess **every effective GC** against the original PDF regardless of R coverage; record full support, supported-noncovering claims, and exact unsupported/contradicted residual predicates. A missing R match is never FP proof. | `05_generated_claim_validity.jsonl`, `05_exclusion_reassessment.jsonl` | Every substantive exclusion has eligibility disposition, every effective GC has one PDF decision, and every unsupported residual traces to real GO/GC and PDF checks |
| **06 — FP Canonicalization and Negative Controls** | Merge semantically equivalent unsupported residuals across all eight files only on full mutual entailment. Make a targeted second cross-cluster over-merge/under-merge check. Adjudicate **every frozen N**, crosswalk asserted controls against residuals, and eliminate control/FP double counting. | `06_fp_controls.jsonl` | All residuals and N controls accounted for; one independent FP cluster per distinct unsupported-only proposition; no overlap with asserted N |
| **07 — Quality Audit and Final Canonical Universe** | Reconcile all Phase 04–06 evidence; deep-audit up to fixed 80 risk + 20 reproducible canonical groups. Correct discovered GO/GC/TP/FN/FP/control errors only through linked `CHANGE` records; provide a new reviewed `TP_AUDIT` overlay for each newly established TP; annotate source reference exceptions but never mutate locked `R`/`N`. Produce exactly one effective canonical decision for each unit in `U_m = R ⊎ N ⊎ F_m`; audit duplicates and all correction dependencies. | `07_final_ledger.jsonl`, `07_change_delta.jsonl`, `07_duplicate_metrics.json` | Every R, N, effective GC, recovered exclusion and residual reconciled; all prior changes applied; complete canonical four-cell universe and duplicate partition |
| **08 — Independent Metrics and Delivery** | Compute final values **from Phase 07 item-level records**, verify reference/input digests again, exact coverage/validity counts, occurrence-class mappings, FP-N nonoverlap, proofs, equations, confidence, audit budgets, and method comparability. No manually invented totals; clearly disclose provisional semantic limits. | `compute_metrics.py`, `08_metrics.json`, `08_report.md`, `08_coverage_and_limitations.md`; comparison files only if multiple methods | Recomputed TP/TN/FP/FN/Precision/Recall/F1 and duplication metrics are internally consistent, with accurate verification status |

For every phase, include a compact `PHASE_SUMMARY` record in its principal JSONL artifact, or an equivalent summary object in the phase's principal JSON file: counts, complete/incomplete status, confidence distribution, remaining uncertainties, and exact input references. Summary records are **not** GO, GC, R, N, FP, or canonical scoring units. Preserve earlier phase outputs immutably; overlays and final effective-state reconstruction are mandatory.

**Reference to v6.1's two independent evidence directions:** Phase 03–04 decide `R -> generated` coverage; Phase 05–06 decide `generated -> PDF` validity. Never confuse raw GC count with canonical predicted-positive count, and never classify a supported but noncovering GC as FP.

### Mandatory completion and audit discipline

- Semantic uncertainty with accessible evidence receives a defensible binary decision, basis (`DIRECT`, `CONTEXTUAL`, or `BEST_EFFORT`), confidence (`HIGH`, `MEDIUM`, or `LOW`), and actual evidence/alternative-search receipt. No threshold by itself proves entailment or absence.
- A true file/PDF/reference identity blocker yields an `INCOMPLETE` or `BLOCKED_REFERENCE` checkpoint; do not falsely complete the phase. An incomplete result cannot authorize the next phase.
- An extracted definitive claim omitted from GO, even within an `EXCLUSION` range, must be recovered or documented as a known defect—not silently ignored. An excluded row/paragraph is searched when judging FN and FP.
- Do not run a subsequent phase to improve earlier work until the currently requested phase is actually complete. Once complete, corrections made later follow explicit overlays, not silent overwrites.
- Do not describe bounded self-audit as independent model/expert review. A `VERIFIED` structural check does not certify semantic completeness.

## 7. Required individual artifacts and record contract

For one method, keep outputs in one directory. For multiple methods, share one frozen `R`/`N` reference and isolate method-specific artifacts in separate method directories. Output content must be English. Retain the actual original filenames/line numbers in locators. Avoid archives unless requested.

| File | Content |
|---|---|
| `01_reference_lock.json` | Input identities/digests, PDF pages, source/reference mode, immutable R/N IDs, known benchmark limitations, and reference exceptions |
| `01_source_atoms_final.jsonl`, `01_source_negative_controls_final.jsonl` | **Construction mode only**: newly extracted PDF-positive and bounded negative reference; locked before generated inspection |
| `02_generated_atoms_final.jsonl` | Complete, eligible GO; original file/line/table scope; normalized full propositions |
| `02_generated_classes_final.jsonl` | Effective initial GC groups with member GO IDs and mutual-entailment proof |
| `02_excluded_units.jsonl` | Contextual/nondefinitive coherent ranges, classification reasons, inherited-assertion links where applicable |
| `02_duplicate_classes.jsonl` | Excess GO by GC; `EXPECTED_REUSE` versus `REDUNDANT_DUPLICATE` and within/across-file locators |
| `03_source_coverage.jsonl` | One provisional result per R, strongest evidence or missing predicates, extraction-gap flags |
| `03_semantic_coverage_bridges.jsonl` | Direct and E2 universal/contextual/conjunctive proof locators and scope validation |
| `04_fn_root_cause_audit.jsonl` | Every provisional FN with bidirectional search, strongest candidate, unmet predicates, disposition and evidence |
| `04_tp_evidence_audit.jsonl` | Every provisional TP and every effective final TP with complete predicate checks; correction links |
| `04_coverage_changes.jsonl` | FN-to-TP/TP-to-FN revisions and recovered occurrences/classes, with provenance; marker if none |
| `05_generated_claim_validity.jsonl` | One source-PDF support judgment per effective GC; supported noncovering or exact residuals |
| `05_exclusion_reassessment.jsonl` | One review per substantive Phase 02 excluded range, with any recovered definitive GO/GC IDs and original locators |
| `06_fp_controls.jsonl` | Every negative control judgment and every deduplicated, generated-only unsupported residual FP class, N crosswalk |
| `07_final_ledger.jsonl` | Exactly one `FINAL_SOURCE` per R, `FINAL_CLASS` per effective GC, `FINAL_CONTROL` per N, `FINAL_FP_CLUSTER` per generated-only FP, plus final canonical decisions and summary |
| `07_change_delta.jsonl` | Every later correction/overlay and its dependent-ID impact, or a no-change marker |
| `07_duplicate_metrics.json` | GO/GC counts, repeated-class counts, within-/across-file excess, expected reuse versus redundant duplicate, raw duplicate rate |
| `compute_metrics.py` | Independent parser and fail-fast structural/digest/evidence/count-equation validation; no hard-coded expected scores |
| `08_metrics.json` | Final TP, TN, FP, FN, Precision, Recall, F1, Duplicate and underlying population counts |
| `08_report.md` | Interpretation, sample scope, methods, outcomes, confidence, corrections, limitations, comparable counts |
| `08_coverage_and_limitations.md` | PDF/Markdown coverage, reference limitations, source atomization exceptions, FN root causes, TP evidence-audit, bounded negative controls, uncertainty |
| `08_comparison.json` and `08_comparison.md` | Only if two or more methods share identical frozen R/N, PDF and rules |

**Minimum evidence fields:** Each item-level JSONL row has `record_type`, stable real IDs, applicable physical PDF page or original Markdown file/line/table locator, normalized complete proposition, source/generated evidence, a short reproducible reason, decision basis and confidence when making a judgment, and links to applicable changes. `PHASE_SUMMARY` and no-change markers are excluded from count populations.

**Required types:** `OCCURRENCE`, `EXCLUSION`, `CLASS`, `DUPLICATE`, `SOURCE_JUDGMENT`, `COVERAGE_BRIDGE`, `FN_REASSESSMENT`, `TP_AUDIT`, `EXCLUSION_REASSESSMENT`, `RECOVERED_OCCURRENCE`, `RECOVERED_CLASS`, `PDF_JUDGMENT`, `FP_CLUSTER`, `NEGATIVE_CONTROL`, `CHANGE`, `REFERENCE_EXCEPTION`, `FINAL_SOURCE`, `FINAL_CLASS`, `FINAL_CONTROL`, `FINAL_FP_CLUSTER`, `CANONICAL_JUDGMENT`, `FINAL_SUMMARY`, `PHASE_SUMMARY`. Emit only the types applicable to the phase.

**Frozen ID mapping:** Preserve identifiers supplied in the actual files (e.g., `requirement_id` or `source_id` for R; `control_id` or `negative_control_id` for N). Normalize only an internal read-only key map; do not alter JSONL input, ID spelling, or statement text. Never claim a reference is fully semantically audited merely because its hashes/IDs pass.

## 8. Machine-readable schemas and invariants

### 8.1 Canonical positive judgment example (illustrative schema, not a finding)

```json
{
  "prefix": "onelevel",
  "canonical_id": "ATOM-00001",
  "atomic_statement_en": "A source-defined endpoint validates input before allocating an asynchronous operation.",
  "actual_label": 1,
  "predicted_label": 1,
  "scoring_cell": "TP",
  "origin_source_ids": ["PDF-00001"],
  "origin_generated_class_ids": ["GCLASS-00001"],
  "origin_negative_control_ids": [],
  "coverage_mode": "UNIVERSAL_INSTANTIATION",
  "pdf_evidence": [
    {
      "file": "OrionDesk_AI_Detailed_Design_Specification.pdf",
      "physical_page": 8,
      "quote_en": "Exact English evidence from the actual source is required."
    }
  ],
  "generated_evidence": [
    {
      "file": "onelevel_02_api.md",
      "line_start": 10,
      "line_end": 10,
      "table_cell": null,
      "translation_en": "Faithful English statement from the actual generated input is required."
    }
  ],
  "scope_membership_proof_en": "Explain why this endpoint belongs to the generated universal rule's declared scope.",
  "predicate_check_en": "Confirm that the rule includes required timing, action, condition, and outcome.",
  "entailment_grade": "E2",
  "adjudication_policy": "VERIFIED_BRIDGE",
  "specific_reason_en": "The cited universal statement entails the complete source atom."
}
```

The example strings and page/line values above are schema placeholders, **not verified quotations or claims about an actual file**. In executed ledgers, use genuine extracted English quotes and existing file paths, without copied placeholder language.

A `TN` record must reference a `NEG-*` ID and have no definitive generated evidence asserting the counterfactual. An asserted `NEG-*` control becomes one `FP` in that same negative-control row. An ordinary unsupported generated proposition also becomes one `FP`, but must reference its `GCLASS-*` evidence and a specific PDF non-entailment finding.

### 8.1a Required FN root-cause and TP-proof fields

In `04_fn_root_cause_audit.jsonl`, record one row for every source atom initially nominated as FN (including corrected cases): `source_id`, `initial_grade`, `initial_predicted_label`, `fn_review_disposition`, `final_source_id_or_replacement_ids`, `final_scoring_cell` (or `REMOVED_OR_MERGED`), `pdf_evidence`, `best_generated_candidates` with actual file/line/table-cell quotation, `exact_and_alias_keys_checked`, `universal_context_conjunction_checked`, `scope_membership_proof_en`, `met_predicates_en`, `unmet_predicates_en`, and `specific_reason_en`. Each final FN must be `TRUE_MISSING`, `PARTIAL_ENTAILMENT`, or `CONSERVATIVE_UNRESOLVED`; a source-atomization concern is recorded separately as a reference exception, not as a silent deletion of a frozen R item. Do not claim to have searched the complete corpus based solely on a generic true/false flag; retain enough actual candidate/search evidence to reproduce the conclusion.

In `04_tp_evidence_audit.jsonl`, record one row for each **initial TP candidate**, preserving corrected-to-FN cases: `source_id`, `entailment_grade`, `coverage_mode`, actual `pdf_evidence`, real `generated_evidence` locators, a full predicate-check map with `met`/`not_applicable` and explanatory proof, `scope_membership_proof_en` for universal bridges, `contrary_evidence_checked_en`, and `audit_outcome` (`CONFIRMED_TP` or `CORRECTED_TO_FN`). A TP that is downgraded must be reflected in the canonical judgment ledger and change delta. Each **final** TP must have exactly one effective audited proof record with `CONFIRMED_TP` in Phase 04 or a linked Phase 07 audit overlay; any `CORRECTED_TO_FN` audit must reference a final FN or a frozen reference exception (without modifying R). Counts alone are not evidence.

Within `01_reference_lock.json` in construction mode, document each PDF source split/merge/dedup decision before freezing R/N. In frozen mode, record each apparent source duplicate, parent-child overlap, or test-overlap defect as a `REFERENCE_EXCEPTION` without changing `R` or the scores' denominator. Phase 07 includes all resulting reference exceptions in its final limitations.

The example fields above specify **reporting obligations**, not benchmark answers or preapproved atom IDs. These new audit files are not scored source documents and must never be used to create requirements independently of the original PDF.

### 8.2 Required final summary shape (schema only)

```json
{
  "prefix": "onelevel",
  "status": "FINAL_VERIFIED",
  "universe": {
    "source_positive_atoms": 0,
    "source_negative_controls": 0,
    "raw_generated_claim_classes": 0,
    "generated_positive_occurrences": 0,
    "covered_source_atoms": 0,
    "asserted_negative_controls": 0,
    "unsupported_generated_only_propositions": 0,
    "canonical_predicted_positive_units": 0,
    "canonical_decision_units": 0,
    "negative_universe_scope": "PDF-grounded, predeclared bounded controls only"
  },
  "confusion": {
    "TP": 0,
    "TN": 0,
    "FP": 0,
    "FN": 0
  },
  "metrics": {
    "Precision": null,
    "Recall": null,
    "F1": null,
    "Duplicate": null
  },
  "metric_interpretation": "One canonical effective-proposition universe; raw generated classes are counted separately; TN is limited to fixed controls."
}
```

The zeroes and nulls in this block describe **schema types and empty example data only**. Replace all of them with actual recomputed values for a completed evaluation. Never report a dummy zero as an audited count. Use native JSON integer, number, or `null` types. If input evidence is unavailable, do not invent metric values; explicitly identify the blocker and use `null` where results cannot be computed.

### 8.3 Required independent recomputation and invariants

`compute_metrics.py` must read immutable Phase 01–07 files and actual frozen inputs, reconstruct overlays, and **fail** on any missing/duplicate/inconsistent population:

1. Read frozen `R`, `N`, all effective GO/GC, source judgments, FN reassessments, TP audits, PDF judgments, asserted controls and unsupported residual FP classes. Ignore `PHASE_SUMMARY` and audit markers when counting.
2. Verify identity and SHA-256 of every required input against the Phase 01 lock and `reference_freeze.json` where supplied; verify PDF physical page count and sample evidence locators against actual files; fail on changed frozen reference bytes.
3. Assert unique R/N IDs and source provenance; no R/N changes after lock; exactly one `FINAL_SOURCE` per R, one `FINAL_CONTROL` per N, and one `FINAL_CLASS` per effective GC, including recoveries. Each effective GO belongs to exactly one GC and each GC has a PDF validity decision.
4. Assert all substantive Phase 02 exclusions have a Phase 05 re-assessment, and every Phase 02–04 extraction-gap record is recovered or explicitly bounded with provenance; recovery classes and occurrences have original real locators. Source decisions are not based solely on lexical similarity.
5. Verify that each final TP has actual predicate-level proof and a corresponding audited TP record; each final FN has a reciprocal search disposition, real candidate/absence receipt, and `TRUE_MISSING`, `PARTIAL_ENTAILMENT`, or `CONSERVATIVE_UNRESOLVED`. Record but do not silently adjust frozen reference exceptions.
6. Assert all effective GC receive complete `PDF_ENTAILED`/`PDF_UNSUPPORTED`/`SUPPORTED_NONCOVERING` (or equivalent supported/unsupported with noncovering qualifier) with evidence; every unsupported residual maps to exactly one asserted N or unique generated-only FP cluster. Never count a residual in both.
7. Enumerate `U_m = R ⊎ N ⊎ F_m` with one actual/predicted binary label and one `TP`/`TN`/`FP`/`FN` per unit; assert `TP+FN=|R|`, `TN+|B_m|=|N|`, `FP=|F_m|+|B_m|`, `TP+TN+FP+FN=|U_m|`, and `TP+FP=|P_m|`. **Never** require `TP+FP=|GC|`.
8. Recompute Precision, Recall, F1 and raw Duplicate with documented zero denominators; verify `GO = GC + EXPECTED_REUSE + REDUNDANT_DUPLICATE`, `PDF_SUPPORTED_GC + PDF_UNSUPPORTED_GC = GC`, and within-file plus across-file excess equals `GO-GC`. Repeated GO do not increase TP/FP.
9. Check the exact fixed 120+40 and 80+20 deep-audit budgets used where eligible, sampling determinism, correction overlays, low-confidence totals and item-level completeness. Budgets do not excuse missing all-population checks.
10. Run reciprocal regression probes from actual filenames, source fields, endpoints, scenarios and rules present in this run (e.g., case title, workspace retention class and idempotent same-key case creation when present); flag obvious uncorrected direct matches and supported GC erroneously counted as FP.
11. Verify every report's English text, file existence, relative paths, original locator recoverability, full eight-document input identity and method separation. Cross-method results require identical SHA-256 of the frozen R/N/PDF and eligibility rules.
12. Fail `FINAL_VERIFIED` if any required population/evidence receipt is incomplete, direct-match error remains, source hash fails, or known reference anomaly is concealed. If all populations are enumerated but material semantic uncertainty remains, report an honestly qualified `FINAL_BEST_EFFORT`, not a fabricated certified score.

### 8.4 Cross-method fairness and interpretation

Use identical source-positive `R`, negative `N`, adjudication rubric, and applicability tests for `fullload`, `onelevel`, and `twolevel`. A generated universal statement may cover the same source atoms for any method if its scope proof is equally strong. Compare the resulting effective-proposition Precision, Recall, F1, and raw-class Duplicate. Report raw class count separately, not as the Precision denominator unless a separately labeled class-level metric is being computed.

Do not reinterpret these scores as verified implementation correctness, production safety, or actual application performance. They measure coverage and correctness of **generated specifications** against this specific fictional PDF baseline.

## 9. Completion gates, failures, and stop rule

A finished run has: all 90 PDF physical pages inspected or the supplied frozen reference verified against the PDF; eight Markdown files including substantive table context covered; stable R/N; all eligible GO assigned to GC and all substantive exclusions re-assessed; every R decided with full-predicate evidence; every provisional FN reciprocally challenged; every TP proof audited; every effective GC checked against PDF; every N and unsupported residual judged; a single canonical U and four-cell matrix; deduplicated FP/GO; fixed audit budgets documented; and independently recomputed metrics.

**Statuses:** `PHASE_COMPLETED_VERIFIED` (structural and required evidence gates met), `PHASE_COMPLETED_BEST_EFFORT` (complete population with explicitly bounded semantic ambiguity), `INCOMPLETE` (phase checkpoint awaiting missing required work), `BLOCKED_REFERENCE` (source/hash/identity blocker), `FINAL_VERIFIED` (all eight phases and audits complete without material known evidence defect), `FINAL_BEST_EFFORT` (all phases structurally complete with disclosed semantic doubt), `INVALID_REFERENCE_CHANGED` (a required frozen reference changed). A structurally verified calculation is not expert certification of semantic completeness.

Never convert an uninspected close candidate into a verified FN, an unchecked similarity hit into TP, a supported noncovering GC into FP, or an unadopted proposal into a scored assertion. A known explicit complete match left as FN is a defect requiring a correction record, not an ordinary best-effort ambiguity. A mandatory missing PDF/input/reference file is a blocker; do not invent metrics to meet the phase count.

**Final directive:** Retain v6.1's meaningful, context-restored source/generated atomization and complete semantic-entailment rubric. Integrate v9.0's frozen-reference discipline, immutable phase ledgers, comprehensive GC/PDF/FP residual accounting, bounded supplemental audits, and independent metric computation. Finish exactly the requested phase in each response; do not silently amend source benchmarks, inflate GO by splitting table cells, or suppress unsupported assertions as exclusions.
