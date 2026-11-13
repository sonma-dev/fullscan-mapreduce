# 4. Batch Function Specification

## Batch Inventory and Triggers

### Specification Basis and Status

| Item | Definition |
|---|---|
| Specification file | `04_batch_functions.md` |
| Source document | `1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Source baseline | `OD-AI-DDS-001`, release `R1.0`, design revision `1.3` |
| Completed preceding specifications | [`01_screen_functions.md`](01_screen_functions.md), [`02_api.md`](02_api.md), [`03_data.md`](03_data.md) |
| Scope | Source-supported asynchronous application functions, scheduled processing, bounded backfills, recovery processing, and supporting platform workflows. |
| Identifier convention | `BAT-001`–`BAT-026` identify logical processing functions. `BAT-COM-xxx`, `BAT-OPS-xxx`, `AC-BAT-xxx`, `CON-BAT-xxx`, and `OQ-BAT-xxx` identify shared requirements, operational requirements, acceptance criteria, conflicts, and unresolved contracts. |
| Identifier interpretation | The source supplies no individual batch-job IDs. These identifiers do not establish executable names, deployment units, queue names, or scheduler entries. Existing source component, event, API, and data identifiers are preserved. |
| Citation convention | `[DDS]` identifies the source filename above. Citations use original PDF page numbers and sections. |

[DDS]: 1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf

The following statuses apply:

- **Confirmed:** The source establishes the processing function, condition, constraint, event, or outcome.
- **Needs confirmation:** An implementation contract, operational setting, or deployment decision is absent or conflicting.
- **Proposal:** An explicitly labeled, unapproved design suggestion.
- **NC:** Table abbreviation for **Needs confirmation**.

**BAT-COM-001 — Logical functions versus executable jobs.** Batch/background processing is explicitly required. The source describes asynchronous classification, extraction, indexing, AI workflows, retention jobs, reconciliation workers, and bounded operator replay. The function inventory below preserves that behavior. Whether functions share an executable, worker pool, timer service, provider-managed facility, or deployment unit remains **Needs confirmation**. No independent executable is confirmed merely by assigning a `BAT` identifier.

**Sources:** [DDS], p. 12, §2.2.1; p. 19, §4.2.1; p. 26, §6.3.2; pp. 48–50, Chapter 13; pp. 78–80, Chapter 22.  
**Earlier trace:** `API-PROC-002`–`API-PROC-017`; `DAT-LC-001`–`DAT-LC-012`.

### Scope Boundaries

| Area | Treatment and reason |
|---|---|
| Event-driven and request-triggered background processing | **Confirmed.** Includes accepted ingestion, synchronization, AI runs, evaluations, export, deletion, and replay. A scheduled batch is not the only execution model. [DDS], pp. 12, 27–32, 40–50, 74–80, 83. |
| Timer-driven review expiry, audit export, daily rollups, and rotation | **Confirmed behavior; executable realization NC.** The source does not select a scheduler or require a separate application job for each function. [DDS], pp. 45, 62–66. |
| CI/CD, migration, backup, and incident recovery workflows | **Confirmed supporting processing; platform implementation NC.** These are identified separately from ordinary application workers. [DDS], pp. 19–20, 52, 69–73, 89. |
| Physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing, administrative cloud permissions for agents | **Out of scope.** Explicit system exclusions. [DDS], p. 9, §1.2.1. |
| Application-hosted GPU inference | **Out of scope for the R1 execution profile.** Inference providers are external dependencies. [DDS], p. 19, §4.2.1. |
| Cross-region active/active mutation, OCR beyond English, customer-managed model weights | **Deferred from this baseline.** No corresponding R1 processing job is authorized. [DDS], p. 10, §1.3.2. |
| Undescribed nightly jobs, summary refreshes, automatic closure, bulk business transactions, cancellation, or cleanup jobs | **Needs confirmation**, not out of scope. No such function is created by this specification. |

The illustrated case title `Batch quality deviation` is fictional business content, not evidence of a batch-processing function.  
**Source:** [DDS], p. 7, Reference UI A; p. 14, Figure 2.2.

### Trigger and Time Conventions

**BAT-COM-002 — Scheduling and time.**

1. Durable server times are UTC; public timestamps use RFC 3339.
2. Event producers use UTC and canonical JSON.
3. Workspace timezone and business calendars govern contractual case deadlines.
4. A daily aggregation requirement does not select midnight execution, a reporting-day timezone, or a scheduler timezone.
5. A configured review SLA does not establish a business-calendar SLA or an execution interval for expiry processing.
6. No cron expression, polling interval, maintenance window, holiday rule, missed-run policy, or schedule catch-up policy is supplied.

**Sources:** [DDS], p. 25, §6.3.1; p. 48, §13.1.1; p. 54, §15.1.1; p. 59, §16.3.2; p. 65, §18.3.1.  
**Needs confirmation — OQ-BAT-001:** Define scheduler ownership, execution times, timezone, DST behavior, missed-trigger handling, and reporting-day boundaries for each affected function.

The inventory uses these time profiles:

| Profile | Meaning |
|---|---|
| **E** | Event/request driven. Durable event and processing timestamps use UTC. No calendar execution schedule is supplied. |
| **T** | Deadline or retention driven. Durable timestamps use UTC; timer mechanism, eligibility boundary, and execution cadence are NC. |
| **D** | Daily aggregation is confirmed. Reporting-day boundary, scheduler timezone, and execution time are NC. |
| **P** | Policy/platform driven. Schedule or exact trigger is NC unless explicitly described. Durable timestamps remain UTC. |

### Function Inventory

“Manual execution” identifies only a source-confirmed initiation path or operational action. It does not confirm a screen, command-line interface, or standalone rerun endpoint.

| Job ID | Logical name / source terminology | Purpose | Executing actor or component | Trigger / schedule | Time | Manual execution | Status and source |
|---|---|---|---|---|---|---|---|
| BAT-001 | Asynchronous case classification / Triage Agent | Attach policy-aware labels, confidences, and provenance to a created case. | Classifier; Triage Agent responsibility confirmed. Exact workload identity NC. | `CaseCreated` → run classifier. | E | Case creation through API-001; independent classifier launch/rerun NC. | **Confirmed.** [DDS], p. 12, §2.2.1; p. 40, §11.1.1; p. 87, §C.1. |
| BAT-002 | Incremental connector synchronization / `SyncRun` | Ingest repository changes while preserving source identity, ACLs, and history. | Connector workers; Admin initiates API-018. | Accepted `POST /v1/connectors/{connectorId}/sync`; `ConnectorSyncStarted` is source-named. Automatic schedule NC. | E | API-018, returning `202`; SCR-006-A02. | **Confirmed.** [DDS], pp. 27–29; p. 83, §A.2. |
| BAT-003 | Document extraction and normalization / `ExtractionJob` | Convert allowed sources into immutable text, layout, metadata, and anchors. | Ingestion Service; extraction workers. | Accepted API-006 ingestion or connector-delivered document. Exact queued envelope NC. | E | Upload through API-006; side-by-side reprocessing supported, initiation contract NC. | **Confirmed.** [DDS], pp. 30–32. |
| BAT-004 | Embedding and index commit / Indexer | Build searchable keyword/vector derivatives from normalized versions. | Indexer; embedding workers. | `DocumentNormalized` → build index. | E | No standalone index-build endpoint confirmed; controlled replay under BAT-012 is supported. | **Confirmed.** [DDS], p. 19, §4.2.1; p. 34, §9.1; p. 87, §C.1. |
| BAT-005 | Parallel search-index rebuild | Rebuild a derivative generation and switch the read alias safely. | Indexing responsibility; exact executor NC. | Rebuild operation confirmed; initiating event/API/schedule NC. | P | Rebuild recipes exist; operator launch contract NC. | **Confirmed behavior; launch NC.** [DDS], p. 34, §9.1.2; p. 69, §19.3.1. |
| BAT-006 | Source-access/delete propagation and query-cache invalidation | Enforce revoked access, suppress deleted sources, and invalidate stale results. | Connector, index, and cache-processing responsibilities; exact division NC. | Source ACL/delete change; authorization change; `SearchIndexCommitted` → invalidate query cache. | E | Scoped ACL replay is supported during an incident; exact control NC. | **Confirmed.** [DDS], p. 28, §7.2.2; p. 53, §14.3.2; p. 79, §22.2.2; p. 87. |
| BAT-007 | Durable bounded AI workflow / `AgentRun` | Retrieve evidence, generate a candidate, evaluate policy, and route required review. | Orchestrator; Research Agent; Draft Agent; deterministic Policy Evaluator; Model Gateway. | Accepted API-011; alternate API-012 unresolved. `AgentPlanApproved` dispatches plan steps; `WorkflowStageAdvanced` resumes consumers. | E | Analyst requests API-011, returning `202`; SCR-002-A07. | **Confirmed.** [DDS], pp. 12, 37–42, 49, 58, 83. |
| BAT-008 | Publication validation consumer / `PublicationGate` | Validate the exact artifact and current evidence before atomically publishing. | Policy Service produces decision event; exact publication consumer identity NC. | `ApprovalDecisionRecorded` → validate publication. Automatic-allow path NC. | E | Public Publish action/API not confirmed. | **Confirmed.** [DDS], pp. 44–46; p. 87, §C.1. |
| BAT-009 | Review-task expiry, reassignment, and escalation | Apply configured expiry without implicit approval. | Review/policy processing responsibility; timer executor NC. | Task reaches configured SLA. Timer versus scan mechanism NC. | T | Independent manual expiry/reassignment API NC. | **Confirmed behavior; job mechanism NC.** [DDS], p. 45, §12.2.1; p. 89, `TST-010`. |
| BAT-010 | Outbox publication and durable consumer dispatch | Publish committed events and safely dispatch/resume consumers. | Platform messaging responsibility; business producers and scoped consumers. | Committed outbox/saga work; delivery is at least once. Polling/push arrangement NC. | E | No generic publisher launch API confirmed; bounded recovery uses BAT-012. | **Confirmed processing pattern.** [DDS], pp. 15–17, 48–52. |
| BAT-011 | Source/index and message-link reconciliation | Repair failed derivative writes and broken message links without undoing accepted source metadata. | Reconciliation worker; outbox repair responsibility. | Failed index write or broken message link. Detection cadence NC. | E | Delayed-indexing runbook supports operator investigation/recovery. | **Confirmed.** [DDS], p. 49, §13.2.2; p. 90, §F.1. |
| BAT-012 | Bounded operator replay / dead-letter recovery | Replay validated scoped records with reason and provenance controls. | Authorized operator and protected replay processing identity. | API-038; validated outbox replay under §F.1. | E | `POST /internal/deadletters/{id}/replay`; reason, dry-run validation, scope limit. | **Confirmed.** [DDS], p. 50, §13.3.2; p. 90, §F.1. |
| BAT-013 | Eligible closed-case retention and tombstone purge | Retain/purge eligible closed-case data while enforcing holds and deletion controls. | Retention processing; exact executor for every purge target NC. | Retention eligibility; scheduled tombstone pipeline. Exact schedule NC. | T | API-040 is a protected purge surface; exact launch scope and response mode NC. | **Confirmed.** [DDS], p. 26, §6.3.2; pp. 51–53. |
| BAT-014 | Diagnostic and security-audit retention purge | Apply distinct diagnostic/audit policies and retain purge/hold evidence. | Telemetry/audit retention responsibility; provider-managed versus application executor NC. | Retention policy/TTL eligibility. Exact execution schedule NC. | T | No dedicated manual diagnostic/audit purge API confirmed. | **Confirmed behavior; mechanism NC.** [DDS], p. 66, §18.3.2. |
| BAT-015 | Audit batch-hash chaining and independent export | Preserve tamper-evident append-only audit evidence outside ordinary operational control. | Audit processing responsibility; exact export identity NC. | Audit batches and retention export; batch boundary/cadence NC. | P | No dedicated audit-export launch API confirmed. | **Confirmed behavior; mechanism NC.** [DDS], p. 62, §17.3.1; p. 88, `T-09`. |
| BAT-016 | Daily usage and cost rollups | Produce attributed budget, forecast, usage, and rejected-excess reporting. | Usage/FinOps processing responsibility; exact rollup executor NC. | Daily aggregation confirmed; execution schedule NC. | D | No rollup execution/rerun API confirmed; API-022 reads results. | **Confirmed aggregation; mechanism NC.** [DDS], p. 65, §18.3.1. |
| BAT-017 | Frozen benchmark evaluation / AI evaluation harness | Produce quality, safety, statistical, and release-gate evidence. | Evaluation harness; Admin initiates API-023. | Accepted API-023; prompt/model changes require reevaluation. | E | `POST /v1/evaluations`, returning `202`; SCR-011-A01 placement remains proposed. | **Confirmed.** [DDS], pp. 74–76, 83, 88–89. |
| BAT-018 | Idempotent tenant/workspace provisioning / `ProvisioningJob` | Establish policy, encryption references, roles, quotas, and connector stubs. | Provisioning responsibility; executor and initiating role NC. | Provisioning request/workflow; entry API/event/schedule NC. | E | Provisioning capability confirmed; launch interface NC. | **Confirmed.** [DDS], p. 78, §22.1.1. |
| BAT-019 | Historic source backfill and batch reconciliation | Ingest historical documents in bounded windows using stable source IDs. | Onboarding/backfill processing responsibility; exact executor NC. | Initial data onboarding/backfill. Window selection and launch NC. | E | Operational backfill supported; command/API NC. | **Confirmed.** [DDS], p. 78, §22.1.2. |
| BAT-020 | Controlled workspace export / `ExportManifest` | Package authorized exit data with manifest/checksums and exclusions. | Export processing identity NC; `Admin + approver` initiates. | Accepted API-025 after independent approval checks. | E | `POST /v1/workspaces/{workspaceId}/export`, returning `202`; no screen placement confirmed. | **Confirmed.** [DDS], pp. 78–80, 83. |
| BAT-021 | Verified workspace deletion / Retention Worker | Tombstone and remove eligible data, preserve holds, and record verified receipts. | Retention Worker produces `TenantDeletionVerified`; complete worker division NC. | Accepted API-026; verification event closes purge record. | E | `POST /v1/workspaces/{workspaceId}/delete`, returning `202`. | **Confirmed.** [DDS], pp. 78–80, 83, 87, 89. |
| BAT-022 | Database migration backfill and constraint enforcement / `MigrationPlan` | Perform compatible bounded data migration before final enforcement. | Deployment/migration pipeline; exact workload identity NC. | Controlled schema rollout: expand, bounded backfill, postdeployment enforcement. | P | Protected release/migration workflow; standalone migration API/command NC. | **Confirmed.** [DDS], p. 52, §14.2.2; p. 72, §20.2.2. |
| BAT-023 | Continuous backup, incident restore, and recovery validation | Recover relational/object consistency and rebuild search under incident control. | Backup facilities; restore under incident command; exact provider/identity NC. | Continuous PostgreSQL backup; incident restore; DR exercises. Exercise schedule NC. | P | Secondary snapshots restored only under incident command. | **Confirmed platform behavior.** [DDS], p. 19, §4.2.2; pp. 69–70; p. 89. |
| BAT-024 | Policy-based service-secret and encryption-key rotation | Rotate credentials/keys without disclosing secrets or requiring request-path bulk reencryption. | Identity/vault/key-management responsibility; exact implementation NC. | Automatic service credential rotation; defined encryption-key policy. Schedule NC. | P | Manual rotation or background reencryption requirement NC. | **Confirmed behavior; application-job realization NC.** [DDS], p. 21, §5.1.2; p. 63, §17.3.2. |
| BAT-025 | Optional signed outbound webhook delivery | Deliver external notifications independently of accepted case transactions. | Notification producer/delivery processing; recipient verifies signature and age. | Optional subscribed notification; retry with exponential backoff. Exact event mapping NC. | E | Subscription and manual redelivery interfaces NC. | **Confirmed optional capability.** [DDS], p. 55, §15.2.2. |
| BAT-026 | Build, verification, and controlled release workflow | Produce attested artifacts, execute release tests, canary, and promote or roll back traffic. | CI/deployment pipeline; Security and SRE sign-off responsibilities. | Controlled build/release; API-043 exists. Exact pipeline trigger NC. | P | `POST /internal/releases`; exact operator/build grants and response mode NC. | **Confirmed platform workflow.** [DDS], pp. 71–73, 88–89. |

**Needs confirmation — OQ-BAT-003:** Map every executor to a distinct workload identity, allowed service audience, resource grants, and operator role. `Service`, `Admin`, or internal-network location alone does not grant universal execution rights.  
**Earlier:** `OQ-API-002/027/028`; `OQ-DAT-001/017`.

### Predecessors, Successors, and Prerequisites

Dependencies below are logical evidence/data dependencies, not a selected scheduler DAG. Conditional successors must not be launched automatically unless the source-established condition applies.

| Job | Predecessor or required data | Conditional successor / consumer | Prerequisites and unresolved dependency |
|---|---|---|---|
| BAT-001 | Committed case creation and `CaseCreated` from Case Service. | Case work and later BAT-007 may use classification; exact dependency on classification completion NC. | Authorized case/revision, policy-aware classification contract. |
| BAT-002 | Completed provisioning under BAT-018. | BAT-003 for fetched sources; BAT-006 for ACL/delete changes. | Configured repository, capability advertisement, workspace credentials, authorized connector, quotas. |
| BAT-003 | Accepted attachment, BAT-002 source, or BAT-019 historic source. | BAT-004 via `DocumentNormalized` for normalized material eligible for indexing. | Allowed file, type/size validation, scan, bounded parser, pipeline version, scoped object access. |
| BAT-004 | Immutable normalized document version and anchors. | BAT-006 via `SearchIndexCommitted`; retrieval may use committed derivatives. | Tenant/workspace scope, versioned index target, compatible embedding contract, source ACL. |
| BAT-005 | Authoritative source inventory and rebuild recipe. | BAT-006 cache invalidation after source-confirmed index commit; exact rebuild event mapping NC. | Parallel generation, completeness/recall checks, current source authorization. |
| BAT-006 | Detected ACL/delete/authorization change or committed index event. | Safe next retrieval; deletion may enter BAT-013 tombstone pipeline. | Revocation before next retrieval; no soft-deleted resource retrieval. |
| BAT-007 | Authorized case, input, deployment policy, token budget, admission capacity, permitted evidence. | BAT-008 when publication validation is required; BAT-009 for issued review tasks. | Valid bounded plan, narrow authorized tools, checkpoints, deterministic policy. |
| BAT-008 | Exact candidate, policy/evidence records, applicable accepted review decision. | Published run/case projection; BAT-025 only if subscribed event mapping is resolved. | Exact reviewed hash, current authorization/evidence, satisfied gate. |
| BAT-009 | Valid task with configured expiry and routing policy. | Reassignment/escalation; no automatic BAT-008 publication. | Task validity, role and separation-of-duty constraints; race behavior NC. |
| BAT-010 | Committed outbox or reconciled saga records. | Source-catalogued consumers, including BAT-001/004/006/007/008/021. | Versioned signed tenant context, deduplication and revision checks. |
| BAT-011 | Durable source metadata, index fingerprints, outbox ledger, identified mismatch. | BAT-004 or BAT-010 repair/retry as applicable. | Bounded safe repair; exact automatic/manual boundary NC. |
| BAT-012 | Selected dead letter or validated outbox records; diagnostic evidence. | Original authorized consumer and BAT-011 verification. | Operator reason, dry run, scope limit; migration provenance when schema transforms. |
| BAT-013 | Eligible closed cases or eligible tombstoned targets. | Verified purge/receipt processing; relation to BAT-021 NC. | Retention policy, legal holds, protected lineage, authorized inventory. |
| BAT-014 | Diagnostic/audit records reaching their distinct policy eligibility. | Purge receipts and hold exceptions. | Approved policy precedence; no conflation of diagnostics and audit. |
| BAT-015 | Append-only audit entries. | Independent retention storage; BAT-020 may include audit manifests. | Defined hash-chain/batch/export contract and authorized destination. |
| BAT-016 | Attributed model, embedding, storage, indexing, and rejected-request usage. | API-022 usage reporting. | Reporting window, quota/budget context, cost centers and deployment versions. |
| BAT-017 | Frozen versioned corpus, expected outcomes, actual prompt/model versions. | BAT-026 release gates. | Signed manifest, independent fixture review, statistical/domain contracts. |
| BAT-018 | Authorized provisioning input/configuration. | BAT-002; BAT-019 onboarding. | Idempotent resource establishment; incomplete state blocks sync. |
| BAT-019 | Configured historical source and onboarding scope. | BAT-003/004; coverage/reconciliation evidence. | Stable source IDs, bounded windows, per-batch receipts. |
| BAT-020 | Authorized workspace inventory and two independent approval checks. | Authorized export recipient; no deletion successor is implied. | Export scope and manifest; secrets/internal prompts excluded. |
| BAT-021 | Authorized workspace deletion inventory and two independent approval checks. | Blob/index removal and purge processing; `TenantDeletionVerified` consumer closes purge record. | Legal holds, tombstones, completion receipts. Whether BAT-013 shares execution NC. |
| BAT-022 | Backward-compatible schema expansion and controlled migration plan. | Constraint enforcement after backfill and old-reader drainage; BAT-026 release completion. | Active-reader compatibility and explicit readable-write rollback plan. |
| BAT-023 | Valid backup/object versions and search rebuild recipes. | BAT-005 when index rebuilding is needed for recovery. | Incident command for restore, consistency verification, approved recovery region. |
| BAT-024 | Approved rotation policy and vault-backed references. | Continued authorized service/object access. | Managed identity where supported; key isolation/rotation design unresolved. |
| BAT-025 | Accepted internal event and optional authorized subscription. | External recipient. | Signature and event-age verification contract; delivery failure cannot undo case state. |
| BAT-026 | Source/build/configuration artifacts; required test evidence, BAT-017 and applicable BAT-022. | Approved deployment/release record; rollback on regression. | Allowed build identity; Security/SRE validation; critical safety acceptance. |

**Sources:** [DDS], pp. 12, 19, 26–42, 44–55, 62–66, 69–80, 87–90.

**Needs confirmation — OQ-BAT-004:** Resolve dependency dispatch, overlapping launches, resource-specific exclusion, and shared versus separate executable boundaries. The table does not authorize a global serial pipeline.

## Processing by Job

### Shared Argument and Input Contracts

**BAT-COM-003 — Arguments are not invented wire fields.** The tables below use exact names only where provided by the source/API/data specifications. Other entries describe necessary logical inputs; their runtime argument names, transport, required-property schema, lengths, nullability, and defaults remain **Needs confirmation**.

| Argument / context | Meaning and confirmed constraints | Type / carrier | Trace |
|---|---|---|---|
| `tenant_id` | Required trusted scope; immutable in signed background envelopes; part of every storage predicate. | `UUID` in case DDL; complete job representation NC. | `DAT-COM-F01`; `DAT-EVT-F04`; API authentication/event profiles. |
| Resource identity | Applicable case, connector, run, task, document version, workspace, inventory, or release target. | Application UUIDv7 baseline; exact path-to-job mappings NC. External IDs/cursors are not automatically UUIDs. | API shared parameters; `DAT-COM-004`. |
| `revision` / `aggregate_revision` | Applicable stale-write/delivery guard. | Case `BIGINT`; full job/event encoding NC. | `DAT-COM-F02`; `DAT-EVT-F06`. |
| `actor_id`, actor/reviewer attribution | Authenticated initiating actor or authorized processing attribution at durable changes. | Trusted context; physical/envelope alias mapping NC. | `DAT-COM-F03`; `API-PROC-001`. |
| `occurred_at` | Durable occurrence time. | UTC; public RFC 3339. Precision and time authority NC. | `DAT-COM-F04`; `DAT-EVT-F07`. |
| `trace_id`, `correlation_id` | Cross-boundary diagnostic linkage; independent of provider trace identifiers. | Transport, lengths, and persisted carriers NC. | `DAT-COM-F05`; `API-COM-006`. |
| `event_id`, `type`, `schema_version`, `aggregate_id`, `payload` | Required versioned event identity/content. | Exact field names confirmed; complete scalar/payload schemas NC. | `DAT-EVT-F01`–`F09`; `API-COM-006`. |
| `Idempotency-Key` / operation key | Required for POST mutations creating long-running jobs; mutable tools require idempotency. | Public header named; internal key carrier/schema NC. | `API-PROC-018`; `DAT-026-F01/F02`. |
| Versioned policy/configuration | Governs routing, quotas, retention, tools, quality, and reviewer requirements. | Reference/configuration schemas and precedence NC. | DAT-002/017/024/032. |
| Bound/deadline/window | Source requires bounded plans, retries, replay, and backfill where identified. | Exact numeric settings NC except independently confirmed limits. | `API-PROC-021`–`029`; DAT-008/026/029/032. |

**Sources:** [DDS], pp. 15–17, 22, 25, 40–42, 48–56, 71, 78, 85–87.

**Needs confirmation — OQ-BAT-002:** Supply repository-controlled job/envelope schemas, allowed arguments, extraction predicates, defaults, and result contracts.  
**Needs confirmation — OQ-BAT-006:** Define event/operation-key namespaces, fingerprints, ledger retention, pending duplicate handling, and result reconstruction. Actor/correlation attribution is required but its relationship to the enumerated event envelope remains unresolved.

### BAT-001 — Asynchronous Case Classification

<a id="bat-001"></a>

**Status:** Confirmed asynchronous function. Exact classifier executable, version schema, and mutation contract are NC.  
**Sources:** [DDS], p. 12, §2.2.1; p. 40, §11.1.1; p. 87, §C.1.

| Contract category | Definition |
|---|---|
| Arguments | `CaseCreated` envelope and case ID/revision concepts; exact payload keys NC. |
| Inputs and extraction | Created tenant-scoped case and submitted business context. Attachment inclusion and readiness dependency NC. |
| Transformation | Policy-aware classification produces labels, confidences, and provenance. The Triage Agent classifies cases. |
| Update targets | DAT-003 case context and DAT-020 classification data; physical classification fields are unresolved. |
| Outputs | Attached classification result; no separate classification-completed event or result schema is supplied. |
| Successful completion | Accepted result is associated with the correct case/version and preserves provenance. Completion does not itself establish publication authorization. |
| Related contracts | API-001; API-GAP-001; `API-CASE-F16/F17`; `DAT-020-F02/F03`; SCR-002-F14–F17. |

**Procedure:**

1. Validate the event, trusted tenant scope, target case, and applicable revision.
2. Apply duplicate/stale-delivery controls.
3. Obtain authorized case context through the appropriate scoped boundary.
4. Perform policy-aware classification.
5. Persist labels, confidences, provenance, and required durable attribution.
6. Preserve the separate user-correction requirement: correcting a label requires a reason code.

**Needs confirmation — OQ-BAT-010:** Define attachment dependencies, classifier/model version, labels and confidence scale, stale-result handling, correction-versus-job races, retryable classification failures, and completion status. Do not overwrite a later user correction through an unresolved rerun policy.

### BAT-002 — Incremental Connector Synchronization

<a id="bat-002"></a>

**Sources:** [DDS], pp. 27–29, §§7.1–7.3; p. 83, §A.2.

| Contract category | Definition |
|---|---|
| Arguments | API-018 `connectorId`, authorized workspace/tenant context, job idempotency, configured credential reference. Optional sync arguments NC. |
| Inputs and extraction | Configured repository capability metadata, provider listing/delta results, source IDs, ACL/delete changes, stored cursor and high-watermark. Provider selection/query schema NC. |
| Update targets | DAT-021 `Connector`/`SyncRun`; DAT-015 `connector_cursors`; DAT-005/006 source/version records; deletion/ACL targets under BAT-006. |
| Confirmed fields | `connector_id`, `cursor`, `watermark`, `retry_state`; per-run error ledger; quarantine reason, correlation ID, remediation path. |
| Outputs | Durable sync outcomes and cursor ledger; `ConnectorSyncStarted` evidence. API-019 reads run history. |
| Successful completion | Preceding items have durable ingestion outcomes before cursor advancement. Recorded quarantine exceptions remain visible; an exceptional batch is not represented as wholly synchronized without exceptions. |
| Related contracts | API-018/019/049; `API-PROC-007/025`; DAT-015/021; SCR-006. |

**Procedure:**

1. Validate Admin/resource authorization, idempotency, and completed provisioning.
2. Resolve workspace-scoped credentials. Revoked queued credentials produce `CONNECTOR_REAUTH_REQUIRED` without token disclosure.
3. Discover list, fetch, delta-cursor, ACL, and delete support.
4. Surface explicit lower-trust warnings for unsupported capabilities; do not silently assume support.
5. Obtain the stored provider cursor/high-watermark and fetch changes under provider throttling and workspace quotas.
6. Preserve stable source identity, permissions, and change history.
7. Send fetched sources through BAT-003; apply ACL/delete propagation through BAT-006.
8. Store per-item durable outcomes and the run error ledger.
9. Advance the cursor only after all preceding items have durable outcomes.
10. After bounded malformed-record retries, quarantine the record with reason, correlation ID, and remediation path. The remaining batch may proceed with the exception recorded.

**Needs confirmation — OQ-BAT-011:** Provider capabilities/permissions, cursor ordering and expiration, initial cursor, batch limits, sync states, lower-trust restrictions, parallel sync ownership, retry bounds, and empty-delta completion are unresolved. Missing ACL capability cannot waive revocation-before-next-retrieval.

### BAT-003 — Document Extraction and Normalization

<a id="bat-003"></a>

**Sources:** [DDS], pp. 30–32, §§8.1–8.3; p. 62, §17.2.2.

| Contract category | Definition |
|---|---|
| Arguments | Accepted document/source reference, tenant/workspace/case association as applicable, pipeline/parser version, OCR opt-in context. Exact queued fields NC. |
| Inputs and extraction | PDF, DOCX, HTML, or UTF-8 text with agreeing MIME signature/extension; configurable 25 MB per-file cap; decompression-bomb threshold. Exact byte boundary and threshold NC. |
| Transformation | Scan; layout-aware extraction; segmentation; normalization without rewriting claims; immutable derivative versioning; quality and likely-personal-data tagging. |
| Update targets | DAT-005–007/020/022/028; `document_versions.document_id/hash/parser_version/object_key`; `chunks.id/document_version_id/page/bbox/text_hash`. |
| Outputs | Immutable text/layout/metadata and resolvable anchors; quality/OCR provenance; `DocumentNormalized` carrying version ID/source hash concepts. |
| Successful completion | Safe normalized derivatives and provenance are durable. Unsafe material never enters the index. Document readiness depends on applicable downstream scan/index/quality state, not solely extraction completion. |
| Related contracts | API-006/007/039; `API-PROC-003`; DAT-FILE-001/002; DAT-CODE-003. |

**Procedure:**

1. Validate file category, MIME/extension agreement, configured size, and decompression controls.
2. Scan before parsing. Disable macro execution and do not fetch embedded remote references.
3. Quarantine unsafe content without indexing.
4. Parse PDF pages into blocks with page index/bounding boxes; preserve table row/column annotations, headings, and reading order.
5. Use OCR fallback only through opt-in configuration and mark its provenance. OCR beyond English is deferred.
6. Normalize transport artifacts without rewriting source claims.
7. Produce immutable derivative identity from content fingerprint plus pipeline version; support side-by-side reprocessing.
8. Store source URI, file hash, page number, and optional bounding box for every chunk.
9. Record empty-page ratio, unknown-character ratio, table-loss indicators, language confidence, and likely-personal-data tags.
10. Make low-quality material viewable under authorization but exclude it from autonomous recommendations.
11. Persist normalized output and dispatch the supported index-build event through durable messaging.

**Needs confirmation — OQ-BAT-012:** Exact format allowlist, parser limits, malformed-versus-unsafe handling, OCR default/carrier, quality thresholds, file/object serialization, commit coordination, extraction retry bounds, and no-text outcomes. Low-quality viewing does not authorize rendering quarantined active content.

### BAT-004 — Embedding and Index Commit

<a id="bat-004"></a>

**Sources:** [DDS], p. 19, §4.2.1; p. 34, §9.1; p. 87, §C.1.

| Contract category | Definition |
|---|---|
| Arguments | `DocumentNormalized` envelope; version ID/source hash concepts; target index generation/alias and scoped version context. Exact field schema NC. |
| Inputs and extraction | Immutable normalized chunks and associated source identity, language, classification, and ACL context. Unsafe quarantined material is excluded. |
| Transformation | Build normalized keyword text and compatible embeddings; write a nonauthoritative search derivative using versioned aliases. |
| Update targets | DAT-023 search rows/aliases; source metadata remains authoritative. |
| Required row content | `tenant_id`, `workspace_id`, `document_version_id`, `chunk_id`, language, classification, 1536-dimensional embedding, normalized keyword text. |
| Outputs | `SearchIndexCommitted` with index generation/document revision concepts; query-cache invalidation consumer. |
| Successful completion | Intended derivative writes are committed under the resolved index contract and source/version identity is preserved. Failed writes require reconciliation rather than rollback of accepted source metadata. |
| Related contracts | API-009/010/045 as consumers; `API-PROC-004/019`; `DAT-023-F01`–`F03`. |

**Procedure:**

1. Validate event identity, tenant/version scope, and stale/duplicate delivery.
2. Resolve normalized source/chunks and their permitted indexing context.
3. Produce keyword/vector derivative content compatible with the confirmed 1536-dimensional representation.
4. Write the selected versioned index target.
5. Record committed index-generation/document-revision evidence.
6. Publish `SearchIndexCommitted` through the durable messaging boundary.
7. Route failed derivative writes to BAT-011; do not undo accepted source metadata.

**Needs confirmation — OQ-BAT-013:** Embedding provider, numeric representation, analyzers, target selection, item/batch commit units, partial-index semantics, completeness checks, index-event schema, and readiness state. The source does not specify an embedding batch size.

### BAT-005 — Parallel Search-Index Rebuild

<a id="bat-005"></a>

**Sources:** [DDS], p. 34, §9.1.2; p. 69, §19.3.1.

| Contract category | Definition |
|---|---|
| Arguments | Authorized rebuild scope, authoritative inventory, target generation, rebuild recipe. Names, defaults, and launch contract NC. |
| Inputs and extraction | Source database metadata and immutable normalized versions/chunks; exact snapshot/selection boundary NC. |
| Update targets | Parallel DAT-023 index generation and read alias; no authority transfer from PostgreSQL to search. |
| Outputs | Rebuilt generation and completeness/recall evidence; atomic alias switch after checks. |
| Successful completion | Parallel index passes completeness and recall checks before atomic read-alias replacement. |
| Related contracts | `API-PROC-019`; DAT-023; `DAT-LC-017`; BAT-004/006/023. |

**Procedure:**

1. Validate the authorized scope and target generation.
2. Create a parallel index without prematurely replacing the current read alias.
3. Build derivatives from authoritative versioned source data.
4. Apply source-access/deletion protections during the rebuild.
5. Execute completeness and recall checks.
6. Switch the read alias atomically only after the required checks pass.

**Needs confirmation — OQ-BAT-013:** Snapshot/catch-up strategy during concurrent source updates, alias exclusion, completeness/recall thresholds, empty inventory, old-generation retention/removal, rerun/resume controls, and rollback of an already-switched alias. No rebuild schedule or public API is supplied.

### BAT-006 — Source-Access/Delete Propagation and Cache Invalidation

<a id="bat-006"></a>

**Sources:** [DDS], p. 28, §7.2.2; p. 53, §14.3.2; p. 79, §22.2.2; p. 87, §C.1.

| Contract category | Definition |
|---|---|
| Arguments | Source ACL/delete revision, authorization-change scope, or `SearchIndexCommitted` envelope. Exact change-event names/payloads NC. |
| Inputs and extraction | Affected source/index/cache records; keys include tenant, user-scope digest, source ACL revision, query hash, index generation. |
| Update targets | DAT-005 ACL/source state; DAT-029 tombstones; DAT-023 index entries/aliases; DAT-027 caches. |
| Outputs | Revoked/deleted content is not served; affected cache invalidation; scheduled source-delete index removal. |
| Successful completion | Revoked access is effective before the next retrieval, and soft-deleted entities are not retrievable. Normal TTL or delayed index removal cannot serve as permission to disclose content. |
| Related contracts | `API-PROC-007/019`; `DAT-LC-017`; SCR-003-A04; SCR-006-A04; `TST-004`. |

**Procedure:**

1. Identify the affected tenant, source, ACL revision, and index/cache scope.
2. Validate the change and apply stale/duplicate controls.
3. For source deletion, create a tombstone and schedule index removal.
4. For ACL/authorization changes, invalidate affected retrieval cache entries before new results are served.
5. Continue enforcing originating source ACLs independently of ranking and index freshness.
6. For `SearchIndexCommitted`, invalidate query caches associated with the committed generation/revision.
7. Treat stale unauthorized visibility as a security incident.

**Needs confirmation — OQ-BAT-013:** Atomic revocation protocol, membership/group propagation, affected-key discovery, changes during retrieval, source-change detection, and safe behavior if a connector cannot advertise ACL support. Authorization propagation is not an ordinary eventual-consistency allowance.

### BAT-007 — Durable Bounded AI Workflow

<a id="bat-007"></a>

**Sources:** [DDS], pp. 12, 34–42, 44–46, 49, 58, 69, 83, 87.

| Contract category | Definition |
|---|---|
| Arguments | API-011 `caseId`, validated analyst input, operation identity, case/run context, approved deployment/tool/policy references, reserved budget. API-012 relationship NC. |
| Inputs and extraction | Authorized case and permitted evidence; source ACLs applied before text release; only resolvable anchors with current access may be cited. |
| Transformation | Bounded retrieval, generation, deterministic policy evaluation, review routing, durable checkpoint progression. |
| Update targets | DAT-008/009/010/016/017/024/025/026; applicable review tasks DAT-011. |
| Confirmed fields | `runs.id/case_id/status/plan_revision/budget`; `run_steps.id/run_id/step_kind/status/checkpoint`; `evidence_sets.id/run_id/chunk_refs/acl_digest`; policy and token fields. |
| Outputs | Candidate, evidence, actual prompt/model versions, policy inputs/result/reasons, checkpoints, review work where required. Source-named events include `AgentPlanApproved`, `WorkflowStageAdvanced`, and `ModelInvocationCompleted`. |
| Successful completion | Grounded publication only after all required evidence/policy/approval controls. Source also requires terminal completion within configured maximum or recoverable timeout; exact timeout representation is unresolved. |
| Related contracts | API-011–015/036/037/045/046/050; `API-PROC-005/008/020`–`029`; DAT-CODE-002/006/007; SCR-004. |

**Procedure:**

1. Validate input, authorization, idempotency, and case scope before allocating work.
2. Admit only when workspace tokens, queue age, and provider capacity satisfy thresholds. Throttled clients receive `429` and `Retry-After`; saved cases remain available.
3. Reserve input/output token budget under the workspace quota.
4. Persist a DAG plan revision before executing side effects. Enforce depth maximum eight, maximum sixteen tool invocations, and explicit dependencies.
5. Dispatch only approved version-pinned tools after argument and separate capability authorization.
6. Retrieve bounded lexical/vector candidates; merge using reciprocal rank fusion, deterministic reranking, diversity, and token budgets.
7. If evidence confidence/quality is insufficient, return `NO_SUPPORTED_EVIDENCE`; clarification or human routing may follow. Do not fabricate context.
8. Select a specific approved model deployment for the maximum included material class. Fallback requires an approved equal-or-stronger data-handling class and approved region/deployment.
9. Construct fixed system rules, signed workflow instruction, validated user input, and separately delimited untrusted evidence. Strip tool-call directives from evidence contexts and record injection indicators.
10. Redact nonessential personal fields before provider invocation where policy permits.
11. Request versioned structured JSON and apply bounded parsing retries. Unknown fields, invalid citations, or control-character injection produce `MODEL_OUTPUT_INVALID`.
12. Track provider usage. Quota exhaustion is terminal for the current run without automatic model/data-class changes.
13. Normalize and store deterministic policy inputs with rule version. Outcomes are `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, or `DENY`; LLM tags cannot override them.
14. Issue policy-routed review where required and retain separate retrieval, generation, policy, and approval records.
15. Persist each stage checkpoint before downstream dispatch. Report the exact failed checkpoint on failure.
16. Validate publication through BAT-008 as applicable.

