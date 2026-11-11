# 2. API Specification

## API Inventory and Responsibilities

### API-001 — Scope, authority and traceability

**Confirmed.** This specification describes the APIs of OrionDesk AI, `OD-AI-DDS-001`, `R1.0`, design revision `1.3`, a controlled fictional reference architecture. All citations below refer to **1794353355-OrionDesk_AI_Detailed_Design_Specification.pdf**, using original pages and supplied finding IDs. The root has reconciled the supplied chapter outcomes; it does not claim a new inspection of unavailable attachments. The candidate remains provisional pending evidence review.

The source states: **“All numbers are design assumptions, not measured production performance.”** Figures illustrate normative boundaries, not generated implementation artifacts. Fictional identities, UI values, grants, times and configuration examples are not production defaults or evidence of approval. **Confirmed** identifies reference-system requirements; **Needs confirmation** identifies incomplete contracts or unresolved choices; **Proposal** would identify a suggested design. No new design proposal is selected here. `API-*` identifiers in this file are specification-assigned, not source namespace mappings. [Source: pp.1–2,8; `api:r1:c1:f1`, `api:r1:c1:f2`, `api:r1:c2:f1`, `api:r1:c2:f2`, `api:r1:c5:f1`]

The API scope includes enterprise document ingestion, permission-aware retrieval, grounded drafting, deterministic policy, human review, publication, audit and controlled operations. Physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing and agent cloud-administration permissions are **Out of scope**. Application-hosted GPU inference is excluded. Cross-region active/active mutation, OCR beyond English and customer-managed model weights are deferred. [Source: pp.7,9–10,19; `api:r1:c4:f1`, `api:r1:c7:f1`, `api:r1:c8:f5`, `api:r1:c25:f2`]

References to [01_screen_functions.md](01_screen_functions.md) preserve `SCR-001`–`SCR-008` and `SF-*`. They are activity associations, not browser routes or a complete caller permission matrix. No endpoint establishes an additional screen. Screen/figure aliases remain unresolved under `SF-005` and `SF-020 OQ-001`.

### API-002 — Shared authentication and authorization

Every request binds an authenticated principal and tenant. Authorization combines role, tenant, workspace membership, resource attributes, case sensitivity, originating document ACL, action and separation of duties. Apply it at edge, domain transaction, retrieval, tool dispatch and publication as applicable. Navigation hiding is not authorization. Baseline roles are `Analyst`, `Reviewer`, `Admin`, `Auditor`, `Service`; Appendix A's `Owner`, `Member` and `approver` scopes require mapping. `Workspace Admin` is not silently equated with `Admin`. [Source: pp.11,21–23,41,83; `api:r1:c12:f1`, `api:r1:c29:f1`, `api:r1:c31:f1`, `api:r1:c31:f5`, `api:r1:c67:f1`, `api:r1:c137:f8`, `api:r1:c137:f15`]

| Profile | Confirmed requirements | Needs confirmation |
|---|---|---|
| Public REST | OIDC authorization-code flow with PKCE; tokens carry issuer, audience, expiry, subject, tenant; reject unexpected algorithms and missing tenancy claims | Header syntax, exact claim keys/algorithms/audiences, token lifetimes, session/refresh/revocation/login/logout contracts |
| Browser storage | No long-lived refresh tokens in local storage | Session implementation |
| Optional BFF | Secure `HttpOnly`, `SameSite` cookies may be issued | Selection, cookie name/value, CSRF and session contracts |
| Internal HTTP/RPC | Scoped identities; mTLS-authenticated HTTP or gRPC; generated/versioned contracts and independent authorization; audience/scoped IAM checks; do not share identities between deployment units | Protocol per interface, claims/grants and audience values |
| Provider calls | Controlled egress; only scoped model context/structured prompts, never raw connector tokens or unrestricted database access | Selected providers/endpoints/regions |
| MCP/A2A | Separate invoking-principal/workspace-policy/tool-scope/data-classification authorization; discovery never grants capability permission | Grant resolution and transport |

[Source: pp.15–18,21,54,87; `api:r1:c18:f1`, `api:r1:c20:f1`, `api:r1:c24:f4`, `api:r1:c30:f1`, `api:r1:c30:f5`, `api:r1:c89:f1`, `api:r1:c139:f13`]

The orchestrator has **no direct database credentials** and uses narrowly scoped APIs. Datastores are private; public TLS terminates at the gateway forwarding to private API workloads. [Source: pp.9,18; `api:r1:c8:f1`, `api:r1:c24:f1`]

### API-003–API-017 — Reference REST operations

All rows inherit API-002. Scopes are necessary conditions, not sufficient authorization. `202` means accepted asynchronous work, not `READY`, `PUBLISHED`, finished evaluation, downloadable export or completed purge. `200` reads are ordinary synchronous reference results; dependency-failure alternatives remain unresolved in API-043.

| API ID | Method and exact path | Purpose / success content | Activity caller association | Scope | Behavior / result | Source |
|---|---|---|---|---|---|---|
| API-003 | POST `/v1/cases` | Create idempotent case | SCR-001/SCR-002; SF-007 | Analyst | Synchronous creation; `201`; classification asynchronous | p.83 A.2; `api:r1:c137:f6` |
| API-004 | GET `/v1/cases/{caseId}` | Authorized current case revision | SCR-002; SF-007 | Analyst / Reviewer | Synchronous `200` | p.83; `api:r1:c137:f7` |
| API-005 | PATCH `/v1/cases/{caseId}` | Revision-controlled mutation | SCR-002; SF-007 | Owner, mapping open | `200 / 409`; `If-Match` | p.83; `api:r1:c137:f8` |
| API-006 | POST `/v1/cases/{caseId}/attachments` | Create ingestion operation | SCR-003 and case attachment activity; SF-008 | Analyst | Asynchronous ingestion; `202` | p.83; `api:r1:c137:f9` |
| API-007 | POST `/v1/cases/{caseId}/runs` | Start bounded AI workflow | SCR-004; SF-009 | Analyst | Asynchronous workflow; `202` | p.83; `api:r1:c137:f10` |
| API-008 | GET `/v1/runs/{runId}` | Stages and evidence metadata | SCR-004; SF-009 | Analyst / Reviewer | Synchronous `200` | p.83; `api:r1:c137:f11` |
| API-009 | GET `/v1/streams/runs/{runId}` | Authorized resumed run events | SCR-004; SF-009 | Analyst / Reviewer | Long-lived SSE; `200`; `Last-Event-ID` | p.83; `api:r1:c137:f12` |
| API-010 | POST `/v1/approvals/{approvalId}/decision` | Bind decision to reviewed hash | SCR-005; SF-010 | Reviewer | `200 / 409`; not publication | p.83; `api:r1:c137:f13` |
| API-011 | POST `/v1/connectors/{connectorId}/sync` | Incremental source sync | SCR-006; SF-011 | Admin | Asynchronous; `202` | p.83; `api:r1:c137:f14` |
| API-012 | POST `/v1/search` | ACL-filtered lexical/semantic evidence | SCR-003; SF-008 | Member, mapping open | Synchronous `200` | p.83; `api:r1:c137:f15` |
| API-013 | GET `/v1/audit/events` | Immutable cursor log | SCR-008; SF-013 | Auditor | Synchronous `200` | p.83; `api:r1:c137:f16` |
| API-014 | GET `/v1/usage` | Costs, quotas, trend estimates | Unmapped usage activity; SF-014 | Admin | Synchronous `200` | p.83; `api:r1:c137:f17` |
| API-015 | POST `/v1/evaluations` | Frozen benchmark start | Unmapped evaluation activity; SF-014 | Admin | Asynchronous; `202` | p.83; `api:r1:c137:f18` |
| API-016 | POST `/v1/workspaces/{workspaceId}/export` | Controlled manifest export | Unmapped controlled exit; SF-013 | Admin + approver | Asynchronous; `202`; independent checks/two-person export | p.83; `api:r1:c137:f19` |
| API-017 | POST `/v1/workspaces/{workspaceId}/delete` | Legal-hold-safe deletion | Unmapped controlled exit; SF-013 | Admin + approver | Asynchronous; `202`; independent checks | p.83; `api:r1:c137:f20` |

### API-018–API-042 — Additional interfaces

