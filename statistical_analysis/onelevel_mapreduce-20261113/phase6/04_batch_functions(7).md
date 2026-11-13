# 4. Batch Function Specification

## Batch Inventory and Triggers

### Baseline and specification status

`04_batch_functions.md` specifies OrionDesk AI, `OD-AI-DDS-001`, release `R1.0`, design revision `1.3`. **Confirmed** means confirmed behavior of the fictional reference design, not deployed operational evidence. The source states: “All numbers are design assumptions, not measured production performance.” Source: `1794325316-OrionDesk_AI_Detailed_Design_Specification.pdf`, pp.1–2 [batch_functions:r1:c1:f1–f4; batch_functions:r1:c2:f1]. All page citations below refer to that exact filename.

BAT identifiers are assigned here to logical processing functions, not claimed source identifiers, queue names or independently deployed workers. Related identifiers retain their meanings in [02_api.md](02_api.md) and [03_data.md](03_data.md); [01_screen_functions.md](01_screen_functions.md) remains the presentation dependency. These earlier files are references, not independent evidence. **Needs confirmation** is an unresolved requirement, not permission to select defaults. No proposals are approved.

The source confirms asynchronous workers, extraction/indexing/runs, retention jobs and operational bulk procedures. A logical function may be a stage of another workflow. Event-driven work, manually requested asynchronous operations, scheduled purge, aggregation and engineering procedures are distinguished below. Contents entries and logical figures do not define executable job graphs. (pp.2–6, 15, 48 [batch_functions:r1:c2:f2–f7; batch_functions:r1:c6:f1; batch_functions:r1:c16:f1]).

**Out of scope:** Physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing, agent administrative cloud permissions and application-hosted GPU inference. Cross-region active/active mutation, OCR beyond English and customer-managed model weights are deferred. These exclusions do not exclude ordinary authorized enterprise-knowledge processing. (pp.9–10, 19 [batch_functions:r1:c4:f6,f10; batch_functions:r1:c7:f4]).

### Inventory conventions

For **every row**, execution cadence, scheduler product, cron, scheduler timezone, simultaneous-launch policy and complete worker identity are **Needs confirmation** unless explicitly stated. UTC applies to durable event time, not an invented scheduler. Workspace timezone applies to business-calendar deadlines; UI presents labeled workspace-local time. (pp.25, 48, 59 [batch_functions:r1:c9:f10; batch_functions:r1:c16:f2; batch_functions:r1:c19:f9]).

“Manual NC” means manual execution permission/interface is not supplied; it does not establish an operator action. Requester scope is not the executing service identity. Dependencies below are supported logical producer/consumer relationships, not a requirement for separate deployment units.

