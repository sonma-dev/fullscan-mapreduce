# 6. Exception Handling Specification

## Exception Inventory and Classification

### Specification Basis

| Item | Definition |
|---|---|
| Output file | `06_exception_handling.md` |
| Application | OrionDesk AI |
| Source document | `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Baseline | `OD-AI-DDS-001`; release `R1.0`; design revision `1.3` |
| Source authority | Fictional reference architecture, normative for this sample application. Numeric targets are design assumptions, not measured production results. |
| Citation convention | **S** denotes `1794806332-OrionDesk_AI_Detailed_Design_Specification.pdf`. Every source citation identifies an original PDF page and section. |
| Completed specifications | [01_screen_functions.md](01_screen_functions.md), [02_api.md](02_api.md), [03_data.md](03_data.md), [04_batch_functions.md](04_batch_functions.md), and [05_business_rules.md](05_business_rules.md) |
| Exception identifiers | `ERR-001`–`ERR-060` are specification identifiers, not public business error codes, event names, database identifiers, or batch exit codes. Existing source codes, `T-`, and `TST-` identifiers take precedence for wire and verification terminology. |
| Confirmed | Explicitly supported by S. Confirmation of handling behavior does not establish an unspecified HTTP status, error code, schema, retry count, threshold, notification recipient, or schedule. |
| Needs confirmation | A missing or conflicting contract. It is not permission for an implementation AI to choose behavior. |
| Proposal | An explicitly labeled suggestion. Earlier UI arrangements, API bodies, SSE examples, and caller-reconciliation suggestions remain Proposals. |
| Later specifications | Remaining specification details are **To be defined in a later stage**. The identity and contents of Stage 7 are not supplied here. Stage 8 will consolidate unresolved items in `08_architecture_decision.md`; that document has not been generated. |

### Scope and Classification Principles

**ERR-SCP-001 — Confirmed:** Exception handling covers public requests, internal service interfaces, tool dispatch, durable workflows, source ingestion, retrieval, model generation, review/publication, persistence, background jobs, lifecycle operations, and operational recovery. Abuse paths fail closed and expose stable, non-sensitive outcomes. Partial processing must never appear as an approved answer.  
**Source:** S, p. 13, §2.3.2; pp. 48–50, Chapter 13; pp. 78–80, Chapter 22.

**ERR-SCP-002 — Confirmed:** An exception is scoped to the affected request, resource, step, batch item, workflow, index generation, or incident. Source-confirmed continuation of unaffected work must be preserved. The source does not establish universal whole-job rollback or whole-system shutdown.  
**Source:** S, pp. 28–29, §§7.2–7.3; p. 49, §13.2.2; p. 90, Appendix F.1.

**ERR-SCP-003 — Confirmed:** Classification must distinguish:

- Permanent request validation and permission failures.
- Transient dependency failures eligible for bounded retry.
- Source-specific bounded parsing retries followed by quarantine.
- Bounded model-output validation retries.
- Controlled duplicate execution, which is not a new business failure.
- Expected restricted outcomes such as insufficient evidence, required review, expiry, or legal hold.
- Actual internal or security failures, including stale ACL visibility and partial transaction integrity violations.

**Source:** S, pp. 29, 36, 38, 45, 49, 80, 89.

**ERR-SCP-004 — Needs confirmation:** Exact exception-selection order when multiple conditions fail, internal exception classes, batch exit codes, gRPC status mapping, and endpoint-specific error taxonomy. No first-match priority or generic internal error code is selected. See **ERR-OQ-001**.

### Category Definitions

These are analytical categories, not new stored enums.

| Category | Meaning |
|---|---|
| Invalid input | An approved request, argument, file, envelope, or output contract is violated. |
| Business-rule violation | A state, evidence, budget, policy, lifecycle, or integrity prerequisite is unsatisfied. |
| Permission violation | Identity, tenant, resource access, tool grant, reviewer eligibility, or separation-of-duties conditions fail. |
| External failure | A connector, model provider, search dependency, object service, notification recipient, or regional dependency fails. |
| Internal failure | A transaction, worker, checkpoint, derivative, archive, accounting, migration, or release-processing boundary fails. |
| Controlled replay | Identical requests or duplicate events are recognized without reapplying accepted business effects. |
| Restricted or degraded outcome | Work is limited, awaiting intervention, expired, quarantined, unsupported, legally protected, or reduced quality without being treated as approved completion. |

### Identity, Input, Concurrency, and Shared Infrastructure Exceptions

“Applicable jobs” means existing `BAT-` functions affected by the operation, not a newly created job.

| Exception ID | Occurrence location and detection condition | Category and affected scope | Preceding specification mappings | Evidence/status |
|---|---|---|---|---|
| ERR-001 | Gateway/session or internal service authentication fails required issuer, audience, expiry, subject, tenant, algorithm, or service-identity checks | Permission; request or service invocation | All protected `SCR`; API authentication profiles, API-027; DAT-019–020; BAT-CTX-001–003; BR-001 | Confirmed controls; S, pp. 18, 21–22, §§4.1.2, 5.1. Exact response Needs confirmation. |
| ERR-002 | Resource/action authorization, reviewer eligibility, or separation of duties fails | Permission; requested resource/action | SF-AUTH-001; protected APIs; DAT-019–022, DAT-011–012; applicable BAT; BR-002, BR-027 | S, pp. 11, 22, 45, 85, §§2.1.2, 5.2, 12.2 and B.1 |
| ERR-003 | Resource is absent, belongs to another tenant, or is soft-deleted | Permission/unavailable resource; inquiry or mutation target | SCR-001–008; API-AUTH-002, API-002, API-021, API-035; DAT-RI-007/009; applicable BAT; BR-003, BR-038 | S, p. 23, §5.3.2; p. 51, §14.1.2; p. 89, `TST-003` |
| ERR-004 | Tenant context is missing/incorrect, pooled scope is retained, or case workspace belongs to another tenant | Permission/internal integrity; transaction and tenant-owned data | API-AUTH-003; DAT-RI-001–003; BAT-CTX-001; BR-003 | S, p. 22, §5.3.1; p. 86, B.2 |
| ERR-005 | Approved request or argument schema is invalid | Invalid input; request before allocation, domain validation, or dispatch | SF-GEN-005; API-VAL-001; DAT-VAL; BAT-CTX-005; BR-006 | S, p. 54, §15.1.1; p. 56, §15.3.2 |
| ERR-006 | Required `Idempotency-Key`, revision precondition, or trusted mutation context is missing or malformed | Invalid input/business prerequisite; mutation | API-IDEM/CNC; DAT-COM-F02–06, DAT-044; BAT argument contracts; BR-006–008 | Requirement existence Confirmed; missing-header status/code Needs confirmation. S, pp. 25, 48, 54. |
| ERR-007 | Case revision no longer matches submitted `If-Match` | Business conflict; case mutation | SCR-002-A02/A04/A07; API-003/017; DAT-CNC-001; case-mutating BAT; BR-007 | S, p. 25, §6.2.2; pp. 83–84, A.2–A.3 |
| ERR-008 | Workspace configuration revision is stale | Business conflict; settings update | SCR-007-A02; API-050; DAT-002-F10, DAT-CNC-002; BR-007 | S, p. 24, §6.1.1. Settings-specific response Needs confirmation. |
| ERR-009 | Unsupported case transition, closure guard, or ordinary in-place exit from `CLOSED` is requested | Business-rule violation; case | SCR-002-T01–T08, SCR-002-A04/A07/A08; API-003/017/052; DAT-STATE-001; BR-013/014 | S, pp. 24–26, Chapter 6; p. 82, A.1 |
| ERR-010 | Late classifier result/correction conflicts with current revision, correction prerequisites, or other supported case business invariants | Business conflict/invalid input; case classification or business fields | SCR-002-F05–15/A03; API-051 and case APIs; DAT-024, DAT-003-F11–17; BAT-001; BR-010–012 | S, pp. 12, 25, §§2.2.1, 6.2–6.3. Detailed precedence/formulas Needs confirmation. |
| ERR-011 | An identical HTTP mutation is repeated under the applicable idempotency binding | Controlled replay; original operation | SF-GEN-008; API-IDEM-002/003; DAT-044; job-creating BAT; BR-008 | S, pp. 25, 54, 83, 89, `TST-001` |
| ERR-012 | Same idempotency key is reused with a different request fingerprint | Business conflict; mutation/job request | SF-GEN-008; API-IDEM-002/003; DAT-044; job-creating BAT; BR-008 | S, p. 54, §15.1.2; p. 89, `TST-002` |
| ERR-013 | Duplicate event ID/operation key arrives after accepted processing | Controlled replay; consumer effect | API-EVT-002; DAT-014/045; BAT-008/022 and consumers; BR-008/009/037 | S, pp. 17, 48–50; p. 88, `T-07`; p. 89, `TST-007` |
| ERR-014 | Delayed/stale event revision or invalid required envelope/job context is detected | Business conflict/invalid input/permission; consumer | API-EVT-001/002; DAT-014/048; BAT-008/022; BR-003/008/037 | S, pp. 22, 48–50. Detailed stale/future/schema disposition Needs confirmation. |
| ERR-015 | Integration is unavailable, request delivery fails, or response is lost before the caller can determine the durable outcome | External/internal; request or accepted operation | All APIs as applicable; DAT-044–048; applicable BAT; BR-006/008/036 | Unambiguous dependency handling Confirmed; lost-response lookup protocol Needs confirmation. S, p. 12, interface boundary; p. 49, §13.3.1. |
| ERR-016 | Transaction, required persistence, or checkpoint/dispatch boundary fails or crashes | Internal; confirmed transaction or workflow unit | API-TXN-001–003; DAT-TXN-001–004; BAT-TXN-001, BAT-008/010/011; BR-009/031 | S, pp. 45, 49, 52, §§12.3.1, 13.2, 14.2.1 |

### Connector, Ingestion, Retrieval, and Source Exceptions

| Exception ID | Occurrence location and detection condition | Category and affected scope | Preceding specification mappings | Evidence/status |
|---|---|---|---|---|
| ERR-017 | Connector batch fails after some items have durable outcomes | External/internal partial failure; items and cursor | SCR-006; API-009/025; DAT-015/028; BAT-002/019; BR-035 | S, p. 28, §7.2.1 |
| ERR-018 | Connector advertises unsupported list/fetch/delta cursor/ACL/delete capability | Restricted outcome; connector ingestion trust | SCR-006-F02/F03; API-009/025; DAT-027; BAT-002; BR-034 | S, p. 27, §7.1.1 |
| ERR-019 | Connector credentials are revoked before queued execution | Permission/external credential failure; queued sync job | SCR-006-F04/A02/A03; API-009/025/054/055; DAT-027; BAT-002; BR-034 | S, p. 27, §7.1.2 |
| ERR-020 | File type, MIME signature/extension agreement, configured size cap, or decompression safety fails | Invalid input; file ingestion | SCR-002-F20/A05; API-004; DAT-023/029; BAT-003; BR-015 | S, p. 30, §8.1.1; p. 90, Appendix F |
| ERR-021 | Malware/unsafe active content or malicious parser input is detected | Security/invalid input; attachment | SCR-002-F22/F25; API-004/018; DAT-029; BAT-003/004; BR-016 | S, p. 30, §8.1.2; pp. 88–89, `T-04`, `TST-015` |
| ERR-022 | Malformed source document exhausts bounded processing retries | Restricted outcome/internal parsing failure; source item | SCR-006-F08, SCR-002-F25; API-009/025/018; DAT-028/029; BAT-002/003; BR-035/036 | S, p. 29, §7.3.2 |
| ERR-023 | Extraction quality is insufficient according to the applicable quality gate | Restricted outcome; safe document and autonomous recommendation | SCR-002-F23, SCR-003-F09/F10; API-018/010; DAT-029; BAT-003/010; BR-018 | S, p. 32, §8.3.2 |
| ERR-024 | Index write fails, indexed version/fingerprint is missing/mismatched, or indexing is delayed | External/internal derivative failure; source/index scope | SCR-006/SCR-003; API-033; DAT-006/014/031/032; BAT-004/009/022; BR-020/037 | S, p. 49, §13.2.2; p. 90, F.1 |
| ERR-025 | Parallel index fails completeness/recall validation or activation prerequisites | Business/internal validation; rebuild generation | DAT-031/032; BAT-005; retrieval APIs indirectly; BR-020 | S, p. 34, §9.1.2 |
| ERR-026 | Citation anchor cannot resolve, source object is unavailable, or signed delivery access has expired | Business/external source-delivery failure; evidence item | SCR-003-A03, SCR-005-F07; API-021/022/035/057; DAT-006/007/035; BR-017/019/043 | Anchoring and controlled delivery Confirmed; expired-URL recovery Needs confirmation. S, pp. 31, 35, 52, 57. |
| ERR-027 | Confidence, evidence quality, or supported evidence is insufficient | Restricted outcome; retrieval and grounded run | SCR-003-F11/A06; API-010/021/046; DAT-010; BAT-010; BR-019 | S, p. 36, §9.3.2 |

### Model, Tool, Workflow, Review, and Publication Exceptions

| Exception ID | Occurrence location and detection condition | Category and affected scope | Preceding specification mappings | Evidence/status |
|---|---|---|---|---|
| ERR-028 | Retrieved/model content attempts instruction, tool, tenant, approval, or destination injection | Security/untrusted input; prompt and planner | SF-GEN-011; API-008; DAT-037/038/041; BAT-010; BR-005/022 | S, p. 7; pp. 38–39, 61; p. 88, `T-02` |
| ERR-029 | Tool arguments/grant are invalid, arbitrary capability is invoked, or denied action is replaced by an equivalent tool | Permission/invalid input; tool dispatch | API-046/047; DAT-041/042; BAT-010; BR-005 | S, pp. 41–42, 87; p. 89, `TST-014` |
| ERR-030 | Model response violates versioned schema through unknown fields, invalid citations, or control-character injection | Invalid external output; generation attempt | SCR-004-A04; API-008; DAT-038; BAT-010; BR-022 | S, p. 38, §10.2.2; p. 89, `TST-005` |
| ERR-031 | Plan is cyclic, exceeds depth/call limits, repeatedly invalid, or exhausts call budget | Business/invalid plan; run and dispatch | SCR-004-F04/F06; API-005/019; DAT-008/040; BAT-010; BR-023 | S, pp. 40–42; p. 88, `T-10`; p. 90 |
| ERR-032 | Run deadline/configured runtime expires | Business/runtime failure; current run | SCR-004-F02/F06/A04; API-005/006/019; DAT-008/046; BAT-010; BR-023 | S, pp. 12, 41, 49, 82, 90. State/wait semantics Needs confirmation. |
| ERR-033 | A2A recipient declines, handoff schema/grant fails, or task deadline expires | Restricted/permission/external handoff; task | API-047; DAT-042; BAT-010; BR-005/023 | Decline/deadline/schema concepts Confirmed; response/retry contract Needs confirmation. S, pp. 41, 87. |
| ERR-034 | Current run exhausts workspace/token budget | Business budget failure; current run | API-008; DAT-008-F05/016; BAT-010; BR-024 | S, p. 38, §10.3.1 |
| ERR-035 | New-run admission thresholds fail or provider produces throttling/`429` bursts | Business quota/external throttle; admission and dependency attempts | SCR-002-A06, SCR-006-F07; API-005/008/009; DAT-055/015/016; BAT-002/010; BR-024/036 | S, pp. 28, 69; p. 89, `TST-008` |
| ERR-036 | Generation provider is unavailable or proposed fallback violates deployment/region/data-handling requirements | External/permission; generation route | SCR-002-A11, SCR-004; API-008/026/041; DAT-036; BAT-010; BR-021/044 | S, p. 37, §10.1.2; pp. 69, 79; p. 88, `T-06` |
| ERR-037 | Recovery/fallback/publication attempts use lower information-class controls than required by included material | Security/business invariant; four run controls | API-CLS-001; DAT-CLS-001; BAT-CLS-001; BR-026; SCR-002-F10 | S, p. 62, §17.2.1; p. 90 |
| ERR-038 | Policy yields `DENY`, `REQUEST_MORE_EVIDENCE`, or required approval is missing | Restricted/business gate; action/run/publication | SCR-002/SCR-004/SCR-005; API-020/024; DAT-017/011; BAT-010/011; BR-025/031 | S, pp. 11–13, 41, 44–46 |
| ERR-039 | Required review fields are incomplete | Invalid input/UI prerequisite; review form | SCR-005-F10/F11/A03/A04; API-024; DAT-012; BR-028 | S, p. 58, §16.2.2; p. 56, §15.3.2 |
| ERR-040 | Reviewer decision references changed/wrong artifact hash | Business conflict/security replay; decision and publication | SCR-005-A03/A04; API-024/020; DAT-011/012/039; BAT-011; BR-028/031 | S, p. 45, §12.2.2; pp. 83, 89, `TST-006` |
| ERR-041 | Review task expires under configured SLA | Restricted/business expiry; task/routing | SCR-005-A05; API-023/024; DAT-011; BAT-012; BR-029 | S, p. 45, §12.2.1; p. 89, `TST-010` |
| ERR-042 | Override lacks elevated role, secondary reviewer, or audited reason | Permission/business prerequisite; override | SCR-005-A06; API-053; DAT-043-F03; BR-030 | S, p. 46, §12.3.2 |
| ERR-043 | Publication lacks current authorization, supported anchors/evidence, satisfied policy/approvals, or atomic commit | Business/permission/internal; exact candidate and final pointer | SCR-002-A09; API-020; DAT-043/003-F15; BAT-011; BR-031 | S, pp. 12, 45–46; p. 87, C.1 |

### Operational, Lifecycle, and Verification Exceptions

| Exception ID | Occurrence location and detection condition | Category and affected scope | Preceding specification mappings | Evidence/status |
|---|---|---|---|---|
| ERR-044 | Forbidden evidence remains visible after ACL revocation or an ACL leak is suspected | Security incident; affected aliases/cache/source scope | SCR-003-A04; API-REC-001; DAT-022/034; BAT-006/022; BR-004/037 | S, p. 28, §7.2.2; p. 79, §22.2.2 |
| ERR-045 | SSE disconnects, cursor/offset is invalid/expired, or retained backfill is unavailable | External/transport/input; read session | SCR-004-A02/A03, SCR-001/SCR-008 pagination; API-007/011/016; DAT-049; BR-032 | Scoped reconnect Confirmed; invalid/expired handling Needs confirmation. S, pp. 54–55, 58. |
| ERR-046 | Worker heartbeat is lost or worker stops during accepted processing | Internal partial failure; claimed work/checkpoint | Applicable BAT; DAT-045/046/055; BR-008/023/044 | Fault coverage Confirmed; takeover timing/mechanism Needs confirmation. S, p. 70, §19.3.2. |
| ERR-047 | Provisioning is incomplete or backfill lacks reconciled coverage despite queue emptiness | Restricted/internal partial failure; onboarding | SCR-006-F09; API-056/009; DAT-058; BAT-018/019; BR-033 | S, p. 78, §§22.1.1–22.1.2 |
| ERR-048 | Export/delete lacks two independent checks; single Admin attempts export | Permission/business prerequisite; lifecycle request | SF-SCP-007; API-014/015; DAT-059; BAT-020/021; BR-039 | S, pp. 78, 83, 88, `T-11` |
| ERR-049 | Export is partial, inventory/package integrity is unverified, or prohibited contents are included | Internal/security lifecycle failure; package | API-014; DAT-059; BAT-020; BR-040 | Required contents/checksums/exclusions Confirmed; partial-package recovery Needs confirmation. S, p. 79, §22.3.1. |
| ERR-050 | Retention candidate is ineligible or legal hold protects purge inventory | Restricted/business protection; eligible objects/cases | API-036/029; DAT-018/026/053; BAT-013/014/021; BR-038/041 | S, pp. 26, 66, 80; p. 89, `TST-013` |
| ERR-051 | Deletion removes only part of eligible inventory or completion/receipt verification fails | Internal/external partial failure; lifecycle inventory | API-015/036; DAT-018/035/053/059; BAT-021; BR-041 | Verified outcomes/receipts Confirmed; final partial state Needs confirmation. S, pp. 80, 87, 89. |
| ERR-052 | Historical audit/decision edit is attempted or audit archive/chain processing fails | Permission/internal integrity; immutable evidence | SCR-008-A04; API-011; DAT-013/012; BAT-015; BR-043 | Modification prohibited; archive-failure response Needs confirmation. S, p. 62, §17.3.1; p. 88, `T-09`. |
| ERR-053 | Response/diagnostic/provider context would disclose secrets or documents; vault/rotation dependency fails | Security/external dependency; response, invocation, telemetry, key boundary | API-PRV-001/002; DAT-052/054; applicable BAT and rotation capability; BR-043 | S, pp. 21, 54, 61–64, 84. Incident/rotation-failure procedure Needs confirmation. |
| ERR-054 | Usage/rollup is incomplete, duplicated, late, or lacks supported attribution | Internal/accounting data outcome; ledger/day | SCR-010; API-012; DAT-016/054; BAT-016; BR-042 | Attribution/daily concepts Confirmed; correction/finalization/error contract Needs confirmation. S, p. 65, §18.3.1. |
| ERR-055 | Frozen evaluation dataset/expected fixtures or signed-manifest integrity is compromised | Security/invalid verification input; evaluation | API-013/045; DAT-057; BAT-017/026; BR-045 | S, p. 88, `T-12`; p. 89, E.1 |
| ERR-056 | Evaluation has safety regression, low confidence, failed critical case, or insufficient/incomplete evidence | Restricted/internal verification; scorecard/release | SCR-010; API-013/045/043; DAT-057; BAT-017/026; BR-045 | S, pp. 74–76, 88–89. Missing-case state/formulas Needs confirmation. |
| ERR-057 | Governance invariant lacks negative-test linkage, contract is incompatible, or migration/backfill violates reader compatibility | Business/internal validation; change/migration | API-030/037/043; DAT-056/060/061; BAT-023/026; BR-046 | S, pp. 8–10, 52, 55, 72 |
| ERR-058 | Build digest/sign-off is unverified or canary regresses latency, errors, denials, or AI safety/quality | Business/internal release gate; deployment traffic | API-043/044; DAT-056/057; BAT-026; BR-045/046 | S, pp. 20, 72–73, 88–89 |
| ERR-059 | Primary region, persistence, object access, or recovery profile fails | External/internal incident; affected service/region | API-038–042; DAT-055/063; BAT-025; BR-044 | S, pp. 19, 69–70; p. 89, `TST-012` |
| ERR-060 | Background operation has no eligible input, only duplicate/ineligible input, or no usable evaluation corpus | Restricted/no-work outcome; existing job | BAT-AC-051–057; affected DAT; BR-019/029/038/045 | Empty fixtures Confirmed; universal no-work status/receipt Needs confirmation. S, p. 89, E.1. |

### Explicit Boundaries

| Category | Status and reason |
|---|---|
| Physical automation, irreversible financial transactions, foundation-model fine-tuning, unrestricted browsing, agent administrative cloud permissions | **Out of scope:** explicitly excluded by S, p. 9, §1.2.1. Attempts to use existing tools outside declared authority still require ERR-029 handling. |
| Application-hosted GPU inference failures | **Out of scope:** inference is not hosted in the application. External provider failures remain covered by ERR-035/036. S, p. 19, §4.2.1. |
| Cross-region active/active mutation, OCR beyond English, customer-managed model weights | **Deferred from this baseline:** do not invent recovery modes enabling them. S, p. 10, §1.3.2. |
| Browser session-expiry UX, health failure statuses, unhandled-runtime mapping, batch exit codes, and notification recipients | **Needs confirmation:** these are not excluded, but the source does not define complete contracts. |
| Secret or internal-model-prompt export | **Out of scope for package contents:** explicitly excluded. Inclusion is a violation under ERR-049. S, p. 79, §22.3.1. |

## Handling by Exception

### Shared Response Contract

**ERR-RES-001 — Confirmed:** Preserve the canonical public error envelope and its safe-information boundary.

| Field | Source-supported type | Requirement |
|---|---|---|
| `error` | JSON object | Canonical error container |
| `error.code` | String | Stable, non-sensitive business code; preserve exact confirmed literals |
| `error.message` | String | Safe explanation; exact copy is confirmed only where supplied |
| `error.correlation_id` | String | Safe diagnostic correlation reference |
| `error.retryable` | Boolean | Communicates applicable retryability; does not establish retry counts or delays |
| `error.details` | Optional safe structured object | Per-error schema Needs confirmation |
| `error.details.expected_revision` | Integer in the source conflict example | Example-specific expected revision |
| `error.details.actual_revision` | Integer in the source conflict example | Current revision information for case conflict |

**Source:** S, p. 84, Appendix A.3. Earlier mapping: `API-ERR-001`, `DAT-061-F02`.

The source-confirmed example is:

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "error": {
    "code": "CASE_VERSION_CONFLICT",
    "message": "Case revision no longer matches.",
    "correlation_id": "trace_01HZZ_EXAMPLE",
    "retryable": false,
    "details": {
      "expected_revision": 7,
      "actual_revision": 8
    }
  }
}
```

