# 6. Exception Handling Specification

## Exception Inventory and Classification

### Baseline and Evidence Status

This specification defines exception handling for OrionDesk AI **OD-AI-DDS-001, R1.0 / revision 1.3**.

**Source** means `1794310747-OrionDesk_AI_Detailed_Design_Specification.pdf`. Citations refer to original PDF pages and sections.

- **Confirmed:** Explicit source-supported handling or invariant.
- **Needs confirmation:** An unspecified contract, threshold, state, permission or recovery choice. It must be resolved before implementation lock.
- **Proposal:** A suggested interaction or implementation approach, not an approved requirement.

`ERR-*` identifiers identify exception scenarios; they are not new wire error codes. Exact source codes and test identifiers are preserved.

Mappings reference the completed specifications:

- [01_screen_functions.md](01_screen_functions.md): `SCR-*`, `SF-*`.
- [02_api.md](02_api.md): `API-*`, `API-R-*`.
- [03_data.md](03_data.md): `DAT-*`, `DAT-R-*`.
- [04_batch_functions.md](04_batch_functions.md): `BAT-*`, `BAT-R-*`.
- [05_business_rules.md](05_business_rules.md): `BR-*`.

### Shared Safety Requirements

**ERR-R-001 — Confirmed:** Oversized uploads, prompt injection, cross-tenant identifiers, stale approvals and ungrounded recommendations fail closed with stable, non-sensitive errors. Partial processing must never appear as an approved answer. Recovery, replay and degraded operation do not bypass authorization or publication gates.  
**Evidence:** Source, p. 13, §2.3.2; pp. 45–46, §12.3; pp. 68–70, Chapter 19.

**ERR-R-002 — Confirmed:** Stale or unauthorized writes leave business state unchanged and do not produce another accepted business transition. Denied-attempt audit evidence is distinct from accepted-transition evidence. Duplicate deliveries are recorded without reapplying mutations.  
**Evidence:** Source, pp. 17, 25–26, 48–50; chapter design checkpoints and failure-mode sections.

### Exception Inventory

Detection conditions and affected behavior below are Confirmed unless explicitly marked otherwise. Scope identifies the affected operation or resource, not an authorization to interrupt an entire tenant or platform.

