# 2-Level Hierarchical MapReduce Specification Generation

Upload a PDF or PPTX file (up to 50 MiB) to `POST /upload` to generate seven specifications and a TBD register through the OpenAI Responses API. Stages 01–07 use source files through `input_file`; stage 8 uses only their completed Markdown. All eight generated documents, including titles, headings, and explanatory text, use English Markdown; server logs are in English.

## Setup

Use Python 3.11 or later in an activated virtual environment. From the repository root, enter this backend directory and install its dependencies and Gunicorn:

```bash
cd experiment/twolevel_mapreduce/be
python -m pip install -r requirements.txt
python -m pip install gunicorn
```

Create or edit `.env` in this `be/` directory:

```dotenv
API_KEY=replace-with-a-backend-api-key-at-least-32-characters
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=replace-with-your-azure-openai-key
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=your-deployment-name
APP_ENV=development
LLM_MAX_OUTPUT_TOKENS=128000
LLM_INTERMEDIATE_MAX_OUTPUT_TOKENS=64000
```

`API_KEY` authenticates requests to this backend and must contain at least 32 characters. It is separate from `AZURE_OPENAI_API_KEY`, which authenticates the development backend to Azure OpenAI. The application loads `.env` automatically at startup.

`AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` is accepted as a fallback deployment setting. When `APP_ENV` is `prod`, `production`, or `staging`, the backend uses Microsoft Entra ID through managed identity; `AZURE_CLIENT_ID` can select a user-assigned identity. The current startup validation still requires `AZURE_OPENAI_API_KEY` to be set. Choose a deployment that supports Responses API file input, JSON output, and background execution for the document types you use.

## Start the server

Run this exact command from `experiment/twolevel_mapreduce/be/`:

```bash
gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app --bind localhost:8001 2>&1 | tee ../../../_test_twolevel-20261108.log
```

The server listens on `http://localhost:8001`. Both standard output and standard error are displayed in the terminal and written to `_test_twolevel-20261108.log` in the repository root. `tee` overwrites that log on each run. All three backend examples use the same port, so run one at a time on this address.

## POST a document with curl

Open a second terminal in `experiment/twolevel_mapreduce/be/`. Set the client-side `API_KEY` to the same value configured in the backend's `.env`; the server's automatic `.env` loading does not export it into this terminal.

```bash
export API_KEY='replace-with-a-backend-api-key-at-least-32-characters'
```

Upload a PDF using the multipart form field named `file`:

```bash
curl --fail-with-body --show-error \
  --request POST 'http://localhost:8001/upload' \
  --header "Authorization: Bearer ${API_KEY}" \
  --form 'file=@/absolute/path/document.pdf;type=application/pdf'
```

For a PowerPoint presentation, use the same endpoint with a PPTX file:

```bash
curl --fail-with-body --show-error \
  --request POST 'http://localhost:8001/upload' \
  --header "Authorization: Bearer ${API_KEY}" \
  --form 'file=@/absolute/path/document.pptx;type=application/vnd.openxmlformats-officedocument.presentationml.presentation'
```

Replace the example path with your document path. `curl --form` sets the multipart content type and boundary. The command prints the API response in the terminal. The request remains open until all eight documents finish. The backend saves each completed Markdown file and a `checkpoint.json` under top-level `res/` before starting the next stage. Follow the server log for progress.

## Resume an interrupted run

Send the same source document to `POST /upload` with `resume_from` set to the run directory's **name**, for example `twolevel_20261111082915_iqz55pk5`. Find this name in `Stage output saved` logs or the successful response's `run_id`. Paths and run IDs from other backends are rejected.

```bash
curl --fail-with-body --show-error \
  --request POST 'http://127.0.0.1:8001/upload' \
  --header "Authorization: Bearer ${API_KEY}" \
  --form 'file=@../../../dataset/OrionDesk_AI_Detailed_Design_Specification.pdf;type=application/pdf' \
  --form 'resume_from=twolevel_20261111082915_iqz55pk5'
```

For runs created **before this feature**, add `--form 'allow_legacy_resume=true'`. Such runs contain only Markdown. This explicit import assumes you supply the original source and compatible generation settings: their original input, settings, global context, and approval history cannot be verified. Imported stages are listed in `resume.unverified_stages`, including on subsequent resumes. Their token usage and elapsed time remain `null`. If stages 01–07 are not all complete, the global context is generated again. A malformed checkpoint never falls back to legacy import.

The completed specifications must form a contiguous prefix starting at 01. If 01–04 are complete, they are loaded as previous specifications and generation begins at 05. The failed specification starts from its beginning; partial Map or chapter results within it are not reused. If only 08 remains, only the Markdown synthesis call runs, with no source splitting, global-context call, Map, reduction, or approval. A fully completed run makes no model calls. The file upload is still required for source identity verification.

Each resume creates a **new output directory**, copies the completed prefix there before generation, and leaves the original directory untouched. Repeated failures can be resumed using the latest directory's run ID. No running server is restarted and no resume is started automatically. After an existing server has finished its work, start the updated program to use the feature; an already running old process keeps its old behavior. Avoid launching a second analysis against the same deployment while the existing run is active if it would compete for quota. The per-process busy gate also applies to resume requests.

