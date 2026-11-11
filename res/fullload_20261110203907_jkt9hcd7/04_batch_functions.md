# 4. Batch Function Specification

## Batch Inventory and Triggers

### Baseline and Evidence Status

This specification covers background, event-driven, scheduled and operator-controlled processing for OrionDesk AI **OD-AI-DDS-001, R1.0 / revision 1.3**.

**Source** means `1794310747-OrionDesk_AI_Detailed_Design_Specification.pdf`; references use original PDF page numbers.

- **Confirmed:** Explicitly supported processing requirements.
- **Needs confirmation:** Missing operational or interface details that must be resolved before implementation lock.
- **Proposal:** Suggested implementation organization, not an approved source requirement.

The source confirms batch processing, including asynchronous classification, extraction, indexing, reconciliation, retention and bounded historical backfill. `BAT-*` identifiers are assigned here because the source supplies no batch-job IDs. These identifiers identify logical functions, not mandatory separate executables, queues or deployments.

Related contracts and data identifiers refer to [02_api.md](02_api.md) and [03_data.md](03_data.md). Earlier proposed schemas and screen placements remain proposals.

### Job Inventory

Unless stated otherwise:

- Exact scheduler, cron expression, execution timezone, launch window, manual-launch permission and launch endpoint **Need confirmation**.
- Event-driven jobs have no confirmed periodic schedule.
- Dependencies below describe supported processing relationships, not a mandated global job chain.
- Executing component names do not establish complete service-account grants.

| Job ID | Name and purpose | Executing actor / component | Trigger and manual execution | Predecessors, successors and prerequisites | Evidence |
|---|---|---|---|---|---|
| BAT-001 | Case classification — attach policy-aware labels, confidence and provenance | Classifier; Triage Agent classifies cases; exact component relationship Needs confirmation | `CaseCreated`; case creation through API-001. Separate manual rerun unspecified | Accepted case ID/revision → classification output; no confirmed attachment-readiness dependency | Source, p. 12, §2.2.1; p. 40, §11.1.1; p. 87, §C.1 |
| BAT-002 | Incremental connector synchronization — preserve source identity, permissions and changes | Connector workers; Admin initiates | API-018, `POST /v1/connectors/{connectorId}/sync`, `202`; periodic schedule unspecified | Completed BAT-011 provisioning; configured capabilities/credentials → BAT-003 and BAT-007 as applicable | Source, pp. 27–29, §§7.1–7.3; pp. 78, 83 |
| BAT-003 | Document scan, extraction and normalization | Ingestion Service / extraction workers | Attachment acceptance through API-006, `202`, or connector ingestion; side-by-side reprocessing supported | Accepted immutable source → `DocumentNormalized` → BAT-004; scan before parsing | Source, pp. 30–32, Chapter 8; p. 87 |
| BAT-004 | Embedding and search-index construction | Embedding workers / Indexer | `DocumentNormalized` | Version ID/source hash from BAT-003 → `SearchIndexCommitted` → BAT-007 cache invalidation | Source, p. 19, §4.2.1; p. 34, §9.1.1; p. 87 |
| BAT-005 | Parallel search-index rebuild | Search subsystem; exact executing identity unspecified | Rebuild supported; initiating API and automatic/manual trigger unspecified | Authoritative source inventory → completeness/recall validation → atomic read-alias switch | Source, p. 34, §9.1.2 |
| BAT-006 | Source/index and outbox-link reconciliation | Reconciliation worker | Failed index writes / broken message links; scan cadence and manual launch unspecified | Durable source metadata and outbox ledger → repair/retry BAT-004 delivery or indexing | Source, p. 49, §13.2.2 |
| BAT-007 | Source deletion and ACL/cache propagation | Connector and search/cache boundaries; exact worker division unspecified | Source delete, source ACL change, or `SearchIndexCommitted`; scoped ACL replay under incident runbook | Current source changes → tombstone/index removal/cache invalidation; revocation effective before next retrieval | Source, pp. 28, 53, 79, 87 |
| BAT-008 | Durable grounded AI workflow and publication validation | Orchestrator, Research Agent, Draft Agent, Model Gateway, deterministic Policy Service | API-008/API-009 run request; `AgentPlanApproved`, `WorkflowStageAdvanced`, `ApprovalDecisionRecorded` drive consumers | Authorized case, admission, approved capabilities/evidence → candidate/policy/review → gated publication or failure | Source, pp. 37–46, 48–49, 69, 87 |
| BAT-009 | Review-task expiry and reassignment/escalation | Policy/review boundary; exact worker identity unspecified | Configured review SLA expiry; timer-versus-scan implementation unspecified | Eligible pending review task → recorded expiry/reassignment/escalation; never implicit approval | Source, p. 45, §12.2.1; p. 89, `TST-010` |
| BAT-010 | Outbox dispatch and controlled dead-letter replay | Messaging boundary; authorized operator for replay | Committed outbox; manual API-038, `POST /internal/deadletters/{id}/replay`; bounded validated outbox replay in indexing runbook | Durable event / validated replay scope → appropriate event consumer; reason, dry run and scope limit for dead letters | Source, pp. 17, 48–50, 90 |
| BAT-011 | Tenant/workspace provisioning | Provisioning workflow; initiating role and service identity unspecified | Onboarding; API-056 remains undefined | Policy, encryption references, role bindings, quotas, connector stubs → enables BAT-002; incomplete state blocks sync | Source, p. 78, §22.1.1 |
| BAT-012 | Historical document backfill | Onboarding/ingestion boundary; exact actor unspecified | Historical onboarding; manual interface and schedule unspecified | Provisioned scope and stable source IDs → bounded ingestion windows through BAT-003/BAT-004 and per-batch reconciliation | Source, p. 78, §22.1.2 |
| BAT-013 | Retention and scheduled tombstone purge | Retention Worker / storage boundary | Scheduled final purge confirmed; exact schedule unspecified. API-040 provides purge interface, response mode unresolved | Eligible closed cases and applicable retention/holds → tombstones, removal, receipts; diagnostic/audit policies remain distinct | Source, pp. 26, 51–53, 66, 85 |
| BAT-014 | Controlled workspace export and verified deletion | Authorized Admin + approver; Retention Worker produces deletion verification | API-025/API-026, `202`; two independent approval checks | Authorized inventory and legal holds → export package or purge receipts; export is not confirmed as a mandatory predecessor to deletion | Source, pp. 78–80, 83, 87 |
| BAT-015 | Daily usage and cost rollup | Usage/cost boundary; exact worker identity unspecified | Daily aggregation confirmed; clock time/timezone and manual recalculation unspecified | Attributed invocation, embedding, storage and indexing usage → budget, forecast, rejected excess requests | Source, p. 65, §18.3.1 |
| BAT-016 | Frozen benchmark evaluation | Evaluation harness; Admin initiates | API-023, `POST /v1/evaluations`, `202`; model/prompt changes require reevaluation | Frozen versioned synthetic dataset/expected outcomes → Scorecard, ReleaseGateResult, `EvaluationCompleted` | Source, pp. 74–76, 83, 88–89 |
| BAT-017 | Audit batch-hash chaining and retention export | Audit boundary; exact executor unspecified | Append-only audit accumulation; batch cutoff and schedule unspecified | Audit entries → batch-hash chain and independently controlled retention storage | Source, p. 62, §17.3.1 |
| BAT-018 | Deployment migration, bounded backfill and release verification | CI/CD tooling; Security and SRE sign-off | Deployment workflow/API-043; no periodic schedule confirmed | Compatible expansion → bounded backfill → old-replica drain → constraint enforcement; release gates before promotion | Source, pp. 52, 71–73, 89 |
| BAT-019 | Continuous backup and incident-controlled recovery | Backup infrastructure; incident command controls recovery-region restore | Continuous PostgreSQL backup; incident restore and recovery exercises. Exact exercise cadence unspecified | Primary relational/object state → consistent restored state and index rebuild recipes | Source, pp. 19, 69–70, 89 |
| BAT-020 | Optional signed webhook delivery | Notification integration boundary; exact executor unspecified | Applicable committed internal transitions; event subscription mapping unspecified | Durable internal transition → signed external notification; failure does not roll back internal state | Source, pp. 52, 55 |

