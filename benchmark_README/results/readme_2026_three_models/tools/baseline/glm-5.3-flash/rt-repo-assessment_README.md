# RT Repo Assessment

**RT Repo Assessment** (`rt-repo-assessment`) is an LLM-powered tool that automatically evaluates the quality of software repositories — with a particular focus on AI/ML and data science projects. It downloads (or clones) a target GitHub repository, extracts metadata, and scores it against a rich set of predefined criteria spanning **code quality**, **dependencies**, **documentation**, **licensing**, and **repository structure**. The results are written as JSON assessment files and summarized in a human-readable Markdown report.

The tool uses OpenAI chat models (via LangChain) to perform structured, criteria-based scoring, combining three evaluation strategies:

- **Logic-based scoring** — deterministic checks computed directly from repository metadata (e.g., README presence, script length limits, secret management, repository size).
- **Metadata-based scoring** — LLM evaluation using repository metadata, README content, and the directory structure.
- **Content-based scoring** — per-file LLM evaluation of tracked files (Python scripts, notebooks, PDFs, text files, etc.), with results aggregated across files using configurable `AND`/`OR` logic.

## Features

- **Automated repository acquisition**: Public repositories are downloaded as zip archives; private or non-GitHub repositories are cloned via `git`. Failed downloads are retried.
- **Criteria-driven evaluation**: All criteria are defined declaratively in YAML configuration files, organized into categories and subcategories, and tagged as **Essential**, **Professional**, or **Elite** tiers.
- **Parallel file scoring**: Files are scored concurrently using a thread pool for faster assessments.
- **Structured LLM output**: LLM responses are parsed into validated Pydantic models (`CriterionScoring`), each yielding a binary score (0/1) and an explanation.
- **Markdown reporting**: A final report summarizes overall completion percentage, a breakdown by tier (Essential / Professional / Elite), and a detailed table of every criterion with pass/fail status and explanations.
- **Extensible criteria**: Adding a new criterion is as simple as adding an entry to a YAML file — no code changes required for metadata- or content-based criteria.

## How It Works

1. **Project acquisition** — The repository is downloaded and extracted (public repos) or cloned (private repos) into `data/inputs/`.
2. **Metadata extraction** — Validators check for the presence of `README.md`, `requirements.txt`, `pyproject.toml`, `setup.py`, `LICENSE`, `.gitignore`, and ignored/sensitive files; script lengths and the directory tree are also collected.
3. **Logic-based criteria** — Deterministic checks run immediately (e.g., `readme_presence`, `script_length`, `secret_management`, `repository_size`).
4. **Content-based scoring** — The repository is walked as a tree; each tracked file is loaded (supporting `.pdf`, `.docx`, `.ipynb`, and text formats), split into chunks with `RecursiveCharacterTextSplitter`, token-counted (via `tiktoken`, files exceeding 128K tokens are skipped), and scored by the LLM. Per-criterion scores are aggregated with `AND`/`OR` logic across all files.
5. **Metadata-based scoring** — Metadata-based criteria are evaluated concurrently by the LLM using the README, project metadata, and directory structure.
6. **Reporting** — Results are saved as `assessment.json`, `file_scores.json`, and `report.md` under `data/outputs/<project-name>/`.

## Requirements

