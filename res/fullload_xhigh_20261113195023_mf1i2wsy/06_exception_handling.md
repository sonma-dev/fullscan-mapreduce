# 6. Exception Handling Specification

## Exception Inventory and Classification

### Specification Basis and Status

| Item | Definition |
|---|---|
| Specification file | `06_exception_handling.md` |
| Source document | `1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Source baseline | `OD-AI-DDS-001`, release `R1.0`, design revision `1.3` |
| Completed preceding specifications | [`01_screen_functions.md`](01_screen_functions.md), [`02_api.md`](02_api.md), [`03_data.md`](03_data.md), [`04_batch_functions.md`](04_batch_functions.md), [`05_business_rules.md`](05_business_rules.md) |
| Scope | Source-supported request rejection, business and permission exceptions, integration failures, asynchronous partial processing, duplicate execution, timeout, recovery, and operational failure evidence. |
| Identifier convention | `ERR-001`–`ERR-054` identify exception or exceptional-result contracts. `ERR-COM-xxx`, `ERR-OPS-xxx`, `AC-ERR-xxx`, `CON-ERR-xxx`, and `OQ-ERR-xxx` identify shared requirements, operational procedures, acceptance criteria, conflicts, and unresolved decisions. |
| Identifier interpretation | Assigned `ERR` identifiers are specification references, **not new wire error codes**. Existing source literals, events, threat IDs, test IDs, and preceding requirement identifiers remain unchanged. |
| Citation convention | `[DDS]` identifies the source filename above. Citations use original PDF page numbers and sections. |
| Source character | Fictional normative reference design. Numeric values are design assumptions, not measured production results. |

[DDS]: 1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf

Statuses used throughout:

- **Confirmed:** Explicitly supported behavior, condition, constraint, literal, or contract.
- **Needs confirmation:** Missing or conflicting implementation contract. An unresolved value must not be selected silently.
- **Proposal:** Unapproved design suggestion. Earlier proposals retain their earlier status.
- **NC:** Table abbreviation for **Needs confirmation**.

**ERR-COM-001 — Interpretation and implementation boundary.**

1. Preserve existing source error literals exactly. Do not replace them with assigned `ERR` identifiers.
2. A confirmed failure condition does not establish a complete HTTP, RPC, event, database, or screen contract.
3. Do not infer a new endpoint, status, error code, state, retry count, schedule, notification channel, or remediation control.
4. A rejected business mutation may still produce authorized denial or diagnostic evidence. “Business state unchanged” does not mean all audit recording is prohibited.
5. Expected duplicate results, degraded retrieval, low-quality extraction, expiry, and legal-hold exceptions must remain distinguishable from internal defects.
6. Do not classify an unresolved implementation choice as permission to continue, retry, publish, or purge.

**Sources:** [DDS], pp. 1–2; p. 13, §2.3.2; pp. 48–56; pp. 82–84; p. 90, Appendix F.  
**Earlier trace:** `SCR-COM-001/010/011`, `API-COM-001/007`, `DAT-COM-001`, `BAT-COM-001`, BR-006.

### Classification Model

The following categories organize this specification. They are not confirmed wire enums or database columns.

| Category | Interpretation |
|---|---|
| Invalid input | Request, file, tool argument, or envelope fails its applicable validation contract. |
| Business-rule violation | State, revision, quota, evidence, policy, approval, retention, or lifecycle guard is unsatisfied. |
| Permission violation | Authentication, tenancy, resource ACL, role, service scope, or separation of duties is unsatisfied. |
| External failure | Repository, model provider, object service, identity provider, or other dependency cannot complete the requested operation. |
| Internal failure | Transaction, workflow, index, messaging, integrity, worker, or deployment processing fails. |
| Expected exceptional result | Replay, insufficient evidence, reduced quality, expiry, or protected-record outcome that requires explicit handling but is not necessarily a defect. |
| Contract gap | The underlying function is supported, but its specific failure detection, state, or recovery contract is absent. |

**Confirmed retry distinction:** Validation and permission failures are permanent and are not retried as transient failures. Transient dependency failures use bounded exponential backoff, randomized jitter, and per-dependency circuit breakers. Exact bounds and thresholds are NC.  
**Source:** [DDS], p. 49, §13.3.1.

### Exception Inventory: Requests, Identity, and Execution Consistency

Mappings below refer to the completed filenames listed in the specification basis. Screen placement remains proposed or unresolved wherever the preceding screen specification says so.

| Exception ID / source terminology | Occurrence and detection condition | Category and affected scope | Cross-layer mapping | Status and source |
|---|---|---|---|---|
| ERR-001 — `CASE_VERSION_CONFLICT` | Case mutation submits a revision that no longer matches current case revision. | Business-rule violation; targeted case update. | SCR-002-A03; API-004; DAT-003/004/026; applicable case-writing workers; BR-007. | **Confirmed.** [DDS], p. 25, §6.2.2; pp. 83–84. |
| ERR-002 — `IDEMPOTENCY_CONFLICT` | Previously used operation key is submitted with a different request fingerprint. | Business-rule violation; conflicting submission. | `SCR-COM-010`; API-001 and job-creating POSTs; DAT-026; `BAT-OPS-004`; BR-008. | **Confirmed.** [DDS], p. 54, §15.1.2; p. 89, `TST-002`. |
| ERR-003 — `CONNECTOR_REAUTH_REQUIRED` | Queued connector work uses revoked credentials. | Permission/external failure; affected connector jobs. | SCR-006-F05/A03; API-018/019/049; DAT-015/019/021; BAT-002; BR-034. | **Confirmed.** [DDS], p. 27, §7.1.2. |
| ERR-004 — `NO_SUPPORTED_EVIDENCE` | Retrieval confidence or evidence quality is insufficient. | Expected exceptional result; retrieval and dependent recommendation. | SCR-003-A02, SCR-002 draft/gate; API-009/045 and run retrieval; DAT-010/023; BAT-007; BR-019. | **Confirmed.** [DDS], p. 36, §9.3.2. |
| ERR-005 — `MODEL_OUTPUT_INVALID` | Model result contains unknown fields, invalid citations, or control-character injection under the versioned output contract. | Invalid output/external failure; generation and publication. | SCR-004-F08, SCR-002 candidate; API-036/050; DAT-008/009/024/025; BAT-007/008; BR-023. | **Confirmed.** [DDS], p. 38, §10.2.2; p. 89, `TST-005`. |
| ERR-006 — Schema-invalid request or arguments | Public payload, internal payload, required review data, or typed tool arguments fail the applicable schema. Missing-header behavior is not fully specified. | Invalid input; requested operation before allocation, transaction, or dispatch. | Shared screen validation; applicable API-001–050; resolved DAT schemas; `BAT-OPS-001`; BR-006/027/030. | **Confirmed validation and public `422`; detailed schemas NC.** [DDS], pp. 54, 56, §§15.1.1 and 15.3.2. |
| ERR-007 — Invalid authentication or service context | Unexpected token algorithm, missing tenancy claim, invalid required identity claims, or unsatisfied service audience/scope. | Permission violation; boundary access. | `SCR-X-001`; API authentication profiles/API-027/048; DAT-019; all authenticated BAT boundaries; BR-002. | **Confirmed rejection controls; exact mappings NC.** [DDS], pp. 18, 21–22. |
| ERR-008 — Resource/action authorization denial | Applicable role, membership, sensitivity, ACL, requested action, or segregation predicate fails. | Permission violation; requested resource/action. | `SCR-COM-002`; resource APIs; DAT-019 and affected resources; `BAT-OPS-001`; BR-003. | **Confirmed.** [DDS], pp. 22–23, §5.2; p. 87, `AccessDenied`. |
| ERR-009 — Foreign-tenant or absent resource | Resource ID is absent or belongs to another tenant. | Permission/non-disclosing result; resource read or mutation. | `SCR-COM-003`; resource APIs; tenant-qualified DAT references; scoped BAT access; BR-004. | **Confirmed same not-found class.** [DDS], p. 23, §5.3.2; p. 89, `TST-003`. |
| ERR-010 — Invalid case transition or business change | Unsupported transition, unauthorized overwrite of closed lineage, missing correction reason, or invalid resolved business input. | Business-rule/invalid-input violation; case or correction. | SCR-002-A03/A04/A09–A11; API-004/005/API-GAP-001/005; DAT-003/004/020/025; BAT-001 and applicable consumers; BR-011–015/033. | **Confirmed guards; complete trigger/error contracts NC.** [DDS], pp. 12, 25–26, 46, 82, 86. |
| ERR-011 — Stale or invalid workspace configuration | Configuration revision precondition fails or proposed configuration violates approved policy. Missing configuration/effective-version treatment is unresolved. | Business-rule violation/contract gap; workspace settings and dependent work. | SCR-007-A02; API-GAP-002; DAT-002/017/032; affected BAT functions; BR-007/010. | **Confirmed stale/unauthorized rejection; detailed validation NC.** [DDS], p. 24, §6.1.1; pp. 71–73. |
| ERR-012 — Identical request replay | Same actor, operation key, and fingerprint repeats an accepted request. | Expected exceptional result; submission/result reconstruction. | `SCR-COM-010`; API-001 and long-running POSTs; DAT-026; `BAT-OPS-004`; BR-008. | **Confirmed.** [DDS], pp. 25, 54; p. 89, `TST-001`. |
| ERR-013 — Duplicate accepted event or step delivery | Event ledger identifies an already accepted event/operation; delivery follows network retry or replay. | Expected exceptional result; consumer mutation. | SCR-004 progress indirectly; API events/API-037/038; DAT-014/026; BAT-010/012 and consumers; BR-009. | **Confirmed.** [DDS], pp. 17, 48–50; p. 89, `TST-007`. |
| ERR-014 — Delayed/stale or invalid event envelope | Aggregate revision is stale, required envelope content fails validation, or trusted signed scope is invalid. | Internal/invalid-input/permission condition; message consumer. | API-COM-006; DAT-EVT fields/DAT-014/026/034; BAT-010/012; BR-002/006/009. | **Confirmed validation, deduplication, and stale detection; disposition NC.** [DDS], pp. 22, 48–50, 56. |

### Exception Inventory: Integrations, Ingestion, and AI Processing

| Exception ID / source terminology | Occurrence and detection condition | Category and affected scope | Cross-layer mapping | Status and source |
|---|---|---|---|---|
| ERR-015 — Dependency unavailable or request outcome unresolved | Dependency cannot complete work, or response is lost after an operation may have committed. | External/internal failure; boundary-specific scope. | `SCR-COM-010/011`; applicable API-001–050; affected DAT records; applicable BAT functions; BR-006/008/009/036. | **Confirmed no ambiguous success and replay safety; transport-loss resolution details NC.** [DDS], pp. 8–80, interface-boundary requirements; pp. 25, 49, 54. |
| ERR-016 — Provider throttling / `429` burst | Repository/model provider throttles calls or returns a `Retry-After` instruction. | External failure; affected dependency and admitted workload. | SCR-006/SCR-004 safe outcomes; API-049/050; DAT-015/016/026/036; BAT-002/007; BR-036. | **Confirmed.** [DDS], pp. 28, 49, 70; p. 89, `TST-008`. |
| ERR-017 — New-run admission throttled | Workspace tokens, queue age, or provider capacity fails configured admission thresholds. | Business-rule/capacity violation; new AI-run request. | SCR-002-A07; API-011/012; DAT-002/008/026/036; BAT-007; BR-024. | **Confirmed.** [DDS], p. 69, §19.2.1. |
| ERR-018 — Current-run quota exhaustion | Current run exhausts workspace token quota. | Business-rule violation; current run. | SCR-004-F07/F08; API-036/050 and run state; DAT-008/016/024; BAT-007/016; BR-025. | **Confirmed terminal current-run outcome.** [DDS], p. 38, §10.3.1. |
| ERR-019 — Unsupported connector capability | Connector does not support an advertised contract category: list, fetch, delta cursor, ACL, or delete. | Expected warning/business restriction; connector ingestion trust. | SCR-006-F02/F03; API-018/019/049; DAT-021; BAT-002/006; BR-034. | **Confirmed lower-trust mode and warning; restrictions NC.** [DDS], p. 27, §7.1.1. |
| ERR-020 — Poison connector record | Malformed document persists after bounded retries. | Invalid input; individual source record. | SCR-006-F09–F12; API-019/049; DAT-015/021/022; BAT-002/003; BR-035. | **Confirmed.** [DDS], p. 29, §7.3.2. |
| ERR-021 — Partial connector batch | Some items have durable outcomes while preceding or remaining items fail or await processing. | Partial external/internal failure; sync run and cursor. | SCR-006-F06–F09; API-018/019/049; DAT-015/021; BAT-002; BR-035. | **Confirmed durable-outcome/cursor rule.** [DDS], p. 28, §7.2.1; p. 29, §7.3.2. |
| ERR-022 — File admission failure | Unsupported file category, MIME/extension disagreement, configured size violation, or decompression threshold violation. | Invalid input/safety violation; uploaded/source file. | SCR-002-A05; API-006; DAT-022/028; BAT-003; BR-016. | **Confirmed fail-closed controls; detailed boundaries NC.** [DDS], pp. 13, 30, §8.1.1. |
| ERR-023 — Unsafe attachment | Malware/unsafe active content, polyglot PDF, or unsafe payload fails scan/sandbox/parser controls. | Invalid input/security condition; file and derivatives. | SCR-002-F20/A05; API-006/007; DAT-005/006/022/028; BAT-003/004; BR-016. | **Confirmed quarantine/no indexing.** [DDS], p. 30, §8.1.2; pp. 88–89, `T-04/TST-015`. |
| ERR-024 — Low-quality extraction | Quality evaluation identifies low-quality text/layout using source-described flags. | Expected exceptional result; evidence-use eligibility. | SCR-002-F21/SCR-003-F12; API-007 and evidence consumers; DAT-022; BAT-003/007; BR-018. | **Confirmed viewing/use distinction; thresholds NC.** [DDS], p. 32, §8.3.2. |
| ERR-025 — Invalid/unresolvable citation or unavailable cited source | Citation cannot resolve to stored version/anchor, current permission fails, or source access cannot complete. | Evidence/permission/external condition; citation and dependent gate. | `SCR-COM-006`; SCR-003-A03/SCR-005-A03; API-008/010/039/API-GAP-003; DAT-006/007/010/028; BAT-007/008; BR-017/019. | **Confirmed valid-anchor/current-access requirements; source-access errors NC.** [DDS], pp. 31, 35, 52, 57. |
| ERR-026 — Prompt injection or evidence instruction smuggling | Retrieved/model content attempts to introduce instructions, tool directives, tenant changes, approvals, or unrestricted destinations. | Invalid input/security condition; prompt, plan, tool, and publication boundaries. | `SCR-COM-012`; API-036/045/046; DAT-024/025; BAT-007; BR-005/023. | **Confirmed fail-closed authority controls and recorded indicators.** [DDS], pp. 7, 13, 38–39, 61; p. 88, `T-02`. |
| ERR-027 — Unauthorized tool action or A2A decline | Capability lacks separate authorization, arguments are forged/invalid, consequential write lacks required human authorization, or receiving agent declines. | Permission/invalid-input/expected decline; invocation. | `SCR-COM-012`; API-045/046; DAT-019/024/026/034; BAT-007; BR-027. | **Confirmed denial/decline constraints; protocol NC.** [DDS], pp. 41–42, 87; p. 89, `TST-014`. |
| ERR-028 — Invalid/unbounded plan or exhausted call budget | Plan violates DAG/dependency/depth requirements, exceeds tool-call budget, or repeatedly remains invalid. | Business-rule/internal failure; run execution. | SCR-004-F08/A04; API-011–014/037; DAT-008/009/026; BAT-007; BR-026. | **Confirmed limits and stop conditions; accounting NC.** [DDS], pp. 40–42; p. 88, `T-10`. |
| ERR-029 — Deadline/runtime timeout | Execution reaches its applicable deadline or configured maximum runtime. | Business-rule/external/internal condition; run/task execution. | SCR-004; API-011–015/036/046; DAT-008/009/034; BAT-007; BR-026. | **Confirmed terminal-or-recoverable requirement; representation NC.** [DDS], p. 12, §2.3.1; p. 41, §11.3.1; p. 90. |
| ERR-030 — Policy denial, more evidence, or missing approval | Deterministic outcome denies execution or requests more evidence; required approval is absent. | Business-rule/expected controlled result; action and publication. | SCR-002 gate/SCR-004/SCR-005; API-017 and run processing; DAT-011/017/025; BAT-007/008; BR-028/032. | **Confirmed outcomes and restrictions; waiting distinction NC.** [DDS], pp. 11–13, 41, 44–46, 49. |

### Exception Inventory: Review, Persistence, Lifecycle, and Operations

| Exception ID / source terminology | Occurrence and detection condition | Category and affected scope | Cross-layer mapping | Status and source |
|---|---|---|---|---|
| ERR-031 — Stale approval artifact | Submitted reviewed hash differs from changed/current candidate artifact. | Business-rule violation; decision and publication. | SCR-005-A04/A05; API-017; DAT-011/012/025; BAT-008; BR-030/032. | **Confirmed rejection/audit and `409` surface.** [DDS], pp. 45–46, 83; p. 89, `TST-006`. |
| ERR-032 — Ineligible/self-review or incomplete override authorization | Reviewer fails pool/minimum role/SoD; high-risk author self-approves; override lacks elevated role, secondary reviewer, or audited reason. | Permission/business-rule violation; review/override. | SCR-005-A04/A07; API-017/API-GAP-006; DAT-011/012/019/025; BAT-007/008/009; BR-029/033. | **Confirmed restrictions; role/scope details NC.** [DDS], pp. 11, 45–46, 85, 90. |
| ERR-033 — Expired review task | Task reaches configured SLA; decision may arrive after expiry/reassignment. | Expected expiry/business-rule condition; task and routing. | SCR-005-F06/A06; API-016/017; DAT-011/012; BAT-009; BR-031. | **Confirmed no implicit approval/escalation; late/race rules NC.** [DDS], p. 45, §12.2.1; p. 89, `TST-010`. |
| ERR-034 — Incomplete review fields or unavailable review context | Required fields incomplete or exact candidate/citations/model/prompt/policy context cannot be obtained. | Invalid input/external/internal condition; review interaction. | SCR-005 procedure/A02–A05; API-016/017/API-GAP-004; DAT-011/012/025/035; BAT-008; BR-030/045. | **Confirmed completeness and inspectability requirements; outage behavior NC.** [DDS], pp. 57–58. |
| ERR-035 — Publication revalidation failure | Authorization/evidence changes after retrieval, required gate remains unsatisfied, or replay targets different content. | Permission/business-rule violation; final artifact publication. | SCR-002-A12; API-017 publication consumer; DAT-003/010/011/012/017/025; BAT-008; BR-032. | **Confirmed.** [DDS], pp. 13, 45–46, 52. |
| ERR-036 — Stale unauthorized visibility / suspected ACL leak | Revoked/deleted evidence remains available, or affected alias/cache may disclose forbidden content. | Security/internal failure; affected retrieval scope. | SCR-003-A04/SCR-006-A04; API-009/010; DAT-005/019/023/027/029; BAT-006/012; BR-021/044. | **Confirmed security incident/runbook.** [DDS], pp. 27–29, 53, 79; p. 89, `TST-004`. |
| ERR-037 — Failed/delayed indexing or broken message link | Index write fails, source/index fingerprints diverge, backlog ages, or durable message linkage breaks. | Internal/external partial failure; derivative and workflow continuation. | SCR-006/SCR-004 status; API-037/038; DAT-005–007/014/023/026; BAT-004/011/012; BR-009/020/044. | **Confirmed reconciliation/runbook.** [DDS], p. 49, §13.2.2; p. 90, §F.1. |
| ERR-038 — Rebuild completeness/recall gate unsatisfied | Replacement generation has not passed required checks. | Business-rule/internal condition; read-alias replacement. | SCR-006 readiness where bound; API search consumers; DAT-023; BAT-005; BR-020. | **Confirmed alias-switch guard; thresholds NC.** [DDS], p. 34, §9.1.2. |
| ERR-039 — Object/source access failure | Object provider access fails, referenced object cannot be obtained, or signed access is invalid/expired. | External/permission/contract gap; source viewer or worker. | SCR-003/SCR-005; API-039/API-GAP-003; DAT-006/028; BAT-003/007/023; BR-017/037/047. | **Confirmed controlled access and fault-injection coverage; exact failure mapping NC.** [DDS], pp. 52, 70. |
| ERR-040 — Transaction, integrity, or commit-outcome failure | Case/approval/outbox or gate/pointer transaction fails; FK/unique/state constraint fails; commit reply is lost. | Internal/invalid-input/permission condition; transaction unit. | SCR-002/005/007; API-001/004/005/017 and settings; DAT-003/004/012/014/025/026; applicable BAT mutations; BR-004/007–009/032. | **Confirmed atomicity/constraints; failure-specific mappings NC.** [DDS], pp. 45, 52, 85–86. |
| ERR-041 — Lost worker heartbeat | Fault injection or runtime observation identifies lost worker activity. | Internal failure; in-flight step or worker scope. | SCR-004 authoritative progress; API-037; DAT-008/009/026/036; affected worker BAT functions; BR-009/026/047. | **Confirmed test scenario; detection/ownership protocol NC.** [DDS], p. 70, §19.3.2. |
| ERR-042 — SSE disconnection or cursor/history failure | Stream disconnects, resume cursor cannot be used, retained history has a gap, or caller scope/session changes. | External/permission/contract gap; progress delivery, not necessarily execution. | SCR-004-A03; API-013/015; DAT-034/035; BAT-007 progress; BR-045. | **Confirmed scoped resume/server reconstruction; gap/expiry behavior NC.** [DDS], pp. 55, 58. |
| ERR-043 — Optional webhook delivery failure | Outbound recipient cannot accept/verify delivery or invocation fails. | External/permission condition; notification delivery. | `SCR-X-007`; API-047; DAT-034; BAT-025; BR-009/036. | **Confirmed retry/no case rollback; acknowledgments NC.** [DDS], p. 55, §15.2.2. |
| ERR-044 — Ineligible purge or legal-hold exception | Case-retention target is not eligible/closed, or inventoried record is protected by hold. | Business-rule/expected protected outcome; destructive scope. | `SCR-X-004/X-005`; API-026/029/040; DAT-018/025/029/030; BAT-013/014/021; BR-038/041. | **Confirmed protection and receipts.** [DDS], pp. 26, 66, 80, 89. |
| ERR-045 — Missing independent export/delete approvals | Single Admin or otherwise insufficient independent checks attempts controlled exit. | Permission/business-rule violation; export/deletion admission. | `SCR-X-003/X-004`; API-025/026; DAT-019/029; BAT-020/021; BR-039. | **Confirmed two-person control.** [DDS], pp. 78, 83, 88, `T-11`. |
| ERR-046 — Partial export/deletion or failed verification | Accepted exit work has incomplete packaging/removal/receipts or cannot verify completion. | External/internal partial failure; manifest and inventory. | `SCR-X-003/X-004`; API-025/026/040; DAT-018/028/029; BAT-020/021; BR-040/041. | **Confirmed truthful durable outcome constraints; partial-state/compensation contract NC.** [DDS], pp. 78–80. |
| ERR-047 — Incomplete provisioning/backfill readiness | Required provisioning resources are incomplete or indexed coverage does not establish readiness. | Internal/expected incomplete condition; workspace onboarding and sync admission. | SCR-006-F13/`SCR-X-002`; API-GAP-008/API-018; DAT-001/002/019/023/029; BAT-018/019; BR-042. | **Confirmed sync block/readiness rule; detailed failures NC.** [DDS], p. 78, §22.1. |
| ERR-048 — Historical audit edit or audit-integrity/export failure | Caller attempts historical mutation; hash-chain/export verification fails or cannot complete. | Permission/internal/contract gap; immutable evidence. | SCR-008-A04; API-021; DAT-004/012/013; BAT-015; BR-037. | **Confirmed immutability; integrity/export failure procedure NC.** [DDS], p. 62, §17.3.1; p. 88, `T-09`. |
| ERR-049 — Sensitive-value disclosure or rotation failure | Error/trace/provider/export boundary attempts out-of-scope disclosure; vault/rotation mechanism fails. | Permission/security/external/contract gap; secret/data boundary. | `SCR-COM-011`; API-036/047/049/050 and shared responses; DAT-019/024/028/030/032; BAT-024; BR-037. | **Confirmed disclosure prohibitions/rotation requirements; post-disclosure and rotation-failure recovery NC.** [DDS], pp. 21, 27, 61–66, 79, 84. |
| ERR-050 — Invalid evaluation evidence or blocking quality result | Fixture replacement/signature failure, incomplete suite, critical test failure, insufficient statistical confidence, or quality target failure. | Internal/business-rule/expected blocking result; evaluation and release. | SCR-011; API-023/024/043; DAT-031/032; BAT-017/026; BR-049. | **Confirmed safety/fixture/confidence gates; partial/empty-suite contracts NC.** [DDS], pp. 74–76, 88–89. |
| ERR-051 — Release/migration incompatibility or canary regression | Active-reader compatibility, build verification, sign-off, or canary criteria is unsatisfied. | Internal/business-rule condition; rollout and data migration. | `SCR-X-009`; API-031/043/044; DAT-032; BAT-022/026; BR-048. | **Confirmed gates/traffic rollback; thresholds and specific migration recovery NC.** [DDS], pp. 20, 52, 55, 72–73. |
| ERR-052 — Primary-region outage or failed recovery | Primary region fails or restore cannot satisfy consistency/RPO/RTO. | External/internal failure; regional service and persistence. | No recovery screen confirmed; API-034/035/042 operational context; DAT-028/036; BAT-023/005; BR-047. | **Confirmed incident-controlled recovery/test coverage; protocol NC.** [DDS], pp. 19, 69–70, 89. |
| ERR-053 — Incomplete/uncertain usage reporting | Usage, reservations, late provider results, or daily rollup cannot produce a complete attributable result. | Contract gap/internal/external condition; reporting window. | SCR-010; API-022; DAT-016/030; BAT-016; BR-025/043. | **Confirmed accounting function; failure-state/correction contract NC.** [DDS], pp. 38, 65, 85. |
| ERR-054 — Other unspecified screen/internal failure | Undescribed failure in summaries, calendar calculation, UI projection, health, governance, or another supported component. | Contract gap; affected operation only, pending scope definition. | SCR-009/shared summaries and other affected screens; relevant APIs/DAT/BAT; BR-006/010/013/045/046/050. | **Needs confirmation.** Underlying functions are described in [DDS], pp. 8–10, 25, 57–59, 64–70; specific failure conditions are absent. |

## Handling by Exception

### Shared Failure Response and Processing Requirements

**ERR-COM-002 — Authoritative rejection and durable failure handling.**

1. Establish authenticated scope and validate input before allocating long-running work, entering a mutation transaction, or dispatching tools.
2. Apply applicable revision, resource, policy, evidence, quota, and separation-of-duty checks.
3. Reevaluate resource authorization within state-changing transactions.
4. Reject stale or unauthorized actions without accepted business-state change.
5. Preserve already committed authoritative work when a downstream asynchronous derivative fails.
6. For dependency unavailability, return a documented retryable error or an actual persisted asynchronous operation identity. Never fabricate an accepted operation or completion.
7. Record the exact failed run checkpoint where the source requires it.
8. Apply event/operation deduplication during retries and recovery.
9. Do not replace a denied action with an equivalent tool, a weaker deployment, or an unapproved region.
10. Reset tenant-scoped database session variables after every transaction, including exception paths, before pooled reuse.

**Sources:** [DDS], pp. 13, 22, 25, 37–42, 45, 48–56, 86.  
**Earlier trace:** `API-PROC-001/018/019`, `DAT-LC-013/015/016`, `BAT-OPS-001`–`006`, BR-003–009.

**Needs confirmation — OQ-ERR-004/OQ-ERR-015:** Transaction isolation, rollback implementation, commit-outcome reconstruction, audit participation, and database connection handling if context reset itself fails. The requirement to reset context is confirmed; connection disposal/recovery mechanics are not selected.

### Canonical Error Envelope

The source confirms this canonical example, including the example’s value kinds:

| Field | Meaning and type evidence | Requiredness and constraints |
|---|---|---|
| `error` | JSON object containing error information. | Canonical shape confirmed; universal applicability to every REST/RPC/async failure NC. |
| `error.code` | JSON string; stable failure literal. | Exact known literals retained. Complete code inventory and mandatory schema NC. |
| `error.message` | JSON string; safe explanation. | Exact case-conflict message below confirmed. Other messages and localization NC. |
| `error.correlation_id` | JSON string; support correlation. | Present in example; format, length, universal requiredness, and screen display NC. |
| `error.retryable` | JSON Boolean. | Case conflict is `false`; permanent validation/permission classification confirmed. Full per-code mapping NC. |
| `error.details` | Safe structured object in example. | May contain safe validation details. Per-error schemas and mandatory properties NC. |
| `expected_revision`, `actual_revision` | JSON numbers in example details. | Case conflict must expose current revision within authorized scope; full numeric wire representation NC. |

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

**Source:** [DDS], p. 84, §A.3.

**ERR-COM-003 — Safe response content.** Error bodies must not contain connector credentials, full prompts, retrieved documents, or unauthorized resource existence. Public responses must not expose secrets or raw provider credentials. Diagnostic/provider payloads must obey their separate scopes; a public error must not relay an unfiltered provider response.

**Sources:** [DDS], p. 13, §2.3.2; p. 54, Chapter 15 invariant; pp. 61–64; p. 84, §A.3.

**Needs confirmation — OQ-ERR-001:** Resolve the source’s “snake-case” wording versus uppercase examples. Preserve `CASE_VERSION_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `CONNECTOR_REAUTH_REQUIRED`, `NO_SUPPORTED_EVIDENCE`, and `MODEL_OUTPUT_INVALID` pending resolution. No additional literal is defined here.

