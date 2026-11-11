# 3. Data Specification

## Data Inventory and Relationships

### Baseline, Evidence and Design Boundaries

This specification defines data requirements for OrionDesk AI **OD-AI-DDS-001, R1.0 / revision 1.3**. It preserves identifiers from [01_screen_functions.md](01_screen_functions.md) and [02_api.md](02_api.md).

**Source** means `1794310747-OrionDesk_AI_Detailed_Design_Specification.pdf`. All page references are original PDF pages.

- **Confirmed:** Explicit source-supported fields, constraints and behavior.
- **Needs confirmation:** Missing schema details or unresolved source conflicts. These require a recorded decision before implementation lock.
- **Proposal:** Suggested physical or logical design, not an approved requirement.

`DAT-*` identifiers are assigned here for traceability. Exact source table and field names are retained.

**DAT-R-001 — Confirmed:** PostgreSQL is authoritative for mutable metadata and case state; encrypted private object storage holds original and normalized artifacts; hybrid vector/keyword indexes hold nonauthoritative searchable derivatives; caches hold versioned ephemeral results with short TTLs. The orchestrator has no direct database credentials. No datastore is publicly exposed.  
**Evidence:** Source, pp. 7, 9, 16, 18, §§1.3.1, 3.2.2, 4.1.1.

PostgreSQL is a source-confirmed baseline choice, not a new design selection. Its version, hosting product, partition implementation, additional column types and indexes **Need confirmation**. Exact search and object-storage providers remain unresolved in Source, p. 90, §F.2.

### Canonical Relational Inventory

All table names below are **Confirmed** by Source, p. 85, §B.1. Relationships are logical unless explicit DDL is identified. Service ownership is confirmed where Chapter 3 assigns it; otherwise the administrative data owner **Needs confirmation**.

| ID | Table / logical entity | Purpose and owning boundary | Relationships and cardinality | Screen / API mapping |
|---|---|---|---|---|
| DAT-001 | `tenants` | Tenant identity, plan and region; administrative owner Needs confirmation | Tenant groups workspaces; precise provisioning minimum Needs confirmation | Shared context; API-027, API-056 |
| DAT-002 | `workspaces` / Workspace | Policy and quota scope; domain configuration boundary | Each tenant-owned workspace belongs to a tenant; groups users, connectors and cases | SCR-007; API-028, API-050, API-056 |
| DAT-003 | `cases` / CaseAggregate / CaseRow | Current versioned case aggregate; Case Service | Each case belongs to one tenant and one workspace; separate attachment and run references | SCR-001–002; API-001–005 |
| DAT-004 | `case_revisions` / CaseRevision | Append-only case change history; Case Service | Revisions reference a case; exact initial-history rule and key Needs confirmation | SCR-002-F09; API-004–005, API-057 |
| DAT-005 | `documents` / SourceDocument | Stable source identity, classification and source access | Workspace-scoped document; document has versions; exact source-key uniqueness Needs confirmation | SCR-002–003, SCR-006; API-006–007, API-048 |
| DAT-006 | `document_versions` / DocumentVersion | Immutable source/parser/object references; ingestion boundary | Each version references a document; attachments reference exact immutable versions | SCR-003-F03–F07; API-006–007, API-039, API-054 |
| DAT-007 | `chunks` / ChunkAnchor | Anchored chunk identity and text fingerprint; ingestion boundary | Each chunk references a document version; chunks can be selected into evidence sets | SCR-003-F04–F06; API-013–015, API-045 |
| DAT-008 | `runs` / AgentRun | Current bounded execution state; Orchestrator via scoped APIs | Each run references a case; separate steps, evidence, policy and approvals | SCR-002, SCR-004; API-008–012, API-037 |
| DAT-009 | `run_steps` / WorkflowCheckpoint | Idempotent steps and durable checkpoints; orchestration boundary | Each step references a run; plan/checkpoint mapping Needs confirmation | SCR-004-F03–F05; API-011, API-037–038 |
| DAT-010 | `evidence_sets` / EvidenceSet | Selected chunks and ACL validation evidence; retrieval boundary | References run and chunk collection; standalone search association Needs confirmation | SCR-003, SCR-005; API-013–015, API-045 |
| DAT-011 | `approval_tasks` / ApprovalTask | Reviewer routing and exact artifact binding; Policy Service | Each task references run; exact number of tasks per run Needs confirmation | SCR-005; API-016–017 |
| DAT-012 | `approval_decisions` / ReviewDecision | Immutable reviewer decision; Policy Service | Decision references task and reviewer; repeated-decision cardinality Needs confirmation | SCR-005-F08–F11; API-017 |
| DAT-013 | `audit_events` / AuditEntry | Append-only security and business lineage; independently retained audit boundary | Actor/tenant context; links to transition evidence; exact linkage schema Needs confirmation | SCR-008; API-021 |
| DAT-014 | `outbox_events` / OutboxRecord / OutboxTable | Atomically committed event publication; platform messaging boundary | Event references tenant and aggregate revision; one event may have repeated deliveries | API-R-003, API-R-005, API-R-008 |
| DAT-015 | `connector_cursors` / SourceCursor | Durable provider synchronization progress | References connector; cursor scope and number per connector Needs confirmation | SCR-006-F05–F06; API-018–019, API-048 |
| DAT-016 | `token_ledger` / TokenLedger | Attributed provider token consumption; model gateway boundary | References run and deployment; invocation versus rollup granularity Needs confirmation | SCR-010; API-022, API-036, API-049 |
| DAT-017 | `policy_evaluations` / PolicyEvaluation | Reproducible deterministic policy evaluation; Policy Service | References run and rule version; reevaluation history cardinality Needs confirmation | SCR-002-F20, SCR-005-F06; API-017 |
| DAT-018 | `deletion_receipts` / PurgeReceipt | Auditable object purge evidence; retention boundary | Tenant/object reference and purge actor; links to deletion inventory/manifest Needs confirmation | SF-014; API-026, API-040 |

**Relationship evidence:** Source, pp. 16, 24–26, 31, 40–46, 51–53, 85–86.

### Additional Logical Records and Files

Names below are **Confirmed logical source terminology**, not confirmed physical tables. Unless explicitly defined later in this document, physical names, storage selection, schemas, keys, owners and cardinalities **Need confirmation**.

