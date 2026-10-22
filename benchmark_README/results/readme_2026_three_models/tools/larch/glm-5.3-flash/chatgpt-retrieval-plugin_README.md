# ChatGPT Retrieval Plugin

The ChatGPT Retrieval Plugin repository provides a flexible solution for adding semantic search capabilities to ChatGPT via plugins. It allows ChatGPT to search a vector database of your documents and return relevant chunks of text back into the conversation, enabling the model to answer questions grounded in your own data.

The plugin uses the **post-2023-03-23 plugin protocol** and requires an **API key** to be passed as a Bearer token in the `Authorization` header for authentication.

## Table of Contents

- [Introduction](#introduction)
- [Choosing a Datastore](#choosing-a-datastore)
- [General Setup](#general-setup)
  - [API Endpoints](#api-endpoints)
  - [Environment Variables](#environment-variables)
  - [Deployment](#deployment)
  - [Running the API Locally](#running-the-api-locally)
- [Datastore Setup](#datastore-setup)
  - [Chroma](#chroma)
  - [LlamaIndex](#llamaindex)
  - [Elasticsearch](#elasticsearch)
  - [MongoDB Atlas](#mongodb-atlas)
  - [Pinecone](#pinecone)
  - [Postgres](#postgres)
  - [Redis](#redis)
  - [Weaviate](#weaviate)
  - [Qdrant](#qdrant)
  - [Milvus](#milvus)
  - [Zilliz](#zilliz)
  - [Azure Search](#azure-search)
  - [Azure Cosmos DB](#azure-cosmos-db)
  - [AnalyticDB](#analyticdb)
  - [Supabase / pgvector](#supabase--pgvector)
- [Metadata Extraction and Filtering](#metadata-extraction-and-filtering)
- [PII Detection and Redaction](#pii-detection-and-redaction)
- [Uploading Documents](#uploading-documents)
  - [JSON / JSONL](#json--jsonl)
  - [ZIP files](#zip-files)
- [Development](#development)
- [Community Contributions](#community-contributions)

## Introduction

The Retrieval Plugin lets you:

1. **Store documents** — Upload documents in a variety of formats (JSON, JSONL, ZIP) to a vector database datastore of your choice.
2. **Query documents** — Allow ChatGPT to perform semantic search over those documents using natural-language queries, and inject the most relevant text chunks back into the model's context.

The plugin consists of several parts:

- **API server** (`api.py`, `models.py`) — A FastAPI application exposing `/upsert`, `/upsert-files`, `/query`, `/delete`, and other endpoints.
- **Datastore layer** (`datastore/`) — A common `Datastore` interface with adapters for many vector databases.
- **Utilities** (`scripts/`) — Helpers for chunking text, extracting metadata, detecting PII, generating embeddings, and preparing documents for upload.
- **Container definition** (`ai-plugin.json`, `openapi.yaml`) — The plugin manifest and OpenAPI specification used to register the plugin with ChatGPT.

## Choosing a Datastore

The plugin supports a variety of vector database providers. Choose one based on your needs:

| Datastore | Best for | Notes |
|---|---|---|
| **Chroma** | Local development, easy setup | Runs in-process or via Docker Compose; no API key needed |
| **Pinecone** | Managed, large-scale production | Fully managed cloud service |
| **Weaviate** | Full-text + vector search | Open-source, cloud or self-hosted |
| **Qdrant** | Self-hosted or managed cloud | Written in Rust, fast and memory-efficient |
| **Milvus / Zilliz** | Large-scale production | Zilliz is the managed version of Milvus |
| **LlamaIndex (Llama Cloud)** | Managed simplicity | Minimal configuration |
| **Redis** | Low-latency, in-memory | Vector search via RediSearch |
| **Postgres / pgvector / Supabase** | Relational + vector search | Store embeddings alongside relational data |
| **Elasticsearch** | Enterprise search | Combined keyword and vector search |
| **MongoDB Atlas** | Document database with vectors | Managed service |
| **Azure Search / Azure Cosmos DB** | Azure ecosystem | Integration with Microsoft cloud |
| **AnalyticDB** | Alibaba Cloud | Analytical workloads |

For local development, **Chroma** is the simplest choice — it can run entirely locally with no additional services (via a Docker Compose stack) and requires no credentials.

## General Setup

### Prerequisites

- Python 3.10 or later
- [Poetry](https://python-poetry.org/) for dependency management
- An OpenAI API key (for generating embeddings with `text-embedding-ada-002`)

### Installation

Install dependencies with Poetry:

```bash
poetry install
```

Activate the virtual environment:

```bash
poetry shell
```

### API Endpoints

The plugin exposes the following endpoints:

| Method | Path | Description |
|---|---|---|
| `POST` | `/upsert` | Upsert one or more documents into the datastore |
| `POST` | `/upsert-files` | Upsert documents from uploaded files |
| `POST` | `/query` | Query the datastore for the most relevant document chunks |
| `POST` | `/delete` | Delete documents by ID, metadata filter, or delete all |
| `GET` | `/` | Serve the plugin logo (used during registration) |

All endpoints (except the logo route) require the plugin's Bearer token in the `Authorization` header.

### Environment Variables

Configuration is handled via environment variables. The most important ones are:

```bash
# Server
BEARER_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.demo.token.secure
PORT=8080

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_EMBEDDING_BATCH_SIZE=128

# Datastore
DATASTORE=chroma
CHROMA_URL=http://localhost:8000
CHROMA_COLLECTION=chatgpt-retrieval
```

Each datastore has its own set of configuration variables, documented in the corresponding section below. A `.env` file in the project root is loaded automatically.

### Deployment

The repository includes documentation and deployment guides for several hosting providers:

- **Fly.io** — see [flyio.md](./docs/flyio.md)
- **Render** — see [render.md](./docs/render.md)
- **Heroku** — see [heroku.md](./docs/heroku.md)
- **Other options** — see [other-options.md](./docs/other-options.md)

The repository ships with a `Dockerfile`, so the plugin can be deployed to any platform that supports Docker containers.

### Running the API Locally

Run the server locally with:

```bash
poetry run python api.py
```

By default, the server runs on `http://localhost:8080`. For local plugin registration, set `localhost` as the plugin URL.

To easily test the API, you can call the endpoints with Python or `curl`. Example:

```bash
curl --location --request POST 'http://localhost:8080/query' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer YOUR_BEARER_TOKEN' \
  --data-raw '{"queries":[{"query":"What is the temperature in Salt Lake City?","top_k":3,"filter":{}}]}'
```

## Datastore Setup

### Chroma

The simplest way to get started with Chroma is using the provided `docker-compose.yml`:

```bash
cd examples/local-server/chroma
docker compose up -d
```

Then set:

```bash
DATASTORE=chroma
CHROMA_URL=http://localhost:8000
CHROMA_COLLECTION=chatgpt-retrieval
```

### LlamaIndex

Set:

```bash
DATASTORE=llama
```

Llama Cloud manages vector storage, embeddings hosting, and querying.

### Elasticsearch

```bash
DATASTORE=elasticsearch
ELASTICSEARCH_ADDRESS=https://...
ELASTICSEARCH_USERNAME=...
ELASTICSEARCH_PASSWORD=...
ELASTICSEARCH_INDEX=...
ELASTICSEARCH_VERIFY_CERTS=true
```

### MongoDB Atlas

Create a cluster in [MongoDB Atlas](https://www.mongodb.com/atlas), then set:

```bash
DATASTORE=mongodb_atlas
MONGODB_URI=mongodb+srv://...
MONGODB_DATABASE=...
MONGODB_COLLECTION=...
MONGODB_INDEX=...
```

### Pinecone

Set:

```bash
DATASTORE=pinecone
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...
PINECONE_INDEX=...
PINECONE_METRIC=cosine
PINECONE_NAMESPACE=...
```

### Postgres

Use the provided migration scripts:

- `scripts/pgvector/seed.sql`
- `scripts/pgvector/20230414142107_init_pg_vector.sql`

Set:

```bash
DATASTORE=postgres
PG_HOST=...
PG_PORT=5432
PG_USER=...
PG_PASSWORD=...
PG_DATABASE=...
PG_VECTOR_COLLECTION=...
```

### Redis

```bash
DATASTORE=redis
REDIS_HOST=...
REDIS_PORT=6379
REDIS_PASSWORD=...
REDIS_INDEX=...
```

### Weaviate

```bash
DATASTORE=weaviate
WEAVIATE_HOST=...
WEAVIATE_PORT=8080
WEAVIATE_API_KEY=...
WEAVIATE_CLASS=...
```

### Qdrant

```bash
DATASTORE=qdrant
QDRANT_URL=...
QDRANT_API_KEY=...
QDRANT_COLLECTION=...
```

### Milvus

```bash
DATASTORE=milvus
MILVUS_HOST=...
MILVUS_PORT=19530
MILVUS_USER=...
MILVUS_PASSWORD=...
MILVUS_COLLECTION=...
```

### Zilliz

```bash
DATASTORE=zilliz
ZILLIZ_URI=...
ZILLIZ_COLLECTION=...
```

### Azure Search

```bash
DATASTORE=azuresearch
AZURESEARCH_KEY=...
AZURESEARCH_URL=...
AZURESEARCH_INDEX=...
```

### Azure Cosmos DB

```bash
DATASTORE=azurecosmosdb
AZURECOSMOSDB_URI=...
AZURECOSMOSDB_KEY=...
AZURECOSMOSDB_COLLECTION=...
```

### AnalyticDB

```bash
DATASTORE=analyticdb
ANALYTICDB_HOST=...
ANALYTICDB_PORT=...
ANALYTICDB_USER=...
ANALYTICDB_PASSWORD=...
ANALYTICDB_DATABASE=...
ANALYTICDB_TABLE=...
```

### Supabase / pgvector

Follow the setup guide in [examples/local-server/pgvector](./examples/local-server/pgvector/README.md), including the Jupyter notebooks (`semantic-search.ipynb`, `semantic-search-and-filter.ipynb`) for testing semantic search and filtering.

## Metadata Extraction and Filtering

The plugin supports metadata enrichment of documents, which enables filtering during queries. The `scripts/extract_metadata.py` utility extracts metadata from documents using specialized extractors:

- **date** (`scripts/date.py`) — Detects dates in document text
- **file** (`scripts/file.py`) — Extracts file-related metadata (name, type, size, URL)
- **PII detection** (`scripts/pii_detection.py`) — Detects personally identifiable information using the `presidio-analyzer` library

Metadata can be attached to documents when upserting, and used as a filter in queries (e.g., restrict search to a specific source, date range, or file type).

## PII Detection and Redaction

The `scripts/pii_detection.py` script uses Microsoft's Presidio to detect PII entities (names, phone numbers, email addresses, etc.) in your documents. This is useful both for filtering out sensitive content and for redacting it before storing in the vector database.

## Uploading Documents

### JSON / JSONL

The plugin supports uploading documents as JSON or JSONL files. The `scripts/process_jsonl.py`, `scripts/process_json.py`, and example files (`examples/file-qa/README.md`, `example.jsonl`, `example.json`) show the expected format:

```json
{
  "id": "unique-document-id",
  "text": "The text content of the document.",
  "metadata": {
    "source": "https://example.com",
    "title": "Example document",
    "description": "..."
  }
}
```

### ZIP files

Use `scripts/process_zip.py` to process ZIP archives containing documents. Example files (`example.zip`) are included in the repository.

## Development

### Running tests

Each datastore has a corresponding test file (e.g., `tests/datastores/test_chroma_datastore.py`). Run the test suite with:

```bash
poetry run pytest
```

### Code style

The project uses Black for code formatting. Run:

```bash
poetry run black .
```

## Community Contributions

This repository was originally built by the OpenAI community and continues to accept contributions of new datastores, scripts, and improvements. When adding a new datastore, implement the `Datastore` interface from `datastore/datastore.py`, register it in `datastore/factory.py`, and add corresponding tests.
