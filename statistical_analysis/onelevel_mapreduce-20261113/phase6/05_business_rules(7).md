# 5. Business Rules

## Rule Inventory and Scope

### Baseline, evidence and implementation status

`05_business_rules.md` consolidates shared conditions for **OrionDesk AI**, `OD-AI-DDS-001`, release `R1.0`, design revision `1.3`. **Confirmed** means confirmed requirements of the fictional reference design, not evidence of deployment. The source states: “All numbers are design assumptions, not measured production performance.” [Source: `1794325316-OrionDesk_AI_Detailed_Design_Specification.pdf`, pp.1–2; business_rules:r1:c1:f1–f4, business_rules:r1:c2:f1.]

All citations below refer to that exact source filename and original pages. Finding shorthand `cN:fM` means `business_rules:r1:cN:fM`; ranges enumerate the corresponding findings. BR identifiers are assigned here, not invented source REQ/SEC mappings. Source `TST-001`–`TST-016`, `T-01`–`T-12` and `SEC-001`–`SEC-012` retain their namespaces; no one-to-one T/SEC mapping is supplied.

**Needs confirmation** is an implementation blocker, not permission for an implementation AI to select a default. **Proposal** means an explicitly unapproved design suggestion; this file approves none. Earlier files are reference dependencies, not independent evidence: [01_screen_functions.md](01_screen_functions.md), [02_api.md](02_api.md), [03_data.md](03_data.md), [04_batch_functions.md](04_batch_functions.md). Their SCR/SF/API/DAT/BAT identifiers retain their meanings. Application mappings do not invent buttons, routes, schemas or separately deployed jobs.

Figures define logical boundaries, not generated artifacts, physical cardinalities or executable navigation/job graphs. Contents pp.2–6 are evidence navigation only. Full-scan judgments include their qualification, chapter registers and representative views. [p.2, pp.3–6; c2:f2–f7.]

### Rule inventory

Every row states a shared enforcement obligation. Detailed predicates, data and validation cases follow. Unless a period is explicitly supplied, apply the rule at the stated execution point using authorized versioned policy; activation dates, in-flight version choice and grandfathering are **Needs confirmation**.

| Rule | Name and purpose | Targets, actors and timing | Evidence |
|---|---|---|---|
| BR-001 | Baseline governance and scope | All implementation and baseline changes; engineering/change authorization remains policy-defined | pp.8–10 c4:f1–f19 |
| BR-002 | Authenticate and authorize resources | Every principal/service request; gateway, domain transaction, storage, retrieval and publication | pp.21–23 c8:f1–f18; p.83 c26:f6–f20 |
| BR-003 | Tenant persistence and parent integrity | Every tenant-owned row/job; transaction setup and completion; database/service identities | pp.22,51,85–86 c8:f8, c17:f1–f3, c27:f2–f4,f20,f25–f27 |
| BR-004 | Case lifecycle and classification | Analyst creation/classification; authorized Owner edits; transition/closure roles unresolved | pp.12,24–26,82 c5:f9, c9:f1–f16, c26:f2 |
| BR-005 | Priority and contractual deadlines | Explicit impact/urgency; workspace calendar; calculation/recalculation | p.25 §6.3.1 c9:f9 |
| BR-006 | Revision and idempotency safety | Mutating clients/services/jobs; before accepted effects and on retries | pp.15,25,54,89 c6:f1,f12, c9:f7–f8, c18:f4, c30:f1–f2,f7 |
| BR-007 | Safe ingestion and immutable provenance | Analyst attachments/connector inputs; validate, scan, parse, normalize, cite | pp.30–32 c11:f1–f18; p.85 c27:f6–f8 |
| BR-008 | Connector trust and durable continuation | Admin sync, authorized Operators, workers; provisioning/credential/cursor/item gates | pp.27–29 c10:f1–f19; p.78 c25:f2–f3 |
| BR-009 | Grounded retrieval and index authority | Member search/authorized evidence consumers; index switch, result selection and citation release | pp.34–36 c12:f1–f17; pp.49,53 c16:f8, c17:f12 |
| BR-010 | Model routing, trust and structured output | Workspace-approved deployment and gateway; before provider/tool release and output acceptance | pp.37–39 c13:f1–f19; pp.61–63 c20:f1–f17 |
| BR-011 | Bounded orchestration and capability access | Analyst run/agents/services; admission, plan, dispatch/checkpoint and termination | pp.40–42 c14:f1–f18; pp.48–49 c16:f1–f7; p.87 c28:f9–f13 |
| BR-012 | Deterministic policy decision | Policy Service, never LLM authority; candidate evaluation and publication validation | pp.44–46 c15:f1–f18; p.62 c20:f7 |
| BR-013 | Independent exact-artifact review | Eligible Reviewer, independent secondary reviewer for override; task lifecycle/decision/expiry | pp.11,45–46,57–58,82,85 c5:f3–f5, c15:f2,f8–f12, c19:f1,f7, c26:f5, c27:f12–f13 |
| BR-014 | Atomic supported publication | Policy/domain gate; immediately before final pointer commit and on replay | pp.7,12,45–46,52,87 c3:f3–f4, c5:f2,f10, c15:f2,f11,f16, c17:f8, c28:f5 |
| BR-015 | Durable delivery, retries and recovery | Scoped producers/consumers/Operators; outbox commit, consumption, fault and replay | pp.17,48–50 c6:f12, c16:f1–f17; p.90 c31:f6–f10 |
| BR-016 | Safe diagnostics and immutable audit | Auditor redacted reads; Operators query-only; every accepted/denied transition and retained export | pp.11,23,54,62–66,84 c5:f5, c8:f9, c18:f2, c20:f10, c21:f1–f17, c26:f22 |
| BR-017 | Retention, legal hold, export and deletion | Admin + independent approver; eligible lifecycle processing; hold checks precede disposal | pp.26,51,66,78–80,83,89 c9:f10, c17:f4, c21:f12, c25:f1,f6–f7, c26:f19–f20, c30:f13 |
| BR-018 | Usage, quota and period reporting | Run/gateway workers and Admin usage read; reserve/meter/admit/aggregate | pp.38,65,69,83,85 c13:f7, c21:f11, c22:f5, c26:f17, c27:f17 |
| BR-019 | Degradation and safety containment | Services/Operators and user-visible status; outage/throttle/ACL incident | pp.68–70,79 c22:f1–f8, c25:f4–f5 |
| BR-020 | Accessible, truthful presentation | All eight screens; draft/review/progress/error/time display and live updates | pp.57–59 c19:f1–f19; p.89 c30:f11 |
| BR-021 | Private deployment, secrets and recovery | Separate service identities, Security/SRE/incident command; deploy/rotate/restore | pp.18–20,63,69–70 c7:f1–f17, c20:f11, c22:f7–f8 |
| BR-022 | Release correctness and evaluation | CI/evaluation/Security/SRE; change, reevaluation, canary and promotion | pp.71–76,88–89 c23:f1–f18, c24:f1–f18, c29:f1–f14, c30:f17–f22 |

### BR-001 Scope and governance

**Confirmed:** Process enterprise knowledge/user cases, not physical automation or irreversible financial transactions. Exclude foundation-model fine-tuning, unrestricted browsing, agent administrative cloud permissions and application-hosted GPU inference. Defer cross-region active/active mutation, OCR beyond English and customer-managed weights. Ordinary authorized manual case operations are not excluded. [pp.9–10,19; c4:f9,f13, c7:f8.]

