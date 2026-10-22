# eco4cast-5upypgrv

---

[![PyPi](https://badge.fury.io/py/eco4cast.svg)](https://badge.fury.io/py/eco4cast)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![lightning](https://img.shields.io/badge/Lightning-792EE5.svg?style=flat&logo=Lightning&logoColor=white)
![numpy](https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white)
![python](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikitlearn-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [License](#license)
- [Citation](#citation)

---

## Overview

eco4cast is a Python library designed to reduce the CO2 emissions of neural network training on Google Cloud. It targets machine learning researchers and engineers who train models in the cloud and want to track and reduce the carbon footprint of that work, as well as developers who need to automate Google Cloud compute resources programmatically. The package combines carbon-aware training support, including CO2 emission tracking, with tooling for automating cloud compute infrastructure. Runnable examples covering both local and cloud-based scenarios are included; see the Getting Started section for the first runnable steps.

---

## Core Features

- **Carbon-aware training** — Tracks CO2 emissions during neural-network training and is designed to reduce the carbon footprint of training workloads on Google Cloud, so developers can quantify and lower the environmental cost of their experiments.
- **PyTorch and Lightning support** — Works with standard PyTorch and Lightning training code, letting developers bring existing models into a carbon-aware cloud workflow.
- **Google Cloud Compute automation** — Programmatically manages Compute resources such as virtual-machine instances, firewall rules, disks, snapshots, and instance templates, so developers can provision and tear down training environments from code.
- **Scheduling and remote operation** — Provides task scheduling and SSH connectivity so developers can automate recurring jobs and manage remote machines without manual intervention.
- **Ready-to-run examples** — Includes working examples for both local and Google Cloud setups, covering image-classification scenarios such as MNIST and ImageNet, so developers can start from executable reference code.

---

## Installation

**Prerequisites:** requires Python 3.9+

Install eco4cast using one of the following methods:

**Using PyPi:**

```sh
pip install eco4cast
```

---

## Getting Started

**Prerequisites**

- Python 3.9+ and Poetry (the project is packaged with `poetry-core`).
- A Google Cloud project with Compute Engine, plus the `gcloud` CLI.
- An Electricity Maps API key (used by `CO2Predictor` to forecast CO2 intensity).

**Steps**

1. Clone the repository and install the package with Poetry:

```bash
git clone https://github.com/AIRI-Institute/eco4cast
cd eco4cast
poetry install
```

2. Authenticate with Google Cloud so application default credentials are available. The example `Controller` receives their location via `credentials_path` (e.g., `application_default_credentials.json` in the working directory):

```bash
gcloud auth application-default login
```

3. Put your Electricity Maps API key into `electricity_maps_api_key` in `examples/MNIST_google_cloud/master_machine_main.py` (an ImageNet variant with the same structure is available under `examples/ImageNet_google_cloud/`).

4. Adjust the `Controller(...)` parameters in the same file to match your environment: `project_id`, `current_zone`, `current_instance_name`, `current_vm_ip`, `ssh_username`, `ssh_port`, `ssh_python_path`, and `ssh_vm_main_path`.

5. On the training VM, provide a Python interpreter at `ssh_python_path` (e.g., `/home/scheduler/venv/bin/python`) and place your training script at `ssh_vm_main_path` (e.g., `/home/scheduler/scheduler_task/vm_main.py`). The script should be built on `IntervalTrainer` from `eco4cast.virtual_machine.smart_scheduler_concept`, as in the example `vm_main.py`.

6. Start carbon-aware training from the master machine:

```bash
python examples/MNIST_google_cloud/master_machine_main.py
```

The script calls `controller.start_training()` and finishes with `controller.stop_training()` once all intervals are complete. See `examples/README.md` for details on the bundled MNIST, ImageNet, and local/cloud demos.

---

## Examples

The repository bundles runnable examples covering both local and Google Cloud setups:

- **MNIST on Google Cloud** — carbon-aware image-classification training in `examples/MNIST_google_cloud/`, started from `master_machine_main.py`.
- **ImageNet on Google Cloud** — a variant with the same structure in `examples/ImageNet_google_cloud/`.
- **Local and cloud demos** — additional local and cloud-based scenarios; see `examples/README.md` for details.

Browse all examples [here](./examples).

---

## License

This project is licensed under the Apache License 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder author, title, year, and repository URL below with the real project metadata before publishing the citation.

### APA format:

    README Benchmark (2026). eco4cast-5upypgrv repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{eco4cast-5upypgrv,

        author = {README Benchmark},

        title = {eco4cast-5upypgrv repository},

        year = {2026},

        note = {Local repository checkout. Replace the placeholder author, title, year, and REPOSITORY_URL with the real project metadata before publishing.}

    }

---