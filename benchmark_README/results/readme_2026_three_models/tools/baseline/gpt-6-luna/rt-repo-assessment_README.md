# RT Repository Assessment

RT Repository Assessment evaluates Python and AI/ML project repositories against configurable quality criteria. It combines deterministic checks of repository metadata with language-model evaluations of project documentation and tracked file contents. Results are written as JSON files and a Markdown report for each assessed project.

Criteria are organized around code quality, dependencies, licensing, repository structure, and documentation. The scoring definitions and prompts are stored under `src/config/`, so the assessment can be adjusted by editing project configuration files rather than changing the scoring pipeline.

## How it works

For each project, the application collects metadata such as the presence of a README, dependency files, a license, and a `.gitignore`, along with script lengths and a directory tree. It applies custom logic to selected checks, then uses an LLM for criteria based on project metadata and file content. File assessments are combined according to the aggregation rule configured for each criterion (`OR` or `AND`).

The report groups criteria into Essential, Professional, and Elite tiers. File-level and project-level results are also retained as JSON.

## Requirements

- Python **3.12 or later, and below 4.0**.
- [`uv`](https://docs.astral.sh/uv/) for environment and dependency management.
- Credentials for the chat model provider used by LangChain’s `ChatOpenAI`. The application can also use OpenRouter when `OPEN_ROUTER_API_KEY` is set.
- Git is used by the repository-cloning path.

## Setup

Clone this repository, move into its root directory, and install the project dependencies:

```bash
uv sync
```

The Makefile provides the equivalent installation target:

```bash
make install
```

The project loads environment variables from a `.env` file. Configure the credentials required by `ChatOpenAI` in your environment or `.env`. To route requests through OpenRouter, set `OPEN_ROUTER_API_KEY`; when that variable is present, the LLM utility configures the OpenAI-compatible OpenRouter API endpoint. Do not commit real credentials. The repository includes an `.env.example` file, but its contents are not documented here.

## Configuration

The main runtime configuration is `src/config/config.json`:

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

- **`from_inputs_directory`** selects whether to assess a project already in `data/inputs` or to process repository URLs.
- **`project_name`** is the directory name to use under `data/inputs` when assessing a local project.
- **`urls`** lists the repositories to process when `from_inputs_directory` is `false`.
- **`max_workers`** sets the worker limit used for parallel scoring.

For a local assessment, create `data/inputs/<project_name>/`, place the project files there, and set `from_inputs_directory` to `true`. For URL-based assessment, provide the repository URLs in `urls`. The application checks repository visibility and uses its download or Git-clone path accordingly; URL-based processing is implemented for repositories including GitHub.

Additional settings are in `src/config/`:

- `prompts.yaml` contains the prompts used for project-level and file-level scoring.
- `scoring/` contains YAML criteria definitions, including criterion names, instructions, tier membership, file-extension filters, and aggregation rules.
- `tracked_files.yaml` specifies file extensions to inspect, text extensions, script extensions, and names to ignore during file scoring.

Edit these files to adjust assessment criteria, prompts, or tracked-file behavior. The models configured in `src/utils/llm.py` include `gpt-4o-mini`, `gpt-4o`, and `gpt-4.1-mini`; the main assessment uses `gpt-4o-mini`.

## Run an assessment

After setting credentials and editing `src/config/config.json` for the desired input mode, run:

```bash
uv run python src/main.py
```

The entry point reads the JSON configuration and scoring prompts, processes each configured project, and creates an output directory under `data/outputs/` using the project directory’s name. Each assessment produces:

- `assessment.json` — criterion results, including scores and explanations.
- `file_scores.json` — per-file scoring results.
- `report.md` — a human-readable quality assessment report.

Scores are represented as `0` or `1`, with an explanation for each criterion. Files that are empty or exceed the configured token limit may be skipped during file-level scoring; errors encountered while scoring individual files are logged.

## Project layout

- `src/main.py` — assessment entry point and orchestration.
- `src/generators.py` — loads and filters criteria from YAML.
- `src/config/` — runtime configuration, prompts, paths, and scoring definitions.
- `src/directory_scorer/` — builds a tracked file tree, scores files, and combines results.
- `src/utils/` — repository operations, project checks, LLM access, and common file helpers.
- `src/report.py` — writes the Markdown report.
- `data/inputs/` — local projects and downloaded or cloned repositories.
- `data/outputs/` — generated assessment artifacts.
- `tests/` — automated tests.
- `pyproject.toml` and `uv.lock` — project metadata, dependencies, and locked environment.

## Development and testing

Install the development dependency group along with the project dependencies using `uv sync`. The project includes `mypy` in its development dependency group. No separate lint or type-check command is defined in the supplied project files.

Run the test suite with:

```bash
uv run pytest tests/
```

Or use the Makefile target:

```bash
make test
```

The current tests cover repository validator behavior, including detection of README, requirements, setup, license, and `.gitignore` files. Tests use temporary directories and clean them up after execution.

When changing criteria or prompts, verify that criterion identifiers remain consistent with any custom scoring logic and that generated results continue to include the expected score and explanation fields.

## License

This project is licensed under the **MIT License**. See [`LICENSE`](LICENSE) for the full license text and copyright notice.
