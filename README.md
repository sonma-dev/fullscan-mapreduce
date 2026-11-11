# Document Specification Generation Experiments

This repository compares three Python/FastAPI backends that generate software specifications from PDF and PowerPoint (`.pptx`) documents using the Azure OpenAI Responses API: full-file generation, one-level MapReduce, and two-level MapReduce. It also contains the input dataset, execution logs, generated results, and directories for statistical-analysis work instructions and related documents.

**You must design and build your own frontend. This repository provides backend code only; no frontend application is included.**

## Repository layout

The project directories and files are organized as follows. Timestamped logs and result directories represent individual runs.

```text
.
|-- README.md
|-- .gitignore
|-- dataset/
|   `-- OrionDesk_AI_Detailed_Design_Specification.pdf
|-- experiment/
|   |-- fullload/
|   |   `-- be/
|   |-- onelevel_mapreduce/
|   |   `-- be/
|   `-- twolevel_mapreduce/
|       `-- be/
|-- log/
|   |-- fullload-<timestamp>.log
|   |-- onelevel_mapreduce-<timestamp>.log
|   `-- twolevel_mapreduce-<timestamp>.log
|-- res/
|   `-- <prefix>_<YYYYMMDDhhmmss>_<unique suffix>/
|       |-- 01_screen_functions.md
|       |-- ...
|       `-- 08_architecture_decision.md
`-- statistical_analysis/
    |-- fullload/
    |-- onelevel/
    |-- twolevel/
    `-- res/
```

| Directory | Purpose |
| --- | --- |
| [dataset/](dataset/) | Input documents shared by the experiments. The current dataset contains the OrionDesk detailed design PDF shown above. |
| [experiment/](experiment/) | Three independently configured backend programs, each with its own source, prompts, dependencies, tests, and README under `be/`. |
| [log/](log/) | Captured server logs for tracing requests, stage progress, retries, elapsed time, and token usage. The startup command below writes logs here. |
| [res/](res/) | Backend-generated Markdown specifications, grouped by backend and run. Older runs may also contain legacy JSON snapshots. |
| [statistical_analysis/](statistical_analysis/) | Statistical-analysis work instructions, analysis plans, evaluation procedures, and related working documents, organized by experiment. |

The existing directory name is `statistical_analysis`. Its analysis subdirectories are currently empty and reserved for the corresponding materials:

| Backend source | Analysis documents | Generated result prefix |
| --- | --- | --- |
| [experiment/fullload/be/](experiment/fullload/be/) | [statistical_analysis/fullload/](statistical_analysis/fullload/) | `fullload` |
| [experiment/onelevel_mapreduce/be/](experiment/onelevel_mapreduce/be/) | [statistical_analysis/onelevel/](statistical_analysis/onelevel/) | `onelevel` |
| [experiment/twolevel_mapreduce/be/](experiment/twolevel_mapreduce/be/) | [statistical_analysis/twolevel/](statistical_analysis/twolevel/) | `twolevel` |

API responses, existing JSON results, and logs provide inputs for usage and timing analysis; Markdown files provide the specification content for implementation and quality review. The analysis directories hold work instructions and related documents maintained for that work. The backends save their generation results in `res/`.

Local environment files, Python caches, logs, and generated results are covered by the root [.gitignore](.gitignore). Each backend also has its own `.gitignore`.

## The three backends

| Example | Processing strategy | Response-creation calls per successful upload |
| --- | --- | --- |
| [Full file](experiment/fullload/be/README.md) (`fullload`) | Sends the original document for stages 01–07, then generates stage 8 from their Markdown; no approval calls or approval gate. | `8` |
| [One-level MapReduce](experiment/onelevel_mapreduce/be/README.md) (`onelevel_mapreduce`) | For stages 01–07, scans every chunk, then sends leaf evidence directly to a root reducer and a separate approval review. | `1 + 7 * (N + 3) + 1` |
| [Two-level MapReduce](experiment/twolevel_mapreduce/be/README.md) (`twolevel_mapreduce`) | For stages 01–07, maps PDF sections or section parts, combines their evidence within chapter forks, then runs root reduction and a separate approval review. | `1 + 7 * (N + 2G + 3) + 1` |