### HTTP, Async, and Screen Distinctions

**ERR-COM-004 — A response status describes the request, not necessarily the workflow outcome.**

| Boundary/result | Confirmed interpretation |
|---|---|
| `201` case creation | Authoritative case creation outcome, not classification completion. |
| `202` ingestion, run, sync, evaluation, export, or deletion | Durable work accepted; not completed, ready, approved, or published. |
| Successful read of run/document/connector status | The read can succeed while the returned workflow has a failure or exceptional outcome. Complete result schemas remain NC. |
| `409` case conflict | Failed conflicting update, not a successful save. |
| `409` changed reviewed-artifact conflict | Decision cannot authorize the changed candidate. Exact stale-approval code NC. |
| `422` public schema-invalid request | Input correction is required; not a transient retry. |
| `429` run admission | Throttled/not-started result with `Retry-After`; saved cases remain available. |
| `404`-equivalent foreign-resource result | Same response class as absent resource, without existence distinction. |
| Duplicate identical request | Return original operation/outcome, not a new error or second operation. |
| Duplicate event | Consumer records duplicate outcome without reapplying accepted business transition. |
| Stream disconnection | Progress delivery interrupted; no conclusion that execution failed or succeeded. |

**Sources:** [DDS], pp. 25, 48, 54–55, 58, 69, 83, 89.

