# 2. API Specification

## API Inventory and Responsibilities

### Specification Basis and Status

| Item | Definition |
|---|---|
| Specification file | `02_api.md` |
| Source | `1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Source baseline | `OD-AI-DDS-001`, release `R1.0`, design revision `1.3` |
| Previous specification | [`01_screen_functions.md`](01_screen_functions.md) |
| Scope | Source-described public REST APIs, internal HTTP/RPC interfaces, asynchronous event boundaries, MCP/A2A contracts, and outbound integrations needed by the application. |
| Identifier convention | `API-001`–`API-050` identify interfaces. `API-COM-xxx` identifies shared requirements; `API-PROC-xxx` identifies processing requirements; `AC-API-xxx` identifies acceptance criteria; `OQ-API-xxx` identifies unresolved contracts. These API numbers are assigned here because the source describes the `API` namespace but does not assign individual endpoint numbers. |
| Citation convention | `[DDS]` identifies the source filename above. Citations use original PDF page numbers and source sections. |

[DDS]: 1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf

The following statuses apply throughout:

- **Confirmed:** The source establishes the interface, behavior, constraint, literal value, or identified contract content.
- **Needs confirmation:** An implementation contract is absent, ambiguous, or conflicting.
- **Proposal:** An explicitly suggested transport, field mapping, or example. It is not an approved contract.

**API-COM-001 — Contract interpretation.** A confirmed endpoint does not imply a complete request or response schema. A database field does not automatically become a public JSON property or editable request field. An example value does not become production configuration. Unresolved contracts must be resolved explicitly before the affected interface is implemented as a production contract.  
**Sources:** [DDS], pp. 1–2; p. 8, §1.1.1; p. 82, Appendix A introduction; p. 90, Appendix F and §F.2.  
**Screen trace:** `SCR-COM-001`, `SCR-COM-010`, and the field-table interpretation in [`01_screen_functions.md`](01_screen_functions.md#shared-field-and-interaction-contracts).

### Authentication and Execution Profiles

The inventory uses the following profiles.

| Profile | Confirmed authentication and boundary | Authorization | Open contract |
|---|---|---|---|
| **P — Public application API** | Requests are bound to an authenticated principal and tenant. Interactive authentication uses OIDC authorization-code flow with PKCE. API tokens carry issuer, audience, expiry, subject, and tenant; unexpected algorithms or missing tenancy claims are rejected. | Resource checks combine role, tenant, workspace membership, sensitivity, source ACL, requested action, and segregation of duties. | Token transport, claim names, issuer/audience values, accepted algorithms, token lifetime, and BFF/session selection: OQ-API-001. |
| **S — Internal service API** | Internal calls use mTLS-authenticated HTTP or generated gRPC contracts as applicable. Service-to-service audience checks, TLS, scoped IAM, and distinct workload identities apply. | Independently authorized service and resource scope; an internal network or `Service` role alone does not establish permission to invoke every internal operation. | Exact caller identities, audiences, IAM grants, RPC transport per interface, and operator access: OQ-API-002/OQ-API-028. |
| **X — External provider integration** | Connector workers exchange scoped service credentials with repositories. The model gateway isolates provider credentials and sends only scoped context. Managed identity replaces static credentials where supported. | Explicit endpoint allowlists, approved deployments, workspace scope, and provider-specific permissions. | Exact providers, URLs, methods, credential flows, regions, permissions, and adapter schemas: OQ-API-034. |
| **E — Signed asynchronous boundary** | Background jobs carry immutable tenant identity in signed envelopes. Events use versioned envelopes and canonical JSON. | Consumers validate tenant/resource scope, operation authorization, event identity, and aggregate revision. | Signing scheme, key distribution, signature transport, complete event schemas, and broker topology: OQ-API-035. |

**Sources:** [DDS], pp. 15–17, §§3.1–3.3; pp. 18–23, §§4.1 and 5.1–5.3; p. 48, §13.1; p. 87, §C.2.

**API-COM-002 — Non-disclosing resource access.** Foreign-tenant ID substitution must return the same class of not-found response as an absent ID. Denial evidence retains the principal and denied resource class without revealing private resource existence.  
**Sources:** [DDS], p. 23, §5.3.2; p. 89, `TST-003`.  
**Screen trace:** `SCR-COM-002`, `SCR-COM-003`.

### Public Application API Inventory

`Sync` means request/reply processing. `Async` means that the request accepts durable work whose completion occurs later. A `202` response is not completion of that work.

| API ID | Purpose and responsibility | Calling screen/action or system | Behavior | Method and path | Authentication / authorization | Confirmed result | Source |
|---|---|---|---|---|---|---|---|
| <a id="api-001"></a>API-001 | Create a versioned case and initiate classification through durable events | [SCR-002-A02](01_screen_functions.md#scr-002); launch from SCR-001 remains proposed | Sync creation; async classification | `POST /v1/cases` | P; `Analyst` and authorized workspace | `201` | [DDS], pp. 11–13, Chapter 2; p. 83, §A.2 |
| <a id="api-002"></a>API-002 | List authorized cases | [SCR-001-A01/A03](01_screen_functions.md#scr-001) | Sync | `GET /v1/cases`; illustrated query `?cursor=...` | P; list-read role predicate **Needs confirmation** | **Needs confirmation** | [DDS], pp. 57–59, §§16.1–16.4 |
| <a id="api-003"></a>API-003 | Read the authorized current case revision | [SCR-001-A02](01_screen_functions.md#scr-001), [SCR-002-A01](01_screen_functions.md#scr-002) | Sync | `GET /v1/cases/{caseId}` | P; `Analyst / Reviewer`, with resource authorization | `200` | [DDS], p. 83, §A.2 |
| <a id="api-004"></a>API-004 | Mutate authorized case fields using a revision precondition | [SCR-002-A03](01_screen_functions.md#scr-002) | Sync transactional mutation | `PATCH /v1/cases/{caseId}` | P; `Owner` predicate; role/relationship definition unresolved | `200`; conflict `409` | [DDS], pp. 24–26, Chapter 6; p. 83, §A.2 |
| <a id="api-005"></a>API-005 | Close a case and snapshot approved-output lineage | [SCR-002-A09](01_screen_functions.md#scr-002) | Completion mode **Needs confirmation** | `POST /v1/cases/{caseId}/close` | P; closure role and complete state guards unresolved | **Needs confirmation** | [DDS], pp. 24–26, §§6.1–6.4 |
| <a id="api-006"></a>API-006 | Accept an attachment and create ingestion work | [SCR-002-A05](01_screen_functions.md#scr-002) | Async | `POST /v1/cases/{caseId}/attachments` | P; `Analyst`, authorized case/workspace | `202` | [DDS], pp. 30–32, Chapter 8; p. 83, §A.2 |
| <a id="api-007"></a>API-007 | Read authoritative document-ingestion status | [SCR-002-A06](01_screen_functions.md#scr-002) | Sync | `GET /v1/documents/{documentId}/status` | P; document-status read predicate unresolved | **Needs confirmation** | [DDS], pp. 30–32, §§8.1–8.4 |
| <a id="api-008"></a>API-008 | Read permitted evidence associated with a case | [SCR-003-A01](01_screen_functions.md#scr-003); SCR-002/SCR-005 evidence panels | Sync | `GET /v1/cases/{caseId}/evidence` | P; case/evidence-read predicates unresolved; source ACL required | **Needs confirmation** | [DDS], pp. 57–59, §§16.1–16.4 |
| <a id="api-009"></a>API-009 | Retrieve ACL-filtered lexical and semantic evidence | [SCR-003-A02/A04/A05](01_screen_functions.md#scr-003); search-control placement remains proposed | Sync | `POST /v1/search` | P; `Member` predicate, permitted documents | `200` for supported retrieval | [DDS], pp. 34–36, Chapter 9; p. 83, §A.2 |
| <a id="api-010"></a>API-010 | Read an authorized evidence resource | [SCR-003-A03](01_screen_functions.md#scr-003), [SCR-005-A03](01_screen_functions.md#scr-005) | Sync | `GET /v1/evidence/{evidenceId}` | P; evidence-read predicate unresolved; current source permission required | **Needs confirmation** | [DDS], pp. 34–36, §§9.1–9.4 |
| <a id="api-011"></a>API-011 | Start a bounded case AI workflow | [SCR-002-A07/A11](01_screen_functions.md#scr-002); rework binding unresolved | Async | `POST /v1/cases/{caseId}/runs` | P; `Analyst`, authorized case, admission and policy checks | `202` | [DDS], pp. 12–13, 40–42, 58; p. 83, §A.2 |
| <a id="api-012"></a>API-012 | Alternate run-create surface described by the architecture chapter | Same run activity; no separate screen action confirmed | Long-running workflow; exact relationship to API-011 unresolved | `POST /v1/runs` | P; exact role and case-binding contract unresolved | **Needs confirmation** | [DDS], pp. 15–17, Chapter 3 |
| <a id="api-013"></a>API-013 | Read run stages and evidence metadata | [SCR-004-A01](01_screen_functions.md#scr-004); SCR-002 progress | Sync | `GET /v1/runs/{runId}` | P; `Analyst / Reviewer`, authorized run | `200` | [DDS], pp. 15–17; p. 83, §A.2 |
| <a id="api-014"></a>API-014 | Read execution steps and checkpoints | [SCR-004-A01](01_screen_functions.md#scr-004) | Sync | `GET /v1/runs/{runId}/steps` | P; step-read role predicate unresolved | **Needs confirmation** | [DDS], pp. 40–42, §§11.1–11.4 |
| <a id="api-015"></a>API-015 | Stream resumable, scoped run progress | [SCR-004-A02/A03](01_screen_functions.md#scr-004); SCR-002-A07 | Long-lived SSE connection | `GET /v1/streams/runs/{runId}` | P; `Analyst / Reviewer`, authorized run and backfill scope | `200` | [DDS], pp. 54–56, §15.2.1; p. 83, §A.2 |
| <a id="api-016"></a>API-016 | Read policy-routed review work | [SCR-005-A01/A02](01_screen_functions.md#scr-005) | Sync | `GET /v1/review-queue` | P; authorized policy-selected reviewers; exact visibility predicate unresolved | **Needs confirmation** | [DDS], pp. 44–46, Chapter 12 |
| <a id="api-017"></a>API-017 | Record a decision bound to the exact reviewed artifact | [SCR-005-A04/A05](01_screen_functions.md#scr-005) | Sync decision record; publication validation may follow asynchronously | `POST /v1/approvals/{approvalId}/decision` | P; `Reviewer`, task validity, hash, role, and separation of duties | `200`; conflict `409` | [DDS], pp. 44–46; p. 83, §A.2 |
| <a id="api-018"></a>API-018 | Start incremental connector synchronization | [SCR-006-A02](01_screen_functions.md#scr-006) | Async | `POST /v1/connectors/{connectorId}/sync` | P; `Admin`, authorized workspace, completed provisioning | `202` | [DDS], pp. 27–29; p. 78, §22.1.1; p. 83 |
| <a id="api-019"></a>API-019 | Read connector sync runs and durable outcomes | [SCR-006-A01](01_screen_functions.md#scr-006) | Sync | `GET /v1/connectors/{connectorId}/runs` | P; connector-history read predicate unresolved | **Needs confirmation** | [DDS], pp. 27–29, Chapter 7 |
| <a id="api-020"></a>API-020 | Read registered model-deployment metadata | [SCR-007-A03](01_screen_functions.md#scr-007); selector remains proposed | Sync | `GET /v1/model-catalog` | P; catalog-read predicate unresolved; workspace deployment policy applies to selection | **Needs confirmation** | [DDS], pp. 37–39, Chapter 10 |
| <a id="api-021"></a>API-021 | Read immutable, redacted audit history | [SCR-008-A01/A02](01_screen_functions.md#scr-008) | Sync | `GET /v1/audit/events` | P; `Auditor`, tenant and redacted-content scope | `200` | [DDS], pp. 61–63; p. 83 |
| <a id="api-022"></a>API-022 | Read attributed costs, quotas, and trends | [SCR-010-A01](01_screen_functions.md#scr-010); screen binding remains proposed | Sync | `GET /v1/usage` | P; `Admin`, authorized reporting scope | `200` | [DDS], pp. 64–66; p. 83 |
| <a id="api-023"></a>API-023 | Start a frozen benchmark evaluation | [SCR-011-A01](01_screen_functions.md#scr-011); screen control remains proposed | Async | `POST /v1/evaluations` | P; `Admin` | `202` | [DDS], pp. 74–76; p. 83 |
| <a id="api-024"></a>API-024 | Read evaluation results and quality evidence | [SCR-011-A02/A03](01_screen_functions.md#scr-011) | Sync | `GET /v1/evaluations/{evaluationId}` | P; result-read predicate unresolved | **Needs confirmation** | [DDS], pp. 74–76 |
| <a id="api-025"></a>API-025 | Start controlled workspace export | `SCR-X-003`; no screen placement confirmed | Async | `POST /v1/workspaces/{workspaceId}/export` | P; `Admin + approver`; two independent approval checks | `202` | [DDS], pp. 78–80; p. 83 |
| <a id="api-026"></a>API-026 | Start legal-hold-safe workspace deletion | `SCR-X-004`; no screen placement confirmed | Async | `POST /v1/workspaces/{workspaceId}/delete` | P; `Admin + approver`; two independent approval checks | `202` | [DDS], pp. 78–80; p. 83 |
| <a id="api-027"></a>API-027 | Read authenticated principal context | `SCR-X-001`; all-screen identity dependency | Sync | `GET /v1/me` | P; authenticated principal; response visibility unresolved | **Needs confirmation** | [DDS], pp. 21–23 |
| <a id="api-028"></a>API-028 | Update workspace membership | `SCR-X-002`; no membership screen confirmed | Mutation; exact completion mode unresolved | `PUT /v1/workspaces/{workspaceId}/members` | P; membership-administration predicate unresolved | **Needs confirmation** | [DDS], pp. 21–23 |
| <a id="api-029"></a>API-029 | Create a security/legal hold | `SCR-X-005`; no screen placement confirmed | Mutation; exact completion mode unresolved | `POST /v1/security/holds` | P; hold-administration predicate unresolved | **Needs confirmation** | [DDS], pp. 61–63; hold exceptions pp. 26, 80 |
| <a id="api-030"></a>API-030 | Read declared degraded modes | `SCR-COM-009`, `SCR-COM-F06`, `SCR-003-F14`; exact screen binding unresolved | Sync | `GET /v1/system/degraded-modes` | P; read predicate unresolved | **Needs confirmation** | [DDS], pp. 68–70 |
| <a id="api-031"></a>API-031 | Supply the external OpenAPI contract | REST client generation and compatibility tooling; `SCR-X-009` | Sync | `GET /v1/openapi.json` | P; contract register requires OAuth audience; exact read policy unresolved | **Needs confirmation** | [DDS], pp. 54–56 |
| <a id="api-032"></a>API-032 | Record controlled design changes/decisions | `SCR-X-008`; no end-user screen confirmed | Mutation; exact completion mode unresolved | `POST /v1/design-decisions` | P; design-governance predicate unresolved | **Needs confirmation** | [DDS], pp. 8–10 |
| <a id="api-033"></a>API-033 | Read a design baseline | `SCR-X-008` | Sync | `GET /v1/design-baselines/{id}` | P; baseline-read predicate unresolved | **Needs confirmation** | [DDS], pp. 8–10 |
| <a id="api-034"></a>API-034 | Liveness surface | Deployment/monitoring integration; no screen binding confirmed | Sync | `GET /v1/health/live` | Contract register requires OAuth audience; probe identity and exposure policy unresolved | **Needs confirmation** | [DDS], pp. 18–20 |
| <a id="api-035"></a>API-035 | Readiness surface | Deployment/monitoring integration; no screen binding confirmed | Sync | `GET /v1/health/ready` | Contract register requires bounded schema; exact probe authentication/authorization unresolved | **Needs confirmation** | [DDS], pp. 18–20 |

**Needs confirmation — OQ-API-002:** Resolve `Workspace Admin` versus `Admin`, `Owner`, `Member`, `approver`, `operator`, and `elevated role`; define read/write/action predicates for every inventory row. The Auditor journey does not authorize general case reads, and Admin status does not establish case/evidence access.  
**Earlier questions:** `OQ-SCR-003`, `CON-SCR-007`–`CON-SCR-009`.  
**Sources:** [DDS], pp. 11, 22, 27, 46, 50, 83, 85, 90.

### Internal and External Interface Inventory

| API ID | Purpose / responsibility | Caller and screen relationship | Behavior | Method/path or protocol | Authentication / authorization | Success result and source |
|---|---|---|---|---|---|---|
| <a id="api-036"></a>API-036 | Scoped model generation, provider routing, validation, and usage accounting | Internal AI workflow; indirectly supports SCR-002/SCR-004/SCR-005 | Request/reply generation; exact deferred-result support unresolved | `POST /internal/model/generate` | S; approved deployment, workspace quota, maximum data class, scoped input | Status/schema **Needs confirmation**. [DDS], pp. 37–39 |
| <a id="api-037"></a>API-037 | Inspect durable workflow state | Internal workflow/operational clients; `SCR-X-009`, not a browser binding | Sync | `GET /internal/workflows/{runId}` | S; permitted workflow/tenant scope | **Needs confirmation**. [DDS], pp. 48–50 |
| <a id="api-038"></a>API-038 | Operator-controlled dead-letter replay | Authorized operational tooling; `SCR-X-006` | Bounded replay job; completion mode unresolved | `POST /internal/deadletters/{id}/replay` | S plus operator authorization, reason, dry-run validation, scope limit | **Needs confirmation**. [DDS], pp. 48–50; p. 90, §F.1 |
| <a id="api-039"></a>API-039 | Access stored document objects through a narrow service boundary | Authorized storage consumers; may support evidence viewing internally; no browser binding | Sync | `GET /internal/storage/documents/{id}` | S; tenant/workspace/document/version/object-role authorization | **Needs confirmation**. [DDS], pp. 51–53 |
| <a id="api-040"></a>API-040 | Execute eligible storage purge | Retention/deletion workflow; `SCR-X-004/X-005` indirectly | Durable purge; exact request/completion mode unresolved | `POST /internal/storage/purge` | S; retention eligibility, legal holds, inventory scope | **Needs confirmation**. [DDS], pp. 51–53 |
| <a id="api-041"></a>API-041 | Read operational metrics | Monitoring/operational clients; `SCR-X-009` | Sync | `GET /internal/metrics` | S; metrics-read policy unresolved | **Needs confirmation**. [DDS], pp. 64–66 |
| <a id="api-042"></a>API-042 | Read capacity/admission information | Capacity/operational clients; `SCR-X-009` | Sync | `GET /internal/capacity` | S; capacity-read policy unresolved | **Needs confirmation**. [DDS], pp. 68–70 |
| <a id="api-043"></a>API-043 | Record/start controlled release work | Release pipeline/authorized operational tooling; `SCR-X-009` | Mutation/rollout; exact response mode unresolved | `POST /internal/releases` | S; allowed build identity and release/sign-off gates | **Needs confirmation**. [DDS], pp. 71–73 |
| <a id="api-044"></a>API-044 | Read reconstructible release metadata | Release pipeline/authorized operational tooling; `SCR-X-009` | Sync | `GET /internal/releases/{releaseId}` | S; release-read predicate unresolved | **Needs confirmation**. [DDS], pp. 71–73 |
| <a id="api-045"></a>API-045 | Narrow read-only knowledge-search tool | Approved agents through approved MCP servers; not directly browser-callable | Typed tool invocation | `knowledge.search@v1`; HTTP method/path **Needs confirmation** | Scoped service credentials; `read:permitted_documents`, tenant-scoped | `{evidence_set_id: uuid, citations: Citation[]}`. [DDS], pp. 41–42; p. 87, §C.2 |
| <a id="api-046"></a>API-046 | Agent-to-agent task handoff | Approved sending and receiving agents | Task handoff; receiving agent may decline | A2A envelope; transport/method/path **Needs confirmation** | S/E; separate capability authorization, invoking principal, workspace policy, tool scope, classification | Result/decline envelope **Needs confirmation**. [DDS], p. 41, §11.2.2; p. 87 |
| <a id="api-047"></a>API-047 | Optional signed outbound notifications | Application notification producer → subscribed external recipients; `SCR-X-007` | Async delivery with retries | Outbound webhook; recipient URL/method **Needs confirmation** | Signed delivery; recipient verifies signature and event age | Acknowledgment/status/schema **Needs confirmation**. [DDS], p. 55, §15.2.2 |
| <a id="api-048"></a>API-048 | OIDC interactive authentication | Browser/BFF ↔ selected identity provider; `SCR-X-001` | Authorization-code flow with PKCE | Provider authorization/token/discovery endpoints **Needs confirmation** | Selected OIDC provider; token issuer/audience/expiry/subject/tenant validation | Provider contract **Needs confirmation**. [DDS], p. 21, §5.1; p. 90, §F.2 |
| <a id="api-049"></a>API-049 | Enterprise repository access | Connector workers ↔ configured repositories | Listing/fetch/delta/ACL/delete discovery and synchronization | Provider methods/URLs **Needs confirmation** | X; workspace-scoped secret references and provider grants | Provider schemas **Needs confirmation**. [DDS], pp. 27–29; p. 90 |
| <a id="api-050"></a>API-050 | External model-provider invocation | Model Gateway ↔ approved deployment | Provider generation dependency | Provider methods/URLs **Needs confirmation** | X; approved region/deployment and equal-or-stronger fallback data handling | Provider schemas **Needs confirmation**. [DDS], pp. 15, 19, 37–39; p. 90 |

**API-COM-003 — Boundary separation.** Internal endpoints, MCP tools, A2A capability discovery, operational metrics, and storage services must not be treated as browser APIs merely because a screen needs related information. The browser must not submit arbitrary tool definitions to the orchestrator. The orchestrator has no direct database credentials and uses narrow scoped APIs.  
**Sources:** [DDS], pp. 7, 9, 15–17, 40–42, 61–63, 87.  
**Screen trace:** `SCR-COM-012`, `SCR-X-006`–`SCR-X-009`.

### Required Capabilities Without a Confirmed API Contract

These are gaps, not approved new endpoints.

| Gap ID | Supported activity / affected operations | Missing interface | Status and source |
|---|---|---|---|
| API-GAP-001 | Classification correction; `SCR-002-A04` | Mutation contract for corrected labels, mandatory reason code, authorization, and revision behavior | **Needs confirmation.** [DDS], p. 12, §2.2.1 |
| API-GAP-002 | Policy Settings; `SCR-007-A01/A02` | Actual workspace-policy read/update APIs, activation, field-level rights, selectable registries | **Needs confirmation.** [DDS], p. 24, §6.1.1; p. 57 |
| API-GAP-003 | Evidence click-through; `SCR-003-A03`, `SCR-005-A03` | Browser-facing source/signed-URL contract and anchor/highlight representation | **Needs confirmation.** [DDS], pp. 31, 35, 52, 57 |
| API-GAP-004 | Review task opening; `SCR-005-A02` | Task-detail retrieval and the mutation/event trigger for `UserReviewOpened` | **Needs confirmation.** [DDS], pp. 45, 57–59 |
| API-GAP-005 | Closure/reopen/rework; `SCR-002-A10/A11` | Reopen contract and new-run-revision linkage | **Needs confirmation.** [DDS], pp. 25, 46 |
| API-GAP-006 | Publication/override; `SCR-002-A12`, `SCR-005-A07` | Whether a public publication action exists; override API and secondary-reviewer mechanics | **Needs confirmation.** [DDS], pp. 45–46 |
| API-GAP-007 | Connector administration; `SCR-006-A03` | Connector list/read/configure/authenticate/reauthenticate/revoke contracts | **Needs confirmation.** [DDS], pp. 27–29 |
| API-GAP-008 | Provisioning/holds; `SCR-X-002/X-005` | Provisioning entry/status API; membership reads; hold reads/releases | **Needs confirmation.** [DDS], pp. 21–23, 61–63, 78 |
| API-GAP-009 | Export/deletion; `SCR-X-003/X-004` | Approval routing, operation status, export download, receipt retrieval, partial/legal-hold outcomes | **Needs confirmation.** [DDS], pp. 78–80, 83 |
| API-GAP-010 | Overview and shared summary cards | Real summary APIs and aggregation contracts | **Needs confirmation.** Illustrated content does not define these APIs. [DDS], p. 7, Reference UI A; p. 57 |
| API-GAP-011 | Search backend, object storage, secret vault, and broker adapters | Exact provider-facing IDL, endpoints, authentication, and retry/status mapping | **Needs confirmation.** Logical components are confirmed; provider choices are open. [DDS], pp. 7, 16, 34–39, 48–53, 63, 90 |
| API-GAP-012 | Optional webhook administration | Subscription configuration, delivery-history, secret-rotation, and retry-remediation APIs | **Needs confirmation.** [DDS], p. 55, §15.2.2 |

### Explicit API Scope Exclusions

| Area | Treatment and reason |
|---|---|
| Physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing, administrative cloud permissions for agents | **Out of scope.** Explicit platform exclusions. [DDS], p. 9, §1.2.1. |
| Application-hosted GPU inference | **Out of scope for the R1 execution profile.** Model inference is an external dependency. [DDS], p. 19, §4.2.1. |
| Cross-region active/active mutation, OCR beyond English, customer-managed model weights | **Deferred from this baseline.** No R1 API contract is authorized for these deferred capabilities. [DDS], p. 10, §1.3.2. |
| Undescribed CRUD, polling, cancellation, retry, resume, download, or administration APIs | **Needs confirmation**, not out of scope. Endpoint names must not be invented as confirmed contracts. |

## Interfaces by API

### Shared Request, Response, and Serialization Rules

**API-COM-004 — Public contract governance.**

1. Public resource paths use `/v1` nouns.
2. Public timestamps use RFC 3339; durable timestamps are UTC.
3. Public collections use cursor pagination where pagination is provided.
4. Repository-controlled IDL generates OpenAPI and protobuf definitions.
5. The external OpenAPI contract governs REST clients; protobuf IDL governs internal gRPC messages.
6. CI prevents breaking field deletion and incompatible enum changes.
7. Nonbreaking changes are additive. Field removal requires a scheduled migration; no schedule is supplied.
8. Public responses must not expose secrets or raw provider credentials.

**Sources:** [DDS], pp. 15–17, §3.1.2; pp. 54–56, Chapter 15; p. 82, Appendix A.

**Needs confirmation — OQ-API-003:** Supply the actual repository-controlled schemas. Public property names, JSON numeric representation, lengths, formats, nullability, mandatory properties, request media types, and complete response envelopes are not established by the selected database fields.  
**Earlier questions:** `OQ-SCR-004`, `OQ-SCR-011`.

#### Shared Parameter Definitions

These definitions apply when an endpoint references them. `Required in context` does not mean the client is permitted to supply or override trusted context.

| Parameter / datum | Location | Meaning and type | Required status | Constraints / default | Evidence and open question |
|---|---|---|---|---|---|
| `caseId` | Path | Case identifier; domain identifiers use UUIDv7 | Required for paths containing it | Authorized tenant/workspace case; no default. Exact accepted textual representation and UUID-version rejection policy unresolved. | [DDS], p. 51, §14.1.1; p. 83. OQ-API-003 |
| `runId` | Path | Run identifier; UUIDv7 domain baseline | Required in applicable paths | Authorized run/case association; no default | [DDS], pp. 51, 85 |
| `documentId` | Path | Document identifier; UUIDv7 domain baseline | Required | Current document/status authorization; no default | [DDS], pp. 30–32, 51 |
| `evidenceId` | Path | Evidence-resource identifier | Required | Identity and relation to evidence-set/chunk/citation IDs **Needs confirmation**; no default | [DDS], pp. 34–36. OQ-API-010 |
| `approvalId` | Path | Approval resource used for decision capture | Required | Mapping to task ID versus decision/assignment ID unresolved; no default | [DDS], pp. 44–46, 83, 85. OQ-API-015 |
| `connectorId` | Path | Workspace connector identifier | Required | Authorized connector scope; no default | [DDS], pp. 27–29, 51 |
| `workspaceId` | Path | Workspace identifier; UUIDv7 domain baseline | Required | Workspace belongs to authenticated tenant; no default | [DDS], pp. 21–24, 51, 86 |
| `evaluationId` | Path | Evaluation identifier; UUIDv7 domain baseline | Required | Evaluation read predicate unresolved; no default | [DDS], pp. 51, 74–76 |
| `releaseId` | Path | Internal release identifier | Required | Accepted encoding and release-access scope unresolved; no default | [DDS], pp. 71–73 |
| `id` | Path | Resource identifier for baseline, dead letter, or stored document, depending on endpoint | Required | Endpoint-specific resource mapping and accepted encoding unresolved; no default | [DDS], pp. 8–10, 48–53 |
| `cursor` | Query | Continuation for `GET /v1/cases?cursor=...` | Cursor presence confirmed; initial-request omission/empty semantics unresolved | Type/encoding/lifetime/default unresolved; no offset contract | [DDS], pp. 54, 57–59. OQ-API-006 |
| `Idempotency-Key` | Header | Client operation identity for replay-safe mutation | Required for API-001 and POST mutations creating long-running jobs | Identical fingerprint returns original outcome; changed fingerprint conflicts. Format, length, scope, and non-case TTL unresolved. | [DDS], pp. 25, 54, 83, 89. OQ-API-004 |
| `If-Match` | Header | Case revision precondition | Required for API-004; case-domain revision conditions also apply to affected case mutations, but close transport details need confirmation | Must match current revision. Exact ETag/revision encoding, wildcard support, and missing-header outcome unresolved. No default. | [DDS], pp. 25, 83. OQ-API-005 |
| `Last-Event-ID` | Header | Resume position for run SSE | Used on reconnect to resume retained events; first-connection behavior unresolved | Scoped retained backfill; offset encoding/type/expiry unresolved; no invented default | [DDS], p. 55, §15.2.1; p. 83. OQ-API-014 |
| `Retry-After` | Response header / provider response header | Throttling retry instruction | Required in throttled new-run response; connector workers honor provider value | No fixed interval supplied; supported date/delay syntax and propagation unresolved | [DDS], pp. 28, 69. OQ-API-032 |
| Access token | Authentication context; HTTP carrier unresolved | Authenticated issuer, audience, expiry, subject, and tenant | Required for application requests | Reject unexpected algorithms and missing tenancy claims. No client-supplied tenant override. | [DDS], p. 21. OQ-API-001 |
| `tenant_id` | Trusted request/job/storage context; exact public transport unresolved | Mandatory tenant security attribute; UUID in relational case DDL | Required at tenant-owned boundaries | Authenticated and immutable in background jobs; every storage predicate includes tenant | [DDS], pp. 22, 48, 51, 86 |
| `actor_id` | Trusted durable-operation context | Authenticated actor attribution | Required where durable state changes | Cannot be established solely by untrusted body content; exact propagation unresolved | [DDS], repeated interface-boundary requirements, pp. 8–80 |
| `revision` | Durable-operation context | Resource revision | Required where source boundary records change durable state | Monotonic case revision; type/transport varies by resource and needs confirmation | [DDS], pp. 24–25, 86 |
| `occurred_at` | Durable-operation/event context | Time of durable action | Required at applicable state-changing boundaries | UTC; public representation RFC 3339; server/client authority details unresolved | [DDS], pp. 48, 54, 59 |
| `trace_id`, `correlation_id` | Request and downstream diagnostic context; header names unresolved | Correlated request/stage identifiers | Every request carries both; exact transport requiredness unresolved | Correlation remains independent of provider trace IDs; no document content or secrets | [DDS], pp. 16, 64 |
| `Content-Type` | Header | Body representation | Explicit `application/json` confirmed for canonical error example; other endpoint media types unresolved | Upload encoding is not specified. Do not assume every request is JSON. | [DDS], p. 84; upload contract pp. 30–32 |

**Proposal — P-API-001:** Use `Authorization: Bearer <access-token>` for direct token-based REST clients. This is a proposed HTTP carrier for the confirmed access-token requirement; the source does not select it over the optional BFF cookie approach. Cookie names, CSRF controls, and SSE authentication must be resolved under OQ-API-001.

#### Pagination Contract

| Aspect | Confirmed requirement | Needs confirmation |
|---|---|---|
| Case list | Source shows `GET /v1/cases?cursor=...` | Initial cursor behavior, cursor response-property name/type, page size, ordering, filters, consistency during concurrent changes |
| Audit list | Explicitly cursor-paginated immutable log | Query parameter names, response envelope, cursor encoding/lifetime, ordering, maximum page size |
| Other public collections | General public cursor-pagination convention | Whether and how search results, evidence, review tasks, connector runs, model catalog, steps, and evaluation details paginate |
| Internal collections | No complete pagination contract supplied | All pagination/query contracts |
| Empty and final page | No exact response example | Empty collection versus missing collection, continuation absence versus null, total-count availability |
| Invalid/expired cursor | No error mapping supplied | HTTP status, business code, safe details, recovery procedure |

**Needs confirmation — OQ-API-006:** Complete pagination contracts without deriving page sizes from retrieval budgets, illustrated row counts, or maximum corpus sizes.  
**Sources:** [DDS], pp. 54, 57–59, 83.  
**Earlier questions:** `OQ-SCR-011`, `OQ-SCR-013`, `OQ-SCR-019`, `OQ-SCR-021`.

### API-001–API-005 — Case Interfaces

#### Per-Operation Parameters and Results

| API | Path/query | Headers | Body | Successful response and required content | Default / unresolved contract |
|---|---|---|---|---|---|
| API-001 | No path parameter. Workspace-binding transport unresolved. Other query parameters not specified. | Required `Idempotency-Key`; authentication and trace context | Business context is confirmed; exact submitted fields, names, types, and requiredness unresolved | `201`; a case identifier is required as an outcome. Public property name and response envelope unresolved. Creation starts `NEW`. | Case database revision defaults to `1`; sensitivity defaults to `INTERNAL`. These do not establish form requiredness or complete POST defaulting semantics. |
| API-002 | `cursor` as above; filters/sorts/workspace selection unresolved | Authentication and trace context | No body described; absence as a formal contract needs confirmation | Authorized case list; HTTP success status, collection property, required item properties, and continuation field unresolved | No page-size/order/filter defaults supplied |
| API-003 | Required `caseId`; no query contract supplied | Authentication and trace context; response revision/ETag transport unresolved | No body described | `200`; authorized current case revision. Exact projection/mandatory fields unresolved. | No automatic inclusion of all attachments/runs/approval details is confirmed |
| API-004 | Required `caseId`; query contract unresolved | Required `If-Match`; authentication/trace context | Authorized case changes; editable field set and patch format unresolved | `200`; accepted mutation. Response body/current revision property unresolved. `409 CASE_VERSION_CONFLICT` includes current revision. | JSON Patch, JSON Merge Patch, and custom partial-object patch are not selected |
| API-005 | Required `caseId`; query contract unresolved | Revision condition required by case-domain contract; exact close encoding and idempotency header requirement unresolved | Closure request body/required fields unresolved | Accepted closure snapshots approved answer, cited versions, reviewer decisions; status/body/completion mode unresolved | Closure predecessor states, repeat-close behavior, and reopen contract unresolved |

**Sources:** [DDS], pp. 11–13, 24–26, 57–59, 83–86.

#### Case Data and Input Constraints

The names below are source domain/database terminology. Unless stated otherwise, public JSON naming and presence are **Needs confirmation**.

| Field ID | Name / meaning | Applicable interface content | Type | Required / default | Constraints and source |
|---|---|---|---|---|---|
| API-CASE-F01 | `id` — canonical case identity | Create outcome/current case/list reference | Database `UUID`; UUIDv7 identifier baseline | Required identity in stored case and create outcome; server generated | Tenant-scoped identity. Public business-number relationship unresolved. [DDS], pp. 51, 83, 86 |
| API-CASE-F02 | `tenant_id` | Trusted case storage/context | `UUID NOT NULL` in DDL | Required; authenticated scope, not an editable tenant selection | RLS and domain guard. [DDS], pp. 22, 51, 86 |
| API-CASE-F03 | `workspace_id` | Case relationship and intake context | `UUID NOT NULL` in DDL | Required stored relationship; POST carrier unresolved | Must enforce workspace-tenancy membership. [DDS], pp. 24, 86 |
| API-CASE-F04 | Title | Case domain/intake/edit | Exact wire/data type and length unresolved | Stored datum confirmed; POST/PATCH requiredness/default unresolved | Editable field contract and characters unresolved. [DDS], p. 24, §6.1.2 |
| API-CASE-F05 | Description | Case domain/business context | Exact type, length, markup format unresolved | Requiredness/default unresolved | Validate user input; no rich-text contract supplied. [DDS], pp. 12, 24 |
| API-CASE-F06 | Impact | Priority input | Type/vocabulary/range unresolved | Explicit business input; POST/PATCH requiredness unresolved | Priority cannot derive from model output alone. [DDS], p. 25, §6.3.1 |
| API-CASE-F07 | Urgency | Priority input | Type/vocabulary/range unresolved | Requiredness/default unresolved | Deterministic combination with impact; formula absent. [DDS], p. 25 |
| API-CASE-F08 | Priority | Derived case datum | Type/enumeration unresolved | Stored datum confirmed; direct client editing not confirmed | Derived from explicit impact/urgency. [DDS], pp. 24–25 |
| API-CASE-F09 | `sensitivity` / sensitivity label | Stored case/policy input | DDL `TEXT NOT NULL`; information classes `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` | Database default `INTERNAL`; request-requiredness/editability unresolved | Maximum material class in a run governs routing/redaction/retention/approval. [DDS], pp. 62, 86 |
| API-CASE-F10 | `status` | Current case/list/transition result | DDL `TEXT NOT NULL`; case vocabulary below | New case begins `NEW`; direct status-field mutation contract unresolved | Guarded transitions only. [DDS], pp. 12, 25, 82, 86 |
| API-CASE-F11 | Owner | Case relationship / API-004 predicate | Identifier/relationship type unresolved | Assignment/default/reassignment contract unresolved | `Owner` is not a defined baseline role. [DDS], pp. 24, 83 |
| API-CASE-F12 | `revision` | Current case/concurrency | DDL `BIGINT NOT NULL` | Database default `1`; monotonic | Wire integer versus string/ETag representation unresolved. [DDS], pp. 25, 86 |
| API-CASE-F13 | Current approved result | Current case/final response pointer | Artifact/reference structure unresolved | Nullability before publication unresolved | Updated only through satisfied publication gate; closed lineage immutable. [DDS], pp. 24, 45–46 |
| API-CASE-F14 | `created_at` | Stored creation time | `TIMESTAMPTZ NOT NULL DEFAULT now()` | Server-generated stored value | Public timestamp RFC 3339/UTC. [DDS], pp. 54, 86 |
| API-CASE-F15 | `updated_at` | Stored update time | `TIMESTAMPTZ NOT NULL DEFAULT now()` | Initial database default confirmed; update-maintenance mechanism unresolved | No update trigger is supplied by the DDL. [DDS], p. 86 |
| API-CASE-F16 | Classification labels, confidences, provenance | Async case classification result | Collection/numeric/provenance schemas unresolved | Result data confirmed; wire presence and defaults unresolved | Classification is policy-aware and asynchronous. [DDS], p. 12 |
| API-CASE-F17 | Label-correction reason code | API-GAP-001 | Type/length/vocabulary unresolved | Required when correcting a label | Correction permission, payload, endpoint, and revision behavior unresolved. [DDS], p. 12 |
| API-CASE-F18 | SLA deadline | Derived business-calendar result | Exact schema unresolved; timestamp convention applies if exposed as a timestamp | Derivation/default unresolved | Workspace timezone/business calendar; advisory breach prediction cannot alter contractual deadline. [DDS], p. 25 |

#### Confirmed Case States and Guards

| Current state | Confirmed next states / exception | API consequence |
|---|---|---|
| `NEW` | `TRIAGED` | Reject unsupported transitions |
| `TRIAGED` | `IN_PROGRESS` | Apply role/revision/domain guards |
| `IN_PROGRESS` | `PENDING_APPROVAL`, `RESOLVED` | Approval requirements apply to applicable resolution/publication |
| `PENDING_APPROVAL` | `RESOLVED`, `IN_PROGRESS` | Preserve review and rework lineage |
| `RESOLVED` | Closure operation exists, but explicit `RESOLVED -> CLOSED` transition is not enumerated | **Needs confirmation**; do not infer complete close guards |
| `CLOSED` | Final unless explicitly reopened as a new revision | Do not overwrite closed approved-output lineage |

**Sources:** [DDS], p. 25, §6.2.1; p. 82, §A.1.

**Open questions beside these interfaces:**

- **OQ-API-007:** Complete case create/read/list/update field schemas; ownership assignment; impact/urgency/priority/SLA rules; case state and business-number mapping. Earlier: `OQ-SCR-004`–`OQ-SCR-008`.
- **OQ-API-005:** Define revision encoding, missing precondition behavior, response revision/ETag, patch format, and conflict recovery.
- **OQ-API-008:** Define classification correction and async classification failure/result delivery. Earlier: `OQ-SCR-007`.
- **OQ-API-007:** Define closure roles, predecessor states, body/status, repeated closure, reopen API, and new-revision semantics. Earlier: `OQ-SCR-018`.
- No case-delete or attachment-removal endpoint is confirmed.

### API-006–API-010 — Ingestion, Search, and Evidence Interfaces

#### Per-Operation Parameters and Results

| API | Path/query | Headers | Body | Response contract | Defaults / unresolved details |
|---|---|---|---|---|---|
| API-006 | Required `caseId`; other query parameters unresolved | Required long-running-job `Idempotency-Key`; authentication/trace; upload media type unresolved | File content/metadata transport unresolved; OCR opt-in carrier unresolved | `202`; persisted ingestion operation. Operation/document/version identifier property names, types, and required response mapping unresolved. | Configurable 25 MB per-file cap. Multipart versus signed upload, file-part name, number of files/request, and size-boundary units unresolved. |
| API-007 | Required `documentId`; query unresolved | Authentication/trace | No body described | Authoritative document state; exact status-property name, HTTP status, quality/provenance/error fields unresolved | No polling interval or document SSE contract supplied |
| API-008 | Required `caseId`; query/pagination unresolved | Authentication/trace | No body described | Permitted case evidence and citation context; HTTP status/envelope/required properties unresolved | Evidence-set selection/current versus historic run behavior unresolved |
| API-009 | No path parameter; scope/query/pagination carrier unresolved | Authentication/trace; idempotency-key requirement for read-like search is not established by the long-running POST rule | Search query and authorized scope concepts confirmed; public wire names/types/requiredness/filters unresolved | `200` for supported ACL-filtered lexical+semantic evidence; each evidence item has the source-confirmed content below | Empty-query behavior, query limits, result envelope, scores, cursor behavior, and `NO_SUPPORTED_EVIDENCE` HTTP representation unresolved |
| API-010 | Required `evidenceId`; query unresolved | Authentication/trace | No body described | Authorized evidence resource; HTTP status and resource shape unresolved | Not sufficient to establish a source binary/download URL response |

**Sources:** [DDS], pp. 30–36; pp. 57–59; p. 83.

#### Upload and Normalization Constraints

| Field / datum | Meaning and type | Required / default | Confirmed constraints | Open contract |
|---|---|---|---|---|
| File content; wire name unresolved | Uploaded bytes | Necessary for an upload; request field/part requiredness unresolved | R1 allows PDF, DOCX, HTML, UTF-8 text | Exact MIME/extension allowlist, encoding, request transport |
| MIME and extension metadata; names unresolved | Type-detection inputs | Accepted files must have agreeing signature and extension | Authoritative type detection; scan before parsing | Metadata trust rules and exact rejection mapping |
| Per-file size | Byte count; wire exposure unresolved | Configurable cap described as 25 MB | Oversized input fails closed | Decimal/binary MB, inclusive boundary, maximum request/aggregate size |
| Decompression threshold | Resource-safety control | Threshold required; value absent | Prevent decompression bombs; bounded parser/sandbox controls | Threshold value/unit and response code |
| OCR opt-in | Pipeline option; type/carrier unresolved | Opt-in confirmed; default not explicitly specified | Provenance-marked fallback; beyond-English OCR deferred | Opt-in scope, transport, allowed configuration |
| Parser/pipeline version | Immutable normalization identity | Stored versioning required | Fingerprint plus pipeline version produces immutable derivative IDs; reprocess side by side | Public field name/type/visibility |
| Quality flags | Empty-page ratio, unknown-character ratio, table-loss indicators, language confidence | Output data confirmed; presence/nullable behavior unresolved | Low-quality documents remain viewable when authorized, but cannot support autonomous recommendations | Numeric types, thresholds, flag names, autonomous-use eligibility representation |

**Sources:** [DDS], pp. 10, 30–32; p. 88, `T-04`; p. 90, storage example.

**API-COM-005 — Unsafe versus low-quality material.** Unsafe attachments are quarantined without indexing. The permission to view low-quality documents does not establish permission or a safe rendering contract for quarantined active content. Macros must not execute, and embedded remote references must not be fetched.  
**Sources:** [DDS], pp. 30–32, §§8.1.2 and 8.3.2.  
**Screen trace:** `SCR-002-A05`, `SCR-003`, `OQ-SCR-009`.

#### Document State Vocabulary

| Datum | Confirmed values | Guards / unresolved transitions |
|---|---|---|
| Document state | `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED` | Virus-scan and quality gates apply. Complete transition graph, retry-state representation, and whether low-quality indexed material can be `READY` require confirmation. |
| Public state property | **Needs confirmation** | Do not assume the field is named `status` merely from the endpoint suffix. |

**Source:** [DDS], p. 82, §A.1.

#### Evidence and Citation Content

Content presence is confirmed where the source says every item/chunk includes it. Wire names and exact types are not supplied except in the separate MCP tool contract.

| Field ID | Content / source terminology | Type | Required status | Constraints / default | Source |
|---|---|---|---|---|---|
| API-EVID-F01 | Chunk ID; index term `chunk_id` | Identifier; precise public encoding unresolved | Every response evidence item includes it | Cited chunk must resolve; no default | [DDS], pp. 34–35 |
| API-EVID-F02 | Source title | Type/length unresolved | Included in each response evidence item | Authorized metadata only | [DDS], p. 35, §9.3.1 |
| API-EVID-F03 | Document revision/version | Revision/reference type unresolved | Included in each response evidence item | Cite immutable stored version, not silently substituted latest content | [DDS], pp. 31, 35 |
| API-EVID-F04 | Page anchor | Structure/numbering unresolved | Included in each response evidence item | Resolvable stored anchor; click-through highlights anchored page range | [DDS], pp. 31, 35, 57 |
| API-EVID-F05 | ACL digest; stored `acl_digest` | Encoding/type unresolved | Included in each response evidence item | Digest is validation metadata, not authorization authority; current permission remains required | [DDS], pp. 35, 85 |
| API-EVID-F06 | Source URI | URI type/scheme restrictions unresolved | Every stored chunk has source URI | Does not authorize arbitrary browsing/network access | [DDS], pp. 31, 87 |
| API-EVID-F07 | File/source hash | Hash encoding unresolved | Every stored chunk has file hash | Immutable provenance | [DDS], pp. 31, 85 |
| API-EVID-F08 | Page number | Numeric/identifier representation unresolved | Every stored chunk has page number | Page index/number basis unresolved | [DDS], p. 31 |
| API-EVID-F09 | Bounding box; stored `bbox` | Structure/coordinates/unit unresolved | Optional source anchor metadata | Bound to correct source page | [DDS], pp. 31, 85 |
| API-EVID-F10 | Citation identifier | Opaque identifier | Used citations must be verified before display | User-facing identifiers remain opaque; relation to `evidenceId` unresolved | [DDS], p. 35 |
| API-EVID-F11 | Quality/OCR provenance | Structured flags/metadata unresolved | Source data required where extraction produces it; response projection unresolved | Exclude low-quality evidence from autonomous recommendations | [DDS], pp. 31–32 |
| API-EVID-F12 | Reduced-quality retrieval flag | Wire name/type unresolved | Visible when permitted lexical-only degraded retrieval continues | Do not conceal vector degradation or bypass ACLs | [DDS], p. 69, §19.2.2 |
| API-EVID-F13 | Evidence-set ID; stored `evidence_sets.id` | UUIDv7 domain baseline; MCP output `uuid` | Exact public response presence unresolved; required in MCP output contract content | Separate from opaque citation/evidence IDs until mapping resolves | [DDS], pp. 85, 87 |

The internal search row also stores `tenant_id`, `workspace_id`, `document_version_id`, language, classification, normalized text, and a **1536-dimensional embedding**. That index schema does not authorize returning raw embeddings or all index fields publicly.  
**Source:** [DDS], p. 34, §9.1.1.

**Open questions:**

- **OQ-API-009:** Upload encoding/allowlist/size units/decompression thresholds, OCR, document transitions, quality thresholds, result fields, and quarantine-safe access. Earlier: `OQ-SCR-009`.
- **OQ-API-010:** Evidence ID relationships, source/signed-URL API, TTL, authorization after URL issuance, page/bounding-box schema, non-PDF anchors, highlights, and invalid/stale-anchor response. Earlier: `OQ-SCR-010`.
- **OQ-API-011:** Public search schema, query requiredness/length, scope/filter fields, result selection/order/scores/pagination, insufficient-evidence status, and clarification/human-route contract. Earlier: `OQ-SCR-011`.
- Do not copy `knowledge.search@v1` parameter names or limits into API-009 as confirmed public fields.

### API-011–API-015 — Run Creation, State, Steps, and SSE

#### Per-Operation Parameters and Results

| API | Path/query | Headers | Body | Successful response | Unresolved details |
|---|---|---|---|---|---|
| API-011 | Required `caseId`; query contract absent | Required `Idempotency-Key`; authentication/trace | Validated analyst business input; exact fields, lengths, and case-revision binding unresolved | `202`; run created immediately and persisted. Identifier property/envelope/type mapping unresolved. | Prompt/model/tool selection is not a confirmed client control |
| API-012 | Case-binding carrier unresolved | Required job idempotency; authentication/trace | Entire body schema unresolved | Workflow request exists; exact success status/body unresolved | Canonical versus alternate endpoint semantics must resolve |
| API-013 | Required `runId`; query absent | Authentication/trace | No body described | `200`; stages and evidence metadata; authoritative refresh reconstruction | Candidate/model/prompt/policy projection and mandatory fields unresolved |
| API-014 | Required `runId`; query/pagination/order unresolved | Authentication/trace | No body described | Execution steps/checkpoints; HTTP success status/envelope unresolved | Step kinds, statuses, dependencies, and checkpoint payload types unresolved |
| API-015 | Required `runId`; query absent | `Last-Event-ID` for reconnect; authentication/trace | No body described | `200` SSE; monotonically increasing offsets and retained scoped backfill | Event names/data schema/media-type declaration, retention, initial replay, heartbeat, expiry/gap/end/error behavior unresolved |

**Sources:** [DDS], pp. 12–17, 40–42, 49, 54–58, 83.

#### Run and Step Data

| Field / source name | Meaning / applicability | Type | Required / default | Constraints and source |
|---|---|---|---|---|
| `runs.id` | Run identity | UUIDv7 domain baseline | Required stored identity; create-response property unresolved | Authorized case association. [DDS], pp. 51, 85 |
| `case_id` | Associated case | Domain UUID reference | Stored association confirmed; public requiredness unresolved | Immutable identifier relationship. [DDS], pp. 24, 85 |
| `status` | Current run state | Wire type unresolved; vocabulary below | Authoritative run state required for visible progress | Do not reconstruct status solely in browser. [DDS], pp. 49, 58, 82 |
| `plan_revision` | Stored plan version | Type unresolved | Must be stored before side effects | No client-editable plan revision established. [DDS], pp. 40, 85 |
| Plan dependencies/DAG | Bounded execution structure | Schema unresolved | Explicit dependencies required in plan | Depth maximum eight; tool invocations maximum sixteen. [DDS], p. 40 |
| `budget` | Runtime/token/call controls | Object/unit schema unresolved | Bounded runtime and token budget required | Workspace quota; exact allocation schema unresolved. [DDS], pp. 38, 40, 85 |
| `run_steps.id`, `run_id` | Step identity/run association | Domain identifiers | Stored identity/association confirmed | Idempotent steps. [DDS], p. 85 |
| `step_kind`, step `status` | Step classification/outcome | Types/enumerations unresolved | Stored data confirmed; public projection unresolved | Do not invent agent/tool step enum. [DDS], p. 85 |
| `checkpoint` | Durable stage/step continuation | Schema unresolved | Persist before downstream dispatch | Replay-safe continuation. [DDS], pp. 40, 49, 85 |
| Failed checkpoint/cause | Human-visible execution failure | Wire name/type unresolved | Exactly failed checkpoint must be reported | Safe cause, no secrets/document text. [DDS], p. 41 |
| Evidence metadata | Supporting evidence set/citations | See evidence-content catalog | API-013 returns it; complete requiredness unresolved | Current permissions/publication validation. [DDS], pp. 35, 83 |
| Model/prompt version and policy reasons | Exact review context | Schemas unresolved | Reviewer must receive actual candidate context through resolved read contracts | Actual used versions; not arbitrary client choices. [DDS], p. 58 |
| SSE offset | Stream continuation order | Encoding/type unresolved | Monotonic offset required | Independent of event UUID and provider trace identity unless mapping is explicitly defined. [DDS], pp. 16, 55 |
| Event occurrence time | Durable transition time | UTC; RFC 3339 when public | Event envelope requires `occurred_at` | Locale cannot alter durable order. [DDS], pp. 48, 59 |

#### State Vocabulary and Resume Procedure

Run states are:

`REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED`.

**Sources:** [DDS], p. 49, §13.2.1; p. 82, §A.1.

1. API-011 creates durable run state after validation, authorization, and admission.
2. API-013 supplies authoritative current state for initial load or browser refresh.
3. API-014 supplies execution steps where needed.
4. API-015 streams scoped state updates with monotonically increasing offsets.
5. Reconnection uses `Last-Event-ID` to backfill retained events within caller scope.
6. A disconnect is not a successful terminal outcome.
7. Publication is visible only after the publication gate accepts the exact artifact.

**Sources:** [DDS], pp. 45–46, 55, 58, 83.

**Open questions:**

- **OQ-API-012:** Resolve API-011 versus API-012, alternate case-binding semantics, run-revision/rework linkage, and whether any cancel/retry/resume mutation exists. Earlier: `OQ-SCR-012`, `CON-SCR-004`.
- **OQ-API-013:** Resolve missing-approval termination versus `AWAITING_REVIEW`, run-timeout accounting, review waiting, recoverable timeout representation, and runtime/dependency timeouts. The source example `run_timeout_seconds: 180` is not a selected HTTP timeout or reviewer SLA. Earlier: `CON-SCR-005`, `OQ-SCR-012/OQ-SCR-015`.
- **OQ-API-014:** Define SSE payload schemas, offset/cursor types, retention/gaps, reauthorization during streams, token expiry, duplicates/out-of-order handling, stream termination, and steps pagination/order. Earlier: `OQ-SCR-013`.

### API-016–API-017 — Review and Decision Interfaces

#### Parameters and Response Content

| Parameter / content | API / location | Meaning and type | Required / default | Constraints / source |
|---|---|---|---|---|
| Review-queue selection | API-016 query | Pool/assignment/workspace/filter/cursor concepts; names/types absent | Requiredness/defaults unresolved | Only policy-authorized work; no visibility to all tasks inferred. [DDS], p. 45 |
| `approvalId` | API-017 path | Decision-target approval/task resource | Required; no default | Exact resource mapping unresolved. [DDS], pp. 45, 83, 85 |
| Decision | API-017 body; exact wire name unresolved | Approve/reject decision | Decision capture confirmed; wire enum and body requiredness unresolved | `APPROVED`/`REJECTED` are review states, not a confirmed request enum. [DDS], pp. 45, 58, 82 |
| Evaluated artifact hash | API-017 binding; carrier unresolved | Exact reviewed-content hash | Binding mandatory; wire type/encoding/carrier unresolved | Changed artifact is stale; no old approval applied to different content. [DDS], pp. 44–46 |
| Rationale; stored decision `reason` | API-017 record/input | Reviewer explanation | Record includes rationale; nonblank requirement, length, and request name unresolved | Required review fields must be complete; exact field set absent. [DDS], pp. 45, 58, 85 |
| Annotations | API-017 optional record/input | Additional review notes | Optional | Format/count/length/redaction unresolved. [DDS], p. 45 |
| Actor / reviewer ID | Server-authenticated context/record | Decision author | Required in approval record; not an untrusted reviewer override | Role, assignment, and separation of duties checked. [DDS], pp. 22, 45 |
| Timestamp | Decision record | Recorded decision time | Required record datum; server transport details unresolved | UTC/RFC 3339 if public. [DDS], pp. 45, 54, 59 |
| Idempotency | API-017 mutation | Replay-safe cross-service write | Idempotent outcome required; exact public key requirement/transport unresolved | Contract register identifies idempotency policy; no decision-specific TTL supplied. [DDS], pp. 15, 46, 52 |
| Review task context | API-016 or API-GAP-004 response | Task/run/case/pool/state/expiry | Exact response projection/types/requiredness unresolved | Reviewer sees exact candidate, citations, model/prompt versions, policy reasons before approval. [DDS], pp. 45, 58, 85 |
| Accepted decision result | API-017 response | Accepted immutable decision | HTTP `200` confirmed; body fields/types unresolved | Does not by itself mean published. [DDS], pp. 45–46, 83 |

Review states are `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED`.  
Policy outcomes are `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY`.  
These vocabularies are separate from case/run/artifact states.  
**Sources:** [DDS], pp. 44, 57, 82.

#### Decision Procedure

1. Read authorized review work.
2. Obtain the exact candidate, evidence, actual model/prompt versions, and stored policy reasons.
3. Make source evidence inspectable before approval.
4. Submit a decision with exact artifact binding and the resolved required review fields.
5. Re-evaluate principal, task validity/expiry, reviewer policy, separation of duties, and content hash.
6. Store decision, actor, timestamp, evaluated artifact hash, rationale, and optional annotations.
7. Insert required outbox evidence in the transaction.
8. Validate publication separately as required by the gate; update the final response pointer only in the transaction recording a satisfied gate.
9. Reject changed-artifact decisions as stale and audit the rejection.

**Sources:** [DDS], pp. 22, 44–46, 52, 58.

**Open questions:**

- **OQ-API-015:** Task-detail endpoint, `approvalId` mapping, decision enum/body, artifact-hash encoding/carrier, mandatory fields, rationale/annotations, response body, duplicate/conflicting decisions. Earlier: `OQ-SCR-014`.
- **OQ-API-016:** Reviewer pool/role/SLA/routing, late decisions, reassignment/escalation, multi-reviewer rules, and broad self-approval scope. High-risk self-approval is explicitly prohibited; no bypass is authorized by this gap. Earlier: `OQ-SCR-003/OQ-SCR-015`.
- **OQ-API-017:** Publication status/read projection, automatic-allow path, and whether any public publication control/API exists. Earlier: `OQ-SCR-016`.
- **OQ-API-018:** Override role, secondary reviewer, reason schema, and endpoint. Earlier: `OQ-SCR-017`.
- **OQ-API-035:** Define `UserReviewOpened` trigger/schema without making queue/case/evidence GETs mutate review state by inference. Earlier: `OQ-SCR-021`, `CON-SCR-011`.

### API-018–API-020 and API-GAP-002/API-GAP-007 — Connector and Policy Interfaces

#### Per-Operation Interface

| API | Path/query/header/body | Successful content | Types / requiredness / defaults | Source |
|---|---|---|---|---|
| API-018 | Required `connectorId`; required job `Idempotency-Key`; sync-body options and query fields unresolved | `202`; durable incremental sync operation | Operation ID property/schema, capability-warning transport, and accepted initial state unresolved | [DDS], pp. 27–29, 83 |
| API-019 | Required `connectorId`; cursor/filter/order fields unresolved; no body described | Sync run history/outcomes | HTTP status, collection envelope, item fields, requiredness, nullability, and pagination unresolved | [DDS], pp. 28–29 |
| API-020 | Catalog query/filter/workspace carrier unresolved; no body described | Registered deployment metadata | HTTP status, collection/cursor, property names, types, requiredness unresolved | [DDS], pp. 37–39 |
| API-GAP-002 | Method/path absent; workspace context and revision precondition required for configuration changes | Current/accepted versioned policy and durable audit | Entire read/update wire schema and activation contract unresolved | [DDS], p. 24, §6.1.1 |
| API-GAP-007 | Methods/paths absent | Connector configuration and credential-management outcomes | Entire contract unresolved; raw stored tokens must not leak | [DDS], pp. 27–29 |

#### Connector and Policy Data

| Source datum | Meaning | Type / required status / default | Confirmed constraint | Source |
|---|---|---|---|---|
| Connector capabilities | List, fetch, delta cursor, ACL, delete support | Wire schema/types unresolved; capability advertisement required | Unsupported capabilities cause lower-trust ingestion and explicit warning | [DDS], p. 27 |
| Credential reference | Workspace-scoped secret-store reference | Schema unresolved; raw credential public field forbidden | Revocation causes queued jobs to fail `CONNECTOR_REAUTH_REQUIRED` | [DDS], p. 27 |
| Sync cursor | Provider checkpoint | Provider-specific type/default unresolved; stored per run | Advance only after all preceding durable ingestion outcomes | [DDS], p. 28 |
| High-watermark / stored `watermark` | Sync progress boundary | Type/default unresolved; stored datum confirmed | Durable checkpoint consistency | [DDS], pp. 28, 85 |
| Error ledger / `retry_state` | Partial batch/error state | Collection/object schemas unresolved | Safe partial retries; malformed-record exceptions remain recorded | [DDS], pp. 28–29, 85 |
| Quarantine reason, correlation ID, remediation path | Poison-record result | Names/types/vocabulary unresolved | Bounded retries, quarantine; remaining batch may proceed | [DDS], p. 29 |
| Provisioning/readiness | Workspace readiness and index coverage | Schema/default unresolved | Incomplete provisioning blocks sync; search readiness uses coverage, not queue emptiness | [DDS], p. 78 |
| Retention class | Workspace retention policy | Vocabulary/type/default unresolved | Legal-hold exceptions maintained | [DDS], pp. 24, 26 |
| Allowed models/deployments | Workspace deployment allowlist | Collection schema unresolved | Specific deployments, not broad brands; approved equal-or-stronger fallback | [DDS], pp. 24, 37 |
| Approved toolsets | Version-pinned capabilities | Collection schema unresolved | Discovery is not authorization; no arbitrary browser tool definitions | [DDS], pp. 7, 24, 41 |
| Reviewer routing/pools | Workspace review policy | Schema/default unresolved | Minimum role, separation of duties, configured expiry/escalation | [DDS], pp. 24, 45 |
| Policy/configuration revision | Update precondition | Type/carrier unresolved | Reject stale updates; durable audit | [DDS], p. 24 |
| Model registry metadata | Capability, region, data-handling class, context length, cost profile, evaluation approval | Names/types/mandatory public properties unresolved | Selected route must be approved for workspace and maximum included data class | [DDS], pp. 37, 62 |

**Needs confirmation — OQ-API-019:** Define connector read/sync/admin permissions, providers, capability schema, safe lower-trust restrictions, sync concurrency, retries, run states, history pagination, credentials/revocation APIs, and remediation contract. Missing ACL capability must not disable revocation-before-next-retrieval.  
**Earlier:** `OQ-SCR-019`, `CON-SCR-013`.

**Needs confirmation — OQ-API-020:** Supply actual workspace-policy APIs, editable fields, model/tool/reviewer registry contracts, revision transport, activation, precedence, and validation. The case PATCH association in §6.1.1 is not approval to mutate workspace policy through API-004.  
**Earlier:** `OQ-SCR-020`, `CON-SCR-010`.

### API-021–API-024 — Audit, Usage, and Evaluation Interfaces

#### Per-Operation Interface

| API | Path/query/header/body | Confirmed success | Response properties/types/requiredness/defaults |
|---|---|---|---|
| API-021 | Audit cursor convention confirmed; actual cursor/filter parameter names unresolved. Authentication/trace. No body described. | `200`; cursor-paginated immutable authorized log | Audit selected data below confirmed; wire envelope/property names, requiredness, filters, ordering, detail retrieval unresolved |
| API-022 | Workspace/reporting-window/cost-center/deployment filter transport unresolved. Authentication/trace. No body described. | `200`; costs, quotas, trends | Units, currencies, decimals, time-series schema, window defaults, forecast fields, and pagination unresolved |
| API-023 | Required job `Idempotency-Key`; validated evaluation body; dataset/model/prompt/version selection fields unresolved | `202`; frozen benchmark evaluation operation | Evaluation identifier/result-link properties and types unresolved; no completed scorecard implied |
| API-024 | Required `evaluationId`; query/details pagination unresolved; no body described | Evaluation result read operation; HTTP success status unresolved | Status enumeration, scorecard projection, domain/statistical fields, requiredness, and failure envelope unresolved |

**Sources:** [DDS], pp. 61–66, 74–76, 83.

#### Data Contracts

| Content | Meaning / source terminology | Type | Required / default | Constraints and source |
|---|---|---|---|---|
| Audit identity/scope | `audit_events.id`, `tenant_id`, `actor_id` | Domain identifiers; wire schemas unresolved | Required stored identity/scope; response presence unresolved | Tenant/redacted scope; append-only. [DDS], pp. 22, 62, 85 |
| Audit action/digest | `action`, `digest` | Type/encoding unresolved | Selected stored fields confirmed | Batch hash chain and independent retention export. [DDS], pp. 62, 85 |
| Auditor evidence | Decision metadata, prompt-template digests, access events | Structured schemas unresolved | Authorized read scope confirmed; projection unresolved | No unrestricted full prompts or case-content editing. [DDS], p. 11 |
| Audit times/traces | UTC occurrence and correlation evidence | RFC 3339 if public; identifiers | Exact response requiredness unresolved | No private resource existence or document text in diagnostics. [DDS], pp. 23, 48, 54, 64 |
| Usage costs/quotas/trends | API-022 reporting | Numeric/object/series schemas unresolved | Content confirmed; all property/default contracts unresolved | Per-tenant/workspace attribution. [DDS], pp. 65–66, 83 |
| Budget/forecast/rejected excess | Daily rollup data | Types/window/units unresolved | Content confirmed | Daily aggregation does not establish job execution time. [DDS], p. 65 |
| Cost center/deployment | Workspace cost-center and model deployment version | Reference schemas unresolved | Attribution required | Actual invoked deployment version. [DDS], p. 65 |
| Token counts | `in_tokens`, `out_tokens` | Numeric wire/data types unresolved | Stored ledger fields confirmed | Reserved/tracked under workspace quota. [DDS], pp. 38, 85 |
| Embedding/storage/indexing use | Separate measures | Units/types unresolved | Separately tracked content | No invented conversion factor. [DDS], pp. 65, 68 |
| Evaluation identity/status | Evaluation record | Identifier and status schema unresolved | Accepted operation is durable; status enum absent | `202` is not completion. [DDS], pp. 74–76, 83 |
| Dataset/manifest | Frozen, versioned synthetic evaluation corpus and signed manifest | Schema/hash/signature encoding unresolved | Frozen/versioned reviewed corpus required | 1,200 reference synthetic permission-controlled cases; not arbitrary POST size limit. [DDS], pp. 75, 88–89 |
| Expected citations/decisions | Per-example expected outcomes | Schemas unresolved | Every reference example stores them | Fixture replacement must be controlled; no mutable scorecard fixture editing implied. [DDS], pp. 75, 88 |
| Grounded citation precision | Quality measure | Numeric/statistical representation unresolved | Target `>=0.97` | Frozen evaluation evidence. [DDS], p. 75 |
| Unsupported-claim rate | Quality measure | Numeric/statistical representation unresolved | Target `<=0.02` | No inference from mock evidence-coverage percentage. [DDS], p. 75 |
| High-risk policy recall | Safety measure | Numeric/statistical representation unresolved | `1.00` on frozen safety suite | Safety/isolation failures cannot be offset by benchmark quality. [DDS], pp. 74–75, 88 |
| Confidence intervals / distribution shift | By-domain evaluation evidence | Statistical/domain schemas unresolved | Reported by domain; low confidence blocks release | Calculations/domain taxonomy absent. [DDS], pp. 75–76 |
| `ReleaseGateResult` | Evaluation/release result | Schema/status vocabulary unresolved | Source component exists | No promotion control or selected result enum inferred. [DDS], pp. 75–76 |

**Open questions:**

- **OQ-API-021:** Audit list/detail/redaction/filter/ordering/digest schemas and Auditor evidence path. Earlier: `OQ-SCR-021`.
- **OQ-API-022:** Usage units/currency/windows/precision/filtering/forecasts and projection. Earlier: `OQ-SCR-023`.
- **OQ-API-023:** Evaluation inputs, dataset/model/prompt choices, read permission, states/progress, confidence/domain calculations, scorecard schema, and frozen-manifest verification. Earlier: `OQ-SCR-024`.
- Corporate retention remains unresolved despite the fictional 30-day diagnostic default and distinct seven-year security-audit policy. These are not list-date-range limits. [DDS], pp. 66, 90.

### API-025–API-029 — Export, Deletion, Principal, Membership, and Holds

#### Per-Operation Interface

| API | Parameters | Required controls | Successful content | Needs confirmation |
|---|---|---|---|---|
| API-025 | Required `workspaceId`; export scope/body names/types unresolved | P; `Admin + approver`; two independent approval checks; required job idempotency | `202`; durable controlled export; eventual manifest/package content below | Approval references/carrier, exact request requiredness, snapshot semantics, operation/status/download APIs |
| API-026 | Required `workspaceId`; deletion scope/body unresolved | Same independent approval and job-idempotency requirements; legal holds | `202`; durable deletion; tombstones, removal, receipts, protected-record exceptions | Hold timing/races, partial state, status/receipts, permitted resource inventory, final completion representation |
| API-027 | No path parameter; query absent; authenticated context | Valid principal/tenant | Principal-context read interface exists | HTTP status and all response properties, memberships/role projection, timezone/context values |
| API-028 | Required `workspaceId`; member list/body names/types unresolved | Membership authorization and durable revision/audit controls | Authorized membership update | PUT replace/upsert semantics, member/role fields, requiredness, revision transport, concurrency, status/body, removal behavior |
| API-029 | Hold scope/body identifiers unresolved | Authorized hold creation; validated durable state | Hold operation exists and protects purge-eligible records as applicable | Hold type/reason/scope schema, requiredness/defaults, role, status, revision/idempotency transport, read/release contracts |

**Sources:** [DDS], pp. 21–23, 26, 61–63, 78–80, 83, 89.

#### Export and Deletion Result Content

| Content | Type / required status | Confirmed constraint | Source |
|---|---|---|---|
| Case metadata | Schema unresolved; included in authorized export package | Authorized scope only | [DDS], p. 79, §22.3.1 |
| Approved artifacts | Schema/object references unresolved; included | Export approved artifacts; no invented draft-export allowance | [DDS], p. 79 |
| Source references | Reference schema unresolved; included | Preserve provenance | [DDS], p. 79 |
| Audit manifests/checksums | Manifest/hash schema unresolved; included | Package integrity and immutable audit lineage | [DDS], pp. 62, 79 |
| Secrets/internal model prompts | No permitted public export type | Explicitly excluded | [DDS], p. 79 |
| Tombstones | Schema unresolved; required deletion behavior | Prevent retrieval of soft-deleted entities; final purge reconciled | [DDS], pp. 51, 80 |
| Completion receipts | `deletion_receipts` selected fields: `tenant_id`, `object_ref`, `purge_time`, `actor`; types/wire projection unresolved | Auditable removal and legal-hold exceptions | [DDS], pp. 66, 80, 85 |
| Protected records | Inventory/exception schema unresolved | Retained and receipted under legal hold | [DDS], p. 89, `TST-013` |
| Data-subject request inventory | Schema/endpoint unresolved | Handled through the same deletion inventory | [DDS], p. 80 |

**Needs confirmation — OQ-API-024:** Define independent-approval mechanics, validity/revocation, request scopes, durable status, snapshot/download/receipt contracts, and legal-hold/partial outcomes. Do not implement approval as two client-selected IDs without a resolved independent authorization protocol.  
**Earlier:** `OQ-SCR-025`.

**Needs confirmation — OQ-API-025:** Define principal/membership/provisioning/hold schemas, rights, preconditions, read/status/release operations, and provisioning entry point. Provisioning is idempotent and blocks sync when incomplete, but no provisioning endpoint is confirmed.  
**Earlier:** `OQ-SCR-002/OQ-SCR-026`.

### API-030–API-035 — Status, Contract Discovery, and Design Governance

| API | Parameters / body | Successful response content | Requiredness/types/defaults and open contract |
|---|---|---|---|
| API-030 | No path parameter; query/workspace scope unresolved; no body described | Declared degraded modes | HTTP status, state enum, generation/search availability flags, reduced-quality schema, scope, freshness, and authorization unresolved |
| API-031 | No path parameter; query absent; no body described | External OpenAPI contract | OpenAPI version, retrieval status, exact document, cache/version headers, security policy unresolved |
| API-032 | Validated change/decision content; body field names unresolved; durable context required | Accepted controlled decision/change with audit/outbox evidence | Status/body and sync/async selection unresolved; impact-score types/ranges absent |
| API-033 | Required `id`; no body described | Versioned baseline/revision/decision metadata | HTTP status and response schemas unresolved |
| API-034 | Query/body not described | Liveness interface exists | No confirmed dependency checklist, health enum, response body/status, timeout, or unauthenticated probe exception |
| API-035 | Query/body not described | Readiness interface exists | No confirmed dependency checklist, degradation/readiness mapping, response body/status, timeout, or probe exception |

**Sources:** [DDS], pp. 8–10, 18–20, 54–56, 68–70.

For design governance:

- Proposed changes carry impact scores for behavior, data migration, threat surface, and operating cost.
- An approved record increments minor revision; incompatible protocol changes increment major revision.
- Every revised invariant must link to at least one negative test.
- `ChangeRequest`, `DesignRevision`, `RequirementLink`, and `DecisionRecord` are confirmed boundary terms, not complete JSON schemas.

**Source:** [DDS], pp. 8–10, §§1.1–1.4.

**Open questions:**

- **OQ-API-026:** Design-decision/baseline schemas, roles, impact-score definitions, approval protocol, result mode, and `BaselineCommitted` trigger. Earlier: `OQ-SCR-027`.
- **OQ-API-031:** Health/degraded-mode fields, probe identities, dependencies, freshness, timeouts, and safe reduced-quality transport. Earlier: `OQ-SCR-028`.
- **OQ-API-030:** Obtain actual OpenAPI/protobuf repository contracts and compatibility/version-publication policy.

### API-036–API-044 — Internal HTTP Interfaces

Shared S authentication and trusted tenant/actor/revision/time/trace controls apply. Exact HTTP success statuses and complete wire schemas are **Needs confirmation** for every row.

| API | Path parameters | Query / headers / body | Source-confirmed input or output concepts | Constraints / defaults / open contract |
|---|---|---|---|---|
| API-036 | None | Generation body, scoped workflow authorization, request/response schema versions, idempotency/trace carriers unresolved | Approved deployment; fixed system rules; signed workflow instruction; validated user input; delimited evidence; structured output; token usage | No arbitrary tool authority; no secret leakage; bounded output parsing retries. Complete request/result fields, timeouts, quotas, duplicate invocation accounting unresolved. |
| API-037 | Required `runId` | No query/body described; service/trace controls | Workflow stage, checkpoint, outbox/recovery relationships | Status/envelope/detail projection, event-ledger access, read permissions unresolved |
| API-038 | Required `id` — dead-letter resource | Operator reason, dry-run validation, scope limit; exact body names/types/carriers unresolved; job idempotency if long-running | Validated bounded replay preserving event identity | Reason required; size/units/defaults absent. Dry-run protocol, replay result/status/job schema unresolved. |
| API-039 | Required `id` — stored document resource | Version/object-role/tenant/workspace selection carriers unresolved; no body described | Encrypted source/derivative object and authorization | Response bytes versus metadata/signed URL unresolved; no browser endpoint implied; short-lived access-controlled signed URLs mandatory where used |
| API-040 | None | Purge inventory/eligibility/hold context; names/types unresolved; long-running idempotency as applicable | Tombstones, eligible closed-case retention, blob/index removal, purge receipts | No hold bypass; purge scope, batch bounds, schedule, response and legal-hold-race semantics unresolved |
| API-041 | None | Metrics selection/scope/query and media type unresolved | Rate, errors, latency, saturation, grounding pass, retrieval empty rate, provider throttling, token use, approval backlog age | No raw document/secrets; metric names/types/labels/windows/format unresolved |
| API-042 | None | Capacity selection/scope/query unresolved | Capacity budget, admission permit, recovery checkpoint, load profile | Read operation is not permission to admit runs; response schema/admission threshold values unresolved |
| API-043 | None | Release artifacts/config/migration/gate/sign-off body; names/types unresolved; idempotency as applicable | Image digest, schemas, prompts, model-routing policy; attestation and rollout gates | Verify allowed build identity; safety regression blocks promotion; exact approval/rollout/status protocol unresolved |
| API-044 | Required `releaseId` | Query/detail projection unresolved; no body described | Reconstructible release record and version bindings | Status/schema/read permissions/retention unresolved |

**Sources:** [DDS], pp. 37–39, 48–53, 64–73, 85, 90.

**Needs confirmation — OQ-API-027:** Supply internal request/result schemas, service/operator grants, resource mappings, pagination, success/error statuses, and timeout/retry policies. No operational browser console or execution schedule is established.  
**Earlier:** `OQ-SCR-027`.

### API-045 — `knowledge.search@v1` MCP Tool

This is the one source-supplied typed tool signature. It is not the public search endpoint schema.

| Name | Direction | Meaning | Confirmed type | Required status / default | Constraints |
|---|---|---|---|---|---|
| `query` | Input | Search text | `string` | Listed input; formal required-property declaration/default absent | Length, nonempty/normalization rules unresolved |
| `case_id` | Input | Case scope | `uuid` | Listed input; formal required-property declaration/default absent | Tenant-scoped authorized case |
| `max_items` | Input | Maximum returned item count | `int<=10` | Listed input; omission/default unresolved | Upper bound ten confirmed; lower bound not supplied |
| `evidence_set_id` | Output | Evidence-set identity | `uuid` | Listed output; formal nullability/requiredness absent | Authorized evidence set |
| `citations` | Output | Citation collection | `Citation[]` | Listed output; minimum count/nullable behavior absent | `Citation` schema unresolved; current permission/resolvable anchors apply |
| `read:permitted_documents` | Authorization | Tool capability scope | Exact literal | Required authorization scope | Tenant-scoped |
| Effect | Tool behavior | Read-only | Exact source behavior | No write effect | No arbitrary URLs or filesystem access |

**Sources:** [DDS], p. 87, §C.2; tool controls pp. 41–42.

1. Resolve approved version-pinned MCP server/tool metadata.
2. Authenticate the invoking service.
3. Evaluate principal, workspace policy, tool scope, and data classification independently of discovery.
4. Validate arguments before dispatch.
5. Deny arbitrary or unauthorized tool invocation before dispatch.
6. Return only permitted grounded evidence.
7. Retry only transient read failures under bounded dependency policy.

**Sources:** [DDS], pp. 41–42, 87, 89, `TST-014`.

**Needs confirmation — OQ-API-028:** MCP transport/server URLs, protocol version, formal requiredness/defaults, lower bounds, `Citation`, error/decline representation, scoped grants, and per-dependency timeout/retry limits.

### API-046 — A2A Task Envelope

The example supplies property names and JSON value kinds, not a complete required-property schema.

| Property | Meaning | Type evidence | Required status / default | Constraints / gap |
|---|---|---|---|---|
| `task_id` | Task identity | Example JSON string containing UUIDv7-shaped identifier | Task ID required by §11.2.2; no default | Identity/deduplication validation |
| `tenant_id` | Tenant scope | Example JSON string; relational UUID baseline differs from placeholder | Tenant context required; no default | Immutable signed background-job tenant |
| `capability` | Versioned capability reference | Example JSON string | Capability reference required; no default | Discovery does not authorize invocation |
| `input_schema` | Declared input schema | Example JSON string/`schema://` reference | Declared input schema required | Actual referenced schema unavailable |
| Output schema declaration | Declared output schema | Required concept in §11.2.2; property absent from example | Required concept; field name/type unresolved | Do not invent confirmed `output_schema` field |
| `deadline_at` | Task deadline | Example RFC 3339 JSON string | Deadline required | Reject/stop after deadline under resolved runtime contract |
| `trace_id` | Trace context | Example JSON string | Trace context required | Correlation linkage and other trace fields unresolved |
| `authorization_ref` | Separate grant reference | Example JSON string | Included in example; formal requiredness unresolved | Must resolve authorization; reference alone is not proof |
| `payload` | Typed task data | Example JSON object | Payload schema required by declared task; formal requiredness unresolved | Example has `case_id` and `query`; these do not establish general A2A payload schema |
| `revision`, `actor_id`, `occurred_at`, correlation ID | State-changing boundary attribution | Required boundary concepts in Chapter 11 | Required where handoff changes durable state | Relationship to example/envelope and exact names/carriers unresolved |

