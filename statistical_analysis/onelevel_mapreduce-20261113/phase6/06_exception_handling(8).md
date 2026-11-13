# 6. Exception Handling Specification

## Exception Inventory and Classification

### Baseline and interpretation

`06_exception_handling.md` specifies exception handling for **OrionDesk AI**, `OD-AI-DDS-001`, `R1.0`, design revision `1.3`. **Confirmed** denotes requirements of the fictional reference design, not observed production behavior. “All numbers are design assumptions, not measured production performance.” [Source: `1794325316-OrionDesk_AI_Detailed_Design_Specification.pdf`, pp.1–2; exception_handling:r1:c1:f1–f3, exception_handling:r1:c2:f1.]

All citations below refer to that exact filename and original page numbers. Citation shorthand `cN:fM` means `exception_handling:r1:cN:fM`; ranges retain the corresponding finding identifiers. Contents pp.2–6 are navigation, and logical figures are not executable recovery graphs. All pages were covered by supplied text; separate images not exposed to the evidence reviewers were not independently inspected. [pp.2–6; c2:f2–f6.]

ERR identifiers are assigned here for traceability, not claimed source identifiers. Exact source codes and `TST`, `T`, `SEC` namespaces are preserved separately. **Needs confirmation** is an implementation blocker, not permission to choose defaults. No Proposal is approved. Prior specifications are reference dependencies, not independent source evidence: [01_screen_functions.md](01_screen_functions.md), [02_api.md](02_api.md), [03_data.md](03_data.md), [04_batch_functions.md](04_batch_functions.md), [05_business_rules.md](05_business_rules.md). Their identifiers remain unchanged.

**Out of scope:** Physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing, agent administrative cloud permissions and application-hosted GPU inference. Cross-region active/active mutation, OCR beyond English and customer-managed model weights are deferred. These exclusions do not exclude authorized manual case work or separately approved tools. [pp.9–10,19; c4:f12–f13, c7:f7.]

### Classification convention

Categories below are analytical labels, not new wire enums. A duplicate delivery handled correctly is an operational exception, not necessarily an error response. Policy `DENY`, review `REJECTED`, run `FAILED`, document `QUARANTINED`, UI `NEEDS_REVIEW` and HTTP error codes are distinct concepts.

For every exception, unspecified **HTTP status, business literal, error fields/types/requiredness, display wording/location, log level, recipient/channel, retry limit, timeout, terminal state, rerun interface and compensation mechanism** are individually **Needs confirmation**. No universal `500`, `503`, `401`, `403`, retry count or recovery button is selected by this specification.

### Exception inventory and implementation mapping

Mappings identify affected consumers and domain functions, not approved screen controls or newly deployed jobs.

