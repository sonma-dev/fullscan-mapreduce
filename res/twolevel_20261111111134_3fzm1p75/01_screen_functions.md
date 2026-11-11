# 1. Screen Function Specification

## Scope and Users

### SF-001 — Status, authority and source conventions

**Confirmed.** This specification covers screen functions for OrionDesk AI, document `OD-AI-DDS-001`, release `R1.0`, design revision `1.3`, a controlled fictional reference architecture. No previous specification is available. Specification-assigned `SCR-*` and `SF-*` identifiers below are traceability identifiers, not source identifiers.

All citations refer to **1794353355-OrionDesk_AI_Detailed_Design_Specification.pdf** using its original page numbers. Finding IDs identify supplied evidence. The source states: “All numbers are design assumptions, not measured production performance.” Figures are normative boundary illustrations, not generated implementation artifacts. Representative identities, cases and displayed values remain fictional examples. **Confirmed** means supported for this reference system; **Needs confirmation** means an unresolved implementation contract; **Proposal** is not an approved requirement. No design proposals are selected here. [Source: pp.1–2, cover/Document Map; `screen_functions:r1:c1:f1`, `screen_functions:r1:c1:f3`, `screen_functions:r1:c2:f1`, `screen_functions:r1:c2:f2`]

### SF-002 — Business scope and exclusions

The platform ingests enterprise documents and user-submitted cases, searches permitted knowledge, drafts grounded responses, applies deterministic risk policy, routes uncertain/sensitive recommendations to authorized reviewers, publishes through a satisfied gate, and preserves auditable evidence. Classification, retrieval, generation, policy evaluation, approval and publication are distinct activities; separate records do not require separate screens. [Source: pp.7,11–12, §§2.1–2.2; `screen_functions:r1:c4:f1`, `screen_functions:r1:c11:f1`, `screen_functions:r1:c13:f4`]

| Capability | Status and constraint | Source |
|---|---|---|
| Physical automation; irreversible financial transactions | Out of scope | p.9 §1.2.1; `screen_functions:r1:c7:f1` |
| Foundation-model fine-tuning; unrestricted browsing; agent administrative cloud permissions | Out of scope | p.9 §1.2.1; `screen_functions:r1:c7:f1` |
| Application-hosted GPU inference | Out of scope; model gateway uses external providers | p.19 §4.2.1; `screen_functions:r1:c25:f2` |
| Cross-region active/active mutation; OCR beyond English; customer-managed model weights | Deferred, not R1 features | p.10 §1.3.2; `screen_functions:r1:c8:f5` |
| Recovery deployment | One primary and one warm recovery region; primary persistent writes; snapshot restoration only under incident command | p.19 §4.2.2; `screen_functions:r1:c25:f5` |

### SF-003 — Users, scopes and authorization prerequisites

| User or scope | Confirmed responsibilities/access | Qualification and open permission mapping |
|---|---|---|
| Analyst | Opens cases, examines evidence, requests drafts; case creation, attachment and run-start scopes in Appendix A | Does not automatically own every case or approve its own high-risk recommendations |
| Reviewer | Approves/rejects recommendations; authorized case/run/stream reads; hash-bound decision submission | Policy reviewer pool, minimum role and separation-of-duty predicates apply |
| Workspace Admin | Manages connectors and policy | Mapping to baseline `Admin` needs confirmation |
| Admin | Connector sync, usage, evaluation; export/delete with approver | Not sufficient alone for controlled export/delete |
| Auditor | Immutable evidence, decision metadata, prompt-template digests and access events; immutable cursor audit log | Scope-redacted; cannot edit case content |
| Service | Baseline authorization role for service activity | Not a confirmed browser user or screen permission |
| Owner / Member | Appendix A PATCH/search access scopes | Not established as additional human roles; mapping needs confirmation |
| Operator, Security, SRE, engineering teams | Credential revocation, incident/replay/release duties where described | Operational actors do not establish interactive screens or product roles |

[Source: pp.11–12 §2.1,22 §5.2,27 §7.1.2,62 §17.3.1,73 §20.3.2,83 A.2; `screen_functions:r1:c12:f1`, `screen_functions:r1:c12:f2`, `screen_functions:r1:c12:f3`, `screen_functions:r1:c31:f1`, `screen_functions:r1:c42:f5`, `screen_functions:r1:c104:f1`, `screen_functions:r1:c122:f5`, `screen_functions:r1:c137:f8`, `screen_functions:r1:c137:f15`]

Every request binds an authenticated principal and tenant. Authorization combines role, tenant, workspace membership, case sensitivity, source ACL, action and separation of duties. Apply checks at edge, domain transaction, retrieval, tool dispatch and publication as applicable; hiding or disabling navigation is not authorization. Originating ACL filtering precedes text release to generation. Cross-tenant resource substitution returns the absent-resource not-found response class without disclosing private existence. [Source: pp.21–23 §§5.1–5.3,34 chapter9,89 TST-003; `screen_functions:r1:c29:f1`, `screen_functions:r1:c31:f4`, `screen_functions:r1:c32:f4`, `screen_functions:r1:c53:f2`, `screen_functions:r1:c141:f3`]

Interactive authentication uses authorization-code flow with PKCE. Access tokens contain issuer, audience, expiry, subject and tenant; unexpected algorithms and missing tenancy claims are rejected. Do not store long-lived refresh tokens in browser local storage. Secure `HttpOnly`, `SameSite` BFF cookies are an optional source-supported alternative, not a selected architecture. Login/logout routes, session durations, refresh and expiry displays are **Needs confirmation**. [Source: p.21 §5.1; `screen_functions:r1:c30:f1`, `screen_functions:r1:c30:f5`]

**Self-approval open issue:** own-high-risk self-approval is prohibited. Appendix B also states unqualified “no self approval”; Appendix F example has `self_approval_allowed: false`. Confirm wider scope; the narrow prohibition does not grant lower-risk self-approval. [Source: p.11 §2.1.2,85 B.1,90 configuration; `screen_functions:r1:c12:f2`, `screen_functions:r1:c138:f6`, `screen_functions:r1:c142:f3`]

## Screen Inventory and Navigation

### SF-004 — Confirmed primary screens

The source names eight primary screens. Each must have **one primary action and a clear status summary**; it does not identify each primary action. Purposes below distinguish source-named screens from activity associations. Users are activity-level scope evidence, not a complete screen authorization matrix. For **every screen**, exact display conditions, browser URL, entry route, launch method and navigation origins/destinations remain **Needs confirmation**, except the citation click-through behavior in SF-008. [Source: p.57 §16.1.1; `screen_functions:r1:c96:f1`]

| Screen ID | Source name | Supported purpose/activity association | Users and open mapping | Navigation/launch evidence |
|---|---|---|---|---|
| SCR-001 | Case Queue | Case-list surface; exact queue prioritization/primary action unconfirmed | Screen matrix unconfirmed; case activities use Analyst/Reviewer scope | `GET /v1/cases?cursor=...` is a UI integration reference, not a route |
| SCR-002 | Case Detail | Navigable case workspace; individual case read/edit activities | Authorized Analyst/Reviewer reads; Owner PATCH scope mapping open | Keyboard case opening tested; exact origin and destination mechanics open |
| SCR-003 | Evidence Viewer | Source evidence inspection and citation provenance | Analyst examination/Reviewer inspection; ACL applies | Citation opens source and highlights anchored page range; mapping to this screen/window open |
| SCR-004 | Run Timeline | Human-visible run progress/trace activity | Analyst/Reviewer status and SSE reads | Run creation/progress/refresh supported; launch control and final navigation open |
| SCR-005 | Review Inbox | Recommendation review activity | Reviewer pool/role/separation rules | Review queue and decision APIs supported; queue-to-task navigation open |
| SCR-006 | Connector Health | Connector synchronization/health activity | Admin sync scope; Workspace Admin terminology open | Sync/status UI mappings and controls open |
| SCR-007 | Policy Settings | Policy administration activity | Workspace Admin responsibility; detailed predicate open | No confirmed policy-edit endpoint or setting widgets |
| SCR-008 | Audit Explorer | Immutable audit/evidence exploration activity | Auditor scope-redacted access; operator queries separately constrained | Cursor audit API; filters, row detail and export mapping open |

