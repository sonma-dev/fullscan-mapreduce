# 5. Business Rules

## Rule Inventory and Scope

### Specification Basis and Status

| Item | Definition |
|---|---|
| Specification file | `05_business_rules.md` |
| Source document | `1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Source baseline | `OD-AI-DDS-001`, release `R1.0`, design revision `1.3` |
| Completed preceding specifications | [`01_screen_functions.md`](01_screen_functions.md), [`02_api.md`](02_api.md), [`03_data.md`](03_data.md), [`04_batch_functions.md`](04_batch_functions.md) |
| Scope | Shared business decisions, authorization conditions, calculations, lifecycle guards, approval requirements, data-handling restrictions, and operational decision gates supported by the source. |
| Identifier convention | `BR-001`–`BR-050` identify consolidated rules. `OQ-BR-xxx` and `CON-BR-xxx` identify unresolved decisions and conflicts. These identifiers are assigned here because the source does not assign individual business-rule IDs. |
| Identifier preservation | Existing `SCR`, `API`, `DAT`, `BAT`, event, `T-01`–`T-12`, and `TST-001`–`TST-016` identifiers remain unchanged. `SEC-001`–`SEC-012` remain source-described release-blocking identifiers without invented individual definitions. |
| Citation convention | `[DDS]` identifies the source filename above. Citations use original PDF page numbers and source sections. |

[DDS]: 1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf

The following statuses apply throughout:

- **Confirmed:** The source establishes the requirement, condition, outcome, vocabulary, or constraint.
- **Needs confirmation:** An implementation decision, calculation, threshold, field contract, permission, effective-period rule, or exception is missing or conflicting.
- **Proposal:** An explicitly labeled, unapproved design suggestion. Repetition in preceding specifications does not establish approval.
- **NC:** Table abbreviation for **Needs confirmation**.

A rule can contain confirmed constraints and unresolved parameters. An unresolved parameter does not authorize an implementation AI to select a value, invent a fallback, or remove the confirmed constraint.

### Interpretation and Applicability

1. These rules consolidate shared behavior; they do not replace the screen, API, data, or batch contracts.
2. Logical inputs and predicates below are not declarations of new JSON properties, database columns, endpoints, or executable jobs.
3. Apply every relevant guard. Satisfying a role check does not satisfy document ACL, revision, evidence, quota, or approval requirements.
4. Source-supported restrictions remain effective during retries, replay, degradation, migration, and recovery.
5. Appendix F configuration is reference evidence, not automatic production approval. Independently confirmed limits retain their confirmed status.
6. Source numbers are normative design assumptions for the fictional baseline, not measured production results.
7. Where the source supplies no conflict-resolution priority, calculation formula, rounding rule, or period boundary, the affected decision remains NC.

**Sources:** [DDS], pp. 1–2; p. 7; p. 9, §1.2.2; p. 82, Appendix A introduction; p. 90, Appendix F and §F.2.

### Rule Inventory

All inventory rows represent **Confirmed constraints**. Unresolved permissions, parameters, and effective-period details are identified beside the detailed rules.

#### Shared Authority, Validation, and Consistency Rules

| Rule ID | Name and purpose | Applicable targets | Actors and permissions | Enforcement timing | Evidence |
|---|---|---|---|---|---|
| BR-001 | System boundaries and prohibited capabilities — prevent unsupported execution. | All screens, APIs, tools, and background functions. | No actor or agent receives excluded capabilities through this baseline. | Capability configuration, admission, and dispatch. | [DDS], p. 9, §1.2.1; p. 10, §1.3.2; p. 19, §4.2.1. |
| BR-002 | Authenticated principal and scoped service identity — establish trusted identity. | Interactive requests, internal calls, background jobs. | Authenticated principal or independently authorized workload identity. | Before resource access or work allocation. | [DDS], pp. 18–23, §§4.1.2 and 5.1–5.3. |
| BR-003 | Resource-level authorization — combine role and resource attributes. | Cases, evidence, review, membership, settings, and operational actions. | Role, tenancy, membership, sensitivity, ACL, action, and separation-of-duty predicates. | Edge checks, domain boundary, mutation transaction, retrieval, and publication. | [DDS], pp. 21–23, Chapter 5; p. 83, §A.2. |
| BR-004 | Tenant-safe identity and references — prevent cross-tenant access and existence disclosure. | Relational rows, objects, indexes, caches, resource references, jobs. | Trusted tenant scope; no client-selected scope override. | Every storage predicate and reference validation; connection reuse. | [DDS], pp. 22–23; pp. 51–53; p. 86, §B.2. |
| BR-005 | Untrusted content cannot confer authority — separate evidence from instructions. | Retrieved text, model results, plans, tools, policy, approvals. | Model and source content have no authorization authority. | Prompt construction, planning, tool dispatch, and policy evaluation. | [DDS], p. 7; pp. 37–42; p. 61, §17.1.2. |
| BR-006 | Authoritative validation and fail-closed outcomes — prevent invalid or ambiguous success. | Public/internal requests, mutations, long-running work, tool arguments. | Authorized caller still must submit valid input. | Before allocation/transaction; at domain invariants; before dispatch. | [DDS], p. 13, §2.3.2; p. 56, §15.3.2; p. 84, §A.3. |
| BR-007 | Revision-safe updates — prevent stale writes. | Case updates and versioned workspace configuration. | Authorized case updater or configuration administrator. | At accepted mutation boundary and within transaction. | [DDS], pp. 24–25, §§6.1.1 and 6.2.2; pp. 83–84. |
| BR-008 | Request idempotency — preserve one outcome under submission retries. | Case creation, long-running POST mutations, cross-service writes. | Authenticated actor with applicable action permission. | Submission, concurrent duplicate handling, retry, and response reconstruction. | [DDS], pp. 15–17; p. 25, §6.2.2; p. 54, §15.1.2; p. 89. |
| BR-009 | Durable events and replay-safe transitions — preserve committed business authority. | Case/approval writes, outbox, consumers, workflow checkpoints. | Scoped producers and consumers; discovery is not permission. | Commit, dispatch, duplicate/delayed delivery, and replay. | [DDS], pp. 17, 48–52; pp. 85, 87; p. 89, `TST-007`. |
| BR-010 | Versioned configuration and effective policy — make decisions reproducible. | Workspace policy, routing, tools, prompts, quotas, retention. | Workspace Admin activity confirmed; exact field/action rights NC. | Configuration update and subsequent evaluation/invocation. | [DDS], p. 24, §6.1.1; p. 44, §12.1.1; pp. 71–73; p. 90. |

#### Case, Evidence, and AI Rules

| Rule ID | Name and purpose | Applicable targets | Actors and permissions | Enforcement timing | Evidence |
|---|---|---|---|---|---|
| BR-011 | Case creation, classification, and correction — preserve intake and classification provenance. | Case creation and asynchronous classification/correction. | Analyst creates; correction role NC. | Creation, classification completion, label correction. | [DDS], p. 12, §2.2.1; p. 40, §11.1.1; pp. 83, 87. |
| BR-012 | Priority derivation — use explicit business impact and urgency. | Case intake/update and priority result. | Authorized business-input updater; model output alone cannot determine priority. | Initial derivation and applicable recalculation. | [DDS], p. 25, §6.3.1. |
| BR-013 | Contractual SLA and time semantics — preserve business-calendar deadlines. | Case deadline calculations and timestamp presentation. | Authorized calendar/configuration actor; locale cannot change durable values. | Deadline calculation, display, and advisory breach prediction. | [DDS], p. 25, §6.3.1; pp. 48, 54, 59. |
| BR-014 | Guarded case transitions — enforce the confirmed case lifecycle. | `cases.status` and case mutations. | Applicable role, revision, and approval guards. | Every case transition. | [DDS], p. 25, §6.2.1; pp. 82, 86. |
| BR-015 | Closure and reopening lineage — preserve approved historical outputs. | Closure snapshots, closed cases, explicit reopen. | Closure/reopen roles NC; resource authorization required. | Closure and explicit new-revision reopening. | [DDS], pp. 24–26, Chapter 6. |
| BR-016 | File admission and unsafe quarantine — prevent unsafe parsing/indexing. | Attachments, connector documents, extraction. | Analyst upload or scoped connector ingestion. | Input validation, scan, parse admission. | [DDS], p. 30, §§8.1.1–8.1.2; pp. 88–89. |
| BR-017 | Immutable normalization and source anchors — preserve source claims and provenance. | Document versions, chunks, OCR derivatives, citations. | Scoped ingestion; generation cites only permitted resolvable anchors. | Extraction, normalization, reprocessing, citation selection. | [DDS], p. 31, §§8.2–8.3.1; p. 51, §14.1.2. |
| BR-018 | Extraction-quality eligibility — distinguish viewable low-quality evidence from autonomous-use evidence. | Quality flags and recommendation evidence. | Authorized source viewers; autonomous use restricted by quality. | Extraction quality evaluation and evidence selection. | [DDS], p. 32, §8.3.2. |
| BR-019 | Grounded retrieval and verified citations — return supported evidence rather than fabricated context. | Search, evidence sets, generated citations, review source access. | Authorized `Member` predicate and source ACL; exact role mapping NC. | Retrieval, evidence selection, citation display, review. | [DDS], pp. 34–36; pp. 57–58; p. 87, §C.2. |
| BR-020 | Search derivative authority and rebuild gate — prevent incomplete replacement indexes. | Index rows, generations, aliases, reconciliation. | Scoped Indexer/reconciliation identity. | Index commit, rebuild, alias switch, failed-write recovery. | [DDS], pp. 16, 34, 49; p. 78, §22.1.2. |
| BR-021 | ACL revocation, cache invalidation, and soft deletion — prevent stale unauthorized visibility. | Source ACLs, retrieval caches, tombstones, indexes. | Authorized source/identity changes and scoped consumers. | Before next retrieval; before new results; at publication. | [DDS], pp. 27–29; pp. 51–53; p. 46, §12.5. |
| BR-022 | Maximum information class and approved model routing — preserve data-handling restrictions. | Run material, model registry, deployment selection/fallback. | Gateway selects only workspace-approved deployments. | Context assembly, route selection, fallback. | [DDS], p. 37, §§10.1.1–10.1.2; p. 62, §17.2.1. |
| BR-023 | Controlled prompt and structured output — reject invalid model results. | Prompt templates, evidence context, model JSON, injection indicators. | Scoped Model Gateway; model output remains data. | Before provider call and after response parsing. | [DDS], pp. 38–39, §§10.2–10.3.2. |
| BR-024 | Queue-aware run admission — protect quota/capacity without losing saved cases. | New AI-run requests and admission state. | Analyst requests; admission service applies thresholds. | Before new run allocation. | [DDS], p. 69, §19.2.1; p. 79, §22.2.1. |
| BR-025 | Token reservation and quota exhaustion — bound current-run spend. | Run budgets, workspace quotas, provider usage, token ledger. | Scoped gateway/accounting processes. | Before invocation and during usage reconciliation/exhaustion. | [DDS], p. 38, §10.3.1; pp. 65, 85. |
| BR-026 | Bounded plans, checkpoints, and stop conditions — prevent uncontrolled execution. | Run DAG, steps, runtime budget, durable stages. | Orchestrator and approved agents; Policy Evaluator is deterministic. | Plan acceptance, before effects/dispatch, stop-condition evaluation. | [DDS], pp. 40–42; p. 49, §13.2.1; pp. 82, 90. |
| BR-027 | Independent tool/A2A authorization — prevent discovery-based or equivalent-tool bypass. | MCP/A2A discovery, arguments, mutable tools, handoffs. | Invoking principal, workspace policy, tool scope, classification, required human authorization. | Discovery evaluation, argument validation, before dispatch. | [DDS], pp. 41–42; p. 87, §C.2; p. 89, `TST-014`. |
| BR-028 | Deterministic policy inputs and outcomes — separate risk suggestions from binding decisions. | Policy evaluations, reasons, rule versions, review routing. | Deterministic Policy Service/Evaluator; LLM cannot override. | Policy evaluation and publication validation. | [DDS], p. 44, §§12.1.1–12.1.2; p. 85. |

#### Review, Lifecycle, and Operational Rules

| Rule ID | Name and purpose | Applicable targets | Actors and permissions | Enforcement timing | Evidence |
|---|---|---|---|---|---|
| BR-029 | Reviewer eligibility and separation of duties — require appropriate independent review. | Reviewer pools, assignments, high-risk recommendations. | Policy-selected Reviewer; high-risk author cannot self-approve. | Assignment and decision submission. | [DDS], p. 11, §2.1.2; p. 45, §12.2.1; pp. 85, 90. |
| BR-030 | Exact review context and immutable decision capture — bind decision to reviewed content. | Review evidence panel, task, artifact hash, decision record. | Authorized Reviewer; required fields complete. | Task opening, submission, transaction validation. | [DDS], p. 45, §12.2.2; pp. 57–58; pp. 83, 85, 89. |
| BR-031 | Review expiry and escalation — never interpret expiry as approval. | Task SLA, expiry, reassignment, escalation. | Scoped policy processing and eligible replacement reviewers. | Configured task expiry and concurrent decision handling. | [DDS], p. 45, §12.2.1; pp. 82, 89. |
| BR-032 | Atomic publication gate — publish only an exact, authorized, supported artifact. | Candidate, decisions, evidence, final response pointer. | Scoped publication consumer; public Publish action not confirmed. | Immediately before and within publication transaction; replay. | [DDS], pp. 11–13; pp. 45–46; p. 52; p. 87. |
| BR-033 | Override and rework constraints — preserve denial history and independent controls. | Appeals, overrides, rejected/denied candidates, new run revisions. | Elevated role, secondary reviewer, audited reason for override. | Override evaluation and rework creation. | [DDS], p. 46, §12.3.2; p. 75, §21.3.1. |
| BR-034 | Connector trust and credential lifecycle — expose unsupported capabilities safely. | Connector capability metadata, credentials, queued sync. | Admin initiates sync; authorized operator revocation; exact aliases NC. | Discovery, sync admission, credential use/revocation. | [DDS], p. 27, §§7.1.1–7.1.2; p. 83. |
| BR-035 | Durable incremental synchronization — protect cursor advancement and partial outcomes. | Sync runs, provider cursor, watermark, error/quarantine ledger. | Scoped connector workers. | Every item outcome, cursor commit, partial retry. | [DDS], pp. 28–29, §§7.2–7.3.2; p. 85. |
| BR-036 | Fair throttling, bounded retry, and controlled replay — recover without amplifying failure. | Connectors, dependencies, read/mutable tools, dead letters. | Scoped workers; authorized replay operator. | Throttling, retry classification, replay admission/execution. | [DDS], pp. 28–29, 42, 49–50; pp. 89–90. |
| BR-037 | Immutable audit and privacy-safe disclosure — preserve evidence without leaking content/secrets. | Audit, diagnostics, public responses/errors, providers, secret references. | Auditor redacted scope; operators cannot edit history. | Recording, querying, export, provider invocation, rotation. | [DDS], pp. 11, 21, 27, 52, 54, 61–66, 84–85. |
| BR-038 | Retention eligibility and legal holds — prevent ineligible or protected purge. | Closed cases, diagnostic/audit records, purge inventory. | Authorized retention processing; hold administration rights NC. | Eligibility selection and destructive processing. | [DDS], p. 26, §6.3.2; p. 66, §18.3.2; pp. 80, 89–90. |
| BR-039 | Independent export/deletion approvals — prevent single-admin exit bypass. | Workspace export/delete requests and execution. | `Admin + approver`; two independent approval checks. | Before controlled operation proceeds. | [DDS], p. 78, Chapter 22 invariant; pp. 83, 88. |
| BR-040 | Authorized export content — preserve permitted exit data and exclusions. | Export manifest/package. | Authorized independently approved exporter/recipient scope. | Inventory selection, packaging, release of export. | [DDS], p. 79, §22.3.1. |
| BR-041 | Verified deletion and shared request inventory — require tombstones, removal, receipts, and hold exceptions. | Deletion inventory, blobs, indexes, receipts, data-subject requests. | Independently approved deletion and scoped Retention Worker. | Deletion processing and verification. | [DDS], pp. 51, 80, 85, 87, 89. |
| BR-042 | Idempotent provisioning and reconciled onboarding — block sync until ready. | Workspace setup, historical backfill, readiness. | Authorized provisioning/backfill actor; exact role NC. | Provisioning, sync admission, bounded historic ingestion. | [DDS], p. 78, §§22.1.1–22.1.2. |
| BR-043 | Usage attribution and period-end reporting — preserve daily cost/usage accountability. | Token/cost ledgers, usage categories, daily rollups. | Scoped accounting; Admin usage-read scope. | Usage recording and daily aggregation. | [DDS], pp. 65, 68, 83, 85. |
| BR-044 | Safe degradation and incident recovery — retain safe workflows without bypass. | Generation admission, lexical fallback, aliases, incident replay. | Authorized incident/operator actions; existing resource permissions remain. | Outage, suspected ACL leak, delayed indexing recovery. | [DDS], pp. 68–70; p. 79, §22.2; p. 90, §F.1. |
| BR-045 | Truthful accessible state and progress — distinguish accepted work, draft, review, and publication. | Screen labels, run SSE, refresh, evidence navigation, review controls. | Authorized interactive users; navigation is not permission. | Display, live update, refresh, decision enablement. | [DDS], p. 13; pp. 55, 57–59; p. 89, `TST-011`. |
| BR-046 | Service objectives and actionable alerts — distinguish user-impacting incidents from spend anomalies. | SLO metrics, alert policies, capacity/scaling evidence. | Monitoring processes; actual alert/ticket assignments NC. | Measurement, alert evaluation, scaling. | [DDS], p. 19, §4.2.1; pp. 64–65; p. 79. |
| BR-047 | Primary-region writes and controlled recovery — preserve recovery safety and consistency. | Persistence, backups, warm recovery, DR exercises. | Restore only under incident command. | Normal writes, backup, failover/restore, verification. | [DDS], p. 19, §4.2.2; pp. 69–70; p. 89. |
| BR-048 | Compatible release and migration gates — prevent unsafe promotion or automatic data reversal. | Images, configuration, schemas, migrations, rollout records. | Allowed build identity; Security/SRE validation. | Build, predeploy, canary, enforcement, promotion, rollback. | [DDS], pp. 20, 52, 55, 71–73, 89. |
| BR-049 | Frozen evaluation and safety-first release acceptance — prevent benchmark substitution for correctness. | Datasets, scorecards, confidence evidence, security exit criteria. | Admin starts evaluation; independent fixture/security evidence review. | Evaluation, model/prompt change, release decision. | [DDS], pp. 74–76; pp. 88–89. |
| BR-050 | Controlled baseline changes and traceability — preserve approved design authority. | Change requests, design revisions, invariant/test links, architecture decisions. | Authorized governance actor; approval mechanics NC. | Proposed/approved change and implementation lock. | [DDS], pp. 8–10; p. 90, §F.2. |

## Decisions, Calculations, and State Transitions

### Shared Preconditions, Authority, and Conflict Handling

<a id="br-001"></a>
#### BR-001 — System Boundaries and Prohibited Capabilities

**Confirmed:**

- Process enterprise knowledge and user-submitted cases.
- Do not perform physical automation or irreversible financial transactions.
- Do not fine-tune foundation models, browse without restriction, or grant agents administrative cloud permissions.
- Application-hosted GPU inference is **Out of scope for the R1 execution profile** because model providers are external dependencies.
- Cross-region active/active mutation, OCR beyond English, and customer-managed model weights are **Deferred from this baseline**.

Financial-impact categorization, usage reporting, and case subjects involving invoices do not authorize financial transaction execution.

**Sources:** [DDS], p. 9, §1.2.1; p. 10, §1.3.2; p. 19, §4.2.1; p. 44, §12.1.1.

**Needs confirmation — OQ-BR-016:** Define the permitted consequential business-tool actions. The source describes their authorization constraints but provides no complete mutable-tool inventory.

<a id="br-002"></a>
#### BR-002 — Authenticated Principal and Scoped Service Identity

**Prerequisites and inputs:** Interactive identity, API token claims, internal workload identity, tenant context, service audience, and declared action scope.

**Confirmed:**

1. Interactive sessions use OIDC authorization-code flow with PKCE.
2. API access tokens carry issuer, audience, expiry, subject, and tenant.
3. Reject unexpected token algorithms and missing tenancy claims.
4. Every request is bound to an authenticated principal and tenant.
5. Internal service calls use mTLS-authenticated HTTP or generated gRPC as applicable, with TLS, audience checks, and scoped IAM.
6. Use managed workload identity where supported; do not share a service identity between deployment units.
7. Background jobs carry immutable tenant identity in signed envelopes.
8. The browser does not store long-lived refresh tokens in local storage.

The optional backend-for-frontend using secure, `HttpOnly`, `SameSite` cookies is not a selected session implementation.

**Sources:** [DDS], pp. 16, 18, 21–22, §§3.3.1, 4.1.2, 5.1 and 5.3.1.

**Needs confirmation — OQ-BR-001:** Token claim names, issuers/audiences, accepted algorithms, expiry equality/clock tolerance, session transport, service grants, signature protocol, and role mappings remain unresolved.

<a id="br-003"></a>
#### BR-003 — Resource-Level Authorization

Access must satisfy all **applicable** role and resource constraints. A successful check in one dimension does not waive another.

| Condition | Confirmed result |
|---|---|
| Applicable role, tenant, workspace membership, sensitivity, document ACL, action, and separation-of-duty requirements are satisfied | The authorization guard is satisfied; other business guards still apply. |
| Broad policy violation at the edge | Reject the operation. |
| Resource attributes fail within a mutation transaction | Reject without accepted business-state change. |
| Document ACL does not permit the requested access | Do not release that chunk to the model or unauthorized caller. |
| User can see a navigation item or discover a capability | No permission is established by visibility/discovery. |
| Actor is Admin or Auditor but the resource-read predicate is unresolved | Do not infer general case/evidence access. |

**Confirmed actor/action scopes from §A.2:**

| Activity | Source scope |
|---|---|
| Create case, upload attachment, start case run | `Analyst` |
| Read current case or run; receive run SSE | `Analyst / Reviewer` |
| Update case | `Owner`; role-versus-relationship mapping NC |
| Submit review decision | `Reviewer`, with task and policy guards |
| Start connector sync, read usage, start evaluation | `Admin` |
| Search | `Member`; membership/role mapping NC |
| Read audit events | `Auditor` |
| Export/delete workspace | `Admin + approver`, plus BR-039 |

**Sources:** [DDS], pp. 11, 21–23; p. 83, §A.2.

**Needs confirmation — OQ-BR-001:** Complete the action matrix, `Workspace Admin`/`Admin`, `Owner`, `Member`, operator/elevated-role aliases, Auditor redacted evidence path, and field-level permissions. No role hierarchy is supplied.

<a id="br-004"></a>
#### BR-004 — Tenant-Safe Identity and References

**Confirmed:**

- Application identifiers use UUIDv7 as the baseline identity convention.
- Every tenant-owned row has `tenant_id`; every storage access predicate includes tenant identity.
- Use tenant-scoped database context with RLS.
- Validate case tenancy against its referenced workspace; production enforcement uses foreign keys or controlled write procedures.
- Reset scoped database session variables after **every transaction** before pooled connection reuse.
- Attachments reference immutable document versions; approvals reference exact run artifact hashes.
- A foreign-tenant ID and an absent ID return the same not-found response class. `TST-003` identifies a `404`-equivalent non-disclosing result.
- Denial audit evidence retains principal and denied resource class without private-resource existence disclosure.

Preserve explicit reference constraints: `tenants` has `unique(slug)`; `cases.id` is a `UUID PRIMARY KEY`; cases also have `UNIQUE (tenant_id, id)` and non-null tenant/workspace references. The generic tenant/business-key uniqueness statement does not silently remove these explicit constraints.

**Sources:** [DDS], pp. 22–23; pp. 51–53; pp. 85–86, Appendix B.

**Needs confirmation — OQ-BR-002:** Complete identifier validation, business-number mapping, slug normalization/scope, foreign keys, cross-resource cardinalities, and non-disclosing error details.  
**Needs confirmation — OQ-BR-003:** Complete RLS write/privileged-role controls, missing tenant-context handling, and the chosen reference-enforcement mechanism.

<a id="br-005"></a>
#### BR-005 — Untrusted Content Cannot Confer Authority

**Confirmed:** Retrieved documents and LLM responses cannot:

- Authorize tools or external writes.
- Change tenant scope.
- Alter approvals.
- Override the versioned deterministic policy engine.
- Introduce new system instructions or unrestricted network destinations.

The browser does not submit arbitrary tool definitions. The planner receives only allowlisted tool names. The orchestrator has no direct database credentials and uses narrow scoped APIs.

These restrictions apply even when source text is relevant, highly ranked, confidently classified, or returned by an approved model.

**Sources:** [DDS], p. 7; p. 9, §1.3.1; pp. 38–42; p. 61, §17.1.2.

**Needs confirmation — OQ-BR-016:** Specify the actual allowlisted tools and capability grants; do not infer them from agent discovery metadata.

<a id="br-006"></a>
#### BR-006 — Authoritative Validation and Fail-Closed Outcomes

**Confirmed procedure:**

1. Validate request/envelope input before long-running allocation or transaction entry.
2. Revalidate at domain invariants.
3. Validate tool arguments before dispatch.
4. Treat client-side validation as convenience only.
5. Reject stale, unauthorized, oversized, unsafe, ungrounded, or invalid actions under their applicable rules.
6. Return a documented retryable dependency error or a persisted asynchronous operation identifier when a dependency is unavailable; never return ambiguous success.
7. Never represent partial processing as an approved answer.

| Failure category | Confirmed contract |
|---|---|
| Public schema-invalid request | HTTP `422`; exact code/detail schema NC |
| Revision conflict | HTTP `409`; case code `CASE_VERSION_CONFLICT` |
| Quota/admission throttling | HTTP `429`; run admission also includes `Retry-After` |
| Unsafe upload | Fail closed; unsafe attachment quarantined without indexing |
| Invalid model output | `MODEL_OUTPUT_INVALID`; no publication |
| Unsupported evidence | `NO_SUPPORTED_EVIDENCE`, or the source-supported review/clarification path |
| Stale reviewed artifact | Rejected as stale and audited; decision API exposes `409` conflict |
| Unauthorized/foreign resource | Permanent denial or non-disclosing not-found class, as applicable |

**Sources:** [DDS], p. 13, §2.3.2; pp. 30, 36, 38, 45, 54, 56, 69, 83–84, 89.

**Needs confirmation — OQ-BR-002:** Complete per-operation errors, casing, mandatory fields, missing-header outcomes, and asynchronous failure projections. No additional error literal is created here.

<a id="br-007"></a>
#### BR-007 — Revision-Safe Updates

| Input condition | Result |
|---|---|
| Authorized case update with matching current revision and valid domain change | Accept the mutation; maintain monotonic revision. |
| Submitted `If-Match` does not match current case revision | HTTP `409`, `CASE_VERSION_CONFLICT`, current revision; no stale mutation. |
| Workspace configuration update with satisfied revision precondition and valid authorized change | Accept updated configuration and produce durable audit evidence. |
| Stale or unauthorized workspace configuration update | Reject without accepted policy change. |
| Required precondition absent or malformed | **Needs confirmation** for exact response; absence is not permission to bypass the precondition. |

The reference case revision is `BIGINT NOT NULL DEFAULT 1`. The source does not define ETag encoding, wildcard behavior, exact increments, merge logic, or a universal revision type for other resources.

**Sources:** [DDS], pp. 24–25; pp. 83–86.

**Needs confirmation — OQ-BR-003:** Define revision transport, conflict recovery, transaction isolation/locking, configuration revisions, and concurrency with classification, review expiry, or legal holds.

<a id="br-008"></a>
#### BR-008 — Request Idempotency

**Inputs:** Authenticated actor, operation key, request fingerprint, target operation, and previously recorded outcome.

| Condition | Confirmed result |
|---|---|
| Valid new case request/key | One accepted case outcome. |
| Identical actor/request fingerprint replay within the case-domain contract | Original outcome and identical response; no second case. |
| Same key with different fingerprint | `IDEMPOTENCY_CONFLICT`; `TST-002` confirms HTTP `409`. |
| POST mutation creates long-running work | Require `Idempotency-Key`; repeated identical payload returns the original operation. |
| Cross-service write is retried | Idempotent accepted business outcome. |
| Mutable tool is invoked | Idempotency required in addition to separate authorization. |

The case-domain actor/fingerprint mapping lasts **24 hours**. This does not establish the lifetime of every batch ledger, webhook ledger, SSE history, or other API key.

**Sources:** [DDS], pp. 15–17; p. 25, §6.2.2; p. 42, §11.3.2; p. 54, §15.1.2; p. 89, `TST-001/TST-002`.

**Needs confirmation — OQ-BR-003:** Key namespace/length, fingerprint canonicalization, simultaneous pending duplicates, rejected-outcome caching, permission-changed replay, expiry equality, reuse after expiry, and non-case lifetimes.

<a id="br-009"></a>
#### BR-009 — Durable Events and Replay-Safe Transitions

**Confirmed:**

- State-changing workflows use transactional outbox publication or an explicitly reconciled saga step.
- Case mutations and approval decisions commit with their associated outbox inserts in one ACID transaction.
- Events contain exact properties `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, and `payload`.
- Producers use UTC and canonical JSON.
- Consumers deduplicate event IDs and operation keys and detect stale aggregate revisions.
- No business invariant depends on ordering across queue partitions.
- An already accepted duplicate records a duplicate outcome and returns without reapplying the mutation.
- Retain one audit record for an accepted state transition; duplicate-processing evidence must not create another accepted business transition.
- A failed index write does not undo accepted source metadata; reconciliation compares fingerprints and retries.
- Repair broken message links from the outbox ledger.

