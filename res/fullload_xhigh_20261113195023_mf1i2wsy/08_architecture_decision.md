# 8. Architecture Decision Register

## How to Use This Document

This register consolidates unresolved decisions, proposals, contract gaps, assumptions, conflicts, and deferred handoffs from the supplied Markdown specifications **01–07 only**. It does not inspect or independently verify the original PDF, Map evidence, or hierarchy contexts. Quotations below are statements from the cited Markdown specifications.

`AD` identifiers organize consolidated subjects; they do not replace existing requirement identifiers. The traceability tables retain every supplied `OQ`, `CON`, and proposal identifier. Broad questions can map to several independent decisions.

| Status | Meaning | Implementation treatment |
|---|---|---|
| **TBD** | An explicitly outstanding architecture, deployment, policy, or operational selection. | Do not select a provider, technology, value, owner, or deadline independently. |
| **Needs confirmation** | A required contract is missing, incomplete, ambiguous, or inconsistent. | Hold the dependent behavior or assertion until the contract is confirmed. |
| **Unadopted proposal** | An option is explicitly proposed but not approved. | Do not implement it as a confirmed requirement. |
| **Resolved** | Explicit, consistent statements answer the narrowly stated question. | Follow that answer within its stated scope; related implementation gaps remain open. |

Repeated claims, reference configuration, illustrations, proposed mappings, and later-generation order do **not** establish approval. None of the supplied specifications appoints decision owners or deadlines for these outstanding items.

### Work That Can Proceed Without Selecting Open Options

The following constraints are consistently confirmed. They can guide implementation and verification without resolving the outstanding design choices.

| Confirmed constraint | Boundary on implementation | Markdown evidence |
|---|---|---|
| Tenant/resource authorization and non-disclosure | Navigation, Admin status, capability discovery, or an internal network cannot substitute for applicable resource authorization. | [01_screen_functions.md](01_screen_functions.md), **Users and Permissions**, `SCR-COM-002/003`; [05_business_rules.md](05_business_rules.md), **BR-003/BR-004**. |
| Untrusted content cannot grant authority | Retrieved text and model output cannot change tenancy, policy, approvals, or tool grants. | [02_api.md](02_api.md), **Internal and External Interface Inventory**, `API-COM-003`; [05_business_rules.md](05_business_rules.md), **BR-005**; [07_processing_flows.md](07_processing_flows.md), **Shared Prerequisites**, `FLOW-COM-007`. |
| Durable, replay-safe business transitions | Preserve required transaction/checkpoint boundaries; do not infer a particular locking, ledger, or broker implementation. | [07_processing_flows.md](07_processing_flows.md), **Durable Boundary Register**, `FLOW-TX-001–007`; [04_batch_functions.md](04_batch_functions.md), **Idempotency, Reruns, and Resumption**, `BAT-OPS-004`. |
| Exact review/publication binding | An accepted decision is not publication. Changed artifacts cannot use an old approval; expiry never implicitly approves. | [05_business_rules.md](05_business_rules.md), **BR-030–BR-032**; [06_exception_handling.md](06_exception_handling.md), **Review Handling**, `ERR-031/033/035`. |
| Unsafe and unsupported outputs fail closed | Unsafe attachments are not indexed; low-quality viewing does not authorize quarantined active-content rendering; unsupported evidence is not fabricated. | [02_api.md](02_api.md), **Upload and Normalization Constraints**, `API-COM-005`; [05_business_rules.md](05_business_rules.md), **BR-016/BR-018/BR-019**. |
| Truthful asynchronous status and safe errors | `202` is acceptance, not completion. Stream disconnection is not execution success or failure. Preserve known error literals and disclosure restrictions. | [06_exception_handling.md](06_exception_handling.md), **HTTP, Async, and Screen Distinctions**, `ERR-COM-003–005`; [07_processing_flows.md](07_processing_flows.md), **Shared Prerequisites**, `FLOW-COM-008`. |
| Reference-baseline choices and independently confirmed bounds | PostgreSQL authority, the 1536-dimensional index representation, DAG depth eight, sixteen tool invocations, and the case-domain 24-hour idempotency contract are confirmed within their specified contexts—not universal page sizes, quotas, or retention periods. | [03_data.md](03_data.md), **Confirmed Storage Responsibilities**, `DAT-COM-001`; **Supplementary Field Definitions**, `DAT-023-F02/026-F01`; [05_business_rules.md](05_business_rules.md), **BR-008/BR-026**. |
| Recovery and evaluation targets | Preserve the stated recovery and quality targets, but do not invent measurement methods, statistical calculations, deployed providers, or configuration precedence. | [05_business_rules.md](05_business_rules.md), **BR-047/BR-049**; [07_processing_flows.md](07_processing_flows.md), **FLOW-020/FLOW-022**. |

The unresolved tables identify what must remain on hold. Confirmed invariants above remain mandatory during experimentation, retries, degradation, migration, and recovery.

## Unresolved Items

### Platform, Providers, and Configuration Selections

| Item ID | Subject | Status | Reason for remaining unresolved | Questions to confirm | Affected scope and implementation gate | Related specifications and requirement IDs |
|---|---|---|---|---|---|---|
| AD-001 | Cloud provider and primary/recovery regions | TBD | Approved cloud/region selection remains outstanding; a “primary-approved-region” placeholder is not approval. | Which provider and primary/warm recovery regions are approved, with what residency restrictions? | Hold deployment placement and regional adapters; preserve primary-write/recovery constraints. | [03_data.md](03_data.md), **Open-Decision Register**, `OQ-DAT-025`; [07_processing_flows.md](07_processing_flows.md), **Open-Decision Register**, `OQ-FLOW-025`. |
| AD-002 | Search provider | TBD | The hybrid-search responsibility is confirmed, but its provider is not selected. | Which search service and supported capabilities are approved? | Hold provider-specific indexing/query adapters; retain derivative authority and ACL requirements. | [03_data.md](03_data.md), **Confirmed Storage Responsibilities**, `OQ-DAT-011/025`; [02_api.md](02_api.md), **Required Capabilities Without a Confirmed API Contract**, `API-GAP-011`. |
| AD-003 | Identity provider | TBD | OIDC with PKCE is confirmed; the identity provider is undefined. | Which IdP, clients, discovery endpoints, and tenant integration are approved? | Hold IdP-specific configuration, not the confirmed authentication guards. | [01_screen_functions.md](01_screen_functions.md), **Prerequisites**, `OQ-SCR-002`; [02_api.md](02_api.md), **API-047–API-050**, `API-048`, `OQ-API-034`. |
| AD-004 | Approved model providers and deployments | TBD | Specific approved deployments and regions remain unselected. | Which deployments, handling classes, regions, capabilities, evaluation approvals, and fallback relationships are authorized? | Hold actual provider routing; no unapproved fallback is permitted. | [02_api.md](02_api.md), **API-047–API-050**, `API-050`, `OQ-API-034`; [05_business_rules.md](05_business_rules.md), **BR-022**, `OQ-BR-013/030`. |
| AD-005 | Repository providers and third-party permissions | TBD | Connector providers, endpoints, authentication flows, and grants are outstanding. | Which repositories and permissions are approved for each workspace? | Hold provider adapters and credential provisioning. | [02_api.md](02_api.md), **API-047–API-050**, `API-049`, `OQ-API-019/034`; [04_batch_functions.md](04_batch_functions.md), **BAT-002**, `OQ-BAT-011`. |
| AD-006 | PostgreSQL deployment and complete physical model | Needs confirmation | PostgreSQL is confirmed, but version, service, extensions, topology, indexes, partitions, and supplementary persistence are not. | What production schema and deployment profile realize the confirmed datasets and invariants? | Hold physical migrations and tuning choices; do not create tables from component names alone. | [03_data.md](03_data.md), **Confirmed Storage Responsibilities** and **Supplementary Logical Data and Contract Inventory**, `OQ-DAT-001`, `DAT-001–036`; [07_processing_flows.md](07_processing_flows.md), **Open-Decision Register**, `OQ-FLOW-026`. |
| AD-007 | Object-storage provider and addressing layout | TBD | Private encrypted object storage is required; provider, containers, roles, names, and version/object mapping remain open. | Which provider and private addressing/serialization conventions apply? | Hold provider-specific storage layout and adapters. | [03_data.md](03_data.md), **DAT-028**, `DAT-028-F01/02`, `OQ-DAT-010/025`; [02_api.md](02_api.md), **API-036–API-044**, `API-039`, `API-GAP-011`. |
| AD-008 | Vault provider and secret-reference hierarchy | TBD | Vault-backed references are required, but provider and reference/key hierarchy are not selected. | Which vault, reference schema, access model, and key hierarchy are approved? | Hold secret-provider integration; never substitute public/raw-secret storage. | [03_data.md](03_data.md), **Confirmed Storage Responsibilities**, `OQ-DAT-017/025`; [04_batch_functions.md](04_batch_functions.md), **BAT-024**, `OQ-BAT-024`. |
| AD-009 | Broker topology and routing | TBD | At-least-once messaging is confirmed; broker, routes, partition topology, and interface realization remain undefined. | Which broker and routing contracts implement the event boundaries without cross-partition ordering assumptions? | Hold messaging deployment and provider adapters. | [02_api.md](02_api.md), **Asynchronous Event Contracts**, `API-COM-006`, `OQ-API-035`; [03_data.md](03_data.md), **Open-Decision Register**, `OQ-DAT-013`; [04_batch_functions.md](04_batch_functions.md), **BAT-010**, `OQ-BAT-005/006`. |
| AD-010 | Cache product and persistence policy | TBD | Cache responsibilities are confirmed, but product and persistence are not selected. | Which cache realizes versioned ephemeral results and mandatory authorization invalidation? | Hold cache deployment; invalidation requirements remain mandatory. | [03_data.md](03_data.md), **Confirmed Storage Responsibilities** and **DAT-027**, `OQ-DAT-012`, `DAT-027-F01/02`. |
| AD-011 | Declarative infrastructure tool | TBD | “Terraform versus Bicep remains unselected.” | Which documented infrastructure implementation is approved? | Hold tool-specific infrastructure modules. | [05_business_rules.md](05_business_rules.md), **BR-048**, `OQ-BR-029`; [04_batch_functions.md](04_batch_functions.md), **BAT-026**, `OQ-BAT-022`. |
| AD-012 | Per-tenant encryption isolation versus rotation throughput | TBD | The specifications explicitly retain this architecture trade-off. | What tenant-key isolation and rotation design satisfies the approved security and throughput requirements? | Hold key hierarchy/isolation design; do not infer bulk reencryption. | [01_screen_functions.md](01_screen_functions.md), **Screen Integration Register**, `OQ-SCR-030`; [03_data.md](03_data.md), **Open-Decision Register**, `OQ-DAT-017/025`; [04_batch_functions.md](04_batch_functions.md), **BAT-024**, `OQ-BAT-024`. |
| AD-013 | Corporate retention policy | TBD | Fictional diagnostic/audit values coexist with an explicitly outstanding corporate selection. | Which retention classes, durations, exceptions, and precedence are approved? | Hold production retention settings and destructive eligibility calculations. | [03_data.md](03_data.md), **Retention, Export, Deletion, and Recovery**, `DAT-LC-019`, `OQ-DAT-018/025`; [05_business_rules.md](05_business_rules.md), **BR-038**, `OQ-BR-023/030`. |
| AD-014 | Configuration precedence, activation, and in-flight versions | Needs confirmation | There is “no confirmed rule” that all work uses latest policy or policy at creation. | How do versions activate, overlap, roll back, and apply to queued jobs, runs, reviews, caches, existing deadlines, and retention targets? | Hold effective-policy selection; retaining actual evaluated versions can proceed. | [05_business_rules.md](05_business_rules.md), **BR-010**, `OQ-BR-004`; [07_processing_flows.md](07_processing_flows.md), **FLOW-010**, `OQ-FLOW-010`; [02_api.md](02_api.md), **Connector and Policy Interfaces**, `OQ-API-020`. |

### Identity, Contracts, and Mutation Safety

