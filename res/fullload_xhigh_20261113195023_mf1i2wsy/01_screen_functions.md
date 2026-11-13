# 1. Screen Function Specification

## Scope and Users

### Specification Basis and Requirement Status

| Item | Definition |
|---|---|
| Specification file | `01_screen_functions.md` |
| Source document | `1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf` |
| Source baseline | `OD-AI-DDS-001`, release `R1.0`, design revision `1.3` |
| Source character | A fictional, normative reference design. Its numeric values are design assumptions, not measured production results. |
| Previous specifications | None. This is stage 1. |
| Identifier convention | `SCR-001` through `SCR-011` identify screens or explicitly illustrated navigation surfaces. Suffixes `Fxx` and `Axx` identify fields and actions. `SCR-COM-xxx` identifies shared requirements. `OQ-SCR-xxx` identifies unresolved decisions. These screen identifiers are assigned by this specification because the source does not provide screen IDs. |
| Citation convention | `[DDS]` means the source filename above. Page references are original PDF page numbers. Section and figure references identify the supporting source location. |

[DDS]: 1794567023-OrionDesk_AI_Detailed_Design_Specification.pdf

The following statuses apply throughout this specification:

- **Confirmed:** Explicitly supported by source prose, a source contract, or an identified illustration. Illustration-confirmed content is identified separately from fully specified behavior.
- **Needs confirmation:** The source does not establish an implementation decision, field contract, navigation rule, permission, or other necessary detail.
- **Proposal:** An explicitly suggested screen placement or interaction. A proposal is not an approved requirement and must not be implemented as a confirmed decision without resolution.

Field presence in a domain aggregate does **not** by itself confirm an editable screen control. Field tables therefore distinguish confirmed data from proposed placement.

**SCR-COM-001 — Baseline interpretation.** Implement source-supported behavior without interpreting unresolved choices as permission to invent screens, API contracts, field limits, permissions, schedules, or workflow outcomes. Source configuration examples and mock data must not silently become production configuration or initial user data.  
**Source:** [DDS], pp. 1–2; p. 8, §1.1.1; p. 90, Appendix F and §F.2.

### Business Activities and Scope

| Activity | Screen-function scope | Status and source |
|---|---|---|
| Case intake and triage | Create cases, receive business context and attachments, display classification results, and allow label correction with a reason code. | **Confirmed.** [DDS], pp. 11–12, §§2.1–2.2. |
| Evidence-based research | Search only permitted knowledge, inspect cited source versions, and follow citations to stored anchors. | **Confirmed.** [DDS], pp. 30–36, §§8.1–9.3; p. 57, §16.1.2. |
| AI-assisted resolution | Request a grounded draft and show durable retrieval, generation, policy, review, publication, and failure progress. | **Confirmed.** [DDS], p. 12, §2.2.2; pp. 40–42, Chapter 11; p. 49, §13.2.1; p. 58, §16.2.1. |
| Human review | Let authorized reviewers inspect the exact candidate, evidence, model/prompt versions, and policy reasons before approving or rejecting. | **Confirmed.** [DDS], pp. 44–46, Chapter 12; pp. 57–59, Chapter 16. |
| Case maintenance and closure | Edit authorized case data using revision preconditions; preserve immutable approved-output lineage at closure. | **Confirmed.** [DDS], pp. 24–26, Chapter 6; p. 83, §A.2. |
| Connector administration | Monitor connector capabilities and sync outcomes, initiate incremental sync, and surface lower-trust and reauthentication conditions. | **Confirmed.** [DDS], pp. 27–29, Chapter 7; p. 57, §16.1.1. |
| Policy administration | Manage workspace policy, permitted deployments, approved toolsets, retention settings, and reviewer routing with revision-safe updates. | **Confirmed activity and screen name; field controls and API binding need confirmation.** [DDS], p. 11, §2.1.1; p. 24, §6.1.1; p. 57, §16.1.1. |
| Audit inspection | Obtain immutable decision metadata, prompt-template digests, access events, and authorized redacted evidence. | **Confirmed.** [DDS], p. 11, §§2.1.1–2.1.2; pp. 61–63, Chapter 17. |
| Usage and AI-quality inspection | Read cost/quota/trend data and evaluation scorecards. The source illustrates associated navigation/views but does not fully define their screen organization. | **Confirmed data and illustrated surfaces; organization needs confirmation.** [DDS], pp. 64–66, Chapter 18; pp. 74–76, Chapter 21; p. 81, Figure 22.2; p. 83, §A.2. |
| Workspace export and deletion | Controlled export and legal-hold-safe deletion requiring independent approval checks. No screen placement is specified. | **Confirmed operation; screen placement needs confirmation.** [DDS], pp. 78–80, Chapter 22; p. 83, §A.2; p. 88, `T-11`. |

### Explicit Exclusions and Deferrals

| Area | Treatment | Source reason |
|---|---|---|
| Physical automation and irreversible financial transactions | **Out of scope.** | The system processes enterprise knowledge and submitted cases, not these activities. [DDS], p. 9, §1.2.1. |
| Foundation-model fine-tuning, unrestricted browsing, and agents with administrative cloud permissions | **Out of scope.** | Explicit platform exclusions. [DDS], p. 9, §1.2.1. |
| Application-hosted GPU inference | **Out of scope for the R1 execution profile.** | Inference providers are external dependencies. [DDS], p. 19, §4.2.1. |
| Cross-region active/active mutation, OCR languages beyond English, and customer-managed model weights | **Deferred from this baseline.** | Explicit deferrals; no corresponding R1 screen control is authorized. [DDS], p. 10, §1.3.2. |
| Authentication screens, membership screens, provisioning screens, and operational consoles not described by the source | **Needs confirmation, not out of scope.** | Supporting activities or APIs exist, but screen contracts are absent. See unlocated operations below. |

### Users and Permissions

| User or source term | Confirmed responsibilities and restrictions | Screen relevance | Unresolved permissions |
|---|---|---|---|
| Analyst | Opens cases, evaluates evidence, creates cases and attachments, and starts AI runs. Cannot approve their own high-risk recommendation. | Case Queue, Case Detail, Evidence Viewer, Run Timeline. | Queue-read scope, ownership assignment, classification-correction permission, closure permission, and access to administrative summaries. |
| Reviewer | Approves or rejects AI-generated recommendations. Selection depends on policy and organizational role. Case/run read access is listed in the API register. | Review Inbox; authorized Case Detail, Evidence Viewer, and Run Timeline. | Whether unassigned tasks are visible; reassignment/escalation permissions; override role definition. |
| Workspace Admin / Admin | Manages connectors and policy. `Admin` is the role term in the authorization/API chapters. Can initiate connector sync, read usage, and start evaluations. | Connector Health, Policy Settings; usage/evaluation surfaces. | Whether `Workspace Admin` and `Admin` are identical roles; case-read access is not established merely by administrative status. |
| Auditor | Obtains immutable evidence without editing case content. Sees decision metadata, prompt-template digests, and access events within redacted content scope. | Audit Explorer; evidence access requires a separately confirmed permission contract. | The auditor journey allows evidence access, while the case-read API register lists only Analyst/Reviewer. The authorized evidence path needs confirmation. |
| Service | A baseline authorization role for service identities. | No interactive screen access is confirmed. | Any interactive operational use must be explicitly authorized. |
| Owner | Listed as the scope for `PATCH /v1/cases/{caseId}`. | Authorized Case Detail editing. | `Owner` is not listed as a baseline role. Confirm whether this is a resource relationship combined with a role. |
| Member | Listed as the scope for `POST /v1/search`. | Evidence search. | `Member` is not listed as a baseline role. Confirm the membership predicate and permitted interactive roles. |
| Approver / elevated role / operator | These terms occur in export, deletion, overrides, credential revocation, and replay procedures. | Screen placement is unresolved. | Exact role mappings, separation-of-duty requirements, and allowed actions are undefined. |

**Sources:** [DDS], p. 11, §§2.1.1–2.1.2; p. 22, §5.2.1; pp. 45–46, §§12.2–12.3; p. 50, §13.3.2; p. 83, §A.2.

**SCR-COM-002 — Resource authorization.** Access must combine role, tenant, workspace membership, case sensitivity, document ACL, requested action, and segregation-of-duties constraints. Navigation visibility is not the security boundary. The server must re-evaluate resource authorization, including within state-changing transactions. Retrieval must apply source ACLs before releasing text to generation.  
**Source:** [DDS], pp. 21–23, §§5.1–5.3; p. 34, Chapter 9 invariant.

**SCR-COM-003 — Tenant isolation and non-disclosure.** A foreign-tenant identifier must produce the same class of not-found response as an absent identifier. Displays and error details must not reveal unauthorized resource existence. Denials retain the principal and denied resource class in authorized audit evidence.  
**Source:** [DDS], p. 23, §5.3.2; p. 89, `TST-003`.

**Needs confirmation — OQ-SCR-003:** Resolve all role aliases and action predicates above. Do not grant Admin or Auditor general case/evidence access by inference. The source also states no self-approval in `approval_tasks` and `self_approval_allowed: false`; confirm its scope without weakening the explicit high-risk prohibition.  
**Source:** [DDS], p. 85, §B.1; p. 90, Appendix F.

### Prerequisites

1. The user has an authenticated interactive session using OIDC authorization-code flow with PKCE.
2. API access has valid issuer, audience, expiry, subject, and tenant claims. Unexpected token algorithms or missing tenancy claims are rejected.
3. The active resource context is tenant- and workspace-scoped.
4. Case, document, run, and review access satisfies resource-level authorization.
5. Connector sync requires completed provisioning and appropriate workspace configuration. Incomplete provisioning is visible and blocks sync.
6. AI-run admission requires sufficient workspace tokens, acceptable queue age, and provider capacity under configured thresholds.
7. Model routing uses approved deployment-specific workspace policy; no provider outage permits fallback to an unapproved region or data-handling class.
8. Review requires an authorized reviewer assignment, applicable separation of duties, an unchanged candidate artifact, and a non-expired task.

**Sources:** [DDS], pp. 21–23, Chapter 5; p. 37, §§10.1.1–10.1.2; p. 45, §12.2.1; p. 69, §19.2.1; p. 78, §22.1.1.

**Needs confirmation — OQ-SCR-002:** Identity provider, application sign-in entry point, post-authentication destination, session expiry behavior, sign-out behavior, and whether to use the optional backend-for-frontend cookie approach are undefined. The browser must not store long-lived refresh tokens in local storage. Secure, `HttpOnly`, `SameSite` cookies are a source-described option, not a selected implementation.  
**Source:** [DDS], p. 21, §§5.1.1–5.1.2; p. 90, §F.2.

## Screen Inventory and Navigation

### Screen Inventory

The eight screens in §16.1.1 are explicitly confirmed primary screens. Additional illustrated labels are retained for traceability but do not establish complete standalone screen contracts.

| ID | Name and source terminology | Purpose | Users and display conditions | Navigation origins and destinations | Launch method | Status and source |
|---|---|---|---|---|---|---|
| SCR-001 | Case Queue; illustrated title `Case Queue / Risk Prioritization` | Display authorized cases and their status; support entry to case work. | Authorized case users. Exact queue permissions need confirmation. | Sidebar `Case Queue` is illustrated. Opening a case into SCR-002 is a **Proposal**; exact row event and return behavior are undefined. | Browser navigation; route and default landing behavior need confirmation. | **Confirmed primary screen and illustration.** [DDS], p. 14, Figure 2.2; p. 57, §16.1.1. |
| SCR-002 | Case Detail; illustrated title `Case Detail / Resolution Package` | Inspect and maintain a case, its evidence, draft, and decision gate. | Analyst/Reviewer may read authorized cases; edits require the `Owner` predicate. | Sidebar `Case Detail` is illustrated. Citation click-through opens source evidence. Case/run/review links and new-case mode placement need confirmation. | Browser navigation with selected case context; route unresolved. | **Confirmed primary screen.** [DDS], p. 7, Reference UI A; p. 33, Figure 8.2; p. 57, §§16.1.1–16.1.2; p. 83, §A.2. |
| SCR-003 | Evidence Viewer; illustrated title `Evidence Explorer / Citation Audit` | Inspect source evidence and citation provenance; support permitted evidence research. | Authorized document users; reviewers must be able to inspect evidence before approval. | Sidebar `Evidence Viewer` is illustrated. Citation activation opens the source and highlights its anchored page range. Search placement and return-to-origin behavior need confirmation. | Browser navigation or citation click-through; same tab, new tab, drawer, or modal is undefined. | **Confirmed primary screen and citation behavior.** [DDS], p. 43, Figure 11.2; pp. 57–58, §§16.1–16.2. |
| SCR-004 | Run Timeline; sidebar `Agent Runs`; illustrated title `Agent Run / Execution Trace` | Show durable AI-run stages, execution steps, evidence metadata, and failed checkpoints. | Authorized Analyst/Reviewer run readers. | Sidebar `Agent Runs` is illustrated. Entry from a newly requested run or case is a **Proposal**. Case/evidence return links are undefined. | Browser navigation with run context; route unresolved. | **Confirmed primary screen; illustrated naming differs.** [DDS], p. 47, Figure 12.2; p. 57, §16.1.1; p. 58, §16.2.1; p. 83, §A.2. |
| SCR-005 | Review Inbox; illustrated title `Approval Inbox / Binding Decision` | Present authorized review work and capture a binding decision on an exact artifact. | Policy-selected Reviewers meeting minimum role and separation-of-duty constraints. | Sidebar `Review Inbox` is illustrated. Source evidence must be inspectable before decision. Task-detail placement and links to case/run are unresolved. | Browser navigation and task opening; route and notification launch are undefined. | **Confirmed primary screen and review interaction.** [DDS], pp. 45–46, Chapter 12; p. 58, §16.2.2; p. 60, Figure 16.2. |
| SCR-006 | Connector Health; sidebar `Connectors`; illustrated title `Connector Health / Synchronization` | Inspect connector capability, credential, synchronization, and remediation conditions. | Admin initiates sync. Health-read and credential-revocation permissions need confirmation. | Sidebar `Connectors` is illustrated. Connector configuration/authentication subviews are not specified. | Browser navigation; route unresolved. | **Confirmed primary screen.** [DDS], pp. 27–29, Chapter 7; p. 57, §16.1.1; p. 67, Figure 18.2; p. 83, §A.2. |
| SCR-007 | Policy Settings | Inspect and maintain versioned workspace policy/settings. | Workspace Admin activity is confirmed; exact `Admin` mapping and field-level permissions are unresolved. | Not shown in the illustrated sidebar. Navigation origin and all destinations need confirmation. | Browser launch method and route need confirmation. | **Confirmed primary screen name.** [DDS], p. 11, §2.1.1; p. 24, §6.1.1; p. 57, §16.1.1. |
| SCR-008 | Audit Explorer; sidebar `Audit Events`; illustrated title `Audit Explorer / Event Lineage` | Query immutable authorized audit history and inspect lineage. | Auditor API scope is confirmed. Other role access is unresolved. | Sidebar `Audit Events` is illustrated. Links to redacted case/run/evidence records need confirmation. | Browser navigation; route unresolved. | **Confirmed primary screen.** [DDS], pp. 61–63, Chapter 17; p. 57, §16.1.1; p. 77, Figure 21.2; p. 83, §A.2. |
| SCR-009 | Overview | An illustrated navigation destination; business purpose is not described. | Permissions and display prerequisites are undefined. | Sidebar `Overview` appears in reference views. No confirmed destination content or default landing rule. | Sidebar navigation is illustrated; actual launch behavior is undefined. | **Confirmed illustrated navigation label only.** [DDS], p. 7, Reference UI A; p. 14, Figure 2.2. |
| SCR-010 | Usage & Quality | Illustrated destination associated with usage and quality activities. | Admin may read usage and start evaluations; the combined destination’s permissions are undefined. | Sidebar `Usage & Quality` is illustrated. Relationship to SCR-011 is unresolved. | Browser sidebar destination illustrated; route unresolved. | **Confirmed illustrated navigation label and supporting API activity, not a complete screen contract.** [DDS], p. 7, Reference UI A; pp. 65–66, §18.3; p. 83, §A.2. |
| SCR-011 | AI Quality / Evaluation Scorecard | Inspect evaluation results; possible subview of SCR-010. | Admin may start evaluation. Result-read scope needs confirmation. | Illustrated title exists, but the screenshot highlights `Audit Events`, not `Usage & Quality`. No confirmed standalone navigation entry. | Launch method and standalone/subview status need confirmation. | **Confirmed illustrated view title; screen organization unresolved.** [DDS], p. 81, Figure 22.2; pp. 74–76, Chapter 21. |

**Needs confirmation — OQ-SCR-001:** Confirm the actual screen hierarchy, route paths, resource-selection behavior, deep links, navigation origins/destinations, browser-history behavior, and primary action for each screen.