| ID / preferred source identifier | Category and detection condition/location | Affected scope and earlier identifiers | Source |
|---|---|---|---|
| ERR-001 Schema/input invalid | Payload validation before transaction/allocation, domain validation and pinned tool-argument validation; invalid required review/correction data | All applicable APIs/SCR; API-053; DAT-029; BAT shared guards; BR-006, BR-004/013 | pp.12,54,56,58; c5:f6, c18:f3,f12, c19:f8 |
| ERR-002 Authentication invalid | Gateway token algorithm/tenancy and issuer/audience/expiry/subject validation; independently authorized service boundary | All requests; SF-003; API-045; DAT-027; BR-002/021 | pp.18,21; c7:f3, c8:f1–f3 |
| ERR-003 Resource/tenant/duties denied | Role, tenant, workspace, sensitivity, source ACL, action or segregation predicate fails at edge/domain/storage/tool/review | All SCR/API/BAT; API-045/053; DAT-024/027; BR-002/003/013 | pp.21–23,85–86; c8:f8–f12, c27:f5,f11–f13 |
| ERR-004 `CASE_VERSION_CONFLICT` | `If-Match` differs from current case revision; configuration updates also have revision guards, but their contract mapping is unresolved | SCR-002, SCR-007 dependency; API-004; DAT-004/029; BR-006 | pp.24–25,83–84; c9:f2,f7, c26:f8,f17 |
| ERR-005 `IDEMPOTENCY_CONFLICT` | Previously used job key submitted with changed fingerprint/body | Job-creating POSTs; API-001/053; DAT-029; BAT launch controls; BR-006 | pp.25,54,89; c9:f8, c18:f4, c30:f1–f2 |
| ERR-006 Duplicate/stale/reordered execution | Consumer event/operation ledger and aggregate revision detect repeated or delayed work | API-046; DAT-010/015/029/034; BAT-001–013,017,021–022 as applicable; BR-015 | pp.17,48–50; c6:f12, c16:f1–f5,f13 |
| ERR-007 Upload/abuse invalid | Unsupported format, signature/extension mismatch, active size cap or decompression protection fails | SCR-002; API-006; DAT-030/033; BAT-003; BR-007 | pp.13,30; c5:f10, c11:f2 |
| ERR-008 Unsafe file / poison record | Scanner/sandbox/parser detects unsafe content; malformed sync record exhausts bounded attempts | SCR-002/006; API-006/007/018/050; DAT-006/016/030; BAT-002/003; BR-007/008 | pp.29–30,88–89; c10:f12, c11:f5, c29:f4, c30:f15 |
| ERR-009 Extraction quality insufficient | Empty-page/unknown-character ratios, table-loss indicators or language confidence fail quality policy | SCR-003; API-007–010; DAT-025/030; BAT-003/007; BR-007/009 | p.32; c11:f12 |
| ERR-010 Connector capability/provisioning gap | Missing advertised list/fetch/delta/ACL/delete capability; provisioning incomplete | SCR-006; API-018/050; DAT-003/025/030; BAT-002/015; BR-008 | pp.27,78; c10:f2, c25:f2–f3 |
| ERR-011 `CONNECTOR_REAUTH_REQUIRED` | Queued job resolves revoked workspace-scoped credential reference | SCR-006; API-050; DAT-016/026; BAT-002/020; BR-008/021 | p.27; c10:f7 |
| ERR-012 `NO_SUPPORTED_EVIDENCE` / missing citation | Retrieval confidence/quality insufficient, citation not verified/resolvable, or response lacks support | SCR-003/004/005; API-008–010/036/047; DAT-008/011; BAT-007/009; BR-009/014 | pp.31,35–36,89; c11:f11, c12:f10–f11, c30:f9 |
| ERR-013 `MODEL_OUTPUT_INVALID` / injection | Gateway versioned JSON rejects unknown fields, invalid citations/control injection; evidence contains hostile tool/system directives | SCR-004; API-036/047/051/053; DAT-025/035; BAT-007; BR-010/011 | pp.7,38–39,61,89; c3:f4, c13:f6–f10, c20:f3, c30:f5 |
| ERR-014 Tool action `DENY` / A2A decline | Arbitrary/unauthorized capability, invalid pinned arguments, forbidden effect/destination; receiving agent declines | SCR-004; API-047/048; DAT-035; BAT-007; BR-011 | pp.40–42,87,89; c14:f1,f8–f12, c28:f7–f11, c30:f14 |
| ERR-015 Quota/admission/provider throttle | Token/queue-age/provider-capacity admission fails; provider sends 429; run exhausts workspace quota | SCR-002/004/006; API-011/036/042/050/051; DAT-009/017; BAT-002/007/018; BR-018/019 | pp.28,38,69,89; c10:f11, c13:f9, c22:f7, c30:f8 |
| ERR-016 Runtime/plan/deadline/approval timeout | Calls exhausted, repeated invalid plans, policy denial, deadline or missing approval; configured maximum exceeded | SCR-004/005; API-011–017/037; DAT-009/010/028; BAT-007–009; BR-011–014 | pp.12,40–41,49,82; c5:f9, c14:f7,f11, c16:f6, c26:f3 |
| ERR-017 Approval stale/ineligible/incomplete/expired | Artifact hash changed, self approval/duties failure, fields incomplete, configured task SLA expires | SCR-005/003; API-016/017; DAT-012/013; BAT-008/009; BR-013/014 | pp.45–46,58,82,85,89; c15:f8–f12, c19:f8, c26:f5,f11, c27:f5, c30:f6,f10 |
| ERR-018 Stale/revoked evidence / suspected ACL leak | Access revoked after indexing/during search/before publication, source deleted, or stale visibility suspected | SCR-003/004/005; API-008–010/017/033; DAT-006/011/030; BAT-006/009/011; BR-002/009/019 | pp.27–29,51–53,79; c10:f1,f9, c17:f7,f12,f15, c25:f8 |
| ERR-019 Integration unavailable/degraded | Model/repository/identity/tool/internal dependency unavailable; vector index degraded | Affected existing SCR/API/BAT; API-033/045/050/051; SF-017; BR-019 | pp.11–13,37,69,79; c5:f3, c13:f3, c22:f8, c25:f7 |
| ERR-020 Index write/rebuild/link failure | Derivative write fails, source/index fingerprint differs, outbox link broken, completeness/recall not satisfied | SCR-003/006 consumers; DAT-006–008/015/030; BAT-004/005/011/015; BR-009/015 | pp.34,49,78,90; c12:f7, c16:f7, c25:f3, c31:f7–f12 |
| ERR-021 Storage/context/internal worker failure | FK/unique/not-null/status/RLS violations, failed DB/object operation or lost heartbeat; scope-reset failure | API-039/040 and affected mutations; DAT-023/029/032; BAT shared controls/023; BR-003/015/021 | pp.51–52,70,85–86; c17:f1,f8, c22:f11, c27:f1,f8–f13 |
| ERR-022 SSE/object-access interruption | SSE disconnect/retained-offset issue, expired signed URL or unavailable source evidence | SCR-003/004/005; API-015/052; DAT-033; BR-009/020 | pp.52,55,57–58; c17:f11, c18:f8, c19:f1,f7 |
| ERR-023 Webhook delivery/verification failure | Optional delivery fails or recipient signature/event-age validation fails | API-049; DAT-029/033; BAT-016; BR-015 | p.55; c18:f9 |
| ERR-024 Hold/export/deletion control | Independent approval absent, legal hold protects records, export would include excluded secrets/prompts | API-024/025/030/040; DAT-019/031; BAT-012–014/019; BR-017 | pp.26,78–80,88–89; c9:f11, c25:f1,f10–f11, c29:f11, c30:f13 |
| ERR-025 Diagnostic/audit/secret-scope violation | Public or diagnostic disclosure, historical audit edit, model/tool secret outside scope | SCR-008; API-020/041/053; DAT-013/014/026; BAT-017/019/020; BR-016/021 | pp.54,61–66,84,88; c18:f2, c20:f1,f8–f11, c21:f1, c26:f18, c29:f5,f9 |
| ERR-026 Governance/release/evaluation gate failure | Unapproved/incompatible baseline, active-reader deletion, unverified build, canary safety regression, fixture tamper, critical security failure or low statistical confidence | API-022/023/031/032/043/044; DAT-026/032/036; BAT-021/022; BR-001/022 | pp.8,52,55,71–76,88–89; c4:f1–f2, c17:f9, c18:f11, c23:f7–f11, c24:f1,f12, c29:f12–f14, c30:f16 |
| ERR-027 Primary-region outage | Primary fails; incident-command recovery and reference restore verification required | DAT-032; BAT-023; BR-021; affected services/screens | pp.19,69–70; c7:f8, c22:f10–f11 |

## Handling by Exception

### EH-001 Shared decision and transaction procedure

1. Authenticate principal and immutable tenant. Enforce broad edge policy, then resource attributes inside the domain transaction, storage tenancy, source ACL before model text, pinned tool authorization before dispatch and current authorization/evidence before publication. Navigation hiding is not enforcement. [pp.21–23,56; c8:f1–f12, c18:f12.]
2. Validate before long-running allocation or transaction entry. Model output and retrieved text cannot authorize tools, tenancy, approvals or deterministic policy. Orchestrator has no direct DB credentials. [pp.7,9,38,61; c3:f2–f4, c4:f14, c13:f6, c20:f3.]
3. Check revision, artifact hash and request idempotency before accepted effects. Reject stale/unauthorized business mutations unchanged; mandatory safe denial evidence still applies. Do not emit an accepted-business-state event for a rejected mutation. Denial-event commit/revision ordering remains ERR-OQ-002. [pp.22–26,45; c8:f10,f12, c9:f9, c15:f10.]
4. Case mutations, approval decisions and outbox inserts use one ACID commit. Final pointer and satisfied publication gate commit together. Search/webhooks reconcile asynchronously; state-changing workflows use transactional outbox or explicitly reconciled saga. This is not an all-store or whole-batch transaction. [pp.17,45,52; c6:f12, c15:f11, c17:f8.]
5. Preserve immutable document versions, append-only revisions/audit and immutable decisions. Rework denied content as new run revision; pipeline reprocessing may coexist side by side. No generic historical overwrite or compensation is authorized. [pp.31,46,85; c11:f9, c15:f12, c27:f2.]
6. If dependency unavailable, return documented retryable error or a **persisted** asynchronous operation identifier, never ambiguous success. Known `202` results acknowledge ingestion/run/sync/evaluation/export/delete work, not completion, all-item success or publication. Per-interface branch remains open where absent. [pp.11–13,83; c5:f3,f7, c26:f9,f12,f15–f16.]
7. Reset scoped pool variables after **every transaction**, including failed transactions. Enforce additional production workspace-tenancy membership via approved FK or controlled write procedure; reference FKs alone are insufficient. Reset-failure handling is Needs confirmation. [p.86; c27:f8,f11–f13.]

### EH-002 Safe error representation

**Confirmed mappings:** `422` schema-invalid request; `429` quota/admission with `Retry-After` for throttled clients; `409 CASE_VERSION_CONFLICT` for case revision mismatch; `409 IDEMPOTENCY_CONFLICT` for reused key with changed body; foreign-tenant case reads return `404`-equivalent non-disclosing error; hash-bound review decision has `200`/`409` contract, but stale business literal is unspecified. [pp.54,69,83–84,89; c18:f3–f4, c22:f7, c26:f8,f11,f17, c30:f2–f3.]

