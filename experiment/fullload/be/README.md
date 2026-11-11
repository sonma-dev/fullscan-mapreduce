# Full-File Specification Generation

Upload a PDF or PPTX file (up to 50 MiB) to `POST /upload` to generate seven specifications and a TBD register through the OpenAI Responses API. Stages 01–07 use source files through `input_file`; stage 8 uses only their completed Markdown. All eight generated documents, including titles, headings, and explanatory text, use English Markdown; server logs are in English.

## Setup

Use Python 3.11 or later in an activated virtual environment. From the repository root, enter this backend directory and install its dependencies and Gunicorn:

```bash
cd experiment/fullload/be
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
```

`API_KEY` authenticates requests to this backend and must contain at least 32 characters. It is separate from `AZURE_OPENAI_API_KEY`, which authenticates the development backend to Azure OpenAI. The application loads `.env` automatically at startup.

`AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` is accepted as a fallback deployment setting. When `APP_ENV` is `prod`, `production`, or `staging`, the backend uses Microsoft Entra ID through managed identity; `AZURE_CLIENT_ID` can select a user-assigned identity. The current startup validation still requires `AZURE_OPENAI_API_KEY` to be set. Choose a deployment that supports Responses API file input and background execution for the document types you use.

## Start the server

Run this exact command from `experiment/fullload/be/`:

```bash
gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app --bind localhost:8001 2>&1 | tee ../../../_test_fullload-20261108.log
```

The server listens on `http://localhost:8001`. Both standard output and standard error are displayed in the terminal and written to `_test_fullload-20261108.log` in the repository root. `tee` overwrites that log on each run. All three backend examples use the same port, so run one at a time on this address.

## POST a document with curl

Open a second terminal in `experiment/fullload/be/`. Set the client-side `API_KEY` to the same value configured in the backend's `.env`; the server's automatic `.env` loading does not export it into this terminal.

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

Stages 01–07 send the entire original file and all earlier specifications to the LLM using Responses API `input_file`. Stage 8 receives only the seven completed Markdown specifications. A successful request makes eight response-creation calls in total. Polling and SDK transport retries are additional HTTP requests.

This backend has no approval calls, `approved` checks, or approval retry loop. Each completed, non-empty specification advances directly to the next stage. Approval settings apply only to the MapReduce backends.

Each call explicitly sets `max_output_tokens` to 128000 by default, including visible output and reasoning tokens. Configure `LLM_MAX_OUTPUT_TOKENS` in `.env` and restart the server to change it; the application maximum is 128000. Existing environment values override the default. Choose a value supported by your Azure deployment. An incomplete response still fails the request.

The next stage begins only after the current stage succeeds. A failure stops the sequence before later specifications run.

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
| `timing_ms.llm` | Elapsed time for specification generation, including stage output writes. |
| `timing_ms.total` | Handler time including stage saves and final Markdown preparation, before final JSON serialization. |

Each `specifications[].content` is an independent English Markdown document with its own H1 title. Per-stage `usage` and `elapsed_ms` describe that specification. Missing token counts remain `null`, and the corresponding aggregate fields also become `null`.

## Output files

After the first stage completes, each request creates a unique directory under the repository's top-level `res/`. The directory name includes `fullload`, the run-start timestamp in **JST (UTC+09:00)**, and a unique suffix. Each completed stage writes one UTF-8 Markdown file before the next stage starts. A successful run leaves these eight files:

```text
res/fullload_20261110183045_<unique suffix>/
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

A retry resends the current specification request with the original full `input_file` and previous specifications. Completed stages are not regenerated. On cancellation or timeout, the client attempts to cancel the latest known active background response, with a separate five-second cleanup limit; remote cancellation is best effort.

## English server logs

`Stage output saved` records progress such as `completed=2/8`, the Markdown file count, and the absolute output directory after every completed stage. `Output files saved` records the final Markdown file count and directory.

`Responses request submitting` includes the requested `max_output_tokens`.

Stage start, completion, failure, and cancellation logs identify `file_name`, `step`, `stage`, the English specification name, and its dedicated `prompt`. Each `Specification LLM query submitting` event records `phase=generation` and the query size. Completion events include elapsed time and input, output, and total token counts. `Upload completed` records the request-wide totals.

```text
Specification LLM query submitting: file_name=sample.pdf step=1/8 stage=screen_functions specification="Screen Function Specification" prompt=stages/screen_functions.jinja2 phase=generation chunk=none query_chars=1234
Specification stage completed: file_name=sample.pdf step=1/8 stage=screen_functions specification="Screen Function Specification" prompt=stages/screen_functions.jinja2 elapsed_ms=1234 input_tokens=1000 output_tokens=500 total_tokens=1500
```

The numbers above are illustrative. Specification bodies are returned in the HTTP response rather than written to the server log.

## Code, prompts, and tests

Stage order and names are defined in `server/specifications.py`. Dedicated requirements live in `prompt/stages/*.jinja2`, with shared evidence and consistency rules in `prompt/specification_system.jinja2`. The full-file generation flow is in `server/chat.py`.

Run the test suite from this `be/` directory:

```bash
python -m unittest discover -s tests -v
```

Tests mock API traffic and verify the eight-stage order, propagation of earlier outputs, token totals, English logs, upload behavior, and stopping after a failure.
