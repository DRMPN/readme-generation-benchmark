# ChatGPT Retrieval Plugin

This repository contains a FastAPI-based retrieval plugin for ChatGPT. It lets ChatGPT search and store documents, such as files, emails, and chat content, using natural-language queries and metadata filters. The server embeds text with OpenAI embedding models and delegates storage and search to a vector database provider that you select with an environment variable.

## Overview

The plugin exposes these endpoints from `server/main.py`:

- `POST /upsert-file`: uploads a file (PDF, DOCX, PPTX, TXT, MD, or CSV) and stores its extracted text with optional metadata.
- `POST /upsert`: stores an array of documents. Each document has `text` and optional `id` and `metadata`.
- `POST /query`: accepts an array of queries, each with a `query` string, an optional `filter`, and an optional `top_k` (default 3).
- `DELETE /delete`: deletes documents by `ids`, by `filter`, or with `delete_all`. At least one of these must be provided, or the server returns HTTP 400.

A second application is mounted at `/sub`. It exposes only the query endpoint (and, in the memory example, the upsert endpoint) so that its OpenAPI schema can be generated for a custom GPT.

Documents are split into chunks of about 200 tokens using `tiktoken` (`services/chunks.py`), and each chunk is embedded with OpenAI's embeddings API. Document metadata supports the fields `source` (`email`, `file`, or `chat`), `source_id`, `url`, `created_at`, and `author`.

The repository includes the plugin manifest and OpenAPI specification in `.well-known/` (`ai-plugin.json` and `openapi.yaml`), along with a logo. These files reference `https://your-app-url.com`, which you must update for your deployment.

### Supported Vector Database Providers

The `DATASTORE` environment variable selects a provider in `datastore/factory.py`. The supported values are:

| Value | Provider |
| --- | --- |
| `chroma` | Chroma |
| `llama` | LlamaIndex |
| `pinecone` | Pinecone |
| `weaviate` | Weaviate |
| `milvus` | Milvus |
| `zilliz` | Zilliz Cloud |
| `redis` | Redis |
| `azurecosmosdb` | Azure Cosmos DB for MongoDB vCore |
| `qdrant` | Qdrant |
| `azuresearch` | Azure Cognitive Search |
| `supabase` | Supabase (pgvector) |
| `postgres` | PostgreSQL (pgvector) |
| `analyticdb` | AnalyticDB |
| `elasticsearch` | Elasticsearch |
| `mongodb` | MongoDB Atlas |

Setup guides for these providers are in `docs/providers/`.

## Setup

### Requirements

