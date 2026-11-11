# 5. Business Rules

## Rule Inventory and Scope

### Baseline and Evidence Status

This specification consolidates shared business conditions for OrionDesk AI **OD-AI-DDS-001, R1.0 / revision 1.3** across the completed screen, API, data and batch specifications.

**Source** means `1794310747-OrionDesk_AI_Detailed_Design_Specification.pdf`. All citations below refer to original PDF pages and sections.

- **Confirmed:** Explicitly supported requirements for this fictional baseline.
- **Needs confirmation:** Missing conditions, schemas, thresholds or conflicting requirements. These are unresolved decisions, not permission to choose an implementation.
- **Proposal:** Suggested design only. Earlier proposals remain proposals.

`BR-*` identifiers are assigned here because the source does not provide individual business-rule identifiers. Source identifiers such as `TST-001`, `T-03` and `SEC-001` through `SEC-012` are preserved for traceability; they are not renamed as business rules.

The rules apply throughout the stated baseline. Calendar effective dates, future-dated activation, policy supersession and policy selection for already-running operations **Need confirmation**. Configurable numeric thresholds must be versioned policy rather than untracked constants (Source, p. 9, §1.2.2).

### Rule Inventory

All inventory requirements are **Confirmed**, with unresolved implementation details identified in subsequent sections.

| Rule ID | Name and purpose | Applicable targets | Actors and permission boundary | Timing | Evidence |
|---|---|---|---|---|---|
| BR-001 | Authenticated resource access — prevent unauthorized operations | All screens, APIs, resources and jobs | Authenticated principal/service; role, tenant, membership, sensitivity, ACL, action and segregation of duties | Every request; domain reevaluation within mutation transaction | Source, pp. 21–23, §§5.1–5.3 |
| BR-002 | Tenant isolation and nondisclosure | Tenant-owned rows, objects, events and responses | Immutable authorized tenant context; no cross-tenant substitution | Every storage access, job execution and response | Source, pp. 22–23; pp. 51, 86 |
| BR-003 | Revision-safe configuration and case mutation | Workspace configuration and cases | Authorized configuration manager or case Owner; precise scopes unresolved | Before accepted mutation | Source, pp. 24–25, §§6.1–6.2 |
| BR-004 | Idempotent creation and event processing | Case creation, long-running POST creation, cross-service writes and consumers | Authorized original actor/service; replay does not extend authority | Creation, retry, duplicate or delayed delivery | Source, pp. 15–17, 25, 48–50, 54 |
| BR-005 | Durable transition integrity | Mutations, checkpoints, outbox, asynchronous integrations | Authorized domain services and workers | Commit and downstream dispatch | Source, pp. 17, 49, 52, 56 |
| BR-006 | Case classification and correction | New cases and classification history | Classifier; user correction requires reason code; correction permission unresolved | Asynchronous creation processing and correction | Source, p. 12, §2.2.1 |
| BR-007 | Explicit case transitions | Case aggregate and revisions | Role, revision and approval guards | Every state change | Source, pp. 25, 82, 86 |
| BR-008 | Impact/urgency-derived priority | Case priority | Authorized case mutation; model output alone insufficient | Priority calculation; recalculation triggers unresolved | Source, p. 25, §6.3.1 |
| BR-009 | Contractual business-calendar deadlines | Case deadline and advisory breach prediction | Domain calculation under workspace calendar | Deadline calculation and prediction | Source, pp. 25, 59 |
| BR-010 | Immutable closure lineage | Approved answer, source versions and decisions | Closure permission unresolved | Case closure and explicit reopen | Source, pp. 24–26 |
| BR-011 | Provisioning and source-readiness gates | Workspace onboarding, sync and historical backfill | Provisioning identity unresolved; Admin starts sync | Before sync and readiness declaration | Source, p. 78, §22.1 |
| BR-012 | Connector trust, credentials and cursor safety | Connectors, sync outcomes and cursors | Admin starts sync; operators revoke scoped credentials | Discovery, queued execution, item completion and cursor advance | Source, pp. 27–29 |
| BR-013 | Immediate authorization revocation and deletion visibility | Evidence, indexes, caches and source tombstones | Current source ACL and authorized incident operators | Before next retrieval; publication recheck | Source, pp. 27–28, 46, 51, 53, 79 |
| BR-014 | Safe accepted-file processing | Attachments and extraction | Analyst upload; scoped ingestion worker | Admission, scan and parsing | Source, pp. 30–32 |
| BR-015 | Immutable provenance and extraction quality | Document versions, chunks, OCR and anchors | Authorized viewers; autonomous selection subject to quality | Extraction, reprocessing, citation selection | Source, pp. 31–32 |
| BR-016 | Grounded bounded retrieval | Queries, evidence sets and citations | Member/search authorization; Research Agent scoped retrieval | Retrieval, model text release and citation display | Source, pp. 34–36, 87 |
| BR-017 | Approved model route and constrained fallback | Model deployments and provider context | Workspace deployment allowlist and data-handling policy | Each model invocation/fallback | Source, pp. 37–38 |
| BR-018 | Untrusted model/evidence boundary | Prompts, model output and tools | Model text and evidence have no authorization authority | Prompt construction, output parsing and tool dispatch | Source, pp. 7, 38–39, 61 |
| BR-019 | Bounded authorized agent execution | DAG, capabilities and A2A tasks | Separate invoking-principal/capability authorization; human authorization if consequential | Planning, dispatch, retry and stop checkpoint | Source, pp. 40–42, 87 |
| BR-020 | Admission and token-budget control | AI runs, quotas and capacity | Authorized Analyst plus workspace/provider admission | Before run admission and during usage | Source, pp. 38, 69 |
| BR-021 | Deterministic reproducible policy | Policy evaluations and review requirements | Deterministic Policy Service; LLM cannot override | After candidate generation and applicable reevaluation | Source, pp. 40, 44–46 |
| BR-022 | Eligible, inspectable, exact-artifact review | Review tasks and immutable decisions | Eligible Reviewer, minimum role, pool and separation of duties | Before decision acceptance | Source, pp. 11, 45, 57–58, 85 |
| BR-023 | Review expiry, appeal and rework | Expiring tasks, overrides and denied revisions | Policy routing; override requires elevated role and secondary reviewer | SLA expiry, override and rework | Source, pp. 45–46 |
| BR-024 | Atomic controlled publication | Final response pointer and PublicationGate | Satisfied evidence, policy, authorization and required approval | Publication transaction, including replay | Source, pp. 11–13, 45–46 |
| BR-025 | Retention eligibility and legal-hold protection | Closed case data, diagnostics, audit and purge inventory | Authorized retention/deletion scope; holds override eligible removal | Retention selection and deletion | Source, pp. 26, 51, 66, 80 |
| BR-026 | Two-person export and verified deletion | Workspace export/delete and receipts | Admin + approver; two independent checks | Before controlled operation; verification at completion | Source, pp. 78–80, 83, 88 |
| BR-027 | Privacy, secrets and immutable audit | Provider calls, logs, public responses and audit | Declared secret scope; Auditor redacted read; no historical edits | Extraction, invocation, response and audit retention | Source, pp. 21, 27, 54, 61–64, 84 |
| BR-028 | Daily usage attribution and actionable alerts | Usage rollups, budgets, forecasts and alerts | Admin usage read; operational alert routing | Daily aggregation and incident detection | Source, pp. 64–66, 79 |
| BR-029 | Safe degraded operation and controlled recovery | Generation/search degradation, rebuild and regional recovery | Authorized incident command and scoped operators | Dependency outage, leak containment, rebuild and restore | Source, pp. 19, 34, 49, 68–70, 79–90 |
| BR-030 | Controlled replay and failure recovery | Dead letters and transient failures | Operator reason, dry run and scope limit | Retry/replay; no retry of permanent denial | Source, pp. 49–50 |
| BR-031 | Quality and security release gates | Evaluations, migrations and production promotion | Admin evaluation; Security/SRE and security-control review | Before promotion and on model/prompt change | Source, pp. 71–76, 88–89 |
| BR-032 | Truthful, accessible observation | Artifact status, evidence inspection, SSE and local time | Authorized viewer/reviewer; client controls are not security boundaries | Display, refresh and reconnect | Source, pp. 54–59 |
| BR-033 | Controlled baseline and prohibited capabilities | Baseline changes and system scope | Approved change record; agents cannot exceed exclusions | Design change and every attempted excluded operation | Source, pp. 8–10 |

