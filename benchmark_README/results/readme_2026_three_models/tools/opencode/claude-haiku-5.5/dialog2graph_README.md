# Dialog2Graph

Dialog2Graph is a project for creating dialog graphs from input dialogs. It extends the [Chatsky project](https://github.com/deeppavlov/chatsky) by helping to create Chatsky flows and scripts with the help of Large Language Models (LLMs). The project is based on the dialog2graph approach, which transforms conversational data into structured, graph-based representations.

A **dialog graph** is a graph where **nodes** represent key elements of a conversation (such as utterances, intents, or states) and **edges** define the transitions between them.

## Features

- **Graph generation from dialogs** through three pipelines:
  - `gen-graph-light`: the light pipeline (`D2GLightPipeline`, stages in `three_stages_light`).
  - `gen-graph-llm`: the LLM pipeline (`D2GLLMPipeline`).
  - `gen-graph-extender`: the extender pipeline (`D2GExtenderPipeline`), which extends an existing graph using new dialogs.
- **Dialog generation for a topic** through `TopicGenerationPipeline` (a looped graph generator in `dialog2graph/datasets/complex_dialogs`), also exposed as the `gen-data` CLI command (see [Known issues](#known-issues)).
- **Dialog augmentation** in `dialog2graph/datasets/augment_dialogs`.
- **Graph comparison and evaluation metrics** in `dialog2graph/metrics`, including LLM-based and non-LLM validators and metrics. Evaluation is enabled with the `--eval` / `-ev` flag.
- **Reports** written in `.json`, `.csv`, `.html`, `.md`, or `.txt` format.
- **Core classes** `Dialog` and `Graph`, importable from the top-level `dialog2graph` package.

## Requirements

- Python 3.10, 3.11, or 3.12 (`python = "^3.10,<3.13"` in `pyproject.toml`)
- [Poetry](https://python-poetry.org/) 1.8.4 (the version used in the project documentation and CI)
- Access to LLM and embedding models for the generation pipelines. Model configuration is described in [Model configuration](#model-configuration).

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/deeppavlov/dialog2graph.git
cd dialog2graph
poetry install
```

To visualize graphs, the documentation suggests adding PyGraphviz to the Poetry environment (see the [PyGraphviz installation guide](https://pygraphviz.github.io/)):

```bash
poetry add pygraphviz
```

Poetry installs the `dialog2graph` command-line tool from the `[tool.poetry.scripts]` section of `pyproject.toml`.

## Configuration

### Environment variables (`.env`)

The CLI and pipelines load a `.env` file with `python-dotenv`. Store credentials there rather than in code or configuration files. Do not commit `.env`; it is listed in `.gitignore`.

Environment variables read by the code include:

| Variable | Used for |
| --- | --- |
| `OPENAI_API_KEY` | API key for OpenAI-compatible models (used by the `keys2graph` metrics code) |
| `OPENAI_API_BASE` | Base URL for OpenAI-compatible models (defaults to `https://api.openai.com/v1` in some code paths) |
| `EMBEDDING_MODEL` | Embedding model name for the `keys2graph` metrics code |
| `SQLALCHEMY_DATABASE_URI` | Database URI for the LLM response cache used by the CLI commands. If it is missing or invalid, the CLI falls back to an in-memory cache. |
| `DATABASE_URL` | Database URL read by `dialog2graph/utils/prompt_caching.py`. If it is missing, that module falls back to an in-memory cache. |

### Model configuration

Models are configured in a YAML file (passed with `--cfg` / `-c`, default `cfg.yml`). `ModelStorage.load()` reads a mapping in which each key is a model name and each value has:

- `config`: keyword arguments passed to the model class. Use `model_name`, not `name`.
- `model_type`: either `ChatOpenAI` (LLMs) or `HuggingFaceEmbeddings` (embedding models).

Example:

```yaml
three_stages_light_formatting_llm:v1:
  config:
    model_name: gpt-4o-mini
    temperature: 0
  model_type: ChatOpenAI

three_stages_light_sim_model:v1:
  config:
    model_name: BAAI/bge-m3
    model_kwargs:
      device: cpu
  model_type: HuggingFaceEmbeddings
```

Each pipeline uses default model keys, which you can override with its constructor arguments:

| Pipeline | Default model keys |
| --- | --- |
| Light (`D2GLightPipeline`) | `three_stages_light_filling_llm:v1`, `three_stages_light_formatting_llm:v1`, `three_stages_light_sim_model:v1` |
| LLM (`D2GLLMPipeline`) | `three_stages_llm_grouping_llm:v1`, `three_stages_llm_filling_llm:v1`, `three_stages_llm_formatting_llm:v1`, `three_stages_llm_sim_model:v1` |
| Extender (`D2GExtenderPipeline`) | `extender_grouping_llm:v1`, `extender_extending_llm:v1`, `extender_filling_llm:v1`, `extender_formatting_llm:v1`, `extender_dialog_llm:v1`, `extender_sim_model:v1` |
| Topic generation (`TopicGenerationPipeline`) | `looped_graph_generation_llm:v1`, `looped_graph_validation_llm:v1`, `looped_graph_cycle_ends_llm:v1`, `looped_graph_theme_validation_llm:v1` |

Keys in your configuration file must match these names (or the names you pass to the pipeline constructors) for the pipeline to find its models.

## Input data format

Dialogs are lists of messages, where each message has a `participant` (`user` or `assistant`) and a `text`. The parser accepts these shapes, either as Python objects or in a JSON file:

```json
[{"participant": "user", "text": "Hi, I need help with my account."}, {"participant": "assistant", "text": "Sure, what seems to be the problem?"}]
```

```json
{"dialogs": [[{"participant": "user", "text": "..."}, {"participant": "assistant", "text": "..."}]]}
```

The parser also accepts a list of dialogs, each given as `{"messages": [...]}`.

A graph file is a JSON object with a `graph` key (for the supported graph, used by the extender) or a `true_graph` key (for the reference graph used in evaluation). Each graph has `nodes` and `edges`, as in `examples/example_data.json`.

Input files must be `.json`.

## Usage

### Command-line interface

The CLI is available as `dialog2graph` after installation. Run `dialog2graph --help` for the full list of commands.

Generate a graph from dialogs with the light pipeline and write a report:

```bash
poetry run dialog2graph gen-graph-light -c cfg.yml -d dialogs.json -o graph.json -r report.json -ev
```

Other graph commands accept the same core options:

```bash
poetry run dialog2graph gen-graph-llm -c cfg.yml -d dialogs.json -o graph.json -r report.md
poetry run dialog2graph gen-graph-extender -c cfg.yml -d dialogs.json -g existing_graph.json -o graph.json
```

Commands and options:

| Command | Purpose | Options |
| --- | --- | --- |
| `gen-data` | Generate dialog data for a topic (see [Known issues](#known-issues)) | `-t/--topic` (required), `-o/--output` (default `generated_data.json`), `-c/--cfg`, `-e/--env` |
| `gen-graph-light` | Generate a graph with the light pipeline | `-d/--dialogs` (required), `-tg/--tgraph`, `-o/--output`, `-r/--report`, `-ev/--eval`, `-c/--cfg`, `-e/--env` |
| `gen-graph-llm` | Generate a graph with the LLM pipeline | Same as `gen-graph-light` |
| `gen-graph-extender` | Extend a graph from dialogs | Same as `gen-graph-light`, plus `-g/--graph` (input graph file) |

Notes on the options:

- `-c/--cfg` defaults to `cfg.yml`, and `-e/--env` defaults to `.env`.
- If `-o/--output` is not given, the graph is printed to standard output.
- If `-r/--report` is not given, the report is saved as `./report_<pipeline>_<timestamp>.json`.
- The report format is chosen from the file extension: `.json`, `.csv`, `.html`, `.md`, or `.txt`.
- `-ev/--eval` runs additional evaluation metrics. The documentation notes that this usually slows generation and increases token use.

An example configuration is in `examples/cli_usage/cfg.yml`, although its layout (with a top-level `models:` key) differs from the format read by `ModelStorage.load()` described above.

### Python API

The top-level package exports `Dialog` and `Graph`:

```python
from dialog2graph import Dialog, Graph
```

The following example runs the LLM pipeline on a dialog file:

```python
from pathlib import Path

from dialog2graph.pipelines.model_storage import ModelStorage
from dialog2graph.pipelines.d2g_llm.pipeline import D2GLLMPipeline
from dialog2graph.pipelines.helpers.parse_data import PipelineRawDataType

ms = ModelStorage()
ms.load("cfg.yml")

pipeline = D2GLLMPipeline("d2g_llm", ms)
raw_data = PipelineRawDataType(dialogs=Path("dialogs.json"), true_graph=None)
result, report = pipeline.invoke(raw_data, enable_evals=False)

print(result.graph_dict["nodes"])
print(result.graph_dict["edges"])
print(report)
```

The Sphinx user guides show further examples with `Graph`, `Dialog`, sampling with `RecursiveDialogSampler`, and the extender and augmentation workflows. Those guides are written as Sphinx pages under `docs/source/userguides/`.

## Data

The user guides reference a generated dataset of 402 dialog graphs on various topics, hosted on Hugging Face at [`DeepPavlov/d2g_generated`](https://huggingface.co/datasets/DeepPavlov/d2g_generated). The data collections are described in `docs/source/research/data_collections.rst`. The repository also contains sample data in `examples/` and `tests/`.

## Examples

The `examples/` directory contains Jupyter notebooks and sample data:

- `examples/basics/`: base classes (`Graph`, `Dialog`)
- `examples/cli_usage/`: CLI usage
- `examples/pipeline_usage/`: pipeline usage
- `examples/dialog_augmentation/`: dialog augmentation
- `examples/dialog_extension/`: dialog extension
- `examples/data_generation/`: data generation, including caching and `LoopedGraphGenerator`
- `examples/evaluation/`: evaluation metrics

The `experiments/` directory contains research experiments. Each experiment is in its own folder, named `exp<YYYY>_<MM>_<DD>_<hypothesis>`.

## Testing and linting

Tests live in `tests/` and run with pytest:

```bash
poetry install --with tests
poetry run poe test        # run tests in tests/
poetry run poe coverage    # run tests with coverage; the threshold is 80%
```

The tests in `tests/cli/` are skipped when no `.env` file is found.

Code style uses [Ruff](https://docs.astral.sh/ruff/) (configured in `ruff.toml`):

```bash
poetry install --with lint
poetry run poe lint        # check (ruff check --fix)
poetry run poe format      # format (ruff format)
```

Continuous integration (in `.github/workflows/`):

- `test_release.yml` builds the package and runs `tests/` on Python 3.10, 3.11, and 3.12 across macOS, Windows, and Ubuntu.
- `coverage.yml` runs the coverage task on Ubuntu with Python 3.11.
- `codestyle.yml` runs the lint task on Ubuntu with Python 3.11.
- `build_and_publish_release.yml` builds and publishes the package with Poetry (manual trigger, `main` branch only).

## Known issues

- **`gen-data` does not run as written.** `dialog2graph/cli/commands/generate_data.py` calls `TopicGenerationPipeline.invoke(topic)` without the required `output_path` argument. It also runs the pipeline twice. The `gen-data` command should be considered unverified until this is fixed.
- The `gen-graph-light` help text refers to the "d2g_algo" pipeline; the code runs `D2GLightPipeline`.

## Documentation

Sphinx documentation sources are in `docs/source/`. Build instructions are in `docs/Makefile` and `docs/make.bat`. The documentation sections cover getting started, research concepts, user guides, the API reference (generated with `sphinx-autoapi`), development, and the team.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow, branch naming (`feat`, `fix`, `exp`), coding guidelines, and how to report issues. For development rules, see `docs/how_to_contribute.md`.

## Authors

Listed in `pyproject.toml`: Denis Kuznetsov, Chirkin Andrey, Anastasia Voznyuk, Anna Mikhailova, Maria Molchanova, and Yuri Peshkichev.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
