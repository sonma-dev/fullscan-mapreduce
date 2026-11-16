# OrionDesk AI — Six-Turn Semantic-Entailment Atomic Requirement Evaluation Protocol

**Protocol version:** 6.1 (false-negative prevention, source-atomization audit, bidirectional entailment verification; retains one shared four-cell universe and eight scored Markdown inputs)  
**Primary objective:** Evaluate the implementation-relevant requirement coverage and correctness of AI-generated design specifications against the original English PDF, reporting **TP, TN, FP, FN, Precision, Recall, and F1** on one enumerated binary universe.  
**Secondary objective:** Quantify semantic duplication independently of semantic coverage.
**Evidence-quality objective:** Avoid treating an algorithmically computed Recall as certified coverage when explicit source-to-generated equivalences were missed or source requirements were over-split. Record corrected false-negative candidates and independently audit TP evidence before claiming semantic verification.  
**Supported generation methods:** `fullload`, `onelevel`, `twolevel`  
**Execution limit:** Exactly one completed phase per user request–response turn; at most six turns for the selected scope. Never repeat a phase merely to improve precision.  
**Conversation language:** Follow the user's requested conversation language.  
**All authored deliverable files and their content:** **English only.**  
**Archive policy:** Deliver individual files. Do not create ZIP, TAR, or other bundled archives.  
**This revision of the protocol is not an execution phase.**

## 1. Binding instructions and evaluation scope

The evaluation compares the original 90-physical-page English *OrionDesk AI Detailed Application Design Specification* with eight supplied Markdown specification documents per selected method. The authoritative PDF may use a timestamped or untimestamped filename. Verify its identity, 90-page extent, and readable content rather than trusting its filename.

The **sole authoritative source of normative requirements is the PDF**. Generated Markdown, aggregate JSON, prior goldsets, previous judgments, historical atom counts, and earlier scores cannot add PDF requirements or serve as evidence of their correctness. Inspect every physical PDF page, including diagrams, figures, tables, appendices, restrictions, exceptions, and captions, and inspect every substantive physical line and table cell of each scored Markdown document.

The evaluation's **primary matching rule is complete, justified semantic entailment**, not textual identity, one-to-one document-location identity, or syntactic similarity. A requirement may be satisfied by a generated universal/shared rule, a requirement stated elsewhere in the generated corpus, or a combination of explicit generated commitments, provided that the full target requirement—including relevant conditions, scope, actor, exception, timing, and outcome—follows logically from the cited statements.

**Important structural distinction:** A single generated class may cover several independently justified source-positive atoms, but that does not create extra generated occurrences or duplicate classes. Consequently, the positive-prediction count in the canonical decision universe is **not required to equal the number of raw generated semantic classes**. All four confusion cells must nevertheless be computed from the **same** explicitly enumerated decision universe.

### Non-negotiable rules

