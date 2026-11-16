# 8. Architecture Decision Register

## How to Use This Document

This register consolidates outstanding decisions, missing contracts, proposals, and consistency issues in the seven supplied Markdown specifications. **It does not record approval of an architecture option or rewrite those specifications.**

- **Confirmed requirements may proceed:** Implement their stated safeguards and prepare tests without inventing missing interfaces, algorithms, thresholds, or operational settings.
- **Needs confirmation:** A decision or contract is incomplete, ambiguous, or conflicting.
- **TBD:** A required interface, representation, or operational contract has not been defined.
- **Unadopted proposal:** An existing suggestion remains unapproved. Repetition does not adopt it.
- **Resolved:** Explicit, consistent confirmed statements answer the identified question. Resolution is limited to that answer; related implementation decisions may remain open.
- In the tables, **Hold** identifies decision-dependent work. **Ready** identifies confirmed obligations that do not depend on selecting the missing option.

All quotations below are excerpts from the supplied **Markdown specifications**, including their descriptions of inconsistencies. No original PDF, Map evidence, or hierarchy context was inspected. No decision maker, approval date, deadline, technology, or additional numerical limit is assigned here.

### Citation Convention

Citation aliases identify a specific Markdown filename and section. Each use also names the applicable requirement or question identifiers. The crosswalk later in this register retains every identifier in the seven open-question registers.

| File | Open-question citation | Consistency citation |
|---|---|---|
| [01_screen_functions.md](01_screen_functions.md) | **Q1:** “Consolidated Open Questions” | **C1:** “Source Consistency and Required Clarifications” |
| [02_api.md](02_api.md) | **Q2:** “API Open-Decision Register” | **C2:** “Consistency Findings and Required Amendments” |
| [03_data.md](03_data.md) | **Q3:** “Data Open-Decision Register” | **C3:** “Field Mapping and Consistency Findings” |
| [04_batch_functions.md](04_batch_functions.md) | **Q4:** “Batch Open-Decision Register” | **C4:** “Consistency Findings and Required Amendments” |
| [05_business_rules.md](05_business_rules.md) | **Q5:** “Open-Decision Register” | **C5:** “Consistency Findings and Required Amendments” |
| [06_exception_handling.md](06_exception_handling.md) | **Q6:** “Open-Decision Register” | **C6:** “Consistency Findings and Required Amendments” |
| [07_processing_flows.md](07_processing_flows.md) | **Q7:** “Processing Open-Decision Register” | **C7:** “Consistency Findings and Required Amendments” |

Existing specification IDs remain authoritative for traceability. `AD-xxx` identifiers consolidate issues; they do not replace those IDs.

## Unresolved Items

### Identity, Authorization, and Administrative Context

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-001 | Identity provider | Needs confirmation | “Identity provider” remains an explicit choice. | Which provider and approved integration configuration apply? | Hold provider integration; Ready OIDC authorization-code/PKCE and verified tenancy requirements. | [Q1] `OQ-001`, `OQ-022`; [Q7] `FLOW-OQ-001`, `FLOW-OQ-023` |
| AD-002 | Token validation contract | Needs confirmation | “Algorithms/audiences/claims” are unspecified. | Define accepted algorithms, issuer/audience values, exact claims, and validation configuration. | Hold executable authentication contract; Ready rejection of unexpected algorithms and missing tenancy. | [Q2] `API-OQ-001`; [Q6] `ERR-OQ-002`; [Q7] `FLOW-OQ-001` |
| AD-003 | Session architecture and authentication UX | Needs confirmation | “BFF/cookie selection” and session behavior remain open; BFF cookies are optional. | Select transport and session mechanism; define lifetime, expiry, logout, callbacks, return URLs, and post-login destination. | Hold session implementation; Ready prohibition on long-lived refresh tokens in browser local storage. | [Q1] `OQ-001`; [Q2] `API-OQ-001`; [Q5] `BR-OQ-001`; [Q6] `ERR-OQ-002` |
| AD-004 | Tenant/workspace selection and movement | Needs confirmation | “Context switching” and workspace reassignment are undefined. | Define authorized memberships, defaults, switching, case creation context, and whether/how cases may move workspaces. | Hold selection/movement contracts; Ready immutable trusted tenancy and same-tenant association checks. | [Q1] `OQ-002`; [Q2] `API-OQ-001`, `API-OQ-016`; [Q3] `DAT-OQ-004`; [Q7] `FLOW-OQ-001`, `FLOW-OQ-014` |
| AD-005 | Complete role/resource permission matrix | Needs confirmation | “Owner,” “Member,” and “approver” are scopes without complete role mappings. | Define Workspace Admin/Admin mapping and screen, field, action, resource, and independent-approver predicates. | Hold grants and control visibility decisions; Ready cumulative resource authorization and no implied Admin review authority. | [Q1] `OQ-003`; [Q2] `API-OQ-001`; [Q5] `BR-OQ-001`; [Q7] `FLOW-OQ-001` |
| AD-006 | Principal, Actor, and historical identity mapping | Needs confirmation | “Principal/Actor identity mapping” is incomplete. | Define identity references, user/service distinctions, membership keys, and preservation after principal removal. | Hold identity persistence and public projections; Ready server-derived actors and immutable decision attribution. | [Q3] `DAT-OQ-004`, `DAT-OQ-014`; [Q5] `BR-OQ-001`; [Q6] `ERR-OQ-002` |
| AD-007 | Self/originator and assignment-specific access | Needs confirmation | “Self/originator” and assignment-specific rights are undefined. | Identify the disallowed originating actor and task-specific read/action predicates; define reviewer independence. | Hold actor-comparison fixtures and grants; Ready high-risk and assigned-task no-self-approval safeguards. | [Q1] `OQ-003`, `OQ-013`; [Q5] `BR-OQ-001`, `BR-OQ-013`; [Q7] `FLOW-OQ-012` |
| AD-008 | Internal service identities and protocol bindings | Needs confirmation | “Exact caller identities, audiences, permission scopes” remain open. | Define deployment identities, service audiences, workload credentials, HTTP/gRPC bindings, and mTLS configuration. | Hold service deployment bindings; Ready independently authorized narrow interfaces and no shared deployment-unit identity. | [Q2] `API-OQ-002`; [Q4] `BAT-OQ-002`; [Q7] `FLOW-OQ-001`, `FLOW-OQ-023` |
| AD-009 | Operational/probe access and exposure | Needs confirmation | “Probe authentication” and network exposure are not defined. | Define operational roles, tenant handling, authentication, permitted networks, and safe response projections. | Hold probe/operator access configuration; Ready private datastores and no anonymous-access assumption. | [Q2] `API-OQ-002`, `API-OQ-018`; [Q6] `ERR-OQ-023`; [Q7] `FLOW-OQ-023` |
| AD-010 | Membership administration | TBD | “PUT replacement versus incremental semantics” are unresolved. | Define membership schema, eligible actors, revision/idempotency safeguards, replacement behavior, and escalation prevention. | Hold API-028 contract and administration form; Ready tenant/resource checks and durable change evidence. | [Q2] `API-OQ-016`; [Q3] `DAT-OQ-004`; [Q7] `FLOW-OQ-014` |
| AD-011 | Legal/security hold lifecycle | TBD | “Hold target/states/rights/release” are missing. | Define target inventory, creation/release authority, states, precedence, concurrent hold changes, and read/display contracts. | Hold API-029 lifecycle design; Ready protection of held records and receipted exceptions. | [Q2] `API-OQ-016`; [Q3] `DAT-OQ-018`; [Q5] `BR-OQ-017`; [Q7] `FLOW-OQ-014`, `FLOW-OQ-019` |
| AD-012 | Global versus tenant-owned registry scope | Needs confirmation | “Global versus tenant-owned registry scope” is unspecified. | Classify model, policy, deployment, governance, and operational records; define tenancy and uniqueness accordingly. | Hold physical ownership/predicate design; Ready mandatory tenancy for every tenant-owned row. | [Q3] `DAT-OQ-003`, `DAT-OQ-004`; [Q6] `ERR-OQ-002`; [Q7] `FLOW-OQ-001` |

### Data and Interface Contracts

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-013 | Technical identifier acceptance and transport | Needs confirmation | “UUID lexical acceptance” and non-case declarations are incomplete. | Define accepted UUID forms/versions, generated versus supplied identities, and typed transport for each record/protocol. | Hold parsing and schema declarations; Ready immutable technical identity and separation from business references. | [Q2] `API-OQ-003`; [Q3] `DAT-OQ-003`; [Q7] `FLOW-OQ-002` |
| AD-014 | Revision/BIGINT and precondition contract | Needs confirmation | “If-Match syntax” and full-range BIGINT transport are unresolved. | Define quoting/wildcards, missing/malformed outcomes, numeric encoding, revision allocation, overflow, and non-case preconditions. | Hold executable concurrency contract; Ready monotonic case revisions and stale-write rejection. | [Q1] `OQ-007`; [Q2] `API-OQ-003`, `API-OQ-017`; [Q6] `ERR-OQ-003`; [Q7] `FLOW-OQ-003` |
| AD-015 | Complete case create/read/patch schemas | TBD | “Full case create/read/patch/list schemas” are absent. | Define properties, requiredness, lengths, null/blank rules, edit rights, defaults, owner selection, and patch representation. | Hold forms and wire schemas; Ready retention of every confirmed domain field. | [Q1] `OQ-007`; [Q2] `API-OQ-003`; [Q3] `DAT-OQ-005`; [Q7] `FLOW-OQ-002`, `FLOW-OQ-003` |
| AD-016 | Human-facing case reference | Needs confirmation | Illustrated references differ from technical UUID identity. | Is a separate business reference required? Define generation, sequencing, format, and uniqueness if so. | Hold business-reference generation; Ready UUID-based technical identity. | [Q1] `OQ-007`; [Q3] `DAT-OQ-005`; [C1] `SF-CON-002`; [C7] `FLOW-CNS-022` |
| AD-017 | Case history and update-time behavior | Needs confirmation | “Initial revision-history insertion” and an update-time mechanism are unspecified. | Define revision keys, history patch format, initial entry, actor/time mapping, and accepted-update timestamp behavior. | Hold history DDL and timestamp mechanism; Ready append-only accepted revisions. | [Q3] `DAT-OQ-005`; [Q7] `FLOW-OQ-002`, `FLOW-OQ-003`; [C3] `DAT-CNS-010`, `DAT-CNS-017` |
| AD-018 | Production physical data design | Needs confirmation | “Types, lengths/precision, nullability, defaults” and physical controls are incomplete. | Define missing DDL, database version, PK/FK/uniqueness, same-tenant enforcement, indexes, collation, and partitions. | Hold production physical design; Ready existing PostgreSQL authority and explicit case DDL requirements. | [Q3] `DAT-OQ-001`, `DAT-OQ-003`; [Q5] `BR-OQ-002`; [Q6] `ERR-OQ-004` |
| AD-019 | Logical aliases, persistence, and mutable/immutable separation | Needs confirmation | “Aliases versus separate records” and generic immutable labels conflict with current mutable projections. | Define physical aliases, distinct records, persistence needs, and provenance/history separation. | Hold record merging, duplication, and immutability enforcement; Ready immutable approved history and supported current-state mutation. | [Q3] `DAT-OQ-002`; [C3] `DAT-CNS-002`, `DAT-CNS-003`; [C7] `FLOW-CNS-010` |
| AD-020 | Immutable version and derivative identity | Needs confirmation | “Fingerprint/pipeline derivation” coexists with UUIDv7 and incomplete local version keys. | Define document-version identity, parser/pipeline relationships, source hash, derivative derivation, and canonical encoding. | Hold identity algorithm and version schema; Ready immutable side-by-side reprocessing and source provenance. | [Q3] `DAT-OQ-008`; [Q4] `BAT-OQ-008`; [Q7] `FLOW-OQ-004`; [C3] `DAT-CNS-008` |
| AD-021 | Attachment reuse, duplication, and unlinking | Needs confirmation | “Reuse across cases” and duplicate/removal behavior are unspecified. | Define attachment keys, version reuse, duplicate upload/link handling, removal rights, and shared-object retention. | Hold attachment lifecycle design; Ready immutable document-version references. | [Q3] `DAT-OQ-007`, `DAT-OQ-008`, `DAT-OQ-010`, `DAT-OQ-018`; [Q7] `FLOW-OQ-004`, `FLOW-OQ-019` |
| AD-022 | Layout and source-anchor schema | TBD | “Page/bbox conventions” and nonpaginated-source anchors are undefined. | Define indexing, ranges, geometry, table/block relationships, reading order, and HTML/DOCX/text anchors. | Hold rendering/anchor wire contracts; Ready resolvable exact-version citations and retained layout provenance. | [Q1] `OQ-018`; [Q3] `DAT-OQ-008`; [Q7] `FLOW-OQ-004`, `FLOW-OQ-006` |
| AD-023 | Object storage and naming contract | Needs confirmation | “Object provider/key syntax/object-role vocabulary” remain open. | Define provider, scoped key/reference syntax, roles, filenames, media formats, and orphan/shared-object handling. | Hold storage configuration and physical object schema; Ready encryption, private storage, and required scope dimensions. | [Q3] `DAT-OQ-010`, `DAT-OQ-015`; [Q6] `ERR-OQ-010`, `ERR-OQ-023` |
| AD-024 | Public source delivery and signed URLs | TBD | “Binary-versus-URL API contract” and URL lifetime/recovery are missing. | Define public delivery route/result, immutable-version selection, authorization binding, expiry, renewal, and viewer recovery. | Hold API-057 and delivery UX; Ready current access and exact cited-version inspection. | [Q1] `OQ-018`; [Q2] `API-OQ-008`; [Q3] `DAT-OQ-010`; [Q7] `FLOW-OQ-006` |
| AD-025 | Evidence identity and runless search persistence | Needs confirmation | “Evidence-ID mapping” and runless query association are unresolved. | Map `evidenceId`, evidence-set IDs, chunk references, run association, cardinality, and referential integrity. | Hold API/data identity mappings; Ready permitted immutable evidence provenance. | [Q2] `API-OQ-008`, `API-OQ-023`; [Q3] `DAT-OQ-009`; [Q7] `FLOW-OQ-006` |
| AD-026 | Candidate/approved artifacts and editing | TBD | “Candidate/approved-result schemas” and direct draft editing are undefined. | Define artifact content/reference schema, revision lineage, editing capability, approved-pointer exposure, and absence before publication. | Hold artifact interfaces/editing; Ready separation of candidate, decision, gate, and published lineage. | [Q1] `OQ-012`; [Q2] `API-OQ-010`; [Q3] `DAT-OQ-011`, `DAT-OQ-013`; [Q7] `FLOW-OQ-007`, `FLOW-OQ-012` |
| AD-027 | Model catalog representation and rights | TBD | “Model-catalog response/permissions” are unspecified. | Define deployment metadata, workspace filtering, selectors, read/admin rights, and registry version relationships. | Hold API-026 schema/settings selector; Ready specific-deployment rather than brand-only whitelisting. | [Q1] `OQ-020`; [Q2] `API-OQ-009`; [Q3] `DAT-OQ-011`; [Q7] `FLOW-OQ-010`, `FLOW-OQ-014` |
| AD-028 | Generation, prompt, and provider adapter contracts | TBD | “Prompt/output schemas” and adapter/key transport are incomplete. | Define versioned request/output schemas, signed instructions, composition representation, provider adapters, and attempt records. | Hold API-008 executable contract; Ready scoped composition and strict output validation. | [Q2] `API-OQ-009`; [Q3] `DAT-OQ-011`; [Q5] `BR-OQ-009`; [Q7] `FLOW-OQ-010` |
| AD-029 | IDL versions and compatibility publication | Needs confirmation | “Full OpenAPI/protobuf versions” and repository bindings are missing. | Define IDL versions, repositories, generated artifacts, publication/access, approved examples, and compatibility evidence. | Hold tooling configuration; Ready versioned REST/protobuf contracts and nonbreaking evolution guards. | [Q2] `API-OQ-022`; [Q3] `DAT-OQ-019`; [Q7] `FLOW-OQ-015`, `FLOW-OQ-022` |
| AD-030 | Event schema, canonicalization, and signatures | TBD | “Actor/correlation placement” and typed payloads are unspecified. | Define canonical bytes, signatures, versions, producer/aggregate mappings, actor/correlation placement, and safe SSE/webhook projections. | Hold executable envelopes/projections; Ready required envelope concepts, immutable tenancy, and original event identity. | [Q2] `API-OQ-022`; [Q3] `DAT-OQ-012`; [Q4] `BAT-OQ-011`; [Q7] `FLOW-OQ-015` |