New runs save a checkpoint after each completed specification. It records the source hash, code/prompt/dependency-file fingerprint, non-secret generation-settings fingerprint, Markdown hashes, completed-stage metadata and audits, chunk layout, global context, and resume ancestry. Model deployment/endpoint and the configured generation/splitting limits must match; even changes to explicit/default setting representations are conservatively rejected. Authentication secrets and port settings are excluded. Changing a deployment's underlying model without changing its name cannot be detected. Modified, missing, empty, or unapproved checkpoint outputs are rejected. Legacy imports can check filenames, contiguity, encoding, size, and nonempty content, but cannot establish semantic correctness or prior approval.

Checkpoint replacement is the stage commit marker. A write failure preserves the previous checkpoint and completed files; Markdown beyond the committed prefix after a process interruption is ignored on resume. Corrupt checkpoints are errors, not permission to skip stages. Resuming a modified earlier specification requires a new run because later specifications depend on it.

`usage_scope=completed_stages_and_global_context` means aggregate usage covers the retained completed stages and global context, including recorded retries within those stages. It does **not** include abandoned work in a failed stage from a previous request and is not total billed usage across interruptions. `timing_ms` measures the current request; reused specifications retain their original `elapsed_ms` when known. `resume.history` lists the source runs, and `resume.reused_stages` identifies stages reused by this request.

Invalid resume data returns `400`, a missing run returns `404`, and an identity mismatch or legacy run without explicit import returns `409`, before model generation. Authentication and busy responses remain `401` and `503`.


## Generated specifications

The backend generates these eight documents in order. Each stage renders its own prompt and receives all previously completed specifications to preserve terminology, identifiers, and consistency. The prompts distinguish confirmed source facts, design proposals, and matters requiring confirmation. A category with missing source information still receives a specification describing the gaps.

| Step | Key | Specification | Dedicated prompt |
| --- | --- | --- | --- |
| 1 | `screen_functions` | Screen Function Specification | `prompt/stages/screen_functions.jinja2` |
| 2 | `api` | API Specification | `prompt/stages/api.jinja2` |
| 3 | `data` | Data Specification | `prompt/stages/data.jinja2` |
| 4 | `batch_functions` | Batch Function Specification | `prompt/stages/batch_functions.jinja2` |
| 5 | `business_rules` | Business Rules | `prompt/stages/business_rules.jinja2` |
| 6 | `exception_handling` | Exception Handling Specification | `prompt/stages/exception_handling.jinja2` |
| 7 | `processing_flows` | Processing Flow Specification | `prompt/stages/processing_flows.jinja2` |
| 8 | `architecture_decision` | Architecture Decision Register | `prompt/stages/architecture_decision.jinja2` |

The final document keeps the filename `08_architecture_decision.md` and serves as a TBD register. It uses only the completed Markdown specifications 01–07. Items answered consistently by explicit confirmed statements are marked resolved with links to the relevant files, sections, and requirement IDs. Remaining questions, unadopted proposals, and contradictory statements stay open with their impact and questions to confirm. The model does not select design options or invent decisions. Supply all eight Markdown files together to an implementation AI.

Stage 8 makes one direct Markdown-generation call after stage 7 succeeds, with no source attachment, Map evidence, global context, chunk scan, reduction, or approval call. It uses the shared Responses client's processing and deadline retries. Its token usage and elapsed time are included in the eighth specification and overall totals. If it fails or is cancelled, the seven completed Markdown files remain available.

Stage 8 uses `LLM_MAX_OUTPUT_TOKENS` (default and maximum 128000), `LLM_MAX_QUERY_BYTES` (default 8 MiB, maximum 32 MiB), and `LLM_FINAL_MAX_BYTES` (default 1 MiB, maximum 16 MiB). The latter two limits measure the UTF-8 query and Markdown body; exceeding either fails without truncating the specifications. A blank response is not accepted as a completed document.

## Processing model

This backend implements **2-level hierarchical MapReduce**. The depth counts adjudication layers above the leaf chunks. Context generation and the separate final approval call do not add reduction layers. This workflow applies to specifications 01–07; stage 8 uses the Markdown synthesis described above.

```text
Root (document) -> Onelevel forks (chapters) -> Map leaves (sections or section parts)
Reduction: section evidence -> chapter judgments -> root candidate -> root approval
```

1. Split the original file once. For PDFs, use top-level bookmarks (or prominent numbered chapter headings) as chapters. Detect numbered section headings such as `5.2` from text, font size, and alignment; nested bookmark boundaries are also retained. Sections and chapter introductions become separate Map leaves. Large sections are divided into parts under the same chapter fork. PowerPoint keeps its existing native-section and slide-size behavior, retaining images, notes, and layouts.
2. Send the original file and chunk manifest to an initial LLM call for global context and chapter meanings. The server requires exactly one fork per detected `chapter_id`, containing every section and part of that chapter in order. Front matter and appendices remain explicit scopes. Without chapter metadata, native sections or source-grounded semantic jurisdictions remain the fallback.
3. The root creates a context for the current specification. Each intermediate adjudicator then creates a subglobal context for its own chapter or section and distributes it to its leaf workers together with the global and root contexts.
4. **Read every chunk for each of specifications 01–07 and every attempt.** Each leaf returns original page or slide numbers, source excerpts, scope, evidence strength, conditions, exceptions, and gaps as JSON. The server assigns evidence IDs.
5. Each chapter fork adjudicates all its leaf records. If its input is too large, it processes bounded batches and merges their judgments within that same fork; a final call checks conditions, exceptions, and contradictions across batches. This adds calls, not a third tree level. The root receives these adjudicative outcomes and examines relations across jurisdictions to produce the current specification candidate. Judgments consider support, contradiction, qualification, and exception using provenance, evidence strength, applicability, and global consistency. The prompts prohibit majority voting.
6. Make a separate root approval call with a complete chunk/finding checklist. It checks the candidate against all original leaf evidence, coverage records, context, and any intermediate judgments. Uncertainty and unresolved conflicts must remain explicit. An otherwise valid review with missing, duplicate, or unknown IDs is retried against the same candidate and evidence, up to three review attempts by default.
7. If rejected, distribute actionable feedback, regenerate that specification's contexts, and **reprocess every chunk**. The default limit is eight complete attempts, including the initial scan. Advance to the next specification only after approval; persistent rejection stops the request with an error.

