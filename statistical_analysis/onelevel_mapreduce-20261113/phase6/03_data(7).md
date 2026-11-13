# 3. Data Specification

## Data Inventory and Relationships

### Baseline and interpretation

`03_data.md` specifies OrionDesk AI, document `OD-AI-DDS-001`, release `R1.0`, design revision `1.3`. **Confirmed** means confirmed requirements of the fictional reference design, not a deployed system. The source states: “All numbers are design assumptions, not measured production performance.” [Source: `1794325316-OrionDesk_AI_Detailed_Design_Specification.pdf`, pp.1–2; data:r1:c1:f1–f4, data:r1:c2:f1.]

All source citations below refer to that exact filename and original PDF pages. DAT identifiers are assigned here for traceability. Earlier identifiers retain their meanings in [01_screen_functions.md](01_screen_functions.md) and [02_api.md](02_api.md). A related screen is a data consumer, not proof that every stored field is displayed or editable. API identifiers reference the exact methods and paths in `02_api.md`, not newly invented interfaces.

**Needs confirmation** marks a decision that the implementation AI must not silently make. No design proposals are approved. Appendix B is a selected-field catalog and abbreviated reference DDL, not a complete production schema. Figures describe component/contract boundaries, not generated artifacts or ER cardinalities. Table-of-contents pages 2–6 are navigation only. [pp.2–6, 85–86; data:r1:c2:f2–f9, data:r1:c27:f1,f20,f29.]

### DAT-001 Store authority, ownership and scope

| Store or artifact boundary | Confirmed purpose and authority | Responsible producer or contract owner | Open physical decisions |
|---|---|---|---|
| PostgreSQL | Reference authority for mutable metadata and case state; transactional case, decision and outbox writes | Case Service owns transactional mutations; domain teams own case/policy API contracts | Full schemas, database custodians, operational roles and additional indexes |
| Private encrypted blob/object storage | Sources, immutable versions, normalized text/layout/metadata and artifacts | Ingestion Service owns document conversion | Object container/key syntax, artifact formats, retention classes and custodians |
| Hybrid vector/keyword index | Nonauthoritative, eventually consistent searchable derivatives | Retrieval Service returns cited chunks; Indexer produces index-commit events | Exact search product, analyzers, index definitions and capacity configuration |
| Cache | Versioned ephemeral results with short TTL; authorization-versioned | Retrieval/storage boundary | TTL values and cache technology; no durable authority |
| Event queue/outbox | Durable propagation and at-least-once delivery | Platform teams own messaging contracts; individual event producers listed below | Queue product, delivery partitions, complete ledgers and retention |
| Vault/secret store | Workspace credential references, application secrets and encryption-key references | Managed service identities; operator revocation is supported | Provider, key isolation/rotation tradeoff and concrete grants |
| Independently controlled audit retention storage | Append-only batch-hash-chain exports | Audit/governance process; physical custodian unspecified | Export format, chain algorithm and corporate retention selection |
| Release/evaluation repository artifacts | IDL, signed images/configuration/test outputs, fixtures and release bindings | Domain/platform/AI-platform contract teams; Security/SRE validate promotion | Repository layouts, formats and named custodians |

Sources: pp.7, 9, 15–16, 27, 51–53, 62–63, 71–76, 87 [data:r1:c3:f5; data:r1:c4:f12–f13; data:r1:c6:f2,f7–f11; data:r1:c10:f6; data:r1:c17:f8,f13–f14; data:r1:c20:f10–f11; data:r1:c23:f1–f3,f8,f12; data:r1:c24:f2; data:r1:c28:f2–f3].

The Orchestrator has no direct database credentials and uses narrowly scoped APIs. No datastore has a public IP. Internal services use independently authorized TLS/mTLS, service audiences and scoped IAM; deployment units do not share service identities. Managed workload identity replaces static credentials wherever supported. Worker egress is restricted to declared repository/model destinations. [pp.9, 16, 18; data:r1:c4:f12; data:r1:c6:f11; data:r1:c7:f1–f3.]

User responsibilities are not database ownership: Analyst opens cases/evaluates evidence, Reviewer approves/rejects, Workspace Admin manages connectors/policy, Auditor reads redacted immutable evidence without editing case content. Baseline roles are `Analyst`, `Reviewer`, `Admin`, `Auditor`, `Service`; mappings for `Workspace Admin`, `Owner`, `Member`, `approver` and `Operators` remain open under SF-002/OQ-001 and API-OQ-001. [pp.11, 22, 83; data:r1:c5:f2–f3; data:r1:c8:f6; data:r1:c26:f6–f16.]

**Out of scope:** Physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing, agent administrative cloud permissions and application-hosted GPU inference are explicitly excluded. Cross-region active/active mutation, OCR beyond English and customer-managed weights are deferred. These exclusions do not exclude ordinary authorized case operations. [pp.9–10, 19; data:r1:c4:f7,f13; data:r1:c7:f7.]

### Selected relational inventory

All eighteen table names below are source-confirmed. Their complete schemas and named physical owners are **Needs confirmation**. Producer/service mappings are domain responsibility mappings, not proof of a particular SQL-writing identity. Sources for the exact selected fields and constraints are Appendix B p.85 [data:r1:c27:f2–f19]; additional domain relationship evidence is cited after the table.

| ID / table | Purpose / primary constraint | Related screens | Related APIs and operations |
|---|---|---|---|
| DAT-002 `tenants` | Tenant security scope; unique slug | Authorized shell context; exact placement unspecified | API-045 principal/tenant binding; onboarding/lifecycle API-024/025 |
| DAT-003 `workspaces` | Group users, policies, connectors and cases; tenant RLS | SCR-001–008 in authorized scope; especially SCR-007 | API-027 membership; workspace policy mutation missing; API-024/025 lifecycle |
| DAT-004 `cases` | Mutable revisioned case aggregate; tenant/id uniqueness | SCR-001, SCR-002 | API-001 create, API-002 list, API-003 read, API-004 update, API-005 close |
| DAT-005 `case_revisions` | Append-only case change history | SCR-002; audit consumer placement unspecified | API-004/005 domain history; exact history read API unspecified |
| DAT-006 `documents` | Source identity/classification/ACL context | SCR-002, SCR-003, SCR-006 | API-006 ingestion, API-007 status, API-008–010 evidence, API-039 storage |
| DAT-007 `document_versions` | Immutable source/processing versions and object references | SCR-003; case attachments | API-006/039/052; cited through API-008–010 |
| DAT-008 `chunks` | Immutable evidence source anchors | SCR-003, SCR-005 | API-008–010, API-047 |
| DAT-009 `runs` | Bounded case-linked state machine and plan/budget | SCR-004; SCR-002 context | API-011 create, API-012 alternate chapter contract unresolved, API-013–015 read/progress |
| DAT-010 `run_steps` | Idempotent execution steps/checkpoints | SCR-004 | API-014 steps, API-037 workflow, API-046 stage events |
| DAT-011 `evidence_sets` | Run-linked chunk references with publication validation | SCR-003, SCR-004, SCR-005 | API-008–010, API-017 publication dependency, API-047 output |
| DAT-012 `approval_tasks` | Reviewed artifact identity and reviewer routing; no self approval | SCR-005 | API-016 task read, API-017 decision; assignment/opening transport missing |
| DAT-013 `approval_decisions` | Immutable decision history | SCR-005, authorized SCR-008 | API-017 write, API-020 redacted audit lineage |
| DAT-014 `audit_events` | Append-only actor/action/digest records | SCR-008 | API-020 read; accepted/denied operation audit across all APIs |
| DAT-015 `outbox_events` | Transactional event publication | No direct editing screen | API-046; API-038 validated replay/recovery dependency |
| DAT-016 `connector_cursors` | Durable connector checkpoint/retry state | SCR-006, visible subset unspecified | API-018 sync, API-019 run read, API-050 provider integration |
| DAT-017 `token_ledger` | Run/deployment input/output token attribution | Placement unspecified; not an extra Usage screen | API-021 usage, API-036/051 generation usage |
| DAT-018 `policy_evaluations` | Reproducible rule/input/result lineage | SCR-005, SCR-007 context | API-017/046 gate validation; policy write contract incomplete |
| DAT-019 `deletion_receipts` | Auditable purge/protected-record outcomes | Placement unspecified | API-025/040 deletion, API-024 manifest dependency, API-046 verification |

Domain mappings: pp.12, 24–32, 40–46, 48–59, 65, 78–83, 87 [data:r1:c5:f7–f8; data:r1:c9:f1–f4,f13; data:r1:c10:f7; data:r1:c11:f1,f10; data:r1:c14:f2,f5; data:r1:c15:f2,f6–f10; data:r1:c16:f2,f7–f8; data:r1:c17:f5,f8; data:r1:c19:f1–f8; data:r1:c21:f7; data:r1:c25:f10–f11; data:r1:c26:f6–f16; data:r1:c28:f1–f8].

### DAT-020 Relationships and cardinality