### Functions Whose Batch Implementation Is Not Confirmed

| Function | Confirmed behavior | Batch-specific gap | Evidence |
|---|---|---|---|
| Secret/key rotation | Service credentials rotate automatically; vault-managed encryption keys rotate by policy without bulk reencryption in the request path | Needs confirmation: whether a separate application batch job is required, its scope, schedule, arguments and completion checks | Source, pp. 21, 63 |
| Advisory SLA breach prediction | Prediction cannot change contractual deadlines | Needs confirmation: whether prediction is background processing and its trigger/algorithm | Source, p. 25 |
| Alert enrichment | `AccessDenied` consumers enrich alerts | Needs confirmation: whether a separately managed batch function is required; consumer payload/aggregation rules | Source, p. 87 |
| Data subject access requests | Use the deletion workflow's inventory | Needs confirmation: request execution mechanism, identity verification and whether a separate batch job is required | Source, p. 80 |

No foundation-model training/fine-tuning, unrestricted browsing, physical automation or irreversible financial transaction jobs are included: these activities are explicitly excluded by Source, p. 9, §1.2.1. Multilingual OCR beyond English and cross-region active/active mutation remain deferred, not implicitly enabled by background processing (Source, p. 10, §1.3.2).

## Processing by Job

### Shared Arguments, Inputs and Validation

**BAT-R-001 — Confirmed:** Every background job carries immutable tenant identity in a signed envelope. Every storage access uses tenant scope/RLS; pooled scoped session variables are reset after each transaction. Mutations preserve tenant, revision, actor, occurrence time and correlation context.  
**Evidence:** Source, pp. 22, 51, 86; API-R-010; DAT-R-002, DAT-R-005.

