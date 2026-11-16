# 4. Batch Function Specification

## Batch Inventory and Triggers

### Specification Basis and Status

| Item | Definition |
|---|---|
| Output file | `04_batch_functions.md` |
| Application | OrionDesk AI |
| Source document | `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Baseline | `OD-AI-DDS-001`; release `R1.0`; design revision `1.3` |
| Source authority | Fictional reference architecture, normative for this sample application. Numeric targets are design assumptions, not measured production results. |
| Citation convention | **S** denotes `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf`. Citations identify original PDF pages and sections. |
| Completed preceding specifications | [Screen Function Specification](01_screen_functions.md), [API Specification](02_api.md), and [Data Specification](03_data.md) |
| Identifier convention | `BAT-001`–`BAT-026` identify logical background, batch, or operational workflow functions. The source does not assign batch job identifiers. Existing API, data, event, configuration, and test identifiers are preserved. |
| Confirmed | Explicitly supported by S. Confirmation of a background function does not establish a separate executable, deployment, queue, scheduler, or database table. |
| Needs confirmation | An unresolved operational or implementation contract. It does not authorize an implementation AI to choose a schedule, schema, threshold, lock, status, error code, or approval workflow. |
| Proposal | An explicitly suggested design, not an approved requirement. Earlier UI arrangements, API example bodies, and SSE examples remain Proposals. |
| Later specifications | Detailed non-batch processing, exception handling, and remaining specifications are **To be defined in a later stage**. Stage 8 decision consolidation has not been generated. |

**BAT-SCP-001 — Confirmed:** Batch and background processing is required. The source explicitly describes asynchronous case classification, connector batches, extraction and indexing workers, durable AI workflows, reconciliation, retention jobs, daily usage rollups, evaluations, provisioning, historic backfill, export, deletion, and controlled replay.  
**Source:** S, p. 12, §2.2.1; pp. 27–32, Chapters 7–8; pp. 48–50, Chapter 13; p. 65, §18.3.1; pp. 74–80, Chapters 21–22.

**BAT-SCP-002 — Confirmed:** This specification covers scheduled batches, event-driven consumers, request-created asynchronous operations, and source-described operational automation. Event-driven processing must not be converted into periodic polling merely because it appears in a batch specification.  
**Source:** S, p. 17, §3.3.2; pp. 48–50, Chapter 13; p. 87, Appendix C.1.

**BAT-SCP-003 — Needs confirmation:** The deployment grouping of these logical functions, scheduler product, queue topology, executable names, commands, job registration schema, and exact service identities. No standalone executable or additional API is selected here. See **BAT-OQ-002**.

### Execution Context and Time Rules

| Requirement ID | Status | Requirement | Source / adjacent decision |
|---|---|---|---|
| BAT-CTX-001 | Confirmed | Background jobs carry immutable tenant identity in signed envelopes. Tenant-owned storage reads and writes use tenant-scoped predicates and RLS. | S, p. 22, §5.3.1; p. 51, Chapter 14 invariant. Earlier `API-AUTH-003`, `DAT-RI-001`. |
| BAT-CTX-002 | Confirmed | Authenticate and authorize service calls independently. Use scoped service identities, audience checks, TLS, and managed workload identity where supported. Do not share an identity between deployment units. | S, pp. 16 and 18, §§3.3.1 and 4.1.2. Exact identities/scopes: **BAT-OQ-002**. |
| BAT-CTX-003 | Confirmed | The orchestrator has no direct database credentials; it uses narrow scoped APIs. Other workers must remain within their declared service and storage authority. | S, p. 9, §1.3.1; p. 16, §3.2.1. |
| BAT-CTX-004 | Confirmed | Durable mutation evidence retains tenant, revision, actor, occurrence time, and correlation context. Event envelopes use UTC and canonical JSON. | S, p. 48, §13.1.1; chapter interface-boundary requirements. Earlier `API-EVT-001`, `DAT-COM-F02–06`. |
| BAT-TIME-001 | Confirmed | Durable server timestamps are UTC; exposed public timestamps use RFC 3339. | S, p. 54, §15.1.1; p. 59, §16.3.2. |
| BAT-TIME-002 | Needs confirmation | Scheduler timezone, daily accounting timezone, launch clock times, daylight-saving handling, maintenance windows, missed-launch behavior, and cutoff inclusivity. UTC storage does not establish UTC scheduling. | S, pp. 26, 51, 65–66, 78 provides no complete schedule. **BAT-OQ-001**, **BAT-OQ-016**. |
| BAT-TIME-003 | Confirmed | Case contractual deadlines use workspace timezone and business calendars. This does not establish that review-task expiry or daily cost rollups use the same calendar. | S, p. 25, §6.3.1. Earlier `DAT-TIME-003`; **BAT-OQ-013**, **BAT-OQ-016**. |
| BAT-CTX-005 | Confirmed | Validate accepted request/job arguments before long-running allocation, again at domain invariants, and before tool dispatch. Rejected stale or unauthorized writes leave business state unchanged. | S, p. 56, §15.3.2; pp. 25 and 45, design checkpoints. |
| BAT-CTX-006 | Confirmed | Workers use private network resources and declared, NAT-controlled egress. No datastore has a public IP endpoint. Production data is forbidden in development; staging uses synthetic data and test connectors. | S, pp. 18–19, §§4.1–4.3. |

In the launch register below, **“Timezone unresolved”** means BAT-TIME-001 applies to durable timestamps, while the scheduling or selection timezone remains Needs confirmation.

### Logical Job Inventory

| Job ID | Name and purpose | Executing actor or boundary | Related API and data identifiers | Source |
|---|---|---|---|---|
| BAT-001 | Case classification: attach policy-aware labels, confidences, and provenance | Classifier / Triage Agent; exact runtime identity Needs confirmation | API-001, API-051; DAT-003, DAT-024 | S, p. 12, §2.2.1; p. 40, §11.1.1; p. 87, C.1 |
| BAT-002 | Incremental connector synchronization: ingest source changes while preserving identity, ACLs, cursor progress, and exceptions | Connector workers; initiating API scope `Admin` | API-009, API-025; DAT-005, DAT-015, DAT-027–028 | S, pp. 27–29, Chapter 7 |
| BAT-003 | Document scanning, extraction, normalization, and provenance generation | Ingestion Service / extraction workers | API-004, API-018; DAT-005–007, DAT-023, DAT-029–030, DAT-035 | S, pp. 30–32, Chapter 8; p. 19, §4.2.1 |
| BAT-004 | Embedding and search-index build for normalized versions | Indexer / embedding workers | API-010, API-021–022 as consumers, not launch APIs; DAT-006–007, DAT-031–032 | S, pp. 19 and 34, §§4.2.1 and 9.1; p. 87, C.1 |
| BAT-005 | Parallel index rebuild and atomic read-alias switch | Index lifecycle boundary; exact executing service identity Needs confirmation | DAT-031–032; API-010, API-021–022 | S, p. 34, §9.1.2 |
| BAT-006 | Authorization and index-generation cache invalidation | Cache/retrieval boundary; exact executor Needs confirmation | DAT-022, DAT-034; API-010, API-021–022 | S, p. 28, §7.2.2; p. 53, §14.3.2; p. 87, C.1 |
| BAT-007 | Source-deletion index removal | Source-sync/index boundary; exact removal executor Needs confirmation | DAT-005–007, DAT-031–032; API-009, API-025 | S, p. 28, §7.2.2 |
| BAT-008 | Durable outbox delivery and workflow-stage consumer dispatch/resumption | Platform messaging boundary and applicable consumers | API-033; DAT-014, DAT-045–046, DAT-048 | S, p. 17, §3.3.2; pp. 48–50, Chapter 13; p. 87, C.1 |
| BAT-009 | Source/index and broken-message-link reconciliation | Reconciliation worker | API-033; DAT-006, DAT-014, DAT-031–032, DAT-045–047 | S, p. 49, §13.2.2 |
| BAT-010 | Bounded grounded-answer AI workflow | Orchestrator, Research Agent, Draft Agent, model gateway, deterministic Policy Evaluator; request initiated by `Analyst` | API-005–008, API-019, API-032, API-046–047; DAT-008–010, DAT-016–017, DAT-036–042, DAT-046 | S, pp. 37–42, Chapters 10–11; p. 49, §13.2.1 |
| BAT-011 | Exact-artifact publication validation and commit | Publication/policy boundary; exact consumer identity Needs confirmation | API-020, API-024; DAT-003-F15, DAT-010–012, DAT-017, DAT-039, DAT-043 | S, pp. 44–46, Chapter 12; p. 87, C.1 |
| BAT-012 | Review-task expiry, reassignment, or escalation | Review-routing boundary; exact executor Needs confirmation | API-023–024; DAT-011-F05–07, DAT-012 | S, p. 45, §12.2.1; p. 89, `TST-010` |
| BAT-013 | Eligible closed-case retention and scheduled tombstone purge | Retention/storage boundary; exact executor Needs confirmation | API-017, API-036; DAT-003–007, DAT-018, DAT-026, DAT-035, DAT-053 | S, p. 26, §6.3.2; pp. 51–53, Chapter 14 |
| BAT-014 | Diagnostic and security-audit retention purge | Diagnostic/audit retention boundary; exact executor Needs confirmation | API-040 is inquiry only; DAT-013, DAT-018, DAT-054 | S, p. 66, §18.3.2; p. 90, Appendix F |
| BAT-015 | Audit batch hashing and independently controlled archive export | Audit-ledger/archive boundary; exact executor Needs confirmation | API-011 is inquiry only; DAT-013; DAT-STO-007 | S, p. 62, §17.3.1 |
| BAT-016 | Daily usage and cost rollups | Cost/usage processing boundary; exact executor Needs confirmation | API-012; DAT-002-F12, DAT-016, DAT-054-F04 | S, p. 65, §18.3.1 |
| BAT-017 | Frozen benchmark evaluation and scorecard production | Evaluation harness; initiating scope `Admin` | API-013, API-045; DAT-057 | S, pp. 74–76, Chapter 21; p. 83, A.2 |
| BAT-018 | Idempotent tenant/workspace provisioning | Provisioning workflow; exact initiating and executing roles Needs confirmation | API-056; DAT-001–002, DAT-020, DAT-027, DAT-052, DAT-058 | S, p. 78, §22.1.1 |
| BAT-019 | Historic document backfill with per-batch reconciliation | Onboarding/ingestion workflow; exact actor Needs confirmation | DAT-005–007, DAT-028–032, DAT-058; API-009 relationship Needs confirmation | S, p. 78, §22.1.2 |
| BAT-020 | Controlled export packaging | Export workflow; initiating scope `Admin + approver`, with two independent approval checks | API-014; DAT-003, DAT-013, DAT-039, DAT-059 | S, pp. 78–79, Chapter 22; p. 83, A.2 |
| BAT-021 | Legal-hold-safe deletion and verification | Deletion workflow; Retention Worker produces verification event; initiating scope `Admin + approver` | API-015, API-036; DAT-018, DAT-035, DAT-053, DAT-059 | S, pp. 78–80, Chapter 22; p. 87, C.1 |
| BAT-022 | Bounded operator-controlled dead-letter/outbox replay | Authorized operator and replay execution boundary | API-034; DAT-014, DAT-045–048 | S, p. 50, §13.3.2; p. 90, F.1 |
| BAT-023 | Bounded schema backfill and postdeploy constraint enforcement | Migration/release tooling; exact runtime actor Needs confirmation | API-043–044; DAT-056-F03; DAT-MIG-001–002 | S, p. 52, §14.2.2; p. 72, §20.2.2 |
| BAT-024 | Optional signed outbound webhook delivery and retry | Outbound delivery boundary; exact executor Needs confirmation | API-048; DAT-050 | S, p. 55, §15.2.2 |
| BAT-025 | Continuous backup and controlled recovery verification | Backup/recovery platform; restoration under incident command | DAT-055-F02; DAT-REC-001; API-038–039, API-041–042 are related inquiries only | S, p. 19, §4.2.2; pp. 69–70, §19.3 |
| BAT-026 | Build, verification, canary, and release-promotion automation | CI/deployment tooling; Security and SRE sign-off; security-control evidence review | API-043–044; DAT-056–057, DAT-060–061 | S, pp. 71–76, Chapters 20–21; pp. 88–89, D.1 and E.2 |

All listed functions have source-supported behavior. Their separation into the above logical IDs is an analytical inventory, **not confirmation that twenty-six independently deployed jobs exist**. See **BAT-OQ-002**.

### Trigger, Manual Launch, and Dependency Register

Predecessors and successors below describe supported data or workflow dependencies. They do not establish a new unconditional execution chain.

| Job | Trigger, cadence, and timezone | Manual execution | Predecessor / prerequisite | Successor or dependent behavior |
|---|---|---|---|---|
| BAT-001 | `CaseCreated`; event-driven; UTC event time | Separate reclassification launch contract Needs confirmation | Accepted case creation through API-001; authorized case/revision | Classification available to case/triage workflows. Automatic `NEW → TRIAGED` linkage Needs confirmation. |
| BAT-002 | API-009 request; periodic/provider-push triggers Needs confirmation; timezone unresolved | `POST /v1/connectors/{connectorId}/sync`, `Admin`, HTTP `202` | BAT-018 provisioning complete; configured connector, usable credentials, capabilities, quotas | Durable ingestion outcomes; BAT-003, BAT-006, or BAT-007 as applicable |
| BAT-003 | Accepted attachment ingestion through API-004 or connector ingestion; exact connector handoff schema Needs confirmation | Upload through API-004, `Analyst`, HTTP `202`; standalone reprocessing launch Needs confirmation | Accepted allowed file and source context; scanning before parsing | `DocumentNormalized` → BAT-004; quarantine prevents indexing |
| BAT-004 | `DocumentNormalized`; event-driven | Independent index-build API/command Needs confirmation | BAT-003 normalized immutable version and chunks | `SearchIndexCommitted` → BAT-006; evidence becomes available subject to readiness/access checks |
| BAT-005 | Rebuild operation supported; initiating event, API, or cadence Needs confirmation; timezone unresolved | Actor/API/command Needs confirmation | Authoritative source inventory; rebuild generation; completeness and recall validation | Atomic read-alias switch; index-commit/cache effects |
| BAT-006 | Source ACL/authorization change or `SearchIndexCommitted`; no named ACL-change event supplied | Standalone invalidation control Needs confirmation; incident containment exists | Updated authoritative ACL or committed index generation | Subsequent retrieval excludes unauthorized/stale cached evidence |
| BAT-007 | Source deletion creates tombstone and schedules index removal; exact schedule/timezone unresolved | Independent removal launch Needs confirmation | BAT-002 detected source deletion and durable tombstone | Removal of affected search derivatives; later storage purge subject to policy |
| BAT-008 | Committed outbox work; `AgentPlanApproved` dispatch; `WorkflowStageAdvanced` resumes consumers | Normal manual relay launch Needs confirmation; controlled replay is BAT-022 | Durable business/outbox commit or stage checkpoint | Applicable consumers, including BAT-001, BAT-004, BAT-006, BAT-010, BAT-011 |
| BAT-009 | Failed index write or broken message link; detection cadence/timezone unresolved | Operator-controlled incident recovery uses BAT-022; separate reconciliation command Needs confirmation | Authoritative fingerprints, derivative inventory, outbox ledger | Retry missing derivative effects and repair message links |
| BAT-010 | API-005 request; Chapter 3 API-032 route relationship unresolved; `AgentPlanApproved`/`WorkflowStageAdvanced` for execution | `POST /v1/cases/{caseId}/runs`, `Analyst`, HTTP `202`; end-user retry/cancel not established | Authorized saved case, admission thresholds, approved deployments/tools, permitted evidence | Candidate and policy records; review tasks when required; BAT-011 only when gate requirements can be satisfied |
| BAT-011 | `ApprovalDecisionRecorded` consumer action; non-review gate invocation Needs confirmation | No public Publish endpoint or manual control confirmed | Exact candidate/hash, evidence/current access, policy and required approval satisfaction | Atomic approved-result pointer/publication; optional BAT-024 if subscribed |
| BAT-012 | Configured review SLA expires; timer versus scanning batch Needs confirmation; timezone unresolved | Forced expiry/reassignment control Needs confirmation | Applicable review task and configured eligibility/routing | Reassignment or escalation; no implicit approval |
| BAT-013 | Retention eligibility and scheduled tombstone pipeline; frequency/timezone unresolved | API-036 exists; authorized scope, request, and result unresolved | Eligible `CLOSED` case for routine case retention; separately eligible tombstone inventory for final purge; legal holds | Purge receipts and `DataRetentionPurgeCommitted` where applicable |
| BAT-014 | Diagnostic/audit TTL eligibility; purge cadence/timezone unresolved | Manual purge contract Needs confirmation | Applicable retention policy and hold evaluation | Completion receipts and hold exceptions |
| BAT-015 | Append-only audit ledger; batch/export cadence/timezone unresolved | Manual archive/export contract Needs confirmation | Accepted audit evidence and defined batch-chain/archive format | Independently controlled retained audit archive |
| BAT-016 | **Daily rollups Confirmed**; launch time and reporting timezone unresolved | Rerun/backdated rollup API/command Needs confirmation | Attributed usage, budget, quota/rejected-request data | Usage inquiry API-012 and operational cost reporting |
| BAT-017 | API-013 request; prompt/model changes require re-evaluation; deployment test pack includes evaluations | `POST /v1/evaluations`, `Admin`, HTTP `202` | Frozen versioned independently reviewed corpus; expected outcomes; evaluated versions | `EvaluationCompleted`; scorecard and release-gate evidence |
| BAT-018 | Provisioning workflow required; initiating API/event/timezone unresolved | API-056 method/path and role unresolved | Validated authorized tenancy/workspace configuration | BAT-002 sync can proceed only after completion; onboarding BAT-019 |
| BAT-019 | Historic onboarding/backfill; bounded windows; calendar schedule/timezone unresolved | Operational initiation supported in concept; command/API/role unresolved | Stable source IDs, configured source access, bounded inventory/windows | BAT-003/BAT-004; reconciliation receipts and coverage-based readiness |
| BAT-020 | API-014 request; no periodic export schedule confirmed | `POST /v1/workspaces/{workspaceId}/export`, HTTP `202`, independent checks | Authorized scope and two independent approval checks | Export package/manifest; no export-specific completion event supplied |
| BAT-021 | API-015 request; no periodic decommission schedule confirmed | `POST /v1/workspaces/{workspaceId}/delete`, HTTP `202`, independent checks | Authorized scope, two independent approval checks, inventory, legal holds | Tombstones, eligible removals, receipts; `TenantDeletionVerified` closes purge record |
| BAT-022 | Authorized operator request after failure/incident | `POST /internal/deadletters/{id}/replay`; bounded validated outbox recovery also described in F.1 | Operator reason, dry-run validation, scope limit, original event/provenance | Resume affected consumers without duplicate business effects |
| BAT-023 | Approved migration/release; predeploy addition/backfill and postdeploy enforcement after old replicas drain | Release/migration tooling; exact command and permissions unresolved | Backward-compatible migration plan; bounded backfill; compatibility evidence | Constraints enforced only after prerequisites; BAT-026 promotion/rollout context |
| BAT-024 | Optional subscribed committed event/transition; retries follow exponential backoff | Subscription/delivery replay administration Needs confirmation | Committed internal change, authorized recipient configuration, signing context | Recipient notification; failure does not reverse business state |
| BAT-025 | PostgreSQL **continuous backups**; restore only under incident command; exercises required, cadence unresolved | Controlled restoration/exercise; command and actor permissions unresolved | Primary-region profile; backup/object-version inventory and index rebuild recipes | Consistent recovery and measured RPO/RTO evidence |
| BAT-026 | CI/deployment pipeline; exact repository/pipeline trigger and schedule unresolved | `POST /internal/releases` exists; request/actor/result contract unresolved | Signed build/configuration, required tests, migration compatibility, canary and sign-off | Verified promotion and reconstructible release record; regression traffic rollback |

**Sources:** S, pp. 12, 26–32, 34, 40–42, 45, 48–55, 62, 65–66, 69–80; pp. 83 and 87–90, Appendices A–F.

**Needs confirmation — BAT-OQ-001:** All unspecified schedules, timer mechanisms, windows, cutoff boundaries, and missed-run behavior. “Daily,” “continuous,” “scheduled,” and “configured SLA” retain their source meanings without an invented cron expression.

### Explicit Boundaries and Functions Without a Confirmed Batch Implementation

| Category | Status and boundary | Source / decision |
|---|---|---|
| Foundation-model fine-tuning, unrestricted browsing, physical automation, irreversible financial transactions, agent administrative cloud permissions | **Out of scope:** explicitly excluded. No such batch jobs may be introduced. | S, p. 9, §1.2.1 |
| Application-hosted GPU inference | **Out of scope:** model providers are external dependencies. Extraction and embedding workers remain supported. | S, p. 19, §4.2.1 |
| Cross-region active/active mutation, OCR beyond English, customer-managed model weights | **Deferred from R1.0:** do not add enabled job modes. Opt-in English OCR remains supported. | S, p. 10, §1.3.2; p. 31, §8.2.1 |
| Secrets/internal model prompts in export | **Out of scope for export contents:** explicitly excluded. | S, p. 79, §22.3.1 |
| Service credential and encryption-key rotation | Capability **Confirmed**; whether an application batch job, provider-managed automation, or separate workflow is required **Needs confirmation**. Processing boundary is recorded below without inventing a job. | S, p. 21, §5.1.2; p. 63, §17.3.2; **BAT-OQ-023** |
| Priority/SLA recomputation or breach-prediction batch | Business rules exist, but no separate batch job or recalculation schedule is described. **Needs confirmation.** | S, p. 25, §6.3.1; earlier `DAT-003-F11–17` |
| Dashboard refresh, email digest, notification cleanup, cache TTL sweep, automatic reauthorization, automatic reclassification | No independent job contract is supplied. **Needs confirmation**, not Out of scope. | S, pp. 16, 27, 57–59; **BAT-OQ-003**, **BAT-OQ-025** |
| Health, metrics, capacity, usage, and OpenAPI GET requests | Inquiry endpoints do not establish scheduled business jobs or chapter-event side effects. | Earlier `API-CNS-011`, `DAT-LIFE-001`; S, Chapters 4, 15, 18–19 |
| Ordinary human approval/rejection | Interactive decision transaction, not an autonomous approval batch. Its downstream consumer and expiry behavior are BAT-011/BAT-012. | S, pp. 44–46, Chapter 12 |

## Processing by Job

### Shared Argument and Record Contract

The tables below define **semantic arguments and selection criteria**, not newly approved JSON properties, command-line flags, or SQL columns. Exact transport, required-field sets, types, lengths, nullability, and defaults remain governed by the preceding API/data questions and **BAT-OQ-003**.

| Argument or context | Applicability | Confirmed meaning and constraints | Earlier mapping / source |
|---|---|---|---|
| `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, `payload` | Event-driven processing | Required source event envelope; UTC and canonical JSON; event identity/revision support deduplication and stale detection | `API-EVT-001`; DAT-014/DAT-048 envelope. S, p. 48, §13.1.1 |
| Actor and correlation context | Durable mutations | Trusted responsible actor and correlation retained; exact envelope placement not specified | `DAT-COM-F04–06`; S, chapter interface-boundary requirements |
| `Idempotency-Key` | Job-creating POSTs and confirmed case creation | Same key and identical fingerprint returns original outcome; changed fingerprint returns `IDEMPOTENCY_CONFLICT` | `API-IDEM-002–003`, `DAT-CNC-003–004`. S, pp. 25 and 54 |
| Resource identity and scope | All resource jobs | Resolve authorized tenant/workspace/case/document/run/connector/task/object context; no default tenant or unrestricted scope | API shared path parameters; `DAT-RI-001–005`. S, pp. 21–23 and 51 |
| Current resource revision | Applicable writes | Reject stale writes before business mutation; case `revision` is `BIGINT`; other revision transport remains unresolved | `API-CNC-001–004`, `DAT-CNC-001–002`. S, pp. 24–25 |
| Pipeline, plan, prompt, deployment, rule-set, dataset, and index versions | Relevant processing | Preserve the specific versions needed to reproduce derivatives, decisions, and release evidence; do not collapse distinct revision concepts | DAT-006, DAT-008, DAT-017, DAT-032, DAT-036–037, DAT-057. S, pp. 31, 34, 37–45, 74–76 |
| Window, batch, cutoff, or inventory scope | Backfill, rollup, purge, rebuild, replay | Bounded scope where source requires it; no numeric batch/window default supplied | DAT-058; `DAT-MIG-001`; API-034. S, pp. 50, 52, 78, 90 |
| Operator reason, dry-run validation, scope limit | BAT-022 | Required replay prerequisites, not optional conveniences | API-034; DAT-047-F02. S, p. 50, §13.3.2 |
| Independent approval context | BAT-020/BAT-021 | Two independent approval checks; `Admin + approver`; exact proof/actor mapping unresolved | API-014–015; DAT-059. S, pp. 78 and 83 |

