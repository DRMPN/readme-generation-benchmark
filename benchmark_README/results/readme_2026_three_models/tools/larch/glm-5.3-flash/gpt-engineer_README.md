# GPT Engineer

<p align="center">
  <b>Specify what you want it to build, the AI asks for clarification, and then builds it.</b>
</p>

<p align="center">
  <a href="https://github.com/gpt-engineer-org/gpt-engineer/stargazers"><img src="https://img.shields.io/github/stars/gpt-engineer-org/gpt-engineer" alt="GitHub Repo stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License: MIT"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Linting: Ruff"></a>
  <a href="https://discord.gg/A6kU6tPWA8"><img src="https://img.shields.io/discord/1101404903138488320?label=Discord&logo=discord" alt="Discord"></a>
</p>

**GPT Engineer** (`gpte`) generates an entire codebase from a single prompt, then helps you iterate on it with feedback. It is designed to be easy to adapt, extend, and *teach* — so your agent learns how you want your code to look.

This repository contains the complete project: the core agent library, the `gpte` CLI, an experimental web UI, a benchmarking framework, Sphinx documentation, Docker support, and a full test suite.

---

## Table of Contents

- [Community](#community)
- [Features](#features)
- [Philosophy & Vision](#philosophy--vision)
- [How It Works](#how-it-works)
- [Quickstart](#quickstart)
- [Running on Windows](#running-on-windows)
- [Running with Docker](#running-with-docker)
- [Agents & Steps](#agents--steps)
- [Preprompts](#preprompts)
- [Experimental Features](#experimental-features)
- [Experimental Web UI](#experimental-web-ui)
- [Open-Source & Local Models](#open-source--local-models)
- [Caching, Tracing & Token Usage](#caching-tracing--token-usage)
- [Benchmarks](#benchmarks)
- [Feedback Collection (Learning)](#feedback-collection-learning)
- [Documentation](#documentation)
- [Development](#development)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Governance, Code of Conduct & Legal](#governance-code-of-conduct--legal)
- [Acknowledgements](#acknowledgements)
- [License](#license)
- [Citation](#citation)

## Community

Come say hi and share your projects in the [gpt-engineer Discord](https://discord.gg/A6kU6tPWA8)! We also have a mentorship channel for first-time contributors — see [Contributing](#contributing).

## Features

- 🧱 **Codebase generation** — write one `prompt` file, get a full project scaffolded and executed.
- 🔁 **Iterative improvement** — run `gpte -i` in an existing project to fix bugs and add features from natural-language feedback.
- 🗣️ **Clarification step** — when your prompt is ambiguous, the agent asks targeted questions before writing code.
- 🤖 **Multiple LLM backends** — OpenAI (default), Anthropic, and open-source/local models via [LangChain](https://python.langchain.com/).
- 🧩 **Fully customizable** — swap models, tune temperature, edit preprompts, or write your own custom steps.
- 🗂️ **Project-aware context** — a file selector helps pick the right files when improving existing code.
- 🌿 **Git snapshots** — every generation step is committed locally so you can diff and roll back safely.
- 📊 **Benchmarks** — evaluate agents and models on bundled problems, with regression fixtures.
- 🪟 **Windows & Docker friendly** — dedicated Windows guide and container images.

## Philosophy & Vision

Three guiding principles:

1. **Flexibility through prompting.** The code-generation process should be easy to understand, adapt, and extend. The pipeline is plain Python and its behavior is steered by editable preprompts (see the `philosophy` preprompt itself).
2. **"Everything at once" vs. step-by-step.** Generating whole systems in one shot lets the model explore the design space before committing to details; quality is then verified and improved iteratively.
3. **A flexible, interactive feedback loop.** The tool is built around human feedback: clarify the spec, run the code, request improvements.

The long-term vision and release plans live in [ROADMAP.md](ROADMAP.md).

## How It Works

At a high level, `gpte` runs this loop:

1. **Clarify** — the agent asks clarifying questions if the prompt is underspecified.
2. **Plan / generate** — a specification is drafted and the codebase is generated.
3. **Execute** — the project's entrypoint is run and its output is captured; on errors, the agent iterates to fix them.
4. **Improve** — you give feedback; the agent produces diffs that are applied to the code.

Everything happens inside your project folder, and each step is snapshotted with git so you can inspect or undo changes.

> ⚠️ **Note:** `gpte` writes and *executes* generated code on your machine. Always review the code it produces.

### Core components

| Module | Role |
|---|---|
| `core/ai.py` | LLM wrapper (OpenAI / LangChain), message history, response caching, token accounting |
| `core/simple_agent.py`, `core/steps.py` | The default deterministic step pipeline |
| `base_agent.py`, `base_memory.py`, `base_execution_env.py` | Interfaces for agents, memory, and code execution |
| `disk_memory.py`, `disk_execution_env.py`, `file_store.py` | Filesystem-backed memory, file store, and execution environment |
| `chat_to_files.py`, `diff.py`, `files_dict.py` | Parse LLM chat output into files; apply diffs (with fallback logic that salvages correct hunks from imperfect ones) |
| `git.py`, `version_manager.py` | Automatic git snapshots for every generation step |
| `prompt.py` | Reads and validates your `prompt` file |
| `preprompts_holder.py` | Loads the preprompt texts |
| `linting.py` | Static checks on generated code |
| `token_usage.py` | Token usage accounting |
| `project_config.py`, `paths.py`, `constants.py` | Per-project configuration, folder layout (`.gpteng/`), defaults |

## Quickstart

### Requirements

- Python **3.10+**
- `pip` (or [Poetry](https://python-poetry.org/) for development)
- An LLM API key (OpenAI by default)

### Installation (stable)

```bash
pip install gpt-engineer
```

This installs the `gpte` command-line tool.

### Installation (development)

```bash
git clone https://github.com/gpt-engineer-org/gpt-engineer.git
cd gpt-engineer
poetry install
poetry shell
```

### Configuration

Export your API key:

```bash
export OPENAI_API_KEY=[your api key]
```

…or place it in a `.env` file in the repo root:

```
OPENAI_API_KEY=your-key
```

To use Anthropic models, set `ANTHROPIC_API_KEY` instead (see [Open-Source & Local Models](#open-source--local-models) for other providers).

> 💡 Strong models (`gpt-4o`, `gpt-4-turbo`, Claude 3 class) give the best results. Generation runs can cost a few dollars in API fees — monitor your usage.

### Run — generate a new codebase

Create a project folder containing a `prompt` file:

```bash
mkdir -p projects/my-idea
cat > projects/my-idea/prompt <<'EOF'
Make a snake game with HTML/JS on a canvas.
The snake speeds up as it eats food.
Include a start menu and a game-over screen.
EOF
```

Then run:

```bash
gpte projects/my-idea
```

The agent clarifies your idea, generates the code, writes it to the project folder, and executes the entrypoint.

### Run — improve an existing codebase

Point `gpte` at a folder that already contains code, and describe the changes in its `prompt` file:

```bash
gpte projects/my-existing-project -i
```

In improve mode, the file selector (`file_selector.py`) lets you choose which files to include in the agent's context.

### Common CLI options

| Option | Description |
|---|---|
| `PROJECT_PATH` | Path to the project folder containing the `prompt` file |
| `-i`, `--improve` | Improve an existing codebase instead of generating a new one |
| `-m`, `--model` | Model to use (e.g. `gpt-4o`, `gpt-4-turbo`, a Claude model, or a local model) |
| `-t`, `--temperature` | LLM temperature (default `0.1`) |
| `--use-cache` / `--no-use-cache` | Cache LLM responses to disk for reproducible, cheaper re-runs |
| `-v`, `--verbose` | Verbose logging |
| `--help` | Full, up-to-date list of options |

## Running on Windows

Windows-specific setup instructions (environment setup, path handling, alternatives to `make`, etc.) are collected in [WINDOWS_README.md](WINDOWS_README.md). The Sphinx docs also ship a `make.bat` for building documentation on Windows.

## Running with Docker

The repo ships a `Dockerfile`, `docker-compose.yml`, and `entrypoint.sh`:

```bash
# Using docker compose
docker compose build
docker compose run --rm gpte projects/example

# Or manually
docker build -t gpt-engineer .
docker run --rm -it \
  --env OPENAI_API_KEY \
  --volume "$(pwd)/projects:/projects" \
  gpt-engineer gpte /projects/example
```

## Agents & Steps

`gpte` ships with multiple agent implementations:

- **Simple agent** (default) — a fixed pipeline defined in `steps.py`:
  1. **Clarify** — ask the user clarifying questions when needed.
  2. **Plan/Spec** — draft a specification for the task.
  3. **Code** — generate the codebase files.
  4. **Execute** — run the entrypoint; capture errors and iterate.
  5. **Improve** — apply user feedback as diffs.
- **Legacy steps** — the original "spec → unit tests → code" pipeline from early releases, kept for reference and benchmarking.
- **CLI agent** (`cli_agent.py`, experimental) — a tool-using agent that reads/writes files and runs commands in an agentic loop.

Because steps are plain Python functions, you can compose your own pipelines — see `experimental/custom_steps.py`.

## Preprompts

Agent behavior is largely defined by plain-text preprompts in the `preprompts` folder:

| File | Used for |
|---|---|
| `philosophy` | The coding philosophy the agent follows |
| `clarify` | How and when to ask clarifying questions |
| `generate` | Core instructions for generating the codebase |
| `improve` | Instructions for improving existing code |
| `file_format` | Output format for generated files |
| `file_format_diff` | Output format for diffs |
| `file_format_fix` | Repairing malformed file output |
| `roadmap` | Development roadmap hints |
| `entrypoint` | How to detect and run the project entrypoint |

Edit these files to teach your agent your preferred conventions, frameworks, and file layout.

## Experimental Features

Features marked experimental may change without notice:

- **Custom steps** — `experimental/custom_steps.py` shows how to build your own generation pipelines.
- **More languages** — `experimental/supported_languages.py` extends scaffolding beyond the default stack.
- **CLI agent** — the tool-using agent described above.
- **Web UI** — see below.

## Experimental Web UI

A lightweight MVC web interface is included (alpha quality):

- `model.py`, `view.py`, `controller.py` — the MVC application core
- `openai_api_interface.py`, `langchain_interface.py` — pluggable LLM backends
- `navigation.html`, `ux_diagram.png` — navigation mockups and a UX diagram
- `run.sh`, `requirements.txt` — how to start it

Start it with:

```bash
./run.sh
```

## Open-Source & Local Models

`gpte` can run on non-OpenAI backends, including Anthropic models and self-hosted open-source models (e.g. via Ollama, vLLM, llama.cpp, or any OpenAI-compatible endpoint), thanks to the LangChain integration. See [`docs/open_models.md`](docs/open_models.md) for configuration examples.

## Caching, Tracing & Token Usage

- **Response caching** — enable `--use-cache` to persist LLM responses (e.g. `ai_cache.json`) so that re-runs are deterministic and cheap.
- **Token usage** — `token_usage.py` tracks cumulative token consumption per session.
- **Tracing & debugging** — see [`docs/tracing_debugging.md`](docs/tracing_debugging.md) for tracing LLM calls and diagnosing agent behavior.

## Benchmarks

The repository includes a benchmark framework (`gpt_engineer/benchmark/`) for regression-testing agent changes and comparing models/settings:

- **Framework** — `problem.py`, `problems.py`, `load.py`, `types.py` define problems, datasets, and result types.
- **Configuration** — `bench_config.py` and `default_bench_config.toml` select models, agent steps, and problem subsets.
- **Fixtures** — bundled reference artifacts `*_chat` (example conversations) and `*_code` (generated code snapshots) for problems such as `simple_calculator`, `temperature_converter`, `task_master`, `snake`, `apps_benchmark_6` (and `_v2`), `zbf_yml_missing`, plus community-contributed cases (`wheaties_example`, `vgvishesh_example*`, `theo_case`).
- **Utilities** — `legacy_benchmark.py` (the historical runner), `clean_benchmarks.py`, `print_chat.py` (pretty-print stored chats), and `test_api.py` (quick API connectivity check).

Run the suite with:

```bash
python -m gpt_engineer.benchmark
```

## Feedback Collection (Learning)

Because `gpte` is research software, the CLI may ask for your **explicit consent** before collecting feedback:

- `learning.py` stores learnings locally.
- `collect.py` handles optional (consent-based) sharing with the team for research.

Consent handling is covered by dedicated tests (`test_collection_consent.py`, `test_learning.py`, `test_collect.py`). Declining is always fine.

## Documentation

Full Sphinx documentation lives in [`docs/`](docs/):

- `introduction.md`, `quickstart.rst`, `installation.rst` — getting started
- `open_models.md` — using open-source/local models
- `tracing_debugging.md` — tracing and debugging agent runs
- `docs_building.md` — how to build the docs
- `api_reference.rst` — auto-generated API reference (via `create_api_rst.py`)
- `index.rst`, `conf.py`, `Makefile`, `make.bat`, and link stubs for roadmap/terms/conduct/disclaimer pages

Build the docs locally:

```bash
cd docs
python create_api_rst.py   # regenerate the API reference
make html                  # Linux/macOS  (or .\make.bat html on Windows)
```

## Development

### Setup

```bash
git clone https://github.com/gpt-engineer-org/gpt-engineer.git
cd gpt-engineer
poetry install
poetry shell
```

Packaging is defined in `pyproject.toml` (with `poetry.lock` for reproducible environments); `MANIFEST.in` controls distribution contents.

### Running tests

The pytest suite under `tests/` covers the CLI, agents and steps, diff parsing, git integration, file selection, project config, benchmark configuration, learning/consent flow, installation, and token usage. LLM calls are mocked via `mock_ai.py`, so tests run without spending API credits.

```bash
poetry run pytest          # run the test suite
poetry run tox             # lint + type-check + tests matrix (tox.ini)
```

### Code style

Formatting and linting use **black** and **ruff**; `pre-commit` hooks are recommended. The root `Makefile` provides convenience targets for common development tasks.

## Project Structure

(abbreviated)

```
gpt-engineer/
├── gpt_engineer/              # The Python package
│   ├── core/                  # Agents, steps, AI wrapper, memory, execution, git, diffs
│   ├── cli/                   # The `gpte` CLI: main.py, cli_agent.py, file_selector.py, …
│   ├── benchmark/             # Benchmark framework, configs, problems & fixtures
│   ├── preprompts/            # Editable prompt texts (clarify, generate, improve, …)
│   └── experimental/          # custom_steps.py, supported_languages.py
├── app/                       # Experimental web UI (model / view / controller)
├── docs/                      # Sphinx documentation
├── projects/                  # Your projects + bundled examples (snake game, …)
├── tests/                     # pytest suite (+ mock_ai.py)
├── Dockerfile / docker-compose.yml / entrypoint.sh
├── pyproject.toml / poetry.lock / tox.ini / Makefile / MANIFEST.in
└── LICENSE / ROADMAP.md / GOVERNANCE.md / WINDOWS_README.md / citation.cff
```

## Contributing

Contributions are very welcome!

- Look for issues labeled as good first issues, or bring your own ideas.
- The `sweep.yaml` config enables [Sweep](https://sweep.dev/) to draft PRs from suitable GitHub issues.
- For significant changes, please open an issue first to discuss the design.
- Make sure `pytest` and the linters pass before submitting a PR.

## Governance, Code of Conduct & Legal

- Project decision-making and maintainer responsibilities are described in [GOVERNANCE.md](GOVERNANCE.md).
- Please review [TERMS_OF_USE.md](TERMS_OF_USE.md) and [DISCLAIMER.md](DISCLAIMER.md) before using the tool. In short: you are responsible for the code the agent generates and executes on your machine.

## Acknowledgements

Thanks to everyone who has contributed code, ideas, benchmark problems, and feedback — see [Acknowledgements.md](Acknowledgements.md).

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).

## Citation

If you use GPT Engineer in your research, please cite it (see [citation.cff](citation.cff)):

```bibtex
@software{gpt_engineer,
  author = {Osika, Anton and the GPT Engineer contributors},
  title  = {GPT Engineer},
  year   = {2023},
  url    = {https://github.com/gpt-engineer-org/gpt-engineer},
}
```
