# 5. Business Rules

## Rule Inventory and Scope

### BR-001 — Authority and interpretation

**Confirmed.** This Stage 5 specification, `05_business_rules.md`, applies to OrionDesk AI, `OD-AI-DDS-001`, `R1.0 / revision 1.3`, a controlled fictional reference architecture. It consolidates supplied chapter judgments, not a new inspection of attachments. The candidate remains provisional pending evidence review.

**Confirmed** identifies reference-system obligations; **Needs confirmation** identifies missing implementation contracts or unresolved source conflicts. No new **Proposal** is selected. All numbers retain the source qualification: “All numbers are design assumptions, not measured production performance.” Figures are normative boundary illustrations, not generated implementation artifacts. Fictional identities, UI metrics, grants and configuration values are not production defaults or approvals. Contents are navigation, not independent evidence of behavior. [1794353355-OrionDesk_AI_Detailed_Design_Specification.pdf, pp.1–2, cover/Document Map; `business_rules:r1:c1:f1`, `business_rules:r1:c1:f3`, `business_rules:r1:c2:f2`, `business_rules:r1:c2:f3`]

`BR-*` identifiers are specification-assigned. Preserve existing identifiers in [01_screen_functions.md](01_screen_functions.md), [02_api.md](02_api.md), [03_data.md](03_data.md) and [04_batch_functions.md](04_batch_functions.md). These links provide application traceability, not independent evidence. API paths are not browser routes; BAT responsibilities are not approved executable decomposition; selected DAT fields are not exhaustive schemas.

### Inventory

All rules inherit BR-001. Actors below indicate supported activity responsibilities, not sufficient authorization. Unless explicitly supplied, executing identity, permission predicate, formula, rounding, units, threshold, schedule, effective period and error/recovery contract are **Needs confirmation**.

| Rule | Name and purpose | Actors / applicable targets | Timing and evidence in the original PDF |
|---|---|---|---|
| BR-002 | Authority boundaries and prohibited operations | All principals, agents, browsers, model/tool integrations | Every invocation; p.7 safety rule, p.9 §1.2; `business_rules:r1:c4:f5`, `business_rules:r1:c7:f1` |
| BR-003 | Authentication, tenancy and resource authorization | All requests/jobs; Analyst, Reviewer, Admin, Auditor, Service | Edge, transaction, retrieval, dispatch, publication; pp.21–23 §5; `business_rules:r1:c29:f1`, `business_rules:r1:c31:f1`, `business_rules:r1:c32:f2` |
| BR-004 | Case classification, revisions and lifecycle | Analyst intake, authorized case mutators | Creation, correction, update, close/reopen; pp.12,24–26; `business_rules:r1:c13:f1`, `business_rules:r1:c37:f1`, `business_rules:r1:c37:f4` |
| BR-005 | Priority, deadlines and configuration | Case domain, workspace policy administrators | Classification/update and calendar calculations; pp.24–25 §6.1/6.3; `business_rules:r1:c36:f1`, `business_rules:r1:c38:f1`, `business_rules:r1:c38:f2` |
| BR-006 | Safe ingestion and evidence provenance | Analyst uploads, Ingestion, authorized viewers | Before parse/index/autonomous use/citation; pp.30–32 §8; `business_rules:r1:c48:f1`, `business_rules:r1:c48:f5`, `business_rules:r1:c50:f7` |
| BR-007 | Connector trust, durable progress and revocation | Admin sync, operators, connector workers | Admission, batch checkpoint, credential/ACL change; pp.27–29 §7; `business_rules:r1:c42:f1`, `business_rules:r1:c43:f1`, `business_rules:r1:c44:f7` |
| BR-008 | Permitted retrieval and unsupported evidence | Retrieval, Research, authorized search callers | Before generation release/display/publication; pp.34–36 §9; `business_rules:r1:c53:f2`, `business_rules:r1:c56:f5` |
| BR-009 | Model routing, trust and budget | Gateway, Orchestrator, workspace policy | Admission, provider selection, prompt/output processing; pp.37–39 §10; `business_rules:r1:c60:f1`, `business_rules:r1:c62:f2` |
| BR-010 | Bounded plans and independent tool authority | Triage/Research/Draft, deterministic Policy Evaluator | Plan persistence and each dispatch; pp.40–42 §11/C.2 p.87; `business_rules:r1:c66:f5`, `business_rules:r1:c67:f1`, `business_rules:r1:c139:f10` |
| BR-011 | Deterministic risk decision | Policy Service, not model authority | Policy evaluation; pp.44–45 §12.1/p.62 classification; `business_rules:r1:c72:f1`, `business_rules:r1:c72:f2`, `business_rules:r1:c103:f1` |
| BR-012 | Eligible, exact-artifact human review | Policy-selected Reviewer; controlled override actors | Assignment, decision, expiry, rework; pp.11,45–46,58,85; `business_rules:r1:c12:f2`, `business_rules:r1:c73:f1`, `business_rules:r1:c138:f6` |
| BR-013 | Distinct publication gate | Publication invoker unconfirmed | Immediately before atomic final commit; pp.12,45–46,87; `business_rules:r1:c13:f5`, `business_rules:r1:c74:f1`, `business_rules:r1:c139:f5` |
| BR-014 | Retry-safe transactions, events and replay | Domain services, consumers, authorized operators | Validation, commit, delivery, replay; pp.17,48–56; `business_rules:r1:c20:f8`, `business_rules:r1:c80:f1`, `business_rules:r1:c80:f7` |
| BR-015 | Privacy, audit and key lifecycle | All integrations, Auditor, operators | Every disclosure/diagnostic; rotation/retention policies | pp.21,52,62–64,84; `business_rules:r1:c30:f6`, `business_rules:r1:c104:f1`, `business_rules:r1:c104:f8`, `business_rules:r1:c137:f22` |
| BR-016 | Closure lineage, retention and controlled exit | Authorized closer; Admin + approver; Retention Worker | Close, eligible purge, export/delete | pp.26,51,66,78–80,88–89; `business_rules:r1:c38:f5`, `business_rules:r1:c131:f1`, `business_rules:r1:c141:f13` |
| BR-017 | Daily usage and period calculations | Admin observes; rollup executor unconfirmed | Daily report granularity; cutoff/schedule open | pp.65–66/83; `business_rules:r1:c110:f1`, `business_rules:r1:c137:f17` |
| BR-018 | Admission, degradation and recovery | Gateway/workers, operators, incident command | Load admission, outage, restore | pp.19,65,68–70,79–90; `business_rules:r1:c115:f1`, `business_rules:r1:c116:f1`, `business_rules:r1:c133:f1` |
| BR-019 | Safe and accessible observation | All eight screens; eligible reviewers | Rendering, stream reconnect, refresh, interaction | pp.55,57–59; `business_rules:r1:c91:f1`, `business_rules:r1:c97:f6`, `business_rules:r1:c98:f6` |
| BR-020 | Governance, compatible release and verification gates | Engineering, Security, SRE, security-control owner | Change/release/reevaluation | pp.8–10,71–76,88–90; `business_rules:r1:c6:f5`, `business_rules:r1:c122:f1`, `business_rules:r1:c140:f15` |

## Decisions, Calculations, and State Transitions

### BR-002–003 — Authority and access