**Sources:** [DDS], pp. 10, 13, 17; pp. 48–52; pp. 87–89.

**Needs confirmation — OQ-BR-022:** Event signatures, payloads/triggers, actor/correlation carriers, stale-event handling, broker/ledger retention, acknowledgment atomics, and replay migration contracts. The source does not authorize every GET to allocate work or emit a business event.

<a id="br-010"></a>
#### BR-010 — Versioned Configuration and Effective Policy

**Confirmed configuration concepts:** Retention class, allowed deployments, connector credential references, approved toolsets, reviewer routing, quotas, versioned policy inputs, prompts, and deployment configuration.

1. Configuration updates require revision preconditions and durable audit.
2. Store normalized policy inputs with the actual evaluated rule-set version.
3. Pin tool schemas by version and preserve actual prompt/model version evidence.
4. Nonsecret defaults reside in source control; environment values are signed deployment configuration; credentials and keys remain vault-backed references.
5. Configurable numeric thresholds are versioned policy.

**Sources:** [DDS], p. 9, §1.2.2; p. 24, §6.1.1; pp. 41, 44, 58, 71–73.

**Needs confirmation — OQ-BR-004:** Configuration precedence, activation time, effective-period representation, rollback, overlapping versions, and applicability to in-flight runs, assigned tasks, cached evidence, existing deadlines, and queued jobs. There is no confirmed rule that all work uses either “latest policy” or “policy at creation.”

### Case Decisions and Calculations

<a id="br-011"></a>
#### BR-011 — Case Creation, Classification, and Correction

**Confirmed:**

1. An authorized Analyst creates a case using the idempotent creation contract.
2. Creation starts the case in `NEW`; accepted creation returns HTTP `201` and a case identifier.
3. The reference stored revision defaults to `1` and sensitivity to `INTERNAL`. These defaults do not establish complete POST requiredness or form defaults.
4. Intake receives business context and attachments; the source does not require attachments for every creation.
5. `CaseCreated` initiates asynchronous classification.
6. Classification attaches labels, confidences, and provenance.
7. A user correction of labels requires a reason code.
8. Classification does not itself authorize publication or tool execution.

**Sources:** [DDS], p. 12, §2.2.1; p. 40, §11.1.1; pp. 83, 86–87.

**Needs confirmation — OQ-BR-005:** Required intake fields, classification/correction vocabularies, confidence scale, correction permission/API, attachment readiness, failure states, and stale classification versus later correction races.

<a id="br-012"></a>
#### BR-012 — Priority Derivation

| Category | Requirement |
|---|---|
| Prerequisites | Valid explicit impact and urgency inputs under a resolved business vocabulary. |
| Inputs | Impact and urgency; any additional permitted input is NC. |
| Confirmed calculation constraint | Derive priority from explicit impact and urgency, never model output alone. |
| Result | Case priority. Exact labels, range, ordering, and storage/wire representation NC. |
| Formula | **Needs confirmation.** No impact × urgency matrix, weighted sum, multiplication, or lookup table is supplied. |
| Units and rounding | **Needs confirmation.** Input units, numeric precision, rounding, and ties are not defined. |
| Missing/invalid inputs | Must undergo authoritative validation; requiredness, missing-value outcome, and error mapping NC. |
| Recalculation | Trigger on intake/update, manual adjustment rights, historical retention, and effective-period behavior NC. |