`N` is the number of leaf chunks and `G` is the number of intermediate forks (detected PDF chapters in the two-level backend). The trailing `+ 1` is the Markdown-only TBD call. Counts assume one reduction call per fork, approval on the first attempt, and no Map timeouts, Map strength repairs, approval coverage retries, response processing or deadline retries, or relation repairs, and exclude polling and transport retries. Reduction depth counts the layers above the leaf chunks; context generation and approval are separate calls.

The one-level tree is `root > leaf chunks`. The two-level tree is `root > chapter forks > section/part leaves`. Both MapReduce programs split the document once, preserving native PDF outline or PPTX section boundaries where available. The two-level backend additionally detects numbered PDF sections within pages, preserves chapter introductions, and divides oversized sections into parts under the same chapter fork. Oversized chapter reductions run bounded batches concurrently within each round, followed by a check across batches, preserving the two-level tree. Chapter workers and leaf Map workers have independent concurrency limits. See its README for layout fallbacks and budget settings.

An initial MapReduce call receives the entire original document through `input_file` to establish global context. Each of specifications 01–07 then scans every chunk, with each Map call receiving its corresponding file attachment through `input_file`. Aggregation and approval use the retained evidence records. If approval rejects a candidate, the backend regenerates context and scans every chunk again. The default limit per specification, including the initial attempt, is two attempts for the one-level backend and eight for the two-level backend. It retains evidence and review history in the response.

Approval receives an explicit checklist of every chunk and finding ID. If an otherwise valid review has missing, duplicate, or unknown IDs, the backend retries that review with the full checklist, exact ID diagnostics, and previous response. These errors share one allowance of up to three review attempts by default. Retries reuse the candidate and evidence without rerunning Map or reduction. Every allowed ID must appear exactly once; the backend never corrects the reported arrays automatically. Exhaustion fails the request. Failed reviews and their token usage remain in completed stages' audit history and totals.

MapReduce approval accepts a usable draft with documented source gaps, uncertainty, unresolved alternatives, later-stage dependencies, and minor editorial issues. Rejection requires a source-grounded material defect in the current specification, such as omitted core behavior, an incorrect exception, or an invented confirmed requirement. Optional suggestions can remain in an approved review's `feedback` without triggering a rescan. Rejection logs include the rationale and required corrections.

Use full load as a baseline, one level to inspect direct aggregation of chunk evidence, and two levels to inspect aggregation through chapter forks. Compare token usage, elapsed time, and output quality on the same documents; additional reduction layers do not guarantee lower cost or better results.

## Generated specifications

All three examples produce these specifications in order:

| Step | Response key | Specification |
| --- | --- | --- |
| 1 | `screen_functions` | Screen Function Specification |
| 2 | `api` | API Specification |
| 3 | `data` | Data Specification |
| 4 | `batch_functions` | Batch Function Specification |
| 5 | `business_rules` | Business Rules |
| 6 | `exception_handling` | Exception Handling Specification |
| 7 | `processing_flows` | Processing Flow Specification |
| 8 | `architecture_decision` | Architecture Decision Register |

The final document keeps the filename `08_architecture_decision.md` and serves as a TBD register. It uses only the completed Markdown specifications 01–07. Items answered consistently by explicit confirmed statements are marked resolved with links to the relevant files, sections, and requirement IDs. Remaining questions, unadopted proposals, and contradictory statements stay open with their impact and questions to confirm. The model does not select design options or invent decisions. Supply all eight Markdown files together to an implementation AI.

Stage 8 makes one direct Markdown-generation call after stage 7 succeeds, with no source attachment, Map evidence, global context, chunk scan, reduction, or approval call. It uses the shared Responses client's processing and deadline retries. Its token usage and elapsed time are included in the eighth specification and overall totals. If it fails or is cancelled, the seven completed Markdown files remain available.

Stage 8 uses `LLM_MAX_OUTPUT_TOKENS` (default and maximum 128000), `LLM_MAX_QUERY_BYTES` (default 8 MiB, maximum 32 MiB), and `LLM_FINAL_MAX_BYTES` (default 1 MiB, maximum 16 MiB). The latter two limits measure the UTF-8 query and Markdown body; exceeding either fails without truncating the specifications. A blank response is not accepted as a completed document.

Each stage receives all previously completed specifications to preserve terminology and consistency. A failed stage stops the sequence. The current prompts generate **Japanese Markdown specifications**, while server logs are in English. To change the generated language, adapt the prompt templates and specification titles in the selected backend.