Baseline decisions supersede informal discussion; changes require architecture-decision records and requirement-to-contract-to-executable-test traceability. Proposals carry behavior, migration, threat-surface and operating-cost impact scores. Approved records increment minor revision; incompatible protocol changes increment major revision. Scales and simultaneous-condition precedence are **BR-OQ-001**. Every revised invariant links at least one negative test. Configurable numeric thresholds are versioned policy; an `OBLIGATORY` control is an acceptance criterion. Nonbreaking contracts evolve additively; removals require scheduled migration. [pp.8–10,15; c4:f2–f4,f10, c6:f7.]

## Decisions, Calculations, and State Transitions

### BR-002–003 Authorization decision and timing

“Every request is bound to an authenticated principal and a tenant.” Authorization combines **role, tenant, workspace membership, case sensitivity, originating document ACL, requested action and separation of duties**. Hidden navigation is never enforcement. Gateway broad checks precede independent domain checks inside transactions; storage predicates always include tenant. Filter document ACL before any chunk reaches the model, verify citations before display, and recompute current permissions before publication. [pp.21–23,31,35,51; c8:f1–f9, c11:f6, c12:f1,f10, c17:f1.]

| Condition | Required result | Qualification/open decision |
|---|---|---|
| Valid authenticated principal/tenant and all applicable resource predicates satisfied | Continue to remaining revision/evidence/policy gates | A role alone never grants all operations |
| Unexpected token algorithm or missing tenancy claim | Reject at gateway | Allowed algorithms/audiences and error schema need confirmation |
| Foreign-tenant identifier, even if valid | Same not-found response class as absent ID; `404`-equivalent non-disclosing failure | Safely audit principal/denied resource class; do not disclose existence |
| Stale/unauthorized mutation | Reject, unchanged business state | Denial evidence still required; ordering/revision is BR-OQ-012 |
| ACL revoked after indexing or during search | No forbidden evidence on next query; invalidate affected cache before new results | Eventual index consistency is not an exception |
| Permissions changed after retrieval | Publication recomputes and rejects stale evidence | Retained historical evidence confers no continuing permission |

Interactive authentication uses OIDC authorization code with PKCE; tokens carry issuer, audience, expiry, subject and tenant. Browser local storage must not contain long-lived refresh tokens. Secure, HttpOnly, SameSite BFF cookies are **permitted, not selected**. Rotate service credentials automatically; never put them in traces/prompts. [p.21 c8:f3–f4; p.15 c6:f2.]

Baseline roles: `Analyst`, `Reviewer`, `Admin`, `Auditor`, `Service`. Persona `Workspace Admin`, resource `Owner`, membership `Member`, extra `approver` and `Operators` need mapping. Confirmed API action scopes are preserved below; other scopes are **Needs confirmation**, not grants. [pp.11,22,83; c5:f3–f5, c8:f5, c26:f6–f20.]

| Scope | Confirmed interfaces/results |
|---|---|
| Analyst | API-001 create `201`; API-006 attachment `202`; API-011 bounded run `202` |
| Analyst / Reviewer | API-003 authorized current case `200`; API-013 run stages/evidence `200`; API-015 SSE `200` |
| Owner | API-004 `PATCH /v1/cases/{caseId}`, required `If-Match`, `200`/`409` |
| Reviewer | API-017 `POST /v1/approvals/{approvalId}/decision`, reviewed hash, `200`/`409` |
| Admin | API-018 incremental sync `202`; API-021 usage `200`; API-022 frozen evaluation `202` |
| Member | API-008 `POST /v1/search`, ACL-filtered lexical/semantic evidence `200` |
| Auditor | API-020 immutable cursor log `200`, redacted scope, no case edits |
| Admin + approver | API-024 export and API-025 legal-hold-safe deletion `202`; two independent checks, not one person's combined title |

Every tenant-owned row has `tenant_id`; database requests use tenant context/RLS and jobs use signed immutable tenant envelopes. Reference `cases` policy is `tenant_id = current_setting('app.tenant_id')::UUID`. Reset pooled scoped variables after **every transaction**, including failures. Production additionally enforces workspace-tenancy membership via FK or controlled write procedures; separate tenant/workspace FKs alone are insufficient. Selection, RLS bypass/roles and missing-context behavior are **BR-OQ-002**. [pp.22,86; c8:f8, c27:f20,f25–f27.]

Persistence IDs are UUIDv7 with tenant/business-key uniqueness; this does not settle all REST placeholder types. Tenant `slug` is unique. Appendix B is selected data, not complete production schema. [pp.51,85–86; c17:f2, c27:f1–f4.]

### BR-004–005 Case states, classification and calculations

**Confirmed:** Case begins `NEW`, receives business context/attachments and asynchronous policy-aware classification with labels, confidences and provenance. Label correction requires a reason code. Priority cannot derive from model output alone. [p.12 c5:f9; p.25 c9:f9.]

| Current case state | Supplied destination | Preconditions/result |
|---|---|---|
| `NEW` | `TRIAGED` | Authorized role/current revision/required approval guards |
| `TRIAGED` | `IN_PROGRESS` | Same guards |
| `IN_PROGRESS` | `PENDING_APPROVAL` or `RESOLVED` | Same guards; `RESOLVED` edge does not waive publication policy |
| `PENDING_APPROVAL` | `RESOLVED` or `IN_PROGRESS` | Same guards; review/rework paths must be defined |
| Closure | `CLOSED` catalog confirmed; incoming edge unspecified | Snapshot approved answer, cited versions and reviewer decisions |
| `CLOSED` | Explicit reopening as new revision | Final otherwise; target/role/interface not supplied |

Sources: pp.24–26,82; c9:f1,f5–f10, c26:f2. **BR-OQ-003:** Do not invent close-entry/reopen edges, automatic transitions, correction roles or editable fields by state.

Current case stores title, description, priority, sensitivity, status, owner, approved-result pointer and monotonic revision; attachments/runs are separate immutable-ID-linked entities. `case_revisions` append-only, `document_versions` and `approval_decisions` immutable. [pp.24,85; c9:f5, c27:f5,f7,f13.]

Reference database constraints: `id UUID PRIMARY KEY`; non-null tenant/workspace UUID FKs; six-state `TEXT NOT NULL CHECK`; `revision BIGINT NOT NULL DEFAULT 1`; `sensitivity TEXT NOT NULL DEFAULT 'INTERNAL'`; timestamps `TIMESTAMPTZ NOT NULL DEFAULT now()`; `UNIQUE (tenant_id,id)`. These are **database defaults**, not browser defaults, a SQL `NEW` default, positivity check, revision increment mechanism or automatic updated-at trigger. [p.86 c27:f20–f24.]

| Calculation | Confirmed inputs/meaning | Formula, rounding, boundaries and missing decisions |
|---|---|---|
| Priority | Explicit impact and urgency | Formula, catalogs, units, weights, tie priority, rounding and missing-input result **Needs confirmation** |
| Contract deadline | Business calendar in workspace timezone | SLA duration/start, holidays, work hours, DST, timezone source, period boundaries and recalculation **Needs confirmation** |
| Breach prediction | Advisory only | Cannot modify contractual deadline; prediction formula/precision/actions unspecified |
| Classification confidence | Stored separately with labels/provenance | Scale, thresholds, correction catalog and treatment of absent confidence unspecified |

Source: p.25 §6.3.1 c9:f9; classification p.12 c5:f9. **BR-OQ-004:** No implementation-selected formula or calendar is authorized.

### BR-006 Revision, idempotency and validation outcomes