**Proposal — P-SCR-001:** Consolidate `Agent Runs` with Run Timeline, `Evidence Explorer / Citation Audit` with Evidence Viewer, `Approval Inbox / Binding Decision` with Review Inbox, `Connectors` with Connector Health, and `Audit Events` with Audit Explorer. Treat SCR-011 as a subview of SCR-010 if approved. These mappings are not established by the inconsistent illustrations.

### Navigation and Status Requirements

| Requirement ID | Requirement | Status and source |
|---|---|---|
| SCR-COM-004 | Each of the eight confirmed primary screens has one primary action and a clear status summary. The source does not identify which action is primary. | **Confirmed requirement; emphasis and action choice need confirmation.** [DDS], p. 57, §16.1.1. |
| SCR-COM-005 | AI artifacts use accessible text labels `DRAFT`, `NEEDS_REVIEW`, or `PUBLISHED`. Styling alone must not convey status. Artifact labels must not be confused with case, run, or review lifecycle states. | **Confirmed.** [DDS], p. 57, §16.1.2; p. 82, §A.1. |
| SCR-COM-006 | Citation click-through opens the source document and highlights the anchored page range. Citation identifiers are opaque to users and verified before display. | **Confirmed.** [DDS], p. 35, §9.3.1; p. 57, §16.1.2. |
| SCR-COM-007 | All controls target WCAG 2.2 AA behavior, with visible focus, semantic regions, robust keyboard ordering, and keyboard-accessible case opening. Live updates announce only meaningful state transitions. | **Confirmed.** [DDS], p. 58, §16.3.1; p. 89, `TST-011`. |
| SCR-COM-008 | The server stores UTC. The UI presents workspace-local timestamps with timezone labels. Locale selection changes presentation, not durable API representations or event ordering. | **Confirmed.** [DDS], p. 59, §16.3.2; p. 54, §15.1.1. |
| SCR-COM-009 | If generation is unavailable, evidence search and manual case editing remain available and degraded status is displayed. Lexical retrieval may continue during vector degradation with a visible reduced-quality flag. No degraded mode bypasses authorization or approval. | **Confirmed.** [DDS], p. 69, §§19.2.1–19.2.2; p. 79, §22.2.1. |

**Needs confirmation — OQ-SCR-006:** Define the mapping between artifact labels, case/run/review states, and illustrated mixed status text such as `Needs review`, `In progress`, `Published`, `Evidence gap`, and `Triaged`. Do not treat these as interchangeable values of `cases.status`.

**Needs confirmation — OQ-SCR-028:** Define degraded-state response fields, display placement, and reduced-quality labeling. `GET /v1/system/degraded-modes` exists, but its response contract and screen binding are not provided.  
**Source:** [DDS], pp. 68–70, Chapter 19.

**Needs confirmation — OQ-SCR-031:** Supported browsers, viewport behavior, responsive/mobile layout, localization choices, numeric formatting, and exact focus behavior after navigation or validation failure are unspecified. Do not infer these from the reference screenshots.

## Functions by Screen

### Shared Field and Interaction Contracts

#### Field-Table Interpretation

The following profiles apply only where referenced by a field row:

| Profile | Required status | Initial value | Editability | Validation timing and display conditions | Selectable-value source |
|---|---|---|---|---|---|
| **D — Authorized display** | No user input. Whether the response property is mandatory or nullable needs confirmation unless explicitly stated. | Authorized current server value; no mock value is a default. | Read-only presentation. | Resource authorization and applicable version/anchor checks occur on fetch and before display. Show only within authorized resource scope. Exact loading/missing-value presentation needs confirmation. | None; value comes from the identified record/service. |
| **I — Unspecified input contract** | Needs confirmation. | Needs confirmation; no implied empty, selected, or inherited default. | Proposed editable control only where the row says **Proposal placement**. | Authoritative validation before transaction entry, at domain invariants, and before tool dispatch where applicable. Client-side validation is convenience only; blur/change/submit timing needs confirmation. | Needs confirmation unless a source vocabulary is identified. |
| **C — Versioned configuration** | Required/nullable form behavior needs confirmation. | Existing approved configuration. An Appendix F example is not an independently selected deployment setting. | Admin editing activity is confirmed; editable controls and field-level rights need confirmation. | Revision precondition and domain/policy validation on update. Exact local validation timing is undefined. Display within authorized workspace scope. | Versioned configuration, registry, reviewer policy, or referenced catalog as specified. |

Logical presentation descriptions such as “text display,” “numeric display,” or “list display” are not declarations of a wire or database data type. Exact types are only marked confirmed where supplied by the source.

**SCR-COM-010 — Mutation safety.**

1. Validate input before allocating long-running work and before entering state-changing transactions.
2. Carry `tenant_id`, revision, `actor_id`, `occurred_at`, and a correlation ID at durable state-changing boundaries.
3. Use `If-Match` revision conditions for case updates.
4. Use `Idempotency-Key` for POST mutations that create long-running jobs; case creation also has an explicit idempotency requirement.
5. Identical replay returns the original outcome; a reused key with a changed fingerprint returns `IDEMPOTENCY_CONFLICT`.
6. The actor/request fingerprint maps to one outcome for 24 hours in the case-domain contract.
7. Rejected stale or unauthorized actions leave business state unchanged.
8. Dependency failure produces a documented retryable error or a persisted asynchronous operation identifier, never ambiguous success.
9. Validation and permission failures are permanent and must not be retried as transient failures.

**Sources:** [DDS], p. 25, §6.2.2; pp. 49–50, §13.3; pp. 54–56, §§15.1.2 and 15.3.2; p. 89, `TST-001`, `TST-002`, `TST-007`.

**SCR-COM-011 — Safe failure display.** Display authoritative, non-sensitive failure information without showing connector credentials, complete prompts, retrieved documents in error details, or unauthorized resource existence. Partial processing must not be shown as approved or published.  
**Source:** [DDS], p. 13, §2.3.2; p. 84, §A.3.

| Failure or result | Confirmed contract | Screen treatment |
|---|---|---|
| Case revision conflict | HTTP `409`, `CASE_VERSION_CONFLICT`, current revision; canonical details may include `expected_revision` and `actual_revision`. | Show a conflict, not successful save. Exact conflict-recovery/merge UI needs confirmation. |
| Changed payload with reused key | HTTP `409`, `IDEMPOTENCY_CONFLICT`. | Show a failed conflicting submission; do not create a second operation under that key. |
| Invalid request schema | HTTP `422`. | Show safe validation details when supplied. Exact field mapping needs confirmation. |
| Quota/admission throttling | HTTP `429`; run admission includes `Retry-After`. | Show throttled/not-started status. Saved cases remain accessible. No invented retry interval. |
| Foreign-tenant or absent resource | Non-disclosing not-found class; `404`-equivalent test outcome. | Do not reveal which condition occurred. |
| Revoked connector credentials | `CONNECTOR_REAUTH_REQUIRED`. | Show reauthentication-required condition without tokens. |
| Insufficient retrieval evidence | `NO_SUPPORTED_EVIDENCE`. | Show unsupported evidence, not fabricated context. Clarification/human routing may follow; exact UI is unresolved. |
| Invalid model output | `MODEL_OUTPUT_INVALID`. | Show failure; do not publish. |
| Stale approval artifact | HTTP `409` is listed; no exact stale-approval error code is provided. | Show stale decision failure and do not apply approval to changed content. |
| Unsafe upload, invalid MIME, oversized upload, decompression threshold failure | Fail-closed/quarantine behavior is confirmed; exact HTTP/code mapping is absent. | Show safe rejected/quarantined condition. Do not invent a named error code. |

**Sources:** [DDS], pp. 25, 27, 30, 36, 38, 54, 69, 83–84; p. 89, Appendix E.

**Needs confirmation — OQ-SCR-029:** Define error-code casing and complete per-operation status/error mappings. §15.1.1 describes snake-case codes while examples use uppercase identifiers; preserve exact existing identifiers pending resolution. Define how `message`, `correlation_id`, `retryable`, and safe `details` appear to users. Do not expose diagnostic payloads as page content.

### Shared Illustrated Shell and Summary Fields

The reference views repeatedly show the following data. Their presence in the illustrations is confirmed, but aggregate definitions, real APIs, and required placement across screens are not.

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and timing | Display/value source | Evidence and open decision |
|---|---|---|---|---|---|---|
| SCR-COM-F01 | Workspace name — active workspace context | Text display; exact type/length unknown | D | Must match authorized workspace scope | Illustrated under the view title | **Illustration confirmed.** [DDS], p. 7, Reference UI A. Aggregate/name API: OQ-SCR-022. |
| SCR-COM-F02 | Tenant/release indicator | Text display; no schema/length supplied | D | Must not enable tenant switching by editing displayed text | Illustrated header | **Illustration confirmed.** Sample `fictional tenant / R1.0`; not a tenant default. [DDS], p. 7. |
| SCR-COM-F03 | `OPEN CASES` | Count display; type, aggregation, and formatting unknown | D | Count scope and refresh timing undefined | Illustrated summary card | Sample `128`, not initial data or a limit. [DDS], pp. 7, 14. OQ-SCR-022. |
| SCR-COM-F04 | `AWAITING REVIEW` | Count display; type and state mapping unknown | D | Must not infer task counts from unrelated case/run states | Illustrated summary card | Sample `14`, not a default. [DDS], pp. 7, 14. OQ-SCR-022. |
| SCR-COM-F05 | `EVIDENCE COVERAGE` | Percentage display; formula and precision unknown | D | No threshold is defined by the mock percentage | Illustrated summary card | Sample `97.6%`, not the citation-precision release target. [DDS], p. 7. OQ-SCR-022. |
| SCR-COM-F06 | `SERVICE STATE` | Status text; enumeration unknown | D | Must reflect authoritative health/degraded state, not assume healthy | Illustrated summary card | Sample `Healthy`. No summary API mapping confirmed. [DDS], p. 7; p. 69, §19.2.2. |
| SCR-COM-F07 | View title/status summary | Text display; exact length/format unknown | D | Accessible status text required; each primary screen has a clear summary | Screen-specific view state | Requirement confirmed; exact summaries unresolved. [DDS], p. 57, §16.1.1. |

The sample workspace `Meridian Manufacturing`, case numbers `OD-2026-1042` through `OD-2026-1038`, counts, percentages, and model label `gateway-r1.2` are fictional illustrated data. They are not seed data, approved deployment selections, field masks, or cardinality constraints.  
**Source:** [DDS], p. 7, Reference UI A; p. 14, Figure 2.2.

**Needs confirmation — OQ-SCR-022:** Define each summary’s tenant/workspace/user scope, aggregation formula, update source, refresh behavior, null/error representation, and applicable screens. Repetition of the same panel in differently titled illustrations does not confirm universal placement.

<a id="scr-001"></a>
### SCR-001 — Case Queue

#### Fields and List Content

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and validation timing | Display/value source | Status and source |
|---|---|---|---|---|---|---|
| SCR-001-F01 | Case identifier — reference for opening a case | Canonical identifiers use UUIDv7. Illustrated business numbers have an undefined schema/mapping. | D | Validate tenant/resource scope on list retrieval and case opening | Authorized case list | **Confirmed identifier data and illustrated display.** [DDS], p. 14, Figure 2.2; p. 51, §14.1.1. OQ-SCR-006. |
| SCR-001-F02 | Case title — brief business subject | Text display; length and wire type undefined | D | No source-defined truncation or tooltip rule | Authorized case list | **Illustration and domain confirmed.** [DDS], p. 14; p. 24, §6.1.2. |
| SCR-001-F03 | Case/workflow status summary | Case state uses the §A.1 vocabulary; illustrated row text mixes workflow concepts | D | Use accessible text; state mapping must be resolved before implementation | Authorized current server state | **Display confirmed; mapping unresolved.** [DDS], p. 14; p. 57, §16.1.2; p. 82, §A.1. |

#### Actions and Events

| ID | Button/event and execution conditions | Processing | Successful display/navigation | Failure display | Status and source |
|---|---|---|---|---|---|
| SCR-001-A01 | Open Case Queue with authorized context | Request `GET /v1/cases?cursor=...`; use server authorization and cursor pagination | Display returned cases and current status summary | Apply SCR-COM-011; never expose unauthorized rows | **Confirmed list API and screen.** [DDS], pp. 57–59, §§16.1–16.4. |
| SCR-001-A02 | Activate a case reference/row | Read the selected authorized current case | **Proposal:** navigate to SCR-002 with canonical case context | Non-disclosing not-found or safe dependency error | Case-opening activity is **Confirmed**; row gesture/destination binding is **Proposal**. [DDS], p. 11, §2.1.1; p. 83, §A.2. |
| SCR-001-A03 | Request another list page when a server cursor is available | Send the server-supplied cursor; do not create an offset-pagination contract | Display the returned cursor page | Safe pagination/request error; exact retained-list behavior undefined | **Confirmed cursor pagination.** [DDS], p. 54, §15.1.1; p. 57, §16.1.1. |
| SCR-001-A04 | Create-case entry | Source confirms Analyst case creation but not its launch control | **Proposal:** launch a new-case mode associated with SCR-002 | Unauthorized creation must be rejected by server | **Confirmed activity; placement and button need confirmation.** [DDS], pp. 11–12, Chapter 2; p. 83, §A.2. |

**Needs confirmation:**

- **OQ-SCR-005:** Confirm create-case entry, dedicated screen versus modal/mode, submitted fields, and success destination.
- **OQ-SCR-004:** Confirm list response properties, title limits, mandatory columns, and presentation of missing values.
- **OQ-SCR-001 / OQ-SCR-011:** Page size, initial ordering, selectable sort columns, filters, case-text search, previous-page behavior, total counts, and empty/loading states are not specified. The illustrated descending business numbers are not a confirmed sorting rule.
- The title `Risk Prioritization` does not establish an editable priority filter or an AI-defined priority ordering.

<a id="scr-002"></a>
### SCR-002 — Case Detail

#### Case and Intake Fields

