# rt-repo-assessment

## Overview

`rt-repo-assessment` is a Python tool that evaluates the quality of software repositories. It downloads or reads a project, scores it against a set of configurable criteria, and writes the results as JSON files and a Markdown report.

The assessment combines three kinds of scoring:

- **Logic-based checks** (Python code in `src/config/logic_based_scoring.py`), such as README presence, script length, secret file detection, and repository size.
- **Metadata-based checks** that send repository metadata, the README, and the directory tree to an LLM together with each criterion's description and instructions.
- **Content-based checks** that send individual tracked files to an LLM. File-level results are then combined into project-level results using each criterion's `AND` or `OR` aggregation rule.

Criteria are grouped into five categories: Code Quality, Environment and Dependencies, Documentation, License and Legal, and Repository Architecture. Each criterion is also flagged as Essential, Professional, or Elite, and the report summarizes results by these tiers.

## Requirements

- Python 3.12 or later, below 4.0 (from `requires-python` in `pyproject.toml`).
- [uv](https://docs.astral.sh/uv/), used by the Makefile to install dependencies and run tests.
- An OpenAI-compatible API key for the LLM calls. See [Configuration](#configuration).
- Git, which is needed when the tool clones private repositories through `git clone`.

## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/readytensor/rt-repo-assessment
   cd rt-repo-assessment
   ```

2. Install the dependencies:

   ```bash
   make install
   ```

   This runs `uv sync` using the locked versions in `uv.lock`.

3. Create your environment file from the template:

   ```bash
   cp .env.example .env
   ```

   Then fill in the values your setup requires. The contents of `.env.example` are not reproduced here, so check that file for the variable names it expects.

The dependencies declared in `pyproject.toml` are `gitpython`, `langchain`, `langchain-community`, `langchain-openai`, `pandas`, `pypdf`, `pytest`, `python-dotenv`, `pyyaml`, and `types-pyyaml`. The development group includes `mypy`. Some modules import packages that are not listed in `pyproject.toml`, including `tiktoken`, `requests`, `pydantic`, and `langchain_core`. These are probably installed as transitive dependencies, but the files do not confirm this.

## Usage

### Choosing projects to assess

The entry point is `src/main.py`. It reads its settings from `src/config/config.json`:

```json
{
    "from_inputs_directory": false,
    "project_name": "my-first-ai-project",
    "urls": [
        "https://github.com/readytensor/rt-repo-assessment"
    ],
    "max_workers": 30
}
```

- When `from_inputs_directory` is `false`, each URL in `urls` is downloaded into `data/inputs/<repository-name>`.
- When `from_inputs_directory` is `true`, the script assesses the existing folder `data/inputs/<project_name>`. If that folder does not exist, it raises `NotADirectoryError`.

Public GitHub repositories are downloaded as a ZIP archive from the `main` branch, with a fallback to `master`. Other repositories are cloned with `git clone --branch main`. Existing folders at the target location are removed before downloading.

### Running an assessment

The files do not define a run target in the Makefile. The modules import each other using paths relative to `src/`, so the script is best run with `src/` on the path. One way to do this from the project root is:

```bash
uv run python src/main.py
```

### Outputs

For each project, results are written to `data/outputs/<project-directory-name>/`:

- `assessment.json`: criterion scores and explanations. It is updated as metadata-based criteria complete, then written again with directory-level results merged in.
- `file_scores.json`: the per-file scores produced by the content-based scorer.
- `report.md`: a Markdown report containing an overall summary, a category breakdown table, and detailed tables for the Essential, Professional, and Elite criteria. Each row shows a status icon (✅ or ❌) and the explanation.

The `data/inputs` and `data/outputs` directories each contain a `.gitignore` file, so their contents are excluded from version control.

## Configuration

### Runtime settings

| File | Purpose |
|------|---------|
| `src/config/config.json` | Repository URLs, the input-directory switch, the project name, and `max_workers` for parallel processing. |
| `.env` (from `.env.example`) | Environment variables loaded with `python-dotenv`. |
| `src/config/tracked_files.yaml` | Tracked file extensions, text extensions, ignored names, and script extensions. |
| `src/config/prompts.yaml` | Prompt templates: `scoring_v0` for repository-level criteria and `score_file` for individual files. |
| `src/config/paths.py` | Central definitions of the data, input, output, and configuration paths. |

### Environment variables

- `OPEN_ROUTER_API_KEY`: If this variable is set, `src/utils/llm.py` passes it as the API key and points the OpenAI-compatible client at `https://openrouter.ai/api/v1`. If it is not set, the client uses its default configuration. The OpenAI client typically reads `OPENAI_API_KEY` from the environment, but this is not stated in the repository files.
- `.env` is loaded by `src/utils/llm.py` and `src/directory_scorer/content_based_scorer.py`.

### Models

`src/utils/llm.py` defines three models: `gpt-4o-mini`, `gpt-4o`, and `gpt-4.1-mini`. `src/main.py` uses `gpt-4o-mini` for both metadata-based and content-based scoring. The temperature is set to `0` for all models.

### Criteria

Criteria are defined in YAML files under `src/config/scoring/`:

- `code_quality_criteria.yaml`
- `dependancies_criteria.yaml`
- `documentation_criteria.yaml`
- `license_criteria.yaml`
- `structure_criteria.yaml`

Each criterion can define:

- `name` and `description`
- `essential`, `professional`, and `elite` flags
- `based_on`: `file_content`, `custom_logic`, or metadata (the default when omitted)
- `include_extensions` and `exclude_extensions`
- `aggregation`: `AND` or `OR`, used to combine file-level results
- `instructions`: additional guidance passed to the LLM
- `args`: arguments for logic-based checks, such as `max_script_length: 500` and `max_size: 50`

The logic-based checks are registered in `src/config/logic_based_scoring.py`: `readme_presence`, `script_length`, `secret_management`, and `repository_size`.

### Tracked files

`tracked_files.yaml` controls what the content-based scorer reads:

- **Tracked extensions** include `.py`, `.ipynb`, `.json`, `.yaml`, `.txt`, `.toml`, `.md`, `.yml`, and `.lock`.
- **Ignored names** include `.env`, `.venv`, `venv`, `env`, `.git`, `__pycache__`, `.github`, and `.DS_Store`.
- **Script extensions** are `.py` and `.ipynb`.

The file has an entry `-  pdf` with no leading dot, so PDF files may not match the extension check as written. The content-based scorer does include a `PyPDFLoader` path for `.pdf` files.

## Repository Structure

```
.
├── data/
│   ├── inputs/        # Downloaded or local projects to assess
│   └── outputs/       # Assessment results per project
├── src/
│   ├── main.py        # Entry point
│   ├── generators.py  # Criterion iteration and filtering
│   ├── output_parsers.py
│   ├── report.py      # Markdown report generation
│   ├── logger.py
│   ├── config/        # Settings, paths, prompts, and criteria YAML
│   ├── directory_scorer/
│   │   ├── content_based_scorer.py
│   │   └── tree.py
│   └── utils/
│       ├── llm.py
│       ├── general.py
│       ├── project_validators.py
│       └── repository.py
├── tests/
│   ├── conftest.py
│   └── test_project_validators.py
├── Makefile
├── pyproject.toml
└── pytest.ini
```

## Development

- Dependencies are managed with `uv`. Run `make install` to sync the environment from `uv.lock`.
- `mypy` is listed in the `dev` dependency group, but no mypy configuration file is included in the repository.
- Logging is set up in `src/logger.py`. It writes INFO-level messages with timestamps to the console.
- Settings for the LLM and the criteria are kept in configuration files, so most changes to scoring behavior can be made in `src/config/` without modifying Python code.
- To add a logic-based criterion, implement a function that returns `score` and `explanation`, add it to `logic_based_scoring`, and reference it in a criteria YAML file with `based_on: custom_logic`.

## Testing

Tests are run with:

```bash
make test
```

This runs `uv run pytest tests/`.

`pytest.ini` sets `pythonpath = .` and looks for files matching `test_*.py`. `tests/conftest.py` adds the project root and `src/` to `sys.path`.

The current test module, `tests/test_project_validators.py`, covers the file-presence validators in `src/utils/project_validators.py`:

- `has_readme`
- `has_requirements_txt`
- `has_setup_py`
- `has_license_file`
- `has_gitignore_file`

Each test creates files in a temporary directory, checks that the validator returns `False` before the file exists and `True` afterward, and includes a combined test that checks all validators together. The tests do not cover the LLM scoring, downloading, or report generation code.

## License

This project is licensed under the MIT License. Copyright (c) 2025, Ready Tensor, Inc. See the [LICENSE](LICENSE) file for the full text.