1. **Evidence before scores.** Support every source-positive atom with PDF evidence. Support every TP with generated evidence plus a complete logical applicability bridge. For FN, record a corpus-wide search and why plausible general rules fail or do not cover it. For FP, record the precise unentailed or contradicted generated commitment.
2. **No goldset leakage.** Extract PDF requirements independently. An aggregate JSON file may clarify status markers but may neither replace the PDF nor become a scored input.
3. **Meaningful atomicity; no artificial multiplication.** Split genuinely independently testable obligations, fields, constraints, actors, endpoints, conditions, exceptions, outcomes, and limits. Do **not** manufacture multiple identical source atoms by repeating a universal boilerplate requirement for every endpoint or every chapter when the PDF does not establish a distinct testable obligation. Likewise, do not discard unique endpoint-specific duties merely because a common rule exists.
4. **Semantic entailment before absence.** Before labeling any PDF atom FN, examine exact matches, synonyms, universal/shared constraints, inherited section/table context, and explicit multi-document bridges. Missing lexical overlap is not proof of a missing requirement.
5. **No unsupported TP inflation.** Merely mentioning the same API, field, actor, or topic is insufficient. Generic validation does not establish a specific response code, timing requirement, revision predicate, or exception policy unless those conditions are explicitly entailed.
6. **Stable comparisons.** Apply the same independently extracted PDF-positive inventory `R` and predeclared PDF-negative inventory `N` to every selected method. Generated occurrence, semantic-class, bridge, and judgment records remain method-specific.
7. **No fabricated evidence or scores.** Make an explicit, reproducible best-effort determination for normal semantic ambiguity. Missing, corrupted, or unreadable mandatory source material is a genuine input blocker; it must not be pretended to be an E0 finding or a fully audited score.
8. **One response, one complete phase.** Use as many internal tool calls as necessary within the current response. Finish the named phase with real English deliverables and a documented status. **Do not repeat the same phase on future turns** solely to pursue perfect disambiguation; close ordinary ambiguity using the bounded decision policy in §4.2. Never advance to the next phase before the current phase is closed.
9. **No administrative busywork.** Do not require run-ID registries, unrelated hash audits, administrative sign-off forms, frozen manifests, or archives. This does not eliminate substantive PDF requirements for product digests, audit proofs, or release signatures.
10. **Do not treat claims in unresolved registers as adopted decisions.** `Confirmed`, `TBD`, `Needs confirmation`, `Proposal`, `Unadopted proposal`, and `Resolved` are claim-status evidence, not substitutes for PDF verification or approval.
11. **Mandatory reciprocal FN challenge.** An automatic source-to-generated retrieval miss is a *candidate*, never sufficient evidence for an FN. Search all eight documents in both directions by exact identifiers, canonical targets, table context, meaning-preserving aliases, universal rules, and cross-file conjunction before finalizing the binary result. An explicitly located complete match must be corrected to TP in the current phase.
12. **Independent TP and atomization audit.** Review every TP for actual full-predicate entailment and check every source atom for artificial splitting, repeated universal boilerplate, and duplicate scoring of a verification scenario already represented by its substantive obligation. Structural arithmetic cannot certify these semantics.
13. **No silent quality claims.** A plausible-looking `BEST_EFFORT` confusion matrix is not verified requirement coverage. Report the categories and counts of remaining conservative judgments and any discovered but uncorrected evidence defects. Never describe a low Recall as confirmed missing requirements or a high Recall as confirmed completeness without the requisite evidence audit.

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

## 3. Atomic universes and semantic alignment

### 3.1 PDF-positive normative requirement inventory `R`

Extract each smallest *independently meaningful and testable* normative PDF proposition as `PDF-00001`, etc. Preserve the exact English quote, physical page and section/table/figure locator, actor, target, required action or prohibition, scope, precondition, exception, applicable version, timing, modality, and outcome.

A negative obligation in the PDF, such as "do not publish a high-risk draft without required approval," is a **source-positive** obligation to enforce that prohibition. The prohibited counterfactual may separately qualify as a fixed negative control under §3.3, but the two have different logical polarity and IDs.

**Normalize repeated general requirements as follows:**

- A rule explicitly covering **all protected public endpoints** is one universally scoped source proposition, not an arbitrary copy for every path.
- Create separate endpoint atoms when the PDF supplies **distinct method/path, actor, input, success code, validation timing, exception, or outcome requirements** that can be tested independently.
- An exact database field can have separate testable type, nullability, key, default, and relationship constraints, but do not invent unsupported physical constraints or split meaningless fragments.
- A chapter's repeated interface boilerplate is not automatically a separate normative requirement for every subsection merely because it is printed repeatedly. Retain location references for repeated evidence.
- If a parent is only a summary of individually scored child obligations, retain the parent as context rather than scoring both parent and children.
- Verify that splitting and merging preserve the logical force of the original (especially "all", "only", "unless", "before", and "never").

Exclude headings, narrative background with no normative force, illustrative-only fixtures, example configuration not adopted as policy, unsupported proposed alternatives, and purely deferred capabilities from `R`. Record them as exclusions or negative-control evidence where appropriate. Do not reuse a historical source-atom total as a required denominator.

**Source counts must reflect meaningful independent obligations—not repeated prose frequency.** The common `R` inventory is frozen across methods after source inspection and may be corrected with evidence during the designated correction phase without method-specific denominator manipulation.

**Mandatory atomization challenge:** For every scored source proposition, check whether the quoted PDF actually commits to the normalized actor/target/action/scope/outcome. A field such as `title` in a case aggregate is evaluated in the inherited case-storage context; a standalone keyword is not an arbitrary global obligation. Compare semantically identical duties at other PDF locations and retain their additional locators rather than counting them again. A verification-matrix row that merely repeats an already scored implementation rule is supporting test evidence, **not automatically an additional positive requirement**. Retain a separate test obligation only when the PDF independently requires execution, preservation, or a distinct testable outcome not subsumed by the implementation duty. If a source atom is split, merged, or removed, record the old/new IDs and rationale and apply the correction to every selected method without using method-specific evidence to set the common denominator.

