# ChatPaper

ChatPaper is a collection of research-assistance tools for finding and reading academic papers, generating summaries and reviews, drafting responses to reviewer comments, and producing literature surveys. The repository contains several related but independently run components. The main command-line scripts are at the repository root; `auto_survey/`, `ChatReviewerAndResponse/`, and the deployment directories have their own setup notes and should be treated as separate projects.

ChatPaper uses OpenAI APIs for language-model tasks. Generated summaries, reviews, responses, and surveys are aids for research workflows, not substitutes for reading and verifying sources. The project documentation warns against using generated content in serious academic settings without careful human review and against unethical use.

## Features and repository layout

- **Paper reading:** `chat_paper.py` searches arXiv or processes local PDFs and generates paper summaries. `chat_arxiv.py` searches arXiv’s website for recent papers and summarizes downloaded PDFs.
- **Review assistance:** `chat_reviewer.py` and `chat_response.py` provide paper-review and reviewer-response workflows. Related scripts and input-format examples are in `ChatReviewerAndResponse/`.
- **Web and hosted interfaces:** `HuggingFaceDeploy/` contains Flask and Gradio applications. The Flask application exposes `/arxiv`, `/paper`, `/response`, and `/reviewer` endpoints.
- **Literature surveys:** `auto_survey/` searches for references and generates LaTeX and Markdown survey drafts. It includes a sample output and a default LaTeX template.
- **PDF parsing:** `scipdf_parser-master/` contains the SciPDF Parser, which is based on GROBID. Its own README describes how to start GROBID and use the parser.
- **Other materials:** `source/` contains Sphinx documentation; `docker/` contains Docker-related files.

The main repository documentation covers the paper-reading workflow in more detail in `source/tutorial/reading_papers.md` and `source/tutorial/reading_papers_zh.md`.

## Requirements

The getting-started documentation recommends Python 3.9 and lists Windows 10 or Ubuntu 20.04 LTS as recommended operating systems; other Python 3 versions and operating systems may work. Root dependencies are listed in `requirements.txt` and include packages for arXiv access, PDF handling, OpenAI API calls, Flask, Gradio, and documentation generation.

Some components have their own requirements files and may use different package versions. Install the requirements for the component you intend to run rather than assuming every component shares one environment.

## Setup

Clone the repository and install the root requirements:

```bash
git clone https://github.com/kaixindelele/ChatPaper.git
cd ChatPaper
pip install -r requirements.txt
```

The root scripts that call OpenAI expect API configuration in `apikey.ini`. The paper-reading documentation shows an `[OpenAI]` section with an `OPENAI_API_KEYS` value, for example:

```ini
[OpenAI]
OPENAI_API_KEYS = [sk-your-key]
```

`apikey.ini` is not included in the supplied repository file tree. Create it locally and do not commit real credentials. Some scripts also read `OPENAI_API_BASE`; inspect the relevant script and configure that setting if needed. The arXiv workflow additionally accepts an `OPENAI_KEY` environment variable.

For `auto_survey`, change into its directory and install its own dependencies:

```bash
cd auto_survey
pip install -r requirements.txt
```

Set `OPENAI_API_KEY` in the environment before running the survey generator. This component’s README specifically instructs users to work from `auto_survey/`, because it is independent of the root project and relies on paths relative to that directory.

## Usage

### Summarize papers

The main paper-reading script supports arXiv searches and local PDFs. Examples from the project documentation:

```bash
python chat_paper.py --query "chatgpt robot" \
  --filter_keys "chatgpt robot" --language "en" --max_results 3

python chat_paper.py --pdf_path "demo.pdf"
python chat_paper.py --pdf_path "/path/to/paper_folder"
```

The documented options include `--pdf_path`, `--query`, `--key_word`, `--language`, `--file_format`, `--save_image`, `--sort`, `--max_results`, and `--filter_keys`. A query may use arXiv field prefixes such as `ti:` (title), `au:` (author), `abs:` (abstract), or `all:` (all fields). `--filter_keys` filters papers by terms that must appear in the abstract. The documentation describes Markdown and plain-text output and Chinese and English summary languages. Downloaded PDFs and summaries are documented as being written under `pdf_files/` and `export/`.

For a recent-paper search using `chat_arxiv.py`:

```bash
python chat_arxiv.py --query "chatgpt robot" \
  --page_num 2 --max_results 3 --days 10
```

This script searches arXiv’s web pages, filters results by age, downloads PDFs, and summarizes them. Its command-line defaults and available options are defined in the script. The documentation notes that hyphens in search terms may not be recognized as expected.

### Generate a literature survey

From `auto_survey/`, edit the target title in `main.py`, then run:

```bash
python main.py
```

The generator creates a timestamped directory under `auto_survey/outputs/`. The documented outputs include Markdown files and LaTeX source; compile `main.tex` in a LaTeX-capable environment to produce a PDF.

### Run the Flask deployment

The Flask entry point shown in the repository is `HuggingFaceDeploy/app.py`, not a root-level `app.py`. It defines GET routes for `/arxiv`, `/paper`, `/response`, and `/reviewer`, and displays example links at `/` and `/index`. Its route parameters and defaults are visible in that file. The deployment README describes hosted Hugging Face usage, while noting that the current version is essentially a Python application and that Hugging Face may not be necessary.

The Gradio applications in `HuggingFaceDeploy/Private/` and `HuggingFaceDeploy/Public/` provide PDF-upload interfaces. The public version asks users for API keys and model parameters; the private version reads API keys from `apikey.ini`. Follow the README in the relevant deployment directory before exposing either application.

## Configuration and operational notes

- Keep API keys private. Do not place credentials in public source code, public Spaces, or committed configuration files.
- For proxy-related connection problems, the troubleshooting documentation suggests setting `http_proxy` and `https_proxy` in the environment or in the relevant script.
- The paper-reading tools depend on external services, including OpenAI and arXiv. API availability, rate limits, network access, and model responses can affect results.
- PDF section extraction depends on detectable headings and document structure; check summaries against the original paper.
- If using image-upload options, review the relevant script’s Gitee configuration requirements before enabling them.

## Development and documentation

The top-level components are not a single packaged application. The README files under `auto_survey/`, `ChatReviewerAndResponse/`, `HuggingFaceDeploy/`, and `docker/` provide component-specific guidance. In particular, the ChatReviewerAndResponse README says to open that folder independently to avoid path problems.

Documentation is built with Sphinx from `source/`, with configuration in `source/conf.py`. The repository’s Read the Docs configuration uses Python 3.9 and installs the root `requirements.txt`. A local Sphinx build can be run from the repository root with:

```bash
sphinx-build -b html source build/html
```

The Docker materials describe more than one setup. The root `Dockerfile` builds a Python 3.9 environment with GROBID, while `docker/Dockerfile` uses Conda and starts a uWSGI application. The `docker/README.md` cautions that the Docker directory may not work because paths were changed and recommends command-line use instead. Treat these configurations as optional and potentially outdated.

## Testing

No automated test suite or test command is present in the supplied file tree. After changing code, verify the affected workflow manually: install the relevant component’s dependencies, configure its required API credentials, and try it with a small arXiv query or a known local PDF. For documentation changes, build the Sphinx site and check for build errors.

## License

The root `LICENSE.md` states that the work is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)** license. The `auto_survey/README.md` separately declares MIT for that component, and `scipdf_parser-master/` includes its own license file. Check the license associated with each component and its dependencies before reuse or redistribution.