The correlation value and revisions are fictional fixtures, not defaults. Full-range `BIGINT` transport remains unresolved.

**ERR-RES-002 — Confirmed:** Errors must not contain connector credentials, raw provider credentials, full prompts, retrieved documents, or unauthorized resource existence. Provider bodies and internal diagnostics cannot be forwarded wholesale as public error details.  
**Source:** S, pp. 54–56, Chapter 15; p. 84, A.3.

**ERR-RES-003 — Needs confirmation:** Non-HTTP, gRPC, SSE post-connection, A2A, MCP, webhook, and batch-result error representations. The HTTP envelope is not automatically their complete protocol contract. See **ERR-OQ-001**, **ERR-OQ-011**, **ERR-OQ-014**.

### Confirmed HTTP and Outcome Register

| Condition | Confirmed contract | Unresolved boundary |
|---|---|---|
| Schema-invalid REST request | HTTP `422` | Business code, message, field-detail schema |
| Case revision conflict | HTTP `409`; `CASE_VERSION_CONFLICT`; current revision; example `retryable: false` | `If-Match` syntax and full-range revision encoding |
| Changed body under reused key | HTTP `409` `IDEMPOTENCY_CONFLICT` in `TST-002` | Complete per-endpoint conflict coverage, details, retryable flag |
| Quota/admission throttle | HTTP `429`; new-run clients receive `Retry-After` | Quota code, threshold values, header representation |
| Foreign-tenant/absent case | `404`-equivalent non-disclosing class | Exact error code/body and broader resource mapping |
| Stale/conflicting approval | Decision catalog includes HTTP `409`; stale rejection is required | Exact stale-decision mapping and business code |
| Revoked connector credentials | `CONNECTOR_REAUTH_REQUIRED` | HTTP/status-record mapping |
| Insufficient evidence | `NO_SUPPORTED_EVIDENCE` | Normal-result versus error-envelope representation and HTTP status |
| Invalid model output | `MODEL_OUTPUT_INVALID`; no publish | HTTP/internal-result mapping and attempt details |
| Arbitrary MCP invocation | `DENY` before dispatch | `DENY` is a decision outcome, not a newly confirmed error code |
| Accepted long-running work | HTTP `202` for API-004/005/009/013/014/015 | Receipt/status schemas; acceptance is not completion |

**Sources:** S, pp. 25, 27, 36, 38, 54, 69, 83–84, 89.

No undocumented authentication, upload, dependency, health, timeout, or internal-failure HTTP status is selected here.

### Shared Handling Procedure

**ERR-HDL-001 — Confirmed procedure constraints:**

