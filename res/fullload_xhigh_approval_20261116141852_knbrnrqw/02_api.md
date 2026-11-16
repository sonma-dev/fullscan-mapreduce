# 2. API Specification

## API Inventory and Responsibilities

### Specification Basis

| Item | Definition |
|---|---|
| Output file | `02_api.md` |
| Application | OrionDesk AI |
| Source | `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Baseline | `OD-AI-DDS-001`; release `R1.0`; design revision `1.3` |
| Source authority | Fictional reference architecture; normative for this sample application. Numeric targets are design assumptions, not measured production results. |
| Citation convention | **S** means `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf`. Citations identify original PDF pages and sections. |
| Completed preceding specification | [Screen Function Specification](01_screen_functions.md), including its screen, field, operation, transition, acceptance, conflict, and open-question identifiers. |
| API identifiers | `API-001`–`API-059` are specification identifiers. The source confirms methods, paths, events, and tool identifiers but does not assign these operation numbers. |
| Confirmed | Explicitly supported by S. A confirmed domain field does not automatically establish its public JSON property, request requiredness, or response exposure. |
| Needs confirmation | An unresolved contract. Implementers must not select an undocumented method, path, schema, default, permission, error, or schedule. |
| Proposal | Explicitly suggested design or example; not an approved contract. |
| Later specifications | Data, processing, exception-handling, and other specifications are **To be defined in a later stage**. Stage 8 will consolidate open decisions in `08_architecture_decision.md`; it has not been generated. |

**API-SCP-001 — Confirmed:** External interfaces use REST. Internal HTTP and gRPC contracts are versioned, generated, and independently authorized. OpenAPI governs REST clients; protobuf IDL governs internal gRPC messages.  
**Source:** S, pp. 15–17, §§3.1–3.3; pp. 54–56, §§15.1–15.3.

**API-SCP-002 — Confirmed:** The browser enters through the edge API. The orchestrator has no direct database credentials and uses narrow scoped interfaces. Internal endpoints in this specification are not automatically browser-accessible.  
**Source:** S, p. 9, §1.3.1; pp. 15–16, §§3.1.1–3.2.1.

**API-SCP-003 — Confirmed:** The API layer must preserve permitted evidence, immutable source versions, deterministic approval gates, tenant isolation, and idempotent cross-service writes. Untrusted evidence or model responses cannot authorize tools, alter tenant scope, change approvals, or bypass policy.  
**Source:** S, p. 7, Architecture at a Glance; pp. 15–17, Chapter 3; pp. 44–46, Chapter 12.

### Authentication and Authorization Profiles

These profiles apply to every inventory entry that references them.

| Profile | Confirmed authentication and authorization | Needs confirmation |
|---|---|---|
| **I — Interactive/public API** | Authenticated principal and tenant. OIDC authorization-code flow with PKCE for interactive sessions. Access tokens carry issuer, audience, expiry, subject, and tenant. Reject unexpected algorithms and missing tenancy claims. Evaluate resource authorization independently of screen visibility. | Identity provider; exact audience and claim names; accepted algorithms; token/session transport; session lifetime; cookie/BFF selection. Earlier `OQ-001`–`OQ-003`; `API-OQ-001`. |
| **S — Internal service API** | TLS; mTLS-authenticated HTTP or gRPC for internal calls; service audience checks; scoped IAM/service credentials; independently authorized resource and tenant access. Prefer managed workload identity where supported; do not share service identity between deployment units. | Exact caller identities, audiences, permission scopes, HTTP/gRPC selection, and credential configuration. `API-OQ-002`. |
| **O — Operational interface** | Apply authenticated, scoped operational/service access. The source does not establish anonymous access merely because an endpoint is used for health, metrics, capacity, replay, or release operations. | Probe authentication and tenant-context handling, exact operational roles, network exposure, and safe response projection. `API-OQ-002`, `API-OQ-018`. |
| **T — Tool/agent interface** | Scoped service credentials and separate capability authorization. Invocation depends on principal, workspace policy, tool scope, and data classification. Discovery is not permission. | Protocol transport, credential bindings, full schemas, and rejection representations. `API-OQ-023`. |
| **W — Optional outbound webhook** | Signed delivery; recipient verifies signature and event age. Failure cannot roll back the case transition. | Method, URL registration, signature algorithm and headers, allowable age, payload, and response/acknowledgment contract. `API-OQ-024`. |

**API-AUTH-001 — Confirmed:** Resource access combines role, tenant, workspace membership, case sensitivity, originating document ACL, requested action, and segregation-of-duties constraints. Domain services re-evaluate resource attributes within the transaction.  
**Source:** S, pp. 21–23, §§5.2–5.3. Links: `SF-AUTH-001`, `SF-PRE-003`.

**API-AUTH-002 — Confirmed:** A foreign-tenant identifier returns the same class of not-found response as an absent identifier. Denials retain the principal and denied resource class in audit evidence without revealing private resource existence.  
**Source:** S, p. 23, §5.3.2; p. 89, `TST-003`. Link: `SF-AUTH-002`.

**API-AUTH-003 — Confirmed:** Tenant identity participates in every storage predicate. Tenant-owned rows use tenant-scoped database context and RLS; background jobs carry immutable tenant identity in signed envelopes. Connection-pool scoped session variables must reset after every transaction. Workspace-tenancy membership must be enforced by foreign keys or controlled write procedures.  
**Source:** S, p. 22, §5.3.1; pp. 51–53, Chapter 14; p. 86, Appendix B.2.

**API-AUTH-004 — Confirmed:** The browser does not store long-lived refresh tokens in local storage. A BFF *can* issue secure, HttpOnly, SameSite cookies; that architecture is not selected by the source. Credentials must not appear in traces or model prompts.  
**Source:** S, p. 21, §5.1.2. Link: `SF-PRE-002`.

**API-AUTH-005 — Needs confirmation:** `Owner`, `Member`, and `approver` are catalog scopes, not established baseline roles. The mapping of Workspace Admin to `Admin`, case ownership to `Owner`, and role membership to `Member` remains unresolved. An `Admin` is not implicitly a Reviewer or an independent approver.  
**Source:** S, p. 11, §2.1; p. 22, §5.2.1; p. 83, Appendix A.2. Earlier `SF-CON-008`, `OQ-003`; `API-OQ-001`.

### Public Business API Inventory

**Behavior notation:** “Asynchronous” means the request accepts durable work, not that the business work has completed. “Synchronous inquiry” identifies a read interface; it does not establish an undocumented success status or asynchronous fallback schema.

| API ID | Purpose and responsible boundary | Calling screen/operation | Behavior | Method and path | Authentication / authorization | Source |
|---|---|---|---|---|---|---|
| API-001 | Create a case; Case Service | `SCR-001-A03` | Synchronous creation; classification follows asynchronously | `POST /v1/cases` | I; `Analyst` | S, pp. 11–13, Chapter 2; p. 83, A.2 |
| API-002 | Read current authorized case revision | `SCR-001-A04`, `SCR-002-A01` | Synchronous inquiry | `GET /v1/cases/{caseId}` | I; `Analyst / Reviewer` | S, p. 83, A.2 |
| API-003 | Mutate metadata or execute a guarded case transition | `SCR-002-A02`, `SCR-002-A04` | Synchronous transaction | `PATCH /v1/cases/{caseId}` | I; `Owner`; role/revision/approval guards | S, pp. 24–26, Chapter 6; p. 83, A.2 |
| API-004 | Accept attachment ingestion | `SCR-002-A05` | Asynchronous | `POST /v1/cases/{caseId}/attachments` | I; `Analyst` | S, pp. 30–32, Chapter 8; p. 83, A.2 |
| API-005 | Start a bounded case-scoped AI run | `SCR-002-A06`; progress on `SCR-004` | Asynchronous | `POST /v1/cases/{caseId}/runs` | I; `Analyst`; case access, admission, tool, and policy guards | S, p. 12, §2.2.2; pp. 40–42, Chapter 11; p. 83, A.2 |
| API-006 | Read persisted run stages and evidence metadata | `SCR-004-A01`, refresh under `SCR-004-A03` | Synchronous inquiry | `GET /v1/runs/{runId}` | I; `Analyst / Reviewer` | S, pp. 16–17, Chapter 3; p. 83, A.2 |
| API-007 | Stream scoped run progress | `SCR-004-A02`–`A03`; `SCR-002-A06` | Long-lived SSE | `GET /v1/streams/runs/{runId}` | I; `Analyst / Reviewer`; scope also applies to backfill | S, p. 55, §15.2.1; p. 83, A.2 |
| API-009 | Start incremental connector sync | `SCR-006-A02` | Asynchronous | `POST /v1/connectors/{connectorId}/sync` | I; `Admin`; provisioning, credential, workspace, and quota guards | S, pp. 27–29, Chapter 7; p. 78, §22.1.1; p. 83, A.2 |
| API-010 | Search permitted lexical and semantic evidence | `SCR-003-A02`; degraded evidence work | Synchronous retrieval | `POST /v1/search` | I; `Member`; originating source ACL | S, pp. 34–36, Chapter 9; p. 83, A.2 |
| API-011 | Query immutable audit events | `SCR-008-A01`–`A02` | Synchronous, cursor-paginated inquiry | `GET /v1/audit/events` | I; `Auditor`; tenant and redacted-content scope | S, pp. 61–63, Chapter 17; p. 83, A.2 |
| API-012 | Read costs, quotas, and trend estimates | `SCR-010-A01` | Synchronous inquiry | `GET /v1/usage` | I; `Admin` | S, pp. 64–66, Chapter 18; p. 83, A.2 |
| API-013 | Start frozen benchmark evaluation | `SCR-010-A02` | Asynchronous | `POST /v1/evaluations` | I; `Admin` | S, pp. 74–76, Chapter 21; p. 83, A.2 |
| API-014 | Request controlled export | `SF-SCP-007`; placement under `SCR-008-A05` unresolved | Asynchronous | `POST /v1/workspaces/{workspaceId}/export` | I; `Admin + approver`; two independent approval checks | S, pp. 78–80, Chapter 22; p. 83, A.2 |
| API-015 | Request legal-hold-safe deletion | `SF-SCP-007`; placement unresolved | Asynchronous | `POST /v1/workspaces/{workspaceId}/delete` | I; `Admin + approver`; two independent approval checks | S, pp. 78–80, Chapter 22; p. 83, A.2 |
| API-016 | List authorized cases | `SCR-001-A01`–`A02` | Synchronous, cursor-paginated inquiry | `GET /v1/cases?cursor=...` | I; list-access scope Needs confirmation | S, pp. 57–59, Chapter 16 |
| API-017 | Close a case and preserve approved lineage | `SCR-002-A07` | Mutation confirmed; synchronous/asynchronous result Needs confirmation | `POST /v1/cases/{caseId}/close` | I; exact actor scope and closing edge Needs confirmation | S, pp. 24–26, Chapter 6 |
| API-018 | Read document-processing status | Attachment status under `SCR-002` | Synchronous inquiry | `GET /v1/documents/{documentId}/status` | I; exact read scope Needs confirmation | S, pp. 30–32, Chapter 8 |
| API-019 | Read persisted run steps/checkpoints | `SCR-004-A01` | Synchronous inquiry | `GET /v1/runs/{runId}/steps` | I; exact scope Needs confirmation; do not infer from API-006 | S, pp. 40–42, Chapter 11 |
| API-020 | Validate and commit publication gate | `SCR-002-A09`; consequence of `SCR-005-A03` | Transactional gate/event-driven behavior; no public endpoint confirmed | Method/path **Needs confirmation** if an independently callable interface is required | Trusted service invocation and current resource/policy authorization; exact scope Needs confirmation | S, pp. 12–13, Chapter 2; pp. 44–46, Chapter 12 |
| API-021 | Resolve authorized evidence | `SCR-003-A03` | Synchronous inquiry | `GET /v1/evidence/{evidenceId}` | I; current evidence/source authorization; exact catalog scope Needs confirmation | S, pp. 34–36, Chapter 9 |
| API-022 | Read case evidence for inspection/review | `SCR-003-A01`; `SCR-005-F07` | Synchronous inquiry | `GET /v1/cases/{caseId}/evidence` | I; current case and evidence authorization; exact scope Needs confirmation | S, pp. 57–59, Chapter 16 |
| API-023 | Read policy-routed review queue | `SCR-005-A01`–`A02` | Synchronous inquiry | `GET /v1/review-queue` | I; authorized reviewer/pool scope; full role/assignment predicate Needs confirmation | S, pp. 44–46, Chapter 12 |
| API-024 | Record hash-bound approval/rejection | `SCR-005-A03`–`A04` | Synchronous decision transaction; publication is separately guarded | `POST /v1/approvals/{approvalId}/decision` | I; `Reviewer`; hash, role, task, and separation-of-duties guards | S, pp. 44–46, Chapter 12; p. 83, A.2 |
| API-025 | Read connector sync runs | `SCR-006-A01` | Synchronous inquiry | `GET /v1/connectors/{connectorId}/runs` | I; exact read scope Needs confirmation | S, pp. 28–29, Chapter 7 |
| API-026 | Read model deployment catalog | `SCR-007-A03` | Synchronous inquiry | `GET /v1/model-catalog` | I; scope and allowed-deployment projection Needs confirmation | S, pp. 37–39, Chapter 10 |
| API-027 | Read authenticated principal context | All screens; `SF-PRE-001`–`003` | Synchronous inquiry | `GET /v1/me` | I; authenticated principal | S, pp. 21–23, Chapter 5 |
| API-028 | Update workspace membership | `SF-SCP-008`; screen placement unresolved | Mutation; response behavior Needs confirmation | `PUT /v1/workspaces/{workspaceId}/members` | I; exact membership-administration role Needs confirmation | S, pp. 21–23, Chapter 5 |
| API-029 | Create a security/legal hold | `SF-SCP-008`; screen placement unresolved | Mutation; response behavior Needs confirmation | `POST /v1/security/holds` | I; exact hold-administration scope Needs confirmation | S, pp. 61–63, Chapter 17 |
| API-030 | Submit design-governance decision/change | `SF-SCP-008`; no confirmed screen | Mutation; long-running allocation possible, exact result Needs confirmation | `POST /v1/design-decisions` | I; exact design-governance scope Needs confirmation | S, pp. 8–10, Chapter 1 |
| API-031 | Read design baseline | `SF-SCP-008`; no confirmed screen | Synchronous inquiry | `GET /v1/design-baselines/{id}` | I; exact read scope Needs confirmation | S, pp. 9–10, Chapter 1 |
| API-032 | Request a run through the Chapter 3 route | Browser/edge flow; relationship to `SCR-002-A06` unresolved | Run-request behavior; exact response Needs confirmation | `POST /v1/runs` | I; exact scope and relationship to API-005 Needs confirmation | S, pp. 15–17, Chapter 3 |
| API-045 | Read evaluation/result scorecard | `SCR-010-A03` | Synchronous inquiry | `GET /v1/evaluations/{evaluationId}` | I; exact read scope Needs confirmation | S, pp. 74–76, Chapter 21 |

### Internal, Operational, and Protocol Inventory

| API ID | Purpose / caller | Screen relationship | Behavior | Method/path or protocol identifier | Authentication / authorization | Source |
|---|---|---|---|---|---|---|
| API-008 | Controlled generation; AI orchestration/gateway boundary | Indirectly supports `SCR-002-A06`, `SCR-004-A04`, and review metadata | Generation request; exact synchronous/asynchronous response Needs confirmation | `POST /internal/model/generate` | S; scoped context, allowed deployment, quota, classification, and tool-authority boundaries | S, pp. 37–39, Chapter 10 |
| API-033 | Inspect durable workflow; internal services/operators | No direct browser contract; related to `SCR-004-A06` | Synchronous inquiry | `GET /internal/workflows/{runId}` | S/O; exact scope Needs confirmation | S, pp. 48–50, Chapter 13 |
| API-034 | Replay dead letters; authorized operator | `SCR-004-A06` is unresolved, not an ordinary Analyst control | Controlled replay; exact HTTP result Needs confirmation | `POST /internal/deadletters/{id}/replay` | S/O; operator reason, dry-run validation, and scope limit | S, pp. 48–50, Chapter 13 |
| API-035 | Read stored document/version objects; domain services | May support evidence delivery internally; not confirmed browser route | Synchronous inquiry | `GET /internal/storage/documents/{id}` | S; tenant/storage/source access predicates | S, pp. 51–53, Chapter 14 |
| API-036 | Execute storage purge; retention/lifecycle services | Indirect lifecycle behavior; no confirmed screen | Purge workflow; exact result Needs confirmation | `POST /internal/storage/purge` | S/O; retention eligibility, legal holds, and tenant scope | S, pp. 51–53, Chapter 14 |
| API-037 | Obtain REST contract; clients/contract tooling | No dedicated screen confirmed | Synchronous inquiry | `GET /v1/openapi.json` | I/O; audience requirement retained; exact access scope Needs confirmation | S, pp. 54–56, Chapter 15 |
| API-038 | Liveness inquiry; deployment/monitoring systems | No screen confirmed | Synchronous inquiry | `GET /v1/health/live` | O; probe authentication/exposure Needs confirmation | S, pp. 18–20, Chapter 4 |
| API-039 | Readiness inquiry; deployment/monitoring systems | No screen confirmed | Synchronous inquiry | `GET /v1/health/ready` | O; probe authentication/exposure Needs confirmation | S, pp. 18–20, Chapter 4 |
| API-040 | Operational metrics inquiry | No direct browser integration confirmed | Synchronous inquiry | `GET /internal/metrics` | S/O; exact scope/projection Needs confirmation | S, pp. 64–66, Chapter 18 |
| API-041 | Read degraded-mode information | Supports `SF-SCP-006`, `SF-SHELL-F06`; exact binding unresolved | Synchronous inquiry | `GET /v1/system/degraded-modes` | I/O; exact read scope Needs confirmation | S, pp. 68–70, Chapter 19 |
| API-042 | Read capacity/admission information | No direct browser contract confirmed | Synchronous inquiry | `GET /internal/capacity` | S/O; exact scope Needs confirmation | S, pp. 68–70, Chapter 19 |
| API-043 | Submit release operation; release tooling/operators | No confirmed screen | Controlled mutation/promotion; exact result Needs confirmation | `POST /internal/releases` | S/O; build verification, rollout gates, and sign-off | S, pp. 71–73, Chapter 20 |
| API-044 | Read release record | No confirmed screen | Synchronous inquiry | `GET /internal/releases/{releaseId}` | S/O; exact read scope Needs confirmation | S, pp. 71–73, Chapter 20 |
| API-046 | Typed permitted-document retrieval; Research Agent/approved MCP server | Indirectly supports evidence/run screens | Read-only tool request/reply | `knowledge.search@v1`; HTTP method/path **Needs confirmation** | T; `read:permitted_documents`, tenant-scoped | S, pp. 41–42, Chapter 11; p. 87, C.2 |
| API-047 | Scoped agent-to-agent task handoff | Indirect run trace/checkpoint behavior | Task handoff; receiving agent may decline | A2A task envelope; HTTP method/path **Needs confirmation** | T; separate capability authorization | S, p. 41, §11.2.2; p. 87, C.2 |
| API-048 | Optional outbound notification webhook | No webhook-management screen confirmed | Asynchronous, signed, retried delivery | Method/recipient URL **Needs confirmation** | W | S, p. 55, §15.2.2 |

### Supported Capabilities Without Complete API Contracts

These entries prevent missing interfaces from being silently invented. Their capabilities are source-supported, but an independently callable API is not established unless stated below.

| API ID | Capability / affected screen operation | Method/path, caller, and behavior status | Required boundary | Source / adjacent question |
|---|---|---|---|---|
| API-049 | Read workspace settings; `SCR-007-A01` | Method/path and response **Needs confirmation** | Authorized workspace administrative context; configuration revision | S, p. 24, §6.1.1; `API-OQ-014`, earlier `OQ-020` |
| API-050 | Update workspace settings; `SCR-007-A02` | Method/path and result **Needs confirmation** | Revision precondition and durable audit; exact field rights unresolved | S, p. 24, §6.1.1; `API-OQ-014` |
| API-051 | Correct classification labels; `SCR-002-A03` | Method/path and result **Needs confirmation** | Correction reason code; retain classification provenance | S, p. 12, §2.2.1; `API-OQ-005` |
| API-052 | Reopen closed case; `SCR-002-A08` | Method/path, target state, and result **Needs confirmation** | Explicit new revision; immutable prior approved lineage | S, p. 25, §6.2.1; `API-OQ-004` |
| API-053 | Authorized override; `SCR-005-A06` | Method/path and result **Needs confirmation** | Elevated role, secondary reviewer, audited reason | S, p. 46, §12.3.2; `API-OQ-010` |
| API-054 | Revoke connector credentials; `SCR-006-A03` | Operator capability confirmed; method/path **Needs confirmation** | Workspace-scoped secrets; queued jobs fail safely | S, p. 27, §7.1.2; `API-OQ-011` |
| API-055 | Reauthorize connector; `SCR-006-A04` | Flow, method/path, provider URL, and permissions **Needs confirmation** | No credential leakage; do not infer OAuth provider details | S, p. 27, §7.1.2 provides reauth-required outcome, not this flow; `API-OQ-011` |
| API-056 | Provision tenant/workspace | Workflow confirmed; method/path/result **Needs confirmation** | Idempotent provisioning; incomplete state visible and blocks sync | S, p. 78, §22.1.1; `API-OQ-016` |
| API-057 | Deliver public source content / signed URL | Delivery capability confirmed; public method/path/result **Needs confirmation** | Current access, immutable cited version, opaque names, short-lived signed URLs | S, p. 52, §14.3.1; p. 57, §16.1.2; `API-OQ-008` |
| API-058 | Dashboard/summary aggregates; `SCR-009-A01`–`A02`, `SF-SHELL-F03`–`F07` | Fields are illustrated; backing method/path, formulas, and refresh behavior **Needs confirmation** | Authorized aggregate scope; no invented “open” or coverage formula | S, p. 7, Reference UI A; p. 14, Figure 2.2; `API-OQ-025` |
| API-059 | Browser notification state/delivery; `SF-NAV-007` | `Notification` component exists; channels and API **Needs confirmation** | Scoped, safe notification contents | S, pp. 58–59, §§16.2.2–16.4; `API-OQ-025` |

### Explicit API Boundaries

| Category | Status / boundary | Source |
|---|---|---|
| Physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing, agent administrative cloud permissions | **Out of scope:** explicitly excluded. A financial-impact category remains a valid policy input. | S, p. 9, §1.2.1; p. 44, §12.1.1 |
| Application-hosted GPU inference | **Out of scope:** model providers are external dependencies. | S, p. 19, §4.2.1 |
| Cross-region active/active mutation, OCR beyond English, customer-managed model weights | **Deferred from this baseline**, not enabled through undocumented API options. | S, p. 10, §1.3.2 |
| Secrets and internal model prompts in export | **Out of scope for export contents:** explicitly excluded. | S, p. 79, §22.3.1 |
| End-user cancel/pause/run-retry, bulk approval, list filters, webhook subscription administration | **Needs confirmation**, not Out of scope. No complete source contract exists. | S, Chapters 11–16; earlier `OQ-006`, `OQ-011`, `OQ-013`, `OQ-024` |

## Interfaces by API

### Shared Parameter and Response Conventions

**API-IF-001 — Confirmed:** Preserve source methods and paths literally, including camel-case route placeholders. Source record names do not establish matching JSON property names. `caseId` in a route and `case_id` in a stored entity or MCP payload are different contract locations.  
**Source:** S, pp. 83, 85, and 87, Appendices A.2, B.1, and C.2.

**API-IF-002 — Confirmed:** Public timestamps use RFC 3339; server/event time is UTC. Locale changes presentation, not durable API representations or event ordering.  
**Source:** S, p. 54, §15.1.1; p. 59, §16.3.2.

For the following tables:

- **Semantic required** means the source requires the operation to carry or return that information, but its transport property and schema remain unresolved.
- **Record required** means mandatory stored information; public request/response requiredness is not thereby confirmed.
- **Needs confirmation** includes nullable status, length, precision, encoding, and default unless a source value is explicitly stated.
- No unspecified request body is assumed to be `{}`.
- No undocumented `Location`, operation-status URL, response wrapper, total count, or pagination field is mandatory.
- Every API inherits authentication, tenant/resource checks, trace/correlation propagation, safe errors, validation, and applicable consistency rules below.

#### Shared Path Parameters

| Name | APIs | Meaning / type | Required | Constraints | Default |
|---|---|---|---|---|---|
| `caseId` | API-002–005, 017, 022 | Case identifier; logical `UUID`; source identifier-generation policy is UUIDv7 | Yes, in these routes | Tenant/workspace/resource guarded. UUID lexical parsing and acceptance of other UUID versions Needs confirmation. Not the illustrated `OD-2026-...` business reference. | None |
| `runId` | API-006–007, 019, 033 | Run identifier; logical UUID | Yes | Tenant, run, case, and current caller scope | None |
| `connectorId` | API-009, 025 | Connector identifier; logical UUID policy | Yes | Authorized connector/workspace context | None |
| `approvalId` | API-024 | Approval/task route identifier; exact mapping to `approval_tasks.id` Needs confirmation | Yes | Authorized task, exact artifact, separation of duties | None |
| `workspaceId` | API-014–015, 028 | Workspace identifier; logical UUID | Yes | Tenant membership; export/delete operation scope still unresolved | None |
| `documentId` | API-018 | Document identifier; logical UUID | Yes | Document/source access; version-selection behavior Needs confirmation | None |
| `evidenceId` | API-021 | Evidence identifier; exact mapping to `EvidenceSet` or another evidence resource Needs confirmation | Yes | Opaque resolution; current source ACL and anchor verification | None |
| `evaluationId` | API-045 | Evaluation identifier; logical identifier policy | Yes | Tenant/evaluation authorization | None |
| `releaseId` | API-044 | Release identifier; exact wire format Needs confirmation | Yes | Authorized operational scope | None |
| `id` | API-031 | Design baseline identifier; exact entity mapping Needs confirmation | Yes | Tenant/baseline authorization | None |
| `id` | API-034 | Dead-letter entry identifier; exact format Needs confirmation | Yes | Operator and replay-scope authorization | None |
| `id` | API-035 | Stored document/object identifier; document-versus-version mapping Needs confirmation | Yes | Tenant, workspace, immutable version, object role, and source permissions | None |

**Source:** S, endpoint registers in Chapters 1, 6–16, 20–21; p. 51, §14.1.1; pp. 83–87, Appendices A–C.  
**Open contract:** `API-OQ-003`, `API-OQ-008`, `API-OQ-010`, `API-OQ-019`; earlier `OQ-007`, `OQ-018`.

#### Shared Headers and Trusted Context

| Name / concept | Location | Meaning / type | Required | Constraints and default | Status / source |
|---|---|---|---|---|---|
| Authentication token | Header/session transport Needs confirmation | Authenticated identity and tenant context | Authentication required | Audience, issuer, expiry, subject, tenant, and algorithm checks. Exact claim names and transport unresolved. No default identity. | Confirmed semantics; S, p. 21, §5.1.1 |
| `Authorization: Bearer ...` | Request header | Conventional token carriage | Needs confirmation as selected transport | **Proposal** for examples, not proof that BFF cookies are excluded | S, p. 21, §§5.1.1–5.1.2; `API-OQ-001` |
| `Idempotency-Key` | Request header | Opaque operation key; exact type encoding/length Needs confirmation | Required for job-creating POSTs; also confirmed for case creation | Actor/request fingerprint binding; same key and identical payload returns original outcome. No generated default is specified. | S, p. 25, §6.2.2; p. 54, §15.1.2; p. 83, A.2 |
| `If-Match` | Request header | Case revision condition; source case revision is `BIGINT` | Required for API-003; case mutation conditions also apply to API-017 | ETag/revision syntax, quoting, missing-header outcome, and wildcard handling Needs confirmation. No implicit “latest” default. | S, p. 25, §6.2.2; p. 83, A.2; `API-OQ-003`–`004` |
| `Last-Event-ID` | API-007 request header | Last received SSE offset | Required when resuming using this mechanism; initial request has no prior offset | Monotonic server offsets; type, syntax, retention, invalid/expired handling Needs confirmation | S, p. 55, §15.2.1; `API-OQ-006` |
| `Retry-After` | Response header / provider response | Retry guidance | Required for throttled new-run clients; connector workers honor it when supplied by providers | Exact representation and admission delay calculation Needs confirmation; no numeric default | S, p. 28, §7.3.1; p. 69, §19.2.1 |
| `trace_id`, `correlation_id` | Cross-boundary context; HTTP header mapping Needs confirmation | Request and workflow correlation | Every request carries both concepts | Must remain independent of provider trace identifiers; exact names/types and generation policy unresolved | S, p. 16, §3.3.1; p. 64, §18.1.1 |
| `tenant_id`, `revision`, `actor_id`, `occurred_at`, correlation context | Durable mutation records; not automatically public body fields | Trusted tenancy, actor, revision, occurrence, and lineage | Required where durable state changes | User content cannot authorize changes to trusted identity or tenancy; transport and non-case revision types unresolved | S, Chapters 1–22, interface-boundary requirements; earlier `SF-PRE-006` |
| `Content-Type: application/json` | Error response | Canonical error media type | Confirmed for source error example | General request/success media types require OpenAPI definition | S, p. 84, A.3 |

#### Shared Cursor and Asynchronous Result Contracts

| Requirement ID | Confirmed contract | Needs confirmation |
|---|---|---|
| API-PAGE-001 | Public APIs use cursor pagination; API-016 explicitly uses query parameter `cursor`; API-011 returns a cursor-paginated immutable log. | Cursor names for other APIs; type/encoding; initial omission/empty representation; page size; sorting; filters; direction; expiry; snapshot semantics; total count; response cursor property. S, p. 54, §15.1.1; pp. 57–59, Chapter 16; p. 83, A.2. `API-OQ-003`, `007`, `010`, `012`. |
| API-ASYNC-001 | API-004, 005, 009, 013, 014, and 015 return `202` for accepted durable work. | Operation-identifier property, status URL, lifecycle schema, result URL, and cancellation. S, p. 83, A.2. |
| API-ASYNC-002 | On dependency unavailability, callers receive a documented retryable error or a persisted asynchronous job identifier, never ambiguous success. | Which fallback applies per API; error status/code; asynchronous receipt shape for otherwise synchronous APIs. This statement does not establish `202` for every read endpoint. S, Chapters 1–22, interface-boundary requirements. `API-OQ-017`. |
| API-ASYNC-003 | Run creation is immediate and progress is reconstructed from server state; `202` is not publication. | Exact receipt mapping to `runId`, initial response properties, and refresh instructions. S, p. 58, §16.2.1. |

### API-001, API-002, API-003, and API-016 — Case Creation, Reading, Mutation, and Listing

#### Request Contracts

| API | Location / name | Meaning / type | Required | Constraints / default | Source and question |
|---|---|---|---|---|---|
| API-001 | Header `Idempotency-Key` | Create-operation key | Yes | Shared idempotency contract; case-key outcome binding for 24 hours | S, p. 25, §6.2.2; p. 83, A.2 |
| API-001 | Body: workspace context; domain `workspace_id` | Target workspace; stored `UUID` | Workspace relationship record-required; request requiredness Needs confirmation | Authorized workspace; selection/default and body property unresolved | S, p. 86, B.2; `API-OQ-003` |
| API-001, 003 | Body: title | Case title; semantic text; wire type/length Needs confirmation | Needs confirmation | Blank/trim/rich-text rules unresolved; no default confirmed | S, p. 24, §6.1.2; earlier `SCR-002-F03`; `API-OQ-003` |
| API-001, 003 | Body: description/business context | Semantic text/context; structure and length Needs confirmation | Needs confirmation | Validate as untrusted user input; no default confirmed | S, p. 12, §2.2.1; p. 24, §6.1.2 |
| API-001, 003 | Body: impact, urgency | Explicit priority inputs; types/catalogs Needs confirmation | Needs confirmation | Priority derived from both, not model output alone; matrix/default unresolved | S, p. 25, §6.3.1; `API-OQ-005` |
| API-001, 003 | Body: owner | Principal reference; wire type/property Needs confirmation | Record exists; input requiredness/editability Needs confirmation | Eligible owner list, assignment rights, and default unresolved | S, p. 24, §6.1.2; earlier `OQ-003`, `OQ-007` |
| API-001, 003 | Body: sensitivity; domain `sensitivity` | Stored `TEXT`; classes `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` | Record-required; input requiredness Needs confirmation | Database default `INTERNAL`; classification change/lowering rights unresolved. Run controls additionally obey API-CLS-001. | S, pp. 62 and 86, §17.2.1 and B.2 |
| API-003 | Path `caseId` | Case identity | Yes | Shared path contract | S, p. 83, A.2 |
| API-003 | Header `If-Match` | Current revision condition | Yes | Shared revision contract; no implicit latest revision | S, p. 25, §6.2.2 |
| API-003 | Body: supported metadata patch | Metadata changes; patch media type/structure Needs confirmation | Payload required for mutation; field set Needs confirmation | Do not select JSON Patch or Merge Patch by assumption. Identity, tenancy, history, approved pointer, and status are not unrestricted editable fields. | S, pp. 24–26, Chapter 6; `API-OQ-003` |
| API-003 | Body: target status; domain `status` | Requested guarded state transition; stored `TEXT` | Required for state-changing variant; transport Needs confirmation | Only confirmed normal edges below; closing/reopening separate incomplete contracts | S, p. 25, §6.2.1; `API-OQ-004` |
| API-002 | Path `caseId` | Current case inquiry | Yes | Shared path contract | S, p. 83, A.2 |
| API-016 | Query `cursor` | Page continuation | Continuation supported; initial requiredness Needs confirmation | Opaque server cursor; no page-size default supplied | S, p. 57, §16.1.1 |
| API-002, 016 | Additional query/body parameters | No additional names supplied | Needs confirmation | Do not add history version, search, status filter, sort, bulk, or page-size parameters as confirmed contracts | Earlier `OQ-006`, `OQ-007`; `API-OQ-003` |

#### Successful Responses

| API | HTTP status | Response information / type | Requiredness and constraints |
|---|---|---|---|
| API-001 | **`201` Confirmed** | New case identifier; logical UUID; property/location Needs confirmation | Identifier semantic required. Created case begins `NEW`, revision defaults to `1`, sensitivity defaults to `INTERNAL` in reference DDL. Their presence in the receipt is not fully specified. |
| API-002 | **`200` Confirmed** | Authorized current case revision | Current revision semantic required; complete JSON schema Needs confirmation. |
| API-003 | **`200` Confirmed** | Accepted metadata/state mutation and monotonic revision | Exact updated-resource versus mutation-result schema Needs confirmation. No silent overwrite. |
| API-016 | Success status **Needs confirmation** | Authorized case page and pagination continuation | Row schema, collection wrapper, end-of-list representation, and cursor field Needs confirmation. |

**Source:** S, p. 12, §§2.2.1–2.3.1; p. 25, §6.2; pp. 57–59, Chapter 16; pp. 83 and 86, A.2 and B.2.

The following case information must remain represented in the domain contract and must not be discarded because Appendix B.2 is abbreviated.

| Domain information | Source type / format | Required or default | Public response exposure |
|---|---|---|---|
| `id`, `tenant_id`, `workspace_id` | `UUID`; generated identifiers use UUIDv7 policy | Record-required; no client-created default | Exact public fields and trusted-context projection Needs confirmation |
| `status` | `TEXT`; `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED` | Record-required; initial `NEW` | Current case status supported; property schema Needs confirmation |
| `revision` | `BIGINT`, monotonic | Record-required; default `1` | Needed for revision-safe operations; JSON integer/string selection Needs confirmation |
| `sensitivity` | `TEXT` | Record-required; database default `INTERNAL` | Field exists; exact response/edit rights Needs confirmation |
| `created_at`, `updated_at` | `TIMESTAMPTZ`; RFC 3339 API timestamp | Record-required; DDL default `now()` | Response inclusion Needs confirmation |
| Title, description, priority, owner, current approved result | Exact storage/wire types Needs confirmation | Stored domain fields | Complete schema, nullable status, and approved-result representation Needs confirmation |
| Classification labels, confidences, provenance | Structured asynchronous output; exact types Needs confirmation | Attached by classifier | Inquiry projection and label-correction contract Needs confirmation |
| Contractual deadlines / advisory breach prediction | Deadline uses business calendar/workspace timezone; prediction schema unresolved | Domain behavior supported | API fields Needs confirmation; advisory prediction cannot mutate contractual deadlines |

**Source:** S, pp. 12 and 24–26, §§2.2.1 and 6.1–6.3; p. 51, §14.1.1; p. 86, B.2. Links: `SCR-002-F01`–`F18`; `API-OQ-003`, `API-OQ-005`.

#### API-003 Confirmed Normal Transition Contract

| Earlier transition ID | From | To | Confirmed guards / remaining details |
|---|---|---|---|
| `SCR-002-T01` | `NEW` | `TRIAGED` | Current revision; actor/action authorization; applicable role and approval requirements. Detailed trigger and actor mapping Needs confirmation. |
| `SCR-002-T02` | `TRIAGED` | `IN_PROGRESS` | Same shared guards; detailed actor/trigger Needs confirmation. |
| `SCR-002-T03` | `IN_PROGRESS` | `PENDING_APPROVAL` | Same shared guards plus applicable evidence/policy/task requirements; linkage Needs confirmation. |
| `SCR-002-T04` | `IN_PROGRESS` | `RESOLVED` | Evidence and satisfied approval policy remain obligatory; this edge is not an approval bypass. |
| `SCR-002-T05` | `PENDING_APPROVAL` | `RESOLVED` | Applicable exact-hash approval and separation-of-duties requirements; decision-to-case transition linkage Needs confirmation. |
| `SCR-002-T06` | `PENDING_APPROVAL` | `IN_PROGRESS` | Authorized rework transition; do not assume every rejection automatically executes this edge. |

**Source:** S, p. 25, §6.2.1; pp. 44–46, Chapter 12; p. 82, A.1.

**Needs confirmation — API-OQ-004:** Complete missing edge-specific actor/trigger/approval rules. Do not replace these six confirmed edges with an entirely TBD matrix, add a normal edge, infer `RESOLVED → CLOSED`, or permit an ordinary in-place exit from `CLOSED`.

### API-017 — Close Case

| Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|
| Path `caseId` | Case identity | Yes | Shared resource guard; no default |
| Revision condition; `If-Match` mechanism from case mutation contract | Current case revision | Revision condition confirmed; exact close-header encoding Needs confirmation | Stale writes rejected; no default latest revision |
| Body: closure request | Closure intent and any required supporting information | Body shape/required fields Needs confirmation | Allowed originating state, actor, approval guards, and whether a body is required are unresolved |
| Response: closure outcome / snapshot reference | Approved answer, cited immutable document versions, reviewer decisions, and lineage | Snapshot behavior required; response fields/types Needs confirmation | HTTP success status and synchronous/asynchronous behavior Needs confirmation |

**Confirmed:** Closure preserves immutable approved-output lineage. Retention jobs operate only on eligible closed cases and preserve legal-hold exceptions.  
**Source:** S, pp. 24–26, §§6.1.2–6.3.2. Links: `SCR-002-A07`, `SCR-002-T07`, `SF-AC-008`.

**Needs confirmation — API-OQ-004:** Closing edge, eligible actor, complete request/response, repeated-close behavior, and exact conflict/error mapping. Reopening is API-052, not an inferred variant of this endpoint.

### API-004 and API-018 — Attachment Ingestion and Processing Status

#### Parameters and Results

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-004 | Path `caseId` | Attachment target | Yes | Authorized case/workspace |
| API-004 | Header `Idempotency-Key` | Ingestion-operation key | Yes | Job-creation idempotency; exact fingerprint treatment of binary content Needs confirmation |
| API-004 | Body: attachment content | Binary file | File semantic required | PDF, DOCX, HTML, UTF-8 text; MIME signature and extension agree; configurable `25 MB` per-file cap |
| API-004 | Body/metadata: filename, content type | File identification/type metadata | Exact properties/requiredness Needs confirmation | Length, allowed filenames, multipart parts, number of files, and MB-to-byte conversion unresolved |
| API-004 | OCR opt-in | Optional fallback request; wire type/location Needs confirmation | Fallback requires opt-in | OCR output provenance-marked; no enabled-by-default fallback; non-English OCR deferred |
| API-004 | Success receipt | Persisted ingestion-operation identity | Semantic required | **`202` Confirmed**; operation/document/version/attachment properties and status-link mapping Needs confirmation |
| API-018 | Path `documentId` | Processing-status inquiry | Yes | Current source/document authorization |
| API-018 | Additional query/body | Version and status selection | Needs confirmation | No version-selector or polling parameter is confirmed |
| API-018 | Processing status | `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED` | Status information supported; exact property/type/requiredness Needs confirmation | HTTP success status, transition details, and completion representation unresolved |
| API-018 | Quality / quarantine information | Empty-page ratio, unknown-character ratio, table-loss indicators, language confidence; safe quarantine reason/correlation/remediation information | Applicability confirmed; public fields/types Needs confirmation | Quality thresholds, retry limits, quarantine viewing, and remediation actions unresolved |

**Sources:** S, pp. 30–32, §§8.1–8.3; p. 82, A.1; p. 83, A.2; p. 90, Appendix F.

**Confirmed processing obligations:**

1. Validate file limits and type before long-running allocation.
2. Scan before parsing; disable macro execution; do not fetch embedded remote references.
3. Quarantine unsafe content without indexing.
4. Parse PDF blocks with page index and bounding boxes; preserve table row/column annotations, headings, and reading order.
5. Normalize transport artifacts without rewriting claims.
6. Derive immutable derivative identities from content fingerprint and pipeline version; permit side-by-side reprocessing.
7. Preserve source URI, file hash, page, and optional bounding box for every chunk.
8. Permit generated citations only for resolvable anchors with current access.
9. Keep safe low-quality documents viewable but exclude them from autonomous recommendations.
10. Publish `DocumentNormalized` through durable correlated event processing; upload acceptance is not index readiness.

**Open contract — API-OQ-007:** Upload transport, file-count/name rules, archive threshold, size unit conversion, validation codes, fingerprint algorithm, OCR property, status schema, quality thresholds, and status-refresh mechanism. Links: `SCR-002-F20`–`F25`, `SCR-002-A05`, earlier `OQ-015`.

### API-005 — Request a Case-Scoped AI Run

| Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|
| Path `caseId` | Saved case context | Yes | Authorized Analyst; tenant/workspace/case guards |
| Header `Idempotency-Key` | Run-creation key | Yes | Identical replay returns original operation |
| Body: validated user request | Requested grounded-answer input | Schema, property names, types, and requiredness Needs confirmation | No arbitrary tool definitions, destinations, tenancy, authorization, or policy override |
| Requested action and other policy-relevant business input | Supported policy concepts, not a confirmed public JSON schema | Needs confirmation as public parameters | Read/normalize the six policy inputs under API-POL-001; apply API-CLS-001 to included material |
| Evidence/context selection | Exact input/derived selection contract Needs confirmation | Needs confirmation | Evidence must be permitted, quality-appropriate, and anchored |
| Response: durable run/operation identity | Logical identifier; exact receipt property Needs confirmation | Semantic required | **`202` Confirmed**; created immediately; not a completed or published answer |
| Response: initial progress/context | Run state and inquiry/stream association | Exact properties/requiredness Needs confirmation | Status schema under API-006; no confirmed `Location` header |
| Admission failure | HTTP **`429`** with **`Retry-After`** | Conditional | Tokens, queue age, and provider capacity must satisfy configured thresholds |

**Source:** S, pp. 12–13, §§2.2–2.3; pp. 40–42, Chapter 11; p. 58, §16.2.1; p. 69, §19.2.1; p. 83, A.2.

**API-005-P01 — Confirmed:** The run must apply **API-CLS-001**: model routing, log redaction, retention, and approval policy depend on the maximum information class of any material included in the run. An `INTERNAL` case containing permitted `RESTRICTED` evidence cannot use `INTERNAL` controls merely because the case’s own label is lower. Passing ACL checks does not eliminate this classification requirement.  
**Source:** S, p. 62, §17.2.1; p. 90, Appendix F. Link: [Case sensitivity, `SCR-002-F10`](01_screen_functions.md#scr-002--case-detail).

**Needs confirmation — API-OQ-006, API-OQ-026:** Run body/receipt, routing relationship to API-032, normalized-request schema, admission thresholds, classification provenance/transport, and runtime/review-wait treatment. Do not introduce a new public classification response field to implement API-CLS-001.

### API-006, API-019, and API-007 — Run Inquiry, Steps, and SSE

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-006, 019, 007 | Path `runId` | Run identity | Yes | Shared run authorization |
| API-006, 019 | Additional query/body | Inquiry options | Needs confirmation | No arbitrary history, step-kind filter, or pagination parameters established |
| API-006 | Response: stages and evidence metadata | Persisted run information | Semantic required | **`200` Confirmed**; current caller scope |
| API-006 | Run state; domain `status` | `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED` | Stored run state supported; response property/type Needs confirmation | Keep distinct from Case and Review status |
| API-019 | Response: steps | Stored `run_steps`: `id`, `run_id`, `step_kind`, `status`, `checkpoint` | Persisted step behavior confirmed; projection requiredness Needs confirmation | Success HTTP status, enum values, pagination, dependency representation, and wire types unresolved |
| API-006, 019 | Plan revision and budget | Stored `plan_revision`, `budget`; checkpoint/runtime information | Domain data confirmed; response exposure Needs confirmation | DAG depth `8`, maximum tool invocations `16`; exact budget schema unresolved |
| API-006, 019 | Failure checkpoint | Safe failed checkpoint/reason | Visible exact checkpoint required when failed | Property/types and failure-state mapping unresolved; no document/prompt/secret diagnostics |
| API-007 | Header `Last-Event-ID` | Resume offset | Applicable on reconnect | Monotonic offsets; backfill retained events within caller scope |
| API-007 | Stream result | SSE progress events | **`200` Confirmed** | Event names, payloads, media-header details, heartbeat, retention, termination, and expired-cursor behavior Needs confirmation |

**Source:** S, pp. 40–42, §§11.1–11.3; pp. 48–50, §§13.1–13.3; p. 55, §15.2.1; p. 58, §16.2.1; pp. 82–85, A.1–B.1.

**Confirmed:** Each workflow stage writes a checkpoint before downstream dispatch. Refresh reconstructs state from server records; a dropped connection is not completion. Reconnect/backfill is a read mechanism, not a replay of business mutations.

**Needs confirmation — API-OQ-006:** Full run/step/SSE schemas; event offset type; retention; reconnect failure; timeout representation; whether human-review wait consumes `run_timeout_seconds: 180`. Preserve the source’s `AWAITING_REVIEW` state and its missing-approval stop condition without inventing a `TIMED_OUT` state.

Links: `SCR-004-F01`–`F10`, `SCR-004-A01`–`A04`, `SF-CON-004`, earlier `OQ-011`.

### API-008 and API-026 — Controlled Model Generation and Catalog

#### Interface Fields

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-008 | Body: scoped generation request | Structured prompt/context/instruction request | Request semantic required; JSON/protobuf fields and types Needs confirmation | Fixed system rules, signed workflow instruction, validated user input, separately delimited retrieved passages |
| API-008 | Deployment/context selection | Approved deployment and capability/context requirements | Semantic policy requirement; transport Needs confirmation | Workspace whitelists specific deployments, not provider brands; apply API-CLS-001 |
| API-008 | Budget / operation context | Input/output token reservation, workspace quota, run and trace lineage | Semantic required | Exact amounts, schema, idempotency-key transport, provider timeout, and retry counts unresolved |
| API-008 | Structured-output schema/version | Versioned JSON schema requested from provider | Required behavior | Exact schema and version property Needs confirmation; unknown fields, invalid citations, control-character injection cause `MODEL_OUTPUT_INVALID` |
| API-008 | Response: validated result | Candidate generation output and invocation outcome | Exact fields/types/requiredness Needs confirmation | HTTP success status and synchronous/asynchronous shape unresolved; not a publication authorization |
| API-026 | Query/body parameters | Catalog selection/filtering | Needs confirmation | No deployment filter, paging, or workspace-selector property established |
| API-026 | Response: model registry metadata | Capability, region, data-handling class, context length, cost profile, evaluation approval; specific deployment identity | Concepts confirmed; public property names/types/requiredness Needs confirmation | Success HTTP status and whether response is workspace-filtered unresolved |

**Source:** S, pp. 37–39, §§10.1–10.3.

**API-008-P01 — Confirmed:** Before model routing/provider invocation, apply the maximum included-material information class under **API-CLS-001** to model route, log redaction, retention, and approval policy. Do not route restricted evidence under a case’s lower sensitivity. This applies to initial selection and fallback.  
**Source:** S, p. 62, §17.2.1; p. 37, §§10.1.1–10.1.2. Link: `SCR-002-F10`.

**Additional confirmed controls:**

1. Fallback only to an approved deployment with equal or stronger data-handling class.
2. Never route restricted content to an unapproved region or deployment during outage.
3. Label evidence untrusted; strip tool-call directives from evidence contexts; record prompt-injection indicators.
4. Do not promote source text into instruction authority.
5. Validate structured output with bounded retries.
6. Reserve input/output tokens and track provider usage under workspace quota.
7. Quota exhaustion is terminal for the current run; no automatic model or data-class change.
8. Tag likely personal data during extraction; redact nonessential fields before provider invocation where policy permits.
9. Log token counts and digests, not entire prompts by default; diagnostic traces never contain user documents or API secrets.
10. Emit correlated `ModelInvocationCompleted`; this event is not proof of tool permission or publication.

**Sources:** S, pp. 37–39, Chapter 10; p. 62, §17.2.2; p. 64, §18.1.1.

**Needs confirmation — API-OQ-009, API-OQ-026:** Approved model deployments/regions, generation schema, token budgets, timeouts, key transport, catalog permissions, classification-control mappings, and provider adapter endpoints. Links: `SCR-007-F03`, `SCR-004-F07`, earlier `OQ-022`.

### API-009 and API-025 — Connector Sync and Run Inquiry

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-009 | Path `connectorId` | Configured connector | Yes | `Admin`; authorized workspace |
| API-009 | Header `Idempotency-Key` | Sync-operation key | Yes | Durable job idempotency |
| API-009 | Body: sync request/options | Incremental source-sync intent | Shape/requiredness Needs confirmation | No confirmed full-sync flag, cursor override, provider selector, or batch-size field |
| API-009 | Success receipt | Persisted sync-operation identity | Semantic required | **`202` Confirmed**; exact properties and inquiry association unresolved |
| API-025 | Path `connectorId` | Sync-run inquiry context | Yes | Read scope Needs confirmation |
| API-025 | Query pagination/filter/sort | Run-list options | Needs confirmation | No parameter names/defaults supplied |
| API-025 | Response: sync outcomes | `SyncRun` and safe trust/credential/ingestion outcomes | Concepts supported; fields/types/requiredness Needs confirmation | Success status and complete sync-state enum unresolved |
| Domain sync data | Provider cursor, high-watermark, error ledger; `connector_cursors.cursor`, `watermark`, `retry_state` | Durable checkpoint data | Stored each run | Public exposure of raw provider cursor is not established |
| Capability metadata | List, fetch, delta cursor, ACL, delete support | Exact public types/property names Needs confirmation | Connector advertises capabilities | Unsupported capability gives lower-trust ingestion mode and visible warning |
| Quarantine metadata | Reason code, correlation ID, remediation path | Exact public schema Needs confirmation | Applicable after bounded poison-record retries | Remaining batch may continue with durable exception ledger |

**Source:** S, pp. 27–29, §§7.1–7.3; p. 85, B.1; p. 83, A.2.

**Confirmed:** Incomplete provisioning blocks sync. Credentials are secret-store values behind workspace-scoped references. Revocation makes queued jobs fail with `CONNECTOR_REAUTH_REQUIRED` without tokens. Cursor advances only when preceding items have durable outcomes. Source deletion produces a tombstone and scheduled index removal. ACL changes invalidate affected cache before serving new results. Workers honor provider `Retry-After`, use exponential backoff with jitter, enforce workspace quotas, and schedule fairly.

**Needs confirmation — API-OQ-011:** Providers/permissions, read/configuration scopes, exact request/receipt, capabilities/trust policy, retries, cursor projection, sync-state enum, credential revocation/reauthorization APIs, and provisioning/status interfaces. Links: `SCR-006-F01`–`F10`, `SCR-006-A01`–`A06`, earlier `OQ-016`.

### API-010, API-021, and API-022 — Search and Evidence

#### Request and Success Contracts

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-010 | Body: retrieval query | User query; public wire name/type Needs confirmation | Query capability confirmed; public requiredness Needs confirmation | Validate before retrieval; do not equate MCP `query: string` with complete public request schema |
| API-010 | Body/query: scope and filters | Search context | Names/types/requiredness Needs confirmation | Tenant and permissions derived/enforced from trusted context; no invented filters or `max_items` property |
| API-010 | Success response | ACL-filtered lexical/semantic evidence | **`200` Confirmed** | Collection wrapper, paging, and public result limit unresolved |
| API-021 | Path `evidenceId` | Opaque evidence inquiry | Yes | Evidence-resource mapping unresolved; current permission and anchors required |
| API-022 | Path `caseId` | Case evidence inquiry | Yes | Case and each source independently guarded |
| API-021, 022 | Additional query/body | Version/run/evidence selection | Needs confirmation | No confirmed run selector, latest-version fallback, or page-size default |
| API-021, 022 | Success response | Authorized evidence/source metadata | Required semantic capability | Success HTTP status and full schema Needs confirmation |
| All applicable retrieval | Unsupported outcome | Literal `NO_SUPPORTED_EVIDENCE` | Returned when confidence/evidence quality insufficient | HTTP status, envelope versus normal-result representation, and next-step schema Needs confirmation |

#### Evidence Item Contract

Each response evidence item includes the following semantic information. Exact JSON property names and detailed schemas remain unresolved.

| Information | Meaning / type | Requiredness | Constraints |
|---|---|---|---|
| Chunk ID | Immutable chunk reference; logical identifier policy | Required per evidence item | Must resolve to permitted stored source anchor |
| Source title | Semantic text; length Needs confirmation | Required per evidence item | Authorized source metadata only |
| Document revision | Immutable document-version/revision reference | Required per evidence item | Do not substitute arbitrary latest source |
| Page anchor | Stored page/anchor reference; page/range schema Needs confirmation | Required per evidence item | Generated citations resolvable; citation click-through highlights anchored page range |
| ACL digest | Digest of evidence authorization provenance; type/encoding Needs confirmation | Required per evidence item | Digest is not a substitute for current permission checks |
| Citation identifier | Opaque end-user citation reference | Citation semantics confirmed; precise response requiredness Needs confirmation | Verified before display |
| Source URI, file hash, page number | Stored chunk provenance | Stored for every chunk | Public exposure and file-hash encoding Needs confirmation |
| Bounding box | Optional anchor geometry | Optional stored provenance | Coordinate system and wire schema Needs confirmation |
| Text/passages and quality flags | Permitted normalized evidence | Public projection Needs confirmation | No unauthorized text; low-quality safe content remains viewable but cannot support autonomous recommendations |

**Source:** S, p. 31, §§8.2.1 and 8.3.1; p. 32, §8.3.2; p. 35, §9.3.1; p. 57, §16.1.2.

**Confirmed retrieval processing:** Bounded lexical/vector candidates; reciprocal rank fusion; deterministic re-ranking; diversity limiting redundant hits; token budget to the model; ACL filtering before text release. Source database remains authoritative. Rebuilds use parallel indexes/versioned aliases and atomic read-alias switch after completeness/recall checks. Cache authorization changes take effect before the next retrieval.

**Reference configuration, not public request defaults:** `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `embed_dimension: 1536`, `hybrid_rrf_k: 60`.  
**Source:** S, pp. 34–36, Chapter 9; p. 90, Appendix F.