Preserve uppercase source literals despite p.54 snake-case prose. Do not assign HTTP status to `NO_SUPPORTED_EVIDENCE`, `MODEL_OUTPUT_INVALID`, `CONNECTOR_REAUTH_REQUIRED` or tool-policy `DENY` without approved contract evidence.

**Verbatim canonical example**, Appendix A.3 p.84 [c26:f17]:

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

| Demonstrated field | Example type/meaning | Implementation qualification |
|---|---|---|
| `error` | Object wrapper | Universal requiredness/variants Needs confirmation |
| `code`, `message` | Strings; stable code and safe explanation | Full enum/localization/requiredness Needs confirmation |
| `correlation_id` | String investigation reference | Transport/format/requiredness Needs confirmation |
| `retryable` | Boolean; case conflict is `false` in example | Universal field requirement and other exception values Needs confirmation |
| `details` | Safe object | Safe structured validation details are permitted, not universally required |
| `expected_revision`, `actual_revision` | Example integers `7`, `8`; current revision supplied on conflict | Values are placeholders; wire bounds/schema Needs confirmation |

Error objects and public responses must not expose credentials, full prompts, retrieved documents, raw provider secrets or unauthorized resource existence. This prohibition includes structured details, not just messages. Source p.82 qualifies examples as placeholders; OpenAPI/protobuf must derive from repository IDL, which is not supplied. [pp.54–56,82,84; c18:f1–f2,f11, c26:f1,f18.]

### EH-003 Per-exception response, continuation and recovery

Shared EH-001/EH-002 controls apply to every row. “Not retried” means no automatic replay of the same permanent failure; a separately authorized corrected request is not prohibited. All missing row-specific values remain Needs confirmation.

| Exception | Response/display and interruption/continuation | State, retry/rerun/recovery requirements |
|---|---|---|
| ERR-001 | Schema-invalid REST request `422`; other rule-validation literal/status unspecified. Reject before allocation/transaction. Incomplete review fields keep both Approve/Reject disabled. | Validation failures permanent, not retried. Missing correction reason/review field response schema and client timing require confirmation. Do not allocate work on invalid input. |
| ERR-002–003 | Reject invalid authentication or failed resource predicate. Foreign IDs use absent-ID-equivalent non-disclosure. Do not expose tenant/resource existence in UI/details. | Permission failures permanent, not retried; rejected business state unchanged. Maintain safe principal/resource-class denial audit. Token expiry/reauthentication, invalid job-signature/context and service-audience recovery remain open. |
| ERR-004 | `409 CASE_VERSION_CONFLICT`, current revision, canonical safe message; example `retryable:false`. Workspace mutation mapping remains unresolved. | No automatic stale PATCH retry or merge. Current-revision read is available through API-003; reload/merge/unsaved-edit UX must be confirmed. Rejected write cannot advance accepted case revision. |
| ERR-005 | Same key/body returns original operation/outcome; changed body `409 IDEMPOTENCY_CONFLICT`. | Actor/fingerprint outcome retained 24 hours. No second accepted outcome. Key scope/fingerprint locking/missing-key/exact-expiry recovery unspecified; do not treat 24 hours as all-event retention. |
| ERR-006 | Consumer checks ledger/event/operation identity and aggregate revision, records duplicate outcome and returns without mutation. A duplicate is not necessarily HTTP failure. Detect stale/reordered revisions. | One accepted business transition remains; no partition-order dependency. Idempotent `run_steps`/stage checkpoints support continuation. Stale-event disposition and concurrent dedup arbitration need confirmation. |
| ERR-007 | Fail closed safely on unsupported/mismatched/oversized/abusive upload. R1 allowed formats PDF, DOCX, HTML, UTF-8 text; configurable 25 MB per file. | Do not bypass scan/parser gates or silently raise cap. MB units/equality/decompression threshold/file count and code/status open. Corrected upload is separate validated operation; malicious ZIP test does not add supported format. |
| ERR-008 | Unsafe attachment enters quarantine and never index. Scan before parsing; macros disabled; embedded remote references not fetched. Malformed sync item after bounded attempts quarantines with reason/correlation/remediation. | **Remaining sync batch may continue**, with ledger exception; never report partial as all-success or force whole-batch rollback. Cursor advances only after preceding durable ingestion outcomes, not necessarily completed indexing. Retry count/continuation policy/partial state/quarantine release procedure open. |
| ERR-009 | Low-quality permitted document remains viewable, but excluded from autonomous recommendations. Capture specified quality flags. | Not blanket malware quarantine or invisibility. Current ACL still applies. Thresholds/OCR opt-in actor/manual recommendation scope/remediation open. Preserve page/bbox/table/headings/reading order and claims. |
| ERR-010 | Capability gap visibly warns and lowers trust rather than assuming capability. Incomplete provisioning visibly blocks sync. | Supported concepts list/fetch/delta cursor/ACL/delete. One idempotent provisioning workflow does not imply distributed ACID. Recovery/launch endpoint/readiness threshold open; readiness is index coverage, not empty queue. |
| ERR-011 | Queued revoked-credential jobs fail `CONNECTOR_REAUTH_REQUIRED`, no tokens. | No automatic unchanged credential retry that bypasses revocation. Operator revocation is confirmed; eligibility/reauthorization endpoint/control/resume policy open. Credentials remain vault references. |
| ERR-012 | Insufficient support returns `NO_SUPPORTED_EVIDENCE`, not fabricated context. Missing citations yield needs-review or unsupported alternative. Verify opaque IDs before display and resolvable/currently permitted anchors before citation. | Clarification or human routing allowed, universal branch unselected. No approved final unsupported answer. Exact result state/citation-failure UX/code and replacement-evidence path open. No five-citation minimum. |
| ERR-013 | Unknown fields/invalid citations/control injection yield `MODEL_OUTPUT_INVALID`; schema failure cannot publish. Retrieved/system/tool directives are untrusted; delimit evidence, strip evidence-context tool directives and record indicators. | Versioned output parsing has bounded attempts; specific count/exhaustion state open. Do not equate bounded output parsing with retrying permanent request validation or permission denial. Stored source claims remain unchanged. |
| ERR-014 | Arbitrary MCP attempt `DENY` before dispatch; discovery never grants permission. Schema-pinned typed arguments and separate capability grants required. A2A receiver may decline. | No equivalent-tool bypass. Mutable effects need key; consequential effects additionally human authorization. `knowledge.search@v1` read-only tenant `read:permitted_documents`, no arbitrary URL/filesystem; `max_items:int<=10`. A2A decline/deadline/error and case_demo→UUID adapter open. |
| ERR-015 | Admission throttling `429 Retry-After`; saved cases remain available. Honor provider signal, workspace quota/backoff/jitter/fairness. | Bounded retries/admitted load; quota exhaustion terminal for current run without automatic model/data-class switching. Token settlement/refunds/counts and terminal literal open. Reference concurrency twenty is not selected client quota. |
| ERR-016 | Report exactly failed checkpoint for exhausted calls/repeated invalid plans/denial/deadline/missing approval. Depth <=8, invocations <=16; persist plan revision before effects and checkpoints before dispatch. | **ERR-OQ-003 blocks final timing/state choice:** missing approval vs awaiting review, recoverable timeout vs FAILED, expiry-run effect/AUTO_ALLOW. Do not immediately fail ordinary review waiting, implicitly approve or select example timeout 180. Cancellation/retry endpoint not confirmed. |
| ERR-017 | Stale hash decision rejected/audited, review conflict `409`; ineligible/self-approval denied. Required fields disable decisions. Configured expiry records escalation/reassignment, never approval. | Exact candidate/citations/model-prompt version/policy reasons inspectable. Task-wide no self approval. Capture actor/time/hash/rationale/optional annotations. Gate/pointer atomically bind matching current artifact; replay cannot substitute. Override elevated role + secondary reviewer + audited reason; denied rework new run revision, not retroactive approval. |
| ERR-018 | Next retrieval cannot return revoked source; deleted content unretrievable. Purge affected caches before results/ordinary TTL; recheck publication and reject stale evidence. Suspected leak suspends affected aliases/cache and preserves audit. | Scoped ACL-revision replay; search re-enable only after negative access tests pass. This qualifies ordinary search availability. Stale-evidence result state/code, already-open UI removal and re-enable authority open. |
| ERR-019 | Provider outage disables new generation, displays degraded status, retains manual case/evidence. Vector degradation may use lexical-only retrieval with visible reduced-quality flag; all gates remain. Other unavailable integrations use documented retryable error or persisted ID. | Fallback only approved equal-or-stronger handling, never restricted unapproved region/deployment. General fallback does not select in-flight recovery or override new-admission disablement. Identity/vault/repository/tool outage branches/statuses open. |
| ERR-020 | Failed index write does not roll back accepted source metadata; source database authoritative. Failed completeness/recall cannot authorize checked alias switch. | Reconciliation compares fingerprints/retries and repairs outbox links. Delayed indexing uses EH-006 scoped runbook. Retry gates/cadence/failed-rebuild state and parallel-write races open. |
| ERR-021 | Preserve core ACID boundary and source/object authority. Enforce UUID/FK/unique/not-null/status constraints, tenant RLS and parent tenancy independent of AI. | Database constraint/code translation, reset failure containment, heartbeat/lease recovery, object repair and permanent/transient classification by cause open. No raw DB/private values in public diagnostics. Reset pool after failed as well as successful transactions. |
| ERR-022 | Refresh run reconstructs server progress; SSE reconnect `Last-Event-ID` backfills only retained authorized monotonic offsets. Reviewer must be able to inspect evidence before approval. | Do not invent expired/future-offset response, heartbeat or URL-renewal endpoint. Source URLs remain short-lived/access-scoped. Failure to satisfy source-inspection/current-evidence gate cannot be treated as successful review/publication. Exact display/action open. |
| ERR-023 | Optional signed webhook uses exponential backoff; recipient verifies signature and event age. | Delivery failure **cannot roll back internal case transition**. Terminal delivery state/retry cap/recipient notification/subscription administration open. No invented external compensating write. |
| ERR-024 | Absent independent checks cannot authorize export/delete. Export excludes secrets/internal prompts. Held protected records retained and receipted. | Eligible closed-case retention only; hold protection survives purge. Tombstones/eligible blob-index removal/completion receipts/shared subject inventory apply. Hold lifecycle/partial completion/archive/checksum/download and approval protocol open. |
| ERR-025 | Prevent disclosure and historical edits. Auditors read redacted lineage, not case-edit authority; Operators query historical decisions but never alter. Models/tools receive no out-of-scope secrets. | Append-only batch-hash-chain independent audit export. Vault-managed identity/policy rotation. Audit-recording failure/disclosure containment/chain repair/override logging rules open; no permission to log full prompts inferred. |
| ERR-026 | Block incompatible/unverified/critical failed release. Canary regression rolls traffic back, not DB down-migration. Low confidence blocks; fixture tamper cannot establish trusted evaluation. | Binary-first rollback; compensation only explicitly supported. Preserve new-write readability/active-reader fields/reader drain. Reevaluate prompt/model changes; independently reproduce/sign critical security evidence. No benchmark offsets critical failure. |
| ERR-027 | Primary writes, one warm recovery region, secondary restore only under incident command. | Continuous PostgreSQL backups target reference RPO <=15 min/RTO <=4 h; verify relational/object/index recovery together. No user-selected/automatic active-active failover; restore order/snapshot policy/commander identity open. |