**Source:** [DDS], p. 25, §6.3.1.

**Needs confirmation — OQ-BR-006:** Supply the priority formula/matrix, input vocabulary, boundaries, ties, manual override rules, and recalculation/effective-period behavior. The illustrated title `Risk Prioritization` does not establish queue ordering.

<a id="br-013"></a>
#### BR-013 — Contractual SLA and Time Semantics

**Confirmed:**

- Business calendars compute deadlines in workspace timezone.
- Breach prediction is advisory and cannot change contractual deadlines.
- Durable server times are UTC; public timestamps use RFC 3339.
- The UI presents workspace-local times with timezone labels.
- Locale selection changes presentation, not event ordering or durable API values.

| Calculation element | Contract |
|---|---|
| Deadline inputs | Workspace timezone and business calendar confirmed; priority-to-duration, start event/time, pauses, and contractual duration NC. |
| Formula | **Needs confirmation.** No elapsed-time or business-minute addition formula is supplied. |
| Units | SLA duration units and calendar resolution NC; do not assume hours, business days, or seconds. |
| Calendar boundaries | Working periods, weekends, holidays, DST gaps/overlaps, and nonworking start times NC. |
| Breach boundary | Exact `now == deadline` treatment and overdue-state outcome NC. |
| Changed calendar/priority | Recalculation and treatment of an existing contractual deadline NC. |
| Rounding | Fractional-time precision and rounding to a business boundary NC. |

**Sources:** [DDS], p. 25, §6.3.1; pp. 48, 54, 59.

**Needs confirmation — OQ-BR-007:** Complete calendar, duration, start/pause/resume, timezone, DST, equality, and deadline-change rules. Review-task expiry is separately configured under BR-031 and is not confirmed to use this case business calendar.

<a id="br-014"></a>
#### BR-014 — Guarded Case Transitions

All transitions require applicable role, revision, authorization, and approval guards.

| Current state | Confirmed next state | Conditions and exception |
|---|---|---|
| Creation | `NEW` | Valid authorized idempotent creation. |
| `NEW` | `TRIAGED` | Detailed classification/triage completion guard NC. |
| `TRIAGED` | `IN_PROGRESS` | Detailed assignment/work-start guard NC. |
| `IN_PROGRESS` | `PENDING_APPROVAL` | Applicable approval routing; exact trigger NC. |
| `IN_PROGRESS` | `RESOLVED` | Applicable evidence/approval requirements; detailed resolution guard NC. |
| `PENDING_APPROVAL` | `RESOLVED` | Required decision/policy conditions satisfied; publication relationship NC. |
| `PENDING_APPROVAL` | `IN_PROGRESS` | Rework path supported; detailed rejection/return trigger NC. |
| `RESOLVED` | Close operation exists | Explicit `RESOLVED -> CLOSED` transition is not enumerated in §6.2.1. |
| `CLOSED` | Explicit reopen as a new revision | No ordinary transition that overwrites closed lineage. |

The stored case vocabulary is exactly:

`NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED`.

Do not add run, review, artifact, or illustrated summary labels to `cases.status`.

**Sources:** [DDS], p. 25, §6.2.1; p. 82, §A.1; p. 86, §B.2.

**Needs confirmation — OQ-BR-008:** Complete transition triggers/roles, closure predecessor states, closure/reopen contracts, direct-status editability, and case-to-run/publication state synchronization.

<a id="br-015"></a>
#### BR-015 — Closure and Reopening Lineage

**Confirmed closure result:** Snapshot the approved answer, immutable cited document versions, and reviewer decisions. Closed cases preserve immutable approved-output lineage.

**Confirmed reopening exception:** A closed case is final unless explicitly reopened as a new revision. Preserve the earlier closed snapshot; reopening does not replace its cited version or historical decision with a newer value.

**Sources:** [DDS], pp. 24–26, §§6.1–6.3.

**Needs confirmation — OQ-BR-008:** Closure permission, predecessor states, approved-answer absence, required revision transport, repeated close, reopened target state, snapshot copy-versus-reference, and close/reopen response contracts.  
**Needs confirmation — OQ-BR-023:** Resolve historical source access and retained lineage when later retention, source deletion, or workspace deletion applies.

### Document and Evidence Decisions

<a id="br-016"></a>
#### BR-016 — File Admission and Unsafe Quarantine

| Condition | Confirmed result |
|---|---|
| Supported PDF, DOCX, HTML, or UTF-8 text with agreeing MIME signature/extension and satisfied configured limits | Eligible for scan and subsequent pipeline processing; not immediately `READY`. |
| MIME signature and extension disagree | Not accepted; fail closed. |
| File exceeds configured per-file cap | Fail closed; no unsafe processing or false acceptance. |
| Decompression-bomb threshold is violated | Fail closed under bounded parser/sandbox controls. |
| Content is unsafe | `QUARANTINED`; never enter search index. |
| Embedded macro or remote reference | Macro execution disabled; remote reference not fetched. |
| Malformed connector document persists after bounded retries | Quarantine with reason/correlation/remediation under BR-035. |

**Confirmed numeric source value:** Configurable **25 MB per-file cap**.

**Confirmed order:** Scan uploads before parsing.

**Sources:** [DDS], p. 30, §§8.1.1–8.1.2; p. 88, `T-04`; p. 89, `TST-015`.

**Needs confirmation — OQ-BR-009:** Exact allowlist, decimal/binary MB, inclusive equality boundary, aggregate size/file-count limits, decompression threshold, encrypted/corrupt-file handling, parser bounds, quarantine remediation, and safe rendering. No `413`, `415`, or named upload-error code is supplied.

<a id="br-017"></a>
#### BR-017 — Immutable Normalization and Source Anchors

**Confirmed:**

1. Parse PDF pages into blocks with page index and bounding boxes.
2. Preserve table row/column annotations; headings and reading order inform chunk boundaries.
3. OCR fallback is opt-in and provenance-marked; OCR beyond English is deferred.
4. Strip transport artifacts without rewriting claims.
5. A content fingerprint plus pipeline version produces immutable derivative IDs.
6. Reprocess changed pipelines side by side; do not overwrite previously cited derivatives.
7. Every chunk stores source URI, file hash, page number, and optional bounding box.
8. Generation cites only chunks with resolvable anchors and current access permission.
9. Citation click-through opens the cited source and highlights its anchored page range.

**Sources:** [DDS], p. 31, §§8.2–8.3.1; p. 57, §16.1.2.

**Needs confirmation — OQ-BR-009:** OCR opt-in scope/default and normalization rules.  
**Needs confirmation — OQ-BR-011:** Fingerprint/identity generation, parser-versus-pipeline version, page numbering, non-PDF anchors, bounding-box units, source URL lifetime, hash encoding, and highlight behavior.

<a id="br-018"></a>
#### BR-018 — Extraction-Quality Eligibility

| Source condition | Viewing | Autonomous recommendation use |
|---|---|---|
| Safe, authorized material satisfying quality gates | Permitted under resource authorization. | Eligible under other evidence/policy guards. |
| Safe, authorized material determined low quality | Remains viewable. | Excluded. |
| Unsafe quarantined material | Safe viewing contract is not supplied. | Not indexed; cannot enter recommendations through the normal evidence index. |
| Missing/indeterminate quality result | **Needs confirmation.** | Do not invent an eligibility default. |

Quality flags include empty-page ratio, unknown-character ratio, table-loss indicators, and language confidence.

**Source:** [DDS], p. 32, §8.3.2; unsafe distinction p. 30, §8.1.2.

**Needs confirmation — OQ-BR-010:** Formulas, denominators, units/scales, thresholds, equality boundaries, missing flags, indexing/readiness treatment, and whether/how reviewed manual use differs from autonomous use. No quality threshold is supplied.

<a id="br-019"></a>
#### BR-019 — Grounded Retrieval and Verified Citations

**Confirmed retrieval procedure:**

1. Form lexical and normalized vector queries.
2. Retrieve bounded candidate sets.
3. Merge using reciprocal rank fusion and apply deterministic reranking.
4. Limit redundant same-document hits and reserve relevant-source coverage.
5. Cap tokens returned to the model under per-query budgets.
6. Apply originating ACLs before releasing text.
7. Include chunk ID, source title, document revision, page anchor, and ACL digest in each response evidence item.
8. Keep citation identifiers opaque and verify them before display.
9. Require resolvable source anchors and current permission.

| Evidence condition | Result |
|---|---|
| Sufficient confidence/quality, permitted sources, resolvable anchors | Return supported evidence; all later gates still apply. |
| Insufficient confidence or evidence quality | `NO_SUPPORTED_EVIDENCE`; do not fabricate context. |
| Clarification or human help is appropriate | Orchestrator may ask for clarification or route to a human; routing contract NC. |
| Generated response lacks citations | `TST-009`: needs-review or unsupported outcome; no unsupported publication. |
| Cited source becomes unauthorized or anchor invalid | Do not treat the citation as valid; publication revalidation applies. |

The source confirms RRF as the algorithm name, not its equation, score weights, rank indexing, ties, or rounding. Appendix F values `max_candidate_chunks: 80`, `max_selected_chunks: 10`, and `hybrid_rrf_k: 60` remain examples. The separate MCP tool has confirmed `max_items: int<=10`; that is not a public list-page size.

**Sources:** [DDS], pp. 31, 34–36; pp. 57–58; pp. 87, 89–90.

**Needs confirmation — OQ-BR-011:** Query constraints, ranking/tie rules, RRF parameters/formula, diversity quotas, token budgets, confidence/evidence thresholds, source conflicts, minimum citation coverage, and clarification/human-routing outcomes. The illustrative `5 verified citations` is not a minimum.

<a id="br-020"></a>
#### BR-020 — Search Derivative Authority and Rebuild Gate

**Confirmed:**

- PostgreSQL/source metadata is authoritative; search is a nonauthoritative eventually consistent derivative.
- Search rows carry tenant/workspace/version/chunk, language, classification, normalized keyword text, and a **1536-dimensional embedding**.
- Index writes use versioned aliases.
- Rebuild a parallel generation; switch the read alias atomically only after completeness and recall checks.
- Failed indexing preserves accepted source metadata and requires fingerprint reconciliation/retry.
- Search readiness depends on index coverage, not queue emptiness alone.

**Sources:** [DDS], p. 16, §3.2.2; p. 34, §9.1; p. 49, §13.2.2; p. 78, §22.1.2.

**Needs confirmation — OQ-BR-011:** Coverage/completeness/recall formulas and thresholds, empty-corpus behavior, concurrent-update catch-up, index-generation retirement, and permitted nonsecurity staleness. No acceptable ACL staleness is created by eventual consistency.

<a id="br-021"></a>
#### BR-021 — ACL Revocation, Cache Invalidation, and Soft Deletion

| Change | Required result and priority |
|---|---|
| Source ACL revocation | Effective before the next retrieval. |
| Source ACL or authorization change | Purge affected cache entries before new results are served and before normal TTL expiry. |
| Source delete | Create tombstone and schedule index removal. |
| Entity is soft-deleted | Cannot be retrieved, even if physical index removal is pending. |
| Permission changes between search and publication | Recompute authorization and reject stale evidence. |
| Stale unauthorized content remains visible | Treat as security incident, not a tolerated cache result. |

Cache keys contain tenant, user-scope digest, source ACL revision, query hash, and index generation.

**Sources:** [DDS], pp. 27–29; pp. 46, 51–53; p. 89, `TST-004`.

**Needs confirmation — OQ-BR-012:** Revocation atomics, source-change detection, group/membership mapping, in-flight query behavior, multi-source digest scope, URL revocation after issuance, cache TTL, and safe connector restrictions where ACL discovery is missing.

### AI Admission, Routing, and Policy Decisions

<a id="br-022"></a>
#### BR-022 — Maximum Information Class and Approved Model Routing

**Confirmed information classes:** `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`.

The maximum class of any material included in a run governs model route, log redaction, retention, and approval policy.

A symbolic expression of the confirmed requirement is:

> Governing run class = maximum information class among included material.

This expresses the requirement only; the comparison encoding, material-set definition, and missing-class treatment are NC.

| Route condition | Result |
|---|---|
| Specific deployment is approved by workspace policy and applicable data-handling restrictions | Eligible for selection under capability/context/evaluation constraints. |
| Only provider brand is allowlisted | Insufficient; policy must allow specific deployments. |
| Fallback is approved and has equal or stronger data-handling class | Fallback may be eligible; it is not mandatory. |
| Fallback deployment or region is unapproved | Do not route there. |
| Provider outage with restricted content | No unapproved regional/deployment fallback. |

Registry data includes capability, region, data-handling class, context length, cost profile, and evaluation approval.

**Sources:** [DDS], p. 37, §10.1; p. 62, §17.2.1; p. 88, `T-06`.

**Needs confirmation — OQ-BR-013:** Class ordering/encoding, classification inheritance, missing/changed classification, included-material scope, model-class compatibility, context limits, and redaction eligibility.  
**Needs confirmation — OQ-BR-030:** Select approved deployments/regions/providers explicitly.

<a id="br-023"></a>
#### BR-023 — Controlled Prompt and Structured Output

**Confirmed prompt content:** Fixed system rules, signed workflow instruction, validated user input, and separately delimited retrieved passages.

**Confirmed controls:**

- Label retrieved content untrusted.
- Strip tool-call directives from evidence contexts.
- Record prompt-injection indicators.
- Do not alter immutable source claims when preparing a separate evidence context.
- Request a versioned JSON schema and parse with bounded retries.
- Unknown fields, invalid citations, or control-character injection trigger `MODEL_OUTPUT_INVALID`.
- Tool authorization remains outside model text.
- Invalid output cannot publish.

**Sources:** [DDS], pp. 38–39, §§10.2–10.3.2; p. 89, `TST-005`.

**Needs confirmation — OQ-BR-013:** PII/redaction and permitted prompt-data scope.  
**Needs confirmation — OQ-BR-015/OQ-BR-022:** Output schema, injection detection/stripping definitions, bounded parse retries, failed-attempt accounting, and resulting checkpoint/status representation. Detection must fail closed against authority escalation; the source does not define that every detected indicator necessarily terminates all processing.

<a id="br-024"></a>
#### BR-024 — Queue-Aware Run Admission

| Workspace tokens satisfy threshold | Queue age satisfies threshold | Provider capacity satisfies threshold | Admission result |
|---|---|---|---|
| Yes | Yes | Yes | Admission guard satisfied; authorization/input/policy guards still required. |
| No | Any | Any | Throttle new AI run. |
| Any | No | Any | Throttle new AI run. |
| Any | Any | No | Throttle new AI run. |
| Unknown | Any | Any | Exact handling NC; unknown does not establish satisfaction. |
| Generation admission disabled during provider outage | Any | Any | Do not admit new generation under the outage runbook. |

Throttled clients receive HTTP `429` and `Retry-After`; saved cases remain available.

**Sources:** [DDS], p. 69, §19.2.1; p. 79, §22.2.1.

**Needs confirmation — OQ-BR-014:** Threshold values/units, token reservation atomics, queue-age definition, capacity calculation, equality, quota window, and handling of simultaneous requests. Reference `20 concurrent AI runs per large tenant` is a load assumption, not an independently approved admission quota.

<a id="br-025"></a>
#### BR-025 — Token Reservation and Quota Exhaustion

**Confirmed:**

1. Each run reserves input and output token budgets.
2. Track provider usage under workspace quota.
3. Quota exhaustion is terminal for the current run.
4. Do not automatically change model or data class to avoid quota exhaustion.
5. Attribute usage to run and actual deployment; daily reporting preserves cost-center/deployment-version context.

**Sources:** [DDS], p. 38, §10.3.1; p. 65, §18.3.1; p. 85, `token_ledger`.

**Needs confirmation — OQ-BR-014:** Tokenizer/count authority, reservation/actual/release calculation, retries and failed-call billing, missing provider usage, quota reset window, exact exhaustion equality, spend units/currency, and rounding. No pricing or forecast formula is supplied.

<a id="br-026"></a>
#### BR-026 — Bounded Plans, Checkpoints, and Stop Conditions

**Confirmed plan constraints:**