### Durable Execution and Failure Contracts

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-031 | HTTP idempotency binding and lost responses | Needs confirmation | “Namespace/concurrent binding” and lost-response lookup are undefined. | Define fingerprints, key scope, TTL boundaries, simultaneous reservation, error replay, expiry/reuse, and outcome lookup. | Hold binding implementation/recovery; Ready identical replay returns original outcome and changed fingerprint conflicts. | [Q2] `API-OQ-017`; [Q3] `DAT-OQ-012`; [Q6] `ERR-OQ-003`, `ERR-OQ-007`; [Q7] `FLOW-OQ-015` |
| AD-032 | Outbox/consumer deduplication and replay ledger | Needs confirmation | “Claim/ack/atomic ledger” and stale/future disposition are missing. | Define consumer namespaces, acknowledgment, ledger atomicity/retention, incompatible events, checkpoints, and migration provenance. | Hold dispatch/ledger mechanism; Ready one accepted effect, duplicate evidence, and current revision/access checks. | [Q3] `DAT-OQ-012`; [Q4] `BAT-OQ-011`, `BAT-OQ-020`; [Q6] `ERR-OQ-007`; [Q7] `FLOW-OQ-015` |
| AD-033 | Transaction and cross-store crash mechanisms | Needs confirmation | “Transaction isolation/locking” and mandatory audit-failure behavior are unresolved. | Define isolation, locks, reservations, audit placement/failure, consumer transactions, and relational/object crash reconciliation. | Hold mechanism selection; Ready stated ACID boundaries and atomic publication gate/pointer. | [Q2] `API-OQ-017`; [Q3] `DAT-OQ-003`, `DAT-OQ-012`; [Q6] `ERR-OQ-004`; [Q7] `FLOW-OQ-015` |
| AD-034 | Deployment grouping and execution platform | Needs confirmation | “Logical job grouping” does not define deployable units. | Define executable/service grouping, queue/scheduler topology, runtime identities, ownership boundaries, and platform-managed functions. | Hold deployment topology; Ready confirmed logical worker/event functions. | [Q4] `BAT-OQ-002`; [Q3] `DAT-OQ-002`, `DAT-OQ-020`; [Q7] `FLOW-OQ-022` |
| AD-035 | Concurrency, leases, heartbeat, and drain | Needs confirmation | “Locking/lease/fencing” and takeover timing are unspecified. | Define overlap policy, processing units, reservations, fencing, heartbeat/takeover/drain, and concurrency/scale controls. | Hold worker coordination; Ready duplicate-safe effects, durable predecessors, budgets, and current guards. | [Q4] `BAT-OQ-004`; [Q6] `ERR-OQ-016`; [Q7] `FLOW-OQ-009`, `FLOW-OQ-023` |
| AD-036 | Schedules and time-window execution | Needs confirmation | “Scheduler timezone” and launch/catch-up behavior are undefined. | Define required triggers, timer/scanner choices, times, windows, DST/cutoffs, missed runs, and maintenance periods. | Hold schedules; Ready distinct confirmed event-driven, daily, continuous, and scheduled meanings. | [Q4] `BAT-OQ-001`; [Q3] `DAT-OQ-020`; [Q7] `FLOW-OQ-005`, `FLOW-OQ-022` |
| AD-037 | Job arguments, receipts, progress, and no-work outcomes | TBD | “Receipt/result/status/exit codes” and empty-input outcomes are missing. | Define each job’s arguments, states, status inquiry, completion, repeated completion, partial/empty/duplicate-only result, and progress. | Hold executable job contracts; Ready durable acceptance is not completion and no fabricated no-op success. | [Q4] `BAT-OQ-003`; [Q6] `ERR-OQ-024`; [Q7] `FLOW-OQ-015`; `ERR-060`, `BAT-AC-051–057` |
| AD-038 | Retry taxonomy and bounded configuration | Needs confirmation | “Attempts/delays/jitter…exhaustion” are unspecified. | Define stage-specific permanence, parser/model retries, deadlines, circuit breakers, exhaustion, and dead-letter transitions. | Hold retry settings; Ready no automatic permission/schema retry and source-confirmed bounded transient handling. | [Q4] `BAT-OQ-005`; [Q6] `ERR-OQ-008`; [Q7] `FLOW-OQ-009` |
| AD-039 | Error taxonomy and protocol outcomes | TBD | “Simultaneous-failure priority” and non-HTTP mappings are undefined. | Define missing HTTP/business/gRPC/tool/SSE/batch outcomes, safe details, retry flags, exception precedence, and per-interface dependency fallback. | Hold unspecified mappings; Ready canonical safe REST errors and preservation of confirmed literal codes/statuses. | [Q2] `API-OQ-017`; [Q6] `ERR-OQ-001`, `ERR-OQ-003`; [Q7] `FLOW-OQ-015` |

### Case Business Processing

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-040 | Priority calculation | Needs confirmation | “Impact/urgency catalogs” and priority matrix are missing. | Define values, formula/matrix, ties, missing-input behavior, manual override authority, and recalculation triggers. | Hold calculated outputs; Ready explicit impact-and-urgency input, never model-only priority. | [Q1] `OQ-009`; [Q5] `BR-OQ-004`; [Q7] `FLOW-OQ-003` |
| AD-041 | Contractual SLA/calendar and advisory prediction | Needs confirmation | “Start/duration/calendar/timezone/version” are unresolved. | Define calendar, holidays, DST, start/pause/recalculation, breach equality, precision, and advisory prediction schema. | Hold deadline algorithm; Ready workspace-calendar use and prediction cannot alter contractual deadline. | [Q1] `OQ-009`; [Q5] `BR-OQ-005`; [Q7] `FLOW-OQ-003` |
| AD-042 | Classifier and correction contract | Needs confirmation | “Correction precedence” and revision/attachment snapshot are undefined. | Define labels/reasons/confidence, provenance, input snapshot, mutation API, delayed classifier conflicts, and rerun triggers. | Hold classifier/correction executable contract; Ready reason-coded corrections and no stale overwrite. | [Q1] `OQ-010`; [Q4] `BAT-OQ-006`; [Q6] `ERR-OQ-006`; [Q7] `FLOW-OQ-002` |
| AD-043 | Detailed guards for six normal case edges | Needs confirmation | Six edges exist, but “actors/triggers/approval linkage” remain incomplete. | Define each edge’s eligible actor, initiating trigger, evidence/task linkage, and approval consequences. | Hold edge-specific fixtures; Ready retain `SCR-002-T01–T06` without adding normal edges. | [Q1] `OQ-008`; [Q2] `API-OQ-004`; [Q5] `BR-OQ-006`; [Q7] `FLOW-OQ-003` |
| AD-044 | Closing edge and operation | TBD | “Closing origin/request/result” are missing. | Define permitted origin, actor/revision/approval guards, body, response, repeated-close behavior, and snapshot links. | Hold API-017 execution contract; Ready immutable approved-answer/version/decision closure snapshot. | [Q1] `OQ-008`; [Q2] `API-OQ-004`; [Q3] `DAT-OQ-005`; [Q7] `FLOW-OQ-003` |
| AD-045 | Explicit reopening operation | TBD | “Reopening target/endpoint” are unspecified. | Define target state, actors, approvals, request/result, and new-revision linkage. | Hold API-052 contract; Ready CLOSED finality except explicit new-revision reopening preserving history. | [Q1] `OQ-008`; [Q2] `API-OQ-004`; [Q5] `BR-OQ-006`; [Q7] `FLOW-OQ-003` |

### Ingestion and Connector Processing

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-046 | Upload transport and admissibility boundaries | Needs confirmation | “MIME/subtypes/count/name/MB” are incomplete. | Define multipart/body, filenames/counts, exact types/subtypes, text handling, and MB-to-byte boundary. | Hold upload wire/boundary tests; Ready supported formats, MIME agreement, and configured reference cap. | [Q1] `OQ-015`; [Q2] `API-OQ-007`; [Q7] `FLOW-OQ-004` |
| AD-047 | Scanner/parser limits and quarantine remediation | Needs confirmation | “Archive/parser/scanner controls” and unsafe viewing/release are missing. | Define safety thresholds, sandbox resources, failure taxonomy, quarantine rights, remediation, release, and viewing/download policy. | Hold limits/remediation controls; Ready scan-before-parse, no macros/remote fetch, unsafe no indexing. | [Q3] `DAT-OQ-007`; [Q4] `BAT-OQ-008`; [Q6] `ERR-OQ-010`; [Q7] `FLOW-OQ-004` |
| AD-048 | Extraction quality and empty-document treatment | Needs confirmation | “Quality…metrics” lack formulas and thresholds. | Define ratios, table loss, language confidence, zero denominators, empty sources, and autonomous-support thresholds. | Hold quality classification; Ready safe low-quality viewing and autonomous-recommendation exclusion. | [Q1] `OQ-015`; [Q5] `BR-OQ-007`; [Q6] `ERR-OQ-010`; [Q7] `FLOW-OQ-004` |
| AD-049 | OCR opt-in and provenance contract | TBD | “OCR option” representation and placement are undefined. | Define authorized input, provenance schema, supported fallback processing, and status/display linkage. | Hold OCR control/schema; Ready opt-in-only, provenance-marked fallback and deferred non-English OCR. | [Q1] `OQ-015`; [Q3] `DAT-OQ-007`; [Q7] `FLOW-OQ-004` |
| AD-050 | Normalized/exchanged file formats | Needs confirmation | “Encoding,” Unicode normalization, BOM, and serialization are unspecified beyond plain-text upload. | Define derivative/archive encodings, character normalization, line endings, subtype behavior, and file naming/serialization. | Hold format contracts; Ready claim-preserving normalization and UTF-8 plain-text upload. | [Q3] `DAT-OQ-007`, `DAT-OQ-008`, `DAT-OQ-021`; [Q7] `FLOW-OQ-004` |
| AD-051 | Document transitions and readiness | TBD | “Status transitions” and `READY` linkage are incomplete. | Define every edge, partial-index outcome, completion predicate, version selection, status projection, and refresh mechanism. | Hold API-018/state machine; Ready acceptance, normalization, cursor, and queue emptiness are not readiness. | [Q1] `OQ-015`; [Q4] `BAT-OQ-003`, `BAT-OQ-008`, `BAT-OQ-009`; [Q7] `FLOW-OQ-004` |
| AD-124 | Connector providers and configuration | Needs confirmation | “Connector providers/permissions” remain explicit choices. | Select approved providers/permissions and define configuration schema, read/admin rights, and source identity namespaces. | Hold connector adapters/configuration; Ready workspace scope and preservation of source permissions/history. | [Q1] `OQ-016`, `OQ-022`; [Q2] `API-OQ-011`; [Q7] `FLOW-OQ-005` |
| AD-125 | Connector capability/trust matrix | Needs confirmation | “Trust restrictions” by unsupported capability are undefined. | Define missing list/fetch/delta/ACL/delete consequences, restrictions, warnings, and permitted continuation. | Hold trust-policy selection; Ready explicit lower-trust warning and no assumed ACL/capability support. | [Q1] `OQ-016`; [Q4] `BAT-OQ-007`; [Q6] `ERR-OQ-009`; [Q7] `FLOW-OQ-005` |
| AD-126 | Connector credential revoke/reauthorize/resume | TBD | “Credential reauthorization” flow and APIs are absent. | Define operator rights, revoke/reauth interfaces, provider permissions, queued-state treatment, and post-reauth resume. | Hold API-054/055 contract; Ready vault references and revoked queued jobs fail safely with `CONNECTOR_REAUTH_REQUIRED`. | [Q1] `OQ-016`; [Q2] `API-OQ-011`; [Q6] `ERR-OQ-009`; [Q7] `FLOW-OQ-005` |
| AD-127 | Sync cursor, item ledger, and mixed outcomes | Needs confirmation | “Cursor/order/durable-outcome stage” are undefined. | Define provider ordering, cursor partitions/history, item durability, batch bounds, source uniqueness, concurrency/fairness, partial/empty completion. | Hold sync ledger/advancement contract; Ready cursor never skips undurable predecessors and poison exceptions remain recorded. | [Q3] `DAT-OQ-006`; [Q4] `BAT-OQ-007`; [Q6] `ERR-OQ-009`; [Q7] `FLOW-OQ-005` |