**Needs confirmation — OQ-BAT-014:** Canonical run endpoint, run/case-revision linkage, call/retry accounting, invalid-plan bound, `AUTO_ALLOW` progression, waiting versus missing approval, timeout accounting during human review, recoverable timeout state, and any cancel/retry/resume control. Appendix F’s `run_timeout_seconds: 180` is not a universal batch timeout or reviewer SLA.

The receiving A2A agent may decline. Input/output schema declarations are required, but the sample omits the output-schema carrier. This remains unresolved under `OQ-API-028` and `OQ-DAT-024`; no new A2A field is selected.

### BAT-008 — Publication Validation Consumer

<a id="bat-008"></a>

**Sources:** [DDS], pp. 44–46, §§12.1–12.3 and §12.5; p. 87, §C.1.

| Contract category | Definition |
|---|---|
| Arguments | `ApprovalDecisionRecorded` envelope; task, actor, content-hash concepts; exact candidate/run/evidence binding. |
| Inputs and extraction | Immutable decision, exact reviewed artifact, policy version/inputs/result, citations and current resource permissions. |
| Update targets | DAT-025 satisfied publication gate; DAT-003 current approved-result pointer; relevant run/publication state and durable evidence. |
| Outputs | Authoritative publication or safely rejected stale/unauthorized outcome. No new publication event/API is invented. |
| Successful completion | Final response pointer and satisfied gate commit in the same transaction; published artifact is exactly the approved content and remains currently authorized. |
| Related contracts | API-017; `API-PROC-006`; API-GAP-006; DAT-011/012/017/025; `DAT-003-F16`; SCR-002-A12. |