| Relationship | Confirmed or qualified meaning | Cardinality / integrity status |
|---|---|---|
| Case → tenant / workspace | Reference `cases` DDL has non-null UUID FKs to `tenants(id)` and `workspaces(id)` | Every case requires one identifier for each parent; parent keys are referenced. Reverse multiplicity and cascade actions unspecified. Separate FKs do not enforce same-tenant workspace membership. |
| Workspace → users/policies/connectors/cases | Workspace groups these resources | Collection membership supported; minimum/maximum/optionality and complete FKs unspecified |
| Case → revisions | Independently versioned aggregate with append-only history | Exact revision key/uniqueness, count and snapshot/patch relationship unspecified |
| Case → attachments / runs | Separate entities linked by immutable identifiers | Multiplicities and case-link FKs unspecified; no embedded-array schema approved |
| Attachment → document version | References immutable document version | Target semantics explicit; optionality and FK field unspecified |
| Document → versions → chunks | Selected `document_id` and `document_version_id` imply associations, supported by provenance behavior | Logical mapping supported; physical keys/cardinalities unresolved, including omitted `document_versions.id` |
| Run → steps / evidence / tasks / evaluations / token usage | Selected `run_id` fields and domain workflow link these concepts | Not proof of FK definitions, one-to-one relationships or required row counts |
| EvidenceSet → citations/chunks | Permission-sensitive evidence references; MCP returns `Citation[]` | `chunk_refs` representation, dedup/order/count and Citation schema unresolved |
| Decision → task / reviewer | Selected `task_id`, `reviewer_id`; authenticated actor decision | Exact task identity/API `approvalId` mapping, cardinalities and reviewer FK unresolved |
| Approval → run artifact hash | Exact reviewed content identity | Binding mandatory; artifact store/key/hash algorithm and physical constraints unresolved |
| Current approved result → artifact / satisfied gate | Pointer and gate commit atomically; closure snapshots lineage | Pointer field/FK and gate record representation unresolved |
| Connector → cursor / sync runs / ledger | Every sync run retains cursor/high-watermark/error ledger | Provider cursor versus `connector_cursors.cursor` and ledger relationships unresolved |
| Receipt → object / tenant / manifest | Auditable object outcomes; deletion event carries manifest and receipt-hash labels | FK targets, retained-record relationship and cardinalities unresolved |

Sources: pp.7, 24–26, 28, 31, 45, 51, 85–87 [data:r1:c3:f2; data:r1:c9:f1–f4,f13; data:r1:c10:f7; data:r1:c11:f10; data:r1:c15:f7,f9; data:r1:c17:f5; data:r1:c27:f20–f22,f30; data:r1:c28:f5,f8,f11].

No diagram arrow is evidence for a one-to-many FK or delete cascade. Production FK/procedure design must separately prevent cross-tenant links, including same-tenant workspace membership. [pp.2, 86; data:r1:c2:f2; data:r1:c27:f29.]

### DAT-021 Additional logical records and artifacts

The following names are source component/record names, **not additional confirmed SQL table names**. Physical schemas, cardinalities, retention and named data owners remain open. Each row preserves the chapter register in source order. The four register categories mean: first `Owner aggregate / UUIDv7 + tenant scope`; second `Immutable derivative / SHA-256 source/ revision`; third `Policy-bound control / Actor and role predicate`; fourth `Operational ledger / Event ID + trace context`. These labels do not grant the application `Owner` permission, define arbitrary hash columns or resolve mutable lifecycle conflicts.

| Pages / register names in source order | Logical data purpose and API dependency | Register evidence |
|---|---|---|
| 8–10: `ChangeRequest`, `DesignRevision`, `RequirementLink`, `DecisionRecord` | Baseline changes, impact scores, requirement links and decisions; API-031/032 | data:r1:c4:f3–f5,f14–f15 |
| 11–13: `Actor`, `Case`, `Attachment`, `ApprovalAssignment` | Principal/action provenance, case input and assigned review; API-001/011 | data:r1:c5:f4,f12–f13 |
| 15–17: `EdgeGateway`, `CaseService`, `Orchestrator`, `RetrievalService` | Service boundary records, transactional work, run and cited evidence; API-012/013 | data:r1:c6:f3,f8,f13–f14 |
| 18–20: `VirtualNetwork`, `APIReplicaSet`, `WorkerPool`, `RegionFailoverPlan` | Runtime configuration, capacities and restore plans; API-034/035 | data:r1:c7:f4,f12–f13 |
| 21–23: `Principal`, `TenantMembership`, `AccessPolicy`, `ResourceAcl` | Identity/membership/resource authorization; API-026/027/045 | data:r1:c8:f3,f5,f7,f9,f13–f14 |
| 24–26: `Workspace`, `CaseAggregate`, `CaseRevision`, `CaseStatusEvent` | Workspace settings, current case/history/status; API-004/005; workspace write conflicted | data:r1:c9:f5–f6,f14–f16 |
| 27–29: `Connector`, `SyncRun`, `SourceCursor`, `SourceDocument` | Capability/credential/sync/checkpoint/source history; API-018/019/050 | data:r1:c10:f3,f12–f14 |
| 30–32: `DocumentVersion`, `ExtractionJob`, `ContentBlock`, `ChunkAnchor` | Immutable derivatives, parser quality, layout and provenance; API-006/007 | data:r1:c11:f4,f12–f13 |
| 34–36: `SearchChunk`, `IndexAlias`, `RetrievalQuery`, `EvidenceSet` | Index representation, alias versions, query and evidence selection; API-008/009 | data:r1:c12:f3,f10–f11 |
| 37–39: `ModelDeployment`, `PromptTemplate`, `GenerationAttempt`, `TokenLedger` | Deployment registry, prompt revisions, candidate generation and usage; API-028/036/051 | data:r1:c13:f4,f12–f13 |
| 40–42: `AgentRun`, `PlanNode`, `ToolCapability`, `A2ATaskEnvelope` | DAG/checkpoint/capability/handoff; API-011/014/047/048 | data:r1:c14:f3,f13–f14 |
| 44–46: `PolicyEvaluation`, `ApprovalTask`, `ReviewDecision`, `PublicationGate` | Normalized policy, reviewer task, decision and publish gate; API-016/017 | data:r1:c15:f4,f11–f12 |
| 48–50: `OutboxRecord`, `QueueEnvelope`, `WorkflowCheckpoint`, `DeadLetterEntry` | Delivery/replay/checkpoint/recovery; API-037/038/046 | data:r1:c16:f3,f12–f13 |
| 51–53: `CaseRow`, `DocumentBlob`, `OutboxTable`, `CacheEntry` | Storage authority/objects/outbox/ephemeral cache; API-039/040 | data:r1:c17:f3,f7,f9,f11,f15–f16 |
| 54–56: `ApiOperation`, `ErrorEnvelope`, `EventCursor`, `WebhookSubscription` | IDL/client contract/errors/resume/webhook data; API-029/015/049/053 | data:r1:c18:f3,f10–f11 |
| 57–59: `ViewState`, `ReviewForm`, `EvidencePanel`, `Notification` | UI consumer/component records; API-002/010 | data:r1:c19:f3,f12–f13 |
| 61–63: `ThreatControl`, `AuditEntry`, `DataClassification`, `KeyReference` | Controls/audit/material class/key refs; API-020/030 | data:r1:c20:f4,f12–f13 |
| 64–66: `TraceSpan`, `MetricSeries`, `CostLedger`, `AlertPolicy` | Safe telemetry/usage/cost/alert policy; API-021/041 | data:r1:c21:f2,f9–f10 |
| 68–70: `CapacityBudget`, `AdmissionPermit`, `RecoveryCheckpoint`, `LoadProfile` | Capacity/admission/reference recovery; API-033/042 | data:r1:c22:f4,f12–f13 |
| 71–73: `ReleaseArtifact`, `ConfigVersion`, `MigrationPlan`, `RolloutGate` | Reconstructible release/config/schema rollout; API-043/044 | data:r1:c23:f4,f13–f14 |
| 74–76: `TestCase`, `EvalDataset`, `Scorecard`, `ReleaseGateResult` | Synthetic fixtures/versioned benchmark/score/gate; API-022/023 | data:r1:c24:f3,f6,f8,f10,f14–f15 |
| 78–80: `Runbook`, `ProvisioningJob`, `ExportManifest`, `PurgeReceipt` | Operations/onboarding/controlled export/delete lineage; API-024/025 | data:r1:c25:f4,f12–f13 |

Further source-supported artifacts include classification corrections and reason codes, source ACL revisions/tombstones, parser quality/personal-data/injection tags, candidate and approved response artifacts, reviewer escalation/override evidence, event/operation duplicate outcomes, reconciliation receipts, signed evaluation manifests, randomized seeds, signed test outputs, SBOM, signed images/environment configuration, infrastructure definitions, audit exports and incident evidence. No physical table or file name is supplied for these artifacts. [pp.12, 28–32, 38–39, 45–46, 62–66, 71–80, 88–90; data:r1:c5:f7–f8; data:r1:c10:f7–f11; data:r1:c11:f7–f11; data:r1:c13:f7–f11; data:r1:c15:f6–f10; data:r1:c20:f8,f10–f11; data:r1:c21:f6–f8; data:r1:c23:f2–f3,f8–f12; data:r1:c24:f7,f9,f13; data:r1:c25:f2–f3,f10–f11; data:r1:c29:f12; data:r1:c30:f19,f21; data:r1:c31:f7–f12.]

## Data Field Definitions

### Definition convention

Each listed field retains its supplied spelling. Unless the cases DDL or a specific interface explicitly defines a property, its **physical type, length/precision, nullability, requiredness, default, PK/FK/uniqueness, range, encoding and validation mechanism are individually Needs confirmation**. Listing a selected field does not prove `NOT NULL`, an FK or a UI input. Logical mandatory information can reside in a related immutable record rather than an invented column.

Chapter 14 specifies persistence identifiers as UUIDv7 for sortable event-time locality and tenant/business-key-scoped uniqueness. Appendix B uses SQL `UUID` without an identifier generator/default. This combination supports the logical UUIDv7 persistence requirement but does not specify generation location or impose UUIDv7 on every REST placeholder. Exact REST schemas remain governed by unavailable repository IDL/OpenAPI. [pp.51, 55, 82, 86; data:r1:c17:f2; data:r1:c18:f8; data:r1:c26:f1; data:r1:c27:f21.]