| ID / logical function | Purpose and executor | Trigger / manual execution | Predecessor → successor and prerequisites | API / data references; source |
|---|---|---|---|---|
| BAT-001 Case classification | Attach policy-aware labels, confidences, provenance; classifier/Triage responsibility; exact worker NC | `CaseCreated`; manual correction needs reason code, correction transport NC | Authorized NEW case/business context/attachments → classification data; later drafting may use Triage | API-001/046; DAT-004/025; pp.12,40,87 [c5:f4; c14:f2; c28:f1] |
| BAT-002 Incremental connector sync | Preserve repository identities, ACL/history; Connector workers | Admin `POST /v1/connectors/{connectorId}/sync`, `202`; automatic frequency NC | Complete provisioning/credential references/capability discovery → BAT-003 and source-change BAT-006 | API-018/019/050; DAT-006/016/025; pp.27–29,78,83 [c10:f1–f12; c25:f2; c26:f11] |
| BAT-003 Document ingestion and extraction | Scan, extract, normalize immutable artifacts; Ingestion Service, extraction workers | Analyst attachment POST `202`; accepted connector documents; manual OCR/reprocess launch NC | Allowed validated source → scan → parse/normalize → `DocumentNormalized` → BAT-004 | API-006/007; DAT-006–008; pp.16,19,30–32,83,87 [c6:f7; c7:f4; c11:f1–f11; c26:f7; c28:f2] |
| BAT-004 Embedding/index build and rebuild | Search derivatives and checked alias generation; Indexer/embedding workers | `DocumentNormalized` builds index; rebuild launch/manual NC | Immutable normalized version → index commit → BAT-006; source database authoritative | API-046; DAT-008/025/030; pp.19,34,87 [c7:f4; c12:f2–f3; c28:f2–f3] |
| BAT-005 Index reconciliation | Repair failed writes and broken message links; reconciliation worker | Failed index writes/link discrepancies; scan cadence/manual NC | Accepted durable sources/outbox → repaired derivative/link and verified coverage | API-046, API-038 recovery dependency; DAT-006–008/015; p.49 [c16:f8] |
| BAT-006 Source ACL/delete and cache invalidation | Tombstone deletes, remove index derivatives, revoke affected cache | Source delete/ACL revision; `SearchIndexCommitted` invalidates query cache; manual NC | BAT-002/004 changes → current-permission retrieval and publication; eligible final removal BAT-013 | API-046/050; DAT-006/011/030; pp.28,53,87 [c10:f8; c17:f11; c28:f3] |
| BAT-007 Bounded grounded AI run | Orchestrator manages Triage/Research/Draft, retrieval, gateway and deterministic policy | Analyst case-run POST `202`; `AgentPlanApproved` dispatches steps; `WorkflowStageAdvanced` resumes consumers | Authorized case/admission/plan/evidence → candidate/policy → BAT-008/009 as applicable | API-011–015/036/037/046–048/051; DAT-009–011/017/018; pp.37–42,49,83,87 [c13:f1–f8; c14:f1–f11; c16:f7; c26:f8; c28:f4,f6] |
| BAT-008 Review expiry, reassignment/escalation | Policy-defined task lifecycle; expiry executor NC | Configured SLA expires; manual expiry/reassign transport NC | Eligible pool/minimum role/duties and reviewed hash → reassignment/escalation record, never approval | API-016/017/046; DAT-012/028; pp.45,82,89 [c15:f6; c26:f5; c30:f9] |
| BAT-009 Publication validation | Revalidate supported exact artifact/current policy/ACL and commit gate/pointer; Policy Service event producer, gate executor NC | `ApprovalDecisionRecorded` → validate publication; AUTO_ALLOW route NC | Candidate/evidence/current authorization/satisfied approval → published matching pointer or rejection | API-017/046; DAT-004/011–013/018; pp.45–46,87 [c15:f7–f10,f14; c28:f5] |
| BAT-010 Outbox delivery, consumer continuation and denial enrichment | At-least-once publication/dispatch/resumption/enrichment; producer-specific services, consumer identities NC | Committed outbox/domain events; `AccessDenied` enriches alerts; polling cadence/manual NC | Committed state/outbox → scoped deduplicated consumer action | API-046; DAT-014/015/029/034; pp.17,48–50,87 [c6:f12; c16:f1–f6; c28:f7] |
| BAT-011 Validated replay and delayed-index recovery | Bounded operator-controlled recovery | Operator `POST /internal/deadletters/{id}/replay`; reason/dry-run/scope required; delayed-index runbook replay endpoint mapping NC | Validated original records/contained fault → BAT-004/005/010; fingerprint and denied probes before incident closure | API-038/046; DAT-015/029/030; pp.50,90 [c16:f5,f11; c31:f6–f11] |
| BAT-012 Closed-case retention | Select eligible closed cases, preserve holds/approved lineage; actor NC | Retention job; cadence/manual NC | Closure snapshots → eligible retention action/BAT-013; not all cases | API-005/040; DAT-004/005/019/031; p.26 [c9:f1–f2] |
| BAT-013 Tombstone final purge and workspace deletion | Remove eligible objects/index, retain held records/receipts; Retention Worker produces verification event | Scheduled tombstone pipeline, cadence NC; Admin+approver workspace delete `202`; internal purge launch scope NC | Authorized checks/hold inventory/tombstones → receipts; `TenantDeletionVerified` closes purge record | API-025/030/040/046; DAT-019/031; pp.51–53,78–83,87,89 [c17:f3–f4; c25:f1,f7; c26:f16; c28:f8; c30:f12] |
| BAT-014 Controlled export | Checksummed authorized package; executor NC | Admin+approver workspace export `202`, two independent checks | Approved scope/second person → manifest/package; no required deletion successor | API-024; DAT-026/031/033; pp.79–83,88 [c25:f1,f6; c26:f15; c29:f11] |
| BAT-015 Provisioning and historic onboarding | Idempotent policy/key/roles/quota/stub provisioning and bounded historical ingestion; executor NC | Onboarding; launch/manual contract NC | Provisioning complete → BAT-002; bounded history → BAT-003–005 and reconciliation receipts | No confirmed provisioning/backfill endpoint; DAT-003/026/030; p.78 [c25:f2–f3] |
| BAT-016 Optional webhook delivery | Signed outbound delivery/retries; executor NC | Optional subscribed outbound events; subscription administration/manual retry NC | Accepted case transition/outbox → external delivery without business rollback | API-049; DAT-029/033; pp.52,55 [c17:f7; c18:f7] |
| BAT-017 Audit-chain export | Append-only batch-hash chaining/independent retention; executor NC | Audit entries; export cadence/manual NC | Immutable audit lineage → independently controlled retained export | API-020 read dependency; DAT-014/026/031; p.62 [c20:f9] |
| BAT-018 Usage attribution and daily rollups | Workspace/deployment cost aggregation; executor NC | Invocation/embedding/storage/index usage; daily reporting granularity, execution cadence NC | Attributed usage → budget/forecast/rejected excess rollups | API-021/041; DAT-017/026; p.65 [c21:f7] |
| BAT-019 Diagnostic/audit expiration processing | Distinct retention policies and hold receipts; executor NC | Default diagnostic TTL 30 days; fictional audit policy seven years; execution cadence/manual NC | Eligible retention inventory → purge receipts/held exceptions; link BAT-013 subject to scope clarification | API-040 dependency; DAT-019/031; p.66 [c21:f8] |
| BAT-020 Credential/key lifecycle | Automatic service credential rotation; policy encryption-key rotation; managed identities/vault | Automatic/defined policy; interval/manual NC; Operator revocation is confirmed | Vault-scoped references → rotated credential/key lineage; revoked connector jobs fail safely | API-045/050 dependencies; DAT-026/031; pp.21,27,63 [c8:f3; c10:f6; c20:f10] |
| BAT-021 Frozen benchmark evaluation | Evaluation harness; worker NC | Admin evaluation POST `202`; prompt/model changes require reevaluation, automation NC | Frozen synthetic corpus/approved adapters → scorecard/release gate evidence | API-022/023; DAT-026/036; pp.74–76,83 [c24:f1–f12; c26:f14] |
| BAT-022 Migration, release and test pipeline procedure | CI/build and Security/SRE-gated promotion; bounded backfill | Engineering release/change pipeline; POST internal release exists, scopes NC; not periodic production batch | Compatible migrations/tests/signed artifacts → canary → reader drain/enforcement or traffic rollback | API-043/044; DAT-032/036; pp.52,71–73,89 [c17:f8; c23:f1–f11; c30:f18–f19] |
| BAT-023 Backup/restore and resilience procedure | Continuous PostgreSQL backup; incident-command recovery; exact executor NC | Continuous backups; manual incident-command secondary restore; drill cadence NC | Primary/warm recovery snapshots/object versions/index recipes → verified consistent recovery | DAT-032; pp.19,69–70 [c7:f5; c22:f9–f10] |

In table citations, `cN:fM` abbreviates the exact finding prefix `batch_functions:r1:cN:fM`. It does not abbreviate or change the source filename/page location.

## Processing by Job

### Shared argument and field rules

For **each BAT function**, unspecified argument spelling, type, length, requiredness, enum, default, unknown-field behavior and output schema remain **Needs confirmation**, separately for every field. Path placeholders identify resources but unavailable IDL prevents assuming all REST IDs are UUIDv7. Selected database fields are update/lineage targets, not complete wire schemas. No invented scheduler arguments, locks or physical job tables are approved. Repository-generated OpenAPI/protobuf governs final interfaces. (pp.55,82,85–86 [batch_functions:r1:c18:f9; batch_functions:r1:c26:f1; batch_functions:r1:c27:f1–f13]).

