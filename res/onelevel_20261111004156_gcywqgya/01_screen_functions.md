# 1. Screen Function Specification

## Scope and Users

### Baseline and interpretation

This file, `01_screen_functions.md`, specifies the browser screen functions of **OrionDesk AI**, document `OD-AI-DDS-001`, release `R1.0`, design revision `1.3`. **Confirmed** means confirmed requirements of the fictional reference design, not evidence of a deployed product. Source: `1794325316-OrionDesk_AI_Detailed_Design_Specification.pdf`, p.1 [screen_functions:r1:c1:f1–f3], p.8 [screen_functions:r1:c4:f1]. The source explicitly states: “All numbers are design assumptions, not measured production performance.” (p.2 [screen_functions:r1:c2:f1]).

All citations below refer to that exact source filename and original page numbers; bracketed finding IDs link to the retained evidence ledger. Screen and SF identifiers are assigned in this specification for traceability, not claimed as source identifiers. **Needs confirmation** is an unresolved implementation requirement, not permission for the implementation AI to choose. No design proposals or browser defaults are approved by this file.

### SF-001 Business scope

**Confirmed:** Users submit cases, ingest enterprise documents, search permitted knowledge, evaluate evidence, request grounded drafts, review uncertain or sensitive recommendations and publish only through deterministic policy gates. Retrieval, generation, policy evaluation and reviewer decisions are separate records. A final reply requires required evidence and satisfaction of approval policy. (pp.7, 11–12 [screen_functions:r1:c3:f1, screen_functions:r1:c5:f1, screen_functions:r1:c5:f9]).

**Out of scope:** Physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing and agent administrative cloud permissions are explicitly excluded. Application-hosted GPU inference is excluded. Cross-region active/active mutation, OCR beyond English and customer-managed model weights are deferred. (pp.9–10, 19 [screen_functions:r1:c4:f5–f6, screen_functions:r1:c7:f6]). These exclusions do not exclude ordinary manual case operations or approved, separately authorized business tools.

### SF-002 Users and permission prerequisites

| User or scope term | Confirmed activity or restriction | Open mapping |
|---|---|---|
| Analyst | Opens cases, evaluates evidence, requests grounded drafts; attachment and run initiation have Analyst scope | Full screen/action matrix unspecified |
| Reviewer | Approves/rejects recommendations; reads authorized cases and run metadata; decisions bind reviewed hash | Reviewer pool and minimum role are policy-defined |
| Workspace Admin | Manages connectors and policy | Map to baseline `Admin`; not yet explicitly equated |
| Admin | Connector sync, usage and evaluation API scope; export/delete require `Admin + approver` | Policy-setting action scopes and approver mapping unspecified |
| Auditor | Reads immutable evidence, decision metadata, prompt-template digests and access events under redacted scope; cannot edit case content; audit API scope | Complete screen visibility and redaction rules unspecified |
| Service | Baseline noninteractive role | Not a browser persona |
| Owner | Case PATCH scope | Resource ownership predicate, not a newly invented role |
| Member | Search API scope | Membership-to-baseline-role mapping unspecified |
| approver | Additional export/delete scope | Eligibility and independent approval procedure unspecified |
| Operators | Credential revocation, historical decision query and recovery procedures appear in source | Application role mapping and browser exposure unspecified |

Sources: p.11 [screen_functions:r1:c5:f3–f5], p.22 [screen_functions:r1:c8:f5], pp.45–46 [screen_functions:r1:c15:f4, screen_functions:r1:c15:f8], pp.27, 62 [screen_functions:r1:c10:f4, screen_functions:r1:c20:f10], p.83 [screen_functions:r1:c26:f6–f17]. Engineering audiences and contract-owning teams are not application roles (pp.8, 15 [screen_functions:r1:c4:f3, screen_functions:r1:c6:f8]).

**Confirmed:** Authorization combines role, tenant, workspace membership, case sensitivity, document ACL, requested action and segregation of duties. Every request binds an authenticated principal and tenant. Resource-boundary checks apply independently of hidden or disabled controls; domain checks run again within transactions and document ACL filtering precedes model text release. Approval tasks prohibit self approval; specifically, an analyst cannot approve their own high-risk recommendation. Authorized overrides require elevated role, a secondary reviewer and audited reason. (pp.11, 21–23, 46, 85 [screen_functions:r1:c5:f4, screen_functions:r1:c8:f1–f6, screen_functions:r1:c15:f8, screen_functions:r1:c27:f4]).

**Needs confirmation — OQ-001:** Define the complete screen/action/field permission matrix and the mappings above. Do not grant all functions to a role merely because it appears in the inventory.

### SF-003 Session and resource prerequisites

**Confirmed:** Interactive authentication uses OIDC authorization-code flow with PKCE. Tokens carry issuer, audience, expiry, subject and tenant; the gateway rejects unexpected algorithms or absent tenancy claims. Never store long-lived refresh tokens in browser local storage. A backend-for-frontend issuing secure, HttpOnly, SameSite cookies is permitted, not selected. Service credentials do not appear in traces or prompts. (pp.15, 21 [screen_functions:r1:c6:f3, screen_functions:r1:c8:f3–f4]).

**Confirmed:** Foreign-tenant ID substitution returns the same class of not-found response as an absent ID, without private existence disclosure. RLS tenant context, immutable signed background-job tenancy, transaction-scoped pool reset and additional workspace-tenancy enforcement are required. (pp.22–23, 86 [screen_functions:r1:c8:f8–f9, screen_functions:r1:c27:f7]).

**Needs confirmation — OQ-002:** Identity provider, login/logout/expiry/reauthentication interaction, session lifetime, BFF choice and workspace-selection UI are not defined. Do not invent a Login or Workspace Selector screen.

## Screen Inventory and Navigation

### Confirmed inventory

The source explicitly says: “The application contains Case Queue, Case Detail, Evidence Viewer, Run Timeline, Review Inbox, Connector Health, Policy Settings and Audit Explorer.” Each screen has **one primary action and a clear status summary**. (p.57 §16.1.1 [screen_functions:r1:c19:f2]). Screen purposes below distinguish direct screen evidence from associated domain activity.

| ID | Confirmed name | Purpose and associated activities | Users and display conditions | Origins, destinations and launch method |
|---|---|---|---|---|
| SCR-001 | Case Queue | Navigable case workspace/list context; exact prioritization controls unspecified | Analyst workspace activity supported; other screen entitlements need OQ-001; authenticated authorized scope | Browser screen confirmed; route, launch, row navigation and return path need OQ-003 |
| SCR-002 | Case Detail | Case context, revisioned business data, evidence and grounded-resolution work | Analyst/Reviewer authorized current-case read; Owner edit scope unresolved | Citation click-through opens source; specific case route and screen destinations need OQ-003 |
| SCR-003 | Evidence Viewer | Provenance-first evidence inspection and source document access | Permitted documents only; reviewers must be able to inspect evidence before approval | Citation click opens source and highlights anchored page range; whether viewer is embedded, separate route or window needs OQ-003 |
| SCR-004 | Run Timeline | Human-visible execution trace and retrieval/generation/policy progress | Analyst/Reviewer run and SSE scopes; authorized run only | Run creation leads to SSE subscription; refresh reconstructs server progress; route and origin need OQ-003 |
| SCR-005 | Review Inbox | Review assignments, exact candidate/evidence inspection and approval/rejection | Eligible Reviewer under pool, minimum-role, hash and separation-of-duty guards | Queue and decision integrations confirmed; task-opening route, return and postdecision destinations need OQ-003 |
| SCR-006 | Connector Health | Connector/source synchronization context and required health/trust warnings | Workspace Admin connector activity; Admin sync scope; Operators mapping unresolved | Browser screen confirmed; sync launch control, reauthorization path and navigation need OQ-003 |
| SCR-007 | Policy Settings | Policy administration context | Workspace Admin activity supported; exact Admin action predicates unresolved | No confirmed route, save control or destination; OQ-003/OQ-011 |
| SCR-008 | Audit Explorer | Immutable, scope-redacted decision/access lineage | Auditor audit scope; operator historical-query scope needs mapping | Cursor-paginated audit integration; screen launch, row details and export links need OQ-003 |

Sources: pp.11–12, 24–29, 40–46, 57–59, 62, 83 [screen_functions:r1:c5:f3–f9, screen_functions:r1:c9:f1–f9, screen_functions:r1:c10:f1–f10, screen_functions:r1:c14:f1, screen_functions:r1:c15:f4–f9, screen_functions:r1:c19:f1–f6, screen_functions:r1:c20:f10, screen_functions:r1:c26:f7–f15]. Domain activity is confirmed; its precise placement into a screen is Needs confirmation unless Chapter 16 states the placement.

### SF-004 Navigation and representative-view qualification

**Confirmed:** Citation click-through opens the source document and highlights its anchored page range. Reviewer evidence access is a prerequisite to approval, not merely a decorative link. (pp.57–58 [screen_functions:r1:c19:f1, screen_functions:r1:c19:f4, screen_functions:r1:c19:f6]).

**Needs confirmation — OQ-003:** Define routes, deep links, launch methods, origins/destinations, back/return behavior, task selection, row click behavior and each screen's primary action. Browser components `ViewState`, `ReviewForm`, `EvidencePanel` and `Notification` are not additional screens; their generic contract classifications do not establish form editability. Logical diagrams throughout the document depict components/contracts, not screen navigation. (pp.57–59 [screen_functions:r1:c19:f13, screen_functions:r1:c19:f18]).

