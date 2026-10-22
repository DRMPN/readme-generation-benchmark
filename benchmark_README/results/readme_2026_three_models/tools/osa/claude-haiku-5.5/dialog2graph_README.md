# dialog2graph-7219qc0j

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Dialog2Graph is a Python library and command-line tool for generating dialog graphs from dialogs and for evaluating generated graphs against reference graphs. It is intended for developers and researchers working on dialog graph generation, dialog data creation, and graph evaluation. The project provides a command-line interface for running its generation pipelines, along with programmatic access to the same pipelines and evaluation metrics. Some pipelines use language models and embedding models, so review the Getting Started section before running them. For runnable steps and environment requirements, see Getting Started, and for detailed guides, see the documentation.

---

## Core Features

- **Dialog graph generation via CLI:** Generates dialog graphs from input dialog files through three pipeline variants (light, LLM-based, and extender), so graphs can be produced from the terminal without writing code.
- **Topic-based dialog data generation:** Generates dialog data for a given topic, providing input dialogs for graph generation.
- **Generated-versus-reference graph comparison:** Compares generated graphs with a true reference graph using structural and triplet-based checks, with an embedding-model option for triplet comparison, to assess output quality.
- **Reusable pipeline components for Python code:** Provides a base pipeline and dialog sampling components that can be imported to build custom dialog-to-graph workflows.

---

## Installation

**Prerequisites:** requires Python ^3.12

Install dialog2graph-7219qc0j using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/dialog2graph-7219qc0j
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

### Prerequisites

- Python `^3.10,<3.13`
- Poetry, used for packaging (see the Installation section for setup details)

### Steps

1. **Install the package.** Follow the Installation section to set up the project environment.

2. **Verify the CLI is available.**

```bash
dialog2graph --help
```

3. **Prepare configuration (optional).** The CLI commands read a `.env` file (`--env`) and a `cfg.yml` file (`--cfg`) by default. Pass different paths with these options if your files are elsewhere.

4. **Generate dialog data for a topic.** The `--topic` option is required.

```bash
dialog2graph gen-data --topic "<your topic>" --output generated_data.json
```

5. **Generate a dialog graph from the dialogs.** This runs the `d2g_light` pipeline.

```bash
dialog2graph gen-graph-light --dialogs generated_data.json
```

For available options, such as `--output`, `--report`, and `--eval`, run `dialog2graph gen-graph-light --help`.

---

## Testing

Contributors verify changes with the test tasks defined in `pyproject.toml` under `[tool.poe.tasks]`, run through [poethepoet](https://github.com/nat-n/poethepoet) (`poe`).

- `test`: runs `scripts.test:quick_test`.
- `coverage`: runs `scripts.test:coverage`.
- `check_metrics`: runs `scripts.check_metrics:test_d2g_pipelines`.
- `lint`: runs `scripts.codestyle:_check`, which checks code style with ruff (configured in `ruff.toml`).

Test artifacts are located in the `tests/` directory, which contains the subfolders `cli/`, `metrics/`, and `pipelines/`, along with top-level modules such as `test_dialog_augmentation.py`, `test_initialization.py`, `test_topic_generation_init.py`, and `test_validators.py`. The `metrics_results/` folder is also present under `tests/`. The test contents were not reviewed in detail.

The `.github/workflows` directory exists, indicating CI configuration, but its workflow contents were not reviewed, so the CI checks it runs are unknown.

For exact invocation details, refer to the scripts listed above and the `[tool.poetry.group.tests]` dependencies in `pyproject.toml`.

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Documentation

A detailed dialog2graph-7219qc0j description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to dialog2graph-7219qc0j.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). dialog2graph-7219qc0j repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{dialog2graph-7219qc0j,

        author = {README Benchmark},

        title = {dialog2graph-7219qc0j repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---