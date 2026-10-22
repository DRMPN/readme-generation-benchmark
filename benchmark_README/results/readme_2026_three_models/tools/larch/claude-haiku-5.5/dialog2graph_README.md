# dialog2graph

> **Note:** This README was written from the repository's file listing, not from the source code. Module names, CLI flags, configuration keys, and API signatures are inferred from file names and should be checked against the code before you rely on them. Sections marked **(verify)** are the most likely to differ.

## Overview

**dialog2graph** is a toolkit for turning task-oriented dialogs into dialog graphs, and for working with those graphs in the other direction. A dialog graph is a directed graph in which nodes represent dialog states (typically a bot utterance or a user intent) and edges represent allowed transitions between them. Such graphs are useful for designing, documenting, validating, and evaluating conversational systems.

The repository covers the full lifecycle of this work:

1. **Graph generation** from example dialogs, using LLM-based pipelines.
2. **Graph extension** of existing graphs with missing edges, cycles, or new branches.
3. **Synthetic dialog generation** by sampling paths through a graph.
4. **Dialog augmentation** to add variety to generated dialogs (e.g., utterance variations).
5. **Evaluation** with structural, semantic, and annotation-based metrics.
6. **Validation** of graphs and dialogs against schemas and structural rules.

It also contains the research material behind the project: experiment notebooks, reports, generated datasets, and prompt versions.

## Key Features

- **Multiple generation pipelines**
  - *Three-stages LLM pipeline* (`three_stages_llm`): generates a graph in three LLM-driven stages.
  - *Three-stages light pipeline* (`three_stages_light`): a lighter, lower-cost variant of the same approach.
  - *Extender pipeline* (`three_stages_extender`): extends an existing graph, for example by adding missing edges or cycles.
- **Graph algorithms**: cycle detection (`find_cycle_ends`, `cycle_with_missing_edge`), node grouping (`group_nodes`), start and end node selection, and a registry of algorithms (`algorithm_registry`).
- **Missing-edge recovery**: dedicated prompts (`missing_edges_prompt`) for proposing edges that are implied by the dialogs but absent from the graph.
- **Dialog sampling**: generates dialogs by walking paths through a graph (`dialog_sampling`, `dialog_sampler`).
- **Dialog augmentation**: rewrites utterances (`dialog_augmentation`, `augmentation_utils`, `augmentation_prompts`), including "uttr-vars" variants, with a naive filtering option and a one-shot option.
- **Evaluation metrics**
  - Triplet comparison (`graph_triplet_comparison`).
  - Semantic Jaccard similarity (`metrics_semantic_jaccard`).
  - Semantic metrics (`metrics_semantic`).
  - Annotation-based metrics (`metrics_annotation`).
  - A general `metrics` module and an autometrics runner (`run_autometrics.py`).
- **Validation**: JSON validation (`json_validator`), graph and dialog validators, and format conversion (`csv_converter`).
- **Prompt management**: prompt templates stored as modules and text files, a prompt loader, and prompt caching (`prompt_caching`) to reduce repeated LLM calls.
- **Vector storage and embeddings**: `vector_stores` and `embedder` modules, used for similarity lookups (for example, matching dialog utterances to existing graph nodes).
- **Command-line interface** (`main.py`) and a Python API.
- **Docker support** via `docker-compose.yml` and `init.sql`.
- **Sphinx documentation** with user guides covering generation, extension, augmentation, metrics, and the CLI.

## Repository Structure

The listing contains several kinds of content. The main ones are:

