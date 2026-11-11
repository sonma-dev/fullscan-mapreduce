# 2. API Specification

## API Inventory and Responsibilities

### Baseline and evidence convention

`02_api.md` specifies **OrionDesk AI**, `OD-AI-DDS-001`, release `R1.0`, design revision `1.3`. **Confirmed** means confirmed behavior of the fictional reference design, not deployed-product evidence. The source states: “All numbers are design assumptions, not measured production performance.” API identifiers below are assigned traceability identifiers, not claimed source API numbers. [Source: `1794325316-OrionDesk_AI_Detailed_Design_Specification.pdf`, pp.1–2, findings api:r2:c1:f1–f3, api:r2:c2:f1.]

All source citations in this file refer to that exact filename and original PDF page numbers. **Needs confirmation** is an implementation blocker, not permission to choose a default. No proposals are approved. The preceding specification is [01_screen_functions.md](01_screen_functions.md); SCR/SF/OQ identifiers retain its meanings. Screen associations below identify response consumers or related domain operations; they do not establish an unspecified button, route or launch placement.

External OpenAPI is authoritative for REST clients; repository-controlled IDL generates OpenAPI/protobuf, and protobuf governs internal gRPC. The actual definitions are not supplied. This specification preserves known behavior without inventing complete schemas. CI prevents incompatible field deletion or enum changes. Nonbreaking evolution is additive; removal requires scheduled migration. Domain teams own case/policy APIs, platform teams identity/messaging and AI platform the gateway. Baseline changes require an architecture decision; approved records increment minor revision and incompatible protocols major revision. Revised invariants require negative tests. [pp.8, 15, 55, 82; api:r2:c4:f2,f8; api:r2:c6:f7; api:r2:c18:f11; api:r2:c26:f1.]

### Shared authentication and authorization — API-045

Every request binds an authenticated principal and tenant. Browser REST authentication uses OIDC authorization code with PKCE; token semantics include issuer, audience, expiry, subject and tenant. Reject unexpected algorithms or missing tenancy claims. Long-lived refresh tokens must not be in browser local storage. A BFF issuing secure, HttpOnly, SameSite cookies is permitted, not selected. Exact identity endpoints, allowed algorithms/audiences, session lifetimes and token transport schema are **Needs confirmation** (earlier SF-003/OQ-002). [pp.15,21; api:r2:c6:f2; api:r2:c8:f1–f3.]

Authorization combines role, tenant, workspace membership, case sensitivity, originating document ACL, requested action and segregation of duties. Edge checks do not replace transaction-time domain checks. Navigation hiding is not authorization. Baseline roles are `Analyst`, `Reviewer`, `Admin`, `Auditor`, `Service`; map `Workspace Admin`, `Owner`, `Member`, `approver` and `Operators` before implementation. An Analyst cannot approve their own high-risk recommendation; approval tasks prohibit self approval. Auditor reads are redacted and cannot edit case content. [pp.11,22,85; api:r2:c5:f2–f3; api:r2:c8:f7–f8; api:r2:c27:f5; SF-002/OQ-001.]

Internal HTTP/gRPC is generated/versioned and independently authorized, using mTLS, service audiences and scoped IAM. Deployment units never share service identities; managed workload identity replaces static credentials where supported. Service credentials rotate and never appear in prompts/traces. No internal route below becomes browser-accessible merely through this inventory. [pp.16,18,21,54; api:r2:c6:f11; api:r2:c7:f3; api:r2:c8:f3; api:r2:c18:f1.]

### Public HTTP inventory

`S` means synchronous representation/decision; `A` means persisted asynchronous operation; `NC` means exact success mode/status **Needs confirmation**. Every row uses API-045 authentication and resource predicates in addition to its listed scope. `Scope NC` does not authorize any baseline role. The `202` rows acknowledge work, not completed processing or approved publication.

| ID | Method and path | Responsibility / related screen operation | Mode; confirmed success | Authorization scope | Source |
|---|---|---|---|---|---|
| API-001 | `POST /v1/cases` | Create case; SCR-001/SCR-002, SF-006 | S; `201`, case identifier | Analyst; idempotency | p.83 api:r2:c26:f6 |
| API-002 | `GET /v1/cases?cursor=...` | Case list; SCR-001 | Read; status NC | Scope NC | pp.57–59 api:r2:c19:f3,f14 |
| API-003 | `GET /v1/cases/{caseId}` | Authorized current revision; SCR-002 | S; `200` | Analyst / Reviewer | p.83 api:r2:c26:f7 |
| API-004 | `PATCH /v1/cases/{caseId}` | Revisioned case mutation; SCR-002/SF-006 | S; `200` / `409` | Owner; `If-Match` | pp.25,83 api:r2:c9:f8; api:r2:c26:f8 |
| API-005 | `POST /v1/cases/{caseId}/close` | Snapshot approved lineage; SCR-002 | NC | Role/closure guards NC | p.26 api:r2:c9:f11,f13 |
| API-006 | `POST /v1/cases/{caseId}/attachments` | Ingestion operation; SF-007 | A; `202` | Analyst | p.83 api:r2:c26:f9 |
| API-007 | `GET /v1/documents/{documentId}/status` | Document processing status; SF-007 | Read; status NC | Current document scope; role NC | pp.30–32 api:r2:c11:f6,f13 |
| API-008 | `POST /v1/search` | Permitted lexical/semantic evidence; SCR-003/SF-008 | S; `200` | Member; document ACL | p.83 api:r2:c26:f15 |
| API-009 | `GET /v1/evidence/{evidenceId}` | Evidence representation; SCR-003 | Read; status NC | Current evidence/document scope; role NC | pp.35–36 api:r2:c12:f5 |
| API-010 | `GET /v1/cases/{caseId}/evidence` | Case evidence; SCR-002/003/005 | Read; status NC | Scope NC, current ACL | pp.57–59 api:r2:c19:f4,f14 |
| API-011 | `POST /v1/cases/{caseId}/runs` | Bounded AI workflow; SCR-004/SF-009 | A; `202` | Analyst; admission checks | p.83 api:r2:c26:f10 |
| API-012 | `POST /v1/runs` | Chapter run-creation contract; relation to API-011 NC | NC | Scope NC; OAuth audience/idempotency | pp.15–17 api:r2:c6:f4,f14 |
| API-013 | `GET /v1/runs/{runId}` | Stages/evidence metadata; SCR-004 | S; `200` | Analyst / Reviewer | p.83 api:r2:c26:f11 |
| API-014 | `GET /v1/runs/{runId}/steps` | Run steps; SCR-004 | Read; status NC | Scope NC | p.42 api:r2:c14:f6 |
| API-015 | `GET /v1/streams/runs/{runId}` | SSE run updates; SCR-004 | Streaming; `200` | Analyst / Reviewer; retained scoped backfill | pp.55,83 api:r2:c18:f9; api:r2:c26:f12 |
| API-016 | `GET /v1/review-queue` | Eligible review tasks; SCR-005/SF-010 | Read; status NC | Policy pool/minimum role/duties; full scope NC | pp.45–46 api:r2:c15:f6–f7,f13 |
| API-017 | `POST /v1/approvals/{approvalId}/decision` | Hash-bound review decision; SCR-005 | S; `200` / `409` | Reviewer; actor/hash/duties | p.83 api:r2:c26:f13 |
| API-018 | `POST /v1/connectors/{connectorId}/sync` | Incremental source sync; SCR-006/SF-011 | A; `202` | Admin; provisioning complete | pp.78,83 api:r2:c25:f2; api:r2:c26:f14 |
| API-019 | `GET /v1/connectors/{connectorId}/runs` | Sync runs; SCR-006 | Read; status NC | Scope NC | pp.28–29 api:r2:c10:f5 |
| API-020 | `GET /v1/audit/events` | Cursor-paginated immutable log; SCR-008/SF-013 | S; `200` | Auditor; redacted scope | p.83 api:r2:c26:f16 |
| API-021 | `GET /v1/usage` | Costs/quotas/trend estimates; SF-014, screen placement NC | S; `200` | Admin | p.83 api:r2:c26:f17 |
| API-022 | `POST /v1/evaluations` | Frozen benchmark evaluation; no dedicated screen confirmed | A; `202` | Admin | p.83 api:r2:c26:f18 |
| API-023 | `GET /v1/evaluations/{evaluationId}` | Evaluation read; screen placement NC | Read; status NC | Scope NC | pp.74–76 api:r2:c24:f4,f13 |
| API-024 | `POST /v1/workspaces/{workspaceId}/export` | Controlled export/manifest; SF-017, placement NC | A; `202` | Admin + approver; two independent checks | pp.78–83 api:r2:c25:f1,f9; api:r2:c26:f19 |
| API-025 | `POST /v1/workspaces/{workspaceId}/delete` | Legal-hold-safe deletion; SF-017, placement NC | A; `202` | Admin + approver; two independent checks | pp.78–83 api:r2:c25:f1,f10; api:r2:c26:f20 |
| API-026 | `GET /v1/me` | Principal context contract; screen placement NC | Read; status NC | Authenticated principal; exact scope NC | pp.21–23 api:r2:c8:f5 |
| API-027 | `PUT /v1/workspaces/{workspaceId}/members` | Membership contract; screen placement NC | NC | Exact mutation scope NC | pp.22–23 api:r2:c8:f6 |
| API-028 | `GET /v1/model-catalog` | Deployment catalog; related SCR-007, placement NC | Read; status NC | Scope NC; workspace policy governs models | pp.37–39 api:r2:c13:f2,f4 |
| API-029 | `GET /v1/openapi.json` | REST contract retrieval | Read; status NC | OAuth audience/idempotency register; precise policy NC | pp.54–56 api:r2:c18:f7,f16 |
| API-030 | `POST /v1/security/holds` | Security-hold contract; detailed lifecycle/placement NC | NC | Scope NC | pp.61–63 api:r2:c20:f4–f5 |
| API-031 | `POST /v1/design-decisions` | Change/baseline decision record | NC | OAuth audience/idempotency; action role NC | pp.8–10 api:r2:c4:f3,f5 |
| API-032 | `GET /v1/design-baselines/{id}` | Baseline contract read | Read; status NC | Scope NC | pp.9–10 api:r2:c4:f4–f5 |
| API-033 | `GET /v1/system/degraded-modes` | Degradation integration; SF-017 | Read; status NC | OAuth audience/idempotency; precise scope NC | pp.68–70 api:r2:c22:f4 |
| API-034 | `GET /v1/health/live` | Runtime health contract; probe meaning NC | Read; status NC | OAuth audience/idempotency register; anonymous exception not confirmed | pp.18–20 api:r2:c7:f5,f14 |
| API-035 | `GET /v1/health/ready` | Runtime readiness contract; criteria NC | Read; status NC | Scope NC; no anonymous exception confirmed | pp.19–20 api:r2:c7:f6,f14 |

