# OrionDesk AI — Phase 6 Coverage, Provenance, and Limitations

**Protocol:** 6.1 — Six-Turn Semantic-Entailment Atomic Requirement Evaluation
**Phase:** 6 — Independent recomputation and individual delivery
**Method:** One unlabeled complete eight-document Markdown set
**Completion state:** `PHASE_COMPLETED_BEST_EFFORT`
**Semantic certification:** `NOT_CERTIFIED`

## 1. Final decision basis and input status

The authoritative source is the original English 90-physical-page `OrionDesk_AI_Detailed_Design_Specification(2).pdf` (document ID `OD-AI-DDS-001`, baseline `R1.0`, revision `1.3`). All source-positive requirements and predeclared negatives use this PDF. The eight scored input Markdown files are unchanged; the evaluation instruction file and the two user-supplied source ledgers are not scored generated specifications.

| Scored role | Actual unchanged input filename |
|---|---|
| 01 | `01_screen_functions(2).md` |
| 02 | `02_api(2).md` |
| 03 | `03_data(2).md` |
| 04 | `04_batch_functions(3).md` |
| 05 | `05_business_rules(8).md` |
| 06 | `06_exception_handling(20261114-124408).md` |
| 07 | `07_processing_flows(4).md` |
| 08 | `08_architecture_decision(3).md` |

- Original PDF physical pages: **90 / 90**, all text-readable; previously recorded visual page review spans **90 / 90**.
- Source-positive atoms: **979**; fixed source-negative controls: **37**.
- PDF pages carrying positive-source evidence: **76**; non-atom pages are primarily covers, table of contents, or illustration-only pages and are not assumed missing.
- PDF-positive evidence references: **2450**; negative-control evidence references: **37**.
- PDF-text evidence matches: **2484** of **2484** text-based references; **3** diagram labels on physical page 8 were separately verified visually.
- Original PDF SHA-256: `b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3` (matches the Phase-1 recorded file hash).
- Markdown physical-line census: **8330** rows, with **15945** table cells from the Phase-2 census; original files and every eligible occurrence locator were reopened.

## 2. Item-level canonical four-cell recomputation

| | Predicted positive | Predicted negative |
|---|---:|---:|
| Actual positive | TP = **647** | FN = **332** |
| Actual negative | FP = **0** | TN = **37** |

- `TP + FN = 647 + 332 = 979`.
- `TN + |B| = 37 + 0 = 37`.
- `FP = |F| + |B| = 0 + 0 = 0`.
- `|U| = |R| + |N| + |F| = 979 + 37 + 0 = 1016`.
- `|P| = TP + FP = 647`; this **must not be equated** with raw `|G| = 6851`.

- **Provisional precision:** `100.000000%`.
- **Provisional recall:** `66.087845%`.
- **Provisional F1:** `79.581796%`.

**Interpretation:** These rates are arithmetic over the currently adjudicated canonical propositions. Their numerical consistency is independently verified; their semantic truth has not been independently certified. In particular, zero identified FP is not demonstrated zero unsupported claims.

## 3. Source-coverage and false-negative audit

The final source inventory contains **979** source-positive requirements. **647** have complete-TP evidence records and **332** retain non-entailment/uncertainty dispositions. The original root-cause file retains **782** initially proposed FN rows, including later corrections.

| Final FN disposition | Items | Interpretation |
|---|---:|---|
| `PARTIAL_ENTAILMENT` | 185 | The strongest recovered generated evidence lacks at least one required source predicate. |
| `CONSERVATIVE_UNRESOLVED` | 142 | A complete match could not be proven after the bounded challenge; not a verified absence. |
| `TRUE_MISSING` | 5 | No complete match identified following actual reciprocal candidate search. |
| **Total** | **332** | Exactly one final root-cause disposition per remaining FN. |

Examples of the five `TRUE_MISSING` entries, useful for subsequent manual triage (these are *current ledger judgments*, not newly certified findings):

| Source ID | Source proposition, abbreviated |
|---|---|
| `PDF-00435` | Persistent data contracts enforce tenancy, revision safety, referential integrity and deletion semantics independent of AI behavior. |
| `PDF-00528` | Threats include cross-tenant IDOR, connector token exfiltration, prompt injection, malicious file parsing, tool argument forgery and approval replay. |
| `PDF-00940` | Threat T-07 (Message replay) must be mitigated by idempotency and aggregate-revision checks. |
| `PDF-00943` | Threat T-10 (Unbounded agent recursion) must be mitigated by tool, step and time budgets. |
| `PDF-00990` | Threat T-03 must be negatively verified by an exercise that will attempt to approve an earlier draft after its revision. |

**Corrections already applied:** 60 FN-to-TP recoveries in Phase 5, plus earlier Phase-3 recoveries recorded in their original audit. The Phase-6 operation **did not alter** any canonical label.

### Specific regression probes

| Regression probe | Located source IDs | Final ledger judgment | Check |
|---|---|---|---|
| `case_title_field` | `PDF-00208` | TP | PASS |
| `workspace_retention_class` | `PDF-00199` | TP | PASS |
| `case_idempotent_replay` | `PDF-00948` | TP | PASS |

These are diagnostic retrieval probes (title, workspace retention class, and repeated case creation with identical key); they are not preapproved TP labels.

## 4. TP proof evidence and semantic scope