**Confirmed existence; incomplete contracts.** Except API-019's confirmed query name and the exact paths below, successful statuses, response schemas, endpoint-specific permission mappings and ordinary execution timing are **Needs confirmation**. Purpose descriptions distinguish literal interface evidence from associated activity. Public rows inherit public authentication; internal rows inherit independently authorized internal authentication. Governance exposure and precise callers remain open.

`O+I` means the source register requires **OAuth audience + idempotency policy**, not a confirmed header on every GET. `S+B` means **Schema contract / bounded errors**, not a supplied complete schema. Each row also has the conditional preallocation validation/dependency rule in API-043.

| API ID | Method/path | Responsibility / caller association | Register invariant | Original source |
|---|---|---|---|---|
| API-018 | GET `/v1/me` | Principal/identity context; screen mapping open | O+I | p.23 §5.4; `api:r1:c33:f6` |
| API-019 | GET `/v1/cases?cursor=...` | Case list; SCR-001/SF-007 | O+I | p.59 §16.4; `api:r1:c99:f2` |
| API-020 | PUT `/v1/workspaces/{workspaceId}/members` | Membership boundary; caller/update semantics open | S+B | p.23; `api:r1:c33:f7` |
| API-021 | GET `/v1/cases/{caseId}/evidence` | Case evidence; SCR-003/SF-008 | S+B | p.59; `api:r1:c99:f3` |
| API-022 | GET `/v1/evidence/{evidenceId}` | Evidence lookup; SCR-003/SF-008 | S+B | p.36 §9.4; `api:r1:c57:f3` |
| API-023 | GET `/v1/documents/{documentId}/status` | Ingestion status; SCR-003/SF-008 | S+B | p.32 §8.4; `api:r1:c51:f3` |
| API-024 | GET `/v1/runs/{runId}/steps` | Run steps/checkpoints; SCR-004/SF-009 | S+B | p.42 §11.4; `api:r1:c69:f7` |
| API-025 | GET `/v1/review-queue` | Review queue; SCR-005/SF-010 | S+B | p.46 §12.4; `api:r1:c75:f7` |
| API-026 | POST `/v1/cases/{caseId}/close` | Closure; SCR-002/SF-007 | S+B | p.26 §6.4; `api:r1:c39:f7` |
| API-027 | GET `/v1/connectors/{connectorId}/runs` | Sync history; SCR-006/SF-011 | S+B | p.29 §7.4; `api:r1:c45:f7` |
| API-028 | GET `/v1/model-catalog` | Approved-model catalog; caller/screen open | S+B | p.39 §10.4; `api:r1:c63:f3` |
| API-029 | POST `/v1/security/holds` | Hold-related interface; subject/lifecycle/caller open | S+B | p.63 §17.4; `api:r1:c105:f3` |
| API-030 | GET `/v1/evaluations/{evaluationId}` | Evaluation lookup; unmapped activity | S+B | p.76 §21.4; `api:r1:c129:f3` |
| API-031 | GET `/v1/system/degraded-modes` | Degraded-mode interface; operational caller open | O+I | p.70 §19.4; `api:r1:c117:f6` |
| API-032 | GET `/v1/openapi.json` | REST contract interface; caller open | O+I | p.56 §15.4; `api:r1:c93:f6` |
| API-033 | GET `/v1/health/live` | Operational liveness reference; actual probe criteria open | O+I | p.20 §4.4; `api:r1:c27:f2` |
| API-034 | GET `/v1/health/ready` | Operational readiness reference; criteria open | S+B | p.20; `api:r1:c27:f3` |
| API-035 | POST `/v1/design-decisions` | Baseline decision/change governance | O+I | p.10 §1.4; `api:r1:c9:f2` |
| API-036 | GET `/v1/design-baselines/{id}` | Baseline interface; `id` referent open | S+B | p.10; `api:r1:c9:f3` |
| API-037 | POST `/internal/model/generate` | Controlled model generation; orchestrator/model tier | O+I | p.39; `api:r1:c63:f2` |
| API-038 | GET `/internal/workflows/{runId}` | Durable workflow lookup; internal caller open | O+I | p.50 §13.4; `api:r1:c81:f2` |
| API-039 | POST `/internal/deadletters/{id}/replay` | Operator-controlled replay; no browser screen | S+B | p.50; `api:r1:c81:f3` |
| API-040 | GET `/internal/storage/documents/{id}` | Internal document storage access; document/version referent open | O+I | p.53 §14.4; `api:r1:c87:f6` |
| API-041 | POST `/internal/storage/purge` | Internal retention purge, distinct from workspace delete | S+B | p.53; `api:r1:c87:f7` |
| API-042a | GET `/internal/metrics` | Internal telemetry | S+B | p.66 §18.4; `api:r1:c111:f3` |
| API-042b | GET `/internal/capacity` | Internal capacity | S+B | p.70; `api:r1:c117:f7` |
| API-042c | POST `/internal/releases` | Release initiation/governance | O+I | p.73 §20.4; `api:r1:c123:f6` |
| API-042d | GET `/internal/releases/{releaseId}` | Release lookup | S+B | p.73; `api:r1:c123:f7` |
| API-042e | POST `/v1/runs` | General run-start reference; SCR-004 association provisional | O+I | pp.15,17; `api:r1:c17:f4`, `api:r1:c21:f2` |

**Needs confirmation beside API-007/API-042e:** the source supplies both run-start paths but no alias, deprecation, body equivalence, scope equivalence or chosen browser path. Preserve [01_screen_functions.md](01_screen_functions.md) `SF-020 OQ-003`.

Primary chapter operations not marked above also have O+I requirements: case creation, case PATCH, attachment, case-scoped run start, decision, connector sync, search, audit, usage, evaluation and export. Secondary run read and SSE require S+B. These invariants supplement A.2, not override its statuses/scopes. [Source: pp.13,17,26,29,32,36,42,46,56,63,66,76,80; `api:r1:c15:f2`, `api:r1:c21:f3`, `api:r1:c39:f6`, `api:r1:c45:f6`, `api:r1:c51:f2`, `api:r1:c57:f2`, `api:r1:c69:f6`, `api:r1:c75:f6`, `api:r1:c93:f7`, `api:r1:c105:f2`, `api:r1:c111:f2`, `api:r1:c129:f2`, `api:r1:c135:f6`]

## Interfaces by API

### API-043 — Shared interface completeness and REST semantics

**Confirmed.** Public REST uses `/v1` resource nouns, cursor pagination and RFC3339 timestamps. External OpenAPI and internal protobuf are generated from repository-controlled IDL and govern their respective clients/messages. Internal HTTP/RPC is versioned/generated/independently authorized. CI prevents breaking field deletion and incompatible enum changes. Nonbreaking evolution is additive; removal requires a scheduled migration. No actual repository, migration date, enum extension policy or REST unknown-field rule is supplied. Model-output unknown-field rejection must not be applied universally to REST requests without confirmation. [Source: pp.15,54–56,82; `api:r1:c18:f5`, `api:r1:c89:f1`, `api:r1:c90:f1`, `api:r1:c92:f1`, `api:r1:c137:f1`]

For **every API row**, all interface attributes not explicitly supplied are **Needs confirmation**, including absent query/header/body names, media types, exact field encodings, lengths, requiredness, defaults, validation timing, successful response keys/types/requiredness, error fields and examples. Do not manufacture an empty body, multipart field, `Authorization` syntax, `ETag`, `Location`, page-size parameter or job key. No complete success JSON example is supplied. Additional examples would be **Proposal**, not approved contract; none is selected here.

All named interfaces require input validation before any long-running allocation. On dependency unavailability the source repeatedly permits **a documented retryable error OR a persisted asynchronous job identifier, never ambiguous success**. The condition does not prove ordinary GET mutation/job creation. The branch-selection, allocation, persistence owner, status, job schema and lookup/recovery rules remain open alongside all affected operations. A.2's explicit ordinary `200/201/202` results remain confirmed. [Representative source: pp.9,16,30,54–56,64–65; `api:r1:c6:f9`, `api:r1:c18:f7`, `api:r1:c48:f2`, `api:r1:c90:f4`, `api:r1:c90:f8`, `api:r1:c108:f8`]

### API-044 — Parameter definitions