| Item ID | Subject | Status | Reason for remaining unresolved | Questions to confirm | Affected scope and implementation gate | Related specifications and requirement IDs |
|---|---|---|---|---|---|---|
| AD-015 | Token claims, algorithms, and expiry boundaries | Needs confirmation | Claim concepts are confirmed; names, values, lifetimes, equality, and clock tolerance are absent. | What exact token validation contract applies to interactive and service requests? | Hold executable identity-boundary configuration and expiry assertions. | [02_api.md](02_api.md), **Authentication and Execution Profiles**, `OQ-API-001`; [05_business_rules.md](05_business_rules.md), **BR-002**, `OQ-BR-001`; [06_exception_handling.md](06_exception_handling.md), **Open-Decision Register**, `OQ-ERR-003`. |
| AD-016 | Browser session and sign-in/out flow | Needs confirmation | BFF cookies are an option, not a selected implementation; sign-in/out and expiry navigation are undefined. | Direct tokens or BFF cookies? What CSRF, SSE authentication, session expiry, sign-out, callback, and return behavior apply? | Hold session design and navigation; no long-lived refresh token in local storage. | [01_screen_functions.md](01_screen_functions.md), **Prerequisites**, `OQ-SCR-002`, `SCR-X-001`; [02_api.md](02_api.md), **Shared Parameter Definitions**, `OQ-API-001`, `P-API-001`; [07_processing_flows.md](07_processing_flows.md), **FLOW-001**, `OQ-FLOW-001`. |
| AD-017 | Role/action/resource matrix and aliases | Needs confirmation | `Workspace Admin`, `Admin`, `Owner`, `Member`, operator, approver, and elevated role are incompletely mapped. | Which are roles or relationships, and which predicates authorize each read, mutation, field, and operational action? | Hold grants and action visibility dependent on unresolved predicates; do not infer role hierarchy. | [01_screen_functions.md](01_screen_functions.md), **Users and Permissions**, `OQ-SCR-003`; [02_api.md](02_api.md), **Public Application API Inventory**, `OQ-API-002`; [05_business_rules.md](05_business_rules.md), **BR-003**, `OQ-BR-001`. |
| AD-018 | Auditor evidence access | Needs confirmation | The Auditor journey requires redacted evidence while general case-read scope lists Analyst/Reviewer. | What authorized evidence/detail path and redaction contract serves Auditors without general case access? | Hold Auditor evidence navigation and grants. | [01_screen_functions.md](01_screen_functions.md), **Users and Permissions**, `CON-SCR-008`, `OQ-SCR-003/021`; [02_api.md](02_api.md), **Audit Interfaces**, `OQ-API-021`; [07_processing_flows.md](07_processing_flows.md), **FLOW-018**, `OQ-FLOW-022`. |
| AD-019 | Workload identities, datastore writers, and service grants | Needs confirmation | Logical processing responsibilities do not appoint exact database writers or universal `Service` permission. | Which distinct identities, audiences, IAM grants, and narrow APIs execute each function and write each dataset? | Hold workload/IAM bindings and direct datastore access. | [03_data.md](03_data.md), **Canonical Relational Entity Inventory**, `DAT-001–018`, `OQ-DAT-001`; [04_batch_functions.md](04_batch_functions.md), **Function Inventory**, `OQ-BAT-003`; [02_api.md](02_api.md), **API-036–API-044**, `OQ-API-027/028`. |
| AD-020 | Permitted mutable/consequential tools | Needs confirmation | Authorization constraints exist, but no complete mutable-tool inventory or consequence taxonomy is supplied. | Which actions are allowed, consequential, and subject to independently bound human authorization? | Hold mutable-tool capability exposure and dispatch. | [05_business_rules.md](05_business_rules.md), **BR-001/BR-027**, `OQ-BR-016`; [02_api.md](02_api.md), **API-045/API-046**, `OQ-API-028`. |
| AD-021 | Formal MCP transport and tool schema | Needs confirmation | The typed search signature supplies an upper bound, not full requiredness, lower bounds, defaults, transport, or errors. | What approved server/protocol, grants, formal schema, omission rules, and result/error contract apply? | Hold executable MCP integration; preserve read-only scope and `max_items <=10`. | [02_api.md](02_api.md), **API-045**, `API-045`, `OQ-API-028`; [03_data.md](03_data.md), **MCP and A2A Data Contracts**, `OQ-DAT-024`; [05_business_rules.md](05_business_rules.md), **BR-027**. |
| AD-022 | A2A envelope, output declaration, and decline | Needs confirmation | Prose requires declared input/output schemas; the example omits output declaration and uses placeholders. | What transport, IDs, signing/grant validation, acceptance/result/decline envelopes, deadlines, and deduplication apply? | Hold A2A dispatch/result processing; decline cannot be treated as success. | [02_api.md](02_api.md), **API-046**, `OQ-API-028`, `CON-API-012`; [03_data.md](03_data.md), **A2A Envelope**, `OQ-DAT-024`; [07_processing_flows.md](07_processing_flows.md), **FLOW-005-S05**, `OQ-FLOW-016`. |
| AD-023 | Complete REST/internal IDL and serialization | Needs confirmation | Confirmed endpoints and selected fields are not complete wire contracts. | What repository-controlled schemas, media types, types, nullability, required properties, defaults, and internal HTTP/gRPC mappings govern every interface? | Hold production request/response contracts and code generation dependent on absent IDL. | [02_api.md](02_api.md), **Shared Request, Response, and Serialization Rules**, `API-COM-004`, `OQ-API-003/027/030`; [03_data.md](03_data.md), **Field-Definition Rules**, `OQ-DAT-003/024`; [07_processing_flows.md](07_processing_flows.md), **Open-Decision Register**, `OQ-FLOW-002`. |
| AD-024 | Physical relationships and cardinalities | Needs confirmation | Logical associations do not establish all PKs, FKs, nullability, reuse limits, or cascades. | What complete integrity model preserves tenant-qualified relationships and immutable lineage? | Hold undeclared physical constraints and deletion actions; no inferred cascade. | [03_data.md](03_data.md), **Relationships and Cardinality**, `DAT-REL-001–022`, `OQ-DAT-002`; [05_business_rules.md](05_business_rules.md), **BR-004**, `OQ-BR-002/003`. |
| AD-025 | Tenant slug, plan, region codes, and root provisioning | Needs confirmation | Explicit `unique(slug)` exists, but normalization, rename/reuse, code systems, and root semantics do not. | What exact slug namespace and tenant lifecycle/code contracts apply? | Hold tenant business-key generation and root lifecycle behavior. | [03_data.md](03_data.md), **DAT-001**, `DAT-001-F01–05`, `OQ-DAT-004`, `CON-DAT-004`; [05_business_rules.md](05_business_rules.md), **BR-004**, `OQ-BR-002`. |
| AD-026 | Case UUID/business-number mapping | Needs confirmation | Illustrated business numbers have no confirmed generation, uniqueness, mask, or UUID relationship. | Is a business number persisted, and how is it generated, normalized, and mapped to canonical identity? | Hold business-number storage/routing assumptions. | [01_screen_functions.md](01_screen_functions.md), **Case Queue**, `SCR-001-F01`, `OQ-SCR-006`; [03_data.md](03_data.md), **DAT-003**, `DAT-003-F18`, `OQ-DAT-006`; [07_processing_flows.md](07_processing_flows.md), **Open-Decision Register**, `OQ-FLOW-013`. |
| AD-027 | Case forms and editable field contracts | Needs confirmation | Domain field presence does not confirm editability, control placement, lengths, or requiredness. | What create/edit fields, values, defaults, validation timing, and success destination are approved? | Hold unresolved controls and create/update payloads. | [01_screen_functions.md](01_screen_functions.md), **Shared Field and Interaction Contracts** and **Case Detail**, `OQ-SCR-004/005`, `SCR-002-F02–24`; [02_api.md](02_api.md), **Case Interfaces**, `OQ-API-007`; [03_data.md](03_data.md), **DAT-003**, `OQ-DAT-006`. |
| AD-028 | Collection/search pagination and list behavior | Needs confirmation | Cursor conventions do not define page sizes, ordering, filters, consistency, counts, or empty/final-page semantics. | What per-collection pagination, query, sorting, cursor expiry, and loading/empty contracts apply? | Hold list/query UX and wire assertions; no page sizes from screenshots or retrieval budgets. | [02_api.md](02_api.md), **Pagination Contract**, `OQ-API-006`; [01_screen_functions.md](01_screen_functions.md), **Open-Decision Register**, `OQ-SCR-011`; [07_processing_flows.md](07_processing_flows.md), **Open-Decision Register**, `OQ-FLOW-002/017`. |
| AD-029 | Request idempotency protocol and result replay | Needs confirmation | The case-domain duration is confirmed; key namespaces, fingerprints, pending replay, expired reuse, rejected outcomes, and changed-permission replay are not. | What exact identity/reservation/result-reconstruction protocol applies per mutation? | Hold ledger semantics and simultaneous/unknown-outcome assertions; preserve one accepted effect. | [02_api.md](02_api.md), **Idempotency and Concurrency**, `API-PROC-018`, `OQ-API-004`; [06_exception_handling.md](06_exception_handling.md), **Open-Decision Register**, `OQ-ERR-005`; [04_batch_functions.md](04_batch_functions.md), **Idempotency, Reruns, and Resumption**, `OQ-BAT-006`. |
| AD-030 | Revision/ETag/patch protocol | Needs confirmation | `If-Match` is required for case updates, but encoding, patch format, wildcard/missing-header behavior, and other mutation preconditions remain open. | What concurrency transport and conflict-recovery contract applies to each mutation? | Hold patch/ETag implementation and missing-header assertions. | [02_api.md](02_api.md), **Case Interfaces** and **Idempotency and Concurrency**, `OQ-API-005`, `API-004/005/017/028`; [06_exception_handling.md](06_exception_handling.md), **Open-Decision Register**, `OQ-ERR-004`. |
| AD-031 | Transaction participation and cross-store compensation | Needs confirmation | Required atomic outcomes do not choose isolation, locks, audit/result-ledger participation, blob coordination, or compensation. | What commit units, failure handling, unknown-commit recovery, and explicitly supported compensation realize each boundary? | Hold transaction mechanics and partial-operation recovery designs. | [03_data.md](03_data.md), **Transactions, Concurrent Changes, and Replay**, `OQ-DAT-014`; [04_batch_functions.md](04_batch_functions.md), **Processing and Commit Units**, `BAT-OPS-003`, `OQ-BAT-005`; [07_processing_flows.md](07_processing_flows.md), **Durable Boundary Register**, `FLOW-TX-001–007`, `OQ-FLOW-003`. |
| AD-032 | Production RLS, privileged roles, and pool-reset failure | Needs confirmation | The reference `USING` policy is not a complete production write/access design. Reset is required, but failure mechanics are absent. | What write policies, tenant-reference mechanism, privileged-role restrictions, missing-context outcomes, and reset-failure handling apply? | Hold production access DDL and connection failure recovery. | [03_data.md](03_data.md), **Confirmed Reference DDL** and **Tenant Isolation**, `DAT-COM-003`, `OQ-DAT-002/014`; [06_exception_handling.md](06_exception_handling.md), **Shared Failure Response**, `ERR-COM-002`, `OQ-ERR-015`. |

### Case, Ingestion, Evidence, and Connector Contracts