### Retrieval, Index, and Cache

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-052 | Search/embedding providers and physical representation | Needs confirmation | “Search/embedding provider and schema” remain open. | Define approved provider, analyzers, index row key, vector precision, embedding adapter, and write batch controls. | Hold provider/physical index design; Ready hybrid retrieval and confirmed reference dimensions. | [Q1] `OQ-022`; [Q3] `DAT-OQ-009`; [Q4] `BAT-OQ-009`; [Q7] `FLOW-OQ-006`, `FLOW-OQ-023` |
| AD-053 | Public search request/result contract | TBD | “Public search schema/filters/pagination” are missing. | Define query requiredness, scope, filters, ordering, limits, cursors, wrappers, and presentation placement. | Hold API-010/UI schema; Ready Member/current-ACL checks and separation from MCP inputs. | [Q1] `OQ-017`; [Q2] `API-OQ-008`; [Q7] `FLOW-OQ-006` |
| AD-054 | Ranking, diversity, and context budgets | Needs confirmation | “Scoring/ties/diversity/token” formulas are absent. | Define RRF details, missing ranks, normalization, deterministic ties, diversity rules, and selected context-token budget. | Hold executable ranking; Ready bounded hybrid candidates and deterministic re-ranking. | [Q3] `DAT-OQ-009`; [Q5] `BR-OQ-008`; [Q7] `FLOW-OQ-006` |
| AD-055 | Insufficient-support routing | Needs confirmation | “Support thresholds/clarification” are unresolved. | Define confidence/quality criteria, outcome envelope/status, clarification versus human selection, and request/resumption path. | Hold next-step workflow; Ready `NO_SUPPORTED_EVIDENCE` and no fabricated context. | [Q1] `OQ-017`; [Q6] `ERR-OQ-011`; [Q7] `FLOW-OQ-006` |
| AD-056 | Rebuild launch, validation, and generation lifecycle | Needs confirmation | “Scope/delta/fencing/completeness/recall/coverage” are undefined. | Define initiation, inventory consistency, overlap, delta/deletion handling, validation thresholds, activation, cleanup, retention, and rollback eligibility. | Hold rebuild mechanism; Ready parallel generation and atomic switch only after successful checks. | [Q3] `DAT-OQ-009`, `DAT-OQ-020`; [Q4] `BAT-OQ-009`, `BAT-OQ-010`; [Q7] `FLOW-OQ-006` |
| AD-057 | ACL invalidation barrier and cache-fill races | Needs confirmation | “Invalidation barrier” is not selected. | Define current-access checks, propagation barrier, affected dependencies, concurrent fills/old events, unavailable-cache behavior, and incident containment. | Hold propagation mechanism; Ready no forbidden evidence on the next query. | [Q4] `BAT-OQ-010`; [Q5] `BR-OQ-016`; [Q6] `ERR-OQ-011`; [Q7] `FLOW-OQ-006`, `FLOW-OQ-023` |
| AD-058 | Cache key, representation, and expiry | Needs confirmation | “Cache key/TTL” details are incomplete. | Define digest/hash canonicalization, dependency mapping, numeric TTL, size/representation, expiry, and recovery. | Hold cache physical contract; Ready required scope components and immediate authorization invalidation. | [Q3] `DAT-OQ-009`; [Q5] `BR-OQ-008`; [Q7] `FLOW-OQ-006` |

### Model, Run, and Agent Execution

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-059 | Approved deployments and fallback selection | Needs confirmation | “Approved models/regions/deployments” and comparison/priority are missing. | Define specific approvals, capabilities, handling-class ordering, context/cost priorities, and fallback routes. | Hold deployment routing configuration; Ready only approved equal-or-stronger handling and approved destinations. | [Q1] `OQ-022`; [Q2] `API-OQ-009`; [Q5] `BR-OQ-009`; [Q7] `FLOW-OQ-010` |
| AD-060 | Relationship between run creation routes | Needs confirmation | Both `POST /v1/runs` and the case-scoped route are retained. | Are they distinct, aliases, or subject to controlled amendment? Define shared behavior and authorization. | Hold route reconciliation; Ready no unrelated duplicate workflow or silent route removal. | [Q2] `API-OQ-006`; [C2] `API-CNS-002`; [Q7] `FLOW-OQ-007` |
| AD-061 | Run request, receipt, steps, and pinned context | TBD | “Request/receipt/case-revision/steps/artifact mappings” are incomplete. | Define inputs, run identity receipt, pinned case revision, state/step enums, budget/checkpoint schemas, and read scopes. | Hold API-005/006/019/032 schemas; Ready immediate durable accepted run and persisted progress. | [Q2] `API-OQ-006`; [Q3] `DAT-OQ-011`; [Q7] `FLOW-OQ-007`, `FLOW-OQ-013` |
| AD-062 | DAG/call counting and parallel dependencies | Needs confirmation | “Depth/call counting under retry/replay” is unspecified. | Define root-depth convention, retries/replayed invocations, nodes/steps, parallel joins, failure propagation, and checkpoint units. | Hold executable counters/parallelism; Ready acyclic depth/call bounds and checkpoint-before-dispatch. | [Q4] `BAT-OQ-012`; [Q5] `BR-OQ-010`; [Q7] `FLOW-OQ-009` |
| AD-063 | Runtime, human-review wait, and timeout states | Needs confirmation | Waiting, missing-approval termination, and recoverable timeout coexist. | Define clocks, equality, review-wait inclusion, worker release/resume, missing-approval failure, and existing-state mapping. | Hold timeout state machine; Ready bounded runtime, exact checkpoint, and no invented timeout enum. | [Q1] `OQ-011`; [C1] `SF-CON-004`; [Q6] `ERR-OQ-012`; [Q7] `FLOW-OQ-009` |
| AD-064 | Token reservation, usage, and exhaustion | Needs confirmation | “Reservation/release/overrun/concurrency/quota reset” are undefined. | Define units, reservation versus actual use, release, provider corrections, concurrent accounting, and terminal result. | Hold accounting/reservation mechanism; Ready exhaustion terminates current run without model/class downgrade. | [Q2] `API-OQ-009`; [Q5] `BR-OQ-011`; [Q6] `ERR-OQ-013`; [Q7] `FLOW-OQ-008` |
| AD-065 | Admission and capacity thresholds | Needs confirmation | “Thresholds/operators/units” and Retry-After calculation are missing. | Define workspace tokens, queue-age and provider-capacity calculations, thresholds, concurrency policy, and other-job admission. | Hold configuration/formulas; Ready failed new-run admission returns `429` plus `Retry-After`, not authorization recovery. | [Q2] `API-OQ-006`, `API-OQ-018`; [Q6] `ERR-OQ-013`; [Q7] `FLOW-OQ-008` |
| AD-066 | MCP transport, schemas, and grants | TBD | “Optionality and lower bounds,” Citation schema, transport, and grant errors are missing. | Define pinned transport/schema, field optionality, maximum-item lower/default behavior, authorization verification, and outcomes. | Hold executable API-046 binding; Ready read-only permitted-document scope, upper bound, and no arbitrary URL/filesystem access. | [Q2] `API-OQ-023`; [Q3] `DAT-OQ-022`; [Q7] `FLOW-OQ-010` |
| AD-067 | A2A handoff contract | TBD | “Output-schema property” and decline/deadline results are absent. | Define transport, typed IDs, input/output registry, grants, correlation, expiry/decline, retry, and alternate-agent behavior. | Hold API-047 wire contract; Ready declared schemas/deadline and independent authorization; decline is not completion. | [Q2] `API-OQ-023`; [Q3] `DAT-OQ-022`; [Q6] `ERR-OQ-012`; [Q7] `FLOW-OQ-010` |

### Deterministic Policy, Review, and Publication

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-068 | Complete deterministic policy decision table | Needs confirmation | “Six-input…table/priorities” and catalogs are missing. | Define action, financial-impact/risk, model class, quality, confidence bands, selecting conditions, reasons, and overlap priority. | Hold executable policy rules; Ready six normalized concepts and four confirmed outcomes, never LLM override. | [Q2] `API-OQ-014`; [Q5] `BR-OQ-012`; [Q7] `FLOW-OQ-011` |
| AD-069 | Material-class provenance and four-control mappings | Needs confirmation | “Unknown handling” and per-class mappings are undefined; aggregation itself is confirmed. | Define material granularity/history, unclassified/changed material, encoding, transport, and routing/redaction/retention/approval maps. | Hold detailed mappings; Ready maximum included class across all four controls. | [Q2] `API-OQ-026`; [Q3] `DAT-OQ-016`; [Q4] `BAT-OQ-024`; [Q7] `FLOW-OQ-011` |
| AD-070 | Configuration/policy/rule version activation | Needs confirmation | “Effective policy/rule version for in-flight work” is unresolved. | Define version relationships, activation, concurrency, retroactivity, normalized-input storage, and revalidation version selection. | Hold version activation mechanism; Ready reproducible inputs plus applied rule-set version. | [Q3] `DAT-OQ-004`, `DAT-OQ-013`, `DAT-OQ-016`; [Q5] `BR-OQ-012`; [Q7] `FLOW-OQ-011`, `FLOW-OQ-014` |
| AD-071 | Automatic allowance and non-review publication path | Needs confirmation | “Non-review gate invocation/Run-state path” is missing. | Define INTERNAL setting semantics and AUTO_ALLOW invocation/state path without bypassing any full gate. | Hold automatic-publication linkage; Ready INTERNAL/AUTO_ALLOW alone never authorizes publication. | [Q1] `OQ-020`; [C1] `SF-CON-009`; [Q4] `BAT-OQ-013`; [Q7] `FLOW-OQ-011` |
| AD-072 | Reviewer pools, assignment, and quorum | Needs confirmation | “Eligibility/task states/quorum” and pool rules are incomplete. | Define pools, organizational/minimum roles, assignment/reassignment, quorum, task visibility, and independence. | Hold routing/quorum design; Ready eligible review with cumulative separation-of-duties guards. | [Q1] `OQ-013`, `OQ-020`; [Q3] `DAT-OQ-013`; [Q5] `BR-OQ-013`; [Q7] `FLOW-OQ-012` |
| AD-073 | Review queue/detail/form/decision schema | TBD | “Required form/rationale/literals” are unspecified. | Define detail delivery, queue cursors, exact required fields, decision literals, rationale, annotations, and read scopes. | Hold API-023/024 and executable form; Ready exact candidate/citations/versions/reasons and incomplete controls disabled. | [Q1] `OQ-013`; [Q2] `API-OQ-010`; [Q6] `ERR-OQ-014`; [Q7] `FLOW-OQ-012` |
| AD-074 | Artifact hash contract | Needs confirmation | “Hash canonicalization” and algorithm/encoding are missing. | Define exact hashed content boundary, algorithm, canonical bytes, encoding, immutable target, and decision/gate linkage. | Hold hash implementation; Ready exact equality binding, no similarity exception or old-hash publication. | [Q3] `DAT-OQ-013`; [Q5] `BR-OQ-013`; [Q6] `ERR-OQ-014`; [Q7] `FLOW-OQ-012` |
| AD-075 | Whether source opening is an enforced decision prerequisite | Needs confirmation | “Actual source-opening guard” is not established by inspection availability. | Must opening be completed before submission? If so, define verifiable behavior and failure/accessibility handling. | Hold click-completion guard; Ready source inspection must be available before approval. | [Q1] `OQ-013`; [Q2] `API-OQ-010`; [Q7] `FLOW-OQ-012` |
| AD-076 | Review lifecycle, expiry SLA, and races | Needs confirmation | “SLA/timezone/expiry race” and state matrix are incomplete. | Define starts, duration, equality, eligible states, timer/scanner, submit-versus-expire race, reassignment/escalation, and notifications. | Hold expiry algorithm; Ready no implicit approval and immutable history. | [Q1] `OQ-013`, `OQ-020`; [Q4] `BAT-OQ-013`; [Q6] `ERR-OQ-014`; [Q7] `FLOW-OQ-012` |
| AD-077 | Elevated override workflow | TBD | “Roles/reason/extent/endpoint” are missing. | Define eligible elevated and secondary actors, audited reason constraints, exact artifact binding, authority extent, and API/UI. | Hold API-053 execution; Ready all three prerequisites and no ordinary Admin/Reviewer bypass. | [Q1] `OQ-014`; [Q5] `BR-OQ-014`; [Q6] `ERR-OQ-014`; [Q7] `FLOW-OQ-012` |
| AD-078 | Explicit rejected-draft rework linkage | Needs confirmation | “Rework/case linkage” and initiation contract are incomplete. | Define new-run revision initiation, payload, parent lineage, task consequences, and any Case-state linkage. | Hold automatic linkage; Ready new revision preserves prior denial and rejection does not automatically change Case state. | [Q1] `OQ-012`, `OQ-008`; [Q5] `BR-OQ-006`, `BR-OQ-014`; [Q7] `FLOW-OQ-012` |
| AD-079 | Publication interface and atomic revalidation | TBD | “Gate atomic revalidation” and independently callable interface are unspecified. | Define trusted invocation, lookup keys, current-access/hash/version races, failure mapping, pointer projection, and Case-resolution linkage. | Hold interface/mechanism and any manual Publish control; Ready exact supported artifact and atomic satisfied gate/pointer. | [Q2] `API-OQ-010`; [Q6] `ERR-OQ-004`, `ERR-OQ-014`; [Q7] `FLOW-OQ-011`, `FLOW-OQ-012` |