Representative views on pp.7, 14, 33, 43, 47, 60, 67, 77 and 81 use the sidebar labels `Overview`, `Case Queue`, `Case Detail`, `Evidence Viewer`, `Agent Runs`, `Review Inbox`, `Connectors`, `Audit Events`, `Usage & Quality`. These do **not** confirm extra screens or aliases. `Agent Runs`→Run Timeline, `Connectors`→Connector Health and `Audit Events`→Audit Explorer are unapproved mappings. Titles include `Case Detail / Resolution Package`, `Case Queue / Risk Prioritization`, `Evidence Explorer / Citation Audit`, `Agent Run / Execution Trace`, `Approval Inbox / Binding Decision`, `Connector Health / Synchronization`, `Audit Explorer / Event Lineage`, and `AI Quality / Evaluation Scorecard`. Selected navigation often disagrees with the title: respectively Case Queue, Overview, Case Queue, Case Detail, Evidence Viewer, Agent Runs, Review Inbox, Connectors and Audit Events. (Relevant screenshot findings: screen_functions:r1:c3:f6–f10, screen_functions:r1:c5:f20–f24, screen_functions:r1:c11:f16–f19, screen_functions:r1:c14:f16–f18, screen_functions:r1:c15:f16–f17, screen_functions:r1:c19:f19–f22, screen_functions:r1:c21:f14–f16, screen_functions:r1:c24:f13–f16, screen_functions:r1:c25:f14–f15).

**Needs confirmation — OQ-004:** Resolve these labels and selected-item/title mismatches without creating Overview, Usage & Quality, evaluation, export, deletion, provisioning, hold, release or recovery screens solely from backend contracts or representative titles.

## Functions by Screen

### Shared field-definition convention

The tables below preserve known meanings and conditions without inventing schemas. Unless a row explicitly says otherwise, **type, length, format, requiredness, initial browser value, editability, client validation timing, visibility conditions and selectable-value source are Needs confirmation**. This convention applies separately to every listed field, including each member of grouped rows. A stored field or response attribute is not automatically a displayed/input field. Database defaults are identified as such and must not silently become form defaults.

### SF-005 Shared presentation and safety

| Display or input | Confirmed meaning/type/format/values | Requiredness, initial value, editability and constraints | Timing, visibility and source |
|---|---|---|---|
| Screen status summary | Every primary screen has a clear status summary | Required screen presentation; exact contents/defaults need confirmation | Scope-appropriate; update cadence unspecified |
| AI draft status | Accessible text `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` | Styling cannot replace text; server-derived, not a user-authorized status choice | Display with AI drafts; mapping to case/run/review states needs OQ-008 |
| Displayed timestamps | Workspace-local time with timezone label; server UTC; API RFC 3339 | Locale changes presentation only, not ordering/durable representation | Timezone/locale source and precision need OQ-005 |
| Locale selection | Presentation changes only | Control placement, supported locales and initial value unspecified | Never changes event order or API representation |
| Error code/details | Stable, non-sensitive codes and safe structured details | No credentials, full prompts, retrieved documents or unauthorized resource existence | Failure presentation/placement needs OQ-006 |
| Source citation | Opaque verified identifier linked to immutable source anchors | Verify before display; current document access required | Click opens source/anchored page highlight |

Sources: pp.13, 35, 54, 57–59, 84 [screen_functions:r1:c5:f12, screen_functions:r1:c12:f7, screen_functions:r1:c18:f3, screen_functions:r1:c19:f2–f4, screen_functions:r1:c19:f8, screen_functions:r1:c26:f19].

**Confirmed:** All controls target WCAG 2.2 AA behavior, visible focus, semantic regions and robust keyboard ordering. Live updates announce only meaningful state transitions. Keyboard-only case opening must have no blocked action and visible focus (`TST-011`). (pp.58, 89 [screen_functions:r1:c19:f7, screen_functions:r1:c30:f11]). **Needs confirmation — OQ-005:** Detailed responsive layout, focus restoration, locale options, number formatting and specific accessibility test procedures are not supplied.

**Confirmed:** Untrusted retrieved documents and model responses cannot authorize tools, alter tenancy/approvals or bypass versioned deterministic policy. The browser never submits arbitrary tool definitions. Model output is data, not authority. Evidence is delimited/provenance-bearing and planner tools allowlisted/schema-pinned. (pp.7, 37–42, 61 [screen_functions:r1:c3:f2–f4, screen_functions:r1:c13:f1, screen_functions:r1:c13:f6, screen_functions:r1:c13:f10, screen_functions:r1:c14:f7–f11, screen_functions:r1:c20:f3]). Browser delimiter rendering versus model-context delimiting remains OQ-005.

### SCR-001 Case Queue

#### Fields and lists

| Field/list | Confirmed evidence | Attributes and constraints |
|---|---|---|
| Authorized case list | `GET /v1/cases?cursor=...` is a Chapter 16 UI contract; public APIs use cursor pagination | Cursor schema, page size, ordering, selectable filters, search field, totals and list columns need OQ-007 |
| Case identifier, subject/description, textual status | Representative `CASE EVIDENCE & WORKFLOW` rows illustrate these three outputs | Illustrative only; ID pattern and status enum cannot be inferred from screenshot |
| Workspace and tenant/release context | Representative shell shows workspace context and `fictional tenant / R1.0` | Field placement, server source, visibility and switching mechanism unconfirmed |
| `OPEN CASES`, `AWAITING REVIEW`, `EVIDENCE COVERAGE`, `SERVICE STATE` | Representative summary cards | Not confirmed required metrics; units/calculation/freshness/defaults need OQ-007 |

Sources: pp.57, 59 [screen_functions:r1:c19:f10, screen_functions:r1:c19:f14], representative evidence pp.7, 14, 33, 60 [screen_functions:r1:c3:f8–f9, screen_functions:r1:c5:f22–f23, screen_functions:r1:c11:f17–f18, screen_functions:r1:c19:f20–f21].

The representative cards show `128`, `14`, `97.6%`, `Healthy`, and rows `OD-2026-1042` through `OD-2026-1038`, with `Needs review`, `In progress`, `Published`, `Evidence gap`, `Triaged`. Subjects include `Supply chain response discrepancy`, `Batch quality deviation`, `Service contract inquiry`, `Customs document mismatch`, and `Supplier invoice reconciliation`; p.60 instead shows `Supplier invoice reconciliation`. These are fictional records, not initial values, production ID formats, enum catalogs, sort requirements or measured metrics.

#### Events and operation placement

1. **Confirmed domain action:** An Analyst creates a case using `POST /v1/cases` with an idempotency key; valid creation returns `201` and case identifier, and the case begins `NEW`. (pp.12, 83 [screen_functions:r1:c5:f8, screen_functions:r1:c26:f6]).
2. **Needs confirmation:** Whether Case Queue launches creation, the create form location, button label, fields, success navigation and list refresh are not specified. Do not invent a separate Create Case screen.
3. **Confirmed failure:** Validate before long-running allocation. Dependency unavailability yields documented retryable error or persisted asynchronous job ID, never ambiguous success. Rejected unauthorized/stale mutations leave business state unchanged; retry must not create duplicates. (pp.11–13 [screen_functions:r1:c5:f7, screen_functions:r1:c5:f10, screen_functions:r1:c5:f16]).
4. **Needs confirmation — OQ-007:** Define loading/empty/error states, search/sort/filter/pagination interactions, row actions, count authorization and refreshed-list behavior. Cursor pagination is confirmed API behavior, not a specified pagination widget.

### SCR-002 Case Detail

#### Case field inventory

| Field | Meaning and confirmed values/type | Requiredness/initial/editability/constraints | Validation, visibility and value source |
|---|---|---|---|
| title | Case title | Stored; UI length/required/default/editability unspecified | OQ-009 |
| description / business context | User-submitted case context | Case receives business context; rich/plain text and limits unspecified | Validate server payload before transaction; client timing unspecified |
| priority | Derived business priority | Must derive from explicit impact and urgency, never model output alone | Formula/options need OQ-009 |
| impact | Explicit business impact input to priority | Type/options/requiredness/default unspecified | OQ-009 |
| urgency | Explicit urgency input to priority | Type/options/requiredness/default unspecified | OQ-009 |
| sensitivity label | Case sensitivity; information classes `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` are confirmed | Case DDL `TEXT NOT NULL DEFAULT 'INTERNAL'` is database-level only | Editable classification control/default/options mapping need OQ-009 |
| status | Case state | `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED`; initial domain state `NEW` | Server-authoritative transitions; not an unrestricted dropdown |
| owner | Case ownership | Stored; Owner PATCH scope requires mapping | Assignment options and edit permission need OQ-001/OQ-009 |
| current approved result | Pointer to approved response | Updates atomically with satisfied approval gate; closed lineage immutable | Display approved vs partial/draft distinctly |
| revision | Monotonically increasing case revision | Case DDL `BIGINT NOT NULL DEFAULT 1`; client submits `If-Match` | UI visibility/format unspecified; current revision returned on conflict |
| attachments | Immutable document-version-linked entities | Analyst upload supported; see SF-007 | Status/preview/removal placement unspecified |
| runs | Separate linked run entities using immutable identifiers | Analyst starts bounded run | See SCR-004; run selector layout unspecified |
| labels | Asynchronous policy-aware classification output | User correction includes reason code | Correction-authorized user role and label catalog unspecified |
| confidences | Classification output | Numeric scale/precision/threshold unspecified | No inferred editable confidence input |
| provenance | Classification lineage | Stored with labels/confidences | Exact display schema unspecified |
| correction reason code | Reason accompanying corrected labels | Required for correction; catalog/type/default unspecified | Validation timing and selectable source need OQ-009 |
| deadline | Contractual deadline computed with business calendars in workspace timezone | Prediction cannot change it | Calendar/timezone source and visibility need OQ-009 |
| breach prediction | Advisory prediction | Cannot set contractual deadline | Display/precision/action unspecified |
| created_at, updated_at | Case DDL `TIMESTAMPTZ NOT NULL DEFAULT now()` | Database values, not independently mandated UI fields | If displayed, apply SF-005 local-time presentation |