No confirmed `400`, `401`, `403`, `413`, `415`, `500`, `502`, `503`, `504`, gRPC status, or SSE error-event mapping is supplied for the unspecified conditions. These mappings remain **Needs confirmation**, rather than being inferred from convention.

**ERR-COM-005 — Truthful accessible failure display.**

- Display source-supported failure, quarantine, unsupported-evidence, expiry, and degraded conditions as accessible text.
- Show the failed checkpoint where required.
- Do not show partial processing as an approved answer.
- Use `DRAFT`, `NEEDS_REVIEW`, and `PUBLISHED` only for their resolved artifact meaning; do not insert them into case or review state vocabularies.
- Reconstruct run progress from authoritative server state after refresh.
- Announce meaningful state transitions, retain visible focus and keyboard accessibility, and display workspace-local times with timezone labels.
- Exact message copy, banner/modal/inline placement, focus destination, retained form values, and retry-button placement remain NC.

**Sources:** [DDS], pp. 13, 41, 57–59.  
**Earlier trace:** `SCR-COM-005/007/008/011`, BR-045.  
**Open:** OQ-ERR-025.

### Request, Identity, and Replay Handling

Handling requirements inherit the evidence in the corresponding inventory rows and the shared contracts above.

| Exception | Response and user-facing outcome | Continuation, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-001 | HTTP `409`, `CASE_VERSION_CONFLICT`, current revision; canonical `retryable: false`. SCR-002 must not show save success. | Reject stale mutation. API-003 provides authorized current state for recovery. Resolve the intended change against that state before another accepted mutation; no automatic overwrite/merge is confirmed. | **OQ-ERR-004:** Revision encoding, missing header, local edit retention, conflict UI, and merge procedure. |
| ERR-002 | HTTP `409`, `IDEMPOTENCY_CONFLICT`; safe failed-submission indication. | Do not create a second outcome under that key. Do not blindly retry changed content or silently generate a new key to hide the conflict. A corrected/new operation needs explicit resolved identity semantics. | **OQ-ERR-005:** Key scope, fingerprint, TTL, and correction flow. |
| ERR-006 | Public schema-invalid request: HTTP `422`; exact code/details NC. Required review fields incomplete: both Approve and Reject disabled. | Validate before allocation/transaction/dispatch. Permanent failure; correct input rather than transient retry. Do not assume every business or header error is automatically `422`. | **OQ-ERR-001/002:** Field paths, missing-header codes, schemas, and validation presentation. |
| ERR-007 | Reject invalid boundary context. HTTP/code and sign-in/session display NC. | No unauthorized allocation/access. Authentication/session restoration follows the unresolved identity contract; do not retry rejected credentials as a dependency transient or invent browser refresh-token storage. | **OQ-ERR-003:** Claims, token expiry, clock tolerance, BFF/session and service errors. |
| ERR-008 | Stable non-sensitive denial; HTTP/code NC except ERR-009’s not-found class. | Permanent permission failure. No accepted business mutation. Retain permitted denial evidence; `AccessDenied` supports alert enrichment, not automatic paging for every denial. | **OQ-ERR-003/024:** Role/action matrix and alert enrichment/routing. |
| ERR-009 | Same `404`-equivalent response class for foreign-tenant and absent IDs. | Do not disclose content, existence, or foreign current revision. No automatic transient retry. Denial evidence retains principal and denied resource class under authorized audit scope. | **OQ-ERR-001/003:** Exact observable status/body and authorized audit projection. |
| ERR-010 | Safe rejected transition/business change; exact HTTP/code NC. | Reject unsupported state changes; preserve closed snapshots and denial history. Missing label-correction reason is not accepted. Authorized reopen/rework uses new revision, not historical overwrite. | **OQ-ERR-002/004:** Complete case guards, correction schema, close/reopen and invalid business-input outcomes. |
| ERR-011 | Reject stale/unauthorized/invalid settings; exact conflict code and actual settings API NC. | No accepted policy change. Valid update requires revision-safe durable audit. Do not mutate workspace settings through case PATCH solely from the source association. | **OQ-ERR-004/012:** Settings APIs, validation, activation and in-flight policy version. |
| ERR-012 | Return original accepted outcome/operation; case test requires identical response. | One accepted business creation. Case-domain mapping lasts 24 hours. Parallel pending replay, permission-changed result replay, and expiry behavior are unresolved. | **OQ-ERR-005:** Pending duplicates, response reconstruction, key expiry and non-case TTL. |
| ERR-013 | Record duplicate consumer outcome; no new accepted transition. No duplicate-specific HTTP code is confirmed. | Check event ledger and aggregate revision; return without reapplying mutation. Same event replayed 100 times still has one accepted business transition. Streaming backfill is not mutation replay. | **OQ-ERR-006:** Ledger/acknowledgment atomics, retention and step claim identity. |
| ERR-014 | Reject invalid input/permission context; stale mutation must not overwrite accepted later state. Exact consumer acknowledgment/status NC. | No cross-partition ordering assumption. Validate versioned envelope and trusted tenant scope. Permanent validation/permission failure is not transient-retried. Old-schema migration requires explicit provenance. | **OQ-ERR-006:** Stale/future revision disposition, signature/schema failures, poison-event routing and migrations. |
| ERR-015 | Documented retryable dependency error or actual persisted async operation ID; no ambiguous success. Lost response alone must not be presented as completed success. | Use replay-safe operation identity and authoritative records. Retry transient reads under bounded policy; mutable retries preserve idempotency and applicable authorization. Do not undo committed authority merely because a reply is missing. | **OQ-ERR-005/007/015:** Unknown commit outcome, timeouts, response reconstruction, dependency mapping and compensation. |

**Sources:** [DDS], pp. 13, 21–25, 45, 48–56, 83–86, 89.

### Integration, Ingestion, and Evidence Handling

| Exception | Response and user-facing outcome | Continuation, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-003 | `CONNECTOR_REAUTH_REQUIRED`; safe reauthentication-required condition in connector outcomes. HTTP status NC. | Revoked queued jobs fail without exposing tokens. Do not repeatedly retry revoked credentials as transient faults. Reauthentication/relaunch API, permission, and outcome are unresolved. | **OQ-ERR-009:** Credential status, reauthentication and queued-job resumption. |
| ERR-016 | Provider throttling retained as safe dependency outcome. Provider `429` is confirmed; public translation NC. | Honor connector `Retry-After`; use exponential backoff with jitter, caps, quotas, fair scheduling, and circuit controls. Do not amplify a burst with unlimited retries or unapproved fallback. | **OQ-ERR-007/009:** Attempt/delay limits, `Retry-After` syntax, provider classifications and fairness. |
| ERR-017 | HTTP `429` plus `Retry-After`; SCR-002 shows throttled/not-started condition. | Failed admission does not establish a started run. Saved cases remain available. Reattempt only through valid admission and idempotency semantics; no fixed retry interval supplied. | **OQ-ERR-001/008:** Admission code, threshold units/equality and reservation race. |
| ERR-018 | Terminal current-run outcome; exact code/status projection NC. Show authoritative failed checkpoint as applicable. | Do not automatically switch model or data class. Preserve attributed provider usage; refund/release/reconciliation formula NC. A user rerun is not an approved automatic recovery. | **OQ-ERR-008/023:** Exhaustion boundary, failed-call accounting and rerun identity. |
| ERR-019 | Explicit user-visible lower-trust warning; no exact warning literal/code supplied. | Use only supported capabilities. Missing ACL/delete support does not waive mandatory revocation/soft-delete controls. Exact safe restrictions must be resolved before affected mode is implemented. | **OQ-ERR-009/014:** Capability schema and permitted lower-trust behavior. |
| ERR-020 | Quarantined record with reason code, correlation ID, remediation path; literals/schema NC. | Bounded malformed-record retries, then durable quarantine exception. Remaining batch may proceed with exception in cursor ledger. No indefinite poison-record retry. | **OQ-ERR-009/010:** Retry bound, malformed taxonomy, quarantine/remediation and safe access. |
| ERR-021 | Show authoritative partial sync outcomes and recorded exceptions; exact run state NC. | Preserve accepted item outcomes. Cursor advances only after all preceding items have durable outcomes. Retry incomplete work safely; do not restart accepted items as new effects. | **OQ-ERR-009:** Cursor/run-history layout, per-item commits, concurrency, counts and partial completion. |
| ERR-022 | Fail closed; exact HTTP/code NC. Display safe rejected-file condition. | R1 accepts PDF, DOCX, HTML, UTF-8 text only under agreed signature/extension and configured limits. Do not parse beyond applicable safety admission or index rejected input. User correction/replacement is distinct from transient retry. | **OQ-ERR-010:** Exact allowlist, MB definition/equality, decompression threshold and rejection state. |
| ERR-023 | `QUARANTINED`; no indexing. Exact error/status mapping NC. | Scan before parse; no macro execution or remote-reference fetch. Preserve controlled quarantine evidence. Do not treat quarantine as ordinary low quality or automatically release/reparse unsafe content. | **OQ-ERR-010:** Scan/parser failure taxonomy, storage/retention, safe quarantine inspection and release procedure. |
| ERR-024 | Quality flags available under resolved status/view contract; not automatically `QUARANTINED`. | Safe authorized low-quality documents remain viewable but excluded from autonomous recommendations. Reprocessing may create side-by-side immutable versions; launch and eligibility thresholds NC. | **OQ-ERR-010/011:** Quality formulas, missing flags, OCR and document readiness. |
| ERR-025 | Do not present an unverified/unresolvable citation as valid. Safe source-access failure; exact code/display NC. | Cited version/anchor and current permission remain required. Do not substitute latest source or unauthorized cached content. Dependent publication cannot rely on invalid evidence. Evidence sufficiency after removing an invalid item is unresolved. | **OQ-ERR-011/014:** Anchor/URL contracts, revocation, missing source, retry and remaining-evidence rules. |
| ERR-039 | Safe unavailable/denied source outcome; HTTP/provider/signed-URL codes NC. | Retry only transient access faults under approved policy. A permission failure is permanent for that attempt. Do not bypass controlled source access through a public object endpoint or unrestricted URI. | **OQ-ERR-007/011/015:** Signed URL expiry/reissue, object not-found, provider denial and worker continuation. |

**Sources:** [DDS], pp. 27–32, 35–38, 42, 49, 52, 69–70, 82, 89.

### Model, Planner, and Policy Handling

| Exception | Response and user-facing outcome | Continuation, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-005 | `MODEL_OUTPUT_INVALID`; no publication. Run display reports exact failed checkpoint as applicable. HTTP/RPC mapping NC. | Versioned JSON validation with bounded parsing retries. Invalid fields/citations/control injection cannot become an approved artifact. Prior valid records remain distinct; failed-attempt usage treatment NC. | **OQ-ERR-007/008/011:** Output schema, retry count and missing-versus-invalid citation mapping. |
| ERR-026 | Stable safe abuse outcome; no source-supplied standalone injection code. Record injection indicators without logging hostile document/prompt text. | Label evidence untrusted, delimit passages, strip tool-call directives from evidence context, and enforce authorization outside model output. Fail closed against authority escalation. Indicator detection alone does not define a universal terminate-all-work rule. | **OQ-ERR-008/012/021:** Detection/stripping protocol and continue/reject distinctions. |
| ERR-027 | Arbitrary MCP invocation: `DENY` before dispatch as test outcome, not a newly declared HTTP code. A2A receiver may decline. | Validate pinned schemas/arguments and separate grants. Mutable operations require idempotency; consequential operations require human authorization. Do not substitute equivalent denied tool. Decline recovery/rerouting NC. | **OQ-ERR-003/008/012:** Actual grants/tools, human authorization, A2A decline/result and schema carriers. |
| ERR-028 | Stop exhausted/invalid execution and report failed checkpoint. Exact cause code/state mapping NC. | Enforce DAG depth maximum eight and maximum sixteen tool invocations. Repeated invalid plans terminate under a numerical bound not supplied. No recursive hint permits budget extension. | **OQ-ERR-008:** Depth/call counting, retries consuming budget, invalid-plan threshold and resume policy. |
| ERR-029 | Terminal result within configured maximum or recoverable timeout representation required by §2.3.1. Exact timeout state/code NC. | Deadline expiry stops the applicable execution. Retain durable checkpoints. Do not add a timeout enum or treat `run_timeout_seconds: 180` as reviewer SLA/HTTP timeout. Resume/cancel/new-run behavior NC. | **OQ-ERR-008:** Review waiting accounting, deadline equality, recoverable state and external-call deadlines. |
| ERR-030 | Present deterministic `DENY`, `REQUEST_MORE_EVIDENCE`, or required review outcome distinctly. Do not present it as approved/published success. | `DENY` stops denied path. More evidence does not license fabrication. High-risk unapproved run cannot publish. Missing-approval termination versus legitimate `AWAITING_REVIEW` requires explicit resolution. | **OQ-ERR-012/013:** Decision matrix, valid waiting, human/clarification routing and outcome states. |
| ERR-035 | Safe publication rejection; exact HTTP/event failure code NC. `PUBLISHED` must not be shown for rejected gate. | Recompute current authorization/evidence; validate exact artifact binding and approval sufficiency. Gate and final pointer commit together. Preserve earlier decision/generation records; no changed artifact under old approval. | **OQ-ERR-013/014/015:** Publication trigger, policy version, races, failure projection and retry identity. |