All durable changes preserve `tenant_id`, `revision`, `actor_id`, `occurred_at` and correlation context. Events contain exactly supplied envelope names `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, `payload`, using canonical JSON and UTC; complete types/signing/canonicalization are NC. Signed job tenancy is immutable and cannot be replaced by payload instructions. (pp.22,48 [batch_functions:r1:c8:f10; batch_functions:r1:c16:f2–f3]).

### BAT-001 Classification

1. Consume `CaseCreated` from Case Service with selected payload labels `Case ID / revision`; deduplicate before accepted effects.
2. Resolve authorized current case and policy context. Case starts `NEW`; business context and attachments precede the described classification journey. Their exact readiness requirements are NC.
3. Attach labels, confidences and provenance. Store user label correction separately with reason code; correction role/catalog/transport and reclassification triggers are NC.
4. Completion requires the classification data/provenance to be attached without duplicate business effect. Classifier algorithm, confidence scales, case-state change and no-input result are NC. Triage classification within BAT-007 is a supported responsibility; whether it shares this worker is NC.

Targets: DAT-004 `cases`, DAT-025 logical classification fields; API-001/046. Sources: pp.12,40,87 [batch_functions:r1:c5:f4; batch_functions:r1:c14:f2; batch_functions:r1:c28:f1].

### BAT-002 Incremental sync

1. Validate authorized Admin launch and complete provisioning before work allocation. Resolve `connectorId`, tenant/workspace, provider capability and workspace-vault credential reference.
2. Discover list/fetch/delta cursor/ACL/delete support. Unsupported capabilities cause lower-trust ingestion and explicit user warning, not silent assumption or an invented universal rejection.
3. Preserve source IDs, permissions/history and provider cursor/high-watermark/error ledger. Select incremental items using provider capability; concrete delta comparisons/order are NC.
4. Fetch/ingest under workspace quota/fair scheduling. Honor provider `Retry-After` and exponential backoff/jitter.
5. Advance cursor only once **all preceding items have durable ingestion outcomes**. The source does not require downstream indexing to finish before this advance.
6. After bounded retries, malformed items quarantine with reason code, correlation ID and remediation path. Remaining batch **may proceed** while cursor ledger records exception. Do not report all-items success or impose whole-batch rollback. Continuation choice policy and partial-completion status are NC.
7. Revoked credentials make queued jobs fail `CONNECTOR_REAUTH_REQUIRED`, without tokens. Success/completion schema, empty delta outcome, simultaneous sync arbitration and reauthorization transport are NC.

Targets: DAT-016 `connector_cursors.connector_id,cursor,watermark,retry_state`; source records DAT-006; exact mapping to high-watermark/error ledger is NC. API-018/019/050. Sources: pp.27–29,78,83 [batch_functions:r1:c10:f1–f12; batch_functions:r1:c25:f2; batch_functions:r1:c26:f11; batch_functions:r1:c27:f7].

### BAT-003 Ingestion/extraction

1. Validate PDF, DOCX, HTML or UTF-8 text, signature/extension agreement, configurable **25 MB per file** and decompression protection before long-running allocation. MB byte convention, decompression threshold and file-count limits are NC.
2. Scan before parser; disable macros and embedded remote fetch. Unsafe files quarantine and never enter the index.
3. PDF segmentation retains page index/bbox blocks, table row/column annotations, headings and reading order. OCR fallback is opt-in and provenance-marked; actor/flag/default are NC; OCR beyond English is deferred.
4. Strip transport artifacts without rewriting source claims. Content fingerprint plus pipeline version produces immutable derivative IDs, supporting side-by-side reprocessing, not overwriting cited history.
5. Retain source URI, file hash, page and optional bbox. Capture empty-page ratio, unknown-character ratio, table-loss indicators and language confidence; thresholds/scales/coordinates/hash algorithms are NC.
6. Low-quality permitted content remains viewable but is excluded from autonomous recommendations. This is not the unsafe-quarantine rule.
7. Persist version/content/anchor lineage and publish `DocumentNormalized` for BAT-004. A `202` acknowledgement is not READY or completed indexing. Document catalog: `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED`; exact edges and terminal quality branch are NC.

Targets: DAT-006–008 `documents`, immutable `document_versions(document_id,hash,parser_version,object_key)`, `chunks(id,document_version_id,page,bbox,text_hash)`. Artifact formats/keys/version identity are incomplete. API-006/007. Sources: pp.30–32,82–83,85,87 [batch_functions:r1:c11:f1–f11; batch_functions:r1:c26:f4,f7; batch_functions:r1:c27:f3; batch_functions:r1:c28:f2].

### BAT-004–006 Indexing, reconciliation and permission changes

| Function | Input selection and ordered transformation | Update targets / output and completion condition |
|---|---|---|
| BAT-004 | `DocumentNormalized`: `Version ID / source hash`; build scoped keyword/vector derivative. Store tenant/workspace/version/chunk, language/classification, **1536-dimensional embedding**, normalized keyword text. Rebuild creates parallel index; evaluate completeness/recall before atomic read-alias switch. | Nonauthoritative index, DAT-025 alias/generation; `SearchIndexCommitted` from Indexer with `Index generation / document revision` → cache invalidation. Numerical gates, rebuild snapshot/race rules, retirement and empty-index outcome NC. |
| BAT-005 | Compare accepted source fingerprints to derivatives after index write failure; retry missing/failed derivative writes. Repair broken message links from outbox ledger. | DAT-006–008 accepted data remains durable; DAT-015 links/index repaired. Completion requires consistency verification; scan interval, discrepancy selection/schema and report format NC. |
| BAT-006 | Source delete → tombstone and scheduled index removal. ACL change → purge affected retrieval cache before serving new results. Index commit → invalidate query cache. Cache identity uses tenant/user-scope digest/source ACL revision/query hash/index generation. | DAT-006 tombstones and versioned cache/index. Revocation effective before **next retrieval**; stale visibility is security incident. Soft-deleted content unretrievable; publication rechecks current permission. Physical atomicity/TTL and exact delete scope NC. |

Sources: pp.27–28,34,49,51–53,78,87 [batch_functions:r1:c10:f1,f8; batch_functions:r1:c12:f2–f3; batch_functions:r1:c16:f8; batch_functions:r1:c17:f3,f11; batch_functions:r1:c25:f3; batch_functions:r1:c28:f2–f3]. Search readiness is **index coverage**, not queue emptiness; no numeric coverage threshold is supplied.

### BAT-007 Grounded run and gateway stages

1. Authorize Analyst `POST /v1/cases/{caseId}/runs`; validate input and admission before allocation. Return `202` persisted workflow, not approved result. `POST /v1/runs` is also source-confirmed but its relationship is NC; do not treat it as an approved alias.
2. Admit only when workspace tokens, queue age and provider capacity satisfy thresholds. Throttle with `429` and `Retry-After`; saved cases remain available.
3. Persist plan revision before effects. DAG depth is at most **eight**, maximum **sixteen tool invocations**, explicit dependencies and replayable checkpoints. Persist each stage checkpoint before downstream dispatch.
4. Triage classifies; Research requests grounded evidence; Draft constructs candidate; Policy Evaluator is deterministic. Retrieval/generation/policy/reviewer decisions remain separate records.
5. Retrieval applies current ACL before model release, forms lexical/normalized vector queries, bounded candidates, reciprocal rank fusion, deterministic reranking, diversity and token budget. Evidence outputs include chunk ID/source title/document revision/page anchor/ACL digest; opaque citations verify before display. Insufficient support yields `NO_SUPPORTED_EVIDENCE`; clarification or human routing is permitted, branch NC.
6. Gateway selects workspace-approved deployment by capability/region/data-handling/context/cost/evaluation approval. Reserve input/output tokens and attribute provider usage. Quota exhaustion is terminal for the run, without automatic model/data-class change.
7. Construct distinct fixed system rules, signed workflow instruction, validated user input and delimited untrusted passages. Strip evidence tool-call directives, record injection indicators. Likely personal-data tags and policy-permitted redaction precede provider invocation. Model text never grants authority.
8. Validate versioned JSON with bounded parsing retries. Unknown fields, invalid citations and control-character injection trigger `MODEL_OUTPUT_INVALID`; no publication. Never fabricate support or represent partial processing as approved.
9. MCP tools are approved/schema-pinned with validated arguments and separately authorized effects; consequential writes also require human authorization/idempotency. Discovery grants no authority; denied effect cannot use equivalent tool. A2A carries task/capability/input-output schemas/deadline/trace and receiver may decline.
10. Evaluate normalized sensitivity/action/evidence quality/model class/financial impact/confidence with retained rule version. Results: `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY`; model tags cannot override. High-impact recommendations become review tasks.
11. Continue according to confirmed checkpoints and resolved policy path. Run states are `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED`. Missing approval, exhausted calls, repeated invalid plans, policy denial and deadline expiry are termination triggers with exact failed checkpoint reporting. **BAT-OQ-004:** missing-approval timing, recoverable timeout state, review expiry/run consequence and AUTO_ALLOW edge are unresolved; do not implement immediate missing-approval failure or implicit approval.

Targets: DAT-009 `runs(id,case_id,status,plan_revision,budget)`; DAT-010 `run_steps(id,run_id,step_kind,status,checkpoint)`; DAT-011 evidence; DAT-017 `token_ledger(run_id,deployment_id,in_tokens,out_tokens)`; DAT-018 `policy_evaluations(run_id,rule_version,input_digest,result)`. Normalized inputs must be retained; digest alone does not replace them. Sources: pp.12,37–45,49,69,82–85,87 [batch_functions:r1:c5:f5,f7–f8; batch_functions:r1:c12:f1,f6–f10; batch_functions:r1:c13:f1–f8; batch_functions:r1:c14:f1–f11; batch_functions:r1:c15:f1–f3; batch_functions:r1:c16:f7; batch_functions:r1:c22:f6; batch_functions:r1:c26:f3,f8; batch_functions:r1:c27:f4–f5,f8].

`knowledge.search@v1` input is `{query: string, case_id: uuid, max_items: int<=10}`, output `{evidence_set_id: uuid, citations: Citation[]}`; tenant `read:permitted_documents`, read-only, no arbitrary URL/filesystem access. Ten is **tool-specific**, not batch size. Complete Citation/minimum/default/requiredness/transport are NC. A2A `research.grounded_search.v1` / `schema://oriondesk/research-request/1` example uses `case_demo` and deadline `2026-11-09T08:00:00Z`; neither string coercion to MCP UUID nor a production schedule is approved. (p.87 [batch_functions:r1:c28:f9–f13]; API-047/048, DAT-035).

