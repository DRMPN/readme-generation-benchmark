# GPT Engineer

GPT Engineer is a Python command-line tool that takes a natural-language description of an application, optionally asks clarifying questions, and then uses a large language model (LLM) to generate the project's code. It can also improve an existing project from a new instruction. The package is published as `gpt-engineer` (version 0.3.1) under the MIT License.

## Overview

GPT Engineer works on a project folder. You place a `prompt` file in the folder describing what you want, and the tool:

- Sends the prompt, along with preprompt instructions, to an LLM (OpenAI models by default).
- Parses the response into files and writes them into the project.
- Optionally runs the generated entrypoint, and can attempt to repair it if it fails.
- Records logs and memory in a `.gpteng` folder inside the project.

The project includes several operating modes:

- **Generate** (default): creates a new project from `prompt`.
- **Improve** (`-i`): modifies existing files based on a new prompt, using diffs and an interactive file selector.
- **Lite** (`-l`): generates code using only the main prompt.
- **Clarify** (`-c`): discusses the specification with the AI before implementation.
- **Self-heal** (`-sh`): runs the generated code and asks the AI to fix failures.

The repository also contains a benchmarking tool (`bench`) that runs an agent against the APPS and MBPP benchmarks, and a Sphinx documentation set.

## Installation

### Requirements