- Directed acyclic graph.
- Maximum depth **eight**.
- Maximum **sixteen tool invocations**.
- Explicit dependencies and replayable checkpoints.
- Persist plan revision before executing side effects.
- Persist each stage checkpoint before downstream dispatch.
- Triage Agent classifies; Research Agent requests grounded evidence; Draft Agent assembles candidate.
- Policy Evaluator is deterministic, not an LLM agent.

**Confirmed run vocabulary:**

`REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED`.

**Source-described progression:**

`REQUESTED -> RETRIEVING -> GENERATING -> POLICY_CHECK -> AWAITING_REVIEW -> PUBLISHED`, or terminal failure.

| Condition | Required behavior |
|---|---|
| Plan exceeds depth eight or tool-invocation maximum sixteen | Do not execute beyond the bound. |
| Call budget exhausted | Terminate and report failed checkpoint. |
| Repeated invalid plans | Terminate; numerical repetition limit NC. |
| Policy denial | Terminate the denied execution path. |
| Deadline expiry | Terminate; exact deadline/timeout accounting NC. |
| Missing approval | §11.3.1 states termination; distinction from valid `AWAITING_REVIEW` is unresolved. |
| Normal maximum runtime reached | §2.3.1 requires terminal result or recoverable timeout; recoverable representation is unresolved. |

Appendix F `run_timeout_seconds: 180` is an example, not a selected HTTP timeout or reviewer SLA.

**Sources:** [DDS], p. 12, §2.3.1; pp. 40–42; p. 49, §13.2.1; pp. 82, 90.

**Needs confirmation — OQ-BR-015:** Depth counting, whether retries/failed dispatches consume calls, invalid-plan count, automatic-allow path, missing approval versus valid waiting, review-time accounting, and recoverable timeout state. Do not resolve these by adding a new state or silently timing out human review at 180 seconds.

<a id="br-027"></a>
#### BR-027 — Independent Tool/A2A Authorization

| Invocation condition | Result |
|---|---|
| Capability merely registered/discovered | No invocation permission. |
| Approved pinned schema, valid arguments, and separate applicable grant | Eligible for dispatch. |
| Arbitrary or unauthorized MCP capability | `DENY` before dispatch; not a newly defined HTTP error code. |
| External write | Separate capability authorization required. |
| Mutable action | Idempotency key required. |
| Consequential mutable action | Human authorization also required. |
| Requested action denied | Planner cannot substitute a semantically equivalent tool. |
| A2A receiver declines | Decline is permitted; response/status contract NC. |

A2A handoffs carry task ID, capability reference, declared input/output schemas, deadline, and trace context.

The exact MCP tool contract remains:

| Element | Confirmed contract |
|---|---|
| Tool | `knowledge.search@v1` |
| Input | `{query: string, case_id: uuid, max_items: int<=10}` |
| Output | `{evidence_set_id: uuid, citations: Citation[]}` |
| Authorization | `read:permitted_documents`, tenant-scoped |
| Effect | Read-only; no arbitrary URLs or filesystem access |

The upper bound ten is confirmed; lower bound, omission/default, and formal requiredness are NC. These names do not establish the public `POST /v1/search` schema.

**Sources:** [DDS], pp. 41–42; p. 87, §C.2; p. 89, `TST-014`.

**Needs confirmation — OQ-BR-016:** Tool grants/actions, consequential classification, schema transports, A2A output-schema carrier/decline protocol, `Citation`, and authorization-ref resolution.

<a id="br-028"></a>
#### BR-028 — Deterministic Policy Inputs and Outcomes

**Confirmed input inventory:**

| Input | Meaning | Missing contract |
|---|---|---|
| Case sensitivity | Information-handling context; maximum included class also governs run policy. | Class mapping/inheritance and effective version. |
| Requested action | Operation being evaluated. | Action vocabulary and consequence taxonomy. |
| Evidence quality | Quality/support input. | Calculation, thresholds, missing values. |
| Model class | Actual route/model handling context. | Vocabulary and compatibility matrix. |
| Financial impact category | Normalized impact input. | Categories, calculation, units, and thresholds. |
| Confidence bands | Normalized confidence input. | Source confidence, band cutoffs, equality, aggregation. |

Normalize and store **all evaluated inputs** with rule-set version. Preserve `rule_version`, `input_digest`, result, and reproducible input evidence. A digest alone does not replace stored normalized inputs.

**Confirmed outcomes and implications:**

| Outcome | Confirmed meaning and limitation |
|---|---|
| `AUTO_ALLOW` | Deterministic allow outcome. It does not waive evidence, current authorization, structured-output, or publication controls. Exact automatic-publication transition NC. |
| `HUMAN_REVIEW` | Require policy-routed human review before the applicable action/publication. |
| `REQUEST_MORE_EVIDENCE` | Additional evidence is required; do not treat current unsupported content as publishable. Exact case/run routing NC. |
| `DENY` | Denied path cannot proceed or be bypassed with equivalent tools. Authorized override/rework constraints remain BR-033. |

High-impact recommendations become review tasks rather than autonomous mutations. An LLM may propose risk tags but cannot override outcomes.

**Sources:** [DDS], p. 40, §11.1.1; p. 44, Chapter 12 and §12.1; pp. 45–46; p. 85.

**Needs confirmation — OQ-BR-017:** Supply the actual decision matrix mapping normalized inputs to outcomes, high-impact/high-risk definitions, confidence/evidence thresholds, rule combination priorities, missing-input behavior, and effective periods.

Appendix F:

- `auto_publish_classification: INTERNAL`
- `require_human_review_for: [HIGH_RISK, RESTRICTED]`
- `self_approval_allowed: false`

These remain configuration examples. `HIGH_RISK` is a risk tag, not a fifth information class. No rule here confirms that every `INTERNAL` candidate is automatically publishable.

### Review, Expiry, Publication, and Rework

<a id="br-029"></a>
#### BR-029 — Reviewer Eligibility and Separation of Duties

**Confirmed prerequisites:** Policy-defined reviewer pool, minimum role, applicable assignment, resource access, and separation of duties.

- Reviewer selection depends on policy and organizational role.
- An Analyst cannot approve their own high-risk recommendation.
- An unapproved high-risk run cannot publish.
- Appendix B states `approval_tasks` has `no self approval`; Appendix F illustrates `self_approval_allowed: false`.
- Administrative status does not itself authorize review, and author-selected role/pool values do not establish eligibility.

**Sources:** [DDS], p. 11, §2.1.2; p. 45, §12.2.1; pp. 85, 90.

**Needs confirmation — OQ-BR-001/OQ-BR-019:** Define pools, minimum roles, organization relationships, authorship predicate, reassignment rights, and global self-approval scope. No self-approval exception is approved by this gap.

<a id="br-030"></a>
#### BR-030 — Exact Review Context and Immutable Decision Capture

**Confirmed review context:** Exact candidate artifact, source citations, actual model/prompt versions, and policy reasons. A reviewer must be able to inspect source evidence before approval.

**Confirmed capture:** Decision, actor, timestamp, evaluated artifact hash, rationale, and optional annotations.

| Submission condition | Result |
|---|---|
| Required review fields incomplete | Disable both Approve and Reject; server validation remains authoritative. |
| Authorized valid task, exact unchanged artifact, applicable separation satisfied, required fields complete | Record accepted binding decision; API returns `200`. |
| Artifact changed or wrong/prior hash supplied | Reject as stale and audit; API conflict surface `409`. |
| Actor/task permission fails | Reject without accepted decision/publication. |
| Annotation absent | Permitted; annotations are optional. |
| Approval record accepted | Not yet proof of publication; BR-032 applies separately. |

Historical decisions are immutable.

**Sources:** [DDS], p. 45, §12.2.2; pp. 57–58; pp. 83, 85; p. 89, `TST-006`.

**Needs confirmation — OQ-BR-018:** Exact required fields, decision request enum, rationale nonblank/length rules, annotation format, hash canonicalization/encoding, task ID mapping, and conflicting decision handling. No “all citations clicked” requirement or mandatory evidence checkbox is supplied.

<a id="br-031"></a>
#### BR-031 — Review Expiry and Escalation

**Confirmed:** Tasks expire after a configured SLA and are reassigned or escalated without silently approving. `TST-010` requires no implicit approval and recorded escalation.

Review vocabulary:

`ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED`.

| Condition | Result |
|---|---|
| Task reaches configured expiry | Apply expiry and policy routing; never implicit approval. |
| Reviewer unavailable | Does not establish approval. |
| Decision and expiry occur concurrently | Exact resolution NC; no approval bypass or history rewrite permitted. |
| Decision arrives after expiry/reassignment | Validity and response rules NC. |
| No tasks expire | No-op/status/audit contract NC; no task is approved automatically. |

**Sources:** [DDS], p. 45, §12.2.1; pp. 82, 89.

**Needs confirmation — OQ-BR-019:** SLA duration/unit, start event, elapsed/business-clock treatment, equality, timer cadence, eligible predecessor states, late decisions, reassignment identity, escalation recipients, and multi-reviewer conflict resolution.

<a id="br-032"></a>
#### BR-032 — Atomic Publication Gate

The following table lists independently necessary conditions. It does not prescribe a first-match order or complete implementation algorithm.

| Publication condition | Required result |
|---|---|
| Required supporting evidence absent/insufficient | Do not publish unsupported answer. |
| Candidate/model output invalid | Do not publish. |
| Current source/case authorization fails or evidence is stale | Reject publication. |
| Required approval policy unsatisfied | Do not publish. |
| High-risk run is unapproved | Do not publish. |
| Approval hash differs from candidate hash | Reject stale binding; do not publish changed artifact. |
| Applicable policy, evidence, authorization, exact binding, and approval requirements all satisfied | Record satisfied gate and update final response pointer in the **same transaction**. |
| Accepted event replayed | No second accepted business transition. |
| Old approval replayed for different artifact | Cannot publish that artifact. |

Retrieval, generation, policy decision, and reviewer approval remain separate records. `ApprovalDecisionRecorded` leads to publication validation, not unconditional publication.

**Sources:** [DDS], pp. 7, 11–13; pp. 45–46, §§12.3.1 and 12.5; p. 52, §14.2.1; p. 87.

**Needs confirmation — OQ-BR-020:** Automatic-allow trigger, public publication control if any, current policy/evidence revalidation scope, decision expiry/revocation, multi-reviewer sufficiency, transaction races, and publication state/event projection. No public Publish endpoint or button is confirmed.

<a id="br-033"></a>
#### BR-033 — Override and Rework Constraints

| Action | Required conditions/result |
|---|---|
| Authorized override | Elevated role **and** secondary reviewer **and** audited reason. These are cumulative requirements. |
| Missing any override requirement | Cannot bypass the policy through the override path. |
| Denied request reworked | New run revision; candidate follows evidence, model, policy, review, and publication controls again. |
| Historical denial changed retroactively to approval | Prohibited. |
| Rejected draft rework | Supported acceptance flow; preserve historical decision/candidate lineage. |

**Sources:** [DDS], p. 46, §12.3.2; p. 75, §21.3.1.

**Needs confirmation — OQ-BR-020:** Eligible override cases, elevated role, secondary reviewer independence, reason contract, exact overridden result, endpoint, new-run linkage, and version applicability. This rule does not authorize overriding tenancy, excluded capabilities, or arbitrary tool restrictions.

### Connector, Retry, Audit, and Exit Decisions

<a id="br-034"></a>
#### BR-034 — Connector Trust and Credential Lifecycle

**Confirmed capability inventory:** List, fetch, delta cursor, ACL, and delete support.

| Condition | Result |
|---|---|
| Capabilities advertised and supported | Use only advertised/supported behavior with applicable authorization. |
| Capability unsupported | Lower-trust ingestion mode and explicit user-visible warning; no silent support assumption. |
| Connector credential stored | Dedicated secret store under workspace-scoped reference. |
| Credential revoked while job queued | Fail queued job with `CONNECTOR_REAUTH_REQUIRED`; do not expose token. |
| Provisioning incomplete | Block sync under BR-042. |
| Admin submits valid authorized sync request | Accepted asynchronous sync returns `202`; not sync completion. |

**Sources:** [DDS], p. 27, §7.1; p. 78, §22.1.1; p. 83.

**Needs confirmation — OQ-BR-021:** Capability schema/providers, lower-trust restrictions, sync/read/operator grants, revocation/reauthentication contracts. Unsupported ACL capability cannot relax BR-021.

<a id="br-035"></a>
#### BR-035 — Durable Incremental Synchronization

**Confirmed:**

1. Preserve source identity, permissions, and change history.
2. Each sync run stores provider cursor, high-watermark, and error ledger.
3. Advance cursor only after all preceding items have durable ingestion outcomes.
4. Retry partial batches safely without losing accepted outcomes.
5. After bounded retries, malformed documents enter quarantine with reason code, correlation ID, and remediation path.
6. Remaining batch may proceed while the cursor ledger records the exception.

| Preceding item state | Cursor consequence |
|---|---|
| Durable accepted or durably recorded exception outcome | May satisfy the preceding-outcome requirement under the resolved cursor contract. |
| Outcome not durable | Cannot advance past that item. |
| Item retried after accepted outcome | Do not duplicate accepted business effect. |
| Malformed item retry bound exhausted | Record quarantine exception; remaining batch continuation is permitted. |
| No provider changes | Exact cursor/no-change completion rule NC. |

**Sources:** [DDS], pp. 27–29, §§7.2–7.3.2.

**Needs confirmation — OQ-BR-021:** Cursor ordering/expiry, current-versus-run-history layout, concurrency/fencing, batch bounds, accepted exception categories, source ID namespaces, and empty-delta outcomes.

<a id="br-036"></a>
#### BR-036 — Fair Throttling, Bounded Retry, and Controlled Replay

**Confirmed retry distinctions:**

| Condition | Behavior |
|---|---|
| Transient dependency/read fault | Bounded exponential backoff, randomized jitter, applicable circuit breaker. |
| Validation or permission failure | Permanent; do not retry as transient. |
| Provider throttles connector work | Honor `Retry-After`; enforce workspace quotas. |
| Large tenant demand | Fair scheduling prevents starvation of smaller workspaces. |
| Provider `429` burst | Capped retries; admitted load controlled. |
| Malformed connector record persists | Bounded retry then recorded quarantine. |
| Mutable/consequential tool | Idempotency and separate/human authorization still apply during retry. |
| Dead-letter replay | Operator reason, dry-run validation, and scope limit required. |
| Replay schema unchanged | Preserve original event identity. |
| Explicit schema migration transforms replay | Preserve explicit provenance link. |

No fair-scheduling algorithm, backoff equation parameters, retry count, circuit threshold, or replay size/time limit is supplied.

**Sources:** [DDS], pp. 28–29; p. 42, §11.3.2; pp. 49–50; pp. 89–90.

**Needs confirmation — OQ-BR-022:** Retry taxonomy/bounds, `Retry-After` syntax/propagation, exhausted disposition, circuit recovery, worker-loss ownership, replay reason/scope/dry-run contracts, and no-input replay outcomes.

<a id="br-037"></a>
#### BR-037 — Immutable Audit and Privacy-Safe Disclosure

**Confirmed:**

- Audit entries and case revisions are append-only; approval decisions are immutable.
- Audit entries are chained with batch hashes and exported to independently controlled retention storage.
- Operators can query authorized evidence but cannot alter historical review decisions.
- Auditor scope includes decision metadata, prompt-template digests, access events, and authorized redacted content; not case-content editing.
- Every request carries `trace_id` and `correlation_id`; correlation crosses boundaries independently of provider trace identity.
- Diagnostic trace attributes contain identifiers and policy outcomes, never user documents or API secrets.
- Error details exclude connector credentials, full prompts, retrieved documents, and unauthorized resource existence.
- Model/tool calls receive no secrets outside declared scope; providers do not receive raw connector tokens or unrestricted database access.
- Extraction tags likely personal data; gateway redacts nonessential fields before provider invocation where policy permits.
- Logs capture counts/digests, not entire prompts by default.
- Application secrets remain in vault-backed references; managed identity where supported.
- Service credentials rotate automatically; encryption-key rotation follows defined policy without bulk reencryption in the request path.
- Source objects are encrypted; signed URLs are access-controlled and short-lived.

**Sources:** [DDS], pp. 11, 15, 21, 27, 52, 54, 61–66, 84–85.

**Needs confirmation — OQ-BR-013/OQ-BR-023:** PII categories/redaction, auditor source access, audit batch/hash/export protocol, retained actor identities, secret/key rotation policy, and authorized content retention. No unrestricted full-prompt logging exception is approved here.

<a id="br-038"></a>
#### BR-038 — Retention Eligibility and Legal Holds

