# Phase 4 — Uncertified Generated-Claim Evidence Review Queue

Uncertified low-confidence source-support classifications: **3,973 of 5,888 raw classes**.

Priority examples with explicit operational wording: **679** (not certified FP findings).

The provisional status `SUPPORTED_NONCOVERING` must not be treated as proof that the entire generated claim is PDF-entailed. The Phase-5 audit must either supply complete affirmative source evidence, correct extraction eligibility, or materialize a distinct unsupported canonical proposition `F_m` with actual generated and PDF evidence.

| Class | Generated source | Generated proposition excerpt | PDF candidate |
|---|---|---|---|
| `GCLASS-00002` | `01_screen_functions(1).md:35` | Evidence-based research: Search only permitted knowledge, inspect cited source versions, and follow citations to st | PDF p.32; retrieval 0.301 |
| `GCLASS-00038` | `01_screen_functions(1).md:70` | Retrieval must apply source ACLs before releasing text to generation. | PDF p.36; retrieval 0.282 |
| `GCLASS-00055` | `01_screen_functions(1).md:104` | Case Detail; illustrated title `Case Detail / Resolution Package`: Analyst/Reviewer may read authorized cases; edit | PDF p.83; retrieval 0.216 |
| `GCLASS-00068` | `01_screen_functions(1).md:107` | Review Inbox; illustrated title `Approval Inbox / Binding Decision`: Source evidence must be inspectable before dec | PDF p.59; retrieval 0.264 |
| `GCLASS-00090` | `01_screen_functions(1).md:124` | AI artifacts use accessible text labels `DRAFT`, `NEEDS_REVIEW`, or `PUBLISHED`. Styling alone must not convey stat | PDF p.57; retrieval 0.320 |
| `GCLASS-00100` | `01_screen_functions(1).md:143` | The following profiles apply only where referenced by a field row: | PDF p.19; retrieval 0.238 |
| `GCLASS-00103` | `01_screen_functions(1).md:147` | D — Authorized display: Read-only presentation. | PDF p.59; retrieval 0.186 |
| `GCLASS-00104` | `01_screen_functions(1).md:147` | D — Authorized display: Resource authorization and applicable version/anchor checks occur on fetch and before displ | PDF p.70; retrieval 0.228 |
| `GCLASS-00105` | `01_screen_functions(1).md:147` | D — Authorized display: Show only within authorized resource scope. | PDF p.39; retrieval 0.213 |
| `GCLASS-00112` | `01_screen_functions(1).md:151` | Exact types are only marked confirmed where supplied by the source. | PDF p.46; retrieval 0.164 |
| `GCLASS-00123` | `01_screen_functions(1).md:172` | When Case revision conflict: HTTP `409`, `CASE_VERSION_CONFLICT`, current revision; canonical details may include ` | PDF p.84; retrieval 0.306 |
| `GCLASS-00128` | `01_screen_functions(1).md:174` | When Invalid request schema: HTTP `422`. | PDF p.54; retrieval 0.201 |
| `GCLASS-00130` | `01_screen_functions(1).md:175` | When Quota/admission throttling: HTTP `429`; run admission includes `Retry-After`. | PDF p.28; retrieval 0.163 |
| `GCLASS-00142` | `01_screen_functions(1).md:180` | When Stale approval artifact: HTTP `409` is listed | PDF p.45; retrieval 0.201 |
| `GCLASS-00150` | `01_screen_functions(1).md:193` | Workspace name: Must match authorized workspace scope | PDF p.26; retrieval 0.288 |
| `GCLASS-00152` | `01_screen_functions(1).md:194` | Tenant/release indicator: Must not enable tenant switching by editing displayed text | PDF p.11; retrieval 0.118 |
| `GCLASS-00153` | `01_screen_functions(1).md:196` | `AWAITING REVIEW`: Must not infer task counts from unrelated case/run states | PDF p.82; retrieval 0.259 |
| `GCLASS-00155` | `01_screen_functions(1).md:198` | `SERVICE STATE`: Must reflect authoritative health/degraded state, not assume healthy | PDF p.19; retrieval 0.146 |
| `GCLASS-00161` | `01_screen_functions(1).md:213` | Case identifier: Validate tenant/resource scope on list retrieval and case opening | PDF p.12; retrieval 0.150 |
| `GCLASS-00164` | `01_screen_functions(1).md:215` | Case/workflow status summary: Use accessible text; state mapping must be resolved before implementation | PDF p.57; retrieval 0.200 |
| `GCLASS-00168` | `01_screen_functions(1).md:221` | Open Case Queue with authorized context: Apply SCR-COM-011; never expose unauthorized rows | PDF p.84; retrieval 0.152 |
| `GCLASS-00178` | `01_screen_functions(1).md:224` | case entry: Unauthorized creation must be rejected by server | PDF p.12; retrieval 0.195 |
| `GCLASS-00211` | `01_screen_functions(1).md:261` | Attachment/document status: `READY` must not be claimed before indexing/quality conditions are met | PDF p.82; retrieval 0.166 |
| `GCLASS-00213` | `01_screen_functions(1).md:263` | Draft request/business context: Input validation before run allocation and tool/model processing | PDF p.30; retrieval 0.240 |
| `GCLASS-00217` | `01_screen_functions(1).md:271` | Candidate artifact: Must be distinguished from approved result; invalid output must not publish | PDF p.45; retrieval 0.195 |
| `GCLASS-00220` | `01_screen_functions(1).md:273` | Source citations: Verify before display | PDF p.35; retrieval 0.262 |
| `GCLASS-00223` | `01_screen_functions(1).md:274` | Model version/deployment metadata: Must identify the actual approved route used | PDF p.37; retrieval 0.228 |
| `GCLASS-00233` | `01_screen_functions(1).md:280` | Verified citation count: Count only verified citations under the defined verification contract | PDF p.35; retrieval 0.220 |

These examples are risks to audit, **not** evidence of implemented or invented capabilities.
A low similarity score is not proof of PDF non-entailment; a high score is not proof of full normative equivalence.