## Quick start

Use Python 3.11 or later and an Azure OpenAI deployment that supports Responses API file input, background execution, and the configured reasoning settings. The MapReduce examples also require JSON output support. File and model support depend on your deployment.

Choose one backend under `experiment/`. The following Bash commands start with the full-file example; replace `fullload` with `onelevel_mapreduce` or `twolevel_mapreduce` to use another strategy.

```bash
cd experiment/fullload/be
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp -n .env-sample .env
```

The copy command preserves an existing `.env`. All three backends provide `.env-sample`; credential fields are blank, while the MapReduce samples include suggested resource settings. Edit the selected backend's `.env` for your environment:

| Setting | Configuration |
| --- | --- |
| `APP_ENV` | Use `development` for Azure API-key authentication. |
| `API_KEY` | Set your own backend authentication key with at least 32 characters. Clients must send this key to the backend. |
| `PORT` | Set an integer such as `8001`. A copied sample contains an empty value, which must be filled or the line removed before running `app.py`. |
| `AZURE_OPENAI_ENDPOINT` | Set the endpoint for your Azure OpenAI resource. |
| `AZURE_OPENAI_API_KEY` | Set the Azure resource key. This is separate from the backend's `API_KEY`. |
| `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME` | Set the deployment used for Responses requests. |
| `AZURE_CLIENT_ID` | Optional user-assigned managed identity selection. |

The application loads its own `.env` automatically at startup. Restart the server after changing its configuration.

`AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` is supported as a fallback deployment setting. With `APP_ENV=prod`, `production`, or `staging`, Azure authentication uses managed identity; `AZURE_CLIENT_ID` can select a user-assigned identity. Startup validation currently still requires `AZURE_OPENAI_API_KEY` to be set in those environments.

## Run and capture logs

Run the following from the selected `be/` directory with its virtual environment activated:

```bash
mkdir -p ../../../log
backend_name="$(basename "$(dirname "$PWD")")"
python app.py 2>&1 | tee "../../../log/${backend_name}-$(TZ=Asia/Tokyo date +%Y%m%d%H%M%S).log"
```

The server defaults to `http://127.0.0.1:8001`. All three programs default to this port, so run one at a time or select a different `PORT` for each server. The command writes both standard output and standard error to top-level `log/`, using the backend directory name and a JST timestamp. Runtime logs are captured by this command; generation results are saved by the backend itself.

## Use the API

Both endpoints require authentication. In a second terminal in the selected `be/` directory, set the same backend key configured in `.env`; automatic server-side `.env` loading does not export it into your terminal. In Bash, enter the key without echoing it, then check the health endpoint:

```bash
read -r -s -p 'Backend API key: ' API_KEY

curl --fail-with-body --show-error \
  'http://127.0.0.1:8001/' \
  --header "Authorization: Bearer ${API_KEY}"
```

`GET /` returns `{"status":"ok"}`. Upload the included dataset PDF to the full-load backend from its `be/` directory:

```bash
curl --fail-with-body --show-error \
  --request POST 'http://127.0.0.1:8001/upload' \
  --header "Authorization: Bearer ${API_KEY}" \
  --form 'file=@../../../dataset/OrionDesk_AI_Detailed_Design_Specification.pdf;type=application/pdf'
```

For the other backends, use their server address. The backend identifies its output directory with its own prefix automatically. For PPTX, replace the `--form` value with `file=@/absolute/path/document.pptx;type=application/vnd.openxmlformats-officedocument.presentationml.presentation`. The multipart field must be named `file`, and uploads are limited to 50 MiB.

The request stays open until all eight documents finish and their Markdown files are saved. Each completed stage writes its Markdown under top-level `res/` before the next stage starts. The command prints the final JSON API response after stage 8; the backend does not save a JSON output file. Partial specifications are available on disk and are not streamed over HTTP.