**Sources:** [DDS], p. 41, §11.2.2; p. 87, §C.2; signed tenant context p. 22.

**Source-confirmed example — placeholder data, not deployable configuration:**

```json
{
  "task_id": "019ac000-0000-7000-8000-000000000042",
  "tenant_id": "tenant_example_01",
  "capability": "research.grounded_search.v1",
  "input_schema": "schema://oriondesk/research-request/1",
  "deadline_at": "2026-11-09T08:00:00Z",
  "trace_id": "trace_example_01",
  "authorization_ref": "grant_readonly_14",
  "payload": {"case_id": "case_demo", "query": "..."}
}
```

**Needs confirmation — OQ-API-028:** A2A transport, task acceptance/result/decline schemas, output-schema carrier, signing/grant validation, timeouts, task deduplication, and placeholder-versus-UUID representation. The receiving agent may decline; no HTTP decline status is supplied.

### API-047–API-050 — Outbound and Identity Provider Interfaces

| Interface | Path/query/header/body contract | Confirmed successful behavior | Error/retry controls | Missing contract |
|---|---|---|---|---|
| API-047 webhook | Recipient URL, method, signature/age headers, body/event mapping absent | Signed optional outbound notification; recipient verifies signature/event age | Exponential backoff; failure cannot roll back internal case transition | Signature algorithm, canonicalization, key ID/rotation, age window, acknowledgment statuses, deduplication, retry cap, delivery status/admin API |
| API-048 OIDC | Provider URLs/methods/claims/client/callback configuration absent | Authorization-code flow with PKCE; validated API token context | Invalid algorithm/missing tenancy rejected | IdP, claims, algorithms, scopes, redirect URLs, token transport, expiry/session/sign-out and BFF choice |
| API-049 repositories | Provider-specific list/fetch/delta/ACL/delete routes and schemas absent | Preserve source identity, permissions, change history; cursor-ledger outcomes | Honor `Retry-After`; exponential backoff/jitter; malformed record quarantine; credential-revoked jobs fail safely | Exact repositories, grants, cursors, capability mapping, schedules, requests/responses/status codes |
| API-050 models | Provider URL/method/model request/response absent | Approved scoped model generation and usage accounting | Bounded retries/circuit breakers; no unapproved fallback; quota terminal for current run | Exact deployments, regions, data-handling approvals, output schema/adapters, timeouts and retry/accounting mapping |