| ID | Exception and category | Occurrence location / detection condition | Affected scope and preceding identifiers | Evidence |
|---|---|---|---|---|
| ERR-001 | Schema-invalid input — invalid input | Request or tool arguments fail the versioned contract; validation occurs before transaction entry and tool dispatch | Applicable screens/APIs/jobs; DAT-036; BR-001, BR-005, BR-019 | Source, pp. 54–56, §§15.1.1, 15.3 |
| ERR-002 | Invalid authentication — permission violation | Token validation fails, including unexpected algorithm or missing tenancy claim | All protected boundaries; AUTH-P/I/T; DAT-019; all tenant-owned jobs; BR-001–002 | Source, pp. 18, 21–22 |
| ERR-003 | Unauthorized, foreign-tenant or unavailable resource — permission violation | Role/resource attributes fail; foreign-tenant ID substitution; soft-deleted entity requested | All resource screens/APIs; DAT-R-005; BAT-R-001–002; BR-001–002, BR-013 | Source, pp. 22–23, 51, 86 |
| ERR-004 | `CASE_VERSION_CONFLICT` / stale configuration — business rule violation | `If-Match` differs from current case revision, or configuration revision precondition fails | SCR-002-E02, SCR-007-E01; API-004, API-050; DAT-002–004; domain mutations; BR-003 | Source, pp. 24–25, 83–84 |
| ERR-005 | `IDEMPOTENCY_CONFLICT` — business rule violation | Same creation key reused with changed request fingerprint | SCR-001-E04 and long-running creation; API-R-007; DAT-027; applicable jobs; BR-004 | Source, pp. 25, 54, 89 |
| ERR-006 | Duplicate or delayed execution — replay condition | Event ledger/operation key already processed, or aggregate revision stale | All event consumers, BAT-010; DAT-014, DAT-027; API-R-008; BR-004–005 | Source, pp. 17, 48–50; p. 88, `T-07` |
| ERR-007 | Invalid or oversized file — invalid input/security | Unsupported format, MIME/extension disagreement, configured per-file cap or decompression threshold violated | SCR-002-E04; API-006–007; DAT-020, DAT-022; BAT-003; BR-014 | Source, pp. 13, 30, §8.1 |
| ERR-008 | Unsafe file — security violation | Malware/active-content or malicious parsing fixture detected | SCR-002-F15–F16; API-006–007; DAT-022; BAT-003–004; BR-014 | Source, p. 30; pp. 88–89, `T-04`, `TST-015` |
| ERR-009 | Poison connector record / partial sync — external/input failure | Malformed document remains unsuccessful after bounded retries; preceding item lacks durable outcome | SCR-006; API-018–019, API-048; DAT-015, DAT-021–022; BAT-002; BR-012 | Source, pp. 28–29 |
| ERR-010 | Low extraction quality — quality exception | Empty-page, unknown-character, table-loss or language-confidence quality gate fails | SCR-003-F08–F09; API-007; DAT-022; BAT-003–004; BR-015 | Source, pp. 31–32 |
| ERR-011 | Unsupported connector capability — integration degradation | Connector lacks advertised `list`, `fetch`, delta cursor, ACL or delete support | SCR-006-F02; API-048; DAT-021; BAT-002; BR-012 | Source, p. 27, §7.1.1 |
| ERR-012 | `CONNECTOR_REAUTH_REQUIRED` — permission/integration failure | Workspace-scoped connector credentials revoked while work is queued | SCR-006-E03; API-018–019, API-055; DAT-021; BAT-002; BR-012 | Source, p. 27, §7.1.2 |
| ERR-013 | Provider throttling / admission rejection — external/capacity failure | Provider throttles; workspace tokens, queue age or provider capacity do not satisfy admission thresholds | SCR-002-E05, SCR-006; API-008–009, API-042, API-048–049; DAT-031; BAT-002, BAT-008; BR-020 | Source, pp. 28, 69, 89 |
| ERR-014 | Current-run quota exhaustion — business capacity violation | Reserved/available workspace quota exhausted during run | SCR-004; API-036, API-049/run outcome; DAT-008, DAT-016; BAT-008; BR-020 | Source, p. 38, §10.3.1 |
| ERR-015 | `NO_SUPPORTED_EVIDENCE` / missing grounding — business quality failure | Retrieval confidence/evidence quality insufficient, or response lacks required citations | SCR-002–003, SCR-005; API-013–015, API-045; DAT-010; BAT-008; BR-016, BR-024 | Source, p. 36; p. 89, `TST-009` |
| ERR-016 | Invalid/nonresolvable citation — validation failure | Citation cannot be verified against stored anchor/current permission | SCR-003-E03, SCR-005; API-014–015, API-054; DAT-007, DAT-010; BAT-008; BR-015–016 | Source, pp. 31, 35, 57 |
| ERR-017 | `MODEL_OUTPUT_INVALID` — external output validation failure | Versioned JSON parsing fails, including unknown fields, invalid citations or control-character injection | SCR-004-E05; API-036/run outcome; DAT-024; BAT-008; BR-018 | Source, p. 38; p. 89, `TST-005` |
| ERR-018 | Prompt injection / unauthorized tool or route — security violation | Evidence contains hostile directives; arbitrary/forged capability requested; fallback route unapproved | SCR-004; API-036, API-045–046, API-049; DAT-024–025; BAT-008; BR-017–019, BR-033 | Source, pp. 37–42, 61, 87–89 |
| ERR-019 | Invalid plan, exhausted calls, policy stop or deadline expiry — workflow failure | Missing required approval, repeated invalid plans, exhausted call budget, policy denial or expired deadline | SCR-004-F05; API-008–011, API-037; DAT-008–009, DAT-017; BAT-008; BR-019, BR-021–024 | Source, pp. 12, 40–42, 49 |
| ERR-020 | Stale artifact decision — business conflict | Submitted approval hash differs from exact current reviewed artifact | SCR-005-E02; API-017; DAT-011–012, DAT-026; BAT-008; BR-022, BR-024 | Source, pp. 45–46, 83, 89 |
| ERR-021 | Ineligible/incomplete review or override — permission/input violation | Self-approval, pool/minimum-role/separation failure; required fields incomplete; override lacks required controls | SCR-005; API-017, API-052; DAT-011–012; BAT-008; BR-022–023 | Source, pp. 11, 45–46, 58, 85 |
| ERR-022 | Review expiry — business timeout | Configured task SLA expires | SCR-005-E03; API-016–017; DAT-011, DAT-026; BAT-009; BR-023 | Source, p. 45; p. 89, `TST-010` |
| ERR-023 | Revoked evidence / suspected ACL leak — security failure | Permissions change after retrieval/review; stale visibility detected | SCR-003, SCR-005; API-013–017; DAT-019, DAT-023, DAT-028; BAT-007–008; BR-013, BR-024, BR-029 | Source, pp. 28, 46, 53, 79 |
| ERR-024 | Dependency unavailable / ambiguous transport outcome — external/internal failure | Connector, model, object store, DB or service cannot complete request; response lost after execution | Applicable APIs/jobs; API-R-004–009, API-R-013; DAT-027; BR-004–005, BR-030 | Source, pp. 12, 16–17, 49, 52, 70 |
| ERR-025 | Transaction/outbox or indexing-link failure — internal partial failure | Required ACID commit fails; index write or message link fails after source acceptance | SCR-002, SCR-006; mutation APIs; DAT-003–004, DAT-014, DAT-023; BAT-004–006, BAT-010; BR-005 | Source, pp. 49, 52, 90 |
| ERR-026 | Generation/vector integration unavailable — degraded service | Generation unavailable or vector index degraded | SCR-002–003, SCR-004; API-031; DAT-023, DAT-031; BAT-008; BR-029 | Source, pp. 69, 79 |
| ERR-027 | Stream interruption / invalid cursor — observation failure | SSE disconnect; pagination cursor or retained offset invalid/expired; invalid/expired handling Needs confirmation | SCR-001, SCR-004, SCR-008; API-002, API-012, API-021; DAT-028; BR-032 | Source, pp. 54–55, 58 |
| ERR-028 | Lost worker / primary-region outage — internal infrastructure failure | Lost heartbeat or primary-region outage under fault injection | Run/job observation; API-037, API-042; DAT-031; BAT-019 and affected jobs; BR-029 | Source, pp. 19, 69–70 |
| ERR-029 | Incomplete provisioning/readiness — internal partial failure | Provisioning incomplete; queue empty without adequate index coverage | SCR-006-F07–F08; API-056, API-018; DAT-034; BAT-011–012; BR-011 | Source, p. 78 |
| ERR-030 | Export/delete authority or legal-hold exception — permission/business failure | Missing independent approval check, ineligible case retention, or protected object in purge inventory | SF-014; API-025–026, API-040; DAT-018, DAT-029, DAT-034; BAT-013–014; BR-025–026 | Source, pp. 26, 78–80, 89 |
| ERR-031 | Webhook delivery failure — external partial failure | Optional signed notification cannot be delivered/validated by recipient | API-047; DAT-028; BAT-020; BR-032 | Source, p. 55 |
| ERR-032 | Audit/secret-control violation — security/internal failure | Historical-edit attempt, out-of-scope secret disclosure, or audit integrity failure; integrity-failure recovery Needs confirmation | SCR-008; API-021/provider/output boundaries; DAT-013, DAT-029–030; BAT-017; BR-027 | Source, pp. 54, 61–64, 84, 88 |
| ERR-033 | Release/evaluation regression or incompatibility — release failure | Regressed safety/canary metrics, low statistical confidence, poisoned fixtures, incompatible schema or unverified build | SCR-010; API-023–024, API-043–044; DAT-032–033; BAT-016, BAT-018; BR-031 | Source, pp. 55, 72–76, 88–89 |

## Handling by Exception

### Canonical Response and Dispatch Procedure

**ERR-R-003 — Confirmed:** Preserve the canonical error envelope and safe structured details. No diagnostic or user-facing failure may include connector credentials, full prompts, retrieved documents or unauthorized resource existence.  
**Evidence:** Source, p. 84, §A.3; p. 64, §18.1.

| Field | Type evidence | Handling constraint |
|---|---|---|
| `error` | Object | Canonical root |
| `error.code` | String | Stable machine-readable literal |
| `error.message` | String | Non-sensitive description |
| `error.correlation_id` | String | Support correlation reference |
| `error.retryable` | Boolean | Explicit retry guidance |
| `error.details` | Object, optional | Safe validation/conflict details only |
| `expected_revision`, `actual_revision` | Integers in source example | Safe revision details for authorized case conflict |

Complete requiredness, lengths and per-code details schemas **Need confirmation** through controlled IDL; this table does not replace API-R-018.

Source-confirmed example, with illustrative values:

```http
HTTP/1.1 409 Conflict
Content-Type: application/json
```