### BAT-008–009 Review lifecycle and publication

1. Use policy reviewer pool/minimum role/separation of duties. Tasks prohibit self approval; Analyst cannot approve own high-risk recommendation. Task states: `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED`, all actor/hash/duties guarded. Exact edges are NC.
2. Review exposes exact candidate, citations, model/prompt version and policy reasons; sources must be inspectable before approval. Required fields gate Approve/Reject; field list is NC, not permission to guess.
3. Record decision, authenticated actor, timestamp, evaluated hash, rationale and optional annotations. Changed-artifact decision rejects stale and is audited without accepted mutation.
4. BAT-008 configured-SLA expiry records escalation and reassigns/escalates without approval. SLA, recipient, execution/commit unit and race arbitration with decision are NC.
5. BAT-009 consumes `ApprovalDecisionRecorded` from Policy Service, selected labels `Task / actor / content hash`, and **validates publication**, not unconditional publication. Recheck current ACL/tenant/policy/evidence/hash even if retrieval succeeded earlier.
6. Final response pointer and satisfied gate commit in the same transaction. Replay cannot publish another artifact under old approval. High-risk work cannot publish unapproved. Closure later snapshots approved artifact/cited versions/decisions.
7. Override needs elevated role, secondary reviewer and audited reason; denied rework is a new run revision, never retroactive approval. Transport and roles remain NC.

Targets: DAT-012 `approval_tasks(id,run_id,reviewer_pool,artifact_hash)`, DAT-013 immutable `approval_decisions(id,task_id,reviewer_id,decision,reason)`, DAT-004 pointer, DAT-018 gate lineage. Sources: pp.11–12,26,44–46,57–58,82,85,87,89 [batch_functions:r1:c5:f1–f2,f5; batch_functions:r1:c9:f1; batch_functions:r1:c15:f1–f10,f14; batch_functions:r1:c19:f2; batch_functions:r1:c26:f5,f10; batch_functions:r1:c27:f5; batch_functions:r1:c28:f5; batch_functions:r1:c30:f5,f9].

### BAT-010–011 Delivery and recovery

BAT-010 processes canonical scoped envelopes and producer-specific actions: `CaseCreated` classification; `DocumentNormalized` build index; `SearchIndexCommitted` invalidate query cache; `AgentPlanApproved` dispatch steps; `ApprovalDecisionRecorded` validate publication; `WorkflowStageAdvanced` resume consumers; `AccessDenied` alert enrichment; `TenantDeletionVerified` close purge record. Selected payload labels are not typed JSON keys. Producers and mappings are confirmed in Appendix C. (p.87 [batch_functions:r1:c28:f1–f8]; API-046, DAT-034).

Other retained chapter event contracts are `BaselineCommitted`, `RunRequested`, `DeploymentPromoted`, `CaseStateChanged`, `ConnectorSyncStarted`, `ModelInvocationCompleted`, `DataRetentionPurgeCommitted`, `ApiCompatibilityVerified`, `UserReviewOpened`, `SecurityPolicyChanged`, `SloBurnRateDetected`, `BackpressureActivated`, `ReleasePromoted`, `EvaluationCompleted`. They require versioned envelope/outbox, guarded writes, correlated audit and ledger/revision duplicate handling; missing producer/payload/consumer effects remain NC. They are not automatically SSE types or additional jobs. (Registers pp.10–80 [batch_functions:r1:c4:f11–f14; c6:f14–f17; c7:f13–f16; c9:f11–f16; c10:f14–f17; c13:f11–f16; c17:f12–f15; c18:f11–f15; c19:f6–f14; c20:f11–f14; c21:f9–f13; c22:f12–f15; c23:f13–f16; c24:f14–f17]).

