# OrionDesk AI — Frozen-Reference Semantic Evaluation Protocol

**Protocol version:** 7.0  
**Status:** New, self-contained protocol; not a patch or an amendment to a previous version.  
**Purpose:** Compare the fidelity and requirement coverage of AI-generated software design specifications using one externally constructed and frozen Gold Set.  
**Supported methods:** `fullload`, `onelevel`, `twolevel`.  
**Execution environment:** SaaS-hosted ChatGPT; ordinary Python-based file parsing and deterministic checks may be performed within that environment. Codex and switching to external coding agents are not required.  
**Conversation language:** Follow the user's explicit instruction; Japanese when requested.  
**Authored artifact language:** **English only**, including narrative text, field descriptions, report headings, machine-readable strings, and scripts. Original quotations retain the source language.  
**Human interaction budget:** **Six request–response turns maximum for one selected evaluation scope**, with exactly one complete work package per turn. The turn budget is not an API-call budget.

## 1. Governing principles

1. **Read-only reference:** The Gold Set and negative controls are supplied outputs of a separate construction workflow. They are **not** created, reconstructed, semantically validated, supplemented, split, merged, renumbered, corrected, or overwritten during metric evaluation. This applies to temporary copies and final outputs as well as the input originals.
2. **Assumed source coverage:** For the purpose of this evaluation, assume that the externally reconstructed Gold Set comprehensively represents the PDF's normative atomic requirements. Do **not** undertake an independent Gold Set completeness study, page-by-page re-extraction, or source-inventory atomization audit in this protocol.
3. **Reference freeze precedes Turn 1:** The reference version and exact bytes must be fixed before any generated specifications are scored. Once the run starts, use identical reference bytes, identifiers, and scoring rules for every selected method and throughout all six turns.
4. **The PDF remains the evidentiary authority:** Use the original PDF to substantiate semantic matching and test whether a generated claim is actually supported, contradicted, or unsubstantiated. This is **generated-output evaluation**, not Gold Set reconstruction or certification. A valid PDF-supported generated claim that does not cover any frozen reference atom is not automatically a false positive.
5. **One explicit decision universe:** Compute TP, TN, FP, and FN over one enumerated canonical binary universe for each method. Never mix raw occurrence counts, generated-class counts, and source-atom counts without an explicit projection.
6. **Canonical FP counting:** Before counting FP, merge semantically identical unsupported claims across all eight generated specifications. Count the unsupported proposition once, while retaining every source occurrence and provenance. Do not merge merely related, overlapping, or partially different claims.
7. **Two duplicate types:** Classify eligible excess occurrences into exactly `EXPECTED_REUSE` and `REDUNDANT_DUPLICATE`; report both separately. A purposeful cross-document restatement is not automatically a quality defect.
8. **Two measurement views:** Retain conventional canonical-universe Precision, Recall, and F1 and add a distinctly named, expressly **nonstandard** generated-claim-validity measure. Do not substitute one for the other.
9. **Independent critical adjudication:** Perform one independently prompted evidence review of each critical semantic judgment or materially identical review group, with at most one targeted conflict resolution. The goal is independent challenge, not repeated self-confirmation. Do not initiate indefinite review loops or review every ordinary judgment multiple times.
10. **Unconfirmed FN contributes to metrics:** Report fully challenged true FN separately from unconfirmed FN, but include **both** in the total FN used for Precision, Recall, and F1.
11. **Bounded TN:** Negative controls represent a **fixed, bounded diagnostic subset** of the source-negative universe. TN is **not** the population count of everything absent from the PDF. Never infer specificity or population-wide accuracy from these controls.
12. **No manufactured assurance:** A passed script, complete file list, or plausible confusion matrix does not establish correct semantic entailment. Preserve evidence, residual uncertainty, and actual coverage limitations.

This protocol defines **metric evaluation only**. Gold Set construction, quality certification, repairs, and reference re-release belong to a separate workflow; none is a phase, subtask, required deliverable, or permissible automatic repair here.

## 2. Inputs and immutable boundaries

### 2.1 Required inputs

| Input | Evaluation role | Treatment |
| --- | --- | --- |
| `common_atomic_reqs.jsonl` | Frozen source-positive atomic requirements, `R` | Read-only; assumed comprehensive and already constructed and validated externally |
| `common_negative_controls.jsonl` | Frozen bounded source-negative counterfactuals, `N` | Read-only; no creation or revision in evaluation |
| Original `OrionDesk_AI_Detailed_Design_Specification.pdf` | PDF evidence for adjudicating generated claims and matching references | Read for matching and claim support, never for rebuilding `R` or `N` |
| Eight scored Markdown files per selected method | Generated specifications to evaluate | Read-only; never silently edit or regenerate |