## Decisions, Calculations, and State Transitions

### Shared Prerequisites and Conflict Handling — BR-001–005

1. Authenticate the principal and establish authorized tenant, actor, trace and correlation context.
2. Validate payloads before transaction entry, again at domain invariants and before tool dispatch.
3. Reject broad policy violations at the edge.
4. Resolve resources using tenant predicates and current resource attributes.
5. For mutations, reevaluate authorization, state guards and revision preconditions inside the transaction.
6. Apply idempotency and replay safeguards.
7. Commit accepted state and required outbox records atomically; persist workflow checkpoints before downstream dispatch.
8. Return confirmed acceptance/completion or safe documented failure, never ambiguous success.

**Confirmed:** Rejected stale or unauthorized writes leave business state unchanged and do not emit an accepted-transition event. Safe denied-attempt audit evidence may still be retained. Client-side validation and hidden navigation controls do not establish permission.

**Needs confirmation:** Exact ordering of idempotency lookup versus revision checking, locking/isolation, concurrent request winner, missing-precondition errors and policy changes during an in-flight operation. No global rule-order algorithm is supplied.

| Condition | Required result | Rule |
|---|---|---|
| Token algorithm unexpected or tenancy claim missing | Reject protected processing | BR-001 |
| Role allowed but workspace, sensitivity, ACL, action or segregation predicate fails | Do not authorize the action from role alone | BR-001 |
| Foreign-tenant resource ID supplied | Same not-found response class as absent ID; no existence disclosure | BR-002 |
| Case workspace belongs to another tenant | Reject mutation; enforce workspace-tenancy membership | BR-002 |
| Case `If-Match` mismatches current revision | `409 CASE_VERSION_CONFLICT`, current revision; no business mutation | BR-003 |
| Configuration revision precondition fails | No configuration mutation; exact response contract unresolved | BR-003 |
| Same creation key and identical fingerprint | Return original outcome/operation; no duplicate creation | BR-004 |
| Same creation key and changed fingerprint | `IDEMPOTENCY_CONFLICT`; case test requires HTTP `409` | BR-004 |
| Duplicate event or stale aggregate revision | Record duplicate/stale handling without reapplying business mutation | BR-004 |
| Failure of required business/outbox transaction | No partial accepted transaction; safe error or recoverable persisted operation | BR-005 |
| Index write fails after accepted source metadata | Preserve accepted metadata; reconcile source fingerprints and outbox links | BR-005 |

Case idempotency binds **actor + request fingerprint to one outcome for 24 hours**. Namespace, expiration equality, unsuccessful/in-flight outcome retention and post-expiry behavior **Need confirmation**. Do not apply this period universally to batch deduplication.

Every tenant-owned storage access includes tenant identity; tenant-owned rows require `tenant_id`, background envelopes carry signed immutable tenant identity, and pooled scoped variables are reset after each transaction. Business-key uniqueness is tenant-scoped except explicitly supplied constraints such as `tenants.unique(slug)`.

**Evidence:** Source, pp. 17, 21–25, 48–56, 85–89.

### Case Decisions — BR-006–010

#### Classification and Defaults

- Create cases in `NEW`.
- Asynchronous classification attaches labels, confidences and provenance.
- User correction requires a reason code.
- `cases.revision` has storage default `1`; revision is monotonic.
- `cases.sensitivity` has storage default `'INTERNAL'`; this does not settle browser creation-field defaulting.

**Needs confirmation:** Label vocabulary, confidence bands, correction permissions, classification/correction race, owner assignment and automatic transition triggers.

#### Case Transition Table

Each supported transition remains subject to role, revision and approval guards. The table does not declare that every authorized user may execute every transition.

| Current state | Supported next state | Result or missing condition |
|---|---|---|
| `NEW` | `TRIAGED` | Explicit transition supported |
| `TRIAGED` | `IN_PROGRESS` | Explicit transition supported |
| `IN_PROGRESS` | `PENDING_APPROVAL` | Explicit transition supported |
| `IN_PROGRESS` | `RESOLVED` | Explicit transition supported; exact approval guard unresolved |
| `PENDING_APPROVAL` | `RESOLVED` | Explicit transition supported; required gate must be satisfied |
| `PENDING_APPROVAL` | `IN_PROGRESS` | Explicit return to work supported |
| Predecessor unspecified | `CLOSED` | Closure exists, but predecessor/role/guard Need confirmation |
| `CLOSED` | Explicit reopen as new revision | Preserve closed lineage; target state and contract Need confirmation |
| Any state | Other transition | Not established by the source; requires confirmation before implementation |