### Internal HTTP inventory

These callers are service/operator integrations, not SCR screens. All use independent API-045 service authorization; precise audiences, IAM grants and scope checks are **Needs confirmation**. Success statuses and complete schemas are not supplied.

| ID | Method/path | Responsibility and calling boundary | Success mode/status | Source |
|---|---|---|---|---|
| API-036 | `POST /internal/model/generate` | Scoped gateway generation, orchestration integration | NC | pp.37–39 api:r2:c13:f3 |
| API-037 | `GET /internal/workflows/{runId}` | Durable workflow read | Read; status NC | pp.48–50 api:r2:c16:f4 |
| API-038 | `POST /internal/deadletters/{id}/replay` | Operator-controlled validated recovery | NC | pp.49–50 api:r2:c16:f5,f11 |
| API-039 | `GET /internal/storage/documents/{id}` | Tenant-predicated document storage access | Read; status NC | pp.51–53 api:r2:c17:f4 |
| API-040 | `POST /internal/storage/purge` | Tombstone/retention purge integration | NC | pp.51–53 api:r2:c17:f5–f6 |
| API-041 | `GET /internal/metrics` | Internal observability signals | Read; status NC | pp.64–66 api:r2:c21:f3–f4,f10 |
| API-042 | `GET /internal/capacity` | Capacity/admission integration | Read; status NC | pp.69–70 api:r2:c22:f5 |
| API-043 | `POST /internal/releases` | Engineering release record/rollout integration | NC | pp.71–73 api:r2:c23:f3,f12 |
| API-044 | `GET /internal/releases/{releaseId}` | Release representation | Read; status NC | pp.72–73 api:r2:c23:f5,f18 |

Chapter registers impose OAuth audience/idempotency policy on API-036/037/039/043 and schema/bounded-error obligations on their secondary APIs. Generic requirements must be reconciled with specific service authentication and read semantics, not treated as an unspecified browser grant.

### Other contract boundaries

| ID | Interface | Responsibility/caller | Authentication/authorization and outcome | Source |
|---|---|---|---|---|
| API-045 | OIDC and service identity | Browser/identity provider; service-to-service | As above; provider URLs and credential wire contracts NC | pp.15–22 |
| API-046 | Domain events/outbox | Producers/consumers; includes review lifecycle below | Signed immutable job tenancy, versioned envelope, deduplication; not automatically SSE | pp.17,48–50,82,87 |
| API-047 | `knowledge.search@v1` MCP | Research/tool client to approved MCP server | Tenant `read:permitted_documents`; read-only; transport NC | p.87 api:r2:c28:f10–f12 |
| API-048 | `research.grounded_search.v1` A2A | Authorized agent handoff | Separate capability grant, schema/deadline/trace; receiver may decline; transport NC | pp.41,87 api:r2:c14:f9; api:r2:c28:f9 |
| API-049 | Optional outbound webhooks | Case event delivery to subscriber | Signed, recipient age/signature checks, exponential retry, no case rollback | p.55 api:r2:c18:f10 |
| API-050 | Enterprise repository integration | Connector workers/provider | Workspace secret-store credential reference, capability/ACL/history contract | pp.15,27–29 api:r2:c6:f2; api:r2:c10:f1–f11 |
| API-051 | External model deployment integration | Gateway/provider | Approved scoped context/structured prompts; no connector tokens/DB access | pp.15,37–39 api:r2:c6:f2; api:r2:c13:f1–f11 |
| API-052 | Private object access | Authorized document/evidence consumer | Encrypted objects, opaque public names, scoped short-lived signed URL | pp.51–52 api:r2:c17:f6,f10 |

No confirmed endpoint exists for policy-setting mutation separate from the conflicted case PATCH association, classification correction, provisioning, cancellation, reopening, override, reassignment, publication, signed-URL issuance or webhook subscription administration. Those responsibilities are **Needs confirmation**, not out of scope. Explicit exclusions are physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing, agent administrative cloud permissions and application-hosted GPU inference. Cross-region active/active mutation, OCR beyond English and customer-managed weights are deferred. [pp.9–10,19; api:r2:c4:f9,f13; api:r2:c7:f8.]

## Interfaces by API

### Field-definition convention

For every API-001–052, unspecified path/query/header/body and response fields remain **Needs confirmation** individually: exact spelling, wire type, requiredness, format, bounds, enum, default, unknown-field behavior and serialization. An empty list of supplied fields does not establish an empty body or prohibit additional fields. Unless expressly stated, no default is approved. Selected database fields and descriptive response attributes are not complete wire schemas.

Every path placeholder is required to identify that path's resource; wire type/format is **Needs confirmation**, including `caseId`, `documentId`, `evidenceId`, `runId`, `approvalId`, `connectorId`, `workspaceId`, `evaluationId`, `releaseId`, `id`. Persistent UUIDv7 and reference UUID columns do not independently settle all REST typing. Body tenancy is not client authority to substitute token tenancy. [pp.51,83,85–86; api:r2:c17:f2; api:r2:c27:f8–f11.]

### Shared parameters and representation

| Name / location | Meaning and applicability | Confirmed constraint / required status | Type, default and missing-value behavior |
|---|---|---|---|
| `cursor` / query API-002 | Continuation of case list | Name appears in `GET /v1/cases?cursor=...` | Encoding/type/optional-first-page/default/expiry NC |
| Pagination / other public APIs | Cursor pagination convention; explicitly API-020 immutable log | Cursor-based, not offset-based | Exact query/output fields, order, page sizes/defaults, snapshot consistency NC |
| `If-Match` / request header API-004 | Case revision condition | Required by case mutation contract; conflict returns current revision | Exact representation/ETag syntax/type and missing-header status NC |
| `Idempotency-Key` / request header | Job-creating POST mutations; API-001 explicitly uses an idempotency key | Required for long-running job POSTs; same fingerprint returns original operation; changed fingerprint conflicts | Key format/length, full scoping, missing-header response and fingerprint construction NC; actor/fingerprint outcome retained 24 hours |
| `Last-Event-ID` / request header API-015 | Resume SSE after received offset | Used on reconnect, backfill only retained authorized events | Encoding/type, absent/expired/future offset behavior NC; no default |
| `Retry-After` / throttled response/provider response | Caller/provider backoff signal | API admission `429` includes it; connector workers honor it | Format/value/min/max NC |
| `trace_id`, `correlation_id` / request context | Cross-boundary tracing | Every request carries both; correlation independent of provider trace IDs | Transport/header name, generation/validation/type NC |
| `tenant_id`, `revision`, `actor_id`, `occurred_at`, correlation ID / durable record metadata | Identity/revision/provenance | Required wherever operation changes durable state | Exact types/wire representation NC; not automatically editable body fields |
| Timestamp / public response | Durable API time | RFC 3339; server UTC | Field names/precision NC; workspace-local display cannot change ordering |

