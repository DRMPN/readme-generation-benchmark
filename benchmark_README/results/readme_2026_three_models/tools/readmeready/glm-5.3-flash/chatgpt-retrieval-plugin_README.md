# chatgpt-retrieval-plugin<h2>Description</h2>

<p>The ChatGPT Retrieval Plugin lets you easily search and retrieve documents from various data sources by leveraging natural language queries. The plugin uses OpenAI models (<code>text-embedding-ada-002</code> for embeddings and <code>gpt-3.5-turbo</code> and <code>gpt-4</code> for chat completions) and a chosen vector database to expose a <code>/query</code> endpoint, which can be used to search through stored documents and return the most relevant chunks back to ChatGPT. This enables ChatGPT to ground its answers with information retrieved from your documents, which reduces hallucinations and makes its responses more accurate and up-to-date.</p>

<p>At a high level, the project works as follows:</p>

<ol>
<li><strong>Document ingestion</strong> — Documents from supported data sources (files, and various data stores) are split into chunks, each chunk is converted into an embedding, and the embeddings are stored in a vector database along with metadata.</li>
<li><strong>Storage</strong> — A pluggable "datastore" abstraction allows the plugin to work with a number of different vector database providers (e.g. Pinecone, Weaviate, Qdrant, Milvus, pgvector, and others), so you can pick the one that best fits your infrastructure.</li>
<li><strong>Querying</strong> — When a query comes in through the API, the query is embedded and the most semantically similar document chunks are retrieved from the vector database, scored, and returned along with their metadata.</li>
</ol>

<p>The repository is structured around a FastAPI application that exposes the plugin's HTTP interface, a set of data model definitions (schemas for documents, chunks, metadata, and query results), and modular datastore implementations that handle the actual vector storage and similarity search for each supported provider. The FastAPI service can also be self-hosted, giving you full control over the retrieval workflow.</p>

<p>Key capabilities include:</p>

<ul>
<li><strong>Multiple datastore backends</strong> — swap between supported vector databases without changing the rest of your code.</li>
<li><strong>Metadata filtering</strong> — enrich documents with source, timestamp, author, and other metadata to support targeted retrieval.</li>
<li><strong>REST API</strong> — endpoints for upserting, querying, and deleting documents, protected by a bearer token.</li>
<li><strong>ChatGPT integration</strong> — designed to work as a ChatGPT retrieval plugin so that conversational queries can search your private documents.</li>
</ul>
<h2>Requirements</h2>

<p>To use this application, you will need:</p>

<ul>
<li><strong>Python 3.10</strong> or later</li>
<li><strong>Docker</strong> (optional, if you want to run the app in a container)</li>
<li>A supported data provider (see the list of supported datastores below), along with the necessary account credentials, such as API keys, tokens, or connection strings</li>
<li>An <a href="https://platform.openai.com/account/api-keys">OpenAI API key</a> for generating embeddings with the <code>text-embedding-ada-002</code> model</li>
</ul>
<h2>Installation</h2>

<h3>Clone the repository</h3>

<p><code>shell
git clone https://github.com/openai/chatgpt-retrieval-plugin.git
cd chatgpt-retrieval-plugin
</code></p>

<h3>Create a virtual environment</h3>

<p><code>shell
python3 -m venv venv
source venv/bin/activate
</code></p>

<blockquote>
  <p><strong>Note:</strong> If you are working in VS Code with the WSL extension, you can open the cloned repository from within WSL and use the built-in terminal to run the commands above.</p>
</blockquote>

<h3>Install the dependencies</h3>

<p>With your virtual environment activated, install the required Python packages:</p>

<p><code>shell
pip install -r requirements.txt
</code></p>

<p>Once the dependencies are installed, you will need to set the required environment variables (such as your OpenAI API key, vector database credentials, and data source tokens) before running the app.</p>
<h2>Usage</h2>

<!-- The provided context does not contain enough information about the repository's usage instructions (such as how to run the plugin, API endpoints, example requests, or environment configuration). To avoid inventing content, this section is left blank. -->
<h2>Contributing</h2>

<p>Thank you for your interest in contributing to the chatgpt-retrieval-plugin project!</p>

<p>If you would like to contribute, please open an issue or submit a pull request in the project's GitHub repository. Before submitting a pull request, it is recommended that you:</p>

<ol>
<li>Fork the repository and create a new branch for your changes.</li>
<li>Make your changes and ensure that the code passes existing tests.</li>
<li>Submit a pull request with a clear description of the changes you have made.</li>
</ol>