#### Priority and Deadline Calculations

| Calculation | Confirmed inputs and result | Formula, units, rounding and boundary gaps |
|---|---|---|
| Priority | Explicit impact and urgency determine priority; never model output alone | Impact/urgency catalogs, matrix, missing values, tie handling, overrides and recalculation triggers Need confirmation |
| Contractual deadline | Workspace business calendar and timezone calculate deadline | SLA duration, start event, business hours, holidays, pauses, DST, inclusive endpoints and timestamp precision Need confirmation |
| Breach prediction | Advisory prediction | Cannot modify contractual deadline; algorithm/confidence and display rules Need confirmation |
| Closure snapshot | Approved answer, cited immutable document versions and reviewer decisions | Snapshot schema, closure atomicity and handling of no approved answer Need confirmation |

No numeric priority weights or SLA formula are confirmed.

**Evidence:** Source, pp. 12, 24–26, 59, 82, 85–86.

### Onboarding, Connector and Document Decisions — BR-011–015

| Condition / input | Required result | Open decision |
|---|---|---|
| Provisioning incomplete | Visible incomplete state; block connector sync | Completion predicate and compensation |
| Historical backfill | Bounded windows, stable source IDs, per-batch reconciliation receipts | Window boundaries, ordering and sizes |
| Queue empty but index coverage inadequate | Queue emptiness alone cannot prove search readiness | Coverage formula and threshold |
| Connector lacks advertised capability | Lower-trust ingestion and explicit visible warning | Permitted uses and trust-mode policy |
| Credentials revoked | Queued jobs fail `CONNECTOR_REAUTH_REQUIRED`; no token disclosure | Reauthorization and requeue behavior |
| Preceding sync item lacks durable outcome | Do not advance cursor past it | Item ordering/concurrent cursor ownership |
| Malformed source after bounded retries | Quarantine with reason, correlation ID and remediation path; remaining batch may proceed with durable exception | Retry classification and partial-completion status |
| Source deleted | Tombstone; schedule index removal; soft-deleted data not retrievable | Hold/reference-retention interaction |
| ACL revoked | Invalidate affected cache before new result/next retrieval, not merely at TTL expiry | Detection latency and race-safe invalidation |
| File type unsupported or MIME signature/extension disagree | Do not accept as a supported file; fail closed | Error/status and quarantine classification |
| Unsafe file | Scan before parsing; quarantine, never index | Scanner/parser limits |
| Safe supported file | Preserve layout, tables, reading order and source anchors | Parser schema and empty-document result |
| OCR not opted in | Do not invoke opt-in OCR fallback | Configuration capture/default |
| Low extraction quality | Authorized viewing retained; exclude autonomous recommendations | Thresholds and manual-review policy |
| Pipeline version changes | New immutable derivatives may coexist; normalization must not rewrite claims | Identity/fingerprint mapping |

Supported input formats are **PDF, DOCX, HTML and UTF-8 text**. The source specifies a **configurable 25 MB per-file cap** and a decompression-bomb threshold. Exact MB bytes, equality-at-cap behavior, decompression metric/cutoff, total attachment limits and zero-byte handling **Need confirmation**.

Every chunk stores source URI, file hash, page number and optional bounding box. A citation requires both a resolvable stored anchor and current access permission. The extraction quality inputs are empty-page ratio, unknown-character ratio, table-loss indicators and language confidence; their formulas, scales and aggregation are not supplied.

**Evidence:** Source, pp. 27–32, 51, 53, 78.

### Retrieval, Model and Agent Decisions — BR-016–020

#### Retrieval Selection

1. Form lexical and normalized vector queries.
2. Retrieve bounded candidate sets.
3. Merge using reciprocal rank fusion and deterministic reranking.
4. Limit redundant same-document hits and preserve relevant-source diversity.
5. Apply returned-token budgets and ACL filtering before text reaches generation.
6. Return evidence containing chunk ID, source title, document revision, page anchor and ACL digest.
7. Verify opaque citation identifiers before display.
8. Return `NO_SUPPORTED_EVIDENCE` when confidence or evidence quality is insufficient; never fabricate context.

**Needs confirmation:** Exact fusion formula/configuration, rank tie handling, diversity algorithm, token-counting rules, confidence/quality cutoffs and clarification-versus-human routing.

The baseline searchable derivative uses **1536-dimensional embeddings**. `knowledge.search@v1` is read-only, requires tenant-scoped `read:permitted_documents`, disallows arbitrary URLs/filesystem access, and defines `max_items: int<=10`. Requiredness and lower bound **Need confirmation**.

#### Model and Execution Decision Table

| Condition | Required result |
|---|---|
| Deployment is not specifically allowed by workspace policy | Do not infer approval from provider brand |
| Fallback deployment/region unapproved or data-handling class weaker | Do not route content there, including during outage |
| Approved fallback preserves or strengthens data-handling class | Fallback is permitted subject to other applicable controls |
| Evidence contains tool directives/system instructions | Keep as untrusted data, strip evidence-context tool-call directives and record injection indicators |
| Model output has unknown fields, invalid citations or control-character injection | Bounded validation retries; final `MODEL_OUTPUT_INVALID`, no publication |
| Agent/tool discovered but capability not independently authorized | Deny before dispatch |
| External write requested | Separate capability authorization; consequential mutable operations also require human authorization and idempotency |
| Denied action has semantically equivalent alternative tool | Planner must not substitute the equivalent action |
| A2A receiver declines | Decline is allowed; response/status mapping unresolved |
| DAG has cycle or exceeds permitted depth | Do not execute as a valid bounded DAG |
| Tool-call budget exhausted, repeated invalid plans, policy denial or deadline expiry | Stop and expose exact failed checkpoint |
| Required approval missing at execution checkpoint | Stop condition applies; distinction from valid human waiting unresolved |
| Workspace/provider admission predicate unsatisfied | Throttle new run: HTTP `429` plus `Retry-After`; saved cases remain available |
| Current-run quota exhausted | Terminal for that run; no automatic model/data-class switching |