The two reference filenames above are canonical. A supplied filename with a harmless upload suffix is acceptable only if its role is unambiguous. Record the actual path and the source-file SHA-256. Do **not** silently replace these inputs with a historical ledger, a newly synthesized ledger, or a ledger copied from a different run.

Required scored roles (recognizable method prefixes, timestamps, and copy suffixes are acceptable only when unambiguous):

1. `01_screen_functions.md`
2. `02_api.md` (accept `02_api_.md` if that is the supplied file)
3. `03_data.md`
4. `04_batch_functions.md`
5. `05_business_rules.md`
6. `06_exception_handling.md`
7. `07_processing_flows.md`
8. `08_architecture_decision.md`

The eighth file is scored, but `TBD`, open questions, unadopted proposals, and undecided alternatives are **not** definitive implemented commitments. Explicitly adopted, definitive claims may be eligible if evidence supports that status.

### 2.2 Permitted input checks versus prohibited Gold Set verification

Permitted: confirm that required files exist and are readable; check JSONL parseability, required identifier fields, duplicate identifiers, file-to-role mapping, and content hashes; record counts as **input metadata only**. These are technical integrity checks, **not** a semantic audit or completeness certification.

Prohibited: rescan all PDF pages to extract missing reference atoms; compare chapter maps for Gold Set omissions; alter the reference set in response to generated text; normalize away allegedly duplicate reference atoms; add or modify negative controls; produce replacement `common_*.jsonl` files.

If a reference item seems inconsistent with PDF evidence while adjudicating a generated claim, record `REFERENCE_EXCEPTION` with the exact frozen ID, the PDF evidence and its potential effect. Do not revise the reference, create a substitute scoring item, or silently remove it from a denominator. If the inconsistency makes a material result indefensible, withhold `FINAL_VERIFIED` and mark the result as qualified or blocked as appropriate. **Do not turn that exception into a Gold Set validation phase.**

### 2.3 Freeze and cross-method fairness

At the start of Turn 1, record the SHA-256 of both frozen ledgers and PDF and the sizes and paths of scored inputs. The same `R`, `N`, rule definitions, evidence standards, and judgment policies must be used for all selected methods. Assert that reference hashes remain unchanged before final reporting. If a reference changes, **end the run as invalid**; a new run with a new frozen reference is required. Do not quietly continue or recompute a favorable subset.

### 2.4 Evaluation scope

An evaluation may select one method or all three. A six-turn run applies to the **selected scope**, not six turns per internal chunk, and never requires the human to alternate between ChatGPT and Codex. For multiple methods, preserve method isolation and produce a side-by-side comparison only when they share the same frozen reference.

## 3. Semantic units and scoring model

### 3.1 Source and generated units

For a selected method `m`, let:

```text
R      = fixed set of source-positive atomic requirement IDs and propositions
N      = fixed set of bounded source-negative counterfactual control IDs
GO_m   = all eligible definitive generated claim occurrences across eight files
GC_m   = distinct, fully normalized semantic classes of GO_m
A_m    = {r in R : the complete generated corpus entails every material predicate of r}
B_m    = {n in N : an eligible generated claim asserts or entails n}
F_m    = distinct unsupported or source-contradicting generated-only propositions,
         including explicitly conservative unresolved predictions when necessary,
         after cross-file semantic merging and excluding propositions represented in B_m
U_m    = R disjoint-union N disjoint-union F_m
P_m    = A_m union B_m union F_m
```

`GC_m` contains **one class per complete semantic proposition**, not one class per file, sentence, appearance, or PDF atom. Normalize actor, object, operation, modality, condition, scope, exception, timing, constraints, version, and outcome. Keep original occurrence IDs and exact file/line/table-cell locators. A shared universal generated rule may cover multiple genuinely distinct `R` atoms without creating more occurrences or generated classes.

**Do not assume** `|P_m| = |GC_m|`. Source-atom coverage projections and generated-class counts measure different things.

### 3.2 Generated eligibility

Include definitive, independently meaningful implementation/design commitments: API behavior, data constraints, access restrictions, processing conditions and outcomes, timing, exception handling, security rules, and accepted decisions. Exclude pure headings, citations, test-case references without an independent assertion, illustrative nonadopted examples, unresolved options, and unapproved proposals. If a table cell is abbreviated, reconstruct its full meaning using the table title, column, row, section, and explicit inherited rules.

Split a generated sentence when it contains genuinely independent testable commitments. Do not artificially split equivalent wording into many classes. A prohibition is a positive commitment to prohibit behavior; preserve logical polarity rather than converting every negation into a negative control.

