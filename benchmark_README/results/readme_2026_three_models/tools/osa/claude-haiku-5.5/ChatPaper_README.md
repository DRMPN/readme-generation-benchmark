# ChatPaper-o5g5n7wv

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

ChatPaper is a set of Python tools for working with academic papers using large language models. It addresses tasks such as chatting with and summarizing PDF papers, and generating draft survey papers in LaTeX. The project is aimed at researchers and students who work with scientific literature, as well as developers who run or deploy these tools. The repository offers command-line scripts for paper chat and survey generation, along with a web deployment wrapper and a Sphinx documentation set. For runnable steps and dependency setup, see the Getting Started section.

---

## Core Features

- **Automated PDF paper chat and summarization:** Lets users query and summarize academic papers from PDF input using OpenAI-based processing, so they can get quick answers from research documents without reading them in full.
- **Automated LaTeX survey generation:** Generates survey paper sections in LaTeX from a title, using GPT-driven prompts, reducing the effort needed to draft a literature-review style document.
- **Reference collection and BibTeX output:** Gathers related references for keywords and writes them to BibTeX, giving a starting bibliography for generated surveys.
- **Domain knowledge retrieval:** Queries prebuilt FAISS vector databases of domain knowledge to supply context to survey generation when a knowledge database is available.
- **Web deployment wrappers:** Includes app wrappers for Hugging Face deployment, so the tooling can be hosted as a web app.

---

## Installation

Install ChatPaper-o5g5n7wv using one of the following methods:

**Using PyPi:**

```sh
pip install scipdf
```

---

## Getting Started

### Prerequisites

- Python with `pip` available in your shell.
- Access to OpenAI models. `auto_survey/main.py` uses `GPTModel` from `utils/gpt_interaction.py`. The credential setup is not shown in the reviewed files, so check that module before running.

### Quickstart

1. Get the repository and open a terminal in the repository root.
2. Install the `auto_survey` dependencies:

```bash
pip install -r auto_survey/requirements.txt
```

3. Change into the `auto_survey` directory. Its modules are imported as `utils.*`, so run from this directory:

```bash
cd auto_survey
```

4. Run the pipeline from `main.py`. The reviewed excerpt defines `_generation_setup(...)` and `section_generation(...)` but does not show the entry-point code. Check the end of `main.py` for the run entry point before executing it.
5. Check the outputs. `copy_templates` creates a destination folder that receives `generation.log`, and each generated section is written to `<section>.tex` in the save path.

For the root-level scripts (`chat_paper.py`, `chat_arxiv.py`), install dependencies from the root `requirements.txt` instead.

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

    README Benchmark (2026). ChatPaper-o5g5n7wv repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{ChatPaper-o5g5n7wv,

        author = {README Benchmark},

        title = {ChatPaper-o5g5n7wv repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---