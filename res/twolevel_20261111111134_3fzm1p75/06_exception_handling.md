# 6. Exception Handling Specification

## Exception Inventory and Classification

### ERR-000 — Authority, provenance and interpretation

**Confirmed.** This is Stage 6/8, `06_exception_handling.md`, for OrionDesk AI, `OD-AI-DDS-001`, `R1.0 / revision 1.3`, a controlled fictional reference architecture. It integrates the supplied section judgments; it does not claim a fresh inspection of attachments. The candidate remains provisional pending evidence review. **Confirmed** means supported for the reference system; **Needs confirmation** identifies incomplete implementation contracts. No new **Proposal** is selected.

All current citations below refer to **1794363094-OrionDesk_AI_Detailed_Design_Specification.pdf**, abbreviated **Current PDF**, with original pages and finding IDs. Earlier files cite **1794353355-OrionDesk_AI_Detailed_Design_Specification.pdf**. Matching identity/revision does not prove file equivalence; do not relabel their citations. “All numbers are design assumptions, not measured production performance.” Figures illustrate normative boundaries, not generated implementation artifacts. [Current PDF pp.1–2,8 §1.1; `exception_handling:r1:c1:f1`, `exception_handling:r1:c1:f2`, `exception_handling:r1:c2:f1`, `exception_handling:r1:c2:f2`, `exception_handling:r1:c6:f5`]

`ERR-*` identifiers are specification traceability identifiers, **not newly invented production error codes**. Existing literals take precedence. Links to [01_screen_functions.md](01_screen_functions.md), [02_api.md](02_api.md), [03_data.md](03_data.md), [04_batch_functions.md](04_batch_functions.md) and [05_business_rules.md](05_business_rules.md) are mappings, not independent evidence. API paths are not browser routes; batch responsibilities are not selected executable decomposition.

For **every exception**, unspecified HTTP status, business code, message, field schema, screen/durable state, severity, recipient, retry count/delay, timeout, corrected-rerun permission and compensation is **Needs confirmation**. Do not interpret an omission as authority to choose a production contract.

### Inventory and enforcement mappings

Categories below are analytical classification, not a source error enum. Each row inherits ERR-000 and the shared handling rules.

| ID / source identifier | Detection and occurrence | Category / affected scope | Earlier implementation mappings |
|---|---|---|---|
| ERR-001 / CASE_VERSION_CONFLICT | Submitted If-Match differs from current case revision | Business/concurrency; rejected case update | SCR-002; SF-007/017; API-005/049/056; DAT-010/014; BAT-022; BR-004/014 |
| ERR-002 / IDEMPOTENCY_CONFLICT | Same key reused with changed body/fingerprint | Invalid reuse; case creation or stated long-job POST scope | SCR-001/002/004; API-003/044/049; DAT-010; BAT-001/022; BR-004/014 |
| ERR-003 / duplicate execution | Identical request or repeated event/operation identity; stale/delayed aggregate revisions | Coordination; all applicable requests/consumers | API-048/053; DAT-014/018; BAT-010/011/022; BR-014 |
| ERR-004 / schema-invalid request | Server payload/schema validation fails before transaction/allocation | Invalid input; public APIs | SF-006; API-043/048/056; DAT-014; BAT-022; BR-014 |
| ERR-005 / authentication failure | Unexpected token algorithm or missing tenancy claim | Authentication; gateway and requests | All SCRs; SF-003; API-002; DAT-009; BAT-022; BR-003 |
| ERR-006 / permission or tenant violation | Role/resource/workspace/ACL/action/separation fails; foreign resource substitution | Permission; edge, transaction, retrieval, dispatch, publication | API-002/048/050/052; DAT-005/009; BAT-022; BR-003 |
| ERR-007 / attachment admission or unsafe content | Type/signature mismatch, file over configurable cap, bomb condition, malicious scan/parser input | Invalid/hostile input; ingestion | SCR-003; SF-008; API-006/049; DAT-011; BAT-004; BR-006 |
| ERR-008 / extraction quality or provenance gap | Low quality, missing/unresolvable anchor, citation verification fails | Evidence quality; viewing versus autonomous use | SCR-003/004/005; API-021–023/049/050; DAT-007/011; BAT-004/007; BR-006/008 |
| ERR-009 / connector capability gap | Unsupported list/fetch/delta cursor/ACL/delete | Integration trust; connector ingestion | SCR-006; SF-011; API-011/050; DAT-011; BAT-002; BR-007 |
| ERR-010 / CONNECTOR_REAUTH_REQUIRED | Credential revoked while connector job queued | Credential/permission; queued sync work | SCR-006; API-050/056; DAT-011/015; BAT-002/018; BR-007/015 |
| ERR-011 / partial or poisoned sync | Partial batch; malformed document reaches bounded-retry quarantine | Integration/item failure; cursor and remaining batch | SCR-006; API-011/050; DAT-011; BAT-002/003; BR-007 |
| ERR-012 / NO_SUPPORTED_EVIDENCE | Retrieval confidence OR evidence quality insufficient | Unsupported result; grounded workflow | SCR-003/004; API-050/051/056; DAT-012; BAT-007; BR-008 |
| ERR-013 / MODEL_OUTPUT_INVALID | Versioned model JSON has unknown fields, invalid citations or control-character injection | Model validation; no publication | SCR-004; SF-009; API-037/051; DAT-012; BAT-007; BR-009 |
| ERR-014 / hostile evidence or arbitrary tool / DENY | Evidence attempts authority change; arbitrary/unapproved tool, forged arguments or denied equivalent action | Permission/safety; orchestration/dispatch | SCR-004; API-046/051; DAT-012; BAT-007; BR-002/010 |
| ERR-015 / budget, invalid plan, deadline or timeout | Call/token budget exhaustion, repeated invalid plans, missing approval, denial or deadline | Workflow stop; applicability unresolved | SCR-004; API-051; DAT-012; BAT-007; BR-009/010 |
| ERR-016 / provider unavailable or throttled | Provider outage/429, admission thresholds unsatisfied | External/capacity; existing versus new runs | SF-014; API-051/055; DAT-017; BAT-007/023; BR-009/018 |
| ERR-017 / stale or unauthorized review | Wrong/changed artifact hash, ineligible/self reviewer, incomplete required inputs | Review; decision controls and records | SCR-005; SF-010; API-010/052; DAT-013; BAT-008/009; BR-012 |
| ERR-018 / review expiry or denied rework | Configured SLA expires; recommendation denied | Review lifecycle/recovery | SCR-005; API-052; DAT-013; BAT-008/009; BR-012/013 |
| ERR-019 / publication gate failure | Missing required evidence/policy/approval; current permissions changed after search | Publication permission/business rule | SCR-004/005; API-052; DAT-009/013; BAT-009; BR-013 |
| ERR-020 / unavailable dependency | Named interface dependency unavailable | External/internal; documented response or durable accepted work | All applicable API rows; API-043; DAT-018; BAT-OQ-011; BR-014 |
| ERR-021 / index/link failure or ACL incident | Failed index write, broken outbox link, delayed index, stale visibility/suspected leak | Derived-state/internal/security | SCR-003/006 and operations; API-054; DAT-011/017; BAT-005/006/011; BR-008/018 |
| ERR-022 / observation or delivery failure | SSE disconnect/history gap; object/URL access failure; optional webhook failure | Observation/integration, not execution authority | SCR-003/004; API-009/040/047; DAT-007/018; BAT-021/023; BR-019 |
| ERR-023 / incomplete provisioning | Setup workflow incomplete or coverage inadequate | Operational prerequisite; sync/search readiness | SCR-006; API-050; DAT-017; BAT-003/012; BR-018 |
| ERR-024 / controlled exit failure or legal hold | Independent approvals fail; protected records held; purge/export partial | Permission/retention; controlled exit | API-016/017/041/054; DAT-016; BAT-013/014; BR-016 |
| ERR-025 / audit, key, configuration or storage integrity | Historical-edit attempt, vault/rotation fault, integrity/context/precondition violation | Security/internal; exact fault responses open | SCR-007/008 and operations; API-048/054; DAT-005/015/016; BAT-017/018; BR-003/005/015 |
| ERR-026 / release or evaluation failure | Invalid build/config/evidence, safety regression, low confidence, critical isolation/approval finding | Release gate, not product-run error | API-055/057; DAT-017/019; BAT-016/019/024; BR-020 |
| ERR-027 / regional or worker/object failure | Primary outage, lost worker heartbeat, object access failure | Resilience; safety/time measurement and scoped recovery | API-055/057; DAT-017; BAT-020/024; BR-018 |