| Item ID | Subject | Status | Reason for remaining unresolved | Questions to confirm | Affected scope and implementation gate | Related specifications and requirement IDs |
|---|---|---|---|---|---|---|
| AD-033 | Classification and reasoned correction | Needs confirmation | Labels, confidences, provenance, and mandatory correction reason are confirmed; schemas, API, versions, dependencies, and races are not. | Who can correct, using which vocabulary/API/revision? How are failures, stale results, attachments, and later corrections handled? | Hold correction/classifier completion contracts. | [01_screen_functions.md](01_screen_functions.md), **Case Detail**, `OQ-SCR-007`; [02_api.md](02_api.md), **Required Capabilities**, `API-GAP-001`, `OQ-API-008`; [04_batch_functions.md](04_batch_functions.md), **BAT-001**, `OQ-BAT-010`; [07_processing_flows.md](07_processing_flows.md), **FLOW-002**, `OQ-FLOW-004`. |
| AD-034 | Priority calculation | Needs confirmation | “No impact × urgency matrix, weighted sum, multiplication, or lookup table is supplied.” | What vocabularies, formula, ties, rounding, overrides, missing values, and recalculation rules apply? | Hold calculated priority and prioritization ordering assumptions. | [05_business_rules.md](05_business_rules.md), **BR-012**, `OQ-BR-006`; [01_screen_functions.md](01_screen_functions.md), **Case Detail**, `OQ-SCR-008`; [07_processing_flows.md](07_processing_flows.md), **Open-Decision Register**, `OQ-FLOW-005`. |
| AD-035 | Contractual SLA/calendar calculation | Needs confirmation | Timezone/business-calendar use is confirmed; durations, start/pause, DST, holidays, equality, and changed-deadline rules are absent. | What complete deadline calculation and recalculation contract applies? | Hold contractual deadline computation; advisory predictions cannot change it. | [05_business_rules.md](05_business_rules.md), **BR-013**, `OQ-BR-007`; [03_data.md](03_data.md), **DAT-002** and **External Formats, Encoding, and Time**, `DAT-002-F10`, `DAT-INT-006`, `OQ-DAT-005/024`. |
| AD-036 | Case transitions and cross-aggregate synchronization | Needs confirmation | States and selected transitions are confirmed, not every trigger/role or classifier/review/publication-to-case mapping. | Which guarded actions transition each state, and how do case/run/review/artifact states synchronize? | Hold automatic transition assumptions and direct-status editing. | [05_business_rules.md](05_business_rules.md), **BR-014**, `OQ-BR-008`; [07_processing_flows.md](07_processing_flows.md), **State and Completion Interpretation**, `OQ-FLOW-013`; [01_screen_functions.md](01_screen_functions.md), **Navigation and Status Requirements**, `OQ-SCR-006`. |
| AD-037 | Closure, reopening, and snapshot lineage | Needs confirmation | Complete transition into `CLOSED`, roles, approved-answer absence, repeat-close, and reopen contract are missing. | What predecessor/target states, API/preconditions, snapshot identity, history reconstruction, and navigation apply? | Hold close/reopen behavior beyond confirmed lineage preservation. | [02_api.md](02_api.md), **Case Interfaces**, `API-005`, `API-GAP-005`, `OQ-API-007`; [03_data.md](03_data.md), **DAT-004**, `OQ-DAT-007`; [05_business_rules.md](05_business_rules.md), **BR-015**. |
| AD-038 | Source/document/version/chunk identity | Needs confirmation | UUIDv7 baseline and fingerprint-plus-pipeline derivative identity are not formally mapped; version PK and uniqueness are incomplete. | What source namespaces, parser/pipeline versions, identity derivation, side-by-side uniqueness, and delete/recreate semantics apply? | Hold immutable identity and source-reprocessing schema choices. | [03_data.md](03_data.md), **DAT-005–DAT-007**, `OQ-DAT-008`, `CON-DAT-003`; [04_batch_functions.md](04_batch_functions.md), **BAT-003**, `OQ-BAT-012`; [07_processing_flows.md](07_processing_flows.md), **Open-Decision Register**, `OQ-FLOW-007`. |
| AD-039 | Upload transport and admission boundaries | Needs confirmation | The configurable 25 MB cap does not define byte units/equality, request aggregate limits, exact allowlist, or decompression threshold. | What file transport, signatures/extensions, size/count limits, parser bounds, corrupt/encrypted input outcomes, and safe codes apply? | Hold executable upload boundaries and associated error assertions. | [02_api.md](02_api.md), **Upload and Normalization Constraints**, `OQ-API-009`; [03_data.md](03_data.md), **Input and Output File Inventory**, `DAT-FILE-001`, `OQ-DAT-010`; [06_exception_handling.md](06_exception_handling.md), **Open-Decision Register**, `OQ-ERR-010`. |
| AD-040 | OCR opt-in configuration | Needs confirmation | Opt-in and provenance are confirmed; default, scope, carrier, and initiation path are not. | Where is opt-in configured, for which inputs, and how is OCR provenance/version represented? | Hold OCR activation controls; beyond-English OCR remains deferred. | [01_screen_functions.md](01_screen_functions.md), **Case Detail**, `SCR-002-F19`, `OQ-SCR-009`; [03_data.md](03_data.md), **Supplementary Field Definitions**, `DAT-022-F03`, `OQ-DAT-010`. |
| AD-041 | Normalized artifact/layout serialization and text encoding | Needs confirmation | Claims/layout preservation is confirmed, but derivative files, roles, schemas, Unicode/line endings, and normalization details are absent. | What exact text/layout/metadata formats and parsing/normalization rules apply? | Hold artifact serialization and renderer/parser assumptions. | [03_data.md](03_data.md), **Input and Output File Inventory**, `DAT-FILE-002`; **External Formats, Encoding, and Time**, `DAT-INT-001/002`, `OQ-DAT-010/024`; [04_batch_functions.md](04_batch_functions.md), **BAT-003**. |
| AD-042 | Extraction quality and autonomous-use eligibility | Needs confirmation | Flags are named, but formulas, denominators, thresholds, missing-value rules, `READY`, and reviewed/manual use are not. | What measurable quality gates and eligibility outcomes apply? | Hold quality classification/readiness/autonomous-use decisions, not the low-quality exclusion requirement. | [05_business_rules.md](05_business_rules.md), **BR-018**, `OQ-BR-010`; [03_data.md](03_data.md), **Document State** and **DAT-022**, `DAT-CODE-003`, `DAT-022-F04`, `OQ-DAT-010/011`; [06_exception_handling.md](06_exception_handling.md), `ERR-024`, **Open-Decision Register**, `OQ-ERR-010`. |
| AD-043 | Quarantine storage, inspection, release, and remediation | Needs confirmation | Low-quality viewing does not establish a safe quarantine viewer or automatic release/reparse procedure. | How are unsafe records retained, inspected safely, remediated, or released, and by whom under confirmed grants? | Hold quarantine UI/release mechanisms; no unsafe indexing. | [02_api.md](02_api.md), **Upload and Normalization Constraints**, `API-COM-005`; [06_exception_handling.md](06_exception_handling.md), **Integration, Ingestion, and Evidence Handling**, `ERR-020/023`, `OQ-ERR-010`; [01_screen_functions.md](01_screen_functions.md), **Evidence Viewer**, `OQ-SCR-009`. |
| AD-044 | Citation/evidence IDs and anchor geometry | Needs confirmation | `Citation`, ID aliases, page numbering, ranges, bounding boxes, and non-PDF anchors are undefined. | What formal identity/anchor contract supports exact-version verification and highlighting? | Hold source-anchor wire schema and highlight implementation. | [03_data.md](03_data.md), **DAT-007/DAT-010**, `OQ-DAT-009`, `DAT-COM-004`; [02_api.md](02_api.md), **Evidence and Citation Content**, `API-EVID-F01–13`, `OQ-API-010/028`; [01_screen_functions.md](01_screen_functions.md), **Evidence Viewer**, `OQ-SCR-010`. |
| AD-045 | Browser source access and signed-URL lifecycle | Needs confirmation | Short-lived controlled URLs are required; browser endpoint, TTL, reissue, post-issuance revocation, and failures are absent. | How is current permission enforced during issuance and use, including source unavailability and return navigation? | Hold browser document retrieval/download and URL lifecycle. | [02_api.md](02_api.md), **Required Capabilities**, `API-GAP-003`; **Ingestion, Search, and Evidence Interfaces**, `OQ-API-010`; [06_exception_handling.md](06_exception_handling.md), **Evidence Handling**, `ERR-025/039`, `OQ-ERR-011/014`. |
| AD-046 | Retrieval ranking, budgets, sufficiency, and human routing | Needs confirmation | Algorithm names and bounded retrieval do not establish equations, ties, approved parameters, confidence thresholds, or clarification outcomes. | What query/ranking/diversity/token/sufficiency and conflict-handling rules apply? | Hold numeric retrieval policy and clarification/human continuation. | [05_business_rules.md](05_business_rules.md), **BR-019**, `OQ-BR-011`; [02_api.md](02_api.md), **Search Interfaces**, `OQ-API-011`; [07_processing_flows.md](07_processing_flows.md), **FLOW-004**, `OQ-FLOW-007`. |
| AD-047 | Standalone search evidence persistence and digest scope | Needs confirmation | Search need not allocate a run, but `evidence_sets` includes `run_id`; item/set ACL digests are not mapped. | Are standalone results persisted, with what associations, ordering, reuse, and per-item/set validation data? | Hold evidence-set storage/cardinality choices; do not create runs for every search. | [03_data.md](03_data.md), **Relationships and Cardinality**, `DAT-REL-013/014`; **DAT-010**, `OQ-DAT-009/011`, `CON-DAT-009/010`; [02_api.md](02_api.md), **Reads, Writes, and Boundaries**, `API-PROC-004`. |
| AD-048 | Search-row physical representation and analyzers | Needs confirmation | Required row content and dimension are confirmed; vector numeric type, analyzers, language codes, and provider IDL are not. | What provider schema and embedding compatibility/adapter contract apply? | Hold provider-specific index schema and embedding batches. | [03_data.md](03_data.md), **Supplementary Field Definitions**, `DAT-023-F01/02`, `OQ-DAT-011`; [04_batch_functions.md](04_batch_functions.md), **BAT-004**, `OQ-BAT-013`. |
| AD-049 | Index commit, rebuild, coverage, and retirement gates | Needs confirmation | Checked atomic alias switching is required, but completeness/recall formulas, empty corpus, catch-up, partial commit, and retirement are undefined. | What commit/readiness/check/rollback contract handles concurrent updates and generations? | Hold readiness thresholds, alias replacement, and generation cleanup. | [04_batch_functions.md](04_batch_functions.md), **BAT-004/BAT-005**, `OQ-BAT-013`; [05_business_rules.md](05_business_rules.md), **BR-020**, `OQ-BR-011`; [06_exception_handling.md](06_exception_handling.md), `ERR-038`, **Open-Decision Register**, `OQ-ERR-014`. |
| AD-050 | ACL detection, propagation, and cache atomics | Needs confirmation | Revocation before next retrieval is mandatory; detection, group mapping, digest/key encoding, TTL, affected-key discovery, and in-flight races are unresolved. | What protocol prevents stale unauthorized results during retrieval, caching, alias changes, and publication? | Hold propagation/invalidation implementation; ordinary TTL cannot justify leakage. | [03_data.md](03_data.md), **DAT-027** and **Index, Cache, and Source Consistency**, `OQ-DAT-012/019`; [05_business_rules.md](05_business_rules.md), **BR-021**, `OQ-BR-012`; [07_processing_flows.md](07_processing_flows.md), **FLOW-011**, `OQ-FLOW-015`. |
| AD-051 | Connector administration and credential recovery APIs | Needs confirmation | Sync/history exists; list/read/configure/delete/authenticate/reauthenticate/revoke contracts are incomplete. | What schemas, rights, statuses, and queued-job relaunch/resumption rules apply? | Hold connector administration controls and credential recovery. | [02_api.md](02_api.md), **Required Capabilities**, `API-GAP-007`, `OQ-API-019`; [01_screen_functions.md](01_screen_functions.md), **Connector Health**, `OQ-SCR-019`; [06_exception_handling.md](06_exception_handling.md), `ERR-003`, **Open-Decision Register**, `OQ-ERR-009`. |
| AD-052 | Safe lower-trust connector restrictions | Needs confirmation | Unsupported capability warnings coexist with mandatory ACL/revocation/delete invariants. | Which modes are safe when each capability is missing, and which activities must be blocked? | Hold unsupported-capability operation until restrictions are confirmed. | [05_business_rules.md](05_business_rules.md), **BR-034**, `OQ-BR-021`; [04_batch_functions.md](04_batch_functions.md), **BAT-002/BAT-006**, `OQ-BAT-011/013`; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-011`. |
| AD-053 | Cursor/history ownership and partial synchronization | Needs confirmation | Per-run ledger requirements exceed the selected connector-keyed cursor fields; ingestion durability is not confirmed as indexed `READY`. | What cursor namespace/order/expiry, run history, fencing, batch boundary, durable exception, partial/no-change result apply? | Hold cursor advancement mechanics and sync completion assertions. | [03_data.md](03_data.md), **DAT-015**, `OQ-DAT-019`, `CON-DAT-011`; [04_batch_functions.md](04_batch_functions.md), **BAT-002**, `OQ-BAT-011`; [07_processing_flows.md](07_processing_flows.md), **FLOW-009-S05**, `OQ-FLOW-014`. |

### AI Execution, Review, Publication, and Messaging

| Item ID | Subject | Status | Reason for remaining unresolved | Questions to confirm | Affected scope and implementation gate | Related specifications and requirement IDs |
|---|---|---|---|---|---|---|
| AD-054 | Canonical run creation and revision/rework controls | Needs confirmation | Both run-create paths are retained; case revision binding and cancel/retry/resume APIs are incomplete. | Canonical path, alternate semantics, request/result binding, and new revision versus resume? | Hold browser launch binding and rework/control APIs. | [02_api.md](02_api.md), **Run Creation, State, Steps, and SSE**, `API-011/012`, `OQ-API-012`; [01_screen_functions.md](01_screen_functions.md), **Case Detail/Run Timeline**, `OQ-SCR-012`; [07_processing_flows.md](07_processing_flows.md), **FLOW-005/FLOW-007**, `OQ-FLOW-008`. |
| AD-055 | DAG, call-budget, and stop accounting | Needs confirmation | Maxima are confirmed, but depth convention, retries/failed dispatch accounting, invalid-plan repetition, dependency schema, and failure mapping are not. | What exact plan acceptance/accounting and stop rules apply? | Hold boundary accounting and retry/resume assertions; maxima cannot be exceeded. | [05_business_rules.md](05_business_rules.md), **BR-026**, `OQ-BR-015`; [03_data.md](03_data.md), **DAT-008–DAT-009**, `OQ-DAT-015`; [06_exception_handling.md](06_exception_handling.md), `ERR-028`, **Open-Decision Register**, `OQ-ERR-008`. |
| AD-056 | Review waiting, missing approval, and recoverable timeout | Needs confirmation | Valid `AWAITING_REVIEW`, missing-approval termination, and terminal-or-recoverable timeout coexist without one consistent state/accounting contract. | What distinguishes valid waiting from failure? Does execution time pause, and how is recoverability represented? | Hold timeout/wait-state implementation; do not apply 180 seconds to reviewer expiry. | [02_api.md](02_api.md), **Run Interfaces**, `OQ-API-013`, `CON-API-002`; [05_business_rules.md](05_business_rules.md), **BR-026**, `OQ-BR-015`; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-002`. |
| AD-057 | Admission thresholds and capacity reservations | Needs confirmation | Token, queue-age, and provider-capacity conditions exist, but values, units, equality, unknown values, fairness, and simultaneous reservations do not. | What atomic admission contract and approved thresholds apply? | Hold actual admission configuration; preserve `429`/`Retry-After` and saved-case access. | [05_business_rules.md](05_business_rules.md), **BR-024**, `OQ-BR-014`; [02_api.md](02_api.md), **Runtime, Admission, Timeouts, and Retries**, `API-PROC-020`; [07_processing_flows.md](07_processing_flows.md), **Open-Decision Register**, `OQ-FLOW-009`. |
| AD-058 | Token reservation, usage, exhaustion, and refunds | Needs confirmation | Current-run terminal exhaustion is confirmed; tokenizer/count authority, release/refund, retry/failed billing, and quota windows are absent. | What accounting grain and reservation/actual/release reconciliation apply? | Hold quota ledger arithmetic and financial correction; no automatic class/model switch. | [03_data.md](03_data.md), **DAT-016**, `OQ-DAT-020`; [05_business_rules.md](05_business_rules.md), **BR-025**, `OQ-BR-014`; [06_exception_handling.md](06_exception_handling.md), **Open-Decision Register**, `OQ-ERR-023`. |
| AD-059 | Prompt/output version contracts and injection handling | Needs confirmation | Fixed/delimited context and invalid-output rejection are confirmed; schema, signing, detection/stripping, indicator continuation, parse retry, and attempt persistence are not. | What exact prompt/output/injection protocol applies, including absent versus invalid citations? | Hold model payload and detection-specific continuation; authority escalation remains blocked. | [02_api.md](02_api.md), **API-036**, `OQ-API-027`; [03_data.md](03_data.md), **DAT-024**, `OQ-DAT-015/024`; [06_exception_handling.md](06_exception_handling.md), `ERR-005/026`, `CON-ERR-004/005`, `OQ-ERR-008/012`. |
| AD-060 | Deterministic policy decision matrix | Needs confirmation | Inputs/outcomes are named, but categories, high-risk/high-impact definitions, thresholds, missing inputs, and combination priority are not supplied. | What versioned matrix maps normalized inputs to results without inventing a universal outcome priority? | Hold binding policy calculations and review-trigger thresholds. | [05_business_rules.md](05_business_rules.md), **BR-028** and **Confirmed Priorities**, `OQ-BR-017`; [03_data.md](03_data.md), **DAT-017**, `OQ-DAT-021`; [07_processing_flows.md](07_processing_flows.md), **Open-Decision Register**, `OQ-FLOW-010`. |
| AD-061 | Reviewer pools, minimum roles, assignment, and authorship | Needs confirmation | Selection and separation constraints are confirmed, but organizational predicates, pool selection, reassignment rights, and author identity are incomplete. | Who is eligible and independent for each task, using which assignment history? | Hold reviewer routing/grants and authorship-based enforcement details. | [05_business_rules.md](05_business_rules.md), **BR-029**, `OQ-BR-001/019`; [02_api.md](02_api.md), **Review Interfaces**, `OQ-API-016`; [03_data.md](03_data.md), **DAT-011**, `OQ-DAT-016`. |
| AD-062 | Global self-approval scope | Needs confirmation | Explicit high-risk prohibition and broader “no self approval”/false example are not scoped consistently. | Is the prohibition global, and what explicitly approved scope or exceptions exist without weakening high-risk independence? | Hold broader self-approval policy; high-risk self-approval remains prohibited. | [01_screen_functions.md](01_screen_functions.md), `CON-SCR-009`; [02_api.md](02_api.md), `CON-API-005`; [05_business_rules.md](05_business_rules.md), **BR-029**, `OQ-BR-019`. |
| AD-063 | Task detail, `approvalId`, and review-open event | Needs confirmation | Task detail is missing; `UserReviewOpened` has no confirmed trigger/schema and is absent from the partial catalog. | What resource is addressed, how is exact context retrieved, and what explicit action records opening? | Hold task-opening API/state mutation; do not make all GETs mutate review state. | [02_api.md](02_api.md), **Required Capabilities**, `API-GAP-004`, `OQ-API-015/035`; [01_screen_functions.md](01_screen_functions.md), **Review Inbox**, `SCR-005-A02`, `OQ-SCR-021`; [07_processing_flows.md](07_processing_flows.md), **FLOW-006-S02**, `OQ-FLOW-011`. |
| AD-064 | Review decision fields and immutable binding | Needs confirmation | Capture concepts are confirmed, not decision request literals, rationale nonblank/length, annotations, hash carrier, duplicate decisions, or complete storage. | What exact task/candidate-bound request, record, validation, and result apply? | Hold form and decision payload schema; no click-count/checkbox gate by inference. | [02_api.md](02_api.md), **Review Interfaces**, `API-017`, `OQ-API-015`; [03_data.md](03_data.md), **DAT-012**, `OQ-DAT-016`; [05_business_rules.md](05_business_rules.md), **BR-030**, `OQ-BR-018`. |
| AD-065 | Review expiry, late decisions, and multiple reviewers | Needs confirmation | No-implicit-approval is confirmed; SLA units/start/clock/equality, race ordering, escalation, and sufficiency/conflicts are absent. | What complete expiry/reassignment and multi-reviewer protocol applies? | Hold timer policy, late responses, and competing decision resolution. | [04_batch_functions.md](04_batch_functions.md), **BAT-009**, `OQ-BAT-015`; [05_business_rules.md](05_business_rules.md), **BR-031**, `OQ-BR-019`; [06_exception_handling.md](06_exception_handling.md), `ERR-033`, `OQ-ERR-012`. |
| AD-066 | Publication trigger, automatic allow, and approval lifetime | Needs confirmation | Atomic exact-content gating is confirmed; public control, `AUTO_ALLOW` trigger, validity/revocation, current policy scope, and failure projection are not. | How does each permissible result reach publication, with what current checks and sufficient decision evidence? | Hold trigger/state/API mechanics; no unconditional `INTERNAL` publication. | [02_api.md](02_api.md), **Review Interfaces**, `API-GAP-006`, `OQ-API-017`; [04_batch_functions.md](04_batch_functions.md), **BAT-008**, `OQ-BAT-015`; [05_business_rules.md](05_business_rules.md), **BR-032**, `OQ-BR-020`. |
| AD-067 | Override and denied/rejected rework protocol | Needs confirmation | Elevated role, secondary reviewer, audited reason, and new-run rework are confirmed; eligibility, API, independence, linkage, and outcome are not. | What can be overridden, through which binding protocol, and how is a new candidate linked without rewriting denial? | Hold override/rework controls beyond confirmed constraints. | [01_screen_functions.md](01_screen_functions.md), **Review Inbox**, `OQ-SCR-017`; [02_api.md](02_api.md), `API-GAP-005/006`, `OQ-API-018`; [05_business_rules.md](05_business_rules.md), **BR-033**, `OQ-BR-020`. |
| AD-068 | Complete event schemas, signing, and trigger inventory | Needs confirmation | Exact common names exist, but full payloads/producers/signatures, actor/correlation carriers, additional events, and SSE/webhook mappings do not. | What formal versioned event contracts and actual write/detector/promotion triggers apply? | Hold missing event schemas and trigger associations; reads are not writes by inference. | [02_api.md](02_api.md), **Asynchronous Event Contracts**, `API-COM-006`, `OQ-API-035`; [03_data.md](03_data.md), **Event Envelope and Payload Data**, `DAT-EVT-F01–09`, `OQ-DAT-013`; [07_processing_flows.md](07_processing_flows.md), **FLOW-012**, `OQ-FLOW-016`. |
| AD-069 | Outbox/consumer ledger and acknowledgment protocol | Needs confirmation | Durable publication/deduplication does not define claims, ledger keys, acknowledgment atomics, stale/future revisions, poison routing, retention, or migration. | How are eligible, duplicate, stale, invalid, and migrated deliveries handled atomically? | Hold publisher/consumer mechanics and ledger cleanup. | [04_batch_functions.md](04_batch_functions.md), **BAT-010**, `OQ-BAT-005/006`; [06_exception_handling.md](06_exception_handling.md), `ERR-013/014`, **Open-Decision Register**, `OQ-ERR-006`; [03_data.md](03_data.md), **DAT-014/DAT-026**, `OQ-DAT-013`. |