- Python 3.10 or later (`pyproject.toml` specifies `python = "^3.10"`)
- [Poetry](https://python-poetry.org/) for dependency management
- An OpenAI API key
- Docker, optionally, for container builds and local services

### Install Dependencies

```bash
poetry install
```

Some providers require extra packages. For AnalyticDB, Postgres, or Supabase setups that need `psycopg2cffi`, install with the `postgresql` extra:

```bash
poetry install --extras "postgresql"
```

The `docs/providers/analyticdb/setup.md` guide describes how to install the PostgreSQL development headers if `pg_config` is not found.

### Configure the Environment

Copy the example environment file and fill in the values for your setup:

```bash
cp .env.example .env
```

At a minimum, set `DATASTORE`, `BEARER_TOKEN`, and `OPENAI_API_KEY`, then add the variables for your chosen provider. See the Configuration section below.

## Usage

### Run the Server

The `start` script in `pyproject.toml` runs the main server (`server.main:start`) on `0.0.0.0:8000` with auto-reload:

```bash
poetry run start
```

The `dev` script runs the localhost variant (`local_server.main:start`) on `localhost:3333`. It enables CORS for `http://localhost:3333` and `https://chat.openai.com`, disables authentication, and serves the manifest, OpenAPI schema, and logo from `local_server/`:

```bash
poetry run dev
```

The `local_server` module is intended for testing the plugin locally, as described in `docs/deprecated/plugins.md`.

### Run with Docker

The `Dockerfile` exports dependencies from `pyproject.toml` and `poetry.lock` into a `requirements.txt`, then starts Uvicorn on the port given by `PORT`, `WEBSITES_PORT`, or `8080`, in that order:

```bash
docker build -t retrieval-plugin .
docker run -p 8080:8080 --env-file .env retrieval-plugin
```

For Docker-based Qdrant and Elasticsearch setups, see `examples/docker/`. For example, `examples/docker/qdrant/README.md` shows how to start the plugin and Qdrant with `docker-compose up -d`, then store and query documents with `curl`.

### Store and Query Documents

Store documents with the `/upsert` endpoint. Each request must include a bearer token:

```bash
curl -X POST \
  -H "Content-type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  --data-binary '@documents.json' \
  "http://localhost:8000/upsert"
```

Query with `/query`:

```bash
curl -X POST \
  -H "Content-type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  --data-binary '@queries.json' \
  "http://localhost:8000/query"
```

### Bulk Import Scripts

The `scripts/` directory contains utilities that load file dumps into the datastore. Each one accepts `--filepath`, `--custom_metadata`, `--screen_for_pii`, and `--extract_metadata`:

- `scripts/process_json/process_json.py`: a JSON array of documents.
- `scripts/process_jsonl/process_jsonl.py`: newline-delimited JSON.
- `scripts/process_zip/process_zip.py`: a ZIP archive of DOCX, PDF, TXT, MD, and PPTX files.

For example:

```bash
cd scripts/process_json
python process_json.py --filepath path/to/file_dump.json --custom_metadata '{"source": "file"}' --screen_for_pii True --extract_metadata True
```

Both PII screening and metadata extraction call an OpenAI chat model through the functions in `services/pii_detection.py` and `services/extract_metadata.py`. You can change these functions for your use case.

### Connect to ChatGPT

The `.well-known/` files describe the plugin to ChatGPT. Before using them, replace `https://your-app-url.com` in `ai-plugin.json` and `openapi.yaml` with your deployed URL. The deployment guides in `docs/deployment/` describe this step for each platform.

For memory-enabled use, `examples/memory/` describes how to let a custom GPT call the `/upsert` endpoint as well as `/query`.

## Configuration

### Core Environment Variables

| Name | Required | Description |
| --- | --- | --- |
| `DATASTORE` | Yes | Vector database provider, one of the values listed in the Overview. |
| `BEARER_TOKEN` | Yes | Secret token that clients send in the `Authorization: Bearer` header. The server asserts that this variable is set at startup. |
| `OPENAI_API_KEY` | Yes | OpenAI API key used for embeddings and optional chat completions. |
| `EMBEDDING_MODEL` | Optional | Embedding model name. Defaults to `text-embedding-3-large` in `services/openai.py`. |
| `EMBEDDING_DIMENSION` | Optional | Embedding vector size. Defaults to `256`. |
| `OPENAI_EMBEDDING_BATCH_SIZE` | Optional | Number of chunks embedded per request. Defaults to `128`. |
| `OPENAI_EMBEDDINGMODEL_DEPLOYMENTID` | Optional | Deployment ID for Azure OpenAI embeddings. |
| `OPENAI_COMPLETIONMODEL_DEPLOYMENTID` | Optional | Deployment ID for Azure OpenAI chat completions, used by PII screening. |
| `PORT` / `WEBSITES_PORT` | Optional | Port used by the Docker container. Defaults to `8080`. |

Some documentation pages state different defaults or example models. The values above are the ones defined in the code.

### Provider Variables

Each provider has its own variables. Examples include:

- **Pinecone:** `PINECONE_API_KEY`, `PINECONE_ENVIRONMENT`, `PINECONE_INDEX`
- **Qdrant:** `QDRANT_URL` (default `http://localhost`), `QDRANT_PORT` (`6333`), `QDRANT_GRPC_PORT` (`6334`), `QDRANT_API_KEY`, `QDRANT_COLLECTION` (`document_chunks`)
- **Weaviate:** `WEAVIATE_URL` (`http://localhost:8080`), `WEAVIATE_CLASS` (`OpenAIDocument`), `WEAVIATE_API_KEY`
- **Redis:** `REDIS_HOST` (`localhost`), `REDIS_PORT` (`6379`), `REDIS_PASSWORD`, `REDIS_INDEX_NAME` (`index`), `REDIS_DOC_PREFIX` (`doc`), `REDIS_DISTANCE_METRIC` (`COSINE`), `REDIS_INDEX_TYPE` (`FLAT`)
- **Postgres:** `PG_HOST`, `PG_PORT`, `PG_USER`, `PG_PASSWORD`, `PG_DB`
- **Supabase:** `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
- **Elasticsearch:** `ELASTICSEARCH_INDEX` and either `ELASTICSEARCH_URL` or `ELASTICSEARCH_CLOUD_ID`, plus authentication variables
- **Milvus:** `MILVUS_HOST` (`localhost`), `MILVUS_PORT` (`19530`), `MILVUS_COLLECTION`, and optional index and search parameter variables
- **Zilliz:** `ZILLIZ_URI`, `ZILLIZ_USER`, `ZILLIZ_PASSWORD`, and optional `ZILLIZ_COLLECTION`
- **Azure Cognitive Search:** `AZURESEARCH_SERVICE`, `AZURESEARCH_INDEX`, and optional `AZURESEARCH_API_KEY`, `AZURESEARCH_DISABLE_HYBRID`, and `AZURESEARCH_SEMANTIC_CONFIG`
- **Azure Cosmos DB:** `AZCOSMOS_API`, `AZCOSMOS_CONNSTR`, `AZCOSMOS_DATABASE_NAME`, `AZCOSMOS_CONTAINER_NAME`
- **MongoDB Atlas:** `MONGODB_URI`, `MONGODB_DATABASE`, `MONGODB_COLLECTION`, `MONGODB_INDEX`
- **Chroma:** `CHROMA_COLLECTION`, `CHROMA_IN_MEMORY`, `CHROMA_PERSISTENCE_DIR`, `CHROMA_HOST`, `CHROMA_PORT`
- **LlamaIndex:** `LLAMA_INDEX_TYPE` (`simple_dict`), `LLAMA_INDEX_JSON_PATH`, `LLAMA_QUERY_KWARGS_JSON_PATH`, `LLAMA_RESPONSE_MODE`

The per-provider documents in `docs/providers/` contain the complete tables, including required flags and defaults.

### Deployment Configuration

The `Makefile` contains Heroku targets (`heroku-login` and `heroku-push`). You must replace `<your app name>` in the `HEROKU_APP` variable before using them.

Deployment guides are available for:

- Fly.io (`docs/deployment/flyio.md`)
- Heroku (`docs/deployment/heroku.md`)
- Render (`docs/deployment/render.md`)
- Other platforms, including Azure Container Apps, Google Cloud Run, and AWS ECS (`docs/deployment/other-options.md`)

Each guide recommends removing unused provider packages from `pyproject.toml` before deployment, as listed in `docs/deployment/removing-unused-dependencies.md`.

## Development

### Project Layout

- `server/main.py`: the production FastAPI application with bearer-token authentication.
- `local_server/main.py`: a localhost variant without authentication.
- `datastore/`: the abstract `DataStore` class (`datastore.py`), the factory (`factory.py`), and provider implementations in `providers/`.
- `services/`: chunking, embeddings, file text extraction, date parsing, PII detection, and metadata extraction.
- `models/`: Pydantic models for requests, responses, documents, and filters.
- `examples/`: memory, function-calling, authentication-method, Docker, provider, and notebook examples.
- `docs/`: deployment, provider, and deprecated plugin documentation.

### Adding or Changing a Provider

Providers subclass `DataStore` and implement `_upsert`, `_query`, and `delete`. The base class handles chunking and embedding. To register a provider, add a `case` to `datastore/factory.py`.

### Pull Requests

`.github/pull_request_template.md` defines the contribution checklist:

- Prefix PR titles with a type in square brackets, such as `[Bugfix]`, `[Feature]`, `[Enhancement]`, `[Refactor]`, or `[Documentation]`.
- Name branches `<type>/<short-description>-<issue-number>`, for example `feature/advanced-chunking-strategy-123`.
- Link related issues with `Fixes` or `Closes`.
- Include tests for new code and update documentation where relevant.
- Request review from at least one maintainer.

## Testing

Tests are in `tests/` and use pytest, pytest-cov, pytest-asyncio, and httpx. The `pyproject.toml` file sets `asyncio_mode = "auto"` and adds the repository root to `pythonpath`.

Run a provider test file with:

```bash
poetry run pytest ./tests/datastore/providers/<provider>/test_<provider>_datastore.py
```

Several provider tests are integration tests that need a running service:

- **Postgres:** start a pgvector-enabled PostgreSQL instance, apply `examples/providers/supabase/migrations/20230414142107_init_pg_vector.sql`, set `PG_HOST`, `PG_PORT`, and `PG_PASSWORD`, then run `poetry run pytest -s ./tests/datastore/providers/postgres/test_postgres_datastore.py`.
- **Supabase:** run `supabase start` from `examples/providers`, export `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`, then run the Supabase test file.
- **Redis:** start `redis/redis-stack-server:latest`, or use `examples/docker/redis/docker-compose.yml`.
- **Qdrant:** run `docker run -p "6333:6333" -p "6334:6334" qdrant/qdrant:v1.0.3`.
- **Elasticsearch:** run `docker-compose up` in `examples/docker/elasticsearch`.
- **Weaviate:** use `tests/datastore/providers/weaviate/docker-compose.yml`.
- **MongoDB Atlas:** requires a running cluster and the environment variables described in `docs/providers/mongodb/setup.md`. The directory also contains `test_integration.py`.
- **Milvus:** use the Milvus Docker Compose file in `examples/docker/milvus/`.
- **Zilliz:** requires a Zilliz database and updated environment variables.

Unit tests are also present for Analytic DB, Azure Cosmos DB, Azure Cognitive Search, Chroma, Elasticsearch, LlamaIndex, and Pinecone-related provider code paths, as listed in the `tests/datastore/providers/` directory.

## License

This project is licensed under the MIT License. Copyright (c) 2023 OpenAI. See the [LICENSE](LICENSE) file for the full text.