- Python **3.12+** (`>=3.12,<4.0`)
- [uv](https://docs.astral.sh/uv/) for dependency management
- Git (for cloning private repositories)
- An **OpenAI API key** (or an **OpenRouter API key**)

## Installation

Clone the repository and install dependencies with `uv`:

```bash
git clone https://github.com/readytensor/rt-repo-assessment.git
cd rt-repo-assessment
make install   # runs: uv sync
```

The main dependencies include `langchain`, `langchain-openai`, `langchain-community`, `gitpython`, `pandas`, `pypdf`, `pyyaml`, `python-dotenv`, `tiktoken`, and `pytest` (plus `mypy` as a dev dependency).

## Configuration

### Environment variables

Copy the example environment file and add your API credentials:

```bash
cp .env.example .env
```

Set `OPENAI_API_KEY` for direct OpenAI access. Alternatively, if `OPEN_ROUTER_API_KEY` is present in the environment, requests are routed through OpenRouter (`https://openrouter.ai/api/v1`).

### Run configuration

Edit `src/config/config.json`:

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

| Key | Description |
|-----|-------------|
| `from_inputs_directory` | If `true`, assess a project already placed in `data/inputs/` (identified by `project_name`) instead of downloading a URL. |
| `project_name` | Name of the local project directory under `data/inputs/` used when `from_inputs_directory` is `true`. |
| `urls` | List of repository URLs to assess when `from_inputs_directory` is `false`. |
| `max_workers` | Maximum number of parallel workers used for concurrent file and criteria scoring. |

### Scoring criteria

Criteria live in `src/config/scoring/` as YAML files:

- `code_quality_criteria.yaml` — modularity, script/function length, duplication, configuration, logging, error handling, testing, docstrings, type hints, style, complexity, AI/ML-specific checks (random seeds, data validation, model organization), and notebook-specific checks.
- `dependancies_criteria.yaml` — dependency listing and pinning, dependency groups, Python version specification, environment management, lockfiles, GPU requirements, and containerization.
- `documentation_criteria.yaml` — README quality, project structure documentation, setup/usage instructions, technical documentation, license identification, and community documentation.
- `license_criteria.yaml` — license presence and appropriateness, copyright notices, data/model usage rights, and code of conduct.
- `structure_criteria.yaml` — repository organization, naming conventions, directory design, entry points, and secret management.

Each criterion supports fields such as `name`, `description`, tier flags (`essential`, `professional`, `elite`), `based_on` (`metadata`, `file_content`, or `custom_logic`), `aggregation` (`AND`/`OR`), `include_extensions`/`exclude_extensions` for file filtering, optional LLM `instructions`, and `args` for custom-logic parameters (e.g., `max_script_length: 500`, `max_size: 50` for repository size in MB).

### File tracking

`src/config/tracked_files.yaml` controls which files are analyzed:

- `tracked_extensions` — extensions considered for scoring (`.py`, `.ipynb`, `.json`, `.yaml`, `.txt`, `.toml`, `.pdf`, `.md`, `.yml`, `.lock`).
- `text_extensions` — extensions loaded as plain text.
- `script_extensions` — extensions checked for script-length limits (`.py`, `.ipynb`).
- `ignored_names` — directories and files to skip (`.env`, `.venv`, `venv`, `__pycache__`, `.git`, etc.).

### Prompts

LLM prompts are defined in `src/config/prompts.yaml`: `scoring_v0` (repository-level criteria scoring using README, metadata, and directory structure) and `score_file` (per-file content scoring).

## Usage

Run the assessment pipeline:

```bash
uv run python src/main.py
```

The pipeline will:

1. Download/clone each configured repository into `data/inputs/`.
2. Run all logic-based, content-based, and metadata-based criteria.
3. Write outputs to `data/outputs/<project-name>/`:
   - `assessment.json` — scores and explanations for every criterion.
   - `file_scores.json` — per-file content-based scores.
   - `report.md` — a Markdown quality assessment report with an overall summary, category breakdown table, and detailed criterion table (✅/❌ status with explanations).

## Project Structure

```
├── data/
│   ├── inputs/          # Downloaded/cloned repositories
│   └── outputs/         # Assessment results and reports
├── src/
│   ├── config/          # Paths, run config, prompts, criteria YAML, logic-based scoring
│   ├── directory_scorer/# File tree building and content-based file scoring
│   ├── utils/           # LLM setup, repository handling, validators, general helpers
│   ├── main.py          # Pipeline entry point
│   ├── generators.py    # Criteria generators and helpers
│   ├── output_parsers.py# Pydantic models for structured LLM output
│   ├── report.py        # Markdown report generation
│   └── logger.py        # Logging setup
├── tests/               # Test suite
├── Makefile             # install and test targets
├── pyproject.toml       # Project metadata and dependencies
└── pytest.ini           # Pytest configuration
```

## Development

- **Logging**: A console logger (INFO level) is provided via `src/logger.py` and used throughout the pipeline.
- **Type checking**: `mypy` is included as a dev dependency:

  ```bash
  uv run mypy src/
  ```

- **Extending criteria**: Add new criteria to the appropriate YAML file in `src/config/scoring/`. For a new custom-logic criterion, implement the scoring function in `src/config/logic_based_scoring.py`, register it in the `logic_based_scoring` dictionary, and use the provided `@scoring_function` decorator to enforce the `{score, explanation}` result contract.

## Testing

Tests use `pytest` (configured via `pytest.ini` with the project root on the Python path). The existing suite covers the repository validators — detection of `README.md`, `requirements.txt`, `setup.py`, `LICENSE`, and `.gitignore` files — using temporary fixture directories.

Run the tests:

```bash
make test    # runs: uv run pytest tests/
```

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file. Copyright © 2025, Ready Tensor, Inc. (contact@readytensor.com).