### DAT-022 Exact selected-field catalog

The type/default convention above applies separately to **every member** of grouped field rows. The following p.85 excerpts preserve all supplied selected columns and primary constraints. Meaning annotations are logical interpretations, not finalized physical definitions. [Appendix B.1; data:r1:c27:f2–f19.]

| Table | Exact selected field names | Logical meanings | Exact primary constraint |
|---|---|---|---|
| `tenants` | `id`, `slug`, `plan`, `region`, `created_at` | Tenant identifier, unique slug, plan, region, creation time | `unique(slug)` |
| `workspaces` | `id`, `tenant_id`, `policy_version`, `quota` | Workspace/tenant identities, policy version, quota | `RLS tenant scope` |
| `cases` | `id`, `tenant_id`, `workspace_id`, `status`, `revision` | Current case identity/security scope/state/version | `unique(tenant_id,id)` |
| `case_revisions` | `case_id`, `revision`, `patch`, `actor`, `at` | Case link, revision change/patch, actor and time | `append only` |
| `documents` | `id`, `workspace_id`, `source_id`, `sensitivity` | Document/workspace/source identities and class | `source ACL enforced` |
| `document_versions` | `document_id`, `hash`, `parser_version`, `object_key` | Parent document, content identity, parser lineage, object reference | `immutable` |
| `chunks` | `id`, `document_version_id`, `page`, `bbox`, `text_hash` | Chunk/version identity, page/region anchor, text fingerprint | `source anchor` |
| `runs` | `id`, `case_id`, `status`, `plan_revision`, `budget` | Run/case identities, state, plan version and bounded budget | `bounded state machine` |
| `run_steps` | `id`, `run_id`, `step_kind`, `status`, `checkpoint` | Step/run identities, execution kind/state/resume data | `idempotent step` |
| `evidence_sets` | `id`, `run_id`, `chunk_refs`, `acl_digest` | Evidence/run identities, permission-sensitive evidence references | `publish validation` |
| `approval_tasks` | `id`, `run_id`, `reviewer_pool`, `artifact_hash` | Task/run identity, reviewer eligibility and reviewed artifact | `no self approval` |
| `approval_decisions` | `id`, `task_id`, `reviewer_id`, `decision`, `reason` | Immutable task/reviewer decision and explanation | `immutable` |
| `audit_events` | `id`, `tenant_id`, `actor_id`, `action`, `digest` | Audit identity/security/principal/action/integrity digest | `append only` |
| `outbox_events` | `event_id`, `tenant_id`, `aggregate_revision`, `payload` | Delivery/security/version identity and event data | `transactional outbox` |
| `connector_cursors` | `connector_id`, `cursor`, `watermark`, `retry_state` | Connector/provider continuation, durable progress and retry control | `durable checkpoints` |
| `token_ledger` | `run_id`, `deployment_id`, `in_tokens`, `out_tokens` | Run/deployment attribution and token usage | `attributed cost` |
| `policy_evaluations` | `run_id`, `rule_version`, `input_digest`, `result` | Run/rule/input identity and deterministic result | `reproducible` |
| `deletion_receipts` | `tenant_id`, `object_ref`, `purge_time`, `actor` | Tenant/object/time/actor purge lineage | `auditable purge` |

`document_versions.id` is not included in the selected catalog, although `chunks.document_version_id` and event Version ID concepts exist. Its key definition is **Needs confirmation**, not evidence that version identity is absent. `documents` omits `tenant_id` from selected fields, but every tenant-owned row logically requires tenancy under DAT-024. Do not infer that omitted tenancy fields are unnecessary.

### DAT-023 Reference cases DDL and field constraints

**Confirmed reference excerpt**, Appendix B.2 p.86 [data:r1:c27:f20]:

```sql
CREATE TABLE cases (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  workspace_id UUID NOT NULL REFERENCES workspaces(id),
  status TEXT NOT NULL CHECK (status IN
    ('NEW','TRIAGED','IN_PROGRESS','PENDING_APPROVAL',
     'RESOLVED','CLOSED')),
  revision BIGINT NOT NULL DEFAULT 1,
  sensitivity TEXT NOT NULL DEFAULT 'INTERNAL',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, id)
);
ALTER TABLE cases ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_scope ON cases USING (
  tenant_id = current_setting('app.tenant_id')::UUID
);
```

| Physical field | Reference type / nullability / default | Keys, range and meaning | Remaining decision |
|---|---|---|---|
| `id` | `UUID PRIMARY KEY`; no supplied default | Global PK uniqueness plus declared tenant/id unique pair | UUIDv7 generation mechanism; REST/display-ID mapping |
| `tenant_id` | `UUID NOT NULL`; no default | FK `tenants(id)`; mandatory tenant security scope | Update/delete actions and context validation |
| `workspace_id` | `UUID NOT NULL`; no default | FK `workspaces(id)`; mandatory workspace link | Additional same-tenant enforcement and cascade actions |
| `status` | `TEXT NOT NULL`; no SQL default | Exact six-value CHECK shown above | Transition enforcement mechanism; NEW is domain initial state, not a supplied SQL default |
| `revision` | `BIGINT NOT NULL DEFAULT 1` | Monotonic domain revision, used for If-Match | Increment/locking mechanism; DDL has no positivity CHECK |
| `sensitivity` | `TEXT NOT NULL DEFAULT 'INTERNAL'` | Case sensitivity label backing name | No supplied class CHECK/length; input editability and classification mapping |
| `created_at` | `TIMESTAMPTZ NOT NULL DEFAULT now()` | Creation time | Timestamp precision and explicit UTC handling |
| `updated_at` | `TIMESTAMPTZ NOT NULL DEFAULT now()` | Last-update time meaning | No supplied update trigger; automatic refresh is not established by default |

Sources: p.86 [data:r1:c27:f21–f27], monotonic revision/initial state pp.12, 24–25 [data:r1:c5:f7; data:r1:c9:f4,f10]. Database defaults `1`, `'INTERNAL'` and `now()` are not approved browser defaults or independent wire defaults.

Production must additionally enforce workspace-tenancy membership “via foreign keys or controlled write procedures.” The mechanism is **Needs confirmation**. Reset scoped connection-pool session variables after **every transaction**, including failed transactions; no success-only exception exists. RLS role behavior, `WITH CHECK`/bypass/FORCE policy choices and absent/invalid `app.tenant_id` handling are not supplied by the excerpt. Do not independently add a specific mechanism as confirmed. [p.86; data:r1:c27:f27–f29.]

### DAT-024 Shared durable provenance and identity data

| Logical information / supplied spelling | Confirmed meaning and required condition | Physical/wire status |
|---|---|---|
| `tenant_id` | Every tenant-owned row; every durable-change boundary; immutable signed job tenancy | UUID for reference cases/outbox catalog has unspecified type; no client tenancy substitution |
| `revision` | Durable-change metadata; current case monotonic version | `BIGINT` only confirmed for cases; other types/increment rules open |
| `actor_id` | Durable-change principal provenance | Type and mapping to selected `actor`/`reviewer_id` open |
| `occurred_at` | Durable-change time provenance | UTC logically; field type/precision open outside supplied DDL |
| correlation ID / `correlation_id` | Cross-boundary context independent of provider trace IDs | Exact transport and selected-table storage mapping open |
| `trace_id` | Request/event trace; request child spans cover DB/connector/retrieval/model/approval | Type/format/transport open; not silently equivalent to correlation ID |
| `aggregate_revision` | Event/outbox stale-replay guard | Not automatically the physical case `revision` column |
| issuer, audience, expiry, subject, tenant | API token authentication concepts | Claim spellings/types/allowed algorithms/audiences/lifetimes open |
| role/membership/ACL/action/duties | Deterministic authorization inputs | Complete ACL/member/role schemas and predicates open |

Sources: conditional metadata across chapter registers (DAT-021); pp.16–17, 21–23, 48, 64 [data:r1:c6:f3,f11–f12; data:r1:c8:f2,f6,f8,f11–f12; data:r1:c16:f2–f3; data:r1:c21:f1]. Each register's metadata requirement applies **when an operation changes durable state**; it does not make read-only UI components durable tables or metadata client-editable fields.

### DAT-025 Logical domain fields beyond selected columns

