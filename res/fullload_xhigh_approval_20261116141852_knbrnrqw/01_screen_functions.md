# 1. Screen Function Specification

## Scope and Users

### Specification Basis and Requirement Status

| Item | Definition |
|---|---|
| Output file | `01_screen_functions.md` |
| Application | OrionDesk AI |
| Source document | `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Source baseline | Document ID `OD-AI-DDS-001`; release `R1.0`; design revision `1.3` |
| Source status | Fictional reference architecture. Its requirements are normative for the sample application, not evidence of production performance. |
| Citation convention | **S** denotes `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf`. Every citation below specifies the original PDF page and section or figure. |
| Identifier convention | `SCR-xxx` identifies a screen; `SCR-xxx-Fxx` a field or displayed item; `SCR-xxx-Axx` an operation or event. These are specification identifiers, not new API or database identifiers. The source does not provide screen IDs. |
| Confirmed | Explicitly supported by the source, including requirements of the fictional baseline. |
| Needs confirmation | Missing, ambiguous, or conflicting source detail. It is not permission for an implementation AI to choose behavior. |
| Proposal | A suggested UI arrangement or representation, not a confirmed source requirement. |
| Earlier specifications | None. This is Stage 1. API, data, processing, and architectural specifications are **To be defined in a later stage**. |

**Confirmed:** The eight primary screens named in §16.1.1 must exist. Illustrative titles, navigation labels, data values, and repeated dashboard panels are retained separately from confirmed functional contracts. The sample figures do not establish complete forms or API response schemas.  
**Source:** S, pp. 57–60, §§16.1–16.5 and Figure 16.2; p. 2, Document Map.

### Business Activities and Scope

| ID | Status | Business activity and scope | Source |
|---|---|---|---|
| SF-SCP-001 | Confirmed | Create enterprise knowledge cases, supply business context and attachments, classify cases, and correct classification labels with a reason code. | S, pp. 11–12, §§2.1–2.2.1 |
| SF-SCP-002 | Confirmed | Search permitted evidence, inspect immutable source versions and anchors, request grounded AI drafts, and examine execution progress and policy checkpoints. | S, p. 12, §2.2.2; pp. 30–36, §§8.1–9.3; pp. 40–42, §§11.1–11.3 |
| SF-SCP-003 | Confirmed | Route uncertain, sensitive, and high-impact recommendations to authorized human reviewers. Publish only when required evidence and approval policy are satisfied. | S, pp. 11–13, Chapter 2; pp. 44–46, Chapter 12 |
| SF-SCP-004 | Confirmed | Edit authorized case metadata, execute explicit case-state transitions, and close cases while preserving approved-output lineage. Reopening requires a new revision. | S, pp. 24–26, §§6.1–6.3 |
| SF-SCP-005 | Confirmed | Manage connectors and workspace policy, inspect synchronization health, and obtain immutable audit evidence subject to access and redaction scope. | S, p. 11, §2.1.1; pp. 27–29, Chapter 7; pp. 61–63, Chapter 17 |
| SF-SCP-006 | Confirmed | Support manual case editing and evidence search during generation outages. Lexical retrieval may continue during vector-index degradation with a visible reduced-quality flag. Authorization and approval controls remain enforced. | S, pp. 68–70, Chapter 19; p. 79, §22.2.1 |
| SF-SCP-007 | Confirmed functional capability; screen placement Needs confirmation | Expose usage information and controlled benchmark evaluations. Support controlled workspace export and deletion with independent approval checks and legal-hold handling. | S, pp. 64–66, Chapter 18; pp. 74–76, Chapter 21; pp. 78–80, Chapter 22; p. 83, Appendix A.2 |
| SF-SCP-008 | Needs confirmation | Exact UI placement for membership administration, legal holds, provisioning, export, deletion, design-baseline administration, and operator replay. Their APIs or operational requirements do not establish additional screens. | S, pp. 8–10, Chapter 1; pp. 21–23, Chapter 5; pp. 48–50, Chapter 13; pp. 61–63, Chapter 17; pp. 78–80, Chapter 22 |

### Explicit Exclusions and Deferrals

| Category | Status | Boundary and reason | Source |
|---|---|---|---|
| Physical automation and irreversible financial transactions | Out of scope | The platform processes enterprise knowledge and user-submitted cases, not these activities. Financial-impact categories may still be policy inputs. | S, p. 9, §1.2.1; p. 44, §12.1.1 |
| Foundation-model fine-tuning | Out of scope | Explicitly excluded from the platform. | S, p. 9, §1.2.1 |
| Unrestricted browsing and administrative cloud permissions for agents | Out of scope | Explicitly excluded; the browser must not submit arbitrary tool definitions. | S, p. 9, §1.2.1; p. 7, Architecture at a Glance |
| Application-hosted GPU inference | Out of scope | Providers are external dependencies; GPU inference is not hosted within the application. | S, p. 19, §4.2.1 |
| Cross-region active/active mutation, OCR beyond English, and customer-managed model weights | Deferred from this baseline | The source explicitly defers these capabilities. English OCR fallback remains opt-in. | S, p. 10, §1.3.2; p. 31, §8.2.1 |
| Secrets and internal model prompts in tenant export | Out of scope for export contents | Explicitly excluded from the export package. | S, p. 79, §22.3.1 |
| Native mobile screens, browser compatibility matrix, and responsive breakpoints | Needs confirmation | The source specifies a browser client but does not define these categories. They are not explicitly excluded. | S, p. 15, Chapter 3; pp. 57–59, Chapter 16 |

### Users and Permissions

| User or scope term | Confirmed responsibilities and permissions | Restrictions and unresolved details | Source |
|---|---|---|---|
| Analyst | Opens cases, evaluates evidence, creates attachments, and requests AI runs. Can read authorized case revisions, run details, and run streams. | Cannot approve their own high-risk recommendation. Case mutation uses the separate `Owner` scope in Appendix A.2. Whether all Analysts may edit all workspace cases is not established. **OQ-003.** | S, pp. 11–12, §§2.1–2.2; p. 83, Appendix A.2 |
| Reviewer | Approves or rejects recommendations; reads authorized cases, run details, and run streams; inspects exact candidate content, citations, model/prompt version, and policy reasons. | Selection depends on policy, organizational role, reviewer pools, minimum role, and separation of duties. Assignment-specific viewing rights and complete action guards need confirmation. **OQ-003, OQ-013.** | S, p. 11, §2.1.2; p. 45, §12.2; p. 58, §16.2.2; p. 83, Appendix A.2 |
| Workspace Admin / `Admin` | Manages connectors and policy. The API catalog grants `Admin` connector sync, usage access, and evaluation creation. | The mapping between the Workspace Admin archetype and the `Admin` role needs confirmation. Admin alone is insufficient for export or deletion. Administrative status does not establish review permission. **OQ-003, OQ-023.** | S, p. 11, §2.1.1; p. 22, §5.2.1; p. 83, Appendix A.2 |
| Auditor | Obtains immutable evidence without editing case content; sees decision metadata, prompt-template digests, and access events within redacted scope. Reads cursor-paginated immutable audit events. | No permission to alter historical decisions. Direct access to full case or document content is not established by the Auditor role alone. **OQ-003, OQ-019.** | S, p. 11, §§2.1.1–2.1.2; p. 62, §17.3.1; p. 83, Appendix A.2 |
| `Service` | Baseline noninteractive role used for scoped service operations. | No interactive screen access is confirmed. | S, p. 22, §5.2.1 |
| `Owner` | Scope for `PATCH /v1/cases/{caseId}`. | Not listed as a baseline role. Its relationship to case ownership, Analyst role, and workspace membership needs confirmation. **OQ-003.** | S, p. 24, §6.1.2; p. 83, Appendix A.2 |
| `Member` | Scope for `POST /v1/search`. | Not listed as a baseline role. Eligible role combinations and workspace-membership requirements need confirmation. **OQ-003.** | S, p. 22, §5.2.1; p. 83, Appendix A.2 |
| `approver` / elevated override actor | Export and deletion require `Admin + approver`; an override requires elevated role, secondary reviewer, and audited reason. | Exact eligible roles, independent-approval workflow, and screen placement are undefined. **OQ-014, OQ-023.** | S, p. 46, §12.3.2; pp. 78–80, Chapter 22; p. 83, Appendix A.2 |

**SF-AUTH-001 — Confirmed:** Screen visibility is not an authorization boundary. Each operation must evaluate role, tenant, workspace membership, case sensitivity, originating document ACL, action, and segregation-of-duties constraints. Domain services re-evaluate resource attributes within the transaction.  
**Source:** S, pp. 21–23, Chapter 5.

**SF-AUTH-002 — Confirmed:** Foreign-tenant ID substitution must return the same class of not-found response as an absent ID. Denials must not reveal private resource existence.  
**Source:** S, p. 23, §5.3.2; p. 89, `TST-003`.

### Prerequisites

| ID | Status | Prerequisite | Source and adjacent question |
|---|---|---|---|
| SF-PRE-001 | Confirmed | Interactive authentication uses OIDC authorization-code flow with PKCE. Tokens contain issuer, audience, expiry, subject, and tenant. Unexpected algorithms or missing tenancy claims are rejected. | S, p. 21, §5.1.1. Identity provider, login presentation, and post-login destination: **OQ-001.** |
| SF-PRE-002 | Confirmed | The browser must not store long-lived refresh tokens in local storage. A backend-for-frontend **can** issue secure, HttpOnly, SameSite cookies; this is not a mandatory selected architecture. | S, p. 21, §5.1.2. Session-expiry and logout UX: **OQ-001.** |
| SF-PRE-003 | Confirmed | Every request is authenticated and tenant-bound; resource access must satisfy workspace and resource authorization. | S, pp. 21–23, Chapter 5. Tenant/workspace selection mechanism: **OQ-002.** |
| SF-PRE-004 | Confirmed | Incomplete provisioning is visible and blocks connector sync. Provisioning establishes workspace policy, encryption references, role bindings, quotas, and connector stubs. | S, p. 78, §22.1.1. Provisioning-status display location: **OQ-016, OQ-024.** |
| SF-PRE-005 | Confirmed | Evidence must have current permission and resolvable source anchors before it can support generation or citation display. | S, p. 31, §8.3.1; p. 35, §9.3.1 |
| SF-PRE-006 | Confirmed | Durable mutations carry tenant, revision, actor, occurrence time, and correlation context. Trusted identity and tenancy must not be editable user inputs. | S, pp. 11–13, Chapter 2; pp. 24–26, Chapter 6; pp. 44–46, Chapter 12 |
| SF-PRE-007 | Confirmed | New AI runs require admissible workspace tokens, queue age, and provider capacity. Throttling returns HTTP `429` with `Retry-After`; saved cases remain available. | S, p. 69, §19.2.1. Thresholds and UI retry behavior: **OQ-011.** |

## Screen Inventory and Navigation

### Primary and Illustrated Screen Inventory

The first eight entries are **Confirmed primary screens**. `SCR-009` and `SCR-010` retain illustrated navigation destinations without asserting that the source defines their final layouts or their relationship to the eight-screen inventory.

For every confirmed primary screen:

- **Confirmed:** One primary action and a clear status summary are required.
- **Needs confirmation:** Which action is primary, its exact label, and its placement, except where source behavior explicitly names a control.
- **Needs confirmation:** Browser routes, default landing screen, direct-link behavior, parameter handling, and behavior when no case, evidence item, or run is selected.

**Source:** S, p. 57, §16.1.1. See **OQ-004**.

| Screen ID | Name and evidence status | Purpose | Users and display conditions | Navigation origins and destinations | Launch method |
|---|---|---|---|---|---|
| SCR-001 | **Case Queue — Confirmed.** Illustrated title: “Case Queue / Risk Prioritization.” | List cases and summarize case/workflow status. | Authorized case-list users; exact list-access role scope Needs confirmation. Analyst creation permission is confirmed. | Sidebar `Case Queue` is illustrated. Row-to-`SCR-002` navigation is a **Proposal**, not an explicit source interaction. Other sidebar destinations follow authorized navigation. | Browser screen selected through illustrated menu. URL and initial route Needs confirmation. |
| SCR-002 | **Case Detail — Confirmed.** Illustrated title: “Case Detail / Resolution Package.” | Inspect and work on a case, attachments, evidence, drafts, and decision gate. | Authorized Analyst/Reviewer reads; mutations require `Owner` scope. Sensitive content remains resource-guarded. | Illustrated `Case Detail` menu; proposed case-row origin from `SCR-001`. Citation click opens `SCR-003` source view. Proposed run link to `SCR-004` and review-task link to `SCR-005`. | Browser menu or selected case context. Case selection and route Needs confirmation. |
| SCR-003 | **Evidence Viewer — Confirmed.** “Evidence Explorer / Citation Audit” is an illustrated title whose equivalence Needs confirmation. | Inspect permitted source evidence and citation anchors; support evidence search. | Authorized source access. Reviewer inspection before approval is mandatory. Auditor content scope is restricted. | **Confirmed:** Citation click-through opens source document and highlights anchored page range. Illustrated `Evidence Viewer` menu. Return navigation and search placement are Proposals. | Citation click-through is confirmed; menu entry is illustrated. Same-page panel, new route, or new window Needs confirmation. |
| SCR-004 | **Run Timeline — Confirmed.** Illustrated labels: `Agent Runs` and “Agent Run / Execution Trace.” | Show persisted execution stages, checkpoints, and failure information. | Authorized Analyst/Reviewer read and stream access. | `Agent Runs` sidebar is illustrated; mapping to Run Timeline Needs confirmation. Proposed origin from a case run in `SCR-002`; proposed destinations to its case and evidence. | Browser screen; run-context link is a Proposal. Exact route Needs confirmation. |
| SCR-005 | **Review Inbox — Confirmed.** Illustrated title: “Approval Inbox / Binding Decision.” | List policy-routed review tasks and capture binding approval/rejection decisions. | Authorized Reviewers satisfying pool, minimum-role, assignment, and separation-of-duties guards. | `Review Inbox` sidebar is illustrated. **Confirmed:** Review citations must allow source inspection through `SCR-003`. Case/run links are Proposals. | Browser menu; task-selection presentation Needs confirmation. |
| SCR-006 | **Connector Health — Confirmed.** Illustrated menu: `Connectors`; title: “Connector Health / Synchronization.” | Inspect connector capabilities, sync runs, trust warnings, and remediation information; initiate authorized sync. | `Admin` sync permission confirmed. Read-health and credential-operation permissions need confirmation. | `Connectors` sidebar is illustrated. Connection to Policy Settings, sync detail, and remediation UI Needs confirmation. | Browser menu. Connector list/detail arrangement and routes Needs confirmation. |
| SCR-007 | **Policy Settings — Confirmed.** | Manage workspace policy and supported settings with revision protection. | Workspace Admin responsibility confirmed; exact authorization for each setting Needs confirmation. | Not shown as a sidebar entry in the supplied operator mockups. Entry point and destinations Needs confirmation. | Launch method Needs confirmation. |
| SCR-008 | **Audit Explorer — Confirmed.** Illustrated menu: `Audit Events`; title: “Audit Explorer / Event Lineage.” | Query immutable audit events and inspect decision/evidence lineage within redacted scope. | `Auditor` access to audit-event API confirmed. Other roles are not implicitly granted access. | `Audit Events` sidebar is illustrated. Context links from cases/runs/reviews and return navigation are Proposals. | Browser menu. Event-detail route or panel Needs confirmation. |
| SCR-009 | **Overview — Confirmed as an illustrated menu destination; functions Needs confirmation.** | Overview/dashboard purpose is suggested by the label and summary cards, not fully defined. | Permissions and visibility Needs confirmation. | `Overview` sidebar is illustrated. Default landing behavior is not confirmed. | Illustrated browser menu; route and primary action Needs confirmation. |
| SCR-010 | **Usage & Quality — Confirmed as an illustrated menu destination.** “AI Quality / Evaluation Scorecard” is an illustrated screen title. | Usage and benchmark capabilities are confirmed; their combined or separate screen arrangement Needs confirmation. | Usage read and evaluation creation use `Admin`. Evaluation read permissions and screen visibility need confirmation. | `Usage & Quality` sidebar is illustrated. Whether it opens usage, evaluation, tabs, or separate pages Needs confirmation. | Illustrated browser menu. Do not create a separate evaluation screen without resolving **OQ-021**. |

**Sources:** S, p. 7, Reference UI A; p. 14, Figure 2.2; p. 33, Figure 8.2; p. 43, Figure 11.2; p. 47, Figure 12.2; pp. 57–60, §§16.1–16.3 and Figure 16.2; p. 67, Figure 18.2; p. 77, Figure 21.2; p. 81, Figure 22.2; p. 83, Appendix A.2.

### Navigation Requirements

| ID | Status | Requirement | Source / unresolved decision |
|---|---|---|---|
| SF-NAV-001 | Confirmed | Retain navigable access to the eight primary screens and a clear status summary on each. | S, p. 57, §16.1.1 |
| SF-NAV-002 | Confirmed | Citation activation opens the source document and highlights its anchored page range. The displayed citation must first be verified and authorized. | S, p. 57, §16.1.2; p. 35, §9.3.1 |
| SF-NAV-003 | Confirmed | Refreshing a run view reconstructs progress from server state, not ephemeral browser memory. | S, p. 58, §16.2.1 |
| SF-NAV-004 | Needs confirmation | Resolve sidebar aliases, screen-title aliases, and the mismatched active-menu highlights in representative figures. Do not implement the mismatches as navigation rules. | S, Figures 2.2, 11.2, 12.2, 16.2, 18.2, 21.2, and 22.2; **SF-CON-001, OQ-004** |
| SF-NAV-005 | Proposal | Use contextual links from a case to its evidence, runs, and review tasks, preserving the selected resource context. | Proposed arrangement based on related resources; approval and exact navigation require **OQ-004** resolution. |
| SF-NAV-006 | Needs confirmation | Define browser back behavior, unsaved-change handling, inaccessible-link behavior, no-selection states, and retained list position. | S, pp. 57–59, Chapter 16 does not define these details; **OQ-004, OQ-006** |
| SF-NAV-007 | Needs confirmation | Define notification channels, notification destinations, and notification fields. `Notification` is a source component, but its presence does not establish a notification center screen. | S, pp. 58–59, §§16.2.2–16.4; **OQ-025** |

## Functions by Screen

### Shared Field-Contract Conventions

These conventions apply to every field table below. A field’s confirmed existence in a domain record does **not** automatically confirm that it is an editable UI control.

| Attribute | Display-field convention | Input-field convention |
|---|---|---|
| Name and meaning | Defined per row. Technical identifiers are retained where present in the source. | Defined per row; UI labels and wire-field names remain separate where mapping is undefined. |
| Type, length, and format | Exact source data types are stated when available. Otherwise only a semantic representation is described; wire type, maximum length, precision, and encoding are **Needs confirmation**. | Suggested control representations are **Proposals**. No undocumented text length, numeric range, or pattern may be enforced as a confirmed rule. |
| Required status | “Record required” means the source requires stored data, not necessarily a mandatory form input. Otherwise required/nullable status is **Needs confirmation**. | Required fields are enforced only when source-confirmed. Unspecified required-field sets remain unresolved. |
| Initial value | Existing-resource displays use authorized server data. Illustrated values are fixtures, not defaults. | New-input defaults are **Needs confirmation**, except source-confirmed `NEW`, revision `1`, and sensitivity `INTERNAL`. Existing edits begin from the authorized current revision. |
| Editability | Read-only unless the source explicitly supports mutation. | Editing remains subject to operation authorization and revision guards. Exact per-field permissions are **Needs confirmation** when not specified. |
| Constraints and validation timing | Authorization and citation verification occur before protected display. | Server validation occurs before transaction entry or long-running operation allocation, again at domain invariants, and before tool dispatch. Client-side validation is convenience only. Exact blur/change validation timing is **Needs confirmation**. |
| Display conditions | Show only within authorized scope and applicable case/run/task context. More detailed conditional visibility is **Needs confirmation** unless stated. | Applicable operation/context and guards are defined per row. |
| Selectable values | None for read-only fields. | Use the source-confirmed enum or policy/catalog values when defined. Otherwise the value source is **Needs confirmation**. |

**Sources:** S, pp. 21–23, Chapter 5; p. 25, §6.2; p. 35, §9.3.1; pp. 54–56, Chapter 15; p. 86, Appendix B.2.

### Shared Screen Behavior

| ID | Status | Requirement | Source |
|---|---|---|---|
| SF-GEN-001 | Confirmed | Use accessible text for AI artifact labels `DRAFT`, `NEEDS_REVIEW`, and `PUBLISHED`. Color or styling must not substitute for text. These are not additional Case status values. | S, p. 57, §16.1.2 |
| SF-GEN-002 | Confirmed | Target WCAG 2.2 AA behavior, visible focus, semantic regions, and robust keyboard ordering. Live updates announce only meaningful state transitions. | S, p. 58, §16.3.1; p. 89, `TST-011` |
| SF-GEN-003 | Confirmed | Server timestamps remain UTC/RFC 3339. Display workspace-local times with timezone labels. Locale changes presentation, not event ordering or durable API representations. | S, p. 54, §15.1.1; p. 59, §16.3.2 |
| SF-GEN-004 | Confirmed | Never show partial processing as an approved answer or publish an unapproved high-risk response. | S, pp. 11–13, Chapter 2 |
| SF-GEN-005 | Confirmed | Validate state-changing requests before allocating work. If a dependency is unavailable, return a documented retryable error or persisted asynchronous job identifier, never ambiguous success. | S, pp. 11–13, Chapter 2; pp. 24–26, Chapter 6; pp. 44–46, Chapter 12 |
| SF-GEN-006 | Confirmed | Distinguish accepted asynchronous work from completed work. Attachment upload, AI-run creation, connector sync, evaluation creation, export, and deletion return HTTP `202` where cataloged. | S, p. 83, Appendix A.2 |
| SF-GEN-007 | Confirmed | Use revision preconditions for case changes. A conflict returns HTTP `409`, `CASE_VERSION_CONFLICT`, and current revision information. | S, p. 25, §6.2.2; pp. 83–84, Appendices A.2–A.3 |
| SF-GEN-008 | Confirmed | Job-creating POST mutations require `Idempotency-Key`. Identical repeated requests return the original outcome; changed fingerprints under the same key return `IDEMPOTENCY_CONFLICT`. Case keys bind actor and request fingerprint for 24 hours. | S, p. 25, §6.2.2; p. 54, §15.1.2; p. 89, `TST-001`, `TST-002` |
| SF-GEN-009 | Confirmed | Rejected stale or unauthorized mutations leave business state unchanged. Accepted transitions have one accepted business outcome and correlated audit evidence under replay. | S, p. 25, Design checkpoint 6.2; p. 45, Design checkpoint 12.2; p. 89, `TST-007` |
| SF-GEN-010 | Confirmed | Do not expose secrets, raw provider credentials, full prompts, retrieved documents in errors, or unauthorized resource existence. Diagnostic telemetry must not contain source document text or API secrets. | S, pp. 54–56, Chapter 15; p. 64, §18.1.1; p. 84, Appendix A.3 |
| SF-GEN-011 | Confirmed | Retrieved documents and model responses are untrusted data. They cannot authorize tools, change tenant scope, modify approvals, or bypass the deterministic policy engine. The browser never submits arbitrary tool definitions. | S, p. 7, Architecture at a Glance; pp. 38–42, §§10.2–11.3 |
| SF-GEN-012 | Needs confirmation | Exact error placement, loading presentation, empty-state copy, retry controls, disabled-versus-hidden unauthorized controls, focus recovery, and toast/dialog behavior. | S, pp. 57–59, Chapter 16 does not define these details; **OQ-005, OQ-026** |

#### Shared Shell and Illustrated Summary Fields

The following items are confirmed as **illustrated UI content**, not as fully specified production aggregates. Their placement appears repeatedly in sample figures; it does not establish that every production screen must duplicate the panels.

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, timing, conditions, and values | Status / source |
|---|---|---|---|---|---|
| SF-SHELL-F01 | Tenant and release banner | Display text; length and backing fields Needs confirmation | Illustrated; authorized tenant/release context; read-only | No user-editable tenancy. Exact label construction Needs confirmation. | Illustrated Confirmed; S, p. 7, Reference UI A |
| SF-SHELL-F02 | Workspace label | Display text; length Needs confirmation | Illustrated; current authorized workspace; read-only | `Meridian Manufacturing` is fictional fixture data, not a default. Workspace-switch control Needs confirmation. **OQ-002.** | Illustrated Confirmed; S, p. 7, Reference UI A |
| SF-SHELL-F03 | Open cases | Count representation; wire type Needs confirmation | Illustrated; computed value; read-only | Sample `128` is not a limit or default. Which statuses count as open and aggregation scope Needs confirmation. **OQ-027.** | Illustrated Confirmed; S, p. 7, Reference UI A |
| SF-SHELL-F04 | Awaiting review | Count representation; wire type Needs confirmation | Illustrated; computed value; read-only | Sample `14` is not a default. Count of cases, runs, or tasks and permission scope Needs confirmation. **OQ-027.** | Illustrated Confirmed; S, p. 7, Reference UI A |
| SF-SHELL-F05 | Evidence coverage | Percentage representation; precision Needs confirmation | Illustrated; computed value; read-only | Sample `97.6%` is not an acceptance threshold. Formula and denominator Needs confirmation. **OQ-027.** | Illustrated Confirmed; S, p. 7, Reference UI A |
| SF-SHELL-F06 | Service state | Status text; enum Needs confirmation | Illustrated; service-derived value; read-only | Sample `Healthy` is not a complete state vocabulary. Degraded status must be visible when applicable. | S, p. 7, Reference UI A; p. 69, §19.2.2; p. 79, §22.2.1 |
| SF-SHELL-F07 | “Case Evidence & Workflow” rows | Case reference, title, and workflow/status text | Illustrated; server-derived authorized rows; read-only | Human-facing references such as `OD-2026-1042` are not confirmed API UUIDs. Mapping of “Needs review,” “Evidence gap,” and “Published” to aggregates Needs confirmation. **OQ-007, OQ-027.** | Illustrated Confirmed; S, pp. 7 and 14, Reference UI A and Figure 2.2 |

### SCR-001 — Case Queue

#### Fields and Lists

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, timing, display conditions, and selectable-value source | Status / source |
|---|---|---|---|---|---|
| SCR-001-F01 | Case reference / identity | Technical case `id`: UUID, with UUIDv7 identifier policy. Illustrated business reference format is separate and unresolved. | Server-generated; read-only | Display authorized cases only. Do not parse the illustrated `OD-2026-...` reference as an API UUID. **OQ-007.** | S, p. 14, Figure 2.2; p. 51, §14.1.1; p. 86, Appendix B.2 |
| SCR-001-F02 | Case title | Semantic text; wire type and length Needs confirmation | Stored title confirmed; list presentation illustrated; read-only | Current authorized case title. Required creation status Needs confirmation. | S, p. 14, Figure 2.2; p. 24, §6.1.2 |
| SCR-001-F03 | Case/workflow status summary | Case `status`: `TEXT`; artifact and workflow labels are separate vocabularies | Case status record-required; server state; read-only in list | Case states are those in SCR-002-F08. Draft labels use SF-GEN-001. Mixed mockup labels require an explicit mapping. **OQ-027.** | S, p. 14, Figure 2.2; p. 57, §16.1.2; pp. 82 and 86, Appendices A.1 and B.2 |
| SCR-001-F04 | Priority | Semantic derived value; enum and format Needs confirmation | Domain field confirmed; list-column placement Proposal; read-only | Derived from explicit impact and urgency, never model output alone. Formula and list sorting Needs confirmation. **OQ-009.** | S, pp. 24–25, §§6.1.2 and 6.3.1 |
| SCR-001-F05 | Owner and sensitivity | Owner identifier representation Needs confirmation; sensitivity is `TEXT` | Domain data confirmed; list-column placement Proposal; read-only | Authorization applies to sensitivity and workspace context. Owner visibility and list columns Needs confirmation. **OQ-003, OQ-006.** | S, p. 24, §6.1.2; p. 86, Appendix B.2 |
| SCR-001-F06 | Pagination cursor | Cursor token; type, length, and encoding Needs confirmation | API pagination confirmed; initial-request representation Needs confirmation; not manually edited | Obtain subsequent pages with server cursors. Page size, backward traversal, cursor expiry, total count, and snapshot consistency Needs confirmation. **OQ-006.** | S, p. 57, §16.1.1; p. 54, §15.1.1 |
| SCR-001-F07 | Case search/filter/sort controls | No confirmed fields, types, or selectable lists | Needs confirmation | Case Queue existence does not establish text search, status filters, sortable headers, or bulk actions. **OQ-006.** | S, pp. 57–59, Chapter 16; p. 14, Figure 2.2 |

The illustrated shared summary fields are defined in SF-SHELL-F03–F07.

#### Operations and Events

| ID | Operation | Execution conditions and processing | Successful display/navigation | Failure display | Status / source |
|---|---|---|---|---|---|
| SCR-001-A01 | Load cases | Authenticate and apply tenant/resource scope; request `GET /v1/cases?cursor=...`. | Display authorized rows and clear status summary. | Apply shared safe-error rules. A failed request must not be represented as successful retrieval; exact presentation Needs confirmation. | Confirmed list operation; S, p. 57, §16.1.1 |
| SCR-001-A02 | Obtain another page | Submit an applicable server cursor. | Display the returned authorized page. Append-versus-replace and control labels Needs confirmation. | Safe error; invalid/expired cursor response and recovery Needs confirmation. **OQ-006.** | Cursor pagination Confirmed; S, p. 54, §15.1.1 |
| SCR-001-A03 | Create case | Analyst permission; validated case context; idempotency key. Call `POST /v1/cases`. Field definitions are in SCR-002. | HTTP `201`; one case identifier; case starts in `NEW`. Opening SCR-002 after creation is a **Proposal**. | HTTP `422` for schema-invalid input; changed body under reused key produces HTTP `409` `IDEMPOTENCY_CONFLICT`; dependency failures follow SF-GEN-005. | Capability Confirmed; creation-form placement Proposal. S, p. 12, §2.2.1; p. 83, Appendix A.2; p. 89, `TST-001`, `TST-002` |
| SCR-001-A04 | Open selected case | A displayed case is selected and remains authorized. | Proposed navigation to SCR-002 with case context. | Non-disclosing absent/foreign-resource response. | Navigation Proposal; case-read contract Confirmed. S, p. 83, Appendix A.2; p. 23, §5.3.2 |
| SCR-001-A05 | Search, filter, sort, or bulk action | No confirmed execution contract. | Needs confirmation. | Needs confirmation. | **OQ-006.** Do not implement invented query parameters or actions. |

**Primary action:** Needs confirmation. **Proposal:** Create Case for users with Analyst creation permission. **OQ-004.**

### SCR-002 — Case Detail

#### Case Fields

Stored case fields are confirmed by the domain model. Their exact form layout and control types are **Proposals** unless explicitly described as UI displays.

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, timing, display conditions, and selectable-value source | Status / source |
|---|---|---|---|---|---|
| SCR-002-F01 | Case `id` / case reference | `UUID`; UUIDv7 policy. Separate display-reference format Needs confirmation. | Record-required; generated on creation; read-only | Immutable identity; authorized case context. | S, p. 51, §14.1.1; p. 86, Appendix B.2; **OQ-007** |
| SCR-002-F02 | Workspace context / `workspace_id` | `UUID`; human-readable workspace label format Needs confirmation | Record-required; create-time workspace selection/default Needs confirmation; editability Needs confirmation | Must enforce workspace-tenancy membership. Candidate workspaces must be authorized; selector API and move-case behavior undefined. **OQ-002.** | S, pp. 85–86, Appendices B.1–B.2 |
| SCR-002-F03 | Title | Semantic text; wire type and maximum length Needs confirmation | Stored field confirmed; required/default Needs confirmation; authorized mutation supported, per-field edit rights unresolved | Validate submitted payload and domain invariants. Trimming, blank acceptance, and character restrictions Needs confirmation. **OQ-007.** | S, p. 24, §6.1.2; p. 56, §15.3.2 |
| SCR-002-F04 | Description / business context | Semantic text; plain/rich-text format and length Needs confirmation | Stored field confirmed; required/default Needs confirmation; authorized mutation supported | Treat user content as validated data. Attachment-independent business-context structure Needs confirmation. **OQ-007.** | S, p. 12, §2.2.1; p. 24, §6.1.2; p. 38, §10.2.1 |
| SCR-002-F05 | Impact | Explicit business input; type and selectable values Needs confirmation | Input existence Confirmed; required/default/edit rights Needs confirmation | Used with urgency for priority. No model-only priority calculation. Exact matrix and validation Needs confirmation. **OQ-009.** | S, p. 25, §6.3.1 |
| SCR-002-F06 | Urgency | Explicit business input; type and selectable values Needs confirmation | Input existence Confirmed; required/default/edit rights Needs confirmation | Used with impact for priority. Exact matrix Needs confirmation. **OQ-009.** | S, p. 25, §6.3.1 |
| SCR-002-F07 | Priority | Derived business value; type, enum, and format Needs confirmation | Stored field confirmed; derived initial value; direct editability Needs confirmation | Must not derive solely from model output. Manual overrides, if any, are not defined. **OQ-009.** | S, pp. 24–25, §§6.1.2 and 6.3.1 |
| **SCR-002-F08** | **Case status / `status`** | **`TEXT`; exact values: `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED`** | **Record-required; initial `NEW`; changes only through guarded state operations, not unrestricted text editing** | **Allowed edges are defined in SCR-002-T01–T06 below and executed through SCR-002-A04. Role, current revision, and approval requirements apply. Closing/reopening details remain unresolved. OQ-008.** | **Confirmed; S, p. 25, §6.2.1; p. 82, Appendix A.1; p. 86, Appendix B.2** |
| SCR-002-F09 | Owner | Principal reference; identifier/wire format Needs confirmation | Stored field confirmed; required/default and reassignment rights Needs confirmation | `Owner` is the PATCH scope. Eligible owner list and assignment API are undefined. **OQ-003, OQ-007.** | S, p. 24, §6.1.2; p. 83, Appendix A.2 |
| SCR-002-F10 | Sensitivity / `sensitivity` | `TEXT`; information classes: `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` | Record-required; database default `INTERNAL`; editing role and timing Needs confirmation | Policy uses the maximum class of included material. Classification selector mapping and lowering-class safeguards Needs confirmation. **OQ-010.** | S, p. 62, §17.2.1; p. 86, Appendix B.2 |
| SCR-002-F11 | Revision / `revision` | `BIGINT`; monotonic revision. HTTP representation and `If-Match` encoding Needs confirmation. | Record-required; default `1`; read-only | Submit revision precondition for mutation; conflicts report actual/current revision. **OQ-007.** | S, p. 25, §6.2.2; pp. 84 and 86, Appendices A.3 and B.2 |
| SCR-002-F12 | Created/updated timestamps / `created_at`, `updated_at` | `TIMESTAMPTZ`; API RFC 3339; workspace-local display with timezone label | Record-required; database defaults `now()`; read-only | Locale must not change ordering or stored representations. | S, p. 59, §16.3.2; p. 86, Appendix B.2 |
| SCR-002-F13 | Classification labels, confidences, and provenance | Labels/structured provenance and confidence values; schemas, precision, and ranges Needs confirmation | Asynchronously attached; read-only generated values; user can correct labels | Label correction requires reason code. Label catalog and confidence display format undefined. **OQ-010.** | S, p. 12, §2.2.1 |
| SCR-002-F14 | Label-correction reason code | Code; type, length, and allowed-value source Needs confirmation | Required for label correction; initial value Needs confirmation; authorized input | Validate with correction submission. Client validation timing and correction endpoint undefined. **OQ-010.** | S, p. 12, §2.2.1 |
| SCR-002-F15 | Contractual deadline / advisory breach prediction | Deadline timestamp; prediction schema and format Needs confirmation | Domain behavior confirmed; display placement Proposal; read-only | Business calendars use workspace timezone. Prediction is advisory and cannot change contractual deadlines. **OQ-009.** | S, p. 25, §6.3.1 |
| SCR-002-F16 | Current approved result / candidate artifact | Immutable artifact representation; text/content schema and length Needs confirmation | Current approved result stored; present when available; read-only approved artifact | Distinguish candidate from approved/published result. Approved pointer changes only through the satisfied publication gate. Direct candidate editing is not specified. **OQ-012.** | S, p. 24, §6.1.2; p. 45, §12.3.1 |
| SCR-002-F17 | Artifact display status | Exact display vocabulary `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` | Server-derived; read-only | Accessible text required; never equate an unfinished run with `PUBLISHED`. | S, p. 57, §16.1.2 |
| SCR-002-F18 | Decision gate: policy, evidence, model, approval, status | Policy outcome vocabulary is confirmed; other panel schemas Needs confirmation | Illustrated display; current applicable server records; read-only | Mockup values `HUMAN_REVIEW`, `5 verified citations`, `gateway-r1.2`, `Assigned to reviewer`, `Awaiting decision` are examples, not defaults. Keep retrieval, generation, policy, and reviewer records separate. | S, p. 7, Reference UI A; p. 12, §2.2.2; p. 44, §12.1.2 |
| SCR-002-F19 | Requested grounded-answer input / requested action | Validated user input; request schema, length, and selectable actions Needs confirmation | Analyst request capability Confirmed; required/default Needs confirmation; input placement Proposal | Browser cannot define arbitrary tools or permissions. Financial-impact input and clarification UI mapping undefined. **OQ-011, OQ-012.** | S, p. 12, §2.2.2; p. 38, §10.2.1; p. 44, §12.1.1 |

#### Confirmed Case-State Transitions

**SCR-002-F08 and SCR-002-A04 must use the following confirmed portion of the transition contract.** An allowed edge is not authorization to bypass role, revision, evidence, or approval checks.

| Transition ID | From | To | Status | Applicable guards and unresolved details | Source |
|---|---|---|---|---|---|
| SCR-002-T01 | `NEW` | `TRIAGED` | Confirmed allowed edge | Authorized actor/action and current revision; apply documented role and approval requirements where applicable. Exact actor and classification-completion trigger Needs confirmation. | S, p. 25, §6.2.1; p. 82, Appendix A.1 |
| SCR-002-T02 | `TRIAGED` | `IN_PROGRESS` | Confirmed allowed edge | Authorized actor/action and current revision; detailed actor/action guard Needs confirmation. | S, p. 25, §6.2.1; p. 82, Appendix A.1 |
| SCR-002-T03 | `IN_PROGRESS` | `PENDING_APPROVAL` | Confirmed allowed edge | Authorized actor/action, current revision, and applicable policy/approval requirements. Exact initiating actor, trigger, and required task linkage Needs confirmation. | S, p. 25, §6.2.1; p. 82, Appendix A.1 |
| SCR-002-T04 | `IN_PROGRESS` | `RESOLVED` | Confirmed allowed edge | Authorized actor/action and current revision. Required evidence and satisfied approval policy remain obligatory; this edge does not imply approval can be skipped. Detailed resolution guard Needs confirmation. | S, p. 25, §6.2.1; p. 12, §2.2.2; pp. 44–46, Chapter 12; p. 82, Appendix A.1 |
| SCR-002-T05 | `PENDING_APPROVAL` | `RESOLVED` | Confirmed allowed edge | Authorized actor/action, current revision, and applicable approval requirements, including exact reviewed-hash binding and separation of duties. Detailed actor and approval-to-case-state linkage Needs confirmation. | S, p. 25, §6.2.1; pp. 44–46, Chapter 12; p. 82, Appendix A.1 |
| SCR-002-T06 | `PENDING_APPROVAL` | `IN_PROGRESS` | Confirmed allowed edge | Authorized actor/action and current revision. Exact rejection/rework trigger and approval-record consequences Needs confirmation; do not assume automatic transition on every Reject action. | S, p. 25, §6.2.1; p. 46, §12.3.2; p. 82, Appendix A.1 |
| SCR-002-T07 | Not specified | `CLOSED` | Closing capability Confirmed; closing edge Needs confirmation | `POST /v1/cases/{caseId}/close` exists. Closure snapshots approved answer, cited document versions, and reviewer decisions. Permitted originating state and detailed actor/approval guards are unspecified. | S, pp. 24–26, §§6.1.2–6.3.2 |
| SCR-002-T08 | `CLOSED` | Reopening target not specified | New-revision reopening exception Confirmed; target and operation contract Needs confirmation | `CLOSED` is final unless explicitly reopened as a new revision. Preserve immutable approved-output lineage. Reopening target, actor, approval rules, and endpoint are not defined. | S, p. 25, §6.2.1; p. 24, Chapter 6 invariant |

**Confirmed shared guards:**

1. Access evaluates role, tenant, workspace membership, sensitivity, document ACL, action, and segregation of duties.
2. Clients submit `If-Match` revision conditions; stale updates return `CASE_VERSION_CONFLICT` with current revision.
3. Rejected stale or unauthorized writes leave business state unchanged.
4. Publication requires supported evidence and satisfied approval policy.
5. High-risk self-approval is prohibited; required human review cannot be bypassed.
6. An approval applies only to the exact reviewed content hash.
7. Closed cases preserve immutable approved-output lineage.

**Sources:** S, pp. 21–23, Chapter 5; p. 25, §§6.2.1–6.2.2; p. 12, §2.2.2; pp. 44–46, Chapter 12.

**Needs confirmation — OQ-008:** Complete only the missing closing edge, reopening target/operation, and detailed actor, trigger, and approval guards. The six confirmed normal edges above must not be replaced by an entirely TBD transition matrix. No additional normal transition is authorized by this specification.

#### Attachment Fields

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, timing, conditions, and selectable values | Status / source |
|---|---|---|---|---|---|
| SCR-002-F20 | Attachment file | Binary file; R1 supports PDF, DOCX, HTML, and UTF-8 text | File required when invoking attachment upload; initial selection Needs confirmation; selected by authorized Analyst | MIME signature and extension must agree. Configurable per-file cap is `25 MB`. Decompression-bomb threshold exists but value is undefined. MB-to-byte conversion, file count, filename length, and multipart contract Needs confirmation. **OQ-015.** | S, p. 30, §8.1.1; p. 83, Appendix A.2; p. 90, Appendix F |
| SCR-002-F21 | Attachment/document/version identity | Immutable identifiers; UUID policy; exact response-field mapping Needs confirmation | Server-generated; read-only | Attachments reference immutable document versions. | S, p. 24, §6.1.2; p. 51, §14.1.2; p. 85, Appendix B.1 |
| SCR-002-F22 | Document processing status | Exact states: `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED` | Server-derived; read-only | Upload acceptance is not search readiness. State-transition detail and refresh mechanism Needs confirmation. **OQ-015.** | S, pp. 30–32, Chapter 8; p. 82, Appendix A.1 |
| SCR-002-F23 | Extraction quality flags | Empty-page ratio, unknown-character ratio, table-loss indicators, language confidence; schemas/ranges Needs confirmation | Server-generated; read-only; applicable after extraction | Low-quality documents remain viewable but are excluded from autonomous recommendations. Quality thresholds undefined. | S, p. 32, §8.3.2; **OQ-015** |
| SCR-002-F24 | OCR opt-in and provenance | Semantic option and provenance marker; UI control and wire type Needs confirmation | OCR fallback opt-in; default not-enabled behavior follows opt-in requirement; authorized input placement Needs confirmation | OCR output must be provenance-marked. Non-English OCR is deferred. | S, p. 31, §8.2.1; p. 10, §1.3.2; **OQ-015** |
| SCR-002-F25 | Quarantine/remediation information | Reason code, correlation ID, remediation path; formats Needs confirmation | Server-derived; read-only | Unsafe attachments do not enter search. The source does not establish that quarantined unsafe content can be opened. | S, p. 30, §8.1.2; p. 29, §7.3.2; **OQ-015** |

#### Operations and Events

| ID | Operation | Execution conditions and processing | Successful display/navigation | Failure display | Status / source |
|---|---|---|---|---|---|
| SCR-002-A01 | Read current case | Authorized Analyst/Reviewer; `GET /v1/cases/{caseId}`. | HTTP `200`; current authorized revision and applicable result/status data. | Non-disclosing absent/foreign-tenant response; safe dependency error. | Confirmed; S, p. 83, Appendix A.2; p. 23, §5.3.2 |
| SCR-002-A02 | Save case metadata | `Owner` scope; validated supported patch; `If-Match` revision condition; `PATCH /v1/cases/{caseId}`. | HTTP `200`; updated authorized case and monotonic revision; durable audit evidence. Post-save focus and presentation Needs confirmation. | HTTP `409` `CASE_VERSION_CONFLICT` with current revision; HTTP `422` for schema-invalid request; denied/stale action leaves state unchanged. No silent overwrite. | Confirmed; S, p. 25, §6.2.2; p. 83, Appendix A.2; p. 84, Appendix A.3 |
| SCR-002-A03 | Correct classification label | Authorized user; correction includes reason code; classification provenance retained. | Corrected labels and applicable provenance are available. Exact display/update behavior Needs confirmation. | Safe validation/permission error; endpoint and error code undefined. | Capability Confirmed; endpoint/control placement Needs confirmation. S, p. 12, §2.2.1; **OQ-010** |
| **SCR-002-A04** | **Execute case-state change** | **Use SCR-002-F08 and confirmed edges SCR-002-T01–T06. Submit guarded `PATCH /v1/cases/{caseId}` with `If-Match`; verify allowed edge, actor/action authorization, current revision, and applicable approval/evidence guards before mutation.** | **HTTP `200`; selected confirmed target status, updated monotonic revision, and correlated `CaseStateChanged` audit/event evidence. Exact button/menu labels Needs confirmation.** | **Stale revision: HTTP `409` `CASE_VERSION_CONFLICT` with current revision. Unauthorized or invalid transition: reject without changing business state; specific invalid-transition code/status Needs confirmation.** | **Confirmed transition capability and six edges; detailed guards Needs confirmation. S, p. 25, §§6.2.1–6.2.2; p. 26, §§6.4–6.5; p. 83, Appendix A.2; OQ-008** |
| SCR-002-A05 | Upload attachment | Authorized Analyst; validate allowed type, MIME/extension agreement, configured size and archive safety; call `POST /v1/cases/{caseId}/attachments` with job idempotency. Scan before parsing; disable macros; do not fetch embedded remote references. | HTTP `202`; persisted ingestion operation; display processing status. Unsafe content is quarantined, not indexed. | Oversized, mismatched, unsafe, or malformed input fails closed; exact upload error codes undefined. Safe quarantine/remediation information when applicable. | Confirmed; S, pp. 30–32, Chapter 8; p. 83, Appendix A.2 |
| SCR-002-A06 | Request grounded draft / new AI run | Authorized Analyst; saved authorized case; validated request and idempotency key; admission checks; `POST /v1/cases/{caseId}/runs`. | HTTP `202`; run created immediately; subscribe to SSE and display retrieval, generation, and policy stages. SCR-004 navigation is a Proposal. | `429` plus `Retry-After` when throttled; dependency error or persisted job outcome; invalid model output and unsupported evidence never shown as published. | Confirmed; S, p. 12, §2.2.2; p. 58, §16.2.1; p. 69, §19.2.1; p. 83, Appendix A.2 |
| SCR-002-A07 | Close case | Closing operation exists at `POST /v1/cases/{caseId}/close`. Current revision, authorization, and applicable approval requirements apply. Originating state and exact request contract Needs confirmation. | Snapshot approved answer, cited document versions, and reviewer decisions; preserve immutable lineage. Exact HTTP result and navigation undefined. | Reject stale/unauthorized actions without state change. Do not guess closing state guard or error code. | Confirmed closure behavior; missing edge **OQ-008**. S, pp. 24–26, §§6.1.2–6.3.2 |
| SCR-002-A08 | Reopen closed case | Explicit reopening must create a new revision. Actor, target state, endpoint, and request fields Needs confirmation. | New-revision lineage must preserve prior approved outputs. Final display/navigation undefined. | No ordinary in-place transition out of `CLOSED`; undefined reopening contract must not be implemented by assumption. | Confirmed exception; implementation details Needs confirmation. S, p. 25, §6.2.1; **OQ-008** |
| SCR-002-A09 | Publication-gate completion event | Required evidence exists; policy is satisfied; applicable approval matches exact artifact; authorization rechecked. | Final response pointer updates atomically with the satisfied gate; display `PUBLISHED` only for the published artifact. | Changed hash, revoked evidence access, unsatisfied approval, or replay with a different artifact cannot publish. Specific UI error mapping undefined. | Confirmed event-driven behavior; no publish button/endpoint confirmed. S, pp. 45–46, §§12.3–12.5 |
| SCR-002-A10 | Rework denied recommendation | Rework as a new run revision, not retroactive approval. Exact initiation fields and relation to a new run request Needs confirmation. | New candidate/run revision remains distinct from immutable prior denial and approval history. | Never mark denied historical content as approved. | Confirmed; S, p. 46, §12.3.2; **OQ-012** |
| SCR-002-A11 | Continue manual work in degraded mode | Generation unavailable, but case/evidence services remain available and authorization passes. | Manual editing and evidence search remain usable; visible degraded status. | No degradation-based authorization or approval bypass. | Confirmed; S, p. 69, §19.2.2; p. 79, §22.2.1 |

**Primary action:** Needs confirmation. **Proposal:** Request Grounded Draft for an authorized Analyst. This does not remove Save, attachment, state, or closure capabilities. **OQ-004.**

### SCR-003 — Evidence Viewer

#### Fields, Search, and Source Display

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, timing, conditions, and selectable-value source | Status / source |
|---|---|---|---|---|---|
| SCR-003-F01 | Evidence/search query | Semantic text. MCP `knowledge.search@v1` defines `query: string`; public search schema/length Needs confirmation. | Search capability Confirmed; screen placement Proposal; required/default Needs confirmation; authorized input | Public request is `POST /v1/search`. Do not assume the MCP input schema is the public schema. **OQ-017.** | S, pp. 34–36, Chapter 9; p. 83, Appendix A.2; p. 87, Appendix C.2 |
| SCR-003-F02 | Search/evidence result list | Evidence items with source and anchor metadata; full response schema Needs confirmation | Server-derived; read-only | Lexical and vector candidates use reciprocal rank fusion and deterministic re-ranking; diversity limits redundant document hits. ACL filtering precedes text release. UI sorting and pagination undefined. **OQ-017.** | S, p. 35, §9.2; p. 34, Chapter 9 invariant |
| SCR-003-F03 | Source title | Semantic text; length Needs confirmation | Included in response evidence item; read-only | Verify citation before display; only authorized evidence. | S, p. 35, §9.3.1 |
| SCR-003-F04 | Document revision / `document_version_id` | Immutable version identity; exact public mapping Needs confirmation | Response includes document revision; read-only | Open the cited immutable version, not an arbitrary latest replacement. | S, p. 35, §9.3.1; p. 51, §14.1.2 |
| SCR-003-F05 | Page anchor / range | Source page number/anchor; page index conventions and range schema Needs confirmation | Required resolvable anchor for generated citation; read-only | Click-through highlights anchored page range. Nonpaginated HTML/text/DOCX anchor behavior Needs confirmation. **OQ-018.** | S, p. 31, §§8.2.1 and 8.3.1; p. 57, §16.1.2 |
| SCR-003-F06 | Bounding box / table/layout annotations | Optional `bbox`; coordinate system and schema Needs confirmation | Optional bounding box; read-only | PDF blocks retain page and bounding boxes; tables retain row/column annotations. Viewer rendering detail undefined. | S, p. 31, §8.2.1; p. 85, Appendix B.1 |
| SCR-003-F07 | Chunk ID and citation identifier | Chunk identifier; citation identifiers opaque to end users | Response evidence includes chunk ID; read-only technical metadata | Resolve and verify internally. Do not require users to enter or interpret opaque citation IDs. | S, p. 35, §9.3.1 |
| SCR-003-F08 | Source URI, file hash, ACL digest | Stored provenance fields; public exposure, digest encoding, and lengths Needs confirmation | Chunk provenance stored; response evidence includes ACL digest; read-only | Current permission required. Source access uses access-controlled short-lived signed URLs where applicable; lifetime undefined. No arbitrary URL/file access through tools. | S, p. 31, §8.3.1; p. 35, §9.3.1; p. 52, §14.3.1; p. 87, Appendix C.2 |
| SCR-003-F09 | Source content / evidence passage | Authorized document and normalized content; display schema Needs confirmation | Read-only source/version content | Preserve claims; mark OCR provenance and untrusted material. Low-quality safe documents remain viewable but cannot support autonomous recommendations. Quarantined-content viewing not established. | S, pp. 31–32, §§8.2–8.3; p. 61, §17.1.2 |
| SCR-003-F10 | Quality / reduced-quality warning | Extraction flags and degradation text; exact format Needs confirmation | Read-only; conditional on quality/degradation | Lexical fallback during vector degradation requires a visible reduced-quality flag. | S, p. 32, §8.3.2; p. 69, §19.2.2 |
| SCR-003-F11 | Unsupported evidence outcome | Literal `NO_SUPPORTED_EVIDENCE` | Server-derived; read-only when evidence/confidence insufficient | No fabricated context. Clarification or human routing may follow; detailed UI path undefined. **OQ-017.** | S, p. 36, §9.3.2 |
| SCR-003-F12 | Search filters, result count selector, page controls, document zoom/search controls | No confirmed UI contract | Needs confirmation | Source retrieval budgets are not UI pagination limits. Do not create undocumented filters or viewer controls as confirmed requirements. **OQ-017, OQ-018.** | S, pp. 34–36, Chapter 9; pp. 57–59, Chapter 16 |

**Confirmed reference retrieval configuration:** `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `embed_dimension: 1536`, and `hybrid_rrf_k: 60`. MCP `max_items` is `int<=10`. These are backend/reference contracts, not confirmed public page-size or editable screen limits.  
**Source:** S, p. 90, Appendix F; p. 87, Appendix C.2.