### 3.3 Semantic entailment rubric

For **each source atom**, compare the complete predicate against all eligible generated evidence, using:

1. Direct equivalence, including ordinary paraphrases and identifier aliases.
2. Explicit universal or class-wide statements, with a proven membership link for the particular endpoint, object, actor, or workflow.
3. Table/section context and cross-document conjunction when each part is a definitive commitment.
4. Exact conditions, modality, timing, scope, limitations, exceptions, version, and outcome.
5. Contrary and inconsistent generated evidence; mere topic overlap is not a TP.

Use evidence grades:

| Grade | Interpretation | Source-coverage decision |
| --- | --- | --- |
| `E3` | Complete direct semantic equivalence, with genuine locators | TP |
| `E2` | Complete proved entailment through universal/contextual/conjunctive bridge | TP |
| `E1` | Material overlap, but at least one required predicate is not established | FN |
| `E0` | No defensible entailment or contradiction after the retrieval procedure | FN |

Do not infer an exact error code from generic validation, an ordering guarantee from eventual completion, or permission from an unrelated similar operation. E2 counts as **full TP** only with an explicit complete applicability proof.

### 3.4 Bidirectional source-coverage search

Before finalizing an FN candidate, search all eight generated files by exact source identifiers, API method/path, field/entity name, actor, event name, response code, test trigger/outcome, aliases, and relevant general rules. Search both source-to-generated and generated-to-source. Inspect strongest candidates in their original table/section context; check cross-file conjunctions. A similarity-only top-k search cannot by itself establish absence. Preserve actual candidate text and rejected entailment predicates, not only a search counter or an unchecked assertion that the corpus was inspected.

### 3.5 Generated claim validity against PDF

Evaluate every unique generated class against the **original PDF**, not merely against the list of `R` IDs:

- `PDF_FULLY_SUPPORTED`: every material predicate of the generated class follows from PDF evidence; may cover zero, one, or several frozen `R` atoms.
- `PDF_NOT_FULLY_SUPPORTED`: at least one substantive generated predicate is unsupported, exceeds scope, or contradicts PDF evidence after full review. Record the unsupported residual and its FP canonical cluster unless already represented by `B_m`.
- `PDF_SUPPORT_UNRESOLVED`: available evidence does not resolve whether the complete generated class is supported. Record the strongest source evidence and uncertainty. Under the conservative binary policy, any distinct unresolved unsupported residual is provisionally counted in `F_m` and therefore FP; mark it provisional, not a verified fabrication.

A class fully supported by the PDF but not mapped to a frozen source atom is `PDF_FULLY_SUPPORTED` with a `SUPPORTED_NONCOVERING` coverage tag. **It is not FP**, and `R` remains unchanged. It also does not create a new TP or increase the denominator of Recall. The completeness assumption about `R` is not permission to contradict directly observed PDF evidence.

When a compound generated statement contains both a supported obligation and an unsupported additional permission, identify the distinct fully supported subclaim and unsupported residual without erasing qualifiers. One residual is counted once per **unique semantic proposition**, not once per failed `R` match, document, or sentence. A class that asserts an `N` control is represented in `B_m` and must not appear a second time in `F_m`.

### 3.6 Source-negative controls

`N` is a fixed bounded set of affirmative-sounding counterfactuals derived externally from explicit exclusions, prohibitions, or deferrals. For each `n in N`, classify whether the generated corpus definitively asserts it. If asserted, that negative-control row is FP; otherwise it is TN. The rule is about **generated assertion**, not the general absence of a feature from the PDF. Do not create additional controls or alter the supplied controls.

## 4. Metrics and their interpretation

### 4.1 Conventional binary metrics on the effective canonical universe

```text
TP = |A_m|
FN = |R| - |A_m|
TN = |N| - |B_m|
FP = |F_m| + |B_m|

|U_m| = |R| + |N| + |F_m|
|P_m| = TP + FP

TP + FN = |R|
TN + |B_m| = |N|
FP - |B_m| = |F_m|
TP + TN + FP + FN = |U_m|

Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 * TP / (2 * TP + FP + FN)
```

These are conventional binary-rate formulas **on this protocol's explicitly defined effective proposition universe**. `TP` counts covered source atoms, while `FP` counts distinct unsupported generated residual propositions and asserted negative controls. This is an intentionally disclosed difference of semantic projection units; the resulting Precision is **not** raw generated-class precision. Neither equality of `TP + FP` to `|GC_m|` nor equivalence with the new class metric is implied.

If a rate denominator is zero, write JSON `null` and explain. Report numerical rates consistently as decimal fractions or percentages with units. Do not hardcode expected counts or historical results.