| ID | Logical records / files | Purpose, relationships and ownership evidence | Screen / API mapping | Evidence |
|---|---|---|---|---|
| DAT-019 | Actor, Principal, TenantMembership, AccessPolicy, ResourceAcl | Principal, role bindings, membership and resource ACL; platform identity boundary | Shared permissions; API-027–028 | Source, pp. 11, 21–23 |
| DAT-020 | Attachment | Case-to-immutable-document-version association; Case Service | SCR-002-F14; API-006 | Source, pp. 12, 24, 51 |
| DAT-021 | Connector, SyncRun | Connector capabilities, secret references, sync outcomes and error ledger | SCR-006; API-018–019, API-048, API-055 | Source, pp. 27–29 |
| DAT-022 | ExtractionJob, ContentBlock; original/normalized DocumentBlob | Scan/extraction status, layout, OCR provenance and quality; ingestion boundary | SCR-002-F15–F16, SCR-003-F07–F09; API-006–007, API-039 | Source, pp. 30–32, 52 |
| DAT-023 | SearchChunk, IndexAlias, RetrievalQuery | Search derivatives, versioned aliases and bounded query context; retrieval boundary | SCR-003; API-013–015 | Source, pp. 34–36 |
| DAT-024 | ModelDeployment, PromptTemplate, GenerationAttempt; candidate artifact | Approved model registry, prompt/version lineage and generated content; AI platform boundary | SCR-002-F18, F22; SCR-004-F07; API-020, API-036, API-049 | Source, pp. 37–39, 58 |
| DAT-025 | PlanNode, ToolCapability, A2ATaskEnvelope | DAG dependencies and version-pinned capability/task contracts | SCR-004; API-045–046 | Source, pp. 40–42, 87 |
| DAT-026 | ApprovalAssignment, PublicationGate; closure snapshot | Assignment, satisfied exact-artifact gate and immutable approved closure lineage | SCR-002, SCR-005; API-005, API-017, API-052–053 | Source, pp. 12, 26, 45–46 |
| DAT-027 | QueueEnvelope, DeadLetterEntry; consumer event ledger; idempotency outcome record | Signed tenant context, replay control and duplicate prevention | API-038; API-R-007–008 | Source, pp. 17, 22, 25, 48–50, 54 |
| DAT-028 | CacheEntry, EventCursor, WebhookSubscription | Scoped ephemeral results, SSE offsets and optional webhook delivery | API-012–015, API-047 | Source, pp. 53–55 |
| DAT-029 | ThreatControl, DataClassification, KeyReference; legal hold | Privacy controls, classification, vault references and hold protection | SCR-007–008; API-029 | Source, pp. 61–63 |
| DAT-030 | TraceSpan, MetricSeries, CostLedger, AlertPolicy; daily rollups | Safe diagnostics, usage attribution, budgets and forecasts | SCR-010; API-022, API-041 | Source, pp. 64–66 |
| DAT-031 | CapacityBudget, AdmissionPermit, RecoveryCheckpoint, LoadProfile; backups/rebuild recipes | Admission and recovery inventory | API-031, API-042 | Source, pp. 68–70 |
| DAT-032 | ReleaseArtifact, ConfigVersion, MigrationPlan, RolloutGate; SBOM, signed images/configuration | Reconstructible deployment and migration evidence | API-043–044 | Source, pp. 71–73 |
| DAT-033 | TestCase, EvalDataset, Scorecard, ReleaseGateResult; signed test outputs/dataset manifest | Frozen synthetic evaluation evidence and promotion gate | SCR-010; API-023–024 | Source, pp. 74–76, 88–89 |
| DAT-034 | Runbook, ProvisioningJob, ExportManifest; export package and reconciliation receipts | Idempotent onboarding, checksummed export and verified retirement | SF-014; API-025–026, API-056 | Source, pp. 78–80 |
| DAT-035 | ChangeRequest, DesignRevision, RequirementLink, DecisionRecord | Controlled baseline revisions and linked negative verification | API-032–033 | Source, pp. 8–10 |
| DAT-036 | ApiOperation, ErrorEnvelope, ViewState, ReviewForm, EvidencePanel, Notification | Contract/projection and interaction data; independent persistence not established | SCR-001–008; API-030; API-R-018 | Source, pp. 54–59, 84 |

Source container names such as EdgeGateway, CaseService, VirtualNetwork, APIReplicaSet, WorkerPool and RegionFailoverPlan describe architectural boundaries/configuration contracts, not evidence for additional business tables. Their persistence mappings **Need confirmation**.  
**Evidence:** Source, pp. 17, 20.

## Data Field Definitions

### Definition Conventions and Shared Constraints

**DAT-R-002 — Confirmed:**

1. Baseline identities use UUIDv7. Every tenant-owned row has mandatory `tenant_id`; omission from the selected-field catalog does not exempt a table from tenancy.
2. Durable changes carry tenant, revision, actor, occurrence time and correlation context.
3. Business-key uniqueness is tenant-scoped unless the source explicitly gives another constraint.
4. Physical storage types do not define public JSON types or REST property names.
5. Source §B.1 is a **selected-field catalog**, not complete DDL.

**Evidence:** Source, pp. 22, 51, 85–86; chapter interface-boundary clauses.

For all field tables:

- Exact physical names are confirmed only where provided by the source.
- **All unspecified lengths, precision, physical types, nullability, defaults, field requiredness, PK/FK declarations, uniqueness and ranges mean Needs confirmation.**
- “Logical reference” does not confirm an SQL foreign key.
- “Required semantically” means required to preserve the stated invariant, not a finalized `NOT NULL` declaration.
- No new index, database type, partition scheme or cascade action is authorized.

| Shared field / concept | Meaning and type evidence | Requiredness / constraint | Open definition |
|---|---|---|---|
| `id`, `event_id` and identity references | UUIDv7 identity baseline; `cases.id` physical `UUID` | Stable immutable identity | PK declarations outside `cases`; generation and derivative identity mapping |
| `tenant_id` | Tenant security attribute; `cases.tenant_id` physical `UUID` | Mandatory on tenant-owned rows; included in every access predicate | Physical enforcement for non-case tables |
| `revision`, `aggregate_revision` | Monotonic aggregate/change version | Durable mutation/version context; stale writes rejected | Types outside case revision, increment rules and overflow handling |
| `actor_id` / actor context | Authenticated principal responsible for change | Required durable mutation context | `actor`, `reviewer_id` and token subject mappings |
| `occurred_at` / occurrence time | UTC time; public timestamps RFC 3339 | Required durable mutation context | Timestamp precision and mapping from `at`, `purge_time` |
| `trace_id`, `correlation_id` | Cross-boundary correlation, independent of provider traces | Every request carries both | Length, storage and transport conventions |
| Hash / digest | Content/provenance/integrity evidence | Exact-artifact and source integrity where applicable | Algorithms where not explicit, encoding, serialization and canonicalization |

**Evidence:** Source, pp. 16, 25, 44–48, 51, 54, 59, 64, 85–87.

### DAT-003 — Exact Case DDL Fields

All definitions in this table are **Confirmed reference DDL**, Source, p. 86, §B.2.

| Physical field | Meaning | Type / nullability | Default | Key / value constraint | Earlier mapping |
|---|---|---|---|---|---|
| `id` | Case identity | `UUID`, non-null through PK | None specified | `PRIMARY KEY`; UUIDv7 baseline | SCR-001-F01; API-001–005 `caseId` |
| `tenant_id` | Owning tenant | `UUID NOT NULL` | None specified | `REFERENCES tenants(id)`; `UNIQUE (tenant_id, id)` with case ID | AUTH-P context |
| `workspace_id` | Owning workspace | `UUID NOT NULL` | None specified | `REFERENCES workspaces(id)`; workspace-tenancy membership additionally enforced | Case workspace context |
| `status` | Case state | `TEXT NOT NULL`; length unspecified | DDL gives none; creation begins `NEW` | Check allowed case codes below | SCR-002-F07 |
| `revision` | Current revision | `BIGINT NOT NULL` | `1` | Monotonic domain revision; DDL has no positive-range check | SCR-002-F09; API-004 `If-Match` |
| `sensitivity` | Case classification | `TEXT NOT NULL`; length unspecified | `'INTERNAL'` | Four information-class codes; DDL has no sensitivity check | SCR-002-F06 |
| `created_at` | Creation time | `TIMESTAMPTZ NOT NULL`; precision unspecified | `now()` | UTC durable representation | API-003 projection unresolved |
| `updated_at` | Update time | `TIMESTAMPTZ NOT NULL`; precision unspecified | `now()` | Update mechanism/trigger not specified | API-004 projection unresolved |

