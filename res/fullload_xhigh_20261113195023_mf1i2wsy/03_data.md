# 3. Data Specification

## Data Inventory and Relationships

### Specification Basis and Status

| Item | Definition |
|---|---|
| Specification file | `03_data.md` |
| Source document | `1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Source baseline | `OD-AI-DDS-001`, release `R1.0`, design revision `1.3` |
| Completed preceding specifications | [`01_screen_functions.md`](01_screen_functions.md), [`02_api.md`](02_api.md) |
| Scope | Source-described relational data, immutable document and answer evidence, search derivatives, event and operational records, integration files, configuration, and UI projections. |
| Identifier convention | `DAT-001`–`DAT-036` identify datasets or logical data-contract groups. `DAT-xxx-Fxx` identifies fields. `DAT-COM-xxx`, `DAT-REL-xxx`, `DAT-LC-xxx`, `DAT-CODE-xxx`, and `DAT-FILE-xxx` identify shared requirements, relationships, lifecycle requirements, code systems, and file contracts. `AC-DAT-xxx`, `CON-DAT-xxx`, and `OQ-DAT-xxx` identify acceptance criteria, conflicts, and unresolved contracts. |
| Identifier preservation | Source table names and preceding `SCR`, `API`, `API-CASE`, and `API-EVID` identifiers are retained. Assigned `DAT` identifiers do not rename source entities. |
| Citation convention | `[DDS]` identifies the source filename above. Citations use original PDF page numbers and source sections. |

[DDS]: 1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf

Statuses used throughout:

- **Confirmed:** Explicitly supported by source prose, a selected-field catalog, a reference contract, or the reference DDL.
- **Needs confirmation:** The source does not resolve the required physical, logical, integration, or operational contract.
- **Proposal:** An unapproved design suggestion. Previous proposals remain proposals unless explicitly approved through a separate decision.
- **NC:** Table abbreviation for **Needs confirmation**. It is not permission for an implementation AI to choose a value.

**DAT-COM-001 — Evidence interpretation.**

1. Preserve the source-confirmed logical data and invariants even where the reference DDL is incomplete.
2. Do not convert a selected field into a fully specified column, public JSON property, or editable screen control.
3. Do not infer `JSONB`, array storage, enum types, field lengths, indexes, foreign-key cascades, batch limits, schedules, or retention periods.
4. Treat illustrated customers, case numbers, counts, model labels, and Appendix F configuration as reference examples, not seed data or deployment approval.
5. Resolve missing contracts explicitly before implementing the affected production schema.

**Sources:** [DDS], pp. 1–2; p. 24, §6.1; p. 82, Appendix A introduction; pp. 85–86, Appendix B; p. 90, Appendix F and §F.2.  
**Earlier trace:** `SCR-COM-001`, `API-COM-001`, `OQ-API-003`.

### Confirmed Storage Responsibilities

| Store or data boundary | Authority and purpose | Confirmed access and consistency requirements | Unresolved selection |
|---|---|---|---|
| PostgreSQL | Authoritative case state and mutable metadata; transactional case, approval, and outbox writes. | Tenant-scoped database context, RLS, domain guards, ACID transactions, continuous backups. No public datastore endpoint. | Version, managed service, extensions, topology details, partition implementation, transaction isolation, and physical indexes: OQ-DAT-001/OQ-DAT-014. |
| Private encrypted blob/object storage | Source documents and immutable normalized text, layout, and metadata artifacts. | Keys include tenant, workspace, document, version, and object role. Public names are opaque. Access-controlled short-lived signed URLs and encryption at rest are mandatory. | Provider, container layout, serialization, URL lifetime, encryption-key isolation/rotation, and object/database coordination: OQ-DAT-010/OQ-DAT-017/OQ-DAT-025. |
| Hybrid vector/keyword search | Nonauthoritative searchable derivatives. | Eventually consistent; versioned aliases; parallel rebuild and atomic read-alias switch after completeness and recall checks. ACL filtering precedes text release. | Exact search provider, analyzers, vector numeric representation, index definitions, and readiness thresholds: OQ-DAT-011/OQ-DAT-025. |
| Cache | Versioned ephemeral retrieval results with short TTLs. | Authorization changes purge affected entries before normal TTL expiry. | Product, numeric TTL, value schema, invalidation protocol, and persistence policy: OQ-DAT-012. |
| Event queue and outbox | Durable state-change publication and replay-safe workflow continuation. | At-least-once delivery, event/operation deduplication, stale-revision detection, transactional outbox or explicitly reconciled saga steps. | Broker, routes, signatures, ledger schemas, retention, and replay limits: OQ-DAT-013. |
| Secret/key vault | Connector credentials, application secrets, encryption-key material. | Workspace-scoped references; managed identity where supported; secrets do not enter public responses, diagnostic traces, or model prompts. | Vault provider, reference schema, key hierarchy, and rotation policy: OQ-DAT-017/OQ-DAT-025. |
| Independently controlled audit retention storage | Exported append-only audit evidence with batch-hash chaining. | Operators may query but not alter historical review decisions. | Export format, integrity protocol, access controls, and approved corporate retention: OQ-DAT-016/OQ-DAT-018. |

**Sources:** [DDS], p. 7; p. 9, §1.3.1; pp. 16–19, §§3.2.2 and 4.1–4.2; pp. 22, 34, 48–53, 62–63, 69.

PostgreSQL is a **source-confirmed baseline choice**, not a new product decision made by this specification. Search, object-storage, queue, and vault providers are not selected here.

### Canonical Relational Entity Inventory

The first eighteen identifiers follow the order of the source’s Appendix B catalog. “Owner” identifies a source-supported processing responsibility, not an appointed decision owner or database account.

| Data ID | Source entity / physical table name | Purpose and principal relationships | Owner or writer responsibility | Screen and API mapping | Status and source |
|---|---|---|---|---|---|
| <a id="dat-001"></a>DAT-001 | `tenants` | Root tenant identity, slug, plan, region, and creation metadata. Referenced by tenant-owned resources. | Provisioning activity confirmed; exact tenant-table writer NC. | Shared tenant context; `SCR-X-002`; API-027 and provisioning gap API-GAP-008. No tenant CRUD API confirmed. | **Confirmed table and selected fields.** [DDS], pp. 78, 85–86. |
| <a id="dat-002"></a>DAT-002 | `workspaces` / `Workspace` | Groups users, policies, connectors, and cases; stores policy reference and quota. | Workspace configuration activity confirmed; exact datastore writer NC. | SCR-007; shared workspace context; API-028; API-GAP-002/API-GAP-008. | **Confirmed.** [DDS], pp. 24–25, 78, 85–86. |
| <a id="dat-003"></a>DAT-003 | `cases`; related terms `Case`, `CaseAggregate`, `CaseRow` | Current independently versioned case state and approved-result pointer. | Case Service owns transactional mutations. | SCR-001/SCR-002; API-001–005. | **Confirmed.** [DDS], pp. 12, 16, 24–26, 85–86. |
| <a id="dat-004"></a>DAT-004 | `case_revisions` / `CaseRevision` | Append-only case-change history associated with case and revision. | Case mutation boundary; exact table-writing implementation NC. | SCR-002 maintenance and closed lineage; API-004/005. | **Confirmed.** [DDS], pp. 25–26, 85. |
| <a id="dat-005"></a>DAT-005 | `documents`; related term `SourceDocument` | Workspace document identity, stable source reference, sensitivity, and originating ACL. | Connector/ingestion processes; exact writer and alias mapping NC. | SCR-002/SCR-003/SCR-006; API-006–010/018/019/049. | **Confirmed.** [DDS], pp. 27–32, 85. |
| <a id="dat-006"></a>DAT-006 | `document_versions` / `DocumentVersion` | Immutable source/parser/object version identity; parent of chunks and attachment references. | Ingestion Service owns conversion; exact persistence writer NC. | SCR-002/SCR-003/SCR-005; API-006–010/039. | **Confirmed.** [DDS], pp. 16, 30–32, 51–52, 85. |
| <a id="dat-007"></a>DAT-007 | `chunks`; related terms `ChunkAnchor`, `SearchChunk` | Stored source anchors and text fingerprints for immutable document versions. | Ingestion creates normalized evidence; Indexer creates search derivatives. | SCR-003 and citation panels; API-008–010/045. | **Confirmed table; alias equivalence NC.** [DDS], pp. 31, 34–35, 85. |
| <a id="dat-008"></a>DAT-008 | `runs` / `AgentRun` | Case-associated bounded AI workflow, status, plan revision, and budget. | Orchestrator manages run state through narrow scoped APIs; it has no direct database credentials. | SCR-002/SCR-004; API-011–015/037. | **Confirmed.** [DDS], pp. 9, 16, 40–42, 49, 85. |
| <a id="dat-009"></a>DAT-009 | `run_steps` / `PlanNode` relationship | Idempotent execution steps, outcomes, and checkpoints associated with a run. | Orchestration responsibility; exact physical writer and PlanNode mapping NC. | SCR-004; API-014/037. | **Confirmed table; mapping NC.** [DDS], pp. 40–42, 85. |
| <a id="dat-010"></a>DAT-010 | `evidence_sets` / `EvidenceSet` | Run-linked chunk references and ACL digest used for publication validation. | Retrieval returns evidence; persistence ownership NC. | SCR-002/SCR-003/SCR-004/SCR-005; API-008–010/013/045. | **Confirmed.** [DDS], pp. 35–36, 85, 87. |
| <a id="dat-011"></a>DAT-011 | `approval_tasks` / `ApprovalTask` | Run-associated review target, reviewer pool, and exact artifact hash. | Policy Service issues binding approval requirements. | SCR-005 and case decision gate; API-016/017. | **Confirmed.** [DDS], pp. 16, 44–46, 85. |
| <a id="dat-012"></a>DAT-012 | `approval_decisions` / `ReviewDecision` | Immutable reviewer decision and rationale associated with a task. | Policy/approval decision boundary. | SCR-005/SCR-008; API-017/021. | **Confirmed.** [DDS], pp. 45–46, 62, 85. |
| <a id="dat-013"></a>DAT-013 | `audit_events`; related terms `AuditEntry`, `DecisionRecord` | Append-only actor/action/digest evidence and authorized decision/access lineage. | Audit-producing services; exact ledger writer and aliases NC. | SCR-008; API-021. | **Confirmed table and audit behavior.** [DDS], pp. 11, 23, 62, 85. |
| <a id="dat-014"></a>DAT-014 | `outbox_events`; related terms `OutboxRecord`, `OutboxTable` | Transactional events associated with tenant and aggregate revision. | Business transaction producers; publication and consumer ownership vary by event. | Indirectly supports all durable workflows; API-001/004/005/017/037/038. | **Confirmed.** [DDS], pp. 17, 48–52, 85, 87. |
| <a id="dat-015"></a>DAT-015 | `connector_cursors` / `SourceCursor` | Durable connector cursor, watermark, and retry state. | Connector synchronization workers. | SCR-006; API-018/019/049. | **Confirmed.** [DDS], pp. 28–29, 85. |
| <a id="dat-016"></a>DAT-016 | `token_ledger` / `TokenLedger` | Run/deployment input and output token accounting and cost attribution. | Model Gateway accounting responsibility; exact ledger writer NC. | SCR-010; API-022/036/050. | **Confirmed.** [DDS], pp. 38–39, 65, 85. |
| <a id="dat-017"></a>DAT-017 | `policy_evaluations` / `PolicyEvaluation` | Reproducible rule version, normalized policy inputs, input digest, and result. | Deterministic Policy Service/Evaluator, not an LLM. | SCR-002/SCR-005; API-017 and run context. | **Confirmed.** [DDS], pp. 40, 44–46, 85. |
| <a id="dat-018"></a>DAT-018 | `deletion_receipts` / `PurgeReceipt` | Tenant/object purge evidence and legal-hold exceptions. | Retention Worker producer confirmed for `TenantDeletionVerified`; complete receipt writer NC. | `SCR-X-004/X-005`; API-026/040. | **Confirmed.** [DDS], pp. 66, 80, 85, 87, 89. |

### Supplementary Logical Data and Contract Inventory

These groups preserve supported data that is not fully represented in Appendix B. A group does **not** confirm a new table, collection, file name, or independent persistence requirement for every listed term.

| Data ID | Logical data / exact source terms | Purpose, relationships, and ownership | Screens / APIs | Physical-design status and source |
|---|---|---|---|---|
| DAT-019 | `Actor`, `Principal`, `TenantMembership`, `AccessPolicy`, `ResourceAcl` | Authenticated identity, tenant/workspace membership, role/action policy, and source ACL. Platform teams own identity propagation; resource policies are independently enforced. | All screens; API-027/028/048 and resource checks. | Tables, identifier mappings, and full fields **NC**. [DDS], pp. 11, 15, 21–23. |
| DAT-020 | `Attachment`; case classification and correction records | Separate case attachment entity references an immutable document version. Classification supplies labels, confidences, and provenance; correction requires a reason code. | SCR-002; API-001/006; API-GAP-001. | Attachment table and classification/correction schemas **NC**. [DDS], pp. 12, 24, 51. |
| DAT-021 | `Connector`, `SyncRun`, source identity/change history | Connector capabilities, credential references, sync outcomes, per-run cursor/error ledger, quarantine/remediation. | SCR-006; API-018/019/049. | Connector/sync tables and exact source-to-document mapping **NC**. [DDS], pp. 27–29. |
| DAT-022 | `ExtractionJob`, `ContentBlock`, quality and OCR provenance | Conversion jobs, PDF blocks, table annotations, headings, reading order, source anchors, quality indicators, likely-personal-data tags. Ingestion Service owns conversion. | SCR-002/SCR-003; API-006/007. | Job/block/quality schemas and serialization **NC**. [DDS], pp. 16, 30–32, 62. |
| DAT-023 | Search-row derivative, `IndexAlias`, `RetrievalQuery` | Tenant/workspace/version/chunk index projection, hybrid-query processing, generation aliases, and completeness/recall evidence. | SCR-003; API-009/010/045. | Provider-specific physical schema and query persistence **NC**. [DDS], pp. 34–36. |
| DAT-024 | `ModelDeployment`, `PromptTemplate`, `GenerationAttempt`, `ToolCapability` | Approved deployment registry, versioned prompts/output schemas, generation attempts, injection indicators, pinned tool discovery and separate authorization. AI platform owns gateway contracts. | SCR-002/SCR-004/SCR-005/SCR-007; API-020/036/045/050. | Registry/attempt/tool persistence, schemas, and public projection **NC**. [DDS], pp. 15, 37–42, 58. |
| DAT-025 | Candidate/approved artifacts, `ApprovalAssignment`, `PublicationGate`, closure snapshot | Exact candidate content, artifact hash, model/prompt/policy context, satisfied gate, final pointer, immutable closure lineage. | SCR-002/SCR-005; API-005/013/017 and API-GAP-006. | Artifact store, pointer columns, assignment/gate schema, hash contract, and snapshot format **NC**. [DDS], pp. 7, 12, 24–26, 44–46, 58. |
| DAT-026 | `QueueEnvelope`, `WorkflowCheckpoint`, `DeadLetterEntry`, consumer event ledger, operation/idempotency record | Durable continuation, duplicate/stale detection, bounded replay with original event identity and migration provenance. | SCR-004; `SCR-X-006`; API-037/038. | Ledger/checkpoint/dead-letter tables and exact schemas **NC**. [DDS], pp. 17, 25, 48–50. |
| DAT-027 | `CacheEntry` | Ephemeral authorized retrieval results keyed by identity, ACL revision, query hash, and index generation. | Indirectly SCR-003; API-009/010/045. | Key encoding, values, product, and TTL **NC**. [DDS], pp. 16, 53. |
| DAT-028 | `DocumentBlob`, raw and normalized object files | Encrypted source and immutable derivatives with tenant/workspace/document/version/object-role addressing. | SCR-003; API-039; browser source path API-GAP-003. | Actual object names, roles, formats, and URL schema **NC**. [DDS], pp. 31, 51–53. |
| DAT-029 | Holds, tombstones, deletion inventory, `Runbook`, `ProvisioningJob`, `ExportManifest`, backfill receipts | Provisioning, stable-source onboarding, legal-hold-safe deletion, authorized export, reconciliation and completion evidence. | `SCR-X-002/X-003/X-004/X-005`; API-025/026/029/040. | Hold/inventory/tombstone/manifest/provisioning schemas **NC**. [DDS], pp. 26, 51, 78–80. |
| DAT-030 | `TraceSpan`, `MetricSeries`, `CostLedger`, `AlertPolicy`, daily usage rollups | Privacy-safe diagnostics, attributed usage, budget/forecast/rejected excess, alert evidence. | SCR-010; API-022/041. | Metrics, rollup, cost/currency, and alert schemas **NC**. [DDS], pp. 64–66. |
| DAT-031 | `TestCase`, `EvalDataset`, `Scorecard`, `ReleaseGateResult`, signed fixture/test manifests | Frozen synthetic expected outcomes, evaluation scores, domain/statistical evidence, release-blocking results. | SCR-011; API-023/024. | Dataset files, evaluation tables, score types, statuses, and calculations **NC**. [DDS], pp. 74–76, 88–89. |
| DAT-032 | `ReleaseArtifact`, `ConfigVersion`, `MigrationPlan`, `RolloutGate`, release record | Reconstructible image/schema/prompt/routing versions, signed configuration, build and test attestation, migration/rollout compatibility. | `SCR-X-009`; API-043/044. | Artifact schemas, signatures, storage, and release state vocabulary **NC**. [DDS], pp. 71–73. |
| DAT-033 | `ChangeRequest`, `DesignRevision`, `RequirementLink`, `DecisionRecord` | Versioned design governance, impact scores, invariant-to-negative-test linkage, approved major/minor change evidence. | `SCR-X-008`; API-032/033. | Physical records, impact scales, approval schema, and relationships **NC**. [DDS], pp. 8–10. |
| DAT-034 | `ApiOperation`, `ErrorEnvelope`, `EventCursor`, `WebhookSubscription`, `A2ATaskEnvelope`, generated IDL | Versioned wire contracts, safe errors, SSE offsets, optional signed webhooks, typed A2A/MCP boundaries. | API-015/031/045–047; shared errors. | Persistence requirement, transport schemas, signatures, and full IDL **NC**. [DDS], pp. 41, 54–56, 84, 87. |
| DAT-035 | `ViewState`, `ReviewForm`, `EvidencePanel`, `Notification`, illustrated summary projections | Authorized screen data and accessible workflow summaries. Progress reconstructs from server state. | SCR-001–SCR-011; API-002/008/013/016; API-GAP-010. | No corresponding new tables or summary API confirmed. Projection formulas and persistent UI preferences **NC**. [DDS], pp. 7, 57–59. |
| DAT-036 | `EdgeGateway`, `CaseService`, `Orchestrator`, `RetrievalService`; `VirtualNetwork`, `APIReplicaSet`, `WorkerPool`, `RegionFailoverPlan`; `CapacityBudget`, `AdmissionPermit`, `RecoveryCheckpoint`, `LoadProfile` | Named architecture/runtime boundaries and capacity/recovery contract data. These names do not establish application tables. | `SCR-X-009`; API-030/034/035/042; shared service boundaries. | Application persistence, complete data schemas, owners, and scope **NC**. [DDS], pp. 15–20, 68–70. |

**Needs confirmation — OQ-DAT-001:** Complete the production data model, determine which supplementary terms map to existing datasets versus separate persisted records, and define exact datastore-writer identities. Component-register arrows are boundary illustrations, not confirmed entity cardinalities.

### Relationships and Cardinality

“Logical one-to-many” identifies a supported parent/child association. It does not supply minimum child count, physical `NOT NULL`, inverse reuse restrictions, or deletion cascades. Such details remain **Needs confirmation** unless explicitly stated.

| Relationship ID | Parent / referenced data | Child / referencing data | Cardinality and supported mapping | Integrity and unresolved details | Source |
|---|---|---|---|---|---|
| DAT-REL-001 | DAT-001 `tenants.id` | DAT-003 `cases.tenant_id` | Each stored case references exactly one tenant; tenant-to-case logical one-to-many. | Reference DDL supplies `UUID NOT NULL REFERENCES tenants(id)`. Tenant deletion action NC. | [DDS], p. 86, §B.2. |
| DAT-REL-002 | DAT-002 `workspaces.id` | DAT-003 `cases.workspace_id` | Each stored case references exactly one workspace; workspace-to-case logical one-to-many. | `UUID NOT NULL REFERENCES workspaces(id)`. Case tenant must match workspace tenancy; production enforcement method NC. | [DDS], pp. 24, 86. |
| DAT-REL-003 | DAT-001 tenant | DAT-002 `workspaces.tenant_id` | Workspace carries tenant scope; logical tenant-to-workspace one-to-many. | Physical FK, nullability, uniqueness, and root provisioning constraints NC. | [DDS], pp. 22, 85. |
| DAT-REL-004 | DAT-003 case | DAT-004 `case_revisions.case_id` | Case-to-revision logical one-to-many. | Append-only; per-case revision identity required logically. Composite PK/unique/FK design NC. | [DDS], pp. 25–26, 85. |
| DAT-REL-005 | DAT-003 case | DAT-020 attachment | Attachments are separate entities joined to a case by immutable identifiers. | Exact case-reference column, minimum/maximum attachment count, uniqueness, and attachment removal NC. | [DDS], pp. 12, 24. |
| DAT-REL-006 | DAT-006 immutable document version | DAT-020 attachment reference | An attachment references an immutable document version. | FK column, version reuse across attachments/cases, and cascade behavior NC. Never silently redirect to the latest version. | [DDS], p. 51, §14.1.2. |
| DAT-REL-007 | DAT-002 workspace | DAT-005 `documents.workspace_id` | Workspace-to-document logical one-to-many. | Physical FK/nullability and workspace-source uniqueness NC; ACL enforced separately. | [DDS], p. 85. |
| DAT-REL-008 | DAT-005 document | DAT-006 `document_versions.document_id` | Document-to-version logical one-to-many; side-by-side reprocessing supported. | Version identity and uniqueness tuple NC. Immutable version content. | [DDS], pp. 31, 85. |
| DAT-REL-009 | DAT-006 document version | DAT-007 `chunks.document_version_id` | Version-to-chunk logical one-to-many. | Resolvable source anchors required; physical FK, chunk ordering, and identity scheme NC. | [DDS], pp. 31, 85. |
| DAT-REL-010 | DAT-007 stored chunk/version | DAT-023 search row | Search row carries `document_version_id` and `chunk_id`. | Number of projections per chunk across index generations NC. Search is derivative, not authority. | [DDS], p. 34. |
| DAT-REL-011 | DAT-003 case | DAT-008 `runs.case_id` | Case-to-run logical one-to-many; case/run identifier association is immutable. | Physical FK/nullability and reopened/reworked revision linkage NC. | [DDS], pp. 24, 46, 85. |
| DAT-REL-012 | DAT-008 run | DAT-009 `run_steps.run_id` | Run-to-step logical one-to-many. | Step identity/idempotency and explicit dependencies required; PlanNode-to-step mapping and uniqueness NC. | [DDS], pp. 40–42, 85. |
| DAT-REL-013 | DAT-008 run | DAT-010 `evidence_sets.run_id` | Run-linked evidence sets exist. Number per run and optionality NC. | Standalone search without a run is supported as an API activity; storage mapping for such results NC. | [DDS], pp. 35, 83, 85, 87. |
| DAT-REL-014 | DAT-007 chunks | DAT-010 `chunk_refs` | An evidence set references selected chunks. | Collection representation, order, duplicates, minimum count, and cross-set reuse NC; all referenced content must remain version-resolvable and authorized. | [DDS], pp. 31, 35, 85. |
| DAT-REL-015 | DAT-008 run / DAT-025 exact artifact | DAT-011 `approval_tasks.run_id`, `artifact_hash` | Each task identifies a run and reviewed artifact binding. Task count per run NC. | Hash is not an arbitrary replaceable pointer. Physical reference and candidate-version constraints NC. | [DDS], pp. 44–46, 85. |
| DAT-REL-016 | DAT-011 task / DAT-019 reviewer | DAT-012 `task_id`, `reviewer_id` | Decision references task and reviewer. | Decision count, repeated/conflicting decisions, reassignment history, reviewer FK, and expiry races NC. Historical decisions immutable. | [DDS], pp. 45, 62, 85. |
| DAT-REL-017 | DAT-008 run / DAT-024 deployment | DAT-016 `run_id`, `deployment_id` | Usage is attributed to run and deployment. | One row per run, deployment, invocation, or retry is not established. Physical keys and accounting grain NC. | [DDS], pp. 38, 65, 85. |
| DAT-REL-018 | DAT-008 run / versioned policy | DAT-017 `run_id`, `rule_version` | Evaluation associated with run and rule version. | Evaluation count, evaluation-to-candidate/evidence binding, and FK schema NC. | [DDS], pp. 44, 85. |
| DAT-REL-019 | DAT-021 connector/sync run | DAT-015 cursor; per-run cursor/error ledger | Cursor references `connector_id`; every sync run stores cursor, high-watermark, and error ledger. | Source does not resolve connector-current cursor versus run-history storage or concurrency ownership. | [DDS], pp. 28–29, 85. |
| DAT-REL-020 | DAT-025 satisfied gate/artifact | DAT-003 current approved result; closure snapshot | Final pointer and satisfied gate commit atomically; closure snapshots artifact, cited versions, and decisions. | Pointer representation, snapshot identity, copy-versus-reference, and retention of deleted historical sources NC. | [DDS], pp. 24–26, 45–46. |
| DAT-REL-021 | Tenant and target aggregate | DAT-014 events / DAT-026 consumer ledger | Event identifies tenant, aggregate, and aggregate revision. | Exact ledger key/consumer identity, polymorphic reference validation, and retention NC. No cross-partition ordering assumption. | [DDS], pp. 48–50. |
| DAT-REL-022 | Tenant and inventoried object | DAT-018 receipt / DAT-029 hold or manifest | Receipt records tenant/object purge; protected objects remain retained and receipted. | Inventory granularity, receipt identity, legal-hold references, and workspace/tenant operation mapping NC. | [DDS], pp. 80, 85, 87, 89. |

**Needs confirmation — OQ-DAT-002:** Supply physical foreign keys, nullable associations, inverse reuse constraints, cardinality minima/maxima, and deletion behavior for all relationships not fully declared in §B.2. No `ON DELETE CASCADE` or automatic lineage deletion is approved.

## Data Field Definitions

### Field-Definition Rules

| Convention | Meaning |
|---|---|
| **Logical identifier** | UUIDv7 baseline where the source establishes application identifiers. Physical SQL type is NC except where reference DDL explicitly supplies it. External source IDs, opaque citations, provider cursors, trace IDs, and secret references are not automatically UUIDv7. |
| **Selected field** | Exact table/field name is confirmed by §B.1. Its physical type, length, precision, nullability, default, and key declaration remain NC unless another source defines them. |
| **Logical required** | Necessary to satisfy an explicit source invariant, such as decision actor/time/hash capture or event-envelope presence. It does not independently select a column or wire representation. |
| **Conditional required** | Required under an explicit condition, such as a reason code when correcting classification. |
| **Optional** | Source explicitly permits absence, such as a bounding box or reviewer annotations. Physical nullability remains NC unless specified. |
| **Key/reference** | A logical identity or association does not imply a declared physical PK/FK. Only the case reference DDL fully declares those constraints. |
| **Default NC** | No default is supplied. The implementation must not silently select one. This differs from the source-confirmed case defaults. |
| **Length/precision NC** | No application-level bound or numeric precision is supplied. Standard type names are preserved without creating additional business limits. |

**DAT-COM-002 — Shared identity, tenancy, and attribution fields.**

| Field ID | Exact name or source terminology | Meaning / type | Requiredness and physical design | Constraints | Source |
|---|---|---|---|---|---|
| DAT-COM-F01 | `tenant_id` | Tenant partition/security identity. `UUID` in case DDL; other physical declarations NC. | Required on every tenant-owned row. Exact treatment of root `tenants` and potentially shared registries NC. | Included in every storage access predicate; authenticated trusted context; immutable tenant identity in signed background envelopes. | [DDS], pp. 22, 48, 51, 86. |
| DAT-COM-F02 | `revision` | Resource version. Case physical `BIGINT`; other revisions NC. | Required at applicable durable state-changing boundaries. | Case revision is monotonic. Resource revision is not automatically policy version, plan revision, or stream offset. | [DDS], pp. 24–25; repeated boundary requirements pp. 8–80. |
| DAT-COM-F03 | `actor_id`; selected aliases `actor`, `reviewer_id` | Authenticated actor attribution. | Logically required at durable changes; alias equivalence and physical/wire type NC. | Do not trust a body-supplied identity as authority. Retain attribution without exposing unauthorized resources. | [DDS], pp. 22–23, 45, 85. |
| DAT-COM-F04 | `occurred_at`; selected aliases `at`, decision timestamp, `purge_time` | Durable action time. | Required at applicable boundaries; physical mapping and timestamp precision NC. | Server stores UTC; public timestamps RFC 3339. Alias semantics must be resolved, not presumed identical. | [DDS], pp. 25, 45, 48, 54, 59, 85. |
| DAT-COM-F05 | `trace_id`, `correlation_id` / correlation ID | Request and downstream correlation. | Every request carries trace and correlation context. Header/envelope/storage carriers and lengths NC. | Correlation crosses boundaries and remains independent of provider trace identifiers. No documents or secrets in diagnostic attributes. | [DDS], pp. 16, 48, 64. |
| DAT-COM-F06 | Source/revision fingerprint; component-register literal `SHA-256 source/ revision` | Integrity and immutable-derivative provenance. | Fingerprinting required where source establishes it; exact field mappings NC. | Do not assume every `hash`, `text_hash`, `digest`, `artifact_hash`, or checksum has identical input, algorithm, or encoding. | [DDS], pp. 10, 32, 39, 53. |

**Needs confirmation — OQ-DAT-003:** Complete exact scalar types, lengths, precision, mandatory/nullable properties, defaults, and IDL-to-storage mappings. The common requirements may require production columns omitted from the selected-field examples; their omission does not waive tenant scope or attribution.

### DAT-001 — Tenant Fields

**Source for selected names:** [DDS], p. 85, §B.1.  
**Shared gap:** OQ-DAT-003/OQ-DAT-004.

| Field ID | Physical/source name | Meaning and type | Nullability / requiredness / default | Keys, uniqueness, values | Earlier mapping |
|---|---|---|---|---|---|
| DAT-001-F01 | `id` | Tenant identity; logical UUIDv7. Case FK requires UUID-compatible referenced identity; tenant column DDL NC. | Logical identity required; physical nullability/default NC. | Root identity; physical PK declaration NC. | Trusted tenant context in API shared parameters. |
| DAT-001-F02 | `slug` | Tenant business key; exact string type/length NC. | Selected field; requiredness/default NC. | Source explicitly states `unique(slug)`. Case sensitivity, normalization, permitted characters, and rename/reuse rules NC. | No confirmed editable tenant field. |
| DAT-001-F03 | `plan` | Tenant plan reference/code; type and vocabulary NC. | Selected field; nullability/default NC. | Plan-to-quota behavior not defined. | No confirmed public plan property. |
| DAT-001-F04 | `region` | Tenant region designation; type/code system NC. | Selected field; nullability/default NC. | Actual approved cloud region remains unresolved; no default region selected. | `OQ-SCR-030`, `OQ-API-034`. |
| DAT-001-F05 | `created_at` | Tenant creation time; physical type/precision NC. | Selected field; default NC. | UTC/RFC 3339 conventions apply where exposed. | Principal/provisioning projection NC. |

**Needs confirmation — OQ-DAT-004:** Define tenant slug scope and normalization, plan/region code systems, root-tenant constraints, and provisioning semantics. The generic tenant/business-key uniqueness rule must not silently replace explicit `unique(slug)`.

### DAT-002 — Workspace Fields and Settings

**Sources:** [DDS], pp. 24–25, §6.1.1 and §6.3.1; pp. 78, 85.  
**Shared gap:** OQ-DAT-003/OQ-DAT-005.

| Field ID | Physical/source name | Meaning and type | Nullability / requiredness / default | Keys, constraints, values | Earlier mapping |
|---|---|---|---|---|---|
| DAT-002-F01 | `id` | Workspace identity; logical UUIDv7; physical DDL NC. | Logical identity required; physical default NC. | Referenced by `cases.workspace_id`; exact workspace PK NC. | API `workspaceId`; shared workspace context. |
| DAT-002-F02 | `tenant_id` | Workspace tenant scope. | Logical required; physical type/nullability/default NC. | RLS tenant scope; workspace must not be linked to a foreign tenant’s case. | API shared tenant/workspace parameters. |
| DAT-002-F03 | `policy_version` | Workspace policy-version reference; type/format NC. | Selected field; nullability/default NC. | Relationship to configuration revision and `rule_version` NC. | SCR-007-F01/F11; API policy data catalog. |
| DAT-002-F04 | `quota` | Workspace quota configuration; structure/units/precision NC. | Selected field; requiredness/default NC. | Run/token admission uses configured quota; quota windows and limits NC. | SCR-007-F10; SCR-010-F02; API-PROC-020. |
| DAT-002-F05 | Physical name NC — retention class | Retention-policy code/reference; type/vocabulary NC. | Setting confirmed; default and nullable form contract NC. | Closed-case eligibility and legal-hold exceptions apply. | SCR-007-F02. |
| DAT-002-F06 | Physical name NC — allowed models/deployments | Collection of deployment references; storage and count NC. | Setting confirmed; default NC. | Allowlist specific deployments, not broad provider brands. | SCR-007-F03; API-020/OQ-API-020. |
| DAT-002-F07 | Physical name NC — connector credential references | Workspace-scoped vault references; type/length NC. | Setting confirmed; nullability/default NC. | Store references in application configuration, not raw credential material. | SCR-007-F04; SCR-006-F04. |
| DAT-002-F08 | Physical name NC — approved toolsets | Version-pinned approved capability references; structure NC. | Setting confirmed; default NC. | Discovery is not authorization; arbitrary browser tool definitions forbidden. | SCR-007-F05; API-045/046. |
| DAT-002-F09 | Physical name NC — reviewer routing | Reviewer pools, minimum role, separation-of-duty and expiry/escalation policy; schema NC. | Setting confirmed; durations/defaults NC. | No implicit approval on expiry; no unapproved self-approval bypass. | SCR-007-F06–F08; API-016/017. |
| DAT-002-F10 | Physical name NC — workspace timezone/business calendar | Calendar and timezone references; identifier system NC. | Business-rule configuration required; physical storage/default NC. | Compute contractual deadlines using workspace timezone; display locale cannot change them. | SCR-007-F09; SCR-002-F24; API-CASE-F18. |
| DAT-002-F11 | Physical name NC — workspace display name | Illustrated workspace label; type/length NC. | Illustration confirms display only; persisted property/default NC. | `Meridian Manufacturing` is fictional data, not a seed value. | SCR-COM-F01. |

**Needs confirmation — OQ-DAT-005:** Define workspace settings storage, policy/configuration revision distinctions, activation and precedence, complete quota/calendar schemas, and the actual policy read/write API. Do not bind these fields to case PATCH solely from §6.1.1.

### DAT-003 — Case Fields

The first nine rows are covered by the reference DDL. Additional case data is confirmed by domain prose, but its physical columns are unresolved.

| Field ID | Physical/source name | Meaning and type / length / precision | Nullability / requiredness / default | PK/FK/uniqueness, values, constraints | Earlier mapping and source |
|---|---|---|---|---|---|
| DAT-003-F01 | `id` | `UUID`; UUIDv7 identifier baseline. | PK, therefore non-null; server identity. DDL generation default not supplied. | `PRIMARY KEY`; also `UNIQUE (tenant_id, id)`. Illustrated business-number mapping NC. | SCR-002-F01; SCR-001-F01; API-CASE-F01. [DDS], pp. 51, 86. |
| DAT-003-F02 | `tenant_id` | `UUID`. | `NOT NULL`; no DDL default. | `REFERENCES tenants(id)`; RLS predicate. | API-CASE-F02. [DDS], p. 86. |
| DAT-003-F03 | `workspace_id` | `UUID`. | `NOT NULL`; no DDL default. | `REFERENCES workspaces(id)`; additional workspace-tenancy enforcement required. | API-CASE-F03. [DDS], p. 86. |
| DAT-003-F04 | `status` | `TEXT`; no declared application length. | `NOT NULL`; no DDL default. Case creation begins `NEW`. | DDL `CHECK` contains DAT-CODE-001 values. Valid transition guards also apply. | SCR-002-F08; API-CASE-F10. [DDS], pp. 12, 25, 82, 86. |
| DAT-003-F05 | `revision` | `BIGINT`; additional application precision/range NC. | `NOT NULL DEFAULT 1`. | Monotonic case revision; no revision upper limit or increment implementation supplied. | SCR-002-F10; API-CASE-F12. [DDS], pp. 25, 86. |
| DAT-003-F06 | `sensitivity` | `TEXT`; information classes DAT-CODE-005. | `NOT NULL DEFAULT 'INTERNAL'`. | Reference DDL does **not** include a sensitivity `CHECK`. Domain class validation remains required. | SCR-002-F07; API-CASE-F09. [DDS], pp. 62, 86. |
| DAT-003-F07 | `created_at` | `TIMESTAMPTZ`; timestamp precision NC. | `NOT NULL DEFAULT now()`. | UTC storage and RFC 3339 public representation. | SCR-002-F12; API-CASE-F14. [DDS], pp. 54, 59, 86. |
| DAT-003-F08 | `updated_at` | `TIMESTAMPTZ`; timestamp precision NC. | `NOT NULL DEFAULT now()`. | Initial default confirmed; update trigger/application-maintenance mechanism NC. | SCR-002-F13; API-CASE-F15. [DDS], p. 86. |
| DAT-003-F09 | Constraint tuple `(tenant_id, id)` | Tenant-qualified case identity. | Both member fields non-null. | Exact source `UNIQUE (tenant_id, id)`; global `id` PK also remains in reference DDL. | API-CASE-F01/F02. [DDS], p. 86. |
| DAT-003-F10 | Physical name NC — title | Business subject; type/length/characters NC. | Case stores title; POST/PATCH requiredness/nullability/default NC. | Editable field set and text normalization NC. | SCR-001-F02; SCR-002-F02; API-CASE-F04. [DDS], p. 24. |
| DAT-003-F11 | Physical name NC — description | Business context; text/markup type and length NC. | Stored datum confirmed; request requiredness/default NC. | Do not infer rich text or Markdown support. | SCR-002-F03; API-CASE-F05. [DDS], pp. 12, 24. |
| DAT-003-F12 | Physical name NC — impact | Explicit business priority input; type/vocabulary/range NC. | Input concept confirmed; creation/update requiredness/default NC. | Priority must not derive from model output alone. | SCR-002-F04; API-CASE-F06. [DDS], p. 25. |
| DAT-003-F13 | Physical name NC — urgency | Explicit business priority input; type/vocabulary/range NC. | Requiredness/default NC. | Combined with impact through an unresolved deterministic formula. | SCR-002-F05; API-CASE-F07. [DDS], p. 25. |
| DAT-003-F14 | Physical name NC — priority | Derived business value; type/code system NC. | Stored datum confirmed; initial formula and nullability NC. | Direct client editing is not confirmed. | SCR-002-F06; API-CASE-F08. [DDS], pp. 24–25. |
| DAT-003-F15 | Physical name NC — owner | Case-owner relationship; identifier type NC. | Stored datum confirmed; assignment/default/reassignment NC. | `Owner` API authorization predicate is unresolved as role versus relationship. | SCR-002-F09; API-CASE-F11; API-004. [DDS], pp. 24, 83. |
| DAT-003-F16 | Physical name NC — current approved result / final response pointer | Artifact reference or pointer; structure NC. | Stored datum confirmed; prepublication nullability NC. | Update only with satisfied gate in same transaction; closed lineage preserved. | SCR-002-F11; API-CASE-F13. [DDS], pp. 24, 45–46. |
| DAT-003-F17 | Physical name NC — SLA deadline | Business-calendar result; timestamp/data representation NC. | Derivation/nullability/default NC. | Advisory breach prediction cannot alter contractual deadline. | SCR-002-F24; API-CASE-F18. [DDS], p. 25. |
| DAT-003-F18 | Physical name NC — displayed business number | Illustration-only case reference, such as `OD-2026-1042`. | Persistence, requiredness, generation, and default NC. | No confirmed mask, sequence, uniqueness scope, or relationship to UUID. | SCR-001-F01; OQ-SCR-006/OQ-API-007. [DDS], pp. 7, 14. |

**Needs confirmation — OQ-DAT-006:** Complete case field storage and wire mapping, business-number identity, owner relationship, priority/SLA rules, and creation/edit requiredness. The reference DDL is not a complete case schema.

#### Confirmed Reference DDL

The following reproduces the source reference; it is not a complete production migration.

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

**Source:** [DDS], p. 86, §B.2.

**DAT-COM-003 — Production completion of the reference.** Production DDL must additionally enforce workspace-tenancy membership through foreign keys or controlled write procedures. The database pool must reset scoped session variables after every transaction. The choice of enforcement mechanism, complete write policies, privileged-role treatment, and missing-context behavior remain OQ-DAT-002/OQ-DAT-014; no new SQL policy or index is selected here.

### DAT-004 — Case Revision Fields

**Sources:** [DDS], pp. 25–26, §6.2 and §6.3.2; p. 85, §B.1.

| Field ID | Physical/source name | Meaning / type | Nullability / requiredness / default | Keys and constraints | Earlier mapping |
|---|---|---|---|---|---|
| DAT-004-F01 | `case_id` | Parent case identifier; logical UUIDv7 reference; physical type NC. | Association logically required for case history; physical `NOT NULL`/default NC. | Physical FK and tenant-qualified reference NC. | SCR-002 history; API-004/005. |
| DAT-004-F02 | `revision` | Recorded case revision; physical type NC, despite current case `BIGINT`. | Logical required to identify revision history; default NC. | Append-only; exact PK/unique tuple and gap/increment rules NC. | SCR-002-F10; API-CASE-F12. |
| DAT-004-F03 | `patch` | Recorded change content; structure/encoding/type NC. | Selected field; requiredness/default NC. | Not a confirmed JSON Patch, Merge Patch, or `JSONB` column. | API-004/OQ-API-005. |
| DAT-004-F04 | `actor` | Change actor attribution; type NC. | Durable attribution required; physical default NC. | Mapping to `actor_id`/Principal NC. | DAT-COM-F03. |
| DAT-004-F05 | `at` | Revision-record time; type/precision NC. | Durable occurrence-time capture required; default NC. | Mapping to `occurred_at` versus commit time NC; UTC conventions apply. | DAT-COM-F04. |

**Needs confirmation — OQ-DAT-007:** Define revision keys, patch representation, actor/time aliases, reconstruction semantics, closure snapshot placement, reopening/new-run linkage, and eligible-history retention.

### DAT-005–DAT-007 — Document, Version, and Chunk Fields

**Sources for selected names:** [DDS], p. 85, §B.1. Additional requirements: pp. 30–35 and 51–52.

| Field ID | Physical/source name | Meaning / type | Nullability / requiredness / default | Keys, constraints, values | Earlier mapping / additional evidence |
|---|---|---|---|---|---|
| DAT-005-F01 | `documents.id` | Document identity; logical UUIDv7; physical type NC. | Logical identity required; physical default NC. | PK declaration NC. | API `documentId`; SCR-002 attachment status. |
| DAT-005-F02 | `documents.workspace_id` | Workspace association; identifier type NC. | Selected association; physical nullability/default NC. | Tenant/workspace scope and ACL required; physical FK NC. | SCR-003-F02; API-006–010. |
| DAT-005-F03 | `documents.source_id` | Stable originating repository identity; type/length NC. | Selected field; upload-source handling/nullability/default NC. | Preserve stable IDs during backfill. Provider namespace, uniqueness, rename/delete/recreate semantics NC. | SCR-006-F01; API-049. [DDS], pp. 27, 78. |
| DAT-005-F04 | `documents.sensitivity` | Document information class; type NC. | Selected field; default and nullability NC. | DAT-CODE-005; case default `INTERNAL` does not establish document default. | SCR-003 evidence class; API search-index classification. [DDS], p. 62. |
| DAT-005-F05 | Physical name NC — originating ACL and revision | Source permission authority and version; schema NC. | Logically required for ACL-enforced retrieval. | Must support revocation before next retrieval; digest alone is not access authority. | API-EVID-F05; DAT-019. [DDS], pp. 21–23, 27–29. |
| DAT-005-F06 | Physical name NC — document lifecycle state | Document processing outcome; type NC. | Authoritative state required for status API; storage placement NC. | DAT-CODE-003; do not assume `documents.status` exists. | SCR-002-F20; API-007. [DDS], p. 82. |
| DAT-006-F01 | Physical name NC — document-version identity | Immutable version ID referenced by chunks/attachments; logical identifier baseline. | Logical identity required; physical PK/default NC. | §B.1 does not list an `id` column for this table. Exact identity design NC. | API-EVID-F03; SCR-003-F05. |
| DAT-006-F02 | `document_versions.document_id` | Parent document reference; type NC. | Association confirmed; physical nullability/default NC. | Physical FK and delete behavior NC. | DAT-REL-008. |
| DAT-006-F03 | `document_versions.hash` | Source/content fingerprint; algorithm input/encoding/type NC. | Stored immutable fingerprint confirmed; default NC. | Fingerprint plus pipeline version produces immutable derivatives; canonical input and uniqueness NC. | SCR-003-F08; API-EVID-F07. [DDS], p. 31. |
| DAT-006-F04 | `document_versions.parser_version` | Parser-version reference; type/length NC. | Selected field; physical nullability/default NC. | Relationship to wider normalization/pipeline version NC. Changed processing can coexist side by side. | API-006 normalization data. [DDS], p. 31. |
| DAT-006-F05 | `document_versions.object_key` | Private object locator; type/length NC. | Selected field; number of object roles/keys and nullability NC. | Includes scope dimensions under DAT-028; public names opaque; not a public unrestricted URL. | API-039; SCR-003 source access. [DDS], p. 52. |
| DAT-006-F06 | Physical name NC — normalized text/layout/metadata derivative references | Immutable conversion outputs; formats/types NC. | Required outputs according to pipeline; individual presence/defaults NC. | Normalization strips transport artifacts without rewriting claims. | SCR-003-F10; API-PROC-003. [DDS], pp. 30–31. |
| DAT-007-F01 | `chunks.id` | Stored chunk identity; logical identifier baseline; physical type NC. | Logical identity required; physical default NC. | Mapping to search `chunk_id` and opaque citation/evidence IDs NC. | API-EVID-F01; SCR-003-F03. |
| DAT-007-F02 | `chunks.document_version_id` | Immutable version association; type NC. | Logical association required for provenance; physical nullability/default NC. | Resolvable version reference; physical FK NC. | SCR-003-F05; API-EVID-F03. |
| DAT-007-F03 | `chunks.page` | Stored source page anchor/number; numeric or structured type NC. | Every chunk stores page number logically; physical nullability/default NC. | Zero/one-based numbering and non-PDF page semantics NC. | SCR-003-F06; API-EVID-F08. [DDS], p. 31. |
| DAT-007-F04 | `chunks.bbox` | Optional bounding box; shape, numeric precision, coordinates/units NC. | **Optional** logically; physical nullability/default NC. | Must locate the correct cited page/block. | SCR-003-F09; API-EVID-F09. [DDS], p. 31. |
| DAT-007-F05 | `chunks.text_hash` | Text fingerprint; algorithm/canonicalization/encoding/type NC. | Selected field; nullability/default NC. | Distinct from file hash until mapping resolved. | Evidence integrity; API-EVID-F07 is not automatically the same field. |
| DAT-007-F06 | Physical name NC — source URI | Stored originating source reference; URI scheme/length NC. | Every chunk stores it logically. | No arbitrary browsing or network authority from this value. | SCR-003-F07; API-EVID-F06. [DDS], pp. 31, 87. |
| DAT-007-F07 | Physical name NC — file hash | Immutable source fingerprint associated with chunk. | Every chunk stores it logically; column/reference realization NC. | Must preserve source identity; not automatically `text_hash`. | SCR-003-F08; API-EVID-F07. [DDS], p. 31. |
| DAT-007-F08 | Physical name NC — page range/anchor | Resolvable citation target including displayed anchored range; schema NC. | Cited evidence requires resolvable anchor. | Relationship to `page`, `bbox`, block IDs, and citation highlight NC. | SCR-COM-006; API-EVID-F04. [DDS], pp. 35, 57. |

**Needs confirmation — OQ-DAT-008:** Define source/version/chunk identities, stable-source namespaces, parser-versus-pipeline version, immutable derivative uniqueness, document-state storage, and source-delete behavior.

**Needs confirmation — OQ-DAT-009:** Define page/anchor/range/bounding-box schemas, non-PDF anchors, all fingerprint/hash mappings, and the formal `Citation` structure. Do not assume UUIDv7 identifiers are directly derived from hash bytes.

### DAT-008–DAT-009 — Run and Step Fields

**Sources:** [DDS], pp. 40–42, 49, 58, 82, 85.

| Field ID | Physical/source name | Meaning / type | Nullability / requiredness / default | Keys, constraints, values | Earlier mapping |
|---|---|---|---|---|---|
| DAT-008-F01 | `runs.id` | Run identity; logical UUIDv7; physical type NC. | Logical identity required; allocation default NC. | Physical PK NC. | SCR-004-F01; API-011–013. |
| DAT-008-F02 | `runs.case_id` | Case association; type NC. | Association confirmed; physical nullability/default NC. | Immutable ID linkage; case-revision binding NC. | SCR-004-F02; API run data. |
| DAT-008-F03 | `runs.status` | Authoritative workflow state; physical type NC. | State required for durable progress; physical default NC. | DAT-CODE-002; creation/request progression supported. | SCR-004-F03; API-013. |
| DAT-008-F04 | `runs.plan_revision` | Stored plan version; type/range NC. | Must be stored before side effects. | Not interchangeable with case revision or SSE offset. | SCR-004-F06; API run data. |
| DAT-008-F05 | `runs.budget` | Runtime/call/token budget; structure and units NC. | Bounded budget required; allocation/default NC. | Depth eight and maximum sixteen tool invocations; reserved input/output token budget and workspace quota. | SCR-004-F07; API-PROC-021/026. |
| DAT-008-F06 | Physical name NC — DAG/dependencies | Directed acyclic execution plan; schema NC. | Explicit dependencies required. | Cycle rejection, depth counting, retry/tool-call accounting NC; no graphical editor implied. | SCR-004; API run plan data. |
| DAT-008-F07 | Physical name NC — failed checkpoint/cause | Safe checkpoint-specific failure. | Required when a checkpoint fails; nullability outside failure NC. | Report exact failed checkpoint without secrets/document text. | SCR-004-F08; API failure contract. |
| DAT-008-F08 | Physical name NC — rework/new-run revision relationship | Lineage from denied candidate to new run revision. | Required to preserve supported rework lineage; schema NC. | No retroactive approval of old denied content. | SCR-002-A11; API-GAP-005. |
| DAT-009-F01 | `run_steps.id` | Step identity; logical identifier baseline; physical type NC. | Logical identity required; default NC. | Physical PK and operation-key relation NC. | SCR-004-F04. |
| DAT-009-F02 | `run_steps.run_id` | Parent run reference; type NC. | Association confirmed; physical nullability/default NC. | Physical FK NC. | API-014. |
| DAT-009-F03 | `run_steps.step_kind` | Step classification; type/enumeration NC. | Selected field; requiredness/default NC. | Do not invent an enum from agent names. | SCR-004-F04. |
| DAT-009-F04 | `run_steps.status` | Step outcome/progress; type/enumeration NC. | Selected field; requiredness/default NC. | Not automatically the run status vocabulary. | SCR-004-F04. |
| DAT-009-F05 | `run_steps.checkpoint` | Replayable continuation/result evidence; schema/type NC. | Checkpoint persisted before downstream dispatch. | Idempotent step; replacement versus checkpoint history NC. | SCR-004-F05; API-014/037. |

**Needs confirmation — OQ-DAT-015:** Complete run/step states, creation defaults, run/case revision linkage, DAG/checkpoint schemas, budgets, missing-approval versus waiting semantics, and recoverable timeout representation. `run_timeout_seconds: 180` is an example, not a reviewer SLA or a newly approved persisted timeout field.

### DAT-010 — Evidence-Set and Citation Fields

**Sources:** [DDS], pp. 31, 35–36, 85, 87.

| Field ID | Physical/source name | Meaning / type | Nullability / requiredness / default | Keys and constraints | Earlier mapping |
|---|---|---|---|---|---|
| DAT-010-F01 | `evidence_sets.id`; MCP `evidence_set_id` | Evidence-set identity. MCP type `uuid`; physical SQL type NC. | Stored identity confirmed; MCP listed output. Formal wire nullability/default NC. | Physical PK; mapping to public `evidenceId` NC. | API-EVID-F13; API-045. |
| DAT-010-F02 | `evidence_sets.run_id` | Associated run; type NC. | Selected field; physical nullability/default NC. | Standalone search persistence without run NC. | API-009/013/045. |
| DAT-010-F03 | `evidence_sets.chunk_refs` | Selected chunk-reference collection; type/order/count NC. | Selected field; requiredness/default NC. | Publication validates references; no array/JSON/junction-table choice selected. | SCR-004-F09; API evidence metadata. |
| DAT-010-F04 | `evidence_sets.acl_digest` | ACL validation digest; encoding/input scope NC. | Selected field; requiredness/default NC. | Relationship to each evidence item’s ACL digest NC. Current permission remains authoritative. | API-EVID-F05; SCR-003-F11. |
| DAT-010-F05 | Citation identifier; physical name NC | Opaque user-facing citation reference; type/length NC. | Cited items require verified identifiers; persistence/wire requiredness NC. | Do not expose a client-editable authorization token or infer equivalence to chunk/set ID. | API-EVID-F10; SCR-003-F03. |
| DAT-010-F06 | Source title; physical name NC | Authorized evidence item title; type/length NC. | Included in every response evidence item. | Storage/reference projection NC. | API-EVID-F02; SCR-003-F04. |
| DAT-010-F07 | Document revision; physical name NC | Immutable cited version reference; type NC. | Included in every response evidence item. | Must not substitute latest version. | API-EVID-F03; SCR-003-F05. |
| DAT-010-F08 | Page anchor; physical name NC | Resolvable source target; schema NC. | Included in every response evidence item. | See DAT-007-F03/F04/F08. | API-EVID-F04; SCR-003-F06. |
| DAT-010-F09 | MCP `citations` | Citation collection; exact source type `Citation[]`. | Listed output; formal requiredness/nullability/minimum count/default NC. | `Citation` definition absent. | API-045; API-EVID content catalog. |
| DAT-010-F10 | Reduced-quality retrieval flag; name NC | Result-quality indicator; type NC. | Required visible condition when permitted lexical-only degraded search continues. | Stored versus response-only realization NC. | API-EVID-F12; SCR-003-F14. |

**Needs confirmation — OQ-DAT-009/OQ-DAT-011:** Resolve evidence/citation identity, per-item versus set digests, persistence of standalone search, reference collection structure, and degraded-result fields.

### DAT-011–DAT-012 — Approval Task and Decision Fields

**Sources:** [DDS], pp. 44–46, 58, 62, 82, 85.

| Field ID | Physical/source name | Meaning / type | Nullability / requiredness / default | Keys, constraints, values | Earlier mapping |
|---|---|---|---|---|---|
| DAT-011-F01 | `approval_tasks.id` | Review-task identity; logical UUIDv7; physical type NC. | Logical identity required; default NC. | Physical PK; API `approvalId` mapping NC. | SCR-005-F01; API-017/OQ-API-015. |
| DAT-011-F02 | `approval_tasks.run_id` | Associated run; type NC. | Association confirmed; physical nullability/default NC. | Physical FK and task count/run NC. | SCR-005-F02. |
| DAT-011-F03 | `approval_tasks.reviewer_pool` | Policy-defined reviewer pool; reference/type/vocabulary NC. | Selected field; requiredness/default NC. | Pool/minimum role/separation of duties enforced; assignment selection schema NC. | SCR-005-F03/F04; API-016. |
| DAT-011-F04 | `approval_tasks.artifact_hash` | Exact candidate hash binding; algorithm/input/encoding/type NC. | Hash binding logically required. | Changed content makes prior decision stale; no self-approval as catalog constraint, broader scope unresolved. | SCR-005-F08; API decision binding. |
| DAT-011-F05 | Physical name NC — review state | Task state; physical type NC. | Authoritative review state required; default NC. | DAT-CODE-004; not a request decision enum. | SCR-005-F05. |
| DAT-011-F06 | Physical name NC — assignment/minimum role/separation rules | Review authorization context; schema NC. | Required policy controls; fields/defaults NC. | Do not infer authorization from user-selected pool or role. | SCR-005-F03/F04. |
| DAT-011-F07 | Physical name NC — expiry/SLA | Configured deadline/duration; units/time precision NC. | Task expiry required; default duration NC. | Expire then reassign/escalate, never auto-approve. | SCR-005-F06; API-PROC-027. |
| DAT-012-F01 | `approval_decisions.id` | Immutable decision identity; logical UUIDv7; physical type NC. | Logical identity required; default NC. | Physical PK and duplicate-decision key NC. | API-017; SCR-005 decision result. |
| DAT-012-F02 | `approval_decisions.task_id` | Target review-task reference; type NC. | Association confirmed; physical nullability/default NC. | FK and `approvalId` mapping NC. | SCR-005-F01/F02. |
| DAT-012-F03 | `approval_decisions.reviewer_id` | Authenticated decision actor; type NC. | Actor logically required in decision record. | Reviewer/Principal reference and segregation constraints; not a request actor override. | SCR-005-F16; DAT-COM-F03. |
| DAT-012-F04 | `approval_decisions.decision` | Captured approve/reject decision; type/request enum NC. | Decision capture logically required; no preselected default. | `APPROVED`/`REJECTED` are review states, not confirmed request literals. | SCR-005-F13; API-017. |
| DAT-012-F05 | `approval_decisions.reason` | Rationale; text type/length NC. | Rationale belongs in record; nonblank/request-requiredness/default NC. | Mapping to public `rationale` remains unapproved. | SCR-005-F14; P-API-002. |
| DAT-012-F06 | Physical name NC — decision timestamp | Recorded decision time; physical type/precision NC. | Logically required. | Immutable UTC evidence; RFC 3339 public convention. | SCR-005-F17. |
| DAT-012-F07 | Physical name NC — evaluated artifact hash | Exact content reviewed; type/algorithm/encoding NC. | Logically required in approval record, despite omission from §B.1 decision fields. | Bind decision to exact artifact; do not retain only a replaceable current task pointer. | SCR-005-F08; API decision binding. |
| DAT-012-F08 | Physical name NC — annotations | Reviewer annotations; format/count/length NC. | **Optional** logically; physical nullability/default NC. | Redaction and relation to artifact/source anchors NC. | SCR-005-F15. |
| DAT-012-F09 | Physical name NC — override evidence | Elevated role, secondary reviewer, and audited reason; schema NC. | Required only for an authorized override. | No retroactive editing of denied decision. | SCR-005-A07; API-GAP-006. |

**Needs confirmation — OQ-DAT-016:** Define task/assignment/decision identities and physical bindings, required review fields, rationale/annotations, expiry/race rules, reviewer pools, self-approval scope, secondary-review evidence, and immutable decision storage.

### DAT-013–DAT-014 — Audit and Outbox Fields

**Sources:** [DDS], pp. 23, 48–52, 62, 64, 85.

| Field ID | Physical/source name | Meaning / type | Nullability / requiredness / default | Keys and constraints | Earlier mapping |
|---|---|---|---|---|---|
| DAT-013-F01 | `audit_events.id` | Audit identity; logical UUIDv7; physical type NC. | Logical identity required; default NC. | Physical PK NC; append-only. | SCR-008-F01. |
| DAT-013-F02 | `audit_events.tenant_id` | Tenant scope. | Required on tenant-owned audit record; physical type/default NC. | Authorized tenant/redacted scope. | SCR-008-F02. |
| DAT-013-F03 | `audit_events.actor_id` | Action principal; type NC. | Durable actor capture required. | Denials retain principal and denied resource class without revealing private existence. | SCR-008-F03/F10. |
| DAT-013-F04 | `audit_events.action` | Action/event category; type/code system NC. | Selected field; physical requiredness/default NC. | Exact action-to-event-name mapping NC. | SCR-008-F04. |
| DAT-013-F05 | `audit_events.digest` | Integrity digest; algorithm/input/encoding/type NC. | Selected field; physical requiredness/default NC. | Append-only ledger chained with batch hashes; independent retention export. | SCR-008-F05. |
| DAT-013-F06 | Physical names NC — occurrence/trace/correlation | Audit chronology and request lineage. | Required applicable attribution; column names/types/defaults NC. | No full documents/API secrets in diagnostics. | SCR-008-F06/F07. |
| DAT-013-F07 | Physical names NC — decision metadata, prompt-template digests, access events | Authorized auditor evidence. | Content scope confirmed; individual projection/persistence fields NC. | Redacted content; historical review decisions not editable. | SCR-008-F08–F11. |
| DAT-014-F01 | `outbox_events.event_id` | Event identity; logical UUIDv7; physical type NC. | Event identity required; default NC. | Deduplication identity; physical PK/unique scope NC. | API-COM-006. |
| DAT-014-F02 | `outbox_events.tenant_id` | Immutable event tenant. | Logically required; physical type/default NC. | Signed background scope and tenant predicates. | API-COM-006. |
| DAT-014-F03 | `outbox_events.aggregate_revision` | Target aggregate version; physical numeric/string type NC. | Logically required. | Detect stale delivery; not automatically same SQL type as case revision. | API-COM-006; API-PROC-018. |
| DAT-014-F04 | `outbox_events.payload` | Versioned event content; physical type/schema NC. | Logically required. | Validate before mutation; do not infer `JSONB`. | API event inventory. |
| DAT-014-F05 | Event `type`, `schema_version`, `aggregate_id`, `occurred_at`, `trace_id` | Additional mandatory envelope content. | Required in events; outbox column versus serialized/linked representation NC. | Full envelope defined below; actor/correlation carrier still unresolved. | API-COM-006/OQ-API-035. |

**Needs confirmation — OQ-DAT-013:** Define outbox PK, consumer ledger, delivery metadata, event schemas/signatures, actor/correlation carriers, and retention. No `published_at`, retry-count column, or status enum is confirmed solely from the outbox pattern.

### DAT-015–DAT-018 — Cursor, Token, Policy, and Receipt Fields

**Source for selected names:** [DDS], p. 85, §B.1. Additional requirements: pp. 28–29, 38, 44–46, 65–66, 80.

| Field ID | Physical/source name | Meaning / type | Nullability / requiredness / default | Keys, values, constraints | Earlier mapping |
|---|---|---|---|---|---|
| DAT-015-F01 | `connector_cursors.connector_id` | Connector reference; identifier type NC. | Selected association; physical requiredness/default NC. | FK/PK and per-sync-run history reference NC. | SCR-006-F01; API-018/019. |
| DAT-015-F02 | `connector_cursors.cursor` | Provider-specific continuation token; type/length NC. | Each sync run stores cursor; initial/no-cursor behavior NC. | Advance only after all preceding items have durable outcomes. | SCR-006-F07. |
| DAT-015-F03 | `connector_cursors.watermark` | Provider high-watermark; type/order semantics NC. | Each sync run stores high-watermark; default NC. | Mapping to prose “high-watermark” confirmed conceptually, exact representation NC. | SCR-006-F08. |
| DAT-015-F04 | `connector_cursors.retry_state` | Durable retry/checkpoint state; structure NC. | Selected field; default/nullability NC. | Relationship to per-run error ledger NC. | SCR-006-F09; API connector data. |
| DAT-015-F05 | Physical names NC — error ledger/reason/correlation/remediation | Per-item durable exceptions and poison-record outcome. | Error ledger required per sync run; quarantine details required on malformed-record quarantine. | Bounded retry before quarantine; reason vocabulary/count/length NC. | SCR-006-F09–F12. |
| DAT-016-F01 | `token_ledger.run_id` | Run attribution; type NC. | Association required logically; physical default NC. | FK and ledger grain NC. | SCR-010-F09; API-036. |
| DAT-016-F02 | `token_ledger.deployment_id` | Actual deployment reference; type NC. | Attribution confirmed; physical requiredness/default NC. | Deployment version must be attributable; field/version mapping NC. | SCR-010-F08. |
| DAT-016-F03 | `token_ledger.in_tokens` | Provider input token use; numeric type/precision NC. | Tracked usage required; initial/missing-provider usage behavior NC. | Reservation versus actual use and failed/retried billing NC. | SCR-010-F09. |
| DAT-016-F04 | `token_ledger.out_tokens` | Provider output token use; numeric type/precision NC. | Tracked usage required; default NC. | No selected integer width, rounding, or count ceiling. | SCR-010-F09. |
| DAT-016-F05 | Physical names NC — reserved input/output budget and workspace cost center | Budget reservation and cost attribution; schema NC. | Required accounting concepts; storage/default NC. | Quota exhaustion terminal for current run; no automatic class/model change. | SCR-004-F07; SCR-010-F07. |
| DAT-017-F01 | `policy_evaluations.run_id` | Evaluated run; type NC. | Association confirmed; physical nullability/default NC. | Physical FK and evaluation count/run NC. | SCR-005-F02. |
| DAT-017-F02 | `policy_evaluations.rule_version` | Evaluated deterministic rule-set version; type/format NC. | Rule version stored with normalized inputs. | Not automatically workspace `policy_version` or configuration revision. | SCR-007-F11; SCR-005-F18. |
| DAT-017-F03 | `policy_evaluations.input_digest` | Normalized-input fingerprint; algorithm/input/encoding NC. | Selected field; physical requiredness/default NC. | Digest does not replace requirement to store normalized inputs. | SCR-005-F18. |
| DAT-017-F04 | `policy_evaluations.result` | Deterministic policy outcome; physical type NC. | Evaluation result required; default NC. | DAT-CODE-006; LLM risk tags cannot override it. | SCR-002-F30; SCR-005-F12. |
| DAT-017-F05 | Physical names NC — normalized rule inputs | Sensitivity, requested action, evidence quality, model class, financial impact category, confidence bands; individual schemas NC. | All evaluated inputs normalized and stored. | Financial categories/confidence bands and missing-input rules NC. | SCR-005-F18; SCR-002-F23. |
| DAT-017-F06 | Physical name NC — policy reasons | Stored review explanation/rule evidence; schema NC. | Reviewer must receive policy reasons; persistence representation NC. | Must reflect deterministic result, not model-created authority. | SCR-002-F31; SCR-005-F12. |
| DAT-018-F01 | `deletion_receipts.tenant_id` | Purge tenant scope; type NC. | Required tenant-owned attribution; physical default NC. | Physical key and root-deletion survivability NC. | API-026/040. |
| DAT-018-F02 | `deletion_receipts.object_ref` | Inventoried object/resource reference; structure/length NC. | Auditable target reference required; physical nullability/default NC. | Object-level versus aggregate-level grain and public redaction NC. | `SCR-X-004`; API deletion content. |
| DAT-018-F03 | `deletion_receipts.purge_time` | Purge/completion time; physical type/precision NC. | Completion evidence required; pending/held timestamp semantics NC. | UTC/RFC 3339 when public. | API deletion content. |
| DAT-018-F04 | `deletion_receipts.actor` | Purge actor/service attribution; type NC. | Durable attribution required; default NC. | Actor alias and service identity mapping NC. | DAT-COM-F03. |
| DAT-018-F05 | Physical names NC — legal-hold exception, receipt hash, manifest ID | Protected-object and verified-completion evidence; schemas NC. | Protected records retained and receipted; deletion event carries manifest ID/receipt hash concepts. | Receipt identity, hash protocol, manifest type, completion-status vocabulary NC. | API event `TenantDeletionVerified`; `TST-013`. |

**Needs confirmation — OQ-DAT-019:** Resolve connector cursor/history layout, retry/error schema, source namespaces, synchronization concurrency, and safe lower-trust restrictions.

**Needs confirmation — OQ-DAT-020:** Resolve token/accounting grain, quota reservations, numeric types, currencies and precision, failed-attempt reconciliation, daily rollup windows, and cost-center/deployment-version attribution.

**Needs confirmation — OQ-DAT-021:** Define policy input/result/reason storage, rule-version references, complete normalized-input schemas, and artifact/evidence binding.

**Needs confirmation — OQ-DAT-018:** Define receipt/inventory/tombstone/hold schemas and retained evidence after resource deletion.

### Supplementary Field Definitions

These are source-confirmed data concepts unless marked illustration-only. Physical names and all omitted type/length/precision/nullability/default/key details are **Needs confirmation**, not implicit fields.

| Field ID | Dataset and field concepts / exact names where supplied | Meaning, requiredness, and constraints | Earlier trace / source |
|---|---|---|---|
| DAT-019-F01 | Principal identity; OIDC issuer, audience, expiry, subject, tenant | Authenticated context required. Exact claim names/types and subject-to-application-ID mapping NC; reject missing tenancy/unexpected algorithms. | API-027/048; `OQ-API-001/002`. [DDS], p. 21. |
| DAT-019-F02 | Role, tenant/workspace membership, action, sensitivity, source ACL, segregation constraints | Required authorization attributes. Membership relation keys, permitted role combinations, effective periods, and removal history NC. | SCR user table; API authorization inventory. [DDS], pp. 22–23. |
| DAT-019-F03 | Credential/secret reference and revocation context | Vault-backed scoped reference, not public raw secret. Secret values remain in vault; browser refresh-token storage restrictions apply. | SCR-006-F04/F05; API-049. [DDS], pp. 21, 27, 63. |
| DAT-020-F01 | Attachment identity, case reference, immutable document-version reference | Separate entity and stable associations required; exact columns, multiplicity, ownership, and removal NC. | SCR-002-F18; API-006. [DDS], pp. 24, 51. |
| DAT-020-F02 | Classification labels, confidences, provenance | Asynchronous classification output. Types, labels, numeric scale, versions, and failure states NC. | SCR-002-F14–F16; API-CASE-F16. [DDS], p. 12. |
| DAT-020-F03 | Correction reason code and corrected labels | Reason code conditionally required when correcting labels; actor/revision/provenance history required at durable change. Exact vocabulary/schema NC. | SCR-002-F17/A04; API-CASE-F17/API-GAP-001. [DDS], p. 12. |
| DAT-021-F01 | Connector capabilities: list, fetch, delta cursor, ACL, delete | Capability advertisement required. Exact Boolean/list representation and restrictions NC; missing support triggers explicit lower-trust warning. | SCR-006-F02/F03; API-018/049. [DDS], p. 27. |
| DAT-021-F02 | Sync run identity/status and per-item outcomes | Durable accepted operation and preceding-item outcomes required. State enum, item identity, ordering, and timestamps NC. | SCR-006-F06–F09; API-019. [DDS], pp. 28–29. |
| DAT-022-F01 | File bytes, MIME signature, extension, size, decompression control | Necessary validated ingestion content. R1 formats and configurable 25 MB per-file cap; exact wire names/byte unit/boundary/threshold NC. | SCR-002-F18; API-006. [DDS], p. 30. |
| DAT-022-F02 | Page index, block bounding boxes, table row/column annotations, headings, reading order | Layout-aware extraction data. Types, coordinates, order schema, and non-PDF layout representation NC. | SCR-003-F06/F09/F10; API-PROC-003. [DDS], p. 31. |
| DAT-022-F03 | OCR opt-in and provenance | OCR fallback opt-in and provenance-marked; default/configuration scope NC. Beyond-English OCR deferred. | SCR-002-F19; SCR-003-F13. [DDS], pp. 10, 31. |
| DAT-022-F04 | Empty-page ratio, unknown-character ratio, table-loss indicators, language confidence | Extraction quality data. Numeric types/scales/thresholds NC; low-quality documents remain viewable but cannot support autonomous recommendations. | SCR-002-F21; API-EVID-F11. [DDS], p. 32. |
| DAT-022-F05 | Likely-personal-data tags | Extraction tags likely personal data; tag taxonomy, offsets, confidence, and storage NC. | API privacy dependency. [DDS], p. 62, §17.2.2. |
| DAT-023-F01 | Search `tenant_id`, `workspace_id`, `document_version_id`, `chunk_id` | Required search-row scope/version/chunk content; provider types and identity-key tuple NC. | API search index data. [DDS], p. 34. |
| DAT-023-F02 | Search language, classification, embedding, text | Required search row includes language/classification, **1536-dimensional embedding**, and normalized keyword text. Numeric vector type, language codes, analyzers, and text length NC. | API search index data; SCR-003. [DDS], p. 34. |
| DAT-023-F03 | Index alias/generation, completeness and recall checks | Versioned index lifecycle evidence; physical schema, uniqueness, generation IDs, thresholds, and readiness formula NC. | API-PROC-019. [DDS], pp. 34, 78. |
| DAT-023-F04 | Query, lexical/vector candidates, rankings, diversity/token budget | Retrieval concepts confirmed; persistent-query/score schema, field lengths, ranking parameters, and response projections NC. | SCR-003-F01; API-009/045. [DDS], pp. 35–36. |
| DAT-024-F01 | Deployment capability, region, data-handling class, context length, cost profile, evaluation approval | Registered model-selection data required. Types, status vocabulary, and catalog projection NC. Workspace allowlist identifies specific approved deployments. | SCR-007-F03; API-020/036/050. [DDS], p. 37. |
| DAT-024-F02 | Prompt-template version/digest, fixed system rules, signed workflow instruction, user input, delimited passages | Prompt composition and actual version trace required. Template/body storage and signature schemas NC; source text remains untrusted. | SCR-002-F28/F29; SCR-005-F10/F11. [DDS], pp. 38, 58. |
| DAT-024-F03 | Generation attempt, output schema version, structured result, prompt-injection indicators | Versioned JSON output validation and recorded injection indicators required. Attempt/result persistence and safe payload schema NC. | API-036; `MODEL_OUTPUT_INVALID`. [DDS], pp. 38–39. |
| DAT-024-F04 | Tool name/capability reference and pinned schema | Approved, version-pinned discovery metadata; authorization separate. Registry columns/grants and schema IDs NC. | API-045/046. [DDS], pp. 41–42, 87. |
| DAT-025-F01 | Candidate artifact, exact artifact hash, artifact status | Exact review content and hash required; content/media format, identifier, immutable-version boundary, and status storage NC. Accessible labels DAT-CODE-007. | SCR-002-F25/F26; SCR-005-F07/F08. [DDS], pp. 44–45, 57–58. |
| DAT-025-F02 | Model/prompt version, evidence set/citations, policy inputs/result/reasons | Exact review context required. Association keys and immutable snapshot semantics NC. | SCR-005-F09–F12/F18; API-013/016/017. [DDS], p. 58. |
| DAT-025-F03 | Satisfied publication gate and final response pointer | Atomically recorded publication evidence required; physical representation and status enum NC. | SCR-002-A12; API-PROC-006. [DDS], p. 45. |
| DAT-025-F04 | Closed-case snapshot: approved answer, cited versions, reviewer decisions | Immutable closure lineage required; file/table structure, identity, and retention/retrieval projection NC. | SCR-002-A09/A10; API-005. [DDS], p. 26. |
| DAT-026-F01 | Idempotency key, actor, request fingerprint, original outcome | Case-domain mapping persists one outcome for **24 hours**. Physical names, fingerprint canonicalization, scope, rejected-result storage, and TTL elsewhere NC. | SCR-COM-010; API-PROC-018/OQ-API-004. [DDS], pp. 25, 54. |
| DAT-026-F02 | Event ledger identity, operation key, aggregate revision, duplicate outcome | Consumer deduplication/stale detection required. Ledger PK, consumer namespace, and lifetime NC. | API-PROC-018; `TST-007`. [DDS], pp. 17, 48–50. |
| DAT-026-F03 | Dead letter, original event identity, operator reason, dry-run evidence, scope limit, migration provenance | Required replay controls; reason/type/length, scope units, status, and ledger schema NC. | `SCR-X-006`; API-038. [DDS], pp. 50, 90. |
| DAT-027-F01 | Cache key: tenant, user-scope digest, source ACL revision, query hash, index generation | All dimensions required. Canonical key encoding/hash algorithms, multi-source ACL representation, and normal TTL NC. | API-PROC-019. [DDS], p. 53. |
| DAT-027-F02 | Cached result and version/expiry metadata | Only versioned ephemeral results with short TTLs. Exact values/expiry field names/storage NC. Authorization change overrides ordinary expiry. | SCR-003-A04; API-009. [DDS], pp. 16, 53. |
| DAT-028-F01 | Blob key: tenant, workspace, document, version, object role | Required key dimensions; separators/role vocabulary/escaping/key length NC. Public names opaque. | API-039; API-GAP-003. [DDS], p. 52. |
| DAT-028-F02 | Encryption reference and signed object-access URL | Encryption and controlled short-lived source access required. Key/reference format, URL schema, lifetime, and permission revocation after issuance NC. | SCR-003; API source-access gap. [DDS], pp. 52, 63. |
| DAT-029-F01 | Hold scope/reason/authorization and protected-object inventory | Legal-hold behavior confirmed; source does not define field names, types, reason requiredness, hold release, or priority between holds. | API-029; `SCR-X-005`. [DDS], pp. 26, 80. |
| DAT-029-F02 | Tombstone and deletion inventory | Required deletion control and no retrieval of soft-deleted entities. Marker, timestamps, reason, object list, and restoration semantics NC. | API-026/040. [DDS], pp. 51, 80. |
| DAT-029-F03 | Export manifest: case metadata, approved artifacts, source references, audit manifests, checksums | Required export content; scope/serialization/checksum protocol NC. Secrets/internal model prompts excluded. | API-025; `SCR-X-003`. [DDS], p. 79. |
| DAT-029-F04 | Independent approval evidence for export/deletion | Two independent approval checks required. Request references, actor relationships, validity/revocation, and persistence NC. | API-025/026; `T-11`. [DDS], pp. 78, 83, 88. |
| DAT-029-F05 | Provisioning state, policy, encryption references, role bindings, quotas, connector stubs | One idempotent workflow creates these resources. State/schema and consistency evidence NC; incomplete provisioning blocks sync. | API-GAP-008; `SCR-X-002`. [DDS], p. 78. |
| DAT-029-F06 | Stable backfill source IDs, bounded window, reconciliation receipt, index coverage | Per-batch receipts and stable source identity required. Window/receipt/coverage schemas and thresholds NC. | SCR-006-F13; API provisioning gap. [DDS], p. 78. |
| DAT-030-F01 | Costs, quotas, budget, forecast, rejected excess, trends | Attributed reporting data; types/currency/windows/precision and formulas NC. Daily rollups confirmed; execution time not supplied. | SCR-010-F01–F06; API-022. [DDS], pp. 65–66, 83. |
| DAT-030-F02 | Cost center, deployment version, model/embedding/storage/indexing usage | Required separate attribution; reference vocabularies, measure units, and allocation rules NC. | SCR-010-F07–F10; API-022. [DDS], pp. 65, 68. |
| DAT-030-F03 | Trace identifiers, child stages, identifiers/policy outcomes; metrics taxonomy | Privacy-safe diagnostics. Span/metric schemas, sampling/windows/labels and alert thresholds NC. No documents/API secrets. | SCR-004-F11; API-041. [DDS], pp. 64–65. |
| DAT-030-F04 | Alert owner/threshold and incident evidence | Routine spend anomalies create tickets with owner and threshold; actual owner/threshold values are not supplied. | API operational data. [DDS], p. 65, §18.2.2. |
| DAT-031-F01 | Dataset version, signed manifest, expected citation sets, expected decisions | Frozen, versioned, independently reviewed synthetic fixtures; **1,200** reference cases. File/schema/signature/expected-result types NC. | SCR-011-F03/F04/F11; API-023/024. [DDS], pp. 75, 88–89. |
| DAT-031-F02 | Citation precision, unsupported-claim rate, high-risk policy recall | Targets `>=0.97`, `<=0.02`, and `1.00` on frozen safety suite. Numeric representation/aggregation NC. | SCR-011-F05–F07; API evaluation catalog. [DDS], p. 75. |
| DAT-031-F03 | Domain, confidence intervals, distribution shift, release-gate result | Domain/statistical evidence required; taxonomy/calculation/schema/result enum NC. Low confidence blocks release. | SCR-011-F08–F10; API-024. [DDS], pp. 75–76. |
| DAT-031-F04 | Randomized-test seed, signed test output, release digest reference | Required test reproducibility/provenance. Types, signatures, file format, and retention NC. | API fixture requirements. [DDS], p. 89. |
| DAT-032-F01 | Image digest, schema versions, prompts, model-routing policy, build identity, SBOM/test attestations | Reconstructible release bindings and verified build identity required. Fields/signature formats/file names NC. | API-043/044. [DDS], pp. 72–73. |
| DAT-032-F02 | Nonsecret defaults, signed environment configuration, vault-backed references | Source-control/environment/secret taxonomy confirmed; precedence/schema/default approval NC. | SCR-007; API configuration table. [DDS], pp. 71–72, 90. |
| DAT-032-F03 | Migration compatibility/backfill/enforcement and rollout evidence | Expand-and-contract, bounded backfill, old-reader drainage and readable-write rollback plan required. Data format/batch size/schedule NC. | API-COM-004; API-043/044. [DDS], pp. 52, 72. |
| DAT-033-F01 | Change impact scores: behavior, data migration, threat surface, operating cost | Change record carries these scores; numeric scales, nullable/required schema and approvals NC. | API-032/033. [DDS], p. 8. |
| DAT-033-F02 | Design major/minor revision and invariant/test links | Approved record increments minor; incompatible protocol changes major. Every revised invariant links to at least one negative test. Representation/link keys NC. | API-032/033. [DDS], pp. 8–10. |
| DAT-034-F01 | SSE offset / `Last-Event-ID` | Monotonically increasing resumable stream position. Type/storage/history/gap semantics NC; not automatically event UUID. | SCR-004; API-015. [DDS], p. 55. |
| DAT-034-F02 | Webhook recipient, signed payload, age, delivery/retry context | Optional signed notifications; exact fields/signatures/age bounds/acknowledgments NC. Failure does not roll back case state. | API-047; `SCR-X-007`. [DDS], p. 55. |
| DAT-034-F03 | Canonical `error` object: `code`, `message`, `correlation_id`, `retryable`, `details` | JSON object/string/Boolean kinds confirmed by example. Full mandatory schema, per-code details, and any persisted error table NC. | API canonical error body; SCR-COM-011. [DDS], p. 84. |
| DAT-035-F01 | Illustrated open-case/review counts, evidence coverage, service summary | Display examples confirmed; aggregate formulas/types/scope/storage NC. No default `128`, `14`, `97.6%`, or `Healthy`. | SCR-COM-F03–F06; API-GAP-010. [DDS], pp. 7, 14. |
| DAT-035-F02 | View/review/evidence/notification projections | Authorized exact review data and authoritative server progress. Persistent UI state, notification delivery/read receipts, and locale preference storage NC. | SCR-001–SCR-008; API-002/008/013/016. [DDS], pp. 57–59. |
| DAT-036-F01 | Admission/capacity/load/recovery context | Workspace tokens, queue age, provider capacity, recovery evidence. Schema/threshold/defaults NC; no new capacity table selected. | API-030/042; API-PROC-020/030. [DDS], pp. 68–70. |

### Code Systems and Value Constraints

| Code-system ID | Meaning / affected data | Confirmed literals or constraints | Physical and semantic gaps | Source / earlier trace |
|---|---|---|---|---|
| DAT-CODE-001 | Case state | `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED` | Case DDL has exact `CHECK`; complete closure/reopen graph unresolved. | [DDS], pp. 25, 82, 86; SCR-002-F08/API-CASE-F10. |
| DAT-CODE-002 | Run state | `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED` | Physical enum/type and recoverable timeout/wait-versus-failure semantics NC. | [DDS], pp. 49, 82; SCR-004-F03. |
| DAT-CODE-003 | Document state | `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED` | State owner/column, full transitions/retries and low-quality readiness NC. | [DDS], p. 82; SCR-002-F20/API-007. |
| DAT-CODE-004 | Review state | `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED` | Physical field/type and transition/race rules NC. Not a complete decision request enum. | [DDS], p. 82; SCR-005-F05/API-017. |
| DAT-CODE-005 | Information classification | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` | Maximum included material class governs routing/redaction/retention/approval; ordinal encoding and inheritance/missing-class rules NC. | [DDS], p. 62; SCR-002-F07/API-CASE-F09. |
| DAT-CODE-006 | Deterministic policy result | `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY` | Exact result column representation and associated reasons NC; LLM cannot override. | [DDS], p. 44; SCR-002-F30/SCR-005-F12. |
| DAT-CODE-007 | Accessible artifact label | `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` | Stored artifact enum versus derived UI label mapping NC. Distinct from case/run/review states. | [DDS], p. 57; SCR-COM-005. |
| DAT-CODE-008 | Baseline authorization roles | `Analyst`, `Reviewer`, `Admin`, `Auditor`, `Service` | `Workspace Admin`, `Owner`, `Member`, approver/operator/elevated-role mappings NC. | [DDS], pp. 11, 22, 83; OQ-SCR-003/OQ-API-002. |
| DAT-CODE-009 | Classification labels, correction reasons, financial impact, confidence bands, retention classes, plans, language codes | No complete vocabulary supplied. Appendix F includes `HIGH_RISK` as a review-trigger risk tag. | **Needs confirmation.** `HIGH_RISK` is not an additional information class. | [DDS], pp. 12, 24, 34, 44, 90. |
| DAT-CODE-010 | Existing stable failure literals | `CASE_VERSION_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `CONNECTOR_REAUTH_REQUIRED`, `NO_SUPPORTED_EVIDENCE`, `MODEL_OUTPUT_INVALID` | Error casing conflict and full status/code schema remain unresolved. Do not declare these as the complete stored-error enum. | [DDS], pp. 25, 27, 36, 38, 54, 84, 89; OQ-API-032. |

### Identity, Hash, and Version Distinctions

**DAT-COM-004 — Noninterchangeable identifiers.**

| Distinction | Required treatment | Open contract |
|---|---|---|
| Case UUID versus displayed business number | Preserve canonical resource identity; illustrated business number does not replace it. | Number generation/mapping/uniqueness: OQ-DAT-006. |
| Document ID versus document-version ID versus derivative ID | Preserve source and immutable-version lineage; reprocessing does not overwrite prior cited evidence. | Fingerprint/pipeline-to-UUIDv7 identity design: OQ-DAT-008. |
| Chunk ID versus evidence-set ID versus `evidenceId` versus citation ID | Keep concepts distinct until explicitly mapped. Citation IDs remain opaque. | Formal `Citation` and public identity: OQ-DAT-009. |
| Task ID versus `approvalId` versus decision ID versus assignment | A decision targets the exact valid review task/artifact; no inferred alias. | Review identity/routing: OQ-DAT-016. |
| File hash versus text hash versus artifact hash versus ACL/input/audit digests | Each verifies its own source/input and scope. No universal encoding or canonicalization selected. | Hash algorithm/input/encoding protocol: OQ-DAT-009/OQ-DAT-016/OQ-DAT-021. |
| Case revision, plan revision, policy/configuration version, parser/pipeline version, index generation | Track actual versions independently and retain their relationships. | Types and bindings: OQ-DAT-005/007/008/015/021. |
| Event UUID versus stream offset versus provider cursor | Respect event deduplication, SSE order, and provider continuation independently. | Cursor/ledger encoding and retention: OQ-DAT-013/019/024. |

**Sources:** [DDS], pp. 24–25, 28, 31, 34–35, 40, 44–45, 48, 51, 55, 85, 87.

No additional indexes, denormalized summaries, or universal hash columns are approved by these distinctions.

## Lifecycle and Consistency

### Creation, Reading, Modification, and Deletion

The following matrix maps source-supported operations. It does not create missing APIs or authorize direct browser access to internal services.

| Lifecycle ID | Data | Create / update | Read | Delete / retention | Screen and contract limitations |
|---|---|---|---|---|---|
| DAT-LC-001 | Tenant/workspace/identity/settings: DAT-001/002/019/029 | Idempotent provisioning creates policy, references, role bindings, quotas, connector stubs. API-028 updates membership. Workspace settings require revision-safe updates. | API-027 principal context; actual tenant/workspace-policy/membership read APIs absent. | API-026 controlled workspace deletion; target inventory and root-tenant semantics NC. | `SCR-X-002`; SCR-007. API-GAP-002/API-GAP-008 remain unresolved. |
| DAT-LC-002 | Case/current/history/classification: DAT-003/004/020 | API-001 creates `NEW` case; async classification. API-004 uses `If-Match`; correction API absent. API-005 closes/snapshots. | API-002/003 authorized current case/list. | Eligible closed-case retention; legal-hold exceptions. No public case-delete API confirmed. | SCR-001/SCR-002; reopen and correction mutations NC. |
| DAT-LC-003 | Attachment/document/version/extraction/blob: DAT-005–007/020/022/028 | API-006 accepts ingestion; scan, parse, normalize, index asynchronously. Connectors ingest stable-source changes. | API-007 status; API-008/010 evidence; API-039 internal storage; browser source access API absent. | Source deletes create tombstones and index removal; final object removal follows controlled purge. Attachment removal NC. | SCR-002/SCR-003/SCR-006; quarantined rendering contract not supplied. |
| DAT-LC-004 | Search/evidence/cache: DAT-010/023/027 | Indexer builds derivative generations; Retrieval Service forms bounded evidence. Search-result persistence details NC. | API-009/010/045 and API-008 case evidence. | ACL changes invalidate affected entries before new results; soft-deleted sources cannot be retrieved. | SCR-003 and review evidence. Search does not mutate index merely because associated event prose names `SearchIndexCommitted`. |
| DAT-LC-005 | Run/steps/model/artifact: DAT-008/009/024/025/026 | API-011/012 allocates admitted workflow; persists plan before side effects and checkpoints before dispatch. Gateway validates output and records usage/injection evidence. | API-013/014/015/037; approved catalog API-020. | Retention of failed/published/reworked runs and artifacts NC. No cancel/delete-run API confirmed. | SCR-002/SCR-004/SCR-005; no orchestrator database credentials. |
| DAT-LC-006 | Policy/review/gate: DAT-011/012/017/025 | Deterministic evaluation; routed task; API-017 captures exact-hash decision; atomic publication gate/pointer. | API-016; exact task-detail API absent; context must be available before decision. | Historical decisions immutable; permitted retention/purge with holds and audit lineage NC. | SCR-005/SCR-008; accepted approval response is not automatic publication completion. |
| DAT-LC-007 | Connector/cursor: DAT-015/021 | API-018 starts async sync; durable per-run outcomes and cursor advancement. Credential revocation contract absent. | API-019 history; read/configure/authenticate APIs absent. | Connector CRUD/delete and source tombstone persistence NC. | SCR-006; unsupported ACL support cannot waive mandatory authorization. |
| DAT-LC-008 | Outbox/idempotency/dead letters: DAT-014/026/034 | Business transactions write outbox; consumers deduplicate; operator replay uses API-038 with reason/dry-run/scope. | API-037 workflow; retained SSE via API-015. | Ledger, queue, outbox, dead-letter, and stream retention NC. | SCR-004; `SCR-X-006`. Internal replay is not automatically browser-accessible. |
| DAT-LC-009 | Audit/usage/telemetry: DAT-013/016/030 | Services append audit evidence; gateway tracks usage; daily attributed rollups. | API-021 Auditor; API-022 Admin usage; API-041 protected metrics. | Distinct diagnostic/audit retention, receipts, and hold exceptions. Approved corporate policy NC. | SCR-008/SCR-010; full prompts/documents not diagnostics. |
| DAT-LC-010 | Evaluation/release/design: DAT-031/032/033 | API-023 starts frozen benchmark; prompt/model changes reevaluated. API-043 release; API-032 controlled design decision. | API-024/044/033. | Retention and archive of release/test/decision artifacts NC. | SCR-011; `SCR-X-008/X-009`. No implied screen fixture editing or release-promotion control. |
| DAT-LC-011 | Export/holds/purge/receipts: DAT-018/029 | API-025/026 use independent approvals; API-029 hold; API-040 internal purge. | Status/download/receipt/hold-read APIs absent. | Enforce holds, write tombstones, remove eligible blobs/index entries, retain and receipt protected objects. | `SCR-X-003/X-004/X-005`; no invented completion enum/download route. |
| DAT-LC-012 | UI/operational projections: DAT-035/036 | Persistence/mutation of UI state, notification state, health/capacity records NC. | Supported list/evidence/run APIs; API-030/034/035/042 operational data. | Projection/cache retention NC. | UI titles/register names do not justify new persisted tables or read-triggered jobs. |

**Sources:** [DDS], pp. 12, 21–32, 34–46, 48–59, 62–80, 83.  
**Earlier trace:** `API-PROC-002`–`API-PROC-017`.

### Referential Integrity and Tenant Isolation

**DAT-LC-013 — Tenant-safe references.**

1. Establish authenticated tenant scope before accessing tenant-owned data.
2. Apply `tenant_id` to every storage predicate, including relational, object, cache, index, and background-processing boundaries.
3. Enforce case-to-tenant and case-to-workspace references.
4. Prevent an authorized tenant’s case from referring to another tenant’s workspace.
5. Validate attachment-to-version, chunk-to-version, run-to-case, review-to-run/artifact, and receipt-to-inventory relationships under the same applicable tenant/resource scope.
6. Enforce originating source ACL before returning chunks to generation.
7. Return the same non-disclosing not-found class for foreign-tenant and absent identifiers.
8. Reset scoped database session variables after each transaction before pooled connection reuse.

**Sources:** [DDS], pp. 21–23, 24, 31, 51–53, 86; p. 89, `TST-003/TST-004`.  
**Earlier trace:** `SCR-COM-002/003`, `API-COM-002`, `API-PROC-001/019`.

**Needs confirmation — OQ-DAT-002/OQ-DAT-014:** Define the complete physical integrity and RLS write policy, privileged/service-role restrictions, scoped-session failure behavior, and FK/procedure strategy. The shown `USING` policy alone is not the supplied complete production access design.

### State Transitions and History

#### Case State

| Current state | Confirmed transition / exception | Durable requirements |
|---|---|---|
| Creation | Starts `NEW` | One accepted case outcome under idempotent creation. |
| `NEW` | `TRIAGED` | Role/revision/domain guards and change history. |
| `TRIAGED` | `IN_PROGRESS` | Same guards. |
| `IN_PROGRESS` | `PENDING_APPROVAL` or `RESOLVED` | Applicable evidence/approval rules preserved. |
| `PENDING_APPROVAL` | `RESOLVED` or `IN_PROGRESS` | Preserve decisions and rework lineage. |
| `RESOLVED` | Close operation exists; explicit transition to `CLOSED` not enumerated | Predecessor/closure guards require confirmation. |
| `CLOSED` | Final unless explicitly reopened as a new revision | Prior approved-output lineage must remain immutable. |

**Sources:** [DDS], pp. 12, 25–26, 82.  
**Open:** OQ-DAT-007; preceding `CON-SCR-006`, `CON-API-003`.

#### Run, Document, Review, and Artifact State

| Data | Confirmed behavior | Open transition contract |
|---|---|---|
| Run | Source sequence `REQUESTED -> RETRIEVING -> GENERATING -> POLICY_CHECK -> AWAITING_REVIEW -> PUBLISHED` or terminal failure; checkpoint before downstream dispatch. | `AUTO_ALLOW` path, missing-approval termination versus valid waiting, failure entry points, timeout pause/recovery, and unsupported/denied representation: OQ-DAT-015. |
| Document | Scan and quality gates govern DAT-CODE-003 states; unsafe input quarantined without indexing. | Full graph, retry/reprocessing state, whether low-quality derivatives can be `READY`, and state ownership: OQ-DAT-008/OQ-DAT-010. |
| Review | Actor/hash/separation-of-duty guards apply; expiry causes reassignment/escalation, not approval. | Open trigger, complete graph, late/conflicting decisions, and assignment history: OQ-DAT-016. |
| Artifact | Accessible labels `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED`; partial processing never presented as approved answer. | Stored status versus projection and mapping to run/case/review states: OQ-DAT-015/OQ-DAT-026. |

**Sources:** [DDS], pp. 13, 30–32, 41, 44–46, 49, 57–58, 82.

**DAT-LC-014 — Current state versus immutable history.**

- `cases` holds mutable current state; `case_revisions` is append-only.
- Document and normalized evidence versions are immutable; changed processing produces side-by-side derivatives.
- Decisions remain immutable; operators cannot alter historical review decisions.
- Denied requests may be reworked as new run revisions, not retroactively marked approved.
- Closure snapshots approved answer, cited versions, and reviewer decisions.
- Changing the current approved-result pointer must not rewrite an earlier closed snapshot.
- Classification correction requires a reason code and durable attribution; its detailed history schema remains unresolved.

**Sources:** [DDS], pp. 12, 24–26, 31, 45–46, 62, 85.

### Transactions, Concurrent Changes, and Replay

**DAT-LC-015 — Transactional mutations.**

1. Validate payloads before transaction entry, again at domain invariants, and before tool dispatch.
2. Re-evaluate resource authorization within the state-changing transaction.
3. Apply the accepted case mutation or approval decision and associated outbox insert in one ACID transaction.
4. Record the satisfied publication gate and update the final response pointer in the same publication transaction.
5. Reject stale or unauthorized changes without changing business state.
6. Persist run plan revision before side effects and workflow checkpoint before downstream dispatch.
7. Dispatch search indexing and optional webhooks asynchronously with explicit reconciliation.
8. Do not treat a `202` acceptance as completed ingestion, run, evaluation, export, or deletion.

**Sources:** [DDS], pp. 22, 40, 45, 49, 52, 56, 83.  
**Earlier trace:** `API-PROC-001/005/006`.

**Needs confirmation — OQ-DAT-014:** Select transaction isolation, concurrency/lock strategy, idempotency/result reconstruction, audit-write failure handling, object-versus-relational commit coordination, and legal-hold race handling. No implementation technique is selected by this specification.

**DAT-LC-016 — Revision and idempotency consistency.**

- Case mutations use `If-Match` revision preconditions.
- Conflicting updates produce `CASE_VERSION_CONFLICT` with current revision; source API register gives HTTP `409`.
- An idempotency key maps actor and request fingerprint to one case-domain outcome for **24 hours**.
- Identical replay returns the original outcome; changed fingerprint under the same key produces `IDEMPOTENCY_CONFLICT`.
- Every cross-service write is idempotent under retry.
- At-least-once consumers deduplicate event IDs and operation keys and detect stale aggregate revisions.
- No business invariant relies on ordering across separate queue partitions.
- A duplicate may have a recorded duplicate outcome, but it cannot create another accepted business transition.
- Queue replay cannot publish different content under an old approval.

**Sources:** [DDS], pp. 15–17, 25, 45–50, 54, 89.  
**Open:** OQ-DAT-013/OQ-DAT-014. Key format/scope/canonicalization, pending duplicates, permission-changed replay, expired-key reuse, and non-case TTL remain unresolved.

### Index, Cache, and Source Consistency

**DAT-LC-017 — Immutable source and derivative reconciliation.**

1. Preserve accepted source metadata if indexing fails.
2. Compare source fingerprints and indexed versions during reconciliation; retry through durable workflow/outbox evidence.
3. Build replacement indexes in parallel.
4. Switch the read alias atomically only after completeness and recall checks.
5. Apply source ACL filtering before any chunk is released to generation.
6. Purge affected caches upon authorization/ACL change before new retrieval results are served, even if normal TTL has not expired.
7. Re-evaluate current authorization and evidence at publication.
8. Tombstone source deletion and remove corresponding search entries; soft-deleted entities are not retrievable.
9. During suspected ACL leak, suspend affected aliases, revoke cached evidence, preserve audit traces, and re-enable only after negative-access tests pass.
10. If vector search is degraded, permitted lexical retrieval may continue with a visible reduced-quality flag; no degraded mode bypasses approval or authorization.

**Sources:** [DDS], pp. 27–29, 31, 34–36, 46, 49, 53, 69, 79–80, 90.  
**Earlier trace:** `API-PROC-019`, `SCR-003-A04/A05`.

**Needs confirmation — OQ-DAT-011/OQ-DAT-012/OQ-DAT-019:** Define coverage/recall checks, concurrency during alias changes, cache-key and invalidation protocols, reconciliation bounds, safe behavior when ACL capability is missing, and normal staleness for nonsecurity changes. No numeric cache TTL, reconciliation schedule, or acceptable ACL-leak delay is supplied.

### Retention, Export, Deletion, and Recovery

| Lifecycle requirement | Confirmed behavior | Open decision beside requirement |
|---|---|---|
| DAT-LC-018 — Closed-case retention | Retention jobs operate only on eligible closed cases and maintain legal-hold exceptions. | Eligibility/retention-class durations, related artifact/history scope, and execution schedule: OQ-DAT-007/OQ-DAT-018. [DDS], p. 26. |
| DAT-LC-019 — Diagnostic/audit distinction | Diagnostic logs have a **30-day default TTL**; security audit follows a distinct **seven-year policy in the fictional design**. Purge records receipts and hold exceptions. | Approved corporate policy and precedence with legal hold/tenant deletion remain unresolved. These values are not screen query-range limits. OQ-DAT-018/OQ-DAT-025. [DDS], pp. 66, 90. |
| DAT-LC-020 — Controlled export | Two independent approval checks; package metadata, approved artifacts, source references, audit manifests, checksums. Secrets/internal model prompts excluded. | Snapshot boundary, independent-approval validity, draft/held-object treatment, format, download/status and archive lifetime: OQ-DAT-018/OQ-DAT-023. [DDS], pp. 78–79, 83. |
| DAT-LC-021 — Verified deletion | Enforce legal hold; write tombstones; remove eligible blobs/index entries; record completion receipts; protect and receipt held records. | Inventory granularity, physical relational purge/cascade, receipt survival, partial completion, backups and historical citations: OQ-DAT-018. [DDS], pp. 51, 80, 89. |
| DAT-LC-022 — Data-subject inventory | Source states data subject access requests use the same inventory. | Subject identification, authorized access/export/erasure outputs, schema, and interaction with holds are not specified. Do not infer automatic erasure for every access request. OQ-DAT-017/OQ-DAT-018. [DDS], p. 80. |
| DAT-LC-023 — Replay/history retention | Replay preserves original event identity unless explicit schema migration includes provenance link. Retained SSE events backfill only within caller scope. | Ledger/stream/queue retention and expiration/gap recovery: OQ-DAT-013/OQ-DAT-024. [DDS], pp. 50, 55. |
| DAT-LC-024 — Backup and recovery | One primary and one warm recovery region; primary receives writes. PostgreSQL continuous backups target RPO `<=15 minutes`, RTO `<=4 hours`; object versions and rebuild recipes tested together. | Provider/regions, backup retention/encryption, restore inventories and deletion/hold propagation to backups: OQ-DAT-018/OQ-DAT-025. [DDS], pp. 19, 69. |

The source confirms a **scheduled tombstone pipeline**, retention jobs, reconciliation workers, and daily rollups. It does not supply their execution times, polling intervals, batch sizes, or operator assignments.

### Personal Data, Secrets, and Evidence Access

**DAT-LC-025 — Data handling.**

1. Extraction tags likely personal data.
2. Before external provider invocation, the gateway redacts nonessential personal fields where policy permits.
3. Maximum information class of any included material controls model routing, log redaction, retention, and approval policy.
4. Logs capture token counts and digests, not entire prompts by default.
5. Diagnostic traces never contain user documents or API secrets.
6. Connector refresh tokens/service credentials remain in a dedicated workspace-scoped secret store.
7. Application credentials and encryption keys remain in vault-backed references; rotation does not require bulk re-encryption in the request path.
8. Public responses and errors do not expose raw credentials, complete prompts, retrieved documents in error details, or unauthorized resource existence.
9. Auditor evidence is limited to authorized decision metadata, prompt-template digests, access events, and redacted content scope.
10. Production data is forbidden in development; staging uses synthetic data/test connectors.
11. Signed source URLs remain access-controlled and short-lived; issuance is not a waiver of source authorization.
12. Retrieved/model text remains untrusted data and cannot authorize tools, change tenant scope, or alter approval policy.

**Sources:** [DDS], pp. 7, 11, 19, 21, 27, 37–39, 52, 54, 61–64, 79, 84.

**Needs confirmation — OQ-DAT-017:** Define personal-data tag categories and offsets, redaction policy/representation, authorized evidence paths, retained actor identities after deletion, safe source rendering, signed-URL revocation behavior, provider data handling, and encryption references. Do not introduce unconfirmed personal-data categories, masking rules, or retention exemptions.

### Schema Evolution and Onboarding

**DAT-LC-026 — Migration and version compatibility.**

1. Use expand-and-contract migrations: add nullable columns first, backfill in bounded batches, then enforce constraints.
2. Do not remove a field while active readers still depend on it.
3. Run postdeployment enforcement after old replicas drain.
4. Preserve readable writes according to the explicit rollback plan.
5. Regression rollback changes traffic/binary routing; it does not automatically down-migrate the database.
6. Generate OpenAPI and protobuf from repository-controlled IDL; CI blocks incompatible field deletion and enum changes.
7. Bind deployed image, schemas, prompts, and model-routing policy in reconstructible release records.
8. Historic ingestion uses bounded windows, stable source IDs, and per-batch reconciliation receipts.
9. Search readiness depends on index coverage, not queue emptiness.
10. Revised design invariants link to at least one negative test.

**Sources:** [DDS], pp. 8, 15, 20, 52, 55, 72–73, 78, 89.

**Needs confirmation — OQ-DAT-022:** Obtain actual migration plans, IDL, backfill format and batch limits, compatibility matrix, release/fixture signature schemas, readiness thresholds, and retained release evidence. No migration schedule is supplied.

## Integration Data and Acceptance Criteria

### Input and Output File Inventory

`DAT-FILE` identifiers identify logical file contracts; no physical filename is invented.

| File ID | Direction / content | Producer → consumer | Confirmed format and validation | Naming, encoding, structure, limits, and lifecycle gaps |
|---|---|---|---|---|
| DAT-FILE-001 | Case attachment or repository source file | Analyst/API-006 or repository/API-049 → ingestion | R1 PDF, DOCX, HTML, UTF-8 text. MIME signature and extension agree; configurable **25 MB per-file cap**; decompression threshold; scan before parsing; no macros or embedded remote fetch. | File/part name, request encoding, MIME/extension list, MB unit/inclusive boundary, file count, decompression threshold, encrypted/corrupt-file handling, HTML encoding, and source metadata schema NC. OQ-DAT-010. [DDS], pp. 30, 83. |
| DAT-FILE-002 | Immutable normalized text/layout/metadata | Ingestion → object store/indexer/evidence viewer | Preserve claims; remove transport artifacts; PDF block/page/bbox layout; table row/column annotations; headings/reading order; opt-in OCR provenance. | Actual filenames, object-role vocabulary, JSON/text/binary format, encoding, schema, line endings, normalization rules, and version-to-object mapping NC. OQ-DAT-008/009/010. [DDS], p. 31. |
| DAT-FILE-003 | Audit retention export / audit manifest | Audit ledger → independently controlled retention storage | Append-only audit entries chained with batch hashes; independent retention export. | Format, partition/batch layout, signing/hash algorithm, encoding, cadence, verification procedure, encryption and approved retention NC. OQ-DAT-016/018/023. [DDS], p. 62. |
| DAT-FILE-004 | Authorized workspace export package and manifest | API-025 export workflow → authorized recipient | Case metadata, approved artifacts, source references, audit manifests, checksums; exclude secrets/internal model prompts. Independent approvals required. | Archive format/compression, filenames, manifest schema, content encoding, snapshot semantics, package-size limit, download/status/expiry NC. OQ-DAT-018/023. [DDS], pp. 78–79, 83. |
| DAT-FILE-005 | Frozen evaluation corpus, expected-result fixtures, signed manifest | Independent fixture review → evaluation harness | **1,200** reference synthetic permission-controlled cases; expected citations and decisions; frozen/versioned/signed-manifest protection. | JSONL/CSV/database/file choice, filenames, encoding, record schema, version/hash/signature, leakage-review evidence, replacement protocol NC. OQ-DAT-022. [DDS], pp. 75, 88–89. |
| DAT-FILE-006 | Signed test/release artifacts: image attestations, SBOM, schema/prompt/configuration evidence | CI/release pipeline → deployment/verification | Verified build identity, signed images and test outputs, release-digest linkage; signed environment configuration; vault-backed secret references. | SBOM standard, file names, schema versions, signature/canonicalization/key IDs, storage, retention NC. OQ-DAT-022/025. [DDS], pp. 71–73, 89. |
| DAT-FILE-007 | Database/object recovery snapshots and rebuild recipes | Backup services → controlled recovery workflow | Continuous PostgreSQL backups; primary/warm recovery; relational/object consistency and index recipes tested together. | Snapshot format/name, encryption, retention, export/import tool, recovery inventory schema, deletion/hold propagation NC. OQ-DAT-018/025. [DDS], pp. 19, 69. |
| DAT-FILE-008 | Backfill/reconciliation and purge completion evidence | Onboarding/retention workers → operational inventory/audit | Per-batch reconciliation receipts; purge receipts and hold exceptions; source fingerprint comparison. | File versus relational representation, names, schemas, receipt granularity, signatures/checksums, time windows and retention NC. OQ-DAT-018/019/023. [DDS], pp. 78–80, 85, 90. |

No additional bulk-import spreadsheet, CSV screen export, unrestricted document download, or external file format is confirmed.

### External Formats, Encoding, and Time

| Requirement ID | Boundary | Confirmed representation | Needs confirmation |
|---|---|---|---|
| DAT-INT-001 | Plain-text input | UTF-8 text supported. | BOM, invalid-byte behavior, line endings, Unicode normalization, maximum text length, and replacement-character handling: OQ-DAT-010. [DDS], p. 30. |
| DAT-INT-002 | PDF/DOCX/HTML input | Supported file categories with MIME/extension agreement and safety validation. | Exact allowlist, parser versions, supported features, embedded content, encoding and corrupt/encrypted-file outcomes: OQ-DAT-010. [DDS], pp. 30–31. |
| DAT-INT-003 | Model output | Versioned JSON schema; unknown fields, invalid citations, control-character injection → `MODEL_OUTPUT_INVALID`; bounded parse retries. | Complete schema, string/numeric types, encoding, Unicode/control-character rules, retry limits, and safe invalid-result persistence: OQ-DAT-003/015/024. [DDS], p. 38. |
| DAT-INT-004 | Event producer | UTC and canonical JSON; mandatory envelope below. | Canonicalization algorithm, UTF encoding declaration, signing, timestamp precision, and full payload schemas: OQ-DAT-013/024. [DDS], p. 48. |
| DAT-INT-005 | Public dates/times | RFC 3339 timestamps; server stores UTC. | Fractional precision, accepted offsets/leap-second policy, missing/invalid values, server-versus-client time authority: OQ-DAT-024. [DDS], pp. 54, 59. |
| DAT-INT-006 | UI/calendar | Workspace-local display with timezone labels; locale affects presentation, not durable representation/order. Business-calendar deadlines use workspace timezone. | Timezone identifier system/default, DST/holiday/calendar rules, formatting and locale storage: OQ-DAT-005/024/026. [DDS], pp. 25, 59. |
| DAT-INT-007 | Repository data | Stable source identity, ACL and change-history preservation; provider cursor/high-watermark. | Provider URLs/schemas, ID namespaces, ACL/group mapping, cursor encoding, source times, delete/recreate semantics: OQ-DAT-019/025. [DDS], pp. 27–29. |
| DAT-INT-008 | REST/internal RPC | External OpenAPI is REST authority; protobuf IDL governs internal gRPC. Internal HTTP/gRPC independent authorization. | Actual IDL, versions, media types, scalar precision and nullable/absent semantics: OQ-DAT-003/022/024. [DDS], pp. 16, 55, 82. |
| DAT-INT-009 | Hashes/checksums/signatures | Source/revision SHA-256 terminology, fingerprints, batch hashes, signed manifests/configuration/events, exact approval hash binding. | Per-field algorithm, canonical input, binary/text encoding, key ID/signature carrier, and verification protocol: OQ-DAT-009/013/016/022/023. |
| DAT-INT-010 | Outbound webhook | Signed optional notification; recipient verifies signature and event age. | Payload/event mapping, encoding/canonicalization, age bound, recipient/acknowledgment schema and retry ledger: OQ-DAT-024. [DDS], p. 55. |

### Event Envelope and Payload Data

#### Mandatory Envelope

The following exact property names are source-confirmed. Physical outbox columns and complete wire scalar types are unresolved except where stated.

| Field ID | Exact property | Meaning | Requiredness / type and constraints |
|---|---|---|---|
| DAT-EVT-F01 | `event_id` | Event identity | Required; UUIDv7 application baseline, exact JSON representation NC; consumer deduplication. |
| DAT-EVT-F02 | `type` | Event literal | Required; named events below; complete code/schema NC. |
| DAT-EVT-F03 | `schema_version` | Versioned content contract | Required; type/version format NC. |
| DAT-EVT-F04 | `tenant_id` | Immutable tenant scope | Required; trusted signed background context; wire representation NC. |
| DAT-EVT-F05 | `aggregate_id` | Target aggregate identity | Required; resource mapping/type NC. |
| DAT-EVT-F06 | `aggregate_revision` | Stale-delivery guard | Required; numeric/string representation NC. |
| DAT-EVT-F07 | `occurred_at` | Event occurrence time | Required; UTC; public timestamp convention RFC 3339; precision NC. |
| DAT-EVT-F08 | `trace_id` | Cross-boundary trace | Required; encoding/length NC; no document or secret content. |
| DAT-EVT-F09 | `payload` | Event-specific content | Required; exact field schema NC; validate before mutation. |

**Source:** [DDS], p. 48, §13.1.1.  
**Earlier trace:** `API-COM-006`.

Actor and correlation attribution are required at durable boundaries but are not listed as properties in this envelope. Their carrier remains **Needs confirmation — OQ-DAT-013**; do not invent mandatory `actor_id` or `correlation_id` envelope extensions.

#### Catalogued Events

The source’s payload descriptions are conceptual, not exact JSON keys.

| Event literal | Producer | Confirmed payload content | Consumer effect / data relationship | Source |
|---|---|---|---|---|
| `CaseCreated` | Case Service | Case ID/revision | Classifier; DAT-003/020. | [DDS], p. 87, §C.1. |
| `DocumentNormalized` | Ingestion | Version ID/source hash | Indexer; DAT-006/007/023. | [DDS], p. 87. |
| `SearchIndexCommitted` | Indexer | Index generation/document revision | Query-cache invalidation; DAT-023/027. | [DDS], p. 87. |
| `AgentPlanApproved` | Orchestrator | Run ID/plan hash | Dispatch plan steps; DAT-008/009. | [DDS], p. 87. |
| `ApprovalDecisionRecorded` | Policy Service | Task/actor/content hash | Validate publication; DAT-011/012/025. | [DDS], p. 87. |
| `WorkflowStageAdvanced` | Orchestrator | Run/stage/checkpoint | Resume consumers; DAT-008/009/026. | [DDS], p. 87. |
| `AccessDenied` | Policy Service | Principal/action/policy digest | Alert enrichment and non-disclosing denial evidence; DAT-013/019. | [DDS], p. 87. |
| `TenantDeletionVerified` | Retention Worker | Manifest ID/receipt hash | Close purge record; DAT-018/029. | [DDS], p. 87. |

Additional source-named events remain part of the event data vocabulary, but producer, precise trigger, and payload require confirmation:

| Event literal | Related data / source | Missing contract |
|---|---|---|
| `BaselineCommitted` | DAT-033; [DDS], pp. 8–10 | Full producer/trigger/payload. |
| `RunRequested` | DAT-008/026; [DDS], pp. 15–17 | Alternate-run creation binding and full schema. |
| `DeploymentPromoted` | DAT-032/036; [DDS], pp. 18–20 | Distinction from `ReleasePromoted`; no health-GET promotion trigger inferred. |
| `CaseStateChanged` | DAT-003/004; [DDS], pp. 24–26 | Change/closure payload. |
| `ConnectorSyncStarted` | DAT-015/021; [DDS], pp. 27–29 | Sync-start payload. |
| `ModelInvocationCompleted` | DAT-016/024; [DDS], pp. 37–39 | Attempt/output/usage payload and failed-attempt semantics. |
| `DataRetentionPurgeCommitted` | DAT-018/029; [DDS], pp. 51–53 | Purge outcome schema. |
| `ApiCompatibilityVerified` | DAT-032/034; [DDS], pp. 54–56 | CI trigger/schema; no OpenAPI-GET verification mutation inferred. |
| `UserReviewOpened` | DAT-011/013/035; [DDS], pp. 57–59 | Actual open trigger/schema; not all evidence/case GETs. |
| `SecurityPolicyChanged` | DAT-017/019/029; [DDS], pp. 61–63 | Hold versus broader policy-change mapping. |
| `SloBurnRateDetected` | DAT-030; [DDS], pp. 64–66 | Detector trigger/schema; not metrics/usage read mutation. |
| `BackpressureActivated` | DAT-036; [DDS], pp. 68–70 | Admission/degradation trigger/schema. |
| `ReleasePromoted` | DAT-032; [DDS], pp. 71–73 | Release binding/schema. |
| `EvaluationCompleted` | DAT-031; [DDS], pp. 74–76 | Completion/scorecard schema. |

**Needs confirmation — OQ-DAT-013:** Preserve the complete event vocabulary already recorded in `02_api.md`, but obtain exact payloads, producers, signatures, routes, and event-to-SSE/webhook mappings. Repetition of a chapter-boundary event name does not authorize a read endpoint to write that event.

### MCP and A2A Data Contracts

#### `knowledge.search@v1`

| Field / literal | Direction | Confirmed type / behavior | Requiredness, defaults, and validation gaps |
|---|---|---|---|
| `query` | Input | `string` | Formal required property, nonempty rule, length, normalization NC. |
| `case_id` | Input | `uuid` | Formal requiredness/omission semantics NC; authorized tenant-scoped case. |
| `max_items` | Input | `int<=10` | Upper bound ten confirmed; lower bound/default/requiredness NC. |
| `evidence_set_id` | Output | `uuid` | Listed output; formal requiredness/nullability NC. |
| `citations` | Output | `Citation[]` | Formal schema, minimum count, nullability NC. |
| `read:permitted_documents` | Authorization | Exact tenant-scoped capability literal | Separate authorization decision required. |
| Effect | Behavior | Read-only; no arbitrary URLs or filesystem access | Tool data does not authorize any write. |

**Source:** [DDS], p. 87, §C.2.  
**Earlier trace:** API-045. These field names and limits are not confirmed public API-009 request properties.

#### A2A Envelope

| Exact property / concept | Data meaning and type evidence | Requiredness / unresolved mapping |
|---|---|---|
| `task_id` | Task identity; JSON string example | Task ID required by §11.2.2; formal ID encoding/default NC. |
| `tenant_id` | Immutable tenant; JSON string example | Tenant context required; placeholder `tenant_example_01` is not a UUID storage decision. |
| `capability` | Versioned capability; JSON string example | Capability reference required; example `research.grounded_search.v1` is not a universal task capability. |
| `input_schema` | Declared input schema reference; JSON string example | Declaration required; example `schema://oriondesk/research-request/1` does not supply the actual schema. |
| Declared output schema | Required concept in §11.2.2 | Example omits it; property name/type NC. No confirmed `output_schema` field invented. |
| `deadline_at` | Deadline; example `2026-11-09T08:00:00Z` | Deadline required; timestamp precision/expiry semantics NC. |
| `trace_id` | Trace context; JSON string example | Trace context required; correlation carrier NC. |
| `authorization_ref` | Separate grant reference; JSON string example | Formal requiredness and grant-resolution schema NC; reference alone is not proof of permission. |
| `payload` | Typed task input; example object with `case_id` and `query` | Required according to declared task schema; general payload schema and placeholder-to-ID mapping NC. |
| Durable actor/revision/time/correlation attribution | Required where handoff changes durable state | Carrier relative to this example NC. |