### 4.2 Mandatory FN subdivision, without changing the conventional equations

Every source-positive unit not proven covered receives exactly one of these **two** final FN categories:

- `TRUE_FN`: the prescribed bidirectional **full eight-file** retrieval, strongest-candidate inspection, contextual checks, and evidence comparison have been completed; no eligible generated material fully entails the requirement. This includes fully audited partial entailments with a specific missing predicate. `TRUE_FN` means substantiated absence of **full coverage within the scored corpus**, not a claim that no related text exists anywhere.
- `UNCONFIRMED_FN`: full coverage was not established, but the search or semantic adjudication remained incomplete or materially uncertain. Preserve what was checked, the strongest available evidence, and the precise unresolved issue. Do **not** label this a confirmed source omission.

```text
FN_true        = count(TRUE_FN)
FN_unconfirmed = count(UNCONFIRMED_FN)
FN             = FN_true + FN_unconfirmed = |R| - TP
```

**Both categories are counted as FN in Precision, Recall, and F1.** Report `FN_true` and `FN_unconfirmed` next to each metric set and distinguish source absence from unconfirmed coverage. If the number of unconfirmed cases is material, mark the score `BEST_EFFORT`; never call it semantically certified. Missing/unreadable mandatory input is an input blocker, not an `UNCONFIRMED_FN` shortcut.

### 4.3 New nonstandard metric: Generated Claim Validity Rate (GCVR)

**Definition (original protocol-specific measure):** Among all **unique eligible definitive generated semantic claim classes** in `GC_m`, what fraction is fully supported by the original PDF?

```text
C_supported  = number of classes with PDF_FULLY_SUPPORTED
C_invalid    = number of classes with PDF_NOT_FULLY_SUPPORTED
C_uncertain  = number of classes with PDF_SUPPORT_UNRESOLVED
C_all        = |GC_m| = C_supported + C_invalid + C_uncertain

GCVR = C_supported / C_all
```

- Count each generated semantic class **once**, regardless of its number of source atoms covered or occurrences across documents.
- A fully PDF-supported `SUPPORTED_NONCOVERING` generated class **does** contribute to `C_supported` even without a match to `R`.
- A partially supported class is **not** fully valid; if meaningful independent claims can be separated, first atomize them consistently before assigning classes and calculating GCVR.
- Unresolved classes remain in the denominator but **not** the numerator, and `C_uncertain` is prominently disclosed. Thus GCVR is a **conservative operational estimate**, not an estimate with a statistical confidence interval or a universal truth claim.
- For `C_all = 0`, return `null`. Never round raw counts or use duplicated occurrences as the denominator.

**Interpretation:** GCVR describes **generated-claim support**, while Recall describes **coverage of frozen PDF source requirements**; conventional Precision describes correctness within the **effective canonical projection universe**. They are distinct. **GCVR is a newly defined, nonstandard auxiliary indicator**, not a replacement for conventional Precision and not grounds to claim a method is superior by itself. Retain all four-cell metrics independently.

### 4.4 Exactly two duplicate types

For each semantic class, select one representative occurrence by deterministic order: scored-file order, line, then table-cell position. Every other occurrence of that class is an **excess occurrence**, and must have **exactly one** of the following mutually exclusive types:

- `EXPECTED_REUSE`: a semantically identical assertion deliberately serves an independently justifiable role in a distinct specification context (for example, the same required API constraint also being necessary in a processing-flow specification). Record specific role and location evidence. Cross-file duplication alone is **not** sufficient proof of expected reuse.
- `REDUNDANT_DUPLICATE`: a repeated substantive assertion that adds no independently justified contractual, operational, or verification role. This includes unnecessary repetition inside one file or across files. Record the representative occurrence and why the additional assertion is redundant.

Use the **same full-predicate equivalence standard** for clustering duplicates and FP candidates. Similar topics, a narrower rule versus a broader rule, different endpoint/resource scopes, distinct failure codes, or changed conditions are not semantically identical; do **not** merge them to make duplication or FP appear smaller.

```text
C_occurrences       = |GO_m|
C_unique_classes    = |GC_m|
Duplicate_excess    = C_occurrences - C_unique_classes
Expected_reuse      = count(excess occurrences labeled EXPECTED_REUSE)
Redundant_duplicate = count(excess occurrences labeled REDUNDANT_DUPLICATE)

Expected_reuse + Redundant_duplicate = Duplicate_excess

Expected_reuse_rate      = Expected_reuse / C_occurrences
Redundant_duplicate_rate = Redundant_duplicate / C_occurrences
```

