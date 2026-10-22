# dialog2graph

`dialog2graph` is a Python project for generating, extending, and evaluating dialogue graphs. It brings together graph-generation pipelines, dialogue augmentation utilities, automatic metrics, and experiments for turning conversations into graph structures.

> **Note:** This repository contains several experimental subprojects, notebooks, and generated datasets. Their dependencies and command-line interfaces may differ. Use the instructions for the relevant component rather than assuming every directory shares one environment.

## What’s in the repository

The repository includes:

- **Dialogue-to-graph generation**
  - Lightweight, LLM-based, and graph-extender generation approaches.
  - Multi-stage pipelines for constructing or completing graphs from dialogue.
  - Graph utilities, schemas, and algorithms for working with generated structures.
- **Dialogue augmentation and data generation**
  - Utilities and prompts for producing or transforming dialogue data.
  - Scripts and notebooks for sampling, cleaning, and preparing datasets.
- **Evaluation**
  - Automatic metrics and graph comparison tools, including semantic, annotation, and triplet-oriented evaluation.
  - Example metric data and reports.
- **Experiments and documentation**
  - Jupyter notebooks, generated examples, and experiment reports.
  - Sphinx documentation sources, including guides for generation, evaluation, graph extension, and augmentation.

## Repository layout

Some notable files and directories include:

| Path or filename | Purpose |
|---|---|
| `main.py` | Main project entry point. |
| `generate_graph_light.py`, `generate_graph_llm.py`, `generate_graph_extender.py` | Entry points for different graph-generation approaches. |
| `pipeline.py`, `three_stages_*.py` | Pipeline and multi-stage generation implementations. |
| `schemas.py`, `graph.py`, `dialog.py` | Data structures and graph/dialogue-related functionality. |
| `cfg.yml`, `model_storage.yml` | Example configuration files. Check them before running a pipeline. |
| `metrics/`, `validators.py`, `graph_triplet_comparison.py` | Metric, validation, and graph-comparison functionality. |
| `augmentation/`, `dialog_augmentation.py`, `augmentation_utils.py` | Dialogue augmentation code and supporting utilities. |
| `docs/` sources, including `.rst` files and `conf.py` | Documentation source files. |
| `test_*.py` | Python tests and test fixtures. |
| `*.ipynb` | Experiments, analysis, demos, and data-preparation notebooks. |

The repository also contains datasets, generated graph results, and experiment artifacts. These are useful for reproducing or inspecting specific experiments, but are not all required to run the core code.

## Requirements

- Python. The supported version is defined in the relevant `pyproject.toml`; this repository contains multiple Poetry projects, so check the one for the component you intend to use.
- Poetry, if you want to install dependencies from a `pyproject.toml` and `poetry.lock`.
- Credentials and model configuration if you plan to use an external LLM, embedding service, or other hosted model.

## Installation

Clone the repository and enter the project:

```bash
git clone <repository-url>
cd dialog2graph-adc6juxr
```

Before installing dependencies, identify the `pyproject.toml` for the component you want to run. There are multiple project files in the repository, and some experimental subprojects have their own environments.

For a Poetry-managed component:

```bash
cd <component-directory>
poetry install
poetry shell
```

Alternatively, install its dependencies into the active environment:

```bash
poetry install
```

If you are unsure which directory is appropriate, start with the root project files and the component’s `README.md`. Notebooks and nested projects may require their own environment.

## Configuration

Review the configuration files before running a pipeline:

- `cfg.yml` and other YAML configuration files hold project or pipeline settings.
- `model_storage.yml` and related model configuration files may specify model backends or model identifiers.
- Individual experimental subprojects may use files such as `settings.py` or their own configuration files.

Set any required API credentials using the mechanism expected by the selected model integration, such as environment variables. Do not commit secrets or private credentials. Check the relevant configuration loader and model-interaction code to determine the exact variable names and required settings.

Example preparation:

```bash
cp cfg.yml my_cfg.yml
# Edit my_cfg.yml and provide suitable non-secret configuration.
```

The actual configuration options vary by pipeline; consult the selected pipeline’s code, configuration file, and documentation.

## Usage

### Inspect the command-line interface

Start by checking the entry point’s help output:

```bash
python main.py --help
```

The repository also includes generation-specific scripts. Check their supported options before running them:

```bash
python generate_graph_light.py --help
python generate_graph_llm.py --help
python generate_graph_extender.py --help
```

If an entry point does not expose a `--help` option, inspect its argument parser or the corresponding usage guide in the documentation.

### Generate a graph

Choose a generation approach appropriate to your task:

- **Lightweight generation**: use the light pipeline when you want the non-LLM or lighter-weight path.
- **LLM generation**: use the LLM pipeline when graph construction depends on a configured language model.
- **Graph extension**: use the extender pipeline when you already have a graph and want to add or complete graph content.
- **Multi-stage generation**: use the relevant `three_stages_*.py` implementation when following one of the multi-step workflows.

The exact inputs, options, and output paths depend on the chosen implementation. Review its CLI help and configuration before running it. The repository includes JSON fixtures and generated graph files that can help you understand the expected data format.

### Use the Python code

Core classes and functions are organized across modules such as `dialog.py`, `graph.py`, `schemas.py`, and the pipeline modules. Import paths and APIs vary across the main project and experimental subprojects. For a concrete example, see `pipeline_example.ipynb`, `base_classes_usage.ipynb`, or the relevant pipeline implementation.

### Augment dialogue data

Dialogue augmentation functionality is available in the augmentation-related modules and subprojects. Check the local README and configuration for the augmentation component you want to use. Several notebooks demonstrate data preparation, augmentation, and review workflows.

### Evaluate generated graphs

Evaluation code includes automatic metrics, validators, and graph-comparison utilities. See the metric modules and example files, such as `examples_of_metrics_usage.ipynb`, `example_metrics_data.json`, and the evaluation documentation. Metric inputs and output formats are implementation-specific, so use the examples for the relevant metric as a guide.

## Data formats

The project works with dialogue and graph data, often stored as JSON. Schemas and validation logic are available in `schemas.py`, `validators.py`, and related modules.

The repository contains many fixtures and generated artifacts, but their formats may reflect different experiments or versions. Before using a file as input:

1. Identify which pipeline or evaluation tool produced it.
2. Check the corresponding schema or parser.
3. Validate it with the project’s validation utilities, where available.

Do not assume that every JSON file in the repository follows the same schema.

## Running tests

Tests and fixtures are distributed across the repository. From the relevant project directory, run:

```bash
pytest
```

To run a particular test module:

```bash
pytest test_validators.py
```

If a test requires model credentials, external services, or large datasets, consult the test and configuration files before running it. Some notebooks and integration workflows may not be suitable for automated test runs.

## Documentation

The repository includes Sphinx documentation sources. The `.rst` files cover topics such as getting started, graph generation, graph extension, evaluation, CLI usage, and synthetic data generation.

If Sphinx is installed in the documentation environment, build the docs from the directory containing `conf.py`:

```bash
make html
```

The generated site is typically written to a build directory such as `_build/html`. Check the documentation project’s instructions if the build command or working directory differs.

## Notebooks and experiment artifacts

Jupyter notebooks are used for demonstrations, experiments, data preparation, graph visualization, and metric analysis. To explore them:

```bash
jupyter lab
```

Open the notebook relevant to your task. Notebooks may rely on local data files, particular environments, external services, or paths that were specific to the original experiment. Review and adjust those dependencies before executing cells.

Generated JSON, CSV, pickle, and notebook files are experiment artifacts. Treat pickle files as trusted input only: loading a pickle from an untrusted source can execute arbitrary code.

## Development

When contributing:

1. Select the relevant project or subproject and install its dependencies.
2. Make changes in the appropriate module.
3. Run the applicable tests and formatting or lint checks configured for that project.
4. Update examples or documentation if you change a public workflow, schema, or configuration option.

See `CONTRIBUTING.md`, `how_to_contribute.md`, and the repository’s development documentation for additional guidance.

## Limitations and considerations

- This repository contains active and historical experiments; not every script or notebook is necessarily maintained as a stable public interface.
- Results from LLM-based workflows can vary with the configured model, prompts, parameters, and external service.
- Some pipelines may require network access, paid API access, or substantial compute.
- Generated data and evaluation results should be checked against the applicable schema and task requirements before being used downstream.

## License

See [`LICENSE`](LICENSE) for the applicable license.
