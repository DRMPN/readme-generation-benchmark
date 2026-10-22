# Dialog2Graph

Dialog2Graph is a Python library and command-line tool for turning conversational data into structured dialog graphs. It includes graph-generation pipelines, graph extension, synthetic dialog generation, dialog augmentation, graph and dialog evaluation, and utilities for working with graph and dialog objects.

The project also extends the [Chatsky](https://github.com/deeppavlov/chatsky) project by supporting the creation of Chatsky flows and scripts with help from large language models (LLMs).

## Features

- Build directed dialog graphs from one or more conversations using the `d2g_light` and `d2g_llm` pipelines.
- Extend an existing dialog graph with additional nodes and edges.
- Generate synthetic graph-and-dialog data about a topic, or augment an existing dialog.
- Visualize and sample dialogs from graph structures with `Graph` and `Dialog` utilities.
- Evaluate graph structure and dialog quality using metrics and validators, with optional pipeline reports.
- Use the command line or the Python API.

## Requirements and installation

The project requires Python `>=3.10,<3.13` and uses Poetry for dependency management.

```bash
git clone https://github.com/deeppavlov/dialog2graph.git
cd dialog2graph
poetry install
```

To install the optional documentation, linting, and test dependencies as well:

```bash
poetry install --with docs,lint,tests
```

Some features call hosted LLMs. Configure the credentials expected by the model provider in your environment or a `.env` file; do not commit secrets. The examples use LangChain chat models such as `ChatOpenAI`. Embedding models can also be configured, including Hugging Face models.

## Quick start: Python API

`Dialog` represents a conversation as messages with a `participant` and `text`. `Graph` represents a directed dialog graph. Both are exported from the top-level package:

```python
from dialog2graph import Dialog, Graph

dialog = Dialog(
    messages=[
        {"participant": "assistant", "text": "How can I help?"},
        {"participant": "user", "text": "I need to book a ride."},
    ]
)

graph = Graph(
    graph_dict={
        "nodes": [
            {
                "id": 1,
                "label": "Offer help",
                "is_start": True,
                "utterances": ["How can I help?"],
            },
            {
                "id": 2,
                "label": "Book a ride",
                "is_start": False,
                "utterances": ["Where would you like to go?"],
            },
        ],
        "edges": [
            {"source": 1, "target": 2, "utterances": ["I need to book a ride."]}
        ],
    }
)

print(dialog)
graph.visualise()
```

Graph nodes have an integer `id`, a `label`, an `is_start` flag, and a list of assistant `utterances`. Edges have integer `source` and `target` node IDs and a list of user `utterances` that trigger the transition.

For generation pipelines, configure the required models with `ModelStorage` and pass conversations through a pipeline. For example, the documented `LLMGraphGenerator` accepts a `PipelineRawDataType` containing `Dialog` instances and returns a graph and report:

```python
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from dialog2graph import Dialog
from dialog2graph.pipelines.d2g_llm import LLMGraphGenerator
from dialog2graph.pipelines.helpers.parse_data import PipelineRawDataType
from dialog2graph.pipelines.model_storage import ModelStorage

model_storage = ModelStorage()
model_storage.add(
    "formatting",
    config={"model_name": "gpt-4o-mini", "temperature": 0},
    model_type=ChatOpenAI,
)
model_storage.add(
    "embeddings",
    config={"model_name": "sentence-transformers/all-MiniLM-L6-v2",
            "model_kwargs": {"device": "cpu"}},
    model_type=HuggingFaceEmbeddings,
)

generator = LLMGraphGenerator(
    model_storage=model_storage,
    formatting_llm="formatting",
    sim_model="embeddings",
)
data = PipelineRawDataType(
    dialogs=[
        Dialog(messages=[
            {"participant": "assistant", "text": "How can I help?"},
            {"participant": "user", "text": "I need to book a ride."},
        ])
    ],
    supported_graph=None,
    true_graph=None,
)
graph, report = generator.invoke(data, enable_evals=True)
```

This example requires working provider credentials. Enabling evaluations can add processing time and LLM token usage. See [`docs/source/userguides/generate_graphs.rst`](docs/source/userguides/generate_graphs.rst) and the runnable notebooks under [`examples/`](examples/) for more detail.

## Command-line interface

After installation, the executable is `dialog2graph`. It provides these commands:

| Command | Purpose |
| --- | --- |
| `gen-data` | Generate dialog data for a topic. |
| `gen-graph-light` | Generate a graph from dialog data with the `d2g_light` pipeline. |
| `gen-graph-llm` | Generate a graph from dialog data with the `d2g_llm` pipeline. |
| `gen-graph-extender` | Extend a graph using dialog data. |

For example, run graph generation on a JSON file containing dialogs:

```bash
poetry run dialog2graph gen-graph-llm \
  --env .env --cfg models.yml \
  --dialogs dialogs.json --output graph.json --report report.md
```

`--env` defaults to `.env` and `--cfg` defaults to `cfg.yml`. The topic is required for `gen-data`; a dialogs file is required for graph generation. Graph commands also accept `--tgraph` for a true/reference graph, `--eval` to enable pipeline evaluations, and `--report` to choose a report output path. `gen-graph-extender` additionally accepts `--graph` for the graph to extend. Use `poetry run dialog2graph --help` or `poetry run dialog2graph <command> --help` for the full options.

Model configuration files are YAML mappings from model keys to a `config` and `model_type`; see [`tests/cli/cfg.yml`](tests/cli/cfg.yml) and [`examples/pipeline_usage/models_config.yml`](examples/pipeline_usage/models_config.yml) for repository examples. The model keys required depend on the pipeline. Dialog JSON may be a list of message dictionaries or an object with a `dialogs` list. Each message has `participant` and `text` fields. Graph input files are JSON objects with a `graph` (or, for reference graphs, `true_graph`) key containing `nodes` and `edges`.

The `gen-data` command is registered for topic-based dialog data generation, but its current handler calls `TopicGenerationPipeline.invoke` without that method's required `output_path` argument; it therefore raises an argument error as currently implemented. The Python API for synthetic generation is documented in [`docs/source/userguides/generate_synthetic.rst`](docs/source/userguides/generate_synthetic.rst).

When no graph output path is supplied, graph commands print the graph. If no report path is supplied, they create a timestamped JSON report. Report paths with `.json`, `.csv`, `.html`, `.md`, or `.txt` suffixes select the corresponding report format.

## Documentation and examples

- [Getting started](docs/source/getting_started.rst)
- [User guides](docs/source/userguides.rst): base classes, graph generation, synthetic generation, evaluation, CLI usage, augmentation, and graph extension
- [Research notes and datasets](docs/source/research.rst)
- [Examples and notebooks](examples/)
- [Sphinx documentation source](docs/)

The documentation describes the Hugging Face datasets [DeepPavlov/d2g_generated](https://huggingface.co/datasets/DeepPavlov/d2g_generated) and [DeepPavlov/d2g_real_dialogs](https://huggingface.co/datasets/DeepPavlov/d2g_real_dialogs).

## Development and tests

Install development dependencies and run the test task:

```bash
poetry install --with docs,lint,tests
poetry run poe test
```

Other configured tasks include `poetry run poe lint`, `poetry run poe format`, and `poetry run poe coverage`. Contribution guidance is in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

This project is distributed under the [MIT License](LICENSE).