**Sources:** [DDS], pp. 21, 27–29, 37–39, 49, 55, 90.

**Needs confirmation — OQ-API-029:** Complete webhook security, payload, acknowledgments, retry/deduplication, and administration contracts. Earlier: `OQ-SCR-027`.

**Needs confirmation — OQ-API-034:** Select approved region, identity/search/model providers, model deployments, corporate retention, and connector permissions through dated architecture decisions. No vendor URL, selected provider, approval, owner, or decision date is assigned here. Earlier: `OQ-SCR-030`.

### Asynchronous Event Contracts

#### Common Event Envelope

**API-COM-006 — Event envelope.** All events contain the following exact property names. Producers use UTC and canonical JSON.

| Property | Meaning | Type evidence | Required / default | Constraints |
|---|---|---|---|---|
| `event_id` | Event identity | UUIDv7 identifier baseline; exact JSON encoding unresolved | Required; no default specified | Deduplicate by event ID |
| `type` | Event name/type | Exact event-name literals below; wire scalar schema unresolved | Required | Versioned event vocabulary |
| `schema_version` | Payload/envelope version | Type/format unresolved | Required | Versioned contract |
| `tenant_id` | Immutable tenant scope | Tenant identity required; representation unresolved | Required | Signed background scope and storage predicates |
| `aggregate_id` | Target aggregate identity | Identifier representation unresolved | Required | Authorized aggregate |
| `aggregate_revision` | Revision used for stale detection | Numeric/string wire representation unresolved | Required | Reject/ignore stale mutations according to resolved consumer contract |
| `occurred_at` | Event occurrence time | UTC; timestamp representation governed by contract | Required | Canonical public timestamps RFC 3339 |
| `trace_id` | Trace context | Identifier representation unresolved | Required | No document text/secrets |
| `payload` | Versioned event content | Exact schema unresolved per event | Required | Validate before mutation |

