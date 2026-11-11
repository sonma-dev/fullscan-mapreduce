# 1. Screen Function Specification

## Scope and Users

### Evidence and Requirement Status

This specification defines browser-facing functions for the fictional OrionDesk AI baseline **OD-AI-DDS-001, R1.0, revision 1.3**.

All source references below use **Source** to mean `1794310747-OrionDesk_AI_Detailed_Design_Specification.pdf`. Page numbers are original PDF page numbers.

- **Confirmed:** Explicitly supported by source text or visible reference UI. Reference UI values are examples, not production defaults.
- **Needs confirmation:** Source does not define an implementation choice sufficiently. Such choices must not be silently decided.
- **Proposal:** Suggested screen placement or interaction, not a confirmed source requirement.

Screen IDs are assigned here because the source supplies screen names but no screen identifiers. Source test IDs and technical identifiers are preserved.

### Business Scope

| ID | Status | Requirement | Evidence |
|---|---|---|---|
| SF-001 | Confirmed | Support enterprise-document ingestion, permitted knowledge search, grounded case-response drafting, deterministic policy evaluation, authorized human review, and controlled publication. | Source, pp. 11–12, §§2.1–2.2 |
| SF-002 | Confirmed | Keep retrieval, generation, policy decisions, and reviewer approval as separate records. Partial processing must not appear as an approved answer. | Source, pp. 12–13, §§2.2.2, 2.3.2 |
| SF-003 | Confirmed | Never publish an unapproved high-risk response. Approval binds only to the exact reviewed content hash; publication rechecks evidence authorization. | Source, pp. 11, 44–46, Chapter 12 |
| SF-004 | Confirmed | Support immutable closure lineage, connector health, policy configuration, and redacted audit inspection. | Source, pp. 24–29, 57, 62 |
| SF-005 | Out of scope | Physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing, and administrative cloud permissions for agents are explicitly excluded. | Source, p. 9, §1.2.1 |
| SF-006 | Confirmed | Multilingual OCR beyond English, customer-managed model weights, and cross-region active/active mutation are deferred in this baseline. | Source, p. 10, §1.3.2 |

### Users and Permissions

| User / attribute | Confirmed permissions and restrictions | Needs confirmation | Evidence |
|---|---|---|---|
| Analyst | Create cases, add attachments, request drafts, evaluate evidence, and read authorized cases/runs. Cannot approve their own high-risk recommendation. | Queue visibility, label-correction permissions, closure permission, and manual publication permission. | Source, pp. 11–12; p. 83, §A.2 |
| Reviewer | Read authorized cases/runs; inspect the exact artifact and sources; approve or reject assigned recommendations under policy. | Inbox visibility beyond assigned pools and detailed elevated-role hierarchy. | Source, pp. 45, 58, 83 |
| Workspace Admin / Admin | Manage connectors and policy; start sync; read usage; start evaluations. | Whether “Workspace Admin” and “Admin” are identical assignments; settings-field permissions. | Source, pp. 11, 22, 83 |
| Auditor | Obtain immutable evidence without editing case content; inspect decision metadata, prompt-template digests, and access events within redacted scope. Read audit events. | Detailed content-redaction matrix and export rights beyond the explicit export contract. | Source, pp. 11, 62, 83 |
| Service | Baseline noninteractive role. | No interactive screen access is defined. | Source, p. 22, §5.2.1 |
| Owner | Case mutation scope for `PATCH /v1/cases/{caseId}`. | Whether owner is an attribute, permission, or role; assignment and transfer rules. | Source, p. 83, §A.2 |
| Member | Search scope for `POST /v1/search`. | Relationship to baseline roles and workspace membership. | Source, p. 83, §A.2 |
| Admin + approver | Controlled workspace export/delete initiation. Single Admin is insufficient. | Approver eligibility and approval-capture UI. | Source, pp. 78–80, 83, 88 |

**SF-007 — Confirmed:** Every request must be authenticated and tenant-bound. Authorization combines role, tenant, workspace membership, case sensitivity, document ACL, action, and segregation of duties. Navigation controls are not an authorization boundary. Cross-tenant ID substitution must produce a non-disclosing not-found-equivalent result.  
**Evidence:** Source, pp. 21–23, §§5.1–5.3.

### Prerequisites

1. Authenticate using OIDC authorization-code flow with PKCE.
2. Establish authorized tenant and workspace context.
3. Resolve resource-specific access before displaying case, run, evidence, review, connector, or audit data.
4. Before connector sync, confirm provisioning is complete; incomplete provisioning is visible and blocks sync.
5. Before generation, satisfy workspace-token, queue-age, and provider-capacity admission thresholds.
6. Before review or publication, resolve the current artifact, policy version, required evidence, and reviewer eligibility.

**Evidence:** Source, pp. 21–22, 45, 69, 78. Identity provider, threshold values, login-screen design, tenant/workspace selection method, and post-login landing screen **Need confirmation**.

## Screen Inventory and Navigation

### Primary Screens

All eight screens below are **Confirmed** by Source, p. 57, §16.1.1. Each must have one primary action and a clear status summary. Primary-action selection is unresolved unless stated below.

| ID | Name | Purpose | Users / display conditions | Origins and launch method | Destinations |
|---|---|---|---|---|---|
| SCR-001 | Case Queue | Browse and prioritize permitted cases. | Authorized users; exact list-access scope Needs confirmation. | Sidebar “Case Queue” is visible in reference UI. Initial landing and route Needs confirmation. | Case Detail: Proposal for case-row activation. |
| SCR-002 | Case Detail | Case context, attachments, classifications, response and decision gate. | Analyst / Reviewer read scope; Owner mutation scope. Authorized case required. | Sidebar “Case Detail” is visible; case selection mechanics Needs confirmation. | Evidence Viewer via citations is Confirmed. Run Timeline and review entry are Proposals. |
| SCR-003 | Evidence Viewer | Inspect source provenance and anchored evidence. | Current source ACL required; reviewer must have inspection capability. | Citation click-through is Confirmed; sidebar entry is visible. | Opens source document and highlights anchored page range. Return navigation Needs confirmation. |
| SCR-004 | Run Timeline | Display execution stages, checkpoints and failures. | Analyst / Reviewer run-read scope. | Sidebar “Agent Runs” is visible. Mapping to Run Timeline Needs confirmation. | Evidence and case links: Proposal. |
| SCR-005 | Review Inbox | Assigned human review and binding decisions. | Eligible Reviewer under pool, minimum-role and separation-of-duty policy. | Sidebar “Review Inbox” is visible. Queue item opening mechanics Needs confirmation. | Source evidence inspection is Confirmed. Post-decision destination Needs confirmation. |
| SCR-006 | Connector Health | Monitor capabilities, sync, credentials and exceptions. | Admin may start sync; broader read scope Needs confirmation. | Sidebar “Connectors” is visible. Mapping to Connector Health Needs confirmation. | Sync history/remediation placement Needs confirmation. |
| SCR-007 | Policy Settings | Configure workspace policy. | Workspace Admin manages policy; field-level permissions Needs confirmation. | Launch method, route and navigation location Needs confirmation. | Destination after save Needs confirmation. |
| SCR-008 | Audit Explorer | Inspect immutable, redacted event lineage. | Auditor audit-read scope. | Sidebar “Audit Events” is visible; naming mapping Needs confirmation. | Detail drill-down and return destinations Needs confirmation. |