| Response field | Contents |
| --- | --- |
| `file_name` | Uploaded source filename with a server-generated Unix-time prefix. |
| `output_files` | Ordered `markdown` output paths, relative to the repository root on the server. |
| `status` | `completed` in the final response; stage callbacks use `partial` in memory. |
| `request` | `generate_specifications`. |
| `specifications` | Eight ordered objects with `step`, `key`, `title`, `content`, `usage`, and `elapsed_ms`. |
| `reply` | All eight Markdown documents concatenated in stage order. |
| `usage` | Aggregate input, output, and total token counts; unavailable counts remain `null`. |
| `timing_ms` | Generation time including stage saves in `llm`; handler time including stage saves and final Markdown preparation in `total`, before final JSON serialization. |
| `chunks` | MapReduce only: chunk filenames, original page or slide ranges, and section metadata. |
| `hierarchy` | MapReduce only: reduction depth, global context, evidence, candidates, and approval attempts. |

Missing or invalid authentication returns `401`; empty uploads or invalid filenames return `400`; oversized files return `413`; unsupported extensions return `415`. Each MapReduce backend admits one analysis per server process at a time and returns `503` with `Retry-After: 10` when busy. Interactive API documentation and the OpenAPI endpoint are disabled.

## Markdown output files

All three backends save one UTF-8 Markdown file per completed stage. Each request uses its own `<repository>/res/<prefix>_<YYYYMMDDhhmmss>_<unique suffix>/` directory, where the prefix is `fullload`, `onelevel`, or `twolevel` and the timestamp is the run-start time in **JST (UTC+09:00)**. Runs starting in the same second cannot overwrite one another. The location is resolved from the source file and does not depend on the server's working directory.

A successful run contains:

```text
01_screen_functions.md
02_api.md
03_data.md
04_batch_functions.md
05_business_rules.md
06_exception_handling.md
07_processing_flows.md
08_architecture_decision.md
```

Supply the directory's eight Markdown files together to an implementation AI. Stable filenames allow relative links from the decision register to affected specifications. The API returns these paths in `output_files.markdown`; it has no `output_files.json` entry and the backend creates no JSON file.

After stage 2, the directory contains two Markdown files. Earlier outputs survive later failures or cancellation. New files are prepared before being committed; a write failure rolls back files from that save and preserves earlier completed files. Completed Markdown files are not rewritten. No directory is created before the first stage completes. `Stage output saved` logs the completed stage count and absolute directory. Generated output directories are ignored by Git. Saved Markdown does not provide automatic job resumption.

## Node responses and persistent storage

The two-level backend holds node responses in request-local memory while generating specifications. Evidence audits for specifications 01–07 appear in the successful API response under `hierarchy`; they are not written to JSON files. The following paths are relative to `hierarchy.stages[].attempts[]` in that response:

| Response | JSON path |
| --- | --- |
| Level 2: each section or chunk's Map result | `scans[]` |
| Level 1: each chapter's final aggregation result | `nodes[].outcome` |
| Level 1: each batch and merge result for a batched chapter | `nodes[].aggregation_calls[].outcome` |
| Root: specification candidate | `candidate` |
| Root: approval decision and feedback | `approval` |
| Root: specification context | `root_context` |
| Level 1: chapter contexts, keyed by fork ID | `subglobal_contexts` |

The initial document context and jurisdiction plan are stored separately in
`hierarchy.global_context`. `aggregation_calls` is present only for chapters that
require batching. Individual nodes do not get separate output files; the Markdown
files contain completed specification bodies.

**Node completion does not immediately write a file.** If a specification fails
or is cancelled before completion, its node responses are not persisted by the
backend, even if some nodes have already finished. Markdown files for
previously completed specifications remain available.

**The intended production design should persist node responses, intermediate
results, and final Markdown specifications to Azure Blob Storage in an Azure Storage
Account.** Each node response should be saved as it becomes available, identified
by run, specification, attempt, node, and batch where applicable, so it survives a
later stage failure or process restart. The current backends save completed Markdown files under local `res/`; Azure Blob Storage persistence and recovery from saved node results
are not implemented.

## Build your own frontend

You are responsible for implementing the frontend, including document selection, uploading to `POST /upload`, displaying a waiting state, rendering the returned Markdown, and downloading results if needed. Handle the API errors described above and allow for long-running requests in client and proxy timeouts.

For a browser application, use a server-side proxy to keep backend credentials on the server, or implement an appropriate authentication flow. Azure credentials belong in the backend. The examples do not configure CORS; use a same-origin proxy or explicitly configure the allowed frontend origin when adding browser integration.

## Map progress and repair