### 3.2 Generated definitive occurrences `G_O` and semantic classes `G_C`

Inspect all eight supplied Markdown documents line by line and table cell by table cell. Extract the smallest independent **definitive implementation or design commitment**. Include positive duties, prohibitions, exact API methods/statuses, required fields, DDL constraints, access rights, time limits, exceptions, processing outcomes, and approved rules.

Assign occurrence IDs `GEN-00001`, etc., with actual file, physical line range, and table row/column/cell locator. State all normalized propositions in English. Preserve the scope inherited from the containing heading, table header, row key, and linked definition where unambiguous; a short cell such as `NOT NULL`, `201`, or `Owner` is not evaluated outside its field/API/permission context.

Assign every eligible occurrence to exactly **one raw within-method semantic class** in `G_C`. Two occurrences share a class only if their target, actor, required operation, scope, conditions, exceptions, version, and outcome are substantively identical. Stylistic differences such as `must not` versus `must never` can be equivalent; differing API IDs, success codes, resource types, or authorization scopes cannot be merged just because their text is similar.

**Status and eligibility:** Explicitly unapproved `Proposal`, `Unadopted proposal`, `TBD`, `Needs confirmation`, open questions, and undecided alternatives are not final positive predictions. A definitive, separable subclaim inside a partially unresolved section remains eligible. Do not treat a citation, section heading, bare reference, or repeated test mapping without an independent assertion as an eligible occurrence. Record excluded material with its location and reason.

### 3.3 Fixed bounded source-negative controls `N`

Construct `N` **before** reviewing generated predictions, using a deterministic rule from the original PDF's explicit prohibitions, explicit exclusions/non-goals, and explicit release deferrals. Each `NEG-00001` control is an atomic, affirmative-sounding counterfactual that the PDF specifically excludes, such as "Release R1 implements cross-region active/active mutation."

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

A generated statement fully supported by the PDF but too narrow to entail any frozen source atom must be recorded as `SUPPORTED_NONCOVERING` in the generated-validity ledger. It is not automatically FP or a new, method-specific source atom. If source extraction truly missed an independently normative PDF atom, correct `R` transparently **for all methods**, never just for the method benefiting from it.

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
6. **Correct decisive errors immediately:** If the purported FN is completely entailed, change it to TP and provide direct/E2 evidence in the current phase. If the atom itself duplicates an existing source rule, is only a nonnormative example, or has been split incorrectly, correct `R` across methods with an explicit source-atomization delta. Do not carry known errors into a `FINAL_BEST_EFFORT` result merely to satisfy a timetable.

**Diagnostic regression probes (not predefined TP labels):** Exercise searches for a case title field; workspace retention-class settings; and the idempotent repeated case-creation scenario yielding one case and an identical outcome. These are examples of *retrieval failure modes* seen in a prior evaluation, not a goldset, not fixed source-atom IDs, and not permission to label any current source or generated claim without re-reading the actual files. Include additional probes drawn from this run's own PDF and generated tables. If the input corpus changes, derive probes from the new inputs instead of relying on historical IDs.

**Required provisional-FN root-cause disposition:** Every source-positive candidate found by initial matching to be uncovered must receive exactly one final outcome, with real locators:

| `fn_review_disposition` | Meaning | Final handling |
|---|---|---|
| `MATCHER_FALSE_NEGATIVE_CORRECTED` | The generated corpus fully entails the source atom; the initial retrieval or semantic matcher missed it. | Change to TP; preserve proof and correction history. |
| `SOURCE_ATOMIZATION_ERROR_CORRECTED` | The source atom is duplicated, nonnormative, or improperly split/merged. | Correct common `R`; rebuild all affected rows and rates. |
| `TRUE_MISSING` | No eligible definitive generated commitment covers the source duty after bidirectional and applicability checks. | FN; retain searches and nearest actual candidates. |
| `PARTIAL_ENTAILMENT` | Related definitive text exists but a specifically identified required predicate remains absent or contradicted. | FN; cite the strongest partial text and unmet predicate. |
| `CONSERVATIVE_UNRESOLVED` | Evidence is accessible but semantic ambiguity persists after bounded review; no full proof exists. | FN with `BEST_EFFORT_CONSERVATIVE` and explicit uncertainty; not a verified absence claim. |

