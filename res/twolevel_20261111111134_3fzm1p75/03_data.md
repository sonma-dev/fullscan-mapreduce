# 3. Data Specification

## Data Inventory and Relationships

### DAT-001 — Authority, scope and conventions

**Confirmed.** This is `03_data.md`, Stage 3 of 8, for OrionDesk AI, `OD-AI-DDS-001`, `R1.0`, design revision `1.3`. It integrates supplied chapter evidence, not a new inspection of unavailable attachments. The candidate remains provisional pending evidence review. **Confirmed** means supported for the fictional reference system; **Needs confirmation** means an incomplete contract or unresolved decision. No new **Proposal** is selected.

All citations below use **1794353355-OrionDesk_AI_Detailed_Design_Specification.pdf** and original pages. The source states: “All numbers are design assumptions, not measured production performance.” Figures are normative boundary illustrations, not generated implementation artifacts. Logical components, arrows, access scopes and register ownership categories do not independently establish tables, cardinalities or organizational data ownership. [pp.1–2; `data:r2:c1:f1`–`data:r2:c1:f4`, `data:r2:c2:f1`–`data:r2:c2:f3`]

Preserve identifiers in [01_screen_functions.md](01_screen_functions.md) and [02_api.md](02_api.md). `DAT-*` identifiers are specification traceability identifiers, not source namespace mappings. Browser routes and physical-to-wire aliases are not inferred.

The data scope includes enterprise knowledge/cases, grounded evidence, deterministic policy, review/publication, audit and operational evidence. Physical automation, irreversible financial transactions, fine-tuning, unrestricted browsing and agent cloud-administration permissions are **Out of scope**. Application-hosted GPU inference is excluded. Cross-region active/active mutation, OCR beyond English and customer-managed model weights are deferred. [pp.9–10,19; `data:r2:c7:f1`, `data:r2:c8:f6`, `data:r2:c25:f2`]

### DAT-002 — Storage authority and ownership

| Store/responsibility | Confirmed purpose and authority | Implementation qualification |
|---|---|---|
| PostgreSQL | Authoritative mutable metadata; case transactional state | Source-named reference product, not an independently selected new product |
| Private encrypted blob/object storage | Source and normalized artifacts, immutable versions | Provider, literal layout and crypto implementation unresolved |
| Vector/keyword search | Nonauthoritative searchable derivatives | Eventually consistent; cannot confer authorization |
| Cache | Versioned ephemeral results with short TTLs | CacheEntry ledger classification unresolved; no numerical result TTL supplied |
| Case Service | Transactional mutations | Concrete table ownership incomplete |
| Ingestion Service | Document conversion | Parser/catalog ownership details incomplete |
| Retrieval Service | Cited chunks | Search/evidence physical ownership incomplete |
| Orchestrator | Run state, bounded workflow | No direct DB credentials; narrowly scoped APIs |
| Policy Service | Binding approval requirements | Deterministic policy authority, not model decision |
| Engineering domain/platform/AI-platform teams | Case/policy APIs; identity/messaging; model-gateway contracts respectively | Contract ownership, not automatic entity stewardship |

Datastores have no public IP/endpoints. Workload identities are scoped and not shared between deployment units; managed identity replaces static credentials where supported. [pp.9,15–19; `data:r2:c8:f1`–`data:r2:c8:f2`, `data:r2:c18:f5`, `data:r2:c19:f1`, `data:r2:c19:f5`, `data:r2:c24:f1`, `data:r2:c24:f5`]

### DAT-003 — Relational entity and selected-field inventory

The following names and selected fields come from Appendix B. They are **Confirmed selected declarations**, not exhaustive production schemas. Every missing type, length, precision, nullability, required property status, default, PK/FK, uniqueness, index, relationship multiplicity and concrete owner is **Needs confirmation**. Listed column names must not automatically become REST properties. [p.85 B.1; `data:r2:c138:f1`–`data:r2:c138:f19`]

| Source entity | Selected physical names | Purpose/constraint | Screen/API activity mapping |
|---|---|---|---|
| `tenants` | `id`, `slug`, `plan`, `region`, `created_at` | Tenant security scope; `unique(slug)` | Shared authenticated context; API-002/018 |
| `workspaces` | `id`, `tenant_id`, `policy_version`, `quota` | Workspace grouping; RLS tenant scope | SCR-007; API-020/016/017 |
| `cases` | `id`, `tenant_id`, `workspace_id`, `status`, `revision` | Current aggregate; `unique(tenant_id,id)` | SCR-001/002; API-003–005/019/026 |
| `case_revisions` | `case_id`, `revision`, `patch`, `actor`, `at` | Append-only history | SCR-002/008; API-005/013/026 |
| `documents` | `id`, `workspace_id`, `source_id`, `sensitivity` | Source catalog; originating ACL enforced | SCR-003/006; API-006/023/011 |
| `document_versions` | `document_id`, `hash`, `parser_version`, `object_key` | Immutable source-version record | SCR-003; API-021/022/040 |
| `chunks` | `id`, `document_version_id`, `page`, `bbox`, `text_hash` | Source anchor | SCR-003; API-012/021/022 |
| `runs` | `id`, `case_id`, `status`, `plan_revision`, `budget` | Bounded state machine | SCR-004; API-007–009/024/038/042e |
| `run_steps` | `id`, `run_id`, `step_kind`, `status`, `checkpoint` | Idempotent step | SCR-004; API-024/038 |
| `evidence_sets` | `id`, `run_id`, `chunk_refs`, `acl_digest` | Publish validation | SCR-003/005; API-012/021/022/010 |
| `approval_tasks` | `id`, `run_id`, `reviewer_pool`, `artifact_hash` | “no self approval”; breadth unresolved | SCR-005; API-010/025 |
| `approval_decisions` | `id`, `task_id`, `reviewer_id`, `decision`, `reason` | Immutable decisions | SCR-005/008; API-010/013 |
| `audit_events` | `id`, `tenant_id`, `actor_id`, `action`, `digest` | Append only | SCR-008; API-013 |
| `outbox_events` | `event_id`, `tenant_id`, `aggregate_revision`, `payload` | Transactional outbox | API-048/053; no new screen |
| `connector_cursors` | `connector_id`, `cursor`, `watermark`, `retry_state` | Durable checkpoints | SCR-006; API-011/027 |
| `token_ledger` | `run_id`, `deployment_id`, `in_tokens`, `out_tokens` | Attributed cost | Run/usage activities; API-014/037 |
| `policy_evaluations` | `run_id`, `rule_version`, `input_digest`, `result` | Reproducible policy evaluation | SCR-005/007; API-010/025 |
| `deletion_receipts` | `tenant_id`, `object_ref`, `purge_time`, `actor` | Auditable purge | Unmapped exit activity; API-017/041 |

**Relationships.** Workspace groups users, policies, connectors and cases. Attachments and runs are separate entities joined by immutable identifiers; case attachments reference immutable document versions, and approvals reference run artifact hashes. Exact multiplicities and most FK declarations remain **Needs confirmation**. [pp.24,51; `data:r2:c35:f1`, `data:r2:c36:f6`, `data:r2:c84:f5`]