| Target/condition | Result |
|---|---|
| Case is not closed | Not eligible for case-retention processing described by §6.3.2. |
| Case closed but retention eligibility not satisfied | Do not purge under that retention rule. |
| Eligible closed case, no applicable hold | Eligible for the authorized retention pipeline; exact related inventory NC. |
| Record protected by legal hold | Retain and record protected/held outcome. |
| Diagnostic record | Separate diagnostic policy; source default TTL **30 days**. |
| Security-audit record | Distinct source fictional policy **seven years**. |
| Purge occurs | Record completion receipts and legal-hold exceptions. |
| All targets held or selection empty | No protected purge; exact operation completion/no-op representation NC. |

Corporate retention policy selection remains explicitly open in §F.2. The source defaults do not establish production policy precedence.

**Sources:** [DDS], p. 26, §6.3.2; p. 66, §18.3.2; pp. 80, 89–90.

**Needs confirmation — OQ-BR-023:** Retention classes/durations, age clock, equality, calendar-year versus elapsed-year semantics, hold races/releases, related artifact scope, backup handling, immutable lineage survival, and scheduler. The closed-case restriction is not automatically imposed on every target in independently approved workspace deletion.

<a id="br-039"></a>
#### BR-039 — Independent Export/Deletion Approvals

**Confirmed:** Export and delete operations require **two independent approval checks**. The API scope is `Admin + approver`; `T-11` describes two-person approval and a single-Admin bypass test.

| Conditions | Result |
|---|---|
| Single Admin, no independent approval | Operation cannot proceed. |
| Applicable Admin and approver authorization with two independently verified checks | Approval prerequisite satisfied; inventory, retention, hold, and idempotency guards remain. |
| Same person presented twice as independent authorization | Cannot satisfy the source-described two-person control. |
| Approval evidence missing/invalid | Do not treat the prerequisite as satisfied. Exact failure mapping NC. |
| `202` returned after valid admission | Durable operation accepted, not completed export/deletion. |

**Sources:** [DDS], p. 78, Chapter 22 invariant; p. 83; p. 88, `T-11`.

**Needs confirmation — OQ-BR-024:** Exact approver role, whether initiator may participate in one check, approval object/binding, scope changes, expiry/revocation, secondary-user verification, and execution-time rechecks. Two client-selected IDs are not a resolved approval protocol.

<a id="br-040"></a>
#### BR-040 — Authorized Export Content

**Confirmed exported content:**

- Case metadata.
- Approved artifacts.
- Source references.
- Audit manifests.
- Checksums.

**Confirmed exclusions:** Secrets and internal model prompts.

Export requires BR-039 and authorized resource scope. No automatic export-then-delete sequence is supplied.

**Source:** [DDS], p. 79, §22.3.1.

**Needs confirmation — OQ-BR-024:** Snapshot time/consistency, draft/held-content treatment, archive/manifest format, checksum protocol, empty/partial export, size/lifetime, authorized recipient/download, and status APIs. Source references do not confirm export of every raw source binary.

<a id="br-041"></a>
#### BR-041 — Verified Deletion and Shared Request Inventory

**Confirmed procedure:**

1. Enforce independently approved authorized scope.
2. Resolve deletion inventory and legal holds.
3. Write tombstones; soft-deleted entities cannot be retrieved.
4. Remove eligible blobs and index entries.
5. Preserve held protected records.
6. Record completion receipts and protected-record exceptions.
7. Verify outcome before the applicable completion evidence.
8. `TenantDeletionVerified` carries manifest ID/receipt hash concepts and closes the purge record idempotently.

Selected receipt fields are `tenant_id`, `object_ref`, `purge_time`, and `actor`.

Data-subject **access requests** use the same inventory. This wording does not establish automatic erasure for every access request.

**Sources:** [DDS], pp. 51, 80, 85, 87; p. 89, `TST-013`.

**Needs confirmation — OQ-BR-023/OQ-BR-024:** Relational purge, root tenant/workspace mapping, inventory grain, held/partial completion, receipt survival, backups, shared sources, historical citations, and access-versus-export-versus-erasure outputs.

### Onboarding, Period-End Processing, Degradation, and Release

<a id="br-042"></a>
#### BR-042 — Idempotent Provisioning and Reconciled Onboarding

**Confirmed:**

- Provision workspace policy, encryption references, role bindings, quotas, and connector stubs as one idempotent workflow.
- Visible incomplete provisioning blocks connector sync.
- Ingest historic documents in bounded windows using stable source IDs.
- Produce per-batch reconciliation receipts.
- Signal readiness using index coverage, not merely queue emptiness.

**Source:** [DDS], p. 78, §§22.1.1–22.1.2.

**Needs confirmation — OQ-BR-025:** Provisioning role/API, resource order, completeness predicate, partial-resource compensation, changed-config rerun, historical window boundaries/size, sync overlap, quarantine accounting, and readiness threshold.

<a id="br-043"></a>
#### BR-043 — Usage Attribution and Period-End Reporting

**Confirmed accounting content:**

- Attribute model invocations, embeddings, storage, and indexing usage.
- Carry workspace cost-center and actual model-deployment-version context.
- Track raw files, normalized text, chunk vectors, and replication overhead separately.
- Daily rollups show budget, forecast, and rejected excess requests.
- Usage API returns costs, quotas, and trend estimates.

| Period-processing element | Contract |
|---|---|
| Aggregation cadence | Daily rollups confirmed. |
| Reporting-day timezone/start/end | **Needs confirmation.** No midnight or workspace-local day is selected. |
| Input grain | Actual attributed usage confirmed; invocation/retry/ledger grain NC. |
| Cost formula | **Needs confirmation.** No rate table, currency, conversion, tax, or allocation formula supplied. |
| Forecast/trend formula | **Needs confirmation.** No horizon, method, confidence band, or update rule supplied. |
| Rounding | **Needs confirmation.** Token numeric types, money precision, rounding stage/mode NC. |
| Period boundary inclusion | **Needs confirmation.** No inclusive/exclusive event-time interval supplied. |
| Late/corrected usage | **Needs confirmation.** No reopen, replace, incremental adjustment, or restatement rule supplied. |
| Zero usage | **Needs confirmation.** Omit-versus-zero rollup and forecast behavior unresolved. |
| Month/year financial close or settlement | **Needs confirmation**, not out of scope. No such process is described. Monthly API availability is a different measurement under BR-046. |

**Sources:** [DDS], p. 65, §18.3.1; p. 68, §19.1.2; p. 83; p. 85.

**Needs confirmation — OQ-BR-026:** Resolve every calculation/window item above, cost-center selection, deduplication, corrections, quota resets, and execution schedule. Daily aggregation does not establish a standalone midnight batch job.

<a id="br-044"></a>
#### BR-044 — Safe Degradation and Incident Recovery

| Condition | Confirmed action |
|---|---|
| Generation unavailable | Keep evidence search/manual case editing online; display degraded state. |
| Provider outage runbook | Disable new generation admission; page on-call only when availability budget impacted. |
| Vector index degraded | Lexical retrieval may continue with visible reduced-quality flag. |
| Any degraded mode | Never bypass authorization or approval. |
| Suspected ACL leak | Suspend affected aliases, revoke cached evidence, preserve audit traces, replay scoped ACL revisions. |
| Reenable after ACL incident | Only after negative-access tests pass. |
| Delayed indexing | Pause only faulty connector/indexer shard; retain accepted records; bounded validated replay; verify fingerprints and denied-access probes. |

**Delayed-indexing evidence procedure:**

1. Detect oldest queue age/backlog and identify tenant/index generation.
2. Contain only the faulty connector/shard.
3. Diagnose event ID, outbox lag, parser flags, throttling, and ACL revision.
4. Recover with bounded operator-controlled validated outbox replay.
5. Verify source/index fingerprints and denied-access probes.
6. Link audit IDs, time window, blast radius, quality effect, and preventive action.

**Sources:** [DDS], pp. 68–70; p. 79, §22.2; p. 90, §F.1.

**Needs confirmation — OQ-BR-028:** Degraded fields, safe fallback eligibility, admission/outage precedence, incident thresholds, pause/reenable authority, probe definitions, and availability-budget calculation.

<a id="br-045"></a>
#### BR-045 — Truthful Accessible State and Progress

**Confirmed:**

- Artifact labels are `DRAFT`, `NEEDS_REVIEW`, and `PUBLISHED`; visual styling cannot replace accessible text.
- Keep artifact labels distinct from case/run/review/document states.
- Run created immediately after accepted admission; show durable retrieval/generation/policy stages through scoped SSE.
- Refresh reconstructs progress from server state, not browser memory.
- SSE offsets increase monotonically; reconnect uses `Last-Event-ID` and retained backfill within caller scope.
- Disconnection or request acceptance is not completion/publication.
- Reviewer can inspect source evidence before approval.
- Approve and Reject remain disabled until required review fields complete.
- Controls target WCAG 2.2 AA, visible focus, semantic regions, and keyboard ordering.
- Live updates announce only meaningful state transitions.
- Each confirmed primary screen has one primary action and a clear status summary; the actual primary action is not selected by this rule.

**Sources:** [DDS], p. 13; p. 55, §15.2.1; pp. 57–59; p. 89, `TST-011`.

**Needs confirmation — OQ-BR-027:** Aggregate-to-label mapping, routes/primary actions, summaries/formulas, SSE gaps/expiry/order handling, browsers/localization, detailed accessibility behavior, and notification/status contracts. Illustrative counts and mixed labels do not define new aggregate states.

<a id="br-046"></a>
#### BR-046 — Service Objectives and Actionable Alerts

| Measure/condition | Confirmed objective or decision |
|---|---|
| Public API availability | **99.9% monthly** target. |
| Case-create P95 | “Within 300 ms” in §2.3.1; “under 300 ms” in §18.2.1 — strict boundary unresolved. |
| Search P95 | Under **1.5 s**, excluding remote connector fetch. |
| Model generation latency | Measured separately. |
| API scaling | Based on utilization and latency. |
| Extraction/embedding scaling | Based on queue age and throughput. |
| User-impacting failure-budget, stale-ACL, missing-approval incident | Paging category. |
| Routine token-spend anomaly | Ticket with owner and threshold; actual assignment/threshold NC. |
| Model outage | Page only when availability budget impacted. |

Metrics include request/error rate, latency, saturation, grounding pass rate, retrieval empty rate, provider throttling, token use, and approval backlog age.

**Sources:** [DDS], pp. 12, 19, 64–65, 79.

**Needs confirmation — OQ-BR-028:** Availability denominator/exclusions/month timezone, burn-rate formula, measurement points, percentiles/sample windows, strict case latency equality, alert thresholds, and actual routes/owners. No numeric error budget or paging schedule is invented.

<a id="br-047"></a>
#### BR-047 — Primary-Region Writes and Controlled Recovery

**Confirmed:**

- R1 has one primary and one warm recovery region.
- Persistent writes target the primary.
- Secondary snapshots restore only under incident command.
- Continuous PostgreSQL backups target RPO `<=15 minutes` and RTO `<=4 hours`.
- Test object versions and index rebuild recipes with relational consistency.
- Fault injection covers provider `429` storms, lost worker heartbeats, duplicate events, object-access failures, and primary-region outage.
- Recovery acceptance measures both safety and elapsed recovery performance.

**Sources:** [DDS], p. 19, §4.2.2; pp. 69–70; p. 89, `TST-012`.

**Needs confirmation — OQ-BR-028/OQ-BR-030:** Regions/providers, write fencing, recovery measurement start/end, backup retention/hold/deletion propagation, drill cadence, and stale-worker ownership. Equal RPO/RTO target values satisfy the stated `<=` numerical boundaries but not omitted safety checks.

<a id="br-048"></a>
#### BR-048 — Compatible Release and Migration Gates

**Confirmed:**

1. Use the same container images/templates across environments, with isolated secrets/quotas.
2. Staging uses synthetic data/test connectors/reduced model spend; production data is forbidden in development.
3. No datastore is publicly exposed; egress permits declared model/connector endpoints.
4. Use documented declarative infrastructure modules; Terraform versus Bicep remains unselected.
5. CI performs static/dependency analysis, unit/contract tests, SBOM generation, and image signing.
6. Production deploys only digests verified against an allowed build identity.
7. State-machine/schema compatibility is assessed before traffic movement.
8. Expand-and-contract: nullable additions, bounded backfill, then constraint enforcement.
9. Do not remove fields while active readers depend on them; CI prevents incompatible field/enum changes.
10. Postdeploy enforcement follows old-replica drainage.
11. Rollback plans specify whether new-binary writes remain readable.
12. Canary compares latency, errors, authorization denials, and AI-quality regressions.
13. Regression triggers automated traffic rollback, not automatic database down-migration.
14. Reverse binary/traffic first; compensating data operations only when explicitly supported.
15. Security/SRE validate egress, secrets, backup status, and alert routing before promotion.
16. Release record binds image digest, schemas, prompts, and model-routing policy.

**Sources:** [DDS], pp. 18–20; p. 52, §14.2.2; p. 55, §15.3.1; pp. 71–73.

**Needs confirmation — OQ-BR-029:** Build/sign-off protocols, actual migrations/batch bounds, canary comparisons/thresholds/windows, compatibility matrix, explicit compensation, and release-state schema.

<a id="br-049"></a>
#### BR-049 — Frozen Evaluation and Safety-First Release Acceptance

**Confirmed corpus:** **1,200** synthetic permission-controlled cases covering retrieval, refusal, ambiguity, and adversarial evidence. Every example stores expected citations and decision outcomes. Corpora are frozen, versioned, independently reviewed for leakage, and protected through dataset version/signed manifest controls.

| Measure/gate | Confirmed boundary/result |
|---|---|
| Grounded citation precision | Target `>=0.97`; equality `0.97` meets numerical target. |
| Unsupported-claim rate | Target `<=0.02`; equality `0.02` meets numerical target. |
| High-risk policy recall | `1.00` on frozen safety suite. |
| Confidence intervals/distribution shift | Report by domain. |
| Low statistical confidence | Blocking release outcome, not equivalence evidence. |
| Critical isolation/approval tests | Zero exceptions. |
| Unmitigated critical cross-tenant or approval-bypass finding | Block promotion regardless of benchmark score. |
| Safety-regressed canary | Release gate blocks promotion. |
| Changed prompt or model | Reevaluate; independent rollout does not waive evaluation. |
| Uncontrolled expected-fixture replacement | Dataset/signature controls must prevent acceptance. |
| Empty/missing suite | Exact error result NC; no invented “empty denominator passes” convention. |

**Confirmed evidence:**

- Exercise deterministic transitions, tenancy, idempotency, hashes, retries, and schema compatibility without live model calls.
- Pin provider-facing adapters using consumer-driven contracts.
- Integration tests include transactions, replay, revocation, delayed indexing, and purge.
- Synthetic fixtures include successful, empty, mixed-permission, adversarial, and malformed input; record randomized seeds.
- Minimum release pack includes unit, schema evolution, negative authorization, replay, staging sync, visual accessibility, recall, grounding, policy recall, load, and DR tests.
- Sign test outputs and reference release digest.
- A security-control owner reviews evidence, independently reproduces negative cases, and signs the release record. No individual owner is appointed here.

**Sources:** [DDS], pp. 74–76; pp. 88–89.

**Needs confirmation — OQ-BR-029:** Metric numerators/denominators, aggregation, rounding, domains, confidence method/threshold, partial evaluation, signed-manifest protocol, exact gate combination, and individual `SEC-001`–`SEC-012` definitions. Meeting rounded display values is not established as a passing calculation rule.

<a id="br-050"></a>
#### BR-050 — Controlled Baseline Changes and Traceability

**Confirmed:**

- Controlled baseline decisions supersede informal design discussions; changes require architecture-decision records.
- Proposed changes carry impact scores for behavior, data migration, threat surface, and operating cost.
- Approved records increment minor revision; incompatible protocol changes increment major revision.
- Every revised invariant links to at least one negative test.
- Durable changes retain tenant, revision, actor, occurrence time, and correlation attribution.
- Provider/region/search/identity/model/retention/connector selections require dated architecture decisions before implementation lock.

**Sources:** [DDS], pp. 8–10, §§1.1–1.3; p. 90, §F.2.

**Needs confirmation — OQ-BR-029/OQ-BR-030:** Impact scales, revision formatting/reset behavior, approval protocol, governance permissions, and outstanding deployment selections. No owner, deadline, decision date, or approval is assigned by this specification.

### Confirmed Priorities and Unresolved Decision Ordering

