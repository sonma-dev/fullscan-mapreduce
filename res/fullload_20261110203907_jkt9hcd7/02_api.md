# 2. API Specification

## API Inventory and Responsibilities

### Baseline and Evidence Status

This specification covers OrionDesk AI **OD-AI-DDS-001, R1.0 / revision 1.3** and preserves screen and event identifiers from [01_screen_functions.md](01_screen_functions.md).

**Source** means `1794310747-OrionDesk_AI_Detailed_Design_Specification.pdf`; citations use original PDF page numbers.

- **Confirmed:** Explicit source requirements, including the fictional baseline's contracts and constraints.
- **Needs confirmation:** Missing or conflicting contract details. These are implementation blockers, not permission to select an arbitrary behavior.
- **Proposal:** Explicitly suggested examples or design choices; not approved contracts.

API identifiers below are assigned here because the source declares the `API` namespace but does not assign individual endpoint identifiers. Source test, event, tool and schema identifiers are retained.

### Authentication Profiles

| Profile | Confirmed requirements | Needs confirmation | Evidence |
|---|---|---|---|
| AUTH-P — Public API | Authenticated principal and tenant; interactive OIDC authorization-code flow with PKCE. Validate issuer, audience, expiry, subject and tenant; reject unexpected token algorithms or missing tenancy claims. | Issuer, audience literals, accepted algorithms, transport header/session contract, token lifetimes and authentication error codes. BFF cookies are a source option, not a settled decision. | Source, pp. 21–23, §§5.1–5.3 |
| AUTH-I — Internal API | Independent service authorization; mTLS-authenticated HTTP or gRPC, service audience checks, scoped IAM and separate workload identities. Propagate immutable tenant identity and correlation context. | Per-service grants, audience literals, exact HTTP-versus-gRPC selection and internal token/header schemas. | Source, pp. 16, 18, 22, 54–55 |
| AUTH-T — Tools / agents | Scoped service credentials, invoking-principal authorization, workspace policy, tool scope and data classification. Discovery does not authorize execution. | MCP transport, A2A transport and grant-reference verification protocol. | Source, pp. 41–42, 87 |

**API-R-001 — Confirmed:** All inventory entries inherit the applicable authentication profile. Public resource authorization combines role, tenant, workspace membership, sensitivity, document ACL, action and segregation of duties. Domain services reevaluate resource attributes within the transaction; retrieval filters ACLs before releasing text to generation. No endpoint is implicitly anonymous, including health and OpenAPI endpoints. Whether those operational endpoints need a special authenticated probe profile **Needs confirmation**.  
**Evidence:** Source, pp. 18–23, 54–56.

### Browser and Public API Inventory

`Sync` means request/reply; `Async` means an accepted durable operation with later processing. It does not mean processing has completed.

| ID | Purpose / responsibility | Calling screen operation | Method and path | Behavior / success | Auth profile and authorization | Evidence |
|---|---|---|---|---|---|---|
| API-001 | Create case | SCR-001-E04 | `POST /v1/cases` | Sync creation; `201`; classification Async | AUTH-P; Analyst | Source, pp. 12, 83, 87 |
| API-002 | List permitted cases | SCR-001-E01–E02 | `GET /v1/cases` | Sync, cursor pagination; success code Needs confirmation | AUTH-P; list role scope Needs confirmation | Source, pp. 57–59 |
| API-003 | Read current case revision | SCR-002-E01 | `GET /v1/cases/{caseId}` | Sync; `200` | AUTH-P; Analyst / Reviewer | Source, p. 83 |
| API-004 | Mutate case | SCR-002-E02 | `PATCH /v1/cases/{caseId}` | Sync; `200`; conflict `409` | AUTH-P; Owner | Source, pp. 24–26, 83 |
| API-005 | Close and snapshot case lineage | SCR-002-E06 | `POST /v1/cases/{caseId}/close` | Mutation; processing mode / success code Needs confirmation | AUTH-P; closure scope Needs confirmation | Source, pp. 24–26 |
| API-006 | Attach file and start ingestion | SCR-002-E04 | `POST /v1/cases/{caseId}/attachments` | Async; `202` | AUTH-P; Analyst | Source, pp. 30–32, 83 |
| API-007 | Read document processing status | SCR-002-F15–F16; exact event mapping Needs confirmation | `GET /v1/documents/{documentId}/status` | Sync; success code Needs confirmation | AUTH-P; document ACL; role scope Needs confirmation | Source, pp. 30–32 |
| API-008 | Start case-grounded workflow | SCR-002-E05 | `POST /v1/cases/{caseId}/runs` | Async; `202` | AUTH-P; Analyst | Source, pp. 12, 40–42, 83 |
| API-009 | Alternative run creation surface | Same journey; canonical mapping unresolved | `POST /v1/runs` | Async run request; success code Needs confirmation | AUTH-P; exact role scope Needs confirmation | Source, pp. 15–17 |
| API-010 | Read run stages / evidence metadata | SCR-004-E01, E03 | `GET /v1/runs/{runId}` | Sync; `200` | AUTH-P; Analyst / Reviewer | Source, pp. 16–17, 83 |
| API-011 | Read persisted run steps | SCR-004-E01 | `GET /v1/runs/{runId}/steps` | Sync; success code Needs confirmation | AUTH-P; exact scope Needs confirmation | Source, pp. 40–42 |
| API-012 | Stream resumable run progress | SCR-004-E02; SCR-002-E05 | `GET /v1/streams/runs/{runId}` | SSE; `200` | AUTH-P; Analyst / Reviewer, scoped backfill | Source, pp. 55, 83 |
| API-013 | Search permitted knowledge | SCR-003-E02 | `POST /v1/search` | Sync; `200` | AUTH-P; Member + document ACL | Source, pp. 34–36, 83 |
| API-014 | Read evidence item | SCR-003-E01, E03 | `GET /v1/evidence/{evidenceId}` | Sync; success code Needs confirmation | AUTH-P; current evidence/source access; role scope Needs confirmation | Source, pp. 34–36 |
| API-015 | Read case evidence | SCR-003-E01; SCR-005-E01 | `GET /v1/cases/{caseId}/evidence` | Sync; success code Needs confirmation | AUTH-P; permitted case and sources; role scope Needs confirmation | Source, pp. 57–59 |
| API-016 | Read assigned review queue | SCR-005-E01 | `GET /v1/review-queue` | Sync list; success code Needs confirmation | AUTH-P; reviewer eligibility / pools / minimum role / segregation of duties | Source, pp. 45–46 |
| API-017 | Capture binding review decision | SCR-005-E02 | `POST /v1/approvals/{approvalId}/decision` | Sync; `200`; stale conflict `409` | AUTH-P; eligible Reviewer | Source, pp. 44–46, 83 |
| API-018 | Initiate incremental connector sync | SCR-006-E01 | `POST /v1/connectors/{connectorId}/sync` | Async; `202` | AUTH-P; Admin | Source, pp. 27–29, 83 |
| API-019 | Read connector sync history | SCR-006-E02 | `GET /v1/connectors/{connectorId}/runs` | Sync list; success code Needs confirmation | AUTH-P; exact read scope Needs confirmation | Source, pp. 28–29 |
| API-020 | Read model catalog | SCR-007-F02; invocation mapping Needs confirmation | `GET /v1/model-catalog` | Sync; success code Needs confirmation | AUTH-P; exact scope Needs confirmation | Source, pp. 37–39 |
| API-021 | Read immutable audit events | SCR-008-E01–E02 | `GET /v1/audit/events` | Sync, cursor pagination; `200` | AUTH-P; Auditor, redacted scope | Source, pp. 61–63, 83 |
| API-022 | Read usage / cost / quota estimates | SCR-010-E01 | `GET /v1/usage` | Sync; `200` | AUTH-P; Admin | Source, pp. 64–66, 83 |
| API-023 | Start frozen benchmark | SCR-010-E02 | `POST /v1/evaluations` | Async; `202` | AUTH-P; Admin | Source, pp. 74–76, 83 |
| API-024 | Read evaluation | SCR-010-E03 | `GET /v1/evaluations/{evaluationId}` | Sync; success code Needs confirmation | AUTH-P; exact read scope Needs confirmation | Source, pp. 74–76 |
| API-025 | Export workspace with manifest | SF-014; dedicated screen undefined | `POST /v1/workspaces/{workspaceId}/export` | Async; `202` | AUTH-P; Admin + approver; two independent checks | Source, pp. 78–80, 83 |
| API-026 | Legal-hold-safe workspace deletion | SF-014; dedicated screen undefined | `POST /v1/workspaces/{workspaceId}/delete` | Async; `202` | AUTH-P; Admin + approver; two independent checks | Source, pp. 78–80, 83 |
| API-027 | Read authenticated identity context | INT-SF-001; shared screen prerequisite | `GET /v1/me` | Sync; success code Needs confirmation | AUTH-P; principal scope | Source, pp. 21–23 |
| API-028 | Maintain workspace membership | SF-014 | `PUT /v1/workspaces/{workspaceId}/members` | Mutation; mode / success code Needs confirmation | AUTH-P; exact role scope Needs confirmation | Source, pp. 21–23 |
| API-029 | Create security hold | SF-014 | `POST /v1/security/holds` | Mutation; mode / success code Needs confirmation | AUTH-P; exact role scope Needs confirmation | Source, pp. 61–63 |
| API-030 | Serve REST contract | REST clients / tooling; no confirmed screen | `GET /v1/openapi.json` | Sync; success code Needs confirmation | AUTH-P; exact scope Needs confirmation | Source, pp. 54–56 |
| API-031 | Report degraded modes | Browser / operational caller mapping Needs confirmation | `GET /v1/system/degraded-modes` | Sync; success code Needs confirmation | AUTH-P; exact scope Needs confirmation | Source, pp. 68–70 |
| API-032 | Record controlled design decision | Engineering caller; no confirmed screen | `POST /v1/design-decisions` | Mutation; mode / success code Needs confirmation | AUTH-P; exact scope Needs confirmation | Source, pp. 8–10 |
| API-033 | Read design baseline | Engineering caller; no confirmed screen | `GET /v1/design-baselines/{id}` | Sync; success code Needs confirmation | AUTH-P; exact scope Needs confirmation | Source, pp. 9–10 |
| API-034 | Liveness interface | Operational probes; exact caller Needs confirmation | `GET /v1/health/live` | Sync; success code Needs confirmation | AUTH-P; probe scope Needs confirmation | Source, pp. 18–20 |
| API-035 | Readiness interface | Operational probes; exact caller Needs confirmation | `GET /v1/health/ready` | Sync; success code Needs confirmation | AUTH-P; probe scope Needs confirmation | Source, pp. 18–20 |

