# ChatGPT Retrieval Plugin

The ChatGPT Retrieval Plugin is a FastAPI-based service that provides a retrieval API for storing, querying, and managing documents in a vector database of your choice. It exposes endpoints for upserting documents (including file uploads), performing semantic search queries with metadata filtering, and deleting documents. The plugin can be used with ChatGPT plugins to give the model access to up-to-date information, run computations, or interact with third-party services in response to a user's request.

> **Note:** The ChatGPT plugins mechanism described in this repository is deprecated. See [docs/deprecated/plugins.md](docs/deprecated/plugins.md) for details. The repository also includes guidance for using the retrieval API via [function calling](examples/function-calling/README.md) with the Chat Completions API and the Assistants API.

## Features

- **Flexible vector database backends** — Choose from a wide range of supported providers:
  - AnalyticDB
  - Azure Cosmos DB
  - Azure Cognitive Search
  - Chroma
  - Elasticsearch
  - LlamaIndex
  - Milvus / Zilliz
  - MongoDB Atlas
  - Pinecone
  - Postgres (with pgvector)
  - Qdrant
  - Redis
  - Supabase
  - Weaviate
- **Document ingestion** — Upload files (PDF, DOCX, PPTX, and more) via `/upsert-file`, or send structured documents via `/upsert`. Documents are automatically chunked and embedded using OpenAI embeddings.
- **Semantic search with metadata filtering** — Query the datastore with natural language queries, optionally filtering by `document_id`, `source`, `source_id`, `author`, and date ranges (`start_date` / `end_date`).
- **PII detection** — Includes a PII detection service (`services/pii_detection.py`) for handling sensitive data.
- **Plugin manifest and OpenAPI schema** — Serves the required `/.well-known/ai-plugin.json` and `/.well-known/openapi.yaml` files for ChatGPT plugin registration.
- **Authentication** — Bearer token authentication is enforced by default in the production server.

## Project Structure

```
├── server/                  # Production FastAPI application
├── local_server/            # Localhost server for testing plugins in ChatGPT
├── datastore/               # Datastore interface and provider implementations
│   └── providers/           # One module per vector database provider
├── services/                # Chunking, file parsing, embeddings, metadata, PII, dates
├── models/                  # Pydantic models and API request/response types
├── docs/                    # Provider setup guides and deployment docs
├── examples/                # Docker configs, auth methods, notebooks, memory example
├── scripts/                 # JSON / JSONL / ZIP document processing utilities
├── tests/                   # Provider unit and integration tests
├── .well-known/             # Plugin manifest, logo, and OpenAPI schema
├── Dockerfile
├── Makefile
└── pyproject.toml
```