| Record / field meaning | Confirmed logical data requirement | Needs confirmation beside requirement |
|---|---|---|
| Case `title`, `description`, priority, sensitivity label, status, owner, current approved result | Stored case attributes; attachments/runs separate; monotonic revision | Physical columns for fields omitted from DDL; lengths, required create inputs, edit rules and owner predicate |
| impact, urgency, priority | Priority derives from explicit impact/urgency, never model alone | Formula, types/options/ranges and correction permissions |
| labels, confidences, provenance, correction reason code | Asynchronous policy-aware classification; user correction includes reason code | Field names/storage, confidence scale, label/reason catalog and correction API |
| deadline, workspace business calendar/timezone, breach prediction | Calendar computes contractual deadline; prediction advisory only | Calendar source, datatype/precision and schedule rules |
| source identity / ACL / history | Connector preserves source identity, permissions and change history | Provider schemas, ACL revision type and history structure |
| capability support | list, fetch, delta cursor, ACL, delete; unsupported warns lower trust | Flags/schema, supported-source catalog and warning codes |
| provider cursor, high-watermark, error ledger | Every sync run stores these; cursor advances after durable preceding outcomes | Mapping to `cursor`, `watermark`, `retry_state`, item outcomes and checkpoint atomicity |
| quarantine reason/correlation/remediation | Malformed exhausted-retry record retains all three | Reason enum, remediation path format, retry bounds and remediation rights |
| parser/content structure | Page index, bbox, table rows/columns, headings, reading order; opt-in OCR provenance | Coordinates, numbering, opt-in actor/default and parser-version mapping |
| fingerprint + pipeline version | Immutable derivative ID; side-by-side reprocessing without rewriting claims | Algorithm/encoding and relation to `hash`, `text_hash`, `parser_version` |
| chunk source URI, file hash, page, optional bbox | Every chunk stores anchor provenance; citations resolve/currently permitted | Exact column names, URI schema, hash/bbox/page formats |
| extraction quality | Empty-page ratio, unknown-character ratio, table-loss indicators, language confidence | Scales/thresholds; low quality remains viewable but not autonomous support |
| search row | `tenant_id`, `workspace_id`, `document_version_id`, `chunk_id`, language, classification, 1536-dimensional embedding, normalized keyword text | Index types, embedding scalar type/column name, analyzer configuration, language catalog |
| response evidence item | Chunk ID, source title, document revision, page anchor and ACL digest; opaque citation verified before display | Exact wire keys and link to `document_version_id`; complete Citation schema |
| index alias/generation | Parallel rebuild and checked atomic read-alias switch | Generation type, hash scope, thresholds and retirement |
| cache key | Tenant, user-scope digest, source ACL revision, query hash, index generation | Key serialization/digests/TTL; authorization purge precedes normal expiry |
| model deployment | capability, region, data-handling class, context length, cost profile, evaluation approval | Exact registry fields/types/approved values; deployment whitelist is workspace-specific |
| prompt/generation | Fixed system rules, signed workflow instruction, validated user input, delimited retrieved passages; versioned schema | Prompt format/signature/schema; bounded parse retry values |
| injection indicators | Gateway records indicators and strips evidence tool directives | Indicator schema and retention |
| run/plan | DAG, depth eight, maximum sixteen tool invocations, plan revision before effects, dependencies/checkpoints | Node/edge/checkpoint schemas, budget settlement and runtime deadline |
| tokens/cost | Reserved input/output tokens and provider usage under workspace quota; cost-center/model-version attribution | `budget` structure, token/currency numeric types, quota limits and settlement |
| policy evaluation | Normalized sensitivity, action, evidence quality, model class, financial impact category, confidence bands retained with rule-set version | `input_digest` alone is not sufficient; input storage and mapping to `rule_version`/`result` open |
| approval task | Exact candidate hash, reviewer pool/minimum role/duties, configured SLA | Immutable candidate versus mutable task lifecycle, state field, assignment/expiry implementation |
| approval decision | decision, actor, timestamp, evaluated artifact hash, rationale, optional annotations | Map `reason`/`reviewer_id`/`task_id`; required input rationale, enum, hash encoding and annotation schema |
| publication gate | Exact final response pointer and satisfied gate in same transaction | Pointer/FK/gate fields and approved artifact storage |
| override/escalation | Elevated role, secondary reviewer and audited reason; expiry escalation recorded | Role independence, schema, SLA value and recipient; no retroactive approval |

Sources: pp.12, 24–39, 40–46, 53, 65, 85 [data:r1:c5:f7–f8; data:r1:c9:f3–f4,f10,f12; data:r1:c10:f1–f2,f6–f11; data:r1:c11:f7–f11; data:r1:c12:f2,f5–f9; data:r1:c13:f2–f3,f7–f11; data:r1:c14:f5,f8–f12; data:r1:c15:f1–f3,f6–f10; data:r1:c17:f14; data:r1:c21:f7; data:r1:c27:f6–f18].

### DAT-026 Governance, operational, privacy and release fields