- Python `>=3.10,<3.13` (as declared in `pyproject.toml`).
- [Poetry](https://python-poetry.org/) for development installs. The CI and Makefile use it.
- Git is optional. The CLI checks whether Git is installed and initializes a repository in the project folder when it is available.
- An OpenAI API key, or another supported model endpoint (see [Configuration](#configuration)).
- For Docker: Docker, and optionally Docker Compose.

### From a package

The documentation recommends:

```bash
python -m pip install gpt-engineer
```

### From source (development)

```bash
git clone https://github.com/gpt-engineer-org/gpt-engineer.git
cd gpt-engineer
make install        # runs `poetry install` and `pre-commit install`
poetry shell
```

Running `make` with no target prints the available targets (`help`, `install`, `run <folder_name>`).

### Docker

Using the Docker CLI:

```bash
docker build --rm -t gpt-engineer -f docker/Dockerfile .
docker run -it --rm -e OPENAI_API_KEY="YOUR_OPENAI_KEY" -v ./your-project:/project gpt-engineer
```

Using Docker Compose:

```bash
docker-compose -f docker-compose.yml build
docker-compose run --rm gpt-engineer
```

`docker-compose.yml` reads the API key from a `.env` file, or it can be set directly in the `environment` section. It mounts `./projects/example` to `/project`. The container entrypoint runs `gpt-engineer /project` and then changes ownership and permissions of generated files, leaving the `prompt` file unchanged.

To open a shell in the image for debugging:

```bash
docker run -it --entrypoint /bin/bash gpt-engineer
```

### Windows

`WINDOWS_README.md` describes setup on Windows, including setting the key with `set OPENAI_API_KEY=...` in cmd or `$env:OPENAI_API_KEY="..."` in PowerShell, and creating project folders with `xcopy /E projects\example projects\my-new-project`.

## Usage

### Generating a project

1. Create an empty folder for your project.
2. Create a file named `prompt` (no extension) in that folder and describe the application.
3. Run the CLI with the folder path:

```bash
gpte projects/my-new-project
```

The CLI also installs the aliases `gpt-engineer` and `ge`. Generated files are written to the project; the Windows guide also refers to a `workspace` folder for results.

### Improving an existing project

```bash
gpte projects/my-old-project -i
```

Write the change request in the `prompt` file. In improve mode, the CLI shows a file selector (which can be skipped with `-s`), shows the proposed changes, and asks for confirmation before applying them.

### Using the Makefile

```bash
make run my-new-project    # runs: poetry run gpt-engineer projects/my-new-project
```

### Command-line options

These options come from `gpt_engineer/applications/cli/main.py`:

| Option | Purpose |
|---|---|
| `project_path` | Project folder (default `.`). |
| `-m, --model` | Model ID. Defaults to the `MODEL_NAME` environment variable, or `gpt-4o`. |
| `-t, --temperature` | Sampling temperature (default `0.1`). |
| `-i, --improve` | Improve an existing project. |
| `-l, --lite` | Generate using only the main prompt. |
| `-c, --clarify` | Clarify the specification with the AI first. |
| `-sh, --self-heal` | Attempt to fix the code when execution fails. |
| `-a, --azure` | Azure OpenAI endpoint; the model value is then the deployment name. |
| `--use-custom-preprompts` | Use the project's own preprompts, copying defaults where missing. |
| `--llm-via-clipboard` | Exchange messages with the AI through the clipboard. |
| `-v, --verbose` | Verbose logging. |
| `-d, --debug` | Debug mode (starts `pdb` on uncaught exceptions). |
| `--prompt_file` | Path to the prompt file (default `prompt`). |
| `--entrypoint_prompt` | File with requirements for the entrypoint. |
| `--image_directory` | Folder of images to include in the prompt. |
| `--use_cache` | Cache LLM responses in `.langchain.db`. |
| `-s, --skip-file-selection` | Skip the interactive file selector in improve mode. |
| `--no_execution` | Run setup without calling the LLM or writing code (for testing). |
| `--sysinfo` | Print system information for bug reports. |
| `--diff_timeout` | Timeout in seconds for diff regex parsing (default `3`). |

Some options are incompatible: clarify and lite modes cannot be combined with improve mode.

After a run, the CLI prints the total API cost for OpenAI models, or a notice that a local LLM was used when `LOCAL_MODEL` is set.

### Running benchmarks

The `bench` command runs an agent against benchmarks:

```bash
bench path/to/agent.py [bench_config] [--yaml-output PATH] [--verbose] [--use-cache/--no-use-cache]
```

The agent file must define a function named `default_config_agent`. The help text states that the available benchmarks are `apps` and `mbpp`; `default_bench_config.toml` also contains a `gptme` section. Results are printed per benchmark and can be written to YAML.

### Example projects

- `projects/example-improve/` contains a Snake game split into `main.py`, `model.py`, `view.py`, and `controller.py`, with a `prompt` for improvement, a `requirements.txt` (`keyboard==0.13.5`), and a `run.sh` script.
- `projects/example-vision/` contains a `navigation.html` file and a `prompt`, with a UX diagram image.

The example commands in the Docker files and Makefile refer to `projects/example`; that folder is not included in the supplied file listing.

## Configuration

### Model and API keys

- `OPENAI_API_KEY` is required for OpenAI models. The CLI loads it from the environment, or from a `.env` file in the working directory. Copy `.env.template` to `.env` to start.
- `ANTHROPIC_API_KEY` is loaded the same way, and Claude models are supported through `langchain-anthropic`.
- `MODEL_NAME` sets the default model for `--model`.
- `OPENAI_API_VERSION` sets the Azure API version (default `2024-05-01-preview` in `ai.py`).
- `LOCAL_MODEL` changes the cost output for local LLMs.
- `OPENAI_API_BASE` redirects requests to an OpenAI-compatible server.

### Local and alternative models

`docs/open_models.md` describes using `llama-cpp-python`'s server with GGUF models. The documented steps are to set `OPENAI_API_BASE="http://localhost:8000/v1"`, a dummy `OPENAI_API_KEY`, `MODEL_NAME`, and `LOCAL_MODEL=true`, then run with `--lite --temperature 0.1`. The guide also covers OpenRouter (`https://openrouter.ai/api/v1`) and Azure (`--azure <endpoint>` with the deployment name as the model).

### Project configuration

`gpt-engineer.toml` is read and written by `gpt_engineer/core/project_config.py`. It supports these sections:

- `[run]`: `build`, `test`, `lint`, and `format` commands.
- `[paths]`: `base` (for monorepos) and `src`.
- `[gptengineer-app]`: a required `project_id` when the section is present, plus optional `openapi` URLs.

### Preprompts

Default prompts live in `gpt_engineer/preprompts/` (`clarify`, `entrypoint`, `file_format`, `file_format_diff`, `file_format_fix`, `generate`, `improve`, `philosophy`, `roadmap`). Use `--use-custom-preprompts` to copy them into a project's `preprompts` folder and customize them.

### Benchmark configuration

`gpt_engineer/benchmark/default_bench_config.toml` sets `active` flags and index ranges for the `apps`, `mbpp`, and `gptme` benchmarks.

### Tracing (optional)

`docs/tracing_debugging.md` describes sending traces to Weights & Biases by setting `WANDB_API_KEY` and `LANGCHAIN_WANDB_TRACING=true`.

### Data collection

According to `TERMS_OF_USE.md`, usage data is collected only when a `.gpte_consent` file is present in the gpt-engineer directory. The terms also state that data streams may be stored by third parties such as OpenAI.

### Logs and memory

Runs store memory in `.gpteng/memory` inside the project. The bug report template asks users to upload `debug_log_file.txt` from that location.

## Development

### Project layout

- `gpt_engineer/applications/cli/`: CLI entry point, the agent, the file selector, and feedback collection.
- `gpt_engineer/core/`: AI wrapper (`ai.py`), diff parsing and validation (`chat_to_files.py`, `diff.py`), file dictionaries, Git helpers, linting, token accounting, and project configuration.
- `gpt_engineer/core/default/`: default agent, steps, disk-based memory, and execution environment.
- `gpt_engineer/tools/`: custom steps (`lite_gen`, `clarified_gen`, `self_heal`) and supported languages.
- `gpt_engineer/benchmark/`: benchmark runner, configuration, and APPS/MBPP loaders.
- `docs/`: Sphinx documentation; `create_api_rst.py` generates `api_reference.rst`.
- `scripts/`: helper scripts for benchmarks, chat printing, and API testing.

### Tooling

- **Makefile**: `install`, `run <folder_name>`, and `cloc` for line counts.
- **pre-commit** (`.pre-commit-config.yaml`): `black` 23.3.0, `ruff` v0.0.272, and standard checks for TOML, YAML, private keys, end-of-file newlines, and trailing whitespace. Run `pre-commit run --all-files` before opening a pull request.
- **Ruff and Black** settings are in `pyproject.toml`, targeting Python 3.10.
- **Poetry** manages dependencies (`pyproject.toml`, `poetry.lock`).

### Contributing

`.github/CONTRIBUTING.md` describes the contribution process: fork, branch, make changes, run tests, and submit a pull request to `main`. Changes that are likely to introduce breaking changes or significantly alter the user experience require board approval under `GOVERNANCE.md`. Cosmetic-only changes are generally not merged. Contributors agree that their work is licensed under the project's MIT license.

Other community files include `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), issue and pull request templates, `CODEOWNERS`, `ROADMAP.md`, and `GOVERNANCE.md`.

### Documentation

Install the docs extras with Poetry and build locally:

```bash
poetry install --with docs
cd docs/
python create_api_rst.py
make html
```

`sphinx-autobuild . _build/html` rebuilds the docs on changes. `.readthedocs.yaml` configures Read the Docs builds.

## Testing

Tests live in `tests/` and use pytest. Coverage is collected with `pytest-cov`.

Run the suite directly:

```bash
poetry run pytest --cov=gpt_engineer
```

The `tox.ini` file defines environments for Python 3.10, 3.11, and 3.12. Each runs `poetry install --no-root` and then:

```bash
poetry run pytest --cov=gpt_engineer --cov-report=xml -k 'not installed_main_execution'
```

The GitHub Actions workflow `ci.yaml` runs tox on pushes to `main` that touch `gpt_engineer/**` or `tests/**`, and on pull requests to `main`. It passes `OPENAI_API_KEY` from repository secrets.

Notes on the test suite:

- Tests marked `requires_key` need a valid `OPENAI_API_KEY`. Deselect them with `-m "not requires_key"`.
- `tests/mock_ai.py` provides a mock AI for offline tests, and `tests/ai_cache.json` contains cached model interactions.
- `tests/core/improve_function_test_cases/` holds chat and code fixtures for diff parsing.
- `tests/test_install.py` creates a temporary virtual environment and installs the package with Poetry.

## Releases

`.github/workflows/release.yaml` builds the package with Poetry (source distribution only) and publishes to PyPI when a release is published or the workflow is run manually. `automation.yml` marks stale issues after 60 days.

## License

GPT Engineer is released under the MIT License. Copyright (c) 2023 Anton Osika. The full text is in the `LICENSE` file.

Related notices in the repository:

- `DISCLAIMER.md` states that the software is provided "as-is," that users are responsible for their LLM token usage and costs, and that generated code must be reviewed for legal and ethical compliance.
- `TERMS_OF_USE.md` describes data handling and the consent file mechanism.
- `Acknowledgements.md` credits Paul Gauthier and Aider for the basis of the `improve` prompt.