Only the last three dispositions may remain final FN. Distinguish a **verified absence within the scored corpus**, a **partial specification**, and an **unresolved semantic match** in the report; they must not be presented as the same kind of confirmed omission. Maintain one stable current version of the source, bridge and judgment ledgers after corrections.

### 3.7 Reciprocal generated-claim and TP proof audit

- A generated class lacking a matched source atom is **not inherently unsupported**. Search the PDF by generated target/operation, exact field and method/path, context, exceptions and semantic equivalents. `SUPPORTED_NONCOVERING` requires an affirmative, cited PDF entailment; it is not an unlabeled default for all otherwise unused generated classes.
- Before marking a generated claim `PDF_UNSUPPORTED`, check whether it is a restatement of an independently sourced acceptance case or a narrower supported subclaim. Score only the truly unsupported material; do not count the same underlying generated proposition once as an unsupported class and again as an asserted negative control.
- Re-evaluate each TP with the original PDF and actual generated quotations side by side. For E2 bridges, explicitly demonstrate class membership, predicate completeness, conjunction scope and absence of conflicting exceptions. Do not infer a condition simply because the generated text mentions the right identifier.
- Flag direct identifier/field/path exact hits classified as FN, and generated classes marked unsupported despite a complete source equivalent, as **mandatory semantic review exceptions**. Resolve clear errors within the current phase. Remaining material uncertainty stays `BEST_EFFORT`, not `VERIFIED`.

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

**Bounded adjudication:** For ordinary semantic ambiguity, attempt (i) direct match, (ii) universal applicability, (iii) section/table context, (iv) multi-file conjunction, (v) contrary evidence, and (vi) the reciprocal full-corpus FN challenge in §3.6. If complete entailment remains unproved after actual candidate inspection, record `E1`, the strongest candidate's real locator, a specific unmet predicate, the checked alternatives and a conservative binary judgment. Move on. Do not reopen the phase or produce an endless "needs more analysis" cycle. Mark such decisions `BEST_EFFORT_CONSERVATIVE` and report their count in coverage limitations. **Known explicit matches, uninspected close candidates, or malformed atomization are actionable defects, not ordinary E1 ambiguity; fix them within this response.**

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

Report in `08_coverage_and_limitations.md` (a) final `TRUE_MISSING`, `PARTIAL_ENTAILMENT` and `CONSERVATIVE_UNRESOLVED` counts, (b) corrected false negatives and source-atomization changes with links to `07_change_delta.jsonl`, (c) the number of TP records with complete reviewed proof, (d) unsupported and supported-noncovering generated-class evidence gaps, and (e) any unresolved high-risk direct-match exceptions. Distinguish **structural reconciliation** from **semantic evidence certification** in every summary. An arithmetic pass does not upgrade `FINAL_BEST_EFFORT` to `FINAL_VERIFIED`.

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

Count only independently eligible substantive assertions. Do not count bare references, citations, test IDs, headings, or unadopted options as claim repetitions. Scope-changing changes are not duplicates: `API-001` and `API-002` should not merge merely because their wording matches.

For a reproducible **within-file versus across-file partition**, sort each class's eligible occurrences by input-file order, physical line, and table-cell position, then select the earliest as the representative. Classify each subsequent excess occurrence as `within_file` if an earlier occurrence of that class is in the same file; otherwise classify it as `across_file`. The partition must satisfy:

```text
within_file_excess + across_file_excess = duplicate_excess_occurrences
```

Report separately how many repeated classes span multiple files; that descriptive class count can overlap the within-file classification. `Duplicate` is calculated from **raw occurrences and raw classes**, never from `A_m`, `P_m`, or expanded coverage bridges. If `|GO_m|=0`, return `null`.

## 6. Six phase-complete execution turns

**One user message asking to proceed authorizes exactly the next phase.** Complete that phase in the same response, including its files, calculations, and checks. Multiple internal actions and scripts do not consume additional conversation turns. Do not advance to a later phase in the same answer; do not repeat the same phase in response to the next "next" merely to improve confidence.

