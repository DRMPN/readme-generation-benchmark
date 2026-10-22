# dialog2graph-jrmfef7_

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

Dialog2Graph is a Python library and command-line tool for generating dialog graphs from input dialogs, intended for developers and researchers working on dialog systems and NLP pipelines. Alongside graph generation, it supports dialog data generation and augmentation as well as graph evaluation, with LLM-based pipelines at its core. The project also includes a separate layer of self-contained research experiments for exploration beyond the main library. Newcomers should start with the Getting Started section for runnable setup and usage steps.

---

## Core Features

- **Dialog graph generation** — turn collections of input dialogs into dialog graphs with three ready-made pipelines: a light pipeline, an LLM-based pipeline, and a graph extender, so you can choose the approach that fits your task.
- **Topic-driven dialog data generation** — create dialog data for a specified topic on demand, so you can bootstrap datasets without manually collecting dialogs first.
- **Dialog augmentation** — expand existing dialog datasets, giving you more material for building and evaluating graphs.
- **Evaluation and reporting** — measure generated graphs with both LLM-based and non-LLM metrics and validators, optionally against a reference graph, so you can quantify the quality of your results.
- **CLI and Python API access** — drive the whole workflow from a single command-line tool or call pipelines directly from Python, supporting both quick experiments and integration into your own code.

---

## Installation

**Prerequisites:** requires Python ^3.12

Install dialog2graph-jrmfef7_ using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/dialog2graph-jrmfef7_
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

**Prerequisites**

- Python 3.10-3.12 (`pyproject.toml` requires `>=3.10,<3.13`)
- Poetry (the project ships `pyproject.toml` and `poetry.lock`)
- An `.env` file with your LLM API credentials - every CLI command loads it (path configurable via `--env/-e`, default `.env`)
- A YAML config file `cfg.yml` (default; override with `--cfg/-c`)

**Quickstart**

1. Install dependencies:

```bash
   poetry install
```

2. Place `.env` (LLM credentials) and `cfg.yml` (pipeline configuration) in your working directory, or pass custom paths with `-e`/`-c`.

3. (Optional) Start the SQL-backed prompt cache service defined in `docker-compose.yml`:

```bash
   docker-compose up -d
```

4. Generate dialog data for a topic (saved to `generated_data.json` unless `--output/-o` is given):

```bash
   poetry run dialog2graph gen-data --topic "booking a hotel"
```

5. Build a dialog graph from the generated dialogs:

```bash
   poetry run dialog2graph gen-graph-light --dialogs generated_data.json
```

   Add `--eval` to run pipeline evaluations, and `--output/-o` / `--report/-r` to save the graph and an evaluation report.

Two further graph workflows are available: `gen-graph-llm` (LLM-based generation) and `gen-graph-extender` (extends an existing graph passed with `--graph/-g`). Run `poetry run dialog2graph --help` to list all commands and options (Click derives command names from the `gen_data`, `gen_graph_light`, `gen_graph_llm`, `gen_graph_extender` entry points, rendering underscores as dashes). Runnable examples are in the `examples/` directory (e.g., `cli_usage`).

---

## Testing

The project uses **pytest** with coverage tooling (`pytest`, `pytest-cov`, and `coverage` are declared in the optional `tests` dependency group in `pyproject.toml`).

Test suites are organized under the top-level `tests/` directory:

- `tests/cli/` — CLI command tests
- `tests/metrics/` — metrics tests
- `tests/pipelines/` — pipeline tests
- `tests/test_dialog_augmentation.py`, `tests/test_validators.py`, `tests/test_initialization.py`, `tests/test_topic_generation_init.py` — targeted test modules

Run tests via the poethepoet tasks defined in `pyproject.toml`:

```bash
poe test        # quick test suite (scripts.test:quick_test)
poe coverage    # test suite with coverage (scripts.test:coverage)
poe check_metrics  # d2g pipeline checks (scripts.check_metrics:test_d2g_pipelines)
```

The `check_metrics` task exercises the graph-generation pipelines and their evaluation metrics, which may require a configured environment (`.env` with LLM credentials) since the pipelines are LLM-based.

Additional verification commands: `poe lint` and `poe format` run ruff-based checks (configured via `ruff.toml`) through `scripts/codestyle.py`.

A `.github/workflows` directory exists, suggesting CI integration, but its configuration details are not available in the provided context. Note that each package under `experiments/` contains its own `pyproject.toml` and `tests/` directory; tests for a given experiment are scoped to that experiment's package rather than the main test suite.

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Documentation

A detailed dialog2graph-jrmfef7_ description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to dialog2graph-jrmfef7_.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). dialog2graph-jrmfef7_ repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{dialog2graph-jrmfef7_,

        author = {README Benchmark},

        title = {dialog2graph-jrmfef7_ repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---