Inventory detection evidence is expanded beside handling below. No additional screen, endpoint or job is established by these categories.

## Handling by Exception

### ERR-028 — Shared validation, authority and interruption rules

1. Bind authenticated principal and tenant. Apply role, workspace membership, sensitivity, originating ACL, action and separation at applicable edge, transaction, retrieval, tool and publication boundaries. Navigation hiding is not authorization.
2. Validate before transaction entry, again at domain invariants, before tool dispatch and before long-work allocation. Client validation is convenience only.
3. Reject stale/unauthorized business writes before their relevant event publication; leave business state unchanged. Denial audit and duplicate ledger evidence are not accepted business mutations.
4. Preserve the stated local ACID mutation/decision/outbox boundary or explicitly reconciled saga. Do not create a global workflow transaction or assume every case mutation creates an approval decision.
5. Never represent partial processing as an approved answer. Oversized uploads, injection, foreign IDs, stale decisions and ungrounded recommendations fail closed with stable non-sensitive codes.
6. Degraded/recovered operation never bypasses authorization or approval.

[Current PDF pp.7,13 §2.3.2,22–23 §§5.2–5.3,17 §3.3,52 §14.2,56 §15.3,68 chapter19; `exception_handling:r1:c4:f4`, `exception_handling:r1:c14:f6`, `exception_handling:r1:c14:f7`, `exception_handling:r1:c31:f2`, `exception_handling:r1:c32:f7`, `exception_handling:r1:c20:f7`, `exception_handling:r1:c85:f1`, `exception_handling:r1:c92:f6`, `exception_handling:r1:c113:f1`]

**Confirmed exclusions:** physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing, agent cloud administration and application-hosted GPU inference. Deferred active/active mutation, beyond-English OCR and customer-managed weights are not recovery alternatives. The orchestrator has no direct DB credentials. Datastores remain private and service identities distinct. [Current PDF pp.9–10,18–19; `exception_handling:r1:c7:f1`, `exception_handling:r1:c8:f1`, `exception_handling:r1:c8:f6`, `exception_handling:r1:c24:f1`, `exception_handling:r1:c24:f5`, `exception_handling:r1:c25:f2`]

### ERR-001–006 — Request conflicts, duplicate execution and access denial

| Condition | Confirmed response/effect | Retry and recovery boundary |
|---|---|---|
| Case If-Match mismatch | **409 CASE_VERSION_CONFLICT**, current revision; rejected business state unchanged | Example retryable:false; refresh/merge/corrected resubmission and missing/malformed header handling Needs confirmation |
| Identical same-key case creation | One case and identical response | Actor/request-fingerprint outcome maps for **24 hours**; key generation, atomicity and expiry rules open |
| Same key with changed case body | **409 IDEMPOTENCY_CONFLICT** | No duplicate case success; safe correction/new-key procedure open |
| POST mutation creating long-running job repeated identically | Requires **Idempotency-Key**; original operation returned | Changed fingerprint returns IDEMPOTENCY_CONFLICT; general status/window beyond specific case test open |
| Schema-invalid REST request | **422** | Code/details/correction open; permanent validation failure not automatically retried |
| Unexpected token algorithm/missing tenant claim | Gateway rejects | HTTP/code/session recovery open; do not invent401 |
| Permission violation | Reject under applicable predicate; no business mutation | Permanent permission failure not retried; no universal403 |
| Foreign-tenant substitution | Same absent-ID not-found response class; foreign-case test **404-equivalent non-disclosing** | Do not disclose existence; safe denial audit retains principal/resource class |

[Current PDF pp.21,23,25,54,83–84,89; `exception_handling:r1:c30:f1`, `exception_handling:r1:c32:f7`, `exception_handling:r1:c32:f8`, `exception_handling:r1:c37:f4`, `exception_handling:r1:c37:f5`, `exception_handling:r1:c37:f6`, `exception_handling:r1:c90:f2`, `exception_handling:r1:c90:f5`, `exception_handling:r1:c137:f8`, `exception_handling:r1:c137:f21`, `exception_handling:r1:c141:f1`, `exception_handling:r1:c141:f2`, `exception_handling:r1:c141:f3`]