When `C_occurrences = 0`, both rates are `null`. Report **the two types separately as the primary duplicate result**; a raw total may be given for reconciliation, but never report an undifferentiated single `Duplicate` value as though all repetition were harmful. A class that appears in several documents does not become several source-atom TPs merely because it is repeated.

### 4.5 Bounded meaning of TN

`TN = |N| - |B_m|` only measures **unasserted predeclared negative controls** in a deliberately bounded set. There are innumerable possible false features not enumerated by `N`. TN cannot be interpreted as a population-wide true-negative count; these data do not justify general specificity, negative predictive value, or overall accuracy of generated specifications across all imaginable absent claims. Adding more predeclared unasserted controls can increase TN but does **not** change Precision, Recall, F1, or GCVR.

## 5. Mandatory FP cluster audit

Perform a **corpus-wide canonical FP audit**, not a source-to-generated unmatched-count shortcut.

1. Extract every definitive generated occurrence and restore inherited context before any FP classification.
2. Group semantic equivalents into full-predicate `GC_m` classes across all eight files; preserve original occurrences.
3. For each candidate unsupported claim, search the entire PDF for direct support, equivalent terminology, table context, explicit universal rules, exceptions, adopted scope and cross-section conjunction. Lack of a match in `R` alone **never proves FP**.
4. Split supported subclaims from truly unsupported additions without dropping conditional predicates; flag unsupported or contradicting residuals.
5. Normalize all remaining unsupported residuals into **distinct canonical FP propositions**, preserving polarity, target, actor, conditions, scope, modality, timing, outcomes and versions.
6. Deduplicate the residuals **again across all classes and files**, using bidirectional semantic entailment as the equivalence test. A relation of simple containment or shared subject is not equality. Maintain `FP_CLUSTER_ID -> [generated_class_ids, occurrence_ids, evidence]`.
7. Match asserted `NEG-*` controls and remove their exact semantic equivalents from the generated-only `F_m` pool; never count the same proposition in both `B_m` and `F_m`.
8. Verify unique cluster IDs, source locators, original candidate coverage, evidence of semantic equivalence, and reconciliation `FP = |B_m| + |F_m|`.
9. For high-consequence or ambiguous FP clusters, request the independent critical check in Section 6; do not simply relabel every FP as a duplicate or make unsupported behavior disappear.

Maintain at least these descriptive FP subtypes without changing the four-cell equations: `PDF_CONTRADICTION`, `UNSUPPORTED_ADDITION`, and `CONSERVATIVE_UNRESOLVED`. A subtype is a **diagnostic annotation**, not a new confusion-matrix cell or a third duplicate type.

## 6. Independent, bounded critical adjudication

### 6.1 What qualifies as critical

A judgment is critical if **any** of these apply:

- A source-positive atom has an apparently direct complete match but was classified as FN, or a generated claim has a persuasive PDF match but was classified as FP.
- A single universal or cross-file rule is being used to cover **five or more** distinct `R` atoms, or its scope could materially change the result.
- A generated claim contradicts an explicit PDF constraint or asserts a predeclared `N` control.
- An FP canonical cluster changes the FP count substantially if merged or split, or contains a serious semantic scope/modality dispute.
- A required privacy, authorization, safety, financial, data-integrity, or irreversible-action predicate is uncertain or contradictory.
- A remaining `UNCONFIRMED_FN` has an identified close candidate whose acceptance would change a scoring cell.

Ordinary clear direct matches and routine noncritical judgments do not require independent re-review. A large raw occurrence count alone is not a reason to launch a separate review for every repeated occurrence: **review the canonical decision, not its copies**.

### 6.2 Independence procedure and strict anti-loop rule

For each unique critical canonical decision (or evidence-identical group):

1. Preserve the initial decision, strongest candidate evidence, and a concise predicate-level rationale.
2. Submit an **independently prompted second assessment** within the **same user turn and SaaS-hosted ChatGPT environment** whenever the environment permits it. Provide actual PDF and generated evidence, identifiers needed to locate them, and the adjudication rubric, **without providing the initial verdict or score**. Different wording alone does not guarantee statistical independence; label this as a **procedurally independent challenge**, not proof of independent model errors.
3. Record the second verdict and full-predicate reasoning separately.
4. If the decisions agree and the supporting evidence is sufficient, close the case. If they disagree, conduct **at most one** targeted, evidence-based resolution assessment focused only on the disputed predicates.
5. After that, close the case: correct the score if evidence resolves it; otherwise use the declared conservative decision and explicit uncertainty. **Never iterate until agreement.**