**Sources:** [DDS], pp. 7, 11–13, 31, 37–46, 49, 52, 82, 87–90.

### Review Handling

| Exception | Response and user-facing outcome | Continuation, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-031 | HTTP `409` conflict surface; stale rejection audited. Exact stale-approval code NC. SCR-005 must not show accepted approval of changed content. | Do not apply old hash to changed artifact. Obtain current exact task/candidate through the resolved review-read contract. Permanent stale attempt; no automatic unchanged retry. Historical decisions stay immutable. | **OQ-ERR-001/012:** Hash schema, task read/API, field retention and new decision flow. |
| ERR-032 | Reject ineligible/self/insufficient override action; HTTP/code NC. | High-risk author cannot self-approve. Override requires elevated role, secondary reviewer, audited reason. No inferred Admin review privilege. Retry after a genuine authorization/task change is a new validated attempt, not transient recovery. | **OQ-ERR-003/012/013:** Global self-approval scope, roles, secondary independence and override protocol. |
| ERR-033 | Authoritative expiry/reassignment/escalation indication; exact late-decision code NC. | Never implicit approval. Record escalation; preserve prior decisions. Decision/expiry and reassignment races unresolved. Do not apply execution timeout to review SLA by inference. | **OQ-ERR-012:** SLA clocks/values, equality, eligible states, late/multiple reviewers and routing. |
| ERR-034 | Both decision controls disabled when required fields incomplete. Exact context-load failure display NC. | Server validates required fields. Source evidence must be inspectable before approval; do not claim inspectability while unavailable. No confirmed “all citations clicked” gate or compulsory checkbox. Retry transient reads under shared policy; decision admission during partial context failure requires resolution. | **OQ-ERR-002/012/025:** Mandatory fields, exact context sufficiency, UI/focus and task-open trigger. |

**Sources:** [DDS], pp. 11, 45–46, 57–59, 83, 85, 89–90.

### Persistence, Messaging, Streaming, and Recovery Handling

| Exception | Response and user-facing outcome | Continuation, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-036 | Treat stale forbidden visibility as security incident. No forbidden evidence on next query. Exact screen/incident code NC. | Suspend affected aliases, revoke cached evidence, preserve audit traces, replay scoped ACL revisions. Reenable search only after negative-access tests pass. No TTL wait or degraded ACL bypass. | **OQ-ERR-014/024:** Atomic containment, source detection, in-flight data and reenable authority. |
| ERR-037 | Display authoritative indexing/workflow condition; no false source readiness. Alert on oldest queue age/backlog under resolved thresholds. | Keep accepted source metadata durable. Compare fingerprints, retry derivative writes, repair broken links from outbox. Scoped bounded validated operator replay; verify fingerprints and denied-access probes. | **OQ-ERR-006/007/014/024:** Detection bounds, replay selection, states, shard controls and receipts. |
| ERR-038 | Unsatisfied rebuild checks do not authorize read-alias switch. No separate error code supplied. | Keep replacement generation separate until completeness/recall checks pass. Source remains authoritative. Catch-up, failed-generation cleanup and already-switched rollback are unresolved. | **OQ-ERR-014:** Check formulas/thresholds, empty corpus, concurrent updates and generation recovery. |
| ERR-040 | No successful mutation/publication response without authoritative outcome. HTTP/code NC beyond known validation/conflict cases. | ACID units cannot partially commit case/approval and associated outbox, or gate and final pointer. Roll back uncommitted transaction unit; do not reverse confirmed committed work because downstream/response failed. Constraint-to-domain error mapping NC. | **OQ-ERR-004/005/015:** Locking, integrity errors, deadlocks, audit failures, lost commit reply and cross-store compensation. |
| ERR-041 | Worker loss does not establish successful completion. Show only server-authoritative progress/failure. | Durable plans/checkpoints and idempotent steps support safe recovery. Exact heartbeat detection, reassignment, lease, fencing, and resumed dispatch are not specified. | **OQ-ERR-015:** Worker ownership and bounded recovery protocol. |
| ERR-042 | Do not mark run complete/failed merely because SSE disconnected. | Refresh uses API-013 authoritative state. Retained reconnect uses API-015 and `Last-Event-ID`; backfill stays within caller scope. No polling interval, cursor-reset behavior, or new run allocation is implied. | **OQ-ERR-016/025:** Retention/gaps, offset type, token expiry, duplicates/order and connection display. |
| ERR-043 | Notification delivery failure is separate from case outcome. Delivery status/code NC. | Signed optional delivery retries with exponential backoff; recipient verifies signature/age. Internal case transition remains committed. No email/SMS fallback or manual redelivery API confirmed. | **OQ-ERR-017:** Signature/age, acknowledgments, cap, terminal delivery, deduplication and redelivery. |
| ERR-052 | Regional failure/recovery status and API behavior NC. Never claim recovery solely from a healthy-looking summary. | Primary receives persistent writes; secondary snapshot restore only under incident command. Restore relational/object consistency and index recipes; reference RPO `<=15 minutes`, RTO `<=4 hours`. Safety and elapsed recovery both measured. | **OQ-ERR-015/026:** Write fencing, providers/regions, restore failure, backup holds/deletes and timing points. |

**Sources:** [DDS], pp. 19, 34, 40, 45, 48–55, 58, 69–70, 79, 86, 90.

### Retention, Exit, Onboarding, Audit, and Release Handling

| Exception | Response and user-facing outcome | Continuation, data, retry, and recovery | Adjacent open decision |
|---|---|---|---|
| ERR-044 | Protected records retained and receipted. Exact held/all-held/empty operation status NC. | Case-retention jobs select only eligible closed cases. Enforce holds before destructive action; retain hold exceptions and purge receipts. Do not repeatedly attempt held removal as transient recovery. | **OQ-ERR-018:** Eligibility, hold races, receipt survival, retention policy and partial completion. |
| ERR-045 | Deny single-Admin/insufficient independent exit approval; HTTP/code NC. | Export/delete cannot proceed without two independent checks. Two client-selected IDs do not establish approval. Correct authorization protocol must precede execution. | **OQ-ERR-003/019:** Approval bindings, validity/revocation and execution rechecks. |
| ERR-046 | `202` means accepted exit work, not verified completion/download readiness. Partial/failed verification must not appear as full purge or completed export. | Preserve authoritative inventory/manifests/receipts. Held records protected; export excludes secrets/internal prompts. Retry only through durable idempotent work. Reverse deletion, automatic package cleanup, and partial compensation are not defined. | **OQ-ERR-018/019:** Partial states, verification, checksums, restart/resume, status/download and compensation. |
| ERR-047 | Incomplete provisioning visible; sync blocked. Empty queue alone does not establish search readiness. | One idempotent workflow establishes policy/encryption/roles/quotas/connector stubs. Backfill uses bounded windows, stable source IDs and per-batch receipts. Do not invent rollback of partially created resources. | **OQ-ERR-020:** Completeness, launch/status, checkpoint/order, overlap and compensation. |
| ERR-048 | Historical audit/revision/decision edit rejected; exact HTTP/code NC. Integrity/export failure must not be represented as verified evidence. | Keep append-only history and independent batch-hash export. Do not rewrite historical evidence to “repair” it. Specific chain-break/export recovery, retention delivery, and alert treatment NC. | **OQ-ERR-021/024:** Audit algorithms/checkpoints, failure recovery and notifications. |
| ERR-049 | Do not emit out-of-scope sensitive values in error, trace, provider, or export payload. Rotation-failure code/state NC. | Credentials remain vault-backed; declared tool/model scope enforced. Authorized connector credential revocation is supported, but no universal automatic post-disclosure rotation/incident procedure is supplied. Rotation must not require request-path bulk reencryption. | **OQ-ERR-021:** Privacy rules, incident recovery, vault outages, rotation overlap/switch/rollback. |
| ERR-050 | Blocking evaluation/release outcome for critical safety failure, low statistical confidence, or uncontrolled fixture substitution. Exact evaluation failure enum NC. | Preserve frozen versioned reviewed fixtures/expected citations/decisions and signed manifest. Do not treat missing/partial/empty suite as passing. Changed prompt/model requires reevaluation; results remain separate from release pass. | **OQ-ERR-022:** Statistical formulas, incomplete suite, signatures, result/progress, rerun and SEC definitions. |
| ERR-051 | No promotion when applicable compatibility/build/sign-off/safety gates fail. Canary regression triggers automated traffic rollback. | Reverse traffic/binary first; no automatic database down-migration. Compensation only explicitly supported. Nullable expansion/bounded backfill precedes enforcement after old-reader drainage. Preserve reconstructible release record. | **OQ-ERR-022:** Migration plans, thresholds/windows, sign-off, failed-backfill recovery and readable writes. |
| ERR-053 | Usage must not be fabricated as complete or zero merely because source data is missing. Exact degraded reporting status NC. | Preserve run/deployment/cost-center/category attribution. No cost refund, period restatement, or rerun aggregation formula selected. Mutable accounting retries remain idempotent. | **OQ-ERR-023:** Ledger grain, late data, failed-call billing, zero input, corrections and rounding. |
| ERR-054 | Safe error/no ambiguous success applies; exact condition, HTTP/code/display/scope NC. | No universal retry, rollback, cache substitution, or auto-recovery behavior is supplied. Resolve the component-specific failure contract rather than inheriting an arbitrary default. | **OQ-ERR-001/007/025:** Unhandled internal and UI failure contract. |

**Sources:** [DDS], pp. 20–21, 26–27, 52, 62–66, 72–80, 85, 88–90.

### Partial Processing and Compensation Matrix

**ERR-COM-006 — Committed authority and compensating actions.**

| Failure boundary | Required preserved state | Confirmed recovery/compensation | Unresolved action |
|---|---|---|---|
| Stale/unauthorized input rejected | Previously accepted business state. | No rejected business mutation accepted; permitted audit evidence retained. | Exact rejection transaction/audit implementation. |
| Case/approval transaction fails before commit | No partial accepted mutation/outbox. | ACID transaction boundary. | Audit/result-ledger participation and database error translation. |
| Publication transaction fails before commit | No pointer without satisfied gate. | Gate/pointer atomicity. | Retry/locking and exact failure projection. |
| Index write fails after source accepted | Accepted source metadata and immutable versions. | Fingerprint reconciliation/retry. | Partial object/index cleanup and reconciliation scheduling. |
| Connector partially processes batch | Durable accepted/exception item outcomes and safe cursor. | Retry partial batch; quarantine poison record; remaining batch may proceed. | Cursor claim/fencing, counts and partial terminal status. |
| Approval accepted but publication subsequently rejected | Immutable decision and candidate/evidence history. | Reject stale/unauthorized publication; no different artifact under approval. | New review/rework trigger after failed publication. |
| Webhook fails | Accepted case transaction. | Exponential delivery retry; no case rollback. | Terminal delivery/remediation contract. |
| Provisioning/backfill partially completes | Durable operation state and supported receipts. | Idempotent workflow and reconciled onboarding. | Resource cleanup/rollback/resume sequence. |
| Export partially completes | Authorized manifest/package evidence as available. | No excluded content; truthful outcome. | Package retention/cleanup and delivery recovery. |
| Deletion partly succeeds or encounters holds | Tombstones, removal receipts and protected records. | Protect/receipt held data; verify removal. | Relational/backup scope, reverse operations, partial completion enum. |
| Canary regresses | Readable data under declared rollback plan and release evidence. | Automated traffic rollback; binary first. | Explicit migration/data compensation. |
| Regional recovery fails | Recovery evidence and available authoritative backups. | Incident-controlled restore/consistency verification. | Restore retry, fencing, recovery-point selection and failure escalation. |

**Sources:** [DDS], pp. 20, 28–29, 45–46, 49–52, 55, 72, 78–80.

### Retry, Rerun, and Timeout Boundaries

**ERR-COM-007 — Retry permission is not a retry schedule.**

| Condition | Confirmed policy | Needs confirmation |
|---|---|---|
| Validation or permission failure | Permanent; no transient retry. | Exact correction/resubmission flow and code. |
| Transient dependency/read failure | Bounded exponential backoff, jitter, circuit breaker. | Attempts, delays, formula parameters, circuit thresholds/reset. |
| Mutable retry | Idempotency and separate authorization required. | Pending duplicate/unknown outcome protocol. |
| Consequential mutable tool retry | Human authorization also required. | Grant lifetime/reuse and operation inventory. |
| Provider throttling | Capped retries and controlled admission; connector honors `Retry-After`. | Header syntax, propagation, retry cap/deadline. |
| Malformed connector record | Bounded retries then quarantine. | Numerical bound and malformed/transient classification. |
| Invalid model output | Bounded parsing retries. | Count, whether provider is reinvoked, billing and final state. |
| Current-run quota exhaustion | Terminal current run; no model/data-class switch. | Budget release, authorized new-run semantics. |
| Deadline/runtime expiry | Applicable stop; terminal or recoverable result requirement. | Run timeout, review pause, recoverable state and resume. |
| Reprocessing normalization | Changed pipeline may produce side-by-side derivatives. | Launch/status and unchanged-version duplicate behavior. |
| Denied/rejected candidate rework | New run revision; historical denial unchanged. | Request linkage and allowed launch control. |
| Dead-letter replay | Reason, dry run, scope limit; preserve event identity/provenance. | Cap, deadline, approval mechanics and result. |
| SSE reconnect | Retained scoped replay via `Last-Event-ID`. | Cursor/history expiry and connection backoff. |
| Webhook retry | Signed exponential delivery; no case rollback. | Cap, age window, terminal disposition. |