| Turn | Complete work package | Minimum final deliverables and completion test |
|---|---|---|
| **1 — Independent PDF requirements and fixed controls** | Verify all 90 pages; extract `R` and fixed `N`; audit parent/child splits, repeated universal boilerplate, duplicate test-matrix statements, and inherited field/table context before fixing the source denominator; record exclusions and page coverage. | `01_source_atoms_final.jsonl`, `01_source_negative_controls_final.jsonl`, PDF coverage, exclusion evidence, and independently meaningful source atoms; record any initial atomization concerns for Phase 5. |
| **2 — Entire generated corpus and raw deduplication** | Inspect every substantive line and table cell of all eight inputs; extract definitive `GO_m`; preserve table/header/row scopes; construct raw `G_m`; retain canonical identifier/field/API/test lookup keys for reciprocal retrieval; record exclusions and coverage. | `02_generated_atoms_final.jsonl`, `02_generated_classes_final.jsonl`, `04_duplicate_classes_final.jsonl`, generated exclusions and line/cell coverage with usable evidence locators. |
| **3 — Semantic source coverage** | For every `r in R`, apply the complete entailment rubric; run the bidirectional challenge for **every provisional FN**, reconstruct table/test context, classify root causes, correct decisive matcher false negatives and atomization errors immediately, and verify TP evidence predicates. Identify potential unsupported generated claims. | Draft `03_canonical_universe_final.jsonl`, `03_evidence_matches_final.jsonl`, `03_semantic_coverage_bridges_final.jsonl`, **`03_fn_root_cause_audit_final.jsonl`**, complete TP/FN decisions with actual retrieval evidence and no known uncorrected exact matches. |
| **4 — Generated correctness and full four-cell universe** | Validate each raw `g` against the PDF using reciprocal source lookup; explicitly challenge `SUPPORTED_NONCOVERING` and apparent FPs; identify `F_m` and `B_m`; finalize `U_m` and calculate four cells. Distinguish semantic support from score coverage. | `04_generated_claim_validity_final.jsonl`, `04_atomic_judgments_final.jsonl`, `04_confusion_matrix_final.json` and `.md`, canonical universe, structural and semantic evidence checks. |
| **5 — Corrections, merges, and duplicate metrics** | Re-audit **all remaining FN candidate dispositions**, every TP evidence bridge, source split/merge errors, negative controls, and raw duplicates. Apply bounded corrections across all affected ledgers and recompute the four cells **within this turn**. | Corrected ledgers, **`05_tp_evidence_audit_final.jsonl`**, **`05_source_atomization_audit_final.jsonl`**, `04_duplicate_classes_final.jsonl`, `05_duplicate_metrics_final.json` and `.md`, `07_change_delta.jsonl`, and revised four-cell files. |
| **6 — Independent recomputation and individual delivery** | Recompute from final item-level ledgers; validate TP proofs and FN root-cause closure, test exact-match regression probes, source atomization, one-universe equations, input/page/line coverage, duplicate partitions, file language, paths, and method isolation. Do not certify semantics from arithmetic alone. | `06_metrics_final.json` and `.md`, `compute_metrics.py`, `08_coverage_and_limitations.md` with provisional-versus-verified score interpretation, FN/TP/atomization audits, exclusions, and individual file links. Comparison files required only for multiple methods. |

**A request solely to revise this protocol is not an evaluation phase.** No prior TP, TN, FP, FN, historical atom count, or duplication percentage is a preapproved answer for a new run.

### Mandatory no-loop completion rule

- Finish each phase **once**. Normal ambiguous E1/E0 decisions use the bounded process in §4.2 and an explicit accuracy caveat. Imperfect semantic adjudication is not a reason for a second Phase 3 or an indefinite hold.
- If necessary, prefer transparent conservative approximation and a complete, structurally valid output over another round of polishing. Do not knowingly label unsupported TP as verified. Complete the mandated reciprocal FN audit and correct **known** matcher/atomization defects in that phase; only genuinely unresolved semantic interpretations can remain conservatively adjudicated.
- Report phase status as `PHASE_COMPLETED_VERIFIED` when full evidence checks pass, or `PHASE_COMPLETED_BEST_EFFORT` when accessible evidence has been adjudicated using documented conservative approximations. A later improvement belongs in the designated correction phase, **not** a repeated earlier phase.
- If a mandatory PDF or scored input is unavailable/corrupt, finish the current response with the available partial artifacts and `PHASE_TERMINATED_INPUT_BLOCKER`, identifying the exact inaccessible content. Never claim complete evaluation or invent final metrics for missing material.
- A phase may not be declared `FINAL_VERIFIED` from arithmetic reconciliation alone. Explain the difference between structural validity and semantic-evidence certification.