```json
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

**ERR-R-004 — Confirmed handling procedure:**

1. Authenticate and establish tenant, actor, trace and correlation context.
2. Validate the request before transaction entry/operation allocation and validate tool arguments before dispatch.
3. Resolve current resource authorization and domain invariants.
4. On permanent validation or permission failure, reject without automatic retry.
5. On duplicate execution, consult event/operation ledger and revision guards; return/record the existing outcome without a second mutation.
6. For accepted mutations, retain required ACID/outbox and checkpoint boundaries.
7. For transient faults, apply bounded recovery without weakening authorization, idempotency or data-handling restrictions.
8. Return the documented safe error or an actually persisted asynchronous operation identity. Never fabricate completion or an unpersisted job.
9. Make run failures visible at the exact failed checkpoint; distinguish observation failure from execution failure.

**Evidence:** Source, pp. 15–17, 21–25, 40–42, 48–56, 58.

### Request, Identity and Replay Handling — ERR-001–006

| Exception | Response and display | Interruption/data handling | Retry, rerun and recovery |
|---|---|---|---|
| ERR-001 | Confirmed HTTP `422` for schema-invalid request; code and field-detail mapping Need confirmation. Safe error in affected screen; exact layout/copy Needs confirmation | Reject invalid operation before protected processing/transaction; no accepted business mutation | Permanent validation failure is not automatically retried. Proposal: correct fields and submit a newly valid request |
| ERR-002 | Rejection Confirmed; HTTP/code and session-expiry display Need confirmation | No protected operation under invalid identity; never infer tenant from untrusted payload | Authentication/session recovery contract Needs confirmation. Do not retry unchanged invalid credentials as a transient fault |
| ERR-003 | Foreign-tenant case: `404`-equivalent, same class as absent ID. Other denial HTTP/code Need confirmation; no private existence disclosure | Reject unauthorized mutation; no returned forbidden chunks; soft-deleted objects not retrievable; reset pooled tenant context after every transaction | Permission failures are permanent, not automatically retried. Any later authorized request is reevaluated under current scope |
| ERR-004 | Case: `409 CASE_VERSION_CONFLICT`, current revision; `retryable: false` in canonical example. Configuration code/status Need confirmation | Current case/configuration remains unchanged; no accepted-transition event | Proposal: refetch authorized current revision, reconcile intent and resubmit with valid precondition; no blind overwrite. Unsaved-input UX Needs confirmation |
| ERR-005 | `IDEMPOTENCY_CONFLICT`; HTTP `409` Confirmed for case creation | No second creation or changed-intent mutation under reused key | Key/fingerprint mismatch is not transient recovery. Proposal: restore original pairing or use a new key for genuinely new intent |
| ERR-006 | Identical creation replay returns original operation/outcome. Event consumer records duplicate outcome and returns | Exactly one accepted transition and its accepted-transition audit record; no second side effect; delayed stale revision cannot overwrite current state | Replays preserve original event identity. Ledger namespace, retention, in-flight race response and stale-revision acknowledgement Need confirmation |

**Evidence:** Source, pp. 21–26, 48–50, 54–56, 84–86, 89.

Case idempotency retains actor/request-fingerprint outcome for **24 hours**. Expiration equality, failed-outcome retention and behavior after expiry **Need confirmation**. This is not a universal deduplication TTL.

### File and Connector Handling — ERR-007–012

| Exception | Response/display and continuation | Data handling and recovery | Open handling details |
|---|---|---|---|
| ERR-007 | Fail closed for unsupported/type-mismatched/oversized/decompression-threshold input. Upload HTTP/code Needs confirmation | Do not process as an accepted supported file. Validation failures are not automatically retried | Reject-versus-quarantine classification, MB byte basis, equality at 25 MB, bomb metric/threshold, zero-byte/invalid UTF-8 handling |
| ERR-008 | Unsafe accepted payload becomes `QUARANTINED`; show safe processing state, not `READY` | Scan before parsing; macros disabled; remote references not fetched; no indexing | Safe reason vocabulary, scanner outage policy beyond fail-closed safety, remediation permission and release-from-quarantine process |
| ERR-009 | After bounded retries, quarantine malformed record with reason, correlation ID and remediation path. Remaining batch may proceed | Persist cursor/high-watermark/error ledger; cursor advances only after all preceding outcomes are durable, including recorded quarantine exception. Partial batches retry safely | Retry cap/classification, per-item commit unit, partial-success enum, cursor expiration and concurrent cursor ownership |
| ERR-010 | Low-quality documents remain authorized-viewable; autonomous recommendations exclude them | Preserve quality flags and immutable provenance. OCR only opt-in; reprocess changed pipeline side by side without rewriting prior derivatives | Quality thresholds, empty-document state, manual-review eligibility, UI warning placement |
| ERR-011 | Explicit user-visible warning and lower-trust ingestion mode; no silent assumption of support | Continue only according to permitted lower-trust policy, whose allowed uses Need confirmation | Trust-mode enum, blocked capabilities, remediation controls and HTTP/code |
| ERR-012 | `CONNECTOR_REAUTH_REQUIRED` for revoked-credential queued work; no tokens in output | Fail affected queued work; preserve already durable source outcomes and safe sync history | HTTP mapping, final retryability field, reauthorization endpoint and controlled requeue behavior |

**Evidence:** Source, pp. 27–32, §§7.1–7.3, 8.1–8.3; p. 89.

The bounded malformed-record retries in ERR-009 are not permission to retry every permanent request validation or authorization denial. The classification boundary **Needs confirmation**.

### AI Admission, Grounding and Workflow Handling — ERR-013–019

| Exception | Response/display | Interruption and data effects | Retry/recovery constraints |
|---|---|---|---|
| ERR-013 | Throttled new AI-run clients receive `429` plus `Retry-After`; saved cases remain accessible. Provider-throttle translation code Needs confirmation | Control admitted load and workspace quotas; fair scheduling avoids starvation | Honor provider `Retry-After`; bounded exponential backoff/jitter and per-dependency circuit breakers. Delay parsing, attempts and thresholds Need confirmation |
| ERR-014 | Current run terminates; exact business code/HTTP mapping Needs confirmation | No publication; retain safe checkpoint/usage lineage; no automatic model or data-class switch | Same exhausted run cannot continue by bypassing quota. Reservation release/reconciliation and later new-run eligibility Need confirmation |
| ERR-015 | Retrieval returns `NO_SUPPORTED_EVIDENCE`; missing-citation generation produces needs-review or unsupported outcome, never falsely approved output | Do not fabricate context; evidence/generation/policy/review remain distinct records | Clarification or human routing is allowed, but selection/trigger and state mapping Need confirmation. Blind retry of unchanged insufficient evidence is not a confirmed recovery policy |
| ERR-016 | Do not display an invalid/revoked citation as verified or use it as valid grounding | Citation requires resolvable stored anchor and current permission. Invalid model citations also trigger ERR-017 | Source-access failures distinguish temporary dependency faults from revoked authorization. Exact viewer display, signed-URL renewal and HTTP/code Need confirmation |
| ERR-017 | `MODEL_OUTPUT_INVALID`; show safe failed checkpoint; no publication | Preserve separation between invalid output and approved artifact; no final pointer/gate advancement | Gateway parsing uses bounded retries. Retry cap, terminal retryability, attempted-output retention/redaction and provider charge reconciliation Need confirmation |
| ERR-018 | Strip tool directives from evidence contexts, record injection indicators, deny unauthorized dispatch. `DENY` is a policy/test outcome, not a confirmed HTTP error code | Evidence/model text never changes tenant/grants/approval. No arbitrary tools, URLs or filesystem access. No unapproved fallback route | Never substitute semantically equivalent tool for denied action. Fallback only to approved equal-or-stronger data-handling class; no retry of permission denial |
| ERR-019 | Stop at missing approval, exhausted call budget, repeated invalid plan, policy denial or deadline expiry; exact failed checkpoint visible | Persist plan revision before effects and stage checkpoints before dispatch; no partial-as-approved output | Depth maximum eight; tool invocations maximum sixteen. Reads may retry transient faults; consequential mutations require idempotency/human authorization. Stop codes, timeout recovery and A2A decline handling Need confirmation |

**Evidence:** Source, pp. 12–13, 31, 35–42, 49, 69, 87–89.

**Timeout boundary — Needs confirmation:** The source requires a run to become terminal within its configured maximum or yield a recoverable timeout state, but the canonical run vocabulary supplies no separate timeout state. Appendix F `run_timeout_seconds: 180` is example configuration, not a settled universal timeout. Valid `AWAITING_REVIEW` must not automatically be treated as missing-approval failure. Human-wait coverage, time clock, retry budget consumption and recovery endpoint remain unresolved.

### Review and Publication Handling — ERR-020–023

| Exception | Response and screen behavior | Data effects / continuation | Recovery |
|---|---|---|---|
| ERR-020 | Changed/wrong artifact approval rejected as stale; `409` supported; rejection audited. Specific error literal Needs confirmation | No accepted decision authorizing changed content and no publication under old hash; historical decisions remain immutable | Proposal: reload current authorized task/artifact and conduct review again; repeated decision and assignment races Need confirmation |
| ERR-021 | Reject ineligible decision/self-approval. Disable both Approve and Reject until required fields complete; server validates independently | No gate authority from missing fields, wrong role/pool or failed segregation. Override requires elevated role, secondary reviewer and audited reason | Permission failures not automatically retried. Required-field set/rationale rule and denial HTTP/code Need confirmation |
| ERR-022 | Task expires; record reassignment or escalation, never silent approval | Preserve expiry/assignment lineage; do not present expiry as accepted review/publication | Configured routing executes; duration, calendar, decision-versus-expiry winner and repeated escalation Need confirmation |
| ERR-023 | Filter revoked evidence before next retrieval; publication recomputes authorization and rejects stale evidence | Invalidate affected caches before ordinary TTL/new results. For suspected leak, suspend affected aliases and revoke cached evidence while preserving audit | Scoped ACL-revision replay; reenable search only after negative access tests pass. No permission-bypass retry; code, race protocol and incident routing Need confirmation |

**Evidence:** Source, pp. 11, 28, 44–46, 53, 58, 79, 85, 89.

**ERR-R-005 — Confirmed:** Final response pointer and satisfied publication gate update in the same transaction. A failed or rejected publication cannot expose a new final pointer without the gate. An accepted reviewer decision does not independently prove publication completion. Denied drafts may be reworked as new run revisions, never retroactively marked approved.  
**Evidence:** Source, pp. 12, 45–46; API-R-006; DAT-R-008; BR-024.

### Dependency, Partial Failure and Recovery Handling — ERR-024–029

| Exception | Required response/display | Rollback/continuation | Recovery and unresolved choices |
|---|---|---|---|
| ERR-024 | Documented retryable error or actually persisted asynchronous job identity; exact HTTP/code Needs confirmation | Never ambiguous success. Accepted durable work remains distinguishable from completed work | Bounded transient retry. Lost-response replay uses original identity and idempotency safeguards; reconciliation for ambiguous provider side effects Needs confirmation |
| ERR-025 | Safe error for failed atomic commit; downstream failure is not source-acceptance rollback | Required business mutation/approval/outbox commit remains atomic. Failed index preserves accepted source metadata | Compare fingerprints and retry index writes; repair broken links from outbox ledger. No global distributed transaction assumed; lock/commit units and final failure enum Need confirmation |
| ERR-026 | Display degradation; new generation admission disabled during provider outage. Permitted lexical-only retrieval visibly reduced quality | Manual editing/evidence search remain online where supported; no approval/auth bypass | Approved fallback constraints remain. Outage status/code, recovery/re-admission criteria and lexical fallback enablement policy Need confirmation |
| ERR-027 | SSE resumes with `Last-Event-ID` and scope-safe retained backfill; refresh reads server state | Disconnect alone does not establish run failure and must not recreate execution | Retention, heartbeat, session expiry, stale/invalid offset and cursor HTTP/code Need confirmation. Proposal: resynchronize from authorized server state without new mutation |
| ERR-028 | Fault injection must measure safety/recovery time; exact failure display/status Needs confirmation | Checkpoint/idempotency safety survives worker loss. Persistent R1 writes target primary region | Restore warm-region snapshots only under incident command; verify objects/relational data/index recipes together. RPO `<=15 minutes`, RTO `<=4 hours`; heartbeat lease/takeover and restore steps Need confirmation |
| ERR-029 | Incomplete provisioning visible and blocks sync; queue emptiness alone not readiness | Idempotent provisioning retains required policy/key references/roles/quotas/connector stubs; bounded backfill retains stable IDs/receipts | Step compensation, restart selection, empty-history outcome, coverage formula/threshold and status endpoint Need confirmation |

**Evidence:** Source, pp. 12, 17, 19, 49–55, 58, 69–70, 78–79.

Ordinary GET failures must not silently become undocumented asynchronous jobs or emit mutation events. The repeated interface wording does not resolve such a read-conversion contract.

### Governance, Notifications and Release Handling — ERR-030–033

| Exception | Required handling | Rollback, retry and recovery | Needs confirmation |
|---|---|---|---|
| ERR-030 | Single Admin cannot satisfy independent export/delete checks. Routine case retention selects eligible closed cases only. Held records retained and receipted | Eligible deletion writes tombstones/removes blobs and indexes/records receipts. No force purge to “recover” held inventory. Export excludes secrets/internal prompts | Denial HTTP/code, approval validity, routine-retention authority, partial/all-held status, partial purge/export retry, backup/shared-source treatment and cleanup |
| ERR-031 | Optional outbound webhooks signed/retried exponentially; recipients verify signature and event age | Delivery failure never rolls back committed internal transition | Retry cap/deadline, recipient status mapping, signature/event-age bound, terminal delivery state and notification recipients |
| ERR-032 | Deny historical audit/review edits; prohibit out-of-scope secrets in provider calls, responses and diagnostics | Preserve append-only batch-hash chain/independent archive; never alter historical decision as recovery | Integrity-failure detection/repair, vault rotation failure recovery, disclosure containment, audit-service outage policy, status/code and recipients |
| ERR-033 | Block promotion for regressed safety, low confidence or unmitigated critical isolation/approval findings; fixture version/signed manifest protects expected scores | Canary regression rolls traffic back, not automatic DB down-migration. Binary/data compensation only explicitly supported. Active readers retain required fields | Canary/statistical thresholds, evaluation failure/partial-result state, migration repair, rollback readability and error/notification contracts |

**Evidence:** Source, pp. 20, 26, 55, 62–66, 72–76, 78–80, 88–89.

No new financial-transaction compensation workflow is specified: irreversible financial transactions are explicitly excluded by Source, p. 9, §1.2.1.

### Retry and Rerun Contract

**ERR-R-006 — Confirmed:**

1. Classify validation/permission failures as permanent and do not automatically retry them.
2. Use bounded exponential backoff, randomized jitter and per-dependency circuit breakers for transient failures.
3. Honor connector provider `Retry-After` and enforce quotas/fair scheduling.
4. Preserve operation/event identity, tenant scope and aggregate revision through retries.
5. Resume durable workflow stages from checkpoints rather than browser memory.
6. Require operator reason, dry-run validation and scope limit for dead-letter replay.
7. Preserve original event identity unless schema migration has explicit provenance.
8. Do not rerun previously accepted consequential side effects without applicable idempotency and human authorization.

**Evidence:** Source, pp. 17, 28–29, 40–42, 48–50, 54–55.

| Required configuration | Status |
|---|---|
| Per-dependency timeout, attempt cap, base/max delay, jitter distribution and circuit open/reset thresholds | Needs confirmation |
| Coordination of client, gateway and worker retry budgets | Needs confirmation |
| Persisted retry counters and dead-letter eligibility | Needs confirmation |
| Public retry controls, cancel/resume endpoints and terminal-run restart policy | Needs confirmation |
| Deduplication retention sufficient for delayed replay and worker restart | Needs confirmation |
| Malformed-record versus request-validation retry classification | Needs confirmation |

These gaps do not authorize infinite retries, arbitrary constants or the application of the 180-second example to all jobs.

## Logging, Monitoring, and Operations

### Recorded Evidence and Sensitive Values

**ERR-R-007 — Confirmed:** Requests carry `trace_id` and `correlation_id`; child spans correlate DB, connector, retrieval, model and approval stages. Correlation crosses boundaries independently of provider trace IDs. Diagnostic traces contain identifiers/policy outcomes, not user documents or API secrets.  
**Evidence:** Source, p. 16, §3.3.1; p. 64, §18.1.1.

| Record content | Required use / restriction | Evidence |
|---|---|---|
| Tenant, revision, actor, occurrence time, correlation context | Durable mutation/recovery lineage; authorized server context, not untrusted client authority | Source, chapter interface boundaries |
| `event_id`, aggregate identity/revision, schema version and trace | Deduplication, delayed delivery and replay inspection; preserve canonical event contract | Source, pp. 48, 87 |
| Principal and denied resource class | Denial audit without private resource existence | Source, p. 23 |
| Action and policy digest/outcome | `AccessDenied` alert enrichment; reproducible policy inspection | Source, pp. 44, 64, 87 |
| Failed checkpoint, run/plan revision | Visible exact failure and scoped recovery | Source, pp. 40–41, 49 |
| Quarantine reason, correlation ID, remediation path | Malformed-record diagnosis without unsafe content disclosure | Source, p. 29 |
| Provider usage, token counts, deployment version, digests | Attributed diagnostics; no full prompts by default | Source, pp. 38, 62, 65 |
| Source fingerprint/index generation/ACL revision, outbox lag/parser flags | Delayed-indexing diagnosis and verification | Source, p. 90, §F.1 |
| Replay reason, dry-run validation, bounded scope and migration provenance | Controlled operator recovery | Source, p. 50 |
| Purge completion receipts and hold exceptions | Auditable eligible removal/protected retention | Source, pp. 66, 80 |
| Incident audit IDs, time window, blast radius, quality effect, preventive action | Incident closure documentation | Source, p. 90 |

Exact exception-log schema, required per-scenario fields, stack-trace sanitization, cardinality, sampling and log-level assignments **Need confirmation**. No `INFO`, `WARN`, `ERROR` or severity number is source-confirmed.

Diagnostic logs have a **30-day default TTL**; security audit follows a distinct **seven-year policy**. Audit entries are append-only, batch-hash chained and exported to independently controlled retention storage. Operational job-history/dead-letter retention is not supplied.  
**Evidence:** Source, pp. 62, 66.

### Monitoring and Notifications

| Signal / condition | Confirmed action | Recipients and thresholds |
|---|---|---|
| Request/error rate, latency, saturation | Monitor golden signals | Metric names/windows/thresholds Need confirmation |
| Grounding pass rate, retrieval empty rate, provider throttling, tokens, approval backlog age | Monitor AI-specific signals | Per-domain thresholds and alert aggregation Need confirmation |
| Oldest queue age/index backlog | Alert; identify tenant/index generation | Channel/recipient/threshold Needs confirmation |
| User-impacting failure budgets, stale ACL propagation, missing approval enforcement | Paging conditions | Exact on-call/security routing, burn-rate threshold and deduplication Need confirmation |
| Model provider outage | Disable new generation; display degradation; page on-call only when availability budget impacted | On-call identity/channel and budget calculation Need confirmation |
| Routine token-spend anomaly | Create ticket with configured owner/threshold | Owner, threshold and ticket destination not supplied |
| Review expiry | Record policy reassignment/escalation | Pools/escalation recipient/SLA Need confirmation |
| Ordinary validation, duplicate delivery, quarantine, hold exception or webhook exhaustion | Logging/handling as specified above | No automatic page/email recipient confirmed; notification policy Needs confirmation |

**Evidence:** Source, pp. 64–66, 79, 90.

The availability target is **99.9% monthly**. Case-create P95 “within/under 300 ms” has unresolved equality; search P95 is **under 1.5 s excluding remote connector fetch**. These objectives do not establish dependency timeout values or paging thresholds.

### Operator Inspection and Recovery Procedures

#### OPS-ERR-001 — Delayed Indexing / Broken Outbox Link

1. Detect oldest-queue-age/index-backlog alert and identify affected tenant/index generation.
2. Pause only faulty connector or indexer shard; preserve accepted source records.
3. Inspect event ID, outbox lag, parser flags, search throttling and source ACL revision.
4. Replay validated outbox records using a bounded operator-controlled job.
5. Compare source fingerprints against indexed versions and run denied-access probes.
6. Close/document the incident with audit IDs, time window, blast radius, quality effect and preventive action.

**Confirmed evidence:** Source, p. 90, §F.1.  
**Needs confirmation:** Pause interface, operator grants, replay selection/limit, verification thresholds and incident tooling. `POST /internal/deadletters/{id}/replay` (API-038) is not automatically the general outbox-replay endpoint.

#### OPS-ERR-002 — Suspected ACL Leak

1. Suspend affected index aliases.
2. Revoke cached evidence.
3. Preserve audit traces.
4. Execute scoped replay of ACL revisions.
5. Reenable affected search only after negative access tests pass.

**Confirmed evidence:** Source, p. 79, §22.2.2.  
**Needs confirmation:** Exact scope selection, replay contract, evidence-preservation mechanics, recipients and reenable authority.

#### OPS-ERR-003 — Model Provider Outage

1. Disable admission of new generation.
2. Keep authorized manual case/evidence workflows available.
3. Display degraded service state.
4. Prevent unapproved region/deployment fallback.
5. Page on-call only when availability budget is impacted.

**Confirmed evidence:** Source, pp. 37, 69, 79.  
**Needs confirmation:** Recovery probes and thresholds for reopening admission, outage message/status and approved fallback catalog.

#### OPS-ERR-004 — Dead-Letter Replay

1. Authenticate the authorized operator and establish immutable tenant/correlation scope.
2. Require operator reason, dry-run validation and scope limit.
3. Validate event schema and current authorization/revision constraints.
4. Replay with original event identity unless an explicitly provenance-linked migration transforms schema.
5. Verify no second accepted business transition or side effect.

**Confirmed evidence:** Source, pp. 48–50.  
**Needs confirmation:** Dry-run proof binding, replay scope units, grants, limit, acknowledgement and terminal outcome.

#### OPS-ERR-005 — Regional Recovery and Release Regression

1. Under incident command, restore warm-region snapshots for regional failure.
2. Verify relational/object consistency and index rebuild recipes together.
3. Measure reference RPO `<=15 minutes` and RTO `<=4 hours`.
4. For canary regression, reverse traffic/binary as defined by the release rollback plan.
5. Invoke data compensation only when explicitly supported; do not automatically down-migrate the database.
6. Preserve reconstructible image/schema/prompt/model-routing-policy evidence.

**Confirmed evidence:** Source, pp. 19–20, 69–70, 72–73.  
**Needs confirmation:** Restore order, hold/deletion effects on backups, acceptance measurement and migration-specific compensation.

## Failure Acceptance Criteria

### Verification Principles

**ERR-R-008 — Confirmed:** Use synthetic successful, empty, mixed-permission, adversarial and malformed fixtures. Record randomized seeds. Critical isolation and approval tests pass with **zero exceptions**. Signed test outputs are referenced by release digest.  
**Evidence:** Source, pp. 74–76, 88–89.

Unknown HTTP/code/state values remain test-contract blockers. Tests must not assert invented literals or silently pass unresolved choices.

| Acceptance ID | Trigger/action | Expected response, screen/data state and retry result | Traceability |
|---|---|---|---|
| AC-ERR-001 | Submit schema-invalid request, including bypass of client validation | `422`; safe details; no invalid accepted mutation or tool dispatch; no automatic retry of unchanged validation failure | ERR-001; Source, pp. 54–56 |
| AC-ERR-002 | Use token with unexpected algorithm/missing tenant; substitute valid foreign-tenant case ID | Authentication rejected; foreign case same not-found class as absent ID, `404`-equivalent; no private content/existence; no mutation | ERR-002–003; `T-01`, `TST-003`; Source, pp. 21–23, 89 |
| AC-ERR-003 | Reuse pooled DB connection across tenants or assign foreign-tenant workspace | Scoped variables reset; no prior-tenant access; workspace-tenancy violation rejected | ERR-003; DAT-R-005; Source, p. 86 |
| AC-ERR-004 | PATCH case with stale `If-Match` | `409 CASE_VERSION_CONFLICT`, safe current revision and `retryable: false`; case unchanged, no accepted event; refetch/reconciliation UX remains Proposal | ERR-004; Source, pp. 25, 84 |
| AC-ERR-005 | Create twice with same key/body; then change body under same key | One `NEW` case and identical response; changed body `409 IDEMPOTENCY_CONFLICT`; no second mutation | ERR-005–006; `TST-001–002`; Source, p. 89 |
| AC-ERR-006 | Replay outbox event 100 times and delay an old revision | Exactly one accepted transition and accepted-transition audit evidence; duplicates recorded, stale delivery does not overwrite current state | ERR-006; `T-07`, `TST-007`; Source, pp. 48–50, 88–89 |
| AC-ERR-007 | Exceed configured file cap, mismatch MIME/extension, submit unsafe/polyglot/zipped payload | Invalid admission fails closed; unsafe content `QUARANTINED`, no indexing; scan precedes parsing; no macros or remote-reference fetch. Exact upload errors await approved mapping | ERR-007–008; `T-04`, `TST-015`; Source, pp. 30, 88–89 |
| AC-ERR-008 | Sync mixed batch with poison record and an undurable preceding item | Bounded retries then safe quarantine exception; remaining batch may continue; cursor never skips undurable preceding outcomes; replay does not duplicate durable ingestion | ERR-009; Source, pp. 28–29 |
| AC-ERR-009 | Low-quality document, unsupported capability, revoked credentials | Low-quality source remains permitted-viewable but excluded from autonomous use; lower-trust warning visible; revoked queued work `CONNECTOR_REAUTH_REQUIRED` without secrets | ERR-010–012; Source, pp. 27, 32 |
| AC-ERR-010 | Simulate provider 429 storm and admission rejection | Capped retries/control admitted load; honor provider delay; throttled AI client `429` plus `Retry-After`; saved case accessible | ERR-013; `TST-008`; Source, pp. 28, 69, 89 |
| AC-ERR-011 | Exhaust current run quota | Terminal current run; no automatic model/data-class switching; no new published pointer; failure checkpoint observable | ERR-014; Source, pp. 38, 41 |
| AC-ERR-012 | Retrieve insufficient evidence or generate missing citations | `NO_SUPPORTED_EVIDENCE` for insufficient retrieval; missing-citation output needs review or unsupported, never approved fabricated context | ERR-015; `TST-009`; Source, pp. 36, 89 |
| AC-ERR-013 | Return invalid anchor/citation, unknown JSON fields or control-character injection | Invalid citation not verified; `MODEL_OUTPUT_INVALID` where model validation fails; bounded parsing recovery; no publish | ERR-016–017; `TST-005`; Source, pp. 31, 35, 38, 89 |
| AC-ERR-014 | Hostile PDF instructions/arbitrary MCP/equivalent denied tool/unapproved fallback | Evidence has no instruction authority; directives stripped/indicators recorded; `DENY` before unauthorized dispatch; no prohibited fallback or secret scope expansion | ERR-018; `T-02`, `T-06`, `TST-014`; Source, pp. 37–42, 87–89 |
| AC-ERR-015 | Plan exceeds depth eight/tool calls sixteen; stop condition/deadline occurs | No over-budget execution; exact failed checkpoint shown; no partial-as-approved result. Timeout/wait-state fixtures require OQ-ERR-002 resolution | ERR-019; `T-10`; Source, pp. 12, 40–42 |
| AC-ERR-016 | Approve old/wrong hash, self-approve high-risk draft or leave required fields incomplete | Stale decision rejected/audited, `409` supported; self-approval denied; Approve/Reject disabled while incomplete; no changed-artifact publication under old approval | ERR-020–021; `T-03`, `TST-006`; Source, pp. 11, 45–46, 58, 89 |
| AC-ERR-017 | Expire task under configured SLA | No implicit approval; expiry/reassignment/escalation recorded; no publication inferred | ERR-022; `TST-010`; Source, pp. 45, 89 |
| AC-ERR-018 | Revoke source after indexing/cache/review and query/publish | No forbidden evidence on next query; stale evidence rejected at publication; suspect leak containment reenabled only after negative tests | ERR-023; `T-08`, `TST-004`; Source, pp. 28, 46, 79, 89 |
| AC-ERR-019 | Fail required transaction/outbox commit; fail index after source acceptance | No partial required ACID mutation; index failure preserves source; fingerprint/outbox reconciliation repairs without second accepted outcome | ERR-024–025; Source, pp. 17, 49, 52, 74 |
| AC-ERR-020 | Lose successful creation response and retry identical intent | Original key/identity resolves one operation, not duplicate effects; no ambiguous/fabricated completion. In-flight response behavior awaits IDL | ERR-024; Source, pp. 17, 54, 74 |
| AC-ERR-021 | Generation outage/vector degradation | Authorized manual editing/evidence search remain available; generation admission disabled during outage; lexical fallback visibly reduced quality if used; gates remain enforced | ERR-026; Source, pp. 69, 79 |
| AC-ERR-022 | Disconnect SSE, reconnect with offset and refresh | Scoped retained backfill/increasing offsets and persisted progress; no restarted run/side effects; invalid-offset behavior awaits contract | ERR-027; Source, pp. 55, 58 |
| AC-ERR-023 | Lose worker heartbeat; exercise primary-region recovery | Safety/dedup/checkpoint invariants preserved; object/relational consistency verified; RPO `<=15 minutes`, RTO `<=4 hours` for reference profile | ERR-028; `TST-012`; Source, pp. 19, 69–70, 89 |
| AC-ERR-024 | Retry incomplete provisioning/backfill; empty queue without sufficient coverage | Idempotent workflow; incomplete state visible and sync blocked; readiness not falsely inferred from queue emptiness; stable source IDs/receipts retained | ERR-029; Source, p. 78 |
| AC-ERR-025 | Export/delete as single Admin; purge held inventory | Single Admin insufficient; held records retained/receipted; eligible removals tombstoned/verified; no false held-object deletion completion | ERR-030; `T-11`, `TST-013`; Source, pp. 78–80, 88–89 |
| AC-ERR-026 | Fail webhook delivery | Signed exponential retries; committed case transition unchanged; no business rollback | ERR-031; Source, p. 55 |
| AC-ERR-027 | Attempt historical edit; inspect errors/traces/provider requests/export | Edit denied; immutable audit retained; no raw credentials, user documents in diagnostics, unrestricted prompts or unauthorized existence in error details | ERR-032; `T-05`, `T-09`; Source, pp. 62–64, 79, 84, 88 |
| AC-ERR-028 | Poison expected fixtures, regress safety, produce low confidence or incompatible schema/build | Version/manifest detects fixture change; promotion blocked; critical failures cannot be excused by scores; canary rollback does not automatically down-migrate DB | ERR-033; `T-12`, `TST-016`; Source, pp. 55, 72–76, 88–89 |
| AC-ERR-029 | Replay dead letter without reason/dry run/scope, then valid controls | Missing controls do not authorize replay; valid bounded replay preserves original identity except explicit migration provenance and produces no duplicate mutation | ERR-006, ERR-024; OPS-ERR-004; Source, p. 50 |
| AC-ERR-030 | Keyboard-only failure/review interaction; live updates | No blocked permitted action, visible focus, semantic keyboard order; meaningful transitions only announced; failure conveyed in accessible text | ERR-R-001; `TST-011`; Source, pp. 57–58, 89 |

Empty/no-op job outcomes, zero-page documents, all-held inventories and absent/corrupt evaluation corpus must be tested, but their exact states/codes **Need confirmation**. Empty input does not authorize fabricated readiness, scores or completion receipts.

## Consistency and Open Questions

### Conflicts and Required Amendments

Earlier specifications are not rewritten. Existing Proposed UI placements, case payloads, SSE projections and recovery interactions remain **Proposals**.

| ID | Affected exception and earlier IDs | Source conflict / gap | Required resolution or amendment |
|---|---|---|---|
| OQ-ERR-001 | ERR-004–005, ERR-R-003; OQ-SF-007, OQ-API-003, OQ-BR-009 | Source p. 54 specifies snake-case convention; pp. 84, 89 supply uppercase literals | Preserve `CASE_VERSION_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `MODEL_OUTPUT_INVALID`, `NO_SUPPORTED_EVIDENCE`, `CONNECTOR_REAUTH_REQUIRED`; finalize naming/compatibility without silently normalizing |
| OQ-ERR-002 | ERR-019, ERR-022; OQ-SF-006, OQ-API-005, OQ-DAT-009, OQ-BAT-002, OQ-BR-004 | Missing approval terminates p. 41; valid waiting p. 49; recoverable timeout p. 12; 180-second example p. 90; enum p. 82 | Define missing approval versus waiting, timeout clock/human-wait coverage, terminal/recoverable representation and recovery contract; do not invent timeout enum |
| OQ-ERR-003 | ERR-001, ERR-009, ERR-017; OQ-BAT-011, OQ-BR-016 | Permanent validation not retried p. 49, but malformed records and model parsing have bounded retries pp. 29, 38 | Define adapter/record/output-validation recovery classification separately from invalid request/permission denial; supply caps |
| OQ-ERR-004 | ERR-024–025; API-R-005, DAT-R-007, OQ-DAT-017 | Source p. 52 ACID wording versus independently owned service boundaries | Finalize local transaction/aggregate ownership, outbox atomics and saga reconciliation; no inferred distributed provider/index transaction |
| OQ-ERR-005 | ERR-030; DAT-R-016, OQ-BAT-004, OQ-BR-005 | Routine closed-case retention p. 26 versus two independent delete/export checks p. 78 | Define routine-retention approval applicability and authority propagation; do not silently exempt or universally add checks |
| OQ-ERR-006 | ERR-024, ERR-027; OQ-API-008, OQ-BAT-005–006, OQ-BR-011 | Repeated job/event wording beside GETs; dead-letter replay p. 50 versus outbox replay p. 90 | Define actual read errors/events and outbox replay interface; do not expose fabricated job success or mutation event for ordinary GET |
| OQ-ERR-007 | ERR-013, ERR-019, ERR-024; API-008–009, OQ-API-001 | Two run creation routes, Source pp. 15–17 versus pp. 40, 83 | Resolve canonical route/alias and common idempotency namespace before retry implementation |
| OQ-ERR-008 | ERR-004; API-050, OQ-SF-002, OQ-API-002, OQ-BR-001 | Workspace settings associated with case PATCH, Source p. 24 | Supply legitimate configuration endpoint and conflict contract; do not mutate case to recover workspace-settings conflict |
| OQ-ERR-009 | ERR-021; OQ-BR-006 | High-risk self-approval restriction p. 11 versus general no-self-approval task constraint p. 85 | Preserve both; define originating actor and full separation applicability |
| OQ-ERR-010 | ERR-R-007; OQ-SF-008, OQ-API-006, OQ-BR-008 | Case-create within/under 300 ms, Source pp. 12, 65 | Resolve strict boundary/instrumentation; do not infer request timeout or alert threshold from latency objective |
| OQ-ERR-011 | ERR-032–033; OQ-BR-012 | `SEC-001`–`SEC-012` release-blocking namespace exists without individual definitions, Source p. 88 | Confirm requirement/test mapping; no fabricated definitions or exemptions |

