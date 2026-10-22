# Repository Assessment Tool

A Python application for evaluating a software repository using configurable assessment criteria. The project includes repository inspection and validation code, scoring components, prompt and configuration files, and report-generation modules.

## What it assesses

Assessment criteria are organized by topic in YAML files:

- **Code quality** — `code_quality_criteria.yaml`
- **Documentation** — `documentation_criteria.yaml`
- **Dependencies** — `dependancies_criteria.yaml`
- **Licensing** — `license_criteria.yaml`
- **Repository structure** — `structure_criteria.yaml`

The project also includes components for examining repository contents, applying logic- and content-based scoring, running project validators, and generating a report. The precise scoring rules and report format are defined by the project’s configuration and implementation.

## Requirements

- Python, using the version and dependencies declared in `pyproject.toml`
- [uv](https://docs.astral.sh/uv/) is recommended, since the repository includes a `uv.lock` file

## Installation

From the project directory, install the locked dependencies with:

```bash
uv sync
```

If you do not use `uv`, consult `pyproject.toml` for the supported Python version and dependencies before installing them with your preferred package manager.

## Running an assessment

The application entry point is `main.py`. To see whether it supports command-line options, run:

```bash
uv run python main.py --help
```

Then run the command appropriate to your setup. If no arguments are required, the basic invocation is:

```bash
uv run python main.py
```

The assessment may depend on configuration in `config.json` and on the prompt definitions in `prompts.yaml`. Review these files before running the application, especially if you are assessing a repository other than the one configured by default.

The repository includes `llm.py`, so some functionality may use a language model. Check the configuration and implementation for required provider settings or credentials. Keep secrets out of committed configuration files.

## Running tests

Run the test suite with:

```bash
uv run pytest
```

The repository includes `test_project_validators.py` and `conftest.py`. You can also use the project’s Makefile, if it defines a test target:

```bash
make
```

Check `Makefile` for the available targets.

## Configuration and criteria

The main configuration and criteria files are:

| File | Purpose |
|---|---|
| `config.json` | General application configuration |
| `prompts.yaml` | Prompt definitions used by the application |
| `tracked_files.yaml` | Configuration related to tracked repository files |
| `license_criteria.yaml` | Licensing assessment criteria |
| `code_quality_criteria.yaml` | Code-quality assessment criteria |
| `documentation_criteria.yaml` | Documentation assessment criteria |
| `dependancies_criteria.yaml` | Dependency assessment criteria |
| `structure_criteria.yaml` | Repository-structure assessment criteria |

Review the relevant criteria YAML file to understand or adjust what the assessment checks. Keep YAML syntax valid when editing these files.

## Project layout

The project’s Python modules include:

- `main.py` — application entry point
- `repository.py` — repository-related operations
- `tree.py` and `paths.py` — repository structure and path handling
- `project_validators.py` — project validation logic
- `content_based_scorer.py` and `logic_based_scoring.py` — scoring components
- `generators.py`, `output_parsers.py`, and `report.py` — output and report-related components
- `llm.py` — language-model integration
- `logger.py` and `general.py` — shared utilities
- `pytest.ini` — pytest configuration

## Development

To make changes:

1. Install dependencies with `uv sync`.
2. Update the relevant implementation or criteria files.
3. Run the tests with `uv run pytest`.
4. Run the application against a suitable repository and review its output.

For project-specific commands, dependency declarations, and supported Python versions, refer to `pyproject.toml` and `Makefile`.
