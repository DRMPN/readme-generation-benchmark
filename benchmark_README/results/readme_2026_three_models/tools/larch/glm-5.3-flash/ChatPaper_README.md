# ChatPaper 📚🤖

**Use GPT to summarize, review, and chat with arXiv papers — fully automated paper reading.**

ChatPaper is an all-in-one tool that fetches the latest papers from arXiv (or your local PDFs), sends them to GPT, and produces high-quality summaries, reviews, and answers to your questions. It also includes a powerful paper-survey tool that can generate a full related-works section in LaTeX from a corpus of papers.

---

## 📖 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
  - [Command Line (chat_arxiv.py)](#1-command-line---chat_arxivpy)
  - [Paper Downloader (get_paper.py)](#2-paper-downloader---get_paperpy)
  - [Paper Reviewer (chat_reviewer.py)](#3-paper-reviewer---chat_reviewerpy)
  - [Chat with a Paper (chat_response.py)](#4-chat-with-a-paper---chat_responsepy)
  - [Paper Survey Generator (main.py)](#5-paper-survey-generator---mainpy)
  - [Web App (app.py)](#6-web-app---apppy)
  - [Google Scholar Spider](#7-google-scholar-spider---google_scholar_spiderpy)
- [Configuration](#-configuration)
- [Docker](#-docker)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## ✨ Features

| Feature | Script | Description |
|---|---|---|
| **Paper summarization** | `chat_arxiv.py` | Monitor arXiv keywords, fetch new papers, and generate GPT summaries (core contribution, strengths/weaknesses, suggested experiments). |
| **Paper review** | `chat_reviewer.py` | Generate a full referee-style review (summary, strengths, weaknesses, rating) — great for self-checking your manuscript before submission. |
| **Interactive Q&A** | `chat_response.py` | Ask follow-up questions about a paper and get answers grounded in its content. |
| **Paper download** | `get_paper.py` | Download papers from arXiv/other sources and parse them to text (PDF parsing via [GROBID](https://github.com/kermitt2/grobid) and pdffigures2). |
| **Survey generation** | `main.py` | Build a FAISS vector index of a paper corpus and generate a full related-works LaTeX document (with BibTeX citations). |
| **Web interface** | `app.py` | Gradio/Flask web UI for all of the above. |
| **Scholar crawling** | `google_scholar_spider.py` | Crawl Google Scholar results for a keyword and rank authors/citations. |
| **Translation** | `chat_translate.py` | Translate papers/reviews into Chinese. |

---

## 🗂 Project Structure

```
ChatPaper/
├── chat_arxiv.py            # Main CLI: fetch + summarize arXiv papers
├── chat_reviewer.py         # Generate referee reports
├── chat_response.py         # Chat with a paper
├── chat_translate.py        # Translation helper
├── get_paper.py             # Download & parse papers (GROBID, pdffigures2)
├── parse_pdf.py             # PDF parsing utilities
├── serve_grobid.sh          # Start local GROBID server
├── google_scholar_spider.py # Google Scholar crawler
├── app.py                   # Web app (Gradio / Flask)
├── optimizeOpenAI.py        # Token-efficient GPT prompt helpers
│
├── survey/                  # Survey generation module
│   ├── main.py              # Entry point for survey generation
│   ├── embeddings.py        # Vector embeddings (FAISS)
│   ├── knowledge.py         # Knowledge base management
│   ├── gpt_interaction.py   # GPT prompting loops
│   ├── tex_processing.py    # LaTeX processing
│   ├── references.py        # Reference / BibTeX handling
│   ├── figures.py           # Figure extraction
│   ├── storage.py, file_operations.py, text_utils.py
│   └── prompts.py           # Prompt templates
│
├── template.tex, main.tex   # LaTeX survey templates
├── ReviewFormat.txt         # Review output format spec
├── Dockerfile, docker-compose.yaml, Makefile
├── requirements.txt
└── docs/                    # Getting started, reading guides, troubleshooting
```

---

## 🔧 Installation

```bash
git clone https://github.com/kaixindelele/ChatPaper.git
cd ChatPaper
pip install -r requirements.txt
```

> Requires Python ≥ 3.8. FAISS is needed for the survey tool:
> ```bash
> conda install -c pytorch faiss-cpu   # or pip install faiss-cpu
> ```

You'll need an **OpenAI API key**. Export it as an environment variable or pass it via CLI:

```bash
export OPENAI_API_KEY="sk-..."
```

---

## 🚀 Quick Start

### 1. Command Line — `chat_arxiv.py`

Fetch and summarize the latest arXiv papers for your keywords:

```bash
python chat_arxiv.py --query "reinforcement learning" \
                     --key "RL, robot" \
                     --max_key_word 5 \
                     --page_num 1 \
                     --filter "none" \
                     --openai_api_key sk-xxxx \
                     --output ./summary
```

Key arguments:

| Argument | Description |
|---|---|
| `--query` | arXiv search query (e.g. `"reinforcement learning"`) |
| `--key` | Keywords to filter/extract (comma-separated) |
| `--page_num` | Number of arXiv pages to crawl |
| `--filter` | Filter mode: `none` / `fuzzy` / `strict` |
| `--output` | Output directory for markdown summaries |
| `--file` | Summarize a **local PDF** instead of crawling arXiv |

Example — summarize a single local PDF:

```bash
python chat_arxiv.py --file demo.pdf --openai_api_key sk-xxxx
```

### 2. Paper Downloader — `get_paper.py`

```bash
python get_paper.py --arxiv_id 2303.08774   # download by arXiv ID
python get_paper.py --pdf_path ./papers     # parse local PDFs to text/figures
bash serve_grobid.sh                        # start GROBID server first (recommended)
```

### 3. Paper Reviewer — `chat_reviewer.py`

Generate a referee report for your own paper (or any PDF):

```bash
python chat_reviewer.py --pdf_path ./my_paper.pdf --openai_api_key sk-xxxx
```

Output follows the format defined in `ReviewFormat.txt`: paper summary, strengths, weaknesses, missing references, and an overall rating.

### 4. Chat with a Paper — `chat_response.py`

```bash
python chat_response.py --pdf_path demo.pdf --question "What is the main contribution?"
```

### 5. Survey Generator — `main.py`

Build a related-works section from a folder of papers:

```bash
cd survey
python main.py --pdf_folder ./papers --output related_works.tex
```

Pipeline: parse PDFs → embed chunks (OpenAI embeddings) → build FAISS index (`index.faiss` / `index.pkl`) → retrieve relevant passages per section → GPT writes LaTeX with `\cite{}` references → compile with `template.tex` / `main.tex`. A prebuilt example output is available in `survey.md` and `survey_chinese.md`.

### 6. Web App — `app.py`

```bash
python app.py
```

Open the browser UI (default `http://127.0.0.1:7860`) to paste an arXiv ID / upload a PDF and get summaries and reviews interactively. Screenshots: `flask_web_home.png`, `reviews.jpg`, `chatpaper.png`.

### 7. Google Scholar Spider — `google_scholar_spider.py`

```bash
python google_scholar_spider.py --kw "large language models" --nresults 20 --sortby cited
```

Outputs a CSV (e.g. `machine_learning.csv`) with authors, citations, and links.

---

## ⚙️ Configuration

- **API key**: set `OPENAI_API_KEY` env var or pass `--openai_api_key`.
- **GROBID**: run `bash serve_grobid.sh` to spin up the bundled GROBID jar (`pdffigures2-assembly-0.0.12-SNAPSHOT.jar` is used for figure extraction).
- **Prompts**: editable prompt templates live in `survey/prompts.py` and inside the chat scripts — customize the summary/review style to your taste.
- **Proxy**: set `https_proxy` / `http_proxy` if required in your region.

---

## 🐳 Docker

```bash
docker-compose up -d
# or
docker build -t chatpaper .
docker run -e OPENAI_API_KEY=sk-xxxx -p 7860:7860 chatpaper
```

Conda users can use `conda_env.yml`:

```bash
conda env create -f conda_env.yml
```

---

## 🛠 Troubleshooting

See [`docs/troubleshooting.md`](docs/troubleshooting.md) (中文版: `troubleshooting_zh.md`) and `project_analysis.md` for a walkthrough of the codebase. Common issues:

- **GROBID won't start** → ensure Java 8+ is installed: `java -version`.
- **Rate limit errors** → reduce batch size, or use `optimizeOpenAI.py` helpers to trim token usage.
- **FAISS install issues** → prefer `pip install faiss-cpu`.
- **Google Scholar blocking** → use a proxy or reduce crawl frequency.

---

## 📚 Documentation

- [`docs/getting_started.md`](docs/getting_started.md) — setup guide (中文: `getting_started_zh.md`)
- [`docs/reading_papers.md`](docs/reading_papers.md) — how to read papers with ChatPaper (中文: `reading_papers_zh.md`)
- [`docs/index.rst` / `conf.py`] — Sphinx documentation source (`make.bat` / `Makefile` to build)

---

## ⚠️ Disclaimer

Generated summaries and reviews are produced by GPT and may contain errors. Always verify claims against the original paper. Use responsibly and respect arXiv/Google Scholar rate limits.

## 📄 License

This project is released under the MIT License — see `LICENSE.md` / `LICENSE.txt`.
