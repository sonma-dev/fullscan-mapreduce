# Full-File Specification Generation with Approval

Upload a PDF or PPTX file (up to 50 MiB) to `POST /upload` to generate seven specifications and a TBD register through the OpenAI Responses API. Stages 01–07 generate and independently review each candidate against the complete source through `input_file`; stage 8 uses only their approved Markdown. All eight generated documents, including titles, headings, and explanatory text, use English Markdown; server logs are in English.

## Setup

Use Python 3.11 or later in an activated virtual environment. From the repository root, enter this backend directory and install its dependencies and Gunicorn:

```bash
cd experiment/fullload_approve/be
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
LLM_MAX_APPROVAL_ATTEMPTS=8
LLM_MAX_APPROVAL_REVIEW_ATTEMPTS=3
LLM_INTERMEDIATE_MAX_OUTPUT_TOKENS=64000
```

`API_KEY` authenticates requests to this backend and must contain at least 32 characters. It is separate from `AZURE_OPENAI_API_KEY`, which authenticates the development backend to Azure OpenAI. The application loads `.env` automatically at startup.

`AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` is accepted as a fallback deployment setting. When `APP_ENV` is `prod`, `production`, or `staging`, the backend uses Microsoft Entra ID through managed identity; `AZURE_CLIENT_ID` can select a user-assigned identity. The current startup validation still requires `AZURE_OPENAI_API_KEY` to be set. Choose a deployment that supports Responses API file input and background execution for the document types you use.

## Start the server

Run this exact command from `experiment/fullload_approve/be/`:

```bash
gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app --bind localhost:8001 2>&1 | tee ../../../_test_fullload_approve.log
```

The server listens on `http://localhost:8001`. Both standard output and standard error are displayed in the terminal and written to `_test_fullload_approve.log` in the repository root. `tee` overwrites that log on each run. Backend examples use the same port, so run one at a time on this address.

## POST a document with curl

Open a second terminal in `experiment/fullload_approve/be/`. Set the client-side `API_KEY` to the same value configured in the backend's `.env`; the server's automatic `.env` loading does not export it into this terminal.

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

Replace the example path with your document path. `curl --form` sets the multipart content type and boundary. The command prints the API response in the terminal. The request remains open until all eight documents finish. The backend saves each completed Markdown file under top-level `res/` before starting the next stage; it does not create a JSON output file. Follow the server log for progress.


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

Stages 01–07 send the entire original file and all earlier approved specifications to the LLM using Responses API `input_file`. Each candidate is then sent to a separate approval call with the same complete original attachment, the stage requirements, and the previous specifications. Stage 8 receives only the seven approved Markdown specifications. A successful request without rejection, coverage repairs, or client retries makes 15 response-creation calls: seven generation calls, seven approval calls, and one TBD synthesis. Polling and SDK transport retries are additional HTTP requests.

For the same stage, source filename, and previous specifications, the initial generation query and generation system instructions match `fullload` exactly. Page/slide checklists, attempt numbers, and review metadata are supplied only to approval. After a valid rejection, regeneration uses the same generation prompt with a separate correction instruction and blocking feedback appended. Approval uses its own `specification_approval_user.jinja2` wrapper with the stage's requirements, preserving the independent review. This prompt alignment does not change the configured model or `reasoning_effort`.

The source is never split into Map chunks. `pypdf` counts PDF pages and `python-pptx` counts PPTX slides once, providing a checklist of every original one-based page/slide number. Approval reads the original attachment directly, including requirements absent from the candidate; this backend has no Map finding ledger. Unreadable documents and documents with no pages/slides are rejected before generation.

Approval accepts a usable English draft preserving source-supported core behavior, material conditions, and exceptions. Explicit `Needs confirmation`, unresolved source alternatives, labeled `Proposal` items, later-stage dependencies, and minor editorial issues are non-blocking. Rejection requires non-English generated prose/labels or a material source-grounded defect that would mislead implementation or testing. Blocking feedback identifies the original page/slide, the candidate defect, its impact, and the smallest correction. Optional feedback on an approved review is retained without regenerating the candidate.

The reviewer returns JSON with a boolean `approved`, integer-array `reviewed_source_unit_ids`, non-empty `rationale`, and string-array `feedback`. Rejection requires at least one non-empty feedback item. Both approval and rejection must report every required source-unit ID exactly once. The backend validates these fields and coverage; semantic correctness and English output are assessed by the LLM.