| Interaction | Confirmed precedence/constraint | Unresolved ordering |
|---|---|---|
| Ranking versus authorization | Ranking cannot grant access; ACL required before text release. | Ranking tie-breaks and source-conflict resolution. |
| Model output versus policy/tool grants | Model/source text cannot override deterministic policy or separate grants. | Combination of multiple policy rules. |
| Cached result versus revoked authorization | Revocation/invalidation overrides normal TTL. | In-flight race protocol. |
| Expiry versus approval | Expiry cannot silently approve. | Simultaneous valid decision/expiry ordering. |
| Prior approval versus changed artifact | Exact hash binding prevents old approval applying to new content. | Multi-reviewer sufficiency/conflicts and approval lifetime. |
| Legal hold versus purge | Protected records retained/receipted. | Hold arrival during destruction and backup propagation. |
| Quota exhaustion versus cheaper/less restricted route | Current run terminates; no automatic model/data-class change. | Exact reservation/exhaustion equality and reconciliation. |
| Benchmark score versus critical safety failure | Critical isolation/approval failure blocks promotion regardless of score. | Statistical and noncritical quality-gate combination. |
| Index failure versus accepted source metadata | Preserve source authority; reconcile derivative. | Partial cross-store recovery/cleanup. |
| Webhook failure versus accepted case transition | Case remains committed. | Delivery retry/terminal status. |
| Canary regression versus database rollback | Traffic/binary rollback; no automatic down-migration. | Explicit supported compensation. |
| Advisory prediction versus contractual SLA | Prediction cannot change deadline. | Authorized contractual recalculation conditions. |

**Sources:** [DDS], pp. 25, 28, 34, 37–46, 49, 55, 72, 80, 88.

There is no source-confirmed universal priority such as `DENY > REQUEST_MORE_EVIDENCE > HUMAN_REVIEW > AUTO_ALLOW`, first-match evaluation, numeric rule weight, or unrestricted administrator override. **OQ-BR-017** must resolve the deterministic rule-combination contract without weakening the confirmed prohibitions.

## Application Points and Validation Conditions

### Enforcement and Data Mapping

References in this section link to the completed inventories in:

- [`01_screen_functions.md`](01_screen_functions.md): `SCR` fields/actions and shared requirements.
- [`02_api.md`](02_api.md): `API` interfaces, processing requirements, and gaps.
- [`03_data.md`](03_data.md): `DAT` datasets/fields and lifecycle requirements.
- [`04_batch_functions.md`](04_batch_functions.md): `BAT` logical functions and operational controls.

“Reads” and “updates” are logical data responsibilities. They do not declare missing physical columns or APIs. Screen enforcement is advisory/presentation enforcement; the applicable server, storage, transaction, and worker controls remain authoritative.

| Rule | Enforcing screens/actions | APIs and batch functions | Data read / update |
|---|---|---|---|
| BR-001 | `SCR-COM-012`; unlocated operational surfaces remain unresolved. | All interfaces; especially API-036/045/046/050; BAT-007/024/026. | Read DAT-024/032/036 allowed capabilities/deployment configuration; no excluded action data mutation authorized. |
| BR-002 | `SCR-X-001`; shared authenticated context. | API-027/048 and all authenticated boundaries; `BAT-OPS-001`. | Read DAT-019 identity/grants; use DAT-COM tenancy/actor context. |
| BR-003 | `SCR-COM-002`; SCR-002/003/005/006/007/008; `SCR-X` controlled operations. | API authorization inventory; API-028/029; all affected BAT functions. | Read DAT-019 membership/ACL/action policy, DAT-003 sensitivity, DAT-011 assignment; update only authorized targets and denial evidence. |
| BR-004 | `SCR-COM-003`; all resource opening/mutation. | All resource APIs/storage; `API-PROC-001`; `BAT-OPS-001`. | Read/write tenant-qualified DAT-001–018 and scoped objects/cache/index; DAT-REL integrity; DAT-COM-003 session reset. |
| BR-005 | `SCR-COM-012`; SCR-002/004/005. | API-036/045/046; BAT-007. | Read DAT-024 pinned tools/prompts and DAT-010 evidence; evidence/model content cannot mutate grants or scope. |
| BR-006 | `SCR-COM-010/011`; submission and failure displays. | `API-PROC-001`; relevant mutations/tools; `BAT-OPS-001/005/007`. | Validate resolved schemas; accepted target writes only; safe DAT-034 error/operation projection. |
| BR-007 | SCR-002-A03/A09; SCR-007-A02. | API-004/005; API-GAP-002; affected workers. | Read DAT-003 revision and DAT-002 configuration version; update DAT-003/004 or approved settings with audit/outbox. |
| BR-008 | SCR-002-A02/A05/A07; SCR-006-A02; SCR-011-A01; `SCR-X-003/X-004`. | API-001/006/011/012/018/023/025/026; `API-PROC-018`; `BAT-OPS-004`. | Read/write DAT-026 operation/fingerprint/outcome; one accepted target mutation. |
| BR-009 | SCR-004 progression; no inferred read-triggered mutation. | `API-COM-006`; API-037/038; BAT-010/011/012 and event consumers. | DAT-014 outbox, DAT-026 ledgers/checkpoints; accepted business target and audit; repair DAT-023 derivative. |
| BR-010 | SCR-007 fields/actions; actual controls remain unresolved. | API-GAP-002; API-020/036/045; BAT-007/013/014/026. | DAT-002/017/024/032 versions/configuration; retain evaluated inputs/actual versions. |
| BR-011 | SCR-001-A04 and SCR-002-A02/A04; placement proposals retained. | API-001; API-GAP-001; BAT-001. | DAT-003 current case; DAT-020 labels/confidences/provenance/correction reason. |
| BR-012 | SCR-002-F04–F06. | API-001/004; `API-CASE-F06`–`F08`. | Read explicit DAT-003-F12/F13; update derived DAT-003-F14 under resolved formula. |
| BR-013 | SCR-002-F24; `SCR-COM-008`; SCR-007-F09. | API-001/004 and timestamp contracts; affected deadline processing. | DAT-002-F10 calendar/timezone; DAT-003-F17 deadline; DAT-COM time values. |
| BR-014 | SCR-002-F08/A03/A09/A10. | API-001/004/005; API-GAP-005; applicable state consumers. | DAT-003 status/revision; DAT-004 append-only history; DAT-CODE-001. |
| BR-015 | SCR-002-A09/A10. | API-005; API-GAP-005; retention BAT-013 separately constrained. | Read approved DAT-025 artifact/citations/decisions; write closure snapshot/new revision without rewriting history. |
| BR-016 | SCR-002-F18–F20/A05; quarantine status. | API-006/007; BAT-002/003/004. | DAT-022 file/safety inputs; DAT-005/006/028 versions/objects; DAT-CODE-003 quarantine; no unsafe DAT-023 indexing. |
| BR-017 | SCR-003-F03–F10/F13; citation actions. | API-006/008/010/039/045; API-GAP-003; BAT-003/004. | DAT-006/007 immutable versions/anchors, DAT-022 layout/OCR, DAT-028 derivatives, DAT-010 citations. |
| BR-018 | SCR-002-F21; SCR-003-F12. | API-007/009/036; BAT-003/007. | Read DAT-022 quality; enforce DAT-010/023/025 autonomous-use eligibility without inventing a column. |
| BR-019 | SCR-003-A01–A03; SCR-002/SCR-005 citations. | API-008–010/045; BAT-007. | Read DAT-005/006/007/019/023; form DAT-010 evidence under resolved persistence contract. |
| BR-020 | SCR-006-F13; reduced-quality/search readiness where mapped. | API-009/010; BAT-004/005/011/019. | DAT-023 rows/generations/checks; source DAT-005–007 remains authoritative. |
| BR-021 | SCR-003-A04; SCR-006-A04; SCR-002-A12. | API-009/010/017/028; BAT-006/008/013/021. | DAT-019 ACL/membership; DAT-005 source state, DAT-027 caches, DAT-023 index, DAT-029 tombstones. |
| BR-022 | SCR-002-F07/F28; SCR-005-F10/F18; SCR-007-F03. | API-020/036/050; BAT-007. | Read classes DAT-003/005/023 and approved DAT-002/024 routes; retain actual invocation context. |
| BR-023 | SCR-004-F08; draft/review candidate displays. | API-036/050; BAT-007. | DAT-024 prompt/schema/attempt/injection data; DAT-010 evidence; invalid result cannot become approved DAT-025 pointer. |
| BR-024 | SCR-002-A07; degraded/throttle status. | API-011/012/030/042; BAT-007. | Read DAT-002 quota/DAT-036 admission data; allocate DAT-008/026 only after valid admission. |
| BR-025 | SCR-004-F07; SCR-010-F02/F09. | API-036/050/022; BAT-007/016. | DAT-008 budget, DAT-002 quota, DAT-016 `in_tokens/out_tokens`, DAT-030 attribution. |
| BR-026 | SCR-004 fields/progress/failure. | API-011–015/037; BAT-007/010. | DAT-008 plan/status/budget; DAT-009 steps/checkpoints; DAT-026 continuation. |
| BR-027 | `SCR-COM-012`; no arbitrary tool-definition control. | API-045/046; BAT-007. | DAT-024 pinned capability, DAT-019 grants, DAT-034 A2A envelope, DAT-026 idempotency. |
| BR-028 | SCR-002-F30/F31; SCR-005-F12/F18; SCR-007 policy. | API-017/036 and policy gap; BAT-007/008. | DAT-017 normalized inputs/`rule_version/input_digest/result`; DAT-025 candidate/evidence context. |
| BR-029 | SCR-005-F03/F04/A04; no author bypass. | API-016/017; BAT-007/008/009. | DAT-011 pools/assignment; DAT-019 actor/roles; DAT-025 authorship context mapping NC. |
| BR-030 | SCR-005-F07–F17/A02–A05; citation inspection. | API-016/017; API-GAP-004; BAT-008. | DAT-011 exact task/hash; DAT-012 immutable capture; DAT-025 actual candidate/context; DAT-013 stale denial. |
| BR-031 | SCR-005-F05/F06/A06. | API-016/017; BAT-009. | DAT-011 expiry/state/assignment; preserve DAT-012 decisions and escalation audit. |
| BR-032 | SCR-002-A12; SCR-005 accepted decision versus published status. | API-017; API-GAP-006; BAT-008. | DAT-010/011/012/017/019/025 current validation; atomic DAT-025 gate and DAT-003-F16 pointer. |
| BR-033 | SCR-005-A07; SCR-002-A11. | API-GAP-005/006; API-011 linkage NC; BAT-007/008. | Read denial DAT-012/017; write new DAT-008/025 lineage/override evidence; no old-decision rewrite. |
| BR-034 | SCR-006-F02–F05/A02/A03. | API-018/019/049; API-GAP-007; BAT-002. | DAT-021 capabilities/credentials; DAT-019 secret references; warning/reauth outcome. |
| BR-035 | SCR-006-F06–F12. | API-018/019/049; BAT-002/003/019. | DAT-015 cursor/watermark/retry; DAT-021 per-run/item ledger; DAT-005/006 stable sources. |
| BR-036 | Connector/remediation/run failures; `SCR-X-006`. | API-038/045/049/050; BAT-002/007/010–012/025; `BAT-OPS-005`. | DAT-015/026 retry/replay/identity/provenance; unchanged accepted targets on duplicates. |
| BR-037 | SCR-008; `SCR-COM-011`; authorized metadata panels. | API-021/029/036/039; BAT-014/015/024; all diagnostic boundaries. | DAT-013/004/012 immutable evidence; DAT-019/028 secrets; DAT-022 PII; DAT-030 safe diagnostics. |
| BR-038 | Policy retention field; `SCR-X-005`; purge displays unresolved. | API-029/040; BAT-013/014/021. | Read DAT-003 closed status, DAT-002 retention, DAT-029 holds; update eligible inventory and DAT-018 receipts. |
| BR-039 | `SCR-X-003/X-004`; no confirmed form. | API-025/026; BAT-020/021. | DAT-019 authorization; DAT-029 independent approval evidence; operation DAT-026. |
| BR-040 | `SCR-X-003`; status/download placement unresolved. | API-025; BAT-020. | Read permitted DAT-003/025/013 source references; write DAT-029 export manifest/DAT-FILE-004 package. |
| BR-041 | `SCR-X-004/X-005`. | API-026/029/040; BAT-013/021. | DAT-029 inventory/holds/tombstones, DAT-028 blobs, DAT-023 index, DAT-018 receipts. |
| BR-042 | SCR-006-F13; `SCR-X-002`. | API-GAP-008; API-018; BAT-018/019. | DAT-001/002/019/029 provisioning; DAT-005–007/023 stable backfill/coverage and receipts. |
| BR-043 | SCR-010; screen organization remains proposed. | API-022; BAT-016. | DAT-016/030 usage/rollups; DAT-002 quota/cost-center context; category distinction from DAT-036 sizing. |
| BR-044 | `SCR-COM-009`; SCR-003-F14; SCR-006/004 remediation. | API-030; protected controls unresolved; BAT-005/006/007/011/012. | DAT-036 degraded/admission data; DAT-023 aliases, DAT-027 revoked cache, DAT-013 incident traces. |
| BR-045 | `SCR-COM-005`–`008`; SCR-002/003/004/005; primary screens. | API-002/008/013–017; BAT-007/008/009 progress. | Read DAT-CODE-001–007, DAT-008/011/025 authoritative state and DAT-034 offsets; DAT-035 projections not new tables. |
| BR-046 | Shared health/status and SCR-010 where approved. | API-022/030/034/035/041/042; batch/platform monitoring. | DAT-030 metrics/alerts; DAT-036 capacity/load; actual calculations unresolved. |
| BR-047 | No confirmed recovery console. | API-042 operational context; BAT-023/005. | DAT-028 object versions, DAT-036 recovery evidence, DAT-FILE-007 backups, DAT-023 regenerated index. |
| BR-048 | `SCR-X-009`; no release UI confirmed. | API-031/043/044; BAT-022/026. | DAT-032 artifacts/config/migrations/rollout; DAT-031 tests; actual release bindings. |
| BR-049 | SCR-011; placement/read permission unresolved. | API-023/024/043; BAT-017/026. | DAT-031 frozen dataset/expected outcomes/scores/manifests/confidence; DAT-032 signed release linkage. |
| BR-050 | `SCR-X-008`; no design-decision screen confirmed. | API-032/033; controlled governance. | DAT-033 change/revision/invariant links; DAT-032 actual deployment decisions as resolved. |

### Satisfied, Unsatisfied, and Boundary Acceptance Conditions

These criteria validate confirmed behavior. Exact assertions that depend on unresolved formulas, schemas, clocks, thresholds, or schedules must await the linked open decision; test authors must not substitute local implementation defaults.

