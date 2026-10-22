# rt-repo-assessment

An automated tool for assessing the quality of software repositories. `rt-repo-assessment` evaluates a repository against a configurable set of scoring criteria — covering structure, documentation, code quality, dependencies, and licensing — using a combination of deterministic logic checks and LLM-based analysis. It produces raw scoring data as JSON and a human-readable Markdown report.

## How It Works

The assessment pipeline (`src/main.py`) processes each target repository in the following stages:

1. **Acquisition** — Public repositories are downloaded as zip archives and extracted; non-public repositories are cloned with Git. Alternatively, a local project directory already in `data/inputs/` can be assessed directly. Downloads are retried up to 3 times.
2. **Metadata extraction** — The tool inspects the repository for a README, dependency files (`requirements.txt`, `pyproject.toml`, `setup.py`), a license, a `.gitignore`, ignored/sensitive files, script lengths, the directory tree, and README content.
3. **Scoring** — Criteria are scored using three approaches:
   - **Logic-based** — deterministic Python checks (e.g., README presence, script length limits, secret-file detection, repository size).
   - **Metadata-based** — an LLM evaluates repository-level metadata (README content, directory structure, presence of key files) against each criterion, with structured output.
   - **Content-based** — each tracked file's content is loaded, split into chunks, and scored by an LLM in parallel using a thread pool. Per-file scores are then aggregated with AND/OR logic to produce project-level results.
4. **Reporting** — Results are written as JSON, and a Markdown report is generated summarizing overall and per-tier results.

## Scoring Criteria

Criteria are defined in YAML under `src/config/scoring/`:

| File | Category |
|------|----------|
| `structure_criteria.yaml` | Repository Architecture |
| `documentation_criteria.yaml` | Documentation |
| `code_quality_criteria.yaml` | Code Quality |
| `dependancies_criteria.yaml` | Environment and Dependencies |
| `license_criteria.yaml` | License and Legal |

Each criterion specifies a display name and description, which tier levels it applies to (`essential`, `professional`, `elite`), and — where applicable — the scoring method (`custom_logic` or `file_content`), aggregation logic (`AND`/`OR`), file extensions to include, additional LLM instructions, and arguments for logic-based checks.

The report classifies criteria into three tiers:

- **Essential** — required for any repository
- **Professional** — additional expectations beyond essential
- **Elite** — the highest bar; includes criteria not counted at the Professional tier

Each criterion receives a binary score (1 = met, 0 = not met) with a human-readable explanation.

## Outputs

For each assessed repository, results are written to `data/outputs/<repo-name>/`:

- **`assessment.json`** — scores and explanations for every criterion
- **`file_scores.json`** — per-file scores from content-based scoring
- **`report.md`** — a quality assessment report with an overall summary, a category breakdown (Essential / Professional / Elite percentages), and a detailed table of every criterion with pass/fail status and explanation

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for dependency management
- An OpenAI API key, or an OpenRouter API key

### Installation

```bash
make install
```

This runs `uv sync` to install dependencies from `uv.lock`.

### Configuration

1. **API keys** — copy `.env.example` to `.env` and set either `OPENAI_API_KEY` or `OPEN_ROUTER_API_KEY`. If `OPEN_ROUTER_API_KEY` is present, requests are routed through the OpenRouter API.
2. **Target repositories** — edit `src/config/config.json`:

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

| Setting | Description |
|---------|-------------|
| `urls` | List of repository URLs to assess (used when `from_inputs_directory` is `false`) |
| `from_inputs_directory` | If `true`, assess a local project directory instead of downloading from URLs |
| `project_name` | Name of the local project directory in `data/inputs/` (used when `from_inputs_directory` is `true`) |
| `max_workers` | Maximum number of parallel workers for LLM scoring |

### Running the Assessment

```bash
uv run python src/main.py
```

The tool processes each configured repository and writes results to `data/outputs/`.

## Project Structure

```
src/
├── main.py                 # Assessment pipeline entry point
├── generators.py           # Criteria generators and helpers (tiers, aggregation logic, instructions)
├── output_parsers.py       # Pydantic models for structured LLM output
├── report.py               # Markdown report generation
├── logger.py               # Logging setup
├── config/
│   ├── config.json         # Run configuration (URLs, workers, local project mode)
│   ├── paths.py            # Centralized path definitions
│   ├── prompts.yaml        # LLM prompts for metadata and file scoring
│   ├── tracked_files.yaml  # Tracked/text extensions and ignored file names
│   ├── logic_based_scoring.py  # Deterministic scoring functions
│   └── scoring/            # Criteria definitions per category (YAML)
├── directory_scorer/
│   ├── content_based_scorer.py  # Per-file LLM scoring and score aggregation
│   └── tree.py             # Repository tree building
└── utils/
    ├── llm.py              # LLM configuration (OpenAI / OpenRouter)
    ├── repository.py       # Repo download/clone and tree utilities
    ├── project_validators.py   # File-presence and metadata checks
    └── general.py          # File I/O and misc utilities
```

## Key Libraries

- **LangChain** & **LangChain-OpenAI** — LLM orchestration and structured output
- **GitPython** & **requests** — repository cloning and zip downloads
- **pypdf** — PDF document loading during content-based scoring
- **pandas** — data handling
- **pytest** — test suite (`tests/`); run with `make test` or `uv run pytest tests/`
- **mypy** — static type checking (dev dependency)

## Testing

```bash
make test
```

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