Sources for handling rows: pp.7–90 as indexed in the inventory; additional explicit retry/transaction evidence pp.42,49–50,52 [c14:f12, c16:f7–f10, c17:f8]; gate/rework pp.45–46 [c15:f8–f12]; reference test outcomes pp.88–89 [c29:f1–f14, c30:f1–f16].

### EH-004 Retry and rerun policy

1. Classify by actual cause: transient faults use **bounded exponential backoff, randomized jitter, per-dependency circuit breakers**. Validation and permission faults are permanent and not retried. Numeric counts/delays/breaker state/reset/maximum elapsed time require confirmation. [p.49; c16:f9.]
2. Reads may retry transient faults. Mutable retries require idempotency; consequential effects also require human authorization. Honor connector `Retry-After` and fair workspace quotas. Never substitute denied effects through equivalent tools. [pp.28,42; c10:f11, c14:f12.]
3. Bound output parsing, poison-item attempts and provider 429 recovery under their specific policies. Source does not equate these counts or select one universal retry limit. Persisted operation monitoring is distinct from resubmitting job creation. [pp.29,38,89; c10:f12, c13:f7, c30:f8.]
4. Event/operation dedup and stale revision checks survive rerun. Record duplicate outcome; never reapply accepted mutation. Original event identity is preserved on operator replay except explicit provenance-linked schema migration. [pp.48–50; c16:f5,f10,f13.]
5. No invented cancellation, universal Retry/Rerun API, automatic stale-edit merge, unbounded replay or whole-workflow compensation is approved.

### EH-005 User-facing failure behavior

| Existing screen | Confirmed safety/presentation in failure paths | Needs confirmation |
|---|---|---|
| SCR-001 Case Queue | Clear status; saved cases remain during generation throttle; keyboard opening has visible focus | List loading/empty/error wording and retry/navigation |
| SCR-002 Case Detail | Safe conflict/current revision; distinguish draft/partial/approved result; manual editing remains during generation outage | Conflict merge/reload/unsaved edits/upload error placement |
| SCR-003 Evidence Viewer | Permitted verified citation opens anchored range; low-quality permitted content remains viewable; lexical-only continuation visibly reduced quality | Revoked already-open evidence, unavailable source/URL renewal, no-support UX |
| SCR-004 Run Timeline | Server-authoritative stages/progress; exact failed checkpoint; accessible draft labels; degraded status | Timeout state/action, duplicate rendering, reconnect/offset error display |
| SCR-005 Review Inbox | Exact candidate/source/model-prompt/policy reasons; required fields disable Approve/Reject; stale action rejected; no expiry approval | Required fields, stale refresh/expiry/escalation/override controls |
| SCR-006 Connector Health | Lower-trust capability warning; incomplete provisioning visible; safe revoked-credential failure | Partial sync/quarantine/reauthorization controls and wording |
| SCR-007 Policy Settings | Revision/auth/policy guards and safe errors | Actual settings endpoint/form/error display; never send invented workspace settings in case PATCH |
| SCR-008 Audit Explorer | Immutable redacted audit/history; safe trace/error evidence | Filters/retention-boundary/export/incident drilldown placement |