1. Authenticate and establish trusted tenant, actor, trace, and correlation context.
2. Validate the approved request or job arguments before transaction entry or long-running allocation.
3. Evaluate broad authorization, then re-evaluate resource attributes inside the applicable transaction or dispatch boundary.
4. Resolve applicable idempotency binding and current revision.
5. Evaluate state, evidence, hash, policy, classification, budget, and lifecycle prerequisites.
6. Reject unsatisfied guards without changing the denied business aggregate.
7. Preserve confirmed atomicity of business state, applicable revision/decision evidence, and outbox writes.
8. Commit accepted durable work before dependent side effects.
9. If downstream work fails, preserve the actual committed state and checkpoint; apply only source-supported retry, reconciliation, quarantine, or compensation.
10. Return a documented safe error or persisted asynchronous identity, never ambiguous success.
11. Record required safe diagnostic/audit evidence and reset pooled database scope after each transaction.

**Sources:** S, pp. 22, 25, 45, 49, 52, 56, 86.

**Needs confirmation — ERR-OQ-001, ERR-OQ-004:** Exact multi-failure selection, lock/isolation, idempotency reservation, audit-failure transaction behavior, and cross-store crash protocol. This procedure does not select those mechanisms.

### Identity, Input, and Case Handling

| Exception | Response and user-facing behavior | Interruption, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-001 | Reject authentication; return no protected data or accepted work. HTTP/code and login/session message are Needs confirmation. | Stop the affected request/service invocation. Do not substitute tenant or identity. Authentication recovery must follow the approved identity/session contract, not a background retry of an unchanged invalid token. | **ERR-OQ-002:** Claims/algorithms, session recovery, status/code, service audience mapping |
| ERR-002 | Reject the unauthorized action with a stable non-sensitive outcome. Do not infer permission from visible controls. High-risk self-approval and assigned-task `no self approval` constraints remain enforced. | Leave denied business state unchanged. Permission failures are permanent and not automatically retried. Another eligible actor may act only under an authorized workflow. No role escalation, equivalent-tool substitution, or administrative override by assumption. | **ERR-OQ-002**, **ERR-OQ-012:** Role/scope/self definition; task guards; exact code |
| ERR-003 | Foreign-tenant and absent identifiers use the same not-found class. Soft-deleted data is unavailable. Do not display private title, owner, source existence, or history in the error. | Stop the affected access. Retain safe principal/denied resource-class evidence. Do not recover by searching another tenant, exposing latest source, or reviving tombstoned data. | **ERR-OQ-002**, **ERR-OQ-010:** Exact not-found mapping and source-delivery recovery |
| ERR-004 | Reject missing/incorrect tenant scope and invalid workspace-tenancy association. | No denied write or cross-tenant read. Reset scoped pooled variables after every transaction. Job envelopes preserve immutable signed tenant context. Exact detection/quarantine of a contaminated connection and incident response are unresolved. | **ERR-OQ-002**, **ERR-OQ-004** |
| ERR-005 | HTTP `422` for schema-invalid REST requests; safe validation details only. | Validate before allocating work; client validation is not authoritative. Permanent schema-invalid requests are not automatically retried. Corrected input must satisfy the approved schema and all remaining guards. | **ERR-OQ-001**, **ERR-OQ-003:** Field errors, null/blank rules, protocol mappings |
| ERR-006 | Mandatory key/precondition/context must not be silently defaulted to a new identity or latest revision. Specific rejection status/code is Needs confirmation. | Do not execute a mutation lacking its required safeguards. Retry only after approved corrected input; do not treat missing `If-Match` as unconditional overwrite. | **ERR-OQ-003:** Missing/malformed header rules, fingerprint/context schema |
| ERR-007 | `PATCH /v1/cases/{caseId}` returns HTTP `409`, `CASE_VERSION_CONFLICT`, and current revision. Preserve the source message and `retryable: false` example. | Case and accepted revision history remain unchanged. No silent overwrite or automatic replay against latest revision. Earlier suggested reload-and-explicit-reconciliation UX remains a **Proposal**; exact form preservation/conflict UI is unresolved. | **ERR-OQ-003**, **ERR-OQ-005:** Revision transport and reconciliation UX |
| ERR-008 | Reject stale settings update without business mutation. Do not automatically reuse `CASE_VERSION_CONFLICT` for settings. | Current configuration remains authoritative; accepted updates require revision precondition and audit. Reload/merge/activation behavior is unresolved. | **ERR-OQ-003**, **ERR-OQ-005:** Settings API/code/version activation |
| ERR-009 | Reject unsupported normal edges and unsatisfied state guards. Do not add closure/reopening targets. | Preserve the six confirmed normal edges and `CLOSED` finality. Closure must preserve approved answer, cited versions, reviewer decisions. Reopening is explicit new-revision work, not ordinary in-place state reversal. No automatic Reject-to-case transition. | **ERR-OQ-006:** Closing origin, reopen target, actor/approval guards and errors |
| ERR-010 | Reject stale/unauthorized classification changes. Label correction requires reason code. Priority cannot derive from model alone; breach prediction cannot change contractual deadline. | Preserve current case/correction lineage. Automatic classifier retry must not overwrite newer accepted changes. Exact missing-impact/calendar behavior and classifier-versus-correction resolution remain unresolved, not implementation defaults. | **ERR-OQ-006:** Input catalogs, formulas, correction precedence, snapshot and rerun |

**Sources:** S, pp. 11–13, 21–26, 49, 54–56, 83–86.

### Idempotency, Events, Dependency Failure, and Persistence

| Exception | Response and user-facing behavior | Interruption, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-011 | Identical repetition returns the original outcome/operation. Case-create verification requires one case and identical response; original cataloged create outcome is `201`. | Do not create a second business effect. Case actor/fingerprint binding lasts `24` hours. Current authorization and scope remain obligatory. Repetition does not convert acceptance into completed work. | **ERR-OQ-003**, **ERR-OQ-007:** Namespace, concurrent reservation, expiry and error-result replay |
| ERR-012 | Return `IDEMPOTENCY_CONFLICT`; preserve HTTP `409` verification contract. Do not report newly accepted work. | Original outcome remains unchanged; no second operation under changed fingerprint. Do not silently mint a new key or modify body to bypass conflict. Caller correction/key-change UX remains unresolved. | **ERR-OQ-003**, **ERR-OQ-007:** Canonical fingerprint, per-endpoint mapping, details/flag |
| ERR-013 | Record duplicate outcome and return without reapplying mutation. No new public error is required merely because delivery is duplicate. | Retain original event identity and accepted outcome. One accepted business transition and its accepted-transition audit record remain; duplicate-attempt evidence does not count as another accepted transition. | **ERR-OQ-007:** Consumer ledger atomicity, acknowledgment and evidence counts |
| ERR-014 | Detect stale revision and enforce required envelope/tenant/schema constraints. Public/protocol code and queue disposition are Needs confirmation. | Do not use queue ordering to bypass current invariants. Duplicate/stale replay must not resurrect deleted evidence or publish a changed artifact. Invalid permission/request context is not automatically retried. Future revision buffering, schema migration, and dead-letter disposition require a defined contract. | **ERR-OQ-007:** Stale/future events, signatures, incompatible schema disposition |
| ERR-015 | On unavailable dependency, return a documented retryable error or an actually persisted asynchronous identifier. Never return fabricated success or a fabricated empty result. | For transient failures, apply bounded backoff/jitter/circuit-breaker policy. Cross-service writes remain idempotent. A lost response is not proof that commit failed; do not start uncontrolled duplicate work. Exact outcome lookup/retry after lost response is unresolved. | **ERR-OQ-001**, **ERR-OQ-007**, **ERR-OQ-008:** Status/code, fallback per interface, lost-response lookup |
| ERR-016 | Report only actual committed state. Exact internal error/health status is Needs confirmation. | Failed confirmed ACID units cannot partially commit case/approval/outbox or gate/pointer. If failure occurs after a durable checkpoint/commit, retain it and resume/reconcile downstream effects rather than roll back unrelated accepted work. No generic database down-migration or distributed rollback is authorized. | **ERR-OQ-004**, **ERR-OQ-007:** Transaction/crash recovery, dispatch acknowledgment, audit dependency |

**Sources:** S, pp. 15–17, 25, 45, 48–54, 74, 83, 89–90.

### Connector and Ingestion Handling

| Exception | Response and user-facing behavior | Interruption, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-017 | Connector Health presents actual safe run/item outcomes. Partial batch is not full success or search readiness. | Preserve cursor, high-watermark, error ledger, and durable item outcomes. Cursor advances only after preceding items have durable ingestion outcomes. Retry partial batches safely; do not repeat already accepted business effects. | **ERR-OQ-009:** Durable-outcome stage, ordering, mixed completion, batch concurrency |
| ERR-018 | Explicit user-visible lower-trust warning; do not silently claim missing capabilities exist. | Apply source-supported lower-trust ingestion mode. Exact restrictions or stop/continue behavior by missing capability are unresolved. Missing ACL support is not permission to bypass originating access controls. | **ERR-OQ-009:** Capability trust matrix and warning projection |
| ERR-019 | Queued jobs fail with `CONNECTOR_REAUTH_REQUIRED`; show safe reauthentication-required condition without tokens. | Stop affected credential-dependent work. Do not endlessly retry revoked credentials or substitute another workspace secret. Revocation capability exists; reauthorization API/provider flow and post-reauthorization resume policy do not. | **ERR-OQ-009:** Reauthorization, HTTP/job state and actor permissions |
| ERR-020 | Fail closed for unsupported/mismatched/oversized/decompression-unsafe input. Exact upload code/status is unresolved. | Do not allocate unsafe downstream processing. Supported inputs are PDF, DOCX, HTML, UTF-8 text; MIME signature and extension agree; reference configurable per-file cap is `25 MB`. A corrected file still requires scan and remaining guards. | **ERR-OQ-010:** MB conversion, MIME/subtype catalog, archive threshold, transport and codes |
| ERR-021 | Persist actual `QUARANTINED` document outcome; no indexing. Safe status/remediation presentation only. | Scan before parse; macro execution disabled; embedded remote references not fetched. Use scan/sandbox/bounded-parser controls. Do not retry unsafe content as though transient or grant viewing/download merely because quarantined. | **ERR-OQ-010:** Scanner/parser limits, quarantine remediation/release/viewing |
| ERR-022 | Quarantined item retains reason code, correlation ID, remediation path. | After bounded source-processing retries, record exception in cursor ledger. Remaining batch **may** continue. Do not silently omit the item. Permanent job-schema/permission failures remain distinct from source-specific parser retry. | **ERR-OQ-008**, **ERR-OQ-009**, **ERR-OQ-010:** Count, taxonomy, remediated-item rerun |
| ERR-023 | Preserve quality flags and truthful safe-document status. | Authorized safe low-quality content remains viewable but is excluded from autonomous recommendations. It is not automatically malware or universally excluded from indexing. OCR fallback is opt-in and provenance-marked; changed pipelines may reprocess side by side without overwriting old derivatives. | **ERR-OQ-010:** Quality formulas/thresholds, empty documents, OCR and reprocessing launch |

**Sources:** S, pp. 27–32, §§7.1–8.3; pp. 82, 88–90.

### Index, Evidence, and Source Delivery Handling

| Exception | Response and user-facing behavior | Interruption, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-024 | Present actual processing/readiness; delayed derivative is not a ready index or unsupported-evidence proof. | Failed index writes do not roll back accepted source metadata. Compare fingerprints and retry derivatives; repair broken message links from outbox. Delayed-index incident recovery uses bounded scoped replay and denied-access probes. | **ERR-OQ-011:** Comparison scope, readiness, reconciliation exhaustion and receipts |
| ERR-025 | Do not activate an unvalidated parallel generation. Exact rebuild failure state/code is unresolved. | Source database remains authoritative. Read alias switches atomically only after completeness/recall checks. Failed generation cleanup, retry, overlapping rebuilds and old-generation rollback eligibility are not supplied. | **ERR-OQ-011:** Thresholds, delta/deletion/ACL races, cleanup |
| ERR-026 | Do not present an unverified citation as valid or substitute latest document version. Source inspection must resolve the cited immutable version and anchor. | No citation-backed generation/publication using unresolved anchors or missing current access. A transient object failure may use defined read retry. Expired signed URL is not permission to bypass authorization; renewal route/lifetime and viewer recovery are unresolved. | **ERR-OQ-010**, **ERR-OQ-011:** Anchor geometry/nonpaginated format, binary delivery and renewal |
| ERR-027 | Return literal `NO_SUPPORTED_EVIDENCE`, not fabricated context. Empty/ambiguous search remains distinguishable from dependency failure. | Stop unsupported grounded-answer/publication path. Orchestrator **may** ask for clarification or route to human. Exact selection, request, and workflow state are unresolved; unchanged insufficient input is not automatically repeated until an answer appears. | **ERR-OQ-011**, **ERR-OQ-012:** Thresholds, normal/error representation, clarification routing |

**Sources:** S, pp. 31–36, 49, 52, 57, 78, 90.

### Model, Tool, Budget, and Policy Handling