**Needs confirmation:** Full production DDL, including omitted domain fields and `updated_at` update behavior. Do not interpret the partial DDL as permission to discard title, owner or approved-output data.

### Canonical Selected Fields Outside Case DDL

Each exact field below is **Confirmed by Source, p. 85, §B.1**. Types shown describe logical meaning only; physical definitions inherit the unresolved conventions above.

| Entity | Exact fields and meanings | Logical types / constraints |
|---|---|---|
| DAT-001 `tenants` | `id`: identity; `slug`: tenant business label; `plan`: plan; `region`: placement; `created_at`: creation time | Identity, text/catalog values, timestamp. Explicit `unique(slug)`; slug case sensitivity/normalization Needs confirmation |
| DAT-002 `workspaces` | `id`: identity; `tenant_id`: tenant; `policy_version`: applied policy reference; `quota`: resource allowance | Identities/version/budget representation unresolved; RLS tenant scope |
| DAT-004 `case_revisions` | `case_id`: case reference; `revision`: change version; `patch`: recorded change; `actor`: change actor; `at`: change time | Logical case reference, version, structured change, principal reference, UTC time; append-only |
| DAT-005 `documents` | `id`: identity; `workspace_id`: workspace; `source_id`: stable provider source identity; `sensitivity`: classification | Source ACL enforced; `source_id` is not automatically UUIDv7 |
| DAT-006 `document_versions` | `document_id`: parent document; `hash`: content fingerprint; `parser_version`: parser lineage; `object_key`: stored artifact reference | Immutable; exact version identity column is omitted from selected catalog and Needs confirmation |
| DAT-007 `chunks` | `id`: chunk identity; `document_version_id`: immutable version reference; `page`: source page; `bbox`: source bounding box; `text_hash`: text fingerprint | Source anchor required; bounding box optional semantically; page basis, coordinates and units unresolved |
| DAT-008 `runs` | `id`: run identity; `case_id`: case reference; `status`: state; `plan_revision`: executed plan version; `budget`: runtime/token/tool budget | Bounded state machine; persist plan revision before side effects |
| DAT-009 `run_steps` | `id`: step identity; `run_id`: run reference; `step_kind`: step category; `status`: step state; `checkpoint`: durable progress | Idempotent step; step codes and checkpoint shape unresolved |
| DAT-010 `evidence_sets` | `id`: set identity; `run_id`: run reference; `chunk_refs`: selected chunks; `acl_digest`: access-scope evidence | Collection/reference representation unresolved; publish validation required |
| DAT-011 `approval_tasks` | `id`: task identity; `run_id`: run reference; `reviewer_pool`: routing pool; `artifact_hash`: exact reviewed content binding | No self approval; immutable artifact binding |
| DAT-012 `approval_decisions` | `id`: decision identity; `task_id`: task reference; `reviewer_id`: authenticated reviewer; `decision`: action; `reason`: justification | Immutable; decision request literals and reason/rationale mapping unresolved |
| DAT-013 `audit_events` | `id`: event identity; `tenant_id`: scope; `actor_id`: actor; `action`: event action; `digest`: integrity evidence | Append-only; batch hash chain and independently retained export |
| DAT-014 `outbox_events` | `event_id`: event identity; `tenant_id`: scope; `aggregate_revision`: ordering/version guard; `payload`: versioned event data | Transactional outbox; full envelope required below |
| DAT-015 `connector_cursors` | `connector_id`: connector reference; `cursor`: provider checkpoint; `watermark`: progress high-watermark; `retry_state`: retry context | Durable checkpoints; advance only after preceding durable outcomes |
| DAT-016 `token_ledger` | `run_id`: run reference; `deployment_id`: selected deployment; `in_tokens`: input usage; `out_tokens`: output usage | Token counts logically numeric; bounds, corrections and precision unresolved; attributed cost |
| DAT-017 `policy_evaluations` | `run_id`: run reference; `rule_version`: evaluated rules; `input_digest`: normalized-input fingerprint; `result`: deterministic outcome | Reproducible; input values must also be stored, not only the digest |
| DAT-018 `deletion_receipts` | `tenant_id`: scope; `object_ref`: deletion inventory object; `purge_time`: purge time; `actor`: purge actor | Auditable purge; hold exceptions and completion receipts required |

### Required Domain Fields Omitted From Selected DDL

These are **Confirmed semantic data requirements**. Physical names and placement **Need confirmation**; field names below preserve earlier screen terminology without inventing SQL columns.

