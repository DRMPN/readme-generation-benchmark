# Dialog2Graph

**Dialog2Graph** is a project for creating dialog graphs based on input dialogs. It provides a set of LLM-powered pipelines that turn collections of task-oriented dialogs into structured dialog graphs — directed graphs whose nodes carry assistant/user utterances and whose edges represent transitions between conversation states — along with tooling for generating synthetic dialog data, augmenting existing dialogs, and evaluating the quality of generated graphs.

- **Version:** 0.1.1
- **License:** MIT
- **Language:** Python (>=3.10, <3.13)
- **Package management:** Poetry

## Key Features

- **Graph generation pipelines** — three main pipelines for building dialog graphs from dialogs:
  - `d2g_light` — a lightweight, three-stage pipeline
  - `d2g_llm` — an LLM-driven three-stage pipeline
  - `d2g_extender` — a pipeline that extends/increments existing graphs with new dialogs
- **Synthetic data generation** — generate dialog datasets for a given topic, including dialog augmentation and complex dialog generation
- **Evaluation framework** — a registry of metrics, including LLM-based metrics/validators and non-LLM metrics (graph triplet comparison, semantic similarity, Jaccard-based measures), plus automatic validators
- **CLI tool** — a Click-based command-line interface for data and graph generation
- **Prompt caching** — optional PostgreSQL-backed prompt caching to reduce redundant LLM calls
- **Topic generation** — a pipeline for generating conversation topics

## Project Structure

```
dialog2graph/            Main package
├── cli/                 Click-based CLI entrypoints
├── datasets/            Dialog augmentation and complex dialog generation
├── metrics/             Evaluation metrics (LLM and non-LLM), validators, similarity
├── pipelines/           Core abstractions and d2g pipelines
│   ├── core/            Base classes (Dialog, Graph, Pipeline, algorithms, schemas)
│   ├── d2g_light/       Lightweight pipeline
│   ├── d2g_llm/         LLM-based pipeline
│   ├── d2g_extender/    Graph extension pipeline
│   ├── topic_generation/
│   └── helpers/
├── utils/               Logging, prompt caching, vector stores, helpers
examples/                Jupyter notebooks and example configs
experiments/             Research experiments (each is its own Poetry project)
docs/                    Sphinx documentation sources
tests/                   Pytest test suite
scripts/                 Test/lint/metric-check entry scripts
prompt_cache/            Docker Compose setup for the PostgreSQL prompt cache
```

The `experiments/` directory contains dated, self-contained experiment projects (e.g., `exp2025_03_12_rec_models_incrementation`, `exp2025_03_18_embedding_grouper`) used during research. Each experiment is an independent Poetry project; some reference the main package via a local path dependency (`dialog2graph = {path = "../.."}`).

## Installation