[Additional source: pp.57–59 §§16.1–16.2,83 A.2,89 TST-011; `screen_functions:r1:c95:f1`, `screen_functions:r1:c96:f3`, `screen_functions:r1:c96:f6`, `screen_functions:r1:c97:f1`, `screen_functions:r1:c137:f7`, `screen_functions:r1:c137:f8`, `screen_functions:r1:c137:f11`, `screen_functions:r1:c137:f12`, `screen_functions:r1:c137:f13`, `screen_functions:r1:c137:f14`, `screen_functions:r1:c137:f16`, `screen_functions:r1:c141:f11`]

`ViewState`, `ReviewForm`, `EvidencePanel` and `Notification` are logical components, not four additional screens. The same restriction applies to services, entities, events and runbooks throughout the source. [Source: pp.57,59 Figures16.1/§16.4; `screen_functions:r1:c95:f3`, `screen_functions:r1:c99:f1`]

### SF-005 — Representative navigation and naming discrepancies

Representative console sidebar order is: `Overview`, `Case Queue`, `Case Detail`, `Evidence Viewer`, `Agent Runs`, `Review Inbox`, `Connectors`, `Audit Events`, `Usage & Quality`. This is visual inventory evidence only. Do not silently map `Agent Runs` to Run Timeline, `Connectors` to Connector Health, `Audit Events` to Audit Explorer, or approve Overview/Usage & Quality as separate primary screens. [Source: p.7 Reference UI A and pp.14,33,43,47,60,67,77,81 figures; `screen_functions:r1:c4:f8`, `screen_functions:r1:c100:f7`]

| Original location | Visible main title | Selected sidebar | Status |
|---|---|---|---|
| p.7 Reference UI A | Case Detail / Resolution Package | Case Queue | Unresolved |
| p.14 Figure2.2 | Case Queue / Risk Prioritization | Overview | Unresolved |
| p.33 Figure8.2 | Case Detail / Resolution Package | Case Queue | Unresolved |
| p.43 Figure11.2 | Evidence Explorer / Citation Audit | Case Detail | Unresolved |
| p.47 Figure12.2 | Agent Run / Execution Trace | Evidence Viewer | Unresolved |
| p.60 Figure16.2 | Approval Inbox / Binding Decision | Agent Runs | Unresolved |
| p.67 Figure18.2 | Connector Health / Synchronization | Review Inbox | Unresolved |
| p.77 Figure21.2 | Audit Explorer / Event Lineage | Connectors | Unresolved |
| p.81 Figure22.2 | AI Quality / Evaluation Scorecard | Audit Events | Unresolved |

[Source findings respectively: `screen_functions:r1:c4:f7`, `screen_functions:r1:c16:f4`, `screen_functions:r1:c52:f5`, `screen_functions:r1:c70:f4`, `screen_functions:r1:c70:f5`, `screen_functions:r1:c76:f4`, `screen_functions:r1:c76:f5`, `screen_functions:r1:c100:f6`, `screen_functions:r1:c100:f7`, `screen_functions:r1:c112:f4`, `screen_functions:r1:c112:f5`, `screen_functions:r1:c130:f4`, `screen_functions:r1:c130:f5`, `screen_functions:r1:c136:f4`, `screen_functions:r1:c136:f5`]

A repeated selected-item discrepancy is not proof of aliasing. Confirm routing, composite panels and necessary source amendments before implementing navigation.

## Functions by Screen

### SF-006 — Shared field-definition and interaction rules

For each field below, **all attributes not explicitly stated are Needs confirmation**: UI type, length, format, requiredness, initial value, editability, input constraints, validation timing, conditional visibility and selectable-value/data source. Domain persistence types, API types and mockup formatting are labeled separately and must not be copied into UI contracts indiscriminately. No arbitrary field defaults, numeric limits, error copy or recovery flow is authorized by an omission.

Server validation occurs before transaction entry, again at domain invariants, and before tool dispatch. Endpoint-specific validation precedes allocation of long-running work. Client validation is convenience only. On unavailable dependencies, generic source contracts allow a documented retryable error **or** persisted asynchronous job identifier, never ambiguous success; selection conditions and shapes are open. GET wording does not establish universal job creation. [Source: pp.54–56 §§15.1–15.3; `screen_functions:r1:c92:f4`, `screen_functions:r1:c90:f3`, `screen_functions:r1:c90:f7`]

Each actual durable-state-changing boundary record carries `tenant_id`, `revision`, `actor_id`, `occurred_at` and a correlation ID under the source's condition “wherever the operation changes durable state.” General tenant/actor boundary context remains required. These are not editable browser fields. Canonical event fields are separately `event_id`, `type`, `schema_version`, `tenant_id`, `aggregate_id`, `aggregate_revision`, `occurred_at`, `trace_id`, `payload`, using UTC/canonical JSON; aliases between the lists are not supplied. [Source: p.48 §13.1 and pp.57–59; `screen_functions:r1:c78:f1`, `screen_functions:r1:c96:f2`, `screen_functions:r1:c97:f4`, `screen_functions:r1:c98:f7`]

### SF-007 — SCR-001 Case Queue and SCR-002 Case Detail

| Field/activity | Meaning and supported behavior | Type/default/editability qualification | Source |
|---|---|---|---|
| Case identifier | Authorized current case reference | UUIDv7 persistence convention; fictional `OD-2026-*` labels do not define input pattern | pp.51,83; `screen_functions:r1:c84:f1`, `screen_functions:r1:c137:f7` |
| Title, description | Case metadata | UI constraints/requiredness/default/editability open | p.24 §6.1.2; `screen_functions:r1:c36:f3` |
| Attachments, business context | Received by new cases before policy-aware classification | Exact input surface and requiredness open | p.12 §2.2.1; `screen_functions:r1:c13:f1` |
| Labels, confidences, provenance | Asynchronous classification outputs | User may correct labels **with reason code**; actor and catalog open | p.12 §2.2.1; `screen_functions:r1:c13:f1` |
| Impact, urgency, priority | Priority derives from explicit impact and urgency, never model output alone | Formula/domains/direct editability open | p.25 §6.3.1; `screen_functions:r1:c38:f1` |
| Sensitivity | Case classification used in policy/authorization | Data classes PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED; storage default INTERNAL is not a form default | pp.62,86; `screen_functions:r1:c103:f1`, `screen_functions:r1:c138:f11` |
| Status, owner, current approved result, revision | Revision-controlled case metadata | No assumption of editable status/owner or result; revision is monotonic | p.24 §6.1.2; `screen_functions:r1:c36:f3` |
| Deadline, breach prediction | Workspace-timezone business calendars set deadlines; predictions are advisory | Prediction cannot change contractual deadline; formats/calendar setup open | p.25 §6.3.1; `screen_functions:r1:c38:f2` |

**Case/list behavior.** `GET /v1/cases?cursor=...` is supported; public APIs use cursor pagination. List columns, default ordering, user sorting, search/filter controls, cursor format, page size and row activation remain open. No mockup row count is a pagination limit. [Source: pp.54,57–59; `screen_functions:r1:c90:f1`, `screen_functions:r1:c96:f3`, `screen_functions:r1:c99:f6`]

**Creation procedure:**
1. An authorized Analyst submits a valid case request through the still-unmapped creation interaction.
2. The server validates before long-running allocation and applies idempotency.
3. A successful reference creation returns `201` and a case identifier; the case begins `NEW`.
4. Classification asynchronously supplies labels/confidences/provenance; correction requires a reason code.

Successful screen display/navigation and failure copy remain **Needs confirmation**. Same-key duplicate creation has one case and identical response; changed-body reuse returns `409 IDEMPOTENCY_CONFLICT`. [Source: pp.12,83,89; `screen_functions:r1:c13:f1`, `screen_functions:r1:c137:f6`, `screen_functions:r1:c141:f1`, `screen_functions:r1:c141:f2`]

**Update/concurrency:** Clients submit `If-Match`; conflict returns `CASE_VERSION_CONFLICT` with current revision and leaves business state unchanged. Actor/request-fingerprint idempotency maps one outcome for **24 hours**; key generation/transport, fingerprint definition and expiry handling are open. Do not automatically retry permanent validation/permission failures. [Source: p.25 §6.2.2,49 §13.3.1,84 A.3; `screen_functions:r1:c37:f3`, `screen_functions:r1:c37:f6`, `screen_functions:r1:c80:f1`, `screen_functions:r1:c137:f21`]