| Exception | Response and user-facing behavior | Interruption, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-028 | Fail closed against requested privilege/instruction changes; exact prompt-injection code is not supplied. Evidence is visibly/unambiguously delimited as untrusted. | Strip tool-call directives from evidence context, retain safe injection indicators, and independently authorize tools. Content cannot change tenant, approvals, deterministic policy, or network destinations. Whole-run termination on every indicator is not defined; unauthorized effects are always prohibited. | **ERR-OQ-012:** Indicator/severity contract and permitted continuation |
| ERR-029 | `DENY` before arbitrary MCP dispatch; validated pinned tool schemas and separate authorization required. Exact transport error is unresolved. | Stop denied invocation. External writes require separate capability authorization; consequential mutable operations require idempotency and human authorization. No semantically equivalent substitute tool. `knowledge.search@v1` remains tenant-scoped read-only with `read:permitted_documents`, `max_items: int<=10`, and no arbitrary URL/filesystem access. | **ERR-OQ-012:** Tool/grant schemas, consequential taxonomy, MCP status/optional fields |
| ERR-030 | `MODEL_OUTPUT_INVALID`; no publication. Run Timeline reports actual safe failed checkpoint/outcome. | Use bounded structured-output parsing/validation retries. Preserve generation attempt, deployment/prompt/version and attributed usage context. Do not put raw response, full prompt, or evidence into public error. Parsing retry versus new provider invocation is unresolved. | **ERR-OQ-008**, **ERR-OQ-012:** Schema, retry count, attempt accounting and HTTP mapping |
| ERR-031 | Report exact failed checkpoint; no admitted execution beyond DAG depth `8` or tool-call ceiling `16`. | Persist plan revision before side effects and checkpoints before dispatch. Reject cyclic/over-bound plan; exhausted call budget/repeated invalid plan is a stop condition. Previously accepted effects are not retroactively erased. No unbounded replanning. | **ERR-OQ-012:** Depth/call counting under retries/replay, invalid-plan threshold, state/code |
| ERR-032 | Report actual checkpoint and source-defined terminal/recoverable-timeout outcome. Do not invent `TIMED_OUT` or other run states. | Reference `workflow.run_timeout_seconds: 180`; source requires bounded runtime. No further dispatch beyond expired budget. Inclusion of human-review wait, timeout equality and recovery-as-new-run versus resume remain unresolved. | **ERR-OQ-012:** Waiting/termination conflict, runtime clock and recovery |
| ERR-033 | Recipient may decline; do not report decline as completed work. Exact A2A error/result vocabulary is unresolved. | Handoff keeps task/capability/input-output schema/deadline/trace context and separate permission. Permission/schema failure is not retried as transient. Deadline expiry/decline may affect dependent run checkpoints; exact continuation/retry/alternate-agent behavior is not defined. | **ERR-OQ-012:** A2A transport, output-schema property, decline/deadline mapping |
| ERR-034 | Current run terminates on quota exhaustion; exact error/run-state mapping is unresolved. | No automatic model or data-class change. Retain attributed actual usage. Budget reservation release, overrun and provider-charge correction are unresolved; failure does not authorize deleting incurred usage. | **ERR-OQ-013:** Reservation, accounting and terminal code |
| ERR-035 | New-run throttle returns HTTP `429` and `Retry-After`; saved cases remain available. Provider `429` is handled as dependency throttling, not automatically forwarded unchanged in every interface. | Admit only when workspace tokens, queue age, provider capacity meet thresholds. Connector workers honor provider `Retry-After`, bounded exponential backoff/jitter and quotas. Provider bursts use capped retries/admission control and fair scheduling. | **ERR-OQ-008**, **ERR-OQ-009**, **ERR-OQ-013:** Counts, thresholds, header computation and fairness |
| ERR-036 | Display generation degraded status. Preserve manual case editing and evidence search; lexical fallback during vector degradation requires visible reduced quality. | Disable new generation admission during provider outage. Fallback only to approved equal-or-stronger handling and approved region/deployment. Restricted content never routes to unapproved destination. No fallback can bypass authorization/review/classification. | **ERR-OQ-012**, **ERR-OQ-018:** Approved routing, outage/re-enable controls and paging budget |
| ERR-037 | Reject lower-class control bypass; no new public classification field/code is established. | Model route, log redaction, retention and approval all use maximum class of included material. `INTERNAL` case plus permitted `RESTRICTED` evidence requires applicable `RESTRICTED` controls. ACL success and `auto_publish_classification: INTERNAL` do not waive required review. Post-disclosure incident remediation is unspecified. | **ERR-OQ-012**, **ERR-OQ-018:** Provenance, unknown classes, four mappings and incident procedure |
| ERR-038 | Preserve `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY` as policy outcomes, not invented HTTP codes. Missing required approval cannot publish. | Store normalized six-input policy context with rule-set version. LLM cannot override it. Policy denial stops the denied action; rework is a new run revision. Waiting for normal human review versus terminating for missing approval remains an explicit conflict. | **ERR-OQ-012:** Full policy table, version activation, waiting/stop mapping |

**Sources:** S, pp. 7, 11–13, 37–46, 49, 61–62, 68–70, 79, 87–90.

### Review and Publication Handling

| Exception | Response and user-facing behavior | Interruption, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-039 | Approve and Reject disabled until required fields complete. Server validates approved review schema independently of UI. | No accepted incomplete decision. Display exact candidate, citations, model/prompt version, policy reasons and source inspection capability. Do not guess rationale requiredness or decision enum. | **ERR-OQ-014:** Required fields, rationale/annotations, validation details |
| ERR-040 | Reject changed/wrong hash as stale and audit. Decision API catalogs HTTP `409` conflict; exact stale-error mapping/code remains unresolved. | No immutable accepted decision or publication for substituted content under old hash. Retain prior decisions and current approved pointer. Reload/re-review flow and repeated-decision contract require confirmation; do not silently approve “similar” content. | **ERR-OQ-014:** Hash canonicalization, response and detail delivery |
| ERR-041 | Actual expired/escalated condition; no implicit approval. | Tasks expire under configured SLA and are reassigned or escalated. Preserve candidate/hash and history. Decision-versus-expiry race, eligible task states and assignment/read rights after expiry are unresolved. | **ERR-OQ-014:** SLA value/start/timezone, race, routing/notification |
| ERR-042 | Reject override without all prerequisites; code/endpoint unresolved. | Require elevated role, secondary reviewer, audited reason. Ordinary Admin/Reviewer status alone is insufficient. Allowed override extent must be defined; no historical denial rewrite or retroactive approval. | **ERR-OQ-014:** Roles, secondary reviewer, reason and scope |
| ERR-043 | Do not display `PUBLISHED` unless full gate and transaction succeed. A `200` accepted decision is not unconditional publication. | Recompute current authorization; verify immutable evidence/anchors, policy including maximum class, exact-hash eligible approvals. Final pointer and satisfied gate commit atomically. Gate failure preserves previously published pointer; old approval cannot publish different artifact. | **ERR-OQ-004**, **ERR-OQ-012**, **ERR-OQ-014:** Revalidation/atomic mechanism, code, non-review invocation |

**Sources:** S, pp. 12, 44–46, 57–58, 83, 85, 87, 89.

### Operational, Lifecycle, and Verification Handling

| Exception | Response and user-facing behavior | Interruption, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-044 | Treat stale visibility as security incident. Do not release revoked evidence or show stale cache as authorized. | Suspend affected aliases, revoke cached evidence, preserve audit traces, replay scoped ACL revisions. Re-enable search only after negative access tests pass. Ordinary propagation must make revocation effective before next query, not await TTL. | **ERR-OQ-011**, **ERR-OQ-018:** Barrier/current checks, incident scope/controls |
| ERR-045 | Connection loss is not completion. Refresh reconstructs server state. Invalid/expired cursor message/status is unresolved. | Reconnect using `Last-Event-ID`; backfill retained events only within current caller scope, without business mutation replay. Do not invent cursor reset, retention period, heartbeat, or wholesale internal-event exposure. Paginated inquiries preserve authorization. | **ERR-OQ-015:** Cursor syntax/expiry, stream errors/backfill, UI recovery |
| ERR-046 | Show persisted actual progress, not inferred success from a missing worker. Worker-failure state is unresolved. | Durable checkpoints and duplicate-safe effects remain mandatory. Lost heartbeat is fault-injection scope, but takeover/lease/fencing/cancellation policy is not supplied. Replacement execution cannot reapply an accepted effect or bypass expired budgets. | **ERR-OQ-004**, **ERR-OQ-007**, **ERR-OQ-016** |
| ERR-047 | Incomplete provisioning visible; connector sync blocked. Queue emptiness alone cannot indicate ready search. | Provision policy/key references/roles/quotas/stubs as one idempotent workflow. Historic backfill uses bounded windows, stable IDs, per-batch reconciliation receipts, coverage readiness. No automatic deletion of partially provisioned resources or invented compensation. | **ERR-OQ-016:** Completion predicate, partial resources, windows/coverage and resume |
| ERR-048 | Reject single-Admin/insufficiently independently approved lifecycle request. Exact HTTP/business code unresolved. | Two independent checks remain mandatory; export additionally has source two-person control. Eligible accepted export/delete requests return `202`. No package/purge under insufficient authority or automatic approval substitution. | **ERR-OQ-017:** Actor independence, proof/expiry and tenant/workspace extent |
| ERR-049 | Package completion requires required authorized contents and checksums. `202` or partially assembled files are not completed export. | Required contents: case metadata, approved artifacts, source references, audit manifests; exclude secrets/internal prompts. Preserve actual manifest/work outcomes. Cleanup, resumable packaging, failed checksum response and download withholding mechanics are unresolved. | **ERR-OQ-017:** Format/checksum, inventory races, partial completion/download |
| ERR-050 | Do not purge ineligible routine-retention cases or protected held records. Retain and receipt hold exceptions. | Routine case retention selects only eligible `CLOSED` cases; other tombstone/decommission/diagnostic selectors are separate. Apply category/class-dependent retention and preserve closure lineage/holds. No force delete; legal hold is not a transient dependency to retry away. | **ERR-OQ-017**, **ERR-OQ-019:** Eligibility, hold timing/release, related objects and final state |
| ERR-051 | Report actual deletion outcomes; incomplete removals or unverified receipts are not verified completion. | Enforce holds, persist tombstones, remove eligible blobs/index entries, retain completed receipts and exceptions. Use same inventory for subject access. `TenantDeletionVerified` closes purge record only from verified manifest/receipt evidence. Do not attempt unsupported restoration or overwrite immutable receipts. | **ERR-OQ-017:** Partial/held-only final state, sharing/backups, retry/verification |
| ERR-052 | Historical audit/review edits rejected; no edit UI is authorized. Archive/chain failure code/status unresolved. | Append-only batch-hash archive remains independently controlled. Retrying archive work must preserve lineage and not alter history. Archive continuation/hash verification and failure of mandatory audit persistence are unresolved. | **ERR-OQ-004**, **ERR-OQ-019:** Chain/schema/checkpoint and audit-failure handling |
| ERR-053 | Prevent sensitive values entering public responses/errors, diagnostic traces or out-of-scope provider/tool context. Safe dependency failure when vault unavailable; exact mapping unresolved. | Apply maximum-class redaction plus global prohibitions. Secrets remain vault-backed; service credentials rotate automatically; encryption keys rotate under policy without request-path bulk re-encryption. Past leakage response, old-key handling, rotation failure/rollback are not defined. | **ERR-OQ-018**, **ERR-OQ-019:** Incident and rotation recovery |
| ERR-054 | Usage display must reflect actual attributable data; execution completion does not supply missing accounting formulas. | Retain run/deployment/cost-center attribution for model, embedding, storage, indexing usage. Daily rollups show budget/forecast/rejected requests. Preserve idempotent effects; no invented zero totals, loss of actual usage, financial-close workflow or late-correction rule. | **ERR-OQ-020:** Day/formulas, duplicate ledger identity, late/partial repair |
| ERR-055 | Poisoned expected fixtures cannot be accepted as valid frozen evaluation evidence. Exact error/result state unresolved. | Enforce dataset version and signed-manifest control. Preserve actual expectations/results/version lineage. Correcting a compromised corpus requires authorized versioned fixture handling, not rewriting expected scores to pass. | **ERR-OQ-021:** Integrity verification, repair/new evaluation and signatures |
| ERR-056 | Display actual scorecard and confidence. Critical failures or low statistical confidence block release; no fabricated equivalence/pass. | Targets remain precision `>=0.97`, unsupported claims `<=0.02`, high-risk recall `1.00`; critical isolation/approval zero exceptions. Prompt/model changes require re-evaluation. Partial/empty case aggregation, execution retry and score calculation are unresolved. | **ERR-OQ-021:** Formulas, missing cases, confidence, run resume |
| ERR-057 | Do not accept incompatible contract/change/constraint enforcement that violates mandatory evidence/active-reader requirements. Exact code/state unresolved. | Revised invariant links to at least one negative test. Add nullable fields, backfill bounded batches, enforce afterward and after old replicas drain. No field deletion while active readers depend on it. Failed backfill resume/compensation is migration-specific and unresolved. | **ERR-OQ-022:** Governance/migration errors, bounds, effective versions |
| ERR-058 | Unverified allowed-build digest, unsatisfied sign-off, or safety gate cannot promote. Regressed canary blocks promotion. | Canary regression triggers automated traffic rollback; binary routing reverses first. No automatic database down-migration; compensation only if explicitly supported. Retain image/schema/prompt/routing-policy and signed test lineage. | **ERR-OQ-022:** Canary limits/duration, signing/proof, supported compensation |
| ERR-059 | Safe actual degraded/recovery status; health/readiness HTTP response contract remains unresolved. | Primary writes and one warm recovery region; restore secondary snapshots only under incident command. Test relational/object consistency and index recipes. Reference RPO `<=15 minutes`, RTO `<=4 hours`. No active/active mutation or public datastore workaround. | **ERR-OQ-018**, **ERR-OQ-023:** Restore order/inventory, roles and probes |
| ERR-060 | No universal `NO_INPUT`, `SKIPPED`, or successful-no-op status is confirmed. | Apply specific invariants: duplicates do not mutate, no unsupported answer, no implicit approval, no ineligible/held purge, no passing evaluation from absent evidence. Per-job no-work receipt/cursor/zero-row behavior must be defined. | **ERR-OQ-024:** Empty/ineligible/duplicate-only completion |

**Sources:** S, pp. 8, 19–21, 26, 48–55, 58, 62–66, 69–80, 87–90.

### Retry and Recovery Policy

**ERR-RTY-001 — Confirmed:** Retry eligibility is determined by the failure’s semantics, not merely by a broad HTTP class or by an unspecified status.

| Failure class | Confirmed retry behavior | Required limits or decisions |
|---|---|---|
| Permanent request validation/permission failure | No automatic retry | Exact error flag/protocol mapping and corrected-input workflow Needs confirmation |
| Transient workflow dependency failure | Bounded exponential backoff, randomized jitter, per-dependency circuit breaker | Attempts, base/max delay, elapsed deadline, breaker thresholds/reset Needs confirmation |
| Connector provider throttle | Honor `Retry-After`; backoff/jitter, quotas, fair scheduling | Delay representation, retry ceiling and fairness algorithm Needs confirmation |
| Malformed source parsing | Source-specific bounded retry, then quarantine with ledger exception | Parser failure taxonomy, count, remediation/rerun Needs confirmation |
| Invalid model structured output | Bounded validation/parsing retry; `MODEL_OUTPUT_INVALID`, no publish | Parsing versus reinvocation, attempt/call/token counting Needs confirmation |
| Identical HTTP replay | Return original operation/outcome | Concurrency, expiry, original-error replay Needs confirmation |
| Duplicate consumer delivery | Record duplicate without reapplication | Claim/ack/ledger transaction and retention Needs confirmation |
| Stale case/review content | No silent automatic replay against changed revision/hash | Explicit reload/reconciliation/re-review contract Needs confirmation |
| Legal hold | Preserve protected records and receipt exception | Not a retryable obstacle to bypass; release process Needs confirmation |
| Webhook delivery failure | Signed outbound retry with exponential backoff; internal case commit preserved | Retryable acknowledgments, attempts, event age and dead-letter policy Needs confirmation |

