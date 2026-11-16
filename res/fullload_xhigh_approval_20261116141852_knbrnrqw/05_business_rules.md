# 5. Business Rules

## Rule Inventory and Scope

### Specification Basis

| Item | Definition |
|---|---|
| Output file | `05_business_rules.md` |
| Application | OrionDesk AI |
| Source document | `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Baseline | Document `OD-AI-DDS-001`; release `R1.0`; design revision `1.3` |
| Source authority | Fictional reference architecture, normative for this sample application. Numeric targets are design assumptions, not measured production results. |
| Citation convention | **S** denotes `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf`. Citations identify original PDF pages and sections. |
| Completed specifications | [01_screen_functions.md](01_screen_functions.md), [02_api.md](02_api.md), [03_data.md](03_data.md), and [04_batch_functions.md](04_batch_functions.md) |
| Rule identifiers | `BR-001`–`BR-046` are specification identifiers. The source does not assign business-rule IDs. Existing `SCR-`, `API-`, `DAT-`, `BAT-`, `T-`, `TST-`, and `SEC-` identifiers remain unchanged. |
| Confirmed | Explicitly supported by S. A confirmed rule does not establish an undocumented request property, table, field constraint, actor mapping, threshold, error, or schedule. |
| Needs confirmation | An unresolved implementation or policy contract. It is not permission for an implementation AI to select behavior. |
| Proposal | An explicitly suggested design, not approved behavior. Earlier UI arrangements and API/SSE examples remain Proposals. |
| Remaining specifications | Remaining processing, exception-handling, and architecture details are **To be defined in a later stage**. `08_architecture_decision.md` has not yet been generated. |

**Scope:** This specification consolidates business conditions shared by screens, APIs, stored data, background jobs, and operational gates. It does not replace the preceding interface, field, or job specifications.

**Confirmed:** Retrieval, generation, deterministic policy evaluation, and human approval are separate records. Publication depends on supported evidence and satisfied approval policy, not merely successful generation or accepted asynchronous work.  
**Source:** S, p. 12, §2.2.2; pp. 44–46, Chapter 12.

### Rule Inventory

The **core obligations** in this inventory are Confirmed. Detailed gaps are identified beside the affected rules in subsequent sections.

| Rule ID | Name and purpose | Applicable targets | Actor or permission boundary | Evaluation timing | Evidence |
|---|---|---|---|---|---|
| BR-001 | Authenticated identity and safe sessions: establish trusted principal and tenant context | Interactive sessions, service calls, all protected requests | Authenticated user/service; audience and scope checks | Authentication and each protected request | S, pp. 18, 21–22, §§4.1.2, 5.1 |
| BR-002 | Resource authorization: combine roles and resource attributes rather than navigation visibility | Cases, evidence, reviews, settings, administration, tools | Analyst, Reviewer, Admin, Auditor, Service; catalog scopes remain separately defined | Edge authorization and domain/resource transaction boundary | S, pp. 11, 21–23, §§2.1, 5.2 |
| BR-003 | Tenant integrity and non-disclosure: prevent cross-tenant access and invalid workspace association | Tenant-owned rows, objects, jobs, resource identifiers | Trusted tenant-bound callers and scoped services | Every storage predicate and resource operation | S, pp. 22–23, 51, 86 |
| BR-004 | Current source access: make revocation effective before the next retrieval | Source ACLs, evidence, retrieval caches, publication | Currently authorized source readers and services | Before text release, after ACL changes, and at publication | S, pp. 27–28, 35, 53 |
| BR-005 | Untrusted content and independent tool authority: prevent model/evidence-driven privilege changes | Prompts, model replies, planner, MCP/A2A, external writes | Invoking principal, workspace policy, tool scope, classification; consequential writes require human authorization | Prompt construction, planning, argument validation, dispatch | S, p. 7; pp. 37–42, 61, 87 |
| BR-006 | Validation and unambiguous outcomes: fail closed and distinguish acceptance from completion | All requests, mutations, asynchronous operations, errors | Authorized caller; server validation remains authoritative | Before transaction/work allocation, at domain invariants, before dispatch | S, pp. 12–13, 54–56, 83–84 |
| BR-007 | Revision-safe case and configuration mutation | Case metadata/state; workspace settings | `Owner` for cataloged case PATCH; settings actor mapping unresolved | Before each accepted mutation | S, pp. 24–25, §§6.1.1, 6.2.2 |
| BR-008 | Idempotent business effects under request and event replay | Case creation, job-creating POSTs, cross-service writes, consumers | Authorized original operation and scoped consumers | Request retry, duplicate/delayed delivery, replay | S, pp. 15, 17, 25, 48, 54, 89–90 |
| BR-009 | Authoritative records, immutable lineage, and durable commits | Cases, revisions, document versions, decisions, outbox, index/cache | Owning domain services; narrow service interfaces | Storage mutation, external dispatch, historical inquiry | S, pp. 9, 16, 24, 45, 49, 51–52, 85 |
| BR-010 | Case initialization and classification correction | New cases, labels, confidence, provenance, corrections | Analyst creates; authorized user corrects labels | Creation, asynchronous `CaseCreated` consumption, correction | S, pp. 12, 40, 83, 86–87 |
| BR-011 | Explicit impact/urgency priority derivation | Case priority and prioritization displays | Authorized business-input editor; calculation is deterministic business behavior | Priority calculation; recalculation timing unresolved | S, p. 25, §6.3.1 |
| BR-012 | Contractual SLA and time presentation | Deadlines, advisory breach prediction, durable/display times | Authorized business operations; prediction cannot modify contracts | Deadline calculation and presentation | S, pp. 25, 54, 59 |
| BR-013 | Guarded normal case transitions | Case status and revision history | Authorized actor satisfying role, revision, evidence, and approval guards | Requested state change | S, pp. 25–26, 82–83 |
| BR-014 | Closure snapshot and new-revision reopening | Closed cases and approved-output lineage | Closing/reopening actor details unresolved | Closure and explicit reopening | S, pp. 24–26, §§6.1–6.3 |
| BR-015 | File admissibility and per-file limits | Attachments and connector-ingested files | Authorized Analyst upload; scoped ingestion | Before accepted long-running processing | S, p. 30, §8.1.1; p. 90 |
| BR-016 | Malware and active-content containment | Uploaded files, parser, quarantine, index | Ingestion/scanning boundary | Scan before parsing; before indexing | S, p. 30, §8.1.2; pp. 88–89 |
| BR-017 | Claim-preserving normalization, OCR, and source anchors | Document derivatives, content blocks, chunks, citations | Scoped ingestion; current authorized citation users | Extraction, reprocessing, citation generation/display | S, pp. 30–32, §§8.2–8.3 |
| BR-018 | Extraction-quality restrictions | Low-quality safe documents and autonomous recommendations | Extraction/retrieval/policy services; authorized viewer | After extraction and before autonomous recommendation | S, p. 32, §8.3.2; p. 82 |
| BR-019 | Bounded grounded retrieval and verified citations | Search, evidence sets, model context, source viewer | `Member` public-search scope; permitted-document tool scope | Each retrieval and citation display | S, pp. 34–36, 57, 83, 87, 90 |
| BR-020 | Validated index lifecycle and readiness | Index generations, aliases, search readiness | Indexer/rebuild/onboarding boundaries | Index commit, rebuild activation, readiness determination | S, pp. 34, 49, 78, 87 |
| BR-021 | Approved specific model routing and constrained fallback | Model deployment registry and provider invocation | Workspace-approved deployment and region policy | Initial selection and each fallback | S, pp. 37–39, §10.1 |
| BR-022 | Scoped prompt composition and structured-output validation | Prompt templates and generation attempts | Controlled model gateway | Before provider call and after provider reply | S, pp. 38–39, §§10.2–10.3 |
| BR-023 | Bounded plans, durable checkpoints, and stop conditions | AI run DAG, steps, runtime budget, progress | Orchestrator and independently authorized agents/tools | Before side effects, each dispatch, budget/deadline checks | S, pp. 12, 40–42, 49, 82, 90 |
| BR-024 | Token quotas and queue-aware admission | Run token reservation, workspace quota, queue age, provider capacity | Gateway/orchestrator; Analyst requests run | Before new-run admission and during invocation accounting | S, pp. 38, 69, §§10.3.1, 19.2.1 |
| BR-025 | Reproducible deterministic policy decisions | Normalized policy inputs, rule version, result, reasons | Deterministic Policy Evaluator, not an LLM agent | Policy checkpoint and applicable publication revalidation | S, pp. 40, 44–46, 85 |
| BR-026 | Maximum included-material classification across four controls | Routing, log redaction, retention, approval policy | Trusted classification and policy boundaries | Whenever run-included material determines these controls | S, p. 62, §17.2.1; p. 90 |
| BR-027 | Reviewer eligibility and separation of duties | Review pools, minimum role, assignments, self-approval | Eligible Reviewer selected by policy/organizational role | Assignment and decision acceptance | S, pp. 11, 45, 85, 90 |
| BR-028 | Complete review evidence and exact-hash decision capture | Review form, candidate, citations, immutable decisions | Eligible Reviewer | Before controls enable and at decision submission | S, pp. 44–45, 57–58, 83, 89 |
| BR-029 | Review expiry without implicit approval | Review task SLA, reassignment, escalation | Review-routing service; eligible replacement/escalation actors | Configured SLA expiry | S, p. 45, §12.2.1; p. 89 |
| BR-030 | Guarded override and non-retroactive rework | Overrides, rejected recommendations, new run revisions | Elevated role, secondary reviewer, audited reason | Override request or rework | S, p. 46, §12.3.2 |
| BR-031 | Atomic, exact-artifact publication gate | Final response pointer, evidence, policy, approvals | Trusted publication service with current authorization | Publication validation and commit | S, pp. 12, 45–46, 87 |
| BR-032 | Truthful, accessible artifact and progress presentation | Draft labels, run timeline, review evidence, SSE | Authorized Analyst/Reviewer; scoped stream access | Display, refresh, reconnect, meaningful state update | S, pp. 13, 55, 57–59, 83, 89 |
| BR-033 | Complete idempotent provisioning and bounded backfill | Workspace policy, keys, roles, quotas, connector stubs, historic documents | Authorized provisioning/onboarding boundary; exact roles unresolved | Provisioning, backfill batch, sync/readiness check | S, p. 78, §§22.1.1–22.1.2 |
| BR-034 | Explicit connector capability trust and safe credentials | Connector capability metadata, secret references, queued sync | Admin starts sync; authorized operators revoke credentials | Discovery, sync validation, queued execution | S, pp. 27–29, 83 |
| BR-035 | Durable source cursor, source deletion, and poison-record outcomes | Cursor, watermark, error ledger, tombstones, item outcomes | Connector workers and scoped index removal | Each item/batch, cursor advancement, source-change processing | S, pp. 28–29, 51 |
| BR-036 | Bounded retries and fair throttling | Dependencies, connectors, provider throttling, worker queues | Scoped workers; workspace quotas | Transient failure, provider `Retry-After`, scheduling | S, pp. 19, 28–29, 38, 42, 49, 89 |
| BR-037 | Authorized replay, reconciliation, and scoped incident repair | Dead letters, outbox, checkpoints, fingerprints, incident evidence | Authorized operator; reason, dry-run, scope limit | Replay and incident recovery | S, pp. 49–50, 79, 90, §F.1 |
| BR-038 | Retention eligibility, legal holds, and tombstone semantics | Closed cases, diagnostics, audit, run material, cache, purge receipts | Authorized retention/storage services | Eligibility evaluation and each purge | S, pp. 26, 51–53, 62, 66, 80, 90 |
| BR-039 | Independent export and deletion authorization | Controlled lifecycle requests and approval proof | `Admin + approver`; two independent checks; two-person export control | Before accepting export/delete work | S, pp. 78, 83, 88, `T-11` |
| BR-040 | Integrity-protected export contents and exclusions | Export package and manifest | Independently authorized export workflow | Inventory selection, packaging, completion verification | S, p. 79, §22.3.1 |
| BR-041 | Verified deletion and shared data-subject inventory | Tombstones, blobs, index entries, held records, receipts | Independently authorized deletion workflow; Retention Worker | Deletion, hold checks, verification | S, p. 80, §22.3.2; pp. 87, 89 |
| BR-042 | Attributed daily usage and period-end reporting | Usage/cost ledgers, daily budget/forecast/rejected-request rollups | Usage processing; Admin reads cataloged usage | Usage recording and daily rollup | S, pp. 38, 65, 83, 85 |
| BR-043 | Privacy-safe immutable audit and cryptographic handling | PII tags, diagnostics, audit archives, secrets, keys | Scoped services; Auditor redacted inquiry; authorized key/secret administration | Extraction, provider invocation, logging, archive, rotation | S, pp. 11, 21, 52, 54, 61–66, 71, 84 |
| BR-044 | Reliability, alerting, graceful degradation, and recovery safety | Service objectives, modes, capacity, incident/recovery gates | Operational services; incident command; on-call routing | Monitoring, outage containment, restore, re-enable | S, pp. 18–20, 64–70, 79, 89–90 |
| BR-045 | Frozen evaluation and non-overridable safety release gates | Corpus, expected outputs, scorecard, critical tests | Admin starts evaluation; independent fixture/security review | Evaluation, prompt/model change, release gate | S, pp. 74–76, 83, 88–89 |
| BR-046 | Controlled changes, compatible migration, and reconstructible releases | Design decisions, contracts, configuration, builds, migrations, canary, release records | Authorized governance/release actors; Security/SRE validation | Change approval, CI, rollout, promotion/rollback | S, pp. 8–10, 15, 20, 52, 55, 71–73, 88–90 |

### Explicit Prohibitions and Deferrals

| Category | Status | Business boundary | Source |
|---|---|---|---|
| Physical automation and irreversible financial transactions | Out of scope | The platform handles enterprise knowledge and submitted cases, not these operations. Financial-impact category remains a valid policy input. | S, p. 9, §1.2.1; p. 44, §12.1.1 |
| Foundation-model fine-tuning | Out of scope | No fine-tuning operation or job is supported. | S, p. 9, §1.2.1 |
| Unrestricted browsing and agent administrative cloud permissions | Out of scope | Evidence/model text must not create unrestricted browsing or administrative authority. | S, p. 9, §1.2.1 |
| Application-hosted GPU inference | Out of scope | Inference providers are external dependencies. | S, p. 19, §4.2.1 |
| Cross-region active/active mutation, OCR beyond English, customer-managed model weights | Deferred from this baseline | Do not expose these as enabled modes. Opt-in OCR remains supported within the stated baseline. | S, p. 10, §1.3.2; p. 31, §8.2.1 |
| Secrets and internal model prompts in export | Out of scope for export contents | They must be excluded from the package. | S, p. 79, §22.3.1 |
| Monthly financial close, invoicing, tax, currency conversion, quarter/year-end settlement | Needs confirmation | These categories are not described. Daily usage rollups do not establish a financial settlement workflow. | S, p. 65, §18.3.1 |
| End-user run cancellation, bulk approval, automatic reauthorization, scheduled reclassification | Needs confirmation | No complete business contract is supplied. These are not explicitly excluded. | S, Chapters 7, 11–12, 16; earlier open questions |

## Decisions, Calculations, and State Transitions

### Shared Rule Evaluation and Conflict Boundaries

**BR-006 — Confirmed:** Validation occurs before transaction entry or long-running work allocation, again at domain invariants, and before tool dispatch. Client validation is convenience only.

**BR-002, BR-007, BR-031 — Confirmed:** Passing one check does not waive another applicable check. For example:

- A role grant does not waive tenant, workspace, document ACL, sensitivity, or separation-of-duties conditions.
- An allowed case-state edge does not waive revision or approval requirements.
- Valid model output does not authorize a tool call.
- An accepted human decision does not waive current evidence, classification, or publication requirements.
- Export/delete approval does not waive legal hold.
- A high benchmark score does not waive critical security findings.

**Sources:** S, pp. 7, 22, 25, 37, 45, 68, 80, 88.

| Condition | Confirmed result | Conflict or priority detail |
|---|---|---|
| An applicable authorization or stale-write guard fails | Reject the action; leave denied business state unchanged | Which error is returned when several checks fail is Needs confirmation |
| Retrieved/model text requests different permissions, tenant, or approvals | Treat it as untrusted data; do not execute the requested privilege change | It has no rule-authority priority |
| Policy yields `AUTO_ALLOW`, but an obligatory evidence or approval requirement is unsatisfied | Do not publish | `AUTO_ALLOW` is not a universal bypass |
| An `INTERNAL` case includes `RESTRICTED` material | Apply the maximum-material controls under BR-026 | The lower case label cannot reduce the four controls |
| Retention/deletion eligibility and a legal hold overlap | Preserve protected held records and receipt the exception | Exact lifecycle final state and held-data extent remain unresolved |
| Canary/benchmark results pass but a critical isolation or approval-bypass finding is unmitigated | Block promotion | Security exit criteria override benchmark acceptability |
| Dependency unavailable | Return a documented retryable error or persisted asynchronous job identity, never ambiguous success | Per-interface selection and error mapping remain unresolved |

**Needs confirmation — BR-OQ-002, BR-OQ-012, BR-OQ-018, BR-OQ-023:** Error-selection order, overlapping deterministic policy conditions, effective-version selection, and race resolution. This specification does not establish a new first-match or numeric rule-priority scheme.

### BR-001–BR-004 — Identity, Permissions, Tenancy, and Source Access

#### Identity and Session Prerequisites

1. Authenticate interactive sessions through OIDC authorization-code flow with PKCE.
2. Verify token issuer, audience, expiry, subject, and tenant context.
3. Reject unexpected token algorithms or missing tenancy claims.
4. Independently authenticate and authorize internal service calls using TLS, service audience checks, and scoped identities.
5. Use managed workload identity where the provider supports it; do not share one service identity between deployment units.
6. Do not store long-lived refresh tokens in browser local storage.
7. Keep service credentials out of traces and model prompts.

A BFF issuing secure, HttpOnly, SameSite cookies is a **source-supported option**, not a selected mandatory architecture.  
**Source:** S, p. 18, §4.1.2; pp. 21–22, §5.1.

**Needs confirmation — BR-OQ-001:** Identity provider, algorithms, exact claim names/audiences, session transport/lifetime, and user/service identity mapping.

#### Cataloged Permission Decisions

Every row also requires BR-002 resource authorization and BR-003 tenancy.

| Operation or capability | Confirmed permission | Additional conditions |
|---|---|---|
| API-001 `POST /v1/cases` | `Analyst` | Valid case context and idempotency |
| API-002 `GET /v1/cases/{caseId}` | `Analyst / Reviewer` | Authorized current case revision |
| API-003 `PATCH /v1/cases/{caseId}` | `Owner` | `If-Match`, supported mutation, applicable state/evidence/approval guards |
| API-004 `POST /v1/cases/{caseId}/attachments` | `Analyst` | File and ingestion safety checks |
| API-005 `POST /v1/cases/{caseId}/runs` | `Analyst` | Case access, admission, bounded workflow and tool/model policy |
| API-006 / API-007 run read and stream | `Analyst / Reviewer` | Authorized run; backfill remains in current caller scope |
| API-024 `POST /v1/approvals/{approvalId}/decision` | `Reviewer` | Eligible task/pool/role, exact hash, separation of duties |
| API-009 connector sync | `Admin` | Provisioning complete; connector/credential/quota controls |
| API-010 `POST /v1/search` | `Member` | Current originating document ACL |
| API-011 audit inquiry | `Auditor` | Immutable metadata within redacted scope |
| API-012 usage inquiry; API-013 evaluation creation | `Admin` | Authorized resource scope; evaluation job validation |
| API-014 / API-015 export/delete | `Admin + approver` | Two independent approval checks; lifecycle rules |
| API-046 `knowledge.search@v1` | `read:permitted_documents` | Tenant-scoped, read-only, independently authorized capability |

**Source:** S, pp. 83 and 87, Appendices A.2 and C.2.

**Confirmed:** Analyst, Reviewer, Workspace Admin, and Auditor responsibilities are distinct. Auditor evidence access does not permit editing case content or historical decisions. Administrative status does not establish review authority.  
**Source:** S, p. 11, §§2.1.1–2.1.2; p. 62, §17.3.1.

**Needs confirmation — BR-OQ-001:** Mapping of Workspace Admin to `Admin`, `Owner` to case ownership, `Member` to membership/roles, and `approver` to independent actor eligibility. Complete membership, settings, closure, health, hold, and operational permissions are unresolved.

#### Tenant and Access Decision Table

| Prerequisite or input condition | Required result |
|---|---|
| Valid principal, matching tenant/workspace, permitted action, satisfied resource attributes | Continue to the remaining applicable business checks |
| Foreign-tenant resource ID | Same not-found response class as an absent ID; no private existence disclosure |
| Case workspace belongs to another tenant | Reject the write without business-state change |
| Retrieval candidate fails current document ACL | Do not release its text to the user/model as authorized evidence |
| Source permission revoked after indexing/cache fill | No forbidden evidence on the next query |
| Source permission changes after review but before publication | Recompute authorization and reject stale evidence |
| Pooled database connection reused | Reset scoped session variables after every transaction |
| Soft-deleted entity requested | Do not retrieve it |
| Cached evidence has matching query but stale authorization context | It cannot override current access restrictions |

**Sources:** S, pp. 22–23, §§5.2–5.3; p. 28, §7.2.2; pp. 51–53, §§14.1–14.3; p. 86, B.2; p. 89, `TST-003`, `TST-004`.

**BR-003 — Confirmed:** Tenant-owned rows include `tenant_id`; tenant identity participates in every storage access predicate. Workspace-tenancy membership must be enforced through foreign keys or controlled write procedures. Signed background-job envelopes carry immutable tenancy.

**BR-004 — Confirmed:** Cache keys include tenant, user-scope digest, source ACL revision, query hash, and index generation. Authorization changes purge affected entries before normal TTL expiration. Short-lived cache or eventually consistent index behavior cannot defer the next-query revocation obligation.

**Needs confirmation — BR-OQ-008, BR-OQ-016:** ACL representation, invalidation barriers, concurrent cache-fill handling, signed-URL access recovery, and cross-store race mechanisms.

### BR-005–BR-009 — Authority, Mutation, Idempotency, and Record Consistency

#### Untrusted Data and Tool Dispatch

| Input or attempted operation | Confirmed condition/result |
|---|---|
| Source paragraph contains hostile system/tool instructions | Delimit as untrusted evidence; never promote it into instruction authority |
| Model reply claims a tool is authorized | Model output is data, not authorization proof |
| Browser submits arbitrary tool definitions | Not permitted |
| Discovered MCP/A2A capability has no independent grant | Discovery grants no permission; deny unauthorized dispatch |
| Approved MCP tool invocation | Use pinned typed schema, validated arguments, scoped credentials, and separate capability authorization |
| External write | Requires separate capability authorization |
| Consequential mutable tool operation | Requires idempotency and human authorization |
| Denied action replaced with an equivalent tool | Prohibited |
| `knowledge.search@v1` attempts arbitrary URL/filesystem access | Prohibited by its read-only contract |
| A2A handoff | Carries task ID, capability, declared input/output schema, deadline, trace context; recipient may decline |

**Source:** S, p. 7; pp. 38–42, §§10.2–11.3; p. 61, §17.1.2; p. 87, C.2.

**Needs confirmation — BR-OQ-009, BR-OQ-010, BR-OQ-012:** Consequential-action classification, tool/grant schemas, protocol transports, deadline handling, and A2A declared output-schema property. No additional tool or endpoint is approved here.

#### Revision and Idempotency Decisions

| Condition | Confirmed outcome | Period or boundary |
|---|---|---|
| Authorized case mutation with current `If-Match` and satisfied business guards | Accept supported change with monotonic revision and lineage | Revision increment allocation details remain unresolved |
| Case revision no longer matches | HTTP `409`, `CASE_VERSION_CONFLICT`, current revision information; no overwrite | Exact `If-Match` encoding and missing-header outcome unresolved |
| Workspace settings update has stale revision or unauthorized actor | Reject without business mutation | Settings-specific conflict code/header unresolved |
| Same case-create key, actor binding, and identical request fingerprint | One case and identical original response | Case binding lasts `24` hours |
| Same key with changed fingerprint | `IDEMPOTENCY_CONFLICT`; source verification specifies HTTP `409` | Fingerprint/key namespace and expiry handling unresolved |
| Job-creating POST | Requires `Idempotency-Key`; accepted repeat returns original operation | Non-case HTTP retention period not supplied |
| Duplicate event ID/operation key | Record duplicate outcome; do not reapply mutation | Consumer namespace and ledger expiry unresolved |
| Delayed/stale aggregate event | Detect stale revision; do not violate current aggregate invariants | Precise stale-event disposition unresolved |
| Repeated event across queue partitions | Safety cannot rely on cross-partition ordering | No new ordering guarantee |
| Operator replay | Preserve original identity except explicit provenance-linked schema migration | Reference `workflow.replay_dedup_hours: 24` is not a universal TTL |

**Source:** S, pp. 15, 17, 24–25, 48–50, 54; pp. 89–90.

**Needs confirmation — BR-OQ-002, BR-OQ-016:** Fingerprint canonicalization, concurrent duplicate reservation, error replay, exact TTL start/end, request-key namespace, revision allocation, transaction isolation, and deduplication after expiry. Do not assume that the case’s `24`-hour binding defines SSE, cache, archive, or all job retention.

#### Authoritative and Immutable Record Rules

**BR-009 — Confirmed:**

1. PostgreSQL is authoritative for mutable case state and metadata.
2. Source and normalized documents remain in encrypted blob/object storage.
3. Search indexes are nonauthoritative derivatives; cache results are versioned and ephemeral.
4. Attachments reference immutable document versions.
5. Case revisions are append-only.
6. Approval decisions and historical review lineage are immutable.
7. Case mutations, approval decisions, and applicable outbox insertion use the confirmed ACID boundary.
8. Publication gate satisfaction and final response pointer update commit atomically.
9. Indexing and webhook effects are asynchronous and explicitly reconciled.
10. Failed index writes do not roll back accepted source metadata; fingerprint reconciliation retries derivatives and repairs message links from the outbox.
11. The orchestrator has no direct database credentials and uses narrow scoped interfaces.

**Sources:** S, pp. 9, 16, 24, 45, 49, 51–52, 85.

Every durable change retains tenant, revision, actor, occurrence time, and correlation context. Events retain:

`event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, and `payload`.