When each chapter fits a single reduction call, and there are no rejections, Map timeouts, Map strength repairs, response processing or deadline retries, decision identifier or relation repairs, or approval coverage retries, the number of LLM response-creation calls is `1 + 7 * (N + 2G + 3) + 1`. Here, N is the number of leaf chunks and G is the number of semantic jurisdictions. The initial call creates global context; the final extra call generates the TBD register from Markdown. Each of stages 01–07 adds root context, root candidate generation, and root approval, plus G subglobal-context calls and G intermediate adjudication calls. Batched chapter reductions, polling, and SDK transport retries add to this count.

A review with invalid coverage receives the exact missing, duplicate, and unknown chunk/finding IDs and its previous response on the next review call. All three ID error types share `LLM_MAX_APPROVAL_REVIEW_ATTEMPTS` (three calls total by default); changing error types does not reset the allowance. The prompt requires a complete new review of the same candidate and evidence, including any previously identified concerns. Completed Maps, reductions, contexts, and earlier specifications are reused. Each review uses the client's 1200-second deadline attempts and deadline retries.

The backend never fills missing IDs, removes duplicates, or substitutes unknown IDs automatically. Coverage counts include only distinct allowed IDs, and approval requires every allowed ID exactly once. Chunk IDs identify leaves, not page numbers or chapters. Exhausting `LLM_MAX_APPROVAL_REVIEW_ATTEMPTS` fails the request. Invalid JSON, malformed fields, incorrect ID types, and exceeded budgets remain fatal; this repair loop does not handle API errors. A valid review that rejects the candidate still triggers the full rescan in step 7.

Approval requires English prose, headings, table labels, and diagram labels, and accepts a usable draft that preserves the source-supported core behavior, material conditions, and exceptions for the current stage. Documented source gaps (`Needs confirmation`), unresolved alternatives, labeled proposals (`Proposal`), later-stage dependencies (`To be defined in a later stage`), and minor editorial or citation-format issues are non-blocking. Findings outside the current stage must be reviewed for relevance but need not all be repeated in its Markdown body.

Rejection requires a material, source-grounded defect that would mislead implementation or testing, such as omitted core behavior, an incorrect exception, or an invented confirmed requirement. Each rejection must identify the source IDs/locations, the candidate's defect, its impact, and the smallest correction. Approved reviews may contain optional suggestions in `feedback`; these are retained in the audit and do not trigger a rescan. Complete evidence coverage remains required, and persistent material rejection still fails the request.

## PDF chapters, sections, and large inputs

The logical tree is `root -> chapter forks -> section/part leaves`. A large section can produce `5.2 part 1`, `5.2 part 2`, and so on, all at the leaf level under chapter 5. Chapter introductions receive their own leaf. Parts retain the same `section_id`, distinct `part` values, and original page coordinates. Multiple sections on a page become separate cropped PDFs; out-of-region text operators are cleared because a crop box alone leaves hidden text extractable. Graphics and fonts remain in the PDF. Source evidence includes its assigned region's `bottom` and `top` coordinates in the original PDF coordinate system. `covered_units` refers to assigned regions of those original pages, not to full-page reading by each individual worker.

PDF splitting first respects section boundaries, then page limits and a source token estimate. Oversized regions prefer subsection headings and paragraph gaps, then complete text lines; cells sharing a text baseline stay together. Cuts through detected image rectangles are avoided. Continuation parts carry limited opening text and preceding bold headings/table labels with source page numbers as interpretation context, not as new evidence. This is a layout heuristic, not general table recognition. A single indivisible line or figure that cannot fit causes a clear HTTP 413 rather than losing content.

Heading detection requires extractable text and consistent numbered headings/font styles. Repeated, unordered, or misaligned section headings are treated conservatively. A chapter containing rotated pages, Form XObjects, tagged replacement text, or unsupported text transforms uses native outline/page boundaries instead of inferred numbered sections. Annotations intersecting a cropped region are retained. Scans have no OCR fallback. Native bookmarks still guide page splitting; documents without reliable chapter/section structure retain page chunks and semantic grouping. These fallbacks are not presented as exact section cuts.

For the included 90-page OrionDesk PDF, default settings detect 110 numbered sections and produce 142 leaves under 31 scopes: the 22 numbered chapters plus front matter and other bookmarked divisions. Tests check that all original page regions and extracted non-whitespace characters survive exactly once. Finer sections increase the number of Map calls; specifications 01–07 each scan all leaves, while stage 8 uses only their completed Markdown.

