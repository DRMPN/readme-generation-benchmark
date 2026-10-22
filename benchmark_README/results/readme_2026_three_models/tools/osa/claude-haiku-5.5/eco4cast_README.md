# eco4cast-09sz5j9p

---

[![PyPi](https://badge.fury.io/py/eco4cast.svg)](https://badge.fury.io/py/eco4cast)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![lightning](https://img.shields.io/badge/Lightning-792EE5.svg?style={0}&logo=Lightning&logoColor=white)
![numpy](https://img.shields.io/badge/NumPy-013243.svg?style={0}&logo=NumPy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style={0}&logo=pandas&logoColor=white)
![python](https://img.shields.io/badge/Python-3776AB.svg?style={0}&logo=Python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikitlearn-F7931E.svg?style={0}&logo=scikit-learn&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

eco4cast is a Python package designed to reduce CO2 emissions while training neural networks on Google Cloud. It is intended for machine learning practitioners and developers who run training workloads on Google Cloud and want to lower the emissions of those workloads. The repository provides a client library for managing Google Cloud compute resources, along with example workflows for training neural networks. For runnable steps, see Getting Started.

---

## Core Features

- **Reusable Google Cloud Compute functions:** Provides Python functions for managing instances, disks, firewall rules, snapshots, and routes, so these resources can be handled from your own code.
- **Runnable firewall rule sample:** Includes a script that creates, inspects, updates the priority of, and deletes a firewall rule, which serves as a working reference for that workflow.
- **Example directories for training and demos:** Includes example directories for MNIST and ImageNet on Google Cloud, plus local demos, to use as starting points.

---

## Installation

**Prerequisites:** requires Python ^3.9

Install eco4cast-09sz5j9p using one of the following methods:

**Using PyPi:**

```sh
pip install eco4cast
```

---

## Getting Started

### Prerequisites

- Python ^3.9 (as declared in `pyproject.toml`).
- A Google Cloud project with Compute Engine access, since the package is designed for training on Google Cloud.
- Google Cloud Application Default Credentials (ADC) configured on the machine where you run the code. The firewall sample in `eco4cast/master_machine/compute/client_library/recipes/firewall/main.py` suggests this login command:

```bash
gcloud auth application-default login
```

### Steps

1. Confirm your Python version meets the `^3.9` requirement.
2. Configure Google Cloud credentials as described above.
3. Open the `examples/` directory. Its `examples/README.md` describes the end-to-end workflow, so follow that for the first run.
4. Start with one of the bundled examples, such as `examples/MNIST_google_cloud/` or `examples/ImageNet_google_cloud/`, and follow the instructions in `examples/README.md`.

---

## Architecture

The repository is a Python package (`eco4cast`) with two top-level subsystems under `eco4cast/`, plus a set of examples and packaging files.

- **`eco4cast/master_machine`**: Contains a Google Cloud compute client library under `compute/client_library/`. The library is organized into:
  - **Ingredients**: per-resource modules grouped by resource type (for example, `instances`, `disks`, `firewall`, `snapshots`, `routes`, `usage_report`).
  - **Recipes**: runnable scripts organized in the same resource-type layout. The firewall recipe contains `<INGREDIENT />` markers, which suggest that ingredient code is incorporated into recipes, but the mechanism is not visible in the provided snippets.
  - **Snippets**: a parallel tree with the same resource-type layout.
  - **Test fixtures**: `sgs_test_fixtures/` (ingredients, recipes, output). No test modules were observed.
- **`eco4cast/virtual_machine`**: Present in the tree, but only an `__init__.py` file was observed. No source code was provided, so its role and interactions are unknown.
- **External dependency**: The compute client library pins `google-cloud-compute` (1.11.0) in `requirements.txt`. The package also declares ML and energy-tracking dependencies in `pyproject.toml` (including `torch`, `lightning`, and `eco2ai`), but the code that uses them was not observed.

The provided context does not show how the `master_machine` and `virtual_machine` subsystems communicate, or how control flows between them. Consult the source code for runtime interactions.

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Contributing

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). eco4cast-09sz5j9p repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{eco4cast-09sz5j9p,

        author = {README Benchmark},

        title = {eco4cast-09sz5j9p repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---