Both MapReduce backends time out each active leaf Map request after 300 seconds and retry the same chunk up to three times (four requests total when only timeouts occur). Root and fork aggregation each use 1200-second deadline attempts, with up to three additional deadline retries. Waiting for the complete Map batch has no 300-second deadline. Each validated chunk produces a progress log such as `Map completed 30/31`; counts reset for each specification and full-scan approval attempt. See the backend READMEs for cancellation behavior and usage reporting after timeouts.

A missing or invalid Map `strength` triggers up to two repairs of only that chunk, using the same source attachment and context. The LLM must select `explicit`, `inferred`, or `uncertain` based on the source and return a complete valid record. The timeout and strength-repair counters are independent and never reset each other, allowing at most six Map requests when both failure types occur. Invalid values are logged, and completed stages retain the failed responses in `map_failures` with their token usage included. Other evidence and resource checks remain enforced.

## 1200-second deadline retries

All three backends retry a request whose client-side 1200-second deadline expires
up to three additional times, each with a fresh 1200-second deadline. This covers
Root, chapter aggregation, contexts, approval, and full-file generation. Only the
affected request is resubmitted with the same prompt, attachments, and options;
completed work is reused. The fourth deadline expiry stops processing.

The client attempts to cancel the latest known active background job before each
retry, with a separate five-second cleanup limit. Caller cancellation does not
retry. The leaf Map deadline remains 300 seconds with up to three timeout retries;
it cancels the client call before this 1200-second retry mechanism applies.

Deadline retries and processing-error retries each have a separate allowance of
three and do not reset each other: at most four deadline windows and seven response
submissions when failures are mixed. The windows total up to 4800 seconds, plus
cleanup and concurrency-slot waiting. A timed-out call's token usage and its stage
and aggregate totals become `null`. `Responses deadline exceeded` logs the retry
count and `timeout_retries_exhausted`; `deadline_attempt` identifies each window.
See each backend README for cancellation, usage, and timeout details.

## Response processing retries

All three backends resubmit failed background Responses jobs for `server_error`, `rate_limit_exceeded`, and `vector_store_timeout`, up to three additional times. A code-less Azure processing error that explicitly recommends retrying is also recognized. Delays are 2, 4, and 8 seconds plus up to one second of jitter. Other terminal failures, including incomplete output, stop without processing retries.

The same prompt, attachments, candidate, and evidence are reused. A failed Root approval therefore retries only that approval request. Submission, polling, HTTP retries, and processing retries share the current 1200-second deadline attempt; a deadline retry starts a fresh window, and the outer 300-second leaf Map deadline still applies within each Map attempt. Usage includes failed attempts when reported, and becomes `null` if any attempt's usage is incomplete. See each backend README for error classification, timeout interaction, and logs.

Both MapReduce backends require at least two distinct source finding IDs per relation. Conditions within one finding belong in its decision; an empty relations array is valid. An otherwise valid reduction with a zero- or one-ID relation triggers up to two repairs of only that reduction, preserving the original input and full evidence validation. Failed outputs and diagnostics are retained in the successful stage's `reduction_failures` audit, and their token usage is included. See each backend README for limits and exhaustion behavior.

## Output token limits

All three backends set `max_output_tokens` explicitly. These budgets include visible output and reasoning tokens:

| Calls | Environment variable | Default | Application maximum |
| --- | --- | ---: | ---: |
| Full-file generation, MapReduce root reduction, and TBD synthesis | `LLM_MAX_OUTPUT_TOKENS` | 128000 | 128000 |
| MapReduce context, Map, intermediate reduction, and approval | `LLM_INTERMEDIATE_MAX_OUTPUT_TOKENS` | 64000 | 128000 |

Set these values in the selected backend's `.env` and restart the server. Existing environment values override the defaults. Use values supported by your Azure deployment; raising the application budget does not raise the model's own limit. The submission log includes the requested `max_output_tokens`. Incomplete responses still fail the request.

The MapReduce final-candidate byte budget defaults to 1 MiB, and the text-query budget defaults to 8 MiB to accommodate longer candidates and earlier specifications. These byte budgets are separate from model token limits.

## MapReduce configuration

These settings apply to both MapReduce examples and can be placed in the selected backend's `.env`:

| Environment variable | Default | Purpose |
| --- | --- | --- |
| `FILE_CHUNK_MAX_PAGES` | `8` | Maximum PDF pages per leaf chunk, capped at 100. |
| `FILE_CHUNK_MAX_SLIDES` | `8` | Maximum PPTX slides per leaf chunk, capped at 100. |
| `LLM_MAX_PARALLEL_CHUNK_REQUESTS` | `8` (one-level), `16` (two-level) | One-level concurrent API calls, capped at 8; two-level fallback for per-level settings, capped at 16. |
| `LLM_MAX_APPROVAL_ATTEMPTS` | `2` (one-level), `8` (two-level) | Complete attempts per specification, including the initial attempt; capped at 5 for one-level and 8 for two-level. |
| `LLM_MAX_APPROVAL_REVIEW_ATTEMPTS` | `3` | Review calls per candidate for missing, duplicate, or unknown review IDs, including the initial call; capped at 5. |

The two-level backend has separate settings for chapter work and leaf Maps:

```dotenv
# Level 1: chapter contexts and aggregation batches across all chapters
LLM_MAX_PARALLEL_LEVEL1_REQUESTS=16
# Level 2: leaf Map requests across all chapters
LLM_MAX_PARALLEL_LEVEL2_REQUESTS=16
```

Each level accepts 1–16 concurrent requests and independently falls back to
`LLM_MAX_PARALLEL_CHUNK_REQUESTS` when its setting is unset, blank, or invalid.
Explicit level values take precedence, including at the API client. Batches in
the same chapter round share the level 1 limit with other chapters; the next round
waits for the current round to finish. All chapter contexts finish before Map starts.
Each chapter then starts aggregation once its own Maps have succeeded, overlapping
with other chapters' Maps. Root waits for all Maps and chapter aggregations to
succeed. Any Map or chapter failure cancels the remaining work before Root runs.
The shared API concurrency cap remains the larger of the two level limits.
Root calls remain sequential. The eight documents also run sequentially,
with each stage receiving the earlier completed specifications.
Set the values in the two-level backend's `.env`
and restart it to apply changes.

Additional query, intermediate-output, and audit-storage budgets are documented in the individual backend READMEs. Splitting is limited to 256 chunks and 150 MiB of combined chunk data. Evidence validation checks reported coverage and references; it does not establish the correctness of the model's interpretation.

## Source layout and tests

Each example has a self-contained `be/` directory:

| Path within `be/` | Purpose |
| --- | --- |
| `README.md` | Backend-specific setup, workflow, configuration, and API documentation. |
| `.env-sample`, `.env` | Configuration template and local runtime settings. |
| `app.py`, `requirements.txt` | Application entry point and Python dependencies. |
| `server/application.py`, `server/security.py` | Authenticated health/upload endpoints and API-key validation. |
| `server/services.py`, `server/input_files.py` | Azure service configuration and Responses file-input handling. |
| `server/chat.py` | Selects full-file generation or the MapReduce depth. |
| `server/specifications.py` | Defines the eight stages and assembles their output. |
| `server/decision_register.py` | Generates the final TBD register from specifications 01–07 only. |
| `server/output_files.py` | Saves incremental Markdown specifications under top-level `res/`. |
| `server/file_chunks.py`, `server/hierarchy.py`, `server/evidence.py` | MapReduce only: splitting, orchestration, and evidence validation. |
| `server/pdf_sections.py`, `server/chapter_reduction.py` | Two-level only: PDF chapter/section splitting and bounded chapter aggregation. |
| `server/concurrency.py` | Two-level only: independent chapter and leaf request limits with legacy configuration fallback. |
| `prompt/`, `prompt/stages/` | Shared rules, eight stage templates, and MapReduce phase templates. Two-level root and chapter summary/judgment prompts are separate. |
| `plugins/talks_with_responses/` | Azure OpenAI Responses client and polling. |
| `tests/` | Unit and integration tests using mocked API traffic and generated test documents. |

After installing the selected backend's dependencies, run its tests from that `be/` directory:

```bash
python -m unittest discover -s tests -v
```

Repeat from each backend directory to check all three examples. The tests cover specification sequencing, upload handling, API requests, logs, and token usage. The MapReduce suites additionally cover file splitting, evidence coverage, approval retries, concurrency, and resource limits. They do not require live Azure OpenAI calls.