### Internal and External Integration Inventory

| ID | Purpose / caller | Method / path or protocol | Behavior | Authentication / authorization | Evidence |
|---|---|---|---|---|---|
| API-036 | Generate structured candidate; orchestration / model gateway boundary | `POST /internal/model/generate` | Provider generation; Sync-versus-Async response contract Needs confirmation | AUTH-I; approved deployment, region, data class and quota | Source, pp. 37–39 |
| API-037 | Read durable workflow; internal workflow callers | `GET /internal/workflows/{runId}` | Sync read | AUTH-I; workflow tenant scope; exact grants Needs confirmation | Source, pp. 48–50 |
| API-038 | Replay dead letter; operator | `POST /internal/deadletters/{id}/replay` | Controlled mutation; mode Needs confirmation | AUTH-I; operator reason, dry-run validation and scope limit | Source, pp. 48–50 |
| API-039 | Read stored document; internal storage callers | `GET /internal/storage/documents/{id}` | Sync read | AUTH-I; tenant predicate and document access; exact grants Needs confirmation | Source, pp. 51–53 |
| API-040 | Purge eligible stored data; retention / operational callers | `POST /internal/storage/purge` | Purge mutation; response mode Needs confirmation | AUTH-I; retention eligibility / legal holds; exact grants Needs confirmation | Source, pp. 51–53, 66 |
| API-041 | Read metrics; monitoring caller | `GET /internal/metrics` | Sync read | AUTH-I; exact grants Needs confirmation | Source, pp. 64–66 |
| API-042 | Read capacity; admission / operational callers | `GET /internal/capacity` | Sync read | AUTH-I; exact grants Needs confirmation | Source, pp. 68–70 |
| API-043 | Initiate release; deployment tooling | `POST /internal/releases` | Promotion workflow; response mode Needs confirmation | AUTH-I; allowed build identity, release gates / sign-off | Source, pp. 71–73 |
| API-044 | Read reconstructible release record; deployment tooling | `GET /internal/releases/{releaseId}` | Sync read | AUTH-I; exact grants Needs confirmation | Source, pp. 71–73 |
| API-045 | Typed grounded retrieval; Research Agent / approved MCP server | MCP `knowledge.search@v1`; HTTP method/path Needs confirmation | Read-only tool request/reply | AUTH-T; `read:permitted_documents`, tenant-scoped | Source, p. 87, §C.2 |
| API-046 | Agent handoff | A2A task envelope; method/path Needs confirmation | Task handoff; receiver may decline | AUTH-T; separate capability authorization | Source, pp. 41, 87 |
| API-047 | Notify external subscribers | Optional signed outbound webhooks; method/URL Needs confirmation | Async, retried notification | Signed delivery; recipient verifies signature and event age | Source, p. 55, §15.2.2 |
| API-048 | Source repository access; connector workers | Advertised `list`, `fetch`, delta cursor, ACL and delete capabilities; provider methods/URLs Needs confirmation | Provider calls with durable sync checkpointing | Workspace-scoped vault credentials and declared provider permissions | Source, pp. 27–29 |
| API-049 | Provider model invocation; model gateway | Provider method/URL/schema Needs confirmation | Scoped model generation | Declared egress, approved deployment/region and data-handling class; never connector secrets | Source, pp. 15, 18, 37–39 |

Internal paths must not be exposed as browser contracts without an explicit decision. General gRPC contracts require repository-controlled protobuf IDL; no service or RPC method names are supplied.  
**Evidence:** Source, pp. 16, 54–55, 82.

### Required Activities Without Defined Endpoints

| ID | Affected screen operation | Confirmed behavior | Contract gap |
|---|---|---|---|
| API-050 | SCR-007-E01 | Version-preconditioned, audited workspace settings update | Load/save method/path/schema Needs confirmation; case PATCH is not a valid inferred settings contract |
| API-051 | SCR-002-E03 | Correct classification labels with reason code | Method/path, label vocabulary and request schema Needs confirmation |
| API-052 | SCR-005-E04 | Override requires elevated role, secondary reviewer and audited reason | Method/path and elevated eligibility Needs confirmation |
| API-053 | SCR-002-E07 | Rework denial as new run revision, never retroactive approval | Whether API-008 covers rework and its payload Needs confirmation |
| API-054 | SCR-002-E08; SCR-003-E03 | Authorized original source access and anchored citation inspection | Public signed-source access/download endpoint and response schema Needs confirmation |
| API-055 | SCR-006-E03 | Revoke credentials; queued jobs fail safely | Credential-revocation / reauthorization methods and paths Needs confirmation |
| API-056 | SF-014 | Idempotent provisioning; incomplete provisioning blocks sync | Provisioning method/path/status retrieval Needs confirmation |
| API-057 | SCR-002-E06 | Explicit reopen as a new revision | Method/path, predecessor guards and authorization Needs confirmation |

**Evidence:** Source, pp. 12, 24–29, 45–46, 52, 78; [01_screen_functions.md](01_screen_functions.md), corresponding operations.

## Interfaces by API

### Shared Parameter and Schema Rules

**API-R-002 — Confirmed:** Public timestamps use RFC 3339 with UTC durable representations. Source baseline identities are UUIDv7. Database types are not automatically public JSON types. Domain field names and selected database columns do not establish REST property names.  
**Evidence:** Source, pp. 51, 54, 59, 85–86.

Unless specified below, parameter lengths, defaults, nullability, body requiredness, accepted content types, unknown-request-field policy and response property names/types **Need confirmation**. An undocumented GET body or undocumented query parameter is not authorized by this specification.

| Parameter / context name | Location / applicability | Meaning and type | Required status | Constraints / default | Evidence |
|---|---|---|---|---|---|
| `caseId` | Path, API-003–006, 008, 015 | Case identity; UUIDv7 baseline | Required by route | Must resolve in authorized tenant/workspace; no default | Source, pp. 51, 83 |
| `documentId` | Path, API-007 | Document identity; UUIDv7 baseline | Required by route | Current document permission; no default | Source, pp. 30–32, 51 |
| `runId` | Path, API-010–012, 037 | Run identity; UUIDv7 baseline | Required by route | Authorized associated case/workspace; no default | Source, pp. 40–42, 51, 83 |
| `evidenceId` | Path, API-014 | Evidence identity; UUIDv7 identity baseline, public representation Needs confirmation | Required by route | Opaque to users; current source permission; no default | Source, pp. 35, 51 |
| `approvalId` | Path, API-017 | Approval/task reference; UUIDv7 baseline | Required by route | Exact mapping to `approval_tasks.id` Needs confirmation; no default | Source, pp. 51, 83, 85 |
| `connectorId` | Path, API-018–019 | Connector identity; UUIDv7 baseline | Required by route | Tenant/workspace-scoped; no default | Source, pp. 27–29, 51 |
| `workspaceId` | Path, API-025–026, 028 | Workspace identity; UUIDv7 baseline | Required by route | Must belong to authenticated tenant; no default | Source, pp. 21–23, 51, 83 |
| `evaluationId`, `releaseId`, `id` | Respective inventory paths | Resource identity; UUIDv7 baseline; exact resource/version binding Needs confirmation | Required by route | No default; scope checked before disclosure | Source, pp. 9, 48–53, 51, 72–76 |
| `cursor` | Query, API-002 | Pagination continuation; opaque representation Needs confirmation | Continuation supported; first-page requiredness Needs confirmation | Length, expiry, initial behavior and default Needs confirmation | Source, pp. 54, 57 |
| `Idempotency-Key` | Header, API-001 and long-running POST creations | Operation replay key; wire representation/length Needs confirmation | Required for case create and long-running POST jobs | Same fingerprint returns original outcome; changed fingerprint conflicts; no specified generated default | Source, pp. 25, 54, 83, 89 |
| `If-Match` | Header, API-004 | Expected case revision; syntax Needs confirmation | Required | Monotonic revision check; quoting / ETag representation Needs confirmation; no default | Source, pp. 25, 83 |
| `Last-Event-ID` | Header, API-012 | Last received increasing event offset; wire type Needs confirmation | Used on resume; initial connection requirement Needs confirmation | Backfill only retained, currently scoped events; no default specified | Source, pp. 55, 83 |
| `Retry-After` | Response/provider header | Retry delay for throttling | Required for throttled AI-run clients | Value representation and delay calculation Needs confirmation | Source, pp. 28, 69 |
| `trace_id`, `correlation_id` | Request context; transport placement Needs confirmation | Independent trace/correlation identities; strings in examples | Every request carries both | Cross every boundary; independent of provider trace IDs; generation/validation rules Needs confirmation | Source, pp. 16, 64, 84 |
| `tenant_id`, `revision`, `actor_id`, `occurred_at` and correlation ID | Durable boundary record context | Tenant/actor identities, revision and occurrence timestamp | Required whenever operation changes durable state | Do not trust browser values as authority; exact request-versus-server-populated contract Needs confirmation | Source, chapter interface-boundary clauses, pp. 8–80 |

