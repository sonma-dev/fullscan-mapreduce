# 3. Data Specification

## Data Inventory and Relationships

### Specification Basis and Status

| Item | Definition |
|---|---|
| Output file | `03_data.md` |
| Application | OrionDesk AI |
| Source document | `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Source baseline | `OD-AI-DDS-001`; release `R1.0`; design revision `1.3` |
| Source authority | Fictional reference architecture, normative for this sample application. Numeric capacity and performance values are design assumptions, not measured production results. |
| Citation convention | **S** denotes `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf`. Citations identify original PDF pages and sections. |
| Completed preceding specifications | [Screen Function Specification](01_screen_functions.md) and [API Specification](02_api.md) |
| Identifier convention | `DAT-xxx` identifies a logical data entity or related record family; `DAT-xxx-Fxx` identifies a field definition. Other `DAT-` identifiers identify data requirements, relationships, acceptance criteria, and open questions. These are specification identifiers, not newly confirmed database names. |
| Confirmed | Explicitly supported by S. Confirmation of a field or relationship does not automatically confirm its SQL type, nullability, public JSON property, or UI editability. |
| Needs confirmation | An unresolved requirement or physical contract. It is not permission to select a schema, default, code, index, retention period, or schedule. |
| Proposal | A specifically labeled design suggestion, not an approved implementation contract. Earlier API examples and UI arrangements remain Proposals. |
| Later specifications | Processing, exception-handling, and other remaining specifications are **To be defined in a later stage**. Stage 8 will consolidate unresolved decisions in `08_architecture_decision.md`; that document has not been generated. |

**DAT-SCP-001 — Confirmed:** Preserve the complete source-supported domain information, not only the selected columns in Appendix B.1 or the abbreviated `cases` DDL in Appendix B.2. Retrieval, generation, deterministic policy evaluation, and reviewer approval remain separate records.  
**Source:** S, p. 12, §2.2.2; p. 24, §6.1.2; pp. 85–86, Appendices B.1–B.2.  
**Earlier links:** `SF-CON-006`, `API-CNS-005`, `API-TXN-001`–`003`.

**DAT-SCP-002 — Confirmed:** PostgreSQL is the authoritative store for case state and mutable metadata. This is an existing source architecture choice, not a new selection by this specification. Source documents and normalized artifacts reside in encrypted private blob/object storage. Search indexes and caches are not authoritative business records.  
**Source:** S, p. 9, §1.3.1; p. 16, §3.2.2.

**DAT-SCP-003 — Needs confirmation:** Production DDL, additional physical types, database version, search provider, partition implementation, indexes, collation, and physical placement of record families not defined by the source. No additional product, extension, SQL type, or index is selected here. See **DAT-OQ-001**.

### Storage and File Inventory

| Storage ID | Data or file category | Purpose and authority | Confirmed responsible boundary | Constraints and unresolved physical design | Source |
|---|---|---|---|---|---|
| DAT-STO-001 | PostgreSQL transactional metadata | Authoritative cases, revisions, permissions, run metadata, policy/review records, and applicable outbox/ledger records | Case Service owns transactional case mutations; Policy Service issues binding approval requirements. Exact writer ownership for other tables Needs confirmation. | Tenant-scoped predicates and RLS; ACID boundaries; no public datastore. Database version, partition strategy, and additional indexes: **DAT-OQ-001**. | S, pp. 9, 16, 18, 22, 51–52 |
| DAT-STO-002 | Private encrypted blob/object storage | Source files, normalized text/layout/metadata derivatives, immutable document objects | Ingestion Service owns conversion; storage-operation ownership beyond this Needs confirmation. | Object keys include tenant, workspace, document, version, and object role. Public names are opaque; controlled short-lived signed URLs. Exact provider, key syntax, object-role vocabulary, and URL lifetime: **DAT-OQ-010**. | S, pp. 16, 30–32, 51–52 |
| DAT-STO-003 | Hybrid vector/keyword search index | Nonauthoritative searchable derivatives | Indexer produces `SearchIndexCommitted`; Retrieval Service returns cited chunks | Versioned aliases; parallel rebuild and atomic read-alias switch after checks; `1536` embedding dimensions. Provider, physical index schema, analyzers, and validation thresholds: **DAT-OQ-009**. | S, pp. 16, 34–36, 87 |
| DAT-STO-004 | Versioned ephemeral cache | Access-scoped retrieval/query results | Exact cache owner Needs confirmation; affected by Retrieval Service and index/ACL changes | Keys include tenant, user-scope digest, source ACL revision, query hash, and index generation. Short TTL; early purge on authorization changes. Numeric TTL and key encoding: **DAT-OQ-009**. | S, p. 16, §3.2.2; p. 53, §14.3.2 |
| DAT-STO-005 | Dedicated secret store / key vault | Connector refresh tokens, service credentials, encryption keys, and references | Managed-identity access; exact administrative owner Needs confirmation | Workspace-scoped connector references; secrets never become ordinary public metadata or model context. Key isolation, reference format, and rotation policy: **DAT-OQ-015**. | S, pp. 21, 27, 63, 71–72 |
| DAT-STO-006 | Event queue and transactional outbox | Durable asynchronous dispatch, reconciliation, and replay | Platform team owns messaging; named producers retained in DAT-EVT-001 | At-least-once delivery; signed immutable tenant job context; event/operation deduplication and revision checks. Queue provider, retention, schema/signature details: **DAT-OQ-012**. | S, pp. 15, 17, 22, 48–50 |
| DAT-STO-007 | Independently controlled audit retention storage | Append-only hash-chain exports and retained audit evidence | Exact storage administrator Needs confirmation | Audit entries chained with batch hashes; separate fictional seven-year audit retention policy. Archive format, hash/signature encoding, and final corporate policy: **DAT-OQ-014**. | S, p. 62, §17.3.1; p. 66, §18.3.2 |
| DAT-STO-008 | Repository-controlled contracts, configuration, evaluation fixtures, and release artifacts | Reconstructible schemas, prompts, policies, signed configuration, frozen corpora, and release evidence | Domain teams own case/policy contracts; platform team owns identity/messaging; AI platform team owns model-gateway contracts | Nonsecret defaults in source control; versioned IDL; signed test outputs and release references. Exact repositories, filenames, manifest schemas, and formats: **DAT-OQ-017**, **DAT-OQ-019**. | S, pp. 15, 55, 71–76, 88–90 |

No source filename is provided for an uploaded document, normalized derivative, export package, audit archive, evaluation manifest, or deployment configuration. Their naming contracts are **Needs confirmation**. This specification does not assign filenames.

### Canonical Relational Entity Inventory

Names below are the exact source catalog names. Except for `cases`, the source supplies selected fields and constraints, not complete executable table definitions.

Ownership means a source-confirmed component responsibility or producer, not an assigned decision owner.

| Data ID | Source entity / table | Purpose and authority | Owner or responsible boundary | Relationships | Screen and API mappings | Source |
|---|---|---|---|---|---|---|
| DAT-001 | `tenants` | Tenant identity, slug, plan, and region | Needs confirmation; provisioning establishes tenant/workspace context | Parent tenancy context for tenant-owned data | All authenticated screens; API-027, API-056, API-014–015 | S, p. 85, B.1; pp. 21–23, 78 |
| DAT-002 | `workspaces` / `Workspace` | Group users, policy, connectors, and cases; maintain versioned settings | Workspace administrative responsibility confirmed; exact write-service owner Needs confirmation | Belongs to tenant; groups cases, documents, memberships, and connectors | `SF-SHELL-F02`, `SCR-002-F02`, `SCR-007`; API-028, API-049–050, API-056 | S, p. 24, §6.1.1; p. 85, B.1 |
| DAT-003 | `cases`; related source names `Case`, `CaseAggregate`, `CaseRow` | Current independently versioned case aggregate | Case Service | Workspace/tenant; revisions, attachments, runs, approved result | `SCR-001`, `SCR-002`; API-001–003, API-016–017, API-052 | S, pp. 12, 16, 24–26, 51, 85–86 |
| DAT-004 | `case_revisions` / `CaseRevision` | Append-only history of accepted case revisions | Case Service responsibility for case mutations | References case and revision; actor/time lineage | `SCR-002-F11`, `SCR-002-A02`, `A04`, `A07–08`; API-003, API-017, API-052 | S, pp. 25–26; p. 85, B.1 |
| DAT-005 | `documents`; related `SourceDocument` | Stable source identity, workspace scope, sensitivity, and source access | Connector ingestion / Ingestion Service; exact metadata writer allocation Needs confirmation | Workspace; immutable versions; originating ACL | `SCR-002-F21`, `SCR-003`, `SCR-006`; API-004, API-009, API-018, API-021–022, API-035 | S, pp. 27–32, 51; p. 85, B.1 |
| DAT-006 | `document_versions` / `DocumentVersion` | Immutable source/processing version and object linkage | Ingestion Service | Document; chunks, blobs, attachments, cited lineage | `SCR-002-F21`, `SCR-003-F04`; API-004, API-018, API-021–022, API-035, API-057 | S, pp. 30–32, 51; p. 85, B.1 |
| DAT-007 | `chunks`; related `ChunkAnchor` | Immutable evidence anchor and text fingerprint | Ingestion produces anchors; Retrieval Service consumes them | Immutable document version; search rows and evidence references | `SCR-003-F05–09`; API-010, API-021–022, API-046 | S, pp. 31, 34–35; p. 85, B.1 |
| DAT-008 | `runs` / `AgentRun` | Durable bounded execution and plan/budget context | Orchestrator | Case; steps, evidence sets, generation attempts, policy evaluations, review tasks | `SCR-002-A06`, `SCR-004`; API-005–007, API-019, API-032–033 | S, pp. 40–42, 49; p. 85, B.1 |
| DAT-009 | `run_steps` | Idempotent execution steps and checkpoints | Orchestrator | Run; plan node/checkpoint mapping Needs confirmation | `SCR-004-F03–05`; API-019, API-033 | S, pp. 40–42, 49; p. 85, B.1 |
| DAT-010 | `evidence_sets` / `EvidenceSet` | Selected chunk references and ACL provenance used in publication validation | Retrieval Service | Run association in B.1; chunk references; candidate/publication lineage | `SCR-003`, `SCR-004-F08`, `SCR-005-F07`; API-010, API-021–022, API-046, API-020 | S, pp. 16, 35, 45; pp. 85, 87 |
| DAT-011 | `approval_tasks` / `ApprovalTask` | Policy-routed review requirement bound to an artifact | Policy Service issues requirements; exact queue writer ownership Needs confirmation | Run; candidate hash; reviewer pool; decisions | `SCR-005`; API-023–024, API-020, API-053 | S, pp. 16, 44–46; p. 85, B.1 |
| DAT-012 | `approval_decisions` / `ReviewDecision` | Immutable human decisions and rationale | Policy Service produces `ApprovalDecisionRecorded`; authenticated Reviewer acts | Task; reviewer; exact reviewed artifact | `SCR-005-F06`, `F10–13`, `SCR-008`; API-024, API-020, API-011 | S, pp. 45–46, 62; pp. 85, 87 |
| DAT-013 | `audit_events` / `AuditEntry` | Append-only decision, access, and change evidence | Exact ledger writer ownership Needs confirmation; producers retain correlated evidence | Tenant, actor, event/aggregate lineage, batch hashes | `SCR-008`; API-011; audit effects of mutations | S, pp. 23, 62; p. 85, B.1 |
| DAT-014 | `outbox_events`; related `OutboxRecord`, `OutboxTable` | Transactional event publication and reconciliation source | Platform messaging boundary; originating domain transaction writes its applicable event | Aggregate revision, event identity, consumer/replay records | Run/status views indirectly; API-033–034; effects of API mutations | S, pp. 17, 48–52; p. 85, B.1 |
| DAT-015 | `connector_cursors` / `SourceCursor` | Durable provider progress and retry checkpoint | Connector workers | Connector; sync-run progress/outcomes | `SCR-006-F05–08`; API-009, API-025 | S, pp. 28–29; p. 85, B.1 |
| DAT-016 | `token_ledger` / `TokenLedger` | Provider token usage and attributed cost | Model gateway tracks usage; exact ledger writer allocation Needs confirmation | Run; specific deployment; quota/cost attribution | `SCR-004-F06`, `SCR-010-F03–04`; API-008, API-012 | S, pp. 38, 65; p. 85, B.1 |
| DAT-017 | `policy_evaluations` / `PolicyEvaluation` | Reproducible normalized policy inputs, version, digest, and outcome | Deterministic Policy Evaluator / Policy Service | Run; rule-set version; candidate/review/publication context | `SCR-002-F18`, `SCR-004-F07`, `SCR-005-F09`, `SCR-007`; API-005, API-020, API-024, API-050 | S, pp. 40, 44–46; p. 85, B.1 |
| DAT-018 | `deletion_receipts` / related `PurgeReceipt` | Auditable purge completion and retained exceptions | Retention Worker produces verification event; precise storage mapping Needs confirmation | Tenant, object reference, actor, manifest/receipt lineage | Export/delete placement unresolved; API-015, API-036 | S, pp. 66, 79–80; pp. 85, 87 |

**DAT-INV-001 — Needs confirmation:** Related source names in the same inventory row express the same subject area, but the source does not consistently define one-to-one physical aliases. Do not create duplicate tables or merge distinct records solely because names are adjacent. See **DAT-OQ-002** and **DAT-CNS-002**.

### Additional Logical Records, Objects, and Record Families

A source-confirmed logical record does not establish a separately persisted SQL table.

| Data ID | Exact source term or explicitly identified logical data | Purpose / responsible boundary | Principal relationships and cardinality status | Screen/API mappings | Source |
|---|---|---|---|---|---|
| DAT-019 | `Principal`, `Actor` | Authenticated user/service identity; exact identity-store owner Needs confirmation | Membership, case ownership, decisions, audit actors; identity alias and multiplicity Needs confirmation | All screens; API-027, API-028 | S, pp. 11–13, 21–23 |
| DAT-020 | `TenantMembership` | Tenant/workspace membership and role bindings; exact owner Needs confirmation | Principal ↔ tenant/workspace; membership record structure and uniqueness Needs confirmation | `SF-PRE-003`, `SF-SCP-008`; API-028, API-056 | S, pp. 21–23, 78 |
| DAT-021 | `AccessPolicy` | Resource access rules; Policy Service boundary | Principal, workspace, action, classification, ACL, separation of duties; exact record relations Needs confirmation | All protected screens; API-027–028 and authorization across APIs | S, pp. 22–23 |
| DAT-022 | `ResourceAcl` | Originating source/resource permission and revision context | Source document and current principal scope; ACL entries/subjects/cardinality Needs confirmation | `SCR-003`, `SCR-006`; API-009–010, API-020–022, API-028 | S, pp. 22, 28, 53 |
| DAT-023 | `Attachment` | Separate case-to-immutable-version attachment entity | Case → attachments; each attachment references an immutable document version. Reuse across cases Needs confirmation. | `SCR-002-F20–25`, `SCR-002-A05`; API-004 | S, pp. 12, 24, 51 |
| DAT-024 | Case classification output and correction history | Labels, confidences, provenance, and correction reason code; Triage Agent/classifier | Associated case classification/corrections; precise persistence and count Needs confirmation | `SCR-002-F13–14`, `SCR-002-A03`; API-051 | S, p. 12, §2.2.1; p. 40, §11.1.1 |
| DAT-025 | `CaseStatusEvent` | Case-state change lineage | Case revision/event association; table relationship Needs confirmation | `SCR-002-A04`, `A07`; API-003, API-017 | S, pp. 25–26 |
| DAT-026 | Closure snapshot | Approved answer, cited versions, and reviewer decision snapshot | Closed case/revision → retained lineage; snapshot schema and count Needs confirmation | `SCR-002-A07–08`; API-017, API-052 | S, p. 26, §6.3.2 |
| DAT-027 | `Connector` | Repository capability and workspace-scoped credential configuration; connector workers | Workspace, secret references, sync runs, source documents; exact FKs Needs confirmation | `SCR-006`, `SCR-007-F04`; API-009, API-025, API-054–055 | S, pp. 27–29 |
| DAT-028 | `SyncRun` | Provider cursor, high-watermark, durable outcomes, error ledger | Connector → repeated sync runs; cursor/history storage allocation Needs confirmation | `SCR-006-F05–08`; API-009, API-025 | S, pp. 28–29 |
| DAT-029 | `ExtractionJob` | Scan/extraction/indexing progress, parser quality, quarantine | Document/version processing; number of attempts and status location Needs confirmation | `SCR-002-F22–25`; API-004, API-018 | S, pp. 30–32 |
| DAT-030 | `ContentBlock` | Layout-aware page blocks, tables, headings, and reading order | Version → blocks → chunk boundaries; exact block-to-chunk multiplicity Needs confirmation | `SCR-003-F05–06`, `F09`; API-004, API-021–022 | S, p. 31, §8.2.1 |
| DAT-031 | `SearchChunk` | Search row with text, embedding, tenancy, language, and classification; Indexer | References chunk and immutable document version; generation-specific row multiplicity Needs confirmation | `SCR-003`; API-010, API-021–022 | S, pp. 34–36 |
| DAT-032 | `IndexAlias` | Versioned index generation/read selection; Indexer | Parallel generations and atomic active read alias; alias cardinality/schema Needs confirmation | Evidence/degraded-mode views; API-010, API-021, API-041 | S, pp. 34–36, 79 |
| DAT-033 | `RetrievalQuery` | Validated query, ranking and token-budget context; Retrieval Service | Query to selected evidence; runless search relationship Needs confirmation | `SCR-003-F01–02`; API-010, API-046 | S, p. 35, §9.2 |
| DAT-034 | `CacheEntry` | Versioned access-scoped query result | Tenant/scope/ACL/query/index generation key; no authoritative business ownership | `SCR-003`; API-010, API-021–022 | S, pp. 16, 52–53 |
| DAT-035 | `DocumentBlob` | Encrypted immutable source/derivative object and provenance | Tenant/workspace/document/version/object-role context | `SCR-003-F08–09`; API-035, API-036, API-057 | S, pp. 51–53 |
| DAT-036 | `ModelDeployment` | Specific approved deployment registry; AI platform/model gateway | Workspace whitelist, generation, usage, evaluation; exact registry scope Needs confirmation | `SCR-004-F07`, `SCR-007-F03`; API-008, API-026 | S, pp. 37–39 |
| DAT-037 | `PromptTemplate` | Versioned template and digest/provenance; AI platform | Generation attempts, reviewer display, release record, evaluations | `SCR-005-F08`, `SCR-008-F06`; API-008, API-026, API-043–045 | S, pp. 37–39, 58, 73 |
| DAT-038 | `GenerationAttempt` | Scoped generation inputs, structured output validation, invocation lineage; model gateway | Run, deployment, template, selected evidence, usage; attempt cardinality Needs confirmation | `SCR-004`, `SCR-005`; API-008 | S, pp. 38–39 |
| DAT-039 | Candidate and approved artifacts | Exact candidate content and hash-bound approved output; Draft Agent assembles candidate | Run/revision, evidence, generation, task/decision, publication pointer; schema/count Needs confirmation | `SCR-002-F16–17`, `SCR-005-F05–06`; API-020, API-023–024 | S, pp. 7, 24, 40, 44–46, 58 |
| DAT-040 | `PlanNode` | Versioned DAG node and dependencies; Orchestrator | Run plan revision → nodes/dependencies; no cycle allowed | `SCR-004-F03–04`; API-019, API-033 | S, pp. 40–42 |
| DAT-041 | `ToolCapability` | Pinned discovery metadata and separate capability authorization | Principal/workspace/tool scope/classification; registration is not grant | Run screens indirectly; API-046–047 | S, pp. 41–42, 87 |
| DAT-042 | `A2ATaskEnvelope` | Scoped task handoff with declared schema, deadline, and trace | Task, capability, input/output schema, authorization reference; persistence Needs confirmation | `SCR-004`; API-047 | S, p. 41, §11.2.2; p. 87, C.2 |
| DAT-043 | `PublicationGate` | Satisfied evidence/policy/approval gate and atomic final pointer | Exact candidate/hash, approvals, policy, current evidence permissions | `SCR-002-A09`; API-020 | S, pp. 45–46 |
| DAT-044 | Idempotency outcome binding | Actor/request fingerprint/key → one original outcome | Operation identity; physical table, namespace, and concurrency design Needs confirmation | Mutating screens; API-IDEM-001–005 | S, pp. 25, 54 |
| DAT-045 | Consumer event ledger / duplicate outcome | Deduplication and stale revision assurance | Event ID, operation key, aggregate revision; consumer scope Needs confirmation | Progress indirectly; API-033–034 | S, pp. 17, 48–50 |
| DAT-046 | `WorkflowCheckpoint` | Durable stage state before downstream dispatch | Run/stage/checkpoint; mapping to `run_steps.checkpoint` Needs confirmation | `SCR-004`; API-033 | S, pp. 49–50 |
| DAT-047 | `DeadLetterEntry` | Failed event and bounded replay provenance | Original event, operator reason, dry-run, scope, migration link | No confirmed ordinary user screen; API-034 | S, pp. 49–50 |
| DAT-048 | `QueueEnvelope` | Versioned signed tenant job/event context | Original event and workflow dispatch; persistence Needs confirmation | Internal workflow integrations; API-EVT-001–002 | S, pp. 22, 48–50 |
| DAT-049 | `EventCursor` | Monotonically increasing SSE resume offset | Authorized run stream and retained events; not necessarily a stored per-user cursor | `SCR-004-F09`; API-007 | S, p. 55, §15.2.1 |
| DAT-050 | `WebhookSubscription` | Optional signed outbound delivery configuration | Subscription/recipient, committed event, signature and retry context; detailed schema Needs confirmation | No confirmed management screen; API-048 | S, p. 55, §15.2.2 |
| DAT-051 | `DataClassification` | Information-class metadata and run control aggregation | Material and run context; provenance/schema Needs confirmation | `SCR-002-F10`, `SCR-007-F09–11`; API-CLS-001 | S, p. 62, §17.2.1 |
| DAT-052 | `KeyReference` | Vault-backed secret/encryption references | Tenant/workspace/object/credential context; no raw key in application metadata | Settings/provisioning; API-056 | S, pp. 62–63, 71–72, 78 |
| DAT-053 | Legal/security hold data | Retention/deletion exception; separately callable hold capability exists | Protected inventory and lifecycle operation; target types/cardinality Needs confirmation | Screen placement unresolved; API-029, API-015, API-036 | S, pp. 26, 61–63, 80 |
| DAT-054 | `ThreatControl`, `TraceSpan`, `MetricSeries`, `CostLedger`, `AlertPolicy` | Security controls, privacy-safe telemetry, attributed costs, and alert rules | Threat/control/test lineage; tenant/workspace/model attribution; precise stores and owners Needs confirmation | `SCR-008`, `SCR-010`; API-011–012, API-040 | S, pp. 61–66 |
| DAT-055 | `CapacityBudget`, `AdmissionPermit`, `RecoveryCheckpoint`, `LoadProfile` | Capacity, admission, recovery, and workload records | Workspace quota, queue age, provider capacity, backup/recovery context; physical relationships Needs confirmation | Degraded/usage views; API-041–042 | S, pp. 68–70 |
| DAT-056 | `ReleaseArtifact`, `ConfigVersion`, `MigrationPlan`, `RolloutGate` | Reconstructible signed release/configuration and migration evidence | Image/schema/prompt/model-policy versions; build and test evidence | No confirmed release screen; API-043–044 | S, pp. 71–73 |
| DAT-057 | `TestCase`, `EvalDataset`, `Scorecard`, `ReleaseGateResult` | Frozen synthetic fixtures, expected outputs, actual metrics, and release decisions | Evaluation request/result, dataset version, prompt/model version, release digest | `SCR-010-F05–10`; API-013, API-045 | S, pp. 74–76, 88–89 |
| DAT-058 | `Runbook`, `ProvisioningJob` | Idempotent onboarding, bounded backfill, operational evidence | Workspace policy, key references, role bindings, quota, connector stubs, reconciliation receipts | `SCR-006-F09`; API-056; operational placement unresolved | S, pp. 78–80, 90 |
| DAT-059 | `ExportManifest` | Approved export inventory and checksums | Case metadata, approved artifacts, source references, audit manifests; operation scope unresolved | `SF-SCP-007`; API-014 | S, pp. 79–80 |
| DAT-060 | `ChangeRequest`, `DesignRevision`, `RequirementLink`, `DecisionRecord` | Controlled design changes, immutable baseline traceability, impacts, and invariant/test linkage | Baseline revision, requirement, negative test, accepted decision; physical relationships Needs confirmation | No confirmed screen; API-030–031 | S, pp. 8–10 |
| DAT-061 | `ApiOperation`, `ErrorEnvelope` | Contract/version metadata and safe error representation | Repository IDL and compatibility evidence; errors are not automatically persisted records | All API errors; API-037; API-ERR-001 | S, pp. 54–56, 84 |
| DAT-062 | `ViewState`, `ReviewForm`, `EvidencePanel`, `Notification`; illustrated summaries | Browser presentation state, exact review/evidence projection, and notification concepts | Authorized server records; persistence, channels, and summary formulas Needs confirmation | All primary screens; API-058–059 | S, pp. 7, 57–59 |
| DAT-063 | `EdgeGateway`, `CaseService`, `Orchestrator`, `RetrievalService`, `VirtualNetwork`, `APIReplicaSet`, `WorkerPool`, `RegionFailoverPlan` | Source component/register subjects, not automatically application tables | Deployment/service metadata relationships and persistence Needs confirmation | Internal/runtime interfaces, API-038–039 | S, pp. 15–20 |

**DAT-INV-002 — Confirmed:** Retain source register control assertions: UUIDv7 plus tenant scope for owner aggregates; SHA-256 source/revision provenance for entries labeled immutable derivatives; actor/role predicates for policy-bound controls; event ID and trace context for operational ledgers. Their assignment to specific production columns is not fully specified.  
**Source:** S, component registers §§1.4–22.4.

**Needs confirmation — DAT-OQ-002:** Some register labels conflict with explicitly mutable aggregates or operational status. For example, `Case` and `CaseAggregate` are labeled “Immutable derivative” in register tables, while Chapter 6 and Appendix B define mutable current case state and append-only revisions. Preserve the provenance control without treating current case rows as unmodifiable. Record-level separation and SHA-256 field mapping must be clarified.

### Logical Relationships and Referential Integrity Inventory

`1:N` below means the source supports a parent associated with multiple child records. It does not establish that children must already exist when a parent is created. Physical FK implementation and deletion actions remain separate decisions.

| Relationship ID | Parent → related data | Source-supported relationship and cardinality | Physical enforcement / unresolved details | Source |
|---|---|---|---|---|
| DAT-REL-001 | Tenant → workspace / case | Each workspace carries `tenant_id`; each case has exactly one required tenant and workspace in the DDL. Tenant supports multiple scoped resources. | Case FKs confirmed. Workspace tenant FK and production same-tenant enforcement design: **DAT-OQ-003**. | S, pp. 24, 85–86 |
| DAT-REL-002 | Workspace → cases, documents, connectors, membership | Workspace groups these resources; `cases.workspace_id` is required; `documents.workspace_id` is cataloged. | Workspace moves, membership uniqueness, and connector/document physical FKs Needs confirmation. | S, pp. 21–24, 27, 85 |
| DAT-REL-003 | Case → revisions | Repeated independently versioned case changes have append-only history. | Unique revision identity, initial revision-history entry, PK, and FK strategy: **DAT-OQ-005**. | S, pp. 24–25, 85 |
| DAT-REL-004 | Case → attachments → document version | Attachments are separate entities joined by immutable identifiers; each attachment references an immutable document version. Case supports multiple attachments. | Whether the same version can be attached to multiple cases; duplicate-attachment handling; removal/relinking rules: **DAT-OQ-007**. | S, pp. 24, 51 |
| DAT-REL-005 | Document → immutable versions → chunks | Versions reference `document_id`; chunks reference `document_version_id`; side-by-side reprocessing is supported. | Local version identity column, version uniqueness, parser/pipeline relation, FK and purge behavior: **DAT-OQ-008**. | S, pp. 31, 85 |
| DAT-REL-006 | Document version → object roles / content blocks | Source and normalized artifacts retain document/version context; layout blocks produce chunk boundaries. | Number of objects by role; block-to-chunk multiplicity; storage layout: **DAT-OQ-008**, **DAT-OQ-010**. | S, pp. 16, 31, 52 |
| DAT-REL-007 | Case → runs → steps / plan nodes | Runs are separate case-associated entities; steps reference `run_id`; plan is a bounded DAG. | Run revision versus plan revision, step operation identity, and node/step/checkpoint mapping: **DAT-OQ-011**. | S, pp. 24, 40–42, 85 |
| DAT-REL-008 | Run → evidence sets → chunk references | B.1 has `evidence_sets.run_id` and `chunk_refs`; selected evidence participates in publication validation. Multiple queries/evidence selections are supported conceptually. | Minimum/maximum set counts; join table versus structured references; public runless search association: **DAT-OQ-009**. | S, pp. 35, 45, 85, 87 |
| DAT-REL-009 | Run → generation attempts / artifacts / token records | Candidate generation and token usage retain run context; bounded validation retries may produce attempts. | Exact attempt/artifact counts, IDs, and linkage; ledger uniqueness: **DAT-OQ-011**. | S, pp. 38–40, 85 |
| DAT-REL-010 | Run → policy evaluations / approval tasks | Policy inputs/outcome and reviewer requirements are separate records; B.1 references `run_id`. | Evaluation/task counts, version activation, reassignment history, exact candidate relation: **DAT-OQ-013**. | S, pp. 12, 44–46, 85 |
| DAT-REL-011 | Approval task → decisions / reviewer / artifact hash | Decisions reference `task_id` and `reviewer_id`; approvals bind the exact run artifact hash. | Number of accepted decisions per task; quorum or secondary review representation; artifact FK/hash target: **DAT-OQ-013**. | S, pp. 45–46, 51, 85 |
| DAT-REL-012 | Case current result → artifact / publication gate / closure lineage | Final response pointer and satisfied gate update atomically. Closure snapshots approved answer, cited versions, and reviewer decisions. | Pointer column/type; nullability before publication; snapshot shape and reopen lineage: **DAT-OQ-005**, **DAT-OQ-013**. | S, pp. 24, 26, 45 |
| DAT-REL-013 | Source document → ACL / classifications / cached or indexed derivatives | Originating ACL governs text release; ACL revisions invalidate cached results. Included material classifications determine run controls. | ACL/classification record granularity and history; dependency invalidation mapping: **DAT-OQ-004**, **DAT-OQ-016**. | S, pp. 22, 28, 34, 53, 62 |
| DAT-REL-014 | Connector → sync runs / cursors / item outcomes | Every sync run stores provider cursor, high-watermark, and error ledger; cursor advances after durable preceding outcomes. | Current cursor versus per-run history; one/multiple provider cursor partitions and uniqueness: **DAT-OQ-006**. | S, pp. 28–29, 85 |
| DAT-REL-015 | Aggregate mutation → outbox → consumer ledger / checkpoint / dead letter | Applicable outbox event is committed with business state; consumers use event identity, operation key, and revision. | Event PK, consumer namespace, retention, replay lineage, and delivery state schema: **DAT-OQ-012**. | S, pp. 17, 48–52 |
| DAT-REL-016 | Tenant/object inventory → hold / export manifest / purge receipt | Export/deletion use independent approvals and inventory; holds preserve protected records; receipts identify purge evidence. | Tenant-versus-workspace extent, hold targets, shared-object handling, manifest/receipt counts: **DAT-OQ-018**. | S, pp. 78–80, 85 |
| DAT-REL-017 | Evaluation → frozen dataset / expected outputs / scorecard / release evidence | Expected citation sets and outcomes are stored per example; actual metrics and signed outputs bind evaluated versions/release digest. | Evaluation identity/state and all physical FKs/counts: **DAT-OQ-017**. | S, pp. 74–76, 88–89 |
| DAT-REL-018 | Design/release revision → requirements / negative tests / signed artifacts | Revised invariants link to at least one negative test; release record binds image, schemas, prompts, and routing policy. | Requirement-link schema, revision allocation, signatures and physical relationship cardinality: **DAT-OQ-019**. | S, pp. 8–10, 71–73, 89 |

## Data Field Definitions

### Field Contract Conventions

| Attribute | Rule |
|---|---|
| Physical name | A name such as `cases.status` is confirmed where shown in source DDL. Other qualified names retain the exact Appendix B.1 table/selected-field names but do not imply complete production DDL. “Not specified” means the source provides only a logical concept. |
| Type | Exact source types are retained. “Logical UUID” applies the source identifier policy without independently selecting a physical SQL type for a table lacking DDL. “Text,” “structured value,” “reference,” and “timestamp” describe semantics, not approved SQL declarations. |
| Length / precision | **Needs confirmation** unless explicitly provided. No undocumented string length, decimal precision, confidence range, URI length, page limit, or numeric cap is authorized. |
| Required status | “Logical required” means information must exist for the applicable accepted record or stage. It does not establish a required form input or a physical `NOT NULL` column. |
| Nullability | **Needs confirmation** unless Appendix B.2 specifies `NOT NULL` or the source explicitly makes a field optional. Stage-dependent absence is not automatically implemented as SQL `NULL`. |
| Defaults | **Needs confirmation** unless explicitly stated. Missing source defaults are not interpreted as empty string, zero, empty collection, current user, latest version, or `{}`. |
| Keys / uniqueness | Only source-confirmed constraints are mandatory. Logical references require integrity, but their SQL PK/FK, composite form, indexes, and referential actions remain unresolved where no DDL is supplied. |
| Public mapping | Stored field names do not automatically become JSON properties or editable controls. Preserve route placeholders, MCP fields, and existing screen IDs separately. |
| Generated identity/context | Tenant, actor, revision, occurrence, and correlation context are trusted information, not unrestricted user-editable inputs. |
| Unresolved physical design | Each table lacking a complete field definition inherits **DAT-OQ-001** for physical types, lengths, nullability, defaults, keys, and indexes, plus its adjacent domain-specific question. |

### Shared Identity, Mutation, Time, and Hash Fields

| Requirement / field | Meaning | Type / format | Required / nullability / default | Constraints and mapping | Source |
|---|---|---|---|---|---|
| DAT-COM-F01 — identity, usually `id` or `event_id` | Immutable technical record identity | UUIDv7 generation policy; case `id` has source SQL `UUID` | Identity required for identifiable records; exact PK/nullability for non-case records Needs confirmation | Do not derive identity from illustrated `OD-2026-...` references. Derivative fingerprint-based identity details remain unresolved. | S, p. 51, §14.1.1; p. 86, B.2 |
| DAT-COM-F02 — `tenant_id` | Immutable tenant security/partition attribute | Case SQL `UUID`; other physical declarations Needs confirmation | Mandatory for every tenant-owned row; no default tenant | Included in every access predicate and signed job context. Its omission from a selected-field list does not exclude it. | S, p. 22, §5.3.1; p. 51, §14.1.1 |
| DAT-COM-F03 — `revision` | Durable aggregate/change revision | Case SQL `BIGINT`; other revision types Needs confirmation | Required where durable changes require revision context; case default `1` | Case revision monotonic. Not identical by assumption to `plan_revision`, `aggregate_revision`, or design revision `1.3`. | S, pp. 24–25, 48, 86 |
| DAT-COM-F04 — `actor_id`; related `actor`, `reviewer_id` | Authenticated user/service responsible for action | Principal reference; exact storage/wire type Needs confirmation | Required mutation/decision context; server-derived | Identity mapping between these names Needs confirmation. No impersonation through editable fields. | S, pp. 11–13, 25, 45, 85 |
| DAT-COM-F05 — `occurred_at`; related `at`, `purge_time` | Durable occurrence time | UTC; public representation RFC 3339; case timestamps SQL `TIMESTAMPTZ` | Required mutation/event context; physical nullability/defaults not generalized from case DDL | Workspace-local display includes timezone label; locale does not change durable order. | S, pp. 48, 54, 59, 85–86 |
| DAT-COM-F06 — `trace_id`, `correlation_id` | Request/workflow correlation across boundaries | Identifier/string semantics; exact type, length, and generation Needs confirmation | Every request carries both concepts; retained in relevant evidence | Independent of provider trace identifiers. Exact placement in non-case records/events Needs confirmation. | S, p. 16, §3.3.1; p. 64, §18.1.1 |
| DAT-COM-F07 — hashes and digests | Content/provenance/ACL/policy/receipt evidence | Digest semantics; algorithm/encoding field-specific | Required where the applicable contract uses the digest; no universal default | Register SHA-256 assertions do not establish that every `artifact_hash`, `acl_digest`, or `input_digest` uses SHA-256 or a particular encoding. | S, component registers; pp. 31, 35, 45, 62, 85 |
| DAT-COM-F08 — business key | Tenant-scoped business uniqueness | Exact key fields/types Needs confirmation | No generated default established | Unique constraints scoped to tenant and business key, except the explicitly cataloged global `tenants.slug` uniqueness and case PK. | S, p. 51, §14.1.1; pp. 85–86 |

**DAT-ID-001 — Needs confirmation:** Full-range `BIGINT` JSON representation, UUID lexical acceptance, derivative-ID generation, and hash canonicalization. The integer values in the conflict example do not establish safe browser transport for every `BIGINT` value. See **DAT-OQ-003**, **DAT-OQ-008**, **DAT-OQ-013**.

### DAT-001 and DAT-002 — Tenants and Workspaces

| Field ID | Source field / physical name | Meaning | Type / length / precision | Required / nullability / default | Keys, values, and related fields |
|---|---|---|---|---|---|
| DAT-001-F01 | `tenants.id` | Tenant technical identity | Logical UUID; exact SQL declaration Needs confirmation | Logical identity required; physical constraint/default Needs confirmation | FK target of `cases.tenant_id`; PK declaration not supplied |
| DAT-001-F02 | `tenants.slug` | Tenant business key | Semantic text; length/collation/pattern Needs confirmation | Nullability/default Needs confirmation | Source `unique(slug)`; global tenant-slug uniqueness, not `unique(tenant_id,slug)` |
| DAT-001-F03 | `tenants.plan` | Tenant plan classification | Code/reference; catalog Needs confirmation | Requiredness/default Needs confirmation | No plan literals or quota mapping established |
| DAT-001-F04 | `tenants.region` | Tenant region configuration | Region reference; format Needs confirmation | Requiredness/default Needs confirmation | Approved primary/recovery region selection unresolved; do not use `primary-approved-region` as a real selected cloud region |
| DAT-001-F05 | `tenants.created_at` | Tenant creation time | Timestamp; UTC semantics | Physical type/nullability/default Needs confirmation | Do not copy case `now()` default by assumption |
| DAT-002-F01 | `workspaces.id` | Workspace identity | Logical UUID | Logical identity required; physical declaration Needs confirmation | FK target of `cases.workspace_id` |
| DAT-002-F02 | `workspaces.tenant_id` | Owning tenancy | Logical tenant reference | Tenant attribute required | RLS tenant scope; workspace-tenancy consistency required |
| DAT-002-F03 | `workspaces.policy_version` | Applicable versioned workspace policy | Version reference; type/length Needs confirmation | Field confirmed; stage-requiredness/default unresolved | Mapping to `policy_evaluations.rule_version` and configuration revision Needs confirmation |
| DAT-002-F04 | `workspaces.quota` | Workspace quota configuration | Structured/numeric policy; units and schema Needs confirmation | Field confirmed; requiredness/default unresolved | Token/admission/connector quotas exist; no universal limit inferred |
| DAT-002-F05 | Retention class; physical name not specified | Workspace retention setting | Policy reference/code | Stored setting confirmed; requiredness/default unresolved | Final corporate classes/periods and maximum-material-class mapping Needs confirmation |
| DAT-002-F06 | Allowed models; physical name not specified | Whitelisted specific deployments | Deployment reference collection; layout Needs confirmation | Stored setting confirmed; empty-set/default behavior unresolved | Do not whitelist only a provider brand |
| DAT-002-F07 | Connector credential references; physical name not specified | Workspace-scoped secret-store references | Opaque reference collection | Stored setting confirmed; requiredness unresolved | No raw token or service secret in public metadata |
| DAT-002-F08 | Approved toolsets; physical name not specified | Permitted pinned tools/capabilities | Versioned references | Stored setting confirmed; default unresolved | Discovery never grants authorization |
| DAT-002-F09 | Reviewer routing; physical name not specified | Policy-defined reviewer pool/role routing | Structured policy/reference | Stored setting confirmed; default unresolved | Minimum role, separation of duties, configured SLA |
| DAT-002-F10 | Configuration revision; physical name not specified | Optimistic concurrency/version of settings | Monotonic/version semantics; type unresolved | Revision precondition required for update | Not automatically the same as `policy_version`; API-050 transport unresolved |
| DAT-002-F11 | Workspace timezone / business calendar; physical names not specified | Local calendar context for deadlines | Timezone/calendar references; catalogs unresolved | Needed by deadline calculations; persistence/default Needs confirmation | Presentation uses local timezone labels; no timezone selected |
| DAT-002-F12 | Workspace cost center; physical name not specified | Usage attribution | Reference/text; format unresolved | Attribution required where usage recorded; workspace field design unresolved | Model invocations, embeddings, storage, and indexing carry attribution |

**Sources:** S, p. 24, §6.1.1; p. 25, §6.3.1; p. 59, §16.3.2; p. 65, §18.3.1; p. 85, B.1.  
**Mappings:** `SCR-002-F02`, `SCR-007-F01–13`, `SCR-010-F03`; API-028, API-049–050, API-056.  
**Needs confirmation:** **DAT-OQ-003**, **DAT-OQ-004**, **DAT-OQ-016**, **DAT-OQ-018**.

### DAT-003 — Current Case

#### Source DDL Fields

| Field ID | Physical name | Meaning | Confirmed SQL type | Nullability / default | Confirmed key or constraint | Earlier mapping |
|---|---|---|---|---|---|---|
| DAT-003-F01 | `cases.id` | Technical case identity | `UUID` | Primary key; no DDL default | `PRIMARY KEY`; UUIDv7 generation policy | `SCR-001-F01`, `SCR-002-F01`; API-001–003 |
| DAT-003-F02 | `cases.tenant_id` | Case tenant | `UUID` | `NOT NULL`; no default | `REFERENCES tenants(id)` | Trusted context; API-AUTH-003 |
| DAT-003-F03 | `cases.workspace_id` | Case workspace | `UUID` | `NOT NULL`; no default | `REFERENCES workspaces(id)`; production same-tenant enforcement additionally required | `SCR-002-F02`; API-001, API-003 |
| DAT-003-F04 | `cases.status` | Current Case state | `TEXT` | `NOT NULL`; no DDL default. Business initial state `NEW`. | CHECK values in DAT-CODE-001 | `SCR-002-F08`; API-003 |
| DAT-003-F05 | `cases.revision` | Current monotonic revision | `BIGINT` | `NOT NULL DEFAULT 1` | Revision-safe mutation required; no additional DDL range CHECK supplied | `SCR-002-F11`; API-CNC-001 |
| DAT-003-F06 | `cases.sensitivity` | Case information class | `TEXT` | `NOT NULL DEFAULT 'INTERNAL'` | Information-class vocabulary confirmed; source DDL has no sensitivity CHECK | `SCR-002-F10`; API-CLS-001 |
| DAT-003-F07 | `cases.created_at` | Creation timestamp | `TIMESTAMPTZ` | `NOT NULL DEFAULT now()` | UTC durable semantics | `SCR-002-F12` |
| DAT-003-F08 | `cases.updated_at` | Updated timestamp | `TIMESTAMPTZ` | `NOT NULL DEFAULT now()` | DDL default does not establish an update trigger or accepted-change timestamp rule | `SCR-002-F12`; **DAT-OQ-005** |

**Confirmed table-level controls:**

- `UNIQUE (tenant_id, id)`.
- `ALTER TABLE cases ENABLE ROW LEVEL SECURITY`.
- Policy name `tenant_scope`.
- Access predicate: `tenant_id = current_setting('app.tenant_id')::UUID`.
- Connection-pool scoped session variables reset after every transaction.
- Production must additionally enforce workspace-tenancy membership through foreign keys or controlled write procedures.

**Source:** S, p. 86, Appendix B.2.

#### Required Domain Information Omitted from the Abbreviated DDL

These fields remain required domain concepts. Their physical columns, nullable status, public properties, and form requiredness are not supplied.

| Field ID | Logical/source name | Meaning and type | Required/default status | Constraints / earlier mapping |
|---|---|---|---|---|
| DAT-003-F09 | Title | Stored case title; semantic text | Field existence Confirmed; required input, blank rules, and default Needs confirmation | Length, trimming, markup, and allowed characters unresolved; `SCR-002-F03`, API-001/003 |
| DAT-003-F10 | Description / business context | Stored case description/context; semantic text or structured context | Field existence Confirmed; required input/default unresolved | Plain/rich text and schema unresolved; `SCR-002-F04`, API-001/003 |
| DAT-003-F11 | Impact | Explicit business impact input; code/value type unresolved | Input existence Confirmed; requiredness/default unresolved | Used with urgency for priority; catalog/matrix unresolved; `SCR-002-F05` |
| DAT-003-F12 | Urgency | Explicit business urgency input; code/value type unresolved | Input existence Confirmed; requiredness/default unresolved | Catalog/matrix unresolved; `SCR-002-F06` |
| DAT-003-F13 | Priority | Stored derived priority; code/value type unresolved | Field existence Confirmed; calculation/default unresolved | Derived from explicit impact and urgency, never model alone; direct override rules unresolved; `SCR-002-F07` |
| DAT-003-F14 | Owner | Stored principal relationship | Field existence Confirmed; initial assignment/nullability unresolved | `Owner` API scope mapping and reassignment rules unresolved; `SCR-002-F09` |
| DAT-003-F15 | Current approved result / final response pointer | Reference or representation of exact published artifact | Field existence Confirmed; absence before approval must be represented; SQL nullability/default unresolved | Updates only with satisfied publication gate; not ordinary PATCH input; `SCR-002-F16`, API-020 |
| DAT-003-F16 | Contractual deadline | Deadline derived from business calendar/workspace timezone | Behavior Confirmed; column/requiredness/default unresolved | Advisory prediction cannot modify it; `SCR-002-F15` |
| DAT-003-F17 | Advisory breach prediction | Nonbinding prediction about deadline breach | Behavior Confirmed; schema/persistence/default unresolved | Cannot change contractual deadline; `SCR-002-F15` |
| DAT-003-F18 | Human-facing case reference | Illustrated reference such as `OD-2026-1042` | Illustrated existence only; generation/persistence Needs confirmation | Not API UUID; uniqueness, sequencing, and length unresolved; `SF-CON-002`, `API-CNS-006` |

**Sources:** S, p. 12, §2.2.1; p. 14, Figure 2.2; pp. 24–25, §§6.1.2 and 6.3.1.  
**Needs confirmation:** **DAT-OQ-005**. No additional SQL columns or UI defaults are finalized here.

### DAT-004, DAT-024, DAT-025, and DAT-026 — Case History and Classification

| Field ID | Source name / physical name | Meaning | Type / required status | Constraints / unresolved mapping |
|---|---|---|---|---|
| DAT-004-F01 | `case_revisions.case_id` | Case whose revision is recorded | Logical case reference; logically required revision association | SQL FK/PK and tenant-qualified enforcement Needs confirmation |
| DAT-004-F02 | `case_revisions.revision` | Recorded case revision | Monotonic revision semantics; physical type Needs confirmation | Immutable accepted revision; uniqueness design not supplied |
| DAT-004-F03 | `case_revisions.patch` | Accepted change representation | Structured patch; exact schema and requiredness Needs confirmation | Do not assume JSON Patch or Merge Patch |
| DAT-004-F04 | `case_revisions.actor` | Responsible actor | Principal reference | Mapping to `actor_id`, historical principal deletion behavior unresolved |
| DAT-004-F05 | `case_revisions.at` | Revision occurrence time | UTC timestamp semantics | Mapping to `occurred_at`, SQL type/default unresolved |
| DAT-024-F01 | Labels | Asynchronous classification labels | Collection/code structure unresolved | Label catalog and empty-result representation Needs confirmation |
| DAT-024-F02 | Confidences | Classifier confidence values | Numeric/structured representation; range/precision unresolved | No `0..1` range or threshold is confirmed |
| DAT-024-F03 | Provenance | Classification source/version/context | Structured evidence; schema unresolved | Preserve with classification and correction |
| DAT-024-F04 | Correction reason code | Reason for user label correction | Code type/catalog/length unresolved; required for correction | API-051 and `SCR-002-F14` |
| DAT-025-F01 | Case-state change identity and context | State event linked to case/revision | Event identity and trusted mutation context required | Separate table versus history/outbox projection unresolved |
| DAT-026-F01 | Approved answer snapshot | Exact approved answer at closure | Immutable artifact/reference semantics; snapshot required on closure | Format, content/reference strategy, and local key unresolved |
| DAT-026-F02 | Cited document versions | Immutable evidence versions used by closed result | Reference collection; logically required closure lineage | No substitution with latest source version |
| DAT-026-F03 | Reviewer decisions | Decisions supporting the closed approved answer | Immutable decision references/snapshot | Preserve previous decision history on reopening |

**Sources:** S, p. 12, §2.2.1; pp. 25–26, §§6.2–6.3; p. 85, B.1.  
**Mappings:** `SCR-002-F13–16`, `SCR-002-A03–04`, `A07–08`; API-003, API-017, API-051–052.  
**Needs confirmation:** **DAT-OQ-005**. Initial history insertion, revision uniqueness, complete patch schema, classification catalogs, and closure/reopening physical lineage are unresolved.

### DAT-005, DAT-006, DAT-007, DAT-023, DAT-029, DAT-030, and DAT-035 — Documents and Provenance

| Field ID | Source field / physical name | Meaning | Type / required / optional status | Constraints and unresolved design |
|---|---|---|---|---|
| DAT-005-F01 | `documents.id` | Stable internal document identity | Logical UUID; identity required | Exact PK/default declaration Needs confirmation |
| DAT-005-F02 | `documents.workspace_id` | Document workspace | Logical workspace reference | SQL FK/nullability and same-tenant enforcement unresolved |
| DAT-005-F03 | `documents.source_id` | Stable originating repository/source identity | Provider identifier; type/length unresolved | Stable during historic backfill; uniqueness scope across connector/provider/workspace unresolved |
| DAT-005-F04 | `documents.sensitivity` | Document information class | Classification code; physical type/default unresolved | Originating ACL still enforced; no document default `INTERNAL` established |
| DAT-005-F05 | Source title | Human-readable evidence source title | Semantic text; exact local field name/length unresolved | Required semantic evidence-item output |
| DAT-005-F06 | Source URI | Source provenance locator | URI semantics; physical name/format/length unresolved | Every chunk stores source URI; no unrestricted URL-fetch authorization |
| DAT-006-F01 | Version identity; referring name `document_version_id` | Immutable document version identity | Logical immutable identifier | B.1 does not name a local `document_versions.id` column; local identity/PK unresolved |
| DAT-006-F02 | `document_versions.document_id` | Parent document | Logical document reference; associated version requires parent | SQL FK/nullability unresolved |
| DAT-006-F03 | `document_versions.hash` | Source/version content fingerprint | Digest; exact algorithm/encoding unresolved | Immutable; distinguish from `chunks.text_hash` and artifact hashes |
| DAT-006-F04 | `document_versions.parser_version` | Parser version used for processing | Version reference; type/length unresolved | Relation to normalization pipeline version Needs confirmation |
| DAT-006-F05 | `document_versions.object_key` | Stored object locator | Opaque internal key semantics | Key includes required scope dimensions; exact role/reference layout unresolved |
| DAT-006-F06 | Pipeline version / content fingerprint | Inputs to immutable derivative identity | Version and digest concepts | Fingerprint + pipeline version produces immutable derivative IDs; exact derivation and UUIDv7 relationship unresolved |
| DAT-007-F01 | `chunks.id` | Immutable chunk identity | Logical identifier | Source-anchor integrity required |
| DAT-007-F02 | `chunks.document_version_id` | Parent immutable version | Logical version reference; required chunk provenance | FK and local version identity unresolved |
| DAT-007-F03 | `chunks.page` | Source page number/index | Page/anchor value; numeric type/index convention unresolved | Every chunk retains source page provenance; nonpaginated-source semantics unresolved |
| DAT-007-F04 | `chunks.bbox` | Source bounding-box geometry | Optional structured geometry | Explicitly optional; coordinates, units, origin, precision, and boundary rules unresolved |
| DAT-007-F05 | `chunks.text_hash` | Normalized chunk text fingerprint | Digest; type/encoding unresolved | Distinct from original file hash |
| DAT-007-F06 | Source URI / file hash | Chunk provenance back to source | Logically stored for every chunk | Local storage versus resolved reference mapping unresolved |
| DAT-023-F01 | Attachment identity | Separate case attachment identity | Immutable identifier semantics | Exact column/PK and receipt mapping unresolved |
| DAT-023-F02 | Case and document-version references | Attachment linkage | Logical references; required attachment association | Version is immutable; duplicate/reuse/unlink behavior unresolved |
| DAT-023-F03 | File content | Accepted uploaded binary source | Binary file; required when uploading | Allowed formats and cap under DAT-FILE-001 |
| DAT-023-F04 | Filename / type metadata | Original filename, extension, detected MIME information | Text/type metadata; exact fields/requiredness unresolved | Name length, file-count limits, multipart structure, and MIME values unresolved |
| DAT-029-F01 | Document processing state | Scan/extraction/indexing readiness | Values DAT-CODE-003 | Physical status location, requiredness/default, and transition matrix unresolved |
| DAT-029-F02 | Empty-page ratio | Extraction quality indicator | Numeric/structured value; precision/range unresolved | Threshold and calculation unresolved |
| DAT-029-F03 | Unknown-character ratio | Extraction quality indicator | Numeric/structured value; precision/range unresolved | Threshold and calculation unresolved |
| DAT-029-F04 | Table-loss indicators | Extraction loss evidence | Structured flags; schema unresolved | No implied Boolean-only representation |
| DAT-029-F05 | Language confidence | Extraction language quality | Numeric/structured value; range unresolved | Language catalog and confidence thresholds unresolved |
| DAT-029-F06 | Quarantine reason, correlation ID, remediation path | Safe poison/unsafe-record information | Codes/references/text; schemas unresolved | After bounded poison retries; unsafe content never indexed |
| DAT-029-F07 | OCR opt-in and provenance | Requested fallback and generated OCR indication | Option/provenance schema unresolved | Fallback opt-in; output provenance-marked; no automatic enabled fallback |
| DAT-030-F01 | Page index and bounding boxes | Layout-aware PDF block anchoring | Structured page/geometry data | Preserve layout source position |
| DAT-030-F02 | Table row/column annotations | Table structure | Structured annotations | Preserve row/column information; schemas unresolved |
| DAT-030-F03 | Headings and reading order | Chunk boundary inputs | Structured order/text metadata | Normalization does not rewrite claims |
| DAT-035-F01 | Blob key scope | Tenant/workspace/document/version/object role | Composite key concepts, not a selected path syntax | All dimensions required; role vocabulary unresolved |
| DAT-035-F02 | Public object name / signed delivery reference | Controlled source delivery | Opaque name and short-lived signed URL | Exact URL lifetime, representation, refresh, and authorization binding unresolved |
| DAT-035-F03 | Encryption/provenance reference | At-rest protection and source/revision lineage | Key/provenance reference | Mandatory encryption; register SHA-256 source/revision assertion retained; exact column binding unresolved |

**Sources:** S, pp. 24, 27–32, 51–53, 78; p. 85, B.1.  
**Mappings:** `SCR-002-F20–25`, `SCR-003-F03–10`; API-004, API-018, API-021–022, API-035–036, API-057.  
**Needs confirmation:** **DAT-OQ-006–010**. A safe low-quality document remains viewable, but the source does not establish permission to view or download quarantined unsafe content.

### DAT-008, DAT-009, DAT-038–042, and DAT-046 — Runs, Plans, Attempts, and Artifacts

| Field ID | Source field / physical name | Meaning | Type / required status | Constraints / unresolved mapping |
|---|---|---|---|---|
| DAT-008-F01 | `runs.id` | Durable run identity | Logical UUID; identity required | Immediate creation; exact receipt/public field mapping unresolved |
| DAT-008-F02 | `runs.case_id` | Associated saved case | Logical case reference | FK, same-tenant binding, and pinned case revision representation unresolved |
| DAT-008-F03 | `runs.status` | Current Run state | DAT-CODE-002; physical type/default unresolved | Persisted server state; not artifact display state |
| DAT-008-F04 | `runs.plan_revision` | Stored plan revision | Version/revision type unresolved | Stored before side effects; distinct from case and run revision |
| DAT-008-F05 | `runs.budget` | Runtime/tool/token budget | Structured budget; units/detail schema unresolved | Depth `8`, tool calls `16`, reference timeout `180` seconds; review wait treatment unresolved |
| DAT-009-F01 | `run_steps.id` | Execution step identity | Logical identifier | Exact operation key/uniqueness unresolved |
| DAT-009-F02 | `run_steps.run_id` | Parent run | Logical run reference | FK/nullability unresolved |
| DAT-009-F03 | `run_steps.step_kind` | Step category | Code vocabulary/type unresolved | Do not equate to all Run states |
| DAT-009-F04 | `run_steps.status` | Step state | Code vocabulary/type unresolved | Complete step enum not supplied |
| DAT-009-F05 | `run_steps.checkpoint` | Durable replayable step checkpoint | Structured checkpoint/reference | Written before downstream dispatch; schema unresolved |
| DAT-038-F01 | Scoped input and generation output | Versioned request context and structured provider result | Structured data; exact schema unresolved | Fixed system rules, signed workflow instruction, validated user input, separately delimited evidence |
| DAT-038-F02 | Deployment / template / evidence / usage linkage | Reproduce generation | References; exact names unresolved | Keep generation distinct from retrieval, policy, and approval |
| DAT-038-F03 | Validation and injection indicators | Model-schema and prompt-injection evidence | Safe structured flags/outcomes | Unknown fields, invalid citations, control injection yield `MODEL_OUTPUT_INVALID`; no unsafe diagnostics |
| DAT-039-F01 | Exact candidate artifact content | Candidate presented to reviewer | Immutable content/reference; format/length unresolved | Changed content cannot be approved under previous hash |
| DAT-039-F02 | Artifact hash; related `artifact_hash` | Exact reviewed/published-content identity | Hash; algorithm/encoding/canonicalization unresolved | Required binding; not client-authorized policy |
| DAT-039-F03 | Artifact/run revision lineage | Rework and historical content relationship | Immutable revision/reference concepts | Denied requests reworked as new run revisions, not historical approval edits |
| DAT-039-F04 | Artifact display label | Presentation of draft/publication | `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` | Exact stored-versus-derived representation unresolved; not Case status |
| DAT-040-F01 | Plan node and explicit dependencies | DAG structure | Node/reference graph; schemas unresolved | Acyclic; bounded depth `8`; does not impose an undocumented total-node limit |
| DAT-040-F02 | Plan revision / plan hash | Executed plan provenance | Revision/hash concepts | Plan hash occurs in `AgentPlanApproved`; algorithm/field mapping unresolved |
| DAT-041-F01 | Tool/capability name and schema version | Pinned discovery metadata | Versioned reference | Only allowlisted tools; discovery does not grant invocation |
| DAT-041-F02 | Principal/workspace/scope/classification authorization | Separate capability grant decision | Structured policy/reference | External writes separately authorized; consequential mutation requires human authorization |
| DAT-046-F01 | Run / stage / checkpoint context | Durable workflow progress | References and structured checkpoint | Mapping to `run_steps.checkpoint` and separate checkpoint record unresolved |
| DAT-046-F02 | Failed checkpoint/reason | Exact visible failure location | Safe code/reference metadata | No invented failure codes or `TIMED_OUT` state |

**Sources:** S, pp. 12, 38–42, 49, 57–58; pp. 85, 87, 90.  
**Mappings:** `SCR-002-F16–19`, `SCR-004-F01–10`, `SCR-005-F05–08`; API-005–008, API-019–020, API-032–033, API-046–047.  
**Needs confirmation:** **DAT-OQ-011**, **DAT-OQ-013**. These gaps do not remove the confirmed bounded plan, durable checkpoint, or exact-hash requirements.

### DAT-010 and DAT-031–034 — Evidence, Search, Index, and Cache

| Field ID | Source field / physical name | Meaning | Type / required status | Constraints |
|---|---|---|---|---|
| DAT-010-F01 | `evidence_sets.id` | Evidence-set identity | Logical UUID | Mapping to API-021 `evidenceId` and MCP `evidence_set_id` unresolved |
| DAT-010-F02 | `evidence_sets.run_id` | Associated run | Logical run reference | Physical nullability and runless public-search mapping unresolved |
| DAT-010-F03 | `evidence_sets.chunk_refs` | Selected immutable chunks | Reference collection; schema unresolved | Every used reference resolves to authorized source/version/anchor |
| DAT-010-F04 | `evidence_sets.acl_digest` | Permission-provenance digest | Digest; algorithm/encoding unresolved | Does not replace current ACL evaluation |
| DAT-010-F05 | Response evidence item: chunk ID | Selected chunk identity | Logical reference; semantic output required | Exact JSON property unresolved |
| DAT-010-F06 | Response evidence item: source title | Evidence source title | Text; semantic output required | Length/projection unresolved |
| DAT-010-F07 | Response evidence item: document revision | Cited immutable revision | Version/reference; semantic output required | Do not substitute current/latest version |
| DAT-010-F08 | Response evidence item: page anchor | Stored source location | Structured page/range; semantic output required | Resolvable before citation display |
| DAT-010-F09 | Response evidence item: ACL digest | Access provenance | Digest; semantic output required | Current permission independently required |
| DAT-010-F10 | Citation identifier | Opaque end-user citation reference | Opaque identifier | Verified before display; full `Citation` schema unresolved |
| DAT-031-F01 | `tenant_id` | Indexed tenant scope | Logical tenant reference; search row required | Not inferred from index alias alone |
| DAT-031-F02 | `workspace_id` | Indexed workspace scope | Logical workspace reference; search row required | Same-tenant source relationship |
| DAT-031-F03 | `document_version_id` | Immutable indexed source version | Logical reference; search row required | Match authoritative version/fingerprint |
| DAT-031-F04 | `chunk_id` | Indexed chunk reference | Logical reference; search row required | Maps to stored source anchor |
| DAT-031-F05 | `language` | Indexed language | Code/text; search row required | Language code system/length unresolved |
| DAT-031-F06 | `classification` | Indexed material class | Classification code; search row required | Link to DAT-CLS-001; physical code mapping unresolved |
| DAT-031-F07 | Embedding; physical field name not specified | Semantic search vector | `1536` dimensions confirmed; component type/precision unresolved | No search-provider vector SQL type selected |
| DAT-031-F08 | Text field; physical name not specified | Normalized keyword-search content | Text semantics; length/analyzer definitions unresolved | Nonauthoritative derivative; ACL filter before release |
| DAT-032-F01 | Index generation / versioned alias | Active/rebuild index identity | Version/reference; exact names unresolved | Parallel rebuild; atomic read-alias switch after completeness/recall checks |
| DAT-033-F01 | Query context | Validated lexical/vector query and evidence budget | Structured query; public property mapping unresolved | Hybrid RRF and deterministic reranking; selected token cap schema unresolved |
| DAT-034-F01 | Cache-key tenant | Cached tenant boundary | Logical tenant identity | Mandatory key component |
| DAT-034-F02 | User-scope digest | Cache authorization scope | Digest | Mandatory key component; format unresolved |
| DAT-034-F03 | Source ACL revision | Permission version for result | Revision/reference | Mandatory key component; change purges affected entries |
| DAT-034-F04 | Query hash | Query fingerprint | Digest | Mandatory key component; canonicalization unresolved |
| DAT-034-F05 | Index generation | Search-generation context | Version/reference | Mandatory key component; index commit invalidates cache |
| DAT-034-F06 | Cached result / TTL | Ephemeral versioned result | Structured result/expiry semantics | Short TTL confirmed; numeric TTL, size, and storage format unresolved |

**Sources:** S, pp. 16, 31, 34–36, 53; pp. 85, 87.  
**Mappings:** `SCR-003-F01–12`; API-010, API-021–022, API-046.  
**Needs confirmation:** **DAT-OQ-009**. Backend candidate/selection budgets are not public pagination defaults.

### DAT-011, DAT-012, DAT-017, and DAT-043 — Policy and Review

| Field ID | Source field / physical name | Meaning | Type / required / optional status | Constraints / unresolved mapping |
|---|---|---|---|---|
| DAT-011-F01 | `approval_tasks.id` | Task identity | Logical identifier | Mapping to route `approvalId` unresolved |
| DAT-011-F02 | `approval_tasks.run_id` | Reviewed run | Logical run reference | Candidate/revision association must remain exact |
| DAT-011-F03 | `approval_tasks.reviewer_pool` | Policy-defined eligible reviewer pool | Reference/collection semantics unresolved | Minimum role and separation of duties |
| DAT-011-F04 | `approval_tasks.artifact_hash` | Exact assigned candidate hash | Hash binding required | Algorithm/encoding unresolved; no self-approval |
| DAT-011-F05 | Review state; physical name not specified | Task lifecycle state | DAT-CODE-004 | Default/transition matrix/state storage unresolved |
| DAT-011-F06 | Minimum role / assignment / separation-of-duty constraints | Required reviewer eligibility | Policy references/attributes | No unrestricted reviewer self-assignment |
| DAT-011-F07 | Configured expiry / SLA | Review deadline and routing on expiry | Timestamp/duration concepts; units/schema unresolved | Reassign/escalate; no implicit approval |
| DAT-012-F01 | `approval_decisions.id` | Immutable decision identity | Logical identifier | PK/default unresolved |
| DAT-012-F02 | `approval_decisions.task_id` | Target task | Logical task reference | FK and accepted-decision count unresolved |
| DAT-012-F03 | `approval_decisions.reviewer_id` | Authenticated decision actor | Principal reference; required captured actor | Mapping to `actor_id` and service actor semantics unresolved |
| DAT-012-F04 | `approval_decisions.decision` | Approve/reject outcome | Decision code; literal storage/request values unresolved | Do not infer `APPROVE` or `APPROVED` from controls |
| DAT-012-F05 | `approval_decisions.reason` | Rationale | Text/structured explanation; length unresolved | Rationale included in approval record; exact form-requiredness and blank rules unresolved |
| DAT-012-F06 | Decision timestamp; physical name not specified | Recorded action time | UTC timestamp; logically required | Server-derived, immutable |
| DAT-012-F07 | Evaluated artifact hash; physical name not specified | Content actually reviewed | Hash binding; logically required | Direct storage versus immutable task/artifact linkage unresolved |
| DAT-012-F08 | Optional annotations; physical name not specified | Additional reviewer notes | Optional text/structured value | Schema/length/default unresolved |
| DAT-017-F01 | `policy_evaluations.run_id` | Evaluated run context | Logical run reference | Reproducibility linkage required |
| DAT-017-F02 | `policy_evaluations.rule_version` | Rule-set version used | Version reference | Mapping to workspace `policy_version` unresolved |
| DAT-017-F03 | `policy_evaluations.input_digest` | Digest of normalized inputs | Digest | Digest alone does not satisfy requirement to store all normalized inputs |
| DAT-017-F04 | `policy_evaluations.result` | Deterministic outcome | DAT-CODE-005 | LLM cannot override result |
| DAT-017-F05 | Case sensitivity | First source policy input | Classification context | Normalize/store with rule-set version; also obey maximum-material control |
| DAT-017-F06 | Requested action | Second source policy input | Action code/context; catalog unresolved | Authorized action context |
| DAT-017-F07 | Evidence quality | Third source policy input | Quality structure; thresholds unresolved | Exclude inappropriate evidence for autonomous recommendation |
| DAT-017-F08 | Model class | Fourth source policy input | Model-class reference; mapping unresolved | Registry policy requirements |
| DAT-017-F09 | Financial-impact category | Fifth source policy input | Category code; values unresolved | Not permission for irreversible financial transactions |
| DAT-017-F10 | Confidence bands | Sixth source policy input | Band codes/structure; thresholds unresolved | No invented numeric bands |
| DAT-017-F11 | Policy reasons / normalized-input provenance | Reproducible explanation and context | Structured values; physical names unresolved | Reviewer sees reasons; retain evaluated version |
| DAT-043-F01 | Exact artifact and satisfied gate context | Evidence/policy/approval satisfaction | References and evaluated gate data | Gate and final pointer commit atomically |
| DAT-043-F02 | Current permissions / evidence versions / approval decisions | Publication revalidation evidence | Authorized immutable references plus current checks | Wrong artifact, stale ACL, missing approval, or unsupported citations cannot publish |
| DAT-043-F03 | Override context | Elevated actor, secondary reviewer, audited reason | References/reason; schema unresolved | Separate authorized override; no historical decision rewrite |

**Sources:** S, pp. 11–12, 44–46, 51, 58; p. 85, B.1.  
**Mappings:** `SCR-005-F01–13`, `SCR-002-A09`, `SCR-007-F06–11`; API-020, API-023–024, API-053.  
**Needs confirmation:** **DAT-OQ-013**, **DAT-OQ-016**.

### DAT-CLS-001 — Maximum Included-Material Classification

**Confirmed:** Information classes are `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, and `RESTRICTED`. For every run, model routing, log redaction, retention, and approval policy depend on the maximum class of any material included in that run.