**Navigation evidence:** Source, p. 7, Reference UI A; pp. 14, 33, 43, 47, 60, 67, 77, 81, representative operator views; p. 57, §16.1.

### Additional Source-Evidenced Views and Unplaced Functions

| ID | Status | View / activity | Required treatment |
|---|---|---|---|
| SCR-009 | Confirmed reference-view evidence; definition incomplete | Overview | Sidebar label exists, but its independent screen behavior is not described. Fields, permissions, primary action and route Need confirmation. |
| SCR-010 | Confirmed reference-view evidence; definition incomplete | Usage & Quality / AI Quality / Evaluation Scorecard | Sidebar “Usage & Quality” and scorecard title exist. Usage and evaluation activities are supported by APIs; whether one screen or multiple screens Needs confirmation. |
| SF-008 | Needs confirmation | Case creation, label correction, connector configuration/reauthentication, membership management, legal hold, export/delete and operator replay UI | Activities/contracts exist, but no dedicated screen or dialog is confirmed. Do not invent screen routes. Proposed placement is recorded beside affected functions below. |

**Evidence:** Source, pp. 7, 12, 21–22, 27, 50, 61–63, 74–81, 83.

### Shared Presentation and Interaction

| ID | Status | Requirement | Evidence |
|---|---|---|---|
| SF-009 | Confirmed | Use accessible text `DRAFT`, `NEEDS_REVIEW`, or `PUBLISHED` for AI artifact status; color/styling is supplementary. | Source, p. 57, §16.1.2 |
| SF-010 | Confirmed | Conform to WCAG 2.2 AA target behavior: visible focus, semantic regions, robust keyboard ordering. Announce only meaningful live state transitions. | Source, p. 58, §16.3.1 |
| SF-011 | Confirmed | Show workspace-local times with timezone labels. Server/API timestamps remain UTC / RFC 3339. Locale changes affect display, not ordering or durable representations. | Source, pp. 54, 59 |
| SF-012 | Confirmed | Refresh reconstructs run progress from server state. SSE uses increasing offsets; reconnect uses `Last-Event-ID` and scoped retained-event backfill. | Source, pp. 55, 58 |
| SF-013 | Confirmed | Errors must be stable and non-sensitive. Do not expose secrets, full prompts, retrieved documents, or unauthorized resource existence in error details or diagnostic telemetry. | Source, pp. 13, 56, 64, 84 |

Reference UI headers show tenant/release context and workspace name. Summary cards show Open Cases, Awaiting Review, Evidence Coverage and Service State. The example values `128`, `14`, `97.6%`, `Healthy`, `Meridian Manufacturing`, and `gateway-r1.2` are **not initial values or fixed configuration**. Metric definitions, aggregation scopes, refresh behavior and placement across screens **Need confirmation**.  
**Evidence:** Source, p. 7, Reference UI A and representative operator views.

## Functions by Screen

### Field Definition Convention

For every table below:

- Names describe source-supported business fields; they do not invent API property names.
- **Unspecified length/format, input requiredness, initial input value, client validation timing, display condition, or selectable-value provider means Needs confirmation**, unless explicitly stated.
- Read-only displays initialize from authorized server state; user input does not apply to them.
- **Confirmed validation boundary:** Validate payloads before transaction entry, at domain invariants, and before tool dispatch. Client validation is convenience only.  
  **Evidence:** Source, p. 56, §15.3.2.
- Proposed field placement does not confirm editability or mandatory input.

### SCR-001 — Case Queue

#### Fields and Lists

| Field ID | Field / meaning | Type, length and format | Required / initial value | Editability, constraints, display and values |
|---|---|---|---|---|
| SCR-001-F01 | Case identifier | Technical ID: UUIDv7; reference UI also shows business labels such as `OD-2026-1042`. Label-generation format Needs confirmation. | Server-provided display. | Read-only; permitted cases only. Mapping of business label to UUID Needs confirmation. |
| SCR-001-F02 | Case title / subject | Text; length Needs confirmation. | Server-provided display. | Read-only list value. |
| SCR-001-F03 | Case/workflow summary status | Text; reference labels include Needs review, In progress, Published, Evidence gap and Triaged. | Server-provided display. | Mapping to separate case/run/artifact states Needs confirmation; do not merge these enums. |
| SCR-001-F04 | Cursor | Opaque pagination token; format and length Needs confirmation. | Initial cursor behavior Needs confirmation. | Server/API cursor pagination; not an editable business field. |
| SCR-001-F05–F08 | Open Cases; Awaiting Review; Evidence Coverage; Service State | Counts, percentage, status text respectively; exact API types/precision Needs confirmation. | Authorized server values; no fixed sample defaults. | Read-only reference UI cards. Definition and display conditions Needs confirmation. |

**Evidence:** Source, pp. 7, 14, 51, 54, 57, 82.

#### Events

| ID | Event | Conditions and processing | Success | Failure / unresolved behavior |
|---|---|---|---|---|
| SCR-001-E01 | Load case list | Authenticated tenant/workspace context; use `GET /v1/cases?cursor=...`. | Authorized cases and clear status summary. | Safe error; layout and empty-state copy Needs confirmation. |
| SCR-001-E02 | Cursor continuation | Valid server cursor. | Retrieve cursor-paginated continuation. | Page size, expired-cursor handling, previous-page support and UI control Needs confirmation. |
| SCR-001-E03 | Open case | Proposal: activate a row. Must resolve authorized current revision. | Proposal: SCR-002. | Foreign-tenant case produces not-found-equivalent display. |
| SCR-001-E04 | Create case | Analyst; exact form placement Needs confirmation. Proposal: primary queue action. | `POST /v1/cases` returns `201` and case ID; case starts `NEW`. | Schema-invalid input: `422`; duplicate-key fingerprint conflict: `409 IDEMPOTENCY_CONFLICT`; no ambiguous success. |

Queue search, filters, sorting, bulk selection, default sort and risk-prioritization algorithm **Need confirmation**; the “Risk Prioritization” reference title alone does not establish an algorithm.  
**Evidence:** Source, pp. 12, 14, 54, 57, 83, 89.