## 7. Required individual deliverables

For one evaluated method, use one output directory. For multiple methods, share `R` and `N` at root and place method-specific files beneath method-prefix directories. Output file text, explanations, scripts, JSON keys/values written as prose, and Markdown headings must be **English only**. Existing input filenames in location fields are retained unchanged. Deliver individual files, never a bundled archive.

| Filename | Purpose |
|---|---|
| `01_source_atoms_final.jsonl` | Independent PDF-positive atoms with exact English quotes and physical PDF pages. |
| `01_source_negative_controls_final.jsonl` | Fixed PDF-grounded negative counterfactuals and derivation rules. |
| `02_generated_atoms_final.jsonl` | Every definitive generated occurrence with original file/line/table-cell location. |
| `02_generated_classes_final.jsonl` | Raw canonical semantic classes `G_m` and occurrence membership. |
| `03_canonical_universe_final.jsonl` | Canonical units `U_m`: source-positive atoms, negative controls, and distinct unsupported generated propositions. |
| `03_evidence_matches_final.jsonl` | PDF/generated evidence, complete-predicate checks, grades, and alternative searches. |
| `03_semantic_coverage_bridges_final.jsonl` | Universal-instantiation, contextual, conjunctive and equivalent-meaning TP bridge proofs. |
| `03_fn_root_cause_audit_final.jsonl` | Every initially uncovered source atom: reciprocal-search evidence, strongest alternative, root-cause disposition, and final TP/FN or source-inventory correction. |
| `04_generated_claim_validity_final.jsonl` | Every raw generated class labeled PDF_ENTAILED, PDF_UNSUPPORTED, or SUPPORTED_NONCOVERING. |
| `04_atomic_judgments_final.jsonl` | Exactly one `TP`/`TN`/`FP`/`FN` judgment per canonical proposition in `U_m`. |
| `04_confusion_matrix_final.json` and `.md` | Audited or explicitly best-effort four-cell totals, rates, equations, and bounded-TN explanation. |
| `04_duplicate_classes_final.jsonl` | Raw semantic classes, eligible occurrences, and merge/split reasoning. |
| `05_duplicate_metrics_final.json` and `.md` | Duplication counts/rate, within-file/across-file excess and class repetition. |
| `05_tp_evidence_audit_final.jsonl` | Every initially positive TP candidate, including corrected-to-FN cases; all final TP records have confirmed full-predicate proof and real source/generated locators. |
| `05_source_atomization_audit_final.jsonl` | Source split/merge/dedup review decisions, including test-matrix overlap, with old/new IDs; one `NO_ATOMIZATION_CHANGES` marker if no changes. |
| `06_metrics_final.json` and `.md` | Final recomputation of confusion and duplication, assumptions, status, and limitations. |
| `07_change_delta.jsonl` | Substantive corrections or one `NO_COMPARABLE_BASELINE` marker. |
| `08_coverage_and_limitations.md` | PDF/Markdown coverage, actual-input status, FN root-cause counts, corrected false-negative and atomization cases, TP evidence quality, bounded TN, and reliability limits of the calculated metrics. |
| `09_excluded_units.jsonl` | Nonnormative PDF items and nondefinitive generated items with locators and exclusion reasons. |
| `compute_metrics.py` | Independent ledger-based structural recomputation and assertions. |
| `11_comparison_final.json` and `.md` | Required only when two or more methods are evaluated with the same fixed `R` and `N`. |

Optional local audit aids may be delivered individually. Do not let extra audit files substitute for required item-level evidence. Do not deliver legacy source-coverage-only or generated-claim-only metrics as the purported conventional four-cell result.

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

In `03_fn_root_cause_audit_final.jsonl`, record one row for every source atom initially nominated as FN (including corrected cases): `source_id`, `initial_grade`, `initial_predicted_label`, `fn_review_disposition`, `final_source_id_or_replacement_ids`, `final_scoring_cell` (or `REMOVED_OR_MERGED`), `pdf_evidence`, `best_generated_candidates` with actual file/line/table-cell quotation, `exact_and_alias_keys_checked`, `universal_context_conjunction_checked`, `scope_membership_proof_en`, `met_predicates_en`, `unmet_predicates_en`, and `specific_reason_en`. Each final FN must be `TRUE_MISSING`, `PARTIAL_ENTAILMENT`, or `CONSERVATIVE_UNRESOLVED`. Do not claim to have searched the complete corpus based solely on a generic true/false flag; retain enough actual candidate/search evidence to reproduce the conclusion.