**Inference only:** names such as `case_id`, `run_id`, `task_id` and `document_version_id` suggest relationships to their corresponding entities. Appendix B does not declare their target keys or cardinalities; notably the selected `document_versions` row omits an `id` declaration. Only reference `cases` tenant/workspace FKs are explicitly supplied. Do not implement assumed cascades. [pp.85–86; `data:r2:c138:f20`, `data:r2:c138:f29`]

### DAT-004 — Logical contract register inventory

The columns below preserve exact source classifications. For each row, the four categories respectively carry these invariants: **Owner aggregate:** `UUIDv7 + tenant scope`; **Immutable derivative:** `SHA-256 source/ revision`; **Policy-bound control:** `Actor and role predicate`; **Operational ledger:** `Event ID + trace context`. These are logical register obligations, not proof of four tables per chapter. Hash inputs/serialization, ID subjects, actor predicates and ledger fields remain **Needs confirmation**.

| Source register/page | Owner aggregate | Immutable derivative | Policy-bound control | Operational ledger |
|---|---|---|---|---|
| §1.4 p.10 | ChangeRequest | DesignRevision | RequirementLink | DecisionRecord |
| §2.4 p.13 | Actor | Case | Attachment | ApprovalAssignment |
| §3.4 p.17 | EdgeGateway | CaseService | Orchestrator | RetrievalService |
| §4.4 p.20 | VirtualNetwork | APIReplicaSet | WorkerPool | RegionFailoverPlan |
| §5.4 p.23 | Principal | TenantMembership | AccessPolicy | ResourceAcl |
| §6.4 p.26 | Workspace | CaseAggregate | CaseRevision | CaseStatusEvent |
| §7.4 p.29 | Connector | SyncRun | SourceCursor | SourceDocument |
| §8.4 p.32 | DocumentVersion | ExtractionJob | ContentBlock | ChunkAnchor |
| §9.4 p.36 | SearchChunk | IndexAlias | RetrievalQuery | EvidenceSet |
| §10.4 p.39 | ModelDeployment | PromptTemplate | GenerationAttempt | TokenLedger |
| §11.4 p.42 | AgentRun | PlanNode | ToolCapability | A2ATaskEnvelope |
| §12.4 p.46 | PolicyEvaluation | ApprovalTask | ReviewDecision | PublicationGate |
| §13.4 p.50 | OutboxRecord | QueueEnvelope | WorkflowCheckpoint | DeadLetterEntry |
| §14.4 p.53 | CaseRow | DocumentBlob | OutboxTable | CacheEntry |
| §15.4 p.56 | ApiOperation | ErrorEnvelope | EventCursor | WebhookSubscription |
| §16.4 p.59 | ViewState | ReviewForm | EvidencePanel | Notification |
| §17.4 p.63 | ThreatControl | AuditEntry | DataClassification | KeyReference |
| §18.4 p.66 | TraceSpan | MetricSeries | CostLedger | AlertPolicy |
| §19.4 p.70 | CapacityBudget | AdmissionPermit | RecoveryCheckpoint | LoadProfile |
| §20.4 p.73 | ReleaseArtifact | ConfigVersion | MigrationPlan | RolloutGate |
| §21.4 p.76 | TestCase | EvalDataset | Scorecard | ReleaseGateResult |
| §22.4 p.80 | Runbook | ProvisioningJob | ExportManifest | PurgeReceipt |

[Register evidence: `data:r2:c9:f2`–`data:r2:c9:f5`, `data:r2:c15:f2`–`data:r2:c15:f5`, `data:r2:c21:f2`–`data:r2:c21:f5`, `data:r2:c27:f2`–`data:r2:c27:f5`, `data:r2:c33:f2`–`data:r2:c33:f5`, `data:r2:c39:f2`–`data:r2:c39:f5`, `data:r2:c45:f2`–`data:r2:c45:f5`, `data:r2:c51:f2`–`data:r2:c51:f5`, `data:r2:c57:f2`–`data:r2:c57:f5`, `data:r2:c63:f2`–`data:r2:c63:f5`, `data:r2:c69:f2`–`data:r2:c69:f5`, `data:r2:c75:f2`–`data:r2:c75:f5`, `data:r2:c81:f2`–`data:r2:c81:f5`, `data:r2:c87:f2`–`data:r2:c87:f5`, `data:r2:c93:f2`–`data:r2:c93:f5`, `data:r2:c99:f2`–`data:r2:c99:f5`, `data:r2:c105:f2`–`data:r2:c105:f5`, `data:r2:c111:f2`–`data:r2:c111:f5`, `data:r2:c117:f2`–`data:r2:c117:f5`, `data:r2:c123:f2`–`data:r2:c123:f5`, `data:r2:c129:f2`–`data:r2:c129:f5`, `data:r2:c135:f2`–`data:r2:c135:f5`]

Case/CaseService/CaseAggregate, ApprovalTask/ReviewForm, IndexAlias and other disputed classifications require DAT-020 clarification; none is resolved by inventing immutable snapshots and mutable heads. Component spelling is not a physical mapping. WebhookSubscription does not make optional webhooks mandatory.

## Data Field Definitions

### DAT-005 — Reference `cases` physical declarations

All fields below are reference persistence declarations, not browser/API defaults. No additional index, type or product is independently selected. [p.86 B.2; `data:r2:c138:f20`–`data:r2:c138:f28`]

| Physical name | Meaning/type | Nullability/default | Key/value constraint |
|---|---|---|---|
| `id` | Case identifier; `UUID` | Primary key; no default shown | `PRIMARY KEY`; UUIDv7 generation separately scoped, not supplied SQL |
| `tenant_id` | Tenant; `UUID` | `NOT NULL`; no default shown | `REFERENCES tenants(id)` |
| `workspace_id` | Workspace; `UUID` | `NOT NULL`; no default shown | `REFERENCES workspaces(id)` |
| `status` | Case lifecycle; `TEXT` | `NOT NULL`; no default shown | CHECK six literals below |
| `revision` | Aggregate revision; `BIGINT` | `NOT NULL DEFAULT 1` | No positive-value CHECK/increment SQL shown |
| `sensitivity` | Classification; `TEXT` | `NOT NULL DEFAULT 'INTERNAL'` | No sensitivity CHECK or length shown |
| `created_at` | Creation time; `TIMESTAMPTZ` | `NOT NULL DEFAULT now()` | Precision/encoding unresolved |
| `updated_at` | Update time; `TIMESTAMPTZ` | `NOT NULL DEFAULT now()` | No automatic update trigger shown |

Additional constraint: `UNIQUE (tenant_id, id)`, alongside—not instead of—the `id` primary key. Status CHECK values are `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED`. Lengths, final indexing strategy and omitted fields remain **Needs confirmation**.

Preserve reference tenancy SQL:

```sql
ALTER TABLE cases ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_scope ON cases
USING (tenant_id = current_setting('app.tenant_id')::UUID);
```

**Confirmed production qualifications:** reset scoped connection-pool session variables **after every transaction**. Additionally enforce workspace-tenancy membership via foreign keys **or controlled write procedures**; the alternative is not selected. Independent `tenant_id` and `workspace_id` FKs alone do not establish membership. Role/bypass settings, context assignment/reset mechanics, missing-setting behavior and complete all-table policies are **Needs confirmation**.

### DAT-006 — Domain fields and code systems