**Source:** S, pp. 25, 28–29, 38, 42, 49–50, 55, 80.

**ERR-RTY-002 — Confirmed:** Consequential mutable tool retries retain idempotency and human authorization. A retry, rerun, alternate deployment, replacement worker, or operator replay never grants new authority.  
**Source:** S, p. 42, §11.3.2; p. 87, C.2.

**ERR-RTY-003 — Needs confirmation:** Retry configuration must be specified before implementation, including the definition of exhaustion and transition into a dead letter. No numeric default is approved by this document. See **ERR-OQ-008**.

### Rollback and Compensation Matrix

| Boundary | Confirmed preservation/rollback requirement | Not authorized by this specification |
|---|---|---|
| Rejected stale/unauthorized mutation | Denied business state unchanged | Silent overwrite or mutation to “fix” the denial |
| Failed case/approval/outbox ACID unit | No partial commit within confirmed transaction | Success response for uncommitted work |
| Failed gate/final-pointer transaction | Gate and pointer commit together | Published pointer without satisfied gate |
| Failed index write | Accepted source metadata remains durable; reconcile fingerprints | Source rollback to compensate derivative failure |
| Partial sync | Durable outcomes and ledger retained; cursor cannot skip undurable predecessors | Silent exception omission or full-success claim |
| Unsafe file | Quarantine; no index | Automatic release or unrestricted quarantine viewing |
| Failed webhook | Internal case transition remains committed | Reversal because recipient failed |
| Partial provisioning | Incomplete visible; sync blocked | Invented whole-resource deletion compensation |
| Partial purge/delete | Holds, actual removals, tombstones, receipts retained; verify real outcome | Force delete or fictional all-or-nothing cross-store rollback |
| Failed index rebuild checks | No unvalidated read-alias activation | Unspecified old-index rollback or generation cleanup |
| Release regression | Automated traffic rollback; binary first; explicit compensation only | Automatic database down-migration |
| Evaluation failure | Actual results/expectations preserved; safety/confidence gate blocks release | Replacing expectations to make a pass |
| Mandatory audit/archive failure | Immutable lineage obligations remain | Choosing fail-open versus fail-closed transaction behavior without confirmation |

**Sources:** S, pp. 20, 25, 28–34, 45, 49, 55, 62, 72, 76, 78–80.

### Screen Failure Presentation

**ERR-UI-001 — Confirmed:** All displays respect current authorization, accessible textual status, meaningful live announcements, visible focus, keyboard ordering, and truthful acceptance/completion distinctions.  
**Source:** S, pp. 57–59, §§16.1–16.3.

| Screen | Confirmed failure-state obligation | Presentation Needs confirmation |
|---|---|---|
| SCR-001 Case Queue | Do not show failed list retrieval as successful empty data; creation retries preserve one outcome | Inline/global errors, list retention, invalid cursor recovery |
| SCR-002 Case Detail | Preserve authoritative revision; conflicts do not overwrite; quarantine/progress not readiness; unavailable generation still permits supported manual/evidence work | Conflict reconciliation, unsaved-input retention, retry controls, error focus |
| SCR-003 Evidence Viewer | Only verified permitted sources; no fabricated context; reduced-quality flag on lexical fallback | Unsupported-result copy, signed-URL renewal, source failure layout |
| SCR-004 Run Timeline | Persisted progress and exact failed checkpoint; connection loss not completion; scoped reconnect | Stream disconnect presentation, expired offset, user retry/cancel controls |
| SCR-005 Review Inbox | Exact review artifact/evidence; incomplete controls disabled; stale/expired decisions not implicit approval | Required field set, stale-task refresh, expiry/reassignment notifications |
| SCR-006 Connector Health | Explicit capability warning, safe reauth/quarantine outcomes, incomplete provisioning visible | Sync mixed-state schema, warning severity, reauth/remediation controls |
| SCR-007 Policy Settings | Stale/unauthorized update cannot silently activate configuration | Update/read endpoints, conflict details and activation UI |
| SCR-008 Audit Explorer | Redacted immutable evidence only; no historical edit | Query/cursor/archive-failure presentation |
| SCR-009 Overview | Illustrated aggregates are not confirmed fallback defaults or health enum | Error/unknown summary representation and backing APIs |
| SCR-010 Usage & Quality | Actual usage/evaluation results; no false release pass from partial/low-confidence output | Arrangement, progress/status/schema, partial accounting display |

No new screen, dialog, toast, route, notification center, or browser action is confirmed. See **ERR-OQ-005**, **ERR-OQ-015**, **ERR-OQ-020**, **ERR-OQ-021**.

## Logging, Monitoring, and Operations

### Recorded Evidence and Field Contracts

**ERR-LOG-001 — Confirmed:** Every request carries `trace_id` and `correlation_id`. Correlation crosses service boundaries and remains independent of provider trace IDs. Child spans represent database, connector, retrieval, model, and approval stages.  
**Source:** S, p. 16, §3.3.1; p. 64, §18.1.1.

| Field/concept | Recording requirement and scope | Type/format and unresolved projection | Source |
|---|---|---|---|
| `trace_id`, `correlation_id` | Required request/workflow correlation | Exact header names, generation, length and non-HTTP placement Needs confirmation | S, pp. 16, 64 |
| `tenant_id` | Trusted tenant context for requests, tenant-owned persistence, jobs and relevant evidence | Immutable signed job context; no invented default tenant | S, pp. 22, 48, 51 |
| `actor_id`; related principal/reviewer | Responsible authenticated actor for durable changes/decisions; denial retains principal | Mapping to `actor`, `reviewer_id`, historical identities Needs confirmation | S, pp. 23, 45, 85 |
| `revision`, `aggregate_revision` | Durable mutation/stale-delivery context | Case `BIGINT`; other types/public encoding unresolved | S, pp. 25, 48, 86 |
| `occurred_at`; related source timestamps | Durable occurrence evidence | UTC; public RFC 3339; display workspace-local timezone label | S, pp. 48, 54, 59 |
| `event_id`, `type`, `schema_version`, `aggregate_id` | Original event envelope and replay identity | Exact event schemas preserved; storage/projection unresolved | S, p. 48, §13.1.1 |
| Operation key/fingerprint and duplicate outcome | Required idempotency/consumer comparison evidence | Logging raw HTTP key versus safe reference/digest is not defined; avoid assuming disclosure | S, pp. 25, 48, 54 |
| Case/run/task/document/version/chunk/connector/checkpoint references | Scope and reproducibility of affected stage/outcome | Safe identifiers; exact error/log properties unresolved | S, pp. 31, 41, 49, 85, 90 |
| Policy result, applied rule-set version and normalized input provenance | Reproduce decisions and determine gate denial | Logs use safe identifiers/outcomes; full input records remain separately access-controlled | S, pp. 44, 64 |
| Reviewed artifact hash and decision metadata | Binding and stale-review audit | Hash algorithm/canonicalization/encoding unresolved | S, p. 45, §12.2.2 |
| Source fingerprints, ACL revision, index generation | Reconciliation and revocation diagnosis | Digest formats and safe public projection unresolved | S, pp. 28, 34, 49, 90 |
| Parser quality flags and prompt-injection indicators | Retained quality/security evidence | Safe flags, not malicious source text | S, pp. 32, 39, 90 |
| Quarantine reason, correlation ID, remediation path | Poison-record recovery information | Reason catalog/path format unresolved | S, p. 29, §7.3.2 |
| Token counts, deployment version, cost-center attribution | Usage and failure accounting | Units/ledger identity and public aggregation unresolved | S, pp. 38, 65 |
| Manifest/receipt references and checksums/hashes | Export/purge verification and held-data evidence | Algorithms/formats unresolved | S, pp. 79–80, 87 |
| Incident audit IDs, time window, blast radius, quality effect, preventive action | Required delayed-indexing incident documentation | Incident record schema, recipients and system unresolved | S, p. 90, F.1 |
| Exception ID, retry attempt, elapsed time, severity, stack trace | Not completely specified by source | **Needs confirmation**; these are not newly confirmed stored fields | S, pp. 49, 64 lacks these schemas; ERR-OQ-019 |

**ERR-LOG-002 — Confirmed:** Each accepted transition has one accepted-transition audit record and correlated evidence. Duplicate delivery records a duplicate outcome without another accepted mutation. The total number of diagnostic records for attempts is not specified.  
**Source:** S, p. 50, §13.5; p. 74, §21.1.2; p. 89, `TST-007`.

**ERR-LOG-003 — Confirmed:** Audit entries are append-only, chained with batch hashes and exported to independently controlled retention storage. Operators may query, not edit, historical review decisions.  
**Source:** S, p. 62, §17.3.1.

### Sensitive-Value Handling

| Information | Required handling |
|---|---|
| Source document text or retrieved passages | Never in diagnostic traces; never in public errors |
| API secrets, connector tokens, service credentials, raw provider credentials | Never in diagnostic traces, model prompts, public responses/errors or out-of-scope invocations |
| Full prompts | Not logged by default; excluded from errors and internal-model-prompt export contents |
| Personal data | Extraction tags likely personal data; redact nonessential provider-bound fields where policy permits |
| Untrusted provider/parser exception content | Must not bypass safe error/diagnostic boundaries |
| Resource existence | Denials cannot disclose private foreign-tenant existence |
| Signed object delivery | Access-controlled, short-lived; logging of raw signed URL/token components is not defined and requires confirmation |
| Audit/detail content | Respect Auditor redacted scope and current authorization |
| Run classification | Highest included-material class governs log redaction and retention in addition to global prohibitions |

**Sources:** S, pp. 21, 54, 61–64, 79, 84.

**ERR-LOG-004 — Needs confirmation:** Stack-trace policy, sanitizer implementation, log-field allowlist, key/URL redaction, PII detector schema, and remediation of already-written sensitive logs. See **ERR-OQ-019**. No “log full exception” fallback is authorized.

### Log Levels and Retention

The source specifies correlated records and actionable alerts, but no `DEBUG`, `INFO`, `WARN`, `ERROR`, or `CRITICAL` assignment.

| Outcome family | Required evidence | Log level |
|---|---|---|
| Controlled duplicate/idempotent replay | Original outcome and duplicate evidence | Needs confirmation |
| Invalid input, stale write, permission denial | Safe stable outcome; applicable denial/audit evidence | Needs confirmation |
| Capability warning, quarantine, insufficient evidence, expiry, legal hold | Actual restricted outcome and relevant reason/receipt/routing evidence | Needs confirmation |
| Transient retry/provider throttle | Correlation and defined retry/capacity evidence | Needs confirmation |
| Terminal run/internal failure | Actual checkpoint/state and safe diagnostic evidence | Needs confirmation |
| ACL leak, secret disclosure/control breach, critical release failure | Required incident/security evidence and applicable alert | Needs confirmation |

**ERR-LOG-005 — Confirmed reference values:**

- `observability.trace_sample_rate: 0.10`
- `observability.diagnostic_retention_days: 30`
- `observability.audit_retention_years: 7`

Diagnostic sampling does not remove mandatory accepted-transition audit evidence. Diagnostic and security-audit retention are distinct; purges record receipts and legal-hold exceptions. Detailed corporate/per-class policy and calendar calculations remain unresolved.  
**Source:** S, pp. 62, 66, 90. See **ERR-OQ-019**.

### Monitoring and Notification Conditions

| Signal/condition | Confirmed operational use | Recipient/channel/threshold status |
|---|---|---|
| Request rate, error rate, latency, saturation | Golden reliability signals | Formulas, windows, labels, thresholds Needs confirmation |
| Grounding pass rate, retrieval empty rate | AI-specific signals | Denominators and alert thresholds Needs confirmation |
| Provider throttling, token use | Control retries/admission and monitor spend | Thresholds and destinations Needs confirmation |
| Approval backlog age | Review operational signal | Queue/routing/escalation thresholds Needs confirmation |
| Queue oldest age, index backlog | Alert and identify affected tenant/index generation | Numeric age/backlog threshold and alert channel Needs confirmation |
| Outbox lag, parser flags, search throttling, ACL revision | Delayed-index diagnosis | Metric definitions/queries Needs confirmation |
| User-impacting failure budget, stale ACL propagation, missing approval enforcement | Paging category | Named recipients, service roster and notification system Needs confirmation |
| Model provider outage | Page on-call only when availability budget is impacted | On-call identity, budget formula and channel Needs confirmation |
| Routine token-spend anomaly | Ticket with configured owner and threshold | Actual owner/threshold not supplied; do not assign them here |
| Review expiry | Reassign or escalate; no silent approval | Pool/escalation recipient and notification channel Needs confirmation |
| Export/delete/evaluation/provisioning completion/failure | Actual safe operation outcomes required | No completion recipient/channel supplied |
| Optional outbound webhook | Signed, age-verified, exponentially retried delivery | Recipient registration/method/signature/age/retry contract Needs confirmation |

**Sources:** S, pp. 45, 55, 64–66, 79, 90.

**ERR-MON-001 — Confirmed reference objectives:** Public API availability `99.9%` monthly; case-create P95 `<300 ms`; search P95 `<1.5 s`, excluding remote connector fetch; model latency measured separately. These do not supply paging thresholds or retry schedules.  
**Source:** S, p. 65, §18.2.1.

**ERR-MON-002 — Needs confirmation:** Alert deduplication, grouping, escalation timing, severity, suppression, acknowledgment, named recipients, and delivery failure handling. No email/SMS/chat integration or notification-center screen is established. See **ERR-OQ-018**.

### Operator Inspection Interfaces