In `05_tp_evidence_audit_final.jsonl`, record one row for each **initial TP candidate**, preserving corrected-to-FN cases: `source_id`, `entailment_grade`, `coverage_mode`, actual `pdf_evidence`, real `generated_evidence` locators, a full predicate-check map with `met`/`not_applicable` and explanatory proof, `scope_membership_proof_en` for universal bridges, `contrary_evidence_checked_en`, and `audit_outcome` (`CONFIRMED_TP` or `CORRECTED_TO_FN`). A TP that is downgraded must be reflected in the canonical judgment ledger and change delta. Each **final** TP must have exactly one audit record with `CONFIRMED_TP`; any `CORRECTED_TO_FN` audit must reference a final FN or a documented source-atom correction. Counts alone are not evidence.

In `05_source_atomization_audit_final.jsonl`, describe each substantive duplicate/parent-child/test-overlap/split/merge correction with PDF quotes and old/new source IDs; if none were needed, emit one `NO_ATOMIZATION_CHANGES` record documenting the checks performed. Correct the shared `R` and rerun affected method comparisons consistently.

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

### 8.3 Required independent recomputation

`compute_metrics.py` must read the final JSON/JSONL ledgers and:

1. Parse unique frozen PDF atoms `R`, negative controls `N`, eligible generated occurrences `GO_m`, raw classes `G_m`, source coverage bridges `A_m`, asserted controls `B_m`, and distinct unsupported generated propositions `F_m`.
2. Assert `R ∩ N = ∅`; source and negative IDs are unique; every eligible occurrence belongs to exactly one raw class for its method; no cross-method references appear.
3. Assert there is exactly one binary judgment per canonical `U_m` record, with correct `actual_label`, `predicted_label`, and `scoring_cell`.
4. Assert every TP identifies a valid source atom and complete direct/E2 bridge evidence and an entry in the TP evidence audit; every FN has exactly one permissible final root-cause disposition and actual reciprocal-search candidate evidence; every FP identifies a single unsupported proposition or asserted control; every TN references an unasserted fixed control. Ensure corrected candidate-FNs are not still scored as FN and that old atom IDs affected by merges are not double-counted.
5. Assert the nonoverlap of `R`, `N`, and `F_m`, and that asserted negative controls are not also separate unsupported generated-only FP entries.
6. Independently recompute `TP=|A_m|`, `FN=|R|-|A_m|`, `TN=|N|-|B_m|`, `FP=|F_m|+|B_m|`, `|U_m|=|R|+|N|+|F_m|`, `|P_m|=TP+FP`, and the four-cell total.
7. **Do not assert** `TP+FP=|G_m|`. Instead assert `TP+FP=|P_m|` and independently verify `|GO_m| >= |G_m|`.
8. Recompute conventional Precision/Recall/F1 on the effective canonical universe and Duplicate on the raw occurrence/class universe. Reconcile within/across-file excess to the duplicate total.
9. Verify that `08_coverage_and_limitations.md` discloses universal-rule coverage, bounded TN, initial-FN root causes, corrected false negatives, source-atomization deltas, complete TP proof-audit counts, best-effort cases, the difference between raw-class precision and effective-universe precision, input scope, and evidence limitations.
10. Verify all eight scored inputs per selected method were actually available and inspected, required authored deliverables are English, and all reported output paths exist.
11. Fail `FINAL_VERIFIED` certification if any final TP lacks reviewed complete-predicate proof, any FN lacks documented reverse search and a root-cause disposition, any known exact-match inconsistency is unresolved, or any source-atomization error or structural equation remains unfixed. A transparent `FINAL_BEST_EFFORT` result is acceptable with complete inputs, full universe enumeration, reproducible judgments, and explicitly quantified unresolved *semantic* uncertainty; it must not conceal known, objectively correctable false negatives.
12. Check that the sum of final FN root-cause counts equals FN and that each final TP appears exactly once in the TP proof audit. The root-cause ledger may contain corrected candidate-FNs whose final cell is TP or whose source atom was merged; exclude those from the final FN subtotal and reflect every change in the ledger and `07_change_delta.jsonl`.
13. Run reciprocal diagnostic probes using actual case/field/API/test identifiers present in the supplied files. Flag an apparent explicit full match still classified as FN, or a supported generated proposition still classified as an FP, for mandatory adjudication before final reporting. The checker can validate evidence structure and suspicious matches, but must not claim to prove logical entailment purely by string matching.
14. Never hardcode expected TP/TN/FP/FN, PDF requirement totals, generated class totals, or historical scores. Historical false-FN examples are diagnostic retrieval probes, not fixed expected outputs or input-derived goldsets.

