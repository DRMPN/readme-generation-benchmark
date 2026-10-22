# ChatPaper

ChatPaper is a collection of Python tools for reading, summarizing, and reviewing academic papers with the OpenAI Chat API. The repository includes command-line scripts, a Flask web wrapper, Gradio-based Hugging Face deployment variants, a literature survey generator (`auto_survey`), a GROBID-based PDF parser (`scipdf_parser-master`), Docker configurations, and Sphinx documentation sources.

## Overview

The main features described in the supplied files are:

- **Paper search and summarization:** `chat_paper.py` and `chat_arxiv.py` search arXiv, download matching PDFs, extract section text, and ask an OpenAI model to produce a structured summary, method description, and conclusion assessment.
- **Local PDF summarization:** `chat_paper.py` can summarize a local PDF file or a folder of PDFs through `--pdf_path`.
- **Review response and reviewer generation:** `ChatReviewerAndResponse/` contains `chat_response.py` and `chat_reviewer.py` for drafting responses to review comments and generating review comments for a paper.
- **Web interface:** `app.py` exposes the arXiv, paper, response, and reviewer features as Flask routes on port 5000.
- **Literature survey generation:** `auto_survey/main.py` produces LaTeX and Markdown related-work drafts with references.
- **PDF parsing:** `scipdf_parser-master/` provides a Python parser for scientific PDFs using GROBID.
- **Deployment variants:** `HuggingFaceDeploy/` contains Gradio applications for public and private Hugging Face Spaces, and Docker files package the project for containerized use.

The project also includes an `others/` directory with exploratory material, including a project analysis report, a Google Scholar spider, and a notebook. The repository's `LICENSE.md` covers the project as a whole, as described below.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `chat_paper.py` | Search arXiv or read local PDFs, then summarize papers |
| `chat_arxiv.py` | Search arXiv by query and date window, download PDFs, and summarize |
| `app.py` | Flask application with `/arxiv`, `/paper`, `/response`, and `/reviewer` routes |
| `requirements.txt` | Root Python dependencies |
| `start.sh` | Startup script referenced by the root `Dockerfile` |
| `Dockerfile` | Root container image built on `lfoppiano/grobid:0.7.1` |
| `docker/` | Alternative container setup using Miniconda, uWSGI, and Sphinx helper files |
| `ChatReviewerAndResponse/` | Review response and reviewer generation scripts |
| `HuggingFaceDeploy/` | Gradio applications for Hugging Face deployments |
| `auto_survey/` | Automatic survey/related-work generator |
| `scipdf_parser-master/` | GROBID-based scientific PDF parser |
| `source/` | Sphinx documentation sources (English and Chinese) |
| `images/` | Screenshots and images used in documentation |
| `others/` | Additional scripts, notes, and data |

## Setup

### Prerequisites

The getting-started documentation states that the project requires Python 3.9, and that other Python 3 versions should also work. The documentation recommends Windows 10 or Ubuntu 20.04 LTS.

### Installation

Clone the repository and install the root dependencies:

```bash
git clone https://github.com/kaixindelele/ChatPaper
cd ChatPaper
pip install -r requirements.txt
```

The root `requirements.txt` pins packages including `arxiv`, `PyMuPDF`, `openai`, `tiktoken`, `tenacity`, `flask`, `flask-cors`, `gradio`, and `markdown`.

### Working Directory

The `ChatReviewerAndResponse` and `auto_survey` README files both state that each subproject must be opened as its own folder. Opening the top-level `chatpaper` folder can cause incorrect relative paths in those subprojects.

## Configuration

### OpenAI API Keys

`chat_arxiv.py` and `chat_paper.py` read a file named `apikey.ini` from the working directory. The tutorial specifies that the key goes on line 3 in this form:

```ini
OPENAI_API_KEYS = [sk-1234567890abcdefg]
```

The scripts parse the `OpenAI` section, and `chat_arxiv.py` reads `OPENAI_API_BASE` from the same section. `chat_arxiv.py` also appends a key from the `OPENAI_KEY` environment variable to the key list, and ignores keys shorter than the minimum length used in the code.