BAT-011 procedure:

1. Require authenticated authorized Operator, reason, dry-run validation and scope limit; validate before allocation. Role/argument schema and recovery API result are NC.
2. Preserve original event identity. Only schema-transforming migration may change identity with explicit provenance link.
3. For delayed indexing, **Detect → Contain → Diagnose → Recover → Verify → Document**: alert on oldest queue age/backlog; locate tenant/index generation; pause only faulty connector/indexer shard and keep accepted sources durable; inspect event ID/outbox lag/parser flags/search throttling/ACL revision; replay validated outbox through bounded operator-controlled job.
4. Compare source fingerprints/indexed versions and run denied-access probes before incident closure. Record audit IDs/time window/blast radius/quality effect/preventative action. Numeric limits, no-record replay outcome and partial replay handling are NC.

Sources: pp.50,90 [batch_functions:r1:c16:f5,f11; batch_functions:r1:c31:f6–f11]. Targets: DAT-015 outbox, DAT-029 ledgers/checkpoints, DAT-026 incident evidence.

### BAT-012–020 Lifecycle and aggregation processing

| Function | Selection, processing and targets | Output / completion and unresolved conditions |
|---|---|---|
| BAT-012 | Only eligible **closed cases** under workspace retention policy, after snapshot of approved answer/cited versions/reviewer decisions; preserve immutable approved lineage and legal holds. DAT-004/005/007/013/031. | Eligibility beyond CLOSED, retention class/duration, disposal scope and no-input outcome NC. Immutability is not indefinite retention. p.26 [c9:f1–f3]. |
| BAT-013 | Verify two independent workspace-delete checks; enforce legal hold, tombstone, remove eligible blobs/index and record completion receipts. Soft-deleted entities already cannot be retrieved. Shared subject-request inventory is supported, not a new endpoint. | Protected records retained/receipted; `TenantDeletionVerified` from Retention Worker with `Manifest ID / receipt hash` closes purge record. DAT-019 `tenant_id,object_ref,purge_time,actor`. Partial-held completion status, removal ordering/checksum and scheduled cadence NC. pp.51,78–83,85,87,89 [c17:f3; c25:f1,f7; c26:f16; c27:f9; c28:f8; c30:f12]. |
| BAT-014 | Two-person authorized export packages case metadata/approved artifacts/source references/audit manifests with checksums. Exclude secrets/internal model prompts. | Controlled manifest/package; DAT-026/031. Scope/read consistency, archive/schema/checksum/download/expiry/no-input outcome NC. Single Admin export must fail. pp.79–83,88 [c25:f1,f6; c26:f15; c29:f11]. |
| BAT-015 | Provision workspace policy/encryption refs/role bindings/quotas/connector stubs in one idempotent workflow. Incomplete status visible, sync blocked. Historic ingestion uses bounded windows/stable source IDs/per-batch reconciliation receipts. | Readiness requires index coverage, not empty queue. One workflow does not establish one ACID transaction. Launch API/window bounds/receipt/schema/state/commit units NC. DAT-003/026/030; p.78 [c25:f2–f3]. |
| BAT-016 | Signed optional subscribed event delivery; recipient verifies signature/age, retry with exponential backoff. | Failure never rolls back case transition; delivery status/age/signing/terminal retry notification NC. DAT-033; pp.52,55 [c17:f7; c18:f7]. |
| BAT-017 | Append-only audit entries chained by batch hashes and exported independently; Operators cannot alter historic review decisions. | Retained integrity lineage; batch window/algorithm/destination/format/receipt/confirmation NC. DAT-014 `id,tenant_id,actor_id,action,digest`; p.62,85 [c20:f9; c27:f6]. |
| BAT-018 | Attribute model/embedding/storage/index usage by workspace cost center and deployment version; produce daily budget/forecast/rejected excess rollups. DAT-017/026. | API-021 costs/quotas/trends. Formula/currency/window timezone/late corrections/rerun settlement/empty period NC; daily is not execution schedule. pp.65,83 [c21:f7; c26:f13]. |
| BAT-019 | Distinct default diagnostic TTL **30 days**, fictional security audit **seven years**, legal-hold exceptions. | Purge completion receipts; corporate retention selection/overrides/eligibility/disposal cadence NC. DAT-019/031; p.66 [c21:f8]. |
| BAT-020 | Automatic service credentials rotate; policy encryption keys rotate through managed-identity vault refs without request-path bulk reencryption. Connector revocation fails queued jobs safely. | Interval/key-version concurrency/recovery/receipt NC; do not invent off-path bulk reencryption. Isolation-versus-rotation throughput must be decided before enterprise GA. pp.10,21,27,63 [c4:f10; c8:f3; c10:f6; c20:f10]. |

### BAT-021 Evaluation

1. Authorize Admin POST `202`; freeze/version/independently review corpus and signed fixture manifest. Use **1,200 synthetic permission-controlled cases** spanning retrieval/refusal/ambiguity/adversarial evidence, each with expected citation sets/outcomes.
2. Preserve deterministic contract/security tests independently of probabilistic scoring; no live model dependency for deterministic state/idempotency/ACL/hash/retry/schema tests; pin provider adapters.
3. Produce citation precision **>=0.97**, unsupported-claim rate **<=0.02**, frozen high-risk policy recall **1.00**, confidence intervals and distribution shift by domain. Formula/denominator/CI method and low-confidence cutoff NC.
4. Prompt/model change requires reevaluation. Low confidence blocks release, and critical isolation/approval tests have **zero exceptions** regardless of benchmark score.
5. Retain scorecard/result lineage and `EvaluationCompleted`; exact result states/no-input/partial-case failure handling/runtime limits are NC. Corpus fixtures include empty/mixed/adversarial/malformed cases; they do not define empty evaluation success.

API-022/023; DAT-026/036. Sources: pp.74–76,83,88–89 [batch_functions:r1:c24:f1–f12; batch_functions:r1:c26:f14; batch_functions:r1:c29:f12–f13; batch_functions:r1:c30:f16–f19].

### BAT-022–023 Engineering and recovery procedures

BAT-022 procedure:

1. Use source-controlled nonsecret defaults/signed environment config/vault references. Terraform or Bicep remain alternatives.
2. CI runs static analysis/dependency scans/unit/contract tests, generates SBOM and signs images; production allows only verified allowed-build digests.
3. Expand-contract migration adds nullable columns, performs bounded backfill, then enforces constraints after old replicas drain. Active-reader fields cannot be removed. Selection/batch/checkpoint values are NC.
4. Canary compares latency/errors/authorization denials/AI-quality regression against baseline; regression triggers traffic rollback, **not database down-migration**. Binary reverses first; data compensation only explicitly supported. Document new-write readability.
5. Security/SRE validate egress/secrets/backups/alerts before promotion. Bind image digest/schemas/prompts/model-routing policy; preserve reconstructible binary/prompt/policy.
6. Minimum pack includes unit/schema evolution/negative authorization/replay/staging connector sync/accessibility/search recall/grounding/policy recall/load/DR drills. Signed outputs reference release digest.