| Case transition | Confirmed rule |
|---|---|
| NEW → TRIAGED | Supported |
| TRIAGED → IN_PROGRESS | Supported |
| IN_PROGRESS → PENDING_APPROVAL or RESOLVED | Supported |
| PENDING_APPROVAL → RESOLVED or IN_PROGRESS | Supported |
| CLOSED | Final **unless explicitly reopened as a new revision** |

Role, revision and approval guards apply. Transition into CLOSED, permitted closing actor, reopening status/action/API and navigation are open. Closure snapshots approved answer, cited document versions and reviewer decisions; immutable approved-output lineage must survive closure. Retention jobs apply only to eligible closed cases with legal-hold exceptions. [Source: pp.25–26,82; `screen_functions:r1:c37:f1`, `screen_functions:r1:c38:f6`, `screen_functions:r1:c38:f7`, `screen_functions:r1:c137:f2`]

### SF-008 — SCR-003 Evidence Viewer and attachment/evidence activity

| Field or artifact | Confirmed content | Constraints/visibility qualification | Source |
|---|---|---|---|
| Uploaded file | R1 PDF, DOCX, HTML, UTF-8 text | MIME signature/extension agree; configurable **25 MB per file**; decompression-bomb threshold unspecified | p.30 §8.1.1; `screen_functions:r1:c48:f1` |
| Source document/version | Immutable source/version provenance | Authorized access only; not mutable latest-content substitution | pp.31,51; `screen_functions:r1:c50:f1`, `screen_functions:r1:c84:f4` |
| Chunk anchor | Source URI, file hash, page number, optional bbox | Resolvable anchor and current permission needed for generation citations | p.31 §8.3.1; `screen_functions:r1:c50:f1` |
| PDF layout/table data | Page index/bbox, rows/columns, heading/reading order | Block bbox and optional chunk bbox have different granularity | p.31 §8.2.1; `screen_functions:r1:c49:f1` |
| Evidence item | Chunk ID, source title, document revision, page anchor, ACL digest | API inclusion does not mandate every field's visible rendering; identifiers verified before display | p.35 §9.3.1; `screen_functions:r1:c56:f1` |
| Extraction quality | Empty-page ratio, unknown-character ratio, table-loss indicators, language confidence | Thresholds/flag presentation open; low quality remains viewable but excluded from autonomous recommendations | p.32 §8.3.2; `screen_functions:r1:c50:f4` |
| OCR provenance | Opt-in fallback, provenance-marked | Actor/control/timing/marker open; OCR beyond English deferred | pp.10,31; `screen_functions:r1:c8:f5`, `screen_functions:r1:c49:f2` |

**Upload processing:** Scan before parsing; disable macros; do not fetch embedded remote references. Unsafe attachments quarantine without entering search. A `202` attachment response creates ingestion work, not proof of READY. Document catalog states are `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED`, guarded by scan and quality. Upload/status screen location, transitions, remediation and error displays are open. [Source: pp.30–31,82–83,89 TST-015; `screen_functions:r1:c48:f4`, `screen_functions:r1:c137:f4`, `screen_functions:r1:c137:f9`, `screen_functions:r1:c141:f15`]

**Citation click-through:**
1. User activates an available citation.
2. Open the source document and highlight the anchored page range.
3. Preserve exact version provenance and authorization.

Destination screen/window, missing/revoked source errors, bbox rendering, page conventions and recovery remain open. Reviewers must be able to inspect source evidence **before approval**; actual recorded inspection completion is not required by supplied evidence. Access-controlled short-lived signed URLs and encryption are mandatory, but URL lifetime/expiry UX is not specified. [Source: pp.52,57–58; `screen_functions:r1:c86:f1`, `screen_functions:r1:c95:f2`, `screen_functions:r1:c96:f6`, `screen_functions:r1:c97:f2`]

**Search:** Apply lexical and normalized vector retrieval, bounded candidates, reciprocal rank fusion, deterministic reranking, source diversity and per-query model-token budgets. Ranking is not authorization. Revoked source access must be effective **before next retrieval**, even while index cleanup is pending; source ACL changes invalidate affected cache before new results. Query fields, search placement, blank-query behavior, filtering and sorting remain open. If confidence/quality is insufficient, return `NO_SUPPORTED_EVIDENCE`, not fabricated context; clarification versus human routing needs a decision. Missing-citation generation has needs-review **or** unsupported outcome under TST-009, not a selected universal state. [Source: pp.27–29,34–36,89; `screen_functions:r1:c41:f2`, `screen_functions:r1:c43:f4`, `screen_functions:r1:c55:f1`, `screen_functions:r1:c55:f4`, `screen_functions:r1:c56:f4`, `screen_functions:r1:c141:f4`, `screen_functions:r1:c141:f9`]

Normalization cannot rewrite source claims. Content fingerprint/pipeline version identifies immutable derivatives; changed normalization can coexist side by side. No comparison/reprocess control is specified. [Source: p.31 §8.2.2; `screen_functions:r1:c49:f5`]

### SF-009 — SCR-004 Run Timeline, drafting and tool activity

| Display/input | Confirmed definition | Open attributes |
|---|---|---|
| Run progress | Retrieval, generation and policy stages via SSE; human-visible execution traces | Stage-to-widget mapping, step fields and refresh cadence |
| Failed checkpoint | Exact checkpoint that caused termination | Error copy/state and next action |
| Draft label | Accessible `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` text | Mapping to case/run/review state |
| Candidate/model/prompt/policy provenance | Exact candidate/citations/model-prompt version/policy reasons for review | Timeline display of all versions, formatting and hashes |
| Token/cost budget | Run reserves input/output tokens, tracks provider usage under workspace quota | Budget input/editability/units/admission limits |

[Source: pp.38–42,57–58; `screen_functions:r1:c62:f1`, `screen_functions:r1:c65:f1`, `screen_functions:r1:c68:f1`, `screen_functions:r1:c96:f5`, `screen_functions:r1:c97:f1`, `screen_functions:r1:c97:f2`]

**Run procedure:**
1. Authorized Analyst requests a bounded workflow. The launch control and the relationship of `POST /v1/runs` to `POST /v1/cases/{caseId}/runs` are unresolved.
2. A run is created immediately; case-scoped reference acceptance returns `202`, not a completed or approved answer.
3. Subscribe to authorized SSE. Offsets increase monotonically; reconnect sends `Last-Event-ID` and backfills retained caller-scoped events.
4. Page refresh reconstructs progress from server state, not ephemeral browser memory.
5. Show meaningful state transitions; do not represent partial processing as approved output.

Expired-event history recovery, cancellation, resumability, connection errors and final navigation remain open. [Source: pp.15,40,55,58,83; `screen_functions:r1:c17:f3`, `screen_functions:r1:c66:f2`, `screen_functions:r1:c91:f1`, `screen_functions:r1:c97:f1`, `screen_functions:r1:c137:f10`, `screen_functions:r1:c137:f12`]

Run catalog: `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED`; checkpoints precede downstream dispatch. Chapter11 terminates on missing approval, budget exhaustion, repeated invalid plans, policy denial or deadline; chapter2 permits recoverable timeout. **Needs confirmation:** distinguish ordinary review waiting from absent authorization and map timeout/quota/deadline to durable status. Do not select that distinction implicitly. [Source: pp.12,41,49,82; `screen_functions:r1:c14:f2`, `screen_functions:r1:c68:f1`, `screen_functions:r1:c79:f1`, `screen_functions:r1:c137:f3`]

Planner DAG depth is **8**, maximum tool invocations **16**, explicit dependencies/replayable checkpoints, with stored plan revision before side effects. Triage, Research and Draft are bounded AI responsibilities; Policy Evaluator is deterministic. Browser-supplied arbitrary tool definitions are prohibited. Discovery and model text never confer action authority. Pinned approved MCP schemas validate arguments; external writes need separate capability permission; mutable operations need idempotency and, when consequential, human authorization. A denied action cannot be replaced by a semantically equivalent tool. [Source: pp.7,40–42; `screen_functions:r1:c4:f2`, `screen_functions:r1:c4:f4`, `screen_functions:r1:c66:f1`, `screen_functions:r1:c66:f4`, `screen_functions:r1:c67:f1`, `screen_functions:r1:c67:f4`, `screen_functions:r1:c68:f4`]

