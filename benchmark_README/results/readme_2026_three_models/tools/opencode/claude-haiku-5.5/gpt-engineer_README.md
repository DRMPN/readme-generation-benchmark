# gpt-engineer

`gpt-engineer` is a command-line tool that takes a natural-language specification of a software project, asks clarifying questions if needed, and uses a large language model (LLM) to generate the project's code files. It can also improve an existing project based on a written request.

The package is published on PyPI as `gpt-engineer` (version 0.3.1 in `pyproject.toml`), is licensed under the MIT License, and is classified as "Development Status :: 4 - Beta".

## Features

- **Generate a project from a prompt.** Write the requirements in a text file named `prompt` inside a project folder, then run the tool. The LLM produces the project's files.
- **Clarify mode (`--clarify`).** The AI asks questions about the specification before generating code.
- **Lite mode (`--lite`).** Runs a single generation using only the main prompt, without the extra generation steps.
- **Improve mode (`--improve`).** Modifies an existing project. You choose which files the AI may read, and the proposed changes are shown as a diff before you approve them.
- **Self-heal mode (`--self-heal`).** Runs the generated entrypoint script and, if it fails, sends the output back to the AI to fix the code (up to 10 attempts).
- **Entrypoint generation.** The AI writes a `run.sh` script that installs dependencies and runs the project.
- **Custom preprompts.** Use `--use-custom-preprompts` to copy and edit the default instructions for a specific project.
- **Image input.** Pass a folder of images with `--image_directory` for models that support vision.
- **Multiple LLM providers.** OpenAI models, Azure OpenAI deployments, Anthropic (Claude) models, and OpenAI-compatible local or hosted servers are supported (see [Configuration](#configuration)).
- **Clipboard mode (`--llm-via-clipboard`).** Copies the prompt to the clipboard and reads the AI's reply from your input, so you can use a chat interface instead of an API. The code marks this as "not yet fully supported."
- **Response caching (`--use_cache`).** Stores LLM responses in a local SQLite file, `.langchain.db`.
- **Benchmarking.** A separate `bench` command runs an agent against the APPS and MBPP benchmark problems.

## Requirements

- Python 3.10, 3.11, or 3.12 (`python = ">=3.10,<3.13"` in `pyproject.toml`).
- An API key for the LLM provider you plan to use, unless you run a local model.
- Optional: Docker, for the container setup described below.
- Optional: Poetry, if you install from source.

## Installation

### From PyPI

```bash
python -m pip install gpt-engineer
```

### From source

```bash
git clone https://github.com/gpt-engineer-org/gpt-engineer.git
cd gpt-engineer
poetry install
poetry shell
```

`make install` runs `poetry install` and installs the pre-commit hooks.

The CLI is available under three command names: `gpt-engineer`, `ge`, and `gpte`. The examples below use `gpte`.

### Tkinter

Some slim Python installations do not include `tkinter`, which the tool needs. On macOS, install it with `brew install python-tk`. On Debian-based Linux, install it with `sudo apt-get install python3-tk`. See [`docs/installation.rst`](docs/installation.rst).

## Quick start

1. Create an empty folder for your project. The example below uses `projects/my-new-project`.
2. Create a file named `prompt` (no extension) in that folder and describe what you want to build.
3. Set your API key (see [Configuration](#configuration)).
4. Run the tool:

   ```bash
   gpte projects/my-new-project
   ```

If the folder has no `prompt` file, the tool asks you to type the specification on the command line.

## Usage

### Generate a new project

```bash
gpte <project_dir>
```

### Improve an existing project

```bash
gpte <project_dir> -i
```

Put the change request in the `prompt` file in that folder (or type it when asked). The tool lets you choose the files to include, proposes changes as a diff, and asks `Do you want to apply these changes?` before writing them.

### Command-line options

These are the options defined in `gpt_engineer/applications/cli/main.py`:

| Option | Description |
| --- | --- |
| `project_path` | Path to the project folder. Default: `.` |
| `-m, --model` | Model ID. Default: the `MODEL_NAME` environment variable, or `gpt-4o`. |
| `-t, --temperature` | Sampling temperature. Default: `0.1`. |
| `-i, --improve` | Improve an existing project. |
| `-l, --lite` | Lite mode: generate using only the main prompt. Cannot be combined with `--improve`. |
| `-c, --clarify` | Discuss the specification with the AI before generating code. Cannot be combined with `--improve`. |
| `-sh, --self-heal` | Run the entrypoint and ask the AI to fix failures. |
| `-a, --azure` | Azure OpenAI endpoint, such as `https://xx.openai.azure.com`. The model argument is then the deployment name. |
| `--use-custom-preprompts` | Use preprompts from the project's `preprompts/` folder. Missing files are copied from the defaults. |
| `--llm-via-clipboard` | Communicate with the AI through the clipboard. |
| `--prompt_file` | Path, relative to the project, of the prompt file. Default: `prompt`. |
| `--entrypoint_prompt` | Path to a file with extra requirements for the entrypoint script. |
| `--image_directory` | Folder of images to include with the prompt. |
| `--use_cache` | Cache LLM responses in `.langchain.db`. |
| `-s, --skip-file-selection` | In improve mode, skip the interactive file selection and use the saved selection. |
| `--no_execution` | Run setup without calling the LLM or writing code. For testing. |
| `--diff_timeout` | Timeout for the regular-expression search used when applying diffs in improve mode. Default: `3`. Increase it if the search times out. |
| `--sysinfo` | Print system information for debugging. |
| `-v, --verbose` | Enable verbose logging. |
| `-d, --debug` | Open the Python debugger on an unhandled exception. |

Run `gpte --help` for the full list.

### Output and project files

- Generated files are written into the project folder.
- Logs and metadata are stored in `.gpteng/` inside the project folder. The memory directory is `.gpteng/memory/`.
- In improve mode, your file selection is saved to `.gpteng/file_selection.toml`.
- If the project is a Git repository, changes are staged with Git (see `gpt_engineer/core/git.py`).
- The tool prints the total API cost when using an OpenAI model. For other models it prints the total tokens used, or `$ 0.0` when `LOCAL_MODEL` is set.

### Docker

Build the image from the repository root:

```bash
docker build --rm -t gpt-engineer -f docker/Dockerfile .
```

Run it with your key and a project folder mounted at `/project`:

```bash
docker run -it --rm -e OPENAI_API_KEY="YOUR_OPENAI_KEY" -v ./your-project:/project gpt-engineer
```

`docker-compose.yml` is also provided. It reads `.env`, mounts `./projects/example` at `/project`, and can be started with `docker compose up -d --build`. More detail is in [`docker/README.md`](docker/README.md).

## Configuration

The tool loads environment variables from the shell, and falls back to a `.env` file in the current directory. Copy `.env.template` to `.env` and fill in your keys:

```bash
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
```

| Variable | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | API key for OpenAI models, and for Azure OpenAI. |
| `ANTHROPIC_API_KEY` | API key for Anthropic (Claude) models. |
| `MODEL_NAME` | Default model ID when `--model` is not given. |
| `OPENAI_API_BASE` | Base URL for an OpenAI-compatible server. Used in the docs for local and OpenRouter setups. |
| `LOCAL_MODEL` | When set, the cost message reports `$ 0.0` for local LLMs. |
| `OPENAI_API_VERSION` | Azure OpenAI API version. Default: `2024-05-01-preview`. |

### Model selection

- **OpenAI:** pass the model name, for example `gpte <dir> -m gpt-4o`.
- **Anthropic:** any model name containing `claude` is sent to the Anthropic client. Set `ANTHROPIC_API_KEY`.
- **Azure OpenAI:** pass `--azure <endpoint>`, and set the model argument to your deployment name.
- **OpenAI-compatible servers:** set `OPENAI_API_BASE` and `OPENAI_API_KEY`, and pass the model name your server expects. See [`docs/open_models.md`](docs/open_models.md) for a llama.cpp setup and an OpenRouter setup.

The docs recommend `--lite` and a low temperature (`0.1`) for open models.

Image input is used only for models the tool recognizes as vision-capable: model names containing `vision-preview`, `gpt-4-turbo` (without `preview`), or `claude`.

## Consent and data collection

After a new project is generated (not in improve mode), the tool may ask whether it can store your prompts to help improve gpt-engineer:

```
Is it ok if we store your prompts to help improve GPT Engineer? (y/n)
```

- If you answer `y`, the tool writes `true` to a file named `.gpte_consent` in the current directory. It then asks a few questions about the result (whether the code ran, whether it was perfect, whether it was useful, and optional comments). The prompt, model, temperature, configuration, logs, and your answers are sent to RudderStack for analysis. The code states that this data is not shared with third parties.
- If you answer `n`, nothing is sent.
- To withdraw consent, delete `.gpte_consent`.

## Benchmarking

The `bench` command runs an agent against benchmark problems:

```bash
bench path/to/agent.py
```

The agent file must define a function named `default_config_agent`. The CLI help lists `apps` and `mbpp` as the available benchmarks. The default configuration is `gpt_engineer/benchmark/default_bench_config.toml`. Options include `--yaml-output` to save results, `--verbose`, and `--use-cache` (on by default).

## Development

Install the development dependencies with Poetry (see [From source](#from-source)). Useful commands:

```bash
poetry run pytest                  # run tests
poetry run pytest -m "not requires_key"   # skip tests that need a real OPENAI_API_KEY
poetry run pre-commit run --all-files     # run linters and formatters
```

`tox.ini` tests Python 3.10, 3.11, and 3.12. The project uses `ruff`, `black`, and `mypy` (see `pyproject.toml`).

The `make run` target runs the tool on `projects/<name>`. Other targets are listed by `make help`.

### Project layout

- `gpt_engineer/applications/cli/`: the `gpte` command, file selection, consent and feedback collection.
- `gpt_engineer/core/`: the AI wrapper (`ai.py`), execution environments, file handling (`files_dict.py`, `chat_to_files.py`), Git integration, and diff application.
- `gpt_engineer/core/default/`: default agent, steps, and disk-based memory and execution.
- `gpt_engineer/preprompts/`: the default instructions sent to the LLM.
- `gpt_engineer/tools/`: custom steps (`clarified_gen`, `lite_gen`, `self_heal`).
- `gpt_engineer/benchmark/`: the `bench` command and benchmark loaders.
- `projects/`: example projects.
- `docs/`: Sphinx documentation sources.
- `tests/`: the test suite.

## Documentation

- [Installation](docs/installation.rst)
- [Quickstart](docs/quickstart.rst)
- [Open and local models](docs/open_models.md)
- [Docker setup](docker/README.md)
- [Tracing and debugging](docs/tracing_debugging.md)
- [Roadmap](ROADMAP.md)
- [Windows notes](WINDOWS_README.md)

## Contributing

Contributions are welcome. See the roadmap for open work, and see [`GOVERNANCE.md`](GOVERNANCE.md) for project governance. The roadmap describes how to help with design discussion, pull requests, and reviews.

## Legal

- License: MIT. See [`LICENSE`](LICENSE).
- [Terms of use](TERMS_OF_USE.md)
- [Disclaimer](DISCLAIMER.md)
- [Acknowledgements](Acknowledgements.md)

Running the tool means you agree to the terms of use. Generated code is produced by an LLM and is not guaranteed to be correct; review it before use.

## Citation

A citation file is available at [`citation.cff`](citation.cff).