| Acceptance ID / rule | Satisfied-case assertion | Unsatisfied/boundary assertion | Source/test trace |
|---|---|---|---|
| AC-BR-001 / BR-001 | Approved knowledge/case capability follows all applicable guards. | No excluded automation, unrestricted browsing, fine-tuning, administrative agent permission, or deferred R1 capability becomes executable by request text. | [DDS], pp. 9–10, 19. |
| AC-BR-002 / BR-002 | Valid scoped identity reaches applicable authorization checks. | Unexpected algorithm, missing tenant claim, wrong service audience, or substituted job tenant is rejected before unauthorized work. Expiry equality awaits OQ-BR-001. | [DDS], pp. 18, 21–22. |
| AC-BR-003 / BR-003 | All applicable resource attributes satisfied; only authorized operation proceeds. | Role-only, navigation-only, discovery-only, or Admin-only case access does not bypass unresolved/resource predicates. | [DDS], pp. 21–23, 83. |
| AC-BR-004 / BR-004 | Valid tenant/workspace references and reset transaction context preserve scope. | Foreign ID returns same not-found class as absent; mismatched workspace tenancy rejected; pooled connection cannot retain prior tenant context. | `T-01`, `TST-003`; [DDS], pp. 23, 86, 88–89. |
| AC-BR-005 / BR-005 | Delimited evidence informs answer content only. | Hostile PDF/model directives cannot alter tenant, policy, approval, grant, or allowed network destination. | `T-02`; [DDS], pp. 7, 38–42, 61, 88. |
| AC-BR-006 / BR-006 | Valid accepted operation has authoritative result/identity. | Schema invalid gives `422`; denied/stale/unsafe work leaves accepted state unchanged; dependency failure never becomes ambiguous success or approved partial output. | [DDS], pp. 13, 54, 56, 84. |
| AC-BR-007 / BR-007 | Current revision update accepted with monotonic case/version evidence. | Stale `If-Match` gives `409 CASE_VERSION_CONFLICT` and current revision; no stale state change. Missing/malformed-header response awaits OQ-BR-003. | [DDS], pp. 24–25, 83–86. |
| AC-BR-008 / BR-008 | Same actor/body/key within case period returns one case and identical response. | Changed body/key reuse gives `409 IDEMPOTENCY_CONFLICT`; exact 24-hour equality and concurrent pending outcome await OQ-BR-003. | `TST-001/TST-002`; [DDS], pp. 25, 54, 89. |
| AC-BR-009 / BR-009 | Commit preserves mutation/outbox consistency and one accepted outcome. | Replay same event 100 times yields one accepted business transition; delayed/stale safety does not depend on cross-partition order. | `T-07`, `TST-007`; [DDS], pp. 48–52, 88–89. |
| AC-BR-010 / BR-010 | Accepted settings update has revision-safe audit; evaluations retain actual versions. | Stale update cannot replace policy; in-flight effective-version assertion awaits OQ-BR-004. | [DDS], pp. 24, 44, 71–73. |
| AC-BR-011 / BR-011 | Creation returns `201`, starts `NEW`, then async labels/confidences/provenance. | Correction without required reason not accepted; later correction/rerun races await OQ-BR-005. | [DDS], pp. 12, 83, 87. |
| AC-BR-012 / BR-012 | Resolved priority fixtures derive result from explicit impact/urgency. | Model output alone cannot determine priority; formula, missing input, tie, and rounding assertions blocked pending OQ-BR-006. | [DDS], p. 25. |
| AC-BR-013 / BR-013 | Resolved calendar fixture computes workspace-timezone deadline; local display labels timezone. | Advisory prediction or locale cannot alter contractual deadline/durable order; DST/holiday/equality awaits OQ-BR-007. | [DDS], pp. 25, 54, 59. |
| AC-BR-014 / BR-014 | Confirmed transition with all resolved guards accepted. | Unknown case-state value rejected by reference `CHECK`; unsupported transition not accepted. Closing/reopen guards await OQ-BR-008. | [DDS], pp. 25, 82, 86. |
| AC-BR-015 / BR-015 | Authorized resolved closure preserves approved answer, cited versions, decisions. | Explicit reopen creates new revision without changing historical snapshot; absence of approved result/closure role remains unresolved. | [DDS], pp. 24–26. |
| AC-BR-016 / BR-016 | Allowed matching file below resolved cap scanned before parse. | Unsafe/polyglot/bomb/mismatched/oversized input fails closed; unsafe material quarantined, not indexed. At exactly 25 MB waits for unit/equality decision. | `T-04`, `TST-015`; [DDS], pp. 30, 88–89. |
| AC-BR-017 / BR-017 | Layout/claim/source provenance retained; cited anchor resolves to immutable version. | Reprocessing cannot overwrite old cited derivative; absent bbox allowed; non-PDF/invalid anchor contract awaits OQ-BR-011. | [DDS], pp. 31, 57. |
| AC-BR-018 / BR-018 | Safe authorized low-quality source remains viewable. | Low-quality material excluded from autonomous recommendations; quarantine is not treated as low-quality viewing permission. Threshold equality awaits OQ-BR-010. | [DDS], pp. 30–32. |
| AC-BR-019 / BR-019 | Mixed-permission search returns only permitted supported citations with required metadata. | Insufficient evidence returns `NO_SUPPORTED_EVIDENCE`; missing citations produce needs-review/unsupported, not fabricated publication. MCP `max_items >10` violates tool contract; lower/default NC. | `TST-009`; [DDS], pp. 34–36, 87, 89. |
| AC-BR-020 / BR-020 | Parallel generation with passed completeness/recall checks switches alias atomically. | Failed/incomplete checks do not authorize switch; failed index write preserves source metadata. Empty coverage denominator awaits OQ-BR-011. | [DDS], pp. 34, 49, 78. |
| AC-BR-021 / BR-021 | Revocation invalidates affected results before next query. | No forbidden evidence after revocation; soft-deleted source unavailable before physical removal; stale visibility invokes incident controls. | `T-08`, `TST-004`; [DDS], pp. 27–29, 51–53, 88–89. |
| AC-BR-022 / BR-022 | Approved compatible deployment used for governing run class. | Restricted material cannot fall back to unapproved deployment/region; lower-handling fallback prohibited. Missing class handling awaits OQ-BR-013. | `T-06`; [DDS], pp. 37, 62, 88. |
| AC-BR-023 / BR-023 | Valid versioned structured output passes required validation. | Unknown fields, invalid citations, control injection yield `MODEL_OUTPUT_INVALID`; no publish. Parse retry bound awaits OQ-BR-022. | `TST-005`; [DDS], pp. 38–39, 89. |
| AC-BR-024 / BR-024 | All resolved token/queue/capacity thresholds satisfy admission. | Any failed threshold produces `429` plus `Retry-After`; saved case remains available. Threshold equality awaits OQ-BR-014. | [DDS], p. 69. |
| AC-BR-025 / BR-025 | Run reserves input/output budgets and attributes actual usage. | Exhaustion terminates current run without model/data-class switch; retry/failed-call billing and equality await OQ-BR-014. | [DDS], pp. 38, 65, 85. |
| AC-BR-026 / BR-026 | Allowed depth/calls, explicit dependencies, durable plan/checkpoints. | Depth above eight or invocation above sixteen cannot execute. Exactly eight/sixteen is within maxima but must satisfy other guards. Missing approval/wait/time accounting awaits OQ-BR-015. | `T-10`; [DDS], pp. 40–42, 49, 88. |
| AC-BR-027 / BR-027 | Valid pinned capability and separate authorization dispatches permitted operation. | Arbitrary MCP denied before dispatch; denied action not replaced equivalently; consequential write lacks permission without human authorization. | `TST-014`; [DDS], pp. 41–42, 87, 89. |
| AC-BR-028 / BR-028 | Same retained normalized inputs/rule version reproduce deterministic outcome. | LLM tag cannot change outcome; no invented confidence/financial threshold or rule-order default. | [DDS], pp. 44, 85. |
| AC-BR-029 / BR-029 | Eligible independent Reviewer satisfies pool/minimum role/SoD. | High-risk author cannot self-approve; unapproved high-risk run cannot publish. Global self-approval scope awaits explicit resolution. | [DDS], pp. 11–13, 45, 85. |
| AC-BR-030 / BR-030 | Exact candidate/context inspectable; valid decision records required evidence. | Buttons disabled for incomplete required fields; wrong/prior hash rejected and audited; no invented click-count gate. | `T-03`, `TST-006`; [DDS], pp. 45, 57–58, 83, 88–89. |
| AC-BR-031 / BR-031 | Expiry routes reassign/escalate and retains evidence. | No implicit approval; exact deadline equality and decision/expiry race await OQ-BR-019. | `TST-010`; [DDS], pp. 45, 89. |
| AC-BR-032 / BR-032 | Satisfied exact gate/pointer commit atomically after current validation. | Changed artifact or revoked permission cannot publish; interrupted transaction cannot leave published pointer without satisfied gate. | [DDS], pp. 12–13, 45–46, 52. |
| AC-BR-033 / BR-033 | Resolved authorized override meets all three requirements; rework creates new revision. | Missing elevated role/secondary reviewer/audited reason blocks override; denial never retroactively approved. | [DDS], pp. 46, 75. |
| AC-BR-034 / BR-034 | Admin sync on provisioned connector advertises capabilities. | Missing support produces explicit lower-trust warning; revoked queued credential yields `CONNECTOR_REAUTH_REQUIRED` without token leak. | [DDS], pp. 27, 78, 83. |
| AC-BR-035 / BR-035 | Preceding durable outcomes permit resolved cursor advancement. | No advancement past nondurable outcome; bounded malformed record quarantines with ledger exception; no-change rule NC. | [DDS], pp. 28–29. |
| AC-BR-036 / BR-036 | Transient read retry bounded; provider instruction/quota/fairness honored. | Validation/permission failure not transient-retried; replay missing reason/dry-run/scope cannot proceed; preserved event identity/provenance. | `TST-008`; [DDS], pp. 28–29, 42, 49–50, 89–90. |
| AC-BR-037 / BR-037 | Authorized redacted append-only evidence available with safe correlation. | Historical audit/decision edits rejected; traces/errors/provider requests lack out-of-scope secrets/documents; PII redaction follows resolved policy. | `T-05/T-09`; [DDS], pp. 62–66, 84, 88. |
| AC-BR-038 / BR-038 | Eligible closed no-hold selection purges only permitted inventory. | Open/ineligible/held cases not purged by case-retention rule; distinct diagnostic/audit policies; age equality/all-held status NC. | `TST-013`; [DDS], pp. 26, 66, 89–90. |
| AC-BR-039 / BR-039 | Independently verified Admin/approver checks satisfy exit admission. | Single Admin or repeated same-person evidence cannot bypass two-person control. | `T-11`; [DDS], pp. 78, 83, 88. |
| AC-BR-040 / BR-040 | Package includes metadata/approved artifacts/source references/audit manifests/checksums. | Secrets/internal prompts absent; no inferred raw-source/draft export; empty/partial package rules NC. | [DDS], p. 79. |
| AC-BR-041 / BR-041 | Eligible deletion targets tombstoned/removed/receipted; verification event idempotent. | Held records retained/receipted; no false complete erasure; access request not automatically treated as deletion. | `TST-013`; [DDS], pp. 80, 85, 87, 89. |
| AC-BR-042 / BR-042 | Idempotent setup creates required resources; historical batches keep stable IDs/receipts. | Incomplete provisioning blocks sync; empty queue alone does not establish readiness; empty window/coverage thresholds NC. | [DDS], p. 78. |
| AC-BR-043 / BR-043 | Daily outputs retain distinct category/cost-center/deployment attribution. | Replay cannot justify duplicate accepted accounting writes; day-end inclusion, late adjustment, zero usage, rounding/forecast tests wait for OQ-BR-026. | [DDS], pp. 65, 68, 85. |
| AC-BR-044 / BR-044 | Safe manual/evidence work continues; lexical-only flag visible. | No degraded ACL/approval bypass; suspected leak search not reenabled before negative tests pass. | [DDS], pp. 68–70, 79–90. |
| AC-BR-045 / BR-045 | Server-state refresh and retained scoped SSE reconstruct actual progress; keyboard case opening works. | No disconnected/accepted-only state shown as published; no private backfill; visible focus/accessibility; cursor gap NC. | `TST-011`; [DDS], pp. 55, 57–59, 89. |
| AC-BR-046 / BR-046 | Defined measurements preserve separate API/search/model targets; actionable alert category. | Spend anomaly is not automatically paging; search at 1.5 s fails stated “under” numerical target; case at 300 ms awaits wording resolution. | [DDS], pp. 12, 19, 64–65, 79. |
| AC-BR-047 / BR-047 | Incident-controlled recovery meets inclusive RPO/RTO limits and consistency. | Primary-only writes maintained; safety failure not accepted despite timing pass; uncontrolled snapshot restore prohibited. | `TST-012`; [DDS], pp. 19, 69–70, 89. |
| AC-BR-048 / BR-048 | Verified build, compatibility/backfill/drainage, sign-off, reconstructible release. | Incompatible field deletion blocked; regression rolls back traffic, not automatic DB down-migration; production data absent from development. | [DDS], pp. 19–20, 52, 55, 71–73. |
| AC-BR-049 / BR-049 | Frozen evaluated evidence meets all resolved numerical/statistical/safety gates. | Critical failure, low confidence, poisoned fixtures, or regressed safety blocks release regardless of score; exact `0.97/0.02/1.00` meets only relevant numeric condition. | `T-12`, `TST-016`; [DDS], pp. 74–76, 88–89. |
| AC-BR-050 / BR-050 | Approved revision/change preserves impact/test links and dated selection evidence. | Revised invariant without negative-test link fails acceptance; no informal proposal promoted to approved configuration. | [DDS], pp. 8–10, 90. |

## Consistency and Open Questions

### Conflicts and Required Amendments

No preceding specification is rewritten by this document. Resolution must produce controlled amendments to affected earlier identifiers and this file.

| Conflict ID | Source evidence and issue | Affected identifiers | Required resolution/amendment |
|---|---|---|---|
| CON-BR-001 | `POST /v1/runs` versus `POST /v1/cases/{caseId}/runs`. [DDS], pp. 15–17 versus pp. 12, 40–42, 83. | BR-024/026; API-011/012; BAT-007; `CON-SCR-004`, `CON-API-001`, `CON-BAT-002`. | Resolve canonical/alternate launch and case-revision binding; do not silently choose endpoint. |
| CON-BR-002 | Missing approval terminates run, but `AWAITING_REVIEW` is valid; recoverable timeout absent from catalog. [DDS], pp. 12, 41, 45, 49, 82, 90. | BR-026/031/032; `CON-SCR-005`, `CON-API-002`, `CON-DAT-012`, `CON-BAT-003`. | Separate valid waiting, failure, execution timeout, and reviewer expiry; define state/accounting without inventing one. |
| CON-BR-003 | Close exists but explicit transition to `CLOSED` and reopening guards are incomplete. [DDS], pp. 24–26. | BR-014/015; API-005; DAT-003/004/025; `CON-SCR-006`, `CON-API-003`, `CON-DAT-013`. | Complete closure/reopen roles, predecessor states, revisions, and responses while preserving lineage. |
| CON-BR-004 | Role aliases/relationships and Auditor evidence journey differ from API scopes. [DDS], pp. 11, 22, 27, 46, 50, 83. | BR-002/003/029/034/039; preceding role conflicts. | Explicit role/action/attribute matrix and redacted Auditor evidence path; no inferred Admin/Auditor privilege. |
| CON-BR-005 | Explicit high-risk self-approval prohibition versus broader `no self approval` and example false setting. [DDS], pp. 11, 85, 90. | BR-029/030; `CON-SCR-009`, `CON-API-005`, `CON-DAT-014`. | Confirm global scope and any approved exceptions without weakening high-risk prohibition. |
| CON-BR-006 | Workspace settings associated with case PATCH. [DDS], p. 24, §6.1.1. | BR-007/010; SCR-007; API-GAP-002; DAT-002; preceding settings conflicts. | Supply actual settings APIs/schema; do not bind workspace policy to case PATCH solely from association. |
| CON-BR-007 | Lower-trust missing connector capabilities coexist with mandatory ACL enforcement/revocation before next retrieval. [DDS], pp. 21–23, 27–29. | BR-021/034/035; BAT-002/006; preceding connector-trust conflicts. | Define safe capability restrictions; missing ACL capability cannot authorize a leak or delayed revocation. |
| CON-BR-008 | Common event envelope omits actor/correlation carriers required at durable boundaries; chapter GET/event associations are imprecise. [DDS], pp. 48–50, 57–59, 87. | BR-009/010/045; API-COM-006; DAT-EVT fields; BAT-010; preceding event conflicts. | Complete schemas/triggers/attribution; do not make all reads create jobs or mutations. |
| CON-BR-009 | A2A requires declared input/output schemas; example omits output declaration and uses placeholder tenant/case IDs. [DDS], pp. 41, 51, 87. | BR-027; API-046; DAT-034; BAT-007. | Formalize carriers/types and decline protocol without converting sample placeholders into production IDs. |
| CON-BR-010 | Selected schemas omit supported logical fields; generic register calls mutable case an immutable derivative. [DDS], pp. 13, 24–26, 45, 85–86. | BR-004/011/014/015/030; DAT-003/004/012/025; `CON-API-011`, `CON-DAT-001/002/008`. | Complete schemas; distinguish current mutable state from immutable revisions/artifacts/decisions. |
| CON-BR-011 | UUIDv7 identity baseline versus fingerprint-plus-pipeline derivative IDs; distinct hash/digest scopes. [DDS], pp. 31, 35, 44–45, 51, 53, 85. | BR-004/017/019/030; DAT-COM-004; preceding identity/digest conflicts. | Define identities, canonical inputs, hash algorithms/encodings, and reference mapping; no universal hash-to-UUID conversion. |
| CON-BR-012 | Per-sync-run cursor/error history versus connector-keyed selected cursor fields. [DDS], pp. 28–29, 85. | BR-035; DAT-015/021; BAT-002; `CON-DAT-011`, `CON-BAT-007`. | Define cursor ownership, run history, exception durability, and concurrent sync fencing. |
| CON-BR-013 | Closed immutable citation lineage versus source/deletion/retention/hold behavior. [DDS], pp. 26, 51, 62, 80. | BR-015/021/038/041; DAT-025/029; `CON-DAT-019`, `CON-BAT-010`. | Define retained evidence/reference scope and authorized historical access without bypassing purge/holds or substituting latest source. |
| CON-BR-014 | Diagnostic/audit defaults and Appendix F configuration coexist with explicit corporate/provider selections still open. [DDS], pp. 66, 90. | BR-010/022/025/038/043/047; preceding configuration conflicts. | Approve actual values and precedence through dated decisions; preserve example status. |
| CON-BR-015 | Case P95 says “within” and “under” 300 ms. [DDS], pp. 12, 65. | BR-046; AC-BR-046; OQ-API-033; OQ-SCR-031. | Resolve strict equality and measurement boundary before threshold assertion. |
| CON-BR-016 | Error prose says snake-case; examples use uppercase literals. [DDS], pp. 54, 84, 89. | BR-006/007/008/023/034; preceding error conflicts. | Preserve existing literals; resolve canonical casing and per-operation mappings. |
| CON-BR-017 | Artifact/run/review/case status vocabulary differs from mixed illustrated list labels. [DDS], pp. 7, 14, 57, 82. | BR-014/026/031/045; SCR-COM-005; DAT-CODE systems. | Explicit aggregate-to-display mapping; do not expand `cases.status` from illustrations. |
| CON-BR-018 | Daily rollups and monthly SLO measurement do not define financial closing/reset schedules. [DDS], pp. 65, 68–69. | BR-025/043/046; BAT-016; DAT-030. | Define reporting periods, quota windows, corrections, and scheduler independently; no inferred midnight/month-end close. |
| CON-BR-019 | Export/delete approval invariant is defined, but exact independence/binding/expiry protocol is missing. [DDS], pp. 78, 83, 88. | BR-039/040/041; API-025/026; BAT-020/021. | Formal independent authorization protocol; client-supplied actor references alone are insufficient. |
| CON-BR-020 | Earlier files reference business rules as future work. | Earlier handoff sections; all mapped BR requirements. | Controlled amendments may link to `05_business_rules.md`; unresolved earlier questions remain unresolved. No prior file is rewritten here. |