1. Validate payload before transaction/allocation, again at domain invariants and before tool dispatch. Client validation is convenience only.
2. Apply principal/resource, revision/hash and idempotency predicates before accepted effects.
3. `If-Match` conflict returns `409 CASE_VERSION_CONFLICT` with current revision; do not automatically merge/retry a stale edit.
4. Job-creating POSTs require `Idempotency-Key`; identical key/payload returns original operation/outcome. Same key with changed fingerprint returns `409 IDEMPOTENCY_CONFLICT`, not a second outcome.
5. Actor/request-fingerprint outcomes are retained **24 hours**. Full scope, fingerprint canonicalization, concurrent locking, missing key/header and exactly-at/after-expiry behavior require confirmation.
6. Every cross-service write is retry-idempotent. Consumer dedup is not limited to this 24-hour launch policy unless separately specified.

Sources: pp.15–17,25,54,56,89; c6:f1,f12, c9:f7, c18:f4,f12, c30:f1–f2,f7. **BR-OQ-005** covers missing arbitration and expiry semantics.

Known safe outcomes: `422` schema-invalid request; `429` quota with `Retry-After`; foreign resource `404`-equivalent; `NO_SUPPORTED_EVIDENCE`, `MODEL_OUTPUT_INVALID`, `CONNECTOR_REAUTH_REQUIRED` retain literals without invented HTTP mappings. Example case conflict message is `Case revision no longer matches.`, `retryable: false`; safe details contain expected/actual revisions, while `7`, `8` and `trace_01HZZ_EXAMPLE` are placeholders. Error details may be included if safe, never credentials, full prompts, retrieved documents or unauthorized existence. Preserve uppercase literals despite snake-case convention prose. [pp.27,36,38,54,84,89; c10:f7, c12:f11, c13:f6, c18:f3–f4, c26:f21–f22, c30:f2–f6.]

If a dependency is unavailable, return documented retryable error or persisted asynchronous job identifier, **never ambiguous success**. Per-interface branch/status/schema is unresolved where absent. `202` acknowledges work, not readiness, success of every item or approved publication.

### BR-007 Ingestion and evidence decision table

| Condition/input | Required handling | Exception/boundary |
|---|---|---|
| PDF, DOCX, HTML or UTF-8 text; matching signature/extension and active cap/decompression policy | Accept into guarded ingestion operation | Configurable **25 MB per file**; byte convention/equality and decompression threshold unresolved |
| Signature mismatch, unsupported/oversized/abusive input | Fail closed with stable non-sensitive code | Literal/status not supplied |
| Unsafe attachment | Scan before parser; quarantine, no search indexing | Disable macros; never fetch embedded remote references |
| PDF parsing | Preserve page/bbox blocks, tables' rows/columns, headings/reading order | Numbering/coordinate units/schema unresolved |
| OCR fallback | Require opt-in, retain marked provenance | Actor/control/default unresolved; OCR beyond English deferred |
| Normalization/reprocessing | Strip transport artifacts, not claims; content fingerprint + pipeline version immutable derivative IDs | New processing may coexist side by side |
| Low-quality permitted document | Remain viewable; exclude autonomous recommendations | Not equivalent to malware quarantine; manual recommendation scope unresolved |
| Generated citation | Stored URI/file hash/page/optional bbox, resolvable anchor and current permission | No minimum citation count supplied; optional bbox remains optional |

Sources: pp.30–32 c11:f1–f7; p.10 c4:f13. Capture empty-page ratio, unknown-character ratio, table-loss indicators and language confidence. Formulas/denominators/scales/thresholds and all hash/anchor formats are **BR-OQ-006**.

Document catalog `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED` is guarded by virus scan/quality. Exact edges and low-quality state mapping are not defined. [p.82 c26:f4.]

### BR-008 Connector decisions and partial outcomes

1. Block sync while provisioning is incomplete; display incomplete status. Provision policy/key refs/roles/quotas/connector stubs as one idempotent workflow, not an invented single distributed transaction.
2. Preserve stable source identities, ACL and change history. Capability discovery covers list/fetch/delta cursor/ACL/delete.
3. Missing capability produces **lower-trust ingestion and explicit user warning**, not silent capability assumption or blanket rejection.
4. Keep refresh/service credentials in workspace-scoped vault references. Authorized Operator revocation makes queued jobs fail `CONNECTOR_REAUTH_REQUIRED` without token exposure.
5. Store provider cursor, high-watermark and error ledger. Advance only after **all preceding items have durable ingestion outcomes**. Completed downstream indexing is not a supplied extra prerequisite.
6. Honor provider `Retry-After`, workspace quotas, backoff/jitter and fair scheduling so large tenants do not starve smaller workspaces.
7. After bounded retries, malformed item quarantines with reason/correlation/remediation. Remaining batch **may proceed with ledger-recorded exception**; do not call partial batch all-success or force whole-batch rollback.
8. Historical ingestion uses bounded windows, stable IDs and per-batch reconciliation receipts; readiness uses **index coverage, not queue emptiness**.

Sources: pp.27–29,78; c10:f1–f13, c25:f2–f3. **BR-OQ-007:** Capability effects, continuation choice, cursor ordering/atomicity, retry/quota/fairness parameters, empty delta and partial statuses remain unselected.

### BR-009 Index, retrieval and citations

PostgreSQL remains authoritative; vector/keyword index is an eventually consistent derivative, cache ephemeral. Retrieval ranking is not authorization. Scoped search rows contain tenant/workspace/version/chunk, language/classification, **1536-dimensional embedding**, normalized keyword text. Parallel index rebuild atomically switches read alias only after completeness/recall checks. Failed indexing preserves accepted metadata, reconciles fingerprints and repairs links from outbox. [pp.16,34,49; c6:f9, c12:f1–f6, c16:f8.]

Hybrid search forms lexical and normalized vector queries, bounded candidate sets, reciprocal rank fusion, deterministic reranking, diversity against redundant same-document hits, relevant-source coverage and per-query token caps. Exact formulas, fusion parameter, ties, selection counts and tokenizer/budgets are **BR-OQ-008**, not inferred from examples. [p.35 c12:f7–f8.]

Evidence items include chunk ID/source title/document revision/page anchor/ACL digest. Opaque citation IDs verify before display; clicking a permitted citation opens source and anchored page highlight. Insufficient confidence or evidence quality returns `NO_SUPPORTED_EVIDENCE`, not fabricated context. Clarification or human routing is permitted; universal branch remains open. Missing citations yield needs-review or unsupported outcome, never fabricated approved answer. [pp.35–36,57,89; c12:f10–f11, c19:f5, c30:f9.]

Source deletion tombstones and schedules index removal; soft-deleted content cannot be retrieved. ACL changes purge affected cache before new results/normal TTL and revocation applies before next retrieval. Cache key comprises tenant, user-scope digest, source ACL revision, query hash and index generation. Private objects use opaque public names, tenant/workspace/document/version/role keys, encryption and scoped short-lived signed URLs. Lifetimes/geometry/cache mechanics remain unresolved. [pp.28,51–53; c10:f10, c17:f4,f11–f12.]

### BR-010–011 Model, tools and bounded execution

“Model output is data, never proof that a tool action is authorized.” Browser arbitrary tool definitions are prohibited. Retrieved/model payloads cannot change tenancy, approvals or deterministic policy. [pp.7,37; c3:f2,f4, c13:f2.]

