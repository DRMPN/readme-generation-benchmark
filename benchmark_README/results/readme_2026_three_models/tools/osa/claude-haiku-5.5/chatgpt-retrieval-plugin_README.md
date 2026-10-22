# chatgpt-retrieval-plugin-o6elp184

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![elasticsearch](https://img.shields.io/badge/Elasticsearch-005571.svg?style={0}&logo=Elasticsearch&logoColor=white)
![fastapi](https://img.shields.io/badge/FastAPI-009688.svg?style={0}&logo=FastAPI&logoColor=white)
![numpy](https://img.shields.io/badge/NumPy-013243.svg?style={0}&logo=NumPy&logoColor=white)
![openai](https://img.shields.io/badge/OpenAI-412991.svg?style={0}&logo=OpenAI&logoColor=white)
![pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?style={0}&logo=Pydantic&logoColor=white)
![python](https://img.shields.io/badge/Python-3776AB.svg?style={0}&logo=Python&logoColor=white)
![redis](https://img.shields.io/badge/Redis-DC382D.svg?style={0}&logo=Redis&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project is a FastAPI-based document retrieval service that lets clients upsert, query, and delete text documents using natural-language queries with metadata filters. It is built to serve as a ChatGPT retrieval plugin backend and is intended for developers building retrieval-augmented or plugin integrations who need to choose and configure a vector database backend. The backend is selected at startup through configuration, and the API is consumed by an LLM or client application rather than end users. For a first look at the available API surfaces, see the API reference; for runnable setup steps, see Getting Started.

---

## Core Features

- **Document upsert and management via API:** Accepts documents as JSON or file uploads (including DOCX, PDF, and PPTX parsing), with optional metadata, and returns the stored document IDs so applications can index content for later retrieval.
- **Semantic query with metadata filtering:** Accepts natural language queries with optional filters (such as source, author, document ID, or date range) and returns ranked document chunks with relevance scores, enabling retrieval-augmented answers in ChatGPT plugin integrations.
- **Document deletion by ID, filter, or full clear:** Lets developers remove vectors by document IDs, metadata filters, or all records, keeping the index aligned with source content.
- **Pluggable vector database backends:** Selects one of many supported vector stores (such as Chroma, Pinecone, Weaviate, Qdrant, Milvus, Redis, Postgres, and Elasticsearch) through a single environment variable, so teams can switch storage without changing the API surface.
- **Bearer token authentication:** Protects all endpoints with a token set in the environment, giving a simple access control layer for deployed services.
- **Reduced OpenAPI schema for plugin use:** Exposes a sub-application with a focused OpenAPI description of the query endpoint (and upsert in the memory example), so LLM clients receive a concise, usable tool specification.

---

## Installation

**Prerequisites:** requires Python ^3.10

Install chatgpt-retrieval-plugin-o6elp184 using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/chatgpt-retrieval-plugin-o6elp184
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

### Prerequisites

- Python `^3.10` (see `pyproject.toml`)
- Poetry for dependency management
- A vector database backend, selected with the `DATASTORE` environment variable. Supported values are listed in `datastore/factory.py`.
- `OPENAI_API_KEY` and `BEARER_TOKEN` environment variables

### Quickstart

1. Clone the repository and change into the project directory:

```
git clone https://github.com/openai/chatgpt-retrieval-plugin.git
cd chatgpt-retrieval-plugin
```

2. Install dependencies with Poetry:

```
poetry install
```

3. Set the environment variables in your shell:

- `DATASTORE`: selects the backend. The app fails at startup if it is not set.
- `BEARER_TOKEN`: required. `server/main.py` asserts that it is set when the module loads. API requests must send it as an `Authorization: Bearer <token>` header.
- `OPENAI_API_KEY`: used for embeddings.

Provider-specific settings are described in the per-provider guides in `docs/`.

4. Start the server:

```
poetry run start
```

This runs the `start` script (`server.main:start`), which starts uvicorn on `0.0.0.0:8000`. To confirm the server is running, open `http://0.0.0.0:8000/sub/openapi.json`.

5. (Optional) Run the local testing variant:

```
poetry run dev
```

This runs the `dev` script (`local_server.main:start`), which starts uvicorn on `localhost:3333`. This variant does not validate the bearer token, but it still requires `DATASTORE` to be set.

---

## Architecture

The service is a modular monolith built around a single FastAPI application with a pluggable vector store backend.

- **API layer (`server/main.py`)**: A FastAPI app exposes `/upsert-file`, `/upsert`, `/query`, and `/delete` endpoints. All routes require a Bearer token validated against the `BEARER_TOKEN` environment variable. A sub-application mounted at `/sub` provides a reduced OpenAPI schema for the query endpoint (and upsert in the `examples/memory` variant).
- **Datastore abstraction (`datastore/datastore.py`)**: The abstract `DataStore` class defines the `upsert`, `query`, and `delete` contract. Its `upsert` and `query` methods handle chunking and embedding generation before delegating to provider-specific `_upsert` and `_query` implementations.
- **Provider selection (`datastore/factory.py`)**: `get_datastore()` selects one provider at startup based on the `DATASTORE` environment variable and imports only the chosen provider module. Provider implementations live in `datastore/providers/`.
- **Services (`services/`)**: Helper modules handle text chunking (`chunks.py`), embedding generation via OpenAI (`openai.py`), and file parsing for uploads (`file.py`).
- **Data models (`models/`)**: Pydantic models define request, response, document, and metadata schemas shared across the API and datastore layers.

**Primary control and data flow:** A client sends a request to an API endpoint. For upserts, documents are chunked and embedded, then written through the selected provider. For queries, the query text is embedded and passed to the provider's `_query` method, which returns scored chunks.

**Variants:** `local_server/main.py` is a local testing variant that serves the plugin manifest and OpenAPI files from `local_server/`. `examples/memory/main.py` is an alternate server that enables the upsert endpoint.

*Note: Deployment topology, CI/CD pipelines, and runtime infrastructure beyond the Dockerfile and example Docker Compose files are not evidenced in the provided context.*

---

## API Reference

The service exposes HTTP endpoints through FastAPI and a Python `DataStore` interface that provider implementations extend. The service is not script-only.

### HTTP endpoints (`server/main.py`)

| Method | Path | Purpose |
|---|---|---|
| POST | `/upsert-file` | Uploads a file (`file`) with an optional `metadata` string, then upserts the extracted document. Returns `UpsertResponse`. |
| POST | `/upsert` | Upserts `UpsertRequest.documents`. Returns `UpsertResponse`. |
| POST | `/query` | Runs `QueryRequest.queries`. Returns `QueryResponse`. |
| POST | `/sub/query` | Same query handler, served by the `sub_app` sub-application mounted at `/sub`. |
| DELETE | `/delete` | Deletes by `ids`, `filter`, or `delete_all`. Returns `DeleteResponse`. Returns HTTP 400 if none of these is provided. |

### Authentication

All routes on the `server/main.py` app depend on `validate_token`. Send `Authorization: Bearer <token>`, where the token matches the `BEARER_TOKEN` environment variable. The app asserts that `BEARER_TOKEN` is set at import time. Missing or invalid tokens return HTTP 401.

`local_server/main.py` defines the same upsert, query, and delete routes without token validation. It also serves `/.well-known/ai-plugin.json`, `/.well-known/logo.png`, and `/.well-known/openapi.yaml` from `local_server/`.

### Python interfaces

- `datastore.datastore.DataStore`: abstract base class. Public methods are `upsert(documents, chunk_token_size=None)`, `query(queries)`, and `delete(ids=None, filter=None, delete_all=None)`. Provider implementations supply the abstract `_upsert`, `_query`, and `delete` methods.
- `datastore.factory.get_datastore()`: async function that returns a `DataStore` based on the `DATASTORE` environment variable. Supported values are listed in `datastore/factory.py`.
- `services.file.get_document_from_file(file, metadata)`: converts an uploaded file into a document for `/upsert-file`.
- `models.models`: `Document`, `DocumentMetadata`, `DocumentMetadataFilter`, `Query`, `QueryResult`, and `Source`.
- `models.api`: request and response models (`UpsertRequest`, `UpsertResponse`, `QueryRequest`, `QueryResponse`, `DeleteRequest`, `DeleteResponse`). Field definitions are not included in the reviewed context.

### Entry points

- `server.main:start` (script `start`): runs uvicorn on `0.0.0.0:8000`.
- `local_server.main:start` (script `dev`): runs uvicorn on `localhost:3333`.

A code comment in `server/main.py` says the sub-application schema is available at `/sub/openapi.json` when running locally. This path was not verified at runtime.

---

## Testing

Verification in this repository relies on pytest, configured in `pyproject.toml` under `[tool.pytest.ini_options]` with `pythonpath = ["."]` and `asyncio_mode="auto"`. Test dependencies (`pytest`, `pytest-cov`, `pytest-asyncio`, `httpx`) are declared in the Poetry dev group.

**Test artifacts**

- Provider tests are located under `tests/datastore/providers/`, with one subdirectory per vector store backend (for example `chroma`, `postgres`, `qdrant`, `redis`, `weaviate`).
- `tests/datastore/providers/mongodb_atlas/test_integration.py` is an integration-style test file alongside the unit-style `test_mongodb_datastore.py`.
- `tests/datastore/providers/weaviate/docker-compose.yml` is present for running the Weaviate tests against a local service.

**Running tests**

The exact test run command is not defined in the available context. Pytest is the configured framework, and the provider test files are the entry points to review. Test pass/fail status and CI test execution are not evidenced in the repository.

**Scope notes**

- Tests are present for most providers. Not every provider under `datastore/providers/` has a corresponding test directory in the visible tree.
- No CI workflow files are visible in the repository, so automated test runs on pull requests are not evidenced.

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Documentation

A detailed chatgpt-retrieval-plugin-o6elp184 description is available [here](./docs).

---

## Contributing

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). chatgpt-retrieval-plugin-o6elp184 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{chatgpt-retrieval-plugin-o6elp184,

        author = {README Benchmark},

        title = {chatgpt-retrieval-plugin-o6elp184 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---