Sources: pp.12, 24–26, 45, 62, 85–86 [screen_functions:r1:c5:f8, screen_functions:r1:c9:f3, screen_functions:r1:c9:f5–f9, screen_functions:r1:c15:f7, screen_functions:r1:c20:f7, screen_functions:r1:c27:f1, screen_functions:r1:c27:f6].

#### SF-006 Read, update, classify and close

1. Read only an authorized current revision using `GET /v1/cases/{caseId}`; Analyst/Reviewer scope, `200` success. Foreign-tenant reads are non-disclosing not-found-equivalent failures. (pp.23, 83, 89 [screen_functions:r1:c8:f9, screen_functions:r1:c26:f7, screen_functions:r1:c30:f3]).
2. Update through `PATCH /v1/cases/{caseId}` under Owner scope with `If-Match`; success is `200`, conflict `409`. Conflicting revision returns `CASE_VERSION_CONFLICT` with current revision. The canonical example message is `Case revision no longer matches.` with safe expected/actual revisions, `correlation_id` and `retryable: false`; example revisions `7`/`8` and `trace_01HZZ_EXAMPLE` are not fixed values. (pp.25, 83–84 [screen_functions:r1:c9:f6, screen_functions:r1:c26:f8, screen_functions:r1:c26:f18]).
3. Correct classification labels with a reason code. Maintain labels/confidences/provenance from the asynchronous classifier as distinct evidence. (p.12 [screen_functions:r1:c5:f8]).
4. Apply only supported transitions: `NEW→TRIAGED`, `TRIAGED→IN_PROGRESS`, `IN_PROGRESS→PENDING_APPROVAL` or `RESOLVED`, and `PENDING_APPROVAL→RESOLVED` or `IN_PROGRESS`. Guards include role, revision and approval requirements. (pp.25, 82 [screen_functions:r1:c9:f5, screen_functions:r1:c26:f2]).
5. Closure through the documented `POST /v1/cases/{caseId}/close` snapshots approved answer, cited versions and reviewer decisions. `CLOSED` is final except explicit reopening as a new revision. Closed approved-output lineage remains immutable; retention applies only to eligible closed cases with legal-hold exceptions. (pp.24–26 [screen_functions:r1:c9:f1, screen_functions:r1:c9:f9, screen_functions:r1:c9:f11]).
6. Stale/unauthorized writes leave business state unchanged and do not produce an accepted mutation. Accepted changes and CaseStateChanged replay handling preserve one business outcome and audit lineage. (pp.25–26 [screen_functions:r1:c9:f7, screen_functions:r1:c9:f12, screen_functions:r1:c9:f14]).

**Needs confirmation — OQ-009:** Save/edit/correct/close/reopen control labels, execution role matrix, closure entry edge, reopening target, permitted editable fields by state, conflict recovery and unsaved-edit handling are unspecified. No automatic retry of a stale edit is authorized. Case/CaseAggregate/CaseService register “Immutable derivative” labels on pp.13, 17, 26 require amendment to distinguish mutable case state from immutable revisions/evidence/approved lineage.

#### SF-007 Attachment ingestion

| Input/output | Confirmed constraints | Unresolved attributes |
|---|---|---|
| Uploaded file | PDF, DOCX, HTML, UTF-8 text; signature/extension agreement; configurable 25 MB per file; decompression-bomb threshold | MB byte convention, active policy cap source, threshold value, file count/name constraints, browser validation timing |
| Document status | `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED`; scan/quality guards | Exact state edges, UI status location, poll frequency and remediation controls |
| OCR opt-in | Fallback is opt-in and provenance-marked; OCR beyond English deferred | Actor, control, default and supported input-language behavior |
| Quality flags | empty-page ratio, unknown-character ratio, table-loss indicators, language confidence | Thresholds/types/display/units/remediation |
| Source anchors | URI, file hash, page, optional bbox; immutable versions | Page numbering and bbox coordinate system; visible field subset |

Sources: pp.10, 30–32, 82 [screen_functions:r1:c4:f6, screen_functions:r1:c11:f2, screen_functions:r1:c11:f5–f8, screen_functions:r1:c26:f4].

1. An authorized Analyst submits `POST /v1/cases/{caseId}/attachments`; `202` creates an ingestion operation, not a completed/approved answer. Status integration is `GET /v1/documents/{documentId}/status`. (pp.30–32, 83 [screen_functions:r1:c11:f3, screen_functions:r1:c11:f12, screen_functions:r1:c26:f9]).
2. Scan before parsing; do not execute macros or fetch embedded remote references. Unsafe attachments enter quarantine and never enter the search index. Oversized and other abuse cases fail closed with stable non-sensitive codes. (pp.13, 30 [screen_functions:r1:c5:f12, screen_functions:r1:c11:f4]).
3. Normalize without rewriting source claims. Content fingerprint plus pipeline version creates immutable derivative IDs; changed processing can coexist side by side. PDF extraction retains page/bbox blocks, table rows/columns, headings and reading order. (p.31 [screen_functions:r1:c11:f5–f6]).
4. Low-quality permitted documents remain viewable but are excluded from autonomous recommendations. This is distinct from unsafe quarantine and must not be replaced by blanket invisibility. (p.32 [screen_functions:r1:c11:f8]).
5. Failed index writes do not roll back accepted metadata; reconciliation compares fingerprints/retries and repairs message links from the outbox. Search readiness uses index coverage, not queue emptiness. (pp.49, 78 [screen_functions:r1:c16:f6, screen_functions:r1:c25:f3]).

**Needs confirmation — OQ-010:** Upload widget/launch placement, failure wording, status navigation, reprocessing/OCR controls, manual use of low-quality content and quarantine remediation need definition. Do not convert tool/configuration examples into upload limits.

### SCR-003 Evidence Viewer

#### Fields and selectable data

| Field/data | Confirmed meaning and constraints | UI definition |
|---|---|---|
| Source document/content | Permitted source behind citation; immutable source version | Viewable when authorized; preview layout/format need confirmation |
| Anchored page range | Citation opens source and highlights range | Page index/number convention and highlight geometry unspecified |
| Source URI | Chunk source location | Stored; visible/clickable rendering unspecified; no arbitrary browsing permission |
| File hash / document revision | Immutable source identity/version | Stored/returned provenance; hash algorithm/visible formatting require contract mapping |
| Optional bounding box | Source region anchor | Optional; units/coordinates unspecified |
| chunk ID | Evidence item identifier | Response field; opaque citation verification, not necessarily displayed |
| source title | Evidence item source title | Response field; display/length unspecified |
| ACL digest | Permission-sensitive evidence provenance | Response field; user visibility unspecified |
| evidence_set_id / citations | Grounded-search output | Server-resolved/permission-sensitive; complete Citation schema absent |
| Search query | Lexical and normalized vector input | UI placement/type/length/required/default/filter controls unspecified |
| Reduced-quality flag | Required if lexical retrieval continues during vector degradation | Visible; exact wording/accessibility/duration unspecified |

Sources: pp.31, 35–36, 57, 69, 85, 87 [screen_functions:r1:c11:f7, screen_functions:r1:c12:f7–f8, screen_functions:r1:c19:f4, screen_functions:r1:c22:f4, screen_functions:r1:c27:f2, screen_functions:r1:c28:f10].

#### SF-008 Search and citation events

1. Execute authorized search through `POST /v1/search`; Member scope, `200`, ACL-filtered lexical plus semantic evidence. Ranking is separate from authorization; never return model text before ACL filtering. Query processing uses bounded candidates, reciprocal rank fusion, deterministic reranking, source diversity and token budgets. (pp.34–35, 83 [screen_functions:r1:c12:f1, screen_functions:r1:c12:f6, screen_functions:r1:c26:f14]).
2. When support/confidence/quality is insufficient, return `NO_SUPPORTED_EVIDENCE`, not fabricated context. Clarification or routing to a human is permitted; the source does not select one universally. Missing-citation generation must produce needs-review or unsupported outcome (`TST-009`). (pp.36, 89 [screen_functions:r1:c12:f8, screen_functions:r1:c30:f9]).
3. Obtain evidence using existing contracts `GET /v1/evidence/{evidenceId}` and `GET /v1/cases/{caseId}/evidence`; exact overlap/mapping needs confirmation. Verify opaque citation identifiers before display; cite only anchors that resolve and are currently permitted. (pp.31, 35–36, 57–59 [screen_functions:r1:c11:f7, screen_functions:r1:c12:f4, screen_functions:r1:c12:f7, screen_functions:r1:c19:f10]).
4. Citation click opens source and highlights anchored page range. Do not leak soft-deleted or revoked content through previews; soft-deleted entities cannot be retrieved. Objects require access-controlled short-lived signed URLs and opaque names; datastores remain private. (pp.51–52, 57 [screen_functions:r1:c17:f2, screen_functions:r1:c17:f8, screen_functions:r1:c19:f4]).
5. ACL changes invalidate caches before new results and revocation must take effect before the next retrieval. Source deletion tombstones and schedules index removal. Recheck authorization before publication and reject stale evidence even if it was previously retrieved. (pp.27–29, 53, 59 [screen_functions:r1:c10:f1, screen_functions:r1:c10:f7, screen_functions:r1:c17:f9, screen_functions:r1:c19:f16]).

**Needs confirmation — OQ-007/OQ-010:** Query controls, filters/sort/page UI, no-result/quality messages, citation verification failure, signed-URL renewal, source preview and already-open revoked-evidence refresh/removal are unspecified. No unlimited browser URL input is authorized.