| Record or artifact | Logically supported contents | Physical decisions still open |
|---|---|---|
| Change/baseline records | Behavior/data-migration/threat-surface/operating-cost impact scores; requirement links; approved minor revision and incompatible-protocol major revision | Score names/scales, approvals and schemas |
| Diagnostic traces/metrics | Identifier/policy outcomes; request/error/latency/saturation; grounding pass, empty retrieval, provider throttle, tokens, backlog age | Metric names/types/units/windows; no document content |
| Cost rollups/alerts | Workspace cost center/model version; daily budget/forecast/rejected excess; routine spend ticket owner/threshold | Currency/precision/timezone; daily aggregation is not an execution schedule; owner/value not assigned |
| Classification/privacy tags | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`; maximum included material class; likely-personal-data tags | Tag schema/detection rules/redaction catalog and physical class CHECKs |
| Key/credential references | Workspace-scoped secret references, managed identity and policy rotation | Provider/reference types/rotation interval/isolation decision |
| Audit records/exports | Actor/action/digest; decision/prompt-template digest/access lineage; batch hash chain | Canonicalization/chain algorithm/batch size/manifest schema |
| Provisioning/backfill | Workspace policy/key refs/roles/quotas/connector stubs, incomplete status, stable source IDs, batch reconciliation receipts/index coverage | State/readiness/receipt schemas/window bounds |
| Export manifest/package | Case metadata, approved artifacts, source references, audit manifests and checksums | Container/encoding/checksum/delivery/expiry; excludes secrets/internal prompts |
| Hold/tombstone/purge receipt | Protected-record retention, object/tenant/time/actor receipt lineage, eligible blob/index removal | Hold targets/rules, tombstone fields, partial-completion status and corporate policy |
| Evaluation fixture | 1,200 synthetic permission-controlled cases; expected citation sets/outcomes; categories retrieval/refusal/ambiguity/adversarial evidence | Dataset file/schema, label encoding and domain taxonomy |
| Scorecard | Citation precision >=0.97, unsupported-claim rate <=0.02, frozen high-risk recall 1.00; confidence intervals/domain shift | Denominators/precision/CI method/low-confidence threshold |
| Test provenance | Successful/empty/mixed-permission/adversarial/malformed fixtures; every random seed; frozen/versioned/reviewed corpora | Seed/version storage/signing algorithm/reviewer mapping |
| Release record | Image digest, schemas, prompts, model routing policy; signed test outputs digest-linked; SBOM and signed configuration/images | Artifact formats/signatures/allowed build identities and retained lineage schema |
| Incident record | Audit IDs, time window, blast radius, quality effect, preventative action | Table/field schema, time precision and retention |

Sources: pp.8–10, 62–66, 71–80, 88–90 [data:r1:c4:f2–f4,f8; data:r1:c20:f7–f11; data:r1:c21:f1,f4–f8; data:r1:c23:f1–f3,f8–f12; data:r1:c24:f7,f9,f13; data:r1:c25:f2–f3,f10–f11; data:r1:c29:f12–f14; data:r1:c30:f17–f21; data:r1:c31:f12–f13].

## Lifecycle and Consistency

### DAT-027 Authorization and sensitive data procedure

1. Bind each request to authenticated principal and tenant. OIDC authorization-code flow with PKCE and issuer/audience/expiry/subject/tenant validation applies. Reject unexpected algorithms/missing tenancy. Do not keep long-lived refresh tokens in browser local storage. A BFF with secure, HttpOnly, SameSite cookies is permitted, not selected.
2. Enforce role, tenant, workspace membership, sensitivity, document ACL, requested action and separation of duties at resource boundaries. Domain services re-evaluate attributes inside transactions; hidden UI controls are not enforcement.
3. Install tenant-scoped RLS context and include tenant in every storage predicate. Preserve signed immutable background-job tenancy and reset pooled scoped variables after each transaction.
4. Return the same not-found class for absent and foreign-tenant IDs. Denial audit retains principal/denied resource class without disclosing private existence.
5. ACL-filter before any chunk reaches model context. Resolve/verify opaque citations before display. Recheck current authorization and evidence before publication; historical retention/retrieval is not continued access permission.
6. Use the maximum class of included material for route/redaction/retention/approval. Extraction tags likely personal data. Gateway redacts nonessential fields where policy permits; exact rules remain open. Do not invent a PII field catalog, consent regime or jurisdictional law.
7. Keep connector credentials in workspace-scoped secret references. Models receive scoped context/structured prompts, not raw connector tokens or unrestricted DB access; tools/models receive no secrets outside declared scope. Default model logs capture digests/token counts, not full prompts. Diagnostic traces and errors exclude documents, credentials, full prompts and unauthorized existence. Auditor scope is redacted.
8. Treat retrieved/model payloads as untrusted data: no tool/tenant/approval/policy authority. Delimit evidence and preserve provenance; schemas/tools are pinned/allowlisted and independently authorized. Discovery is never invocation permission; consequential writes need human authorization/idempotency and denied effects cannot use equivalent tools.

Sources: pp.7, 15–16, 21–23, 27, 31, 35–42, 57–63, 64, 84, 86–87 [data:r1:c3:f3–f4; data:r1:c6:f2,f11; data:r1:c8:f1–f12,f16; data:r1:c10:f6; data:r1:c11:f10; data:r1:c12:f1,f8,f14; data:r1:c13:f3,f7–f11; data:r1:c14:f8–f12; data:r1:c19:f15; data:r1:c20:f1–f3,f7–f11; data:r1:c21:f1; data:r1:c26:f18; data:r1:c27:f28–f29; data:r1:c28:f12–f13].

### DAT-028 State catalogs and history

| Aggregate | Confirmed states / initial condition | Transitions and guards / open decisions |
|---|---|---|
| Case | `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED`; starts `NEW` | `NEW→TRIAGED→IN_PROGRESS`; `IN_PROGRESS→PENDING_APPROVAL` or `RESOLVED`; `PENDING_APPROVAL→RESOLVED` or `IN_PROGRESS`. Role/revision/approval guards. `CLOSED` final except explicit new-revision reopening; closure entry and reopen target open. |
| Document | `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED` | Scan/quality guards; exact edges and initial persisted status open. Unsafe quarantine/no index; low-quality viewability exception applies. |
| Run | `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED` | Checkpoint/runtime-budget guards; chapter linear progression follows listed processing stages before publication/failure. AUTO_ALLOW route, missing-approval timing and recoverable-timeout literal open. |
| Review | `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED` | Every transition actor/hash/duties guarded. Exact edges and opening/assignment mechanism open; expiry records escalation/reassignment, never approval. |
| Policy result | `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY` | Deterministic versioned normalized inputs; LLM tags cannot override. Not the decision-input enum. |
| UI draft label | `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` | Presentation only; mapping to stored aggregate states open. |

Sources: pp.12, 25, 44–45, 49, 57, 82, 86 [data:r1:c5:f7; data:r1:c9:f9; data:r1:c15:f3,f6; data:r1:c16:f7; data:r1:c19:f6; data:r1:c26:f2–f5; data:r1:c27:f23].

Cases remain mutable revisioned aggregates; revisions and decisions are append-only/immutable as supported. Closure snapshots approved answer, cited versions and reviewer decisions and preserves immutable approved lineage. Denied/rejected work can be reworked as new run revisions, not retroactively approved. The `Immutable derivative` labels for Case/CaseService/CaseAggregate remain source conflicts requiring register amendment; they do not prohibit the confirmed case lifecycle. [pp.13, 17, 24–26, 45–46, 85; data:r1:c5:f12; data:r1:c6:f13; data:r1:c9:f2,f4,f13–f15; data:r1:c15:f10; data:r1:c27:f5,f13.]

### DAT-029 Transactions, concurrency, audit and replay

1. Validate request payload before transaction entry/long-running allocation, revalidate domain invariants and pinned tool arguments before dispatch. Client validation is convenience only.
2. Apply revision/hash/idempotency preconditions before accepted mutation. Case PATCH uses `If-Match`; stale updates return `409 CASE_VERSION_CONFLICT` and current revision. No automatic stale-edit merge/retry is authorized. Changed reviewed artifacts reject as stale and are audited.
3. Job-creating POSTs require `Idempotency-Key`; identical payload replay returns original operation/outcome, changed fingerprint returns `409 IDEMPOTENCY_CONFLICT`. Actor/request-fingerprint outcomes last 24 hours. Key format/scope/fingerprint/locking/missing-key/post-expiry behavior remain open. Do not extend 24 hours to all event/SSE/history retention.
4. Commit case mutations, approval decisions and outbox inserts in one ACID transaction. Commit final response pointer and satisfied approval gate together. Search and webhooks reconcile asynchronously. Every state-changing workflow uses transactional outbox or explicitly reconciled saga.
5. Persist plan revision before side effects and each stage checkpoint before downstream dispatch. The run DAG has depth at most eight and at most sixteen tool invocations. Runtime/token/time budgets and repeat-invalid-plan thresholds remain versioned policy decisions where values are absent.
6. At-least-once consumers deduplicate event ID and operation key, inspect aggregate revision, record duplicate outcome and do not reapply accepted mutation. No business invariant relies on queue ordering across partitions. Accepted replay leaves one business transition and one accepted-transition audit lineage.
7. Transient faults use bounded exponential backoff/jitter/per-dependency circuit breakers. Validation/permission faults are permanent and not retried. Mutable retries require idempotency and consequential effects additionally human authorization.
8. Dead-letter replay requires operator reason, dry-run validation and scope limit. Preserve original event identity except schema-transforming migration with explicit provenance link.
9. Keep one audit record per accepted transition and stable safe denied-operation errors/tenant traces. Mandatory denial audit still applies when business state remains unchanged. `AccessDenied` ordering/revision semantics are open; rejection-before-event prose must not suppress logs.
10. Historical approval decisions cannot be altered. Audit entries are append-only, batch-hash chained and exported independently; exact chain/signature representation remains open.

Sources: pp.15–17, 22–26, 40–46, 48–56, 62, 89 [data:r1:c6:f1,f10,f12,f15,f17; data:r1:c8:f10,f12,f15,f17; data:r1:c9:f10–f11,f17,f19; data:r1:c14:f5,f10–f12,f15,f17; data:r1:c15:f7–f10,f13,f15; data:r1:c16:f1–f3,f6–f11,f14,f16; data:r1:c17:f8; data:r1:c18:f5,f9,f13–f16; data:r1:c20:f10; data:r1:c30:f1–f8].

The repeated chapter pattern also requires positive, foreign-tenant denial, duplicate/replay and evidence-retention tests for component interfaces; their published events must appear in correlated logs/audit without source text in diagnostics. This applies to the entire DAT-021 inventory, not just the relational core. [Chapter verification/registers pp.8–80; data:r1:c4:f6,f18; data:r1:c5:f6,f16; data:r1:c6:f6,f17; data:r1:c7:f6,f16; data:r1:c8:f17; data:r1:c9:f8,f19; data:r1:c10:f17–f18; data:r1:c11:f14,f17; data:r1:c12:f15–f16; data:r1:c13:f14,f17; data:r1:c14:f7,f17; data:r1:c15:f15–f16; data:r1:c16:f5,f16; data:r1:c17:f19–f20; data:r1:c18:f12,f16; data:r1:c19:f5,f16; data:r1:c20:f6,f16; data:r1:c21:f15; data:r1:c22:f6,f16; data:r1:c23:f7,f17; data:r1:c24:f4,f18; data:r1:c25:f6,f16.]

### DAT-030 Ingestion, connector and derivative lifecycle

1. Provision workspace policy/key references/roles/quotas/connector stubs through one idempotent workflow; expose incomplete provisioning and block sync until complete. Exact provisioning API/schema is not supplied.
2. Validate PDF/DOCX/HTML/UTF-8 text signature versus extension, configurable 25 MB per-file policy and decompression threshold. MB convention/file counts/decompression numeric bound remain open.
3. Scan before parsing, disable macros/embedded remote fetch. Unsafe payloads quarantine without indexing. Preserve claim text during normalization, layout/table/page/heading/reading-order provenance and opt-in OCR evidence; OCR beyond English is deferred.
4. Use content fingerprint plus pipeline version for immutable derivative identity and side-by-side reprocessing. Preserve source URI/file hash/page/optional bbox and quality flags. Low-quality permitted documents remain viewable but cannot ground autonomous recommendations.
5. Sync preserves provider source identities/ACL/history and stores cursor/high-watermark/error ledger. Advance only after preceding durable outcomes. Honor provider `Retry-After`, workspace quotas/backoff/jitter/fair scheduling. After bounded retries, malformed items quarantine with reason/correlation/remediation and may permit remaining batch continuation with ledger exception.
6. Historic backfill uses bounded windows/stable source IDs/per-batch reconciliation receipts. Search readiness depends on index coverage, not queue emptiness.
7. Failed index writes do not roll back accepted metadata. Compare fingerprints, retry and repair links from outbox. Rebuild parallel index and atomically switch read alias only after completeness/recall checks.
8. Source deletion creates tombstone and schedules index removal; source ACL change invalidates affected caches before new results, and revocation is effective before next retrieval. Cache key includes tenant/user scope/ACL revision/query hash/index generation and purge precedes ordinary TTL.
9. Model/provider outage disables new generation while retaining safe manual/evidence workflows; lexical continuation during vector degradation may display reduced quality. Never waive approval/authorization. Suspected ACL leakage instead suspends affected aliases/revokes cached evidence/preserves audit/scoped ACL replay until negative tests pass.
10. Delayed-indexing recovery pauses only faulty connector/indexer shard and keeps accepted records durable. Diagnose queue age/backlog/tenant/index generation, event ID/outbox lag/parser flags/search throttle/ACL revision; replay validated outbox through bounded operator job; compare source/index fingerprints and denied probes before closing incident. Link audit IDs/time window/blast radius/quality effect/prevention.

Sources: pp.10, 27–36, 49, 53, 68–70, 78–80, 90 [data:r1:c4:f13; data:r1:c10:f1–f11; data:r1:c11:f1–f11; data:r1:c12:f5–f9; data:r1:c16:f8; data:r1:c17:f14; data:r1:c22:f1,f7–f11; data:r1:c25:f2–f3,f7–f8; data:r1:c31:f7–f12].

### DAT-031 Retention, deletion, export and personal data

| Data scope | Confirmed lifecycle | Needs confirmation |
|---|---|---|
| Eligible closed cases | Retention only for eligible closed cases; approved lineage preserved, legal holds respected | Eligibility/duration/schedule and history disposal mechanisms |
| Soft-deleted resources | Unretrievable; final purge scheduled through tombstone pipeline | Tombstone schema/cadence/partial completion |
| Diagnostic logs | Default TTL 30 days; safe identifiers/outcomes, no documents/API secrets | Override policy and corporate retention mapping |
| Security audit | Separate fictional seven-year policy; append-only hash-chain/independent storage | Corporate retention selection, chain/receipt/hold details |
| Held/protected records | Purge retains and receipts protected records | Hold target/state/create/release schema and authorized procedure |
| Export | Two independent checks; controlled manifest and checksummed metadata/approved artifacts/source refs/audit manifests | Independent approver workflow, format/checksum/download/status |
| Workspace deletion | Two independent checks, legal hold, tombstones, eligible blob/index removal and receipts | Receipt/retained exception fields and verification status |
| Personal-data requests | Share deletion/export inventory; likely personal data tagged/redacted where policy permits | Inventory schema/access scope and request procedure; no extra endpoint confirmed |
| Credentials/key refs | Secrets vaulted; queued revoked connector jobs fail safely; policy key rotation without request-path bulk re-encryption | Key isolation versus rotation throughput before enterprise GA |
| Event/dedup/SSE/fixtures/release artifacts | Domain-specific lineage and retained replay requirements | No universal retention period is supplied |

Sources: pp.26–27, 51–53, 62–66, 78–80, 83, 89–90 [data:r1:c9:f13; data:r1:c10:f6; data:r1:c17:f6,f13; data:r1:c20:f8,f10–f11; data:r1:c21:f8; data:r1:c25:f1,f10–f11; data:r1:c26:f16; data:r1:c30:f13; data:r1:c31:f13].

A single Admin export fails the two-person control. `Admin + approver` in Appendix A does not resolve the independent-person procedure. Immutability does not imply indefinite retention; deletion does not permit destruction of held data or release of revoked historical content. Export excludes secrets and internal model prompts by design. [pp.78–83, 88–89; data:r1:c25:f1,f10–f11; data:r1:c26:f16; data:r1:c29:f11; data:r1:c30:f13.]

### DAT-032 Migration, environment and recovery

Use expand-and-contract migrations: add nullable columns, bounded backfill, then enforce constraints; do not delete fields used by active readers. Predeploy migrations are backward compatible, enforcement waits for old replicas to drain, and rollback plans describe readability of new writes. Canary regression rolls back traffic/binary, not an assumed database down-migration; compensation only if explicitly supported. [pp.20, 52, 72; data:r1:c7:f11; data:r1:c17:f10; data:r1:c23:f9,f11.]

Release records bind image digest/schema/prompt/model-routing policy and reconstruct binary/prompt/policy. Preserve signed configuration, vault references, signed container images/SBOM/allowed build identity and signed digest-linked tests. Terraform or Bicep are alternatives, not selected here. Security/SRE validate egress/secrets/backups/alerts before promotion. [pp.71–73, 89; data:r1:c23:f1–f3,f8–f12; data:r1:c30:f21.]

Production data is forbidden in development. Staging uses synthetic data/test connectors and isolated secrets/quotas. R1 writes primary, with one warm recovery region restored under incident command. Reference continuous PostgreSQL backup targets RPO `<=15 minutes`, RTO `<=4 hours`; test object versions and index rebuild recipes together with relational consistency. No exact region, backup retention or restore schedule is selected. [pp.19, 69–70; data:r1:c7:f8,f10; data:r1:c22:f10–f11.]

Reference sizing is `2,000` active daily users, `60` steady/`180` burst requests/s, `100,000` indexed documents/tenant and `20` concurrent runs/large tenant. Typical `1 MB` source yields approximately `40–120` chunks depending on content/parser quality; raw files/normalized text/vectors/replication overhead are sized separately. These are reference assumptions, not page limits, field constraints or per-client quotas. Availability `99.9%` monthly, case-create P95 under/within `300 ms` and search P95 under `1.5 s` excluding remote fetch are conditional design targets; equality/load measurement remains open. [pp.12, 65, 68; data:r1:c5:f10; data:r1:c21:f5; data:r1:c22:f2–f3.]

## Integration Data and Acceptance Criteria

### DAT-033 Files, encodings and temporal representations

| Input/output or interface | Confirmed representation and validation | Needs confirmation |
|---|---|---|
| Attachment/repository documents | PDF, DOCX, HTML, UTF-8 text; matching MIME signature/extension, configurable 25 MB, decompression protection/scan before parse | Multipart fields, binary format variants, other encodings, MB units/file counts/parser bounds |
| Normalized artifacts | Immutable text/layout/metadata; source claims preserved; anchors/quality/OCR provenance | Output filenames/container formats/text encoding/layout schema |
| Private objects | Key includes tenant/workspace/document/version/object role; public name opaque; encrypted/scoped short-lived signed URL | Key syntax/object role catalog/URL expiry/renewal |
| REST/OpenAPI | `/v1` nouns, cursor pagination, RFC 3339 timestamps; repository IDL generates OpenAPI | Actual IDL files, schema and media types outside examples; cursor order/expiry/page size |
| Internal HTTP/gRPC | Versioned/generated, independently authorized; protobuf governs gRPC | Actual protobuf/schema/deadline/types |
| Events | Canonical JSON, UTC and exact envelope below | Canonicalization standard, signing, encoding/precision and payload schemas |
| SSE | Monotonic offsets; `Last-Event-ID` resumes only retained currently scoped data | Offset encoding/retention/heartbeat/expired or future offset behavior |
| Optional webhooks | Signed; recipient verifies age/signature; backoff retry, no case rollback | URL/method/payload/signature header/algorithm/age/retry bounds |
| Export/audit manifests | Checksummed authorized export; independently retained audit-chain exports | Archive format/encoding/checksum/canonicalization/delivery |
| Evaluation/release artifacts | Frozen/versioned synthetic fixtures, recorded seeds, signed manifests/test outputs and release digests; signed config/images/SBOM | File schemas/signatures/SBOM format/repository names |
| Time in storage/UI | Server UTC; reference cases TIMESTAMPTZ; workspace-local labeled presentation; locale does not change order/API representation | Precision/timezone/calendar configuration and supported locale catalog |
| Business deadlines | Workspace-timezone business calendars; advisory prediction cannot change contractual deadline | Calendar rules/time types/holiday source; no schedule inferred from sample deadline |

Sources: pp.25, 30–32, 48, 51–59, 71–73, 78–79, 87–90 [data:r1:c9:f12; data:r1:c11:f1–f11; data:r1:c16:f2; data:r1:c17:f13; data:r1:c18:f1–f9; data:r1:c19:f11; data:r1:c23:f2–f3,f8,f12; data:r1:c25:f10; data:r1:c28:f9–f12; data:r1:c29:f12; data:r1:c30:f19–f21].

### DAT-034 Event definitions and lineage

All events logically require `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, `payload`; producers use canonical JSON/UTC. These are exact envelope spellings, but their wire types/version values/signature/canonicalization are **Needs confirmation**. Durable actor/correlation metadata is separately required when appropriate; do not silently equate `revision` and `aggregate_revision`. [p.48; data:r1:c16:f2–f3.]

