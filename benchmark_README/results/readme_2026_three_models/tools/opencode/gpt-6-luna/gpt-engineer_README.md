# GPT Engineer

GPT Engineer is a command-line tool for generating software from a natural-language prompt and improving existing projects with an AI model. In generation mode, it can also create an entrypoint script and, after asking for confirmation, run it locally.

The project is experimental. Review generated code before using it, and read the [disclaimer](DISCLAIMER.md) and [terms of use](TERMS_OF_USE.md).

## Requirements

- Python 3.10, 3.11, or 3.12 (the package requires Python `>=3.10,<3.13`).
- An API key for the model provider you configure. The standard quickstart uses an OpenAI API key.

## Install

Install the published stable package with pip:

```bash
python -m pip install gpt-engineer
```

Or install from a clone of this repository with Poetry:

```bash
git clone https://github.com/gpt-engineer-org/gpt-engineer.git
cd gpt-engineer
poetry install
```

## Quickstart

Set your OpenAI API key in the environment:

```bash
export OPENAI_API_KEY="your-api-key"
```

Alternatively, put `OPENAI_API_KEY` in a `.env` file in the working directory. On Windows, see [Windows setup](WINDOWS_README.md) for Command Prompt and PowerShell examples.

Create a project directory and a plain-text file named `prompt` inside it:

```text
my-project/
└── prompt
```

Write what you want to build in `my-project/prompt`, then run:

```bash
gpte my-project
```

The CLI also has the command names `gpt-engineer` and `ge`. It uses `gpt-4o` by default; select a different model with `--model` / `-m`:

```bash
gpte my-project --model MODEL_ID
```

If the `prompt` file is absent or empty, the CLI asks for the prompt interactively. Generated files are written into the project directory. In generation mode, GPT Engineer may create a `run.sh` entrypoint; it displays the script and asks before executing it. Inspect the generated files and script before approving execution.

## Improve an existing project

Place a `prompt` file in the project directory describing the changes you want, then run:

```bash
gpte my-project --improve
```

The CLI selects project files for the improvement request, shows the proposed changes, and asks before applying them. Use `--skip-file-selection` to skip the interactive file selection and use the generated TOML file directly.

## Useful options

Run `gpte --help` (or `gpt-engineer --help`) for the full option list. Common options include:

| Option | Purpose |
| --- | --- |
| `--improve`, `-i` | Propose changes to an existing project. |
| `--clarify`, `-c` | Discuss the specification with the model before implementation. |
| `--lite`, `-l` | Generate using only the main prompt. |
| `--self-heal`, `-sh` | Attempt to fix generated code when it fails. |
| `--model`, `-m` | Set the model ID. Defaults to `gpt-4o` (or `MODEL_NAME` if set). |
| `--temperature`, `-t` | Set response randomness; defaults to `0.1`. |
| `--azure`, `-a` | Use an Azure OpenAI endpoint. |
| `--prompt_file` | Set the prompt file path relative to the project directory; defaults to `prompt`. |
| `--entrypoint_prompt` | Provide a separate prompt file for entrypoint requirements. |
| `--image_directory` | Provide a project-relative directory of images as prompt input. |
| `--use_cache` | Cache model responses in `.langchain.db` for repeated requests. |
| `--use-custom-preprompts` | Use project-specific preprompts, copying the defaults into the project when needed. |
| `--llm-via-clipboard` | Communicate with the model through the clipboard. |

`--clarify` and `--lite` cannot be combined with `--improve`. For Azure, pass the Azure endpoint and use the deployment name as the model ID. Instructions for Azure, Anthropic, and OpenAI-compatible local or hosted models are in the [model configuration guide](docs/open_models.md).

## Development

Install the development dependencies and run the test suite with:

```bash
poetry install
poetry run pytest -k 'not installed_main_execution'
```

Documentation sources are in [`docs/`](docs/). The published documentation is at [gpt-engineer.readthedocs.io](https://gpt-engineer.readthedocs.io/en/latest/).

## Project links

- [Roadmap](ROADMAP.md)
- [Terms of use](TERMS_OF_USE.md)
- [Disclaimer](DISCLAIMER.md)
- [License](LICENSE) (MIT)
