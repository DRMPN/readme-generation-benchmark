# GPT Engineer

**Specify what you want it to build, the AI asks for clarification, and then builds it.**

`gpt-engineer` lets you:

- Specify a software in natural language
- Sit back and watch as an AI writes and executes the code
- Ask the AI to implement improvements

Generated code is executed on your machine (via a generated `run.sh` entrypoint, after you confirm), so please use caution. See [TERMS_OF_USE.md](TERMS_OF_USE.md) and [DISCLAIMER.md](DISCLAIMER.md).

## Requirements

- Python `>=3.10,<3.13` (CI runs tests on 3.10, 3.11 and 3.12)
- An OpenAI API key (or access to another supported LLM — see [Using other models](#using-other-models))
- Note: some slim Python installations do not include `tkinter`, which is required. On macOS install it with `brew install python-tk`; on Debian-based Linux use `sudo apt-get install python3-tk`.

## Installation

Stable release:

```bash
python -m pip install gpt-engineer
```

From source:

```bash
git clone https://github.com/gpt-engineer-org/gpt-engineer.git
cd gpt-engineer
poetry install
poetry shell
```

The project is managed with [Poetry](https://python-poetry.org/); see `pyproject.toml` for dependencies.

## Setup API key

Choose one of the following:

- Export an environment variable (you can add this to `.bashrc` so that you don't have to do it each time you start the terminal):

  ```bash
  export OPENAI_API_KEY=[your api key]
  ```

- Or create a copy of [.env.template](.env.template) named `.env` and add your `OPENAI_API_KEY` there. The same file supports `ANTHROPIC_API_KEY` for Anthropic models.

On Windows, see [WINDOWS_README.md](WINDOWS_README.md) for setup instructions.

## Quickstart

### Create new code (default usage)

- Create an empty folder for your project anywhere on your computer
- Create a file called `prompt` (no extension) inside your new folder and fill it with instructions in natural language
- Run `gpte <project_dir>` with a relative path to your folder, for example:

  ```bash
  gpte projects/my-new-project
  ```

The tool will generate code for the project, generate a `run.sh` entrypoint (a unix script that installs dependencies and runs the codebase), ask you to confirm, and then execute it.

### Improve existing code

- Locate a folder with code which you want to improve anywhere on your computer
- Create a file called `prompt` (no extension) inside your folder and fill it with instructions for how you want to improve the code
- Run `gpte <project_dir> -i`, for example:

  ```bash
  gpte projects/my-old-project -i
  ```

In improve mode you are asked to interactively select which files to include in context (skip this with `--skip-file-selection`). The proposed changes are shown as a diff before you are asked whether to apply them.

The repository contains example projects under `projects/`:

- `projects/example-improve` — a small Python project used for trying improve mode
- `projects/example-vision` — an example that uses image input (a UX diagram in `images/`) together with a `prompt` file

## CLI

The package installs three equivalent entry points (`gpt-engineer`, `ge`, and `gpte`) and a `bench` command for benchmarks. Options include:

| Option | Description |
| --- | --- |
| `project_path` (positional) | Path to the project directory (default: current directory) |
| `--model, -m` | Model id string (default: `$MODEL_NAME` or `gpt-4o`) |
| `--temperature, -t` | Controls randomness; lower values are more deterministic (default: 0.1) |
| `--improve, -i` | Improve an existing project by modifying the files |
| `--lite, -l` | Run a generation using only the main prompt |
| `--clarify, -c` | Discuss the specification with the AI before implementation |
| `--self-heal, -sh` | Fix the code by itself when it fails |
| `--azure, -a` | Endpoint for your Azure OpenAI service; the model is the deployment name |
| `--use-custom-preprompts` | Use your project's custom preprompts instead of the default ones |
| `--llm-via-clipboard` | Use the clipboard to communicate with the AI |
| `--prompt_file` | Relative path to a text file containing a prompt (default: `prompt`) |
| `--entrypoint_prompt` | Relative path to a file specifying requirements for the entrypoint |
| `--image_directory` | Relative path to a folder containing images (requires a vision-capable model) |
| `--use_cache` | Cache LLM responses in a local SQLite database (`.langchain.db`) to speed up repeated runs and save tokens |
| `--skip-file-selection, -s` | Skip interactive file selection in improve mode and use the generated TOML file directly |
| `--verbose, -v` / `--debug, -d` | Verbose logging / debug mode (drops into pdb on errors) |
| `--no_execution` | Run setup but do not call the LLM or write any code (for testing) |
| `--sysinfo` | Output system information for debugging |
| `--diff_timeout` | Diff regexp timeout in seconds (default: 3); increase if regexp search times out |

Clarify and lite mode cannot be combined with improve mode.

## Modes

- **Default mode** generates code from your prompt, generates a `run.sh` entrypoint, and (after your confirmation) executes it.
- **Clarify mode** (`-c`) discusses the specification with the AI before implementation.
- **Lite mode** (`-l`) runs a generation using only the main prompt.
- **Improve mode** (`-i`) modifies an existing codebase. Changes are shown as diffs and applied only after confirmation.
- **Self-heal mode** (`-sh`) executes the entrypoint and, if it fails, sends the error output back to the AI for fixing, retrying up to a maximum number of attempts (10).

## Using other models

- **Azure OpenAI**: set `OPENAI_API_KEY` and pass your service endpoint via `--azure https://<resource-name>.openai.azure.com`, using your Azure AI Studio deployment name as the model name.
- **Anthropic models**: set `ANTHROPIC_API_KEY` in your environment or `.env`.
- **Open/local models**: any OpenAI-compatible API can be used. See [docs/open_models.md](docs/open_models.md) for the recommended setup with `llama-cpp-python`'s server, example model suggestions, OpenRouter usage, and the required environment variables (`OPENAI_API_BASE`, `OPENAI_API_KEY`, `MODEL_NAME`, `LOCAL_MODEL`).

## Vision

Pass `--image_directory` pointing at a folder of images to include them in the prompt (see `projects/example-vision`). Images are only used when the selected model supports vision.

## Custom preprompts

With `--use-custom-preprompts`, gpt-engineer copies the default preprompts (from `gpt_engineer/preprompts/`) into your project's `preprompts` directory if they don't already exist there, and then uses your edited versions. The default preprompts cover steps such as `generate`, `improve`, `clarify`, `entrypoint`, `file_format`, `philosophy`, and `roadmap`.

## Project files and logs

gpt-engineer stores metadata and logs in a `.gpteng/` directory inside your project, including the full code generation chat (`all_output.txt`), improvement logs, diff errors, and debug logs (`debug_log_file.txt`). If improve mode fails to apply changes, the tool asks you to upload the `debug_log_file.txt` from `.gpteng/memory/logs` in a GitHub issue.

## Docker

A [docker-compose.yml](docker-compose.yml) builds the image from [docker/Dockerfile](docker/Dockerfile), loads environment variables from a `.env` file, and mounts `./projects/example` into the container. Example:

```bash
docker compose build
docker compose run gpt-engineer
```

## Benchmarks

The `bench` entry point runs benchmarks against an agent defined in a Python file that exposes a `default_config_agent` function. Available benchmarks are `apps`, `mbpp`, and `gptme` (see `gpt_engineer/benchmark/` and `default_bench_config.toml`):

```bash
bench path/to/agent.py
```

## Development

Install dependencies and pre-commit hooks:

```bash
poetry install
poetry shell
pre-commit install
```

Other developer tooling in the repository:

- `tox` runs the test suite across Python 3.10–3.12 (tests in `tests/`; tests marked `requires_key` need a valid `OPENAI_API_KEY`)
- `Makefile` targets: `make help`, `make install`, `make run <folder_name>`, `make cloc`
- Documentation is built with Sphinx from `docs/` (published at https://gpt-engineer.readthedocs.io)
- Contributing guidelines, the code of conduct, and governance are in `.github/CONTRIBUTING.md`, `.github/CODE_OF_CONDUCT.md`, and [GOVERNANCE.md](GOVERNANCE.md); see also [ROADMAP.md](ROADMAP.md)

## Feedback and data collection

After generating a project, gpt-engineer may ask for a short review of the generated code. If you consent, feedback (prompt, model, temperature, configuration, and logs) is sent to RudderStack and used with the sole purpose of improving gpt-engineer; it is not shared with third parties. Consent logic lives in `gpt_engineer/applications/cli/learning.py`.

## Documentation

- Documentation: https://gpt-engineer.readthedocs.io
- Introduction, installation, and quickstart guides live in `docs/`
- Tracing and debugging with Weights & Biases: [docs/tracing_debugging.md](docs/tracing_debugging.md) (set `WANDB_API_KEY` and `LANGCHAIN_WANDB_TRACING=true`)

## Community and governance

- Contributions are welcome via pull requests, bug reports, feature requests, and discussions — see `.github/CONTRIBUTING.md`
- Project governance is described in [GOVERNANCE.md](GOVERNANCE.md) and the roadmap in [ROADMAP.md](ROADMAP.md)

## Terms of use, disclaimer, and license

By using gpt-engineer you agree to the terms in [TERMS_OF_USE.md](TERMS_OF_USE.md). The software is an experimental application provided "as-is" without warranty — see [DISCLAIMER.md](DISCLAIMER.md). Note that LLM API usage can be expensive; you are responsible for monitoring your own token usage and costs.

This project is licensed under the MIT License — see [LICENSE](LICENSE).

## Acknowledgements

See [Acknowledgements.md](Acknowledgements.md). In particular, the prompt for the improve-code step is strongly based on Paul Gauthier's prompt in [Aider](https://github.com/paul-gauthier/aider/blob/main/aider/coders/editblock_coder.py).

## Citation

If you use this software, please cite it as below (see [citation.cff](citation.cff)):

```bibtex
@software{Osika_gpt-engineer_2023,
  author = {Osika, Anton},
  title = {gpt-engineer},
  year = {2023},
  url = {https://github.com/gpt-engineer-org/gpt-engineer}
}
```