**Needs confirmation — API-OQ-008:** Public search body, scope selection, filters, result schema/pagination, evidence ID mapping, source-content delivery, signed-URL expiry/recovery, page/bounding-box conventions, HTML/DOCX/text anchors, clarification versus human routing. Links: `SCR-003-F01`–`F12`, `SCR-003-A01`–`A06`, earlier `OQ-017`–`OQ-018`.

### API-023 and API-024 — Review Queue and Decision Capture

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-023 | Query/body: queue selection | Reviewer/pool/task inquiry | Exact properties/requiredness Needs confirmation | No self-assignment, filtering, sorting, or bulk approval contract |
| API-023 | Response: task identity, case/run association | Immutable task/context references | Domain data confirmed; public schema Needs confirmation | Authorized reviewer/pool scope |
| API-023 | Review state | `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED` | State vocabulary confirmed; exact projection Needs confirmation | Complete transition matrix unresolved |
| API-023 | Reviewer pool, minimum role, separation of duties, expiry | Policy-routed task requirements | Required behavior; exact response fields/types Needs confirmation | Configured SLA; no implicit approval |
| API-023 / review-detail delivery | Exact candidate, citations, model/prompt version, policy reasons | Review information | Required review display capability | Which endpoint supplies task detail Needs confirmation; no new task-detail URL is established |
| API-024 | Path `approvalId` | Target approval/task | Yes | Exact route-to-entity mapping unresolved |
| API-024 | Body: decision | Approve/reject choice; literal request enum Needs confirmation | Decision semantic required | Do not derive `APPROVE`, `APPROVED`, or another literal from UI button wording |
| API-024 | Evaluated artifact hash; stored `artifact_hash` | Exact candidate binding | Binding semantic required; request property/type Needs confirmation | Hash algorithm, encoding, and length unresolved; changed artifact rejected as stale |
| API-024 | Rationale/reason | Reviewer explanation | Stored record includes rationale; exact required-input rule Needs confirmation | Length, format, and mapping to `reason` unresolved |
| API-024 | Annotations | Additional review annotations | Optional | Schema/length/default Needs confirmation |
| API-024 | Actor and timestamp | Authenticated actor and server occurrence | Record-required; not editable review inputs | Preserve immutable decision lineage |
| API-024 | Success result | Accepted immutable decision | **`200` Confirmed** | Body fields/types/requiredness Needs confirmation; not unconditional publication |
| API-024 | Conflict result | Stale/conflicting decision | **`409` Confirmed in catalog** | Specific stale-approval business code and complete conflict taxonomy Needs confirmation |
| API-023 | Success result | Authorized queue | Status and collection/pagination schema Needs confirmation | Public cursor principle applies; queue-specific fields unresolved |