### SCR-004 Run Timeline

#### Progress fields

| Field | Confirmed meaning/values | Attributes and conditions |
|---|---|---|
| Run status | `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED` | Server workflow/checkpoint/runtime-budget guarded; timeout mapping unresolved |
| Stage/step/checkpoint trace | Human-visible execution trace; retrieval/generation/policy shown | Failed run status reports exactly failed checkpoint |
| Plan revision/hash | Stored before effects; replayable DAG checkpoints | Stored data; visible representation unspecified |
| Runtime/call/token budget | Depth eight; at most sixteen tool invocations; reserved input/output token budget | Not user-editable limits by inference; timeout/quota values need confirmation |
| Evidence metadata | Run read returns stages and evidence metadata | Exact visible subset/schema unspecified |
| Degraded service status | Display when provider unavailable | New generation disabled; manual case/evidence retained |
| SSE offset | Monotonically increasing event offset | Protocol state, not required visible field |

Sources: pp.38, 40–42, 49, 55, 58, 79, 82–83 [screen_functions:r1:c13:f9, screen_functions:r1:c14:f1, screen_functions:r1:c14:f4, screen_functions:r1:c14:f10, screen_functions:r1:c16:f5, screen_functions:r1:c18:f5, screen_functions:r1:c19:f5, screen_functions:r1:c25:f6, screen_functions:r1:c26:f3, screen_functions:r1:c26:f11].

#### SF-009 Start and monitor run

1. Analyst requests grounded drafting via `POST /v1/cases/{caseId}/runs`; `202` starts a bounded AI workflow. Validate input before long-running allocation. Chapter 3 also names `POST /v1/runs`; its relationship is unresolved, not an approved alias. (pp.12, 15–17, 40–42, 83 [screen_functions:r1:c5:f7, screen_functions:r1:c6:f5, screen_functions:r1:c14:f3, screen_functions:r1:c26:f10]).
2. Admit a new run only when workspace tokens, queue age and provider capacity satisfy thresholds. Throttled clients get `429` with `Retry-After`; saved cases remain available. Quota exhaustion is terminal for that run and cannot automatically change model/data class. (pp.38, 69 [screen_functions:r1:c13:f9, screen_functions:r1:c22:f3]).
3. Create the run immediately and subscribe to `GET /v1/streams/runs/{runId}` SSE within Analyst/Reviewer scope. Show retrieval, generation and policy stages. `GET /v1/runs/{runId}` returns stages/evidence metadata; `GET /v1/runs/{runId}/steps` is also a chapter contract. (pp.40–42, 55, 58, 83 [screen_functions:r1:c14:f5, screen_functions:r1:c18:f5, screen_functions:r1:c19:f5, screen_functions:r1:c26:f11]).
4. Resume with `Last-Event-ID` and backfill retained events only within caller authorization. Refresh reconstructs progress from server state, not browser memory. Workflow stages checkpoint before dispatch; consumers deduplicate event IDs/detect stale revisions and cannot rely on ordering across queue partitions. (pp.48–49, 55, 58 [screen_functions:r1:c16:f4–f5, screen_functions:r1:c18:f5, screen_functions:r1:c19:f5]).
5. Triage Agent classifies, Research Agent requests evidence, Draft Agent assembles candidate; Policy Evaluator is deterministic. External writes need separately authorized pinned/validated MCP capabilities; A2A may be declined and carries declared schemas/deadlines/trace. Consequential writes need human authorization and idempotency; denied actions cannot be substituted with semantically equivalent tools. (pp.40–42 [screen_functions:r1:c14:f2, screen_functions:r1:c14:f7–f11]).
6. Fail closed on invalid model output (`MODEL_OUTPUT_INVALID`), ungrounded recommendation, injection or stale approval; never present partial processing as an approved answer. Termination triggers include exhausted calls, repeated invalid plans, policy denial, deadline expiry and missing approval, with exact checkpoint reporting. (pp.13, 38, 41 [screen_functions:r1:c5:f12, screen_functions:r1:c13:f7, screen_functions:r1:c14:f10]).
7. Transient faults may use bounded exponential backoff/jitter/circuit breakers; validation and permission failures are permanent and not retried. Mutable retry requires idempotency. (pp.42, 49 [screen_functions:r1:c14:f11, screen_functions:r1:c16:f8]).

**Needs confirmation — OQ-008:** Define missing-approval terminal timing versus `AWAITING_REVIEW`, AUTO_ALLOW path, terminal timeout literal and recoverable-timeout action, status-label mapping, SSE payload/retention/expired-offset handling, duplicate/stale browser rendering, heartbeat behavior, start placement and cancellation/retry controls. No cancellation endpoint or button is confirmed. `run_timeout_seconds: 180` on p.90 is example-only; p.12 requires terminal completion within configured maximum or recoverable timeout but does not set its literal state [screen_functions:r1:c5:f11, screen_functions:r1:c31:f1].

### SCR-005 Review Inbox

#### Review field inventory

| Field | Confirmed meaning/type/values | Requiredness/editability/initial constraints | Validation and value source |
|---|---|---|---|
| Exact candidate artifact | The content being reviewed | Reviewer must inspect the exact candidate; changed hash invalidates decision | Artifact schema/preview unconfirmed |
| Source citations | Grounding evidence | Reviewer can inspect source before approval | Current permissions/resolvable anchors; see SCR-003 |
| Model/prompt version | Generation lineage | Displayed to reviewer; not an inferred selector | Stored generation lineage |
| Policy reasons | Deterministic reasons for gate | Displayed to reviewer | Versioned policy evaluation |
| Policy outcome | `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY` | LLM risk tags cannot override | Rule-set version and normalized inputs |
| Task status | `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED` | Actor/hash/duties guarded | State edges/UI labels unconfirmed |
| decision | Decision captured in approval record | Approve/Reject controls confirmed; complete wire enum unspecified | Reviewer/hash gate |
| actor/reviewer ID | Decision principal | Captured, immutable decision history | Authenticated principal; visible format unspecified |
| timestamp | Decision time | Captured | UTC storage/workspace-local labeled display if shown |
| evaluated artifact hash | Exact reviewed content identity | Required binding, not user authority to substitute hash | Compare current candidate; stale decision rejected |
| rationale / reason | Decision rationale; `reason` in selected data catalog | Record includes it; required editable review-field mapping unspecified | Length/format/default/timing need OQ-012 |
| annotations | Optional review annotations | Optional in approval record | Type/length/editability need OQ-012 |
| reviewer pool / minimum role | Assignment eligibility | Policy-defined with separation of duties | Pool source, membership/selection control unspecified |
| SLA/expiry | Configured review deadline | Expiry reassigns/escalates; never implicitly approves | Value and destination unspecified |
| override reason / secondary reviewer | Override evidence and independent review | Elevated role, secondary reviewer and audited reason required | Exact UI mechanism and eligible roles unspecified |

Sources: pp.44–46, 58, 82, 85 [screen_functions:r1:c15:f1–f8, screen_functions:r1:c19:f6, screen_functions:r1:c26:f5, screen_functions:r1:c27:f4]. Policy inputs include sensitivity, action, evidence quality, model class, financial impact category and confidence bands, normalized and retained with rule-set version; these do not independently create editable controls [screen_functions:r1:c15:f2].

#### SF-010 Open, decide and publish

1. Read tasks via `GET /v1/review-queue`; exact screen selection and permissions need confirmation. Tasks use policy reviewer pools/minimum role/duties. (pp.45–46 [screen_functions:r1:c15:f4, screen_functions:r1:c15:f9]).
2. Present exact artifact, citations, model/prompt version and policy reasons. Make sources inspectable. **Approve** and **Reject** remain disabled until required review fields are complete. Required field names are not supplied; do not guess them. (pp.57–58 [screen_functions:r1:c19:f1, screen_functions:r1:c19:f6]).
3. Submit `POST /v1/approvals/{approvalId}/decision` with Reviewer scope, binding action to reviewed hash; results `200`/`409`. Capture actor, time, hash, rationale and optional annotations. If content changed, reject as stale and audit; business state is unchanged by rejected decision. (pp.45–46, 83, 89 [screen_functions:r1:c15:f5–f6, screen_functions:r1:c26:f12, screen_functions:r1:c30:f6]).
4. Satisfy current authorization/evidence/policy gates before publication. An unapproved high-risk run cannot publish. Final response pointer and satisfied gate commit atomically; replay cannot publish another artifact under old approval. A recorded decision leads to publication validation, not automatic navigation or unconditional publish. (pp.7, 11–12, 45, 87 [screen_functions:r1:c3:f3, screen_functions:r1:c5:f2, screen_functions:r1:c5:f9, screen_functions:r1:c15:f7, screen_functions:r1:c28:f5]).
5. A rejected/denied request can be reworked as a new run revision, never retroactively approved. Override requires elevated role, secondary reviewer and audited reason. Expiry reassigns/escalates and records escalation without implicit approval. (pp.45–46, 89 [screen_functions:r1:c15:f4, screen_functions:r1:c15:f8, screen_functions:r1:c30:f10]).

**Needs confirmation — OQ-012:** Required review fields, submission validation, decision enum, rationale requiredness, primary-action designation, task-open behavior, success/failure placement, reassignment/override controls, expiry duration and escalation destination are unresolved. No separate Publish button or automatic AUTO_ALLOW bypass is confirmed. `UserReviewOpened` is a chapter audit/event identifier, not proof of a browser event schema (pp.57–59 [screen_functions:r1:c19:f11–f17]).