| Name / location | Affected APIs | Meaning / type evidence | Required status / constraints / default |
|---|---|---|---|
| `caseId` / path | API-004–007,021,026 | Selected case; wire type **Needs confirmation** | Path substitution necessary to address listed resource; format/default/validation response open |
| `runId` / path | API-008–009,024,038 | Selected run; wire type open | Constraints/default open; do not infer UUIDv7 wire type from aggregate register |
| `approvalId` / path | API-010 | Approval/task resource; referent details/type open | Constraints/default open |
| `connectorId` / path | API-011,027 | Connector reference; type open | Constraints/default open |
| `workspaceId` / path | API-016–017,020 | Workspace reference; type open | Tenant membership mandatory; schema/default open |
| `documentId` / path | API-023 | Document reference; type open | Format/default open |
| `evidenceId` / path | API-022 | Evidence resource; type open | Format/default open |
| `evaluationId` / path | API-030 | Evaluation reference; type open | Format/default open |
| `releaseId` / path | API-042d | Release reference; type open | Format/default open |
| `id` / path | API-036,039,040 | Baseline/dead-letter/storage referents respectively; not interchangeable | Meaning/type/constraints/default open |
| `cursor` / query | API-019 | Confirmed pagination query name | Encoding/type/first-page omission/default/page size/order open |
| `If-Match` / header | API-005; general case concurrency | Submitted revision precondition | Submission required by case mutation contract; syntax/type/missing-header result open; no default |
| `Idempotency-Key` / header | POST mutations creating long-running jobs | Retry outcome identity | Required under that condition; key type/format/scope/window/missing-key result open; not universal GET header |
| `Last-Event-ID` / header | API-009 reconnect | Resume retained caller-scoped offsets | Reconnect use confirmed; initial-request requirement/type/expired-ID behavior open |
| `trace_id`, `correlation_id` / request context | Every request, telemetry | Distinct named context; transport/type open | Presence confirmed; not necessarily user-editable body/header values; defaults/format open |
| `Content-Type: application/json` / response header | A.3 conflict example | Demonstrated JSON error media type | Confirmed example, not a universal upload/success encoding |

[Source: pp.25,54–55,64,83–84; `api:r1:c37:f4`, `api:r1:c90:f5`, `api:r1:c91:f1`, `api:r1:c108:f1`, `api:r1:c137:f7`, `api:r1:c137:f8`, `api:r1:c137:f12`, `api:r1:c137:f21`; additional placeholder provenance is in API inventory rows]

Public APIs paginate by cursor, and audit specifically returns an immutable cursor log. Cursor query naming beyond API-019, next-cursor response name, limits/order/snapshot behavior and empty/expired cursor responses are **Needs confirmation**. No five-row mockup is a page limit.

### API-045 — Successful content and body contracts by operation group

Conceptual fields below are supported content, **not literal JSON property definitions**. For each, wire type, encoding, required property spelling, nullability and defaults remain open unless explicitly stated.

| APIs | Confirmed request/processing concepts | Confirmed successful response content | Open wire decisions |
|---|---|---|---|
| API-003–005,019 | Case title, description, priority, sensitivity, status, owner, current approved result, monotonic revision; attachment/business context on creation; impact/urgency determine priority | Case identifier after valid creation; authorized current revision on read; accepted revised mutation | Which fields callers submit/edit, creation requiredness, PATCH format, list fields, revision key and header representation |
| API-006,023 | File admission/ingestion under API-049 | Ingestion operation, not READY; status resource exists | Upload encoding/file field, operation ID, status schema/lookup linkage |
| API-007–009,024,038,042e | Bounded plan/run and checkpoints | Run read stages/evidence metadata; scoped SSE progress | Run request body/ID response, step/report fields, route relationship, failed-checkpoint property |
| API-010,025 | Decision bound to reviewed artifact; decision/actor/time/hash/rationale/optional annotations recorded | Accepted decision, not publication; queue interface exists | Decision values, caller fields vs server metadata, hash encoding, required review fields, queue schema |
| API-011,027 | Incremental sync with durable cursor/high-watermark/error ledger | Accepted sync operation; history interface exists | Provider/capability/cursor/history schema, ID/status linkage |
| API-012,021,022 | Permission-aware evidence retrieval | Each evidence item includes chunk ID, source title, document revision, page anchor, ACL digest; citation IDs opaque/verified | Query body, evidence field names/types, Citation/EvidenceSet schemas, permitted source-access interface |
| API-013 | Authorized audit scope | Immutable, redacted cursor log; decision metadata/template digests/access events | Filters/page keys/audit row schema/hash proof |
| API-014,042a–b | Workspace cost-center/deployment attribution and golden/AI metrics | Costs, quotas, trends; daily budget/forecast/rejected-excess rollups | Currency/token/cost units, formulas, dimensions/windows/filtering and report schemas |
| API-015,030 | Frozen benchmark evaluation | Start acceptance; lookup exists | Corpus selection/body, progress/report/confidence fields |
| API-016–017,029,041 | Controlled export/hold-safe purge | Manifest-based accepted export/delete; completion receipts required by processing | Approval binding, manifest/checksum/download/status, hold subject/lifecycle, partial completion/receipt schema |
| API-018,020,028,031–036,040,042c–d | Identity/membership/catalog/degraded/contract/health/governance/storage/release responsibilities named in inventory | No complete success content supplied | All request/response fields, ordinary status and operational caller scopes |
| API-037 | Approved model routing, signed/delimited prompt, structured schema and token budgets | Validated model output subject to policy; no complete output schema | Model/prompt/citation fields, schema version and invocation result encoding |
| API-039 | Reason, dry run, scope bound; preserved event identity | No complete replay response supplied | Reason/dry-run/scope input names/types, validation result and migration provenance |

[Source: pp.12,24–26,28–29,35,37–39,45,50,62,64–66,75,79–80,83; `api:r1:c13:f1`, `api:r1:c36:f5`, `api:r1:c38:f1`, `api:r1:c43:f1`, `api:r1:c56:f1`, `api:r1:c60:f1`, `api:r1:c73:f4`, `api:r1:c80:f5`, `api:r1:c12:f6`, `api:r1:c108:f6`, `api:r1:c110:f1`, `api:r1:c127:f1`, `api:r1:c134:f1`, `api:r1:c134:f5`, `api:r1:c137:f6`–`api:r1:c137:f20`]

### API-046 — MCP and A2A interfaces

**Confirmed tool contract**, not a public REST endpoint or search pagination limit:

| Field | Direction | Type | Meaning / constraint | Required / default |
|---|---|---|---|---|
| `query` | Input | `string` | Grounded search query | Needs confirmation; length/blank rules open |
| `case_id` | Input | `uuid` | Case handoff context | Requiredness/wire encoding open |
| `max_items` | Input | `int<=10` | Upper bound10 for this tool | Minimum/default/requiredness open |
| `evidence_set_id` | Output | `uuid` | Evidence-set reference | Requiredness/encoding open |
| `citations` | Output | `Citation[]` | Cited evidence | Requiredness and Citation schema open |

`knowledge.search@v1` requires `read:permitted_documents`, tenant-scoped. It is read-only with **no arbitrary URLs or filesystem access**. Approved MCP schemas are version-pinned and arguments validated. Tool transport/method/path/status/error envelope remains **Needs confirmation**. [Source: pp.41,87 C.2; `api:r1:c67:f1`, `api:r1:c139:f10`, `api:r1:c139:f11`, `api:r1:c139:f12`]

A2A carries task ID, capability reference, declared input/output schema, deadline and trace context. Receiver may decline. Registration/discovery does not authorize invocation. The source's **illustrative example**, not a proposed or complete normative schema, is:

```json
{"task_id":"019ac000-0000-7000-8000-000000000042","tenant_id":"tenant_example_01","capability":"research.grounded_search.v1","input_schema":"schema://oriondesk/research-request/1","deadline_at":"2026-11-09T08:00:00Z","trace_id":"trace_example_01","authorization_ref":"grant_readonly_14","payload":{"case_id":"case_demo","query":"..."}}
```

**Needs confirmation:** requiredness/types/schema contents/output schema, grant lifetime/verification, transport, decline and deadline handling, and `case_demo` handoff to typed MCP UUID. The omission of `output_schema` and placeholder case does not establish an exception. [Source: pp.41,87; `api:r1:c67:f5`, `api:r1:c139:f9`, `api:r1:c139:f13`, `api:r1:c139:f14`]

### API-047 — SSE and optional webhook contracts