Plan depth is bounded to **eight**; tool invocations are bounded to **sixteen**. Counts at the maximum are within the stated maxima; exceeding them is prohibited. Depth-counting convention and whether retries consume additional tool-call budget **Need confirmation**.

Each run reserves input/output token budget and records provider usage under workspace quota. Admission depends jointly on workspace tokens, queue age and provider capacity. Reservation calculation, quota units/reset, concurrency limits and exact threshold equality **Need confirmation**.

Prompts include fixed rules, signed workflow instruction, validated user input and separately delimited evidence. Neither evidence nor LLM output may authorize tools, change tenant, alter approvals or override deterministic policy.

**Evidence:** Source, pp. 7, 34–42, 69, 87–90.

### Policy, Review and Publication — BR-021–024

#### Policy Input Definitions

| Input | Confirmed meaning | Missing definition |
|---|---|---|
| Case sensitivity | Information classification relevant to decision | Propagation and reclassification rules |
| Requested action | Action being evaluated | Action vocabulary and consequential-action criteria |
| Evidence quality | Support quality | Metrics/cutoffs and absent-evidence behavior |
| Model class | Model policy classification | Class catalog and comparison |
| Financial impact category | Impact category for risk | Currency, category bands and boundaries |
| Confidence bands | Normalized confidence categories | Source of confidence, thresholds and rounding |
| Rule-set version | Reproducible decision version | Activation, precedence and in-flight version selection |

Normalize and store all inputs with the rule-set version; an input digest alone does not replace stored inputs. LLM risk tags are proposals to policy, not binding outcomes.

The maximum information class of material included in a run governs model route, log redaction, retention and approval policy. Literal classes are `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`; class-comparison representation and missing/unknown-class behavior **Need confirmation**. `HIGH_RISK` is not an additional information-class value.

#### Policy Outcomes

| Deterministic result | Confirmed consequence / gate boundary | Needs confirmation |
|---|---|---|
| `AUTO_ALLOW` | Policy outcome exists; still requires evidence and current authorization for publication | Complete eligibility predicate and auto-allow workflow path |
| `HUMAN_REVIEW` | Required eligible review before publication | Routing priority, reviewer counts and required fields |
| `REQUEST_MORE_EVIDENCE` | Existing evaluation does not establish sufficient publication readiness | Evidence request mechanism and next state |
| `DENY` | Stop denied execution; never relabel old denial as approved | Denial reason catalog and appeal routing |

The source does not supply the full input-to-outcome decision matrix, overlapping-rule precedence or default outcome. These must be approved before implementing policy evaluation.

#### Review and Publication Decisions

| Condition | Required behavior |
|---|---|
| High-risk run lacks required approval | Never publish |
| Analyst attempts approval of own high-risk recommendation | Deny |
| Review-task segregation-of-duties predicate fails | Deny; `approval_tasks` carries no-self-approval constraint |
| Reviewer lacks pool/minimum-role eligibility | Do not accept decision |
| Required review fields incomplete | Disable both Approve and Reject; validate server-side |
| Reviewer opens task | Exact artifact, source citations, model/prompt version and policy reasons must be inspectable |
| Decision submitted for changed/wrong artifact hash | Reject as stale and audit; HTTP `409` supported |
| Valid decision accepted | Store decision, authenticated actor, timestamp, exact hash, rationale and optional annotations immutably |
| Task SLA expires | Reassign or escalate; never implicitly approve |
| Override requested | Require elevated role, secondary reviewer and audited reason |
| Denied draft reworked | New run revision; preserve historical denial |
| Evidence ACL changes after search/review | Publication recomputes current authorization and rejects stale evidence |
| Old approval replayed against different artifact | Never publish different content under old approval |
| Evidence, policy, current authorization and applicable approvals satisfied | Atomically record satisfied gate and update final response pointer |
| Decision accepted but publication not completed | Do not represent decision acceptance as publication success |

Rationale is stored, but exact form mandatory-field rules, annotations schema, decision request literals, artifact hash algorithm/canonicalization, approval validity period and repeated-decision behavior **Need confirmation**. No requirement to prove that a reviewer clicked every citation is supplied; source inspection capability is required.

**Evidence:** Source, pp. 11–13, 44–46, 57–58, 85, 89.

### Retention, Export, Privacy and Period-End Processing — BR-025–028

#### Retention and Export/Deletion

| Condition | Required result |
|---|---|
| Case not closed or not retention-eligible | Routine case-data retention job must not select it |
| Retention-eligible record protected by legal hold | Retain and receipt the protected record/exception |
| Single Admin attempts workspace export/delete | Cannot satisfy two-person controls |
| Authorized export has two independent checks | Package case metadata, approved artifacts, source references and checksummed audit manifests |
| Export includes secrets/internal model prompts | Exclude those items |
| Authorized eligible deletion | Tombstones, blob/index removal and auditable completion receipts |
| Soft-deleted object remains in index/cache | Do not make it retrievable |
| Inventory contains held and removable objects | Preserve held objects and receipt exceptions; final partial-retention status unresolved |
| Data subject access request | Use same inventory; identity verification and response rules unresolved |

Routine retention approval requirements versus workspace export/delete two-person controls **Need confirmation**. No mandatory export-before-delete sequence is confirmed.

| Periodic/effective-period item | Confirmed period | Needs confirmation |
|---|---|---|
| Case idempotency outcome | 24 hours | Start clock, expiration equality and post-expiry reuse |
| Diagnostic logs | Default TTL 30 days | Clock, covered data, policy overrides and hold exceptions |
| Security audit logs | Distinct seven-year policy | Calendar-year arithmetic, retention start and lawful exceptions |
| Review SLA | Configured expiry | Duration, start/pause clock, business versus elapsed time and expiry race |
| Usage rollup | Daily | Day timezone, inclusive endpoints, late usage and correction handling |
| API availability target | 99.9% monthly | Measurement denominator, exclusions and monthly timezone |
| Final tombstone purge | Scheduled | Cadence and cutoff selection |
| Corporate case-data retention | Not supplied | Classes, periods and eligible-date calculation |

No accounting month-end/year-end close, invoices, taxes, payment settlement or financial posting rules are described. Their business requirements **Need confirmation**; irreversible financial transactions are explicitly excluded under BR-033.