- A valid rejection feeds blocking feedback into a new full-file generation of the current stage, including a new approval. Earlier approved stages are reused. `LLM_MAX_APPROVAL_ATTEMPTS` defaults to 8 total attempts, including the initial generation, with a maximum of 8.
- Missing, duplicate, or unknown source-unit IDs trigger approval-only retries against the unchanged candidate and attachment. The next review receives exact diagnostics and the previous response, and must return a complete new review. The three error types share `LLM_MAX_APPROVAL_REVIEW_ATTEMPTS`, defaulting to 3 total reviews per candidate, with a maximum of 5. IDs are never auto-filled, removed, or replaced.
- Exhausting either allowance stops the request. Invalid JSON, malformed fields, incorrect ID types, and exceeded query/output/audit budgets fail immediately. Client API/deadline retries are separate and reuse the identical request.

Generation and TBD synthesis use `LLM_MAX_OUTPUT_TOKENS` (default and maximum 128000). Approval uses `LLM_INTERMEDIATE_MAX_OUTPUT_TOKENS` (default 64000, maximum 128000). These limits include visible output and reasoning tokens. Existing environment values override defaults; choose values supported by your Azure deployment and restart the server after changing `.env`. An incomplete response still fails the request.

`LLM_MAX_QUERY_BYTES` defaults to 8 MiB (maximum 32 MiB). `LLM_FINAL_MAX_BYTES` and `LLM_INTERMEDIATE_MAX_BYTES` limit generation and approval outputs respectively, each defaulting to 1 MiB (maximum 16 MiB). `LLM_AUDIT_MAX_BYTES` limits the request-local approval audit to 16 MiB by default (maximum 64 MiB). Limits measure UTF-8 bytes and stop processing without truncation, including when review diagnostics increase a retry query.

The next stage begins only after the current stage is approved and its Markdown is saved. Stage 8 has no approval call. A failure stops the sequence before later specifications run.

## HTTP response

`POST /upload` returns one JSON object after all eight stages have completed and their Markdown files have been saved. The backend saves each completed Markdown specification under top-level `res/` while generation continues. The API response carries usage, timing, and any evidence audit in memory; it is not saved as a JSON file. Partial specifications are available on disk and are not streamed.

| Field | Meaning |
| --- | --- |
| `file_name` | Uploaded source filename with the server-generated Unix-time prefix. |
| `output_files` | Ordered `markdown` output paths, relative to the repository root on the server. |
| `status` | `completed` in the final response; stage callbacks use `partial` in memory. |
| `request` | `generate_specifications`. |
| `specifications` | Eight ordered objects containing `step`, `key`, `title`, `content`, `usage`, and `elapsed_ms`. |
| `reply` | All eight Markdown documents concatenated in stage order. |
| `usage` | Aggregate `input_tokens`, `output_tokens`, and `total_tokens`. |
| `approval_audit` | Source filename, page/slide kind and complete checklist; seven stage histories containing each candidate, validated approval, and invalid review responses with coverage diagnostics. |
| `timing_ms.llm` | Elapsed time for specification generation, including stage output writes. |
| `timing_ms.total` | Handler time including stage saves and final Markdown preparation, before final JSON serialization. |

Each `specifications[].content` is an independent English Markdown document with its own H1 title. Per-stage `usage` and `elapsed_ms` include generation, approval, rejected candidates, and invalid coverage reviews. Missing token counts remain `null`, and the corresponding aggregate fields also become `null`. Approval audits are included in stage callback snapshots and the final response; only approved Markdown is written to disk, with no JSON audit file.

## Output files

After the first stage completes, each request creates a unique directory under the repository's top-level `res/`. The directory name follows `fullload_approval_YYYYmmddHHMMSS_XXXXXXXX`, using the run-start timestamp in **JST (UTC+09:00)** and eight random lowercase letters. Directory creation is atomic; a collision generates another suffix. Each completed stage writes one UTF-8 Markdown file before the next stage starts. A successful run leaves these eight files:

```text
res/fullload_approval_20261110183045_abcdefgh/
  01_screen_functions.md
  02_api.md
  03_data.md
  04_batch_functions.md
  05_business_rules.md
  06_exception_handling.md
  07_processing_flows.md
  08_architecture_decision.md
```

Stable filenames make the documents easy to supply together to an implementation AI and allow relative links between specifications. Runs starting in the same second use separate directories. `output_files.markdown` in the API response lists repository-relative paths; there is no `output_files.json` entry and no JSON output file. The output location is resolved from the source file, independently of the server's working directory.

After stage 2, the directory contains two Markdown files. If a later stage fails or is cancelled, completed files remain available. New files are prepared before being committed; a write failure rolls back files from that save and preserves earlier completed files. Completed Markdown files are not rewritten during later saves. No output directory is created before the first stage completes. This persistence does not provide automatic job resumption. Generated output directories are ignored by Git.