**Reference envelope, exact example — not a complete universal schema:**

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "error": {
    "code": "CASE_VERSION_CONFLICT",
    "message": "Case revision no longer matches.",
    "correlation_id": "trace_01HZZ_EXAMPLE",
    "retryable": false,
    "details": {"expected_revision": 7, "actual_revision": 8}
  }
}
```

`error/details` are demonstrated objects; code/message/correlation_id strings; retryable boolean; revisions integers. Placeholder ID/7/8 are not limits. Universal requiredness, additional details and trace aliases remain **Needs confirmation**. Preserve uppercase literals despite “stable snake-case” prose. [Current PDF pp.54,82,84; `exception_handling:r1:c90:f1`, `exception_handling:r1:c137:f1`, `exception_handling:r1:c137:f21`]

**Event duplication procedure:**
1. Use event ID/operation key, event ledger and aggregate revision as applicable.
2. Detect stale/delayed revisions without depending on cross-partition ordering.
3. Record duplicate outcome and return without mutation reapplication.
4. Keep one accepted business transition and its audit evidence; do not suppress duplicate records.

The concrete rule applies to `BaselineCommitted`, `CaseCreated`, `RunRequested`, `DeploymentPromoted`, `AccessDenied`, `CaseStateChanged`, `ConnectorSyncStarted`, `DocumentNormalized`, `SearchIndexCommitted`, `ModelInvocationCompleted`, `AgentPlanApproved`, `ApprovalDecisionRecorded`, `WorkflowStageAdvanced`, `DataRetentionPurgeCommitted`, `ApiCompatibilityVerified`, `UserReviewOpened`, `SecurityPolicyChanged`, `SloBurnRateDetected`, `BackpressureActivated`, `ReleasePromoted`, `EvaluationCompleted` and `TenantDeletionVerified`. At-least-once delivery remains; ledger algorithm/atomicity/retention and stale nonduplicate outcome require confirmation. [Current PDF chapter failure sections §§1.5–22.5, pp.10–80; core semantics pp.17,48–50; `exception_handling:r1:c20:f6`, `exception_handling:r1:c78:f5`, `exception_handling:r1:c82:f1`, `exception_handling:r1:c82:f3`, `exception_handling:r1:c141:f7`]

### ERR-007–011 — Ingestion and connector failures

| Condition | Confirmed interruption/continuation and retained data | Open recovery contract |
|---|---|---|
| Unsupported/mismatched/oversized/bomb input | Admit only PDF/DOCX/HTML/UTF-8 text; MIME signature/extension agree; configurable **25 MB/file** and bomb protection | MIME literals/MB/equality/bomb metric, HTTP/code and rejected-file retention |
| Unsafe attachment | Scan before parse; macros disabled; embedded remote references not fetched; **quarantine, no indexing** | Scanner outage versus unsafe verdict, parser timeout, quarantine remediation/release |
| Low extraction quality | Authorized document remains viewable, excluded autonomous recommendations | Quality thresholds/state/index eligibility; not automatically unsafe quarantine |
| Missing anchor/citation verification | Generation cites only resolvable stored anchor AND current permission; citations verify before display | Error code/state, repair and human handling; optional chunk bbox absence alone is not failure |
| OCR fallback | Opt-in, provenance-marked; normalization never rewrites claims; revised derivatives may coexist | Opting actor/trigger/marker and authorized rerun |
| Missing connector capability | Lower-trust ingestion plus explicit visible warning | Warning copy/restrictions; no ACL bypass |
| Revoked queued credential | **CONNECTOR_REAUTH_REQUIRED**, no tokens | Status/retryability/reauth/rerun and running-job effects |
| Partial batch | Cursor only advances after durable preceding ingestion outcomes; retry safely | Atomic outcomes, batch completion, partial receipts |
| Malformed item after bounded retries | Quarantine with reason code/correlation/remediation; remaining batch **may** proceed with cursor-ledger exception | Retry classification/bounds, continue/stop choice; exception does not automatically authorize cursor advancement |
| Source deletion/ACL change | Tombstone/scheduled index removal; invalidate cache before new results and before next retrieval; stale visibility security incident | Cleanup schedule/in-flight mechanism/incident recipients |

[Current PDF pp.27–32 §§7.1–8.3,88–89; `exception_handling:r1:c42:f1`, `exception_handling:r1:c42:f4`, `exception_handling:r1:c43:f1`, `exception_handling:r1:c43:f5`, `exception_handling:r1:c44:f1`, `exception_handling:r1:c44:f5`, `exception_handling:r1:c44:f6`, `exception_handling:r1:c48:f1`, `exception_handling:r1:c48:f4`, `exception_handling:r1:c49:f1`, `exception_handling:r1:c49:f2`, `exception_handling:r1:c49:f7`, `exception_handling:r1:c50:f1`, `exception_handling:r1:c50:f6`, `exception_handling:r1:c140:f4`, `exception_handling:r1:c141:f15`]

Quality indicators are empty-page ratio, unknown-character ratio, table-loss indicators and language confidence. PDF block bboxes and optional chunk bboxes have different granularity. ZIP/polyglot are hostile test inputs, not added admitted formats. Connector workers honor Retry-After, exponential backoff/jitter, workspace quotas and fair scheduling. **Needs confirmation:** classify malformed retries against permanent validation nonretry; retain both rules pending resolution.

### ERR-012–016 — Grounding, model/tool failures and workflow stops

1. **Unsupported evidence:** insufficient confidence **OR** quality returns `NO_SUPPORTED_EVIDENCE`, never fabricated context. Clarification **OR** human route is permitted but unselected. Missing citations separately yield needs review **OR** unsupported; do not silently choose a durable enum.
2. **Invalid structured model output:** bounded versioned-JSON parsing rejects unknown fields, invalid citations or control-character injection as `MODEL_OUTPUT_INVALID`; forced schema failure must not publish. Parsing counts and overlap with missing/unsupported citations remain open.
3. **Injection/authority:** delimit untrusted evidence, strip tool directives, record indicators, preserve provenance and allowlisted/pinned schemas. Model text and discovery never authorize. An indicator alone is not explicitly a universal run-stop predicate; an authority violation must fail closed.
4. **Tool dispatch:** validate approved MCP arguments with scoped identity; every external write needs separate capability; mutable calls require idempotency and consequential human authorization. Arbitrary invocation is `DENY` **before dispatch**. No semantically equivalent denied-tool workaround.
5. **Plan bounds:** DAG depth **8**, maximum **16 tool invocations**, explicit dependencies/replayable checkpoints; persist plan revision before side effects and stage checkpoint before downstream dispatch.
6. **Stops:** missing approval, exhausted calls, repeated invalid plans, policy denial or deadline terminate and show **exact failed checkpoint**. Token quota exhaustion is terminal for current run with no automatic model/data-class change.
7. **Provider recovery:** select only specific approved deployments; fallback requires approved equal-or-stronger handling, with no restricted content routed to unapproved region/deployment on outage. Fallback cannot evade quota.
8. **Admission:** workspace tokens, queue age and provider capacity must satisfy thresholds; throttled clients receive **429 plus Retry-After**, while saved cases remain available.

[Current PDF pp.35–42,49,69,87,89; `exception_handling:r1:c56:f6`, `exception_handling:r1:c56:f7`, `exception_handling:r1:c60:f1`, `exception_handling:r1:c60:f5`, `exception_handling:r1:c61:f6`, `exception_handling:r1:c62:f2`, `exception_handling:r1:c62:f7`, `exception_handling:r1:c66:f6`, `exception_handling:r1:c67:f1`, `exception_handling:r1:c68:f1`, `exception_handling:r1:c68:f2`, `exception_handling:r1:c68:f8`, `exception_handling:r1:c68:f9`, `exception_handling:r1:c79:f1`, `exception_handling:r1:c115:f1`, `exception_handling:r1:c141:f5`, `exception_handling:r1:c141:f9`, `exception_handling:r1:c141:f14`]

**Needs confirmation — lifecycle:** `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED` are cataloged. Terminal within configured maximum **OR recoverable timeout** is also explicit. Define missing authorization versus normal review waiting, deadline scope/counting/equality, cancellation/resumption/new-run and failure-state mappings; do not assign the example180s to human review. [Current PDF pp.12,41,49,82; `exception_handling:r1:c14:f2`, `exception_handling:r1:c68:f1`, `exception_handling:r1:c79:f1`, `exception_handling:r1:c137:f3`]

`knowledge.search@v1` is tenant-scoped `read:permitted_documents`, read-only, no arbitrary URLs/filesystem; input `{query:string, case_id:uuid, max_items:int<=10}`, output `{evidence_set_id:uuid, citations:Citation[]}`. A2A declares task/capability/input-output schema/deadline/trace and may decline. Depicted `case_demo`, `grant_readonly_14`, `deadline_at:"2026-11-09T08:00:00Z"`, input schema `schema://oriondesk/research-request/1` and omitted output_schema do not establish effective permission, UUID exception or typed failure transport. [Current PDF pp.41,87; `exception_handling:r1:c67:f5`, `exception_handling:r1:c139:f9`, `exception_handling:r1:c139:f10`, `exception_handling:r1:c139:f11`, `exception_handling:r1:c139:f12`, `exception_handling:r1:c139:f13`]

