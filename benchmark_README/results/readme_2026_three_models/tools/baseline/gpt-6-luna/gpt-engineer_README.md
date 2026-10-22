# GPT Engineer

GPT Engineer is a Python command-line tool for turning natural-language instructions into software. It sends a project prompt to a language model, can ask questions to clarify requirements, and generates or proposes changes to project files. It also supports improving existing code, running generated entrypoints, and optional self-healing when execution fails.

The package is in beta. Generated code and actions should be reviewed before use; you are responsible for checking that they are safe, legal, and appropriate.

## Requirements

- Python 3.10–3.12
- An API key for the model provider you use. OpenAI is the default provider; supported options also include Anthropic models, Azure OpenAI, and OpenAI-compatible local or hosted endpoints.
- Git is optional, but the CLI can use it when available.

## Installation

Install the latest stable package with pip:

```bash
python -m pip install gpt-engineer
```

To install from source, use Poetry:

```bash
git clone https://github.com/gpt-engineer-org/gpt-engineer.git
cd gpt-engineer
poetry install
poetry shell
```

The repository’s `make install` target installs Poetry dependencies and the pre-commit hooks:

```bash
make install
```

## Configure credentials

Set `OPENAI_API_KEY` in your environment:

```bash
export OPENAI_API_KEY="your-api-key"
```

Alternatively, copy `.env.template` to `.env` and add the key there. The CLI loads environment variables from `.env` when `OPENAI_API_KEY` is not already set.

On Windows Command Prompt:

```cmd
set OPENAI_API_KEY=your-api-key
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-api-key"
```

For Anthropic models, provide `ANTHROPIC_API_KEY` in the environment or `.env` file. See [Windows setup](WINDOWS_README.md) for additional installation and environment-variable instructions.

## Quickstart

Create a project directory and write the software request in a file named `prompt` (no extension):

```bash
mkdir my-project
printf "Write a Python program that converts Celsius to Fahrenheit." > my-project/prompt
```

Run the CLI from the project’s parent directory:

```bash
gpte my-project
```

The `gpte`, `ge`, and `gpt-engineer` commands invoke the same CLI. You can also run `gpt-engineer` with a project path argument. If the project has no `prompt` file, the CLI asks for the request interactively.

To request changes to an existing project, put an improvement request in its `prompt` file and run:

```bash
gpte my-project --improve
```

Improve mode offers interactive file selection. The CLI shows proposed changes and asks before applying them. Use `--skip-file-selection` to skip the interactive selection step.

For complete help, including all available flags, run:

```bash
gpte --help
```

## CLI options

The CLI accepts a project path, which defaults to the current directory (`.`). Useful options include:

| Option | Purpose |
| --- | --- |
| `--model`, `-m` | Choose a model ID. Defaults to the `MODEL_NAME` environment variable, or `gpt-4o` if unset. |
| `--temperature`, `-t` | Set response randomness; defaults to `0.1`. |
| `--improve`, `-i` | Propose changes to an existing project. |
| `--clarify`, `-c` | Discuss the specification before implementation. |
| `--lite`, `-l` | Generate using only the main prompt. |
| `--self-heal` | Try to fix generated code when execution fails. |
| `--prompt_file` | Use a prompt at a relative path other than `prompt`. |
| `--entrypoint_prompt` | Supply a separate entrypoint requirements file. |
| `--image_directory` | Provide a directory of images with the request. |
| `--use-custom-preprompts` | Copy the default preprompts into the project and use the project’s versions. |
| `--llm-via-clipboard` | Communicate with the model through clipboard input and output. |
| `--use_cache` | Cache model responses in `.langchain.db` to reuse them across runs. |
| `--no_execution` | Set up the run without calling the LLM or writing code. |
| `--sysinfo` | Print system information for debugging. |

Improve mode cannot be combined with clarify or lite mode. See `gpte --help` for the full option list, including Azure configuration, logging, and diff parsing settings.