Large chapter inputs are batched based on the serialized child records and the fully rendered query, including global/root/chapter context and previously generated specifications. A large leaf result can be partitioned by individual findings and gaps for chapter judgment without changing the Map leaves. All original scans and every intermediate judgment remain in the audit. Every call validates its input finding IDs; final chapter output must retain the entire chapter's ID set. A final merge checks relationships across batches. Oversized individual records, fixed context that already exceeds the budget, lack of compression progress, or exhaustion of the round limit stop with an explicit error.

Token estimates use UTF-8 text length divided by three, rounded up, plus the configurable visual allowance per PDF region. They are estimates, not model token counts; visual processing varies by deployment. Set optional Map/chapter input ceilings to your model's usable context **after reserving the requested output tokens**. The Map check includes the source estimate and continuation context. If prior specifications alone leave too little room, reduce input/context size or adjust the deployment budget; they are not silently truncated. Without an optional token ceiling, the existing full-query byte ceiling still applies. Initial global-context and root calls retain their existing limits; chapter batching does not make those calls unbounded.

## Level 1 and level 2 concurrency

Configure the two levels independently in `.env`:

```dotenv
# Chapter contexts and aggregation calls, shared across all chapters
LLM_MAX_PARALLEL_LEVEL1_REQUESTS=16
# Leaf Map calls, shared across all chapters
LLM_MAX_PARALLEL_LEVEL2_REQUESTS=16
```

Level 1 covers `onelevel_context` and `onelevel_reduce`, including every chapter
aggregation batch and final chapter merge. Its limit applies across all chapters
and batches in the analysis. Level 2 covers `map` requests with a separate limit.
Both settings accept 1–16 concurrent requests. Each independently falls back to
`LLM_MAX_PARALLEL_CHUNK_REQUESTS` when unset, blank, or invalid; that legacy setting
defaults to 16. An explicit level setting takes precedence over the legacy value.

Within each chapter, batches in the same aggregation round run concurrently under
the level 1 limit. The next round or final chapter merge waits for every batch in
the current round. Results and audit history retain source order regardless of
completion order. A batch failure cancels and awaits its siblings, and the chapter
does not merge a partially completed round. Batching preserves the two-level tree.

The eight documents run sequentially, with each stage receiving the earlier
completed specifications. Within each stage, chapter contexts finish before Map
starts. Each chapter starts aggregation once all of its own Maps have succeeded,
while other chapters may still be scanning. Root reduction waits for every Map
and chapter aggregation to succeed; approval still reviews the complete original
leaf evidence. A Map or chapter failure cancels and awaits the remaining work,
without advancing to Root or saving a partial specification. Inputs and retained
results keep source order. Root calls remain sequential. The Responses client's
shared capacity remains the larger of the two level limits, including when Maps
and chapter aggregation overlap; the limits are not added together. A smaller
legacy value cannot throttle an explicit level setting. Restart the backend after
changing the settings. The scan-start log reports both effective limits.

## Separate reduction prompts

The root and each chapter fork use dedicated prompts for evidence-based semantic judgment and summary integration. `root` names the final reduction level; `onelevel` names the chapter level immediately below the root, whose children are Map workers.

| Role | Semantic judgment | Summary integration |
| --- | --- | --- |
| Each onelevel chapter fork | [hierarchy_onelevel_judgment.jinja2](prompt/hierarchy_onelevel_judgment.jinja2) | [hierarchy_onelevel_summary.jinja2](prompt/hierarchy_onelevel_summary.jinja2) |
| Root | [hierarchy_root_judgment.jinja2](prompt/hierarchy_root_judgment.jinja2) | [hierarchy_root_summary.jinja2](prompt/hierarchy_root_summary.jinja2) |

Semantic judgment populates `decisions`, `relations`, and `gaps` using evidence strength, provenance, scope, conditions, and exceptions. Forks examine their original leaf findings and excerpts. The root examines the forks' decisions and evidence-based rationales across sections; `source_index` supplies citation locations, while the separate approval call receives the original leaf evidence.

Summary integration follows those judgments and populates `summary`, plus `body` at the root. It preserves qualifications and unresolved alternatives and must not introduce unsupported decisions. Each fork uses the same pair of templates with its own jurisdiction, subglobal context, and child evidence.

`hierarchy_onelevel_reduce.jinja2` and `hierarchy_root_reduce.jinja2` compose the corresponding pair of prompts and define the output schema. `hierarchy_onelevel_context.jinja2` supplies the chapter context prompt. Each reduction call contains both prompts; large chapters can require several calls within their fork. The separate prompt files allow the two responsibilities to be edited independently.

## Map timeouts, retries, and progress

Each leaf Map request has a **300-second deadline**, starting after it acquires a hierarchy concurrency slot. This includes response creation, polling, SDK transport retries, and response processing retries. A timeout cancels the local request and retries the same chunk up to **three additional times**, for at most four Map attempts when only timeouts occur. Strength repairs have a separate allowance, described below. The slot is released between Map attempts so queued chunks can proceed.

Root aggregation (`root_reduce`) and fork aggregation (`onelevel_reduce`) each use the Responses client's **1200-second deadline**. Context generation and approval also use that limit. Waiting for all Map tasks to finish has no batch-wide 300-second deadline; the 300-second limit applies separately to each leaf request.