### Retention, Lifecycle, Provisioning, and Keys

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-080 | Corporate/class-dependent retention and closed-case eligibility | Needs confirmation | “Corporate/per-class retention” and eligible-closed selector are undefined. | Define classes/periods, eligibility, effective dates, retained lineage, related run/source scope, and shared-data precedence. | Hold production retention policy; Ready routine case retention only eligible CLOSED cases and maximum-class selection. | [Q1] `OQ-020`, `OQ-022`; [Q3] `DAT-OQ-018`; [Q5] `BR-OQ-017`; [Q7] `FLOW-OQ-020` |
| AD-081 | Diagnostic/audit retention calculations | Needs confirmation | “TTL/year arithmetic” and active/archive scope are missing. | Define start/cutoff/timezone, year/day calculation, purge cadence, holds, receipt retention, and audit/diagnostic separation. | Hold arithmetic/schedules; Ready distinct reference diagnostic and audit policies, mandatory audit unsampled. | [Q4] `BAT-OQ-015`; [Q6] `ERR-OQ-019`; [Q7] `FLOW-OQ-017`, `FLOW-OQ-020` |
| AD-082 | Source tombstone and final purge scope | Needs confirmation | “Related objects/shared versions” and historical citation treatment are unresolved. | Define tombstone fields, removal schedule, source/version scope, referenced/shared objects, backups, and retained history versus retrievability. | Hold final-purge inventory; Ready soft-deleted retrieval blocked and approved citation identity not rewritten. | [Q3] `DAT-OQ-008`, `DAT-OQ-018`; [Q4] `BAT-OQ-010`, `BAT-OQ-014`; [Q7] `FLOW-OQ-020` |
| AD-083 | Lifecycle extent and independent approval proof | Needs confirmation | “Tenant/workspace lifecycle extent” and check proof are undefined. | Define operation extent, independent actors, check sequence, proof records, expiry/reuse, and authorized request schema. | Hold API-014/015 approval workflow; Ready single Admin insufficient and export two-person control. | [Q1] `OQ-023`; [Q2] `API-OQ-015`; [Q6] `ERR-OQ-017`; [Q7] `FLOW-OQ-019` |
| AD-084 | Export inventory, package, and delivery | TBD | “Checksums/format/download” and partial/empty packaging are unspecified. | Define consistent inventory, redaction, archive/manifest/names/checksums, status/download expiry, cleanup/resume, and verified completion. | Hold package/delivery contracts; Ready required categories and exclusion of secrets/internal prompts. | [Q1] `OQ-023`; [Q4] `BAT-OQ-019`; [Q6] `ERR-OQ-017`, `ERR-OQ-024`; [Q7] `FLOW-OQ-019` |
| AD-085 | Deletion inventory, held/partial outcomes, and verification | Needs confirmation | “Partial/held-only completion” and backup/relational extent are missing. | Define shared inventory, hold races, relational/blob/index/backup removal, receipts, retry, final states, and verification. | Hold lifecycle completion contract; Ready held records protected and unverified work never declared deleted. | [Q2] `API-OQ-015`, `API-OQ-021`; [Q3] `DAT-OQ-018`; [Q6] `ERR-OQ-017`; [Q7] `FLOW-OQ-019` |
| AD-086 | Data-subject access matching and disclosure | TBD | “Subject matching/redaction” is unspecified. | Define subject identification, permitted inventory disclosure, redaction, rights, and request/result interfaces. | Hold subject-access contract; Ready use of the same lifecycle inventory. | [Q3] `DAT-OQ-018`; [Q5] `BR-OQ-018`; [Q7] `FLOW-OQ-019` |
| AD-087 | Provisioning initiation and partial recovery | TBD | “API/roles/config/order/completion/compensation” are absent. | Define required configuration, actors, initiation/status, ordering, idempotency, partial-resource resume/compensation, and verification. | Hold API-056/workflow implementation; Ready one idempotent workflow and incomplete state blocks sync. | [Q2] `API-OQ-016`; [Q4] `BAT-OQ-018`; [Q6] `ERR-OQ-016`; [Q7] `FLOW-OQ-016` |
| AD-088 | Historic backfill windows, receipts, and coverage | Needs confirmation | “Windows/order/source uniqueness/batch receipts” and coverage threshold are undefined. | Define bounds/timezone, ordering, stable IDs, restart, late changes, poison/empty batches, receipts, and readiness formula. | Hold selectors/coverage algorithm; Ready bounded backfill and readiness never inferred from queue emptiness. | [Q3] `DAT-OQ-018`, `DAT-OQ-020`; [Q4] `BAT-OQ-018`; [Q7] `FLOW-OQ-016` |
| AD-089 | Key isolation, references, rotation, and destruction | Needs confirmation | “Key isolation/rotation throughput/policy” and platform/app responsibility remain open. | Define per-tenant isolation, reference/version schema, access, regional placement, rotation cadence/mechanism, old keys, recovery, and destruction evidence. | Hold key lifecycle design; Ready scoped vault-backed secrets and no request-path bulk re-encryption workaround. | [Q1] `OQ-022`; [Q3] `DAT-OQ-015`; [Q4] `BAT-OQ-023`; [Q7] `FLOW-OQ-020` |
| AD-090 | Audit inquiry and hash-chain/archive contract | TBD | “Hash chain/batch/archive format/ack/continuation” are incomplete. | Define redaction/detail/filter/cursor rights, action/digest fields, canonical bytes, batches, archive verification, acknowledgment, and continuation. | Hold API-011 detail/archival mechanism; Ready append-only independently retained evidence and no historical edits. | [Q1] `OQ-019`; [Q3] `DAT-OQ-014`; [Q6] `ERR-OQ-019`; [Q7] `FLOW-OQ-017` |

### Usage, Evaluation, Governance, and Release

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-091 | Usage/cost schema and units | TBD | “Currency/units/rates/precision” and scope are undefined. | Define ledger identity, token/billing distinctions, cost rates, categories, currency, rounding, inquiry scope, and attribution schema. | Hold API-012/accounting outputs; Ready actual run/deployment/cost-center attribution across usage categories. | [Q2] `API-OQ-013`; [Q3] `DAT-OQ-014`; [Q5] `BR-OQ-020`; [Q7] `FLOW-OQ-018` |
| AD-092 | Daily rollup and forecast calculation | Needs confirmation | “Reporting day/launch/cutoff/zero/late/partial corrections” are missing. | Define day/timezone, formulas, forecast horizon/confidence, provider adjustments, duplicates, rerun/versioning, and finalization. | Hold executable aggregates; Ready daily budget/forecast/rejected-request concepts and no double accepted accounting effect. | [Q4] `BAT-OQ-016`; [Q5] `BR-OQ-020`; [Q6] `ERR-OQ-020`; [Q7] `FLOW-OQ-018` |
| AD-093 | Operational metric definitions | Needs confirmation | “Formulas, windows, labels” and units are absent. | Define golden/AI/queue/backlog/grounding/empty-rate metrics, denominators, time buckets, and safe tenant projection. | Hold measurement pipelines; Ready required signal categories and privacy-safe correlation. | [Q2] `API-OQ-018`; [Q3] `DAT-OQ-014`; [Q4] `BAT-OQ-025`; [Q7] `FLOW-OQ-023` |
| AD-094 | SLO calculation and latency boundary | Needs confirmation | “Month/percentile/equality” is unresolved; “within” and “under” 300 ms differ. | Define period, denominator/exclusions, P95 method, exact latency boundary, and availability/error-budget calculation. | Hold final acceptance arithmetic; Ready retain reference objectives without selecting the disputed interpretation. | [Q5] `BR-OQ-022`; [C5] `BR-CNS-018`; [C7] `FLOW-CNS-027`; [Q7] `FLOW-OQ-023` |
| AD-095 | Evaluation setup, states, and result interfaces | TBD | “Setup/state/corpus/result” contracts are incomplete. | Define API-013/045 inputs, versions, identity/state, permissions, progress, resume/new evaluation, and retention. | Hold executable evaluation interfaces; Ready durable acceptance and actual execution distinct from quality pass. | [Q2] `API-OQ-013`; [Q3] `DAT-OQ-017`; [Q6] `ERR-OQ-021`; [Q7] `FLOW-OQ-021` |
| AD-096 | Frozen fixture integrity and reproducibility | Needs confirmation | “Signed manifest verification” and fixture repair are undefined. | Define corpus/expected-output format, signatures, independent leakage review, seed storage, evaluated version binding, and compromised-fixture recovery. | Hold harness integrity mechanism; Ready frozen versioned synthetic expectations cannot be rewritten to pass. | [Q3] `DAT-OQ-017`; [Q4] `BAT-OQ-017`; [Q6] `ERR-OQ-021`; [Q7] `FLOW-OQ-021` |
| AD-097 | Evaluation statistics and incomplete evidence | Needs confirmation | “Statistical formulas/domain aggregation/confidence/rounding” are missing. | Define numerators/denominators, aggregation/weighting, confidence method/level, distribution shift, zero/missing cases, and gate composition. | Hold score computation; Ready actual reference targets, zero critical exceptions, and low-confidence release blocking. | [Q5] `BR-OQ-023`; [Q6] `ERR-OQ-021`; [Q7] `FLOW-OQ-021` |
| AD-098 | Individual critical security requirements | TBD | “Individual critical SEC definitions” and threat mappings are unavailable. | Obtain definitions of `SEC-001–SEC-012`, test/control linkage, independent verification, and signed exit evidence. | Hold detailed SEC fixtures/mapping; Ready critical isolation/approval findings block promotion regardless of score. | [Q3] `DAT-OQ-017`, `DAT-OQ-019`; [Q5] `BR-OQ-023`; [Q6] `ERR-OQ-021`; [Q7] `FLOW-OQ-021` |
| AD-099 | Design governance and revision allocation | TBD | “Impacts/revision/roles” and approval schemas are missing. | Define impact scale, governance rights, requirement/test links, approval, version allocation/reset, and baseline read/change records. | Hold API-030/031 contract; Ready revised invariant links to negative test and accepted baseline traceability. | [Q2] `API-OQ-020`; [Q3] `DAT-OQ-019`; [Q7] `FLOW-OQ-022` |
| AD-100 | IaC/CI platform, graph, and signed artifacts | Needs confirmation | “IaC/pipeline platform/graph/signing/build” is unspecified; Terraform/Bicep are alternatives. | Define platform, repositories, stage dependencies, config/artifact schemas, signatures, allowed build identity, and evidence publication. | Hold tool/platform selection; Ready verified build digests, SBOM/tests, signed configuration, and vault-only secret references. | [Q4] `BAT-OQ-021`; [Q5] `BR-OQ-023`; [Q7] `FLOW-OQ-022` |
| AD-101 | Migration backfill and replica coordination | Needs confirmation | “Row bounds/checkpoints/old-replica coordination” are undefined. | Define migration-specific selectors/batches, commits, resume, checks, drain evidence, constraint timing, and supported compensation/readability. | Hold migration mechanism; Ready expand/backfill/enforce and no removal while active readers depend on fields. | [Q3] `DAT-OQ-019`; [Q4] `BAT-OQ-021`; [Q6] `ERR-OQ-022`; [Q7] `FLOW-OQ-022` |
| AD-102 | Canary/promotion and rollback contract | Needs confirmation | “Threshold/duration” and sign-off/proof/status contracts are missing. | Define baseline, thresholds, duration, roles/proof, release API/result, repeated promotion, and explicitly supported data compensation. | Hold executable gates; Ready failed critical gates block promotion and regression rolls traffic/binary routing back, not automatic DB down-migration. | [Q2] `API-OQ-020`; [Q4] `BAT-OQ-021`; [Q6] `ERR-OQ-022`; [Q7] `FLOW-OQ-022` |