#### Privacy and Audit

- Extraction tags likely personal data; redact nonessential fields before provider invocation where policy permits.
- Secrets remain in vault-backed scoped references; service credentials rotate automatically.
- Encryption-key rotation follows defined policy without bulk reencryption in the request path.
- Public fields, failures and diagnostics must not disclose raw credentials, unauthorized existence, full retrieved documents or full prompts.
- Traces contain identifiers, policy outcomes, token counts and digests, not user documents/API secrets.
- Audit is append-only, batch-hash chained and exported to independently controlled retention storage.
- Auditors receive decision metadata, prompt-template digests and access events within redacted scope, without editing case content.
- Historical review decisions cannot be altered.

PII classification/redaction, audit hash batching and exact rotation schedules **Need confirmation**.

#### Usage and Alerts

Model invocations, embeddings, storage and indexing usage carry workspace cost centers and model deployment versions. Daily rollups show budget, forecast and rejected excess requests.

**Needs confirmation:** Monetary formula, price versions, currency, rounding, units, aggregation grain, quota reset, late-provider corrections and zero-usage representation. Do not invent `cost = tokens × price` as the complete confirmed billing rule.

Pages are reserved for user-impacting failure-budget incidents, stale ACL propagation or missing approval enforcement. Routine token-spend anomalies create tickets with configured owner and threshold; actual owner/threshold values are not supplied. During provider outage, page on-call only when availability budget is impacted.

**Evidence:** Source, pp. 26, 51–55, 62–66, 78–80, 83–89.

### Recovery, Release and Observation — BR-029–033

#### Recovery and Release Procedures

1. During generation outage, disable new generation admission while preserving authorized manual case/evidence workflows and visible degradation.
2. Lexical retrieval may continue when vectors degrade, with visible reduced-quality flag; authorization and approval still apply.
3. For suspected ACL leak, suspend affected aliases, revoke cached evidence, preserve audit and replay scoped ACL revisions. Reenable only after negative access tests pass.
4. Rebuild indexes in parallel; switch read alias atomically only after completeness and recall checks.
5. Retry transient faults using bounded exponential backoff, jitter and per-dependency circuit breakers. Do not retry validation/permission failures.
6. Dead-letter replay requires operator reason, dry-run validation and scope limit; preserve original event ID unless schema migration has explicit provenance.
7. Restore warm-region snapshots only under incident command; persistent R1 writes target primary region.
8. Release only verified image digests from allowed build identity with signed configuration, SBOM and required test evidence.
9. Apply backward-compatible expansion, bounded backfill and constraint enforcement after old replicas drain. Do not remove fields still used by active readers.
10. Compare canary latency, errors, authorization denials and AI-quality regression against baseline. Regression triggers traffic rollback, not automatic database down-migration.
11. Security and SRE validate egress, secrets, backups and alert routing before promotion; release record binds image digest, schemas, prompts and routing policy.
12. Security-control review independently reproduces negative tests and signs release evidence. Unmitigated critical isolation/approval-bypass findings block promotion regardless of benchmark quality.

#### Confirmed Numeric Gates and Boundaries

| Measure | Confirmed target or limit | Boundary / calculation qualification |
|---|---|---|
| Evaluation corpus | 1,200 synthetic permission-controlled cases | Frozen, versioned, independently reviewed; expected citations/outcomes stored |
| Citation precision | `>=0.97` | Equality meets numeric target; scoring formula/aggregation/rounding unresolved |
| Unsupported-claim rate | `<=0.02` | Equality meets numeric target; denominator/claim definition unresolved |
| High-risk policy recall | `1.00` on frozen safety suite | Cannot excuse critical approval/isolation failure |
| Critical isolation and approval tests | Zero exceptions | Any critical exception blocks release |
| Statistical confidence | Low confidence blocks release | Confidence method and cutoff unresolved |
| Case-create P95 | Within/under 300 ms | Strict equality conflict unresolved |
| Search P95 | `<1.5 s`, excluding remote connector fetch | Model latency measured separately |
| Recovery RPO | `<=15 minutes` | Equality within reference target; measurement procedure unresolved |
| Recovery RTO | `<=4 hours` | Equality within reference target; measurement procedure unresolved |

The reference workload is 2,000 daily active users, 60 requests/s steady, 180 requests/s burst, 100,000 indexed documents per tenant and 20 concurrent AI runs per large tenant. These are reference capacity assumptions, not automatically per-user quotas.

Prompt/model changes require reevaluation. Tests use synthetic successful, empty, mixed-permission, adversarial and malformed fixtures; randomized tests record seeds. The minimum release test pack includes unit/schema-evolution/authorization/replay/sync/accessibility/search-recall/grounding/policy-recall/load/recovery verification, with signed outputs linked to release digest.

#### Observation and Exclusions

- Artifact text states are `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED`; these do not replace separate case/run/document/review state models.
- Refresh reconstructs server progress; SSE increasing offsets and `Last-Event-ID` backfill remain currently authorized observation, not business replay.
- Optional webhooks are signed and retried; recipient checks signature/event age. Failure cannot roll back internal transition.
- UI supports WCAG 2.2 AA target behavior, keyboard ordering, visible focus and meaningful live announcements.
- Durable/server time is UTC; API time uses RFC 3339; local display carries timezone. Locale does not change ordering or durable representation.
- Baseline changes require an architecture-decision record, impact scores for behavior/migration/threat/cost and negative tests for revised invariants. Approved changes increment minor revision; incompatible protocols increment major revision.
- Physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing and agent cloud-admin grants are **Out of scope**, explicitly excluded in Source, p. 9, §1.2.1.
- Multilingual OCR beyond English, customer-managed weights and cross-region active/active mutation are deferred in this baseline.
- No public datastore; orchestrator has no direct database credentials; only declared worker egress is allowed. Production data is forbidden in development; staging uses synthetic data/test connectors.

**Evidence:** Source, pp. 8–10, 18–20, 34, 49–59, 68–76, 78–90.

## Application Points and Validation Conditions

### Enforcement and Data Mapping

Mappings reference existing identifiers; they do not introduce new endpoints, jobs, screens or physical columns. Screen indications are presentation/application points, not independent security enforcement.