Case-data placement below is a **Proposal** unless explicitly identified as illustrated or described UI content. The data and business rules are confirmed.

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and validation timing | Display/value source | Status and source |
|---|---|---|---|---|---|---|
| SCR-002-F01 | Case ID | `UUID`; identifiers use UUIDv7. Business-number format unresolved. | D; server-generated identifier | Tenant-scoped identity; not user-editable | `cases.id` / authorized case response | **Confirmed data.** [DDS], pp. 51, 85–86, §§14.1.1 and B.1–B.2. |
| SCR-002-F02 | Title | Exact type, length, accepted characters, and multiline behavior undefined | I in proposed intake/edit mode; D otherwise | Authorized case update; client timing unspecified | User business context/current case | **Confirmed data; Proposal input placement.** [DDS], p. 24, §6.1.2. OQ-SCR-004. |
| SCR-002-F03 | Description | Exact type/length/format undefined | I in proposed intake/edit mode; D otherwise | Must be validated user input; rich-text/Markdown support not specified | User business context/current case | **Confirmed data; Proposal placement.** [DDS], pp. 12, 24, §§2.2.1 and 6.1.2. |
| SCR-002-F04 | Impact | Explicit business input used to derive priority; type/range/vocabulary undefined | I | Priority must not derive from model output alone | Selectable values and initial value need confirmation | **Confirmed input concept; Proposal placement.** [DDS], p. 25, §6.3.1. OQ-SCR-008. |
| SCR-002-F05 | Urgency | Explicit business input; type/range/vocabulary undefined | I | Combined with impact by an undefined deterministic rule | Selectable values need confirmation | **Confirmed input concept; Proposal placement.** [DDS], p. 25, §6.3.1. |
| SCR-002-F06 | Priority | Derived business value; type/labels/range undefined | D; initial derivation undefined; no direct edit rule confirmed | Derived from explicit impact and urgency, never model output alone | Business rule result | **Confirmed rule/data; Proposal placement.** [DDS], pp. 24–25, §§6.1.2 and 6.3.1. |
| SCR-002-F07 | Sensitivity label | DDL `TEXT NOT NULL`; classification vocabulary `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED` | Server default `INTERNAL`; user editability and form-required behavior unresolved | Maximum included material class governs model route, redaction, retention, and approval | Current case / classification policy | **Confirmed data/default/classes; Proposal input placement.** [DDS], p. 62, §17.2.1; p. 86, §B.2. |
| SCR-002-F08 | Case status | DDL `TEXT NOT NULL`; `NEW`, `TRIAGED`, `IN_PROGRESS`, `PENDING_APPROVAL`, `RESOLVED`, `CLOSED` | D; creation starts `NEW`; direct status input not confirmed | Only guarded valid transitions; role, revision, and approval requirements apply | Current case state | **Confirmed.** [DDS], pp. 12, 25, 82, 86. OQ-SCR-006 and OQ-SCR-018. |
| SCR-002-F09 | Owner | Identifier/relationship; exact API type and selection source undefined | D; editable owner selector not confirmed | Update scope is `Owner`; assignment/reassignment rules undefined | Current case / authorized membership data if approved | **Confirmed data; Proposal placement.** [DDS], p. 24, §6.1.2; p. 83, §A.2. OQ-SCR-003. |
| SCR-002-F10 | Revision | `BIGINT NOT NULL DEFAULT 1`; monotonic | D; server-managed, not editable | Submit applicable revision through `If-Match`; detect conflicts | Current case revision | **Confirmed.** [DDS], p. 25, §6.2.2; p. 86, §B.2. |
| SCR-002-F11 | Current approved result | Pointer/artifact; full response structure and length undefined | D; absent/nullable behavior undefined before publication | Only satisfied gate may update final response pointer; closure preserves lineage | Approved artifact | **Confirmed data/rule; Proposal placement.** [DDS], p. 24, §6.1.2; pp. 45–46, §12.3.1. |
| SCR-002-F12 | Created time | `TIMESTAMPTZ NOT NULL DEFAULT now()`; public timestamps use RFC 3339 | D; server-generated | Display workspace-local time with timezone label | `created_at` | **Confirmed data; Proposal placement.** [DDS], p. 59, §16.3.2; p. 86, §B.2. |
| SCR-002-F13 | Updated time | `TIMESTAMPTZ NOT NULL DEFAULT now()` in reference DDL | D; update-maintenance mechanism undefined | Do not assume an update trigger from the shown DDL | `updated_at` | **Confirmed data; Proposal placement.** [DDS], p. 86, §B.2. |
| SCR-002-F14 | Classification labels | Label collection; schema, count, and label vocabulary undefined | D for generated labels; correction capability confirmed | Corrections require a reason code; correction permissions and endpoint undefined | Asynchronous classification result | **Confirmed behavior/data; Proposal placement.** [DDS], p. 12, §2.2.1. |
| SCR-002-F15 | Classification confidences | Numeric/band presentation; type, scale, precision, and limits undefined | D | Do not invent confidence thresholds or equate them to policy authority | Classification result | **Confirmed data; Proposal placement.** [DDS], p. 12, §2.2.1. |
| SCR-002-F16 | Classification provenance | Structured metadata; schema undefined | D | Preserve provenance; do not overwrite evidence history through label editing | Classification job result | **Confirmed data; Proposal placement.** [DDS], p. 12, §2.2.1. |
| SCR-002-F17 | Label-correction reason code | Type, length, and vocabulary undefined | Required when correcting labels; initial value unknown; editable during correction | Validate on correction submission; exact local timing undefined | Selectable-value source needs confirmation | **Confirmed conditional requirement; Proposal control placement.** [DDS], p. 12, §2.2.1. |
| SCR-002-F18 | Attachment selection | File input placement is a Proposal. R1 supports PDF, DOCX, HTML, UTF-8 text. | A file is necessary for an upload; case creation itself is not confirmed to require attachments | MIME signature and extension must agree; configurable 25 MB per-file cap; scan before parsing | User-selected file | **Confirmed upload contract; Proposal control.** [DDS], p. 30, §8.1; p. 83, §A.2. |
| SCR-002-F19 | OCR fallback opt-in | Opt-in setting; wire type/control undefined | Default is not specified; editable opt-in placement needs confirmation | OCR fallback is opt-in and provenance-marked; beyond-English OCR is deferred | Ingestion request/configuration path undefined | **Confirmed behavior; Proposal placement.** [DDS], p. 31, §8.2.1; p. 10, §1.3.2. |
| SCR-002-F20 | Attachment/document status | `ACCEPTED`, `SCANNING`, `EXTRACTING`, `INDEXING`, `READY`, `QUARANTINED`; exact wire type undefined | D; server state following accepted ingestion | `READY` must not be claimed before indexing/quality conditions are met | Document-status service | **Confirmed states; Proposal placement.** [DDS], p. 82, §A.1; pp. 30–32, Chapter 8. |
| SCR-002-F21 | Extraction quality flags | Empty-page ratio, unknown-character ratio, table-loss indicators, language confidence; types/thresholds undefined | D | Low-quality documents remain viewable but are excluded from autonomous recommendations | Extraction result | **Confirmed data/rule; Proposal placement.** [DDS], p. 32, §8.3.2. |
| SCR-002-F22 | Draft request/business context | Validated user input; exact public request schema, type, length, and required fields undefined | I; editability/control placement is a Proposal | Input validation before run allocation and tool/model processing | Analyst input and current case context | **Confirmed request activity; Proposal field placement.** [DDS], p. 12, §2.2.2; p. 38, §10.2.1. |
| SCR-002-F23 | Financial impact category | Normalized policy input; vocabulary/type undefined | Source does not confirm a user input control or initial category | Must not imply irreversible financial transaction functionality | Policy evaluation inputs | **Confirmed policy datum; Proposal placement only if approved.** [DDS], p. 44, §12.1.1. |
| SCR-002-F24 | SLA deadline | Business-calendar/timezone result; exact field/API format undefined beyond shared timestamps | D; derivation undefined until impact/urgency/calendar rules resolve | Breach prediction is advisory and cannot alter contractual deadlines | Workspace business calendar | **Confirmed business rule; Proposal display.** [DDS], p. 25, §6.3.1. |

#### Draft and Decision-Gate Fields

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and validation timing | Display/value source | Status and source |
|---|---|---|---|---|---|---|
| SCR-002-F25 | Candidate artifact — AI-generated proposed answer | Artifact structure/content length undefined | D; no in-place candidate editor is confirmed | Must be distinguished from approved result; invalid output must not publish | Current run artifact | **Confirmed reviewable content; Proposal placement on detail.** [DDS], p. 58, §16.2.2. |
| SCR-002-F26 | Artifact status | Literal labels `DRAFT`, `NEEDS_REVIEW`, `PUBLISHED` | D | Accessible status text; never show partial processing as approved | Server artifact/publication state | **Confirmed UI requirement.** [DDS], pp. 13, 57, §§2.3.2 and 16.1.2. |
| SCR-002-F27 | Source citations | Citation collection; public `Citation` schema not supplied | D; count/mandatory response-property details unresolved | Verify before display; only resolvable anchors with current permission may be cited | Evidence set | **Confirmed.** [DDS], p. 31, §8.3.1; p. 35, §9.3.1. |
| SCR-002-F28 | Model version/deployment metadata | Version/reference text; exact public schema undefined | D; not an implicit model selector | Must identify the actual approved route used | Run/model invocation metadata | **Confirmed review datum; illustrated model label.** [DDS], p. 7; p. 58, §16.2.2. |
| SCR-002-F29 | Prompt version | Version/digest metadata; type and format undefined | D; not editable as reviewed evidence | Bind review context to actual prompt/template version | Run/prompt metadata | **Confirmed review datum; Proposal detail placement.** [DDS], p. 58, §16.2.2. |
| SCR-002-F30 | Policy outcome | `AUTO_ALLOW`, `HUMAN_REVIEW`, `REQUEST_MORE_EVIDENCE`, `DENY` | D | An LLM cannot override the outcome | Versioned deterministic policy evaluation | **Confirmed data and illustrated gate.** [DDS], p. 44, §12.1.2; p. 7. |
| SCR-002-F31 | Policy reasons | Explanation/reason data; schema/length undefined | D | Reflect stored normalized inputs and rule-set version, not model-generated authorization | Policy evaluation | **Confirmed review datum; Proposal detail placement.** [DDS], p. 44, §12.1.1; p. 58, §16.2.2. |
| SCR-002-F32 | Approval assignment | Reviewer/task status; schema undefined | D | Assignment depends on policy pools, role, and separation of duties | Approval task/assignment | **Confirmed data and illustration.** [DDS], pp. 12, 45; p. 7. |
| SCR-002-F33 | Decision-gate status | Text/status metadata; no complete enumeration | D | Do not mark satisfied while approval/evidence/authorization is incomplete | Publication gate | **Illustration confirmed; mapping unresolved.** Sample `Awaiting decision`. [DDS], p. 7; pp. 45–46. |
| SCR-002-F34 | Verified citation count | Count display; derivation and numeric type undefined | D | Count only verified citations under the defined verification contract | Evidence verification result | **Illustration confirmed.** Sample `5 verified citations`, not a fixed requirement. [DDS], p. 7. |

#### Actions and Procedures

| ID | Button/event and execution conditions | Processing | Successful display/navigation | Failure display | Status and source |
|---|---|---|---|---|---|
| SCR-002-A01 | Open existing authorized case | `GET /v1/cases/{caseId}` returns authorized current revision | Display case and available evidence/run/gate data | Non-disclosing not-found or safe dependency failure | **Confirmed read API.** [DDS], p. 83, §A.2. |
| SCR-002-A02 | Submit new case as Analyst | `POST /v1/cases` with idempotency key; validate input; create case in `NEW`; classification is asynchronous | HTTP `201`, case identifier; exact success destination unresolved | Schema/idempotency/authorization/dependency failure; do not show a created case without authoritative outcome | **Confirmed operation; new-case mode is Proposal.** [DDS], pp. 11–12; p. 83; p. 89, `TST-001`–`TST-002`. |
| SCR-002-A03 | Save authorized case changes | `PATCH /v1/cases/{caseId}` using `If-Match`; validate business rules and ownership predicate | HTTP `200`; display accepted current revision | HTTP `409` `CASE_VERSION_CONFLICT` with current revision; no stale write accepted | **Confirmed operation; button design unresolved.** [DDS], p. 25, §6.2.2; pp. 83–84. |
| SCR-002-A04 | Correct a classification label | Submit corrected labels with reason code through an undefined mutation contract | Display accepted correction and preserved provenance | Safe validation/permission/version failure; exact codes undefined | **Confirmed behavior; endpoint and control unresolved.** [DDS], p. 12, §2.2.1. |
| SCR-002-A05 | Upload attachment as Analyst to authorized case | `POST /v1/cases/{caseId}/attachments`; validate type/size, scan, disable macros, do not fetch embedded remote references; perform bounded extraction/indexing | HTTP `202`, ingestion operation; show authoritative document state, not immediate readiness | Reject invalid input; unsafe content enters `QUARANTINED` and never enters index | **Confirmed.** [DDS], pp. 30–32; p. 83; p. 89, `TST-015`. |
| SCR-002-A06 | Receive/load attachment status | `GET /v1/documents/{documentId}/status` | Show current ingestion state and available quality/provenance | Safe status-read failure; do not manufacture completion | **Confirmed API; update mechanism undefined.** [DDS], pp. 30–32, §§8.1–8.4. |
| SCR-002-A07 | Request grounded draft as Analyst | `POST /v1/cases/{caseId}/runs` with idempotency; admission/policy/input checks; allocate bounded workflow | HTTP `202`; run created immediately; subscribe to SSE and show stages. **Proposal:** show progress here and offer SCR-004. | HTTP `429` with `Retry-After` when throttled; safe permanent/transient errors; no implied draft/publication | **Confirmed operation/progress.** [DDS], p. 58, §16.2.1; p. 69, §19.2.1; p. 83, §A.2. |
| SCR-002-A08 | Activate citation | Verify current permitted evidence and source anchor | Open source document and highlight anchored page range in evidence workflow | Safe denied/missing/invalid-anchor outcome; exact display copy undefined | **Confirmed.** [DDS], p. 31, §8.3.1; p. 57, §16.1.2. |
| SCR-002-A09 | Close case | `POST /v1/cases/{caseId}/close`; apply confirmed revision/authorization requirements and snapshot approved answer, cited versions, reviewer decisions | Preserve immutable approved-output lineage; show accepted closed state only after server confirmation | Reject unauthorized/stale/invalid transition without business mutation; exact response codes undefined | **Confirmed operation; allowed predecessor state and permission unresolved.** [DDS], pp. 24–26, Chapter 6. |
| SCR-002-A10 | Reopen closed case | Only explicitly as a new revision; no endpoint/guard/control provided | Preserve prior closed lineage; accepted new revision if authorized by a resolved contract | Must not overwrite closed approved lineage | **Confirmed exception; interaction needs confirmation.** [DDS], p. 25, §6.2.1. |
| SCR-002-A11 | Rework denied recommendation | Create a new run revision; no retroactive approval of denied output | New candidate follows retrieval/generation/policy/review controls again | Keep prior denial immutable; do not reuse approval for changed content | **Confirmed rule; UI launch and revision contract unresolved.** [DDS], p. 46, §12.3.2; p. 75, §21.3.1. |
| SCR-002-A12 | Publication status update | Server atomically satisfies gate and updates final response pointer; re-evaluate authorization/evidence and bind exact approved hash | Display `PUBLISHED` only for the authoritative published artifact | Stale evidence, insufficient approval, replay with different artifact, or policy denial cannot publish | **Confirmed event-driven outcome; no Publish button or public publish endpoint is specified.** [DDS], pp. 13, 45–46, §§2.5 and 12.3.1. |

#### Confirmed Lifecycle Rules

1. A new case begins in `NEW`.
2. `NEW` may transition to `TRIAGED`.
3. `TRIAGED` may transition to `IN_PROGRESS`.
4. `IN_PROGRESS` may transition to `PENDING_APPROVAL` or `RESOLVED`.
5. `PENDING_APPROVAL` may transition to `RESOLVED` or back to `IN_PROGRESS`.
6. `CLOSED` is final unless explicitly reopened as a new revision.
7. Closing snapshots the approved answer, immutable cited document versions, and reviewer decisions.
8. Retention applies only to eligible closed cases and preserves legal-hold exceptions.

**Source:** [DDS], pp. 25–26, §§6.2–6.3.

The source does not explicitly enumerate `RESOLVED -> CLOSED` in §6.2.1 despite providing a close operation. Do not infer all closure guards from the endpoint name.

**Needs confirmation:**

- **OQ-SCR-004:** Title/description/input lengths, required fields, formats, allowed characters, initial form values, nullable fields, editable field set, and local validation timing.
- **OQ-SCR-007:** Classification correction vocabulary, reason-code source, correction API, revision behavior, classification failure display, and which user may correct labels.
- **OQ-SCR-008:** Impact/urgency vocabularies, priority formula, business calendars, workspace timezone source, deadline rules, and advisory breach-prediction presentation.
- **OQ-SCR-009:** Exact MIME/extension allowlist, meaning of MB, inclusive size boundary, decompression threshold, upload count limits, OCR configuration path, quality thresholds, document-state update mechanism, and safe handling of quarantined content. Attachment removal is not specified.
- **OQ-SCR-012:** Reconcile alternate `POST /v1/runs` with the case-scoped run endpoint; define run-revision/rework and recoverable-timeout behavior.
- **OQ-SCR-016:** Define whether any user-invoked publication action exists, its permission and endpoint, and how a recorded review decision becomes visibly published.
- **OQ-SCR-018:** Confirm closure predecessor states, closure/reopen roles, preconditions, response contracts, and reopen navigation.

<a id="scr-003"></a>
### SCR-003 — Evidence Viewer

#### Fields

Search controls are **Proposal placement** because search capability is confirmed but its UI placement is not.

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and validation timing | Display/value source | Status and source |
|---|---|---|---|---|---|---|
| SCR-003-F01 | Search query | Public request schema/length undefined. Internal `knowledge.search@v1` uses `query: string`; that does not establish the public schema. | I; Proposal input | Validate before retrieval; exact empty-query and normalization rules undefined | User query | **Confirmed search activity; Proposal control.** [DDS], pp. 34–36; p. 87, §C.2. |
| SCR-003-F02 | Evidence scope — case/workspace context | Domain references are UUIDs; public search scope schema undefined | D if context-bound; editable scope selector not confirmed | Never expand tenant/workspace/document access by client input | Authorized case/workspace context | **Confirmed scope rules; Proposal display.** [DDS], pp. 22, 34; p. 87. |
| SCR-003-F03 | Citation reference/chunk ID | Opaque citation reference; chunk identifiers exist; display format undefined | D | Verify before display; must not be a user-editable authorization token | Evidence item | **Confirmed contract.** [DDS], p. 35, §9.3.1. |
| SCR-003-F04 | Source title | Type/length undefined | D | Show only permitted metadata | Response evidence item | **Confirmed.** [DDS], p. 35, §9.3.1. |
| SCR-003-F05 | Document revision/version | Immutable version reference; revision type/display format undefined | D | Must refer to the cited stored version, not silently substitute latest content | Evidence item/document version | **Confirmed.** [DDS], pp. 31, 35, §§8.2.2 and 9.3.1. |
| SCR-003-F06 | Page anchor/range | Page number and anchored page range; numbering basis/schema undefined | D | Must resolve to stored source anchors; highlight cited range | Chunk/evidence anchor | **Confirmed.** [DDS], p. 31, §8.3.1; p. 57, §16.1.2. |
| SCR-003-F07 | Source URI | URI metadata; allowed schemes/public rendering undefined | D; user-supplied arbitrary URL input not confirmed | Do not use evidence text as unrestricted browsing authority | Stored source anchor | **Confirmed metadata; Proposal display.** [DDS], p. 31, §8.3.1; p. 87, §C.2. |
| SCR-003-F08 | Source file hash | Immutable content fingerprint; exact public encoding undefined | D | Preserve source identity; do not infer every display digest uses the same encoding | Stored document version | **Confirmed metadata; Proposal display.** [DDS], pp. 31, 85. |
| SCR-003-F09 | Bounding box | Optional source anchor metadata; coordinate schema/unit undefined | Optional in source anchor; D | Resolve to the correct cited page; no invented coordinate convention | Chunk layout metadata | **Confirmed optional metadata.** [DDS], p. 31, §§8.2.1 and 8.3.1. |
| SCR-003-F10 | Source document/page content | Stored source/layout/text; rendering format/length undefined | D | Reviewer must be able to inspect source before approval; low-quality content remains viewable if authorized | Access-controlled stored source | **Confirmed viewer behavior.** [DDS], p. 32, §8.3.2; pp. 57–58. |
| SCR-003-F11 | ACL digest | Evidence contract metadata; exact type/encoding undefined | D as protocol metadata; user-visible display not confirmed | Current permission required; digest is not permission authority | Evidence item | **Confirmed metadata; display placement needs confirmation.** [DDS], p. 35, §9.3.1. |
| SCR-003-F12 | Extraction quality flags | As defined in SCR-002-F21; thresholds/format unknown | D | Low-quality evidence cannot support autonomous recommendations | Extraction metadata | **Confirmed data; Proposal viewer display.** [DDS], p. 32, §8.3.2. |
| SCR-003-F13 | OCR provenance indicator | Provenance-marked OCR result; schema undefined | D | Must identify OCR-derived material where fallback occurred | Normalized derivative metadata | **Confirmed provenance; Proposal display.** [DDS], p. 31, §8.2.1. |
| SCR-003-F14 | Reduced-quality retrieval flag | Visible flag; exact field/text/enum undefined | D when lexical-only degraded retrieval continues | Must not conceal degraded retrieval quality | Retrieval/degraded-state result | **Confirmed visible condition.** [DDS], p. 69, §19.2.2. |