### 8.4 Cross-method fairness and interpretation

Use identical source-positive `R`, negative `N`, adjudication rubric, and applicability tests for `fullload`, `onelevel`, and `twolevel`. A generated universal statement may cover the same source atoms for any method if its scope proof is equally strong. Compare the resulting effective-proposition Precision, Recall, F1, and raw-class Duplicate. Report raw class count separately, not as the Precision denominator unless a separately labeled class-level metric is being computed.

Do not reinterpret these scores as verified implementation correctness, production safety, or actual application performance. They measure coverage and correctness of **generated specifications** against this specific fictional PDF baseline.

## 9. Completion gates, failures, and stop rule

For an accessible complete input set, the standard finish conditions are: all 90 physical PDF pages inspected, eight scored Markdown roles inspected including substantive table cells, full independently atomized `R` and `N` inventory, definitive `GO_m` and `G_m` inventory, **bidirectionally challenged FN candidate decisions**, **predicate-audited TP proofs**, correctness decisions for every generated class, a fully enumerated `U_m`, source split/merge deltas, exact equations, and English individual outputs.

**Permitted reporting statuses:**

- `PHASE_COMPLETED_VERIFIED`: The current phase's evidence and structural requirements were fully verified.
- `PHASE_COMPLETED_BEST_EFFORT`: The current phase was finished with all accessible scope enumerated, conservative E1/E0 decisions, explicit limitations, and valid structural ledgers. No phase-repeat obligation remains.
- `PHASE_TERMINATED_INPUT_BLOCKER`: A specified original PDF page or required scored document is missing/unreadable/corrupt; publish available partial work without invented final scores.
- `FINAL_VERIFIED`: All six phases completed with verified evidence and recomputation.
- `FINAL_BEST_EFFORT`: All six phases completed with enumerated evidence, structurally correct metrics, and clearly disclosed bounded approximations.

Do not use `FINAL_VERIFIED` for merely plausible similarity matches, sparse sampling, unchecked candidate FNs, unsupported E2 bridges, or arithmetic-only checks. Do not call accessible ordinary ambiguity a technical blocker. If meaning is only partial after the prescribed checks, record E1/E0 and decide conservatively **in the same phase** rather than deferring it indefinitely. **An explicitly discovered complete match left labeled FN is a known error, not an acceptable unresolved ambiguity.**

When a single assistant response cannot support exhaustive semantic checking to a certification standard, produce the fullest defensible item-level ledger with an explicit best-effort status, quantify potentially affected cases, and close that phase. An actual missing input is different: terminate with a precise blocker, without inventing absent evidence.

**Final operator directive:** Evaluate the original English PDF and all eight supplied Markdown specifications with complete semantic entailment, explicit universal-rule applicability, and a mandatory reverse challenge of *every provisional FN*. Prevent artificial source-denominator inflation, missed field/API/test equivalences and unsupported TP bridges. Keep raw duplicate counts separate from canonical coverage projections. Deliver one coherent TP/TN/FP/FN universe, conventional effective-universe Precision/Recall/F1, semantic duplication, FN root-cause dispositions, predicate-level TP evidence, source-atomization corrections, and individual English files. **Do not interpret a structurally valid metric as semantically certified. Exactly one phase must be closed in each subsequent evaluation response; no repeated phase loops, no hidden scope change, and no archives.**


## 10. Version 6.1 change summary (non-execution metadata)

This revision preserves the six-turn limit, the authoritative PDF-only source rule, eight scored inputs, one canonical TP/TN/FP/FN universe, metric equations, and the no-archive rule. It adds: (1) a required independent source-atomization and acceptance-test deduplication check; (2) full-corpus reciprocal FN retrieval and table-context reconstruction; (3) corrected-false-negative versus genuinely missing versus partial/unresolved dispositions; (4) audited E2/TP predicate proofs and reciprocal FP validation; and (5) explicit reliability disclosures and machine-verifiable reconciliation across new audit ledgers. Prior-run scores and observed false-negative examples are **not** accepted as current-run ground truth.