### Operations, Privacy, and Presentation

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-103 | Primary/recovery regions and infrastructure bindings | Needs confirmation | “Provider/search/region/key choices” include unselected region and deployment details. | Define approved primary/warm regions, storage placement, provider/network bindings, declared egress, and infrastructure configuration. | Hold infrastructure bindings; Ready primary writes/warm recovery, private datastores, controlled egress, and deferred active/active mutation. | [Q1] `OQ-022`; [Q2] `API-OQ-002`, `API-OQ-021`; [Q7] `FLOW-OQ-023` |
| AD-104 | Health, capacity, metrics, and degraded-mode interfaces | TBD | “Operational schemas/probe…status” are absent. | Define live/ready checks, statuses, timeouts, metric protocol, capacity units, mode vocabulary, and browser projection. | Hold API-038–042 contracts; Ready safe authorized inquiry and no inferred health status or GET mutation. | [Q2] `API-OQ-018`; [Q6] `ERR-OQ-023`; [Q7] `FLOW-OQ-023` |
| AD-105 | Backup and consistent regional restoration | Needs confirmation | “Restore inventory/order/roles/exercise cadence” are unspecified. | Define provider/retention, coherent recovery point, relational/object/index order, commands, roles, evidence, and RPO/RTO measurement. | Hold restore implementation/exercises; Ready incident-command restoration and tested consistency under reference targets. | [Q3] `DAT-OQ-020`; [Q4] `BAT-OQ-023`; [Q6] `ERR-OQ-023`; [Q7] `FLOW-OQ-023` |
| AD-106 | Incident controls and bounded operator replay | TBD | “Pause/re-enable” controls and replay limits/dry-run transport are missing. | Define scope, roles, control interfaces, reason/limits, transformed-event provenance, fingerprints/probes, verification, and partial replay. | Hold operational controls; Ready scoped source-preserving repair, reason/dry-run/limit, and negative access tests before resume. | [Q4] `BAT-OQ-020`; [Q6] `ERR-OQ-007`, `ERR-OQ-018`; [Q7] `FLOW-OQ-015`, `FLOW-OQ-023` |
| AD-107 | Alert, paging, ticket, and incident-response configuration | Needs confirmation | “Named recipients/channels/escalation” and thresholds are absent. | Define budgets, severity, routing, suppression/deduplication, acknowledgment/escalation, configured ticket owner, and past-disclosure remediation. | Hold alert settings/ownership assignment; Ready user-impact paging categories and routine-spend ticket distinction. | [Q4] `BAT-OQ-025`; [Q6] `ERR-OQ-018`; [Q7] `FLOW-OQ-023` |
| AD-108 | PII, redaction, sanitizer, and log policy | Needs confirmation | “Safe log fields/levels/sanitizer/stack/PII” are undefined. | Define tagging/confidence, minimization exceptions, redaction versions, allowlists, levels, stack traces, signed-URL/key handling, and leaked-log remediation. | Hold logging/redaction implementation; Ready global document/secret prohibitions and highest-class controls. | [Q3] `DAT-OQ-014`, `DAT-OQ-016`; [Q6] `ERR-OQ-019`; [Q7] `FLOW-OQ-017`, `FLOW-OQ-020`, `FLOW-OQ-023` |
| AD-109 | Canonical screens, routes, actions, and navigation | Needs confirmation | “Canonical screen/menu labels” and route/action behavior are missing. | Define aliases, active highlights, landing, direct links, no-selection states, primary actions, contextual routes, and launch modes. | Hold navigation contract; Ready retain eight confirmed primary screens and authorized citation inspection. | [Q1] `OQ-004`; [Q7] `FLOW-OQ-013`, `FLOW-OQ-024` |
| AD-110 | Lists, filters, cursors, and pagination | TBD | “Columns/access scope” and cursor/list behavior are undefined. | Define supported search/filter/sort/bulk actions, page schema/size/direction/expiry/snapshot, totals, ordering, and retained position per inquiry. | Hold list/query contracts; Ready server cursor and current authorization principles, without invented parameters. | [Q1] `OQ-006`, `OQ-013`, `OQ-019`; [Q2] `API-OQ-003`, `API-OQ-012`; [Q7] `FLOW-OQ-013` |
| AD-111 | Error/loading/empty/focus and unsaved-state UX | TBD | “Error placement/copy/focus” and unsaved values are missing. | Define hidden/disabled controls, validation timing, dialogs/toasts, loading versus empty, retry/reconciliation, back behavior, and focus recovery. | Hold detailed UX; Ready safe truthful accessible displays and no silent overwrite. | [Q1] `OQ-005`, `OQ-006`, `OQ-026`; [Q6] `ERR-OQ-005`; [Q7] `FLOW-OQ-013` |
| AD-112 | Browser/device/locale and accessibility implementation | Needs confirmation | “Supported browsers/devices” and responsive/locale details are undefined. | Define browser/device scope, breakpoints, locale options, focus/live-region behavior, and detailed accessibility verification. | Hold compatibility/layout matrix; Ready WCAG 2.2 AA target, keyboard/focus, meaningful announcements, and timezone-labelled display. | [Q1] `OQ-026`; [Q3] `DAT-OQ-021`; [Q7] `FLOW-OQ-013` |
| AD-113 | Overview and illustrated summary aggregates | TBD | “Formulas/refresh” and backing APIs are absent. | Define scope, permission, counts/coverage formulas, state vocabularies, workflow-label mappings, refresh, and unknown/error values. | Hold API-058/dashboard implementation; Ready fixtures are not defaults, limits, or benchmark metrics. | [Q1] `OQ-027`, `OQ-004`; [Q2] `API-OQ-025`; [Q7] `FLOW-OQ-024` |
| AD-114 | Usage & Quality/evaluation screen arrangement | Needs confirmation | “Combined/separate…arrangement” is unresolved. | Define one screen/tabs/separate arrangement, scope, primary action, filters, progress, and result presentation. | Hold screen split/layout; Ready confirmed usage and evaluation capabilities remain available for contract definition. | [Q1] `OQ-021`; [Q2] `API-OQ-013`; [Q7] `FLOW-OQ-018` |
| AD-115 | Additional administrative/operator screen placement | Needs confirmation | API existence does not confirm additional screens. | Are screens/forms required for membership, holds, provisioning, export/delete, governance, release, webhook administration, or replay? Define inventory/launch if confirmed. | Hold new screens/user controls; Ready preserve internal-versus-browser boundaries. | [Q1] `OQ-024`, `OQ-023`; [Q2] `API-OQ-025`; [Q7] `FLOW-OQ-024` |
| AD-116 | Browser notifications | TBD | “Channels/read state” and recipients are missing. | Define content, channels, delivery/read persistence, permissions, recipients, destinations, retry, and completion notifications. | Hold API-059/notification implementation; Ready scoped non-sensitive content boundaries. | [Q1] `OQ-025`; [Q2] `API-OQ-025`; [Q6] `ERR-OQ-025`; [Q7] `FLOW-OQ-024` |
| AD-117 | Optional outbound webhook contract | TBD | “Method/subscription/payload/signature/age/ack” are unspecified. | Define recipient management, events, canonical bytes, signature/key rotation, age/skew, acknowledgment, retries/dead letters/order/replay. | Hold API-048 delivery contract; Ready signed age-verified delivery and failure never reverses case commit. | [Q2] `API-OQ-024`; [Q3] `DAT-OQ-022`; [Q4] `BAT-OQ-022`; [Q7] `FLOW-OQ-024` |

### Unadopted Proposals

These suggestions remain proposals. Resolving an associated requirement does not adopt the suggested arrangement.