**Source:** S, pp. 44–46, §§12.1–12.3; pp. 57–59, §§16.1–16.2; pp. 82–85, A.1–B.1.

**Confirmed review procedure:**

1. Load authorized policy-routed tasks.
2. Provide the exact candidate, citations, model/prompt version, and policy reasons.
3. Enable source inspection before approval.
4. Validate the defined required review fields; UI controls remain disabled until complete.
5. On submission, re-evaluate actor/task authorization, role/pool constraints, applicable task state, exact hash, and separation of duties.
6. Reject changed-artifact decisions as stale and audit the rejection.
7. Append the immutable decision and publish correlated `ApprovalDecisionRecorded`.
8. Invoke publication validation separately; `200` decision acceptance does not mean other evidence/policy requirements are satisfied.

**Needs confirmation — API-OQ-010:** Full task/detail/decision schemas, exact required-field set, rationale requiredness, hash definition, queue pagination, decision literals, task-state/expiry rules, whether actual evidence opening is enforced as a submission prerequisite, override contract, and automatic case-state consequences.

Links: `SCR-005-F01`–`F14`, `SCR-005-A01`–`A06`, `SCR-002-A09`–`A10`, earlier `OQ-013`–`OQ-014`.

### API-020 — Publication Contract Without a Confirmed Public Endpoint