API-021 is confirmed cursor-paginated, but its query parameter name is not explicitly provided. Using `cursor` there is a **Proposal**, not a confirmed named parameter.

### API-001–005 — Case Interfaces

| API | Request definition | Successful response definition | Open contract decision |
|---|---|---|---|
| API-001 | `Idempotency-Key`; case business context. No complete named body schema supplied. | `201`; case identifier returned; case starts `NEW`. Identifier property name Needs confirmation. | Required title/description/impact/urgency/workspace fields, owner assignment and sensitivity input behavior |
| API-002 | `cursor` continuation; authentication/workspace context | Authorized cursor-paginated cases | Status code, list wrapper, continuation field, page size, filtering, ordering and snapshot consistency |
| API-003 | Required `caseId` | `200`; authorized current case revision | Exact public projection, omission/redaction and revision response header |
| API-004 | Required `caseId`, `If-Match`; mutation body schema Needs confirmation | `200`; accepted mutation; updated public projection Needs confirmation | JSON Patch versus merge/object format, allowed fields, null semantics, missing-precondition error |
| API-005 | Required `caseId`; case revision conditions apply to case mutations, but exact closure header/body contract Needs confirmation | Closure snapshots approved answer, cited versions and reviewer decisions | HTTP success code, source-state guard, replay outcome and snapshot reference |

**Source-supported case data, not a confirmed REST schema:**

| Business field / exact known storage identifier | Type / requiredness evidence | Constraints and defaults | REST mapping |
|---|---|---|---|
| `id`, `tenant_id`, `workspace_id` | Storage `UUID`; mandatory | Tenant/workspace integrity; server authority | Needs confirmation |
| Title, description | Domain text; lengths/requiredness unspecified | Title and description stored | Property names Needs confirmation |
| Impact, urgency, priority | Types/vocabularies unspecified | Priority derives from explicit impact and urgency, not model output alone | Needs confirmation |
| `sensitivity` | Storage `TEXT NOT NULL` | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`; storage default `INTERNAL` | Request default behavior Needs confirmation |
| `status` | Storage `TEXT NOT NULL` | `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED`; initial case `NEW` | Public state meaning Confirmed; property mapping Needs confirmation |
| Owner | Domain reference; type/requiredness unspecified | Mutation scope is Owner | Assignment/transfer contract Needs confirmation |
| Current approved result | Domain artifact reference | Separate from draft; publication-controlled | Needs confirmation |
| `revision` | Storage `BIGINT NOT NULL DEFAULT 1` | Monotonic; concurrency precondition | JSON number/string and range behavior Needs confirmation |
| `created_at`, `updated_at` | Storage `TIMESTAMPTZ NOT NULL`, default `now()` | UTC durable time | Public exposure Needs confirmation |
| Classification labels, confidences, provenance | Asynchronous domain output; types unspecified | Corrections require reason code | API-051 unresolved |
| Deadline | Domain timestamp | Workspace business calendar; prediction cannot alter contractual deadline | Public property and precision Needs confirmation |

**Evidence:** Source, pp. 12, 24–26, 62, 82–86; screen fields SCR-002-F01–F17.

### API-006–007 — Attachment and Document Status Interfaces

| Direction | Name / business item | Type / requiredness | Constraints / default |
|---|---|---|---|
| API-006 path/header | `caseId`, `Idempotency-Key` | Required | Authorized case; idempotent long-running creation |
| API-006 body | File content; part/property name Needs confirmation | File required to attach; transfer encoding unspecified | PDF, DOCX, HTML, UTF-8 text; MIME signature and extension agree; configurable 25 MB per-file cap |
| API-006 body/context | Attachment sensitivity, OCR option and metadata | Schema and requiredness Needs confirmation | OCR is opt-in and provenance-marked; no inferred REST fields |
| API-006 response | Persisted ingestion operation identity | `202`; property/type Needs confirmation | Acceptance is not readiness or successful indexing |
| API-007 response | Processing status | Literal vocabulary Confirmed; property/requiredness Needs confirmation | `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED` |
| API-007 response | Safe reason, correlation ID and remediation path | Conditional quarantine information; exact names/types Needs confirmation | Must not expose unsafe payloads or secrets |
| API-007 response | Extraction quality / provenance | Public exposure and schema Needs confirmation | Empty-page ratio, unknown-character ratio, table-loss indicators, language confidence |

Upload count, aggregate size, byte interpretation of MB, decompression threshold, multipart versus direct upload, scan timing and status polling interval **Need confirmation**.  
**Evidence:** Source, pp. 29–32, 82–83; SCR-002-E04, SCR-002-F14–F16.

### API-008–012 — Run and Streaming Interfaces

| API | Input | Success and source-supported output | Needs confirmation |
|---|---|---|---|
| API-008 | `caseId`, required `Idempotency-Key`; body unspecified | `202`; run created immediately; durable bounded workflow | Run identifier property, requested action/input schema, case-revision binding |
| API-009 | Required long-running creation key; body unspecified | Run request supported by Chapter 3 | Relationship to API-008, case reference input, success status and role |
| API-010 | `runId` | `200`; stages and evidence metadata | Wrapper and field types/requiredness |
| API-011 | `runId` | Stored steps/checkpoints available | Success status, order, pagination, checkpoint detail/redaction |
| API-012 | `runId`; `Last-Event-ID` on resume | `200`; SSE increasing offsets, scoped retained-event backfill | Event names/payload projection, retention duration, stale offsets, heartbeat, connection expiry, terminal close behavior |

Confirmed run states are `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED`. Step records include `step_kind`, `status`, `checkpoint`; run records include `plan_revision` and `budget` in the relational catalog, but public mapping/types **Need confirmation**. Failure output must identify the failed checkpoint safely.

The browser must not send arbitrary tool definitions. No cancel, retry or resume-mutation endpoint is confirmed. Refresh and stream resume must not restart business processing.  
**Evidence:** Source, pp. 7, 40–42, 49, 55, 58, 82–85; SCR-004-E01–E05.

### API-013–015 — Search and Evidence Interfaces

| Interface item | Source-supported definition | Type / requiredness / default |
|---|---|---|
| API-013 request | Business retrieval query | Public property names/types/requiredness Needs confirmation; MCP input is not automatically REST input |
| API-013 response | ACL-filtered lexical + semantic evidence, `200` | Collection wrapper, score fields and pagination Needs confirmation |
| Evidence item | Chunk ID, source title, document revision, page anchor and ACL digest included | Required semantic content; exact property names/types/lengths Needs confirmation |
| Stored anchor | Source URI, file hash, page number, optional bounding box | Bounding box optional; public URI/hash exposure and page numbering basis Needs confirmation |
| API-014 request | `evidenceId` | Required; current source authorization |
| API-015 request | `caseId` | Required; permitted case and source authorization |
| API-014–015 response | Authorized evidence/provenance for exact stored sources | Status codes, source-content transport, set selection and wrappers Needs confirmation |
| Degradation information | Visible reduced-quality flag when lexical-only fallback is used | Flag property/type Needs confirmation |

Opaque citation identifiers must be verified before display. API-014 does not automatically authorize source URL access through API-054.

Configuration examples `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `hybrid_rrf_k: 60` are source configuration examples, not REST page-size parameters or settled public limits.  
**Evidence:** Source, pp. 31, 35–36, 52–53, 57, 69, 90.