| Entity / field group | Meaning and required conditions | Type / default / validation gaps | Earlier mapping and evidence |
|---|---|---|---|
| DAT-003 title, description, impact, urgency, priority, owner | Store case context; priority derives from explicit impact/urgency, not model output alone | Text/reference/catalog representation, required input set, derivation matrix and assignment rules unresolved | SCR-002-F01–F05, F08; API-001–004; Source, pp. 24–25 |
| DAT-003 classification labels, confidences, provenance, correction reason code | Asynchronous classification; corrections require reason code | Vocabulary, confidence precision and history schema unresolved | SCR-002-F11–F13; API-051; Source, p. 12 |
| DAT-003 deadline; workspace timezone/business calendar | Contractual deadline calculated using business calendar; advisory prediction cannot modify it | Calendar/timezone catalog and calculation rules unresolved | SCR-002-F17, SCR-007-F07; Source, p. 25 |
| DAT-002 retention class, allowed models, connector credential references, approved toolsets, reviewer routing | Version-preconditioned audited workspace configuration | Collection/schema/defaults unresolved; specific approved deployments and version-pinned tools | SCR-007-F01–F06; API-050; Source, pp. 24, 37, 41, 45 |
| DAT-020 case/document-version references | Attachment joins case to immutable document version | Association key, reuse cardinality and payload metadata unresolved | API-006; Source, pp. 24, 51 |
| DAT-021 capabilities, credentials reference, provider cursor, high-watermark, error ledger | Capabilities include `list`, `fetch`, delta cursor, ACL, delete; unsupported capabilities recorded as lower trust | Provider schema and health/trust enums unresolved; resolved secrets stay in vault | SCR-006-F02–F06; Source, pp. 27–29 |
| DAT-022 status, scan outcome, quality flags, OCR provenance, quarantine reason/correlation/remediation | Scan before parsing; low quality excludes autonomous use but not authorized viewing | Quality precision/thresholds, OCR opt-in representation and safe reason codes unresolved | SCR-002-F15–F16, SCR-003-F08–F09; API-007; Source, pp. 30–32 |
| DAT-007 source URI, file hash, page number, optional bounding box | Every cited chunk has resolvable stored source anchor and current permission | URI exposure, hash encoding and mapping to `page`/`bbox` unresolved | SCR-003-F04–F06; Source, p. 31 |
| DAT-024 candidate artifact, model/prompt version, injection indicators | Preserve exact reviewable candidate and generation provenance; output is not authority | Artifact schema, storage role and digest algorithm/canonicalization unresolved | SCR-002-F18, SCR-005-F03, F05; Source, pp. 38–39, 58 |
| DAT-017 normalized policy inputs and policy reasons | Store sensitivity, requested action, evidence quality, model class, financial impact category, confidence bands and rule-set version | Input code systems, normalization and reason schema unresolved | SCR-005-F06; Source, pp. 44, 58 |
| DAT-011 assignment, task state, SLA/expiry, minimum role, separation of duties | Route eligible reviewers; expiry records reassignment/escalation, never approval | Exact assignment history and expiry timestamps unresolved | SCR-005-F01–F02, F12; Source, p. 45 |
| DAT-012 decision actor/time, evaluated hash, rationale, optional annotations | Immutable decision includes exact artifact binding; stale decisions audited and rejected | Physical columns and mandatory input rationale rule unresolved | SCR-005-F07–F11; Source, p. 45 |
| DAT-026 current approved result/final response pointer, satisfied gate, closure snapshot | Pointer and gate commit atomically; closure retains approved artifact, cited versions and reviewer decisions | Pointer target, snapshot manifest and gate schema unresolved | SCR-002-F10; API-005, API-R-006; Source, pp. 26, 45–46 |
| DAT-027 actor/request fingerprint/outcome, event ID/operation key, aggregate revision | Case idempotency outcome lasts 24 hours; consumer dedup prevents repeated mutations | Namespace, key type, canonicalization and ledger retention unresolved | SF-015; API-R-007–008; Source, pp. 17, 25, 48, 54 |
| DAT-030 cost center, deployment version, budget, forecast, rejected excess requests | Attributed model/embedding/storage/index usage and daily rollups | Currency, units, precision, daily timezone and aggregation formulas unresolved | SCR-010-F01–F03; Source, p. 65 |
| DAT-033 expected citation sets/outcomes, dataset version/manifest, scores | Frozen 1,200-case synthetic permission-controlled corpus; signed manifest protects fixtures | File schema, confidence calculation and domain codes unresolved | SCR-010-F04–F06; Source, pp. 75, 88–89 |
| DAT-034 package inventory, checksums, reconciliation receipts | Export required approved content; historical backfill keeps stable source IDs and per-batch receipts | Archive format, filenames, checksum encoding and consistency point unresolved | API-025; Source, pp. 78–80 |

### Search, Object and Cache Data

**DAT-R-003 — Confirmed:**

| Data representation | Required content / validation | Unresolved physical definition | Evidence |
|---|---|---|---|
| SearchChunk row | `tenant_id`, `workspace_id`, `document_version_id`, `chunk_id`, `language`, `classification`; 1536-dimensional embedding; text with normalized keyword analyzers | Embedding/text physical field names, element precision, language codes, analyzer configuration and indexes | Source, p. 34, §9.1.1 |
| Evidence item | Chunk ID, source title, document revision, page anchor, ACL digest; opaque citation identity verified before display | Public property names, digest and revision formats, collection order | Source, p. 35, §9.3.1 |
| DocumentBlob key | Tenant, workspace, document, version and object role | Exact key delimiter, role catalog and filename scheme; public names must remain opaque | Source, p. 52, §14.3.1 |
| CacheEntry key | Tenant, user-scope digest, source ACL revision, query hash, index generation | Exact key serialization, TTL, invalidation race protocol and cache product | Source, p. 53, §14.3.2 |
| EventCursor | Monotonically increasing SSE offset; resume through `Last-Event-ID` | Per-run/global offset scope, storage type, retention and expiry | Source, p. 55, §15.2.1 |

Embedding dimension **1536** is confirmed by Chapter 9, not merely inferred from Appendix F. Changing dimensions requires versioned compatibility/rebuild handling; exact migration design **Needs confirmation**.

### Code Systems and States

