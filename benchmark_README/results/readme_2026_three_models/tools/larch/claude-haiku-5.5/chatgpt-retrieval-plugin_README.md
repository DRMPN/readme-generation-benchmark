# ChatGPT Retrieval Plugin

A ChatGPT retrieval plugin that lets ChatGPT search and reason over your own documents. It exposes a REST API for upserting, querying, and deleting document chunks, backed by a vector database of your choice. Its OpenAPI spec and manifest allow ChatGPT to call it as a plugin.

> **Note:** This README was written from the repository's file layout. Confirm environment variable names, provider-specific options, and Makefile targets against the source code and `docs/` before relying on them.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Vector Database Providers](#vector-database-providers)
- [API Reference](#api-reference)
- [Registering the Plugin with ChatGPT](#registering-the-plugin-with-chatgpt)
- [Data Ingestion Scripts](#data-ingestion-scripts)
- [Services](#services)
- [Running with Docker](#running-with-docker)
- [Deployment](#deployment)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The plugin acts as a bridge between ChatGPT and a vector store. The workflow is:

1. **Ingest:** Documents are split into chunks, optionally enriched with metadata, embedded with OpenAI's embedding models, and stored in a vector database.
2. **Retrieve:** When ChatGPT needs information, it calls the `/query` endpoint with natural-language queries and optional metadata filters.
3. **Answer:** The top-matching chunks are returned to ChatGPT, which uses them to ground its response.

The datastore layer is pluggable. You select a backend with an environment variable and the plugin handles the rest.

---

## Features

- **Pluggable vector stores:** Pinecone, Weaviate, Zilliz, Milvus, Qdrant, Redis, Chroma, Azure AI Search, LlamaIndex, Elasticsearch, AnalyticDB, PostgreSQL with pgvector, Supabase, MongoDB Atlas, and Azure Cosmos DB.
- **Semantic search** over embedded document chunks.
- **Metadata filtering** by source, source ID, document ID, and date range.
- **Upsert and delete** operations for both JSON documents and uploaded files.
- **File upload and parsing** for common document formats, with automatic chunking.
- **Optional PII detection** to identify or redact sensitive data before storage.
- **Bearer token authentication** on all endpoints.
- **Plugin manifest and OpenAPI spec** included, ready for ChatGPT plugin registration.
- **Docker and cloud deployment** configurations for Fly.io, Render, and Heroku.
- **Batch ingestion scripts** for JSON, JSONL, and ZIP archives.

---

## Architecture

```
                 ┌──────────────────────────┐
  ChatGPT  ───▶  │  FastAPI app (server/)   │
  (plugin)       │  - auth (Bearer token)   │
                 │  - /upsert /query ...    │
                 └────────────┬─────────────┘
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
      services/          datastore/        models/
      - chunking         factory.py        Document,
      - metadata         datastore.py      Query,
      - PII detection    providers/*       DeleteFilter...
      - OpenAI embeddings     │
                              ▼
                  Vector database (Pinecone, Qdrant, ...)
```

- **`server/`** contains the FastAPI application, route handlers, and Pydantic models.
- **`datastore/`** defines the abstract `DataStore` interface and its provider implementations. `factory.py` picks the active provider at startup from the `DATASTORE` environment variable.
- **`services/`** holds the helpers for chunking, file parsing, metadata extraction, PII detection, and OpenAI embedding calls.

---

## Project Structure

```
chatgpt-retrieval-plugin/
├── server/
│   ├── main.py                 # App entrypoint (FastAPI instance, startup)
│   ├── api.py                  # HTTP routes: /upsert, /upsert-file, /query, /delete
│   ├── models.py              # Pydantic models (Document, Query, Filter, ...)
│   └── __init__.py
├── datastore/
│   ├── datastore.py           # Abstract DataStore base class
│   ├── factory.py             # Selects the datastore from DATASTORE env var
│   └── providers/
│       ├── pinecone_datastore.py
│       ├── weaviate_datastore.py
│       ├── zilliz_datastore.py
│       ├── milvus_datastore.py
│       ├── qdrant_datastore.py
│       ├── redis_datastore.py
│       ├── chroma_datastore.py
│       ├── azuresearch_datastore.py
│       ├── llama_datastore.py
│       ├── elasticsearch_datastore.py
│       ├── analyticdb_datastore.py
│       ├── pgvector_datastore.py
│       ├── postgres_datastore.py
│       ├── supabase_datastore.py
│       ├── mongodb_atlas_datastore.py
│       └── azurecosmosdb_datastore.py
├── services/
│   ├── chunks.py              # Text chunking
│   ├── file.py                # File parsing (PDF, DOCX, TXT, ...)
│   ├── extract_metadata.py    # Metadata extraction
│   ├── pii_detection.py       # PII detection and redaction
│   ├── openai.py              # OpenAI embedding client
│   └── date.py                # Date parsing and normalization
├── scripts/
│   ├── process_json.py        # Ingest a JSON file of documents
│   ├── process_jsonl.py       # Ingest a JSON Lines file
│   ├── process_zip.py         # Ingest files from a ZIP archive
│   └── example.{json,jsonl,zip}
├── examples/
│   ├── providers/             # Example configs and notebooks per provider
│   ├── memory/                # In-memory example
│   └── ...
├── tests/
│   ├── test_integration.py
│   └── test_<provider>_datastore.py   # One test file per provider
├── docs/
│   ├── setup.md
│   ├── deployment/
│   │   ├── flyio.md
│   │   ├── render.md
│   │   ├── heroku.md
│   │   └── other-options.md
│   ├── removing-unused-dependencies.md
│   └── plugins.md
├── .well-known/
│   └── ai-plugin.json         # Plugin manifest for ChatGPT
├── openapi.yaml               # OpenAPI spec for the plugin API
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── poetry.lock
├── LICENSE
└── README.md
```

Each provider has a matching test file in `tests/`. Some providers also include a `docker-compose.yml` under `examples/providers/` for running their backing service locally.

---

## Prerequisites

- **Python 3.10+** (check `pyproject.toml` for the exact version constraint)
- **Poetry** for dependency management
- **An OpenAI API key** for generating embeddings
- **A vector database** of your choice, or Docker to run one locally
- **Docker** (optional, for containerized runs)

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/openai/chatgpt-retrieval-plugin.git
cd chatgpt-retrieval-plugin
```

### 2. Install dependencies

```bash
poetry install
```

Or with pip, if a `requirements.txt` is present:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```bash
DATASTORE=pinecone
BEARER_TOKEN=your-secret-token
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...
PINECONE_INDEX=...
```

See [Configuration](#configuration) for the full list.

### 4. Run the server

```bash
poetry run start
```

Or directly with uvicorn:

```bash
poetry run uvicorn server.main:app --host 0.0.0.0 --port 8000
```

### 5. Verify it's running

Open `http://localhost:8000/docs` for the interactive Swagger UI, or check the health of the API with a query request (see [API Reference](#api-reference)).

---

## Configuration

Configuration is read from environment variables.

### Core settings

| Variable | Required | Description |
|---|---|---|
| `DATASTORE` | Yes | The vector store backend to use (see [Providers](#vector-database-providers)). |
| `BEARER_TOKEN` | Yes | Static token that clients must send in the `Authorization: Bearer <token>` header. |
| `OPENAI_API_KEY` | Yes | API key used for generating embeddings. |
| `OPENAI_EMBEDDING_MODEL` | No | Embedding model name (default: `text-embedding-ada-002`). |
| `EMBEDDING_DIMENSION` | No | Vector dimension. Must match the embedding model. Default: `1536`. |
| `PORT` | No | Port the server listens on (default: `8000`). |

### Provider-specific settings

Each datastore requires its own variables. Examples:

| Provider | Variables |
|---|---|
| Pinecone | `PINECONE_API_KEY`, `PINECONE_ENVIRONMENT`, `PINECONE_INDEX` |
| Weaviate | `WEAVIATE_HOST`, `WEAVIATE_PORT`, `WEAVIATE_USERNAME`, `WEAVIATE_PASSWORD`, `WEAVIATE_INDEX` |
| Qdrant | `QDRANT_URL`, `QDRANT_API_KEY`, `QDRANT_COLLECTION` |
| Redis | `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `REDIS_INDEX_NAME` |
| Chroma | `CHROMA_COLLECTION`, `CHROMA_IN_MEMORY`, `CHROMA_PERSISTENCE_DIR`, `CHROMA_HOST`, `CHROMA_PORT` |
| Azure AI Search | `AZURESEARCH_SERVICE`, `AZURESEARCH_INDEX`, `AZURESEARCH_API_KEY` |
| PostgreSQL / pgvector | `PG_HOST`, `PG_PORT`, `PG_DB`, `PG_USER`, `PG_PASSWORD` |
| Supabase | `SUPABASE_URL`, `SUPABASE_ANON_KEY` |
| Elasticsearch | `ELASTICSEARCH_URL`, `ELASTICSEARCH_USERNAME`, `ELASTICSEARCH_PASSWORD`, `ELASTICSEARCH_INDEX` |
| Zilliz | `ZILLIZ_URI`, `ZILLIZ_USER`, `ZILLIZ_PASSWORD` |
| Milvus | `MILVUS_HOST`, `MILVUS_PORT`, `MILVUS_COLLECTION` |
| MongoDB Atlas | `MONGODB_URI`, `MONGODB_DATABASE`, `MONGODB_COLLECTION`, `MONGODB_INDEX` |
| Azure Cosmos DB | `AZCOSMOS_API_ENDPOINT`, `AZCOSMOS_API_KEY`, `AZCOSMOS_DATABASE_NAME`, `AZCOSMOS_CONTAINER_NAME` |
| LlamaIndex | See `datastore/providers/llama_datastore.py` |
| AnalyticDB | See `datastore/providers/analyticdb_datastore.py` |

Verify exact names in each provider module, since they are the source of truth.

### Example `.env` for local Chroma

```bash
DATASTORE=chroma
CHROMA_COLLECTION=documents
CHROMA_IN_MEMORY=false
CHROMA_PERSISTENCE_DIR=./chroma_data
BEARER_TOKEN=dev-token
OPENAI_API_KEY=sk-...
```

---

## Vector Database Providers

Set `DATASTORE` to one of the following values:

| `DATASTORE` value | Backend |
|---|---|
| `pinecone` | Pinecone |
| `weaviate` | Weaviate |
| `zilliz` | Zilliz Cloud (managed Milvus) |
| `milvus` | Milvus |
| `qdrant` | Qdrant |
| `redis` | Redis Stack (RediSearch) |
| `chroma` | Chroma |
| `azuresearch` | Azure AI Search |
| `llama` | LlamaIndex |
| `elasticsearch` | Elasticsearch |
| `analyticdb` | AnalyticDB for PostgreSQL |
| `pgvector` | PostgreSQL with the pgvector extension |
| `postgres` | PostgreSQL |
| `supabase` | Supabase |
| `mongodb_atlas` | MongoDB Atlas Vector Search |
| `azurecosmosdb` | Azure Cosmos DB |

Each provider is implemented in `datastore/providers/<name>_datastore.py` and has a corresponding test in `tests/`. Some providers need a vector index or collection created ahead of time. Check the provider's module or `examples/providers/` for setup steps.

For PostgreSQL-based backends, `examples/providers/pgvector/` includes SQL migrations such as `20230414142107_init_pg_vector.sql`.

---

## API Reference

The API is defined in `server/api.py` and documented in `openapi.yaml`. All endpoints require a bearer token:

```
Authorization: Bearer <BEARER_TOKEN>
```

### `POST /upsert`

Insert or update one or more documents. Each document is chunked, embedded, and stored.

**Request body**

```json
{
  "documents": [
    {
      "id": "doc-001",
      "text": "The quarterly report shows revenue grew 12% year over year.",
      "metadata": {
        "source": "email",
        "source_id": "msg-42",
        "url": "https://example.com/report",
        "created_at": "2024-03-01T10:00:00Z",
        "author": "Jane Doe"
      }
    }
  ]
}
```

**Response**

```json
{ "ids": ["doc-001"] }
```

### `POST /upsert-file`

Upload a file (PDF, DOCX, TXT, MD, and others). The file is parsed, chunked, embedded, and stored.

```bash
curl -X POST http://localhost:8000/upsert-file \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -F "file=@./annual-report.pdf"
```

**Response**

```json
{ "ids": ["annual-report-0", "annual-report-1", "..."] }
```

### `POST /query`

Run one or more semantic search queries, optionally with metadata filters.

**Request body**

```json
{
  "queries": [
    {
      "query": "What was revenue growth last year?",
      "filter": {
        "source": "email",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
      },
      "top_k": 3
    }
  ]
}
```

**Response**

```json
{
  "results": [
    {
      "query": "What was revenue growth last year?",
      "results": [
        {
          "id": "doc-001",
          "text": "The quarterly report shows revenue grew 12% year over year.",
          "metadata": { "source": "email", "source_id": "msg-42" },
          "score": 0.91
        }
      ]
    }
  ]
}
```

**Filter fields**

| Field | Type | Description |
|---|---|---|
| `source` | enum | One of `email`, `file`, `chat`. |
| `source_id` | string | ID in the originating system. |
| `document_id` | string | ID of the document. |
| `start_date` | string (date) | Include documents created on or after this date. |
| `end_date` | string (date) | Include documents created on or before this date. |

`top_k` defaults to 3 and is capped at 10.

### `DELETE /delete`

Delete documents by ID, by filter, or delete all.

```bash
# Delete by IDs
curl -X DELETE http://localhost:8000/delete \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids": ["doc-001"]}'

# Delete by filter
curl -X DELETE http://localhost:8000/delete \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"source": "email"}}'

# Delete all
curl -X DELETE http://localhost:8000/delete \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"delete_all": true}'
```

Only one of `ids`, `filter`, or `delete_all` should be used per request.

---

## Registering the Plugin with ChatGPT

1. **Deploy the server** to a publicly reachable HTTPS URL. See [Deployment](#deployment).
2. **Update the manifest** at `.well-known/ai-plugin.json`. Set `api.url` to your server's `openapi.yaml` location and set `logo_url` if you have a custom logo.
3. **Update the OpenAPI spec** `openapi.yaml`. Set the `servers` URL to your deployment's base URL.
4. **Install the plugin in ChatGPT** through the plugin store's developer mode, pointing it at your domain. ChatGPT fetches `/.well-known/ai-plugin.json` from that domain.
5. **Authenticate.** Choose "Service Level" authentication in the plugin settings and enter your `BEARER_TOKEN`.

The manifest is served from `/.well-known/ai-plugin.json`. Make sure your server or reverse proxy serves that path.

`docs/plugins.md` covers the plugin registration flow in more detail.

---

## Data Ingestion Scripts

Batch loaders live in `scripts/`. They read a source file, build documents, and send them to the `/upsert` endpoint or the datastore directly.

| Script | Input | Use case |
|---|---|---|
| `process_json.py` | A JSON array of documents | Small to medium batches |
| `process_jsonl.py` | JSON Lines, one document per line | Large streaming ingestion |
| `process_zip.py` | A ZIP archive of text or document files | Bulk file import |

Example input files are provided as `scripts/example.json`, `scripts/example.jsonl`, and `scripts/example.zip`.

```bash
poetry run python scripts/process_jsonl.py --filepath scripts/example.jsonl
```

Each script has its own `README.md` in `scripts/` with its exact command-line options. Check those before running, since argument names may vary.

---

## Services

The `services/` package contains helpers used by the API and scripts.

- **`chunks.py`** splits document text into overlapping chunks suited to embedding. Chunks are roughly 200 tokens, with overlap so context is preserved across boundaries.
- **`file.py`** extracts text from uploaded files. Supported formats include PDF, DOCX, TXT, and Markdown.
- **`extract_metadata.py`** derives or normalizes metadata (for example, from file names or headers).
- **`pii_detection.py`** detects personally identifiable information so it can be flagged, redacted, or excluded from indexing before storage. It is optional and typically configured through environment variables.
- **`openai.py`** wraps the OpenAI embeddings API, including batching.
- **`date.py`** parses and normalizes date strings used in metadata and filters.

---

## Running with Docker

### Build the image

```bash
docker build -t chatgpt-retrieval-plugin .
```

### Run the container

```bash
docker run -d -p 8000:8000 --env-file .env chatgpt-retrieval-plugin
```

### Run with Docker Compose

The root `docker-compose.yml` starts the plugin. Some providers have their own compose files under `examples/providers/<name>/docker-compose.yml` to run the backing database locally.

```bash
docker compose up --build
```

For example, to run Redis Stack or Qdrant locally, start the provider's compose file first and then point the plugin at it:

```bash
docker compose -f examples/providers/qdrant/docker-compose.yml up -d
```

---

## Deployment

Deployment guides are in `docs/`:

| Platform | Guide |
|---|---|
| Fly.io | `docs/deployment/flyio.md` |
| Render | `docs/deployment/render.md` (thumbnail: `render-thumbnail.png`) |
| Heroku | `docs/deployment/heroku.md` |
| Other | `docs/deployment/other-options.md` |

General steps for any platform:

1. Set all required environment variables as secrets in the platform's dashboard.
2. Build from the `Dockerfile` or use the platform's Python buildpack.
3. Expose port `8000` (or the value of `PORT`).
4. Confirm that the server is reachable over HTTPS, since ChatGPT requires it.
5. Set the public URL in `.well-known/ai-plugin.json` and `openapi.yaml`.

For production use, keep the `BEARER_TOKEN` secret and rotate it periodically.

---

## Development

### Install dev dependencies

```bash
poetry install --with dev
```

### Common tasks

Check the `Makefile` for the exact targets. Typical ones include:

```bash
make start     # Run the server locally
make format    # Format code (black / isort)
make lint      # Run linters
make test      # Run the test suite
```

### Code layout tips

- To add a new datastore, create `datastore/providers/<name>_datastore.py` that implements the `DataStore` abstract class from `datastore/datastore.py`. Register it in `datastore/factory.py`, add a test file under `tests/`, and document the environment variables.
- To change the API surface, update `server/api.py` and `server/models.py`, then regenerate or update `openapi.yaml` so ChatGPT stays in sync.

### Removing unused dependencies

`docs/removing-unused-dependencies.md` explains how to slim the install by removing providers you do not use. This shrinks the Docker image and speeds up builds.

---

## Testing

Tests use pytest and live in `tests/`.

```bash
poetry run pytest
```

Run the tests for one provider:

```bash
poetry run pytest tests/test_pinecone_datastore.py
```

Provider tests usually need live credentials or a running backing service. Set the relevant environment variables or start the provider's Docker Compose file first. Tests for unavailable providers can be skipped.

`tests/test_integration.py` runs end-to-end checks across the API: upsert, query, and delete against the configured datastore.

---

## Troubleshooting

**`401 Unauthorized`**
The `Authorization` header is missing or does not match `BEARER_TOKEN`. Send `Authorization: Bearer <token>`.

**Embedding dimension mismatch**
`EMBEDDING_DIMENSION` must match the embedding model's output size. For `text-embedding-ada-002` this is `1536`. Changing models usually requires recreating the index.

**Provider fails on startup**
Check that `DATASTORE` matches a supported value and that all of that provider's required variables are set. Read the startup logs for the missing variable name.

**Query returns no results**
Confirm documents were upserted successfully and that filters are not excluding them. Remove filters to test. Check that the date range covers the document's `created_at`.

**ChatGPT cannot load the plugin**
Verify that `https://<your-domain>/.well-known/ai-plugin.json` and `openapi.yaml` are publicly accessible, return valid JSON or YAML, and that the URLs inside them point to your deployment.

**File upload fails**
Check that the file type is supported and that the file is not password-protected or corrupted. Large files may need a higher request size limit at the proxy layer.

---

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.

---

## Acknowledgments

Built on FastAPI, Pydantic, and the OpenAI embeddings API. Thanks to the maintainers of each vector database integration.