### API-016–017 — Review Interfaces

| Direction | Business item | Type / requiredness | Constraints |
|---|---|---|---|
| API-016 response | Review identity, task status, assignment/pool | Public schema Needs confirmation | Review states: `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED` |
| API-016 response or related detail contract | Exact candidate, citations, model/prompt version, policy reasons | Required reviewer inspection capability; endpoint allocation Needs confirmation | Must describe exact artifact under review |
| API-017 path | `approvalId` | Required | Authorized current assignment and eligible Reviewer |
| API-017 body | Decision | Required semantic action; property and literal enum Needs confirmation | Approval or rejection; review state enum is not automatically request enum |
| API-017 binding | Evaluated artifact hash | Exact binding required; body/header property and digest encoding Needs confirmation | Changed/wrong artifact rejected as stale |
| API-017 body / record | Rationale | Stored; input mandatory rule, type/length Needs confirmation | Safe validated reviewer content |
| API-017 body | Annotations | Optional semantic content; type/property Needs confirmation | Cannot alter historical approval authority |
| API-017 server record | Actor and timestamp | Captured server context; property names Needs confirmation | Authenticated actor; UTC timestamp |
| API-017 response | Accepted binding decision | `200`; response projection Needs confirmation | Does not by itself establish that publication has completed |
| Conflict response | Stale artifact decision | `409` supported; exact code/details Needs confirmation | Audit rejection; no publication under old hash |

Rule outcomes are `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY`. Normalized policy inputs comprise sensitivity, requested action, evidence quality, model class, financial impact category and confidence bands, stored with rule-set version. No public policy-evaluation request schema is supplied.  
**Evidence:** Source, pp. 44–46, 58, 82–85.

### API-018–024 — Connector, Catalog, Audit, Usage and Evaluation Interfaces

| API | Named inputs / body | Output content and success | Remaining schema decisions |
|---|---|---|---|
| API-018 | `connectorId`, required long-running `Idempotency-Key`; body unspecified | `202`, incremental sync operation | Operation ID field, requested scope, concurrent-sync handling |
| API-019 | `connectorId`; list query unspecified | Sync runs, durable cursor/high-watermark/error ledger domain data | Public cursor exposure, timestamps, status enum, safe remediation projection, pagination |
| API-020 | No specific query/body documented | Registered model deployments by capability, region, data-handling class, context length, cost profile and evaluation approval | Public fields, authorization, allowed-versus-complete catalog selection |
| API-021 | Cursor pagination; parameter name unresolved | `200`, immutable redacted audit list; domain fields include `id`, `tenant_id`, `actor_id`, `action`, `digest` | Public projection/types, filter inputs, hash-chain detail, continuation field |
| API-022 | Query/body unspecified | `200`, costs, quotas, trends; daily budget/forecast/rejected excess requests; cost-center/deployment attribution | Currency, units, windows, precision, completeness/freshness indicators |
| API-023 | Required long-running `Idempotency-Key`; benchmark-selection body unspecified | `202`, frozen benchmark operation | Dataset/model/prompt/policy version inputs, operation identity |
| API-024 | `evaluationId` | Evaluation/scorecard: citation precision, unsupported-claim rate, high-risk recall, confidence intervals and distribution shift by domain | Status vocabulary, public field names/types, partial result handling |

These rows do not authorize exposing secret references' resolved values, raw credentials, full internal prompts or unrestricted audit content.  
**Evidence:** Source, pp. 27–29, 37, 62–66, 74–76, 83, 85.

### API-025–029 — Export, Delete, Identity, Membership and Holds

| API | Request definition | Success/output content | Needs confirmation |
|---|---|---|---|
| API-025 | `workspaceId`, required long-running `Idempotency-Key`; two independent approval checks | `202`; export packages case metadata, approved artifacts, source references and audit manifests with checksums; excludes secrets/internal model prompts | Approval-reference fields, manifest schema, snapshot consistency, status/download endpoint and URL expiry |
| API-026 | `workspaceId`, required long-running `Idempotency-Key`; two independent approval checks | `202`; legal holds enforced, tombstones written, blobs/index entries removed, completion receipts recorded | Approval-capture schema, status retrieval, partial-retention outcome and completion definitions |
| API-027 | Authenticated principal context; no named query/body documented | Principal/membership/access context interface | Status and entire public identity projection |
| API-028 | `workspaceId`; membership body unspecified | Durable membership change with tenant/revision/actor/time/correlation context | Full replacement versus scoped update semantics, role vocabulary, revision header, response status and changed-ACL invalidation contract |
| API-029 | Hold body unspecified | Durable hold control supported | Hold scope/reference/reason, permissions, response status, release endpoint and idempotency classification |

**Evidence:** Source, pp. 21–23, 61–63, 78–80, 83.

### API-030–044 — Contract and Operational Interfaces

All entries inherit shared path/context validation. Exact HTTP success codes, response fields/types/requiredness, query options and body requiredness are **Needs confirmation** unless the table states otherwise.

| API | Confirmed interface content / inputs | Processing responsibility | Specific unresolved decisions |
|---|---|---|---|
| API-030 | OpenAPI contract document | Serve REST source-of-truth contract generated from controlled IDL | OpenAPI version, publication metadata, auth and compatibility-error representation |
| API-031 | Degraded-mode state | Report modes without authorization/approval bypass | Mode enum, affected scope, freshness and response schema |
| API-032 | ChangeRequest / RequirementLink / DecisionRecord context; impact scores for behavior, migration, threat surface and cost | Validate controlled changes, record approved baseline revision lineage | Input names/types, approval mechanism, success status and operation model |
| API-033 | Required `id` | Read controlled baseline/revision | Baseline-versus-revision identity and public projection |
| API-034–035 | Liveness/readiness interface paths | Operational health boundary | Probe credentials, checks, dependency policy, statuses and disclosure-safe payload |
| API-036 | Validated user input, signed workflow instruction, separately delimited evidence, versioned output schema, model budget/context | Scoped generation and output validation | Complete request/output IDL, signing fields, timeout and provider retry budget |
| API-037 | Required `runId` | Read authoritative workflow/checkpoints | Public/internal projection separation and response schema |
| API-038 | Required `id`; operator reason, dry-run validation, scope limit | Controlled replay; preserve original event ID unless explicit migration provenance | Parameter names/types, dry-run evidence binding, limit units and response mode |
| API-039 | Required `id` | Authorized immutable source/artifact access | Version/role selector, bytes-versus-signed-URL response and expiry |
| API-040 | Eligible purge inventory; exact named body unspecified | Tombstone/purge with legal-hold exceptions and receipts | Scope selectors, approval propagation, operation status and partial failure schema |
| API-041 | Metrics interface | Safe monitoring of golden / AI-specific signals | Metric names, exposition format, label cardinality and tenant access |
| API-042 | Capacity interface | Workspace tokens, queue age and provider capacity admission | Numeric thresholds, freshness and permit representation |
| API-043 | Release artifact / signed config / migration and rollout-gate data | Verify image digest/build identity, compatibility, quality, Security/SRE checks; bind reconstructible versions | Complete request IDL, gate proofs, success status and idempotency key transport |
| API-044 | Required `releaseId` | Read image/schema/prompt/model-routing-policy lineage | Release-state enum and schema |

**Evidence:** Source, pp. 8–10, 18–20, 37–39, 48–56, 64–73.

The repeated source wording about validating GET requests “before allocating a long-running operation” does not sufficiently establish that ordinary reads create jobs. A read-failure-to-async conversion contract **Needs confirmation**; implementations must not fabricate a successful read or an undocumented job response.

### API-045–049 — Integration Protocol Definitions

#### API-045 — `knowledge.search@v1`

| Direction | Exact field | Type | Required status / default | Constraints |
|---|---|---|---|---|
| Input | `query` | `string` | Requiredness/default Needs confirmation | Length and normalization rules Needs confirmation |
| Input | `case_id` | `uuid` | Requiredness/default Needs confirmation | Tenant-scoped permitted case |
| Input | `max_items` | `int` | Requiredness/default Needs confirmation | `<=10`; lower bound Needs confirmation |
| Output | `evidence_set_id` | `uuid` | Output field Confirmed | Evidence set identity |
| Output | `citations` | `Citation[]` | Output field Confirmed | Citation schema representation Needs confirmation; source anchors/current permission required |

Effect is read-only: no arbitrary URLs or filesystem access. Authorization is `read:permitted_documents`, tenant-scoped.  
**Evidence:** Source, p. 87, §C.2.

#### API-046 — A2A Task Envelope