Producers use UTC and canonical JSON. Actor/correlation placement outside the stated envelope remains unresolved.  
**Source:** S, p. 48, §13.1.1; chapter interface-boundary requirements.

### BR-010–BR-014 — Case Rules, Priority, SLA, and State

#### Case Initialization and Classification

| Input/event | Confirmed result | Unresolved details |
|---|---|---|
| Valid authorized new case | Case starts in `NEW`; reference revision default `1`; sensitivity default `INTERNAL` | Complete required business inputs and public receipt fields |
| `CaseCreated` | Asynchronous classification attaches labels, confidences, and provenance | Classification schema, empty result, exact revision/attachment snapshot |
| User corrects a label | Correction requires a reason code; supported provenance remains represented | Label/reason catalogs, correction precedence, endpoint schema |
| Classifier result arrives after newer correction/revision | Stale-write and provenance rules remain applicable | Exact correction-versus-classifier conflict rule |

The source does not establish that classification completion automatically executes `NEW → TRIAGED`.  
**Source:** S, p. 12, §2.2.1; p. 25, §6.2; pp. 86–87, B.2 and C.1.

**Needs confirmation — BR-OQ-003, BR-OQ-006:** Case field requiredness, owner initialization, correction/history schemas, confidence format, and classification-to-state trigger.