### Background Execution, Lifecycle, and Protected Operations

| Item ID | Subject | Status | Reason for remaining unresolved | Questions to confirm | Affected scope and implementation gate | Related specifications and requirement IDs |
|---|---|---|---|---|---|---|
| AD-070 | Executable packaging and trigger realization | Needs confirmation | Assigned `BAT` IDs “do not establish executable names, deployment units, queue names, or scheduler entries.” | Which functions share workers, timers, managed facilities, or deployments, and what exact triggers apply? | Hold runtime packaging and inferred read-triggered jobs. | [04_batch_functions.md](04_batch_functions.md), **Specification Basis and Status** and **Function Inventory**, `BAT-COM-001`, `BAT-001–026`; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-019`, `OQ-FLOW-026`. |
| AD-071 | Schedules, clocks, catch-up, and maintenance windows | Needs confirmation | Daily/timer/policy behavior does not supply cron, timezone, DST, missed-run, or catch-up rules. | What per-function execution calendar, reporting boundary, and missed-trigger handling apply? | Hold scheduler entries and temporal batch assertions. | [04_batch_functions.md](04_batch_functions.md), **Trigger and Time Conventions**, `BAT-COM-002`, `OQ-BAT-001`; [05_business_rules.md](05_business_rules.md), **BR-043**, `OQ-BR-026`; [07_processing_flows.md](07_processing_flows.md), `OQ-FLOW-021/023`. |
| AD-072 | Parallelism, worker claims, heartbeat, and fencing | Needs confirmation | Outcome safety is confirmed; leases, heartbeat intervals, ownership transfer, allowed parallel DAG nodes, and region-worker fencing are not. | What concurrency and lost-worker protocol prevents stale/duplicate effects? | Hold worker-loss recovery and mutual exclusion mechanics. | [04_batch_functions.md](04_batch_functions.md), **Concurrent Launches and Mutual Exclusion**, `BAT-OPS-002`, `OQ-BAT-004/007`; [06_exception_handling.md](06_exception_handling.md), `ERR-041`, `OQ-ERR-015`; [07_processing_flows.md](07_processing_flows.md), **Parallel Processing**, `FLOW-COM-009`, `OQ-FLOW-018`. |
| AD-073 | Dependency retry, circuit, timeout, and uncertain outcome | Needs confirmation | Bounded retry principles do not supply counts, delays, circuit settings, retry taxonomy, `Retry-After` syntax, or uncertain external-write handling. | What per-dependency policies and exhausted dispositions apply? | Hold numeric resilience policies; permanent validation/permission failures remain non-transient. | [04_batch_functions.md](04_batch_functions.md), **Retries, Timeouts, and Worker Loss**, `BAT-OPS-005`, `OQ-BAT-007`; [06_exception_handling.md](06_exception_handling.md), **Retry Boundaries**, `ERR-COM-007`, `OQ-ERR-007`; [05_business_rules.md](05_business_rules.md), **BR-036**. |
| AD-074 | Controlled replay admission and migration | Needs confirmation | Reason, dry run, scope limit, identity preservation, and provenance are confirmed; units, approval, limits, status, and partial handling are absent. | What protected replay request/result, validation, migration approval, and deadline apply? | Hold executable replay/remediation controls. | [02_api.md](02_api.md), **Internal HTTP Interfaces**, `API-038`, `OQ-API-027`; [04_batch_functions.md](04_batch_functions.md), **BAT-012**, `OQ-BAT-007`; [06_exception_handling.md](06_exception_handling.md), **ERR-OPS-006**, `OQ-ERR-006/007`. |
| AD-075 | Empty/no-input and partial-result conventions | Needs confirmation | Empty fixtures are required, but there is no universal “zero rows means success,” passing score, receipt, or successor rule. | What per-job/flow status, counts, receipts, side effects, and downstream dispatch apply to empty, all-held, and partial selections? | Hold executable no-input assertions across all applicable functions. | [04_batch_functions.md](04_batch_functions.md), **No-Input and Empty-Selection Coverage**, `OQ-BAT-009`; [06_exception_handling.md](06_exception_handling.md), **Empty, Partial, and Boundary Tests**; [07_processing_flows.md](07_processing_flows.md), **Unresolved Boundary Assertions**, `OQ-FLOW-018–024`. |
| AD-076 | Reconciliation and incident-control interfaces | Needs confirmation | Runbook steps exist, but detection cadence, mismatch bounds, shard identity, pause/resume, denied probes, receipts, and reenable authority are incomplete. | What protected operational controls and verification contracts realize delayed-index and ACL recovery? | Hold commands/console exposure and recovery completion. | [04_batch_functions.md](04_batch_functions.md), **BAT-011** and **BAT-OPS-009/010**, `OQ-BAT-013`; [06_exception_handling.md](06_exception_handling.md), **ERR-OPS-003/004**, `OQ-ERR-014/024`; [07_processing_flows.md](07_processing_flows.md), **FLOW-013**. |
| AD-077 | Independent exit-approval protocol | Needs confirmation | Two-person checks are confirmed, but bindings, initiator participation, expiry/revocation, scope changes, and execution rechecks are missing. | How are two independent authorizations verified for the exact export/delete inventory? | Hold exit approval mechanics; two client-selected IDs are insufficient. | [05_business_rules.md](05_business_rules.md), **BR-039**, `OQ-BR-024`; [02_api.md](02_api.md), **Export and Deletion Interfaces**, `OQ-API-024`; [07_processing_flows.md](07_processing_flows.md), **FLOW-015/FLOW-016**, `OQ-FLOW-020`. |
| AD-078 | Export snapshot, package, status, and download | Needs confirmation | Content/exclusions are confirmed; snapshot, draft/held treatment, raw binaries, format, checksum, lifetime, limits, and partial delivery are not. | What authorized package and recipient/status/download contract applies? | Hold package implementation and export completion UI; no export-then-delete chain. | [03_data.md](03_data.md), **Input and Output File Inventory**, `DAT-FILE-004`, `OQ-DAT-023`; [04_batch_functions.md](04_batch_functions.md), **BAT-020**, `OQ-BAT-021`; [02_api.md](02_api.md), `API-GAP-009`. |
| AD-079 | Deletion inventory, receipts, held results, and historical survival | Needs confirmation | Tombstones/removal/receipts are confirmed; relational/root mapping, shared sources, history/actors/audit/backups, partial verification, and receipt survival are not. | What is removed or retained, and when may `TenantDeletionVerified` close an all-held/partial operation? | Hold destructive inventory and completion semantics. | [03_data.md](03_data.md), **Retention, Export, Deletion, and Recovery**, `DAT-LC-021/022/024`, `OQ-DAT-018`; [04_batch_functions.md](04_batch_functions.md), **BAT-021**, `OQ-BAT-016`; [07_processing_flows.md](07_processing_flows.md), **FLOW-016**, `OQ-FLOW-020/021`. |
| AD-080 | Hold creation, scope, read/release, and races | Needs confirmation | Hold protection exists, but fields, rights, types, priorities, release APIs, and arrival-during-destruction rules are absent. | What complete hold lifecycle and destructive-operation fence applies? | Hold hold-administration contracts and purge race handling. | [02_api.md](02_api.md), **Principal, Membership, and Holds**, `API-029`, `API-GAP-008`, `OQ-API-025`; [03_data.md](03_data.md), **DAT-029**, `DAT-029-F01`, `OQ-DAT-018`; [07_processing_flows.md](07_processing_flows.md), **FLOW-017**. |
| AD-081 | Retention eligibility and historical evidence scope | Needs confirmation | Eligible closed-case processing is confirmed, but age clock/equality, related inventory, held history, diagnostic/audit export coordination, and deletion relationship are incomplete. | What production eligibility and survival contract applies to each record class? | Hold retention selection and purge; do not impose closed-case eligibility on all workspace deletion targets by inference. | [04_batch_functions.md](04_batch_functions.md), **BAT-013/BAT-014**, `OQ-BAT-016`; [05_business_rules.md](05_business_rules.md), **BR-038**, `OQ-BR-023`; [06_exception_handling.md](06_exception_handling.md), `ERR-044`, `OQ-ERR-018`. |
| AD-082 | Provisioning launch, completeness, and compensation | Needs confirmation | One idempotent workflow is required; entry/status API, actor, resource order, completeness, changed-config rerun, and partial-resource recovery are undefined. | What provisioning contract establishes and verifies policy, keys, roles, quotas, and connector stubs? | Hold provisioning interfaces and compensation; incomplete state must block sync. | [02_api.md](02_api.md), `API-GAP-008`, **Open-Decision Register**, `OQ-API-025`; [04_batch_functions.md](04_batch_functions.md), **BAT-018**, `OQ-BAT-020`; [07_processing_flows.md](07_processing_flows.md), **FLOW-014**, `OQ-FLOW-019`. |
| AD-083 | Historical backfill windows and incremental overlap | Needs confirmation | Stable IDs, bounded windows, receipts, and coverage readiness are confirmed; selection/order/bounds, concurrent source changes, overlap, and checkpoints are not. | What onboarding window/batch/receipt and catch-up contract applies? | Hold historical backfill implementation and readiness calculation. | [04_batch_functions.md](04_batch_functions.md), **BAT-019**, `OQ-BAT-020`; [03_data.md](03_data.md), **DAT-029**, `DAT-029-F06`, `OQ-DAT-019/022`; [05_business_rules.md](05_business_rules.md), **BR-042**, `OQ-BR-025`. |
| AD-084 | Audit hash chain and independent export | Needs confirmation | Tamper-evident export is required; order, batch boundaries, algorithms, files, destination grants, verification, cadence, and outage recovery are missing. | What integrity/export protocol preserves append-only evidence without rewriting history? | Hold hash/export implementation and verified-export claims. | [04_batch_functions.md](04_batch_functions.md), **BAT-015**, `OQ-BAT-017`; [03_data.md](03_data.md), **Input and Output File Inventory**, `DAT-FILE-003`, `OQ-DAT-016/023`; [06_exception_handling.md](06_exception_handling.md), `ERR-048`, `OQ-ERR-021`. |
| AD-085 | Audit query/detail/redaction contracts | Needs confirmation | Cursor history is confirmed; response/detail/filter ordering, digests, lineage links, and non-Auditor permissions are incomplete. | What exact authorized query/detail projection and verification display apply? | Hold Audit Explorer details and query UX. | [01_screen_functions.md](01_screen_functions.md), **Audit Explorer**, `OQ-SCR-021`; [02_api.md](02_api.md), **Audit Interfaces**, `API-021`, `OQ-API-021`; [07_processing_flows.md](07_processing_flows.md), **FLOW-018**, `OQ-FLOW-022`. |
| AD-086 | PII tags, redaction, and disclosure response | Needs confirmation | Likely-personal-data tagging and permitted redaction are required; taxonomy, offsets, masking, retained identity, full-prompt exceptions, and post-disclosure response are not. | What authorized privacy contract applies separately to source, provider, audit, diagnostics, errors, and exports? | Hold unconfirmed redaction/disclosure exceptions; existing secret/content prohibitions remain. | [03_data.md](03_data.md), **Personal Data, Secrets, and Evidence Access**, `DAT-LC-025`, `OQ-DAT-017`; [05_business_rules.md](05_business_rules.md), **BR-037**, `OQ-BR-013/023`; [06_exception_handling.md](06_exception_handling.md), `ERR-049`, `OQ-ERR-021`. |
| AD-087 | Credential/key rotation realization and failure recovery | Needs confirmation | Rotation is required, but managed versus application execution, schedule, overlap/grace, reference switch, revoke/rollback, and background reencryption are not selected. | What policy and verification/failure protocol maintain authorized access? | Hold rotation mechanics and any reencryption job; no request-path bulk reencryption. | [04_batch_functions.md](04_batch_functions.md), **BAT-024**, `OQ-BAT-024`; [07_processing_flows.md](07_processing_flows.md), **FLOW-023**, `OQ-FLOW-022/025`; [06_exception_handling.md](06_exception_handling.md), `ERR-049`, `OQ-ERR-021`. |

### Usage, Evaluation, Release, Governance, and Recovery

| Item ID | Subject | Status | Reason for remaining unresolved | Questions to confirm | Affected scope and implementation gate | Related specifications and requirement IDs |
|---|---|---|---|---|---|---|
| AD-088 | Reporting windows, late data, zero usage, and restatement | Needs confirmation | Daily rollups do not define reporting-day timezone, interval inclusion, rerun identity, corrections, or extra period-end processes. | What window, zero/omit, late-data, replace/increment, and restatement rules apply? | Hold aggregation identity/correction semantics; do not invent midnight or financial close. | [04_batch_functions.md](04_batch_functions.md), **BAT-016**, `OQ-BAT-018`; [05_business_rules.md](05_business_rules.md), **BR-043**, `OQ-BR-026`; [06_exception_handling.md](06_exception_handling.md), `ERR-053`, `OQ-ERR-023`. |
| AD-089 | Cost/forecast/trend calculation and reporting schema | Needs confirmation | Attribution/content is confirmed; currencies, precision, rates, allocation, forecast horizon/formulas, units, filters, and presentation are absent. | What approved accounting/reporting model and UI/API projection apply? | Hold money/forecast calculations and usage display assumptions. | [01_screen_functions.md](01_screen_functions.md), **Usage & Quality**, `OQ-SCR-023`; [02_api.md](02_api.md), **Audit, Usage, and Evaluation Interfaces**, `OQ-API-022`; [03_data.md](03_data.md), **DAT-030**, `OQ-DAT-020`. |
| AD-090 | Evaluation launch/read/status/progress contract | Needs confirmation | Start/read interfaces exist; input choices, result-read permission, statuses, progress, concurrency, timeouts, and partial execution are not defined. | What dataset/model/prompt selection and durable result contract applies? | Hold evaluation controls and progress/status schema. | [02_api.md](02_api.md), **Evaluation Interfaces**, `API-023/024`, `OQ-API-023`; [04_batch_functions.md](04_batch_functions.md), **BAT-017**, `OQ-BAT-019`; [07_processing_flows.md](07_processing_flows.md), **FLOW-020**, `OQ-FLOW-024`. |
| AD-091 | Evaluation metric/statistical calculations | Needs confirmation | Targets are confirmed, not denominators, aggregation, rounding, domain taxonomy, confidence method/threshold, shift calculation, or gate combination. | What exact calculations determine sufficient statistical and quality evidence? | Hold pass/fail calculations; rounded display values are not confirmed acceptance inputs. | [05_business_rules.md](05_business_rules.md), **BR-049**, `OQ-BR-029`; [03_data.md](03_data.md), **DAT-031**, `DAT-031-F02/03`, `OQ-DAT-022`; [06_exception_handling.md](06_exception_handling.md), `ERR-050`, `OQ-ERR-022`. |
| AD-092 | Frozen fixtures and signed test/release evidence | Needs confirmation | Versioned reviewed fixtures and signed evidence are required; formats, signatures, keys, replacement protocol, storage, and retention are absent. | What formal manifest, leakage-review, reproducibility, and release-link verification contracts apply? | Hold fixture/signature adapters and evidence acceptance mechanics. | [03_data.md](03_data.md), **Input and Output File Inventory**, `DAT-FILE-005/006`, `OQ-DAT-022`; [04_batch_functions.md](04_batch_functions.md), **BAT-017/BAT-026**; [07_processing_flows.md](07_processing_flows.md), **Verification Basis**, `FLOW-COM-010`. |
| AD-093 | Individual security exit requirements | Needs confirmation | `SEC-001–SEC-012` are release-blocking identifiers “without invented individual definitions.” | What are their exact controls, evidence, negative cases, and authorized sign-off contracts? | Hold complete security-exit acceptance mapping; critical safety prohibitions still apply. | [05_business_rules.md](05_business_rules.md), **Specification Basis and Status** and **BR-049**, `SEC-001–SEC-012`, `OQ-BR-029`; [06_exception_handling.md](06_exception_handling.md), **Open-Decision Register**, `OQ-ERR-022`. |
| AD-094 | Actual migrations and compatibility publication | Needs confirmation | Expand-and-contract is confirmed; transformations, batch bounds, checkpoints, concurrent writes, compatibility matrices, removal schedules, and compensation are absent. | What approved migrations and contract-publication process preserve active readers and readable writes? | Hold specific migrations/enforcement/removal and data compensation. | [02_api.md](02_api.md), **Public Contract Governance**, `API-COM-004`, `OQ-API-030`; [04_batch_functions.md](04_batch_functions.md), **BAT-022**, `OQ-BAT-022`; [03_data.md](03_data.md), **Schema Evolution and Onboarding**, `DAT-LC-026`, `OQ-DAT-022`. |
| AD-095 | Build, canary, promotion, and sign-off protocol | Needs confirmation | Required gates exist, but toolchain, allowed build identities, SBOM/signatures, sequence, thresholds/windows, sign-off transport, and promotion state are incomplete. | What reproducible pipeline and rollback protocol realizes required Security/SRE and security-control validation? | Hold promotion configuration and canary calculations; no automatic database down-migration. | [04_batch_functions.md](04_batch_functions.md), **BAT-026**, `OQ-BAT-022`; [05_business_rules.md](05_business_rules.md), **BR-048**, `OQ-BR-029`; [07_processing_flows.md](07_processing_flows.md), **FLOW-021**, `OQ-FLOW-024`. |
| AD-096 | Design-decision/baseline governance | Needs confirmation | Change impacts and revision/test-link rules exist; schemas, scales, rights, approval, formatting/reset, result mode, and commit trigger are absent. | What controlled approval/versioning contract governs changes and implementation lock? | Hold governance APIs/approval mechanics; baseline reads do not commit changes. | [02_api.md](02_api.md), **Status, Contract Discovery, and Design Governance**, `API-032/033`, `OQ-API-026`; [03_data.md](03_data.md), **DAT-033**, `OQ-DAT-022`; [07_processing_flows.md](07_processing_flows.md), **FLOW-025**, `OQ-FLOW-024`. |
| AD-097 | Health, readiness, capacity, and degraded projections | Needs confirmation | Interfaces exist; probe identity/exposure, dependency checks, freshness, states, scope, timeouts, and UI mapping are undefined. | What authorized projection and readiness/degradation contract applies to each interface? | Hold probe/health API implementation and health-summary assumptions. | [02_api.md](02_api.md), **Status, Contract Discovery, and Design Governance**, `API-030/034/035/042`, `OQ-API-031`; [01_screen_functions.md](01_screen_functions.md), `OQ-SCR-028`; [03_data.md](03_data.md), `OQ-DAT-026`. |
| AD-098 | SLO/load measurement and strict case-create boundary | Needs confirmation | “Within 300 ms” and “under 300 ms” differ; availability/burn denominator, windows, exclusions, and workload-to-quota mapping are absent. | What measurement points and exact boundary/availability/load calculations apply? | Hold strict acceptance and error-budget computation; latency targets are not timeouts. | [05_business_rules.md](05_business_rules.md), **BR-046**, `OQ-BR-028`; [02_api.md](02_api.md), **Configuration and Performance Boundaries**, `OQ-API-033`; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-021`, `AC-FLOW-042`. |
| AD-099 | Metrics, logs, sampling, scaling, alerts, and recipients | Needs confirmation | Signal/paging categories exist; schemas, levels, sample policy, calculation windows, thresholds, routes, channels, assignments, and deduplication do not. | What approved observability and notification policies realize the confirmed categories? | Hold actual monitoring/scaling/paging configuration; do not invent owners or recipients. | [04_batch_functions.md](04_batch_functions.md), **Logging, Notifications, Monitoring, and Capacity**, `BAT-OPS-007/008`, `OQ-BAT-008`; [06_exception_handling.md](06_exception_handling.md), **Log Levels** and **Monitoring and Notification Conditions**, `OQ-ERR-024`; [07_processing_flows.md](07_processing_flows.md), `OQ-FLOW-023`. |
| AD-100 | Backup, regional recovery, and activation mechanics | Needs confirmation | Primary/warm recovery and targets exist; backup formats/retention, checkpoints, commands, fencing, restore failure, deletion/hold propagation, drill cadence, and timing points are missing. | What incident-controlled recovery protocol and evidence establish safe restoration? | Hold failover/restore activation and backup lifecycle choices. | [04_batch_functions.md](04_batch_functions.md), **BAT-023**, `OQ-BAT-023`; [03_data.md](03_data.md), **DAT-LC-024/DAT-FILE-007**, `OQ-DAT-018/025`; [06_exception_handling.md](06_exception_handling.md), `ERR-052`, `OQ-ERR-026`; [07_processing_flows.md](07_processing_flows.md), **FLOW-022**. |

