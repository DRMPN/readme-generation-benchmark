# rt-repo-assessment-87564zmb

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project provides an automated pipeline for assessing the quality of software repositories against configurable criteria, combining deterministic checks with LLM-based scoring of repository metadata and file contents. It is written in Python and is intended for developers and engineering or platform teams who need criteria-based repository evaluation, for example in internal assessment or curation workflows. The pipeline is operated from the command line and produces structured JSON scores together with a Markdown report for each assessed repository. See Getting Started for setup instructions and runnable steps.

---

## Core Features

*   **Deep Content Analysis:** The system analyzes the substantive content of source files and documentation (e.g., PDFs, notebooks, code). This provides granular quality insights based on the actual structure and writing quality of the repository.
*   **Hybrid Scoring Engine:** Assessment combines strict, deterministic checks (e.g., required file presence) with advanced LLM criteria based on project metadata. This ensures comprehensive evaluation across compliance and contextual quality.
*   **Automated Repository Ingestion:** It handles the download and structural inspection of target repositories, whether provided via a URL or a local path. This enables seamless automated quality evaluation of external codebases.
*   **Standardized Reporting:** Results are exported in both structured JSON format and comprehensive Markdown reports. This allows developers and platform teams to easily integrate and audit the assessment results.

---

## Installation

**Prerequisites:** requires Python >=3.12,<4.0

Install rt-repo-assessment-87564zmb using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/rt-repo-assessment-87564zmb
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

The pipeline scores target repositories against configurable criteria using deterministic rules and LLM calls (GPT-4o-mini via `langchain-openai`) and writes JSON scores plus a Markdown report.

**Prerequisites**

- Python 3.12 or newer (`pyproject.toml` specifies `>=3.12,<4.0`)
- The `uv` package manager (a `uv.lock` is included)
- An OpenAI API key
- Git (required only for cloning non-public repositories)

**Steps**

1. Install dependencies:

```bash
   uv sync
```

2. Create your environment file and add your OpenAI API key (`.env` is loaded with `python-dotenv`):

```bash
   cp .env.example .env
```

3. Edit the JSON config file read by `src/main.py` (`paths.CONFIG_FPATH`, defined in `src/config`):
   - `urls`: repository URLs to assess; they are downloaded or cloned into `data/inputs` automatically
   - `max_workers`: number of parallel workers
   - To score a repository already present in `data/inputs`, set `from_inputs_directory` to `true` and `project_name` to its directory name instead of providing URLs.

4. From the repository root, run the pipeline:

```bash
   uv run python src/main.py
```

5. Inspect the results in `data/outputs/<project-name>/`:
   - `assessment.json` and `file_scores.json`: JSON scores
   - `report.md`: Markdown report

> Note: `tiktoken` is imported by `src/directory_scorer/content_based_scorer.py` but is not declared in `pyproject.toml`. If the first run fails with an import error for `tiktoken`, install it into your environment and rerun.

---

## Architecture

The repository utilizes a modular, pipeline-based architecture designed for automated software repository quality assessment. The core flow involves ingesting a target repository and subjecting it to multiple layers of scoring defined by configurable criteria.

*   **Repository Ingestion**: The system manages the acquisition of external repositories, handling both public downloads and private cloning. It subsequently extracts foundational project metadata (e.g., existence of `LICENSE` or `README`) and builds a comprehensive file system tree structure.
*   **Scoring Modes**: Assessment is performed using two primary scoring mechanisms:
    *   **Logic-Based Scoring**: Deterministic checks validate predefined structural and metadata criteria using configured rules (stored in `src/config`).
    *   **Content-Based Scoring**: Files are processed by traversing the codebase tree. Content analysis loads diverse file types (PDF, DOCX, Notebook, text) and splits them into chunks for LLM evaluation against detailed criteria.
*   **Execution and Processing**: Scoring operations, particularly the content-based evaluation, are highly concurrent, utilizing a thread pool executor to maximize throughput when scoring files across the repository structure.
*   **Outputs and Reporting**: Results are captured as structured data. The system aggregates scores from both the logic checks and the detailed file analyses, producing both granular JSON score outputs and a final comprehensive Markdown report.

---

## Testing

The project employs `pytest` as its primary testing framework. Verification scripts are located in the `tests/` directory and configuration is managed via `pytest.ini`. Test artifacts currently include `tests/test_project_validators.py` and `tests/conftest.py`.

---

## Contributing

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). rt-repo-assessment-87564zmb repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{rt-repo-assessment-87564zmb,

        author = {README Benchmark},

        title = {rt-repo-assessment-87564zmb repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---