**Sources:** [DDS], p. 41, §11.2.2; p. 87, §C.2.  
**Earlier trace:** API-046/OQ-API-028.  
**Open:** OQ-DAT-013/OQ-DAT-024. Receiver decline/result schema, signatures, transport, and deduplication are not supplied.

### Configuration Example Interpretation

The source’s YAML-shaped example preserves the following exact keys and literals:

| Area | Source example | Implementation interpretation |
|---|---|---|
| Release | `release: r1.0` | Example configuration label; not a new mapping replacing document release `R1.0`. |
| Workflow | `max_plan_depth: 8`, `max_tool_calls: 16`, `run_timeout_seconds: 180`, `replay_dedup_hours: 24` | Depth/call maxima independently confirmed in Chapter 11. Timeout and replay-ledger deployment settings remain unresolved. |
| Retrieval | `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `embed_dimension: 1536`, `hybrid_rrf_k: 60` | Embedding dimension independently confirmed in index schema. Other values are example configuration, not page sizes or new DB constraints. |
| Policy | `auto_publish_classification: INTERNAL`, `require_human_review_for: [HIGH_RISK, RESTRICTED]`, `self_approval_allowed: false` | Examples do not make every `INTERNAL` result automatically publishable. All evidence/authorization/gate checks still apply. |
| Storage | `upload_limit_mb: 25`, `user_data_region: primary-approved-region` | Cap independently described in ingestion; MB interpretation remains unresolved. Region is a placeholder, not approval. |
| Observability | `trace_sample_rate: 0.10`, `diagnostic_retention_days: 30`, `audit_retention_years: 7` | Sampling is example-only; diagnostic/audit retention also described in §18.3.2 but corporate selection remains open. |

**Source:** [DDS], p. 90, Appendix F; independent requirements pp. 30, 34, 40, 66.  
**Open:** OQ-DAT-005/015/018/025.

### Data Acceptance Criteria

Tests with unresolved schemas must verify the confirmed invariant and defer exact field/transport assertions to the linked open contract. They must not use implementation-selected values as if approved.

| Acceptance ID | Prerequisites / action | Expected data result | Requirement and source trace |
|---|---|---|---|
| AC-DAT-001 | Create a valid authorized case through API-001 | One case identity, initial `NEW`, source DDL revision `1` and sensitivity `INTERNAL` under resolved create semantics; correct tenant/workspace association. | DAT-003; API-001; [DDS], pp. 12, 83, 86. |
| AC-DAT-002 | Same actor/body/key within case-domain contract; repeat creation | One case and identical original response/outcome; no duplicate business creation. | DAT-LC-016; `TST-001`; [DDS], pp. 25, 89. |
| AC-DAT-003 | Reuse key with changed body | HTTP `409 IDEMPOTENCY_CONFLICT`; no second outcome under key. | `TST-002`; [DDS], p. 89. |
| AC-DAT-004 | Attempt duplicate `cases.id` or `(tenant_id,id)` under reference schema | PK/unique constraints prevent duplicate stored identity. No inferred tenant-only relaxation of global PK. | DAT-003-F01/F09; [DDS], p. 86. |
| AC-DAT-005 | Insert/change case with nonexistent tenant/workspace | Declared case FKs reject invalid references. | DAT-REL-001/002; [DDS], p. 86. |
| AC-DAT-006 | Case tenant and referenced workspace tenant differ | Production FK/procedure enforcement rejects cross-tenant workspace association; business state unchanged. | DAT-COM-003; [DDS], p. 86. Enforcement method NC. |
| AC-DAT-007 | Foreign-tenant read or resource-ID substitution | No private data/existence leak; same `404`-equivalent class as absent resource. | `TST-003`, `T-01`; DAT-LC-013; [DDS], pp. 23, 88–89. |
| AC-DAT-008 | Reuse pooled connection across tenants after a transaction | Scoped variables reset; next transaction cannot inherit prior tenant visibility. | DAT-COM-003; [DDS], p. 86. |
| AC-DAT-009 | Save with stale `If-Match` | `409 CASE_VERSION_CONFLICT` with current revision; no stale case/history/outbox business mutation. | DAT-LC-015/016; [DDS], pp. 25, 83–84. |
| AC-DAT-010 | Accepted case mutation; inject failure before transaction commit | Business mutation/history and associated outbox do not diverge through partial commit. | DAT-LC-015; [DDS], p. 52. Complete history transaction design OQ-DAT-014. |
| AC-DAT-011 | Attempt case status outside exact DDL vocabulary | Source `CHECK` rejects it; supported transition guards also prevent invalid business transitions. | DAT-CODE-001; [DDS], pp. 25, 86. |
| AC-DAT-012 | Attempt historical case-revision or approval-decision modification | Append-only/immutable history remains unchanged. | DAT-004/012; DAT-LC-014; [DDS], pp. 62, 85. |
| AC-DAT-013 | Classification completion followed by correction | Labels/confidences/provenance retained under resolved schema; correction requires reason code and durable attribution. | DAT-020; SCR-002-A04; [DDS], p. 12. |
| AC-DAT-014 | Evaluate priority/deadline with resolved input/calendar fixtures | Priority uses explicit impact/urgency, not model output alone; advisory prediction cannot alter contractual deadline. | DAT-003-F12–F17; [DDS], p. 25. |
| AC-DAT-015 | Authorized supported upload, matching MIME/extension and resolved cap | Accepted durable ingestion; scan precedes parse; macros do not execute; remote references not fetched; no immediate false `READY`. | DAT-FILE-001; API-006; [DDS], pp. 30, 83. |
| AC-DAT-016 | Unsafe/polyglot/bomb or oversized/mismatched file | Fail closed; unsafe content quarantined and never indexed. Exact size unit/threshold/error tests wait for OQ-DAT-010. | `T-04`, `TST-015`; [DDS], pp. 30, 88–89. |
| AC-DAT-017 | Reprocess source under changed parser/pipeline version | Side-by-side immutable derivatives preserve prior source claims and cited-version identity. | DAT-006/007; DAT-LC-014; [DDS], p. 31. |
| AC-DAT-018 | Resolve each generated citation | Stored chunk/version/source anchor resolves under current permission; page range highlights correctly after anchor contract resolution. | DAT-007/010; SCR-COM-006; [DDS], pp. 31, 35, 57. |
| AC-DAT-019 | Authorized low-quality document | Remains viewable through resolved safe viewer; excluded from autonomous recommendations. No quarantined-active-content viewing inferred. | DAT-022-F04; [DDS], pp. 30–32. |
| AC-DAT-020 | Mixed permitted/forbidden evidence search | Only permitted chunks/text reach result/generation; source ACL remains authority. | DAT-LC-013/017; [DDS], pp. 21–23, 34–36. |
| AC-DAT-021 | Revoke indexed source permission and query next | No forbidden evidence; affected caches invalidated before new result. | `TST-004`, `T-08`; [DDS], pp. 27–29, 88–89. |
| AC-DAT-022 | Evidence confidence/quality insufficient | `NO_SUPPORTED_EVIDENCE`, supported clarification, or human route; no fabricated evidence content. | DAT-010/023; [DDS], p. 36. |
| AC-DAT-023 | Failed index write after accepted source metadata | Accepted source data remains durable; fingerprint reconciliation/outbox recovery restores derivative consistency. | DAT-LC-017; [DDS], pp. 49, 90. |
| AC-DAT-024 | Rebuild index generation | Old readable generation remains until completeness/recall checks pass; read alias switches atomically. | DAT-023; [DDS], p. 34. Thresholds NC. |
| AC-DAT-025 | Inspect cache keys/results and change authorization | All five required key dimensions present; affected results purged before ordinary TTL expiry. | DAT-027; [DDS], p. 53. |
| AC-DAT-026 | Inspect search row/vector contract | Tenant/workspace/version/chunk/language/classification/text present; embedding dimension **1536**; no public raw-vector projection inferred. | DAT-023-F01/F02; [DDS], p. 34. |
| AC-DAT-027 | Allocate admitted run and execute steps | Durable plan revision precedes side effects; each checkpoint precedes downstream dispatch; depth/call limits enforced. | DAT-008/009; [DDS], pp. 40, 49. |
| AC-DAT-028 | Refresh UI and reconnect retained SSE position | Server records reconstruct progress; monotonic scoped retained backfill; no workflow duplication from refresh. | DAT-034-F01; API-015; [DDS], pp. 55, 58. |
| AC-DAT-029 | Replay same event 100 times and deliver stale revisions | Exactly one accepted business transition; duplicate/stale handling does not rely on cross-partition order. | `T-07`, `TST-007`; DAT-LC-016; [DDS], pp. 48, 88–89. |
| AC-DAT-030 | Replay dead letter without reason/dry-run/scope, then valid bounded replay | Invalid replay cannot proceed; valid replay preserves original event identity unless explicit migration carries provenance. | DAT-026; API-038; [DDS], p. 50. |
| AC-DAT-031 | Model output has unknown fields, invalid citations, or control injection | `MODEL_OUTPUT_INVALID`; no publication; evidence cannot become tool/tenant/approval authority. | DAT-024; `TST-005`, `T-02`; [DDS], pp. 38–39, 88–89. |
| AC-DAT-032 | Provider outage with restricted context | No unapproved region/deployment fallback; approved equal-or-stronger data-handling constraint preserved. | DAT-024-F01; `T-06`; [DDS], pp. 37, 88. |
| AC-DAT-033 | Current run exhausts quota; observe usage | Terminal current-run outcome, no automatic model/class switch; actual usage remains attributable under resolved ledger grain. | DAT-016; [DDS], p. 38. |
| AC-DAT-034 | Recompute deterministic evaluation with retained inputs/rule version | Normalized inputs and actual rule version support reproducibility; digest alone is insufficient; result cannot be overwritten by LLM tags. | DAT-017; [DDS], p. 44. |
| AC-DAT-035 | Reviewer obtains exact task context | Exact candidate, citations, model/prompt versions, policy reasons available; source inspection possible before approval. | DAT-011/025; SCR-005; [DDS], pp. 57–58. |
| AC-DAT-036 | Submit prior/wrong artifact hash | Decision rejected as stale and audited; changed artifact cannot publish under old approval. | `TST-006`, `T-03`; [DDS], pp. 44–46, 88–89. |
| AC-DAT-037 | High-risk author attempts self-approval | Independent authorized review required; no self-approved high-risk publication. | DAT-011/012; [DDS], pp. 11, 13. Broader scope NC. |
| AC-DAT-038 | Task expiry or unauthorized override | No implicit approval; escalation/reassignment recorded. Override cannot bypass elevated-role/secondary-reviewer/audited-reason requirements. | DAT-011/012; `TST-010`; [DDS], pp. 45–46, 89. |
| AC-DAT-039 | Publication transaction interrupted or replayed with changed artifact | Gate/pointer cannot partially commit; one accepted artifact binding; current authorization/evidence rechecked. | DAT-025; DAT-LC-015; [DDS], pp. 45–46, 52. |
| AC-DAT-040 | Authorized closure/reopen/rework under resolved guards | Closed snapshot preserves approved answer/cited versions/decisions; reopen/new-run revision does not overwrite historical approval or denial. | DAT-004/025; [DDS], pp. 25–26, 46. |
| AC-DAT-041 | Partial sync failure or poison record | Cursor advances only after durable preceding outcomes; exceptions remain recorded; bounded malformed-record retries then quarantine. | DAT-015/021; [DDS], pp. 28–29. |
| AC-DAT-042 | Revoke queued connector credentials or omit capability support | Queued work fails `CONNECTOR_REAUTH_REQUIRED` without tokens; missing capabilities produce explicit warning, not silent assumptions. | DAT-021; [DDS], p. 27. |
| AC-DAT-043 | Attempt historical audit edit; query as Auditor | Append-only hash-chain evidence remains intact; authorized redacted metadata returned; no general case-edit access. | DAT-013; `T-09`; [DDS], pp. 11, 62, 88. |
| AC-DAT-044 | Inspect provider requests, logs, traces, errors, exports, and development data | No out-of-scope secrets/documents/full prompt disclosure; permitted PII redaction and synthetic development/staging rules applied. | DAT-LC-025; `T-05`; [DDS], pp. 19, 62–64, 79, 84, 88. |
| AC-DAT-045 | Read usage rollups | Separate model/embedding/storage/indexing attribution with cost-center/deployment-version context and source-supported budget/forecast/rejected-excess data. | DAT-016/030; [DDS], p. 65. Units/formulas NC. |
| AC-DAT-046 | Replace expected fixtures or evaluate low-confidence/regressed safety result | Frozen version/signed-manifest verification prevents uncontrolled fixture replacement; release blocked for low confidence or critical isolation/approval failure regardless of model score. | DAT-031; `T-12`, `TST-016`; [DDS], pp. 74–76, 88–89. |
| AC-DAT-047 | Run frozen reference evaluation | Preserve 1,200-case reference and targets `>=0.97`, `<=0.02`, `1.00`; retain expected citations/decisions, domains/statistical evidence, seeds, signed release-linked outputs. | DAT-031; [DDS], pp. 75, 89. |
| AC-DAT-048 | Single Admin requests export/deletion | Independent approval checks prevent execution bypass. | DAT-029-F04; `T-11`; [DDS], pp. 78, 83, 88. |
| AC-DAT-049 | Properly authorized export | Manifest/package includes case metadata, approved artifacts, source references, audit manifests/checksums; excludes secrets/internal prompts. | DAT-FILE-004; [DDS], p. 79. Format NC. |
| AC-DAT-050 | Purge under legal hold | Protected records retained and receipted; eligible targets tombstoned/removed/receipted; no false complete deletion of held data. | DAT-018/029; `TST-013`; [DDS], pp. 80, 89. |
| AC-DAT-051 | Retry provisioning/backfill and inspect readiness | One idempotent provisioning outcome; incomplete state blocks sync; stable source IDs and batch receipts retained; readiness uses coverage, not empty queue. | DAT-029; [DDS], p. 78. |
| AC-DAT-052 | Apply incompatible schema removal or rollback new binary | Active-reader compatibility protected; bounded backfill before constraint enforcement; no automatic DB down-migration; release bindings reconstructible. | DAT-LC-026; [DDS], pp. 52, 55, 72–73. |
| AC-DAT-053 | Regional recovery exercise | Relational/object/index consistency restored within reference RPO `<=15 minutes`, RTO `<=4 hours`. | DAT-LC-024; `TST-012`; [DDS], pp. 69, 89. |
| AC-DAT-054 | Vector/model degradation or failed webhook | Safe manual/evidence workflows continue where supported; reduced-quality flag visible; no ACL/approval bypass; webhook failure does not undo accepted case state. | DAT-LC-017; DAT-034; [DDS], pp. 55, 69, 79. |

### Capacity and Test-Data Boundaries

| Source value | Data-specification interpretation |
|---|---|
| 100,000 indexed documents per tenant maximum; 20 concurrent AI runs per large tenant | Reference workload envelope, not newly selected SQL constraints or quotas. |
| Typical 1 MB source produces approximately 40–120 chunks | Sizing estimate dependent on content/parser quality; not a required chunk count or per-document bound. |
| Raw files, normalized text, vectors, and replication overhead tracked separately | Preserve distinct capacity measures; units/allocation formulas NC. |
| 2,000 daily active users; 60 requests/s steady; 180 requests/s burst | Synthetic reference load for data/integration tests; no new membership or API limits inferred. |
| Case-create P95 within/under 300 ms; search P95 under 1.5 s excluding remote connector fetch | Preserve preceding SLO questions; measure data/API outcome, not full UI rendering. Exact case threshold wording remains unresolved. |
| Successful, empty, mixed-permission, adversarial, malformed synthetic fixtures; randomized seeds | Required verification coverage and reproducibility. |
| Critical isolation and approval tests | Zero-exception acceptance; benchmark quality cannot offset failure. |

**Sources:** [DDS], pp. 12, 65, 68, 74–76, 88–89.  
**Open:** OQ-DAT-020/022/025; preceding OQ-API-033.

## Consistency and Open Questions

### Field Mapping and Preceding-Specification Consistency

| Mapping ID | Data mapping preserved | Preceding screen/API identifiers | Status and required treatment |
|---|---|---|---|
| MAP-DAT-001 | Current case ID/scope/status/revision/sensitivity/times | SCR-002-F01/F07/F08/F10/F12/F13; API-CASE-F01–F03/F09/F10/F12/F14/F15 | **Confirmed reference storage fields.** Public JSON projection and forms remain unresolved. |
| MAP-DAT-002 | Title/description/impact/urgency/priority/owner/approved pointer/deadline | SCR-002-F02–F06/F09/F11/F24; API-CASE-F04–F08/F11/F13/F18 | **Confirmed logical data; physical names/schema NC.** Proposed screen placement not promoted. |
| MAP-DAT-003 | Classification/correction | SCR-002-F14–F17/A04; API-CASE-F16/F17; API-GAP-001 | Preserve reason-code condition and provenance; physical/wire contract NC. |
| MAP-DAT-004 | File/OCR/document/quality data | SCR-002-F18–F21; SCR-003-F12/F13; API-006/007/OQ-API-009 | Source formats/safety confirmed; upload controls/schema/thresholds still unresolved. |
| MAP-DAT-005 | Citation/version/anchor/title/hash/ACL data | SCR-003-F03–F11; API-EVID-F01–F10/F13; API-008–010/045 | Preserve content requirements; exact IDs, `Citation`, source URLs, and anchor structures NC. |
| MAP-DAT-006 | Run/plan/step/checkpoint/budget/failure/evidence | SCR-004-F01–F11; API-011–015/037 | Source durable data confirmed; full states/projections and transport gaps retained. |
| MAP-DAT-007 | Exact review decision/context/gate | SCR-005-F01–F18; SCR-002-F25–F34; API-016/017 | Exact binding/capture confirmed; requested decision/rationale property mappings in P-API-002 remain proposals. |
| MAP-DAT-008 | Connector/cursor/error/credential/readiness | SCR-006-F01–F13; API-018/019/049 | Preserve selected `cursor`, `watermark`, `retry_state`; full sync schema and lower-trust behavior NC. |
| MAP-DAT-009 | Workspace settings/deployment/tool/reviewer policy | SCR-007-F01–F15; API-020; API-GAP-002 | Admin activity confirmed; control placement and policy APIs not established. |
| MAP-DAT-010 | Audit/digest/access/decision evidence | SCR-008-F01–F11; API-021 | Append-only authorized data confirmed; actor/action/detail/redaction projections NC. |
| MAP-DAT-011 | Usage/quality | SCR-010-F01–F10; SCR-011-F01–F11; API-022–024 | Data/targets confirmed; screen organization, reporting types/calculations, and statuses unresolved. |
| MAP-DAT-012 | Provisioning/holds/export/deletion/replay/release/design | `SCR-X-002`–`SCR-X-009`; API-025/026/028/029/032/033/038/040/043/044 | Source operation data retained; no new screen, table, endpoint, schedule, or operator grant inferred. |
| MAP-DAT-013 | Shared summary/degraded/UI data | SCR-COM-F01–F07; SCR-009; API-GAP-010/API-030 | Illustrated labels do not confirm materialized tables, summary formulas, or selected defaults. |
| MAP-DAT-014 | Event/MCP/A2A contracts | API-COM-006; API-045/046; full API event inventory | Exact names/literals preserved; output-schema omission and attribution carriers remain unresolved. |

### Conflicts and Required Amendments

This specification does not rewrite earlier files. Required amendments must be made through a controlled change after resolution.

| Conflict ID | Evidence and issue | Affected identifiers | Required resolution / amendment |
|---|---|---|---|
| CON-DAT-001 | §B.2 DDL omits title, description, priority, owner, approved result and other Chapter 6 logical data. | DAT-003; `CON-API-011`; SCR-002/API-CASE fields | Complete production schema and wire mappings; omission is not permission to omit supported case functionality. [DDS], pp. 24–26, 85–86. |
| CON-DAT-002 | Generic registers call `Case`/`CaseAggregate` “Immutable derivative,” while prose explicitly defines mutable versioned case state. | DAT-003/004/025; `CON-API-011` | Distinguish current mutable row from immutable revisions/approved snapshots; do not freeze all case fields by register label. [DDS], pp. 13, 24–26. |
| CON-DAT-003 | Generic UUIDv7 identity baseline coexists with fingerprint-plus-pipeline immutable derivative IDs; `document_versions` selected fields omit version ID. | DAT-006/007; DAT-COM-004 | Define identity versus fingerprint derivation and physical version PK. No hash-to-UUID algorithm inferred. [DDS], pp. 31, 51, 85. |
| CON-DAT-004 | `unique(slug)` and global case `id` PK coexist with generic tenant/business-key uniqueness. | DAT-001-F02; DAT-003-F01/F09 | Preserve explicit constraints pending scope decision; do not remove global PK or tenant-root slug uniqueness silently. [DDS], pp. 51, 85–86. |
| CON-DAT-005 | RLS example and simple workspace FK do not alone enforce workspace-to-case tenant match; source explicitly requires additional enforcement. | DAT-COM-003; DAT-REL-001–003; AC-DAT-006/008 | Supply complete production FKs/procedures and RLS/write/session controls. [DDS], p. 86. |
| CON-DAT-006 | Mandatory tenant-owned row scope and durable attribution are absent from many selected-field rows. | DAT-COM-002; DAT-004–018 | Complete physical or linked-record realization without treating selected catalogs as exhaustive. [DDS], pp. 22, 48, 85. |
| CON-DAT-007 | `actor`/`reviewer_id`/`actor_id`; `at`/`occurred_at`/timestamp/`purge_time`; policy `policy_version`/`rule_version`/configuration revision; parser/pipeline names differ. | DAT-004/012/015/017/018; DAT-COM fields | Define explicit semantic mappings and types; similar names do not prove equivalence. [DDS], pp. 25, 31, 44–45, 48, 85. |
| CON-DAT-008 | Review capture requires actor/time/hash/rationale/annotations, but §B.1 decision row only lists selected fields; public P-API-002 uses proposed names. | DAT-011/012/025; SCR-005; API-017/P-API-002 | Add exact immutable binding/capture contract; do not adopt proposed wire property names as confirmed. [DDS], pp. 45, 58, 85. |
| CON-DAT-009 | Set `acl_digest`, response-item ACL digest, source ACL revision and cache user-scope digest have different possible scopes. | DAT-005/010/027; API-EVID-F05 | Define distinct digest inputs/relationships and current-permission checks. [DDS], pp. 31, 35, 53, 85. |
| CON-DAT-010 | Search can be public/read-like without a run; `evidence_sets` selects `run_id`. MCP is read-only but returns an evidence-set ID. | DAT-010/023; API-009/045; DAT-REL-013 | Resolve persistence and nullability for standalone search; do not force every query to allocate a run or write an index event. [DDS], pp. 35, 83, 85, 87. |
| CON-DAT-011 | Every sync run stores cursor/high-watermark/error ledger; §B.1 cursor row keys conceptually by connector and omits sync-run reference. | DAT-015/021; SCR-006; API-019 | Define current cursor versus immutable run history, cursor ownership/concurrency, and durable exception links. [DDS], pp. 28–29, 85. |
| CON-DAT-012 | Missing approval terminates run, `AWAITING_REVIEW` is valid, and recoverable timeout lacks a catalog state. | DAT-008/009; DAT-LC state tables; `CON-SCR-005`, `CON-API-002` | Resolve waiting/failure/timeout representation and review SLA accounting. [DDS], pp. 12, 41, 45, 49, 82, 90. |
| CON-DAT-013 | Close endpoint exists but complete transition into `CLOSED` and reopen/rework revision contracts are absent. | DAT-003/004/008/025; `CON-SCR-006`, `CON-API-003` | Complete guards and revision relationships; retain historical snapshots/denials. [DDS], pp. 25–26, 46. |
| CON-DAT-014 | Role aliases and Auditor evidence path are inconsistent; high-risk self-approval rule versus broader no-self-approval catalog. | DAT-019/011/012; `CON-SCR-007`–`009`, `CON-API-004/005` | Resolve roles/relationships and redacted access path without inferred privileges or weakening high-risk prohibition. [DDS], pp. 11, 22, 83, 85, 90. |
| CON-DAT-015 | Workspace settings associated with case PATCH in §6.1.1. | DAT-002; SCR-007; API-GAP-002; `CON-SCR-010`, `CON-API-006` | Define actual settings APIs and schema; do not bind workspace fields to case mutation solely from association. [DDS], p. 24. |
| CON-DAT-016 | Mandatory actor/correlation attribution absent from enumerated event fields; partial catalog and read/event associations lack triggers. | DAT-014/026/034; DAT-EVT fields; `CON-API-007/008/013/014` | Complete event schemas/attribution/producers/triggers; do not make GETs create business changes by inference. [DDS], pp. 48, 57–59, 87. |
| CON-DAT-017 | A2A placeholder tenant/case strings differ from application UUID baseline; declared output schema missing. | DAT-034; API-046; `CON-API-012` | Define formal types and output-schema carrier; preserve example as nondeployable placeholder evidence. [DDS], pp. 41, 51, 87. |
| CON-DAT-018 | Source lower-trust connector behavior coexists with mandatory ACL/revocation-before-next-query invariant. | DAT-005/015/021/023/027; `CON-SCR-013`, `CON-API-010` | Define safe capability restrictions and source authorization propagation. [DDS], pp. 21–23, 27–29. |
| CON-DAT-019 | Immutable closed citation lineage versus source/tenant deletion and retained legal-hold/audit evidence. | DAT-006/007/012/013/018/025/029 | Define retained reference/snapshot scope and authorized historical retrieval after deletion; do not silently substitute source versions or waive purge/hold rules. [DDS], pp. 26, 51, 62, 80. |
| CON-DAT-020 | Fictional diagnostic/audit policies and example region/configuration coexist with explicit open corporate/provider selections. | DAT-001/002/030/032; DAT-LC-019; `CON-SCR-015`, `CON-API-015` | Approve deployment values and precedence through dated decisions; no owner/date/approval invented here. [DDS], pp. 66, 90. |
| CON-DAT-021 | Error-code snake-case prose differs from uppercase literals; UI status summaries mix aggregate concepts. | DAT-CODE-001–010/035; `CON-SCR-003/012`, `CON-API-009` | Preserve exact literals; define error casing and aggregate-to-visible status mapping. [DDS], pp. 14, 54, 57, 82, 84, 89. |
| CON-DAT-022 | Earlier files describe the Data Specification as future work; `02_api.md` says filename not supplied. | Earlier handoff sections | Controlled amendment may point to `03_data.md`; other later specifications remain ungenerated. No earlier document is rewritten here. |
| CON-DAT-023 | Source says “data subject access requests”; deletion inventory supports them, but request semantics are not defined. | DAT-LC-022; API deletion content/OQ-API-024/025 | Preserve access-request wording; distinguish access/export/erasure without inventing a universal delete outcome. [DDS], p. 80. |

### Open-Decision Register

All entries are **Needs confirmation**. No decision, owner, deadline, or approval is assigned.

| Open ID | Affected data requirements | Missing decision / contract | Preceding specification links and evidence |
|---|---|---|---|
| <a id="oq-dat-001"></a>OQ-DAT-001 | DAT-001–036; DAT-COM-001 | Complete production model, supplementary persistence/aliases, exact writer identities, PostgreSQL deployment details, physical indexes/partitioning | [`02_api.md`](02_api.md): OQ-API-003/027/030. [DDS], pp. 16, 51, 85–86. |
| <a id="oq-dat-002"></a>OQ-DAT-002 | DAT-REL-001–022; DAT-COM-003 | Full PK/FK/unique/nullability/cardinality and cascade/procedure/tenant-reference enforcement | [`02_api.md`](02_api.md): OQ-API-003/005. [DDS], pp. 24, 51, 85–86. |
| <a id="oq-dat-003"></a>OQ-DAT-003 | All field definitions; DAT-COM-002 | Physical/wire types, lengths/precision, nullability/requiredness/defaults, shared-context carriers, actual IDL and property mapping | [`01_screen_functions.md`](01_screen_functions.md): OQ-SCR-004; [`02_api.md`](02_api.md): OQ-API-003/030. [DDS], pp. 55, 82, 85–87. |
| <a id="oq-dat-004"></a>OQ-DAT-004 | DAT-001 | Slug namespace/normalization/rename, plan/region codes, root identity and provisioning contract | OQ-API-025/034. [DDS], pp. 78, 85, 90. |
| <a id="oq-dat-005"></a>OQ-DAT-005 | DAT-002; DAT-017/032 | Workspace/settings schema, policy/config/version distinctions, quotas/calendars, activation/precedence, actual policy APIs | OQ-SCR-008/020; OQ-API-020/025. [DDS], pp. 24–25, 44, 78, 90. |
| <a id="oq-dat-006"></a>OQ-DAT-006 | DAT-003; MAP-DAT-001/002 | Full case storage/create/edit schemas, UUID/business number, owner relationship, priority/SLA formulas and input vocabularies | OQ-SCR-004/006/008; OQ-API-007. [DDS], pp. 12, 24–25, 85–86. |
| <a id="oq-dat-007"></a>OQ-DAT-007 | DAT-004/025; DAT-LC-014/018 | Revision keys/patch/actor/time semantics, closure/reopen/rework linkage, snapshot/history reconstruction and retention | OQ-SCR-018; OQ-API-005/007/012. [DDS], pp. 25–26, 46, 85. |
| <a id="oq-dat-008"></a>OQ-DAT-008 | DAT-005–007/020/022/028 | Document/version/chunk/source identity, UUID-versus-fingerprint derivation, parser/pipeline versions, immutable uniqueness, state placement, source-delete lineage | OQ-SCR-009/010; OQ-API-009/010. [DDS], pp. 30–35, 51, 85. |
| <a id="oq-dat-009"></a>OQ-DAT-009 | DAT-007/010; DAT-COM-004 | Formal Citation/evidence ID mapping; page/range/bbox/non-PDF anchor schemas; hash/digest inputs, algorithms and encodings | OQ-SCR-010; OQ-API-010/028. [DDS], pp. 31, 35, 57, 87. |
| <a id="oq-dat-010"></a>OQ-DAT-010 | DAT-022/028; DAT-FILE-001/002 | File transports/allowlist/size units/bounds/decompression, corrupted/encrypted input, text/HTML encoding, OCR/defaults, quality thresholds, derivative serialization, safe quarantine/source access | OQ-SCR-009; OQ-API-009/010. [DDS], pp. 10, 30–32, 52. |
| <a id="oq-dat-011"></a>OQ-DAT-011 | DAT-010/023; DAT-LC-017 | Search provider schema/vector type/analyzers, aliases/coverage/recall checks, standalone evidence persistence, result ordering/budgets/degraded flags | OQ-SCR-011/028; OQ-API-011/031/034. [DDS], pp. 34–36, 69, 78, 90. |
| <a id="oq-dat-012"></a>OQ-DAT-012 | DAT-027; DAT-LC-017 | Cache product/key encoding/digest scopes/value schema/TTL/atomic invalidation and safe authorization-race behavior | OQ-API-019/027. [DDS], pp. 16, 28, 53. |
| <a id="oq-dat-013"></a>OQ-DAT-013 | DAT-014/026/034; DAT-EVT fields/event inventory | Outbox/consumer/idempotency/queue/dead-letter schemas, signatures/triggers/routes, actor/correlation, dedup history/replay provenance, event-to-SSE/webhook mapping | OQ-SCR-013/021/027; OQ-API-004/027/035. [DDS], pp. 17, 25, 48–50, 55, 87, 90. |
| <a id="oq-dat-014"></a>OQ-DAT-014 | DAT-COM-003; DAT-LC-013/015/016 | Complete RLS/write/session controls, isolation/locks, revision transport, atomic allocation, audit/idempotency result failures, relational/object and legal-hold concurrency | OQ-API-004/005/024/027. [DDS], pp. 22, 25, 45, 52, 80, 86. |
| <a id="oq-dat-015"></a>OQ-DAT-015 | DAT-008/009/024/025 | Run/step/DAG/budget/checkpoint/rework schemas, waiting/missing approval, timeout and failure states, call/retry accounting, artifact status mapping | OQ-SCR-012/013; OQ-API-012–014/017. [DDS], pp. 12, 40–42, 49, 82, 90. |
| <a id="oq-dat-016"></a>OQ-DAT-016 | DAT-011/012/013/025 | Review identity/context/hash/rationale/annotation/schema, pools/SLA/races/self-approval/override evidence, audit integrity/redaction/detail projection | OQ-SCR-003/014–017/021; OQ-API-015–018/021. [DDS], pp. 11, 44–46, 58, 62, 85. |
| <a id="oq-dat-017"></a>OQ-DAT-017 | DAT-019/022/024/028/029; DAT-LC-025 | Identity/role mappings, PII tags/redaction, safe source URLs/rendering, retained actor identities, vault references/encryption-key isolation/rotation | OQ-SCR-002/003/010/030; OQ-API-001/002/010/034. [DDS], pp. 10, 21–23, 52, 62–63, 90. |
| <a id="oq-dat-018"></a>OQ-DAT-018 | DAT-018/025/029/030; DAT-LC-018–024 | Hold/tombstone/inventory/receipt schemas, approved retention, object/history/audit survival, independent approvals, legal-hold partial outcomes, backup/delete/citation interaction, execution schedules | OQ-SCR-025/026/030; OQ-API-024/025/034. [DDS], pp. 26, 51, 62, 66, 78–80, 85, 89–90. |
| <a id="oq-dat-019"></a>OQ-DAT-019 | DAT-005/015/021/029 | Connector/source namespaces/capabilities/ACL mapping, current versus per-run cursor history, sync concurrency/retries/ledger/quarantine/remediation and safe lower-trust mode | OQ-SCR-019; OQ-API-019/034. [DDS], pp. 27–29, 78, 85, 90. |
| <a id="oq-dat-020"></a>OQ-DAT-020 | DAT-002/016/030/036 | Usage/ledger grain/reservations/quota windows/token types/currency/cost attribution/rollup/forecast/sizing/admission thresholds | OQ-SCR-023; OQ-API-022/033. [DDS], pp. 38, 65, 68–69, 85. |
| <a id="oq-dat-021"></a>OQ-DAT-021 | DAT-017/024/025 | Normalized policy inputs/reasons/rule-version references/result schema, reproducibility and exact artifact/evidence binding | OQ-SCR-008/014/020; OQ-API-015/017/020. [DDS], pp. 44–46, 58, 85. |
| <a id="oq-dat-022"></a>OQ-DAT-022 | DAT-031/032/033; DAT-LC-026 | Evaluation/test/dataset/signature/statistical/domain/status schemas, release/design/version records, actual IDL/migrations/backfill limits and compatibility evidence | OQ-SCR-024/027; OQ-API-023/026/027/030. [DDS], pp. 8–10, 52, 55, 71–76, 88–89. |
| <a id="oq-dat-023"></a>OQ-DAT-023 | DAT-FILE-003–008; DAT-018/029 | Audit/export/receipt file structures/names/encoding/checksum/signature/snapshot/download/lifetime and authorized inventory projection | OQ-SCR-025; OQ-API-021/024/027. [DDS], pp. 62, 78–80, 85. |
| <a id="oq-dat-024"></a>OQ-DAT-024 | DAT-034; DAT-INT-001–010 | Exact serialization/canonicalization/encoding/time precision/authority; cursors/SSE gaps/history; A2A output/decline and webhook schemas/security; complete errors/code casing | OQ-SCR-013/027/029/031; OQ-API-014/028/029/032/035. [DDS], pp. 41, 48, 54–56, 59, 84, 87. |
| <a id="oq-dat-025"></a>OQ-DAT-025 | Storage responsibilities; DAT-001/024/028/032/036 | Approved provider/region/search/IdP/model deployments/connector permissions/corporate retention, backup services, encryption hierarchy and performance/load selections | OQ-SCR-030/031; OQ-API-033/034. [DDS], pp. 10, 19, 69, 90. |
| <a id="oq-dat-026"></a>OQ-DAT-026 | DAT-035/036; MAP-DAT-013 | UI summary formulas/scope/fields/refresh, persistent ViewState/Notification/locale choices, status/degraded/health/capacity projections and associated APIs | OQ-SCR-001/006/022/028/031; OQ-API-031/036. [DDS], pp. 7, 57–59, 68–70. |

### Proposal Status

| Proposal source | Status in this specification |
|---|---|
| `P-SCR-001`, `P-SCR-002`, `P-SCR-003` in `01_screen_functions.md` | Remain **unapproved** screen hierarchy/new-case/control-placement proposals. They do not determine data persistence or editable columns. |
| `P-API-001` in `02_api.md` | Remains **unapproved** token carrier. It does not select session storage, claim names, or cookie schema. |
| `P-API-002` in `02_api.md` | Remains **unapproved** public JSON mapping. Similarity to physical field names or MCP names does not confirm a public schema. |
| New data-design proposals | None selected or approved by this specification. Source-permitted FK versus controlled-write-procedure alternatives remain unresolved choices, not implementation authority to decide silently. |

### Dependencies and Later Handoffs

| Specification / dependency | Required handoff |
|---|---|
| [`01_screen_functions.md`](01_screen_functions.md) | Preserve SCR fields/actions and open questions. DAT field mappings support the source data but do not approve proposed controls, routes, summaries, or screen hierarchy. |
| [`02_api.md`](02_api.md) | Preserve API/API-CASE/API-EVID/event identifiers and wire-versus-storage distinctions. Resolve schemas and missing interfaces through controlled amendments, not new inferred APIs. |
| Exception Handling Specification | **To be defined in a later stage.** Carry failed/unsupported/quarantined/expired/stale/partial states, safe errors, hash and revision conflicts, SSE gaps, retry permanence, and hold-safe completion. |
| Workflow / Business Rule Specification | **To be defined in a later stage.** Resolve priority/calendar/SLA, closure/reopen/rework, review routing/expiry/override, publication, run waiting/timeout, cursor/trust and purge eligibility. |
| Security / Nonfunctional Specification | **To be defined in a later stage.** Resolve full role/action/attribute model, RLS/service grants, PII/redaction, source access/rendering, signatures, provider approval, key isolation/rotation, and precise SLO measurement. |
| Operations Specification | **To be defined in a later stage.** Resolve provisioning/backfill, retention/export/deletion/holds, reconciliation/replay, event history, migration/rollback, backup/failover, and protected operational contracts. No schedule or operator assignment is created here. |
| Stage 8 decision consolidation | **To be defined in a later stage.** `08_architecture_decision.md` must consolidate unresolved items from completed Markdown specifications, linking to `03_data.md` DAT/OQ/CON IDs and affected IDs in `01_screen_functions.md` and `02_api.md`. No decision, owner, deadline, or approval is invented by this document. |
