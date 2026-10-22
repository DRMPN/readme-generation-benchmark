# ChatPaper

Use ChatGPT to read, summarize, review, and respond to academic papers. ChatPaper is a full-workflow research assistant built on the OpenAI API: it searches arXiv, parses local PDFs, generates structured paper summaries, drafts reviewer-style comments, writes responses to review comments, and can even auto-generate literature-survey drafts in LaTeX and Markdown.

> **Ethics notice (from the project documentation):** ChatPaper does not support unethical use. It is intended for quick pre-reading screening only — not for serious academic scenarios such as formal peer review. Review-response features embed deliberate text-injection safeguards to discourage misuse.

## Key Features

- **`chat_paper.py`** – The main CLI script. Batch-search arXiv, download papers, parse PDFs, and generate structured summaries (title, authors, affiliation, keywords, links, background, methods, conclusions, and an innovation/performance/workload assessment). Also summarizes local PDFs (single file or a folder).
- **`chat_arxiv.py`** – A web-based arXiv search variant that scrapes the arXiv search pages, filters by recent submission days, downloads PDFs, and produces the same GPT summaries.
- **`ChatReviewerAndResponse/`** – `chat_reviewer.py` generates reviewer-style comments for a local PDF (two-stage: section selection, then review), and `chat_response.py` auto-genders responses to review comments stored in a text file.
- **`chat_translate.py`** – Translation utility script.
- **`others/google_scholar_spider.py`** – Crawls Google Scholar for a keyword and exports results (title, authors, citations) to CSV, optionally with plots.
- **`auto_survey/`** – “文献调研神器” (survey generator): given a paper title, it searches real references on arXiv, optionally mines a FAISS knowledge database, and produces a compiled-ready LaTeX "related works" section plus Markdown (English and Chinese) versions, packaged as a zip.
- **Web deployments** – A Flask service wrapping the four main scripts, Gradio apps for Hugging Face Spaces (public and private variants), and Docker images.

## Project Structure

```
├── chat_paper.py / chat_arxiv.py / chat_translate.py   # CLI entry points
├── ChatReviewerAndResponse/    # reviewer + review-response generators
├── HuggingFaceDeploy/          # Flask app.py + Public/Private Gradio Spaces
├── docker/                     # conda-based Dockerfile, docker-compose, scripts
├── Dockerfile                  # GROBID-based image (root)
├── auto_survey/                # literature survey generator
├── scipdf_parser-master/       # bundled third-party GROBID PDF parser (MIT)
├── others/                     # notebook, Google Scholar spider, "maomao" variant
├── source/                     # Sphinx documentation (EN/ZH tutorials)
├── demo.pdf                    # sample paper for local testing
├── requirements.txt / start.sh / apikey.ini (user-created)
```

## Requirements

- **Python 3.9** (other Python 3 versions generally work; Python 3.9.16 is used in the Docker image).
- OS: Windows 10 or Ubuntu 20.04 LTS recommended; macOS also works.
- An OpenAI API key. The default model is `gpt-3.5-turbo` (Hugging Face app also offers `gpt-3.5-turbo-0301`; `auto_survey` uses `gpt-3.5-turbo-16k`).

## Installation

```bash
git clone https://github.com/kaixindelele/ChatPaper
cd ChatPaper
pip install -r requirements.txt
```

Key dependencies include `arxiv`, `PyMuPDF (fitz)`, `openai`, `tiktoken`, `tenacity`, `flask`, `flask-cors`, `gradio`, `Pillow`, `beautifulsoup4`, and `markdown`.

`auto_survey/` and `ChatReviewerAndResponse/` are independent projects: open those folders directly as your working directory, then run `pip install -r requirements.txt` inside them. The bundled `scipdf_parser-master` can be installed with `python setup.py install` if you want GROBID-based scientific PDF parsing (run `bash serve_grobid.sh` first; it starts GROBID on port 8070).

## Configuration

Create/edit `apikey.ini` in the project root (the key stays on your local machine):

```ini
[OpenAI]
OPENAI_API_KEYS = [sk-1234567890abcdefg]   # list your key(s), line 3
OPENAI_API_BASE = https://api.openai.com/v1

[Gitee]
api = ...        # optional; only needed for --save_image uploads
owner = ...
repo = ...
path = ...
```

- Multiple keys can be comma-separated in `OPENAI_API_KEYS`; the scripts rotate between them.
- The Docker deployment instead reads the `OPENAI_KEY` environment variable (set in `docker-compose.yaml`).
- For auto-survey, set the `OPENAI_API_KEY` environment variable (and optionally `openai.proxy` for VPNs).

## Usage

### Command line

```bash
# arXiv search + download + summarize
python chat_paper.py --query "chatgpt robot" --filter_keys "chatgpt robot" --language "en" --max_results 3

# Advanced queries
python chat_paper.py --query "all: reinforcement learning robot 2023" --filter_keys "reinforcement robot" --max_results 3
python chat_paper.py --query "au: Sergey Levine" --filter_keys "reinforcement robot" --max_results 3

# Local PDF (single or folder)
python chat_paper.py --pdf_path "demo.pdf"
python chat_paper.py --pdf_path "absolute_path_to_paper_folder"

# Newer arXiv web search with page/day filtering
python chat_arxiv.py --query "chatgpt robot" --page_num 2 --max_results 3 --days 10
```