`knowledge.search@v1` is read-only, requires tenant-scoped `read:permitted_documents`, accepts `{query: string, case_id: uuid, max_items: int<=10}`, returns `{evidence_set_id: uuid, citations: Citation[]}`, and prohibits arbitrary URLs/filesystem access. This is a tool contract, not an editable form or page-size contract. A2A declares task/capability/input-output schema/deadline/trace and may decline; its example `case_demo` and absent output-schema field do not establish typed exceptions. [Source: pp.41,87 C.2; `screen_functions:r1:c67:f4`, `screen_functions:r1:c139:f9`, `screen_functions:r1:c139:f10`, `screen_functions:r1:c139:f11`, `screen_functions:r1:c139:f12`]

Structured model parsing uses versioned JSON and bounded retries; unknown fields, invalid citations or control-character injection cause `MODEL_OUTPUT_INVALID` and no publication. Quota exhaustion is terminal for the current run, without automatic model/data-class changes. Fallback only uses approved equal-or-stronger data-handling class and approved region/deployment. Retry bounds and failure recovery remain open. [Source: pp.37–39,89; `screen_functions:r1:c60:f4`, `screen_functions:r1:c61:f4`, `screen_functions:r1:c62:f1`, `screen_functions:r1:c141:f5`]

### SF-010 — SCR-005 Review Inbox and publication

| Field/control | Confirmed meaning/rule | Requiredness, values and editing |
|---|---|---|
| Exact candidate artifact | Content under review, not a different/latest draft | Display required; hash representation/rendering open |
| Citations | Review source evidence | Display/inspection available; source constraints SF-008 |
| Model/prompt version | Provenance of candidate | Display required; exact identifier format open |
| Policy reasons | Deterministic justification | Display required; formatting open |
| Decision record | Decision, actor, timestamp, evaluated artifact hash, rationale | Record contents confirmed; input options/types/required fields open |
| Annotations | Additional review notes | Explicitly optional in record; UI limits open |
| Approve / Reject | Recommendation decision actions | **Disabled until required review fields complete**; unnamed fields and additional enablement gates open |
| Override reason | Audited reason for elevated override | Required by override rule; format/control open |

[Source: pp.45–46,58; `screen_functions:r1:c73:f4`, `screen_functions:r1:c74:f4`, `screen_functions:r1:c97:f2`, `screen_functions:r1:c97:f3`]

**Decision procedure:**
1. Determine reviewer eligibility from policy pool, minimum role and separation of duties; source inspection must be available.
2. Show exact artifact/citations/model-prompt version/policy reasons.
3. Keep Approve and Reject disabled while required review fields are incomplete. Completion does not replace authorization.
4. Submit a hash-bound decision through `POST /v1/approvals/{approvalId}/decision`.
5. Reject changed/wrong-hash or unauthorized decisions, preserve business state and audit stale denial; reference result is `200 / 409`.

Successful decision display/navigation, detailed rejection reason choices, editing workflow and error copy are open. [Source: pp.45,58,83,89; `screen_functions:r1:c73:f1`, `screen_functions:r1:c73:f8`, `screen_functions:r1:c97:f3`, `screen_functions:r1:c137:f13`, `screen_functions:r1:c141:f6`]

Review states: `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED`, guarded by actor/hash/separation. Configured-SLA expiry reassigns or escalates without silent approval; TST-010 requires escalation recorded. Confirm SLA, recipients and when each alternative applies. Denied recommendations may be reworked as **new run revisions**, never retroactively approved. Overrides require elevated role, secondary reviewer and audited reason; exact roles/independence/applicability remain open. [Source: pp.45–46,82,89; `screen_functions:r1:c73:f1`, `screen_functions:r1:c74:f4`, `screen_functions:r1:c137:f5`, `screen_functions:r1:c141:f10`]

**Publication is distinct from approval.** Required evidence and satisfied versioned deterministic policy are prerequisites; unapproved high-risk runs cannot publish. Approval binds exactly reviewed content. Final-response pointer and satisfied gate commit atomically; replay cannot publish another artifact under old approval. Recompute authorization at publication after intervening tenant/document permission changes; reject stale evidence even after successful search/review. Publication invoker, endpoint/button, exact status mapping and recovery are open. [Source: pp.7,11–12,45–46,59; `screen_functions:r1:c4:f3`, `screen_functions:r1:c11:f2`, `screen_functions:r1:c13:f4`, `screen_functions:r1:c74:f1`, `screen_functions:r1:c76:f2`, `screen_functions:r1:c100:f2`]

### SF-011 — SCR-006 Connector Health

| Activity/data | Confirmed behavior | Missing UI contract |
|---|---|---|
| Capabilities | Advertise list/fetch/delta cursor/ACL/delete | Provider values/widgets unspecified |
| Unsupported capability | Lower-trust ingestion with explicit visible warning | Warning text/acknowledgment/restrictions unspecified; no ACL bypass |
| Sync | Admin starts incremental sync;202 accepted operation | Launch/status/list/primary action unspecified |
| Cursor/high-watermark/error ledger | Advance only after durable preceding outcomes | Columns, formats, reset/retry permissions unspecified |
| Credentials | Workspace vault references; queued revoked jobs fail `CONNECTOR_REAUTH_REQUIRED` without tokens | Reauth/revocation control and running-job behavior open |
| Quarantine | Bounded-retry malformed item has reason/correlation/remediation; ledger exception permits batch continuation | Retry bound, reason catalog, remediation/release UI open |

[Source: pp.27–29,83; `screen_functions:r1:c42:f1`, `screen_functions:r1:c42:f5`, `screen_functions:r1:c43:f1`, `screen_functions:r1:c44:f4`, `screen_functions:r1:c137:f14`]

Workers honor `Retry-After`, backoff/jitter, workspace quotas and fair scheduling. Deleted source tombstones schedule index removal; ACL invalidation occurs before serving new results. Incomplete provisioning is visible and blocks sync. Historic ingestion readiness uses index coverage, not queue emptiness. Schedules, quotas, coverage threshold and successful/failure navigation are open. [Source: pp.28,78; `screen_functions:r1:c43:f4`, `screen_functions:r1:c44:f1`, `screen_functions:r1:c132:f1`, `screen_functions:r1:c132:f2`]

### SF-012 — SCR-007 Policy Settings

| Setting/input family | Supported definition | Open UI attributes |
|---|---|---|
| Workspace settings | Retention class, allowed deployments, credential references, approved toolsets, reviewer routing | Widget/type/options/required/default/edit authority |
| Workspace calendar/timezone | Determines business deadlines/local display | Selection/control/source and calendar definitions |
| Policy inputs | Sensitivity, requested action, evidence quality, model class, financial impact category, confidence bands | Stored normalized with rule-set version; not necessarily editable here |
| Outcomes | `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY` | Deterministic; displayed next actions and outcome-to-lifecycle mapping open |
| Classification | Maximum included PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED class controls route/redaction/retention/approval | Assignment/conflict/default/override policies open |

Configuration updates need revision preconditions and durable audit. Models whitelist specific approved deployments, not brands. High-impact recommendations create review tasks rather than autonomous mutations; model tags cannot override policy. No confirmed policy-save endpoint/control or quota editor exists. [Source: pp.24,37,44–45,62; `screen_functions:r1:c36:f1`, `screen_functions:r1:c60:f1`, `screen_functions:r1:c72:f1`, `screen_functions:r1:c72:f5`, `screen_functions:r1:c103:f1`]

Do not promote AppendixF policy examples (`auto_publish_classification: INTERNAL`, `require_human_review_for: [HIGH_RISK, RESTRICTED]`, `self_approval_allowed: false`) into a complete selected policy or unconditional INTERNAL publication permission. [Source: p.90; `screen_functions:r1:c142:f3`]

### SF-013 — SCR-008 Audit Explorer and controlled data exit

Audit content is immutable/append-only, batch-hash chained and independently retained. Auditors see redacted scope-appropriate evidence/decision metadata/template digests/access events; operators may query, not alter historical review decisions. `GET /v1/audit/events` returns an immutable cursor log under Auditor scope. Columns, filters, sort, page sizes, detail navigation and hash-verification UI remain open. [Source: pp.11,62,83; `screen_functions:r1:c12:f3`, `screen_functions:r1:c104:f1`, `screen_functions:r1:c137:f16`]

Diagnostics contain identifiers/policy outcomes, token counts/digests by default, not documents or API secrets. Public responses and errors exclude credentials, full prompts, retrieved documents and private resource existence. PII redaction is policy-conditional, not authority to weaken those prohibitions. [Source: pp.54,62,64,84; `screen_functions:r1:c89:f2`, `screen_functions:r1:c103:f5`, `screen_functions:r1:c108:f1`, `screen_functions:r1:c137:f22`]