| Interface aspect | Confirmed semantic contract | Needs confirmation |
|---|---|---|
| Invocation | Publication validation is the consumer action of `ApprovalDecisionRecorded`; policy/evidence completion governs publication | Whether a separate callable interface exists; method/path; service scope; invocation payload |
| Inputs | Exact candidate artifact/hash; run/case context; required evidence/source versions and current access; applicable normalized policy/rule version and approval records | JSON/protobuf properties, types, requiredness, record lookup keys, hash canonicalization |
| Classification controls | **API-CLS-001 applies.** Approval policy, model routing, log redaction, and retention use maximum class of all run-included material, not only the case label. | Storage and transport representation; per-class policy details. No new public field or seventh policy input is established. |
| Success | Final response pointer updates in the same transaction that records the satisfied approval gate; publish only supported, policy-satisfied content | HTTP status/body only if an independent endpoint is confirmed |
| Rejection | Stale hash, changed permissions, insufficient evidence, unsatisfied approval/policy, or wrong-artifact replay cannot publish | Specific HTTP/code/envelope for each gate failure |
| Public effect | Published artifact may be displayed as `PUBLISHED`; historical approved lineage remains immutable | Exact current-approved-result public schema |

**Sources:** S, pp. 12–13, §§2.2.2–2.3.2; pp. 44–46, §§12.1–12.5; p. 62, §17.2.1; p. 87, C.1; p. 90, Appendix F.

**API-020-P01 — Confirmed procedure:**

1. Resolve the exact candidate and its immutable hash.
2. Recompute authorization against current tenant/workspace/source permissions.
3. Verify required citations/evidence and resolvable source anchors.
4. Apply the applicable deterministic policy, including maximum included-material classification under API-CLS-001.
5. Verify required approvals bind the exact artifact and satisfy actor/separation-of-duties conditions.
6. Reject a replay attempting to publish another artifact under an old approval.
7. Atomically record the satisfied gate and update the final response pointer, with applicable outbox publication.
8. Expose the published result only after that transaction succeeds.

**Needs confirmation — API-OQ-010, API-OQ-026:** Gate transport, classification-control provenance, revalidation/error schema, and exact activation/version rules. Link: [Publication operation, `SCR-002-A09`](01_screen_functions.md#scr-002--case-detail). A manual Publish button or endpoint is not confirmed.

### API-011 — Audit Events

| Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|
| Query: pagination cursor | Immutable-log continuation | Cursor pagination confirmed; parameter name and initial requiredness Needs confirmation | No page size/direction/expiry default supplied |
| Query: action/actor/date/resource filters | Possible audit inquiry controls | Needs confirmation | Do not invent parameter names or numeric range limits |
| Response: event metadata | Selected stored fields `id`, `tenant_id`, `actor_id`, `action`, `digest` | Entity fields confirmed; public projection/types/requiredness Needs confirmation | Append-only, tenant-scoped, redacted content |
| Decision/template/access lineage | Decision metadata, prompt-template digests, access events | Auditor capability confirmed; exact fields Needs confirmation | Auditor access does not imply full case/source-content access |
| Occurrence/trace/hash-chain metadata | Durable time/correlation and batch hashes | Stored behavior confirmed; full response schema unresolved | RFC 3339 UTC where timestamps exposed |
| Success | Authorized cursor-paginated immutable log | **`200` Confirmed** | Collection wrapper/end cursor/detail lookup unresolved |

**Sources:** S, p. 11, §2.1.2; pp. 61–63, §§17.2–17.3; p. 83, A.2; p. 85, B.1.

**Confirmed:** Audit records are append-only, chained with batch hashes, and exported to independently controlled retention storage. Operators may query but not alter historical review decisions.

**Needs confirmation — API-OQ-012:** Query/detail schema, redaction scope, non-Auditor permissions, digest encoding, cursor behavior, and current classification-dependent redaction projection. Links: `SCR-008-F01`–`F08`, `SCR-008-A01`–`A04`, earlier `OQ-019`.

### API-012 — Usage

| Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|
| Query/body: scope/time selection | Usage inquiry | Names/types/requiredness Needs confirmation | No confirmed currency, billing interval, date range, or workspace selector |
| Response: costs, quotas, trend estimates | Usage summary concepts | Required semantic response; exact properties/types unresolved | **`200` Confirmed**; authorized `Admin` |
| Budget, forecast, rejected excess requests | Daily rollup concepts | Rollup behavior confirmed; inclusion in this response Needs confirmation | Daily rollups do not establish a screen refresh interval |
| Cost-center and deployment attribution | Workspace cost center/model deployment version | Ledger attribution required; public schema unresolved | Includes model invocations, embeddings, storage, indexing |
| `in_tokens`, `out_tokens` | Selected `token_ledger` fields | Ledger fields confirmed; response exposure/types unresolved | Do not infer currency or numeric precision |

**Source:** S, pp. 64–66, §§18.1–18.3; p. 83, A.2; p. 85, B.1.  
**Needs confirmation — API-OQ-013:** Complete usage schema, units/currency, aggregation window, quotas, scope, and display linkage. Links: `SCR-010-F01`–`F04`, earlier `OQ-021`.

### API-013 and API-045 — Evaluation Creation and Reading

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-013 | Header `Idempotency-Key` | Evaluation-operation key | Yes | Job idempotency |
| API-013 | Body: benchmark setup/version selections | Frozen benchmark evaluation request | Schema, selector names, types, and requiredness Needs confirmation | No arbitrary expected-fixture edit or dataset-management permission established |
| API-013 | Success receipt | Durable evaluation-operation identity | Semantic required | **`202` Confirmed**; fields/status URL unresolved |
| API-045 | Path `evaluationId` | Evaluation/result inquiry | Yes | Exact read scope unresolved |
| API-045 | Query/body options | Result selection | Needs confirmation | No comparison, time-range, paging, or format selector established |
| API-045 | Response: status, dataset/model/prompt/version metadata | Reproducible evaluation context | Concepts required for evaluation behavior; wire fields/types unresolved | Success HTTP status and evaluation-state enum Needs confirmation |
| API-045 | Scorecard | Grounded citation precision, unsupported-claim rate, high-risk policy recall | Metrics confirmed; schema/precision/requiredness Needs confirmation | Reference targets `>=0.97`, `<=0.02`, `1.00` |
| API-045 | Domain confidence intervals / distribution shift | Statistical result | Required reporting behavior | Detailed statistical schema unresolved |
| API-045 | Release-gate result | Safety/quality acceptance evidence | Supported behavior; response property unresolved | Low statistical confidence blocks release, not evidence of equivalence |

**Source:** S, pp. 74–76, §§21.1–21.3; p. 83, A.2; p. 89, E.1.

**Confirmed:** The reference evaluation corpus has `1,200` synthetic, permission-controlled cases covering retrieval, refusal, ambiguity, and adversarial evidence. Each stores expected citation sets and decisions. Corpora are frozen, versioned, and independently reviewed. Prompt/model updates require re-evaluation. Critical isolation and approval tests must pass with zero exceptions.

**Needs confirmation — API-OQ-013:** Setup/result schemas, state enum, read permission, progress contract, version selection, signed-manifest verification interface, and exact relationship to Usage & Quality. Links: `SCR-010-A02`–`A04`, earlier `OQ-021`.

### API-014 and API-015 — Export and Deletion

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| Both | Path `workspaceId` | Requested resource scope | Yes | Workspace route confirmed; chapter’s tenant-level language creates unresolved scope distinction |
| Both | Header `Idempotency-Key` | Lifecycle-operation key | Yes | Durable job idempotency |
| Both | Independent approval context | Two independent approval checks; `Admin + approver` | Required semantic gate | Approval actors, proof references, transport, sequence, and reuse rules Needs confirmation |
| API-014 | Body: export request | Controlled export intent/options | Schema/requiredness Needs confirmation | No raw-secret/internal-prompt export option allowed |
| API-015 | Body: deletion request | Controlled deletion intent/scope | Schema/requiredness Needs confirmation | Cannot bypass legal hold; no undocumented force-delete option |
| Both | Success receipt | Persisted operation identity | Semantic required | **`202` Confirmed**; not package completion or deletion verification |
| API-014 | Completed export contents | Case metadata, approved artifacts, source references, audit manifests with checksums | Package contents confirmed | Package format, checksum algorithms, manifest schema, download/status endpoint and URL lifetime unresolved |
| API-015 | Completed deletion evidence | Tombstones, blob/index removal, completion receipts, legal-hold exceptions | Required behavior | Status/receipt properties, final-state enum, and download/read endpoint unresolved |

**Source:** S, pp. 78–80, §§22.1–22.3; p. 83, A.2; p. 88, `T-11`; p. 89, `TST-013`.

**Confirmed:** A single Admin is insufficient. Export excludes secrets and internal model prompts. Deletion enforces holds, records protected retained records and receipts, and uses the same inventory for data-subject access requests. `TenantDeletionVerified` carries manifest/receipt evidence for closing the purge record.

**Needs confirmation — API-OQ-015:** Tenant-versus-workspace extent, approval workflow/actors, request schemas, job inquiries, package/receipt formats, held-data status representation, and partial-failure recovery. Links: `SF-SCP-007`, `SCR-008-A05`, `SF-CON-010`, earlier `OQ-023`.

### API-027 and API-028 — Principal Context and Membership

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-027 | Authenticated context | Current principal/tenant | Yes | Verified token/session, no supplied subject impersonation |
| API-027 | Query/body | Context options | Needs confirmation | No tenant-switch or workspace-selector parameter confirmed |
| API-027 | Response: principal/membership/policy context | Identity context inquiry | Exact fields/types/requiredness and HTTP success status Needs confirmation | Baseline roles exist; does not grant every role access to every API |
| API-028 | Path `workspaceId` | Workspace membership target | Yes | Tenant/workspace and action authorization |
| API-028 | Body: membership update | Member identities and bindings | Property names, types, requiredness Needs confirmation | Exact PUT replacement versus incremental semantics unresolved |
| API-028 | Revision/idempotency context | Safe durable membership change | Stale/unauthorized write rejection confirmed; exact transport Needs confirmation | No unguarded role escalation |
| API-028 | Response | Accepted membership result | Status/body Needs confirmation | Update must produce durable actor/tenant/revision/time/correlation evidence |

**Source:** S, pp. 21–23, Chapter 5.  
**Needs confirmation — API-OQ-001, API-OQ-016:** Principal schema, membership administration scope, update semantics, concurrency/key transport, and session context selection. Links: `SF-PRE-001`–`003`, `SF-SCP-008`, earlier `OQ-002`–`OQ-003`, `OQ-024`.

### API-029 — Security Holds

| Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|
| Body: hold target, scope, reason, policy context | Legal/security hold request concepts | Full schema and required fields Needs confirmation | Target names and identifiers are not supplied by the source |
| Trusted mutation context | Tenant, revision, actor, occurrence, correlation | Required for durable change | Exact transport/concurrency condition unresolved |
| Success response | Hold result/identity | Status, fields, types, and requiredness Needs confirmation | No hold-release or hold-list endpoint confirmed |
| Lifecycle effect | Preserve legal-hold exceptions in retention/deletion | Required behavior | Approval/administrative role, precedence, and hold-state schema unresolved |

**Source:** S, pp. 61–63, Chapter 17; p. 26, §6.3.2; p. 80, §22.3.2.  
**Needs confirmation — API-OQ-016:** Hold API schema/rights, lifecycle semantics, release process, and relationship to `SecurityPolicyChanged`. Link: `SF-SCP-008`, earlier `OQ-024`.

### API-030 and API-031 — Design Governance

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-030 | Body: change/decision record | Design change and requirement/invariant linkage | Schema/property names/types/requiredness Needs confirmation | Supported concepts: `ChangeRequest`, `RequirementLink`, `DecisionRecord` |
| API-030 | Impact scores | Behavior, data migration, threat surface, operating cost impacts | Change-record behavior supported; exact fields/ranges unresolved | No invented numeric scale |
| API-030 | Trusted mutation context | Tenant, revision, actor, occurrence, correlation | Required | Validate before allocating long-running work |
| API-030 | Success response | Accepted/approved design-governance outcome | Status/body and approval workflow Needs confirmation | Approved change increments minor revision; incompatible protocol change increments major revision |
| API-031 | Path `id` | Baseline inquiry | Yes | Authorized tenant/baseline |
| API-031 | Response | `DesignRevision` / baseline information | Status/properties/types/requiredness Needs confirmation | Preserve immutable revision traceability |

**Confirmed:** Revised invariants link to at least one negative test. Accepted baseline changes produce correlated `BaselineCommitted` evidence. Duplicate delivery cannot reapply mutation.  
**Source:** S, pp. 8–10, Chapter 1.

**Needs confirmation — API-OQ-020:** Governance roles, approval/revision allocation, request/response schemas, impact score definitions, invariant-test linkage schema, and read projection. No screen is established by these endpoints.

### API-032 — Chapter 3 Run Request Route

| Aspect | Contract |
|---|---|
| Method/path | **Confirmed:** `POST /v1/runs` |
| Request | Validated run request; complete body, case reference property, required fields, and caller scope **Needs confirmation** |
| Idempotency | Cross-service writes must be idempotent; job-creating POSTs require `Idempotency-Key` |
| Response | Run-request result and dependency fallback must be unambiguous; exact status/receipt **Needs confirmation** |
| Event | `RunRequested` confirmed |
| Shared controls | Tenant/resource access, bounded workflow, API-POL-001, and API-CLS-001 apply to run behavior; transport mapping remains unresolved |
| Route relationship | Whether distinct from, alias of, or superseded by API-005 **Needs confirmation** |

**Source:** S, pp. 15–17, §§3.1–3.4; p. 54, §15.1.2; p. 62, §17.2.1.  
**Open contract:** `API-OQ-006`; earlier `SF-CON-007`, `OQ-011`. Do not silently remove either route or implement two unrelated run-creation behaviors.

### API-033 and API-034 — Workflow Inquiry and Dead-Letter Replay

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-033 | Path `runId` | Workflow inquiry | Yes | Scoped internal/operator authorization |
| API-033 | Response: workflow/checkpoints | `WorkflowCheckpoint`, outbox/reconciliation context | Fields/types/requiredness/status Needs confirmation | Preserve persisted stage/checkpoint information; safe telemetry only |
| API-034 | Path `id` | Dead-letter target | Yes | Operator scope guard |
| API-034 | Operator reason | Audited replay reason | Semantic required | Property/type/length/catalog unresolved |
| API-034 | Dry-run validation | Validate replay before execution | Required procedure | Whether a flag, separate result, or enforced preliminary step Needs confirmation |
| API-034 | Scope limit | Bounded replay extent | Semantic required | Numeric limit and field schema unresolved |
| API-034 | Original event identity/provenance | Replay/migration linkage | Required behavior | Preserve identity unless explicit schema transformation with provenance link |
| API-034 | Idempotency/operation context | Replay-safe durable operation | Required semantics | Exact key transport/TTL and HTTP result unresolved |
| Both | Success response | Inquiry/replay result | HTTP status/body Needs confirmation | No ordinary end-user replay permission established |

**Source:** S, pp. 48–50, §§13.1–13.3; p. 90, F.1.  
**Needs confirmation — API-OQ-019:** Replay schema, scope values, operator roles, dry-run transport, and schema-migration provenance. Links: `SCR-004-A06`, earlier `OQ-024`.

### API-035 and API-036 — Internal Storage Read and Purge

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-035 | Path `id` | Stored document/object inquiry | Yes | Document/version/object-role mapping unresolved |
| API-035 | Query/body: object selection | Version/object role | Exact parameters Needs confirmation | No arbitrary filesystem/path access |
| API-035 | Response | Authorized immutable object/metadata or controlled delivery | Status/media type/fields/requiredness Needs confirmation | Encrypted storage; opaque public names; access-controlled short-lived signed URLs |
| API-036 | Body: purge scope/inventory | Eligible tombstoned/retained objects | Schema/types/requiredness Needs confirmation | Tenant predicate, legal holds, eligibility, immutable receipts; apply API-CLS-001 retention control where run material is involved |
| API-036 | Revision/key context | Safe purge operation | Required semantics; exact transport unresolved | Stale/unauthorized mutations rejected |
| API-036 | Success result | Purge outcome/receipt | Status/body/requiredness Needs confirmation | Completion receipts and legal-hold exceptions required |
| Both | Query/body defaults | Not supplied | Needs confirmation | No default tenant, object role, purge range, or signed-URL lifetime |

**Source:** S, pp. 51–53, §§14.1–14.3; p. 62, §17.2.1; p. 66, §18.3.2.

**Confirmed:** Soft-deleted entities cannot be retrieved. Final purge uses a scheduled tombstone pipeline, but no schedule is supplied. Object keys include tenant, workspace, document, version, and role. Source metadata is not rolled back by failed index writes; reconciliation repairs derivatives.

**Needs confirmation — API-OQ-008, API-OQ-015, API-OQ-021:** Object-delivery shape, eligible purge inventory, classification-dependent retention mapping, schedule, receipts, and partial failure handling.

### API-037 — OpenAPI Contract Inquiry

| Aspect | Contract |
|---|---|
| Request | `GET /v1/openapi.json`; additional parameters **Needs confirmation** |
| Authentication | Source audience requirement retained; exact client/tooling access scope **Needs confirmation** |
| Response | External OpenAPI definition; exact OpenAPI version, success status, caching/version headers, and safe tenant-specific projection **Needs confirmation** |
| Governance | Repository-controlled IDL generates OpenAPI/protobuf; CI blocks breaking field deletion and incompatible enum changes |
| Event | `ApiCompatibilityVerified` exists; a GET does not automatically emit it or mutate a compatibility record |
| Default | No contract-version selector or cache lifetime supplied |

**Source:** S, pp. 54–56, §§15.1–15.3; p. 82, Appendix A introductory text.  
**Needs confirmation — API-OQ-022:** OpenAPI version, publication/access mechanism, schema repository binding, and compatibility evidence.

### API-038 and API-039 — Liveness and Readiness

| API | Request | Confirmed purpose | Response / constraints needing confirmation |
|---|---|---|---|
| API-038 | `GET /v1/health/live` | Runtime liveness inquiry in deployment topology | Probe role/tenant handling, checks, status codes, fields/types, timeout, cache behavior, and public exposure |
| API-039 | `GET /v1/health/ready` | Runtime readiness inquiry | Dependency checks, healthy/unhealthy states, status codes, fields/types, warm-recovery behavior, and public exposure |

**Confirmed network constraints:** Public TLS terminates at the application gateway; API workloads remain private; datastore public endpoints are rejected; worker egress is declared and controlled. No probe response exposes datastore credentials or private tenant data.  
**Source:** S, pp. 18–20, §§4.1–4.3.

**Needs confirmation — API-OQ-018:** Health schemas, authenticated probe mechanism, status/error codes, and thresholds. Do not invent `200`/`503` health contracts or readiness definitions from endpoint names alone.

### API-040, API-041, and API-042 — Metrics, Degraded Modes, and Capacity

| API | Request/parameter contract | Supported response concepts | Status / schema gaps |
|---|---|---|---|
| API-040 | `GET /internal/metrics`; query/body fields Needs confirmation | Request rate, error rate, latency, saturation; grounding pass rate, retrieval empty rate, provider throttling, token use, approval backlog age | Success status, metric protocol, labels, units, aggregation, tenant-safe projection, and read role Needs confirmation |
| API-041 | `GET /v1/system/degraded-modes`; query/body fields Needs confirmation | Degraded service availability and supported manual/evidence paths | Success status, mode enum, quality-flag property, read role, and refresh contract Needs confirmation |
| API-042 | `GET /internal/capacity`; query/body fields Needs confirmation | Capacity/admission budgets, queue age, token/provider capacity context, recovery/load information | Success status, units, thresholds, field types, and safe projection Needs confirmation |

**Confirmed:** Generation outage preserves manual case editing and evidence search. Vector degradation may use lexical retrieval with a visible reduced-quality flag. New generation admission can be disabled during provider outage. Degraded modes never bypass authorization, maximum-class controls, or approval.  
**Source:** S, pp. 68–70, §§19.1–19.3; p. 79, §22.2.1; p. 62, §17.2.1.

**Needs confirmation — API-OQ-018:** Operational metrics/capacity schemas, mode vocabulary, read scopes, timeout/retry details, and browser binding. Link: `SF-SCP-006`, `SCR-002-A11`, `SCR-003-F10`.

### API-043 and API-044 — Release Operations

| API | Location / name | Meaning / type | Required | Constraints / default |
|---|---|---|---|---|
| API-043 | Body: release request/artifact references | Reproducible release operation | Schema/property names/types/requiredness Needs confirmation | Verified image digest/build identity, schemas, prompt versions, model-routing policy |
| API-043 | Migration/config/rollout context | `MigrationPlan`, `ConfigVersion`, `RolloutGate` | Semantic release evidence supported; detailed fields unresolved | Signed deployment config; secrets only vault references |
| API-043 | Approval/sign-off context | Security/SRE validation before promotion | Required procedure | Exact transport, actor identities, and approval state schema unresolved |
| API-043 | Success response | Accepted/promoted release operation | HTTP status and synchronous/asynchronous result Needs confirmation | `ReleasePromoted` correlated evidence |
| API-044 | Path `releaseId` | Release record inquiry | Yes | Authorized operational scope |
| API-044 | Response | Image/schema/prompt/policy/config/migration lineage | Status/fields/types/requiredness Needs confirmation | Deployed binary, prompt, and policy versions reconstructible |

**Confirmed:** CI performs static/dependency analysis, unit/contract tests, SBOM generation, and image signing. Production deploys only digests verified against allowed build identity. Predeploy changes remain backward compatible; canary precedes enforcement after old replicas drain. Regression rolls back traffic, not an automatic database down-migration. Release records preserve whether new writes remain readable after rollback.  
**Source:** S, pp. 71–73, §§20.1–20.3.

**Needs confirmation — API-OQ-020:** Release schemas/roles, digest formats, sign-off proof, canary thresholds, operation timeouts, and status inquiries. No release UI is confirmed.

### API-046 — MCP `knowledge.search@v1`

This is a **Confirmed tool contract**, not the public API-010 body schema.

| Direction / field | Meaning | Source type | Required status | Constraints / default |
|---|---|---|---|---|
| Input `query` | Retrieval query | `string` | Listed in contract; optional/nullable treatment Needs confirmation | Length/normalization/default not supplied |
| Input `case_id` | Authorized case context | `uuid` | Listed in contract; optional/nullable treatment Needs confirmation | Tenant/case/source scope; no default |
| Input `max_items` | Maximum returned items | `int<=10` | Listed in contract; optionality Needs confirmation | Upper bound `10` confirmed; lower bound/default not supplied |
| Output `evidence_set_id` | Evidence-set identity | `uuid` | Contract output field | Exact relationship to API-021 `evidenceId` Needs confirmation |
| Output `citations` | Returned evidence citations | `Citation[]` | Contract output field | Citation semantics under evidence contract; complete element schema unresolved |
| Authorization | Permitted-document retrieval | `read:permitted_documents` | Required | Tenant-scoped; separate capability decision |
| Effect | Read-only | Literal source effect | Required | No arbitrary URLs or filesystem access |

**Source:** S, p. 87, C.2.

**Needs confirmation — API-OQ-023:** MCP version/transport, endpoint, error shape/status, optionality, lower bound, and pinned `Citation` schema. Discovery metadata cannot authorize dispatch. A denied action cannot be substituted with a semantically equivalent tool.

### API-047 — A2A Task Envelope

| Field | Meaning / type | Required status | Constraints / default |
|---|---|---|---|
| `task_id` | Task identity; UUID example | Required task concept | Exact lexical/version contract Needs confirmation |
| `tenant_id` | Immutable task tenant | Required | Example contains fictional string placeholder, not proof that storage UUID tenancy changes type |
| `capability` | Versioned capability reference | Required | Example `research.grounded_search.v1`; discovery alone insufficient |
| `input_schema` | Declared input-schema reference | Required | Example `schema://oriondesk/research-request/1`; registry resolution/version policy unresolved |
| Declared output schema | Handoff output contract | Required concept in §11.2.2 | Property absent from example; name/transport Needs confirmation |
| `deadline_at` | Task deadline | Required deadline concept | RFC 3339 example; exact expiry/decline error semantics unresolved |
| `trace_id` | Trace context | Required | Cross-boundary correlation also required; correlation-field transport unresolved |
| `authorization_ref` | Independent invocation grant/reference | Present in source example | Exact requiredness/verification/schema Needs confirmation |
| `payload` | Declared input | Task payload | Example has `case_id`, `query`; complete schema governed by referenced contract |
| Handoff result | Completion/decline | Receiving agent may decline | Status enum, response envelope, transport, retries, and timeout representation Needs confirmation |

**Source:** S, p. 41, §11.2.2; p. 87, C.2.

### API-048 — Optional Outbound Webhooks

| Interface aspect | Confirmed behavior | Needs confirmation |
|---|---|---|
| Request delivery | Optional outbound delivery after internal change | HTTP method, recipient URL contract, subscriptions, event selection, body schema, media type |
| Signature | Delivery signed; recipient verifies signature | Algorithm, secret/key reference, signature header names, canonical signing bytes, rotation |
| Event age | Recipient verifies age | Timestamp field, maximum age, clock-skew handling |
| Retry | Exponential backoff | Retryable statuses, counts, jitter, timeout, delivery ledger, dead-letter policy |
| Failure isolation | Delivery failure cannot roll back internal case transition | Acknowledgment/response status and caller recovery workflow |
| Authorization | Scoped subscription/delivery context | Subscription administration methods/paths and eligible roles |

**Source:** S, p. 55, §15.2.2.  
**Open contract:** `API-OQ-024`; earlier `OQ-024`. No webhook endpoint or signature header is invented here.

### API-049–API-059 — Missing Interface Field Contracts

| APIs | Confirmed field/processing concepts to preserve | Interface information Needs confirmation |
|---|---|---|
| API-049, 050 | Workspace identity/configuration revision; retention class, allowed models, connector credential references, approved toolsets, reviewer routing; revision-protected updates and audit | Read/update method/path, JSON fields/types/requiredness/defaults, per-setting permissions, activation timing, conflict code |
| API-051 | Labels, confidences, provenance; correction reason code | Method/path, allowed labels/reason codes, required body properties, response, revision/key rules |
| API-052 | Explicit new case revision preserving prior closed output | Method/path, reopening target, actors/approval guards, request/result |
| API-053 | Elevated actor, secondary reviewer, audited reason | Method/path, exact roles, reason constraints, hash/override binding, response |
| API-054, 055 | Workspace secret references; revocation and `CONNECTOR_REAUTH_REQUIRED` | Method/path, operator rights, credential/reauthorization transport and provider permissions |
| API-056 | Policy, encryption references, role bindings, quotas, connector stubs; idempotent workflow; incomplete visible state | Provisioning request/receipt/status schema and method/path; rollback/reconciliation behavior |
| API-057 | Authorized cited source version, page anchor, short-lived signed URL | Public route, binary versus URL response, media types, expiry/recovery |
| API-058 | Illustrated case/review counts, evidence coverage, service state, workflow summaries | Aggregate method/path, formulas, scope, units, fields, requiredness, refresh trigger |
| API-059 | Scoped Notification component | Channels, delivery/read status, fields, method/path, persistence, retry and UI destination |

**Sources:** S, p. 12, §2.2.1; pp. 24–25, §§6.1–6.2; p. 27, §7.1.2; p. 46, §12.3.2; p. 52, §14.3.1; pp. 57–59, Chapter 16; p. 78, §22.1.1; p. 7, Reference UI A.

### Request and Response Examples

#### Source-Confirmed Canonical Error Example

The following is the source example, including fictional correlation value and revisions. It does not define every error’s `details` schema.

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "error": {
    "code": "CASE_VERSION_CONFLICT",
    "message": "Case revision no longer matches.",
    "correlation_id": "trace_01HZZ_EXAMPLE",
    "retryable": false,
    "details": {
      "expected_revision": 7,
      "actual_revision": 8
    }
  }
}
```

**Source:** S, p. 84, A.3.

#### Proposal — Case Create and Receipt Shapes

These JSON properties and token transport are **Proposals**, not source-confirmed request/response schemas. The confirmed parts are the method/path, `Idempotency-Key`, `201`, case identity, initial `NEW`, and reference revision/sensitivity defaults. Resolve `API-OQ-001` and `API-OQ-003` before using this as an executable contract.

```http
POST /v1/cases
Authorization: Bearer <validated-access-token>
Idempotency-Key: <caller-operation-key>
Content-Type: application/json