1. API-009 authorizes principal/tenant/resource scope before stream and replay.
2. Emit monotonically increasing offsets for long-running run updates.
3. On reconnect, use `Last-Event-ID` to backfill **retained caller-scoped events**, never private data outside caller scope.
4. Refresh reconstructs progress from server state; announce meaningful transitions only and never portray partial work as approval.

**Needs confirmation:** event framing/schema, media type/header details, heartbeat/connection timeouts, retention duration, expired-history recovery, current-connection permission revocation and final-state reconstruction fields. [Source: pp.55,58,83; `api:r1:c91:f1`, `api:r1:c97:f1`, `api:r1:c137:f12`]

Outbound webhooks are **optional, unselected**. If used, sign them, retry with exponential backoff, require recipient signature/event-age verification and do not roll back committed case transitions on delivery failure. No subscription CRUD/callback method/path is confirmed. Payload/signature algorithm/key/transport, acceptable age, retries/dedup and terminal recovery remain open. [Source: pp.52,55–56; `api:r1:c85:f1`, `api:r1:c91:f5`, `api:r1:c93:f5`]

## Processing and Consistency

### API-048 — Validation, transactions, tenancy and retry safety

1. Validate request payload **before transaction entry**, then domain invariants, then tool dispatch; validate before allocating long-running work. Browser validation is convenience, not security.
2. Set authenticated tenant/resource context for each domain transaction; re-evaluate attributes inside the transaction and apply RLS.
3. Reject stale/unauthorized writes before relevant business event publication; leave business state unchanged. Denial audits and duplicate ledger outcomes are not accepted business mutations.
4. Commit the stated case mutation/approval decision/outbox ACID boundary as applicable. The source does not establish that every case mutation simultaneously approves another record. Search indexing/webhooks are asynchronous with reconciliation.
5. Accepted state transitions require **one audit record**, tenant-scoped traces and stable denial codes. Events are observable through correlated logs/audit without document text in diagnostic telemetry.
6. Every cross-service write is retry-safe. At-least-once consumers check event identity/operation key, ledger and aggregate revision, record duplicate outcome and do not reapply mutation. Detect stale/delayed revisions without relying on cross-partition ordering.
7. Transient faults use bounded exponential backoff, randomized jitter and per-dependency breakers; **validation/permission failures are permanent and never retried**.

[Source: pp.15–17,22,48–56; `api:r1:c17:f2`, `api:r1:c20:f6`, `api:r1:c31:f5`, `api:r1:c78:f5`, `api:r1:c80:f1`, `api:r1:c85:f1`, `api:r1:c92:f4`, `api:r1:c94:f1`, `api:r1:c94:f3`]

**Confirmed additional database safeguards:** reset scoped connection-pool session variables **after every transaction**. The reference policy uses `current_setting('app.tenant_id')::UUID`; production additionally enforces workspace-tenancy membership through foreign keys **or controlled write procedures**, still unselected. Independently referenced tenant/workspace foreign keys do not implement that membership invariant alone. [Source: p.86 B.2; `api:r1:c138:f14`, `api:r1:c138:f18`, `api:r1:c138:f19`, `api:r1:c138:f20`]

Actual durable-changing boundary records carry `tenant_id`, `revision`, `actor_id`, `occurred_at` and a correlation ID **“wherever the operation changes durable state.”** General principal/tenant context applies everywhere, but this fuller record condition does not imply all GETs write or prescribe body fields. Types, placement and aliases remain open. [Source: pp.24–25,48–49,54–59; `api:r1:c36:f2`, `api:r1:c78:f2`, `api:r1:c90:f3`, `api:r1:c96:f2`]

Persistence is not a public schema. PostgreSQL owns mutable metadata; encrypted source/normalized objects preserve versions; search is a nonauthoritative derivative; cache is versioned/ephemeral. Reference DDL `revision BIGINT DEFAULT 1`, `sensitivity TEXT DEFAULT 'INTERNAL'`, UUID keys and timestamp defaults do not establish request defaults or automatic timestamp-update triggers. [Source: pp.16,51,85–86; `api:r1:c19:f5`, `api:r1:c84:f1`, `api:r1:c138:f4`, `api:r1:c138:f16`, `api:r1:c138:f17`]

### API-049 — Case creation, mutation, close and ingestion

**Case procedure:**
1. Validate/authorize Analyst creation, apply idempotency and create `NEW` with `201`/case identifier.
2. Asynchronously classify, retaining labels/confidences/provenance; user corrections require a reason code, with correction endpoint/catalog open.
3. Read only authorized current revision. PATCH uses `If-Match`; conflict returns `409 CASE_VERSION_CONFLICT` and current revision without business mutation.
4. An actor/request-fingerprint idempotency key maps one outcome for **24 hours**; identical same-key creation has one case/identical response; changed body returns `409 IDEMPOTENCY_CONFLICT`. Long-running-job POSTs transport `Idempotency-Key`; broader scope/fingerprint/expiry mechanics remain open.
5. Apply guarded lifecycle: `NEW→TRIAGED→IN_PROGRESS`; `IN_PROGRESS→PENDING_APPROVAL or RESOLVED`; `PENDING_APPROVAL→RESOLVED or IN_PROGRESS`; `CLOSED` is final **unless explicitly reopened as a new revision**.
6. Close snapshots approved answer, cited document versions and reviewer decisions as immutable approved-output lineage. Retention applies only to eligible closed cases, with legal holds.

Priority uses explicit impact/urgency, never model alone. Workspace business calendars/timezone set deadlines; predicted breach cannot change them. **Needs confirmation:** closing edge/actor, reopen endpoint/status, transition predicates, impact/urgency formula and schemas. [Source: pp.12,24–26,83–84,89; `api:r1:c13:f1`, `api:r1:c37:f1`, `api:r1:c37:f4`, `api:r1:c37:f5`, `api:r1:c38:f1`, `api:r1:c38:f2`, `api:r1:c38:f6`, `api:r1:c38:f7`, `api:r1:c137:f8`, `api:r1:c141:f1`, `api:r1:c141:f2`]

**Attachment procedure:**
1. Admit only R1 `PDF`, `DOCX`, `HTML`, `UTF-8 text`; MIME signature/extension agree; configurable **25 MB per file** and decompression-bomb threshold apply.
2. Scan before parse, disable macros, do not fetch embedded remote references. Unsafe files quarantine without indexing.
3. Preserve page/block bboxes, table rows/columns, headings/reading order; optional OCR is opt-in/provenance-marked, with OCR beyond English deferred.
4. Normalize transport artifacts without rewriting source claims. Content fingerprint/pipeline version yields immutable derivative IDs; new derivatives may coexist side by side.
5. Preserve chunk source URI, file hash, page and **optional** bbox; generation citations require resolvable stored anchor and current permission.
6. Record quality flags for empty-page ratio, unknown-character ratio, table-loss and language confidence. Low quality remains viewable, but excluded from autonomous recommendations.

Document catalog: `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED`, guarded by scan/quality. `202` ingestion is not READY. **Needs confirmation:** exact transitions/thresholds/media types/MB convention, quarantine recovery and source/anchor schema. [Source: pp.30–32,82–83; `api:r1:c48:f1`, `api:r1:c48:f4`, `api:r1:c49:f1`, `api:r1:c49:f2`, `api:r1:c49:f6`, `api:r1:c50:f1`, `api:r1:c50:f5`, `api:r1:c137:f4`, `api:r1:c137:f9`]

### API-050 — Connector synchronization and retrieval

**Synchronization:**
1. Block sync if provisioning incomplete; show incomplete state.
2. Advertise list/fetch/delta cursor/ACL/delete. Unsupported capability yields lower-trust mode and explicit visible warning, never ACL bypass.
3. Store workspace vault credential references. Revoked queued jobs fail `CONNECTOR_REAUTH_REQUIRED` without tokens; running-job behavior remains open.
4. Persist provider cursor/high-watermark/error ledger. Advance only after durable preceding outcomes; retry partial batches safely.
5. Honor `Retry-After`, exponential backoff/jitter, workspace quotas and fair scheduling. After bounded retries, malformed item quarantine includes reason/correlation/remediation; recorded ledger exception **permits** remaining batch continuation.
6. Source deletion tombstones/schedules index removal. Source ACL changes invalidate affected caches before new results; revoked access applies **before next retrieval**, not after cleanup.
7. Backfill bounded windows/stable source IDs/per-batch receipts; readiness uses index coverage, not queue emptiness.