**Export/delete are supported activities with unresolved screen mapping**, not automatically Audit Explorer buttons:
1. Apply `Admin + approver` scope and two independent approval checks.
2. For export, require **two-person approval plus manifest**; a single Admin fails. Package case metadata, approved artifacts, source references and checksum audit manifests, excluding secrets/internal prompts.
3. For deletion, enforce legal holds, tombstones, blob/index removal and completion receipts. Protected held records are retained and receipted.
4. `202` means accepted work, not completed export/purge. Confirm package/checksum/receipt schemas, download/status controls, approval identities/timing and partial-failure recovery.

[Source: pp.78–80,83,88–89; `screen_functions:r1:c131:f1`, `screen_functions:r1:c134:f1`, `screen_functions:r1:c134:f5`, `screen_functions:r1:c137:f19`, `screen_functions:r1:c137:f20`, `screen_functions:r1:c140:f11`, `screen_functions:r1:c141:f13`]

Diagnostic retention is **30-day default TTL**; security audit follows a distinct **seven-year fictional policy**, with legal-hold exceptions/completion receipts. Corporate retention remains unselected. Eligible closed-case retention and immutable-lineage interaction require definition. [Source: pp.26,66,90; `screen_functions:r1:c38:f7`, `screen_functions:r1:c110:f5`, `screen_functions:r1:c142:f5`, `screen_functions:r1:c142:f9`]

### SF-014 — Unmapped usage, evaluation and operational functions

These requirements remain in scope as affected activities, **without inventing screens**:

| Activity | Confirmed behavior | UI mapping/open details |
|---|---|---|
| Usage | Admin costs/quotas/trends; workspace cost centers/deployment versions; daily budget/forecast/rejected excess rollups | Usage & Quality screen status, units, charts, refresh and budget editing open |
| Evaluation | Admin frozen benchmark start;1200 synthetic permission-controlled cases; expected citations/outcomes; precision≥0.97, unsupported claims≤0.02, high-risk recall1.00 | Launch/report/export UI, confidence method/domains and threshold open |
| Degraded admission | Token/queue/provider thresholds;429 plus Retry-After; saved cases available | Values, message and client retry controls open |
| Generation outage | Preserve manual editing/evidence search; disable new generation admission and show degraded status | Placement/clearance/navigation open |
| Vector degradation | May continue lexical retrieval **with visible reduced-quality flag** | Optional fallback selection and flag/accessibility detail open |
| ACL incident | Suspend affected aliases, revoke cached evidence, preserve audit, scoped ACL replay; search restoration only after negative tests | Operator role/control/status undefined |
| Dead-letter recovery | Operator reason, dry-run validation, scope bound; original identity except schema-migration provenance exception | No replay screen; migration/link/limits open |
| Delayed indexing runbook | Detect tenant/generation, pause only faulty connector/shard, preserve accepted sources, diagnose event/outbox/parser/throttling/ACL, replay validated bounded work, compare fingerprints/denied probes, link incident evidence | No incident screen; operators/thresholds/receipts open |
| Release/configuration | Reconstruct image/schema/prompt/model-policy provenance; signed evidence; traffic rollback not DB down-migration; Security/SRE sign-off | No release screen or product approval mapping |

[Source: pp.49–50,65,69,73,75–76,79,83,90; `screen_functions:r1:c80:f4`, `screen_functions:r1:c110:f1`, `screen_functions:r1:c115:f1`, `screen_functions:r1:c115:f3`, `screen_functions:r1:c122:f1`, `screen_functions:r1:c122:f5`, `screen_functions:r1:c127:f1`, `screen_functions:r1:c127:f4`, `screen_functions:r1:c133:f1`, `screen_functions:r1:c133:f4`, `screen_functions:r1:c137:f17`, `screen_functions:r1:c137:f18`, `screen_functions:r1:c142:f6`, `screen_functions:r1:c142:f7`, `screen_functions:r1:c142:f8`]

Degraded/recovered operation never bypasses authorization or approval. Valid transient faults use bounded retries/jitter/circuit breakers; permanent validation/permission failures do not retry. Failed indexing does not roll back accepted source metadata. [Source: pp.49,68–70; `screen_functions:r1:c79:f5`, `screen_functions:r1:c80:f1`, `screen_functions:r1:c113:f2`]

### SF-015 — Shared accessibility, localization and representative displays

All relevant controls target **WCAG 2.2 AA**, visible focus, semantic regions and robust keyboard order. Accessible text—not color/styling alone—expresses draft state. Live updates announce only meaningful state transitions to avoid screen-reader noise. Server UTC values display as workspace-local times with timezone labels; locale changes display only, not ordering or durable API representation. API timestamps remain RFC3339. Responsive layout, number formatting, locale choices, focus destinations and announcement inventory are **Needs confirmation**. [Source: pp.54,57–59,89; `screen_functions:r1:c90:f1`, `screen_functions:r1:c96:f5`, `screen_functions:r1:c98:f1`, `screen_functions:r1:c98:f2`, `screen_functions:r1:c98:f6`, `screen_functions:r1:c141:f11`]

Representative figures share header `ORIONDESK / OPERATIONS CONSOLE`, badge `fictional tenant / R1.0`, and workspace subtitle `Workspace: Meridian Manufacturing / All identifiers and data are fictitious`. The following fields/values are **confirmed depictions only**, not defaults, limits, calculations or complete state enums:

| Panel | Visible fields and fictional values |
|---|---|
| Summary cards | `OPEN CASES = 128`; `AWAITING REVIEW = 14`; `EVIDENCE COVERAGE = 97.6%`; `SERVICE STATE = Healthy` |
| CASE EVIDENCE & WORKFLOW | `OD-2026-1042 / Supply chain response discrepancy / Needs review`; `OD-2026-1041 / Batch quality deviation / In progress`; `OD-2026-1040 / Service contract inquiry / Published`; `OD-2026-1039 / Customs document mismatch / Evidence gap`; `OD-2026-1038 / Supplier invoice reconciliation / Triaged` |
| DECISION GATE | `POLICY = HUMAN_REVIEW`; `EVIDENCE = 5 verified citations`; `MODEL = gateway-r1.2`; `APPROVAL = Assigned to reviewer`; `STATUS = Awaiting decision` |

Page7 uses **Service contract inquiry**, while later supplied figure excerpts use **Service contract inquiry**. Preserve each original example wording; no business meaning is assigned to the difference. Sample case lists lack supplied column headers/action/sort/page contracts; panels do not establish approval buttons. All formal field attributes and data sources remain open. [Source: p.7 and pp.14,33,43,47,60,67,77,81; `screen_functions:r1:c4:f9`, `screen_functions:r1:c4:f10`, `screen_functions:r1:c4:f11`, `screen_functions:r1:c16:f7`, `screen_functions:r1:c52:f8`, `screen_functions:r1:c70:f7`, `screen_functions:r1:c76:f7`, `screen_functions:r1:c100:f8`, `screen_functions:r1:c100:f9`, `screen_functions:r1:c100:f10`, `screen_functions:r1:c112:f7`, `screen_functions:r1:c130:f7`, `screen_functions:r1:c136:f7`]

## Integrations and Acceptance Criteria

### SF-016 — Public integration inventory

Endpoint references are not browser routes. Scopes are necessary resource authorization evidence; apply SF-003 and operation-specific conditions in addition. Detailed OpenAPI/data contracts are **To be defined in a later stage** from repository-controlled IDL, not inferred from examples.