| Path | Purpose |
|---|---|
| `dialog2graph/` (package) | Core library: pipelines, generators, algorithms, metrics, validators, storage, and utilities. |
| `dialog2graph/.../pipeline.py`, `three_stages_*.py` | Pipeline implementations for graph generation. |
| `dialog2graph/.../prompts.py` | Prompt templates for each stage. |
| `dialog2graph/.../metrics*.py` | Evaluation metrics. |
| `dialog2graph/.../validators.py`, `json_validator.py` | Validation logic. |
| `dialog2graph/.../algorithms.py`, `algorithm_registry.py` | Graph algorithms and their registry. |
| `main.py`, `generate_*.py` | CLI entry point and generation scripts. |
| `tests/` | Pytest suite: `test_d2g_*.py`, `test_automatic_metrics.py`, `test_cli_d2g.py`, `test_validators.py`, `test_dialog_augmentation.py`, and others. Fixture JSON files sit next to them. |
| `docs/` | Sphinx documentation sources (`.rst`), `conf.py`, `Makefile`, `make.bat`. |
| `docker-compose.yml`, `init.sql` | Container setup and database initialization. |
| `cfg.yml`, `wrong_cfg.yml`, `models_config.yml`, `env_example` | Example configuration and environment files. |
| `pyproject.toml`, `poetry.lock` | Dependency management with Poetry. |
| `research/`, `experiments/`, `*/notebooks/` (various) | Experiment notebooks, reports, and generated datasets. Many of these folders contain their own `README.md`, `pyproject.toml`, and `poetry.lock`, so they are closer to self-contained sub-projects than to library code. |
| `*.json`, `*.pkl` (data) | Generated graphs, dialogs, augmented datasets, and metric results. |

### A note on the research folders

The repository contains many numbered and dated experiment folders (for example, `three_stages_light_25.04.2025_*.json` and `extender_*.json`). These are outputs from specific runs and are useful as reference data, but they are not part of the installable package. Treat them as examples and benchmarks.

## Installation

### Requirements