| Event | Producer | Exact selected payload labels, not typed JSON keys | Consumer action |
|---|---|---|---|
| `CaseCreated` | Case Service | `Case ID / revision` | Run classifier |
| `DocumentNormalized` | Ingestion | `Version ID / source hash` | Build index |
| `SearchIndexCommitted` | Indexer | `Index generation / document revision` | Invalidate query cache |
| `AgentPlanApproved` | Orchestrator | `Run ID / plan hash` | Dispatch plan steps |
| `ApprovalDecisionRecorded` | Policy Service | `Task / actor / content hash` | Validate publication |
| `WorkflowStageAdvanced` | Orchestrator | `Run / stage / checkpoint` | Resume consumers |
| `AccessDenied` | Policy Service | `Principal / action / policy digest` | Alert enrichment |
| `TenantDeletionVerified` | Retention Worker | `Manifest ID / receipt hash` | Close purge record |

Source p.87 Appendix C.1 [data:r1:c28:f1–f8]. Publication validation is not unconditional publication.

Other chapter event identifiers remain `BaselineCommitted`, `RunRequested`, `DeploymentPromoted`, `CaseStateChanged`, `ConnectorSyncStarted`, `ModelInvocationCompleted`, `DataRetentionPurgeCommitted`, `ApiCompatibilityVerified`, `UserReviewOpened`, `SecurityPolicyChanged`, `SloBurnRateDetected`, `BackpressureActivated`, `ReleasePromoted`, `EvaluationCompleted`. Preserve register versioned-envelope/outbox, audit, duplicate-ledger/revision and authorization-recheck requirements. Producer/typed payload/SSE/state mappings not supplied remain open; these names are not automatically SSE event types. [Registers pp.10–80; DAT-021 source references; data:r1:c4:f15–f18; data:r1:c5:f13–f16; data:r1:c6:f14–f17; data:r1:c7:f13–f16; data:r1:c9:f16–f19; data:r1:c10:f14–f18; data:r1:c13:f13–f17; data:r1:c17:f16–f20; data:r1:c18:f11–f16; data:r1:c19:f13–f16; data:r1:c20:f13–f16; data:r1:c21:f10,f12–f15; data:r1:c22:f13–f16; data:r1:c23:f14–f17; data:r1:c24:f15–f18.]

### DAT-035 MCP, A2A and errors

| `knowledge.search@v1` field | Supplied type | Constraint / meaning |
|---|---|---|
| `query` | `string` | Search text; length/default/requiredness open |
| `case_id` | `uuid` | Case context; UUID version and requiredness open |
| `max_items` | `int<=10` | Tool-specific upper bound; minimum/default/requiredness open |
| `evidence_set_id` | `uuid` | Evidence reference; requiredness open |
| `citations` | `Citation[]` | Citation output; complete member schema/count/requiredness open |

Authorization is tenant-scoped `read:permitted_documents`; effect is read-only, with no arbitrary URLs/filesystem access. This bound is not UI page size or global evidence-selection ten. Capability registration is discovery metadata; principal/workspace policy/tool scope/data class independently decide invocation. [p.87; data:r1:c28:f10–f13.]

A2A requires task/capability, declared input/output schemas, deadline and trace context; receiver may decline. Exact source example follows, not a default, identifier pattern or schedule. [pp.41, 87; data:r1:c14:f9; data:r1:c28:f9.]

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

Formal A2A requiredness/types/output schema/transport/error handling remain open. `case_demo` cannot directly satisfy adjacent MCP `uuid`; adapter resolution is Needs confirmation, not approved coercion. [p.87; data:r1:c28:f14; API-OQ-015.]