### SCR-002 — Case Detail

Field placement below is a **Proposal** where derived from domain data rather than explicit UI text.

#### Case and Attachment Fields

| Field ID | Name / meaning | Type, length / format | Required / initial value | Editability and constraints / value source |
|---|---|---|---|---|
| SCR-002-F01 | Title | Text; length Needs confirmation. | Input requiredness/default Needs confirmation. | Case stores title; Owner mutation scope. |
| SCR-002-F02 | Description / business context | Text; length/format Needs confirmation. | Requiredness/default Needs confirmation. | Editable-field mapping Needs confirmation. |
| SCR-002-F03 | Impact | Type and vocabulary Needs confirmation. | Requiredness/default Needs confirmation. | Explicit input to priority; selection source Needs confirmation. |
| SCR-002-F04 | Urgency | Type and vocabulary Needs confirmation. | Requiredness/default Needs confirmation. | Explicit input to priority; selection source Needs confirmation. |
| SCR-002-F05 | Priority | Type/vocabulary Needs confirmation. | Derived from impact and urgency. | Must not derive from model output alone; direct editability Needs confirmation. |
| SCR-002-F06 | Sensitivity | Storage `TEXT`; `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`. Length Needs confirmation. | Storage mandatory, default `INTERNAL`; creation-form behavior Needs confirmation. | Changes subject to policy/authorization; selector implementation Needs confirmation. |
| SCR-002-F07 | Case status | Storage `TEXT`; `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED`. | Storage mandatory; case starts `NEW`. | Server-enforced transitions; direct status selector Needs confirmation. |
| SCR-002-F08 | Owner | Identifier/reference; exact representation Needs confirmation. | Requiredness/default Needs confirmation. | Allowed owner set and transfer rights Needs confirmation. |
| SCR-002-F09 | Revision | `BIGINT`, monotonic. | Mandatory storage; default `1`. | Read-only; submit revision precondition with mutations. |
| SCR-002-F10 | Current approved result | Artifact/reference; payload type/length Needs confirmation. | Present only when approved result exists. | Publication-controlled; not interchangeable with candidate draft. |
| SCR-002-F11 | Classification labels | Vocabulary/type/length Needs confirmation. | Asynchronous classification output. | User may correct with reason code; allowed labels/provider Needs confirmation. |
| SCR-002-F12 | Classification confidence and provenance | Type/precision/structure Needs confirmation. | Classification output. | Read-only provenance and confidence display placement is Proposal. |
| SCR-002-F13 | Label correction reason code | Type/length/vocabulary Needs confirmation. | Required when correcting labels. | Validate with label correction; client timing/provider Needs confirmation. |
| SCR-002-F14 | Attachment file | PDF, DOCX, HTML, UTF-8 text; configurable 25 MB per-file cap. | Required for attachment submission; default selection Needs confirmation. | MIME signature and extension must agree; enforce decompression-bomb threshold. Threshold and MB byte interpretation Needs confirmation. |
| SCR-002-F15 | Document status | `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED`. | Server-provided. | Read-only; status polling/update mechanism Needs confirmation. |
| SCR-002-F16 | Quarantine reason / correlation ID / remediation path | Types and length Needs confirmation. | For malformed quarantined records. | Safe read-only output; remediation controls Needs confirmation. |
| SCR-002-F17 | Deadline | Timestamp; workspace-local display with timezone. | Business-calendar calculation. | Breach prediction is advisory and cannot change contractual deadline. |

**Evidence:** Source, pp. 12, 24–26, 29–32, 62, 82, 85–86.

#### Candidate and Decision Gate Fields

| Field ID | Field | Definition and behavior |
|---|---|---|
| SCR-002-F18 | Candidate response | Exact generated artifact; read-only candidate display is Proposal. Editing/revision UI, payload type and length Need confirmation. |
| SCR-002-F19 | Artifact status | Accessible `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED`; initialize from server state. |
| SCR-002-F20 | Policy outcome | `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY`; read-only deterministic outcome. |
| SCR-002-F21 | Evidence summary | Reference UI shows verified citation count; exact count semantics/API type Needs confirmation. |
| SCR-002-F22 | Model | Deployment/version display; source example is not an approved deployment selection. |
| SCR-002-F23 | Approval summary | Reference UI shows assignment/status; initialized from approval records, not inferred from model text. |
| SCR-002-F24 | Gate status | Reference UI shows “Awaiting decision”; complete vocabulary and state mapping Needs confirmation. |

Display fields have no user-input requiredness; missing-data placeholders and conditional panel visibility **Need confirmation**.  
**Evidence:** Source, pp. 7, 44–46, 57–58.

#### Operations

1. **SCR-002-E01 — Read:** Call `GET /v1/cases/{caseId}` for an authorized current revision; display server state.
2. **SCR-002-E02 — Save:** Owner mutation uses `PATCH /v1/cases/{caseId}` with `If-Match`. Success returns `200`. Conflict returns `409 CASE_VERSION_CONFLICT` with current revision. Stale or unauthorized writes leave business state unchanged. Conflict-resolution UX Needs confirmation.
3. **SCR-002-E03 — Classify/correct labels:** Classification asynchronously attaches labels, confidences and provenance. Corrected labels require a reason code. Correction endpoint and navigation Needs confirmation.
4. **SCR-002-E04 — Add attachment:** Analyst submits `POST /v1/cases/{caseId}/attachments`; success `202` starts ingestion, not readiness. Scan before parsing; disable macros; do not fetch embedded remote references. Unsafe files are quarantined and never indexed. Exact upload error codes and transfer-progress display Need confirmation.
5. **SCR-002-E05 — Request grounded draft:** Analyst submits `POST /v1/cases/{caseId}/runs` with `Idempotency-Key`; success `202` starts a bounded workflow. Subscribe to SSE and show retrieval, generation and policy stages. Do not send arbitrary tool definitions.
6. **SCR-002-E06 — Close:** `POST /v1/cases/{caseId}/close` snapshots approved answer, cited document versions and reviewer decisions. Closure role, source-state guard, response status and confirmation UI Need confirmation.
7. **SCR-002-E07 — Rework:** Denied drafts may become new run revisions; never retroactively mark a denied revision approved. Rework control and request payload Need confirmation.
8. **SCR-002-E08 — Citation activation:** Verify citation before display; open SCR-003/source document and highlight the anchored page range.

**Confirmed case transitions:** `NEW → TRIAGED`; `TRIAGED → IN_PROGRESS`; `IN_PROGRESS → PENDING_APPROVAL` or `RESOLVED`; `PENDING_APPROVAL → RESOLVED` or `IN_PROGRESS`. `CLOSED` is final unless explicitly reopened as a new revision. The transition into `CLOSED` and reopening mechanism **Need confirmation**.  
**Evidence:** Source, pp. 7, 25–26, 30, 40–42, 46, 54, 57–58, 83–84.

