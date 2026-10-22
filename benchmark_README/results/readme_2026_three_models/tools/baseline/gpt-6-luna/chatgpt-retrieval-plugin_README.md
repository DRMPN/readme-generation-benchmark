# ChatGPT Retrieval Plugin

A FastAPI service for storing documents in a vector database and retrieving relevant text chunks with natural-language queries. Documents are split into chunks, embedded using the OpenAI API, and saved through a configurable datastore provider. Queries are embedded and searched against that datastore, with optional metadata filters.

The repository includes API and local-development servers, support for multiple datastore providers, document-processing utilities, provider setup guides, and examples for function calling and conversation memory.

## Features

- Upsert documents as text or upload supported files.
- Split text into chunks and generate embeddings before storage.
- Query one or more natural-language prompts, with optional metadata filters and a result limit.
- Delete stored data by document ID, metadata filter, or all records.
- Choose among Chroma, LlamaIndex, Pinecone, Weaviate, Milvus, Zilliz, Redis, Azure Cosmos DB, Azure Cognitive Search, Qdrant, Supabase, PostgreSQL with pgvector, AnalyticDB, Elasticsearch, and MongoDB Atlas.
- Use scripts to ingest JSON, JSONL, and ZIP file dumps, optionally screening for PII or extracting metadata.

## Requirements

- Python 3.10 or later in the Python 3.10 series, as specified by the project.
- Poetry for installing and running the application.
- An OpenAI API key for embeddings.
- A configured datastore and the environment variables required by its provider.

Some providers also require a hosted service or a locally running database. See the provider guides in [`docs/providers`](docs/providers) for provider-specific setup and configuration.

## Setup

Clone the repository and install its dependencies:

```bash
git clone https://github.com/openai/chatgpt-retrieval-plugin.git
cd chatgpt-retrieval-plugin
poetry install
```

The repository contains an [`.env.example`](.env.example) file. Use it as a starting point for your local environment configuration, and set the variables required by your chosen datastore. At minimum, the application needs `DATASTORE`, `BEARER_TOKEN`, and `OPENAI_API_KEY`. The `DATASTORE` value must match a supported provider name, such as `qdrant`, `redis`, or `postgres`. Provider-specific variables are documented in the corresponding setup guide.

The server reads configuration from environment variables; it does not automatically load a `.env` file in the shown server code. If you use a dotenv file, make sure its values are available in the process environment when you start the application.

For embedding configuration, `EMBEDDING_MODEL` defaults to `text-embedding-3-large`, and `EMBEDDING_DIMENSION` defaults to `256`. Ensure the configured dimension matches the index or collection in your datastore. `OPENAI_EMBEDDING_BATCH_SIZE` controls the number of chunk embeddings requested per batch and defaults to `128`.

## Running the service

Start the authenticated API server:

```bash
poetry run start
```

The server listens on `0.0.0.0:8000`. It requires `BEARER_TOKEN` at startup and protects its routes with HTTP Bearer authentication. Send the matching token in the `Authorization` header.

For local plugin development, start the separate local server:

```bash
poetry run dev
```

This server listens on `localhost:3333` and serves the local manifest, logo, and OpenAPI description under `/.well-known/`. It is configured with local CORS origins and does not require authentication. It still needs a configured datastore and any credentials required by that datastore.

The production server serves its static plugin files under `/.well-known/`. Before deploying, update the application URL in [`.well-known/ai-plugin.json`](.well-known/ai-plugin.json) and [`.well-known/openapi.yaml`](.well-known/openapi.yaml) to match the deployed service.

## API usage

All API requests to the authenticated server require a Bearer token.

### Upsert documents

`POST /upsert` accepts a `documents` array. Each document has required `text` and optional `id` and `metadata` fields. Metadata can include `source` (`email`, `file`, or `chat`), `source_id`, `url`, `created_at`, and `author`.

```bash
curl -X POST http://localhost:8000/upsert \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"documents":[{"text":"Example document text.","metadata":{"source":"file"}}]}'
```

`POST /upsert-file` accepts a file upload and optional metadata as form data. Supported file types include PDF, plain text, Markdown, DOCX, CSV, and PPTX. If metadata is omitted or invalid, the uploaded document is assigned the `file` source.

### Query

`POST /query` accepts a `queries` array. Each query requires a `query` string and may include `top_k` and a metadata `filter`. The default `top_k` is 3. Filters can include document ID, source, source ID, author, and date bounds.

```bash
curl -X POST http://localhost:8000/query \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"queries":[{"query":"What does the document say?","top_k":3}]}'
```

The response contains a result set for each query, with matching chunks, metadata, and scores.

### Delete

`DELETE /delete` accepts one or more of `ids`, `filter`, and `delete_all`. At least one must be provided. The `ids` field refers to document IDs for this API operation.

The production server also exposes a query-only OpenAPI sub-application at `/sub/openapi.json`. The repository’s main OpenAPI file describes the query endpoint for plugin use.

## Configuration and datastore guides

Set `DATASTORE` to one of the provider names supported by [`datastore/factory.py`](datastore/factory.py). Provider configuration is not interchangeable: for example, Qdrant uses `QDRANT_URL`, while PostgreSQL uses `PG_HOST`, `PG_PORT`, `PG_USER`, `PG_PASSWORD`, and `PG_DB`.

Browse [`docs/providers`](docs/providers) for environment-variable tables, database setup instructions, and provider-specific test commands. The guides cover services such as Pinecone, Weaviate, Redis, Elasticsearch, and Azure Cognitive Search, as well as database-backed options including PostgreSQL, Supabase, and MongoDB Atlas.

To reduce deployment image size, the deployment documentation describes removing dependencies for unused providers from `pyproject.toml`. The Docker build exports the Poetry dependencies to a requirements file before installing them.

## Development and utilities

The project’s Poetry configuration provides `start` and `dev` scripts. Development dependencies include pytest, pytest-cov, pytest-asyncio, and httpx.

The ingestion tools under `scripts/` process JSON, JSONL, and ZIP files and upsert their documents to the selected datastore. Their READMEs explain accepted input formats and options for custom metadata, PII screening, and metadata extraction. The PII screening and metadata extraction functions are examples intended to be adapted to a particular use case.

The `examples/` directory also includes Docker Compose configurations for selected databases, provider notebooks, and examples for function calling and conversation memory.

## Testing

Run the test suite from the repository root:

```bash
poetry run pytest
```

Provider tests may require a running database, valid credentials, or provider-specific environment variables. Run an individual test module with, for example:

```bash
poetry run pytest tests/datastore/providers/qdrant/test_qdrant_datastore.py
```

Consult the relevant provider setup guide for integration-test prerequisites. Some guides provide Docker commands or Compose configurations for starting a local service.

## Deployment

A `Dockerfile` builds the application using Python 3.10 and starts `server.main:app` with Uvicorn. The container listens on `PORT`, then `WEBSITES_PORT`, or defaults to port `8080`. Deployment guides are available for Fly.io, Heroku, and Render under [`docs/deployment`](docs/deployment). Set the required application and datastore environment variables in the hosting platform before starting the service.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for the full terms.