### Open-Decision Register

All entries are **Needs confirmation**. No decision, owner, deadline, or approval is assigned.

| Open ID | Affected rules | Missing decision/contract | Preceding linkage and source evidence |
|---|---|---|---|
| <a id="oq-br-001"></a>OQ-BR-001 | BR-002/003/029/034/039 | Authentication/session/token boundaries; complete role/action/resource matrix; owner/member/admin/operator/elevated aliases; Auditor evidence path; authorship/independence. | [`01_screen_functions.md`](01_screen_functions.md): OQ-SCR-002/003; [`02_api.md`](02_api.md): OQ-API-001/002/016; [`03_data.md`](03_data.md): OQ-DAT-017; [`04_batch_functions.md`](04_batch_functions.md): OQ-BAT-003. [DDS], pp. 11, 18–23, 83–90. |
| <a id="oq-br-002"></a>OQ-BR-002 | BR-004/006/011 | Full request/data types, lengths/requiredness/defaults, ID/business-number/slug contracts, error casing/details/status mappings, missing-precondition outcomes. | OQ-SCR-004/006/029; OQ-API-003/007/032; OQ-DAT-002/003/004/006; OQ-BAT-002/009. [DDS], pp. 24–25, 54–56, 84–86. |
| <a id="oq-br-003"></a>OQ-BR-003 | BR-004/007/008/009 | RLS/write/session controls, tenant-reference mechanism, revisions/patch format, locks/isolation, idempotency scope/fingerprint/TTL/pending replay and concurrency. | OQ-API-004/005; OQ-DAT-013/014; OQ-BAT-004/005/006. [DDS], pp. 22, 25, 48–54, 86. |
| <a id="oq-br-004"></a>OQ-BR-004 | BR-010/013/022/028/031/038 | Configuration precedence/activation/effective periods; in-flight task/run/job version selection; changed calendar/classification/retention behavior. | OQ-SCR-020; OQ-API-020; OQ-DAT-005/021; OQ-BAT-014/015/016. [DDS], pp. 24–25, 44, 71–73, 90. Effective-period mechanics absent. |
| <a id="oq-br-005"></a>OQ-BR-005 | BR-011 | Classification inputs/version, labels/confidence/provenance, reason vocabulary, correction permission/API, attachment dependencies and stale-result races. | OQ-SCR-007; OQ-API-008; DAT-020; OQ-BAT-010. [DDS], p. 12. |
| <a id="oq-br-006"></a>OQ-BR-006 | BR-012 | Impact/urgency vocabulary, priority formula/matrix/order/ties/rounding, overrides, missing values and recalculation. | OQ-SCR-008; OQ-API-007; OQ-DAT-006. [DDS], p. 25, §6.3.1. |
| <a id="oq-br-007"></a>OQ-BR-007 | BR-013 | Contract durations/start/pause/reopen conditions, business calendar/timezone/DST/holiday rules, equality/rounding and deadline changes. | OQ-SCR-008/031; OQ-API-007; OQ-DAT-005/024. [DDS], pp. 25, 54, 59. |
| <a id="oq-br-008"></a>OQ-BR-008 | BR-014/015/033 | Complete transition/closure/reopen guards, roles, predecessor/target states, approved-answer absence, revision/snapshot/repeated-close/rework contracts. | OQ-SCR-018; OQ-API-007/012; OQ-DAT-007/015. [DDS], pp. 24–26, 46. |
| <a id="oq-br-009"></a>OQ-BR-009 | BR-016/017 | Exact file allowlist/transport/size unit/equality/decompression/parser constraints, OCR opt-in/default, corruption/encryption, safe quarantine viewing/remediation. | OQ-SCR-009; OQ-API-009; OQ-DAT-008/010; OQ-BAT-012. [DDS], pp. 10, 30–32. |
| <a id="oq-br-010"></a>OQ-BR-010 | BR-018/019/028 | Quality formulas/scales/denominators/thresholds/equality/missing flags, autonomous-use definition, indexed `READY` and manual reviewed-use treatment. | OQ-API-009/011; OQ-DAT-010/011; OQ-BAT-012/013. [DDS], pp. 32, 36, 44. |
| <a id="oq-br-011"></a>OQ-BR-011 | BR-017/019/020 | Citation/anchor/hash/identity/source-access schemas; query/RRF/rerank/diversity/token budgets/ties; evidence sufficiency/conflicts; index coverage/recall/checks/empty corpus. | OQ-SCR-010/011; OQ-API-010/011/028; OQ-DAT-008/009/011; OQ-BAT-013. [DDS], pp. 31, 34–36, 52, 57, 78, 87, 90. |
| <a id="oq-br-012"></a>OQ-BR-012 | BR-021/034/044 | ACL/membership/source-change propagation, in-flight races, cache-key/digest scopes/TTL, signed-URL revocation, safe missing-ACL capability restrictions. | OQ-API-019; OQ-DAT-012/017/019; OQ-BAT-011/013. [DDS], pp. 21–23, 27–29, 53, 79. |
| <a id="oq-br-013"></a>OQ-BR-013 | BR-022/023/037 | Maximum-class order/material scope/defaults/inheritance, route compatibility/context constraints, PII tags/redaction, prompt/output/injection protocols. | OQ-SCR-030; OQ-API-020/027/034; OQ-DAT-017/021/025; OQ-BAT-012/014/024. [DDS], pp. 37–39, 62–63, 90. |
| <a id="oq-br-014"></a>OQ-BR-014 | BR-024/025/043 | Admission token/queue/capacity thresholds/units/equality, reservations and quota window/reset, provider use/count/billing/retry reconciliation. | OQ-API-022/033; OQ-DAT-020; OQ-BAT-018/026. [DDS], pp. 38, 65, 68–69, 85. |
| <a id="oq-br-015"></a>OQ-BR-015 | BR-023/026/031 | Canonical run launch/revision, DAG depth/call counting, retries/invalid-plan bounds, waiting/missing approval, deadline/timeout pause/recoverable states. | OQ-SCR-012/013; OQ-API-012–014; OQ-DAT-015; OQ-BAT-014. [DDS], pp. 12–17, 40–42, 49, 82, 90. |
| <a id="oq-br-016"></a>OQ-BR-016 | BR-001/005/027 | Allowed business-tool actions, consequential taxonomy/grants/human authorization, MCP requiredness/lower bounds/Citation, A2A output/decline/transport/signatures. | OQ-API-028; OQ-DAT-024; OQ-BAT-014. [DDS], pp. 41–42, 87. |
| <a id="oq-br-017"></a>OQ-BR-017 | BR-028/029/032 | Complete normalized policy decision matrix, high-risk/high-impact/financial categories, confidence bands, missing inputs, rule combination/priority and effective version. | OQ-SCR-008/014/020; OQ-API-015/017/020; OQ-DAT-021; OQ-BAT-015. [DDS], pp. 44–46, 90. |
| <a id="oq-br-018"></a>OQ-BR-018 | BR-030/032 | Required review fields/enum/rationale/annotations, task/approval identity, exact hash canonicalization/binding, conflicting or duplicate decisions. | OQ-SCR-014; OQ-API-015; OQ-DAT-016; OQ-BAT-015. [DDS], pp. 45, 58, 83, 85. |
| <a id="oq-br-019"></a>OQ-BR-019 | BR-029/031 | Pools/minimum role/global self-approval scope, SLA clocks/units/start/equality, eligible states, late/expiry races, reassignment/escalation/multi-reviewer rules. | OQ-SCR-003/015; OQ-API-016; OQ-DAT-016; OQ-BAT-015. [DDS], pp. 11, 45, 82, 85, 90. |
| <a id="oq-br-020"></a>OQ-BR-020 | BR-032/033 | Automatic publication trigger/control/API, gate/decision lifetime/current rechecks, elevated override role/secondary reviewer/reason, rework linkage. | OQ-SCR-016/017; OQ-API-017/018; OQ-DAT-015/016/021; OQ-BAT-015. [DDS], pp. 45–46, 58. |
| <a id="oq-br-021"></a>OQ-BR-021 | BR-034/035 | Providers/capabilities/grants, trust restrictions, credential revoke/reauth, source IDs/cursor history/order/expiry/concurrency/bounds/quarantine/empty delta. | OQ-SCR-019; OQ-API-019/034; OQ-DAT-019; OQ-BAT-011. [DDS], pp. 27–29, 85, 90. |
| <a id="oq-br-022"></a>OQ-BR-022 | BR-009/023/036 | Event triggers/schema/signature/actor/correlation, retries/backoff/circuits/deadlines/worker loss, replay scopes/provenance, ledger retention/no-input outcome, webhooks. | OQ-API-004/027–029/035; OQ-DAT-013/024; OQ-BAT-005–009/025. [DDS], pp. 48–50, 55, 87, 90. |
| <a id="oq-br-023"></a>OQ-BR-023 | BR-015/037/038/041 | Audit/hash/export/redaction, retention durations/clocks/precedence/holds/races, deletion inventory/receipts, retained lineage/actors/backups, access-request semantics. | OQ-SCR-021/025/026/030; OQ-API-021/024/025/034; OQ-DAT-007/016–018/023; OQ-BAT-016/017/023/024. [DDS], pp. 26, 62–66, 78–80, 85, 89–90. |
| <a id="oq-br-024"></a>OQ-BR-024 | BR-039/040/041 | Independent approver protocol/binding/validity, execution rechecks, export snapshot/content/format/checksum/lifetime/status/download, empty/partial exit operations. | OQ-SCR-025; OQ-API-024; OQ-DAT-018/023; OQ-BAT-016/021. [DDS], pp. 78–80, 83, 88–89. |
| <a id="oq-br-025"></a>OQ-BR-025 | BR-042 | Provisioning launch/role/order/checkpoint/completeness/compensation and changed-config rerun; historical windows/overlap/receipts/readiness. | OQ-SCR-026; OQ-API-025; OQ-DAT-018/019; OQ-BAT-020. [DDS], p. 78. |
| <a id="oq-br-026"></a>OQ-BR-026 | BR-025/043 | Period/day timezone/boundaries, cost/forecast/trend formulas, currency/precision/rounding/allocation, late corrections/zero input, quotas and any additional period-end processes/schedules. | OQ-SCR-023; OQ-API-022; OQ-DAT-020; OQ-BAT-001/009/018. [DDS], pp. 38, 65, 68–69. |
| <a id="oq-br-027"></a>OQ-BR-027 | BR-045 | Status/summary/formula mapping, screen aliases/routes/primary actions, SSE offsets/history/gaps, source navigation, detailed accessibility/locale/notification choices. | OQ-SCR-001/006/013/022/028/031; OQ-API-014/031/036; OQ-DAT-024/026; OQ-BAT-008. [DDS], pp. 7, 55, 57–59, 82. |
| <a id="oq-br-028"></a>OQ-BR-028 | BR-044/046/047 | Incident/degraded protocols, availability/burn/latency calculations, thresholds/routes/actual assignments, recovery fencing/time measurement/backups/drills and capacity realization. | OQ-SCR-028/031; OQ-API-031/033; OQ-DAT-020/025/026; OQ-BAT-004/008/023/026. [DDS], pp. 19, 64–70, 79, 90. |
| <a id="oq-br-029"></a>OQ-BR-029 | BR-048/049/050 | Migration/release/build/sign-off/canary calculations; metric denominators/rounding/confidence/domains; signed fixtures/tests; individual SEC requirements; governance impact/revision approval. | OQ-SCR-024/027; OQ-API-023/026/027/030; OQ-DAT-022; OQ-BAT-019/022. [DDS], pp. 8–10, 52, 55, 71–76, 88–89. |
| <a id="oq-br-030"></a>OQ-BR-030 | BR-010/022/037/038/047/048/050 | Approved cloud/region/search/identity/model deployments/corporate retention/connector permissions and encryption-key isolation versus rotation throughput. | OQ-SCR-030; OQ-API-034; OQ-DAT-025; OQ-BAT-024/026. [DDS], p. 10, §1.3.2; p. 90, §F.2. |

### Proposal Status

| Proposal | Status and effect on business rules |
|---|---|
| `P-SCR-001`–`P-SCR-003` | Remain unapproved screen alias/hierarchy, new-case mode, and field/control placement proposals. They do not determine rule permissions, persistence, or calculations. |
| `P-API-001` | Remains unapproved `Authorization: Bearer` token carrier. It does not select against optional BFF cookies or define job/service identity transport. |
| `P-API-002` | Remains unapproved JSON mapping for case/run/search/review examples. It does not supply required business fields or formulas. |
| New business-rule design proposals | None selected. Missing priority matrices, SLA durations, confidence thresholds, rule-combination order, retention schedules, and reporting formulas remain open decisions. |

### Dependencies and Later Handoffs

| Specification/dependency | Required handoff |
|---|---|
| [`01_screen_functions.md`](01_screen_functions.md) | Preserve screen/action/field identifiers. Apply confirmed BR constraints to existing controls and displays; do not approve proposed routes, fields, summaries, or new operational screens. |
| [`02_api.md`](02_api.md) | Preserve interface/error/event identifiers. Resolve missing schemas, roles, preconditions, publication/override, correction, and exit protocols through controlled amendments. |
| [`03_data.md`](03_data.md) | Preserve storage-versus-wire distinctions, immutable history, exact artifact/version relationships, normalized inputs, tenant predicates, and all unresolved physical schemas. |
| [`04_batch_functions.md`](04_batch_functions.md) | Preserve logical BAT functions, durable checkpoints, fairness/retries, eligibility, receipts, and schedule gaps. BR rules do not select executables, queues, timers, batch sizes, or no-input statuses. |
| Exception handling specification | **To be defined in a later stage.** Carry fail-closed/permanent-transient distinctions, stale/hash conflicts, unsupported evidence, quarantine, expiry, timeout, partial exit results, safe errors, and retry/replay boundaries. Filename is not supplied. |
| Security/nonfunctional and remaining operational specifications | **To be defined in a later stage.** Complete role/grant/signature/PII/source-access controls, SLO measurement, provider approval, incident/recovery/release protocols, and scheduler realization. Do not presume their future decisions here. |
| Stage 8 architecture-decision consolidation | **To be defined in a later stage.** `08_architecture_decision.md` must consolidate unresolved items only from completed Markdown specifications, linking to `05_business_rules.md` BR/OQ/CON identifiers and affected earlier filenames/identifiers. No decision, owner, deadline, or approval is invented by this document. |