| Data/control requirement | Confirmed obligation | Physical design status |
|---|---|---|
| Material classification | Preserve classification context of included material, including evidence | Exact classification-record granularity, source/version linkage, and provenance **Needs confirmation** |
| Run control selection | Apply the maximum included-material class, not only `cases.sensitivity` | No new column or public response field is established |
| Model routing | Initial and fallback deployment selection obey the highest included class | Per-class deployment mapping **Needs confirmation** |
| Log redaction | Highest-class redaction applies; global prohibition on document/secret diagnostics remains | Detailed redaction policy/version linkage **Needs confirmation** |
| Retention | Highest-class retention selection applies while preserving legal holds and approved lineage | Per-class duration and eligibility mapping **Needs confirmation** |
| Approval policy | Highest included class determines requirements and publication validation | Detailed rule/version storage and task linkage **Needs confirmation** |

**Source:** S, p. 62, §17.2.1.  
**Earlier requirements:** [API-CLS-001](02_api.md#api-cls-001), `API-005-P01`, `API-008-P01`, `API-020-P01`, `API-AC-034`; `SCR-002-F10`, `SCR-007-F09–11`.

**Confirmed consequences:**

1. A permitted `RESTRICTED` document included in an `INTERNAL` case run requires the applicable `RESTRICTED` controls across all four categories.
2. ACL permission does not authorize lower-class routing or approval policy.
3. Reference `require_human_review_for: [HIGH_RISK, RESTRICTED]` remains applicable. `HIGH_RISK` is a risk category, not a fifth information class.
4. `auto_publish_classification: INTERNAL` is not an evidence/risk/approval bypass.
5. The source does not require rewriting the case sensitivity to represent the run’s control classification.
6. The source does not add a seventh deterministic policy input or a client-controlled classification override.

**Needs confirmation — DAT-OQ-016:** Classification provenance/storage/transport, treatment of unclassified material, version activation, and per-class control mappings. The maximum-class rule is already Confirmed and must not be deferred as optional.

### DAT-013–018, DAT-027–028, and DAT-044–050 — Ledgers and Delivery

| Field ID | Source field / physical name | Meaning / type | Requiredness and constraints |
|---|---|---|---|
| DAT-013-F01 | `audit_events.id` | Audit identity; logical UUID | Append-only identity; physical PK unresolved |
| DAT-013-F02 | `audit_events.tenant_id` | Audit tenant | Required tenant context |
| DAT-013-F03 | `audit_events.actor_id` | Recorded actor | Required relevant action/denial context |
| DAT-013-F04 | `audit_events.action` | Action/decision metadata; code vocabulary unresolved | Exact action enum not supplied |
| DAT-013-F05 | `audit_events.digest` | Audit digest; encoding/algorithm field mapping unresolved | Append-only; batch hash-chain export |
| DAT-013-F06 | Occurrence, correlation, template digest, access/decision lineage | Safe audit evidence; physical fields unresolved | Auditor redacted scope; no historical edit |
| DAT-014-F01 | `outbox_events.event_id` | Original event identity | Deduplication identity; full PK declaration unresolved |
| DAT-014-F02 | `outbox_events.tenant_id` | Event tenant | Required immutable tenant |
| DAT-014-F03 | `outbox_events.aggregate_revision` | Revision of affected aggregate | Required stale/replay check; physical type unresolved |
| DAT-014-F04 | `outbox_events.payload` | Versioned canonical event payload | Exact event-specific JSON schemas unresolved |
| DAT-015-F01 | `connector_cursors.connector_id` | Connector association | Logical connector reference; PK/partitioning unresolved |
| DAT-015-F02 | `connector_cursors.cursor` | Provider cursor | Provider-specific opaque value; nullability/encoding unresolved |
| DAT-015-F03 | `connector_cursors.watermark` | High-watermark | Provider ordering/time/token semantics unresolved |
| DAT-015-F04 | `connector_cursors.retry_state` | Durable retry progress | Structured state; enum/schema/default unresolved |
| DAT-016-F01 | `token_ledger.run_id` | Run attribution | Logical run reference |
| DAT-016-F02 | `token_ledger.deployment_id` | Specific model deployment attribution | Logical deployment reference; physical key unresolved |
| DAT-016-F03 | `token_ledger.in_tokens` | Input token usage | Numeric count semantics; physical type/range/default unresolved |
| DAT-016-F04 | `token_ledger.out_tokens` | Output token usage | Numeric count semantics; physical type/range/default unresolved |
| DAT-018-F01 | `deletion_receipts.tenant_id` | Purge tenant | Required auditable tenant context |
| DAT-018-F02 | `deletion_receipts.object_ref` | Object affected by purge | Reference format/length unresolved; must identify inventory item |
| DAT-018-F03 | `deletion_receipts.purge_time` | Purge occurrence | UTC timestamp semantics; physical type/default unresolved |
| DAT-018-F04 | `deletion_receipts.actor` | Responsible purge actor | Principal/service reference; mapping to `actor_id` unresolved |
| DAT-018-F05 | Completion receipt / held-record exception / receipt hash | Verified purge evidence | Required lifecycle evidence; schema and hash algorithm unresolved |
| DAT-027-F01 | Connector identity / workspace / repository configuration | Scoped connector metadata | Field names/types/provider catalog unresolved |
| DAT-027-F02 | Capability support | List, fetch, delta cursor, ACL, delete support | Advertised capability concepts required; representation unresolved |
| DAT-027-F03 | Credential reference | Workspace-scoped vault reference | Never raw secret in public fields |
| DAT-027-F04 | Lower-trust mode / warning | Unsupported capability condition | Must be explicit and user-visible; code schema unresolved |
| DAT-028-F01 | Provider cursor / high-watermark | Per-sync-run durable source progress | Every sync run stores both; allocation to DAT-015/history unresolved |
| DAT-028-F02 | Error ledger / durable item outcomes | Completed or quarantined preceding-item evidence | Required before cursor advances |
| DAT-028-F03 | Reason code / correlation ID / remediation path | Poison-record outcome | Required after bounded retries; retry count/schema unresolved |
| DAT-028-F04 | Sync state / retry timing | Current synchronization outcome | Complete state enum and scheduling fields unresolved |
| DAT-044-F01 | `Idempotency-Key` | HTTP operation key | Required for job-creating POSTs and case creation; no SQL column name established |
| DAT-044-F02 | Actor / request fingerprint / original outcome | One-result binding | Case binding retained for `24` hours; key namespace/canonicalization/storage unresolved |
| DAT-045-F01 | Event ID / operation key / aggregate revision | Consumer deduplication and stale detection | Required replay-safe concepts; table/schema/uniqueness unresolved |
| DAT-045-F02 | Duplicate outcome | Record that delivery was duplicate | Must not reapply mutation; schema/retention unresolved |
| DAT-047-F01 | Original event / failure context | Dead-letter recovery subject | Exact safe fields and error-state enum unresolved |
| DAT-047-F02 | Operator reason / dry-run / scope limit | Replay prerequisites | Required semantics; reason constraints and numeric scope bound unresolved |
| DAT-047-F03 | Migration provenance link | Explicit transformed-schema lineage | Required if replay migration changes schema/identity |
| DAT-049-F01 | SSE offset / `Last-Event-ID` | Resume cursor | Monotonically increasing; type/retention/expiry unresolved |
| DAT-050-F01 | Recipient/subscription context | Optional outbound target and event selection | Exact fields/method/URL management unresolved |
| DAT-050-F02 | Signature / event age / retry context | Safe outbound delivery | Signed, age verified, exponential retry; algorithms/limits unresolved |

**Sources:** S, pp. 25, 27–29, 38, 48–55, 62, 65–66, 79–80; p. 85, B.1.  
**Mappings:** API-007, API-009, API-011–012, API-015, API-025, API-034, API-036, API-048; related `SCR-004`, `SCR-006`, `SCR-008`, `SCR-010`.  
**Needs confirmation:** **DAT-OQ-006**, **DAT-OQ-012**, **DAT-OQ-014**, **DAT-OQ-018**.

### DAT-014 and DAT-048 — Confirmed Event Envelope Fields

| Field | Meaning | Type / format | Required status | Mapping |
|---|---|---|---|---|
| `event_id` | Original event identity | UUIDv7 identifier policy; exact wire declaration unresolved | Required | DAT-014-F01; consumer deduplication |
| `type` | Event name | Exact event vocabulary; string/schema details unresolved | Required | DAT-EVT-001 |
| `schema_version` | Envelope/payload version | Version representation unresolved | Required | Repository-controlled contracts |
| `tenant_id` | Immutable tenant context | Logical tenant identity; signed job context | Required | DAT-COM-F02 |
| `aggregate_id` | Affected aggregate | Logical identifier; mapping per event unresolved | Required | Aggregate lineage |
| `aggregate_revision` | Affected revision | Revision representation unresolved | Required | DAT-014-F03 |
| `occurred_at` | UTC occurrence time | Timestamp; RFC 3339 representation where exposed | Required | DAT-COM-F05 |
| `trace_id` | Trace context | Identifier format/length unresolved | Required | DAT-COM-F06 |
| `payload` | Event-specific data | Canonical JSON | Required | DAT-014-F04 |

**Source:** S, p. 48, §13.1.1.  
**Earlier mapping:** `API-EVT-001`.

**Needs confirmation — DAT-OQ-012:** Canonical JSON byte rules, signatures, schema versioning, actor/correlation placement, event-specific payload fields, and storage projection. Required mutation actor/correlation context must be preserved, but no additional envelope property name is invented here.

### Remaining Logical Record Field Contracts

All rows inherit shared context requirements when they change durable state. Exact SQL table names, PK/FK definitions, lengths, precision, nullability, and defaults are **Needs confirmation** unless stated.

| Field ID / record family | Source-supported field concepts and meaning | Required behavior / values | Source and adjacent decision |
|---|---|---|---|
| DAT-019-F01 — Principal/Actor | Issuer, audience, expiry, subject, tenant; user/service identity | Required access-token concepts; missing tenant or unexpected algorithm rejected. Token claim names and persistent identity mapping unresolved. | S, pp. 21–23; **DAT-OQ-004** |
| DAT-020-F01 — Membership | Principal, tenant/workspace membership, role bindings | Baseline roles DAT-CODE-006; revision-safe durable change; exact association/uniqueness unresolved | S, pp. 21–23, 78; **DAT-OQ-004** |
| DAT-021-F01 / DAT-022-F01 — AccessPolicy/ResourceAcl | Role, tenant, workspace, sensitivity, source ACL, action, separation of duties; source ACL revision | Evaluate at edge and again transaction/resource boundary; preserve denial principal/resource class | S, pp. 22–23, 28, 53; **DAT-OQ-004** |
| DAT-036-F01 — ModelDeployment | Capability, region, data-handling class, context length, cost profile, evaluation approval, specific deployment identity | Registry supports approved specific deployment selection/fallback; no provider brand-only whitelist | S, p. 37, §10.1; **DAT-OQ-011**, **DAT-OQ-016** |
| DAT-037-F01 — PromptTemplate | Template content/version, digest, fixed rules and composition context | Reproduce used prompt version; SHA-256 source/revision register assertion; no full prompts in ordinary diagnostics/export | S, pp. 37–39, 58, 73, 79; **DAT-OQ-011**, **DAT-OQ-019** |
| DAT-051-F01 — DataClassification | Material class and run aggregation provenance | DAT-CLS-001 across all four controls; exact physical fields unresolved | S, p. 62, §17.2.1; **DAT-OQ-016** |
| DAT-052-F01 — KeyReference | Vault reference, scope and rotation provenance | Vault-backed secrets; no bulk re-encryption in request path; no raw-key response | S, pp. 63, 71–72; **DAT-OQ-015** |
| DAT-053-F01 — Hold | Protected inventory/retention exception context | Preserve held records and receipt exceptions; target IDs, states, creation/release rules unresolved | S, pp. 26, 61–63, 80; **DAT-OQ-018** |
| DAT-054-F01 — ThreatControl | Threat/control/negative-test linkage | Each source threat has preventive control and negative verification; `SEC-001`–`SEC-012` named as release-blocking, detailed mapping not supplied | S, pp. 61, 88; **DAT-OQ-019** |
| DAT-054-F02 — TraceSpan | `trace_id`, `correlation_id`, child-span identifiers, policy outcomes | DB/connector/retrieval/model/approval correlation; identifiers/outcomes only, no document content or API secrets | S, p. 64, §18.1.1; **DAT-OQ-014** |
| DAT-054-F03 — MetricSeries | Request/error rates, latency, saturation, grounding pass rate, retrieval empty rate, throttling, token use, approval backlog age | Metric concepts Confirmed; exact labels, units, time buckets, and store unresolved | S, pp. 64–65; **DAT-OQ-014** |
| DAT-054-F04 — CostLedger | Workspace cost center, deployment version, model/embedding/storage/index usage, budget, forecast, rejected excess requests | Attributed usage and daily rollups; currency, precision, billing semantics unresolved | S, p. 65, §18.3.1; **DAT-OQ-014** |
| DAT-054-F05 — AlertPolicy | User-impacting incident conditions; spend anomaly ticket owner/threshold | Pages reserved for user impact; routine spend anomalies create tickets. No actual owner/threshold value supplied. | S, p. 65, §18.2.2; **DAT-OQ-014** |
| DAT-055-F01 — CapacityBudget/AdmissionPermit | Workspace tokens, queue age, provider capacity, quota/load context | Admit only under configured thresholds; no new universal quota | S, pp. 68–69; **DAT-OQ-020** |
| DAT-055-F02 — RecoveryCheckpoint/LoadProfile | Backup/restore evidence, object versions, rebuild recipes, fault-test result | Reference RPO `<=15 minutes`, RTO `<=4 hours`; separate raw/normalized/vector/replication accounting | S, pp. 68–70; **DAT-OQ-020** |
| DAT-056-F01 — ReleaseArtifact | Image digest, allowed build identity, schemas, prompts, model-routing policy, SBOM/test evidence | Signed image and verified digest; reconstruct deployed binary/prompt/policy versions | S, pp. 71–73, 89; **DAT-OQ-019** |
| DAT-056-F02 — ConfigVersion | Nonsecret defaults, signed environment configuration, secret references | Defaults in source control; environment values signed; raw credentials/keys only in vault | S, pp. 71–72; **DAT-OQ-019** |
| DAT-056-F03 — MigrationPlan/RolloutGate | Backfill/constraint compatibility, old-reader/new-writer behavior, canary measures, operator sign-off | Backward-compatible predeploy; enforcement after old replicas drain; no automatic DB down-migration | S, pp. 52, 72–73; **DAT-OQ-019** |
| DAT-057-F01 — TestCase/EvalDataset | Synthetic examples, permissions, expected citation sets/outcomes, dataset version, signed manifest, random seed | Reference corpus `1,200` cases; frozen/versioned/independently reviewed; randomized tests store seed | S, pp. 75, 88–89; **DAT-OQ-017** |
| DAT-057-F02 — Scorecard | Actual precision, unsupported-claim rate, high-risk recall, domain confidence intervals, distribution shift | Targets `>=0.97`, `<=0.02`, `1.00`; schema/precision/statistical definitions unresolved | S, p. 75, §21.2.2; **DAT-OQ-017** |
| DAT-057-F03 — ReleaseGateResult | Evaluation/safety confidence and release evidence | Critical isolation/approval zero exceptions; low confidence blocks release; signed output referenced by release digest | S, pp. 74–76, 89; **DAT-OQ-017** |
| DAT-058-F01 — ProvisioningJob | Workspace policy, encryption references, role bindings, quota, connector stubs, completion/progress context | One idempotent workflow; incomplete provisioning visible and sync blocked | S, p. 78, §22.1.1; **DAT-OQ-018** |
| DAT-058-F02 — Runbook/backfill evidence | Stable source IDs, bounded batch windows, reconciliation receipts, index coverage | Search readiness by coverage, not queue emptiness. Delayed-indexing incident evidence links audit IDs, time window, blast radius, quality effect, preventive action. | S, pp. 78, 90 F.1; **DAT-OQ-018**, **DAT-OQ-020** |
| DAT-059-F01 — ExportManifest | Case metadata, approved artifacts, source references, audit manifests, checksums, operation approvals | Required export inventory; secrets/internal model prompts excluded; exact manifest/archive schemas unresolved | S, pp. 78–80; **DAT-OQ-018** |
| DAT-060-F01 — ChangeRequest | Change impacts for behavior, data migration, threat surface, operating cost | Approved change increments minor revision; incompatible protocol change increments major; no impact scale supplied | S, pp. 8–10; **DAT-OQ-019** |
| DAT-060-F02 — DesignRevision/RequirementLink/DecisionRecord | Baseline revision, invariant/requirement links, at least one negative test per revised invariant, accepted decision lineage | Immutable baseline traceability and correlated `BaselineCommitted`; complete schema unresolved | S, pp. 8–10; **DAT-OQ-019** |
| DAT-061-F01 — ApiOperation | REST/protobuf contract/version and compatibility evidence | Repository-controlled IDL; no incompatible field deletion/enum change | S, pp. 54–56; **DAT-OQ-019** |
| DAT-061-F02 — ErrorEnvelope | `error.code`, `error.message`, `error.correlation_id`, `error.retryable`, optional `error.details` | String/string/string/Boolean semantics from example; `details` safe structured JSON; not automatically stored as a business entity | S, p. 84, A.3; **DAT-OQ-021** |
| DAT-062-F01 — ViewState/ReviewForm/EvidencePanel | Authorized resource context, exact candidate/citations/model-prompt versions/policy reasons | Reconstruct run progress from server; source inspection available before approval; required review fields completed | S, pp. 57–59; **DAT-OQ-021** |
| DAT-062-F02 — Notification | Scoped notification context | Channel/content/read-state schema and persistence not supplied | S, pp. 58–59; **DAT-OQ-021** |
| DAT-062-F03 — Illustrated summaries | Open cases, awaiting review, evidence coverage, service state, mixed workflow labels | Fixtures `128`, `14`, `97.6%`, `Healthy` are not defaults/limits or schema enums | S, p. 7, Reference UI A; **DAT-OQ-021** |
| DAT-063-F01 — Runtime/component records | Service/deployment/network identity, revision, actor, time, correlation where durable state changes | Source register concepts retained; no new operational SQL schemas or GET mutation side effects | S, pp. 15–20; **DAT-OQ-020** |

### Code Systems and Value Vocabularies

| Code ID | Applicable data | Exact confirmed values / conditions | Important distinction | Source |
|---|---|---|---|---|
| DAT-CODE-001 | Case `status` | `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED` | Initial business state `NEW`; only confirmed transitions in DAT-STATE-001 | S, pp. 25, 82, 86 |
| DAT-CODE-002 | Run state | `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED` | Do not invent `TIMED_OUT`, `CANCELLED`, or step enums | S, pp. 49, 82 |
| DAT-CODE-003 | Document processing state | `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED` | Enum does not establish full transition/default contract | S, p. 82, A.1 |
| DAT-CODE-004 | Review state | `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED` | Not the request/storage decision enum by assumption | S, p. 82, A.1 |
| DAT-CODE-005 | Policy result | `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY` | `DENY` is a policy outcome, not automatically an HTTP business error code | S, p. 44, §12.1.2 |
| DAT-CODE-006 | Baseline roles | `Analyst`, `Reviewer`, `Admin`, `Auditor`, `Service` | `Owner`, `Member`, `approver` are unresolved catalog scopes; Workspace Admin mapping unresolved | S, pp. 11, 22, 83 |
| DAT-CODE-007 | Information classes | `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` | `HIGH_RISK` is risk, not an information class | S, pp. 62, 90 |
| DAT-CODE-008 | Artifact display labels | `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` | Presentation vocabulary separate from Case/Run/Review states | S, p. 57, §16.1.2 |
| DAT-CODE-009 | Supported literal outcomes/errors | `CASE_VERSION_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `CONNECTOR_REAUTH_REQUIRED`, `NO_SUPPORTED_EVIDENCE`, `MODEL_OUTPUT_INVALID` | Preserve uppercase literals; other error/reason catalogs unresolved | S, pp. 25, 27, 36, 38, 54, 84, 89 |
| DAT-CODE-010 | MCP tool and permission | `knowledge.search@v1`; `read:permitted_documents` | Discovery metadata is not authorization | S, p. 87, C.2 |

**Needs confirmation:** Classification-label and correction-reason catalogs, impact/urgency/priority values, action and financial-impact categories, confidence bands, step/sync/provisioning/evaluation states, object roles, language codes, retention classes, and review decision literals. No values are added by this specification.

### Versioned Reference Configuration Values

These are source configuration examples, not newly selected SQL defaults or public request fields.

| Exact configuration path | Source value | Meaning / confirmed boundary | Unresolved semantics |
|---|---|---|---|
| `release` | `r1.0` | Reference configuration release | Relationship to display `R1.0` and schema/version IDs |
| `workflow.max_plan_depth` | `8` | Maximum DAG depth | Depth-counting convention |
| `workflow.max_tool_calls` | `16` | Maximum tool invocations | Retry/replay counting rules |
| `workflow.run_timeout_seconds` | `180` | Reference runtime timeout | Inclusion of human-review wait |
| `workflow.replay_dedup_hours` | `24` | Workflow replay deduplication baseline | Consumer ledger expiry; not general SSE/HTTP TTL |
| `retrieval.max_candidate_chunks` | `80` | Backend candidate budget | Collection strategy; not public page size |
| `retrieval.max_selected_chunks` | `10` | Backend selected evidence budget | Selection/token budget details |
| `retrieval.embed_dimension` | `1536` | Embedding dimension | Component precision and provider implementation |
| `retrieval.hybrid_rrf_k` | `60` | RRF reference configuration | Detailed ranking contract |
| `policy.auto_publish_classification` | `INTERNAL` | Reference policy setting | Must not bypass DAT-CLS-001 or publication gate |
| `policy.require_human_review_for` | `[HIGH_RISK, RESTRICTED]` | Reference mandatory review categories | Detailed risk classification and routing |
| `policy.self_approval_allowed` | `false` | Reference self-approval setting | No UI option to bypass high-risk prohibition |
| `storage.upload_limit_mb` | `25` | Configurable per-file cap | MB-to-byte conversion |
| `storage.user_data_region` | `primary-approved-region` | Placeholder for selected approved primary region | Actual region not selected |
| `observability.trace_sample_rate` | `0.10` | Reference sampling setting | Sampling implementation and audit separation |
| `observability.diagnostic_retention_days` | `30` | Diagnostic default retention | Detailed purge policy/hold handling |
| `observability.audit_retention_years` | `7` | Fictional security audit retention | Final corporate retention and year boundary rules |

**Source:** S, p. 90, Appendix F.  
**Needs confirmation:** **DAT-OQ-012**, **DAT-OQ-014–016**, **DAT-OQ-020**. Sampling does not authorize loss of required accepted-transition audit evidence.

## Lifecycle and Consistency

### Screen and API Data Access Matrix

`Create`, `Read`, and `Update` describe supported data effects, not undocumented table-level permissions. Deletion effects occur only through the guarded lifecycle operations described below.

| Data / lifecycle | Create / update origin | Read origin | Delete / archive effect | Confirmed guard and source |
|---|---|---|---|---|
| Case/current revision | `SCR-001-A03`, `SCR-002-A02`, `A04`; API-001, API-003 | `SCR-001-A01–02`, `SCR-002-A01`; API-002, API-016 | Eligible closed-case retention; controlled workspace/tenant deletion | Analyst creation, `Owner` PATCH scope, revision/tenant/domain checks. S, pp. 24–26, 83. |
| Case classification | Asynchronous classifier after `CaseCreated`; correction `SCR-002-A03`, API-051 | Case inquiry/projection; exact schema unresolved | Retention scope unresolved | Correction reason/provenance. S, p. 12. |
| Closure/reopening lineage | `SCR-002-A07–08`; API-017, API-052 | Case/history/audit projections; complete contracts unresolved | Held/retained lineage protected | New-revision reopening only; approved snapshot at closure. S, pp. 25–26. |
| Attachment/source/version/extraction | `SCR-002-A05`, API-004; connector workers after API-009 | API-018, API-021–022, API-035, API-057; `SCR-002`, `SCR-003` | Source tombstones; API-015/API-036 purge | Scan/type/safety, immutable version, current ACL. S, pp. 27–32, 51–53. |
| Search/index/cache | `DocumentNormalized` index build; `SearchIndexCommitted` cache invalidation; ACL change invalidation | `SCR-003-A01–04`; API-010, API-021–022, API-046 | Deleted source index removal; cache purge; alias containment | Index nonauthoritative; ACL before release. S, pp. 28, 34–36, 53, 87. |
| Run/plan/steps/checkpoints | `SCR-002-A06`, API-005; API-032 relationship unresolved; internal orchestration | `SCR-004`; API-006–007, API-019, API-033 | Retention/deletion scope unresolved | Admission, plan budgets, persisted plan before side effects, checkpoints before dispatch. S, pp. 40–42, 49, 69. |
| Generation/template/deployment/token records | API-008; versioned deployment/template administration contract incomplete | API-026; run/review/usage inquiry | Class-dependent retention and controlled deletion | Approved deployment, structured output, scoped context, token quota. S, pp. 37–39, 62. |
| Policy/task/decision/publication | Deterministic evaluation; `SCR-005-A03–04`, API-024; API-020 gate | `SCR-005`, API-023; audit API-011 | Immutable decisions retained under policy/holds; detailed purge relationship unresolved | Exact hash, eligible Reviewer, no high-risk self-approval; atomic gate/pointer. S, pp. 44–46, 62. |
| Connector/cursor/sync ledger | `SCR-006-A02`, API-009; credential revocation API-054 capability | `SCR-006-A01`, API-025 | Source deletion/tombstone; controlled lifecycle | Cursor only after durable preceding outcomes; reauth-safe queued failure. S, pp. 27–29. |
| Workspace settings/membership | `SCR-007-A02`, API-050; API-028; API-056 provisioning | API-027, API-049, authorized workspace context | Controlled lifecycle; exact removal semantics unresolved | Settings revision and audit; membership/resource checks. S, pp. 21–24, 78. |
| Audit/outbox/dedup/dead letters | Accepted/rejected action evidence; domain outbox; consumer outcome/replay | `SCR-008`, API-011; API-033–034 | Retention-safe archive/purge; ledger periods unresolved | Append-only audit, duplicate-safe consumer, guarded operator replay. S, pp. 48–52, 62, 66. |
| Usage/metrics/capacity | Usage/model/worker processing and daily rollups, not automatically caused by GET | `SCR-010`, API-012, API-040–042 | Diagnostic default TTL; other ledger retention unresolved | Privacy-safe attributed evidence. S, pp. 64–70. |
| Evaluation fixtures/results | `SCR-010-A02`, API-013; frozen versioned fixture management not fully defined | `SCR-010-A03`, API-045 | Dataset/result retention unresolved | Signed manifest, independent review, actual metrics/release gate. S, pp. 74–76, 88–89. |
| Hold/export/deletion | API-029, API-014–015, API-036; screen placement unresolved | Status/manifest/download APIs unresolved | Tombstones, blob/index removal, receipts, hold exceptions | Two independent checks; `Admin + approver`; no single-Admin bypass. S, pp. 78–83. |
| Governance/release/configuration | API-030, API-043 and repository release workflow | API-031, API-037, API-044 | History/retention unresolved | Version/test linkage, signed build/config, compatibility and sign-off. S, pp. 8–10, 55, 71–73. |
| View/notification/webhook state | Exact persistence and API-059 unresolved; optional API-048 delivery | Browser projections; API-058 aggregates unresolved | TTL/read-state/subscription deletion unresolved | No new screens or notification schemas inferred. S, pp. 55, 57–59. |

**DAT-LIFE-001 — Confirmed:** A GET inquiry is not automatically a business mutation, a job creator, or a producer of its chapter’s named event. The source’s repeated interface-boundary statements do not define such side effects.  
**Earlier consistency:** `API-CNS-011`.  
**Needs confirmation:** Per-interface fallback and projection contracts remain governed by existing API open questions.

### Tenant and Referential Integrity Requirements

| Requirement ID | Status | Requirement | Source / open dependency |
|---|---|---|---|
| DAT-RI-001 | Confirmed | Every tenant-owned row includes `tenant_id`; every storage access predicate includes tenancy. Apply tenant-scoped database context and RLS. | S, p. 22, §5.3.1; p. 51, Chapter 14 invariant |
| DAT-RI-002 | Confirmed | A case workspace must belong to the case tenant. Production enforcement uses foreign keys or controlled write procedures. | S, p. 86, B.2; implementation choice **DAT-OQ-003** |
| DAT-RI-003 | Confirmed | Reset scoped connection-pool session variables after every transaction. Reuse must not carry another tenant’s context. | S, p. 86, B.2 |
| DAT-RI-004 | Confirmed | Attachment references resolve to immutable document versions. Approvals reference exact run artifact hashes. | S, p. 51, §14.1.2 |
| DAT-RI-005 | Confirmed | Generated citations resolve to stored source anchors with current permission. Historical identity does not grant current source access. | S, p. 31, §8.3.1; p. 35, §9.3.1 |
| DAT-RI-006 | Confirmed | Source ACL changes invalidate affected cache before new retrieval results are served. Index/cache state cannot override authoritative ACLs. | S, p. 28, §7.2.2; p. 53, §14.3.2 |
| DAT-RI-007 | Confirmed | Soft-deleted entities cannot be retrieved. Final purge follows a tombstone pipeline. | S, p. 51, §14.1.2 |
| DAT-RI-008 | Needs confirmation | Complete FKs, tenant-qualified keys, delete/restrict/cascade behavior, cross-store orphan handling, and shared version/object retention. | S, pp. 51–53, 85–86; **DAT-OQ-003**, **DAT-OQ-008**, **DAT-OQ-018** |
| DAT-RI-009 | Confirmed | Foreign-tenant resource substitution yields the same not-found class as an absent ID. Safe denial evidence retains principal and denied resource class. | S, p. 23, §5.3.2; p. 89, `TST-003` |

### DAT-STATE-001 — Case Transition Data Contract

Preserve the confirmed transition IDs from Stage 1. An allowed edge remains subject to actor, revision, evidence, and approval guards.

| Earlier transition ID | From | To | Data effect / guard status |
|---|---|---|---|
| `SCR-002-T01` | `NEW` | `TRIAGED` | Accepted guarded revision/state change; actor/classifier trigger detail Needs confirmation |
| `SCR-002-T02` | `TRIAGED` | `IN_PROGRESS` | Accepted guarded revision/state change; actor/action trigger detail Needs confirmation |
| `SCR-002-T03` | `IN_PROGRESS` | `PENDING_APPROVAL` | Accepted guarded revision/state change; policy/task/candidate linkage Needs confirmation |
| `SCR-002-T04` | `IN_PROGRESS` | `RESOLVED` | Evidence and applicable approval policy still required; no approval bypass |
| `SCR-002-T05` | `PENDING_APPROVAL` | `RESOLVED` | Exact reviewed-hash, role, revision, evidence, and separation-of-duties obligations remain |
| `SCR-002-T06` | `PENDING_APPROVAL` | `IN_PROGRESS` | Authorized rework transition; not automatically every Reject decision |
| `SCR-002-T07` | Origin not specified | `CLOSED` | Closing capability and immutable snapshot confirmed; originating edge/guards unresolved |
| `SCR-002-T08` | `CLOSED` | Target not specified | Explicit reopening as a new revision only; preserve old lineage |

**Sources:** S, p. 25, §6.2.1; p. 26, §6.3.2; p. 82, A.1.  
**Earlier links:** `SF-CON-003`, `API-CNS-001`, `API-OQ-004`.  
**Needs confirmation — DAT-OQ-005:** Closing origin, reopening target/operation, edge-specific actor/approval rules, history shape, and rejected-decision-to-case-state linkage. Do not add `RESOLVED → CLOSED` or another ordinary transition by assumption.

### Other State and Stage Contracts

| Requirement ID | Data | Confirmed lifecycle | Unresolved details |
|---|---|---|---|
| DAT-STATE-002 | Run | Chapter 13 describes `REQUESTED → RETRIEVING → GENERATING → POLICY_CHECK → AWAITING_REVIEW → PUBLISHED` or terminal failure. Stages persist checkpoint before downstream dispatch. | Exact failure edges, `AUTO_ALLOW` publication path, missing-approval waiting versus termination, recoverable timeout representation, review-wait budget. **DAT-OQ-011**. |
| DAT-STATE-003 | Document | DAT-CODE-003 states; scan and quality gate govern readiness; unsafe content quarantined and never indexed. | Complete edge matrix, status location, failure/retry state and initial physical default. **DAT-OQ-007**. |
| DAT-STATE-004 | Review | DAT-CODE-004 states; actor/hash/separation guards; configured expiry reassigns/escalates, never silently approves. | Accepted decisions after expiry, assignment/open transition mutation, reassignment lineage, quorum. **DAT-OQ-013**. |
| DAT-STATE-005 | Sync/provisioning/evaluation/export/delete | Durable asynchronous work and outcomes are required where cataloged `202`; receipt is not completion. | Full state vocabularies and status/receipt schemas. **DAT-OQ-006**, **DAT-OQ-017–018**. |
| DAT-STATE-006 | Artifact | `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` labels reflect artifact status; partial processing is not approved output. | Stored/derived label mapping, direct draft editing, artifact revisions. **DAT-OQ-013**. |

**Sources:** S, pp. 12–13, 30–32, 41, 45, 49, 57–58, 78–83.

### Transactions, Concurrent Updates, and Idempotency

**DAT-TXN-001 — Confirmed:** Case mutations, approval decisions, and applicable outbox inserts commit in one ACID transaction. Search indexing and external webhook delivery are asynchronous and explicitly reconciled.  
**Source:** S, p. 52, §14.2.1.  
**Earlier links:** `API-TXN-001`, `API-TXN-003`.

**DAT-TXN-002 — Confirmed:** The final response pointer and satisfied approval gate commit in the same transaction. A replay cannot publish another artifact under an old approval.  
**Source:** S, p. 45, §12.3.1.  
**Earlier link:** `API-TXN-002`.

**DAT-TXN-003 — Confirmed:** A failed index write does not roll back accepted source metadata. Reconciliation compares source fingerprints, retries derivative writes, and repairs broken links from the outbox ledger.  
**Source:** S, p. 49, §13.2.2.

**DAT-TXN-004 — Needs confirmation:** Transaction isolation, locking, compare-and-update SQL, idempotency reservation, audit write placement beyond explicit boundaries, and crash recovery across relational/object stores. No distributed transaction implementation is selected. See **DAT-OQ-003**, **DAT-OQ-012**.

#### Accepted Mutation Data Procedure

1. Authenticate and establish trusted tenant, actor, trace, and correlation context.
2. Validate the approved request schema before transaction entry or long-running allocation.
3. Resolve the applicable idempotency key and original outcome.
4. Enter tenant-scoped transactional context.
5. Load current resource attributes; re-evaluate role, membership, sensitivity, ACL, action, and separation of duties.
6. Validate current revision and operation-specific state/hash/policy conditions.
7. Apply DAT-CLS-001 when run-included material is involved.
8. Write the accepted state and required append-only revision/decision evidence.
9. Insert the applicable outbox record in the confirmed ACID boundary.
10. Commit before reporting accepted durable work or dependent side effects.
11. Dispatch downstream work from durable records/checkpoints and reconcile external effects.
12. Reset connection-pool scope after the transaction.

**Sources:** S, pp. 22, 25, 45, 49, 52, 56, 62, 86.  
**Needs confirmation:** Approved schema and transaction mechanisms remain blocking decisions; the procedure does not finalize new SQL or error codes.

| Requirement ID | Confirmed consistency requirement | Source / unresolved detail |
|---|---|---|
| DAT-CNC-001 | Case mutations use `If-Match`; stale revision returns HTTP `409`, `CASE_VERSION_CONFLICT`, and current revision information. Business state unchanged. | S, pp. 25, 83–84; header/BIGINT representation **DAT-OQ-003** |
| DAT-CNC-002 | Workspace settings updates require revision preconditions and durable audit. | S, p. 24, §6.1.1; physical revision and API mapping **DAT-OQ-004** |
| DAT-CNC-003 | Case idempotency binds actor/request fingerprint/key to one outcome for `24` hours. Identical repeat returns original outcome; changed fingerprint yields `IDEMPOTENCY_CONFLICT`. | S, pp. 25, 54, 89; namespace/concurrency/error replay **DAT-OQ-012** |
| DAT-CNC-004 | Job-creating POSTs require `Idempotency-Key`; all cross-service writes are retry-safe. | S, pp. 15, 54; non-case retention/schema **DAT-OQ-012** |
| DAT-CNC-005 | Consumers deduplicate event ID and operation key, detect stale aggregate revision, and record duplicates without mutation. No invariant depends on cross-partition ordering. | S, pp. 17, 48–50 |
| DAT-CNC-006 | Every run stores plan revision before side effects; every stage checkpoint precedes downstream dispatch. | S, pp. 40, 49 |
| DAT-CNC-007 | Review acceptance checks the exact artifact hash; changed artifact is stale and audited. | S, pp. 44–45, 89 |
| DAT-CNC-008 | Rejected stale/unauthorized writes leave business state unchanged; rejection audit evidence is not permission to mutate the denied aggregate. | S, pp. 25, 45, design checkpoints |

### History, Auditing, and Replay

| Requirement ID | Status | Requirement | Source |
|---|---|---|---|
| DAT-HIS-001 | Confirmed | `case_revisions` is append-only. Immutable document versions, approved output lineage, and review decisions cannot be overwritten as ordinary edits. | S, pp. 24–26, 51, 62, 85 |
| DAT-HIS-002 | Confirmed | Capture decision, actor, timestamp, exact reviewed hash, rationale, and optional annotations. Preserve prior denial when creating a reworked run revision. | S, pp. 45–46 |
| DAT-HIS-003 | Confirmed | Audit entries are append-only, chained with batch hashes, and exported to independently controlled retention storage. Operators may query but not modify historical review decisions. | S, p. 62, §17.3.1 |
| DAT-HIS-004 | Confirmed | Accepted transitions have correlated audit evidence. Diagnostic traces contain identifiers and policy outcomes, never source document text or API secrets. | S, chapter acceptance sections; p. 64, §18.1.1 |
| DAT-HIS-005 | Confirmed | Replay requires operator reason, dry-run validation, and scope limit. Preserve original event identity unless schema migration includes explicit provenance linkage. | S, p. 50, §13.3.2 |
| DAT-HIS-006 | Needs confirmation | Audit-chain canonical bytes/hash fields, batch boundaries, archive verification, duplicate-attempt record counts, historical principal representation, and retained ledger schemas. | S, pp. 50, 62, 85; **DAT-OQ-012**, **DAT-OQ-014** |

### Retention, Export, Deletion, and Legal Holds

| Requirement ID / category | Confirmed retention or deletion rule | Needs confirmation |
|---|---|---|
| DAT-RET-001 — Closed case data | Retention jobs operate only on eligible closed cases; closure preserves approved answer, cited versions, reviewer decisions, and legal-hold exceptions. | Eligibility, retention classes/periods, schedule, and scope of related run/document objects |
| DAT-RET-002 — Diagnostics | Default TTL `30` days | TTL start, exact deletion job/store, holds and receipt representation |
| DAT-RET-003 — Security audit | Distinct fictional `7`-year policy; independently controlled archive | Final corporate policy, calculation boundaries, archive/purge format |
| DAT-RET-004 — Run material | Retention selection depends on maximum included-material class | No `RESTRICTED`-specific period is supplied; per-class mappings unresolved |
| DAT-RET-005 — Cache | Versioned ephemeral results with short TTL; authorization change purges early | Numeric TTL, expiry records, and recovery behavior |
| DAT-RET-006 — Idempotency/replay | Case binding `24` hours; reference workflow dedup setting `24` hours | Other HTTP keys, event ledgers, SSE, and outbox TTLs not established |
| DAT-RET-007 — Source deletion | Source delete creates tombstone and schedules index removal; soft-deleted entities not retrievable | Tombstone fields/schedule, retained cited history versus source purge |
| DAT-RET-008 — Export | Two independent approval checks; package case metadata, approved artifacts, source references, audit manifests/checksums; omit secrets/internal model prompts | Tenant/workspace extent, package/manifest schema, checksum algorithms, archive/download retention |
| DAT-RET-009 — Verified deletion | Two independent checks; enforce holds; tombstones; remove blobs/index entries; completion receipts | Relational deletion extent, partial status/retry, shared objects, backups, legal-hold release |
| DAT-RET-010 — Data-subject access | Use the same inventory as verified deletion | Subject matching, permitted disclosure/redaction, request/result schema |
| DAT-RET-011 — Keys/secrets | Vault-backed; rotate on policy without bulk re-encryption in request path | Rotation cadence, key isolation/throughput, revoked-key impact, destruction evidence |
| DAT-RET-012 — Evaluation/release/governance | Frozen versioned fixtures and reconstructible release/design evidence | Retention periods and lifecycle rules not described |

**Sources:** S, pp. 25–26, 51–53, 62–63, 66, 74–80, 90.  
**Open dependencies:** **DAT-OQ-012**, **DAT-OQ-014–019**.

#### Controlled Deletion Data Procedure

1. Resolve the authorized lifecycle scope and inventory.
2. Verify both independent approval checks before accepting work.
3. Evaluate legal holds and retention protections.
4. Write durable tombstones for eligible deletion targets.
5. Remove eligible blob objects and index entries using replay-safe operations.
6. Record completion receipts and protected retained-record exceptions.
7. Verify inventory outcomes and retain manifest/receipt evidence.
8. Publish `TenantDeletionVerified` only for the verified lifecycle outcome; its consumer closes the purge record.
9. Do not portray HTTP `202` acceptance or an incomplete cross-store purge as verified completion.

**Sources:** S, pp. 78–80, Chapter 22; p. 87, C.1; p. 89, `TST-013`.  
**Needs confirmation — DAT-OQ-018:** Scope, approval proof, physical inventory, held-data completion semantics, backup handling, and partial-failure recovery. The confirmed procedure does not authorize force deletion.

### Personal Data, Secrets, and Untrusted Content

| Requirement ID | Status | Data handling requirement | Source |
|---|---|---|---|
| DAT-PRV-001 | Confirmed | Extraction tags likely personal data. Gateway redacts nonessential fields before provider invocation where policy permits. | S, p. 62, §17.2.2 |
| DAT-PRV-002 | Confirmed | Log token counts and digests, not entire prompts by default. Diagnostic traces never contain user documents or API secrets. | S, pp. 62, 64 |
| DAT-PRV-003 | Confirmed | Public fields/errors exclude secrets, raw provider credentials, full prompts, retrieved documents in errors, and unauthorized resource existence. | S, pp. 54–56, 84 |
| DAT-PRV-004 | Confirmed | Providers receive scoped context and structured prompts, not connector tokens or unrestricted database access. Model/tool calls receive no secrets outside declared scope. | S, pp. 15, 61 |
| DAT-PRV-005 | Confirmed | Evidence and provider output are untrusted data. They cannot authorize tools, change tenant scope, alter approvals, or override deterministic policy. Strip tool-call directives from evidence contexts and record injection indicators. | S, pp. 7, 38–39, 61 |
| DAT-PRV-006 | Confirmed | Browser local storage must not contain long-lived refresh tokens. A BFF cookie arrangement is optional, not selected. | S, p. 21, §5.1.2 |
| DAT-PRV-007 | Confirmed | Staging uses synthetic data/test connectors; production data is forbidden in development. | S, p. 19, §4.3.1 |
| DAT-PRV-008 | Needs confirmation | PII tag schema, detection confidence, redaction policy/versions, personal data in reasons/annotations/identity metadata, and subject-inventory matching. | S, pp. 62, 80; **DAT-OQ-004**, **DAT-OQ-016**, **DAT-OQ-018** |

### Migration, Recovery, and Sizing

**DAT-MIG-001 — Confirmed:** Expand-and-contract migrations add nullable columns first, backfill in bounded batches, and enforce constraints afterward. No required field is removed while active readers depend on it. CI prevents incompatible field deletion or enum changes.  
**Source:** S, p. 52, §14.2.2; p. 55, §15.3.1.

**DAT-MIG-002 — Confirmed:** Predeploy migrations remain backward compatible; enforcement follows old-replica drain. Rollback documentation states whether new writes remain readable. Regression rolls back traffic, not an automatic database down-migration.  
**Source:** S, pp. 72–73, §§20.2–20.3.

**DAT-REC-001 — Confirmed:** Primary-region writes and warm-region restoration are the R1 profile. Recovery exercises verify relational/object consistency and index rebuild recipes. Reference continuous-backup targets are RPO `<=15 minutes` and RTO `<=4 hours`.  
**Source:** S, p. 19, §4.2.2; p. 69, §19.3.1.

**DAT-REC-002 — Confirmed:** During delayed indexing, contain only the affected connector/indexer shard, retain accepted source records, replay validated bounded outbox work, compare fingerprints/indexed versions, and execute denied-access probes before closing recovery.  
**Source:** S, p. 90, Appendix F.1.

**DAT-REC-003 — Confirmed:** Suspected ACL leakage suspends affected aliases, revokes cached evidence, preserves audit traces, and replays scoped ACL revisions. Search resumes only after negative access tests pass.  
**Source:** S, p. 79, §22.2.2.

| Sizing ID | Confirmed reference assumption | Implementation significance |
|---|---|---|
| DAT-SIZE-001 | `100,000` indexed documents per tenant maximum in the reference workload | Capacity baseline, not an invented universal API validation constraint |
| DAT-SIZE-002 | `20` concurrent AI runs per large tenant in the reference workload | Large-tenant load assumption, not every workspace’s selected quota |
| DAT-SIZE-003 | Typical `1 MB` source yields approximately `40–120` chunks | Sizing estimate, not a chunk-count invariant or minimum |
| DAT-SIZE-004 | Raw files, normalized text, chunk vectors, replication overhead tracked separately | Preserve distinct storage-cost categories |
| DAT-SIZE-005 | `2,000` active daily users; `60` requests/second steady; `180` burst | Reference verification load; no physical partition/index choice implied |

**Source:** S, p. 68, §§19.1.1–19.1.2.  
**Needs confirmation — DAT-OQ-020:** Backup retention, restoration inventory consistency rules, bounded batch sizes, readiness/recall/coverage thresholds, and recovery record schemas.

## Integration Data and Acceptance Criteria

### Input and Output File/Data Contracts

| Integration ID | Direction / data | Confirmed format and contents | Validation / encoding / time requirements | Needs confirmation | Source |
|---|---|---|---|---|---|
| DAT-INT-001 | Input: attachment source file | PDF, DOCX, HTML, UTF-8 text | MIME signature and extension agree; configurable `25 MB` per-file cap; scan before parse; no macros/embedded remote fetch | Multipart/body shape, exact MIME values, filename/count rules, MB conversion, archive threshold, subtype versions | S, p. 30, §8.1 |
| DAT-INT-002 | Input: connector repository data | Stable source identity, permissions, change history; advertised list/fetch/delta/ACL/delete capability | Scoped secret references; durable cursor/outcome; revoked credentials fail `CONNECTOR_REAUTH_REQUIRED` | Provider formats/encoding/cursor values, permission model, version mapping | S, pp. 27–29 |
| DAT-INT-003 | Output: normalized derivatives | Immutable text, layout, metadata; page/block/table/reading-order provenance | Strip transport artifacts without claim rewriting; fingerprint + pipeline version; OCR opt-in/provenance | File extensions, serialization schema, normalized-text encoding, parser/pipeline format | S, pp. 30–32 |
| DAT-INT-004 | Output/input: search derivative | Tenant/workspace/version/chunk/language/classification, embedding, normalized searchable text | `1536` dimensions; authoritative source/ACL validation | Provider wire format, vector precision, analyzers, row key, complete schema | S, pp. 34–36 |
| DAT-INT-005 | Output: evidence/citation | Chunk ID, source title, immutable document revision, page anchor, ACL digest | Current permission and stored-anchor resolution before display; opaque citations | JSON `Citation` shape, nonpaginated anchors, bbox units, response encoding | S, pp. 31, 35, 57, 87 |
| DAT-INT-006 | Provider input/output: generation | Scoped prompt composition; provider output conforms to versioned JSON schema | Validate unknown fields/citations/control injection; bounded retries; privacy and classification controls | Provider adapter schema/encoding, schema version, attempt identity, content size | S, pp. 37–39 |
| DAT-INT-007 | Internal event / job | Required event envelope and canonical JSON; immutable signed tenant context | UTC; event ID/revision deduplication; separate mutation actor/correlation evidence | Canonicalization/signatures, all payload types, character encoding, size, retention | S, pp. 22, 48–50 |
| DAT-INT-008 | REST / internal RPC | External OpenAPI; internal protobuf IDL and versioned HTTP/gRPC | Public timestamps RFC 3339; validation before transaction/domain/tool boundaries | IDL versions, JSON numeric mapping, success media types, encodings | S, pp. 54–56, 82 |
| DAT-INT-009 | SSE progress | Monotonically increasing offsets; `Last-Event-ID`; retained scoped backfill | Reconstruct persisted server state; no private backfill outside caller scope | Payload/event names, offset type, retention/expiry, heartbeat and encoding | S, p. 55, §15.2.1 |
| DAT-INT-010 | Optional outbound webhook | Signed event delivery; recipient age/signature verification | Exponential retry; failure never reverses internal transaction | Method/recipient format, payload/canonical bytes, signature/age limits, delivery ledger | S, p. 55, §15.2.2 |
| DAT-INT-011 | Output: source object delivery | Authorized immutable cited object; opaque public name; short-lived signed URL | Encryption at rest/current access | Binary-versus-URL API contract, MIME/encoding, URL lifetime and recovery | S, p. 52, §14.3.1; p. 57 |
| DAT-INT-012 | Output: export package | Case metadata, approved artifacts, source references, audit manifests and checksums | Two independent checks; exclude secrets/internal prompts | Archive/file names, format/encoding, manifest schema/checksum algorithms, download expiry | S, pp. 78–80 |
| DAT-INT-013 | Output: audit archive / purge receipt | Append-only batch-hash audit archive; completion and legal-hold exceptions | Independently controlled retention; safe UTC evidence | Archive format, receipt schema/signature, algorithm/encoding, retention details | S, pp. 62, 66, 80 |
| DAT-INT-014 | Input/output: evaluation corpus and results | Frozen versioned synthetic cases; expected citation sets/decisions; actual scorecard; signed manifest/outputs | Independent leakage review; randomized seed; release digest linkage | Corpus/result file schema/encoding/names, statistical formats, signature verification | S, pp. 74–76, 88–89 |
| DAT-INT-015 | Input/output: release/configuration/contracts | Signed images/configuration, SBOM, schemas/prompts/routing policy, migrations | Allowed build identity; reconstruct versions; vault references only for secrets | Artifact names, digest/signature formats, manifest schemas, repository layout | S, pp. 55, 71–73 |
| DAT-INT-016 | Input: authentication context | OIDC authorization-code/PKCE; issuer/audience/expiry/subject/tenant access-token concepts | Reject unexpected algorithm/missing tenancy; scoped service identity | Exact claim names, identity mapping, token/session representation and retention | S, pp. 21–23 |

**DAT-FMT-001 — Confirmed:** UTF-8 is explicitly required for the supported plain-text upload category. This does not establish the encoding of every normalized file, archive, CSV, webhook, or provider payload. Unspecified encodings remain **Needs confirmation**.

**DAT-FMT-002 — Needs confirmation:** Unicode normalization, database collation, BOM handling, HTML charset behavior, document subtype versions, file compression, delimiter/line-ending formats, and numeric localization in exchanged files. No CSV or spreadsheet export is confirmed.

### Dates, Times, and Ordering

| Requirement ID | Status | Requirement | Source / unresolved detail |
|---|---|---|---|
| DAT-TIME-001 | Confirmed | Server durable time is UTC; public timestamps use RFC 3339. | S, pp. 54, 59 |
| DAT-TIME-002 | Confirmed | UI presents workspace-local times with timezone labels. Locale selection does not alter event ordering or durable API representations. | S, p. 59, §16.3.2 |
| DAT-TIME-003 | Confirmed | Contractual deadlines use workspace timezone and business calendars; predictions cannot alter them. | S, p. 25, §6.3.1 |
| DAT-TIME-004 | Needs confirmation | Timestamp fractional precision, timezone identifiers/default, daylight-saving/calendar rules, leap handling, clock skew, TTL start points, and provider timestamp conversion. | **DAT-OQ-005**, **DAT-OQ-006**, **DAT-OQ-014**, **DAT-OQ-020** |
| DAT-TIME-005 | Confirmed | Aggregate revision and event identity govern replay safety; cross-partition queue order is not a business guarantee. | S, p. 48, §13.1.2 |
| DAT-TIME-006 | Needs confirmation | Ordering within public lists/audit cursors and tie-breakers for equal timestamps/UUID locality. | **DAT-OQ-003**, **DAT-OQ-014**, **DAT-OQ-021** |

### Tool and Agent Exchange Data

#### MCP `knowledge.search@v1`

| Direction / exact field | Source type | Meaning and confirmed constraint | Requiredness/default gaps |
|---|---|---|---|
| Input `query` | `string` | Permitted-document retrieval query | Optional/nullable treatment and length/default Needs confirmation |
| Input `case_id` | `uuid` | Authorized case context | Optionality and default Needs confirmation |
| Input `max_items` | `int<=10` | Tool maximum items; upper bound `10` | Lower bound/default/optional treatment not supplied |
| Output `evidence_set_id` | `uuid` | Evidence-set identity | Mapping to DAT-010 and API-021 route identity unresolved |
| Output `citations` | `Citation[]` | Verified permitted citations | Full element schema and empty/unsupported shape unresolved |

**Confirmed:** `read:permitted_documents`, tenant-scoped, read-only; no arbitrary URLs or filesystem access.  
**Source:** S, p. 87, C.2.  
**Earlier mapping:** API-046.  
**Needs confirmation:** **DAT-OQ-009**, **DAT-OQ-022**. These fields are not automatically API-010 public search properties.

#### A2A Task Envelope

| Exact source field / concept | Meaning | Type / required status |
|---|---|---|
| `task_id` | Handoff identity | Task ID required concept; UUID example; exact schema unresolved |
| `tenant_id` | Immutable task tenant | Required tenant; example placeholder does not change logical tenancy type |
| `capability` | Versioned capability | Required concept; example `research.grounded_search.v1` |
| `input_schema` | Declared input schema | Required concept; example `schema://oriondesk/research-request/1` |
| Declared output schema | Required handoff output contract | Required by §11.2.2, but property name absent from C.2 example |
| `deadline_at` | Task deadline | RFC 3339 example `2026-11-09T08:00:00Z`; expiry/decline representation unresolved |
| `trace_id` | Trace correlation | Required trace concept; exact type unresolved |
| `authorization_ref` | Independent invocation grant/reference | Present in example; verification/requiredness unresolved |
| `payload` | Declared input data | Example contains `case_id` and `query`; referenced input schema governs full structure |

**Source:** S, p. 41, §11.2.2; p. 87, C.2.  
**Earlier mapping:** API-047.  
**Needs confirmation — DAT-OQ-022:** Transport/schema registry, exact ID types, output-schema property, grant verification, completion/decline schema, and correlation/actor placement.

### DAT-EVT-001 — Source Event Data Lineage

Payload descriptions are semantic source keys, not approved JSON property names.

| Exact event | Confirmed producer / payload concepts | Required data effect | Source |
|---|---|---|---|
| `CaseCreated` | Case Service; Case ID/revision | Classifier input; case identity/revision lineage | S, p. 87, C.1 |
| `DocumentNormalized` | Ingestion; Version ID/source hash | Build derivative index | S, p. 87, C.1 |
| `SearchIndexCommitted` | Indexer; index generation/document revision | Invalidate query cache | S, p. 87, C.1 |
| `AgentPlanApproved` | Orchestrator; Run ID/plan hash | Dispatch durable plan steps | S, p. 87, C.1 |
| `ApprovalDecisionRecorded` | Policy Service; task/actor/content hash | Validate exact publication gate | S, p. 87, C.1 |
| `WorkflowStageAdvanced` | Orchestrator; run/stage/checkpoint | Resume durable consumers | S, p. 87, C.1 |
| `AccessDenied` | Policy Service; principal/action/policy digest | Safe denial audit and alert enrichment | S, p. 87, C.1 |
| `TenantDeletionVerified` | Retention Worker; manifest ID/receipt hash | Close verified purge record | S, p. 87, C.1 |
| `BaselineCommitted`, `RunRequested`, `DeploymentPromoted`, `CaseStateChanged`, `ConnectorSyncStarted`, `ModelInvocationCompleted`, `DataRetentionPurgeCommitted`, `ApiCompatibilityVerified`, `UserReviewOpened`, `SecurityPolicyChanged`, `SloBurnRateDetected`, `BackpressureActivated`, `ReleasePromoted`, `EvaluationCompleted` | Event names Confirmed in their chapter registers; complete producer/payload schemas not specified | Preserve correlated accepted-operation/version evidence; do not infer GET mutation or browser payload | S, Chapters 1, 3–7, 10, 14–22, component registers |

**Needs confirmation — DAT-OQ-012:** Full typed payload schemas, aggregate mappings, producer identities not named in C.1, and projections for SSE/webhooks. Preserve all source names without inventing `EVT` identifiers.

### Source-Supported Validation Conditions

| Validation ID | Data condition | Confirmed validation result | Open boundary |
|---|---|---|---|
| DAT-VAL-001 | Tenant/workspace/resource identity | Enforce same-tenant membership and resource authorization before protected access/mutation | Complete FK/claim schemas |
| DAT-VAL-002 | Case status/revision | Case status CHECK plus allowed edges; current revision required | Missing header syntax/errors and edge-specific guards |
| DAT-VAL-003 | Attachment file | Type/MIME agreement, configured cap, decompression safety, scanning before parse | MB conversion, MIME/subtype catalog, archive threshold |
| DAT-VAL-004 | Normalized evidence | Claims unchanged; source URI/hash/page/optional bbox preserved; resolvable anchors | Geometry/nonpaginated-anchor schema |
| DAT-VAL-005 | Low extraction quality | Safe document viewable; excluded from autonomous recommendations | Metric formulas/thresholds |
| DAT-VAL-006 | Retrieval | ACL before text release; bounded candidates/diversity/token budget; insufficient support returns `NO_SUPPORTED_EVIDENCE` | Public body/result schema, selected token limit |
| DAT-VAL-007 | Model output | Versioned schema; unknown fields, invalid citations, control-character injection produce `MODEL_OUTPUT_INVALID`; no publish | Exact output schema and retry count |
| DAT-VAL-008 | Plan | Acyclic, depth `8`, tool invocations `16`, stored revision/checkpoint before side effects | Count conventions and timeout/review-wait semantics |
| DAT-VAL-009 | Review | Eligible actor, exact artifact hash, separation of duties, required form completeness | Decision literals, rationale rules, task guards |
| DAT-VAL-010 | Mixed material class | Maximum class governs all four DAT-CLS-001 controls | Per-class provenance/mapping |
| DAT-VAL-011 | Event/replay | Original identity, operation deduplication, stale revision, guarded replay | Canonical bytes, namespace/TTL |
| DAT-VAL-012 | Export/purge | Independent approvals, hold/retention protection, inventory/checksum/receipt verification | Scope and manifest/partial-failure schemas |
| DAT-VAL-013 | Evaluation/release | Frozen signed fixture/version integrity; actual metrics/confidence; zero critical exceptions | Statistical schema/signature format |
| DAT-VAL-014 | Contract evolution | No incompatible deletion/enum mutation while readers rely on fields | Repository IDL and compatibility tooling |

**Sources:** S, pp. 21–56, 62, 74–80, 85–90. Detailed source locations are retained in the corresponding field and lifecycle requirements.

### Acceptance Criteria

All identities, cases, files, and provider replies used in verification are synthetic. Include successful, empty, mixed-permission, mixed-classification, adversarial, malformed, duplicate, and delayed inputs. Randomized tests record their seed. Critical isolation and approval tests pass with zero exceptions.

**Source:** S, p. 74, Chapter 21 invariant; p. 89, E.1–E.2.

| Acceptance ID | Related data / earlier requirements | Procedure | Expected result | Source / dependency |
|---|---|---|---|---|
| DAT-AC-001 | DAT-003-F01–08, DAT-RI-001–003 | Verify source case DDL fields/defaults/constraints and use pooled connections across two tenants | Exact case types/constraints retained; scoped context reset; no cross-tenant row exposure | S, pp. 85–86; `API-AC-039` |
| DAT-AC-002 | DAT-REL-001–002, DAT-RI-002 | Attempt case write using a workspace belonging to another tenant | Rejected without business-state change; same-tenant enforcement effective | S, p. 86; physical mechanism blocked by DAT-OQ-003 |
| DAT-AC-003 | DAT-003-F09–17 | Read/write an approved case schema covering title, description, impact, urgency, priority, owner, approved-result context | Domain-supported fields not lost because abbreviated DDL omits them; no model-only priority/deadline mutation | S, pp. 24–25; schema blocked by DAT-OQ-005 |
| DAT-AC-004 | DAT-CNC-003–004, DAT-044 | Submit identical case creation twice under one key; then reuse with changed body | One case/identical outcome; changed body `409 IDEMPOTENCY_CONFLICT` | S, p. 89, `TST-001–002`; `API-AC-002–003` |
| DAT-AC-005 | DAT-RI-009 | Read valid case ID using foreign tenant and compare absent ID | Same `404`-equivalent non-disclosing class; safe denial actor/resource-class evidence | S, pp. 23, 89 `TST-003` |
| DAT-AC-006 | DAT-STATE-001, DAT-004 | Execute each of six confirmed edges with current revision and approved guard fixtures | Target state/monotonic revision accepted; append-only history and one accepted transition evidence | S, pp. 25–26; `API-AC-005`; detailed guards DAT-OQ-005 |
| DAT-AC-007 | DAT-CNC-001, DAT-HIS-001 | Submit stale PATCH and unsupported/unauthorized normal transition | Stale `409 CASE_VERSION_CONFLICT` with current revision; no denied business mutation or silent overwrite | S, pp. 25, 84; `API-AC-006–007` |
| DAT-AC-008 | DAT-026, DAT-STATE-001 | Close through the to-be-confirmed edge; reopen through explicit approved new-revision operation | Snapshot retains approved answer/version/decisions; old lineage unchanged; no ordinary in-place `CLOSED` exit | S, pp. 25–26; blocked by DAT-OQ-005 |
| DAT-AC-009 | DAT-024 | Correct asynchronous classification label | Correction reason code recorded with supported confidence/provenance information | S, p. 12; schema/catalog DAT-OQ-005 |
| DAT-AC-010 | DAT-023, DAT-029, DAT-FILE-001 | Upload supported safe file meeting configured MIME/size/archive rules | Durable `202` ingestion; scan before parse; no macro/remote embedded fetch; acceptance not readiness | S, pp. 30–32, 83 |
| DAT-AC-011 | DAT-VAL-003, DAT-029-F06 | Upload polyglot/unsafe/oversized/decompression-unsafe fixture | Fail closed; unsafe payload quarantined and not indexed; safe remediation evidence only | S, pp. 30, 88 `T-04`, 89 `TST-015`; boundary DAT-OQ-007 |
| DAT-AC-012 | DAT-006–007, DAT-030 | Normalize source twice using same approved pipeline; reprocess side-by-side with changed version | Claims/provenance preserved; immutable derivatives distinguished using fingerprint/pipeline version; no old anchor overwrite | S, p. 31; derivation blocked by DAT-OQ-008 |
| DAT-AC-013 | DAT-007, DAT-010, DAT-035 | Reviewer activates verified permitted citation | Required evidence semantic fields resolve cited immutable version and anchor; highlighted page range available | S, pp. 31, 35, 57–58; `API-AC-012` |
| DAT-AC-014 | DAT-029-F02–05 | Process safe low-quality source fixture | Quality flags retained; document remains viewable, excluded from autonomous recommendations | S, p. 32; formulas/thresholds DAT-OQ-007 |
| DAT-AC-015 | DAT-031, DAT-032 | Rebuild index in parallel and validate generation completeness/recall before switch | Search rows retain required scope/version/class/vector/text; alias switches atomically only after checks | S, p. 34; provider/thresholds DAT-OQ-009 |
| DAT-AC-016 | DAT-022, DAT-034, DAT-RI-006 | Revoke source access after indexing/cache fill; issue next query | No forbidden evidence; affected cache purged before release, regardless of normal TTL | S, pp. 28, 53, 89 `TST-004` |
| DAT-AC-017 | DAT-010, DAT-VAL-006 | Query insufficient confidence/quality/evidence | `NO_SUPPORTED_EVIDENCE`, not fabricated context; only supported clarification/human path | S, p. 36 |
| DAT-AC-018 | DAT-008–009, DAT-040, DAT-046 | Start run, verify plan/checkpoint persistence, refresh browser, reconnect SSE | Immediate durable run; plan before side effects; stage before dispatch; server progress reconstructed/scoped backfill | S, pp. 40, 49, 55, 58 |
| DAT-AC-019 | DAT-038, DAT-VAL-007–008 | Force invalid model fields/citations/control injection and recursive plan hints | `MODEL_OUTPUT_INVALID` where applicable; no publish; depth/call bounds honored; exact safe failed checkpoint | S, pp. 38, 40–42, 88 `T-10`, 89 `TST-005` |
| DAT-AC-020 | DAT-011–012, DAT-CNC-007 | Change artifact after review; submit prior/wrong hash | Stale rejection audited; old approval cannot publish new content; immutable prior decision/history preserved | S, p. 45; p. 89 `TST-006` |
| DAT-AC-021 | DAT-011-F06–07, DAT-STATE-004 | Attempt own high-risk approval and expire review under configured SLA | Self-approval blocked; expiry creates reassignment/escalation, never implicit approval | S, pp. 11, 45, 89 `TST-010` |
| DAT-AC-022 | DAT-TXN-002, DAT-043 | Inject failure between satisfied gate and final pointer update | No partially committed publication; exact gate/pointer commit together | S, p. 45, §12.3.1 |
| **DAT-AC-023** | **DAT-CLS-001; DAT-003-F06; DAT-031-F06; DAT-017; `API-AC-034`** | **Run an authorized `INTERNAL` case with permitted anchored quality-appropriate `RESTRICTED` evidence; inspect controlled internal policy/provenance records for routing, redaction, retention, and approval; attempt publication without required human decision** | **All four controls use applicable `RESTRICTED` policy despite lower case label and passed ACL. Reference human review remains required; `auto_publish_classification: INTERNAL` cannot bypass it. No invented public classification field required for verification.** | **S, p. 62, §17.2.1; p. 90; detailed mappings DAT-OQ-016** |
| DAT-AC-024 | DAT-015, DAT-028 | Fail/retry partial sync with a poison record | Cursor only advances past durable outcomes; high-watermark/error ledger retained; quarantine exception recorded; remaining batch may proceed | S, pp. 28–29 |
| DAT-AC-025 | DAT-027 | Revoke credentials before queued sync; use unsupported capability | `CONNECTOR_REAUTH_REQUIRED` without token disclosure; explicit lower-trust warning, no silent support assumption | S, p. 27 |
| DAT-AC-026 | DAT-014, DAT-045, DAT-CNC-005 | Replay event `100` times; add delayed/stale delivery | Exactly one accepted business transition; duplicates recorded; no cross-partition-order dependency | S, p. 88 `T-07`; p. 89 `TST-007` |
| DAT-AC-027 | DAT-047–048, DAT-HIS-005 | Replay without reason/dry-run/scope; then valid scoped replay and approved schema transform | Unguarded replay rejected; original identity preserved except explicit provenance-linked transformation | S, p. 50 |
| DAT-AC-028 | DAT-PRV-001–007, DAT-054 | Inspect provider requests, public fields/errors, telemetry, audit projections, and environments | Scoped/redacted provider context; no secrets/documents in diagnostics/errors; Auditor redacted scope; no production data in development | S, pp. 19, 54–56, 62–64, 84 |
| DAT-AC-029 | DAT-013, DAT-HIS-003 | Attempt historical audit/decision modification; verify archive chain using approved format | Modification rejected; append-only hash-chain archive remains verifiable | S, p. 62; p. 88 `T-09`; chain schema DAT-OQ-014 |
| DAT-AC-030 | DAT-RET-001–006 | Evaluate configured diagnostics/audit retention and run classification selection | Distinct 30-day diagnostic/default and seven-year fictional audit policy retained; class selection/holds honored; no fabricated RESTRICTED duration or universal TTL | S, pp. 62, 66, 90 |
| DAT-AC-031 | DAT-059, DAT-RET-008 | Single Admin attempts export; then independently authorized export | Single Admin rejected; package inventory/checksums valid; no secrets/internal prompts | S, pp. 78–79, 88 `T-11` |
| DAT-AC-032 | DAT-018, DAT-053, DAT-RET-009–010 | Purge held inventory and simulate partial object/index failure | Held objects retained/receipted; no false verified completion; same inventory available for subject-access handling | S, p. 80; p. 89 `TST-013`; partial semantics DAT-OQ-018 |
| DAT-AC-033 | DAT-057 | Evaluate signed frozen reference corpus and replace expected fixture manifest | `1,200` reference synthetic cases preserve expected citations/decisions; poisoned fixture control fails; actual metrics/confidence reported; safety/low confidence blocks release | S, pp. 75–76, 88 `T-12`, 89 |
| DAT-AC-034 | DAT-MIG-001–002, DAT-056 | Add/backfill/enforce compatible field; attempt required-field deletion with active reader; simulate canary regression | Expand-and-contract behavior; incompatible deletion rejected; new-write readability documented; traffic rollback, not automatic down-migration | S, pp. 52, 55, 72–73 |
| DAT-AC-035 | DAT-REC-001–003 | Restore reference region profile and recover delayed indexing/ACL leak | Relational/object/version consistency; RPO/RTO targets met; fingerprints and denied-access probes before resume | S, pp. 19, 69, 79, 90; `TST-012` |
| DAT-AC-036 | DAT-058, DAT-002 | Replay provisioning/backfill and attempt sync during incomplete state | One idempotent onboarding outcome; policy/key/role/quota/stubs represented; incomplete sync blocked; readiness by index coverage | S, p. 78 |
| DAT-AC-037 | DAT-041–042, DAT-INT tool contracts | Attempt arbitrary discovered capability without independent grant | `DENY` before dispatch; no arbitrary URL/filesystem/tool authorization from metadata | S, p. 87; p. 89 `TST-014` |
| DAT-AC-038 | DAT-050, DAT-TXN-001 | Fail webhook recipient after committed case mutation | Business state remains committed; signed age-verifiable delivery follows defined retries | S, p. 55 |
| DAT-AC-039 | DAT-060, DAT-056–057 | Inspect accepted revised invariant and release evidence | At least one negative-test link; reconstruct image/schema/prompt/routing/config versions; signed outputs referenced by release digest | S, pp. 8, 73, 89 |
| DAT-AC-040 | DAT-TIME-001–003 | Compare durable timestamps/event order across workspace locale/timezone presentation | RFC 3339/UTC durable representation unchanged; local display labels timezone; deadlines follow calendar, not prediction | S, pp. 25, 54, 59 |

**DAT-FILE-001 — Confirmed:** The attachment format, scanning, MIME agreement, `25 MB` configurable cap, and decompression-safety requirements used in DAT-AC-010–011 are those in DAT-INT-001 and DAT-VAL-003. Exact byte and archive thresholds remain **DAT-OQ-007**.

**Acceptance blocking rule:** Where an executable fixture depends on an unresolved schema, threshold, state guard, or algorithm, retain the acceptance obligation and identify the blocking question. Do not make the test executable by inventing a contract.

## Consistency and Open Questions

### Field Mapping and Consistency Findings

Earlier specifications are not rewritten here. Required amendments are identified for later controlled updates.

| Consistency ID | Source issue / evidence | Affected identifiers and earlier mapping | Required clarification or amendment |
|---|---|---|---|
| DAT-CNS-001 | Appendix B.2 is abbreviated and omits domain fields required by §6.1.2. S, pp. 24, 85–86. | DAT-003-F09–17; `SCR-002-F03–19`; API-001–003; `SF-CON-006`, `API-CNS-005` | Preserve title, description, priority, owner, approved result and business input/deadline concepts. Complete physical schema; do not exclude omitted data. |
| DAT-CNS-002 | Source uses `Case`, `CaseAggregate`, `CaseRow`; `OutboxRecord`, `OutboxTable`; `ReviewDecision`, `approval_decisions`; `SourceDocument`, `documents`, and other related names without complete mappings. | DAT-INV-001; DAT-003, DAT-005, DAT-012, DAT-014, DAT-018 | Confirm aliases/projections versus distinct records. No duplicate/merged tables inferred. |
| DAT-CNS-003 | Register tables label `Case`/`CaseAggregate` immutable while case current state is mutable; similar generic “immutable derivative” labels appear on jobs, aliases, metrics, deployment records. S, component registers; §§6.1–6.2. | DAT-INV-002; DAT-HIS-001; DAT-063 | Separate immutable provenance/revision evidence from mutable current projections. Preserve SHA-256 register assertions without inventing column mapping or prohibiting supported mutation. |
| DAT-CNS-004 | Selected lists omit `tenant_id` on many tables; Chapter 5 requires it on every tenant-owned row. S, pp. 22, 85. | DAT-COM-F02; DAT-RI-001; API-AUTH-003 | Production design must add required tenant context where applicable. Determine which registry/deployment records are global versus tenant-owned without removing isolation obligations. |
| DAT-CNS-005 | `cases` has global UUID PK plus `UNIQUE (tenant_id,id)`; tenant slug has explicit `unique(slug)`; general rule says tenant/business-key-scoped uniqueness. S, pp. 51, 85–86. | DAT-001-F02, DAT-003-F01–03, DAT-COM-F08 | Preserve explicit PK/slug constraints and tenant-scoped business uniqueness. No undocumented source-ID or revision unique index inferred. |
| DAT-CNS-006 | Case workspace FK alone does not enforce same tenant; source explicitly requires additional production enforcement. S, p. 86. | DAT-REL-001, DAT-RI-002; API-AUTH-003 | Confirm composite-FK or controlled-procedure implementation; do not rely on isolated IDs/RLS alone. |
| DAT-CNS-007 | Human reference `OD-2026-1042` differs from UUIDv7 technical identity. S, p. 7, Reference UI A; p. 51. | DAT-003-F18; `SCR-001-F01`, `SCR-002-F01`; `SF-CON-002`, `API-CNS-006` | Define separate reference generation/uniqueness only if required. Never use fixture reference as API `caseId`. |
| DAT-CNS-008 | `document_versions` B.1 omits local version identity; other records refer to `document_version_id`. Fingerprint+pipeline derivative identity coexists with UUIDv7 policy. S, pp. 31, 51, 85. | DAT-006-F01/F06; DAT-007-F02; `SCR-003-F04`; API-004/021/035 | Define version key/derivation and `parser_version` versus pipeline version. No invented `document_versions.id`, hash encoding, or identity equivalence. |
| DAT-CNS-009 | B.1 evidence sets carry `run_id`; public search and MCP identify evidence sets with different contexts; `evidenceId` mapping unresolved. S, pp. 35, 83, 85, 87. | DAT-010-F01–02; API-010/021/046; `API-CNS-009`, `API-OQ-008` | Define runless search persistence/nullability and route/resource identity. Keep MCP/public payloads separate. |
| DAT-CNS-010 | `case_revisions.actor/at`, `deletion_receipts.actor/purge_time`, and shared `actor_id/occurred_at` differ. Review also uses `reviewer_id`. S, pp. 25, 45, 85. | DAT-COM-F04–05; DAT-004; DAT-012; DAT-018; API-EVT-001 | Confirm actor/time mapping while preserving exact source column names and trustworthy history. |
| DAT-CNS-011 | `policy_version`, `rule_version`, aggregate revision, run revision, and `plan_revision` are distinct names with incomplete version relationships. Input catalog has `input_digest`, but §12.1.1 requires storing all normalized inputs. S, pp. 24, 40, 44, 48, 85. | DAT-002-F03/F10; DAT-008-F04; DAT-017-F02–10 | Store reproducible inputs plus rule-set version; digest-only implementation insufficient. Resolve version activation and lookup without collapsing versions. |
| DAT-CNS-012 | Artifact hash is semantically mandatory, but algorithm/canonical content boundary is not specified. Register SHA-256 provenance cannot automatically define every artifact/ACL/policy hash. S, pp. 31, 35, 45, 62, registers. | DAT-COM-F07; DAT-039-F02; DAT-011-F04; API-CNC-003 | Define hash scope/algorithm/encoding and immutable target. Do not independently select a hash serialization. |
| DAT-CNS-013 | Six normal case edges confirmed; closing origin/reopening target missing. S, pp. 25–26. | DAT-STATE-001; `SCR-002-T01–T08`; `SF-CON-003`, `API-CNS-001` | Complete only missing edges/guards. No inferred `RESOLVED → CLOSED`, ordinary `CLOSED` exit, or automatic Reject transition. |
| DAT-CNS-014 | Review wait, missing-approval stop, recoverable timeout and `FAILED` enum coexist. S, pp. 12, 41, 45, 49, 82, 90. | DAT-STATE-002; DAT-008-F05; `SF-CON-004`, `API-CNS-003` | Define waiting versus terminal failure and runtime/review SLA; no new timeout state. |
| DAT-CNS-015 | Maximum material class affects four controls; earlier screen field summary did not list all four. S, p. 62. | DAT-CLS-001, DAT-AC-023; `SCR-002-F10`; `API-CNS-013`, `API-CLS-001` | Required earlier amendment remains: explicitly connect maximum material class to routing, log redaction, retention, approval. No extra policy input or automatic case relabeling. |
| DAT-CNS-016 | Tenant lifecycle language and workspace route scope differ; `Admin + approver` and two independent checks coexist. Closed-case retention restriction is separate from decommission workflow. S, pp. 26, 78–83. | DAT-REL-016; DAT-RET-001/008/009; API-014–015; `SF-CON-010`, `API-CNS-008` | Define scope, independent approvals, and retention/hold precedence for nonclosed decommission inventory. No single-actor or hold bypass. |
| DAT-CNS-017 | Source `updated_at DEFAULT now()` initializes value but defines no update trigger. Case business `NEW` has no SQL default in DDL. S, pp. 12, 86. | DAT-003-F04/F08; API-001/003 | Confirm update-time behavior and where initial `NEW` is assigned; do not invent SQL defaults/triggers. |
| DAT-CNS-018 | Source A2A example contains placeholder non-UUID strings and omits declared output-schema field. S, pp. 41, 87. | DAT-042; API-047; `API-CNS-010` | Confirm typed IDs/output-schema property without treating placeholders as production types. |
| DAT-CNS-019 | Illustrated workflow labels, evidence coverage `97.6%`, and `Healthy` are not domain enums or benchmark precision. S, pp. 7, 57, 75, 82. | DAT-062-F03; DAT-CODE-001–008; `SF-CON-011`, `API-CNS-016` | Keep aggregate/presentation vocabularies and scorecard metrics separate; define formulas and mappings. |
| DAT-CNS-020 | Generic registers associate components/GETs with events and durable metadata without full data schemas. S, Chapters 3–4, 15–19. | DAT-063; DAT-LIFE-001; `API-CNS-011`, `API-CNS-017` | Do not create operational tables, GET mutations, or new screens merely from component-register presence. |
| DAT-CNS-021 | General “snake-case” error wording differs from uppercase concrete literals. S, pp. 54, 84. | DAT-CODE-009; DAT-061-F02; `SF-CON-005`, `API-CNS-007` | Preserve existing uppercase codes; future naming and undefined code schemas unresolved. |

### Data Open-Decision Register

No decision, owner, deadline, or approval is established here. Each question is also recorded beside affected requirements.

| Question ID | Status | Required decision / missing data contract | Affected data requirements | Earlier specification links |
|---|---|---|---|---|
| DAT-OQ-001 | Needs confirmation | Production physical design: types, lengths/precision, nullability, defaults, PK/FK/unique constraints where absent, indexes, collation, partition implementation, database/search/cache provider details | All non-DDL entities; DAT-SCP-003, DAT-STO-001–004 | [02_api.md, API-OQ-003/007–010/017/021](02_api.md#api-open-decision-register); [01_screen_functions.md, OQ-007/022](01_screen_functions.md#consolidated-open-questions) |
| DAT-OQ-002 | Needs confirmation | Logical-source aliases versus separate records; register immutable/current projection conflict; SHA-256 provenance assignment; whether component records need persistence | DAT-INV-001–002; DAT-003/005/012/014/018/063; DAT-CNS-002–003 | `SF-CON-006`; `API-CNS-005/011/017`; S, component registers and B.1 |
| DAT-OQ-003 | Needs confirmation | Tenant/workspace FK enforcement; global versus tenant-owned registry scope; UUID/BIGINT transport; case PK/business key; revision precondition and transaction mechanism | DAT-RI-001–003/008; DAT-ID-001; DAT-REL-001–003 | API-AUTH-003, API-OQ-003/017; earlier OQ-002/007; S, pp. 22, 51, 86 |
| DAT-OQ-004 | Needs confirmation | Principal/Actor identity mapping; membership schema/uniqueness; roles/scopes; ACL granularity/revision; workspace setting revision/policy mapping; timezone/model/tool/reviewer/secret settings | DAT-002; DAT-019–022; DAT-CNC-002 | API-OQ-001/014/016; earlier OQ-002/003/020; S, pp. 21–24 |
| DAT-OQ-005 | Needs confirmation | Full case domain schema/field constraints; business reference; owner/priority/deadline/classification catalogs; history identity/patch/initial entry; updated time; closing/reopening schema/guards | DAT-003–004/024–026; DAT-STATE-001 | `SCR-002-F01–19`; API-OQ-003–005; earlier OQ-007–010; S, pp. 12, 24–26 |
| DAT-OQ-006 | Needs confirmation | Source-ID uniqueness; provider/cursor formats; connector and per-run/current cursor history; sync item ledger/retries/trust schema and credential references | DAT-005-F03; DAT-015/027–028 | API-OQ-011; earlier OQ-016/022; S, pp. 27–29 |
| DAT-OQ-007 | Needs confirmation | Upload transport/count/name/MIME/subtype rules/MB conversion/archive threshold; extraction status/quality/OCR/quarantine schema and thresholds; unsafe viewing policy | DAT-023/029/030; DAT-INT-001–003 | API-OQ-007; earlier OQ-015; S, pp. 30–32 |
| DAT-OQ-008 | Needs confirmation | Version identity and fingerprint/pipeline derivation; parser-version mapping; chunk/block/anchor schema, page/bbox conventions and nonpaginated-source anchors; immutable FK/purge behavior | DAT-006–007/030/035; DAT-REL-004–006 | API-OQ-007–008; earlier OQ-015/018; S, pp. 31, 51–52, 85 |
| DAT-OQ-009 | Needs confirmation | Search provider/physical schema/analyzers/vector precision; evidence/citation ID mapping; runless query association; `chunk_refs` integrity; query/token/result schema; cache key/TTL; index/coverage/recall criteria | DAT-010/031–034; DAT-REL-008 | API-OQ-008/023; earlier OQ-017/018/022; S, pp. 34–36, 53, 85, 87 |
| DAT-OQ-010 | Needs confirmation | Object provider/key syntax/object-role vocabulary; public object/source API; signed-URL schema/lifetime/recovery; object/ref mapping and orphan/shared-object handling | DAT-STO-002; DAT-035; DAT-INT-011 | API-OQ-008/019/021; earlier OQ-018/022; S, pp. 51–53 |
| DAT-OQ-011 | Needs confirmation | Run revision/case revision binding; plan/node/step/checkpoint/attempt/artifact schemas; deployment/template/usage references; budget counting; wait/timeout semantics; run-route relationship | DAT-008–009/036–042/046; DAT-STATE-002 | API-OQ-006/009; earlier OQ-011/012/022; S, pp. 12, 15–17, 37–42, 49, 90 |
| DAT-OQ-012 | Needs confirmation | Outbox/event/consumer/dead-letter/HTTP idempotency schemas and namespaces; canonical bytes/signatures; actor/correlation placement; key concurrency/error replay/TTLs; operator replay provenance; SSE retention | DAT-014/044–049; DAT-CNC-003–006 | API-OQ-006/017/019/022; earlier OQ-011/024; S, pp. 17, 25, 48–55 |
| DAT-OQ-013 | Needs confirmation | Artifact content/hash algorithm/canonicalization; task/decision/gate/pointer schemas; decision literals/rationale/annotations; required review fields, assignment/expiry/quorum/override; approved lineage | DAT-011–012/017/039/043; DAT-TXN-002 | API-OQ-010; earlier OQ-012–014; S, pp. 44–46, 58, 85 |
| DAT-OQ-014 | Needs confirmation | Audit detail/redaction/hash-chain/archive schema; action/digest/time/cursor mapping; diagnostic and cost ledgers, metrics, currency/units/daily rollup boundaries; retention/receipt calculations | DAT-013/016/054; DAT-RET-002–003 | API-OQ-012/013/018/021; earlier OQ-019/021/022; S, pp. 62, 64–66 |
| DAT-OQ-015 | Needs confirmation | Key/secret reference format, scope/access, per-tenant isolation versus rotation throughput, rotation/destruction policy and regional storage placement | DAT-052; DAT-RET-011; DAT-STO-005 | API-OQ-021; earlier OQ-022; S, pp. 10, 63, 71–72, 90 |
| **DAT-OQ-016** | **Needs confirmation** | **Material-classification provenance/storage/transport, unknown-class handling, per-class routing/redaction/retention/approval mapping and policy activation. Maximum included-material aggregation across all four controls is already Confirmed.** | **DAT-CLS-001; DAT-051; DAT-017; DAT-AC-023** | **[API-CLS-001](02_api.md#api-cls-001), API-AC-034, API-OQ-026; `SCR-002-F10`, `SCR-007-F09–11`; S, p. 62** |
| DAT-OQ-017 | Needs confirmation | Evaluation job identity/state, dataset/expected-output/result schemas, signed manifest verification, statistics/precision/domain confidence, seed persistence, release output linkage, retention | DAT-057; DAT-INT-014 | API-OQ-013; earlier OQ-021; S, pp. 74–76, 88–89 |
| DAT-OQ-018 | Needs confirmation | Tenant/workspace lifecycle extent; independent approval proof; holds/subject inventory/shared objects; closed-case/decommission precedence; provisioning/backfill/manifest/receipt schemas; partial deletion/backups and retention schedules | DAT-018/026/053/058–059; DAT-RET-001/007–010 | API-OQ-015/016/021; earlier OQ-023/024; S, pp. 26, 78–80 |
| DAT-OQ-019 | Needs confirmation | Design/release/contract records and immutable version relationships; impact scores; requirement/negative-test links; build/config/schema/prompt/policy digests/signatures; migration/sign-off evidence; retention | DAT-056–057/060–061; DAT-MIG-001–002 | API-OQ-020/022; earlier OQ-024; S, pp. 8–10, 55, 71–76, 89 |
| DAT-OQ-020 | Needs confirmation | Capacity/admission/recovery/runtime record schemas; backup retention and consistent restore inventory; bounded windows/batches; index readiness and incident recovery thresholds | DAT-055/058/063; DAT-REC-001–003; DAT-SIZE-001–005 | API-OQ-018/021; earlier OQ-011/016/024; S, pp. 18–20, 68–70, 78–79, 90 |
| DAT-OQ-021 | Needs confirmation | Browser projection versus persistence; view/review/evidence/notification fields; summary formulas/states; cursor/list schema; safe error-details mappings; locale/encoding constraints | DAT-061–062; DAT-CNS-019–021; DAT-TIME-004/006 | API-OQ-003/012/025; earlier OQ-004–006/019/025–027; S, pp. 7, 54–59, 84 |
| DAT-OQ-022 | Needs confirmation | MCP/A2A/webhook data transports/schemas, optionality and lower bounds, output schema/grants, recipient/signature/age/retry ledger and canonicalization | DAT-041–042/050; DAT-INT-009–010; tool exchange tables | API-OQ-023–024; earlier OQ-024; S, pp. 41–42, 55, 87 |

### Dependencies and Required Carry-Forward

| Specification dependency | Required carry-forward |
|---|---|
| [01_screen_functions.md](01_screen_functions.md) | Preserve `SCR-` field/operation/state IDs. Data existence does not confirm an editable control. Required amendments include the four-control classification linkage in `API-CNS-013`/DAT-CNS-015 and resolution of source aliases/business references without altering confirmed screens. |
| [02_api.md](02_api.md) | Preserve all `API-` identifiers, literal methods/paths, confirmed codes, tool fields, and record-versus-public-schema distinctions. Resolve storage/public mappings through controlled amendments; earlier example JSON and SSE payloads remain Proposals. |
| Processing / Workflow Specification | **To be defined in a later stage.** Complete six-edge guards, closing/reopening, classification correction, safe ingestion, budgets/checkpoints, review wait/expiry/override, maximum-class selection, atomic publication, cursor progress, replay/reconciliation, and controlled lifecycle recovery. |
| Exception Handling Specification | **To be defined in a later stage.** Complete missing validation/code/detail schemas, stale/expired states, quarantine, cursor/SSE expiry, dependency ambiguity, lost responses, partial purge/holds, and caller recovery without inventing codes or changing immutable data. |
| Architecture / Security Specifications | **To be defined in a later stage.** Resolve provider/region, key isolation/rotation, identity/protocol boundaries, physical constraints/indexes where absent, signed transport, corporate retention, backup consistency, and service ownership. |
| Stage 8 decision consolidation | `08_architecture_decision.md` is **To be defined in a later stage**. Consolidate only completed Markdown specifications, with links to `03_data.md` and `DAT-OQ-001`–`DAT-OQ-022`, plus affected earlier filenames/IDs. Do not presume decisions, owners, dates, or approvals. |

**Implementation boundary:** Implement and test the confirmed data obligations. Keep unresolved physical design, field mappings, state guards, classifications, hashes, formats, retention, and lifecycle choices as explicit blocking decisions. An omitted catalog field, illustrative value, or repeated Proposal does not authorize an implementation AI to finalize the missing contract.