Sources: pp.20,52,71–73,89 [batch_functions:r1:c7:f7; c17:f8; c23:f1–f11; c30:f18–f19].

BAT-023 uses continuous PostgreSQL backups and primary writes with one warm recovery region. Secondary snapshots restore only under incident command. Reference **RPO <=15 minutes**, **RTO <=4 hours**; object versions/index rebuild recipes tested together with relational consistency. Exercise 429 storms/lost heartbeats/duplicate events/object access failures/primary outage and measure safety/recovery. Backup retention, snapshot selection, restore ordering/actor, heartbeat interval/lease and drill cadence are NC. (pp.19,69–70 [batch_functions:r1:c7:f5; batch_functions:r1:c22:f9–f10]).

## Operations and Recovery

### Authorization, transaction and concurrency controls

1. Bind authenticated principal and immutable tenant to every launch/step/replay. Authorization combines role, workspace membership, sensitivity, source ACL, requested action and duties. Resource guards run inside transactions; hidden UI is not enforcement. Map Workspace Admin/Admin, Owner, Member, approver and Operators before grants. (pp.11,21–23,83 [batch_functions:r1:c5:f2; c8:f1–f11; c26:f6–f16]; API-045, DAT-027).
2. Use transaction-scoped RLS/storage tenant predicates. Reference cases policy is `tenant_id = current_setting('app.tenant_id')::UUID`; reset pooled scoped variables after **every transaction**, including failures. Add production workspace-tenancy enforcement via FK or controlled writes; choice NC. (pp.51,86 [batch_functions:r1:c17:f1; c27:f10,f12–f13]).
3. Validate payload before allocation/transaction, domain invariants and tool dispatch. If dependency unavailable, return documented retryable error or persisted asynchronous identifier, never ambiguous success. Exact per-interface branch remains NC when source lacks status/schema. (pp.11–13,54–56 [batch_functions:r1:c5:f3; c18:f10]).
4. Case mutations, decisions and outbox inserts share one ACID commit; final pointer/gate commits together. Index/webhook effects are asynchronous with explicit reconciliation; state-changing workflow uses outbox or explicitly reconciled saga. No distributed all-store transaction or generic compensation is approved. (pp.17,45,52 [batch_functions:r1:c6:f12; c15:f9; c17:f7]).
5. Concurrent launches: enforce confirmed revision/hash/idempotency predicates. Case `If-Match` conflict returns `409 CASE_VERSION_CONFLICT` with current revision; no automatic stale-edit merge/retry. Job-creating POSTs require `Idempotency-Key`; identical payload returns original operation, changed fingerprint `409 IDEMPOTENCY_CONFLICT`. Actor/fingerprint outcome lasts **24 hours**. Lock/lease/atomic same-key arbitration, post-expiry handling and key scope are NC. (pp.25,54,84,89 [batch_functions:r1:c9:f8; c18:f3; c26:f17; c30:f1]).
6. At-least-once consumers check event ID/operation identity and aggregate revision, record duplicate outcome and do not reapply accepted mutation. Detect stale revisions; do not depend on partition ordering. Ledger physical schema/retention and stale-event result are NC. The 24-hour launch outcome is not universal event retention. (pp.17,48–50 [batch_functions:r1:c6:f12,f15; c16:f6,f15]).
7. Specific commit units are only those above, checkpoint-before-dispatch and sync durable-item/cursor requirements. All other item/batch sizes, mutual exclusion, leases, simultaneous rebuild/export/delete arbitration and compensation remain **BAT-OQ-003**, not implementation discretion.

### Retry, timeout and failure behavior

Transient failures: bounded exponential backoff, randomized jitter and per-dependency circuit breakers. Validation/permission faults are permanent, not retried. Mutable retry requires idempotency; consequential effects require human authorization. Honor connector provider `Retry-After` and fair workspace quotas. Numeric caps/backoff/timeout/thresholds are **BAT-OQ-005**. (pp.28,42,49 [batch_functions:r1:c10:f11; c14:f11; c16:f10]).

Reruns preserve accepted business effects and immutable versions. Reprocessing changed pipeline versions may coexist side by side; denied drafts rework as new run revisions. Accepted metadata survives failed indexing; webhook failure cannot roll back case. Poison sync quarantine may permit ledger-recorded remaining-batch continuation. Held-record purge retains/receipts exceptions. No generic whole-batch rollback is authorized. (pp.29,31,46,49,55,89 [batch_functions:r1:c10:f12; c11:f6; c15:f10; c16:f8; c18:f7; c30:f12]).

Missing approval/deadline/call-budget failure reports exact failed checkpoint, but review waiting/expiry and recoverable timeout semantics remain **BAT-OQ-004**. Example `run_timeout_seconds: 180` is not selected. There is no confirmed cancel endpoint, universal rerun endpoint or automatic approval bypass.

### Degradation and containment

- Provider outage disables new generation admission, retains safe manual case/evidence workflows and displays degradation. Page on-call only when availability budget is impacted. General fallback is only approved equal-or-stronger data handling; no unapproved restricted-region/deployment route. In-flight fallback details are NC. (pp.37,79 [batch_functions:r1:c13:f4; c25:f4]).
- Vector degradation may use lexical retrieval with visible reduced-quality flag. Safety/authorization never weaken under load. Suspected ACL leakage instead suspends **affected aliases**, revokes cache, preserves audit and scopes ACL replay; negative access tests must pass before reenabling. (pp.68–69,79 [batch_functions:r1:c22:f1,f7; c25:f5]).
- Delayed indexing pauses only faulty connector/indexer shard, preserves accepted sources and uses BAT-011 validation/fingerprint/denied probes. No global pause is inferred. (p.90 [batch_functions:r1:c31:f7–f10]).

### Monitoring, logging and notifications