Error data retains API-053. The source conflict example has `error` object with string `code: CASE_VERSION_CONFLICT`, `message: Case revision no longer matches.`, example string `correlation_id: trace_01HZZ_EXAMPLE`, Boolean `retryable: false`, and `details` object with integer `expected_revision: 7`, `actual_revision: 8`; HTTP `409`, `Content-Type: application/json`. Values are placeholders, not defaults; universal requiredness remains open. Preserve uppercase literals despite snake-case naming prose. Other known literals are `IDEMPOTENCY_CONFLICT`, `NO_SUPPORTED_EVIDENCE`, `MODEL_OUTPUT_INVALID`, `CONNECTOR_REAUTH_REQUIRED`, `DENY`, each only with its documented scope/status mapping. Safe validation details are permitted, never credentials/full prompts/retrieved documents/private existence. [pp.25, 27, 36, 38, 54, 84, 89; data:r1:c9:f10; data:r1:c10:f6; data:r1:c12:f9; data:r1:c13:f8; data:r1:c18:f2,f5; data:r1:c26:f17–f18; data:r1:c30:f2–f6,f14.]

### DAT-036 Acceptance matrix

Use synthetic authorized and negative fixtures. Confirm missing schema/threshold choices before executable tests depend on them; tests cannot silently decide defaults.

| Source test / affected DAT | Procedure | Expected data outcome |
|---|---|---|
| TST-001 / DAT-004,029 | Create twice with same key/body | One case and identical response |
| TST-002 / DAT-029 | Same key, changed body | `409 IDEMPOTENCY_CONFLICT`; no second accepted outcome |
| TST-003 / DAT-024,027 | Read foreign-tenant case | `404`-equivalent non-disclosing error |
| TST-004 / DAT-006,011,030 | Index then revoke source access; query next | No forbidden evidence |
| TST-005 / DAT-025,035 | Force model schema failure | `MODEL_OUTPUT_INVALID`; no publication |
| TST-006 / DAT-012,013,029 | Approve wrong/old artifact hash | Stale rejection, audited; no accepted stale change |
| TST-007 / DAT-015,029 | Replay accepted outbox message | Exactly one accepted business transition |
| TST-008 / DAT-029,030 | Provider 429 burst | Capped retries and controlled admission; exact cap open |
| TST-009 / DAT-011,028 | Generate missing citations | Needs-review or unsupported; deterministic branch open, never fabricated approved response |
| TST-010 / DAT-012,028 | Expire review task | No implicit approval; escalation recorded |
| TST-011 / DAT-004 consumer | Keyboard-only case opening | No blocked action and visible focus |
| TST-012 / DAT-032 | Reference regional recovery | RPO <=15 minutes, RTO <=4 hours; relational/object/index verification |
| TST-013 / DAT-019,031 | Tenant purge under legal hold | Protected records retained and receipted |
| TST-014 / DAT-027,035 | Arbitrary MCP invocation | `DENY` before dispatch |
| TST-015 / DAT-030 | Unsafe PDF | Quarantine, no indexing |
| TST-016 / DAT-032 | Regressed canary safety score | Release promotion blocked |

Sources p.89 [data:r1:c30:f1–f16], recovery p.69 [data:r1:c22:f10].

Additional concrete verification:

1. Perform create→ingest→retrieve→draft→review→publish with authorized Analyst, permitted evidence and independent eligible Reviewer. Keep retrieval/generation/policy/approval records separate. Show exact artifact/citations/model-prompt/policy reasons, inspect sources before approval, and atomically publish only matching supported artifact under current ACL/policy. Exercise rejected rework, poisoned quarantine and foreign search denial. [pp.11–12, 45–46, 57–58, 75; data:r1:c5:f1–f3,f7–f8; data:r1:c15:f7–f10; data:r1:c19:f1,f8; data:r1:c24:f12.]
2. Exercise transaction-scoped tenant context in pooled connections after success/failure; test foreign ID, cross-tenant parent-link and same-tenant workspace integrity. Exact mechanism is open, but bypass is unacceptable. [pp.22–23, 86; data:r1:c8:f8,f11–f12; data:r1:c27:f22,f27–f29.]
3. Verify source anchor preservation, citation resolution/opaque-ID verification/page-range click-through, current ACL, low-quality viewability and unsafe no-index behavior. Revoke mid-search and between retrieval/publication; no stale release. [pp.31–36, 57–59, 88; data:r1:c11:f7–f11; data:r1:c12:f1,f8,f14; data:r1:c19:f6,f15; data:r1:c29:f8.]
4. Quarantine exhausted malformed sync item with reason/correlation/remediation and ledger-recorded partial continuation. Cursor must not pass an item without durable outcome. Revoked credentials fail queued jobs without token exposure; unsupported capabilities visibly lower trust. [pp.27–29; data:r1:c10:f2,f6–f11.]
5. Fail index write and confirm accepted source metadata remains durable; reconcile fingerprints/outbox and gate alias switch/readiness on completeness/recall/coverage. Contain only faulty shard; for suspected ACL leak require negative tests before re-enable. [pp.34, 49, 78–79, 90; data:r1:c12:f5; data:r1:c16:f8; data:r1:c25:f3,f8; data:r1:c31:f8–f11.]
6. Refresh/reconnect ongoing authorized run; reconstruct server progress and replay only retained scoped monotonic events. Review transitions must enforce actor/hash/duties. Required form fields, offset expiry and exact state edges await decisions. [pp.55, 58, 82; data:r1:c18:f6; data:r1:c19:f7–f8; data:r1:c26:f5.]
7. Test historical decision/audit edit denial, redacted Auditor reads, safe error/traces, independent audit export and two-person export. Hold-safe purge must retain/receipt protected objects. [pp.11, 62, 78–80, 88–89; data:r1:c5:f3; data:r1:c20:f10; data:r1:c25:f1,f10–f11; data:r1:c29:f9,f11; data:r1:c30:f13.]
8. Verify schema compatibility/reader drain and release reconstruction without assumed DB down-migration; signed test output references release digest. Test restored relational/object/index consistency and production-data prohibition in development. [pp.19–20, 52, 69, 71–73, 89; data:r1:c7:f8,f10–f11; data:r1:c17:f10; data:r1:c22:f10; data:r1:c23:f1,f8–f12; data:r1:c30:f21.]

### Security, fixtures and evaluation exit criteria

Appendix D preserves `T-01`–`T-12`: foreign-token valid-ID guessing; hostile PDF instructions; old-draft approval; polyglot PDF/zipped attack; credential observations in traces/provider requests; unapproved regional fallback; **100** same-event replays; mid-search permission revocation; historical audit edit; mutually recursive tool hints; single-Admin export; replaced expected-score fixtures. ZIP is attack input, not added supported format; 100 is test count, not runtime retries. Dataset version/signed manifest protect fixtures. `SEC-001`–`SEC-012` block release; no explicit one-to-one mapping to T numbering exists. Security-control owner independently reviews/reproduces negative cases and signs release evidence, but no owner name/date is assigned. Unmitigated critical isolation/approval failures block regardless of AI scores. [p.88; data:r1:c29:f1–f14.]

Critical isolation/approval tests allow zero exceptions. Test deterministic state/idempotency/ACL/hash/retry/schema invariants without live model calls, pin provider adapters and exercise disposable PostgreSQL/outbox/ACL/delayed-index/object-purge scenarios with randomized retries leaving one outcome. [p.74; data:r1:c24:f1–f2,f5.]

Reference evaluation uses `1,200` synthetic permission-controlled cases with expected citations/outcomes; precision `>=0.97`, unsupported claims `<=0.02`, frozen high-risk recall `1.00`, confidence intervals/domain shift. Changed prompt/model requires re-evaluation; low confidence blocks release. Fixtures cover successful, empty, mixed-permission, adversarial and malformed inputs; record every randomized seed and freeze/version/independently review corpora for leakage. Release pack includes unit/schema-evolution/negative-auth/replay/staging-sync/visual-accessibility/search-recall/grounding/policy-recall/load/recovery tests with signed digest-linked outputs. [pp.75–76, 89; data:r1:c24:f7,f9,f13; data:r1:c30:f17–f21.]

## Consistency and Open Questions

### Field mappings and required amendments