**Sources:** [DDS], pp. 25, 28–29, 31, 38, 41–42, 46, 49–55, 58, 69.

The following must **not** become universal exception settings:

- `run_timeout_seconds: 180` and `replay_dedup_hours: 24` are Appendix F examples.
- The **24-hour case-domain** idempotency mapping is independently confirmed, but other ledger/history TTLs are NC.
- The **eight-depth** and **sixteen-tool-invocation** maxima are independently confirmed.
- Case-create P95 within/under **300 ms** and search P95 under **1.5 s** are service objectives, not request timeout settings.
- No retry count, heartbeat interval, polling schedule, replay batch size, or notification retry interval is supplied.

**Sources:** [DDS], pp. 12, 25, 40, 65, 90.

## Logging, Monitoring, and Operations

### Recorded Evidence and Trace Fields

**ERR-OPS-001 — Correlated evidence.** Every request carries trace and correlation context. Child spans represent database, connector, retrieval, model, and approval stages. Durable state-changing boundaries retain tenant, revision, actor, occurrence time, and correlation attribution. Exact carriers are unresolved where earlier contracts identify gaps.

| Field/content | Recording requirement | Type/carrier and sensitivity constraints | Source / mapping |
|---|---|---|---|
| `trace_id`, `correlation_id` | Every request; cross-boundary correlation. | Encoding/length/header/log schema NC. Correlation is independent of provider trace identifiers. | [DDS], pp. 16, 64; DAT-COM-F05. |
| `tenant_id` | Tenant-scoped requests, storage and signed background work. | Only trusted established scope. Invalid authentication must not fabricate a trusted tenant from unverified input. Failure-record carrier NC. | [DDS], pp. 22, 48, 51; DAT-COM-F01. |
| `revision` / `aggregate_revision` | Applicable durable change/stale-event guard. | Resource-specific representation NC; case revision is `BIGINT`. | [DDS], pp. 25, 48, 86. |
| `actor_id` / actor attribution | Applicable durable changes and authorized denial evidence. | Authenticated actor, not an untrusted actor override. Alias mapping NC. Unknown-identity failure recording NC. | [DDS], pp. 23, 45; DAT-COM-F03. |
| `occurred_at` and record times | Applicable durable changes/events. | UTC; public timestamp convention RFC 3339. Precision and commit-versus-occurrence mappings NC. | [DDS], pp. 48, 54, 59. |
| `event_id`, event type/version and aggregate context | Event identity, duplicate/stale processing, replay inspection. | Mandatory envelope fields; exact log projection NC. Do not dump raw `payload` into diagnostics. | [DDS], pp. 48–50; DAT-EVT fields. |
| Operation key/fingerprint/outcome | Replay-safe outcome reconstruction. | Physical/log projection, redaction and key scope NC. No new diagnostic key schema selected. | [DDS], pp. 25, 54; DAT-026. |
| Denied principal/resource class/action/policy digest | Authorized denial evidence and `AccessDenied` alert enrichment. | Must not disclose private resource existence. | [DDS], pp. 23, 87. |
| Failed checkpoint and safe cause | Human-visible run failure. | Exact fields/code vocabulary NC. No source text or secrets. | [DDS], p. 41; SCR-004-F08. |
| Quarantine reason/correlation/remediation | Malformed connector record outcome. | Vocabulary and remediation link/action schema NC. | [DDS], p. 29; DAT-015/021. |
| Evaluated artifact hash/decision/actor/time/rationale | Immutable review decision and stale-decision evidence. | Hash encoding and authorized rationale projection NC. Not unrestricted diagnostic text. | [DDS], pp. 45–46; DAT-011/012. |
| Prompt-injection indicators | Record detected indicators. | Indicator schema NC; no hostile source/prompt content in traces. | [DDS], p. 39; DAT-024. |
| Source fingerprints/index generation/ACL revision | Reconciliation and delayed-index inspection. | Hash algorithms and safe projection NC. | [DDS], pp. 49, 90; DAT-023/026. |
| Purge target/time/actor/receipts/hold exceptions | Auditable eligible removal and protected-record outcomes. | Selected receipt fields `tenant_id`, `object_ref`, `purge_time`, `actor`; complete schema NC. | [DDS], pp. 66, 80, 85. |
| Incident audit IDs/time window/blast radius/quality effect/preventive action | Delayed-indexing incident documentation. | Incident schema, authorized audience and mandatory record format NC. | [DDS], p. 90, §F.1. |
| Release digest/schema/prompt/routing versions; signed test evidence | Reconstructible deployment and acceptance evidence. | Signature/storage/record schema NC. | [DDS], pp. 73, 89; DAT-031/032. |

**Needs confirmation — OQ-ERR-006/021/024:** Complete exception-event/log schemas, actor/correlation envelope carriers, log access, missing-identity recording, and evidence retention. No new `error_events` table or diagnostic schema is confirmed.

### Log Levels and Sensitive Values

| Logging aspect | Specification |
|---|---|
| Log level per exception | **Needs confirmation — OQ-ERR-024.** The source does not assign `DEBUG`, `INFO`, `WARN`, `ERROR`, `CRITICAL`, or equivalent levels. |
| Recovered versus exhausted retry level | **Needs confirmation.** Do not infer a level solely from HTTP `429`, `409`, or a duplicate result. |
| Stack traces/raw internal diagnostics | **Needs confirmation.** Any authorized diagnostic representation must preserve the source privacy constraints; public raw-stack display is not confirmed. |
| Sampling | `trace_sample_rate: 0.10` is an example, not approved policy. Required audit/accepted-transition evidence must not be silently waived through sampling. |
| Documents/prompts/secrets | Diagnostic traces never contain user documents or API secrets. Logs capture token counts/digests, not entire prompts by default. Error details exclude credentials/full prompts/retrieved documents. |
| Provider request observation | Verify no connector tokens or out-of-scope secrets enter model/tool/provider calls. |
| PII | Extraction tags likely personal data; provider context redacts nonessential fields where policy permits. Categories and masking rules NC. |
| Historical evidence | Audit entries/revisions append-only; decisions immutable; audit batch-hash export independently retained. |
| Diagnostic versus audit retention | Source baseline distinguishes 30-day diagnostic default TTL and fictional seven-year audit policy. Approved corporate policy and precedence remain NC. Purge records receipts/hold exceptions. |

**Sources:** [DDS], pp. 15, 21, 27, 62–66, 79, 84, 90.

**ERR-OPS-002 — Accepted-transition evidence.** Retain one audit record for an accepted state transition. Duplicate-processing outcomes must not create another accepted business transition. Preserve required denial/stale/replay evidence without reclassifying it as a second accepted mutation.

**Sources:** [DDS], pp. 10, 13, 17, 46, 50, 74, 89.

### Monitoring and Notification Conditions

| Condition / related exceptions | Confirmed signal/action | Recipient and threshold status |
|---|---|---|
| User-impacting failure-budget incident | Paging category; monitor request/error rate, latency and saturation. | Actual recipient, budget calculation, threshold/window and route **NC**. |
| Stale ACL propagation / missing approval enforcement — ERR-030/035/036 | User-impacting paging category. | Specific on-call/security recipient and escalation sequence **NC**. |
| Model provider outage — ERR-015/016/017 | Disable new generation admission, preserve manual/evidence workflows, display degraded state; page on-call only when availability budget impacted. | Generic on-call role confirmed; individuals/routes/budget threshold **NC**. |
| Routine token-spend anomaly — ERR-018/053 | Create ticket with owner and threshold, not automatically a page. | Actual owner, threshold, ticket channel and deduplication **NC**. |
| Delayed indexing — ERR-037 | Alert on queue oldest age/index backlog; identify tenant/generation. | Numeric age/backlog threshold, route and recipient **NC**. |
| Worker capacity/queue pressure — ERR-016/017/041 | Extraction/embedding scale on queue age/throughput; API scales on utilization/latency. | Worker counts, scaling windows and triggers **NC**. |
| AI behavior | Monitor grounding pass rate, retrieval empty rate, provider throttling, token use and approval backlog age. | Calculation/window/alert thresholds **NC**. |
| Review task expiry — ERR-033 | Reassign/escalate under policy; record escalation. | Reviewer pools/minimum roles supported; specific recipients/channels/SLA **NC**. |
| Denial event — ERR-008/009/027/032/045 | `AccessDenied` supports alert enrichment. | No confirmation that every denial pages; enrichment and thresholds **NC**. |
| Export/deletion/evaluation completion/failure — ERR-046/050 | Durable authoritative outcomes and source-required evidence. | Email/SMS/in-app/other notification delivery and recipients **NC**. |
| Webhook delivery — ERR-043 | Optional signed notification to configured recipient; signature/age validation. | Subscription/admin/acknowledgment/security/retry contract **NC**. |
| Audit, rotation, object or reporting failure — ERR-039/048/049/053 | Required integrity/privacy/accounting constraints remain effective. | Failure-specific alert thresholds, recipients and runbooks **NC**. |

**Sources:** [DDS], pp. 19, 45, 55, 64–66, 69, 79, 87, 90.  
**Earlier trace:** `BAT-OPS-008`, BR-044/046.

**Needs confirmation — OQ-ERR-024:** Define severity-to-notification mapping, actual recipients, routing, escalation, deduplication, notification-content redaction, and failed-notification handling. Security/SRE sign-off responsibilities are confirmed release roles, not automatically the notification recipients for all exceptions.

### Operational Inspection Surfaces

| Interface/activity | Confirmed inspection or recovery purpose | Boundary restrictions and gaps |
|---|---|---|
| API-013 `GET /v1/runs/{runId}` | Authoritative run stages/evidence; refresh reconstruction. | Analyst/Reviewer resource scope; complete result NC. |
| API-014 `GET /v1/runs/{runId}/steps` | Steps/checkpoints. | Read predicate/order/schema NC. |
| API-019 `GET /v1/connectors/{connectorId}/runs` | Sync outcomes/cursor/error context. | Read permission/schema NC. |
| API-021 `GET /v1/audit/events` | Auditor immutable cursor-paginated evidence. | Redacted scope; no inferred general case/source access. |
| API-037 `GET /internal/workflows/{runId}` | Protected workflow inspection. | Service/operator identity and projection NC; not automatically browser-accessible. |
| API-038 `POST /internal/deadletters/{id}/replay` | Bounded validated replay. | Operator reason, dry run, scope; request/result/role NC. |
| API-039 `GET /internal/storage/documents/{id}` | Narrow protected storage access. | Not a confirmed browser source endpoint. |
| API-041/042 internal metrics/capacity | Protected observability/capacity data. | Exact grants/projections NC; reads do not authorize execution. |
| API-043/044 internal releases | Controlled release work and evidence inspection. | Build/operator grants and contracts NC. |
| Pause connector/shard, suspend/reenable aliases, restore snapshots | Source-described incident controls. | Commands/endpoints/roles are NC; no new operational console established. |

**Sources:** [DDS], pp. 28–29, 40–42, 48–53, 64–73, 79, 83, 90.

### ERR-OPS-003 — Delayed Document Indexing Runbook

**Applies to:** ERR-021/037/038; BAT-002/004/011/012.

1. **Detect:** Alert on oldest queue age and index backlog; identify affected tenant and index generation.
2. **Contain:** Pause only the faulty connector or indexer shard. Keep accepted source records durable.
3. **Diagnose:** Inspect event ID, outbox lag, parser flags, search throttling and source ACL revision.
4. **Recover:** Replay validated outbox records through a bounded operator-controlled job.
5. **Verify:** Compare source fingerprints with indexed versions and run denied-access probes before closing the incident.
6. **Document:** Link audit IDs, time window, blast radius, quality effect and preventive action.

**Source:** [DDS], p. 90, §F.1.

**Needs confirmation — OQ-ERR-006/014/024:** Alert thresholds, shard identity, pause/resume controls, replay bounds, probe definitions, incident schema and operator authorization.

### ERR-OPS-004 — Suspected ACL Leak Runbook

**Applies to:** ERR-036 and publication effects under ERR-035.

1. Suspend affected index aliases.
2. Revoke cached evidence.
3. Preserve audit traces.
4. Execute scoped replay of ACL revisions.
5. Reenable search only after negative-access tests pass.

**Source:** [DDS], p. 79, §22.2.2.

Do not rely on ordinary cache TTL, eventual index consistency, or reduced-quality retrieval to tolerate forbidden evidence.

**Needs confirmation — OQ-ERR-014/024:** Affected-scope determination, in-flight containment, command/API, authorization, test selection, and reenable sign-off.

### ERR-OPS-005 — Model Provider Outage Runbook

**Applies to:** ERR-015/016/017 and approved fallback restrictions.

1. Disable new generation admission.
2. Keep manual case and evidence workflows available.
3. Display degraded status.
4. Preserve approved deployment/region and equal-or-stronger fallback constraints.
5. Page on-call only when availability budget is impacted.

**Sources:** [DDS], p. 37, §10.1.2; p. 69, §19.2.2; p. 79, §22.2.1.

Lexical retrieval may continue during vector degradation only with a visible reduced-quality flag and unchanged authorization/approval controls.

**Needs confirmation — OQ-ERR-007/014/026:** Outage detection, admission/error response, permitted fallback selection, recovery/reenable conditions and budget calculation.

### ERR-OPS-006 — Controlled Replay Procedure

**Applies to:** ERR-013/014/037 and dead-letter recovery.

1. Authenticate and authorize the operator for the selected tenant/resource scope.
2. Require an operator reason, dry-run validation and scope limit.
3. Validate the original envelope/schema and applicable resource controls.
4. Preserve original event identity.
5. If an explicit migration transforms the schema, retain an explicit provenance link.
6. Execute only the bounded validated selection.
7. Let original consumers enforce idempotency, revisions, policy and exact publication binding.
8. Use the applicable reconciliation verification, including fingerprints and denied-access probes for delayed indexing.

**Sources:** [DDS], p. 50, §13.3.2; p. 90, §F.1.

**Needs confirmation — OQ-ERR-006/007:** Reason format, scope units/value, dry-run result, migration approval, deadline, partial result, replay status and exhausted disposition. No automatic replay of every permanent denial is authorized.

### ERR-OPS-007 — Regional and Release Recovery Constraints