| Rule | Screens / API enforcement | Batch enforcement | Data read or updated |
|---|---|---|---|
| BR-001 | All `SCR-*`; all applicable `API-*`, AUTH-P/I/T, API-R-001 | All tenant-owned jobs, BAT-R-001–002 | DAT-019 membership/ACL/principal; resource attributes |
| BR-002 | All resource APIs; SF-007, API-R-010–012 | All jobs, BAT-R-001 | All tenant-owned records; DAT-001–003; scoped session context |
| BR-003 | SCR-002-E02, SCR-007-E01; API-004, API-050 | Domain mutations in applicable jobs | DAT-002 policy/configuration; DAT-003 `revision`; DAT-004 history |
| BR-004 | SF-015; API-001, 006, 008–009, 018, 023, 025–026; API-R-007–008 | BAT-001–020 as applicable; BAT-010 | DAT-027 outcome/dedup ledger; DAT-014 event revision |
| BR-005 | API-R-004–009; mutation APIs | BAT-006, 008, 010, 020; BAT-R-003–005 | DAT-003–004, 009, 012, 014, 026 |
| BR-006 | SCR-002-F11–F13/E03; API-051 | BAT-001 | DAT-003–004 labels/confidence/provenance/reason |
| BR-007 | SCR-002-F07/E02/E06; API-004–005, 057 | BAT-001/008 applicable domain changes | DAT-003 `status`, `revision`; DAT-004 |
| BR-008 | SCR-002-F03–F05; API-001/004 | BAT-001 only if authorized calculation is assigned | DAT-003 impact, urgency, priority |
| BR-009 | SCR-002-F17, SCR-007-F07; case/configuration APIs | Prediction batch implementation unresolved | DAT-002 calendar/timezone; DAT-003 deadline |
| BR-010 | SCR-002-E06/E07; API-005/057 | Closure batch implementation unresolved | DAT-026 snapshot; DAT-006, 012 cited lineage |
| BR-011 | SCR-006-F07–F08; API-018/056 | BAT-011–012 | DAT-001–002, 019, 021, 029, 034 |
| BR-012 | SCR-006; API-018–019, 048, 055 | BAT-002 | DAT-015 `cursor`, `watermark`, `retry_state`; DAT-021 |
| BR-013 | SCR-003/SCR-005; API-013–017, 028, 054 | BAT-007/008 | DAT-005/019 ACL; DAT-023 aliases; DAT-028 cache |
| BR-014 | SCR-002-E04; API-006–007 | BAT-003/004 | DAT-006/020/022 source and scan state |
| BR-015 | SCR-003-F03–F09; API-007/014/054 | BAT-003/004 | DAT-006–007 anchors/fingerprints; DAT-022 quality/OCR |
| BR-016 | SCR-003; API-013–015/045 | BAT-008 | DAT-007/010/023 evidence and query |
| BR-017 | SCR-007-F02; API-020/036/049 | BAT-008 | DAT-002 allowlist; DAT-024 registry/provenance |
| BR-018 | SCR-004-E05; API-036/045–046 | BAT-008 | DAT-024 candidate/injection indicators; DAT-025 |
| BR-019 | SCR-004; API-008–011/045–046 | BAT-008 | DAT-008 plan/budget; DAT-009 checkpoints; DAT-025 capability/task |
| BR-020 | SCR-002-E05/SCR-010; API-008–009/036/042 | BAT-008 | DAT-002 quota; DAT-016 usage; DAT-031 admission |
| BR-021 | SCR-002-F20/SCR-005-F06; policy boundary related to API-017 | BAT-008 | DAT-017 normalized inputs, `rule_version`, `result` |
| BR-022 | SCR-005-E01–E02; API-016–017 | BAT-008 | DAT-011 task/hash/pool; DAT-012 decision; DAT-024 exact artifact |
| BR-023 | SCR-005-E03–E04/SCR-002-E07; API-052–053 | BAT-009/008 | DAT-011 assignment/expiry; DAT-008 revisions; DAT-012 history |
| BR-024 | SCR-002/SCR-005; API-R-006 | BAT-008; `ApprovalDecisionRecorded` consumer | DAT-010/012/017/026 evidence, decisions and final pointer/gate |
| BR-025 | SCR-007-F01; API-029/040 | BAT-013/014 | DAT-003 closed status; DAT-029 holds; DAT-018 receipts |
| BR-026 | SF-014; API-025–026 | BAT-014 | DAT-034 manifest/package; DAT-018 receipts; DAT-029 holds |
| BR-027 | SCR-008; API-021 and all output/provider boundaries | All jobs; BAT-003/008/017 | DAT-013 audit; DAT-029 keys/classes/holds; DAT-030 diagnostics |
| BR-028 | SCR-010; API-022/041 | BAT-015; operational alerting | DAT-016 usage; DAT-030 cost/metric/alert records |
| BR-029 | SCR-003/006; API-031/042 | BAT-005–007/019 | DAT-023 aliases; DAT-028 cache; DAT-031 recovery |
| BR-030 | SF-014; API-038; error/retry boundary | BAT-010; applicable retries | DAT-027 original identity, dry-run/replay provenance |
| BR-031 | SCR-010; API-023–024/043–044 | BAT-016/018 | DAT-032 release/config/migration; DAT-033 corpus/score/gate |
| BR-032 | SCR-001–010; API-010–012/014–015/047 | BAT-020; progress producers | DAT-028 offsets/delivery; DAT-036 presentation projections |
| BR-033 | API-032–033; all attempted excluded capability calls | BAT-018; all job scope checks | DAT-035 controlled decisions; DAT-032 version lineage |

### Concrete Validation and Acceptance Conditions

The following tests complement the detailed completed-specification criteria. Requirements with unresolved formulas cannot receive fabricated numeric fixtures.

