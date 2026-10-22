# ChatGPT Retrieval Plugin

A FastAPI service that stores text documents in a vector database and answers natural-language queries against them. It is designed to back a ChatGPT plugin (or custom GPT action) that searches a user's own documents. Embeddings are generated with the OpenAI embeddings API, and 15 vector database backends are selectable through a single environment variable.

## Contents

- [How it works](#how-it-works)
- [Repository layout](#repository-layout)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Running with Docker](#running-with-docker)
- [Local development server](#local-development-server)
- [API](#api)
- [Authentication](#authentication)
- [Configuration](#configuration)
- [Supported vector databases](#supported-vector-databases)
- [Supported file types](#supported-file-types)
- [Batch import scripts](#batch-import-scripts)
- [Examples](#examples)
- [Deployment](#deployment)
- [Tests](#tests)
- [Known issues](#known-issues)
- [License](#license)

## How it works

1. **Upsert.** Documents are sent to `/upsert` (JSON) or `/upsert-file` (a single uploaded file). Text is split into chunks of about 200 tokens (`cl100k_base` tokenizer, see `services/chunks.py`). Chunks are split on sentence-ending punctuation and newlines where possible.
2. **Embed.** Each chunk is embedded with the OpenAI embeddings API (`services/openai.py`). The default model is `text-embedding-3-large` with a 256-dimension output. Requests are batched (default 128 chunks per request).
3. **Store.** The chunks and their embeddings are written to the configured vector database. Before inserting, existing vectors for the same document `id` are deleted, so re-upserting a document replaces it.
4. **Query.** Each query string is embedded and passed to the datastore, which returns the most similar chunks with scores. Queries can include metadata filters (`document_id`, `source`, `source_id`, `author`, `start_date`, `end_date`). The default `top_k` is 3.

Documents carry optional metadata: `source` (`email`, `file`, or `chat`), `source_id`, `url`, `created_at`, and `author`.

## Repository layout

| Path | Contents |
| ---- | -------- |
| `server/main.py` | Main FastAPI app. Exposes `/upsert`, `/upsert-file`, `/query`, `/delete`, and a `/sub` sub-app for the query-only schema. Started by `poetry run start`. |
| `local_server/main.py` | Unauthenticated localhost variant with CORS for `chat.openai.com`, serving the manifest and OpenAPI files. Started by `poetry run dev`. |
| `datastore/` | `datastore.py` defines the abstract `DataStore` base class. `factory.py` selects a backend from `DATASTORE`. `providers/` holds one implementation per backend. |
| `models/` | Pydantic models for documents, chunks, queries, and API request/response bodies. |
| `services/` | Chunking (`chunks.py`), OpenAI calls (`openai.py`), file text extraction (`file.py`), and optional PII screening and metadata extraction (`pii_detection.py`, `extract_metadata.py`). |
| `scripts/` | Batch importers for JSON, JSONL, and ZIP dumps. |
| `.well-known/` | Plugin manifest (`ai-plugin.json`), OpenAPI schema (`openapi.yaml`), and logo served by the main server. |
| `local_server/` | Manifest, OpenAPI schema, and logo for localhost testing. |
| `docs/` | Setup guides for each vector database, deployment guides, and a deprecated plugin guide. |
| `examples/` | Authentication variants, a memory example, Docker Compose files, and Jupyter notebooks. |
| `tests/` | Pytest suite for the datastore providers. |
| `Dockerfile`, `Makefile` | Container build and a Heroku push helper. |
| `pyproject.toml`, `poetry.lock` | Poetry project definition and pinned dependencies. |

## Requirements

- Python 3.10 or later (`pyproject.toml` specifies `^3.10`).
- [Poetry](https://python-poetry.org/) for local installs.
- An OpenAI API key, or Azure OpenAI deployment settings (see [Configuration](#configuration)).
- A running instance of the vector database you choose.
- Docker, optionally, for containerized runs.

## Quick start

These steps run the main server on `http://0.0.0.0:8000` with the Chroma backend, which runs in memory by default.

```bash
# Install dependencies
poetry install

# Required settings. The server does not load .env files itself,
# so export the variables in your shell.
export DATASTORE="chroma"
export BEARER_TOKEN="<a-long-random-secret>"
export OPENAI_API_KEY="<your-openai-api-key>"

# Start the server (reload is enabled)
poetry run start
```

The interactive API docs are served by FastAPI at `http://localhost:8000/docs`. The query-only OpenAPI schema is at `http://localhost:8000/sub/openapi.json`.

Example requests:

```bash
# Upsert a document
curl -X POST http://localhost:8000/upsert \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"documents": [{"text": "The quarterly report is due on Friday.", "metadata": {"source": "file", "author": "Alice"}}]}'

# Query
curl -X POST http://localhost:8000/query \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"queries": [{"query": "When is the report due?", "top_k": 3}]}'
```

## Running with Docker

The `Dockerfile` exports dependencies from `poetry.lock` into a `requirements.txt`, then runs Uvicorn.

```bash
docker build -t chatgpt-retrieval-plugin .

docker run -p 8080:8080 \
  -e DATASTORE=chroma \
  -e BEARER_TOKEN="<a-long-random-secret>" \
  -e OPENAI_API_KEY="<your-openai-api-key>" \
  chatgpt-retrieval-plugin
```

The container listens on `$PORT` if set, then `$WEBSITES_PORT`, and defaults to `8080`. The image does not include a vector database. Use the provider-specific settings and, where available, the Compose files in `examples/docker/` (Elasticsearch, Milvus, Qdrant, Redis) or `tests/datastore/providers/weaviate/docker-compose.yml`.

## Local development server

`local_server/main.py` is a copy of the main app intended for testing with ChatGPT on localhost. It has no authentication, and it serves the manifest, OpenAPI file, and logo from `local_server/`.

```bash
export DATASTORE="chroma"
export OPENAI_API_KEY="<your-openai-api-key>"
poetry run dev
```

This starts the server on `localhost:3333`. Its `/upsert`, `/upsert-file`, `/query`, and `/delete` endpoints are not protected by a bearer token. Do not deploy it. See [docs/deprecated/plugins.md](docs/deprecated/plugins.md) for the localhost plugin steps. That guide describes ChatGPT plugins, which OpenAI has deprecated.

## API

All endpoints in the main server require a bearer token (see [Authentication](#authentication)). Request and response bodies use the models in `models/api.py` and `models/models.py`.

| Method | Path | Description |
| ------ | ---- | ----------- |
| `POST` | `/upsert` | Body: `{"documents": [Document, ...]}`. Chunks, embeds, and stores each document. Returns `{"ids": [...]}`. |
| `POST` | `/upsert-file` | Multipart form with a `file` field and an optional `metadata` field containing a JSON-encoded document metadata object. Extracts text from the file, then upserts it. Returns `{"ids": [...]}`. |
| `POST` | `/query` | Body: `{"queries": [{"query": "...", "filter": {...}, "top_k": 3}]}`. Returns `{"results": [{"query": "...", "results": [chunk with score, ...]}]}`. |
| `DELETE` | `/delete` | Body: `{"ids": [...]}`, `{"filter": {...}}`, or `{"delete_all": true}`. Returns `{"success": true|false}`. Returns HTTP 400 if none of these is given. |

The `/sub` mount exposes only `POST /sub/query`, with a description written for GPT actions. Its OpenAPI schema is at `/sub/openapi.json`.

Each `Document` has `text` (required), and optional `id` and `metadata`. If `id` is omitted, a UUID is generated. Chunk IDs have the form `<document_id>_<index>`.

## Authentication

The main server uses HTTP Bearer authentication. Every request must include `Authorization: Bearer <BEARER_TOKEN>`, where the token matches the `BEARER_TOKEN` environment variable. Otherwise the server returns HTTP 401. The server will not start unless `BEARER_TOKEN` is set.

The `examples/authentication-methods/` directory contains manifest variants for no-auth, service-level HTTP, user-level HTTP, and OAuth.

## Configuration

### General

| Variable | Required | Default | Description |
| -------- | -------- | ------- | ----------- |
| `DATASTORE` | Yes | none | Backend to use. One of the names in [Supported vector databases](#supported-vector-databases). The server fails to start if it is unset. |
| `BEARER_TOKEN` | Yes (main server) | none | Secret for the bearer token. The server fails to start if it is unset. |
| `OPENAI_API_KEY` | Yes | none | OpenAI API key, read by the `openai` Python client. |
| `EMBEDDING_MODEL` | No | `text-embedding-3-large` | Embedding model name. |
| `EMBEDDING_DIMENSION` | No | `256` | Embedding dimension. Passed to the embeddings API as `dimensions`, and used by backends to size their indexes. Must match the index you create. |
| `OPENAI_EMBEDDING_BATCH_SIZE` | No | `128` | Number of chunks per embeddings request. The Azure example sets this to `1`. |

### Azure OpenAI (optional)

| Variable | Description |
| -------- | ----------- |
| `OPENAI_API_BASE` | Azure OpenAI endpoint, e.g. `https://<name>.openai.azure.com/`. |
| `OPENAI_API_TYPE` | Set to `azure`. |
| `OPENAI_EMBEDDINGMODEL_DEPLOYMENTID` | Azure deployment name for the embedding model. When set, embeddings use `deployment_id` instead of `model`. |
| `OPENAI_COMPLETIONMODEL_DEPLOYMENTID` | Azure deployment used by the PII screening function. |
| `OPENAI_METADATA_EXTRACTIONMODEL_DEPLOYMENTID` | Listed in `.env.example`. The metadata extraction code currently does not read it. |

The `.env.example` file lists the variables for every backend. Copy it to `.env` for reference, then export the values you need.

### Backend-specific variables

These are the variables read by each provider in `datastore/providers/`. Defaults are shown where the code provides one. See the matching guide in `docs/providers/` for setup details.

**Chroma** (`DATASTORE=chroma`)
`CHROMA_IN_MEMORY` (default `True`), `CHROMA_PERSISTENCE_DIR` (default `openai`), `CHROMA_HOST` (default `http://127.0.0.1`), `CHROMA_PORT` (default `8000`), `CHROMA_COLLECTION` (default `openaiembeddings`).

**Pinecone** (`DATASTORE=pinecone`)
`PINECONE_API_KEY`, `PINECONE_ENVIRONMENT`, `PINECONE_INDEX`.

**Weaviate** (`DATASTORE=weaviate`)
`WEAVIATE_URL`, `WEAVIATE_API_KEY` (required for Weaviate Cloud Services, per the provider guide), `WEAVIATE_CLASS` (default `OpenAIDocument`), `WEAVIATE_BATCH_SIZE` (default `20`), `WEAVIATE_BATCH_DYNAMIC`, `WEAVIATE_TIMEOUT_RETRIES` (default `3`), `WEAVIATE_BATCH_NUM_WORKERS` (default `1`).

**Milvus** (`DATASTORE=milvus`)
`MILVUS_HOST` (default `localhost`), `MILVUS_PORT` (default `19530`), `MILVUS_USER`, `MILVUS_PASSWORD`, `MILVUS_COLLECTION` (default: a random name beginning with `c`), `MILVUS_INDEX_PARAMS`, `MILVUS_SEARCH_PARAMS`, `MILVUS_CONSISTENCY_LEVEL`.

**Zilliz** (`DATASTORE=zilliz`)
`ZILLIZ_URI`, `ZILLIZ_USER`, `ZILLIZ_PASSWORD`, `ZILLIZ_COLLECTION` (default: a random name beginning with `c`), `ZILLIZ_CONSISTENCY_LEVEL`.

**Redis** (`DATASTORE=redis`)
`REDIS_HOST` (default `localhost`), `REDIS_PORT` (default `6379`), `REDIS_PASSWORD`, `REDIS_INDEX_NAME` (default `index`), `REDIS_DOC_PREFIX` (default `doc`), `REDIS_DISTANCE_METRIC` (default `COSINE`), `REDIS_INDEX_TYPE` (default `FLAT`).

**Qdrant** (`DATASTORE=qdrant`)
`QDRANT_URL` (default `http://localhost`), `QDRANT_PORT` (default `6333`), `QDRANT_GRPC_PORT` (default `6334`), `QDRANT_API_KEY`, `QDRANT_COLLECTION` (default `document_chunks`).

**Azure Cognitive Search** (`DATASTORE=azuresearch`)
`AZURESEARCH_SERVICE`, `AZURESEARCH_INDEX`, `AZURESEARCH_API_KEY` (optional according to `.env.example`, which says key-free managed identity is used if it is not set), `AZURESEARCH_SEMANTIC_CONFIG`, `AZURESEARCH_LANGUAGE` (default `en-us`), `AZURESEARCH_DISABLE_HYBRID`, `AZURESEARCH_DIMENSIONS`. Existing indexes with different field names can be mapped with `AZURESEARCH_FIELDS_ID`, `_TEXT`, `_EMBEDDING`, `_DOCUMENT_ID`, `_SOURCE`, `_SOURCE_ID`, `_URL`, `_CREATED_AT`, and `_AUTHOR`.

**Supabase** (`DATASTORE=supabase`)
`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`.

**Postgres** (`DATASTORE=postgres`, uses pgvector)
`PG_HOST` (default `localhost`), `PG_PORT` (default `5432`), `PG_DB` (default `postgres`), `PG_USER` (default `postgres`), `PG_PASSWORD` (default `postgres`).

**AnalyticDB** (`DATASTORE=analyticdb`)
`PG_HOST` (default `localhost`), `PG_PORT` (default `5432`), `PG_DATABASE` (default `postgres`), `PG_USER` (default `user`), `PG_PASSWORD` (default `password`), `PG_COLLECTION` (default `document_chunks`). Note that the `PG_*` names are shared with Postgres, but the defaults differ.

**Elasticsearch** (`DATASTORE=elasticsearch`)
`ELASTICSEARCH_URL` (default `http://localhost:9200`), `ELASTICSEARCH_CLOUD_ID`, `ELASTICSEARCH_USERNAME`, `ELASTICSEARCH_PASSWORD`, `ELASTICSEARCH_API_KEY`, `ELASTICSEARCH_INDEX`, `ELASTICSEARCH_REPLICAS` (default `1`), `ELASTICSEARCH_SHARDS` (default `1`).

**MongoDB Atlas** (`DATASTORE=mongodb`)
`MONGODB_URI`, `MONGODB_DATABASE` (default `default`), `MONGODB_COLLECTION` (default `default`), `MONGODB_INDEX` (default `default`).

**Azure CosmosDB for MongoDB vCore** (`DATASTORE=azurecosmosdb`)
`AZCOSMOS_API` (default `mongo-vcore`), `AZCOSMOS_CONNSTR`, `AZCOSMOS_DATABASE_NAME`, `AZCOSMOS_CONTAINER_NAME`.

**LlamaIndex** (`DATASTORE=llama`)
`LLAMA_INDEX_JSON_PATH` (optional path to a saved index), `LLAMA_QUERY_KWARGS_JSON_PATH` (optional), `LLAMA_RESPONSE_MODE` (defaults to the `NO_TEXT` mode in the code). See `docs/providers/llama/setup.md`.

## Supported vector databases

Set `DATASTORE` to the value in the second column.

| Backend | `DATASTORE` value | Setup guide |
| ------- | ----------------- | ----------- |
| Chroma | `chroma` | [docs/providers/chroma/setup.md](docs/providers/chroma/setup.md) |
| LlamaIndex | `llama` | [docs/providers/llama/setup.md](docs/providers/llama/setup.md) |
| Pinecone | `pinecone` | [docs/providers/pinecone/setup.md](docs/providers/pinecone/setup.md) |
| Weaviate | `weaviate` | [docs/providers/weaviate/setup.md](docs/providers/weaviate/setup.md) |
| Milvus | `milvus` | [docs/providers/milvus/setup.md](docs/providers/milvus/setup.md) |
| Zilliz | `zilliz` | [docs/providers/zilliz/setup.md](docs/providers/zilliz/setup.md) |
| Redis | `redis` | [docs/providers/redis/setup.md](docs/providers/redis/setup.md) |
| Qdrant | `qdrant` | [docs/providers/qdrant/setup.md](docs/providers/qdrant/setup.md) |
| Azure Cognitive Search | `azuresearch` | [docs/providers/azuresearch/setup.md](docs/providers/azuresearch/setup.md) |
| Azure CosmosDB (Mongo vCore) | `azurecosmosdb` | [docs/providers/azurecosmosdb/setup.md](docs/providers/azurecosmosdb/setup.md) |
| Supabase | `supabase` | [docs/providers/supabase/setup.md](docs/providers/supabase/setup.md) |
| Postgres (pgvector) | `postgres` | [docs/providers/postgres/setup.md](docs/providers/postgres/setup.md) |
| AnalyticDB | `analyticdb` | [docs/providers/analyticdb/setup.md](docs/providers/analyticdb/setup.md) |
| Elasticsearch | `elasticsearch` | [docs/providers/elasticsearch/setup.md](docs/providers/elasticsearch/setup.md) |
| MongoDB Atlas | `mongodb` | [docs/providers/mongodb/setup.md](docs/providers/mongodb/setup.md) |

Some backends have dependencies that are only needed for that backend. [docs/deployment/removing-unused-dependencies.md](docs/deployment/removing-unused-dependencies.md) lists which packages in `pyproject.toml` can be removed for each provider. Removing them is optional.

## Supported file types

`/upsert-file` and the batch scripts extract text from:

| Type | MIME type |
| ---- | --------- |
| PDF | `application/pdf` (via PyPDF2) |
| Plain text | `text/plain` |
| Markdown | `text/markdown` |
| Word (.docx) | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (via docx2txt) |
| CSV | `text/csv` |
| PowerPoint (.pptx) | `application/vnd.openxmlformats-officedocument.presentationml.presentation` (via python-pptx) |

Other types are rejected with an error. The file type is taken from the upload's `Content-Type` header.

## Batch import scripts

The scripts in `scripts/` load a file dump into the configured datastore. Each script accepts `--filepath`, `--custom_metadata` (a JSON object merged into each document's metadata), `--screen_for_pii` (default `False`), and `--extract_metadata` (default `False`).

- `scripts/process_json/process_json.py`: a JSON array of documents. See [README](scripts/process_json/README.md).
- `scripts/process_jsonl/process_jsonl.py`: one JSON document per line. See [README](scripts/process_jsonl/README.md).
- `scripts/process_zip/process_zip.py`: a ZIP of DOCX, PDF, TXT, MD, and PPTX files. See [README](scripts/process_zip/README.md).

The scripts use the environment variables described above, so set `DATASTORE` and the backend variables before running them.

`--screen_for_pii` and `--extract_metadata` call the language model through `services/pii_detection.py` and `services/extract_metadata.py`. The metadata extraction prompt asks for a `gpt-4` model by default. Both functions are examples and should be adapted to your use case. The main server does not call them.

## Examples

- `examples/memory/`: lets a custom GPT save conversation snippets through `/upsert`. See its [README](examples/memory/README.md).
- `examples/authentication-methods/`: manifest files for no-auth, service-level HTTP, user-level HTTP, and OAuth.
- `examples/docker/`: Docker Compose files for Elasticsearch, Milvus, Qdrant, and Redis, with a Qdrant walkthrough in [its README](examples/docker/qdrant/README.md).
- `examples/providers/`: Jupyter notebooks for Azure CosmosDB, Elasticsearch, MongoDB, Pinecone, and Redis, plus a Supabase pgvector migration.
- `examples/function-calling/`: see its [README](examples/function-calling/README.md).

## Deployment

Guides are in `docs/deployment/`:

- [Heroku](docs/deployment/heroku.md). Uses the `Makefile` targets `heroku-login` and `heroku-push`.
- [Fly.io](docs/deployment/flyio.md).
- [Render](docs/deployment/render.md).
- [Other options](docs/deployment/other-options.md), including Azure Container Apps, Google Cloud Run, and AWS ECS.

After deploying, update the `url` fields in `.well-known/ai-plugin.json` and `.well-known/openapi.yaml` to your public app URL. The manifest and schema are served from `/.well-known/` on the main server.

## Tests

The tests are in `tests/datastore/providers/` and use pytest, pytest-asyncio, and pytest-cov (dev dependencies in `pyproject.toml`). Most provider tests need the matching vector database and credentials running, so they are not self-contained. Run them with:

```bash
poetry run pytest
```

Some test files read a `.env` file or need `BEARER_TOKEN` and `OPENAI_API_KEY` set in the environment.

## Known issues

These were observed while reading the code. They have not been fixed.

- `/upsert-file` writes every upload to the fixed path `/tmp/temp_file`. Concurrent uploads can overwrite each other.
- When `/upsert-file` fails, the error detail is the literal string `str({e})` rather than the exception text. The format string is missing its `f` prefix (`server/main.py`, `local_server/main.py`).
- The main server returns a generic `Internal Service Error` for most failures in `/upsert`, `/query`, and `/delete`. The underlying error is only written to the log.

## License

See [LICENSE](LICENSE).