### BAT-001 — Case Classification

| Aspect | Contract |
|---|---|
| Arguments and inputs | `CaseCreated` with Case ID/revision; authorized case business context and applicable attachments. Exact case-revision/attachment snapshot is **Needs confirmation**. |
| Extraction conditions | Consume an eligible, nonduplicate event and resolve its authorized case context. Stale-event handling must not overwrite a newer accepted correction or revision. The correction-versus-classifier rule is unresolved. |
| Update targets | DAT-024-F01–03: labels, confidences, provenance. Any associated case mutation uses Case Service revision/history controls. |
| Outputs | Policy-aware classification attached to the case; safe correlated processing evidence. No classifier-completed event name is supplied. |
| Successful completion | Supported labels/confidences/provenance are durably attached to the applicable case context without unauthorized/stale mutation. Exact completion state and empty-classification representation are unresolved. |
| APIs and fields | API-001; API-051 is user correction, not a confirmed rerun endpoint. DAT-003-F01–03/F09–10; DAT-024-F01–04. |

1. Validate the event envelope, tenant identity, and case reference.
2. Deduplicate by event identity/operation context and check aggregate revision.
3. Obtain the authorized case business context through the appropriate scoped boundary.
4. Execute policy-aware classification using the classifier/Triage Agent responsibility.
5. Attach labels, confidences, and provenance through a revision-safe durable operation.
6. Preserve correction provenance; a user label correction requires a reason code.
7. Retain correlated accepted-outcome evidence.

**Source:** S, p. 12, §2.2.1; p. 40, §11.1.1; p. 87, C.1; pp. 25 and 48, consistency controls.  
**Needs confirmation — BAT-OQ-006:** Label/reason catalogs, confidence format, classifier input snapshot, update API/schema, correction precedence, missing-context behavior, and rerun rules. Classification completion does not automatically authorize `SCR-002-T01`.

### BAT-002 — Incremental Connector Synchronization

| Aspect | Contract |
|---|---|
| Arguments | Authorized `connectorId`, accepted sync operation, `Idempotency-Key`, tenant/workspace context. Request options and cursor override are not confirmed. |
| Inputs and selection | Configured repository, advertised capabilities, workspace secret reference, stored provider cursor/high-watermark, provider changes, source IDs/ACLs/deletions. Provider ordering and page/window bounds are unresolved. |
| Update targets | DAT-015-F01–04: `connector_id`, `cursor`, `watermark`, `retry_state`; DAT-028 cursor/high-watermark/error ledger/item outcomes; DAT-005 source metadata and ACL linkage. |
| Outputs | Durable sync outcomes, `ConnectorSyncStarted`, ingestion handoffs, visible lower-trust warnings, quarantine reason/correlation/remediation information. |
| Successful completion | Cursor advances only past preceding items with durable ingestion outcomes. Recorded quarantine exceptions can permit the remaining batch to proceed. Search readiness is not implied by cursor advancement. |
| Related APIs | API-009 `POST /v1/connectors/{connectorId}/sync`, HTTP `202`; API-025 `GET /v1/connectors/{connectorId}/runs`. |

1. Validate the request and `Admin` authorization before allocating work.
2. Confirm provisioning completion, connector scope, quota, and usable credentials.
3. Read advertised list, fetch, delta cursor, ACL, and delete capabilities.
4. Apply lower-trust ingestion mode and a visible warning for unsupported capabilities; do not assume missing support.
5. Resume from durable provider progress and obtain incremental items.
6. For each item, preserve stable source identity, permission, and change-history context; initiate the applicable ingestion or deletion/ACL handling.
7. Persist each durable item outcome, including poison-record exceptions.
8. Advance the cursor only after all preceding items have durable outcomes; retain high-watermark and error ledger.
9. Honor provider `Retry-After`, bounded exponential backoff with jitter, workspace quotas, and fair scheduling.
10. Expose safe run outcomes through the existing inquiry boundary.

Queued work with revoked credentials fails with `CONNECTOR_REAUTH_REQUIRED`, without token disclosure. Malformed documents enter quarantine after bounded retries; remaining batch work **may** proceed with the ledger exception.

**Source:** S, pp. 27–29, §§7.1–7.3; p. 78, §22.1.1; p. 83, A.2.  
**Needs confirmation — BAT-OQ-007:** Providers/permissions, cursor semantics, durable-outcome definition, batch bounds, retry limits, concurrent sync policy, safe inquiry schema, and mixed-outcome completion status.

### BAT-003 — Document Scanning, Extraction, and Normalization

| Aspect | Contract |
|---|---|
| Arguments | Accepted source/file operation, immutable document/version context, parser/pipeline version, optional OCR opt-in, trusted scope. |
| Inputs and selection | Allowed PDF, DOCX, HTML, or UTF-8 text with agreeing MIME signature/extension and configured per-file cap `25 MB`; decompression safety applies. |
| Transformation | Scan → safe parsing → layout segmentation → normalization → chunk/provenance and quality output. This ordering does not define a complete status transition matrix. |
| Update targets | DAT-006 version/hash/parser/object linkage; DAT-007 chunk/version/page/optional `bbox`/text hash; DAT-029 status/quality/quarantine/OCR provenance; DAT-030 blocks/table annotations; DAT-035 objects. |
| Outputs | Immutable text/layout/metadata derivatives and `DocumentNormalized`; unsafe input is quarantined without indexing. |
| Successful completion | Authorized immutable derivatives preserve claims and source anchors; quality information is stored. Extraction completion is not indexing completion. |

1. Validate type, extension agreement, size, and decompression safety before long-running allocation.
2. Scan the uploaded content before parsing.
3. Disable macro execution and do not fetch embedded remote references.
4. Quarantine unsafe content and prevent its entry into BAT-004.
5. Parse PDF pages into blocks with page indices and bounding boxes.
6. Preserve table row/column annotations; use headings and reading order to determine chunk boundaries.
7. Use OCR fallback only when opted in, and mark generated OCR provenance. OCR beyond English is deferred.
8. Strip transport artifacts without rewriting source claims.
9. Derive immutable derivative identity using content fingerprint and pipeline version; support side-by-side reprocessing.
10. Preserve source URI, file hash, page number, and optional bounding box for every chunk.
11. Record empty-page ratio, unknown-character ratio, table-loss indicators, language confidence, and applicable likely-personal-data tags.
12. Persist the accepted derivatives and correlated `DocumentNormalized` effect.

Safe low-quality documents remain viewable but are excluded from autonomous recommendations. The source does not say that every low-quality document is excluded from indexing, nor that quarantined unsafe content may be viewed.

**Related APIs:** API-004 `POST /v1/cases/{caseId}/attachments`, HTTP `202`; API-018 `GET /v1/documents/{documentId}/status`.  
**Source:** S, pp. 30–32, §§8.1–8.3; p. 62, §17.2.2; p. 83, A.2.  
**Needs confirmation — BAT-OQ-008:** MB conversion, archive threshold, subtype/MIME catalog, file counts, parser sandbox bounds, quality formulas/thresholds, empty-document treatment, derivative-ID algorithm, status transitions, attempt/resume units, and reprocessing launch contract.