| Recovery situation | Confirmed procedure/constraint | Open operational contract |
|---|---|---|
| Regional outage | Restore secondary snapshots only under incident command; reconcile relational/object consistency and test index rebuild recipes. Measure RPO/RTO and safety. | Recovery point, write fencing, provider/region, worker activation, restore commands and retry. |
| Canary regression | Automated traffic rollback, binary first; no automatic database down-migration. | Thresholds, duration, traffic sequence and explicitly supported data compensation. |
| Migration/backfill failure | Preserve active-reader compatibility; bounded backfill before final enforcement; old replicas drain before postdeploy enforcement. | Resume/checkpoint, failed-batch compensation, verification and result state. |
| Security-release finding | Unmitigated critical tenant-isolation/approval-bypass findings block promotion regardless of benchmark score. Security-control evidence independently reproduced and signed. | Individual `SEC-001`–`SEC-012`, sign-off transport and assigned control owner. |

**Sources:** [DDS], pp. 19–20, 52, 69–70, 72–76, 88–89.

### Undescribed Operational Recovery

The source does not establish complete runbooks for transaction deadlocks, audit-storage outage, lost worker ownership, failed key rotation, incomplete usage rollup, partial export packaging, corrupt backups, or generic unhandled application exceptions.

These are **Needs confirmation**, not out of scope. ERR-040/041/046/048/049/052/053/054 retain the shared safety and durability constraints, but no automatic restart, rollback, cleanup, replacement credential, or notification recipient is selected.

## Failure Acceptance Criteria

### Verification Basis

**ERR-COM-008 — Failure test evidence.**

- Use synthetic successful, empty, mixed-permission, adversarial and malformed fixtures.
- Record every randomized-test seed.
- Exercise transitions, tenancy, idempotency, hashes, retries and schema compatibility without live model dependencies where specified.
- Pin provider-facing adapters through consumer-driven contracts.
- Integration tests cover PostgreSQL transactions, outbox replay, ACL revocation, delayed indexing and object purge.
- Critical isolation and approval tests pass with zero exceptions.
- Sign release test outputs and reference release digest.
- A test may assert a confirmed invariant now, but must not invent an unresolved code, state, threshold, retry count or schedule.

**Sources:** [DDS], pp. 74–76, 88–89.

### Request, Authorization, and Replay Criteria

| Acceptance ID | Trigger/action | Expected response, screen and data result | Retry/recovery assertion | Trace/source |
|---|---|---|---|---|
| AC-ERR-001 | Authorized current case is changed on server; submit stale `If-Match`. | `409 CASE_VERSION_CONFLICT`, current revision, canonical safe conflict; no successful-save display or stale case mutation. | Unchanged stale request is not transient-retried. Authorized current read supports resolved conflict recovery. | ERR-001; API-004; AC-BR-007. [DDS], pp. 25, 83–84. |
| AC-ERR-002 | Reuse accepted case-create key with changed body. | `409 IDEMPOTENCY_CONFLICT`; no second outcome under key. | Repeat changed body remains conflicting; no silent new operation identity. | ERR-002; `TST-002`. [DDS], pp. 54, 89. |
| AC-ERR-003 | Submit identical case creation twice within case-domain contract. | One case and identical original response. | Concurrent/randomized retry leaves one accepted creation; pending-response details await OQ-ERR-005. | ERR-012; `TST-001`. [DDS], pp. 25, 89. |
| AC-ERR-004 | Schema-invalid public payload before allocation. | `422`; no accepted mutation or premature long-running allocation. Safe details only. | No transient retry; correction required. Exact field paths/code await resolution. | ERR-006; BR-006. [DDS], pp. 54, 56. |
| AC-ERR-005 | Unexpected token algorithm, missing tenant claim, or wrong internal audience. | Reject before unauthorized access/work. Do not expose private resource context. | Invalid credentials are not treated as transient dependency fault. | ERR-007; BR-002. [DDS], pp. 18, 21–22. |
| AC-ERR-006 | Role/resource/ACL/action/SoD predicate fails. | Denied action leaves accepted business state unchanged; authorized non-sensitive denial evidence retained. | No automatic transient retry or role inference from navigation/Admin status. | ERR-008; BR-003. [DDS], pp. 22–23, 83. |
| AC-ERR-007 | Foreign-tenant case ID compared with absent ID. | Same `404`-equivalent non-disclosing class; no content/existence/current-revision leak. | Retry does not expand scope. | ERR-009; `TST-003/T-01`. [DDS], pp. 23, 88–89. |
| AC-ERR-008 | Invalid case-state value/transition or missing classification-correction reason. | Invalid state rejected under resolved domain/schema mapping; reasonless correction not accepted; prior lineage preserved. | Correction/rework uses supported new validated action; no historical overwrite. | ERR-010; BR-011/014/015. [DDS], pp. 12, 25–26, 86. |
| AC-ERR-009 | Stale/unauthorized workspace settings update. | No accepted settings change; valid updates retain revision/audit requirement. | No case PATCH binding invented; API/conflict recovery awaits resolution. | ERR-011; BR-007/010. [DDS], p. 24. |
| AC-ERR-010 | Replay same event 100 times. | Exactly one accepted business transition; duplicate outcome recorded; one accepted-transition audit record. | No repeated mutation on consumer retries. | ERR-013; `T-07/TST-007`. [DDS], pp. 48–50, 88–89. |
| AC-ERR-011 | Deliver delayed/stale event and invalid scope/schema. | Stale mutation cannot overwrite accepted later state; validation/permission failures cannot mutate target. | No cross-partition ordering dependency; exact stale acknowledgment/poison disposition awaits OQ-ERR-006. | ERR-014; BR-009. [DDS], pp. 22, 48–50. |
| AC-ERR-012 | Lose reply after an accepted idempotent mutation, then retry same operation identity. | Authoritative original outcome recovered under resolved contract; no second business effect or invented completion. | Retry respects original fingerprint and resource authorization; pending/permission-changed result details NC. | ERR-015/040; BR-006/008. [DDS], pp. 25, 54, 74. |
| AC-ERR-013 | Dependency unavailable before completion/allocation. | Documented retryable failure or real persisted operation identity; never ambiguous success. | Bounded transient policy; permanent denial/validation not retried. | ERR-015; `API-PROC-001`; [DDS], interface requirements pp. 8–80; p. 49. |

### Integration, Ingestion, and AI Criteria

| Acceptance ID | Trigger/action | Expected response, screen and data result | Retry/recovery assertion | Trace/source |
|---|---|---|---|---|
| AC-ERR-014 | Provider produces `429` burst. | Capped retries and admitted load controlled; safe provider outcome, no false completion. | Configured connector `Retry-After` honored; exact cap/window awaited. | ERR-016; `TST-008`. [DDS], pp. 28, 49, 89. |
| AC-ERR-015 | New-run tokens/queue/capacity threshold fails. | `429` plus `Retry-After`; no started-run success; saved case remains available. | Reattempt through normal admission/key semantics, not automatic unlimited retry. | ERR-017; BR-024. [DDS], p. 69. |
| AC-ERR-016 | Current-run quota exhausted. | Terminal current-run outcome; exact failed checkpoint shown as applicable. | No automatic cheaper/model/data-class switch; usage stays attributable. | ERR-018; BR-025. [DDS], pp. 38, 65. |
| AC-ERR-017 | Revoke connector credential while jobs queued. | `CONNECTOR_REAUTH_REQUIRED`; no token in response, trace or prompt. | Revoked credential not transient-retried; reauthentication contract remains NC. | ERR-003; BR-034. [DDS], p. 27. |
| AC-ERR-018 | Connector capability unsupported. | Explicit lower-trust warning; no silent capability assumption. | Missing ACL support does not permit forbidden evidence/revocation delay. | ERR-019; BR-034. [DDS], pp. 27–29. |
| AC-ERR-019 | Malformed record reaches resolved retry bound. | Quarantine reason/correlation/remediation; durable exception ledger. | Remaining batch may proceed; repeated processing cannot duplicate accepted outcomes. | ERR-020; BR-035. [DDS], p. 29. |
| AC-ERR-020 | Partial batch interrupted before cursor commit. | Cursor cannot advance beyond preceding nondurable outcomes; accepted outcomes preserved. | Retry accounts for earlier accepted/exception outcomes. | ERR-021; BAT-002. [DDS], p. 28. |
| AC-ERR-021 | Upload MIME mismatch, unsupported category, oversized or decompression-violating input. | Fail closed; safe rejection; no unsafe parsing/indexing or false ready state. | Invalid input not indefinite-retried. Exact 25 MB/unit/equality tests await OQ-ERR-010. | ERR-022; BR-016. [DDS], pp. 13, 30. |
| AC-ERR-022 | Unsafe PDF/polyglot/zipped payload. | Quarantine; no indexing; scan precedes parse; no macro execution/remote fetch. | No automatic quarantine release or treatment as low-quality viewing permission. | ERR-023; `T-04/TST-015`. [DDS], pp. 30, 88–89. |
| AC-ERR-023 | Safe authorized low-quality extraction. | Viewable but excluded from autonomous recommendations; quality flags preserved. | Changed-pipeline reprocessing is side-by-side; thresholds/state await resolution. | ERR-024; BR-018. [DDS], pp. 31–32. |
| AC-ERR-024 | Retrieval evidence insufficient or ambiguous. | `NO_SUPPORTED_EVIDENCE`; no fabricated context or supported-publication claim. | Clarification/human routing only through resolved contract, not repeated blind generation. | ERR-004; BR-019. [DDS], p. 36. |
| AC-ERR-025 | Candidate has missing citations. | Needs-review or unsupported outcome; no unsupported publication. | Distinction from invalid citation/schema failure must be explicitly mapped. | ERR-004/005/025; `TST-009`. [DDS], p. 89. |
| AC-ERR-026 | Citation cannot resolve/current source permission fails. | No unverified source presented as valid; dependent gate cannot count forbidden/unresolvable evidence. | Do not substitute latest/unauthorized source; transient object retry is separate. | ERR-025/039; BR-017/019. [DDS], pp. 31, 35, 52, 57. |
| AC-ERR-027 | Model has unknown field/invalid citation/control injection. | `MODEL_OUTPUT_INVALID`; no publish; authoritative checkpoint failure. | Bounded parse retries; no unbounded regeneration. | ERR-005; `TST-005`. [DDS], pp. 38, 41, 89. |
| AC-ERR-028 | Hostile paragraph/tool directive in retrieved evidence. | Evidence untrusted/delimited; directives stripped from evidence context; indicators recorded safely; no authority escalation. | No tenant/tool/approval changes or unrestricted destination from content. | ERR-026; `T-02`. [DDS], pp. 7, 38–39, 61, 88. |
| AC-ERR-029 | Arbitrary MCP or consequential mutable tool without authorization. | `DENY` before arbitrary dispatch; no unauthorized mutable effect. | No equivalent-tool substitution; retries retain idempotency/human authorization. | ERR-027; `TST-014`. [DDS], pp. 41–42, 87, 89. |
| AC-ERR-030 | A2A receiver declines task. | No assumed task acceptance or completed result. | Decline response/recovery remains NC; no invented transport status/fallback. | ERR-027; API-046. [DDS], p. 41. |
| AC-ERR-031 | Plan exceeds depth eight/call maximum sixteen or repeatedly invalid. | Bound enforced; exhausted/invalid path stops; checkpoint reported. | Exactly eight/sixteen is within maxima but other guards apply; accounting/invalid count unresolved. | ERR-028; `T-10`; BR-026. [DDS], pp. 40–42, 88. |
| AC-ERR-032 | Execution reaches resolved deadline/runtime maximum. | Applicable stop and terminal/recoverable result; no false publication. | No invented timeout enum or 180-second review expiry; resume behavior awaited. | ERR-029; BR-026. [DDS], pp. 12, 41, 90. |
| AC-ERR-033 | Deterministic `DENY`/more-evidence or absent required approval. | Denied path does not proceed; unsupported/high-risk unapproved answer not published. | More evidence/review wait stays distinct from missing-approval failure pending resolution. | ERR-030; BR-028/032. [DDS], pp. 11–13, 41, 44–49. |
| AC-ERR-034 | Restricted context during provider outage. | No unapproved model/deployment/region fallback. | Only approved equal-or-stronger fallback is eligible; no quota-driven class change. | ERR-015/018; `T-06`. [DDS], pp. 37, 88. |

### Review, Persistence, and Lifecycle Criteria