| Decision point | Required conditions/result |
|---|---|
| Deployment selection | Specific workspace-whitelisted deployment with capability/region/data handling/context/cost/evaluation approval; not blanket provider-brand approval |
| Fallback | Approved model with equal or stronger data-handling class; outage never authorizes restricted content to unapproved region/deployment |
| Prompt composition | Distinct fixed system rules, signed workflow, validated user input, delimited untrusted evidence; strip evidence-context tool directives and record injection indicators without rewriting source artifacts |
| Personal data | Extraction tags likely personal data; redact nonessential fields before provider where policy permits; default logs digests/counts, not entire prompts |
| Structured output | Versioned JSON schema; unknown fields, invalid citations or control-character injection trigger `MODEL_OUTPUT_INVALID`; bounded parsing retries, no publication on failure |
| Tool dispatch | Allowlisted/version-pinned schemas, validated arguments, scoped identity and separate capability authorization; discovery is not authority |
| External/consequential write | Separate external-write capability grant; if consequential, human authorization and idempotency; denied effect cannot use semantically equivalent tool |
| A2A handoff | Task/capability/declared input-output schemas/deadline/trace; authorized receiving agent may decline |

Sources: pp.37–42,61–62,87; c13:f3–f8, c14:f8–f12, c20:f1–f8, c28:f12. **BR-OQ-009:** Registry order/class comparison, consequential definition, schemas, redaction rules and parse limits remain open.

`knowledge.search@v1` input `{query: string, case_id: uuid, max_items: int<=10}`; output `{evidence_set_id: uuid, citations: Citation[]}`; tenant `read:permitted_documents`, read-only, no arbitrary URLs/filesystem. **10 passes the upper bound; 11 fails.** Minimum/default/requiredness/Citation schema remain open. A2A example `research.grounded_search.v1`, `schema://oriondesk/research-request/1`, `case_demo`, `2026-11-09T08:00:00Z` does not approve UUID coercion or a schedule. [p.87 c28:f9–f13.]

Runs admit only if workspace tokens, queue age and provider capacity thresholds pass. `429 Retry-After` preserves saved cases. Each run reserves input/output tokens and meters workspace quota; exhaustion is terminal for current run, without automatic model/data-class change. [pp.38,69; c13:f7, c22:f5.]

Plan is DAG depth **≤8**, tool invocations **≤16**, explicit dependencies/replayable checkpoints. Store plan revision before effects and checkpoint each stage before downstream dispatch. Counting retries/depth and runtime limits require confirmation. Triage classifies, Research retrieves, Draft assembles; Policy Evaluator is deterministic, not LLM. [pp.40,49; c14:f1–f5, c16:f7.]

Run catalog: `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED`; checkpoint/runtime guards. Described linear progression includes awaiting review. Missing approval, calls exhausted, repeated invalid plans, policy denial and deadline expiry terminate with exact failed-checkpoint status, but timing versus waiting/expiry/recoverable timeout is **BR-OQ-010**. Do not implement immediate missing-approval failure, implicit approval or example timeout `180`. [pp.12,41,49,82; c5:f12, c14:f11, c16:f7, c26:f3.]

### BR-012–014 Policy, review and publication decisions

Normalize and retain **case sensitivity, requested action, evidence quality, model class, financial impact category and confidence bands** with rule-set version. Digest alone does not replace retained inputs. Maximum included material class among `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` governs routing/redaction/retention/approval, not merely the case label. Class decision rows/unknown class and activation semantics remain **BR-OQ-011**. [pp.44,62,85; c15:f3, c20:f7, c27:f18.]

| Condition/result | Confirmed behavior | Missing decision |
|---|---|---|
| High-impact recommendation | Human review task, not autonomous mutation | Definition/threshold and relation to high-risk |
| Uncertain/sensitive action | Authorized-reviewer routing | Exact eligibility/branch |
| `AUTO_ALLOW` | Valid deterministic outcome | Publication eligibility and bypass path not supplied |
| `HUMAN_REVIEW` | Valid deterministic outcome; apply reviewer gate | Complete assignment/expiry/required fields |
| `REQUEST_MORE_EVIDENCE` | Valid outcome | Rework/retrieval steps and state edges |
| `DENY` | No unauthorized effect/publication | Rework only new run revision; no retroactive approval |
| LLM risk tags | Proposal data only | Cannot override any engine outcome |
| Missing/unsupported citations | Needs-review or unsupported; no fabricated approved response | Branch selection |

Sources: pp.11–12,44–46,89; c5:f1,f10, c15:f1,f4,f12, c30:f9. The table is not an invented complete rule-set: thresholds, precedence and missing-input results remain open.

Review tasks use policy pools, minimum role and separation of duties. **No self approval for approval tasks**; the own-high-risk Analyst prohibition is a specific case, not permission elsewhere. Overrides require elevated role **and secondary reviewer and audited reason**; no exact-hash exception is stated. [pp.11,45–46,85; c5:f4, c15:f8,f12, c27:f12.]

Review catalog `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED`; every transition actor/hash/duties guarded. Present exact artifact, citations, model/prompt version and policy reasons; reviewer must be able to inspect sources before approval. Both Approve/Reject disabled until required fields complete. Required list and mandatory actual-click acknowledgment are not supplied. Record decision, actor, timestamp, evaluated hash, rationale and optional annotations; input rationale requiredness remains open. [pp.45,57–58,82; c15:f8–f9, c19:f1,f7, c26:f5.]

| Attempt | Required result |
|---|---|
| Current matching artifact, independent eligible actor, complete fields | Record decision subject to all current policy/resource guards; not unconditional publication |
| Old/wrong/changed artifact hash | Reject as stale, audit; unchanged accepted business state; API-017 conflict `409` |
| Task expires under configured SLA | Reassign/escalate, record escalation, never implicit approval |
| Denied/rejected work reworked | New run revision, not retroactive approved history |
| Replay old decision for another artifact | Cannot publish different artifact |
| Unapproved high-risk run | No publication |
| Missing required evidence/current permission/policy satisfaction | No final approved publication |

Sources: pp.11–12,45–46,83,87,89; c5:f2,f10, c15:f2,f8,f12,f16, c26:f13, c28:f5, c30:f6,f10. **BR-OQ-013:** Pool/role comparison, hash canonicalization, review fields/SLA/recipient/races/override interface remain unresolved.

Retrieval, generation, policy and reviewer decisions remain separate records. Publication recomputes authorization/current evidence and binds exact artifact. Final response pointer and satisfied gate commit atomically; case/decision/outbox ACID boundary is preserved. Recorded `ApprovalDecisionRecorded` causes **validation**, not unconditional publish. [pp.12,45,52,87; c5:f10, c15:f11,f16, c17:f8, c28:f5.]

### BR-015–016 Transactions, events, recovery and audit

All durable changes propagate `tenant_id`, `revision`, `actor_id`, `occurred_at` and correlation context, conditional on actually changing durable state. Every request carries `trace_id` and `correlation_id`; correlation crosses boundaries independently of provider traces. These are server provenance, not user-editable authority. [Chapter registers pp.8–80; c4:f5 through c25:f8; pp.16,64 c6:f11, c21:f2.]

