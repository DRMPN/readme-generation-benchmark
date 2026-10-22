# README

# Dialog2Graph

**Dialog2Graph** is a research framework for generating, augmenting, and evaluating **dialog graphs** — structured representations of task-oriented dialogs as graphs of utterances (nodes) and transitions (edges). The library supports synthesizing dialogs from graphs, generating graphs from dialogs, augmenting existing dialogs, and evaluating generated graphs against ground truth with a rich set of metrics.

---

## ✨ Features

- **Graph generation from dialogs** — three interchangeable pipelines:
  - `three_stages_light` — lightweight, fast generation
  - `three_stages_llm` — LLM-driven generation with rich prompts
  - `three_stages_extender` — generation via incremental graph extension
- **Graph incrementation** — extend existing graphs with new nodes/edges (LLM- and embedder-based approaches)
- **Dialog augmentation** — generate new synthetic dialogs from graphs, with utterance-variant augmentation (`uttr-vars`)
- **Dialog sampling** — sample valid dialogs from generated graphs (`dialog_sampler`, path/cycle handling, cycle-end detection)
- **Evaluation metrics** — structural, semantic, and embedding-based comparisons (Jaccard, semantic similarity, triplet-based graph comparison, automatic metrics)
- **Prompt management** — a shared prompt registry with support for **prompt caching** (`prompt_caching.py`)
- **Vector stores & embeddings** — `vector_stores.py`, `embedder.py`, `vectors.py` for semantic retrieval and node matching
- **Pipelines & registries** — composable pipeline abstraction (`pipeline.py`), algorithm registry (`algorithm_registry.py`), model storage (`model_storage.py` / `models_config.yml`)
- **Validation** — graph and dialog validators, JSON schema validation
- **Experiment tracking** — timestamped JSON result files, reports, and CSV metric exports
- **Documentation** — Sphinx docs (`docs/`) with user guides for each pipeline
- **Testing** — pytest suite covering pipelines, validators, metrics, CLI, and data fixtures

---

## 📁 Project Structure

```
dialog2graph-inn_4_xo/
├── dialog2graph/                  # Core library
│   ├── d2g/                       # Dialog-to-graph pipelines
│   │   ├── three_stages_light/    # Light 3-stage pipeline
│   │   ├── three_stages_llm/      # LLM-based 3-stage pipeline
│   │   ├── three_stages_extender/ # Extender-based pipeline
│   │   ├── pipelines.py           # Pipeline orchestration
│   │   └── model_storage.py       # Model configuration storage
│   ├── generation/                # Graph generation helpers
│   ├── augmentation/              # Dialog augmentation
│   ├── evaluation/                # Metrics & graph comparison
│   │   ├── metrics.py, metrics_semantic.py
│   │   ├── metrics_semantic_jaccard.py
│   │   ├── metrics_annotation.py
│   │   ├── graph_triplet_comparison.py
│   │   └── file_handler.py
│   ├── algorithms/                # graph.py, similarity.py, validators.py
│   ├── dialog/                    # Dialog schemas & sampling
│   ├── prompt/                    # Prompt loader & registry
│   ├── pipeline/                  # Base pipeline classes & validators
│   ├── utils/                     # Logging, helpers, JSON validation
│   └── storage/                   # Vector stores, DB (init.sql, docker-compose.yml)
├── app/                           # Application-level modules
│   ├── core/                      # generation, pipelines, model interactions
│   ├── metrics/                   # app-facing metric wrappers
│   └── api/                       # CLI & JSON handling
├── experiments/                   # Research notebooks & experimental code
│   ├── three_stages_variants/     # three_stages_1i, 0i, algo variants
│   ├── graph_incrementation/      # incremental graph extension experiments
│   ├── dialog_augmentation/       # augmentation notebooks & utilities
│   ├── sampling/                  # dialog sampler research
│   ├── metrics_research/          # metric experiments, FT_Llama fine-tuning
│   └── data_analysis/             # notebooks for dataset inspection
├── data/                          # Datasets (dialog graphs, augmented corpora)
├── docs/                          # Sphinx documentation
│   ├── basic_usage.rst, generate_graphs.rst, augment_dialogs.rst,
│   ├── evaluate_userguide.rst, extend_graphs.rst, cli_usage.rst, ...
├── tests/                         # Test suite + fixtures
├── examples/                      # Jupyter notebook examples
│   ├── LoopedGraphGenerator_example.ipynb
│   ├── cache_example.ipynb
│   ├── dialogue_augmentation_example.ipynb
│   └── ...
├── pyproject.toml                 # Project metadata & dependencies (Poetry)
├── poetry.lock
├── docker-compose.yml             # DB services for vector storage
├── init.sql
├── cfg.yml / models_config.yml    # Configuration files
├── Makefile / make.bat
└── ruff.toml                      # Linter config
```