{
  "workspace_id": "019ac000-0000-7000-8000-000000000041",
  "title": "Synthetic supply-chain discrepancy",
  "description": "Synthetic business context"
}
```

```json
{
  "id": "019ac000-0000-7000-8000-000000000042",
  "status": "NEW",
  "revision": 1,
  "sensitivity": "INTERNAL"
}
```

The UUID values and text are synthetic fixtures. Omission of impact, urgency, owner, or other inputs in this proposal does not establish optionality.

#### Proposal — SSE Wire Representation

Only SSE, monotonic offsets, `Last-Event-ID`, scoped retained-event backfill, and the cataloged `200` are confirmed. The media header, event name, payload names, and offset encoding below are **Proposals** pending `API-OQ-006`. Internal event envelopes must not be exposed wholesale to the browser by assumption.

```http
GET /v1/streams/runs/019ac000-0000-7000-8000-000000000042
Last-Event-ID: 7
```

```text
Content-Type: text/event-stream

id: 8
event: run_progress
data: {"status":"RETRIEVING"}
```

#### Source-Confirmed A2A Example

This source example is retained for traceability. Placeholder `tenant_id` and `case_id` values do not establish their production data types. The example lacks the declared output-schema property required conceptually by §11.2.2.

```json
{
  "task_id": "019ac000-0000-7000-8000-000000000042",
  "tenant_id": "tenant_example_01",
  "capability": "research.grounded_search.v1",
  "input_schema": "schema://oriondesk/research-request/1",
  "deadline_at": "2026-11-09T08:00:00Z",
  "trace_id": "trace_example_01",
  "authorization_ref": "grant_readonly_14",
  "payload": {
    "case_id": "case_demo",
    "query": "..."
  }
}
```

**Source:** S, p. 87, C.2.

**Example completeness rule — Needs confirmation:** Valid executable bodies/receipts for run, attachment, search, approval, settings, evaluation, sync, export, deletion, replay, and other unresolved interfaces depend on their open schemas. An invented `{}`, `operation_id`, `decision: "APPROVE"`, `max_items`, or classification property is not supplied as a confirmed example. Contract-approved examples must be added when those decisions are resolved.

## Processing and Consistency

### Validation and Durable Mutation Procedure

**API-VAL-001 — Confirmed:** Validate payloads before transaction entry, again at domain invariants, and before tool dispatch. Client validation is convenience only. Validate before allocating long-running work.  
**Source:** S, p. 56, §15.3.2; interface-boundary requirements throughout S.

For an applicable mutation:

1. Authenticate the caller and verify identity/tenant/service audience.
2. Validate route, query, headers, and the approved request schema.
3. Establish trace/correlation context independently of provider trace IDs.
4. Evaluate broad edge authorization.
5. Resolve idempotency outcome where required, preserving one accepted result.
6. Enter tenant-scoped transactional context.
7. Load current aggregate/resource attributes and re-evaluate authorization, revision, and domain guards.
8. Validate evidence/hash/policy conditions for the operation, including API-CLS-001 where run material is involved.
9. Write accepted business state, append required revision/decision evidence, and insert applicable outbox records atomically.
10. Commit before reporting accepted durable work or dispatching dependent side effects.
11. Return the cataloged success/result; otherwise reject safely without business mutation.
12. Dispatch/reconcile asynchronous indexing, model work, notifications, and other external effects using durable checkpoints.
13. Reset database connection-pool scoped context after every transaction.

**Confirmed procedure constraints:** Stale/unauthorized requests leave business state unchanged; each accepted transition has one accepted business outcome and correlated audit evidence.  
**Source:** S, p. 22, §5.2.2; p. 25, Design checkpoint 6.2; p. 45, Design checkpoint 12.2; p. 52, §14.2.1; p. 86, B.2.

**Needs confirmation — API-OQ-017:** Exact validation schemas, missing-precondition errors, transaction isolation level, locks, request-fingerprint canonicalization, and safe field-level errors. The steps above do not establish an undocumented database isolation mode or lock strategy.

### Data Reads, Writes, and Transaction Boundaries

| APIs / requirement | Confirmed reads | Confirmed writes / boundary | Remaining data contract |
|---|---|---|---|
| API-001 | Principal, authorized workspace/context | Case, creation lineage/outbox; `CaseCreated`; asynchronous classifier | Complete case/classification entities and receipt mapping |
| API-002, 016 | Current authorized case revision / case collection | No business mutation established by reading | Read schema, list snapshot, response projection |
| API-003 | Current case/revision, actor/workspace, applicable policy/approval | Case mutation and append-only `case_revisions`; outbox in ACID boundary; `CaseStateChanged` | Patch/history schema, edge-specific guards |
| API-017 | Approved answer, cited versions, review decisions, current case | Closure snapshot and immutable lineage | Closing edge, snapshot references |
| API-004, 018 | Case/source context, immutable document data/status | Accepted source metadata, immutable derivatives, extraction state/checkpoints; asynchronous indexing | Object-storage/write reconciliation details |
| API-005, 006, 019, 032, 033 | Case/workspace/tool/model policies, source ACL/classification, persisted workflow | Run/plan revision before side effects; step checkpoints before downstream dispatch | Run/artifact/budget/provenance schemas |
| API-008 | Allowed deployment, class/region policy, scoped evidence, token budget | Generation-attempt and token-usage records; `ModelInvocationCompleted` | Provider invocation/result/ledger schema |
| API-009, 025 | Connector capabilities/credentials/source state | Durable cursor/high-watermark/error ledger; tombstones/ACL cache invalidation | Cursor uniqueness, item outcomes, trust schema |
| API-010, 021, 022, 046 | Authoritative source permissions, anchors, index derivatives/cache | Evidence-set and query/cache records where applicable; no search-driven index mutation inferred | Public projection and classification/ACL provenance |
| API-023, 024 | Exact artifact, task/routing/role/hash/policy | Immutable approval decision and applicable outbox in ACID transaction | Task-state guards; decision enum |
| API-020 | Exact artifact/evidence, current permissions, approval/policy | Satisfied gate and final response pointer in the same transaction | Gate record/result schema |
| API-011 | Append-only audit/decision/access evidence | No edit of historical records | Public redaction/detail schema |
| API-012, 040, 042 | Usage/token/capacity/metric ledgers | Rollup/operational processing, not necessarily caused by GET | Units/aggregation/projection |
| API-013, 045 | Frozen versioned corpus/expected outputs and evaluated versions | Evaluation job, actual scorecard/release evidence; `EvaluationCompleted` | Evaluation entities/state/results |
| API-014, 015, 029, 035, 036 | Approval/hold/retention inventory and object versions | Export manifest; holds; tombstones; object/index purge; completion receipts | Scope and cross-store reconciliation |
| API-028, 050, 056 | Membership, configuration revision, provisioning state | Role/config bindings and durable audit; idempotent provisioning | API/schema/precondition details |
| API-030, 031 | Baseline/requirement/test lineage | Approved versioned governance record; `BaselineCommitted` | Approval/impact/revision data |
| API-034 | Original event, dead-letter ledger, scope, migration provenance | Replay ledger/provenance and resumed checkpoint outcomes | Replay receipt/schema |
| API-043, 044 | Signed image/build/config/schema/prompt/policy evidence | Reproducible release record and promotion evidence | Exact release operation/result |
| API-048 | Committed internal transition/outbound subscription scope | Asynchronous signed delivery/retry state | Webhook schema/delivery ledger |

**Source:** S, pp. 12, 24–26, 28–32, 37–42, 44–53, 62, 65–66, 71–80; p. 85, B.1.

**API-TXN-001 — Confirmed:** Case mutations, approval decisions, and outbox inserts commit in one ACID transaction. Search indexing and external webhooks are asynchronous with explicit reconciliation.  
**Source:** S, p. 52, §14.2.1.

**API-TXN-002 — Confirmed:** The publication pointer and satisfied approval gate commit atomically. A queue replay cannot publish a different artifact under an old approval.  
**Source:** S, p. 45, §12.3.1.

**API-TXN-003 — Confirmed:** Failed index writes do not roll back accepted source metadata. Reconciliation compares fingerprints and retries; broken links are repaired from the outbox ledger.  
**Source:** S, p. 49, §13.2.2.

### Idempotency and Concurrency

| Requirement ID | Confirmed rule | Applicability / unresolved transport |
|---|---|---|
| API-IDEM-001 | Every cross-service write is idempotent under retries. | S, p. 15, Chapter 3 invariant. Protocol-specific operation key and retention outside stated configurations Needs confirmation. |
| API-IDEM-002 | Job-creating POSTs require `Idempotency-Key`; identical repeated payload returns original operation; changed fingerprint with same key yields `IDEMPOTENCY_CONFLICT`. | API-004, 005, 009, 013–015, and other APIs if their confirmed operation allocates a long-running job. S, p. 54, §15.1.2. |
| API-IDEM-003 | Case creation uses an idempotency key; case key binds actor/request fingerprint to one outcome for 24 hours. | API-001 and applicable case mutations. Exact tenant/route/key namespace, simultaneous request behavior, error-result caching, and expiry handling Needs confirmation. S, p. 25, §6.2.2; p. 83, A.2; p. 89, `TST-001`–`002`. |
| API-IDEM-004 | Consumers deduplicate by event ID and operation key, detect stale aggregate revision, record duplicate outcome, and do not reapply business mutation. | All asynchronous consumers; no invariant depends on cross-partition queue ordering. S, p. 17, §3.3.2; p. 48, §13.1.2. |
| API-IDEM-005 | Reference workflow setting `replay_dedup_hours: 24`. | Configured replay baseline; not evidence that every HTTP operation or SSE stream has a 24-hour retention period. S, p. 90, Appendix F. |
| API-CNC-001 | Clients submit case `If-Match` revision conditions; conflicting update returns `CASE_VERSION_CONFLICT` with current revision. | API-003; case mutation conditions also affect closure. Header encoding and missing-header handling unresolved. S, p. 25, §6.2.2. |
| API-CNC-002 | Workspace configuration updates require revision preconditions and durable audit. | API-050; endpoint/header/code unresolved. S, p. 24, §6.1.1. |
| API-CNC-003 | Approval binds only the exact reviewed content hash; changed-artifact decision is stale. | API-024 and API-020; hash canonicalization/type unresolved. S, pp. 44–45, §§12.2–12.3. |
| API-CNC-004 | Rejected stale/unauthorized writes leave business state unchanged. | Applicable mutations; audit of rejection remains permitted/required. S, pp. 25 and 45, design checkpoints. |

**Needs confirmation — API-OQ-017:** Idempotency storage/key scope, request canonicalization, replay of errors, concurrent duplicate handling, retention for non-case HTTP keys, and lost-response recovery. Do not generalize case-key TTL to all protocols.

### Deterministic Policy and Maximum Included-Material Classification

**API-POL-001 — Confirmed:** Policy evaluates exactly the source-described concepts:

| Policy input concept | Required processing | Detailed schema status |
|---|---|---|
| Case sensitivity | Preserve the case’s classification context; do not use a lower case label to bypass API-CLS-001 | JSON/property mapping Needs confirmation |
| Requested action | Normalize authorized action context | Action vocabulary Needs confirmation |
| Evidence quality | Normalize extraction/retrieval quality | Thresholds and types Needs confirmation |
| Model class | Evaluate permitted model class | Registry/policy mapping Needs confirmation |
| Financial-impact category | Evaluate business impact category | Category values Needs confirmation |
| Confidence bands | Evaluate normalized confidence bands | Band definitions/thresholds Needs confirmation |

All inputs are normalized and stored with the rule-set version.  
**Source:** S, p. 44, §12.1.1.

**API-POL-002 — Confirmed:** Outcomes are `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, or `DENY`. An LLM may propose risk tags but cannot override the result.  
**Source:** S, p. 44, §12.1.2.

