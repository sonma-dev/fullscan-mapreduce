# Phase 3 — Revised Semantic Coverage and Limitations

**Protocol:** 6.1. **Status:** `PHASE_COMPLETED_BEST_EFFORT`. **Method:** `current_scored_8`.

## Inputs and verified identity
The authoritative PDF has 90 physical pages and is SHA-256-identical to the previous `fullload_cal` source (b71541e74564559d2cc0a84e9827086946998fbc6c627488fb9e7a7f9b0137c3). The eight unchanged supplied Markdown files contain 3123 lines. Phase 2 retains 3265 definitive generated occurrences and 3168 raw semantic classes.

## Common PDF source atomization correction
The original positive source inventory contained 1024 units; 8 standalone field-name obligations derived solely from an illustrative A2A JSON envelope in Appendix C.2 were removed. The revised common source inventory has 1016 positive units. The negative-control inventory is unchanged at 37.
Removed IDs: PDF-00915, PDF-00916, PDF-00917, PDF-00918, PDF-00919, PDF-00920, PDF-00921, PDF-00922. The exact PDF quotation, old ID, scope rationale and across-method application are preserved in `03_source_atomization_delta.jsonl` and `07_change_delta.jsonl`. No original Phase 1 or Phase 2 input was overwritten.
All 1024 old source items received a preliminary nearest-neighbor and independent-target source-atomization challenge in `03_source_atomization_review_preliminary.jsonl`. High lexical similarity does not prove a duplicate when the resource, endpoint, field, status, or test obligation differs. Full independent source split/merge review is reserved for Phase 5.

## Mandatory reciprocal challenge of all originally missed source duties
| Initial FN candidate disposition | Items |
|---|---:|
| `MATCHER_FALSE_NEGATIVE_CORRECTED` | 301 |
| `SOURCE_ATOMIZATION_ERROR_CORRECTED` | 5 |
| `PARTIAL_ENTAILMENT` | 6 |
| `CONSERVATIVE_UNRESOLVED` | 7 |
| `TRUE_MISSING` | 0 |
| **Total** | **319** |

Every original FN candidate has PDF source evidence, actual generated-file/line candidates, exact/alias key-search records, a reverse and contextual full-corpus review disposition, and a final scoring cell in `03_fn_root_cause_audit_final.jsonl`.

## Current source-side judgments — provisional, not independently certified
| Item | Count |
|---|---:|
| TP | 1003 |
| FN | 13 |
| E3 direct/equivalent | 410 |
| E2 contextual/universal/conjunctive | 593 |
| Revised source positives | 1016 |

Provisional arithmetic Recall = 1003/1016 = 0.987205 (98.72%). The prior v6.0 source-side results (705 TP, 319 FN) are superseded, not reused as labels. A provisional high Recall is **not proof** of semantically certified specification completeness.

## Remaining FN entries
| Source ID | Unproved or partially covered PDF requirement |
|---|---|
| PDF-00005 | The primary deployment profile provides stateless HTTP APIs. |
| PDF-00078 | An AI run becomes terminal within the configured maximum or yields a recoverable timeout state. |
| PDF-00091 | The system has a web client, an edge API, domain services, an orchestration tier, a controlled model gateway, a search subsystem, asynchronous workers and external enterprise connectors. |
| PDF-00094 | Connector workers exchange service credentials with document providers. |
| PDF-00130 | Production runs in a private cloud network with independent web, API, worker and data subnets |
| PDF-00134 | Workers use NAT-controlled egress to explicit model and connector endpoints. |
| PDF-00150 | Each environment uses the same container images and deployment templates with different isolated secrets and quotas. |
| PDF-00279 | Headings and reading order inform chunk boundaries. |
| PDF-00357 | Approved MCP servers expose typed retrieval and business functions through scoped service credentials. |
| PDF-00468 | Public APIs use /v1 nouns, cursor pagination, RFC 3339 timestamps and stable snake-case error codes. |
| PDF-00613 | Terraform or Bicep declares network, managed identity, databases, storage, queues, search, monitoring and secret-vault bindings. |
| PDF-00614 | Shared modules expose only documented inputs and outputs. |
| PDF-00964 | All identities, cases, documents and provider replies in this specification are synthetic. |

Remaining FN records distinguish incomplete/generated support from semantic ambiguity. Absence is not universally verified merely because no complete bridge was proven.

## TP predicate evidence audit
All 1003 final provisional TP items have a corresponding item-level best-effort TP predicate review in `03_tp_predicate_review_provisional.jsonl`; 593 E2 records have real PDF and generated quotation locators, plus scope/predicate review notes in `03_semantic_coverage_bridges_final.jsonl`.
Checks reference target, actor, action, scope, condition, timing, version, constraint, exception, and outcome when applicable. Actual raw input lines were checked against the stored generated evidence. They are not yet a semantically certified independent human audit. Source fields and exact DDL literals can be complete despite low bag-of-words similarity.

## What has not been scored
Draft Phase 3 canonical units: 1053 = 1016 PDF-positive units + 37 fixed negative controls. Phase 4 must independently verify each generated class and discover generated-only unsupported propositions F and asserted negative controls B. TN, FP, Precision and F1 are deliberately not computed in this phase.

## Reliability warnings
1. Semantic candidate retrieval combined exact structural keys, word/character similarity, context-aware table extraction, cross-file conjunction, raw Markdown line citations and generated-to-source reverse checks. Text similarity is a retrieval aid, not a proof of logical entailment.
2. Source-atomization scrutiny included example status and high-similarity independent fields/endpoints, but another substantive Phase 5 source test/parent/child deduplication audit remains mandatory.
3. Several retained TP judgments rely on best-effort contextual interpretation. Any unproved actor, condition, exception, outcome or constraint must be corrected in Phase 5 rather than silently treating high computed Recall as ground truth.
4. The revised source-positive inventory is common to all methods evaluated against this exact PDF. No method-specific denominator changes are permitted.
5. All authored deliverables are English; no ZIP/TAR/archive was created. Phase 4 has not begun.