| Existing interface | Supported inspection/recovery purpose | Boundary |
|---|---|---|
| API-033 `GET /internal/workflows/{runId}` | Persisted workflow/checkpoint inquiry | Internal/operator scope and schema Needs confirmation |
| API-034 `POST /internal/deadletters/{id}/replay` | Guarded replay | Reason, dry-run validation, scope limit mandatory |
| API-025 `GET /v1/connectors/{connectorId}/runs` | Safe sync outcomes/cursor exception information | Read permissions/public projection unresolved |
| API-018 `GET /v1/documents/{documentId}/status` | Processing/quarantine status | Document access and status schema required |
| API-006 `GET /v1/runs/{runId}`; API-019 `GET /v1/runs/{runId}/steps` | Actual run and checkpoint state | Resource authorization; complete schemas unresolved |
| API-011 `GET /v1/audit/events` | Cursor-paginated immutable audit inquiry | `Auditor`, tenant/redacted scope |
| API-040 `GET /internal/metrics`; API-042 `GET /internal/capacity` | Monitoring/capacity context | Internal access and safe schemas unresolved |
| API-041 `GET /v1/system/degraded-modes` | Supported degradation information | Read scope/mode schema unresolved |
| API-044 `GET /internal/releases/{releaseId}` | Release/build/prompt/policy/configuration lineage | Authorized operator scope |
| API-035 `GET /internal/storage/documents/{id}` | Authorized storage inquiry | Not a direct browser source route by assumption |

**Sources:** S, Chapters 7–15, 18–20; pp. 83–85. Existing identifiers remain as defined in [02_api.md](02_api.md).

No pause, alias-suspension, cache-revocation, re-enable, or provisioning-repair endpoint is invented from operational procedure text.

### Operator Recovery Procedures

#### ERR-OPS-001 — Controlled Dead-Letter/Outbox Replay

1. Authenticate the operator and validate tenant/resource scope.
2. Require an audited operator reason.
3. Perform dry-run validation before execution.
4. Enforce the approved scope limit.
5. Preserve original event identity and envelope.
6. If explicit schema migration transforms the event, retain the required provenance link.
7. Dispatch through original event/operation deduplication, current revision, access, and domain guards.
8. Verify actual outcomes and preserve replay evidence.

**Source:** S, p. 50, §13.3.2.  
**Needs confirmation:** Operator roles, dry-run transport, numerical/time limits, acknowledgment and partial replay — **ERR-OQ-007**.

#### ERR-OPS-002 — Delayed Document Indexing

1. Detect queue oldest age and index backlog.
2. Identify affected tenant and index generation.
3. Pause only the faulty connector or indexer shard.
4. Keep accepted source records durable.
5. Inspect event ID, outbox lag, parser flags, search throttling and source ACL revision.
6. Replay validated outbox records with bounded operator-controlled scope.
7. Compare source fingerprints to indexed versions.
8. Run denied-access probes before closing recovery.
9. Document audit IDs, time window, blast radius, quality effect and preventive action.

**Source:** S, p. 90, F.1.  
**Needs confirmation:** Alert threshold, control interfaces, replay bounds, comparison/coverage criteria — **ERR-OQ-011**, **ERR-OQ-018**.

#### ERR-OPS-003 — Suspected ACL Leak

1. Suspend affected index aliases.
2. Revoke cached evidence.
3. Preserve audit traces.
4. Replay scoped ACL revisions through authorized recovery.
5. Re-enable search only after negative access tests pass.

**Source:** S, p. 79, §22.2.2.  
**Needs confirmation:** Scope/roles, invalidation barrier, control methods and negative-test matrix — **ERR-OQ-011**, **ERR-OQ-018**.

#### ERR-OPS-004 — Model Provider Outage

1. Disable new generation admission.
2. Keep manual case and evidence workflows available.
3. Display degraded status.
4. Permit lexical retrieval during vector degradation only with visible reduced quality.
5. Preserve approved deployment/region, maximum-class, authorization and approval controls.
6. Page on-call only when availability budget is impacted.

**Source:** S, p. 37, §10.1.2; p. 69, §19.2.2; p. 79, §22.2.1.  
**Needs confirmation:** Outage detection, re-enable criteria, approved fallback selection and paging budget — **ERR-OQ-012**, **ERR-OQ-018**.

#### ERR-OPS-005 — Regional Recovery

1. Execute restoration under incident command, using the R1 primary/warm-recovery profile.
2. Resolve the authorized recovery point and related relational/object inventory.
3. Restore secondary snapshots under that command.
4. Test object versions and index rebuild recipes together.
5. Verify relational/object consistency and access safety.
6. Measure RPO `<=15 minutes` and RTO `<=4 hours`.
7. Retain recovery evidence.

**Source:** S, p. 19, §4.2.2; pp. 69–70, §19.3; p. 89, `TST-012`.  
**Needs confirmation:** Exact restore order, inventory consistency rules, commands/roles, exercise frequency and probe contracts — **ERR-OQ-023**. RPO is not a backup schedule.

#### ERR-OPS-006 — Release Regression

1. Validate state-machine/schema compatibility before traffic movement.
2. Compare canary latency, errors, authorization denials and AI-quality/safety against baseline.
3. Block promotion for failed critical gates or missing required evidence/sign-off.
4. On regression, perform automated traffic rollback, reversing binary routing first.
5. Use compensating data operations only when explicitly supported.
6. Do not automatically down-migrate the database.
7. Preserve reconstructible release and signed-test evidence.

**Source:** S, p. 20, §4.3.2; pp. 72–73, §§20.2–20.3; pp. 88–89.  
**Needs confirmation:** Thresholds, duration, approved compensation and sign-off proof — **ERR-OQ-022**.

## Failure Acceptance Criteria

### Verification Basis

**ERR-AC-BASIS-001 — Confirmed:** Use synthetic identities, cases, documents and provider replies. Include successful, empty, mixed-permission, adversarial, malformed, duplicate, delayed and partial-failure fixtures. Record randomized seeds. Critical isolation and approval tests pass with zero exceptions.  
**Source:** S, pp. 74–75, §§21.1–21.2; p. 89, E.1.

**ERR-AC-BASIS-002 — Confirmed:** Test state transitions, idempotency, tenant filters, approval hashes, retry semantics and compatibility without live model calls where specified. Use disposable integration environments for PostgreSQL transactions, outbox replay, ACL revocation, delayed indexing and object purge.  
**Source:** S, p. 74, §21.1.

An unresolved schema, threshold, actor, state edge, retry count or algorithm blocks the corresponding executable fixture. It does not remove the acceptance obligation or authorize inventing a contract.

### Identity, Input, and Replay Tests

| Acceptance ID | Exceptions / earlier tests | Trigger and action | Expected response, screen/data state and retry result | Source / blocker |
|---|---|---|---|---|
| ERR-AC-001 | ERR-001; API-AC-001 | Submit token with missing tenancy claim or unexpected algorithm | Authentication rejected before protected data/work; no default tenant. Exact HTTP/code not guessed. | S, p. 21, §5.1.1; ERR-OQ-002 |
| ERR-AC-002 | ERR-002; BR-027 | Attempt own high-risk recommendation approval and assigned-task self-approval fixture | Denied; no published pointer/accepted prohibited decision. Admin status does not supply review independence. | S, pp. 11, 45, 85, 90; self identity fixture ERR-OQ-002 |
| ERR-AC-003 | ERR-003; `T-01`, `TST-003` | Read valid foreign-tenant case and absent case | Same `404`-equivalent non-disclosing class; no private metadata; safe principal/resource-class evidence. | S, pp. 23, 88–89 |
| ERR-AC-004 | ERR-004; DAT-AC-001/002 | Use another tenant’s workspace in case write; reuse pooled connection across tenants | Invalid association rejected without mutation; pool scope reset; no foreign row exposure. | S, p. 86, B.2 |
| ERR-AC-005 | ERR-005/006 | Submit invalid approved schema and missing required safeguard | Schema-invalid REST request `422`; no long-running allocation. Missing key/precondition cannot default to unguarded execution. Its exact status/code awaits confirmation. | S, pp. 54, 56; ERR-OQ-003 |
| ERR-AC-006 | ERR-007; SF-AC-006 | Submit valid PATCH using stale `If-Match` | `409 CASE_VERSION_CONFLICT`, source-safe message/current revision, `retryable: false` example; unchanged case/history; no silent retry overwrite. | S, pp. 25, 84 |
| ERR-AC-007 | ERR-008/009; BR-AC-002 | Attempt stale settings update, unlisted normal edge, or ordinary exit from `CLOSED` | Rejected without business change; six confirmed edges retained; closure/reopen details not invented. | S, pp. 24–26; ERR-OQ-006 |
| ERR-AC-008 | ERR-010; BAT-AC-004 | Deliver classifier result after newer correction/revision; submit correction without required reason | No stale overwrite; correction reason/provenance requirement enforced. Detailed precedence uses approved rule, not a fixture assumption. | S, pp. 12, 25, 48; ERR-OQ-006 |
| ERR-AC-009 | ERR-011/012; `TST-001/002` | Repeat valid create with same key/body, then change body under reused key | One case and identical original response; changed body `409 IDEMPOTENCY_CONFLICT`; no second case/job outcome. | S, p. 89 |
| ERR-AC-010 | ERR-013/014; `T-07`, `TST-007` | Replay same event `100` times; inject delayed/stale revisions | Exactly one accepted business transition and accepted-transition audit record; duplicate outcomes retained without reapplication; no cross-partition ordering dependence. | S, pp. 48, 88–89 |
| ERR-AC-011 | ERR-014 | Submit invalid signed tenant context/envelope and unauthorized replay | No business effect under invalid context; permanent permission/schema faults not retried as transient. Queue disposition/code follows approved contract. | S, pp. 22, 48–50; ERR-OQ-007 |
| ERR-AC-012 | ERR-015/016 | Fail dependency before allocation; separately lose response after committed accepted work | Documented retryable error or real persisted async identity; no ambiguous/fabricated success. Repetition preserves one original accepted effect. Lost-response lookup test blocked until contract defined. | S, pp. 12, 15, 49, 54; ERR-OQ-007/008 |

### Connector, File, Index, and Evidence Tests

| Acceptance ID | Exceptions / earlier tests | Trigger and action | Expected response, screen/data state and retry result | Source / blocker |
|---|---|---|---|---|
| ERR-AC-013 | ERR-017; BAT-AC-006 | Fail incremental sync after some durable items; retry batch | Cursor does not skip undurable predecessors; durable outcomes/high-watermark/error ledger retained; no duplicate accepted item effect; partial not readiness. | S, p. 28, §7.2.1 |
| ERR-AC-014 | ERR-018/019 | Remove capability support; revoke credentials before queued sync | Visible lower-trust warning; revoked job `CONNECTOR_REAUTH_REQUIRED`; no token exposure or substituted credential. | S, p. 27, §7.1 |
| ERR-AC-015 | ERR-020 | Submit type mismatch, unsupported subtype, cap-exceeding and decompression-unsafe fixtures | Fail closed before unsafe processing; no invented upload HTTP/code. Exact cap-byte/decompression boundaries require confirmation. | S, p. 30, §8.1.1; ERR-OQ-010 |
| ERR-AC-016 | ERR-021; `T-04`, `TST-015` | Upload polyglot/unsafe PDF or zipped malicious payload | Scan/sandbox/bounded parser controls; quarantine; no indexing, macros or embedded remote fetch; no assumed quarantine-view grant. | S, pp. 30, 88–89 |
| ERR-AC-017 | ERR-022 | Exhaust approved bounded parser retries for one source item with other valid items | Quarantine reason/correlation/remediation and cursor exception retained; remaining batch may proceed; no silent omission. | S, p. 29; count ERR-OQ-008/010 |
| ERR-AC-018 | ERR-023 | Process safe low-quality and OCR-not-opted-in sources | Quality flags retained; safe source viewable but not autonomous support; no automatic OCR fallback or universal malware/no-index classification. | S, pp. 31–32 |
| ERR-AC-019 | ERR-024; DAT-AC-016 | Fail index write after accepted source; later reconcile | Source remains durable; fingerprint comparison/retry repairs derivative; broken links repaired from outbox; no false ready state. | S, p. 49, §13.2.2 |
| ERR-AC-020 | ERR-025 | Fail parallel completeness/recall checks, then pass approved checks | Failed generation not activated; successful alias switch atomic after checks; no old-version/source overwrite. | S, p. 34; thresholds ERR-OQ-011 |
| ERR-AC-021 | ERR-026 | Activate unresolved citation or fail object delivery for exact cited source | No invalid citation/latest-version substitution; supported source-inspection path retains authorization and exact anchor. Signed-URL renewal follows confirmed-to-be-completed contract. | S, pp. 31, 35, 52, 57; ERR-OQ-010/011 |
| ERR-AC-022 | ERR-027; `TST-009` | Search insufficient/empty evidence; generate missing citations | `NO_SUPPORTED_EVIDENCE` where applicable; missing citations yield needs-review or unsupported outcome; no fabricated approved answer. Dependency failure is not silently empty support. | S, pp. 36, 89 |
| ERR-AC-023 | ERR-044; `T-08`, `TST-004` | Revoke source permission after index/cache population; query next | No forbidden text to user/model; invalidation before release, not TTL waiting. Stale visibility invokes security containment. | S, pp. 27–28, 53, 88–89 |

### Model, Tool, Run, and Review Tests