#### Operations and Events

| ID | Operation | Execution conditions and processing | Successful display/navigation | Failure display | Status / source |
|---|---|---|---|---|---|
| SCR-003-A01 | Load case evidence | Authorized case/evidence scope; `GET /v1/cases/{caseId}/evidence`. | Display permitted evidence metadata and citations. | Non-sensitive authorization/dependency error; never display unauthorized passages. | Confirmed endpoint; S, pp. 57–59, §§16.1.2–16.4 |
| SCR-003-A02 | Search permitted evidence | `Member` scope and current document permissions; validated query; `POST /v1/search`. | HTTP `200`; ACL-filtered lexical/semantic evidence; display applicable quality warnings. | `NO_SUPPORTED_EVIDENCE` for insufficient evidence; safe error on denied or failed retrieval. | Confirmed capability; screen placement Proposal. S, pp. 34–36, Chapter 9; p. 83, Appendix A.2 |
| SCR-003-A03 | Activate citation / inspect source | Verify citation and current source permission; resolve stored anchor, using `GET /v1/evidence/{evidenceId}` where applicable. Exact binary-content route undefined. | Open cited source document and highlight anchored page range. | Do not open unresolved or unauthorized evidence. Exact failure message and expired signed-URL recovery Needs confirmation. | Confirmed; S, p. 35, §9.3.1; p. 57, §16.1.2; **OQ-018** |
| SCR-003-A04 | Retrieve after source ACL change | Apply changed ACL and invalidate affected cache before serving results. | Next query contains no forbidden evidence. | Stale visibility is a security incident; fail closed rather than show stale cached content. | Confirmed; S, p. 28, §7.2.2; p. 53, §14.3.2; p. 89, `TST-004` |
| SCR-003-A05 | Return to case/review/run | Exact origin context and browser behavior unresolved. | Context-preserving return is a Proposal. | Needs confirmation. | **OQ-004, OQ-018** |
| SCR-003-A06 | Clarify or route to human | Insufficient evidence may cause clarification or human routing. Selection rule and request contract undefined. | Display only the server-selected supported path once defined. | No fabricated evidence or automatic approval. | Permitted behavior Confirmed; detailed workflow Needs confirmation. S, p. 36, §9.3.2 |