No hard numerical limit is imposed on internal parsing, searching, Python checks, batching, or model calls needed to complete a phase. **The exceptional critical review process itself is bounded to one second assessment plus at most one targeted resolution per unique case/group**, and only the listed critical categories trigger it. Do not clone identical rechecks across every duplicate occurrence or repeat prior full phases. If a genuinely separate assessment is unavailable in the current environment, document `INDEPENDENT_CHALLENGE_UNAVAILABLE` and do not claim independent confirmation or `FINAL_VERIFIED` for that unresolved material case.

## 7. Six-turn execution plan

**One turn** means one user request followed by **one assistant response**. The assistant may use any reasonable number of internal tool calls, local scripts, batches, targeted model passes, and file operations **within that turn**. The user should never be asked to run tens of interactive turns, change to Codex, or manually execute an internal batch. A phase is complete only when its required output exists or a precisely reported input/technical blocker prevents completion. Ordinary semantic uncertainty must be recorded, not used to silently skip work.

| Turn | Full work package | Mandatory turn outputs |
| --- | --- | --- |
| **1 — Input freeze and generated occurrence extraction** | Read frozen `R` and `N`, original PDF, and all eight generated documents per selected method. Record input hashes and integrity, inspect all substantive generated lines/table cells, extract eligible definitive `GO_m`, and record excluded generated material. **No Gold Set verification or editing.** | `00_input_inventory.json`, `01_generated_occurrences.jsonl`, `01_generated_exclusions.jsonl`, `01_generated_coverage.json` |
| **2 — Generated classes and two duplicate types** | Normalize every eligible occurrence, form `GC_m`, classify every excess occurrence as `EXPECTED_REUSE` or `REDUNDANT_DUPLICATE`, preserve all provenance, and reconcile occurrence/class counts. | `02_generated_classes.jsonl`, `02_duplicate_occurrences.jsonl`, `02_duplicate_metrics.json` |
| **3 — Frozen-source coverage: TP and two FN categories** | Judge every frozen source-positive `r`, perform reciprocal eight-file retrieval for provisional FN, record every direct/bridged TP proof, and classify remaining FN as `TRUE_FN` or `UNCONFIRMED_FN`. Flag critical cases for Turn 5. Never alter `R`. | `03_source_coverage.jsonl`, `03_coverage_bridges.jsonl`, `03_fn_diagnostics.jsonl`, `03_source_confusion.json` |
| **4 — Generated correctness: FP, TN and class validity** | For every `GC_m`, check full PDF support; complete both passes of FP semantic consolidation, detect `B_m`, construct `F_m`, assign `TN` and `FP`, calculate a provisional GCVR, and flag critical cases. Do not amend `N`. | `04_generated_validity.jsonl`, `04_fp_clusters.jsonl`, `04_negative_control_judgments.jsonl`, `04_canonical_universe.jsonl`, `04_provisional_metrics.json` |
| **5 — Targeted independent review and reconciliation** | Independently challenge only critical decisions, close disagreements under the bounded rule, apply corrections to **judgments, FP clusters, duplicate classifications, and evidence links only**, and reconcile all rows. **Never modify the frozen Gold Set or controls.** | `05_critical_review.jsonl`, `05_judgment_changes.jsonl`, `05_reconciliation.json`; updated full copies of affected `02_duplicate_occurrences.jsonl`, `03_source_coverage.jsonl`, `03_fn_diagnostics.jsonl`, `04_generated_validity.jsonl`, `04_fp_clusters.jsonl`, and `04_canonical_universe.jsonl` in their original evaluation-output locations |
| **6 — Independent mechanical recomputation and delivery** | Recompute every metric from final item-level ledgers, recheck frozen hashes, total counts, FN split, both duplicate types, FP clustering, bounded TN, critical-review coverage, file existence and report limitations. Deliver individual files and comparison when scope includes multiple methods. | `06_metrics_final.json`, `06_metrics_final.md`, `06_coverage_and_limitations.md`, `compute_metrics.py`, and `06_comparison_final.json`/`.md` if applicable |

If a requested turn cannot finish because a mandatory input is missing or unreadable, return available **English** partial artifacts with `PHASE_TERMINATED_INPUT_BLOCKER`, state exactly what is inaccessible, and do not invent metrics. If inputs are accessible but semantic decisions are incomplete, complete the specified work package with itemized `BEST_EFFORT` judgments and quantified limitations rather than manufacturing verified certainty. There is no requirement to revisit the same phase repeatedly to make every ambiguity vanish.

## 8. Output data requirements

### 8.1 Provenance and schemas

Every **generated occurrence** must contain at least:

```json
{"method":"fullload","occurrence_id":"GEN-000001","file":"01_screen_functions.md","line_start":1,"line_end":1,"table_locator":null,"statement_en":"Illustrative definitive statement","eligibility":"DEFINITIVE"}
```

Every **generated semantic class** must contain a stable class ID, normalized proposition, predicate structure, all member occurrence IDs, and whether it has one or more PDF support/coverage bridges. Every **duplicate excess** record must contain `occurrence_id`, `class_id`, `representative_occurrence_id`, `duplicate_type`, `reason_en`, and genuine file/line evidence.

Every source-coverage record must contain `source_id`, `cell` (`TP` or `FN`), grade, PDF source citation, actual generated candidate locators, full-predicate applicability explanation, and **if FN**, exactly one `fn_type` (`TRUE_FN` or `UNCONFIRMED_FN`) with search evidence and unresolved predicates. Every E2 TP must additionally include explicit scope membership and any cross-file evidence links.

Every generated-validity record must contain `class_id`, one `pdf_support_status`, evidence locators, fully justified or missing predicate list, and links to zero or more source atoms and relevant FP clusters. Every canonical FP cluster must contain exactly one distinct residual proposition, a support subtype, proof of its cross-occurrence semantic merging, a list of source class IDs and generated occurrence IDs, and a flag showing whether the cluster belongs to `F_m` or is represented by `B_m` (never both).

Every critical review must retain original decision, blinded-review decision, evidence, exact disputed predicates, optional targeted resolution and final decision, plus evidence of how the initial verdict was excluded from the independent challenge. Never invent an independent reviewer, a separate model call, or a review trace that did not occur.

Illustrative rows in this section are **schemas, not actual OrionDesk findings**. Replace all placeholders with evidence from the actual supplied inputs when executing a phase.

### 8.2 A canonical scoring ledger

The final `04_canonical_universe.jsonl` must enumerate exactly one binary judgment per element of `U_m`:

- For each `r in R`: actual `1`; predicted `1` iff fully entailed (TP), otherwise predicted `0` (FN, with the required split).
- For each `n in N`: actual `0`; predicted `1` if asserted (FP), else predicted `0` (TN).
- For each distinct `f in F_m`: actual `0`, predicted `1` (FP), with canonical FP-cluster provenance.

There must be no overlap of canonical IDs, no double inclusion of an asserted negative control in `F_m`, and no duplication of one FP residual due only to repeated generated wording. The complete final ledger must be emitted after Turn 5 corrections; the earlier Turn 4 file may be marked provisional until reconciled.

### 8.3 Required results

For each method, report:

- `TP`, `TN`, `FP`, `FN`, `Precision`, `Recall`, `F1` and universe sizes.
- `FN_true`, `FN_unconfirmed`, the fraction of FNs unconfirmed, and strongest reasons for uncertainty.
- `GCVR`, `C_supported`, `C_invalid`, `C_uncertain`, `C_all`, with **nonstandard auxiliary metric** labeling.
- `Expected_reuse`, `Redundant_duplicate`, their separate rates, eligible occurrences, unique classes, and reconciliation.
- FP subtype counts, distinct FP clusters, negative-control assertions, and semantic merging corrections.
- Confirmed versus unresolved critical-review cases, coverage of mandatory evidence checks, actual limitations, and the read-only Gold Set hash.

Do not claim a higher GCVR proves higher source Recall or that a high precision implies zero omitted requirements. Report numerical comparisons only when reference version, method scope, evidence standard, and dataset are genuinely comparable.

## 9. Mechanical recomputation and audit gates

Write an English `compute_metrics.py` that recomputes the final values from emitted JSON/JSONL rather than copying a summary. The following checks are mandatory:

1. All required inputs are accounted for and the frozen R/N hashes equal the Turn 1 recorded values. No revised reference files are emitted.
2. `GO_m` occurrences each belong to exactly one `GC_m` class; no method cross-contamination occurs; every duplicate excess has exactly one of the two permitted types.
3. `Expected_reuse + Redundant_duplicate = |GO_m| - |GC_m|`, and both duplicate rates use **occurrences** as their denominator.
4. Every `R` ID has exactly one TP/FN judgment; every `N` ID has exactly one TN/FP judgment; every generated-only `F_m` ID has exactly one FP judgment.
5. `FN = FN_true + FN_unconfirmed`; no `UNCONFIRMED_FN` is quietly dropped from the confusion matrix.
6. Every TP has real proof evidence, every `TRUE_FN` has a completed reciprocal-search audit, and every `UNCONFIRMED_FN` has documented limitations rather than fabricated absence evidence.
7. No semantic duplicate remains among canonical FP clusters according to the completed equivalence audit; asserted negative controls are not also represented by `F_m`.
8. `FP = |F_m| + |B_m|`, `TN = |N| - |B_m|`, `TP + FN = |R|`, and the enumerated four-cell total equals `|U_m|`.
9. `C_all = C_supported + C_invalid + C_uncertain = |GC_m|`; GCVR is independently recomputed from the complete class ledger, not inferred from TP or FP.
10. Every flagged critical case has a recorded independent second assessment, one permitted resolution, or an explicit unavailable/unresolved status. No case/group was subjected to repetitive unbounded rechecks.
11. All output JSON/JSONL parses, each cited input-file locator exists, all authored deliverable text is English, and any output-vs-input paths are distinct.
12. Arithmetic checks are described as **structural**. They do not independently prove all semantic judgments or that the externally constructed Gold Set is complete.