| Subject/fields | Confirmed logical definition | Requiredness/design qualification |
|---|---|---|
| Case title, description, priority, sensitivity label, status, owner, current approved result, revision | Stored case metadata; monotonic revision | Physical names/types, lengths, initial requiredness and editability unresolved |
| Attachments, business context | New-case intake | Format/requiredness beyond admitted-file contract unresolved |
| Labels, confidences, provenance, correction reason code | Asynchronous classification and reason-coded corrections | Catalogs/ranges/types/authorizers unresolved |
| Impact, urgency, contractual deadline, breach prediction | Priority from explicit impact/urgency; workspace calendar deadline; prediction advisory | Formula/calendar/timezone identifiers unresolved |
| Workspace retention class, allowed models, credential references, approved toolsets, reviewer routing | Revision-preconditioned audited settings | Catalogs/types/config endpoint unresolved |
| Policy sensitivity, requested action, evidence quality, model class, financial impact category, confidence bands, rule-set version | Normalize/store all inputs for reproducibility | Literal mappings to `rule_version`, `policy_version`, digests unresolved |
| Review decision, actor, timestamp, evaluated artifact hash, rationale | Recorded decision content | Input/server metadata distinction and types unresolved; annotations explicitly optional |
| Model capability, region, handling class, context length, cost profile, evaluation approval | Approved deployment registry | Specific deployments/units/values unresolved |
| Input/output token budget and provider usage | Reserve/account under workspace quota | Structure/precision/pricing/release/reconciliation unresolved |

[pp.12,24–26,37–39,44–46; `data:r2:c13:f1`, `data:r2:c36:f1`–`data:r2:c36:f6`, `data:r2:c38:f1`–`data:r2:c38:f2`, `data:r2:c60:f1`, `data:r2:c62:f1`, `data:r2:c72:f1`, `data:r2:c73:f4`]

Information classes: `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`; maximum class of included material governs model route, log redaction, retention and approval. Policy outcomes: `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY`; these are not lifecycle states or model authority. Accessible display labels `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` have an unresolved mapping to durable states. [pp.44,57,62; `data:r2:c72:f5`, `data:r2:c96:f5`, `data:r2:c103:f1`]

### DAT-007 — Evidence, extraction and search fields

| Data | Confirmed content/constraint | Unresolved attributes |
|---|---|---|
| Chunk anchor | Source URI, file hash, page number, **optional** bounding box | Field names, URI/hash encoding, page basis, bbox coordinates |
| PDF block | Page index/bounding boxes, table row/column annotations, heading/reading order | Types, layout schema, table cardinalities |
| Immutable derivative identity | Content fingerprint plus pipeline version; side-by-side revised normalization | Fingerprint algorithm, relation to `parser_version`/`hash`/`text_hash` |
| Quality flags | Empty-page ratio, unknown-character ratio, table-loss indicators, language confidence | Computation/scales/thresholds/storage |
| Search row | `tenant_id`, `workspace_id`, `document_version_id`, `chunk_id`, `language`, `classification`, normalized keyword text,1536-dimensional embedding | Remaining physical types/names/precision/analyzers/keys |
| Evidence response item | Chunk ID, source title, document revision, page anchor, ACL digest | Literal JSON mapping, Citation schema, digest algorithm |
| Cache key | Tenant, user-scope digest, source ACL revision, query hash, index generation | Serialization/hash algorithm/TTL/physical fields |
| Object key | Tenant, workspace, document, version, object role; opaque public name | Literal path and role catalog |

Citation IDs are opaque and verified before display. Generation cites only resolvable anchors with current permission. Reviewers can open source and highlight anchored page range before approval. No persisted inspection-completion record is required by supplied evidence. [pp.31–35,52–53,57–58; `data:r2:c49:f1`–`data:r2:c49:f2`, `data:r2:c49:f6`, `data:r2:c50:f1`–`data:r2:c50:f7`, `data:r2:c54:f1`, `data:r2:c56:f1`–`data:r2:c56:f2`, `data:r2:c86:f1`–`data:r2:c86:f7`, `data:r2:c95:f2`, `data:r2:c96:f6`, `data:r2:c97:f4`]

### DAT-008 — Boundary, event and request contexts

