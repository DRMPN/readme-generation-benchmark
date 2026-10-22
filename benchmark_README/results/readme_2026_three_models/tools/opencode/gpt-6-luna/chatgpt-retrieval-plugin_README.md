# ChatGPT Retrieval Plugin

This repository contains a FastAPI service for storing text as searchable document chunks and retrieving relevant chunks for natural-language queries. It generates embeddings through the OpenAI API (or an Azure OpenAI deployment) and uses a configurable vector datastore.

## How it works

- Documents submitted to `/upsert` are split into chunks (target size: 200 tokens by default), embedded, and written to the configured datastore. Supplying a document ID allows existing chunks for that document to be replaced.
- `/query` embeds each query and returns matching chunks with scores. Each query can include a metadata filter and `top_k` (default `3`).
- `/upsert-file` extracts text from supported uploads, then stores it like other documents. Supported formats are PDF, plain text, Markdown, DOCX, CSV, and PPTX.
- `/delete` removes records by chunk IDs, metadata filter, or the `delete_all` option.

The production application requires a bearer token for its API routes. The separate `local_server` application is a localhost testing helper and does not enforce authentication.

## Requirements

- Python 3.10
- [Poetry](https://python-poetry.org/)
- An OpenAI API key, or the corresponding Azure OpenAI configuration
- A configured datastore and its connection settings

## Installation and configuration

Install the project dependencies:

```bash
poetry install
```

Use `.env.example` as a reference for configuration. At minimum, set:

| Variable | Purpose |
| --- | --- |
| `DATASTORE` | Datastore provider name |
| `BEARER_TOKEN` | Secret accepted by the production API's bearer authentication |
| `OPENAI_API_KEY` | Key used to generate embeddings (unless using Azure OpenAI) |

The code reads configuration from process environment variables; it does not automatically load a `.env` file. For a POSIX shell, you can copy the template, edit the values, then export them into the current shell:

```bash
cp .env.example .env
# Edit .env and set the variables for your chosen provider.
set -a
. ./.env
set +a
```

Set only the provider-specific variables you need. `EMBEDDING_MODEL` defaults to `text-embedding-3-large`, and `EMBEDDING_DIMENSION` defaults to `256`; when changing embedding settings, make sure the selected datastore's vector dimension is compatible. Azure OpenAI settings are listed in `.env.example` as well.

### Datastore providers

Set `DATASTORE` to one of the provider names supported by the datastore factory:

`analyticdb`, `azurecosmosdb`, `azuresearch`, `chroma`, `elasticsearch`, `llama`, `milvus`, `mongodb`, `pinecone`, `postgres`, `qdrant`, `redis`, `supabase`, `weaviate`, or `zilliz`.

Each provider has its own setup notes and environment variables:

- [AnalyticDB](docs/providers/analyticdb/setup.md)
- [Azure Cosmos DB](docs/providers/azurecosmosdb/setup.md)
- [Azure AI Search](docs/providers/azuresearch/setup.md)
- [Chroma](docs/providers/chroma/setup.md)
- [Elasticsearch](docs/providers/elasticsearch/setup.md)
- [LlamaIndex](docs/providers/llama/setup.md)
- [Milvus](docs/providers/milvus/setup.md)
- [MongoDB Atlas](docs/providers/mongodb/setup.md)
- [Pinecone](docs/providers/pinecone/setup.md)
- [Postgres](docs/providers/postgres/setup.md)
- [Qdrant](docs/providers/qdrant/setup.md)
- [Redis](docs/providers/redis/setup.md)
- [Supabase](docs/providers/supabase/setup.md)
- [Weaviate](docs/providers/weaviate/setup.md)
- [Zilliz](docs/providers/zilliz/setup.md)

## Run the API

After setting the environment variables, start the production application:

```bash
poetry run start
```

This runs Uvicorn on `0.0.0.0:8000`. The API is bearer-token protected. Include the configured token in requests as `Authorization: Bearer <BEARER_TOKEN>`.

### API routes

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/upsert` | Insert or replace documents supplied as JSON |
| `POST` | `/upsert-file` | Upload and index a supported file (multipart form) |
| `POST` | `/query` | Search using one or more natural-language queries |
| `DELETE` | `/delete` | Delete by IDs, metadata filter, or all records |

The request and response models are defined in [`models/api.py`](models/api.py) and [`models/models.py`](models/models.py). A query request has this shape:

```json
{
  "queries": [
    {
      "query": "What does the project do?",
      "top_k": 3,
      "filter": {
        "source": "file"
      }
    }
  ]
}
```

`filter` and `top_k` are optional. Metadata filters support `document_id`, `source`, `source_id`, `author`, `start_date`, and `end_date`; `source` may be `email`, `file`, or `chat`. See the model definitions for the complete document and result schemas.

## Local plugin helper

For local testing of the included plugin manifest and OpenAPI schema, set the datastore and embedding environment variables, then run:

```bash
poetry run dev
```

This starts `local_server` on `localhost:3333`. It serves files from `local_server/` under `/.well-known/` and enables CORS for `http://localhost:3333` and `https://chat.openai.com`. This helper has no authentication and is intended for local testing, not as the production server. Plugin-related documentation in this repository is in the deprecated-plugins area: [`docs/deprecated/plugins.md`](docs/deprecated/plugins.md).

## Docker and deployment

The included [`Dockerfile`](Dockerfile) builds the application and starts `server.main:app`. It listens on `PORT`, then `WEBSITES_PORT`, or `8080` if neither is set. Supply the same required and provider-specific environment variables to the container.

Deployment notes are available for [Fly.io](docs/deployment/flyio.md), [Heroku](docs/deployment/heroku.md), [Render](docs/deployment/render.md), and [other container platforms](docs/deployment/other-options.md). Provider setup guides also include datastore-specific configuration.

## Examples and tests

- [`examples/`](examples/) contains provider notebooks, Docker Compose configurations, authentication examples, and a memory example.
- [`scripts/`](scripts/) contains JSON, JSONL, and ZIP processing examples.
- Run the test suite with `poetry run pytest` (test dependencies are included in the Poetry development group).

## License

This project is licensed under the MIT License; see [`LICENSE`](LICENSE).