### ERR-017–019 — Review, expiry and publication rejection

| Condition | Confirmed handling | Needs confirmation beside implementation |
|---|---|---|
| Ineligible reviewer | Enforce policy pool, minimum role and separation; own-high-risk self-approval forbidden | Wider unqualified no-self-approval scope and role aliases; no lower-risk grant |
| Incomplete review fields | **Both Approve and Reject disabled** | Required fields/validation/copy; completeness is not authorization |
| Wrong/changed hash | Reject stale, audit; rejected business state unchanged | Dedicated code/status mapping; decision API reference200/409 is not universal permission409 |
| Expired task | No implicit approval; configured-SLA reassign OR escalate; **escalation recorded** | SLA/time basis/branch/recipients and recording semantics |
| Denied recommendation | Rework as **new run revision**, not retroactive approval | Launch/state/hash/review procedure |
| Override | Elevated role AND secondary reviewer AND audited reason | Identities/independence/applicability; no hash/tenant/ACL bypass evidenced |
| Publication prerequisite absent | Required evidence and satisfied versioned policy; no unapproved high-risk publish | Invoker/endpoint, precise predicates/state/code/recovery |
| Permission changed after search/review | Recompute current authorization, reject stale evidence | In-flight algorithm and corrective evidence/review flow |
| Replay old approval against changed artifact | Cannot publish different content | Same transaction final pointer/satisfied gate; exact participants/encoding open |

[Current PDF pp.11–12,44–46,58,83,85,87,89; `exception_handling:r1:c12:f2`, `exception_handling:r1:c13:f4`, `exception_handling:r1:c73:f1`, `exception_handling:r1:c73:f2`, `exception_handling:r1:c73:f5`, `exception_handling:r1:c73:f6`, `exception_handling:r1:c73:f11`, `exception_handling:r1:c74:f1`, `exception_handling:r1:c74:f5`, `exception_handling:r1:c74:f6`, `exception_handling:r1:c76:f2`, `exception_handling:r1:c97:f5`, `exception_handling:r1:c137:f13`, `exception_handling:r1:c138:f5`, `exception_handling:r1:c139:f5`, `exception_handling:r1:c141:f6`, `exception_handling:r1:c141:f10`]

Show exact candidate, citations, model/prompt version and policy reasons; source inspection must be available before approval. Recorded completed inspection is not required by supplied evidence. Decision records retain actor/time/evaluated hash/rationale and explicitly optional annotations. `ApprovalDecisionRecorded` consumes as **Validate publication**, not automatic publish.

### ERR-020 — Unavailable integration contract

Every source-named interface retains validation before long-running allocation. When a dependency is unavailable: **documented retryable error OR persisted asynchronous job identifier, never ambiguous success**. Neither alternative is universally selected. This applies across governance, case/run/attachment, identity/membership, health, connector/search/model, review, internal workflow/replay/storage, OpenAPI/SSE/evidence, audit/holds/usage/metrics/capacity, release/evaluation and exit interfaces.

Preserve the paths and inventory in API-003–042e; generic clauses do not invent new endpoints. In particular ordinary `200` reads/search/SSE, `201` creation and `202` ingestion/run/sync/evaluation/export/delete acceptance remain distinct. `202` is not READY, PUBLISHED, downloadable export or completed purge. No generic GET wording authorizes job allocation. **Needs confirmation:** dependency taxonomy, selection, allocation owner, durable ID/status/readback/lifetime, retryability and client presentation for each interface. [Current PDF representative §§3.1,15.1–15.3 and A.2, pp.15–16,54–56,83; `exception_handling:r1:c18:f3`, `exception_handling:r1:c18:f7`, `exception_handling:r1:c90:f4`, `exception_handling:r1:c90:f7`, `exception_handling:r1:c92:f8`, `exception_handling:r1:c137:f9`, `exception_handling:r1:c137:f10`, `exception_handling:r1:c137:f11`, `exception_handling:r1:c137:f12`, `exception_handling:r1:c137:f19`, `exception_handling:r1:c137:f20`]

### ERR-021–023 — Derived-state, observation and provisioning recovery

- Failed index write **does not roll back accepted source metadata**. Reconcile fingerprints/retry eligible faults and repair broken message links from outbox ledger. Build parallel index; promote read alias atomically only after completeness/recall checks. Numerical checks/retired-generation policy remain open.
- SSE offsets increase; reconnect uses `Last-Event-ID` to backfill only retained caller-scoped events. Refresh reconstructs stages from server. This is observation, not authorized execution resume. Expired/unknown history, active-stream revocation, heartbeats/timeouts and error displays remain open.
- Encrypted objects use opaque public names and controlled short-lived URLs. Missing object/version/anchor, expired URL, interrupted download and vault/storage failures have no supplied exact response/recovery contract; authorization remains mandatory.
- Optional signed webhooks verify signature/event age and retry exponentially; failed delivery **never rolls back committed case**. Selection/age/algorithms/exhaustion/recipients remain open.
- Idempotent provisioning remains visibly incomplete and blocks sync until complete. Historic sources use bounded windows/stable IDs/per-batch receipts; readiness comes from **index coverage, not queue emptiness**.

[Current PDF pp.34,49–50,52–53,55,58,78; `exception_handling:r1:c54:f6`, `exception_handling:r1:c79:f5`, `exception_handling:r1:c86:f1`, `exception_handling:r1:c91:f1`, `exception_handling:r1:c91:f5`, `exception_handling:r1:c97:f1`, `exception_handling:r1:c132:f1`, `exception_handling:r1:c132:f2`, `exception_handling:r1:c132:f7`, `exception_handling:r1:c132:f8`]