| Exact field / business element | Type evidence | Requiredness / constraints |
|---|---|---|
| `task_id` | UUID string in source example | Task identity required semantically; exact schema requiredness Needs confirmation |
| `tenant_id` | String placeholder in example | Immutable tenant context; placeholder `tenant_example_01` is not a production UUID format |
| `capability` | String | Versioned reference; source example `research.grounded_search.v1`; discovery does not authorize |
| `input_schema` | Schema URI string | Source example `schema://oriondesk/research-request/1` |
| Declared output schema | Business contract in §11.2.2 | Exact property absent; Needs confirmation |
| `deadline_at` | RFC 3339 timestamp string | Deadline required semantically; enforcement and expiry reply Needs confirmation |
| `trace_id` | String | Propagated trace context |
| `authorization_ref` | String | Source example `grant_readonly_14`; grant verification contract Needs confirmation |
| `payload` | Object in example | Schema-bound task input; example includes `case_id` and `query` |

Receiver may decline. Decline/error vocabulary and transport statuses **Need confirmation**.  
**Evidence:** Source, pp. 41, 87.

#### API-047–049 — Provider Contracts

| API | Confirmed behavior | Missing interface definitions |
|---|---|---|
| API-047 | Optional outbound signed webhook; recipient checks signature/event age; exponential retries; internal transition is not rolled back by failure | Method, destination-registration API, signature header/algorithm, event projection, event-age bound, retry limit, recipient success statuses |
| API-048 | Capabilities `list`, `fetch`, delta cursor, ACL and delete; scoped secret references; `Retry-After` respected | Supported providers, URLs/methods, permission scopes, capability schema, provider response mapping, token refresh/revoke contract |
| API-049 | Only scoped prompt/context; approved region/deployment/data class; equal-or-stronger approved fallback only | Provider URLs/methods, request/output schema, model deployment IDs, timeouts, error translation and usage reconciliation |

**Evidence:** Source, pp. 15, 18, 27–29, 37–39, 55, 90.

### Event Boundary Contracts

**API-R-003 — Confirmed:** Internal events use canonical JSON and UTC and contain the following exact envelope fields. This envelope is not automatically the public SSE or webhook payload.

| Field | Meaning / type evidence | Required status |
|---|---|---|
| `event_id` | Event identity; UUIDv7 baseline | Required |
| `type` | Event type; serialization type Needs confirmation | Required |
| `schema_version` | Version identifier; type Needs confirmation | Required |
| `tenant_id` | Immutable tenant identity | Required |
| `aggregate_id` | Aggregate identity | Required |
| `aggregate_revision` | Aggregate revision; JSON representation Needs confirmation | Required |
| `occurred_at` | UTC occurrence timestamp | Required |
| `trace_id` | Trace identity | Required |
| `payload` | Versioned event-specific data | Required |

| Event | Producer / consumer behavior | Related API |
|---|---|---|
| `CaseCreated` | Case Service; classifier consumes case ID/revision | API-001 |
| `DocumentNormalized` | Ingestion; build index using version ID/source hash | API-006–007 |
| `SearchIndexCommitted` | Indexer; invalidate cache using index generation/document revision | API-013–015 integration |
| `AgentPlanApproved` | Orchestrator; dispatch run plan by run ID/plan hash | API-008–011 |
| `ApprovalDecisionRecorded` | Policy Service; validate publication using task/actor/content hash | API-017 |
| `WorkflowStageAdvanced` | Orchestrator; resume consumers by run/stage/checkpoint | API-010–012, 037–038 |
| `AccessDenied` | Policy Service; alert enrichment using principal/action/policy digest | Authorization boundary |
| `TenantDeletionVerified` | Retention Worker; close purge record by manifest ID/receipt hash | API-026, 040 |

Additional chapter-register events are confirmed names: `BaselineCommitted`, `RunRequested`, `DeploymentPromoted`, `CaseStateChanged`, `ConnectorSyncStarted`, `ModelInvocationCompleted`, `DataRetentionPurgeCommitted`, `ApiCompatibilityVerified`, `UserReviewOpened`, `SecurityPolicyChanged`, `SloBurnRateDetected`, `BackpressureActivated`, `ReleasePromoted`, `EvaluationCompleted`. Their complete payload schemas and exact endpoint emission conditions **Need confirmation**; a GET does not inherently emit its chapter's mutation event.

**Evidence:** Source, pp. 10–80, chapter contract registers; pp. 48, 87.

### Request and Response Examples

#### Source-confirmed Error Example

Preserved exactly from Source, p. 84, §A.3. Revisions and correlation ID are illustrative values, not defaults.

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

#### Proposal — Case Creation Exchange

The following illustrates a possible wire schema only. Property names, required fields, token transport and response representation require approval before client/server implementation.

```http
POST /v1/cases
Authorization: Bearer <access-token>
Idempotency-Key: <opaque-operation-key>
Content-Type: application/json
```

```json
{
  "workspace_id": "019ac000-0000-7000-8000-000000000041",
  "title": "Synthetic contract inquiry",
  "description": "Review the permitted contract evidence.",
  "sensitivity": "INTERNAL"
}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json
```

```json
{
  "id": "019ac000-0000-7000-8000-000000000042",
  "status": "NEW",
  "revision": 1
}
```

#### Proposal — Run Progress Frame

The SSE mechanism and increasing offsets are confirmed; field names, event name and content type below are an illustrative projection, not a settled payload contract.

```text
id: 12
event: run_progress
data: {"run_id":"019ac000-0000-7000-8000-000000000042","status":"RETRIEVING"}
```

Full executable request/response examples for the other APIs depend on the unresolved schemas recorded above. They must be generated from approved IDL rather than inferred from domain tables.

## Processing and Consistency

### Shared Request Procedure

**API-R-004 — Confirmed:**

1. Authenticate and establish tenant, actor, trace and correlation context.
2. Validate path/query/header/body against the versioned contract before transaction entry or long-running allocation.
3. Reject broad policy violations at the edge.
4. Resolve resources with tenant-scoped predicates; do not disclose foreign-tenant resource existence.
5. For mutations, reevaluate domain authorization, state invariants and revision conditions within the transaction.
6. Resolve applicable idempotency identity/fingerprint without allowing duplicate side effects.
7. Persist accepted business state, revision/context and transactional outbox records atomically where specified.
8. Dispatch downstream work only through a committed outbox or explicitly reconciled saga step.
9. Return the confirmed success result or a safe documented error/persisted operation identity; never ambiguous success.
10. Validate tool arguments and separate capability authorization again before dispatch.

Exact ordering of revision checking versus idempotency lookup under concurrent requests **Needs confirmation**, while the no-duplicate/no-unauthorized-write invariants remain mandatory.  
**Evidence:** Source, pp. 16–17, 21–26, 48–56.

### Transaction and Replay Requirements

| ID | Confirmed requirement | Affected APIs | Evidence |
|---|---|---|---|
| API-R-005 | Case mutations, approval decisions and outbox inserts commit in one ACID transaction. Search indexing and external webhooks are asynchronous and reconciled. | API-001, 004–006, 017 and downstream processing | Source, p. 52, §14.2.1 |
| API-R-006 | Final response pointer and satisfied publication gate are recorded in the same transaction. Recompute evidence authorization at publication; an old approval never authorizes a different artifact. | API-017 / publication workflow | Source, pp. 45–46 |
| API-R-007 | Long-running POST creation requires `Idempotency-Key`. Identical replay returns original operation; changed fingerprint with same key returns `IDEMPOTENCY_CONFLICT`. Case idempotency binds actor/request fingerprint to one outcome for 24 hours. | API-001, 006, 008–009, 018, 023, 025–026; other job-creating POSTs once classified | Source, pp. 25, 54, 83, 89 |
| API-R-008 | Every cross-service write is retry-idempotent. At-least-once consumers deduplicate event IDs/operation keys and reject stale aggregate revisions; queue ordering across partitions is not an invariant. | All internal writes/events | Source, pp. 15–17, 48–50 |
| API-R-009 | Stale/unauthorized writes leave business state unchanged. Rejected attempts may retain safe audit evidence but must not publish an accepted-transition event. | All mutations | Source, chapter design checkpoints, pp. 9–80 |
| API-R-010 | Every tenant-owned access uses tenant context/RLS. Reset connection-pool scoped session variables after every transaction; enforce workspace-tenancy membership. | All storage-backed APIs | Source, pp. 22, 51, 86 |
| API-R-011 | Soft-deleted entities cannot be retrieved. Blob references are opaque, encrypted and accessed through short-lived authorization-controlled signed URLs. | API-003, 007, 014–015, 039, 054 | Source, pp. 51–53 |
| API-R-012 | Cache keys include tenant, user-scope digest, source ACL revision, query hash and index generation. Authorization changes invalidate affected entries before ordinary TTL expiry and before next retrieval. | API-013–015, 018–019 integrations | Source, pp. 28, 53 |

General idempotency-key namespace, fingerprint canonicalization, in-flight duplicate behavior, failed-outcome retention and post-24-hour behavior **Need confirmation**. The case-specific 24-hour rule must not silently become a universal retention rule.

### Business Processing by API Family

#### Cases — API-001–005