Sources: pp.17,25,48,54–59,64,69; api:r2:c6:f3,f11–f12; api:r2:c9:f8; api:r2:c16:f2; api:r2:c18:f3–f4,f9; api:r2:c19:f12; api:r2:c21:f1; api:r2:c22:f7.

### Case interfaces — API-001–005

| Interface | Input meanings supported by source | Successful response meanings | Open schema decisions |
|---|---|---|---|
| API-001 | Case/business context; Analyst; idempotency key | `201`, case identifier; initial case `NEW` | Create body field names/types/requiredness and identifier/revision response spelling NC |
| API-002 | Authorized list and `cursor` | Authorized case-list contract | Columns/filters/sort/counts/pagination schema/status NC; screenshot cards are not response requirements |
| API-003 | `caseId` | `200`, authorized current revision | Full case representation/field redaction NC |
| API-004 | `caseId`, `If-Match`; case mutation | `200`; stale revision `409 CASE_VERSION_CONFLICT` with current revision | Patch media type, permitted fields by state, response fields and merge semantics NC |
| API-005 | `caseId`; closure guards | Snapshot approved answer, cited versions and reviewer decisions | Closure entry edge, role/body/status/receipt, reopen contract NC |

Case attributes confirmed semantically are title, description, priority, sensitivity label, status, owner, current approved result and monotonic revision. Attachments/runs are separate immutable-ID-linked entities. Priority uses explicit impact and urgency, never model alone; formula/types/catalogs are NC. Asynchronous classification stores labels/confidences/provenance; correction needs reason code, but correction endpoint/permissions/catalog are NC. Business-calendar deadlines use workspace timezone; breach prediction is advisory. [pp.12,24–26; api:r2:c5:f7; api:r2:c9:f6–f11.]

Reference case backing schema has `id UUID`, tenant/workspace UUID foreign keys, status `TEXT NOT NULL`, revision `BIGINT NOT NULL DEFAULT 1`, sensitivity `TEXT NOT NULL DEFAULT 'INTERNAL'`, timestamps `TIMESTAMPTZ NOT NULL DEFAULT now()` and `UNIQUE (tenant_id,id)`. These are database defaults, not client defaults or complete REST fields. [p.86; api:r2:c27:f8–f9.]

### Document interfaces — API-006–007 / API-052

| Input/output | Confirmed meaning/constraint | Requiredness/type/default gap |
|---|---|---|
| Uploaded file | PDF, DOCX, HTML, UTF-8 text; MIME signature matches extension; configurable 25 MB per-file cap; decompression-bomb protection | Multipart field names, count/name constraints, MB byte convention, active cap source, threshold NC |
| Ingestion acknowledgement | API-006 `202`, ingestion operation, not completed indexing | Operation/document identifiers and response schema NC |
| Document status | Catalog below; scan/quality guards | State field spelling/type, response status/details/quality payload NC |
| OCR fallback | Opt-in, provenance-marked; beyond English deferred | Input flag, actor, default and permission NC |
| Quality flags | Empty-page ratio, unknown-character ratio, table-loss indicators, language confidence | Numeric scales/thresholds/types NC |
| Chunk source anchor | URI, file hash, page and optional bbox; current access/resolvable anchor required | Exact schema/hash encoding/page origin/bbox units NC |
| Signed object URL | Access-controlled short-lived URL; public object name opaque | Issuance endpoint, expiry value, renewal, response fields NC |

PDF extraction preserves page indices/bboxes, table rows/columns, headings and reading order. Normalize transport artifacts without rewriting claims; content fingerprint plus pipeline version generates immutable derivative IDs, allowing side-by-side reprocessing. [pp.30–32,51–52; api:r2:c11:f1–f11; api:r2:c17:f6,f10; SF-007/OQ-010.]

### Search/evidence interfaces — API-008–010

API-008 returns `200` ACL-filtered lexical/semantic evidence. The source describes each evidence response item as including chunk ID, source title, document revision, page anchor and ACL digest. These attributes are required semantically, but exact wire names/types remain NC. Citation IDs are opaque and verified before display; citations resolve immutable anchors under current permission. Query/body schema, filters, confidence/quality threshold, results schema and pagination are NC. API-009 evidence ID and API-010 case evidence overlap are unresolved. [pp.34–36,57–59,83; api:r2:c12:f1–f9; api:r2:c19:f4; api:r2:c26:f15.]

Search representation includes `tenant_id`, `workspace_id`, `document_version_id`, `chunk_id`, language, classification, 1536-dimensional embedding and normalized keyword text. This is backing index data, not a required request vector or returned embedding. [p.34; api:r2:c12:f2.]

### Run interfaces — API-011–015 / API-036–037

| Interface | Confirmed request/response semantics | Needs confirmation beside contract |
|---|---|---|
| API-011 | Analyst, `caseId`; `202` starts bounded workflow | Body/model/prompt selectors, run identifier fields, admission thresholds NC |
| API-012 | Explicit chapter `POST /v1/runs`; validate/non-ambiguous outcome | Alias versus distinct path, body linkage, role and success status NC |
| API-013 | `runId`; `200` stages/evidence metadata | Exact stage/evidence/failed-checkpoint fields NC |
| API-014 | `runId`, run steps read | Schema, step pagination/status/scope NC |
| API-015 | `runId`, `Last-Event-ID` reconnect; `200` SSE | Event type/payload/id format, retention, heartbeat, expired offset, disconnect/error handling NC |
| API-036 | Scoped prompt/model-generation contract | Complete input/output JSON schema, RPC deadline, success status and job mode NC |
| API-037 | Workflow representation by `runId` | Exact checkpoint representation and read/allocation semantics NC |

Create run immediately and subscribe to server updates showing retrieval/generation/policy stages; refresh reconstructs server state. SSE offsets increase monotonically and replay retained events only within current caller scope. Do not equate domain event names with SSE types without IDL evidence. Display labels `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` remain UI labels, not replacements for the run catalog. Live announcements expose meaningful transitions only. [pp.55,57–59,83; api:r2:c18:f9; api:r2:c19:f7–f12; api:r2:c26:f11–f12; SCR-004/SF-009.]

### Review interfaces — API-016–017 / API-046

**Confirmed Review aggregate state catalog:** `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED`. **Every transition is guarded by actor, content hash and separation of duties.** This applies to API-016 task representations, API-017 decision processing and API-046 review lifecycle events. It does not supply exact edges, state wire field name/type, opening endpoint or decision-input enum; each remains **Needs confirmation**. [p.82 Appendix A.1; api:r2:c26:f5; earlier SCR-005/SF-010.]

| Review input/output meaning | Confirmed requirement | Type/requiredness/default decision |
|---|---|---|
| `approvalId` | Identify hash-bound review task | Required path component; type NC |
| decision | API-017 Reviewer action, `200` / `409` | Wire enum/name/type NC; do not infer input enum from states |
| actor, timestamp | Capture authenticated decision principal/time | Exact response fields/types NC; client cannot grant actor authority |
| evaluated artifact hash | Approval binds exact reviewed content | Binding mandatory; input field/algorithm/encoding NC |
| rationale / reason | Approval record includes rationale; backing catalog `reason` | Required input status/length/format NC |
| annotations | Optional approval annotations | Type/default NC |
| candidate, citations, model/prompt version, policy reasons | Reviewer must see exact artifact and inspect evidence before approval | Exact representation/field names NC |
| reviewer pool / minimum role | Policy-defined eligibility/duties | Catalog and membership predicate NC |
| SLA / expiry | Expiry reassigns/escalates, never approves | Value, timing, recipient and run effect NC |
| override evidence | Elevated role + secondary reviewer + audited reason | Endpoint, field schema and eligible independent roles NC |