The project uses [Poetry](https://python-poetry.org/). Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd dialog2graph
poetry install
```

Optional dependency groups (installed with `poetry install --with <group>`):

- `docs` — Sphinx documentation toolchain (sphinx, nbsphinx, pydata-sphinx-theme, etc.)
- `lint` — Ruff linter/formatter
- `tests` — pytest, pytest-cov, coverage
- `dev` — ipykernel, deptry

Core dependencies include `langchain`, `langchain-openai`, `langchain-community`, `langchain-chroma`, `langchain-huggingface`, `sentence-transformers`, `networkx`, `pandas`, `pydantic`, `click`, `pyyaml`, `matplotlib`, `datasets`, and `psycopg2-binary`.

## Configuration

### Environment variables

The CLI loads environment variables from a `.env` file (default path: `.env`, configurable via `--env`). LLM access (e.g., OpenAI API keys) is provided through environment variables. If you use the PostgreSQL prompt cache, the Compose file also expects `POSTGRES_PASSWORD` and `PROMPT_CACHE_PASSWORD`.

### Pipeline configuration (YAML)

Pipelines are configured via YAML files:

- `cfg.yml` — pipeline configuration (see `examples/cli_usage/cfg.yml` and `tests/cli/cfg.yml`)
- `models_config.yml` — model storage configuration listing the models used by a pipeline (see `examples/pipeline_usage/models_config.yml`)

### Input data format

Dialogs and graphs are stored as JSON. Each dialog record contains a list of `messages`, where each message has `text` and `participant` (`"assistant"` or `"user"`), plus optional `topic` and `validate` fields. Graphs contain:

- `nodes` — each with `id`, `label`, `is_start` (boolean), and `utterances` (list of strings)
- `edges` — each with `source`, `target`, and `utterances`

Examples of this format can be found in `tests/test_pipelines_data.json` and `examples/example_data.json`.

## Usage

### CLI

The package installs a `dialog2graph` console entry point (`dialog2graph.cli.main:cli`). Available commands:

```bash
# Generate dialog data for a given topic
dialog2graph gen-data --topic "Fixing a calendar sync delay" \
    --cfg cfg.yml --output generated_data.json

# Generate a graph from dialogs using the light pipeline
dialog2graph gen-graph-light --dialogs dialogs.json \
    --cfg cfg.yml [--tgraph true_graph.json] \
    [--output graph.json] [--report report.json] [--eval]

# Generate a graph from dialogs using the LLM pipeline
dialog2graph gen-graph-llm --dialogs dialogs.json \
    --cfg cfg.yml [--tgraph true_graph.json] \
    [--output graph.json] [--report report.json] [--eval]

# Generate/extend a graph using the extender pipeline
dialog2graph gen-graph-extender ...
```

Common options:

| Option | Description |
|--------|-------------|
| `--env` / `-e` | Path to `.env` file (default: `.env`) |
| `--cfg` / `-c` | Path to `cfg.yml` pipeline config (default: `cfg.yml`) |
| `--topic` / `-t` | Topic for dialog generation (`gen-data`, required) |
| `--dialogs` / `-d` | Input dialogs file (graph generation, required) |
| `--tgraph` / `-tg` | Optional ground-truth graph file |
| `--output` / `-o` | Output graph/data file |
| `--report` / `-r` | Output report file |
| `--eval` / `-ev` | Run pipeline evaluations |

(Use `dialog2graph --help` to see the exact command names and options in your installed version.)

### Python API

The library can also be used programmatically. The `examples/` directory provides Jupyter notebooks covering:

- **Base classes usage** (`examples/basics/base_classes_usage.ipynb`) — working with the core `Dialog`, `Graph`, and pipeline abstractions
- **Pipeline usage** (`examples/pipeline_usage/pipeline_example.ipynb`) — running pipelines with a `models_config.yml` and multiple dialogs
- **CLI usage** (`examples/cli_usage/main.ipynb`)
- **Data generation** (`examples/data_generation/`) — looped graph generation and LLM prompt caching
- **Dialog augmentation** (`examples/dialog_augmentation/dialogue_augmentation_example.ipynb`)
- **Dialog extension** (`examples/dialog_extension/dialog_extender_example.ipynb`)
- **Metrics evaluation** (`examples/evaluation/examples_of_metrics_usage.ipynb`)

### Prompt caching

An optional PostgreSQL-based prompt cache avoids re-paying for identical LLM calls. Set it up with Docker Compose:

```bash
cd prompt_cache
cp .env.example .env   # define POSTGRES_PASSWORD and PROMPT_CACHE_PASSWORD
docker compose up -d
```

The service runs a PostgreSQL instance exposed on port 5432, initialized via `prompt_cache/init.sql`, and connected to from the library through the utilities in `dialog2graph/utils/prompt_caching.py`.

## Metrics and Evaluation

The `dialog2graph.metrics` package provides an algorithm registry of evaluation tools:

- **LLM metrics and validators** (`metrics/llm_metrics`, `metrics/llm_validators`) — prompt-driven evaluation of generated graphs and dialogs
- **Non-LLM metrics** (`metrics/no_llm_metrics`) — including graph triplet comparison, semantic similarity metrics (Jaccard-based), annotation pipelines, and key-to-graph utilities
- **Non-LLM validators** (`metrics/no_llm_validators`) — automatic structural checks

Pipeline runs can produce metric reports (stored, for example, under `tests/metrics_results/`), and CI runs a dedicated `check_metrics` workflow.

## Development

### Code style

Linting and formatting are handled by [Ruff](https://docs.astral.sh/ruff/) (configured in `ruff.toml`), exposed through [poethepoet](https://github.com/nat-n/poethepoet) tasks:

```bash
poetry run poe lint      # check code style
poetry run poe format    # apply formatting
```

### Testing

The test suite uses pytest and includes CLI tests, pipeline tests (`test_d2g_light.py`, `test_d2g_llm.py`, `test_d2g_extender.py`), metric tests, validator tests, dialog augmentation tests, and topic generation tests:

```bash
poetry run poe test      # quick test suite
poetry run poe coverage  # run tests with coverage reporting
```

A dedicated `check_metrics` task (`poetry run poe check_metrics`) tests the D2G pipelines' metrics.

### Documentation

Documentation is built with Sphinx (sources in `docs/source/`, including user guides for basic usage, CLI usage, graph generation, graph extension, evaluation, and data generation):

```bash
cd docs
make html
```

### CI

The repository includes GitHub Actions workflows for:

- Running tests (`tests.yml`) and release testing (`test_release.yml`)
- Code style checks (`codestyle.yml`)
- Coverage reporting (`coverage.yml`)
- Pipeline metrics checks (`check_metrics.yml`)
- Building and publishing docs (`build_and_publish_docs.yml`)
- Building and publishing releases (`build_and_publish_release.yml`)

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and `docs/how_to_contribute.md` for contribution guidelines. Additional development notes are available in `docs/source/development.rst`, and `docs/doc_structure.md` describes the documentation layout.

## Experiments

The `experiments/` directory preserves the research history behind the library, covering topics such as prompt engineering for graph generation, synthetic data creation, dialog augmentation at dataset scale, embedding-based node grouping, graph incrementation with different LLMs (e.g., GPT-4o, o1-mini, o3-mini), and dataset preparation/pushing to the Hugging Face Hub. Each experiment directory contains its own README describing its purpose and results.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Anastasia Voznyuk