Representative `DECISION GATE` fields `POLICY`, `EVIDENCE`, `MODEL`, `APPROVAL`, `STATUS` show `HUMAN_REVIEW`, `5 verified citations`, `gateway-r1.2`, `Assigned to reviewer`, `Awaiting decision`. These are example values, not a five-citation minimum, selected model, assignment default or complete status vocabulary.

### SCR-006 Connector Health

| Field/data | Confirmed meaning/constraints | UI attributes needing confirmation |
|---|---|---|
| Connector capabilities | list, fetch, delta cursor, ACL, delete support | Types/format/status layout; not inferred editable flags |
| Trust warning | Unsupported capability causes lower-trust ingestion and explicit user-visible warning | Text/severity/location/audience/dismissal and action impact |
| Credential reference | Workspace-scoped reference to secret-store OAuth refresh token/service credential | Entry/reauthorization UI; never display raw secret by inference |
| Sync status/history | Incremental sync and `GET /v1/connectors/{connectorId}/runs` | Columns/status enums/sort/cursors/refresh unspecified |
| Provider cursor / high-watermark / error ledger | Durable sync checkpoints | Backend stored data, not mandated visible/editable fields |
| Quarantine reason/correlation/remediation path | Malformed document outcome after bounded retries | Literal catalog, visibility and remediation controls |
| Provisioning status | Incomplete provisioning is visible and blocks sync | Placement/status vocabulary/readiness threshold |
| Index coverage | Search-readiness signal, not empty queue | Calculation/threshold/display format |

Sources: pp.27–29, 78 [screen_functions:r1:c10:f2–f6, screen_functions:r1:c10:f10, screen_functions:r1:c25:f2–f3].

#### SF-011 Sync and credential lifecycle

1. Permit incremental sync under Admin scope using `POST /v1/connectors/{connectorId}/sync`; `202`. Validate before allocation and block sync when provisioning is incomplete. (pp.27, 78, 83 [screen_functions:r1:c10:f3, screen_functions:r1:c25:f2, screen_functions:r1:c26:f13]).
2. Preserve source identity/permissions/history. Advance cursor only after durable ingestion outcomes for preceding items; partial batches retry safely. Honor provider `Retry-After`, backoff/jitter, workspace quotas and fair scheduling. (pp.27–28 [screen_functions:r1:c10:f1, screen_functions:r1:c10:f6, screen_functions:r1:c10:f9]).
3. Operator credential revocation makes queued jobs fail `CONNECTOR_REAUTH_REQUIRED` without exposing tokens. Role/UI reauthorization mapping is unresolved. (p.27 [screen_functions:r1:c10:f4]).
4. After bounded retries, malformed records quarantine with reason/correlation/remediation; remaining batch **may continue** and ledger records the exception. Do not misreport partial batch as all-success or force whole-batch failure contrary to this exception. (p.29 [screen_functions:r1:c10:f10]).
5. Handle deletion/ACL invalidation as SCR-003 requires. Sync/event retries must not reapply accepted mutations; unauthorized/stale writes leave business state unchanged. (pp.28–29 [screen_functions:r1:c10:f7–f8, screen_functions:r1:c10:f14–f15]).

**Needs confirmation — OQ-013:** Identify primary action, Sync control, credential entry/revoke/reauthorize flows, operator permissions, quota/retry values, cursor-list UI and partial-success/quarantine messages. Do not treat `GET /v1/connectors/{connectorId}/runs` as a confirmed job-creating UI action despite repeated allocation wording.

### SCR-007 Policy Settings

| Setting/data | Confirmed meaning or constraint | Required/editable/initial/selectable source |
|---|---|---|
| retention class | Workspace retention setting | Values and corporate policy unresolved |
| allowed models | Workspace-specific approved deployments | Registry considers capability, region, data-handling class, context length, cost and evaluation approval; not provider-brand-wide approval |
| connector credentials references | Workspace secret references | Never substitute browser exposure of tokens |
| approved toolsets | Workspace allowed toolsets | Discovery never grants invocation authority; schemas pinned/separate authorization |
| reviewer routing | Pool/minimum role/separation of duties | Pool/role/source catalog unresolved |
| workspace policy version/revision | Update precondition and lineage | Revision precondition/audit required; UI field and default unspecified |
| quota | Selected workspace backing data | Numeric limits, edit permissions and UI placement unresolved |
| policy inputs/outcomes | See SCR-005 | Evaluation data is not an unrestricted editable policy form |

Sources: pp.24, 37, 44–46, 85 [screen_functions:r1:c9:f2, screen_functions:r1:c13:f2, screen_functions:r1:c15:f2–f4, screen_functions:r1:c27:f1].

#### SF-012 Policy administration

1. Workspace Admin manages policy; configuration updates require revision preconditions and durable audit records. (pp.11, 24 [screen_functions:r1:c5:f3, screen_functions:r1:c9:f2]).
2. Deterministic versioned policy cannot be overridden by model tags/text. Routing/retention/redaction/review depend on maximum information class included in a run. Fallback is only to approved deployments with equal or stronger data handling; provider outage cannot route restricted data to unapproved region/deployment. (pp.37, 44, 62 [screen_functions:r1:c13:f3, screen_functions:r1:c15:f3, screen_functions:r1:c20:f7]).
3. Reject stale/unauthorized settings mutations without changing business state. Preserve audit lineage and secret scope. (pp.24, 62–63 [screen_functions:r1:c9:f2, screen_functions:r1:c20:f9–f15]).

**Needs confirmation — OQ-011:** Define primary action, Save control, field schema/value catalogs/validation, publish-versus-draft policy revision behavior and update endpoint. Chapter 6 associates workspace configuration with `PATCH /v1/cases/{caseId}`; this is an unresolved mapping, not authorization to send workspace settings in case patches. `GET /v1/model-catalog`, security-hold and membership contracts do not themselves define settings controls.

### SCR-008 Audit Explorer

| Field/data | Confirmed meaning and constraints | UI definition |
|---|---|---|
| Immutable audit events | Cursor-paginated immutable log | Columns, filter/sort/cursor widgets/default range need confirmation |
| decision metadata | Auditor-visible within redacted scope | Exact schema/visible subset unspecified |
| prompt-template digests | Auditor-visible lineage | Not full internal model prompts |
| access events | Auditor-visible within redacted scope | Principal/resource redaction and drill-down unspecified |
| actor/action/digest/tenant ID | Selected append-only backing fields | Not every backing field is automatically displayed |
| event/trace/correlation/revision/time | Cross-boundary provenance | Display selection unspecified; time rules SF-005 |
| historical review decisions | Operators may query, never alter | Operator mapping/scope unresolved |
| audit manifests/receipts | Export/purge lineage | Viewing/downloading screen mapping unspecified |

Sources: pp.11, 62, 83, 85 [screen_functions:r1:c5:f5, screen_functions:r1:c20:f10, screen_functions:r1:c26:f15, screen_functions:r1:c27:f5].

#### SF-013 Audit viewing

1. Query `GET /v1/audit/events` under Auditor scope; `200` yields cursor-paginated immutable log. Apply redacted content scope and non-disclosing denied-resource handling. (pp.11, 23, 83 [screen_functions:r1:c5:f5, screen_functions:r1:c8:f9, screen_functions:r1:c26:f15]).
2. Preserve append-only batch-hash-chained entries exported to independently controlled retention storage. Do not permit edits to historical decisions or case content by an Auditor. (pp.11, 62 [screen_functions:r1:c5:f3, screen_functions:r1:c20:f10]).
3. Accepted transitions have one audit record; denied operations have stable errors and tenant-scoped traces. Denial audit includes principal and denied resource class without private existence leakage. Source text and secrets do not enter diagnostics. (pp.23, 59, 64 [screen_functions:r1:c8:f9, screen_functions:r1:c19:f17, screen_functions:r1:c21:f1]).

**Needs confirmation — OQ-014:** Primary action, filter/query inputs, columns, pagination layout, retention boundary messages, export links, row detail, audit redaction policy and operator entitlements are unspecified. Diagnostic default TTL 30 days is distinct from fictional audit seven-year policy, both subject to legal-hold receipts; corporate retention remains an open decision (pp.66, 90 [screen_functions:r1:c21:f8, screen_functions:r1:c31:f8]).

## Integrations and Acceptance Criteria

### SF-014 Confirmed screen-relevant integration inventory