| Rule IDs | Satisfied case | Unsatisfied / boundary case and required result | Source test trace |
|---|---|---|---|
| BR-001–002 | Authorized resource attributes and tenant/workspace match | Valid foreign-tenant ID returns absent-ID-equivalent nondisclosing result; reused pooled connection exposes no previous tenant data | `T-01`, `TST-003`; Source, pp. 23, 86, 88–89 |
| BR-003 | Owner submits current revision | Stale revision produces `409 CASE_VERSION_CONFLICT`; no accepted state/outbox change | Source, pp. 25, 84 |
| BR-004–005 | Valid request/event commits once | Identical replay returns same creation result; changed fingerprint conflicts; replay event 100 times produces exactly one accepted transition | `T-07`, `TST-001–002`, `TST-007`; Source, pp. 88–89 |
| BR-006–009 | Classification provenance stored; corrected label has reason; priority uses explicit fields | Missing correction reason cannot satisfy correction rule; changing prediction cannot alter contractual deadline; numeric priority/calendar boundaries await approved fixtures | Source, pp. 12, 25 |
| BR-010 | Eligible closure captures exact approved lineage | Later source/run revision must not rewrite historical closure; predecessor/role tests await guard resolution | Source, pp. 25–26 |
| BR-011–012 | Complete provisioning and durable prior-item outcomes | Incomplete provisioning blocks sync; undurable preceding item blocks cursor; revoked credentials safely fail queued job | Source, pp. 27–29, 78 |
| BR-013 | Current permitted evidence served | Revoke after indexing/cache, then query/publish: no forbidden next-query evidence and no stale-ACL publication | `T-08`, `TST-004`; Source, pp. 46, 88–89 |
| BR-014–015 | Safe source with anchors/provenance processed | Unsafe/polyglot/zipped payload quarantined without indexing; low quality remains authorized-viewable but not autonomous evidence; exact upload/quality boundary fixtures unresolved | `T-04`, `TST-015`; Source, pp. 30–32, 88–89 |
| BR-016 | Authorized supported evidence with verifiable anchors | Missing support returns `NO_SUPPORTED_EVIDENCE`; missing citations cannot yield falsely approved answer; `max_items >10` violates MCP bound | `TST-009`; Source, pp. 36, 87, 89 |
| BR-017–019 | Approved route and separately authorized bounded plan | Regional outage cannot send restricted content to unapproved route; arbitrary/equivalent-denied tool denied before dispatch; depth 9/call 17 exceeds limits | `T-02`, `T-06`, `T-10`, `TST-014`; Source, pp. 40–42, 88–89 |
| BR-018 | Valid structured candidate | Unknown fields/invalid citation/control injection yields `MODEL_OUTPUT_INVALID`, no publication | `TST-005`; Source, pp. 38, 89 |
| BR-020 | All admission predicates satisfied | 429 storm has capped retries/controlled load; rejected new runs return `429` + `Retry-After`; quota exhaustion stops current run | `TST-008`; Source, pp. 38, 69, 89 |
| BR-021–024 | Exact eligible reviewed artifact and current evidence pass gate | Wrong hash stale/audited; incomplete review controls disabled; self approval denied; expiry never approves; old approval cannot publish changed artifact | `T-03`, `TST-006`, `TST-010`; Source, pp. 45–46, 58, 88–89 |
| BR-025–026 | Independent approval checks and removable eligible inventory | Single Admin insufficient; held records retained and receipted; export excludes secrets/internal prompts | `T-11`, `TST-013`; Source, pp. 78–80, 88–89 |
| BR-027–028 | Redacted immutable audit and attributed rollup | Historical edit denied; diagnostics/provider requests expose no out-of-scope secrets; cost expected values await approved formula | `T-05`, `T-09`; Source, pp. 62–66, 88 |
| BR-029–030 | Validated scoped recovery/replay | Missing reason/dry-run/scope does not authorize replay; failed index preserves source; incomplete rebuild cannot activate alias; recovery meets stated RPO/RTO | `TST-012`; Source, pp. 34, 49–50, 69, 89 |
| BR-031 | Verified release, adequate confidence and all gates satisfied | Score equality satisfies stated numeric threshold only; any critical isolation/approval exception, low confidence or regressed safety blocks promotion | `T-12`, `TST-016`; Source, pp. 74–76, 88–89 |
| BR-032 | Authorized refresh/resume reconstructs progress | Reconnect does not duplicate execution or reveal private retained data; keyboard action remains available with visible focus | `TST-011`; Source, pp. 55, 58, 89 |
| BR-033 | Approved baseline change linked to negative verification | Unapproved incompatible change or excluded capability is not authorized by this baseline | Source, pp. 8–10 |

## Consistency and Open Questions

### Conflicts and Required Amendments

Earlier specifications are not rewritten. Links identify affected completed requirements for later consolidation.

| ID | Affected rules / earlier identifiers | Source evidence and conflict | Required resolution |
|---|---|---|---|
| OQ-BR-001 | BR-003; [01_screen_functions.md](01_screen_functions.md) OQ-SF-002; [02_api.md](02_api.md) API-050/OQ-API-002; [03_data.md](03_data.md) OQ-DAT-005 | Source p. 24 associates workspace configuration with case PATCH | Define legitimate settings contract and revision scope; do not save workspace policy through inferred case mutation |
| OQ-BR-002 | BR-004/019/020; API-008–009, OQ-API-001; [04_batch_functions.md](04_batch_functions.md) OQ-BAT-001 | Source pp. 15–17 versus pp. 40, 83 gives two run paths | Resolve canonical route/alias and shared replay namespace |
| OQ-BR-003 | BR-007/010; OQ-SF-005, OQ-API-004, OQ-DAT-009 | Source p. 25 omits predecessor into `CLOSED` and explicit reopen target | Define closure/reopen guards, role, endpoint and preserved revision lineage |
| OQ-BR-004 | BR-019/023/032; OQ-SF-006, OQ-API-005, OQ-BAT-002 | Source p. 41 missing-approval termination conflicts with valid `AWAITING_REVIEW` on p. 49; p. 90 example timeout 180 s | Distinguish waiting from failed approval checkpoint; define timeout clock and recoverable state |
| OQ-BR-005 | BR-025/026; DAT-R-016, OQ-BAT-004 | Source p. 26 routine eligible-closed-case retention versus p. 78 two independent delete/export checks | Define routine-retention authorization and propagation; neither universal exemption nor universal two-person addition is confirmed |
| OQ-BR-006 | BR-001/022; DAT-011; Source p. 11 and p. 85 | High-risk analyst self-approval prohibition is narrower than general `approval_tasks` “no self approval” constraint | Preserve both; confirm complete separation-of-duties applicability and definition of originating actor |
| OQ-BR-007 | BR-032; OQ-SF-004/OQ-DAT-009 | Source pp. 57, 82 and reference UI use different state vocabularies | Define explicit presentation mapping without merging aggregate enums or treating example labels as new states |
| OQ-BR-008 | BR-031; OQ-SF-008/OQ-API-006 | Source p. 12 says within 300 ms; p. 65 says under 300 ms | Resolve strict/non-strict equality and timing measurement |
| OQ-BR-009 | BR-003/004/030; OQ-SF-007/OQ-API-003 | Source p. 54 naming convention versus uppercase literal errors on pp. 84, 89 | Preserve confirmed literals; decide compatible error convention |
| OQ-BR-010 | BR-005/010/015; OQ-DAT-001/OQ-DAT-003 | Mutable case prose versus “immutable derivative” register; UUIDv7 versus fingerprint-derived IDs | Distinguish mutable current aggregate, immutable history and identity/fingerprint roles |
| OQ-BR-011 | BR-005/030; OQ-API-008/OQ-BAT-005–006 | Repeated mutation-event wording beside reads; dead-letter replay versus p. 90 outbox replay | Define actual emission/replay contracts; ordinary GET must not fabricate mutation events |
| OQ-BR-012 | BR-031; Source p. 88 §D.1 | `SEC-001` through `SEC-012` are release-blocking, but individual definitions/mapping to `T-01` through `T-12` are not supplied | Preserve namespace/range; confirm exact security requirements and evidence mapping without inventing definitions |