### Permitted status labels

- `PHASE_COMPLETED_VERIFIED`: required phase outputs and semantic/evidence checks completed for that work package.
- `PHASE_COMPLETED_BEST_EFFORT`: work package closed with explicitly enumerated unresolved judgments and limitations.
- `PHASE_TERMINATED_INPUT_BLOCKER`: mandatory evidence was missing, corrupt, or unreadable.
- `FINAL_VERIFIED`: all six phases completed; all material semantic judgments and mandatory independent critical challenges are supported and closed.
- `FINAL_BEST_EFFORT`: all six phases completed with a complete canonical decision universe but some clearly disclosed unresolved semantic judgments.
- `RUN_INVALID_REFERENCE_CHANGED`: frozen reference bytes changed during evaluation; do not publish comparable final scores for that run.

**Do not** award `FINAL_VERIFIED` merely because algebra reconciles or because all expected output filenames exist. If critical review cannot be genuinely isolated, describe the limitation plainly rather than falsely claiming model independence.

## 10. Required artifact layout and delivery

All original input files remain unchanged. Write only **English-language evaluation artifacts** to a separate output directory. For multi-method evaluations, put shared input/hash metadata at the output root and method-scoped artifacts under `fullload/`, `onelevel/`, and `twolevel/` respectively. No `common_atomic_reqs.jsonl` or `common_negative_controls.jsonl` output copies, corrected ledgers, or Gold Set creation outputs are permitted.

```text
<evaluation-output>/
    00_reference_freeze.json
    fullload/                         # if selected
        00_input_inventory.json
        01_generated_occurrences.jsonl
        01_generated_exclusions.jsonl
        01_generated_coverage.json
        02_generated_classes.jsonl
        02_duplicate_occurrences.jsonl
        02_duplicate_metrics.json
        03_source_coverage.jsonl
        03_coverage_bridges.jsonl
        03_fn_diagnostics.jsonl
        03_source_confusion.json
        04_generated_validity.jsonl
        04_fp_clusters.jsonl
        04_negative_control_judgments.jsonl
        04_canonical_universe.jsonl
        04_provisional_metrics.json
        05_critical_review.jsonl
        05_judgment_changes.jsonl
        05_reconciliation.json
        06_metrics_final.json
        06_metrics_final.md
        06_coverage_and_limitations.md
        compute_metrics.py
    onelevel/                         # same per-method schema if selected
    twolevel/                         # same per-method schema if selected
    06_comparison_final.json          # only if two or more methods
    06_comparison_final.md            # only if two or more methods
```

For a single selected method, the same files may be placed directly under the output root provided their method identity is explicit. Deliver **individual files**, not a mandatory ZIP/TAR archive. A protocol-edit request creates **this protocol only**; it does not execute an evaluation phase.

## 11. Final binding instructions

**Build no Gold Set here. Validate no Gold Set completeness here. Change no Gold Set or negative-control item here.** Assume the externally supplied, frozen reference is comprehensive; use it unchanged for source coverage and denominator construction. Verify generated assertions against the PDF to prevent false FP determinations, not to reformulate the reference. Evaluate the complete eight-document generated corpus, collapse meaning-equivalent FP residuals once, report both `EXPECTED_REUSE` and `REDUNDANT_DUPLICATE`, retain the canonical Precision/Recall/F1 alongside the **new nonstandard GCVR**, count both `TRUE_FN` and `UNCONFIRMED_FN` in FN, and interpret TN only within fixed bounded negative controls.

Use no Codex workflow. Finish one named work package per request–response turn within a six-turn scope. Internal model/tool operations have **no numerical call cap**, but independence checks are limited to critical decisions and one fresh challenge plus at most one narrowly targeted resolution per case. Close ordinary uncertainty with traceable best-effort judgments rather than repetitive human interaction, unrecorded omissions, invented evidence, or unbounded review loops.