## Model configuration

The default CLI model is `gpt-4o`. Set `MODEL_NAME` to choose a different model, or pass `--model`. For Azure OpenAI, set `OPENAI_API_KEY`, pass the service URL using `--azure`, and provide the Azure deployment name as the model. `OPENAI_API_VERSION` can be set to override the API version used by the Azure integration.

The project also documents using OpenAI-compatible APIs for local or hosted models. Configure `OPENAI_API_BASE`, `OPENAI_API_KEY`, `MODEL_NAME`, and `LOCAL_MODEL` as appropriate for the provider. Refer to [Using with open/local models](docs/open_models.md) for the documented llama.cpp and OpenRouter examples.

## Project configuration

The package includes support for a `gpt-engineer.toml` TOML configuration structure. Its documented fields include:

- `[paths]`: optional `base` and `src` paths.
- `[run]`: optional `build`, `test`, `lint`, and `format` commands.
- `[gptengineer-app]`: a required `project_id` when this section is present, and an optional list of OpenAPI schema URLs.

The configuration helpers can read and write this format. The benchmark runner uses a separate TOML configuration; its default file is `gpt_engineer/benchmark/default_bench_config.toml`.

## Docker

The repository includes a Docker image and Compose configuration. With Docker installed, build and run the image from the repository root:

```bash
docker build --rm -t gpt-engineer -f docker/Dockerfile .
docker run -it --rm \
  -e OPENAI_API_KEY="your-api-key" \
  -v ./my-project:/project \
  gpt-engineer
```

The container runs the CLI against `/project`. Alternatively, configure `.env` and the project volume in `docker-compose.yml`, then run:

```bash
docker compose run --rm gpt-engineer
```

See [`docker/README.md`](docker/README.md) for Docker setup details.

## Development

Install the project and activate its Poetry environment:

```bash
poetry install
poetry shell
pre-commit install
```

The pre-commit configuration runs Black and Ruff, along with checks for TOML, YAML, private keys, end-of-file newlines, and trailing whitespace. To run the hooks across the repository:

```bash
pre-commit run --all-files
```

Contributions should follow the project’s established style and include tests for relevant changes. See [contributing guidelines](.github/CONTRIBUTING.md) and the [code of conduct](.github/CODE_OF_CONDUCT.md).

## Testing and benchmarks

Run the test suite with pytest:

```bash
poetry run pytest
```

Some tests require a valid `OPENAI_API_KEY`; they are marked `requires_key`. To exclude those tests:

```bash
poetry run pytest -m "not requires_key"
```

The Tox configuration covers Python 3.10, 3.11, and 3.12. To run its configured checks:

```bash
tox
```

The benchmark CLI is available as `bench`. It takes a Python agent file containing `default_config_agent` and an optional benchmark configuration path:

```bash
bench --help
bench path/to/agent.py
```

The benchmark runner supports task selection through TOML configuration and can optionally write YAML results. Benchmark runs may call a language model and execute generated code.

## Documentation

Documentation sources are in `docs/` and use Sphinx. Install the documentation dependencies and build the HTML site:

```bash
poetry install --with docs
cd docs
python create_api_rst.py
make html
```

The generated site is placed in `docs/_build/html`. For automatic rebuilds while editing, the documentation guide also describes using `sphinx-autobuild`.

## Privacy, costs, and safety

Model requests may be processed or stored by the provider. The project’s optional usage-data collection occurs only when a `.gpte_consent` file is present in the gpt-engineer directory; data passing through the tool to a third party may be retained by that provider. Model usage can incur costs, so monitor provider usage and limits. Review [`TERMS_OF_USE.md`](TERMS_OF_USE.md) and [`DISCLAIMER.md`](DISCLAIMER.md) before use.

## License

GPT Engineer is distributed under the MIT License. See [`LICENSE`](LICENSE) for the full license text.