### Unresolved Handling Decisions

| ID | Affected requirements | Needs confirmation | Evidence / earlier dependency |
|---|---|---|---|
| OQ-ERR-012 | All ERR-* / ERR-R-003 | Complete HTTP/business-code/retryable/details mapping; authentication, permission, upload, stale review, dependency, timeout, object access, provisioning, purge and operational failures | Source pp. 54, 83–84 provide partial contracts; OQ-API-026 |
| OQ-ERR-013 | ERR-001–005, ERR-020–021, ERR-027 | Error copy, safe field-level mapping, focus/announcement behavior, unsaved-input preservation, conflict reconciliation, session/stream/cursor recovery UX | Source pp. 57–58; OQ-SF-024, OQ-API-019 |
| OQ-ERR-014 | ERR-005–006, ERR-024–025, ERR-R-006 | Fingerprint/key rules, in-flight races, retry counter persistence, dedup retention/expiry, worker fencing/lease and per-operation safe replay | Source pp. 25, 48–54; OQ-API-014, OQ-DAT-018, OQ-BAT-008/011 |
| OQ-ERR-015 | ERR-009, ERR-013, ERR-017, ERR-024, ERR-031 | Timeout/retry/circuit values; end-to-end budget coordination; malformed record/model/webhook exhaustion and terminal states | Source pp. 28–29, 38, 49, 55; OQ-BAT-011/017 |
| OQ-ERR-016 | ERR-007–011, ERR-015–016, ERR-023 | Upload cap byte/equality, decompression and quality thresholds, retrieval confidence, anchor failure and lower-trust allowed uses; race-safe ACL propagation | Source pp. 27–36; OQ-BR-016, OQ-BAT-012 |
| OQ-ERR-017 | ERR-014, ERR-019–023 | Quota reservation reconciliation, call/depth counting, policy version changes, hash canonicalization, review required fields, repeated decisions/expiry races/publication trigger | Source pp. 38–46, 58; OQ-BR-017–018 |
| OQ-ERR-018 | ERR-025, ERR-028–030 | Partial provisioning/export/purge compensation, all-held completion, shared objects/backups/holds, index commit/ready mapping, restore consistency and takeover | Source pp. 49–52, 69–70, 78–80; OQ-DAT-020/023, OQ-BAT-015–016 |
| OQ-ERR-019 | ERR-027, ERR-031 | Cursor/SSE retention and expired offsets; source signed-URL expiration/renewal; webhook signature/age/status/terminal delivery | Source pp. 52, 55; OQ-API-019, OQ-BR-023 |
| OQ-ERR-020 | ERR-032, ERR-R-007 | Log levels, safe schema/stack traces, exception sampling, metric labels, archive verification/repair, vault/audit outage and disclosure incident procedure | Source pp. 62–66; OQ-DAT-021–022 |
| OQ-ERR-021 | Monitoring table, OPS-ERR-* | Notification recipients/channels, owners, thresholds, incident dedup/escalation, pause/replay/reenable authority and controls | Source pp. 65, 79, 90; OQ-BAT-017 |
| OQ-ERR-022 | ERR-029–030, ERR-033 / acceptance | Empty/no-op/partial status schemas, absent/corrupt corpus, completeness/confidence methods, canary thresholds and migration-specific repair | Source pp. 75–80, 89; OQ-BAT-010/013/016 |
| OQ-ERR-023 | All integration recovery | Approved region/search/identity/model deployments/corporate retention/provider permissions and per-tenant key isolation/rotation | Source pp. 10, 90, §F.2; OQ-BR-024 |