### SCR-003 — Evidence Viewer

| Field ID | Field / meaning | Type / format and constraints | Required, initial value, editability and display |
|---|---|---|---|
| SCR-003-F01 | Query | Business search input; exact public schema/type/length Needs confirmation. MCP `knowledge.search@v1` uses `query: string`, but this does not define the UI schema. | Input placement, requiredness/default and client timing Needs confirmation. |
| SCR-003-F02 | Source title | Text; length Needs confirmation. | Server evidence display; read-only. |
| SCR-003-F03 | Document revision | Revision representation Needs confirmation. | Read-only immutable source version. |
| SCR-003-F04 | Page anchor / range | Page number and optional bounding box; numbering basis and representation Needs confirmation. | Required resolvable anchor for citations; read-only highlighted source. |
| SCR-003-F05 | Source URI and file hash | URI; source fingerprint/hash. Exact public exposure Needs confirmation. | Authorized source provenance; read-only. |
| SCR-003-F06 | Chunk ID / ACL digest | Opaque technical identifiers/digest; exact types/length Needs confirmation. | Evidence contract includes both; citation IDs remain opaque to end users. |
| SCR-003-F07 | Source document content | Original authorized source/version. | Read-only; no source-rewriting operation defined. |
| SCR-003-F08 | Extraction-quality flags | Empty-page ratio, unknown-character ratio, table-loss indicators, language confidence. Precision/thresholds Needs confirmation. | Low-quality documents remain viewable but excluded from autonomous recommendations. UI placement is Proposal. |
| SCR-003-F09 | OCR provenance | Provenance-marked opt-in fallback. | Read-only indication; opt-in configuration placement/default Needs confirmation. |
| SCR-003-F10 | Reduced-quality status | Visible flag when lexical-only retrieval continues after vector degradation. | Read-only conditional display. Exact wording Needs confirmation. |

**Evidence:** Source, pp. 31–32, 35–36, 57, 69, 87.

| Event ID | Processing and success | Failure / open behavior |
|---|---|---|
| SCR-003-E01 | Read case evidence using `GET /v1/cases/{caseId}/evidence`, or evidence item using `GET /v1/evidence/{evidenceId}`; inspect permitted source anchors. | Contract selection and response schema Needs confirmation. Unauthorized evidence must not be displayed. |
| SCR-003-E02 | Search using `POST /v1/search`; Member scope; `200` returns ACL-filtered lexical + semantic evidence. Ranking uses bounded candidates, reciprocal rank fusion and deterministic re-ranking; diversity reduces redundant same-document hits. | `NO_SUPPORTED_EVIDENCE` for insufficient confidence/quality; clarification or human-routing path Needs confirmation. |
| SCR-003-E03 | Click citation to open exact source and highlight anchored page range. | Invalid/nonresolvable or revoked citations must not appear as verified. Precise failure display Needs confirmation. |