<a id="api-cls-001"></a>

**API-CLS-001 — Confirmed: Maximum included-material classification**

Data classes are `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, and `RESTRICTED`. For every run, **the model route, log redaction, retention, and approval policy depend on the maximum class of any material included in that run**.

| Control | Confirmed application of the aggregation rule | Related interfaces |
|---|---|---|
| Model route | Select and constrain initial/fallback deployment using the highest included-material class, not only the case sensitivity | API-005, API-008, API-026, API-032 |
| Log redaction | Apply the redaction policy associated with the highest included-material class; global prohibitions on document/secret diagnostics still apply | Run/model processing; API-011, API-040 and other diagnostics |
| Retention | Apply retention policy based on that highest class, preserving legal holds and immutable approved lineage | Run/artifact lifecycle; API-015, API-017, API-029, API-036 |
| Approval policy | Use the highest included-material class when determining approval requirements and validating publication | API-005, API-020, API-023, API-024 |

**Source:** S, p. 62, §17.2.1. Screen traceability: [Case sensitivity, `SCR-002-F10`](01_screen_functions.md#scr-002--case-detail); policy settings `SCR-007-F09`–`F11`.

**Confirmed consequences:**

1. An `INTERNAL` case that includes permitted `RESTRICTED` evidence must invoke `RESTRICTED` controls for all four categories.
2. Source ACL permission is necessary but not sufficient to select a lower model route or approval requirement.
3. Under the reference configuration, `require_human_review_for: [HIGH_RISK, RESTRICTED]` applies. `HIGH_RISK` is a risk category, not an additional information class.
4. `auto_publish_classification: INTERNAL` is not permission to auto-publish a run that includes `RESTRICTED` material or otherwise fails evidence/risk/approval gates.
5. The stored case’s lower sensitivity must not be treated as the complete run-control classification. The source does not require automatically rewriting the case sensitivity to implement this rule.
6. No additional public response property, client-controlled classification value, or seventh policy input is established. The rule is a shared control obligation across the existing run, model, policy, diagnostic, retention, and publication boundaries.

**Additional source:** S, p. 90, Appendix F; pp. 37–39, Chapter 10; pp. 44–46, Chapter 12.

**Needs confirmation — API-OQ-026:** Detailed material-classification provenance, normalization/storage/transport, treatment of unclassified material, policy-version activation, and per-class routing/redaction/retention/approval mappings. The aggregation rule itself is confirmed and must not be deferred as an optional design choice.

**API-POL-003 — Confirmed:** High-risk self-approval is prohibited. Reference `self_approval_allowed: false` remains a reference policy setting, not an undocumented toggle to bypass the prohibition. Overrides require elevated role, secondary reviewer, and audited reason; denied content is reworked as a new run revision, not retroactively approved.  
**Source:** S, p. 11, §2.1.2; p. 46, §12.3.2; p. 90, Appendix F.

### Events and Asynchronous Consistency

**API-EVT-001 — Confirmed event envelope:**

| Field | Meaning / type | Required | Constraints |
|---|---|---|---|
| `event_id` | Event identity; source UUIDv7 identifier policy | Yes | Deduplication identity; replay preserves original identity unless explicitly provenance-linked migration |
| `type` | Event type | Yes | Exact event-name vocabulary preserved; wire type/schema Needs confirmation |
| `schema_version` | Payload/envelope version | Yes | Type/version allocation Needs confirmation |
| `tenant_id` | Immutable event tenant | Yes | Tenant-scoped signed job context; UUID storage policy; envelope schema Needs confirmation |
| `aggregate_id` | Aggregate reference | Yes | Exact aggregate mapping per event Needs confirmation |
| `aggregate_revision` | Revision for stale/duplicate detection | Yes | Type and non-case revision representation Needs confirmation |
| `occurred_at` | Occurrence timestamp | Yes | UTC, RFC 3339 public timestamp conventions |
| `trace_id` | Trace context | Yes | Independent of provider trace |
| `payload` | Event-specific canonical JSON | Yes | Complete schemas/property names Needs confirmation |

Producers use UTC and canonical JSON. Durable mutation records also retain actor and correlation context; their exact envelope placement is not supplied by §13.1.1.  
**Source:** S, p. 48, §13.1.1; p. 22, §5.3.1; p. 51, §14.1.1.

#### Source Event Register

| Event | Producer / supported payload concepts | Consumer behavior / API relationship | Source |
|---|---|---|---|
| `CaseCreated` | Case Service; Case ID/revision | Run classifier after API-001; labels/confidences/provenance attach asynchronously | S, pp. 12–13; p. 87, C.1 |
| `DocumentNormalized` | Ingestion; version ID/source hash | Build index after API-004 normalization | S, pp. 30–32; p. 87, C.1 |
| `SearchIndexCommitted` | Indexer; index generation/document revision | Invalidate query cache; affects API-010/021/022 | S, pp. 34–36; p. 87, C.1 |
| `AgentPlanApproved` | Orchestrator; run ID/plan hash | Dispatch plan steps after durable plan revision | S, pp. 40–42; p. 87, C.1 |
| `ApprovalDecisionRecorded` | Policy Service; task/actor/content hash | Validate API-020 publication after API-024 | S, pp. 44–46; p. 87, C.1 |
| `WorkflowStageAdvanced` | Orchestrator; run/stage/checkpoint | Resume consumers; persisted run progress | S, pp. 48–50; p. 87, C.1 |
| `AccessDenied` | Policy Service; principal/action/policy digest | Alert enrichment and safe audit | S, pp. 21–23; p. 87, C.1 |
| `TenantDeletionVerified` | Retention Worker; manifest ID/receipt hash | Close purge record after verified lifecycle operation | S, pp. 78–80; p. 87, C.1 |
| `CaseStateChanged` | Producer and complete payload Needs confirmation | Correlated accepted case mutation/closure evidence | S, pp. 24–26, Chapter 6 |
| `RunRequested` | Producer and complete payload Needs confirmation | Chapter 3 run-request flow, API-032 | S, pp. 15–17, Chapter 3 |
| `ConnectorSyncStarted` | Producer and complete payload Needs confirmation | Durable sync initiation | S, pp. 27–29, Chapter 7 |
| `ModelInvocationCompleted` | Producer and complete payload Needs confirmation | Generation/usage completion evidence, not authorization | S, pp. 37–39, Chapter 10 |
| `UserReviewOpened` | Producer and complete payload Needs confirmation | Authorized review-open evidence under `SCR-005-A02`; endpoint/state-change mapping unresolved | S, pp. 57–59, Chapter 16 |
| `BaselineCommitted` | Producer and complete payload Needs confirmation | Accepted versioned governance evidence | S, pp. 8–10, Chapter 1 |
| `DeploymentPromoted` | Producer and complete payload Needs confirmation | Deployment evidence; not a GET health side effect | S, pp. 18–20, Chapter 4 |
| `DataRetentionPurgeCommitted` | Producer and complete payload Needs confirmation | Purge and receipt lineage | S, pp. 51–53, Chapter 14 |
| `ApiCompatibilityVerified` | Producer and complete payload Needs confirmation | Schema compatibility evidence; not an automatic OpenAPI GET mutation | S, pp. 54–56, Chapter 15 |
| `SecurityPolicyChanged` | Producer and complete payload Needs confirmation | Security-governance change evidence; settings/hold binding unresolved | S, pp. 61–63, Chapter 17 |
| `SloBurnRateDetected` | Producer and complete payload Needs confirmation | Operational alert/evidence | S, pp. 64–66, Chapter 18 |
| `BackpressureActivated` | Producer and complete payload Needs confirmation | Admission/degraded-mode evidence | S, pp. 68–70, Chapter 19 |
| `ReleasePromoted` | Producer and complete payload Needs confirmation | Release promotion evidence | S, pp. 71–73, Chapter 20 |
| `EvaluationCompleted` | Producer and complete payload Needs confirmation | Actual benchmark/release-gate evidence | S, pp. 74–76, Chapter 21 |

**API-EVT-002 — Confirmed:** At-least-once, duplicate, delayed, and stale delivery must be safe. Use event/operation deduplication and aggregate revision checks. Do not depend on order between queue partitions. Stateful workflows use transactional outbox or explicitly reconciled saga steps.  
**Source:** S, pp. 17 and 48–50, §§3.3.2 and 13.1–13.3.

**Needs confirmation — API-OQ-022:** Complete event schemas, actor/correlation placement, signatures, producer mappings not named in C.1, and which safe projections become SSE or webhook payloads.

### Timeouts, Retries, Backpressure, and Recovery

| Requirement ID | Confirmed behavior | Numeric/status/schema gaps |
|---|---|---|
| API-RTY-001 | Read operations may retry transient faults. Consequential mutable tool operations require idempotency keys and human authorization. Denied action cannot be replaced with an equivalent tool. | Per-read retry rules, attempts/delay, request deadlines unresolved. S, p. 42, §11.3.2. |
| API-RTY-002 | Transient workflow failures use bounded exponential backoff, jitter, per-dependency circuit breakers. Validation and permission failures are permanent and not retried. | Counts, delays, breaker thresholds/states, HTTP mapping unresolved. S, p. 49, §13.3.1. |
| API-RTY-003 | Connector workers honor `Retry-After`, workspace quotas, and fair scheduling. Poison records enter quarantine after bounded retries; remaining batch may proceed with ledger exception. | Retry count/schedule, batch bounds, remediation contract unresolved. S, pp. 28–29, §7.3. |
| API-RTY-004 | Structured model validation uses bounded retries; invalid output does not publish. | Attempt count, whether provider is re-invoked, and timeout/error transport unresolved. S, p. 38, §10.2.2. |
| API-TMO-001 | Orchestrator stops on missing approval, exhausted call budget, repeated invalid plans, policy denial, deadline expiry; reports exact failed checkpoint. | Relationship between waiting and missing-approval termination; recoverable timeout versus `FAILED`; review SLA unresolved. S, pp. 12, 41, 45, 49, and 82. |
| API-TMO-002 | Reference `max_plan_depth: 8`, `max_tool_calls: 16`, `run_timeout_seconds: 180`. | Budget inclusion of review wait and per-request/provider timeouts unresolved. S, p. 90, Appendix F. |
| API-BKP-001 | Admit new runs only when workspace tokens, queue age, and provider capacity meet thresholds; throttled client receives `429` and `Retry-After`; saved cases remain available. | Thresholds, permit schema, retry delay, concurrency quota policy unresolved. S, p. 69, §19.2.1. |
| API-DGD-001 | Generation outage leaves manual case/evidence work available; lexical fallback may continue with visible reduced quality. Safety checks remain enforced. | Degraded mode enum/quality-flag transport unresolved. S, pp. 68–70, Chapter 19; p. 79, §22.2.1. |
| API-REC-001 | Suspected ACL leak suspends affected aliases, revokes cached evidence, preserves audit traces, replays scoped ACL revisions; search resumes only after negative access tests pass. | Operational control methods/statuses unresolved. S, p. 79, §22.2.2. |
| API-REC-002 | Delayed indexing containment affects only faulty connector/indexer shard, preserving accepted source records; bounded validated replay; verify fingerprints and denied-access probes. | Replay job details unresolved. S, p. 90, F.1. |

**No automatic retry is authorized merely because an HTTP status/code is unspecified.** Unresolved caller retry behavior remains `API-OQ-017`.

### Privacy, Retention, and Contract Evolution

| Requirement ID | Confirmed requirement | Source / dependency |
|---|---|---|
| API-PRV-001 | Public responses never expose secrets or raw provider credentials. Errors exclude connector credentials, full prompts, retrieved documents, unauthorized resource existence. Diagnostic traces exclude documents/API secrets. | S, pp. 54–56, Chapter 15; p. 64, §18.1.1; p. 84, A.3 |
| API-PRV-002 | Providers receive only scoped context and structured prompts, never raw connector tokens or unrestricted database access; model/tools receive secrets only within declared scope. | S, p. 15, §3.1.1; p. 61, Chapter 17 invariant |
| API-RET-001 | Reference diagnostics default to 30 days; security audit retention is a distinct seven-year fictional policy; purge receipts/legal-hold exceptions retained. Apply API-CLS-001 where material classification determines retention. | S, pp. 62 and 66, §§17.2.1 and 18.3.2; p. 90, Appendix F |
| API-RET-002 | Corporate retention policy and per-class detailed mappings remain explicit decisions. The source does not assign a new retention period specifically to `RESTRICTED` run material. | S, p. 90, F.2; `API-OQ-021`, `API-OQ-026` |
| API-SCH-001 | Additive nonbreaking versioning; field removal requires migration; CI blocks incompatible deletion/enum changes; active readers must not lose required fields. | S, p. 15, §3.1.2; pp. 52 and 55, §§14.2.2 and 15.3.1 |
| API-SCH-002 | Expand-and-contract data migration: nullable additions, bounded backfill, then constraints. Do not remove fields while active readers depend on them. | S, p. 52, §14.2.2 |
| API-SCH-003 | Binary/prompt/policy versions and specific model deployments must be reconstructible. Re-evaluate prompt/model changes. | S, pp. 71–76, Chapters 20–21 |

## Errors and Acceptance Criteria

### Canonical Error Body

**API-ERR-001 — Confirmed canonical envelope:**

| Field | Type supported by source example | Required status | Constraints |
|---|---|---|---|
| `error` | JSON object | Canonical error container | No unsafe metadata |
| `error.code` | String | Canonical field | Preserve exact supported literals; naming inconsistency does not authorize changing them |
| `error.message` | String | Canonical field | Safe message; exact copy for other errors Needs confirmation |
| `error.correlation_id` | String | Canonical field | Safe diagnostic correlation, not a credential |
| `error.retryable` | Boolean | Canonical field | Actual retry policy; does not itself define number/delay |
| `error.details` | Safe structured JSON object in example | Optional | Per-error schema Needs confirmation |
| `error.details.expected_revision` | JSON integer in conflict example | Example-specific | Full-range `BIGINT` transport remains unresolved |
| `error.details.actual_revision` | JSON integer in conflict example | Example-specific | Current revision information required for case conflict |

**Source:** S, p. 84, A.3.

### Failure Register and Caller Behavior

“Caller handling Proposal” below identifies suggested presentation/recovery, not an undocumented mandatory client algorithm.

| Failure | Affected APIs | Confirmed HTTP / business outcome | Body / retry treatment | Caller action and unresolved details | Source |
|---|---|---|---|---|---|
| Missing tenant claim, unexpected token algorithm, invalid authenticated context | Protected APIs | Authentication rejected; exact HTTP/code Needs confirmation | Safe auth error; no protected result/work | Do not infer `401`/`403` or silently substitute tenant. Session recovery Needs confirmation. | S, p. 21, §5.1.1 |
| Foreign-tenant / absent identifier | Resource APIs | Same not-found class; `404`-equivalent non-disclosing error | No existence/content disclosure | Proposal: report unavailable resource without private metadata | S, p. 23, §5.3.2; p. 89, `TST-003` |
| Other permission / separation-of-duties denial | Mutations, queries, tools | Fail closed; exact HTTP/business code Needs confirmation | Permanent workflow failure; not retried | Do not infer `403` or treat `DENY` policy outcome as a new error code | S, pp. 22 and 49, §§5.2 and 13.3.1 |
| Schema-invalid request | REST interfaces | **`422`**; business code Needs confirmation | Canonical safe validation details | Correct approved-schema input; field-to-error mapping unresolved | S, p. 54, §15.1.1 |
| Stale case revision | API-003; applicable case mutation | **`409` `CASE_VERSION_CONFLICT`**; current revision | Canonical example has `retryable: false` | Proposal: reload current revision and reconcile explicitly; never silent overwrite | S, p. 25, §6.2.2; p. 84, A.3 |
| Same key, changed fingerprint | Idempotent operations | **`409` `IDEMPOTENCY_CONFLICT`** in source test; code confirmed generally | No second accepted outcome; precise details/retryable value unresolved | Do not report new job; caller key/body correction strategy Needs confirmation | S, p. 54, §15.1.2; p. 89, `TST-002` |
| Unsupported case transition / missing business guard | API-003, 017, 052 | Reject without state change; exact HTTP/code Needs confirmation | Safe domain failure | No invented transition/reopen default | S, p. 25, §6.2.1; p. 82, A.1 |
| Oversized/type-mismatched/decompression-unsafe file | API-004 | Fail closed; exact HTTP/code Needs confirmation | No unsafe downstream allocation/indexing | No invented `413`, `415`, or archive threshold. Safe remediation schema unresolved. | S, pp. 13 and 30, §§2.3.2 and 8.1.1 |
| Malware/unsafe attachment | API-004, 018 | Quarantine; no indexing | Safe processing status/reason | Do not expose unsafe viewing/download by assumption | S, p. 30, §8.1.2; p. 89, `TST-015` |
| Revoked connector credentials | API-009, 025 and queued jobs | **`CONNECTOR_REAUTH_REQUIRED`**; HTTP mapping Needs confirmation | Tokens excluded; reauthorization needed | Reauth flow API-055 unresolved; do not invent provider URL | S, p. 27, §7.1.2 |
| Insufficient confidence/quality/evidence | API-010, 021; orchestration | **`NO_SUPPORTED_EVIDENCE`**; HTTP/envelope mapping Needs confirmation | Not fabricated context | Clarification or human routing allowed, exact policy/transport unresolved | S, p. 36, §9.3.2 |
| Invalid model schema, unknown fields, invalid citations, control injection | API-008; run read/display | **`MODEL_OUTPUT_INVALID`**; no publish; HTTP mapping Needs confirmation | Bounded validation retries; safe checkpoint | No secret/prompt/source in error | S, p. 38, §10.2.2; p. 89, `TST-005` |
| Missing citations | Generation/publication | Needs-review or unsupported outcome; not approved answer | Exact mapping to model-validation versus evidence policy unresolved | Do not claim all missing citations necessarily use one error code | S, p. 89, `TST-009` |
| Wrong/changed reviewed hash | API-024, 020 | Stale rejection, audited; decision catalog includes **`409`** | Specific stale-approval code Needs confirmation | Reload exact candidate through confirmed detail delivery; no old-hash publication | S, p. 45, §12.2.2; p. 83, A.2; p. 89, `TST-006` |
| Required human approval absent, high-risk self-approval | API-005, 024, 020 | Cannot publish; exact HTTP/code/wait-versus-fail mapping Needs confirmation | Preserve awaiting/failed state distinction pending decision | Degradation or case label cannot bypass review | S, pp. 11, 41, 44–46, and 62 |
| Mixed classifications incorrectly lower controls | Run/model/policy/publication | API-CLS-001 prohibits lower-class controls; no additional error code established | Correct maximum-class policy; no auto publication bypass | Transport/details Needs confirmation; test through controlled policy fixtures | S, p. 62, §17.2.1; p. 90, Appendix F |
| Review expiry | API-023, 024, 020 | No implicit approval; reassignment/escalation recorded | Exact expired-task decision status/code unresolved | Display actual state; no ordinary stale-task approval | S, p. 45, §12.2.1; p. 89, `TST-010` |
| Quota / admission throttle | API-005 and applicable quotas | **`429`**; new-run response includes **`Retry-After`** | No run admission under failed thresholds | Honor defined retry guidance; saved cases available; no model/class downgrade | S, p. 69, §19.2.1 |
| Run token budget exhausted | API-008 / run workflow | Terminal current run; exact state/code Needs confirmation | No automatic model/data-class change | Report real failed checkpoint | S, p. 38, §10.3.1 |
| Deadline/call-budget/invalid-plan/policy stop | Run workflow | Termination/failure checkpoint; exact code/state mapping Needs confirmation | Preserve runtime/review-wait open question | No invented `TIMEOUT` state/code | S, p. 41, §11.3.1; p. 12, §2.3.1 |
| Dependency unavailable / lost response | Applicable APIs | Documented retryable error or persisted async identifier; never ambiguous success | Exact HTTP/code/receipt and attempts unresolved | Reuse operation identity where applicable; no uncontrolled new-job retry | S, Chapters 1–22; p. 49, §13.3.1 |
| Expired/invalid cursor or SSE offset | API-007, 011, 016, other paginated inquiries | **Needs confirmation** | Must not backfill private data outside current scope | Recovery/status/code unresolved; no invented reset behavior | S, pp. 54–55, §§15.1–15.2 |
| Webhook failure | API-048 | Internal transition remains committed | Signed delivery retry with exponential backoff | Recipient acknowledgment/retry taxonomy unresolved | S, p. 55, §15.2.2 |
| Insufficient export/delete approval | API-014, 015 | Single Admin rejected; exact HTTP/code Needs confirmation | No unauthorized package/purge | Independent workflow must be defined; no single-actor bypass | S, p. 78, Chapter 22 invariant; p. 88, `T-11` |
| Legal hold during purge | API-015, 036 | Protected records retained and receipted | Exact partial/completion state and error treatment unresolved | Do not retry as force-delete | S, p. 80, §22.3.2; p. 89, `TST-013` |
| Low confidence / safety regression in evaluation | API-013, 045, 043 | Release blocked; exact result schema/code Needs confirmation | Safety failure not overridden by benchmark score | No assumed automated promotion from API success | S, pp. 74–76; pp. 88–89, D.1 and `TST-016` |
| Historical audit/decision edit | Storage/administrative boundary | Prohibited and rejected; exact response Needs confirmation | Immutable historical evidence | No mutation endpoint is invented to test this prohibition | S, p. 62, §17.3.1; p. 88, `T-09` |

### Acceptance Criteria

All fixtures are synthetic. Include successful, empty, mixed-permission, mixed-classification, adversarial, malformed, duplicate, and delayed-delivery cases. Randomized tests record their seed. Critical isolation and approval cases pass with zero exceptions. Do not invent a source `TST` identifier for a newly specified test.

**Source:** S, p. 74, Chapter 21 invariant; p. 89, E.1–E.2.

| Acceptance ID | Related requirements / screens | Procedure | Expected result | Source / dependency |
|---|---|---|---|---|
| API-AC-001 | API-AUTH-001–004; all screens | Send token missing tenancy claim or using unexpected algorithm | Rejected before protected data/work; HTTP/code remain unresolved, not guessed | S, p. 21, §5.1.1; earlier `SF-AC-001` |
| API-AC-002 | API-001, API-IDEM-003; `SCR-001-A03` | Submit identical valid case create twice with same key | One case and identical response; `201`; case `NEW` | S, p. 83, A.2; p. 89, `TST-001` |
| API-AC-003 | API-001, API-IDEM-002–003 | Reuse key with changed body | `409 IDEMPOTENCY_CONFLICT`; no second case | S, p. 89, `TST-002` |
| API-AC-004 | API-002, API-AUTH-002 | Read valid case ID with foreign tenant token and compare to absent ID | Same `404`-equivalent non-disclosing class; no private metadata | S, p. 23, §5.3.2; p. 89, `TST-003` |
| API-AC-005 | API-003; `SCR-002-T01`–`T06` | For each confirmed edge, use current revision and fixture satisfying approved actor/evidence/approval guards | `200`, specified target, monotonic revision, one accepted correlated transition | S, p. 25, §6.2.1; detailed fixtures blocked by `API-OQ-004` |
| API-AC-006 | API-003, API-CNC-001 | Submit valid patch using stale `If-Match` | `409 CASE_VERSION_CONFLICT`, current revision information; business state unchanged | S, pp. 25 and 84; earlier `SF-AC-006` |
| API-AC-007 | API-003, API-AUTH-001 | Attempt unlisted normal edge or actor failing guard | Reject without mutation; undefined HTTP/code not invented | S, p. 25, §6.2.1 and checkpoint |
| API-AC-008 | API-017, 052; `SCR-002-A07`–`A08` | Close using confirmed-to-be-completed edge; inspect snapshot; attempt ordinary exit from `CLOSED` | Approved answer/cited versions/review history immutable; reopening only explicit new revision | S, pp. 24–26; executable close/reopen requests depend on `API-OQ-004` |
| API-AC-009 | API-051; `SCR-002-A03` | Correct classifier label under authorized request | Reason code accompanies correction; classification provenance retained | S, p. 12, §2.2.1; schema/catalog blocked by `API-OQ-005` |
| API-AC-010 | API-004, 018; `SCR-002-A05` | Upload allowed type meeting configured cap and MIME/extension rules | `202`, durable ingestion, scan before parse, immutable derivatives; not immediate search readiness | S, pp. 30–32; p. 83, A.2 |
| API-AC-011 | API-004; `T-04`, `SCR-002-F20` | Upload oversized, polyglot, active/malware, and zipped/decompression-unsafe fixtures | Fail closed; unsafe content quarantined, no indexing; no macros or embedded remote fetch | S, p. 30, §8.1; pp. 88–89, `T-04`, `TST-015`; size/error boundary depends on `API-OQ-007` |
| API-AC-012 | API-010, 021, 022; `SCR-003-A03` | Retrieve permitted anchored evidence and activate verified citation | Evidence item has five source-required semantic fields; opens cited immutable source and highlights anchor | S, pp. 31, 35, and 57; source delivery depends on `API-OQ-008` |
| API-AC-013 | API-010, API-AUTH-003; `SCR-003-A04` | Revoke source ACL after indexing, then query | No forbidden evidence on next query/model context; affected cache invalidated before release | S, p. 28, §7.2.2; p. 89, `TST-004` |
| API-AC-014 | API-010, 021 | Force insufficient evidence/confidence/quality | `NO_SUPPORTED_EVIDENCE`, not fabricated context; permitted clarification/human path only | S, p. 36, §9.3.2 |
| API-AC-015 | API-005–007, 019; `SCR-004-A01`–`A03` | Start admitted run; read stages; refresh; reconnect using last offset | `202` immediate durable run; server-reconstructed stages; monotonic scoped retained backfill; no duplicate mutation | S, pp. 55 and 58; p. 83, A.2 |
| API-AC-016 | API-005, 008; `SCR-004-A04` | Exceed depth/tool bounds or return recursive hints | Plan respects depth `8`/calls `16`; rejected/terminated before unauthorized/unbounded side effects; exact checkpoint visible | S, pp. 40–42; p. 88, `T-10`; p. 90, Appendix F |
| API-AC-017 | API-008 | Return unknown output fields, invalid citations, or control-character injection | `MODEL_OUTPUT_INVALID`; bounded validation retries; no publish | S, p. 38, §10.2.2; p. 89, `TST-005` |
| API-AC-018 | API-008, 020 | Return a draft with missing citations | Needs-review or unsupported outcome; no fabricated approval/publication | S, p. 89, `TST-009` |
| API-AC-019 | API-023, 024; `SCR-005-F05`–`F11` | Load exact candidate and leave required review fields incomplete | Exact review content/evidence/version/reasons accessible; Approve/Reject disabled; server validates approved required-field contract | S, pp. 57–58; field set blocked by `API-OQ-010` |
| API-AC-020 | API-024, API-POL-003; `SCR-005-A03` | Analyst attempts own high-risk approval | Rejected; no publication/pointer change | S, p. 11, §2.1.2; pp. 44–46 |
| API-AC-021 | API-024, 020, API-CNC-003 | Change candidate after review or approve wrong hash | Stale rejection and audit; old approval cannot publish another artifact | S, p. 45, §§12.2.2–12.3.1; p. 89, `TST-006` |
| API-AC-022 | API-023, 024, 020 | Expire review task under configured SLA | No implicit approval; escalation/reassignment recorded; acceptance after expiry follows approved guards | S, p. 45, §12.2.1; p. 89, `TST-010` |
| API-AC-023 | API-020, API-TXN-002 | Fail transaction between gate record and final-pointer change | No partially committed publication; gate/pointer commit together | S, p. 45, §12.3.1 |
| API-AC-024 | API-009, 025; `SCR-006-A02` | Replay partial sync and inspect cursor | Cursor advances only after durable preceding outcomes; one accepted outcome/item; exception ledger preserved | S, p. 28, §7.2.1 |
| API-AC-025 | API-009, 025 | Discover unsupported capability; revoke credentials before queued job executes | Visible lower-trust warning; queued job `CONNECTOR_REAUTH_REQUIRED`; no token exposure | S, p. 27, §7.1 |
| API-AC-026 | API-EVT-002; all event consumers | Replay same event `100` times and introduce delayed/stale revisions | Exactly one accepted business transition; duplicates recorded without reapplication | S, p. 88, `T-07`; p. 89, `TST-007` |
| API-AC-027 | API-005, 008, 009, API-BKP-001 | Inject provider `429` bursts | Capped retries/admission; throttled new-run client `429` plus `Retry-After`; saved cases remain available | S, p. 69, §19.2.1; p. 89, `TST-008` |
| API-AC-028 | API-DGD-001; `SCR-002-A11`, `SCR-003-F10` | Disable generation and degrade vector index | Manual edit/evidence APIs remain usable; lexical fallback reduced-quality flag visible; no authorization/approval bypass | S, p. 69, §19.2.2; p. 79, §22.2.1 |
| API-AC-029 | API-008, API-PRV-002 | Simulate approved deployment outage and unsafe fallback candidate | No restricted content sent to unapproved region/deployment; fallback only approved equal-or-stronger handling | S, p. 37, §10.1.2; p. 88, `T-06` |
| API-AC-030 | API-008, API-PRV-001–002, API-011 | Inspect public responses, errors, diagnostics, and provider requests | No unauthorized secrets/raw credentials/full error prompts/retrieved documents; no document/API-secret diagnostics | S, pp. 54, 61–64, and 84; p. 88, `T-05` |
| API-AC-031 | API-011; `SCR-008-A01`, `A04` | Query as authorized Auditor; attempt historical edit | `200` redacted immutable cursor log; historical modification rejected | S, pp. 62 and 83; p. 88, `T-09` |
| API-AC-032 | API-014, 015; `SF-SCP-007` | Attempt export as single Admin; then request independently authorized export | Single Admin rejected; authorized job `202`; package includes approved metadata/artifact/source/audit manifests/checksums, excludes secrets/internal prompts | S, pp. 78–79, 83, 88, `T-11` |
| API-AC-033 | API-015, 036, API-RET-001 | Purge inventory under legal hold | Protected records retained and receipted; no unverified deletion completion | S, p. 80, §22.3.2; p. 89, `TST-013` |
| **API-AC-034** | **API-CLS-001; API-005, 008, 020, 024; `SCR-002-F10`** | **Create an authorized `INTERNAL` case. Include permitted, anchored, quality-appropriate `RESTRICTED` evidence in its run. Use controlled approved routing/redaction/retention/approval policy fixtures. Invoke the run and generation flow, inspect policy-selected controls, and attempt publication without the required human decision.** | **The maximum included-material class is `RESTRICTED`. Model routing, log redaction, retention, and approval policy all select the applicable `RESTRICTED` controls, despite the case’s lower label and successful ACL checks. Under `require_human_review_for: [HIGH_RISK, RESTRICTED]`, required human review is enforced; the run cannot auto-publish using `auto_publish_classification: INTERNAL`. Publication remains blocked without satisfied review/evidence/hash policy. Verify through controlled internal policy/provenance evidence, not an invented public classification field. Exact per-class schemas/mappings depend on API-OQ-026.** | **S, p. 62, §17.2.1; p. 90, Appendix F; pp. 44–46, Chapter 12** |
| API-AC-035 | API-013, 045 | Evaluate frozen versioned corpus and inspect actual results | `202` creation; actual targets/metrics retained: precision `>=0.97`, unsupported rate `<=0.02`, high-risk recall `1.00`; domain confidence/shift reported | S, pp. 74–76; p. 83, A.2 |
| API-AC-036 | API-013, 045, 043 | Replace expected fixture manifest or force safety regression/low statistical confidence | Poisoned fixture control fails; critical safety/low-confidence outcome blocks release regardless of API success | S, p. 88, `T-12`, D.1; p. 89, `TST-016` |
| API-AC-037 | API-046–047 | Discover arbitrary tool/capability then attempt invocation without separate grant | `DENY` before dispatch; no arbitrary URL/filesystem access; discovery grants nothing | S, p. 87, C.2; p. 89, `TST-014` |
| API-AC-038 | API-034 | Replay without reason, dry-run validation, or scope limit; then perform authorized replay | Unguarded replay rejected; valid replay preserves original identity, except explicit provenance-linked migration | S, p. 50, §13.3.2 |
| API-AC-039 | API-035, API-AUTH-003 | Reuse pooled connection across tenants; read soft-deleted object | Scoped context reset; foreign object denied; soft-deleted entity unavailable | S, p. 51, §14.1.2; p. 86, B.2 |
| API-AC-040 | API-048, API-TXN-001 | Fail recipient delivery after committed case change | Case remains committed; signed delivery follows defined retries; recipient verifies age/signature | S, p. 55, §15.2.2 |
| API-AC-041 | API-050, 056 | Submit stale/unauthorized settings update; leave provisioning incomplete then sync | No settings mutation; durable revision/audit on valid update; incomplete provisioning visible and sync blocked | S, pp. 24 and 78; transport blocked by `API-OQ-014`, `016` |
| API-AC-042 | API-030, API-SCH-001 | Approve revised invariant without negative-test linkage; attempt incompatible field deletion with active client | Governance/schema gates reject invalid change; accepted revision has test lineage; old-reader field preserved | S, pp. 8, 52, and 55 |
| API-AC-043 | API-043–044 | Promote unverified digest or canary regression; inspect accepted release record | Unverified/regressed promotion blocked; accepted binary/schema/prompt/model-policy versions reconstructible; traffic rollback not automatic DB down-migration | S, pp. 71–73 |
| API-AC-044 | API-001, 010; `SF-AC-028` | Measure under reference workload | Case-create P95 under `300 ms`; search P95 under `1.5 s`, excluding remote connector fetch; generation measured separately | S, p. 65, §18.2.1; p. 68, §19.1.1 |
| API-AC-045 | API-REC-001–002; operational interfaces | Inject delayed indexing/ACL leak and execute controlled recovery | Accepted source durable; affected scope contained; fingerprints and denied-access probes verified before re-enable | S, p. 79, §22.2.2; p. 90, F.1 |
| API-AC-046 | API-SCP-002, API-038–039; recovery profile | Exercise network/object/relational recovery | No public datastore; only declared flows; reference RPO `<=15 minutes`, RTO `<=4 hours`, with relational/object consistency | S, pp. 18–20; p. 69, §19.3.1; p. 89, `TST-012` |

**Reference performance envelope:** `2,000` active daily users, `60` requests/second steady state, `180` requests/second burst, maximum `100,000` indexed documents per tenant, and `20` concurrent AI runs per large tenant. These are fictional reference assumptions, not universal public request limits. Public API availability target is `99.9%` monthly.  
**Source:** S, pp. 65 and 68, §§18.2.1 and 19.1.1.

## Consistency and Open Questions

### Consistency Findings and Required Amendments

Earlier specifications are not rewritten here. Confirmed source requirements take precedence over incomplete transport contracts; previously labeled proposals remain proposals.

| Consistency ID | Evidence / issue | Affected identifiers | Required clarification or amendment |
|---|---|---|---|
| API-CNS-001 | Case normal transition contract is partial, not absent. Six edges are explicit; closure origin/reopening target are not. S, pp. 24–26, §6.2.1; p. 82, A.1. | API-003, 017, 052; `SCR-002-T01`–`T08`; `SF-CON-003`; earlier `OQ-008` | Preserve six edges/CLOSED finality. Complete only closing/reopening and detailed guards. No inferred `RESOLVED → CLOSED` or automatic Reject transition. |
| API-CNS-002 | Both `POST /v1/runs` and case-scoped run route occur. S, pp. 15–17 and 40–42; p. 83. | API-005, 032; `SF-CON-007`; earlier `OQ-011` | Decide distinct/alias/amendment relationship without deleting source occurrences or inventing equivalence. |
| API-CNS-003 | Waiting for review, missing-approval termination, recoverable timeout, and `FAILED` vocabulary coexist. S, pp. 12, 41, 45, 49, 82, 90. | API-005–007, 019–020, 024; API-TMO-001–002; `SF-CON-004` | Define runtime versus review SLA and timeout representation. Do not invent state literals. |
| API-CNS-004 | Role archetype/catalog scope mismatch. S, pp. 11, 22, 83. | API-AUTH-005; APIs with `Owner`, `Member`, `approver`; `SF-CON-008` | Confirm role/scope mapping and independent approver eligibility; no broad grants by terminology assumption. |
| API-CNS-005 | Domain case fields exceed abbreviated reference DDL. S, p. 24, §6.1.2; pp. 85–86. | API-001–003, case field table; `SF-CON-006` | Data Specification must preserve title/description/priority/owner/approved result and complete types rather than exclude omitted fields. |
| API-CNS-006 | Human case references in mockups are not UUIDv7 API identities. S, p. 14, Figure 2.2; p. 51, §14.1.1. | API shared paths, API-001–003; `SCR-001-F01`, `SCR-002-F01`; `SF-CON-002` | Define separate business reference if required; no conversion rule is established. |
| API-CNS-007 | General error wording says snake-case; literal examples use uppercase snake-case. S, pp. 54 and 84. | API-ERR-001; failure register; `SF-CON-005` | Preserve exact existing codes; settle future naming separately. |
| API-CNS-008 | Chapter 22 says tenant export/deletion; routes use `workspaceId`; two independent checks and `Admin + approver` are both stated. S, pp. 78–83. | API-014–015; `SF-CON-010`; earlier `OQ-023` | Specify operation extent and independent workflow/actors; do not infer two approvals by one actor. |
| API-CNS-009 | MCP `query`, `case_id`, `max_items` are not public search request properties. S, pp. 83 and 87. | API-010, 046; `SCR-003-F01`, earlier `OQ-017` | Keep contracts separate. Retrieval budgets are not public pagination limits. |
| API-CNS-010 | A2A §11.2.2 requires declared input/output schemas; C.2 example only has `input_schema` and fictional non-UUID placeholders. S, pp. 41 and 87. | API-047; source example | Complete output-schema field and ID types; do not invent a property name or treat placeholders as production schema. |
| API-CNS-011 | Repeated chapter boundary text associates GET endpoints with chapter events/durable metadata. It does not define each GET as a business mutation or job-creating operation. S, Chapters 1–22. | API-031, 037–042, 044 and event register | Clarify GET fallback/read projections. Do not add idempotency-required reads or promotion events as GET side effects. |
| API-CNS-012 | Workspace settings §6.1.1 is adjacent to case PATCH, but does not define workspace update routing. S, p. 24. | API-049–050; `SCR-007-A01`–`A02` | Confirm settings APIs; do not repurpose case PATCH as workspace update. |
| API-CNS-013 | Source evidence uses maximum material class for four controls. Earlier `SCR-002-F10` says policy uses maximum class but does not explicitly list all four controls in that field contract. S, p. 62, §17.2.1. | **API-CLS-001; API-005, 008, 020; API-AC-034; `SCR-002-F10`; `SCR-007-F09`–`F11`; earlier `OQ-010`, `OQ-020`** | **Required amendment to the affected earlier field/policy contract: explicitly link maximum included-material class to model routing, log redaction, retention, and approval policy. This specification supplies the confirmed shared API obligation; detailed JSON/provenance transport remains unresolved. Do not reduce aggregation to case label, introduce a seventh policy input, or infer automatic case-label rewriting.** |
| API-CNS-014 | `auto_publish_classification: INTERNAL` must coexist with `require_human_review_for: [HIGH_RISK, RESTRICTED]`, maximum-material classification, evidence, and exact-hash gates. S, pp. 44–46, 62, 90. | API-POL-001–003, API-CLS-001, API-020; `SF-CON-009` | Complete configuration semantics without an INTERNAL-case bypass. API-AC-034 verifies the mixed-class case. |
| API-CNS-015 | Source confirms diagnostic 30-day/audit seven-year reference retention but leaves corporate retention choice open. No RESTRICTED-specific duration is supplied. S, pp. 62, 66, 90. | API-RET-001–002; API-CLS-001; API-015, 036 | Preserve baseline defaults and classification-dependent selection; confirm detailed retention mappings without inventing durations/schedules. |
| API-CNS-016 | Illustrations contain mixed workflow labels and dashboard coverage; they are not API enums or benchmark precision. S, pp. 7, 14, 57, 75, 82. | API-058; API-045; `SF-CON-001`, `SF-CON-011`; earlier `OQ-027` | Preserve separate Case/Run/Review/artifact vocabularies; define dashboard formulas and aliases separately. |
| API-CNS-017 | Source provides internal storage, health, metrics, capacity, OpenAPI, and release routes that were not all individually listed in Stage 1. Their existence does not establish new screens. | API-035–044; `SF-SCP-008`, earlier `OQ-024` | Retain source APIs in Stage 2; add screen bindings only if separately confirmed. |

### API Open-Decision Register

These items appear beside affected contracts. No decision, owner, deadline, or approval is created here.

| Question ID | Status | Unresolved decision / contract | Affected API requirements | Earlier links and source |
|---|---|---|---|---|
| API-OQ-001 | Needs confirmation | Identity provider; token algorithms/audiences/claim names/transport; BFF/cookie selection; principal response; role/scope mapping; membership/tenant context selection | API-AUTH-001–005; API-027–028; public APIs | [Stage 1 `OQ-001`–`003`](01_screen_functions.md#consistency-and-open-questions). S, pp. 21–23, 83, 90. |
| API-OQ-002 | Needs confirmation | Internal caller identities, service audiences/scopes, HTTP/gRPC/mTLS configuration, workload identity, operational auth and exposure | API-008, 033–044, 046–047 | Earlier `OQ-022`, `OQ-024`. S, pp. 15–20, 54–56. |
| API-OQ-003 | Needs confirmation | Full case create/read/patch/list schemas; field requiredness/length/defaults; public exposure; BIGINT transport; `If-Match` syntax; cursor/list capabilities; business reference | API-001–003, 016; API-CNC-001, API-PAGE-001 | Earlier `OQ-006`–`007`, `SF-CON-002`, `SF-CON-006`. S, pp. 24–26, 54, 57–59, 83–86. |
| API-OQ-004 | Needs confirmation | Closing edge/request/result/actor; new-revision reopening target/operation; detailed six-edge guards and approval-to-case-state linkage | API-003, 017, 052 | [Case transitions](01_screen_functions.md#confirmed-case-state-transitions), earlier `OQ-008`, `SF-CON-003`. S, pp. 24–26, 44–46, 82. |
| API-OQ-005 | Needs confirmation | Impact/urgency/priority matrix, business calendars/timezone/deadlines; classifier/correction catalogs/confidence schema; sensitivity lowering permissions | Case fields, API-051 | Earlier `OQ-009`–`010`. S, pp. 12, 25, 62. |
| API-OQ-006 | Needs confirmation | Run route relationship; request/receipt/steps/SSE; admission thresholds; runtime versus review wait; timeout state; offset syntax/retention/recovery; end-user cancel/retry if supported | API-005–007, 019, 032; API-TMO-001–002 | [Run Timeline](01_screen_functions.md#scr-004--run-timeline), earlier `OQ-011`, `SF-CON-004`, `SF-CON-007`. S, pp. 12, 15–17, 40–42, 49, 55, 58, 69, 82, 90. |
| API-OQ-007 | Needs confirmation | Upload transport/file count/name/MIME representation/MB conversion/archive threshold; binary fingerprint; OCR input; status schema; quality thresholds/quarantine remediation | API-004, 018 | Earlier `OQ-015`. S, pp. 30–32, 82–83, 90. |
| API-OQ-008 | Needs confirmation | Public search schema/filters/pagination; evidence-ID mapping; source response; signed-URL lifetime; immutable version/anchor/page/bbox conventions; unsupported-evidence workflow | API-010, 021–022, 035, 057 | [Evidence Viewer](01_screen_functions.md#scr-003--evidence-viewer), earlier `OQ-017`–`018`. S, pp. 31, 34–36, 52, 57, 83, 87. |
| API-OQ-009 | Needs confirmation | Generation schema/key/deadline/provider adapter; approved models/regions/deployments; token budget/fallback; model-catalog response/permissions | API-008, 026 | Earlier `OQ-020`, `OQ-022`. S, pp. 37–39, 90. |
| API-OQ-010 | Needs confirmation | Review queue/detail/decision/gate schema; required fields; literal decisions; hash/canonicalization; assignment/expiry/state guards; override actors/transport; direct draft editing or publish control if supported | API-020, 023–024, 053; API-CNC-003 | [Review Inbox](01_screen_functions.md#scr-005--review-inbox), earlier `OQ-012`–`014`. S, pp. 44–46, 57–59, 82–85. |
| API-OQ-011 | Needs confirmation | Connector providers/permissions; trust/capability schema; sync options/states/cursor; read/configuration rights; credential lifecycle APIs; retries | API-009, 025, 054–055 | [Connector Health](01_screen_functions.md#scr-006--connector-health), earlier `OQ-016`, `OQ-022`. S, pp. 27–29, 78, 90. |
| API-OQ-012 | Needs confirmation | Audit response/detail/redaction/filters/cursor/digest; permissions beyond Auditor; classification-aware redaction projection | API-011 | [Audit Explorer](01_screen_functions.md#scr-008--audit-explorer), earlier `OQ-019`. S, pp. 11, 62, 83, 85. |
| API-OQ-013 | Needs confirmation | Usage units/currency/scopes/time windows; evaluation setup/version/state/results/read scope/progress; signed corpus-manifest verification | API-012–013, 045 | [Usage & Quality](01_screen_functions.md#scr-010--usage--quality), earlier `OQ-021`. S, pp. 64–66, 74–76, 83. |
| API-OQ-014 | Needs confirmation | Workspace settings read/update methods/paths, schema/permissions/preconditions/activation/conflicts; deterministic threshold/reviewer/quota/tool mappings | API-049–050; API-POL-001–003 | [Policy Settings](01_screen_functions.md#scr-007--policy-settings), earlier `OQ-020`. S, pp. 24, 37–39, 44–46, 90. |
| API-OQ-015 | Needs confirmation | Export/delete tenant-versus-workspace extent, two independent checks/actors/proof, requests/status/download/receipts/package/checksum formats, partial holds/failures | API-014–015, 036 | Earlier `OQ-023`, `SF-CON-010`. S, pp. 78–80, 83, 88–89. |
| API-OQ-016 | Needs confirmation | Membership/hold/provisioning methods where missing, schemas/rights/revisions/idempotency; hold release and provisioning recovery | API-028–029, 056 | Earlier `OQ-002`, `OQ-003`, `OQ-024`. S, pp. 21–23, 61–63, 78–80. |
| API-OQ-017 | Needs confirmation | Non-case key TTL/scope/canonicalization, concurrent duplicates/error replay, missing headers, transaction isolation/locking, unknown HTTP/business codes, safe details, dependency fallback and caller retries | API-IDEM/CNC/TXN/ERR; all incomplete failures | Earlier `OQ-005`, `OQ-007`, `OQ-011`. S, pp. 25, 42, 49, 52, 54–56, 84. |
| API-OQ-018 | Needs confirmation | Health/readiness checks/statuses/probe auth, metrics/capacity modes/schema/units/thresholds, operational response timeouts/exposure | API-038–042 | Earlier `OQ-024`; S, pp. 18–20, 64–70. |
| API-OQ-019 | Needs confirmation | Workflow/replay/storage inquiry schemas; operator rights/reason/scope limits/dry-run transport; migration provenance | API-033–035 | Earlier `OQ-024`. S, pp. 48–53, 90 F.1. |
| API-OQ-020 | Needs confirmation | Design/release decision schemas, impact scale, approval actor/record, version allocation, digest/build/sign-off/canary proof and results | API-030–031, 043–044 | Earlier `OQ-024`. S, pp. 8–10, 71–73. |
| API-OQ-021 | Needs confirmation | Corporate/class-dependent retention mapping; purge eligibility/schedules/inventory/receipts; key isolation/rotation and region selection | API-RET-001–002, API-CLS-001, API-015, 017, 029, 036 | Earlier `OQ-020`, `OQ-022`–`023`. S, pp. 10, 26, 51–53, 62–63, 66, 80, 90. |
| API-OQ-022 | Needs confirmation | Full OpenAPI/protobuf versions; event schemas/producers, actor/correlation placement/signatures; compatibility publication and SSE/webhook projections | API-037, API-EVT-001–002 | Earlier integration register and `OQ-011`, `OQ-024`. S, pp. 48–50, 54–56, 82, 87. |
| API-OQ-023 | Needs confirmation | MCP/A2A transports, scopes, errors, optionality/lower bounds, `Citation`, output-schema property, grant verification/decline result | API-046–047 | Earlier external integration register. S, pp. 41–42, 87. |
| API-OQ-024 | Needs confirmation | Webhook method/recipient/subscription management, signature/age headers, canonical bytes, retry/acknowledgment contract | API-048 | Earlier `OQ-024`. S, p. 55, §15.2.2. |
| API-OQ-025 | Needs confirmation | Dashboard APIs/formulas/labels/refresh; notification channels/state/fields/endpoints and screen placement for nonprimary capabilities | API-058–059 and unbound APIs | Earlier `OQ-004`, `OQ-024`–`025`, `OQ-027`. S, pp. 7, 14, 57–59. |
| **API-OQ-026** | **Needs confirmation** | **Material-classification provenance/storage/transport; per-class model-route/log-redaction/retention/approval mappings; unclassified-material and policy-version handling. The maximum included-material aggregation across all four controls is already Confirmed, not an open permission to omit it.** | **API-CLS-001; API-005, 008, 020, 024; API-AC-034** | **Earlier `SCR-002-F10`, `SCR-007-F09`–`F11`, `OQ-010`, `OQ-020`, `OQ-022`; S, p. 62, §17.2.1; p. 90, Appendix F.** |

### Carry-Forward Dependencies

| Later specification | Required carry-forward | Links / requirement IDs |
|---|---|---|
| Data Specification | Complete source-supported domain fields and public/storage mapping; UUID/UUIDv7 and BIGINT transport; case revision history; immutable document versions/anchors; run/artifact/plan/budget; evidence ACL and classification provenance; hash-bound approvals; append-only audit/outbox; cursor/token/policy/deletion records; retention and legal holds | `02_api.md`: API-IF-001–002, API-AUTH-003, API-TXN-001–003, API-CNC-001–004, **API-CLS-001**, API-EVT-001, API-OQ-003–004, 007–010, 015–017, 021, 026. [Stage 1 field contracts](01_screen_functions.md#functions-by-screen). **To be defined in a later stage.** |
| Processing / Workflow Specification | Six case edges and missing guards; closing/reopening; classifier correction; safe ingestion/quality gates; bounded plan/checkpoints; maximum-class control selection; review wait/expiry/override; exact-hash atomic publication; fair sync/admission; replay/reconciliation; degraded and incident paths | API-003–005, 008–010, 017–020, 024, 032–036, 050–056; API-POL-001–003, **API-CLS-001**, API-RTY/TMO/BKP/DGD/REC requirements. **To be defined in a later stage.** |
| Exception Handling Specification | Preserve confirmed HTTP meanings and exact literal codes; define missing statuses/codes safely; classify retryable/permanent failures; cursor/SSE expiry; quarantine; stale decisions; mixed-class policy enforcement; dependency ambiguity/lost responses; partial purge/hold outcomes; safe caller recovery | API-ERR-001, failure register, API-OQ-006–010, 015, 017–019, 024, 026; earlier [Failure-Display Contract](01_screen_functions.md#failure-display-contract). **To be defined in a later stage.** |
| Architecture / Security Specifications | Identity/service/probe boundaries; private datastores/declared egress; provider/search/region choices; tenant encryption-key isolation; specific approved model deployments; separate tool authorization; signed task/event/webhook transport; corporate retention; compatibility and deployment evidence | API-AUTH-001–005, API-PRV-001–002, API-SCH-001–003, API-OQ-001–002, 009, 011, 018, 020–024, 026; earlier `OQ-022`. **To be defined in a later stage.** |
| Stage 8 architecture decision consolidation | Consolidate only completed Markdown specifications. Link unresolved items back to `01_screen_functions.md`, `02_api.md`, and their requirement/question IDs, including **API-CLS-001**, **API-AC-034**, and **API-OQ-026**. Do not create presumed decisions, owners, deadlines, or approvals. | `08_architecture_decision.md` is **To be defined in a later stage**. |

**Implementation boundary:** Confirmed behavior must be implemented and tested. Unresolved transport, schema, role, error, numeric policy, and lifecycle choices must remain explicit blocking decisions; neither an illustrative example nor a repeated proposal constitutes approval.