#### Actions and Search Behavior

| ID | Button/event and execution conditions | Processing | Successful display/navigation | Failure display | Status and source |
|---|---|---|---|---|---|
| SCR-003-A01 | Load authorized case evidence | `GET /v1/cases/{caseId}/evidence` | Display permitted evidence metadata/citations | Safe resource/dependency failure | **Confirmed API.** [DDS], pp. 57–59, §§16.1–16.4. |
| SCR-003-A02 | Search permitted evidence as authorized Member | `POST /v1/search`; form lexical/vector queries; merge bounded candidates using reciprocal rank fusion and deterministic reranking; apply diversity and token budgets; enforce ACLs | HTTP `200`; display permitted results and provenance. Search-result UI placement is a Proposal. | `NO_SUPPORTED_EVIDENCE` when confidence/quality is insufficient; no fabricated context | **Confirmed retrieval behavior; UI control unresolved.** [DDS], pp. 34–36, Chapter 9; p. 83, §A.2. |
| SCR-003-A03 | Open an evidence item/citation | `GET /v1/evidence/{evidenceId}` and source access under current permission; browser-facing source-download mechanism undefined | Open cited stored source and highlight anchored page range | Do not show unauthorized or unresolvable content; exact stale-anchor display undefined | **Confirmed evidence API and click-through requirement.** [DDS], pp. 34–36; p. 57, §16.1.2. |
| SCR-003-A04 | Query after source access revocation | ACL changes invalidate affected caches before new results are served | No forbidden evidence on the next query | Stale visibility is a security incident, not a normal tolerated result | **Confirmed.** [DDS], pp. 27–29, §§7.1–7.2; p. 89, `TST-004`. |
| SCR-003-A05 | Vector retrieval degradation | Lexical retrieval may continue while authorization/policy controls remain enforced | Results include a visible reduced-quality flag | If safe retrieval cannot continue, no unsupported result is fabricated | **Confirmed optional degraded behavior.** [DDS], p. 69, §19.2.2. |

The source example has:

- `max_candidate_chunks: 80`
- `max_selected_chunks: 10`
- `hybrid_rrf_k: 60`
- `embed_dimension: 1536`

The internal MCP tool has `max_items: int<=10`. These are retrieval/tool configuration constraints, **not** confirmed screen page sizes or a user-editable “maximum results” field.  
**Source:** [DDS], p. 87, §C.2; p. 90, Appendix F.

**Needs confirmation:**

- **OQ-SCR-010:** Browser-facing source retrieval/signed-URL endpoint, URL lifetime, anchor structure, page numbering, bounding-box coordinates, highlight semantics, DOCX/HTML/text anchor presentation, invalid-anchor behavior, and return-to-origin navigation.
- **OQ-SCR-011:** Public search request/response schema, query requiredness/length, filters, sort controls, result ordering display, result pagination, score presentation, empty-query behavior, and clarification/human-routing UI.
- **OQ-SCR-009:** Safe viewing of quarantined documents is not established by the low-quality-document exception. Do not render quarantined active content by assuming it is merely low-quality.
- No in-document search, zoom, download, print, annotation editor, or page-jump control is confirmed. These require explicit approval if desired.

<a id="scr-004"></a>
### SCR-004 — Run Timeline

#### Fields

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and validation timing | Display/value source | Status and source |
|---|---|---|---|---|---|---|
| SCR-004-F01 | Run ID | Identifier; UUIDv7 baseline | D; server-managed | Authorized run scope | Run record | **Confirmed data; Proposal visible placement.** [DDS], pp. 51, 85. |
| SCR-004-F02 | Case reference | Immutable case/run association; UUID domain reference | D | Do not substitute foreign-tenant case | Run record | **Confirmed data; Proposal link.** [DDS], pp. 24, 85. |
| SCR-004-F03 | Run status | `REQUESTED`, `RETRIEVING`, `GENERATING`, `POLICY_CHECK`, `AWAITING_REVIEW`, `PUBLISHED`, `FAILED` | D; begins at allocated server state | Server state is authoritative; no client-only progress reconstruction | Run API/SSE | **Confirmed visible progression/states.** [DDS], p. 49, §13.2.1; p. 58, §16.2.1; p. 82, §A.1. |
| SCR-004-F04 | Execution step | `step_kind`, status, checkpoint exist; exact types/enums undefined | D | Steps must be idempotent; preserve accepted execution history | `run_steps` / steps API | **Confirmed data and human-visible trace; layout unresolved.** [DDS], pp. 40–42; p. 85, §B.1. |
| SCR-004-F05 | Checkpoint | Checkpoint metadata; schema undefined | D | Each stage persists checkpoint before downstream dispatch | Workflow/step records | **Confirmed.** [DDS], p. 49, §13.2.1. |
| SCR-004-F06 | Plan revision | Exact type undefined | D; server-managed | Plan revision stored before side effects | Run plan metadata | **Confirmed data; Proposal display.** [DDS], p. 40, §11.1.2. |
| SCR-004-F07 | Runtime/call/token budget | Budget object/units undefined | D; no editable budget control confirmed | Bounded depth/calls/time; workspace token budget applies | Run/workspace configuration | **Confirmed constraint; Proposal display.** [DDS], pp. 38, 40–41. |
| SCR-004-F08 | Failed checkpoint and cause | Visible checkpoint failure information; full code vocabulary undefined | D when failed | Report exactly which checkpoint failed, without secret/document leakage | Orchestrator failure result | **Confirmed visible requirement.** [DDS], p. 41, §11.3.1. |
| SCR-004-F09 | Evidence metadata | Evidence-set/citation metadata; full schema undefined | D | Authorized metadata only; current permission and anchor controls apply | Run read API | **Confirmed returned data.** [DDS], p. 83, §A.2. |
| SCR-004-F10 | Transition time | Event `occurred_at`; RFC 3339 public representation | D; visible timestamps are a Proposal | Workspace-local label; ordering uses authoritative event offsets/server state | Events/checkpoints | **Confirmed event time; Proposal timeline display.** [DDS], p. 48, §13.1.1; p. 59, §16.3.2. |
| SCR-004-F11 | Correlation/trace reference | Identifier strings; exact length/schema undefined | D if displayed; display is a Proposal | No source document text, secrets, or provider credentials in diagnostics | Safe run/error metadata | **Confirmed diagnostic metadata; display unresolved.** [DDS], p. 64, §18.1.1; p. 84, §A.3. |

#### Actions and Progress Procedure

1. Retrieve the authorized run with `GET /v1/runs/{runId}`.
2. Retrieve execution steps with `GET /v1/runs/{runId}/steps` where needed.
3. Subscribe to `GET /v1/streams/runs/{runId}`.
4. Apply monotonically increasing SSE event offsets.
5. On reconnect, use `Last-Event-ID` to backfill retained events within the caller’s scope.
6. On browser refresh, reconstruct progress from current server state, not ephemeral browser memory.
7. Announce meaningful state transitions accessibly.
8. Show authoritative terminal publication/failure or the unresolved recoverable-timeout representation. Never interpret an SSE disconnection as successful completion.

**Sources:** [DDS], pp. 40–42, Chapter 11; p. 55, §15.2.1; p. 58, §16.2.1; p. 83, §A.2.

| ID | Button/event and execution conditions | Processing | Successful display/navigation | Failure display | Status |
|---|---|---|---|---|---|
| SCR-004-A01 | Open/refresh authorized run | Read current run and steps | Restore current stages, evidence, and checkpoints | SCR-COM-011 | **Confirmed.** |
| SCR-004-A02 | Receive SSE update | Apply scoped monotonic update | Show meaningful accepted progression | Do not apply unauthorized private backfill | **Confirmed.** |
| SCR-004-A03 | Reconnect SSE | Resume using `Last-Event-ID` | Backfill retained scoped events | Retention-gap/expired-cursor behavior is undefined | **Confirmed resumption; exceptional behavior needs confirmation.** |
| SCR-004-A04 | Runtime stop/failure | Stop on exhausted call budget, repeated invalid plan, policy denial, deadline expiry, or missing approval as stated by §11.3.1 | Report the failed checkpoint | Do not substitute a denied action with a semantically equivalent tool | **Confirmed rule; missing-approval/waiting semantics conflict needs resolution.** |
| SCR-004-A05 | Inspect referenced evidence | Apply shared citation controls | Open permitted source evidence | Safe denied/unresolvable result | **Confirmed evidence-inspection capability; link placement is Proposal.** |

**Runtime constraints:** Maximum DAG depth eight and maximum sixteen tool invocations are explicit. Appendix F shows `run_timeout_seconds: 180`. The timeout’s treatment of human review is unresolved; it must not be assumed to be the reviewer task SLA.  
**Source:** [DDS], p. 40, §11.1.2; p. 90, Appendix F.

The Triage Agent classifies, Research Agent requests evidence, Draft Agent assembles the candidate, and Policy Evaluator is deterministic, not an LLM agent. The timeline must not represent a model-generated recommendation as a binding policy authorization.  
**Source:** [DDS], p. 40, §11.1.1; p. 44, §12.1.2.

**Needs confirmation:**

- **OQ-SCR-012:** Exact stop-state/error mapping, recoverable timeout, whether timeout pauses during review, alternate run-create endpoint, and any user cancellation/retry/resume control. None of those controls is confirmed.
- **OQ-SCR-013:** SSE payload schemas, retention duration, cursor-expiry/gap handling, duplicate/out-of-order UI handling, connection-state display, and steps pagination/order. No polling interval is supplied.
- **OQ-SCR-001:** Whether the timeline renders a graphical DAG or only stage/step history; a DAG data model does not confirm a graphical editor or viewer.

<a id="scr-005"></a>
### SCR-005 — Review Inbox

#### Fields

The exact candidate, citations, model/prompt version, policy reasons, and Approve/Reject controls are explicit UI requirements. Other task metadata placement is proposed.

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and validation timing | Display/value source | Status and source |
|---|---|---|---|---|---|---|
| SCR-005-F01 | Approval task ID | Identifier; UUIDv7 baseline; public response schema undefined | D | Tenant/task scope | Approval task | **Confirmed data; Proposal display.** [DDS], pp. 45, 85. |
| SCR-005-F02 | Case/run references | Immutable reference data; public schema undefined | D | Only authorized related resources | Approval task/run | **Confirmed association; Proposal links.** [DDS], p. 85, §B.1. |
| SCR-005-F03 | Reviewer pool/assignment | Policy-defined pool/reference; type/vocabulary undefined | D; manual selection not confirmed | Minimum role and separation of duties apply | Versioned routing policy/task | **Confirmed data/rule; Proposal display.** [DDS], p. 45, §12.2.1. |
| SCR-005-F04 | Required role/separation-of-duty summary | Policy attributes; schema undefined | D; not editable within a decision | Must not grant approval from UI selection | Approval policy | **Confirmed rule; Proposal display.** [DDS], p. 45, §12.2.1. |
| SCR-005-F05 | Review state | `ASSIGNED`, `OPENED`, `APPROVED`, `REJECTED`, `EXPIRED` | D; server-managed | State guarded by actor, content hash, separation of duties | Review task | **Confirmed states.** [DDS], p. 82, §A.1. |
| SCR-005-F06 | Review expiry/deadline | Configured SLA/time result; exact field/format undefined beyond shared timestamp rules | D; no invented SLA/default | Expiry causes reassignment/escalation, never implicit approval | Task/routing policy | **Confirmed rule; Proposal display.** [DDS], p. 45, §12.2.1. |
| SCR-005-F07 | Exact candidate artifact | Artifact structure/length undefined | D; read-only reviewed content | Must be the exact content bound to decision; changed artifact makes decision stale | Immutable candidate artifact | **Confirmed UI requirement.** [DDS], p. 58, §16.2.2. |
| SCR-005-F08 | Evaluated artifact hash | Hash binding exists; wire format/encoding undefined | Required in approval record; not a user-editable approval override | Verify exact reviewed content at decision submission | Candidate/task hash | **Confirmed binding; visible hash placement unresolved.** [DDS], pp. 44–45, §§12.1–12.2.2. |
| SCR-005-F09 | Source citations/evidence panel | Citation collection/anchor data | D | Reviewer can inspect source before approval; current ACLs apply | Evidence set/source viewer | **Confirmed UI requirement.** [DDS], pp. 57–59, Chapter 16. |
| SCR-005-F10 | Model version | Metadata; schema/length undefined | D | Actual used model/deployment, not arbitrary selection | Run metadata | **Confirmed UI requirement.** [DDS], p. 58, §16.2.2. |
| SCR-005-F11 | Prompt version | Metadata; schema/length undefined | D | Actual prompt/template version reviewed | Run/prompt metadata | **Confirmed UI requirement.** [DDS], p. 58, §16.2.2. |
| SCR-005-F12 | Policy outcome/reasons | Outcome vocabulary as SCR-002-F30; reason schema undefined | D | Deterministic result cannot be changed by model text or review-form editing | Policy evaluation | **Confirmed UI requirement.** [DDS], p. 44, §12.1.2; p. 58, §16.2.2. |
| SCR-005-F13 | Decision | Captured decision; exact wire enum is not supplied | Required in decision record; no initial selection defined | Approve/Reject controls initiate decision. `APPROVED`/`REJECTED` are confirmed review states, not a fully specified request enum. | Reviewer action | **Confirmed capture/control; enum needs confirmation.** [DDS], p. 45, §12.2.2; p. 58, §16.2.2. |
| SCR-005-F14 | Rationale/reason | Captured rationale; exact type/length and nonblank rule undefined | Record includes rationale; exact required-review-field/nonblank rule needs confirmation; editable proposed input | Completion gating applies to required review fields; validate authoritatively on submit | Reviewer input | **Confirmed record datum; control contract unresolved.** [DDS], p. 45, §12.2.2; p. 85, §B.1. |
| SCR-005-F15 | Annotations | Optional annotations; format/count/length undefined | Optional; initial value undefined; editable control placement is Proposal | Annotation semantics and redaction unresolved | Reviewer input | **Confirmed optional data; Proposal control.** [DDS], p. 45, §12.2.2. |
| SCR-005-F16 | Decision actor | Actor identity; schema/display name unresolved | Required in record; server-authenticated, not editable | Must be authorized reviewer and satisfy separation of duties | Authenticated principal | **Confirmed capture.** [DDS], p. 45, §12.2.2. |
| SCR-005-F17 | Decision timestamp | Timestamp; RFC 3339/UTC durable representation | Required in record; server-managed | Workspace-local display; immutable decision history | Decision record | **Confirmed capture.** [DDS], pp. 45, 54, 59. |
| SCR-005-F18 | Normalized policy inputs/rule version | Sensitivity, requested action, evidence quality, model class, financial impact category, confidence bands; schemas undefined | D; detailed panel is Proposal | Store normalized inputs with rule-set version; model tags cannot override outcome | Policy evaluation | **Confirmed data; Proposal detailed display.** [DDS], p. 44, §12.1.1. |

#### Review Procedure

1. Load authorized work from `GET /v1/review-queue`.
2. Open a task and show the exact candidate, source citations, model version, prompt version, and policy reasons.
3. Permit inspection of source evidence before approval.
4. Collect required review fields. Disable both **Approve** and **Reject** until those fields are complete.
5. Submit `POST /v1/approvals/{approvalId}/decision` with the reviewed-artifact binding.
6. Re-evaluate actor authorization, task validity/expiry, separation of duties, and exact content hash.
7. Record decision, actor, timestamp, artifact hash, rationale, and optional annotations.
8. Show the accepted decision only after server confirmation.
9. Show `PUBLISHED` only when the server reports successful publication-gate completion, not merely because an approval submission returned success.

