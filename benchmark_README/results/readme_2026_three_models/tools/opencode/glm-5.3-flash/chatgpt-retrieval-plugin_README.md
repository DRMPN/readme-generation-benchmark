# ChatGPT Retrieval Plugin

The ChatGPT Retrieval Plugin is a Python (3.10) project built with FastAPI that provides a retrieval API for storing and querying documents using natural language queries and metadata filters. It is designed as a [ChatGPT plugin](https://openai.com/blog/chatgpt-plugins) and includes a plugin manifest, OpenAPI schema, and logo under `.well-known/`, so it can be tested as a localhost plugin in ChatGPT via `local_server/main.py`. Note that ChatGPT plugins are deprecated (see `docs/deprecated/plugins.md`), but the project can still be used as a standalone retrieval service.

## Features

- **FastAPI server** exposing four authenticated endpoints: `POST /upsert-file`, `POST /upsert`, `POST /query`, and `DELETE /delete` (`server/main.py`).
- **Pluggable vector database support** through a common `DataStore` interface, selected with the `DATASTORE` environment variable (`datastore/factory.py`).
- **Automatic document processing**: documents are split into chunks of roughly 200 tokens using the `cl100k_base` tokenizer, then embedded with the OpenAI embeddings API (`services/chunks.py`, `services/openai.py`). Upserting a document with the same ID first deletes its existing chunks.
- **File ingestion**: `/upsert-file` extracts text from PDF, DOCX, PPTX, TXT, Markdown, and CSV files (`services/file.py`).
- **Metadata filtering**: queries can filter on `document_id`, `source` (`email`, `file`, or `chat`), `source_id`, `author`, and date ranges, with a `top_k` parameter (default 3) (`models/models.py`).
- **Batch import scripts** (`scripts/process_json`, `scripts/process_zip`) that optionally screen documents for personally identifiable information (PII) and extract metadata using a language model.
- **Deployment configs** for Docker, Heroku, Render, and Fly.io.

## Supported Data Stores

The `DATASTORE` environment variable selects one of the following providers (setup guides are in `docs/providers/<provider>/setup.md`):

| Provider | `DATASTORE` value |
| --- | --- |
| Chroma | `chroma` |
| Llama Index | `llama` |
| Pinecone | `pinecone` |
| Weaviate | `weaviate` |
| Milvus | `milvus` |
| Zilliz | `zilliz` |
| Redis | `redis` |
| Azure Cosmos DB | `azurecosmosdb` |
| Qdrant | `qdrant` |
| Azure Cognitive Search | `azuresearch` |
| Supabase | `supabase` |
| Postgres | `postgres` |
| AnalyticDB | `analyticdb` |
| Elasticsearch | `elasticsearch` |
| MongoDB Atlas | `mongodb` |

## API Endpoints

All requests require Bearer token authentication (the `BEARER_TOKEN` environment variable).

| Method | Path | Description |
| --- | --- | --- |
| POST | `/upsert-file` | Upload a file (PDF, DOCX, PPTX, TXT, MD, or CSV), extract its text, chunk, embed, and store it. Optional metadata can be supplied. |
| POST | `/upsert` | Store a batch of documents provided as JSON (`UpsertRequest`). |
| POST | `/query` | Run one or more queries with optional metadata filters and `top_k`, returning scored document chunks. |
| DELETE | `/delete` | Delete documents by `ids`, metadata `filter`, or everything with `delete_all`. One of the three is required. |

A sub-application mounted at `/sub` exposes only the `/query` endpoint in its OpenAPI schema (available at `/sub/openapi.json`), which is used as the plugin API schema. The full OpenAPI schema for the plugin is served at `/.well-known/openapi.yaml`, and the plugin manifest at `/.well-known/ai-plugin.json`.

## Getting Started

### Prerequisites

- Python 3.10
- [Poetry](https://python-poetry.org/)
- An OpenAI API key
- A vector database of your choice (see the table above for configuration variables)

### Installation

```bash
git clone https://github.com/openai/chatgpt-retrieval-plugin.git
cd chatgpt-retrieval-plugin
poetry install
```

To run tests, the development dependencies (pytest, httpx, pytest-asyncio, pytest-cov) are included via Poetry's dev group. Provider tests live under `tests/datastore/providers/`.

### Configuration

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Core variables:

- `DATASTORE` — which vector database to use (see table above).
- `BEARER_TOKEN` — the Bearer token required by the API.
- `OPENAI_API_KEY` — your OpenAI API key.
- `EMBEDDING_MODEL` — embedding model to use (default in the example is `text-embedding-3-large`).
- `EMBEDDING_DIMENSION` — the dimension of the embeddings (default in the example is 256).

Provider-specific configuration variables are listed in `.env.example` and in each provider's setup guide under `docs/providers/`.

### Running the Server

Production server (port 8000):

```bash
poetry run start
```

Local development server for testing the plugin in ChatGPT (port 3333, CORS-enabled, serves the local manifest, OpenAPI schema, and logo, and requires no authentication):

```bash
poetry run dev
```

### Docker

The included `Dockerfile` builds a Python 3.10 image that exports the Poetry dependencies and runs the server with uvicorn. It honors `PORT`, `WEBSITES_PORT`, or defaults to 8080:

```bash
docker build -t retrieval-plugin .
docker run -p 8080:8080 --env-file .env retrieval-plugin
```

The `Makefile` contains targets for pushing the container to Heroku (`make heroku-login` and `make heroku-push`).

## Batch Import Scripts

- `scripts/process_json/process_json.py` processes a JSON file dump of documents (fields: `text` required; optional `id`, `source`, `source_id`, `url`, `created_at`, `author`) and upserts them into the database. Supports `--custom_metadata`, `--screen_for_pii`, and `--extract_metadata` flags.
- `scripts/process_zip/process_zip.py` processes a ZIP file containing docx, pdf, txt, md, and pptx files, with the same options.

## Examples

The `examples/` directory contains:

- A **memory example** (`examples/memory/`) that demonstrates a personal-memory plugin backed by this retrieval service.
- A **function-calling example** (`examples/function-calling/`).
- **Authentication method examples** (`examples/authentication-methods/`) for no-auth, user HTTP, service HTTP, and OAuth plugin manifests.
- **Docker Compose setups** (`examples/docker/`) for running the server with Qdrant, Redis, Elasticsearch, or Milvus locally.
- **Notebooks** (`examples/providers/`) for several providers, including semantic-search examples for Pinecone, Redis, Elasticsearch, Azure Cosmos DB, and MongoDB.

## Repository Structure

- `server/` — the production FastAPI application.
- `local_server/` — the localhost testing version of the server.
- `.well-known/` — plugin manifest, OpenAPI schema, and logo.
- `datastore/` — the `DataStore` interface and provider implementations.
- `models/` — Pydantic models for documents, chunks, queries, and API requests/responses.
- `services/` — file parsing, chunking, embedding, PII detection, and metadata extraction.
- `scripts/` — batch import utilities.
- `docs/` — provider setup guides, deployment guides (Heroku, Render, Fly.io), and deprecated plugin documentation.
- `examples/` — example plugins, notebooks, and Docker Compose files.
- `tests/` — datastore provider tests.

## License

This project is licensed under the MIT License (see [LICENSE](LICENSE)).