### Unresolved Business Decisions

| ID | Affected rules | Needs confirmation | Evidence / dependency |
|---|---|---|---|
| OQ-BR-013 | BR-001–003/022/026 | Complete role/attribute matrix, Owner/Member meaning, Admin terminology, reviewer/approver eligibility and mutation field permissions | Source pp. 11, 22, 45, 83; OQ-API-011 |
| OQ-BR-014 | BR-003–005/021–024 | Policy effective periods, priority between overlapping rules, default/unmatched result, in-flight policy changes, concurrency and repeated decision semantics | Source pp. 9, 24–25, 44–46; OQ-API-014/021, OQ-DAT-016–018 |
| OQ-BR-015 | BR-006–009 | Labels/reasons/confidence, priority matrix, override/recalculation, SLA durations/calendar/start/pause/DST and prediction rules | Source pp. 12, 25; OQ-SF-014, OQ-DAT-014/024 |
| OQ-BR-016 | BR-012–016 | Lower-trust allowed uses, credential/cursor expiry, poison-record retry classification, file cap bytes/equality, quality/confidence thresholds, anchor coordinates and retrieval ranking/budgets | Source pp. 27–36, 87; OQ-BAT-011–012 |
| OQ-BR-017 | BR-017–020 | Approved model/data-class catalogs, quota reset/reservation/usage reconciliation, admission thresholds, call counting and run timeout | Source pp. 37–42, 69, 90; OQ-API-018, OQ-BAT-014 |
| OQ-BR-018 | BR-021–024 | Full normalized input/outcome decision matrix, financial categories, review required fields/rationale, exact hashing, review expiry races, overrides and publication trigger | Source pp. 44–46, 58; OQ-API-021, OQ-DAT-016 |
| OQ-BR-019 | BR-025–027 | Corporate retention periods/eligibility, holds creation/release/reevaluation, independent checks and validity, manifest/checksum, backup/shared-source treatment and partial-retention completion | Source pp. 26, 66, 78–80, 90; OQ-BAT-015 |
| OQ-BR-020 | BR-027–028 | PII/redaction policy, audit hash/rotation periods, cost/forecast formulas, currency/units/rounding, daily cutoff, late corrections and notification thresholds/routes | Source pp. 62–66; OQ-DAT-021–022, OQ-BAT-010/017 |
| OQ-BR-021 | BR-029–031 | Retry/circuit values, replay proof/scope/dedup periods, coverage/recall/recovery checks, scoring/confidence methods and canary thresholds | Source pp. 34, 49–50, 69–76; OQ-BAT-011–012/016 |
| OQ-BR-022 | BR-004/023/025/028 | Expiration equality, business versus elapsed periods, monthly/daily timezone, inclusive endpoints and empty/late/catch-up processing | Source pp. 25, 45, 65–66; OQ-BAT-009/013 |
| OQ-BR-023 | BR-032 | Display enum mapping, summary formulas, SSE retention/expired offsets, webhook age/signature and signed URL expiration | Source pp. 7, 52, 55–59; OQ-SF-013, OQ-API-019 |
| OQ-BR-024 | BR-033 and all rules | Supported cloud region, search/identity providers, approved deployments, corporate retention and connector permissions; per-tenant key isolation versus rotation throughput | Source pp. 10, 90 §F.2 |
| OQ-BR-025 | BR-028 | Any required accounting period-end close, billing/tax/payment calculation or other financial reporting beyond usage attribution | Needs confirmation: source supplies daily usage, not financial accounting requirements |

### Carried Proposals and Later Dependencies

- [01_screen_functions.md](01_screen_functions.md): Proposed field placement, primary actions, navigation and unplaced controls remain **Proposals**. BR mappings do not confirm new UI behavior.
- [02_api.md](02_api.md): Proposed case payload, authentication transport and SSE projection remain **Proposals**. Domain/storage terminology is not executable REST IDL.
- [03_data.md](03_data.md): Physical columns, schemas, hashing and logical-record persistence remain unresolved outside explicit source definitions. No business rule here silently adds DDL.
- [04_batch_functions.md](04_batch_functions.md): Logical job IDs do not require separate executables. Schedules, locking, batch units and empty/partial-result semantics remain unresolved.
- Appendix F configuration is example evidence. In particular, `auto_publish_classification: INTERNAL`, `require_human_review_for: [HIGH_RISK, RESTRICTED]`, `run_timeout_seconds: 180`, `replay_dedup_hours: 24`, retrieval counts/RRF value and `trace_sample_rate: 0.10` are not unconditional confirmed policy. Values independently confirmed elsewhere retain that independent status.
- Exception handling and remaining later-stage specifications are **To be defined in a later stage**. They must preserve these rules when completing error mappings, timeout recovery, partial outcomes and operational contracts.
- `08_architecture_decision.md` is **To be defined in a later stage**. Stage 8 must consolidate unresolved decisions from completed Markdown only, linking `05_business_rules.md`, affected `BR-*`/`OQ-BR-*` and earlier filenames/identifiers.

No owner identity, deadline or approval is supplied for these unresolved decisions. They require explicit resolution before implementation lock; this specification does not authorize the implementation AI to choose missing rules.