**Primary action:** Needs confirmation. Inspect Source or Search Evidence are possible **Proposals**, not an approved selection.

### SCR-004 — Run Timeline

#### Fields

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, timing, conditions, and selectable values | Status / source |
|---|---|---|---|---|---|
| SCR-004-F01 | Run and case identity | Identifier policy UUIDv7; exact response mapping Needs confirmation | Server-generated/context-derived; read-only | Authorized Analyst/Reviewer scope. | S, p. 51, §14.1.1; p. 83, Appendix A.2; p. 85, Appendix B.1 |
| SCR-004-F02 | Run status / stage | Exact Run states: `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED` | Server state; immediate creation followed by persisted stages; read-only | Keep separate from Case and artifact display status. Timeout and missing-approval mappings unresolved. **OQ-011.** | S, p. 49, §13.2.1; p. 82, Appendix A.1 |
| SCR-004-F03 | Stage/step list | `run_steps` includes `step_kind`, `status`, `checkpoint`; complete enums/schema Needs confirmation | Persisted server steps; read-only | Show retrieval, generation, and policy progress and exact failed checkpoint. | S, p. 41, §11.3.1; p. 58, §16.2.1; p. 85, Appendix B.1 |
| SCR-004-F04 | Plan revision, dependencies, and checkpoints | Plan revision and DAG metadata; detailed types Needs confirmation | Stored before side effects; read-only | Bounded plan depth `8`, maximum tool invocations `16`; checkpoints replayable. | S, p. 40, §11.1.2; p. 90, Appendix F |
| SCR-004-F05 | Failure checkpoint and reason | Safe checkpoint/reason metadata; error schema Needs confirmation | Conditional on failure; read-only | Visible status reports exactly which checkpoint failed. Do not expose raw prompts, documents, or secrets in diagnostics. | S, p. 41, §11.3.1; p. 64, §18.1.1 |
| SCR-004-F06 | Runtime/call/token budget and usage | Budget metadata; units and response schema Needs confirmation | Server data; read-only display placement Proposal | Reference `run_timeout_seconds: 180`; quota exhaustion is terminal for the current run. Do not infer a cancellation control or countdown semantics. **OQ-011.** | S, p. 38, §10.3.1; p. 90, Appendix F |
| SCR-004-F07 | Model/prompt version and policy outcome | Version identifiers and policy result: `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY` | Server records; read-only | Model output cannot override policy or authorize tools. Exact timeline exposure schema Needs confirmation. | S, p. 44, §12.1.2; p. 58, §16.2.2 |
| SCR-004-F08 | Evidence metadata / citations | Evidence contract in SCR-003 | Server-derived; read-only | Current source permission and resolvable anchors required. | S, p. 83, Appendix A.2; p. 35, §9.3.1 |
| SCR-004-F09 | Event offset / resume cursor | Monotonically increasing SSE offset; exact type/length Needs confirmation | Last received server offset; read-only transport context | Reconnect sends `Last-Event-ID`; backfill only retained events within caller scope. Retention/expiry behavior undefined. **OQ-011.** | S, p. 55, §15.2.1 |
| SCR-004-F10 | Stage timestamps and correlation context | UTC/RFC 3339 timestamps; identifiers; complete display schema Needs confirmation | Server-derived; read-only | Workspace-local presentation and safe diagnostic identifiers only. | S, p. 48, §13.1.1; p. 59, §16.3.2; p. 64, §18.1.1 |