### Dependencies and Required Carry-Forward

- [01_screen_functions.md](01_screen_functions.md): Preserve `SF-013`, `SF-015`, document/run/review/connector failures and accessible status requirements. Do not add unconfirmed retry buttons or operational screens.
- [02_api.md](02_api.md): This specification addresses API-R-013–018 and OQ-API-026 without resolving unsupported wire values. Controlled IDL must incorporate approved error decisions.
- [03_data.md](03_data.md): Preserve tenant reset, immutable history, exact approval binding, atomic publication, source acceptance during indexing failure, hold receipts and distinct diagnostic/audit retention.
- [04_batch_functions.md](04_batch_functions.md): Preserve logical jobs, bounded replay, durable cursor/checkpoint requirements and unresolved schedules/commit/partial-state choices.
- [05_business_rules.md](05_business_rules.md): Exception recovery must enforce BR-001–005, BR-013–024 and BR-025–033. No retry or degradation grants missing authority.
- Remaining operational/architecture specification details are **To be defined in a later stage**; this document does not imply they already exist.
- Stage 8 must consolidate open decisions from completed Markdown only into `08_architecture_decision.md`, linking `06_exception_handling.md` and affected `ERR-*`, `ERR-R-*`, `OPS-ERR-*`, `AC-ERR-*`, `OQ-ERR-*` and earlier identifiers.

No owner identity, deadline or approval is supplied for these unresolved decisions. Unsupported codes, limits, states, schedules and recovery mechanisms require explicit resolution; they are not permission for the implementation AI to choose defaults.
