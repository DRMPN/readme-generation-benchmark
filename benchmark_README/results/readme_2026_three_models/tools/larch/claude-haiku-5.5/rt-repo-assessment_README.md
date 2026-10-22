# rt-repo-assessment-kna7nv30

A Python tool for assessing the quality of a software repository. It scores a codebase against configurable criteria covering licensing, code quality, documentation, dependencies, and project structure. It combines deterministic rule-based checks with content-based analysis, optionally using an LLM for judgments that are hard to express as rules, and produces a structured report.

> **Note:** This README was written from the file listing alone, without the source code. The directory layout, module responsibilities, and commands are inferred from file names and should be checked against the code. Items marked **(verify)** need confirmation.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Architecture Overview](#architecture-overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Assessment Criteria](#assessment-criteria)
- [Scoring Model](#scoring-model)
- [LLM Integration](#llm-integration)
- [Reports](#reports)
- [Testing](#testing)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Multi-dimensional assessment** across five areas: license, code quality, documentation, dependencies, and structure.
- **Criteria defined in YAML**, so rules can be changed without modifying code.
- **Two scoring approaches**:
  - *Logic-based scoring* for deterministic checks (e.g., does a LICENSE file exist, is a lock file present).
  - *Content-based scoring* for analysis of file contents.
- **Optional LLM-assisted evaluation** with prompt templates, generators, and output parsers that turn model responses into structured results.
- **Repository inspection** that walks the directory tree and collects tracked files.
- **Report generation** summarizing scores and findings.
- **Logging** throughout the pipeline.
- **Test suite** with pytest and shared fixtures.
- **Reproducible environment** managed with `uv`, with a locked dependency file.

---

## Project Structure

The file listing does not include directory paths, so the layout below is a best-effort reconstruction. Verify it against the actual repository.

```
rt-repo-assessment-kna7nv30/
├── LICENSE
├── Makefile
├── pyproject.toml
├── pytest.ini
├── uv.lock
├── main.py                        # CLI entry point (verify)
├── config.json                    # Runtime configuration
├── prompts.yaml                   # LLM prompt templates
├── tracked_files.yaml             # Files to track/inspect in a repository
│
├── criteria/                      # Assessment criteria (verify location)
│   ├── license_criteria.yaml
│   ├── code_quality_criteria.yaml
│   ├── documentation_criteria.yaml
│   ├── dependancies_criteria.yaml
│   └── structure_criteria.yaml
│
├── src/ or package root           # Main package (verify)
│   ├── __init__.py
│   ├── paths.py                   # Path constants and resolution helpers
│   ├── tree.py                    # Directory tree traversal
│   ├── repository.py              # Repository abstraction
│   ├── project_validators.py      # Rule-based validation of project artifacts
│   ├── logic_based_scoring.py     # Deterministic scoring logic
│   ├── content_based_scorer.py    # Scoring based on file contents
│   ├── llm.py                     # LLM client wrapper
│   ├── generators.py              # Prompt/request generation
│   ├── output_parsers.py          # Parsing LLM output into structured data
│   ├── general.py                 # Shared utilities
│   ├── logger.py                  # Logging configuration
│   └── report.py                  # Report building and rendering
│
└── tests/                         # (verify location)
    ├── conftest.py                # Shared pytest fixtures
    └── test_project_validators.py
```

Several subpackages contain `__init__.py` files, so the code is organized into modules. The exact grouping should be confirmed.

---

## Architecture Overview

The assessment pipeline likely runs in these stages:

```
 ┌──────────────┐    ┌────────────────┐    ┌─────────────────────┐
 │  Repository  │ -> │  Tree / Files  │ -> │ Project validators  │
 │  (input)     │    │  (tracked_files)│   │ & criteria (YAML)   │
 └──────────────┘    └────────────────┘    └──────────┬──────────┘
                                                      │
                    ┌─────────────────────────────────┴──────────┐
                    ▼                                            ▼
          ┌──────────────────┐                        ┌────────────────────┐
          │ Logic-based      │                        │ Content-based      │
          │ scoring          │                        │ scorer (+ LLM)     │
          └────────┬─────────┘                        └─────────┬──────────┘
                   └──────────────────┬─────────────────────────┘
                                      ▼
                             ┌────────────────┐
                             │ Report         │
                             └────────────────┘
```

1. **Input**: A target repository is identified, and its tracked files are listed.
2. **Traversal**: `tree.py` and `repository.py` gather the file structure.
3. **Validation**: `project_validators.py` checks for required artifacts.
4. **Scoring**: Logic-based scoring applies deterministic rules. Content-based scoring reads file contents, optionally calling the LLM through `llm.py`, `generators.py`, and `output_parsers.py`.
5. **Reporting**: `report.py` assembles and writes the final assessment.

---

## Requirements

- Python version as specified in `pyproject.toml` **(verify)**
- [`uv`](https://docs.astral.sh/uv/) for dependency management
- An LLM API key, if LLM-assisted scoring is enabled **(verify provider and variable name)**
- `make` (optional, for the Makefile targets)

---

## Installation

Clone the repository and install dependencies from the lock file:

```bash
git clone <repository-url> rt-repo-assessment-kna7nv30
cd rt-repo-assessment-kna7nv30
uv sync
```

`uv sync` creates a virtual environment and installs the exact versions pinned in `uv.lock`.

If the project provides a Makefile setup target, it can be used instead **(verify)**:

```bash
make install
```

---

## Configuration

### `config.json`

Holds runtime settings. Likely options include:

- which criteria files to load
- scoring weights and thresholds
- whether LLM-based scoring is enabled
- model name and parameters
- output format and location

Example (illustrative; the actual keys will differ):

```json
{
  "criteria_dir": "criteria",
  "enable_llm": true,
  "llm": {
    "model": "your-model-name",
    "temperature": 0.0
  },
  "report": {
    "format": "markdown",
    "output_dir": "reports"
  }
}
```

### `tracked_files.yaml`

Lists the files the assessment inspects (for example `README.md`, `LICENSE`, `pyproject.toml`, `requirements.txt`, CI configuration). Adding an entry extends what the tool looks at without code changes.

### Criteria files

Each `*_criteria.yaml` file defines the checks for one assessment area. A criterion would typically include an identifier, description, weight, and either a deterministic rule or a content-based instruction. See [Assessment Criteria](#assessment-criteria).

### `prompts.yaml`

Contains prompt templates used when content-based scoring calls the LLM. Templates are filled in by `generators.py`.

### Environment variables

Secrets such as API keys should come from environment variables and not be committed. Example **(verify variable names)**:

```bash
export OPENAI_API_KEY="..."        # or the provider key used by llm.py
```

---

## Usage

### Command line

Run the assessment against a repository. The exact arguments depend on `main.py` **(verify)**:

```bash
uv run python main.py --repo /path/to/target-repository
```

Common options that may exist **(verify)**:

| Option | Purpose |
|---|---|
| `--repo PATH` | Path to the repository to assess |
| `--config PATH` | Alternative config file (default `config.json`) |
| `--output PATH` | Where to write the report |
| `--no-llm` | Run only deterministic checks |
| `--verbose` | Increase log detail |

### Using the modules programmatically

```python
from <package> import repository, logic_based_scoring, report

repo = repository.Repository("/path/to/target-repository")
scores = logic_based_scoring.score(repo)
print(report.build(scores))
```

Replace `<package>` with the actual package name and check the function names before use.

---

## Assessment Criteria

Each area has its own YAML file.

### License (`license_criteria.yaml`)

- A LICENSE file exists at the repository root
- The license is recognized (e.g., MIT, Apache-2.0, GPL)
- License information is referenced in the README or package metadata
- Source files carry license headers, where applicable

### Code Quality (`code_quality_criteria.yaml`)

- Consistent formatting and linting configuration
- Tests are present and discoverable
- Type hints or static analysis configuration
- Reasonable module organization
- Absence of obvious issues flagged by content review

### Documentation (`documentation_criteria.yaml`)

- A README exists and has sufficient sections (installation, usage)
- Docstrings or API documentation
- Contribution and changelog guidance
- Examples are present

### Dependencies (`dependancies_criteria.yaml`)

- Dependencies are declared in `pyproject.toml` or equivalent
- A lock file exists (e.g., `uv.lock`)
- Dependencies are pinned or constrained
- No unnecessary or duplicated packages

> The file name is spelled `dependancies_criteria.yaml` in the repository. Keep this spelling when referencing the file, or rename it everywhere, including the code that loads it.

### Structure (`structure_criteria.yaml`)

- Standard layout (source, tests, docs, configuration separated)
- Presence of build and tooling files (`Makefile`, `pyproject.toml`, `pytest.ini`)
- Sensible entry points
- Clean root directory

---

## Scoring Model

Scoring probably works as follows **(verify)**:

1. Each criterion produces a result: pass/fail for deterministic rules, or a graded score for content-based rules.
2. Criterion results are normalized to a common scale (for example 0–100).
3. Criteria within an area are combined using their weights to produce an area score.
4. Area scores are combined into an overall score.

Pseudocode:

```
area_score   = Σ (criterion_score × criterion_weight) / Σ criterion_weight
overall      = Σ (area_score × area_weight)
```

---

## LLM Integration

When LLM-assisted scoring is enabled, the pipeline:

1. **Selects** the relevant files for a criterion (`content_based_scorer.py`).
2. **Builds** a prompt from a template in `prompts.yaml` (`generators.py`).
3. **Calls** the model through the wrapper in `llm.py`.
4. **Parses** the response into structured data (`output_parsers.py`).
5. **Feeds** the parsed result into the scoring logic.

Best practices:

- Use a low temperature for consistent results (`0.0` is a common choice).
- Keep prompts in `prompts.yaml` so behavior can be tuned without code changes.
- Run with `--no-llm` or disable LLM scoring in `config.json` to get fully deterministic and offline results.
- Be aware that sending repository content to an external provider may have privacy implications.

---

## Reports

`report.py` produces the final assessment. A typical report contains:

- repository name and assessment date
- overall score and per-area scores
- for each criterion: result, evidence, and recommendations
- a summary of failed or weak criteria

Output is likely Markdown, with JSON as a possible alternative **(verify)**.

---

## Testing

The test suite uses pytest. Configuration lives in `pytest.ini`, and shared fixtures are in `conftest.py`.

Run all tests:

```bash
uv run pytest
```

Run a single test module:

```bash
uv run pytest test_project_validators.py -v
```

Run with coverage, if `pytest-cov` is installed **(verify)**:

```bash
uv run pytest --cov
```

Current coverage includes `project_validators.py`. Adding tests for scoring, parsing, and report generation is recommended.

---

## Development

### Makefile

Check the Makefile for available targets. Commonly used targets might include:

```bash
make install     # install dependencies
make test        # run the test suite
make lint        # run linters/formatters
make run         # run the assessment
make clean       # remove caches and build artifacts
```

**(verify all targets)**

### Code style

- Follow the style configured in `pyproject.toml`.
- Add type hints and docstrings to new public functions.
- Keep criteria definitions in YAML rather than hard-coding them.

### Adding a new criterion

1. Add an entry to the appropriate `*_criteria.yaml` file.
2. Implement the check in `project_validators.py` (deterministic) or `content_based_scorer.py` (content-based).
3. If it is content-based, add or update a prompt in `prompts.yaml`.
4. Add the file to `tracked_files.yaml` if it is not already tracked.
5. Write tests in the `tests/` directory.

### Adding dependencies

```bash
uv add <package>          # runtime dependency
uv add --dev <package>    # development dependency
```

Commit the updated `uv.lock` together with `pyproject.toml`.

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Dependencies not installed | Run `uv sync` |
| LLM calls fail | Missing or invalid API key | Check the environment variable |
| Criteria not loaded | Wrong path in `config.json` | Verify `criteria_dir` |
| Empty report | Repository path incorrect or no tracked files matched | Check `--repo` and `tracked_files.yaml` |
| Tests cannot import modules | Package not on the path | Run tests through `uv run pytest` from the project root |

---

## Contributing

1. Fork the repository and create a feature branch.
2. Make your changes with tests.
3. Run the test suite and linters.
4. Open a pull request describing the change and its motivation.

---

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.
