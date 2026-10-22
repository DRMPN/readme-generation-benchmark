# ChatPaper-zny27arw

---

[![PyPi](https://badge.fury.io/py/scipdf.svg)](https://badge.fury.io/py/scipdf)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![arxiv](https://img.shields.io/badge/arXiv-B31B1B.svg?style={0}&logo=arXiv&logoColor=white)
![markdown](https://img.shields.io/badge/Markdown-000000.svg?style={0}&logo=Markdown&logoColor=white)
![openai](https://img.shields.io/badge/OpenAI-412991.svg?style={0}&logo=OpenAI&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style={0}&logo=pandas&logoColor=white)
![spacy](https://img.shields.io/badge/spaCy-09A3D5.svg?style={0}&logo=spaCy&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

ChatPaper is a Python toolkit that uses large language models (OpenAI GPT-3.5 via the ChatCompletion API) to help researchers and students process academic papers: it searches and summarizes arXiv papers, translates papers into Chinese, supports automated peer-review drafting and response generation, and can generate literature surveys. The project is aimed at researchers working with academic literature as well as developers who want to self-host the tooling. It provides several semi-independent surfaces, including command-line tools, a Jupyter notebook example, automated survey generation with retrieval and LaTeX output, and a web application deployable on Hugging Face Spaces or via Docker. Newcomers should start with the Getting Started section for setup and runnable steps, and consult the Documentation section for tutorials and per-component details.

---

## Core Features

- **ArXiv paper search and AI-powered summarization**: query arXiv with keyword, date, and sorting filters, then generate structured GPT-based summaries of downloaded papers to stay on top of relevant research faster.
- **PDF parsing and section extraction**: extract titles, section headings, text, and key figures from local PDFs so papers can be processed programmatically without manual reading.
- **Paper translation into Chinese**: translate paper titles and sections into idiomatic, colloquial Chinese with terminology preserved in English, making English-language papers accessible to Chinese readers.
- **Automated peer review and response generation**: use LLMs to draft review comments and responses, reducing the manual effort of the reviewing cycle.
- **Automated survey generation**: retrieve related work via embeddings-based search and render a complete survey with bibliography in Markdown and LaTeX formats.

---

## Installation

Install ChatPaper-zny27arw using one of the following methods:

**Using PyPi:**

```sh
pip install scipdf
```

---

## Getting Started

**Prerequisites**

- Python 3. The project tutorial (`source/tutorial/getting_started.md`) recommends Python 3.9 and notes that other Python 3 versions should also work; it also recommends Windows 10 or Ubuntu 20.04 LTS.
- An OpenAI API key. The tools call the OpenAI ChatCompletion API (e.g., `gpt-3.5-turbo`).

**Steps**

1. Clone this repository and change into the project directory.

2. Install the Python dependencies:

```bash
pip install -r requirements.txt
```

3. Add your OpenAI API key on line 3 of `apikey.ini`, as documented in `source/tutorial/reading_papers.md` (per the tutorial, the key stays on your local machine):

```ini
OPENAI_API_KEYS = [sk-...]  # input your API key here
```

4. Run the main script `chat_paper.py` to search arXiv and generate paper summaries:

```bash
python chat_paper.py --query "ti: chatgpt

---

## Examples

Examples of how this should work and how it should be used are available [here](./source/tutorial).

---

## Contributing

---

## License

This project is protected under the License. For more details, refer to the [LICENSE](./LICENSE.md) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). ChatPaper-zny27arw repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{ChatPaper-zny27arw,

        author = {README Benchmark},

        title = {ChatPaper-zny27arw repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---