When a background response ID is known, the client also requests remote cancellation, with a separate five-second cleanup limit and no transport retries. Remote cancellation is best effort; if submission has not returned an ID or cancellation fails, the remote job may still finish. The fourth Map timeout fails the scan, cancels sibling tasks, and prevents reduction of partial evidence. Caller cancellation, invalid evidence, and other errors do not trigger these timeout retries.

Each successfully validated chunk advances the completion counter exactly once:

```text
Map completed 30/31: file_name=sample.pdf step=1/8 stage=screen_functions attempt=1 chunk=31 request_attempt=1
Map request timed out: file_name=sample.pdf step=1/8 stage=screen_functions attempt=1 chunk=8 timeout_s=300 retry=1/3
Map completed 31/31: file_name=sample.pdf step=1/8 stage=screen_functions attempt=1 chunk=8 request_attempt=2
```

The counter follows completion order and resets for each specification and each full-scan approval attempt. `attempt` identifies the approval attempt, `request_attempt` identifies the request for that chunk, and `retry` reports timeout retries. Timed-out requests do not advance progress or duplicate retained findings. Because they may consume unreported tokens, token counts in their specification's usage and aggregate usage become `null`; usage for unaffected specifications remains available.

## 1200-second deadline retries

When the Responses client's **1200-second deadline expires**, it resubmits the
identical request up to **three additional times**, giving each retry a fresh
1200-second deadline. The fourth deadline expiry raises `ElapsedTimeException` and
stops the request. This applies to context generation, Root reduction and approval,
chapter aggregation where present, full-file specification generation, and TBD synthesis.

Before retrying, the client attempts to cancel the latest known active background
response, with a separate five-second cleanup limit. Cancellation is best effort;
a job whose ID was not returned cannot be cancelled. The prompt, instructions,
attachment, output token limit, and output format are reused. Only the affected
request is resubmitted; completed Maps, chapter results, and earlier specifications
are not regenerated. These retries do not consume semantic approval or content
repair attempts. Caller cancellation stops immediately without starting another
request.

Deadline retries and API processing-error retries have independent allowances of
three additional retries each. Neither counter resets the other. Processing-error
retries share the current deadline; only deadline expiry starts a new 1200-second
window. Mixed failures therefore allow at most seven response submissions and four
deadline windows. The deadline windows total at most 4800 seconds, plus bounded
cancellation cleanup and any wait for a concurrency slot. An SDK HTTP timeout that
occurs before the deadline retains the SDK's existing retry behavior and does not
trigger this deadline retry loop.

If any deadline expires, token usage for the affected request, specification, and
aggregate result is reported as `null`, since the expired attempt may have consumed
unreported tokens. Usage for unaffected specifications remains available.
`Responses deadline exceeded` logs the response ID, `timeout_s`, `deadline_attempt`,
`retry`, and `timeout_retries_exhausted`. Submission, polling, and completion logs
include `response_attempt` and `deadline_attempt`; `elapsed_s` covers the entire
client call, including retries and cleanup.

The MapReduce leaf **300-second deadline and three timeout retries remain
unchanged**. A leaf deadline cancels the client call and is handled by the Map
retry loop; it does not start a 1200-second retry inside that call.

## Response processing retries

All phases retry a terminal `status=failed` response for `server_error`, `rate_limit_exceeded`, or `vector_store_timeout`. A code-less Azure error is also retried when its message starts with "An error occurred while processing your request." and explicitly says "You can retry your request". Known permanent errors and unknown codes stop immediately; the message fallback never overrides a supplied code. Incomplete responses (including `max_output_tokens`), cancellation, and invalid generated content are not retried by this mechanism.

For processing failures, the client resubmits the identical request up to **three additional times** (four submissions if no deadline expires), with waits of **2, 4, and 8 seconds**, each plus 0–1 seconds of jitter. Submission, polling, SDK HTTP retries, and these processing retries share the current **1200-second deadline attempt**. A deadline retry starts a fresh window as described above; SDK transport retries remain separate.

Retry logs include the failed response ID, error code, `retry=1/3`, delay, and elapsed time. Submission and polling logs include `response_attempt`; exhaustion logs include `processing_retries_exhausted=True`. Token usage includes failed submissions when all attempts report complete usage; otherwise the affected request, specification, and aggregate usage become `null`. Usage for unaffected specifications remains available.

For Root approval, a processing retry reuses the candidate, evidence ledger, and review payload. It does not rerun Map, regenerate the candidate, consume another coverage-review attempt, or restart an earlier specification. The leaf Map deadline remains **300 seconds across processing retries within each Map attempt**; Root and fork calls use 1200 seconds per deadline attempt, with up to three deadline retries. A Map timeout can start a new Map attempt with its own processing-retry allowance. Semantic approval and evidence validation remain separate.

## Map strength validation and repair

Every finding must include `strength` as exactly `explicit`, `inferred`, or
`uncertain`. If an otherwise valid Map response omits this field or returns a
different value or type, only that chunk is retried with `strength_repair`
diagnostics and the same attachment, contexts, and specification instructions.
The model re-evaluates the evidence and returns a complete Map record. The backend
does not guess or normalize the strength. Successful chunks and earlier stages
are reused, and progress advances only after the replacement passes validation.