### ERR-024–027 — Exit, integrity, release and resilience

1. Export/delete require **two independent approval checks** and `Admin + approver`. Export specifically needs **two-person approval plus manifest**; a single Admin fails. Do not silently extend person semantics to every deletion check.
2. Export contains case metadata, approved artifacts, source references and checksum audit manifests; excludes secrets/internal prompts. Deletion enforces legal holds, tombstones, permitted blob/index removal and receipts. Held protected records remain **retained and receipted**; `202` is not completion. Tenant/workspace scope and partial completion remain open.
3. Closure snapshots approved answer/cited versions/review decisions and preserves immutable lineage. Case retention only for eligible closed cases; CLOSED alone insufficient and explicit reopen-as-new-revision remains possible. Purge/reopen races and legally permitted lineage purge require decision.
4. Audit/history/decisions remain append-only or immutable as declared. Operators may query, never edit historical review decisions. Vault/credential/encryption rotation obligations remain during recovery; exact rotation-failure response is open.
5. Every storage predicate includes tenant; pool scoped variables reset after **every transaction including failed ones**. Production additionally enforces workspace-tenancy membership by FK **OR** controlled writes. Missing context/reset failure and SQL-to-business errors remain open.
6. Compatible migration/canary/drain and signed build/config/evidence prerequisites apply. Unverified allowed-build digest cannot deploy. Regression triggers **automated traffic rollback, not DB down-migration**; general binary-first compensation only explicitly supported. Plans disclose whether new writes remain readable, not guarantee readability.
7. Low statistical confidence blocks release; independent prompt/model changes require reevaluation. Critical isolation/approval tests have zero exceptions; unmitigated critical cross-tenant OR approval bypass blocks regardless benchmark. SEC-001–012 evidence independently reviewed/reproduced and release-signed.
8. Primary writes/one warm region; snapshot restoration only under incident command. Reference **RPO≤15 min, RTO≤4 h**, continuous PostgreSQL backups and joint object/index-recipe checks. Lost heartbeats/object failures/primary outage need executable recovery contracts; objectives are not schedules.

[Current PDF pp.19–20,25–26,62–63,69–70,72–80,83,85–86,88–89; `exception_handling:r1:c25:f6`, `exception_handling:r1:c26:f6`, `exception_handling:r1:c37:f1`, `exception_handling:r1:c38:f7`, `exception_handling:r1:c38:f8`, `exception_handling:r1:c104:f1`, `exception_handling:r1:c104:f6`, `exception_handling:r1:c116:f1`, `exception_handling:r1:c121:f1`, `exception_handling:r1:c121:f5`, `exception_handling:r1:c122:f1`, `exception_handling:r1:c128:f6`, `exception_handling:r1:c131:f1`, `exception_handling:r1:c134:f1`, `exception_handling:r1:c134:f5`, `exception_handling:r1:c138:f11`, `exception_handling:r1:c138:f12`, `exception_handling:r1:c138:f13`, `exception_handling:r1:c140:f11`, `exception_handling:r1:c140:f13`, `exception_handling:r1:c140:f14`, `exception_handling:r1:c141:f13`]

## Logging, Monitoring, and Operations

### ERR-029 — Evidence and sensitivity contracts

| Evidence | Confirmed fields/conditions | Qualification |
|---|---|---|
| Request/span context | `trace_id`, `correlation_id`; child DB/connector/retrieval/model/approval spans; identifiers and policy outcomes | Provider trace independent; no alias/type/transport supplied |
| General boundary | tenant_id and actor context everywhere | Not editable UI fields |
| Durable-changing record | tenant_id, revision, actor_id, occurred_at, correlation ID | Only “wherever the operation changes durable state”; not universal GET write |
| Canonical event | event_id, type, schema_version, tenant_id, aggregate_id, aggregate_revision, occurred_at, trace_id, payload; UTC/canonical JSON | Canonicalization/types/aliases/version rules open; not SSE/job-envelope equivalence |
| Actual background job | Signed envelope, immutable tenant identity | Whole job/permissions not immutable; signature verification schema open |
| Accepted transition | One audit record, tenant-scoped trace | Separate denial/duplicate evidence retained |
| Denial | Stable non-sensitive code; foreign-resource audit principal and denied resource class | Most code literals and levels open |
| Duplicate | Event ledger/revision and recorded duplicate outcome | No mutation reapplication; schema/atomicity/retention open |
| Incident | Audit IDs, time window, blast radius, quality effect, preventative action | Link evidence, not invented receipt fields |

[Current PDF pp.16–17,22–23,48,64,90; `exception_handling:r1:c20:f2`, `exception_handling:r1:c32:f2`, `exception_handling:r1:c32:f8`, `exception_handling:r1:c78:f1`, `exception_handling:r1:c78:f2`, `exception_handling:r1:c82:f3`, `exception_handling:r1:c108:f1`, `exception_handling:r1:c142:f10`]

**Sensitive values:** public responses/errors never expose secrets/raw provider credentials, connector tokens, full prompts, retrieved documents or unauthorized existence. Safe structured validation details only. Diagnostic traces contain no user documents/API secrets; source text is absent from diagnostic telemetry. Policy-permitted nonessential PII redaction and default token/digest logs do not waive these prohibitions. Audit is independently retained, append-only/batch-hash chained; register SHA-256 source/revision does not select the chain algorithm. Diagnostic logs use **30-day default TTL**; security audit a separate **seven-year fictional policy**, with holds/receipts and corporate selection unresolved. [Current PDF pp.54,62–66,84; `exception_handling:r1:c89:f2`, `exception_handling:r1:c103:f4`, `exception_handling:r1:c104:f1`, `exception_handling:r1:c107:f2`, `exception_handling:r1:c110:f6`, `exception_handling:r1:c137:f22`]

**Needs confirmation:** severity/log levels, field requiredness/types, redaction/hash algorithms, thresholds, notifications/channels/recipients, retention arithmetic and audit verification failure handling. No ERROR/WARN/INFO assignment is source-confirmed.

### ERR-030 — Monitoring and notification conditions

| Signal/incident | Confirmed action/condition | Open operational contract |
|---|---|---|
| Rate/error/latency/saturation; grounding/empty retrieval/provider throttle/token/backlog | Monitor golden and AI metrics | Formula/windows/thresholds/sampling |
| Queue oldest age/index backlog/outbox lag/parser flags/ACL revision | Detect tenant/index generation; diagnose indexing | Numeric thresholds/on-call mapping |
| User-impact incident | Pages reserved for user impact, including failure budgets/stale ACL/missing approval enforcement | Recipient/routing/escalation |
| Routine token spend anomaly | Ticket with owner and threshold, not routine page | Owner identity/threshold |
| Provider outage | Disable new generation; preserve manual/evidence; display degraded; page on-call **only if availability budget impacted** | Detection/budget calculation/current-run recovery/clearance |
| Vector degraded | Lexical retrieval **may** continue with visible reduced-quality flag | Fallback selection/copy/accessibility |
| AccessDenied event | Alert enrichment | Not blanket paging or a production error code |