Required review fields must be completed before Approve/Reject controls enable; the required field list is not supplied. API validation must enforce the eventual list server-side. Changed artifact decisions reject stale and are audited without accepted mutation. A recorded decision leads to publication validation, not unconditional publication. Denied rework uses a new run revision, never retroactive approval. [pp.44–46,58,83,85,89; api:r2:c15:f1–f11; api:r2:c19:f9; api:r2:c26:f13; api:r2:c27:f5; api:r2:c30:f6,f10.]

### Connector interfaces — API-018–019 / API-050

API-018 `202` starts incremental sync only after complete provisioning. API-019 reads sync-run context; exact fields/status/schema/pagination/role are NC. Semantic records contain provider cursor, high-watermark and error ledger; backing `connector_cursors` contains `connector_id`, `cursor`, `watermark`, `retry_state`. Credentials are workspace references to a dedicated secret store, not returned tokens. Capabilities are list, fetch, delta cursor, ACL and delete; unsupported capability yields lower-trust ingestion with visible warning. [pp.27–29,78,83,85; api:r2:c10:f1–f13; api:r2:c25:f2; api:r2:c26:f14; api:r2:c27:f7.]

Credential registration/revocation/reauthorization transport, Operator mapping, provider endpoint schemas, capability field types, warning and quarantine reason catalogs are NC. Revoked credentials cause queued jobs to fail `CONNECTOR_REAUTH_REQUIRED`, no token exposure. This literal lacks a confirmed HTTP mapping. [p.27; api:r2:c10:f6; SCR-006/OQ-013.]

### Audit, usage, evaluation and lifecycle interfaces — API-020–025 / API-040–041

| APIs | Confirmed representation / behavior | Missing wire contract |
|---|---|---|
| API-020 | `200`, cursor immutable redacted log; decision metadata, prompt-template digests, access events within scope | Filters/cursor/order/fields/types/retention boundary responses NC |
| API-021 | `200`, costs/quotas/trend estimates; workspace cost centers/model deployment versions; daily budget/forecast/rejected excess rollups | Units, date range, timezone, aggregation response schema NC; no rollup execution schedule supplied |
| API-022/023 | `202` frozen benchmark start / evaluation read | Dataset/version input, scorecard schema, evaluation status/read scope NC |
| API-024 | `202`, controlled checksummed manifest package of case metadata/approved artifacts/source refs/audit manifests; exclude secrets/internal prompts | Two-person approval protocol, manifest schema/checksum algorithm/download/status contract NC |
| API-025/040 | `202` workspace delete; internal purge status NC; hold-safe tombstones, eligible blob/index removal and completion receipts | Scope/hold partial-completion/status/receipt fields and polling NC |
| API-041 | Golden request/error/latency/saturation signals and AI grounding/empty retrieval/provider throttle/token/backlog age | Metric names/types/units/serialization NC |

Audit is append-only, batch-hash chained and exported to independently controlled retention storage. Operators query but cannot change historical review decisions. Diagnostics default to 30-day TTL; security audit follows separate fictional seven-year policy, legal holds and purge receipts. Corporate retention remains unselected. Single Admin export fails two-person control. Protected held records are retained and receipted; data subject requests share inventory, not a newly confirmed endpoint. [pp.11,62,64–66,74–80,83,88–89; api:r2:c5:f3; api:r2:c20:f11; api:r2:c21:f4,f7–f8; api:r2:c24:f3–f13; api:r2:c25:f1,f9–f10; api:r2:c29:f11; api:r2:c30:f13.]

### Remaining REST/internal interfaces — API-026–035, API-038–039, API-042–044

Each inventory path and its path placeholders are confirmed; all unlisted query/header/body/response fields, success statuses, defaults and exact caller scopes are NC.

| APIs | Supported additional requirements | Open decision |
|---|---|---|
| API-026/027 | Principal/tenant membership/resource-ACL boundaries; tenant/resource checks | Principal response/member list schema, update eligibility/concurrency, GET allocation NC |
| API-028 | Deployment-specific approved capability/region/data class/context length/cost/evaluation registry | Exact catalog fields/types/read scope NC; registry descriptions are not automatic wire fields |
| API-029 | Authoritative REST contract retrieval | Content representation/status/auth/access policy and GET allocation NC |
| API-030 | Security-holds contract exists | Hold target/create/release/lifecycle/role/effects NC; do not infer legal-hold implementation solely from path |
| API-031/032 | Baseline decision/change records with behavior/migration/threat/cost impact scores; revision governance | Score field names/scales, approval protocol and read allocation NC |
| API-033/042 | Capacity/degraded-mode integration, admission safety | Degradation enum, reduced-quality wire flag, threshold/status schema NC |
| API-034/035 | Private runtime health interfaces/registers | Probe criteria/dependency depth/caller/health payload/statuses NC |
| API-038 | Operator reason, dry-run validation, scope limit required; preserve original event identity except provenance-linked schema migration | Reason/scope field names/types, dry-run protocol/role/replay bounds/status NC |
| API-039 | Tenant-predicated current-authorized immutable document access | Object/body versus metadata output, read scope/status/URL issuance NC |
| API-043/044 | Reconstructible release digest/schema/prompt/model-policy binding; signed config/vault references | Release body/status/rollout gate schema, concrete audience/operator scopes NC |

Sources: pp.8–10,18–23,37–39,48–56,61–73; api:r2:c4:f3–f8; api:r2:c7:f5–f6,f14; api:r2:c8:f5–f6; api:r2:c13:f2–f4; api:r2:c16:f4–f5,f11; api:r2:c17:f4; api:r2:c18:f7,f11; api:r2:c20:f4–f5; api:r2:c22:f4–f5; api:r2:c23:f3–f12.

### Event contract — API-046

| Envelope field | Meaning | Requiredness / representation |
|---|---|---|
| `event_id` | Delivery/dedup identity | Required; type/version NC |
| `type` | Event kind | Required; enumerated supported names below, exhaustive catalog NC |
| `schema_version` | Payload/envelope version | Required; type/value NC |
| `tenant_id` | Immutable tenancy scope | Required; signed background-job scope; type NC |
| `aggregate_id` | Aggregate reference | Required; type NC |
| `aggregate_revision` | Stale/replay guard | Required; wire type NC |
| `occurred_at` | Event time | Required; UTC; exact precision/type NC |
| `trace_id` | Trace context | Required; type NC |
| `payload` | Event-specific data | Required; canonical JSON; complete typed payload NC |

All events use canonical JSON and UTC. Actor/revision/correlation durable-record metadata is additionally propagated where applicable; do not silently insert user-editable envelope fields or equate metadata `revision` with exact event wire `aggregate_revision`. Canonicalization standard and signed-envelope algorithm are NC. [pp.17,22,48; api:r2:c6:f12; api:r2:c8:f10; api:r2:c16:f2–f3.]

| Event | Producer | Selected payload labels, not exact typed JSON keys | Consumer action |
|---|---|---|---|
| `CaseCreated` | Case Service | Case ID / revision | Run classifier |
| `DocumentNormalized` | Ingestion | Version ID / source hash | Build index |
| `SearchIndexCommitted` | Indexer | Index generation / document revision | Invalidate query cache |
| `AgentPlanApproved` | Orchestrator | Run ID / plan hash | Dispatch plan steps |
| `ApprovalDecisionRecorded` | Policy Service | Task / actor / content hash | Validate publication |
| `WorkflowStageAdvanced` | Orchestrator | Run / stage / checkpoint | Resume consumers |
| `AccessDenied` | Policy Service | Principal / action / policy digest | Alert enrichment |
| `TenantDeletionVerified` | Retention Worker | Manifest ID / receipt hash | Close purge record |

Source p.87, api:r2:c28:f1–f8. The Review catalog above remains part of this boundary; no event-to-state transition mapping is implied by these labels.