[Source: pp.27–29,78; `api:r1:c42:f1`, `api:r1:c42:f5`, `api:r1:c43:f1`, `api:r1:c43:f4`, `api:r1:c44:f1`, `api:r1:c44:f5`, `api:r1:c132:f1`, `api:r1:c132:f5`]

**Retrieval:** ACL filtering precedes generation text release; relevance never grants access. Form lexical/normalized vector queries, bound candidates, RRF merge, deterministic rerank, diversify documents/sources and cap model-context tokens. Internal search rows retain tenant/workspace/version/chunk/language/classification, normalized text and **1536-dimensional embeddings**. Parallel rebuilds atomically switch read alias only after completeness/recall checks; database remains authoritative. Cache keys include tenant, user-scope digest, source ACL revision, query hash and index generation. Permission change purges affected cache before TTL and next-query access remains mandatory. Insufficient quality/confidence returns `NO_SUPPORTED_EVIDENCE`, never fabricated context; clarification versus human route is unresolved. [Source: pp.34–36,53; `api:r1:c53:f2`, `api:r1:c54:f1`, `api:r1:c54:f5`, `api:r1:c55:f1`, `api:r1:c55:f4`, `api:r1:c56:f5`, `api:r1:c86:f7`]

Source opening is authorized, encrypted and via access-controlled short-lived signed URLs with opaque public names. URL expiry/revocation/page/bbox contracts remain open. Authorized evidence interfaces do not permit documents in errors/diagnostic telemetry. [Source: pp.52,57,84; `api:r1:c86:f1`, `api:r1:c86:f2`, `api:r1:c96:f6`, `api:r1:c137:f22`]

### API-051 — Run, model and tool processing

1. Create accepted bounded run immediately, not a completed/approved answer. Persist plan revision **before side effects**; DAG depth **8**, maximum tool calls **16**, explicit dependencies/replayable checkpoints.
2. Checkpoint each stage before downstream dispatch. Run catalog: `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED`; guard is workflow checkpoint/runtime budget.
3. Triage classifies, Research obtains evidence, Draft assembles candidate; Policy Evaluator is deterministic.
4. Approve specific deployments by capability/region/handling class/context/cost/evaluation, not provider brand. Fallback only to approved equal-or-stronger handling/approved region/deployment.
5. Reserve input/output tokens; account provider usage/workspace quota. Exhaustion is terminal for current run without automatic model/data-class switch.
6. Construct fixed system rules/signed workflow/validated user input/delimited untrusted passages. Strip evidence tool directives and record injection indicators; content never becomes instruction authority.
7. Request versioned JSON and bounded parse retries. Unknown fields, invalid citations or control-character injection yield `MODEL_OUTPUT_INVALID`, no publish.
8. Dispatch only approved pinned MCP schemas/validated arguments. External writes need separate capability; mutable calls idempotency; consequential calls human authorization. Discovery never grants permission; equivalent tools cannot replace denied action.
9. Terminate on missing approval, call-budget exhaustion, repeated invalid plans, policy denial or deadline; expose exact failed checkpoint.

**Needs confirmation beside steps2/9:** ordinary `AWAITING_REVIEW` versus missing-approval termination; recoverable timeout versus `FAILED`; exact deadlines/retry counts/recovery/cancellation/resume and state mapping. Do not select an inferred distinction. [Source: pp.12,37–42,49,82,89; `api:r1:c14:f2`, `api:r1:c60:f1`, `api:r1:c60:f5`, `api:r1:c61:f1`, `api:r1:c61:f5`, `api:r1:c62:f1`, `api:r1:c62:f5`, `api:r1:c66:f1`, `api:r1:c66:f5`, `api:r1:c68:f1`, `api:r1:c68:f5`, `api:r1:c79:f1`, `api:r1:c137:f3`, `api:r1:c141:f5`]

### API-052 — Review and distinct publication gate

Policy normalizes/stores sensitivity, requested action, evidence quality, model class, financial-impact category and confidence bands with rule-set version. Outcomes are `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY`; model tags cannot override. High-impact recommendations become review tasks, not autonomous mutations. [Source: pp.44–45; `api:r1:c72:f1`, `api:r1:c72:f5`]

1. Assign eligible policy pool/minimum-role/separation reviewers. Own-high-risk self-approval prohibited; B also says unqualified “no self approval.” Broader scope remains unresolved; lower-risk permission is not granted.
2. Expose exact artifact, citations, model/prompt version and policy reasons; source inspection must be available before approval. Required review field completion gates Approve/Reject in UI, not server permission.
3. Submit reviewed-hash decision; record decision, actor/time/hash/rationale/optional notes. Changed/wrong hash or unauthorized decision rejects stale/denied, leaves business state unchanged and records denial audit.
4. Review catalog is `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED`, guarded by actor/hash/separation. Configured-SLA expiry reassigns/escalates without approval; escalation recorded under TST-010. Branch conditions/SLA remain open.
5. Denied rework creates **new run revisions**, never retroactive approval. Override requires elevated role, secondary reviewer, audited reason; no hash/ACL bypass is established.
6. **Publication is separate:** required evidence and satisfied versioned deterministic policy are prerequisites; high-risk unapproved cannot publish. Validate decision event, reviewed artifact identity and current tenant/document authorization. Reject stale evidence after intervening permission changes.
7. Atomically commit final response pointer and satisfied gate. Replay cannot publish another artifact under old approval.

Publication/override endpoint/invoker, detailed decision fields/options, eligibility/self-approval/secondary-independence rules, error recovery remain **Needs confirmation**. [Source: pp.11–12,45–46,58–59,82–85,87,89; `api:r1:c12:f5`, `api:r1:c13:f5`, `api:r1:c73:f1`, `api:r1:c73:f4`, `api:r1:c73:f8`, `api:r1:c74:f1`, `api:r1:c74:f5`, `api:r1:c97:f5`, `api:r1:c100:f2`, `api:r1:c137:f5`, `api:r1:c138:f9`, `api:r1:c139:f5`, `api:r1:c141:f6`, `api:r1:c141:f10`]

### API-053 — Event contracts and cross-operation causality

Every event includes the following fields, uses UTC and canonical JSON. Inclusion is confirmed; types/encodings/defaults/canonicalization algorithm are **Needs confirmation** except event-specific typed declarations elsewhere.

| Required envelope fields | Scope |
|---|---|
| `event_id`, `type`, `schema_version` | Event identity/type/version |
| `tenant_id`, `aggregate_id`, `aggregate_revision` | Tenant and aggregate/revision scope |
| `occurred_at`, `trace_id`, `payload` | Time, trace and versioned payload |

Do not equate `revision` to `aggregate_revision`, boundary correlation ID to `trace_id`, provider trace to application correlation, or event envelope to SSE framing. [Source: pp.16,48; `api:r1:c20:f2`, `api:r1:c78:f1`]

| Event | Confirmed producer | Selected payload content, not JSON keys | Confirmed consumer action |
|---|---|---|---|
| `CaseCreated` | Case Service | Case ID / revision | Run classifier |
| `DocumentNormalized` | Ingestion | Version ID / source hash | Build index |
| `SearchIndexCommitted` | Indexer | Index generation / document revision | Invalidate query cache |
| `AgentPlanApproved` | Orchestrator | Run ID / plan hash | Dispatch plan steps, still authorized |
| `ApprovalDecisionRecorded` | Policy Service | Task / actor / content hash | **Validate publication**, not publish automatically |
| `WorkflowStageAdvanced` | Orchestrator | Run / stage / checkpoint | Resume consumers |
| `AccessDenied` | Policy Service | Principal / action / policy digest | Alert enrichment |
| `TenantDeletionVerified` | Retention Worker | Manifest ID / receipt hash | Close purge record; tenant/workspace scope open |

[Source: p.87 C.1; `api:r1:c139:f1`, `api:r1:c139:f2`, `api:r1:c139:f3`, `api:r1:c139:f4`, `api:r1:c139:f5`, `api:r1:c139:f6`, `api:r1:c139:f7`, `api:r1:c139:f8`]

All published register events require **versioned envelope/outbox**, correlated audit/log visibility, stale/unauthorized-write rejection and ledger/revision duplicate controls. Additional exact events are:

| Event | Register source | Open semantics |
|---|---|---|
| `BaselineCommitted` | p.10; `api:r1:c9:f4` | Governance trigger/payload |
| `RunRequested` | p.17; `api:r1:c21:f4` | Which run path/producer/payload |
| `DeploymentPromoted` | p.20; `api:r1:c27:f4` | Distinct from ReleasePromoted |
| `CaseStateChanged` | p.26; `api:r1:c39:f8` | Distinct from logical `CaseStatusEvent` |
| `ConnectorSyncStarted` | p.29; `api:r1:c45:f8` | Start not completion; history GET emission not established |
| `ModelInvocationCompleted` | p.39; `api:r1:c63:f4` | Provider-complete versus validated-output semantics |
| `DataRetentionPurgeCommitted` | p.53; `api:r1:c87:f8` | Distinct from TenantDeletionVerified |
| `ApiCompatibilityVerified` | p.56; `api:r1:c93:f8` | Contract-test trigger/payload |
| `UserReviewOpened` | p.59; `api:r1:c99:f4` | Exact opening trigger/payload |
| `SecurityPolicyChanged` | p.63; `api:r1:c105:f4` | Policy/hold endpoint causality not established |
| `SloBurnRateDetected` | p.66; `api:r1:c111:f4` | Threshold/window/action |
| `BackpressureActivated` | p.70; `api:r1:c117:f8` | Admission trigger/action |
| `ReleasePromoted` | p.73; `api:r1:c123:f8` | Release gate trigger, not product approval |
| `EvaluationCompleted` | p.76; `api:r1:c129:f4` | Completion/report payload |

Repeated diagram labels and adjoining API paragraphs are not independent proof of event emission. In particular run requests do not thereby emit `CaseCreated`, GETs do not thereby start jobs, export does not thereby emit deletion, and a plan/decision event cannot confer publication authority.

### API-054 — Controlled exit, operations and recovery

Export/delete both require **two independent approval checks**; export explicitly requires **two-person approval plus manifest**, and a single Admin fails. Export includes case metadata, approved artifacts, source references and checksum audit manifests; exclude secrets/internal prompts. Deletion applies holds/tombstones/blob/index removal/completion receipts. Held protected records are retained and receipted. Data-subject requests use the same inventory, not a newly invented endpoint. Manifest/receipt/checksum/approval/download/status and partial-failure schemas remain open. [Source: pp.78–80,83,88–89; `api:r1:c131:f1`, `api:r1:c134:f1`, `api:r1:c134:f5`, `api:r1:c137:f19`, `api:r1:c137:f20`, `api:r1:c140:f11`, `api:r1:c141:f13`]

Audit is append-only/batch-hash chained and independently retained; operators may query, not alter historical decisions. Maximum included data class controls model routing/redaction/retention/approval. Likely PII tagging/policy-permitted nonessential redaction/default token/digest logs do not waive secrecy or diagnostic content bans. Vault identity/rotation avoids bulk request-path reencryption. Diagnostic TTL **30-day default**, audit **seven-year fictional policy**, receipts/holds apply; corporate retention remains unselected. [Source: pp.62–63,66,90; `api:r1:c103:f1`, `api:r1:c103:f5`, `api:r1:c104:f1`, `api:r1:c104:f6`, `api:r1:c110:f5`, `api:r1:c142:f13`]

Failed indexing does **not** roll back accepted source metadata. Reconcile fingerprints/retry and repair broken links from outbox. Replay requires operator reason/dry-run/scope limit; original event identity remains except schema-transforming migration with explicit provenance linkage. [Source: pp.49–50; `api:r1:c79:f5`, `api:r1:c80:f5`]

Delayed-indexing runbook:
1. Detect queue oldest age/index backlog; identify tenant/index generation.
2. Pause **only** faulty connector/indexer shard; preserve accepted records.
3. Diagnose event ID/outbox lag/parser flags/search throttling/ACL revision.
4. Replay validated outbox records with bounded operator-controlled job.
5. Compare source fingerprints/index versions and run denied-access probes before incident closure.
6. Link audit IDs/time window/blast radius/quality effect/preventative action.

ACL leakage separately suspends affected aliases/cache and preserves audit; search restoration requires negative access tests. Bounds/operators/probe results/recovery interfaces remain open. [Source: pp.79,90 F.1; `api:r1:c133:f5`, `api:r1:c142:f7`, `api:r1:c142:f8`, `api:r1:c142:f9`, `api:r1:c142:f10`, `api:r1:c142:f11`, `api:r1:c142:f12`]

### API-055 — Admission, objectives and release behavior

New-run admission depends on workspace tokens, queue age and provider capacity thresholds; throttled callers receive **429 plus Retry-After**, while saved cases remain available. Generation outage disables new generation admission but preserves manual editing/evidence. Vector degradation **may** use lexical retrieval with visible reduced-quality flag. Degradation/recovery never bypasses approval or authorization. [Source: pp.68–70,79; `api:r1:c113:f2`, `api:r1:c115:f1`, `api:r1:c115:f5`, `api:r1:c133:f1`]

| Value | Confirmed reference scope / qualification |
|---|---|
| API availability99.9% monthly | Target, not observed result |
| Case-create P95 within300ms / under300ms | Both source formulations retained; equality/load/measurement unresolved |
| Search P95 under1.5s | Excludes remote connector fetch; model latency separate |
|2000 active daily users;60steady/180burst rps | Reference workload, not selected admission limits |
|100000 indexed documents/tenant maximum;20concurrent runs/large tenant | Reference envelope; not automatically enforceable quota values |
| Typical1MB → approx40–120chunks | Content/parser-dependent sizing, not upload/parser requirement |
| RPO≤15min;RTO≤4h | Reference recovery targets; primary/warm-region incident-command restoration |
|1200 benchmark cases;precision≥.97;unsupported≤.02;high-risk recall1.00 | Frozen synthetic-suite targets; domain confidence/shift reporting, not achieved results |

[Source: pp.12,19,65,68–70,75; `api:r1:c14:f1`, `api:r1:c25:f6`, `api:r1:c109:f1`, `api:r1:c114:f1`, `api:r1:c114:f6`, `api:r1:c116:f1`, `api:r1:c127:f1`, `api:r1:c127:f4`]

Preserve F configuration **examples**: `release:r1.0`; `max_plan_depth:8`, `max_tool_calls:16`, `run_timeout_seconds:180`, `replay_dedup_hours:24`; `max_candidate_chunks:80`, `max_selected_chunks:10`, `embed_dimension:1536`, `hybrid_rrf_k:60`; `auto_publish_classification:INTERNAL`, `require_human_review_for:[HIGH_RISK, RESTRICTED]`, `self_approval_allowed:false`; `upload_limit_mb:25`, `user_data_region:primary-approved-region`; `trace_sample_rate:0.10`, `diagnostic_retention_days:30`, `audit_retention_years:7`. Independent chapter evidence confirms scoped8/16/1536/configurable25MB and retention qualifications. Example180s/replay24h/80/10/RRF60/.10 are not universal timeout, SSE history, pagination or quota. INTERNAL is not unrestricted publication permission; placeholder region is not selected. [Source: p.90; `api:r1:c142:f1`–`api:r1:c142:f6`]

Governance records changes/impact scores and minor/major revision effects; revised invariants require negative tests. Release tooling uses reproducible artifacts, source nonsecret defaults, signed environment values, vault references, scans/tests/SBOM/signed images and allowed build identity. Terraform/Bicep remains alternative. Compatible migrations precede canary; old replicas drain before enforcement; rollback plans disclose new-write readability. Regression triggers traffic rollback, **not database down-migration**. Security/SRE verify egress/secrets/backups/alerts before promotion. Release records bind image/schema/prompt/model-routing policy, and versions must be reconstructible. Gate thresholds/signatures/interfaces remain open. [Source: pp.8–10,71–73; `api:r1:c6:f6`, `api:r1:c5:f2`, `api:r1:c120:f1`, `api:r1:c120:f5`, `api:r1:c121:f1`, `api:r1:c121:f5`, `api:r1:c122:f1`, `api:r1:c122:f4`, `api:r1:c124:f4`]

## Errors and Acceptance Criteria

### API-056 — Failure contract and caller behavior