**Confirmed.** “Untrusted retrieved documents and LLM responses cannot authorize tools, change tenant scope, alter approvals or bypass the versioned deterministic policy engine.” Browser-supplied arbitrary tool definitions are prohibited. Source/model content remains data, including hostile instructions, recursive hints and displayed capability grants. Discovery, registration, schema validity and relevance confer no permission. [PDF p.7; `business_rules:r1:c4:f2`, `business_rules:r1:c4:f5`; pp.40–42,87; `business_rules:r1:c65:f2`, `business_rules:r1:c68:f7`, `business_rules:r1:c139:f11`]

| Condition | Required decision / result | Qualification |
|---|---|---|
| Authenticated request | Bind principal and tenant; evaluate role, tenant, workspace membership, case sensitivity, source ACL, action and separation | Role/screen visibility alone insufficient |
| Interactive session | Authorization-code flow with PKCE; token issuer/audience/expiry/subject/tenant concepts | Reject unexpected algorithms and missing tenancy; exact values/lifetimes open |
| Browser refresh credential | No long-lived refresh token in local storage | Secure `HttpOnly`, `SameSite` BFF cookie is optional, not selected |
| Domain access | Re-evaluate attributes within transaction; tenant context/RLS; every storage predicate contains tenant | Pool context reset after **every transaction**; additional workspace membership FK **OR** controlled-write enforcement mandatory, choice open |
| Background job | Signed envelope with immutable tenant identity | Whole job and permissions are not frozen |
| Foreign resource substitution | Absent-ID not-found response class, no private-existence disclosure | Foreign case test requires `404-equivalent non-disclosing`; universal body/status unspecified |
| Retrieved chunk | Originating ACL filter before text reaches model | Ranking and immutable version do not authorize |
| Permission change after search | Recompute publication authorization; reject stale evidence | Earlier search/review not continuing authority |

[PDF pp.21–23 §§5.1–5.3; `business_rules:r1:c30:f1`, `business_rules:r1:c30:f5`, `business_rules:r1:c31:f1`, `business_rules:r1:c31:f2`, `business_rules:r1:c32:f1`, `business_rules:r1:c32:f2`, `business_rules:r1:c32:f7`; pp.51,86,89; `business_rules:r1:c83:f2`, `business_rules:r1:c138:f14`, `business_rules:r1:c138:f15`, `business_rules:r1:c141:f3`]

**Out of scope:** physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing, agent administrative-cloud permissions and application-hosted GPU inference. Financial-impact evaluation and usage accounting are not themselves excluded. **Deferred:** active/active cross-region mutation, OCR beyond English and customer-managed weights. [PDF pp.9–10,19; `business_rules:r1:c7:f1`, `business_rules:r1:c8:f7`, `business_rules:r1:c25:f2`]

### BR-004–005 — Case rules and calculations

1. An authorized Analyst creates an idempotent case, reference `201`, beginning `NEW`.
2. Asynchronous classification attaches labels, confidences and provenance. Label correction requires a reason code; actor/catalog/intake completeness are **Needs confirmation**.
3. Case mutation submits `If-Match`. Conflicting revision returns `409 CASE_VERSION_CONFLICT` with current revision and unchanged business state.
4. Actor/request-fingerprint idempotency maps one outcome for **24 hours**. Same-key duplicate creation produces one case and identical response; changed-body reuse returns `409 IDEMPOTENCY_CONFLICT`. Window origin/expiry equality/fingerprint/concurrent admission remain open.
5. Apply role/revision/approval guards to supported transitions. Do not add missing closing/reopening edges.

| Source state | Supported destination | Condition / exception |
|---|---|---|
| NEW | TRIAGED | Applicable guards |
| TRIAGED | IN_PROGRESS | Applicable guards |
| IN_PROGRESS | PENDING_APPROVAL or RESOLVED | Branch guards undefined |
| PENDING_APPROVAL | RESOLVED or IN_PROGRESS | Branch guards undefined |
| CLOSED | Final, **unless explicitly reopened as a new revision** | Reopen actor/action/destination and transition into CLOSED undefined |

[PDF pp.12,24–26,82–84,89; `business_rules:r1:c13:f1`, `business_rules:r1:c36:f4`, `business_rules:r1:c37:f1`, `business_rules:r1:c37:f4`, `business_rules:r1:c37:f5`, `business_rules:r1:c137:f6`, `business_rules:r1:c137:f8`, `business_rules:r1:c141:f1`, `business_rules:r1:c141:f2`]

| Calculation / setting | Confirmed constraint | Needs confirmation beside implementation |
|---|---|---|
| Priority | Derive from explicit impact and urgency, never model output alone | Domains, formula, ties, units, rounding, precedence and whether model may contribute alongside inputs |
| Contractual deadline | Business calendar computes in workspace timezone | Start, duration, working hours, holidays, DST, rounding and calendar version |
| Breach prediction | Advisory; cannot alter contractual deadline | Prediction method/confidence/threshold |
| Workspace settings | Retention class, allowed models, credential references, approved tools and reviewer routing | Values and administrative permission/endpoint |
| Configuration change | Revision precondition plus durable audit | Conflict/activation/version selection |
| Configurable numeric threshold | Explicitly versioned policy | Effective periods, selection and reevaluation |

[PDF pp.24–25 §§6.1/6.3, p.9 §1.2.2; `business_rules:r1:c36:f1`, `business_rules:r1:c38:f1`, `business_rules:r1:c38:f2`, `business_rules:r1:c7:f6`]

Reference `cases` DDL has UUID keys, six status CHECK literals, `revision BIGINT NOT NULL DEFAULT 1`, `sensitivity TEXT NOT NULL DEFAULT 'INTERNAL'` and creation/update `TIMESTAMPTZ DEFAULT now()`. These are persistence declarations, not UI defaults, publication permissions or automatic update triggers. Append-only `case_revisions` is distinct from mutable case state. [PDF pp.85–86; `business_rules:r1:c138:f3`, `business_rules:r1:c138:f9`, `business_rules:r1:c138:f10`, `business_rules:r1:c138:f11`, `business_rules:r1:c138:f12`]

### BR-006–008 — Documents, synchronization and retrieval

| Prerequisite / condition | Required result | Open boundary |
|---|---|---|
| File admission | R1 PDF, DOCX, HTML, UTF-8 text; MIME signature/extension agreement; configurable **25 MB/file**; bomb protection | MIME literals, MB convention, cap equality and bomb threshold |
| Before parsing | Scan, disable macros, no embedded remote fetch | Scanner failure/remediation contract |
| Unsafe attachment | Quarantine, no indexing | ZIP/polyglot are hostile tests, not admitted formats |
| PDF extraction | Page/block bboxes, table row/column metadata, heading/reading order | Coordinate units/page basis/chunking method |
| OCR fallback | Opt-in and provenance-marked | Actor/control/trigger/marker; beyond-English deferred |
| Normalization | Remove transport artifacts, never rewrite claims; fingerprint + pipeline version immutable derivatives may coexist | Hash/serialization/reprocess/retention mechanics |
| Every chunk | Source URI/hash/page, optional bbox | Block bbox does not make chunk bbox mandatory |
| Generation citation | Resolvable stored anchor **AND** current access permission | Missing-anchor/error/recovery |
| Low extraction quality | Authorized document viewable, excluded autonomous recommendation | Empty-page/unknown-character/table-loss/language-confidence formulas/thresholds and index/state mapping |
| Missing connector capability | Explicit visible lower-trust warning | Safe restrictions for unsupported ACL/delete/delta; no ACL bypass |
| Revoked credential | Queued jobs fail `CONNECTOR_REAUTH_REQUIRED`, no token exposure | Already-running jobs/reauth timing |
| Sync progress | Cursor/high-watermark/error ledger; advance only after durable preceding outcomes | Atomicity, durable outcome catalog |
| Malformed item after bounded retries | Quarantine with reason/correlation/remediation; remaining batch **may** continue with ledger exception | Continue/stop choice and permanent-fault taxonomy; not poisoned-item success |
| Source deletion | Tombstone/scheduled index removal | Cleanup cadence open |
| Source ACL change | Invalidate cache before new results; revocation effective before next retrieval | During-search cancellation/release algorithm open; stale visibility is incident |
| Index rebuild | Parallel build, completeness/recall checks, atomic alias switch; database authoritative | Measures/thresholds/promotion arbitration |
| Failed index write | Keep accepted metadata; fingerprint reconciliation and outbox link repair | No unrestricted retry of permanent errors |