**Procedure:**

1. Validate signed tenant/event context, event identity, and aggregate revision.
2. Resolve the exact decision and candidate artifact.
3. Reevaluate current authorization and evidence; reject stale evidence.
4. Validate applicable policy and approval requirements, including separation of duties.
5. Reject a changed artifact under an old approval and audit the stale action.
6. Record the satisfied gate and update the final response pointer atomically.
7. On duplicate delivery, do not create another accepted publication transition or publish different content.

**Needs confirmation — OQ-BAT-015:** Publication consumer identity, transaction/locking protocol, `AUTO_ALLOW` trigger, decision revocation/expiry semantics, multiple decisions, output state/event, and public status projection. A recorded rejection is not permission to run the satisfied-gate branch.

### BAT-009 — Review Expiry, Reassignment, and Escalation

<a id="bat-009"></a>

**Sources:** [DDS], p. 45, §12.2.1; p. 82, §A.1; p. 89, `TST-010`.

| Contract category | Definition |
|---|---|
| Arguments | Target review task and configured SLA/routing context; timer/scan fields NC. |
| Inputs and extraction | Tasks reaching their configured expiry; exact predicate and eligible predecessor states NC. |
| Transformation | Expire and reassign or escalate using policy-defined reviewer pools, minimum role, and separation of duties. |
| Update targets | DAT-011 review state/assignment/expiry data; durable escalation evidence. |
| Outputs | Authoritative expired/reassigned/escalated outcome; no implicit approval. |
| Successful completion | Expiry handled without publication bypass; escalation recorded as required by `TST-010`. |
| Related contracts | API-016/017; `API-PROC-027`; `DAT-011-F03/F05`–`F07`; SCR-005-A06. |

**Procedure:**

1. Resolve the current task, candidate binding, and expiry/routing policy.
2. Recheck task validity and concurrent decisions before a durable state change.
3. Apply the expiry outcome using the resolved transition contract.
4. Reassign or escalate to policy-eligible reviewers.
5. Preserve historical decisions and record escalation evidence.
6. Never treat expiry or an unavailable reviewer as approval.

**Needs confirmation — OQ-BAT-015:** SLA value/unit, expiry clock, task states eligible for expiry, scan interval/timer behavior, late decisions, reassignment identity, retry behavior, and no-expired-task completion.

### BAT-010 — Outbox Publication and Durable Consumer Dispatch

<a id="bat-010"></a>

**Sources:** [DDS], pp. 15–17, §§3.1–3.3; pp. 48–52, §§13.1–13.2 and §14.2.1; p. 87, §C.1.

| Contract category | Definition |
|---|---|
| Arguments | Committed event/operation identities and versioned envelope. Publisher claim/routing arguments NC. |
| Inputs and extraction | Committed `outbox_events` or explicitly reconciled saga work. Physical unpublished/eligible predicate NC. |
| Update targets | DAT-014 outbox publication evidence and DAT-026 consumer event/operation ledgers; target mutation is owned by its scoped consumer. |
| Outputs | At-least-once publication/dispatch and correlated accepted/duplicate outcomes. |
| Successful completion | Durable state change and event publication remain replay/recovery safe; duplicates do not reapply accepted business mutations. |
| Related contracts | `API-COM-006`; `API-PROC-001/018`; `DAT-014-F01`–`F05`; `DAT-026-F02`; DAT-EVT fields. |

**Procedure:**

