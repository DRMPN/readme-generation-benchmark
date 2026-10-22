# GPT Researcher

GPT Researcher is an autonomous agent for online research. Given a task, it plans sub-questions, searches the web (or other sources), scrapes and filters the results, and writes a cited report. It is available as a Python library, a CLI, a FastAPI server with a WebSocket interface, a Next.js frontend, a LangGraph multi-agent workflow, and an MCP integration.

![GPT Researcher architecture](docs/static/img/architecture.png)

## Features

- **Autonomous research loop**: plans sub-questions, gathers sources, and aggregates context before writing (`gpt_researcher/agent.py`, `gpt_researcher/skills/`).
- **Multiple report types**: `research_report`, `detailed_report`, `resource_report`, `outline_report`, `custom_report`, `subtopic_report`, and `deep` (deep research).
- **Tone options**: 15 tones in the CLI, including `objective`, `formal`, `analytical`, and `critical`.
- **Many search backends**: 14 retriever modules (see [Retrievers](#retrievers)), selectable individually or as a comma-separated list.
- **Pluggable LLMs**: 20 provider identifiers in the generic LLM layer, configured as `provider:model` strings (see [LLM providers](#llm-providers)).
- **Local and hybrid research**: report from your own documents (`DOC_PATH`) alongside or instead of the web.
- **Multiple scrapers**: BeautifulSoup, headless browser, NoDriver, Tavily Extract, Firecrawl, and arXiv/PDF handling.
- **Deep research**: a recursive tree of concurrent searches with configurable breadth, depth, and concurrency.
- **Detailed reports**: a STORM-inspired process that generates subtopic reports and assembles them with an introduction and table of contents.
- **Output formats**: Markdown, PDF, and DOCX (the server and LangGraph workflow write all three; the CLI writes Markdown).
- **MCP support**: connect Model Context Protocol servers as a research source.
- **Multi-agent workflow**: a LangGraph-based team (editor, researcher, reviewer, reviser, writer, publisher) in `multi_agents/`.

## Requirements

- Python 3.11 or newer (`requires-python = ">=3.11, <4"` in `pyproject.toml`).
- An LLM API key. The defaults use OpenAI models.
- A search API key. The default retriever is Tavily (`RETRIEVER` defaults to `tavily`).
- Docker and Docker Compose, if you use the container setup.
- Node.js, if you run the Next.js frontend outside Docker.

## Installation

Clone the repository and install the Python dependencies:

```bash
git clone https://github.com/assafelovic/gpt-researcher.git
cd gpt-researcher
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` is the dependency list used by the Dockerfile. `pyproject.toml` and `setup.py` also declare the `gpt-researcher` package.

## Configuration

Copy the example environment file and fill in your keys:

```bash
cp .env.example .env
```

`.env.example` contains:

```bash
OPENAI_API_KEY=
TAVILY_API_KEY=
DOC_PATH=./my-docs

# NEXT_PUBLIC_GPTR_API_URL=http://0.0.0.0:8000  # Defaults to localhost:8000 if not set
```

The CLI and server call `load_dotenv()`, so values in `.env` are loaded automatically.

### Default models

From `gpt_researcher/config/variables/default.py`:

| Setting | Default |
|---|---|
| `FAST_LLM` | `openai:gpt-4o-mini` |
| `SMART_LLM` | `openai:gpt-4.1` |
| `STRATEGIC_LLM` | `openai:o4-mini` |
| `EMBEDDING` | `openai:text-embedding-3-small` |
| `RETRIEVER` | `tavily` |
| `SCRAPER` | `bs` |
| `REPORT_SOURCE` | `web` |
| `REPORT_FORMAT` | `APA` |
| `TEMPERATURE` | `0.4` |
| `TOTAL_WORDS` | `1200` |
| `MAX_SEARCH_RESULTS_PER_QUERY` | `5` |
| `MAX_ITERATIONS` | `3` |
| `DOC_PATH` | `./my-docs` |

### Overriding settings with environment variables

Each setting in the defaults table can be overridden with an environment variable of the same name. The values are converted to the type of the default (booleans accept `true/1/yes/on`; lists and dicts are parsed as JSON). For example:

```bash
SMART_LLM=openai:gpt-4o
TEMPERATURE=0.2
RETRIEVER=tavily,duckduckgo
```

Set a model with `provider:model`, for example `anthropic:claude-3-5-sonnet-latest` or `openrouter:<model-id>`. The provider must be one of the supported providers listed below.

`REASONING_EFFORT` accepts `high`, `medium` (default), or `low`. It applies to OpenAI reasoning models such as `o3` and `o4-mini`.

Deprecated variables `LLM_PROVIDER`, `FAST_LLM_MODEL`, `SMART_LLM_MODEL`, and `EMBEDDING_PROVIDER` still work but emit a `FutureWarning`. Use `FAST_LLM`, `SMART_LLM`, and `EMBEDDING` instead.

### Retrievers

Set `RETRIEVER` to one name, or a comma-separated list of names. The valid names are the modules in `gpt_researcher/retrievers/`:

| Retriever | Environment variables |
|---|---|
| `tavily` | `TAVILY_API_KEY` |
| `duckduckgo` | none found in the module |
| `google` | `GOOGLE_API_KEY`, `GOOGLE_CX_KEY` |
| `bing` | `BING_API_KEY` |
| `serper` | `SERPER_API_KEY` |
| `serpapi` | `SERPAPI_API_KEY` |
| `searchapi` | `SEARCHAPI_API_KEY` |
| `searx` | `SEARX_URL` |
| `exa` | `EXA_API_KEY` |
| `arxiv` | none found in the module |
| `semantic_scholar` | none found in the module |
| `pubmed_central` | `NCBI_API_KEY` |
| `custom` | `RETRIEVER_ENDPOINT`; `RETRIEVER_ARG_*` variables are passed as parameters |
| `mcp` | configured through `MCP_SERVERS` (see [MCP](#mcp-model-context-protocol)) |

An invalid retriever name in `RETRIEVER` causes a warning, and the code falls back to `tavily`.

### LLM providers

The generic LLM layer (`gpt_researcher/llm_provider/generic/base.py`) supports these provider identifiers:

`openai`, `anthropic`, `azure_openai`, `cohere`, `google_vertexai`, `google_genai`, `fireworks`, `ollama`, `together`, `mistralai`, `huggingface`, `groq`, `bedrock`, `dashscope`, `xai`, `deepseek`, `litellm`, `gigachat`, `openrouter`, `vllm_openai`, `aimlapi`

Provider-specific variables read by the code:

| Provider | Environment variables |
|---|---|
| `openai` | `OPENAI_API_KEY`; optional `OPENAI_BASE_URL` |
| `openrouter` | `OPENROUTER_API_KEY`; optional `OPENROUTER_LIMIT_RPS` (default `1.0` requests per second) |
| `deepseek` | `DEEPSEEK_API_KEY` |
| `ollama` | `OLLAMA_BASE_URL` |
| `vllm_openai` | `VLLM_OPENAI_API_KEY`, `VLLM_OPENAI_API_BASE` |
| `aimlapi` | `AIMLAPI_API_KEY` |
| `azure_openai` | `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION` (embeddings) |

Other providers rely on the environment variables expected by their LangChain integrations. The generic layer installs a missing LangChain integration package at runtime if it is not present.

For embeddings, `EMBEDDING` accepts the same `provider:model` format with these providers: `openai`, `azure_openai`, `cohere`, `gigachat`, `google_vertexai`, `google_genai`, `fireworks`, `ollama`, `together`, `mistralai`, `huggingface`, `nomic`, `voyageai`, `dashscope`, `custom`, `bedrock`, and `aimlapi`. The `custom` provider uses an OpenAI-compatible endpoint at `OPENAI_BASE_URL` (default `http://localhost:1234/v1`). `voyageai` requires `VOYAGE_API_KEY`.

### Scrapers

Set `SCRAPER` to one of `bs` (default), `browser`, `nodriver`, `arxiv`, `tavily_extract`, or `firecrawl`. PDF links and arXiv links are routed to dedicated handlers automatically.

- `tavily_extract` uses `TAVILY_API_KEY`.
- `firecrawl` uses `FIRECRAWL_API_KEY`, and reads `FIRECRAWL_SERVER_URL`.

### Report sources

`REPORT_SOURCE` (or the `report_source` argument) accepts `web`, `local`, `hybrid`, `azure`, `langchain_documents`, `langchain_vectorstore`, and `static`. Local and hybrid sources read documents from `DOC_PATH`. Azure reads `AZURE_CONTAINER_NAME` and `AZURE_CONNECTION_STRING`.

## Usage

### Command line

`cli.py` runs research and writes the report to `outputs/<uuid>.md`.

```bash
python cli.py "What are the latest developments in quantum computing?" \
  --report_type research_report \
  --tone objective \
  --query_domains arxiv.org,nature.com
```

Arguments:

- `query` (required): the research question.
- `--report_type` (required): one of `research_report` (summary, about 2 minutes), `detailed_report` (longer, about 5 minutes), `resource_report`, `outline_report`, `custom_report`, `subtopic_report`, or `deep`.
- `--tone` (optional, default `objective`): `objective`, `formal`, `analytical`, `persuasive`, `informative`, `explanatory`, `descriptive`, `critical`, `comparative`, `speculative`, `reflective`, `narrative`, `humorous`, `optimistic`, or `pessimistic`.
- `--query_domains` (optional): comma-separated domains to restrict search to.
- `--encoding` (optional, default `utf-8`): encoding for the output file.

### Python library

```python
import asyncio
from gpt_researcher import GPTResearcher

async def main():
    researcher = GPTResearcher(
        query="What are the latest developments in quantum computing?",
        report_type="research_report",
    )
    await researcher.conduct_research()
    report = await researcher.write_report()
    print(report)

asyncio.run(main())
```

`GPTResearcher` also accepts `tone`, `report_source`, `query_domains`, `headers`, `mcp_configs`, `verbose`, and `config_path`, a path to a JSON configuration file. Helper methods used in the code include `get_source_urls()`, `get_research_sources()`, `get_costs()`, and `get_research_images()`.

### Web server

Start the FastAPI server:

```bash
python main.py
```

This runs Uvicorn on `http://0.0.0.0:8000`. It also writes logs to `logs/app.log`. Alternatively, run `uvicorn backend.server.server:app --host 0.0.0.0 --port 8000`, which matches the `Procfile`.

Routes defined in `backend/server/server.py`:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/` | Serves the bundled HTML interface from `frontend/index.html` |
| `POST` | `/report/` | Starts a report. Body fields: `task`, `report_type`, `report_source`, `tone`, `repo_name`, `branch_name`, and optional `headers`, `generate_in_background` (default `true`). |
| `GET` | `/report/{research_id}` | Returns the generated `.docx` report |
| `GET` | `/files/` | Lists files in `DOC_PATH` |
| `POST` | `/upload/` | Uploads a document to `DOC_PATH` |
| `DELETE` | `/files/{filename}` | Deletes a document from `DOC_PATH` |
| `POST` | `/api/multi_agents` | Intended to run the multi-agent workflow on a fixed query. **Currently broken:** `backend/server/server_utils.py` calls `run_research_task` and `stream_output` without importing them, so the request fails with a `NameError`. |
| `WS` | `/ws` | Interactive research over WebSocket |

The WebSocket endpoint accepts text messages: `ping` (replies `pong`), `start <json>` (runs research with fields such as `task`, `report_type`, `tone`, `report_source`, `source_urls`, `document_urls`, `query_domains`, `headers`, `mcp_enabled`, `mcp_strategy`, and `mcp_configs`), `chat <json>`, and `human_feedback <json>`. Only one task runs per connection at a time. Note that `human_feedback` is currently a placeholder: the handler logs the feedback and contains a TODO for forwarding it.

CORS is configured to allow only `http://localhost:3000`.

### Next.js frontend

The React/Next.js UI is in `frontend/nextjs/`. Its `package.json` defines `dev`, `build`, and `start` scripts:

```bash
cd frontend/nextjs
npm install
npm run dev
```

Set `NEXT_PUBLIC_GPTR_API_URL` to the backend URL if it is not `http://localhost:8000`.

### Deep research

Use `report_type="deep"` (or `--report_type deep` in the CLI). Deep research explores each query as a tree:

- `DEEP_RESEARCH_BREADTH` (default `3`): parallel paths at each level.
- `DEEP_RESEARCH_DEPTH` (default `2`): levels to explore.
- `DEEP_RESEARCH_CONCURRENCY` (default `4`): maximum concurrent operations.

Failed branches are skipped, and the run continues. Deep research makes many more LLM and search calls than a basic report, so expect higher cost and runtime. See `backend/report_type/deep_research/README.md`.

### Detailed reports

`detailed_report` generates an initial report, derives subtopics, writes a report for each subtopic while avoiding repeated headers, and assembles an introduction, table of contents, and the subtopic sections. See `backend/report_type/detailed_report/README.md`.

### Multi-agent workflow

`multi_agents/` contains a LangGraph workflow with eight roles: human, chief editor, researcher, editor, reviewer, reviser, writer, and publisher. Configure the run in `multi_agents/task.json`, then:

```bash
cd multi_agents
pip install -r requirements.txt
python main.py
```

The workflow uses `SMART_LLM` only. Output is written to the `output` directory in Markdown, PDF, and DOCX depending on `publish_formats`. See `multi_agents/README.md` for the `task.json` fields. The `langgraph.json` file at the repository root can be used with `langgraph up`.

### MCP (Model Context Protocol)

Set `RETRIEVER=mcp` or pass `mcp_configs` to connect MCP servers as a research source. Each server entry can use stdio (`command` and `args`), WebSocket (`connection_url` starting with `ws://` or `wss://`), or HTTP (`connection_url` starting with `http://` or `https://`). Server-level options are `name`, `command`, `args`, `connection_url`, `connection_type`, `connection_token`, `tool_name`, and `env`. Requires `langchain-mcp-adapters`. See `gpt_researcher/mcp/README.md`.

## Docker

Build and run the backend and frontend with Docker Compose. The `docker-compose.yml` file defines:

- `gpt-researcher`: the API server on port `8000`. Mounts `my-docs`, `outputs`, and `logs` from the project directory.
- `gptr-nextjs`: the Next.js frontend on port `3000`.

```bash
cp .env.example .env
docker compose up --build
```

The backend image is built from `Dockerfile`. It installs Chromium, ChromeDriver, Firefox, and Geckodriver for browser-based scraping, then runs `uvicorn main:app` on port `8000`. `Dockerfile.fullstack` is also present.

The Compose file has a `test` profile that runs `tests/report-types.py` and `tests/vector-store.py`:

```bash
docker compose --profile test run --rm gpt-researcher-tests
```

A `discord-bot` service is defined under the `discord` profile. It needs `DISCORD_BOT_TOKEN` and `DISCORD_CLIENT_ID`.

## Output

- **CLI**: `outputs/<uuid>.md`.
- **Server and WebSocket**: Markdown, DOCX, and PDF files under `outputs/`, plus a JSON log of events and content (`outputs/task_*.json`). Filenames are sanitized from the task text.
- **Multi-agent workflow**: Markdown, PDF, and DOCX depending on `publish_formats`.
- **Application log**: `logs/app.log` when started through `main.py`.

## Project structure

```
gpt_researcher/        Core library: agent, skills, retrievers, scrapers, LLM and embedding providers, config, MCP
backend/               FastAPI server, WebSocket manager, report types (basic, detailed, deep research), chat
frontend/              Bundled HTML interface (index.html) and the Next.js app (nextjs/)
multi_agents/          LangGraph multi-agent workflow
mcp-server/            Pointer to the separate gptr-mcp repository
evals/                 SimpleQA evaluation harness
tests/                 Test and check scripts
docs/                  Documentation site sources, blog posts, and the npm package
cli.py                 Command-line interface
main.py                Server entry point
```

## Testing

The pytest configuration in `pyproject.toml` sets `testpaths = ["tests"]` and `python_files = "test_*.py"`. Most of the files in `tests/` are standalone scripts that exercise specific components (for example `tests/test-your-llm.py` and `tests/test-your-retriever.py`). Run them with `python -m pytest` or `python tests/<file>.py` after configuring the required API keys.

To evaluate factual accuracy, `evals/simple_evals/` runs a SimpleQA-based evaluation:

```bash
cd evals/simple_evals
pip install -r requirements.txt
python run_eval.py --num_examples 10
```

The grader defaults to a GPT-4-class OpenAI model. See `evals/README.md`.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community guidelines. Bug reports and feature requests use the templates in `.github/ISSUE_TEMPLATE/`.

## License

Released under the [MIT License](LICENSE).

## Citation

A `citation.cff` file is included in the repository.

## Links

- Documentation: https://docs.gptr.dev
- Repository: https://github.com/assafelovic/gpt-researcher
- Author: Assaf Elovic (assaf.elovic@gmail.com)