[PDF pp.27–36,49,88–89; `business_rules:r1:c42:f1`, `business_rules:r1:c42:f5`, `business_rules:r1:c43:f1`, `business_rules:r1:c43:f4`, `business_rules:r1:c43:f5`, `business_rules:r1:c44:f6`, `business_rules:r1:c44:f7`, `business_rules:r1:c48:f1`, `business_rules:r1:c48:f4`, `business_rules:r1:c48:f5`, `business_rules:r1:c49:f1`, `business_rules:r1:c49:f2`, `business_rules:r1:c49:f6`, `business_rules:r1:c50:f1`, `business_rules:r1:c50:f2`, `business_rules:r1:c50:f6`, `business_rules:r1:c50:f7`, `business_rules:r1:c54:f5`, `business_rules:r1:c79:f6`, `business_rules:r1:c140:f4`, `business_rules:r1:c141:f15`]

Retrieval uses scoped tenant/workspace/version/chunk/language/classification rows, normalized text and **1536-dimensional embeddings**. Form lexical and normalized vector queries; bounded candidate retrieval → reciprocal rank fusion → deterministic reranking → redundancy/source-diversity control, subject to model-token cap and ACL filtering. No RRF equation, constant, scoring tie rule or selected numeric candidate/token limit is supplied by this operative prose. Cache identity includes tenant, user-scope digest, ACL revision, query hash and index generation; authorization change purges before normal TTL and must satisfy the stronger next-retrieval rule. [PDF pp.34–36,53; `business_rules:r1:c54:f1`, `business_rules:r1:c55:f1`, `business_rules:r1:c55:f6`, `business_rules:r1:c86:f7`, `business_rules:r1:c86:f8`]

Every evidence item includes chunk ID, source title, document revision, page anchor and ACL digest; opaque citation identifiers are verified before display. Insufficient confidence **OR** quality returns `NO_SUPPORTED_EVIDENCE`, never fabricated context. Clarification **OR** human routing is permitted but unselected. Missing citations separately require needs-review **OR** unsupported outcome; do not silently choose a durable state. [PDF pp.35–36,89; `business_rules:r1:c56:f1`, `business_rules:r1:c56:f2`, `business_rules:r1:c56:f5`, `business_rules:r1:c56:f6`, `business_rules:r1:c141:f9`]

### BR-009–010 — Model, plan and tool decisions

1. Whitelist specific approved deployments by capability, region, handling class, context length, cost profile and evaluation approval, not provider brand.
2. Fallback requires approved equal-or-stronger handling; equal satisfies the stated comparison, weaker does not. Restricted content cannot enter unapproved region/deployment on outage. Exact handling order and other-class region mappings remain open.
3. Reserve run input/output tokens and account provider usage under workspace quota. Exhaustion terminates the current run without automatic model/data-class switching, including switching to evade quota.
4. Prompt uses fixed system rules, signed workflow, validated user input and delimited untrusted passages. Strip evidence tool directives; record injection indicators.
5. Request versioned JSON; bounded parsing retries reject unknown fields, invalid citations and control injection with `MODEL_OUTPUT_INVALID` and no publication. This is not a universal REST unknown-field rule.
6. Persist DAG plan revision before side effects; depth **8**, maximum **16** tool invocations, explicit dependencies and replayable checkpoints. Each workflow stage checkpoints before downstream dispatch.
7. Dispatch approved pinned MCP schema/validated arguments with scoped credentials. Separate capability authorization applies to external writes; mutable calls require idempotency; consequential mutable calls additionally require human authorization. A denied action cannot be replaced by an equivalent tool.
8. Triage/Research/Draft are bounded responsibilities. Policy Evaluator is deterministic, not an LLM agent.

[PDF pp.37–42,49,89; `business_rules:r1:c60:f1`, `business_rules:r1:c60:f2`, `business_rules:r1:c61:f1`, `business_rules:r1:c61:f4`, `business_rules:r1:c62:f1`, `business_rules:r1:c62:f2`, `business_rules:r1:c62:f7`, `business_rules:r1:c66:f1`, `business_rules:r1:c66:f5`, `business_rules:r1:c66:f6`, `business_rules:r1:c67:f1`, `business_rules:r1:c68:f6`, `business_rules:r1:c68:f7`, `business_rules:r1:c79:f1`, `business_rules:r1:c141:f5`]

| Tool contract | Exact declaration |
|---|---|
| Name | `knowledge.search@v1` |
| Input | `{query: string, case_id: uuid, max_items: int<=10}` |
| Output | `{evidence_set_id: uuid, citations: Citation[]}` |
| Authorization/effect | `read:permitted_documents`, tenant-scoped; read-only; no arbitrary URLs/filesystem |

`max_items=10` satisfies the upper bound; integer values above 10 do not. Minimum/default/requiredness and rejection transport remain open. It is not a pagination/batch/selected-chunk limit. A2A declares task/capability/input-output schemas/deadline/trace; receiver may decline. Invoking principal, workspace policy, tool scope and classification authorize separately. Depicted `case_demo`, `grant_readonly_14`, deadline and absent `output_schema` establish neither typed exception nor effective grant. [PDF pp.41,87; `business_rules:r1:c67:f5`, `business_rules:r1:c139:f9`, `business_rules:r1:c139:f10`, `business_rules:r1:c139:f11`, `business_rules:r1:c139:f12`, `business_rules:r1:c139:f13`]

Run catalog: `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED`, guarded by checkpoint/runtime budget. Chapter11 terminates on missing approval, exhausted calls, repeated invalid plans, denial or deadline and displays failed checkpoint; chapter2 permits recoverable timeout. **Needs confirmation:** normal waiting versus missing-approval termination, timeout/FAILED mapping, limit counting including retries/delegation, equality at deadlines, cancellation/resume/restart. No inferred exception is selected. [PDF pp.12,41,49,82; `business_rules:r1:c14:f2`, `business_rules:r1:c68:f1`, `business_rules:r1:c79:f1`, `business_rules:r1:c137:f3`]

### BR-011–013 — Deterministic policy, review and publication

Policy normalizes/stores sensitivity, requested action, evidence quality, model class, financial-impact category and confidence bands with rule-set version. Maximum included `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` class governs routing/redaction/retention/approval dependencies; a lower-class item cannot govern a mixed-class run alone. Assignment authority, formal order representation, unknown-class handling, thresholds, normalization and complete input-to-outcome table are **Needs confirmation**. Model risk tags may propose, never override. [PDF pp.44,62; `business_rules:r1:c72:f1`, `business_rules:r1:c72:f2`, `business_rules:r1:c103:f1`]