| Acceptance ID | Exceptions / earlier tests | Trigger and action | Expected response, screen/data state and retry result | Source / blocker |
|---|---|---|---|---|
| ERR-AC-024 | ERR-028/029; `T-02`, `TST-014` | Embed hostile instructions; invoke arbitrary/forged tool; substitute equivalent denied tool | Evidence has no authority; directives stripped/indicators retained; `DENY` before unauthorized dispatch; no tenant/approval/destination change. | S, pp. 7, 39, 41–42, 87–89 |
| ERR-AC-025 | ERR-030; `TST-005` | Return unknown fields, invalid citations or injected control characters | `MODEL_OUTPUT_INVALID`; bounded validation retries; safe checkpoint; no publish and no raw model/prompt/evidence error content. | S, pp. 38, 89 |
| ERR-AC-026 | ERR-031; `T-10` | Return cycle/recursive hints, depth beyond `8`, or attempted call beyond `16` | No beyond-bound dispatch; exact failed checkpoint; persisted plan/checkpoint prerequisites maintained. Retry/replay counting uses approved convention. | S, pp. 40–42, 88, 90; ERR-OQ-012 |
| ERR-AC-027 | ERR-032/033 | Expire runtime/task deadline or cause A2A recipient decline | No false completed/published result; actual checkpoint; runtime bounded; no invented timeout/decline state. Waiting semantics and A2A wire assertions await confirmation. | S, pp. 12, 41, 49, 87, 90; ERR-OQ-012 |
| ERR-AC-028 | ERR-034/035; `TST-008` | Exhaust tokens; fail admission; inject provider `429` bursts | Current exhausted run terminal without model/class downgrade; throttled new run `429 Retry-After`; capped dependency retries/admitted load; saved cases available. | S, pp. 38, 69, 89 |
| ERR-AC-029 | ERR-036; `T-06` | Outage approved deployment; offer unsafe region/weaker fallback | No restricted content to unapproved route; only approved equal-or-stronger fallback; manual/evidence remain supported and degraded status visible. | S, pp. 37, 69, 79, 88 |
| ERR-AC-030 | ERR-037; API-AC-034, DAT-AC-023, BAT-AC-027, BR-AC-001 | Run authorized `INTERNAL` case with permitted anchored quality-appropriate `RESTRICTED` evidence; attempt unreviewed publish | All four controls use applicable `RESTRICTED` policy; lower case/ACL success/INTERNAL auto-publish cannot waive human review/evidence/hash gates. Inspect controlled internal provenance, not invented public field. | S, pp. 62, 90; maps ERR-OQ-012 |
| ERR-AC-031 | ERR-038/039 | Policy denies/requires evidence/review; leave required review fields incomplete | Denied action cannot proceed; no publish without required approval; Approve/Reject disabled; server validates approved schema. | S, pp. 41, 44–46, 58 |
| ERR-AC-032 | ERR-040; `T-03`, `TST-006` | Change candidate after review or approve wrong hash | Stale rejection audited; no prohibited decision/publication; prior immutable decisions and approved pointer preserved; no automatic similar-content acceptance. | S, pp. 45, 88–89 |
| ERR-AC-033 | ERR-041; `TST-010` | Expire configured review task | No implicit approval; reassignment/escalation recorded; UI actual expiry; expiry-versus-submit race follows approved contract. | S, pp. 45, 89; ERR-OQ-014 |
| ERR-AC-034 | ERR-042/043 | Attempt incomplete override; revoke evidence before publish; fail gate transaction | Override prerequisites enforced; current access failure blocks; gate/pointer cannot partially commit; old approval cannot publish changed artifact. | S, pp. 45–46 |
| ERR-AC-035 | ERR-045; SF-AC-015/024 | Disconnect SSE, refresh/reconnect with retained valid offset; separately use expired offset | Server progress restored; monotonic scoped backfill; no mutation replay or completion claim. Invalid-offset recovery awaits contract; keyboard/focus and meaningful announcements preserved. | S, pp. 55, 58–59; ERR-OQ-015 |
| ERR-AC-036 | ERR-046 | Lose worker heartbeat after checkpoint or during side effect | No duplicated accepted business outcome or false completion; persisted state retained; takeover/fencing/deadline assertions depend on approved mechanism. | S, p. 70, §19.3.2; ERR-OQ-016 |

### Lifecycle, Security Evidence, and Recovery Tests

| Acceptance ID | Exceptions / earlier tests | Trigger and action | Expected response, screen/data state and retry result | Source / blocker |
|---|---|---|---|---|
| ERR-AC-037 | ERR-047 | Fail provisioning partway; attempt sync; leave backfill queue empty with incomplete coverage | Incomplete visible, sync blocked; idempotent provisioning; stable IDs/per-batch receipts; no queue-empty readiness. Compensation not invented. | S, p. 78 |
| ERR-AC-038 | ERR-048/049; `T-11` | Single Admin export/delete attempt; then authorized export with missing/corrupt/package contents | Independent controls enforced; accepted work `202` only; required package/checksums/exclusions; no false complete or prohibited secret/internal-prompt contents. | S, pp. 78–79, 83, 88 |
| ERR-AC-039 | ERR-050/051; `TST-013` | Routine retention includes open/ineligible/eligible/held cases; inject blob/index purge failure | Only eligible closed routine cases; held records retained/receipted; real completed removals retained; no force-delete or unverified `TenantDeletionVerified`. | S, pp. 26, 80, 87, 89 |
| ERR-AC-040 | ERR-052; `T-09` | Attempt historical edit; fail audit archive continuation | Edit rejected; immutable chain/history not rewritten. Archive failure/checkpoint verification awaits format/transaction contract. | S, pp. 62, 88; ERR-OQ-019 |
| ERR-AC-041 | ERR-053; `T-05` | Inspect errors/traces/provider requests and simulate vault/rotation unavailability | No credentials/documents/full unsafe prompts/out-of-scope secrets; scoped vault controls retained; no plaintext fallback/request-path bulk re-encryption workaround. | S, pp. 21, 54, 61–64, 84, 88 |
| ERR-AC-042 | ERR-054 | Repeat daily rollup with duplicate/late usage and partial attribution | Actual supported attribution maintained; idempotent effects; no invented zero totals or finalization. Exact totals/correction states await formulas. | S, pp. 38, 65; ERR-OQ-020 |
| ERR-AC-043 | ERR-055/056; `T-12`, `TST-016` | Replace expected fixtures; produce high benchmark with critical finding/low confidence/safety regression | Fixture integrity enforced; actual results/expectations retained; critical or low-confidence outcome blocks promotion regardless of scores. | S, pp. 74–76, 88–89 |
| ERR-AC-044 | ERR-057/058 | Delete required field with active reader, enforce early, promote unverified digest, or regress canary | Compatibility/build/gate blocked; bounded expand/backfill/enforce; traffic rollback on regression, no automatic DB down-migration; reconstructible signed evidence. | S, pp. 20, 52, 55, 72–73 |
| ERR-AC-045 | ERR-059; `TST-012` | Primary outage with relational/object/index recovery exercise | Incident-command restore, safety/consistency verified; RPO `<=15 minutes`, RTO `<=4 hours`; no active/active/public datastore workaround. | S, pp. 19, 69–70, 89 |
| ERR-AC-046 | ERR-060; BAT-AC-051–057 | Empty, duplicate-only, ineligible, held-only or missing-corpus job inputs | Specific safety invariants maintained; no generic fabricated successful no-op/ready/approved/evaluation pass. Exact per-job receipt/status remains blocked. | S, pp. 36, 45, 76, 80, 89; ERR-OQ-024 |
| ERR-AC-047 | ERR-OPS-001–004 | Recover delayed index/ACL leak; replay without reason/dry-run/scope; then authorized recovery | Unguarded replay denied; bounded identity-preserving recovery; accepted source durable; fingerprints/negative probes before resume; provider outage retains manual/evidence/safety. | S, pp. 50, 79, 90 |
| ERR-AC-048 | ERR-LOG/MON; BAT-024 | Fail optional webhook after committed case change; inspect retention and notifications | Internal case unchanged; signed retry/recipient age verification; distinct diagnostic/audit policies; mandatory audit not sampled away; notifications follow confirmed categories, not invented recipients. | S, pp. 55, 62, 65–66, 90 |

### Release Evidence

**ERR-AC-RELEASE-001 — Confirmed:** Exception verification contributes to the minimum release pack: negative authorization, workflow replay, schema evolution, staging connector sync, visual accessibility, search recall, grounding, policy recall, load and disaster recovery, alongside unit tests. Outputs are signed and referenced by release digest.  
**Source:** S, p. 89, E.2.

**ERR-AC-RELEASE-002 — Confirmed:** Unmitigated critical cross-tenant or approval-bypass findings block promotion regardless of model benchmark score. `SEC-001` through `SEC-012` are release-blocking, but their individual definitions and mapping to `T-01`–`T-12` are not supplied.  
**Source:** S, p. 88, D.1. See **ERR-OQ-021/022**.

## Consistency and Open Questions

### Consistency Findings and Required Amendments

Earlier documents are not rewritten here. Confirmed source requirements remain mandatory; repeated proposals remain proposals.

| Finding ID | Conflict or evidence distinction | Affected identifiers/files | Required clarification or controlled amendment |
|---|---|---|---|
| ERR-CNS-001 | General source wording says stable snake-case; concrete codes are uppercase. S, pp. 54, 84, 89. | ERR-RES-001; ERR-007/012/019/027/030; SF-CON-005; API-CNS-007; DAT-CNS-021; BR-CNS-016 | Preserve all exact existing literals. Define future naming separately; no lowercase conversion. |
| ERR-CNS-002 | `422`, `429`, `409` have source meanings, but not every exception has an HTTP mapping. Decision API catalogs `409`; wrong-hash test requires stale/audited rejection without a named code. | ERR-005/007/012/035/040; API failure register/API-OQ-017; SCR-005-A03 | Complete endpoint-specific status/details. Do not infer upload/auth/dependency/timeout/health codes or make every stale condition `CASE_VERSION_CONFLICT`. |
| ERR-CNS-003 | `AWAITING_REVIEW`, missing-approval termination, recoverable timeout and `FAILED` coexist. S, pp. 12, 41, 45, 49, 82, 90. | ERR-032/038/041; SF-CON-004; API-CNS-003; DAT-CNS-014; BAT-CNS-004; BR-CNS-002 | Define normal review wait versus missing-approval failure and runtime inclusion of wait. Preserve existing states; no invented timeout state. |
| ERR-CNS-004 | Permanent workflow validation/permission failure coexists with bounded source parsing and model validation retries. S, pp. 29, 38, 49. | ERR-005/014/022/030; API-RTY-002–004; BAT-CNS-005; BR-036 | Define stage-specific taxonomy and exhaustion. Do not retry invalid job authority/schema or disable source-confirmed bounded parser/model handling. |
| ERR-CNS-005 | Rejected writes leave business state unchanged while `AccessDenied` remains required evidence. Source checkpoint wording generically mentions rejecting before publishing that event. S, pp. 22–23, 87. | ERR-002/004; API-AUTH-002; DAT-CNC-008; BAT-LOG-003 | Clarify denied aggregate versus denial/audit record. Do not suppress `AccessDenied` evidence because business mutation was rejected, and do not mutate denied aggregate to record denial. |
| ERR-CNS-006 | One accepted-transition audit record is required; duplicate outcomes are also recorded. | ERR-013; ERR-LOG-002; API-AC-026; DAT-AC-026; BAT-AC-019; BR-008 | Distinguish one accepted outcome from diagnostic/duplicate-attempt records. Do not assert every replay creates a new accepted audit transition or prohibit separate duplicate evidence. |
| ERR-CNS-007 | Case-key binding and workflow dedup both use `24` hours, but are different policies; SSE/cache/outbox/general HTTP retention not defined. | ERR-011/013/045; API-IDEM-003–005; DAT-RET-005/006; BAT-CNS-016; BR-CNS-017 | Define each namespace/expiry behavior independently. No universal TTL or replay permission after expiry. |
| ERR-CNS-008 | Revocation-before-next-query must coexist with asynchronous cache/index processing. S, pp. 27–28, 48, 53. | ERR-026/044; BAT-CNS-007; BR-CNS-011; DAT-RI-006 | Confirm fail-closed barrier/current checks and concurrent fills; eventual delivery cannot permit forbidden next-query evidence. |
| ERR-CNS-009 | Failed index preserves source; cursor durability and queue emptiness are not readiness. S, pp. 28, 49, 78. | ERR-017/024/047; BAT-CNS-006/009; BR-020/033/035 | Complete durable-outcome stage/coverage and UI states without claiming `202`, cursor advancement or empty queue means `READY`. |
| ERR-CNS-010 | Safe low quality and unsafe quarantine are distinct. S, pp. 30–32. | ERR-021/023; SCR-002-F23/F25; DAT-029; BAT-CNS-020; BR-CNS-012 | Preserve safe viewing/autonomous exclusion; do not impose unsupported universal low-quality no-index or quarantine-view permission. |
| ERR-CNS-011 | Maximum material class governs four controls; earlier Stage 1 field summary does not explicitly enumerate all four. S, p. 62. | ERR-037; SCR-002-F10, SCR-007-F09–11; API-CNS-013; DAT-CNS-015; BAT-CNS-010; BR-CNS-006 | Required earlier amendment remains: explicitly link routing, log redaction, retention, approval. No case-label/ACL shortcut, seventh input or automatic relabeling. |
| ERR-CNS-012 | High-risk self-approval prohibition plus `approval_tasks` `no self approval` and reference `false`. S, pp. 11, 85, 90. | ERR-002/040; SCR-005; API-POL-003; DAT-011-F04; BAT-011; BR-CNS-005 | Earlier guard definitions must retain all evidence. Define originator/actor scope without undocumented assigned-task exception. |
| ERR-CNS-013 | Six normal case edges confirmed; closure/reopen remain incomplete. S, pp. 25–26. | ERR-009/010; SCR-002-T01–T08; API-003/017/052; DAT-STATE-001; BR-CNS-001 | Complete only missing guards/edges; no `RESOLVED → CLOSED`, classifier-auto-triage, automatic Reject transition or reopening target invented. |
| ERR-CNS-014 | Tenant lifecycle language differs from workspace paths; routine closed retention, decommission and log purges have different selectors. | ERR-048–051; SF-CON-010; API-CNS-008; DAT-CNS-016; BAT-CNS-012/013; BR-CNS-013/014 | Confirm extent, independent actors/proof and hold precedence. Do not use one actor or a generic CLOSED/force-delete rule. |
| ERR-CNS-015 | Repeated Chapter 22 boilerplate associates deletion event with export/provisioning; C.1 closes verified purge record. | ERR-047/049/051; BAT-CNS-014; BR-CNS-015 | Do not emit `TenantDeletionVerified` for export/provisioning. Their completion transport remains unresolved. |
| ERR-CNS-016 | Source optional BFF and earlier proposed UI/JSON/SSE/reconciliation arrangements are not selected contracts. | ERR-001/007/045; OQ-001/005; API examples; BR proposal register | Keep proposals labeled; do not introduce cookie architecture, event shape, error dialog or automatic reconcile behavior through repetition. |
| ERR-CNS-017 | Internal health/metrics/capacity/GET registers do not imply public exposure or business mutation. | ERR-015/059; API-038–042; API-CNS-011; DAT-LIFE-001; BAT-CNS-018 | Define safe probe/read contracts separately. No invented probe `200`/failure status, job launch or promotion event on GET. |
| ERR-CNS-018 | Diagnostic sample/retention values do not define severity, paging windows, recipients, or mandatory audit sampling. | ERR-LOG-005; ERR-MON; DAT-054; BAT-LOG/MON; BR-043/044 | Specify levels/routing and distinct retention. No owner, schedule or critical-evidence sampling assumed. |
| ERR-CNS-019 | Partial job/held-only/no-work outcomes lack source enums/receipts; atomicity exists only at stated boundaries. | ERR-016/046/049–060; BAT-AC-051–057; DAT-STATE-005 | Complete operation-specific state/receipt/recovery. Do not add `PARTIAL_SUCCESS`, `SKIPPED`, global rollback or automatic compensation as confirmed. |
| ERR-CNS-020 | Evaluation formulas/confidence/missing-case rules, critical `SEC` definitions and canary thresholds absent. | ERR-055–058; DAT-OQ-017/019; BAT-OQ-017/021; BR-CNS-022 | Preserve release blocking and actual evidence while resolving calculations; no invented SEC-to-threat mapping or score rounding. |
| ERR-CNS-021 | Earlier carry-forward sections describe exception handling as later work; it is now the current completed specification. | Carry-forward tables in `01_screen_functions.md`–`05_business_rules.md` | In future controlled updates, reference `06_exception_handling.md` and affected `ERR-` IDs. This document does not rewrite the earlier files or claim remaining stages are complete. |

