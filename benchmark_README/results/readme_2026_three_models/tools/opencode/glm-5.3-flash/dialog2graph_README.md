# Dialog2Graph

**Dialog2Graph** is a project for creating dialog graphs based on input dialogs. It extends the [Chatsky project](https://github.com/deeppavlov/chatsky) by enhancing `chatsky` flows and scripts creation with the help of Large Language Models (LLMs), transforming conversational data into structured, graph-based representations.

## Features

- **Dialog Graph Generation:** Generate dialog graphs from dialogs using three pipelines: algorithm-based (`d2g_algo`), LLM-based (`d2g_llm`), and graph extension (`d2g_extender`).
- **Synthetic Data Generation:** Generate dialog data for a given topic using LLMs.
- **Dialog Sampling:** Sample dialogs from existing dialog graphs using recursion.
- **Dialog Augmentation:** Augment existing dialogs using LLMs.
- **Graph Evaluation:** Assess single dialog graphs and dialog sets, and compare graphs using LLM-based and non-LLM metrics and validators.
- **Visualization:** Visualize dialog graphs with all utterances or in a schematic way.
- **CLI Interface:** Use the `dialog2graph` command-line tool to generate dialogs, graphs, and reports.

## Installation

To install the project, please follow the steps below:

1. Install Poetry v1.8.4:

   ```bash
   pipx install poetry==1.8.4
   ```

2. Clone this repository and install the project dependencies:

   ```bash
   git clone https://github.com/deeppavlov/dialog2graph.git
   cd dialog2graph
   poetry install
   ```

3. If you plan to visualize your graphs, add PyGraphviz to the poetry environment:

   ```bash
   poetry add pygraphviz
   ```

4. Create a `.env` file to store your credentials (such as API tokens). Never hardcode your personal tokens and other sensitive credentials; use the `.env` file to store them.

5. Ensure that the dependencies were installed correctly by running any Python script:

   ```bash
   poetry run python <your_file_name>.py
   ```

## Usage

### Python API

The `Graph` and `Dialog` classes are the base structures used in the `dialog2graph` project to store information about graphs and dialogs.

```python
from datasets import load_dataset
from dialog2graph import Graph

# Load generated data from HuggingFace
dataset = load_dataset("DeepPavlov/d2g_generated", token=True)

# Initialize a graph by passing a dictionary with graph edges and nodes
graph = Graph(graph_dict=dataset['train'][5]["graph"])

# Visualize the graph with all the utterances it contains
graph.visualise()

# Visualize the graph in a schematic way to see its general structure
graph.visualise_short("Schematic graph view")
```

You can also sample dialogs from an existing dialog graph:

```python
from dialog2graph.pipelines.core.dialog_sampling import RecursiveDialogSampler
from langchain_openai import ChatOpenAI

sampler = RecursiveDialogSampler()
model = ChatOpenAI(model="gpt-3.5-turbo")
dialogs = sampler.invoke(graph=graph, upper_limit=10, cycle_ends_model=model)
```

The output is a list of `Dialog` instances that provide methods for visualization and conversion.

### CLI

The `dialog2graph` command-line tool supports the following commands:

- `gen_data`: Generate dialog data for a given topic.
- `gen_graph_light`: Generate a graph from dialog data via the `d2g_algo` pipeline.
- `gen_graph_llm`: Generate a graph from dialog data via the `d2g_llm` pipeline.
- `gen_graph_extender`: Generate/extend a graph from dialog data via the extender pipeline.

Each command accepts options to specify the path to the `.env` file, the configuration file (`cfg.yml`), input dialogs, an optional true graph, output paths for the graph and report, and an evaluation flag. For example:

```bash
dialog2graph gen-graph-light --dialogs <input_dialogs.json> --output <output_graph.json>
```

Configuration for models is provided via a `cfg.yml` file, e.g.:

```yaml
models:
  generation-model:
    name: openai/gpt-4o-latest
  validation-model:
    name: openai/gpt-4o-mini
    temperature: 1.0
```

### Examples

The `examples/` directory contains Jupyter notebooks demonstrating usage of the project:

- `basics/base_classes_usage.ipynb`: Learn base `dialog2graph` classes.
- `pipeline_usage/pipeline_example.ipynb`: Configure models with `ModelStorage` and use the graph generators.
- `data_generation/`: Generate synthetic graphs on certain topics.
- `evaluation/examples_of_metrics_usage.ipynb`: Evaluate single dialog graphs and dialog sets.
- `cli_usage/`: Use the `dialog2graph` CLI interface.
- `dialog_augmentation/`: Augment existing dialogs using LLMs.
- `dialog_extension/`: Extend existing dialog graphs using LLMs.

## Documentation

Full documentation is built with Sphinx and is located in the `docs/` directory. It includes:

- **Getting Started:** Installation instructions.
- **Research:** Key concepts, data collections, and dialog graph assessment.
- **User Guides:** Usage examples for graph generation, evaluation, augmentation, extension, and CLI usage.
- **API Reference:** Documentation for classes and abstractions used in the library.
- **Development:** Development status and contribution rules.

To build the documentation locally, navigate to the `docs/` directory and run the Makefile:

```bash
cd docs
make html
```

## Development

To run tests, use the following task:

```bash
poetry run poe test
```

To check code style and format the code, use:

```bash
poetry run poe lint
poetry run poe format
```

To check metrics of the d2g pipelines, use:

```bash
poetry run poe check_metrics
```
