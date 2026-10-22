# rt-repo-assessment

A Python tool that automatically assesses software repositories against configurable quality criteria using Large Language Models (LLMs). The tool analyzes a repository's structure, code quality, documentation, dependencies, and licensing, then produces a structured assessment report.

## Overview

`rt-repo-assessment` walks through a target repository, collects relevant files, scores them against YAML-defined criteria (code quality, documentation, dependencies, licensing, and project structure), and uses LLM-generated evaluations to produce a final report. It supports multiple LLM providers, custom prompts, and flexible output formats.

## Features

- **Automated repository traversal** — builds a file tree of the target repository and filters tracked files via configurable patterns.
- **Criteria-driven evaluation** — assessment rules are defined in declarative YAML files:
  - `code_quality_criteria.yaml`
  - `documentation_criteria.yaml`
  - `dependancies_criteria.yaml`
  - `license_criteria.yaml`
  - `structure_criteria.yaml`
- **LLM-powered scoring** — combines logic-based scoring (deterministic checks) with content-based scoring (LLM analysis of file contents).
- **Configurable prompts** — customize LLM behavior via `prompts.yaml`.
- **Pluggable LLM providers** — provider settings managed through `config.json`.
- **Structured reports** — outputs generated via configurable report generators with robust output parsing.
- **Project validation** — validates repositories before assessment (`project_validators.py`).
- **Logging** — built-in, configurable logging throughout the pipeline.

## Project Structure

```
rt-repo-assessment/
├── main.py                     # CLI entry point
├── repository.py               # Repository traversal and file handling
├── project_validators.py       # Pre-assessment repository validation
├── report.py                   # Report generation
├── llm.py                      # LLM provider abstraction
├── logger.py                   # Logging configuration
├── config.json                 # Runtime configuration (LLM settings, etc.)
├── prompts.yaml                # LLM prompt templates
├── tracked_files.yaml          # File patterns to include in analysis
├── criteria/                   # Assessment criteria (YAML)
│   ├── code_quality_criteria.yaml
│   ├── documentation_criteria.yaml
│   ├── dependancies_criteria.yaml
│   ├── license_criteria.yaml
│   └── structure_criteria.yaml
├── scorers/                    # Scoring logic
│   ├── content_based_scorer.py # LLM-based content scoring
│   └── logic_based_scoring.py  # Deterministic rule-based scoring
├── utils/                      # Helpers
│   ├── tree.py                 # File tree building
│   ├── paths.py                # Path utilities
│   ├── general.py              # General helpers
│   ├── generators.py           # Output generators
│   └── output_parsers.py       # LLM output parsing
└── tests/
    ├── conftest.py
    ├── pytest.ini
    └── test_project_validators.py
```

## Requirements

- Python 3.10+ (managed with [uv](https://github.com/astral-sh/uv) — see `uv.lock` / `pyproject.toml`)
- An LLM provider API key (configured in `config.json` or via environment variables)

## Installation

Using `uv` (recommended):

```bash
uv sync
```

Or with pip:

```bash
pip install -e .
```

## Configuration

1. **`config.json`** — set your LLM provider, model name, API keys/environment variable names, and generation parameters.
2. **`prompts.yaml`** — adjust the prompts sent to the LLM for each assessment category.
3. **`tracked_files.yaml`** — define which files (globs/extensions) should be collected and analyzed.
4. **`criteria/*.yaml`** — edit the assessment criteria and scoring rubrics for each category.

## Usage

Run the assessment from the command line:

```bash
python main.py --repo /path/to/target/repo
```

Typical workflow:

1. The repository is validated (`project_validators.py`).
2. A file tree is built (`tree.py`) and filtered against `tracked_files.yaml`.
3. Relevant files are gathered (`repository.py`).
4. Each criteria category is scored using logic-based checks and LLM content-based scoring.
5. LLM responses are parsed (`output_parsers.py`) and aggregated.
6. A final report is generated (`report.py` / `generators.py`).

## Running Tests

```bash
# Using pytest directly
pytest

# Or via the Makefile
make test
```

Test configuration lives in `pytest.ini` and `conftest.py`.

## Extending

- **Add criteria**: create a new YAML file in `criteria/` following the existing schema.
- **Add a scorer**: implement scoring logic in `scorers/` and register it with the pipeline.
- **Add an LLM provider**: extend the abstraction in `llm.py`.
- **Change report format**: add or modify a generator in `utils/generators.py`.

## License

This project is licensed under the terms found in the [LICENSE](LICENSE) file.