**Sources:** [DDS], pp. 44–46, Chapter 12; p. 58, §16.2.2; p. 83, §A.2.

| ID | Button/event and execution conditions | Processing | Successful display/navigation | Failure display | Status and source |
|---|---|---|---|---|---|
| SCR-005-A01 | Load Review Inbox | `GET /v1/review-queue` under permitted reviewer scope | Show authorized tasks and status | Safe denied/read failure | **Confirmed API/screen; list columns/filtering undefined.** [DDS], p. 45; p. 57. |
| SCR-005-A02 | Open review task | Display exact review context; source names `UserReviewOpened` as auditable event | Show evidence-inspection and decision interface | Fail safely if task/context cannot be obtained | **Confirmed review-open activity/event name; detailed event/request contract unresolved.** [DDS], pp. 57–59. |
| SCR-005-A03 | Inspect citation | Apply SCR-COM-006 and SCR-003-A03 | Open permitted source and highlight anchor | No unauthorized source disclosure | **Confirmed.** [DDS], p. 57, Chapter 16 invariant and §16.1.2. |
| SCR-005-A04 | Approve with all required fields complete | Submit binding decision; reject self-approval where prohibited and stale content | HTTP `200`; record accepted decision; exact return destination undefined | HTTP `409` for changed reviewed hash; stable safe denial otherwise; no publication of changed artifact | **Confirmed control/operation.** [DDS], pp. 45, 58, 83; p. 89, `TST-006`. |
| SCR-005-A05 | Reject with all required fields complete | Submit rejection with required decision context | Record immutable rejection; denied output can be reworked as a new run revision | Safe validation/authorization/stale failure | **Confirmed control/rule.** [DDS], pp. 45–46; p. 58. |
| SCR-005-A06 | Task expires | Reassign or escalate using configured SLA/routing | Show authoritative expired/reassigned condition; escalation is recorded | Never silently approve | **Confirmed behavior.** [DDS], p. 45, §12.2.1; p. 89, `TST-010`. |
| SCR-005-A07 | Authorized override request | Require elevated role, secondary reviewer, and audited reason; exact endpoint/control undefined | Only accepted override follows an explicit resolved contract | Single-reviewer or unauthorized override cannot bypass policy | **Confirmed constraints; interaction unresolved.** [DDS], p. 46, §12.3.2. |

**Needs confirmation:**

- **OQ-SCR-014:** Task-detail retrieval endpoint/schema; decision request enum; exact mandatory review fields; rationale nonblank/length rules; annotation format; validation timing; button progress/failure presentation. The source requires ability to inspect evidence, not a particular “all citations clicked” checkbox or click-count rule.
- **OQ-SCR-015:** Reviewer pools, minimum roles, exact task SLA, reassignment/escalation routing, late decisions, and multi-reviewer conflict handling.
- **OQ-SCR-017:** Elevated override role, secondary reviewer selection, reason contract, override endpoint, and its navigation.
- **OQ-SCR-021:** Define the actual trigger/envelope for `UserReviewOpened`; the name appears in Chapter 16 but not the Appendix C event catalog.
- **OQ-SCR-001 / OQ-SCR-011:** Inbox pagination, sorting, filtering, empty states, and primary-action emphasis are unspecified.

<a id="scr-006"></a>
### SCR-006 — Connector Health

#### Fields

The screen name, warning conditions, and underlying connector/sync data are confirmed. Specific columns and controls are proposed where not explicitly described.

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and validation timing | Display/value source | Status and source |
|---|---|---|---|---|---|---|
| SCR-006-F01 | Connector identity/source | Identifier; provider/name schema undefined | D; provider selector/configuration control not confirmed | Workspace-scoped connector access | Connector record | **Confirmed data; Proposal display.** [DDS], pp. 27–29. |
| SCR-006-F02 | Advertised capabilities | List, fetch, delta cursor, ACL, delete support; wire types undefined | D | Unsupported capability triggers lower-trust mode and explicit warning | Connector capability discovery | **Confirmed visible warning requirement/data.** [DDS], p. 27, §7.1.1. |
| SCR-006-F03 | Ingestion trust-mode warning | Explicit user-visible warning; enum/text undefined | D when capabilities are unsupported | Never silently assume unsupported capability | Capability evaluation | **Confirmed UI condition.** [DDS], p. 27, §7.1.1. |
| SCR-006-F04 | Credential reference | Workspace-scoped secret-store reference; format undefined | D if exposed; raw token entry/display not confirmed | Credentials remain in secret store and must not appear in traces, prompts, or public responses | Workspace credential reference | **Confirmed storage rule; Proposal safe reference display.** [DDS], p. 27, §7.1.2; p. 54, Chapter 15 invariant. |
| SCR-006-F05 | Credential/reauthentication condition | `CONNECTOR_REAUTH_REQUIRED` failure identifier; complete status enum undefined | D | Revoked queued jobs fail without exposing tokens | Sync/credential outcome | **Confirmed condition.** [DDS], p. 27, §7.1.2. |
| SCR-006-F06 | Sync run identity/status | Run record; type/status enum undefined | D | Accepted sync is asynchronous; do not imply completion from `202` | Connector runs API | **Confirmed data; Proposal column.** [DDS], pp. 28–29; p. 83. |
| SCR-006-F07 | Provider cursor | Provider-specific cursor; schema/length undefined | D; not editable replay authority | Advance only after preceding items have durable ingestion outcomes | Sync checkpoint | **Confirmed data/rule; visibility needs confirmation.** [DDS], p. 28, §7.2.1. |
| SCR-006-F08 | High-watermark | Provider/checkpoint data; type undefined | D | Preserve durable checkpoint consistency | Sync run | **Confirmed data; Proposal display.** [DDS], p. 28, §7.2.1. |
| SCR-006-F09 | Error ledger | Exception collection; schema/count limits undefined | D | Partial batch may proceed while exceptions remain durably recorded | Sync run | **Confirmed data; Proposal display.** [DDS], pp. 28–29. |
| SCR-006-F10 | Quarantine reason code | Exact vocabulary/type undefined | D for quarantined record | Malformed records quarantine after bounded retries | Poison-record outcome | **Confirmed data; Proposal display.** [DDS], p. 29, §7.3.2. |
| SCR-006-F11 | Correlation ID | Identifier; length/format undefined | D if displayed | Non-sensitive remediation trace; no token leakage | Quarantine/error outcome | **Confirmed data; Proposal display.** [DDS], p. 29, §7.3.2. |
| SCR-006-F12 | Remediation path | Remediation metadata; link/action schema undefined | D; automated repair control not confirmed | Must not introduce unrestricted URLs/actions | Quarantine/error outcome | **Confirmed remediation datum; UI needs confirmation.** [DDS], p. 29, §7.3.2. |
| SCR-006-F13 | Provisioning/readiness status | Incomplete provisioning and index coverage; full status enum/formula undefined | D | Incomplete provisioning blocks sync. Search readiness depends on coverage, not queue emptiness alone. | Provisioning/index coverage | **Confirmed visible readiness conditions; Proposal placement.** [DDS], p. 78, §§22.1.1–22.1.2. |

#### Actions

| ID | Button/event and execution conditions | Processing | Successful display/navigation | Failure display | Status and source |
|---|---|---|---|---|---|
| SCR-006-A01 | Inspect connector sync history | `GET /v1/connectors/{connectorId}/runs` | Display permitted sync outcomes/checkpoints/errors | Safe read failure | **Confirmed API; list layout undefined.** [DDS], pp. 28–29. |
| SCR-006-A02 | Start sync as Admin for fully provisioned workspace | `POST /v1/connectors/{connectorId}/sync` with long-running-job idempotency; discover capabilities; incremental sync/checkpoint logic | HTTP `202`, persisted operation; display started/pending status and warnings | Block incomplete provisioning; show safe retryable error or `CONNECTOR_REAUTH_REQUIRED` as applicable | **Confirmed.** [DDS], pp. 27–29; p. 78; p. 83. |
| SCR-006-A03 | Credential revocation | Authorized operator revokes stored credentials through undefined contract | Queued jobs fail reauthentication-required; no secret exposed | Unauthorized action rejected; exact failure code undefined | **Confirmed operation; control/role/API unresolved.** [DDS], p. 27, §7.1.2. |
| SCR-006-A04 | Source delete/ACL-change update | Tombstone deletes and schedule index removal; invalidate caches before new retrieval results | No newly served revoked evidence; safe current status | Stale visibility treated as security incident | **Confirmed behavior.** [DDS], p. 28, §7.2.2. |
| SCR-006-A05 | Throttling or poison-record outcome | Honor `Retry-After`, bounded backoff/jitter, workspace quotas; quarantine malformed records after bounded retries | Show authoritative outcome/remediation; remaining batch may proceed with durable exception ledger | No false “all records synchronized” claim | **Confirmed processing; exact UI states undefined.** [DDS], pp. 28–29, §7.3. |

**Needs confirmation — OQ-SCR-019:** Define connector list/read/configure/delete/authenticate/reauthenticate/revoke APIs, exact providers and third-party permissions, operator role, capability schema, sync state vocabulary, run pagination/sorting, warnings, remediation actions, retry bounds, and lower-trust restrictions. Unsupported ACL capability must not be treated as permission to violate the “revoked access before next retrieval” invariant.

<a id="scr-007"></a>
### SCR-007 — Policy Settings

#### Fields

Workspace settings are confirmed. Their editable controls and read/write API are not. The following table is a **Proposal field placement**, not authorization to expose every configuration value as a form input.

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and validation timing | Display/selectable-value source | Source and open decision |
|---|---|---|---|---|---|---|
| SCR-007-F01 | Policy/configuration revision | Exact type/format undefined | C; server-managed revision | Configuration updates require revision preconditions and durable audit | Workspace/current policy | [DDS], p. 24, §6.1.1; p. 85, §B.1. |
| SCR-007-F02 | Retention class | Type/vocabulary undefined | C | Respect legal-hold exceptions; corporate retention selection unresolved | Approved retention policy | [DDS], pp. 24, 26; p. 90, §F.2. |
| SCR-007-F03 | Allowed model deployments | Deployment-reference collection; type/count undefined | C | Allowlist specific approved deployments, not broad provider brands; fallback equal/stronger data-handling class and approved region | `GET /v1/model-catalog` / approved registry; response/filtering undefined | [DDS], pp. 24, 37–39. |
| SCR-007-F04 | Connector credential references | Secret-reference collection; schema undefined | C for references only; secret-value form not confirmed | Secrets remain in vault-backed storage; no public credential disclosure | Workspace secret references | [DDS], pp. 24, 27, 71. |
| SCR-007-F05 | Approved toolsets/capabilities | Version-pinned references; schema/count undefined | C | Capability discovery is not authorization; browser cannot submit arbitrary tool definitions | Approved tool registry/workspace policy; selectable contract undefined | [DDS], p. 7; pp. 24, 41; p. 87, §C.2. |
| SCR-007-F06 | Reviewer routing/pools | Policy references; schema undefined | C | Enforce minimum role, separation of duties, assignment, expiry/escalation | Versioned reviewer policy | [DDS], pp. 24, 45. |
| SCR-007-F07 | Minimum reviewer role | Role predicate; values undefined | C | Cannot authorize self-approval or bypass task policy | Approved role/routing policy | [DDS], p. 45, §12.2.1. |
| SCR-007-F08 | Review task SLA | Duration/configuration; unit/value/range undefined | C | Expiry reassigns/escalates; never auto-approves | Approved routing policy | [DDS], p. 45, §12.2.1. |
| SCR-007-F09 | Workspace timezone/business calendar | Timezone/calendar references; identifier format undefined | C if screen editing is approved | Compute deadlines with business calendar; display timezone labels | Workspace calendar configuration | [DDS], p. 25, §6.3.1; p. 59, §16.3.2. |
| SCR-007-F10 | Workspace quota/budgets | Quota object; units/ranges undefined | C if editing is approved | AI admission/token/model budgets apply; exhaustion does not change model/data class automatically | Workspace quota and token policy | [DDS], pp. 38, 69, 85. |
| SCR-007-F11 | Policy rule-set version | Immutable/versioned identifier; type undefined | D/C; editing mechanism not defined | Normalize/store evaluated inputs with rule version | Policy registry/evaluation | [DDS], p. 44, §12.1.1. |
| SCR-007-F12 | Automatic publication classification | Example `auto_publish_classification: INTERNAL`; exact schema undefined | C; example value only | Does not mean every `INTERNAL` run is authorized to publish; evidence and all policy conditions still apply | Versioned policy configuration | [DDS], p. 90, Appendix F; pp. 44–46. |
| SCR-007-F13 | Human-review classifications/tags | Example `[HIGH_RISK, RESTRICTED]`; schema undefined | C; editable vocabulary unresolved | `HIGH_RISK` is a risk tag, not one of the four information classes | Versioned policy configuration | [DDS], p. 62, §17.2.1; p. 90, Appendix F. |
| SCR-007-F14 | Self-approval policy | Example `self_approval_allowed: false`; exact schema undefined | Existing baseline prohibits self-approval as documented; UI toggle is not confirmed | Do not expose an unapproved bypass toggle | Approved separation-of-duty policy | [DDS], pp. 11, 85, 90. |
| SCR-007-F15 | Runtime/retrieval/upload configuration | Example limits exist; field types/editability/ranges are not UI-defined | C only if editable settings are approved | Preserve source limits; no unsupported arbitrary increase or policy bypass | Approved deployment/workspace configuration | [DDS], pp. 30, 40, 90. |

#### Actions

| ID | Button/event and execution conditions | Processing | Successful display/navigation | Failure display | Status and source |
|---|---|---|---|---|---|
| SCR-007-A01 | Open authorized workspace policy | Read current approved settings through an undefined policy-read API | Show current revision/configuration | Safe read failure | **Confirmed screen/activity; API unresolved.** [DDS], pp. 24, 57. |
| SCR-007-A02 | Save configuration as authorized Admin | Use revision precondition, validate policy/domain rules, produce durable audit | Show accepted new revision only after authoritative success | Reject stale/unauthorized/invalid config; exact conflict code undefined | **Confirmed update constraints; endpoint/control unresolved.** [DDS], p. 24, §6.1.1. |
| SCR-007-A03 | Load available model deployments | `GET /v1/model-catalog`; catalog schema and read scope undefined | Offer only policy-eligible deployments if a selector is approved | Do not replace an unavailable allowed deployment with an unapproved fallback | **Confirmed API/selection rule; selector is Proposal.** [DDS], pp. 37–39. |

**Needs confirmation — OQ-SCR-020:** Define policy-read/write endpoints, complete field schema, local and server validation, version-precondition transport, policy activation behavior, model/tool/reviewer selectable sources, field-level permissions, configuration precedence, and which settings are actually editable. §6.1.1 associates workspace settings with `PATCH /v1/cases/{caseId}`; this is not sufficient evidence for a workspace-policy update endpoint.

<a id="scr-008"></a>
### SCR-008 — Audit Explorer

#### Fields

The source confirms immutable audit data and the auditor’s metadata scope. Detailed column placement is proposed.

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and validation timing | Display/value source | Status and source |
|---|---|---|---|---|---|---|
| SCR-008-F01 | Audit event ID | UUIDv7 identifier baseline; public schema undefined | D | Immutable event identity | `audit_events` | **Confirmed data; Proposal column.** [DDS], pp. 51, 85. |
| SCR-008-F02 | Tenant scope | Mandatory security attribute; domain UUID | D if visible; not editable query authority | Tenant identity participates in every access predicate | Authorized audit context | **Confirmed data/control; display unresolved.** [DDS], pp. 22, 51. |
| SCR-008-F03 | Actor ID | Actor/principal identifier; public schema undefined | D | Preserve authenticated actor and denied principal metadata without resource disclosure | Audit record | **Confirmed data.** [DDS], pp. 23, 85. |
| SCR-008-F04 | Action/event type | Type/vocabulary undefined; existing event names must be preserved | D | No inferred complete list of filter values | Audit record/event metadata | **Confirmed data; selector/column unresolved.** [DDS], pp. 62, 85, 87. |
| SCR-008-F05 | Digest/hash-chain evidence | `digest` and batch hashes exist; per-field encoding/schema undefined | D | Append-only ledger; independently retained hash-chain export | Audit ledger/manifests | **Confirmed data/integrity rule.** [DDS], p. 62, §17.3.1; p. 85, §B.1. |
| SCR-008-F06 | Occurrence time | Timestamp; UTC/RFC 3339 durable representation | D | Workspace-local display; event order unaffected by locale | Audit/event record | **Confirmed boundary data; Proposal column.** [DDS], pp. 48, 54, 59. |
| SCR-008-F07 | Correlation/trace reference | Identifier strings; lengths undefined | D if visible | Correlated diagnostics contain identifiers/policy outcomes, not source text/secrets | Safe event metadata | **Confirmed diagnostic data; Proposal column.** [DDS], p. 64, §18.1.1. |
| SCR-008-F08 | Decision metadata | Decision/actor/hash/reason references; redacted schema undefined | D | Historical review decisions cannot be altered | Approval/audit evidence | **Confirmed auditor scope.** [DDS], p. 11, §2.1.2; p. 62, §17.3.1. |
| SCR-008-F09 | Prompt-template digest | Digest metadata; encoding/length undefined | D | Auditor receives digests within redacted scope, not unrestricted full prompts | Audit evidence | **Confirmed auditor scope.** [DDS], p. 11, §2.1.2. |
| SCR-008-F10 | Access/denial events | Principal/action/policy metadata; schema undefined | D | No leakage of private resource existence | Audit/event ledger | **Confirmed auditor scope.** [DDS], pp. 11, 23, 87. |
| SCR-008-F11 | Redacted evidence/resource lineage | Authorized metadata/source references; schema undefined | D if available | Auditor cannot edit case content; evidence-read path needs confirmation | Redacted audit evidence | **Confirmed activity; navigation/data path unresolved.** [DDS], p. 11, §§2.1.1–2.1.2. |