**Source:** [DDS], p. 48, §13.1.1.

The repeated durable-boundary requirements also require actor and correlation attribution. Their carrier is not explicitly included in the §13.1.1 envelope list. Resolve whether they are envelope extensions, payload fields, or linked durable records; do not invent confirmed fields. **OQ-API-035.**

#### Source Event Inventory

Payload-key descriptions below preserve source concepts. Appendix C does not supply exact JSON payload property names/types.

| Event identifier | Producer | Confirmed payload content / consumer action | API and screen relationship | Schema gap / source |
|---|---|---|---|---|
| `CaseCreated` | Case Service | Case ID/revision → run classifier | API-001; SCR-002-A02 | Payload schema unresolved. [DDS], p. 87, §C.1 |
| `DocumentNormalized` | Ingestion | Version ID/source hash → build index | API-006/007; SCR-002-A05/A06 | Payload schema unresolved. [DDS], p. 87 |
| `SearchIndexCommitted` | Indexer | Index generation/document revision → invalidate query cache | API-009/010; SCR-003-A04 | Not confirmation that each search POST writes an index event. [DDS], pp. 34–36, 87 |
| `AgentPlanApproved` | Orchestrator | Run ID/plan hash → dispatch plan steps | API-011/014; SCR-004 | Payload schema unresolved. [DDS], pp. 40–42, 87 |
| `ApprovalDecisionRecorded` | Policy Service | Task/actor/content hash → validate publication | API-017; SCR-005-A04/A05, SCR-002-A12 | Publication still validates exact artifact/current evidence. [DDS], pp. 44–46, 87 |
| `WorkflowStageAdvanced` | Orchestrator | Run/stage/checkpoint → resume consumers | API-013/014/015/037/038; SCR-004 | SSE mapping not established. [DDS], pp. 48–50, 87 |
| `AccessDenied` | Policy Service | Principal/action/policy digest → alert enrichment | Authorization failures; SCR-COM-003 | No private-resource existence leakage. [DDS], pp. 23, 87 |
| `TenantDeletionVerified` | Retention Worker | Manifest ID/receipt hash → close purge record | API-026/040; SCR-X-004 | Exact workspace/tenant completion mapping unresolved. [DDS], pp. 80, 87 |
| `BaselineCommitted` | Producer not explicitly defined | Controlled baseline commitment; correlated audit evidence | API-032/033; SCR-X-008 | Full catalog entry absent. [DDS], pp. 8–10 |
| `RunRequested` | Producer not explicitly defined in catalog | Run request; durable replay-safe workflow | API-012/013 | Full catalog entry absent. [DDS], pp. 15–17 |
| `CaseStateChanged` | Producer not explicitly defined in catalog | Case mutation/closure state evidence | API-004/005; SCR-002-A03/A09 | Full catalog entry absent. [DDS], pp. 24–26 |
| `ConnectorSyncStarted` | Producer not explicitly defined in catalog | Sync-start evidence | API-018/019; SCR-006-A02 | Full catalog entry absent. [DDS], pp. 27–29 |
| `ModelInvocationCompleted` | Producer not explicitly defined in catalog | Generation/usage evidence | API-036/050 | Full catalog entry absent. [DDS], pp. 37–39 |
| `DeploymentPromoted` | Producer not explicitly defined in catalog | Deployment evidence | API-034/035 chapter association | Health GET is not confirmed as promotion trigger. [DDS], pp. 18–20 |
| `DataRetentionPurgeCommitted` | Producer not explicitly defined in catalog | Purge completion evidence | API-040 | Full catalog entry absent. [DDS], pp. 51–53 |
| `ApiCompatibilityVerified` | Producer not explicitly defined in catalog | Compatibility verification evidence | API-031 chapter association | OpenAPI GET is not confirmed as CI verification trigger. [DDS], pp. 54–56 |
| `UserReviewOpened` | Producer not explicitly defined in catalog | Auditable review-open activity | SCR-005-A02; API-GAP-004 | Trigger and schema unresolved; not assigned to all case/evidence GETs. [DDS], pp. 57–59 |
| `SecurityPolicyChanged` | Producer not explicitly defined in catalog | Security-policy evidence | API-029 chapter association; policy gap | Hold creation versus broader policy-change mapping unresolved. [DDS], pp. 61–63 |
| `SloBurnRateDetected` | Producer not explicitly defined in catalog | SLO detection/audit evidence | API-041 chapter association | Usage/metrics GET does not by itself define detector execution. [DDS], pp. 64–66 |
| `BackpressureActivated` | Producer not explicitly defined in catalog | Backpressure evidence | API-030/042 chapter association; run admission | Trigger/full schema unresolved. [DDS], pp. 68–70 |
| `ReleasePromoted` | Producer not explicitly defined in catalog | Release promotion evidence | API-043/044 | Distinct from `DeploymentPromoted` pending explicit mapping. [DDS], pp. 71–73 |
| `EvaluationCompleted` | Producer not explicitly defined in catalog | Evaluation completion evidence | API-023/024; SCR-011 | Full catalog entry absent. [DDS], pp. 74–76 |