## Requirements

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management
- An OpenAI API key (for generating embeddings)
- A vector database of your choice (see [Configuration](#configuration))

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/openai/chatgpt-retrieval-plugin.git
cd chatgpt-retrieval-plugin
```

### 2. Install dependencies

```bash
poetry install
```

If you plan to use Postgres, install with the `postgresql` extra:

```bash
poetry install --extras postgresql
```

### 3. Configure environment variables

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Required environment variables include:

- `DATASTORE` — the name of your chosen vector database provider (e.g. `pinecone`, `qdrant`, `postgres`, `redis`, `chroma`, `weaviate`, `milvus`, `zilliz`, `mongodb_atlas`, `supabase`, `pgvector`, `azuresearch`, `azurecosmosdb`, `elasticsearch`, `analyticdb`, `llama`)
- `OPENAI_API_KEY` — your OpenAI API key
- `BEARER_TOKEN` — the bearer token used to authenticate requests to the API
- `EMBEDDING_DIMENSION` — embedding vector dimension (provider-dependent; e.g. Qdrant defaults to 256)

Additional provider-specific variables (e.g. `PINECONE_API_KEY`, `PINECONE_ENVIRONMENT`, `PINECONE_INDEX` for Pinecone; `QDRANT_URL`, `QDRANT_PORT`, `QDRANT_API_KEY`, `QDRANT_COLLECTION` for Qdrant; `PG_HOST`, `PG_PORT`, `PG_DB`, `PG_USER`, `PG_PASSWORD` for Postgres; `MONGODB_URI`, `MONGODB_DATABASE`, `MONGODB_COLLECTION`, `MONGODB_INDEX` for MongoDB Atlas) are documented in the per-provider setup guides under [docs/providers/](docs/providers/).

### 4. Set up your vector database

Each provider has its own setup guide in [docs/providers/](docs/providers/). For local development, Docker Compose files are provided for several providers:

- `examples/docker/qdrant/docker-compose.yaml`
- `examples/docker/elasticsearch/docker-compose.yaml`
- `examples/docker/milvus/docker-compose.yaml`
- `examples/docker/redis/docker-compose.yml`
- `tests/datastore/providers/weaviate/docker-compose.yml`

For example, to start a local Redis Stack server:

```bash
docker compose -f examples/docker/redis/docker-compose.yml up
```

### 5. Run the server

**Production server** (bearer-token-protected, serves `.well-known` files):

```bash
poetry run start
```

This runs `server.main:app` on `0.0.0.0:8000`.

**Local development server** (for testing a localhost plugin in ChatGPT — no auth, CORS configured for `localhost:3333` and `chat.openai.com`):

```bash
poetry run dev
```

This runs `local_server.main:app` on `localhost:3333`.

**Docker:**

```bash
docker build -t chatgpt-retrieval-plugin .
docker run -p 8080:8080 \
  -e DATASTORE=... \
  -e OPENAI_API_KEY=... \
  -e BEARER_TOKEN=... \
  chatgpt-retrieval-plugin
```

The container listens on the `PORT` environment variable, falling back to `WEBSITES_PORT`, then to `8080` (the default for Fly.io). This makes it compatible with Heroku, Azure App Services, and Fly.io out of the box.

## Usage

The API exposes four main endpoints:

### `POST /upsert-file`

Upload a file for ingestion. The file is parsed, chunked, embedded, and stored.

```
POST /upsert-file
Content-Type: multipart/form-data

file: <binary file>
metadata: (optional) JSON string of document metadata
```

### `POST /upsert`

Insert structured documents directly.

```json
{
  "documents": [
    {
      "text": "Your document text",
      "metadata": {
        "source": "file",
        "source_id": "example",
        "url": "https://example.com",
        "created_at": "2023-01-01",
        "author": "Jane Doe"
      }
    }
  ]
}
```

### `POST /query`

Search the datastore. Accepts an array of query objects, each with a `query` string, an optional `filter`, and an optional `top_k` (default 3). Complex questions should be broken down into sub-questions; refine results by criteria such as time or source.

```json
{
  "queries": [
    {
      "query": "What is the meaning of life?",
      "filter": { "source": "file", "author": "Jane Doe" },
      "top_k": 3
    }
  ]
}
```

Responses include the matching document chunks with their similarity scores and metadata.

### `DELETE /delete`

Delete documents by one of three criteria (at least one is required):

```json
{ "delete_all": true }
```

```json
{ "ids": ["<document-or-chunk-id>"] }
```

```json
{ "filter": { "author": "Jane Doe", "start_date": "2023-01-01" } }
```

All authenticated endpoints require an `Authorization: Bearer <BEARER_TOKEN>` header (except on the local server, which has no authentication).

### OpenAPI schema

When running locally, a sub-application exposes a query-only OpenAPI schema at `http://0.0.0.0:8000/sub/openapi.json`. The full OpenAPI schema and plugin manifest are served at `/.well-known/openapi.yaml` and `/.well-known/ai-plugin.json`. Remember to update the plugin URL in both the manifest and the schema to your deployed URL.

## Configuration

### Choosing a datastore

The `DATASTORE` environment variable selects the provider, and `datastore/factory.py` instantiates the corresponding implementation. All providers implement the same `DataStore` interface (`datastore/datastore.py`), so switching providers only requires changing environment variables and redeploying.

### Reducing bundle size

Before deploying, you can remove unused provider dependencies from `pyproject.toml` to reduce image size. A per-provider list of packages to remove is documented in [docs/deployment/removing-unused-dependencies.md](docs/deployment/removing-unused-dependencies.md). The Dockerfile handles dependency installation automatically via `poetry export`, so there is no need to run `poetry lock` / `poetry install` after editing.

### Authentication methods

Examples of alternative authentication approaches (in `examples/authentication-methods/`) include:

- **No auth** — a version of `server/main.py` with authentication removed
- **OAuth**
- **Service-level HTTP**
- **User-level HTTP**

### Memory example

The [examples/memory/](examples/memory/) directory contains a variant of the server that exposes the upsert endpoint to ChatGPT as well, allowing the model to save information from the conversation back into the vector database.

## Deployment

The repository includes a `Dockerfile` that builds a container running the server with Uvicorn. Deployment guides are available for:

- **Fly.io** — [docs/deployment/flyio.md](docs/deployment/flyio.md) (uses port 8080; set environment variables with `flyctl secrets set`)
- **Heroku** — [docs/deployment/heroku.md](docs/deployment/heroku.md) (uses the `Makefile` targets `make heroku-login` and `make heroku-push`; set `HEROKU_APP` in the Makefile first)
- **Render** — [docs/deployment/render.md](docs/deployment/render.md) (one-click deploy via Render's maintained fork, with a self-hosted Weaviate backend)
- **Other options** — [docs/deployment/other-options.md](docs/deployment/other-options.md) covers Azure Container Apps, Google Cloud Run, and AWS Elastic Container Service

After deploying, update the plugin URL in `/.well-known/ai-plugin.json` and `/.well-known/openapi.yaml` to your app's URL and redeploy.

## Data Ingestion Scripts

Utility scripts in `scripts/` help prepare documents for ingestion:

- `scripts/process_json/` — process a JSON file of documents
- `scripts/process_jsonl/` — process a JSONL file of documents
- `scripts/process_zip/` — process a ZIP archive of files

Each has its own README with usage instructions and an example input file.

## Examples

- `examples/function-calling/` — using the retrieval plugin's `query`/`upsert` endpoints as tools with the Chat Completions API and the Assistants API, including full tool definitions
- `examples/memory/` — a server variant enabling the model to save chat content to the vector database
- `examples/providers/` — Jupyter notebooks demonstrating semantic search (and filtering) against Azure Cosmos DB, Elasticsearch, MongoDB, Pinecone, Redis, and Supabase
- `examples/docker/` — local vector database setups for Qdrant, Elasticsearch, Milvus, and Redis, including sample documents and queries

## Development

The project uses Poetry for dependency management. The core abstractions are:

- `datastore/datastore.py` — the `DataStore` abstract interface (`upsert`, `query`, `delete`)
- `datastore/providers/*_datastore.py` — provider-specific implementations
- `services/chunks.py` — document chunking logic
- `services/file.py` — file parsing and extraction
- `services/openai.py` — embedding generation
- `models/models.py` / `models/api.py` — Pydantic models for documents, chunks, metadata, and API payloads

### Adding a new datastore provider

1. Create a new module in `datastore/providers/` implementing the `DataStore` interface (or a shared base such as `PgVectorDataStore` for Postgres-based providers).
2. Register the provider in `datastore/factory.py`.
3. Add a setup guide under `docs/providers/`.
4. Add tests under `tests/datastore/providers/`.

## Testing

Tests are located in `tests/datastore/providers/` and cover each provider implementation. Run the test suite with:

```bash
poetry run pytest
```

The pytest configuration in `pyproject.toml` enables `asyncio_mode="auto"` and adds the repository root to `pythonpath`, so async tests run automatically. Test dependencies include `pytest`, `pytest-cov`, `pytest-asyncio`, and `httpx`. Some providers (e.g. Weaviate, MongoDB Atlas) require a running database instance — use the provided `docker-compose.yml` files or integration tests (`test_integration.py`) accordingly.

## Contributing

Contributions are welcome. When submitting a pull request, follow the checklist in [.github/pull_request_template.md](.github/pull_request_template.md):

1. Label the PR type in the title (e.g. `[Bugfix]`, `[Feature]`, `[Enhancement]`, `[Refactor]`, `[Documentation]`).
2. Provide a short description and link related issues with `Fixes` or `Closes`.
3. Create a new branch based on the latest `main`.
4. Keep code changes minimal and focused.
5. Write clear commit messages.
6. Include unit and/or integration tests for new code.
7. Update relevant documentation.
8. Request a review from at least one contributor or maintainer.
9. For large or complex PRs, submit a brief video walkthrough.

PR branches should follow the naming convention `<type>/<short-description>-<issue-number>`, e.g. `feature/advanced-chunking-strategy-123`.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE). Copyright © 2023 OpenAI.