#### Actions

| ID | Button/event and execution conditions | Processing | Successful display/navigation | Failure display | Status and source |
|---|---|---|---|---|---|
| SCR-008-A01 | Query audit events as Auditor | `GET /v1/audit/events`; cursor-paginated immutable log | HTTP `200`; show authorized history | Safe denied/read/validation error | **Confirmed.** [DDS], p. 83, §A.2. |
| SCR-008-A02 | Load another cursor page | Use server pagination contract | Show returned immutable records | Safe cursor error; exact presentation unresolved | **Confirmed cursor API behavior.** [DDS], pp. 54, 83. |
| SCR-008-A03 | Inspect event/lineage | Obtain permitted metadata; detail endpoint and link behavior undefined | **Proposal:** show event details/authorized lineage | Non-disclosing failure for inaccessible references | **Confirmed inspection purpose; detail interaction is Proposal.** [DDS], p. 77, Figure 21.2; p. 11, §2.1.2. |
| SCR-008-A04 | Attempt historical modification | Reject modification of append-only audit/review history | No historical edit accepted | Denial/integrity failure, safely audited | **Confirmed prohibition.** [DDS], p. 62, §17.3.1; p. 88, `T-09`. |

**Needs confirmation — OQ-SCR-021:** Define audit response/detail schemas, time/actor/action/resource filters, ordering, page size, redaction rules, accessible lineage links, digest verification display, event-open behavior, and all non-Auditor permissions. A workspace export operation does not establish an Audit Explorer “export current results” button.

The fictional baseline has a 30-day diagnostic-log default and a distinct seven-year security-audit policy. Corporate retention selection remains an explicit open architecture decision; neither is a confirmed audit-screen date-range limit.  
**Source:** [DDS], p. 66, §18.3.2; p. 90, §F.2.

<a id="scr-009"></a>
### SCR-009 — Overview

#### Fields and Functions

| Category | Specification | Status and source |
|---|---|---|
| Screen existence | `Overview` appears as a sidebar destination. | **Illustration confirmed.** [DDS], pp. 7, 14. |
| Purpose and users | No overview-specific business purpose or permission is supplied. | **Needs confirmation — OQ-SCR-001 and OQ-SCR-003.** |
| Fields | No distinct Overview field contract is supplied. Shared summary cards occur on other titled reference views, but their presence here is not separately established. | **Needs confirmation — OQ-SCR-022.** |
| Requiredness, type, length, format, defaults, editing, validation, display conditions, selectable values | No Overview-specific definitions are supplied. | **Needs confirmation.** Do not create editable dashboard controls by inference. |
| Primary action and buttons | Undefined. | **Needs confirmation — OQ-SCR-001.** |
| Search, list, sorting, pagination | Undefined. | **Needs confirmation — OQ-SCR-011.** |
| Data/API inputs and outputs | No dedicated Overview endpoint is provided. | **Needs confirmation.** |
| Success/failure navigation | Undefined beyond illustrated sidebar presence and shared authorization/error requirements. | **Needs confirmation.** |

No dashboard, chart, aggregate refresh schedule, or default landing decision is confirmed.

<a id="scr-010"></a>
### SCR-010 — Usage & Quality

#### Usage Fields

Usage data is confirmed. Placement within this illustrated destination is a **Proposal** pending the screen hierarchy decision.

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and validation timing | Display/value source | Source |
|---|---|---|---|---|---|---|
| SCR-010-F01 | Costs/usage attribution | Numeric/currency/object schema undefined | D | Per-tenant/workspace attribution; no invented currency/rounding | Usage/CostLedger | [DDS], pp. 65–66, §18.3; p. 83, §A.2. |
| SCR-010-F02 | Quotas | Units/schema undefined | D; editable quota placement not confirmed | Must reflect authoritative workspace quota | Usage/workspace policy | [DDS], pp. 38, 69, 83. |
| SCR-010-F03 | Budget | Numeric/currency/window undefined | D | Do not infer budget window or threshold | Daily rollup/usage result | [DDS], p. 65, §18.3.1. |
| SCR-010-F04 | Forecast | Estimate schema/units/horizon undefined | D | Present as forecast, not approved spend | Daily rollup/usage result | [DDS], p. 65, §18.3.1. |
| SCR-010-F05 | Rejected excess requests | Count/reason schema undefined | D | Reflect rejected admission/quota outcomes | Daily rollup/usage result | [DDS], p. 65, §18.3.1. |
| SCR-010-F06 | Trend estimates | Series/window/precision undefined | D | Do not invent charts or sampling intervals | Usage API | [DDS], p. 83, §A.2. |
| SCR-010-F07 | Workspace cost center | Reference/type/vocabulary undefined | D; editor not confirmed | Usage carries workspace cost-center attribution | Usage ledger | [DDS], p. 65, §18.3.1. |
| SCR-010-F08 | Model deployment version | Reference/version schema undefined | D | Attribute actual deployment version | Model/usage ledger | [DDS], p. 65, §18.3.1. |
| SCR-010-F09 | Input/output token usage | `in_tokens`, `out_tokens` exist; exact data types/display units undefined | D | Provider usage accounted under workspace quotas | `token_ledger` / usage result | [DDS], pp. 38, 85. |
| SCR-010-F10 | Embedding, storage, indexing usage | Measures/schema/units undefined | D | Track these separately; no invented conversion factors | Attributed usage ledger | [DDS], p. 65, §18.3.1; p. 68, §19.1.2. |

#### Actions

| ID | Button/event and execution conditions | Processing | Successful display/navigation | Failure display | Status and source |
|---|---|---|---|---|---|
| SCR-010-A01 | Read usage as Admin | `GET /v1/usage` | HTTP `200`; costs, quotas, trend estimates | Safe denied/read failure | **Confirmed API; binding to screen is Proposal.** [DDS], p. 83, §A.2. |
| SCR-010-A02 | Open quality scorecard | Screen organization unresolved | **Proposal:** open SCR-011 within this destination | Shared safe failure handling | **Proposal only.** [DDS], p. 81, Figure 22.2. |

**Needs confirmation — OQ-SCR-023:** Define usage response schema, units/currency/precision, reporting windows, selectable cost centers/deployments, filter/sort/pagination, forecast semantics, update behavior, and whether data is tabular or graphical. “Daily rollups” confirms data aggregation cadence, not a specific batch-job execution schedule.

<a id="scr-011"></a>
### SCR-011 — AI Quality / Evaluation Scorecard

#### Fields

Evaluation data and targets are confirmed. Detailed scorecard field placement is a **Proposal** because the illustrated page does not provide a real scorecard schema.

| ID | Field and meaning | Type, length, and format | Required / initial / editability | Constraints and validation timing | Display/value source | Source |
|---|---|---|---|---|---|---|
| SCR-011-F01 | Evaluation ID | Identifier; UUIDv7 baseline; API schema undefined | D; server-managed | Authorized evaluation scope | Evaluation response | [DDS], pp. 74–76. |
| SCR-011-F02 | Evaluation status | Full enumeration/type undefined | D | Accepted asynchronous request is not completed evaluation | Evaluation read API | [DDS], pp. 74–76; p. 83. |
| SCR-011-F03 | Dataset version/manifest | Versioned dataset and signed-manifest metadata; schema undefined | D; dataset selector not confirmed | Frozen, versioned, independently reviewed synthetic fixtures | Evaluation dataset/manifest | [DDS], pp. 75, 88–89. |
| SCR-011-F04 | Corpus case count | Numeric count; type undefined | D | Reference corpus has 1,200 synthetic permission-controlled cases; not a user input limit | Reference evaluation dataset | [DDS], p. 75, §21.2.1. |
| SCR-011-F05 | Grounded citation precision | Numeric score; precision/aggregation schema undefined | D | Target `>=0.97` | Scorecard/frozen suite | [DDS], p. 75, §21.2.2. |
| SCR-011-F06 | Unsupported-claim rate | Numeric score; precision/aggregation schema undefined | D | Target `<=0.02` | Scorecard/frozen suite | [DDS], p. 75, §21.2.2. |
| SCR-011-F07 | High-risk policy recall | Numeric score; representation undefined | D | `1.00` on frozen safety suite | Scorecard/frozen suite | [DDS], p. 75, §21.2.2. |
| SCR-011-F08 | Confidence intervals | Statistical output schema undefined | D | Low statistical confidence blocks release; cannot be presented as equivalence | Evaluation result by domain | [DDS], pp. 75–76, §§21.2.2 and 21.3.2. |
| SCR-011-F09 | Distribution shift/domain report | Domain/shift schema undefined | D | Report by domain; no invented domain taxonomy | Evaluation result | [DDS], p. 75, §21.2.2. |
| SCR-011-F10 | Release-gate result | `ReleaseGateResult` exists; status schema undefined | D | Critical isolation/approval tests have zero-exception acceptance; benchmark quality does not override safety failures | Release/evaluation evidence | [DDS], pp. 74–76; p. 88, §D.1. |
| SCR-011-F11 | Expected citation sets/decision outcomes | Per-example fixture data; response schema undefined | D if detail display approved | Do not permit screen edits of frozen expected fixtures | Evaluation dataset | [DDS], p. 75, §21.2.1; p. 88, `T-12`. |

#### Actions

| ID | Button/event and execution conditions | Processing | Successful display/navigation | Failure display | Status and source |
|---|---|---|---|---|---|
| SCR-011-A01 | Start benchmark evaluation as Admin | `POST /v1/evaluations` with long-running-job idempotency and validated input | HTTP `202`, persisted evaluation; display pending outcome | Safe schema/authorization/dependency error; no false scorecard completion | **Confirmed API; UI control/placement is Proposal.** [DDS], pp. 74–76; p. 83. |
| SCR-011-A02 | Inspect evaluation result | `GET /v1/evaluations/{evaluationId}` | Display authoritative result and supplied domain/statistical evidence | Safe read failure; result-read role undefined | **Confirmed API; screen binding is Proposal.** [DDS], pp. 74–76. |
| SCR-011-A03 | Show changed prompt/model evaluation outcome | Re-evaluation required for independent prompt/model rollout | Report new accepted evaluation evidence; low confidence remains blocking | Do not show equivalence or approval without sufficient evidence | **Confirmed lifecycle rule; UI event mapping unresolved.** [DDS], p. 76, §21.3.2. |

**Needs confirmation — OQ-SCR-024:** Resolve standalone versus SCR-010 subview, launch/primary action, result-read permissions, evaluation input schema, selectable dataset/model/prompt versions, evaluation status vocabulary, progress transport, score aggregation/precision, domain taxonomy, confidence calculations, and details pagination. No release-promotion button is confirmed on this screen.

### Unlocated Screen-Affecting Operations

These operations are included because the source supports them, not because a corresponding screen is confirmed. No new screen ID is assigned.

| Operation ID | Activity | Confirmed inputs/data and field constraints | Processing and outcomes | Screen/control gaps | Source |
|---|---|---|---|---|---|
| SCR-X-001 | Authentication/session | OIDC code flow with PKCE; access-token claims issuer, audience, expiry, subject, tenant; no long-lived refresh token in local storage | Gateway rejects invalid/missing claims/algorithms; `GET /v1/me` exists | No local username/password/MFA form, sign-in route, sign-out control, session-error display, or return destination defined | [DDS], pp. 21–23. OQ-SCR-002. |
| SCR-X-002 | Membership and provisioning | `PUT /v1/workspaces/{workspaceId}/members`; provisioning establishes policy, encryption references, role bindings, quotas, connector stubs | Idempotent provisioning; incomplete state visible and blocks sync | Member/role field schemas, requiredness/defaults/editability, provisioning API, form placement, success/failure screens undefined | [DDS], pp. 21–23; p. 78, §22.1.1. OQ-SCR-026. |
| SCR-X-003 | Workspace export | Authorized workspace reference; `Admin + approver`; two independent approval checks. Manifest contains case metadata, approved artifacts, source references, audit manifests, checksums. Secrets and internal model prompts excluded. | `POST /v1/workspaces/{workspaceId}/export`, HTTP `202`; controlled asynchronous export | No approval form, export scope selector, download/status API, manifest display, or completion navigation specified; do not invent confirmation checkboxes | [DDS], pp. 78–80; p. 83; p. 88, `T-11`. OQ-SCR-025. |
| SCR-X-004 | Workspace deletion | Authorized workspace reference; `Admin + approver`; independent approvals; legal holds enforced | `POST /v1/workspaces/{workspaceId}/delete`, HTTP `202`; tombstones, blob/index removal, receipts; protected records retained/receipted | Deletion form, approver routing, status API, receipt display, partial/legal-hold completion language, and final navigation undefined | [DDS], pp. 78–80; p. 83; p. 89, `TST-013`. OQ-SCR-025. |
| SCR-X-005 | Legal/security hold | `POST /v1/security/holds`; hold protects eligible records from purge | Durable authorized hold behavior and purge exceptions | Exact fields, types, requiredness, value sources, permissions, validation, screen placement, and read/release-hold API undefined | [DDS], pp. 61–63; pp. 26, 80. OQ-SCR-026. |
| SCR-X-006 | Dead-letter replay/remediation | Required operator reason, dry-run validation, scope limit. Reason type/length and scope-limit units/value undefined. | `POST /internal/deadletters/{id}/replay`; preserve original event identity unless explicitly migrated with provenance; bounded replay | No browser console, operator role, dry-run request schema, job/status UI, or navigation confirmed. An internal endpoint is not automatically browser-accessible. | [DDS], pp. 48–50; p. 90, §F.1. OQ-SCR-027. |
| SCR-X-007 | Optional webhook administration | Optional signed outbound webhooks; recipient signature/event-age verification | Retry with exponential backoff; webhook failure does not roll back case transition | No webhook configuration screen, public CRUD API, fields, signature display, or delivery-history UI defined | [DDS], p. 55, §15.2.2. OQ-SCR-027. |
| SCR-X-008 | Design baseline/change records | `POST /v1/design-decisions`, `GET /v1/design-baselines/{id}`; versioned change/decision metadata | Revised invariants linked to negative tests; authorized/idempotent durable behavior | No end-user design-decision screen or form is defined. Do not assign these functions to Policy Settings by name similarity. | [DDS], pp. 8–10, Chapter 1. OQ-SCR-027. |
| SCR-X-009 | Health, operational diagnostics, release control | Health, metrics, capacity, workflow, and release APIs are described | Operational recovery/release controls preserve safety and evidence | No operator screen contract is supplied; do not create browser access to `/internal/...` endpoints by inference | [DDS], pp. 18–20, 48–50, 64–73. OQ-SCR-027. |

For each unlocated operation, screen-specific input type, length, format, requiredness, initial value, editability, validation timing, display conditions, selectable values, button enablement, navigation, list/search/sort/pagination, and failure layout remain **Needs confirmation** unless explicitly stated in the table.

## Integrations and Acceptance Criteria

### Screen Integration Register

This register identifies existing contracts only. It does not define new endpoints, full API schemas, or backend implementation specifications.