## 1200-second deadline retries

When the Responses client's **1200-second deadline expires**, it resubmits the
identical request up to **three additional times**, giving each retry a fresh
1200-second deadline. The fourth deadline expiry raises `ElapsedTimeException` and
stops the request. This applies to full-file specification generation, approval,
and TBD synthesis.

Before retrying, the client attempts to cancel the latest known active background
response, with a separate five-second cleanup limit. Cancellation is best effort;
a job whose ID was not returned cannot be cancelled. The prompt, instructions,
attachment, output token limit, and output format are reused. Only the affected
request is resubmitted; the current candidate and earlier specifications
are not regenerated when approval is retried. These retries do not consume semantic
approval attempts or coverage-review attempts. Caller cancellation stops immediately without starting another
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

## Response processing retries

All phases retry a terminal `status=failed` response for `server_error`, `rate_limit_exceeded`, or `vector_store_timeout`. A code-less Azure error is also retried when its message starts with "An error occurred while processing your request." and explicitly says "You can retry your request". Known permanent errors and unknown codes stop immediately; the message fallback never overrides a supplied code. Incomplete responses (including `max_output_tokens`), cancellation, and invalid generated content are not retried by this mechanism.

For processing failures, the client resubmits the identical request up to **three additional times** (four submissions if no deadline expires), with waits of **2, 4, and 8 seconds**, each plus 0–1 seconds of jitter. Submission, polling, SDK HTTP retries, and these processing retries share the current **1200-second deadline attempt**. A deadline retry starts a fresh window as described above; SDK transport retries remain separate.

Retry logs include the failed response ID, error code, `retry=1/3`, delay, and elapsed time. Submission and polling logs include `response_attempt`; exhaustion logs include `processing_retries_exhausted=True`. Token usage includes failed submissions when all attempts report complete usage; otherwise the affected request, specification, and aggregate usage become `null`. Usage for unaffected specifications remains available.

A retry resends the current specification request with the original full `input_file` and previous specifications. Completed stages are not regenerated. On cancellation or timeout, the client attempts to cancel the latest known active background response, with a separate five-second cleanup limit; remote cancellation is best effort.

## English server logs

`Stage output saved` records progress such as `completed=2/8`, the Markdown file count, and the absolute output directory after every completed stage. `Output files saved` records the final Markdown file count and directory.

`Responses request submitting` includes the requested `max_output_tokens` and the actual request's `reasoning_effort`, including on retries.

Stage start, completion, failure, and cancellation logs identify `file_name`, `step`, `stage`, the English specification name, and its dedicated `prompt`. Each `Specification LLM query submitting` event records `phase=generation`, `phase=approval`, or `phase=decision_register`, and the query size. `Full-file approval decision` records the decision and feedback count. `Full-file rejected candidate` records escaped rationale and blocking feedback. `Full-file approval coverage invalid` records the attempt, review allowance, coverage counts, samples of missing/duplicate/unknown IDs, and whether the allowance is exhausted. Completion events include elapsed time and input, output, and total token counts. `Upload completed` records the request-wide totals.

```text
Specification LLM query submitting: file_name=sample.pdf step=1/8 stage=screen_functions specification="Screen Function Specification" prompt=stages/screen_functions.jinja2 phase=generation chunk=none query_chars=1234
Specification stage completed: file_name=sample.pdf step=1/8 stage=screen_functions specification="Screen Function Specification" prompt=stages/screen_functions.jinja2 elapsed_ms=1234 input_tokens=1000 output_tokens=500 total_tokens=1500
```

The numbers above are illustrative. Specification bodies are returned in the HTTP response rather than written to the server log.

## Code, prompts, and tests

Stage order and names are defined in `server/specifications.py`. Dedicated requirements live in `prompt/stages/*.jinja2`, with shared evidence and consistency rules in `prompt/specification_system.jinja2`. `prompt/specification_user.jinja2` matches `fullload` for generation; `prompt/specification_revision.jinja2` is appended only after rejection. Approval uses `prompt/specification_approval_user.jinja2` and acceptance rules in `prompt/specification_approval.jinja2`; JSON and coverage validation live in `server/approval.py`. The full-file generation and approval flow is in `server/chat.py`.

Run the test suite from this `be/` directory:

```bash
python -m unittest discover -s tests -v
```

Tests mock API traffic and verify stage order, original attachments and page/slide coverage, rejection and approval-only retries, validation failures and budgets, propagation of approved outputs, token totals, English logs, upload behavior, and preservation of completed Markdown after failure.
