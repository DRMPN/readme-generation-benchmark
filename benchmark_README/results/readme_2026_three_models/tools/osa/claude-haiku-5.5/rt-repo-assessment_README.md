# rt-repo-assessment-bwus27ob

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

rt-repo-assessment-bwus27ob is a Python batch pipeline that scores software repositories against configurable quality criteria and produces per-repository assessment results and a Markdown report. It combines deterministic checks with large language model-based scoring of repository metadata and individual file contents. It is intended for developers and maintainers who want automated, criteria-driven quality reports, with repositories supplied either as remote URLs or from a local inputs directory. The project is a command-line-style workflow rather than a web application or library, so newcomers should see the Getting Started section for setup and runnable steps.

---

## Core Features

- **Automated repository assessment:** Scores a repository from a list of repo URLs or a local inputs directory, and writes a JSON assessment, per-file JSON scores, and a Markdown report for each project.
- **Hybrid criteria evaluation:** Combines deterministic logic-based checks with LLM-based scoring for repository metadata and per-file content, so both rule-based and judgment-based criteria are covered in one run.
- **Multi-format file content scoring:** Loads and scores text files, PDFs, DOCX files, and Jupyter notebooks, skipping files that are empty or exceed the token limit.
- **YAML-defined criteria and prompts:** Defines criteria, their evaluation type (custom logic, file content, or metadata), and scoring prompts in YAML files, making them easier to review and edit.

---

## Installation

**Prerequisites:** requires Python >=3.12,<4.0

Install rt-repo-assessment-bwus27ob using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/rt-repo-assessment-bwus27ob
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

### Prerequisites

- Python, as specified in `.python-version` and `pyproject.toml`. For dependency setup, see the Installation section.
- Access to the LLM used for scoring (`GPT_4O_MINI`, configured in `utils/llm.py`). The required credential setup is not documented in the provided context.

### Steps

1. **Set up the environment.** Follow the Installation section to install dependencies.
2. **Review the prompts file.** The pipeline reads `prompts.yaml`, whose path is defined by `config.paths.PROMPTS_FPATH`.
3. **Prepare the run configuration.** The pipeline reads a JSON configuration file whose path is defined by `config.paths.CONFIG_FPATH`. `src/main.py` reads these keys: `urls`, `max_workers`, `from_inputs_directory`, and `project_name`. If `from_inputs_directory` is true, `project_name` must match a directory under the inputs directory (`paths.INPUTS_DIR`).
4. **Run the pipeline.** The entry point is the `__main__` block in `src/main.py`. The exact run command is not documented in the provided context.
5. **Review the outputs.** Results are written to `data/outputs/<project-name>/`:
   - `assessment.json`
   - `file_scores.json`
   - `report.md`

---

## Testing

The repository includes pytest-based test artifacts:

- `pytest.ini`: pytest configuration file.
- `tests/conftest.py`: shared pytest fixtures and setup.
- `tests/test_project_validators.py`: tests for the project validators in `src/utils/project_validators.py`.

The observed test files cover the project validators in `src/utils/project_validators.py`. The exact command used to run the test suite is not documented in the provided context. Check `Makefile` and `pytest.ini` for project-specific run settings.

No CI workflow files were observed in the provided repository tree.

---

## Contributing

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). rt-repo-assessment-bwus27ob repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{rt-repo-assessment-bwus27ob,

        author = {README Benchmark},

        title = {rt-repo-assessment-bwus27ob repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---