Additional confirmed chapter events remain `BaselineCommitted`, `RunRequested`, `DeploymentPromoted`, `CaseStateChanged`, `ConnectorSyncStarted`, `ModelInvocationCompleted`, `DataRetentionPurgeCommitted`, `ApiCompatibilityVerified`, `UserReviewOpened`, `SecurityPolicyChanged`, `SloBurnRateDetected`, `BackpressureActivated`, `ReleasePromoted`, `EvaluationCompleted`. Their registers require versioned envelope/outbox, correlated audit without source text, ledger/revision duplicate checks and no reapplication. Producer/payload/SSE mappings remain NC where absent. [pp.10,17,20,26,29,39,53,56,59,63,66,70,73,76; api:r2:c4:f5,f14; api:r2:c6:f14–f15; api:r2:c7:f14–f15; api:r2:c9:f13–f14; api:r2:c10:f13–f14; api:r2:c13:f13–f14; api:r2:c17:f13–f14; api:r2:c18:f16–f17; api:r2:c19:f14–f15; api:r2:c20:f13–f14; api:r2:c21:f10–f12; api:r2:c22:f13–f14; api:r2:c23:f12–f14; api:r2:c24:f13–f14.]

### MCP/A2A and examples — API-047–048

| MCP field | Location/type | Meaning/constraint | Requiredness/default |
|---|---|---|---|
| `query` | Input `string` | Grounded search query | NC; length/default NC |
| `case_id` | Input `uuid` | Case context | NC; UUID version NC |
| `max_items` | Input `int<=10` | At most ten items for this tool only | NC; minimum/default NC |
| `evidence_set_id` | Output `uuid` | Evidence set reference | NC |
| `citations` | Output `Citation[]` | Grounded citations | NC; `Citation` definition absent |

`knowledge.search@v1` requires tenant-scoped `read:permitted_documents`, read-only effects and no arbitrary URLs/filesystem access. Approved MCP service credentials and pinned schemas do not replace separate authorization. Consequential external writes need human authorization and idempotency; browser arbitrary tool definitions are forbidden. [pp.7,41–42,87; api:r2:c3:f2–f4; api:r2:c14:f8,f12; api:r2:c28:f10–f12.]

**Source example, not defaults or schedule**, A2A p.87:

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

These exact example fields are string-valued except object `payload`; formal requiredness/types/defaults are NC. A2A additionally requires declared input/output schema, task/capability/deadline/trace concepts and permits receiving-agent decline. Output schema, authentication transport, rejection/error/status/retry contract are NC. `case_demo` cannot directly satisfy adjacent MCP UUID typing; identifier-resolution adapter is **Needs confirmation**, not approved string coercion. [pp.41,87; api:r2:c14:f9; api:r2:c28:f9,f13.]

Successful REST body examples cannot be generated as confirmed JSON because exact schemas are absent. The inventory's `201` identifier, `202` acknowledgements and `200` semantic outputs are the confirmed success contracts. Proposed field names or examples require a separately labeled future proposal; none are selected here. Webhook methods/URLs/payload/signature header/algorithm/key rotation/maximum event age/retry cap remain NC; recipients verify age and signature, and delivery failure never rolls back internal case state. [p.55; api:r2:c18:f10.]

## Processing and Consistency

### Shared processing procedure

1. Authenticate principal and immutable tenant; enforce gateway algorithm/audience/claims and quotas.
2. Validate payload before transaction or long-running allocation. Client validation is convenience only. Independently validate domain invariants and pinned tool arguments before dispatch.
3. Apply resource checks including workspace/sensitivity/duties and current document ACL; re-evaluate attributes inside transaction. Foreign resource identifiers cannot disclose existence.
4. Read mutable authority from PostgreSQL; objects hold sources/normalized artifacts, index is nonauthoritative and eventually consistent, cache ephemeral/versioned. Orchestrator has no direct DB credentials.
5. Check revision/hash/idempotency preconditions before accepted mutation. Rejected stale/unauthorized actions leave business state unchanged, but denial audit remains required.
6. Commit case mutations, approval decisions and outbox inserts in one ACID transaction. Atomically commit final-response pointer with satisfied publication gate. Index and webhooks reconcile asynchronously; use outbox or explicitly reconciled saga for state-changing workflows.
7. Carry tenant/revision/actor/time/correlation metadata and safe traces; do not log documents, credentials or full prompts in public errors/diagnostics.
8. If dependency unavailable, return documented retryable error or persisted asynchronous operation identifier, never ambiguous success. Exact per-operation branch/body/status remains NC where not in Appendix A.

Sources: pp.9,15–17,21–25,45,48–56,64; api:r2:c4:f12; api:r2:c6:f1–f12; api:r2:c8:f1–f11; api:r2:c9:f8–f9; api:r2:c15:f9–f10; api:r2:c16:f1–f10; api:r2:c17:f7; api:r2:c18:f12; api:r2:c21:f1.

Install transaction-scoped tenant RLS context; every storage predicate includes tenant. `cases` RLS uses `tenant_id = current_setting('app.tenant_id')::UUID`. Reset scoped pool variables after **every transaction**, including failures. Add production workspace-tenancy enforcement via foreign keys or controlled writes; selection is NC. Background jobs use signed immutable tenancy. [pp.22,51,86; api:r2:c8:f10; api:r2:c17:f1; api:r2:c27:f10–f11.]

### State catalogs and transitions

| Aggregate | Confirmed allowed states | Guards and supported transitions / open edges |
|---|---|---|
| Case | `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED` | Role/revision/approval. Initial NEW; NEW→TRIAGED→IN_PROGRESS; IN_PROGRESS→PENDING_APPROVAL or RESOLVED; PENDING_APPROVAL→RESOLVED or IN_PROGRESS. CLOSED final except explicit new-revision reopen. Closure entry/reopen target NC. |
| Document | `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED` | Virus scan/quality gate; exact edges NC. Unsafe content quarantine/no index; low-quality permitted content remains viewable but not autonomous support. |
| Run | `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED` | Checkpoint/runtime budget. Source linear stages checkpoint before downstream dispatch. AUTO_ALLOW route, exact failure edges, missing-approval trigger and recoverable timeout state NC. |
| Review | `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED` | Actor/content hash/separation of duties. Exact transition edges, opening/assignment transport and decision-input enum NC. Expiry never implicitly approves. |
| Policy outcome | `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY` | Deterministic normalized retained inputs/rule version; model risk tags cannot override. Not a Review decision enum. |

Sources: pp.12,25,44–45,49,82; api:r2:c5:f7; api:r2:c9:f7; api:r2:c15:f2–f3,f7; api:r2:c16:f7; api:r2:c26:f2–f5.

### Idempotency, concurrency and retry

- Actor/request-fingerprint outcomes are retained **24 hours**. Identical key/payload replay returns original outcome; changed fingerprint produces `409 IDEMPOTENCY_CONFLICT`. Scope beyond actor/fingerprint, concurrency locking, response retention, post-expiry behavior and missing-key errors are NC.
- Case PATCH requires `If-Match`; stale revision produces `409 CASE_VERSION_CONFLICT` and current revision. No automatic stale-edit retry or merge is authorized. Approval validates exact reviewed hash, actor/duties and current candidate; stale decision is rejected/audited.
- At-least-once consumers deduplicate event ID and operation key, detect stale aggregate revision, record duplicate outcome and do not reapply accepted mutation. No invariant depends on ordering across queue partitions. Replaying an accepted outbox event produces exactly one accepted business transition.
- Each workflow stage checkpoints before dispatch; plan revision is stored before effects. Dead-letter replay needs operator reason/dry-run/scope and original identity unless provenance-linked schema migration.
- Transient failures use bounded exponential backoff, jitter and per-dependency circuit breakers. Validation and permission failures are permanent, not retried. Read transient retries are allowed; mutable retries require idempotency; consequential writes additionally human authorization. Numeric counts/backoff/deadline bounds are NC.
- Connector workers honor provider `Retry-After`, quotas and fair scheduling. Provider 429 bursts have capped retries/admitted load. Quota exhaustion is terminal for current run, without automatic model/data-class change.

Sources: pp.25,38,40–42,48–50,54,89; api:r2:c9:f8; api:r2:c10:f10; api:r2:c13:f10; api:r2:c14:f5,f12; api:r2:c16:f6,f10–f11; api:r2:c18:f4; api:r2:c30:f1–f8.

### Domain processing and exceptions