#### Operations and Events

| ID | Operation | Execution conditions and processing | Successful display/navigation | Failure display | Status / source |
|---|---|---|---|---|---|
| SCR-004-A01 | Load persisted run and steps | Authorized Analyst/Reviewer run read; `GET /v1/runs/{runId}`; steps endpoint `GET /v1/runs/{runId}/steps` exists, but its exact scope/schema Needs confirmation. | HTTP `200` for cataloged run read; reconstruct server stages and evidence metadata. | Safe resource/dependency error. | S, pp. 40–42, Chapter 11; p. 83, Appendix A.2 |
| SCR-004-A02 | Subscribe to progress | Authorized run; `GET /v1/streams/runs/{runId}`. | SSE updates with monotonic offsets; meaningful state announcements only. | Connection-error presentation Needs confirmation; do not show connection loss as completion. | S, p. 55, §15.2.1; p. 58, §§16.2.1 and 16.3.1 |
| SCR-004-A03 | Reconnect or refresh | Reconnect with `Last-Event-ID`; refresh reloads server state. | Scoped retained-event backfill and restored progress, without duplicate business mutations. | Expired cursor and backfill-unavailable handling Needs confirmation. **OQ-011.** | S, p. 55, §15.2.1; p. 58, §16.2.1 |
| SCR-004-A04 | Display terminal/checkpoint failure | Runtime detects missing approval, call-budget exhaustion, repeated invalid plans, policy denial, or deadline expiry. | Display exact failed checkpoint and actual server state; no unsupported publication. | `MODEL_OUTPUT_INVALID` is supported for structured-output failures. Other code/status mappings undefined. | S, p. 41, §11.3.1; p. 38, §10.2.2; **SF-CON-004** |
| SCR-004-A05 | Open associated source evidence | Current permission and verified citation. | SCR-003 source inspection. | Safe denial/unresolved-anchor display. | Confirmed citation behavior; S, p. 57, §16.1.2 |
| SCR-004-A06 | Cancel, pause, manually retry, or operator replay | No confirmed end-user contract. Internal operator replay is a separate guarded capability. | Needs confirmation. | Needs confirmation. | **OQ-011, OQ-024.** Do not expose internal replay endpoints as ordinary browser controls. |

**Primary action:** Needs confirmation. The source confirms timeline viewing, not a specific primary control.

### SCR-005 — Review Inbox

#### Fields and Review Form

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, timing, conditions, and selectable-value source | Status / source |
|---|---|---|---|---|---|
| SCR-005-F01 | Review task identity and related case/run | Immutable references; exact public fields/schema Needs confirmation | Server-assigned; read-only | Authorized task/pool scope only. | S, p. 45, §12.2.1; p. 85, Appendix B.1 |
| SCR-005-F02 | Review status | Exact states: `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED` | Server state; initial task-state details Needs confirmation; read-only | Actor, content hash, and separation of duties guard review transitions. Full transition matrix undefined. **OQ-013.** | S, p. 82, Appendix A.1 |
| SCR-005-F03 | Reviewer pool, minimum role, assignment | Policy-defined references; value-list source/schema Needs confirmation | Policy-assigned; read-only unless reassignment is explicitly authorized later | No self-assignment or pool selection is confirmed. **OQ-013.** | S, p. 45, §12.2.1 |
| SCR-005-F04 | Expiry / review SLA | Configured deadline; API RFC 3339 timestamp if exposed; SLA value undefined | Server-derived; read-only | Expiry triggers reassignment or escalation without implicit approval. | S, p. 45, §12.2.1; p. 89, `TST-010` |
| SCR-005-F05 | Exact candidate artifact | Reviewed immutable content; representation/length Needs confirmation | Required review display; exact assigned candidate; read-only | Do not substitute a changed draft or another artifact under the old hash. | S, p. 58, §16.2.2; pp. 44–45, Chapter 12 |
| SCR-005-F06 | Evaluated artifact hash / `artifact_hash` | Content hash; algorithm, encoding, and length Needs confirmation | Required stored binding; current candidate hash; not user-editable | Server rejects decisions against changed artifacts as stale. | S, p. 45, §12.2.2; p. 85, Appendix B.1 |
| SCR-005-F07 | Source citations | Citation fields defined in SCR-003 | Required evidence display; server evidence; read-only | Reviewer must be able to inspect source evidence before approval. Whether actual click/open completion is a submission guard is not specified. **OQ-013.** | S, pp. 57–58, Chapter 16 |
| SCR-005-F08 | Model version and prompt version | Version/digest metadata; schema and length Needs confirmation | Required review display; server data; read-only | Display metadata, not raw provider credentials or unrestricted prompt contents. | S, p. 58, §16.2.2; p. 56, §15.5 |
| SCR-005-F09 | Policy reasons and outcome | Normalized policy reasons; exact outcome vocabulary defined in SCR-004-F07 | Required review display; server evaluation; read-only | Outcome cannot be changed by model text or ordinary review input. | S, p. 44, §12.1; p. 58, §16.2.2 |
| SCR-005-F10 | Decision | Approve/Reject controls are confirmed; request enum literals Needs confirmation | Stored decision required; no default confirmed; Reviewer input | Do not assume button labels imply request literals such as `APPROVE` or `APPROVED`. Validate role, task state, hash, and separation of duties. **OQ-013.** | S, p. 45, §12.2.2; p. 58, §16.2.2 |
| SCR-005-F11 | Rationale / reason | Semantic text; wire mapping and length Needs confirmation | Approval record includes rationale; precise UI required-field rule Needs confirmation; Reviewer input | Required review fields must be complete before enabling decision controls. Which fields satisfy completeness is unresolved. **OQ-013.** | S, p. 45, §12.2.2; p. 58, §16.2.2; p. 85, Appendix B.1 |
| SCR-005-F12 | Annotations | Optional annotations; structured/text format and length Needs confirmation | Explicitly optional; initial value Needs confirmation; Reviewer input | Bind to reviewed artifact/decision; validation schema undefined. | S, p. 45, §12.2.2 |
| SCR-005-F13 | Decision actor and timestamp | Authenticated actor reference; server occurrence timestamp | Stored decision metadata required; server-generated; read-only | Not editable to impersonate another actor or alter historical decisions. | S, p. 45, §12.2.2; p. 62, §17.3.1 |
| SCR-005-F14 | Queue pagination/search/filter/sort | Public cursor-pagination principle exists; queue-specific contract undefined | Needs confirmation | No task sort keys, filters, page size, total count, or bulk approval are confirmed. **OQ-013.** | S, p. 54, §15.1.1; pp. 44–46, Chapter 12 |