Events contain exact `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, `payload`, canonical JSON/UTC. Complete types/signing/canonicalization remain open. At-least-once consumers deduplicate event ID/operation key, detect stale revisions, record duplicate outcome and never reapply accepted mutation; no invariant depends on queue partition ordering. [pp.17,48–50 c6:f12, c16:f2,f6,f14.]

| Event | Producer | Selected payload labels | Consumer action |
|---|---|---|---|
| `CaseCreated` | Case Service | Case ID / revision | Run classifier |
| `DocumentNormalized` | Ingestion | Version ID / source hash | Build index |
| `SearchIndexCommitted` | Indexer | Index generation / document revision | Invalidate query cache |
| `AgentPlanApproved` | Orchestrator | Run ID / plan hash | Dispatch steps |
| `ApprovalDecisionRecorded` | Policy Service | Task / actor / content hash | Validate publication |
| `WorkflowStageAdvanced` | Orchestrator | Run / stage / checkpoint | Resume consumers |
| `AccessDenied` | Policy Service | Principal / action / policy digest | Alert enrichment |
| `TenantDeletionVerified` | Retention Worker | Manifest ID / receipt hash | Close purge record |

Source: p.87 c28:f1–f8. Labels are not complete typed JSON keys and events are not automatically SSE types.

Chapter events `BaselineCommitted`, `RunRequested`, `DeploymentPromoted`, `CaseStateChanged`, `ConnectorSyncStarted`, `ModelInvocationCompleted`, `DataRetentionPurgeCommitted`, `ApiCompatibilityVerified`, `UserReviewOpened`, `SecurityPolicyChanged`, `SloBurnRateDetected`, `BackpressureActivated`, `ReleasePromoted`, `EvaluationCompleted` retain register obligations: versioned envelope/outbox, stale/unauthorized mutation rejection, correlated safe log/audit, ledger/revision dedup, current publication recheck and one accepted-transition audit. Producer/cause/SSE mappings not supplied remain unresolved. [Respective registers and failure sections pp.10–80: c4:f15–f18, c5:f15–f18, c6:f14–f17, c7:f14–f17, c9:f11–f14, c10:f15–f18, c13:f15–f18, c17:f14–f17, c18:f14–f17, c19:f16–f19, c20:f13–f16, c21:f14–f17, c22:f14–f17, c23:f14–f17, c24:f14–f17.]

Transient faults use bounded exponential backoff/jitter/per-dependency circuit breakers. Validation/permission faults are permanent and never retried. Mutable retry requires idempotency; consequential effects additionally require human authorization. Operator replay requires reason, dry-run, scope and original event identity except explicit provenance-linked schema migration. [pp.42,49–50 c14:f12, c16:f10–f11.]

Delayed-index recovery: **Detect → Contain → Diagnose → Recover → Verify → Document**. Alert oldest queue age/backlog, identify tenant/generation; pause **only faulty connector/indexer shard** and preserve accepted records; inspect event/outbox/parser/throttle/ACL; replay validated bounded operator-controlled outbox; compare fingerprints/indexed versions and denied probes before closure; link audit IDs/time window/blast radius/quality/prevention. Bounds/closure authority are **BR-OQ-014**. [p.90 c31:f6–f10.]

Audit is append-only, batch-hash chained and independently exported. Operators query, never alter historical decisions; Auditors read redacted decision/prompt-template digest/access lineage, not case-edit authority. One audit record per accepted transition does not suppress separate mandatory denial evidence. Diagnostics exclude user documents/API secrets/full prompts/private existence; default model logging uses digests/tokens. [pp.11,23,54,62,64,84 c5:f5, c8:f9, c18:f2, c20:f8,f10, c21:f1, c26:f22.]

### BR-017–018 Retention, export, usage and period-end processing

| Scope | Confirmed rule/period | Open conditions |
|---|---|---|
| Eligible closed case | Retention selects only eligible closed cases; preserves closure lineage and holds | Eligibility beyond CLOSED, retention class/duration/schedule |
| Diagnostic log | Default TTL **30 days** | Start timestamp, overrides, equality/calendar conventions |
| Security audit | Distinct fictional **seven-year** policy | Corporate selection, years/expiry/hold mechanics |
| Soft-deleted entity | Cannot retrieve; scheduled tombstone final purge | Cadence, tombstone scope/format |
| Legal-hold protected record | Retain and receipt during purge | Hold lifecycle/release/partial completion |
| Export/delete | Two independent approval checks, Admin + approver | Identity independence, binding/expiry/procedure |
| Export package | Checksummed case metadata/approved artifacts/source refs/audit manifests | Snapshot/archive/checksum/download/expiry; excludes secrets/internal prompts |
| Subject request | Shared export/delete inventory | Request procedure and authorized scopes; no extra endpoint supplied |

Sources: pp.26,51,66,78–80,83,89; c9:f10, c17:f4, c21:f12, c25:f1,f6–f7, c26:f19–f20, c30:f13. Single-Admin export fails two-person control (`T-11`). Immutability is not infinite retention, and retained evidence is not continued access permission. **BR-OQ-015** blocks unspecified lifecycle implementation.

**Period-end coverage:** Daily usage rollups are confirmed reporting granularity, not a cron or fiscal-close rule. Model/embedding/storage/index usage is attributed to workspace cost centers and deployment versions; rollups show budget, forecast and rejected excess requests. `token_ledger` retains `run_id`, `deployment_id`, `in_tokens`, `out_tokens`. [pp.65,85 c21:f11, c27:f17.]

| Calculation/period | Confirmed | Needs confirmation — BR-OQ-016 |
|---|---|---|
| Token reservation/metering | Reserve input/output budget per run; track provider usage under workspace quota | Tokenizer, reserve amounts, settlement/refunds, concurrent reservations, provider adjustments |
| Cost | Attributed model/embedding/storage/index usage | Price/rate/currency/unit formula, precision, taxes if applicable, rounding; none approved |
| Daily budget/forecast/excess | Display these daily aggregates | Day timezone/boundary, forecast algorithm, budget period, late events/corrections/rerun settlement, empty day |
| Accounting period end | No close/finalization procedure supplied | Monthly/fiscal close, cutoff, reconciliations, carry-forward and immutability/adjustment policy |
| Quota/admission | Thresholds gate new runs; exhaustion terminal for current run | Values/equality/priority/missing telemetry/effective period |

Do not implement invented accounting close, fixed token price, daily schedule or rounding convention. Routine spend anomalies create owner/threshold tickets; user-impacting failure-budget/ACL/approval incidents may page. Actual owners/values/channels are unspecified. [p.65 c21:f9.]

### BR-019–022 Degradation, presentation, deployment and release

**Safety precedence:** Degraded modes never bypass approval/authorization. Generation outage disables new generation, displays status and preserves manual/evidence work; page on-call only if availability budget impacted. Vector degradation may use visibly reduced-quality lexical retrieval. **Exception:** suspected ACL leakage suspends affected aliases, revokes cached evidence, preserves audit and scoped ACL replay; re-enable search only after negative access tests pass. [pp.68–70,79 c22:f1,f5–f6, c25:f4–f5.]

Every primary screen has one primary action/status summary: SCR-001 Case Queue, SCR-002 Case Detail, SCR-003 Evidence Viewer, SCR-004 Run Timeline, SCR-005 Review Inbox, SCR-006 Connector Health, SCR-007 Policy Settings, SCR-008 Audit Explorer. Accessible draft text `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` is mandatory, not an aggregate enum replacement. Run SSE shows retrieval/generation/policy, reconstructs server progress on refresh, resumes monotonic retained authorized offsets with `Last-Event-ID`. WCAG 2.2 AA, focus/semantic/keyboard order and meaningful transition announcements apply. Server UTC/API RFC3339; display workspace-local labeled timezone, locale cannot change ordering/durable API time. [pp.54–59 c18:f3,f8, c19:f1–f10.]

**BR-OQ-017:** No route, extra screen, alias, mandatory metric formula or five-citation/model default follows from representative views. Cards `128`, `14`, `97.6%`, `Healthy`, `gateway-r1.2`, sample IDs `OD-2026-1042`–`OD-2026-1038` and sidebar Overview/Agent Runs/Connectors/Audit Events/Usage & Quality are fictional. Title/selected-item mismatches persist on pp.7,14,33,43,47,60,67,77,81. [c3:f6–f10, c5:f20–f22, c11:f19–f20, c14:f19–f20, c15:f19–f21, c19:f20–f22, c21:f18–f19, c24:f19–f20, c25:f19–f20.]

Private segmented networks, declared flows, no datastore public IP, managed gateway/private APIs, restricted worker egress, separate service identities and internal TLS/audience/IAM are required. Managed identity substitutes static credentials where supported; secrets/keys are vault references. Rotate keys by policy without request-path bulk reencryption. Staging synthetic/test connectors/isolated spend; no production data in development. [pp.18–20,63 c7:f1–f3,f11, c20:f11.]

| Design assumption/target | Applicable boundary |
|---|---|
| Public API availability `99.9%` monthly | Denominator/exclusions unresolved |
| Case-create P95 within/under `300 ms` | Defined load; equality wording conflict unresolved |
| Search P95 under `1.5 s` | Excludes remote connector fetch; model generation separate |
| `2,000` daily active users; `60` steady/`180` burst requests/s | Reference workload, not client throttle values |
| Maximum `100,000` indexed documents/tenant; `20` concurrent AI runs/large tenant | Reference profile; no automatic admission configuration inference |
| Typical `1 MB` source ~`40–120` chunks | Content/parser dependent, not fixed count; raw/text/vector/replication sized separately |
| RPO `<=15 minutes`, RTO `<=4 hours` | Reference recovery; inclusive boundaries; primary/warm region, incident-command restore |
| Evaluation `1,200` synthetic cases | Permission-controlled expected citations/outcomes across retrieval/refusal/ambiguity/adversarial |
| Citation precision `>=0.97`; unsupported rate `<=0.02`; frozen high-risk recall `1.00` | Equality accepted where explicit; CI/domain shift and low-confidence gate still apply |

Sources: pp.12,65,68–70,75 c5:f12, c21:f8, c22:f2–f8, c24:f8–f9. Measurement definitions, denominators/rounding and confidence/regression formulas are **BR-OQ-018**. Never round a failing raw score into passing absent approved rules.

Continuous PostgreSQL backups and object/index rebuild recipes are tested together; primary writes and secondary restore only under incident command. Chaos covers 429 storms, lost heartbeat, duplicates, object failures and region outage, measuring safety/recovery. [pp.19,69–70 c7:f9, c22:f7–f8.]

Release prerequisites: reconstruct binary/prompt/policy; signed config/vault refs/images/SBOM/allowed-build digest; generated OpenAPI/protobuf and nonbreaking compatibility; nullable additions/bounded backfill/constraints after old reader drain; document new-write readability. Canary compares latency/errors/auth denials/AI quality; regression rolls **traffic/binary**, not DB down-migration; compensation only explicitly supported. Security/SRE validate egress/secrets/backups/alerts before promotion; release binds image/schema/prompt/model-route. Terraform/Bicep remains unselected. [pp.20,52,55,71–73 c7:f12, c17:f9, c18:f11, c23:f1–f12.]

Critical isolation/approval tests allow **zero exceptions**, and unmitigated critical findings block regardless of benchmark score. SEC-001–SEC-012 require independent security-control evidence/reproduction/signature. Prompt/model roll-forward requires reevaluation; low statistical confidence blocks release, not equivalence. Deterministic tests avoid live models, pin adapters and randomized retries leave one outcome. Fixtures synthetic/successful/empty/mixed/adversarial/malformed, seeds recorded, corpora frozen/versioned/independently reviewed and signed release-digest-linked outputs retained. [pp.74–76,88–89 c24:f1–f12, c29:f13–f14, c30:f17–f22.]

## Application Points and Validation Conditions

### Enforcement and data mapping

Source-confirmed service responsibility: gateway authentication/quota; Case Service transactional mutation; Ingestion conversion; Retrieval cited chunks; Orchestrator run state; Policy binding approvals. Orchestrator has no direct DB credentials. Internal calls independently authorize; model providers receive scoped prompts, never connector tokens/DB access. [pp.9,15–16 c4:f12, c6:f2,f8–f11.]

| Rule | Existing application points | Reads/updates and required satisfied/unsatisfied checks |
|---|---|---|
| BR-001 | API-031/032; DAT-021/026; BAT-022 | Baseline decision/impact/test links; reject unapproved change assumptions, preserve migration/version obligations |
| BR-002 | All SCR/API/BAT; API-045/053 | Principal/member/ACL/class/action/duties DAT-024/027; positive authorized, absent/foreign denied, mid-search/publication revocation |
| BR-003 | All storage/jobs; DAT-002–019/023/024; BAT shared guards | RLS/context/parent links; cross-tenant FK attempt denied; pool reuse after success/failure clean |
| BR-004 | SCR-001/002; API-001/003–005; BAT-001/012 | DAT-004/005/025/028; NEW creation, supported edges, correction reason, immutable close lineage; missing edges not auto-selected |
| BR-005 | SCR-002 domain service; DAT-025 | Explicit impact/urgency/calendar; prediction must not alter contract; calculation tests await confirmed formula |
| BR-006 | API-001/004/006/011/017/018/022/024/025 and applicable job POSTs; BAT launch/replay | DAT-029/revision/hash/idempotency ledger; same payload one outcome, changed payload409, stale edit unchanged; 24h boundary pending |
| BR-007 | SCR-002/003; API-006/007; BAT-003/004 | DAT-006–008/025/030; safe format accepted, unsafe no-index, low-quality viewable/nonautonomous, anchors current/resolvable |
| BR-008 | SCR-006; API-018/019/050; BAT-002/006/015/020 | DAT-006/016/025; warning, revoked credential failure, durable cursor, quarantine exception/partial continuation |
| BR-009 | SCR-003/005; API-008–010/047/052; BAT-004–007/009 | DAT-008/011/025/030; ACL before text, verified citation, no-support result, checked alias/readiness and fingerprint recovery |
| BR-010 | SCR-007 context; API-028/036/051; BAT-007 | DAT-025–027/registry/prompt/attempt; approved route, equal-handling fallback, invalid-output no publish, injection not authority |
| BR-011 | SCR-004; API-011–015/037/047/048; BAT-007 | DAT-009/010/025/035; bounded DAG/checkpoints, arbitrary toolDENY, 10/11 MCP boundary, no equivalent-tool bypass |
| BR-012 | SCR-005/007; API-017/046; BAT-007/009 | DAT-018 normalized inputs/rule/result; reproducible policy, LLM proposal cannot override; full decision rows pending |
| BR-013 | SCR-005/003; API-016/017; BAT-008/009 | DAT-012/013/028; independent actor/exact hash/required fields; stale rejection/audit; expiry escalation/no approval |
| BR-014 | SCR-002/004/005; API-017/046; BAT-009 | DAT-004 pointer/011 evidence/012–013 decisions/018 gate/outbox; atomic current supported artifact only, replay wrong artifact denied |
| BR-015 | API-037/038/046/049; BAT-005/007/010/011/016 | DAT-015/029/034/checkpoints; duplicates/stale order safe, permanent errors no retry, validated scoped replay, webhook no rollback |
| BR-016 | SCR-008; API-020/041/053; BAT-010/017/019 | DAT-013/014/026/031; append-only/redacted safe audits; denied trace no private existence/content/secrets |
| BR-017 | API-005/024/025/030/040; BAT-012–014/019 | DAT-019/026/031/033; eligible closed selection, held retained/receipted, two-person export, excluded secret/prompt package |
| BR-018 | API-021/036/042/051; BAT-007/018 | DAT-017/018/025/026; attributed usage/quota terminal/daily outputs; numeric/period close tests await confirmation |
| BR-019 | All affected SCR; API-033; BAT-006/007/009/011 | DAT-025/030; degraded manual/evidence retention, lexical flag, affected ACL aliases suspended until negative probes |
| BR-020 | SCR-001–008; API-002/010/015/017 | DAT-033/view state; accessible truthful text/source highlight/server refresh/locale-invariant ordering |
| BR-021 | API-034/035/045; BAT-020/023 | DAT-001/026/032; private routes/separate identities/vault, controlled restore and reference RPO/RTO |
| BR-022 | API-022/023/043/044; BAT-021/022/023 | DAT-026/032/036; signed reconstructible evidence, zero-exception safety, score/CI gates, compatibility/rollback |

No mapping authorizes missing UI controls or exposes internal APIs to browsers. API inventory chapter-only omissions are not exclusions.

### Shared registers and qualification

For every chapter component, verification includes positive, foreign-tenant denial, duplicate/replay and evidence-retention tests; published event is correlated in logs/audit without source text. This applies across all named component records retained in DAT-021, not only selected SQL tables. [Repeated verification pp.8–80: c4:f8, c5:f8, c6:f6, c7:f6, c8:f12, c9:f4, c10:f6, c11:f11, c12:f5, c13:f12, c14:f7, c15:f7, c16:f5, c17:f7, c18:f7, c19:f13, c20:f6, c21:f6, c22:f11, c23:f7, c24:f7, c25:f10.]

Register classifications remain exact scoped references: `Owner aggregate / UUIDv7 + tenant scope`, `Immutable derivative / SHA-256 source/ revision`, `Policy-bound control / Actor and role predicate`, `Operational ledger / Event ID + trace context`. They do not create application `Owner` grants, physical tables or universally SHA-256 hashes. Specific mutable case/task/alias/form/checkpoint behavior remains confirmed while inconsistent register scope requires amendment. Full per-chapter records are preserved in [03_data.md](03_data.md) DAT-021; source evidence is pp.10–80 register findings c4:f14, c5:f14, c6:f13, c7:f13, c8:f13, c9:f11,f16, c10:f14, c11:f13, c12:f12, c13:f14, c14:f13, c15:f13, c16:f12, c17:f13, c18:f13, c19:f15, c20:f12, c21:f13, c22:f13, c23:f13, c24:f13, c25:f12.

Generic API/register validation-before-allocation, OAuth audience/idempotency, schema/bounded-error and event/outbox duties remain retained. Their GET/health/OpenAPI/member/workspace/lifecycle associations do not authorize invented mutations. Resolve each causal mapping under **BR-OQ-019**. [Relevant interface findings c4:f6–f7,f15, c5:f7,f15, c6:f4–f5,f14, c7:f5,f14, c8:f11,f14, c9:f3,f11, c10:f4–f5,f15, c11:f9–f10,f14, c12:f4,f13, c13:f10–f11,f15, c14:f4,f6,f14, c15:f6,f14, c16:f4,f13, c17:f6,f14, c18:f6,f14, c19:f12,f16, c20:f5,f13, c21:f5,f14, c22:f10,f14, c23:f5–f6,f14, c24:f5–f6,f14, c25:f9,f13,f18.]

### Concrete acceptance matrix

| Source test / rules | Procedure | Required result |
|---|---|---|
| TST-001 / BR-004,006 | Authorized valid case create twice, same key/body | One case, identical response |
| TST-002 / BR-006 | Reuse key changed body | `409 IDEMPOTENCY_CONFLICT`, no second accepted outcome |
| TST-003 / BR-002 | Foreign-tenant case read | `404`-equivalent non-disclosing error |
| TST-004 / BR-002,009 | Index, revoke, query next | No forbidden evidence |
| TST-005 / BR-010,014 | Force model schema failure | `MODEL_OUTPUT_INVALID`; no publish |
| TST-006 / BR-013,014 | Wrong/prior artifact hash decision | Stale rejection, audited, unchanged accepted state |
| TST-007 / BR-006,015 | Replay accepted outbox | Exactly one accepted business transition |
| TST-008 / BR-008,018,019 | Provider429burst | Capped retry/controlled admission; values pending |
| TST-009 / BR-009,012,014 | Missing citations | Needs-review or unsupported; branch pending, never fabricated approval |
| TST-010 / BR-013 | Expire configured task | No implicit approval; escalation recorded |
| TST-011 / BR-020 | Keyboard-only case opening | No blocked action, visible focus |
| TST-012 / BR-021 | Reference region recovery | RPO≤15min/RTO≤4h, object/relational/index checks |
| TST-013 / BR-017 | Held tenant purge | Protected records retained/receipted |
| TST-014 / BR-011 | Arbitrary MCP invoke | `DENY` before dispatch |
| TST-015 / BR-007 | Unsafe PDF | Quarantine/no index |
| TST-016 / BR-022 | Canary safety regression | Promotion blocked |

Source: p.89 c30:f1–f16; recovery p.69 c22:f7. Test missing schema/threshold decisions only after confirmation; tests cannot silently choose them.

Appendix D negative pack: `T-01` foreign-token valid IDs/RLS+domain guard; `T-02` hostile PDF/evidence delimiting+schema pinning; `T-03` revised-artifact old approval; `T-04` polyglot/zipped scan/sandbox/bounded parser; `T-05` vault/trace/provider credential observation; `T-06` regional unapproved fallback; `T-07` same event **100 replays**; `T-08` mid-search revoke; `T-09` historical audit edit; `T-10` recursive tool hints/budgets; `T-11` single-Admin export/two-person manifest; `T-12` replaced expected fixtures/version+signed manifest. ZIP is an attack, not supported upload;100 is test count, not runtime retry allowance. [p.88 c29:f1–f14.]

Additional acceptance executes authorized independent create→ingest→retrieve→draft→review→publish, rejected new-revision rework, poison quarantine and foreign denial. Inspect exact candidate/sources/model/prompt/policy; test permission change between retrieval/publication, transaction pool reset success/failure, partial sync ledger/cursor, low-quality viewability, failed-index fingerprint repair, approved alias coverage, scoped replay, held receipts, source click highlight, SSE refresh, secret-free diagnostics and reconstructible release/reader compatibility. [pp.12,22–32,45–59,75,78–80,86,90; affected rule citations above, c24:f11, c27:f26–f27, c31:f6–f10.]

## Consistency and Open Questions

### Required clarifications and amendments

Do not rewrite completed files. Record amendments against the following existing identifiers and BR rules. No unresolved choice constitutes implementation discretion.

| Open ID / rules | Evidence/conflict and required decision | Earlier dependencies |
|---|---|---|
| BR-OQ-001 / BR-001 | Impact-score formulas/approval/effective revision and major/minor overlap p.8; source IDs/namespaces not arbitrary mappings | API-031/032; DAT-026; BAT-022 |
| BR-OQ-002 / BR-002,003 | Roles/personas/scopes pp.11/22/83; missing identity provider/session/allowed token claims; RLS roles/context and FK/procedure choice p.86 | SF-002/OQ-001, SF-003/OQ-002; API-OQ-001/002/017; DAT-OQ-003; BAT-OQ-001 |
| BR-OQ-003 / BR-004 | Close incoming/reopen target/actor/interface and field/correction predicates missing pp.12/25–26/82 | SF-006/OQ-009; DAT-OQ-009; API-OQ-008 |
| BR-OQ-004 / BR-005 | Priority/calendar/rounding/missing inputs p.25 unprovided | SCR-002/SF-006/OQ-009; DAT-025 |
| BR-OQ-005 / BR-006 | Key scope/fingerprint/locking/missing headers/exact24h expiry pp.25/54; no automatic stale edit merge | API-053/API-OQ-003/013; DAT-029; BAT-OQ-003 |
| BR-OQ-006 / BR-007 | Cap MB/equality/decompression/quality/OCR/hash/anchor formats pp.30–32; permitted low-quality manual use unresolved | SF-007/OQ-010; API-OQ-011/015; DAT-OQ-007/014; BAT-OQ-009 |
| BR-OQ-007 / BR-008 | Capability trust effects, poison continuation/status, cursor races/retry/fairness/empty delta pp.27–29 | SF-011/OQ-013; API-OQ-012; DAT-OQ-006/014; BAT-OQ-003/005 |
| BR-OQ-008 / BR-009 | Fusion/rerank/ties/diversity/token/coverage/completeness/recall and insufficiency branch missing pp.34–36/78 | API-OQ-011/015/016; DAT-OQ-007/014; BAT-OQ-009 |
| BR-OQ-009 / BR-010,011 | Registry classes/order, redaction, parse bounds, tool/A2A formal schemas/adapter/authorization missing pp.37–42/62/87 | API-OQ-015/017; DAT-OQ-005/016; BAT-OQ-005/009 |
| BR-OQ-010 / BR-011–014 | Missing approval terminates p.41 vs AWAITING_REVIEW p.49/82 and expiry p.45; recoverable timeout p.12 vs FAILED catalog; AUTO_ALLOW p.44 vs linear workflow | SF-009/OQ-008; API-OQ-009; DAT-OQ-008; BAT-OQ-004; sources c14:f11,c16:f7,c15:f8,c5:f12,c26:f3 |
| BR-OQ-011 / BR-012 | High-impact/high-risk thresholds, financial/confidence units/normalization, maximum-class rows, priorities and policy activation/in-flight/grandfathering missing pp.44/62 | SCR-007/SF-012/OQ-011; DAT-018/025; API-OQ-006 |
| BR-OQ-012 / BR-006,015,016 | p.22 reject before AccessDenied vs mandatory safe audit pp.23/87 and stale approval p.89; clarify event order/revision/commit without suppressing denial | SF-016/OQ-015; API-OQ-013; DAT-OQ-012; BAT-OQ-006; c8:f7,f9,c28:f7,c30:f6 |
| BR-OQ-013 / BR-013,014 | Required fields/rationale/hash/pools/self-principal/secondary independence/SLA/race/escalation/override transport pp.45–46/58/85 | SF-010/OQ-012; API-OQ-008; DAT-OQ-009/010; BAT-OQ-003/004 |
| BR-OQ-014 / BR-015 | Retry/jitter/circuit/replay/lease limits, event/SSE retention/offset expiry/webhook age-signature, no-input/partial outcome missing pp.48–55/90 | API-OQ-010/012/013; DAT-OQ-013; BAT-OQ-003/005 |
| BR-OQ-015 / BR-017 | Closed eligibility/retention/corporate policy, hold lifecycle/receipts/independent approver/export formats missing pp.26/66/78–83 | SF-017/OQ-016; API-OQ-014/017; DAT-OQ-015/016; BAT-OQ-008 |
| BR-OQ-016 / BR-018 | Cost/token/forecast/quota formulas, units/rounding/late settlement, daily timezone/boundary and period-end close absent pp.38/65/69 | DAT-026; API-021; BAT-018/BAT-OQ-010 |
| BR-OQ-017 / BR-020 | Eight primary screen names vs fictional aliases/title mismatches; route/action/status/time formatting/SSE/focus specifics missing | SF-004/OQ-003/004/005/008; API-OQ-018; DAT-OQ-017 |
| BR-OQ-018 / BR-019,021,022 | within300 p.12 vs under300 p.65; load/SLO/recovery/CI/low-confidence/regression formulas absent; thresholds not approved | SF-OQ-017; API-OQ-016/019; DAT-OQ-018/020; BAT-OQ-005/010 |
| BR-OQ-019 / BR-001,004,011,015 | POST /v1/runs vs case-run; workspace config/case PATCH; repeated GET/health allocation/events and provisioning/export-delete association | API-OQ-005/006/007/019; DAT-OQ-004/011; BAT-OQ-007; source respective register/interface citations above |
| BR-OQ-020 / BR-003,004,008,009,013,020 | Mutable case pp.24–25 vs immutable registers pp.13/17/26; membership/sync/alias/task/form immutable labels vs update/lifecycle | SF-006/OQ-009; API-OQ-006/012; DAT-OQ-002/010; BAT-OQ-006; c5:f14,c6:f13,c9:f11,f16,c8:f13,c10:f14,c12:f12,c15:f13,c19:f15 |
| BR-OQ-021 / BR-001,010,017,021 | Dated region/search/identity/model/corporate retention/connector choices before implementation lock p.90; key isolation/rotation before enterprise GA p.10 | SF-OQ-018; API-OQ-017; DAT-OQ-019; BAT-OQ-011; c31:f11,c4:f13 |

Specific domain evidence confirms mutable current cases and immutable revisions/evidence/approved lineage, but inconsistent register text still requires amendment. Task-wide no-self-approval qualifies the own-high-risk Analyst clause; it is not weakened by the narrower example. Eventual index consistency is never an ACL timing exception. Hold protection, poison-record continuation, low-quality viewability, failed-index durability and ACL incident containment are explicit exceptions, not defects to remove.

### Configuration/example status

Appendix F p.90 examples retain exact values: `release: r1.0`; `max_plan_depth: 8`, `max_tool_calls: 16`, `run_timeout_seconds: 180`, `replay_dedup_hours: 24`; `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `embed_dimension: 1536`, `hybrid_rrf_k: 60`; `auto_publish_classification: INTERNAL`, `require_human_review_for: [HIGH_RISK, RESTRICTED]`, `self_approval_allowed: false`; `upload_limit_mb: 25`, `user_data_region: primary-approved-region`; `trace_sample_rate: 0.10`, `diagnostic_retention_days: 30`, `audit_retention_years: 7`. [c31:f1–f5,f12.]

Independent chapter support confirms depth8/calls16, dimension1536, configurable25MB, actor/fingerprint24hours and substantive no-self-approval/diagnostic/audit rules **only in their stated scopes**. Timeout180/candidates80/global selected10/RRF60/sample0.10/auto-publishINTERNAL/placeholderregion remain examples, not selected requirements. MCP ten is tool-specific. DDL defaults remain persistence-only. Earlier repetition does not approve proposals or fill missing decision rows.

### Dependencies and consolidation

This is Stage 5; prior completed specifications remain unchanged. Remaining exception-handling and architecture details are **To be defined in a later stage**. No later result is presumed. Stage 8 must consolidate BR/BR-OQ and prior linked identifiers in `08_architecture_decision.md`, linking `05_business_rules.md` and the affected earlier filenames. It must not invent a decision, owner, deadline, region/provider or approval. This specification is provisional pending separate root approval.