| Open ID / affected requirements | Evidence and unresolved mapping | Required clarification / earlier links |
|---|---|---|
| DAT-OQ-001 / DAT-002–024 | Selected catalog p.85, abbreviated DDL p.86 lack full schemas | Complete every field type/length/precision/nullability/default/key/range/physical owner and FK/cascade/cardinality. Link API-OQ-003 and earlier SF-014/OQ-015; do not fill omitted columns silently. |
| DAT-OQ-002 / DAT-004,005,021,028 | Mutable case pp.24–25 versus Case/CaseService/CaseAggregate immutable registers pp.13/17/26 | Amend register semantics to distinguish current state/revisions/evidence/approved lineage; scope SHA-256 rather than invent case hash. SF-006/OQ-009; API-OQ-006. Evidence data:r1:c5:f12, data:r1:c6:f13, data:r1:c9:f4,f14–f15. |
| DAT-OQ-003 / DAT-003,023,024,027 | Separate parent FKs and RLS p.86 do not enforce same-tenant workspace | Select FK versus controlled write, RLS roles/context missing/invalid behavior/reset verification; SF-003/OQ-018, API-OQ-017. data:r1:c27:f22,f27–f29. |
| DAT-OQ-004 / DAT-003,025 | Workspace settings linked to case PATCH p.24 | Define genuine workspace mutation/revision schema; never send invented settings in API-004. SCR-007/SF-012/OQ-011, API-OQ-006. data:r1:c9:f3,f6. |
| DAT-OQ-005 / DAT-024,035 | UUIDv7 persistence p.51, SQL UUID p.86, REST placeholders unspecified, A2A case_demo versus MCP UUID p.87 | Resolve generators/display IDs/REST types/adapter without coercion; API-OQ-003/015, SF-015/OQ-015. data:r1:c17:f2, data:r1:c27:f21, data:r1:c28:f9–f10,f14. |
| DAT-OQ-006 / DAT-005,013,016,018,019,024 | `actor`/`at` versus `actor_id`/`occurred_at`; `reason` versus rationale; `watermark` versus high-watermark; `rule_version` versus rule-set version | Explicit physical/wire/semantic mapping; retain source spelling. `input_digest` does not replace normalized inputs. API-OQ-003/008/012; SCR-005/OQ-012. data:r1:c27:f5,f13,f16,f18–f19, data:r1:c15:f2,f7. |
| DAT-OQ-007 / DAT-007,008,011,025 | Omitted version key; `hash`, file hash, text_hash, document revision/version ID, page index/page, optional bbox/anchor | Define keys/hash inputs/encoding/canonicalization/page numbering/bbox units/Citation schema. No SHA-256 propagation beyond evidenced scope. SF-007/SCR-003/OQ-010; API-OQ-011/015. data:r1:c11:f7–f10, data:r1:c12:f8, data:r1:c27:f7–f8. |
| DAT-OQ-008 / DAT-009,028 | Missing-approval termination p.41 versus AWAITING_REVIEW p.49/82 and expiry p.45; recoverable timeout p.12 versus FAILED p.82; AUTO_ALLOW p.44 versus linear review | Define terminal timing/run consequence/timeout literal/recovery/AUTO_ALLOW edges; no implicit approval. SF-009/OQ-008; API-OQ-009. data:r1:c14:f11, data:r1:c16:f7, data:r1:c15:f3,f6, data:r1:c5:f10, data:r1:c26:f3. |
| DAT-OQ-009 / DAT-004,012,013,025,028 | Close/reopen edge, priority formula/classification correction and required review inputs absent | Define guards/input schemas/reason catalogs/decision enum/annotations/SLA/assignment/override; keep state enum distinct from decision input. SF-006/OQ-009, SF-010/OQ-012; API-OQ-008. |
| DAT-OQ-010 / DAT-021,025 | Membership/SyncRun/IndexAlias/ApprovalTask/ReviewForm immutable classifications versus update/checkpoint/switch/task/form behavior | Clarify immutable content/revisions versus mutable pointers/control state. No generic register creates missing SQL tables or prohibits documented actions. API-OQ-007/012, OQ-012. data:r1:c8:f13, data:r1:c10:f7,f12–f13, data:r1:c12:f5,f10, data:r1:c15:f6,f11, data:r1:c19:f8,f12. |
| DAT-OQ-011 / DAT-021,029,034 | Repeated GET allocation/idempotency/entity/event associations throughout registers | Reconcile each read/health/OpenAPI/status path and related records; preserve validation/non-ambiguous success but do not approve GET-triggered mutation. API-OQ-007/019, SF-014/OQ-015. Representative data:r1:c6:f5, data:r1:c7:f5,f13, data:r1:c18:f4,f11, data:r1:c26:f7,f10,f14–f15. |
| DAT-OQ-012 / DAT-024,029,034 | Rejection before AccessDenied p.22 coexists with mandatory denial audit pp.23/87 | Define ordering/revision semantics without changing rejected business state or suppressing denial evidence. API-OQ-013, SF-016/OQ-015. data:r1:c8:f10,f12, data:r1:c28:f7. |
| DAT-OQ-013 / DAT-029,033–035 | IDL/payload types/signatures/canonicalization, SSE/webhook retention/offset/age/retry schemas missing | Define generated contracts and separate actor/fingerprint 24-hour retention from event/SSE policies. API-OQ-003/010/013/015; SF-009/OQ-008. |
| DAT-OQ-014 / DAT-025,030 | Cap 25 MB configurable; decompression/quality/OCR/retry/quota thresholds absent | Define units/policy versions/thresholds/actor/defaults/remediation; preserve unsafe versus low-quality and poison continuation. SF-007/OQ-010/013, API-OQ-011/012/016. |
| DAT-OQ-015 / DAT-026,031 | Two checks, legal hold, receipts and shared inventory lack schemas/procedure | Define independent approver/held-record/partial completion/export format/checksum/download/subject inventory. No new screen inferred. SF-017/OQ-016; API-OQ-014. |
| DAT-OQ-016 / DAT-026,027,031 | Likely personal data and conditional redaction p.62; defaults differ from unselected corporate policy | Define privacy tags/redaction/access scopes/retention classes/hold rules without inventing laws or consent. SF-013/OQ-014/018; API-OQ-017. data:r1:c20:f7–f8, data:r1:c21:f8, data:r1:c31:f13. |
| DAT-OQ-017 / DAT-021,032,036 | Representative aliases and title/selection mismatches pp.7/14/33/43/47/60/67/77/81 | Preserve eight primary SCR names; no new Overview/Usage/evaluation/recovery screen. Define consumers and display-ID/status/metric mappings. SF-004/OQ-003/004, API-OQ-018. |
| DAT-OQ-018 / DAT-032,036 | within versus under 300 ms, undefined measured load/admission/retry thresholds | Resolve equality/measurement and versioned numeric controls; keep reference target/sizing status. OQ-017; API-OQ-016. data:r1:c5:f10, data:r1:c21:f5, data:r1:c22:f2,f7. |
| DAT-OQ-019 / DAT-001,026,031,032 | Region/search/identity/models/corporate retention/connector permissions unselected p.90; key isolation/rotation open p.10 | Dated architecture decisions before implementation lock and encryption tradeoff before enterprise GA. No owner/date/provider/approval invented. OQ-018; API-OQ-017. data:r1:c4:f13, data:r1:c31:f13. |
| DAT-OQ-020 / DAT-021,026,032,036 | Evaluation/release/incident schemas, score confidence methods and artifact formats absent | Define signed fixture/output/release lineage and restore recipes; critical safety gates remain separate from AI scores. API-OQ-019; later specifications dependency. |

### Representative values and configuration are not approved defaults

Representative views display fictional tenant/workspace context, `Meridian Manufacturing`, case IDs `OD-2026-1042`–`OD-2026-1038`, subjects Supply chain response discrepancy / Batch quality deviation / Service contract inquiry / Customs document mismatch / Supplier invoice reconciliation and mixed human-readable statuses `Needs review`, `In progress`, `Published`, `Evidence gap`, `Triaged`. Cards show `128`, `14`, `97.6%`, `Healthy`; gate examples show `HUMAN_REVIEW`, `5 verified citations`, `gateway-r1.2`, `Assigned to reviewer`, `Awaiting decision`. These establish neither seeds/ID syntax/state catalog/formulas nor a five-citation minimum/model default. [pp.7, 14, 33, 43, 47, 60, 67, 77, 81; data:r1:c3:f6–f10; data:r1:c5:f18–f20; data:r1:c11:f19–f21; data:r1:c14:f19–f21; data:r1:c15:f18–f21; data:r1:c19:f18–f21; data:r1:c21:f16–f17; data:r1:c24:f20–f22; data:r1:c25:f18–f20.]

Appendix F exact examples: `release: r1.0`; workflow `max_plan_depth: 8`, `max_tool_calls: 16`, `run_timeout_seconds: 180`, `replay_dedup_hours: 24`; retrieval `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `embed_dimension: 1536`, `hybrid_rrf_k: 60`; policy `auto_publish_classification: INTERNAL`, `require_human_review_for: [HIGH_RISK, RESTRICTED]`, `self_approval_allowed: false`; storage `upload_limit_mb: 25`, `user_data_region: primary-approved-region`; observability `trace_sample_rate: 0.10`, `diagnostic_retention_days: 30`, `audit_retention_years: 7`. [p.90; data:r1:c31:f1–f6.]

Depth eight/sixteen calls, 1536 dimensions, configurable 25 MB cap, actor/fingerprint 24 hours and substantive no-self-approval/diagnostic/audit rules have independent chapter evidence **in their stated scopes**. Timeout 180, candidates 80, selected chunks ten, RRF 60, trace sample 0.10, auto-publish INTERNAL and placeholder region remain examples, not approved decisions. MCP `max_items<=10` is independently tool-specific. Configuration thresholds are versioned policy, not unversioned constants. [pp.9, 25, 30, 34, 40, 66, 85, 87, 90; data:r1:c4:f8; data:r1:c9:f10; data:r1:c11:f2; data:r1:c12:f2; data:r1:c14:f5; data:r1:c21:f8; data:r1:c27:f12; data:r1:c28:f10; data:r1:c31:f2–f6.]

### Dependencies and decision consolidation

This is Stage 3; [01_screen_functions.md](01_screen_functions.md) and [02_api.md](02_api.md) are reference dependencies, not independent source evidence. Do not rewrite their identifiers or elevate earlier proposals. This file supplies selected data details requested by API-OQ-003 and preserves unresolved API/SF mappings beside affected DAT requirements.

Asynchronous job details, exception/retry/error mappings, complete operational architecture and other remaining stage outputs are **To be defined in a later stage**. No later filename or requirement is presumed, except the required Stage 8 consolidation in `08_architecture_decision.md`. Stage 8 must link unresolved DAT/DAT-OQ items to `03_data.md` and the affected prior SCR/SF/OQ/API/API-OQ identifiers without inventing a decision, owner, deadline or approval. The current specification remains provisional pending separate root approval.