| Integration | Existing methods/paths | Confirmed input or request control | Confirmed output/behavior | Screen dependency and unresolved details | Source |
|---|---|---|---|---|---|
| Identity provider/edge | OIDC authorization-code flow with PKCE; `GET /v1/me` | Valid issuer, audience, expiry, subject, tenant; expected algorithms | Authenticated principal/tenant scope; exact `me` response undefined | All screens; IdP and BFF/session decision unresolved | [DDS], pp. 21–23; p. 90, §F.2. |
| Case Service | `POST /v1/cases`; `GET /v1/cases?cursor=...`; `GET /v1/cases/{caseId}`; `PATCH /v1/cases/{caseId}`; `POST /v1/cases/{caseId}/close` | Authorized scope, validated case data, idempotency for creation, `If-Match` revision for mutation | Create `201`; read/update `200`; update conflict `409`; closure snapshot behavior | SCR-001/SCR-002; complete payloads/list schema/close result undefined | [DDS], pp. 11–13, 24–26, 57–59, 83–84. |
| Ingestion/source storage | `POST /v1/cases/{caseId}/attachments`; `GET /v1/documents/{documentId}/status` | Supported files, agreed MIME/extension, configurable 25 MB cap, scan, opt-in OCR | `202` operation; immutable derivatives/anchors; readiness/quarantine states | SCR-002/SCR-003; multipart/signed-upload design and source-view endpoint undefined | [DDS], pp. 30–32, 82–83. |
| Retrieval/evidence | `POST /v1/search`; `GET /v1/evidence/{evidenceId}`; `GET /v1/cases/{caseId}/evidence` | Permitted query scope; ACL before release; bounded evidence budgets | ACL-filtered lexical/semantic evidence; anchor metadata; `NO_SUPPORTED_EVIDENCE` | SCR-002/SCR-003/SCR-005; public schemas/filter/pagination contracts undefined | [DDS], pp. 34–36, 57–59, 83. |
| Orchestrator/run API | `POST /v1/cases/{caseId}/runs`; alternate `POST /v1/runs`; `GET /v1/runs/{runId}`; `GET /v1/runs/{runId}/steps` | Analyst run request, idempotency, admission thresholds, bounded plan | Case-scoped creation `202`; read `200`, stages/evidence metadata | SCR-002/SCR-004; alternate create API and timeout/review semantics unresolved | [DDS], pp. 15–17, 40–42, 83, 90. |
| Run streaming | `GET /v1/streams/runs/{runId}` | Authorized run; `Last-Event-ID` on reconnect | HTTP `200` SSE; monotonic offsets, retained scoped backfill | SCR-002/SCR-004; event payload and retention-gap handling undefined | [DDS], pp. 54–56, 58, 83. |
| Policy/review | `GET /v1/review-queue`; `POST /v1/approvals/{approvalId}/decision` | Reviewer authorization, required fields, task/hash binding | Decision `200`/`409`; immutable decision; publication validation | SCR-005 and detail gate; task-detail/read and decision schemas unresolved | [DDS], pp. 44–46, 58, 83. |
| Enterprise connectors/secret store | `POST /v1/connectors/{connectorId}/sync`; `GET /v1/connectors/{connectorId}/runs` | Admin sync, workspace credentials reference, provider cursor/capabilities | `202`; durable incremental outcomes; lower-trust warning; reauthentication failure | SCR-006; exact providers/permissions/configuration/auth APIs unresolved | [DDS], pp. 27–29, 83; p. 90, §F.2. |
| Model catalog/gateway | `GET /v1/model-catalog`; internal `POST /internal/model/generate` | Deployment-specific allowlist, normalized scoped prompts, versioned output schema | Validated model output/usage; `MODEL_OUTPUT_INVALID` on invalid fields/citations/control characters | SCR-002/SCR-005 metadata and proposed SCR-007 selection. Browser does not call the internal gateway by inference. | [DDS], pp. 37–39. |
| Audit | `GET /v1/audit/events` | Auditor and tenant/redaction scope; cursor | HTTP `200`, immutable cursor-paginated history | SCR-008; exact filters/details/redaction schema undefined | [DDS], pp. 61–63, 83. |
| Usage | `GET /v1/usage` | Admin scope | HTTP `200`; costs, quotas, trends; daily attributed rollups | Proposed SCR-010 placement; response/display units undefined | [DDS], pp. 65–66, 83. |
| Evaluation | `POST /v1/evaluations`; `GET /v1/evaluations/{evaluationId}` | Admin starts frozen benchmark; validated versioned inputs | Create `202`; evaluation/scorecard evidence | Proposed SCR-011 placement; result-read scope/input/result schemas undefined | [DDS], pp. 74–76, 83. |
| Export/deletion | `POST /v1/workspaces/{workspaceId}/export`; `POST /v1/workspaces/{workspaceId}/delete` | `Admin + approver`; independent approvals; legal holds | HTTP `202`; controlled manifest/verified receipts | Unlocated UI; status/download/approval contracts undefined | [DDS], pp. 78–80, 83. |
| Safe source access | Short-lived access-controlled signed URLs required; no public viewer endpoint defined | Authorized tenant/workspace/document/version access | Stored encrypted source/derivative access; opaque public object names | SCR-003; generation, expiry, and browser retrieval contract undefined | [DDS], p. 52, §14.3.1. |
| Degraded-state information | `GET /v1/system/degraded-modes` | Authorization/response schema undefined | Declared degraded-state API exists | Shared status displays; do not substitute internal metrics/capacity as a browser API | [DDS], pp. 68–70. |

**SCR-COM-012 — External-boundary safety.**

- The browser never submits arbitrary tool definitions to the orchestrator.
- Retrieved source text and model output cannot change tenant scope, approvals, policy authority, or tool authorization.
- Model/provider requests receive only scoped context; connector credentials must not enter model prompts or public responses.
- Internal MCP/A2A discovery does not grant action permission.
- Consequential mutable tool actions require separate authorization; a denied action cannot be replaced with a semantically equivalent tool.
- Optional webhook failure cannot undo an accepted case transition.

**Source:** [DDS], p. 7; pp. 15, 37–42, 55, 61–63, 87.

**Needs confirmation — OQ-SCR-030:** Select the supported cloud region, search provider, identity provider, approved model deployments, corporate retention policy, and third-party connector permissions through dated architecture decisions. Per-tenant encryption-key isolation versus rotation throughput also remains unresolved. No provider, region, owner, decision date, or approval is selected by this specification.  
**Source:** [DDS], p. 10, §1.3.2; p. 90, §F.2.

### Major-Operation Acceptance Criteria

The criteria below verify confirmed behavior. Where control placement or request schemas are unresolved, execute through the authorized operation and attach the final screen binding after the associated open question is resolved.

| Acceptance ID | Prerequisites | Action/procedure | Expected result | Requirement/test trace and source |
|---|---|---|---|---|
| AC-SCR-001 | Valid Analyst session, authorized workspace, valid create payload/key | Submit case creation | `201` with a case identifier; case begins `NEW`; asynchronous classification may attach labels/confidences/provenance | SCR-002-A02; [DDS], p. 12, §2.2.1; p. 83. |
| AC-SCR-002 | Same actor, identical create payload and idempotency key within the contract period | Submit create twice | One case and identical original response; no duplicated business creation | `TST-001`; SCR-COM-010; [DDS], pp. 25, 89. |
| AC-SCR-003 | An already used create key | Reuse key with changed body | HTTP `409` `IDEMPOTENCY_CONFLICT`; no second outcome under that key | `TST-002`; [DDS], pp. 54, 89. |
| AC-SCR-004 | Valid session from another tenant; a known foreign-tenant case ID | Open that case | Same non-disclosing not-found class as absent case; no case content/existence leakage | `TST-003`, `T-01`; SCR-COM-003; [DDS], pp. 23, 88–89. |
| AC-SCR-005 | Authorized current case with changed server revision | Save using stale `If-Match` | `409` `CASE_VERSION_CONFLICT` with current revision; no stale mutation; UI does not show successful save | SCR-002-A03; [DDS], pp. 25, 84. |
| AC-SCR-006 | Authorized classification-correction workflow | Correct a label with a reason code | Accepted correction retains appropriate provenance; correction without required reason is not accepted | SCR-002-F14–F17/A04; [DDS], p. 12, §2.2.1. Exact code/schema pending OQ-SCR-007. |
| AC-SCR-007 | Authorized case; permitted file with matching MIME/extension under configured cap | Upload attachment | `202` ingestion operation; scan precedes parsing; macros are not executed; embedded remote references are not fetched; readiness follows server pipeline state | SCR-002-A05; [DDS], pp. 30–32, 83. |
| AC-SCR-008 | Unsafe PDF or malicious/polyglot/decompression payload | Upload/ingest | Fail closed; unsafe content quarantined and never indexed; UI does not show searchable readiness | `TST-015`, `T-04`; [DDS], pp. 30, 88–89. Exact boundary/error mapping pending OQ-SCR-009. |
| AC-SCR-009 | Authorized low-quality source with quality flags | View source and attempt autonomous recommendation use | Source remains viewable under permission; low-quality material excluded from autonomous recommendations | SCR-002-F21/SCR-003-F12; [DDS], p. 32, §8.3.2. |
| AC-SCR-010 | Search corpus with permitted and forbidden sources | Search evidence | Only permitted lexical/semantic evidence returned; forbidden text never released to generation | SCR-003-A02; [DDS], pp. 22, 34–36, 83. |
| AC-SCR-011 | Previously indexed source; access subsequently revoked | Issue next evidence query | No revoked source evidence returned; affected caches invalidated before serving new results | `TST-004`, `T-08`; [DDS], pp. 27–29, 88–89. |
| AC-SCR-012 | Authorized citation with resolvable stored anchor | Activate citation before review decision | Open cited stored document version and highlight anchored page range; reviewer can inspect actual evidence | SCR-COM-006; [DDS], pp. 31, 35, 57–59. |
| AC-SCR-013 | Insufficient evidence quality/confidence | Search/request grounded answer | `NO_SUPPORTED_EVIDENCE`, clarification, or human route as authorized; no fabricated context or approved answer | SCR-003-A02; `TST-009`; [DDS], p. 36, §9.3.2; p. 89. |
| AC-SCR-014 | Authorized Analyst, sufficient run admission, valid payload/key | Request grounded draft | `202`; run immediately allocated; UI shows durable retrieval/generation/policy stages via scoped streaming | SCR-002-A07; SCR-004-A01–A02; [DDS], pp. 58, 83. |
| AC-SCR-015 | Running authorized workflow | Refresh browser, then reconnect SSE with retained `Last-Event-ID` | Progress reconstructs from server; retained events backfill within scope; no workflow restarted merely by refresh | SCR-004 procedure; [DDS], pp. 55, 58. |
| AC-SCR-016 | Quota/provider/queue admission thresholds not satisfied | Request new AI run | HTTP `429` plus `Retry-After`; UI does not imply run started; saved cases remain available | SCR-COM-009; [DDS], p. 69, §19.2.1. |
| AC-SCR-017 | Model response contains unknown fields, invalid citations, or injected control characters | Process response through gateway | `MODEL_OUTPUT_INVALID`; no publication; visible run failure reflects authoritative checkpoint | `TST-005`; SCR-004-F08; [DDS], pp. 38, 41, 89. |
| AC-SCR-018 | Planner reaches call/depth/runtime boundary or attempts arbitrary/denied capability | Attempt further invocation | Enforced bounded/denied outcome before unauthorized dispatch; no equivalent-tool substitution; checkpoint failure visible | `TST-014`, `T-10`; [DDS], pp. 40–42, 87–89. Timeout/review interpretation pending OQ-SCR-012. |
| AC-SCR-019 | Authorized non-expired review task, incomplete required review fields | Open decision interface | Exact candidate/citations/model/prompt/policy reasons displayed; both Approve and Reject disabled until required fields complete | SCR-005 procedure; [DDS], p. 58, §16.2.2. Field set pending OQ-SCR-014. |
| AC-SCR-020 | Authorized reviewer; exact unchanged artifact; completed required fields; separation of duties satisfied | Submit approval | `200`, immutable decision record with actor/time/hash/rationale; publication only after satisfied gate | SCR-005-A04; [DDS], pp. 45–46, 83. |
| AC-SCR-021 | Reviewer uses prior or wrong artifact hash | Submit approval | Stale decision rejected/audited; `409` contract; changed artifact not published under old approval | `TST-006`, `T-03`; [DDS], pp. 45–46, 83, 88–89. |
| AC-SCR-022 | Analyst is the author of a high-risk recommendation | Attempt self-approval | Approval denied; no high-risk publication without authorized independent review | SCR-COM-002; [DDS], pp. 11, 13, 85, 90. |
| AC-SCR-023 | Configured review task SLA expires | Process expiry | No implicit approval; reassignment/escalation recorded and authoritative state shown | `TST-010`; [DDS], pp. 45, 89. |
| AC-SCR-024 | Recommendation rejected or denied | Rework | New run revision follows controls; historical denial is not retroactively changed to approval | SCR-002-A11; SCR-005-A05; [DDS], pp. 46, 75. |
| AC-SCR-025 | Previously accepted approval/publication event | Replay event, including attempted changed artifact | Exactly one accepted business transition; different artifact cannot publish under old approval | `TST-007`, `T-07`; [DDS], pp. 45–46, 88–89. |
| AC-SCR-026 | Source/case permissions change between retrieval and publication | Complete publication gate | Re-evaluate authorization and reject stale evidence; UI does not show published success | SCR-002-A12; [DDS], p. 13, §2.5; p. 46, §12.5. |
| AC-SCR-027 | Closure is permitted under resolved role/state guards | Close case | Preserve snapshot of approved answer, cited versions, reviewer decisions, and immutable closed lineage | SCR-002-A09; [DDS], pp. 24–26. Guards pending OQ-SCR-018. |
| AC-SCR-028 | Admin; fully provisioned connector/workspace | Start connector sync | `202` operation; unsupported capabilities cause explicit lower-trust warning; durable cursor advances only after preceding outcomes | SCR-006-A02; [DDS], pp. 27–29, 78, 83. |
| AC-SCR-029 | Connector credentials revoked while jobs queued | Execute queued sync | `CONNECTOR_REAUTH_REQUIRED`; no credential leakage; safe remediation condition shown | SCR-006-F05/A03; [DDS], p. 27, §7.1.2. |
| AC-SCR-030 | Authorized configuration update with current revision | Save policy/settings | Revision-safe accepted configuration and durable audit; stale/unauthorized write does not mutate policy | SCR-007-A02; [DDS], p. 24, §6.1.1. Endpoint pending OQ-SCR-020. |
| AC-SCR-031 | Auditor, permitted redacted audit scope | Query and inspect audit; attempt historical edit | Cursor-paginated immutable metadata; no case-content edit; historical audit/review edit rejected | SCR-008; `T-09`; [DDS], pp. 11, 62, 83, 88. |
| AC-SCR-032 | Generation provider unavailable | Open/edit case and search evidence | Manual case/evidence workflows remain available; degraded status visible; approval/ACL controls remain enforced | SCR-COM-009; [DDS], pp. 69, 79. |
| AC-SCR-033 | Vector index degraded but permitted lexical retrieval remains available | Search | Visible reduced-quality flag with lexical evidence; no ACL/policy bypass | SCR-003-A05; [DDS], p. 69, §19.2.2. |
| AC-SCR-034 | Keyboard-only user with authorized case access | Navigate and open case using keyboard | No blocked action, visible focus, meaningful semantic/keyboard ordering | `TST-011`; SCR-COM-007; [DDS], pp. 58, 89. |
| AC-SCR-035 | Workspace timezone/locale configured | Display timestamp and change locale presentation | Workspace-local time includes timezone label; durable UTC/RFC 3339 value and event order unchanged | SCR-COM-008; [DDS], pp. 54, 59. |
| AC-SCR-036 | Admin with authorized usage scope | Read usage | `200`; costs, quotas, and trend estimates reflect attributed usage, not invented chart data | SCR-010-A01; [DDS], pp. 65, 83. Screen binding pending OQ-SCR-023. |
| AC-SCR-037 | Admin and frozen versioned benchmark | Start/read evaluation | `202` start; authoritative scorecard reported; citation precision, unsupported-claim rate, high-risk recall, confidence/domain evidence preserve source acceptance targets | SCR-011; [DDS], pp. 75–76, 83. UI schemas pending OQ-SCR-024. |
| AC-SCR-038 | Single Admin without independent export approval | Request export | Controlled export cannot proceed as a single-admin bypass | `T-11`; SCR-X-003; [DDS], pp. 78, 83, 88. |
| AC-SCR-039 | Authorized independent export approvals | Export workspace | Package includes case metadata, approved artifacts, source references, audit manifests, checksums; excludes secrets/internal model prompts | SCR-X-003; [DDS], p. 79, §22.3.1. |
| AC-SCR-040 | Authorized deletion workflow with legal hold | Request/process deletion | Protected records retained and receipted; eligible records removed with tombstones/receipts; no false complete purge | `TST-013`; SCR-X-004; [DDS], pp. 80, 89. |

### Performance and Verification Boundaries

| Requirement | Confirmed target/boundary | Screen-test interpretation | Source |
|---|---|---|---|
| Case creation latency | Case identifier within 300 ms at P95 / under 300 ms in SLO wording, under defined load | API outcome target, not a complete browser-rendering target. Resolve wording/boundary before strict threshold testing. | [DDS], p. 12, §2.3.1; p. 65, §18.2.1. |
| Search latency | P95 under 1.5 s excluding remote connector fetch | Measure retrieval separately from browser rendering and model generation | [DDS], p. 65, §18.2.1. |
| Reference load | 2,000 daily active users; 60 requests/s steady; 180 requests/s burst; maximum 100,000 indexed documents per tenant; 20 concurrent AI runs per large tenant | Use as source workload assumptions, not new screen row-count/input limits | [DDS], p. 68, §19.1.1. |
| Critical safety verification | Isolation and approval tests pass with zero exceptions | A high model score cannot compensate for approval or tenant-isolation failure | [DDS], pp. 74, 88, Chapter 21 invariant and §D.1. |
| Fixture coverage | Synthetic successful, empty, mixed-permission, adversarial, malformed inputs; randomized tests retain seeds | Apply to screen/API integration and failure presentation tests | [DDS], p. 89, §E.1. |