---

## 🚀 Installation

Requires **Python 3.10+** and [Poetry](https://python-poetry.org/).

```bash
git clone <repository-url>
cd dialog2graph-inn_4_xo
poetry install
```

Or with pip:

```bash
pip install .
```

Set up environment variables (API keys for LLM providers, embedding services, etc.) — see `env_example` for a template.

To run the storage backend (for vector stores / embeddings):

```bash
docker-compose up -d
```

---

## ⚙️ Configuration

- **`cfg.yml`** — main pipeline configuration (models, endpoints, parameters)
- **`models_config.yml`** — LLM/embedder model definitions
- **`model_storage.yml`** — model storage settings for the CLI

Configure your LLM (e.g., OpenAI-compatible APIs) and embedding model before running pipelines.

---

## 📖 Quick Start

### 1. Generate a graph from dialogs

```python
from dialog2graph.d2g import pipelines

pipeline = pipelines.get_pipeline("three_stages_light")
graph = pipeline.invoke(dialogs=dialogs, topic="book_table")
```

Or via the CLI:

```bash
python -m dialog2graph --config cfg.yml ...
```

### 2. Augment dialogs from a graph

```python
from dialog2graph.augmentation.dialog_augmentation import DialogAugmentation

augmenter = DialogAugmentation(...)
new_dialogs = augmenter.invoke(graph=graph, n_dialogs=10)
```

### 3. Evaluate generated graphs

```python
from dialog2graph.evaluation.metrics import ...

scores = compare_graphs(generated_graph, reference_graph)
```

### 4. Extend an existing graph

Use the `three_stages_extender` pipeline or the incremental generation experiments (`graph_incrementation`) to iteratively add nodes and edges validated by an LLM.

---

## 🧪 Testing

```bash
pytest tests/
```

Test fixtures include graph JSONs (`test_complex_graph.json`, `test_single_nodes.json`, `test_cycle_with_missing_edge.json`, ...) and dialog datasets (`test_pipelines_data.json`, `test_dialog_augmentation_data.json`).

Run the style checks:

```bash
make codestyle   # uses ruff.toml
```

---

## 📚 Documentation

Build the Sphinx docs:

```bash
cd docs
make html
```

Key guides:

| Guide | Content |
|---|---|
| `basic_usage.rst` | Getting started |
| `generate_graphs.rst` | Dialog-to-graph pipelines |
| `extend_graphs.rst` | Graph incrementation |
| `augment_dialogs.rst` | Dialog augmentation |
| `generate_synthetic.rst` | Synthetic data generation |
| `evaluate_userguide.rst` | Metrics & evaluation |
| `cli_usage.rst` | Command-line interface |

---

## 🤝 Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`how_to_contribute.md`](docs/how_to_contribute.md) for coding standards, codestyle checks, and the PR workflow.

---

## 📄 License

This project is distributed under the terms of the [`LICENSE`](LICENSE) file.

---

## 🙏 Acknowledgments

Built with the [DeepPavlov](https://deeppavlov.ai) ecosystem — see `logo-deeppavlov.svg` in the docs. The project supports research on dialog-graph synthesis, LLM-based dialog modeling, and automatic evaluation of generated dialog structures.