There are **up to two strength repairs** (the initial response and two corrections).
Timeouts have a separate allowance of three retries per chunk and full-scan
attempt; neither counter resets the other. With both failure types, there are
at most six Map requests, each with its own 300-second deadline. The fourth timeout
or third invalid strength response stops the scan and cancels sibling tasks.
Other schema, coverage, source, and budget errors remain fatal. Cancellation does
not retry, and Root/fork requests use 1200-second client deadline attempts and deadline retries.

Warnings identify the chunk, request and strength attempt, zero-based finding
indices, missing-field flags, and original invalid values. The escaped diagnostic
sample is limited to 2000 characters. Full invalid responses and diagnostics are
retained in `hierarchy.stages[].attempts[].map_failures` for completed stages, and
usage includes every response, including those with invalid strength.
Repair feedback is subject to the existing query and audit limits, including the
configured Map input token estimate.

## Decision identifier and relation validation and repair

A decision may cite a single finding. A relation must cite at least two distinct
input finding IDs because it describes an interaction between findings. Conditions
or exceptions within one finding belong in its decision statement and rationale.
Return an empty `relations` array when fewer than two findings are available or no
supported cross-finding relation exists.

If an otherwise valid reducer output contains a relation with zero or one finding
ID, the backend retries only that reduction, for **three attempts total** (the
initial call and up to two repairs). The original child records and source IDs
remain unchanged. The next request includes the malformed relations and allowed
IDs as `relation_repair` diagnostics and requests a complete replacement output.
Map, context generation, completed forks, and earlier specifications are reused.
The backend does not remove relations automatically or manufacture another ID.

Duplicate or unknown finding IDs within a decision also retry only the affected
root or chapter reduction, including a chapter batch. The next request includes
`decision_identifier_repair`: the exact allowed IDs, malformed decisions with
zero-based indices, duplicate and unknown IDs, and any missing evidence IDs.
The model must re-evaluate those decisions against the original evidence and
return a complete replacement. The backend never deduplicates, substitutes, or
drops IDs automatically. A finding may legitimately appear in multiple decisions;
uniqueness is required within each decision's `finding_ids` array. Decision ID
repairs and relation repairs share the same three-attempt limit, even if the error
kind changes between responses.

Every replacement must pass the full schema, evidence coverage, and provenance
checks. Unknown or duplicate IDs in relations, omitted evidence without a decision
ID error, incorrect ID types, other malformed fields, and invalid JSON remain
fatal. Each repair call uses the client's
1200-second deadline attempts and deadline retries; leaf Map calls keep their separate 300-second deadline.
These attempts are separate from API processing retries, approval coverage
reviews, and full-scan approval attempts.

Invalid reducer outputs and their diagnostics are retained in
`hierarchy.stages[].attempts[].reduction_failures` when present. Usage includes
every completed repair call. Query, output, and audit byte limits remain enforced;
the two-level chapter input estimate also includes repair feedback. Budget failure
or repeated invalid outputs stops processing without accepting partial evidence.
The warning log identifies the phase, node, reduction attempt, and zero-based
relation indices; `repair_exhausted=True` identifies exhaustion.
Decision identifier warnings include bounded, escaped samples of offending IDs and
missing evidence IDs; the audit retains the full diagnostics and original output.

## Evidence retention and validation

Intermediate records stay in request-local memory and are included in the response's `hierarchy` field. Original leaf evidence remains available for the separate root approval review, even after intermediate judgments have compressed it.

- Every chunk belongs to exactly one jurisdiction in source order. For PDFs with detected chapters, the planner cannot split or mix `chapter_id` values: all sections and parts of one chapter share its fork. Without chapters, native `section_id` remains the ownership boundary.
- Each leaf must account for every page or slide in its assigned range, and its source references must remain within that range.
- Each adjudication must account for all input evidence IDs and must not reference unknown IDs.
- Root approval must explicitly return a boolean decision and report reviewing every chunk and finding.
- Invalid coverage records retain the returned review and all missing, duplicate, and unknown IDs in `approval_review_failures`; a successful retry must independently pass the full coverage check. Map and reduction ID validation remains strict and does not enter this approval repair loop.
- Invalid JSON, missing required fields, omitted evidence, or exceeded output budgets fail the request. A leaf failure cancels sibling tasks and prevents reduction of a partial scan.

These checks validate reported coverage and provenance references. They do not prove that the API interpreted every source element or that every quotation is correct. PDF images and non-text PowerPoint content depend on the model and deployment. Evaluate output quality with representative documents.

## HTTP response

`POST /upload` returns one JSON object after all eight stages have completed and their Markdown files have been saved. The backend saves each completed Markdown specification and updates `checkpoint.json` under top-level `res/` while generation continues. The checkpoint retains the state needed to resume; it is not a copy of the final API response. Partial specifications are available on disk and are not streamed.