### Open-Decision Register

All items are **Needs confirmation** and also appear beside affected requirements. No decision, owner, deadline, date, or approval is established.

| Question ID | Required missing contract or decision | Affected identifiers | Earlier dependency links and source |
|---|---|---|---|
| ERR-OQ-001 | Full error taxonomy, simultaneous-failure priority, safe message/details, public/internal/non-HTTP/gRPC mappings, asynchronous fallback per interface, unhandled-runtime and batch exit contracts | ERR-SCP-004, ERR-RES-001–003; ERR-005/015/016 | [02_api.md](02_api.md#api-open-decision-register), API-OQ-017/022; [03_data.md](03_data.md#data-open-decision-register), DAT-OQ-021; BR-OQ-002. S, pp. 54–56, 84. |
| ERR-OQ-002 | Identity claims/algorithms/session expiry/recovery; service audiences; Owner/Member/approver/Admin mapping; originator/self definition; absent/foreign/soft-delete denial details; tenancy incident mechanics | ERR-001–004, ERR-048 | [01_screen_functions.md](01_screen_functions.md#consolidated-open-questions), OQ-001–003; API-OQ-001/002; DAT-OQ-003/004; BR-OQ-001. S, pp. 11, 18, 21–23, 83–86. |
| ERR-OQ-003 | Missing/malformed keys and preconditions; revision/BIGINT encoding; request fingerprint/namespace/concurrent binding; settings conflict; error flag/details | ERR-006–008/011/012 | API-OQ-003/017; DAT-OQ-003/012; BAT-OQ-003/011; BR-OQ-002. S, pp. 25, 54, 84–86. |
| ERR-OQ-004 | Transaction isolation/locking, required audit persistence failure, consumer-ledger atomicity, object/relational crash recovery, checkpoint/dispatch claim/fencing | ERR-004/016/043/046/052 | API-OQ-017; DAT-TXN-004/DAT-OQ-012; [04_batch_functions.md](04_batch_functions.md#batch-open-decision-register), BAT-OQ-004; BR-OQ-002. S, pp. 45, 49, 52, 70. |
| ERR-OQ-005 | UI error placement/copy/focus, unsaved values, explicit revision reconciliation, status projection, hidden/disabled controls and loading/empty distinction | ERR-UI-001; ERR-007/008 and affected screens | OQ-005/026; API-OQ-025; DAT-OQ-021; [05_business_rules.md](05_business_rules.md#open-decision-register), BR-OQ-024. S, pp. 57–59. |
| ERR-OQ-006 | Classifier/correction precedence and catalogs, business invariant missing-input behavior; detailed case edges, closing/reopening actor/target/operation and lineage | ERR-009/010 | OQ-007–010; API-OQ-004/005; DAT-OQ-005; BAT-OQ-006; BR-OQ-003–006. S, pp. 12, 24–26. |
| ERR-OQ-007 | Event/key dedup namespaces/retention/expiry, stale/future/incompatible envelope disposition, signed/canonical schema, claim/ack/replay ledger, original error outcome/lost-response lookup, dry-run/scope/provenance | ERR-011–016/046; ERR-OPS-001 | API-OQ-017/019/022; DAT-OQ-012; BAT-OQ-011/020; BR-OQ-016. S, pp. 17, 25, 48–55, 90. |
| ERR-OQ-008 | Retry attempts/delays/jitter/dependency deadlines/circuit-breaker thresholds/reset; parser/model-specific taxonomy; exhaustion/dead-letter transition | ERR-015/022/030/035; ERR-RTY-001–003 | API-RTY/API-OQ-017; BAT-OQ-005/012; BR-OQ-015. S, pp. 29, 38, 42, 49. |
| ERR-OQ-009 | Connector provider/permissions/capability trust, revoked-credential reauth/resume, partial states/cursor order/outcome stage/batch bounds/fairness/concurrency and safe projection | ERR-017–019/022/035 | OQ-016/022; API-OQ-011; DAT-OQ-006; BAT-OQ-007; BR-OQ-015. S, pp. 27–29. |
| ERR-OQ-010 | File/MIME/subtype/count/MB/archive/parser/scanner limits and errors; quality/OCR/empty source/status/quarantine release/viewing; immutable identity/anchors; signed source delivery/expiry recovery | ERR-020–023/026 | OQ-015/018; API-OQ-007/008; DAT-OQ-007/008/010; BAT-OQ-008; BR-OQ-007/008. S, pp. 30–32, 52, 57, 90. |
| ERR-OQ-011 | Index partial readiness/rebuild completeness/recall/coverage, reconciliation exhaustion/scope, source/anchor failures, support thresholds/clarification, invalidation barrier and ACL/rebuild races | ERR-024–027/044 | API-OQ-008; DAT-OQ-009/020; BAT-OQ-009/010; BR-OQ-008/016. S, pp. 28, 34–36, 49, 53, 78–79, 90. |
| ERR-OQ-012 | Model/prompt/tool/A2A schemas and grants; route/fallback; plan/call/retry counting; runtime/review wait/stop/deadline; policy version/table; material provenance/unknown class and four-control mapping | ERR-028–033/036–038/043 | OQ-011/020/022; API-OQ-006/009/023/026; DAT-OQ-011/016/022; BAT-OQ-012/024; BR-OQ-009/010/012. S, pp. 12, 37–46, 49, 62, 87, 90. |
| ERR-OQ-013 | Token reservations/actual use/release/overruns/quota reset; admission thresholds/units/provider capacity; `Retry-After` calculation and terminal quota mapping | ERR-034/035 | API-OQ-006/009/018; DAT-OQ-014/020; BAT-OQ-012; BR-OQ-011. S, pp. 38, 69. |
| ERR-OQ-014 | Review required fields/rationale/decision literals/hash; stale/expiry response, task states/assignment/quorum/SLA/timezone/race; source-inspection prerequisite; override scope/role/reason; atomic gate lookup | ERR-039–043 | OQ-012–014; API-OQ-010; DAT-OQ-013; BAT-OQ-013; BR-OQ-013/014. S, pp. 45–46, 57–58, 82–85. |
| ERR-OQ-015 | Pagination/SSE cursor syntax/lifetime/invalid/expired handling, retained-backfill failure, reconnect/stream error payload, heartbeat and scoped refresh UX | ERR-045 | OQ-006/011/019; API-OQ-006/012; DAT-OQ-012/021; BR-OQ-024. S, pp. 54–55, 58. |
| ERR-OQ-016 | Worker heartbeat/lease/fencing/takeover/drain; partial provisioning compensation/resume; historic batch windows/receipts/coverage and no-queue readiness | ERR-046/047 | API-OQ-016/018; DAT-OQ-018/020; BAT-OQ-004/018; BR-OQ-019/022. S, pp. 70, 78. |
| ERR-OQ-017 | Tenant/workspace lifecycle extent and independent proof/actors/expiry; export format/checksum/download/partial recovery; holds/shared/backup inventory; partial/held-only purge verification and receipts | ERR-048–051 | OQ-023; API-OQ-015/016/021; DAT-OQ-018; BAT-OQ-014/019; BR-OQ-017/018. S, pp. 26, 78–83, 87–89. |
| ERR-OQ-018 | Security/outage incident routing, named recipients/channels/escalation; failure/availability budgets, thresholds/detection/re-enable; degraded mode controls, past ACL/classification/secret incident remediation | ERR-036/037/044/053/059; ERR-MON | API-OQ-018/025; DAT-OQ-014/020; BAT-OQ-025; BR-OQ-021/022. S, pp. 64–70, 79, 90. |
| ERR-OQ-019 | Safe log schema/levels/sanitizer/stack traces/PII and signed-URL redaction; diagnostic/audit/class retention; audit chain/archive failure/checkpoint; vault/rotation/old-key recovery | ERR-050/052/053; ERR-LOG | API-OQ-012/021; DAT-OQ-014–016; BAT-OQ-015/023/025; BR-OQ-017/021. S, pp. 21, 52, 62–66, 84, 90. |
| ERR-OQ-020 | Usage ledger identity/correction, day/timezone/formulas/units/currency/rounding, late/partial/zero-use rollup state, rerun/finalization | ERR-054 | API-OQ-013; DAT-OQ-014; BAT-OQ-016; BR-OQ-020. S, pp. 38, 65, 85. |
| ERR-OQ-021 | Evaluation integrity/error/result schema, missing/partial/empty case handling, statistical formulas/confidence/rounding, resume/new evaluation and individual critical `SEC` definitions | ERR-055/056/060 | API-OQ-013; DAT-OQ-017/019; BAT-OQ-017; BR-OQ-023. S, pp. 74–76, 88–89. |
| ERR-OQ-022 | Governance/migration/build/sign-off failure schemas, impact/revision, backfill checkpoint/bounds, canary threshold/duration/stage graph and explicitly supported compensation | ERR-057/058 | API-OQ-020/022; DAT-OQ-019; BAT-OQ-021; BR-OQ-023. S, pp. 8–10, 20, 52, 55, 71–73. |
| ERR-OQ-023 | Region/object/persistence recovery inventory/order/roles/commands/verification/exercise frequency; health/live/ready statuses/checks/authentication/exposure | ERR-015/059 | API-OQ-018/021; DAT-OQ-020; BAT-OQ-023; BR-OQ-022. S, pp. 18–20, 69–70. |
| ERR-OQ-024 | Per-job empty/ineligible/duplicate-only/held-only receipts and states, cursor/watermark advancement, no-op accounting/archive/package behavior | ERR-060 and applicable families | BAT-OQ-003 and BAT-AC-051–057; DAT-STATE-005; BR-OQ-018/020/023. S, p. 89, E.1; affected domain sections. |
| ERR-OQ-025 | Optional webhook method/recipient management, payload/signature/canonical bytes/key/age, acknowledgment/retry/dead letters/manual replay; browser notification channels/recipients/read state | ERR-RTY webhook row; ERR-MON; BAT-024 | API-OQ-024/025; DAT-OQ-022; BAT-OQ-022/025; OQ-025; BR-OQ-024. S, pp. 55, 58–59. |

### Dependencies and Carry-Forward

| Specification | Required dependency |
|---|---|
| [01_screen_functions.md](01_screen_functions.md) | Preserve screen/action/state IDs, truthful accessible displays and unresolved UI arrangements. Link failure displays to `ERR-UI-001` and affected exceptions through controlled amendments. |
| [02_api.md](02_api.md) | Preserve API IDs, literal methods/paths/statuses/codes, protocol boundaries and record-versus-wire distinctions. Unknown error mappings remain blocking contracts; internal endpoints are not new browser controls. |
| [03_data.md](03_data.md) | Preserve tenant predicates, authoritative/source/derivative separation, immutable versions/revisions/decisions, exact artifact binding, outbox/checkpoints, receipts and legal holds. Recovery cannot rewrite accepted historical evidence. |
| [04_batch_functions.md](04_batch_functions.md) | Preserve source triggers, bounded retries, partial batch continuation, cursor/checkpoint safety, logical grouping and unresolved schedules. Exception handling does not add a scheduler, executable, lock, or no-work enum. |
| [05_business_rules.md](05_business_rules.md) | Preserve all cumulative guards, six case edges, four-control classification, no-self-approval, review/publication separation, lifecycle approvals/holds and release blockers. Errors do not waive business rules. |
| Remaining specifications | **To be defined in a later stage.** Resolve processing/security/architecture details identified above without assuming the name or contents of an unprovided Stage 7 document. |
| Stage 8 | `08_architecture_decision.md` is **To be defined in a later stage**. Consolidate only completed Markdown specifications, linking `06_exception_handling.md`, `ERR-OQ-001`–`ERR-OQ-025`, affected `ERR-` IDs, and the preceding filenames/IDs. Do not presume a decision, owner, deadline, approval or selected implementation. |

**Implementation boundary:** Implement and test every Confirmed failure-handling obligation. Unspecified HTTP/business/protocol codes, safe schemas, retry counts, thresholds, state guards, hashes, concurrency controls, notification recipients, retention calculations, schedules and recovery choices remain explicit blocking decisions. A reference value, illustrative screen, repeated Proposal or generic exception category does not authorize silently completing the missing contract.