Supported `chat_paper.py` flags: `--pdf_path`, `--query`, `--key_word`, `--language` (`zh` default / `en`), `--file_format` (`md` default / `txt`), `--save_image`, `--sort` (`Relevance` default / `LastUpdatedDate`), `--max_results` (default 1), `--filter_keys`. Query prefixes follow arXiv semantics:

| Prefix | Field |
| --- | --- |
| `ti` / `au` / `abs` | Title / Author / Abstract |
| `co` / `jr` / `cat` | Comment / Journal ref / Category |
| `rn` / `id` / `all` | Report number / ID / All fields |

Notes: search terms recognize spaces but not hyphens; local summarization currently supports non-survey papers.

### Flask web service

```bash
pip install virtualenv && virtualenv venv
source venv/bin/activate      # or .\venv\Scripts\activate.bat on Windows
python app.py
```

Visit `http://127.0.0.1:5000/` (or `/index`). Four GET endpoints wrap the CLI scripts with the same parameters: `/arxiv`, `/paper` (local PDF), `/response` (`comment_path`, `language`), and `/reviewer` (`paper_path`, `research_fields`, `language`). Results are saved to `export/`, `pdf_files/`, and `response_file/`. The reference implementation is `HuggingFaceDeploy/app.py`.

### Docker

Edit `docker-compose.yaml` (line 21) to set `- OPENAI_KEY=sk-...`, then:

```bash
docker-compose up -d
```

The service listens on `https://127.0.0.1:28460/`. Results persist in Docker volumes: `chatpaper_log`, `chatpaper_export`, `chatpaper_pdf_files`, `chatpaper_response_file`. The conda-based image (`docker/Dockerfile`) serves a uWSGI app on port 8088 with `NUM_PROCESS`, `NUM_THREAD`, and `TIME_OUT` env knobs. The root `Dockerfile` builds on `lfoppiano/grobid:0.7.1`, installs Python 3.9 from source, installs all requirements plus scipdf_parser, and runs `start.sh`. **Caveat (from `docker/README.md`):** the docker folder's paths have changed and may not work; command-line usage is recommended.

### Hugging Face Spaces

Duplicate the [ChatPaper Space](https://huggingface.co/spaces/wangrongsheng/ChatPaper) as **Private** (keys in `apikey.ini` on the server side) or **Public** (users paste comma-separated API keys in the web UI, with a built-in key-validation tab). The public UI accepts API keys, section-title keywords, model choice, top-p/temperature sliders, and a PDF upload, returning an HTML summary plus a JSON token/cost report. A hosted demo is available at chatwithpaper.org.

### Auto survey (auto_survey/)

```bash
cd auto_survey
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...      # and optionally openai.proxy
# edit target title in main.py, then:
python main.py
```

Outputs land in `outputs/<timestamp>/`: `main.tex` (+ `ref.bib`, `math_commands.tex`, `related works.tex`) compilable to PDF, `survey.md`, `survey_chinese.md`, `generation.log`, and a zip archive.

### Google Scholar

```bash
python google_scholar_spider.py --kw "deep learning" --nresults 30 --csvpath "./data" --sortby "cit/year" --plotresults 1
```

## Documentation

Sphinx documentation lives in `source/` (bilingual getting-started, paper-reading, and troubleshooting guides) and is hosted on Read the Docs via `.readthedocs.yaml` (Python 3.9, HTML + PDF output). Build locally with `sphinx-build -M html source build` (doc requirements: `sphinx-book-theme`, `recommonmark`, `sphinx-markdown-tables`, `sphinxemoji`).

## Testing

The repository ships no automated test suite. Verify your installation manually:

```bash
python chat_paper.py --pdf_path demo.pdf        # end-to-end local summarization
python chat_paper.py --query "chatgpt robot" --filter_keys "chatgpt robot" --max_results 1
```

Check that `pdf_files/` and `export/` are populated. The Hugging Face app's API-key validation tab doubles as a connectivity check. `auto_survey` results can be validated by compiling `main.tex` to PDF.

## Troubleshooting

- **Proxy:** set `os.environ["http_proxy"]` / `https_proxy` in `chat_paper.py`, or use `pip install -r requirements.txt --proxy ...` / `-i https://pypi.tuna.tsinghua.edu.cn/simple`.
- **`openai.error.RateLimitError ... access was terminated`**: your key was revoked; register a new key and replace it in `apikey.ini`/`chat_paper.py`.

## License

The main project is released under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)** license (see `LICENSE.md`). Third-party components carry their own licenses: `scipdf_parser-master` is MIT-licensed by Titipat Achakulvisut, and `auto_survey`'s README metadata declares MIT.

## Acknowledgments

ChatPaper builds on [auto-draft](https://github.com/CCCBora/auto-draft) (survey generation), [scipdf_parser](https://github.com/titipata/scipdf_parser) (GROBID/pdffigures2 parsing), and [google_scholar_spider](https://github.com/JessyTsu1/google_scholar_spider). If you find the project useful, please star the repo — a donation QR code is included in `images/`.