1. Create one tenant/workspace-bound case in `NEW`.
2. Persist immutable attachment/run references separately from the case aggregate.
3. Classify asynchronously with labels, confidence and provenance; corrections require a reason code.
4. Enforce transitions: `NEW → TRIAGED → IN_PROGRESS`; from `IN_PROGRESS` to `PENDING_APPROVAL` or `RESOLVED`; from `PENDING_APPROVAL` to `RESOLVED` or `IN_PROGRESS`.
5. Derive priority from explicit impact/urgency; compute deadlines using workspace timezone/business calendars.
6. On eligible closure, snapshot approved answer, cited document versions and reviewer decisions immutably.
7. Permit reopening only explicitly as a new revision; predecessor-to-`CLOSED` guard is unresolved.

**Evidence:** Source, pp. 12, 24–26, 82–86.

#### Ingestion — API-006–007

1. Check permitted type, MIME/extension agreement, configured per-file cap and decompression threshold.
2. Scan before parsing; disable macros; never fetch embedded remote references.
3. Quarantine unsafe files without indexing.
4. Parse layout, tables, headings and reading order; preserve page/bounding-box anchors.
5. Opt-in OCR must retain provenance; normalization strips transport artifacts without rewriting claims.
6. Derive immutable identities from content fingerprint/pipeline version; allow side-by-side reprocessing.
7. Exclude low-quality documents from autonomous recommendations while retaining authorized viewing.

**Evidence:** Source, pp. 30–32.

#### Retrieval — API-013–015, 045

1. Resolve current tenant/workspace/document ACL scope.
2. Form lexical and normalized vector queries; retrieve bounded candidates.
3. Merge by reciprocal rank fusion, deterministic reranking and evidence diversity.
4. Apply token-return budgets and current ACL controls before model text release.
5. Return only verifiable anchored evidence.
6. Return `NO_SUPPORTED_EVIDENCE` for insufficient quality/confidence, never fabricated context.
7. If permitted lexical fallback continues after vector degradation, expose reduced-quality status without bypassing authorization or approval.

**Evidence:** Source, pp. 34–36, 69, 87.

#### Runs / Model Gateway — API-008–012, 036, 045–046, 049

1. Admit only when workspace tokens, queue age and provider capacity satisfy thresholds.
2. Reserve input/output token budget and track workspace quota/provider usage.
3. Persist DAG plan revision before side effects; bound depth to eight and tool invocations to sixteen.
4. Persist each stage checkpoint before downstream dispatch.
5. Route only to approved deployments/regions; fallback only to an approved equal-or-stronger data-handling class.
6. Treat retrieved passages as untrusted data, separate from fixed rules and signed workflow instructions; remove evidence-context tool directives and record injection indicators.
7. Validate versioned structured output with bounded retries. Unknown fields, invalid citations and control-character injection produce `MODEL_OUTPUT_INVALID`.
8. Evaluate deterministic policy; the model cannot override outcomes or authorize tools.
9. Stop on missing approval, exhausted call budget, repeated invalid plans, policy denial or deadline expiry; identify failed checkpoint.
10. Quota exhaustion is terminal for the current run without automatic model/data-class switching.
11. Do not replace a denied action with a semantically equivalent tool.

Configured maximum / recoverable timeout representation **Needs confirmation**. Appendix F's `run_timeout_seconds: 180` is configuration-example evidence; its scope across human waiting is unresolved.  
**Evidence:** Source, pp. 37–42, 49, 69, 90.

#### Reviews / Publication — API-016–017

1. Normalize/store policy inputs with rule-set version.
2. Assign eligible pool/minimum role and enforce segregation of duties.
3. Make exact candidate, sources, model/prompt version and policy reasons inspectable.
4. Validate complete required review inputs server-side; exact required set Needs confirmation.
5. Bind immutable decision to authenticated actor, UTC timestamp and exact artifact hash.
6. Reject stale decisions and audit them.
7. At publication, reevaluate current evidence authorization and satisfied policy/approval requirements atomically.
8. Expire tasks after configured SLA and reassign/escalate; never silently approve.
9. Overrides require elevated role, secondary reviewer and audited reason.
10. Rework denied drafts as new run revisions.

The source does not settle whether publication is automatic following API-017 or separately triggered.  
**Evidence:** Source, pp. 44–46, 58.

#### Connector Sync — API-018–019, 048

1. Block sync while provisioning is incomplete.
2. Discover capability support; missing support yields lower-trust mode and visible warning.
3. Resolve vault-backed workspace credentials; revoked credentials fail queued work with `CONNECTOR_REAUTH_REQUIRED`.
4. Persist provider cursor, high-watermark and error ledger.
5. Advance cursor only after all preceding items have durable outcomes.
6. Honor provider `Retry-After`, bounded exponential backoff/jitter, workspace quotas and fair scheduling.
7. Quarantine poison records after bounded retries; remaining batch may continue with recorded exception.
8. Tombstone deleted sources and schedule index removal; invalidate ACL caches before the next retrieval.

**Evidence:** Source, pp. 27–29, 78.

#### Governance / Operations

- **API-021:** Append-only audit with batch-hash chaining and independently controlled retention; historical decisions cannot be edited.
- **API-023–024:** Frozen, versioned evaluation corpus with expected citations/outcomes; report domain confidence intervals/distribution shift. Targets: citation precision `>=0.97`, unsupported-claim rate `<=0.02`, high-risk recall `1.00`; low statistical confidence blocks release.
- **API-025–026, 040:** Two-person export/delete controls; legal-hold protection; inventory-based deletion with tombstones, blob/index removal and receipts. Held records remain retained and receipted.
- **API-038:** Operator reason, validated dry run and scope limit; retain original event identity unless schema migration has explicit provenance.
- **API-043–044:** Bind image digest, schemas, prompts and model routing policy; verify build identity, compatibility and safety gates. Canary regression rolls traffic back, not database schema down.

**Evidence:** Source, pp. 50, 62, 72–76, 78–80, 88–89.

### Timeouts, Retries and Performance

| ID | Confirmed requirement | Needs confirmation | Evidence |
|---|---|---|---|
| API-R-013 | Transient dependency failures use bounded exponential backoff, jitter and per-dependency circuit breakers. Validation/permission failures are permanent and not retried. | Attempt caps, delay values, dependency timeout/circuit thresholds and caller retry policy | Source, pp. 28, 49 |
| API-R-014 | Read operations may retry transient faults; mutable/consequential tool actions need idempotency and human authorization. | Operation-specific safe replay classification | Source, p. 42 |
| API-R-015 | Throttled AI-run clients receive `429` plus `Retry-After`; existing saved cases remain accessible. Generation outage keeps evidence/manual editing available. | Admission threshold values and outage error status/code | Source, pp. 69, 79 |
| API-R-016 | Reference public API availability target is 99.9% monthly. Case-create P95 is described as within/under 300 ms; search P95 under 1.5 s excluding remote connector fetch. | Strict case-create boundary, measurement window, workload mix and acceptance instrumentation | Source, pp. 12, 65, 68 |
| API-R-017 | Reference envelope: 2,000 daily active users, 60 requests/s steady, 180 requests/s burst, up to 100,000 indexed documents/tenant and 20 concurrent AI runs/large tenant. | Whether concurrency is a quota or capacity assumption; do not infer universal request caps | Source, p. 68 |

No HTTP connection/request timeout, sync schedule, SSE retention interval or webhook event-age limit is confirmed.

## Errors and Acceptance Criteria

### Canonical Error Body

**API-R-018 — Confirmed:** Use safe stable errors with the source envelope. Requiredness beyond the illustrated canonical fields must be finalized in IDL.

| Exact field | Type evidence | Requiredness / constraints |
|---|---|---|
| `error` | Object | Canonical envelope root |
| `error.code` | String | Stable machine-readable code; preserve exact confirmed literals |
| `error.message` | String | Safe message; no sensitive content |
| `error.correlation_id` | String | Safe support correlation |
| `error.retryable` | Boolean | Explicit retry guidance |
| `error.details` | Object | Optional safe structured validation/conflict details |
| `error.details.expected_revision` | Integer in case-conflict example | Safe expected revision; broader schema Needs confirmation |
| `error.details.actual_revision` | Integer in case-conflict example | Safe current revision; broader schema Needs confirmation |

Never include connector credentials, full prompts, retrieved documents or unauthorized resource existence. Diagnostic traces likewise exclude user documents/API secrets.  
**Evidence:** Source, pp. 54, 64, 84.

### Failure Mapping and Caller Actions

Caller actions below are **Proposals** except mandated nonretry and `Retry-After` behavior.