| Condition | Confirmed HTTP/business outcome | Confirmed caller/processing rule | Needs confirmation |
|---|---|---|---|
| Case revision conflict | `409 CASE_VERSION_CONFLICT`, current revision | No business mutation; example `retryable:false` | Revision/header schema, refresh/merge/retry flow |
| Changed-body same-key case reuse | `409 IDEMPOTENCY_CONFLICT` | No second business case/outcome | Key expiry/fingerprint/recovery |
| Schema-invalid REST request | `422` | Validate server-side before transaction/allocation | Literal code/details/correction contract |
| Quota/new-run throttling | `429`, admission `Retry-After` | Preserve saved cases; controlled load | Header value/time/retry limits |
| Foreign-tenant case/resource substitution | Absent-ID not-found class; case `404-equivalent non-disclosing` | Never reveal private existence; audit principal/resource class | Universal exact status/body/code |
| Model schema/unknown field/citation/control injection | `MODEL_OUTPUT_INVALID`; no publish | Bounded parsing retries only; output confers no authority | HTTP/run-state/rework mapping |
| Insufficient evidence | `NO_SUPPORTED_EVIDENCE` | Never fabricate context | Error vs result; clarification/human route |
| Missing citations | Needs review **or** unsupported | Neither universal alternative selected | Durable state/caller selection |
| Wrong/stale artifact decision | Stale rejection/audit; decision reference `200 / 409` | No business mutation/no transferred approval | Specific code/body/recovery |
| Expired review | No implicit approval; escalation recorded | Reassign/escalate per unresolved conditions | SLA/recipient/status/body |
| Revoked queued connector credentials | `CONNECTOR_REAUTH_REQUIRED`, no tokens | Fail queued job | HTTP/retryability/reauth/running jobs |
| Arbitrary MCP tool | `DENY before dispatch` | No equivalent-tool workaround | Tool transport/error body |
| Unsafe upload | Quarantine/no indexing | Scan/sandbox/bounded parse | HTTP/code/remediation |
| Dependency unavailable | Retryable error **or** persisted async ID | Never ambiguous success | Branch/status/job schema/readback |
| Stale evidence at publication | Reject after reauthorization | Earlier search/approval insufficient | Endpoint/code/body/recovery |
| Held purge | Protected records retained/receipted | No deletion bypass | Partial-completion/receipt contract |

[Source: pp.23,25,27,36,38,45,54,69,83–84,89; `api:r1:c32:f6`, `api:r1:c37:f4`, `api:r1:c42:f5`, `api:r1:c56:f5`, `api:r1:c61:f5`, `api:r1:c73:f4`, `api:r1:c90:f2`, `api:r1:c115:f1`, `api:r1:c137:f21`, `api:r1:c141:f2`–`api:r1:c141:f15`]

Permanent validation/permission failures do not automatically retry. Transient/dependency retry rules are bounded but counts/timeouts remain open; caller UX/recovery is not permission to retry stale decisions or alter model/data class automatically.

**Source reference error example**, exact values preserved; identifier/revisions are placeholders, not validation limits or mandatory universal detail fields:

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

Demonstrated types: `error/details` objects; `code/message/correlation_id` strings; `retryable` boolean; revision integers. Production requiredness/additional fields remain open. Error details may be safe structured validation data; **never connector credentials, full prompts, retrieved documents or unauthorized existence**. Public fields never expose secrets/raw provider credentials; diagnostics exclude documents/API secrets. Preserve uppercase codes despite unresolved “stable snake-case” convention. [Source: pp.54,64,82–84; `api:r1:c89:f2`, `api:r1:c90:f6`, `api:r1:c108:f1`, `api:r1:c137:f1`, `api:r1:c137:f21`, `api:r1:c137:f22`]

### API-057 — Concrete verification obligations

Tests below are required, **not reported passed**. They preserve preceding `SF-019 AC-*` associations without inventing namespace equivalence.

| Source test | Action / expected result | Relevant API / screen activity |
|---|---|---|
| TST-001 / AC-001 | Same-key case twice → one case/identical response | API-003; SCR-001/002 |
| TST-002 / AC-002 | Changed body/key →409 IDEMPOTENCY_CONFLICT | API-003 |
| TST-003 / T-01 / AC-003 | Valid foreign-tenant ID/token → non-disclosing404-equivalent; domain/RLS denial | Resource APIs |
| TST-004 / T-08 / AC-004 | Revoke indexed ACL → next query excludes; additionally revoke **during search** | API-012/021/022 |
| TST-005 / AC-005 | Forced schema invalid model → MODEL_OUTPUT_INVALID/no publish | API-037/run |
| TST-006 / T-03 / AC-006 | Prior/wrong hash approval after revision → stale rejection/audit | API-010 |
| TST-007 / T-07 / AC-007 | Replay outbox; same event **100 times** → exactly one accepted business transition | Event consumers |
| TST-008 / AC-008 | Provider429 burst → capped retries/controlled admission; saved cases remain available | Run/model admission |
| TST-009 / AC-009 | Missing citations → review OR unsupported, selection unresolved | Generation |
| TST-010 / AC-010 | Expire review → no approval/escalation recorded | Review |
| TST-011 / AC-011 | Keyboard-only case open → no blocked action/visible focus | SCR-002 consumer |
| TST-012 / AC-012 | Recovery exercise → stated RPO/RTO with safety | Recovery |
| TST-013 / AC-013 | Held tenant purge → protected records retained/receipted | API-017/041 |
| TST-014 / AC-014 | Arbitrary MCP → DENY before dispatch | API-046 |
| TST-015 / T-04 / AC-015 | Unsafe PDF/polyglot/zipped hostile input → scan/sandbox/bounded parse/quarantine/no index | API-006; zipped test is not supported format |
| TST-016 / AC-016 | Safety-regressed canary → blocked promotion | Release gates |

[Source: pp.88–89; `api:r1:c140:f1`, `api:r1:c140:f3`, `api:r1:c140:f4`, `api:r1:c140:f7`, `api:r1:c140:f8`, `api:r1:c141:f1`–`api:r1:c141:f16`]

Additional required negative tests: hostile PDF instructions with evidence delimiting/pinned tools (`T-02`); credential observation in traces/provider requests (`T-05`); regional outage/approved fallback (`T-06`); historical audit edit/hash-chain protection (`T-09`); recursive tool hints/budgets (`T-10`); single Admin export denial/two-person manifest (`T-11`); replaced score fixtures/versioned signed dataset (`T-12`). [Source: p.88; `api:r1:c140:f2`, `api:r1:c140:f5`, `api:r1:c140:f6`, `api:r1:c140:f9`, `api:r1:c140:f10`, `api:r1:c140:f11`, `api:r1:c140:f12`]

Also verify:
- Authoritative revision/nonmutation guards, exactly one audit record per accepted transition, duplicate outcome without business reapplication and delayed-event safety.
- Current source ACL before generation/next retrieval and publication reauthorization after permission changes; source inspection/exact review display/required-field UI gating; refresh and scoped SSE replay.
- Unsafe-versus-low-quality distinction, durable accepted metadata after failed indexing, queued credential revoke, incomplete provisioning block and index-coverage readiness.
- No public datastores; private tenancy predicates/pool reset/workspace integrity; no secrets in public responses/model/tool undeclared scopes or document diagnostic telemetry.
- Full create→ingest→retrieve→draft→review→publish journey, rejected rework, poisoned quarantine, foreign search denial.
- Provider429 storms, lost worker heartbeats, duplicate events, object access failure and primary-region outage, measuring safety **and** recovery time.

[Source: pp.20,32,50–56,58–59,63,70,75,78; `api:r1:c28:f4`, `api:r1:c50:f5`, `api:r1:c82:f4`, `api:r1:c88:f4`, `api:r1:c94:f4`, `api:r1:c97:f1`, `api:r1:c97:f5`, `api:r1:c100:f2`, `api:r1:c106:f4`, `api:r1:c116:f5`, `api:r1:c128:f1`, `api:r1:c132:f1`]

Critical isolation/approval tests permit **zero exceptions**. `SEC-001`–`SEC-012` are release-blocking; a security-control owner independently reviews/reproduces negative evidence and signs release record. No mapping to `T-01`–`T-12` is supplied. Unmitigated critical isolation/approval bypass blocks promotion regardless of benchmarks. Low statistical confidence also blocks release; independent prompt/model roll-forward requires reevaluation. [Source: pp.74–76,88; `api:r1:c125:f2`, `api:r1:c128:f6`, `api:r1:c140:f13`, `api:r1:c140:f14`]

