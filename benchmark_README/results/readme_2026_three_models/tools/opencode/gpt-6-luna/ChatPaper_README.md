# ChatPaper

ChatPaper is a collection of Python tools for working with research papers. The main scripts can search arXiv, download papers, extract text from PDFs, and use an OpenAI-compatible Chat Completions API to produce paper summaries. Separate tools in the repository generate review-comment responses, draft paper reviews, translate papers, and create literature surveys.

The scripts are independent utilities rather than one unified application. In particular, `auto_survey/`, `ChatReviewerAndResponse/`, and the translation/parser workflow have their own requirements and setup. Generated text should be checked against the source papers and used responsibly; the project documentation warns against submitting generated review text as one's own peer-review work.

## Repository contents

| Path | Purpose |
| --- | --- |
| `chat_paper.py` | Summarize one local PDF or a directory of PDFs, or search and download papers from arXiv. |
| `chat_arxiv.py` | Search the arXiv website for recent papers matching a query, download selected PDFs, and summarize them. |
| `ChatReviewerAndResponse/` | Scripts for drafting a review of local PDFs and drafting point-by-point responses to review comments. |
| `chat_translate.py` | A translation workflow for a parsed PDF; it depends on SciPDF Parser and GROBID and currently contains example credentials/settings in the script. |
| `scipdf_parser-master/` | A vendored SciPDF Parser source tree used by the translation workflow. |
| `auto_survey/` | A separate literature-survey generator with its own dependencies and configuration. |
| `HuggingFaceDeploy/`, `docker/`, `Dockerfile` | Deployment-related code and configuration. The included deployment notes say some deployment files may no longer work as-is. |
| `source/` | Sphinx documentation, including tutorials and troubleshooting notes. |
| `others/` | Additional examples and utilities, including a Google Scholar spider and notebooks. |

## Main scripts: installation and configuration

The getting-started guide recommends Python 3.9 (other Python 3 versions may work) and documents Windows 10 and Ubuntu 20.04. From the repository root, install the main script dependencies:

```bash
python -m pip install -r requirements.txt
```

The main paper scripts read an `apikey.ini` file from the current working directory. This file is ignored by Git and is not included in the repository. Create it locally with an `[OpenAI]` section, for example:

```ini
[OpenAI]
OPENAI_API_BASE = https://api.openai.com/v1
OPENAI_API_KEYS = [sk-your-key]
CHATGPT_MODEL = gpt-3.5-turbo
```

Use your provider's actual API base, key, and supported model. `chat_paper.py` also reads an optional `OPENAI_KEY` environment variable. `chat_arxiv.py` reads its key list from `apikey.ini`. The scripts use the legacy `openai` Python client API pinned in `requirements.txt`; compatibility with newer client versions is not established here.

## Summarize papers with `chat_paper.py`

Set `--pdf_path` to an empty string to make the script search arXiv, filter results by words in their abstracts, download matching PDFs, and summarize them. For example:

```bash
python chat_paper.py --pdf_path "" \
  --query "all: reinforcement learning robot" \
  --filter_keys "reinforcement robot" \
  --max_results 3 --language en
```

The arXiv query accepts field prefixes such as `ti:` (title), `au:` (author), `abs:` (abstract), and `all:` (all fields). Every space-separated word in `--filter_keys` must occur in the abstract for a result to pass the filter. The script's default `--max_results` is `1`; its default query and filter are examples, not recommendations.

To summarize a local PDF, or PDFs found recursively in a directory, pass its path instead:

```bash
python chat_paper.py --pdf_path "demo.pdf"
python chat_paper.py --pdf_path "/path/to/papers"
```

Useful options include:

| Option | Description |
| --- | --- |
| `--pdf_path` | A PDF file or directory of PDFs. An empty string selects arXiv search instead. The default is `demo.pdf`. |
| `--query` | arXiv search expression used when `--pdf_path` is empty. |
| `--filter_keys` | Space-separated terms that must all appear in a result abstract. |
| `--max_results` | Maximum number of arXiv results to process. |
| `--sort` | `Relevance` or `LastUpdatedDate` in the script. |
| `--key_word` | Research field supplied to the summary prompts. |
| `--language` | `zh` (default) or `en`. |
| `--file_format` | Output extension; defaults to `md` (the script writes generated text). |

Downloaded PDFs are written under `pdf_files/`; summaries are written under `export/`. These directories are created at runtime and are ignored by Git.

## Search recent arXiv papers with `chat_arxiv.py`

This script scrapes arXiv search-result pages, keeps entries within a recent-day window, downloads up to the requested number, and summarizes them:

```bash
python chat_arxiv.py --query "traffic flow prediction" \
  --page_num 2 --max_results 3 --days 10 --language en
```

`--page_num` controls the number of result pages inspected (the code requests pages of 50 entries), `--days` sets the date window, and `--max_results` caps the number of papers processed. PDFs and summaries are saved under `pdf_files/` and `export/`. The script's defaults are defined in `chat_arxiv.py`; use `python chat_arxiv.py --help` to see them.

## Reviews and responses

These tools are separate from the root scripts. Their configuration and input paths are relative to the current working directory. The included review format is `ChatReviewerAndResponse/ReviewFormat.txt`; run the commands from that directory and provide an `apikey.ini` there.

Draft a review from one PDF or a directory of PDFs:

```bash
cd ChatReviewerAndResponse
python chat_reviewer.py --paper_path "/path/to/paper.pdf" \
  --research_fields "computer science" --language en
```

Draft point-by-point responses from a text file of reviewer comments:

```bash
python chat_response.py --comment_path review_comments.txt --language en
```

Both scripts support `--language en` or `--language zh` and a `--file_format` extension. Reviews are written under `ChatReviewerAndResponse/output_file/`; responses are written under `ChatReviewerAndResponse/response_file/`. The review script inserts generated-text notices and an ethics statement in its output. Treat its result as a draft for human evaluation, not as a substitute for independent peer review.

## Literature surveys

`auto_survey/` is an independent tool with a separate, larger dependency set. Its README instructs users to install that directory's requirements, set the `OPENAI_API_KEY` environment variable, edit `main.py` to set the survey title, and run:

```bash
cd auto_survey
python -m pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
python main.py
```

The README says results are placed in a timestamped directory under `auto_survey/outputs/`; it describes Markdown and LaTeX survey outputs. On Windows, set the environment variable using the shell's normal syntax instead of `export`.

## Translation workflow

`chat_translate.py` parses a PDF with `scipdf` and sends sections to a Chat Completions API. Its current `__main__` block hard-codes `demo.pdf`, a placeholder key (`sk-xxx`), an API base, and a translation task, so configure these values before use. The parser requires GROBID to be running; see `scipdf_parser-master/README.md` and `scipdf_parser-master/serve_grobid.sh` for its setup. The root `requirements.txt` does not install all of this parser workflow's requirements.

## Additional documentation and notes

- The English and Chinese tutorials are in `source/tutorial/`; troubleshooting notes are in `source/troubleshooting/`.
- `others/google_scholar_spider.py` is an additional utility and has its own command-line options; it is not part of the `chat_paper.py` workflow.
- Deployment artifacts are included for reference, but the repository's `docker/README.md` cautions that its Docker setup may not work after path changes. The Hugging Face deployment notes likewise describe a separate deployment copy.
- PDF text extraction and section detection depend on PDF structure. Review generated summaries and extracted content for omissions or errors.

## License

`LICENSE.md` identifies the repository license as Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0). See that file for the license text and link.