#### Priority and Contractual Deadline Calculations

| Rule | Prerequisites and inputs | Confirmed calculation/result | Formula, units, rounding, and boundaries |
|---|---|---|---|
| BR-011 | Explicit impact and urgency business inputs | Priority derives from both; model output alone cannot determine it | No impact/urgency catalog, priority matrix, numeric formula, weight, tie-breaker, default, rounding, or override rule is supplied |
| BR-012 | Applicable business calendar and workspace timezone | Calendar computes contractual deadlines in workspace timezone | Start event, SLA duration, business hours, holidays, cutoff rules, pause/resume, DST handling, precision, and rounding are unresolved |
| BR-012 | Breach prediction | Advisory only; cannot change contractual deadline | Prediction formula, confidence, and display schema are unresolved |
| BR-012 | Durable time and locale | Server stores UTC; public timestamps use RFC 3339; UI shows workspace-local time with timezone label | Locale changes presentation, not event order or durable API values |

**Source:** S, p. 25, §6.3.1; p. 54, §15.1.1; p. 59, §16.3.2.

**Needs confirmation — BR-OQ-004:** Complete priority decision matrix, missing-input behavior, manual override authority, and recalculation triggers.

**Needs confirmation — BR-OQ-005:** Contractual deadline inputs, duration units, business-calendar version, day boundaries, equal-to-deadline breach condition, and permitted recalculation. No review-SLA or daily accounting timezone is inferred from the case calendar.

#### Confirmed Normal Case Transition Table

**BR-013:** Preserve the six existing transition identifiers. Each edge requires current revision and applicable role, resource, evidence, and approval guards.

| Existing transition ID | From | To | Confirmed result and conditions | Needs confirmation |
|---|---|---|---|---|
| `SCR-002-T01` | `NEW` | `TRIAGED` | Allowed guarded state/revision change | Actor and classification/triage trigger |
| `SCR-002-T02` | `TRIAGED` | `IN_PROGRESS` | Allowed guarded state/revision change | Actor/action trigger |
| `SCR-002-T03` | `IN_PROGRESS` | `PENDING_APPROVAL` | Allowed guarded state/revision change | Policy/task/candidate linkage and initiating actor |
| `SCR-002-T04` | `IN_PROGRESS` | `RESOLVED` | Allowed when applicable evidence and approval requirements are satisfied | Exact resolution trigger and actor; this edge is not an approval bypass |
| `SCR-002-T05` | `PENDING_APPROVAL` | `RESOLVED` | Applicable approval must bind exact reviewed artifact and satisfy separation of duties | Decision-to-case-state linkage |
| `SCR-002-T06` | `PENDING_APPROVAL` | `IN_PROGRESS` | Authorized guarded rework transition | Rejection trigger and task consequences; not automatically every Reject action |

**Source:** S, p. 25, §6.2.1; pp. 44–46, Chapter 12; p. 82, A.1.

A normal edge not listed above is not authorized by this specification. Invalid or unauthorized transitions leave business state unchanged; an invalid-transition code is not supplied.

#### Closure and Reopening

| Existing identifier | Confirmed business requirement | Missing contract |
|---|---|---|
| `SCR-002-T07`; API-017 `POST /v1/cases/{caseId}/close` | Closure snapshots approved answer, cited document versions, and reviewer decisions; preserve immutable approved-output lineage | Permitted originating state, eligible actor, request/result, repeated-close behavior |
| `SCR-002-T08`; API-052 | `CLOSED` is final except explicit reopening as a new revision; prior lineage remains immutable | Target state, actor, approval requirements, endpoint and revision linkage |

**Source:** S, pp. 24–26, §§6.1–6.3.

**Needs confirmation — BR-OQ-006:** Complete only missing closing/reopening and edge-specific guards. Do not invent `RESOLVED → CLOSED`, a reopening target, or an ordinary in-place exit from `CLOSED`.

### BR-015–BR-020 — File, Quality, Retrieval, and Index Decisions

#### File and Extraction Decision Table

| Condition | BR rule | Confirmed result |
|---|---|---|
| Supported PDF, DOCX, HTML, or UTF-8 text; MIME signature and extension agree; configured size/decompression checks pass | BR-015 | May accept authorized ingestion; cataloged upload returns HTTP `202` |
| Unsupported or type-mismatched file | BR-015 | Fail closed; no invented `413`/`415` status or error code |
| File exceeds configured per-file cap | BR-015 | Fail closed |
| Decompression safety condition fails | BR-015 | Fail closed |
| Scan finds unsafe content | BR-016 | Quarantine; do not index |
| Parser would execute macros or fetch embedded remote references | BR-016 | Macro execution disabled; remote references not fetched |
| Safe PDF normalization | BR-017 | Preserve page/block/bounding-box, tables, headings, and reading order |
| OCR fallback not opted in | BR-017 | Do not enable fallback automatically |
| OCR fallback opted in | BR-017 | Apply supported fallback and mark OCR provenance |
| Pipeline version changes | BR-017 | Reprocess side by side using immutable derivative identities |
| Normalization strips transport artifacts | BR-017 | Source claims must not be rewritten |
| Safe document has low extraction quality | BR-018 | Remains viewable to authorized users; excluded from autonomous recommendations |
| Chunk anchor unresolved or current source permission absent | BR-017/BR-019 | Must not support a generated citation |
| Unsafe quarantined content requested for viewing | BR-016 | Viewing/download contract Needs confirmation; quarantine is not a viewing grant |

**Source:** S, pp. 30–32, §§8.1–8.3; pp. 83, 88–90.

**BR-015 numeric boundary:** `storage.upload_limit_mb: 25` is the reference configurable per-file cap. A file at or below the defined cap still requires all other admissibility checks. Exact conversion of MB to bytes and subtype/MIME definitions remain unresolved.

**BR-017 provenance:** Every chunk stores source URI, file hash, page number, and optional bounding box. Content fingerprint plus pipeline version produces immutable derivative IDs.

**BR-018 quality inputs:** Empty-page ratio, unknown-character ratio, table-loss indicators, and language confidence. No formula, confidence range, threshold, zero-denominator rule, or rounding is supplied.

**Needs confirmation — BR-OQ-007:** File count/name/transport constraints, decompression threshold, parser sandbox bounds, quality formulas/limits, document-state edges, empty source behavior, OCR input schema, derivative-ID/hash algorithm, and unsafe viewing policy.

#### Retrieval and Citation Rules

1. Form lexical and normalized vector queries.
2. Obtain bounded candidate sets.
3. Merge with reciprocal rank fusion and apply deterministic re-ranking.
4. Limit redundant same-document hits and preserve relevant-source diversity.
5. Enforce per-query model-context token budgets.
6. Apply originating ACL checks before text release.
7. Verify citations before display.
8. Include chunk ID, source title, immutable document revision, page anchor, and ACL digest in each response evidence item.
9. Citation activation opens the cited source and highlights its anchored page range.
10. Return `NO_SUPPORTED_EVIDENCE` when confidence or evidence quality is insufficient; never fabricate context. Clarification or human routing is permitted, but the selection rule is unresolved.

**Source:** S, pp. 34–36, §§9.1–9.3; p. 57, §16.1.2.

| Reference parameter | Exact value | Business boundary |
|---|---|---|
| `retrieval.max_candidate_chunks` | `80` | Backend candidate budget, not public page size |
| `retrieval.max_selected_chunks` | `10` | Backend selected-evidence budget |
| `retrieval.hybrid_rrf_k` | `60` | RRF reference parameter; executable scoring details are not provided |
| `retrieval.embed_dimension` | `1536` | Embedding representation, not a user-input limit |
| MCP `max_items` | `int<=10` | Tool upper bound; lower bound/default/optionality unresolved |

**Source:** S, pp. 87 and 90, C.2 and Appendix F.

**Needs confirmation — BR-OQ-008:** RRF scoring equation, normalization, missing-rank treatment, tie-breakers, diversity quotas, token limit, confidence/quality thresholds, `Citation` schema, nonpaginated anchors, and public pagination. No conventional formula is promoted to a confirmed application rule.

#### Index Commit, Rebuild, and Readiness

| Condition | BR-020 result |
|---|---|
| Normalized immutable version available | Build its searchable derivative under source scope/version/classification controls |
| Index write fails | Keep accepted source metadata; reconcile fingerprints and retry |
| Rebuild requested | Create parallel index generation |
| Completeness or recall check fails | Do not activate the unvalidated read generation |
| Required rebuild checks succeed | Atomically switch the read alias |
| Historic backfill queue is empty but coverage incomplete | Queue emptiness does not establish search readiness |
| `SearchIndexCommitted` delivered | Invalidate applicable query cache |
| Source is tombstoned or unauthorized during rebuild | Current deletion/access restrictions remain enforced |

**Source:** S, p. 34, §§9.1.1–9.1.2; p. 49, §13.2.2; p. 78, §22.1.2; p. 87, C.1.

**Needs confirmation — BR-OQ-008, BR-OQ-019:** Completeness/recall/coverage formulas and thresholds, incremental change handling during rebuild, generation overlap, old-index retention, and exact document `READY` linkage.

### BR-021–BR-026 — Model, Workflow, Admission, and Policy

#### Model Routing and Prompt Decisions

| Condition | Rule | Confirmed result |
|---|---|---|
| Deployment has required capability/region/handling/context/evaluation approval and workspace whitelist membership | BR-021 | Eligible for policy-governed selection |
| Only provider brand is whitelisted | BR-021 | Insufficient; whitelist specific deployments |
| Approved provider/deployment unavailable | BR-021 | Fallback only to approved equal-or-stronger data-handling class and approved region/deployment |
| Restricted content would reach unapproved fallback | BR-021 | Prohibited, including outages |
| Prompt assembled | BR-022 | Fixed system rules, signed workflow instruction, validated user input, separately delimited evidence |
| Evidence contains tool-call directives | BR-005/BR-022 | Strip directives from evidence context and record injection indicators |
| Provider output conforms to approved versioned JSON schema | BR-022 | Candidate data may proceed to remaining grounding/policy checks; not publication authority |
| Unknown fields, invalid citations, or control-character injection | BR-022 | `MODEL_OUTPUT_INVALID`; bounded validation retries; no publication |
| Likely personal data is nonessential and policy permits redaction | BR-043 | Redact before provider invocation |

**Source:** S, pp. 37–39, §§10.1–10.3; p. 62, §17.2.2.

**Needs confirmation — BR-OQ-009:** Approved deployments/regions, routing selection priorities, class comparison mapping, prompt/output schemas, retry counts, provider deadlines, context/token accounting, and injection-indicator schema.

#### Bounded Workflow and Stop Conditions

**BR-023 — Confirmed:** Plan is a DAG with explicit dependencies, bounded depth `8`, maximum `16` tool invocations, and replayable checkpoints. Persist plan revision before side effects and each stage checkpoint before downstream dispatch.

| Input or boundary | Result |
|---|---|
| Cyclic plan | Not a valid DAG |
| Plan depth exceeds `8` | Must not execute as an admissible plan |
| Exactly depth `8` | Within depth bound, subject to all other checks |
| Invocation would exceed `16` calls | Must not dispatch beyond the bound |
| Exactly `16` invocations | Within numeric ceiling; further dispatch is prohibited when budget exhausted |
| Missing approval, exhausted call budget, repeated invalid plans, policy denial, deadline expiry | Source stop condition; report exact failed checkpoint |
| Runtime reaches configured maximum | Run becomes terminal or yields the source-described recoverable timeout behavior; representation unresolved |
| Reference timeout setting | `workflow.run_timeout_seconds: 180` |
| Workflow stage progresses | Checkpoint precedes downstream dispatch; user refresh reconstructs persisted state |

**Source:** S, p. 12, §2.3.1; pp. 40–42, §§11.1–11.3; p. 49, §13.2.1; pp. 82, 90.

Confirmed Run vocabulary:

`REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED`.

The source progression is:

`REQUESTED → RETRIEVING → GENERATING → POLICY_CHECK → AWAITING_REVIEW → PUBLISHED`, or terminal failure.

**Needs confirmation — BR-OQ-010:** Missing-approval waiting versus termination, runtime inclusion of human-review wait, budget counting under retries/replay, deadline equality, failure edges, recoverable timeout representation, and the `AUTO_ALLOW` publication path. Do not invent `TIMED_OUT`, `CANCELLED`, or an ordinary end-user retry/cancel contract.