[Current PDF pp.64–65,69,79,87,90; `exception_handling:r1:c108:f5`, `exception_handling:r1:c109:f6`, `exception_handling:r1:c115:f5`, `exception_handling:r1:c133:f1`, `exception_handling:r1:c139:f7`, `exception_handling:r1:c142:f5`, `exception_handling:r1:c142:f7`]

Reference objectives99.9% monthly, case-create P95 within/under300ms unresolved at equality, search P95 under1.5s excluding remote fetch and separately measured generation are not alert thresholds. Reference2000daily users/60steady180burst rps/100000documents per tenant/20runs per large tenant and approximate1MB→40–120chunks are not selected admission quotas. Configurable numeric thresholds must be **versioned policy**. [Current PDF pp.9,12,65,68; `exception_handling:r1:c7:f5`, `exception_handling:r1:c14:f1`, `exception_handling:r1:c109:f1`, `exception_handling:r1:c114:f1`, `exception_handling:r1:c114:f6`]

### ERR-031 — Operator inspection and bounded recovery

**Delayed-indexing procedure:**
1. Alert on queue oldest age/backlog; identify affected tenant and index generation.
2. Pause **only** faulty connector or indexer shard; keep accepted sources durable.
3. Inspect event ID, outbox lag, parser flags, search throttling and source ACL revision.
4. Replay validated outbox records using bounded operator-controlled work.
5. Compare source fingerprints with indexed versions and run denied-access probes before incident closure.
6. Link audit IDs/time window/blast radius/quality effect/preventative action.

[Current PDF p.90 F.1; `exception_handling:r1:c142:f5`, `exception_handling:r1:c142:f6`, `exception_handling:r1:c142:f7`, `exception_handling:r1:c142:f8`, `exception_handling:r1:c142:f9`, `exception_handling:r1:c142:f10`]

**ACL suspicion:** suspend affected aliases, revoke cached evidence, preserve audit and replay scoped ACL revisions; **restore search only after negative access tests pass**. Running probes is not itself proof of passing. [Current PDF p.79 §22.2.2; `exception_handling:r1:c133:f5`]

**Dead-letter replay:** require operator reason, dry-run validation and scope limit. Preserve original event identity **except** schema-transforming migration with explicit provenance linkage. Replay never confers new tenant/tool/publication permission. Operator identity, numeric bounds, validation criteria and transformed deduplication remain open. [Current PDF p.50 §13.3.2; `exception_handling:r1:c80:f6`]

Transient faults use bounded exponential backoff/random jitter/per-dependency breakers; validation and permission failures are permanent/nonretry. Read transient retry is permitted; mutable idempotency and consequential authorization still apply. Quota terminality, malformed quarantine and model parse bounds retain their distinct conditions. [Current PDF pp.42,49; `exception_handling:r1:c68:f7`, `exception_handling:r1:c68:f8`, `exception_handling:r1:c80:f1`]

### ERR-032 — User-facing failure observation

Use the eight formal screens in SF-004, not representative aliases. Every screen has primary action/status summary; exact error text/placement/retry control/navigation is **Needs confirmation**. Preserve accessible DRAFT/NEEDS_REVIEW/PUBLISHED text, meaningful-only live transitions, visible focus/semantic regions/keyboard order and WCAG2.2AA target behavior. Show exact failed checkpoint; incomplete review disables both decisions; lower-trust/degraded/reduced-quality/incomplete-provisioning warnings are visible where specified. Store UTC and display workspace-local timezone-labeled time; locale never changes ordering/durable representation. No achieved accessibility conformance is asserted. [Current PDF pp.41,57–59,78–79; `exception_handling:r1:c68:f2`, `exception_handling:r1:c96:f1`, `exception_handling:r1:c96:f5`, `exception_handling:r1:c97:f5`, `exception_handling:r1:c98:f1`, `exception_handling:r1:c98:f5`, `exception_handling:r1:c132:f2`, `exception_handling:r1:c133:f1`]

## Failure Acceptance Criteria

### ERR-033 — Required matrix

Tests are obligations, **not reported passes**. Expected states are only those supported; omitted UI/durable state mappings remain open.

| Test / exception | Trigger | Required observable response/state/retry result |
|---|---|---|
| TST-001 / ERR-002–003 | Same-key case twice | One case, identical response; no second business creation |
| TST-002 / ERR-002 | Changed-body key reuse |409 IDEMPOTENCY_CONFLICT |
| TST-003 / T-01 / ERR-006 | Valid foreign case/token |404-equivalent non-disclosing; domain/RLS guard; safe denial evidence |
| TST-004 / T-08 / ERR-006/021 | Revoke indexed access; additionally revoke **during search** | No forbidden next-query evidence; ACL-revision cache invalidation; in-flight mechanism remains required decision |
| TST-005 / ERR-013 | Force schema failure | MODEL_OUTPUT_INVALID; no publish |
| TST-006 / T-03 / ERR-017 | Wrong/prior artifact after revision | Stale rejection/audit; unchanged rejected business state |
| TST-007 / T-07 / ERR-003 | Same outbox event replayed **100 times** | Exactly one accepted business transition and its audit; duplicates recorded, no reapplication |
| TST-008 / ERR-016 | Provider429 storm | Capped retries, controlled admission; saved cases available; no quota/approval escape |
| TST-009 / ERR-012/013 | Missing citations | Needs review **OR unsupported**; branch/state selection open |
| TST-010 / ERR-018 | Review expires | No implicit approval; escalation recorded; reassignment conditions open |
| TST-011 / ERR-032 | Keyboard-only case opening | No blocked action, visible focus |
| TST-012 / ERR-027 | Region recovery | Stated RPO≤15min/RTO≤4h and retained safety/artifact consistency |
| TST-013 / ERR-024 | Purge under hold | Protected records retained and receipted; not full unqualified purge |
| TST-014 / ERR-014 | Arbitrary MCP | DENY before dispatch; no equivalent-tool substitution |
| TST-015 / T-04 / ERR-007 | Unsafe PDF/polyglot/zipped hostile input | Scan/sandbox/bounded parsing; quarantine/no index; ZIP not admitted format |
| TST-016 / ERR-026 | Safety-regressed canary | Promotion blocked; applicable regression traffic rollback, never DB down-migration |
| T-02 / ERR-014 | Hostile paragraph/instructions | Delimited evidence/pinned schemas; no authority change |
| T-05 / ERR-010/025 | Observe traces/provider requests | Vault/redacted telemetry; no credential disclosure |
| T-06 / ERR-016 | Regional provider outage | Only approved eligible fallback, no restricted unapproved route |
| T-09 / ERR-025 | Historical audit edit | Append-only chain integrity; cannot alter past review decision |
| T-10 / ERR-015 | Recursive tool hints | Tool/step/time budgets constrain execution; exact counting open |
| T-11 / ERR-024 | Single Admin export | Denied; two-person approval plus manifest |
| T-12 / ERR-026 | Replace expected score fixture | Versioned signed-manifest integrity; no valid substituted evidence |

