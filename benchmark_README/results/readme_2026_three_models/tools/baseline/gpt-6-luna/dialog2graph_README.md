# Dialog2Graph

Dialog2Graph transforms conversational data into structured dialog graphs. It provides graph-generation pipelines, graph extension, dialog and synthetic-data generation utilities, and metrics and validators for assessing graphs and dialogs. The project describes itself as extending the Chatsky project with tools for creating dialog graphs and supporting LLM-assisted conversational flows.

A dialog graph is a directed structure: nodes hold assistant utterances and edges connect nodes with user utterances. The package also provides `Dialog` and `Graph` classes for working with dialogs and graphs in Python.

## Features

- Generate graphs from dialog data using an algorithm-based pipeline or an LLM-based pipeline.
- Extend an existing graph with dialog data.
- Generate synthetic dialog data for a topic, and augment existing dialogs with paraphrases.
- Sample dialogs from graphs and visualize graph structures.
- Evaluate graph structure and dialog quality with LLM and non-LLM metrics and validators.
- Use the library from Python or through the `dialog2graph` command-line interface.

The project includes examples and notebooks under `examples/`, user guides under `docs/source/userguides/`, and experimental work under `experiments/`.

## Requirements

The project supports Python `>=3.10,<3.13` and uses Poetry for dependency management. The documentation’s installation instructions specify Poetry 1.8.4. Core dependencies include LangChain integrations, NetworkX, sentence-transformers, pandas, PyYAML, and Click.

Some operations use external language or embedding models. Configure the credentials required by your chosen model provider before running those operations. Do not put secret tokens in source code or commit them to the repository.

## Installation

Install Poetry 1.8.4 and clone the repository:

```bash
pipx install poetry==1.8.4
git clone https://github.com/deeppavlov/dialog2graph.git
cd dialog2graph
```

Install the project and its dependencies:

```bash
poetry install
```

To use graph visualization features that depend on PyGraphviz, install it separately. Refer to the [PyGraphviz installation guide](https://pygraphviz.github.io/) for platform requirements, then add it to the Poetry environment:

```bash
poetry add pygraphviz
```

Create a `.env` file for credentials and other local environment settings as needed. The CLI loads `.env` by default; you can point it to another file with `--env`. Keep credentials private.

## Python usage

The package exports `Dialog` and `Graph` from its top-level namespace. A graph dictionary uses `nodes` and `edges`; node entries include an `id`, a list of `utterances`, and may include a `label` and `is_start`. Edges include `source`, `target`, and `utterances`.

```python
from dialog2graph import Dialog, Graph

graph_data = {
    "nodes": [
        {
            "id": 1,
            "label": "greeting",
            "is_start": True,
            "utterances": ["Hello! How can I help?"],
        }
    ],
    "edges": [],
}

graph = Graph(graph_dict=graph_data)
dialog = Dialog.from_list([
    {"participant": "assistant", "text": "Hello! How can I help?"},
    {"participant": "user", "text": "I have a question."},
])

print(dialog)
dialog.to_list()
graph.visualise()
graph.visualise_short("Example graph")
```

A fuller graph example is available in `examples/example_data.json`. For loading the project’s published synthetic dataset, the documentation demonstrates:

```python
from datasets import load_dataset
from dialog2graph import Graph

dataset = load_dataset("DeepPavlov/d2g_generated", token=True)
graph = Graph(graph_dict=dataset["train"][0]["graph"])
```

The documentation also describes `RecursiveDialogSampler` for sampling dialogs from a graph, `ModelStorage` for configuring models, and graph generation with `LLMGraphGenerator`. See the notebooks in `examples/` and the guides in `docs/source/userguides/` for complete workflows.

## Command-line usage

The installed CLI is available as `dialog2graph`. Run `dialog2graph --help` to inspect its commands. The commands accept `--env` / `-e` for an environment file and `--cfg` / `-c` for a YAML configuration file; both default to `.env` and `cfg.yml`, respectively.

Generate dialog data for a topic:

```bash
dialog2graph gen_data --topic "restaurant reservation" \
  --cfg cfg.yml \
  --output generated_data.json
```

Generate a graph from dialogs with the light or LLM pipeline:

```bash
dialog2graph gen_graph_light --dialogs dialogs.json \
  --cfg cfg.yml \
  --output graph.json \
  --report report.json \
  --eval
```

```bash
dialog2graph gen_graph_llm --dialogs dialogs.json \
  --cfg cfg.yml \
  --output graph.json \
  --report report.json
```

Extend a graph using dialogs:

```bash
dialog2graph gen_graph_extender --dialogs dialogs.json \
  --graph graph.json \
  --cfg cfg.yml \
  --output extended_graph.json \
  --report report.json
```

For graph-generation and extension commands, `--tgraph` optionally supplies a true graph for evaluation. The output and report paths are also optional. Use `--eval` to request pipeline evaluations. The CLI accepts configuration-file paths, but the exact YAML fields depend on the pipeline; example configuration files are in `examples/cli_usage/` and `examples/pipeline_usage/`.

## Configuration

For Python workflows, `ModelStorage` lets you register models under keys and select them for pipeline tasks. For example, the documentation configures a LangChain `ChatOpenAI` model and a Hugging Face embedding model, then passes their registered keys to an `LLMGraphGenerator`. Model names and task-specific settings are supplied when adding the models.

For command-line workflows, pass a YAML file with `--cfg`. The repository includes example files, but does not define a single configuration schema in this README. Use the relevant CLI notebook or user guide as the reference for the operation you plan to run.

## Development

Install the optional documentation, lint, and test dependencies:

```bash
poetry install --with docs,lint,tests
```

The project provides Poetry tasks for common development work:

```bash
poetry run poe lint
poetry run poe format
poetry run poe test
poetry run poe coverage
poetry run poe check_metrics
```

Linting and formatting use Ruff. The `test` task runs the test suite in `tests/`; the coverage task generates terminal and HTML reports and requires at least 80% coverage. `check_metrics` runs pipeline metric checks against a Hugging Face dataset and uses environment configuration for dataset access and a SQLAlchemy-backed LLM cache, so it may require external credentials and services.

To build the Sphinx documentation, install the `docs` group and run:

```bash
poetry run sphinx-build -b html docs/source/ docs/build/
```

Contributors should follow `CONTRIBUTING.md`: use a feature, fix, or experiment branch; follow PEP 8; document code with docstrings; and add tests for new behavior. Store experiments in separate, descriptively named folders under `experiments/`, and record their setup and results in an experiment README. Keep secrets out of commits and do not add images to experiment folders.

## Testing

Run the project tests with:

```bash
poetry run poe test
```

The test suite covers initialization, CLI behavior, pipelines, metrics, validators, and dialog augmentation. Some tests make live model calls. In particular, the augmentation test module skips when it cannot find a `.env` file and uses configured chat models; tests that call external services may therefore need valid credentials and network access.

To run tests with coverage:

```bash
poetry run poe coverage
```

For pipeline metric comparisons, see `poetry run poe check_metrics`. That task compares current pipeline results with recorded metrics and can fail if results regress.

## Datasets and documentation

The documentation describes the `DeepPavlov/d2g_generated` synthetic dialog-graph dataset and the `DeepPavlov/d2g_real_dialogs` collection of reformatted task-oriented dialogs. Dataset loading examples and formats are in `docs/source/research/data_collections.rst`.

Build and usage details are also available in the Sphinx documentation, including guides for graph generation, synthetic generation, augmentation, extension, evaluation, and CLI use.

## License

Dialog2Graph is distributed under the MIT License. See [`LICENSE`](LICENSE) for the license text and terms.