| Interface | Input/authorization | Output or behavior | Source |
|---|---|---|---|
| OIDC authorization code + PKCE | Authenticated principal/tenant/token claims | Authorized browser session; no local-storage long-lived refresh token | pp.21–22 [screen_functions:r1:c8:f3–f6] |
| `POST /v1/cases` | Analyst; idempotency key; schema not complete | `201`, case identifier/NEW case | p.83 [screen_functions:r1:c26:f6] |
| `GET /v1/cases?cursor=...` | Authorized scope; cursor schema unresolved | UI case-list contract | pp.57–59 [screen_functions:r1:c19:f10, screen_functions:r1:c19:f14] |
| `GET /v1/cases/{caseId}` | Analyst/Reviewer, authorized case | `200`, current revision | p.83 [screen_functions:r1:c26:f7] |
| `PATCH /v1/cases/{caseId}` | Owner; `If-Match` | `200`/`409`; current revision on `CASE_VERSION_CONFLICT` | pp.25, 83 [screen_functions:r1:c9:f6, screen_functions:r1:c26:f8] |
| `POST /v1/cases/{caseId}/close` | Guards/role/schema unresolved | Approved-output/source/decision snapshot | pp.26 [screen_functions:r1:c9:f9, screen_functions:r1:c9:f11] |
| `POST /v1/cases/{caseId}/attachments` | Analyst; supported file constraints | `202`, ingestion operation | pp.30, 83 [screen_functions:r1:c11:f2–f4, screen_functions:r1:c26:f9] |
| `GET /v1/documents/{documentId}/status` | Document authorization/schema unresolved | Document status integration | p.32 [screen_functions:r1:c11:f3, screen_functions:r1:c11:f12] |
| `POST /v1/search` | Member; query/schema unresolved; ACL checks | `200`, lexical/semantic evidence or `NO_SUPPORTED_EVIDENCE` | pp.34–36, 83 [screen_functions:r1:c12:f4–f8, screen_functions:r1:c26:f14] |
| `GET /v1/evidence/{evidenceId}`; `GET /v1/cases/{caseId}/evidence` | Current evidence scope | Verified provenance/evidence; exact overlap unresolved | pp.36, 57–59 [screen_functions:r1:c12:f4, screen_functions:r1:c19:f10] |
| `POST /v1/cases/{caseId}/runs` | Analyst; runtime/admission/idempotency guards | `202`, bounded workflow | p.83 [screen_functions:r1:c26:f10] |
| `POST /v1/runs` | Alternate chapter contract; relation unresolved | Do not assume alias | pp.15–17 [screen_functions:r1:c6:f5, screen_functions:r1:c6:f14] |
| `GET /v1/runs/{runId}`; `GET /v1/runs/{runId}/steps` | Analyst/Reviewer for run read; steps scope unresolved | `200` run read with stages/evidence; step contract | pp.42, 83 [screen_functions:r1:c14:f12, screen_functions:r1:c26:f11] |
| `GET /v1/streams/runs/{runId}` | Analyst/Reviewer; `Last-Event-ID` | `200` SSE, monotonic authorized retained backfill | pp.55, 83 [screen_functions:r1:c18:f5, screen_functions:r1:c26:f11] |
| `GET /v1/review-queue` | Policy-eligible reviewer; detailed scope unresolved | Review tasks | pp.45–46 [screen_functions:r1:c15:f9, screen_functions:r1:c15:f11] |
| `POST /v1/approvals/{approvalId}/decision` | Reviewer; exact hash/duties/fields | `200`/`409`; stale reject/audit | p.83 [screen_functions:r1:c26:f12] |
| `POST /v1/connectors/{connectorId}/sync` | Admin; complete provisioning | `202`, incremental sync | pp.78, 83 [screen_functions:r1:c25:f2, screen_functions:r1:c26:f13] |
| `GET /v1/connectors/{connectorId}/runs` | Scope/schema unresolved | Sync-run contract | pp.28–29 [screen_functions:r1:c10:f5] |
| `GET /v1/audit/events` | Auditor | `200`, cursor-paginated immutable log | p.83 [screen_functions:r1:c26:f15] |
| `GET /v1/usage` | Admin | `200`, costs/quotas/trends; daily budget/forecast/rejected excess rollups | pp.65, 83 [screen_functions:r1:c21:f7, screen_functions:r1:c26:f16] |
| `POST /v1/evaluations`; `GET /v1/evaluations/{evaluationId}` | Admin create; read scope unresolved | `202` frozen evaluation; read contract; no dedicated screen confirmed | pp.74–76, 83 [screen_functions:r1:c24:f4, screen_functions:r1:c26:f16] |
| `POST /v1/workspaces/{workspaceId}/export` | Admin + approver; two independent checks/two-person export | `202`, checksummed controlled manifest/package excluding secrets/internal prompts | pp.78–80, 83, 88 [screen_functions:r1:c25:f1, screen_functions:r1:c25:f9, screen_functions:r1:c26:f17, screen_functions:r1:c29:f11] |
| `POST /v1/workspaces/{workspaceId}/delete` | Admin + approver; two independent checks/legal hold | `202`, tombstones/blob-index removal/protected-record receipts | pp.78–80, 83, 89 [screen_functions:r1:c25:f1, screen_functions:r1:c25:f10, screen_functions:r1:c26:f17, screen_functions:r1:c30:f13] |
| `GET /v1/system/degraded-modes` | Scope/schema unresolved | Degradation integration, not an extra screen | pp.68–70 [screen_functions:r1:c22:f5–f6] |
| Object access | Current tenant/workspace/document authorization | Opaque names, encrypted private objects and short-lived scoped signed URLs | pp.51–52 [screen_functions:r1:c17:f1–f2, screen_functions:r1:c17:f8] |
| Optional outbound webhooks | Signed subscriptions/recipient signature-age verification | Bounded backoff; failures do not roll back case transition | p.55 [screen_functions:r1:c18:f6] |

**Needs confirmation — OQ-015:** External OpenAPI is authoritative for REST clients and repository IDL generates contracts; complete schemas, request fields, scopes and literal error catalogs are To be defined in a later stage. Internal HTTP/gRPC/protobuf contracts are independently authorized, not browser APIs. Do not invent missing endpoint identifiers.

Additional source contracts retained as dependencies, **not screens**: `GET /v1/me`, `PUT /v1/workspaces/{workspaceId}/members`, `GET /v1/model-catalog`, `GET /v1/openapi.json`, `POST /v1/security/holds`, `POST /v1/design-decisions`, `GET /v1/design-baselines/{id}`; internal `POST /internal/model/generate`, `GET /internal/workflows/{runId}`, `POST /internal/deadletters/{id}/replay`, `GET /internal/storage/documents/{id}`, `POST /internal/storage/purge`, `GET /internal/metrics`, `GET /internal/capacity`, `POST /internal/releases`, `GET /internal/releases/{releaseId}`; runtime `GET /v1/health/live`, `GET /v1/health/ready`. Sources: pp.8–10, 18–23, 37–39, 48–56, 61–73 [screen_functions:r1:c4:f9–f10, screen_functions:r1:c7:f4, screen_functions:r1:c7:f11, screen_functions:r1:c8:f11, screen_functions:r1:c8:f15, screen_functions:r1:c13:f4, screen_functions:r1:c16:f3, screen_functions:r1:c17:f4, screen_functions:r1:c18:f10, screen_functions:r1:c20:f4, screen_functions:r1:c21:f2, screen_functions:r1:c22:f5, screen_functions:r1:c23:f3].

Repeated section/register wording applies validation before long-running allocation and retryable-error-or-persisted-job outcomes even to GET/health/contract-read paths. Preserve the no-ambiguous-success requirement, but **OQ-015** must clarify whether those reads allocate work and their mismatched entity/event associations. This file does not silently rewrite them or approve GET-triggered mutations.

### SF-015 Tool and external data contracts

Enterprise repository workers preserve source ACL/history and use secret-store credentials; model providers receive scoped context/structured prompts, never raw connector tokens or unrestricted DB access. Approved MCP servers use separate scoped capability authorization and pinned argument schemas. Model routing, prompt/output validation and policy publication gates remain server-authoritative. (pp.15, 27–29, 37–42 [screen_functions:r1:c6:f3, screen_functions:r1:c10:f1–f4, screen_functions:r1:c13:f2–f10, screen_functions:r1:c14:f7–f11]).

`knowledge.search@v1` accepts `{query: string, case_id: uuid, max_items: int<=10}` and returns `{evidence_set_id: uuid, citations: Citation[]}`. It requires tenant-scoped `read:permitted_documents`, read-only effects, no arbitrary URLs or filesystem access. The bound is a tool argument limit, **not** screen page size or a general UI evidence-selection limit. Capability registration is discovery only. (p.87 [screen_functions:r1:c28:f10–f12]).

The A2A example uses `research.grounded_search.v1`, `schema://oriondesk/research-request/1`, task/tenant/deadline/trace/authorization references and payload query/case ID. `case_demo` is fictional and does not satisfy the MCP uuid contract; adapter typing and output-schema completeness remain **OQ-015**. No deadline such as example `2026-11-09T08:00:00Z` is a schedule. (p.87 [screen_functions:r1:c28:f9]).

### SF-016 Transaction, event and audit behavior

**Confirmed:** Durable changes propagate `tenant_id`, `revision`, `actor_id`, `occurred_at` and correlation context. They are server/interface metadata, not mandatory user-editable fields. Case mutations, approval decisions and outbox inserts commit in one ACID transaction; search/webhooks reconcile asynchronously. Cross-service writes are idempotent. Job-creating POSTs require `Idempotency-Key`: identical payload replay returns original outcome, changed fingerprint returns `409 IDEMPOTENCY_CONFLICT`. Actor/request-fingerprint outcomes are retained for 24 hours. (pp.15–17, 25, 52, 54, 89 [screen_functions:r1:c6:f2, screen_functions:r1:c6:f4, screen_functions:r1:c9:f6, screen_functions:r1:c17:f5, screen_functions:r1:c18:f4, screen_functions:r1:c30:f1–f2]).