1. Obtain committed event work under the authorized scope.
2. Validate the mandatory envelope: `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, `payload`.
3. Publish through the declared versioned routing contract; exact broker/topic arrangement is unresolved.
4. At the consumer, validate tenant/resource scope and payload before mutation.
5. Deduplicate event IDs and operation keys; detect stale aggregate revisions.
6. For a duplicate accepted event, record a duplicate outcome and return without reapplying the mutation.
7. Dispatch or resume the source-catalogued action.
8. Use durable checkpoints/outbox or an explicitly reconciled saga step for further state changes.
9. Repair broken message links through BAT-011/BAT-012 as applicable.

**Needs confirmation — OQ-BAT-005/OQ-BAT-006:** Publisher selection/claim protocol, acknowledgment-versus-commit boundary, ledger atomics, stale-event policy, broker topology, poison-event disposition, and outbox retention. No `published_at` column or publisher status enum is confirmed.

### BAT-011 — Reconciliation of Source, Index, and Message Links

<a id="bat-011"></a>

**Sources:** [DDS], p. 49, §13.2.2; p. 90, §F.1.

| Contract category | Definition |
|---|---|
| Arguments | Affected tenant/index generation/source scope and durable event/outbox context. Automatic selection parameters NC. |
| Inputs and extraction | Failed index writes, mismatched source/index fingerprints, broken message links, outbox ledger. Exact mismatch query/schema NC. |
| Transformation | Compare fingerprints, retry derivative writes, and repair links from durable outbox evidence. |
| Update targets | DAT-023 derivative state; DAT-014/026 messaging/checkpoints; accepted source metadata remains intact. |
| Outputs | Reconciled source/index/message consistency and operational evidence. |
| Successful completion | Correct scoped source versions are indexed/relinked and verified without duplicate accepted business changes or ACL leakage. |
| Related contracts | `API-PROC-019`; `DAT-LC-017`; BAT-004/010/012; API-037/038. |

**Procedure:**

1. Identify the affected tenant and index generation.
2. Compare authoritative source fingerprints with indexed versions.
3. Inspect event ID, outbox lag, parser flags, search throttling, and source ACL revision.
4. Retry failed derivative work under bounded transient-failure policy.
5. Repair broken message links from the outbox ledger.
6. Preserve accepted source records.
7. Verify fingerprints and denied-access behavior before considering an incident recovered.

**Needs confirmation — OQ-BAT-013:** Automatic reconciliation schedule, scan selection, mismatch thresholds, bounds, checkpoint schema, automatic-versus-operator replay boundary, and completion/receipt schema.

### BAT-012 — Bounded Operator Replay

<a id="bat-012"></a>

**Sources:** [DDS], p. 50, §13.3.2; p. 90, §F.1.

| Contract category | Definition |
|---|---|
| Arguments | API-038 `id`; operator reason; dry-run validation; scope limit. Exact request names/types and scope units NC. |
| Inputs and extraction | Selected dead letter or validated outbox records; original schema, event identity, aggregate revision, and authorized target scope. |
| Transformation | Validate and replay bounded original processing; explicit migration may transform schema with provenance link. |
| Update targets | Original consumer targets; DAT-026 replay/dead-letter/provenance evidence; append-only audit attribution. |
| Outputs | Scoped replay outcome and evidence used for reconciliation/incident closure. |
| Successful completion | Original event identity preserved unless explicitly migrated with provenance; no duplicate mutation or changed-artifact publication. |
| Related contracts | API-038; `API-PROC-014`; `DAT-026-F01`–`F03`; `SCR-X-006`. |

**Procedure:**

1. Authorize the operator and establish the selected tenant/resource scope.
2. Require an operator reason and explicit scope limit.
3. Perform dry-run validation before replay execution.
4. Validate original envelope/schema and current applicable resource authorization.
5. Preserve event identity; if an approved migration transforms the schema, retain an explicit provenance link.
6. Replay only the validated bounded selection.
7. Let original consumers enforce idempotency, revisions, and publication guards.
8. Compare resulting fingerprints and execute denied-access probes.
9. Retain correlated replay/audit evidence.

**Needs confirmation — OQ-BAT-007:** Reason format, scope units/value, dry-run result/approval mechanics, replay deadline, partial result, pause/resume, and exhausted-retry handling. API-038 does not by itself confirm a browser console or generic outbox-replay request schema.

### BAT-013 — Eligible Closed-Case Retention and Tombstone Purge

<a id="bat-013"></a>

**Sources:** [DDS], p. 26, §6.3.2; pp. 51–53, §§14.1–14.3; p. 85, §B.1.

| Contract category | Definition |
|---|---|
| Arguments | Authorized retention/purge inventory, policy/eligibility context, holds, scoped actor and operation identity. API-040 body NC. |
| Inputs and extraction | Case-retention processing selects only eligible `CLOSED` cases. Final purge also processes eligible tombstoned targets under the scheduled pipeline. Exact predicates/age boundaries NC. |
| Update targets | DAT-003/004/025 and related eligible inventory; DAT-028/023 object/index targets; DAT-029 tombstones/holds; DAT-018 receipts. |
| Outputs | Auditable purge outcomes and hold exceptions; source-named `DataRetentionPurgeCommitted` evidence, exact trigger/schema NC. |
| Successful completion | Only eligible targets purged; held records protected; soft-deleted entities not retrievable; completion evidence retained. |
| Related contracts | API-040; `DAT-LC-018/021`; `DAT-018-F01`–`F05`; BAT-021. |

**Procedure:**

1. Resolve authorized scope and approved retention policy.
2. Select eligible closed cases for case-retention processing.
3. Resolve associated inventory and legal-hold exceptions before destructive work.
4. Preserve protected approved-output lineage according to the resolved retention contract.
5. Apply tombstone controls so soft-deleted entities are not retrievable.
6. Remove eligible object/index data through the controlled purge pipeline.
7. Record target, tenant, purge time, actor, completion evidence, and hold exceptions.
8. Do not claim completion for unverified removal or held protected data.

**Needs confirmation — OQ-BAT-016:** Retention classes/durations, closure-time boundary, shared-source handling, historical citations/audit survival, physical relational deletion, hold races, receipt survival, scheduler, and partial completion. The eligible-closed-case restriction is confirmed for case-retention jobs; its relationship to independently approved workspace deletion remains unresolved.

### BAT-014 — Diagnostic and Security-Audit Retention Purge

<a id="bat-014"></a>

**Sources:** [DDS], p. 66, §18.3.2; p. 90, §F.2.

| Contract category | Definition |
|---|---|
| Arguments | Diagnostic/audit record class, retention policy, tenant scope where applicable, legal holds, purge inventory. Exact fields NC. |
| Inputs and extraction | Records eligible under distinct diagnostic and security-audit policies. Source baseline: diagnostic 30-day default TTL; security-audit seven-year policy. |
| Update targets | DAT-030 diagnostic records; DAT-013 retained audit records/storage as applicable; DAT-018 receipts/hold exceptions. |
| Outputs | Completion receipts and legal-hold exceptions. |
| Successful completion | Applicable retention class enforced without conflating diagnostic and security-audit policies or deleting protected evidence. |
| Related contracts | `DAT-LC-019`; DAT-013/018/030; `OQ-API-034`; `OQ-DAT-018/025`. |

**Procedure:**

1. Distinguish diagnostic versus security-audit records.
2. Resolve the applicable approved retention policy and legal holds.
3. Select eligible records using the resolved timestamp/boundary contract.
4. Purge eligible records through the approved retention mechanism.
5. Record completion receipts and protected-record exceptions.

**Needs confirmation — OQ-BAT-016:** Corporate policy selection and precedence, time boundary, provider TTL versus application purge, batch units, audit export coordination, receipts, and execution schedule. The source defaults are not confirmation of a production policy decision.

### BAT-015 — Audit Batch-Hash Chaining and Independent Export

<a id="bat-015"></a>

**Sources:** [DDS], p. 62, §17.3.1; p. 88, `T-09`.

| Contract category | Definition |
|---|---|
| Arguments | Authorized audit batch scope and independent retention destination; exact contract NC. |
| Inputs and extraction | Append-only DAT-013 audit entries and prior chain context. Ordering/batch boundary NC. |
| Transformation | Chain entries with batch hashes and export to independently controlled retention storage. |
| Update targets | Tamper-evident audit manifests/chain evidence and retention export; original audit entries remain append-only. |
| Outputs | Independently retained audit evidence, including batch-hash integrity data. |
| Successful completion | Historical audit/review evidence remains unalterable and integrity/export requirements are satisfied. |
| Related contracts | API-021 reads authorized evidence; DAT-013; DAT-FILE-003; `DAT-LC-025`; BAT-020. |

**Procedure:**

1. Select authorized append-only audit entries under the resolved batch contract.
2. Retain actor/action/digest and required chronology/correlation evidence.
3. Compute the source-required batch-hash chain using the resolved integrity protocol.
4. Export to independently controlled retention storage.
5. Preserve the append-only ledger and historical reviewer decisions.

**Needs confirmation — OQ-BAT-017:** Batch ordering, algorithm/canonical input/encoding, manifest format, export cadence, checkpoint, duplicate export behavior, delivery verification, destination grants, and audit-export failure response. No universal SHA-256 mapping is selected for every digest.

### BAT-016 — Daily Usage and Cost Rollups

<a id="bat-016"></a>

**Sources:** [DDS], p. 38, §10.3.1; p. 65, §18.3.1; p. 83, §A.2; p. 85, §B.1.

| Contract category | Definition |
|---|---|
| Arguments | Reporting scope/day/window, configuration version, cost-center/deployment context. Exact fields and reporting timezone NC. |
| Inputs and extraction | Attributed model invocations, embeddings, storage/indexing usage, quotas/budgets, and rejected excess requests. |
| Aggregation | Daily reporting of budget, forecast, rejected excess requests, costs/quotas/trends; separate usage categories retain attribution. Formulas NC. |
| Update targets | DAT-030 daily usage/CostLedger projections; DAT-016 token ledger remains usage input. Physical rollup table NC. |
| Confirmed fields | `token_ledger.run_id`, `deployment_id`, `in_tokens`, `out_tokens`; workspace cost center and actual model deployment version attribution. |
| Outputs | API-022 costs, quotas, and trend estimates; daily budget/forecast/rejected-excess reporting. |
| Successful completion | Reporting reflects attributed source usage without losing tenant/workspace, cost-center, deployment-version, or category distinctions. |
| Related contracts | API-022; `API-PROC-009`; DAT-016/030; SCR-010. |

**Procedure:**

1. Resolve the reporting-day/window and authorized tenant/workspace scope.
2. Extract attributed source usage under the resolved accounting grain.
3. Keep model, embedding, storage, indexing, raw-file, normalized-text, vector, and replication measures distinct where required.
4. Aggregate the daily reporting inputs without duplicating replayed usage.
5. Produce budget, forecast, rejected-excess, and trend data using approved formulas.
6. Persist/report the authoritative rollup through the resolved data contract.

**Needs confirmation — OQ-BAT-018:** Day boundary, execution time, currency/units/precision, cost allocation, forecast formula, late-arriving usage, failed/retried provider accounting, zero-input output, corrections, reruns, and rollup identity. No midnight job, currency, or “replace versus increment” rule is selected.

### BAT-017 — Frozen Benchmark Evaluation

<a id="bat-017"></a>

**Sources:** [DDS], pp. 74–76, §§21.1–21.3; pp. 88–89; p. 83, §A.2.

| Contract category | Definition |
|---|---|
| Arguments | API-023 evaluation request and job idempotency; dataset/prompt/model/version selection schema NC. |
| Inputs and extraction | Frozen, versioned, independently reviewed synthetic corpus; signed manifest; expected citation sets/decision outcomes. Reference corpus contains 1,200 permission-controlled cases. |
| Transformation | Execute deterministic contracts and probabilistic AI evaluation separately; compute quality/safety scores, confidence intervals, and distribution shift by domain. |
| Update targets | DAT-031 `Scorecard`/`ReleaseGateResult` and evaluation evidence; exact persistence/schema NC. |
| Outputs | Evaluation results via API-024; `EvaluationCompleted`; signed release-linked test output where part of release pack. |
| Successful completion | Authoritative evaluation evidence produced. Execution completion is distinct from passing release gates. |
| Related contracts | API-023/024; `API-PROC-010`; DAT-031; DAT-FILE-005/006; SCR-011. |

**Procedure:**

1. Validate Admin authorization, input, idempotency, and frozen dataset/version.
2. Verify the signed manifest and independently reviewed fixture integrity.
3. Preserve expected citation sets and decision outcomes; reject uncontrolled replacement.
4. Run required retrieval, refusal, ambiguity, adversarial, and permission-controlled scenarios.
5. Exercise deterministic state/idempotency/authorization/hash/retry/schema contracts without live model calls where specified; pin provider-facing adapters with consumer-driven contracts.
6. Evaluate citation precision, unsupported-claim rate, and high-risk policy recall.
7. Report confidence intervals and distribution shift by domain.
8. Preserve targets `>=0.97`, `<=0.02`, and `1.00` on the frozen safety suite.
9. Block release for low statistical confidence or critical isolation/approval failures regardless of benchmark score.
10. Persist correlated evaluation completion evidence; reevaluate independent prompt/model changes.

**Needs confirmation — OQ-BAT-019:** Evaluation input/status/result schemas, dataset selection, score denominators/aggregation, domain taxonomy, confidence methods, fixture failure and partial-evaluation treatment, concurrency, progress, timeout, and completion event. Missing/empty fixtures must not be assigned a passing score by an unresolved convention.

### BAT-018 — Idempotent Provisioning

<a id="bat-018"></a>

**Source:** [DDS], p. 78, §22.1.1.

| Contract category | Definition |
|---|---|
| Arguments | Authorized provisioning target and approved policy/encryption/role/quota/connector configuration. Names, role, entry API, and defaults NC. |
| Inputs and extraction | Target tenant/workspace context and required configuration references. |
| Transformation | Establish required resources as one idempotent workflow; no single distributed ACID transaction is specified. |
| Update targets | DAT-001/002/019/029; workspace policy, encryption references, role bindings, quotas, connector stubs. |
| Outputs | Authoritative complete or visible incomplete provisioning state. |
| Successful completion | Required provisioning resources exist consistently and connector sync is no longer blocked for incomplete provisioning. |
| Related contracts | API-GAP-008; `API-PROC-012`; `DAT-029-F05`; `SCR-X-002`. |

**Procedure:**

1. Validate the authorized target and required approved configuration.
2. Resolve prior operation/checkpoint state for idempotent processing.
3. Create workspace policy, encryption references, role bindings, quotas, and connector stubs.
4. Persist durable provisioning state.
5. Keep incomplete provisioning visible and block connector synchronization.
6. Resume/retry using durable workflow controls rather than creating duplicate resources.

**Needs confirmation — OQ-BAT-020:** Input schema, actor, entry/status API, resource creation order, compensation for partial resources, checkpoint identity, completeness predicate, and rerun behavior after configuration changes.

### BAT-019 — Historic Source Backfill and Reconciliation

<a id="bat-019"></a>

**Source:** [DDS], p. 78, §22.1.2.

| Contract category | Definition |
|---|---|
| Arguments | Authorized historic source scope and bounded window; exact window carrier/units/value NC. |
| Inputs and extraction | Historical documents with stable source IDs. Ordering, time boundary, and overlap with incremental sync NC. |
| Transformation | Ingest through the established pipeline and reconcile each batch against source/version/index evidence. |
| Update targets | DAT-005–007/022/023/029; stable source identity and per-batch reconciliation receipts. |
| Outputs | Reconciled batch receipts and index-coverage readiness evidence. |
| Successful completion | Selected bounded history is accounted for; readiness is based on index coverage, not queue emptiness. |
| Related contracts | BAT-002/003/004/011; `DAT-029-F06`; `DAT-LC-026`; API-GAP-008. |

**Procedure:**

1. Resolve the authorized source and bounded historical window.
2. Preserve stable source IDs.
3. Ingest selected documents through safety, normalization, and indexing controls.
4. Compare source and resulting version/index outcomes for each batch.
5. Record per-batch reconciliation receipts.
6. Signal search readiness using index coverage under the resolved readiness contract.

**Needs confirmation — OQ-BAT-020:** Window size/order, inclusive bounds, source changes during backfill, batch receipt schema, parallelism with incremental sync, checkpoint/resume, quarantine accounting, coverage threshold, and no-history outcome.

### BAT-020 — Controlled Workspace Export

<a id="bat-020"></a>

**Sources:** [DDS], p. 78, Chapter 22 invariant; p. 79, §22.3.1; p. 83, §A.2; p. 88, `T-11`.

| Contract category | Definition |
|---|---|
| Arguments | API-025 `workspaceId`, required job idempotency, independently verified approval context. Exact scope/approval body NC. |
| Inputs and extraction | Authorized workspace inventory; case metadata, approved artifacts, source references, audit manifests. Snapshot boundary NC. |
| Transformation | Package permitted content and checksums; exclude secrets and internal model prompts. |
| Update targets | DAT-029 `ExportManifest` and export evidence; DAT-FILE-004 package. |
| Outputs | Controlled export manifest/package. API-025 `202` indicates acceptance, not completion/download readiness. |
| Successful completion | Required authorized content packaged with checksums and exclusions after two independent approval checks. |
| Related contracts | API-025; `API-PROC-011`; `DAT-029-F03/F04`; `SCR-X-003`. |

**Procedure:**

1. Validate workspace authorization, request, and operation identity.
2. Enforce two independent approval checks; a single Admin cannot bypass them.
3. Resolve the permitted inventory/snapshot.
4. Collect case metadata, approved artifacts, source references, and audit manifests.
5. Exclude secrets and internal model prompts.
6. Produce manifest/checksums under the resolved file contract.
7. Record the authoritative export outcome; release/download transport remains unresolved.

**Needs confirmation — OQ-BAT-021:** Independent-approval protocol/validity, exact inventory, snapshot consistency, held/draft content treatment, package format/size/lifetime, partial export, checksum validation, result/status/download APIs, and rerun behavior. No automatic export-then-delete chain is confirmed.

### BAT-021 — Verified Workspace Deletion

<a id="bat-021"></a>

**Sources:** [DDS], pp. 78–80; p. 83, §A.2; p. 87, §C.1; p. 89, `TST-013`.

| Contract category | Definition |
|---|---|
| Arguments | API-026 `workspaceId`, required job idempotency, independently verified approval context, authorized inventory and holds. Exact body NC. |
| Inputs and extraction | Deletion inventory; current legal holds; eligible blob/index/resource targets. Inventory granularity and relational scope NC. |
| Update targets | DAT-029 holds/tombstones/inventory; DAT-028 blobs; DAT-023 index entries; DAT-018 `deletion_receipts`. |
| Confirmed receipt fields | `tenant_id`, `object_ref`, `purge_time`, `actor`; manifest ID/receipt hash are event payload concepts. |
| Outputs | Completion receipts and retained/receipted protected records; `TenantDeletionVerified` → close purge record. |
| Successful completion | Eligible data removed/verified and held data protected with receipts; no false full purge of protected records. |
| Related contracts | API-026/029/040; `API-PROC-011`; `DAT-LC-021/022`; `SCR-X-004/X-005`. |

**Procedure:**

1. Validate target, request, operation identity, and two independent approval checks.
2. Resolve the authorized deletion inventory and legal holds.
3. Write tombstones and prevent retrieval of soft-deleted targets.
4. Preserve held protected records.
5. Remove eligible blobs and index entries through controlled deletion/purge processing.
6. Record completion receipts and legal-hold exceptions.
7. Verify the inventory/receipt outcome before emitting the applicable verification event.
8. Process `TenantDeletionVerified` idempotently to close the purge record.
9. Use the same inventory for source-described data-subject access requests without assuming every such request requires erasure.

**Needs confirmation — OQ-BAT-016:** Hold/deletion races, deletion scope, closure eligibility relationship, relational cleanup, backup handling, retained audit/actor/citation references, partial completion, verification/receipt schema, and legal-hold completion event semantics.

### BAT-022 — Database Migration Backfill and Constraint Enforcement

<a id="bat-022"></a>

**Sources:** [DDS], p. 52, §14.2.2; p. 72, §20.2.2; p. 20, §4.3.2.

| Contract category | Definition |
|---|---|
| Arguments | Controlled `MigrationPlan`, source/target schema versions, bounded backfill scope, rollout compatibility and rollback plan. Exact schemas/commands NC. |
| Inputs and extraction | Rows requiring the approved transformation; actual table/column mapping and predicate belong to the migration plan, not this generic function. |
| Transformation | Expand-and-contract: add nullable columns, backfill bounded batches, enforce constraints after required compatibility/drainage conditions. |
| Update targets | Only targets defined by the approved migration; DAT-032 migration/release evidence. |
| Outputs | Compatible migrated data and enforced constraints with reconstructible release bindings. |
| Successful completion | No field removed while active readers depend on it; postdeployment enforcement follows old-replica drainage and successful backfill. |
| Related contracts | API-043/044; `API-COM-004`; `DAT-LC-026`; `DAT-032-F03`. |

**Procedure:**

1. Validate the migration plan and active-reader compatibility.
2. Add nullable columns first through backward-compatible predeployment expansion.
3. Apply the declared transformation in bounded batches.
4. Preserve readable-write behavior required by the explicit rollback plan.
5. Canary traffic as part of the release workflow.
6. Wait for old replicas to drain before postdeployment enforcement.
7. Enforce approved constraints after backfill and compatibility conditions.
8. Do not automatically down-migrate the database on a canary regression.

**Needs confirmation — OQ-BAT-022:** Actual migrations, transformation rules, batch bounds, transaction units, concurrent writes, checkpoints, zero-row behavior, verification queries, field-removal schedule, and supported compensation.

### BAT-023 — Continuous Backup, Incident Restore, and Recovery Validation

<a id="bat-023"></a>

**Sources:** [DDS], p. 19, §4.2.2; pp. 69–70, §19.3; p. 89, `TST-012` and §E.2.

| Contract category | Definition |
|---|---|
| Arguments | Backup/recovery scope, selected snapshot/recovery point, object-version inventory, index rebuild recipes, incident authorization. Exact schemas NC. |
| Inputs and extraction | Continuous PostgreSQL backups, object versions, and index rebuild recipes. |
| Update targets | Recovery environment, restored relational/object state, regenerated index as required, DAT-036 recovery evidence. |
| Outputs | Consistency/recovery evidence and release-linked DR test output where applicable. |
| Successful completion | Reference RPO `<=15 minutes`, RTO `<=4 hours`; relational/object/index consistency verified. |
| Related contracts | `API-PROC-030`; `DAT-LC-024`; DAT-FILE-007; BAT-005/026. |

**Procedure:**

1. Maintain the source-confirmed continuous PostgreSQL backup capability.
2. Retain/test object versions and index rebuild recipes with relational recovery.
3. Under incident command, select the authorized recovery scope and point.
4. Restore secondary snapshots only through incident control.
5. Reconcile relational and object state.
6. Rebuild search from authoritative data where necessary.
7. Measure safety, consistency, RPO, and RTO.
8. Exercise provider `429` storms, lost worker heartbeats, duplicate events, object-access failures, and primary-region outage as required by fault-injection testing.

**Needs confirmation — OQ-BAT-023:** Providers/regions, backup retention/encryption, restore commands, recovery checkpoints, write fencing, hold/deletion propagation to backups, failed-restore handling, drill cadence, and exact measurement boundaries. Cross-region active/active writes remain deferred.

### BAT-024 — Secret and Encryption-Key Rotation

<a id="bat-024"></a>

**Sources:** [DDS], p. 21, §5.1.2; p. 63, §17.3.2; p. 10, §1.3.2.

| Contract category | Definition |
|---|---|
| Arguments | Approved rotation policy and scoped vault/key references. Exact identifiers, schedule, and operation contract NC. |
| Inputs and extraction | Application/service credentials and encryption keys eligible under the defined policy. |
| Transformation | Automatic service credential rotation and policy-based encryption-key rotation through vault-backed access. |
| Update targets | DAT-019 credential references; DAT-028 encryption references; DAT-032 secret configuration bindings. Exact persistence NC. |
| Outputs | Rotated authorized credentials/keys and required durable attribution where state changes. |
| Successful completion | Secrets remain in the vault, do not appear in traces/prompts, and rotation does not require bulk reencryption in the request path. |
| Related contracts | API external/internal authentication profiles; `DAT-LC-025`; `OQ-DAT-017/025`. |

**Procedure:**

1. Resolve the approved rotation policy and authorized vault references.
2. Access secret/key facilities with managed identity where supported.
3. Rotate eligible credentials/keys through the selected provider mechanism.
4. Maintain declared application/service access without sharing workload identities.
5. Keep secret values out of job arguments exposed to callers, telemetry, and model prompts.

**Needs confirmation — OQ-BAT-024:** Provider-managed versus application execution, policy/schedule, overlap/grace periods, reference switching, rollback/revocation, verification, key isolation versus throughput, and whether any background reencryption is needed. No bulk reencryption job is invented.

### BAT-025 — Optional Signed Webhook Delivery

<a id="bat-025"></a>

**Source:** [DDS], p. 55, §15.2.2.

| Contract category | Definition |
|---|---|
| Arguments | Optional authorized subscription, notification/event context, signing reference. Actual URL/method/header/body schema NC. |
| Inputs and extraction | Accepted internal notification eligible for an optional outbound subscription; exact event mapping NC. |
| Transformation | Sign delivery; retry with exponential backoff. Recipient verifies signature and event age. |
| Update targets | DAT-034 subscription/delivery evidence if persisted; physical schema NC. |
| Outputs | Signed outbound notification and resolved delivery outcome. |
| Successful completion | Recipient acknowledgment under the resolved contract; internal accepted case transition remains committed regardless of delivery failure. |
| Related contracts | API-047; `API-PROC-017/028`; `DAT-034-F02`; `SCR-X-007`. |

**Procedure:**

1. Resolve the optional authorized recipient and eligible accepted notification.
2. Construct and sign the approved payload.
3. Deliver to the configured endpoint.
4. Retry transient delivery failure with exponential backoff under the resolved bounded policy.
5. Preserve accepted internal case state; do not roll it back due to notification failure.

**Needs confirmation — OQ-BAT-025:** URL/method/payload, event mapping, signature/canonicalization, key rotation, event-age window, acknowledgment statuses, deduplication, retry cap/deadline, terminal delivery handling, and manual redelivery. No email/SMS notification channel is confirmed.

### BAT-026 — Build, Verification, and Controlled Release

<a id="bat-026"></a>

**Sources:** [DDS], pp. 71–73, Chapter 20; p. 88, §D.1; p. 89, §E.2.

| Contract category | Definition |
|---|---|
| Arguments | Controlled source/build/release identity, image/schema/prompt/routing/configuration versions, migration plan, gate and sign-off evidence. API-043 body NC. |
| Inputs and extraction | Source artifacts, nonsecret source-controlled defaults, signed environment configuration, vault references, synthetic test fixtures, baseline metrics. |
| Transformation | Static/dependency analysis, tests, SBOM, image signing, compatibility checks, staged canary, release gates. |
| Update targets | DAT-032 release/configuration/migration/rollout records and signed test artifacts. |
| Outputs | Reconstructible release record binding image digest, schemas, prompts, model-routing policy; `ReleasePromoted` where promotion is accepted. |
| Successful completion | Allowed build identity verified; required tests/gates and Security/SRE validation satisfied; no unresolved critical isolation/approval bypass promoted. |
| Related contracts | API-043/044; `API-PROC-015`; DAT-031/032/033; DAT-FILE-006; BAT-017/022/023. |

**Procedure:**

1. Build reproducible artifacts using the declared infrastructure/configuration contracts. Terraform versus Bicep remains unselected.
2. Run static analysis, dependency scanning, unit and contract tests.
3. Generate SBOM and sign container images.
4. Verify production image digests against an allowed build identity.
5. Execute the minimum release pack: unit, schema-evolution, negative authorization, workflow replay, staging connector sync, visual accessibility, search recall, grounding, policy recall, load, and DR tests.
6. Sign test outputs and reference them by release digest.
7. Apply backward-compatible migrations and relevant BAT-022 sequencing.
8. Compare canary latency, errors, authorization denials, and AI-quality regressions against baseline.
9. On regression, automatically roll back traffic; do not automatically down-migrate the database.
10. Require Security and SRE validation of external egress, secret handling, backup status, and alert routing before promotion.
11. Preserve a release record sufficient to reconstruct binary, prompt, schema, and policy versions.

**Needs confirmation — OQ-BAT-022:** Pipeline trigger/order beyond confirmed dependencies, tools, SBOM/signature formats, allowed build identities, canary duration/thresholds, sign-off transport, promotion schema, and supported compensating data operations. `SEC-001`–`SEC-012` are release-blocking source identifiers, but their individual definitions are not supplied.

## Operations and Recovery

### Execution Security and Launch Procedure

**BAT-OPS-001 — Authorized durable launch.**

1. Authenticate the caller/workload and establish trusted tenant, actor, trace, and correlation context.
2. Validate arguments/envelope/schema before long-running allocation.
3. Evaluate role, tenant, workspace membership, sensitivity, source ACL, requested action, and separation of duties as applicable.
4. Check operation idempotency, resource revisions, provisioning, quota, and policy prerequisites.
5. Reevaluate resource authorization within state-changing transactions.
6. Commit only accepted state and associated durable event/checkpoint evidence.
7. Return the authoritative synchronous result or persisted asynchronous operation identity. A dependency failure must not yield ambiguous success.
8. Execute background work with immutable signed tenant scope.
9. Reset tenant-scoped database session variables after every transaction before connection reuse.

**Sources:** [DDS], pp. 18, 21–23, 25, 48–56, 86.  
**Earlier trace:** `API-PROC-001`; `DAT-COM-003`; `DAT-LC-013/015`.

**Needs confirmation — OQ-BAT-002/OQ-BAT-003:** Complete job schemas/signatures, service audiences/grants, operation identifiers, internal success/error modes, and missing-context outcomes. Internal APIs are not automatically browser APIs.

### Concurrent Launches and Mutual Exclusion

**BAT-OPS-002 — Required concurrency outcomes.** The source requires replay-safe writes, revision checks, durable cursor/checkpoint consistency, and atomic publication/alias transitions. It does not select a locking mechanism.

| Contention area | Confirmed requirement | Unresolved exclusion / recovery contract |
|---|---|---|
| Duplicate job-creating requests | Identical key/fingerprint returns the original operation; changed fingerprint conflicts. | Key namespace, simultaneous-pending response, claim protocol, and non-case TTL. |
| Case classification versus case edit/correction | Stale/unauthorized writes rejected; correction reason/provenance preserved. | Revision binding and classifier overwrite/recompute policy. |
| Same connector synchronization | Cursor advances only after preceding durable outcomes; partial retry safe. | Single active sync versus parallel partitions; cursor ownership/fencing. |
| Same document/pipeline processing | Immutable fingerprint/pipeline derivatives; cross-service idempotency. | Derivative uniqueness/claim and duplicate extraction behavior. |
| Incremental index writes versus rebuild | Versioned aliases; atomic read switch after checks; source remains authoritative. | Snapshot/catch-up, generation writer exclusion, alias fencing. |
| ACL change versus retrieval/publication | Revocation before next retrieval; publication rechecks current evidence/authorization. | Atomic propagation protocol and in-flight result handling. |
| Duplicate workflow step/resume | Idempotent steps and replayable checkpoints. | Lease, claim, heartbeat timeout, and stale worker fencing. |
| Decision versus task expiry/reassignment | Valid task/hash/actor controls; no implicit approval. | Race ordering, late-decision response, assignment identity. |
| Publication consumers | Gate/pointer atomic; old approval cannot authorize changed artifact. | Transaction isolation, locking, and duplicate acknowledgment. |
| Retention/workspace deletion versus new hold | Legal holds protect records; held records retained/receipted. | Hold timing, destructive-operation fence, and partial verification. |
| Rollups/evaluations/export/migration | Cross-service writes idempotent and evidence versioned. | Resource/window/result identity and same-scope concurrency. |
| Primary versus recovery region | Persistent writes target the primary; restore under incident command. | Failover/write fencing and worker activation protocol. |

**Sources:** [DDS], pp. 19, 25, 28, 31, 34, 40–42, 45–50, 69, 80, 85.

**Needs confirmation — OQ-BAT-004:** Define the permitted parallelism and conflict behavior for every row. Do not introduce a distributed lock, lease duration, database isolation level, or “one job per tenant” rule as confirmed.

### Processing and Commit Units

**BAT-OPS-003 — Durable boundaries.**

| Processing unit | Confirmed commit/checkpoint rule | Needs confirmation |
|---|---|---|
| Case/approval mutation | Business mutation and associated outbox insert commit in one ACID transaction. | Exact history/audit/result-ledger participation and audit-write failure handling. |
| Publication | Satisfied gate and final response pointer commit together. | Isolation/locks and publication-state projection. |
| AI plan | Plan revision persisted before side effects. | Plan/checkpoint schema and accepted-plan transaction. |
| Workflow stage | Checkpoint written before downstream dispatch. | Checkpoint history, broker acknowledgment, and continuation claim. |
| Connector item/cursor | Preceding items have durable ingestion outcomes before cursor advancement. | Item/batch transaction size, quarantine accounting, and source-provider ordering. |
| Extraction/object/index | Immutable derivative writes and durable continuation; index failure does not undo source metadata. | Cross-store coordination, partial-object cleanup, and derivative readiness boundary. |
| Index rebuild | Read alias switches atomically after completeness/recall checks. | Batch commit and generation cleanup/rollback. |
| Historic/migration backfill | Bounded batches; historic backfill has per-batch reconciliation receipts. | Numeric batch bounds and receipt/checkpoint atomics. |
| Audit export | Append-only entries, batch hashes, independent retention export. | Batch ordering, export checkpoint, and verification boundary. |
| Purge/deletion | Tombstones, eligible removal, hold exceptions, and completion receipts. | Object versus inventory commit units, verification and partial completion. |
| Daily rollup | Daily aggregation required. | Window identity and replace/increment/correction commit rule. |
| Evaluation/export/release | Durable accepted work and retained result/evidence. | Result transaction, partial-output publication, and completion criteria schemas. |

**Sources:** [DDS], pp. 28, 31, 34, 40, 45, 49, 52, 62, 65, 72, 78–80.

**Needs confirmation — OQ-BAT-005:** Define commit units, cross-store reconciliation, checkpoint/acknowledgment ordering, and recovery claims. Do not replace source-required durability with an in-memory job-status record.

### Idempotency, Reruns, and Resumption

**BAT-OPS-004 — Replay safety.**

- Every cross-service write is idempotent under retry.
- POST mutations creating long-running jobs require `Idempotency-Key`.
- The case-domain actor/request fingerprint maps to one outcome for 24 hours.
- A repeated identical request returns the original operation/outcome; changed fingerprint under the same key produces `IDEMPOTENCY_CONFLICT`.
- At-least-once consumers deduplicate event IDs and operation keys and detect stale aggregate revisions.
- No business invariant depends on ordering across queue partitions.
- A duplicate accepted event records a duplicate outcome without reapplying the mutation.
- Rerunning changed normalization produces side-by-side immutable versions, not overwritten cited evidence.
- Denied recommendations are reworked as new run revisions, not retroactively approved.
- Operator replay preserves original event identity unless explicit schema migration retains a provenance link.
- Browser refresh reconstructs run progress from server state; it must not launch another workflow.
- SSE reconnect uses `Last-Event-ID` and retained scoped backfill; streaming replay is not business mutation replay.

**Sources:** [DDS], pp. 15–17, 25, 31, 40, 46, 48–50, 54–55, 58, 89.  
**Earlier trace:** `API-PROC-018`; `DAT-LC-016/023`.

**Needs confirmation — OQ-BAT-006:**

- Ledger retention and key expiry outside the case-domain contract.
- Fingerprint canonicalization and key scope.
- Pending duplicate response and concurrent key reservation.
- Replay after permission/configuration changes.
- Rerun versus resume versus new revision for each job.
- Late-data rollup correction and duplicate provider usage accounting.
- Checkpoint migration and replay of old schema versions.
- SSE history/gap behavior.

Appendix F’s `replay_dedup_hours: 24` is an example. It is not confirmation of all job ledgers, broker retention, or SSE history lifetime.

### Retries, Timeouts, and Worker Loss

**BAT-OPS-005 — Retry discipline.**

| Condition | Confirmed behavior | Unresolved setting |
|---|---|---|
| Transient dependency failure | Bounded exponential backoff, randomized jitter, per-dependency circuit breaker. | Attempt count, initial/max delay, circuit thresholds, recovery window. |
| Validation or permission failure | Permanent; do not retry as a transient fault. | Per-job status/code and correction workflow. |
| Repository throttling | Honor `Retry-After`, enforce quotas and fair scheduling. | Provider mapping, attempt/deadline bounds, fairness algorithm. |
| Provider `429` burst | Capped retries and controlled admitted load. | Exact caps and capacity thresholds. |
| Malformed connector record | Bounded retries, then quarantine with reason/correlation/remediation; remaining batch may proceed. | Malformed/retryable taxonomy and numerical bound. |
| Unsafe attachment | Quarantine; no indexing. | Failure code, status transport, remediation path. Do not retry safety validation indefinitely. |
| Model output invalid | Bounded parsing retries; `MODEL_OUTPUT_INVALID`; no publish. | Parse retry count and usage accounting. |
| Current-run quota exhaustion | Terminal current-run outcome; no automatic model/data-class change. | Exact terminal status/error mapping. |
| Run call/deadline/policy failure | Stop and report failed checkpoint. | Timeout, repeated-invalid-plan count, retry call accounting. |
| Review waiting versus missing approval | Both waiting state and missing-approval stop text exist. | Explicit semantic resolution required; no timeout assumption. |
| Webhook failure | Exponential backoff; no rollback of internal case transition. | Cap/deadline, acknowledgment classification, terminal delivery outcome. |
| Lost worker heartbeat/object failure | Covered by fault-injection acceptance. | Heartbeat interval, lease expiry, ownership transfer, stale-worker fencing. |

**Sources:** [DDS], pp. 28–29, 38, 41–42, 49–50, 55, 69–70, 89.

**Needs confirmation — OQ-BAT-007:** Per-job retry bounds, deadlines, stop states, exhausted-retry disposition, cancellation, and worker-loss recovery. No general batch timeout is supplied.

### Rollback and Compensation

**BAT-OPS-006 — Failure handling must respect committed authority.**

| Failure | Confirmed recovery behavior | Prohibited or unresolved action |
|---|---|---|
| Stale/unauthorized write | Reject; business state unchanged. | No compensating mutation is needed to “undo” an unaccepted write. |
| Failed index write | Preserve accepted source metadata; compare fingerprints and retry through reconciliation. | Do not roll back accepted source metadata merely because search failed. |
| Broken message link | Repair from the outbox ledger. | Do not create a new event identity without explicit migrated provenance. |
| Changed reviewed artifact | Reject stale action and audit; new candidate follows controls. | Do not reuse prior approval or modify historical decision. |
| Valid review wait/expiry | Apply resolved waiting/expiry routing; no implicit approval. | No automatic “timeout approval.” |
| Failed webhook | Accepted case transaction remains committed. | No case rollback due to notification delivery. |
| Canary regression | Automated traffic rollback; binary reversed first. | No automatic database down-migration. Data compensation only when explicitly supported. |
| Legal hold during purge | Protect and receipt held records. | No hold bypass or false complete erasure. |
| Partial provisioning/export/migration/purge | Use durable workflow/evidence; exact compensation is NC. | Do not invent cleanup, reverse-delete, or resource recreation semantics. |

**Sources:** [DDS], pp. 20, 45–46, 49–50, 55, 72, 78–80, 89.  
**Needs confirmation — OQ-BAT-005/016/020/021/022:** Supply explicit compensation plans for unresolved cross-store and partial-operation cases.

### Logging, Notifications, Monitoring, and Capacity

**BAT-OPS-007 — Correlated privacy-safe evidence.**

1. Carry trace and correlation context across API, database, connector, retrieval, model, approval, and background boundaries.
2. Log identifiers and policy outcomes, not full document content.
3. Never place connector credentials, API secrets, or entire prompts in diagnostic traces.
4. Preserve one audit record for an accepted state transition; duplicate-processing evidence must not create another accepted business transition.
5. Expose stable non-sensitive failures and the exact failed workflow checkpoint where required.
6. Keep public error details within the safe scope defined by the canonical error envelope.
7. Retain source-required quarantine reason/correlation/remediation, review escalation, replay provenance, reconciliation receipts, purge receipts, and release/evaluation evidence.
8. Do not represent partial work as an approved answer or `202` acceptance as completed work.

**Sources:** [DDS], pp. 13, 29, 41, 48–50, 62–66, 78–80, 84–89.  
**Earlier trace:** `API-COM-007`; `DAT-LC-025`; SCR-COM-011.

**BAT-OPS-008 — Monitoring and notification boundaries.**

| Signal / condition | Source-required behavior | Open operational setting |
|---|---|---|
| Extraction/embedding worker queue age and throughput | Worker scaling is based on queue age/throughput. | Autoscaling thresholds, minimum/maximum workers, sampling windows. |
| Delayed indexing | Alert on oldest queue age and index backlog; identify tenant and generation. | Age/backlog thresholds and alert routing. |
| Diagnostics | Inspect event ID, outbox lag, parser flags, search throttling, ACL revision. | Metric names, labels, dashboards, retention and query access. |
| Golden signals | Request rate, errors, latency, saturation. | Job-specific metric projection and thresholds. |
| AI signals | Grounding pass rate, retrieval empty rate, throttling, token use, approval backlog age. | Calculation windows and alert thresholds. |
| User-impacting safety/reliability incident | Page for failure budgets, stale ACL propagation, missing approval enforcement. | Availability/error-budget calculation and on-call identities. |
| Routine token-spend anomaly | Create ticket with owner and threshold. | Actual owner, threshold, ticket channel and deduplication. |
| Model outage | Disable new generation admission; preserve manual case/evidence workflows; show degraded status; page only when availability budget impacted. | Capacity/error-budget threshold and admission response details. |
| Review expiry | Escalation recorded; task reassigned/escalated. | Notification recipient/channel and routing policy. |
| Run progress | Scoped durable SSE progression and server-state refresh reconstruction. | Payloads, retained history, connection/gap behavior. |
| Export/deletion/evaluation completion | Durable authoritative outcome required. | Completion notification channel/status endpoints; no email/SMS assumed. |
| Optional webhooks | Signed delivery independent of case transaction. | Complete delivery/security contract. |

**Sources:** [DDS], pp. 19, 45, 55, 58, 64–66, 69, 79, 90.

**Needs confirmation — OQ-BAT-008:** Define monitoring thresholds, metrics, job status projections, alert destinations, escalation channels, completion notification behavior, and actual operational assignments. No owner, deadline, email recipient, or alert threshold is appointed here.

Reference capacity assumptions are 2,000 daily active users, 60 requests/s steady, 180 requests/s burst, 100,000 indexed documents per tenant maximum, and 20 concurrent AI runs per large tenant. Typical 1 MB sources yield approximately 40–120 chunks. These are source workload/sizing assumptions, not newly selected worker concurrency limits or batch sizes.  
**Source:** [DDS], p. 68, §§19.1.1–19.1.2.  
**Open:** OQ-BAT-004/008/026; preceding `OQ-API-033`, `OQ-DAT-020/025`.

### Source-Confirmed Recovery Runbooks

#### BAT-OPS-009 — Delayed Document Indexing

1. **Detect:** Alert on oldest queue age and index backlog; identify affected tenant and index generation.
2. **Contain:** Pause only the faulty connector or indexer shard; retain accepted source records.
3. **Diagnose:** Inspect event ID, outbox lag, parser flags, search throttling, and source ACL revision.
4. **Recover:** Replay validated outbox records using a bounded operator-controlled job.
5. **Verify:** Compare source fingerprints with indexed versions, run denied-access probes, and close the incident.
6. **Document:** Link audit IDs, time window, blast radius, quality effect, and preventive action.

**Source:** [DDS], p. 90, §F.1.  
**Trace:** BAT-002/004/011/012.

Pause/resume endpoint, shard identity, replay scope, alert thresholds, and incident-record schema are **Needs confirmation — OQ-BAT-007/008/013**.

#### BAT-OPS-010 — Suspected ACL Leak

1. Suspend affected index aliases.
2. Revoke cached evidence.
3. Preserve audit traces.
4. Execute scoped replay of ACL revisions.
5. Reenable search only after negative access tests pass.

**Source:** [DDS], p. 79, §22.2.2.  
**Trace:** BAT-006/012.

The scope, command/API, hold on concurrent index work, and reenable authorization remain **Needs confirmation — OQ-BAT-003/004/013**.

#### BAT-OPS-011 — Model Provider Outage

1. Disable new generation admission.
2. Keep manual case and evidence workflows available.
3. Display degraded status.
4. Preserve approved deployment/region and data-handling constraints.
5. Page on-call only when the availability budget is impacted.

**Sources:** [DDS], p. 37, §10.1.2; p. 69, §19.2.2; p. 79, §22.2.1.  
**Trace:** BAT-007; API-030/036/050.

No degraded mode may bypass authorization or approval.

## Acceptance Criteria

### Verification Basis

**BAT-COM-004 — Test evidence.**

- Use synthetic successful, empty, mixed-permission, adversarial, and malformed fixtures.
- Record every randomized-test seed.
- Test state transitions, idempotency, tenant filters, approval hashes, retry semantics, and schema compatibility without live models where specified.
- Integration tests cover PostgreSQL transactions, outbox replay, ACL revocation, delayed indexing, and object purge.
- Critical isolation and approval tests pass with zero exceptions.
- Release test outputs are signed and referenced by release digest.
- Source-confirmed invariants are testable now; unresolved schemas, thresholds, and schedules must not be replaced with implementation-selected defaults.

**Sources:** [DDS], pp. 74–76, 88–89.

### Success, Safety, Partial Failure, and Rerun Criteria

| Acceptance ID | Prerequisites and action | Expected result | Trace and source |
|---|---|---|---|
| AC-BAT-001 | Create authorized case and deliver `CaseCreated`. | Policy-aware classification attaches labels, confidences, and provenance asynchronously; correct case scope retained. | BAT-001; API-001; DAT-020; [DDS], pp. 12, 87. |
| AC-BAT-002 | Replay accepted `CaseCreated` or classifier event delivery. | Consumer records duplicate outcome and does not reapply accepted mutation. | BAT-001/010; `TST-007`; [DDS], pp. 13, 48–50, 89. |
| AC-BAT-003 | Correct generated label. | Correction requires a reason code and durable attribution/provenance. Race/rerun assertion awaits OQ-BAT-010. | BAT-001; API-GAP-001; [DDS], p. 12. |
| AC-BAT-004 | Submit authorized connector sync to completed provisioning. | API-018 returns `202` and durable operation; capabilities discovered and unsupported support explicitly warned. | BAT-002; API-018; [DDS], pp. 27, 78, 83. |
| AC-BAT-005 | Sync workspace with incomplete provisioning. | Incomplete state visible; connector sync blocked. | BAT-002/018; [DDS], p. 78. |
| AC-BAT-006 | Revoke connector credential while work queued. | Queued job fails `CONNECTOR_REAUTH_REQUIRED`; no token disclosure. | BAT-002; DAT-019/021; [DDS], p. 27. |
| AC-BAT-007 | Fail some connector items before cursor commit, then retry. | Cursor never advances beyond preceding items without durable outcomes; retry preserves accepted outcomes. | BAT-002; DAT-015; [DDS], p. 28. |
| AC-BAT-008 | Malformed connector record reaches resolved retry bound. | Quarantine with reason, correlation ID, remediation; remaining batch may proceed with durable exception ledger. | BAT-002/003; [DDS], p. 29. |
| AC-BAT-009 | Provider issues `429` burst/`Retry-After`. | Capped retries; provider retry instruction honored where applicable; quota/fair scheduling/admission controls remain effective. | BAT-002/007; `TST-008`; [DDS], pp. 28, 49, 69, 89. |
| AC-BAT-010 | Ingest allowed file with agreeing MIME/extension under resolved cap. | Scan before parsing; macros not executed; remote references not fetched; durable normalization pipeline starts. | BAT-003; API-006; [DDS], pp. 30, 83. |
| AC-BAT-011 | Unsafe/polyglot/bomb or oversized/mismatched input. | Fail closed; unsafe input quarantined and never indexed. Exact boundary/code assertions await OQ-BAT-012. | BAT-003/004; `T-04`, `TST-015`; [DDS], pp. 30, 88–89. |
| AC-BAT-012 | Layout-rich PDF and opt-in OCR fixture. | Page/block anchors, table annotations, headings/order preserved; OCR fallback provenance marked. | BAT-003; DAT-022; [DDS], p. 31. |
| AC-BAT-013 | Reprocess source under changed pipeline version. | Side-by-side immutable derivatives; prior claims/citation lineage not overwritten. | BAT-003; DAT-006/007; [DDS], p. 31. |
| AC-BAT-014 | Low-quality extraction result. | Authorized viewing remains possible; material excluded from autonomous recommendations. | BAT-003/007; [DDS], p. 32. |
| AC-BAT-015 | Deliver normalized version for index build. | Search row includes required tenant/workspace/version/chunk/language/classification/text and 1536-dimensional vector; commit event supports cache invalidation. | BAT-004/006; DAT-023; [DDS], pp. 34, 87. |
| AC-BAT-016 | Fail index write after source metadata accepted. | Accepted source remains durable; reconciliation compares fingerprints and retries. | BAT-004/011; [DDS], p. 49. |
| AC-BAT-017 | Build replacement index generation. | Parallel rebuild; alias switches atomically only after completeness/recall checks. Failed/incomplete checks do not authorize switch. | BAT-005; DAT-023; [DDS], p. 34. |
| AC-BAT-018 | Revoke indexed source access before next query. | No forbidden evidence on next query; affected caches invalidated before serving results. | BAT-006; `TST-004`, `T-08`; [DDS], pp. 27–29, 53, 88–89. |
| AC-BAT-019 | Delete source before index removal completes. | Tombstone created; soft-deleted entity not retrievable; removal scheduled. | BAT-006/013; [DDS], pp. 28, 51. |
| AC-BAT-020 | Search mixed-permission corpus during AI workflow. | ACL filtering before text release to generation; ranking does not grant authorization. | BAT-007; API-009/045; [DDS], pp. 21–23, 34–36. |
| AC-BAT-021 | Insufficient/ambiguous evidence or missing citations. | `NO_SUPPORTED_EVIDENCE`, needs-review, or authorized human/clarification route; no fabricated context or unsupported publication. | BAT-007/008; `TST-009`; [DDS], pp. 36, 89. |
| AC-BAT-022 | Valid admitted Analyst run request. | API-011 returns `202`; run immediately durable; stages/checkpoints and scoped progress visible. | BAT-007; API-011/013/015; [DDS], pp. 49, 58, 83. |
| AC-BAT-023 | Run admission thresholds fail. | `429` plus `Retry-After`; no started-run success implied; saved cases remain available. | BAT-007; [DDS], p. 69. |
| AC-BAT-024 | DAG/tool invocation boundary reached or arbitrary tool proposed. | Depth/call bounds enforced; arbitrary MCP invocation denied before dispatch; no equivalent-tool substitution for a denied action. | BAT-007; `T-10`, `TST-014`; [DDS], pp. 40–42, 88–89. |
| AC-BAT-025 | Execute side-effecting plan and inject failure. | Plan revision precedes effects; each stage checkpoint precedes downstream dispatch; failed checkpoint reported. | BAT-007/010; DAT-008/009; [DDS], pp. 40–41, 49. |
| AC-BAT-026 | Hostile retrieved paragraph/tool directive. | Source remains untrusted; directives stripped from evidence context; injection indicators recorded; no tenant/tool/approval authority gained. | BAT-007; `T-02`; [DDS], pp. 38–39, 61, 88. |
| AC-BAT-027 | Force unknown fields, invalid citation, or control injection in model output. | `MODEL_OUTPUT_INVALID`; bounded parse retries; no publish. | BAT-007/008; `TST-005`; [DDS], pp. 38, 89. |
| AC-BAT-028 | Restricted-context provider outage. | No unapproved region/deployment fallback; approved equal-or-stronger handling class required. | BAT-007; `T-06`; [DDS], pp. 37, 88. |
| AC-BAT-029 | Exhaust current run quota. | Terminal current-run outcome; no automatic model/data-class switch; usage remains attributable under resolved accounting contract. | BAT-007/016; [DDS], p. 38. |
| AC-BAT-030 | Recompute policy from retained inputs/version. | Normalized inputs and rule version reproduce deterministic result; LLM risk tags cannot override. | BAT-007/008; DAT-017; [DDS], p. 44. |
| AC-BAT-031 | Approval event for exact unchanged authorized artifact. | Gate and final pointer atomically commit; exact required evidence/policy/approval satisfied. | BAT-008; DAT-025; [DDS], pp. 45–46. |
| AC-BAT-032 | Approval references prior/wrong hash. | Stale action rejected/audited; changed artifact not published under old approval. | BAT-008; `TST-006`, `T-03`; [DDS], pp. 45–46, 88–89. |
| AC-BAT-033 | High-risk author attempts self-approval. | Denied; no unapproved high-risk publication. | BAT-007/008; [DDS], pp. 11, 13. Broader scope remains NC. |
| AC-BAT-034 | Task reaches configured expiry. | No implicit approval; reassignment/escalation and required escalation evidence. | BAT-009; `TST-010`; [DDS], pp. 45, 89. |
| AC-BAT-035 | Replay publication event, including changed artifact attempt. | Exactly one accepted business transition; different artifact cannot publish using old approval. | BAT-008/010/012; `TST-007`; [DDS], pp. 45–50, 89. |
| AC-BAT-036 | Change source/case permission between retrieval and publication. | Gate recomputes authorization and rejects stale/unauthorized evidence. | BAT-006/008; [DDS], pp. 13, 46. |
| AC-BAT-037 | Rework denied/rejected candidate. | New run revision follows controls; old denial remains immutable. | BAT-007/008; DAT-008/012/025; [DDS], pp. 46, 75. |
| AC-BAT-038 | Interrupt case/approval transaction before commit. | Mutation and associated outbox do not partially commit. | BAT-010; `API-PROC-001`; [DDS], p. 52. |
| AC-BAT-039 | Deliver same event 100 times and delay/stale revisions across partitions. | One accepted business transition; duplicate/stale safety without cross-partition ordering assumption. | BAT-010/012; `T-07`, `TST-007`; [DDS], pp. 48, 88–89. |
| AC-BAT-040 | Invalid replay: missing reason, dry-run validation, or scope. | Replay cannot proceed as an uncontrolled job; valid replay preserves identity or explicit migration provenance. | BAT-012; API-038; [DDS], p. 50. |
| AC-BAT-041 | Delayed-index runbook recovery. | Faulty connector/shard only paused; accepted records retained; validated bounded replay; fingerprints/denied probes verified; incident evidence linked. | BAT-OPS-009; [DDS], p. 90, §F.1. |
| AC-BAT-042 | Run closed-case retention with mixed eligible/open/held cases. | Only eligible closed cases selected for case retention; legal-hold exceptions maintained. | BAT-013; DAT-LC-018; [DDS], p. 26. |
| AC-BAT-043 | Purge inventory contains held records. | Protected records retained and receipted; eligible removal verified; no false full purge. | BAT-013/014/021; `TST-013`; [DDS], pp. 66, 80, 89. |
| AC-BAT-044 | Apply diagnostic/audit retention. | Distinct policies and hold exceptions used; completion receipts recorded. Approved deployment policy remains prerequisite. | BAT-014; [DDS], pp. 66, 90. |
| AC-BAT-045 | Export/chaining audit batch and attempt historical edit. | Append-only batch-hash evidence exported independently; historical review/audit modification rejected. | BAT-015; `T-09`; [DDS], pp. 62, 88. |
| AC-BAT-046 | Produce daily usage reporting. | Separate usage categories retain tenant/workspace cost centers and deployment versions; budget/forecast/rejected-excess reporting available. | BAT-016; DAT-016/030; [DDS], p. 65. |
| AC-BAT-047 | Evaluate frozen reference corpus. | Expected citations/decisions preserved; quality targets and domain/statistical evidence reported; execution completion distinct from release pass. | BAT-017; DAT-031; [DDS], pp. 75–76. |
| AC-BAT-048 | Replace expected fixtures or produce low-confidence/critical-safety failure. | Signed/frozen fixture controls and release gates block acceptance/promotion; benchmark score cannot compensate. | BAT-017/026; `T-12`, `TST-016`; [DDS], pp. 74–76, 88–89. |
| AC-BAT-049 | Repeat provisioning or interrupt it partially. | One idempotent workflow outcome; incomplete state visible and blocks sync. Exact compensation awaits OQ-BAT-020. | BAT-018; [DDS], p. 78. |
| AC-BAT-050 | Backfill bounded history and inspect readiness. | Stable source IDs and per-batch reconciliation receipts; readiness depends on coverage, not empty queue. | BAT-019; [DDS], p. 78. |
| AC-BAT-051 | Single Admin requests export/deletion. | Independent approval checks prevent bypass. | BAT-020/021; `T-11`; [DDS], pp. 78, 83, 88. |
| AC-BAT-052 | Authorized controlled export. | Required metadata/approved artifacts/source references/audit manifests/checksums; secrets/internal prompts absent. | BAT-020; API-025; [DDS], p. 79. |
| AC-BAT-053 | Verify deletion and replay verification event. | Held exceptions/receipts preserved; `TenantDeletionVerified` closes purge record without duplicate business mutation. | BAT-021; [DDS], pp. 80, 87. |
| AC-BAT-054 | Compatible migration and old-reader drainage. | Nullable expansion, bounded backfill, postdeployment enforcement after drainage; no dependent field removed early. | BAT-022; [DDS], pp. 52, 72. |
| AC-BAT-055 | Canary regression during migration/release. | Automated traffic/binary rollback; no automatic DB down-migration; compensation only explicitly supported. | BAT-022/026; [DDS], pp. 20, 72. |
| AC-BAT-056 | Regional recovery/fault-injection exercise. | Safety and relational/object/index consistency verified; RPO `<=15 minutes`, RTO `<=4 hours`. | BAT-023; `TST-012`; [DDS], pp. 19, 69–70, 89. |
| AC-BAT-057 | Rotate credential/encryption key. | Vault/managed-identity scope preserved; no telemetry/prompt secret leakage; no request-path bulk reencryption requirement. | BAT-024; [DDS], pp. 21, 63. |
| AC-BAT-058 | Fail optional webhook after committed case change. | Case remains committed; signed delivery retries under resolved policy; recipient checks signature/age. | BAT-025; [DDS], p. 55. |
| AC-BAT-059 | Build/promote release with invalid identity/sign-off or safety regression. | Promotion blocked; valid release binds digest/schema/prompt/routing and signed test evidence. | BAT-026; [DDS], pp. 72–73, 88–89. |
| AC-BAT-060 | Foreign tenant/job scope or inherited pooled DB context. | Tenant guards and session reset prevent disclosure/mutation; foreign ID remains non-disclosing. | BAT-OPS-001; `T-01`, `TST-003`; [DDS], pp. 22–23, 86, 88–89. |
| AC-BAT-061 | Inspect traces, errors, provider requests, and exported content. | No out-of-scope documents, credentials, or internal prompts; required safe evidence remains correlated. | BAT-OPS-007; `T-05`; [DDS], pp. 62–66, 79, 84, 88. |
| AC-BAT-062 | Generation/vector degraded. | Manual case/evidence functions remain where supported; lexical-only quality flag visible; no approval/ACL bypass. | BAT-007; BAT-OPS-011; [DDS], pp. 68–70, 79. |

### No-Input and Empty-Selection Coverage

The source requires empty fixtures but defines only selected empty/insufficient-evidence outcomes. It does not establish a universal “zero rows means success,” exit code, receipt, or downstream-dispatch rule.

| Scenario | Source-supported expectation | Unresolved acceptance contract |
|---|---|---|
| Retrieval has insufficient confidence/quality or missing supported evidence | `NO_SUPPORTED_EVIDENCE` or supported needs-review/human path; no fabricated context/publication. | Exact HTTP/async representation and clarification routing. |
| Duplicate already-accepted event | Record duplicate outcome; return without reapplying mutation. | Exact consumer acknowledgment/result schema. |
| No source changes in connector delta | Cursor/outcome integrity and authorization controls still apply. | Whether cursor advances, successful no-change state, receipt/counts. OQ-BAT-009/011. |
| Extracted document has no usable text/empty pages | Record applicable quality information; low-quality material cannot support autonomous recommendations. | Thresholds, indexing eligibility, document state, retry/remediation. OQ-BAT-012. |
| No index-rebuild/backfill/migration rows | No source authority or compatibility rule may be bypassed. | Empty completeness/recall checks, success/no-op status, receipts, alias/enforcement behavior. OQ-BAT-009/013/020/022. |
| No expired review tasks | No task is implicitly approved. | No-op status/audit behavior and next timer/scan scheduling. OQ-BAT-009/015. |
| No eligible retention targets or all targets held | Held records protected; no ineligible removal. | Empty/all-held receipt and operation completion semantics. OQ-BAT-009/016. |
| No usage in reporting window | Attribution and reporting contracts remain applicable. | Omit versus zero rollup, budget/forecast behavior, correction identity. OQ-BAT-009/018. |
| Missing/empty evaluation corpus | Frozen expected-result integrity and critical-safety gates remain required. | Error/result status; never assume empty denominator means a passing score. OQ-BAT-009/019. |
| Empty export/deletion inventory | Independent approvals, authorized scope, and manifest/receipt controls remain applicable. | Empty package/no-op deletion, verification event, status/receipt representation. OQ-BAT-009/016/021. |
| No outbox/reconciliation/replay work | No duplicate/unauthorized mutation. | No-op run record, acknowledgment, completion notification, polling behavior. OQ-BAT-009. |
| Rotation policy selects no eligible credentials/keys | No out-of-scope secrets accessed or disclosed. | No-op verification and schedule behavior. OQ-BAT-009/024. |

**Sources:** [DDS], pp. 29, 32, 36, 45, 48–50, 66, 78–80, 89, §E.1.

**Needs confirmation — OQ-BAT-009:** Define no-input/empty-selection outcomes, exit/status codes, counts, receipts, and downstream behavior for every applicable job. These test expectations must be resolved before implementation-ready no-input assertions are finalized.

## Consistency and Open Questions

### Conflicts and Required Amendments

This document does not rewrite the preceding specifications. The following records identify source ambiguities, affected identifiers, and amendments required after explicit resolution.

| Conflict ID | Evidence / issue | Affected identifiers | Required resolution or amendment |
|---|---|---|---|
| CON-BAT-001 | Source confirms logical workflows but supplies no executable job inventory or scheduler definitions. | BAT-001–026; `OQ-DAT-001`; `OQ-API-027` | Resolve packaging/executor/scheduler contracts without treating assigned BAT IDs as confirmed deployment units. [DDS], pp. 12, 19, 26, 48–50, 65, 78. |
| CON-BAT-002 | Chapter 3 uses `POST /v1/runs`; Chapters 2/11 and §A.2 use case-scoped creation. | BAT-007; API-011/012; `CON-SCR-004`, `CON-API-001` | Define canonical/alternate launch and case-binding semantics; amend earlier mappings only after decision. [DDS], pp. 12–17, 40–42, 83. |
| CON-BAT-003 | Missing approval terminates run; `AWAITING_REVIEW` is valid; recoverable timeout absent from run vocabulary. | BAT-007/009; `CON-SCR-005`, `CON-API-002`, `CON-DAT-012` | Resolve valid waiting, missing-approval failure, timeout accounting and recoverability; keep review SLA separate. [DDS], pp. 12, 41, 45, 49, 82, 90. |
| CON-BAT-004 | Repeated chapter-boundary prose associates GETs with work allocation/events without precise triggers. | BAT-005/009–016/018/023/024/026; API read interfaces | Define actual triggers. Do not schedule jobs or write business events merely because a GET is associated with a chapter event. [DDS], corresponding sections pp. 8–80; `CON-API-007/014`, `CON-DAT-016`. |
| CON-BAT-005 | Common event envelope omits actor/correlation carriers required at durable boundaries. | BAT-COM-003; BAT-010/012; API-COM-006; DAT-EVT fields | Resolve carrier/schema; do not invent confirmed envelope extensions. [DDS], p. 48 and durable-boundary prose. |
| CON-BAT-006 | Unsupported capabilities cause lower-trust mode, while ACL/revocation enforcement is mandatory. | BAT-002/006; `CON-SCR-013`, `CON-API-010`, `CON-DAT-018` | Define safe restrictions; missing ACL support cannot permit unauthorized retrieval or delayed revocation. [DDS], pp. 21–23, 27–29. |
| CON-BAT-007 | Per-sync-run cursor/high-watermark/error ledger versus selected connector-keyed cursor fields. | BAT-002; DAT-015/021; `CON-DAT-011` | Define current cursor, run history, parallelism, durable exceptions, and cursor fencing. [DDS], pp. 28–29, 85. |
| CON-BAT-008 | Approval/purge/output data are partial selected-field catalogs; necessary task/hash/time/inventory fields omitted. | BAT-001/003/007–021; DAT field catalogs; API-GAP contracts | Complete job/data/wire schemas without dropping supported behavior or adopting proposed JSON mappings. [DDS], pp. 12, 31, 45, 78–80, 85–87. |
| CON-BAT-009 | Exact derivative identity uses fingerprint plus pipeline version while identifier baseline is UUIDv7. | BAT-003/004; `CON-DAT-003` | Define identity/uniqueness and parser/pipeline mapping; no hash-to-UUID algorithm inferred. [DDS], pp. 31, 51, 85. |
| CON-BAT-010 | Eligible closed-case retention coexists with independently approved workspace deletion and immutable closed lineage. | BAT-013/021; DAT-004/025/029; `CON-DAT-019` | Resolve deletion inventory, retained lineage, holds, and scope relationship. Do not infer all workspace targets must be closed or erase protected history by cascade. [DDS], pp. 26, 51, 62, 80. |
| CON-BAT-011 | Fictional 30-day/seven-year policies and Appendix F values coexist with explicitly open corporate/provider selections. | BAT-007/013–016/023/024; `CON-SCR-015`, `CON-API-015`, `CON-DAT-020` | Approve deployment values/precedence through dated decisions; examples remain examples. [DDS], pp. 66, 90. |
| CON-BAT-012 | Global 24-hour case-key contract and example `replay_dedup_hours: 24` have different scopes. | BAT-OPS-004; API-PROC-018; DAT-026 | Define per-ledger/request/stream retention; do not apply one TTL to all jobs. [DDS], pp. 25, 50, 55, 90. |
| CON-BAT-013 | `Admin`, `Workspace Admin`, operator, approver, elevated role, and service grants are incompletely mapped; self-approval scope varies. | BAT-002/007–009/012/017–026; existing role questions | Resolve role/action matrix without weakening high-risk prohibition or granting general Admin case access. [DDS], pp. 11, 22, 27, 46, 50, 83, 85, 90. |
| CON-BAT-014 | Source error prose says snake-case; examples use uppercase literals; many async states/errors absent. | BAT-OPS-005/007; `CON-API-009`, `CON-DAT-021` | Preserve exact literals; define canonical casing and job-specific status/error/result mappings. [DDS], pp. 54, 84, 89. |
| CON-BAT-015 | Source events `DeploymentPromoted`, `ReleasePromoted`, `TenantDeletionVerified`, and other repeated associations lack full trigger mapping. | BAT-020/021/026; API/DAT event inventories | Do not emit deletion verification for export/provisioning or promotion for health reads by association alone. [DDS], pp. 18–20, 71–80, 87. |
| CON-BAT-016 | Daily rollup content confirms aggregation cadence, not a standalone daily executable or midnight schedule. | BAT-016; SCR-010; API-022; DAT-030 | Define realization/day boundary/schedule and correction semantics without promoting prior gaps to decisions. [DDS], p. 65. |
| CON-BAT-017 | Source requires rotation/expiry/audit export behavior without selecting provider-managed versus application jobs. | BAT-009/014/015/024 | Resolve realization and operational contracts; do not create new runtime jobs from behavior alone. [DDS], pp. 45, 62–66. |
| CON-BAT-018 | Earlier files describe operational/batch details as future work. | Earlier handoff sections in `01_screen_functions.md`, `02_api.md`, `03_data.md` | Controlled amendments may link batch/background coverage to `04_batch_functions.md`; other later specifications remain ungenerated. |

### Open-Decision Register

All entries are **Needs confirmation**. No decision, owner, deadline, or approval is supplied.

| Open ID | Affected requirements | Missing decision / contract | Earlier linkage and evidence |
|---|---|---|---|
| <a id="oq-bat-001"></a>OQ-BAT-001 | BAT-COM-002; timer/daily/policy jobs | Schedules, scheduler timezone, DST, maintenance windows, missed/catch-up triggers, reporting-day boundaries. | `OQ-DAT-018/020/022`; [DDS], pp. 45, 51, 65, 78. Numeric schedules absent. |
| <a id="oq-bat-002"></a>OQ-BAT-002 | All job contracts; BAT-COM-003 | Full arguments/envelopes, selection predicates, types, requiredness/defaults, operation/result schemas and missing launch/status APIs. | [`02_api.md`](02_api.md): OQ-API-003/027/030/035; [`03_data.md`](03_data.md): OQ-DAT-003/024. |
| <a id="oq-bat-003"></a>OQ-BAT-003 | Executors; BAT-OPS-001 | Workload identities, service audiences/IAM, operator/approver roles, grants and independent authorization. | OQ-SCR-003; OQ-API-002/028; OQ-DAT-001/017; [DDS], pp. 18–23, 27, 46, 50, 83. |
| <a id="oq-bat-004"></a>OQ-BAT-004 | Inventory dependencies; BAT-OPS-002 | Deployment partition, parallelism, mutual exclusion, claims/fencing, same-scope conflict and worker ownership. | OQ-API-005/019/027; OQ-DAT-014/019; [DDS], pp. 25, 28, 34, 45, 48–50, 69. |
| <a id="oq-bat-005"></a>OQ-BAT-005 | BAT-OPS-003/006; BAT-003/008/010–022 | Transaction/commit units, checkpoint/ack ordering, cross-store coordination, isolation/locks and explicit compensation. | OQ-API-004/005/024/027; OQ-DAT-014; [DDS], pp. 40, 45, 49, 52, 80. |
| <a id="oq-bat-006"></a>OQ-BAT-006 | BAT-010/012; BAT-OPS-004 | Key scope/fingerprints/TTL, pending duplicates, result replay, event ledgers, schema migration, attribution and retention. | OQ-API-004/035; OQ-DAT-013/024; [DDS], pp. 25, 48–55, 90. |
| <a id="oq-bat-007"></a>OQ-BAT-007 | BAT-012; BAT-OPS-005 | Retry caps/backoff/circuit settings, deadlines, terminal disposition, heartbeat/lease, pause/resume/cancel, replay dry-run/scope protocol. | OQ-API-013/027/028/032; OQ-DAT-013/015; [DDS], pp. 29, 38–42, 49–50, 70. |
| <a id="oq-bat-008"></a>OQ-BAT-008 | BAT-OPS-007–011 | Metrics, queue/backlog/SLO thresholds, autoscaling, alert/ticket routing, actual assignments, notification/status contracts. | OQ-SCR-013/027/028; OQ-API-014/031/033; OQ-DAT-020/026; [DDS], pp. 19, 64–70, 79, 90. |
| <a id="oq-bat-009"></a>OQ-BAT-009 | No-input matrix; all applicable jobs | Empty-selection success/no-op/error, counts, receipts, exit/status codes, and downstream triggers. | [DDS], p. 89, §E.1 requires empty fixtures but most expected job outcomes are absent. |
| <a id="oq-bat-010"></a>OQ-BAT-010 | BAT-001 | Classification inputs/version/labels/confidences/provenance, attachment readiness, correction races, stale completion and failure/rerun. | OQ-SCR-007; OQ-API-008; DAT-020; [DDS], p. 12. |
| <a id="oq-bat-011"></a>OQ-BAT-011 | BAT-002/006/019 | Provider capability/permissions, cursor/history/order/expiration, sync state/bounds/concurrency, quarantine and lower-trust restrictions. | OQ-SCR-019; OQ-API-019/034; OQ-DAT-019; [DDS], pp. 27–29, 78, 85, 90. |
| <a id="oq-bat-012"></a>OQ-BAT-012 | BAT-003/004 | Exact upload/format/size/decompression/parser/OCR/quality/PII contracts, derivative serialization, unsafe versus low-quality outcomes. | OQ-SCR-009; OQ-API-009/010; OQ-DAT-008–010/017; [DDS], pp. 30–32, 62. |
| <a id="oq-bat-013"></a>OQ-BAT-013 | BAT-004–006/011; recovery runbooks | Embedding/search contracts, index commit/rebuild/catch-up, coverage/recall, cache/ACL atomics, reconciliation schedule/bounds/reenable controls. | OQ-API-011/019/027; OQ-DAT-011/012; [DDS], pp. 28, 34–36, 49, 53, 78–79, 90. |
| <a id="oq-bat-014"></a>OQ-BAT-014 | BAT-007 | Canonical run endpoint, case revision/rework, budget accounting, valid waiting/missing approval, runtime/recoverable timeout and A2A/MCP contracts. | OQ-SCR-012/013; OQ-API-012–014/028; OQ-DAT-015/024; [DDS], pp. 12–17, 40–42, 49, 82, 87, 90. |
| <a id="oq-bat-015"></a>OQ-BAT-015 | BAT-008/009 | Publication consumer/auto-allow/gate contract; reviewer pools/roles/SLA/late decisions/expiry races/self-approval/override. | OQ-SCR-003/014–017; OQ-API-015–018; OQ-DAT-016/021; [DDS], pp. 44–46, 58, 85. |
| <a id="oq-bat-016"></a>OQ-BAT-016 | BAT-013/014/021 | Approved retention, eligible scope/age, tombstone/hold/inventory/receipt, partial deletion, closed lineage, backup/audit survival and hold races. | OQ-SCR-025/026/030; OQ-API-024/025/034; OQ-DAT-007/018/025; [DDS], pp. 26, 51, 66, 78–80, 89–90. |
| <a id="oq-bat-017"></a>OQ-BAT-017 | BAT-015 | Audit batch ordering/hash/encoding, independent export format/destination/checkpoint/verification/cadence and rerun. | OQ-API-021; OQ-DAT-016/023; [DDS], p. 62. |
| <a id="oq-bat-018"></a>OQ-BAT-018 | BAT-016 | Daily reporting window/timezone, currency/units/precision, attribution/reservations, forecast, late corrections and rerun/zero-input rule. | OQ-SCR-023; OQ-API-022; OQ-DAT-020; [DDS], pp. 38, 65, 85. |
| <a id="oq-bat-019"></a>OQ-BAT-019 | BAT-017 | Dataset/request/result/status/progress, metric calculations/domains/confidence, partial fixture failures, signatures/timeouts/rerun. | OQ-SCR-024; OQ-API-023; OQ-DAT-022; [DDS], pp. 74–76, 88–89. |
| <a id="oq-bat-020"></a>OQ-BAT-020 | BAT-018/019 | Provisioning entry/status/role/completeness/order/compensation; historical windows/checkpoints/receipts/coverage and sync overlap. | OQ-SCR-026; OQ-API-025; OQ-DAT-018/019; [DDS], p. 78. |
| <a id="oq-bat-021"></a>OQ-BAT-021 | BAT-020 | Independent approvals, export inventory/snapshot, format/checksums/limits/lifetime, partial completion, status/download and rerun. | OQ-SCR-025; OQ-API-024; OQ-DAT-018/023; [DDS], pp. 78–79, 83, 88. |
| <a id="oq-bat-022"></a>OQ-BAT-022 | BAT-022/026 | Actual migration transformations/bounds/checkpoints/compatibility; pipeline/build/signatures/canary thresholds/sign-off/rollback. | OQ-API-027/030; OQ-DAT-022; [DDS], pp. 20, 52, 71–73, 88–89. |
| <a id="oq-bat-023"></a>OQ-BAT-023 | BAT-023 | Backup/provider/regions/retention/encryption, restore/write fencing/checkpoints, delete/hold propagation, drill cadence/RPO-RTO measurement. | OQ-API-033/034; OQ-DAT-018/025; [DDS], pp. 19, 69–70, 89. |
| <a id="oq-bat-024"></a>OQ-BAT-024 | BAT-024 | Rotation realization/policy/schedule, grace/reference switch/revocation/verification, key isolation/throughput and any background reencryption. | OQ-SCR-030; OQ-API-034; OQ-DAT-017/025; [DDS], pp. 10, 21, 63. |
| <a id="oq-bat-025"></a>OQ-BAT-025 | BAT-025 | Optional webhook subscription/event mapping/method/URL/payload/signature/age/ack/dedup/retry/redelivery. | OQ-SCR-027; OQ-API-029; OQ-DAT-024; [DDS], p. 55. |
| <a id="oq-bat-026"></a>OQ-BAT-026 | All integrations and capacity boundaries | Approved cloud/region/search/identity/model/connector choices, corporate retention, provider grants, capacity/quota and strict SLO interpretation. | OQ-SCR-030/031; OQ-API-033/034; OQ-DAT-020/025; [DDS], pp. 10, 65, 68–70, 90. |

### Proposal Status

| Proposal source | Status in this specification |
|---|---|
| `P-SCR-001`–`P-SCR-003` | Remain unapproved screen hierarchy, creation placement, and control-placement proposals. No batch console or job-control screen is established. |
| `P-API-001` | Remains unapproved token carrier; it does not select scheduler/service authentication or browser access to internal execution APIs. |
| `P-API-002` | Remains unapproved JSON mappings. Similarity to data or job concepts does not confirm runtime argument names. |
| New batch implementation proposals | None selected. Scheduler, executable partition, locking, physical ledgers, and retry settings remain unresolved decisions, not implementation discretion. |

### Dependencies and Later Handoffs

| Specification / dependency | Required handoff |
|---|---|
| [`01_screen_functions.md`](01_screen_functions.md) | Preserve SCR action/status/open-question IDs. Batch results support existing progress, connector, usage, evaluation, and unlocated operations; no routes, controls, consoles, or notification screens are added. |
| [`02_api.md`](02_api.md) | Preserve API and event IDs. Resolve missing launch/status/result contracts and errors by controlled amendment. Internal replay/storage/release APIs are not browser APIs by inference. |
| [`03_data.md`](03_data.md) | Preserve DAT fields, immutability, tenant predicates, revision/hash distinctions, outbox/checkpoint/receipt contracts, and wire-versus-storage gaps. No new physical job tables or columns are selected here. |
| Exception Handling Specification | **To be defined in a later stage.** Carry permanent/transient failure classification, failed checkpoint, quarantine, unsupported evidence, stale approval, exhausted retries, worker loss, partial completion, and safe errors. |
| Workflow / Business Rule Specification | **To be defined in a later stage.** Resolve review waiting/expiry/publication, closure/reopen/rework, retention eligibility, cursor trust, priority/calendar rules, and deterministic policy details. |
| Security / Nonfunctional Specification | **To be defined in a later stage.** Resolve workload/role grants, envelope/signature/vault protocols, ACL propagation, privacy, provider approvals, capacity, and precise SLO/recovery measurements. |
| Operations Specification | **To be defined in a later stage.** Complete scheduler/platform realization, monitoring/alert routing, release/failover procedures, and operator controls while preserving BAT IDs and unresolved conditions above. |
| Stage 8 architecture-decision consolidation | **To be defined in a later stage.** `08_architecture_decision.md` must consolidate unresolved items from completed Markdown specifications, linking to `04_batch_functions.md` BAT/OQ/CON identifiers and affected identifiers in the three preceding files. No decision, owner, deadline, or approval is invented here. |