| Field | Meaning |
| --- | --- |
| `file_name` | Uploaded source filename with the server-generated Unix-time prefix. |
| `output_files` | Ordered `markdown` paths and a `checkpoint` path, relative to the repository root on the server. |
| `run_id` | Output directory name; pass this as `resume_from` to resume it. |
| `resume` | Present on resumes: source run, reused stages, unverified legacy stages, and source-run history. |
| `usage_scope` | `completed_stages_and_global_context`; excludes abandoned stages from earlier requests. |
| `status` | `completed` in the final response; stage callbacks use `partial` in memory. |
| `request` | `generate_specifications`. |
| `specifications` | Eight ordered objects containing `step`, `key`, `title`, `content`, `usage`, and `elapsed_ms`. |
| `reply` | All eight Markdown documents concatenated in stage order. |
| `usage` | Aggregate `input_tokens`, `output_tokens`, and `total_tokens`. |
| `timing_ms.llm` | Elapsed time for specification generation, including stage output writes. |
| `timing_ms.total` | Handler time including stage saves and final Markdown preparation, before final JSON serialization. |
| `chunks` | Original ranges, filenames, `chapter`, `chapter_id`, `section`, `section_id`, `part`, headings, PDF `source_regions`, estimated tokens, and continuation context. |
| `hierarchy.reduce_levels` | `2`. |
| `hierarchy.global_context` | Global context and semantic jurisdictions. |
| `hierarchy.context_usage` | Token usage for the initial global-context call. |
| `hierarchy.stages[].attempts[]` | Root and subglobal contexts, leaf evidence in `scans`, intermediate judgments in `nodes`, the `candidate`, its validated `approval`, and any `approval_review_failures` for each attempt. Batched chapter nodes also retain `aggregation_calls` with rounds, modes, and intermediate outcomes. |

Each `specifications[].content` is an independent English Markdown document with its own H1 title. Per-stage `usage` and `elapsed_ms` describe that specification. Missing token counts remain `null`, and the corresponding aggregate fields also become `null`.

Overall usage includes the initial global-context call and all eight stages. For stages 01–07, usage includes every context, map, reduction, and approval call, including rejected attempts and reviews with incomplete coverage. Stage 8 includes only its Markdown synthesis call and any client retries. The hierarchy audit contains seven stages and has no entry for the TBD register. Rejected attempts and failed review records remain in the audit history when a later attempt succeeds.

## Output files

After the first stage completes, each new request creates a unique directory under the repository's top-level `res/`. A resume creates its new directory when copying the completed prefix. The directory name includes `twolevel`, the run-start timestamp in **JST (UTC+09:00)**, and a unique suffix. Each completed stage writes one UTF-8 Markdown file and updates its checkpoint before the next stage starts. A successful run leaves eight specifications and a checkpoint:

```text
res/twolevel_20261110183045_<unique suffix>/
  01_screen_functions.md
  02_api.md
  03_data.md
  04_batch_functions.md
  05_business_rules.md
  06_exception_handling.md
  07_processing_flows.md
  08_architecture_decision.md
  checkpoint.json
```

Stable filenames make the documents easy to supply together to an implementation AI and allow relative links between specifications. Runs starting in the same second use separate directories. `output_files.markdown` and `output_files.checkpoint` in the API response list repository-relative paths; there is no `output_files.json` entry. The output location is resolved from the source file, independently of the server's working directory.

After stage 2, the directory contains two Markdown files and a checkpoint. If a later stage fails or is cancelled, completed files remain available. New files are prepared before being committed; a write failure rolls back files from that save and preserves earlier completed files and their checkpoint. Completed Markdown files are not rewritten during later saves. Fresh runs create no output directory before the first stage completes. Use the explicit resume request above to continue an interrupted run. Generated output directories are ignored by Git.

## English server logs

`Specification LLM query submitting` identifies the final synthesis as `phase=decision_register`; it does not emit hierarchy query or Root approval events.

`Stage output saved` records progress such as `completed=2/8`, the Markdown file count, and the absolute output directory after every completed stage. `Output files saved` records the final Markdown file count and directory.

`Responses request submitting` includes the requested `max_output_tokens`.

`Full scan started` includes `level1_max_parallel` and `level2_max_parallel`, the
effective concurrent request limits for chapters and leaf Maps, respectively.

`Root approval coverage invalid` reports the review attempt, distinct allowed/expected chunk and finding counts, and a sample of up to 20 missing IDs of each kind. `invalid_ids_sample` includes up to 20 duplicate/unknown IDs of each kind as escaped JSON, capped at 2000 characters; `review_exhausted=True` identifies the final failed attempt. Completed stages retain full diagnostic lists and returned reviews in `approval_review_failures`. Their token usage is included, and query, output, and audit limits also apply to repairs.

`Specification stage started/completed/failed/cancelled` and `Specification LLM query submitting` identify the specification's English name, `step`, `stage`, and dedicated `prompt`.

`Hierarchy query started/completed/failed/cancelled` identifies `phase`, `node`, and `attempt`. Completion events include elapsed time and input, output, and total token counts. `Full scan coverage verified` records the processed chunk count. `PDF structure detected` records detected chapters and numbered sections. `Chapter aggregation` identifies the fork, mode, round, batch, and finding count. `Root approval decision` records the approval outcome, `Root rejected candidate` records a rejection, and `Upload completed` records aggregate usage.

The phases for this backend are `global_context`, `root_context`, `onelevel_context`, `map`, `onelevel_reduce`, `root_reduce`, and `root_approval`. `Root rejected candidate` includes the review's `rationale` and blocking `feedback`, serialized as JSON with escaped newlines and non-ASCII characters. Full specification bodies and the evidence ledger remain in the response; rejection feedback may refer to relevant source passages.

## Resource limits and configuration