No separate browser load-time, list-page-size, debounce delay, automatic refresh period, connector schedule, or screen-level retry count is specified.

## Consistency and Open Questions

### Source Conflicts and Required Amendments

No earlier specification exists to amend. The following conflicts and ambiguities are recorded against this stage and must be resolved in later contracts or by an explicit amendment to `01_screen_functions.md`; they are not silently decided here.

| Conflict ID | Source evidence | Affected identifiers | Required resolution/amendment |
|---|---|---|---|
| CON-SCR-001 | §16.1.1 lists eight primary screens. Illustrations add `Overview`, `Usage & Quality`, and alternative titles. | SCR-001–SCR-011; OQ-SCR-001 | Confirm screen hierarchy and aliases; identify which illustration-only surfaces become actual screens/subviews. |
| CON-SCR-002 | Reference titles and active-sidebar highlights disagree: Case Detail highlights Case Queue; Case Queue highlights Overview; Evidence Explorer highlights Case Detail; Agent Run highlights Evidence Viewer; Approval Inbox highlights Agent Runs; Connector Health highlights Review Inbox; Audit Explorer highlights Connectors; AI Quality highlights Audit Events. | Screen inventory; P-SCR-001; OQ-SCR-001 | Do not copy the mismatched active navigation state. Confirm intended route-to-navigation mapping. Sources: [DDS], pp. 7, 14, 33, 43, 47, 60, 67, 77, 81. |
| CON-SCR-003 | Illustrations mix `Needs review`, `Published`, `Evidence gap`, and case-like states in one list. §16.1.2 defines artifact labels, while §A.1 defines separate aggregate states. | SCR-COM-005; SCR-001-F03; SCR-002-F08/F26; OQ-SCR-006 | Define explicit status-summary mapping and its source aggregate; no expanded `cases.status` enum by inference. |
| CON-SCR-004 | Chapter 3 registers `POST /v1/runs`; Chapters 2/11 and §A.2 use `POST /v1/cases/{caseId}/runs`. | SCR-002-A07; SCR-004; integration register; OQ-SCR-012 | Identify canonical browser run-create endpoint and supported alternate semantics. Source: [DDS], pp. 13, 17, 42, 83. |
| CON-SCR-005 | §11.3.1 says missing approval terminates a run; §13.2.1 and §A.1 include `AWAITING_REVIEW`. Appendix F shows a 180-second run timeout but review tasks have a separate configured SLA. | SCR-004-F03/F07/F08/A04; SCR-005-F06; OQ-SCR-012/OQ-SCR-015 | Define valid waiting versus missing-approval failure, runtime timeout accounting, and review expiry separately. Source: [DDS], pp. 41, 45, 49, 82, 90. |
| CON-SCR-006 | §6.2.1 omits an explicit `RESOLVED -> CLOSED` transition despite a close API. Reopening is allowed as a new revision but no route/guard/API is given. | SCR-002-A09/A10; OQ-SCR-018 | Complete closure/reopen transition guards and interaction contracts without rewriting historic closed lineage. Source: [DDS], pp. 24–26. |
| CON-SCR-007 | `Workspace Admin`, `Admin`, `Owner`, `Member`, `approver`, `operator`, and `elevated role` are not consistently defined as roles or relationships. | User table; SCR-002/003/005/006/007/008; SCR-X operations; OQ-SCR-003 | Provide an explicit role/attribute/action matrix and field-level rules. Source: [DDS], pp. 11, 22, 27, 46, 50, 83. |
| CON-SCR-008 | Auditor evidence journey is described, but case-read scope in §A.2 is Analyst/Reviewer. | SCR-003/SCR-008; OQ-SCR-003/OQ-SCR-021 | Define authorized auditor evidence access/redaction API rather than granting general case reads. Source: [DDS], pp. 11, 83. |
| CON-SCR-009 | High-risk self-approval is expressly prohibited in Chapter 2; §B.1 and Appendix F describe no self-approval more generally. | SCR-005; SCR-007-F14; OQ-SCR-003 | Confirm global scope and exceptions, if any, without weakening the confirmed high-risk prohibition. Source: [DDS], pp. 11, 85, 90. |
| CON-SCR-010 | §6.1.1 describes workspace settings but associates them with `PATCH /v1/cases/{caseId}`. | SCR-007-A01/A02; OQ-SCR-020 | Supply actual workspace-policy read/update contracts. Do not use a case mutation endpoint for workspace settings solely from this association. Source: [DDS], p. 24. |
| CON-SCR-011 | `UserReviewOpened` is named in Chapter 16 but absent from Appendix C’s event catalog. Repeated chapter-boundary text associates GETs with durable validation/event requirements without a precise trigger contract. | SCR-005-A02; SCR-COM-010; OQ-SCR-021 | Define actual review-open write/event trigger and schema; do not infer that every case/evidence GET performs a review-state mutation. Source: [DDS], pp. 57–59, 87. |
| CON-SCR-012 | §15.1.1 describes snake-case error codes, while canonical/test examples use uppercase codes. | SCR-COM-011; OQ-SCR-029 | Preserve exact existing literals and specify canonical casing/HTTP mapping. Source: [DDS], pp. 54, 84, 89. |
| CON-SCR-013 | Lower-trust ingestion for unsupported connector capabilities coexists with mandatory source ACL enforcement and revocation before next retrieval. | SCR-006-F02/F03/A04; OQ-SCR-019 | Define safe capability restrictions; missing ACL capability cannot silently disable the invariant. Source: [DDS], pp. 21, 27–29. |
| CON-SCR-014 | Repeated mock summary/table/gate content appears under unrelated view titles. | SCR-COM-F01–F07; SCR-009–SCR-011; OQ-SCR-022 | Confirm actual data placement and aggregate definitions; do not treat mock repetition as complete screen design. Source: [DDS], pp. 7, 14, 33, 43, 47, 60, 67, 77, 81. |
| CON-SCR-015 | Retention defaults and Appendix F examples exist, but §F.2 explicitly leaves corporate retention, providers, deployments, region, and connector permissions open. | SCR-007/SCR-010/SCR-011; OQ-SCR-020/OQ-SCR-030 | Distinguish reference values from approved deployment decisions and define configuration precedence. Source: [DDS], pp. 66, 90. |

### Open-Decision Register

All items below are **Needs confirmation**. No decision owner, deadline, approval, or selected implementation is supplied.

| Open question ID | Affected requirements | Decision or missing contract | Source location / gap |
|---|---|---|---|
| OQ-SCR-001 | [Screen inventory](#screen-inventory); SCR-001–SCR-011 | Actual screen hierarchy/aliases, routes, launch methods, deep links, resource selection, return/browser-history behavior, and one primary action per confirmed primary screen | [DDS], p. 57, §16.1.1; illustrations listed in CON-SCR-002. Routes and event bindings absent. |
| OQ-SCR-002 | SCR-COM-002; SCR-X-001 | IdP, sign-in/out/session-expiry flow, return destination, BFF/cookie choice, and authentication failure display | [DDS], p. 21, §5.1; p. 90, §F.2. |
| OQ-SCR-003 | Users/permissions; SCR-002/003/005/006/007/008; SCR-X-002–006 | Resolve role aliases/attributes, screen-read/update permissions, self-approval scope, Auditor evidence access, owner/member predicates, operators/approvers/elevated roles | [DDS], pp. 11, 22, 27, 46, 50, 83, 85, 90. |
| OQ-SCR-004 | SCR-001 fields; [SCR-002](#scr-002); shared field profiles | Complete public field schemas, exact types/lengths/formats, requiredness/nullability, initial values, editable field set, selectable values, and client validation timing | [DDS], pp. 12, 24–25, 85–86. Full form contracts absent. |
| OQ-SCR-005 | SCR-001-A04; SCR-002-A02; P-SCR-001 | Create-case launch and form placement, create payload, and successful navigation | [DDS], pp. 11–12, 83. No creation screen/form specified. |
| OQ-SCR-006 | SCR-COM-005; SCR-001-F01/F03; SCR-002-F01/F08/F26 | Canonical UUID/business number relationship and aggregate-to-visible status mapping | [DDS], pp. 14, 51, 57, 82, 86. |
| OQ-SCR-007 | SCR-002-F14–F17/A04 | Classification schemas, label/reason-code values, correction permission/API, revision behavior, asynchronous result/failure display | [DDS], p. 12, §2.2.1. |
| OQ-SCR-008 | SCR-002-F04–F06/F23/F24; SCR-007-F09 | Impact/urgency categories, priority formula, business calendar/timezone source, SLA rules, financial-impact categories, advisory predictions | [DDS], pp. 25, 44, 59. |
| OQ-SCR-009 | SCR-002-F18–F21/A05–A06; SCR-003-F12/F13 | Exact file allowlist/MB boundary, decompression threshold, upload count, OCR configuration/default, quality thresholds, document-update mechanism, quarantine-safe viewing, removal behavior | [DDS], pp. 10, 30–32, 82, 90. |
| OQ-SCR-010 | SCR-COM-006; SCR-003-F03–F11/A03 | Source-view/download endpoint, signed-URL lifecycle, anchors/page numbering/bbox/highlight schemas, non-PDF representation, invalid anchors, return behavior | [DDS], pp. 31, 35, 52, 57. |
| OQ-SCR-011 | SCR-001 lists; SCR-003 search; SCR-005/006/008 lists | Query schemas, UI placement, query lengths/requiredness, filters/sorts/order, cursors/page sizes, result scores, total/empty/loading states, clarification/human routing | [DDS], pp. 34–36, 45, 54, 57, 83. Only selected pagination behavior is supplied. |
| OQ-SCR-012 | SCR-002-A07/A11; SCR-004 | Canonical run-create endpoint, rework revision contract, missing-approval versus waiting failure, timeout accounting/recoverability, and any cancellation/retry/resume controls | [DDS], pp. 12, 17, 40–42, 46, 49, 82–83, 90. |
| OQ-SCR-013 | SCR-004-F03–F10/A01–A03 | SSE schemas, retention/gaps/expiry, UI dedup/order handling, connection-state display, step ordering/pagination, reconstruction semantics | [DDS], pp. 40–42, 55, 58. |
| OQ-SCR-014 | SCR-005 fields/procedure/A02–A05 | Task detail endpoint, decision schema/enum, exact required review fields, rationale/annotations constraints, client/server validation and submission-state displays | [DDS], pp. 45, 58, 83, 85. |
| OQ-SCR-015 | SCR-005-F03–F06/A06; SCR-007-F06–F08 | Reviewer pools/minimum roles, expiry SLA, reassignment/escalation, late/multi-reviewer decisions | [DDS], p. 45, §12.2.1. |
| OQ-SCR-016 | SCR-002-A12; SCR-005 procedure | Whether publication has a user control/public endpoint; gate status contract and decision-to-publication display | [DDS], pp. 12, 45–46, 57–58. No Publish button contract. |
| OQ-SCR-017 | SCR-005-A07 | Override role, secondary reviewer, audited reason schema, endpoint, launch and outcome navigation | [DDS], p. 46, §12.3.2. |
| OQ-SCR-018 | SCR-002-F08/A09/A10 | Complete closure/reopen states, roles, guards, version transport, response codes and navigation | [DDS], pp. 24–26. |
| OQ-SCR-019 | SCR-006 | Provider permissions, connector configuration/auth/revoke contracts, exact capabilities/trust restrictions, sync/read scopes/states, list behavior, retry bounds and remediation controls | [DDS], pp. 27–29; p. 90, §F.2. |
| OQ-SCR-020 | SCR-007 | Policy read/update contracts, editable fields, registries/selectable sources, revision transport, validation/activation and configuration precedence | [DDS], pp. 24, 37–39, 44–46, 90. |
| OQ-SCR-021 | SCR-005-A02; SCR-008 | `UserReviewOpened` trigger/schema; audit response/details/filters/redaction/digest display; authorized lineage and non-Auditor access | [DDS], pp. 11, 57–59, 61–63, 77, 83, 87. |
| OQ-SCR-022 | Shared illustrated fields; SCR-009–SCR-011 | Summary formulas/scopes/APIs, placement, refresh/error/null behavior, Overview-specific purpose/content | [DDS], illustrated pages cited in CON-SCR-014. |
| OQ-SCR-023 | SCR-010 | Usage schema/units/currency/windows/precision, selectable filters, layout, forecast meanings, update behavior and primary action | [DDS], pp. 65–66, 83. |
| OQ-SCR-024 | SCR-011; P-SCR-001 | Scorecard hierarchy/launch, result-read permission, evaluation selection/schema/status/progress, domain/statistical calculation and detail displays | [DDS], pp. 74–76, 81, 83. |
| OQ-SCR-025 | SCR-X-003/SCR-X-004 | Export/deletion screens, independent approval mechanics/routing, scopes, status/download/receipt contracts, legal-hold/partial completion displays and final navigation | [DDS], pp. 78–80, 83, 88–89. |
| OQ-SCR-026 | SCR-X-002/SCR-X-005 | Membership/provisioning/hold screens, complete schemas, permissions and missing read/update/status/release-hold APIs | [DDS], pp. 21–23, 61–63, 78–80. |
| OQ-SCR-027 | SCR-X-006–SCR-X-009 | Whether replay, webhook, design-baseline, release, and operational administration have interactive screens; if so, their protected contracts | [DDS], pp. 8–10, 18–20, 48–50, 55, 64–73, 90. |
| OQ-SCR-028 | SCR-COM-009; SCR-COM-F06; SCR-003-F14 | Degraded-mode response/schema, health-summary mapping, visible flag/text/placement and unavailable-safe-workflow behavior | [DDS], pp. 68–70, 79. |
| OQ-SCR-029 | SCR-COM-011; all mutation/read failures | Canonical error casing and per-operation codes/statuses, safe field-detail mapping, correlation/retryable presentation and conflict recovery | [DDS], pp. 13, 25, 54, 84, 89. |
| OQ-SCR-030 | All integrations; SCR-007 | Approved region/search/IdP/model deployments, corporate retention, connector permissions, and encryption-key isolation/rotation decision | [DDS], p. 10, §1.3.2; p. 90, §F.2. |
| OQ-SCR-031 | SCR-COM-007/008; all screens; performance boundaries | Browser/viewport/mobile/localization choices, detailed focus/error behavior, number/time formats and strict interpretation of case-create P95 boundary | [DDS], pp. 12, 58–59, 65. Detailed choices absent. |

### Proposal Register

| Proposal ID | Proposal | Approval status | Affected requirements |
|---|---|---|---|
| P-SCR-001 | Consolidate illustrated aliases with the eight primary screens and, if approved, organize the scorecard as a Usage & Quality subview | **Unapproved.** Requires OQ-SCR-001/OQ-SCR-024 resolution. | SCR-001–SCR-011 |
| P-SCR-002 | Use a new-case mode associated with Case Detail, launched from Case Queue | **Unapproved.** Requires OQ-SCR-005 resolution. | SCR-001-A04; SCR-002-A02 |
| P-SCR-003 | Place source-confirmed domain/configuration data in the field catalogs on the associated screens; use proposed row/link/search/edit controls only after contracts resolve | **Unapproved wherever placement/control is not source-confirmed.** | Field rows and actions explicitly labeled Proposal |

### Dependencies on Later Specifications

| Dependency | Status and required handoff |
|---|---|
| API specification | **To be defined in a later stage.** Resolve public payloads, response properties, role scopes, error mappings, signed source access, SSE contracts, revision/idempotency transport, and missing APIs. Preserve the screen/action/open-question IDs above. |
| Data specification | **To be defined in a later stage.** Resolve field types/nullability, revision and artifact relationships, citation/anchor structures, classification/rationale schemas, and public business-number mapping. Do not treat proposed UI controls as confirmed schema fields. |
| Workflow/business-rule specification | **To be defined in a later stage.** Resolve priority/SLA rules, closure/reopen transitions, review expiry/overrides, timeout versus review waiting, publication guards, and connector lower-trust restrictions. |
| Security/nonfunctional specification | **To be defined in a later stage.** Resolve authorization predicates, redaction, session model, browser/source-rendering safety, accessibility details, provider configuration, and test/load interpretation. |
| Operations specification | **To be defined in a later stage.** Resolve protected provisioning, legal holds, export/deletion, replay/remediation, retained-event gaps, and operational status contracts. No UI or schedule is created by this dependency. |
| Stage 8 decision consolidation | **To be defined in a later stage.** `08_architecture_decision.md` must consolidate unresolved items from completed Markdown specifications with links to `01_screen_functions.md` and affected identifiers. This document records no invented decision, owner, deadline, or approval. |