#### Token and New-Run Admission Decisions

| Workspace tokens satisfy threshold | Queue age satisfies threshold | Provider capacity satisfies threshold | Confirmed admission consequence |
|---|---|---|---|
| Yes | Yes | Yes | May admit authorized, valid bounded run after remaining checks |
| No | Any | Any | Do not admit; throttled client receives HTTP `429` and `Retry-After` |
| Any | No | Any | Same throttling consequence |
| Any | Any | No | Same throttling consequence |

**BR-024 — Confirmed:** Each run reserves input/output token budget and tracks provider usage under workspace quota. Quota exhaustion terminates the current run without automatically changing model or data class. Saved cases remain available when new runs are throttled.  
**Source:** S, p. 38, §10.3.1; p. 69, §19.2.1.

**Needs confirmation — BR-OQ-011:** Threshold values/operators/units, remaining-token calculation, reservation/release behavior, overrun treatment, quota reset periods, concurrent reservations, provider-capacity accounting, and `Retry-After` computation. The reference `20` concurrent AI runs per large tenant is not every workspace’s selected quota.

#### Deterministic Policy Input Contract

| Input concept | Required behavior | Missing definition |
|---|---|---|
| Case sensitivity | Normalize/store classification context; also apply BR-026 | Classification provenance and policy mapping |
| Requested action | Normalize authorized action | Action catalog |
| Evidence quality | Normalize quality evidence | Metrics, thresholds, combinations |
| Model class | Evaluate model-class context | Registry/class mapping |
| Financial-impact category | Normalize business impact | Category catalog and thresholds |
| Confidence bands | Normalize band values | Band definitions and boundary operators |

Store **all normalized inputs** with rule-set version. `policy_evaluations.input_digest` does not replace the required normalized input records.  
**Source:** S, p. 44, §12.1.1; p. 85, B.1.

| Policy result | Confirmed consequence | Selection and conflict gap |
|---|---|---|
| `AUTO_ALLOW` | Automatic allowance remains subject to evidence, authorization, classification, and publication requirements | Exact selecting conditions and workflow edge unresolved |
| `HUMAN_REVIEW` | Required eligible human review must be satisfied before publication | Pool/role/quorum and input thresholds unresolved |
| `REQUEST_MORE_EVIDENCE` | No fabricated support; evidence request/clarification path needs definition | Required additional evidence and next action unresolved |
| `DENY` | Denied action cannot proceed as an autonomous mutation or be substituted through another tool | Detailed denial reasons and authorized override extent unresolved |

The Policy Evaluator is deterministic, not an LLM agent. An LLM may propose risk tags but cannot override outcomes. High-impact recommendations become review tasks rather than autonomous mutations.  
**Source:** S, pp. 40, 44, 46.

**Needs confirmation — BR-OQ-012:** Complete decision table, confidence/risk/impact thresholds, competing-condition priorities, action taxonomy, activation of `policy_version` versus `rule_version`, and in-flight version handling.

#### BR-026 — Maximum Included-Material Classification

<a id="br-026"></a>

**Confirmed:** For every run, use the maximum information class of any included material to determine:

1. Model routing.
2. Log redaction.
3. Retention.
4. Approval policy.

