# OrionDesk AI — Phase 3 Semantic Source Coverage Audit

**Protocol:** v6.1
**Method:** eight supplied Markdown specifications (method designation not independently known).
**Status:** PHASE_COMPLETED_BEST_EFFORT

## Input and denominator preservation

- PDF-positive inventory: **1,024** unchanged source atoms.
- Fixed predeclared negative controls: **37** (assertion checks deferred to Phase 4).
- Original Phase-2 generated occurrence/class count: **2,523 / 2,475**.
- Corrected generated occurrence/class count: **2,672 / 2,624** (+149 table-cell eligibility corrections).
- The eight original generated Markdown documents were not changed.

## Source coverage (preliminary; not a four-cell matrix)

- Fully entailed by Phase-3 best-effort screening (TP): **621**.
- Not yet fully entailed under bounded conservative review (FN): **403**.
- Provisional positive coverage ratio: **60.64%** (not certified coverage).

## TP evidence modes

- `CONJUNCTIVE_BRIDGE`: 94.
- `DIRECT_EQUIVALENCE`: 81.
- `INHERITED_CONTEXT`: 196.
- `SEMANTIC_EQUIVALENCE`: 175.
- `UNIVERSAL_INSTANTIATION`: 75.

## FN root-cause dispositions

- `CONSERVATIVE_UNRESOLVED`: 213.
- `MATCHER_FALSE_NEGATIVE_CORRECTED`: 196.
- `PARTIAL_ENTAILMENT`: 79.
- `TRUE_MISSING`: 111.

**Reciprocal false-negative corrections:** 196 source atoms explicitly promoted to TP after direct contextual acceptance-test, DDL, schema, domain-field and cross-file verification. The original candidate FN entries remain in the FN audit as corrected history.
## Key eligibility correction

The prior line/cell classifier incorrectly excluded standalone confirmed selected relational fields, DDL key/foreign-key constraints, public API authorization cells, and primary-screen names as nondefinitive. Their meanings follow directly from a row name, column header and confirmed section context. These must not be classified as absent in the user-supplied eight-document corpus. All 149 corrected occurrences retain their actual original line and cell and new class/occurrence IDs; the original Phase-2 ledgers remain unchanged for reproducibility.

## Structural and semantic evidence gate

- **Structural verification:** PASSED (source IDs, generated class references, real original-file quotes, binary positive judgments, FN dispositions and reciprocal correction counts).
- **Semantic evidence certification:** NOT CERTIFIED; classification is bounded best effort and is not a full independent human predicate review.
- **Phase 1 source hashes:** exact byte-for-byte matches to the fullload_cal source-atom and negative-control references.
- **No Phase-4 correctness decisions:** 37 negative-control prediction statuses and generated-only FP remain pending.

## Retrieval and semantic limitations

Source-to-generated candidate ranking combines token and character similarity. Inverse exact-identifier, field, event, test, endpoint and inherited-table-context inspection supplements the ranking. Matched items record their specific real quotes, source page, generated file, physical line and table-cell locator. Every remaining FN has a candidate evidence record and a concrete full-predicate gap or conservative unresolved reason. Mechanical checks can detect obvious equality and schema defects; they do not prove the semantic correctness of every non-literal bridge.

Generative claims outside the PDF, negative-control assertion decisions and the FP/TN calculation are the independent work of Phase 4; no Precision, F1 or conventional four-cell estimate is claimed in this phase.

## Outputs

- `03_canonical_universe_final.jsonl` — positive source decisions and fixed negative controls with Phase-4 status pending.
- `03_evidence_matches_final.jsonl` — full TP/FN source coverage with references, predicate checks and bounded adjudications.
- `03_semantic_coverage_bridges_final.jsonl` — evidenced non-direct source coverage.
- `03_fn_root_cause_audit_final.jsonl` — every provisional/final FN and reciprocal retrieval evidence.
- `03_candidate_retrieval_final.jsonl` — directional candidate search and inverse-index diagnostics.
- `03_generated_inventory_corrections_final.jsonl` — confirmed omitted generated source cells.
- `03_reciprocal_corrections_final.jsonl` — item-level initial-FN corrections with original evidence.
- `02_generated_atoms_corrected_phase3.jsonl` and `02_generated_classes_corrected_phase3.jsonl` — downstream-corrected generated inventory.
- `03_phase_status_final.json` — item counts and limitations.
- `03_structural_and_semantic_gate_final.json` — independently rechecked Phase-3 structural and evidence gate.

## Source-category coverage, not certified

| Source evidence kind | TP | FN |
|---|---:|---:|
| A2A_FIELD | 8 | 0 |
| ACCEPTANCE_TEST | 16 | 0 |
| API_ACTOR | 15 | 0 |
| API_BEHAVIOR | 11 | 6 |
| API_METHOD_PATH | 15 | 0 |
| API_STATUS | 15 | 0 |
| BOUNDARY_CONTEXT | 5 | 0 |
| COMPONENT_CONTRACT | 0 | 110 |
| CONTRACT_GOVERNANCE | 0 | 2 |
| CROSS_CUTTING_CHECKPOINT | 0 | 2 |
| CROSS_CUTTING_FAILURE | 5 | 0 |
| CROSS_CUTTING_SAFETY | 1 | 0 |
| CROSS_CUTTING_TEST | 0 | 7 |
| DATA_CONSTRAINT | 7 | 11 |
| DATA_FIELD | 80 | 0 |
| DDL_CHECK_OR_DEFAULT | 5 | 0 |
| DDL_FK | 2 | 0 |
| DDL_KEY | 2 | 0 |
| DDL_NULL | 7 | 0 |
| DDL_RLS | 2 | 0 |
| DDL_TYPE | 8 | 0 |
| DESIGN_GOVERNANCE | 0 | 1 |
| DOMAIN_FIELD | 13 | 0 |
| ERROR_CONTRACT | 6 | 0 |
| EVENT_CONTRACT | 24 | 0 |
| EVENT_VERIFICATION | 0 | 44 |
| INDEPENDENT_CONTRACT_FIELD | 17 | 0 |
| INTERFACE_VALIDATION | 43 | 0 |
| MCP_CONTRACT | 9 | 0 |
| NORMATIVE_FIGURE | 0 | 3 |
| NORMATIVE_INVARIANT | 20 | 2 |
| NORMATIVE_PROSE | 144 | 197 |
| NORMATIVE_TEXT | 1 | 0 |
| PRIMARY_SCREEN | 8 | 0 |
| REGISTER_API | 68 | 0 |
| REGISTER_EVENT | 29 | 15 |
| RUNBOOK | 5 | 1 |
| SECURITY_NEGATIVE_TEST | 12 | 0 |
| SECURITY_VERIFICATION | 10 | 2 |
| STATE_CATALOG | 8 | 0 |