| Acceptance ID | Trigger/action | Expected response, screen and data result | Retry/recovery assertion | Trace/source |
|---|---|---|---|---|
| AC-ERR-035 | Wrong/prior reviewed artifact hash submitted. | `409` conflict surface, stale rejection audited; changed candidate not approved/published. | Reload exact current context through resolved API; no old hash reuse. | ERR-031; `T-03/TST-006`. [DDS], pp. 45–46, 83, 88–89. |
| AC-ERR-036 | High-risk author self-approves or override lacks cumulative requirements. | Denied; no high-risk self-publication or unauthorized override. | Historical denial unchanged; legitimate rework is new run revision. | ERR-032; BR-029/033. [DDS], pp. 11, 46, 85. |
| AC-ERR-037 | Task reaches configured SLA. | No implicit approval; reassignment/escalation and escalation evidence. | Late/race handling awaited; no timer-triggered publication. | ERR-033; `TST-010`. [DDS], pp. 45, 89. |
| AC-ERR-038 | Required review fields incomplete or source context unavailable. | Incomplete fields disable both controls; exact candidate/context and source inspectability are not falsely claimed. | Transient read retry separate from decision; no mandatory click-count invented. | ERR-034; BR-030/045. [DDS], pp. 57–58. |
| AC-ERR-039 | Permissions change between retrieval and publication; replay old approval for changed artifact. | Gate rechecks and rejects stale/forbidden evidence/content; final pointer unchanged by failed publication. | Replay cannot publish different artifact or create second transition. | ERR-035; BR-032. [DDS], pp. 13, 45–46. |
| AC-ERR-040 | Interrupt publication/case/approval transaction before commit. | Gate/pointer and mutation/outbox cannot partially commit. | Retry follows idempotency/transaction recovery, not blind compensation. | ERR-040; DAT-LC-015. [DDS], pp. 45, 52. |
| AC-ERR-041 | FK/workspace-tenancy mismatch or pooled-context reuse. | Constraint/domain guard prevents invalid reference or inherited tenant visibility; no unauthorized effect. | Session reset after exception/transaction; failure mechanics awaited. | ERR-008/009/040; BR-004. [DDS], p. 86. |
| AC-ERR-042 | Revoke source access after indexing and query next. | No forbidden evidence; affected cache invalidated before new result; stale visibility is incident. | No wait for TTL/index cleanup; apply ACL containment/verification. | ERR-036; `TST-004/T-08`. [DDS], pp. 27–29, 53, 88–89. |
| AC-ERR-043 | Index write fails after source accepted. | Source metadata remains durable; no false indexing readiness. | Reconciliation compares fingerprints and retries; outbox repairs broken links. | ERR-037; BR-009/020. [DDS], p. 49. |
| AC-ERR-044 | Execute delayed-index runbook. | Pause only faulty connector/shard, preserve source; documented scope/evidence. | Bounded validated replay; fingerprints and denied-access probes verified. | ERR-037; ERR-OPS-003. [DDS], p. 90. |
| AC-ERR-045 | Replacement index fails completeness/recall checks. | No authorized alias switch to unpassed generation. | Threshold/catch-up/empty-corpus behavior awaited; no default pass. | ERR-038; BR-020. [DDS], p. 34. |
| AC-ERR-046 | Lose worker heartbeat or fail object access. | No false completed step/run/source retrieval; tenant/privacy controls remain. | Durable checkpoint/idempotency safety verified; lease/fencing/retry specifics awaited. | ERR-039/041; BR-047. [DDS], pp. 40, 49, 70. |
| AC-ERR-047 | Disconnect SSE then refresh/reconnect within retained history. | API-013 server state reconstructs progress; scoped monotonic retained backfill through `Last-Event-ID`; no new run. | Cursor gap/session expiry result awaited; no disconnection-as-success. | ERR-042; BR-045. [DDS], pp. 55, 58. |
| AC-ERR-048 | Webhook fails after committed case change. | Case remains committed; notification not shown as evidence of rollback. | Signed exponential retry; recipient signature/age checks; cap awaited. | ERR-043; BAT-025. [DDS], p. 55. |
| AC-ERR-049 | Retention selection includes open/ineligible/held cases. | Only eligible closed cases selected for case retention; held data protected/receipted. | No transient retry of protected purge; all-held/empty state awaited. | ERR-044; BR-038. [DDS], pp. 26, 66. |
| AC-ERR-050 | Single Admin attempts export/delete. | Independent checks prevent operation proceeding. | Resubmission cannot satisfy two-person control with same-person duplicated evidence. | ERR-045; `T-11`. [DDS], pp. 78, 83, 88. |
| AC-ERR-051 | Authorized exit partially fails or encounters legal hold. | No false completed export/full purge; tombstones/receipts/protected data preserved; export secrets/internal prompts absent. | Idempotent scoped continuation; specific compensation/status awaited. | ERR-046/044; `TST-013`. [DDS], pp. 79–80, 89. |
| AC-ERR-052 | Provisioning interrupted or backfill readiness incomplete. | Visible incomplete state; sync blocked; stable source IDs/batch receipts and coverage-based readiness preserved. | One idempotent workflow; no invented partial-resource rollback. | ERR-047; BR-042. [DDS], p. 78. |
| AC-ERR-053 | Attempt historical audit/decision edit. | Rejected; append-only/immutable evidence unchanged. | No recovery that rewrites historical record to hide exception. | ERR-048; `T-09`. [DDS], pp. 62, 85, 88. |
| AC-ERR-054 | Inspect errors/traces/provider requests/exports for sensitive content. | No forbidden credentials/documents/full prompt/error existence leakage; allowed counts/digests and authorized evidence remain. | Vault/rotation failure must not introduce secret fallback in diagnostics. | ERR-049; `T-05`; ERR-COM-003. [DDS], pp. 61–66, 79, 84, 88. |
| AC-ERR-055 | Replace frozen fixtures, fail critical isolation/approval test, or produce low statistical confidence. | Evaluation/release gate blocks acceptance/promotion irrespective of benchmark score. | Reevaluation preserves versions/manifests; no empty/partial denominator pass. | ERR-050; `T-12`; BR-049. [DDS], pp. 74–76, 88. |
| AC-ERR-056 | Canary safety regresses or compatibility/build/sign-off gate fails. | Promotion blocked; regression traffic rollback, not database down-migration; release bindings reconstructible. | Data compensation only explicitly supported; failed-backfill procedure awaited. | ERR-051; `TST-016`. [DDS], pp. 20, 52, 72–73, 89. |
| AC-ERR-057 | Primary-region outage/recovery exercise. | Incident-controlled restore; relational/object/index consistency; RPO `<=15 minutes`, RTO `<=4 hours`. | Timing pass cannot override safety failure; fencing/restore retry awaited. | ERR-052; `TST-012`. [DDS], pp. 19, 69–70, 89. |
| AC-ERR-058 | Provider usage missing/late or rollup partially processed. | No invented complete/zero/cost value; attribution preserved. Exact reporting failure state NC. | No duplicate mutable accounting under retry; correction/refund formula awaited. | ERR-053; BR-025/043. [DDS], pp. 38, 65, 85. |
| AC-ERR-059 | Keyboard-only user encounters supported error/recovery interaction. | No blocked supported action; visible focus; meaningful accessible state text. | Exact post-error focus/navigation awaits screen contract, not arbitrary implementation. | ERR-COM-005; `TST-011`. [DDS], pp. 58–59, 89. |
| AC-ERR-060 | Generic supported boundary fails without component-specific mapping. | Safe no-ambiguous-success requirement remains; no invented code/state/retry policy becomes confirmed. | Failure contract must resolve before production assertions use it. | ERR-054; ERR-COM-001/002. [DDS], pp. 8–80, boundary requirements. |

### Empty, Partial, and Boundary Tests Requiring Resolution

| Test family | Confirmed constraint | Unresolved assertion |
|---|---|---|
| Exact upload size/decompression boundary | Fail closed beyond configured bounds. | Decimal/binary MB, inclusive 25 MB equality, decompression units/value. |
| Admission/quota equality | Admit only when thresholds satisfy; exhaustion terminal current run. | Comparison boundaries, reservation/count and provider-use authority. |
| Run/review deadline equality | Stop applicable execution; expiry never approves. | Clocks, pause, equality, valid wait and recoverable representation. |
| Event/key expiry | One accepted outcome within applicable contract; safe replay. | Exact 24-hour equality, non-case TTL, expired history and key reuse. |
| No connector changes | Durable cursor/outcome constraints remain. | No-op status, cursor advancement, receipt and notification. |
| Empty extraction | Quality evidence and no unsupported autonomous use. | Quality thresholds, indexing/readiness and quarantine distinction. |
| Empty index/rebuild/backfill | Alias/readiness checks remain required. | Empty completeness/recall/coverage denominator and no-op result. |
| No expired tasks | No implicit approval. | No-op record/notification and timer behavior. |
| All held/no eligible purge | No protected/ineligible removal. | Receipt, operation completion, verification event and final status. |
| Empty/partial export | Scope, independent approvals and exclusions remain. | Manifest/package/no-op/cleanup behavior. |
| Empty/partial evaluation | Frozen evidence and safety gates required. | Failure/result enum, scores, confidence and rerun. |
| No/late usage | Attribution and truthful reporting required. | Zero/omit, daily window, refund/restatement and rounding. |
| SSE cursor/history gap | Server state authoritative; no private backfill. | Status/event protocol, cursor reset and recovery display. |
| Audit/rotation/restore failure | Integrity/privacy/controlled recovery constraints remain. | Alert threshold, retry, compensation and completion schema. |

**Source:** [DDS], p. 89, §E.1 requires empty/malformed/adversarial fixtures; component-specific boundaries cited above.  
**Open:** OQ-ERR-005–026 as applicable. No universal “zero records means successful completion” or exit code is confirmed.

## Consistency and Open Questions

### Conflicts and Required Amendments

This specification does not rewrite earlier Markdown files. The following records identify source conflicts, affected requirements, and required controlled amendments.

| Conflict ID | Evidence / issue | Affected identifiers | Required resolution or amendment |
|---|---|---|---|
| CON-ERR-001 | “Snake-case error codes” versus uppercase examples. [DDS], pp. 54, 84, 89. | ERR-001–005; ERR-COM-003; `CON-SCR-012`, `CON-API-009`, `CON-DAT-021`, `CON-BAT-014`, `CON-BR-016`. | Preserve literals; define canonical casing and full per-operation error schemas. |
| CON-ERR-002 | `409` revision semantics coexist with idempotency-conflict test and artifact-binding conflict. [DDS], pp. 54, 83–84, 89. | ERR-001/002/031; API-004/017; BR-006–008/030. | Distinguish each `409` cause/code/details; do not use one generic revision code for all conflicts. |
| CON-ERR-003 | Missing approval terminates; `AWAITING_REVIEW` valid; recoverable timeout absent from state list. [DDS], pp. 12, 41, 45, 49, 82, 90. | ERR-029/030/033; BR-026/031; API-013; DAT-008; BAT-007/009; preceding waiting conflicts. | Resolve execution timeout, valid wait, missing-approval failure and review expiry independently. |
| CON-ERR-004 | Missing citations yield needs-review/unsupported; invalid citations yield `MODEL_OUTPUT_INVALID`. [DDS], pp. 38, 89. | ERR-004/005/025; API failure matrix; BAT-007; BR-019/023. | Specify schema-invalid versus absent/insufficient-evidence distinctions and exact downstream state. |
| CON-ERR-005 | Injection abuse must fail closed, while gateway strips directives and records indicators. [DDS], pp. 13, 39, 61. | ERR-026; BR-005/023; BAT-007; API-036. | Define detection and continuation/termination without weakening fail-closed authority control or assuming every indicator terminates all work. |
| CON-ERR-006 | Lower-trust connector mode versus mandatory ACL/revocation invariant. [DDS], pp. 21–23, 27–29. | ERR-019/036; BR-021/034; BAT-002/006; preceding trust conflicts. | Resolve safe restrictions before unsupported ACL capability is used; no authorization bypass. |
| CON-ERR-007 | Poison record permits remaining batch continuation; cursor requires preceding durable outcomes. [DDS], pp. 28–29, 85. | ERR-020/021; DAT-015/021; BAT-002; BR-035. | Define durable exception accounting, cursor/run-history identity and partial status; no skipped nondurable item. |
| CON-ERR-008 | Unsafe quarantine and viewable low-quality exception are distinct. [DDS], pp. 30–32. | ERR-023/024/039; API-006/007; DAT-022/028; BR-016/018. | Define safe quarantine access; do not approve active-content rendering from low-quality viewing rule. |
| CON-ERR-009 | Code/time/actor/hash fields incomplete in selected data and event catalogs. [DDS], pp. 45, 48, 85–87. | ERR-014/031/040; ERR-OPS-001; DAT-EVT/DAT-012; API-COM-006; preceding attribution conflicts. | Supply schema/carriers and immutable review binding without adopting proposed JSON names. |
| CON-ERR-010 | Read endpoints associated with durable events/work allocation through repeated chapter prose. [DDS], pp. 8–80. | ERR-015/042/048/054; API reads/events; BAT trigger contracts; `UserReviewOpened`. | Specify actual triggers; do not make every GET allocate work or emit business changes. |
| CON-ERR-011 | Alternate run-create endpoints. [DDS], pp. 15–17 versus pp. 12, 40–42, 83. | ERR-017/029/030; API-011/012; BAT-007; BR-024/026. | Resolve canonical/alternate case binding and failure mappings. |
| CON-ERR-012 | Role aliases, Auditor evidence path and global self-approval scope unresolved. [DDS], pp. 11, 22, 45–46, 83, 85, 90. | ERR-007–009/032/045; BR-003/029/039; preceding role conflicts. | Explicit role/action matrix and independent reviewer/approver protocol; no inferred grants or self-approval exception. |
| CON-ERR-013 | Workspace settings associated with case PATCH. [DDS], p. 24. | ERR-011; SCR-007; API-GAP-002; DAT-002; BR-007/010. | Supply true settings API and conflict behavior; do not repurpose case mutation by association. |
| CON-ERR-014 | Close/reopen guards absent while immutable lineage required. [DDS], pp. 25–26, 46. | ERR-010/044/046; API-005; DAT-004/025; BR-014/015/038/041. | Complete close/reopen/rework and retention/deletion lineage interactions without historical overwrite. |
| CON-ERR-015 | Retention/config examples coexist with open corporate/provider selections. [DDS], pp. 66, 90. | ERR-018/029/044/049/052; retry/retention tables; preceding configuration conflicts. | Approve deployment settings/precedence; no universal 180-second timeout, 24-hour ledger, 10% sampling, or approved corporate retention by repetition. |
| CON-ERR-016 | Immutable history and protected receipts versus tenant/workspace purge. [DDS], pp. 26, 51, 62, 80, 85, 89. | ERR-044/046/048/052; DAT-018/025/029; BR-038/041. | Define retained scope, receipt survival, shared sources, backups and historical access. |
| CON-ERR-017 | Exact source/approval identities and hash encodings unresolved; A2A output schema omitted. [DDS], pp. 31, 41, 45, 51, 87. | ERR-025/027/031; API-046; DAT-COM-004; BR-017/027/030. | Formalize identity/hash/schema/decline contracts; examples remain placeholders. |
| CON-ERR-018 | Case-create “within” versus “under” 300 ms; SLO is not timeout. [DDS], pp. 12, 65. | ERR-029/054; BR-046; OQ-API-033/OQ-SCR-031. | Resolve strict measurement boundary separately from request/worker timeout and alert threshold. |
| CON-ERR-019 | Earlier files identify exception specification as future work. | Earlier dependency sections in files 01–05. | Controlled amendments may point to `06_exception_handling.md`; unresolved earlier decisions remain unresolved. No earlier file is rewritten here. |

### Open-Decision Register

All items are **Needs confirmation**. No decision, owner, deadline, approval, or selected implementation is assigned.