Classes are `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, and `RESTRICTED`. This is semantic classification aggregation, not lexical string comparison.

| Case and included-material context | Required result |
|---|---|
| `INTERNAL` case includes permitted, anchored, quality-appropriate `RESTRICTED` evidence | All four controls use applicable `RESTRICTED` policy |
| Source ACL passes but evidence class is higher than case class | ACL permission does not authorize lower-class controls |
| Run is otherwise eligible for publication but meets required high-risk/restricted review condition | Required human review cannot be bypassed |
| `policy.auto_publish_classification: INTERNAL` | Not sufficient by itself to publish |
| `HIGH_RISK` used in review policy | Risk category, not another information class |
| Case label is lower than required run controls | No source requirement automatically rewrites case label |
| Unclassified material or changed material classification | Detailed handling Needs confirmation; no lower-class default established |

**Reference settings:**

- `policy.auto_publish_classification: INTERNAL`
- `policy.require_human_review_for: [HIGH_RISK, RESTRICTED]`
- `policy.self_approval_allowed: false`

**Source:** S, p. 62, §17.2.1; p. 90, Appendix F.

**Earlier equivalent obligations:** [API-CLS-001](02_api.md#api-cls-001), `DAT-CLS-001`, [BAT-CLS-001](04_batch_functions.md#bat-cls-001), `API-AC-034`, `DAT-AC-023`, `BAT-AC-027`.

**Needs confirmation — BR-OQ-012:** Material-class provenance, severity encoding, unclassified-material handling, version activation, and per-class routing/redaction/retention/approval mappings. No seventh policy input or new public classification property is established.

### BR-027–BR-032 — Review, Overrides, Publication, and Presentation

#### Reviewer Eligibility and Decision Capture

| Condition | Confirmed result |
|---|---|
| Actor meets policy-defined pool, minimum role, organizational-role and separation-of-duty requirements | Eligible to perform applicable review, subject to task/hash/state checks |
| Analyst attempts to approve own high-risk recommendation | Reject; cannot publish through self-approval |
| Assigned approval task subject to source `no self approval` constraint | No self-approval exception is established |
| Review panel loaded | Show exact candidate, source citations, model/prompt version, and policy reasons |
| Required review fields incomplete | Approve and Reject remain disabled |
| Source evidence inspection | Must be available before approval |
| Exact candidate hash matches decision and remaining guards pass | Capture decision, actor, timestamp, evaluated hash, rationale, optional annotations |
| Candidate changed after review | Reject decision as stale and audit |
| Accepted decision | Immutable historical record; HTTP `200` decision result is not unconditional publication |

**Source:** S, p. 11, §2.1.2; p. 45, §12.2; pp. 57–58, Chapter 16; pp. 83, 85, 89–90.

**BR-027 scope distinction:** High-risk self-approval is explicitly prohibited. Appendix B.1 additionally gives `approval_tasks` the constraint `no self approval`, and Appendix F has `self_approval_allowed: false`. The source establishes no assigned-task self-approval exception. Identity of the disallowed originating actor and scope outside approval tasks remain unresolved.

**BR-028 hash comparison:** Approval applies only to the exact reviewed content hash. Hash equality is an exact binding, not a similarity or “materially unchanged” exception.

**Needs confirmation — BR-OQ-001, BR-OQ-013:** Definition of self/originator, assignment-specific read/action rights, complete required review fields, rationale blank/length rules, decision literals, hash algorithm/canonical bytes, task-state guards, quorum, and whether actual source opening is a submission prerequisite. “Must be able to inspect” does not confirm a mandatory click-completion guard.

#### Expiry, Override, and Rework

| Condition | Rule | Confirmed result |
|---|---|---|
| Review task reaches configured SLA expiry | BR-029 | Reassign or escalate; no silent approval |
| Expired review task receives decision | BR-029 | Exact acceptance/state/race rule Needs confirmation; expiry cannot itself approve |
| Override lacks elevated role, secondary reviewer, or audited reason | BR-030 | Prerequisites are unsatisfied; ordinary review/admin status cannot bypass them |
| Authorized override has all prerequisites | BR-030 | May follow explicitly authorized override policy while preserving audit lineage |
| Denied recommendation is reworked | BR-030 | Create new run revision; do not retroactively mark denied historical content approved |
| Reject decision recorded | BR-030/BR-013 | No automatic `PENDING_APPROVAL → IN_PROGRESS` linkage is confirmed |

**Source:** S, pp. 45–46, §§12.2.1, 12.3.2; p. 89, `TST-010`.

**Needs confirmation — BR-OQ-013, BR-OQ-014:** Review SLA duration/unit/timezone/start point/equality, routing priorities, expiry race, elevated roles, secondary-reviewer eligibility, override scope and endpoint, reason constraints, and rework initiation contract.

#### Publication Decision Table

The conditions below are cumulative. The table describes gate consequences, not a complete policy-selection matrix.

| Current authorization | Required evidence/anchors | Applicable policy satisfied | Required exact-hash approvals satisfied | Artifact unchanged | Result |
|---|---|---|---|---|---|
| Yes | Yes | Yes | Yes, or no human decision required by applicable policy | Yes | Commit satisfied gate and final response pointer atomically; expose published result afterward |
| No | Any | Any | Any | Any | Do not publish; recompute/reject stale authorization |
| Any | No | Any | Any | Any | Do not publish unsupported/unresolvable content |
| Any | Any | No | Any | Any | Do not publish |
| Any | Any | Any | No | Any | Do not publish unapproved required-review content |
| Any | Any | Any | Any | No | Old approval cannot publish changed artifact |

**BR-031 — Confirmed procedure:**

1. Resolve exact candidate and reviewed hash.
2. Recompute current tenant/workspace/source authorization.
3. Verify required evidence, cited immutable versions, and resolvable anchors.
4. Verify applicable deterministic policy, including BR-026.
5. Verify exact-hash decisions and eligible actors/separation of duties.
6. Reject wrong-artifact replay under old approval.
7. Commit gate satisfaction and final pointer in the same transaction.
8. Display publication only after commit.

`ApprovalDecisionRecorded` causes publication validation; a rejection event is not permission to publish. No separate public Publish endpoint is confirmed.  
**Source:** S, pp. 12, 45–46; p. 87, C.1.

**Needs confirmation — BR-OQ-012, BR-OQ-013:** Non-review invocation, in-flight policy selection, gate/revalidation transaction mechanism, actor/hash lookups, failure codes, and case-resolution linkage.

#### Artifact, Progress, and Accessibility Rules

**BR-032 — Confirmed:**

- Use accessible text labels `DRAFT`, `NEEDS_REVIEW`, and `PUBLISHED`; styling alone is insufficient.
- Keep artifact labels separate from Case, Run, and Review state vocabularies.
- Partial processing, accepted `202`, dropped connection, or generation completion is not approval/publication.
- Create admitted runs immediately and show retrieval, generation, and policy stages.
- Refresh reconstructs progress from server state.
- SSE offsets increase monotonically; reconnect uses `Last-Event-ID` and backfills retained events only within caller scope.
- Source inspection remains available before approval.
- Target WCAG 2.2 AA, visible focus, semantic regions, keyboard ordering, and meaningful state announcements only.

**Source:** S, pp. 13, 55, 57–59, 83, 89, `TST-011`.

**Needs confirmation — BR-OQ-024:** Artifact/state projection, cursor retention/expiry, event payloads, notification channels, exact focus/error behavior, summary formulas, and routes. Illustrated “Evidence Coverage” `97.6%` and “5 verified citations” are fixtures, not thresholds or formulas.

### BR-033–BR-037 — Onboarding, Source Synchronization, Retries, and Replay

#### Onboarding and Connector Decisions

| Condition | Rule | Confirmed result |
|---|---|---|
| Provisioning completes required policy, encryption references, role bindings, quotas, connector stubs | BR-033 | One idempotent provisioning workflow outcome |
| Provisioning incomplete | BR-033 | Visible incomplete state; block connector sync |
| Historic backfill | BR-033 | Bounded windows, stable source IDs, per-batch reconciliation receipts |
| Connector advertises list/fetch/delta cursor/ACL/delete support | BR-034 | Respect advertised capability contract |
| Capability unsupported | BR-034 | Lower-trust ingestion mode and explicit visible warning, not silent assumption |
| Credentials stored | BR-034 | Workspace-scoped references to dedicated secret store |
| Operator revokes credentials before queued job executes | BR-034 | Job fails `CONNECTOR_REAUTH_REQUIRED`, without token disclosure |
| Provider item ingested | BR-035 | Preserve source identity, permissions, change history, durable outcome |
| Some preceding cursor items lack durable outcomes | BR-035 | Do not advance beyond them |
| All preceding items have durable outcomes | BR-035 | Cursor may advance under provider ordering contract |
| Malformed document exhausts bounded retries | BR-035 | Quarantine with reason code, correlation ID, remediation path; retain ledger exception |
| Other batch items remain processable | BR-035 | Remaining batch may proceed with recorded exception |
| Source deletion detected | BR-035 | Write tombstone and schedule index removal; soft-deleted source unavailable |
| Source ACL changes | BR-004/BR-035 | Invalidate affected retrieval cache before new results |

**Source:** S, pp. 27–29, §§7.1–7.3; p. 51, §14.1.2; p. 78, §22.1.

**Needs confirmation — BR-OQ-015, BR-OQ-019:** Provider permissions, capability trust restrictions, sync states/options, cursor/high-watermark order and types, durable-outcome stage, batch sizes/windows, source-ID uniqueness, partial/empty completion, reauthorization, and provisioning compensation. Cursor advancement is not necessarily index readiness.

#### Retry and Scheduling Decisions

| Failure or operation | BR-036 treatment |
|---|---|
| Transient dependency fault | Bounded exponential backoff, randomized jitter, per-dependency circuit breaker |
| Schema validation or permission failure | Permanent; do not automatically retry |
| Connector `Retry-After` response | Honor guidance, workspace quotas, and backoff/jitter controls |
| Read operation transient fault | May retry |
| Consequential mutable tool operation | Idempotency and human authorization remain required |
| Invalid model output | Bounded structured-validation retries; no publication |
| Malformed source document | Source-specific bounded retry/quarantine rules apply |
| Large tenant and smaller workspace compete for connector work | Fair scheduling must prevent starvation |
| Extraction/embedding scaling | Queue age and throughput are source scaling inputs |
| API scaling | Utilization and latency are source scaling inputs |

**Source:** S, p. 19, §4.2.1; pp. 28–29, §7.3; p. 38, §10.2.2; p. 42, §11.3.2; p. 49, §13.3.1.

**Needs confirmation — BR-OQ-015:** Retry counts/delays, circuit-breaker thresholds, elapsed-time ceilings, parser-poison versus schema-invalid request classification, fair-queue algorithm, starvation bound, and schedule. No exponential-backoff equation with invented base/max delay is supplied.

#### Authorized Replay and Incident Repair

**BR-037 — Confirmed:**

1. Authenticate operator and validate authorized scope.
2. Require audited reason.
3. Perform dry-run validation.
4. Enforce a scope limit.
5. Preserve original event identity unless explicit schema transformation includes provenance linkage.
6. Resume through original deduplication, revision, access, and domain guards.
7. Compare source fingerprints/indexed versions and repair broken links from outbox.
8. Preserve accepted source metadata rather than compensating an index failure by removing source data.
9. For delayed indexing, pause only faulty connector/indexer shard, diagnose scoped evidence, use bounded replay, verify fingerprints and denied-access probes, and document audit IDs/time window/blast radius/quality effect/preventive action.
10. For suspected ACL leak, suspend affected aliases, revoke cached evidence, preserve audit traces, replay scoped ACL revisions, and re-enable only after negative access tests pass.

**Source:** S, pp. 49–50, §§13.2.2–13.3.2; p. 79, §22.2.2; p. 90, §F.1.

**Needs confirmation — BR-OQ-016:** Replay roles, reason format, numeric/time scope, dry-run transport, migration provenance, worker fencing/takeover, and recovery thresholds. Replay does not make a still-invalid authorization or schema condition valid.

### BR-038–BR-041 — Retention, Independent Approval, Export, and Deletion

#### Retention Decision Table

| Data/condition | Confirmed rule | Period or missing detail |
|---|---|---|
| Routine case-retention candidate not `CLOSED` | Ineligible for routine case-retention job | No inferred application to all logs or decommission inventory |
| Closed case otherwise ineligible | Do not purge through routine retention | Eligibility criteria unresolved |
| Eligible closed case | Apply authorized retention with closure lineage and hold exceptions | Workspace retention classes/periods unresolved |
| Protected legal-hold record | Retain and receipt protected exception | Hold scope/start/release/races unresolved |
| Run material | Select retention using BR-026 maximum material class | No class-specific duration supplied |
| Diagnostic logs | Default TTL `30` days | Start/cutoff/timezone/sweep unresolved |
| Security audit logs | Distinct fictional `7`-year retention | Calendar-year calculation and final corporate policy unresolved |
| Versioned cache | Short TTL; purge early for authorization change | Numeric TTL unresolved |
| Soft-deleted entity | Not retrievable | Final scheduled tombstone purge timing unresolved |
| Case idempotency / reference workflow dedup | Separate `24`-hour scopes | Not a universal data-retention period |

**Source:** S, pp. 26, 51–53, 62, 66, 90.

**Needs confirmation — BR-OQ-017:** Corporate retention, eligibility and effective dates, shared source versions/objects, retained approved lineage versus source purge, archive receipts, backup treatment, and scheduling. Retention periods do not authorize a new purge job schedule.

#### Independent Lifecycle Approval

| Actor/check context | BR-039 result |
|---|---|
| Single Admin without independent approval | Reject export/delete |
| Same person tries to satisfy the export two-person control alone | Insufficient |
| `Admin + approver` and required independent approval checks satisfied | May accept validated authorized lifecycle work |
| Required approval checks satisfied but legal hold protects deletion target | Hold protection still applies |
| Export/delete job accepted with HTTP `202` | Durable work accepted; completion remains separate |

**Source:** S, p. 78, Chapter 22 invariant; p. 83, A.2; p. 88, `T-11`.

**Needs confirmation — BR-OQ-001, BR-OQ-018:** Exact actors, check sequence, proof schema, validity/reuse period, independence definition, and tenant-versus-workspace scope. The confirmed two-person export control does not establish how many separate approval records or endpoints are used.

#### Export and Deletion Procedures

**BR-040 — Confirmed export:**

1. Validate lifecycle scope and independent approvals.
2. Select authorized case metadata, approved artifacts, source references, and audit manifests.
3. Package them with checksums.
4. Exclude secrets and internal model prompts.
5. Retain manifest/integrity and actual completion evidence.

**BR-041 — Confirmed deletion:**

1. Validate scope and independent approvals.
2. Resolve inventory used by deletion and data-subject access requests.
3. Enforce legal holds.
4. Write tombstones for eligible targets.
5. Remove eligible blobs and index entries.
6. Record completion receipts and protected retained-record exceptions.
7. Verify inventory outcomes.
8. Produce `TenantDeletionVerified` with manifest/receipt evidence for closing the purge record.

Partial deletion must not be portrayed as verified completion. No force-delete exception is supplied.  
**Source:** S, pp. 79–80, §§22.3.1–22.3.2; p. 87, C.1; p. 89, `TST-013`.

**Needs confirmation — BR-OQ-018:** Package/checksum formats, inventory consistency during concurrent changes, shared-object extent, held-only/partial completion state, backup/relational deletion, subject matching/redaction, receipt status/download contracts, and approval expiry. `TenantDeletionVerified` is not an export or provisioning completion event by assumption.

### BR-042 — Daily Usage and Period-End Calculations

| Calculation or period | Confirmed inputs/output | Needs confirmation |
|---|---|---|
| Invocation token usage | `token_ledger.in_tokens`, `out_tokens`, run and specific deployment attribution | Reservation versus actual billing, count units/range, provider corrections |
| Per-tenant usage attribution | Model invocations, embeddings, storage, indexing; workspace cost center and model deployment version | Ledger identity, cost rates, currency, precision |
| Storage accounting | Raw files, normalized text, chunk vectors, replication overhead tracked separately | Cost conversion and storage unit conventions |
| Daily rollup | Show budget, forecast, and rejected excess requests | Reporting day/timezone, launch time, cutoff inclusivity, zero-use rows |
| Forecast | Required rollup concept | Formula, horizon, minimum observation count, confidence, rounding |
| Daily rerun/late usage | Idempotent cross-service write obligations remain | Aggregate identity/replacement/versioning, late-arrival and correction policy |
| Monthly availability reporting | Separate SLO period under BR-044 | Calendar versus rolling month, eligible-request denominator |
| Month/quarter/year-end financial settlement | Not described | No close, billing, invoice, tax, or settlement rule established |

**Source:** S, p. 38, §10.3.1; p. 65, §§18.2.1, 18.3.1; p. 68, §19.1.2; pp. 83, 85.

**Needs confirmation — BR-OQ-020:** Executable aggregation/forecast/cost formulas, exchange units, currency/rounding, accounting timezone/cutoffs, correction policy, and period finalization. No generic zero-denominator, round-half-up, or end-of-month rule is selected.

### BR-043–BR-044 — Privacy, Audit, Reliability, and Recovery

#### Privacy and Audit Conditions

**BR-043 — Confirmed:**

- Extraction tags likely personal data.
- Gateway redacts nonessential fields before provider invocation where policy permits.
- Model/providers receive scoped context, not raw connector tokens or unrestricted database access.
- Model/tool calls receive no secrets outside declared scope.
- Public fields never expose secrets/raw provider credentials.
- Errors exclude connector credentials, full prompts, retrieved documents, and unauthorized existence.
- Diagnostics contain identifiers/policy outcomes, not user-document content or API secrets.
- Log token counts/digests, not entire prompts by default.
- Required accepted-transition audit evidence is retained independently of diagnostic sampling.
- Audit entries are append-only, batch-hash chained, and exported to independently controlled retention storage.
- Auditor sees permitted decision metadata, prompt-template digests, and access events within redacted scope, not automatic full-source access.
- Vault-backed secrets use scoped managed identity; service credentials rotate automatically; encryption keys rotate under defined policy without request-path bulk re-encryption.
- Blob keys contain tenant/workspace/document/version/object role; public names opaque; encryption at rest and access-controlled short-lived signed URLs mandatory.
- Staging uses synthetic data/test connectors; production data is forbidden in development.

**Reference setting:** `observability.trace_sample_rate: 0.10` applies to diagnostic sampling, not permission to sample away obligatory audit evidence.

**Sources:** S, pp. 11, 19, 21, 52, 54, 61–66, 71, 84, 90.

**Needs confirmation — BR-OQ-021:** PII tags and policy exceptions, audit-chain canonical bytes/batch boundaries, redaction projection, secret/key isolation/rotation/destruction, URL lifetime, and telemetry retention calculations.

#### Service Targets, Alerts, and Degraded Operation

| Condition/target | BR-044 requirement | Boundary detail |
|---|---|---|
| Public API availability | Target `99.9%` monthly | Measurement denominator/exclusions/month definition unresolved |
| Case creation latency | P95 `<300 ms` under defined load | Source §2.3.1 also says “within 300 ms”; equality clarification required |
| Search latency | P95 `<1.5 s`, excluding remote connector fetch | Model-generation latency measured separately |
| User-impacting failure budget, stale ACL, missing approval enforcement | Paging category | Actual thresholds/routing unresolved |
| Routine token-spend anomaly | Ticket with configured owner and threshold | No specific owner/threshold assigned here |
| Model provider outage | Disable new generation admission; manual case/evidence work available; visible degraded state | Page on-call only when availability budget impacted |
| Vector degradation | Lexical retrieval may continue with visible reduced-quality flag | No lower safety/approval/classification controls |
| Suspected ACL leak | Scoped containment and negative access tests before search re-enable | BR-037 applies |
| Regional persistence | Primary-region writes, one warm recovery region; secondary restore under incident command | No active/active mutation |
| Recovery objective | RPO `<=15 minutes`; RTO `<=4 hours` | Continuous backups; targets are not backup launch schedules |
| Recovery/chaos verification | Test relational/object consistency, index recipes, provider `429` storms, lost heartbeat, duplicates, object failures, primary outage | Measure safety and recovery time |
| Network exposure | No public-IP datastore; only declared flows; controlled explicit worker egress | Does not invent probe response schemas |

**Sources:** S, pp. 18–20, 65, 68–70, 79; p. 89, `TST-012`.

**Reference workload:** `2,000` active daily users, `60` requests/second steady, `180` burst, `100,000` indexed documents per tenant maximum, `20` concurrent AI runs per large tenant. Typical `1 MB` source yields approximately `40–120` chunks. These are reference workload/sizing assumptions, not universal user-request or normalization limits.  
**Source:** S, p. 68, §19.1.

**Needs confirmation — BR-OQ-022:** Metric formulas, P95 method, monthly boundaries, failure budgets, burn-rate thresholds, forecast/ticket/page configuration, degraded mode vocabulary, restore inventory/roles, heartbeat takeover, and detection/re-enable thresholds.

### BR-045–BR-046 — Evaluation, Change Control, and Release Decisions

#### Evaluation and Release Gate Table

| Input or condition | Confirmed result |
|---|---|
| Reference evaluation corpus | `1,200` synthetic permission-controlled cases spanning retrieval, refusal, ambiguity, adversarial evidence |
| Each example | Store expected citation set and decision outcome |
| Corpus lifecycle | Frozen, versioned, independently reviewed for acceptance-data leakage |
| Expected fixtures replaced maliciously | Dataset version/signed-manifest control must detect poisoned fixture use |
| Grounded citation precision | Target `>=0.97` |
| Unsupported-claim rate | Target `<=0.02` |
| High-risk policy recall | Target `1.00` on frozen safety suite |
| Confidence/distribution behavior | Report confidence intervals and distribution shift by domain |
| Low statistical confidence | Blocking release outcome, not equivalence |
| Critical isolation or approval test exception | Not acceptable: zero exceptions required |
| Unmitigated critical cross-tenant/approval-bypass finding | Block promotion regardless of benchmark score |
| Prompt/model update | Require re-evaluation even if rolled forward independently |
| Randomized test | Record seed |
| Successful evaluation execution | Not automatic quality pass or release promotion |

**Source:** S, pp. 74–76, Chapter 21; pp. 88–89, D.1 and E.1–E.2.

The source names `SEC-001` through `SEC-012` as release-blocking critical requirements, but does not provide their individual definitions or a one-to-one mapping to `T-01`–`T-12`. No such mapping is invented.

**Needs confirmation — BR-OQ-023:** Metric numerator/denominator, macro/micro aggregation, domain weighting, confidence method/level, zero-denominator and incomplete-case treatment, rounding, missing corpus behavior, fixture signature verification, and exact scorecard gate composition.

#### Controlled Change and Release Rules

**BR-046 — Confirmed:**

1. Baseline changes require an architecture-decision record.
2. Changed invariants link to at least one negative test.
3. Proposed changes carry impacts for behavior, data migration, threat surface, and operating cost.
4. Approved change increments minor design revision; incompatible protocol change increments major revision.
5. Contract changes are additive when nonbreaking; removals require migration.
6. Repository-controlled OpenAPI governs REST; protobuf IDL governs internal gRPC. CI prevents breaking field deletions/incompatible enum changes.
7. Expand-and-contract migration adds nullable fields, backfills in bounded batches, then enforces constraints.
8. Do not remove a required field while active readers depend on it.
9. Predeploy migrations remain backward compatible; postdeploy enforcement follows old-replica drain.
10. Rollback plans state whether new-binary writes remain readable.
11. Nonsecret defaults are source controlled; environment configuration signed; credentials/keys only vault-backed references.
12. CI performs static/dependency analysis, unit/contract tests, SBOM, image signing.
13. Production deploys only digests verified against allowed build identity.
14. Assess state-machine/schema compatibility before traffic movement.
15. Canary compares latency, errors, authorization denials, and AI-quality regression against baseline.
16. Regression triggers automated traffic rollback, not automatic database down-migration; binary routing reverses first; compensation only when explicitly supported.
17. Security/SRE validate egress, secrets, backups, alerts before promotion.
18. Release record binds image digest, schemas, prompts, model-routing policy; deployed binary/prompt/policy versions reconstructible.
19. Security-control evidence is independently negatively verified and signed under the source exit criteria.
20. Minimum release pack includes unit, schema evolution, negative authorization, workflow replay, staging connector sync, visual accessibility, search recall, grounding, policy recall, load, and disaster recovery verification. Sign outputs and reference them by release digest.
21. Select region, search provider, identity provider, approved deployments, corporate retention, connector permissions in dated architecture decisions before implementation lock; resolve per-tenant key isolation versus rotation throughput before enterprise general availability.

**Sources:** S, pp. 8–10, 15, 20, 52, 55, 71–73, 88–90.

**Needs confirmation — BR-OQ-023:** Impact scale/formulas, governance approval roles, revision allocation/reset rules, signature/digest schemas, canary thresholds/duration, release stage dependencies, supported compensation, and exact critical requirement definitions. No decision date, owner, or approval is assigned here.

### Effective Periods and Numeric Boundary Register

| Rule | Source value or period | Confirmed interpretation | Unresolved boundary |
|---|---|---|---|
| BR-007 / BR-010 | Case revision initial `1` | `BIGINT`; monotonic accepted changes | Increment formula, overflow, JSON transport |
| BR-008 | Case binding `24` hours | Actor/request fingerprint to original outcome | Start, equality at expiry, cleanup/reuse |
| BR-008 / BR-037 | `workflow.replay_dedup_hours: 24` | Reference workflow dedup scope | Non-case/event retention after expiry |
| BR-015 | `25 MB` | Configurable per-file cap | Byte conversion and exact MIME/subtype boundaries |
| BR-019 | Candidate `80`, selected `10`; MCP `int<=10` | Backend/tool upper budgets | Retry/selection counting, MCP lower/default |
| BR-023 | Depth `8`, calls `16` | Do not exceed defined bounds | Root-depth convention, repeated/replayed call counting |
| BR-023 | `180` seconds | Reference run timeout | Start, pause/review wait, equality, state |
| BR-029 | Configured review SLA | Expiry reassigns/escalates, never approves | Duration, start, timezone, equality |
| BR-038 | Diagnostic `30` days; audit `7` years | Distinct reference retention policies | TTL/year arithmetic, cutoff/timezone |
| BR-042 | Daily | Daily rollup cadence | Accounting day, launch/cutoff, late data |
| BR-043 | `0.10` | Reference diagnostic trace sample rate | Sampling mechanism; mandatory audit unaffected |
| BR-044 | Monthly `99.9%`; P95 latency targets | Reference service objectives | Period/denominator/percentile calculation |
| BR-044 | RPO `<=15 minutes`; RTO `<=4 hours` | Inclusive reference targets | Measurement start/end and recovery scope |
| BR-045 | `>=0.97`, `<=0.02`, `1.00` | Threshold equality satisfies the stated comparator, subject to other gates | Metric calculation/precision and rounding |
| BR-025 / BR-026 / BR-046 | Versioned policy/configuration | Store applied versions and reproducible inputs | Effective-from dates, in-flight activation, retroactivity |

No undocumented rounding, monetary precision, business-day conversion, cron expression, policy activation date, or general boundary default is selected.

## Application Points and Validation Conditions

### Enforcement and Data Mapping

The mappings preserve existing identifiers. “Read” and “update” describe required business effects, not new SQL column declarations or public JSON fields. Rules not tied to a confirmed screen remain service/operational requirements; no additional screen is invented.

| Rule | Enforcing screen/API/job identifiers | Data read or updated | Satisfied and unsatisfied validation |
|---|---|---|---|
| BR-001 | All protected screens/APIs; API-027; `BAT-CTX-001–003` | Read DAT-019/020 trusted identity; retain context | Valid identity proceeds; missing tenant/unexpected algorithm rejected before protected data/work |
| BR-002 | `SF-AUTH-001`; all resource operations; API-AUTH-001; scoped jobs | Read DAT-019–022, case/source/task attributes | Matching role plus attributes proceeds; visible control alone cannot grant operation |
| BR-003 | API-AUTH-002/003; all tenant-owned jobs/storage | DAT-COM-F02; DAT-001–003; tenant-owned objects | Foreign ID non-disclosing; cross-tenant workspace write rejected; pooled context reset |
| BR-004 | `SCR-003-A04`, `SCR-002-A09`; API-010/020–022; BAT-006/007/011 | Read/update DAT-022/034; read evidence/version | After revocation next query contains no forbidden text; old ACL digest/cache cannot authorize publication |
| BR-005 | `SF-GEN-011`; API-008/046/047; BAT-010 | DAT-037–042; tool authorization/injection records | Approved pinned grant dispatches; hostile evidence/discovery/equivalent-tool bypass denied |
| BR-006 | All mutations; API-VAL-001; applicable BAT jobs | Approved request and trusted context; safe error DAT-061 | Invalid schema `422`; no work allocation before validation; `202` not completion |
| BR-007 | `SCR-002-A02/A04/A07`, `SCR-007-A02`; API-003/017/050 | DAT-003/004; DAT-002-F10 | Current revision accepts guarded change; stale case `409 CASE_VERSION_CONFLICT`, state unchanged |
| BR-008 | `SF-GEN-008/009`; API-IDEM; BAT-008/022 | DAT-044/045; DAT-014 event/revision | Identical key original outcome; changed fingerprint conflict; repeated event one accepted effect |
| BR-009 | Case/policy/storage services; API-TXN; BAT-004/008/009/011/024 | DAT-003/004/006/012/014/031/034/043 | Immutable history retained; failed index preserves source; gate/pointer and outbox boundaries enforced |
| BR-010 | `SCR-001-A03`, `SCR-002-A03`; API-001/051; BAT-001 | DAT-003/024 | New `NEW`/revision `1`/default `INTERNAL`; correction reason/provenance required |
| BR-011 | `SCR-001-F04`, `SCR-002-F05–07`; API case mutation | Read DAT-003-F11/12; update F13 | Approved impact/urgency matrix determines priority; model-only priority prohibited |
| BR-012 | `SCR-002-F15`, `SF-GEN-003`; case deadline processing | DAT-002-F11; DAT-003-F16/17; DAT-TIME | Calendar/timezone deadline; prediction cannot alter it; locale leaves durable order unchanged |
| BR-013 | `SCR-002-A04/T01–T06`; API-003 | DAT-003-F04/05; DAT-004/025 | Each confirmed edge with guards accepts; unlisted normal edge rejects without mutation |
| BR-014 | `SCR-002-A07/A08/T07/T08`; API-017/052 | DAT-026; DAT-003/004; approved references | Closure snapshot immutable; reopening only explicit new revision; missing edge/actor tests blocked |
| BR-015 | `SCR-002-A05/F20`; API-004; BAT-003 | DAT-023/029; file metadata | Supported matched file within defined cap proceeds; oversized/mismatch/decompression unsafe fails closed |
| BR-016 | API-004/018; BAT-003/004 | DAT-029 quarantine; DAT-031 exclusion | Scan before parse; unsafe no index; macros/remote embedded fetch never executed |
| BR-017 | `SCR-003-F04–09/A03`; API-004/021/022/057; BAT-003 | DAT-006/007/030/035 | Claims/anchors preserved; opted OCR marked; changed pipeline side-by-side; unresolved citation not displayed |
| BR-018 | `SCR-002-F23`, `SCR-003-F09/10`; BAT-003/010 | DAT-029-F02–05; evidence/policy | Low-quality safe source viewable but not autonomous support; exact threshold tests await confirmation |
| BR-019 | `SCR-003-A01–03/A06`; API-010/021/022/046; BAT-010 | DAT-010/031/033/034 | ACL-filtered bounded verified evidence; insufficient support `NO_SUPPORTED_EVIDENCE`, no fabrication |
| BR-020 | Indexer; BAT-004/005/009/019; API-010 indirectly | DAT-031/032; source fingerprints/coverage | Parallel alias activates only after checks; queue empty alone not readiness; source survives index failure |
| BR-021 | `SCR-007-F03/A03`; API-008/026; BAT-010 | DAT-002-F06; DAT-036; DAT-051 | Specific approved deployment route; unsafe outage fallback prohibited |
| BR-022 | API-008; BAT-010; `SCR-004-A04` | DAT-037/038; DAT-016 usage | Valid structured candidate proceeds; unknown fields/invalid citation/control injection `MODEL_OUTPUT_INVALID`, no publish |
| BR-023 | `SCR-004-F02–06/A01–04`; API-005/006/019/032; BAT-010 | DAT-008/009/040/046 | Acyclic bounded plan and checkpoint before dispatch; excess/stop condition no further unsafe work |
| BR-024 | `SCR-002-A06`, `SCR-010-F04`; API-005/008; BAT-010 | DAT-002-F04; DAT-008-F05; DAT-016/055 | All admission thresholds pass; failed threshold `429 Retry-After`; quota exhausted no class/model switch |
| BR-025 | `SCR-007-F08/09`, `SCR-005-F09`; API-020/024/050; BAT-010/011 | DAT-017 normalized inputs/version/result | Six concepts stored with rule version; LLM cannot change deterministic result |
| BR-026 | `SCR-002-F10`, `SCR-007-F09–11`; API-005/008/020; BAT-010/011/013 | DAT-051/classified material; DAT-017; retention/routing records | Mixed `INTERNAL`/`RESTRICTED` uses all four restricted controls; case-label/ACL shortcut fails |
| BR-027 | `SCR-005-A03/A04`; API-023/024; review routing | DAT-011; DAT-019/020; originating actor | Eligible independent reviewer proceeds; own high-risk approval and assigned-task self exception not permitted |
| BR-028 | `SCR-005-F05–13/A02–04`; API-023/024; BAT-011 | DAT-039/011/012/010/017 | Exact panel and complete form; changed hash stale/audited; accepted decision immutable |
| BR-029 | `SCR-005-A05`; API-023/024; BAT-012 | DAT-011-F05–07; routing evidence | Expiry reassignment/escalation recorded; never implicit approval |
| BR-030 | `SCR-005-A06`, `SCR-002-A10`; API-053/005 | DAT-043-F03; DAT-039/012 | Elevated actor/secondary reviewer/reason required; rework new revision, history not retroapproved |
| BR-031 | `SCR-002-A09`; API-020; BAT-011 | DAT-003-F15; DAT-010–012/017/039/043 | Exact currently permitted supported artifact atomically published; any failed gate blocks |
| BR-032 | `SCR-002/003/004/005`; API-007; progress effects of BAT-010 | DAT-062/049; persisted DAT-008/009 | Accessible truthful labels/source view/server reconstruction; connection loss/private backfill not completion/access |
| BR-033 | `SCR-006-F09`; API-056/009; BAT-018/019 | DAT-001/002/020/027/052/058 | Required provisioning set complete and idempotent; incomplete blocks sync; bounded receipts/readiness |
| BR-034 | `SCR-006-F02–04/A02/A03`; API-009/054/055; BAT-002 | DAT-027; vault references | Unsupported visible lower trust; revoked queued job `CONNECTOR_REAUTH_REQUIRED`, no token |
| BR-035 | `SCR-006-F05–08/A05/A06`; API-009/025; BAT-002/007/019 | DAT-005/015/028; tombstones/index | Cursor only past durable outcomes; poison exception retained; source deletion unavailable |
| BR-036 | API-RTY; BAT-002/003/008/010/024 | DAT-015 retry state; DAT-047/055 | Bounded transient retry/provider guidance/fairness; permission/schema failures not retried |
| BR-037 | API-033/034; BAT-009/022; incident procedures | DAT-014/045–048/058; source/index fingerprints | Unguarded replay denied; scope/provenance verified; negative access tests before resume |
| BR-038 | API-036; BAT-013/014; routine lifecycle | DAT-026/053/018; eligible data/archives | Only eligible closed routine cases; held protected; category TTLs distinct and receipted |
| BR-039 | API-014/015; BAT-020/021; placement unresolved | Independent authorization proof; lifecycle inventory | Single Admin denied; independent checks necessary; acceptance remains `202` |
| BR-040 | API-014; BAT-020 | DAT-059/003/039/013 | Authorized package/manifest/checksums includes required categories, excludes secrets/internal prompts |
| BR-041 | API-015/029/036; BAT-021 | DAT-053/018/035/031/059 | Held records retained/receipted; real removals verified; partial/accepted work not verified deletion |
| BR-042 | `SCR-010-F01–04/A01`; API-012; BAT-016 | DAT-016/054-F04; cost center/deployment | Attributed daily budget/forecast/rejected requests; exact totals require approved formulas/day |
| BR-043 | `SCR-008`; API-008/011/035/057; BAT-003/014/015 and secret rotation capability | DAT-013/052/054; PII tags/archives | Safe scoped provider/public/diagnostic data; immutable archive; historical edits rejected |
| BR-044 | `SF-SCP-006`; API-038–042; BAT-025; incident controls | DAT-055/063; safe metrics/modes/recovery | Degraded manual/evidence work and safety intact; targets measured; restore under incident command |
| BR-045 | `SCR-010-A02–04`; API-013/045; BAT-017/026 | DAT-057; frozen expectations/signed results | Actual reproducible metrics; critical exception/low confidence/poison fixture blocks acceptable release |
| BR-046 | API-030/031/037/043/044; BAT-023/026 | DAT-056/060/061; signed config/build/tests | Negative-test link, compatibility, verified digest/sign-off; regression traffic rollback, no unsupported data reversal |

### Source Verification Coverage

| Existing source identifier | Rules validated | Required observable result |
|---|---|---|
| `TST-001`, `TST-002` | BR-008/010 | One case/identical response; changed key body `409 IDEMPOTENCY_CONFLICT` |
| `TST-003`; `T-01` | BR-001–003 | Foreign tenant valid ID receives absent-ID-equivalent non-disclosing response |
| `TST-004`; `T-08` | BR-004/019/035 | No forbidden evidence on next query after source revocation |
| `TST-005`; `T-02` | BR-005/022 | Invalid model schema `MODEL_OUTPUT_INVALID`; no publish; hostile evidence no authority |
| `TST-006`; `T-03` | BR-028/031 | Wrong/prior hash stale and audited |
| `TST-007`; `T-07` | BR-008/009/037 | Exactly one accepted business transition; source negative test repeats event `100` times |
| `TST-008` | BR-024/036 | Capped retries and controlled admission during provider `429` bursts |
| `TST-009` | BR-017/019/031 | Missing citations yields needs-review or unsupported outcome, never fabricated approval |
| `TST-010` | BR-029 | Expiry produces no implicit approval; escalation recorded |
| `TST-011` | BR-032 | Keyboard action unblocked; visible focus |
| `TST-012` | BR-044 | Recovery safety and RPO/RTO within stated targets |
| `TST-013` | BR-038/041 | Held protected records retained and receipted |
| `TST-014`; `T-10` | BR-005/023 | Arbitrary tool denied before dispatch; recursion bounded by tool/step/time budgets |
| `TST-015`; `T-04` | BR-015/016 | Unsafe PDF quarantined; no indexing; parser scan/sandbox/bounds enforced |
| `TST-016` | BR-045/046 | Safety-regressed canary blocks promotion |
| `T-05`, `T-06` | BR-021/043 | No credential leakage in traces/provider requests; no unapproved outage fallback |
| `T-09` | BR-043 | Historical modification rejected; append-only archive preserved |
| `T-11` | BR-039/040 | Single-Admin export denied; two-person approval/manifest control |
| `T-12` | BR-045 | Replaced expected fixtures fail version/signed-manifest integrity control |

**Source:** S, pp. 88–89, Appendices D–E.

### Composite Acceptance Criteria

All fixtures are synthetic. Include successful, empty, mixed-permission, mixed-classification, adversarial, malformed, delayed, duplicate, and partial-failure cases. Record randomized seeds. Tests requiring unresolved formulas, actors, algorithms, or state guards remain blocked by the associated question rather than inventing fixtures.  
**Source:** S, p. 74, Chapter 21 invariant; p. 89, E.1.

#### BR-AC-001 — Mixed Classification Across All Four Controls

1. Create an authorized `INTERNAL` case.
2. Include permitted, anchored, quality-appropriate `RESTRICTED` evidence.
3. Execute run/model/policy processing with approved controlled per-class policy fixtures.
4. Inspect internal routing, redaction, retention, and approval provenance.
5. Attempt publication without required human decision.

**Expected:** All four controls select applicable `RESTRICTED` policy. Passed ACL and lower case label do not waive it. `auto_publish_classification: INTERNAL` cannot bypass required human review or evidence/hash gates. Verify through controlled internal evidence, not an invented public classification field.  
**Source:** S, p. 62, §17.2.1; p. 90.  
**Traceability:** BR-026/031; API-AC-034; DAT-AC-023; BAT-AC-027. Per-class fixtures depend on BR-OQ-012.

#### BR-AC-002 — Case Transition and Closure Guard Coverage

1. For each `SCR-002-T01`–`T06`, prepare source state, current revision, and actor/evidence/approval fixture satisfying its approved guard.
2. Execute API-003 guarded PATCH.
3. Repeat with stale revision, unauthorized actor, and unlisted normal edge.
4. Exercise closure and reopening only after their missing contracts are confirmed.

**Expected:** Six specified edges accept when guards pass, with monotonic revision and one accepted transition evidence. Stale case request returns `CASE_VERSION_CONFLICT`; denied/unsupported changes preserve state. Closure preserves exact approved lineage; no ordinary in-place exit from `CLOSED`.  
**Source:** S, pp. 25–26, 82–84.  
**Blocking:** BR-OQ-002/006. Closing/reopening origin/target must not be guessed.

#### BR-AC-003 — Priority, SLA, and Daily Accounting Separation

1. Use approved impact/urgency catalogs and priority matrix.
2. Calculate deadline with approved workspace calendar/timezone.
3. Produce advisory breach prediction.
4. Run daily usage processing with approved reporting-day and accounting formulas.
5. Change display locale and rerun applicable idempotent processing.

**Expected:** Priority uses explicit impact and urgency; prediction never changes contractual deadline; locale does not alter durable time/order. Daily rollups preserve attribution and replay-safe business effects. Case calendar, review SLA, and accounting day are not silently conflated.  
**Source:** S, pp. 25, 59, 65.  
**Blocking:** BR-OQ-004/005/020 for exact numeric outputs.

#### BR-AC-004 — Publication Atomicity and Current Access

1. Prepare exact approved candidate and satisfied evidence/policy conditions.
2. Revoke evidence access after review, or change candidate hash.
3. Attempt publication.
4. Separately inject transaction failure between gate satisfaction and final-pointer update.

**Expected:** Revoked access or changed hash blocks publication and preserves prior approved pointer. No partial gate/pointer commit. Old approval cannot publish another artifact under replay.  
**Source:** S, pp. 45–46, §§12.2–12.5.

#### BR-AC-005 — Held and Partially Completed Lifecycle Operations

1. Attempt export/delete as single Admin.
2. Start independently authorized lifecycle work.
3. Include held inventory and inject blob/index removal failure.
4. Inspect receipts and reported completion.

**Expected:** Single-Admin bypass denied. Export contains required integrity-protected categories, not secrets/internal prompts. Held records retained and receipted; accepted `202` or incomplete cross-store removal is not verified completion.  
**Source:** S, pp. 78–80, 83, 88–89.  
**Blocking:** BR-OQ-018 for exact held-only/partial lifecycle state and receipt schema.

#### BR-AC-006 — Safety Gate Cannot Be Offset by Quality Scores

1. Run frozen signed evaluation suite.
2. Produce acceptable benchmark scores but introduce an unmitigated critical isolation/approval finding, low statistical confidence, or safety canary regression.
3. Attempt promotion.

**Expected:** Promotion blocked despite benchmark scores. Actual expectations/results remain unchanged and signed release evidence is retained.  
**Source:** S, pp. 74–76, 88–89.  
**Blocking:** BR-OQ-023 for statistical calculation and exact release evidence schema.

## Consistency and Open Questions

### Consistency Findings and Required Amendments

Earlier specifications are not rewritten here. The findings below retain source conflicts and required controlled amendments.

| Finding ID | Conflict or evidence distinction | Affected identifiers/files | Required clarification or amendment |
|---|---|---|---|
| BR-CNS-001 | Six normal case edges are explicit; closing origin and reopening target are absent. S, pp. 25–26. | BR-013/014; `SCR-002-T01–T08`; `SF-CON-003`; API-CNS-001; DAT-CNS-013; BAT-CNS-002 | Preserve six edges and CLOSED finality; complete only missing edges/guards; no automatic classifier/Reject state trigger |
| BR-CNS-002 | `AWAITING_REVIEW`, missing-approval termination, recoverable timeout, and `FAILED` coexist. S, pp. 12, 41, 45, 49, 82, 90. | BR-023/029; SF-CON-004; API-CNS-003; DAT-CNS-014; BAT-CNS-004 | Define wait versus terminal failure and runtime/review SLA; no new timeout state |
| BR-CNS-003 | Both run request routes exist. S, pp. 15–17, 40, 83. | BR-023/024; API-005/032; SF-CON-007; BAT-CNS-003 | Resolve distinct/alias/amendment relationship; do not create duplicate unrelated workflows |
| BR-CNS-004 | Archetype/role/catalog scopes differ. S, pp. 11, 22, 83. | BR-001/002/027/039; SF-CON-008; API-AUTH-005 | Confirm Workspace Admin/Admin, Owner, Member, approver mapping without broad grants |
| BR-CNS-005 | Earlier text emphasizes high-risk self-approval; B.1 specifies `approval_tasks` `no self approval`, and F specifies `false`. S, pp. 11, 85, 90. | BR-027; `SCR-005` guards; API-POL-003; DAT-011-F04; BAT-011 | Earlier guard documentation must retain assigned-task no-self-approval evidence as well as unconditional high-risk prohibition. Define originating actor/scope; no undocumented task exception |
| BR-CNS-006 | Maximum material class affects routing, redaction, retention, approval; lower case label and INTERNAL auto-publish cannot bypass it. S, pp. 62, 90. | BR-026/031; `SCR-002-F10`, `SCR-007-F09–11`; API-CNS-013; DAT-CNS-015; BAT-CNS-010/011 | Required Stage 1 amendment remains: explicitly link all four controls. No extra policy input, automatic case relabeling, or public field |
| BR-CNS-007 | Generic immutable-derivative register labels conflict with mutable current case/job/index projections. S, component registers; pp. 24–25. | BR-009; DAT-CNS-002/003; BAT-CNS-017 | Separate immutable provenance/revision/history from mutable current state; do not freeze supported mutations |
| BR-CNS-008 | Domain case fields exceed abbreviated DDL; `NEW` is business initial state but not SQL default; `updated_at DEFAULT now()` is not update trigger. S, pp. 12, 24, 86. | BR-010/011/012; DAT-003 fields; API-CNS-005; DAT-CNS-017 | Complete schemas without dropping supported fields or inventing default/trigger behavior |
| BR-CNS-009 | `policy_version`, `rule_version`, aggregate revision, and `plan_revision` differ; digest-only policy storage insufficient. S, pp. 24, 40, 44, 48, 85. | BR-007/023/025/026; DAT-CNS-011 | Preserve distinct version concepts; store normalized inputs plus applied rule version; confirm activation |
| BR-CNS-010 | Source confirms fingerprint/pipeline immutable IDs but UUIDv7 and abbreviated version identity coexist. Hash algorithms for artifact/ACL/audit not fully specified. S, pp. 31, 45, 51, 85. | BR-017/028/043; DAT-CNS-008/012 | Define identity/hash canonicalization without assuming every digest is SHA-256 or adding an unconfirmed version column |
| BR-CNS-011 | Revocation-before-next-query coexists with asynchronous cache/index delivery. S, pp. 27–28, 48, 53. | BR-004/020/035/037; BAT-CNS-007 | Define fail-closed propagation barrier/current checks; queue eventual consistency cannot weaken next-query safety |
| BR-CNS-012 | Safe low quality is viewable but excluded from autonomous recommendations; unsafe quarantine has no indexing. S, pp. 30–32. | BR-016/018; BAT-CNS-020 | Do not equate low quality with malware, impose unsupported universal no-index rule, or grant unsafe-content viewing |
| BR-CNS-013 | Routine retention only eligible closed cases; decommission/tombstone and diagnostic categories separately described. S, pp. 26, 51, 66, 78–80. | BR-038/041; DAT-CNS-016; BAT-CNS-012 | Define inventory/hold/retention precedence without applying CLOSED to every log or bypassing holds through decommission |
| BR-CNS-014 | Tenant export/delete terminology differs from workspace routes; independent checks, `Admin + approver`, and two-person export control coexist. S, pp. 78–83, 88. | BR-039–041; SF-CON-010; API-CNS-008; BAT-CNS-013 | Define extent and independent proof/actors. Retain T-11 two-person evidence; no single-person export |
| BR-CNS-015 | Repeated Chapter 22 boundary text references deletion verification for other subjects; C.1 consumer closes purge record. S, pp. 78–80, 87. | BR-033/040/041; BAT-CNS-014 | Do not emit `TenantDeletionVerified` for export/provisioning by boilerplate association |
| BR-CNS-016 | General snake-case error wording versus uppercase source literals. S, pp. 54, 84, 89. | BR-006/007/008/019/022/034; SF-CON-005 | Preserve exact existing literals; undefined codes remain open |
| BR-CNS-017 | Case key TTL, workflow dedup, cache TTL, diagnostics/audit retention, daily/monthly periods are distinct. | BR-008/012/029/038/042/044 | No universal `24`-hour TTL, UTC schedule, shared calendar, or backup schedule inferred |
| BR-CNS-018 | §2.3.1 says identifier “within 300 ms”; §18.2.1 says P95 “under 300 ms.” S, pp. 12, 65. | BR-044; SF-AC-028; API-AC-044; BAT reference targets | Retain stricter earlier `<300 ms` target pending clarification; confirm exact equality boundary |
| BR-CNS-019 | Dashboard “Evidence Coverage” `97.6%`, `128`, `14`, `Healthy`, and “5 verified citations” are illustrated fixtures, not benchmark/citation thresholds. S, p. 7; p. 75. | BR-019/025/032/045; SF-CON-011; API-CNS-016; DAT-CNS-019 | Define aggregate formulas independently; preserve distinct state vocabularies and evaluation metrics |
| BR-CNS-020 | A2A requires input/output schemas but example omits output property; MCP limit is not public search schema. S, pp. 41, 87. | BR-005/019; API-CNS-009/010; DAT-CNS-018 | Keep public/tool contracts separate; complete missing declared output field without guessing its name |
| BR-CNS-021 | GET chapter registers mention mutation context/events, but do not define GET business writes/jobs. | BR-006/009/044/046; API-CNS-011; DAT-LIFE-001; BAT-CNS-018 | No idempotency-required read, release event on probe, or new job/screen inferred |
| BR-CNS-022 | Source gives score targets but not metric formulas/rounding; security critical IDs lack individual definitions. S, pp. 75, 88. | BR-045/046; DAT-OQ-017/019; BAT-OQ-017/021 | Do not invent metric denominator/aggregation, confidence level, or SEC-to-threat mapping |

### Open-Decision Register

Each item also appears beside affected rules. All are **Needs confirmation**. No decision, owner, deadline, or approval is established.

| Question ID | Required decision or missing contract | Affected rules | Earlier dependencies and source |
|---|---|---|---|
| BR-OQ-001 | Authentication/session claims/transport; service scopes; complete role/resource permission matrix; Owner/Member/approver mapping; self/originator definition | BR-001–003/027/039 | [01_screen_functions.md](01_screen_functions.md), OQ-001–003; [02_api.md](02_api.md), API-OQ-001/002/016; [03_data.md](03_data.md), DAT-OQ-004. S, pp. 11, 18, 21–23, 83, 85, 90 |
| BR-OQ-002 | Approved schemas, missing precondition/key failures, If-Match/BIGINT representation, revision allocation, concurrency/isolation, fingerprint/namespace/TTL/error replay, simultaneous-failure error priority | BR-006–010/013 | API-OQ-003/017/022; DAT-OQ-001/003/012; BAT-OQ-003/004/011. S, pp. 25, 48–56, 84–86 |
| BR-OQ-003 | Case required fields/defaults/owner; classification/reason catalogs, confidence/provenance, correction precedence and input revision snapshot | BR-010 | OQ-007/010; API-OQ-003/005; DAT-OQ-005; BAT-OQ-006. S, pp. 12, 24–25, 40 |
| BR-OQ-004 | Impact/urgency catalogs, priority matrix/formula/ties, missing inputs, override authority, recalculation triggers | BR-011 | OQ-009; API-OQ-005; DAT-OQ-005. S, p. 25, §6.3.1 |
| BR-OQ-005 | Contractual SLA start/duration/calendar/timezone/version, holidays/DST/cutoffs, pause/resume/recalculation, breach equality, timestamp/rounding | BR-012 | OQ-009/020; API-OQ-005; DAT-TIME-004; BAT-TIME-002/003. S, pp. 25, 54, 59 |
| BR-OQ-006 | Six-edge detailed actors/triggers/approval linkage; closing origin/request/result; explicit reopening target/operation; repeated-close and lineage schema | BR-013/014/030 | OQ-008; API-OQ-004; DAT-STATE-001/DAT-OQ-005; BAT-CNS-002. S, pp. 24–26, 44–46, 82 |
| BR-OQ-007 | Upload subtype/MIME/count/name/transport/MB/archive/parser limits; OCR/empty source/quality formulas and thresholds; anchors/derivative identity; quarantine viewing and state matrix | BR-015–018 | OQ-015/018; API-OQ-007/008; DAT-OQ-007/008; BAT-OQ-008. S, pp. 30–32, 82, 90 |
| BR-OQ-008 | Retrieval scoring/ties/diversity/token/support formulas; citation/page/bbox schema; index completeness/recall/coverage; cache dependencies/TTL/current access and rebuild races | BR-004/017/019/020 | OQ-017/018; API-OQ-008; DAT-OQ-009/010; BAT-OQ-009/010. S, pp. 28, 31, 34–36, 53, 57, 78 |
| BR-OQ-009 | Approved models/regions/deployments, route/fallback priority/class mapping, prompt/output schemas, provider timeouts, structured-validation retries, context accounting | BR-021/022 | OQ-020/022; API-OQ-009; DAT-OQ-011; BAT-OQ-012. S, pp. 37–39, 90 |
| BR-OQ-010 | Run-route relationship, pinned case context, DAG-depth/call counting, retry/replay budget, stop-state mapping, review wait versus timeout and deadline equality, A2A completion/decline | BR-005/023/029 | OQ-011; API-OQ-006/023; DAT-OQ-011/022; BAT-OQ-012. S, pp. 12, 15–17, 40–42, 45, 49, 82, 87, 90 |
| BR-OQ-011 | Token/admission thresholds and units/operators, reservation release/overrun/concurrency, quota reset, capacity calculation, retry delay | BR-024/042 | OQ-011/020/021; API-OQ-006/009/013/018; DAT-OQ-014/020; BAT-OQ-012/016. S, pp. 38, 65, 69 |
| BR-OQ-012 | Full six-input policy table/thresholds/priorities; material class provenance/encoding/unknown handling; per-class four-control mapping; effective policy/rule version for in-flight work | BR-025/026/031 | OQ-010/020/022; API-POL-001–003/API-OQ-026; DAT-OQ-016; BAT-OQ-024. S, pp. 44–46, 62, 90 |
| BR-OQ-013 | Review eligibility/task states/quorum; complete form/rationale/decision literals; hash algorithm/canonicalization; actual evidence-open prerequisite; expiry SLA/races; gate lookup and atomic revalidation | BR-027–029/031 | OQ-012/013; API-OQ-010; DAT-OQ-013; BAT-OQ-013. S, pp. 45, 57–58, 82–85 |
| BR-OQ-014 | Elevated override roles, secondary reviewer, reason format, permissible override extent, endpoint, rework input and revision linkage | BR-030 | OQ-014/012; API-053/API-OQ-010; DAT-043/DAT-OQ-013; BAT-OQ-013. S, p. 46, §12.3.2 |
| BR-OQ-015 | Connector/provider permissions, capabilities/trust restrictions, credential reauth, cursor/order/outcome stage, poison/retry classification, fairness/concurrency/schedules/limits | BR-034–036 | OQ-016/022; API-OQ-011/017; DAT-OQ-006; BAT-OQ-001/005/007. S, pp. 27–29, 49 |
| BR-OQ-016 | Scoped replay roles/reason/dry-run/limit/schema migration; event dedup expiry; invalidation barriers and concurrent writes; worker fencing/takeover; incident re-enable thresholds | BR-004/008/020/037 | API-OQ-019/022; DAT-OQ-012/020; BAT-OQ-004/010/011/020. S, pp. 48–50, 70, 79, 90 F.1 |
| BR-OQ-017 | Corporate/per-class retention, eligible closed selector, lineage/shared-source/backups, legal-hold timing/release, TTL/year calculations, tombstone and purge schedules/receipts | BR-038/043 | OQ-020/022/023; API-OQ-021; DAT-OQ-014/018; BAT-OQ-014/015. S, pp. 26, 51–53, 62, 66, 80, 90 |
| BR-OQ-018 | Tenant/workspace lifecycle extent, independent actor/check proof/expiry, inventory races, export format/checksum/status/download, held-only/partial deletion, subject matching/redaction, backups and relational purge | BR-039–041 | OQ-023; API-OQ-015/016; DAT-OQ-018; BAT-OQ-019. S, pp. 78–83, 87–89 |
| BR-OQ-019 | Provisioning roles/API/required configuration/order/compensation; bounded historic windows/stable IDs/batch receipts/readiness | BR-020/033 | OQ-016/024; API-OQ-016; DAT-OQ-018/020; BAT-OQ-018. S, p. 78 |
| BR-OQ-020 | Cost/forecast/daily rollup formulas, currency/units/rates/precision/rounding, reporting day/cutoffs, late correction/rerun/zero use, period finalization; any additional financial close behavior | BR-042 | OQ-021; API-OQ-013; DAT-OQ-014; BAT-OQ-016. S, pp. 38, 65, 68, 83, 85 |
| BR-OQ-021 | PII tags/minimization exceptions, audit/redaction/chain archive/batch schema, signatures and receipts, scoped key/secret rotation/isolation/destruction, signed-URL lifetime | BR-043 | OQ-019/022; API-OQ-012/021; DAT-OQ-014–016; BAT-OQ-015/023. S, pp. 10–11, 21, 52, 62–66, 90 |
| BR-OQ-022 | SLO measurement/month/P95 equality, availability/error budgets, alert/ticket/page configuration, degraded modes, recovery inventory/roles/frequency and heartbeat failure | BR-044 | API-OQ-018/021; DAT-OQ-020; BAT-OQ-023/025. S, pp. 12, 18–20, 64–70, 79, 90 |
| BR-OQ-023 | Evaluation metric/statistical formulas/rounding/missing cases/corpus integrity; SEC individual definitions; governance impact/revision/approval; signed release/config and canary thresholds/stage graph/compensation | BR-045/046 | OQ-021/024; API-OQ-013/020/022; DAT-OQ-017/019; BAT-OQ-017/021. S, pp. 8–10, 52, 55, 71–76, 88–90 |
| BR-OQ-024 | Status projection, UI aliases, dashboard formulas, browser routes/focus/error states, SSE/cursor retention/recovery, notification/webhook channels/subscriptions/signature age | BR-032/043 | OQ-004–006/025–027; API-OQ-006/024/025; DAT-OQ-021/022; BAT-OQ-022/025. S, pp. 7, 55, 57–59 |

### Proposals and Reference Values Carried Forward

| Earlier item | Preserved status | Business-rule treatment |
|---|---|---|
| Primary action choices, contextual navigation, screen arrangements | Proposal | Do not derive new permissions, triggers, state transitions, or APIs |
| Proposed case-create JSON fields and bearer-token example | Proposal | Do not establish field requiredness, transport, or omitted-input defaults |
| Proposed SSE event name/payload/offset encoding | Proposal | Only source-confirmed streaming/scoped-resume behavior is normative |
| Illustrated dashboard counts/coverage/service labels and business case references | Confirmed illustration; formulas/schema Needs confirmation | Not defaults, numeric limits, SLA, or canonical domain status |
| BFF cookie architecture | Source-supported optional capability | Not selected mandatory architecture |
| Appendix F configuration values | Confirmed reference configuration | Preserve exact values and scope; not public-field defaults, universal quotas, or permission to bypass mandatory gates |
| Proposed physical schema or job grouping from earlier stages | Proposal or Needs confirmation as originally labeled | Repetition does not approve a table, scheduler, lock, or deployment unit |

No new implementation proposal is selected by this specification.

### Dependencies on Earlier and Later Specifications

| Dependency | Required carry-forward |
|---|---|
| [01_screen_functions.md](01_screen_functions.md) | Preserve screens/fields/actions/transitions and distinction between stored data and editable control. Amend affected review/classification guards through controlled updates, not a rewrite here. |
| [02_api.md](02_api.md) | Preserve operation IDs, methods/paths, cataloged permissions/statuses, exact error literals, record-versus-wire schema distinction, and API-CLS-001. Business rules do not fill missing JSON or endpoint contracts. |
| [03_data.md](03_data.md) | Preserve authoritative/derivative separation, complete domain fields, immutable history/versions/hashes, tenant integrity, normalized policy inputs, and unresolved physical schema/retention mappings. |
| [04_batch_functions.md](04_batch_functions.md) | Preserve logical jobs/triggers/checkpoints, daily/continuous/scheduled distinctions, partial/empty outcomes, replay requirements, and no invented schedule/deployment grouping. |
| Remaining processing specification | **To be defined in a later stage.** Resolve algorithms, count conventions, state triggers, priority/deadline formulas, review/gate linkage, policy tables, and lifecycle selectors without changing confirmed rules. |
| Exception-handling specification | **To be defined in a later stage.** Resolve safe unknown errors, multiple-failure selection, retry/exhaustion, cursor/expiry, partial/held/no-input outcomes, and caller recovery. |
| Remaining architecture/security decisions | **To be defined in a later stage.** Resolve provider/region/identity, service authority, locking/fencing, signed contracts, corporate retention/key isolation, recovery and operational configuration. |
| Stage 8 consolidation | `08_architecture_decision.md` is **To be defined in a later stage**. Consolidate only completed Markdown specifications, linking `05_business_rules.md`, `BR-OQ-001`–`BR-OQ-024`, affected rule IDs, and earlier filenames/IDs. Do not presume an owner, date, approval, or selected outcome. |

**Implementation boundary:** Implement and test the Confirmed business obligations. Missing formulas, thresholds, scopes, actors, schemas, effective periods, state guards, hashes, rounding, schedules, and recovery choices remain explicit blocking decisions. Neither a reference value, illustrated fixture, nor repeated Proposal authorizes silently completing the missing business contract.