### Screens, Errors, Remaining Handoffs, and Shared Metadata

| Item ID | Subject | Status | Reason for remaining unresolved | Questions to confirm | Affected scope and implementation gate | Related specifications and requirement IDs |
|---|---|---|---|---|---|---|
| AD-101 | Screen hierarchy, routes, navigation, and primary actions | Needs confirmation | Primary screens exist, but aliases, active-navigation illustrations, resource selection, deep links, history, and action emphasis are unresolved. | What approved hierarchy and route/action/navigation contract applies to each screen? | Hold route organization and proposed interactions, not confirmed screen responsibilities. | [01_screen_functions.md](01_screen_functions.md), **Screen Inventory and Navigation**, `SCR-001–011`, `OQ-SCR-001`, `CON-SCR-001/002`; [07_processing_flows.md](07_processing_flows.md), **Screen-to-Contract Mapping**, `OQ-FLOW-017`. |
| AD-102 | Overview and shared summary projections | Needs confirmation | Illustrated cards do not define scope, formulas, APIs, placement, refresh, null/error behavior, or Overview purpose. | What real aggregates and authorized projection contracts are required? | Hold dashboard/summary APIs, materialization, and refresh jobs. | [01_screen_functions.md](01_screen_functions.md), **Shared Illustrated Shell and Summary Fields** and **Overview**, `SCR-COM-F01–07`, `OQ-SCR-022`; [02_api.md](02_api.md), `API-GAP-010`, `OQ-API-036`; [03_data.md](03_data.md), `DAT-035`, `OQ-DAT-026`. |
| AD-103 | Usage/quality screen organization | Needs confirmation | The illustrated combined destination and scorecard do not establish standalone/subview organization, permissions, primary action, or graphical/tabular layout. | What approved navigation, controls, reporting layout, and result permissions apply? | Hold Usage & Quality/scorecard binding and promotion controls. | [01_screen_functions.md](01_screen_functions.md), **SCR-010/SCR-011**, `OQ-SCR-023/024`, `P-SCR-001`; [07_processing_flows.md](07_processing_flows.md), **Screen-to-Contract Mapping**, `OQ-FLOW-017/024`. |
| AD-104 | Browser, responsive/localized presentation, and failure UX | Needs confirmation | WCAG/timezone constraints do not define supported browsers, viewport/mobile, formats, focus after navigation/error, messages, retained forms, or retry controls. | What exact presentation/accessibility/error-recovery contract is approved? | Hold unconfirmed UI behavior and screen-level performance assertions. | [01_screen_functions.md](01_screen_functions.md), **Navigation and Status Requirements**, `OQ-SCR-031`; [06_exception_handling.md](06_exception_handling.md), **Truthful Accessible Failure Display**, `ERR-COM-005`, `OQ-ERR-025`; [03_data.md](03_data.md), `OQ-DAT-024/026`. |
| AD-105 | Completion notifications and optional webhook administration | Needs confirmation | No general completion channel is selected; signed webhook capability lacks subscription, payload, URL/method, signature/age, acknowledgment, retries, and redelivery contracts. | Which notifications are required, through what authorized channels and webhook security/delivery protocol? | Hold notification screens/delivery/admin APIs; no email/SMS fallback by inference. | [02_api.md](02_api.md), **API-047**, `API-GAP-012`, `OQ-API-029`; [04_batch_functions.md](04_batch_functions.md), **BAT-025**, `OQ-BAT-025`; [06_exception_handling.md](06_exception_handling.md), `ERR-043`, `OQ-ERR-017/024`. |
| AD-106 | Complete error/status/casing and generic failure contracts | Needs confirmation | Known literals and selected statuses are confirmed; universal envelopes, per-operation mappings, RPC/async errors, field details, and generic internal handling are absent. | What stable safe contract distinguishes revision, idempotency, stale hash, validation, permission, dependency, and asynchronous failures? | Hold undocumented error mappings and generic fallback/retry policies. | [02_api.md](02_api.md), **Failure Mapping and Caller Actions**, `OQ-API-032`; [06_exception_handling.md](06_exception_handling.md), **Canonical Error Envelope**, `ERR-COM-003/004`, `ERR-054`, `OQ-ERR-001`; [01_screen_functions.md](01_screen_functions.md), `OQ-SCR-029`. |
| AD-107 | Remaining security/nonfunctional/operations coverage and stale handoffs | Needs confirmation | These implementation contracts remain open; no additional completed specification is supplied. Existing stages resolve documentation availability only within their scope. | Where will missing security/operations contracts and controlled dependency-pointer amendments be maintained? | Hold claims that a complete additional security or operations specification exists. | [07_processing_flows.md](07_processing_flows.md), **Cross-Specification Conflicts** and **Proposal Status and Dependencies**, `CON-FLOW-022`, `OQ-FLOW-026`; [06_exception_handling.md](06_exception_handling.md), **Dependencies and Later Handoffs**. |
| AD-108 | Hash/digest/checksum canonicalization | Needs confirmation | Similar field names do not establish common algorithms, inputs, scope, or encoding. | What exact protocol applies separately to source, text, artifact, ACL, input, audit, manifest, and release checksums/signatures? | Hold digest equality/verification and hash-derived identity assumptions. | [03_data.md](03_data.md), **Identity, Hash, and Version Distinctions**, `DAT-COM-004`, `OQ-DAT-009/016/021/023`; [05_business_rules.md](05_business_rules.md), **BR-030/BR-037**, `OQ-BR-018/023`. |
| AD-109 | Version, actor, time, and identifier alias mapping | Needs confirmation | `actor`/`actor_id`/`reviewer_id`, `at`/`occurred_at`/`purge_time`, and policy/parser/plan versions are not interchangeable by name. | What physical/wire semantic mappings, time authority, precision, accepted encoding, and independent version relationships apply? | Hold alias unification and serialization/time-order assumptions. | [03_data.md](03_data.md), **Shared Identity, Tenancy, and Attribution Fields** and **Identity, Hash, and Version Distinctions**, `DAT-COM-F01–06`, `DAT-COM-004`, `CON-DAT-007`, `OQ-DAT-003/024`; [02_api.md](02_api.md), **Shared Parameter Definitions**. |

### Explicitly Unadopted Proposals

These rows preserve actual proposed options. They are not additional approved architecture choices.