| Method/path | Source scope | Reference result/output | Source |
|---|---|---|---|
| POST `/v1/cases` | Analyst |201; idempotent case | p.83 A.2; `screen_functions:r1:c137:f6` |
| GET `/v1/cases/{caseId}` | Analyst / Reviewer |200; authorized current revision | p.83; `screen_functions:r1:c137:f7` |
| PATCH `/v1/cases/{caseId}` | Owner, mapping open |200/409; If-Match mutation | p.83; `screen_functions:r1:c137:f8` |
| POST `/v1/cases/{caseId}/attachments` | Analyst |202; ingestion operation | p.83; `screen_functions:r1:c137:f9` |
| POST `/v1/cases/{caseId}/runs` | Analyst |202; bounded workflow | p.83; `screen_functions:r1:c137:f10` |
| GET `/v1/runs/{runId}` | Analyst / Reviewer |200; stages/evidence metadata | p.83; `screen_functions:r1:c137:f11` |
| GET `/v1/streams/runs/{runId}` | Analyst / Reviewer |200 SSE; Last-Event-ID | p.83; `screen_functions:r1:c137:f12` |
| POST `/v1/approvals/{approvalId}/decision` | Reviewer |200/409; reviewed-hash binding | p.83; `screen_functions:r1:c137:f13` |
| POST `/v1/connectors/{connectorId}/sync` | Admin |202; incremental sync | p.83; `screen_functions:r1:c137:f14` |
| POST `/v1/search` | Member, mapping open |200; lexical/semantic ACL evidence | p.83; `screen_functions:r1:c137:f15` |
| GET `/v1/audit/events` | Auditor |200; immutable cursor log | p.83; `screen_functions:r1:c137:f16` |
| GET `/v1/usage` | Admin |200; costs/quotas/trends | p.83; `screen_functions:r1:c137:f17` |
| POST `/v1/evaluations` | Admin |202; frozen benchmark | p.83; `screen_functions:r1:c137:f18` |
| POST `/v1/workspaces/{workspaceId}/export` | Admin + approver |202; controlled manifest export | p.83; `screen_functions:r1:c137:f19` |
| POST `/v1/workspaces/{workspaceId}/delete` | Admin + approver |202; hold-safe deletion | p.83; `screen_functions:r1:c137:f20` |

Additional supported references with incomplete schemas/scopes: `GET /v1/me`, `PUT /v1/workspaces/{workspaceId}/members`, `GET /v1/cases?cursor=...`, `GET /v1/cases/{caseId}/evidence`, `GET /v1/evidence/{evidenceId}`, `GET /v1/documents/{documentId}/status`, `GET /v1/runs/{runId}/steps`, `GET /v1/review-queue`, `POST /v1/cases/{caseId}/close`, `GET /v1/connectors/{connectorId}/runs`, `GET /v1/model-catalog`, `POST /v1/security/holds`, `GET /v1/evaluations/{evaluationId}`, `GET /v1/system/degraded-modes`, `GET /v1/openapi.json`, `GET /v1/health/live`, `GET /v1/health/ready`. Their existence does not confirm additional screens. [Source: pp.20,23,26,29,32,36,39,42,46,56,59,63,70,76; `screen_functions:r1:c27:f3`, `screen_functions:r1:c33:f6`, `screen_functions:r1:c33:f7`, `screen_functions:r1:c39:f7`, `screen_functions:r1:c45:f2`, `screen_functions:r1:c51:f2`, `screen_functions:r1:c57:f7`, `screen_functions:r1:c63:f7`, `screen_functions:r1:c69:f7`, `screen_functions:r1:c75:f7`, `screen_functions:r1:c93:f6`, `screen_functions:r1:c99:f6`, `screen_functions:r1:c99:f7`, `screen_functions:r1:c105:f7`, `screen_functions:r1:c117:f1`, `screen_functions:r1:c129:f4`]

Governance/internal references also remain preserved without UI invention: `POST /v1/design-decisions`, `GET /v1/design-baselines/{id}`, `POST /internal/model/generate`, `GET /internal/workflows/{runId}`, `POST /internal/deadletters/{id}/replay`, `GET /internal/storage/documents/{id}`, `POST /internal/storage/purge`, `GET /internal/metrics`, `GET /internal/capacity`, `POST /internal/releases`, `GET /internal/releases/{releaseId}`. Internal calls use scoped identities/mTLS and independently authorized HTTP/gRPC; the orchestrator lacks direct DB credentials. [Source: pp.9–10,16,39,50,53,66,70,73; `screen_functions:r1:c8:f1`, `screen_functions:r1:c9:f6`, `screen_functions:r1:c9:f7`, `screen_functions:r1:c20:f1`, `screen_functions:r1:c63:f6`, `screen_functions:r1:c81:f4`, `screen_functions:r1:c81:f5`, `screen_functions:r1:c87:f6`, `screen_functions:r1:c87:f7`, `screen_functions:r1:c111:f7`, `screen_functions:r1:c117:f2`, `screen_functions:r1:c123:f4`]

### SF-017 — Integration data, events and errors

External dependencies are OIDC identity, enterprise repositories/connectors, approved model deployments, hybrid search, PostgreSQL authoritative mutable metadata, encrypted object storage and durable outbox/message processing. No provider/region/vendor selections are supplied. Do not expose datastores publicly. RLS requires per-transaction session-context reset and additional workspace-tenancy enforcement by foreign keys **or** controlled writes, still unselected. [Source: pp.7,16,18–23,85–86,90; `screen_functions:r1:c4:f5`, `screen_functions:r1:c19:f5`, `screen_functions:r1:c24:f1`, `screen_functions:r1:c32:f1`, `screen_functions:r1:c138:f12`, `screen_functions:r1:c138:f13`, `screen_functions:r1:c142:f9`]

| Event | Producer / selected payload / consumer action from Appendix C |
|---|---|
| CaseCreated | Case Service / Case ID, revision / run classifier |
| DocumentNormalized | Ingestion / Version ID, source hash / build index |
| SearchIndexCommitted | Indexer / index generation, document revision / invalidate query cache |
| AgentPlanApproved | Orchestrator / run ID, plan hash / dispatch steps |
| ApprovalDecisionRecorded | Policy Service / task, actor, content hash / **validate** publication |
| WorkflowStageAdvanced | Orchestrator / run, stage, checkpoint / resume consumers |
| AccessDenied | Policy Service / principal, action, policy digest / alert enrichment |
| TenantDeletionVerified | Retention Worker / manifest ID, receipt hash / close purge record |

[Source: p.87 C.1; `screen_functions:r1:c139:f1`, `screen_functions:r1:c139:f2`, `screen_functions:r1:c139:f3`, `screen_functions:r1:c139:f4`, `screen_functions:r1:c139:f5`, `screen_functions:r1:c139:f6`, `screen_functions:r1:c139:f7`, `screen_functions:r1:c139:f8`]

Other registered events are `BaselineCommitted`, `RunRequested`, `DeploymentPromoted`, `ModelInvocationCompleted`, `DataRetentionPurgeCommitted`, `ApiCompatibilityVerified`, `UserReviewOpened`, `SecurityPolicyChanged`, `SloBurnRateDetected`, `BackpressureActivated`, `ReleasePromoted`, `EvaluationCompleted`. Preserve versioned envelopes/outbox and source-specific audit/log visibility; exact triggers/payloads/browser subscriptions remain open. Event names do not authorize actions or automatic publication. [Source: pp.10,17,20,39,53,56,59,63,66,70,73,76; `screen_functions:r1:c9:f8`, `screen_functions:r1:c21:f8`, `screen_functions:r1:c27:f4`, `screen_functions:r1:c63:f8`, `screen_functions:r1:c87:f8`, `screen_functions:r1:c93:f8`, `screen_functions:r1:c99:f8`, `screen_functions:r1:c105:f8`, `screen_functions:r1:c111:f8`, `screen_functions:r1:c117:f2`, `screen_functions:r1:c123:f5`, `screen_functions:r1:c129:f5`]

Cross-service writes must be retry-safe. At-least-once consumers check ledger/event identity and aggregate revision, record duplicate outcome and do not reapply mutation; delayed events are safe without cross-partition order reliance. Rejected stale/unauthorized writes leave business state unchanged before the relevant event publication. Accepted transitions require one audit record and tenant-scoped traces; diagnostic telemetry excludes source text. [Source: pp.15,48–50,59; `screen_functions:r1:c17:f2`, `screen_functions:r1:c78:f4`, `screen_functions:r1:c79:f8`, `screen_functions:r1:c82:f1`, `screen_functions:r1:c82:f3`, `screen_functions:r1:c100:f1`]

| Failure | Confirmed result | Open UX/schema details |
|---|---|---|
| Revision mismatch |409 `CASE_VERSION_CONFLICT`, current revision; example message `Case revision no longer matches.` and `retryable:false` | Mandatory production envelope fields, refresh/merge/navigation |
| Changed body/key reuse |409 `IDEMPOTENCY_CONFLICT` | Safe copy/key recovery |
| Schema-invalid request |422 | Specific code/details |
| Quota throttling |429; admission `Retry-After` | Timing/value/client behavior |
| Invalid model output |`MODEL_OUTPUT_INVALID`; no publish | HTTP/run mapping and rework |
| Revoked queued connector credential |`CONNECTOR_REAUTH_REQUIRED`, no tokens | Reauth flow |
| Foreign tenant ID |404-equivalent absent-ID class, non-disclosing | Exact status/message not universally specified |
| Unsupported evidence |`NO_SUPPORTED_EVIDENCE` | Error/result classification and clarification/human route |