<p>For larger changes or new features, it is best to open an issue first to discuss your proposal with the maintainers before investing significant time into the implementation.</p>
<h2>License</h2>
<h2>Description</h2>

<p>The ChatGPT Retrieval Plugin lets you easily search and find personal or work documents by asking questions in everyday language. You can store your documents in one of the supported vector databases and get answers to your questions based on your specific data.</p>

<p>With this template, you can build, deploy, and use a plugin that lets ChatGPT search the contents of your documents, powered by a vector store of your choice. It provides examples of how to search and fetch documents from various vector stores, use OpenAI's <code>text-embedding-ada-002</code> model to generate embeddings via the OpenAI and LangChain libraries, store and process documents and file uploads in supported vector databases, convert text from various file formats into a common document format, chunk documents using simple whitespace or token-based methods, extract text from a variety of file formats, switch between various vector database providers, and use FastAPI to define API endpoints.</p>
<h2>Requirements</h2>

<p>Before you can run the ChatGPT retrieval plugin, make sure you have the following set up:</p>

<ul>
<li><strong>Python 3.10</strong> – The project is developed and tested against Python 3.10, so this is the recommended version to use.</li>
<li><strong>pip</strong> – Used to install the project's Python dependencies (they are defined in the project's dependency files, with exact versions pinned in the lock file).</li>
<li><strong>OpenAI API key</strong> – The plugin uses OpenAI's embedding models to generate embeddings for your documents and user queries, so a valid API key is required.</li>
<li><strong>A vector database provider</strong> – The plugin stores and searches document embeddings in a vector database. You will need an account and the corresponding API credentials for whichever supported provider you choose to work with.</li>
</ul>

<p>Core Python dependencies include the web framework (FastAPI, with Uvicorn as the server) and OpenAI's tooling for embeddings and tokenization. For example, the tokenization package pulls in the following pinned dependencies:</p>

<ul>
<li><code>blobfile &gt;= 2</code></li>
<li><code>regex &gt;= 2022.1.18</code></li>
<li><code>requests &gt;= 2.26.0</code></li>
</ul>

<p>Configuration values such as the OpenAI API key, the chosen vector database, and authentication tokens are provided via environment variables (typically in a <code>.env</code> file) rather than being hard-coded in the source.</p>
<h2>Installation</h2>

<p>To get started with the ChatGPT Retrieval Plugin, follow the steps below to set up your development environment.</p>

<h3>Prerequisites</h3>

<ul>
<li><strong>Python 3.10</strong> — this project uses Python 3.10, which is required to run the code. If you don't have it installed already, you can download it from the official Python website or use a package manager like pyenv.</li>
</ul>

<h3>Setting Up the Environment</h3>

<ol>
<li>Create a new Python environment and activate it:</li>
</ol>

<p><code>shell
python -m venv venv
source venv/bin/activate
</code></p>

<ol start="2">
<li>Navigate to the project directory:</li>
</ol>

<p><code>shell
cd /path/to/chatgpt-retrieval-plugin
</code></p>

<ol start="3">
<li>Install the required dependencies using the <code>requirements.txt</code> file:</li>
</ol>

<p><code>shell
pip install -r requirements.txt
</code></p>

<ol start="4">
<li>Set up your environment variables by creating a <code>.env</code> file in the root directory of the project, and fill in the required values:</li>
</ol>

<p><code>shell
DATASTORE=&lt;your-datastore-choice&gt;
BEARER_TOKEN=&lt;your-secret-key-for-authentication&gt;
OPENAI_API_KEY=&lt;your-openai-api-key-here&gt;
</code></p>

<ul>
<li><code>DATASTORE</code> should be set to the vector database you want to use to store and retrieve documents.</li>
<li><code>BEARER_TOKEN</code> is the secret key used for authentication when making requests to the API.</li>
<li><code>OPENAI_API_KEY</code> is your OpenAI API key, used for generating document embeddings.</li>
</ul>

<p>Once you have completed these steps, your development environment is set up and ready to use.</p>
<h2>Usage</h2>

<p>Once the environment variables are configured (e.g. <code>DATASTORE</code>, <code>BEARER_TOKEN</code>, <code>OPENAI_API_KEY</code>, plus any credentials required by your chosen vector database), you can interact with the retrieval plugin either by calling its API directly or by using the helper scripts included in the repository.</p>

<h3>Running the API locally</h3>

<p>Navigate to the <code>app</code> directory and start the API with:</p>