| Item ID | Subject | Status | Reason remaining unresolved | Questions to confirm | Affected scope and work boundary | Related specifications and IDs |
|---|---|---|---|---|---|---|
| AD-118 | Suggested primary actions | Unadopted proposal | “Proposal: Create Case” and other primary-action suggestions are not approvals. | Confirm the primary action, label, eligibility, and placement for each screen. | Hold proposed prioritization; Ready confirmed underlying operations. | [01_screen_functions.md](01_screen_functions.md#functions-by-screen), “Functions by Screen,” `SCR-001-A03`, `SCR-002-A06`, `SCR-006-A02`, `SCR-007-A02`; [Q1] `OQ-004` |
| AD-119 | Contextual/source navigation arrangements | Unadopted proposal | “Context-preserving return is a Proposal.” | Adopt or reject case-row/context links, source launch mode, and return behavior explicitly. | Hold proposed routes/panels; Ready verified citation activation and highlighted anchors. | [01_screen_functions.md](01_screen_functions.md#navigation-requirements), “Navigation Requirements,” `SF-NAV-005`, `SF-NAV-006`; “SCR-003 — Evidence Viewer,” `SCR-003-A05`; [Q1] `OQ-004`, `OQ-018` |
| AD-120 | Form placement and control representations | Unadopted proposal | “Suggested control representations are Proposals.” | Confirm creation/search placement, field controls, settings selectors, layouts, and per-field editability. | Hold proposed forms; Ready domain-field existence does not imply editable input. | [01_screen_functions.md](01_screen_functions.md#shared-field-contract-conventions), “Shared Field-Contract Conventions”; “Functions by Screen,” `SCR-001-A03`, `SCR-003-F01`, `SCR-007-F03`; [Q1] `OQ-007`, `OQ-017`, `OQ-020` |
| AD-121 | Proposed case JSON/bearer transport example | Unadopted proposal | “These JSON properties and token transport are Proposals.” | Approve executable properties, optionality, receipt, media type, and authentication carriage independently. | Hold example as implementation contract; Ready literal API-001 path/status and idempotency semantics. | [02_api.md](02_api.md#proposal--case-create-and-receipt-shapes), “Proposal — Case Create and Receipt Shapes,” `API-001`, `API-OQ-001`, `API-OQ-003` |
| AD-122 | Proposed SSE wire representation | Unadopted proposal | “Event name, payload names, and offset encoding…are Proposals.” | Confirm media/header, event names, payload, offset type, and stream lifecycle. | Hold example wire implementation; Ready SSE, monotonic offsets, and scoped retained backfill. | [02_api.md](02_api.md#proposal--sse-wire-representation), “Proposal — SSE Wire Representation,” `API-007`, `API-OQ-006` |
| AD-123 | Suggested reload/reconcile caller recovery | Unadopted proposal | “Reload-and-explicit-reconciliation UX remains a Proposal.” | Confirm reconciliation steps, preserved input, focus, retry controls, and explicit user consent. | Hold client recovery algorithm; Ready no silent overwrite or automatic latest-revision replay. | [02_api.md](02_api.md#failure-register-and-caller-behavior), “Failure Register and Caller Behavior,” `API-CNC-001`; [06_exception_handling.md](06_exception_handling.md#identity-input-and-case-handling), “Identity, Input, and Case Handling,” `ERR-007`; [Q6] `ERR-OQ-005` |

## Items Resolved by the Specifications

Resolution below is deliberately scoped. It does not close an entire compound open question when its schemas, mappings, or mechanisms remain unspecified.

| Resolution ID | Original question or deferred reference | Statements establishing the answer | Referenced files, sections, and IDs | Reason for resolution and remaining boundary |
|---|---|---|---|---|
| RES-001 | Stage 1 references API work as “To be defined in a later stage.” | Stage 2 defines a “Public Business API Inventory,” literal methods/paths, shared contracts, and error/acceptance requirements. | [01_screen_functions.md](01_screen_functions.md#dependencies-on-later-specifications), “Dependencies on Later Specifications,” `OQ-007`, `OQ-011`, `OQ-013`; [02_api.md](02_api.md#public-business-api-inventory), “Public Business API Inventory,” `API-001–API-059`, `API-IF-001`, `API-ERR-001` | **Deliverable availability and explicitly confirmed API portions are resolved.** Missing wire schemas and permissions remain AD-001–AD-117 as applicable; the whole API contract is not resolved. |
| RES-002 | Earlier stages defer “Data definitions” and complete domain representation. | Stage 3 states “Preserve the complete source-supported domain information” and defines entity/field inventories and lifecycle obligations. | [01_screen_functions.md](01_screen_functions.md#dependencies-on-later-specifications), “Dependencies on Later Specifications,” `OQ-007`, `OQ-012`; [02_api.md](02_api.md#carry-forward-dependencies), “Carry-Forward Dependencies,” `API-CNS-005`; [03_data.md](03_data.md#data-inventory-and-relationships), “Data Inventory and Relationships,” `DAT-SCP-001`, `DAT-001–DAT-063` | **Data specification availability and preservation obligation are resolved.** Production DDL and mappings remain AD-013–AD-030 and related lifecycle items. |
| RES-003 | Earlier stages defer processing and exception-handling specifications. | Stage 6 defines `ERR-001–ERR-060`; Stage 7 connects initiation, processing, outcomes, and recovery through `FLOW-001–FLOW-022`. | [04_batch_functions.md](04_batch_functions.md#dependencies-and-required-carry-forward), “Dependencies and Required Carry-Forward,” `BAT-OQ-003`, `BAT-OQ-005`; [05_business_rules.md](05_business_rules.md#dependencies-on-earlier-and-later-specifications), “Dependencies on Earlier and Later Specifications,” `BR-OQ-002`, `BR-OQ-010`; [06_exception_handling.md](06_exception_handling.md#exception-inventory-and-classification), “Exception Inventory and Classification,” `ERR-SCP-001–003`; [07_processing_flows.md](07_processing_flows.md#flow-inventory-and-prerequisites), “Flow Inventory and Prerequisites,” `FLOW-SCP-001`, `FLOW-001–FLOW-022` | **The deferred documents now exist.** They explicitly retain missing algorithms, thresholds, states, and mechanisms; those decisions remain open. |
| RES-004 | Stage 6 says “The identity and contents of Stage 7 are not supplied here.” | The supplied Stage 7 is “Processing Flow Specification” with flow procedures, diagrams, mappings, and acceptance criteria. | [06_exception_handling.md](06_exception_handling.md#specification-basis), “Specification Basis,” `ERR-CNS-021`; [07_processing_flows.md](07_processing_flows.md#specification-basis-and-status), “Specification Basis and Status,” `FLOW-SCP-001`, `FLOW-CNS-028` | **Stage 7 identity/availability is resolved by the supplied document**, not by assuming what an absent stage would contain. |
| RES-005 | Earlier field wording says “Policy uses the maximum class of included material” without enumerating all control boundaries. | “The model route, log redaction, retention, and approval policy depend on the maximum class” is explicit and consistently retained. | [01_screen_functions.md](01_screen_functions.md#scr-002--case-detail), “SCR-002 — Case Detail,” `SCR-002-F10`; [02_api.md](02_api.md#api-cls-001), “Deterministic Policy and Maximum Included-Material Classification,” `API-CLS-001`, `API-CNS-013`, `API-AC-034`; [03_data.md](03_data.md#dat-cls-001--maximum-included-material-classification), `DAT-CLS-001`, `DAT-AC-023`; [07_processing_flows.md](07_processing_flows.md#shared-prerequisites-and-control-obligations), `FLOW-CTL-010`, `FLOW-AC-019` | **The four-control aggregation obligation is resolved.** AD-069/AD-070 retain provenance, unknown-class handling, mappings, and activation. The requested earlier-file amendment is not performed here. |
| RES-006 | Could INTERNAL/AUTO_ALLOW bypass required evidence or restricted/high-risk review? | “INTERNAL alone is not sufficient authorization to publish”; “AUTO_ALLOW is not a universal bypass”; the full gate remains cumulative. | [01_screen_functions.md](01_screen_functions.md#scr-007--policy-settings), “SCR-007 — Policy Settings,” `SCR-007-F11`, `SF-CON-009`; [05_business_rules.md](05_business_rules.md#shared-rule-evaluation-and-conflict-boundaries), `BR-026`, `BR-031`; [07_processing_flows.md](07_processing_flows.md#draft-review-policy-and-publication-branches), `FLOW-007-S11`, `FLOW-007-S16`, `FLOW-CNS-008` | **No-bypass semantics are resolved.** The exact automatic/no-review invocation and selecting rules remain AD-068–AD-071/AD-079. |
| RES-007 | Is the Case transition matrix wholly TBD? | All seven specifications retain the six normal edges and CLOSED finality; later stages say “complete only missing” guards/closing/reopening. | [01_screen_functions.md](01_screen_functions.md#confirmed-case-state-transitions), `SCR-002-T01–T08`, `OQ-008`; [02_api.md](02_api.md#api-003-confirmed-normal-transition-contract), `API-003`, `API-CNS-001`; [03_data.md](03_data.md#dat-state-001--case-transition-data-contract), `DAT-STATE-001`; [07_processing_flows.md](07_processing_flows.md#flow-003--case-inquiry-mutation-state-closure-and-reopening), `FLOW-003-S03`, `FLOW-CNS-002` | **The six permitted normal edges are resolved, not erased by later deferrals.** AD-043–AD-045 retain all missing details. |
| RES-008 | Does earlier high-risk wording establish an assigned-task self-approval exception? | Later specifications explicitly retain `approval_tasks` “no self approval” and state “no assigned-task self-approval exception.” | [01_screen_functions.md](01_screen_functions.md#users-and-permissions), `SF-SCP-003`, `OQ-003`; [05_business_rules.md](05_business_rules.md#reviewer-eligibility-and-decision-capture), `BR-027`, `BR-CNS-005`; [06_exception_handling.md](06_exception_handling.md#identity-input-and-case-handling), `ERR-002`, `ERR-CNS-012`; [07_processing_flows.md](07_processing_flows.md#flow-007--bounded-draft-review-and-atomic-publication), `FLOW-007-S14`, `FLOW-CNS-006` | **No undocumented assigned-task exception is established.** AD-007/AD-072 retain self/originator, eligibility, and independence definitions. |
| RES-009 | Could authentication/resource denial follow the quota retry branch? | “Authentication/resource denial is not admission throttling”; FLOW-007-S02 rejects authority failure, while S04 uses `429`/`Retry-After` for new-work admission. | [06_exception_handling.md](06_exception_handling.md#model-tool-budget-and-policy-handling), `ERR-002`, `ERR-035`; [07_processing_flows.md](07_processing_flows.md#shared-prerequisites-and-control-obligations), `FLOW-CTL-003`; “Identity, Validation, Admission, and Replay Branches,” `FLOW-BRANCH-001`, `FLOW-AC-002`, `FLOW-AC-003` | **Branch separation is resolved.** AD-002/AD-005/AD-039/AD-065 retain actual claims, denial codes, and admission thresholds. |
| RES-010 | Do GET/component-register references create mutations, job launches, or public internal endpoints? | “A GET inquiry is not automatically a business mutation”; internal endpoints are not automatically browser-accessible. | [02_api.md](02_api.md#api-inventory-and-responsibilities), `API-SCP-002`, `API-CNS-011`, `API-CNS-017`; [03_data.md](03_data.md#screen-and-api-data-access-matrix), `DAT-LIFE-001`; [07_processing_flows.md](07_processing_flows.md#consistency-findings-and-required-amendments), `FLOW-CNS-021` | **No implied mutation/exposure is resolved.** AD-009/AD-104/AD-115 retain probe, inquiry, fallback, and screen contracts. |
| RES-011 | Does safe low quality mean malware or mandatory no-index treatment? | “Safe low-quality documents remain viewable” but cannot support autonomous recommendations; later specifications explicitly reject a universal low-quality no-index rule. | [01_screen_functions.md](01_screen_functions.md#attachment-fields), `SCR-002-F23`; [04_batch_functions.md](04_batch_functions.md#bat-003--document-scanning-extraction-and-normalization), `BAT-003`, `BAT-CNS-020`; [06_exception_handling.md](06_exception_handling.md#connector-and-ingestion-handling), `ERR-021`, `ERR-023`; [07_processing_flows.md](07_processing_flows.md#ingestion-sync-and-retrieval-branches), `FLOW-CNS-015` | **The quality/quarantine distinction is resolved.** AD-047/AD-048 retain thresholds, empty sources, and unsafe-viewing policy. |
| RES-012 | Does duplicate evidence mean another accepted business/audit transition? | “One accepted-transition audit record” remains; duplicate outcome is recorded “without another accepted mutation.” | [04_batch_functions.md](04_batch_functions.md#notifications-logging-and-monitoring), `BAT-LOG-003`; [06_exception_handling.md](06_exception_handling.md#recorded-evidence-and-field-contracts), `ERR-LOG-002`, `ERR-CNS-006`; [07_processing_flows.md](07_processing_flows.md#flow-011--outbox-delivery-reconciliation-and-operator-replay), `FLOW-011-S03`, `FLOW-AC-023` | **Accepted-effect versus duplicate-attempt evidence is resolved.** Ledger atomicity, retention, and acknowledgment remain AD-032/AD-033. |
| RES-013 | Are `24` hours, short cache TTL, diagnostic retention, and audit retention interchangeable? | The specifications explicitly describe them as “separate policies” and prohibit a universal TTL or RPO-derived schedule. | [02_api.md](02_api.md#idempotency-and-concurrency), `API-IDEM-003`, `API-IDEM-005`; [03_data.md](03_data.md#retention-export-deletion-and-legal-holds), `DAT-RET-002–006`; [07_processing_flows.md](07_processing_flows.md#consistency-findings-and-required-amendments), `FLOW-CNS-020` | **Scope separation is resolved.** Actual boundaries, additional TTLs, arithmetic, and schedules remain AD-031/AD-032/AD-036/AD-058/AD-081/AD-105. |
| RES-014 | Can existing uppercase error literals be lowercased to follow generic naming wording? | Every specification directs preservation of the concrete uppercase literals. | [01_screen_functions.md](01_screen_functions.md#source-consistency-and-required-clarifications), `SF-CON-005`; [02_api.md](02_api.md#canonical-error-body), `API-ERR-001`; [06_exception_handling.md](06_exception_handling.md#consistency-findings-and-required-amendments), `ERR-CNS-001`; [07_processing_flows.md](07_processing_flows.md#consistency-findings-and-required-amendments), `FLOW-CNS-019` | **Existing literal preservation is resolved.** Future naming and all undefined mappings remain AD-039; the reported generic wording mismatch is not erased. |
| RES-015 | Does `TenantDeletionVerified` establish export/provisioning completion? | Its stated consumer closes the verified purge record; later specifications explicitly say not to emit it for export/provisioning. | [02_api.md](02_api.md#source-event-register), `API-EVT-001`, `TenantDeletionVerified`; [04_batch_functions.md](04_batch_functions.md#consistency-findings-and-required-amendments), `BAT-CNS-014`; [07_processing_flows.md](07_processing_flows.md#flow-015--controlled-export), `FLOW-015-S06`; “Flow-016 — Legal-Hold-Safe Verified Deletion,” `FLOW-016-S08`, `FLOW-CNS-018` | **The supplied specifications consistently define the purge-verification purpose.** Export/provisioning completion transport remains AD-084/AD-087; no new event is invented. |
| RES-016 | Does a logical batch/flow inventory establish independently deployed executables? | “Not confirmation that twenty-six independently deployed jobs exist”; flow inventory is also analytical grouping. | [04_batch_functions.md](04_batch_functions.md#logical-job-inventory), `BAT-SCP-003`, `BAT-001–BAT-026`, `BAT-CNS-001`; [07_processing_flows.md](07_processing_flows.md#flow-inventory), `FLOW-001–FLOW-022`, `FLOW-CON-001` | **No implied deployment count is resolved.** Actual grouping/platform/concurrency remains AD-034/AD-035. |

## Cross-Specification Conflicts and Pending Decisions

The following statements are both retained. Reported source inconsistencies are treated as descriptions in the supplied Markdown, not independently verified source facts. No statement wins because it is later or more frequent.

| Conflict ID | Statements and references | Impact | Pending confirmation |
|---|---|---|---|
| CF-001 | “Both `POST /v1/runs` and `POST /v1/cases/{caseId}/runs` appear” — [C1] `SF-CON-007`; the API inventory retains API-005 and API-032 — [C2] `API-CNS-002`; [C7] `FLOW-CNS-003`. | Ambiguous initiation, authorization, receipt, and duplication behavior. | AD-060/AD-061: establish distinct/alias/amendment relationship without deleting either occurrence by assumption. |
| CF-002 | Run vocabulary includes `AWAITING_REVIEW`; the specifications also report “termination occurs on missing approval” and a “recoverable timeout” with only `FAILED` in the failure vocabulary — [C1] `SF-CON-004`; [C2] `API-CNS-003`; [C3] `DAT-CNS-014`; [C4] `BAT-CNS-004`; [C5] `BR-CNS-002`; [C6] `ERR-CNS-003`; [C7] `FLOW-CNS-004`. | Runtime clocks, worker occupancy, expiry, resumption, and terminal-state tests cannot be completed. | AD-063/AD-076: define normal wait versus missing-approval failure and timeout representation; no new enum or wait exclusion selected. |
| CF-003 | Register descriptions label `Case`/`CaseAggregate` “Immutable derivative,” while the same specifications define mutable current Case state and append-only revisions — [C3] `DAT-CNS-003`; [C4] `BAT-CNS-017`; [C5] `BR-CNS-007`; [C7] `FLOW-CNS-010`. | Incorrect immutability enforcement or duplicate/merged record structures. | AD-019: clarify provenance/current projection mapping. Preserve both mutable aggregate behavior and immutable history. |
| CF-004 | UUIDv7 generation policy is retained; derivative IDs are described as produced from “content fingerprint and pipeline version,” and local version identity is omitted — [C3] `DAT-CNS-008`; [C4] `BAT-CNS-008`; [C5] `BR-CNS-010`; [C7] `FLOW-CNS-011`. | Identity collisions, replay/reprocessing, version FKs, and hashing cannot be implemented consistently. | AD-013/AD-020/AD-074: define identity and digest roles; do not assume every hash is SHA-256 or a new local key. |
| CF-005 | Baseline roles list Analyst/Reviewer/Admin/Auditor/Service; catalog scopes additionally use `Owner`, `Member`, `approver`, and archetype “Workspace Admin” — [C1] `SF-CON-008`; [C2] `API-CNS-004`; [C5] `BR-CNS-004`; [C7] `FLOW-CNS-005`. | Ambiguous permissions and approval independence. | AD-005/AD-007/AD-072/AD-083: confirm mappings and actor predicates, not broad terminology-based grants. |
| CF-006 | Lifecycle language says tenant export/deletion; routes identify `/workspaces/{workspaceId}` — [C1] `SF-CON-010`; [C2] `API-CNS-008`; [C3] `DAT-CNS-016`; [C4] `BAT-CNS-013`; [C5] `BR-CNS-014`; [C6] `ERR-CNS-014`; [C7] `FLOW-CNS-017`. | Approval scope and lifecycle inventory may differ materially. | AD-083–AD-086: define extent, proof, holds, sharing, and completion before packaging/purge. |
| CF-007 | “Within 300 ms” is reported alongside P95 “under 300 ms” — [C5] `BR-CNS-018`; [C7] `FLOW-CNS-027`. Those sections recommend retaining a stricter earlier target pending clarification. | Equality and possibly measurement scope differ. | AD-094: confirmation remains required. This register does **not** resolve the difference by adopting the stricter recommendation. |
| CF-008 | Generic error wording says “snake-case”; concrete supported codes are uppercase — [C1] `SF-CON-005`; [C2] `API-CNS-007`; [C3] `DAT-CNS-021`; [C6] `ERR-CNS-001`. | Future naming remains ambiguous. | RES-014 resolves preservation of existing literals only; AD-039 retains future naming and undefined taxonomy. |
| CF-009 | `policy_version`, `rule_version`, Case/run/aggregate revisions, and `plan_revision` are distinct; `input_digest` is cataloged while all normalized inputs must be stored — [C3] `DAT-CNS-011`; [C5] `BR-CNS-009`; [C7] `FLOW-CNS-012`. | Version collapse or digest-only storage would lose reproducibility. | AD-017/AD-030/AD-061/AD-070: define relationships and activation; normalized-input preservation is already confirmed. |
| CF-010 | Required durable actor/correlation context coexists with an event envelope whose explicit nine fields do not include those placements — [Q2] `API-OQ-022`; [Q3] `DAT-OQ-012`; [Q7] `FLOW-OQ-015`. | Signed/canonical event and audit schemas remain incomplete. | AD-030/AD-032/AD-033: define placement without inventing an extra property or dropping required context. |
| CF-011 | Next-query ACL revocation is mandatory; queue/index/cache delivery is asynchronous — [C4] `BAT-CNS-007`; [C5] `BR-CNS-011`; [C6] `ERR-CNS-008`; [C7] `FLOW-CNS-013`. | Eventual propagation alone may violate access safety. | AD-057: select a fail-closed mechanism; no relaxation of next-query safety. |
| CF-012 | Routine retention is limited to eligible CLOSED cases; source tombstone, diagnostic purge, and decommission inventory are separately described — [C3] `DAT-CNS-016`; [C4] `BAT-CNS-012`; [C5] `BR-CNS-013`; [C7] `FLOW-CNS-016`. | One generic selector could wrongly delete or retain data. | AD-080–AD-085: define selector, lineage, sharing, hold, and backup precedence. |
| CF-013 | Soft-deleted entities “cannot be retrieved”; approved outputs preserve cited immutable versions and closure lineage — [03_data.md](03_data.md#tenant-and-referential-integrity-requirements), `DAT-RI-007`, `DAT-HIS-001`; [Q4] `BAT-OQ-010`, `BAT-OQ-014`. | Historical identity, current source access, physical retention, and purge are not interchangeable. | AD-021/AD-024/AD-082/AD-085: confirm historical source availability and physical lifecycle; do not revive deleted evidence or rewrite history. |
| CF-014 | Permanent validation/permission failures are not retried; malformed source parsing and model-output validation have bounded retries — [C4] `BAT-CNS-005`; [C6] `ERR-CNS-004`; [C7] `FLOW-CNS-024`. | A broad failure class could retry invalid authority or suppress supported parsing retries. | AD-038/AD-047/AD-048/AD-062: define stage taxonomy and exhaustion, retaining each confirmed rule. |
| CF-015 | General dependency handling allows a retryable error or persisted asynchronous identity; GET interfaces are inquiries without automatic job creation — [C2] `API-CNS-011`; [C6] `ERR-CNS-017`; [C7] `FLOW-CNS-021`. | Fallback could accidentally change read semantics or return fabricated acceptance. | AD-037/AD-039/AD-104: define fallback separately per interface. RES-010 rejects implied GET mutations. |
| CF-016 | A2A requires declared input/output schemas; the retained example omits output-schema property and uses placeholder ID strings — [C2] `API-CNS-010`; [C3] `DAT-CNS-018`; [C5] `BR-CNS-020`; [C7] `FLOW-CNS-023`. | Example cannot be an executable typed contract. | AD-013/AD-067: confirm fields/types/registry and decline results; do not infer a property name. |
| CF-017 | Domain fields exceed abbreviated DDL; `NEW` is initial business state without SQL default, and `updated_at DEFAULT now()` does not define updating — [C1] `SF-CON-006`; [C2] `API-CNS-005`; [C3] `DAT-CNS-001`, `DAT-CNS-017`; [C7] `FLOW-CNS-009`. | Schema omission/default copying could lose supported behavior. | AD-015/AD-017/AD-018: complete controlled schema without discarding fields or inventing triggers. |
| CF-018 | Primary screen names differ from illustrated aliases/highlights; business references, mixed workflow labels, coverage, and health fixtures differ from domain identities/enums/metrics — [C1] `SF-CON-001`, `SF-CON-002`, `SF-CON-011`; [C2] `API-CNS-016`; [C3] `DAT-CNS-019`; [C7] `FLOW-CNS-022`. | Wrong navigation, aggregates, IDs, or evaluation thresholds. | AD-016/AD-109–AD-114: confirm mappings/formulas independently. No mockup error becomes a navigation rule. |
| CF-019 | Case conflict example uses JSON integers, but revision is full-range BIGINT and transport is expressly unresolved — [Q2] `API-OQ-003`; [Q3] `DAT-OQ-003`; [Q6] `ERR-OQ-003`. | Browser precision and precondition comparison could fail. | AD-014: define transport; the small example values do not resolve it. |
| CF-020 | Generic Chapter 22 associations reportedly mention deletion verification for other subjects; the supplied specifications explicitly define it for verified purge — [C4] `BAT-CNS-014`; [C5] `BR-CNS-015`; [C6] `ERR-CNS-015`; [C7] `FLOW-CNS-018`. | Completion events could falsely indicate deletion. | RES-015 resolves the supplied contract’s purge purpose. AD-037/AD-084/AD-087 retain other completion contracts and any further evidence verification. |

## Consistency and Open Questions

### Complete Open-Question Crosswalk

Every question below remains outstanding to the extent mapped to an unresolved `AD` item. A resolved semantic boundary in the preceding section does not close its remaining subquestions.

#### 01_screen_functions.md — Consolidated Open Questions

| Existing IDs | Consolidated items |
|---|---|
| `OQ-001` | AD-001–AD-003 |
| `OQ-002` | AD-004, AD-010, AD-012 |
| `OQ-003` | AD-005–AD-011, AD-072, AD-090 |
| `OQ-004` | AD-109, AD-114–AD-115, AD-118–AD-120 |
| `OQ-005` | AD-039, AD-111, AD-123 |
| `OQ-006` | AD-109–AD-111 |
| `OQ-007` | AD-013–AD-017, AD-021, AD-120–AD-121 |
| `OQ-008` | AD-043–AD-045, AD-078–AD-079 |
| `OQ-009` | AD-040–AD-041 |
| `OQ-010` | AD-042, AD-069, AD-108 |
| `OQ-011` | AD-060–AD-067, AD-109–AD-110, AD-122 |
| `OQ-012` | AD-026, AD-078–AD-079 |
| `OQ-013` | AD-007, AD-072–AD-076, AD-110 |
| `OQ-014` | AD-077 |
| `OQ-015` | AD-020–AD-022, AD-046–AD-051 |
| `OQ-016` | AD-034–AD-036, AD-051–AD-052, AD-087–AD-088, AD-124–AD-127 |
| `OQ-017` | AD-053–AD-055, AD-066, AD-120 |
| `OQ-018` | AD-022–AD-024, AD-111, AD-119 |
| `OQ-019` | AD-090, AD-110 |
| `OQ-020` | AD-027, AD-065, AD-068–AD-072, AD-076, AD-080–AD-081, AD-089, AD-120 |
| `OQ-021` | AD-091–AD-092, AD-095–AD-097, AD-114 |
| `OQ-022` | AD-001, AD-052, AD-059, AD-080, AD-089, AD-103, AD-124 |
| `OQ-023` | AD-083–AD-086, AD-115 |
| `OQ-024` | AD-009–AD-011, AD-034, AD-087, AD-099–AD-100, AD-102, AD-106, AD-115, AD-117 |
| `OQ-025` | AD-116 |
| `OQ-026` | AD-111–AD-112 |
| `OQ-027` | AD-016, AD-113 |

All rows cite [Q1]. Relevant semantic resolutions: RES-001–RES-002, RES-005–RES-008, RES-011, RES-014. Outstanding consistency references: [C1] `SF-CON-001–SF-CON-011`, mapped through CF-001–CF-020 and the corresponding AD items.

#### 02_api.md — API Open-Decision Register

| Existing IDs | Consolidated items |
|---|---|
| `API-OQ-001` | AD-001–AD-007, AD-010, AD-121 |
| `API-OQ-002` | AD-008–AD-009, AD-034, AD-103 |
| `API-OQ-003` | AD-013–AD-018, AD-110, AD-121 |
| `API-OQ-004` | AD-043–AD-045, AD-078–AD-079 |
| `API-OQ-005` | AD-040–AD-042, AD-069 |
| `API-OQ-006` | AD-060–AD-065, AD-109–AD-110, AD-122 |
| `API-OQ-007` | AD-020, AD-046–AD-051 |
| `API-OQ-008` | AD-022–AD-025, AD-053–AD-058 |
| `API-OQ-009` | AD-027–AD-028, AD-059, AD-064 |
| `API-OQ-010` | AD-026, AD-072–AD-079 |
| `API-OQ-011` | AD-035–AD-036, AD-038, AD-124–AD-127 |
| `API-OQ-012` | AD-081, AD-090, AD-108, AD-110 |
| `API-OQ-013` | AD-091–AD-092, AD-095–AD-097, AD-114 |
| `API-OQ-014` | AD-065, AD-068–AD-072, AD-076, AD-080 |
| `API-OQ-015` | AD-082–AD-086 |
| `API-OQ-016` | AD-004, AD-010–AD-011, AD-087–AD-088 |
| `API-OQ-017` | AD-014, AD-031–AD-033, AD-035, AD-037–AD-039, AD-123 |
| `API-OQ-018` | AD-009, AD-035, AD-065, AD-093–AD-094, AD-104–AD-105, AD-107 |
| `API-OQ-019` | AD-023, AD-032–AD-033, AD-106 |
| `API-OQ-020` | AD-099–AD-102, AD-115 |
| `API-OQ-021` | AD-080–AD-082, AD-085–AD-086, AD-089, AD-103, AD-105 |
| `API-OQ-022` | AD-029–AD-030, AD-032, AD-100 |
| `API-OQ-023` | AD-022, AD-025, AD-062, AD-066–AD-067 |
| `API-OQ-024` | AD-117 |
| `API-OQ-025` | AD-109–AD-111, AD-113, AD-115–AD-116 |
| `API-OQ-026` | AD-059, AD-069–AD-070, AD-079–AD-080, AD-089, AD-108 |

All rows cite [Q2]. Relevant semantic resolutions: RES-005–RES-007, RES-010, RES-013–RES-015. Consistency references [C2] `API-CNS-001–API-CNS-017` remain traceable through the AD subjects and CF table; distinctions about public/MCP schemas and proposed examples remain AD-053/AD-066/AD-121/AD-122.

#### 03_data.md — Data Open-Decision Register

| Existing IDs | Consolidated items |
|---|---|
| `DAT-OQ-001` | AD-018, AD-023, AD-052, AD-058 |
| `DAT-OQ-002` | AD-019, AD-034 |
| `DAT-OQ-003` | AD-012–AD-014, AD-018, AD-033 |
| `DAT-OQ-004` | AD-004–AD-006, AD-010–AD-011, AD-070, AD-072 |
| `DAT-OQ-005` | AD-015–AD-017, AD-026, AD-040–AD-045 |
| `DAT-OQ-006` | AD-088, AD-124–AD-127 |
| `DAT-OQ-007` | AD-021, AD-046–AD-051 |
| `DAT-OQ-008` | AD-020–AD-022, AD-024, AD-050, AD-082 |
| `DAT-OQ-009` | AD-025, AD-052–AD-058 |
| `DAT-OQ-010` | AD-021, AD-023–AD-024, AD-082 |
| `DAT-OQ-011` | AD-026–AD-028, AD-059–AD-064, AD-067 |
| `DAT-OQ-012` | AD-030–AD-033, AD-035–AD-037, AD-106, AD-109 |
| `DAT-OQ-013` | AD-026, AD-068, AD-070, AD-072–AD-079 |
| `DAT-OQ-014` | AD-006, AD-081, AD-090–AD-094, AD-107–AD-108 |
| `DAT-OQ-015` | AD-023, AD-089, AD-103 |
| `DAT-OQ-016` | AD-068–AD-070, AD-080, AD-108 |
| `DAT-OQ-017` | AD-095–AD-098 |
| `DAT-OQ-018` | AD-021, AD-044, AD-080, AD-082–AD-088 |
| `DAT-OQ-019` | AD-029, AD-098–AD-102 |
| `DAT-OQ-020` | AD-034–AD-036, AD-056, AD-065, AD-088, AD-093–AD-094, AD-103–AD-106 |
| `DAT-OQ-021` | AD-015, AD-039, AD-050, AD-109–AD-113, AD-116 |
| `DAT-OQ-022` | AD-030, AD-066–AD-067, AD-116–AD-117 |

All rows cite [Q3]. Relevant semantic resolutions: RES-002, RES-005, RES-007, RES-010–RES-013. Consistency references [C3] `DAT-CNS-001–DAT-CNS-021` are covered by physical/mapping items, CF-003–CF-005, CF-009–CF-013, and CF-016–CF-019. Explicit keys and same-tenant obligations remain confirmed; their missing implementation choices are AD-018.

#### 04_batch_functions.md — Batch Open-Decision Register

| Existing IDs | Consolidated items |
|---|---|
| `BAT-OQ-001` | AD-036, AD-041, AD-076, AD-081–AD-082, AD-088, AD-092, AD-100–AD-101, AD-105 |
| `BAT-OQ-002` | AD-008, AD-034, AD-103 |
| `BAT-OQ-003` | AD-037–AD-039, AD-051, AD-061, AD-073, AD-084–AD-085, AD-087, AD-095, AD-110, AD-116 |
| `BAT-OQ-004` | AD-031–AD-033, AD-035, AD-056–AD-057, AD-079, AD-085, AD-092, AD-100–AD-101, AD-105 |
| `BAT-OQ-005` | AD-038–AD-039, AD-047–AD-048, AD-062–AD-063, AD-106 |
| `BAT-OQ-006` | AD-042–AD-043 |
| `BAT-OQ-007` | AD-035, AD-038, AD-124–AD-127 |
| `BAT-OQ-008` | AD-020, AD-022, AD-046–AD-051 |
| `BAT-OQ-009` | AD-051–AD-052, AD-056, AD-088 |
| `BAT-OQ-010` | AD-022, AD-056–AD-058, AD-082 |
| `BAT-OQ-011` | AD-030–AD-033, AD-035, AD-037, AD-106 |
| `BAT-OQ-012` | AD-028, AD-059–AD-067 |
| `BAT-OQ-013` | AD-043, AD-068, AD-070–AD-079 |
| `BAT-OQ-014` | AD-080, AD-082, AD-085, AD-089 |
| `BAT-OQ-015` | AD-081, AD-090, AD-108 |
| `BAT-OQ-016` | AD-091–AD-092 |
| `BAT-OQ-017` | AD-095–AD-098 |
| `BAT-OQ-018` | AD-087–AD-088, AD-124, AD-127 |
| `BAT-OQ-019` | AD-083–AD-086 |
| `BAT-OQ-020` | AD-032, AD-035, AD-106 |
| `BAT-OQ-021` | AD-029, AD-099–AD-102 |
| `BAT-OQ-022` | AD-117 |
| `BAT-OQ-023` | AD-035, AD-089, AD-103, AD-105 |
| `BAT-OQ-024` | AD-059, AD-069–AD-070, AD-080, AD-108 |
| `BAT-OQ-025` | AD-037, AD-039, AD-093–AD-094, AD-104, AD-106–AD-108, AD-113, AD-116 |

All rows cite [Q4]. Relevant semantic resolutions: RES-003, RES-005, RES-007, RES-011–RES-013, RES-015–RES-016. Consistency references [C4] `BAT-CNS-001–BAT-CNS-021` are retained through grouping, trigger/time, cursor/readiness, retry, lifecycle, and conflict items. Key rotation is a capability with unresolved platform/application implementation, not an adopted new job.

#### 05_business_rules.md — Open-Decision Register

| Existing IDs | Consolidated items |
|---|---|
| `BR-OQ-001` | AD-001–AD-011, AD-072, AD-083 |
| `BR-OQ-002` | AD-013–AD-015, AD-017–AD-018, AD-030–AD-033, AD-035, AD-039, AD-123 |
| `BR-OQ-003` | AD-015–AD-016, AD-042 |
| `BR-OQ-004` | AD-040 |
| `BR-OQ-005` | AD-036, AD-041 |
| `BR-OQ-006` | AD-043–AD-045, AD-078–AD-079 |
| `BR-OQ-007` | AD-020, AD-022, AD-046–AD-051 |
| `BR-OQ-008` | AD-022, AD-024–AD-025, AD-052–AD-058, AD-088 |
| `BR-OQ-009` | AD-027–AD-028, AD-059, AD-062, AD-064 |
| `BR-OQ-010` | AD-060–AD-063, AD-067 |
| `BR-OQ-011` | AD-064–AD-065, AD-091–AD-093, AD-104 |
| `BR-OQ-012` | AD-068–AD-071, AD-079–AD-080, AD-089, AD-108 |
| `BR-OQ-013` | AD-007, AD-072–AD-076, AD-079 |
| `BR-OQ-014` | AD-077–AD-078 |
| `BR-OQ-015` | AD-035–AD-036, AD-038, AD-124–AD-127 |
| `BR-OQ-016` | AD-030–AD-033, AD-035, AD-056–AD-057, AD-106 |
| `BR-OQ-017` | AD-011, AD-080–AD-082, AD-085, AD-105 |
| `BR-OQ-018` | AD-083–AD-086 |
| `BR-OQ-019` | AD-056, AD-087–AD-088 |
| `BR-OQ-020` | AD-091–AD-092 |
| `BR-OQ-021` | AD-023–AD-024, AD-074, AD-081, AD-089–AD-090, AD-108 |
| `BR-OQ-022` | AD-035, AD-093–AD-094, AD-103–AD-107 |
| `BR-OQ-023` | AD-029, AD-095–AD-102 |
| `BR-OQ-024` | AD-109–AD-123 |

All rows cite [Q5]. Relevant semantic resolutions: RES-003, RES-005–RES-008, RES-011, RES-013–RES-015. Consistency references [C5] `BR-CNS-001–BR-CNS-022` remain linked through the conflict table and applicable AD items. The absence of financial-close rules is retained under AD-091/AD-092; daily rollups do not approve invoicing or settlement.

#### 06_exception_handling.md — Open-Decision Register

| Existing IDs | Consolidated items |
|---|---|
| `ERR-OQ-001` | AD-029–AD-030, AD-037, AD-039 |
| `ERR-OQ-002` | AD-001–AD-012, AD-083 |
| `ERR-OQ-003` | AD-013–AD-015, AD-017, AD-031, AD-033, AD-039 |
| `ERR-OQ-004` | AD-018, AD-030–AD-033, AD-035, AD-079, AD-090 |
| `ERR-OQ-005` | AD-109–AD-113, AD-123 |
| `ERR-OQ-006` | AD-015, AD-040–AD-045 |
| `ERR-OQ-007` | AD-030–AD-033, AD-035, AD-106 |
| `ERR-OQ-008` | AD-038–AD-039, AD-047–AD-048, AD-062–AD-063, AD-117 |
| `ERR-OQ-009` | AD-035, AD-038, AD-065, AD-124–AD-127 |
| `ERR-OQ-010` | AD-020–AD-024, AD-046–AD-051 |
| `ERR-OQ-011` | AD-025, AD-052–AD-058, AD-082, AD-088 |
| `ERR-OQ-012` | AD-026–AD-028, AD-059–AD-063, AD-066–AD-071, AD-079, AD-108 |
| `ERR-OQ-013` | AD-064–AD-065, AD-091–AD-092, AD-104 |
| `ERR-OQ-014` | AD-007, AD-072–AD-079 |
| `ERR-OQ-015` | AD-061, AD-109–AD-111 |
| `ERR-OQ-016` | AD-034–AD-035, AD-087–AD-088 |
| `ERR-OQ-017` | AD-011, AD-080, AD-082–AD-086 |
| `ERR-OQ-018` | AD-057, AD-059, AD-069, AD-093–AD-094, AD-103–AD-108, AD-116 |
| `ERR-OQ-019` | AD-023–AD-024, AD-033, AD-074, AD-080–AD-081, AD-089–AD-090, AD-108 |
| `ERR-OQ-020` | AD-091–AD-092 |
| `ERR-OQ-021` | AD-095–AD-098 |
| `ERR-OQ-022` | AD-029, AD-099–AD-102 |
| `ERR-OQ-023` | AD-008–AD-009, AD-023, AD-103–AD-105 |
| `ERR-OQ-024` | AD-037, AD-051, AD-055, AD-081, AD-084–AD-085, AD-087–AD-088, AD-092, AD-095 |
| `ERR-OQ-025` | AD-116–AD-117 |

All rows cite [Q6]. Relevant semantic resolutions: RES-003–RES-004, RES-008–RES-015. Consistency references [C6] `ERR-CNS-001–ERR-CNS-021` are retained; `ERR-CNS-021` is resolved only as later-deliverable availability. No undefined exception is assigned a conventional HTTP, gRPC, or batch code.

#### 07_processing_flows.md — Processing Open-Decision Register

| Existing IDs | Consolidated items |
|---|---|
| `FLOW-OQ-001` | AD-001–AD-008, AD-012 |
| `FLOW-OQ-002` | AD-013, AD-015–AD-017, AD-042 |
| `FLOW-OQ-003` | AD-014–AD-015, AD-017, AD-040–AD-045, AD-078–AD-079 |
| `FLOW-OQ-004` | AD-020–AD-023, AD-033, AD-046–AD-052, AD-056 |
| `FLOW-OQ-005` | AD-036, AD-038, AD-057, AD-082, AD-124–AD-127 |
| `FLOW-OQ-006` | AD-022–AD-025, AD-052–AD-058, AD-066 |
| `FLOW-OQ-007` | AD-026, AD-060–AD-061 |
| `FLOW-OQ-008` | AD-064–AD-065 |
| `FLOW-OQ-009` | AD-035, AD-038, AD-062–AD-063, AD-076 |
| `FLOW-OQ-010` | AD-027–AD-028, AD-059, AD-066–AD-067 |
| `FLOW-OQ-011` | AD-068–AD-071, AD-074, AD-079 |
| `FLOW-OQ-012` | AD-007, AD-026, AD-033, AD-072–AD-079 |
| `FLOW-OQ-013` | AD-014, AD-061, AD-109–AD-112, AD-122–AD-123 |
| `FLOW-OQ-014` | AD-004–AD-005, AD-010–AD-011, AD-027, AD-070, AD-080 |
| `FLOW-OQ-015` | AD-029–AD-033, AD-035, AD-037–AD-039, AD-106 |
| `FLOW-OQ-016` | AD-087–AD-088 |
| `FLOW-OQ-017` | AD-024, AD-033, AD-081, AD-090, AD-107–AD-108, AD-110 |
| `FLOW-OQ-018` | AD-091–AD-092, AD-114 |
| `FLOW-OQ-019` | AD-011, AD-021, AD-080, AD-082–AD-086 |
| `FLOW-OQ-020` | AD-080–AD-082, AD-089, AD-103, AD-108 |
| `FLOW-OQ-021` | AD-095–AD-098 |
| `FLOW-OQ-022` | AD-029, AD-034, AD-036, AD-099–AD-102 |
| `FLOW-OQ-023` | AD-001, AD-008–AD-009, AD-035, AD-052, AD-059, AD-065, AD-089, AD-093–AD-094, AD-103–AD-108, AD-124 |
| `FLOW-OQ-024` | AD-109, AD-111–AD-113, AD-115–AD-123 |

All rows cite [Q7]. Relevant semantic resolutions: RES-004–RES-016. Consistency references [C7] `FLOW-CNS-001–FLOW-CNS-028` are retained. `FLOW-CNS-028` resolves availability of processing/exception documents, not the missing implementation choices.

### Reviewed Section Coverage by File

| File | Sections reviewed | Traceable requirements and register coverage | Current status |
|---|---|---|---|
| [01_screen_functions.md](01_screen_functions.md) | Scope and Users; Screen Inventory and Navigation; Functions by Screen; Integrations and Acceptance Criteria; Consistency and Open Questions; Dependencies on Later Specifications | `SF-`, `SCR-001–SCR-010`, `SCR-002-T01–T08`, `SF-AC-001–028`, `SF-CON-001–011`, `OQ-001–027`; AD-001–AD-127 through Q1 crosswalk | Confirmed screen/safety obligations retained; UI/contracts open; later-document availability and selected semantic boundaries resolved. |
| [02_api.md](02_api.md) | API Inventory and Responsibilities; Interfaces by API; Request and Response Examples; Processing and Consistency; Errors and Acceptance Criteria; Consistency and Open Questions; Carry-Forward Dependencies | `API-001–059`, authentication/IF/TXN/IDEM/CNC/POL/CLS/EVT/ERR requirements, `API-AC-001–046`, `API-CNS-001–017`, `API-OQ-001–026` | Confirmed methods/statuses/codes/boundaries retained; incomplete wire contracts and proposals remain open. |
| [03_data.md](03_data.md) | Data Inventory and Relationships; Data Field Definitions; Lifecycle and Consistency; Integration Data and Acceptance Criteria; Consistency and Open Questions; Dependencies and Required Carry-Forward | `DAT-001–063`, fields/REL/RI/STATE/TXN/CLS/RET/FMT/TIME requirements, `DAT-AC-001–040`, `DAT-CNS-001–021`, `DAT-OQ-001–022` | Authority/integrity/history obligations retained; physical design, mappings, identities, algorithms, and lifecycle details open. |
| [04_batch_functions.md](04_batch_functions.md) | Batch Inventory and Triggers; Processing by Job; Operations and Recovery; Acceptance Criteria; Consistency and Open Questions; Dependencies and Required Carry-Forward | `BAT-001–026`, CTX/TIME/CON/TXN/IDEM/RES/BKP/CLS/LOG requirements, `BAT-AC-001–057`, `BAT-CNS-001–021`, `BAT-OQ-001–025` | Logical functions/triggers retained; deployment, schedules, concurrency, receipts, retries, and completion open. |
| [05_business_rules.md](05_business_rules.md) | Rule Inventory and Scope; Decisions, Calculations, and State Transitions; Application Points and Validation Conditions; Consistency and Open Questions; Proposals and Reference Values Carried Forward | `BR-001–046`, `BR-AC-001–006`, `BR-CNS-001–022`, `BR-OQ-001–024`; existing `T-`/`TST-`/`SEC-` references retained without invented mappings | Cumulative guards retained; formulas, thresholds, actors, effective periods, and precise gates open. |
| [06_exception_handling.md](06_exception_handling.md) | Exception Inventory and Classification; Handling by Exception; Logging, Monitoring, and Operations; Failure Acceptance Criteria; Consistency and Open Questions; Dependencies and Carry-Forward | `ERR-001–060`, RES/HDL/RTY/UI/LOG/MON/OPS requirements, `ERR-AC-001–048`, `ERR-CNS-001–021`, `ERR-OQ-001–025` | Confirmed preservation/rejection/recovery retained; unknown protocol/status/severity/recipient/mechanism contracts open. |
| [07_processing_flows.md](07_processing_flows.md) | Flow Inventory and Prerequisites; Normal Processing; Branches, Failures, and Recovery; Flow Diagrams and Specification Mappings; Acceptance Criteria; Consistency and Open Questions | `FLOW-001–022` and step IDs, CTL/TXN/BRANCH/CON requirements, `FLOW-AC-001–035`, `FLOW-CNS-001–028`, `FLOW-OQ-001–024` | Confirmed ordering/branches retained; unresolved diagram arrows and analytical grouping do not adopt implementation choices. |

### Missing Evidence and Further Confirmation

The supplied specifications do not contain the evidence needed to close the following categories. Any additional material must be explicitly supplied and reviewed in a subsequent confirmation process; this register does not claim it exists or has been inspected.

| Missing evidence category | Needed confirmation material | Related items |
|---|---|---|
| Approved identity, role, and operational-access configuration | Explicit identity/session decision; claim/audience/algorithm configuration; resource permission and independent-actor matrices | AD-001–AD-012 |
| Executable API/data/protocol contracts | Approved OpenAPI/protobuf/tool/event schemas, production DDL, identity/hash/canonicalization definitions, approved examples | AD-013–AD-033, AD-046–AD-079, AD-090 |
| Business calculations and state guards | Approved priority/calendar/policy tables; review/closure/reopen transitions; counting, statistical, and accounting definitions | AD-040–AD-045, AD-048, AD-054–AD-055, AD-062–AD-076, AD-091–AD-098 |
| Operational and lifecycle configuration | Explicit platform/provider/region/key decisions; schedules, retries, fencing, backup/restore, incident controls, retention, inventories, receipts | AD-034–AD-039, AD-080–AD-089, AD-099–AD-108, AD-124–AD-127 |
| UI and notification adoption | Approved routes/layouts/control behavior, screen inventory amendments, accessibility/compatibility matrix, notification/webhook contracts | AD-109–AD-123 |
| Reported source inconsistencies and missing critical definitions | Explicit clarification of the conflicting statements and `SEC-001–SEC-012` definitions, with updated requirement links | CF-001–CF-020; AD-098 and associated items |

### Confirmation Order Implied by Dependencies

This is dependency ordering, not a schedule or assignment.

1. **Establish identity, tenancy, actors, and resource authority** — AD-001–AD-012. These constrain every protected interface, reviewer, lifecycle actor, and operational control.
2. **Define identities, versions, artifacts, schemas, and durable boundaries** — AD-013–AD-033. Hashing, publication, replay, and physical integrity depend on these contracts.
3. **Confirm provider/platform/region/key bindings and execution mechanisms** — AD-034–AD-039, AD-052, AD-059, AD-089, AD-100, AD-103–AD-108, AD-124–AD-127. No alternative is adopted merely to make another item executable.
4. **Complete domain calculations and state/approval guards** — AD-040–AD-079. Resolve run timing, classification mappings, reviewer eligibility, and publication invocation before final end-to-end fixtures.
5. **Complete lifecycle, onboarding, accounting, and evaluation contracts** — AD-080–AD-102. Approval scope, holds, identities, and versions precede verified inventory outcomes and release evidence.
6. **Bind approved contracts to presentation and notification behavior** — AD-109–AD-123. Confirmed accessibility and truthfulness can be developed earlier; proposed layouts, wire examples, and recovery controls cannot be silently adopted.
7. **Execute the retained acceptance obligations using confirmed fixtures** — corresponding `SF-AC`, `API-AC`, `DAT-AC`, `BAT-AC`, `BR-AC`, `ERR-AC`, and `FLOW-AC` IDs. A blocked fixture remains blocked rather than being completed with guessed values.

Independent decisions may be confirmed in parallel when their prerequisite contracts are already explicit. Closing one mapped subquestion does not close the remaining questions of a compound original ID.

**Final register boundary:** The seven specifications establish substantial confirmed requirements, but none supplies a blanket approval to complete its outstanding decisions independently. All unresolved items and unadopted proposals above remain on hold until explicit, consistent confirmation is supplied.

[Q1]: 01_screen_functions.md#consolidated-open-questions "01_screen_functions.md — Consolidated Open Questions"
[C1]: 01_screen_functions.md#source-consistency-and-required-clarifications "01_screen_functions.md — Source Consistency and Required Clarifications"
[Q2]: 02_api.md#api-open-decision-register "02_api.md — API Open-Decision Register"
[C2]: 02_api.md#consistency-findings-and-required-amendments "02_api.md — Consistency Findings and Required Amendments"
[Q3]: 03_data.md#data-open-decision-register "03_data.md — Data Open-Decision Register"
[C3]: 03_data.md#field-mapping-and-consistency-findings "03_data.md — Field Mapping and Consistency Findings"
[Q4]: 04_batch_functions.md#batch-open-decision-register "04_batch_functions.md — Batch Open-Decision Register"
[C4]: 04_batch_functions.md#consistency-findings-and-required-amendments "04_batch_functions.md — Consistency Findings and Required Amendments"
[Q5]: 05_business_rules.md#open-decision-register "05_business_rules.md — Open-Decision Register"
[C5]: 05_business_rules.md#consistency-findings-and-required-amendments "05_business_rules.md — Consistency Findings and Required Amendments"
[Q6]: 06_exception_handling.md#open-decision-register "06_exception_handling.md — Open-Decision Register"
[C6]: 06_exception_handling.md#consistency-findings-and-required-amendments "06_exception_handling.md — Consistency Findings and Required Amendments"
[Q7]: 07_processing_flows.md#processing-open-decision-register "07_processing_flows.md — Processing Open-Decision Register"
[C7]: 07_processing_flows.md#consistency-findings-and-required-amendments "07_processing_flows.md — Consistency Findings and Required Amendments"