The `HuggingFaceDeploy/Private/README.md` file describes the same `OPENAI_API_KEYS` setting and notes that multiple keys can be listed.

### Gitee Image Upload

When `--save_image` is enabled, the scripts read a `Gitee` section from `apikey.ini`. The code uses the keys `api`, `owner`, `repo`, and `path`. The `--save_image` option is described as slow, taking a minute or two per picture.

### auto_survey

The `auto_survey/README.md` says to set the `OPENAI_API_KEY` environment variable. Its `main.py` also contains a placeholder assignment, `openai.api_key = "your key"`, in its `__main__` block, so the key must be supplied or the placeholder replaced.

### Proxy Settings

The troubleshooting guide describes setting `http_proxy` and `https_proxy` environment variables in `chat_paper.py` when working behind a proxy.

## Usage

### Command-Line Search and Summary

`chat_paper.py` accepts these arguments: `--pdf_path`, `--query`, `--key_word`, `--language`, `--file_format`, `--save_image`, `--sort`, `--max_results`, and `--filter_keys`.

Examples from the documentation:

```bash
python chat_paper.py --query "chatgpt robot" --filter_keys "chatgpt robot" --language "en" --max_results 3
python chat_paper.py --query "all: reinforcement learning robot 2023" --filter_keys "reinforcement robot" --max_results 3
python chat_paper.py --query "au: Sergey Levine" --filter_keys "reinforcement robot" --max_results 3
python chat_paper.py --pdf_path "demo.pdf"
python chat_paper.py --pdf_path "absolute_path_to_paper_folder"
```

Searches use arXiv query prefixes: `ti` (title), `au` (author), `abs` (abstract), `co` (comment), `jr` (journal reference), `cat` (subject category), `rn` (report number), `id`, and `all`.

Downloaded PDFs are saved under `./pdf_files`, and summaries are written to `./export`. The documentation states that the script currently supports only non-survey papers.

### Date-Window Search

`chat_arxiv.py` accepts `--query`, `--key_word`, `--page_num`, `--max_results`, `--days`, `--sort`, `--save_image`, `--file_format`, and `--language`:

```bash
python chat_arxiv.py --query "chatgpt robot" --page_num 2 --max_results 3 --days 10
```

Its `--language` option defaults to `zh`, and `--file_format` defaults to `md`.

### Google Scholar

The tutorial describes a separate Google Scholar script:

```bash
python google_scholar_spider.py --kw "deep learning" --nresults 30 --csvpath "./data" --sortby "cit/year" --plotresults 1
```

The tutorial refers users to the upstream project at `https://github.com/JessyTsu1/google_scholar_spider` for details.

### Flask Web Service

Start the service with:

```bash
python app.py
```

The application listens on port 5000 at `http://127.0.0.1:5000/` or `http://127.0.0.1:5000/index`. It provides these routes:

- `/arxiv`: parameters `query`, `key_word`, `page_num`, `max_results`, `days`, `sort`, `save_image`, `file_format`, `language`
- `/paper`: parameters `pdf_path`, `query`, `key_word`, `filter_keys`, `max_results`, `sort`, `save_image`, `file_format`, `language`
- `/response`: parameters `comment_path`, `file_format`, `language`
- `/reviewer`: parameters `paper_path`, `file_format`, `research_fields`, `language`

Results are written to the `export`, `pdf_files`, and `response_file` folders in the working directory.

### Review Response and Reviewer Tools

The `ChatReviewerAndResponse` folder contains `chat_response.py`, `chat_reviewer.py`, `get_paper.py`, `ReviewFormat.txt`, and `review_comments.txt`. The Flask documentation describes `--comment_path` for response generation and `--paper_path` and `--research_fields` for reviewer generation.

### Literature Survey Generator

`auto_survey/main.py` defines a `generate_draft` function that collects references, builds a related-works section, and writes results to the `outputs` directory. Outputs for a sample run include `main.tex`, `related works.tex`, `ref.bib`, `survey.md`, `survey_chinese.md`, and `generation.log`, plus a zipped archive. The `__main__` block uses the target title `Reinforcement Learning for Robot Control`, the knowledge database `ml_textbook_test`, and the model `gpt-3.5-turbo-16k`. The README says users edit `main.py` to customize the title and then run `python main.py`.

