# Repository Assessment

Repository Assessment analyzes configured code repositories against criteria for code quality, dependencies, licensing, repository structure, and documentation. It combines local checks and repository metadata with language-model evaluations of repository information and selected file contents. Results are written as JSON scores and a Markdown report.

## How it works

The assessment is configured in `src/config/config.json`. By default, the program obtains each repository listed in `urls`, places it under `data/inputs/`, collects repository metadata and a directory tree, and evaluates criteria defined in `src/config/scoring/`. File-content criteria and metadata criteria use the configured language model; criteria marked for custom logic are checked by local Python functions. File extensions and names considered during file scoring are configured in `src/config/tracked_files.yaml`.

For each project, the program writes:

- `data/outputs/<project>/assessment.json` — criterion scores and explanations, including aggregated file-based scores.
- `data/outputs/<project>/file_scores.json` — individual file scoring results.
- `data/outputs/<project>/report.md` — a Markdown report with an overall summary and criterion breakdown.

## Requirements

- Python `>=3.12,<4.0` (the checked-in `.python-version` specifies Python 3.12).
- [uv](https://docs.astral.sh/uv/) to install and run the project.
- An API key for OpenAI or OpenRouter. The assessment uses `gpt-4o-mini`.
- Network access when assessing repositories by URL or making model requests.

## Installation

From the repository root, synchronize the locked dependencies:

```bash
uv sync
```

Create a local environment file and replace the placeholder value with a real key for the provider you intend to use:

```bash
cp .env.example .env
```

Set `OPENAI_API_KEY` to use OpenAI, or `OPEN_ROUTER_API_KEY` to use OpenRouter. If `OPEN_ROUTER_API_KEY` is present, the application configures the OpenAI-compatible client to use OpenRouter.

## Configure a run

Edit `src/config/config.json` before running:

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

- With `from_inputs_directory` set to `false`, the application assesses the repositories in `urls` and stores downloaded or cloned repositories in `data/inputs/`.
- With `from_inputs_directory` set to `true`, it assesses the existing directory `data/inputs/<project_name>` instead. That directory must already exist; the URL list is not used in this mode.
- `max_workers` controls the worker count used for parallel criterion and file processing.

Assessment criteria, prompts, and the file selection rules are under `src/config/`. Adjust them there to change what the program evaluates.

## Run

Run the assessment from the repository root:

```bash
uv run python src/main.py
```

The program processes each configured project and writes its outputs beneath `data/outputs/`.

## Tests

Run the test suite with either command:

```bash
uv run pytest tests/
```

```bash
make test
```

The tests currently cover repository project-file validators.

## Repository layout

```text
.
├── data/
│   ├── inputs/       # Repositories to assess, including URL-fetched repositories
│   └── outputs/      # Generated assessment results
├── src/
│   ├── config/       # Runtime settings, prompts, file rules, and scoring criteria
│   ├── directory_scorer/  # File selection and content-based scoring
│   ├── utils/        # Repository, model, and project-validation helpers
│   ├── main.py       # Assessment entry point
│   └── report.py     # Markdown report generation
├── tests/            # Pytest tests
├── .env.example      # API-key variable names
├── Makefile          # Install and test targets
├── pyproject.toml    # Package metadata and dependencies
└── uv.lock           # Locked dependency versions
```

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for the full text.