Events use canonical JSON/UTC envelope fields `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, `payload`. Consumers deduplicate event/operation identities, check revisions and do not reapply accepted mutations after retry. Outbox publication or explicitly reconciled saga protects state. (pp.17, 48–50 [screen_functions:r1:c6:f13, screen_functions:r1:c16:f1–f4, screen_functions:r1:c16:f12]).

| Event | Confirmed producer / selected payload / consumer action from Appendix C |
|---|---|
| `CaseCreated` | Case Service / Case ID, revision / run classifier |
| `DocumentNormalized` | Ingestion / Version ID, source hash / build index |
| `SearchIndexCommitted` | Indexer / index generation, document revision / invalidate query cache |
| `AgentPlanApproved` | Orchestrator / Run ID, plan hash / dispatch steps |
| `ApprovalDecisionRecorded` | Policy Service / Task, actor, content hash / validate publication |
| `WorkflowStageAdvanced` | Orchestrator / Run, stage, checkpoint / resume consumers |
| `AccessDenied` | Policy Service / Principal, action, policy digest / alert enrichment |
| `TenantDeletionVerified` | Retention Worker / Manifest ID, receipt hash / close purge record |

Source p.87 [screen_functions:r1:c28:f1–f8]. These are not automatically browser/SSE event types. Other chapter identifiers—`BaselineCommitted`, `RunRequested`, `DeploymentPromoted`, `CaseStateChanged`, `ConnectorSyncStarted`, `ModelInvocationCompleted`, `DataRetentionPurgeCommitted`, `ApiCompatibilityVerified`, `UserReviewOpened`, `SecurityPolicyChanged`, `SloBurnRateDetected`, `BackpressureActivated`, `ReleasePromoted`, `EvaluationCompleted`—retain chapter audit/deduplication contracts, without inferred screen-status mapping. Sources pp.8–80, respective contract registers [screen_functions:r1:c4:f10, screen_functions:r1:c6:f14, screen_functions:r1:c7:f11, screen_functions:r1:c9:f11, screen_functions:r1:c10:f13, screen_functions:r1:c13:f12, screen_functions:r1:c17:f11, screen_functions:r1:c18:f16, screen_functions:r1:c19:f14, screen_functions:r1:c20:f12, screen_functions:r1:c21:f9, screen_functions:r1:c22:f8, screen_functions:r1:c23:f9, screen_functions:r1:c24:f10].

Rejected stale/unauthorized actions leave business state unchanged. Denial audit is still mandatory; the p.22 “before publishing AccessDenied” checkpoint does not authorize suppressing denial logs. **OQ-015:** Clarify ordering, denial-event revision semantics and generic component-event mappings (pp.22–23, 87 [screen_functions:r1:c8:f7, screen_functions:r1:c8:f12, screen_functions:r1:c28:f7]).

### SF-017 Degradation and lifecycle operations

1. Provider outage disables admission of new generation, displays degraded status and retains manual case/evidence workflows. Generation unavailability retains evidence search/manual editing; vector degradation may use lexical retrieval only with visible reduced-quality flag. All safety/approval checks remain active. (pp.68–69, 79 [screen_functions:r1:c22:f1, screen_functions:r1:c22:f4, screen_functions:r1:c25:f6]).
2. Suspected ACL leakage suspends affected aliases, revokes cached evidence, preserves audit and replays ACL revisions within scope; search re-enables only after negative access tests pass. This safety containment qualifies ordinary search-availability expectations. (p.79 [screen_functions:r1:c25:f7]).
3. Delayed indexing contains only faulty connector/indexer shard and keeps accepted records durable. Diagnosis uses event ID/outbox lag/parser flags/search throttle/ACL revision; bounded validated replay verifies source/index fingerprints and denied probes. Incident evidence links audit IDs/time window/blast radius/quality effect/prevention. No recovery screen is confirmed. (p.90 [screen_functions:r1:c31:f5–f7]).
4. Export/delete use two independent checks; single Admin export fails the two-person control. Export checksums metadata/approved artifacts/source references/audit manifests and excludes secrets/internal prompts. Deletion respects legal hold and receipts protected retained records, tombstones, removes eligible blobs/index and uses shared subject-request inventory. Exact browser placement/confirmation/receipt delivery is **OQ-016**, not a newly specified screen. (pp.78–80, 83, 88–89 [screen_functions:r1:c25:f1, screen_functions:r1:c25:f9–f10, screen_functions:r1:c26:f17, screen_functions:r1:c29:f11, screen_functions:r1:c30:f13]).

### Acceptance criteria

For each criterion, test only within its supported prerequisites and retain open presentation decisions. Source test IDs are preserved; links to SCR/SF identify affected requirements in this file, not invented source mappings.

| ID / affected requirement | Prerequisites | Action | Expected result |
|---|---|---|---|
| TST-001 / SF-006, SF-016 | Authorized Analyst, valid case request and same key/body | Create twice | One case and identical response |
| TST-002 / SF-016 | Previously used idempotency key | Resubmit changed body | `409 IDEMPOTENCY_CONFLICT`; no second accepted business outcome |
| TST-003 / SF-003, SCR-002 | Foreign-tenant case ID | Read case | `404`-equivalent non-disclosing error |
| TST-004 / SF-008 | Source indexed, then access revoked | Next query | No forbidden evidence |
| TST-005 / SF-009 | Model schema failure forced | Generate | `MODEL_OUTPUT_INVALID`; no publication |
| TST-006 / SF-010 | Candidate hash no longer matches reviewed hash | Approve old/wrong hash | Stale rejection, audited; no accepted stale mutation |
| TST-007 / SF-016 | Accepted outbox event available | Replay | Exactly one accepted business transition |
| TST-008 / SF-009, SF-011 | Provider 429 burst | Exercise workload/retries | Capped retries and controlled admission; numeric bounds need confirmation |
| TST-009 / SF-008, SF-010 | Generated response lacks citations | Evaluate response | Needs review or unsupported outcome, not fabricated/approved answer; branch unresolved |
| TST-010 / SF-010 | Review task reaches configured expiry | Expire | No implicit approval; escalation recorded |
| TST-011 / SF-005 | Keyboard-only user | Open case | No blocked action and visible focus |
| TST-012 / SF-017 | Reference recovery exercise | Recover | RPO ≤15 minutes, RTO ≤4 hours for reference profile |
| TST-013 / SF-017 | Tenant purge under legal hold | Purge | Protected records retained and receipted |
| TST-014 / SF-005, SF-015 | Arbitrary MCP invocation attempted | Dispatch attempt | `DENY` before dispatch |
| TST-015 / SF-007 | Unsafe PDF payload | Ingest | Quarantine; no indexing |
| TST-016 / release dependency | Canary has regressed safety score | Promote | Release gate blocks promotion |

Source p.89 [screen_functions:r1:c30:f1–f16]; recovery numeric conditions p.69 [screen_functions:r1:c22:f12].

Additional source-supported acceptance procedures:

1. **Case resolution (SF-001/SF-007–SF-010):** Given authorized Analyst, permitted evidence and eligible independent Reviewer, create→ingest→retrieve→draft→review→publish. Show exact candidate/sources/model-prompt/policy reasons; complete required fields before enabling decisions. Publish only matching approved/supported artifact under current policy and authorization. Also exercise rejected-draft new-revision rework, poisoned-document quarantine and cross-tenant search denial. (pp.11–12, 45, 58, 75 [screen_functions:r1:c5:f2–f9, screen_functions:r1:c15:f7–f8, screen_functions:r1:c19:f6, screen_functions:r1:c24:f8]).
2. **Citation viewing (SCR-003):** Given a currently permitted, verified resolvable citation, click it; open source and highlight anchored page range. Given revoked or soft-deleted source, do not return prohibited content. Low-quality permitted content remains viewable but cannot support autonomous recommendations. (pp.31–32, 51, 57 [screen_functions:r1:c11:f7–f8, screen_functions:r1:c17:f2, screen_functions:r1:c19:f4]).
3. **Concurrency (SCR-002/SCR-005):** Given changed case revision or artifact hash, submit old `If-Match` or approval hash; return conflict/stale result, retain unchanged business state and audit denial. Exact reload/merge/return UI remains OQ-009/OQ-012. (pp.25, 45, 84, 89 [screen_functions:r1:c9:f6–f7, screen_functions:r1:c15:f5–f6, screen_functions:r1:c26:f18, screen_functions:r1:c30:f6]).
4. **Run refresh/reconnect (SCR-004):** Given authorized ongoing run, refresh and reconnect with `Last-Event-ID`; reconstruct server progress and scope-limited retained events, showing retrieval/generation/policy stages. Do not depend on ephemeral browser progress. Retention expiry behavior remains OQ-008. (pp.55, 58 [screen_functions:r1:c18:f5, screen_functions:r1:c19:f5]).
5. **Connector exception (SCR-006):** Given unsupported capability, display lower-trust warning; given revoked credential, queued jobs fail `CONNECTOR_REAUTH_REQUIRED` without tokens; given malformed exhausted-retry record, quarantine with reason/correlation/remediation and permit ledger-recorded batch continuation. (pp.27–29 [screen_functions:r1:c10:f2, screen_functions:r1:c10:f4, screen_functions:r1:c10:f10]).
6. **Degradation (SF-017):** Given generation outage, saved/manual/evidence operations remain available while new generation is restricted and degradation visible; lexical continuation displays reduced quality. Never weaken approval/authorization to meet load. Suspected ACL leakage uses containment exception until negative tests pass. (pp.68–69, 79 [screen_functions:r1:c22:f1–f4, screen_functions:r1:c25:f6–f7]).
7. **Closed lineage (SF-006):** Given eligible closure, snapshot approved output, cited versions and reviewer decisions; preserve lineage on retention/reopening, respecting legal hold. Closure entry and reopen target remain open. (pp.24–26 [screen_functions:r1:c9:f1, screen_functions:r1:c9:f5, screen_functions:r1:c9:f9]).
8. **Secret/audit safety (SF-013/SF-016):** Exercise positive, foreign-tenant, duplicate/replay and evidence-retention tests; verify one accepted transition/audit and non-sensitive denial. No raw credentials, documents or full prompts in public errors/diagnostic telemetry; immutable audit cannot be historically edited. (pp.54–56, 62–64, 84, 88 [screen_functions:r1:c18:f2, screen_functions:r1:c18:f14, screen_functions:r1:c20:f10, screen_functions:r1:c21:f1, screen_functions:r1:c26:f19, screen_functions:r1:c29:f9]).

### Performance and release qualification

**Confirmed design targets:** API availability `99.9%` monthly; case-create P95 **under 300 ms** under defined load (p.12 also says **within 300 ms**, boundary wording needs OQ-017); search P95 **under 1.5 s**, excluding remote connector fetch; model-generation latency measured separately. Reference load: `2,000` active daily users, `60` requests/s steady, `180` burst, maximum `100,000` indexed documents/tenant and `20` concurrent AI runs per large tenant. Typical `1 MB` source gives approximately `40–120` chunks depending on content/parser quality. These do not specify UI retry/page limits. (pp.12, 65, 68 [screen_functions:r1:c5:f11, screen_functions:r1:c21:f5, screen_functions:r1:c22:f2, screen_functions:r1:c22:f14]).

Fault exercises include provider 429 storms, lost worker heartbeats, duplicate events, object failures and primary-region outage, measuring safety and recovery. R1 has one primary/warm recovery region, primary writes and incident-command restore; no user-selected failover. (pp.19, 69–70 [screen_functions:r1:c7:f7, screen_functions:r1:c22:f12–f13]).

Critical isolation/approval tests have **zero exceptions**, cannot be offset by AI scores, and revised invariants need negative tests. Appendix D `T-01`–`T-12` scenarios cover foreign IDs, hostile PDF instructions, stale approval, malicious polyglot/zipped payloads, credential disclosure, unapproved outage fallback, **100** event replays, mid-search revocation, audit edits, recursive tool hints, single-Admin export and poisoned evaluation fixtures. The replay count is a test count, not browser retry allowance; zipped malicious input is not an added supported upload format. `SEC-001`–`SEC-012` are release-blocking but no explicit one-to-one mapping to T numbering is supplied. Security-control-owner independent reproduction/signature is source process, not a newly assigned owner in this specification. (pp.8, 74, 88 [screen_functions:r1:c4:f2, screen_functions:r1:c24:f1–f3, screen_functions:r1:c29:f1–f13]).

Evaluation uses `1,200` synthetic permission-controlled cases, expected citations/outcomes, citation precision `>=0.97`, unsupported-claim rate `<=0.02`, frozen high-risk policy recall `1.00`, with confidence intervals/domain shift by domain. Prompt/model roll-forward requires re-evaluation; low confidence blocks release. Fixtures are frozen/versioned/independently reviewed; randomized seeds recorded. Signed test outputs link release digest; pack includes unit/schema/auth/replay/staging sync/visual accessibility/search recall/grounding/policy recall/load/recovery tests. (pp.75–76, 89 [screen_functions:r1:c24:f6, screen_functions:r1:c24:f9, screen_functions:r1:c30:f17–f19]).

Release dependencies preserve reconstructible binary/prompt/policy, signed configuration/vault references, verified images/SBOM, compatible expand-and-contract migrations, active-reader field compatibility and canary safety gates. Rollback reverses traffic/binary, not an assumed database down-migration; Security/SRE promotion evidence and release bindings remain engineering processes. Production data is forbidden in development; staging uses synthetic data/test connectors. (pp.19–20, 52, 71–73 [screen_functions:r1:c7:f9–f10, screen_functions:r1:c17:f6, screen_functions:r1:c23:f1–f9]). No release-management screen is confirmed.

## Consistency and Open Questions

### Unresolved source conflicts and required amendments

| Open ID / affected requirements | Both source positions or missing evidence | Required clarification/amendment |
|---|---|---|
| OQ-001 / SF-002, all SCR | Personas p.11 versus baseline roles p.22 and Owner/Member/approver scopes p.83; Operators pp.27/62 | Map terms and define full screen/action/field predicates, independence and redaction; do not invent roles |
| OQ-002 / SF-003 | Authentication pp.15/21 without login/session UI | Select identity/session architecture and specify expiry/logout/navigation without assuming a screen |
| OQ-003 / all SCR | Eight primary names p.57; no route/launch graph/most primary-action labels | Specify route/navigation/launch/status/primary action for each screen |
| OQ-004 / SF-004 | Representative aliases and selected-item/title mismatches pp.7/14/33/43/47/60/67/77/81 | Resolve aliases/components/extra-screen proposals explicitly; no implicit Overview/Usage & Quality approval |
| OQ-005 / SF-005 | WCAG/time/status requirements pp.57–59; delimiters p.61 | Define responsive/focus/locale/number rendering and browser delimiter behavior |
| OQ-006 / all operations | Stable snake-case prose p.54 versus uppercase literal codes pp.25/38/54/84/89 | Retain exact literals; amend naming convention and specify safe user-facing placement/recovery |
| OQ-007 / SCR-001/SCR-003/SCR-008 | Cursor APIs pp.54/57/83; representative columns only | Define filters/query fields/sort/page controls/cursors/authorized totals/empty/loading states; tool max_items≤10 is not page size |
| OQ-008 / SCR-004/SCR-005 | Missing approval terminates p.41 versus awaiting review pp.49/82 and reassignment/expiry p.45; FAILED catalog p.82 versus recoverable timeout p.12; AUTO_ALLOW p.44 but linear review path p.49 | Define terminal trigger, expiry/run consequences, AUTO_ALLOW path, timeout/recovery literal, SSE lifecycle and status mapping; never implicitly approve |
| OQ-009 / SCR-002 | Mutable revisioned aggregates pp.24–25 versus Case/CaseService/CaseAggregate immutable-derivative registers pp.13/17/26; incomplete close/reopen edges | Amend register semantics; define field schemas/editability, priority formula, reason catalog, close/reopen guards and conflict recovery |
| OQ-010 / SF-007/SCR-003 | Configurable 25 MB p.30; OCR opt-in p.31; viewable low-quality p.32; anchors/quality lacking formats | Define cap units/decompression threshold/OCR control/quality thresholds/preview geometry/remediation; retain unsafe versus low-quality distinction |
| OQ-011 / SCR-007 | Workspace settings/update precondition p.24 associated with `PATCH /v1/cases/{caseId}` | Resolve workspace mutation contract and settings form/save/value sources; do not send invented workspace patch |
| OQ-012 / SCR-005 | Required-field completion p.58 without field list; rationale/optional annotations p.45; override p.46 | Define required UI fields/decision schema/expiry/assignment/override workflow and success/failure navigation |
| OQ-013 / SCR-006 | Operator credential revocation p.27, partial quarantine p.29, visible provisioning p.78 | Define role mapping/buttons/reauthorization/retry bounds/status/warning/remediation presentation |
| OQ-014 / SCR-008 | Immutable/redacted audit pp.11/62/83; retention p.66 | Define field visibility/query/download/retention messages and scope-safe audit detail |
| OQ-015 / SF-014–SF-016 | `POST /v1/runs` pp.15–17 versus case-scoped pp.12/40/83; repeated GET/health allocation/event/register associations; p.22 denial checkpoint versus mandatory audit; A2A case_demo vs uuid p.87 | Reconcile exact contracts without treating Appendix A omissions as exclusions; define schemas/errors/SSE and denial ordering; map protocols safely |
| OQ-016 / SF-017 | Two independent checks pp.78–80, Admin + approver p.83, two-person export p.88; no UI placement | Define independent approver procedure, legal-hold outcomes, launch/confirmation and receipt/download controls; do not create screens from APIs |
| OQ-017 / performance | Case latency within 300 ms p.12 versus under 300 ms p.65; configured maxima/admission thresholds undefined | Resolve test boundary/load procedure, quota/retry/timeout thresholds while retaining design-target status |
| OQ-018 / architecture dependencies | p.90 requires dated choices; p.10 encryption isolation/rotation tradeoff | Decide region/search/identity/approved models/corporate retention/connector permissions before implementation lock; resolve encryption tradeoff before enterprise general availability |

Source IDs for conflicts are retained in the corresponding requirement sections and root relations. No conflicts are resolved by repetition or majority voting. Specific domain semantics support case edits; immutable evidence/revisions/approved lineage remain immutable, while the inconsistent register must be amended.

### Example configuration is not approved UI behavior

Appendix F p.90 contains examples: `release: r1.0`; `max_plan_depth: 8`, `max_tool_calls: 16`, `run_timeout_seconds: 180`, `replay_dedup_hours: 24`; `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `embed_dimension: 1536`, `hybrid_rrf_k: 60`; `auto_publish_classification: INTERNAL`, `require_human_review_for: [HIGH_RISK, RESTRICTED]`, `self_approval_allowed: false`; `upload_limit_mb: 25`, `user_data_region: primary-approved-region`; `trace_sample_rate: 0.10`, `diagnostic_retention_days: 30`, `audit_retention_years: 7`. (screen_functions:r1:c31:f1–f4).

Depth eight/sixteen calls, embedding dimension 1536, configurable upload 25 MB, actor/fingerprint retention 24 hours and substantive diagnostic/audit policies have independent chapter evidence; example-only values such as timeout 180, candidate 80, RRF 60, trace sample 0.10 and auto-publish classification are **not approved decisions**. MCP `max_items≤10` is independently tool-specific and does not make example `max_selected_chunks: 10` a global UI limit. Database revision `1`, sensitivity `INTERNAL` and `now()` defaults likewise remain database-level evidence rather than invented browser initial values.

### Later-stage dependencies

No previous specifications exist; this is Stage 1. API schemas/contracts, backing data completeness, asynchronous jobs and architecture decisions are **To be defined in a later stage**. Appendix B is selected-field/abbreviated DDL, not a complete schema; production workspace-tenancy enforcement still must be added (pp.85–86 [screen_functions:r1:c27:f1–f7]). Do not rewrite this file's confirmed identifiers when later stages reconcile contracts; record required amendments against SCR/SF/OQ IDs.

Stage 8 must consolidate these unresolved items in `08_architecture_decision.md` with links to `01_screen_functions.md` and the affected identifiers. It must not invent a selected provider, architecture, owner, deadline or approval. The specification remains provisional pending separate root approval.