| Open ID | Affected requirements | Missing decision / contract | Earlier links and evidence |
|---|---|---|---|
| <a id="oq-err-001"></a>OQ-ERR-001 | Error envelope; ERR-001–011/015/017/031/054 | Full REST/RPC/async status/code/casing/message/`retryable`/safe details; universal requiredness; missing-header and provider mappings. | [`02_api.md`](02_api.md): OQ-API-032; [`01_screen_functions.md`](01_screen_functions.md): OQ-SCR-029; [`05_business_rules.md`](05_business_rules.md): OQ-BR-002. [DDS], pp. 54, 83–84, 89. |
| <a id="oq-err-002"></a>OQ-ERR-002 | ERR-006/010/034/054 | Required input/review fields, reason codes, lengths/types, field-path validation, business versus schema errors and client validation timing. | `02_api.md`: OQ-API-003/007/008/015; [`03_data.md`](03_data.md): OQ-DAT-003/006/016; `05_business_rules.md`: OQ-BR-002/005/018. [DDS], pp. 12, 24–25, 56, 58, 85–86. |
| <a id="oq-err-003"></a>OQ-ERR-003 | ERR-007–009/027/032/045; operational access | Token/session/clock transport; complete role/action/resource/service grants; owner/member/operator/elevated aliases; Auditor path; self/independent approval scope. | `01_screen_functions.md`: OQ-SCR-002/003; `02_api.md`: OQ-API-001/002; `03_data.md`: OQ-DAT-017; [`04_batch_functions.md`](04_batch_functions.md): OQ-BAT-003; `05_business_rules.md`: OQ-BR-001. [DDS], pp. 11, 18–23, 45–46, 83–90. |
| <a id="oq-err-004"></a>OQ-ERR-004 | ERR-001/010/011/040 | Revision/ETag/patch transport, missing precondition, close/reopen guards, config conflict, transaction locks/isolation and UI conflict recovery. | `02_api.md`: OQ-API-005/007/020; `03_data.md`: OQ-DAT-007/014; `05_business_rules.md`: OQ-BR-003/008. [DDS], pp. 24–26, 45, 86. |
| <a id="oq-err-005"></a>OQ-ERR-005 | ERR-002/012/015/040; ERR-COM-007 | Key scope/format/fingerprint, pending simultaneous duplicates, TTL boundaries, rejected outcomes, permission-changed replay and unknown commit response reconstruction. | `02_api.md`: OQ-API-004; `03_data.md`: OQ-DAT-013/014; `04_batch_functions.md`: OQ-BAT-006; `05_business_rules.md`: OQ-BR-003. [DDS], pp. 25, 54, 89–90. |
| <a id="oq-err-006"></a>OQ-ERR-006 | ERR-013/014/037; replay/logging | Event/step ledger atomics, stale/future revision disposition, envelope/signature/schema failures, actor/correlation, poison-event handling, identity-preserving migration and retention. | `02_api.md`: OQ-API-027/035; `03_data.md`: OQ-DAT-013/024; `04_batch_functions.md`: OQ-BAT-005/006/007; `05_business_rules.md`: OQ-BR-022. [DDS], pp. 22, 48–50, 87, 90. |
| <a id="oq-err-007"></a>OQ-ERR-007 | ERR-015/016/005/029/039/043 | Per-dependency timeout, transient taxonomy, retry count/delay/jitter/circuit thresholds, exhaustion, `Retry-After`, unknown external mutable outcome and no-input recovery. | `02_api.md`: OQ-API-013/027–029/032; `04_batch_functions.md`: OQ-BAT-007/009; `05_business_rules.md`: OQ-BR-022. [DDS], pp. 28–29, 38, 42, 49–55. |
| <a id="oq-err-008"></a>OQ-ERR-008 | ERR-005/017/018/026–030 | Canonical run endpoint/revision, admission thresholds/reservations, DAG/call/retry accounting, invalid-plan bound, execution deadline, valid review wait and recoverable timeout/state. | `02_api.md`: OQ-API-012–014; `03_data.md`: OQ-DAT-015/020; `04_batch_functions.md`: OQ-BAT-014; `05_business_rules.md`: OQ-BR-014/015. [DDS], pp. 12–17, 38–42, 49, 69, 82, 90. |
| <a id="oq-err-009"></a>OQ-ERR-009 | ERR-003/019–021 | Connector providers/capabilities/trust restrictions, credentials revoke/reauth, run states, cursor history/order/expiry/claims, partial records, retry/remediation and empty delta. | `02_api.md`: OQ-API-019/034; `03_data.md`: OQ-DAT-019; `04_batch_functions.md`: OQ-BAT-011; `05_business_rules.md`: OQ-BR-021. [DDS], pp. 27–29, 85, 90. |
| <a id="oq-err-010"></a>OQ-ERR-010 | ERR-020/022–024 | File allowlist/transport/MB/equality/decompression/parser limits, scan outages, malformed/unsafe/quality taxonomy, OCR, quality thresholds, state and quarantine access/remediation. | `01_screen_functions.md`: OQ-SCR-009; `02_api.md`: OQ-API-009; `03_data.md`: OQ-DAT-008/010; `04_batch_functions.md`: OQ-BAT-012; `05_business_rules.md`: OQ-BR-009/010. [DDS], pp. 30–32, 82. |
| <a id="oq-err-011"></a>OQ-ERR-011 | ERR-004/005/025/039 | Evidence/Citation/ID/hash/anchor/URL structures, signed access expiry/reissue, missing source, confidence/quality sufficiency, missing citations versus invalid citations and remaining-evidence continuation. | `02_api.md`: OQ-API-010/011/028; `03_data.md`: OQ-DAT-009/011/024; `05_business_rules.md`: OQ-BR-011. [DDS], pp. 31, 35–38, 52, 57, 87, 89. |
| <a id="oq-err-012"></a>OQ-ERR-012 | ERR-011/026/027/030–034 | Policy matrix/version/activation, injection continuation, tool/A2A decline contracts, required review context, pools/roles/SLA/late and concurrent decisions/self-approval/task-open triggers. | `02_api.md`: OQ-API-015/016/020/028/035; `03_data.md`: OQ-DAT-016/021/024; `04_batch_functions.md`: OQ-BAT-015; `05_business_rules.md`: OQ-BR-004/016–019. [DDS], pp. 39, 41, 44–46, 58, 87. |
| <a id="oq-err-013"></a>OQ-ERR-013 | ERR-030/032/035 | Publication/auto-allow trigger, gate projection, approval validity/revocation, multiple decisions, elevated override/secondary reviewer/reason, failed-publication rework and locking. | `02_api.md`: OQ-API-017/018; `03_data.md`: OQ-DAT-016/021; `04_batch_functions.md`: OQ-BAT-015; `05_business_rules.md`: OQ-BR-020. [DDS], pp. 45–46, 58. |
| <a id="oq-err-014"></a>OQ-ERR-014 | ERR-019/025/035–038 | ACL/cache/source-change atomics, in-flight queries/URLs, group mapping, safe degraded/missing-ACL modes, index completeness/recall/coverage/catch-up, containment/reenable and reconciliation bounds. | `02_api.md`: OQ-API-019/031; `03_data.md`: OQ-DAT-011/012/017/019; `04_batch_functions.md`: OQ-BAT-013; `05_business_rules.md`: OQ-BR-011/012/028. [DDS], pp. 27–29, 34, 46, 53, 69, 78–79, 90. |
| <a id="oq-err-015"></a>OQ-ERR-015 | ERR-015/039–041/052 | Transaction/commit/constraint failures, RLS/reset failure, audit participation, object coordination, lost worker heartbeat/ownership/fencing, cross-store compensation and regional mutation safety. | `02_api.md`: OQ-API-005/027; `03_data.md`: OQ-DAT-014; `04_batch_functions.md`: OQ-BAT-004/005/007/023; `05_business_rules.md`: OQ-BR-003/028. [DDS], pp. 19, 40, 45, 49, 52, 70, 86. |
| <a id="oq-err-016"></a>OQ-ERR-016 | ERR-042 | SSE payload/offset/history, cursor gap/expiry, token/permission changes, duplicate/out-of-order handling, end/error protocol and reconnect/display behavior. | `01_screen_functions.md`: OQ-SCR-013; `02_api.md`: OQ-API-014; `03_data.md`: OQ-DAT-024; `05_business_rules.md`: OQ-BR-027. [DDS], pp. 55, 58. |
| <a id="oq-err-017"></a>OQ-ERR-017 | ERR-043 | Webhook URLs/methods/subscriptions/event mapping, signature/age, acknowledgments, retry/deadline/deduplication, terminal delivery and manual redelivery. | `02_api.md`: OQ-API-029; `03_data.md`: OQ-DAT-024; `04_batch_functions.md`: OQ-BAT-025; `05_business_rules.md`: OQ-BR-022. [DDS], p. 55. |
| <a id="oq-err-018"></a>OQ-ERR-018 | ERR-010/044/046/052 | Approved retention/eligibility clocks, holds/races/releases, inventory/receipt/tombstone/partial completion, closed-history/shared-source/audit/actor/backup survival and schedules. | `02_api.md`: OQ-API-024/025/034; `03_data.md`: OQ-DAT-007/018/025; `04_batch_functions.md`: OQ-BAT-016/023; `05_business_rules.md`: OQ-BR-023. [DDS], pp. 26, 51, 66, 80, 85, 89–90. |
| <a id="oq-err-019"></a>OQ-ERR-019 | ERR-045/046 | Independent exit approval protocol/binding/validity, inventory/snapshot, export format/checksums/lifetime, status/download, partial failures/verification and compensation. | `01_screen_functions.md`: OQ-SCR-025; `02_api.md`: OQ-API-024; `03_data.md`: OQ-DAT-018/023; `04_batch_functions.md`: OQ-BAT-021; `05_business_rules.md`: OQ-BR-024. [DDS], pp. 78–80, 83, 88. |
| <a id="oq-err-020"></a>OQ-ERR-020 | ERR-047 | Provisioning launch/status/role/order/completeness, partial-resource compensation/checkpoints, historic windows/overlap/receipts and readiness thresholds. | `02_api.md`: OQ-API-025; `03_data.md`: OQ-DAT-018/019; `04_batch_functions.md`: OQ-BAT-020; `05_business_rules.md`: OQ-BR-025. [DDS], p. 78. |
| <a id="oq-err-021"></a>OQ-ERR-021 | ERR-026/048/049; logging | Audit integrity/hash/export outage recovery, PII/redaction/sensitive diagnostic schema, disclosure incident procedure, vault/rotation failure and reference overlap/rollback. | `02_api.md`: OQ-API-021/034; `03_data.md`: OQ-DAT-016–018/023/025; `04_batch_functions.md`: OQ-BAT-017/024; `05_business_rules.md`: OQ-BR-013/023/030. [DDS], pp. 21, 27, 62–66, 84, 90. |
| <a id="oq-err-022"></a>OQ-ERR-022 | ERR-050/051 | Evaluation/fixture/signature/partial-suite/statistical/domain/result contracts, `SEC-001`–`SEC-012`, build/sign-off/canary thresholds, migration failure/resume and explicit data compensation. | `02_api.md`: OQ-API-023/026/027/030; `03_data.md`: OQ-DAT-022; `04_batch_functions.md`: OQ-BAT-019/022; `05_business_rules.md`: OQ-BR-029. [DDS], pp. 52, 55, 72–76, 88–89. |
| <a id="oq-err-023"></a>OQ-ERR-023 | ERR-018/053 | Token reservation/actual/release/billing grain, daily windows, cost units/formulas, late corrections/refunds/zero input, rollup rerun/partial state and schedules. | `02_api.md`: OQ-API-022; `03_data.md`: OQ-DAT-020; `04_batch_functions.md`: OQ-BAT-018; `05_business_rules.md`: OQ-BR-014/026. [DDS], pp. 38, 65, 85. |
| <a id="oq-err-024"></a>OQ-ERR-024 | ERR-OPS-001–007; all operational outcomes | Log schemas/levels/sampling/retention/access, metric windows/thresholds, notification recipients/channels/routing/escalation/deduplication, operational commands and incident records. | `01_screen_functions.md`: OQ-SCR-027/028; `02_api.md`: OQ-API-031/033; `03_data.md`: OQ-DAT-026; `04_batch_functions.md`: OQ-BAT-008; `05_business_rules.md`: OQ-BR-028. [DDS], pp. 64–70, 79, 87, 90. |
| <a id="oq-err-025"></a>OQ-ERR-025 | ERR-034/042/054; shared displays | Error copy/placement/focus/form retention, retry controls, primary actions/routes, summary/error/null behavior, browsers/localization and generic UI/internal failure handling. | `01_screen_functions.md`: OQ-SCR-001/004/022/029/031; `02_api.md`: OQ-API-036; `03_data.md`: OQ-DAT-026; `05_business_rules.md`: OQ-BR-027. [DDS], pp. 7, 57–59; precise failure UI absent. |
| <a id="oq-err-026"></a>OQ-ERR-026 | ERR-015–018/049/052; configuration/SLOs | Approved providers/regions/deployments/connector grants/corporate retention/key isolation, capacity, availability budget and strict latency/RPO/RTO measurement/recovery activation. | `01_screen_functions.md`: OQ-SCR-030/031; `02_api.md`: OQ-API-033/034; `03_data.md`: OQ-DAT-025; `04_batch_functions.md`: OQ-BAT-026; `05_business_rules.md`: OQ-BR-028/030. [DDS], pp. 10, 19, 65, 68–70, 90. |

### Proposal Status

| Proposal source | Status in this specification |
|---|---|
| `P-SCR-001`–`P-SCR-003` | Remain unapproved screen hierarchy/new-case/control-placement proposals. This specification does not add an error screen, batch console, retry button, modal, or notification surface. |
| `P-API-001` | Remains unapproved token carrier. Authentication-error handling does not select direct Bearer transport over optional BFF cookies. |
| `P-API-002` | Remains unapproved public JSON mapping. Error/result similarity does not confirm those property names or request schemas. |
| New exception-design proposals | None selected. Missing error codes, log levels, retry settings, compensation, notification recipients and recovery controls remain open decisions. |

### Dependencies and Later Handoffs

| Specification/dependency | Required handoff |
|---|---|
| [`01_screen_functions.md`](01_screen_functions.md) | Preserve screen/action/field IDs and proposed-placement status. Resolve safe failure presentation, conflict recovery, source access, progress gaps and exit-operation placement through controlled amendments. |
| [`02_api.md`](02_api.md) | Preserve API/error/event IDs. Complete per-operation REST/RPC/async error mappings, missing interfaces, preconditions, replay and status projections without inventing endpoints from recovery needs. |
| [`03_data.md`](03_data.md) | Preserve tenant predicates, immutable history, exact version/hash relationships, transactional outbox/checkpoint/receipt constraints and wire-versus-storage distinctions. No new error schema/table is selected. |
| [`04_batch_functions.md`](04_batch_functions.md) | Preserve logical BAT IDs, partial outcome/cursor rules, bounded retry/replay, retention eligibility and schedule gaps. Exception handling does not select executable packaging, worker leases or timers. |
| [`05_business_rules.md`](05_business_rules.md) | Preserve BR guards, priorities and open formulas. Failures do not authorize policy bypass, weakened routing, implicit approval, automatic purge or invented calculation defaults. |
| Remaining security/nonfunctional and operational coverage | **To be defined in a later stage.** Complete role/grant/signature/privacy protocols, provider selections, SLO measurements, scheduler/worker realization and protected recovery controls. No later specification is presumed already generated; its filename is not supplied here. |
| Stage 8 architecture-decision consolidation | **To be defined in a later stage.** `08_architecture_decision.md` must consolidate unresolved items only from completed Markdown specifications, linking to `06_exception_handling.md` ERR/OQ/CON identifiers and affected earlier filenames/requirement IDs. This document assigns no invented decision, owner, deadline or approval. |