**Needs confirmation — OQ-API-035:** Complete schemas, producers, triggers, broker routes, signatures, actor/correlation attribution, event-retention/deduplication periods, and SSE/webhook mappings. Appendix F’s `replay_dedup_hours: 24` is an example, not confirmation of every ledger’s retention or SSE history lifetime.

### Request and Response Examples

#### Confirmed Request Shapes

These illustrate only source-confirmed methods/paths and named controls. Placeholders must be replaced; missing bodies remain unresolved.

```http
POST /v1/cases
Idempotency-Key: <resolved-client-key>

<case-create body: Needs confirmation>
```

```http
PATCH /v1/cases/<caseId>
If-Match: <resolved-current-revision-encoding>

<case patch format and body: Needs confirmation>
```

```http
GET /v1/cases?cursor=<resolved-server-cursor>
```

```http
GET /v1/streams/runs/<runId>
Last-Event-ID: <resolved-retained-offset>
```

The first two operations return `201` and `200` respectively on accepted success; the SSE connection returns `200`. Exact success bodies are not provided by the source.

#### Proposed Partial JSON Mappings

**Proposal — P-API-002:** The following examples demonstrate possible public property mappings for source-confirmed content. All property mappings, wrappers, mandatory properties, media types, and example strings are **unapproved**. They are not executable schemas and must not resolve OQ-API-003 by inference.

**Proposed case-create body:**

```json
{
  "workspace_id": "<authorized-workspace-id>",
  "title": "<business-subject>",
  "description": "<validated-business-context>",
  "impact": "<resolved-impact-value>",
  "urgency": "<resolved-urgency-value>"
}
```

**Proposed case-create response:**

```json
{
  "id": "<created-case-id>",
  "status": "NEW",
  "revision": 1
}
```