#### Review Procedure

1. Load the authorized review queue through `GET /v1/review-queue`.
2. Open an authorized task and display the exact candidate artifact, citations, model/prompt version, and policy reasons.
3. Permit source inspection through SCR-003.
4. Capture decision, rationale, and any optional annotations.
5. Keep Approve and Reject disabled until the required review fields are complete.
6. Submit to `POST /v1/approvals/{approvalId}/decision`.
7. Re-evaluate actor authorization, separation of duties, applicable task state/expiry, and exact artifact hash.
8. Record the immutable decision and correlated audit evidence.
9. If approval requirements are satisfied, permit the publication gate to validate and publish the exact artifact. Decision acceptance alone must not be portrayed as publication when other gate requirements remain unsatisfied.

**Confirmed sources:** S, pp. 44–46, Chapter 12; pp. 57–59, Chapter 16; p. 83, Appendix A.2.  
**Needs confirmation:** Detailed request schema, required-field set, review-state guards, and task-detail loading contract — **OQ-013**.

#### Operations and Events

| ID | Operation | Execution conditions and processing | Successful display/navigation | Failure display | Status / source |
|---|---|---|---|---|---|
| SCR-005-A01 | Load review queue | Authenticated reviewer scope and policy-defined routing; `GET /v1/review-queue`. | Display authorized tasks and review status summary. | Safe permission/dependency error; exact empty-state presentation undefined. | Confirmed; S, pp. 44–46, Chapter 12 |
| SCR-005-A02 | Open review | Authorized task; load exact candidate and review evidence. Correlate `UserReviewOpened`. | Review evidence panel supports source inspection. | No unauthorized or substituted artifact content. Exact task-detail endpoint and open-state mutation undefined. | Confirmed review display/event; S, pp. 57–59, §§16.1–16.5 |
| SCR-005-A03 | Approve | Required fields complete; eligible Reviewer; current exact hash; separation of duties; applicable policy/task guards. Submit decision endpoint. | HTTP `200`; immutable decision recorded. Publish only if the full gate is satisfied. Navigation Needs confirmation. | Changed artifact produces stale rejection; cataloged decision conflict may return HTTP `409`. High-risk self-approval rejected. Specific stale-approval code undefined. | S, p. 45, §12.2.2; p. 58, §16.2.2; p. 83, Appendix A.2; p. 89, `TST-006` |
| SCR-005-A04 | Reject | Same form-completeness and actor/hash guards; submit rejection to decision endpoint. | Immutable rejected decision; denied recommendation may be reworked as a new run revision. Automatic case-state change is not confirmed. | Safe stale/authorization/validation error; preserve prior business state. | S, pp. 45–46, §§12.2–12.3.2 |
| SCR-005-A05 | Task expiry event | Configured SLA expires; policy selects reassignment/escalation. | Expiry/escalation recorded; no implicit approval. | Expired-task decision acceptance rules and UI refresh timing Needs confirmation. | S, p. 45, §12.2.1; p. 89, `TST-010` |
| SCR-005-A06 | Authorized override | Elevated role, secondary reviewer, and audited reason required. | Outcome follows an explicitly authorized override, retaining audit lineage. | Ordinary Reviewer/Admin status alone must not bypass the prerequisites. Endpoint and form undefined. | Capability Confirmed; UI/contract Needs confirmation. S, p. 46, §12.3.2; **OQ-014** |

**Primary action:** Needs confirmation for the inbox as a whole. Approve and Reject are both confirmed task controls; neither may bypass completeness or eligibility guards.

### SCR-006 — Connector Health

#### Fields

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, timing, conditions, and selectable values | Status / source |
|---|---|---|---|---|---|
| SCR-006-F01 | Connector identity and repository configuration | Connector/source references; exact schema/name format Needs confirmation | Server/configuration data; read-only health view; configuration edit layout undefined | Workspace-scoped connector context. Provider choices and permissions must be selected explicitly. **OQ-016.** | S, pp. 27–29, Chapter 7; p. 90, §F.2 |
| SCR-006-F02 | Capability support | Exact capability concepts: list, fetch, delta cursor, ACL, delete; Boolean/badge representation Proposal | Connector-advertised values; read-only | Unsupported capabilities trigger lower-trust mode and an explicit visible warning, not silent assumptions. | S, p. 27, §7.1.1 |
| SCR-006-F03 | Ingestion trust warning | Warning text/status; vocabulary Needs confirmation | Conditional on unsupported capability; read-only | Must be user-visible. Exact warning severity, acknowledgment, and restriction rules undefined. | S, p. 27, §7.1.1 |
| SCR-006-F04 | Credential reference / authorization condition | Workspace-scoped secret reference; public display schema Needs confirmation | Credentials stored outside UI in secret store; no raw-secret display | Operators can revoke credentials. Reauth-required jobs fail with `CONNECTOR_REAUTH_REQUIRED`, without exposing tokens. | S, p. 27, §7.1.2 |
| SCR-006-F05 | Sync-run list and status | `SyncRun` records; exact state enum, columns, lengths Needs confirmation | Server-derived; read-only | `GET /v1/connectors/{connectorId}/runs`. Read scope, sort, pagination, and retention undefined. **OQ-016.** | S, pp. 28–29, §§7.2–7.4 |
| SCR-006-F06 | Provider cursor, high-watermark, error ledger | Stored sync metadata; types and safe public projection Needs confirmation | Stored for each run; read-only; exposing raw cursor is not confirmed | Cursor advances only after preceding items have durable outcomes. Health UI placement is a Proposal. | S, p. 28, §7.2.1 |
| SCR-006-F07 | Retry/throttling information | Retry metadata; `Retry-After` where supplied; schema Needs confirmation | Server-derived; read-only | Honor provider Retry-After, exponential backoff with jitter, and workspace quotas. Retry count and schedule undefined. | S, p. 28, §7.3.1 |
| SCR-006-F08 | Quarantined source items | Reason code, correlation ID, remediation path; schemas Needs confirmation | Conditional on poison records; read-only | Remaining batch may proceed after bounded retries while ledger records exception. | S, p. 29, §7.3.2 |
| SCR-006-F09 | Provisioning/readiness status | Provisioning and index-coverage information; enum/formula Needs confirmation | Server-derived; read-only | Incomplete provisioning visible and blocks sync. Search readiness uses index coverage, not queue emptiness. Placement undefined. | S, p. 78, §§22.1.1–22.1.2 |
| SCR-006-F10 | Health summary | Required clear status summary; complete connector-health enum undefined | Server-derived; read-only | Do not treat mockup service `Healthy` as the connector-state contract. | S, p. 57, §16.1.1; p. 67, Figure 18.2 |

#### Operations and Events

| ID | Operation | Execution conditions and processing | Successful display/navigation | Failure display | Status / source |
|---|---|---|---|---|---|
| SCR-006-A01 | Inspect connector runs | Authorized connector scope; `GET /v1/connectors/{connectorId}/runs`. | Display safe run outcomes, warnings, and applicable remediation information. | Safe permission/dependency error; schema/HTTP result not cataloged. | Confirmed endpoint; S, pp. 28–29, Chapter 7 |
| SCR-006-A02 | Start incremental sync | `Admin`; complete provisioning; applicable credentials/capabilities/quotas; validated request with job idempotency; `POST /v1/connectors/{connectorId}/sync`. | HTTP `202`; persisted sync operation and correlated `ConnectorSyncStarted`; later durable item outcomes. | Reauth-required jobs expose `CONNECTOR_REAUTH_REQUIRED`, not credentials. Other dependency/quota errors follow shared rules. | S, pp. 27–29, Chapter 7; p. 78, §22.1.1; p. 83, Appendix A.2 |
| SCR-006-A03 | Revoke credentials | Authorized operator capability exists; specific interactive actor/endpoint undefined. | Credentials revoked; queued jobs fail with reauth-required outcome. | No token disclosure; failure UX undefined. | Capability Confirmed; screen implementation Needs confirmation. S, p. 27, §7.1.2; **OQ-016** |
| SCR-006-A04 | Reauthorize connector | Reauth-required condition can be reported, but reauthorization flow is not described. | Needs confirmation. | Needs confirmation. | **OQ-016.** Do not invent an OAuth provider URL or endpoint. |
| SCR-006-A05 | Process source deletion/ACL update | Connector detects source deletion or changed ACL. | Tombstone and scheduled index removal for deletion; invalidate retrieval caches before serving results after ACL change. | Stale visibility treated as security incident. | Confirmed background event behavior affecting visible evidence; S, p. 28, §7.2.2 |
| SCR-006-A06 | Poison-record/quarantine event | Malformed document exhausts bounded retries. | Display reason code, correlation ID, and remediation path; remaining batch may continue. | Do not silently omit exception from durable ledger. | Confirmed; S, p. 29, §7.3.2 |

**Primary action:** Needs confirmation. **Proposal:** Start Sync for an authorized Admin.

### SCR-007 — Policy Settings

The source confirms the screen and workspace configuration capabilities, but does not define a complete settings form or its read/update endpoints. The following is the required inventory of supported settings concepts; **control layout, wire schema, and per-setting editability remain unresolved**.

#### Settings Fields

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, validation, display conditions, and selectable-value source | Status / source |
|---|---|---|---|---|---|
| SCR-007-F01 | Workspace identity and configuration revision | Workspace identifier; monotonic revision; exact schema Needs confirmation | Current authorized configuration; identity read-only; revision not editable | Configuration updates require revision preconditions and durable audit records. | S, p. 24, §6.1.1 |
| SCR-007-F02 | Retention class | Policy class/reference; values and length Needs confirmation | Stored workspace setting; required/default/edit rights undefined | Closed-case eligibility and legal-hold exceptions apply. Corporate retention policy remains an explicit decision. **OQ-020, OQ-022.** | S, p. 24, §6.1.1; p. 26, §6.3.2; p. 90, §F.2 |
| SCR-007-F03 | Allowed model deployments | Deployment references; selection control Proposal | Stored setting; current allowed set; authorized configuration input once contract is defined | Whitelist specific approved deployments, not broad provider brands. Catalog endpoint `GET /v1/model-catalog` exists. Filter/select schema undefined. | S, p. 24, §6.1.1; pp. 37–39, Chapter 10; **OQ-020, OQ-022** |
| SCR-007-F04 | Connector credential references | Workspace-scoped secret references; schema Needs confirmation | Stored setting; edit rights/input mechanism undefined | Never display raw refresh tokens/service credentials in public responses or diagnostics. | S, p. 24, §6.1.1; p. 27, §7.1.2 |
| SCR-007-F05 | Approved toolsets | Version-pinned tool/capability references; selector schema Needs confirmation | Stored setting; current approved set; edit contract undefined | Discovery is not authorization. No arbitrary browser tool definitions, URLs, or filesystem access. | S, p. 24, §6.1.1; p. 41, §11.2; p. 87, Appendix C.2 |
| SCR-007-F06 | Reviewer routing and pools | Policy-defined pool/routing references; values/schema Needs confirmation | Stored setting; current routing; edit contract undefined | Minimum role and separation of duties apply. Exact routing criteria and eligible pools undefined. | S, p. 24, §6.1.1; p. 45, §12.2.1 |
| SCR-007-F07 | Review SLA / expiry behavior | Configured duration and escalation/reassignment policy; units and limits undefined | Current policy; required/default/edit rights Needs confirmation | Expiry cannot silently approve. | S, p. 45, §12.2.1; **OQ-020** |
| SCR-007-F08 | Rule-set version / policy version | Version identifier; `policy_version` and `rule_version` occur in source entities; mapping undefined | Stored reproducibility metadata; read-only version display or managed update flow undefined | Normalized policy inputs must be stored with rule-set version. | S, p. 44, §12.1.1; p. 85, Appendix B.1 |
| SCR-007-F09 | Policy inputs and decision rules | Sensitivity, requested action, evidence quality, model class, financial-impact category, confidence bands | Input concepts Confirmed; editable rule form and category values undefined | Outcomes limited to `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY`. No model override. Exact thresholds Needs confirmation. | S, p. 44, §12.1; **OQ-020** |
| SCR-007-F10 | Human-review/self-approval settings | Reference config: `require_human_review_for: [HIGH_RISK, RESTRICTED]`; `self_approval_allowed: false` | Reference configuration values; UI toggle/editability not confirmed | High-risk self-approval prohibition remains obligatory. Do not offer an undocumented option that bypasses it. | S, p. 11, §2.1.2; p. 90, Appendix F |
| SCR-007-F11 | Automatic-publication classification | Reference literal `auto_publish_classification: INTERNAL` | Reference value; full rule semantics/editability undefined | `INTERNAL` alone is not sufficient authorization to publish: all evidence, risk, and approval gates still apply. **SF-CON-009.** | S, p. 90, Appendix F; pp. 44–46, Chapter 12 |
| SCR-007-F12 | Workspace quotas / run budgets | Quota/budget data; units, limits, and schema undefined | Workspace quota exists; current policy; edit contract undefined | Admission uses workspace tokens, queue age, and provider capacity. Reference large-tenant capacity is not a universal UI quota. | S, p. 85, Appendix B.1; pp. 68–69, §§19.1–19.2 |
| SCR-007-F13 | Workspace timezone and business calendar | Timezone/calendar references; available values/schema undefined | Domain behavior Confirmed; settings placement Proposal | Deadlines use business calendar and workspace timezone; display includes timezone labels. | S, p. 25, §6.3.1; p. 59, §16.3.2; **OQ-009, OQ-020** |

#### Operations and Events

| ID | Operation | Execution conditions and processing | Successful display/navigation | Failure display | Status / source |
|---|---|---|---|---|---|
| SCR-007-A01 | Load settings | Authorized workspace administrative scope; read endpoint undefined. | Current versioned settings and clear status summary. | Safe denial/dependency error; exact contract undefined. | Settings capability Confirmed; endpoint Needs confirmation. S, pp. 24 and 57, §§6.1.1 and 16.1.1 |
| SCR-007-A02 | Update workspace policy/settings | Authorized actor; validated fields; current revision precondition; durable audit. Do not use the adjacent case PATCH endpoint as an invented workspace update contract. | Updated configuration/version with correlated audit evidence. Exact publication/activation timing undefined. | Reject stale or unauthorized update without business mutation; conflict code/schema undefined for settings. | Confirmed update guards; endpoint and fields Needs confirmation. S, p. 24, §6.1.1; **OQ-020** |
| SCR-007-A03 | Load permitted model catalog | `GET /v1/model-catalog`; exact scope/schema Needs confirmation. | Available deployment metadata sufficient to enforce approved deployment selection once contract is defined. | Safe error; no unapproved fallback. | Endpoint Confirmed; S, pp. 37–39, Chapter 10 |
| SCR-007-A04 | Policy/security change event | Accepted versioned policy change. `SecurityPolicyChanged` exists for security governance. Exact relationship to settings update undefined. | Retain actor/version/audit lineage; subsequent policy decisions reproducible. | Reject unauthorized or stale changes. | Event Confirmed; UI binding Needs confirmation. S, pp. 61–63, Chapter 17 |

**Primary action:** Needs confirmation. **Proposal:** Save Settings, only after update schema and permissions are confirmed.

### SCR-008 — Audit Explorer