| Area | Confirmed monitoring/output | Missing operational choice |
|---|---|---|
| Worker scaling | Extraction/embedding queue age and throughput; APIs utilization/latency | Threshold/window/min-max replicas/lease recovery NC |
| Delivery/index recovery | Oldest queue age/backlog, affected tenant/index generation, outbox lag/event ID/parser flags/throttle/ACL revision; index coverage readiness | Alert values and notification recipients/channels NC |
| Run/AI | Request/error/latency/saturation, grounding pass/retrieval empty/provider throttle/token use/approval backlog age; exact failed checkpoint | Names/units/windows/cost anomaly thresholds NC |
| User progress | Server-state/SSE monotonic scoped retained backfill via `Last-Event-ID`; refresh reconstructs stages; meaningful accessible transitions only | SSE schemas/retention/expired offsets/heartbeat NC |
| Audit/privacy | One audit record per accepted transition; safe denial traces; no documents/API secrets/full prompts/private existence in public diagnostics; default model logs digests/tokens | Audit-chain schema/denial ordering and detailed redaction policy NC |
| Notification routing | User-impacting incidents page; routine spend anomaly creates owner/threshold ticket; expiry records escalation, capability gap warns | Actual owner/threshold/channel/SLA/destination NC |

Sources: pp.19,54–59,62,64–66,90 [batch_functions:r1:c7:f4; c18:f1,f6–f7; c19:f1–f3,f8–f9; c20:f7,f9; c21:f1,f4,f6; c31:f6,f8,f11]. No new batch-admin screen or email/chat channel is confirmed.

Reference sizing: `2,000` active daily users, `60` steady/`180` burst requests/s, `100,000` documents/tenant, `20` concurrent runs/large tenant; typical `1 MB` source roughly `40–120` chunks depending on content/parser quality. These are reference assumptions, not batch commit sizes or configured client quotas. API targets `99.9%` monthly, case-create P95 under/within `300 ms`, search P95 under `1.5 s` excluding connector fetch; model latency separate. Equality/load procedure remains NC. (pp.12,65,68 [batch_functions:r1:c5:f7; c21:f5; c22:f2–f3]).

Runtime prerequisites: private datastores, separate deployment identities, scoped managed identity/mTLS/audiences/IAM, declared worker egress. Production data forbidden in development; staging synthetic/test connectors/isolated quotas. Orchestrator has no direct DB credentials. (pp.9,15–19 [batch_functions:r1:c4:f9; c6:f2,f11; c7:f1–f6]).

## Acceptance Criteria

Tests must use synthetic fixtures and unresolved thresholds must be confirmed before executable expectations depend on them. Every revised invariant requires a negative test. Critical isolation/approval failures block release with zero exceptions; do not offset them with AI quality scores. (pp.8,74,88 [batch_functions:r1:c4:f1; c24:f1; c29:f13]).

| ID / function | Procedure | Required result |
|---|---|---|
| TST-001 / launch consistency, BAT-001 | Create case twice same key/body | One case, identical response |
| TST-002 / job POST consistency | Same key, changed body | `409 IDEMPOTENCY_CONFLICT`; no second accepted outcome |
| TST-003 / all resource access | Foreign-tenant case ID | `404`-equivalent non-disclosing error |
| TST-004 / BAT-006/007/009 | Index then revoke access, query next | No forbidden evidence |
| TST-005 / BAT-007 | Force model schema failure | `MODEL_OUTPUT_INVALID`, no publish |
| TST-006 / BAT-009 | Approve wrong/prior hash | Stale rejection, audited, no accepted stale mutation |
| TST-007 / BAT-010/011 | Replay accepted outbox | Exactly one accepted business transition |
| TST-008 / BAT-002/007 | Provider 429 burst | Capped retries and controlled admission; cap NC |
| TST-009 / BAT-007/009 | Generate missing citations | Needs review or unsupported; branch NC, never approved fabrication |
| TST-010 / BAT-008 | Expire configured review task | No implicit approval; escalation recorded |
| TST-011 / screen dependency | Keyboard-only case opening | No blocked action, visible focus |
| TST-012 / BAT-023 | Reference region recovery | RPO<=15 minutes/RTO<=4 hours; relational/object/index verification |
| TST-013 / BAT-013/019 | Purge under legal hold | Protected records retained and receipted |
| TST-014 / BAT-007 | Arbitrary MCP invocation | `DENY` before dispatch |
| TST-015 / BAT-003 | Unsafe PDF | Quarantine, no indexing |
| TST-016 / BAT-022 | Regressed canary safety score | Promotion blocked |

Source: p.89 [batch_functions:r1:c30:f1–f15]; recovery values p.69 [batch_functions:r1:c22:f9].

Additional supported criteria:

1. **Success:** Authorized independent Analyst/Reviewer create→ingest→retrieve→draft→review→publish; preserve separate records/current ACL/exact hash/supported anchors and atomic pointer/gate. Inspect sources/model-prompt/policy reasons before decision. Exercise rejected new-revision rework. (pp.12,45,58,75 [batch_functions:r1:c5:f5; c15:f7–f10; c19:f2; c24:f11]).
2. **Partial sync failure:** Exhausted malformed item quarantines with reason/correlation/remediation and ledger exception; cursor passes only durable preceding outcomes. Remaining batch may continue; not all-success. (pp.28–29 [batch_functions:r1:c10:f7,f12]).
3. **Derivative failure/resumption:** Fail index write; accepted metadata remains. Fingerprint/outbox reconciliation repairs. Backfill produces per-batch receipts; queue emptiness alone never declares readiness; alias switch only after completeness/recall. (pp.34,49,78 [batch_functions:r1:c12:f3; c16:f8; c25:f3]).
4. **Rerun:** Accepted events, including every retained chapter event, record duplicate outcome without reapplication. `T-07` replays same event **100 times**; this is test count, not retry allowance. (pp.10–80 registers; p.88 [batch_functions:r1:c29:f7]).
5. **No input:** Successful/empty/mixed-permission/adversarial/malformed fixtures are required, but **per-job empty selection/delta/replay/export/evaluation completion behavior is Needs confirmation**. `NO_SUPPORTED_EVIDENCE` is retrieval behavior, not a batch empty-success default. (pp.36,89 [batch_functions:r1:c12:f10; c30:f16]).
6. **Security negative pack:** `T-01` foreign IDs; `T-02` hostile PDF directives; `T-03` prior-draft approval; `T-04` polyglot/zipped attacks; `T-05` credential observations; `T-06` regional unapproved fallback; `T-08` mid-search revocation; `T-09` historical audit edit; `T-10` recursive tool hints; `T-11` single-Admin export; `T-12` replaced score fixtures. ZIP is attack input, not supported upload. Preserve `SEC-001`–`SEC-012` blocking namespace without invented T/SEC one-to-one mapping. Independent security-control reproduction/signature is required. (p.88 [batch_functions:r1:c29:f1–f13]).
7. **Recovery:** Contain only faulty indexing shard; bounded validated replay; compare fingerprints/denied probes before incident closure and retain incident evidence. ACL leak reenables only after negative tests. Webhook failure leaves accepted case unchanged. (pp.55,79,90 [batch_functions:r1:c18:f7; c25:f5; c31:f6–f11]).
8. **Reproducibility:** Record every randomized seed; freeze/version/independently review corpora for leakage. Test transactions/outbox/revocation/delayed-index/purge with randomized retries leaving one accepted outcome. Signed release test outputs link digest. (pp.74,89 [batch_functions:r1:c24:f2,f7; c30:f17–f19]).