### BAT-004 — Embedding and Search-Index Build

| Aspect | Contract |
|---|---|
| Arguments | `DocumentNormalized` version/source-hash context; authorized document/chunk inventory and index generation. |
| Selection | Applicable immutable normalized chunks. Unsafe quarantined attachments must not enter the index. Source authority, tombstones, ACLs, and classification remain applicable. |
| Transformation | Produce searchable rows containing tenant/workspace/version/chunk/language/classification, `1536`-dimensional embedding, and normalized keyword text. |
| Update targets | DAT-031-F01–08 `SearchChunk`; DAT-032 index generation/alias; derivative processing evidence. |
| Outputs | Committed searchable derivatives and `SearchIndexCommitted`, with index generation/document revision context. |
| Successful completion | Accepted index writes correspond to authoritative immutable source versions and required row context. Exact per-version completeness and `READY` linkage are unresolved. |

1. Validate and deduplicate the normalization event.
2. Resolve the authorized immutable version and source fingerprint.
3. Obtain its normalized chunks and relevant language, classification, and scope metadata.
4. Generate embeddings and normalized keyword-search representation.
5. Write through the applicable versioned index alias/generation.
6. Record the committed derivative outcome and `SearchIndexCommitted`.
7. Trigger query-cache invalidation through BAT-006.

A failed index write does **not** roll back accepted source metadata; BAT-009 reconciles fingerprints and retries.

**Source:** S, p. 19, §4.2.1; p. 34, §§9.1.1–9.1.2; p. 49, §13.2.2; p. 87, C.1.  
**Needs confirmation — BAT-OQ-009:** Search/embedding provider, index row key, vector precision, embedding batch bounds, alias/write schema, partial-row handling, completeness criteria, and document-readiness transition. Retrieval settings `80` candidates and `10` selected chunks are not embedding batch-size limits.

### BAT-005 — Parallel Index Rebuild

| Aspect | Contract |
|---|---|
| Arguments and input | Authorized rebuild scope, authoritative source inventory, intended parallel generation, applicable versions/configuration. Exact argument names and input-consistency strategy are unresolved. |
| Selection | Source records and immutable derivatives required for the rebuild scope; current deletion/access restrictions remain enforced. |
| Update targets | DAT-031 searchable derivatives; DAT-032 parallel generation and read alias. Authoritative source rows are not replaced by the index. |
| Outputs | Validated parallel index, atomic read-alias switch, correlated generation evidence. |
| Successful completion | Read alias switches only after completeness and recall checks pass. Failed validation does not justify switching to the unvalidated generation. |

1. Validate the rebuild scope and authority.
2. Create a parallel index generation.
3. Populate it using authoritative source/version/chunk data and BAT-004 representation rules.
4. Evaluate completeness and recall.
5. Atomically switch the read alias only after required checks succeed.
6. Apply applicable index-commit/cache invalidation effects.

**Source:** S, p. 34, §9.1.2; p. 87, C.1.  
**Needs confirmation — BAT-OQ-009**, **BAT-OQ-010:** Launch contract, completeness/recall thresholds, incremental changes during rebuild, deletion/ACL races, overlap between rebuilds, switch guard, failed-generation cleanup, old-generation retention, and rollback eligibility. No snapshot or change-capture mechanism is selected.

### BAT-006 — Cache Invalidation

| Aspect | Contract |
|---|---|
| Arguments/input | Changed authoritative ACL revision or committed index generation/document revision. `SearchIndexCommitted` is a confirmed trigger; no ACL-event name is supplied. |
| Selection | Cache entries affected by tenant, user-scope digest, source ACL revision, query hash, and index generation dependencies. |
| Update targets | DAT-034-F01–06 affected cached results; applicable current permission context in DAT-022. |
| Outputs | Invalidated affected entries; no new result served using revoked access. |
| Successful completion | Revoked source access is effective before the next retrieval. Authorization invalidation must not wait for normal TTL expiration. |

1. Validate scope and event/change identity.
2. Resolve the current authoritative ACL or committed generation.
3. Identify affected access-scoped cache entries.
4. Purge affected entries before new retrieval results are served under changed authorization.
5. Continue to apply current document ACL checks before text release.
6. Treat stale visibility as a security incident.

**Source:** S, p. 28, §7.2.2; p. 53, §14.3.2; p. 87, C.1; p. 89, `TST-004`.  
**Needs confirmation — BAT-OQ-010:** Change propagation/barrier mechanism, invalidation dependency mapping, concurrent cache fills, delayed old events, and recovery when cache services fail. Eventual queue delivery alone is insufficient if it permits forbidden evidence on the next query.

### BAT-007 — Source-Deletion Index Removal

| Aspect | Contract |
|---|---|
| Arguments/input | Detected source deletion, durable tombstone, affected document/version/index references. |
| Selection | Derivatives affected by the authorized source deletion. Exact version scope is unresolved. |
| Update targets | Source tombstone and affected DAT-031/DAT-032 search entries. |
| Outputs | Scheduled removal outcome and correlated deletion evidence. |
| Successful completion | A soft-deleted entity is not retrievable; affected index-removal outcomes are durable. Physical source/blob purge and retained cited history require separate retention decisions. |

1. Preserve the detected source deletion and create its tombstone.
2. Prevent retrieval of soft-deleted entities through authoritative guards.
3. Schedule removal of affected index entries.
4. Execute replay-safe removal and retain outcome evidence.
5. Keep final storage purge subject to retention and legal-hold controls.

**Source:** S, p. 28, §7.2.2; p. 51, §14.1.2.  
**Needs confirmation — BAT-OQ-010**, **BAT-OQ-014:** Removal schedule, retry/result schema, old cited-version handling, shared derivatives, and races with indexing/rebuilds. Source deletion must not silently rewrite an approved answer or its historical citation identity.

### BAT-008 — Outbox Delivery and Stage Resumption

| Aspect | Contract |
|---|---|
| Input selection | Applicable committed outbox records or delivered workflow events. The source does not name a pending/sent column or polling predicate. |
| Arguments | Required source envelope; operation key and consumer scope for deduplication; applicable durable checkpoint. |
| Update targets | DAT-014 outbox evidence, DAT-045 duplicate/consumer outcomes, DAT-046 checkpoints, DAT-048 queue context. Exact delivery-state fields are unresolved. |
| Outputs | At-least-once delivery and dispatch/resumption of applicable consumers. |
| Successful completion | One accepted business effect despite duplicate/delayed delivery; duplicate outcomes recorded without reapplication. Dispatch never substitutes for the required preceding durable commit. |

1. Obtain only durable committed event/workflow work.
2. Preserve the original event envelope and immutable signed tenant context.
3. Dispatch the applicable consumer.
4. At the consumer, check event ID, operation key, and aggregate revision.
5. Record a duplicate outcome and return without reapplying mutation when duplicate.
6. Validate stale-revision and current resource/domain conditions.
7. Resume the applicable persisted checkpoint or perform its idempotent effect.
8. Record the durable outcome and applicable next event/checkpoint before downstream dispatch.

`AgentPlanApproved` dispatches plan steps; `WorkflowStageAdvanced` resumes consumers. Case mutations, approval decisions, and applicable outbox insertion retain the confirmed ACID boundary.

**Source:** S, p. 17, §3.3.2; pp. 48–50, §§13.1–13.3; p. 52, §14.2.1; p. 87, C.1.  
**Needs confirmation — BAT-OQ-011:** Delivery selection, acknowledgment, consumer-ledger transaction boundaries, operation-key namespace, canonical bytes/signature verification, stale/future revision treatment, delivery-state schema, and expired-dedup behavior.

### BAT-009 — Reconciliation

| Aspect | Contract |
|---|---|
| Inputs | Authoritative source fingerprints, indexed versions, failed derivative outcomes, broken message links, outbox ledger. |
| Selection | Fingerprint mismatches/missing index effects and broken links identified within authorized scope. Scan cadence and precise predicates are unresolved. |
| Update targets | Search derivatives and message-link repair outcomes; applicable DAT-014/DAT-045–047 evidence. Accepted source metadata remains unchanged by index failure compensation. |
| Outputs | Retried derivative writes and repaired message links. |
| Successful completion | Reconciled derivative effects match authoritative source fingerprints and repaired links retain original lineage. |

1. Identify the affected authorized source/index or message scope.
2. Compare source fingerprints with indexed versions.
3. Retry missing/failed derivative effects through idempotent processing.
4. Repair broken message links from the outbox ledger.
5. Verify repaired versions and outcomes.
6. For incident recovery, apply the bounded replay and denied-access verification procedure under BAT-022.

**Source:** S, p. 49, §13.2.2; p. 90, F.1.  
**Needs confirmation — BAT-OQ-009**, **BAT-OQ-011:** Comparison inventory, scan bounds/cadence, mismatch taxonomy, retry exhaustion, orphan handling, and completion receipts. Reconciliation does not authorize restoring tombstoned or forbidden evidence.

### BAT-010 — Bounded Grounded-Answer Workflow

| Aspect | Contract |
|---|---|
| Arguments/input | Accepted authorized run request, saved case, user input, workspace policy, approved tools/deployments, evidence, runtime/token budgets, plan and rule versions. Public request schema remains unresolved. |
| Selection | Permitted, resolvable, quality-appropriate evidence; current ACL filtering precedes text release. |
| Aggregation/transformation | Hybrid retrieval and diversity; scoped prompt construction; structured model validation; candidate assembly; normalized deterministic policy evaluation. Apply BAT-CLS-001. |
| Update targets | DAT-008 run/plan/budget; DAT-009 steps; DAT-010 evidence; DAT-016 usage; DAT-017 policy; DAT-038–040 attempts/artifact/plan; DAT-046 checkpoints; applicable review tasks. |
| Outputs | Persisted progress, candidate/policy/review context, exact failed checkpoint when stopped, and source-named workflow/model events. |
| Completion | Publication only through satisfied BAT-011 gate. Failure/timeout must never appear as an approved answer. Review waiting and terminal-stop semantics require confirmation. |