#### Fields and Query Controls

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, timing, conditions, and selectable values | Status / source |
|---|---|---|---|---|---|
| SCR-008-F01 | Audit event identity / `id` | Identifier policy UUIDv7; exact public encoding Needs confirmation | Stored identity; server data; read-only | Append-only historical record. | S, p. 51, §14.1.1; p. 85, Appendix B.1 |
| SCR-008-F02 | Tenant and actor / `tenant_id`, `actor_id` | UUID/principal references; exact API field mapping Needs confirmation | Stored metadata; read-only | Tenant-scoped query; actor retained for accepted/denied access without disclosing private resource existence. | S, p. 23, §5.3.2; p. 85, Appendix B.1 |
| SCR-008-F03 | Action / decision metadata | `action` and decision metadata; vocabulary/schema Needs confirmation | Stored data; read-only | Auditor sees permitted decision metadata and access events; no historical edits. | S, p. 11, §2.1.2; p. 62, §17.3.1; p. 85, Appendix B.1 |
| SCR-008-F04 | Occurrence time / correlation identifiers | UTC/RFC 3339 time; trace/correlation identifiers; public projection undefined | Durable metadata; read-only | Localized time with timezone label; no ordering change from locale. | S, p. 48, §13.1.1; p. 59, §16.3.2; p. 64, §18.1.1 |
| SCR-008-F05 | Digest / hash-chain metadata | `digest`; batch hashes; algorithm/display encoding Needs confirmation | Stored immutable evidence; read-only | Audit entries append-only, chained with batch hashes, exported to independently controlled retention storage. | S, p. 62, §17.3.1; p. 85, Appendix B.1 |
| SCR-008-F06 | Prompt-template digest and review lineage | Template digest, actor/time, artifact hash, rationale, and decision metadata where authorized | Metadata capability Confirmed; exact detail panel/schema Needs confirmation; read-only | Respect redacted content scope. Raw prompt contents are not established as Auditor-visible fields. | S, p. 11, §2.1.2; p. 45, §12.2.2 |
| SCR-008-F07 | Audit pagination cursor | Cursor token; type/length/encoding Needs confirmation | Server pagination; read-only transport context | Cursor-paginated immutable log. Page size, direction, expiry, and query snapshot behavior undefined. **OQ-019.** | S, p. 83, Appendix A.2 |
| SCR-008-F08 | Audit search/filter/sort controls | Exact filters, date ranges, sort keys, validation limits, and value catalogs not defined | Needs confirmation | Query capability does not authorize invented request parameters. **OQ-019.** | S, p. 62, §17.3.1; p. 83, Appendix A.2 |

**Confirmed retention baseline:** Diagnostic logs have a 30-day default TTL; security audit logs use a distinct seven-year fictional policy. Purges record receipts and legal-hold exceptions. Final corporate retention selection remains unresolved.  
**Source:** S, p. 66, §18.3.2; p. 90, Appendix F and §F.2.

#### Operations and Events

| ID | Operation | Execution conditions and processing | Successful display/navigation | Failure display | Status / source |
|---|---|---|---|---|---|
| SCR-008-A01 | Query audit events | `Auditor` scope; authorized tenant/redaction scope; `GET /v1/audit/events`. | HTTP `200`; immutable, cursor-paginated event data. | Safe denied/failed-query display; no resource-existence leakage. | Confirmed; S, p. 83, Appendix A.2 |
| SCR-008-A02 | Obtain next audit page | Use server cursor within original authorized scope. | Authorized page of immutable events. | Cursor failure/recovery contract undefined. | Cursor behavior Confirmed; **OQ-019** |
| SCR-008-A03 | Inspect event/decision lineage | Authorized metadata scope. Exact detail endpoint not defined. | Read-only permitted decision, digest, and access metadata. | No unauthorized content. | Capability Confirmed; layout/endpoint Needs confirmation. S, p. 11, §2.1.2; p. 62, §17.3.1 |
| SCR-008-A04 | Attempt historical edit | No allowed mutation of historical review decisions or audit records. | No edit capability. | Server/storage rejects modification; negative verification required. | Confirmed prohibition; S, p. 62, §17.3.1; p. 88, `T-09` |
| SCR-008-A05 | Export evidence or place legal hold | Tenant/workspace export and legal-hold capabilities exist elsewhere in the source; Audit Explorer placement is not confirmed. | Needs confirmation; apply independent approvals and safe export contents if exposed. | No ordinary single-user export bypass. | **OQ-023, OQ-024.** S, pp. 61–63, Chapter 17; pp. 78–80, Chapter 22 |

**Primary action:** Needs confirmation. Query Audit Events is a **Proposal**.

### SCR-009 — Overview

#### Fields

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, timing, conditions, and values | Status / source |
|---|---|---|---|---|---|
| SCR-009-F01 | Tenant/workspace/release context | See SF-SHELL-F01–F02 | Illustrated; current context; read-only | User permissions and selection behavior unresolved. | S, p. 7, Reference UI A |
| SCR-009-F02 | Summary cards | See SF-SHELL-F03–F06 | Illustrated; computed server values; read-only | Formulas, scope, refresh interval, and API undefined. **OQ-027.** | S, pp. 7 and 14, Reference UI A and Figure 2.2 |
| SCR-009-F03 | Overview-specific content | No confirmed fields or schema | Needs confirmation | Do not infer a full dashboard from a menu label or repeated mockup panels. | S, p. 14, Figure 2.2; **OQ-004, OQ-027** |

#### Operations

| ID | Operation | Execution conditions and processing | Success and navigation | Failure display | Status |
|---|---|---|---|---|---|
| SCR-009-A01 | Open illustrated Overview destination | Authorization, landing rules, and backing data undefined. | Screen contents and destinations Needs confirmation. | Needs confirmation. | Illustrated navigation only; S, p. 7, Reference UI A |
| SCR-009-A02 | Refresh dashboard summaries | Refresh trigger, interval, and APIs undefined. | Needs confirmation. | Needs confirmation. | **OQ-027** |

**Primary action and complete functional scope:** Needs confirmation. No dashboard refresh schedule is established.

### SCR-010 — Usage & Quality

**Confirmed:** Usage and evaluation capabilities exist, and the mockups show `Usage & Quality` plus “AI Quality / Evaluation Scorecard.”  
**Needs confirmation — OQ-021:** Whether these form one screen, tabs, or separate screens. The identifier preserves the unresolved illustrated destination; it does not approve a split.

#### Fields

| ID | Field / meaning | Type, length, and format | Required / initial / editability | Constraints, timing, conditions, and selectable values | Status / source |
|---|---|---|---|---|---|
| SCR-010-F01 | Usage cost, quotas, and trend estimates | Usage metrics; currency, units, precision, and schema undefined | API returns these concepts; server values; read-only | `Admin` usage access; do not invent currency or billing period. | S, p. 83, Appendix A.2 |
| SCR-010-F02 | Budget, forecast, rejected excess requests | Daily rollup metrics; schema/units undefined | Server rollups; read-only; UI arrangement Proposal | Daily rollups show budget, forecast, and rejected excess requests. This does not establish a screen refresh schedule. | S, p. 65, §18.3.1 |
| SCR-010-F03 | Cost center, deployment version, usage attribution | Workspace cost-center and model-deployment references; format undefined | Attributed usage; read-only | Model invocations, embeddings, storage, and indexing usage retain attribution. | S, p. 65, §18.3.1 |
| SCR-010-F04 | Input/output token usage | `in_tokens`, `out_tokens` selected entity fields; numeric types/precision undefined | Server ledger data; read-only; UI placement Proposal | Quota exhaustion terminates current run without automatically changing model/data class. | S, p. 38, §10.3.1; p. 85, Appendix B.1 |
| SCR-010-F05 | Evaluation identity, status, and dataset/version metadata | `evaluationId` path exists; response schema and status enum undefined | Server-generated; read-only | Reference corpus contains `1,200` synthetic permission-controlled cases; corpora frozen/versioned and independently reviewed. | S, pp. 74–76, Chapter 21; p. 89, §E.1 |
| SCR-010-F06 | Grounded citation precision | Metric representation; precision and interval schema undefined | Server scorecard; read-only | Reference target `>=0.97`; not the mockup evidence-coverage percentage. | S, p. 75, §21.2.2 |
| SCR-010-F07 | Unsupported-claim rate | Metric representation; precision undefined | Server scorecard; read-only | Reference target `<=0.02`. | S, p. 75, §21.2.2 |
| SCR-010-F08 | High-risk policy recall | Metric representation; precision undefined | Server scorecard; read-only | Target `1.00` on frozen safety suite. Critical isolation and approval tests pass with zero exceptions. | S, pp. 74–75, Chapter 21 |
| SCR-010-F09 | Confidence intervals and distribution shift | Domain-level statistical output; schema undefined | Server results; read-only | Report by domain. Low statistical confidence blocks release rather than proving equivalence. | S, pp. 75–76, §§21.2.2 and 21.3.2 |
| SCR-010-F10 | Evaluation creation inputs | Required setup fields, model/prompt/dataset selectors, defaults, and validation undefined | `Admin` creation capability Confirmed; input layout Needs confirmation | Do not invent dataset-management or expected-fixture editing controls. **OQ-021.** | S, pp. 74–76, Chapter 21; p. 83, Appendix A.2 |
| SCR-010-F11 | Usage/evaluation filters, sorting, pagination | No screen-specific contract | Needs confirmation | No time range, page size, chart type, or comparative layout confirmed. **OQ-021.** | S, pp. 64–66 and 74–76, Chapters 18 and 21 |

#### Operations and Events

| ID | Operation | Execution conditions and processing | Successful display/navigation | Failure display | Status / source |
|---|---|---|---|---|---|
| SCR-010-A01 | Read usage | `Admin`; authorized scope; `GET /v1/usage`. | HTTP `200`; costs, quotas, and trend estimates. | Safe permission/dependency error. | Confirmed; S, p. 83, Appendix A.2 |
| SCR-010-A02 | Start frozen benchmark evaluation | `Admin`; validated setup; job idempotency; `POST /v1/evaluations`. | HTTP `202`; persisted evaluation operation. Progress UI/stream not defined. | Safe validation/dependency/quota error; no fabricated success. | Confirmed; S, pp. 74–76, Chapter 21; p. 83, Appendix A.2 |
| SCR-010-A03 | Read evaluation | `GET /v1/evaluations/{evaluationId}`; exact scope/schema Needs confirmation. | Authorized evaluation results and scorecard once contract is defined. | Safe resource/dependency error. | Endpoint Confirmed; S, pp. 74–76, Chapter 21 |
| SCR-010-A04 | Evaluation completion / release-gate result | Correlate `EvaluationCompleted`; retain versioned synthetic fixtures and results. | Display actual scorecard and confidence. No automatic release-promotion control is established. | Critical safety/isolation failures or low confidence cannot be represented as an acceptable release outcome. | S, pp. 74–76, Chapter 21; p. 89, `TST-016` |

**Primary action:** Needs confirmation. Read Usage and Start Evaluation are supported capabilities; their placement and prioritization require **OQ-021** resolution.

## Integrations and Acceptance Criteria

### Screen-Relevant Integration Register

The following endpoints already exist in the source. They are retained verbatim. This register does not define missing payload schemas or invent API identifiers.

| Related requirements/screens | Existing integration | Confirmed inputs / outputs and behavior | Details for later stages |
|---|---|---|---|
| SF-PRE-001–003; all screens | OIDC authorization-code flow with PKCE; `GET /v1/me` | Authenticated principal and tenant context; required token claims and algorithm checks. | Identity provider, user response schema, session architecture, login/logout UX: **OQ-001, OQ-002**. S, pp. 21–23, Chapter 5. |
| SCR-001-A01–02 | `GET /v1/cases?cursor=...` | Authorized case listing; cursor pagination. | Query/response schema, scope, page size, sorting/filtering: **OQ-006**. S, pp. 57–59, Chapter 16. |
| SCR-001-A03 | `POST /v1/cases` | Analyst; idempotency; HTTP `201`; new case identifier and `NEW` state. | Full creation schema and fields: **OQ-007**. S, p. 12, §2.2.1; p. 83, Appendix A.2. |
| SCR-002-A01 | `GET /v1/cases/{caseId}` | Analyst/Reviewer; HTTP `200`; authorized current revision. | Complete case/result response schema: **OQ-007, OQ-012**. S, p. 83, Appendix A.2. |
| SCR-002-A02, A04 | `PATCH /v1/cases/{caseId}` | `Owner`; `If-Match`; HTTP `200`/`409`; confirmed transitions SCR-002-T01–T06; revision conflicts. | Patch format, allowed field mutations, detailed transition guards: **OQ-003, OQ-007, OQ-008**. S, p. 25, §6.2; p. 83, Appendix A.2. |
| SCR-002-A07 | `POST /v1/cases/{caseId}/close` | Closure snapshots approved answer, cited versions, and reviewer decisions. | Originating state, actor/approval guards, request and response: **OQ-008**. S, pp. 24–26, Chapter 6. |
| SCR-002-A05 | `POST /v1/cases/{caseId}/attachments`; `GET /v1/documents/{documentId}/status` | Analyst upload returns HTTP `202`; allowed files, safety checks, immutable derivatives, document-status inquiry. | Upload transport, status schema, polling/notification contract, validation errors: **OQ-015**. S, pp. 30–32, Chapter 8; p. 83, Appendix A.2. |
| SCR-002-A06; SCR-004 | `POST /v1/cases/{caseId}/runs` | Analyst; HTTP `202`; bounded workflow; validated request and idempotency. | Full request, admission thresholds, timeout mapping: **OQ-011**. S, pp. 40–42, Chapter 11; p. 83, Appendix A.2. |
| SCR-002-A06; SF-CON-007 | `POST /v1/runs` | Additional run-request path appears in Chapter 3 with `RunRequested`. | Relationship to the case-scoped route must be resolved; do not silently treat them as identical. S, pp. 15–17, Chapter 3; **OQ-011**. |
| SCR-004-A01 | `GET /v1/runs/{runId}`; `GET /v1/runs/{runId}/steps` | Run read returns stages/evidence metadata; steps endpoint exists. | Full status/step schemas and steps scope: **OQ-011**. S, pp. 40–42, Chapter 11; p. 83, Appendix A.2. |
| SCR-004-A02–03 | `GET /v1/streams/runs/{runId}` | Analyst/Reviewer; HTTP `200`; SSE monotonic offsets, `Last-Event-ID`, scoped retained-event backfill. | Event payloads, retention, expired-cursor handling: **OQ-011**. S, p. 55, §15.2.1; p. 83, Appendix A.2. |
| SCR-003-A01 | `GET /v1/cases/{caseId}/evidence` | Case evidence inquiry supporting review display. | Scope and full response contract: **OQ-017, OQ-018**. S, pp. 57–59, Chapter 16. |
| SCR-003-A02–03 | `POST /v1/search`; `GET /v1/evidence/{evidenceId}` | `Member` search returns HTTP `200` ACL-filtered lexical/semantic evidence; evidence lookup exists. | Public search schema, ranking presentation, anchors, source delivery: **OQ-017, OQ-018**. S, pp. 34–36, Chapter 9; p. 83, Appendix A.2. |
| SCR-005-A01–04 | `GET /v1/review-queue`; `POST /v1/approvals/{approvalId}/decision` | Reviewer decision endpoint returns HTTP `200`/`409`; exact artifact hash binding and immutable decision. | Queue/detail schemas, required review fields, decision literals, actor/task guards: **OQ-013**. S, pp. 44–46, Chapter 12; p. 83, Appendix A.2. |
| SCR-006-A01–02 | `POST /v1/connectors/{connectorId}/sync`; `GET /v1/connectors/{connectorId}/runs` | Admin sync returns HTTP `202`; provider capabilities, durable cursor/watermark/error ledger, reauth outcome. | Provider selection, permissions, credential lifecycle UI, response schemas: **OQ-016, OQ-022**. S, pp. 27–29, Chapter 7; p. 83, Appendix A.2. |
| SCR-007-A03 | `GET /v1/model-catalog` | Model registry/catalog capability; approved specific deployments. | Scope, allowed-deployment filtering, catalog schema: **OQ-020, OQ-022**. S, pp. 37–39, Chapter 10. |
| SCR-008-A01–02 | `GET /v1/audit/events` | Auditor; HTTP `200`; cursor-paginated immutable log. | Filter and redacted-detail schemas: **OQ-019**. S, p. 83, Appendix A.2. |
| SCR-010-A01 | `GET /v1/usage` | Admin; HTTP `200`; costs, quotas, trend estimates. | Units, currency, rollup response, screen arrangement: **OQ-021**. S, pp. 64–66, Chapter 18; p. 83, Appendix A.2. |
| SCR-010-A02–03 | `POST /v1/evaluations`; `GET /v1/evaluations/{evaluationId}` | Admin creation returns HTTP `202`; frozen benchmark and scorecard capability. | Input/status/result schemas, read scope, UI arrangement: **OQ-021**. S, pp. 74–76, Chapter 21; p. 83, Appendix A.2. |
| SF-SCP-008 | `PUT /v1/workspaces/{workspaceId}/members`; `POST /v1/security/holds` | Membership and legal-hold interfaces exist. | No screen/form or full permission/schema contract is confirmed. **OQ-024.** S, pp. 21–23 and 61–63, Chapters 5 and 17. |
| SF-SCP-007; SCR-008-A05 | `POST /v1/workspaces/{workspaceId}/export`; `POST /v1/workspaces/{workspaceId}/delete` | `Admin + approver`; HTTP `202`; independent approval checks; export manifest/checksums; legal-hold-safe deletion and receipts. | UI placement, scope, approver workflow, operation status/download endpoints: **OQ-023**. S, pp. 78–80, Chapter 22; p. 83, Appendix A.2. |
| SF-SCP-008 | `POST /v1/design-decisions`; `GET /v1/design-baselines/{id}` | Design-governance interfaces and `BaselineCommitted` exist. | Screen need and placement undefined; do not create screens from endpoint existence alone. **OQ-024.** S, pp. 8–10, Chapter 1. |