Result sorting controls, filters, pagination, download, zoom and in-document search **Need confirmation**. Source configuration examples specify `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `hybrid_rrf_k: 60`; they are retrieval configuration examples, not confirmed UI pagination limits.  
**Evidence:** Source, pp. 35–36, 57, 90.

### SCR-004 — Run Timeline

| Field ID | Field | Definition |
|---|---|---|
| SCR-004-F01 | Run identifier | UUIDv7 identity; server-provided, read-only. |
| SCR-004-F02 | Run status | `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED`; server-provided text. |
| SCR-004-F03 | Steps / checkpoint | Step kind, status and persisted checkpoint; types/length and list ordering Needs confirmation. |
| SCR-004-F04 | Plan revision | Stored before side effects; read-only display placement is Proposal. |
| SCR-004-F05 | Failed checkpoint / reason | Visible status must report exactly which checkpoint failed. Safe reason vocabulary Needs confirmation. |
| SCR-004-F06 | Evidence metadata | Server-returned metadata; detail schema Needs confirmation. |
| SCR-004-F07 | Model / prompt version | Source-supported review provenance; timeline placement is Proposal. |

All fields initialize from authorized persisted state, are display-only, and have no selectable-value provider except server state. Format, missing-value display and conditional sections **Need confirmation**.

1. **SCR-004-E01:** Read `GET /v1/runs/{runId}` and `GET /v1/runs/{runId}/steps`.
2. **SCR-004-E02:** Subscribe to `GET /v1/streams/runs/{runId}`; reconnect with `Last-Event-ID`.
3. **SCR-004-E03:** Refresh reconstructs progress without rerunning business operations.
4. **SCR-004-E04:** Show failure at missing approval, exhausted call budget, repeated invalid plan, policy denial or deadline expiry. Quota exhaustion is terminal for the current run; do not automatically switch model/data class.
5. **SCR-004-E05:** Show `MODEL_OUTPUT_INVALID` without publication for invalid structured output, unknown fields, invalid citations or control-character injection.

Plan depth is bounded to eight and tool invocations to sixteen. Appendix F gives `run_timeout_seconds: 180` as configuration evidence; timeout scope relative to awaiting human review **Needs confirmation**. Cancel/retry/resume buttons are not defined and **Need confirmation**.  
**Evidence:** Source, pp. 38, 40–42, 49, 55, 58, 82–83, 90.

### SCR-005 — Review Inbox

| Field ID | Field / meaning | Type / format | Required / initial value | Editability, constraints and values |
|---|---|---|---|---|
| SCR-005-F01 | Review task status | `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED`. | Server state. | Read-only; exact queue columns Needs confirmation. |
| SCR-005-F02 | Reviewer pool / assignment | Reference; schema Needs confirmation. | Policy-defined. | Required role and separation of duties enforced; selection UI Needs confirmation. |
| SCR-005-F03 | Candidate artifact | Exact reviewed content; schema/length Needs confirmation. | Available before decision. | Inspection display; must bind decision to same hash. |
| SCR-005-F04 | Source citations | Verified evidence items. | Available for inspection before approval. | Citation click-through; current ACL required. |
| SCR-005-F05 | Model and prompt version | Version identifiers; length Needs confirmation. | Server provenance. | Read-only. |
| SCR-005-F06 | Policy reasons / rule version | Structured reasons/version; representation Needs confirmation. | Server evaluation. | Read-only; LLM cannot override outcome. |
| SCR-005-F07 | Evaluated artifact hash | Digest; serialization Needs confirmation. | Decision must include binding to reviewed artifact. | Not user-editable authority. |
| SCR-005-F08 | Decision | Approval/rejection; literal request values Needs confirmation. | Required for decision capture. | Approve / Reject controls. |
| SCR-005-F09 | Rationale | Text; length/format Needs confirmation. | Stored in approval record; exact mandatory-form rule Needs confirmation. | Reviewer input; validation timing Needs confirmation. |
| SCR-005-F10 | Annotations | Type/length Needs confirmation. | Optional. | Reviewer input. |
| SCR-005-F11 | Actor and timestamp | Principal reference and timestamp. | Recorded with decision. | Server-controlled; workspace-local display. |
| SCR-005-F12 | Expiry / SLA | Configured SLA; timestamp representation Needs confirmation. | Policy-defined. | Read-only; no silent approval at expiry. |

**SCR-005-E01 — Open review:** Load `GET /v1/review-queue`; display exact candidate, citations, model/prompt version and policy reasons. `UserReviewOpened` must be correlated in logs/audit without source text in telemetry.

**SCR-005-E02 — Approve or Reject:**

1. Confirm Reviewer eligibility, current assignment, separation of duties and current artifact.
2. Disable both controls until required review fields are complete. Exact required-field set **Needs confirmation**.
3. Submit `POST /v1/approvals/{approvalId}/decision`.
4. Record decision, actor, timestamp, evaluated artifact hash, rationale and optional annotations.
5. Success returns `200`; show accepted decision, not a fabricated publication success.
6. A changed/wrong artifact is rejected as stale (`409` supported; specific stale error code Needs confirmation).
7. Publication updates the final response pointer atomically with satisfied approval-gate recording and rechecks evidence access.

**SCR-005-E03 — Expiry:** Reassign or escalate according to policy; do not approve implicitly.

**SCR-005-E04 — Override:** Requires elevated role, secondary reviewer and audited reason. UI placement, eligibility and endpoint **Need confirmation**.

Queue filters, sorting, pagination controls, primary action and post-decision navigation **Need confirmation**.  
**Evidence:** Source, pp. 44–46, 58–59, 82–83, 89.

### SCR-006 — Connector Health

Placement of operational detail fields is a **Proposal** based on confirmed connector records.

| Field ID | Field | Definition / constraints |
|---|---|---|
| SCR-006-F01 | Connector identity and status summary | Exact name/type/status enum Needs confirmation; authorized server display. |
| SCR-006-F02 | Capability support | `list`, `fetch`, delta cursor, ACL and delete support; unsupported capability must produce lower-trust mode and explicit visible warning. |
| SCR-006-F03 | Credential reference / reauth state | Workspace-scoped secret reference only; never display tokens. Reference edit UI Needs confirmation. |
| SCR-006-F04 | Sync run history | Server sync outcomes; row schema and timestamp fields Needs confirmation. |
| SCR-006-F05 | Provider cursor / high-watermark | Durable sync checkpoint data; representation and whether user-visible Needs confirmation. |
| SCR-006-F06 | Error ledger / quarantined exceptions | Safe reasons, correlation IDs and remediation path; format Needs confirmation. |
| SCR-006-F07 | Provisioning readiness | Incomplete provisioning visible and blocks sync; status vocabulary Needs confirmation. |
| SCR-006-F08 | Index readiness | Readiness based on index coverage, not only empty queue; coverage definition Needs confirmation. |

Requiredness for operational displays is conditional on available records; initial values are authorized server state. Editability is not confirmed except supported administration activities.

1. **SCR-006-E01 — Sync:** Admin calls `POST /v1/connectors/{connectorId}/sync`; `202` indicates incremental sync initiation. Use `Idempotency-Key` for long-running creation.
2. **SCR-006-E02 — History:** Load `GET /v1/connectors/{connectorId}/runs`.
3. **SCR-006-E03 — Credential revoke:** Operators may revoke credentials; queued jobs fail with `CONNECTOR_REAUTH_REQUIRED` without token disclosure. Control placement and endpoint Need confirmation.
4. **SCR-006-E04 — Sync exception:** Honor provider `Retry-After`, bounded backoff and workspace quotas. Malformed documents may quarantine while remaining batch proceeds; cursor advances only after durable preceding-item outcomes.
5. **SCR-006-E05 — ACL/delete propagation:** Source deletion creates tombstone/index-removal work. ACL changes invalidate evidence caches before the next retrieval.

Connector creation/edit fields, reauthorization launch, pause/resume UI, sync schedule, list sorting/pagination and remediation permissions **Need confirmation**.  
**Evidence:** Source, pp. 27–29, 78, 83, 90.

### SCR-007 — Policy Settings

The following are **Confirmed workspace settings**; their placement together on this screen is a **Proposal**.

| Field ID | Setting | Type, requiredness and default | Constraints / selectable-value source |
|---|---|---|---|
| SCR-007-F01 | Retention class | Type/vocabulary/default Needs confirmation. | Corporate retention policy unresolved; legal holds remain exceptions. |
| SCR-007-F02 | Allowed models | Deployment references; collection type/default Needs confirmation. | Whitelist specific approved deployments, not provider brands. `GET /v1/model-catalog` exists; response schema Needs confirmation. |
| SCR-007-F03 | Connector credential references | Reference types/default Needs confirmation. | Vault-backed, workspace-scoped; no raw secrets in public response. |
| SCR-007-F04 | Approved toolsets | Version-pinned capability references; schema/default Needs confirmation. | Discovery never authorizes execution; no arbitrary tool definitions from browser. |
| SCR-007-F05 | Reviewer routing | Reviewer pools, minimum role, separation of duties; schema/default Needs confirmation. | Pool provider, eligible roles and SLA values Needs confirmation. |
| SCR-007-F06 | Policy / configuration revision | Version/revision representation Needs confirmation. | Read-only current revision; updates require revision preconditions and durable audit. |
| SCR-007-F07 | Workspace timezone / calendar | Domain uses timezone/business calendars; editor placement is Proposal. | Allowed timezone/calendar catalog and defaults Needs confirmation. |

**SCR-007-E01 — Configuration update:** Validate configuration and revision before durable mutation, preserve tenant/actor/correlation context, and audit accepted updates. Stale or unauthorized updates must leave state unchanged.

The source associates workspace settings text with `PATCH /v1/cases/{caseId}`; this does **not** establish a valid workspace-settings save contract. Load/save endpoints, individual-field edit permissions, required fields, primary action, success display and conflict code **Need confirmation**.

Appendix F gives `auto_publish_classification: INTERNAL`, `require_human_review_for: [HIGH_RISK, RESTRICTED]`, and `self_approval_allowed: false` as configuration examples. Do not infer unconditional publication permission from classification alone.  
**Evidence:** Source, pp. 7, 24, 37–39, 45, 90.

### SCR-008 — Audit Explorer

| Field ID | Field | Definition |
|---|---|---|
| SCR-008-F01 | Event ID | Identity; UUIDv7 baseline; read-only. |
| SCR-008-F02 | Tenant / actor | Authorized event context; identifier representation Needs confirmation. |
| SCR-008-F03 | Action | Event action; vocabulary/length Needs confirmation. |
| SCR-008-F04 | Digest / lineage | Immutable digest and hash-chain evidence; public representation Needs confirmation. |
| SCR-008-F05 | Decision metadata | Historical decision data within redacted scope; read-only. |
| SCR-008-F06 | Prompt-template digests | Digest/version evidence, not unrestricted full prompt content. |
| SCR-008-F07 | Access events | Authorized/denied access metadata; must not disclose unauthorized resource existence. |
| SCR-008-F08 | Time / correlation | Workspace-local timestamp with timezone and safe correlation reference; public schema Needs confirmation. |
| SCR-008-F09 | Cursor | Server pagination token; format/default Needs confirmation. |

All business fields are read-only and initialized from authorized audit records. Historical review decisions cannot be altered. Exact mandatory columns, redaction rules, detail panels and display conditions **Need confirmation**.

**SCR-008-E01:** Auditor loads `GET /v1/audit/events`; `200` returns cursor-paginated immutable log.  
**SCR-008-E02:** Continue with server cursor; page size, controls and cursor error handling Need confirmation.  
**SCR-008-E03:** Historical-edit attempts must fail; audit ledger is append-only and independently retained.

Search/filter fields, sorting, event detail navigation and audit-download UI **Need confirmation**.  
**Evidence:** Source, pp. 11, 23, 62, 77, 83, 85, 88.

### SCR-009 and SCR-010 — Incomplete Reference Views

#### SCR-009 — Overview

Only navigation and repeated summary-card evidence is confirmed. Apply SCR-001-F05–F08 if those cards are retained, but independent content, calculations, primary action, users, fields and navigation **Need confirmation**.  
**Evidence:** Source, p. 7, Reference UI A; p. 14.

#### SCR-010 — Usage & Quality / Evaluation Scorecard

| Field ID | Source-supported data | Definition and unresolved constraints |
|---|---|---|
| SCR-010-F01 | Costs / quotas / trends | `GET /v1/usage` returns costs, quotas and trend estimates; currency, units, time window and precision Needs confirmation. |
| SCR-010-F02 | Budget / forecast / rejected excess requests | Daily rollups show these values; screen placement is Proposal. |
| SCR-010-F03 | Workspace cost center / model version | Usage attribution dimensions; display and filters Needs confirmation. |
| SCR-010-F04 | Evaluation scorecard | Citation precision target `>=0.97`, unsupported-claim rate `<=0.02`, high-risk policy recall `1.00` on frozen safety suite; display schema Needs confirmation. |
| SCR-010-F05 | Confidence intervals / distribution shift | Reported by domain; numeric format and thresholds Needs confirmation. |
| SCR-010-F06 | Evaluation identity / status | Schema and status vocabulary Needs confirmation. |

All output fields are read-only server values; evaluation-input fields, initial values and requiredness are unspecified.

1. **SCR-010-E01:** Admin reads `GET /v1/usage`, success `200`.
2. **SCR-010-E02:** Admin starts frozen benchmark using `POST /v1/evaluations`, success `202`.
3. **SCR-010-E03:** Read `GET /v1/evaluations/{evaluationId}`.
4. **SCR-010-E04:** Low statistical confidence blocks release rather than proving equivalence; no release-approval button is defined here.

Primary action, separate usage/evaluation screens, sorting, pagination, filters and failure displays **Need confirmation**.  
**Evidence:** Source, pp. 65–66, 74–76, 81, 83.

### Unplaced Operational Activities

**SF-014 — Confirmed behavior; UI Needs confirmation.**

| Activity | Source-supported behavior | Missing screen decisions |
|---|---|---|
| Membership management | `PUT /v1/workspaces/{workspaceId}/members` exists. | Role scope, fields, selection provider, navigation and response schema. |
| Legal hold | `POST /v1/security/holds` exists; deletion respects holds. | Authorized users, hold form, required rationale, scope and release mechanism. |
| Workspace export | `POST /v1/workspaces/{workspaceId}/export`, `202`, Admin + approver; two independent approval checks. Package metadata, approved artifacts, source references and audit manifests with checksums; exclude secrets and internal model prompts. | Initiation/approval screens, status retrieval, download and failure UX. |
| Workspace delete | `POST /v1/workspaces/{workspaceId}/delete`, `202`, Admin + approver; two independent approval checks. Enforce legal holds, tombstones, blob/index removal and completion receipts. | Confirmation fields, approval screens, progress and partial-retention display. |
| Dead-letter replay | `POST /internal/deadletters/{id}/replay`; operator reason, dry-run validation and scope limit required. Preserve event identity unless explicit schema-migration provenance exists. | Whether any browser UI exists; never expose internal endpoint as a public screen contract without confirmation. |

**Evidence:** Source, pp. 21–23, 48–50, 61–63, 78–80, 83, 88.

## Integrations and Acceptance Criteria

### Integration Inventory

| ID | Integration / boundary | Screen inputs and outputs | Confirmed requirements / gaps | Evidence |
|---|---|---|---|---|
| INT-SF-001 | OIDC identity / edge | Principal, tenant and membership context. `GET /v1/me`. | PKCE; no long-lived refresh token in local storage. BFF secure, HttpOnly, SameSite cookie issuance is a source option, not a settled architecture. Provider/login UX Needs confirmation. | Source, pp. 21–22 |
| INT-SF-002 | Case APIs | Case creation/read/mutation/close; attachments; evidence. | Preserve `If-Match`, idempotency and authorized current revision. Full request/response schemas To be defined in a later stage. | Source, pp. 25, 30, 57, 83 |
| INT-SF-003 | Run APIs and SSE | Create run; read run/steps; stream progress. | Durable server reconstruction, scope-safe event backfill. Retained-event duration and stale-offset behavior Needs confirmation. | Source, pp. 40–42, 55, 58 |
| INT-SF-004 | Ingestion and source objects | File input; document status; authorized original source/anchors. | Scan before parsing, immutable derivatives, opt-in OCR provenance, short-lived access-controlled signed URLs. Public object-access contract Needs confirmation. | Source, pp. 30–32, 52 |
| INT-SF-005 | Retrieval | Query input; evidence set/citations. | ACL filter before model text release; citation verification before display; no unsupported fabricated context. Search provider Needs confirmation. | Source, pp. 34–36, 90 |
| INT-SF-006 | Connector providers / secret vault | Sync commands, capabilities and safe health results. | Preserve source identity/ACL/change history; no raw credentials in browser output. Provider permissions and connector list Needs confirmation. | Source, pp. 27–29, 90 |
| INT-SF-007 | Model gateway / approved tools | Validated case input and permitted evidence; candidate/provenance/errors. | Browser uses REST, not arbitrary tool definitions or internal model calls. Approved models and regions Needs confirmation. | Source, pp. 7, 37–42, 87, 90 |
| INT-SF-008 | Policy / approvals | Exact artifact, review fields and decision hash; binding decision output. | Deterministic outcomes, segregation of duties and atomic publication gate. Schemas To be defined in a later stage. | Source, pp. 44–46 |
| INT-SF-009 | Audit / usage / evaluation | Scoped immutable records, cost outputs, benchmark operation. | Redaction and append-only history; no full source content in telemetry. Public schemas To be defined in a later stage. | Source, pp. 62–66, 74–76 |

### Shared Failure and Mutation Contract

**SF-015 — Confirmed:**

- Long-running POST creation requires `Idempotency-Key`; identical replay returns original operation. Changed fingerprint with the same key returns `IDEMPOTENCY_CONFLICT`.
- Case idempotency associates actor/request fingerprint with one outcome for 24 hours.
- HTTP `409` represents revision conflict, `429` quota, and `422` schema-invalid request.
- Throttled AI-run clients receive `429` plus `Retry-After`; saved cases remain available.
- Dependency failure produces a documented retryable error or a persisted asynchronous job identifier, never ambiguous success.
- Safe error envelope fields include `error.code`, `message`, `correlation_id`, `retryable`, and optional safe `details`.
- Validation/permission failures are permanent and not retried.
- Accepted durable transitions retain tenant, revision, actor, occurrence time and correlation context; replay must not apply a second mutation.

Exact UI messages, retry control, field-error mapping and unsaved-input preservation **Need confirmation**.  
**Evidence:** Source, pp. 12–13, 25, 49, 54, 69, 84, 89.

### Acceptance Criteria

| ID | Prerequisites | Action | Expected result | Traceability |
|---|---|---|---|---|
| AC-SF-001 | Authorized Analyst and valid case payload/key. | Create case twice with identical key/body. | One `NEW` case, same outcome/identifier, no duplicate mutation. Case-create P95 under/within 300 ms as described by source under reference load; strict boundary reconciliation Needs confirmation. | Source, pp. 12, 65, 68, 83, 89; `TST-001` |
| AC-SF-002 | Previously used creation key. | Change body and reuse key. | `409 IDEMPOTENCY_CONFLICT`; no second case. | Source, pp. 54, 89; `TST-002` |
| AC-SF-003 | Valid foreign-tenant case ID. | Read or navigate to it. | Not-found-equivalent non-disclosing response; no private existence or content shown. | Source, pp. 23, 89; `TST-003` |
| AC-SF-004 | Owner has stale revision. | Save case with stale `If-Match`. | `409 CASE_VERSION_CONFLICT`, current revision returned; business state unchanged. | Source, pp. 25, 84 |
| AC-SF-005 | Analyst and unsafe PDF. | Attach file. | Quarantine, no indexing, no approved/ready misrepresentation. | Source, pp. 30, 89; `TST-015` |
| AC-SF-006 | Authorized case and accepted run. | Observe stages, disconnect SSE, reconnect and refresh. | Recover progress from scoped persisted state and retained offsets without recreating run or replaying side effects. | Source, pp. 55, 58 |
| AC-SF-007 | Indexed source initially permitted. | Revoke source access, then query/click/publish. | No forbidden evidence on next query; publication rechecks and rejects stale authorization. | Source, pp. 28, 46, 89; `TST-004` |
| AC-SF-008 | Reviewer has current task. | Inspect candidate/citations, leave required fields incomplete. | Evidence inspection is available; Approve and Reject remain disabled. | Source, pp. 57–58 |
| AC-SF-009 | Candidate changed since review. | Approve old/wrong artifact hash. | Stale rejection, audited, no publication of changed artifact under old approval. | Source, pp. 45–46, 89; `TST-006` |
| AC-SF-010 | High-risk candidate from acting Analyst. | Attempt self-approval or unapproved publication. | Denied; no response published. | Source, pp. 11, 44–46, 85, 90 |
| AC-SF-011 | Review task reaches configured expiry. | Process expiry. | No implicit approval; reassignment/escalation recorded. | Source, pp. 45, 89; `TST-010` |
| AC-SF-012 | Model returns schema-invalid output. | Complete generation attempt. | `MODEL_OUTPUT_INVALID`; no publication. | Source, pp. 38, 89; `TST-005` |
| AC-SF-013 | Insufficient supported evidence. | Search/request draft. | `NO_SUPPORTED_EVIDENCE`, clarification or human route; missing citations never yield falsely approved output. Routing choice Needs confirmation. | Source, pp. 36, 89; `TST-009` |
| AC-SF-014 | Generation unavailable / vector degraded. | Edit case and search evidence. | Manual editing/search remain available; permitted lexical fallback shows reduced-quality flag; no approval/auth bypass. | Source, pp. 69, 79 |
| AC-SF-015 | Keyboard-only user. | Open case, inspect evidence, use permitted controls. | No blocked action, visible focus, semantic navigation and meaningful live announcements. | Source, pp. 58, 89; `TST-011` |
| AC-SF-016 | Closed case with approved result. | Close and inspect lineage. | Immutable snapshot includes approved artifact, cited versions and reviewer decisions; eligible retention respects legal holds. | Source, pp. 25–26 |
| AC-SF-017 | Single Admin or held workspace. | Attempt export/delete. | Single Admin cannot satisfy two-person controls; held records are protected and receipted. UI completion workflow Needs confirmation. | Source, pp. 78–80, 88–89; `T-11`, `TST-013` |
| AC-SF-018 | Auditor with permitted redacted scope. | Browse events and attempt historical modification. | Cursor-paginated immutable evidence visible; historical modification denied; no unrestricted prompts/secrets disclosed. | Source, pp. 11, 62, 83, 88; `T-09` |

The normal end-to-end acceptance procedure is:

1. Create and classify a permitted case.
2. Ingest allowed attachments.
3. Retrieve currently permitted anchored evidence.
4. Produce a validated grounded draft.
5. Evaluate deterministic policy.
6. Obtain required eligible human review on the exact artifact.
7. Publish only after satisfied gate and current authorization checks.

**Evidence:** Source, p. 75, §21.3.1. Exact button placement and automatic-versus-user-triggered publication remain unresolved.

## Consistency and Open Questions

No earlier specifications exist. This document does not authorize unresolved implementation choices. API, data, workflow and operational details are **To be defined in a later stage**; Stage 8 must consolidate open decisions from completed Markdown specifications into `08_architecture_decision.md` with links to `01_screen_functions.md` and affected IDs.

### Source Conflicts and Required Clarifications

| ID | Status | Affected IDs | Evidence / conflict | Required clarification or amendment |
|---|---|---|---|---|
| OQ-SF-001 | Needs confirmation | SCR-001–SCR-010 | Source §16.1.1, p. 57 names eight primary screens. Reference UI adds Overview/Usage & Quality and alternate names; selected sidebar items often disagree with visible titles (pp. 7, 14, 43, 47, 60, 67, 77, 81). | Confirm canonical names, alias mappings, independent screen count, selected-nav behavior and routes. Do not reproduce inconsistent highlighting as a requirement. |
| OQ-SF-002 | Needs confirmation | SCR-007-E01 | Workspace-settings subsection uses case PATCH endpoint, Source p. 24, §6.1.1. | Define workspace settings load/save contract; do not mutate a case to save workspace configuration. |
| OQ-SF-003 | Needs confirmation | SCR-002-E05, INT-SF-003 | Source pp. 15–17 uses `POST /v1/runs`; pp. 12, 40, 83 uses `POST /v1/cases/{caseId}/runs`. | Establish canonical browser creation endpoint and relationship between both supported paths. |
| OQ-SF-004 | Needs confirmation | SF-009, SCR-001-F03, SCR-002-F07, SCR-004-F02 | Artifact labels differ from case/run states and reference summary labels, Source pp. 7, 57, 82. | Define explicit display mapping while retaining separate state models. |
| OQ-SF-005 | Needs confirmation | SCR-002-E06, SCR-002-E07 | Case transitions omit predecessor to CLOSED; reopening described only as new revision, Source p. 25. | Define close/reopen guards, role scope, endpoint and preserved lineage. |
| OQ-SF-006 | Needs confirmation | SCR-004-E04, SCR-005-E03 | Missing approval is a stop condition, Source p. 41; `AWAITING_REVIEW` is a workflow state, pp. 49, 82; timeout example 180 seconds, p. 90. | Distinguish valid awaiting review from missing-approval failure and determine timeout coverage. |
| OQ-SF-007 | Needs confirmation | SF-015 | Source p. 54 describes snake-case codes while explicit examples use uppercase `CASE_VERSION_CONFLICT`, `IDEMPOTENCY_CONFLICT`, etc. | Preserve exact supported literals; resolve naming convention in API specification rather than normalize silently. |
| OQ-SF-008 | Needs confirmation | AC-SF-001 | Source p. 12 says within 300 ms; p. 65 says under 300 ms. | Confirm strict/non-strict test boundary and measurement of API response versus browser display. |

### Open Screen and Field Decisions

| ID | Affected requirements | Open decision / dependency | Source location |
|---|---|---|---|
| OQ-SF-009 | SF-007, all screens | Complete permission matrix; Owner/Member meanings; Admin terminology; login/tenant/workspace selection and session-expiry UX. | Source pp. 11, 21–23, 83; detailed UX unavailable |
| OQ-SF-010 | SCR-001–SCR-010 | One primary action per screen, navigation origins/destinations, launch routes, browser-back behavior and authorized deep-link handling. | Source p. 57; detailed routes unavailable |
| OQ-SF-011 | All field tables | Public field schemas, lengths, required input sets, defaults, allowed catalogs, validation timing, conditional display and empty/error placeholders. | Source pp. 24, 45, 58, 85–86 provide partial evidence only |
| OQ-SF-012 | SCR-001, SCR-003, SCR-005, SCR-006, SCR-008, SCR-010 | Search/filter/sort controls, cursor page sizes, default ordering, continuation UI and invalid-cursor behavior. | Source pp. 54, 57, 83; control details unavailable |
| OQ-SF-013 | SCR-001-F05–F08, SCR-002-F21 | Summary metric formulas, aggregation scope, refresh triggers and which screens display shared cards. | Source p. 7 and representative views |
| OQ-SF-014 | SCR-002-F01–F17, E03 | Case-creation form placement, label vocabulary/correction endpoint, impact/urgency-to-priority rules, owner choices and business calendar configuration. | Source pp. 12, 24–25 |
| OQ-SF-015 | SCR-002-F14–F16, SCR-003 | Attachment count/aggregate limits, 25 MB byte interpretation, decompression threshold, OCR opt-in UI, quarantine remediation and signed-source access. | Source pp. 29–32, 52 |
| OQ-SF-016 | SCR-003, SCR-005 | Anchor numbering/representation, citation failure display, exact required review fields, rationale requirement, decision enum, stale-decision code, overrides and publication trigger. | Source pp. 31, 35, 44–46, 57–58, 83 |
| OQ-SF-017 | SCR-004 | Cancel/retry/resume support, SSE retention and expired offsets, run step ordering and recoverable timeout representation. | Source pp. 12, 40–42, 55, 82 |
| OQ-SF-018 | SCR-006–SCR-007 | Connector configuration/reauthentication, provisioning status UI, policy field authority, model/tool catalogs, review pools and SLA thresholds. | Source pp. 24, 27–29, 37, 45, 78 |
| OQ-SF-019 | SCR-008–SCR-010 | Redaction matrix, audit detail fields, usage units/time windows, evaluation schemas and whether usage/quality views are separate. | Source pp. 11, 62, 65, 75, 81 |
| OQ-SF-020 | SF-014 | Place membership, holds, export/delete and replay functions; define authorized forms, approvals, progress, receipts and downloads without inventing dedicated screens. | Source pp. 21–23, 50, 61–63, 78–80 |
| OQ-SF-021 | INT-SF-001, INT-SF-005–007, SCR-007 | Select cloud region, search provider, identity provider, approved model deployments, corporate retention policy and third-party connector permissions through recorded architecture decisions. | Source p. 90, §F.2 |
| OQ-SF-022 | SF-006, INT-SF-004 | Per-tenant encryption-key isolation versus rotation throughput remains unresolved; deferred multilingual OCR must not be accidentally enabled by localization work. | Source p. 10, §1.3.2 |
| OQ-SF-023 | SF-010–SF-011 | Supported locales, locale-selector placement, screen-reader evidence-view behavior and concrete accessibility verification fixtures. | Source pp. 58–59, 89 |
| OQ-SF-024 | SF-015, all mutations | Failure-message copy, safe field-detail mapping, retry interactions and conflict/unsaved-input recovery. | Source pp. 54, 84; browser recovery details unavailable |

**Required later-stage consistency:** Preserve all `SCR-*`, `SF-*`, `INT-SF-*`, `AC-SF-*`, and `OQ-SF-*` identifiers. Retain Proposal status for suggested placement/navigation unless new source evidence or an explicit recorded decision confirms it. No owner, deadline or approval for these unresolved decisions is supplied by the source.
