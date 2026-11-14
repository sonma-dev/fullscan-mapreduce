# Phase 1 — Independent Source Extraction and Fixed Negative Controls

**Status:** `PHASE_COMPLETED_BEST_EFFORT`
**Reference:** `OrionDesk_AI_Detailed_Design_Specification.pdf` — `OD-AI-DDS-001` (`R1.0`, revision `1.3`).
**Physical pages:** 90; inspected 90; PDF text readable on all pages.
**Source-positive atomic propositions (R):** 1024.
**Fixed source-negative controls (N):** 37.
**Excluded PDF text items:** 274.
**Raster-image pages visually reviewed:** 31 (pages 7, 8, 11, 14, 15, 18, 21, 24, 27, 30, 33, 34, 37, 40, 43, 44, 47, 48, 51, 54, 57, 60, 61, 64, 67, 68, 71, 74, 77, 78, 81).

## Input verification
All eight scored Markdown roles are present and mapped unambiguously. Their contents are explicitly reserved for Phase 2 and have not been used as source-evidence or to construct negative controls.

| Role | Actual filename | Available | Bytes |
|---|---|---|---:|
| 01 | `01_screen_functions.md` | Yes | 55572 |
| 02 | `02_api.md` | Yes | 76224 |
| 03 | `03_data.md` | Yes | 58905 |
| 04 | `04_batch_functions.md` | Yes | 58145 |
| 05 | `05_business_rules.md` | Yes | 53356 |
| 06 | `06_exception_handling(1).md` | Yes | 55820 |
| 07 | `07_processing_flows(1).md` | Yes | 62995 |
| 08 | `08_architecture_decision.md` | Yes | 63755 |

## Independent PDF coverage
The page-level JSONL enumerates all 90 physical pages, extracted text and inspected figure presence. The title, contents pages, reference UI images, chapters 1–22, API catalog, data schema/DDL, event/tool protocols, threat matrix, test matrix, and configuration/runbook appendix were inspected.

### Chapter entry pages

- Page 8: 01 Document Control and Design Baseline
- Page 11: 02 Product Scope and User Journeys
- Page 15: 03 System Context and Container Architecture
- Page 18: 04 Runtime Deployment Topology
- Page 21: 05 Identity, Tenancy and Authorization
- Page 24: 06 Workspace and Case Domain Model
- Page 27: 07 Connector Management and Source Sync
- Page 30: 08 Document Extraction and Normalization
- Page 34: 09 Search Index and Grounded Retrieval
- Page 37: 10 Model Gateway and Prompt Lifecycle
- Page 40: 11 Agent Orchestration and Tool Access
- Page 44: 12 Policy Decisions and Human Approval
- Page 48: 13 Workflow, Queues and Event Semantics
- Page 51: 14 Relational Data and Object Storage Design
- Page 54: 15 Public API and Internal RPC Contracts
- Page 57: 16 User Interface, Accessibility and Interaction
- Page 61: 17 Application Security and Data Governance
- Page 64: 18 Observability, Cost and Service Reliability
- Page 68: 19 Performance, Capacity and Resilience
- Page 71: 20 Deployment, Configuration and Release Engineering
- Page 74: 21 Test Strategy and Quality Evaluation
- Page 78: 22 Operations, Migration and Runbooks

## Positive-inventory method

The authoritative source is the PDF alone. Requirements are normalized as independently meaningful testable design or behavioral propositions. Explicit SQL column type, nullability, keys, defaults, foreign keys, and checks are separate when independently testable. The appendix API register preserves distinct endpoint path, role, success result and behavior propositions. Chapter interface fields, event-visibility assertions, chapter contracts, and failure controls are independently enumerated where they refer to different targets. Boilerplate assertions repeated across chapters are consolidated into one shared proposition per applicable rule, rather than multiplied by their repeated printed frequency.

The image-based chapter figures were reviewed for constraints not present in selectable text; their repeating cross-cutting runtime assertions are represented once using Figure 1.1 visual evidence. Reference UI sample counts, fictional names, and configuration examples are not treated as product defaults. Parent descriptions that merely summarize separately enumerated child obligations are not artificially doubled.

## Predeclared negative-control construction

The negative inventory was constructed solely from explicit PDF exclusions/non-goals, R1 release deferrals and independently prohibited behaviors. Each item is an affirmative counterfactual, with an exact English PDF quote and a physical page. A single canonical counterfactual is retained per distinct prohibited capability, even when the prohibition is repeated elsewhere. The bounded negative inventory does not represent every logically possible false requirement. It will be fixed across all methods.

## Structural verification

- 90 / 90 pages yielded readable extracted text.
- 31 image-bearing pages were inspected using rendered contact sheets; all page images were accessible.
- 1024 distinct `PDF-*` IDs; 37 distinct `NEG-*` IDs.
- All text-backed positive and negative evidence quotations were checked against the physical-page extracted text after whitespace normalization.
- No generated Markdown assertions, aggregate JSON, previous goldsets or previous scores were consulted.
- No TP, TN, FP, FN, Precision, Recall, F1 or Duplicate values are calculated in this phase.

## Evidence-grade limitation and bounded adjudication

This phase is complete at the declared BEST_EFFORT standard, not full semantic certification. The extraction uses deterministic parsing of PDF headings, paragraphs, appendix tables and DDL plus limited manual inspection of normative raster diagrams. Complex long sentences remain conservatively bundled where a split would risk changing modality or scope. Named record-type metadata clauses in chapter boundary templates were retained per distinct target as directly testable, but repeated identical target requirements were merged. The fixed source inventory must not be manipulated to help any particular generated method; the protocol allows legitimate, method-independent corrections only at the designated correction phase.

## Files

- `01_source_atoms_final.jsonl`: item-level PDF-positive inventory and exact source evidence.
- `01_source_negative_controls_final.jsonl`: fixed, PDF-grounded negative controls.
- `01_pdf_page_coverage_final.jsonl`: physical-page inspection and inclusion/exclusion coverage.
- `09_excluded_units.jsonl`: source exclusions, examples, headings and nonnormative material.
- `01_phase_status_final.json`: machine-readable scope, counts and limitations.

**Phase gate:** Phase 1 is closed. Phase 2 has not started.