| Condition / policy outcome | Confirmed consequence | Not established |
|---|---|---|
| Uncertain OR sensitive action / high-impact recommendation | Authorized human review; high-impact task not autonomous mutation | Risk thresholds or universal human approval |
| AUTO_ALLOW | Deterministic outcome | Unconditional publication permission |
| HUMAN_REVIEW | Deterministic outcome / reviewer route | Exact case/run state mapping |
| REQUEST_MORE_EVIDENCE | Deterministic outcome | Selected clarification workflow/state |
| DENY | Deterministic outcome | Model override or retroactive approval |
| Own-high-risk self-approval | Prohibited | Lower-risk grant; B's broader prohibition remains unresolved |
| Review assignment | Pool AND minimum role AND separation predicates | Generic Reviewer alone sufficient |
| Changed/wrong candidate hash | Stale rejection and audit, unchanged business state | Old decision transferable |
| Required review fields incomplete | Both Approve and Reject disabled | Field names or completeness sufficient authorization |
| SLA expires | No implicit approval; reassign OR escalate; escalation recorded | SLA/calendar/equality/branch/recipient |
| Override | Elevated role AND secondary reviewer AND audited reason | Hash/ACL/tenant bypass or selected eligible effects |
| Denied rework | New run revisions; original denial not retrospectively approved | Exact launch/state procedure |

[PDF pp.11,44–46,58,85,89; `business_rules:r1:c11:f2`, `business_rules:r1:c71:f1`, `business_rules:r1:c12:f2`, `business_rules:r1:c73:f1`, `business_rules:r1:c73:f2`, `business_rules:r1:c73:f6`, `business_rules:r1:c74:f5`, `business_rules:r1:c74:f6`, `business_rules:r1:c97:f6`, `business_rules:r1:c138:f6`, `business_rules:r1:c141:f6`, `business_rules:r1:c141:f10`]

Review states are `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED`, guarded by actor/hash/separation. Record decision, actor, timestamp, evaluated artifact hash and rationale; annotations optional. Show exact candidate/citations/model-prompt version/policy reasons; source inspection must be available before approval, not necessarily recorded completed. [PDF pp.45,57–58,82; `business_rules:r1:c73:f5`, `business_rules:r1:c95:f2`, `business_rules:r1:c97:f5`, `business_rules:r1:c137:f5`]

**Publication procedure:**
1. Require evidence and satisfied versioned deterministic approval policy; unapproved high-risk cannot publish.
2. Validate exact reviewed artifact and current permissions, rejecting stale evidence after intervening tenant/document changes.
3. Treat `ApprovalDecisionRecorded` as publication **validation**, not automatic publication authority.
4. Commit final response pointer and satisfied gate in the same transaction. Replay cannot publish changed artifact under old approval.

Publication endpoint/invoker, hash encoding, full predicates and recovery remain **Needs confirmation**. [PDF pp.7,11–12,45–46,87; `business_rules:r1:c4:f3`, `business_rules:r1:c11:f3`, `business_rules:r1:c13:f5`, `business_rules:r1:c74:f1`, `business_rules:r1:c76:f2`, `business_rules:r1:c139:f5`]

### BR-014 — Validation, commits, events and effective identity

| Boundary | Rule |
|---|---|
| Server validation | Before transaction entry, again domain invariants, before tool dispatch and long-work allocation; client validation convenience only |
| Dependency unavailable | Documented retryable error **OR** persisted asynchronous ID, never ambiguous success; branch/allocation/owner/readback open |
| Ordinary API result | Preserve A.2 `200/201/202/409`; `202` accepts an operation, not completed business work |
| Long-work POST | `Idempotency-Key`; identical payload original operation, changed fingerprint conflict |
| Accepted durable write | Applicable local mutation/decision/outbox ACID or explicitly reconciled saga; no global workflow transaction inferred |
| Stale/unauthorized business write | Reject before relevant event publication, unchanged business state |
| At-least-once event | Ledger/event or operation identity plus aggregate revision; record duplicate, no reapplication; detect delayed/stale revisions without cross-partition order dependence |
| Transient fault | Bounded exponential backoff, randomized jitter, per-dependency breakers; connector Retry-After/quota/fairness |
| Permanent validation/permission fault | No automatic retry |
| Operator replay | Reason, dry run, bounded scope; retain original identity **except** schema-transforming migration with explicit provenance link |
| Accepted transition evidence | One audit record, stable denied-operation codes, tenant-scoped traces; duplicate/denial evidence not suppressed |