### Docker

The root `Dockerfile` starts from `lfoppiano/grobid:0.7.1`, installs Python 3.9.16 from source, clones the ChatPaper repository into `/app`, installs requirements, installs `scipdf_parser-master`, and runs `/start.sh` as the command.

The `docker/Dockerfile` uses `continuumio/miniconda3`, creates a conda environment from `docker/conda_env.yml`, sets `NUM_PROCESS=2`, `NUM_THREAD=2`, and `TIME_OUT=1800`, and runs uWSGI on port 8088 with the entry point `app:app`.

The Docker tutorial describes `docker-compose up -d`, with an API key entered in the compose file as `OPENAI_KEY`. The tutorial refers to `https://127.0.0.1:28460/`, and to Docker volumes named `chatpaper_log`, `chatpaper_export`, `chatpaper_pdf_files`, and `chatpaper_response_file`.

Note that `docker/README.md` states that paths in that folder have been modified and the setup may not work as-is, and recommends running the single Python file directly.

### Hugging Face

`HuggingFaceDeploy/app.py` is a Flask version that imports `chat_arxiv`, `chat_paper`, `chat_response`, and `chat_reviewer`. The `HuggingFaceDeploy/Public` and `HuggingFaceDeploy/Private` folders contain Gradio applications that import `optimizeOpenAI.chatPaper`. The private README describes duplicating a Space with visibility set to Private and listing API keys in `apikey.ini`.

### PDF Parser (scipdf)

The `scipdf_parser-master/README.md` describes installation with:

```bash
pip install git+https://github.com/titipata/scipdf_parser
python -m spacy download en_core_web_sm
bash serve_grobid.sh
```

The GROBID service runs on default port 8070. Example usage:

```python
import scipdf
article_dict = scipdf.parse_pdf_to_dict('example_data/futoma2017improved.pdf')
```

The `parse_figures` function uses the pdffigures2 JAR bundled in the package.

## Development

- **Source documentation:** Sphinx sources live in `source/`, with English and Chinese tutorials, a troubleshooting guide, and `conf.py`. `index.rst` links to these pages.
- **Documentation build:** `.readthedocs.yaml` specifies Ubuntu 22.04, Python 3.9, `source/conf.py` as the Sphinx configuration, PDF output, and `requirements.txt` for documentation dependencies. `docker/Makefile` provides a Sphinx `Makefile` with `SOURCEDIR = source` and `BUILDDIR = build`.
- **Helper scripts:** The docs refer to `build.sh`, `dev.sh`, and `tagpush.sh` in the `docker/` directory. Their contents are not included in the supplied files, so their behavior is not documented here.
- **Contributions:** The `others/chat_arxiv_maomao.py` file contains a note inviting pull requests to improve its persona-style prompts.

## Testing

The supplied files do not include a test suite, test configuration, or CI workflow. No testing commands are documented beyond the manual usage examples above. The `auto_survey` and `ChatReviewerAndResponse` READMEs describe running scripts directly rather than running tests.

## Known Limitations

- Several documentation files describe behavior that the current code may not fully match. For example, the Chinese reading tutorial refers to a `--research_field` option for the reviewer, while the Flask page documents `research_fields`.
- The Docker documentation refers to `docker-compose.yml`, while the supplied file is `docker/docker-compose.yaml`.
- The `docker/README.md` warns that paths have changed and the Docker setup may not work.
- The `auto_survey` script depends on an OpenAI key and a placeholder in `main.py`.
- The project documentation includes a warning that ChatPaper should be used responsibly and not for unethical academic purposes. The documentation states that review-reply features include text injection intended to discourage misuse.

## License

The root `LICENSE.md` contains a Creative Commons notice: the work is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License** (CC BY-NC-ND 4.0). The file links to `http://creativecommons.org/licenses/by-nc-nd/4.0/`.

The vendored `scipdf_parser-master` package has its own `LICENSE.txt`. Its `setup.py` identifies the license as the MIT License, copyright Titipat Achakulvisut, 2019.