| Item ID | Subject | Status | Reason for remaining unresolved | Questions to confirm | Affected scope and implementation gate | Related specifications and requirement IDs |
|---|---|---|---|---|---|---|
| AD-110 | Consolidated screen aliases and scorecard subview | Unadopted proposal | Proposed alias consolidation and SCR-011-as-SCR-010 subview are not approved. | Is `P-SCR-001` adopted, amended, or rejected after hierarchy confirmation? | Hold this organization; related decisions `AD-101/103`. | [01_screen_functions.md](01_screen_functions.md), **Screen Inventory** and **Proposal Register**, `P-SCR-001`, `OQ-SCR-001/024`; [07_processing_flows.md](07_processing_flows.md), **Proposal Status and Dependencies**. |
| AD-111 | New-case mode associated with Case Detail | Unadopted proposal | “Use a new-case mode associated with Case Detail, launched from Case Queue” remains unapproved. | Which creation placement and success destination are approved? | Hold `P-SCR-002`; related `AD-027/101`. | [01_screen_functions.md](01_screen_functions.md), **Proposal Register**, `P-SCR-002`, `SCR-001-A04`, `SCR-002-A02`; [07_processing_flows.md](07_processing_flows.md), **FLOW-002-S01**. |
| AD-112 | Proposed domain/configuration field and control placement | Unadopted proposal | Confirmed data does not approve the proposed screen fields, links, search/edit controls, or configuration toggles. | Which placements and controls are approved after schemas and permissions resolve? | Hold `P-SCR-003` wherever placement is proposed. | [01_screen_functions.md](01_screen_functions.md), **Proposal Register**, `P-SCR-003`; [03_data.md](03_data.md), **Proposal Status**; [07_processing_flows.md](07_processing_flows.md), **FLOW-COM-001**. |
| AD-113 | Direct REST Bearer token carrier | Unadopted proposal | `Authorization: Bearer` is proposed, not selected against optional BFF cookies. | Is this carrier approved for relevant clients, with what session/SSE/CSRF contract? | Hold `P-API-001`; related `AD-015/016`. | [02_api.md](02_api.md), **Shared Parameter Definitions** and **Proposal Register**, `P-API-001`, `OQ-API-001`; [06_exception_handling.md](06_exception_handling.md), **Proposal Status**. |
| AD-114 | Partial JSON request/result mappings | Unadopted proposal | Case/run/search/decision examples are explicitly “unapproved” mappings, not executable schemas. | Which exact IDL properties/wrappers/requiredness are approved? | Hold `P-API-002`; related `AD-023/027/054/064`. | [02_api.md](02_api.md), **Proposed Partial JSON Mappings**, `P-API-002`; [03_data.md](03_data.md), **Proposal Status**; [07_processing_flows.md](07_processing_flows.md), **FLOW-COM-001**. |

## Items Resolved by the Specifications

Resolution here is deliberately narrow. **Documentation availability** is resolved where a later supplied file explicitly supplies the previously deferred specification. This does not resolve that document’s open contracts or authorize a rewrite of earlier files.

| Item ID | Original question/deferred reference | Statements establishing the answer | Referenced Markdown sections and requirement IDs | Reason for resolution and remaining boundary |
|---|---|---|---|---|
| AD-R001 | Is the API specification still future work? | The earlier dependency says “API specification — To be defined in a later stage.” The supplied API file explicitly inventories public/internal/external interfaces and processing contracts. | [01_screen_functions.md](01_screen_functions.md), **Dependencies on Later Specifications**, API specification dependency; `SCR-COM-010/012`. [02_api.md](02_api.md), **API Inventory and Responsibilities**, `API-001–050`, `API-COM-001–007`; **Handoffs and Dependencies**. `CON-API-017`. | **Resolved: API documentation exists as `02_api.md`.** Payloads, missing APIs, authorization, and errors remain outstanding under `AD-015–032/051/054/063/066/106`. |
| AD-R002 | Is the Data Specification/filename still undefined? | The earlier API handoff says “Data Specification — To be defined in a later stage” and “Filename is not supplied.” The supplied data file declares `03_data.md` and defines its datasets, fields, relationships, and lifecycle requirements. | [02_api.md](02_api.md), **Handoffs and Dependencies**, Data Specification dependency; `API-CASE-F01–18`, `API-EVID-F01–13`. [03_data.md](03_data.md), **Specification Basis and Status**, **Data Inventory and Relationships**, `DAT-001–036`, `DAT-REL-001–022`; `CON-DAT-022`. | **Resolved: data documentation exists as `03_data.md`.** It is not a complete physical schema; `AD-006/023–025/031/032/038/108/109` remain open. |
| AD-R003 | Is business-rule coverage still deferred? | Earlier handoffs defer workflow/business rules. The supplied Business Rules file explicitly defines `BR-001–BR-050` and application/acceptance mappings. | [01_screen_functions.md](01_screen_functions.md), **Dependencies on Later Specifications**, Workflow/business-rule dependency. [04_batch_functions.md](04_batch_functions.md), **Dependencies and Later Handoffs**, Workflow/business-rule dependency. [05_business_rules.md](05_business_rules.md), **Rule Inventory and Scope**, `BR-001–050`; `CON-BR-020`. | **Resolved: business-rule documentation exists as `05_business_rules.md`.** Missing calculations, predicates, effective periods, and lifecycle guards are not resolved. |
| AD-R004 | Is exception-handling documentation still future work? | Earlier handoffs explicitly defer exception handling. The supplied exception file defines exceptional conditions, shared handling, recovery, and acceptance mappings. | [02_api.md](02_api.md), **Handoffs and Dependencies**, Exception Handling dependency; `API-COM-007`. [05_business_rules.md](05_business_rules.md), **Dependencies and Later Handoffs**, Exception handling dependency. [06_exception_handling.md](06_exception_handling.md), **Exception Inventory and Classification**, `ERR-001–054`, `ERR-COM-001–008`; `CON-ERR-019`. | **Resolved: exception documentation exists as `06_exception_handling.md`.** Complete status/code, retry, compensation, and UI contracts remain open. |
| AD-R005 | Is processing/workflow documentation still deferred? | Earlier handoffs defer workflow coverage. The supplied flow file provides logical flows, numbered steps, durable boundaries, branches, diagrams, and mappings. | [03_data.md](03_data.md) and [06_exception_handling.md](06_exception_handling.md), **Dependencies and Later Handoffs**, Workflow dependency. [07_processing_flows.md](07_processing_flows.md), **Flow Inventory and Prerequisites**, `FLOW-001–025`; **Durable Boundary Register**, `FLOW-TX-001–007`; `CON-FLOW-022`. | **Resolved: processing-flow documentation exists as `07_processing_flows.md`.** Diagrams do not resolve absent APIs, permissions, states, or compensation. |
| AD-R006 | Is batch/background coverage still unavailable within the earlier operational handoffs? | Earlier operational handoffs defer background details. The supplied batch file explicitly documents logical functions and says controlled amendments may link that coverage to `04_batch_functions.md`. | [03_data.md](03_data.md), **Dependencies and Later Handoffs**, Operations dependency; `DAT-LC-001–012`. [04_batch_functions.md](04_batch_functions.md), **Batch Inventory and Triggers**, `BAT-001–026`; **Conflicts and Required Amendments**, `CON-BAT-018`. | **Resolved only for batch/background documentation availability.** A complete Operations Specification, scheduler, worker, monitoring, and protected-control design is **not** resolved; see `AD-070–076/099/100/107`. |

No supplied `OQ` record is closed in full by these documentation resolutions. No provider, deployment setting, proposed UI organization, token carrier, or JSON mapping is adopted here.

## Cross-Specification Conflicts and Pending Decisions

The following records show both sides of each conflict or tension. Some are incomplete contracts rather than mutually exclusive requirements; that distinction is retained. Repetition and later-generation order do not choose an answer.