[Source: pp.25,27,36,38,54,84,89; `screen_functions:r1:c37:f3`, `screen_functions:r1:c42:f5`, `screen_functions:r1:c56:f4`, `screen_functions:r1:c61:f4`, `screen_functions:r1:c90:f1`, `screen_functions:r1:c137:f21`, `screen_functions:r1:c141:f2`, `screen_functions:r1:c141:f3`]

The A.3 example uses `Content-Type: application/json`, `correlation_id: trace_01HZZ_EXAMPLE`, and `details: {expected_revision:7, actual_revision:8}`; those ID/numbers are placeholders, not limits. Keep exact uppercase literals despite unresolved “stable snake-case” convention. Optional signed webhooks verify signature/event age, retry exponentially and never roll back internal case transitions; no webhook screen is confirmed. [Source: pp.54–55,82–84; `screen_functions:r1:c90:f5`, `screen_functions:r1:c91:f4`, `screen_functions:r1:c137:f1`, `screen_functions:r1:c137:f21`]

### SF-018 — Numeric targets and configuration provenance

| Value | Scope/status |
|---|---|
| API99.9% monthly; case-create P95 under300ms; search P95 under1.5s excluding remote fetch | Reference targets; model generation separately measured. Chapter2 says within300ms: exact boundary needs confirmation |
|2000 active daily users;60 steady/180 burst requests/s;100000 documents/tenant maximum;20 concurrent runs/large tenant | Reference load, not selected admission thresholds |
| Typical1MB source → approximately40–120 chunks | Approximate parser/content-dependent sizing, not upload rule |
| RPO≤15min;RTO≤4h | Reference recovery targets, not screen response guarantees |
|1536 embedding dimensions | Search data design, not UI field |
|1200 synthetic evaluation cases;precision≥0.97;unsupported≤0.02;high-risk recall1.00 | Frozen reference evaluation targets, not observed results |

[Source: pp.12,34,65,68–70,75; `screen_functions:r1:c14:f1`, `screen_functions:r1:c54:f1`, `screen_functions:r1:c109:f1`, `screen_functions:r1:c114:f1`, `screen_functions:r1:c114:f5`, `screen_functions:r1:c116:f1`, `screen_functions:r1:c127:f1`, `screen_functions:r1:c127:f4`]

AppendixF examples retain exact keys/values: `release:r1.0`; `max_plan_depth:8`, `max_tool_calls:16`, `run_timeout_seconds:180`, `replay_dedup_hours:24`; `max_candidate_chunks:80`, `max_selected_chunks:10`, `embed_dimension:1536`, `hybrid_rrf_k:60`; policy entries in SF-012; `upload_limit_mb:25`, `user_data_region:primary-approved-region`; `trace_sample_rate:0.10`, `diagnostic_retention_days:30`, `audit_retention_years:7`. Only independently confirmed constraints apply in their substantive scopes. The timeout/replay example does not equate to the24-hour request-idempotency or SSE retention window. [Source: p.90; `screen_functions:r1:c142:f1`, `screen_functions:r1:c142:f2`, `screen_functions:r1:c142:f3`, `screen_functions:r1:c142:f4`, `screen_functions:r1:c142:f5`]

### SF-019 — Concrete acceptance criteria

Each criterion states an implementation/test obligation, not a completed test. Unspecified presentation is still open. Critical isolation/approval tests have zero exceptions; benchmark quality cannot offset security failures. [Source: pp.74,88; `screen_functions:r1:c125:f2`, `screen_functions:r1:c140:f14`]

| Criterion | Prerequisite/action | Expected result and traceability |
|---|---|---|
| AC-001 / TST-001 | Submit case twice with same key | One case, identical response; p.89 `screen_functions:r1:c141:f1` |
| AC-002 / TST-002 | Reuse key with changed body |409 IDEMPOTENCY_CONFLICT; p.89 `screen_functions:r1:c141:f2` |
| AC-003 / TST-003 / T-01 | Valid foreign-tenant resource ID/token attempt | Non-disclosing404-equivalent denial; domain/RLS guard; pp.88–89 `screen_functions:r1:c140:f1`, `screen_functions:r1:c141:f3` |
| AC-004 / TST-004 / T-08 | Index source, revoke access, query again; include during-search revocation test | No forbidden next-query evidence; cache revision control; pp.88–89 `screen_functions:r1:c140:f8`, `screen_functions:r1:c141:f4` |
| AC-005 / TST-005 | Force model schema failure | MODEL_OUTPUT_INVALID and no publish; p.89 `screen_functions:r1:c141:f5` |
| AC-006 / TST-006 / T-03 | Revise candidate; approve prior/wrong hash | Stale rejection/audit, no business mutation; pp.45,88–89 `screen_functions:r1:c73:f8`, `screen_functions:r1:c140:f3`, `screen_functions:r1:c141:f6` |
| AC-007 / TST-007 / T-07 | Replay outbox message; replay same event100 times | Exactly one accepted transition; ledger/revision checks prevent reapplication; pp.88–89 `screen_functions:r1:c140:f7`, `screen_functions:r1:c141:f7` |
| AC-008 / TST-008 | Provider429 burst | Capped retries/controlled admission; saved cases remain available; pp.69,89 `screen_functions:r1:c115:f1`, `screen_functions:r1:c141:f8` |
| AC-009 / TST-009 | Generate with missing citations | Needs review or unsupported outcome; selection remains open; p.89 `screen_functions:r1:c141:f9` |
| AC-010 / TST-010 | Expire review task | No implicit approval; escalation recorded; p.89 `screen_functions:r1:c141:f10` |
| AC-011 / TST-011 | Open case using keyboard only | No blocked action and visible focus; p.89 `screen_functions:r1:c141:f11` |
| AC-012 / TST-012 | Region recovery exercise | Stated RPO/RTO limits, safety preserved; pp.69,89 `screen_functions:r1:c116:f1`, `screen_functions:r1:c141:f12` |
| AC-013 / TST-013 | Purge tenant under legal hold | Protected records retained/receipted; p.89 `screen_functions:r1:c141:f13` |
| AC-014 / TST-014 | Arbitrary MCP invocation | DENY before dispatch; p.89 `screen_functions:r1:c141:f14` |
| AC-015 / TST-015 / T-04 | Unsafe PDF/polyglot/zipped malicious payload | Scan/sandbox/bounded parsing; quarantine/no indexing; pp.88–89 `screen_functions:r1:c140:f4`, `screen_functions:r1:c141:f15` |
| AC-016 / TST-016 | Safety-regressed canary | Release gate blocks promotion; p.89 `screen_functions:r1:c141:f16` |
| AC-017 | Eligible Reviewer opens candidate and activates citation | Exact artifact/citations/model-prompt version/reasons; source opens/highlights anchor before approval is available; pp.57–58 `screen_functions:r1:c95:f2`, `screen_functions:r1:c96:f6`, `screen_functions:r1:c97:f2` |
| AC-018 | Required review fields incomplete | Approve and Reject disabled; completing fields does not bypass role/hash gates; p.58 `screen_functions:r1:c97:f3` |
| AC-019 | Active run; refresh/reconnect | Server-reconstructed progress; retained scoped SSE resume via Last-Event-ID, no private replay; pp.55,58 `screen_functions:r1:c91:f1`, `screen_functions:r1:c97:f1` |
| AC-020 | Permissions change after search, then publication attempted | Authorization recomputed, stale evidence rejected; p.59 `screen_functions:r1:c100:f2` |
| AC-021 / T-11 | Single Admin attempts export | Denied; two-person approval plus manifest required; p.88 `screen_functions:r1:c140:f11` |
| AC-022 | Authorized close | Approved answer/source versions/reviewer decisions preserved as immutable lineage; p.26 `screen_functions:r1:c38:f6`, `screen_functions:r1:c40:f4` |
| AC-023 | Generation unavailable/vector degraded | Manual editing/evidence online; any lexical fallback visibly reduced quality; no safety bypass; pp.68–69 `screen_functions:r1:c113:f2`, `screen_functions:r1:c115:f3` |
| AC-024 | Credential revoke with queued connector job | CONNECTOR_REAUTH_REQUIRED without token disclosure; p.27 `screen_functions:r1:c42:f5` |
| AC-025 | Incomplete provisioning | Visible incomplete state and sync blocked; p.78 `screen_functions:r1:c132:f1` |
| AC-026 | End-to-end authorized journey and exceptions | Create/ingest/retrieve/draft/review/publish, rejected rework, poisoned quarantine, foreign search denial verified; p.75 `screen_functions:r1:c128:f1` |
| AC-027 | Low-quality but authorized document | Viewable, excluded from autonomous recommendation; p.32 `screen_functions:r1:c50:f4` |
| AC-028 / T-02,T-05,T-06,T-09,T-10,T-12 | Hostile evidence, credential observation, regional outage, historical edit, recursive hints, fixture replacement | Delimit/pin tools; vault/redaction; approved fallback; append-only hash integrity; bounded execution; signed/versioned fixtures; p.88 `screen_functions:r1:c140:f2`, `screen_functions:r1:c140:f5`, `screen_functions:r1:c140:f6`, `screen_functions:r1:c140:f9`, `screen_functions:r1:c140:f10`, `screen_functions:r1:c140:f12` |

