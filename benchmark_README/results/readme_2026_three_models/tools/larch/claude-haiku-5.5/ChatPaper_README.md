# ChatPaper

ChatPaper is a toolkit for reading, summarizing, reviewing, translating, and chatting about academic papers with large language models (LLMs) such as ChatGPT. It fetches papers from arXiv and Google Scholar, parses their PDFs and LaTeX sources, and produces structured summaries, peer-review-style critiques, and translations. It also includes a knowledge-base layer for question answering over a document collection and a web interface for interactive use.

> **Note:** This README was written from the repository's file listing and common project conventions, not from a full code audit. Check each script's `--help` output and the source code for exact arguments and behavior.

---

## Table of Contents

- [Features](#features)
- [Repository Structure](#repository-structure)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Summarizing arXiv Papers](#summarizing-arxiv-papers)
  - [Summarizing a Local PDF](#summarizing-a-local-pdf)
  - [Reviewing a Paper](#reviewing-a-paper)
  - [Translating a Paper](#translating-a-paper)
  - [Chatting with a Paper](#chatting-with-a-paper)
  - [Google Scholar Search](#google-scholar-search)
  - [Knowledge Base Question Answering](#knowledge-base-question-answering)
  - [Web Application](#web-application)
  - [Jupyter Notebook](#jupyter-notebook)
- [PDF Parsing with GROBID and pdffigures2](#pdf-parsing-with-grobid-and-pdffigures2)
- [Docker Deployment](#docker-deployment)
- [Output Files](#output-files)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **arXiv paper retrieval and summarization.** Search arXiv by keyword, filter results, download PDFs or LaTeX sources, and generate a structured summary for each paper.
- **Local PDF summarization.** Summarize any PDF you provide.
- **Automated paper review.** Generate a critical review with strengths, weaknesses, and suggestions, following the format in `ReviewFormat.txt`.
- **Translation.** Translate papers or summaries into Chinese or other target languages while preserving formulas and structure.
- **Paper chat.** Ask follow-up questions about a specific paper in an interactive session.
- **Google Scholar spider.** Collect paper metadata and links from Google Scholar searches.
- **Knowledge base QA.** Build a FAISS vector index over a set of papers and answer questions with retrieved context.
- **Figure and reference extraction.** Extract figures with pdffigures2 and bibliographic references with GROBID.
- **LaTeX processing.** Clean and process LaTeX sources, handle math macros, and reuse templates.
- **Web interface.** Use a Flask/Gradio-style web app for browser-based interaction.
- **Containerized deployment.** Run the full stack with Docker and docker-compose.
- **Bilingual documentation.** Getting-started and reading guides are available in English and Chinese.

---

## Repository Structure

The layout below is inferred from the file listing. Directory groupings are approximate.

```
ChatPaper/
├── chat_paper.py          # Main entry point: summarize arXiv papers
├── chat_arxiv.py          # arXiv search and chat-based summarization
├── chat_arxiv_maomao.py   # Alternative arXiv workflow
├── chat_reviewer.py       # Automated paper review
├── chat_translate.py      # Paper translation
├── chat_response.py       # Response generation for paper discussion
├── get_paper.py           # Paper download and retrieval
├── parse_pdf.py           # PDF parsing (GROBID and pdffigures2)
├── text_utils.py          # Text cleaning and helper functions
├── google_scholar_spider.py  # Google Scholar crawler
├── gpt_interaction.py     # LLM API wrapper
├── prompts.py             # Prompt templates
├── file_operations.py     # File I/O utilities
├── tex_processing.py      # LaTeX source processing
├── figures.py             # Figure extraction
├── references.py          # Reference extraction and processing
├── embeddings.py          # Embedding generation
├── storage.py             # Storage for vector indexes and metadata
├── knowledge.py           # Knowledge base QA logic
├── main.py                # Additional entry point
├── app.py                 # Web application
├── optimizeOpenAI.py      # OpenAI API optimizations (retries, batching)
├── pdffigures2-assembly-0.0.12-SNAPSHOT.jar  # Figure extraction tool
├── serve_grobid.sh        # Starts a GROBID server
├── ReviewFormat.txt       # Output template for reviews
├── review_comments.txt    # Example review comments
├── ref.bib, related works.tex, template.tex, main.tex, math_commands.tex
├── demo.pdf
├── generation.log
├── survey.md, survey_chinese.md
├── machine_learning.csv   # Sample paper list
├── ChatPaper.ipynb        # Jupyter notebook demo
├── tsinghua.condarc       # Conda mirror configuration
├── conda_env.yml          # Conda environment
├── requirements.txt       # Python dependencies (several copies exist in subfolders)
├── setup.py               # Package installation
├── Dockerfile, docker-compose.yaml, build.sh, dev.sh, tagpush.sh, start.sh
├── Makefile, make.bat     # Documentation build helpers
├── docs/                  # Sphinx documentation (conf.py, index.rst, *.md guides)
├── troubleshooting.md, troubleshooting_zh.md
├── reading_papers.md, reading_papers_zh.md
├── getting_started.md, getting_started_zh.md
├── project_analysis.md
├── index.pkl, index.faiss, text_embedding_pairs.pickle, db_meta.json  # Sample knowledge base
├── Reinforcement Learning for Robot Control.zip  # Sample paper bundle
├── reviews.jpg, ChatPaper.png, ChatPaper-zh.png, and other images
└── LICENSE.md / LICENSE.txt
```

Several subfolders (for example, the web app and the LaTeX-based pipeline) contain their own `README.md`, `app.py`, `optimizeOpenAI.py`, and `requirements.txt`. Use the requirements file that matches the component you are running.

---

## Architecture Overview

```
           ┌──────────────┐
           │ arXiv / GS   │  get_paper.py, google_scholar_spider.py
           └──────┬───────┘
                  │ PDF / LaTeX source
           ┌──────▼───────┐
           │   Parsing    │  parse_pdf.py, tex_processing.py,
           │              │  figures.py, references.py
           └──────┬───────┘
                  │ text, figures, references
           ┌──────▼───────┐
           │  LLM layer   │  gpt_interaction.py, prompts.py,
           │              │  optimizeOpenAI.py
           └──────┬───────┘
                  │
     ┌────────────┼─────────────┬──────────────┐
     ▼            ▼             ▼              ▼
 Summaries    Reviews      Translations   Chat / QA
 chat_paper   chat_reviewer chat_translate knowledge.py
                                          storage.py, embeddings.py
                  │
           ┌──────▼───────┐
           │  Interfaces  │  app.py (web), ChatPaper.ipynb, CLI
           └──────────────┘
```

---

## Prerequisites

- **Python 3.8 or later** (3.9+ recommended)
- **An OpenAI API key** or a compatible endpoint
- **Java 8 or later** (required by `pdffigures2-assembly-*.jar`)
- **GROBID** (optional but recommended for reference extraction; runs via Docker or from source)
- **Conda** (optional, for the provided `conda_env.yml`)
- **Docker and docker-compose** (optional, for containerized deployment)
- A working internet connection for arXiv, Google Scholar, and LLM API access

---

## Installation

### Option 1: pip

```bash
git clone https://github.com/kaixindelele/ChatPaper.git
cd ChatPaper

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

To install as a package:

```bash
pip install -e .
```

### Option 2: Conda

```bash
conda env create -f conda_env.yml
conda activate chatpaper
pip install -r requirements.txt
```

If you are in mainland China, `tsinghua.condarc` provides a Tsinghua mirror configuration:

```bash
conda config --file tsinghua.condarc
```

### Verify Java (for pdffigures2)

```bash
java -version
```

---

## Configuration

### API key

Set your OpenAI key as an environment variable:

```bash
export OPENAI_API_KEY="sk-..."           # Linux/macOS
set OPENAI_API_KEY=sk-...                # Windows CMD
$env:OPENAI_API_KEY="sk-..."             # Windows PowerShell
```

If you use a proxy or an OpenAI-compatible endpoint, set the base URL variable documented in `gpt_interaction.py` (commonly `OPENAI_API_BASE` or `OPENAI_BASE_URL`, depending on your client version).

Do not commit API keys to version control. Add your `.env` file to `.gitignore`.

### Proxy settings

If you need a proxy to reach arXiv or the LLM API:

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

### GROBID

Start a GROBID server with the provided script:

```bash
bash serve_grobid.sh
```

By default it listens on port 8070. Point the parser at it if you use a different port.

---

## Usage

Run `python <script>.py --help` to see the current list of options. The examples below follow the conventions of the project; confirm the exact flag names in the source.

### Summarizing arXiv Papers

Search arXiv by keyword and summarize the results:

```bash
python chat_paper.py \
  --key_word "reinforcement learning" \
  --query "robot control" \
  --filter_keywords "robot" \
  --max_results 3 \
  --language zh \
  --file_format txt
```

Typical parameters:

| Parameter | Description |
|---|---|
| `--key_word` | Category or topic used for the arXiv search |
| `--query` | Query string to match in titles and abstracts |
| `--filter_keywords` | Keywords a paper must contain to be kept |
| `--max_results` | Maximum number of papers to process |
| `--language` | Output language, for example `en` or `zh` |
| `--file_format` | Output format, for example `txt` or `md` |

Each run writes a summary for every paper that passes the filters.

### Summarizing a Local PDF

Summarize a PDF on disk (for example, the included `demo.pdf`):

```bash
python chat_paper.py --pdf_path demo.pdf --language en
```

Or use the arXiv chat workflow:

```bash
python chat_arxiv.py --query "diffusion models" --max_results 2
```

### Reviewing a Paper

Generate a structured review:

```bash
python chat_reviewer.py --paper_path demo.pdf --language en
```

Reviews follow the template in `ReviewFormat.txt`. `review_comments.txt` contains example output you can use as a reference.

### Translating a Paper

```bash
python chat_translate.py --pdf_path demo.pdf --target_language zh
```

Translation keeps LaTeX math and section structure where possible. Check the output for formula rendering errors.

### Chatting with a Paper

`chat_response.py` supports interactive question answering about a single paper. Start a session and type questions at the prompt:

```bash
python chat_response.py --pdf_path demo.pdf
```

Example session:

```
> What problem does this paper solve?
> Which baselines are compared in Table 2?
> Summarize the limitations in three sentences.
```

### Google Scholar Search

```bash
python google_scholar_spider.py --query "large language models" --max_results 20
```

Google Scholar rate-limits automated access. Use modest request volumes and add delays if you see blocking.

### Knowledge Base Question Answering

`knowledge.py`, `embeddings.py`, and `storage.py` build a vector index over a collection of papers:

1. Parse and chunk the documents.
2. Generate embeddings and store them in a FAISS index (`index.faiss`) with metadata (`index.pkl`, `db_meta.json`) and embedding pairs (`text_embedding_pairs.pickle`).
3. At query time, retrieve the most similar chunks and pass them to the LLM as context.

The repository includes a sample index. To query it, run the knowledge-base script with a question:

```bash
python knowledge.py --query "What are the main challenges in robot control?"
```

To rebuild the index from your own papers, place the PDFs in the input directory and run the indexing step described in the script's help text.

### Web Application

The web interface is in `app.py`. The repository contains more than one copy of `app.py` (for example, in a subfolder with its own `optimizeOpenAI.py`). Run the one that matches your use case:

```bash
python app.py
```

Then open the address printed in the console, typically `http://127.0.0.1:7860` for Gradio or `http://127.0.0.1:5000` for Flask.

### Jupyter Notebook

`ChatPaper.ipynb` walks through the main workflow interactively:

```bash
jupyter notebook ChatPaper.ipynb
```

---

## PDF Parsing with GROBID and pdffigures2

ChatPaper uses two external tools for structured PDF parsing:

- **GROBID** extracts the header, abstract, sections, and bibliography. Start it with `serve_grobid.sh` or run it in Docker:

  ```bash
  docker run --rm -p 8070:8070 lfoppiano/grobid:0.8.0
  ```

- **pdffigures2** extracts figures and captions using the bundled jar:

  ```bash
  java -jar pdffigures2-assembly-0.0.12-SNAPSHOT.jar input.pdf -d output_dir -i 150
  ```

  Adjust `-i` (image DPI) and `-d` (output directory) as needed.

If GROBID is unavailable, the parser falls back to plain-text extraction. Expect lower quality for references and section boundaries.

---

## Docker Deployment

### Build and run with docker-compose

```bash
cp .env.example .env          # if provided; otherwise create .env manually
# Add OPENAI_API_KEY=... to .env

docker-compose up --build
```

The `docker-compose.yaml` file starts the ChatPaper service and, depending on configuration, a GROBID container.

### Build the image manually

```bash
bash build.sh
# or
docker build -t chatpaper:latest .
```

### Development helper

```bash
bash dev.sh
```

### Tag and push

```bash
bash tagpush.sh <version>
```

Check `build.sh`, `dev.sh`, and `tagpush.sh` before running them, since they may reference registry names or tags specific to the original maintainers.

---

## Output Files

| File or directory | Contents |
|---|---|
| Summary files (`.txt` or `.md`) | Structured summaries of each paper |
| Review files | Strengths, weaknesses, and suggestions |
| Translation files | Translated text with preserved structure |
| `index.faiss`, `index.pkl` | Vector index and metadata for knowledge-base QA |
| `text_embedding_pairs.pickle` | Cached text and embedding pairs |
| `db_meta.json` | Index metadata |
| `generation.log` | Log of a generation run |
| `survey.md`, `survey_chinese.md` | Example survey outputs |

---

## Documentation

- `getting_started.md` / `getting_started_zh.md`: installation and first steps
- `reading_papers.md` / `reading_papers_zh.md`: guidance on using summaries for reading
- `troubleshooting.md` / `troubleshooting_zh.md`: common errors and fixes
- `project_analysis.md`: design notes
- `docs/`: Sphinx documentation

To build the Sphinx docs:

```bash
cd docs
make html           # Linux/macOS
make.bat html       # Windows
```

The built HTML is written to `docs/_build/html`.

---

## Troubleshooting

**`openai.error.AuthenticationError` or 401 responses**
Check that `OPENAI_API_KEY` is set in the current shell and that the key is valid.

**Timeouts or connection errors to arXiv or the LLM API**
Configure a proxy (see [Configuration](#configuration)) or retry later. `optimizeOpenAI.py` includes retry logic for transient failures.

**`java: command not found` or pdffigures2 failures**
Install Java 8 or later and confirm `java -version` works.

**GROBID connection refused**
Make sure the GROBID server is running on the expected port (default `8070`) and that the parser points to the same host and port.

**Garbled Chinese output or encoding errors**
Use UTF-8 for input and output files. On Windows, set `PYTHONUTF8=1` or open files with `encoding="utf-8"`.

**Formulas broken in translated output**
Translation of LaTeX math is imperfect. Compare against the original source and use `math_commands.tex` to define any custom macros the parser does not recognize.

**Google Scholar returns no results or blocks requests**
Reduce request frequency, add delays between queries, or use a different search source.

**Knowledge base returns irrelevant answers**
Rebuild the index with better chunking, or increase the number of retrieved chunks. Check that the embedding model matches the one used to build the index.

For more, see `troubleshooting.md` and `troubleshooting_zh.md`.

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make your changes and test them on a few sample papers, including `demo.pdf`.
4. Commit with a clear message and open a pull request describing the change and how you tested it.

Please keep API keys, personal paper collections, and large generated artifacts out of commits.

---

## License

This project is distributed under the license in `LICENSE.md` (and `LICENSE.txt`). Read it before using or redistributing the code. Papers you process remain subject to their original licenses and copyright terms.

---

## Acknowledgments

- [arXiv](https://arxiv.org) for open access to research papers
- [GROBID](https://github.com/kermitt2/grobid) for scholarly PDF parsing
- [pdffigures2](https://github.com/allenai/pdffigures2) for figure extraction
- [FAISS](https://github.com/facebookresearch/faiss) for vector search
- OpenAI and the broader LLM community