- TP evidence audit records: **647** of **647**.
- Evidence grades: **E3 = 151** and **E2 = 496**.
- Each TP has reloaded Markdown quotation evidence, PDF evidence, a target/actor/action/condition/scope/timing/exception/outcome predicate-check record, and explicit scope-bridge or direct-match attribution.
- All TP audit records describe their semantic certainty as bounded best effort rather than independent expert certification. A recorded predicate check does not mechanically prove its logical correctness.
- One narrow high-risk `reviewed artifact`/hash-binding source candidate was conservatively left FN (**1 FN, 0 TP among the targeted search criterion**). This is a semantic investigation priority, not a proven missing publication guard.

## 5. Generated claims and FP reliability

| Generated-class validity ledger classification | Classes | Evidence-quality caveat |
|---|---:|---|
| `PDF_ENTAILED` | 1483 | Best-effort PDF support; not independently certified. |
| `SUPPORTED_NONCOVERING` | 5368 | Many class-to-PDF links are lexically weak or incomplete; labels must be challenged. |
| `PDF_UNSUPPORTED` identified | 0 | None was established with adequate evidence; **absence is not verified**. |

**3904 classes** have PDF support not established by lexical retrieval, making `FP=0` and the computed precision highly uncertain. An unresolved or proposed architecture decision is not an adopted generated implementation commitment. A generated statement with a narrower supported scope does not automatically become FP.

## 6. Source atomization, corrections and exclusions

- Source-atomization audit entries: **979**; retained **977** and retained after wording correction **2**.
- Phase 1 normalized 1,024 supplied source-positive records into 979 independent source atoms (42 repeated global validation records and 3 nonnormative summaries did not increase the denominator).
- Two Phase-5 edits corrected a PDF-wrapped `/members` API path and removed a sample sizing illustration from a normative source paraphrase; the common denominator remained 979.
- Phase-5 correction delta: **76** records: **60** FN-to-TP, **9** exclusions of unadopted proposals, **5** class merges, and **2** source wording/context edits.
- Consolidated excluded-unit ledger: **12600** records, including proposal, TBD, reference context, commentary, illustrations and duplicate/source-support exclusions (some exclusions are indexed at source occurrence/cell level, not as independent scoring units).

## 7. Raw semantic duplication

| Quantity | Value |
|---|---:|
| Eligible generated occurrences `GO` | 6929 |
| Unique raw generated classes `G` | 6851 |
| Excess occurrences | 78 |
| Within-file excess | 5 |
| Across-file excess | 73 |
| Repeated classes | 66 |
| Repeated classes spanning files | 63 |
| Duplicate rate | 1.125704% |

The duplicate partition was independently reconstructed from occurrences ordered by scored input file, physical line, and occurrence position. For a class, the first occurrence is the representative and every subsequent occurrence is partitioned as within-file or across-file. Paraphrase duplicates that were not firmly established retain separate classes; the calculated rate is not an exhaustive semantic-duplication rate.

## 8. Negative controls and bounded true negatives

The **37** fixed negative controls were constructed from explicit PDF prohibitions, exclusions or release deferrals, before generated corpus matching. None was identified as an affirmative generated commitment (**B = 0**), so **TN = 37**. This TN count is strictly a bounded diagnostic set, not a claim about every requirement the PDF does not state. Adding extra unasserted negatives would affect TN but not precision, recall or F1.

## 9. Independent verification checks

The executable `compute_metrics.py` passed **46 of 46** item-level structural and provenance checks (the full keyed checklist appears in `06_metrics_final.json`). It independently confirmed source/negative IDs, generated occurrence-to-class membership, canonical label parity, every TP/FN evidence quote line, real file names, all 90 PDF pages and directly extractable PDF text references, Phase-2 line/cell census, negative-control arithmetic, duplicate partitions, and method isolation.

### Verification boundaries and unresolved limitations

1. A text match is not a formal semantic-entailment proof. Full-predicate support must also be substantively evaluated by a reviewer.
2. A single source requirement may be covered by multiple generated passages; the raw class count is not an interchangeable prediction denominator.
3. The PDF is fully readable but three diagram labels on physical page 8 require visual inspection rather than raw PDF text search. Those labels were directly inspected in the phase-6 visual check.
4. Conservative FN, weakly supported generated classes, test-matrix overlap and alternative atomization can change apparent TP, FN, FP, or the denominator in a future **new** audit. This run is complete under the prescribed six phases and is not reopened here.
5. No second method was supplied and therefore no cross-method comparison files are required. No ZIP/TAR is created under the protocol archive prohibition.
6. Language compliance is applied to authored outputs: narrative records, report prose, headings and program comments are English. Original filenames and source quotations are preserved verbatim as provenance.

## 10. Reproduce this Phase-6 result

Run the following command from any working directory with the mounted original PDF and Markdown inputs:

```bash
python /mnt/data/orion_phase6/compute_metrics.py --ledger-dir /mnt/data/orion_phase6 --source-dir /mnt/data --output-dir /mnt/data/orion_phase6
```

The script reads the final item-level Phase-5 ledgers, recomputes all scores, and refreshes `06_metrics_final.json` and `06_metrics_final.md`; the Phase-5 ledgers remain unchanged. Individual deliverables are in the same directory. The outputs are not a semantic accuracy certificate.

## 11. Phase boundary and delivery result

**Phase 6 is complete with `PHASE_COMPLETED_BEST_EFFORT`.** No subsequent phase is defined by protocol 6.1. All listed artifacts are provided individually and no archive was generated.