| Condition | Affected APIs | Confirmed HTTP / business code | Retry classification / caller action | Evidence / unresolved details |
|---|---|---|---|---|
| Stale case revision | API-004; other case mutation mapping unresolved | `409 CASE_VERSION_CONFLICT` | `retryable: false` in source example; Proposal: refetch current case and reconcile, never blind overwrite | Source, pp. 25, 83–84 |
| Changed body with reused creation key | API-001; general long-running creations | `409 IDEMPOTENCY_CONFLICT` confirmed for case test | Proposal: correct key/body pairing; do not replay changed intent under old key | Source, pp. 54, 89 |
| Foreign-tenant resource / absent resource | Resource reads/mutations | Same not-found class; `404`-equivalent for case; literal code Needs confirmation | Permanent denial; do not disclose existence | Source, pp. 23, 89 |
| Invalid request schema | Contracted requests | `422`; business code Needs confirmation | Permanent, not retried; Proposal: correct validated fields | Source, pp. 54, 56 |
| Quota / admission failure | API-008–009 / gateway | `429` and `Retry-After`; business code Needs confirmation | Wait according to header; saved-case access preserved | Source, pp. 54, 69 |
| Wrong/changed reviewed artifact | API-017 | `409`; stale business code Needs confirmation | Do not publish; Proposal: reload exact current task/artifact | Source, pp. 45, 83, 89 |
| Invalid model structure/citation/control characters | API-036 and run outcome | `MODEL_OUTPUT_INVALID`; HTTP mapping Needs confirmation | Gateway bounded parsing retries; no publication; final retryability Needs confirmation | Source, pp. 38, 89 |
| Insufficient supported evidence | API-013–015 / run retrieval | `NO_SUPPORTED_EVIDENCE`; HTTP mapping Needs confirmation | No fabricated context; clarification/human route allowed, choice unresolved | Source, p. 36 |
| Connector credentials revoked | API-018 processing / API-019 outcome | `CONNECTOR_REAUTH_REQUIRED`; HTTP mapping Needs confirmation | Reauthorization required; no secret disclosure | Source, p. 27 |
| Unsafe/oversized/type-mismatched/decompression-bomb upload | API-006–007 | Quarantine/fail-closed behavior; statuses/codes Needs confirmation | Never index unsafe content; remediation contract unresolved | Source, pp. 13, 30, 89 |
| Self-approval / missing capability / unauthorized action | API-017, 036, 045–046 | Denial; `DENY` before arbitrary tool dispatch is test outcome, not confirmed HTTP error code | Permanent permission failure; no equivalent-tool substitution | Source, pp. 11, 41–46, 89 |
| Expired review | API-016–017 / workflow | No implicit approval; error code/status Needs confirmation | Reassign/escalate, record outcome | Source, pp. 45, 89 |
| Dependency unavailable | All applicable boundaries | Documented retryable error or persisted async job identity; specific status/code Needs confirmation | Bounded transient recovery; never ambiguous success | Source, interface-boundary clauses pp. 8–80 |
| Deadline/call budget/invalid plan/policy stop | Run interfaces | Exact failed checkpoint reported; code/status Needs confirmation | No publication bypass; timeout recovery contract unresolved | Source, pp. 12, 41 |
| Legal hold during deletion | API-026, 040 | Protected records retained and receipted; operation status/code Needs confirmation | Never force purge held records | Source, pp. 80, 89 |
| Missing second independent export/delete check | API-025–026 | Denied; HTTP/code Needs confirmation | Obtain legitimate independent authorization; single Admin insufficient | Source, pp. 78, 83, 88 |
| Invalid/expired cursor or stream offset | API-002, 012, 021 and paginated lists | Needs confirmation | Proposal: recover from authorized server state without recreating operations | Source, pp. 54–55, 58 |
| Authentication failure | All APIs | Rejection confirmed; HTTP/code Needs confirmation | No protected processing; session recovery contract unresolved | Source, pp. 21–23 |

### Acceptance Criteria

All fixtures must be synthetic and cover successful, empty, mixed-permission, adversarial and malformed inputs. Randomized tests record seeds. Critical isolation/approval tests pass with zero exceptions.  
**Evidence:** Source, pp. 74, 88–89.

| ID | Preconditions / action | Expected result | Traceability |
|---|---|---|---|
| AC-API-001 | Authorized Analyst submits valid case twice with identical key/body | One `NEW` case and identical response; `201` initial creation; no duplicate classification-triggering business transition | API-001; SCR-001-E04; Source, pp. 12, 83, 89; `TST-001` |
| AC-API-002 | Reuse case-create key with changed body | `409 IDEMPOTENCY_CONFLICT`; no second case | API-001; Source, p. 89; `TST-002` |
| AC-API-003 | Foreign-tenant token reads valid case ID; compare absent ID | Same non-disclosing not-found class, no private existence/content | API-003; Source, pp. 23, 89; `TST-003`, `T-01` |
| AC-API-004 | Owner submits stale `If-Match` | `409 CASE_VERSION_CONFLICT`, safe current revision, no business mutation/outbox accepted-transition event | API-004; SCR-002-E02; Source, pp. 25, 84 |
| AC-API-005 | Valid authorized upload accepted; unsafe PDF then processed | Acceptance returns `202`, not readiness; unsafe content becomes quarantined and never indexed; macros/remote references do not execute/fetch | API-006–007; Source, pp. 30–32, 83, 89; `TST-015`, `T-04` |
| AC-API-006 | Source ACL revoked after indexing, then query and publication | No forbidden evidence on next query; stale authorization cannot pass publication gate | API-013–015, 017; Source, pp. 28, 46, 89; `TST-004`, `T-08` |
| AC-API-007 | Accepted run; disconnect/reconnect with last offset; refresh | Scope-safe retained-event backfill, increasing offsets and persisted progress; no restarted run/duplicate side effects | API-008, 010–012; SCR-004-E02–E03; Source, pp. 55, 58 |
| AC-API-008 | Model returns unknown fields, invalid citations or injected control characters | `MODEL_OUTPUT_INVALID`; no publication | API-036 / API-010 outcome; Source, pp. 38, 89; `TST-005` |
| AC-API-009 | Approve wrong/previous artifact hash | Stale rejection with `409` supported, audited; no changed-artifact publication under old approval | API-017; Source, pp. 45–46, 83, 89; `TST-006`, `T-03` |
| AC-API-010 | Analyst tries high-risk self-approval or publication without required review | Denied; no response published | API-017 / gate; Source, pp. 11, 44–46, 85 |
| AC-API-011 | Review task reaches configured SLA | No implicit approval; reassignment/escalation recorded | API-016–017 processing; Source, pp. 45, 89; `TST-010` |
| AC-API-012 | Replay same outbox event, including 100-repeat security fixture | Exactly one accepted business transition; duplicates/stale revisions safely ignored/recorded | API-R-008; Source, pp. 48–50, 88–89; `TST-007`, `T-07` |
| AC-API-013 | Provider sends 429 storm; workspace admission unavailable | Capped retries and controlled admitted load; throttled clients get `429` + `Retry-After`; saved cases remain available | API-008–009, 048–049; Source, pp. 28, 69, 89; `TST-008` |
| AC-API-014 | Missing/insufficient citations or evidence quality | Unsupported/needs-review outcome, never fabricated approved context; `NO_SUPPORTED_EVIDENCE` for insufficient retrieval support | API-013 / run; Source, pp. 36, 89; `TST-009` |
| AC-API-015 | Planner attempts arbitrary MCP function or equivalent substitute for denied action | `DENY` before dispatch; discovery/model text grants no authority | API-045–046; Source, pp. 41–42, 87, 89; `TST-014` |
| AC-API-016 | Generation down or vector index degraded | Manual mutation/evidence search remain available where supported; lexical fallback visibly reduced quality; no authorization/approval bypass | API-004, 013, 031; Source, pp. 69, 79 |
| AC-API-017 | Revoke connector credentials with queued jobs; incomplete provisioning attempts sync | Revoked jobs fail `CONNECTOR_REAUTH_REQUIRED` without secrets; incomplete provisioning blocks sync | API-018–019; Source, pp. 27, 78 |
| AC-API-018 | Close eligible case and inspect lineage | Immutable approved answer/cited-version/reviewer-decision snapshot; historical lineage not altered by later revisions | API-005; Source, pp. 25–26 |
| AC-API-019 | Single Admin initiates export; authorized export subsequently completes | Single Admin insufficient; authorized package has checksummed required content, excludes secrets/internal prompts | API-025; Source, pp. 78–80, 88; `T-11` |
| AC-API-020 | Authorized deletion targets held records | Held records retained and receipted; eligible deletion uses tombstones/blob/index removal and auditable completion | API-026, 040; Source, pp. 80, 89; `TST-013` |
| AC-API-021 | Auditor browses audit and attempts historical modification | Cursor-paginated authorized immutable records; historical edit denied; no secrets/full prompts/private existence in errors | API-021; Source, pp. 62, 83–84, 88; `T-09` |
| AC-API-022 | Operator replays dead letter without required controls, then with valid controls | Missing reason/dry-run/scope validation cannot authorize replay; valid replay preserves identity unless explicit migration provenance | API-038; Source, p. 50 |
| AC-API-023 | Regional outage attempts unapproved fallback | Restricted material never sent to unapproved deployment/region; approved fallback must preserve or strengthen data-handling class | API-036, 049; Source, p. 37; `T-06` |
| AC-API-024 | Regressed safety score or insufficient statistical confidence | Release promotion blocked; quality cannot excuse critical isolation/approval failure | API-023–024, 043; Source, pp. 75–76, 88–89; `TST-016` |
| AC-API-025 | Representative reference-load case creation/search | Case identifier P95 meets reconciled 300 ms criterion; search P95 `<1.5 s` excluding remote connector fetch | API-001, 013; Source, pp. 12, 65, 68; boundary Needs confirmation |
| AC-API-026 | Dependency fails during mutation/outbox commit | No partial accepted business mutation without required atomic outbox; caller gets safe error or persisted recoverable operation, never ambiguous success | API-R-004–009; Source, pp. 17, 52 |
| AC-API-027 | Reuse pooled DB connection across tenant transactions | Tenant context reset; no prior-tenant data visible; workspace-tenancy integrity enforced | API-R-010; Source, p. 86 |
| AC-API-028 | Inspect public bodies, failures, telemetry and provider requests | No raw provider/connector credentials, user document text in diagnostics, unrestricted internal prompts or unauthorized existence disclosure | API-R-018, API-047–049; Source, pp. 54, 64, 84, 88; `T-05` |