| Argument / context | Definition and applicability | Requiredness / format | Open decisions |
|---|---|---|---|
| `tenant_id` | Immutable authorized execution scope, all tenant-owned work | Required; UUIDv7 identity baseline | Signature verification format, provisioning identity allocation |
| Event envelope | `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, `payload` | Required for event-driven execution; canonical JSON and UTC | Full payload schemas, canonicalization and signing |
| Actor / revision / occurrence / correlation context | Responsible principal and durable mutation lineage | Required for durable changes | Mapping to selected storage fields such as `actor`, `at`, `purge_time` |
| `Idempotency-Key` | Public POST creation of long-running operations | Required; same fingerprint returns original operation | Length, namespace, canonicalization, in-flight race and expiry |
| Resource references | Case, connector, document version, run, workspace, evaluation or dead-letter identity | Route/event references as supplied; exact job argument schemas unavailable | No undocumented CLI flags or JSON property names are confirmed |
| Policy/configuration versions | Applicable retention, model, tool, reviewer and pipeline configuration | Version-bound where specified | Capture timing, policy change during execution |
| Window / scope / cutoff | Historical backfill, replay, rollup, purge, migration and rebuild selection | Bounded scope required where stated | Exact selector names/types, interval inclusion and maximum sizes |

**Evidence:** Source, pp. 17, 22, 25, 48, 54, 64, 78, 87; API-R-003, API-R-007; DAT-R-004.

All unspecified argument types, lengths, requiredness, defaults, selection ordering, output schemas and physical update columns **Need confirmation**. Domain concepts in the following procedures are not invented wire fields.

### BAT-001 — Case Classification

**Inputs/targets:** `CaseCreated` case ID/revision; authorized case business context; DAT-003/DAT-004 classification labels, confidences, provenance and correction reason; API-001, API-051.

1. Validate tenant/event context and deduplicate delivery.
2. Resolve the authorized case and supplied revision.
3. Perform policy-aware classification.
4. Attach classification labels, confidence and provenance through the domain mutation boundary.
5. Preserve user correction behavior: corrections require a reason code.

**Successful completion:** Classification output is durably associated with the relevant case without a duplicate accepted mutation.

**Needs confirmation:** Classification algorithm, label/confidence schema, automatic case-state transition, handling of a later user correction while classification is running, reclassification trigger and empty business context.

**Evidence:** Source, pp. 12, 25, 40, 87.

### BAT-002 — Incremental Connector Synchronization

**Inputs/targets:** API-018/API-019/API-048; DAT-021 Connector/SyncRun; DAT-015 `connector_cursors.connector_id`, `cursor`, `watermark`, `retry_state`; DAT-005 `source_id`, sensitivity and ACL records.

1. Verify completed provisioning and authorized connector scope.
2. Inspect advertised `list`, `fetch`, delta cursor, ACL and delete capabilities.
3. Record unsupported capabilities as lower trust with a visible warning; do not presume support.
4. Resolve workspace-scoped credentials from the secret store. Revoked credentials cause queued jobs to fail with `CONNECTOR_REAUTH_REQUIRED`.
5. Read provider changes using the persisted cursor/high-watermark.
6. Preserve source IDs, source permissions and change history; dispatch eligible document ingestion.
7. Apply source deletes/ACL changes through BAT-007.
8. Persist ingestion outcomes and error-ledger exceptions.
9. Advance the cursor only after all preceding items have durable outcomes.

**Successful completion:** Selected source items have durable outcomes and cursor advancement does not skip undurable preceding work. A quarantined poison record can coexist with continued processing of the remaining batch.

**Needs confirmation:** Provider contracts, initial cursor, cursor expiration, sync boundary, item ordering, batch size, same-connector concurrent execution and complete-versus-partial success status.

**Evidence:** Source, pp. 27–29, 78, 85.

### BAT-003 — Scan, Extraction and Normalization

**Inputs/targets:** API-006/API-007/API-039; DAT-005–007, DAT-020, DAT-022; `document_versions.hash`, `parser_version`, `object_key`; `chunks.document_version_id`, `page`, `bbox`, `text_hash`.

1. Validate allowed PDF, DOCX, HTML or UTF-8 text; require MIME signature/extension agreement, configured 25 MB per-file cap and decompression-bomb threshold.
2. Scan before parsing; disable macros and never fetch embedded remote references.
3. Quarantine unsafe content without indexing.
4. Parse PDF pages into blocks/page indexes/bounding boxes; retain table row/column annotations, headings and reading order.
5. Apply OCR only when opted in and record provenance.
6. Normalize transport artifacts without rewriting claims.
7. Create immutable derivatives using content fingerprint plus pipeline version; reprocessing may coexist side by side.
8. Store source URI, file hash, page number and optional bounding box for each chunk.
9. Record empty-page ratio, unknown-character ratio, table-loss indicators and language confidence; tag likely personal data.
10. Make authorized low-quality documents viewable while excluding them from autonomous recommendations.
11. Publish `DocumentNormalized` through the durable event boundary.

**Successful completion:** Immutable normalized derivatives and resolvable anchors are stored with quality/provenance evidence; downstream indexing is distinct from extraction completion. `202` is only acceptance.

**Needs confirmation:** MB byte interpretation, parser/bomb thresholds, quality cutoffs, OCR default/configuration, coordinate encoding, derivative ID mapping, per-file commit boundary and empty-document outcome.

**Evidence:** Source, pp. 30–32, 62, 82–85.

### BAT-004 — Embedding and Index Construction

**Inputs/targets:** `DocumentNormalized` version ID/source hash; DAT-007/DAT-023; SearchChunk fields from DAT-R-003; API-013–015 downstream reads.

1. Validate the event and immutable source/version references.
2. Build searchable derivatives with `tenant_id`, `workspace_id`, `document_version_id`, `chunk_id`, `language`, `classification`, **1536-dimensional embedding**, and normalized keyword-analyzed text.
3. Write through versioned aliases while retaining PostgreSQL as authoritative metadata.
4. Persist the supported indexing outcome and publish `SearchIndexCommitted` with index generation/document revision context.
5. Trigger query-cache invalidation through BAT-007.

**Successful completion:** The corresponding indexed version can be reconciled to its source fingerprint and index generation. Unsafe quarantined documents never enter the index; low-quality content cannot become autonomous evidence merely because it is indexed.

**Needs confirmation:** Embedding deployment, batch/token limits, index commit unit, partial chunk failures, quality eligibility representation, index-status-to-`READY` mapping and event publication/reconciliation protocol.

**Evidence:** Source, pp. 19, 30–34, 49, 87.

### BAT-005 and BAT-006 — Rebuild and Reconciliation

**Inputs/targets:** DAT-005–007/DAT-014/DAT-023; source fingerprints, indexed versions, IndexAlias, outbox ledger; DAT-R-011–012.

**BAT-005 procedure:**

1. Resolve authoritative rebuild scope.
2. Create a parallel index rather than replacing the active index in place.
3. Populate the parallel index with versioned source derivatives.
4. Run completeness and recall checks.
5. Atomically switch the read alias only after checks pass.

**Completion:** Validated parallel index is activated by an atomic alias switch.

**BAT-006 procedure:**

1. Compare accepted source fingerprints with indexed versions.
2. Identify failed/missing index writes and retry them.
3. Repair broken message links from the outbox ledger.
4. Preserve accepted source metadata throughout repair.

**Completion:** Identified source/index or message-link discrepancies are repaired with traceable durable outcomes.

**Needs confirmation:** Extraction predicates, scan cadence, completeness/recall thresholds, authoritative snapshot boundary, delta changes during rebuild, concurrency with purge/sync, old-index retirement and unresolved-discrepancy status.

**Evidence:** Source, pp. 34, 49, 90.

### BAT-007 — Source Deletion, ACL and Cache Propagation

**Inputs/targets:** DAT-005/DAT-019/DAT-023/DAT-028; source ACL revision and tombstones; cache key dimensions from DAT-R-003.

1. On source delete, create a tombstone and schedule index removal.
2. Prevent retrieval of soft-deleted entities.
3. On ACL changes, invalidate affected evidence/query caches before serving new results and before ordinary TTL expiry.
4. On `SearchIndexCommitted`, invalidate query caches by index generation/document revision.
5. For suspected ACL leakage, suspend affected aliases, revoke cached evidence, preserve audit traces and replay scoped ACL revisions.
6. Reenable affected search only after negative access tests pass.

**Completion:** No revoked evidence is returned on the next retrieval. Asynchronous index removal does not permit stale visibility.

**Needs confirmation:** Propagation transport, race-safe invalidation, source-change detection latency, index-removal acknowledgement, replay interface and delete-versus-retention interactions.

**Evidence:** Source, pp. 27–28, 51, 53, 79, 87, 89, `TST-004`.

### BAT-008 — Grounded AI Workflow and Publication

**Inputs/targets:** API-008–012/API-036/API-045–046/API-049/API-017; DAT-008–012/DAT-016–017/DAT-024–026.

1. Admit new generation only when workspace tokens, queue age and provider capacity satisfy configured thresholds.
2. Reserve input/output token budget and persist plan revision before side effects.
3. Execute the dependency-bound DAG with maximum depth **eight** and maximum **sixteen tool invocations**.
4. Persist each stage checkpoint before downstream dispatch.
5. Retrieve currently authorized, anchored evidence using bounded hybrid candidates, reciprocal rank fusion, deterministic reranking, diversity and returned-token budgets.
6. Return `NO_SUPPORTED_EVIDENCE` for insufficient evidence; do not fabricate context.
7. Use only approved deployment/region/data-handling routes. Approved fallback must preserve or strengthen data-handling class.
8. Build prompts from fixed rules, signed workflow instruction, validated user input and separately delimited untrusted evidence. Strip evidence tool directives, retain injection indicators and minimize nonessential personal data where policy permits.
9. Validate versioned JSON output with bounded retries; unknown fields, invalid citations or control-character injection cause `MODEL_OUTPUT_INVALID`.
10. Store normalized policy inputs with rule version and deterministic outcome: `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE` or `DENY`.
11. Obtain required eligible human review with exact-artifact binding and segregation of duties.
12. On publication validation, recheck current evidence authorization and exact artifact hash. Atomically record satisfied gate and update final response pointer.
13. Record failure at the exact checkpoint for stop conditions; never present partial processing as approved.

Quota exhaustion is terminal for the current run without automatic model/data-class switching. Missing approval, exhausted call budget, repeated invalid plans, policy denial and deadline expiry stop execution. Discovery/model text never authorizes tools; a denied action cannot be substituted with an equivalent tool.

**Completion:** A legitimately published exact artifact or a supported terminal/recoverable outcome is persisted. `AWAITING_REVIEW` is a waiting state, not publication success.

**Needs confirmation:** Canonical creation route, policy auto-allow path, publication trigger, plan and output IDL, admission values, stop-code mappings and timeout coverage. Source p. 90 gives example `run_timeout_seconds: 180`; it does not settle human-wait timeout semantics.

**Evidence:** Source, pp. 12–13, 35–46, 49, 62, 69, 82, 87, 90.

### BAT-009 and BAT-010 — Expiry, Dispatch and Replay

**BAT-009 inputs/targets:** DAT-011/DAT-026; configured reviewer pool, role, SLA, task state and assignment.

1. Select tasks whose configured SLA has expired.
2. Enforce current task/assignment policy and separation of duties.
3. Record expiration and reassign or escalate.
4. Never create implicit approval.

**Completion:** Required reassignment/escalation is recorded without publication authority.

**Needs confirmation:** Eligible states, SLA clock/calendar, task selection cadence, race with reviewer decision, routing priorities and repeated escalation behavior.  
**Evidence:** Source, pp. 45, 82, 89.

**BAT-010 inputs/targets:** DAT-014/DAT-027; event envelope, consumer ledger, DeadLetterEntry; API-038.

1. Dispatch state-changing work only from committed outbox publication or an explicitly reconciled saga step.
2. Consumers deduplicate event ID/operation key and detect stale aggregate revisions.
3. Record duplicate outcome and return without reapplying a mutation.
4. Before dead-letter replay, require operator reason, dry-run validation and scope limit.
5. Preserve original event identity unless schema transformation has explicit migration provenance.
6. Resume appropriate consumers from valid persisted checkpoints.

**Completion:** Delivery/replay results in at most one accepted mutation for the original operation; operator recovery stays within validated scope.

**Needs confirmation:** Outbox selection/acknowledgement, lease ownership, dead-letter entry conditions, scope units, dry-run proof, dedup retention, operator permissions and final delivery-status schema.  
**Evidence:** Source, pp. 17, 48–50, 87, 90.

### BAT-011 and BAT-012 — Provisioning and Historical Backfill

**Inputs/targets:** API-056; DAT-001–002/DAT-019/DAT-021/DAT-029/DAT-034.

**BAT-011:**

1. Create workspace policy, encryption references, role bindings, quotas and connector stubs as one idempotent workflow.
2. Expose incomplete provisioning.
3. Block connector sync until provisioning is complete.

**Completion:** Required provisioning elements exist consistently and sync eligibility reflects completion.

**BAT-012:**

1. Select historical documents in bounded windows.
2. Preserve stable source IDs.
3. Ingest through the document/index pipeline.
4. Produce per-batch reconciliation receipts.
5. Signal search readiness using index coverage, not queue emptiness.

**Completion:** The selected window has durable ingestion/reconciliation evidence; readiness satisfies coverage checks.

**Needs confirmation:** Initiation contracts, required configuration, step order/compensation, window size and boundaries, backfill overlap, receipt schema, coverage threshold and no-document result.

**Evidence:** Source, p. 78, §§22.1.1–22.1.2.

### BAT-013 and BAT-014 — Retention, Export and Verified Deletion

**Inputs/targets:** API-025/API-026/API-029/API-040; DAT-003/DAT-018/DAT-029/DAT-034; `deletion_receipts.tenant_id`, `object_ref`, `purge_time`, `actor`.

**BAT-013:**

1. Select only eligible closed cases for case-data retention processing.
2. Apply retention class and legal-hold exceptions.
3. Process scheduled tombstones/final purge with normal retrieval disabled for soft-deleted objects.
4. Preserve distinct diagnostic default **30-day TTL** and security-audit **seven-year policy**.
5. Record completion receipts and legal-hold exceptions.

**BAT-014 export:**

1. Verify two independent approval checks for the authorized workspace inventory.
2. Package case metadata, approved artifacts, source references and audit manifests with checksums.
3. Exclude secrets and internal model prompts.

**BAT-014 deletion:**

1. Verify two independent approval checks and inventory scope.
2. Enforce legal holds; retain protected records and receipt exceptions.
3. Write tombstones.
4. Remove eligible blobs and index entries.
5. Record completion receipts.
6. Emit `TenantDeletionVerified` with manifest ID/receipt hash for purge-record closure.

**Completion:** Export contains required checksummed authorized content, or deletion has verified eligible removals and explicit protected-record receipts. HTTP `202` never means package or purge completion.

**Needs confirmation:** Corporate retention durations/eligibility, routine-retention approval requirements, hold reevaluation during purge, backup treatment, shared-source references, inventory snapshot, archive/checksum format, completion status with holds, orphan/cascade behavior and partial failure recovery. Do not equate routine retention of closed cases with unconditional permission to delete all workspace records.

**Evidence:** Source, pp. 26, 51–53, 66, 78–80, 83, 85, 87, 89.

### BAT-015 — Daily Usage Rollup

**Inputs/targets:** DAT-016/DAT-030; `token_ledger.run_id`, `deployment_id`, `in_tokens`, `out_tokens`; API-022 read projection.

1. Select the applicable daily usage interval.
2. Attribute model invocations, embeddings, storage and indexing usage to workspace cost centers and deployment versions.
3. Aggregate daily budget, forecast and rejected excess requests.
4. Make rollup outputs available to usage reporting.

**Completion:** Daily outputs retain required attribution dimensions.

**Needs confirmation:** Day timezone, interval boundaries, currency/units, price versions, forecast formula, dedup grain, late provider usage, corrections, rerun/upsert behavior and zero-usage representation. No concrete aggregation formula or physical rollup table is confirmed.

**Evidence:** Source, pp. 38, 65, 85.

### BAT-016 — Frozen Evaluation

**Inputs/targets:** API-023/API-024; DAT-033 dataset, Scorecard, ReleaseGateResult.

1. Resolve frozen, versioned, independently reviewed synthetic corpus: **1,200 permission-controlled cases**, with expected citation sets and decision outcomes.
2. Protect expected fixtures through dataset version/signed manifest.
3. Exercise retrieval, refusal, ambiguity and adversarial evidence.
4. Report citation precision target `>=0.97`, unsupported-claim rate `<=0.02`, and high-risk policy recall `1.00` on the frozen safety suite.
5. Report confidence intervals and distribution shift by domain.
6. Block release for low statistical confidence or critical isolation/approval failures; quality scores cannot excuse those failures.
7. Persist results and `EvaluationCompleted` evidence.

**Completion:** Traceable evaluation results exist; completion does not imply a passing release gate. Prompt/model changes require reevaluation.

**Needs confirmation:** Version-selection arguments, scoring/statistical methods, completeness rules, failed-example treatment, parallel execution, reproducibility beyond recorded versions/seeds and empty/corrupt corpus error handling.

**Evidence:** Source, pp. 74–76, 88–89.

### BAT-017–020 — Supporting Operational Processing

| Job | Inputs and ordered processing | Update targets / outputs / completion | Needs confirmation | Evidence |
|---|---|---|---|---|
| BAT-017 | Read append-only audit batches; chain batch hashes; export to independently controlled retention storage | DAT-013 audit lineage/archive; completion preserves immutable historical decisions and hash-chain evidence | Batch boundaries, hash algorithm/encoding, export format, durable acknowledgement, chain repair and executor grants | Source, pp. 62, 66, 88 |
| BAT-018 | Validate build identity/digest and signed configuration; static/dependency/unit/contract checks; expand schema with nullable columns; bounded backfill; canary compatible traffic; enforce constraints after old replicas drain; evaluate release gates and Security/SRE sign-off | DAT-032/DAT-033 release/migration evidence; signed test outputs linked to release digest; reconstructible image/schema/prompt/routing policy | Transformation per migration, batch sizes, cutoffs, rollback readability, canary thresholds/duration and pipeline tooling | Source, pp. 20, 52, 71–73, 89 |
| BAT-019 | Continuously back up PostgreSQL; preserve/test object versions and index recipes; under incident command restore warm-region snapshots; verify relational/object consistency and rebuild indexes as necessary | DAT-031 RecoveryCheckpoint/backups; reference RPO `<=15 minutes`, RTO `<=4 hours` | Backup implementation/retention, restore selectors/order, hold/deletion effects, exercise cadence and recovery verification details | Source, pp. 19, 69–70, 89 |
| BAT-020 | Select subscribed committed transitions; sign outbound notification; deliver; retry exponentially; recipient checks signature and event age | DAT-028 WebhookSubscription/delivery context; API-047; internal transition remains committed regardless of webhook failure | Whether optional webhooks enabled, destination contract, event projection, signature/age limits, recipient success codes and terminal delivery outcome | Source, pp. 52, 55 |

## Operations and Recovery

### Launch Authorization, Concurrency and Mutual Exclusion

**BAT-R-002 — Confirmed:**

1. Validate inputs before allocating long-running work, at transaction/domain boundaries and before tool dispatch.
2. Authenticate services independently with scoped identities/audience checks; jobs cannot use model output to change tenant or grants.
3. Keep worker egress limited to declared connector/model endpoints; no public datastore.
4. Retain tenant-scoped authorization through retries, replay, reconciliation and recovery.
5. Reject stale/unauthorized writes without changing business state or publishing accepted-transition events.

**Evidence:** Source, pp. 15–18, 21–23, 41–42, 56; API-R-001, API-R-004, API-R-009.

| Concurrent-launch concern | Confirmed invariant | Needs confirmation |
|---|---|---|
| Identical public job-creation request | Same key/fingerprint returns original operation; changed fingerprint returns `IDEMPOTENCY_CONFLICT` | In-flight duplicate response, key namespace and outcome retention |
| Same event processed by multiple workers | One accepted mutation; dedup/event-revision safeguards | Claim/lease/lock/fencing implementation and ledger transaction |
| Concurrent sync/backfill on same connector | Cursor cannot skip preceding undurable outcomes; stable source IDs | Mutual-exclusion scope, overlapping windows and cursor owner |
| Rebuild versus incremental writes/ACL changes | Atomic alias switch after checks; no stale unauthorized retrieval | Snapshot/delta reconciliation and switch fencing |
| Purge versus ingestion, export, review or rebuild | Holds/tenant scope/soft-delete visibility/exact-artifact checks preserved | Conflict policy, snapshot consistency, locks and cancellation |
| Expiry versus reviewer decision | No implicit approval; exact eligible decision binding | Transactional winner rule and stale task response |
| Rollup/evaluation/migration rerun | Shared retry-idempotent write rules apply | Job-specific dedup grain and same-version duplicate policy |
| Worker capacity | Fair scheduling prevents large tenants starving smaller workspaces; extraction/embedding workers scale by queue age/throughput | Worker counts, partitioning, quotas and scheduling algorithm |

**Evidence:** Source, pp. 19, 25, 28, 34, 45, 48–49, 54, 78.

The source does not confirm a global singleton scheduler or one-job-at-a-time rule. A lock/lease design must be recorded before implementation rather than inferred from the required invariants.

### Processing and Commit Units

**BAT-R-003 — Confirmed:**

- Case mutations, approval decisions and associated outbox inserts use the source-defined ACID boundary.
- Each AI stage writes a durable checkpoint before dispatch.
- Connector cursor advancement follows durable preceding-item outcomes.
- Historical onboarding uses bounded windows and per-batch receipts.
- Schema backfills use bounded batches.
- Publication pointer and satisfied gate commit atomically.
- External indexing/webhook writes are asynchronous and explicitly reconciled.

**Evidence:** Source, pp. 28, 40, 45, 49, 52, 78; API-R-005–006; DAT-R-007–008, DAT-R-013–014.

**Needs confirmation:** Transaction isolation/locking, document/chunk/index commit units, audit/usage batch units, deletion receipt atomics, acknowledgement timing, batch sizes and checkpoints outside explicitly defined workflows. No distributed ACID transaction across provider, index, object storage and PostgreSQL is confirmed.

### Idempotency, Rerun and Resumption

**BAT-R-004 — Confirmed:**

1. Assume at-least-once message delivery.
2. Deduplicate event ID/operation key and detect stale aggregate revisions; do not rely on ordering across partitions.
3. Record duplicate outcomes without reapplying mutations.
4. Resume from persisted checkpoints/events rather than browser memory.
5. Preserve replay event identity except explicitly provenance-linked schema migration.
6. Preserve immutable source derivatives during pipeline-version reprocessing.
7. Rework denied drafts as new run revisions; do not retroactively approve old denial.
8. Treat SSE reconnection/backfill as observation, not a new execution request.

Case idempotency retains actor/request-fingerprint outcome for **24 hours**. This is not a confirmed universal batch ledger retention period. Appendix F `replay_dedup_hours: 24` remains configuration-example evidence.

**Evidence:** Source, pp. 17, 25, 31, 46, 48–50, 54–55, 58, 90; API-R-007–008; DAT-R-010.

**Needs confirmation:** Dedup ledger retention covering delayed delivery, restart claim recovery, rerun selectors, completed-job replay response, retry-counter persistence, lost-worker detection and job-specific checkpoint schemas.

### Retries and Timeouts

| Condition | Confirmed handling | Unresolved operational values |
|---|---|---|
| Transient dependency failure | Bounded exponential backoff, randomized jitter, per-dependency circuit breaker | Attempt cap, base/max delay, circuit thresholds/reset, total deadline |
| Provider throttling | Honor `Retry-After`; workspace quotas/fair scheduling; capped retries and controlled admission | Delay parsing, per-provider quotas and retry budget |
| Validation/permission failure | Permanent; not retried | Detailed error-code/status mapping |
| Malformed connector record | Bounded retries then quarantine with reason/correlation/remediation; remaining batch may proceed | Retry classification distinct from permanent validation denial; cap and quarantine transition |
| Revoked connector credential | Queued work fails `CONNECTOR_REAUTH_REQUIRED`; no tokens disclosed | Reauthorization/requeue contract |
| Invalid model output | Bounded validation retries, then `MODEL_OUTPUT_INVALID`; no publication | Parsing retry cap and provider-charge handling |
| Quota exhaustion | Terminal for current AI run; no automatic model/data-class switch | Terminal code and reservation reconciliation |
| AI stop/deadline | Exact failed checkpoint visible; terminal/configured maximum or recoverable timeout outcome | Timeout clock, human waiting, recoverable state schema |
| Lost worker heartbeat/object access fault | Covered by fault injection; safety and recovery time assessed | Heartbeat cadence, lease expiry and takeover protocol |

**Evidence:** Source, pp. 12, 27–29, 38, 41–42, 49, 69–70, 89–90.

No universal batch timeout is confirmed. The example 180-second run timeout must not be applied to extraction, rebuild, purge, evaluation or human review.

### Rollback and Compensation

**BAT-R-005 — Confirmed:**

- A failed index write does not roll back accepted source metadata; reconcile fingerprints and retry.
- Repair broken message links from the outbox ledger.
- Unsafe files remain quarantined without index admission.
- Webhook failure cannot roll back the internal case transition.
- Rejected stale/unauthorized mutation leaves business state unchanged.
- Canary regression causes automated traffic rollback, not automatic database down-migration.
- Binary rollback invokes compensating data operations only when explicitly supported.
- Preserve held records and record exceptions; never compensate purge failure by overriding a legal hold.

**Evidence:** Source, pp. 20, 30, 49, 55, 72, 80, 89.

**Needs confirmation:** Compensation for partially provisioned resources, orphan derivatives/export packages, partially deleted inventories, token reservations and provider requests with ambiguous outcomes. No automatic restoration of physically purged objects or cleanup policy is confirmed.

### Notifications, Logging and Monitoring

**BAT-R-006 — Confirmed:**

- Preserve `trace_id` and `correlation_id`; correlate DB, connector, retrieval, model and approval stages.
- Log identifiers, policy outcomes, token counts and digests, never user documents/API secrets in diagnostic traces.
- Retain accepted-transition audit evidence; duplicates do not create another accepted business transition.
- Record safe reason/correlation/remediation information for quarantined records.
- Observe request/error/latency/saturation signals and AI grounding, retrieval-empty, throttling, token and approval-backlog-age signals.
- Extraction/embedding autoscaling uses queue age and throughput.
- Alert on oldest queue age and index backlog.
- Page for user-impacting failure budgets, stale ACL propagation or missing approval enforcement.
- Routine spend anomalies create tickets with configured owner/threshold; those owner identities/thresholds are not supplied.
- During model outage, disable new generation admission, retain manual/evidence workflows, display degradation and page only when availability budget is impacted.
- Run progress is observable through API-010–012; connector history through API-019; document status through API-007; evaluation results through API-024.

**Evidence:** Source, pp. 19, 29, 55, 58, 64–66, 79, 90.

**Needs confirmation:** Batch summary schema, notification recipients/channels, success/empty/partial-failure notices, dashboard metrics, job latency SLOs, alert thresholds, sampling policy and operational retention for job histories. Appendix F `trace_sample_rate: 0.10` remains an example.

### Delayed Indexing Recovery Procedure

The following preserves Source, p. 90, §F.1:

1. **Detect:** Alert on oldest queue age/index backlog; identify affected tenant and index generation.
2. **Contain:** Pause only the faulty connector or indexer shard; preserve accepted source records.
3. **Diagnose:** Inspect event ID, outbox lag, parser flags, search throttling and source ACL revision.
4. **Recover:** Replay validated outbox records through a bounded operator-controlled job.
5. **Verify:** Compare source fingerprints with indexed versions and run denied-access probes before closing the incident.
6. **Document:** Link audit IDs, incident time window, blast radius, quality effect and preventive action.

The exact pause/replay control interfaces, scope limits and verification thresholds **Need confirmation**. API-038 specifically confirms dead-letter replay; it must not silently become an endpoint for every outbox replay scenario.

## Acceptance Criteria

### Verification Rules

Use synthetic successful, empty, mixed-permission, adversarial and malformed fixtures. Record random seeds. Critical isolation and approval tests pass with zero exceptions. Signed deployment test outputs are referenced by release digest.  
**Evidence:** Source, pp. 74, 88–89.

| ID | Job / scenario | Expected result | Traceability |
|---|---|---|---|
| AC-BAT-001 | BAT-001: accepted case and `CaseCreated` | Labels, confidence and provenance durably attached; user correction requires reason code | Source, pp. 12, 87; DAT-003; API-001/API-051 |
| AC-BAT-002 | Any event consumer: replay event 100 times, including delayed revision | Exactly one accepted business transition; duplicate outcome recorded without repeated mutation | Source, pp. 48–50, 88–89; `T-07`, `TST-007`; API-R-008 |
| AC-BAT-003 | Any tenant-owned job: substitute foreign-tenant identity / reuse pooled connection | No foreign data or mutation; non-disclosing denial; scoped session reset | Source, pp. 22–23, 86, 88; DAT-R-005 |
| AC-BAT-004 | Public long-running creation: same key/body, then changed fingerprint | Identical replay returns original operation; changed fingerprint returns `IDEMPOTENCY_CONFLICT`, no second operation | Source, p. 54; API-R-007 |
| AC-BAT-005 | BAT-002: incomplete provisioning or revoked credentials | Sync blocked while incomplete; revoked queued jobs fail `CONNECTOR_REAUTH_REQUIRED` without secret disclosure | Source, pp. 27, 78 |
| AC-BAT-006 | BAT-002: partial batch with malformed item | Poison item durably quarantined after bounded retries; remaining batch may proceed; cursor does not skip undurable preceding items | Source, pp. 28–29; AC-DAT-017 |
| AC-BAT-007 | BAT-002/BAT-008: provider 429 burst | Capped retries, honored provider delay and controlled admitted load; no quota bypass | Source, pp. 28, 69, 89; `TST-008` |
| AC-BAT-008 | BAT-003: unsafe PDF/polyglot/zipped payload | Quarantine, no indexing; scan before parsing, no macros or embedded remote fetch | Source, pp. 30, 88–89; `T-04`, `TST-015` |
| AC-BAT-009 | BAT-003: safe low-quality content / changed pipeline version | Authorized viewing retained; autonomous recommendation excludes low-quality content; new derivatives coexist without rewriting prior lineage | Source, pp. 31–32; AC-DAT-008, AC-DAT-010 |
| AC-BAT-010 | BAT-004/BAT-006: index failure after source acceptance | Source remains durable; fingerprint reconciliation/outbox repair can recover downstream work | Source, p. 49; AC-DAT-016 |
| AC-BAT-011 | BAT-005: incomplete parallel index | No read-alias activation until completeness/recall checks pass; passing rebuild switches atomically | Source, p. 34; DAT-R-012 |
| AC-BAT-012 | BAT-007: ACL revoked after indexing/cache population | Next query returns no forbidden evidence; stale visibility treated as security incident | Source, pp. 27–28, 89; `TST-004`, `T-08` |
| AC-BAT-013 | BAT-007: suspected leak remediation | Affected aliases suspended/caches revoked; search reenabled only after negative access tests pass | Source, p. 79, §22.2.2 |
| AC-BAT-014 | BAT-008: no supported evidence / missing citations | `NO_SUPPORTED_EVIDENCE` where retrieval insufficient; clarification/human path remains unresolved; no fabricated approved answer | Source, pp. 36, 89; `TST-009` |
| AC-BAT-015 | BAT-008: invalid structured model output | `MODEL_OUTPUT_INVALID`; no publication | Source, pp. 38, 89; `TST-005` |
| AC-BAT-016 | BAT-008: old approval / changed source permissions | Stale decision audited/rejected; old hash cannot publish changed artifact; publication rechecks evidence authorization | Source, pp. 45–46, 89; `TST-006`; API-R-006 |
| AC-BAT-017 | BAT-008: high-risk self-approval / arbitrary MCP tool / recursion hints | No unapproved publication; `DENY` before unauthorized tool dispatch; depth/tool budgets enforced; failed checkpoint visible | Source, pp. 11, 40–42, 88–89; `T-10`, `TST-014` |
| AC-BAT-018 | BAT-008: outage or quota exhaustion | Approved fallback constraints preserved; quota exhaustion terminal; manual case/evidence workflows remain available during generation outage | Source, pp. 37–38, 69, 79; `T-06` |
| AC-BAT-019 | BAT-009: SLA expiry | No implicit approval; reassignment/escalation recorded | Source, pp. 45, 89; `TST-010` |
| AC-BAT-020 | BAT-010: replay without reason/dry run/scope, then valid replay | Missing controls cannot authorize replay; valid replay preserves original event ID unless explicit migration provenance | Source, p. 50; API-038 |
| AC-BAT-021 | BAT-011/BAT-012: retry provisioning and historical backfill | One idempotent provisioning workflow; stable historical source IDs and per-batch receipts; readiness based on coverage, not empty queue | Source, p. 78 |
| AC-BAT-022 | BAT-013/BAT-014: held records in purge inventory | Held records retained and receipted; eligible objects tombstoned/removed; no false claim of held-object deletion | Source, pp. 80, 89; `TST-013` |
| AC-BAT-023 | BAT-013: case eligibility / diagnostic and audit retention | Case retention selects eligible closed cases only; diagnostic 30-day default and security-audit seven-year policy remain distinct | Source, pp. 26, 66 |
| AC-BAT-024 | BAT-014: single Admin export/delete attempt; properly authorized export | Single Admin insufficient; authorized export has required checksummed metadata/artifacts/references/audit manifests and excludes secrets/internal prompts | Source, pp. 78–79, 83, 88; `T-11` |
| AC-BAT-025 | BAT-015: daily attributed usage | Output contains workspace cost-center/deployment attribution, budget, forecast and rejected excess requests; numeric expected fixtures depend on approved formulas | Source, p. 65; OQ-BAT-010 |
| AC-BAT-026 | BAT-016: frozen benchmark / fixture tampering / low confidence | Required metrics/domain confidence reported; changed expected fixtures detected by version/signed manifest; low confidence or critical safety failure blocks release | Source, pp. 75–76, 88–89; `T-12`, `TST-016` |
| AC-BAT-027 | BAT-017: attempt historical audit/review modification | Historical modification denied; append-only batch-hash-chain export preserved | Source, pp. 62, 88; `T-09` |
| AC-BAT-028 | BAT-018: migration with old readers / canary regression | Compatible bounded backfill; enforcement after old replicas drain; regression rolls traffic back, not database schema automatically | Source, pp. 52, 72–73, 89; `TST-016` |
| AC-BAT-029 | BAT-019: regional restore exercise | Object/relational consistency checked together with index recipes; RPO `<=15 minutes`, RTO `<=4 hours` | Source, pp. 19, 69, 89; `TST-012` |
| AC-BAT-030 | BAT-020: outbound webhook failure | Signed retried notification; internal case transition remains committed | Source, p. 55 |
| AC-BAT-031 | All jobs: inspect diagnostics, provider requests and public failures | No user document text/API secrets in diagnostics, no undeclared secret disclosure, stable safe errors | Source, pp. 61–64, 84, 88; `T-05` |
| AC-BAT-032 | BAT-008 observation: refresh/SSE reconnect | Progress reconstructed from server state/scoped retained offsets without rerunning side effects | Source, pp. 55, 58; API-012 |
| AC-BAT-033 | Applicable jobs: dependency unavailable before/after accepted launch | Safe documented retryable error or persisted asynchronous operation identity; never ambiguous success or partial-as-approved output | Source, pp. 12–13, 48–50; API-R-004–009 |

### No-Input and Partial-Completion Decisions

The source requires empty fixtures but does not define universal empty-batch behavior.

| Scenario | Confirmed expected boundary | Needs confirmation |
|---|---|---|
| BAT-008 retrieval returns empty/insufficient support | No fabricated context; `NO_SUPPORTED_EVIDENCE`; no unsupported approval | Exact clarification-versus-human route |
| BAT-003 zero-page/no extractable text | Quality flags include empty-page ratio | Quarantine versus low-quality outcome and downstream index eligibility |
| BAT-002 no provider changes | Cursor safety and source identity requirements still apply | Empty sync status, cursor update and receipt behavior |
| BAT-006 no discrepancy / BAT-010 no selected replay records | No duplicate/unauthorized mutation | No-op completion/status/audit semantics |
| BAT-009 no expired task / BAT-013 no eligible object | No implicit approval and no ineligible purge | Empty selection outcome/notification |
| BAT-012 empty history / BAT-015 zero usage | Stable IDs/coverage and attribution requirements remain | Empty receipt/rollup representation and readiness |
| BAT-016 absent/corrupt corpus | Frozen versioned corpus and low-confidence release blocking remain required | Failure status; do not fabricate benchmark scores |
| BAT-014 inventory contains only held objects | Protected records retained and receipted | Complete-with-retention versus blocked/partial operation state |

**Evidence:** Source, pp. 28, 32, 36, 45, 75–80, 89. These gaps are tracked in OQ-BAT-013; unresolved status choices are not implementation permission.

## Consistency and Open Questions

### Conflicts and Required Amendments

Earlier specifications are not rewritten. Their identifiers and proposal statuses remain unchanged.

| ID | Affected identifiers | Evidence / conflict | Required clarification or amendment |
|---|---|---|---|
| OQ-BAT-001 | BAT-008; API-008/API-009; OQ-SF-003, OQ-API-001, OQ-DAT-006 | Source pp. 15–17 uses `POST /v1/runs`; pp. 40, 83 uses case-nested route | Resolve canonical creation/alias behavior and shared idempotency namespace before launch implementation |
| OQ-BAT-002 | BAT-008/BAT-009; OQ-SF-006, OQ-API-005, OQ-DAT-009 | Missing approval stops orchestration on p. 41; waiting state on pp. 49, 82; example 180-second timeout on p. 90 | Define valid waiting, missing-approval failure, timeout clock and recoverable representation |
| OQ-BAT-003 | BAT-011/BAT-012/BAT-014; API-025/API-026/API-056 | Source p. 78 places provisioning/backfill prose beside export/delete endpoint boilerplate | Do not treat export/delete as provisioning/backfill launch APIs; define missing contracts and event emission separately |
| OQ-BAT-004 | BAT-013/BAT-014; DAT-R-016; API-040; OQ-API-024, OQ-DAT-020 | Source p. 26 confirms routine retention of eligible closed cases; p. 78 explicitly requires two independent export/delete checks | Clarify which routine retention operations need two-person approval and how authority reaches purge workers; do not silently exempt or universally add checks |
| OQ-BAT-005 | BAT-008/BAT-010/BAT-014; API-R-003; DAT-R-004 | Chapter register events are repeated beside ordinary GET endpoints; Appendix C p. 87 gives specific consumer actions | Preserve specific event-driven behavior; do not create purge/release/publication events merely from reads |
| OQ-BAT-006 | BAT-010; API-038; SF-014; DAT-027 | Source p. 50 defines dead-letter replay; p. 90 describes validated outbox replay | Define whether a common replay mechanism covers both; API-038 is not automatically the outbox replay contract |
| OQ-BAT-007 | BAT-001; DAT-003/DAT-004; OQ-DAT-001 | Mutable case aggregate versus “immutable derivative” register wording, Source pp. 13, 24–26 | Preserve mutable case state plus immutable history; specify asynchronous classification revision/correction conflict handling |

### Operational Decisions and Dependencies

| ID | Affected requirements | Needs confirmation | Source / completed-specification dependency |
|---|---|---|---|
| OQ-BAT-008 | All jobs; inventory; BAT-R-002–003 | Exact executable/queue topology, service identities/grants, scheduler product, launch APIs/CLI, mutual-exclusion/lease/fencing scope and batch commit/acknowledgement units | Source pp. 15–22, 48–52; API OQ-API-013–014; Data OQ-DAT-013, OQ-DAT-017–018 |
| OQ-BAT-009 | BAT-002/005/006/009/012/013/015/017/019 | Schedules, timezones, catch-up/missed-run behavior, DST/calendar/cutoff rules, scan cadence, batch/window sizes and backfill ordering | Source pp. 25–28, 34, 51–52, 65, 69, 78; no exact schedules supplied; OQ-DAT-024 |
| OQ-BAT-010 | BAT-015/BAT-016/BAT-017 | Rollup formulas/prices/units/late corrections; evaluation statistical methods/partial-results policy; audit hash batch/format/acknowledgement | Source pp. 62, 65, 75–76; OQ-API-023, OQ-DAT-022 |
| OQ-BAT-011 | BAT-R-004–006; all recovery | Retry caps/delays/circuit thresholds, heartbeat/lease expiry, timeout budgets, dedup/history retention, dead-letter criteria and terminal/partial error schemas | Source pp. 28–29, 38–42, 49–50, 70, 90; OQ-API-018–019, OQ-API-026; OQ-DAT-018 |
| OQ-BAT-012 | BAT-003–007/BAT-012 | Quality/scan thresholds, MB bytes, pipeline identity, embedding deployment, index completeness/recall/coverage thresholds, concurrent delta/ACL/delete handling and readiness state | Source pp. 30–34, 49, 78, 90; OQ-API-017, OQ-API-020, OQ-DAT-015 |
| OQ-BAT-013 | Acceptance no-input table; all jobs | Empty/no-op statuses, per-item/partial completion, job summary and notification semantics; no fabricated success/score/readiness | Source p. 89 requires empty fixtures; operation results otherwise incomplete |
| OQ-BAT-014 | BAT-008/BAT-009 | Policy/reviewer catalogs, required review fields, expiry races/routing, exact-artifact hash canonicalization, publication trigger and admission quotas versus reference capacity | Source pp. 40–46, 58, 68–69; OQ-API-018, OQ-API-021, OQ-DAT-016 |
| OQ-BAT-015 | BAT-011/BAT-013/BAT-014/BAT-019 | Provisioning compensation; approved retention/hold controls; inventory/manifest/checksum schema; concurrent hold enforcement; shared-source/backup purge treatment; export status/download and deletion verification | Source pp. 26, 51, 66, 78–80, 90; OQ-API-024, OQ-DAT-020 |
| OQ-BAT-016 | BAT-018/BAT-019 | Migration-specific transforms/backfill/rerun rules, canary gates, supported data compensation, backup retention/provider/region and restore order/exercise cadence | Source pp. 19–20, 52, 69–73; OQ-API-025, OQ-DAT-023 |
| OQ-BAT-017 | BAT-020; BAT-R-006 | Optional webhook enablement, destination/signature/event-age/attempt limits; job notification recipients/channels; metric labels, ticket/page routes and thresholds | Source pp. 55, 64–66, 79, 90; OQ-API-019, OQ-API-023 |
| OQ-BAT-018 | All jobs; supporting functions | Approved region/search/identity/model deployments/corporate retention/provider permissions; per-tenant key isolation and whether rotation requires application batch processing | Source pp. 10, 63, 90, §F.2; OQ-SF-021–022, OQ-API-027, OQ-DAT-021–023 |

### Completed and Later Specification Dependencies

- [01_screen_functions.md](01_screen_functions.md): Preserve SCR-002 document/run operations, SCR-004 persisted progress, SCR-005 expiry, SCR-006 sync/readiness, SCR-010 usage/evaluation and SF-014 replay/export/delete behavior. Batch IDs do not confirm new screens or buttons.
- [02_api.md](02_api.md): Preserve all referenced API paths, authorization profiles, idempotency and error contracts. Unresolved job arguments must be finalized through controlled IDL, not inferred from these procedures.
- [03_data.md](03_data.md): Preserve immutable source/approval history, tenant RLS, outbox/dedup, retention classes, held-record receipts and canonical selected field names. This document does not add physical job tables.
- Exception handling and further operational/architecture details are **To be defined in a later stage**: carry forward retry classification, timeouts, safe errors, partial failure, compensation, concurrency and recovery decisions.
- `08_architecture_decision.md` is **To be defined in a later stage**. Consolidate open decisions from completed Markdown specifications with links to `04_batch_functions.md`, affected `BAT-*`, `BAT-R-*`, `AC-BAT-*`, `OQ-BAT-*` and earlier IDs.

No owner identity, deadline or approval is supplied for these unresolved decisions. Missing schedules, limits, schemas and recovery mechanisms must be explicitly decided rather than silently selected by the implementation AI.
