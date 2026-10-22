# ChatPaper

ChatPaper is a set of Python scripts that use the OpenAI Chat Completions API to help with reading and reviewing academic papers. The main workflow searches arXiv, downloads matching PDFs, extracts their text, and writes a structured summary in Markdown or plain text. The project's documentation is primarily in Chinese, with English versions of the main tutorials under `source/tutorial/`.

Other scripts in this repository translate papers, draft responses to reviewer comments, generate reviewer-style feedback, and draft literature surveys.

## Features

- **Paper summaries from arXiv** (`chat_paper.py`): searches arXiv with the `arxiv` package, downloads PDFs, and filters results so that every filter keyword appears in the abstract. For each paper it writes a summary covering title, authors, affiliation, keywords, links, background, prior methods, the proposed method, and results. It then summarizes the method section and the conclusion, with a critique of significance, strengths, and weaknesses.
- **Paper summaries from arXiv search pages** (`chat_arxiv.py`): scrapes arXiv search result pages, keeps papers submitted within the last `--days` days, downloads the PDFs, and writes summaries in the same general format.
- **Local PDF summaries**: `chat_paper.py --pdf_path` summarizes one PDF or every PDF in a folder.
- **PDF translation** (`chat_translate.py`): parses a PDF with a [GROBID](https://github.com/kermitt2/grobid) server through the bundled `scipdf` parser and translates the title, abstract, and sections into Chinese with OpenAI, writing a Markdown file.
- **Review response drafting** (`ChatReviewerAndResponse/chat_response.py`): takes a text file of reviewer comments and drafts a point-by-point author response.
- **Reviewer-style review** (`ChatReviewerAndResponse/chat_reviewer.py`): generates a review of a local PDF, given the paper's research fields.
- **Literature survey drafting** (`auto_survey/`): collects references and writes a survey in LaTeX and Markdown from a title.
- **Web interface** (`HuggingFaceDeploy/`): a Flask app that exposes the arXiv, paper, response, and reviewer tools as HTTP GET endpoints.
- **Docker packaging**: a root `Dockerfile` and a `docker/` directory with a Compose file.

## Repository layout

| Path | Purpose |
| --- | --- |
| `chat_paper.py` | Main script: arXiv search or local PDFs, then OpenAI summaries. Writes to `export/`. |
| `chat_arxiv.py` | Alternative arXiv workflow that scrapes arXiv search pages by date window. |
| `chat_translate.py` | Translates one PDF to Chinese Markdown. Needs a GROBID server. |
| `start.sh` | Start script used by the root `Dockerfile`. Launches GROBID and then `chat_translate.py`. |
| `Dockerfile` | Builds an image from `lfoppiano/grobid` with Python 3.9. |
| `requirements.txt` | Python dependencies for the root scripts. |
| `ChatReviewerAndResponse/` | `chat_reviewer.py`, `chat_response.py`, and `get_paper.py`. Its README says to open this folder on its own. |
| `auto_survey/` | Literature survey generator (`main.py` and `utils/`). Its README says to open this folder on its own. |
| `HuggingFaceDeploy/` | Flask app and deployment variants (`Public/`, `Private/`) for Hugging Face Spaces. |
| `scipdf_parser-master/` | Bundled `scipdf` PDF-parsing library, its `setup.py`, and `serve_grobid.sh`. |
| `docker/` | Docker Compose file, build scripts, and a Conda environment file. |
| `source/` | Sphinx documentation sources, including tutorials and troubleshooting (English and Chinese). |
| `others/` | Miscellaneous scripts and notes, including a Google Scholar spider and a Jupyter notebook. |
| `images/`, `source/_static/` | Screenshots used in the documentation. |
| `demo.pdf` | Sample PDF used as the default input for `chat_paper.py`. |

## Requirements

- Python 3.9 is recommended. The documentation says Python 3.9 and other Python 3 versions "should also work". The Dockerfile uses Python 3.9.16.
- An OpenAI API key (or an Azure OpenAI deployment, see [Configuration](#configuration)).
- Java and a running GROBID server are required only for `chat_translate.py` and the `scipdf` parser. The GROBID setup script in `scipdf_parser-master/serve_grobid.sh` fetches GROBID 0.6.2 and runs it with Gradle. The `scipdf` default URL is `http://localhost:8070`.

The root `requirements.txt` pins older packages, including `PyMuPDF==1.22.3`, `openai==0.27.8`, `tiktoken==0.4.0`, `gradio==3.20.1`, and `flask==2.2.3`. Install into a clean virtual environment.

## Installation

```bash
git clone https://github.com/kaixindelele/ChatPaper
cd ChatPaper
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` does not list `scipdf`. `chat_translate.py` imports it, so install the bundled copy separately:

```bash
cd scipdf_parser-master
pip install -r requirements.txt
python setup.py install
cd ..
```

## Configuration

### OpenAI key and API settings

The scripts read `apikey.ini` from the current working directory. This file is listed in `.gitignore`, and it is not included in the repository, so create it yourself. Based on the keys the code reads, a minimal file looks like this:

```ini
[OpenAI]
OPENAI_API_BASE = https://api.openai.com/v1
OPENAI_API_KEYS = [sk-your-key-here]
CHATGPT_MODEL = gpt-3.5-turbo
```

Notes on how the values are used:

- `OPENAI_API_KEYS` is a bracketed, comma-separated list. The code strips the first and last characters and splits on commas, so keep the brackets. Keys shorter than about 20 characters are ignored.
- The `OPENAI_KEY` environment variable is also read and added to the key list.
- `chat_paper.py` uses `CHATGPT_MODEL`. `chat_arxiv.py`, `chat_response.py`, and `chat_reviewer.py` hard-code `gpt-3.5-turbo` in their API calls.
- If no OpenAI key is found in `[OpenAI]` or `OPENAI_KEY`, `chat_paper.py` falls back to an `[AzureOPenAI]` section with `OPENAI_API_KEYS`, `CHATGPT_MODEL`, `OPENAI_API_BASE`, and `OPENAI_API_VERSION`.
- The `[Gitee]` section (`api`, `owner`, `repo`, `path`) is read only when `--save_image` is set. See [Known limitations](#known-limitations).

Keep your key private. The tutorial notes that the key stays on your machine, and `apikey.ini` is listed in `.gitignore` so it is not committed.

### Chinese and English output

`--language zh` (the default in `chat_paper.py` and `chat_arxiv.py`) writes Chinese output. `--language en` writes English. Other values fall back to Chinese.

## Usage

Run commands from the repository root, since `apikey.ini` and the `pdf_files/` and `export/` output folders are resolved relative to the working directory.

### Summarize arXiv papers with `chat_paper.py`

```bash
python chat_paper.py --query "chatgpt robot" --filter_keys "chatgpt robot" --language "en" --max_results 3
```

Arguments:

| Argument | Default | Description |
| --- | --- | --- |
| `--query` | `all: ChatGPT robot` | arXiv search string. Use prefixes such as `ti:`, `au:`, and `all:`. Hyphens are not handled well by the search. |
| `--filter_keys` | `ChatGPT robot` | Space-separated keywords. A paper is kept only if every keyword appears in its abstract (case-insensitive). |
| `--key_word` | `reinforcement learning` | Research field, used in the prompt given to the model. |
| `--max_results` | `1` | Maximum number of papers to download and summarize. |
| `--sort` | `Relevance` | `Relevance` or `LastUpdatedDate`. |
| `--pdf_path` | `demo.pdf` | Local PDF file or folder. When set, arXiv search is skipped. |
| `--file_format` | `md` | Output extension, `md` or `txt`. |
| `--language` | `zh` | `zh` or `en`. |
| `--save_image` | `False` | See [Known limitations](#known-limitations). |

Downloaded PDFs are saved under `pdf_files/`, and summaries are written to `export/`.

Examples:

```bash
# Summarize the default local sample
python chat_paper.py

# Summarize a local PDF
python chat_paper.py --pdf_path "demo.pdf"

# Summarize every PDF in a folder
python chat_paper.py --pdf_path "/absolute/path/to/paper_folder"

# Search by author, then filter by keywords
python chat_paper.py --query "au: Sergey Levine" --filter_keys "reinforcement robot" --max_results 3
```

The documentation says `chat_paper.py` supports only non-survey papers.

### Summarize recent arXiv papers with `chat_arxiv.py`

```bash
python chat_arxiv.py --query "chatgpt robot" --page_num 2 --max_results 3 --days 10
```

This script fetches arXiv search result pages (50 results per page), keeps papers whose submission date is within `--days` days, and summarizes up to `--max_results` of them. Its defaults are `--query "traffic flow prediction"`, `--key_word "GPT robot"`, `--page_num 2`, `--max_results 3`, and `--days 10`. Output goes to `export/`.

### Translate a PDF with `chat_translate.py`

`chat_translate.py` has no command-line arguments. Its `__main__` block sets the input, the output directory, the API base URL, and the key. The key defaults to the placeholder `"sk-xxx"`, so edit the file before running. It then:

1. Parses the PDF with `scipdf`, which requires a GROBID server at `http://localhost:8070`.
2. Asks the model to identify the paper's domain from its title and abstract.
3. Translates the title, abstract, and each section into Chinese, writing a Markdown file named after the PDF in the current directory.

This script does not read `apikey.ini`.

### Review response and reviewer tools

These tools live in `ChatReviewerAndResponse/`. Their README says to open that folder as its own project, because the scripts read `apikey.ini` and write output relative to the current directory. Run them from inside that folder.

```bash
cd ChatReviewerAndResponse
python chat_response.py --comment_path review_comments.txt --language en --file_format txt
python chat_reviewer.py --paper_path /path/to/paper.pdf --research_fields "computer science" --language en
```

- `chat_response.py` reads a text file of reviewer comments. It writes a point-by-point reply to `response_file/`, in the format "Concern #N / Author response".
- `chat_reviewer.py` reads one PDF and writes a reviewer-style review. Defaults are `--file_format txt` and `--language en`.

The repository includes `ChatReviewerAndResponse/review_comments.txt` as sample input. The documentation notes that these features include text injection to discourage misuse (see [Responsible use](#responsible-use)).

### Literature survey drafts with `auto_survey/`

`auto_survey/` has its own README, which says to open that folder as its own project. Its `main.py` builds a survey draft from a title and writes the results to `outputs/` as LaTeX, Markdown, and a zip archive.

- The README says to set `OPENAI_API_KEY` as an environment variable. The current `main.py` sets `openai.api_key = "your key"` in its `__main__` block, so you must edit that line.
- Edit `target_title` in `main.py` and run `python main.py`.
- Install dependencies from `auto_survey/requirements.txt`. The code imports `langchain`, `scholarly`, `bibtexparser`, `gradio_client`, `boto3`, and `matplotlib`.
- The repository includes a sample output in `auto_survey/outputs/outputs_20230707_202302/`.

### Web interface (Flask)

The `HuggingFaceDeploy/` folder contains `app.py` for a Flask service on port 5000. It exposes four GET endpoints: `/arxiv`, `/paper`, `/response`, and `/reviewer`. Their parameters correspond to the matching command-line scripts. The home page (`/` or `/index`) lists example links.

`HuggingFaceDeploy/app.py` imports `chat_arxiv`, `chat_paper`, `chat_response`, and `chat_reviewer`. Those modules are not in `HuggingFaceDeploy/`, so the app needs them copied or placed on the Python path before it will start. The `Public/` and `Private/` subfolders contain their own `app.py` files, and the `Private/` version includes the Gitee image-upload path.

The `source/tutorial/reading_papers.md` tutorial says to run `python app.py` from the repository root. There is no `app.py` at the root in this copy, so use the file under `HuggingFaceDeploy/`.

### Docker

The root `Dockerfile` builds an image from `lfoppiano/grobid:0.7.1`, installs Python 3.9.16, and clones the upstream repository from GitHub into `/app`. It then installs the dependencies and runs `/start.sh` as the container command. Build it from the repository root:

```bash
docker build -t chatpaper .
```

The `docker/docker-compose.yaml` file runs a prebuilt image, `panda1024/chatpaper:v1.0`, and maps host port `28460` to container port `8088`. It sets `OPENAI_KEY` in the environment, which you must replace:

```yaml
environment:
  - OPENAI_KEY=sk-your-key-here
```

```bash
cd docker
docker-compose up -d
```

The output folders are Docker volumes: `chatpaper_export`, `chatpaper_pdf_files`, `chatpaper_response_file`, and `chatpaper_log`.

The `docker/README.md` says the paths in that folder have been changed, so these files may not work without modification. It also recommends running the Python scripts directly. The `HuggingFaceDeploy/README.md` says the same about its single-file app.

## Output

- `chat_paper.py` and `chat_arxiv.py` write one file per run to `export/`, named by date and title (or query). Each paper gets a numbered section with the summary, the method summary, and the conclusion. The default is Markdown.
- `chat_translate.py` writes a Markdown file named after the input PDF, in the working directory.
- `chat_response.py` writes to `response_file/`. `chat_reviewer.py` writes its review in the same way.
- `auto_survey` writes to `outputs/<timestamp>/`, including `main.tex`, `survey.md`, `survey_chinese.md`, `ref.bib`, and a zip archive.

Model output is not checked against the source paper. Verify summaries and citations before relying on them.

## Known limitations

- **No `apikey.ini` in the repository.** You must create it (see [Configuration](#configuration)).
- **Section and title extraction is heuristic.** `chat_paper.py` finds the title from font size and matches section names such as "Abstract", "Introduction", and "Method". Papers with unusual layouts or section names may be parsed poorly. The code contains TODO comments noting this.
- **`--save_image` does not produce images in the root summary flow.** `chat_paper.py` and `chat_arxiv.py` define `get_image_path` and `upload_gitee`, but the summary flow does not call them. The option only reads the `[Gitee]` section. Only `HuggingFaceDeploy/Private/app.py` calls these functions.
- **Root `requirements.txt` does not include `scipdf`** (needed by `chat_translate.py`) or `langchain` and the other dependencies of `auto_survey/`.
- **`start.sh` assumes a working directory.** It runs `serve_grobid.sh` and `python chat_translate.py` relative to the current directory. In the root `Dockerfile`, the last `WORKDIR` is `/app/scipdf_parser-master`, while `chat_translate.py` is in `/app`. Adjust the paths before relying on the container to run translation. This was not tested.
- **`.gitmodules` refers to a `ChatPaper2Xmind` submodule** at `https://github.com/MasterYip/ChatPaper2Xmind.git`, but the `ChatPaper2Xmind/` directory is not present in this copy.
- **No automated tests** were found in the repository.
- **Pinned, old dependencies.** The `openai==0.27.8` package uses the legacy `openai.ChatCompletion` API. Newer OpenAI SDK versions do not support it.
- **API costs.** Every summary makes several Chat Completions calls. The scripts print token usage, but the repository does not estimate cost.

## Responsible use

The project's documentation states that ChatPaper should be used responsibly, in line with academic integrity. It says the review-related features include text injection intended to discourage misuse of generated reviews and replies (`source/index.rst`). Generated summaries, reviews, reply letters, and surveys are drafts. They must be checked by a human and must not be submitted as your own unedited work.

## Documentation

- `source/tutorial/getting_started.md` (English) and `getting_started_zh.md` (Chinese): prerequisites and installation.
- `source/tutorial/reading_papers.md` and `reading_papers_zh.md`: command-line usage, Flask, Docker, and Hugging Face.
- `source/troubleshooting/troubleshooting.md` and `troubleshooting_zh.md`: proxy settings and OpenAI API errors.

The Sphinx configuration is in `source/conf.py`, and `.readthedocs.yaml` is provided for Read the Docs.

## Acknowledgements

- `auto_survey/README.md` says the survey code is based mainly on [auto-draft](https://github.com/CCCBora/auto-draft).
- The bundled `scipdf_parser-master/` is a copy of the `scipdf` parser, which uses GROBID and `pdffigures2`.
- The Google Scholar spider in `others/` is referenced in the tutorial as [google_scholar_spider](https://github.com/JessyTsu1/google_scholar_spider).

## License

The root `LICENSE.md` is a Creative Commons license, **CC BY-NC-ND 4.0** (Attribution-NonCommercial-NoDerivatives 4.0 International). It permits sharing with attribution, but not commercial use and not distribution of modified versions. The license text is in Chinese at `LICENSE.md`.

`auto_survey/README.md` has a front-matter field that says `license: mit`. This conflicts with the root license. Check with the repository owner before relying on either license for a specific use.