| Conflict ID | Type and statements retained from the Markdown specifications | Evidence | Impact and pending confirmation |
|---|---|---|---|
| CF-001 | Endpoint conflict: `POST /v1/runs` versus `POST /v1/cases/{caseId}/runs`. | [02_api.md](02_api.md), **Public Application API Inventory**, `API-011/012`; [07_processing_flows.md](07_processing_flows.md), **Cross-Specification Conflicts**, `CON-FLOW-001`. | Canonical/alternate semantics and case binding remain pending: `AD-054`. |
| CF-002 | Lifecycle conflict: “missing approval terminates a run” versus valid `AWAITING_REVIEW`; “terminal result or recoverable timeout” has no complete state representation. | [01_screen_functions.md](01_screen_functions.md), `CON-SCR-005`; [02_api.md](02_api.md), **Runtime, Admission, Timeouts, and Retries**, `API-PROC-022/023`; [05_business_rules.md](05_business_rules.md), **BR-026**. | Distinguish waiting, missing-approval failure, execution timeout, and reviewer expiry: `AD-056/065`. |
| CF-003 | Lifecycle gap: a close operation exists, but “explicit `RESOLVED -> CLOSED` transition is not enumerated”; reopening is permitted only as a new revision without a complete API. | [02_api.md](02_api.md), **Confirmed Case States and Guards**, `API-005`, `OQ-API-007`; [07_processing_flows.md](07_processing_flows.md), **FLOW-008**, `CON-FLOW-003`. | Closure/reopen guards and lineage contracts remain pending: `AD-036/037`. |
| CF-004 | Authorization inconsistency: baseline roles are named, but `Owner`, `Member`, operator, approver, elevated role, and `Workspace Admin` are not consistently classified. | [01_screen_functions.md](01_screen_functions.md), **Users and Permissions**, `OQ-SCR-003`, `CON-SCR-007`; [05_business_rules.md](05_business_rules.md), **BR-003**. | No inferred alias, hierarchy, or grant: `AD-017/019/020/061/077`. |
| CF-005 | Authorization conflict: “Auditor journey allows evidence access” while case-read scope lists “only Analyst/Reviewer.” | [01_screen_functions.md](01_screen_functions.md), **Users and Permissions**, `CON-SCR-008`; [02_api.md](02_api.md), **API-003/API-021**, `CON-API-004`. | Confirm a redacted Auditor evidence path, not general case access: `AD-018/085`. |
| CF-006 | Scope conflict: high-risk self-approval is expressly prohibited, while `approval_tasks` says “no self approval” and the example says `self_approval_allowed: false`. | [05_business_rules.md](05_business_rules.md), **BR-029**, `CON-BR-005`; [03_data.md](03_data.md), **DAT-011**, `DAT-011-F04`. | Preserve high-risk prohibition; confirm broader scope separately: `AD-062`. |
| CF-007 | Interface association conflict: workspace settings are associated with `PATCH /v1/cases/{caseId}`, but that endpoint mutates a case. | [01_screen_functions.md](01_screen_functions.md), **Policy Settings**, `OQ-SCR-020`, `CON-SCR-010`; [02_api.md](02_api.md), **Required Capabilities**, `API-GAP-002`. | Supply actual policy interfaces; do not repurpose case PATCH: `AD-014/030`. |
| CF-008 | Trigger gap: chapter-boundary descriptions associate GETs with durable events/work; `UserReviewOpened` is named without a precise trigger. | [02_api.md](02_api.md), **Source Conflicts**, `CON-API-007/008`; [07_processing_flows.md](07_processing_flows.md), **FLOW-018–021/FLOW-025**, `CON-FLOW-006`. | Confirm real write/detector/open triggers; do not make every read mutate: `AD-063/068/070/097`. |
| CF-009 | Envelope gap: mandatory event names omit actor/correlation properties, while durable boundaries require actor/correlation attribution. | [02_api.md](02_api.md), **Common Event Envelope**, `API-COM-006`, `CON-API-013`; [03_data.md](03_data.md), **Mandatory Envelope**, `DAT-EVT-F01–09`. | Confirm whether attribution is linked, payload-carried, or an approved envelope extension: `AD-068/109`. |
| CF-010 | A2A contract gap: “declared input/output schemas” are required, but the example omits output declaration and uses non-production tenant/case placeholders. | [02_api.md](02_api.md), **API-046**, `CON-API-012`; [03_data.md](03_data.md), **A2A Envelope**, `CON-DAT-017`. | Formalize output/ID/grant/decline contracts without copying placeholders: `AD-022`. |
| CF-011 | Data interpretation conflict: registers describe mutable case concepts as “Immutable derivative,” while prose defines mutable current case state and append-only revisions; selected DDL omits business fields. | [03_data.md](03_data.md), **Conflicts and Required Amendments**, `CON-DAT-001/002`; **DAT-003/DAT-004**; [02_api.md](02_api.md), `CON-API-011`. | Complete schema and distinguish current state from immutable history: `AD-006/023/027/037`. |
| CF-012 | Identity gap: application UUIDv7 baseline coexists with “fingerprint plus pipeline version” immutable derivative identity and an omitted version-ID field. | [03_data.md](03_data.md), **DAT-006**, `CON-DAT-003`; [04_batch_functions.md](04_batch_functions.md), **BAT-003**, `CON-BAT-009`. | Confirm identity derivation and uniqueness, not a guessed hash-to-UUID conversion: `AD-038/108`. |
| CF-013 | Uniqueness scope tension: explicit `unique(slug)`, global case `id` PK, and `(tenant_id,id)` uniqueness coexist with generic tenant/business-key wording. | [03_data.md](03_data.md), **DAT-001/DAT-003**, `CON-DAT-004`; [05_business_rules.md](05_business_rules.md), **BR-004**. | Preserve explicit reference constraints until scope/normalization is confirmed: `AD-024–026`. |
| CF-014 | Security tension: unsupported capabilities trigger lower-trust ingestion, while ACL enforcement and revocation before next retrieval remain mandatory. | [01_screen_functions.md](01_screen_functions.md), `CON-SCR-013`; [05_business_rules.md](05_business_rules.md), **BR-021/BR-034**; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-011`. | Define safe capability restrictions, never an ACL bypass: `AD-050/052`. |
| CF-015 | Cursor/storage gap: each sync run stores cursor/watermark/error ledger, but selected cursor data is connector-associated; durable ingestion is not formally equated to indexed `READY`. | [03_data.md](03_data.md), **DAT-015**, `CON-DAT-011`; [07_processing_flows.md](07_processing_flows.md), **FLOW-009-S05**, `CON-FLOW-012`. | Confirm current/history layout, durable exceptions, ownership, and completion boundary: `AD-053`. |
| CF-016 | Lifecycle tension: immutable closed citations, audit, and receipts coexist with source/workspace deletion, holds, and backup recovery. | [03_data.md](03_data.md), `CON-DAT-019`; [05_business_rules.md](05_business_rules.md), **BR-015/BR-038/BR-041**; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-015`. | Confirm retained/removed scope and historical access; no cascade erasure or source substitution: `AD-037/079–081/100`. |
| CF-017 | Configuration status tension: reference timeout, retention, sampling, and policy values exist, while actual corporate/provider selections are expressly open. | [03_data.md](03_data.md), **Configuration Example Interpretation**, `CON-DAT-020`; [05_business_rules.md](05_business_rules.md), **BR-010/BR-038/BR-050**. | Examples remain examples; confirm approved values and precedence: `AD-001–014/056/081/099`. |
| CF-018 | Error convention conflict: “snake-case error codes” versus uppercase known literals. Also, `409` has distinct revision, key-fingerprint, and artifact-hash causes. | [02_api.md](02_api.md), **Failure Mapping**, `CON-API-009`; [06_exception_handling.md](06_exception_handling.md), `CON-ERR-001/002`, `ERR-001/002/031`. | Preserve exact known literals; confirm complete distinct mappings: `AD-106`. |
| CF-019 | Evidence outcome distinction: missing citations yield “needs-review or unsupported”; invalid citations trigger `MODEL_OUTPUT_INVALID`. | [06_exception_handling.md](06_exception_handling.md), `CON-ERR-004`, `ERR-004/005/025`; [05_business_rules.md](05_business_rules.md), **BR-019/BR-023**. | Define absence, invalidity, insufficiency, and remaining-evidence continuation: `AD-046/059/106`. |
| CF-020 | Injection continuation gap: abuse must fail closed against authority escalation, while the gateway strips directives and records indicators. | [06_exception_handling.md](06_exception_handling.md), `CON-ERR-005`, **ERR-026 handling**; [05_business_rules.md](05_business_rules.md), **BR-023**. | Confirm detection-specific continuation/termination; neither unrestricted continuation nor universal indicator termination is established: `AD-059`. |
| CF-021 | Safety distinction: unsafe attachments are quarantined without indexing; authorized low-quality material remains viewable. | [02_api.md](02_api.md), `API-COM-005`; [06_exception_handling.md](06_exception_handling.md), `CON-ERR-008`, `ERR-023/024`. | The latter does not authorize active quarantine rendering: `AD-042/043`. |
| CF-022 | Illustration conflicts: active-sidebar highlights disagree with titles; mixed statuses and repeated summaries do not define actual hierarchy, aggregate ownership, or placement. | [01_screen_functions.md](01_screen_functions.md), **Source Conflicts**, `CON-SCR-001/002/003/014`; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-018`. | Confirm navigation, status mapping, and real aggregates: `AD-036/101–104/110–112`. |
| CF-023 | Numerical boundary conflict: case-create P95 “within 300 ms” versus “under 300 ms”; neither is a worker/HTTP timeout. | [01_screen_functions.md](01_screen_functions.md), **Performance and Verification Boundaries**, `OQ-SCR-031`; [05_business_rules.md](05_business_rules.md), **BR-046**, `CON-BR-015`; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-021`. | Confirm strict equality and measurement separately from timeout: `AD-056/098`. |
| CF-024 | Event association gap: `DeploymentPromoted` and `ReleasePromoted` are distinct; deletion verification is sometimes associated with export/provisioning prose without a valid trigger contract. | [02_api.md](02_api.md), **Source Event Inventory**, `CON-API-014`; [04_batch_functions.md](04_batch_functions.md), `CON-BAT-015`; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-016`. | Confirm producers/triggers; no health-read promotion or export deletion-verification: `AD-068/079/095`. |
| CF-025 | Execution-realization gap: expiry, rotation, retention, and audit-export behavior does not select standalone jobs or managed facilities. | [04_batch_functions.md](04_batch_functions.md), `BAT-COM-001`, `CON-BAT-001/017`; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-019`. | Confirm executables, triggers, and scheduling: `AD-070/071/087`. |
| CF-026 | Documentation-status gap: earlier handoffs still call completed stages future work; additional security/operations coverage remains incomplete. | [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-022`, **Proposal Status and Dependencies**; earlier file-specific handoff conflicts listed below. | Documentation availability is resolved narrowly under `AD-R001–006`; controlled pointer updates and missing contracts remain `AD-107`. |
| CF-027 | Alias semantics gap: actor/time and policy/parser/configuration versions use differing names with no confirmed universal equivalence. | [03_data.md](03_data.md), `CON-DAT-007`, `DAT-COM-F01–06`; [02_api.md](02_api.md), **Shared Parameter Definitions**. | Confirm explicit mappings and independent versions: `AD-014/109`. |
| CF-028 | Digest/persistence gap: set/item/source/cache digests have distinct possible scopes; read-like search returns an evidence-set ID despite run-linked selected storage. | [03_data.md](03_data.md), `CON-DAT-009/010`, `DAT-010/DAT-027`; [02_api.md](02_api.md), `API-PROC-004`. | Confirm standalone persistence and digest scopes: `AD-047/050/108`. |
| CF-029 | Physical-security completeness gap: simple case FKs/RLS and partial fields omit required workspace-tenancy enforcement and tenant/attribution realization. | [03_data.md](03_data.md), `CON-DAT-005/006`, `DAT-COM-003`; [04_batch_functions.md](04_batch_functions.md), `CON-BAT-008`; [06_exception_handling.md](06_exception_handling.md), `CON-ERR-009`. | Complete physical/shared-context contracts without waiving invariants: `AD-023/024/031/032/109`. |
| CF-030 | Retention-scope distinction: the confirmed 24-hour case request mapping differs from example `replay_dedup_hours: 24` and undefined SSE/broker/consumer history. | [04_batch_functions.md](04_batch_functions.md), `CON-BAT-012`, **BAT-OPS-004**; [06_exception_handling.md](06_exception_handling.md), `CON-ERR-015`. | Confirm each ledger/history lifetime separately: `AD-029/068/069/104`. |
| CF-031 | Period/clock distinction: daily aggregation and monthly availability do not imply midnight execution, quota resets, or financial closing. | [05_business_rules.md](05_business_rules.md), `CON-BR-018`, **BR-043/BR-046**; [04_batch_functions.md](04_batch_functions.md), `CON-BAT-016`. | Confirm independent reporting, scheduler, quota, and SLO windows: `AD-058/071/088/098`. |
| CF-032 | Request-semantics gap: data-subject “access requests” use deletion inventory; this does not establish universal erasure. | [03_data.md](03_data.md), `DAT-LC-022`, `CON-DAT-023`; [05_business_rules.md](05_business_rules.md), **BR-041**. | Confirm access/export/erasure outputs and hold interactions: `AD-079/080`. |
| CF-033 | Approval-protocol gap: two independent checks are required, but scope binding, validity, and initiator participation are absent. | [05_business_rules.md](05_business_rules.md), `CON-BR-019`, **BR-039**; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-014`. | No client-ID-only protocol is adopted: `AD-077/078/079`. |
| CF-034 | Review-record gap: decision capture requires actor/time/hash/rationale/optional annotations, while selected fields are incomplete and public JSON mappings are proposed. | [03_data.md](03_data.md), `CON-DAT-008`, **DAT-012**; [02_api.md](02_api.md), `P-API-002`; [07_processing_flows.md](07_processing_flows.md), `CON-FLOW-008/014`. | Complete immutable capture and formal wire schema: `AD-063/064/108/109/114`. |

## Consistency and Open Questions

### Review Coverage and Complete Open-Question Traceability

Each table below cites the named file’s **Consistency and Open Questions → Open-Decision Register**. Every listed `OQ` remains outstanding in full. The associated `AD` items separate independent questions; they do not close the original broad record.

The reviewed scope also includes each file’s inventories, detailed requirements, acceptance boundaries, proposal status, conflicts, and later handoffs—not merely its final register.

### 01_screen_functions.md

**Reviewed sections:** Scope and Users; Screen Inventory and Navigation; Functions by Screen; Unlocated Screen-Affecting Operations; Integrations and Acceptance Criteria; Consistency and Open Questions.  
**Reference:** [01_screen_functions.md](01_screen_functions.md), **Open-Decision Register**.

| Existing ID | Consolidated items |
|---|---|
| OQ-SCR-001 | AD-028/101–104/110/111 |
| OQ-SCR-002 | AD-003/015/016/113 |
| OQ-SCR-003 | AD-017–020/061/062/077/085 |
| OQ-SCR-004 | AD-023/027/104/109/112/114 |
| OQ-SCR-005 | AD-027/101/111 |
| OQ-SCR-006 | AD-026/036/101/102 |
| OQ-SCR-007 | AD-033 |
| OQ-SCR-008 | AD-034/035/060 |
| OQ-SCR-009 | AD-038–043 |
| OQ-SCR-010 | AD-044/045/108 |
| OQ-SCR-011 | AD-028/046/047 |
| OQ-SCR-012 | AD-054–056/067/072/073 |
| OQ-SCR-013 | AD-068/069/104/109 |
| OQ-SCR-014 | AD-063/064/108 |
| OQ-SCR-015 | AD-061/065 |
| OQ-SCR-016 | AD-066 |
| OQ-SCR-017 | AD-067 |
| OQ-SCR-018 | AD-030/036/037 |
| OQ-SCR-019 | AD-005/051–053/073 |
| OQ-SCR-020 | AD-014/023/030/060/066/112 |
| OQ-SCR-021 | AD-018/063/068/084/085/108 |
| OQ-SCR-022 | AD-102/103 |
| OQ-SCR-023 | AD-088/089/103 |
| OQ-SCR-024 | AD-090–093/103/110 |
| OQ-SCR-025 | AD-077–081 |
| OQ-SCR-026 | AD-017/080/082/083 |
| OQ-SCR-027 | AD-070–076/096/099/105/107 |
| OQ-SCR-028 | AD-050/052/076/097/099/102/104 |
| OQ-SCR-029 | AD-030/104/106 |
| OQ-SCR-030 | AD-001–014/087/100 |
| OQ-SCR-031 | AD-035/098/104/109 |

**Conflict trace — same file, Source Conflicts and Required Amendments:**  
`CON-SCR-001/002/003/014` → `CF-022`; `004` → `CF-001`; `005` → `CF-002`; `006` → `CF-003`; `007` → `CF-004`; `008` → `CF-005`; `009` → `CF-006`; `010` → `CF-007`; `011` → `CF-008`; `012` → `CF-018`; `013` → `CF-014`; `015` → `CF-017`.

**Proposal trace — Proposal Register:** `P-SCR-001` → `AD-110`; `P-SCR-002` → `AD-111`; `P-SCR-003` → `AD-112`.  
**Handoff status — Dependencies on Later Specifications:** API/data/rule/flow/exception and batch documentation availability is addressed in `AD-R001–006`; unresolved security/operations content remains `AD-107`.

### 02_api.md

**Reviewed sections:** API Inventory and Responsibilities; Interfaces by API; Processing and Consistency; Errors and Acceptance Criteria; Consistency and Open Questions.  
**Reference:** [02_api.md](02_api.md), **Open-Decision Register**.

| Existing ID | Consolidated items |
|---|---|
| OQ-API-001 | AD-003/015/016/113 |
| OQ-API-002 | AD-017–020/061/062/077 |
| OQ-API-003 | AD-023/027/039/064/109/114 |
| OQ-API-004 | AD-029/031/069 |
| OQ-API-005 | AD-030–032/065/079/080 |
| OQ-API-006 | AD-028 |
| OQ-API-007 | AD-025–027/034–037 |
| OQ-API-008 | AD-033 |
| OQ-API-009 | AD-038–043 |
| OQ-API-010 | AD-044/045/050/108 |
| OQ-API-011 | AD-028/046–049 |
| OQ-API-012 | AD-054/067 |
| OQ-API-013 | AD-055–058/065/073 |
| OQ-API-014 | AD-028/068/104/109 |
| OQ-API-015 | AD-063/064/065/108 |
| OQ-API-016 | AD-061/062/065 |
| OQ-API-017 | AD-066 |
| OQ-API-018 | AD-067 |
| OQ-API-019 | AD-005/050–053/073 |
| OQ-API-020 | AD-014/023/030/060/066/112 |
| OQ-API-021 | AD-018/084–086/108 |
| OQ-API-022 | AD-058/088/089 |
| OQ-API-023 | AD-090–093 |
| OQ-API-024 | AD-031/077–081 |
| OQ-API-025 | AD-017/023/025/080/082/083 |
| OQ-API-026 | AD-068/096 |
| OQ-API-027 | AD-019/023/031/069/070/072–076/079/094/095 |
| OQ-API-028 | AD-019–022/044/073 |
| OQ-API-029 | AD-073/105 |
| OQ-API-030 | AD-023/094 |
| OQ-API-031 | AD-049/050/057/097/102 |
| OQ-API-032 | AD-030/073/104/106 |
| OQ-API-033 | AD-057/098–100 |
| OQ-API-034 | AD-001–014/051/086/087/100 |
| OQ-API-035 | AD-022/063/068/069/074/104/105/109 |
| OQ-API-036 | AD-101–104 |

**Conflict trace — same file, Source Conflicts and Required Amendments:**  
`CON-API-001` → `CF-001`; `002` → `CF-002`; `003` → `CF-003`; `004` → `CF-004/005`; `005` → `CF-006`; `006` → `CF-007`; `007/008` → `CF-008`; `009` → `CF-018`; `010` → `CF-014`; `011` → `CF-011`; `012` → `CF-010`; `013` → `CF-009`; `014` → `CF-024`; `015` → `CF-017`; `016` → `CF-023`; `017` → `CF-026/AD-R001`.

**Gap trace — Required Capabilities Without a Confirmed API Contract:**  
`API-GAP-001` → `AD-033`; `002` → `AD-014/023/030`; `003` → `AD-044/045`; `004` → `AD-063`; `005` → `AD-037/054/067`; `006` → `AD-066/067`; `007` → `AD-051`; `008` → `AD-080/082/083`; `009` → `AD-077–079`; `010` → `AD-102`; `011` → `AD-002/007–010/023`; `012` → `AD-105`.

**Proposal trace — Proposal Register:** `P-API-001` → `AD-113`; `P-API-002` → `AD-114`.  
**Handoff status — Handoffs and Dependencies:** documentation pointers resolved under `AD-R002–006`; remaining security/operations implementation coverage is `AD-107`.

### 03_data.md

**Reviewed sections:** Data Inventory and Relationships; Data Field Definitions; Lifecycle and Consistency; Integration Data and Acceptance Criteria; Consistency and Open Questions.  
**Reference:** [03_data.md](03_data.md), **Open-Decision Register**.

| Existing ID | Consolidated items |
|---|---|
| OQ-DAT-001 | AD-006/019/023/070/102/107 |
| OQ-DAT-002 | AD-024/025/032 |
| OQ-DAT-003 | AD-023/027/064/109 |
| OQ-DAT-004 | AD-025 |
| OQ-DAT-005 | AD-014/030/035/058/060/109 |
| OQ-DAT-006 | AD-026/027/034–036 |
| OQ-DAT-007 | AD-030/037/067/079/081/109 |
| OQ-DAT-008 | AD-038/041/044/108 |
| OQ-DAT-009 | AD-044/047/108 |
| OQ-DAT-010 | AD-007/039–043/045 |
| OQ-DAT-011 | AD-002/042/046–050/097 |
| OQ-DAT-012 | AD-010/047/050 |
| OQ-DAT-013 | AD-009/029/068/069/074/104/109 |
| OQ-DAT-014 | AD-030–032/072/079/080 |
| OQ-DAT-015 | AD-036/054–056/059/066 |
| OQ-DAT-016 | AD-061–067/084/085/108 |
| OQ-DAT-017 | AD-008/012/015–019/045/050/086/087 |
| OQ-DAT-018 | AD-013/037/077–083/084/088/100 |
| OQ-DAT-019 | AD-005/038/050–053/083 |
| OQ-DAT-020 | AD-057/058/088/089/098/099 |
| OQ-DAT-021 | AD-014/060/064/066/108/109 |
| OQ-DAT-022 | AD-023/083/090–096 |
| OQ-DAT-023 | AD-078/079/084/092/100/108 |
| OQ-DAT-024 | AD-021–023/041/068/069/104–106/108/109 |
| OQ-DAT-025 | AD-001–014/087/098/100 |
| OQ-DAT-026 | AD-036/097/099/101–105 |

**Conflict trace — same file, Conflicts and Required Amendments:**  
`CON-DAT-001/002` → `CF-011`; `003` → `CF-012`; `004` → `CF-013`; `005/006` → `CF-029`; `007` → `CF-027`; `008` → `CF-034`; `009/010` → `CF-028`; `011` → `CF-015`; `012` → `CF-002`; `013` → `CF-003`; `014` → `CF-004/005/006`; `015` → `CF-007`; `016` → `CF-008/009/024`; `017` → `CF-010`; `018` → `CF-014`; `019` → `CF-016`; `020` → `CF-017`; `021` → `CF-018/022`; `022` → `CF-026/AD-R002`; `023` → `CF-032`.

**Proposal Status:** earlier proposals remain `AD-110–114`; no new data option is approved.  
**Handoff status — Dependencies and Later Handoffs:** batch/rule/exception/flow documentation is available; complete security/operations and production data contracts remain open.

### 04_batch_functions.md

**Reviewed sections:** Batch Inventory and Triggers; Processing by Job; Operations and Recovery; Acceptance Criteria; Consistency and Open Questions.  
**Reference:** [04_batch_functions.md](04_batch_functions.md), **Open-Decision Register**.

| Existing ID | Consolidated items |
|---|---|
| OQ-BAT-001 | AD-035/065/071/081/088 |
| OQ-BAT-002 | AD-023/070/075 |
| OQ-BAT-003 | AD-017/019–022/077 |
| OQ-BAT-004 | AD-031/049/053/072/100 |
| OQ-BAT-005 | AD-031/069/079 |
| OQ-BAT-006 | AD-029/068/069/074/104 |
| OQ-BAT-007 | AD-055/056/072–074 |
| OQ-BAT-008 | AD-076/097–099/104/105 |
| OQ-BAT-009 | AD-075 |
| OQ-BAT-010 | AD-033 |
| OQ-BAT-011 | AD-005/050–053/083 |
| OQ-BAT-012 | AD-038–043/086 |
| OQ-BAT-013 | AD-046/048–050/076 |
| OQ-BAT-014 | AD-021/022/054–060 |
| OQ-BAT-015 | AD-061–067 |
| OQ-BAT-016 | AD-013/037/079–081/100 |
| OQ-BAT-017 | AD-084/108 |
| OQ-BAT-018 | AD-058/088/089 |
| OQ-BAT-019 | AD-090–093 |
| OQ-BAT-020 | AD-082/083 |
| OQ-BAT-021 | AD-077/078 |
| OQ-BAT-022 | AD-011/092/094/095 |
| OQ-BAT-023 | AD-001/079/100 |
| OQ-BAT-024 | AD-008/012/087 |
| OQ-BAT-025 | AD-105 |
| OQ-BAT-026 | AD-001–005/013/057/098–100 |

**Conflict trace — same file, Conflicts and Required Amendments:**  
`CON-BAT-001/017` → `CF-025`; `002` → `CF-001`; `003` → `CF-002`; `004` → `CF-008`; `005` → `CF-009`; `006` → `CF-014`; `007` → `CF-015`; `008` → `CF-029/034`; `009` → `CF-012`; `010` → `CF-016`; `011` → `CF-017`; `012` → `CF-030`; `013` → `CF-004/006`; `014` → `CF-018`; `015` → `CF-024`; `016` → `CF-031`; `018` → `CF-026/AD-R006`.

**Proposal Status:** prior proposals remain `AD-110–114`; scheduler, locking, packaging, and retry alternatives are not approved.  
**Handoff status:** this file supplies logical batch/background coverage, not a complete selected scheduler or Operations Specification.

### 05_business_rules.md

**Reviewed sections:** Rule Inventory and Scope; Decisions, Calculations, and State Transitions; Application Points and Validation Conditions; Consistency and Open Questions.  
**Reference:** [05_business_rules.md](05_business_rules.md), **Open-Decision Register**.

| Existing ID | Consolidated items |
|---|---|
| OQ-BR-001 | AD-015–020/061/062/077 |
| OQ-BR-002 | AD-023–027/030/106/109 |
| OQ-BR-003 | AD-029–032/069 |
| OQ-BR-004 | AD-014/035/060/065/081 |
| OQ-BR-005 | AD-033 |
| OQ-BR-006 | AD-034 |
| OQ-BR-007 | AD-035 |
| OQ-BR-008 | AD-026/036/037/054/067 |
| OQ-BR-009 | AD-039–043 |
| OQ-BR-010 | AD-042/046/060 |
| OQ-BR-011 | AD-038/044–049/108 |
| OQ-BR-012 | AD-045/050/052/076 |
| OQ-BR-013 | AD-004/014/059/060/086/108 |
| OQ-BR-014 | AD-057/058/088/089 |
| OQ-BR-015 | AD-054–056/059/065 |
| OQ-BR-016 | AD-020–022/044 |
| OQ-BR-017 | AD-060/061/066 |
| OQ-BR-018 | AD-063/064/108 |
| OQ-BR-019 | AD-061/062/065 |
| OQ-BR-020 | AD-054/066/067 |
| OQ-BR-021 | AD-005/051–053 |
| OQ-BR-022 | AD-068/069/072–075/105 |
| OQ-BR-023 | AD-013/037/079–081/084–087/100 |
| OQ-BR-024 | AD-077–079 |
| OQ-BR-025 | AD-082/083 |
| OQ-BR-026 | AD-058/071/075/088/089 |
| OQ-BR-027 | AD-044/045/101–105 |
| OQ-BR-028 | AD-057/072/076/097–100 |
| OQ-BR-029 | AD-090–096 |
| OQ-BR-030 | AD-001–014/087/100 |

**Conflict trace — same file, Conflicts and Required Amendments:**  
`CON-BR-001` → `CF-001`; `002` → `CF-002`; `003` → `CF-003`; `004` → `CF-004/005`; `005` → `CF-006`; `006` → `CF-007`; `007` → `CF-014`; `008` → `CF-008/009`; `009` → `CF-010`; `010` → `CF-011/034`; `011` → `CF-012/028`; `012` → `CF-015`; `013` → `CF-016`; `014` → `CF-017`; `015` → `CF-023`; `016` → `CF-018`; `017` → `CF-022`; `018` → `CF-031`; `019` → `CF-033`; `020` → `CF-026/AD-R003`.

**Proposal Status:** earlier proposals remain `AD-110–114`; no priority matrix, confidence threshold, rule order, reporting formula, or retention schedule is adopted.  
**Handoff status:** exception and processing documentation availability is resolved; substantive rule gaps remain outstanding.

### 06_exception_handling.md

**Reviewed sections:** Exception Inventory and Classification; Handling by Exception; Logging, Monitoring, and Operations; Failure Acceptance Criteria; Consistency and Open Questions.  
**Reference:** [06_exception_handling.md](06_exception_handling.md), **Open-Decision Register**.

| Existing ID | Consolidated items |
|---|---|
| OQ-ERR-001 | AD-023/030/073/106 |
| OQ-ERR-002 | AD-027/033/034/064/104 |
| OQ-ERR-003 | AD-015–022/061/062/077 |
| OQ-ERR-004 | AD-030–032/036/037/104 |
| OQ-ERR-005 | AD-029/031 |
| OQ-ERR-006 | AD-068/069/074/109 |
| OQ-ERR-007 | AD-059/073–075/105 |
| OQ-ERR-008 | AD-054–059 |
| OQ-ERR-009 | AD-005/051–053 |
| OQ-ERR-010 | AD-039–043 |
| OQ-ERR-011 | AD-044–047/059/108 |
| OQ-ERR-012 | AD-014/020–022/059–065 |
| OQ-ERR-013 | AD-066/067 |
| OQ-ERR-014 | AD-045/049/050/052/076 |
| OQ-ERR-015 | AD-031/032/072/079/100 |
| OQ-ERR-016 | AD-068/104/109 |
| OQ-ERR-017 | AD-105 |
| OQ-ERR-018 | AD-013/037/079–081/100 |
| OQ-ERR-019 | AD-077–079 |
| OQ-ERR-020 | AD-082/083 |
| OQ-ERR-021 | AD-084/086/087/108 |
| OQ-ERR-022 | AD-090–096 |
| OQ-ERR-023 | AD-058/071/088/089 |
| OQ-ERR-024 | AD-019/071/076/084–087/099/105/109 |
| OQ-ERR-025 | AD-027/101–104/106 |
| OQ-ERR-026 | AD-001–014/057/098/100 |

**Conflict trace — same file, Conflicts and Required Amendments:**  
`CON-ERR-001/002` → `CF-018`; `003` → `CF-002`; `004` → `CF-019`; `005` → `CF-020`; `006` → `CF-014`; `007` → `CF-015`; `008` → `CF-021`; `009` → `CF-009/029/034`; `010` → `CF-008`; `011` → `CF-001`; `012` → `CF-004/005/006`; `013` → `CF-007`; `014` → `CF-003/016`; `015` → `CF-017/030`; `016` → `CF-016`; `017` → `CF-010/012`; `018` → `CF-023`; `019` → `CF-026/AD-R004`.

**Proposal Status:** prior proposals remain `AD-110–114`; no new error code, log level, retry value, compensation, notification recipient, or recovery control is adopted.  
**Handoff status:** processing documentation is now available; remaining security/nonfunctional/operational contracts remain `AD-107`.

### 07_processing_flows.md

**Reviewed sections:** Flow Inventory and Prerequisites; Normal Processing; Branches, Failures, and Recovery; Flow Diagrams and Specification Mappings; Acceptance Criteria; Consistency and Open Questions.  
**Reference:** [07_processing_flows.md](07_processing_flows.md), **Open-Decision Register**.

| Existing ID | Consolidated items |
|---|---|
| OQ-FLOW-001 | AD-015–020/061/062/077/085 |
| OQ-FLOW-002 | AD-023/024/027/028/030/106/109 |
| OQ-FLOW-003 | AD-029–032/069/072 |
| OQ-FLOW-004 | AD-027/033/111 |
| OQ-FLOW-005 | AD-034/035 |
| OQ-FLOW-006 | AD-038–043 |
| OQ-FLOW-007 | AD-038/044–050/059/108 |
| OQ-FLOW-008 | AD-054/057/067 |
| OQ-FLOW-009 | AD-055–058/072 |
| OQ-FLOW-010 | AD-014/059/060/066/112 |
| OQ-FLOW-011 | AD-061–065/108 |
| OQ-FLOW-012 | AD-066/067 |
| OQ-FLOW-013 | AD-026/036/037/054/067 |
| OQ-FLOW-014 | AD-005/051–053/083 |
| OQ-FLOW-015 | AD-045/047/049/050/052/076 |
| OQ-FLOW-016 | AD-021/022/063/068/069/105/109 |
| OQ-FLOW-017 | AD-028/036/068/101–104/110–112 |
| OQ-FLOW-018 | AD-069/072–076/105 |
| OQ-FLOW-019 | AD-082/083 |
| OQ-FLOW-020 | AD-031/075/077–079 |
| OQ-FLOW-021 | AD-013/037/071/079–081/100 |
| OQ-FLOW-022 | AD-018/084–087/108 |
| OQ-FLOW-023 | AD-057/058/071/088/089/099 |
| OQ-FLOW-024 | AD-090–096 |
| OQ-FLOW-025 | AD-001–014/057/087/098/100 |
| OQ-FLOW-026 | AD-006/023/070/075/088/101–107 |

**Conflict trace — same file, Cross-Specification Conflicts and Required Amendments:**  
`CON-FLOW-001` → `CF-001`; `002` → `CF-002`; `003` → `CF-003`; `004` → `CF-004/005/006/033`; `005` → `CF-007`; `006` → `CF-008`; `007` → `CF-009`; `008` → `CF-011/034`; `009` → `CF-012/028`; `010` → `CF-010`; `011` → `CF-014`; `012` → `CF-015`; `013` → `CF-019/020/021`; `014` → `CF-033/034`; `015` → `CF-016`; `016` → `CF-024`; `017` → `CF-018`; `018` → `CF-022`; `019` → `CF-025/031`; `020` → `CF-017`; `021` → `CF-023`; `022` → `CF-026/AD-107/AD-R001–006`.

**Proposal Status and Dependencies:** earlier proposals remain `AD-110–114`; flow diagrams do not approve missing choices. Stage 8 is consolidation, not an additional completed security or operations design.

### Missing Evidence and Required Confirmation Material

The supplied specifications establish constraints but do not provide the following complete confirmation material. These are requested evidence categories, not claims that such evidence has been inspected or that a particular approval process has been selected.

| Confirmation material needed | Related items | Acceptance boundary |
|---|---|---|
| Explicit approved provider/deployment/region/retention/key decisions | AD-001–014 | A placeholder, repeated example, or proposed configuration is insufficient. |
| Complete role/action/resource/service and independent-approval contracts | AD-015–022/061/062/077 | Named roles and navigation alone do not establish grants. |
| Repository-controlled REST/RPC/job/event/data schemas | AD-023–032/038–045/063/064/068/069/108/109 | Selected fields and proposed JSON are not complete IDL. |
| Approved calculation, state, lifetime, and concurrency contracts | AD-033–037/042/046–060/065–067/079–083/088–091 | Missing formulas, comparison boundaries, or race ordering cannot be guessed. |
| Protected operational, scheduler, resilience, release, and recovery contracts | AD-070–076/084/087/094–100 | Logical functions/runbooks do not establish commands, executables, numeric settings, or appointed operators. |
| Approved UI organization, presentation, and notification contracts | AD-101–105/110–114 | Illustrations and proposals do not establish routes, controls, summaries, channels, or defaults. |
| Complete error and security-exit evidence | AD-093/106/107 | Known examples and identifier ranges do not define all errors or individual security controls. |

If confirmation requires original-source reconciliation, obtain an explicit confirmed amendment or decision and then update affected Markdown requirement IDs through controlled change. Such verification remains pending; this register does not perform it.

### Confirmation Order Implied by Dependencies

This is a dependency order, not a deadline or assignment. Independent subjects may be confirmed in parallel.

1. **Establish approved authority and deployment boundaries:** provider/residency/key/retention choices and identity/role/service grants (`AD-001–022`). These constrain external routing, source access, tooling, and destructive operations.
2. **Define formal contracts and identities:** IDL, physical relationships, revision/idempotency, transaction/RLS, hashes, versions, and attribution (`AD-023–032/038/044/068/069/108/109`).
3. **Confirm business calculations and lifecycle guards:** classification, priority/calendar, quality/retrieval, policy, review, publication, and exit/hold scope (`AD-033–067/077–083`). Do not implement approval or purge mechanics before their binding and race contracts.
4. **Realize execution and recovery:** worker/scheduler/claim/retry/replay, reconciliation, audit/rotation, release, and recovery mechanics (`AD-070–076/084/087/094–100`) using the confirmed contracts above.
5. **Bind screens, reporting, and notifications:** approved routes, fields, summaries, source inspection, usage/evaluation presentation, and safe recovery UX (`AD-088–093/101–106/110–114`). Source inspection must be usable before approval; status displays must reflect authoritative completion.
6. **Finalize executable acceptance evidence:** resolve empty/partial/boundary assertions, statistical calculations, SLO measurement, individual security exit controls, and signed release evidence (`AD-075/091–100/106/107`).
7. **Record controlled amendments and close narrowly answered items:** preserve original identifiers, cite the confirming Markdown section/requirement or approved amendment, update stale handoff pointers without rewriting specifications in this consolidation, and leave unrelated portions open.

Until that evidence exists, the relevant items remain on hold. Confirmed safety, authorization, durability, truthful-status, and scope restrictions continue to apply throughout.