| Code system | Confirmed literal values | Required guard / unresolved mapping | Evidence |
|---|---|---|---|
| Information classification | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` | Maximum class of included material governs route, redaction, retention and approval; propagation schema unresolved | Source, p. 62 |
| Case `status` | `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED` | Role, revision and approval requirements | Source, pp. 25, 82, 86 |
| Run `status` | `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED` | Checkpoint and runtime budget | Source, pp. 49, 82 |
| Document processing status | `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED` | Virus scan and quality gate; physical status location unresolved | Source, p. 82 |
| Review task state | `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED` | Actor, exact hash and separation of duties | Source, p. 82 |
| Policy `result` | `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY` | Deterministic policy; LLM cannot override | Source, p. 44 |
| Artifact display status | `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` | Separate from case/run/review enums; persisted-versus-derived mapping unresolved | Source, p. 57 |
| Baseline roles | Analyst, Reviewer, Admin, Auditor, Service | Owner and Member meanings remain unresolved; do not add them as confirmed role enum entries | Source, pp. 22, 83 |

Appendix F values `HIGH_RISK`, `auto_publish_classification: INTERNAL` and `self_approval_allowed: false` retain their configuration-example status. `HIGH_RISK` is not an additional information-class code.

### Event Envelope and Integration Fields

**DAT-R-004 — Confirmed:** Internal events contain these exact required fields and use canonical JSON/UTC. This does not establish a public SSE or webhook projection.

| Exact field | Meaning / logical type | Physical and format gap |
|---|---|---|
| `event_id` | UUIDv7 event identity | PK/uniqueness enforcement and encoding |
| `type` | Event category | Literal event catalog exists; physical/wire type and version compatibility |
| `schema_version` | Payload/envelope version | Type and version syntax |
| `tenant_id` | Immutable tenant scope | Signed-envelope binding implementation |
| `aggregate_id` | Changed aggregate identity | Aggregate-class mapping |
| `aggregate_revision` | Revision guard | Numeric wire/physical type |
| `occurred_at` | UTC occurrence timestamp | Precision |
| `trace_id` | Correlated trace | Length and syntax |
| `payload` | Event-specific versioned data | Full schemas |

**Evidence:** Source, pp. 22, 48, 87; API-R-003.

Preserve the event names and semantic payload keys in `02_api.md`, API-R-003, including `CaseCreated`, `DocumentNormalized`, `SearchIndexCommitted`, `AgentPlanApproved`, `ApprovalDecisionRecorded`, `WorkflowStageAdvanced`, `AccessDenied` and `TenantDeletionVerified`. Chapter-register events are not automatically emitted by ordinary reads. Their exact persisted payloads **Need confirmation**.

For API-045, preserve `knowledge.search@v1` input `{query: string, case_id: uuid, max_items: int<=10}` and output `{evidence_set_id: uuid, citations: Citation[]}`. Requiredness, lower bound, string lengths and complete `Citation` schema **Need confirmation**. For API-046, preserve `task_id`, `tenant_id`, `capability`, `input_schema`, `deadline_at`, `trace_id`, `authorization_ref`, `payload`; the declared output-schema field is missing and **Needs confirmation**. Source example placeholders are not production identity formats.  
**Evidence:** Source, pp. 41, 87; API-045–046.

## Lifecycle and Consistency

### Creation, Reading, Update and Deletion Matrix

The API identifiers below refer to contracts in [02_api.md](02_api.md), not newly declared endpoints.

| Data | Create | Read | Update / append | Delete / retain |
|---|---|---|---|---|
| DAT-001–002, DAT-019 | Idempotent provisioning API-056; endpoint unresolved | API-027; settings read unresolved | API-028 membership; API-050 versioned policy | API-026 inventory-based retirement; holds apply |
| DAT-003–004 | SCR-001-E04 / API-001 | SCR-001–002 / API-002–003 | SCR-002-E02 / API-004; append revisions; API-051 label correction | API-005 closure; eligible retention/API-026, API-040 |
| DAT-005–007, DAT-020–023 | SCR-002-E04 / API-006; connector API-048 | API-007, API-013–015, API-039, API-054 | New immutable versions/derivatives; ACL updates and index reconciliation | Source deletion tombstones; eligible blob/index purge |
| DAT-008–010, DAT-024–025 | SCR-002-E05 / API-008–009; API-036 generation | SCR-004 / API-010–012, API-037 | Durable stages/checkpoints; new revisions for rework | Retention duration and independently eligible run cleanup Needs confirmation |
| DAT-011–012, DAT-017, DAT-026 | Policy evaluation creates review/gate requirements | SCR-005 / API-016 and authorized evidence | API-017 immutable decisions; expiry/reassignment; atomic publication pointer | Historical decisions not edited; retention/hold policy applies |
| DAT-013–014, DAT-027–028 | Accepted transition appends outbox/audit and dedup evidence | SCR-008/API-021; scoped stream API-012 | Delivery/replay operational progress; API-038 controlled replay | Distinct retention classes; cache invalidation; ledger TTLs unresolved |
| DAT-015, DAT-021 | SCR-006/API-018 | API-019 | Checkpoint after durable preceding outcomes; exception ledger | Credential revoke through API-055; record-retention duration unresolved |
| DAT-016, DAT-030–033 | Invocation usage, daily rollups, release/evaluation operations | SCR-010/API-022–024; internal API-041–044 | Versioned evaluation/configuration evidence | Diagnostics/audit separated; other retention durations unresolved |
| DAT-018, DAT-029, DAT-034 | API-029 holds; API-025–026 export/delete | Receipts/status retrieval contract unresolved | Append completion/hold-exception receipts | Held objects remain protected; export-package expiry unresolved |

**Evidence:** Source, pp. 12, 24–32, 40–55, 62–66, 71–80, 83.

### Referential Integrity and Isolation

**DAT-R-005 — Confirmed:**

1. Resolve every tenant-owned read/write using authenticated tenant context and RLS.
2. Ensure case workspace belongs to the same tenant; an ordinary FK to `workspaces(id)` alone is insufficient.
3. Reset `app.tenant_id` and other scoped connection-pool variables after every transaction.
4. Attachments refer to immutable document versions; approvals refer to exact run artifact hashes.
5. Soft-deleted entities cannot be retrieved, including through stale derivative indexes or caches.
6. Foreign-tenant identity substitution produces the same not-found class as absent identity; safe audit evidence records principal and denied resource class without private existence disclosure.
7. Current source authorization is checked before evidence release and again at publication.

**Evidence:** Source, pp. 21–23, 28, 31, 46, 51, 86; API-R-010–012.

**Needs confirmation:** Composite FK versus controlled write-procedure enforcement, all non-case FKs, orphan handling, delete/cascade actions, shared-document retention and reference integrity after lawful purge.

### State Transitions

**DAT-R-006 — Confirmed:**

- Cases: `NEW → TRIAGED → IN_PROGRESS`; `IN_PROGRESS → PENDING_APPROVAL` or `RESOLVED`; `PENDING_APPROVAL → RESOLVED` or `IN_PROGRESS`.
- `CLOSED` is final unless explicitly reopened as a new revision.
- Runs follow `REQUESTED → RETRIEVING → GENERATING → POLICY_CHECK → AWAITING_REVIEW → PUBLISHED`, or terminal failure, with durable checkpoint before downstream dispatch.
- Quarantined unsafe documents never enter indexing.
- Expired review tasks cause recorded reassignment/escalation, never implicit approval.
- Denied drafts can be reworked as new run revisions; historical denial cannot become retroactive approval.

**Evidence:** Source, pp. 25, 30, 45–46, 49, 82.

**Needs confirmation beside these transitions:** Transition into `CLOSED`; reopen target and history mechanics; policy auto-allow run path; full document/review transition matrices; distinction between valid `AWAITING_REVIEW` and missing-approval termination; recoverable timeout representation. Preserve OQ-SF-005–006 and OQ-API-004–005.

### Transaction, Concurrency and Replay Procedures

**DAT-R-007 — Confirmed accepted mutation procedure:**

1. Validate input before transaction entry.
2. Establish tenant/actor/time/correlation context.
3. Reevaluate resource authorization and domain invariants within the transaction.
4. Check case `If-Match` revision or applicable configuration precondition.
5. Resolve idempotent outcome and request fingerprint.
6. Commit required case mutation, approval decision and outbox inserts in the ACID boundary specified by the source.
7. Dispatch asynchronous indexing/webhooks through committed outbox or reconciled saga.
8. On stale/unauthorized failure, leave business state unchanged and publish no accepted-transition event.
9. Consumers deduplicate event IDs/operation keys and detect stale aggregate revisions; cross-partition ordering is not an invariant.

**Evidence:** Source, pp. 17, 25, 48–52, 56.

**Needs confirmation:** Exact transaction aggregate boundaries across services, isolation level, lock strategy, idempotency lookup versus revision-check order, in-flight duplicate handling and failure-outcome retention. These choices must preserve API-R-005–009 without assuming a new distributed transaction.

**DAT-R-008 — Confirmed publication procedure:**

1. Load the exact current artifact, policy evaluation, evidence set and applicable review decisions.
2. Verify eligible actor/assignment and separation of duties.
3. Verify decision hash matches exact reviewed content.
4. Recompute current evidence authorization.
5. Atomically record satisfied publication gate and update final response pointer.
6. Reject replay attempting to publish different content under an old approval.

**Evidence:** Source, pp. 44–46; API-R-006.

Artifact bytes, hash serialization, canonicalization, algorithm and decision-repeat semantics **Need confirmation**. Generic register references to SHA-256 do not independently settle candidate-artifact hashing.

### History, Derivatives, Reconciliation and Migration

| ID | Confirmed requirement | Evidence / open detail |
|---|---|---|
| DAT-R-009 | Closure immutably snapshots approved answer, cited document versions and reviewer decisions | Source, p. 26; snapshot key/schema and retention linkage unresolved |
| DAT-R-010 | Content fingerprint plus pipeline version produces immutable derivative IDs; reprocessing occurs side by side without rewriting claims | Source, p. 31; relationship to UUIDv7 identity and `parser_version` unresolved |
| DAT-R-011 | Failed indexing does not roll back accepted source metadata; reconciliation compares fingerprints and repairs outbox links | Source, p. 49; reconciliation schema/schedule unresolved |
| DAT-R-012 | Rebuild creates parallel index and atomically switches read alias only after completeness/recall checks | Source, p. 34; check thresholds and old-index retirement unresolved |
| DAT-R-013 | Cursor advances only after preceding items have durable outcomes; quarantine exceptions are retained while remaining batch may proceed | Source, pp. 28–29; cursor/error-record schema unresolved |
| DAT-R-014 | Schema rollout expands with nullable columns, bounded backfill, then constraint enforcement; no field removal while active readers depend on it | Source, pp. 52, 72; batch sizes and migration plan unresolved |
| DAT-R-015 | Release binds image digest, schemas, prompts and model routing policy; rollback reverses traffic/binary, not automatic database down-migration | Source, pp. 20, 72–73; compatibility evidence schema unresolved |

### Retention, Deletion and Recovery

| Data category | Confirmed retention / lifecycle | Needs confirmation | Evidence |
|---|---|---|---|
| Case-related user data | Retention jobs operate only on eligible closed cases; legal holds preserved | Corporate classes/durations, eligibility calculation, independent document/run retention | Source, pp. 26, 90 |
| Case idempotency outcome | Actor/request fingerprint maps to one outcome for 24 hours | Expiry boundary, failed/in-flight outcomes and post-expiry behavior | Source, p. 25 |
| Diagnostics | Default TTL 30 days | Exact data coverage, expiration clock and hold interaction | Source, p. 66 |
| Security audit | Distinct seven-year policy; append-only, batch-hash chaining, independently controlled retention export | Archive format, chain verification, exact policy clock and legal exceptions | Source, pp. 62, 66 |
| Cache | Short-lived versioned ephemeral results; ACL changes invalidate before TTL and next retrieval | Numeric TTL and race-proof invalidation contract | Source, pp. 16, 28, 53 |
| Outbox, consumer ledger, dead letters, SSE events | Durable recovery/retained backfill supported | Retention periods; Appendix F `replay_dedup_hours: 24` is not a universal confirmed ledger TTL | Source, pp. 48–55, 90 |
| Export package | Required content with checksums; excludes secrets/internal prompts; two independent checks | Package expiry, snapshot consistency, download and hold redaction | Source, pp. 78–80 |
| Purge inventory / receipts | Tombstones, blob/index removal, completion receipts and held-record exceptions | Schedule, complete-versus-partial outcome, inventory/receipt schema and backup deletion | Source, pp. 51, 66, 80 |
| Backups / recovery | Continuous PostgreSQL backups; reference RPO `<=15 minutes`, RTO `<=4 hours`; object versions/rebuild recipes tested together; primary writes and warm recovery region | Backup retention, provider/region and restore consistency procedures | Source, pp. 19, 69 |

**DAT-R-016 — Confirmed deletion procedure:**

1. Establish authorized inventory scope and two independent export/delete approval checks.
2. Evaluate retention eligibility and legal holds.
3. Preserve protected objects and record hold exceptions.
4. Write tombstones and prevent normal retrieval.
5. Remove eligible blobs and index entries.
6. Record auditable completion receipts.
7. Use the same inventory for data subject access requests.

**Evidence:** Source, pp. 78–80, 89, `TST-013`. Exact hold authorization/capture/release and inventory identifiers **Need confirmation**; API-029 does not define them fully.

### Personal Data and Secret Handling

**DAT-R-017 — Confirmed:**

- Extraction tags likely personal data.
- Before provider invocation, the gateway redacts nonessential fields where policy permits.
- Maximum classification of included material controls route, redaction, retention and approval.
- Logs capture identifiers, policy outcomes, token counts and digests, not full document content or full prompts by default.
- Diagnostic traces never contain user documents/API secrets.
- Connector credentials and encryption keys remain in vault-backed secret references; rotation does not require bulk re-encryption in the request path.
- Public responses never expose resolved credentials.
- Development forbids production data; staging uses synthetic data and test connectors.

**Evidence:** Source, pp. 19, 27, 54, 62–64, 71.

**Needs confirmation:** PII tag vocabulary/schema, detection/redaction rules, auditor projection matrix, data subject matching and verification, encryption algorithm and per-tenant key isolation versus rotation throughput. Deferred multilingual OCR beyond English must not be enabled inadvertently.  
**Evidence:** Source, pp. 10, 62, 80, 90.

## Integration Data and Acceptance Criteria

### Input and Output Formats

| ID | Direction / integration | Confirmed format and validation | Needs confirmation | Evidence |
|---|---|---|---|---|
| DAT-I-001 | Browser/connector file input | PDF, DOCX, HTML, UTF-8 text; MIME signature/extension agree; configurable 25 MB per-file cap; decompression threshold; scan before parsing; macros disabled; remote references not fetched | MIME literals, MB byte basis, threshold, attachment count/aggregate cap, transfer encoding and malformed UTF-8 handling | Source, p. 30; API-006 |
| DAT-I-002 | Extraction output | Immutable text/layout/metadata; page blocks/bounding boxes; table row/column annotations; heading/reading-order segmentation; opt-in provenance-marked OCR | File/container formats, normalized-text encoding, newline/Unicode normalization, coordinates and pipeline manifest | Source, pp. 31–32 |
| DAT-I-003 | Connector provider metadata | Stable source identity, ACL, change history; advertised capability support; cursor/watermark/error ledger | Provider-specific ID/date/ACL encoding and external file naming | Source, pp. 27–29; API-048 |
| DAT-I-004 | REST and internal RPC | Controlled OpenAPI / protobuf IDL; public RFC 3339 time; validations at boundary/domain/tool dispatch | Complete field schemas, JSON charset policy, protobuf definitions and null/unknown-field semantics | Source, pp. 54–56 |
| DAT-I-005 | Internal events | Canonical JSON and UTC; exact DAT-R-004 envelope; signed immutable tenant job context | Canonical JSON algorithm, byte encoding, signing and payload schemas | Source, pp. 22, 48 |
| DAT-I-006 | Model input/output | Fixed rules, signed workflow instructions, validated user input, delimited untrusted evidence; versioned JSON output; unknown fields/invalid citations/control-character injection invalid | Output schema, artifact encoding, retry count, prompt retention and signing format | Source, pp. 38–39 |
| DAT-I-007 | MCP/A2A | Preserve API-045–046 exact fields/types and `max_items <=10`; schema-pinned capability/task data | Full citation/output-schema definition, envelope encoding and identity placeholders | Source, pp. 41, 87 |
| DAT-I-008 | SSE / optional webhook | Increasing retained offsets and scoped resume; webhook signed and event age verified | SSE payload/retention; webhook format/signature/age/recipient contract | Source, p. 55 |
| DAT-I-009 | Export output | Case metadata, approved artifacts, source references, audit manifests and checksums; excludes secrets/internal prompts | Archive/content filenames, schema, encoding, checksum algorithm and snapshot point | Source, p. 79 |
| DAT-I-010 | Evaluation/test files | Frozen versioned synthetic permission-controlled corpus with expected citation sets/outcomes; signed manifest and outputs referenced by release digest | File schema, signature algorithm, manifest fields and score precision | Source, pp. 75, 88–89 |
| DAT-I-011 | Deployment configuration | Nonsecret defaults in source control; signed environment values; secret references only | Final configuration schema and catalogs; YAML on p. 90 remains example configuration | Source, pp. 71, 90 |

### Dates, Time Zones and Numeric Representation

**DAT-R-018 — Confirmed:** Server/event durable time is UTC; public API timestamps use RFC 3339; UI displays workspace-local time with timezone labels. Locale changes never change durable representation or event ordering. Business calendar deadlines use workspace timezone.  
**Evidence:** Source, pp. 25, 48, 54, 59.

**Needs confirmation:** Timezone catalog/default, daylight-saving ambiguity rules, timestamp precision, database session timezone, daily rollup timezone, numeric decimal/currency precision and range handling. UUIDv7 locality does not replace explicit aggregate revision or event offset ordering.

Source capacity estimates—100,000 indexed documents per tenant in the reference envelope and approximately 40–120 chunks from a typical 1 MB source—are sizing assumptions, not new chunk-count validation limits.  
**Evidence:** Source, p. 68.

### Acceptance Criteria

Use synthetic successful, empty, mixed-permission, adversarial and malformed fixtures. Record randomized seeds. Critical isolation/approval tests must pass with zero exceptions.  
**Evidence:** Source, pp. 74, 89.

| ID | Preconditions and action | Expected data result | Traceability |
|---|---|---|---|
| AC-DAT-001 | Create case twice with same actor/key/body | One `NEW` case, identical outcome, no second accepted transition | DAT-003, DAT-027; API-001; Source, pp. 25, 89, `TST-001` |
| AC-DAT-002 | Reuse creation key with changed fingerprint | `409 IDEMPOTENCY_CONFLICT`; no second case | DAT-027; Source, pp. 54, 89, `TST-002` |
| AC-DAT-003 | Foreign tenant reads valid case ID; reuse pooled connection across tenants | No foreign data; not-found-equivalent disclosure; scoped variables reset | DAT-R-005; API-R-010; Source, pp. 23, 86, 89, `TST-003` |
| AC-DAT-004 | Attempt case write with workspace belonging to another tenant | Workspace-tenancy violation rejected; business state unchanged | DAT-003; Source, p. 86 |
| AC-DAT-005 | Submit stale case revision | `409 CASE_VERSION_CONFLICT`, safe current revision; no accepted mutation/outbox event | DAT-R-007; Source, pp. 25, 84 |
| AC-DAT-006 | Fail transaction during business/outbox commit | No required business mutation without its atomic outbox record; no ambiguous success | DAT-014; API-R-005; Source, p. 52 |
| AC-DAT-007 | Replay event 100 times and deliver delayed revision | Exactly one accepted business transition; dedup/revision guard prevents replay mutation | DAT-027; Source, pp. 48, 88–89, `T-07`, `TST-007` |
| AC-DAT-008 | Reprocess same source using changed pipeline version | Original derivative lineage unchanged; new derivatives can coexist with resolvable source anchors | DAT-006–007; Source, p. 31 |
| AC-DAT-009 | Upload unsafe PDF/polyglot/zipped content | Quarantine; no indexing; no macros/remote fetch; safe quarantine evidence | DAT-022; Source, pp. 30, 88–89, `T-04`, `TST-015` |
| AC-DAT-010 | Authorized low-quality document | Authorized viewing remains possible; autonomous recommendation selection excludes it | DAT-022; Source, p. 32 |
| AC-DAT-011 | Revoke source ACL after index/cache population | Next query releases no forbidden evidence; publication rejects stale access | DAT-010, DAT-028; Source, pp. 28, 46, 89, `TST-004` |
| AC-DAT-012 | Model returns unknown fields or invalid citation | `MODEL_OUTPUT_INVALID`; no published pointer/gate advancement | DAT-024; Source, pp. 38, 89, `TST-005` |
| AC-DAT-013 | Review old/wrong artifact hash, then replay decision | Stale rejection audited; old approval never publishes changed artifact | DAT-011–012, DAT-026; Source, pp. 45–46, 89, `TST-006` |
| AC-DAT-014 | Analyst attempts self approval; task expires | Self approval denied; expiry records escalation/reassignment, no implicit approval | DAT-011–012; Source, pp. 11, 45, 85, 89, `TST-010` |
| AC-DAT-015 | Close eligible case; later rework/new revision | Approved answer/cited versions/reviewer decisions in closure remain immutable | DAT-026; Source, pp. 25–26 |
| AC-DAT-016 | Index write fails after source acceptance | Source remains durable; fingerprint reconciliation can repair index/outbox linkage | DAT-R-011; Source, p. 49 |
| AC-DAT-017 | Partial sync batch includes malformed record | Cursor does not skip undurable preceding outcomes; quarantine exception durable; safe retry | DAT-015, DAT-021; Source, pp. 28–29 |
| AC-DAT-018 | Purge under legal hold | Protected records retained and receipted; eligible objects tombstoned/removed; completion evidence auditable | DAT-018; Source, pp. 80, 89, `TST-013` |
| AC-DAT-019 | Single Admin requests export; then properly authorized export | Single Admin insufficient; permitted package includes required checksummed content and excludes secrets/internal prompts | DAT-034; Source, pp. 78–79, 88, `T-11` |
| AC-DAT-020 | Attempt historical audit/review modification | Edit denied; append-only chain and independent audit retention preserved | DAT-012–013; Source, pp. 62, 88, `T-09` |
| AC-DAT-021 | Inspect telemetry/provider/public/export output | No raw credentials or document content in diagnostics; policy-permitted PII minimization before provider invocation | DAT-R-017; Source, pp. 54, 62–64, 79, 88, `T-05` |
| AC-DAT-022 | Migrate while old readers active; canary rollback | Required fields remain compatible; bounded backfill/enforcement; no automatic database down-migration | DAT-R-014–015; Source, pp. 52, 72–73 |
| AC-DAT-023 | Alter frozen expected score fixtures | Dataset version/signed manifest detects unauthorized fixture change; no false release equivalence | DAT-033; Source, pp. 76, 88, `T-12` |
| AC-DAT-024 | Reference regional restore exercise | Relational/object versions consistent; index rebuild recipes tested; RPO `<=15 minutes`, RTO `<=4 hours` | DAT-031; Source, pp. 19, 69, 89, `TST-012` |
| AC-DAT-025 | Change display locale/timezone presentation | Durable UTC/RFC 3339 values and ordering unchanged; local display has timezone label | DAT-R-018; Source, p. 59 |
| AC-DAT-026 | Evaluate retention settings | Diagnostics default 30 days and security audit distinct seven years; no accidental universal 24-hour ledger rule | Retention table; Source, pp. 25, 66, 90 |

## Consistency and Open Questions

### Source Conflicts and Required Amendments

Earlier documents are not rewritten here. Earlier proposed payloads, field placement and navigation remain **Proposals**.

| ID | Affected identifiers | Evidence / conflict | Required resolution |
|---|---|---|---|
| OQ-DAT-001 | DAT-003–004; SCR-002; API-001–005 | Source pp. 13, 26 labels Case/CaseAggregate an immutable derivative, whereas p. 24 defines independently versioned mutable aggregate and p. 86 mutable `cases` | Preserve mutable current aggregate plus immutable history; confirm register terminology and exact history/snapshot design |
| OQ-DAT-002 | DAT-001; DAT-R-002 | Source p. 51 tenant-scoped business uniqueness; p. 85 explicit `unique(slug)` | Preserve explicit tenant slug uniqueness; confirm global slug normalization/case semantics and other business keys |
| OQ-DAT-003 | DAT-006, DAT-R-010; API-R-002 | Source p. 51 UUIDv7 identities versus p. 31 fingerprint/pipeline-derived immutable IDs | Define identity-versus-fingerprint roles and version identity column without replacing either invariant |
| OQ-DAT-004 | DAT-004, DAT-012, DAT-018; API-R-002, OQ-API-012 | Source p. 85 uses `actor`, `at`, `reason`, `reviewer_id`, `purge_time`; chapter context uses `actor_id`, `occurred_at`; UI uses rationale | Approve explicit mappings; do not silently rename confirmed storage fields |
| OQ-DAT-005 | DAT-002; SCR-007-E01; API-050; OQ-SF-002, OQ-API-002 | Source p. 24 associates workspace configuration with case PATCH | Define separate valid settings contract and revision schema; never save workspace policy by inferred case mutation |
| OQ-DAT-006 | DAT-008; API-008–009; OQ-SF-003, OQ-API-001 | Two run creation paths in Source pp. 15–17 versus pp. 40, 83 | Define canonical routing/shared idempotency namespace and case association |
| OQ-DAT-007 | DAT-010; API-013, API-045 | Source p. 85 evidence set has `run_id`; standalone search/tool can return evidence set without supplied run | Define standalone retrieval association and `run_id` nullability/cardinality |
| OQ-DAT-008 | DAT-011; API-017 `approvalId` | Source p. 85 has `approval_tasks.id`, but path uses approval identity | Confirm path-to-task identity mapping and assignment/history model |
| OQ-DAT-009 | DAT-R-006; OQ-SF-004–006, OQ-API-004–005 | Source omits close predecessor, mixes display/aggregate statuses, and contrasts missing-approval termination with waiting state | Define separate explicit state mappings, guards, reopen lineage and timeout coverage |
| OQ-DAT-010 | DAT-R-017, DAT-030; OQ-SF-019, OQ-API-024 | Earlier documents leave detailed retention unresolved; Source p. 66 explicitly confirms 30-day diagnostic default and seven-year security audit | Future amendments must include these distinct confirmed baseline periods while corporate user-data policy remains unresolved |
| OQ-DAT-011 | DAT-R-001, DAT-R-003; OQ-SF-021, OQ-API-027 | PostgreSQL and 1536-dimensional embedding explicitly confirmed in Source pp. 9, 34; exact provider/region still open p. 90 | Do not treat confirmed baseline database/dimension as arbitrary implementation choices; resolve provider and migration details separately |

### Unresolved Data Decisions

| ID | Affected requirements | Needs confirmation / implementation dependency | Evidence and earlier links |
|---|---|---|---|
| OQ-DAT-012 | DAT-001–018; all field tables | Complete production DDL and logical requiredness: types, lengths, precision, nullability, PK/FK/uniqueness, enum checks, ranges and defaults outside explicit case DDL | Source pp. 85–86; [02_api.md](02_api.md) OQ-API-012 |
| OQ-DAT-013 | DAT-019–036 | Physical persistence versus projections/configuration files, authoritative owner and cardinality for logical records | Source chapter registers; no full schemas |
| OQ-DAT-014 | DAT-003–004, DAT-020 | Case business-key generation, impact/urgency priority matrix, owner transfer, label history, attachment reuse and immutable revision key | Source pp. 12, 24–26, 51; OQ-SF-014 |
| OQ-DAT-015 | DAT-005–007, DAT-022–024 | Source version identity; parser/pipeline version relationship; anchor page basis/coordinates; quality thresholds; normalized encoding; artifact storage | Source pp. 30–39; OQ-API-017, OQ-API-020 |
| OQ-DAT-016 | DAT-010–012, DAT-017, DAT-026 | Artifact hash algorithm/canonicalization, normalized input storage, policy catalogs, reviewer rationale requirement, repeated decisions, gate/snapshot schema | Source pp. 44–46, 58, 85; OQ-API-021 |
| OQ-DAT-017 | DAT-R-005, DAT-R-007–008 | Tenant-safe FK/write-procedure choice, transaction/lock strategy, concurrency ordering, orphan/delete cascade and shared-source retention | Source pp. 51–52, 86; API-R-005–010 |
| OQ-DAT-018 | DAT-014, DAT-027–028 | Complete outbox/consumer/idempotency ledger, key/fingerprint rules, ledger TTLs, signed job context, SSE offset scope/retention and webhook data | Source pp. 17, 22, 25, 48–55; OQ-API-014, OQ-API-019 |
| OQ-DAT-019 | DAT-015, DAT-021 | Provider ID/ACL encoding, concurrent cursor ownership, cursor/watermark/retry-state format, trust status and secret lifecycle | Source pp. 27–29; OQ-API-022 |
| OQ-DAT-020 | DAT-018, DAT-029, DAT-034 | Corporate retention eligibility/durations, hold scope/release, export snapshot/manifest/checksums, inventory/purge receipts and backup hold/deletion | Source pp. 26, 66, 78–80, 90; OQ-API-024 |
| OQ-DAT-021 | DAT-R-017 | PII tags/redaction matrix, data subject matching/verification, auditor scope, vault/key isolation and rotation policy | Source pp. 10, 62–63, 80; OQ-SF-022, OQ-API-027 |
| OQ-DAT-022 | DAT-016, DAT-030–033 | Usage granularity, currency/units/precision, daily rollup timezone, metrics labels, dataset/score/signature schemas, release evidence linkage | Source pp. 65, 71–76, 88–89; OQ-API-023, OQ-API-025 |
| OQ-DAT-023 | DAT-R-014–015, DAT-031 | Database hosting/version, partition/index design, migration batch sizing, restoration inventory/backup retention and approved regions/providers | Source pp. 19, 52, 69, 72, 90 |
| OQ-DAT-024 | DAT-R-018; all timestamps/numerics | Time precision, DST/calendar rules, timezone catalog, numeric range/wire mapping and Unicode/character encoding policy | Source pp. 25, 54, 59; OQ-SF-023, OQ-API-012 |
| OQ-DAT-025 | DAT-036; SCR-001-F05–F08, SCR-002-F21 | Summary metric formulas, scope, refresh and derived projection versus persisted values | Source p. 7; OQ-SF-013 |

### Dependencies on Completed and Later Specifications

- [01_screen_functions.md](01_screen_functions.md): Preserve all `SCR-*`, `SF-*`, field/event and acceptance identifiers. Physical definitions here do not confirm formerly proposed screen placement or input fields.
- [02_api.md](02_api.md): Preserve `API-*`, `API-R-*` and open-question identifiers. Storage columns are not executable REST schemas. Resolve wire mappings through controlled IDL rather than copying this catalog.
- Exception handling and workflow/operational specifications are **To be defined in a later stage**: carry forward transaction failure, stale-hash handling, quarantine, replay, cursor recovery, retention scheduling, index reconciliation and recovery dependencies.
- `08_architecture_decision.md` is **To be defined in a later stage**: consolidate unresolved decisions using links to `03_data.md` and affected `DAT-*`, `DAT-R-*`, `OQ-DAT-*`, and earlier requirement IDs.

No owner, deadline or approval is supplied for these open decisions. Unresolved physical design and lifecycle choices must not be silently selected by the implementation AI.