`NEW` and the database initial revision `1` are source-confirmed concepts; their mandatory response projection above is proposed.

**Proposed run-acceptance response:**

```json
{
  "run_id": "<persisted-run-id>",
  "status": "REQUESTED"
}
```

**Proposed decision body:**

```json
{
  "decision": "<resolved-approve-or-reject-literal>",
  "artifact_hash": "<exact-reviewed-artifact-hash>",
  "rationale": "<reviewer-rationale>"
}
```

**Proposed search body:**

```json
{
  "query": "<validated-search-query>",
  "case_id": "<authorized-case-id>"
}
```

The proposed search fields must not be accepted as confirmed merely because the MCP contract uses similar names. Successful `200` search responses must contain the confirmed evidence-item content, but the source supplies no complete public success example.

#### Confirmed Canonical Error Example

The following is the exact source example, including fictional sample values.

```http
HTTP/1.1 409 Conflict
Content-Type: application/json
```

```json
{
  "error": {
    "code": "CASE_VERSION_CONFLICT",
    "message": "Case revision no longer matches.",
    "correlation_id": "trace_01HZZ_EXAMPLE",
    "retryable": false,
    "details": {"expected_revision": 7, "actual_revision": 8}
  }
}
```

**Source:** [DDS], p. 84, §A.3.

## Processing and Consistency

### Shared Validation and Transaction Procedure

**API-PROC-001 — State-changing request procedure.**

1. Authenticate the principal/service and establish immutable tenant and trace/correlation context.
2. Validate path, query, headers, body, and declared schema before transaction entry or long-running allocation.
3. Evaluate broad policy at the edge and resource attributes at the domain boundary.
4. Resolve operation identity/idempotency and revision preconditions where applicable.
5. Enter tenant-scoped database context and re-evaluate resource authorization and domain invariants inside the mutation transaction.
6. Apply the accepted business mutation and required append-only revision/decision/audit evidence.
7. Insert corresponding outbox events in the same ACID transaction for source-defined case/approval writes.
8. Commit only accepted state. Rejected stale or unauthorized requests leave business state unchanged.
9. Dispatch asynchronous external work from durable outbox/saga checkpoints, not an uncommitted browser assumption.
10. Return the authoritative result or persisted async identity. Dependency failure must not produce ambiguous success.
11. Reset scoped database session variables after every transaction before connection reuse.

**Sources:** [DDS], pp. 17, 22, 25, 48–56, 86.  
**Screen trace:** `SCR-COM-010`, `SCR-COM-012`.

**Needs confirmation:** Transaction isolation level, lock strategy, audit-write failure behavior, idempotency ledger implementation, exact allocation transaction, and response reconstruction are not selected by the source. **OQ-API-004/OQ-API-005/OQ-API-027.**

### Reads, Writes, and Boundaries by API Group

| Processing ID | APIs | Confirmed reads and business processing | Confirmed writes / transaction boundaries | Source and adjacent gap |
|---|---|---|---|---|
| API-PROC-002 | API-001–005 | Authorized workspace/case; owner/revision/state; explicit impact/urgency and business calendar; approved artifact lineage | Case metadata/revisions/outbox commit transactionally; create starts `NEW`; closure snapshots approved answer, cited versions, reviewer decisions | [DDS], pp. 12, 24–26, 52, 85–86. OQ-API-007/008 |
| API-PROC-003 | API-006/007 | Type/signature/extension/size; scan; layout/page/table/heading reading order; optional OCR; quality gates | Immutable source/version/text/layout/anchors; fingerprint+pipeline derivative identity; quarantine excludes index; `DocumentNormalized` supports indexing | [DDS], pp. 30–32. Blob/database coordination and exact job transaction unresolved: OQ-API-009 |
| API-PROC-004 | API-008–010/045 | Authorized index alias, source ACL/current anchors; lexical/vector candidates; RRF; deterministic rerank; diversity; token budget | Search evidence-set persistence, if any, needs confirmation; index/cache operations have separate durable events | [DDS], pp. 34–36, 87. Do not make every search mutate index: OQ-API-011/035 |
| API-PROC-005 | API-011–015/036/037/046 | Case/evidence/policy/deployment/quota/admission; bounded DAG; allowed tools; structured generation | Persist run/plan revision before side effects; persist each checkpoint before downstream dispatch; separate retrieval, generation, policy, approval records | [DDS], pp. 12, 38–42, 49, 58. OQ-API-012–014/028 |
| API-PROC-006 | API-016/017 | Exact candidate/hash, reviewer policy/task validity/current permissions, normalized policy inputs/version | Immutable decision/outbox transaction; final response pointer and satisfied gate in same publication transaction; no changed artifact under old approval | [DDS], pp. 44–46, 52, 85. Decision-to-publication timing unresolved: OQ-API-015/017 |
| API-PROC-007 | API-018/019/049 | Provisioning, capabilities, workspace credential reference, provider cursor/ACL/delete changes | Durable cursor/high-watermark/error ledger; advance after preceding outcomes; source tombstone/index removal; invalidate ACL-dependent cache before new retrieval | [DDS], pp. 27–29, 78. OQ-API-019 |
| API-PROC-008 | API-020/036/050 and policy gap | Approved registry/maximum material class, signed instruction, validated input, delimited untrusted evidence, token quota | Generation attempt/token ledger/policy evidence; scope-respecting output validation; recorded injection indicators | [DDS], pp. 37–39, 62, 85. Exact storage/write protocol unresolved: OQ-API-020/027/034 |
| API-PROC-009 | API-021/022/041 | Authorized audit ledger and usage/metric aggregates | Audit append-only, batch-chained and independently retained; usage attributed and daily rolled up; reads do not imply new business events | [DDS], pp. 61–66. OQ-API-021/022/035 |
| API-PROC-010 | API-023/024 | Frozen versioned signed corpus; expected citations/decisions; actual prompt/model versions | Durable evaluation/scorecard/release evidence; low confidence blocking; re-evaluation for changed prompt/model | [DDS], pp. 74–76, 88–89. OQ-API-023 |
| API-PROC-011 | API-025/026/029/039/040 | Independent approvals; authorized inventory; legal holds; retention eligibility; object/index fingerprints | Export manifest/checksums; deletion tombstones/blob+index removal/receipts; hold exceptions; eligible closed-case retention only | [DDS], pp. 26, 51–53, 78–80, 85, 89. OQ-API-024/025/027 |
| API-PROC-012 | API-028 and provisioning gap | Workspace tenancy, membership/roles/policy/quota/encryption references | Idempotent provisioning creates policy, references, role bindings, quotas, connector stubs; incomplete state visible and blocks sync | [DDS], pp. 21–23, 78. Membership/provisioning transaction details unresolved: OQ-API-025 |
| API-PROC-013 | API-032/033 | Baseline/revision, impact scores, requirement-to-negative-test links | Accepted baseline changes/versioned audit/outbox; stale/unauthorized writes rejected | [DDS], pp. 8–10. OQ-API-026 |
| API-PROC-014 | API-038 | Authorized dead letter/original event/schema, operator reason, dry-run and scope | Bounded replay preserves original event ID unless explicit migration with provenance link; duplicate/stale mutation not reapplied | [DDS], pp. 48–50, 90. OQ-API-027/035 |
| API-PROC-015 | API-043/044 | Signed artifact/build identity, SBOM/test attestations, backward-compatible schemas/config/prompts/routing, Security/SRE evidence | Reconstructible release record; canary gates; regression causes traffic rollback, not automatic database down-migration | [DDS], pp. 71–73, 89. OQ-API-027 |
| API-PROC-016 | API-030/034/035/042 | Health/degraded/capacity information | No business mutation or promotion trigger established by read endpoints | [DDS], pp. 18–20, 68–70. OQ-API-031/035 |
| API-PROC-017 | API-047 | Accepted internal event and authorized recipient scope | Async delivery state requires resolved contract; webhook failure never rolls back accepted case transition | [DDS], pp. 52, 55. OQ-API-029 |

### Idempotency and Concurrency

**API-PROC-018 — Replay-safe writes.**

- Every cross-service write is idempotent under retries.
- POST mutations creating long-running jobs require `Idempotency-Key`.
- API-001 explicitly requires case-creation idempotency.
- Identical replay returns the original operation/outcome; changed fingerprint under the same key returns `IDEMPOTENCY_CONFLICT`.
- The case-domain key maps actor and request fingerprint to one outcome for **24 hours**.
- Concurrent duplicate submissions must leave one accepted business outcome.
- At-least-once consumers deduplicate event IDs and operation keys and detect stale aggregate revisions.
- No invariant relies on ordering across queue partitions.
- Replay may record a duplicate outcome, but it must not create another accepted business transition.
- Case updates use `If-Match`; conflicting revisions return `CASE_VERSION_CONFLICT` with current revision.
- Publication cannot reuse old approval for another artifact.
- Mutable tool operations require idempotency and separate authorization; consequential operations also require human authorization.

**Sources:** [DDS], pp. 15–17, 25, 42, 45–50, 54, 74, 89.

**Needs confirmation — OQ-API-004:** Define key namespace/tenant/actor/endpoint scope, fingerprint canonicalization, key size, simultaneous-pending replay response, caching of rejected outcomes, result replay after permission changes, expired-key reuse, and TTLs outside the case domain. Do not assume Appendix F’s replay example equals the request-key TTL for every API.

**Needs confirmation — OQ-API-005:** Define revision transport and mutation preconditions outside API-004, conflicting decision races, workspace-policy concurrency, legal-hold races, and exact stale-event handling without selecting a locking implementation by inference.

### Retrieval, Cache, and Eventual Consistency

**API-PROC-019 — Evidence consistency.**

1. PostgreSQL is authoritative for mutable metadata.
2. Blob storage holds encrypted source and immutable normalized artifacts.
3. Search is a nonauthoritative, eventually consistent derivative.
4. Index rebuilds use a parallel generation and switch read aliases atomically only after completeness/recall checks.
5. Retrieval applies document ACLs before releasing text to generation.
6. Source ACL changes invalidate affected retrieval caches before new results are served.
7. Cache keys include tenant, user-scope digest, source ACL revision, query hash, and index generation.
8. Authorization changes purge affected entries before ordinary TTL expiration.
9. Publication re-evaluates current authorization and rejects stale evidence.
10. Failed indexing does not roll back accepted source metadata; reconciliation compares fingerprints and retries.
11. Broken message links are repaired from the outbox ledger.
12. Soft-deleted entities cannot be retrieved; final purge follows the tombstone pipeline.
13. Low-quality extraction remains viewable under permission but is excluded from autonomous recommendations.

**Sources:** [DDS], pp. 9, 16, 27–29, 31–36, 46, 49, 51–53.

No numeric cache TTL, index-readiness threshold, reconciliation schedule, or maximum staleness allowance is supplied. Revoked access is not allowed to remain visible until the next scheduled sync or TTL expiry. **OQ-API-019/OQ-API-027/OQ-API-035.**

### Runtime, Admission, Timeouts, and Retries

| Requirement ID | Area | Confirmed behavior | Unresolved numeric/transport contract |
|---|---|---|---|
| API-PROC-020 | Run admission | Admit new AI runs only when workspace tokens, queue age, and provider capacity satisfy thresholds. Throttle with `429` and `Retry-After`; saved cases remain available. | Threshold values, reservation atomics, quota window, provider capacity mapping |
| API-PROC-021 | Bounded planner | DAG depth maximum eight; maximum sixteen tool invocations; explicit dependencies, persisted plan revision and checkpoints | Depth-counting convention, call accounting including retries, repeated-invalid-plan limit |
| API-PROC-022 | Stop conditions | Terminate on exhausted call budget, repeated invalid plans, policy denial, deadline expiry, or source-described missing approval; report failed checkpoint | Missing approval versus valid waiting, terminal code/state, timeout pause/recovery |
| API-PROC-023 | Run completion | Terminal outcome within configured maximum or recoverable timeout state | Recoverable timeout representation absent from run state catalog; example `180` seconds not HTTP timeout |
| API-PROC-024 | Dependency retries | Bounded exponential backoff, randomized jitter, per-dependency circuit breakers; validation/permission failures permanent and not retried | Attempt caps, intervals, circuit thresholds, deadlines |
| API-PROC-025 | Connector throttling | Honor provider `Retry-After`; enforce workspace quota and fair scheduling; bounded malformed-record retries then quarantine | Provider status translation, retry bounds, fairness algorithm |
| API-PROC-026 | Model validation/accounting | Versioned JSON schema, bounded parse retries; unknown fields/invalid citations/control injection → `MODEL_OUTPUT_INVALID`; quota exhaustion terminal for current run | Retry count, timeout, final error transport, failed-attempt usage accounting |
| API-PROC-027 | Review expiry | Configured SLA; reassign/escalate, never implicitly approve | Duration, timers, late decision response, routing |
| API-PROC-028 | Webhooks | Signed async delivery, exponential retry; no rollback of case transition | Retry cap, acknowledgment mapping, age/signature protocol |
| API-PROC-029 | Degradation | Generation unavailable: keep search/manual editing available. Vector degraded: lexical search may continue with visible reduced-quality flag. Never bypass approval/authorization. | Public response fields, exact admission error during outage, safe fallback eligibility |
| API-PROC-030 | Recovery | RPO `<=15 minutes`, RTO `<=4 hours`; restore object/relational consistency and index rebuild recipes together | Selected provider/region, API behavior during failover, operational protocols |

**Sources:** [DDS], pp. 12, 28–29, 38–42, 45, 49–50, 55, 68–70, 79, 90.

### Configuration and Performance Boundaries