## Consistency and Open Questions

### Conflicts and Required Amendments

This specification does not rewrite [01_screen_functions.md](01_screen_functions.md). Earlier proposals remain proposals.

| ID | Affected requirements / earlier IDs | Evidence and conflict | Required resolution |
|---|---|---|---|
| OQ-API-001 | API-008–009; OQ-SF-003, SCR-002-E05 | Source pp. 15–17 registers `POST /v1/runs`; pp. 12, 40, 83 registers case-nested path | Decide canonical creation route, aliases and shared idempotency namespace; neither path is silently removed |
| OQ-API-002 | API-004, 050; OQ-SF-002, SCR-007-E01 | Source p. 24 workspace settings text associates case PATCH | Supply valid workspace settings load/save contract; do not use case mutation to save workspace policy |
| OQ-API-003 | API-R-018; OQ-SF-007, SF-015 | Source p. 54 says snake-case codes; pp. 84, 89 use uppercase literals | Preserve literals; confirm naming convention and compatibility rule |
| OQ-API-004 | API-005, 057; OQ-SF-005 | Source p. 25 omits transition into `CLOSED` and reopen route | Define close/reopen role, guards, revision semantics and statuses |
| OQ-API-005 | API-008–012; OQ-SF-006 | Source p. 41 missing approval stop condition versus valid `AWAITING_REVIEW`; p. 90 timeout example 180 s | Define valid waiting, terminal missing approval and timeout coverage/recoverable representation |
| OQ-API-006 | API-R-016, AC-API-025; OQ-SF-008 | Source p. 12 “within 300 ms” versus p. 65 “under 300 ms” | Set strict/non-strict boundary and response-time measurement |
| OQ-API-007 | API-007; SCR-002-F15–F16, OQ-SF-015 | Earlier screen specification leaves status mechanism unresolved; Source pp. 30–32 explicitly provides document status GET | Required future screen amendment: link status observation to API-007, without inventing polling frequency |
| OQ-API-008 | API-030–044 and event mappings | Source repeats mutation/event boilerplate beside GET endpoints | Confirm which reads can allocate jobs and exact audit/event emission triggers; do not cause deployment/purge/release events merely by reading |
| OQ-API-009 | API-016–017; SCR-005-E01–E02, OQ-SF-016 | Source pp. 45, 58 requires exact inspection but supplies no detail endpoint/schema or publication trigger | Allocate review-detail fields/contracts and separate accepted decision from publication completion |
| OQ-API-010 | API-R-002, API-046 | Source p. 51 UUIDv7 baseline; p. 87 A2A example uses placeholder `tenant_example_01`, `case_demo` | Finalize typed identity schema; placeholders are not production formats |

### Open Contract Decisions Beside the Affected APIs

| ID | Affected APIs / requirements | Needs confirmation | Evidence / dependency |
|---|---|---|---|
| OQ-API-011 | All public APIs; API-R-001 | Exact role matrix, Owner/Member meaning, Admin terminology, auditor redaction, service/probe scope | Source pp. 21–23, 83; earlier OQ-SF-009 |
| OQ-API-012 | All APIs; shared parameter tables | Complete controlled IDL: property names, wire types, required/null fields, lengths, defaults, allowed enums, content types and unknown-field handling | Source pp. 55–56, 82–87 only partial contracts; earlier OQ-SF-011 |
| OQ-API-013 | AUTH-P / AUTH-I / AUTH-T | Identity provider, audience/issuer/algorithm literals, token/session/CSRF/CORS behavior, service grants and correlation headers | Source pp. 16, 18, 21, 90; BFF remains optional |
| OQ-API-014 | API-R-007–008 | Key length/scope/fingerprint canonicalization, in-flight races, failed outcomes, retention and expiry; public versus internal key transport | Source pp. 25, 54; no full replay contract |
| OQ-API-015 | API-002, 011, 016, 019, 021, 020 | Pagination applicability, cursor names/expiry, wrappers, sizes, ordering, filters, snapshot behavior | Source pp. 54, 57, 83; earlier OQ-SF-012 |
| OQ-API-016 | API-004–005, 028, 050 | `If-Match` syntax, missing-precondition error, patch format, field mutation permissions, revision JSON representation | Source pp. 24–25, 83–86 |
| OQ-API-017 | API-006–007, 054 | Upload encoding/count/aggregate cap, MB bytes, bomb threshold, OCR option, signed source expiry and anchor representation | Source pp. 30–32, 52; earlier OQ-SF-015 |
| OQ-API-018 | API-008–012, 036, 042, 049 | Admission quotas versus reference capacity, runtime/provider timeouts, parsing retry caps, stop codes and mutation retry/cancel support | Source pp. 38–42, 68–70, 90; earlier OQ-SF-017 |
| OQ-API-019 | API-012, 047 | SSE event schema, heartbeat/backfill/expired offsets/session expiry; webhook destination/signature/age/retry/status contracts | Source p. 55 |
| OQ-API-020 | API-013–015, 045 | REST search request, scoring/quality thresholds, source-version selection, evidence schema, insufficient-evidence HTTP mapping | Source pp. 35–36, 87, 90 |
| OQ-API-021 | API-016–017, 052–053 | Required rationale/review fields, decision literals, hash canonicalization, current assignment checks, repeated decision behavior, override/rework contract | Source pp. 44–46, 58 |
| OQ-API-022 | API-018–019, 048, 055–056 | Connector providers/permissions, health/configuration interface, concurrent sync, credentials lifecycle and provisioning status | Source pp. 27–29, 78, 90 |
| OQ-API-023 | API-022–024, 041 | Usage units/windows/freshness; evaluation frozen-version inputs/status/schema; metrics format and safe labels | Source pp. 64–66, 74–76 |
| OQ-API-024 | API-025–026, 029, 040 | Independent approver eligibility, approval binding/time validity, hold creation/release, operation status/download/receipt schemas and held-data completion | Source pp. 61–63, 78–80 |
| OQ-API-025 | API-032–035, 038–044 | Engineering/operational complete contracts, authorization and success/error statuses; replay dry-run proof and release gate input schemas | Source chapters 1, 4, 13–14, 18–20 |
| OQ-API-026 | Error matrix / API-R-018 | Complete HTTP/code/retry mapping including authentication, upload, stale approval, unsupported evidence, dependency faults and stream errors | Source pp. 54, 84, 89; later Exception Handling Specification |
| OQ-API-027 | API-048–049, storage/security context | Supported cloud region/search/identity/models/corporate retention/connector permissions; encryption-key isolation versus rotation throughput | Source pp. 10, 90; earlier OQ-SF-021–022 |

### Later-Stage Dependencies

| Specification dependency | Requirements to carry forward |
|---|---|
| Data Specification — To be defined in a later stage | API-R-002–012; immutable case revisions/document derivatives/evidence sets/approvals; artifact hashing and canonicalization; operation/idempotency ledger; event/outbox schemas; tenant/workspace constraints and RLS reset; tombstones/legal holds/receipts; public-versus-storage type mapping |
| Exception Handling Specification — To be defined in a later stage | API-R-013–018; error matrix; permanent versus transient failures; bounded retries/circuit breakers; unsafe file quarantine; stale approval/revision errors; async operation failure and partial-retention receipts; stream cursor recovery |
| Workflow / operational specifications — To be defined in a later stage | Run/review timeout distinction; stage checkpoints; connector reconciliation; purge/export controls; signed webhooks; operator replay; release/evaluation gates |
| Screen consistency amendments | API-007 status contract; canonical API-008/009 resolution; API-050 settings contract; exact review inspection/publication behavior. Preserve all existing `SCR-*`, `SF-*`, `INT-SF-*`, `AC-SF-*`, `OQ-SF-*` IDs |
| `08_architecture_decision.md` — To be defined in a later stage | Consolidate unresolved decisions from completed Markdown only, linking `02_api.md` requirement/API/open-question IDs and `01_screen_functions.md` affected IDs; no invented owner, deadline or approval |

No open decision in this document has a supplied owner, deadline or approval. Missing schemas or statuses must be explicitly resolved before implementation lock rather than silently chosen by the implementation AI.