[Current PDF pp.88–89 D/E; `exception_handling:r1:c140:f1`, `exception_handling:r1:c140:f2`, `exception_handling:r1:c140:f3`, `exception_handling:r1:c140:f4`, `exception_handling:r1:c140:f5`, `exception_handling:r1:c140:f6`, `exception_handling:r1:c140:f7`, `exception_handling:r1:c140:f8`, `exception_handling:r1:c140:f9`, `exception_handling:r1:c140:f10`, `exception_handling:r1:c140:f11`, `exception_handling:r1:c140:f12`, `exception_handling:r1:c141:f1`, `exception_handling:r1:c141:f2`, `exception_handling:r1:c141:f3`, `exception_handling:r1:c141:f4`, `exception_handling:r1:c141:f5`, `exception_handling:r1:c141:f6`, `exception_handling:r1:c141:f7`, `exception_handling:r1:c141:f8`, `exception_handling:r1:c141:f9`, `exception_handling:r1:c141:f10`, `exception_handling:r1:c141:f11`, `exception_handling:r1:c141:f12`, `exception_handling:r1:c141:f13`, `exception_handling:r1:c141:f14`, `exception_handling:r1:c141:f15`, `exception_handling:r1:c141:f16`]

Also verify:
- Case revision mismatch returns current revision/no mutation; configuration revision preconditions/audit and per-transaction tenant reset hold under failures.
- Unsafe versus authorized low-quality behavior remains distinct; quality document viewable but no autonomous recommendation.
- Revoked queued connector credentials fail without tokens; poison continuation preserves ledger/cursor conditions; incomplete provisioning blocks sync; readiness uses coverage.
- Index failure preserves accepted metadata; replay requires reason/dry run/bounds and migration provenance exception; ACL restoration requires passing negatives.
- Exact source/artifact review and required-field disablement; publication reauthorization and atomic exact-pointer/gate, including old-approval replay.
- Server-reconstructed progress and scoped retained SSE, no false approved partial answer; optional webhook cannot roll back case.
- Generation outage/manual-evidence continuity, optional flagged lexical fallback, terminal current-run quota and no degraded safety bypass.
- Lost-heartbeat/object-access/primary-outage chaos measures **both safety and recovery time**; runtime thresholds/response states remain Needs confirmation.
- No public datastore, shared deployment identity or production data in development; no secrets/documents in prohibited responses/diagnostics; policy-driven rotation remains mandatory.

[Current PDF pp.18–23,28–32,45–50,55–59,63,69–70,78–79,86; `exception_handling:r1:c24:f1`, `exception_handling:r1:c24:f5`, `exception_handling:r1:c26:f1`, `exception_handling:r1:c32:f2`, `exception_handling:r1:c43:f1`, `exception_handling:r1:c44:f6`, `exception_handling:r1:c50:f6`, `exception_handling:r1:c74:f1`, `exception_handling:r1:c79:f5`, `exception_handling:r1:c80:f6`, `exception_handling:r1:c91:f1`, `exception_handling:r1:c91:f5`, `exception_handling:r1:c97:f1`, `exception_handling:r1:c104:f6`, `exception_handling:r1:c116:f6`, `exception_handling:r1:c132:f2`, `exception_handling:r1:c133:f5`, `exception_handling:r1:c138:f12`]

### ERR-034 — Evidence pack and release failure gates

Every revised invariant links at least one negative test. Deterministic tests avoid live models and pin adapters; disposable integration covers transactional/replay/ACL/index/purge faults. Synthetic fixtures include success, empty, mixed-permission, adversarial and malformed inputs; every randomized seed is recorded; corpora frozen/versioned/independently leakage-reviewed. Empty fixtures do not establish successful runtime no-op.

Minimum pipeline: unit, schema evolution, negative authorization, workflow replay, staging sync, visual accessibility, search recall, grounding, policy recall, load and disaster recovery. Outputs signed/release-digest linked. Frozen1200-case targets citation precision≥.97, unsupported≤.02, high-risk recall1.00 require domain confidence/shift reporting; low confidence blocks. Zero critical isolation/approval exceptions; SEC-001–012 independent review/reproduction/signature and benchmark-independent critical promotion block apply. **Needs confirmation:** statistics, signatures, report/fixture contracts and SEC/T/TST mapping; equal namespace counts are not equivalence. [Current PDF pp.8,74–76,88–89; `exception_handling:r1:c5:f2`, `exception_handling:r1:c126:f1`, `exception_handling:r1:c126:f6`, `exception_handling:r1:c126:f7`, `exception_handling:r1:c127:f1`, `exception_handling:r1:c127:f6`, `exception_handling:r1:c128:f6`, `exception_handling:r1:c140:f13`, `exception_handling:r1:c140:f14`, `exception_handling:r1:c141:f17`, `exception_handling:r1:c141:f18`, `exception_handling:r1:c141:f19`, `exception_handling:r1:c141:f20`]

## Consistency and Open Questions

### ERR-035 — Conflicts, amendments and implementation decisions

Do not rewrite completed files or silently select unresolved alternatives. The following must be carried beside the affected `ERR-*` and prior identifiers into later decision consolidation.