| Item | Source-supported value / interpretation | API consequence |
|---|---|---|
| Case-create latency | Case ID within 300 ms at P95; SLO wording says under 300 ms | Applies to API outcome under defined load, not full browser render. Strict inclusive/exclusive boundary unresolved. |
| Search latency | P95 under 1.5 s, excluding remote connector fetch | Measure retrieval independently of model generation |
| Public API availability | 99.9% monthly | Error-budget calculation/exclusions need confirmation |
| Reference workload | 2,000 daily active users; 60 requests/s steady; 180 requests/s burst; 100,000 indexed documents/tenant maximum; 20 concurrent AI runs/large tenant | Workload assumptions, not automatically request/page limits or selected quota configuration |
| Embeddings | 1536 dimensions in index schema | Internal embedding compatibility required; not a public response obligation |
| Appendix F retrieval example | `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `hybrid_rrf_k: 60` | Versioned configuration examples; not screen/page-size values |
| Appendix F workflow example | `max_plan_depth: 8`, `max_tool_calls: 16`, `run_timeout_seconds: 180`, `replay_dedup_hours: 24` | Depth/call maxima independently confirmed in Chapter 11; timeout/dedup deployment selection remains unresolved |
| Policy example | `auto_publish_classification: INTERNAL`; `require_human_review_for: [HIGH_RISK, RESTRICTED]`; `self_approval_allowed: false` | Does not authorize every `INTERNAL` run to publish; evidence/all policy guards remain required. `HIGH_RISK` is not an information class. |
| Storage/observability example | `upload_limit_mb: 25`; `user_data_region: primary-approved-region`; `trace_sample_rate: 0.10`; diagnostic `30` days; audit `7` years | Preserve example identifiers; no selected region, trace policy, corporate retention, or API date-range limit inferred |

**Sources:** [DDS], pp. 12, 34, 40, 65–69, 90.

**Needs confirmation — OQ-API-033:** Resolve exact SLO measurement points/load distribution, strict case-create boundary, availability calculation, and workload-versus-admission configuration. Earlier: `OQ-SCR-031`.

## Errors and Acceptance Criteria

### Canonical Error Body

| Field | Meaning | Type confirmed by example | Required status | Constraints |
|---|---|---|---|---|
| `error` | Error envelope | JSON object | Canonical envelope structure confirmed; applicability to every failure/RPC unresolved | No secret/private-content leakage |
| `error.code` | Stable business/technical code | JSON string | Present in canonical example; complete mandatory schema unresolved | Preserve exact existing literals pending casing decision |
| `error.message` | Safe explanatory message | JSON string | Present in example; mandatory/localization contract unresolved | No raw prompts/retrieved documents/private existence |
| `error.correlation_id` | Support correlation | JSON string | Present in example; mandatory transport unresolved | Independent correlation linkage; no secret data |
| `error.retryable` | Whether failure is transient/retryable | JSON Boolean | Present in example; all-code mapping unresolved | Canonical revision conflict is `false`; validation/permission failures permanent |
| `error.details` | Safe structured validation/conflict data | JSON object in example | Optional safe structured details are allowed | Per-code schema unresolved |
| `expected_revision`, `actual_revision` | Conflict revisions | JSON numbers in example | Shown in case conflict; exact general requiredness/wire integer format unresolved | Current revision must be supplied for case conflict |

**Sources:** [DDS], pp. 25, 49, 84.

**API-COM-007 — Safe errors.** Error details, public responses, traces, provider requests, and export packages must obey their separate redaction scopes. Errors must not include connector credentials, full prompts, retrieved documents, or unauthorized resource existence. Partial processing must not be represented as approved/published success.  
**Sources:** [DDS], pp. 13, 54, 61–66, 79, 84.  
**Screen trace:** `SCR-COM-011`.

### Failure Mapping and Caller Actions

Caller actions below implement the source’s permanent/transient and authoritative-state distinctions; no retry interval or new endpoint is invented.

| Failure condition | Affected APIs | Confirmed HTTP status | Confirmed code / outcome | Response and caller action | Gap / source |
|---|---|---|---|---|---|
| Case revision no longer matches | API-004; other case mutation mapping unresolved | `409` | `CASE_VERSION_CONFLICT` | Safe canonical error with current revision; do not report save success. Obtain authorized current state and resolve conflict before a new attempt. | Encoding/merge behavior unresolved. [DDS], pp. 25, 83–84 |
| Same idempotency key, changed fingerprint | API-001 and job-creating POSTs | `409` confirmed by test | `IDEMPOTENCY_CONFLICT` | No second outcome under key; caller must correct operation identity/payload intentionally, not blindly retry changed data | Complete per-operation mapping unresolved. [DDS], pp. 54, 89 |
| Schema-invalid request | Applicable schema-validated public operations | `422` | Code **Needs confirmation** | Safe validation details if supplied; correct input; no transient retry | Field-path/detail contract unresolved. [DDS], pp. 54, 56, 84 |
| Invalid/missing token, unexpected algorithm, missing tenant claim | P/S boundaries | **Needs confirmation** | Code **Needs confirmation** | Reject before unauthorized work; caller follows resolved authentication contract | Do not assume `401/403` mappings. [DDS], pp. 18, 21–23 |
| Role/resource/segregation-of-duty denial | Applicable resource operations | **Needs confirmation**, except non-disclosing not-found class | Stable non-sensitive code required; literal absent | Permanent denial; no retry as transient; audit permitted denial metadata | [DDS], pp. 22–23, 49 |
| Foreign-tenant or absent ID | Resource reads/mutations | `404`-equivalent non-disclosing class | Code **Needs confirmation** | Same observable response class; no existence distinction | Exact status/body/timing contract unresolved. [DDS], pp. 23, 89 |
| AI-run admission throttled | API-011/012 | `429` | Code **Needs confirmation** | Include `Retry-After`; no run-start success implied; saved cases remain usable | Exact retryable/details mapping unresolved. [DDS], p. 69 |
| Current run quota exhausted | API-036/run workflow | Public/internal mapping **Needs confirmation** | Terminal current-run outcome; literal code absent | Do not auto-switch model/data class; surface authoritative failed checkpoint | Distinct from new-run admission. [DDS], p. 38 |
| Connector credentials revoked | API-018/019/049 queued work | **Needs confirmation** | `CONNECTOR_REAUTH_REQUIRED` | Persist safe failed job condition; reauthentication through unresolved contract; never expose tokens | [DDS], p. 27 |
| Repository/provider throttling | API-049/050 | Provider `429` storms confirmed; public translation unresolved | Code **Needs confirmation** | Capped retries; honor `Retry-After` where applicable; backpressure controls admitted load | [DDS], pp. 28, 49, 70, 89 |
| Malformed connector record after bounded retries | API-049 and sync outcomes | **Needs confirmation** | Quarantine reason code required; vocabulary absent | Quarantine and durable exception/remediation ledger; remaining batch may proceed | [DDS], p. 29 |
| Unsupported type, MIME/extension mismatch, size/decompression limit | API-006 | **Needs confirmation** | Stable safe failure required; literal absent | Fail closed; no unsafe parsing/indexing; caller corrects file/input | Do not invent `413/415` or codes. [DDS], pp. 13, 30 |
| Malware/unsafe PDF/polyglot content | API-006/007 | **Needs confirmation** | `QUARANTINED` state; error literal absent | No indexing; safe status/remediation only | [DDS], pp. 30, 82, 89 |
| Low-quality extraction | API-007 and evidence workflow | **Needs confirmation** | Quality flags; not automatically quarantine | Authorized view remains possible; autonomous recommendation excluded | [DDS], p. 32 |
| Insufficient evidence quality/confidence | API-009/retrieval/run | **Needs confirmation** | `NO_SUPPORTED_EVIDENCE` | No fabricated context; clarification or human route only through resolved contract | [DDS], p. 36 |
| Model unknown fields, invalid citations, injected control characters | API-036/050/run | **Needs confirmation** | `MODEL_OUTPUT_INVALID` | Bounded validation retries; no publish; report authoritative failed checkpoint | [DDS], pp. 38, 41, 89 |
| Missing citations | Run/publication | **Needs confirmation** | Needs-review or unsupported outcome | Do not publish unsupported answer | Relationship to schema-invalid citations needs confirmation. [DDS], p. 89, `TST-009` |
| Arbitrary/unauthorized MCP capability | API-045/046/run | **Needs confirmation** | `DENY` before dispatch as test outcome; not an invented HTTP error code | No dispatch or equivalent-tool substitution | [DDS], pp. 41–42, 89 |
| Stale/wrong reviewed artifact hash | API-017 | `409` conflict surface confirmed | Stale rejection; exact code absent | Reject/audit; no changed artifact under old approval; reload exact review context | [DDS], pp. 45–46, 83, 89 |
| Self-approval where prohibited | API-017 | **Needs confirmation** | Denial; exact code absent | High-risk author cannot self-approve; apply resolved broader separation rules | [DDS], pp. 11, 85, 90 |
| Expired review task | API-017/review workflow | **Needs confirmation** | `EXPIRED` review state; late-decision error absent | No implicit approval; reassignment/escalation recorded | [DDS], pp. 45, 82, 89 |
| Policy denial/runtime budget/deadline failure | Run/tool/publication | **Needs confirmation** | `DENY` policy outcome / failed checkpoint | Stop unauthorized/exhausted action; do not change historical denial | [DDS], pp. 41–46 |
| Dependency unavailable | All applicable boundaries | **Needs confirmation** | Documented retryable error or persisted async job ID | Retry only transient failures under bounded policy, or track durable operation; never ambiguous success | [DDS], interface requirements pp. 8–80 |
| SSE retained cursor expired/gap/token expiry | API-015 | **Needs confirmation** | Code/protocol **Needs confirmation** | Do not infer completion; authoritative run state remains recovery basis | [DDS], pp. 55, 58 |
| Failed index write | Ingestion/index/workflow | API/async mapping **Needs confirmation** | Reconciliation outcome; code absent | Keep accepted metadata durable; reconcile fingerprints/retry | [DDS], p. 49 |
| Single-admin export/delete bypass | API-025/026 | **Needs confirmation** | Denial; code absent | Independent approval checks must prevent execution | [DDS], pp. 78, 83, 88 |
| Legal hold during purge | API-026/040 | **Needs confirmation** | Protected records retained/receipted | Do not report complete deletion of protected data; return resolved exception/receipt representation | [DDS], pp. 80, 89 |
| Attempt historical audit/decision edit | Audit/storage/internal mutation boundary | **Needs confirmation** | Rejected; code absent | Append-only history unchanged | [DDS], pp. 62, 88 |
| Poisoned evaluation fixture/safety regression/low confidence | API-023/024/043 | **Needs confirmation** | Blocking release outcome | No promotion based on benchmark score despite critical safety failure | [DDS], pp. 74–76, 88–89 |

**Needs confirmation — OQ-API-032:** Complete per-operation status/code/body/retryable/detail mappings, canonical error casing, validation field paths, dependency mapping, missing-header responses, cursor failures, late decision responses, and HTTP versus asynchronous failure representation.  
**Earlier:** `OQ-SCR-029`, `CON-SCR-012`.

### Acceptance Criteria

Unless a row supplies an exact status/schema, test the confirmed invariant and complete the wire assertion after the linked open contract is resolved. Unknown values must not be replaced with implementation-selected defaults.

| Acceptance ID | Prerequisites and action | Expected result | Trace / source |
|---|---|---|---|
| AC-API-001 | Authenticated Analyst, authorized workspace, valid resolved case payload/key; invoke API-001 | `201`, one case identifier, initial case `NEW`; classification is asynchronous | API-001; `AC-SCR-001`. [DDS], pp. 12, 83 |
| AC-API-002 | Same actor/payload/key within case contract period; submit twice | One case and identical original response | `TST-001`; `AC-SCR-002`. [DDS], pp. 25, 89 |
| AC-API-003 | Reuse accepted create key with changed body | `409 IDEMPOTENCY_CONFLICT`; no second outcome under key | `TST-002`; `AC-SCR-003`. [DDS], pp. 54, 89 |
| AC-API-004 | Submit concurrent/retried cross-service writes and replay same event 100 times | Exactly one accepted business transition; duplicates do not reapply state | `T-07`, `TST-007`; API-PROC-018. [DDS], pp. 15–17, 48, 88–89 |
| AC-API-005 | Foreign-tenant token with known case ID; compare absent-ID read | Same `404`-equivalent non-disclosing response class; no content/existence leakage | `TST-003`; API-COM-002; `AC-SCR-004`. [DDS], pp. 23, 89 |
| AC-API-006 | Request any tenant-owned resource through wrong scoped service/job context | Domain/storage guards prevent cross-tenant access; no business mutation; safe denial evidence | `T-01`; API-COM-002/API-PROC-001. [DDS], pp. 22–23, 51, 88 |
| AC-API-007 | API-004 with stale `If-Match` | `409 CASE_VERSION_CONFLICT`, current revision, no stale write | `AC-SCR-005`; [DDS], pp. 25, 83–84 |
| AC-API-008 | API-004 with authorized current revision and valid resolved patch | `200`, accepted monotonic revision/change; required case/revision/outbox evidence committed | API-PROC-002; [DDS], pp. 24–26, 52 |
| AC-API-009 | Invalid schema input before mutation/job allocation | `422` for public schema-invalid request; no accepted mutation or premature work allocation | API-PROC-001; [DDS], pp. 54, 56 |
| AC-API-010 | Classification result followed by user correction | Labels/confidences/provenance available; correction requires reason code and preserves lineage | `SCR-002-A04`; `AC-SCR-006`; API-GAP-001. [DDS], p. 12 |
| AC-API-011 | Resolved impact/urgency/business-calendar rules; create/update case | Priority uses explicit business inputs, not model output alone; advisory breach prediction cannot alter deadline | API-CASE-F06–F08/F18. [DDS], p. 25 |
| AC-API-012 | Permitted file, matching signature/extension, below resolved cap; API-006 | `202` ingestion; scan before parse; no macros or embedded remote fetch; no immediate `READY` assumption | `AC-SCR-007`; [DDS], pp. 30–32, 83 |
| AC-API-013 | Oversized, MIME-mismatched, polyglot, bomb, or unsafe PDF | Fail closed; unsafe content quarantined, never indexed; stable safe error/outcome | `T-04`, `TST-015`; `AC-SCR-008`. [DDS], pp. 13, 30, 88–89 |
| AC-API-014 | Authorized low-quality document | Viewable through resolved safe source path; excluded from autonomous recommendation | `AC-SCR-009`; [DDS], p. 32 |
| AC-API-015 | Reprocess same source under changed pipeline version | Immutable derivatives coexist; original claims/source identity preserved | API-PROC-003. [DDS], p. 31 |
| AC-API-016 | Mixed permitted/forbidden corpus; API-009/API-045 | Supported `200` public search returns only authorized evidence; forbidden text never sent to generation | `AC-SCR-010`; [DDS], pp. 22, 34–36, 83 |
| AC-API-017 | Revoke indexed source access; issue next query | No forbidden evidence; affected cache invalidated before response | `TST-004`, `T-08`; `AC-SCR-011`. [DDS], pp. 27–29, 88–89 |
| AC-API-018 | Authorized citation with valid stored version/anchor | Citation verifies; reviewer can open source and highlighted anchored page range before approval | `AC-SCR-012`; API-EVID-F01–F10. [DDS], pp. 31, 35, 57 |
| AC-API-019 | Evidence insufficient/ambiguous | `NO_SUPPORTED_EVIDENCE` or authorized clarification/human route; no fabricated context | `AC-SCR-013`; [DDS], p. 36 |
| AC-API-020 | Authorized Analyst, admitted valid API-011 request/key | `202`, immediately persisted run, durable visible retrieval/generation/policy progression | `AC-SCR-014`; [DDS], pp. 58, 83 |
| AC-API-021 | Run admission thresholds fail | `429` plus `Retry-After`; no started-run success; saved case remains available | `AC-SCR-016`; [DDS], p. 69 |
| AC-API-022 | Refresh/read current run, reconnect within retained SSE history | API-013 `200` reconstructs state; API-015 `200` backfills monotonically scoped retained offsets via `Last-Event-ID` | `AC-SCR-015`; [DDS], pp. 55, 58, 83 |
| AC-API-023 | Stream/backfill request from unauthorized scope | No private events outside caller scope | API-015; [DDS], p. 55 |
| AC-API-024 | Planner reaches depth/tool budget or proposes arbitrary/denied capability | Bound enforced before unauthorized dispatch; `DENY` for arbitrary MCP; no equivalent-tool substitution; failed checkpoint visible | `T-10`, `TST-014`; `AC-SCR-018`. [DDS], pp. 40–42, 88–89 |
| AC-API-025 | Hostile retrieved paragraph/tool directive | Evidence remains untrusted/delimited; no tenant/approval/tool authority change; injection indicators recorded | `T-02`; API-COM-003/API-PROC-008. [DDS], pp. 7, 38–39, 61, 88 |
| AC-API-026 | Gateway receives unknown field/invalid citation/control injection | `MODEL_OUTPUT_INVALID`; bounded retries; no publication | `TST-005`; `AC-SCR-017`. [DDS], pp. 38, 89 |
| AC-API-027 | Generated candidate lacks citations | Needs-review or unsupported outcome; no unsupported approved answer | `TST-009`; [DDS], p. 89 |
| AC-API-028 | Approved provider unavailable, restricted input present | No unapproved region/deployment fallback; only approved equal-or-stronger class eligible | `T-06`; [DDS], pp. 37, 88 |
| AC-API-029 | Current run exhausts token quota | Terminal current-run outcome; no automatic model/data-class change | API-PROC-026. [DDS], p. 38 |
| AC-API-030 | Valid reviewer context; inspect review task | Exact artifact/citations/actual model/prompt version/policy reasons available; source inspection possible before approval | `AC-SCR-019`; [DDS], pp. 57–58 |
| AC-API-031 | Authorized nonexpired independent reviewer, unchanged hash, completed resolved fields; API-017 | `200`, immutable decision includes actor/time/hash/rationale; publication only after satisfied gate | `AC-SCR-020`; [DDS], pp. 45–46, 83 |
| AC-API-032 | Wrong/prior artifact hash in API-017 | `409` conflict surface; stale rejection audited; changed artifact not published | `TST-006`, `T-03`; `AC-SCR-021`. [DDS], pp. 45–46, 83, 88–89 |
| AC-API-033 | Author attempts own high-risk approval | Denied; no high-risk publication without independent authorized review | `AC-SCR-022`; [DDS], pp. 11, 13 |
| AC-API-034 | Review SLA expires | No implicit approval; reassignment/escalation and expiry evidence recorded | `TST-010`; `AC-SCR-023`. [DDS], pp. 45, 89 |
| AC-API-035 | Replay accepted approval with different artifact or revoke source permission before publish | One accepted gate transition; reject changed/stale unauthorized evidence; final pointer and satisfied gate commit atomically | `AC-SCR-025/026`; [DDS], pp. 13, 45–46, 52 |
| AC-API-036 | Rework rejected/denied recommendation | New run revision follows controls; historical denial not retroactively approved | `AC-SCR-024`; [DDS], pp. 46, 75 |
| AC-API-037 | Override attempted without elevated role/secondary reviewer/audited reason | No policy bypass; only resolved authorized override may proceed | `SCR-005-A07`; [DDS], p. 46 |
| AC-API-038 | Authorized permitted closure | Snapshot approved answer/cited immutable versions/reviewer decisions; preserve closed lineage and legal-hold exceptions | `AC-SCR-027`; [DDS], pp. 24–26 |
| AC-API-039 | Fully provisioned Admin starts sync | `202`; durable operation; unsupported capabilities produce explicit lower-trust warning | `AC-SCR-028`; [DDS], pp. 27, 78, 83 |
| AC-API-040 | Partial sync retry or malformed record | Cursor advances only after durable preceding outcomes; bounded retries/quarantine/error ledger allow safe remaining batch | API-PROC-007; [DDS], pp. 28–29 |
| AC-API-041 | Connector credentials revoked with queued work | `CONNECTOR_REAUTH_REQUIRED`; no token disclosure | `AC-SCR-029`; [DDS], p. 27 |
| AC-API-042 | Stale/unauthorized workspace policy change | No policy mutation; current authorized update uses revision precondition and durable audit | `AC-SCR-030`; API-GAP-002. [DDS], p. 24 |
| AC-API-043 | Auditor API-021 query; historical edit attempt | `200` cursor-paginated redacted immutable log; historical review/audit edit rejected | `T-09`; `AC-SCR-031`. [DDS], pp. 11, 62, 83, 88 |
| AC-API-044 | Admin API-022 query | `200`; attributed costs/quotas/trends; model/embedding/storage/indexing use separately attributable | `AC-SCR-036`; [DDS], pp. 65, 83 |
| AC-API-045 | Admin starts frozen evaluation; prompt/model changed | `202` start; resolved read returns authoritative frozen/versioned score evidence; changed prompt/model reevaluated | `AC-SCR-037`; [DDS], pp. 74–76, 83 |
| AC-API-046 | Poisoned fixture, low confidence, safety regression, or critical isolation/approval failure | Release blocked; targets preserve `>=0.97`, `<=0.02`, `1.00`; no benchmark compensation for safety failure | `T-12`, `TST-016`; [DDS], pp. 74–76, 88–89 |
| AC-API-047 | Single Admin requests controlled export/delete | Independent approval checks prevent bypass | `T-11`; `AC-SCR-038`. [DDS], pp. 78, 83, 88 |
| AC-API-048 | Proper independent export approvals; API-025 | `202`; package includes metadata/approved artifacts/source references/audit manifests/checksums; excludes secrets/internal prompts | `AC-SCR-039`; [DDS], pp. 79, 83 |
| AC-API-049 | Legal hold during authorized deletion/purge | API-026 accepts durable controlled workflow as applicable; protected records retained/receipted; eligible objects removed with tombstones/receipts | `TST-013`; `AC-SCR-040`. [DDS], pp. 80, 83, 89 |
| AC-API-050 | Incomplete provisioning then sync attempt | Visible incomplete state; no connector sync until complete; provisioning replay remains idempotent | `SCR-X-002`; [DDS], p. 78 |
| AC-API-051 | Operator replay missing reason/dry-run/scope, then valid bounded replay | Invalid replay rejected; valid replay preserves event identity unless explicit migration provenance; no duplicate transition | API-038; [DDS], pp. 48–50, 90 |
| AC-API-052 | Index write fails after accepted source metadata | Metadata remains durable; reconciliation fingerprints/retries restore derivative consistency | API-PROC-019; [DDS], p. 49 |
| AC-API-053 | Model/vector degradation | Manual editing/evidence remain available where safe; lexical-only results visibly reduced quality; no approval/ACL bypass | `AC-SCR-032/033`; [DDS], pp. 69, 79 |
| AC-API-054 | Invalid token algorithm or missing tenant; internal wrong audience | Rejected before unauthorized work; service identity remains scoped/distinct | API-COM-002; [DDS], pp. 18, 21–23 |
| AC-API-055 | Read public response/error/trace/provider request/export | No out-of-scope secrets/raw credentials/document telemetry; safe required evidence retained | `T-05`; API-COM-007. [DDS], pp. 15, 54, 61–66, 79, 84, 88 |
| AC-API-056 | Attempt incompatible schema/enum deletion while active readers depend on it | CI/contract governance blocks breaking change; migration remains expand-and-contract | API-COM-004; [DDS], pp. 52, 55 |
| AC-API-057 | Supported release request with invalid build/sign-off or regressed safety | No promotion; valid release binds image/schema/prompt/routing evidence; regression rollback changes traffic, not automatic down-migration | API-043/044; [DDS], pp. 71–73, 89 |
| AC-API-058 | Revised design invariant without linked negative test | Controlled baseline cannot satisfy acceptance; accepted changes retain versioned audit/replay evidence | API-032/033; [DDS], pp. 8–10 |
| AC-API-059 | Webhook delivery fails after committed case change | Case transition remains committed; signed delivery retries under resolved bounded policy | API-047; [DDS], pp. 52, 55 |
| AC-API-060 | Reuse pooled database connection across tenants | Session context reset after every transaction; workspace-tenancy controls prevent leakage | API-PROC-001; [DDS], p. 86 |
| AC-API-061 | Regional recovery fault injection | Reference recovery meets RPO `<=15 minutes`, RTO `<=4 hours`; object/relational/index evidence consistent | `TST-012`; [DDS], pp. 69–70, 89 |
| AC-API-062 | Defined-load API performance test | Verify case-create P95 boundary after wording resolution; search P95 under 1.5 s excluding remote fetch; generation separately measured | API-PROC-020; `OQ-API-033`. [DDS], pp. 12, 65, 68 |

#### Verification Fixture Requirements

- Use synthetic successful, empty, mixed-permission, adversarial, and malformed fixtures.
- Record the seed for randomized tests.
- Exercise state, idempotency, authorization, approval hashes, retries, and schema compatibility without live model dependencies where deterministic testing is possible.
- Consumer-driven contracts pin provider-facing adapters.
- Integration tests cover PostgreSQL transactions, outbox replay, ACL revocation, delayed indexing, and purge.
- Critical isolation and approval tests pass with zero exceptions.
- Release test outputs are signed and linked to release digest.
- `SEC-001`–`SEC-012` are source-described release-blocking identifiers, but their individual definitions are not supplied. Do not map them to new API rules by invention.

**Sources:** [DDS], pp. 74–76, 88–89.

## Consistency and Open Questions

### Source Conflicts and Required Amendments

This specification does not rewrite `01_screen_functions.md`. The following records identify unresolved source conflicts, affected API/screen IDs, and required contract amendments.

| Conflict ID | Evidence / conflict | Affected requirements | Required resolution or earlier amendment |
|---|---|---|---|
| CON-API-001 | `POST /v1/runs` in Chapter 3 versus case-scoped run creation in Chapters 2/11 and §A.2 | API-011/012; `SCR-002-A07`, `CON-SCR-004` | Resolve canonical and alternate semantics; amend earlier integration binding only after decision. [DDS], pp. 12–17, 40–42, 83 |
| CON-API-002 | Missing approval terminates run; `AWAITING_REVIEW` also confirmed; recoverable timeout absent from state catalog | API-011–015; API-PROC-022/023; `SCR-004`, `CON-SCR-005` | Define waiting/failure/timeout accounting and representation; keep review SLA separate. [DDS], pp. 12, 41, 45, 49, 82, 90 |
| CON-API-003 | Closure exists, but explicit predecessor-to-`CLOSED` transition and reopen API absent | API-005/API-GAP-005; `SCR-002-A09/A10`, `CON-SCR-006` | Complete states/roles/preconditions/result; preserve closed lineage. [DDS], pp. 24–26 |
| CON-API-004 | Role aliases/relationships inconsistent; Auditor evidence journey exceeds listed case-read roles | API-COM-002; API-003/004/009/017/025/026; `CON-SCR-007/008` | Explicit role/attribute matrix and redacted Auditor evidence path; no inferred grants. [DDS], pp. 11, 22, 83 |
| CON-API-005 | High-risk self-approval prohibition versus broader `no self approval` and example false setting | API-017; API-PROC-006; `CON-SCR-009` | Resolve broader scope/exception policy without weakening high-risk prohibition. [DDS], pp. 11, 85, 90 |
| CON-API-006 | Workspace settings associated with case PATCH in §6.1.1 | API-004/API-GAP-002; `SCR-007`, `CON-SCR-010` | Supply true workspace-policy APIs; do not reuse case PATCH solely from association. [DDS], p. 24 |
| CON-API-007 | Repeated GET boundary prose associates reads with long-running allocation/durable events without precise triggers | API-002/007/008/013/014/016/020/027/031/033–035/037/039/041/042/044; event catalog | Define actual read behavior and event triggers. Do not infer every GET creates jobs or changes business state. [DDS], corresponding chapter sections pp. 8–80 |
| CON-API-008 | `UserReviewOpened` named in Chapter 16, absent from Appendix C catalog | API-GAP-004/API-COM-006; `SCR-005-A02`, `CON-SCR-011` | Add reviewed trigger/schema/producer and appropriate interface; case/evidence GET is not automatically review-open mutation. [DDS], pp. 57–59, 87 |
| CON-API-009 | §15.1.1 says snake-case codes; canonical/tests use uppercase literals | API-COM-007/error mapping; `CON-SCR-012` | Preserve exact existing codes; explicitly decide canonical casing and per-code schemas. [DDS], pp. 54, 84, 89 |
| CON-API-010 | Lower-trust ingestion for missing connector capabilities versus mandatory ACL/revocation invariant | API-018/019/049; API-PROC-007/019; `CON-SCR-013` | Define safe restrictions; missing ACL support cannot disable authorization. [DDS], pp. 21–23, 27–29 |
| CON-API-011 | DDL/entity fields are partial; Chapter 6 describes additional case fields; generic registers call some mutable concepts “immutable derivative” | Case/evidence/review field catalogs; OQ-API-003/007 | Supply complete data/wire schemas. Keep case mutability explicit; do not treat generic register labels as complete schema semantics. [DDS], pp. 13, 24–26, 85–86 |
| CON-API-012 | A2A example uses non-UUID tenant/case placeholders and omits output schema while prose requires declared input/output schemas | API-046; API-COM-006 | Define formal ID representation, required fields, output-schema carrier, and signed attribution. Examples remain placeholders. [DDS], pp. 22, 41, 51, 87 |
| CON-API-013 | Common event field list lacks actor/correlation fields required at durable boundaries | API-COM-006/API-PROC-001 | Define attribution carrier without inventing confirmed envelope properties. [DDS], p. 48 and repeated durable-boundary sections |
| CON-API-014 | Appendix C is a partial event catalog; chapter registers name additional events and sometimes associate them with unrelated reads | Full event inventory/OQ-API-035 | Complete producers/triggers/payloads; distinguish `DeploymentPromoted`/`ReleasePromoted`; do not attach purge/deletion events to export/read by repetition alone. [DDS], pp. 10–80, 87 |
| CON-API-015 | Reference configuration/retention values exist, but §F.2 leaves corporate/provider selections open | Configuration table; API-020/022/023/025/026/036/049/050; `CON-SCR-015` | Define approved configuration and precedence; reference values do not constitute deployment approval. [DDS], pp. 66, 90 |
| CON-API-016 | Case-create boundary uses “within 300 ms” and “under 300 ms” | AC-API-062; `OQ-SCR-031` | Resolve strict test boundary and measurement point. [DDS], pp. 12, 65 |
| CON-API-017 | Earlier screen integration marked the API specification as future work | Later-dependency section of `01_screen_functions.md` | At the appropriate controlled amendment, replace only that dependency pointer with `02_api.md`; other later stages remain ungenerated. No rewrite is performed here. |

### Open-Decision Register

All entries are **Needs confirmation**. No decision owner, deadline, approval, or selected implementation is supplied.

| Open ID | Affected API requirements | Missing decision / contract | Earlier screen linkage and evidence |
|---|---|---|---|
| OQ-API-001 | API authentication profiles; API-015/027/048; P-API-001 | IdP, claim names/values/algorithms, token transport/lifetime, browser versus BFF cookies, session/CSRF/SSE auth | `OQ-SCR-002`; [DDS], p. 21; p. 90 |
| OQ-API-002 | All authorization inventory rows | Complete role/attribute/action matrix, owner/member aliases, approvers/operators/elevated roles, Auditor path, service audiences/grants | `OQ-SCR-003`; [DDS], pp. 11, 18–23, 27, 46, 50, 83 |
| OQ-API-003 | API-COM-001/004; all field catalogs | Full repository wire schemas, property naming/types/limits/nullability/requiredness/defaults/media types | `OQ-SCR-004`; [DDS], pp. 55, 82, 85–87 |
| OQ-API-004 | API-PROC-018; all writes | Key scope/format/fingerprint/TTL/pending replay/concurrency/error caching/permission-changed replay | `SCR-COM-010`; [DDS], pp. 15–17, 25, 54, 90 |
| OQ-API-005 | API-004/005/017/028 and policy/hold writes | Precondition encoding/requiredness/missing-header mapping/ETags/patch format/race handling | `OQ-SCR-018/OQ-SCR-020`; [DDS], pp. 24–25, 45, 83 |
| OQ-API-006 | Public/internal collections | Cursor/envelope/size/order/filter/snapshot/expiry/empty/final-page contracts | `OQ-SCR-011/OQ-SCR-013`; [DDS], pp. 54, 57, 83 |
| OQ-API-007 | API-001–005; API-CASE fields | Case create/read/edit/owner/business-number/state/priority/SLA/closure/reopen contracts | `OQ-SCR-004`–`008`, `018`; [DDS], pp. 12, 24–26, 82–86 |
| OQ-API-008 | API-GAP-001/API-CASE-F16/F17 | Classification correction/results/failure API, reason vocabulary, rights, revision and provenance | `OQ-SCR-007`; [DDS], p. 12 |
| OQ-API-009 | API-006/007; API-PROC-003 | File transport/allowlist/size units/bounds/decompression/OCR/quality/states/quarantine access | `OQ-SCR-009`; [DDS], pp. 10, 30–32, 82, 90 |
| OQ-API-010 | API-008/010; API-EVID fields; API-GAP-003 | Evidence ID mapping, source retrieval/signed URLs/TTL/current grants/anchors/highlights/non-PDF/stale behavior | `OQ-SCR-010`; [DDS], pp. 31, 35, 52, 57 |
| OQ-API-011 | API-009/045; API-PROC-004 | Public search schema/scope/query constraints/results/scores/pagination/insufficient evidence/human route | `OQ-SCR-011`; [DDS], pp. 34–36, 83, 87 |
| OQ-API-012 | API-011/012; API-GAP-005 | Canonical run endpoint, alternate semantics, case-revision binding, rework, any cancel/retry/resume | `OQ-SCR-012`; [DDS], pp. 12–17, 40–42, 46 |
| OQ-API-013 | API-PROC-021–023/026/027 | Runtime/call accounting, invalid-plan bound, waiting/missing approval, recoverable timeout/dependency deadlines | `OQ-SCR-012/OQ-SCR-015`; [DDS], pp. 12, 38–45, 49, 82, 90 |
| OQ-API-014 | API-013–015 | Run/steps projections/order; SSE schema/offsets/history/gaps/expiry/reauthorization/end/errors | `OQ-SCR-013`; [DDS], pp. 40–42, 55, 58 |
| OQ-API-015 | API-016/017/API-GAP-004 | Task detail, approval ID, decision body/enum/hash/rationale/annotations/result/duplicate conflicts | `OQ-SCR-014`; [DDS], pp. 45, 58, 83, 85 |
| OQ-API-016 | API-016/017/policy configuration | Pools/roles/SLA/routing/late and multi-reviewer decisions/self-approval scope | `OQ-SCR-003/OQ-SCR-015`; [DDS], pp. 11, 45, 85, 90 |
| OQ-API-017 | API-PROC-006/API-GAP-006 | Publication control/API, auto-allow path, gate status and decision-to-publication projection | `OQ-SCR-016`; [DDS], pp. 44–46, 57–58 |
| OQ-API-018 | API-GAP-006 | Override endpoint, elevated role, secondary reviewer, reason and outcome protocol | `OQ-SCR-017`; [DDS], p. 46 |
| OQ-API-019 | API-018/019/049/API-GAP-007 | Connector CRUD/auth/revoke/provider/capability/trust/state/concurrency/retry/remediation contracts | `OQ-SCR-019`; [DDS], pp. 27–29, 78, 90 |
| OQ-API-020 | API-020/API-GAP-002 | True policy APIs, field rights, registries, revision/activation/config precedence | `OQ-SCR-020`; [DDS], pp. 24, 37–39, 44–46, 90 |
| OQ-API-021 | API-021 | Audit/detail/filter/cursor/redaction/digest/lineage/Auditor evidence contracts | `OQ-SCR-021`; [DDS], pp. 11, 61–63, 83 |
| OQ-API-022 | API-022 | Usage schema/windows/currency/units/precision/forecast/filters/rollup projection | `OQ-SCR-023`; [DDS], pp. 65–66, 83 |
| OQ-API-023 | API-023/024 | Evaluation inputs/read rights/states/progress/signed fixtures/score/domain/statistical schemas | `OQ-SCR-024`; [DDS], pp. 74–76, 83, 88–89 |
| OQ-API-024 | API-025/026/040/API-GAP-009 | Independent approvals, snapshots/scopes/status/download/receipts/legal-hold races/partial completion | `OQ-SCR-025`; [DDS], pp. 78–80, 83, 89 |
| OQ-API-025 | API-027–029/API-GAP-008 | Principal/membership/provisioning/hold schemas, roles, preconditions, read/status/release APIs | `OQ-SCR-026`; [DDS], pp. 21–23, 61–63, 78 |
| OQ-API-026 | API-032/033 | Design governance schema/rights/impact/version/approval/result/event protocol | `OQ-SCR-027`; [DDS], pp. 8–10 |
| OQ-API-027 | API-036–044; storage/replay/release gaps | Internal schemas/method behavior/services/operators/statuses/purge/replay/release limits and result modes | `OQ-SCR-027`; [DDS], pp. 37–39, 48–53, 64–73 |
| OQ-API-028 | API-045/046 and internal RPC | MCP/A2A/gRPC transport/IDL/requiredness/Citation/grants/output/decline/signing/retry | `SCR-COM-012`; [DDS], pp. 16, 41–42, 55, 87 |
| OQ-API-029 | API-047/API-GAP-012 | Webhook methods/URLs/payload/signature/age/acknowledgment/dedup/retry/admin contracts | `OQ-SCR-027`; [DDS], p. 55 |
| OQ-API-030 | API-COM-004/API-031 | Actual OpenAPI/protobuf versions/repository definitions, compatibility publication/migration process | `SCR-COM-001`; [DDS], pp. 15, 52, 55, 82 |
| OQ-API-031 | API-030/034/035/042 | Health/degraded/capacity schema/probe identity/dependencies/freshness/timeouts/status mapping | `OQ-SCR-028`; [DDS], pp. 18–20, 68–70 |
| OQ-API-032 | Error catalog/all interfaces | Complete per-operation statuses/codes/casing/envelopes/details/retryability/cursor/header/dependency outcomes | `OQ-SCR-029`; [DDS], pp. 13, 25, 49, 54, 84, 89 |
| OQ-API-033 | Performance table/AC-API-062 | Strict latency boundary, measurement/exclusions/load mix/availability and selected quota interpretation | `OQ-SCR-031`; [DDS], pp. 12, 65, 68 |
| OQ-API-034 | External profiles/API-048–050/provider gaps | Approved cloud/regions/search/IdP/model deployments/connector grants/corporate retention/key isolation versus rotation | `OQ-SCR-030`; [DDS], pp. 10, 90 |
| OQ-API-035 | API-COM-006/event catalog/API-015/047 | Event producer/trigger/schema/signature/topic/actor/correlation/dedup/history/SSE/webhook mapping | `OQ-SCR-021/OQ-SCR-013`; [DDS], pp. 22, 48–50, 57–59, 87, 90 |
| OQ-API-036 | API-GAP-010 / screen integration | Summary scope/formulas/API fields and Overview content; whether any approved aggregate endpoint exists | `OQ-SCR-001/OQ-SCR-022`; [DDS], p. 7, illustration; p. 57 |

### Proposal Register

| Proposal ID | Proposal | Approval status / affected requirements |
|---|---|---|
| P-API-001 | `Authorization: Bearer` as the direct REST token carrier | **Unapproved.** OQ-API-001; all P interfaces; does not select against optional BFF cookies. |
| P-API-002 | Partial example JSON mappings for case creation, run acceptance, decision capture, and search | **Unapproved.** OQ-API-003/007/011/015. Confirmed state/content concepts do not confirm the proposed property wrappers. |
| Earlier P-SCR-001/P-SCR-002/P-SCR-003 | Screen aliases/hierarchy, new-case mode, and domain-field/control placement | Remain **unapproved** as recorded in `01_screen_functions.md`. This API specification does not promote them to confirmed screen bindings. |

### Handoffs and Dependencies

| Specification / dependency | Required handoff |
|---|---|
| [`01_screen_functions.md`](01_screen_functions.md) | Preserve SCR/action/event/open-question identifiers. API-001–035 map supported calls, but screen routes, proposed control placement, summaries, and navigation remain unresolved. Record approved future amendments through the conflicts above rather than rewriting the screen specification here. |
| Data Specification | **To be defined in a later stage.** Carry API-CASE/API-EVID catalogs, wire-versus-storage distinctions, UUID/business-number mapping, revision/hash/anchor/Citation structures, classification/reason schemas, event fields, audit/usage/evaluation/export/receipt data, RLS session-reset and workspace-tenancy constraints. Filename is not supplied. |
| Exception Handling Specification | **To be defined in a later stage.** Carry API-COM-007, the failure matrix, OQ-API-032, permanent/transient classification, async versus HTTP failures, conflict recovery, SSE gaps, timeout/review distinction, quarantine/unsupported evidence, legal-hold partial completion, and redaction. Filename is not supplied. |
| Workflow / Business Rule Specification | **To be defined in a later stage.** Resolve priority/SLA, closure/reopen, review routing/expiry/overrides, auto-allow/publication, run waiting/timeout, sync trust/cursor and purge eligibility. |
| Security / Nonfunctional Specification | **To be defined in a later stage.** Resolve full role/action matrix, identity transport, source URL/rendering safety, grant/signature protocols, provider approvals, privacy/redaction, SLO measurements, key-isolation/rotation constraints. |
| Operations Specification | **To be defined in a later stage.** Resolve provisioning, protected internal calls, purge/legal holds/export/deletion, replay/reconciliation, event-history retention, release/failover/health behavior. No job schedule, owner, or console is created by this handoff. |
| Stage 8 architecture-decision consolidation | **To be defined in a later stage.** `08_architecture_decision.md` must consolidate unresolved items only from completed Markdown specifications, linking to `02_api.md` API/OQ/CON identifiers and affected `01_screen_functions.md` SCR/OQ identifiers. This specification records no invented decision, owner, deadline, or approval. |