1. **Ingestion:** validate formats/size/decompression; scan before parser, disable macros and remote embedded fetch. Preserve claims, immutable anchors and derivative versions. Unsafe files quarantine/no index. Low-quality permitted files remain viewable but cannot autonomously ground recommendations. [pp.30–32; api:r2:c11:f2–f11.]
2. **Sync:** cursor advances only after durable outcomes for preceding items. Bounded-retry malformed records quarantine with reason/correlation/remediation; remaining batch **may continue** with ledger-recorded exception. Do not force whole-batch failure or call partial batch all-success. Credential revocation fails queued work safely. [pp.27–29; api:r2:c10:f6–f11.]
3. **Index/retrieval:** failed indexing preserves accepted source metadata; reconcile fingerprints and repair outbox links. Search readiness is index coverage, not queue emptiness. Build parallel index and switch alias atomically only after completeness/recall checks. Form bounded lexical/vector queries, fuse via reciprocal rank fusion, deterministic rerank, diversity and token budgets. [pp.34–35,49,78; api:r2:c12:f6–f7; api:r2:c16:f8; api:r2:c25:f3.]
4. **ACL lifecycle:** deletion tombstones/removes eligible index entries; soft-deleted content is unretrievable. Source ACL revision invalidates tenant/user-scope/query/index caches before new results and before ordinary TTL; revocation effective before next retrieval. Filter before any model text, verify citations before display, and revalidate authorization/evidence at publication even when previously retrieved. [pp.27–29,31,35,51–53,59; api:r2:c10:f1,f8; api:r2:c11:f10; api:r2:c12:f8,f14; api:r2:c17:f6,f11; api:r2:c19:f16.]
5. **Generation/tool safety:** model registry checks deployment capability/region/class/context/cost/evaluation and workspace approval. Only approved equal-or-stronger fallback; outages never expose restricted data to unapproved region. Fixed system rules, signed workflow instruction, validated user input and delimited evidence remain distinct. Strip evidence tool directives/record injection indicators; pinned schema parsing bounded retries rejects unknown fields, invalid citations/control injection. Model text cannot authorize tools, scope changes or approvals; discovery is not invocation; denied action cannot substitute equivalent tool. [pp.7,37–42,61,87; api:r2:c3:f2–f4; api:r2:c13:f1–f11; api:r2:c14:f8–f12; api:r2:c20:f3; api:r2:c28:f12.]
6. **Policy/publication:** use maximum material classification `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` for routing/redaction/retention/approval. Normalize sensitivity/action/evidence quality/model class/financial category/confidence bands and retain rule version. High-impact recommendations become tasks. No unapproved high-risk publication; pointer/gate atomically bind exact supported artifact, current ACL and policy. Review expiry escalates/reassigns, never approves. Override requires elevated role/secondary reviewer/audited reason; denied rework new revision. [pp.11–12,44–46,62; api:r2:c5:f1,f8; api:r2:c15:f1–f11; api:r2:c20:f8.]
7. **Degradation/recovery:** admit generation only when token/queue-age/provider thresholds pass; `429 Retry-After` leaves saved cases available. Provider outage disables new generation but preserves manual/evidence workflows and visible degraded state; page on-call only if availability budget affected. Vector outage may use visibly reduced-quality lexical retrieval. Suspected ACL leak instead suspends affected aliases/revokes evidence/preserves audit/scoped replay until negative probes pass. Never weaken authorization/approval. Delayed indexing pauses only faulty connector/index shard and preserves records; diagnose event/outbox/parser/throttle/ACL, bounded validated replay, fingerprint/index/denied probes and incident audit/time/blast-radius/quality/prevention links. [pp.68–70,79,90; api:r2:c22:f1,f7–f11; api:r2:c25:f6–f7; api:r2:c31:f5–f10.]
8. **Lifecycle:** idempotent provisioning creates policy/key refs/roles/quotas/connector stubs, blocks sync if incomplete. Export/delete require independent checks; export excludes secrets/prompts, deletion respects holds/receipts and closed-case retention eligibility. No schedule or new provisioning/subject-request endpoint is supplied. [pp.26,78–80,89; api:r2:c9:f11; api:r2:c25:f1–f5,f9–f10; api:r2:c30:f13.]

### Deployment, performance and release conditions

Private datastores have no public IP; managed gateway terminates public TLS to private APIs. Restrict workers' NAT egress to declared model/repository endpoints and separate web/API/worker/data subnet flows. R1 writes primary with one warm recovery region, secondary restored under incident command; object/relational/index recipes tested together. API scaling uses utilization/latency, workers queue age/throughput; hosted GPU excluded. [pp.18–19; api:r2:c7:f1–f3,f8–f9.]

| Design target | Applicable condition / unresolved measurement |
|---|---|
| `99.9%` monthly public API availability | Measurement denominator/exclusions NC |
| Case-create P95 under `300 ms` | Defined load; p.12 says within 300 ms, equality boundary NC |
| Search P95 under `1.5 s` | Excludes remote connector fetch; model latency measured separately |
| `2,000` active daily users; `60` steady / `180` burst requests/s | Reference workload, not per-request throttle defaults |
| `100,000` indexed documents/tenant; `20` concurrent runs/large tenant | Reference capacity profile; exact admission configuration NC |
| Typical `1 MB` source approximately `40–120` chunks | Depends on content/parser quality, not upload/page limit |
| RPO `<=15 minutes`; RTO `<=4 hours` | Reference profile, combined object/relational/index recovery |

Sources: pp.12,65,68–70; api:r2:c5:f10; api:r2:c21:f5; api:r2:c22:f2–f3,f10–f11.

Release compatibility preserves active readers via expand/contract migrations, bounded backfill and old-replica drain. Use signed images/SBOM/allowed build identity, signed environment config and vault refs. Security/SRE checks egress/secrets/backups/alerts before promotion. Canary compares latency/errors/auth denials/AI safety against baseline; regression rolls traffic back, not assumed DB down-migration. Preserve reconstructible binary/prompt/policy/schema/model-route bindings and readability of new writes. Staging is synthetic/test-connectors; production data forbidden in development. Terraform/Bicep remains unselected. [pp.19–20,52,71–73; api:r2:c7:f11–f12; api:r2:c17:f8; api:r2:c23:f1–f10.]

## Errors and Acceptance Criteria

### Error contract — API-053

| Condition | Confirmed HTTP / business literal | Required behavior and caller action |
|---|---|---|
| Case revision mismatch | `409 CASE_VERSION_CONFLICT` | Current revision, no accepted mutation; error example nonretryable. Caller reload/merge UI/procedure NC; do not auto-retry stale patch. |
| Same idempotency key, changed fingerprint | `409 IDEMPOTENCY_CONFLICT` | No second outcome; caller must not retry changed body under same key; key recovery policy NC. |
| Schema-invalid request | `422`; business code NC | Reject before allocation/transaction; validation failures not retried. Safe details permitted. |
| Quota/admission throttling | `429`, `Retry-After`; business code NC | Controlled admission and bounded provider retries; saved cases available. |
| Foreign-tenant ID | `404`-equivalent non-disclosing error; literal NC | Same class as absent ID; safe principal/resource-class denial audit. |
| Insufficient supported evidence | `NO_SUPPORTED_EVIDENCE`; HTTP NC | No fabricated context; clarification or human routing permitted, deterministic branch NC. |
| Unknown fields/invalid citations/control injection in model output | `MODEL_OUTPUT_INVALID`; HTTP NC | No publication; bounded parsing retry only, exhaustion/recovery contract NC. |
| Revoked connector credentials | `CONNECTOR_REAUTH_REQUIRED`; HTTP NC | Queued jobs fail without secrets; reauthorization endpoint/caller procedure NC. |
| Stale approval hash | API-017 `409` conflict result; literal stale code NC | Reject/audit, unchanged business state; retrieve current candidate before new review, exact flow NC. |
| Unsafe/oversized/malformed files | Stable non-sensitive code required; literal/status NC | Fail closed; unsafe quarantine/no index; malformed bounded-retry ledger exception may continue batch. |
| Arbitrary/denied tool action | `DENY` before dispatch; HTTP NC | No equivalent-tool bypass; discovery does not grant permission. |
| Permanent permission/validation error | Exact per-API status/code NC | Not retried, preserve denial evidence safely. |
| Transient dependency unavailable | Documented retryable error or persisted asynchronous ID; exact mapping NC | Never ambiguous success; idempotent bounded retry or monitor known operation. |
| Missing approval/calls exhausted/invalid plan/policy denial/deadline | Failure checkpoint required; literal/status NC | Termination trigger timing and timeout recovery unresolved; pending review is not implicit failure/approval. |
| Legal hold during purge | Status/code NC | Protected records retained and receipted; never force purge. |