Fixtures are synthetic and cover successful/empty/mixed-permission/adversarial/malformed inputs; randomized tests record seeds; evaluation corpus is frozen/versioned/independently leakage-reviewed. Pipeline minimum: unit, schema evolution, negative authorization, workflow replay, staging connector sync, visual accessibility, search recall, grounding, policy recall, load and disaster recovery. Outputs are signed/release-digest linked; signature/report/statistical contracts remain open. [Source: p.89 E.1–E.2; `api:r1:c141:f17`, `api:r1:c141:f18`, `api:r1:c141:f19`, `api:r1:c141:f20`]

## Consistency and Open Questions

### API-058 — Source conflicts and required prior-stage amendments

Do not rewrite earlier files or interpret a TBD as discretion to choose. Carry the following with links to this file's identifiers and [01_screen_functions.md](01_screen_functions.md).

| Open decision | Affected requirements / earlier links | Evidence and required resolution |
|---|---|---|
| API-G02a Run route | API-007/042e/051; SF-009/016, OQ-003 | General POST `/v1/runs` pp.15/17 (`api:r1:c17:f4`) versus case POST p.83 (`api:r1:c137:f10`). Define relationship/body/scope/browser use; no alias inferred |
| API-G02b Lifecycle | API-051/052; OQ-004 | Missing approval terminates p.41 (`api:r1:c68:f1`) versus AWAITING_REVIEW pp.49/82 (`api:r1:c79:f1`, `api:r1:c137:f3`); recoverable timeout p.12 (`api:r1:c14:f2`) versus FAILED catalog. Define conditions/states/recovery |
| API-G05 Case immutability | API-048/049; OQ-005 | Case/CaseService/CaseAggregate Immutable derivative rows pp.13/17/26 (`api:r1:c15:f6`, `api:r1:c21:f6`, `api:r1:c39:f3`) versus mutable monotonic aggregate p.24/history p.85 (`api:r1:c36:f5`, `api:r1:c138:f4`). Identify immutable subject/amend registers; no invented split |
| API-G05 Review immutability | API-052; OQ-007 | ApprovalTask/ReviewForm Immutable derivative pp.46/59 (`api:r1:c75:f3`, `api:r1:c99:f6`) versus assignment/expiry/input pp.45/58 (`api:r1:c73:f1`, `api:r1:c97:f5`). Define subjects/fields |
| API-G05 Other register subjects | API-018–042,048–054; OQ-016 | APIReplicaSet p.20 (`api:r1:c27:f6`), TenantMembership p.23 (`api:r1:c33:f3`), SyncRun p.29 (`api:r1:c45:f3`), ExtractionJob p.32 (`api:r1:c51:f6`), IndexAlias p.36 (`api:r1:c57:f6`), ErrorEnvelope p.56 (`api:r1:c93:f3`), CacheEntry p.53 (`api:r1:c87:f5`), ProvisioningJob p.80 (`api:r1:c135:f3`). Retain exact classifications/hash/ledger invariants; define subjects and mutation/revision semantics |
| API-G04 Self-approval/roles | API-002/052; OQ-006 | Own-high-risk prohibition p.11 (`api:r1:c12:f5`) versus no-self-approval p.85 (`api:r1:c138:f9`); F false example p.90 (`api:r1:c142:f4`). No lower-risk grant; resolve broader scope/override and all role mappings |
| API-G03 GET/async selection | API-043/044; OQ-008 | Generic clauses versus A.2 ordinary200 reads/SSE (`api:r1:c18:f7`, `api:r1:c137:f11`, `api:r1:c137:f12`). Define allocation/ownership/error-job branch and schemas; not universal jobs |
| API-G15 Error naming | API-056; OQ-009 | Snake-case p.54 (`api:r1:c90:f1`) versus explicit uppercase p.38/84/89 (`api:r1:c61:f5`, `api:r1:c137:f21`, `api:r1:c141:f2`). Preserve literals/clarify convention |
| API-G17 Latency boundary | API-055; OQ-015 | Within300ms p.12 (`api:r1:c14:f1`) versus under300ms p.65 (`api:r1:c109:f1`). Define equality/load/accounting/test method |
| API-G10 A2A handoff | API-046; OQ-018 | Full input/output requirement p.41 (`api:r1:c67:f5`) versus case_demo/absent output schema example and typed UUID p.87 (`api:r1:c139:f9`, `api:r1:c139:f10`, `api:r1:c139:f14`). No typed exception |
| API-G13 Exit scope | API-053/054; OQ-012/017 | Workspace export/delete versus TenantDeletionVerified/receipt tenant IDs p.83/85/87 (`api:r1:c137:f20`, `api:r1:c138:f13`, `api:r1:c139:f8`). Define aggregate scope/holds/receipts/independent approvals; no tenant-workspace equivalence |
| API-G22 Prior additions | API-044/053; SF-007/016/017 | Add **CaseStateChanged**, **ConnectorSyncStarted** to earlier event inventory from pp.26/29 (`api:r1:c39:f8`, `api:r1:c45:f8`); clarify **Idempotency-Key** for long-running-job POSTs from p.54 (`api:r1:c90:f5`). Transport uncertainty otherwise remains |

The Document Map child's execution-title comparison is internally garbled and establishes no coherent contrary source label. Do not create a source amendment from it. Other repeated figure title/selected-sidebar mismatches remain as already recorded in `SF-005`; no majority-based aliasing or API routing choice is authorized. [Source: pp.2,7,14,33,43,47,60,67,77,81; `api:r1:c2:f5`, `api:r1:c4:f6`, `api:r1:c16:f5`, `api:r1:c52:f4`, `api:r1:c70:f5`, `api:r1:c76:f4`, `api:r1:c100:f4`, `api:r1:c112:f4`, `api:r1:c130:f5`, `api:r1:c136:f5`]

### API-059 — Remaining contract decisions and later-stage dependencies

| Gap group | Required definition beside affected APIs | Carry-forward destination |
|---|---|---|
| API-G01/04 | Complete IDL/media types/fields/defaults/requiredness/examples, caller/owner/role/audience/session/grants and policy-setting interfaces | Data and security/interface contracts **To be defined in a later stage** |
| API-G06/07/14 | Revisions/fingerprints/24h applicability/transactions, canonical envelope/correlation, cursor/order/page sizes, SSE lifetime/history/permissions, event triggers/payloads, optional webhook signing/age/retries | Later Data and Exception Handling Specifications |
| API-G08/09/10 | MIME/MB/parser/scan/OCR/quality/Citation/URL schemas; capability/cursor/quarantine/reauth/bounds/readiness; ranking/model/prompt/token/unsupported-outcome rules | Later Data, integration and Exception Handling Specifications; SF-020 OQ-010/013/018 |
| API-G11/12/13 | Close/reopen/priority/calendar, review fields/pools/SLA/override/publication, independent exit approvals/manifests/holds/status/partial receipts | Later Data, workflow/security and Exception Handling; OQ-011/012/017 |
| API-G15/16/17 | Full error taxonomy/caller recovery, retention/redaction/hash/encryption/key/cost/metric rules, objective measurement/admission/retry/recovery thresholds | Later Exception Handling, Data and architecture; OQ-009/015/017 |
| API-G18/19 | Governance/release/canary/readability/signature/reconstruction schemas, executable fixtures/statistical domain/confidence/equivalence/mappings and evidence formats | Later verification/architecture; OQ-019/021 |
| API-G20 | Dated supported-region/exact-search/identity/approved-model/corporate-retention/connector-permission selections **before implementation lock**; key isolation versus rotation throughput **before enterprise GA** | Future architecture decision consolidation; OQ-020 |

[Source: pp.10,71–76,88–90; `api:r1:c8:f6`, `api:r1:c120:f1`, `api:r1:c121:f5`, `api:r1:c127:f4`, `api:r1:c128:f6`, `api:r1:c140:f13`, `api:r1:c141:f20`, `api:r1:c142:f13`]

All source-supported invariants and explicit exceptions remain binding while these contracts are incomplete. No owner, deadline, approval, provider, corporate policy, BFF, webhook or infrastructure alternative is selected. Stage8 will consolidate TBDs from completed Markdown files into `08_architecture_decision.md`, linking this file's `API-*`/`API-G*` and the earlier `SF-*` identifiers. That later specification is not generated here.