All revised invariants link to a negative test. Minimum release pack includes unit, schema evolution, negative authorization, replay, staging sync, visual accessibility, search recall, grounding, policy recall, load and disaster recovery. Randomized tests record seeds; synthetic corpora are frozen/versioned/independently reviewed for leakage; outputs are signed/release-digest linked. SEC-001–SEC-012 evidence must be independently reviewed/reproduced and release-signed; mapping to T-01–T-12 remains absent. Low statistical confidence blocks release. [Source: pp.8–10,76,88–89; `screen_functions:r1:c5:f2`, `screen_functions:r1:c128:f5`, `screen_functions:r1:c140:f13`, `screen_functions:r1:c141:f17`, `screen_functions:r1:c141:f18`, `screen_functions:r1:c141:f19`]

## Consistency and Open Questions

### SF-020 — Required clarifications and amendments

No missing detail is permission for an implementation AI to choose silently. Retain the following beside affected requirements and link these `SF-*`/`SCR-*` identifiers from **01_screen_functions.md** in later decision consolidation. No owner, deadline, approval or completed later specification is supplied.

| Open ID | Affected requirement | Both positions / missing decision / required amendment |
|---|---|---|
| OQ-001 | SF-004–005, all SCRs | Confirm eight-screen routes, origins/destinations, launch, users, primary action/status summary, conditional visibility and figure aliases. Preserve all title/selected-navigation pairs; no majority-based naming choice |
| OQ-002 | SF-006–015 | Complete every actual field contract, including required review fields; do not use DDL defaults, UUID/hash metadata or fictional values as form constraints. Define list/search/filter/sort/pagination/row interactions |
| OQ-003 | SF-009,016 | General POST /v1/runs versus case-scoped POST /v1/cases/{caseId}/runs: define relationship/browser endpoint/amendment. Evidence pp.15,83; `screen_functions:r1:c17:f3`, `screen_functions:r1:c137:f10` |
| OQ-004 | SF-009–010 | Missing approval terminates (§11.3) versus AWAITING_REVIEW (§13.2/A.1); recoverable timeout (§2.3) versus FAILED catalog; define applicable conditions, deadlines, cancellation/resume/new-run and displayed states. Evidence pp.12,41,49,82; `screen_functions:r1:c14:f2`, `screen_functions:r1:c68:f1`, `screen_functions:r1:c79:f1`, `screen_functions:r1:c137:f3` |
| OQ-005 | SF-007 | Case/CaseService/CaseAggregate Immutable derivative registers versus revision-controlled transactional mutation and append-only history. Identify immutable subject and amend registers, not supported edit/transition behavior. Evidence pp.13,17,24–26,85; `screen_functions:r1:c15:f6`, `screen_functions:r1:c21:f3`, `screen_functions:r1:c39:f3`, `screen_functions:r1:c36:f3`, `screen_functions:r1:c138:f3` |
| OQ-006 | SF-003,010 | Own-high-risk self-approval prohibition versus unqualified B.1 no-self-approval; confirm broader scope. Admin/Workspace Admin, Owner/Member/approver/operator mappings; reviewer pools, separation, elevated override and secondary independence remain open |
| OQ-007 | SF-010 | ReviewForm/ApprovalTask Immutable derivative versus required review input/assignment/expiry; identify immutable artifact/revision and editable fields without inventing separation. Evidence pp.45–46,58–59; `screen_functions:r1:c73:f1`, `screen_functions:r1:c75:f3`, `screen_functions:r1:c97:f3`, `screen_functions:r1:c99:f3` |
| OQ-008 | SF-006,016–017 | Generic GET allocation/error-or-job language versus explicit200 status/lookup contracts: define allocation conditions, component ownership, schemas, audience/idempotency and response selection. Repetition does not establish jobs. Missing event triggers/namespace schemas and browser notification mappings remain open |
| OQ-009 | SF-017 | Stable snake-case capitalization versus explicit uppercase CASE_VERSION_CONFLICT/IDEMPOTENCY_CONFLICT/MODEL_OUTPUT_INVALID; preserve literals and amend convention. Most denial messages/recovery/routes remain undefined |
| OQ-010 | SF-008 | MIME literals/MB unit/cap authority/decompression threshold, unsafe quarantine remediation, OCR opt-in actor/control/marker, quality thresholds, source highlight/page conventions/signed URL expiry/revocation/missing anchors and Citation schema |
| OQ-011 | SF-007 | Closure entry/reopening actor/API/resulting status; immutable approved lineage versus later retention; impact/urgency formula and reason-code/calendar/timezone definitions |
| OQ-012 | SF-010,013 | Distinct approval/publication invocation and success/error navigation; expiry reassignment/escalation conditions; export independent two-person workflow/manifests/checksums/download; deletion independent checks/holds/receipts/partial recovery and TenantDeletionVerified tenant/workspace scope |
| OQ-013 | SF-011,014 | Connector providers/capability warning/reauth/running-job effects, cursor reset/retry/quarantine release, provisioning readiness, sync/replay/backoff/quota schedules/bounds and operator permissions |
| OQ-014 | SF-015 | Focus/keyboard/semantic/live-transition inventory, locale options/control/default, workspace timezone/time/number formatting and responsive behavior; no achieved conformance claimed |
| OQ-015 | SF-018 | Within300ms versus under300ms boundary and test method; reference capacity versus admission limits; budgets/retry/circuit thresholds;180s/24h replay/candidate/RRF/sample examples are not selected universal rules |
| OQ-016 | SF-017 | Other register subjects need clarification: APIReplicaSet, TenantMembership, SyncRun, ExtractionJob, IndexAlias, ErrorEnvelope, CacheEntry, ProvisioningJob. Preserve exact classifications alongside detailed scope, not new schemas. Cache ledger versus ephemeral cache and alias immutability versus atomic switch remain open |
| OQ-017 | SF-013–014 | Corporate retention, holds, audit verification/hash algorithm/redaction, source-lineage deletion, cache/in-flight revocation handling, degraded flags and restoration state. Current next-query/publication authorization remains mandatory |
| OQ-018 | SF-009,017 | A2A full input/output schema, placeholder case_demo versus typed UUID search handoff, grant/capability authorization and example omission; no schema exception established |
| OQ-019 | SF-019 | REQ/API/EVT/SEC/TST mappings, especially SEC-001–012 versus T-01–12, complete fixtures, domain confidence criteria, safety regression windows and signed fixture/report contracts |
| OQ-020 | SF-002,014,017 | Dated region/search/identity/model/retention/connector-permission decisions before implementation lock; key isolation/rotation throughput before enterprise GA. Terraform/Bicep, optional BFF/webhooks remain unselected. Evidence pp.10,71,90; `screen_functions:r1:c8:f6`, `screen_functions:r1:c120:f1`, `screen_functions:r1:c142:f9` |
| OQ-021 | SF-014 | Governance impact scores/approval actors, deployment compatibility/readability/sign-off/reconstruction and operational evidence UI mapping; source procedures do not authorize new screens |

**Dependencies:** detailed API, data, workflow/security, integration, architecture and verification contracts are **To be defined in a later stage**. Stage8 will consolidate unresolved items into `08_architecture_decision.md` from completed Markdown specifications; this stage does not generate that document or choose those decisions. The candidate specification is provisional pending evidence approval review.