| Open ID | Affected requirements / prior links | Both positions or required contract |
|---|---|---|
| ERR-OQ-001 | ERR-000; SF-001/API-001/DAT-001/BAT-000/BR-001 | Current cover/governance confirms revision; full equivalence to prior1794353355 PDF remains open. Preserve separate citations; filename alone does not prove substantive change |
| ERR-OQ-002–004 | All; API-G01/G03/G06/G07/G14/G15; DAT-OQ-001/007/008/016/019 | Complete response/operation/event/job schemas, statuses/codes/messages, audiences/roles, field types/defaults/requiredness, dependency error OR persisted-ID selection/owner/readback. No universal GET jobs or conventional status invention |
| ERR-OQ-005 | ERR-015; SF OQ-003/004; API-G02a/b; DAT-OQ-005; BAT-OQ-008; BR-OQ-003 | Recoverable timeout p.12 versus termination p.41 and AWAITING_REVIEW/FAILED pp.49/82. Define applicability/timers/resume/cancel/counting. POST /v1/runs versus case-run path remains unaliased |
| ERR-OQ-006 | ERR-011/013/028/031; BR-OQ-007; DAT-OQ-011; BAT-OQ-006/007 | Malformed bounded retries/model parse bounds versus permanent validation/permission nonretry p.49. Define fault/attempt taxonomy, bounds/breakers, poison durable outcomes and continuation/cursor conditions |
| ERR-OQ-007 | ERR-002/003/031; API-G06/07; DAT-014; BAT-022; BR-OQ-010 |24h request fingerprint mechanics distinct from example replay24h/SSE retention; define ledger atomicity/retention/delayed outcomes/replay migration provenance |
| ERR-OQ-008 | ERR-025; API-G05; DAT-OQ-002–004; BAT-OQ-009; BR-OQ-004 | Preserve immutable Case/CaseService/CaseAggregate versus mutable revision state, ApprovalTask/ReviewForm versus expiry/input, IndexAlias versus switch, SyncRun/ProvisioningJob versus progress. Clarify APIReplicaSet/TenantMembership/ExtractionJob/ErrorEnvelope and CacheEntry ledger/ephemeral subject, all hash/predicate scopes; no invented heads/snapshots |
| ERR-OQ-009 | ERR-017/018; SF OQ-006/007; API-G04/G12; DAT-OQ-006/013; BAT-OQ-010; BR-OQ-002 | Own-high-risk prohibition p.11 versus unqualified no-self-approval p.85; no lower-risk grant. Required fields/pools/secondary independence/override/hash, expiry reassign OR escalate p.45 versus recorded escalation p.89 need contracts |
| ERR-OQ-010–012 | ERR-007–016/019/021/022; SF OQ-010/013/018; API-G08–10/G12; DAT-OQ-011–013; BR-OQ-006–011/018 | MIME/MB/quality/OCR/scanner/anchor/Citation, capability/cursor/reauth/readiness, model/fallback/grants/A2A schema, missing-invalid-unsupported precedence, in-flight ACL/URLs/SSE and exact publication recovery remain open |
| ERR-OQ-013/014 | ERR-024–027; API-G13; DAT-OQ-014/015; BAT-OQ-012–016; BR-OQ-012–016 | Local ACID participants/approved compensation; closure lineage versus eligible hold-safe purge; tenant receipts/event versus workspace paths; approvals/manifest/hold/partial receipt; audit/hash/retention/key-rotation failure recovery |
| ERR-OQ-015/016 | ERR-029–034; API-G16–19; DAT-OQ-017/018; BAT-OQ-013–016; BR-OQ-015/016 | Levels/recipients/windows/thresholds/on-call, SLO within versus under300ms, capacity versus quotas, recovery clocks/schedules, canary/readability/build/signatures/statistics/fixtures/SEC mapping. Preserve exact values, no achieved results |
| ERR-OQ-017 | ERR-032; SF-005/015/OQ-001; DAT-OQ-020; BR-OQ-017 | Complete routes/actions/field and accessible error observation. Preserve all title/sidebar discrepancies; fictional values never determine failure codes, limits, five-citation minimum or model selection |
| ERR-OQ-018 | All; SF OQ-020; API-G20; DAT-OQ-021; BAT-OQ-018; BR-OQ-020 | Six dated architecture selections before implementation lock; key isolation/rotation throughput before enterprise GA; optional BFF/webhooks/Terraform-Bicep unselected. No supplied owner/date/approval |

Key current conflict evidence: `exception_handling:r1:c14:f2` / `exception_handling:r1:c68:f1` / `exception_handling:r1:c79:f1` / `exception_handling:r1:c137:f3`; `exception_handling:r1:c44:f5` / `exception_handling:r1:c61:f6` / `exception_handling:r1:c80:f1`; `exception_handling:r1:c12:f2` / `exception_handling:r1:c138:f5`; `exception_handling:r1:c73:f2` / `exception_handling:r1:c141:f10`; `exception_handling:r1:c90:f1` / `exception_handling:r1:c137:f21`; `exception_handling:r1:c14:f1` / `exception_handling:r1:c109:f1`. Original pages are stated beside the affected requirements above.

Preserve DAT-004 exact classification families: Owner aggregate / UUIDv7 + tenant scope; Immutable derivative / SHA-256 source/ revision; Policy-bound control / Actor and role predicate; Operational ledger / Event ID + trace context. The supplied register evidence is logical, not a complete physical schema or hash-equivalence decision. [Current PDF chapter registers, particularly pp.13,17,26,29,32,36,46,53,56,59,80; `exception_handling:r1:c15:f3`, `exception_handling:r1:c21:f3`, `exception_handling:r1:c39:f3`, `exception_handling:r1:c45:f3`, `exception_handling:r1:c51:f3`, `exception_handling:r1:c57:f3`, `exception_handling:r1:c75:f3`, `exception_handling:r1:c87:f5`, `exception_handling:r1:c93:f3`, `exception_handling:r1:c99:f3`, `exception_handling:r1:c135:f3`]

**Example configuration retained, not selected defaults:**

```yaml
release: r1.0
workflow: {max_plan_depth: 8, max_tool_calls: 16, run_timeout_seconds: 180, replay_dedup_hours: 24}
retrieval: {max_candidate_chunks: 80, max_selected_chunks: 10, embed_dimension: 1536, hybrid_rrf_k: 60}
policy: {auto_publish_classification: INTERNAL, require_human_review_for: [HIGH_RISK, RESTRICTED], self_approval_allowed: false}
storage: {upload_limit_mb: 25, user_data_region: primary-approved-region}
observability: {trace_sample_rate: 0.10, diagnostic_retention_days: 30, audit_retention_years: 7}
```

Only independently confirmed8/16/1536/configurable25MB and scoped retention bind their operative contexts.180s/24h replay/80/10/RRF60/.10 do not select timeout/history/replay/pagination; INTERNAL does not authorize unrestricted publication; placeholder region is unselected. [Current PDF p.90; `exception_handling:r1:c142:f1`, `exception_handling:r1:c142:f2`, `exception_handling:r1:c142:f3`, `exception_handling:r1:c142:f4`]

**Prior-stage amendment notes, not rewrites:** retain CaseStateChanged, ConnectorSyncStarted and scoped Idempotency-Key additions; explicitly preserve signed immutable background-job tenant identity, policy-driven encryption rotation without request-path bulk reencryption, versioned numeric thresholds and conditional transient read retry. Clarify pool reset includes failed transactions. Record exact rejection-before-AccessDenied ordering without converting every GET into event emission. Current error handling now supplies the Stage6 destination for earlier exception dependencies, but does not resolve their remaining TBDs.

Six selections—supported cloud region, exact search provider, identity provider, approved model deployments, corporate retention and third-party connector permissions—require dated architecture decisions before implementation lock. Key isolation/rotation throughput requires future-revision resolution before enterprise GA. [Current PDF pp.10,90; `exception_handling:r1:c8:f7`, `exception_handling:r1:c142:f11`]

**Dependencies:** remaining integration and architecture refinements are **To be defined in a later stage**. Stage8 will consolidate unresolved items from completed Markdown into `08_architecture_decision.md` with ERR/SF/API/DAT/BAT/BR links. It is not generated here. No unresolved choice authorizes implementation discretion, and no owner, calendar deadline, sign-off, passed test or production selection is invented.
