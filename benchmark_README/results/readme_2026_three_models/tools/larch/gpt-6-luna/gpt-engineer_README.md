# GPT Engineer

GPT Engineer turns a plain-language description of a software project into a working codebase. Give it a prompt, let it clarify what you want, and it will generate files in a project workspace for you to review and run.

This repository includes the command-line application, AI interfaces, file and project management tools, documentation, examples, and tests.

## Contents

- [Requirements](#requirements)
- [Install](#install)
- [Quick start](#quick-start)
- [How it works](#how-it-works)
- [Working with an existing project](#working-with-an-existing-project)
- [Configuration and models](#configuration-and-models)
- [Run with Docker](#run-with-docker)
- [Development](#development)
- [Documentation and examples](#documentation-and-examples)
- [Safety and limitations](#safety-and-limitations)
- [Contributing](#contributing)
- [License and terms](#license-and-terms)

## Requirements

- Python version compatible with the versions declared in `pyproject.toml`
- An API key for the AI provider you configure
- An internet connection when using a hosted AI provider

Generated projects may have their own runtime and dependency requirements.

## Install

Install the package from PyPI:

```bash
pip install gpt-engineer
```

Alternatively, install this repository for development:

```bash
git clone <repository-url>
cd gpt-engineer-i9d_jxfv
pip install -e .
```

Set the API key required by your chosen provider. For the OpenAI interface, for example:

**macOS / Linux**

```bash
export OPENAI_API_KEY="your-api-key"
```

**PowerShell**

```powershell
$env:OPENAI_API_KEY = "your-api-key"
```

Keep API keys private. Do not commit them to your project or share them in prompts.

## Quick start

Create a directory for the project and write a prompt in a file named `prompt`:

```bash
mkdir -p projects/hello-app
printf "Create a small command-line app that greets the user by name.\n" \
  > projects/hello-app/prompt
```

Run GPT Engineer against that directory:

```bash
gpte projects/hello-app
```

The program reads the prompt, may ask follow-up questions, and generates project files in the project workspace. Review the generated files before running them.

To see the options supported by your installed version:

```bash
gpte --help
```

## How it works

A typical run follows this flow:

1. **Describe the project.** GPT Engineer reads the project’s `prompt` file.
2. **Clarify requirements.** Depending on the workflow, it may ask questions to resolve ambiguity.
3. **Generate files.** The AI produces code and supporting files for the requested project.
4. **Review and iterate.** Inspect the output, adjust the prompt, and run GPT Engineer again as needed.
5. **Run the project yourself.** Install any dependencies and start the generated application using its own instructions.

The repository contains components for AI provider interfaces, agents and steps, prompt handling, project configuration, file selection, file storage, execution environments, and conversion of AI responses into files. It also includes support for collecting feedback or learning data; consult the relevant prompts and documentation before enabling those features.

## Working with an existing project

You can point GPT Engineer at a directory containing an existing codebase and describe the requested changes in its `prompt` file. Check the CLI help for the workflows and options available in your version.

Before using it on valuable work:

- Commit or back up the project.
- Review which files the tool is allowed to read or change.
- Inspect diffs after generation.
- Run the project’s tests and checks yourself.

GPT Engineer can generate code, but it does not guarantee that changes are correct, secure, or compatible with your environment.

## Configuration and models

This repository includes OpenAI and LangChain interfaces, project configuration support, and benchmark configuration files. The available models and configuration options depend on the installed version and the interface you use.

Use the command-line help for supported flags:

```bash
gpte --help
```

For repository-level configuration and model details, see the source files and documentation, including `gpt_engineer/core/project_config.py`, `gpt_engineer/ai.py`, `gpt_engineer/benchmarks/bench_config.py`, and `docs/`.

## Run with Docker

The repository includes a `Dockerfile`, `docker-compose.yml`, and an entrypoint script for Docker-based use. Docker can help isolate the application environment, but it does not make generated code inherently safe. Review the Docker configuration and any mounted directories before running containers.

## Development

Install the project’s development dependencies using Poetry:

```bash
poetry install
```

Run the test suite:

```bash
poetry run pytest
```

You can also run the tests in an available Python environment with:

```bash
pytest
```

The repository includes `tox.ini` and a `Makefile` for additional development workflows. Check those files for the commands supported by your checkout.

## Documentation and examples

The `docs/` directory contains documentation on installation, usage, tracing, and supported models. The repository also includes example prompts, generated code, chat transcripts, and benchmark utilities.

Start with:

- `docs/index.rst` — documentation index
- `docs/quickstart.rst` — quick start
- `docs/installation.rst` — installation guidance
- `docs/open_models.md` — information about open models
- `docs/tracing_debugging.md` — tracing and debugging
- `ROADMAP.md` — project roadmap

## Safety and limitations

GPT Engineer sends prompts and, depending on the configured workflow, project context to the AI provider you select. Review that provider’s data-handling terms before using private or sensitive material.

Generated code can contain bugs, insecure patterns, destructive operations, or unsuitable dependencies. Treat it as untrusted input:

- Inspect generated code before executing it.
- Run it in an environment with only the permissions it needs.
- Avoid providing secrets or sensitive data in prompts.
- Test changes before deploying or relying on them.

AI output may be incomplete or incorrect and should be reviewed by a qualified developer.

## Contributing

Contributions are welcome. Read `GOVERNANCE.md` and the repository’s contribution guidance before opening a pull request. Please include tests for behavior changes where appropriate.

## License and terms

See `LICENSE`, `TERMS_OF_USE.md`, and `DISCLAIMER.md` for the applicable license, terms, and disclaimers.