| Contract | Confirmed names/inclusion | Scope and open mapping |
|---|---|---|
| General boundaries | `tenant_id` and actor context | Every boundary; not necessarily editable/body fields |
| Durable-changing boundary record | `tenant_id`, `revision`, `actor_id`, `occurred_at`, correlation ID | “wherever the operation changes durable state”; all DAT-004 subjects inherit applicable condition |
| Canonical event | `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, `payload` | All events; UTC and canonical JSON; types/canonicalization algorithm unresolved |
| Request telemetry | `trace_id`, `correlation_id` | Every request; provider trace independent |
| SSE | Monotonically increasing offset; reconnect `Last-Event-ID` | Retained caller-scoped replay, not necessarily canonical `event_id` |

No alias is approved between `revision`/`aggregate_revision`, correlation ID/`trace_id`, principal/actor metadata or SSE/event identity. Appendix B outbox selected fields do not replace the full event envelope. [pp.16,24–25,48,54–59,64,85; `data:r2:c20:f2`, `data:r2:c36:f3`, `data:r2:c78:f1`–`data:r2:c78:f5`, `data:r2:c90:f3`, `data:r2:c91:f1`, `data:r2:c108:f1`, `data:r2:c138:f15`]

## Lifecycle and Consistency

### DAT-009 — Tenant and referential integrity

1. Bind authenticated principal/tenant to requests; authorize role, workspace membership, sensitivity, source ACL, action and separation as applicable.
2. Re-evaluate resource attributes inside domain transactions and apply RLS. Every storage predicate includes tenant identity.
3. Reject cross-tenant substitutions with the absent-ID not-found response class, without revealing private existence; denial audit may retain principal and denied resource class.
4. Apply current ACL before retrieval text reaches generation and again at publication after permission changes. Ranking, immutable versions, cached results and prior approval never grant continuing access.

OIDC authorization-code flow uses PKCE and issuer/audience/expiry/subject/tenant token concepts. Reject unexpected algorithms/missing tenancy; no long-lived browser-local-storage refresh tokens. Optional secure `HttpOnly`, `SameSite` BFF cookies are unselected. [pp.21–23,34,51,89; `data:r2:c30:f1`, `data:r2:c30:f5`, `data:r2:c31:f1`, `data:r2:c31:f5`, `data:r2:c32:f1`, `data:r2:c32:f5`, `data:r2:c53:f2`, `data:r2:c83:f2`, `data:r2:c141:f3`]

### DAT-010 — Case and asynchronous-job lifecycle

**Case creation/read/update:** API-003 creates idempotently (`201`), starting `NEW`; classification is asynchronous. API-004 reads authorized current revision (`200`). API-005 PATCH uses `If-Match` (`200/409`). Actor/request-fingerprint outcomes are retained for24 hours; identical same-key creation yields one case/identical response, changed-body reuse yields `409 IDEMPOTENCY_CONFLICT`. Conflict returns `CASE_VERSION_CONFLICT` and current revision without changing business state. Long-running-job POST mutations transport `Idempotency-Key`; its complete scope/fingerprint/expiry contract remains open. [pp.12,25,54,83–84,89; `data:r2:c13:f1`, `data:r2:c37:f4`–`data:r2:c37:f5`, `data:r2:c90:f5`, `data:r2:c137:f6`–`data:r2:c137:f8`, `data:r2:c137:f21`, `data:r2:c141:f1`–`data:r2:c141:f2`]

| Case transition | Confirmed rule |
|---|---|
| `NEW → TRIAGED` | Role/revision/approval guards as applicable |
| `TRIAGED → IN_PROGRESS` | Supported |
| `IN_PROGRESS → PENDING_APPROVAL` or `RESOLVED` | Supported |
| `PENDING_APPROVAL → RESOLVED` or `IN_PROGRESS` | Supported |
| `CLOSED` | Final **unless explicitly reopened as a new revision** |

Closing edge/actor, reopening endpoint/target state and complete predicates remain **Needs confirmation**. Closure snapshots approved answer, cited versions and reviewer decisions as immutable approved-output lineage. [pp.25–26,82; `data:r2:c37:f1`, `data:r2:c38:f6`, `data:r2:c137:f2`]

**Mandatory job tenancy:** “Background jobs carry immutable tenant identity in signed envelopes.” Signing and tenant-identity immutability are separate confirmed obligations for classification, ingestion, synchronization, workflow, replay, provisioning/export/purge and other actual background jobs. Do **not** classify the entire job record immutable. Envelope schema, signature algorithm/keys and verification remain **Needs confirmation**. This also applies beside DAT-012 and DAT-017; canonical events/general tenant context do not substitute. [p.22 §5.3.1; `data:r2:c32:f2`]

### DAT-011 — Ingestion, connector and derivative lifecycle

1. Admit R1 PDF, DOCX, HTML, UTF-8 text with MIME signature/extension agreement and configurable25MB per file; enforce an unspecified decompression-bomb threshold.
2. Scan before parsing, disable macros and never fetch embedded remote references. Unsafe content quarantines without indexing; API-006 `202` accepts ingestion, not READY.
3. Preserve layout/provenance. OCR fallback is opt-in/provenance-marked; beyond-English OCR deferred. Normalize transport artifacts without rewriting claims; changed pipelines produce side-by-side immutable derivatives.
4. Preserve quality flags. Authorized low-quality documents remain viewable but cannot support autonomous recommendations; low quality is not automatically unsafe quarantine.
5. Connector capability gaps trigger explicit visible lower-trust warning, not assumed support. Credentials are workspace-scoped vault references; revoked queued jobs fail `CONNECTOR_REAUTH_REQUIRED` without tokens.
6. Record provider cursor/high-watermark/error ledger. Advance after durable preceding outcomes; bounded-retry quarantine records reason/correlation/remediation. Recorded ledger exceptions permit remaining batch continuation without declaring poisoned items successful.
7. Source deletion writes tombstones/schedules index removal. ACL changes invalidate cache before new results and revoked access applies before next retrieval, even during pending cleanup.
8. Rebuild parallel index; atomically switch read alias only after completeness/recall checks. Failed indexing never rolls back accepted source metadata; reconcile fingerprints/links from outbox.

Document catalog: `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED`, guarded by scan/quality. Exact edges/remediation/thresholds remain open. Sync respects `Retry-After`, bounded backoff/jitter, workspace quotas/fairness. [pp.27–36,49,82–83,89; `data:r2:c42:f1`, `data:r2:c42:f5`, `data:r2:c43:f1`, `data:r2:c43:f4`, `data:r2:c44:f1`, `data:r2:c44:f4`, `data:r2:c48:f1`, `data:r2:c48:f4`, `data:r2:c49:f1`–`data:r2:c49:f6`, `data:r2:c50:f6`–`data:r2:c50:f7`, `data:r2:c54:f5`, `data:r2:c79:f5`, `data:r2:c137:f4`, `data:r2:c137:f9`, `data:r2:c141:f15`]

### DAT-012 — Run, model and tool lifecycle

API-007 accepts bounded run (`202`); API-008 reads stages/evidence (`200`); API-009 SSE resumes (`200`). Immediate run creation and refresh reconstruct progress from server state. General `POST /v1/runs` (API-042e) versus case-scoped API-007 remains unresolved.

Run catalog: `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED`. Checkpoint each stage before downstream dispatch. Persist plan revision before side effects; DAG depth8/tool invocations16 with explicit dependencies/replayable checkpoints. Triage classifies, Research retrieves, Draft assembles; Policy Evaluator is deterministic. Missing approval, exhausted call budget, repeated invalid plans, denial and deadline terminate per chapter11; chapter2 permits recoverable timeout. **Needs confirmation:** normal review waiting versus missing authorization and timeout/FAILED mapping. [pp.15,40–42,49,58,82–83; `data:r2:c17:f4`, `data:r2:c66:f1`, `data:r2:c66:f5`, `data:r2:c68:f1`, `data:r2:c79:f1`, `data:r2:c97:f1`, `data:r2:c137:f3`, `data:r2:c137:f10`–`data:r2:c137:f12`]

Models whitelist deployments, not brands; fallback requires approved equal-or-stronger handling and approved region/deployment. Reserve tokens/account usage; exhaustion is terminal for current run, with no automatic model/class switch. Compose fixed rules, signed workflow, validated input and delimited untrusted passages; strip evidence tool directives/record injection indicators. Versioned JSON parsing uses bounded retries; unknown fields, invalid citations/control-character injection cause `MODEL_OUTPUT_INVALID` and no publication. This is not a universal REST unknown-field rule. [pp.37–39,89; `data:r2:c60:f1`, `data:r2:c60:f5`, `data:r2:c61:f1`, `data:r2:c61:f4`, `data:r2:c62:f1`, `data:r2:c62:f5`, `data:r2:c141:f5`]

Discovery/schema validity never grants tool permission. Validate pinned MCP arguments; external writes require separate capability; mutable calls require idempotency and consequential human authorization. Do not substitute an equivalent tool for a denied action. Apply DAT-010's signed immutable job-tenancy requirement independently of plan/workflow signing. [pp.7,22,41–42; `data:r2:c4:f2`, `data:r2:c4:f4`, `data:r2:c32:f2`, `data:r2:c67:f1`, `data:r2:c67:f5`, `data:r2:c68:f5`]

### DAT-013 — Review, publication and histories

1. Select policy reviewer pool/minimum role/separation; own-high-risk self-approval is prohibited. Appendix B's unqualified “no self approval” leaves broader scope unresolved—no lower-risk permission is granted.
2. Show exact candidate, citations, model/prompt version and policy reasons. Source inspection is available before approval. Required review inputs gate UI actions; their names/types remain open.
3. API-010 (`200/409`) binds decision to reviewed hash. Changed/wrong-hash or unauthorized decisions reject stale/denied, preserve business state and audit denial. Decision records are immutable; annotations explicitly optional.
4. Review states: `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED`, guarded by actor/hash/separation. Configured expiry reassigns/escalates without approval; TST-010 records escalation. Branch/SLA remain open.
5. Overrides require elevated role, secondary reviewer and audited reason. Denied rework creates new run revisions, never retroactive approval.
6. Publication is distinct: validate exact artifact/evidence/versioned policy and current permissions. Unapproved high-risk cannot publish. Commit final pointer and satisfied gate atomically; old approvals cannot publish changed artifacts. `ApprovalDecisionRecorded` consumer **validates publication**, not automatically publishes.

[pp.11–12,45–46,58–59,82–85,87,89; `data:r2:c12:f5`, `data:r2:c13:f5`, `data:r2:c73:f1`, `data:r2:c73:f4`, `data:r2:c73:f8`, `data:r2:c74:f1`, `data:r2:c74:f5`, `data:r2:c76:f2`, `data:r2:c97:f4`, `data:r2:c137:f5`, `data:r2:c138:f12`–`data:r2:c138:f13`, `data:r2:c139:f5`, `data:r2:c141:f6`, `data:r2:c141:f10`]

`case_revisions` and `audit_events` are append-only. Approved source versions/decision lineage are immutable; assignment/form immutable-subject conflicts remain DAT-020, not permission to rewrite history.

### DAT-014 — Transactions, concurrency and replay

1. Validate before transaction, at domain invariants and before tool dispatch; client validation is convenience only.
2. Reject stale/unauthorized business writes before relevant publication; preserve business state. Denial/duplicate evidence is not an accepted business transition.
3. Apply stated case-mutation/approval/outbox ACID boundary as applicable. Do not infer every case mutation also approves another record. Search/webhook changes are asynchronous and reconciled; state-changing workflows use outbox or explicitly reconciled saga.
4. At-least-once consumers check event/operation identity, ledger and aggregate revision. Record duplicates and do not reapply. Detect delayed/stale revisions without cross-partition order reliance.
5. Each accepted transition has one audit record and tenant-scoped traces; correlated event logs/audit exclude document text in diagnostics.
6. Transient retries are bounded exponential backoff/jitter/per-dependency breakers. Validation/permission failures are permanent and never retry.
7. Operator replay requires reason, dry run and bounded scope. Preserve original event identity **except** schema-transforming migration with explicit provenance linkage.
8. Expand-contract migrations add nullable columns, backfill bounded batches then enforce constraints; active readers must not lose fields. Initial migration nullability is not final business nullability.

[pp.17,48–56; `data:r2:c20:f6`–`data:r2:c20:f7`, `data:r2:c78:f4`, `data:r2:c80:f1`, `data:r2:c80:f5`, `data:r2:c82:f1`–`data:r2:c82:f3`, `data:r2:c85:f1`, `data:r2:c85:f6`, `data:r2:c92:f4`]

### DAT-015 — Personal data, secrets and cryptographic lifecycle

**Confirmed.** Application secrets remain in a key vault with managed-identity access. **“Encryption keys rotate on defined policy without requiring bulk re-encryption in the request path.”** Both policy-driven rotation and the request-path restriction are mandatory. Key hierarchy, algorithms, intervals, isolation/throughput tradeoff and implementation remain **Needs confirmation**; unresolved choices do not permit never rotating keys. This applies also beside DAT-016. Service-credential automatic rotation is a separate obligation; credentials never appear in traces/model prompts. [pp.21,63 §17.3.2; `data:r2:c30:f6`, `data:r2:c104:f5`–`data:r2:c104:f6`]

Encrypt objects at rest and use access-controlled short-lived signed URLs. No model/tool receives secrets outside declared scope; providers receive scoped context/structured prompts, not raw connector tokens or unrestricted database access. Extraction tags likely PII; redact nonessential fields before providers **where policy permits**. Maximum included classification governs policy. Logs default to token counts/digests, not whole prompts; this does not waive mandatory bans. Public errors/responses exclude credentials, full prompts, retrieved documents and unauthorized existence; diagnostics exclude documents/API secrets. [pp.15,52,62–64,84; `data:r2:c18:f1`, `data:r2:c86:f2`, `data:r2:c101:f2`, `data:r2:c103:f1`, `data:r2:c103:f4`–`data:r2:c103:f5`, `data:r2:c108:f2`, `data:r2:c137:f22`]

### DAT-016 — Audit, retention and controlled exit

Audit is append-only, batch-hash chained and exported to independently controlled retention storage. Operators query but never alter historical review decisions; Auditor scope is redacted/nonediting. Diagnostic logs have30-day **default** TTL; security audit follows a distinct7-year **fictional** policy. Corporate retention selection remains unresolved. Purges record receipts/legal-hold exceptions; do not apply diagnostic TTL to security audit. Retention jobs consider only eligible closed cases; CLOSED alone is not eligibility. [pp.11–12,26,62,66; `data:r2:c12:f6`, `data:r2:c38:f7`, `data:r2:c104:f1`, `data:r2:c110:f5`]

Export/delete both require two independent approval checks and `Admin + approver` scope. Export explicitly requires **two-person approval plus manifest**; single Admin fails. Export contains case metadata, approved artifacts, source references and checksum audit manifests, excluding secrets/internal prompts. Deletion honors holds, writes tombstones, removes blobs/index entries and records receipts; held protected records are retained/receipted. Soft-deleted entities cannot be retrieved; final purge is scheduled tombstone processing. API-016/017 `202` is acceptance, not completion. Data-subject access uses the same inventory, not an invented endpoint. Tenant/workspace scope, partial receipts and lineage purge remain open. DAT-015 vault/rotation rules remain binding during retention/exit. [pp.51,78–80,83,88–89; `data:r2:c84:f6`, `data:r2:c131:f1`, `data:r2:c134:f1`, `data:r2:c134:f5`, `data:r2:c137:f19`–`data:r2:c137:f20`, `data:r2:c140:f11`, `data:r2:c141:f13`]

### DAT-017 — Operational, usage, evaluation and release data

| Activity | Confirmed data/lifecycle | Open implementation |
|---|---|---|
| Provisioning | Workspace policy/encryption references/role bindings/quotas/connector stubs in idempotent workflow; incomplete visible and blocks sync | Inputs/status/compensation/owners; not a single proven DB transaction |
| Historic onboarding | Bounded windows, stable IDs, per-batch receipts; readiness from index coverage,not queue emptiness | Bounds/coverage formula/threshold |
| ACL incident | Suspend affected aliases/revoke cached evidence/preserve audit/scoped ACL replay; restore only after negative access tests | Operator permissions/probes/receipts |
| Provider outage | Disable new generation; manual editing/evidence remain; degraded display; page only if availability budget impacted | Status/threshold/on-call mapping |
| Admission | Workspace tokens/queue age/provider capacity;429+Retry-After; saved cases remain | Limits/windows/formulas |
| Vector fallback | Lexical retrieval may continue **with visible reduced-quality flag** | Selection/flag schema;never safety bypass |
| Usage | Golden/AI metrics; workspace cost centers/deployment versions; daily budget/forecast/rejected-excess rollups | Units/currency/formulas/daily cutoff |
| Evaluation |1200 synthetic controlled cases store expected citations/outcomes; frozen precision≥.97,unsupported≤.02,high-risk recall1.00; domain confidence/shift | Confidence/denominators/domains/report schema;low confidence blocks |
| Release | Reconstruct binary/prompt/policy; bind image/schema/prompt/model-routing policy; signed env/images,SBOM,allowed build identity,Security/SRE validation | Signature formats/gates/owners/readability |
| Migration/rollback | Compatible predeploy,canary,old-replica drain; record new-write readability; regression traffic rollback **not DB down-migration** | Scripts/windows/batch bounds |
| Recovery | Primary writes,warm recovery incident-command restore; continuous PostgreSQL backup reference RPO≤15min,RTO≤4h; joint object/index verification | Formats/schedules/order/retention |

[pp.19,64–80; `data:r2:c25:f6`, `data:r2:c108:f6`, `data:r2:c109:f6`, `data:r2:c110:f1`, `data:r2:c115:f1`, `data:r2:c115:f5`, `data:r2:c116:f1`, `data:r2:c120:f5`, `data:r2:c121:f1`–`data:r2:c121:f6`, `data:r2:c122:f1`, `data:r2:c122:f5`–`data:r2:c122:f6`, `data:r2:c127:f1`, `data:r2:c127:f5`, `data:r2:c128:f6`, `data:r2:c132:f1`–`data:r2:c132:f5`, `data:r2:c133:f1`, `data:r2:c133:f5`]

Actual operational background jobs inherit DAT-010's **signed envelopes with immutable tenant identity** (`data:r2:c32:f2`, p.22); build/config/test signing is not a substitute.

Delayed-indexing procedure:
1. Detect oldest queue age/backlog, tenant/index generation.
2. Pause only faulty connector/shard; preserve accepted records.
3. Diagnose event ID/outbox lag/parser flags/search throttling/ACL revision.
4. Replay validated outbox with bounded operator-controlled job.
5. Compare fingerprints/index versions and run denied probes before closure.
6. Link audit IDs/time window/blast radius/quality effect/preventative action.
[p.90 F.1; `data:r2:c142:f7`–`data:r2:c142:f13`]

## Integration Data and Acceptance Criteria

### DAT-018 — Formats, events and representative values

Public REST uses `/v1`, cursor pagination and RFC3339. Server/event time is UTC; UI uses workspace-local timezone-labeled display without changing event order/durable representation. JSON event canonicalization algorithm is undefined. Repository-controlled OpenAPI/protobuf govern contracts; nonbreaking evolution is additive and removal requires scheduled migration. Model JSON has its own versioned validation. File encoding is confirmed only as UTF-8 for supported text; DB/export/config/other-file encodings remain **Needs confirmation**. [pp.15,48,54–59,82; `data:r2:c18:f6`, `data:r2:c78:f1`, `data:r2:c90:f1`, `data:r2:c92:f1`, `data:r2:c98:f5`, `data:r2:c137:f1`]

MCP `knowledge.search@v1`:

| Direction/name | Exact type | Constraint |
|---|---|---|
| Input `query` | `string` | Length/blank/requiredness unresolved |
| Input `case_id` | `uuid` | Encoding/requiredness unresolved |
| Input `max_items` | `int<=10` | Tool upper bound10;minimum/default unresolved |
| Output `evidence_set_id` | `uuid` | Encoding/requiredness unresolved |
| Output `citations` | `Citation[]` | Citation schema unresolved |

Authorization is tenant-scoped `read:permitted_documents`; read-only, no arbitrary URLs/filesystem. Discovery never authorizes invocation. A2A declares task/capability/input-output schema/deadline/trace; receiver may decline. Preserve illustrative JSON, not a complete contract:

```json
{"task_id":"019ac000-0000-7000-8000-000000000042","tenant_id":"tenant_example_01","capability":"research.grounded_search.v1","input_schema":"schema://oriondesk/research-request/1","deadline_at":"2026-11-09T08:00:00Z","trace_id":"trace_example_01","authorization_ref":"grant_readonly_14","payload":{"case_id":"case_demo","query":"..."}}
```

`case_demo` versus MCP UUID and omitted `output_schema` remain unresolved,no typed exception. [pp.41,87 C.2; `data:r2:c67:f5`, `data:r2:c139:f9`–`data:r2:c139:f12`]

All registered events use versioned envelope/outbox and applicable DAT-014 controls. Selected payload concepts below are not complete JSON keys:

| Event | Producer | Payload concepts | Consumer action |
|---|---|---|---|
| CaseCreated | Case Service | Case ID/revision | Classifier |
| DocumentNormalized | Ingestion | Version ID/source hash | Build index |
| SearchIndexCommitted | Indexer | Generation/document revision | Invalidate query cache |
| AgentPlanApproved | Orchestrator | Run ID/plan hash | Dispatch still-authorized steps |
| ApprovalDecisionRecorded | Policy Service | Task/actor/content hash | Validate publication |
| WorkflowStageAdvanced | Orchestrator | Run/stage/checkpoint | Resume consumers |
| AccessDenied | Policy Service | Principal/action/policy digest | Alert enrichment |
| TenantDeletionVerified | Retention Worker | Manifest ID/receipt hash | Close purge record |

[p.87 C.1; `data:r2:c139:f1`–`data:r2:c139:f8`]

Other exact register events: `BaselineCommitted`, `RunRequested`, `DeploymentPromoted`, `CaseStateChanged`, `ConnectorSyncStarted`, `ModelInvocationCompleted`, `DataRetentionPurgeCommitted`, `ApiCompatibilityVerified`, `UserReviewOpened`, `SecurityPolicyChanged`, `SloBurnRateDetected`, `BackpressureActivated`, `ReleasePromoted`, `EvaluationCompleted`. Their full producers/triggers/payloads remain open. `CaseStatusEvent` is not automatically `CaseStateChanged`; deployment/release/baseline/purge events are distinct. GET adjacency does not emit events. [pp.10,17,20,26,29,39,53,56,59,63,66,70,73,76; respective DAT-004 register event findings `data:r2:c9:f8`, `data:r2:c21:f8`, `data:r2:c27:f8`, `data:r2:c39:f8`, `data:r2:c45:f8`, `data:r2:c63:f8`, `data:r2:c87:f8`, `data:r2:c93:f8`, `data:r2:c99:f8`, `data:r2:c105:f8`, `data:r2:c111:f8`, `data:r2:c117:f8`, `data:r2:c123:f8`, `data:r2:c129:f8`]

Optional webhooks sign/verify signature+event age and retry exponentially; failure never rolls back committed case state. SSE replays retained caller-scoped history via `Last-Event-ID`; framing/TTL/expired-history recovery remain open. Repeated endpoint clauses require validation before long work; unavailable dependencies yield documented retryable error **OR persisted async ID**,never ambiguous success. API-043 branch/owner/schema remains open; explicit ordinary200/201/202 contracts stand. [pp.54–56; `data:r2:c90:f4`, `data:r2:c91:f1`, `data:r2:c91:f4`, `data:r2:c93:f6`–`data:r2:c93:f7`]

A.3 conflict example preserves `error.code="CASE_VERSION_CONFLICT"`, message `Case revision no longer matches.`, `correlation_id="trace_01HZZ_EXAMPLE"`, `retryable=false`, `details.expected_revision=7`, `details.actual_revision=8`, `HTTP/1.1 409 Conflict`, `Content-Type: application/json`. Object/string/boolean/integer example types do not establish universal requiredness or limits. Preserve uppercase codes despite unresolved snake-case convention. [p.84; `data:r2:c137:f21`–`data:r2:c137:f22`]

Appendix F examples—not universal defaults:

```yaml
release: r1.0
workflow: {max_plan_depth: 8, max_tool_calls: 16, run_timeout_seconds: 180, replay_dedup_hours: 24}
retrieval: {max_candidate_chunks: 80, max_selected_chunks: 10, embed_dimension: 1536, hybrid_rrf_k: 60}
policy: {auto_publish_classification: INTERNAL, require_human_review_for: [HIGH_RISK, RESTRICTED], self_approval_allowed: false}
storage: {upload_limit_mb: 25, user_data_region: primary-approved-region}
observability: {trace_sample_rate: 0.10, diagnostic_retention_days: 30, audit_retention_years: 7}
```

Only independently evidenced8/16/1536/configurable25MB and scoped retention obligations are confirmed in substantive sections. Example24-hour replay does not equal request24-hour idempotency or SSE retention. `INTERNAL` does not grant unrestricted publication; placeholder region is not selected. [p.90; `data:r2:c142:f1`–`data:r2:c142:f6`]

Reference capacity is2000 active daily users,60 steady/180 burst rps,100000 documents/tenant maximum,20 runs/large tenant; typical1MB yields approximately40–120chunks. Reference API99.9% monthly, case-create P95 within/under300ms unresolved at equality, search P95<1.5s excluding remote fetch, model latency separate. These are not observed outcomes or automatically configured quotas. [pp.12,65,68–69; `data:r2:c14:f1`, `data:r2:c109:f1`–`data:r2:c109:f2`, `data:r2:c114:f1`, `data:r2:c114:f5`]

Representative figures retain `ORIONDESK / OPERATIONS CONSOLE`, fictional tenant/R1.0 and Meridian Manufacturing;128 open/14 review/97.6%/Healthy,five case labels `OD-2026-1042` through `OD-2026-1038` and gate HUMAN_REVIEW/five citations/gateway-r1.2/Assigned to reviewer/Awaiting decision are depictions only. Preserve exact descriptions in SF-015; no formulas,ID patterns,limits,states or deployment selections follow. Title/selected-sidebar pairs remain SF-005,not aliases. [pp.7,14,33,43,47,60,67,77,81; `data:r2:c4:f6`–`data:r2:c4:f10`, `data:r2:c16:f5`–`data:r2:c16:f9`, `data:r2:c52:f5`–`data:r2:c52:f9`, `data:r2:c70:f4`–`data:r2:c70:f8`, `data:r2:c76:f5`–`data:r2:c76:f9`, `data:r2:c100:f5`–`data:r2:c100:f9`, `data:r2:c112:f5`–`data:r2:c112:f10`, `data:r2:c130:f4`–`data:r2:c130:f7`, `data:r2:c136:f5`–`data:r2:c136:f9`]

### DAT-019 — Data acceptance criteria

These are obligations,not reported passes. Retain preceding SF-019 AC and API-057 mappings.

| Source test | Action | Expected outcome |
|---|---|---|
| TST-001 | Same-key case twice | One case,identical response |
| TST-002 | Changed-body key reuse |409 IDEMPOTENCY_CONFLICT |
| TST-003/T-01 | Valid foreign-tenant ID/token | Non-disclosing404-equivalent;RLS/domain guard |
| TST-004/T-08 | Revoke indexed source;also revoke during search | No forbidden next-query evidence;ACL-revision cache control;in-flight contract open |
| TST-005 | Model schema failure | MODEL_OUTPUT_INVALID,no publication |
| TST-006/T-03 | Wrong/prior artifact hash after revision | Stale rejection/audit,no business mutation |
| TST-007/T-07 | Same outbox event100 replays | Exactly one accepted business transition;duplicate outcomes,no reapplication |
| TST-008 | Provider429 burst | Capped retries/controlled admission;save-case availability |
| TST-009 | Missing citations | Needs review **OR unsupported**,selection open |
| TST-010 | Review expires | No implicit approval;escalation recorded |
| TST-011 | Keyboard-only case open | No blocked action,visible focus |
| TST-012 | Region recovery | Stated RPO/RTO while preserving safety |
| TST-013 | Tenant purge under hold | Protected records retained/receipted |
| TST-014 | Arbitrary MCP invocation | DENY before dispatch |
| TST-015/T-04 | Unsafe PDF/polyglot/zipped hostile input | Scan/sandbox/bounded parse,quarantine,no index;ZIP not supported format |
| TST-016 | Safety-regressed canary | Promotion blocked |
| T-02/T-05/T-06 | Hostile PDF/credential observation/regional outage | Delimit/pin tools,vault+safe telemetry,approved fallback |
| T-09/T-10 | Historical edit/recursive hints | Append-only hash integrity,bounded tools/steps/time |
| T-11/T-12 | Single Admin export/replaced expected fixtures | Two-person+manifest denial/versioned signed dataset manifest |

[pp.88–89; `data:r2:c140:f1`–`data:r2:c140:f14`, `data:r2:c141:f1`–`data:r2:c141:f16`]

Also test source-anchor resolution/current access, low-quality viewability exclusion,server refresh/scoped SSE,publication reauthorization,pool reset/workspace integrity,closure lineage,accepted source durability after indexing failure,credential revoke,incomplete provisioning and negative probes before restoration. Every revised invariant links at least one negative test. Critical isolation/approval permits zero exceptions; unmitigated critical findings block promotion regardless of benchmark. SEC-001–012 evidence is independently reproduced/reviewed by a security-control owner and release-signed; mapping to T-01–12 remains absent. [pp.8,22,26,32,50–59,74–80,88; `data:r2:c5:f2`, `data:r2:c32:f2`, `data:r2:c40:f4`, `data:r2:c50:f7`, `data:r2:c82:f3`, `data:r2:c100:f2`, `data:r2:c125:f2`, `data:r2:c132:f2`, `data:r2:c133:f5`, `data:r2:c140:f13`–`data:r2:c140:f14`]

Synthetic fixtures cover successful,empty,mixed-permission,adversarial,malformed inputs; every randomized test records seed. Corpora freeze/version and undergo independent leakage review. Full release pack includes unit,schema evolution,negative authorization,replay,staging sync,visual accessibility,search recall,grounding,policy recall,load,DR. Outputs are signed/release-digest linked. Signature/report/statistical schemas remain open. [p.89 E.1–E.2; `data:r2:c141:f17`–`data:r2:c141:f22`]

## Consistency and Open Questions

### DAT-020 — Required decisions, mappings and amendments

No TBD is permission to choose silently. All unspecified attributes in DAT-003–008 remain **Needs confirmation**; no new physical schemas, indexes, endpoints, schedules, owners, dates or approvals are invented. Retain complete gaps beside affected data and link these IDs in future Stage8 consolidation.

| Open ID | Affected data/earlier identifiers | Evidence and required resolution |
|---|---|---|
| DAT-OQ-001 | DAT-003–008;SF OQ-002/API-G01 | Complete all physical/wire fields,types,lengths,precision,nullability,requiredness,defaults,keys,cardinality,owners;selected B.1 is partial,p.85 `data:r2:c138:f1`. Do not promote persistence defaults to forms |
| DAT-OQ-002 | DAT-004/010;SF OQ-005/API-G05 | Case/CaseService/CaseAggregate immutable rows pp.13/17/26 (`data:r2:c15:f3`,`data:r2:c21:f3`,`data:r2:c39:f3`) versus mutable metadata/revision pp.16/24/85 (`data:r2:c19:f5`,`data:r2:c36:f5`,`data:r2:c138:f5`). Define immutable subject/amend registers;no invented split |
| DAT-OQ-003 | DAT-004/013;SF OQ-007/API-G05 | ApprovalTask/ReviewForm immutable pp.46/59 (`data:r2:c75:f3`,`data:r2:c99:f3`) versus assignment/expiry/input pp.45/58 (`data:r2:c73:f1`,`data:r2:c97:f4`). Immutable approval_decisions p.85 (`data:r2:c138:f13`) does not resolve tasks/forms |
| DAT-OQ-004 | DAT-004/011/014/017;SF OQ-016/API-G05 | Define immutable subjects/lifecycles for APIReplicaSet,TenantMembership,SyncRun,ExtractionJob,IndexAlias,ErrorEnvelope,ProvisioningJob and CacheEntry. Atomic alias switch p.34 vs immutable p.36 (`data:r2:c54:f5`,`data:r2:c57:f3`);ephemeral cache p.16 vs ledger p.53 (`data:r2:c19:f5`,`data:r2:c87:f5`). Also define immutable revision semantics of other DAT-004 derivatives |
| DAT-OQ-005 | DAT-012;SF OQ-003/004/API-G02a/b | General run path p.15 vs case p.83 (`data:r2:c17:f4`,`data:r2:c137:f10`);missing-approval termination p.41 vs wait/failure pp.49/82 and recoverable timeout p.12 (`data:r2:c68:f1`,`data:r2:c79:f1`,`data:r2:c137:f3`,`data:r2:c14:f2`). Define applicable conditions,states,cancel/resume/rework |
| DAT-OQ-006 | DAT-009/013/016;SF OQ-006/API-G04 | Own-high-risk p.11 vs unqualified no self approval p.85 (`data:r2:c12:f5`,`data:r2:c138:f12`);F false is example. Resolve broader scope,roles/Owner/Member/Workspace Admin/approver,review pools/secondary independence/operator predicates |
| DAT-OQ-007 | DAT-010/014/018;SF OQ-008/API-G03 | Define dependency error/job branch,allocation owner/ID/readback/recovery;ordinary200 pp.83 and conditional clauses pp.54–56 coexist (`data:r2:c137:f11`,`data:r2:c90:f4`). Not universal GET jobs |
| DAT-OQ-008 | DAT-008/018;API-G06/07/14 | Complete canonical/event/SSE/job/A2A schemas,trigger/payload ownership,cursor/offset retention;no aliases. Add confirmed signed immutable job tenancy to earlier SF-006/017/API-048/053 as distinct p.22 obligation `data:r2:c32:f2`;schema/signature/verification open |
| DAT-OQ-009 | DAT-005/009;API-048/SF-017 | Preserve exact RLS/pool reset and choose additional FK OR controlled-write membership enforcement only by decision,p.86 `data:r2:c138:f26`–`data:r2:c138:f28`;define context/reset/bypass/errors |
| DAT-OQ-010 | DAT-006/010;SF OQ-011/API-G11 | Define close/reopen edge/actor/status,reason/label catalogs,priority formula/calendar,revision/idempotency encoding/fingerprint/expiry. Retain24-hour outcome scope and immutable closure lineage |
| DAT-OQ-011 | DAT-007/011;SF OQ-010/013/API-G08/09 | Complete MIME/MB/parser/decompression/OCR/quality/page/bbox/hash/version schemas,quarantine recovery,capabilities/cursors/reauth/running-job effects/backoff/quota/readiness. Preserve low-quality exception/current ACL |
| DAT-OQ-012 | DAT-007/012/018;SF OQ-018/API-G10 | A2A full schemas/grants/decline/deadline and illustrative case_demo vs MCP UUID/omitted output schema pp.41/87 (`data:r2:c67:f5`,`data:r2:c139:f9`,`data:r2:c139:f10`);no typed exception. Complete Citation/EvidenceSet/ID mappings,retrieval/model budgets and unsupported branches |
| DAT-OQ-013 | DAT-013;API-G12 | Review field/hash/rationale schemas,SLA/override,new-revision/publication invoker/endpoint/error/atomic participants. Artifact/source-revision SHA-256 equivalence not established |
| DAT-OQ-014 | DAT-015/016;SF OQ-017/020/API-G16/20 | Earlier crypto sections must explicitly retain managed-identity vault and policy-driven rotation/no bulk request-path re-encryption,p.63 `data:r2:c104:f5`–`data:r2:c104:f6`;not service-credential rotation. Define algorithms/hierarchy/intervals/permissions/isolation tradeoff;no selection |
| DAT-OQ-015 | DAT-010/016;SF OQ-012/017/API-G13 | Immutable closure lineage vs eligible retention/holds/independent audit;tenant receipts/event versus workspace paths pp.26/66/83/85/87/89. Define legal-hold lifecycle,permitted purge,approval binding,manifests/checksums/download/status/partial receipts;no scope equivalence |
| DAT-OQ-016 | DAT-006/008;API-G01/06 | `actor`/`at` vs `actor_id`/`occurred_at`;`reason` vs rationale;`watermark` vs high-watermark;`rule_version` vs rule-set/`policy_version`;parser/pipeline/hash and document-version target key mappings remain open,p.85 `data:r2:c138:f5`–`data:r2:c138:f19` |
| DAT-OQ-017 | DAT-017/018;SF OQ-015/API-G17 | Within300ms p.12 vs under300ms p.65 (`data:r2:c14:f1`,`data:r2:c109:f1`);define equality/load/measurement,cost/metric formulas,windows/sampling,reference capacity versus admission limits,retry/circuit/recovery thresholds |
| DAT-OQ-018 | DAT-017/019;SF OQ-019/021/API-G18/19 | Complete fixture/corpus/seed/signature/report/statistical contracts,SEC/T mappings,release/canary/readability/sign-off/reconstruction and operational incident/probe evidence. No passed-test claims |
| DAT-OQ-019 | DAT-018;SF OQ-009/API-G15 | Snake-case prose p.54 vs explicit uppercase pp.38/84/89;preserve literals and amend convention,not error identifiers |
| DAT-OQ-020 | DAT-004/018;SF-005/OQ-001 | Preserve all formal eight-screen names and figure title/selection discrepancies;define routes/actions/field data sources without alias inference. Display examples never determine physical types/defaults |
| DAT-OQ-021 | DAT-017/018;SF OQ-020/API-G20 | Before implementation lock record dated cloud region/search/identity/model/corporate retention/connector-permission selections,p.90 `data:r2:c142:f14`;before enterprise GA resolve key isolation/rotation throughput,p.10 `data:r2:c8:f7`. Terraform/Bicep,BFF/webhooks unselected |

**Prior-stage amendment notes:** retain API-G22's addition of `CaseStateChanged`, `ConnectorSyncStarted` and scoped `Idempotency-Key` to SF-017/SF-006. Add distinct signed immutable job tenant identity and encryption-key lifecycle obligations as above; do not rewrite completed files or pretend they already contain these clarifications. [pp.22,26,29,54,63; `data:r2:c32:f2`,`data:r2:c39:f8`,`data:r2:c45:f8`,`data:r2:c90:f5`,`data:r2:c104:f5`–`data:r2:c104:f6`]

**Dependencies:** exception handling, integration, security/workflow, architecture and executable verification refinements are **To be defined in a later stage**. Stage8 will consolidate unresolved decisions from completed Markdown into `08_architecture_decision.md`, linking DAT IDs and earlier SF/API IDs. It is not generated here; no owner, deadline or approval is invented.