| Environment variable | Default | Purpose and maximum |
| --- | ---: | --- |
| `FILE_CHUNK_MAX_PAGES` | 8 | Pages per PDF leaf; maximum 100. |
| `FILE_CHUNK_MAX_SLIDES` | 8 | Slides per PPTX leaf; maximum 100. |
| `FILE_CHUNK_MAX_ESTIMATED_TOKENS` | 12000 | Estimated source tokens per PDF leaf; maximum 100000. |
| `FILE_CHUNK_PAGE_TOKEN_ESTIMATE` | 2000 | Visual allowance per attached PDF page region; maximum 10000. |
| `LLM_CHAPTER_BATCH_MAX_BYTES` | 131072 | Soft UTF-8 size target for chapter child records; capped at the query byte limit. |
| `LLM_MAX_CHAPTER_REDUCE_ROUNDS` | 8 | Maximum batching/merge rounds inside one chapter fork; maximum 16. |
| `LLM_CHAPTER_INPUT_TOKEN_BUDGET` | unset | Optional estimate ceiling for the complete chapter prompt and instructions; maximum 1000000. |
| `LLM_MAP_INPUT_TOKEN_BUDGET` | unset | Optional estimate ceiling for Map instructions, complete prompt, and PDF source estimate; maximum 1000000. |
| `LLM_MAX_PARALLEL_LEVEL1_REQUESTS` | legacy or 16 | Chapter context and aggregation requests across all chapters and batches; maximum 16. |
| `LLM_MAX_PARALLEL_LEVEL2_REQUESTS` | legacy or 16 | Leaf Map requests across all chapters; maximum 16. |
| `LLM_MAX_PARALLEL_CHUNK_REQUESTS` | 16 | Legacy fallback for either level without a valid explicit setting; maximum 16. |
| `LLM_MAX_APPROVAL_ATTEMPTS` | 8 | Full-scan attempts per specification, including the initial attempt; maximum 8. |
| `LLM_MAX_APPROVAL_REVIEW_ATTEMPTS` | 3 | Review calls per candidate for missing, duplicate, or unknown review IDs, including the initial call; maximum 5. |
| `LLM_INTERMEDIATE_MAX_BYTES` | 1048576 (1 MiB) | Intermediate JSON size in UTF-8 bytes; maximum 16777216 (16 MiB). |
| `LLM_MAX_OUTPUT_TOKENS` | 128000 | Root reduction and TBD synthesis API output limit, including reasoning tokens; maximum 128000. |
| `LLM_INTERMEDIATE_MAX_OUTPUT_TOKENS` | 64000 | Context, Map, intermediate reduction, and approval API output limit, including reasoning tokens; maximum 128000. |
| `LLM_FINAL_MAX_BYTES` | 1048576 (1 MiB) | Final candidate JSON or TBD Markdown size in UTF-8 bytes; maximum 16777216 (16 MiB). |
| `LLM_MAX_QUERY_BYTES` | 8388608 (8 MiB) | Text query size in UTF-8 bytes, including previous specifications; maximum 33554432 (32 MiB). |
| `LLM_AUDIT_MAX_BYTES` | 16777216 | Cumulative serialized intermediate-record budget; maximum 67108864. |

Leaf JSON must fit both the configured intermediate limit and a bound smaller than the average binary chunk size. Intermediate adjudication output must also be smaller than its input JSON payload, including child records and context. These byte limits control growth; they are not a proof of semantic compression or token reduction. Original evidence is retained separately.

Root reduction and TBD synthesis default to 128000 output tokens and a separate 1 MiB output byte budget. Context, Map, intermediate reduction, and approval default to 64000 output tokens. Token budgets include visible output and reasoning tokens. Set the environment variables above in `.env` and restart the server; existing environment values override defaults. Use values supported by your Azure deployment, whose own limits still apply. An incomplete API response or exceeded budget stops processing without silently truncating evidence. Review the budgets and chunk settings when a document exceeds them.

Splitting is limited to 256 chunks and 150 MiB of combined chunk data. Because files and audit records remain in memory throughout an analysis, each server process admits one upload analysis at a time. Additional uploads return HTTP `503` with `Retry-After: 10`. Leaf calls within the active analysis still run concurrently. Additional server processes require corresponding memory and API quota.

The Responses client retains SDK transport retries for transient failures. Map calls use the 300-second deadline and timeout retries described above; other phases use 1200-second deadline attempts with up to three deadline retries.

## Code, prompts, and tests

`server/chat.py` selects the reduction depth. `server/hierarchy.py` executes the workflow, `server/concurrency.py` resolves the independent level limits for the hierarchy and API client, and `server/evidence.py` validates model records. The first seven stage templates inherit the shared template and use `prompt/hierarchy_*.jinja2` for each phase. `server/decision_register.py` generates stage 8 with its own standalone Markdown prompt and system instructions. `server/file_chunks.py` dispatches file splitting, `server/pdf_sections.py` builds PDF chapter/section parts, and `server/chapter_reduction.py` handles bounded calls within chapter forks.

Run the test suite from this `be/` directory:

```bash
python -m unittest discover -s tests -v
```

Tests mock API traffic and cover real file splitting, hierarchy paths, context distribution, full-scan coverage, evidence IDs, rejection and reprocessing, resource limits, concurrency, logs, token totals, and HTTP responses. Map tests also cover timeout retries, strength repair and its interaction with timeouts, retry exhaustion, cancellation, slot release, queue wait, and completion counters.

Chapter tests cover concurrent batches, round dependencies, ordered audit history,
and cancellation on failure. Concurrency tests exercise different level limits,
the shared chapter limit across batches, legacy fallback, and client capacity.
