# gpt-engineer

> **Note:** The file listing you provided is flattened, so some directory boundaries are inferred. Flags, commands, and paths below reflect the gpt-engineer project as commonly documented. Verify them against the source before relying on them.

gpt-engineer is a Python CLI tool that generates and iteratively improves entire codebases from a natural-language prompt. You describe what you want in a plain-text file, and the tool asks a large language model (LLM) to plan, write, and revise the project's files. It can also improve existing code, run a clarification dialogue with you, and benchmark different models and prompts against a set of coding problems.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Layout](#project-layout)
- [Configuration](#configuration)
- [Prompt Engineering Tips](#prompt-engineering-tips)
- [Using Docker](#using-docker)
- [Benchmarking](#benchmarking)
- [Running Tests](#running-tests)
- [Building the Documentation](#building-the-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Governance, Legal, and Citation](#governance-legal-and-citation)
- [Roadmap](#roadmap)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## Features

- **Prompt-to-project generation.** Write a `prompt` file describing your application and get a full set of source files, dependencies, and run instructions.
- **Iterative improvement.** Run the tool on an existing project to add features or fix issues.
- **Clarification step.** The agent can ask follow-up questions before generating code to reduce ambiguity.
- **Structured file output.** Model responses are parsed into a file dictionary and written to disk, with diff-based updates supported for edits.
- **Git integration.** Changes can be versioned so you can review or revert what the AI did.
- **Execution environment.** Generated code can be executed and linted to check for errors, which feeds back into the next revision.
- **Memory and caching.** Conversations and responses can be stored and reused, reducing API cost during iteration.
- **Pluggable LLM backends.** Supports OpenAI and compatible APIs, with additional interfaces for other providers.
- **Customizable preprompts.** The system prompts that steer the model (roadmap, generation, improvement, clarification, file format, philosophy) are plain text files you can edit.
- **Benchmark suite.** Evaluate models and configurations on a set of coding problems.
- **Docker support.** Run the tool in a container with a consistent environment.

---

## How It Works

1. **Input.** You provide a project directory containing a `prompt` file (and optionally `file_format`, `roadmap`, or other context files).
2. **Clarify (optional).** The agent may ask you questions to refine requirements.
3. **Plan.** The model produces a roadmap or architecture outline for the project.
4. **Generate.** The model writes the files in a structured format, which the file-format parser converts into a file dictionary.
5. **Persist.** Files are written to the project directory, and a Git commit may be created.
6. **Execute and lint (optional).** Generated code is run or checked, and errors can be fed back to the model for fixing.
7. **Improve.** On subsequent runs, the tool can modify existing code based on a new prompt, applying diffs where possible.

---

## Requirements

- Python 3.10 or later (check `pyproject.toml` for the exact range)
- An API key for your chosen LLM provider. For OpenAI, set `OPENAI_API_KEY`.
- Git (recommended, for version tracking)
- Docker (optional)
- [Poetry](https://python-poetry.org/) if you are developing from source

---

## Installation

### From PyPI

```bash
pip install gpt-engineer
```

### From Source

```bash
git clone https://github.com/gpt-engineer-org/gpt-engineer.git
cd gpt-engineer
poetry install
poetry shell
```

Or with pip in editable mode:

```bash
pip install -e .
```

### Windows

See `WINDOWS_README.md` in the repository for Windows-specific setup instructions, including environment variable configuration and path notes.

### Set Your API Key

Linux/macOS:

```bash
export OPENAI_API_KEY="your-api-key"
```

Windows (PowerShell):

```powershell
$env:OPENAI_API_KEY="your-api-key"
```

You can also place the key in a `.env` file in the project directory.

---

## Quick Start

1. Create a project folder with a prompt file:

```bash
mkdir -p projects/snake
```

2. Write `projects/snake/prompt`:

```text
Build a snake game in Python using pygame.
- The snake grows when it eats food.
- The game ends when the snake hits a wall or itself.
- Display the score in the top-left corner.
- Include a README with run instructions.
```

3. Run the generator:

```bash
gpt-engineer projects/snake
```

4. Review the generated files in `projects/snake/` and run the project as instructed in its README.

5. To request changes later, update the prompt or add a new one, then run:

```bash
gpt-engineer projects/snake --improve
```

---

## Usage

### Basic Command

```bash
gpt-engineer <PROJECT_PATH> [OPTIONS]
```

### Common Options

The exact set of flags depends on your installed version. Run `gpt-engineer --help` to see the current list. Commonly used options include:

| Option | Description |
|---|---|
| `--improve` | Modify an existing project instead of generating from scratch |
| `--lite` | Use a lighter-weight workflow with fewer steps and tokens |
| `--clarify` | Enable the clarification dialogue before generation |
| `--use-cache` | Reuse cached LLM responses where available |
| `--no-execution` | Skip running or linting the generated code |
| `--model <name>` | Choose the LLM model (for example, `gpt-4`) |
| `--temperature <float>` | Control output randomness |
| `--azure <endpoint>` | Use an Azure OpenAI endpoint |
| `--steps <name>` | Select a particular step configuration |

### Examples

Generate a new project with a specific model:

```bash
gpt-engineer projects/todo-app --model gpt-4
```

Improve an existing project and skip execution:

```bash
gpt-engineer projects/todo-app --improve --no-execution
```

Use a cheaper, faster workflow:

```bash
gpt-engineer projects/todo-app --lite
```

### Getting Help

```bash
gpt-engineer --help
```

---

## Project Layout

Each project managed by gpt-engineer lives in its own directory:

```
projects/
└── snake/
    ├── prompt              # Your requirements (required)
    ├── file_format         # Optional: describes the expected output format
    ├── roadmap             # Optional: high-level plan or milestones
    ├── .gpteng/            # Internal memory, logs, and cache
    └── ...                 # Generated source files
```

Files that gpt-engineer writes into a project are tracked so that changes can be reviewed with Git.

---

## Configuration

### Environment Variables

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | API key for OpenAI |
| `MODEL_NAME` | Default model to use |
| `AZURE_OPENAI_*` | Azure OpenAI configuration, if used |

### Project Configuration

Per-project settings are handled by the project config module. Check the project's configuration files for options such as default model, steps, and execution behavior.

### Preprompts

The system prompts that guide the model live in the preprompts directory. Each file controls a stage of the workflow:

| File | Purpose |
|---|---|
| `roadmap` | Instructs the model to plan the project |
| `generate` | Instructs the model to write the initial code |
| `improve` | Instructs the model to modify existing code |
| `clarify` | Guides the clarification dialogue |
| `entrypoint` | Asks for a script to run the project |
| `file_format` | Defines how the model should format file output |
| `file_format_diff` | Defines the diff-based output format |
| `file_format_fix` | Guides fixing malformed output |
| `philosophy` | General guidance on code quality and style |

You can copy these files and edit them to change the tool's behavior globally or per project.

### Benchmark Configuration

Benchmark settings are stored in `default_bench_config.toml` and can be overridden with your own TOML file.

---

## Prompt Engineering Tips

- **Be specific about the stack.** Name the language, frameworks, and libraries you want.
- **List features as bullet points.** Concrete, testable requirements produce better results.
- **State constraints.** Mention file layout, naming conventions, or things to avoid.
- **Ask for run instructions.** Requesting a README with setup steps makes the output easier to use.
- **Iterate.** Use `--improve` with focused follow-up prompts rather than rewriting the whole prompt.
- **Use `--clarify` for vague requests.** Letting the agent ask questions often yields better specifications.

---

## Using Docker

### Build and Run with Docker Compose

```bash
docker compose up --build
```

The `docker-compose.yml` file mounts a local projects directory into the container and passes through your API key. Adjust the volume paths to match your setup.

### Build and Run with Docker Directly

```bash
docker build -t gpt-engineer .
docker run -it --rm \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -v "$(pwd)/projects:/app/projects" \
  gpt-engineer projects/snake
```

The `entrypoint.sh` script handles startup inside the container.

---

## Benchmarking

The benchmark suite runs a model and configuration against a set of coding problems (defined in the `benchmark` package) and records the results.

```bash
python -m gpt_engineer.benchmark
```

Key components:

- `bench_config.py`: Loads benchmark configuration.
- `default_bench_config.toml`: Default settings.
- `load.py`: Loads problem definitions.
- `problems.py` and `problem.py`: Represent problems and their evaluation.
- `types.py`: Shared type definitions.

Two legacy scripts are included at the repository root: `legacy_benchmark.py` and `clean_benchmarks.py`. `print_chat.py` prints saved conversations for review.

---

## Running Tests

The test suite uses `pytest`.

```bash
poetry run pytest
```

Or, with tox, which runs the tests in an isolated environment:

```bash
tox
```

Test files cover the CLI agent, file selection, collection and consent, learning, project configuration, installation, benchmark configuration, chat-to-files parsing, Git integration, disk memory and execution environments, the simple agent, diff salvage, and token usage. Several tests use `mock_ai.py` so they run without making real API calls.

Test fixtures include example chat transcripts and generated code snapshots for scenarios such as a calculator, a temperature converter, a task master, and several benchmark apps.

---

## Building the Documentation

The documentation uses Sphinx.

```bash
cd docs
make html
```

On Windows, use `make.bat html`. See `docs_building.md` for details. The API reference is generated with `create_api_rst.py`.

---

## Troubleshooting

| Problem | Suggested fix |
|---|---|
| `Authentication error` or `Invalid API key` | Check that `OPENAI_API_KEY` is set in the current shell or `.env` |
| Output files are missing or malformed | Try `--lite` or a stronger model, or check `file_format` |
| Generated code fails to run | Enable execution feedback and rerun with `--improve` describing the error |
| Costs are higher than expected | Use `--use-cache`, `--lite`, or a smaller model |
| Windows path or encoding issues | Follow `WINDOWS_README.md` |
| Docker cannot see the projects folder | Verify the volume mount path in `docker-compose.yml` |

If you hit an issue not listed here, search the project's issue tracker or open a new issue with your command, version, and logs.

---

## Contributing

Contributions are welcome. Before opening a pull request:

1. Read the contributing guidelines linked from the docs.
2. Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
3. Install development dependencies with `poetry install`.
4. Run the test suite and linters (`pytest`, `tox`).
5. Keep changes focused and include tests where practical.

For ideas on where help is needed, see `ROADMAP.md`.

---

## Governance, Legal, and Citation

- **Governance:** See `GOVERNANCE.md` for decision-making and maintainership.
- **Terms of Use:** See `TERMS_OF_USE.md`.
- **Disclaimer:** See `DISCLAIMER.md`. Generated code is produced by an AI model and must be reviewed before use, especially in production or security-sensitive contexts.
- **Citation:** If you use gpt-engineer in research, cite it using `citation.cff`.

---

## Roadmap

Planned work is tracked in `ROADMAP.md`. Areas of interest include better handling of large codebases, expanded model support, improved diff application, and stronger benchmark coverage.

---

## Acknowledgements

Thanks to all contributors and users. See `Acknowledgements.md` for the full list.

---

## License

This project is released under the license in the `LICENSE` file. Check that file for the exact terms.