- Python 3.10 or newer **(verify)**
- [Poetry](https://python-poetry.org/) for dependency management
- An API key for the LLM provider you plan to use (for example, OpenAI) **(verify)**
- Docker and Docker Compose, if you want to use the containerized setup

### From source with Poetry

```bash
git clone <repository-url> dialog2graph-ksp184ub
cd dialog2graph-ksp184ub
poetry install
```

To activate the environment:

```bash
poetry shell
```

### With Docker

```bash
docker-compose up --build
```

This starts the services defined in `docker-compose.yml`. `init.sql` is applied at database initialization **(verify which database and what it stores)**.

## Configuration

### Environment variables

Copy the example file and fill in your credentials:

```bash
cp env_example .env
```

Typical variables include:

```
OPENAI_API_KEY=your-key-here
```

**(verify the exact variable names in `env_example`)**

### Pipeline configuration

Pipelines are configured with YAML. `cfg.yml` holds a working example, and `wrong_cfg.yml` is a deliberately invalid configuration used by the tests to check error handling.

A configuration typically specifies:

- the pipeline to run (LLM, light, or extender);
- the model and provider;
- generation parameters such as temperature and number of retries;
- caching and storage options;
- paths to input dialogs or graphs.

Model options are collected in `models_config.yml`. **(verify)**

Example skeleton (illustrative only; check `cfg.yml` for the real schema):

```yaml
pipeline: three_stages_llm
model:
  provider: openai
  name: gpt-4o
  temperature: 0.0
cache:
  enabled: true
input:
  dialogs: data/dialogs.json
output:
  dir: results/
```

## Usage

### Command line

The CLI is implemented in `main.py` and is documented in `cli_usage.rst`. The general pattern is:

```bash
python main.py --config cfg.yml
```

**(verify the exact subcommands and flags, which the tests in `test_cli_d2g.py` exercise)**

### Python API

Generic pattern for generating a graph from dialogs:

```python
from dialog2graph import ...  # check the package __init__ for exported names

dialogs = load_dialogs("tests/test_cli.json")
pipeline = ...  # construct from config
graph = pipeline.run(dialogs)
graph.save("output/graph.json")
```

Refer to the Sphinx guides in `docs/` (`generate_graphs.rst`, `extend_graphs.rst`, `basic_usage.rst`) for runnable examples.

### Common workflows

**1. Generate a graph from dialogs**

Use the three-stages LLM pipeline on a set of example dialogs. Results are written as a graph JSON file with nodes and edges.

**2. Extend an existing graph**

Run the extender pipeline on a graph that is missing some transitions. It proposes the missing edges, checks them against the dialogs, and writes an updated graph. Cycle and cycle-end algorithms help locate where edges are missing.

**3. Sample synthetic dialogs from a graph**

Walk the paths of a graph to produce dialogs. Sampling can be restricted by path length or by coverage of nodes and edges.

**4. Augment dialogs**

Apply the augmentation pipeline to generated dialogs to produce utterance variants. Filtering removes low-quality or duplicate variants.

**5. Evaluate a generated graph**

Compare a generated graph against a reference graph with the triplet, semantic Jaccard, or annotation metrics. Use `run_autometrics.py` to run a batch of metrics over multiple results.

## Data Formats

### Dialogs

Dialogs are stored as JSON. Each dialog is a sequence of turns. Test fixtures such as `tests/test_cli.json` and `test_dialog_augmentation_data.json` show the exact layout. **(verify field names)**

### Graphs

Graphs are stored as JSON with two main lists:

- `nodes`: each node has an identifier and its utterance or intent.
- `edges`: each edge connects a source node to a target node.

Example fixtures include `test_complex_graph.json`, `test_split_node.json`, and `test_cycle_with_missing_edge.json`.

### Metrics

Metric results are stored as JSON (`all_metrics.json`) and plain-text summaries (`mean_metrics.txt`).

## Testing

Run the test suite with pytest from the project root:

```bash
poetry run pytest tests/
```

Test files cover:

- pipelines (`test_d2g_llm.py`, `test_d2g_light.py`, `test_d2g_extender.py`);
- the CLI (`test_cli_d2g.py`), including empty graphs, missing graphs, and empty dialog sets;
- automatic metrics (`test_automatic_metrics.py`);
- validators (`test_validators.py`);
- dialog augmentation (`test_dialog_augmentation.py`);
- initialization and configuration (`test_initialization.py`, `test_topic_generation_init.py`).

Note that pipeline tests call an LLM. Running them requires valid credentials and may incur costs. Enable prompt caching to make repeated runs cheaper and more deterministic.

## Documentation

The documentation is built with Sphinx.

```bash
cd docs
make html        # Linux/macOS
make.bat html    # Windows
```

The output is written to `docs/_build/html/`. The guides cover getting started, basic usage, graph generation, extension, augmentation, synthetic generation, evaluation, the CLI, data collections, and development.

## Project Layout Notes

- The package is organized by pipeline. Each pipeline has its own `prompts.py`, `pipeline.py`, and a set of helper modules, so a change to one pipeline usually stays local.
- Shared utilities live in `logger.py`, `dg_helper.py`, `prompt_caching.py`, and `vector_stores.py`.
- Experiment and research directories are not required for the library to function.

## Contributing

Contributions are welcome. See `CONTRIBUTING.md` and `docs/how_to_contribute.md` for details. A typical workflow:

1. Fork the repository and create a feature branch.
2. Install the development dependencies with `poetry install`.
3. Make your change and add or update tests in `tests/`.
4. Run the test suite and the linter (the project includes `ruff.toml`).
5. Open a pull request with a clear description of the change.

For prompt changes, include before-and-after examples and, where possible, metric results on the fixture data.

## License

This project is distributed under the license in the `LICENSE` file at the repository root.

## Citation

If you use this work in research, please cite the project. A citation entry will be added here once it is available **(placeholder)**.

## Acknowledgements

This work builds on research into dialog graph generation and evaluation. The repository's `docs/` folder includes a list of collaborators and related projects, and the `logo-*.svg` files in `docs/` reflect the affiliated organizations.