All screens require one primary action/status summary; WCAG 2.2 AA target focus/semantic/keyboard behavior, meaningful live-transition announcements, textual `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED`, UTC server/RFC 3339 API and workspace-local timezone-labeled display apply. Locale cannot change event order. [pp.54,57–59; c18:f3, c19:f1–f11.]

Representative images are fictional: `128`, `14`, `97.6%`, `Healthy`, `5 verified citations`, `gateway-r1.2`, example case IDs/statuses and sidebar aliases are not error vocabulary, thresholds, defaults or extra screens. Title/selection mismatches on pp.7,14,33,43,47,60,67,77,81 remain unresolved. [c3:f6–f9, c5:f17–f18, c11:f19–f20, c14:f18, c15:f19, c19:f17–f18, c21:f17, c24:f18, c25:f18–f19.]

## Logging, Monitoring, and Operations

### EH-006 Recorded evidence and inspection

| Record/signal | Confirmed fields or meaning | Constraints/open details |
|---|---|---|
| Request tracing | `trace_id`, `correlation_id`; DB, connector, retrieval, model, approval child spans | Correlation crosses every boundary independently of provider trace. Format/transport/generation open |
| Durable change provenance | `tenant_id`, `revision`, `actor_id`, `occurred_at`, correlation ID | Conditional on durable change; not editable payload authority or complete public envelope |
| Event envelope | `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, `payload` | Canonical JSON/UTC; wire types/signing/canonicalization open |
| Accepted/rejected outcome | One audit record per accepted transition; stable safe denied code/tenant trace; principal/denied resource class without existence leak | Rejected state unchanged; denial audit mandatory; denial-event ordering/revision open |
| Review lineage | Actor/time/hash/rationale, optional annotations, model/prompt version, policy reasons, normalized policy inputs/rule version | Exact field mapping/required rationale/hash algorithm open; no historical edits |
| Duplicate/replay | Event/operation identity, ledger/revision check, recorded duplicate outcome | Ledger schema/retention/arbitration and stale disposition open |
| Sync poison item | Reason code, correlation ID, remediation path; cursor/high-watermark/error ledger | Reason catalog/partial status/remediation rights open |
| Index incident | Tenant/index generation, event ID, outbox lag, parser flags, search throttle, source ACL revision | Numeric alert/consistency gates open |
| Golden/AI monitoring | Rate/errors/latency/saturation; grounding pass/empty retrieval/provider throttling/token use/approval backlog age; worker queue age/throughput | Metric names/types/units/windows and thresholds open |
| Usage | Workspace cost centers/deployment version, input/output usage; daily budget/forecast/rejected excess | Daily granularity is not execution schedule; price/formula/settlement open |
| Incident documentation | Audit IDs, time window, blast radius, quality effect, preventative action | Schema/retention/closure authority open |

Sources: pp.16–17,27–29,44–50,62–66,90 [c6:f5,f11–f12, c10:f3,f8,f12, c15:f2,f6,f9, c16:f2–f3, c20:f10, c21:f1–f6,f10, c31:f7–f12].

Diagnostics never contain user documents/API secrets or full retrieved content; public errors additionally exclude full prompts and private existence. Default model logs use token counts/digests, not entire prompts. Policy-conditional personal-data redaction does not approve any logging override. Maximum included material class governs route/log redaction/retention/approval. Audit is append-only, batch-hash chained and exported independently. Diagnostic default TTL **30 days** is distinct from fictional **seven-year** audit policy and legal-hold receipts. Corporate retention remains unselected. [pp.62–66,84; c20:f7–f11, c21:f1,f11, c26:f18.]

**Log levels:** Per-exception severity/level, sampling overrides, alert dedup and alert destinations are **Needs confirmation**. Do not invent ERROR/WARN mappings. Example `trace_sample_rate: 0.10` is not selected.

### Notification conditions

- Page for user-impacting incidents such as availability/failure-budget impact, stale ACL propagation or missing approval enforcement. Routine token-spend anomalies create tickets with owner and threshold instead. Actual owners, thresholds, channels and recipients are Needs confirmation. [p.65; c21:f8.]
- Model-provider outage pages on-call **only when availability budget is impacted**, while showing degradation and preserving manual/evidence. On-call identity/channel and impact formula are open. [p.79; c25:f7.]
- Review expiry records escalation/reassignment without approval; destination/SLA are open. Capability and provisioning gaps are user-visible, but warning wording/audience/dismissal remain open. [pp.27,45,78; c10:f2, c15:f8, c25:f2.]
- Security/SRE promotion validators and security-control owner are source process actors, not invented universal incident recipients or newly assigned individuals. [pp.73,88; c23:f11, c29:f13.]

### Operator recovery procedures

**Dead-letter recovery:**

1. Independently authorize the operator; require reason, dry-run validation and scope limit before replay allocation through existing internal `POST /internal/deadletters/{id}/replay` (API-038).
2. Validate tenant/schema/revision/operation identity and preserve original event identity; schema-transforming migration requires explicit provenance link.
3. Replay bounded work without reapplying accepted outcomes; inspect correlated event/audit/ledger evidence.
4. Exact grants, dry-run wire protocol, limits, partial/empty result and final approval are Needs confirmation. This internal endpoint is not exposed to browsers by this specification. [pp.48–50; c16:f4,f10–f15.]

**Delayed document indexing — Detect → Contain → Diagnose → Recover → Verify → Document:**

1. Alert on oldest queue age/index backlog; identify tenant/index generation.
2. Pause **only faulty connector/indexer shard**; retain accepted sources durably.
3. Inspect event ID/outbox lag/parser flags/search throttling/source ACL revision.
4. Replay validated outbox through bounded operator-controlled job. Relationship to API-038 requires confirmation; no new endpoint is invented.
5. Compare source fingerprints/indexed versions and run denied-access probes before incident closure.
6. Link audit IDs/time window/blast radius/quality effect/preventative action. Numeric bounds/probe suite/closure authority remain open. [p.90 §F.1; c31:f7–f12.]

**ACL incident:** Suspend affected aliases, revoke cached evidence, preserve audit, execute scoped ACL-revision replay, and re-enable search only after negative access tests pass. This containment overrides ordinary evidence availability for affected scope. [p.79; c25:f8.]

**Region/release recovery:** Restore warm secondary only under incident command and jointly verify relational/object/index lineage. Canary regression rolls traffic/binary back, not DB down-migration; data compensation requires explicit support and new-write readability must be documented. [pp.19–20,69–73; c7:f8,f11, c22:f10–f11, c23:f8,f10–f11.]

### EH-007 Source-wide contract and event coverage

The repeated chapter obligations apply to **all** logical component interfaces retained in `03_data.md` DAT-021, including governance, health, membership, holds, metrics, release and evaluation—not merely core case APIs. They require conditional durable metadata, validation before allocation, nonambiguous dependency result, positive/foreign-tenant/duplicate/evidence-retention tests, safe correlated audit, unchanged stale/unauthorized business writes and publication-current-permission checks. Generic read/allocation/register associations remain unresolved and do not authorize GET mutation.

| Chapter boundary, original pages | Existing APIs | Chapter event retained for safe observability/dedup | Evidence |
|---|---|---|---|
| Governance 8–10 | API-031/032 | `BaselineCommitted` | c4:f3–f11 |
| Journeys 11–13 | API-001/011 | `CaseCreated` | c5:f3–f15 |
| Architecture 15–17 | API-012/013 | `RunRequested` | c6:f3–f17 |
| Runtime 18–20 | API-034/035 | `DeploymentPromoted` | c7:f4–f16 |
| Identity 21–23 | API-026/027 | `AccessDenied` | c8:f4–f16 |
| Cases 24–26 | API-004/005 | `CaseStateChanged` | c9:f2–f16 |
| Connectors 27–29 | API-018/019 | `ConnectorSyncStarted` | c10:f3–f17 |
| Ingestion 30–32 | API-006/007 | `DocumentNormalized` | c11:f3–f17 |
| Retrieval 34–36 | API-008/009 | `SearchIndexCommitted` | c12:f3–f16 |
| Gateway 37–39 | API-036/028 | `ModelInvocationCompleted` | c13:f4–f16 |
| Orchestration 40–42 | API-011/014 | `AgentPlanApproved` | c14:f3–f16 |
| Policy 44–46 | API-017/016 | `ApprovalDecisionRecorded` | c15:f4–f17 |
| Workflow 48–50 | API-037/038 | `WorkflowStageAdvanced` | c16:f3–f15 |
| Storage 51–53 | API-039/040 | `DataRetentionPurgeCommitted` | c17:f3–f16 |
| Contracts 54–56 | API-029/015 | `ApiCompatibilityVerified` | c18:f5–f17 |
| UI 57–59 | API-002/010 | `UserReviewOpened` | c19:f3–f15 |
| Security 61–63 | API-020/030 | `SecurityPolicyChanged` | c20:f4–f16 |
| Telemetry 64–66 | API-021/041 | `SloBurnRateDetected` | c21:f3–f15 |
| Capacity 68–70 | API-033/042 | `BackpressureActivated` | c22:f4–f15 |
| Release 71–73 | API-043/044 | `ReleasePromoted` | c23:f2–f15 |
| Evaluation 74–76 | API-022/023 | `EvaluationCompleted` | c24:f3–f16 |
| Lifecycle 78–80 | API-024/025 | `TenantDeletionVerified` | c25:f4–f16 |

Appendix C confirms selected producer/consumer lineage: Case Service case/revision→classifier; Ingestion version/hash→index; Indexer generation/revision→cache invalidation; Orchestrator plan/hash→dispatch and run/stage/checkpoint→resume; Policy Service task/actor/hash→**validate publication**, principal/action/policy digest→alert enrichment; Retention Worker manifest/receipt hash→close purge record. These selected labels are not complete typed JSON keys or automatic SSE event types. [p.87; c28:f1–f6.]

Registers retain scoped `Owner aggregate / UUIDv7 + tenant scope`, `Immutable derivative / SHA-256 source/ revision`, `Policy-bound control / Actor and role predicate`, `Operational ledger / Event ID + trace context`; they do not create application Owner grants, complete SQL schemas, universal hash fields or executable recovery graphs. Specific mutable case/task/alias/form behavior still requires register amendment. [pp.10–80, respective register findings in EH-007; figure qualifications c4:f16, c6:f18, c8:f17, c9:f17, c10:f18, c11:f18, c12:f17, c13:f17, c14:f17, c15:f18, c16:f16, c17:f17, c18:f18, c19:f16, c20:f17, c21:f16, c22:f16, c23:f16, c24:f17, c25:f17.]

## Failure Acceptance Criteria

### Source acceptance matrix

Use authorized synthetic fixtures and independent eligible actors. Confirm missing schemas/thresholds before tests depend on them; test code must not silently choose defaults.

| Source ID / ERR mapping | Trigger | Expected response, screen/data state and retry result |
|---|---|---|
| TST-001 / ERR-005 | Valid case create twice same key/body | One case and identical original response; no duplicate list/business outcome |
| TST-002 / ERR-005 | Reuse key changed body | `409 IDEMPOTENCY_CONFLICT`; no second accepted case/job |
| TST-003 / ERR-003 | Foreign-tenant case read | `404`-equivalent non-disclosing error; no foreign content/existence disclosure |
| TST-004 / ERR-018 | Revoke indexed source then query | No forbidden evidence next query; cache/index history cannot override permission |
| TST-005 / ERR-013 | Force model schema failure | `MODEL_OUTPUT_INVALID`; no publish; no partial-as-approved display |
| TST-006 / ERR-017 | Approve wrong/prior hash | Stale rejection, audited; matching artifact not falsely approved; rejected business state unchanged |
| TST-007 / ERR-006 | Replay accepted outbox | Exactly one accepted business transition; recorded duplicate without reapplication |
| TST-008 / ERR-015 | Provider 429 burst | Capped attempts and controlled admitted load; numeric cap needs confirmation; saved cases retained |
| TST-009 / ERR-012 | Generate missing citations | Needs-review or unsupported outcome; universal branch open; never fabricated approved result |
| TST-010 / ERR-017 | Configured task expiry | No implicit approval; escalation recorded; preserve EXPIRED catalog, exact run effect open |
| TST-011 / ERR-022 presentation | Keyboard-only case opening | No blocked action, visible focus; approved UI recovery layout still open |
| TST-012 / ERR-027 | Reference region exercise | RPO <=15 min/RTO <=4 h with object/relational/index verification |
| TST-013 / ERR-024 | Tenant purge under legal hold | Protected records retained and receipted; no forced held-object removal |
| TST-014 / ERR-014 | Arbitrary MCP invocation | `DENY` before dispatch; no equivalent-tool substitute |
| TST-015 / ERR-008 | Unsafe PDF | Quarantine; no indexing |
| TST-016 / ERR-026 | Canary safety regression | Gate blocks promotion; traffic rollback as applicable, no assumed DB down-migration |

Source: p.89 [c30:f1–f16]; numeric recovery condition p.69 [c22:f10].

### Additional source-supported failure procedures

1. **Validation/concurrency:** Submit schema-invalid request (`422`), stale `If-Match` (`409 CASE_VERSION_CONFLICT`, current revision) and unauthorized write. Verify no accepted mutation/allocation and safe denial evidence; corrected authorized submission must obey idempotency. Missing-key/header tests await approved mappings. [pp.25,54,56,84; c9:f7, c18:f3,f12, c26:f17.]
2. **Poison partial sync:** Exhaust malformed-item attempts; quarantine with reason/correlation/remediation and ledger exception. If continuation policy permits, remaining items proceed; cursor passes only durable preceding outcomes. Replay leaves one accepted outcome, never all-success for failed item. [pp.28–29; c10:f8,f12.]
3. **Low quality versus unsafe:** Quality-policy failure leaves permitted source viewable but unavailable to autonomous recommendation; unsafe source never indexes. Validate anchors/layout/OCR provenance and current permission after reprocessing. [pp.30–32; c11:f5,f8–f12.]
4. **Index and webhook partial failure:** Fail index write after source acceptance; metadata remains and fingerprint/outbox reconciliation repairs. Fail webhook delivery; accepted case remains unchanged while bounded delivery recovery operates. Failed rebuild gates cannot switch alias; queue-empty alone cannot declare readiness. [pp.34,49,55,78; c12:f7, c16:f7, c18:f9, c25:f3.]
5. **Permission races:** Revoke during search or between retrieval/publication. No forbidden model/result release; publication rejects stale evidence. Suspected leak suspends affected aliases/cache until denied probes pass. Preserve audit and do not weaken policy under load. [pp.22–23,27–29,79; c8:f9,f15, c10:f1,f9, c25:f8.]
6. **Degraded integrations:** Generation outage disables new generation and shows degradation while manual/evidence remain. If lexical continuation selected, visible reduced-quality flag required. Attempt unapproved regional fallback and quota-driven model/class change; neither allowed. [pp.37–38,69,79; c13:f3,f9, c22:f8, c25:f7.]
7. **Refresh/replay:** Reconnect authorized SSE using retained `Last-Event-ID`, refresh server progress and ensure no foreign replay. Repeat each chapter event in EH-007; ledger/revision handling yields no reapplication. Expired/future offsets and browser duplicate-rendering expectations await confirmed schema. [pp.48–50,55,58; c16:f5,f13, c18:f8, c19:f7.]
8. **Pool/storage failure:** Exercise successful and failed transactions followed by pooled reuse; no prior tenant scope remains. Test cross-tenant parent linking against selected production mechanism and immutable history edits. Lost heartbeat/object/region fault exercises measure safety and recovery, but lease thresholds/dispositions remain open. [pp.70,85–86; c22:f11, c27:f2,f8–f13.]
9. **Review/rework:** Exact candidate/evidence/model-prompt/policy reasons inspectable; incomplete fields keep decisions disabled; independent hash/duties guards reject stale/self actions. Expiry never approves; rejected rework new revision. Valid publication commits supported matching pointer/gate atomically. [pp.45–46,58,85; c15:f8–f12, c19:f1,f8, c27:f5.]
10. **Controlled lifecycle/release:** Single Admin export fails two-person control; export excludes secrets/prompts; held records retained/receipted. Active-reader incompatible deletion, unverified digest, tampered fixtures, critical security failure and low confidence block promotion. Signed release evidence remains reconstructible. [pp.52,72–76,78–80,88–89; c17:f9, c23:f7–f11, c24:f1,f12, c25:f1,f10–f11, c29:f11–f14, c30:f20.]

### Threat matrix and exit qualification

| Source threat ID | Negative input/procedure | Required control/expected containment |
|---|---|---|
| T-01 | Valid ID with foreign tenant token | RLS plus domain resource guard; non-disclosure |
| T-02 | Hostile PDF paragraph instructions | Evidence delimiting/tool schema pinning; no instruction authority |
| T-03 | Approve prior draft after revision | Artifact-hash binding; stale rejected |
| T-04 | Polyglot PDF/zipped payload | Scan/sandbox/bounded parser; no unsafe index admission |
| T-05 | Observe traces/provider requests | Vault/redacted telemetry; no connector credential disclosure |
| T-06 | Regional provider outage | Allowed deployment registry; no unapproved fallback |
| T-07 | Same event **100 replays** | Idempotency/aggregate revision; one accepted transition |
| T-08 | Revoke source during search | ACL revision invalidation; no stale forbidden evidence |
| T-09 | Historical audit edit | Append-only/hash-chain export; edit denied |
| T-10 | Mutually recursive tool hints | Tool/step/time budget; no unbounded recursion |
| T-11 | Single-Admin export | Two-person approval/manifest gate |
| T-12 | Replace expected score fixtures | Dataset version/signed manifest integrity |

Source p.88 [c29:f1–f12]. ZIP is an attack input, not supported format; 100 is a test count, not retry allowance. `SEC-001`–`SEC-012` remain separate release-blocking namespace with no confirmed one-to-one T/TST mapping. Security-control owner independently reproduces/reviews negative evidence and signs release record; no person/date assigned. Critical isolation/approval tests allow **zero exceptions**; benchmark score cannot offset unmitigated critical failure. [pp.74,88; c24:f1, c29:f13–f14.]

Deterministic state/idempotency/ACL/hash/retry/schema tests avoid live model calls, pin adapters and randomized integration retries leave one outcome. Fixtures cover synthetic successful/empty/mixed-permission/adversarial/malformed inputs; empty fixture coverage does not select every job's empty-result behavior. Record seeds; freeze/version/independently review corpora; signed unit/schema/auth/replay/staging-sync/accessibility/search/grounding/policy/load/DR outputs reference release digest. [pp.74–76,89; c24:f2,f7–f12, c30:f17–f20.]

Reference evaluation `1,200` cases, citation precision `>=0.97`, unsupported claims `<=0.02`, frozen high-risk recall `1.00`, CI/domain-shift reporting and low-confidence release blocking remain conditional design targets. Admission/retry controls are not derived from reference `2,000` users, `60` steady/`180` burst requests/s, `100,000` documents/tenant, `20` concurrent runs/large tenant or typical `1 MB`/`40–120` chunks. [pp.68,75–76; c22:f2–f3, c24:f8–f12.]

## Consistency and Open Questions

### Required decisions and earlier amendments

Do not rewrite earlier files. Amend the affected identifiers when decisions are approved; unresolved choices are not delegated to implementation.

| Open ID / affected requirements | Evidence and required clarification | Earlier links |
|---|---|---|
| ERR-OQ-001 / EH-002, ERR-001–005/011–015/017 | Snake-case p.54 versus uppercase literals pp.25/27/36/38/84/89. Preserve literals; complete every API status/code/envelope field/type/requiredness, SQL translation, safe detail/localization/display and missing key/header errors. [c18:f3–f4, c26:f17–f18, c30:f2–f3] | `01_screen_functions.md` OQ-006; `02_api.md` API-053/API-OQ-003/013; `03_data.md` DAT-035; `05_business_rules.md` BR-OQ-005 |
| ERR-OQ-002 / EH-001/006, ERR-003/006/017/025 | Reject before AccessDenied p.22, mandatory safe audit pp.23/87. Define denial-event order/revision/commit and audit-recording failure without business mutation or suppressed evidence. [c8:f10,f12, c28:f1] | SF-016/OQ-015; API-OQ-013; DAT-OQ-012; BAT-OQ-006; BR-OQ-012 |
| ERR-OQ-003 / ERR-016/017 | Missing-approval termination p.41 vs waiting pp.49/82, task expiry p.45, recoverable timeout p.12 vs FAILED catalog, AUTO_ALLOW p.44 vs linear review. Define timing, state/timeout recovery, expiry/decision race, run effects and AUTO_ALLOW publication edge. [c14:f11, c16:f6, c15:f3,f8, c5:f9, c26:f3] | SF-009/OQ-008; API-OQ-009; DAT-OQ-008; BAT-OQ-004; BR-OQ-010 |
| ERR-OQ-004 / EH-004, ERR-008/013/015/020–023 | Retry counts/delays/jitter/breaker thresholds/reset, queue/token/provider limits, parser/quality/decompression/replay/heartbeat bounds absent. Define versioned values, exhaustion disposition, idempotency scope/arbitration/24h expiry and separate event/SSE retention. | API-OQ-010/012/016; DAT-OQ-013/014; BAT-OQ-003/005; BR-OQ-005/014 |
| ERR-OQ-005 / EH-005/006, ERR-002/003/010/011/017/024 | Map Workspace Admin/Admin, Owner/Member/approver/Operators; complete action/resource/redaction/independence predicates, required review fields, SLA/recipients, override and two-person lifecycle protocol. [pp.11/22/45–46/83/85] | SF-002/OQ-001, SF-010/OQ-012; API-OQ-001/008/014; DAT-OQ-009/015; BAT-OQ-001/008; BR-OQ-002/013/015 |
| ERR-OQ-006 / EH-003/006 | Log levels, trace transport/signing/schema, metric units/windows/alert thresholds and recipients/channels/owners unspecified. Define on-call budget impact, spend tickets, escalation, audit failure and disclosure containment; never expose sensitive values. [pp.62–66/79/90] | API-OQ-013/019; DAT-OQ-016/020; BAT-OQ-005/010; BR-OQ-014/016/018 |
| ERR-OQ-007 / EH-007, ERR-004/019 | Retain alternate `POST /v1/runs` versus case path; workspace settings associated with case PATCH; generic GET/health/OpenAPI allocation/events; provisioning/export-delete associations. Clarify each cause/mode; no invented GET mutation/alias/endpoint. | API-OQ-005/006/007/019; DAT-OQ-004/011; BAT-OQ-007; BR-OQ-019; SF-014/OQ-015 |
| ERR-OQ-008 / EH-001/007 | Mutable current case pp.24–25 vs Case/CaseService/CaseAggregate immutable registers pp.13/17/26; task/sync/alias/form labels vs lifecycle. Amend immutable content/revision vs mutable pointer/control scope, retain exact register terminology. | SF-006/OQ-009; API-OQ-006/012; DAT-OQ-002/010; BAT-OQ-006; BR-OQ-020 |
| ERR-OQ-009 / ERR-007–012/014/018/022 | Cap units/equality/quality/anchor/hash/OCR choices, Citation schema/tool requiredness/min/defaults, A2A output/decline/deadline/case_demo typing, signed-URL renewal and already-open revocation behavior missing. | SF-007/OQ-010; API-OQ-011/015; DAT-OQ-005/007/014; BAT-OQ-009; BR-OQ-006/008/009 |
| ERR-OQ-010 / ERR-020–027 | Internal persistence/reset/worker/object/vault/identity outage disposition, concurrency/leases/partial-empty results, hold/receipt/archive/checksum/restore sequence and recovery grants missing. No generic compensation permitted. | DAT-OQ-001/003/015/020; API-OQ-014/017/019; BAT-OQ-003/008/010; BR-OQ-015/018 |
| ERR-OQ-011 / Failure Acceptance | Within300 p.12 vs under300 p.65; availability denominator/load, CI/low-confidence/regression/fingerprint/probe methods and boundaries missing. Confirm measured criteria without rounding failures into pass. [c5:f9, c21:f7, c24:f9,f12] | SF OQ-017; API-OQ-016/019; DAT-OQ-018/020; BAT-OQ-010; BR-OQ-018 |
| ERR-OQ-012 / EH-005 | Screen routes/action/error/loading/empty/recovery placement and representative alias/title mismatches unresolved. Eight screens only; no new login/recovery/evaluation/export screen inferred. | SF-004/OQ-003/004/005/008; API-OQ-018; DAT-OQ-017; BR-OQ-017 |
| ERR-OQ-013 / EH-001/006 | Production workspace tenancy FK vs controlled write, token/session/identity choices, provider/region/search/model approval/corporate retention/connector permissions and encryption isolation/rotation unresolved. [pp.10/21/86/90; c4:f13, c8:f2–f3, c27:f13, c31:f13] | SF OQ-018; API-OQ-002/017; DAT-OQ-003/019; BAT-OQ-011; BR-OQ-021 |

### Example-only settings and remaining dependencies

Appendix F p.90 preserves exact examples: `release: r1.0`; `max_plan_depth: 8`, `max_tool_calls: 16`, `run_timeout_seconds: 180`, `replay_dedup_hours: 24`; `max_candidate_chunks: 80`, `max_selected_chunks: 10`, `embed_dimension: 1536`, `hybrid_rrf_k: 60`; `auto_publish_classification: INTERNAL`, `require_human_review_for: [HIGH_RISK, RESTRICTED]`, `self_approval_allowed: false`; `upload_limit_mb: 25`, `user_data_region: primary-approved-region`; `trace_sample_rate: 0.10`, `diagnostic_retention_days: 30`, `audit_retention_years: 7`. [c31:f1–f6.]

Independent chapter evidence confirms depth eight/calls sixteen, 1536 embedding dimension, configurable 25 MB file cap, actor/fingerprint 24-hour outcome and substantive task-wide no-self-approval/diagnostic/audit policy only in their scopes. Timeout180/candidates80/global selected10/RRF60/sampling0.10/auto-publishINTERNAL/placeholderregion remain **examples**, not selected exception policies. MCP `int<=10` is tool-specific. Database `1`, `'INTERNAL'`, `now()` remain persistence defaults, not UI values or retry decisions. [pp.25/30/34/40/66/85–87; c9:f8, c11:f2, c12:f2, c14:f7, c21:f11, c27:f5,f10, c28:f7.]

Before implementation lock, source requires dated region/search/identity/approved-model/corporate-retention/connector-permission choices; encryption-key isolation/rotation tradeoff must be resolved before enterprise general availability. No decision, owner, calendar deadline or approval is invented. [pp.10,90; c4:f13, c31:f13.]

This is Stage 6. Remaining stage details are **To be defined in a later stage**; no later specification is presumed completed. Stage 8 must consolidate ERR/EH/ERR-OQ and linked prior identifiers in `08_architecture_decision.md`, linking `06_exception_handling.md` and the affected completed filenames. Earlier references to later exception handling now resolve to this provisional file; unresolved API-053 mappings remain open rather than silently filled. The candidate requires separate root approval.