General tenant/actor context applies at every boundary. Fuller record `tenant_id`, `revision`, `actor_id`, `occurred_at`, correlation ID applies “wherever the operation changes durable state.” Canonical event fields are `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, `payload`, UTC/canonical JSON. No aliases to SSE offsets, provider trace, request correlation or signed-job envelopes are supplied. [PDF pp.17,48–56; `business_rules:r1:c20:f8`, `business_rules:r1:c78:f1`, `business_rules:r1:c78:f2`, `business_rules:r1:c78:f6`, `business_rules:r1:c80:f1`, `business_rules:r1:c80:f6`, `business_rules:r1:c80:f7`, `business_rules:r1:c82:f1`, `business_rules:r1:c82:f3`, `business_rules:r1:c90:f5`, `business_rules:r1:c92:f5`; pp.82–84 `business_rules:r1:c137:f1`, `business_rules:r1:c137:f21`]

All registered events retain versioned envelope/outbox, correlated log/audit visibility without document diagnostic text, applicable nonmutation and duplicate guards. Do not infer emission from adjoining GETs or diagrams.

| Event | Producer / payload concepts / consumer action |
|---|---|
| CaseCreated | Case Service / case ID, revision / classify |
| DocumentNormalized | Ingestion / version ID, source hash / build index |
| SearchIndexCommitted | Indexer / generation, document revision / invalidate cache |
| AgentPlanApproved | Orchestrator / run ID, plan hash / dispatch still-authorized steps |
| ApprovalDecisionRecorded | Policy Service / task, actor, content hash / validate publication |
| WorkflowStageAdvanced | Orchestrator / run, stage, checkpoint / resume consumers |
| AccessDenied | Policy Service / principal, action, policy digest / alert enrichment |
| TenantDeletionVerified | Retention Worker / manifest ID, receipt hash / close verified purge record; scope open |

[PDF p.87 C.1; `business_rules:r1:c139:f1`, `business_rules:r1:c139:f2`, `business_rules:r1:c139:f3`, `business_rules:r1:c139:f4`, `business_rules:r1:c139:f5`, `business_rules:r1:c139:f6`, `business_rules:r1:c139:f7`, `business_rules:r1:c139:f8`]

Also preserve `BaselineCommitted`, `RunRequested`, `DeploymentPromoted`, `CaseStateChanged`, `ConnectorSyncStarted`, `ModelInvocationCompleted`, `DataRetentionPurgeCommitted`, `ApiCompatibilityVerified`, `UserReviewOpened`, `SecurityPolicyChanged`, `SloBurnRateDetected`, `BackpressureActivated`, `ReleasePromoted`, `EvaluationCompleted`, with full triggers/payloads open. `CaseStatusEvent` is not automatically `CaseStateChanged`; promotion and purge names are distinct. [PDF chapter registers pp.10–76; `business_rules:r1:c9:f8`, `business_rules:r1:c21:f8`, `business_rules:r1:c27:f8`, `business_rules:r1:c39:f8`, `business_rules:r1:c45:f8`, `business_rules:r1:c63:f8`, `business_rules:r1:c87:f8`, `business_rules:r1:c93:f8`, `business_rules:r1:c99:f8`, `business_rules:r1:c105:f8`, `business_rules:r1:c111:f8`, `business_rules:r1:c117:f8`, `business_rules:r1:c123:f8`, `business_rules:r1:c129:f8`]

### BR-015–017 — Privacy, retention, exit and period processing

**Confirmed.** Service credentials rotate automatically and never appear in traces/prompts. Application secrets use managed-identity vault access; encryption keys rotate on defined policy without bulk request-path reencryption. No model/tool receives secrets outside declared scope; this does not affirm any particular disclosure permission. Providers receive scoped context, not connector tokens/unrestricted DB access. Objects require encryption and controlled short-lived signed URLs, tenant/workspace/document/version/role key scope and opaque public names. [PDF pp.15,21,52,61–63; `business_rules:r1:c18:f2`, `business_rules:r1:c30:f6`, `business_rules:r1:c86:f1`, `business_rules:r1:c86:f2`, `business_rules:r1:c101:f2`, `business_rules:r1:c104:f7`, `business_rules:r1:c104:f8`]

Extraction tags likely PII; redact nonessential fields before providers where policy permits. Default logs count tokens/digests, not whole prompts. Neither clause authorizes prohibited diagnostics/errors: no user documents/API secrets in diagnostic traces, no source text in diagnostic telemetry, no credentials/full prompts/retrieved documents/private existence in errors. Safe structured validation details may appear. [PDF pp.62–64,84; `business_rules:r1:c103:f6`, `business_rules:r1:c103:f7`, `business_rules:r1:c107:f1`, `business_rules:r1:c108:f1`, `business_rules:r1:c137:f22`]

Audit is append-only, batch-hash chained and exported to independently controlled retention; operators may query, not alter historical review decisions. Auditor access is redacted/nonediting. SHA-256 source/revision register obligations do not select the batch-chain algorithm. Diagnostic TTL **30-day default**, security audit distinct **seven-year fictional policy**; corporate selection remains open. [PDF pp.11,62,66; `business_rules:r1:c12:f4`, `business_rules:r1:c104:f1`, `business_rules:r1:c104:f2`, `business_rules:r1:c105:f3`, `business_rules:r1:c110:f6`, `business_rules:r1:c110:f7`]

**Exit procedure:**
1. Closure preserves approved answer/cited versions/reviewer decisions as immutable lineage. CLOSED alone does not establish retention eligibility.
2. Case retention considers only eligible closed cases, preserving holds.
3. Export/delete require `Admin + approver` and two independent approval checks. Export additionally requires **two-person approval plus manifest**; a single Admin fails.
4. Export packages case metadata, approved artifacts, source references and checksum audit manifests; exclude secrets/internal model prompts.
5. Hold-safe deletion writes tombstones, removes permitted blobs/index entries, records completion receipts. Protected held records remain retained and receipted; soft-deleted entities cannot be retrieved.
6. Data-subject requests reuse inventory; `202` is acceptance, not finished download/purge. Verify completion before closing purge record; partial/held scope and tenant/workspace mapping are open.

[PDF pp.26,51,78–80,83,87–89; `business_rules:r1:c38:f5`, `business_rules:r1:c38:f6`, `business_rules:r1:c84:f7`, `business_rules:r1:c131:f1`, `business_rules:r1:c134:f1`, `business_rules:r1:c134:f6`, `business_rules:r1:c134:f7`, `business_rules:r1:c137:f19`, `business_rules:r1:c137:f20`, `business_rules:r1:c139:f8`, `business_rules:r1:c140:f11`, `business_rules:r1:c141:f13`]

| Period/calculation | Confirmed | Needs confirmation |
|---|---|---|
| Usage attribution | Invocation, embedding, storage, indexing; workspace cost center/deployment version | Units, prices, allocation, precision, rounding, price effective periods |
| Daily rollup | Budget, forecast, rejected excess requests | Day/cutoff/timezone, launch cadence, formulas, late corrections, refunds, duplicates, empty/partial report |
| Monthly availability | 99.9% reference objective | Calendar boundary, numerator/denominator, exclusions and rounding |
| Retention elapsed periods | Distinct30-day default and7-year fictional scopes | TTL start/reset, year calculation, equality, overrides, holds and receipts |
| Period-end settlement/close | Not described | Needs confirmation; no invented monthly settlement or period-close job |

[PDF pp.65–66,83; `business_rules:r1:c109:f1`, `business_rules:r1:c110:f1`, `business_rules:r1:c110:f6`, `business_rules:r1:c137:f17`]

### BR-018 — Admission, containment and recovery

Admit new AI runs only when workspace tokens **AND** queue age **AND** provider capacity satisfy thresholds. Throttling uses `429` plus `Retry-After`, preserving saved cases. Generation outage disables new generation admission but preserves manual case editing/evidence search and shows degraded status. Optional lexical fallback during vector degradation requires a visible reduced-quality flag. Never bypass authorization/approval. Pages require user-impact incidents; routine spend creates owner/threshold tickets; provider-outage page only when availability budget impacted. [PDF pp.65,68–69,79; `business_rules:r1:c109:f7`, `business_rules:r1:c113:f2`, `business_rules:r1:c115:f1`, `business_rules:r1:c115:f4`, `business_rules:r1:c115:f5`, `business_rules:r1:c133:f1`]

| Reference value | Scope / boundary |
|---|---|
| 2000 daily users;60steady/180burst rps | Workload, not selected quotas |
| 100000 indexed documents/tenant maximum;20concurrent runs/large tenant | Reference envelope; large-tenant/admission definitions open |
| Typical1MB≈40–120chunks | Content/parser dependent approximation |
| API99.9% monthly | Objective, not observed result |
| Case P95 within300ms / under300ms | Equality and common measurement unresolved |
| Search P95<1.5s | Excludes remote fetch; model separately measured; equality fails strict clause |
| RPO≤15min;RTO≤4h | Reference recovery objectives, equality included; not backup intervals |

API scaling uses utilization/latency; extraction/embedding scaling queue age/throughput. Primary writes and warm recovery snapshot restore require incident command; continuous PostgreSQL backups and object/index-recipe joint tests apply. Chaos includes429 storms, lost heartbeats, duplicates, object failure and primary outage, measuring safety **and** recovery time. [PDF pp.19,65,68–70; `business_rules:r1:c25:f1`, `business_rules:r1:c25:f6`, `business_rules:r1:c109:f1`, `business_rules:r1:c109:f2`, `business_rules:r1:c114:f1`, `business_rules:r1:c114:f5`, `business_rules:r1:c116:f1`, `business_rules:r1:c116:f2`, `business_rules:r1:c116:f7`]

Provisioning idempotently creates policy/encryption refs/role bindings/quotas/connector stubs. Visible incomplete state blocks sync; historic readiness uses index coverage, not queue emptiness. [PDF p.78; `business_rules:r1:c132:f1`, `business_rules:r1:c132:f2`, `business_rules:r1:c132:f7`, `business_rules:r1:c132:f8`]

**Delayed-index procedure:**
1. Detect oldest queue age/backlog and identify tenant/generation.
2. Pause only faulty connector/indexer shard; preserve accepted source records.
3. Diagnose event/outbox/parser/throttling/ACL revision.
4. Replay validated outbox through bounded operator-controlled work.
5. Compare source fingerprints/index versions and run denied probes before closure; closure pass criteria open.
6. Link audit IDs/time window/blast radius/quality effect/preventative action.

Suspected ACL leakage separately suspends affected aliases/revokes evidence cache/preserves audit/scoped ACL replay; search restoration requires negative access tests **pass**. [PDF pp.79,90; `business_rules:r1:c133:f5`, `business_rules:r1:c142:f7`, `business_rules:r1:c142:f8`, `business_rules:r1:c142:f9`, `business_rules:r1:c142:f10`, `business_rules:r1:c142:f11`, `business_rules:r1:c142:f12`, `business_rules:r1:c142:f13`]

### BR-019–020 — Observation, changes and release gates

Eight primary screens each require one primary action and status summary. Draft labels use accessible `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED`, not color alone. Meaningful-only announcements, visible focus/semantic regions/keyboard order and WCAG2.2AA target apply. Server UTC presents workspace-local labeled time; locale never changes durable API/order. Run refresh reconstructs server state; SSE increasing offsets reconnect with `Last-Event-ID`, replay retained caller-scoped history only. Observation/resumption headers do not authorize business execution. Optional webhooks sign/verify signature and age/retry exponentially; failures never roll back internal case. [PDF pp.55,57–59; `business_rules:r1:c91:f1`, `business_rules:r1:c91:f5`, `business_rules:r1:c96:f1`, `business_rules:r1:c96:f6`, `business_rules:r1:c97:f1`, `business_rules:r1:c98:f1`, `business_rules:r1:c98:f2`, `business_rules:r1:c98:f6`]

Baseline changes require architecture record/four impact dimensions/traceable contracts and executable tests; approved minor versus incompatible major increment precedence/reset/activation remains open. Every revised invariant links a negative test. [PDF pp.8–10; `business_rules:r1:c5:f2`, `business_rules:r1:c6:f1`, `business_rules:r1:c6:f5`]

Release procedure:
1. Use reproducible artifacts/policy checks; Terraform **OR** Bicep remains unselected. Source defaults, signed environment values and vault references remain distinct.
2. CI static/dependency scans/unit/contracts/SBOM/signed images; production verifies allowed-build-identity digest.
3. Compatible predeploy migration, nullable expansion/bounded backfill/constraints; canary; drain old readers before enforcement/removal.
4. Disclose new-write readability. Canary regression in latency/errors/auth denials/AI quality triggers automated **traffic rollback, not database down-migration**. Other data compensation only explicitly supported.
5. Security/SRE verify egress/secrets/backups/alerts before promotion. Bind/reconstruct image/schema/prompt/model-routing-policy versions.
6. Independent prompt/model roll-forward requires reevaluation. Frozen1200 synthetic controlled cases target citation precision≥0.97, unsupported≤0.02, high-risk recall1.00, with domain intervals/shift reporting. No rounding tolerance selected; low confidence blocks.
7. Critical isolation/approval tests have zero exceptions; unmitigated critical cross-tenant **OR** approval-bypass findings block regardless benchmarks. `SEC-001`–`SEC-012` release-blocking; security-control owner reviews, independently reproduces negatives and signs release. SEC/T mapping absent.

[PDF pp.52,71–76,88–89; `business_rules:r1:c85:f4`, `business_rules:r1:c120:f1`, `business_rules:r1:c120:f5`, `business_rules:r1:c121:f1`, `business_rules:r1:c121:f2`, `business_rules:r1:c121:f7`, `business_rules:r1:c121:f8`, `business_rules:r1:c122:f1`, `business_rules:r1:c122:f6`, `business_rules:r1:c122:f7`, `business_rules:r1:c125:f2`, `business_rules:r1:c127:f1`, `business_rules:r1:c127:f6`, `business_rules:r1:c127:f7`, `business_rules:r1:c128:f6`, `business_rules:r1:c128:f7`, `business_rules:r1:c140:f13`, `business_rules:r1:c140:f14`, `business_rules:r1:c140:f15`]

Appendix F retains **examples**, not selected universal defaults:

```yaml
release: r1.0
workflow: {max_plan_depth: 8, max_tool_calls: 16, run_timeout_seconds: 180, replay_dedup_hours: 24}
retrieval: {max_candidate_chunks: 80, max_selected_chunks: 10, embed_dimension: 1536, hybrid_rrf_k: 60}
policy: {auto_publish_classification: INTERNAL, require_human_review_for: [HIGH_RISK, RESTRICTED], self_approval_allowed: false}
storage: {upload_limit_mb: 25, user_data_region: primary-approved-region}
observability: {trace_sample_rate: 0.10, diagnostic_retention_days: 30, audit_retention_years: 7}
```

Independently supported8/16/1536/configurable25MB and scoped retention apply.180s/replay24h/80/10/RRF60/.10 are not chosen timeout, history, batch or pagination rules; INTERNAL not unconditional publication; placeholder region not selected. [PDF p.90; `business_rules:r1:c142:f1`, `business_rules:r1:c142:f2`, `business_rules:r1:c142:f3`, `business_rules:r1:c142:f4`, `business_rules:r1:c142:f5`, `business_rules:r1:c142:f6`]

## Application Points and Validation Conditions

### Enforcement mapping

Each row reads applicable tenant/principal/policy context and writes only authorized durable outcomes. UI display is not server enforcement. Unlisted field/schema attributes remain open.

| Rules | Screen / API enforcement | Data read/update and batch application |
|---|---|---|
| BR-001–003 | All SCRs/SF-003/017; API-002/048/056; dispatch/publication boundaries | DAT-005/008/009/010; tenant/workspace/resource ACL; all actual BAT jobs/BAT-022 |
| BR-004–005 | SCR-001/002/007, SF-007/012; API-003–005/026/049 | cases, case_revisions, workspace settings; DAT-006/010; BAT-001/014 |
| BR-006 | SCR-003/SF-008; API-006/023/049 | documents/document_versions/chunks/quality; DAT-007/011; BAT-004 |
| BR-007 | SCR-006/SF-011; API-011/027/050 | connector_cursors/source ACL/vault refs; DAT-011/017; BAT-002/003/012 |
| BR-008 | SCR-003/004/SF-008; API-012/021/022/050 | search rows/evidence_sets/cache generation/ACL; DAT-007/009/011; BAT-005/006/007 |
| BR-009–010 | SCR-004/SF-009; API-007/028/037/042e/046/051 | runs/run_steps/plan/budget/token_ledger; DAT-012/018; BAT-007 |
| BR-011–013 | SCR-005/007, SF-010/012; API-010/025/052 | policy_evaluations/evidence_sets/approval_tasks/decisions/final pointer; DAT-006/013; BAT-008/009 |
| BR-014 | API-043/044/048/053/054; server validations, not browser-only | outbox/ledger/revisions/checkpoints; DAT-008/014/018; BAT-010/011/022/023 |
| BR-015–016 | SCR-008/SF-013; API-013/016/017/029/040/041/054/056 | audit_events/holds/tombstones/deletion_receipts/manifest/vault; DAT-015/016; BAT-013/014/017/018 |
| BR-017 | Usage screen mapping open/SF-014; API-014 | token_ledger/cost centers/deployment versions/rollups; DAT-017; BAT-015 |
| BR-018 | SF-014; API-031/042b/055 | admission/queue/index/incident/recovery evidence; DAT-017; BAT-011/012/020/023 |
| BR-019 | All eight SCRs/SF-004/009/010/015; API-009/047 | server progress/source anchors/review artifact; DAT-007/008/018; BAT-007/008/021/023 |
| BR-020 | API-035/036/042c/042d/015/030/055/057 | change/release/config/fixture/report provenance; DAT-004/017/019; BAT-016/019/024 |

### Required validation outcomes

These are test obligations, **not passed results**. Safety failure cannot be offset by benchmark score. Every revised invariant has a negative-test link.

| Rule/test | Satisfied, unsatisfied and boundary validation |
|---|---|
| BR-003 / TST-003,T-01 | Valid foreign tenant resource denies non-disclosing; verify RLS/domain guards and pooled context reset; exact universal response open |
| BR-004 / TST-001/002 | Same key/request one case/identical response; changed body409 IDEMPOTENCY_CONFLICT;24h expiration/concurrency boundary needs fixture/contract |
| BR-004 | Revision mismatch409 CASE_VERSION_CONFLICT/current revision/no business mutation; missing If-Match and exact close/reopen edges open |
| BR-006 / TST-015,T-04 | Unsafe PDF/polyglot/zipped attacks quarantine/no index with scan/sandbox/bounded parsing; ZIP not allowed format;25MB equality open |
| BR-006 | Authorized low-quality document remains viewable/excluded autonomous use; quality threshold/equality fixtures open |
| BR-007 | Quarantined poison exception may continue with durable ledger; cursor cannot advance absent durable preceding outcome; retry/count/continue boundaries open |
| BR-007 | Revoked queued credential CONNECTOR_REAUTH_REQUIRED/no tokens; incomplete provisioning visible/blocks sync; coverage readiness not empty queue |
| BR-008 / TST-004,T-08 | Indexed source revoke excludes next-query evidence; also revoke **during search**; mechanism open, no ignored test |
| BR-009 / TST-005 | Invalid model schema MODEL_OUTPUT_INVALID/no publish; unknown/citation/control triggers and parse-retry fixtures |
| BR-009 / T-06 | Regional outage only approved fallback; quota exhaustion cannot auto-switch model/class; equal handling allowed/weaker forbidden |
| BR-010 / TST-014,T-02,T-10 | Arbitrary MCP DENY before dispatch; hostile evidence/recursive hints never authorize; max_items10 allowed/>10 invalid; depth/call counting open |
| BR-012 / TST-006,T-03 | Wrong/prior hash stale reject/audit/no mutation; inspectable exact source; incomplete fields disable both controls |
| BR-012 / TST-010 | Expiry never approves; escalation recorded; SLA equality/assignment alternatives open |
| BR-013 | Permission change after search/review rejects stale evidence; pointer/gate atomic exact artifact; replay old approval cannot change published artifact |
| BR-014 / TST-007,T-07 | Same event100 attempts → exactly one accepted transition; duplicate records/no reapplication; delayed revisions safe, not exactly-once delivery |
| BR-015 / T-05,T-09 | Observe traces/provider calls for credentials; historical edit denied/hash integrity; no document/API-secret diagnostics |
| BR-016 / T-11,TST-013 | Single Admin export denied; two-person/manifest; held protected purge records retained/receipted |
| BR-018 / TST-008/012 | Provider429 capped retry/admission, saved cases retained; recovery≤stated RPO/RTO while preserving safety; clocks/limits fixtures open |
| BR-019 / TST-011 | Keyboard-only case opens without blocked action and with visible focus; scoped retained SSE/server refresh; expiry/live revocation open |
| BR-020 / TST-016,T-12 | Safety-regressed canary blocked/traffic rollback not DB down-migration; replaced score fixtures fail integrity; low confidence blocks independent of point targets |

[PDF pp.88–89 D/E; `business_rules:r1:c140:f1`, `business_rules:r1:c140:f2`, `business_rules:r1:c140:f3`, `business_rules:r1:c140:f4`, `business_rules:r1:c140:f5`, `business_rules:r1:c140:f6`, `business_rules:r1:c140:f7`, `business_rules:r1:c140:f8`, `business_rules:r1:c140:f9`, `business_rules:r1:c140:f10`, `business_rules:r1:c140:f11`, `business_rules:r1:c140:f12`, `business_rules:r1:c141:f1`, `business_rules:r1:c141:f2`, `business_rules:r1:c141:f3`, `business_rules:r1:c141:f4`, `business_rules:r1:c141:f5`, `business_rules:r1:c141:f6`, `business_rules:r1:c141:f7`, `business_rules:r1:c141:f8`, `business_rules:r1:c141:f9`, `business_rules:r1:c141:f10`, `business_rules:r1:c141:f11`, `business_rules:r1:c141:f12`, `business_rules:r1:c141:f13`, `business_rules:r1:c141:f14`, `business_rules:r1:c141:f15`, `business_rules:r1:c141:f16`]

Deterministic tests avoid live model calls and pin provider adapters. Disposable integration covers transactions, replay, ACL revocation, delayed indexing and purge. Synthetic fixtures cover successful/empty/mixed-permission/adversarial/malformed; each randomized seed recorded; corpora frozen/versioned/independently leakage-reviewed. Complete minimum pipeline: unit, schema evolution, negative authorization, workflow replay, staging connector sync, visual accessibility, search recall, grounding, policy recall, load and DR. Sign outputs and reference release digest. Empty fixture coverage does not define runtime successful no-op behavior. [PDF pp.74–75,89; `business_rules:r1:c126:f1`, `business_rules:r1:c126:f6`, `business_rules:r1:c126:f7`, `business_rules:r1:c141:f17`, `business_rules:r1:c141:f18`, `business_rules:r1:c141:f19`, `business_rules:r1:c141:f20`, `business_rules:r1:c141:f21`, `business_rules:r1:c141:f22`]

## Consistency and Open Questions

### Source conflicts and required amendments

No unresolved choice grants implementation discretion. Do not rewrite completed files. Record amendments with the affected links below.

| Open ID / affected rule | Both positions and required decision | Earlier identifiers |
|---|---|---|
| BR-OQ-002 / BR-012 | Own-high-risk no self-approval p.11 versus unqualified B no self approval p.85; F false example not resolution. Clarify breadth/definition/overrides; no lower-risk grant | SF OQ-006; API-G04; DAT-OQ-006; BAT-OQ-010 |
| BR-OQ-003 / BR-009–010 | Missing approval termination p.41 versus AWAITING_REVIEW pp.49/82; recoverable timeout p.12 versus FAILED catalog. Define applicability/status/recovery. General POST /v1/runs p.15 versus case route p.83 has no confirmed relationship | SF OQ-003/004; API-G02a/b; DAT-OQ-005; BAT-OQ-008 |
| BR-OQ-004 / BR-004/007/008/012/019 | Immutable derivative registers versus mutation/expiry/forms/alias switch; preserve Case/CaseService/CaseAggregate, APIReplicaSet, TenantMembership, SyncRun, ExtractionJob, IndexAlias, ApprovalTask, ReviewForm, ErrorEnvelope, ProvisioningJob. CacheEntry ledger versus ephemeral cache. Define subjects/hashes/revisions, not invented heads/snapshots | API-G05; DAT-OQ-002–004; BAT-OQ-009 |
| BR-OQ-007 / BR-007/014 | Bounded malformed retries/poison continuation pp.28–29 versus permanent validation/permission nonretry p.49; classify fault and durable quarantine/cursor outcome | API-G09; DAT-OQ-011; BAT-OQ-006/007 |
| BR-OQ-002 / BR-012 | Reassign OR escalate p.45 versus escalation recorded p.89. Define SLA/branch/recording without silent approval | API-G12; DAT-OQ-013; BAT-OQ-010 |
| BR-OQ-012 / BR-016 | Immutable closure lineage/eligible retention/holds versus scheduled removal; tenant-named event/receipts versus workspace paths. Define permitted purge scope/partial completion/reopen race | SF OQ-011/012/017; API-G13; DAT-OQ-015; BAT-OQ-012 |
| BR-OQ-015 / BR-018 | Within300ms p.12 versus under300ms p.65; equality/common load/measurement missing | SF OQ-015; API-G17; DAT-OQ-017; BAT-OQ-017 |
| BR-OQ-009 / BR-014 | Conditional dependency error OR async ID versus ordinary A.2 reads/admissions; no GET jobs inferred | API-G03; DAT-OQ-007; BAT-OQ-011 |
| BR-OQ-009 / BR-014 | Snake-case prose p.54 versus explicit uppercase codes pp.38/84/89; preserve CASE_VERSION_CONFLICT/IDEMPOTENCY_CONFLICT/MODEL_OUTPUT_INVALID; clarify convention | SF OQ-009; API-G15; DAT-OQ-019 |
| BR-OQ-018 / BR-010 | Full declared A2A input/output schemas p.41 versus case_demo/omitted output_schema depiction and typed UUID tool p.87; no exception | API-G10; DAT-OQ-012; SF OQ-018 |

Evidence pairs: `business_rules:r1:c12:f2`/`business_rules:r1:c138:f6`; `business_rules:r1:c68:f1`/`business_rules:r1:c79:f1`/`business_rules:r1:c137:f3`/`business_rules:r1:c14:f2`; `business_rules:r1:c18:f4`/`business_rules:r1:c137:f10`; `business_rules:r1:c39:f3`/`business_rules:r1:c36:f4`; `business_rules:r1:c75:f3`/`business_rules:r1:c73:f2`; `business_rules:r1:c99:f3`/`business_rules:r1:c97:f6`; `business_rules:r1:c57:f3`/`business_rules:r1:c54:f5`; `business_rules:r1:c19:f5`/`business_rules:r1:c87:f5`; `business_rules:r1:c44:f7`/`business_rules:r1:c80:f1`; `business_rules:r1:c73:f2`/`business_rules:r1:c141:f10`; `business_rules:r1:c14:f1`/`business_rules:r1:c109:f1`; `business_rules:r1:c90:f1`/`business_rules:r1:c137:f21`; `business_rules:r1:c67:f5`/`business_rules:r1:c139:f13`. Locations are the original PDF pages stated beside each rule.

### Remaining implementation decisions

| Open group | Definition required; no selected proposal |
|---|---|
| BR-OQ-001 | All field/schema/permission/role/audience/session/ownership mappings, unknown requiredness/defaults/types/cardinality and errors |
| BR-OQ-005/019 | Classification reason/intake, priority/calendar/DST formulas; normalized policy domains/precedence, version selection/activation/reevaluation; governance impact scores/approval/minor-major reset |
| BR-OQ-006–008 | MIME/MB/scan/bomb/OCR/quality/provenance/hash/Citation; capabilities/cursor/reauth/quarantine/readiness/fairness; ranking/token/model/prompt/retry/unsupported thresholds |
| BR-OQ-010 | Canonical JSON/context aliases/job signatures, event triggers/full payloads, ledger/revision atomicity/windows/delayed ordering, transaction participants, replay provenance, request24h origin/expiry |
| BR-OQ-011 | In-flight ACL/cache/stream/download/URL revocation and failure recovery; next-query/current-publication obligations remain binding |
| BR-OQ-012–014 | Eligibility/holds/lineage exit/receipt/manifest/checksum, retention period arithmetic, key/credential intervals/chain algorithms, daily usage prices/formulas/rounding/cutoff/timezone/adjustments; period-end processing not described |
| BR-OQ-015–016 | Scale/admission/burn-rate/SLO/recovery clocks/criteria, canary/compatibility/readability/signatures, statistical confidence/domains/shift/metric arithmetic, complete fixtures and SEC/T/TST mappings |
| BR-OQ-017 | Routes/actions/fields/permissions and all fictional title/selection pairs in SF-005; accessible focus/announcement/locale/number rules. Identical garbled comparisons create no amendment |
| BR-OQ-018/020 | Complete A2A grants/schemas/decline/deadline and all architecture selections; optional BFF/webhooks and Terraform/Bicep remain unselected |

Preserve the established logical register classifications in DAT-004: Owner aggregate / `UUIDv7 + tenant scope`; Immutable derivative / `SHA-256 source/ revision`; Policy-bound control / `Actor and role predicate`; Operational ledger / `Event ID + trace context`. These are obligations at unspecified logical subjects, not complete tables, hash-equivalence decisions or permissions. Resolve disputed subjects with original register evidence rather than majority voting.

Preserve SF-005 figure title/selection evidence: p.7 Case Detail/Case Queue; p.14 Case Queue/Overview; p.33 Case Detail/Case Queue; p.43 Evidence Explorer/Case Detail; p.47 Agent Run/Evidence Viewer; p.60 Approval Inbox/Agent Runs; p.67 Connector Health/Review Inbox; p.77 Audit Explorer/Connectors; p.81 AI Quality/Audit Events. All displayed values remain fictional. No aliases, new screens or citation minimums follow. [PDF cited figures; `business_rules:r1:c4:f8`, `business_rules:r1:c16:f6`, `business_rules:r1:c52:f6`, `business_rules:r1:c70:f6`, `business_rules:r1:c76:f6`, `business_rules:r1:c100:f6`, `business_rules:r1:c112:f6`, `business_rules:r1:c130:f6`, `business_rules:r1:c136:f6`]

**Prior-stage amendment notes:** retain CaseStateChanged, ConnectorSyncStarted and scoped Idempotency-Key additions. Explicitly preserve signed immutable job tenant identity and managed-identity vault/policy-driven encryption-key rotation without request-path bulk reencryption as distinct from service-credential rotation. Add the directly confirmed qualification **configurable numeric thresholds are versioned policy** beside earlier configuration requirements; activation/effective periods still open. [PDF pp.9,22,26,29,54,63; `business_rules:r1:c7:f6`, `business_rules:r1:c32:f2`, `business_rules:r1:c39:f8`, `business_rules:r1:c45:f8`, `business_rules:r1:c90:f5`, `business_rules:r1:c104:f8`]

Before implementation lock, each of six selections—supported cloud region, exact search provider, identity provider, approved model deployments, corporate retention and third-party connector permissions—requires a **dated architecture decision**. Per-tenant key isolation versus rotation throughput requires future-revision resolution **before enterprise GA**. Neither milestone supplies a calendar date, owner, approval or actual selection. [PDF pp.10,90; `business_rules:r1:c8:f8`, `business_rules:r1:c142:f14`]

**Dependencies:** detailed exception-handling, integration and remaining implementation refinements are **To be defined in a later stage**. Stage8 will consolidate TBDs from completed Markdown into `08_architecture_decision.md`, linking BR identifiers and prior SF/API/DAT/BAT identifiers. It is not generated here. No test pass, sign-off, architecture selection, owner or deadline is invented.
