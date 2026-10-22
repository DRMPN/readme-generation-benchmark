# chatgpt-retrieval-plugin-xztdawyl

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![elasticsearch](https://img.shields.io/badge/Elasticsearch-005571.svg?logo=Elasticsearch&logoColor=white)
![fastapi](https://img.shields.io/badge/FastAPI-009688.svg?logo=FastAPI&logoColor=white)
![numpy](https://img.shields.io/badge/NumPy-013243.svg?logo=NumPy&logoColor=white)
![openai](https://img.shields.io/badge/OpenAI-412991.svg?logo=OpenAI&logoColor=white)
![pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?logo=Pydantic&logoColor=white)
![python](https://img.shields.io/badge/Python-3776AB.svg?logo=Python&logoColor=white)
![redis](https://img.shields.io/badge/Redis-DC382D.svg?logo=Redis&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Citation](#citation)

---

## Overview

This project provides a semantic retrieval backend designed to work as a ChatGPT plugin: it ingests documents, splits them into token-based chunks, generates embeddings, and exposes upsert, query, and delete operations through a REST API. Written in Python, it targets developers deploying or extending the retrieval service, teams evaluating vector database backends, and data scientists prototyping semantic search. The datastore layer is pluggable, allowing operators to select among supported vector database providers at runtime via configuration, and the repository also offers provider-specific notebook workflows for exploratory search. See the Getting Started section for runnable setup steps.

---

## Core Features

- **Natural-language semantic search**: Ask questions in plain text, optionally narrowed by metadata filters, and receive scored, relevant document chunks from an API secured with bearer-token authentication.
- **Out-of-the-box ChatGPT plugin integration**: The service exposes a plugin manifest and OpenAPI schema and runs a CORS-enabled local server, so it can be registered with ChatGPT and exercised end to end without extra glue code.
- **Swappable vector database backends**: Point the service at more than a dozen providers—including Pinecone, Weaviate, Milvus/Zilliz, Redis, Qdrant, Chroma, Elasticsearch, Postgres, Supabase, MongoDB Atlas, Azure AI Search, and Azure Cosmos DB—via a single environment variable, keeping application code unchanged.
- **Complete document lifecycle management**: Upsert content as structured payloads or direct file uploads, replace previous versions by re-upserting a document ID, and delete entries by ID, metadata filter, or the entire index.
- **Automatic ingestion pipeline**: Submitted text is split into token-aware chunks and embedded with OpenAI embeddings before storage, so no custom preprocessing code is required.

---

## Installation

**Prerequisites:** Python 3.10 or later (as specified in `pyproject.toml`), with Poetry for dependency management.

Install chatgpt-retrieval-plugin-xztdawyl from the current local checkout:

1. Open the repository root:

```sh
cd path/to/chatgpt-retrieval-plugin-xztdawyl
```

2. Install the project and its dependencies with Poetry:

```sh
poetry install
```

---

## Getting Started

**Prerequisites**

- Python with Poetry — dependencies are defined in `pyproject.toml` / `poetry.lock` (see the Installation section).
- An OpenAI API key for generating embeddings (`OPENAI_API_KEY`).
- Access to a supported vector database.

**Steps**

1. **Choose a datastore.** Set `DATASTORE` to a supported provider, for example `pinecone`, `weaviate`, `chroma`, `qdrant`, `redis`, `postgres`, or `elasticsearch`. The full list of providers is in `datastore/factory.py`, and each provider has its own setup documentation and connection settings.

2. **Configure the environment.** Copy `.env.example` to `.env` and fill in the values:
   - `DATASTORE` — the provider chosen above
   - `OPENAI_API_KEY` — your OpenAI API key
   - `BEARER_TOKEN` — the bearer token used to authenticate API requests

   Add any provider-specific variables required by your datastore. Note that the server asserts that `DATASTORE` is set at startup.

3. **Start the local plugin server.**

```bash
   poetry run dev
```

   This runs the FastAPI app in `local_server/main.py` on port 3333, set up for local plugin testing with ChatGPT. It serves the plugin manifest and OpenAPI schema at:

   - `http://localhost:3333/.well-known/ai-plugin.json`
   - `http://localhost:3333/.well-known/openapi.yaml`

4. **Try the API.** Four endpoints are exposed on `http://localhost:3333`:

   - `POST /upsert` — insert or update documents
   - `POST /upsert-file` — upload and ingest a file
   - `POST /query` — search stored documents with natural-language queries
   - `DELETE /delete` — delete by ids, metadata filter, or `delete_all`

5. **Deploy to production (optional).** Step-by-step guides for Fly.io, Heroku, and other platforms are in `docs/deployment/`. After deploying, update the plugin URL in `.well-known/ai-plugin.json` and `.well-known/openapi.yaml` and redeploy.

---

## Architecture

A single FastAPI service that exposes a retrieval API (upsert, query, delete) over documents, backed by a pluggable vector-database layer. All endpoints require bearer-token authentication (`BEARER_TOKEN`).

- **HTTP API (`server/main.py`)** — exposes `POST /upsert`, `POST /upsert-file`, `POST /query`, and `DELETE /delete`, and mounts `/.well-known` static assets (plugin manifest and OpenAPI spec). A `/sub` sub-app titled "Retrieval Plugin API" exposes only `/query` with its own OpenAPI schema.
- **Datastore layer (`datastore/`)** — an abstract `DataStore` base class defines `upsert`, `query`, and `delete`. At startup, `datastore/factory.py` (`get_datastore`) instantiates the provider selected by the `DATASTORE` environment variable via lazy imports, supporting `pinecone`, `weaviate`, `milvus`/`zilliz`, `redis`, `qdrant`, `chroma`, `elasticsearch`, `postgres`, `supabase`, `mongodb`, `azurecosmosdb`, `azuresearch`, `analyticdb`, and `llama`.
- **Request flow** — upsert: text is chunked (tiktoken `cl100k_base`), embeddings are generated via the OpenAI API, and the provider's `_upsert` stores the chunks. Query: query embeddings are generated and the provider's `_query` returns scored chunks. Delete: ids, metadata filters, or `delete_all` are passed through to the provider.
- **Shared services (`services/`)** — chunking, OpenAI embeddings, file parsing, metadata extraction, date handling, and PII detection, used by both the API and the datastore base class.
- **Models (`models/`)** — Pydantic models (documents, chunks, queries, results, metadata filters) shared across the API, services, and datastore layers.
- **Local plugin server (`local_server/main.py`)** — a variant of the API for local plugin testing on port 3333, with CORS enabled for `https://chat.openai.com`, serving the AI-plugin manifest, logo, and OpenAPI spec from `./local_server`.
- **Ingestion scripts (`scripts/`)** — CLI utilities that prepare documents for upsert.

---

## Testing

Tests live under `tests/`, organized per vector database provider in `tests/datastore/providers/` (for example, `tests/datastore/providers/chroma/test_chroma_datastore.py` and `tests/datastore/providers/postgres/test_postgres_datastore.py`). MongoDB Atlas additionally includes an integration test at `tests/datastore/providers/mongodb_atlas/test_integration.py`.

- **Provider-specific suites**: Each datastore provider with tests has a dedicated test module under `tests/datastore/providers/`; verify changes to a provider against its matching test file.
- **Local test dependencies**: `tests/datastore/providers/weaviate/docker-compose.yml` provides a Docker Compose setup for the Weaviate datastore tests.
- **Local plugin testing**: `local_server/main.py` mirrors `server/main.py` for testing the plugin locally; start it with `poetry run dev` (serves on port 3333).
- **No CI configuration**: The repository contains no CI workflow files (only a pull request template under `.github/`), so run the relevant tests locally as part of change verification.

No suite-wide test command is specified here; check the `Makefile` and `pyproject.toml` for available tasks and tooling definitions.

---

## Examples

Examples of how the service should be set up and used are available in the [`examples/`](./examples) directory