1. Validate the request, `Analyst` authorization, and idempotency before allocation.
2. Admit a new run only when workspace tokens, queue age, and provider capacity satisfy configured thresholds.
3. Create the run immediately and persist its plan revision before side effects.
4. Validate an acyclic plan with explicit dependencies, maximum depth `8`, and maximum `16` tool invocations.
5. Persist each applicable stage checkpoint before downstream dispatch.
6. Retrieve ACL-filtered lexical/vector candidates, merge with reciprocal rank fusion, deterministically rerank, apply evidence diversity, and enforce the model-context token budget.
7. Return `NO_SUPPORTED_EVIDENCE` for insufficient evidence/confidence/quality; clarification or human routing follows only the defined policy.
8. Select an approved specific model deployment using maximum included-material classification. Fallback requires approved equal-or-stronger handling and approved region/deployment.
9. Reserve input/output token budget and record attributed provider usage under workspace quota.
10. Construct the prompt from fixed system rules, signed workflow instruction, validated user input, and separately delimited untrusted evidence.
11. Strip evidence tool-call directives, record injection indicators, and redact nonessential personal data where policy permits.
12. Validate the provider’s versioned structured output with bounded retries; unknown fields, invalid citations, or control-character injection cause `MODEL_OUTPUT_INVALID`.
13. Assemble the exact candidate separately from retrieval, policy, and review records.
14. Normalize and store the six policy input concepts with rule-set version: case sensitivity, requested action, evidence quality, model class, financial-impact category, and confidence bands.
15. Apply `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, or `DENY`; model text cannot override policy.
16. Route required review to eligible pools/roles with separation of duties. Do not autonomously approve high-risk recommendations.
17. Permit publication only after BAT-011 succeeds.

The source run progression is `REQUESTED → RETRIEVING → GENERATING → POLICY_CHECK → AWAITING_REVIEW → PUBLISHED` or failure. The source also describes missing-approval termination and a recoverable timeout, requiring reconciliation rather than a new state invention.

**Reference configuration:** `workflow.run_timeout_seconds: 180`; `retrieval.max_candidate_chunks: 80`; `retrieval.max_selected_chunks: 10`; `retrieval.hybrid_rrf_k: 60`. MCP `knowledge.search@v1` remains read-only with `read:permitted_documents` and `max_items: int<=10`.

**Source:** S, pp. 34–42, Chapters 9–11; pp. 44 and 49, §§12.1 and 13.2.1; p. 62, §17.2; p. 69, §19.2.1; pp. 87 and 90.  
**Needs confirmation — BAT-OQ-012**, **BAT-OQ-024:** Run-route relationship, budget counting under retries/replay, review-wait exclusion/inclusion, timeout representation, case revision binding, structured schemas, provider deadlines, admission thresholds, and classification provenance/mappings.

### BAT-011 — Publication Validation

| Aspect | Contract |
|---|---|
| Trigger/input | `ApprovalDecisionRecorded` carries task/actor/content-hash concepts. A recorded rejection is not permission to publish. Exact candidate, evidence, policy, and approval records are required. |
| Selection | Applicable exact-artifact publication candidate satisfying current access, evidence, policy, and required approval conditions. |
| Update targets | DAT-043 satisfied gate and DAT-003-F15 final approved-result pointer in the same transaction; applicable outbox/audit evidence. |
| Outputs | Exact published artifact or safe gate rejection. No independently callable public endpoint is confirmed. |
| Successful completion | Supported exact content is published only after all gates pass; wrong-artifact replay cannot use an old approval. |

1. Validate/deduplicate the event and resolve the exact candidate/hash.
2. Recompute current tenant/workspace/source authorization.
3. Verify required evidence, immutable cited versions, and resolvable source anchors.
4. Verify the applicable deterministic policy and BAT-CLS-001 controls.
5. Verify required decisions bind the exact artifact and satisfy role, routing, and separation-of-duties constraints.
6. Reject stale content, revoked evidence, insufficient support, unsatisfied approvals, and old-approval replay for another artifact.
7. Atomically record the satisfied gate and update the final response pointer.
8. Expose `PUBLISHED` only after successful commit.

**Source:** S, pp. 12 and 44–46, §§2.2.2 and 12.1–12.5; p. 62, §17.2.1; p. 87, C.1.  
**Earlier mappings:** API-020-P01; API-TXN-002; DAT-TXN-002; `SCR-002-A09`.  
**Needs confirmation — BAT-OQ-013:** Gate payload/lookup/hash definition, policy-version activation, transaction/revalidation mechanics, decision/expiry races, non-review invocation, and failure codes. Do not create a Publish API or assume approval acceptance automatically resolves the case.

### BAT-012 — Review Expiry and Routing

| Aspect | Contract |
|---|---|
| Arguments/input | Task context, configured SLA/deadline, current review state, pool/minimum-role/separation policy. |
| Selection | Tasks whose applicable configured SLA has expired. Physical deadline field, timer/scanning mechanism, and eligible-state predicate are unresolved. |
| Update targets | DAT-011 expiry/routing state and retained escalation/reassignment evidence. Immutable DAT-012 decisions cannot be rewritten. |
| Outputs | Reassignment or escalation; no implicit approval. |
| Successful completion | Applicable expiry/escalation is durably recorded and no expired task silently grants publication. |

1. Determine expiry using the applicable configured SLA.
2. Validate current task state, scope, and routing policy.
3. Apply policy-selected reassignment or escalation.
4. Preserve exact candidate/hash linkage and prior immutable decisions.
5. Record expiry/routing evidence without creating an approval.
6. Continue publication blocking until required approval policy is satisfied.

**Source:** S, p. 45, §12.2.1; p. 82, A.1; p. 89, `TST-010`.  
**Needs confirmation — BAT-OQ-013:** SLA value/unit/timezone, expiration boundary, eligible-state matrix, race with submitted decisions, reassignment history, escalation targets, and notification channel. A separate periodic expiry scanner is not yet selected.

### BAT-013 — Closed-Case Retention and Tombstone Purge

| Aspect | Contract |
|---|---|
| Arguments/input | Authorized retention/purge scope, applicable policy/cutoff, closed-case state and lineage, tombstone inventory, legal holds, object/version references. |
| Selection | **Routine case retention:** only eligible `CLOSED` cases. **Final tombstone purge:** independently eligible tombstoned entities. Source-deletion and decommission inventory must not be treated as automatically subject to the same case selector. |
| Update targets | Eligible lifecycle data/objects and DAT-018 receipts; protected DAT-026 closure lineage and DAT-053 hold exceptions. |
| Outputs | Purge outcomes/receipts and applicable `DataRetentionPurgeCommitted` evidence. |
| Successful completion | Only authorized eligible data is purged; held/protected data remains retained and receipted; soft-deleted entities are not retrievable. |

1. Resolve the authorized retention policy and inventory.
2. For routine case retention, select only eligible closed cases.
3. Preserve the approved-answer, cited-version, and reviewer-decision lineage required by closure policy.
4. Apply maximum included-material retention control where run material is involved.
5. Evaluate legal-hold exceptions before eligible removal.
6. Use the scheduled tombstone pipeline for final purge.
7. Record completed outcomes and protected exceptions with tenant/actor/time/correlation context.
8. Emit applicable purge-commit evidence only for its accepted durable outcome.

**Source:** S, p. 26, §6.3.2; pp. 51–53, §§14.1–14.3; p. 62, §17.2.1; p. 66, §18.3.2.  
**Related API/data:** API-036 `POST /internal/storage/purge`; DAT-RET-001/004/007; DAT-018-F01–05.  
**Needs confirmation — BAT-OQ-014:** Retention periods/cutoffs, scope of related objects and versions, final-purge schedule, sharing/deduplication, hold race handling, backups, physical deletion actions, receipts, and partial completion. The two-independent-check decommission requirements remain BAT-021; sharing an implementation does not collapse the authorization rules.

### BAT-014 — Diagnostic and Security-Audit Retention Purge

| Aspect | Contract |
|---|---|
| Inputs | Diagnostic logs, security-audit inventory, retention policies, hold exceptions, purge receipts. |
| Selection | Diagnostics use default TTL `30` days; security audit uses a distinct fictional `7`-year policy. Exact TTL start and calendar boundaries are unresolved. |
| Update targets | Eligible diagnostic/audit retention data and purge receipt/exception evidence. |
| Outputs | Completion receipts and legal-hold exceptions. |
| Successful completion | Distinct policies remain enforced; protected evidence is not removed under a generic diagnostic TTL. |

1. Identify the data category and applicable retention policy.
2. Evaluate its eligibility and legal holds.
3. Purge only eligible data using the defined retention mechanism.
4. Retain completion receipts and hold exceptions.
5. Preserve required audit evidence independently of diagnostic sampling.

**Source:** S, p. 66, §18.3.2; p. 90, Appendix F.  
**Needs confirmation — BAT-OQ-015:** Corporate policy, TTL/year calculation, archive-versus-active audit inventory, purge cadence, hold precedence, receipt retention, and rerun/completion schema. No `RESTRICTED`-specific duration is supplied.

### BAT-015 — Audit Batch Hashing and Archive Export

| Aspect | Contract |
|---|---|
| Inputs/selection | Authorized append-only audit entries to be included in an archive batch; batch boundaries and archive continuation contract unresolved. |
| Transformation | Chain entries with batch hashes and export to independently controlled retention storage. |
| Update targets | DAT-013 audit-chain/archive evidence and DAT-STO-007 retention objects; no historical review/audit mutation. |
| Outputs | Verifiable immutable audit archive and chain provenance. |
| Successful completion | Archived entries preserve audit lineage and batch-chain integrity; operators cannot edit historical review decisions. |

1. Resolve the authorized append-only ledger input and batch scope.
2. Apply the defined batch-hash chaining format.
3. Preserve event, tenant, actor, and correlation lineage.
4. Export the batch to independently controlled retention storage.
5. Retain the evidence needed to verify chain/export integrity.
6. Prohibit historical edits.

**Source:** S, p. 62, §17.3.1; p. 88, `T-09`.  
**Needs confirmation — BAT-OQ-015:** Batch boundaries, hash algorithm/canonical bytes, chain fields, archive names/formats, export acknowledgment, checkpoint, retention, and overlapping-batch behavior. Generic register SHA-256 provenance does not establish every audit-chain serialization or digest field.

### BAT-016 — Daily Usage and Cost Rollups

| Aspect | Contract |
|---|---|
| Arguments/input | Daily reporting scope/window; model invocation, embedding, storage, indexing, token ledger, workspace cost center, deployment version, budget/quota/rejected-request data. |
| Selection | Usage attributable to the applicable reporting day and tenant/workspace scope. Day definition and late-arrival rules are unresolved. |
| Aggregation | Daily summaries show budget, forecast, and rejected excess requests while preserving cost-center/deployment attribution. Formulas, currency, and precision are not supplied. |
| Update targets | DAT-054-F04 CostLedger/rollup concepts; exact physical aggregate schema unresolved. Raw DAT-016 usage remains separately attributable. |
| Outputs | Daily rollup information supporting API-012 `GET /v1/usage`. |
| Successful completion | Reporting preserves supported usage categories and attribution without duplicate replay accounting. Exact report completeness/finalization rules are unresolved. |

1. Resolve the authorized reporting scope and defined daily window.
2. Read attributed usage for model invocations, embeddings, storage, and indexing.
3. Preserve workspace cost-center and model-deployment-version linkage.
4. Produce the defined budget, forecast, and rejected-excess-request aggregates.
5. Persist replay-safe aggregate outcomes using the approved rollup contract.
6. Make applicable cost/quota/trend information available through authorized usage inquiry.

**Source:** S, p. 38, §10.3.1; p. 65, §18.3.1; p. 83, A.2.  
**Needs confirmation — BAT-OQ-016:** Daily timezone/time, accounting cutoffs, forecast formula, units/currency/rounding, late usage, provider adjustments, scope, duplicate ledger identity, rollup replacement/versioning, zero-usage rows, and backdated reruns. Daily rollups do not establish browser refresh cadence.

### BAT-017 — Frozen Benchmark Evaluation

| Aspect | Contract |
|---|---|
| Arguments/input | Accepted API-013 request and idempotency key; frozen versioned dataset, expected citation sets/decisions, evaluated prompt/model/policy context. Exact setup schema unresolved. |
| Selection | Reference corpus of `1,200` synthetic permission-controlled cases spanning retrieval, refusal, ambiguity, and adversarial evidence. |
| Transformation | Execute applicable deterministic/integration/AI cases; compare actual outputs to frozen expectations; calculate quality and domain confidence/shift reporting. |
| Update targets | DAT-057 TestCase/EvalDataset/Scorecard/ReleaseGateResult and correlated evaluation records. |
| Outputs | Actual scorecard, `EvaluationCompleted`, and applicable signed release-test evidence. |
| Completion | Evaluation outcome is reproducible and actual. Job execution success is not quality-gate success or release promotion. |

1. Validate authorized `Admin` request and job idempotency before allocation.
2. Resolve frozen, versioned, independently reviewed fixtures and their signed-manifest integrity control.
3. Preserve expected citation sets and decision outcomes; do not replace them to fit actual output.
4. Record the evaluated prompt/model and relevant configuration versions.
5. Execute deterministic software contracts without live model calls where required.
6. Execute integration/failure-injection and applicable AI evaluation cases under controlled synthetic identities and permissions.
7. Record seeds for randomized cases.
8. Produce actual grounded citation precision, unsupported-claim rate, and high-risk policy recall.
9. Report confidence intervals and distribution shift by domain.
10. Record `EvaluationCompleted` and applicable release-gate evidence.

**Reference targets:** grounded citation precision `>=0.97`; unsupported-claim rate `<=0.02`; high-risk policy recall `1.00` on the frozen safety suite. Critical isolation and approval tests pass with zero exceptions. Low statistical confidence blocks release. Prompt/model changes require re-evaluation.

**Source:** S, pp. 74–76, §§21.1–21.3; pp. 88–89, `T-12`, D.1, E.1–E.2; p. 83, A.2.  
**Needs confirmation — BAT-OQ-017:** Job/state/result schemas, statistical formulas/confidence threshold, missing/failed-case handling, resume versus new evaluation, provider budgets, frozen-manifest verification format, and empty-corpus outcome. No partial or empty dataset may be silently treated as equivalent evidence of an acceptable release.

### BAT-018 — Tenant/Workspace Provisioning

| Aspect | Contract |
|---|---|
| Arguments/input | Authorized provisioning intent and tenant/workspace policy, encryption references, role bindings, quotas, and connector-stub configuration. API-056 has no confirmed method/path. |
| Selection | Validated provisioning scope with no implicit tenant or unrestricted role binding. |
| Update targets | DAT-001–002, DAT-020, DAT-027, DAT-052, DAT-058-F01. |
| Outputs | One idempotent provisioning workflow outcome; visible incomplete state; sync blocked while incomplete. |
| Successful completion | Required policy, encryption references, roles, quotas, and connector stubs are established. Exact completion state is unresolved. |

1. Validate provisioning input and administrative/service authority.
2. Establish the idempotent workflow scope and trusted context.
3. Create the required policy, encryption-reference, role-binding, quota, and connector-stub results.
4. Keep incomplete provisioning visible and block connector sync.
5. Record durable workflow outcomes and verify the required set before completion.

The source confirms **one idempotent workflow**, not one cross-store ACID transaction or a fixed resource-creation order.

**Source:** S, p. 78, §22.1.1.  
**Needs confirmation — BAT-OQ-018:** Initiation API/role, configuration requiredness/defaults, step ordering, encryption reference provisioning, partial-resource handling, concurrency, completion verification, rollback/compensation, and safe resume.

### BAT-019 — Historic Document Backfill

| Aspect | Contract |
|---|---|
| Arguments/input | Authorized historic source inventory, bounded windows, stable source IDs, source permissions, processing versions, and batch reconciliation context. |
| Selection | Historic documents within the defined window. Exact window fields, ordering, and bounds are unresolved. |
| Transformation | Ingest through source/extraction/index controls; reconcile each batch against its selected inventory. |
| Update targets | DAT-005–007, DAT-028–032, DAT-058-F02; reconciliation receipt representation unresolved. |
| Outputs | Stable source identity, per-batch reconciliation receipts, index-coverage readiness evidence. |
| Successful completion | Selected batches have durable reconciled outcomes; search readiness is based on coverage, not merely queue emptiness. |

1. Validate source access and bounded backfill scope.
2. Select historic documents in the defined bounded window.
3. Preserve stable source IDs through ingestion.
4. Execute applicable BAT-002/BAT-003/BAT-004 controls.
5. Produce per-batch reconciliation receipts.
6. Determine search readiness using index coverage.

**Source:** S, p. 78, §22.1.2.  
**Needs confirmation — BAT-OQ-018:** Launch contract, window bounds/timezone, stable-ID uniqueness, batch receipts, poison-record coverage treatment, late source changes, restart checkpoint, and coverage formula/threshold. Backfill does not establish a `full_sync` request flag.

### BAT-020 — Controlled Export

| Aspect | Contract |
|---|---|
| Arguments/input | `workspaceId`, accepted API-014 request, idempotency key, authorized lifecycle inventory, two independent approval checks. Chapter terminology describes tenant export; extent remains unresolved. |
| Selection | Authorized case metadata, approved artifacts, source references, and audit manifests. |
| Transformation | Package selected inventory and checksums; exclude secrets and internal model prompts. |
| Update targets | DAT-059 ExportManifest and package/provenance records; source business data remains authoritative. |
| Outputs | Controlled export package/manifest with checksums. |
| Completion | Required authorized inventory is packaged with integrity evidence. HTTP `202` is acceptance, not package completion or download availability. |

1. Validate request, resource scope, `Admin + approver`, and both independent approval checks before accepting work.
2. Resolve the authorized export inventory and applicable access/redaction controls.
3. Collect case metadata, approved artifacts, source references, and audit manifests.
4. Exclude secrets and internal model prompts.
5. Generate the package and checksum evidence.
6. Record the export manifest and actual completion outcome.

**Source:** S, pp. 78–79, Chapter 22; p. 83, A.2; p. 88, `T-11`.  
**Needs confirmation — BAT-OQ-019:** Tenant/workspace extent, independent actors/proof, concurrent mutation/deletion handling, package format/names/checksum algorithm, download/status API, expiry, partial-file recovery, and completion notification. `TenantDeletionVerified` is not an export-specific completion event.

### BAT-021 — Verified Deletion

| Aspect | Contract |
|---|---|
| Arguments/input | `workspaceId`, accepted API-015 request, idempotency key, lifecycle inventory, two independent checks, current legal holds/retention protections. |
| Selection | Eligible authorized deletion targets; protected held records remain retained. Exact tenant/workspace and related-object extent unresolved. |
| Update targets | Tombstones, eligible DAT-035 blob objects, DAT-031 search entries, DAT-018 receipts, DAT-053 protected exceptions; relational extent unresolved. |
| Outputs | Completion receipts and retained exceptions; Retention Worker `TenantDeletionVerified` with manifest ID/receipt hash concepts; consumer closes purge record. |
| Completion | Actual verified inventory outcome, including held-data receipts. Partial removal must not be represented as verified complete deletion. |

1. Validate scope and both independent approval checks.
2. Resolve the lifecycle inventory.
3. Enforce applicable legal holds.
4. Write durable tombstones for eligible targets.
5. Remove eligible blobs and index entries using retry-safe effects.
6. Record completed removals and protected-record exceptions.
7. Verify inventory outcomes and retain manifest/receipt evidence.
8. Produce `TenantDeletionVerified` only for the verified outcome; close the purge record through its consumer.
9. Use the same inventory for data-subject access handling.

**Source:** S, pp. 78–80, §§22.1–22.3; p. 87, C.1; p. 89, `TST-013`.  
**Needs confirmation — BAT-OQ-019**, **BAT-OQ-014:** Scope, approval proof, hold races, shared versions, active-case decommission versus routine closed-case retention, backups, relational deletion, partially retained final state, retry/receipt verification, and completion transport. No force-delete option is authorized.

### BAT-022 — Operator Replay

| Aspect | Contract |
|---|---|
| Arguments/input | Original dead-letter/event/outbox record, operator reason, dry-run validation, bounded scope, optional explicit schema-migration provenance. |
| Selection | Authorized affected records within operator-controlled scope. Numeric limit/window and selection schema unresolved. |
| Update targets | DAT-047 replay/provenance evidence and applicable resumed DAT-045/DAT-046 consumer outcomes; business changes only through original guarded boundaries. |
| Outputs | Validated bounded replay and resumed outcomes preserving original lineage. |
| Successful completion | No reapplication of accepted business effects; original event identity retained unless an explicit provenance-linked migration transforms schema. |

1. Authenticate the operator and validate authorized replay scope.
2. Require an audited operator reason.
3. Perform dry-run validation before execution.
4. Apply the configured scope limit.
5. Preserve original event identity and envelope unless explicit migration requires provenance-linked transformation.
6. Dispatch through existing deduplication, revision, resource, and domain guards.
7. Verify repaired outcomes; record replay evidence.
8. For delayed-indexing recovery, compare source fingerprints/indexed versions and run denied-access probes.

**Related API:** API-034 `POST /internal/deadletters/{id}/replay`; API-033 `GET /internal/workflows/{runId}` is inquiry.  
**Source:** S, p. 50, §13.3.2; p. 90, F.1.  
**Needs confirmation — BAT-OQ-020:** Operator permissions, dry-run request/result, numeric/time scope, migration format, replay key retention, partially completed replay, and whether bounded outbox recovery uses API-034 or another controlled interface. Replay cannot bypass a still-invalid permission or validation condition.

### BAT-023 — Schema Backfill and Constraint Enforcement

| Aspect | Contract |
|---|---|
| Arguments/input | Approved migration plan, schema/configuration version, target data scope, bounded batches, active-reader/replica compatibility evidence. |
| Selection | Rows requiring the defined backfill; exact selector and batch size are migration-specific and unresolved. |
| Transformation | Add nullable fields first, backfill in bounded batches, then enforce constraints under compatible rollout conditions. |
| Update targets | Approved target fields/constraints and DAT-056-F03 migration evidence. No new production DDL is invented. |
| Completion | Backfill and constraint enforcement satisfy compatibility; active readers do not lose required fields. |

1. Validate the approved migration and rollback-readability plan.
2. Apply backward-compatible nullable additions.
3. Backfill the defined data in bounded batches.
4. Verify applicable backfill/compatibility conditions.
5. Enforce postdeploy constraints only after old replicas drain.
6. Preserve required fields while active readers depend on them.
7. Record migration/configuration lineage.

**Source:** S, p. 52, §14.2.2; p. 55, §15.3.1; p. 72, §20.2.2.  
**Needs confirmation — BAT-OQ-021:** Migration-specific schema, selector/bounds, parallelism, checkpoints, validation, maintenance window, and supported compensation. Canary regression rolls back traffic, not an automatic database down-migration.

### BAT-024 — Optional Webhook Delivery

| Aspect | Contract |
|---|---|
| Arguments/input | Optional authorized subscription/recipient context and a committed internal transition/event. No HTTP method, recipient registration endpoint, or signature header is supplied. |
| Selection | Applicable committed subscribed notifications; exact event catalog and payload projection unresolved. |
| Transformation | Sign outbound delivery; preserve event-age evidence; retry with exponential backoff. |
| Update targets | DAT-050 delivery/subscription context; exact retry ledger/schema unresolved. |
| Completion | Actual delivery outcome under the approved acknowledgment contract. Internal business commit remains independent of delivery failure. |

1. Resolve authorized optional delivery configuration for a committed change.
2. Produce a scoped safe payload using the defined contract.
3. Sign the delivery and include defined event-age information.
4. Send through the declared outbound boundary.
5. Apply exponential-backoff retries where permitted.
6. Retain delivery outcome; do not roll back the internal case transition.
7. Require recipients to verify signature and event age.

**Source:** S, p. 55, §15.2.2.  
**Needs confirmation — BAT-OQ-022:** Method/URL management, subscribed events, signature/canonical bytes/key rotation, maximum age, retryable acknowledgments, count/deadline, delivery ordering, dead letters, and manual replay.

### BAT-025 — Backup and Recovery Verification

| Aspect | Contract |
|---|---|
| Inputs | PostgreSQL continuous backup evidence, object versions, index rebuild recipes, recovery profile, authorized incident/exercise context. |
| Execution profile | R1 uses primary-region writes and one warm recovery region. Secondary snapshots are restored only under incident command. |
| Update targets | RecoveryCheckpoint/LoadProfile concepts in DAT-055 and controlled restored resources. Exact platform implementation unresolved. |
| Outputs | Consistent relational/object recovery, index rebuild verification, measured safety/RPO/RTO evidence. |
| Completion | Reference RPO `<=15 minutes` and RTO `<=4 hours`, with tested object/relational consistency. |

1. Maintain the source-described continuous PostgreSQL backup capability.
2. Resolve the authorized recovery point and relational/object inventory.
3. Restore secondary snapshots only under incident command.
4. Execute the defined object-version and index-rebuild recovery procedure.
5. Verify relational/object consistency and access safety.
6. Measure recovery time and data-loss exposure against the reference RPO/RTO.
7. Retain exercise/incident evidence.

**Source:** S, p. 19, §4.2.2; pp. 69–70, §19.3; p. 89, `TST-012`, E.2.  
**Needs confirmation — BAT-OQ-023:** Provider, retention, consistent recovery-point selection, restore order, scope/roles, exercise frequency, commands, heartbeat/failover thresholds, and recovery receipts. RPO `15 minutes` is not a confirmed fifteen-minute backup schedule.

### BAT-026 — Verification and Release Automation

| Aspect | Contract |
|---|---|
| Inputs | Source-controlled contracts/defaults, signed deployment configuration, build identity, image digest, schemas/prompts/model-routing policy, migration plan, baseline/canary metrics, sign-off evidence. |
| Selection | Authorized release/build artifacts and applicable minimum test pack. Exact pipeline triggers and stage graph unresolved. |
| Transformation | Static/dependency analysis, unit/contract and release verification, SBOM generation, image signing, canary comparison, controlled promotion/rollback. |
| Update targets | DAT-056 release/configuration/migration/rollout evidence; DAT-057 test outputs; relevant compatibility evidence. |
| Outputs | Signed test outputs referenced by release digest; verified release record and applicable `ReleasePromoted`/`DeploymentPromoted` evidence. |
| Completion | Production deploys only verified allowed-build digests; required gates/sign-off pass; binary, prompt, and policy versions are reconstructible. |

1. Execute static analysis, dependency scanning, unit/contract verification, SBOM generation, and image signing.
2. Run the minimum release test pack: unit, schema evolution, negative authorization, workflow replay, staging connector sync, visual accessibility, search recall, grounding, policy recall, load, and disaster-recovery verification.
3. Sign test outputs and reference them by release digest.
4. Independently reproduce critical negative security cases and retain security-control review/signature evidence.
5. Verify production image digest against an allowed build identity.
6. Apply backward-compatible migration/backfill rules through BAT-023.
7. Assess state-machine/schema compatibility before traffic movement.
8. Canary latency, errors, authorization denials, and AI-quality regression against baseline.
9. On regression, roll back traffic; reverse binary routing first and use compensating data operations only if explicitly supported.
10. Before promotion, obtain source-required Security/SRE validation of external egress, secret handling, backup status, and alert routing.
11. Record image digest, schemas, prompts, and model-routing policy in the release lineage.

The source does not prescribe one serial ordering for every independent test in the minimum pack. Exact pipeline dependencies must be confirmed rather than inferred from this numbered description.

**Source:** S, p. 20, §4.3.2; pp. 71–73, §§20.1–20.3; pp. 74–76, Chapter 21; pp. 88–89, D.1 and E.2.  
**Needs confirmation — BAT-OQ-021:** Pipeline platform/trigger, build/signature formats, stage graph, canary duration/thresholds, gate-result schema, release-role proof, supported compensation, and rerun/promotion idempotency.

### Capability Without a Confirmed Standalone Job — Key and Secret Rotation

| Aspect | Confirmed requirement | Needs confirmation |
|---|---|---|
| Inputs | Vault-backed application secrets/encryption references; managed-identity access | Rotation API/arguments, provider responsibility, eligible keys, policy schema |
| Processing | Service credentials rotate automatically; encryption keys rotate on defined policy | Whether any application job is required; policy cadence; concurrency; rewrap/re-encryption approach |
| Update targets | Relevant secret/key references and protected encryption context | Exact reference/version/history schema and storage coordination |
| Boundaries | Secrets do not appear in traces/model prompts; bulk re-encryption is not required in request processing | Background re-encryption necessity, throughput, recovery/rollback, destruction evidence |
| Completion | Rotated credentials/keys remain within declared access scope | Verification, failure state, resumption, and old-key retention |

**Source:** S, p. 21, §5.1.2; p. 63, §17.3.2; p. 10, §1.3.2.  
**Earlier mappings:** DAT-052; DAT-RET-011; API-OQ-021.  
**Open decision:** **BAT-OQ-023**. Do not invent a nightly rotation or bulk re-encryption job.

## Operations and Recovery

### Concurrent Launches and Mutual Exclusion

**BAT-CON-001 — Confirmed:** Concurrent/delayed delivery and retries must preserve one accepted business outcome. A job ID is not itself the operation’s deduplication key. Event identity, operation key, aggregate revision, source/version identity, and exact-artifact binding retain their applicable roles.  
**Source:** S, pp. 15, 17, 25, 45, 48–50; p. 85, B.1.

| Overlap | Required safety invariant | Mechanism Needs confirmation |
|---|---|---|
| Identical job-creating requests | Return original operation/outcome under applicable idempotency; no second accepted job effect | Concurrent key reservation, key namespace, lost-response recovery, error caching |
| Same connector sync/backfill | Cursor cannot skip preceding undurable outcomes; source IDs remain stable; exceptions retained | One-active-sync rule versus partitioned cursor concurrency, lock/lease scope, expiry |
| Classification and user correction/case edit | No stale or unauthorized overwrite; correction reason/provenance retained | Case revision pinning and correction precedence |
| Same document/pipeline normalization | Immutable derivatives and safe replay; changed pipeline supports side-by-side versions | Duplicate worker reservation, physical derivative identity, attempt/checkpoint granularity |
| Index build, rebuild, deletion, and ACL changes | No unvalidated alias switch or resurrection of soft-deleted/forbidden evidence | Generation fencing, delta capture, alias compare-and-switch, invalidation barrier |
| Publication and artifact/ACL/approval changes | Exact-artifact/current-permission gate; atomic gate/pointer; no old-hash publication | Transaction guards, lock/isolation, policy activation and revalidation |
| Review expiry and submitted decision | No implicit approval or invalid task decision | Eligible-state/expiry boundary and race winner |
| Retention/delete and legal hold/export/active work | Enforce holds, authorized scope, immutable lineage protections; no false verified completion | Lifecycle freeze, inventory snapshot, shared-object protection, hold race |
| Daily rollup rerun and late usage | Preserve attribution and replay-safe outcomes | Aggregate key/versioning, late-arrival policy, day finalization |
| Audit export and replay | Append-only chain/evidence; no historical edit | Batch boundary allocation, continuation checkpoint, duplicate archive handling |
| Migration and old/new replicas | Bounded backfill and compatible readers; enforcement after old replicas drain | Migration coordinator, partitioning, resume and verification controls |
| Lost worker heartbeat and replacement worker | Duplicate-safe effects and durable progress | Heartbeat cadence, lease/fencing, reassignment timing, cancellation authority |

**Sources:** S, pp. 25, 28, 31, 34, 45, 48–53, 65, 70, 72, 78–80.  
**Needs confirmation — BAT-OQ-004:** Mutual-exclusion granularity, locks/leases, fencing, partition strategy, maximum concurrent executions, heartbeat timeout, and graceful drain. No database lock type or one-job-per-tenant limit is selected.

### Processing Units and Commit Boundaries

| Job family | Source-supported processing/checkpoint unit | Confirmed commit behavior | Open operational detail |
|---|---|---|---|
| Case classification/mutations | Case/event/revision context | Case mutation and applicable history/outbox follow domain ACID controls; denied/stale mutation changes no business state | Classifier mutation interface and exact atomic history/audit placement |
| Connector sync/backfill | Source item outcomes and provider cursor; bounded historic batches | Cursor advances only after preceding durable ingestion outcomes; per-backfill-batch reconciliation receipts | Batch size, durable-outcome stage, per-item versus multi-item DB transaction |
| Extraction | Immutable source/pipeline derivatives and processing progress | Scan before parse; unsafe no index; durable immutable source/derivative relationships | Page/chunk/version checkpoint, object/relational crash reconciliation |
| Index build/rebuild | Version/chunk/generation; alias switch | Index is nonauthoritative; accepted source metadata survives failed index writes; rebuild read switch atomic after checks | Write batch atomicity, partially populated version/readiness, cleanup |
| Outbox/consumers | Original event/operation/aggregate revision | Applicable business mutation and outbox commit in one ACID transaction; consumer deduplication | Claim/ack/ledger commit boundaries and duplicate-delivery races |
| AI workflow | Plan revision before side effects; each stage checkpoint before dispatch | Durable progression reconstructed from server state | Step/attempt checkpoint schema and worker occupancy during review |
| Approval/publication | Immutable decision/exact hash; satisfied gate | Approval decision/outbox ACID; final response pointer and gate same transaction | Gate invocation and task/expiry races |
| Retention/deletion | Eligible inventory and tombstones/receipts | Replay-safe cross-store removal and verified receipts; holds preserved | Commit batch size, partial final state, backup/shared-object scope |
| Rollup/audit archive/evaluation | Daily scope, audit batch, frozen evaluation cases/results | Durable reproducible outcomes and required lineage | Aggregate/archive/result schema, checkpoint/finalization |
| Provisioning | One idempotent workflow | Incomplete remains visible and blocks sync | Cross-resource compensation and completion predicate |
| Migration | Bounded backfill batches | Expand → backfill → enforce; reader compatibility | Batch commit, resumption, constraints/checks |
| Webhook | Delivery associated with committed internal change | Delivery failure cannot reverse case commit | Retry ledger/acknowledgment |
| Backup/release | Recovery/release evidence | Primary-region write profile; verified signed release and gates | Platform-specific units and rollback mechanisms |

**Sources:** S, pp. 25, 28, 31, 34, 45, 49, 52, 55, 62, 65, 72, 78–80.  
**Earlier mappings:** API-TXN-001–003; DAT-TXN-001–004; DAT-CNC-005–006.

**BAT-TXN-001 — Needs confirmation:** Transaction isolation, row/object locking, worker reservation, consumer-ledger atomicity, and cross-store crash-recovery protocol. The confirmed logical units above do not select a distributed transaction or allow whole-job rollback of previously accepted source data.

### Idempotency, Reruns, and Resumption

| Requirement ID | Status | Requirement | Source |
|---|---|---|---|
| BAT-IDEM-001 | Confirmed | Every cross-service write is idempotent under retries. | S, p. 15, Chapter 3 invariant |
| BAT-IDEM-002 | Confirmed | Job-creating POSTs require `Idempotency-Key`; identical payload returns original operation; same key/different fingerprint yields `IDEMPOTENCY_CONFLICT`. | S, p. 54, §15.1.2 |
| BAT-IDEM-003 | Confirmed | Case idempotency binds actor/request fingerprint to one outcome for `24` hours. This is not a universal TTL for all jobs. | S, p. 25, §6.2.2 |
| BAT-IDEM-004 | Confirmed reference setting | `workflow.replay_dedup_hours: 24`. It does not establish SSE, archive, all HTTP key, or all outbox retention. | S, p. 90, Appendix F |
| BAT-IDEM-005 | Confirmed | Consumers deduplicate event ID and operation key; detect stale revision; record duplicate outcome without business mutation. No invariant relies on cross-partition ordering. | S, pp. 17 and 48, §§3.3.2 and 13.1.2 |
| BAT-RES-001 | Confirmed | Partial connector batches retry safely from durable cursor/outcomes; cursor does not skip undurable preceding items. | S, p. 28, §7.2.1 |
| BAT-RES-002 | Confirmed | Workflow checkpoints precede downstream dispatch; refresh/reconnect reads server state, not a new business execution. | S, p. 49, §13.2.1; p. 58, §16.2.1 |
| BAT-RES-003 | Confirmed | Changed normalization pipeline can be reprocessed side by side without overwriting immutable old derivatives. | S, p. 31, §8.2.2 |
| BAT-RES-004 | Confirmed | Denied recommendations are reworked as new run revisions, not retroactively approved historical records. | S, p. 46, §12.3.2 |
| BAT-RES-005 | Confirmed | Operator replay requires reason, dry-run validation, scope limit, and preserved original identity except explicit provenance-linked migration. | S, p. 50, §13.3.2 |
| BAT-RES-006 | Needs confirmation | Rerun identity versus resume identity, valid replay after dedup expiry, backdated rollups, repeated purge/export/evaluation completion, checkpoint retention, and invalidated-original-input recovery. | **BAT-OQ-003**, **BAT-OQ-011**, **BAT-OQ-016–020** |

No ordinary end-user Cancel, Pause, or Retry control is confirmed for AI runs. Controlled operator replay is not an Analyst capability.

### Retry, Timeout, and Backpressure Policy

| Failure or condition | Confirmed treatment | Numeric/contract gaps |
|---|---|---|
| Transient workflow dependency fault | Bounded exponential backoff, randomized jitter, per-dependency circuit breaker | Attempt counts, delays, breaker thresholds/reset, elapsed-time budget: **BAT-OQ-005** |
| Validation or permission failure | Permanent; do not automatically retry | Safe codes/statuses and corrected-input replay procedure unresolved |
| Connector provider throttling | Honor `Retry-After`, exponential backoff/jitter, workspace quotas, fair scheduling | Provider delay format, retry ceiling, fairness algorithm, queue policy: **BAT-OQ-007** |
| Poison connector record | Quarantine after bounded retries; retain reason/correlation/remediation; remaining batch may proceed | Distinction from immediately permanent schema validation; retry count and mixed status: **BAT-OQ-005**, **BAT-OQ-007** |
| Revoked connector credentials | Queued job `CONNECTOR_REAUTH_REQUIRED`; no token disclosure | Credential refresh/reauthorization workflow and paused-job treatment unresolved |
| Invalid model output | Bounded structured validation retries; `MODEL_OUTPUT_INVALID`; no publish | Whether parsing retry or fresh invocation, count, provider deadline: **BAT-OQ-012** |
| Missing approval, call-budget exhaustion, repeated invalid plan, policy denial, deadline expiry | Stop/terminate and report exact checkpoint | Waiting-versus-failure and recoverable timeout representation: **BAT-OQ-012–013** |
| Workspace token exhaustion | Terminal current run; no automatic model/data-class change | Token accounting and reservation-release behavior unresolved |
| New-run admission fails token/queue-age/provider thresholds | HTTP `429` plus `Retry-After`; saved cases remain available | Thresholds and retry calculation unresolved |
| Optional webhook failure | Exponential-backoff retry; no internal transition rollback | Retryable acknowledgments, count, age/deadline, dead letters unresolved |
| Object access, lost heartbeat, primary-region outage | Fault-injection/recovery verification required | Worker takeover and recovery policy details unresolved |

**Sources:** S, pp. 27–29, 38, 41–42, 49, 55, 69–70; p. 89, `TST-008`; p. 90, Appendix F.

**BAT-BKP-001 — Confirmed:** Fair connector scheduling prevents large tenants from starving smaller workspaces. Extraction/embedding workers scale on queue age and throughput. API replicas scale on utilization and latency.  
**Source:** S, p. 28, §7.3.1; p. 19, §4.2.1.

**BAT-BKP-002 — Needs confirmation:** Per-job queue capacity, worker concurrency, scale thresholds, batch sizes, provider reservations, starvation bounds, heartbeat/retry deadlines, and admission control for jobs other than new AI runs. The reference `20` concurrent runs per large tenant is a load assumption, not a universal selected quota.

### Rollback and Compensation

| Failure boundary | Confirmed response | Prohibited assumption / required confirmation |
|---|---|---|
| Stale/unauthorized domain mutation | Reject without business-state change; retain safe rejection evidence | No silent overwrite or automatic “latest revision” retry |
| Failed index write | Keep accepted source metadata; compare fingerprints and retry through reconciliation | Do not roll back accepted document/source records |
| Publication transaction failure | Gate and final pointer must not partially commit | Exact transactional mechanism remains unresolved |
| Unsafe file | Quarantine, no indexing | No automatic unsafe-content release/download |
| Failed optional webhook | Internal case transition stays committed | No rollback because recipient unavailable |
| Partial sync poison record | Durable quarantine exception; remaining batch may proceed | Do not silently skip the exception or advance past undurable items |
| Partial provisioning | Incomplete visible; sync blocked | No invented deletion of successfully created resources; compensation Needs confirmation |
| Partial purge/deletion | Holds preserved, actual removals/receipts retained; no false verified completion | No all-or-nothing distributed rollback or force delete |
| Failed rebuild validation | Do not switch to unvalidated generation | Cleanup, retry, or old-generation rollback policy Needs confirmation |
| Release canary regression | Automated traffic rollback; binary routing reversed first | No automatic database down-migration; data compensation only if explicitly supported |
| Failed evaluation or low confidence | Report actual result; release blocked when safety/confidence criteria fail | Do not rewrite expected fixtures or treat execution completion as a pass |

**Sources:** S, pp. 20, 28–32, 34, 45, 49, 55, 72, 76, 78–80.

### Maximum Included-Material Classification

<a id="bat-cls-001"></a>

**BAT-CLS-001 — Confirmed:** Preserve [API-CLS-001](02_api.md#api-cls-001) and `DAT-CLS-001`. For every run, model routing, log redaction, retention, and approval policy use the maximum information class of all included material: `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`.

| Batch boundary | Required application |
|---|---|
| BAT-003/BAT-004 | Preserve material classification/provenance needed by later controls; exact source/version mapping unresolved |
| BAT-010 | Apply highest included class to initial/fallback routing, redaction, retention selection, and approval policy |
| BAT-011 | Validate the applicable highest-class approval/evidence policy before publication |
| BAT-013/BAT-014 | Apply classification-dependent retention where relevant without inventing a class-specific duration |
| Batch telemetry | Apply relevant maximum-class redaction in addition to global document/secret prohibitions |

An `INTERNAL` case using permitted `RESTRICTED` evidence must use the applicable `RESTRICTED` controls. Under reference `policy.require_human_review_for: [HIGH_RISK, RESTRICTED]`, required review cannot be bypassed using `policy.auto_publish_classification: INTERNAL`. `HIGH_RISK` is a risk category, not another information class.

**Source:** S, p. 62, §17.2.1; p. 90, Appendix F.  
**Needs confirmation — BAT-OQ-024:** Material provenance, unclassified-material treatment, policy activation, and per-class mappings. The aggregation obligation itself is not open. No automatic case relabeling, seventh policy input, or public classification property is introduced.

### Notifications, Logging, and Monitoring

#### Required Evidence

| Requirement ID | Status | Requirement | Source |
|---|---|---|---|
| BAT-LOG-001 | Confirmed | Requests/workflow boundaries retain `trace_id` and `correlation_id`, independent of provider trace identifiers. | S, p. 16, §3.3.1; p. 64, §18.1.1 |
| BAT-LOG-002 | Confirmed | Child spans represent DB, connector, retrieval, model, and approval stages. Attributes contain identifiers and policy outcomes, never user-document content or API secrets. | S, p. 64, §18.1.1 |
| BAT-LOG-003 | Confirmed | Accepted transitions have correlated audit evidence; duplicate delivery records duplicate outcome without another accepted mutation. | S, chapter failure/acceptance sections; pp. 48–50 |
| BAT-LOG-004 | Confirmed | Preserve safe source/version/checkpoint/operation identifiers, parser quality/injection indicators, token counts/digests, and applicable receipt/manifest references. Do not log full prompts by default. | S, pp. 31–32, 39, 50, 62, 66, 80, 90 |
| BAT-LOG-005 | Confirmed reference setting | `observability.trace_sample_rate: 0.10`; diagnostic default `30` days; audit fictional `7` years. Diagnostic sampling does not remove obligatory accepted-transition audit evidence. | S, pp. 62 and 66; p. 90, Appendix F |
| BAT-LOG-006 | Needs confirmation | Exact job-status/log schema, event/attempt counts, job metrics labels, correlation placement, retention for job ledgers, and safe error details. | **BAT-OQ-003**, **BAT-OQ-011**, **BAT-OQ-015**, **BAT-OQ-025** |

#### Monitoring and Alert Conditions

| Signal | Source-required use | Thresholds or implementation Needs confirmation |
|---|---|---|
| Queue oldest age and index backlog | Detect delayed indexing and identify tenant/index generation | Age/backlog threshold, evaluation interval |
| Queue age and throughput | Extraction/embedding worker scaling | Scale rules, min/max workers |
| Outbox lag, event ID, parser flags, search throttling, ACL revision | Delayed-indexing diagnosis | Exact metric definitions/queries |
| Provider throttling/token use | AI/cost monitoring and controlled retries/admission | Rate thresholds and time windows |
| Approval backlog age | AI-specific operational signal | Page/escalation threshold |
| Grounding pass rate and retrieval empty rate | AI quality/reliability monitoring | Formula, denominator, reporting window |
| Request/error rate, latency, saturation | Golden signals and SLO monitoring | Burn-rate thresholds/window |
| Stale ACL propagation or missing approval enforcement | User-impacting security/reliability incidents warrant paging | Routing and urgency contract |
| Routine token-spend anomalies | Create tickets with configured owner and threshold | No actual owner or numeric threshold is supplied |
| Backup status and recovery evidence | Security/SRE validation before promotion | Status schema/check cadence |

**Source:** S, pp. 19, 64–66, 69–70, 73; p. 90, F.1.  
**Needs confirmation — BAT-OQ-025:** Monitoring schemas, formulas, thresholds, alert routing, ticket configuration, and notification channels. No email, SMS, chat, or notification-center job is confirmed.

#### Progress and External Notification Boundaries

- **Confirmed:** AI progress is exposed through API-007 SSE with monotonic offsets, `Last-Event-ID`, scoped retained-event backfill, and server reconstruction on refresh.
- **Confirmed:** Connector run and document status inquiries exist through API-025/API-018.
- **Confirmed:** Optional signed outbound webhooks are BAT-024.
- **Needs confirmation:** Progress transport for evaluation, backfill, provisioning, archive, rollup, export, deletion, migration, and replay; completion notifications and recipients.
- **Needs confirmation:** Browser Notification fields/channels/read state. DAT-062/ API-059 component presence does not establish delivery behavior.

**Source:** S, pp. 28–32, 55, 58–59, 74–80. Earlier `API-OQ-006`, `API-OQ-025`; **BAT-OQ-003**, **BAT-OQ-025**.

### Incident Recovery Procedures

#### Delayed Document Indexing

1. Detect queue oldest age and index backlog; identify the affected tenant and index generation.
2. Pause only the faulty connector or indexer shard.
3. Keep accepted source records durable.
4. Inspect event ID, outbox lag, parser flags, search throttling, and source ACL revision.
5. Replay validated outbox records using BAT-022 within a bounded operator-controlled scope.
6. Compare source fingerprints against indexed versions.
7. Run denied-access probes before closing recovery.
8. Document audit IDs, time window, blast radius, quality effect, and preventive action.

**Source:** S, p. 90, F.1.  
**Needs confirmation:** Detection threshold, pause/re-enable interface, replay batch limit, and incident-record schema — **BAT-OQ-009**, **BAT-OQ-020**, **BAT-OQ-025**.

#### Suspected ACL Leak

1. Suspend affected index aliases.
2. Revoke cached evidence.
3. Preserve audit traces.
4. Execute scoped replay of ACL revisions through applicable controlled recovery.
5. Re-enable search only after negative access tests pass.

**Source:** S, p. 79, §22.2.2.  
**Needs confirmation:** Control APIs/roles, scope and verification matrix — **BAT-OQ-010**, **BAT-OQ-020**.

#### Model Provider Outage

1. Disable new generation admission.
2. Keep manual case and evidence workflows available.
3. Display degraded status.
4. Permit lexical fallback during vector degradation only with a visible reduced-quality flag.
5. Continue all authorization, classification, and approval checks.
6. Page on-call only when the availability budget is impacted.

**Source:** S, p. 69, §19.2.2; p. 79, §22.2.1.  
**Needs confirmation:** Admission/degraded-mode controls and budget threshold — **BAT-OQ-012**, **BAT-OQ-025**.

## Acceptance Criteria

### Verification Basis

**BAT-AC-BASIS-001 — Confirmed:** Use synthetic identities, cases, documents, and provider replies. Include successful, empty, mixed-permission, mixed-classification, adversarial, malformed, duplicate, delayed, and partial-failure fixtures. Record every randomized seed. Critical isolation and approval tests pass with zero exceptions.  
**Source:** S, p. 74, Chapter 21 invariant; p. 89, E.1–E.2.

A test blocked by an unresolved field, threshold, status, or guard remains an acceptance obligation with the associated question. It must not be made executable by inventing a contract.

### Success, Safety, and Recovery Tests

| Acceptance ID | Related requirements | Procedure | Expected result | Source / dependency |
|---|---|---|---|---|
| BAT-AC-001 | BAT-CTX-001–006; all applicable jobs | Attempt job execution with foreign tenant scope, invalid service audience, or missing trusted tenant context; reuse pooled connection across tenants | Unauthorized work/data access rejected; no denied business mutation; pool scope reset; safe evidence only | S, pp. 18, 21–23, 86; `API-AC-001/004/039`, `DAT-AC-001/002/005` |
| BAT-AC-002 | BAT-IDEM-002–003 | Repeat identical case/job creation under same key, then change fingerprint under reused key | Original operation/outcome returned; one accepted result; changed request `IDEMPOTENCY_CONFLICT`, cataloged `409` where specified | S, pp. 25, 54, 89 `TST-001–002`; namespace/TTL BAT-OQ-011 |
| BAT-AC-003 | BAT-001 | Consume authorized `CaseCreated` and inspect classification | Labels, confidences, provenance attached to applicable case; correction requires reason code; no invented automatic triage edge | S, pp. 12, 40, 87; BAT-OQ-006 |
| BAT-AC-004 | BAT-001; BAT-CON-001 | Delay classifier outcome until after accepted correction/newer case revision | Stale/unauthorized mutation does not overwrite business state; corrected provenance preserved under approved precedence contract | S, pp. 12, 25, 48; detailed rule BAT-OQ-006 |
| BAT-AC-005 | BAT-002 | Sync a permitted incremental source batch | Stable source identities/permissions/history preserved; durable cursor/high-watermark/error ledger available; cursor follows durable preceding outcomes | S, pp. 27–28; `API-AC-024`, `DAT-AC-024` |
| BAT-AC-006 | BAT-002; BAT-RES-001 | Fail midway through sync and retry | No skipped undurable preceding item or duplicate accepted effect; resume uses durable outcomes/cursor | S, p. 28, §7.2.1 |
| BAT-AC-007 | BAT-002 | Exhaust bounded poison-record retries while other items are processable | Poison record quarantined with reason/correlation/remediation; exception ledger preserved; remaining batch may proceed | S, p. 29, §7.3.2; count/status BAT-OQ-007 |
| BAT-AC-008 | BAT-002 | Revoke source credentials before queued execution | `CONNECTOR_REAUTH_REQUIRED`; no token in status, logs, or provider context | S, p. 27, §7.1.2 |
| BAT-AC-009 | BAT-002; BAT-BKP-001 | Use connector lacking capability and large-tenant load alongside smaller workspaces | Explicit visible lower-trust warning; unsupported feature not assumed; smaller workspaces not starved | S, pp. 27–28; fairness criteria BAT-OQ-007 |
| BAT-AC-010 | BAT-003 | Process allowed safe PDF/DOCX/HTML/UTF-8 text within defined limits | Validated durable ingestion; scan before parse; no macro execution or embedded remote fetch; immutable derivatives/provenance | S, pp. 30–32, 83; exact boundaries BAT-OQ-008 |
| BAT-AC-011 | BAT-003/BAT-004 | Submit unsafe/polyglot PDF and decompression-unsafe/oversized fixtures | Fail closed; unsafe input quarantined; no indexing; safe errors only | S, pp. 30, 88 `T-04`, 89 `TST-015` |
| BAT-AC-012 | BAT-003 | Normalize same content under approved pipeline; reprocess under changed pipeline version | Claims unchanged; source URI/hash/page/optional box preserved; immutable derivative identities and side-by-side history retained | S, p. 31; identity algorithm BAT-OQ-008 |
| BAT-AC-013 | BAT-003 | Process safe low-quality/OCR-opt-in fixtures | Quality flags retained; safe low-quality document viewable but excluded from autonomous recommendations; OCR provenance marked and only opted-in fallback | S, pp. 31–32; thresholds BAT-OQ-008 |
| BAT-AC-014 | BAT-004 | Consume `DocumentNormalized` and inspect indexed rows | Required tenant/workspace/version/chunk/language/classification/text and `1536`-dimension vector represented; committed event/correlation retained | S, pp. 34, 87 |
| BAT-AC-015 | BAT-004/BAT-009 | Fail index write after accepted source metadata, then reconcile | Accepted source remains durable; fingerprint comparison and retry repair derivative outcome | S, p. 49, §13.2.2 |
| BAT-AC-016 | BAT-005 | Rebuild parallel generation; fail completeness/recall check, then pass approved checks | Failed generation not activated; successful read-alias switch atomic after checks | S, p. 34, §9.1.2; thresholds/race BAT-OQ-009–010 |
| BAT-AC-017 | BAT-006 | Revoke source access after indexing/cache fill; issue next query | No forbidden evidence on next query/model context; cache invalidated before release rather than waiting for TTL | S, pp. 28, 53, 89 `TST-004` |
| BAT-AC-018 | BAT-007 | Detect source deletion while stale derivative remains | Tombstone durable; soft-deleted source not retrievable; index removal scheduled/executed under defined contract | S, pp. 28, 51; schedule BAT-OQ-010 |
| BAT-AC-019 | BAT-008/BAT-022 | Replay same event `100` times, including delayed/stale delivery | Exactly one accepted business transition; duplicates recorded without mutation; no cross-partition-order dependence | S, pp. 48, 88 `T-07`, 89 `TST-007` |
| BAT-AC-020 | BAT-008/BAT-010 | Crash between persisted checkpoint and downstream delivery; refresh/reconnect | Progress reconstructed from durable server state; idempotent downstream outcome; scoped retained SSE backfill; connection loss not completion | S, pp. 49, 55, 58; acknowledgment details BAT-OQ-011 |
| BAT-AC-021 | BAT-010 | Start admitted valid run and inspect plan/steps | Immediate durable run; plan before side effects; checkpoint before dispatch; depth `8`/calls `16` respected | S, pp. 40, 49, 58, 90 |
| BAT-AC-022 | BAT-010 | Supply recursive hints, arbitrary discovered tool, forged arguments, or equivalent substitute for denied action | Denied before unauthorized dispatch; no discovery-based grant or substitute-tool bypass; bounded execution | S, pp. 41–42, 87–89 `T-10`, `TST-014` |
| BAT-AC-023 | BAT-010 | Force model unknown fields, invalid citations, or control-character injection | Bounded validation retries; `MODEL_OUTPUT_INVALID`; no publish | S, p. 38; p. 89 `TST-005` |
| BAT-AC-024 | BAT-010/BAT-011 | Retrieve insufficient support or generate missing citations | `NO_SUPPORTED_EVIDENCE` where applicable; missing-citation needs-review/unsupported outcome; never fabricated approval | S, pp. 36, 89 `TST-009` |
| BAT-AC-025 | BAT-010 | Exhaust token/call/time budget or deny policy | Stop at actual checkpoint; no automatic model/data-class change or publication; timeout/wait state follows confirmed-to-be-completed contract | S, pp. 38, 41, 49, 90; BAT-OQ-012 |
| BAT-AC-026 | BAT-010; BAT-BKP-001 | Inject provider `429` bursts and failed admission thresholds | Capped retries/admitted load; new-run client `429` plus `Retry-After`; saved cases available | S, pp. 69, 89 `TST-008` |
| BAT-AC-027 | BAT-010/BAT-011; BAT-CLS-001 | Run authorized `INTERNAL` case with permitted anchored quality-appropriate `RESTRICTED` evidence; inspect controlled internal policy/provenance; attempt publish without required human decision | Routing, log redaction, retention, and approval all use applicable `RESTRICTED` controls; no INTERNAL auto-publication bypass; publication blocked without satisfied gate | S, pp. 62, 90; `API-AC-034`, `DAT-AC-023`; mappings BAT-OQ-024 |
| BAT-AC-028 | BAT-011 | Change artifact or source ACL after review; replay approval against different artifact | Stale/wrong-artifact publication rejected and audited; current authorization recomputed | S, pp. 45–46, 89 `TST-006` |
| BAT-AC-029 | BAT-011 | Inject failure between gate record and pointer update | No partially committed publication; gate/pointer atomic | S, p. 45, §12.3.1 |
| BAT-AC-030 | BAT-011/BAT-012 | Attempt own high-risk approval; expire required review task | Self-approval blocked; expiry produces no implicit approval; escalation/reassignment recorded | S, pp. 11, 45, 89 `TST-010` |
| BAT-AC-031 | BAT-013 | Include open, ineligible closed, eligible closed, and held cases in routine retention scope | Only eligible closed cases qualify; approved lineage/holds protected; actual outcomes receipted | S, p. 26; eligibility/period BAT-OQ-014 |
| BAT-AC-032 | BAT-014 | Apply diagnostic/audit retention to mixed categories/holds | Distinct `30`-day default and fictional `7`-year policy; held evidence retained with exceptions; no generic diagnostic purge of audit history | S, pp. 66, 90; calculation BAT-OQ-015 |
| BAT-AC-033 | BAT-015 | Archive batch, verify chain, attempt historical edit | Append-only batch-hash archive retained independently; historical modification rejected | S, pp. 62, 88 `T-09`; format BAT-OQ-015 |
| BAT-AC-034 | BAT-016 | Roll up synthetic model/embedding/storage/index usage with multiple cost centers/deployments; rerun same day | Budget/forecast/rejected-request concepts and attribution preserved; replay does not double accepted accounting effect | S, p. 65; formulas/day/rerun BAT-OQ-016 |
| BAT-AC-035 | BAT-017 | Evaluate frozen signed reference corpus | `1,200` synthetic cases/expected citations/decisions retained; actual target metrics and domain confidence/shift reported; execution completion distinct from quality pass | S, pp. 75–76, 88–89 |
| BAT-AC-036 | BAT-017/BAT-026 | Replace expected fixtures; force critical failure/low confidence/safety regression | Fixture integrity control fails where poisoned; critical isolation/approval and low-confidence outcome block release regardless of benchmark score | S, pp. 76, 88 `T-12`, D.1, 89 `TST-016` |
| BAT-AC-037 | BAT-018 | Fail provisioning partway, attempt sync, then replay same authorized provisioning | Incomplete visible; sync blocked; one idempotent completed outcome establishes required policy/key/roles/quotas/stubs | S, p. 78; compensation/resume BAT-OQ-018 |
| BAT-AC-038 | BAT-019 | Backfill bounded historic windows with partial failures and empty queue but incomplete index coverage | Stable IDs and per-batch receipts; no false readiness based only on queue emptiness | S, p. 78; receipt/coverage BAT-OQ-018 |
| BAT-AC-039 | BAT-020/BAT-021 | Request export/delete as single Admin, then independently authorized scope | Single-Admin bypass rejected; accepted cataloged request `202`; two independent checks required | S, pp. 78, 83, 88 `T-11` |
| BAT-AC-040 | BAT-020 | Complete authorized export and inspect package | Case metadata, approved artifacts, source references, audit manifests/checksums; no secrets/internal model prompts | S, p. 79; format BAT-OQ-019 |
| BAT-AC-041 | BAT-021 | Delete held inventory and inject blob/index partial failure | Protected records retained/receipted; actual removals preserved; no unverified completion or force deletion | S, p. 80; p. 89 `TST-013`; partial status BAT-OQ-019 |
| BAT-AC-042 | BAT-022 | Replay without reason/dry-run/scope; then valid replay and approved schema transform | Unguarded replay rejected; valid bounded replay preserves identity except explicit provenance-linked migration | S, p. 50 |
| BAT-AC-043 | BAT-023 | Backfill compatible nullable addition; try enforcement before old replicas drain or remove active-reader field | Bounded backfill; compatibility retained; invalid enforcement/removal blocked | S, pp. 52, 55, 72 |
| BAT-AC-044 | BAT-024 | Fail recipient after committed case transition | Case commit unchanged; signed delivery follows defined retry; recipient verifies signature/age | S, p. 55; transport BAT-OQ-022 |
| BAT-AC-045 | BAT-025 | Region recovery with relational/object/index recipes | Consistency and safety verified; RPO `<=15 minutes`, RTO `<=4 hours` under reference profile | S, pp. 19, 69, 89 `TST-012` |
| BAT-AC-046 | BAT-026 | Submit unverified digest/canary regression; inspect valid release evidence | Invalid/regressed promotion blocked; traffic rollback, no automatic DB down-migration; signed tests and reconstructible versions | S, pp. 71–73, 88–89 |
| BAT-AC-047 | BAT-LOG-001–005 | Inspect job/public errors, provider context, and sampled diagnostics | No source-document content/API secrets/full unsafe error prompts; required correlated audit retained independently | S, pp. 54–56, 62–66, 84 |
| BAT-AC-048 | Incident procedures | Recover delayed indexing and suspected ACL leak; separately disable generation | Affected scope contained; accepted source durable; bounded replay/fingerprints/negative probes before resume; manual/evidence available; no safety bypass | S, pp. 69, 79, 90 F.1 |
| BAT-AC-049 | BAT-CON-001; BAT-CTX | Inject lost worker heartbeats, duplicate events, object faults, and regional outage | Safety and recovery measured; no duplicate accepted mutation or authorization bypass | S, p. 70, §19.3.2; takeover thresholds BAT-OQ-004 |
| BAT-AC-050 | Key/secret rotation boundary | Exercise defined rotation mechanism and inspect traces/context | Vault/scope protections preserved; no request-path bulk re-encryption requirement or leaked credential | S, pp. 21, 63; mechanism BAT-OQ-023 |

### No-Input and Ineligible-Input Coverage

The source requires empty fixtures but does not define a universal `NO_INPUT`, `SKIPPED`, or successful-no-op job status. None is invented.

| Acceptance ID / family | Test input | Confirmed expected safety result | Completion/status Needs confirmation |
|---|---|---|---|
| BAT-AC-051 — Event consumers | No applicable event, duplicate-only input, or stale delivery | Duplicate event does not reapply mutation; processing does not fabricate a supported business event/result | Empty launch receipt, polling behavior, stale-event disposition — BAT-OQ-003/011 |
| BAT-AC-052 — Sync/backfill/index | No provider changes, empty historic window, or no applicable normalized chunks | Cursor durability/provenance rules remain; unsafe input cannot be indexed; readiness cannot be inferred solely from queue emptiness | Whether cursor/watermark advances, empty batch receipt, index completion, empty-source status — BAT-OQ-007–009/018 |
| BAT-AC-053 — AI retrieval | Empty, ambiguous, or insufficient supported evidence | `NO_SUPPORTED_EVIDENCE`, not fabricated context; only defined clarification/human routing | HTTP/result envelope and workflow state — BAT-OQ-012 |
| BAT-AC-054 — Expiry/retention/purge | No expired tasks, no eligible closed cases, or held-only inventory | No implicit approval; no purge of ineligible/open routine-retention cases; held records protected/receipted when processed | Empty-run summary, zero-work receipt, held-only completion — BAT-OQ-013–015/019 |
| BAT-AC-055 — Rollup/archive/export | Zero usage, no archive entries, or empty authorized export inventory | Attribution, immutable audit, independent approval, and exclusion/integrity rules still apply | Zero rows versus zero-valued report, empty archive/package behavior — BAT-OQ-015–016/019 |
| BAT-AC-056 — Evaluation | Empty/incomplete/missing corpus or no usable statistical evidence | Actual absence cannot be fabricated into a passing reference evaluation; defined statistical-confidence release gate remains obligatory | Validation/error/result status and exact confidence handling — BAT-OQ-017 |
| BAT-AC-057 — Replay/migration/webhook | No selected replay records, no remaining backfill rows, or no applicable subscription | No replay authorization bypass, no active-reader schema violation, no fabricated delivery acknowledgment | Empty-result status, enforcement prerequisites, no-delivery receipt — BAT-OQ-020–022 |

**Source:** S, p. 36, §9.3.2; pp. 26, 45, 52, 55, 76, 78–80; p. 89, E.1. The precise no-work contracts remain open.

### Reference Capacity and Operational Targets

| Target | Source-confirmed meaning |
|---|---|
| `2,000` active daily users; `60` requests/second steady; `180` burst | Reference integrated workload, not batch launch rates |
| `100,000` indexed documents per tenant | Reference capacity maximum, not a new universal job argument constraint |
| `20` concurrent AI runs per large tenant | Reference load assumption, not every workspace’s configured quota |
| Typical `1 MB` source → approximately `40–120` chunks | Sizing estimate, not a normalization acceptance range |
| Public API availability `99.9%` monthly; case-create P95 `<300 ms`; search P95 `<1.5 s` excluding connector fetch | Integrated service objectives; generation measured separately, not universal batch duration limits |
| RPO `<=15 minutes`; RTO `<=4 hours` | Reference recovery targets |
| Depth `8`; tool calls `16`; reference run timeout `180` seconds | Applicable AI workflow limits; not extraction/export/evaluation timeouts |

**Source:** S, pp. 65, 68–69, §§18.2.1 and 19.1–19.3; p. 90, Appendix F.

**Needs confirmation:** Per-job throughput, queue-age SLA, maximum execution duration outside AI, batch/window size, scale ceiling, and recovery deadline. These must not be derived from unrelated reference numbers.

## Consistency and Open Questions

### Consistency Findings and Required Amendments

Earlier specifications are not rewritten here. The following retain conflicts, evidence distinctions, and required controlled amendments.

| Consistency ID | Evidence / issue | Affected identifiers | Required clarification or amendment |
|---|---|---|---|
| BAT-CNS-001 | Source describes background functions but no `BAT-` IDs, executable names, or twenty-six deployment units. | BAT-001–026; BAT-SCP-003; DAT-INV-001–002 | Confirm implementation grouping/ownership. Logical inventory must not create duplicate services, jobs, or tables. |
| BAT-CNS-002 | `CaseCreated` runs classifier, but no automatic classification-to-state trigger is defined. Six case edges are explicitly confirmed; closing/reopening remain partial. S, pp. 12, 25, 87. | BAT-001/BAT-010; `SCR-002-T01–T08`; API-OQ-004; DAT-STATE-001 | Preserve six edges and CLOSED finality. Do not infer automatic triage, Reject-to-case transition, closing origin, or reopening target. |
| BAT-CNS-003 | `POST /v1/runs` and `POST /v1/cases/{caseId}/runs` coexist. S, pp. 15–17, 40, 83. | BAT-010; API-005/API-032; SF-CON-007; API-CNS-002 | Resolve route relationship without creating unrelated duplicate workflows or silently removing a path. |
| BAT-CNS-004 | Missing-approval termination, `AWAITING_REVIEW`, recoverable timeout, and `FAILED` enum coexist. `180`-second runtime and configured review SLA are distinct. S, pp. 12, 41, 45, 49, 82, 90. | BAT-010–012; API-TMO-001–002; DAT-STATE-002; SF-CON-004 | Define runtime versus review wait, worker release/resume, missing-approval stop, and timeout representation without new states. |
| BAT-CNS-005 | Connector poison records have bounded retries, while workflow validation/permission failures are permanent. S, pp. 29, 49. | BAT-002; retry table; API-RTY-002–003 | Define malformed-source processing versus schema-invalid job arguments; do not retry authorization failure or treat every parser failure as immediately identical. |
| BAT-CNS-006 | Cursor requires durable ingestion outcomes, not necessarily fully indexed/readable documents. S, pp. 28, 78. | BAT-002/BAT-019; DAT-028; DAT-058-F02 | Define outcome stage and coverage criteria. Do not equate cursor advancement, queue emptiness, normalization, or HTTP `202` with search readiness. |
| BAT-CNS-007 | Revoked ACL effective before next retrieval coexists with asynchronous index/cache delivery. S, pp. 27–28, 48, 53. | BAT-006/BAT-008; API-REC-001; DAT-RI-006 | Specify fail-closed propagation/barrier and concurrent cache-fill handling. Eventual processing cannot weaken next-query security. |
| BAT-CNS-008 | Normalization fingerprint/pipeline-derived identities coexist with UUIDv7 policy and abbreviated version catalog. S, pp. 31, 51, 85. | BAT-003/BAT-004; DAT-006-F01/F06; DAT-CNS-008 | Define derivative identity and parser/pipeline mapping; no invented local version column, hash encoding, or overwrite behavior. |
| BAT-CNS-009 | Index failure must retain accepted source; rebuild switches only after checks. S, pp. 34, 49. | BAT-004–005/BAT-009; API-TXN-003; DAT-TXN-003 | Define partial index/readiness and delta handling without full-source rollback or unvalidated alias activation. |
| BAT-CNS-010 | Maximum material class applies to routing, redaction, retention, approval. Earlier screen summary needs explicit four-control linkage. S, p. 62. | BAT-CLS-001; BAT-AC-027; `SCR-002-F10`; API-CNS-013; DAT-CNS-015 | Required earlier amendment remains. Preserve all four controls; no case-label-only shortcut, extra policy input, or automatic case relabeling. |
| BAT-CNS-011 | INTERNAL auto-publish setting must coexist with HIGH_RISK/RESTRICTED review, current ACL, supported evidence, and exact hash. S, pp. 44–46, 62, 90. | BAT-010/BAT-011; BAT-CLS-001; API-CNS-014; SF-CON-009 | Complete policy semantics without bypass. Execution/decision success does not establish publication success. |
| BAT-CNS-012 | Routine case retention only eligible closed cases; source tombstone purge and tenant decommission are separately described. S, pp. 26, 51, 78–80. | BAT-007/BAT-013/BAT-021; DAT-CNS-016 | Define selector/authorization precedence and related-object scope. Do not apply CLOSED restriction blindly to all logs/objects or use decommission to bypass holds. |
| BAT-CNS-013 | Tenant export/deletion terminology differs from workspace routes; `Admin + approver` and two independent checks are both stated. S, pp. 78–83. | BAT-020/BAT-021; API-CNS-008; DAT-CNS-016; SF-CON-010 | Resolve extent and independent proof/actors. No one-actor interpretation or invented approval endpoint. |
| BAT-CNS-014 | Chapter 22 repeatedly associates export/provisioning text with `TenantDeletionVerified`; C.1 specifically closes purge record from manifest/receipt hash. S, pp. 78–80, 87. | BAT-018/BAT-020/BAT-021; DAT-EVT-001; API event register | Do not emit deletion verification for export or provisioning merely because of repeated chapter boilerplate. Clarify their own completion events if needed; none is invented. |
| BAT-CNS-015 | Daily rollup, scheduled purge, continuous backup, configured SLA provide different cadence detail levels. S, pp. 45, 51, 65–66, 69. | BAT-TIME-002; BAT-012–016/BAT-025 | Preserve confirmed cadence concepts; confirm clock/timezone/frequency. UTC timestamps and RPO do not select schedules. |
| BAT-CNS-016 | Case key `24` hours, workflow dedup `24` hours, diagnostics `30` days, audit `7` years, short cache TTL are separate policies. | BAT-IDEM-003–004; BAT-014; DAT-RET-002–006 | Do not generalize one TTL to every HTTP key, consumer, SSE, archive, or ledger. Confirm each scope and expiry behavior. |
| BAT-CNS-017 | Source register “immutable derivative” labels are generic; current job/case/index status can be mutable while provenance/history stays immutable. | BAT-001–026; DAT-CNS-003; DAT-HIS-001–006 | Preserve mutable projections and immutable history separately; do not make supported job state unmodifiable or overwrite historical decisions. |
| BAT-CNS-018 | GET APIs and component registers do not confirm new launch APIs or scheduled jobs. | BAT-004–006/BAT-008–009/BAT-014–016/BAT-025; API-CNS-011; DAT-LIFE-001 | Retain inquiry boundaries; do not launch indexing from search GET/POST, purge from metrics GET, or promotion from health GET. |
| BAT-CNS-019 | Existing uppercase literal errors differ from generic snake-case wording. S, pp. 54, 84. | Retry/error behavior; API-ERR-001; DAT-CODE-009; SF-CON-005 | Preserve exact codes; define unspecified failures separately. No new batch exit codes or HTTP mappings are approved. |
| BAT-CNS-020 | Low-quality safe documents remain viewable but excluded from autonomous recommendation; unsafe quarantined documents never indexed. S, pp. 30–32. | BAT-003/BAT-004; DAT-029; API-OQ-007 | Keep quality and malware outcomes distinct; do not infer low-quality no-index rule or unsafe download permission. |
| BAT-CNS-021 | CI/release and continuous backup are source operational automation, not automatically application worker jobs. Key rotation capability lacks a standalone batch contract. | BAT-025/BAT-026; rotation boundary; DAT-055–056/DAT-052 | Confirm platform/application division and executable ownership without inventing schedules or re-encryption jobs. |

### Batch Open-Decision Register

These questions are also recorded beside affected requirements. No decision, owner, deadline, or approval is established here.

| Question ID | Status | Required decision / missing contract | Affected requirements | Earlier links and evidence |
|---|---|---|---|---|
| BAT-OQ-001 | Needs confirmation | Schedules, scheduler timezone, clock times, timer/polling choice, bounded-window/cutoff semantics, missed/catch-up launches, maintenance windows | BAT-TIME-002; BAT-002/005/007/009/012–016/019/023/025–026 | [03_data.md, DAT-OQ-014/018/020](03_data.md#data-open-decision-register); API-OQ-021. S, pp. 26, 45, 51, 65–66, 69, 78. |
| BAT-OQ-002 | Needs confirmation | Logical job grouping, executable/scheduler/queue topology, scoped identities/roles, service ownership and platform-managed versus application processing | BAT-SCP-003; BAT-CTX-002–003; all inventory | [02_api.md, API-OQ-002](02_api.md#api-open-decision-register); DAT-OQ-002; earlier OQ-022/024. S, pp. 15–20. |
| BAT-OQ-003 | Needs confirmation | Job argument schemas, required fields/defaults/types, receipt/result/status/exit codes, progress, empty-input outcomes, repeated completion, manual launch where undefined | All incomplete job contracts; BAT-AC-051–057 | API-ASYNC-001–003/API-OQ-017; DAT-STATE-005; earlier OQ-005. S, pp. 54–59, 83–85. |
| BAT-OQ-004 | Needs confirmation | Concurrent launch policy, locking/lease/fencing, partition scope, heartbeat/takeover/drain, maximum concurrent workers, processing/commit units and cross-store crash safety | BAT-CON-001; BAT-TXN-001; concurrency table | API-OQ-017/018; DAT-OQ-003/012/020. S, pp. 25, 28, 45, 49–52, 70. |
| BAT-OQ-005 | Needs confirmation | Dependency retry counts/delays/jitter/breakers/deadlines; poison-parser versus validation classification; exhaustion/dead-letter conditions; stable safe failure codes | Retry table; BAT-002/003/008–010 | API-RTY-001–004/API-OQ-017; DAT-OQ-006–007/012. S, pp. 29, 38, 42, 49. |
| BAT-OQ-006 | Needs confirmation | Classifier catalogs/confidence/provenance, case/attachment revision snapshot, correction precedence, mutation contract, missing-context/rerun rules and state trigger | BAT-001; BAT-AC-003–004 | API-OQ-005; DAT-OQ-005; [01_screen_functions.md, OQ-008/010](01_screen_functions.md#consolidated-open-questions). S, pp. 12, 25, 40. |
| BAT-OQ-007 | Needs confirmation | Connector providers/permissions, request/states, cursor/high-watermark/order semantics, batch size, durable-outcome stage, concurrency/fairness/retry policy, credential reauthorization | BAT-002; BAT-AC-005–009/052 | API-OQ-011; DAT-OQ-006; earlier OQ-016/022. S, pp. 27–29. |
| BAT-OQ-008 | Needs confirmation | Upload/MIME/MB/archive/parser bounds; version/fingerprint algorithm; OCR option and extraction quality/empty-document handling; checkpoints/status/rerun | BAT-003; BAT-AC-010–013/052 | API-OQ-007; DAT-OQ-007–008; earlier OQ-015. S, pp. 30–32. |
| BAT-OQ-009 | Needs confirmation | Search/embedding provider and schema, vector/batch controls, index partial commit/readiness, rebuild launch and coverage/completeness/recall thresholds, reconciliation inventory | BAT-004–005/BAT-009/BAT-019 | API-OQ-008/009; DAT-OQ-009/020; earlier OQ-017/022. S, pp. 19, 34, 49, 78. |
| BAT-OQ-010 | Needs confirmation | ACL invalidation barrier/current checks, cache dependency/race handling, source deletion removal schedule/scope, old-version/shared-index protection, concurrent rebuild/deletion fencing | BAT-005–007; incident ACL recovery | API-REC-001/API-OQ-008; DAT-RI-005–008/DAT-OQ-009–010. S, pp. 28, 34, 51, 53, 79. |
| BAT-OQ-011 | Needs confirmation | Signed envelope/canonical bytes; outbox delivery claim/ack/consumer ledger, operation namespaces/TTL, stale/future events, lost-response/resume/dedup expiry and checkpoint retention | BAT-008–009/BAT-022; BAT-IDEM/RES | API-OQ-017/019/022; DAT-OQ-012. S, pp. 17, 25, 48–55, 90. |
| BAT-OQ-012 | Needs confirmation | Run route/schema, pinned case revision, plan/tool/retry budget counting, provider/token reservation/timeouts, review-wait worker semantics, stop/timeout state and admission thresholds | BAT-010; BAT-AC-021–026 | API-OQ-006/009; DAT-OQ-011; SF-CON-004/007. S, pp. 12, 15–17, 37–42, 49, 69, 90. |
| BAT-OQ-013 | Needs confirmation | Publication/review hash/task/gate schemas, version activation, exact decision/expiry/assignment races, review SLA/timezone/routing, non-review publication trigger, case-state linkage | BAT-011–012 | API-OQ-010; DAT-OQ-013; earlier OQ-008/012–014. S, pp. 44–46, 58, 82–85. |
| BAT-OQ-014 | Needs confirmation | Corporate/class-dependent case retention, related object/shared version/cited lineage scope, tombstone eligibility/schedule, hold races, backup and partial-purge semantics | BAT-007/BAT-013/BAT-021; BAT-CLS-001 | API-OQ-021; DAT-OQ-018; earlier OQ-020/022/023. S, pp. 26, 51–53, 62, 80, 90. |
| BAT-OQ-015 | Needs confirmation | Diagnostic/audit retention calculations, archive/active inventory, audit batch/hash/canonical/continuation schema, receipts/holds, purge/export schedules, repeated/empty batch | BAT-014–015; BAT-LOG-005 | API-OQ-012/021; DAT-OQ-014; earlier OQ-019/022. S, pp. 62, 66, 90. |
| BAT-OQ-016 | Needs confirmation | Daily rollup launch/timezone/cutoff, units/currency/precision/formulas, forecast, zero usage, late corrections, attribution identity, aggregate replacement/versioning and rerun | BAT-016; BAT-AC-034/055 | API-OQ-013; DAT-OQ-014; earlier OQ-021. S, pp. 38, 65, 83, 85. |
| BAT-OQ-017 | Needs confirmation | Evaluation arguments/state/corpus integrity/result schema, statistics/confidence, missing/partial/empty case policy, resume versus new run, model budget, release linkage | BAT-017; BAT-AC-035–036/056 | API-OQ-013; DAT-OQ-017; earlier OQ-021. S, pp. 74–76, 88–89. |
| BAT-OQ-018 | Needs confirmation | Provisioning/backfill launch/roles/configuration/step order, idempotency and compensation, historic window/ID/receipt/schema, poison coverage and readiness threshold | BAT-018–019 | API-OQ-016; DAT-OQ-018/020; earlier OQ-016/024. S, p. 78. |
| BAT-OQ-019 | Needs confirmation | Export/delete tenant/workspace extent and independent proof/actors, lifecycle inventory freeze/races, package/checksum/status/download, holds/shared data/backups, partial/empty/held-only completion | BAT-020–021; BAT-AC-039–041/054–055 | API-OQ-015; DAT-OQ-018; SF-CON-010/API-CNS-008. S, pp. 78–83, 87–89. |
| BAT-OQ-020 | Needs confirmation | Operator replay role/reason/scope/window, dry-run transport, bounded outbox versus dead-letter interface, migration provenance, partial replay and post-recovery verification | BAT-022; incident runbooks | API-OQ-019; DAT-OQ-012; earlier OQ-024. S, pp. 50, 79, 90 F.1. |
| BAT-OQ-021 | Needs confirmation | Migration/pipeline platform and graph, batch selector/commit/checkpoint, replica drain and canary thresholds/duration, sign-off proof, supported compensation, repeated release | BAT-023/BAT-026 | API-OQ-020/022; DAT-OQ-019; earlier OQ-024. S, pp. 52, 55, 71–73, 88–89. |
| BAT-OQ-022 | Needs confirmation | Optional webhook recipient/method/subscription/payload, signatures/canonical bytes/age/key rotation, ack/retry/dead-letter and manual replay | BAT-024 | API-OQ-024; DAT-OQ-022; earlier OQ-024. S, p. 55. |
| BAT-OQ-023 | Needs confirmation | Backup/restore provider/retention/consistent inventory/order/roles/frequency and worker recovery; key/secret rotation platform/app boundary, policy/throughput/isolation/verification | BAT-025; rotation boundary | API-OQ-021; DAT-OQ-015/020; earlier OQ-022. S, pp. 10, 19, 21, 63, 69–70, 90. |
| BAT-OQ-024 | Needs confirmation | Material-classification provenance/storage/transport, unclassified-material handling, policy activation and per-class routing/redaction/retention/approval maps; aggregation itself already Confirmed | BAT-CLS-001; BAT-010/011/013; BAT-AC-027 | [API-CLS-001](02_api.md#api-cls-001), API-OQ-026/API-AC-034; DAT-CLS-001/DAT-OQ-016/DAT-AC-023. S, pp. 62, 90. |
| BAT-OQ-025 | Needs confirmation | Metrics/alert formulas and thresholds, ticket owner configuration without assigning one here, page routing, safe log/job evidence schema, progress/completion notifications and channels | BAT-LOG; monitoring; incident procedures; undefined Notification jobs | API-OQ-018/025; DAT-OQ-014/021; earlier OQ-025/027. S, pp. 58–59, 64–66, 73, 79, 90. |

### Dependencies and Required Carry-Forward

| Specification dependency | Required carry-forward |
|---|---|
| [01_screen_functions.md](01_screen_functions.md) | Preserve `SCR-` IDs and confirmed UI status/progress/source-inspection rules. Job existence does not establish a new screen, launch control, polling schedule, cancel/retry button, or notification channel. Earlier proposed arrangements remain Proposals. |
| [02_api.md](02_api.md) | Preserve API IDs, HTTP methods/paths/statuses, exact literal codes, idempotency/revision semantics, internal-versus-public boundaries, and unresolved receipt/status schemas. No batch endpoint is added here. |
| [03_data.md](03_data.md) | Preserve DAT IDs, authoritative/source/derivative separation, complete domain information, immutable versions and decision lineage, tenant predicates, current ACL checks, checkpoints/outbox, and unresolved physical schema/hash/retention choices. |
| Detailed Processing Specification | **To be defined in a later stage.** Complete remaining domain algorithms, state guards, classification correction, budget counting, review/gate linkage, quality/statistical formulas, and lifecycle eligibility without changing confirmed batch behavior. |
| Exception Handling Specification | **To be defined in a later stage.** Complete safe codes/status/details, retry classification, lost-response/heartbeat recovery, expired cursor/dedup handling, partial/empty job outcomes, quarantine, stale review, and held-data completion. |
| Architecture/Security Specifications | **To be defined in a later stage.** Resolve scheduler/queue/identity/provider/region topology, locking/fencing and physical transactions, signed transport, key isolation/rotation, corporate retention, backup consistency, monitoring, and operational access. |
| Stage 8 consolidation | `08_architecture_decision.md` is **To be defined in a later stage**. Consolidate only completed Markdown specifications and link unresolved decisions to `04_batch_functions.md`, affected `BAT-` IDs, and the earlier filenames/requirement IDs. Do not presume an owner, date, approval, or selected implementation. |

**Implementation boundary:** Implement and test the Confirmed worker, batch, event, and recovery obligations. Unresolved schedules, schemas, thresholds, concurrency controls, hashes, roles, status/receipt semantics, and lifecycle choices remain explicit blocking decisions. Repeated reference values, illustrative APIs, or analytical job grouping do not constitute implementation approval.