<p><code>shell
uvicorn main:app --reload --port 8000
</code></p>

<p>The service will be available at <code>http://localhost:8000</code>. Every request must include an <code>Authorization</code> header with a bearer token that matches the <code>BEARER_TOKEN</code> environment variable you configured.</p>

<h3>API Endpoints</h3>

<p>The plugin exposes the following endpoints for interacting with the vector database:</p>

<p>| Endpoint | Method | Description |
| --- | --- | --- |
| <code>/upsert</code> | <code>POST</code> | Upserts a batch of documents into the vector database |
| <code>/upsert-file</code> | <code>POST</code> | Upserts a single file (PDF, TXT, DOCX, PPTX, or CSV) into the vector database |
| <code>/query</code> | <code>POST</code> | Queries the vector database using one or more natural language queries and optional metadata filters |
| <code>/docs</code> | <code>GET</code> | Returns a list of all document IDs in the vector database, with optional pagination |
| <code>/docs</code> | <code>DELETE</code> | Deletes all documents in the vector database, or specific documents by ID |</p>

<h3>Example Requests</h3>

<p>Upserting documents:</p>

<p><code>shell
curl -X POST http://localhost:8000/upsert \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "id": "doc-1",
        "text": "This is the text content of the document.",
        "metadata": {
          "source": "example",
          "source_id": "example-1",
          "url": "https://example.com",
          "created_at": "2023-01-01",
          "author": "Example Author",
          "title": "Example Document"
        }
      }
    ]
  }'
</code></p>

<p>Uploading a file directly:</p>

<p><code>shell
curl -X POST http://localhost:8000/upsert-file \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -F "file=@/path/to/file.pdf"
</code></p>

<p>Querying the datastore:</p>

<p><code>shell
curl -X POST http://localhost:8000/query \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      {
        "query": "What is the content about?",
        "filter": { "source": "example" },
        "top_k": 3
      }
    ]
  }'
</code></p>

<p>Listing and deleting documents:</p>

<p>```shell
curl "http://localhost:8000/docs?limit=10&amp;offset=0" \
  -H "Authorization: Bearer $BEARER_TOKEN"</p>

<p>curl -X DELETE "http://localhost:8000/docs?ids=doc-1&amp;ids=doc-2" \
  -H "Authorization: Bearer $BEARER_TOKEN"
```</p>

<p>Calling <code>DELETE /docs</code> without an <code>ids</code> parameter removes all documents from the datastore.</p>

<h3>Example Scripts</h3>

<p>The repository includes scripts to help you process and load data into your configured datastore:</p>

<ul>
<li><code>scripts/process_json.py</code> — takes a JSON file with training data and converts it into JSONL files containing chunks of at most a specified maximum length.</li>
<li><code>scripts/upsert.py</code> — reads the JSONL files produced by <code>process_json.py</code> and upserts them into the datastore.</li>
</ul>

<p>Example usage:</p>

<p><code>shell
python scripts/process_json.py path/to/input.json path/to/output_dir 200
python scripts/upsert.py path/to/output_dir
</code></p>

<h3>Using the Plugin with ChatGPT</h3>

<p>To use the plugin with ChatGPT:</p>

<ol>
<li>Run the API locally, or deploy it to a publicly accessible URL.</li>
<li>In the ChatGPT UI, select <code>Plugins</code> from the model dropdown (this requires a ChatGPT Plus subscription).</li>
<li>Open the <code>Plugin store</code>, then select <code>Develop your own plugin</code>.</li>
<li>Enter the domain of your plugin (e.g. <code>localhost:8000</code> if running locally, or your deployed URL) and select <code>Find plugin</code>.</li>
<li>Select <code>Install plugin</code>, then start asking questions about the documents stored in your vector database.</li>
</ol>
<h2>Contributing</h2>

<p>We welcome contributions to the ChatGPT Retrieval Plugin! If you'd like to contribute, please follow these steps:</p>

<ol>
<li>Fork the repository and create a new branch for your changes.</li>
<li>Make your changes, and ensure that the code is well-documented and tested.</li>
<li>Write clear and concise commit messages.</li>
<li>Submit a pull request with your changes, describing the purpose and scope of the changes.</li>
</ol>

<p>Before contributing, please review the project's code of conduct and make sure your actions comply with it.</p>

<p>We appreciate your efforts to improve the ChatGPT Retrieval Plugin, and we look forward to your contributions!</p>
<h2>License</h2>

<p>MIT License</p>