### External Dependencies and Data Boundaries

| Integration | Required input/output behavior | Screen impact | Source / open decision |
|---|---|---|---|
| Enterprise document providers | Connector workers use scoped credentials; preserve source identity, permissions, deletion/ACL history, cursor, and durable ingestion outcomes. | Connector Health warnings/status; source evidence availability. | S, pp. 27–29, Chapter 7. Exact providers and third-party permissions: **OQ-016, OQ-022**. |
| Controlled model gateway / external LLM providers | Providers receive scoped context and structured prompts, not raw connector tokens or unrestricted database access. Invalid fields/citations/control-character injection cause `MODEL_OUTPUT_INVALID`. Fallback only to approved equal-or-stronger data-handling class and approved region/deployment. | Run progress/failure; exact draft and model/prompt metadata; no unsupported publication. | S, p. 15, §3.1.1; pp. 37–39, Chapter 10. Approved deployments/regions: **OQ-022**. |
| Search subsystem | ACL-filtered hybrid retrieval, deterministic re-ranking, evidence diversity, source anchors, and unsupported-evidence outcome. | Evidence results and reduced-quality warnings. | S, pp. 34–36, Chapter 9; p. 69, §19.2.2. Exact search provider: **OQ-022**. |
| PostgreSQL / private object storage | Authoritative mutable metadata; immutable source/normalized artifacts; tenant scope; short-lived access-controlled signed URLs. | Current revisions, source viewing, closed-case lineage. Browser must not receive datastore credentials. | S, pp. 51–53, Chapter 14. Source-content API/URL lifetime: **OQ-018**. |
| MCP / A2A | Typed, pinned, scoped tools; separate capability authorization. `knowledge.search@v1` is read-only and returns `evidence_set_id` and `Citation[]`. Discovery never grants permission. | Visible run checkpoints, not an arbitrary browser tool picker. | S, pp. 40–42, Chapter 11; p. 87, Appendix C.2. |
| Events and transactional outbox | Versioned tenant/revision/trace envelopes; duplicate and delayed delivery safe; consumer deduplication. | Persisted progress and auditable accepted outcomes; browser SSE schema remains separately unresolved. | S, pp. 48–50, Chapter 13; p. 87, Appendix C.1. |
| Optional outbound webhooks | Signed, retried with exponential backoff; recipient verifies signature and event age; failure cannot roll back case transition. | No webhook-management screen is confirmed. | S, p. 55, §15.2.2; **OQ-024**. |

Internal APIs such as `POST /internal/model/generate`, `GET /internal/workflows/{runId}`, and `POST /internal/deadletters/{id}/replay` are source-confirmed service/operational interfaces. They must not be assumed to be direct browser integrations. Operator replay requires a reason, dry-run validation, and scope limit, preserving original event identity except explicitly provenance-linked schema migration. Its UI placement remains unresolved.  
**Source:** S, pp. 37–39, Chapter 10; pp. 48–50, Chapter 13.

### Failure-Display Contract

| Condition | Confirmed response/outcome | Screen requirement | Source |
|---|---|---|---|
| Stale case revision | HTTP `409`; `CASE_VERSION_CONFLICT`; current revision information | Show safe conflict information; no silent overwrite. Exact reconciliation UX Needs confirmation. | S, p. 25, §6.2.2; p. 84, Appendix A.3 |
| Changed payload under reused idempotency key | HTTP `409` `IDEMPOTENCY_CONFLICT` | Do not report a newly accepted operation. | S, p. 54, §15.1.2; p. 89, `TST-002` |
| Schema-invalid request | HTTP `422` | Show only safe validation details. Field-to-error mapping Needs confirmation. | S, p. 54, §15.1.1 |
| Quota/admission throttling | HTTP `429`, with `Retry-After` for throttled new runs | Saved cases remain available; no automatic policy/model-class downgrade. | S, p. 69, §19.2.1; p. 38, §10.3.1 |
| Foreign-tenant/absent resource | Same not-found class; `404`-equivalent non-disclosing error | Do not disclose existence or private metadata. | S, p. 23, §5.3.2; p. 89, `TST-003` |
| Revoked connector credentials | `CONNECTOR_REAUTH_REQUIRED` for queued jobs | Display safe reauth-required condition without tokens. | S, p. 27, §7.1.2 |
| Insufficient supported evidence | `NO_SUPPORTED_EVIDENCE`; clarification or human route may follow | No fabricated context; exact next-step UI unresolved. | S, p. 36, §9.3.2 |
| Invalid model output | `MODEL_OUTPUT_INVALID`; no publish | Display safe failed checkpoint/outcome; never show as approved. | S, p. 38, §10.2.2; p. 89, `TST-005` |
| Stale reviewed artifact | Reject as stale; audit; decision endpoint catalogs HTTP `409` conflict | No decision/publication under outdated hash. Specific stale code not provided. | S, p. 45, §12.2.2; p. 83, Appendix A.2; p. 89, `TST-006` |
| Unsafe file | Quarantine; no indexing | Show safe status/remediation only; unsafe-source viewing policy unresolved. | S, p. 30, §8.1.2; p. 89, `TST-015` |
| Review expiry | No implicit approval; reassignment/escalation recorded | Display actual expired/escalated condition once schema is defined. | S, p. 45, §12.2.1; p. 89, `TST-010` |
| Dependency unavailable | Documented retryable error or persisted asynchronous operation ID | Never ambiguous success; UI retry mechanics unresolved. | S, pp. 11–13, Chapter 2 |

**Confirmed error envelope:** `error.code`, `error.message`, `error.correlation_id`, `error.retryable`, and optional safe `error.details`. The example conflict includes `expected_revision` and `actual_revision`. Preserve literal supported codes; do not invent codes for undefined failures.  
**Source:** S, p. 84, Appendix A.3.

### Acceptance Criteria

All tests use synthetic identities, cases, documents, and provider replies. Include successful, empty, mixed-permission, adversarial, and malformed inputs. Randomized tests record their seed. Critical isolation and approval tests pass with zero exceptions.  
**Source:** S, p. 74, Chapter 21 invariant; p. 89, §§E.1–E.2.

| Acceptance ID | Related requirements | Prerequisites and action | Expected result | Source / existing test |
|---|---|---|---|---|
| SF-AC-001 | SF-PRE-001; SF-AUTH-001 | Submit an interactive/API request with missing tenant claim or unexpected token algorithm. | Gateway rejects authentication; no protected screen data or operation is returned. | S, p. 21, §5.1.1 |
| SF-AC-002 | SCR-001-A03; SF-GEN-008 | Authorized Analyst submits the same valid create request twice with the same idempotency key. | One case and identical response; HTTP `201` create outcome; initial case status `NEW`. | S, p. 12, §2.2.1; p. 83, Appendix A.2; p. 89, `TST-001` |
| SF-AC-003 | SCR-001-A03; SF-GEN-008 | Reuse a case-create key with a changed body. | HTTP `409` `IDEMPOTENCY_CONFLICT`; no duplicate created case. | S, p. 89, `TST-002` |
| SF-AC-004 | SCR-002-A01; SF-AUTH-002 | Read a valid case ID with another tenant’s token. | `404`-equivalent non-disclosing response; no private existence/content disclosure. | S, p. 23, §5.3.2; p. 89, `TST-003` |
| **SF-AC-005** | **SCR-002-F08; SCR-002-A04; SCR-002-T01–T06** | **For each confirmed edge, prepare an authorized actor fixture satisfying applicable role/approval guards and a current revision. Execute guarded PATCH from the specified source to target state.** | **Each of `NEW → TRIAGED`, `TRIAGED → IN_PROGRESS`, `IN_PROGRESS → PENDING_APPROVAL`, `IN_PROGRESS → RESOLVED`, `PENDING_APPROVAL → RESOLVED`, and `PENDING_APPROVAL → IN_PROGRESS` is accepted when its guards are satisfied; return cataloged HTTP `200`, target status, monotonic revision, and one accepted correlated transition. Detailed guard fixtures require OQ-008 resolution.** | **S, p. 25, §§6.2.1–6.2.2; p. 26, §6.5; p. 83, Appendix A.2** |
| SF-AC-006 | SCR-002-A02, A04 | Submit a valid metadata/state request with stale `If-Match`. | HTTP `409` `CASE_VERSION_CONFLICT` with current/actual revision; business state unchanged. | S, p. 25, §6.2.2 and Design checkpoint 6.2; p. 84, Appendix A.3 |
| SF-AC-007 | SCR-002-A04; SF-AUTH-001 | Attempt a normal case edge not in SCR-002-T01–T06, or use an actor failing authorization/approval guards. | Reject the unsupported/unauthorized transition without business-state change. Exact invalid-transition error code is Needs confirmation. | S, p. 25, §6.2.1 and Design checkpoint 6.2; p. 82, Appendix A.1 |
| SF-AC-008 | SCR-002-A07–08 | Close through the to-be-confirmed permitted closing edge, then inspect history; attempt ordinary in-place exit from `CLOSED`. | Closure snapshots approved answer, cited versions, and reviewer decisions. `CLOSED` remains final except explicit new-revision reopening; historical lineage unchanged. Closing/reopening target and actor tests are blocked by OQ-008, not invented. | S, pp. 24–26, Chapter 6 |
| SF-AC-009 | SCR-002-A03 | Authorized user corrects an asynchronously assigned classification label. | Correction includes reason code; labels/confidences/provenance remain represented as supported classification data. Exact correction payload requires OQ-010 resolution. | S, p. 12, §2.2.1 |
| SF-AC-010 | SCR-002-A05 | Upload an allowed PDF, DOCX, HTML, or UTF-8 text file meeting MIME/extension agreement and configured size/safety checks. | HTTP `202` ingestion operation; scanning precedes parsing; immutable derivatives/status are persisted; acceptance is not displayed as immediate search readiness. | S, pp. 30–32, Chapter 8; p. 83, Appendix A.2 |
| SF-AC-011 | SCR-002-A05; F20–25 | Upload unsafe/polyglot or oversized content. | Fail closed; unsafe payload quarantined with no indexing. Macro execution disabled and remote embedded references not fetched. Exact oversized error and MB boundary depend on OQ-015. | S, p. 30, §8.1; p. 88, `T-04`; p. 89, `TST-015` |
| SF-AC-012 | SCR-003-A03; SCR-005-F07 | Reviewer activates a verified, permitted citation for the exact candidate. | Cited immutable source opens and anchored page range is highlighted; reviewer can inspect evidence before approval. | S, pp. 57–58, §§16.1.2–16.2.2 |
| SF-AC-013 | SCR-003-A04 | Revoke source access after indexing, then issue the next retrieval. | No forbidden evidence returned or released to generation; affected cache invalidated before results are served. | S, p. 28, §7.2.2; p. 89, `TST-004` |
| SF-AC-014 | SCR-003-A02, A06 | Request evidence whose confidence/quality is insufficient. | `NO_SUPPORTED_EVIDENCE`, not fabricated context. Clarification or human routing follows only the defined server policy. | S, p. 36, §9.3.2 |
| SF-AC-015 | SCR-002-A06; SCR-004-A01–03 | Start an admitted valid run, observe stages, refresh, then reconnect with last event offset. | HTTP `202`; immediate persisted run; retrieval/generation/policy progress reconstructed from server state; scoped retained-event backfill with monotonic offsets. | S, p. 55, §15.2.1; p. 58, §16.2.1 |
| SF-AC-016 | SCR-004-A04; SF-GEN-004 | Force structured model-schema failure or missing citations. | Schema failure yields `MODEL_OUTPUT_INVALID` and no publish. Missing citations yield needs-review or unsupported outcome, not fabricated approval. | S, p. 89, `TST-005`, `TST-009` |
| SF-AC-017 | SCR-005-A03–04 | Leave required review fields incomplete. | Approve and Reject remain disabled. Exact completeness field set must be defined under OQ-013. | S, p. 58, §16.2.2 |
| SF-AC-018 | SCR-005-A03; SF-SCP-003 | Analyst attempts to approve their own high-risk recommendation. | Deny self-approval; no publication or altered approved-result pointer. | S, p. 11, §2.1.2; pp. 44–46, Chapter 12 |
| SF-AC-019 | SCR-005-A03; SCR-002-A09 | Change candidate after review, then submit approval against prior hash or replay approval for a different artifact. | Stale decision rejected and audited; different artifact cannot publish under old approval. | S, p. 45, §§12.2.2–12.3.1; p. 89, `TST-006` |
| SF-AC-020 | SCR-005-A05 | Expire review task under configured SLA. | No implicit approval; escalation/reassignment recorded. | S, p. 45, §12.2.1; p. 89, `TST-010` |
| SF-AC-021 | SCR-006-F02–03; A02 | Connector lacks an advertised capability; separately revoke credentials before queued jobs run. | Unsupported capability produces visible lower-trust warning. Revoked credential jobs fail with `CONNECTOR_REAUTH_REQUIRED`, without token disclosure. | S, p. 27, §7.1 |
| SF-AC-022 | SF-GEN-009; relevant state operations | Replay an outbox event, including repeated delayed delivery. | Exactly one accepted business transition; duplicate outcome recorded without reapplying mutation. | S, pp. 48–50, Chapter 13; p. 88, `T-07`; p. 89, `TST-007` |
| SF-AC-023 | SCR-002-A06, A11; SCR-003-F10 | Force provider `429` bursts or generation/vector degradation. | Capped retries/admission control; throttled run client receives `429` and `Retry-After`; saved cases/manual editing/evidence remain available as supported; lexical fallback visibly reduced quality; no safety bypass. | S, p. 69, §19.2; p. 89, `TST-008` |
| SF-AC-024 | SF-GEN-002–003 | Open and operate a case using keyboard only; observe live transitions and localized timestamps. | No blocked keyboard action, visible focus, meaningful state announcements; workspace-local times include timezone labels without changing event order. | S, pp. 58–59, §16.3; p. 89, `TST-011` |
| SF-AC-025 | SCR-008-A01, A04 | Query audit data as authorized Auditor, then attempt historical-record modification. | Permitted redacted immutable data returned; historical edits rejected; no secret/document text in diagnostics. | S, p. 62, §17.3.1; p. 88, `T-09` |
| SF-AC-026 | SCR-010-F06–09; A04 | Display results of the frozen reference safety/evaluation suite. | Actual metrics and domain confidence/shift are reported; targets retained as `>=0.97`, `<=0.02`, and `1.00`; critical safety failures or low confidence cannot imply acceptable release. | S, pp. 74–76, Chapter 21 |
| SF-AC-027 | SF-SCP-007 | Single Admin attempts export; separately run authorized deletion under legal hold. | Single-Admin export denied; independent approvals required. Protected held records retained and receipted. Export omits secrets/internal model prompts and includes manifests/checksums. UI steps require OQ-023 resolution. | S, pp. 78–80, Chapter 22; p. 88, `T-11`; p. 89, `TST-013` |
| SF-AC-028 | SCR-001-A03; SCR-003-A02 | Measure case creation and search under the source reference workload. | Case-create P95 target under `300 ms`; search P95 under `1.5 s`, excluding remote connector fetch. These are backend acceptance targets, not complete browser render budgets. | S, p. 65, §18.2.1; p. 68, §19.1.1 |

