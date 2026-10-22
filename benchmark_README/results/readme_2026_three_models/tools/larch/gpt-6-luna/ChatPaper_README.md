# ChatPaper

ChatPaper is a collection of tools for using large language models to assist with academic-paper workflows. It includes scripts and applications for obtaining and parsing papers, generating summaries and reviews, translating content, and exploring related work. The repository also contains PDF-processing utilities, a retrieval-based knowledge component, web interfaces, and documentation.

The project contains several implementations and frontends. Their options and setup requirements may differ; use the README or help output in the directory for the particular tool you plan to run.

## Features

Depending on the selected component, ChatPaper can help with:

- **Paper retrieval and reading:** work with papers obtained from sources such as arXiv or supplied as PDFs.
- **PDF and LaTeX processing:** extract text and figures, and process LaTeX source files.
- **Summarization and Q&A:** generate explanations or responses about paper content.
- **Review assistance:** draft review comments and structured paper reviews.
- **Translation:** translate paper content or generated responses.
- **Related-work discovery:** search or generate related-work material.
- **Retrieval and knowledge storage:** create or use a local index of paper content.
- **Web-based interaction:** run one of the included application frontends.

LLM-generated summaries, translations, and reviews are suggestions, not substitutes for reading the original paper or applying expert judgment.

## Repository overview

The repository includes several related tools and supporting assets:

| Files or directories | Purpose |
|---|---|
| `chat_paper.py`, `chat_arxiv.py`, `chat_arxiv_maomao.py` | Paper-reading and arXiv-oriented scripts |
| `chat_reviewer.py`, `chat_translate.py`, `chat_response.py` | Review, translation, and response-related workflows |
| `get_paper.py`, `parse_pdf.py` | Paper retrieval and PDF-processing utilities |
| `figures.py`, `text_utils.py`, `tex_processing.py` | Figure, text, and LaTeX processing |
| `knowledge.py`, `embeddings.py`, `storage.py`, `references.py` | Knowledge indexing, embeddings, storage, and reference handling |
| `index.faiss`, `index.pkl`, `text_embedding_pairs.pickle`, `db_meta.json` | Example or generated retrieval-index data |
| `main.py`, `app.py` | Application entry points; check the containing directory for the intended frontend |
| `Dockerfile`, `docker-compose.yaml`, `start.sh`, `build.sh` | Container and startup support |
| `serve_grobid.sh` | Helper for running a GROBID service |
| `pdffigures2-assembly-0.0.12-SNAPSHOT.jar` | PDF figure-extraction dependency |
| `README.md`, `getting_started.md`, `troubleshooting.md`, and translated documentation | Additional guides |
| `demo.pdf`, `*.tex`, `*.bib`, `*.md`, and image files | Examples, templates, and project documentation |

Some filenames occur more than once in the repository listing, which suggests that the project contains multiple subprojects or copied application directories. Run installation and startup commands from the directory containing the relevant `requirements.txt` and entry point.

## Requirements

Requirements depend on the component you use. In general, you may need:

- Python and the packages listed in that component’s `requirements.txt`.
- An API key for the language-model provider configured by the selected implementation.
- Java if you use the bundled `pdffigures2` JAR.
- GROBID if you use workflows that rely on its service.
- LaTeX tools if you need to compile generated or supplied `.tex` files.
- Docker and Docker Compose if you prefer the container setup.

Check the relevant subproject’s documentation and dependency file before installing optional services.

## Installation

### 1. Get the project

Clone the repository, or change into the directory where you have placed it:

```bash
git clone <repository-url>
cd ChatPaper-ge0fy5iu
```

If you received the project as an archive, extract it and open a terminal in the extracted directory.

### 2. Create a Python environment

For example, using `venv`:

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the requirements for the component you intend to use. For a root-level requirements file:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the application you want to run has its own `requirements.txt`, install that file instead (or as additionally instructed by its local documentation).

### 4. Configure model access

Many workflows require access to a language-model API. Provide the credentials using the mechanism expected by the selected implementation. A common environment-variable setup is:

```bash
# macOS / Linux
export OPENAI_API_KEY="your-api-key"

# Windows PowerShell
$env:OPENAI_API_KEY = "your-api-key"
```

Some components may use a different provider, configuration file, or variable name. Check that component’s code and documentation before running it. Do not commit API keys, tokens, or other credentials to the repository.