## Consistency and Open Questions

### Required clarifications and earlier-file amendments

| Open ID / affected functions | Source conflict or missing condition | Required decision / dependency |
|---|---|---|
| BAT-OQ-001 / all | Services/requester personas/scopes differ; no complete deployment or action matrix | Define worker identities/deployed function boundaries/manual grants and Workspace Admin/Admin/Owner/Member/approver/Operators. Link API-OQ-001/002 and SF-002/OQ-001; do not invent roles. |
| BAT-OQ-002 / all | No cron/cadence/timezone; scheduled tombstone p.51, daily rollups p.65, continuous backup p.69 are distinct | Confirm schedule/calendar/manual launch/misfire/overlap policy per function. No daily execution time inferred. |
| BAT-OQ-003 / all | IDL/selected schemas incomplete; transaction units known only for core ACID/checkpoint/cursor | Complete arguments/results/checkpoints/manifests/receipts/ledger selection/empty/partial statuses, commit sizes and concurrency/locks/lease mechanisms. Link API-OQ-003/012/014, DAT-OQ-001/006/013/015. |
| BAT-OQ-004 / BAT-007–009 | Missing-approval termination p.41 vs waiting p.49/82 and SLA expiry p.45; recoverable timeout p.12 vs FAILED p.82; AUTO_ALLOW p.44 vs linear review | Resolve timing/timeout literal/recovery/expiry-run effects/AUTO_ALLOW edges. Link API-OQ-009, DAT-OQ-008, SF-OQ-008. No implicit approval or example timeout. Findings c14:f10; c16:f7; c15:f3,f6; c5:f7; c26:f3. |
| BAT-OQ-005 / all recovery/admission | Retry/circuit/scaling/quotas/alert/heartbeat bounds absent | Version numeric controls; confirm provider backoff/deadlines/replay scope/fairness and fault recovery. Link API-OQ-012/016, DAT-OQ-014/018. |
| BAT-OQ-006 / state/event functions | Mutable cases p.24–25 vs immutable labels pp.13/17/26; SyncRun/IndexAlias/task/form labels vs changing control state; rejection before AccessDenied p.22 vs denial audit pp.23/87 | Amend register distinction current mutable state vs immutable artifacts/revisions. Define denial ordering/revision without suppressing audit. Link API-OQ-006/013; DAT-OQ-002/010/012. Findings c5:f12; c6:f13; c9:f15; c10:f13; c12:f11; c15:f11; c19:f10; c8:f9,f11; c28:f7. |
| BAT-OQ-007 / ancillary/read contracts | Generic GET allocation/event wording throughout versus actual reads; `POST /v1/runs` vs case-scoped; workspace settings/case PATCH p.24; provisioning/backfill/recovery/export-delete associations pp.78–80 | Resolve each causal mapping. No GET mutation, unapproved alias, invented workspace payload or provisioning-via-export/delete. Link API-OQ-005/006/007/019 and DAT-OQ-004/011. Findings c6:f3,f9; c26:f9; c9:f6; c25:f17. |
| BAT-OQ-008 / BAT-012–020 | Hold/retention/two-person scope and formats incomplete; corporate policy unselected | Define eligible closed-case retention, protected receipts, independent approver/hold lifecycle, export delivery and credential/key strategy. Link API-OQ-014/017; DAT-OQ-015/016/019. |
| BAT-OQ-009 / BAT-002–007 | Cap units/decompression/OCR/quality/anchor/fingerprint/Citation/coverage gates missing | Complete versioned constraints and formats, preserving quarantine vs viewable low quality and cursor continuation. Link API-OQ-011/015; DAT-OQ-007/014. |
| BAT-OQ-010 / BAT-018/021–023 | Usage formulas/timezones/late corrections; score CI/denominators/partial failure; migration/recovery/signatures formats absent | Define implementation/testable calculation and artifact procedures; do not infer schedules or down-migration. Link DAT-OQ-020/API-OQ-019. |
| BAT-OQ-011 / architecture dependencies | p.90 requires dated region/search/identity/model/retention/connector decisions; p.10 encryption tradeoff open | Resolve before implementation lock; encryption tradeoff before enterprise GA. No selected provider/date/owner/approval invented. Link API-OQ-017; DAT-OQ-019; SF-OQ-018. |

These conflicts remain recorded, not silent rewrites of earlier files. Specific domain evidence supports mutable case state, eligible retention and safe per-item continuation; inconsistent register wording still requires amendment. Chapter-only endpoints/events are not excluded because Appendix A omits them. Governance `POST /v1/design-decisions` / `GET /v1/design-baselines/{id}`, membership, holds, health, catalog and ancillary reads retain API contract obligations but are not additional confirmed periodic jobs. Baseline changes require architecture records/impact scores and approved minor/incompatible major revision rules. (pp.8–10 [batch_functions:r1:c4:f1–f5,f11–f15]).

### Example configuration is not an operational decision

Appendix F p.90 exact example values: `release: r1.0`; workflow `max_plan_depth: 8`, `max_tool_calls: 16`, `run_timeout_seconds: 180`, `replay_dedup_hours: 24`; retrieval `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `embed_dimension: 1536`, `hybrid_rrf_k: 60`; policy `auto_publish_classification: INTERNAL`, `require_human_review_for: [HIGH_RISK, RESTRICTED]`, `self_approval_allowed: false`; storage `upload_limit_mb: 25`, `user_data_region: primary-approved-region`; observability `trace_sample_rate: 0.10`, `diagnostic_retention_days: 30`, `audit_retention_years: 7`. [batch_functions:r1:c31:f1–f5].

Independent chapter support confirms depth/call limits, dimension, configurable file cap, actor/fingerprint retention and substantive no-self-approval/diagnostic/audit rules **in their stated scopes**. Timeout 180, candidate 80, global selected ten, RRF 60, sample 0.10, auto-publish INTERNAL and placeholder region remain examples. No example creates universal consumer retention, scheduler cadence or approved routing.

### Later-stage dependencies

This is Stage 4. Exception/error/retry details and remaining architecture outputs are **To be defined in a later stage**; no later file is presumed generated. Stage 8 must consolidate BAT-OQ items in `08_architecture_decision.md`, linking `04_batch_functions.md` BAT identifiers and affected `02_api.md`, `03_data.md`, `01_screen_functions.md` identifiers. It must not invent decisions, owners, dates or approvals. The present specification remains provisional pending separate root approval.