**Reference workload for SF-AC-028:** `2,000` active daily users, `60` requests/second steady state, `180` requests/second burst, maximum `100,000` indexed documents per tenant, and `20` concurrent AI runs per large tenant. These are fictional baseline assumptions, not universal screen limits.  
**Source:** S, p. 68, §19.1.1.

## Consistency and Open Questions

### Source Consistency and Required Clarifications

No earlier completed specification exists. The following issues are source conflicts, partial contracts, or evidence distinctions; they do not authorize silently changing supported requirements.

| ID | Issue and evidence | Affected identifiers | Required clarification or amendment |
|---|---|---|---|
| SF-CON-001 | Primary names in §16.1.1 differ from illustrated sidebar/title aliases, and active highlights do not consistently match screen titles. For example, Figure 16.2 shows “Approval Inbox / Binding Decision” while highlighting `Agent Runs`. S, pp. 57 and 60. Similar mismatches occur in Figures 2.2, 11.2, 12.2, 18.2, 21.2, and 22.2. | SF-NAV-004; SCR-001–010 | Confirm canonical labels, alias mappings, and active-navigation behavior. Retain the eight confirmed primary screens; do not implement mockup highlight errors. |
| SF-CON-002 | Illustrated case references such as `OD-2026-1042` differ from UUID/UUIDv7 technical identity. S, p. 14, Figure 2.2; p. 51, §14.1.1; p. 86, Appendix B.2. | SCR-001-F01; SCR-002-F01; SF-SHELL-F07 | Define a human-facing case reference separately from API `id`, including generation and uniqueness rules if required. |
| **SF-CON-003** | **The case transition contract is partial, not wholly absent. S, p. 25, §6.2.1 explicitly confirms the six normal edges retained in SCR-002-T01–T06. Closure capability is documented in §§6.1.2/6.3.2, but its originating edge is not stated. `CLOSED` is final except explicit reopening as a new revision; reopening target is unspecified. Appendix A.1 names role, revision, and approval guards without defining every edge-specific rule.** | **SCR-002-F08; SCR-002-A04, A07–08; SCR-002-T01–T08; SF-AC-005–008; OQ-008** | **Preserve all six confirmed edges and CLOSED finality. Complete only the missing closing edge, reopening target/contract, and detailed actor/trigger/approval guards. Do not invent `RESOLVED → CLOSED`, a reopening target, or automatic Reject-to-case-state behavior.** |
| SF-CON-004 | Run stages include `AWAITING_REVIEW` in §13.2.1 and Appendix A.1, while §11.3.1 says termination occurs on missing approval. §2.3.1 allows a recoverable timeout state; Appendix A.1 only lists `FAILED` as failure state. Appendix F has `run_timeout_seconds: 180`, while review tasks have a separately configured SLA. S, pp. 12, 41, 45, 49, 82, and 90. | SCR-004-F02, F06; SCR-004-A04; SCR-005-F04; OQ-011 | Define when missing approval means waiting versus terminal failure, timeout representation, and whether runtime budget excludes human-review wait. Preserve both confirmed waiting and failure requirements until resolved. |
| SF-CON-005 | §15.1.1 describes snake-case error codes; concrete source codes are uppercase snake-case literals. S, p. 54; p. 84, Appendix A.3. | SF-GEN-007–008; failure-display register | Preserve `CASE_VERSION_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `CONNECTOR_REAUTH_REQUIRED`, `NO_SUPPORTED_EVIDENCE`, and `MODEL_OUTPUT_INVALID` exactly. Define naming for future codes; do not lowercase existing literals. |
| SF-CON-006 | Domain model includes title, description, priority, owner, current approved result, and revision; Appendix B.2 DDL is a limited reference and omits several domain fields. S, p. 24, §6.1.2; pp. 85–86, Appendices B.1–B.2. | SCR-002-F03–19; OQ-007, OQ-012 | Preserve all domain-supported fields. Complete schemas in a later stage rather than treating omitted DDL fields as excluded. |
| SF-CON-007 | Both `POST /v1/runs` and `POST /v1/cases/{caseId}/runs` appear. The case-scoped route is cataloged in Appendix A.2. S, pp. 15–17, Chapter 3; pp. 40–42, Chapter 11; p. 83. | SCR-002-A06; integration register; OQ-011 | Define whether routes are distinct, aliases, or an amendment is required. Do not invent equivalence or remove either source occurrence. |
| SF-CON-008 | `Workspace Admin` archetype and baseline `Admin` role differ in wording; API scopes include `Owner`, `Member`, and `approver`, absent from the baseline role list. S, pp. 11, 22, and 83. | User matrix; SF-AUTH-001; OQ-003 | Specify role/scope mapping and permission matrix. Do not grant broad rights through terminology assumptions. |
| SF-CON-009 | Appendix F contains `auto_publish_classification: INTERNAL`, while high-risk and `RESTRICTED` review, evidence, and exact-hash gates remain obligatory. S, pp. 11–13, 44–46, and 90. | SCR-007-F09–11; SCR-002-A09 | Define configuration semantics without interpreting `INTERNAL` as sufficient to bypass deterministic risk/evidence/approval checks. |
| SF-CON-010 | Chapter 22 discusses tenant export/deletion, while endpoints operate at `/workspaces/{workspaceId}`; the invariant requires two independent approval checks and Appendix A.2 uses `Admin + approver`. S, pp. 78–80 and 83. | SF-SCP-007; SCR-008-A05; OQ-023 | Define workspace-versus-tenant operation scope and independent-approval workflow. Do not guess approval actors or approval endpoints. |
| SF-CON-011 | Mockup “Evidence Coverage” `97.6%` is distinct from grounded citation precision target `>=0.97`. S, p. 7, Reference UI A; p. 75, §21.2.2. | SF-SHELL-F05; SCR-010-F06; OQ-027 | Keep dashboard aggregation and benchmark metrics separate; define coverage formula independently. |

### Consolidated Open Questions

Each item below is also recorded beside the affected requirement. No decision, owner, deadline, or approval is established by this specification.

| Question ID | Status | Required decision or missing contract | Affected identifiers | Source / dependency |
|---|---|---|---|---|
| OQ-001 | Needs confirmation | Identity provider; login/logout/session-expiry UX; post-login route; choice of BFF/session mechanism; permitted return URLs. | SF-PRE-001–002; all screens | S, p. 21, §5.1; p. 90, §F.2. Authentication/architecture details **To be defined in a later stage**. |
| OQ-002 | Needs confirmation | Tenant/workspace selection, defaults, accessible memberships, context switching, case workspace creation input, and workspace reassignment behavior. | SF-PRE-003; SF-SHELL-F02; SCR-002-F02 | S, pp. 21–24, Chapters 5–6; p. 86, Appendix B.2. |
| OQ-003 | Needs confirmation | Full screen/field/action permission matrix; Workspace Admin-to-Admin mapping; `Owner`, `Member`, and `approver` semantics; Auditor redaction/content scope; health/settings read rights. | User matrix; SF-AUTH-001; SCR-001–008 | S, pp. 11, 22, and 83; SF-CON-008. |
| OQ-004 | Needs confirmation | Canonical screen/menu labels, aliases, Overview status, primary action per screen, browser routes, contextual navigation, default landing, and no-selected-resource behavior. | Screen inventory; SF-NAV-001, 004–006; SCR-009 | S, pp. 7, 14, 43, 47, 57, 60, 67, 77, and 81; SF-CON-001. |
| OQ-005 | Needs confirmation | Safe error placement/copy, dependency-failure states, loading and empty-state presentation, retry controls, disabled-versus-hidden unauthorized actions, and error focus handling. | SF-GEN-005–006, 010, 012; all actions | S, pp. 54–59 and 84. Do not invent error codes. |
| OQ-006 | Needs confirmation | Case-list columns/access scope; search/filter/sort/bulk capabilities; pagination schema/page size/direction/expiry; total count; retained list position; unsaved-change handling. | SCR-001-F04–07; SCR-001-A01–05; SF-NAV-006 | S, p. 14, Figure 2.2; pp. 54 and 57–59. |
| OQ-007 | Needs confirmation | Complete case creation/read/patch schemas; title/description constraints; defaults and required inputs; human case reference; owner selection; `If-Match` encoding and BIGINT transport. | SCR-001-F01; SCR-002-F01–04, F09–12; SCR-002-A01–02 | S, pp. 24–25, 83–86; SF-CON-002, SF-CON-006. |
| **OQ-008** | **Needs confirmation** | **Preserve confirmed edges SCR-002-T01–T06. Define the unspecified closing edge, reopening target and endpoint, and detailed actor/action/trigger/revision/approval guards for each applicable edge. Clarify approval decision-to-case-state linkage without assuming automatic rejection/rework transitions. Preserve CLOSED finality except explicit new-revision reopening.** | **SCR-002-F08; SCR-002-A04, A07–08; SCR-002-T01–T08; SF-AC-005–008; SF-CON-003** | **S, pp. 24–26, Chapter 6; pp. 44–46, Chapter 12; p. 82, Appendix A.1. Domain/API details To be defined in a later stage.** |
| OQ-009 | Needs confirmation | Impact/urgency catalogs, priority matrix, manual override rules, business calendar, timezone configuration, deadline calculation, and advisory breach display. | SCR-001-F04; SCR-002-F05–07, F15; SCR-007-F13 | S, p. 25, §6.3.1. |
| OQ-010 | Needs confirmation | Classification label/reason-code catalogs, confidence format, correction schema/endpoint, sensitivity selector mapping, and rights to lower classifications. | SCR-002-F10, F13–14; SCR-002-A03 | S, p. 12, §2.2.1; p. 62, §17.2.1. |
| OQ-011 | Needs confirmation | Run request/response/steps/SSE schemas; route relationship; admission thresholds; runtime/review-wait semantics; timeout state; event retention/cursor expiry; any end-user cancel/retry controls. | SCR-002-F19, A06; SCR-004; SF-CON-004, SF-CON-007 | S, pp. 12, 15–17, 40–42, 49, 55, 69, 82, and 90. |
| OQ-012 | Needs confirmation | Candidate/approved-result schemas; direct draft editing, if supported; clarification/rework form; artifact revisions; manual publish control, if any; result-pointer exposure. | SCR-002-F16–19; SCR-002-A09–10 | S, pp. 12, 24, and 44–46. No publish endpoint is defined. |
| OQ-013 | Needs confirmation | Review queue/detail schema and read scope; required review field set; rationale rules; decision enum literals; hash algorithm; task transition/expiry/assignment guards; whether evidence-open is an enforced prerequisite; pagination/filter/sort. | SCR-005-F01–14; SCR-005-A01–05 | S, pp. 44–46, 57–59, 82–85. |
| OQ-014 | Needs confirmation | Elevated override role, secondary-reviewer selection, audited reason constraints, override endpoint, and UI placement. | SCR-005-A06; User matrix | S, p. 46, §12.3.2. |
| OQ-015 | Needs confirmation | Upload transport, file count/name constraints, MB conversion, decompression threshold, type-error codes, document transition/status schema, OCR option placement, quality thresholds, quarantine viewing/remediation. | SCR-002-F20–25; SCR-002-A05; SCR-003-F09 | S, pp. 30–32, 82, and 90. |
| OQ-016 | Needs confirmation | Connector providers, configuration/read permissions, credential revoke/reauth flow, capabilities/trust policy, sync states/list pagination, safe cursor projection, remediation and provisioning-status UI. | SCR-006; SCR-007-F04 | S, pp. 27–29, 78, and 90. |
| OQ-017 | Needs confirmation | Public search schema, required query fields, supported filters, display order/sorting/pagination, UI result limits, unsupported-evidence clarification/routing rules, and placement of search controls. | SCR-003-F01–02, F11–12; SCR-003-A02, A06 | S, pp. 34–36, 83, 87, and 90. MCP limits are not public UI pagination limits. |
| OQ-018 | Needs confirmation | Evidence/source-content delivery API, signed-URL lifetime/recovery, source-view launch mode, page/bbox indexing, nonpaginated anchors, viewer controls, and origin return behavior. | SCR-003-F04–09, F12; SCR-003-A03, A05 | S, pp. 31, 35, 52, and 57. |
| OQ-019 | Needs confirmation | Audit event/detail/redaction schema; query filters, time ranges, sorting, cursor behavior, and read rights beyond Auditor, if any. | SCR-008 | S, pp. 11, 62, 83, and 85. |
| OQ-020 | Needs confirmation | Policy Settings read/update endpoints, schema and field constraints, per-setting permissions, version activation timing, reviewer pools/SLA, quotas, toolsets, and exact deterministic thresholds. | SCR-007 | S, pp. 24, 37–39, 44–46, and 90. |
| OQ-021 | Needs confirmation | Combined/separate Usage & Quality/evaluation arrangement; primary action; usage units/currency/time ranges; evaluation setup/status/result schemas; read scope; progress and result display. | SCR-010; screen inventory | S, pp. 64–66, 74–76, 81, and 83. |
| OQ-022 | Needs confirmation | Supported cloud region, exact search provider, identity provider, approved model deployments, corporate retention policy, third-party connector permissions, and per-tenant encryption-key isolation. | SF-PRE-001; SCR-006–007; external integrations | S, p. 10, §1.3.2; p. 90, §F.2. These must be explicit architecture decisions, not assumed defaults. |
| OQ-023 | Needs confirmation | Export/delete tenant-versus-workspace scope; two independent approval checks and actor eligibility; screen placement; request schemas; job-status/download contract; legal-hold display and receipt exposure. | SF-SCP-007; SCR-008-A05; SF-CON-010 | S, pp. 78–80, 83, 88–89. |
| OQ-024 | Needs confirmation | Whether screens/forms are required for membership, legal holds, provisioning, design decisions/baselines, webhook subscriptions, operator replay, or operational release functions; if so, inventory and launch paths. | SF-SCP-008; SCR-004-A06; SCR-008-A05 | Source APIs/operational chapters exist, but primary-screen definitions do not establish these additional screens. S, Chapters 1, 5, 13, 15, 17, 20, and 22. |
| OQ-025 | Needs confirmation | Notification content, channels, delivery/read state, and navigation destinations. | SF-NAV-007 | S, pp. 58–59, §§16.2.2–16.4. |
| OQ-026 | Needs confirmation | Supported browsers/devices, responsive layouts, locale options, accessibility acceptance details, focus recovery, and live-region implementation. | SF-GEN-002–003, 012; all screens | S, pp. 58–59, §16.3. |
| OQ-027 | Needs confirmation | Dashboard summary formulas, scope, APIs, refresh triggers, and mapping of mixed mockup workflow labels to Case/Run/Review/artifact states. | SF-SHELL-F03–07; SCR-001-F03; SCR-009; SF-CON-011 | S, p. 7, Reference UI A; p. 14, Figure 2.2; p. 57, §16.1.2; p. 82, Appendix A.1. |

### Dependencies on Later Specifications

| Dependency | Requirement |
|---|---|
| API contracts | **To be defined in a later stage.** Resolve schemas, permission scopes, literal decision values, revision/idempotency transport, cursor/SSE contracts, and undefined operation errors without changing confirmed methods, paths, states, or guards. |
| Data definitions | **To be defined in a later stage.** Preserve all source-supported domain fields, immutable version/hash relationships, tenant scope, revision safety, review history, and closure lineage. |
| Processing/workflow definitions | **To be defined in a later stage.** Define missing state guards, closing/reopening contract, approval-to-case-state linkage, timeout semantics, classification correction, ingestion quality gates, and degraded-mode behavior. |
| Architecture decisions | Stage 8 will consolidate unresolved decisions using completed Markdown specifications in `08_architecture_decision.md`, linking back to `01_screen_functions.md` and the requirement/question IDs above. That document has not yet been generated, and no decision is presumed here. |