## Running the tools

The repository has multiple entry points rather than one guaranteed universal command. First navigate to the directory containing the script or application you want to use.

If the script supports command-line help, inspect its options before running it:

```bash
python chat_paper.py --help
python chat_arxiv.py --help
```

The available arguments depend on the implementation. The main scripts and their apparent roles include:

- `chat_paper.py` — paper-reading workflow.
- `chat_arxiv.py` and `chat_arxiv_maomao.py` — arXiv-oriented workflows.
- `chat_reviewer.py` — review assistance.
- `chat_translate.py` — translation.
- `get_paper.py` and `parse_pdf.py` — paper retrieval and PDF parsing.

If a script does not provide `--help`, consult its source, configuration, and the nearby documentation for required inputs and settings.

### Web applications

The repository contains `app.py` files and other frontend-related assets. To run a web application, use the instructions in the directory containing the desired `app.py`. A typical Python application may be started with:

```bash
python app.py
```

This is not guaranteed to be the correct command for every `app.py` in this repository; some may require a framework-specific command, configuration, or a different working directory. Check the local README and dependencies first.

### Docker

The repository includes Docker-related files. From the directory containing the relevant `docker-compose.yaml`, you can try:

```bash
docker compose up --build
```

Some setups also provide helper scripts such as `build.sh`, `start.sh`, or `dev.sh`. Review those scripts before running them, especially if they require API credentials or mount local files.

## Working with PDFs, figures, and LaTeX

PDF extraction and figure processing may require additional tools beyond the Python packages:

- `pdffigures2-assembly-0.0.12-SNAPSHOT.jar` is included for figure-related processing. Java must be installed to run it.
- `serve_grobid.sh` can be used with workflows that depend on GROBID; follow the script and related documentation to configure the service.
- LaTeX-related files such as `template.tex`, `math_commands.tex`, and `related works.tex` may be templates or generated output. Compiling them requires a suitable LaTeX distribution and any required bibliography or style files.

PDF parsing is imperfect. Scanned PDFs, unusual layouts, equations, tables, and multi-column formatting can result in incomplete or incorrectly ordered text.

## Retrieval index and generated data

Files such as `index.faiss`, `index.pkl`, `text_embedding_pairs.pickle`, and `db_meta.json` are associated with local indexing or retrieval workflows. Their presence does not necessarily mean the index is current or suitable for every user.

- Follow the relevant component’s instructions to create or refresh an index.
- Keep generated indexes consistent with the documents and embedding configuration used to build them.
- Avoid sharing indexes that contain private or copyrighted source material unless you have permission.
- Back up any data you want to preserve before regenerating or deleting indexes.

## Troubleshooting

- **Missing package:** activate the intended environment and install dependencies from the `requirements.txt` beside the tool you are running.
- **API or authentication error:** confirm that the selected provider is configured correctly and that credentials are available to the process.
- **PDF or figure-processing error:** check that the input PDF is readable and install any required external tools, including Java when using the bundled JAR.
- **GROBID connection error:** confirm that the service is installed, running, and reachable at the address expected by the selected workflow.
- **Unexpected output or missing paper content:** try another PDF, inspect the extracted text, or use the paper’s LaTeX source if available.
- **Web app fails to start:** run it from the correct directory and install that app’s own dependencies. Check its local documentation for required environment variables and ports.
- **Container startup problems:** inspect the relevant Docker files and logs, and verify that required credentials and mounted paths are configured.

The repository includes additional troubleshooting documentation, including `troubleshooting.md` and `troubleshooting_zh.md`.

## Responsible use

- Verify factual claims, citations, equations, and references against the original paper.
- Do not submit confidential, unpublished, or otherwise sensitive manuscripts to an external model provider unless you are authorized to do so and understand that provider’s data policies.
- Review generated peer-review material carefully. The tool can assist with drafting but cannot replace qualified reviewers.
- Observe copyright and publisher restrictions when downloading, storing, or redistributing papers.
- API usage may incur charges. Review your provider’s pricing and usage limits.

## License

License files are included in the repository (`LICENSE.txt` and `LICENSE.md`). Check the applicable license before using, modifying, or redistributing the project. Third-party components, including the bundled PDF-figure tool, may have separate license terms.
