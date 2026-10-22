# GPT Engineer

**Specify what you want it to build, the AI asks for clarification, and then builds it.**

GPT Engineer is a project that uses LLMs (such as GPT-4) to automate the process of software engineering. It lets you:

- Specify a software in natural language
- Sit back and watch as an AI writes and executes the code
- Ask the AI to implement improvements

## Table of Contents

- [Installation](#installation)
- [Setup API Key](#setup-api-key)
- [Usage](#usage)
- [Docker](#docker)
- [Configuration](#configuration)
- [Modes](#modes)
- [Open and Local Models](#open-and-local-models)
- [Development](#development)
- [Testing](#testing)
- [Documentation](#documentation)
- [Governance](#governance)
- [Acknowledgements](#acknowledgements)
- [Disclaimer](#disclaimer)
- [License](#license)

## Installation

### Stable release

To install GPT Engineer, run this command in your terminal:

```bash
python -m pip install gpt-engineer
```

This is the preferred method to install `gpt-engineer`, as it will always install the most recent stable release.

> **Note:** When reporting bugs, please specify your installation method (using `pip install` or by building the repository) in the "Installation Method" section of the bug report template.

### From sources

The sources for `gpt-engineer` can be downloaded from the [GitHub repo](https://github.com/gpt-engineer-org/gpt-engineer.git).

You can either clone the public repository:

```bash
git clone https://github.com/gpt-engineer-org/gpt-engineer.git
cd gpt-engineer
poetry install
poetry shell
```

### Windows Setup

On Windows, follow the standard installation instructions above, but to set the API key do one of:

- `set OPENAI_API_KEY=[your api key]` on cmd
- `$env:OPENAI_API_KEY="[your api key]"` on powershell

Alternatively, you can set up a user-specific environment variable through System Properties > Environment Variables.

For the full Windows setup guide, see [WINDOWS_README.md](WINDOWS_README.md).

### Troubleshooting

For mac and linux systems, there are sometimes slim Python installations that do not include the `gpt-engineer` requirement tkinter, which is a standard library and thus not pip installable.

To install tkinter on mac, you can for example use brew:

```bash
brew install python-tk
```

On debian-based linux systems you can use:

```bash
sudo apt-get install python3-tk
```

## Setup API Key

Choose one of the following:

- Export env variable (you can add this to `.bashrc` so that you don't have to do it each time you start the terminal):

  ```bash
  export OPENAI_API_KEY=[your api key]
  ```

- Add it to the `.env` file:
  - Create a copy of `.env.template` named `.env`
  - Add your `OPENAI_API_KEY` in .env

- If you want to use a custom model, visit the docs on [using open models and azure models](docs/open_models.md).

## Usage

The project supports Python `>=3.10` and `<3.13`.

### Creating new code (default usage)

- Create an empty folder for your project anywhere on your computer
- Create a file called `prompt` (no extension) inside your new folder and fill it with instructions
- Run `gpte <project_dir>` with a relative path to your folder

For example, if you create a new project inside the gpt-engineer `/projects` directory:

```bash
gpte projects/my-new-project
```

### Improving existing code

- Locate a folder with code which you want to improve anywhere on your computer
- Create a file called `prompt` (no extension) inside your new folder and fill it with instructions for how you want to improve the code
- Run `gpte <project_dir> -i` with a relative path to your folder

For example, if you want to run it against an existing project inside the gpt-engineer `/projects` directory:

```bash
gpte projects/my-old-project -i
```

By running `gpt-engineer` you agree to our [terms of use](TERMS_OF_USE.md).

### Running in the browser

You can simply use [GitHub Codespaces](https://github.com/gpt-engineer-org/gpt-engineer/codespaces).

### CLI Options

| Option | Flag | Description |
|--------|------|-------------|
| model | `--model`, `-m` | Model ID string (default: `gpt-4o`) |
| temperature | `--temperature`, `-t` | Controls randomness: lower values for more focused, deterministic outputs (default: 0.1) |
| improve | `--improve`, `-i` | Improve an existing project by modifying the files |
| lite mode | `--lite`, `-l` | Run a generation using only the main prompt |
| clarify mode | `--clarify`, `-c` | Discuss specification with AI before implementation |
| self-heal mode | `--self-heal`, `-sh` | Fix the code by itself when it fails |
| azure | `--azure`, `-a` | Endpoint for your Azure OpenAI Service |
| use custom preprompts | `--use-custom-preprompts` | Use your project's custom preprompts instead of the default ones |
| llm via clipboard | `--llm-via-clipboard` | Use the clipboard to communicate with the AI |
| verbose | `--verbose`, `-v` | Enable verbose logging for debugging |
| debug | `--debug`, `-d` | Enable debug mode for debugging |
| prompt file | `--prompt_file` | Relative path to a text file containing a prompt (default: `prompt`) |
| entrypoint prompt | `--entrypoint_prompt` | Relative path to a text file specifying requirements for your entrypoint |
| image directory | `--image_directory` | Relative path to a folder containing images |
| use cache | `--use_cache` | Speeds up computations and saves tokens by caching the LLM response |
| skip file selection | `--skip-file-selection`, `-s` | Skip interactive file selection in improve mode |
| no execution | `--no_execution` | Run setup but do not call LLM or write any code |
| sysinfo | `--sysinfo` | Output system information for debugging |
| diff timeout | `--diff_timeout` | Diff regexp timeout (default: 3) |

### Makefile targets

If working from the repository, you can use the following Makefile targets:

- `make install` — Install dependencies using Poetry and set up pre-commit hooks
- `make run <folder_name>` — Run GPT Engineer on the folder with the given name

## Docker

### Using Docker CLI

1. Clone the repository:

    ```bash
    git clone https://github.com/gpt-engineer-org/gpt-engineer.git
    cd gpt-engineer
    ```

2. Build the Docker Image:

    ```bash
    docker build --rm -t gpt-engineer -f docker/Dockerfile .
    ```

3. Run the Docker Container:

    ```bash
    docker run -it --rm -e OPENAI_API_KEY="YOUR_OPENAI_KEY" -v ./your-project:/project gpt-engineer
    ```

    Replace `YOUR_OPENAI_KEY` with your actual OpenAI API key. The `-v` flag mounts your local `your-project` directory inside the container. Ensure this directory contains all necessary files, including the `prompt` file.

### Using Docker Compose

1. Clone the repository (if not already done)
2. Build and run using Docker Compose:

    ```bash
    docker-compose -f docker-compose.yml build
    docker-compose run --rm gpt-engineer
    ```

    Set the `OPENAI_API_KEY` in the `docker-compose.yml` using an `.env` file or as an environment variable. Mount your project directory to the container using volumes, e.g., `"./projects/example:/project"`.

### Debugging

To facilitate debugging, you can run a shell inside the built Docker image:

```bash
docker run -it --entrypoint /bin/bash gpt-engineer
```

## Configuration

### `gpt-engineer.toml`

The `gpt-engineer.toml` file is a TOML file that contains project-specific configuration used by the GPT Engineer CLI and gptengineer.app. An example configuration:

```toml
[run]
build = "npm run build"
test = "npm run test"
lint = "quick-lint-js"

[paths]
base = "./frontend"  # base directory to operate in (for monorepos)
src = "./src"        # source directory (under the base directory) from which context will be retrieved

[gptengineer-app]  # this namespace is used for gptengineer.app
project_id = "..."

# we support multiple OpenAPI schemas, used as context for the LLM
openapi = [
    { url = "https://api.gptengineer.app/openapi.json" },
    { url = "https://some-color-translating-api/openapi.json" },
]
```

### Preprompts

Preprompts are instructions to the AI on how the task should be approached. They are stored in `gpt_engineer/preprompts/` and can be customized per-project by using the `--use-custom-preprompts` flag, which copies all original preprompts to the project's workspace if they don't exist there.

## Modes

GPT Engineer supports several generation and execution modes:

- **Default mode**: Generate code from the prompt, execute the entrypoint
- **Clarify mode** (`--clarify` / `-c`): Discuss specification with the AI before implementation
- **Lite mode** (`--lite` / `-l`): Run a generation using only the main prompt
- **Improve mode** (`--improve` / `-i`): Improve an existing project by modifying files
- **Self-heal mode** (`--self-heal` / `-sh`): Fix the code by itself when it fails

## Open and Local Models

You can integrate `gpt-engineer` with open-source models by leveraging an OpenAI-compatible API. The recommended approach is to use [llama.cpp](https://github.com/ggerganov/llama.cpp) with its Python bindings `llama-cpp-python`.

For testing that the open LLM setup works, see [docs/examples/open_llms/README.md](docs/examples/open_llms/README.md).

To run with a local model, set the following environment variables:

```bash
export OPENAI_API_BASE="http://localhost:8000/v1"
export OPENAI_API_KEY="sk-xxx"
export MODEL_NAME="CodeLLama"
export LOCAL_MODEL=true
```

Then run `gpt-engineer`:

```bash
gpte <project_dir> $MODEL_NAME --lite --temperature 0.1
```

The `--lite` mode is needed for now since open models behave worse with too many instructions. Temperature is set to `0.1` to get consistent results.

### Open Router models

In case you don't possess the hardware to run local LLMs yourself, you can use the hosting on [Open Router](https://openrouter.ai) and pay as you go for the tokens.

### Azure models

Set your Azure OpenAI key and call `gpt-engineer` with your service endpoint:

```bash
gpt-engineer --azure https://myairesource.openai.azure.com ./projects/example/ my-gpt4-project-name
```

## Benchmarking

GPT Engineer includes a benchmarking tool for evaluating agents against coding tasks. Currently available benchmarks are: `apps`, `mbpp`, and `gptme`.

To run benchmarks:

```bash
bench <path_to_agent> <bench_config> [options]
```

Where `path_to_agent` is a Python file that contains a function called `default_config_agent`. The benchmark configuration is specified in a TOML file (default: `gpt_engineer/benchmark/default_bench_config.toml`).

## Development

### Getting Started

To set up gpt-engineer as a developer:

```bash
git clone git@github.com:gpt-engineer-org/gpt-engineer.git
cd gpt-engineer
poetry install
poetry shell
```

Then install the `pre-commit` hooks:

```bash
pre-commit install
```

### Code Style

The project uses [`pre-commit`](https://pre-commit.com/) to run [`black`](https://black.readthedocs.io/en/stable/index.html) and [`ruff`](https://beta.ruff.rs/docs/) on every commit.

If `pre-commit` modifies files during commit, simply `git add` the modified files again and commit.

If `pre-commit` appears to pass locally but fails in the build pipeline, run `pre-commit run --all-files` to force `pre-commit` to execute checks on all files.

### Contributing

The main contribution avenues are:

- **Pull request**: implement code and have it reviewed and potentially merged by the maintainers
- **Bug report**: report when something in gpt-engineer doesn't work (do not report errors in programs written *by* gpt-engineer)
- **Feature request**: provide a detailed sketch about something you want to have implemented
- **Discussion**: raise awareness of a potential improvement

By participating in this project, you agree to abide by the [code of conduct](.github/CODE_OF_CONDUCT.md).

Code that is likely to introduce breaking changes, or significantly change the user experience, requires [board approval](GOVERNANCE.md) to be merged. Smaller code changes can be merged directly.

## Testing

The project uses `pytest` for testing and `tox` for running tests across multiple Python versions (3.10, 3.11, and 3.12).

To run the test suite:

```bash
poetry run pytest --cov=gpt_engineer --cov-report=xml -k 'not installed_main_execution'
```

Tests that require a valid `OPENAI_API_KEY` are marked with `requires_key` and can be deselected with `-m "not requires_key"`.

To run tests across all supported Python versions:

```bash
tox
```

## Documentation

Documentation is hosted on [Read the Docs](https://gpt-engineer.readthedocs.io/en/latest/).

To build documentation locally:

```bash
poetry install
cd docs/
python create_api_rst.py
make html
```

Alternatively, to rebuild the docs on changes with live-reload in the browser:

```bash
sphinx-autobuild . _build/html
```

## Governance

The governance model of GPT-Engineer is documented in [GOVERNANCE.md](GOVERNANCE.md). The Project Board is the central decision-making body for the project, overseeing both strategic and technical decisions.

Current board members:
- Anton Osika
- Axel Theorell
- Corey Gallon
- Peter Harrington
- Theo McCabe

## Acknowledgements

The prompt for the `improve code` step is strongly based on Paul's prompt in [Aider](https://github.com/paul-gauthier/aider/blob/main/aider/coders/editblock_coder.py). See [Acknowledgements.md](Acknowledgements.md) for details.

## Disclaimer

GPT-engineer is an experimental application and is provided "as-is" without any warranty, express or implied. By using this software, you agree to assume all risks associated with its use. Please see the full [DISCLAIMER.md](DISCLAIMER.md) for details.

Note that the use of the GPT-4 language model can be expensive due to its token usage. By utilizing this project, you acknowledge that you are responsible for monitoring and managing your own token usage and the associated costs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Copyright (c) 2023 Anton Osika

By contributing to gpt-engineer, you agree that your contributions will be licensed under the LICENSE file of the project.
