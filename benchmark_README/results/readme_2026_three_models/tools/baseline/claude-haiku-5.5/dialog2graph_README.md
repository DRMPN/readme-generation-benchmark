# Dialog2Graph

Dialog2Graph is a Python project for creating dialog graphs from input dialogs. It extends the [Chatsky project](https://github.com/deeppavlov/chatsky) by supporting the creation of Chatsky flows and scripts with Large Language Models (LLMs). The project is developed by DeepPavlov and its contributors.

## Overview

A dialog graph is a structured representation of conversational data, where nodes hold assistant utterances and edges hold user utterances. The project provides tools to:

- **Generate graphs from dialogs** using several pipelines: a light pipeline (`d2g_light`), an LLM-based pipeline (`d2g_llm`), and an extender that adds dialogs to an existing graph (`d2g_extender`).
- **Sample dialogs from graphs** with `RecursiveDialogSampler`.
- **Generate synthetic dialogs and graphs** for a given topic with `LoopedGraphGenerator` and `CycleGraphGenerator`.
- **Augment dialogs** by paraphrasing utterances with `DialogAugmenter`.
- **Evaluate graphs and dialogs** with no-LLM and LLM metrics, and with validators.
- **Use a command-line interface** (`dialog2graph`) for data generation and graph generation.

The supported graph types, as stated in `CONTRIBUTING.md`, are chains, single cycles, multi-cycle graphs, and complex graphs with cycles. Single-node cycles are listed as currently unsupported.

Synthetic and real datasets are published on Hugging Face under the `DeepPavlov` organization, including `d2g_generated`, `d2g_real_dialogs`, and `d2g_generated_augmented`.

## Installation

The project uses [Poetry](https://python-poetry.org/) and requires Python `^3.10,<3.13`.

1. Install Poetry. The documentation recommends version 1.8.4:

    ```bash
    pipx install poetry==1.8.4
    ```

2. Clone the repository and install the dependencies:

    ```bash
    git clone https://github.com/deeppavlov/dialog2graph.git
    cd dialog2graph
    poetry install
    ```

3. Optional: to visualise graphs, add PyGraphviz to the Poetry environment:

    ```bash
    poetry add pygraphviz
    ```

    The documentation links to the [PyGraphviz installation page](https://pygraphviz.github.io/) for platform requirements.

4. Verify the installation by running any Python script:

    ```bash
    poetry run python <your_file_name>.py
    ```

## Configuration

### Environment variables

Credentials and other sensitive values should be stored in a `.env` file rather than hardcoded. The CLI loads a `.env` file through `python-dotenv`. Each CLI command accepts `--env` (`-e`), which defaults to `.env`.

The maintenance script `scripts/check_metrics.py` reads the following variables:

- `SQLALCHEMY_DATABASE_URI`: database URI used for the LLM response cache.
- `HUGGINGFACE_TOKEN`: token used to load the `DeepPavlov/d2g_generated_augmented` dataset.

### Prompt cache database

The `prompt_cache/` directory contains a Docker Compose file and an SQL initialisation script for a PostgreSQL database used as an LLM prompt cache. The Compose file reads `POSTGRES_PASSWORD` and `PROMPT_CACHE_PASSWORD` from the environment and exposes port `5432`. The `init.sql` script creates a `langchain_cache` database and a `langchain_user` role with limited privileges.

### Model configuration

Models are registered in a `ModelStorage` object by key, configuration, and model type (for example, `ChatOpenAI` or `HuggingFaceEmbeddings`). Pipelines then reference models by these keys:

```python
from langchain_openai import ChatOpenAI
from dialog2graph.pipelines.model_storage import ModelStorage

model_storage = ModelStorage()
model_storage.add(
    key="generation-llm",
    config={"model_name": "gpt-4o-mini-2024-07-18", "temperature": 0.7},
    model_type=ChatOpenAI,
)
```

The example files `examples/cli_usage/cfg.yml` and `examples/pipeline_usage/models_config.yml` show YAML configuration files. The CLI commands take a configuration file through `--cfg` (`-c`), which defaults to `cfg.yml`.

## Usage

### Python API

Core classes are exposed at the package level:

```python
from dialog2graph import Dialog, Graph

graph = Graph(graph_dict=graph_data)  # graph_data: {"edges": [...], "nodes": [...]}
graph.visualise()
```

Sampling dialogs from a graph:

```python
from dialog2graph.pipelines.core.dialog_sampling import RecursiveDialogSampler
from langchain_openai import ChatOpenAI

sampler = RecursiveDialogSampler()
model = ChatOpenAI(model="gpt-3.5-turbo")
dialogs = sampler.invoke(graph=graph, upper_limit=10, cycle_ends_model=model)
```

Generating a graph from dialogs with the LLM pipeline. Passing `enable_evals=True` includes metrics in the report, which may slow generation and increase token usage:

```python
from dialog2graph.pipelines.d2g_llm import LLMGraphGenerator

graph_generator = LLMGraphGenerator(
    model_storage=model_storage,
    formatting_llm="my_formatting_model",
    sim_model="my_embedding_model",
)
graph, report = graph_generator.invoke(data, enable_evals=True)
```

Other public components referenced in the documentation include `DialogAugmenter`, `LoopedGraphGenerator`, `LLMGraphExtender`, and `RawDGParser`. Evaluation utilities include `is_same_structure`, `match_graph_triplets`, `triplet_match_accuracy`, `compute_graph_metrics` (in `dialog2graph.metrics.no_llm_metrics.metrics`), and `is_greeting_repeated_regex` (in `dialog2graph.metrics.no_llm_validators`).

### Command-line interface

After installation, the `dialog2graph` command is available through Poetry:

```bash
poetry run dialog2graph --help
```

| Command | Purpose | Key options |
|---|---|---|
| `gen_data` | Generate dialog data for a topic | `--topic/-t` (required), `--output/-o` (default `generated_data.json`) |
| `gen_graph_light` | Generate a graph via the `d2g_light` pipeline | `--dialogs/-d` (required), `--tgraph/-tg`, `--output/-o`, `--report/-r`, `--eval/-ev` |
| `gen_graph_llm` | Generate a graph via the `d2g_llm` pipeline | Same options as `gen_graph_light` |
| `gen_graph_extender` | Extend a graph with dialogs via the `d2g_llm` extender | `--dialogs/-d` (required), `--graph/-g`, plus the options above |

All commands also accept `--env/-e` (default `.env`) and `--cfg/-c` (default `cfg.yml`).

Example:

```bash
poetry run dialog2graph gen_data -t "restaurant reservation" -o generated_data.json
```

The documentation and `tests/cli/` contain CLI usage examples.

### Documentation

Documentation is built with Sphinx from `docs/source/`. Build it from the project root with:

```bash
python -m poetry run sphinx-build -b html docs/source/ docs/build/
```

The user guides cover base classes, graph generation, synthetic generation, evaluation, the CLI, dialog augmentation, and graph extension.

## Development

### Setup

Install all optional dependency groups:

```bash
poetry install --with docs,lint,tests
```

Remove all virtual environments created by Poetry for the project with `poetry env remove --all`.

### Workflow

From `CONTRIBUTING.md`:

1. Create a branch. The preferred prefixes are `feat`, `fix`, and `exp`.
2. Make your changes, following PEP 8, writing docstrings for functions and classes, and adding unit tests for new features or bug fixes.
3. Check and format the code:

    ```bash
    poetry run poe lint
    poetry run poe format
    ```

4. Open a pull request with a clear name and a description of the changes.

To update the versions pinned in `poetry.lock`, run `poetry update`.

### Tasks

Tasks are defined in `pyproject.toml` under `[tool.poe.tasks]`:

| Task | Command | Description |
|---|---|---|
| `test` | `scripts.test:quick_test` | Runs pytest over `tests/` |
| `coverage` | `scripts.test:coverage` | Runs pytest with coverage and fails below 80% |
| `lint` | `scripts.codestyle:_check` | Runs `ruff check --fix` |
| `format` | `scripts.codestyle:_format` | Runs `ruff format` |
| `check_metrics` | `scripts.check_metrics:test_d2g_pipelines` | Compares pipeline metrics against the latest saved results |

### Experiments

Experiments live in the `experiments/` directory. Each experiment is stored in its own folder named `exp<YYYY>_<MM>_<DD>_<hypothesis>` and created with `poetry new` or `poetry init`. Images should not be added to experiment folders; external links should be used instead. Older work is kept in `experiments/old_experiments/`.

### Repository layout

- `dialog2graph/`: the library package, including `cli/`, `datasets/`, `metrics/`, `pipelines/`, and `utils/`.
- `docs/`: Sphinx documentation and contribution guides for documentation.
- `examples/`: Jupyter notebooks and sample data.
- `tests/`: pytest tests, test data, and stored metrics results.
- `scripts/`: helper scripts for testing, linting, and metric checks.
- `.github/workflows/`: CI workflows for tests, coverage, code style, metric checks, documentation, and releases.

## Testing

Run the test suite with:

```bash
poetry run poe test
```

To run coverage with an 80% threshold:

```bash
poetry run poe coverage
```

Some tests require credentials. For example, `tests/test_dialog_augmentation.py` skips the whole module when no `.env` file is found.

The `check_metrics` task runs the three D2G pipelines (`three_stages_light`, `three_stages_llm`, and `extender`) on a sample from `DeepPavlov/d2g_generated_augmented`. It writes results to `tests/metrics_results/` and fails if the mean similarity drops by 0.01 or more compared with the latest saved run, or if the mean duration grows by more than one second.

GitHub Actions workflows are defined for tests, coverage, code style, metric checks, documentation publishing, release publishing, and release testing.

## License

Dialog2Graph is released under the MIT License. The license text is in the `LICENSE` file and names "Anastasia Voznyuk" as the copyright holder for 2024.

## Authors

The `pyproject.toml` file lists the following authors: Denis Kuznetsov, Chirkin Andrey, Anastasia Voznyuk, Anna Mikhailova, Maria Molchanova, and Yuri Peshkichev. The documentation's About Us page names Denis Kuznetsov and Andrey Chirkin as project founders and lists DeepPavlov as the developing organization.
