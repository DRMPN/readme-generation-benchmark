# rt-repo-assessment

A Python tool that evaluates a code repository against a set of documented quality criteria and writes a Markdown report. It combines deterministic checks (for example, whether a README, LICENSE, or `.gitignore` exists) with LLM-based scoring of the repository metadata, the README, and individual source files.

For each repository, the tool produces:

- `assessment.json`: a score (0 or 1) and an explanation for every criterion.
- `file_scores.json`: per-file scores from the file-content criteria.
- `report.md`: a summary of criteria met, broken down by Essential, Professional, and Elite tiers.

## Features

- **Repository input from GitHub URLs or local files.** Public GitHub repositories are downloaded as a ZIP archive. Private repositories are cloned with `git`.
- **Three criterion types:**
  - *Logic-based* checks run in Python (README presence, script length, secret-file detection, repository size).
  - *Metadata-based* checks send repository metadata and the README to an LLM.
  - *File-content* checks send each tracked file to an LLM and combine the per-file results using OR or AND aggregation.
- **Criteria defined in YAML.** Criteria live in `src/config/scoring/*.yaml`, so they can be edited without changing code.
- **Tiered reporting.** Each criterion is tagged as Essential, Professional, and/or Elite.

## Requirements

- Python 3.12 or later (`requires-python = ">=3.12,<4.0"`; `.python-version` is set to `3.12`)
- [uv](https://docs.astral.sh/uv/) for dependency management (the Makefile uses `uv sync` and `uv run`)
- `git` on your `PATH`, required when cloning private repositories
- An OpenAI API key or an OpenRouter API key, because the scoring pipeline calls an LLM
- Network access to GitHub and to the LLM provider

## Installation

```bash
git clone https://github.com/readytensor/rt-repo-assessment.git
cd rt-repo-assessment
make install   # runs: uv sync
```

## Configuration

### API keys

Copy the example environment file and add a key:

```bash
cp .env.example .env
```

`.env.example` supports two options:

```
# Using openai key
OPENAI_API_KEY=...

# Or you can use OpenRouter key
OPEN_ROUTER_API_KEY=...
```

If `OPEN_ROUTER_API_KEY` is set, `src/utils/llm.py` sends requests to `https://openrouter.ai/api/v1`. Otherwise, it uses the default OpenAI endpoint. The scoring pipeline in `src/main.py` and `src/directory_scorer/content_based_scorer.py` uses the `gpt-4o-mini` model (`GPT_4O_MINI` in `src/utils/llm.py`).

### Run settings

Runtime settings are in `src/config/config.json`:

| Key | Default | Description |
|-----|---------|-------------|
| `from_inputs_directory` | `false` | If `true`, assess the project folder named by `project_name` under `data/inputs/`. If `false`, download each URL in `urls`. |
| `project_name` | `"my-first-ai-project"` | Folder name under `data/inputs/` used when `from_inputs_directory` is `true`. |
| `urls` | `["https://github.com/readytensor/rt-repo-assessment"]` | GitHub repository URLs to assess when `from_inputs_directory` is `false`. |
| `max_workers` | `30` | Number of parallel workers for LLM calls and file scoring. |

## Usage

Run the assessment from the repository root:

```bash
uv run python src/main.py
```

`src/main.py` is the only entry point. It does not take command-line arguments. Edit `src/config/config.json` to choose which repositories to assess.

For each project, the tool:

1. Downloads the repository into `data/inputs/<repo-name>/`, or uses an existing folder there when `from_inputs_directory` is `true`.
2. Runs the logic-based checks.
3. Runs the metadata-based checks with the LLM.
4. Scores every tracked file with the LLM and combines the results.
5. Writes the outputs to `data/outputs/<repo-name>/`.

Downloads and output folders are overwritten on each run.

## Output

```
data/outputs/<repo-name>/
├── assessment.json    # Criterion ID -> {score, explanation}
├── file_scores.json   # Per-file criterion scores
└── report.md          # "Quality Assessment Report" with summary tables
```

`report.md` contains:

- an overall count of criteria met;
- a table of met criteria and percentages for each tier (Essential, Professional, Elite);
- a detailed table for each tier, showing each criterion's status (✅ or ❌) and explanation.

## Assessment criteria

Criteria are defined in `src/config/scoring/`:

| File | Area |
|------|------|
| `structure_criteria.yaml` | Repository layout, naming, directory design, environment files, secret management, repository size |
| `documentation_criteria.yaml` | README contents, setup and usage instructions, license mention, contribution and contact information |
| `code_quality_criteria.yaml` | Modularity, script and function length, configuration, logging, error handling, testing, docstrings, type hints, notebook checks |
| `dependancies_criteria.yaml` | Dependency files, pinning, dependency groups, Python version, environment management, containerization |
| `license_criteria.yaml` | License presence and appropriateness, copyright notices, data and model usage rights, code of conduct |

Each criterion has a `name`, `description`, and tier flags (`essential`, `professional`, `elite`). Criteria may also include:

- `based_on`: `metadata` (the default, LLM-scored from repository metadata), `file_content` (LLM-scored per file), or `custom_logic` (Python-scored).
- `aggregation`: `OR` (met if any file satisfies it) or `AND` (met only if all files satisfy it). This applies to file-content criteria.
- `include_extensions` / `exclude_extensions`: restricts which file types a file-content criterion is applied to.
- `instructions`: extra guidance passed to the LLM.
- `args`: parameters for custom-logic checks, such as `max_script_length: 500`.

The logic-based checks are implemented in `src/config/logic_based_scoring.py`:

- `readme_presence`: a `README.md` exists in the repository root.
- `script_length`: no `.py` or `.ipynb` file exceeds `max_script_length` lines.
- `secret_management`: no common secret files are present (for example, `.env`, `credentials.json`, `id_rsa`).
- `repository_size`: the repository is no larger than `max_size` MB.

Which file types are tracked, and which folder names are ignored, is set in `src/config/tracked_files.yaml`.

## Project structure

```
.
├── data/
│   ├── inputs/        # Downloaded or local repositories to assess (contents git-ignored)
│   └── outputs/       # Generated assessments and reports (contents git-ignored)
├── src/
│   ├── main.py                    # Entry point: runs the full assessment
│   ├── generators.py              # Loads criteria and builds criterion generators
│   ├── output_parsers.py          # Builds Pydantic models for LLM structured output
│   ├── report.py                  # Writes report.md
│   ├── logger.py                  # Logging setup
│   ├── config/
│   │   ├── config.json            # Run settings
│   │   ├── paths.py               # Project paths
│   │   ├── prompts.yaml           # LLM prompt templates
│   │   ├── tracked_files.yaml     # Tracked extensions and ignored names
│   │   ├── logic_based_scoring.py # Python-implemented checks
│   │   └── scoring/               # Criteria definitions (YAML)
│   ├── directory_scorer/
│   │   ├── content_based_scorer.py # Per-file LLM scoring and aggregation
│   │   └── tree.py                 # File tree used for file-content scoring
│   └── utils/
│       ├── llm.py                  # LLM client setup
│       ├── repository.py           # Download, clone, and tree helpers
│       ├── project_validators.py   # File-presence checks
│       └── general.py              # YAML/JSON helpers
├── tests/
│   ├── conftest.py
│   └── test_project_validators.py
├── .env.example
├── Makefile
├── pyproject.toml
├── pytest.ini
└── uv.lock
```

## Testing

```bash
make test   # runs: uv run pytest tests/
```

The test suite currently covers the file-presence helpers in `src/utils/project_validators.py` (README, requirements.txt, setup.py, LICENSE, and .gitignore detection). It does not cover the LLM-based scoring or the report generation.

## Dependencies

Declared in `pyproject.toml`:

- `gitpython`
- `langchain`, `langchain-community`, `langchain-openai`
- `pandas`
- `pypdf`
- `pytest`
- `python-dotenv`
- `pyyaml`, `types-pyyaml`

The development group includes `mypy`.

The code also imports `tiktoken`, `requests`, and `pydantic`. These are not listed directly in `pyproject.toml`; they are available through the locked dependencies in `uv.lock`.

## Limitations

- Assessments depend on LLM output. Results can vary with the model and provider, and the scores are not a substitute for human review.
- File-content scoring skips files that exceed the token limit (128,000 tokens by default) or are empty.
- The tool supports only the file types listed in `src/config/tracked_files.yaml` and the loaders in `src/directory_scorer/content_based_scorer.py`.
- Public repositories are downloaded from the `main` branch, falling back to `master`. Private repositories are cloned from the `main` branch.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for the full text. Copyright (c) 2025 Ready Tensor, Inc.
