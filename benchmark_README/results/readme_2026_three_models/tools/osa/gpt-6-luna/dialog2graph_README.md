# dialog2graph-09sackv3

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Dialog2Graph creates dialog graphs from input dialogs and can also generate dialog data. It is intended for developers and researchers working with dialog data and graph generation. The project offers command-line workflows and modular pipelines for graph generation and evaluation. See Getting Started for runnable steps.

---

## Core Features

- Generate dialog graphs from dialog data with light and LLM-based pipeline variants, giving developers alternative graph-generation workflows.
- Extend an existing graph using dialog data, supporting graph updates rather than only generating graphs from scratch.
- Generate dialog data for a specified topic, providing input data for graph-generation workflows.

---

## Installation

**Prerequisites:** requires Python ^3.12

Install dialog2graph-09sackv3 using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/dialog2graph-09sackv3
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

Requires Python 3.10–<3.13. The project is managed with Poetry; see `pyproject.toml` for its dependencies.

The `dialog2graph` CLI provides `gen_data`, `gen_graph_light`, `gen_graph_llm`, and `gen_graph_extender` commands. A runnable example cannot be established from the available setup and input-file details.

---

## Architecture

The package uses a modular, single-package structure. The CLI delegates data and graph generation to command handlers, and the pipeline package contains shared core components alongside light, LLM-based, graph-extender, and topic-generation modules.

Dataset modules cover dialog augmentation and complex dialogs. Metrics are organized into LLM-based and non-LLM metrics and validators, with utilities in a separate package. The repository structure indicates these as supporting modules; their detailed interactions are not established by the available context.

---

## Testing

A root test suite is available in `tests/`.

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Documentation

A detailed dialog2graph-09sackv3 description is available [here](./docs).

---

## Contributing

- **[Submit Pull Requests](./CONTRIBUTING.md)**: To learn more about making a contribution to dialog2graph-09sackv3.

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). dialog2graph-09sackv3 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{dialog2graph-09sackv3,

        author = {README Benchmark},

        title = {dialog2graph-09sackv3 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---