Sources: pp.13,23,25,27,36,38,41–42,49,54,69,83–84,89; api:r2:c5:f11; api:r2:c8:f11; api:r2:c9:f8; api:r2:c10:f6,f11; api:r2:c12:f9; api:r2:c13:f8; api:r2:c14:f11–f12; api:r2:c16:f10; api:r2:c18:f3–f5; api:r2:c22:f7; api:r2:c26:f13,f21–f22; api:r2:c30:f2–f6,f13–f15.

**Verbatim source example**, p.84 Appendix A.3 (api:r2:c26:f21); values are fictional placeholders, not defaults:

```http
HTTP/1.1 409 Conflict
Content-Type: application/json
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

| Example field | Demonstrated JSON type / meaning | Formal schema status |
|---|---|---|
| `error` | Object wrapper | Requiredness/variants NC |
| `code` | String, stable literal | Full enum/requiredness NC; preserve uppercase literals despite snake-case prose |
| `message` | String, safe explanation | Localization/requiredness NC |
| `correlation_id` | String, trace reference | Format/requiredness NC |
| `retryable` | Boolean; conflict example `false` | Universal requiredness/retry classification schema NC |
| `details` | Object; safe structured validation detail | Optional detail is permitted; full schema NC |
| `expected_revision`, `actual_revision` | Example integers `7`, `8` | Wire range/requiredness NC; actual expresses current conflict revision |

Do not place connector credentials, full prompts, retrieved documents or unauthorized resource existence in errors. Public success responses likewise exclude secrets/raw provider credentials. Diagnostic traces exclude user documents/API secrets; default model logs contain digests/token counts, not entire prompts. Denial audit does not change rejected business revision; event revision/order semantics require clarification. [pp.23,54,62,64,84; api:r2:c8:f9,f11; api:r2:c18:f2; api:r2:c20:f9; api:r2:c21:f1; api:r2:c26:f22.]

### Concrete acceptance matrix

Use synthetic authorized and negative fixtures; retain unknown schema/threshold decisions rather than letting tests choose them. Source TST identifiers are unchanged.

| ID / APIs and screen link | Procedure | Expected result |
|---|---|---|
| TST-001 / API-001, SF-006/SF-016 | Authorized valid create twice, same key/body | One case, identical response; `201` original creation contract |
| TST-002 / API-001 and job POSTs | Reuse prior key with changed body | `409 IDEMPOTENCY_CONFLICT`, no second accepted outcome |
| TST-003 / API-003, SF-003 | Read valid foreign-tenant case ID | `404`-equivalent, no private existence disclosure |
| TST-004 / API-008–010, SF-008 | Index source, revoke access, query again | No forbidden evidence on next query |
| TST-005 / API-036/011, SF-009 | Force model schema failure | `MODEL_OUTPUT_INVALID`, no publication |
| TST-006 / API-017, SF-010 | Approve wrong/prior artifact hash | Stale rejection, audited, no accepted stale mutation |
| TST-007 / API-046, SF-016 | Replay accepted outbox event | Exactly one accepted business transition |
| TST-008 / API-018/036, SF-009/SF-011 | Provider 429 burst | Capped retries, controlled admitted load; numeric cap NC |
| TST-009 / API-008/017/036 | Generate without citations | Needs review or unsupported, never fabricated approved answer; branch NC |
| TST-010 / API-016/017/046 | Expire configured review task | No implicit approval, escalation recorded; preserve EXPIRED catalog |
| TST-011 / API-002/003 consumer, SF-005 | Open case keyboard-only | No blocked action, visible focus |
| TST-012 / recovery dependency | Reference region recovery exercise | RPO ≤15 min/RTO ≤4 h; object/relational/index consistency |
| TST-013 / API-025/040 | Purge under legal hold | Protected records retained/receipted |
| TST-014 / API-047 | Arbitrary MCP tool attempt | `DENY` before dispatch |
| TST-015 / API-006 | Unsafe PDF | Quarantine, no indexing |
| TST-016 / API-043 release dependency | Canary regressed safety score | Promotion blocked |

Source p.89, api:r2:c30:f1–f16; numeric recovery p.69 api:r2:c22:f10.

Additional source-supported procedures:

1. Authorized independent Analyst/Reviewer executes create→ingest→retrieve→draft→review→publish. Verify exact artifact/source/model-prompt/policy reasons, current ACL/policy/hash and atomic pointer/gate. Test rejected rework new revision, poisoned quarantine and cross-tenant search denial. [pp.11–12,45,58,75; api:r2:c5:f1,f8; api:r2:c15:f8–f11; api:r2:c19:f9; api:r2:c24:f10.]
2. Click permitted verified citation: source opens with anchored page highlight. Revoke/delete source: no prohibited read/model/publication. Low-quality permitted source remains viewable but cannot support autonomous recommendation. [pp.31–32,51,57; api:r2:c11:f10–f11; api:r2:c17:f6; api:r2:c19:f7.]
3. Run refresh/reconnect reconstructs server stages with scoped retained monotonic backfill; pending Review state transitions enforce actor/hash/duties. Exact expired-offset and review-edge tests await confirmed contracts. [pp.55,58,82; api:r2:c18:f9; api:r2:c19:f8; api:r2:c26:f5.]
4. Connector capability gap warns lower trust; credential revocation returns safe reauth literal; malformed exhausted item quarantines with ledger exception and may continue remaining batch. Failed index write preserves accepted metadata, then fingerprint/outbox reconciliation restores readiness. [pp.27–29,49,78; api:r2:c10:f2,f6–f11; api:r2:c16:f8; api:r2:c25:f3.]
5. Generation outage retains manual/evidence, lexical continuation visibly reduced quality; suspected ACL leak contains affected aliases until denied probes pass. No safety waiver under load. [pp.68–70,79; api:r2:c22:f1,f7–f8; api:r2:c25:f6–f7.]
6. Every interface/component runs positive, foreign-tenant denial, duplicate/replay and evidence-retention tests. Accepted transition has one audit record; denied operations safe stable errors/tenant traces. Confirm private datastores, secret scopes, immutable audit, active-reader compatibility and reconstructible releases. [pp.8–80 chapter verification/registers; api:r2:c4:f7,f15; api:r2:c7:f17; api:r2:c17:f16; api:r2:c18:f13,f19; api:r2:c20:f16; api:r2:c23:f16.]

### Security and evaluation exit gates

Appendix D `T-01`–`T-12` verify foreign-token resource IDs; hostile PDF instructions; revised-artifact approval; polyglot PDF/zipped attacks; vault/trace/provider credential probes; unapproved regional fallback; **100** same-event replays; mid-search revocation; historical audit edit; recursive tool hints; single-Admin export; replaced evaluation fixtures. ZIP is attack input, not supported format; 100 is test count, not retry allowance. `SEC-001`–`SEC-012` are release-blocking, with security-control-owner independent negative reproduction/signature; no exact one-to-one T/SEC mapping is supplied. Critical isolation/approval tests allow zero exceptions and cannot be outweighed by model score. [pp.74,88; api:r2:c24:f1–f2; api:r2:c29:f1–f13.]

Evaluation uses `1,200` synthetic permission-controlled cases with expected citations/outcomes; citation precision `>=0.97`, unsupported-claim rate `<=0.02`, high-risk policy recall `1.00` on frozen safety suite. Report confidence intervals and domain distribution shift; low confidence blocks release; changed prompt/model requires reevaluation. Record randomized seeds, freeze/version/independently review corpora, pin provider adapters, test transactions/replay/revocation/delayed index/purge without relying on live models for deterministic tests. Signed outputs link release digest. Minimum pack includes unit/schema/negative-auth/replay/staging-sync/visual-accessibility/search-recall/grounding/policy-recall/load/recovery tests. [pp.74–76,89; api:r2:c24:f2,f6–f11; api:r2:c30:f17–f20.]

## Consistency and Open Questions

### Required source clarifications and earlier-specification links

| Open ID / affected API requirements | Evidence conflict or gap | Required amendment / dependency |
|---|---|---|
| API-OQ-001 / API-045 and all scopes | Persona/role/scope differences pp.11,22,83 | Resolve [01_screen_functions.md](01_screen_functions.md) SF-002/OQ-001: Workspace Admin/Admin, Owner, Member, approver, Operators; define action/resource/redaction/independence predicates. No inferred role grants. |
| API-OQ-002 / API-045 | BFF permitted, provider/algorithms/session not selected p.21 | Earlier SF-003/OQ-002; define identity/token/session and internal audiences without inventing Login screen. |
| API-OQ-003 / all wire interfaces | IDL absent, selected data/descriptive fields only pp.55,82–86 | Earlier SF-014/OQ-015: complete per-field request/response/type/required/default/status/error schemas; REST IDs not automatically UUID. Data Specification dependency. |
| API-OQ-004 / API-002/020 and other pagination | Cursor convention, only list query example pp.54,57,83 | Earlier OQ-007: cursor/order/page-size/expiry/filter/result/redaction schemas; MCP ten is not page size. |
| API-OQ-005 / API-011/012 | `POST /v1/runs` pp.15–17 versus case-scoped pp.12,40,83 | Earlier SF-009/OQ-015: retain both, decide distinct/alias relationship and typing, never silently replace. |
| API-OQ-006 / API-004 and workspace settings | Workspace config p.24 associated with case PATCH; mutable aggregates pp.24–25 versus immutable registers pp.13,17,26 | Earlier SF-006/SF-012/OQ-009/OQ-011: amend register distinction; define genuine workspace update contract. Do not send invented settings to case PATCH. Evidence api:r2:c9:f1–f3,f12; api:r2:c5:f12; api:r2:c6:f13. |
| API-OQ-007 / GET APIs and API-046 | Repeated GET/health/OpenAPI allocation/idempotency/event associations versus specific read responsibilities | Earlier OQ-015: clarify each operation's allocation and event mapping. Retain validation/non-ambiguous success, but do not authorize GET mutation or suppress chapter-only interfaces. Representative examples api:r2:c7:f5–f6,f14; api:r2:c18:f7,f16; api:r2:c26:f11. |
| API-OQ-008 / API-016/017/046 | Review catalog p.82 versus missing exact edges/wire/form enum | Earlier SCR-005/SF-010/OQ-012: preserve ASSIGNED/OPENED/APPROVED/REJECTED/EXPIRED and actor/hash/duties; define edges, required form fields, reason/annotation schema, SLA/escalation/override transport. api:r2:c26:f5; api:r2:c15:f7–f11; api:r2:c19:f9. |
| API-OQ-009 / API-011–017/036–037 | Missing-approval termination p.41, AWAITING_REVIEW p.49/82, expiry p.45; recoverable timeout p.12 versus FAILED p.82; AUTO_ALLOW p.44 versus linear review p.49 | Earlier OQ-008: define terminal trigger, SLA/run consequences, AUTO_ALLOW path, timeout literal and recovery. No implicit approval/cancel/publish endpoint. api:r2:c14:f11; api:r2:c16:f7; api:r2:c15:f3,f7; api:r2:c5:f10; api:r2:c26:f3. |
| API-OQ-010 / API-015/049 | SSE payload/retention/expired offsets and webhook signature/age/retry missing p.55 | Earlier SF-009/OQ-008/OQ-015: define generated schemas/auth/reconnect and recipient controls; do not map domain event names automatically. |
| API-OQ-011 / API-006–010/052 | 25 MB cap units/decompression/OCR/quality/anchor/URL geometry missing pp.30–32,52 | Earlier SF-007/SCR-003/OQ-010: exact values/formats/actor/remediation, preserving viewable low-quality versus unsafe quarantine and revoked/deleted prohibition. |
| API-OQ-012 / API-018–019/038/050 | Cursor/ledger schemas, retries, credential role/reauth and SyncRun derivative label pp.27–29; replay bounds pp.49–50 | Earlier OQ-013/OQ-015: define checkpoint/partial-success/quarantine/provider/recovery contracts; no invented whole-batch failure. |
| API-OQ-013 / API-053/046 | Snake-case prose versus uppercase literals p.54/84; denial checkpoint p.22 versus mandatory audit pp.23/87 | Earlier OQ-006/OQ-015: preserve exact codes; define error requiredness/status mapping/caller recovery and denial ordering/revision without suppressing audit. api:r2:c18:f3–f5; api:r2:c26:f21; api:r2:c8:f9,f11; api:r2:c28:f7. Exception Handling dependency. |
| API-OQ-014 / API-024–025/030/040 | Independent checks/hold control without workflow schema pp.78–83; single-Admin export p.88 | Earlier SF-017/OQ-016: define independent approver procedure, hold scope/receipt/download/partial completion. No new screens inferred. |
| API-OQ-015 / API-047–048 | A2A case_demo versus MCP UUID p.87, missing Citation/output/transport | Earlier SF-015/OQ-015: define adapter resolution, formal requiredness/min/defaults, protocol auth/error/deadline. Example deadline not schedule. |
| API-OQ-016 / performance/admission | Within versus under 300 ms pp.12/65; thresholds/bounds absent | Earlier OQ-017: confirm equality/load/measurement, quotas/token/retry/deadline values. Keep reference-load status. |
| API-OQ-017 / storage/retention/providers | Additional workspace tenancy p.86; encryption isolation/rotation p.10; dated selections p.90 | Earlier SF-003/OQ-018: select FK/procedure enforcement, key tradeoff, cloud region/search/identity/models/corporate retention/connector permissions. None selected. |
| API-OQ-018 / screen consumers | Eight primary screens p.57 versus representative aliases/title-selection mismatch pp.7,14,33,43,47,60,67,77,81 | Earlier SF-004/OQ-003/OQ-004: define launch/route/action placements without new Overview/Usage/evaluation/lifecycle screens. Screenshot counts/model/five citations not schemas/defaults. |
| API-OQ-019 / ancillary contracts | Holds/design/member/health/release/evaluation read schemas and operational mappings missing in respective chapters | Define each inventory contract, not exclusions based on Appendix A omissions. Complete caller identities/read modes/statuses and engineering lifecycle tests. |

### Selected data and later specifications

The later **Data Specification** must retain Appendix B selected entities and constraints: `tenants` unique slug; `workspaces` RLS tenant policy/quota; `cases` tenant uniqueness/revisioned state; append-only `case_revisions`; source-ACL `documents`; immutable `document_versions`; source-anchor `chunks`; bounded `runs`; idempotent `run_steps`; publish-validated `evidence_sets`; no-self-approval `approval_tasks`; immutable `approval_decisions`; append-only `audit_events`; transactional `outbox_events`; durable `connector_cursors`; attributed `token_ledger`; reproducible `policy_evaluations`; auditable `deletion_receipts`. Complete types/relationships/nullability/retention and production workspace tenancy remain **To be defined in a later stage**, not approved by abbreviated DDL. [pp.85–86; api:r2:c27:f1–f11.]

The later **Exception Handling Specification** must consolidate API-053 per-operation mappings, safe envelope schemas, permanent/transient classifications, retry/circuit-breaker bounds, missing-key/header behavior, quota terminal consequences, SSE offset errors, stale-decision recovery, poison partial-success, hold receipts and denial event ordering. Neither later specification has been generated here; do not reference an invented filename or requirement identifier.

### Example-only configuration and implementation lock

Appendix F p.90 examples remain examples: `release: r1.0`; `max_plan_depth: 8`, `max_tool_calls: 16`, `run_timeout_seconds: 180`, `replay_dedup_hours: 24`; `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `embed_dimension: 1536`, `hybrid_rrf_k: 60`; `auto_publish_classification: INTERNAL`, `require_human_review_for: [HIGH_RISK, RESTRICTED]`, `self_approval_allowed: false`; `upload_limit_mb: 25`, `user_data_region: primary-approved-region`; `trace_sample_rate: 0.10`, `diagnostic_retention_days: 30`, `audit_retention_years: 7`. [api:r2:c31:f1–f4.]

Depth eight/sixteen calls, 1536 dimensions, actor/fingerprint 24 hours, configurable file 25 MB and substantive retention/self-approval rules have independent chapter support in their stated scopes. Example-only timeout 180, candidates 80, selected chunks ten, RRF 60, sampling 0.10 and auto-publish INTERNAL are not decisions. MCP `max_items<=10` does not confirm global selection/page size ten. Reference database defaults likewise do not approve browser defaults.

Before implementation lock, record dated choices for supported region, exact search/identity provider, approved model deployments, corporate retention and connector permissions; encryption-key isolation/rotation tradeoff must be resolved before enterprise general availability. No owner, date, selected provider or approval is invented. Stage 8 must consolidate open items in `08_architecture_decision.md`, linking `02_api.md` API/API-OQ identifiers and [01_screen_functions.md](01_screen_functions.md) SCR/SF/OQ dependencies without rewriting the earlier file. This specification remains provisional pending separate root approval. [pp.10,90; api:r2:c4:f13; api:r2:c31:f11–f12.]
