# ChatGPT Retrieval Plugin

A FastAPI-based retrieval service for connecting ChatGPT or other applications to a vector database. It accepts documents, creates or stores embeddings through a configured datastore, and returns relevant passages for natural-language queries.

The repository includes multiple datastore integrations, document-processing utilities, example datasets and notebooks, and deployment examples.

## Features

- **Document ingestion and retrieval** through a small HTTP API.
- **Multiple datastore backends:** Chroma, MongoDB Atlas, PostgreSQL, Pinecone, Redis, Azure AI Search, AnalyticDB, Qdrant, Zilliz, Weaviate, Elasticsearch, Milvus, pgvector, Azure Cosmos DB, Supabase, and LlamaIndex.
- **Plugin metadata and API description** in `ai-plugin.json` and `openapi.yaml`.
- **Document preparation tools** for processing JSON, JSONL, and ZIP files.
- **Examples and notebooks** for semantic search and filtering.

## How it works

1. Prepare documents with text, IDs, and optional metadata.
2. Send them to the plugin’s upsert endpoint.
3. The configured datastore stores the documents and their embeddings.
4. Send one or more natural-language queries to the query endpoint.
5. The service returns matching passages and associated metadata.

The plugin provides retrieval; it does not itself generate a final answer from the retrieved passages. A calling application, such as ChatGPT, can use the results as context.

## Requirements

- Python and Poetry
- An API key for the embedding provider used by the project
- A running instance or account for the datastore you select

Some datastores require additional services or credentials. See the relevant datastore implementation and setup documentation before configuring one.

## Installation

Clone the repository and install its dependencies:

```bash
git clone <repository-url>
cd chatgpt-retrieval-plugin-bzkwg8_o
poetry install
```

Create a `.env` file in the project root. At minimum, configure the datastore and credentials required by your setup. A typical configuration includes:

```dotenv
DATASTORE=<datastore-name>
OPENAI_API_KEY=<your-openai-api-key>
BEARER_TOKEN=<a-long-random-secret>
```

The datastore name and its required environment variables depend on the backend. Consult the relevant implementation under `datastore/` and the setup guides included in the repository. Do not commit secrets or share a production bearer token.

## Run locally

Start the API with Uvicorn:

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

For local development, you can enable automatic reload:

```bash
poetry run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

When the server is running, the OpenAPI specification is available at:

```text
http://localhost:8000/openapi.yaml
```

Use the repository’s `ai-plugin.json` and `openapi.yaml` when configuring a compatible plugin client. For a deployed service, make sure the manifest and API description point to the publicly reachable HTTPS URL for that deployment.

## API overview

The API is described in `openapi.yaml`; use it as the source of truth for the complete request and response schemas.

### Query documents

Send one or more queries to `POST /query`. A request generally contains a `queries` array, with each item holding a query string and optionally a filter. It may also include a result limit.

Example:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "queries": [
      {
        "query": "How do I configure the service?"
      }
    ],
    "top_k": 3
  }'
```

The response contains matching document passages and relevant metadata. Exact fields and filter syntax are defined in `openapi.yaml`.

### Upsert documents

Send documents to `POST /upsert`. A document typically includes an `id`, `text`, and optional `metadata`.

```bash
curl -X POST http://localhost:8000/upsert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -d '{
    "documents": [
      {
        "id": "getting-started",
        "text": "Instructions for getting started with the service.",
        "metadata": {
          "source": "docs"
        }
      }
    ]
  }'
```

Check the OpenAPI definition for required fields, batching behavior, and any backend-specific limitations.

### Delete documents

Use `POST /delete` to remove documents by ID or filter. Some implementations may also support deleting all indexed documents. Treat broad deletion operations with care, especially in production.

## Choosing a datastore

Datastore integrations are implemented in `datastore/`. The repository includes:

| Backend | Implementation |
|---|---|
| Chroma | `chroma_datastore.py` |
| MongoDB Atlas | `mongodb_atlas_datastore.py` |
| PostgreSQL | `postgres_datastore.py` |
| Pinecone | `pinecone_datastore.py` |
| Redis | `redis_datastore.py` |
| Azure AI Search | `azuresearch_datastore.py` |
| AnalyticDB | `analyticdb_datastore.py` |
| Qdrant | `qdrant_datastore.py` |
| Zilliz | `zilliz_datastore.py` |
| Weaviate | `weaviate_datastore.py` |
| LlamaIndex | `llama_datastore.py` |
| Elasticsearch | `elasticsearch_datastore.py` |
| Milvus | `milvus_datastore.py` |
| pgvector | `pgvector_datastore.py` |
| Azure Cosmos DB | `azurecosmosdb_datastore.py` |
| Supabase | `supabase_datastore.py` |

Configure the backend using the variables it expects; there is no single set of connection settings that applies to every provider. The datastore factory and implementation files show how the selected backend is initialized. Backend-specific setup guides and Compose files are also included in the repository.

## Preparing documents

The repository includes scripts for common ingestion workflows:

- `process_json.py` — prepare JSON input.
- `process_jsonl.py` — prepare JSON Lines input.
- `process_zip.py` — process ZIP archives.
- `chunks.py` — split text into chunks.
- `extract_metadata.py` — extract or prepare document metadata.
- `file.py` — file-related processing utilities.
- `pii_detection.py` — personally identifiable information detection utilities.

Use the examples alongside these scripts to understand the expected input format. Before ingesting a large collection, test a small sample and verify that chunking, metadata, and filtering behave as expected.

The repository also includes sample data such as `example.json`, `example.jsonl`, and `example.zip`, plus notebooks for semantic search and filtering.

## Docker and deployment

A `Dockerfile`, `docker-compose.yml` files, and deployment guides are included. Use the Compose configuration appropriate to your datastore and follow the associated setup documentation.

For a production deployment:

- Set a strong `BEARER_TOKEN` and keep it secret.
- Configure datastore credentials as deployment secrets, not as committed files.
- Serve the API over HTTPS.
- Restrict access to the service and datastore to trusted networks where possible.
- Review the deployment guide for your platform and datastore.

The repository includes deployment notes for Fly.io, Render, and Heroku, as well as additional deployment options.

## Development and tests

Run the test suite with:

```bash
poetry run pytest
```

Many datastore tests require credentials or a running backend, so configure the relevant environment before running them. The repository contains integration tests and datastore-specific tests, including tests for Chroma, Elasticsearch, MongoDB, PostgreSQL, Redis, Qdrant, Supabase, Weaviate, and others.

`docker-compose.yml` and the datastore-specific Compose files can help start local dependencies for development and testing.

## Project layout

```text
main.py                 API application
api.py                  API definitions and request handling
models.py               Request and response models
datastore/              Datastore implementations and factory
openapi.yaml            API specification
ai-plugin.json          Plugin manifest
process_*.py            Document ingestion utilities
chunks.py               Text chunking utilities
extract_metadata.py     Metadata utilities
pii_detection.py        PII detection utilities
Dockerfile              Container build
docker-compose*.yml     Local service configurations
```

## Security and privacy

This service may store submitted documents and derived embeddings in an external datastore. Review the retention, access-control, and data-processing policies for the datastore and embedding provider you use. Avoid ingesting sensitive information unless your configuration and policies permit it. Protect the API with a strong bearer token, and do not expose datastore credentials or secrets in logs, source control, or public deployment configuration.

## License

See [`LICENSE`](LICENSE).
