# Eco2AI-pcjrwewu

---

[![PyPi](https://badge.fury.io/py/eco2ai.svg)](https://badge.fury.io/py/eco2ai)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Eco2AI is a Python library for tracking the energy consumption, CO2 emissions, and electricity cost of CPU and GPU compute during machine learning workloads. It is intended for ML researchers and practitioners who want per-experiment accounting of these quantities for their training runs, as well as developers integrating emission tracking into their own scripts or pipelines. The library exposes a tracker that is started before and stopped after a block of computation; it samples power consumption in the background at a configurable interval and records the results alongside user-defined project and experiment metadata. It is imported into training scripts or interactive notebooks, and runnable tutorial notebooks demonstrate typical usage for model training.

---

## Core Features

- **Automatic emission tracking for ML workloads** — measures CPU and GPU power consumption at a configurable sampling interval and converts it into energy use and CO2 emissions, giving every experiment a concrete environmental footprint without changes to your training code.
- **Location-aware carbon intensity** — automatically identifies your country and region via IP and applies the matching carbon index from a bundled database, with manual overrides and fallback to broader averages, so emissions reflect your actual grid without manual data lookup.
- **Electricity cost estimation** — supports time-of-use electricity prices defined as daily time intervals, so experiments report the monetary cost of consumed energy alongside emissions.
- **Per-experiment CSV reporting** — writes results tagged with a project name and experiment description and can optionally produce an encoded copy of the results, making runs easy to collect, compare, and log.
- **Data-center-aware accounting** — an adjustable power usage effectiveness (PUE) parameter accounts for facility overhead, yielding realistic consumption figures when training on data-center infrastructure.

---

## Installation

**Prerequisites:** requires Python 3.7.

Install Eco2AI-pcjrwewu using one of the following methods:

**Using PyPi:**

```sh
pip install eco2ai
```

---

## Usage

Eco2AI is used as a Python library: you wrap your training (or any CPU/GPU-heavy) code between a tracker's `start()` and `stop()` calls.

### Basic pattern

```python
import eco2ai

tracker = eco2ai.Tracker(project_name="mnist", experiment_description="Convolutional model")
tracker.start()

# ... your training / inference code ...

tracker.stop()
```

The tracker samples CPU and GPU power consumption in the background (via APScheduler) between `start()` and `stop()`, then writes results to a CSV file.

### Common parameters

`eco2ai.Tracker(...)` accepts (among others):

- `project_name`, `experiment_description` – labels for the experiment.
- `file_name` – name of the output CSV file (must end with `.csv`; defaults are resolved from the library config).
- `measure_period` – interval in seconds between power measurements (default `10`, must be positive).
- `emission_level`, `alpha_2_code`, `region` – override the CO2 emission level and location instead of automatic IP-based lookup.
- `cpu_processes` – `"current"` (only the current process, default) or `"all"` (sum of all running processes).
- `pue` – power usage efficiency factor for data-center setups (default `1`).
- `encode_file` – additionally write an encoded copy of the results (with a `.csv` extension).
- `electricity_pricing` – dict mapping `"hh:mm-hh:mm"` time intervals to electricity prices (intervals must be non-overlapping, in chronological order, and cover 24 hours).
- `ignore_warnings`, `timezone` – suppress advisory warnings and set the timezone explicitly if auto-detection fails.

### Important note on timing

Per the library's own documentation, create the `Tracker` **before** any CPU or GPU usage so that power consumption is measured correctly, and create a new `Tracker` object per calculation.

### Country / region lookup

By default, the country carbon index is resolved from your IP address. If you use a VPN or prefer a manual setup, pass an ISO Alpha-2 country code (see [iban.com/country-codes](https://www.iban.com/country-codes)) and optionally a region:

```python
tracker = eco2ai.Tracker(project_name="mnist", alpha_2_code="US", region="New York")
```

### Helper utilities

Beyond the `Tracker`, the package may also expose the following helper utilities via `import eco2ai` (confirm availability against your installed version):

- `eco2ai.available_devices()` – prints all available CPU and GPU devices.
- `eco2ai.get_params()` / `eco2ai.set_params(...)` – read and persist default Tracker parameters.
- `eco2ai.summary(...)` – summarize results files (imported from `eco2ai.utils`).
- `from eco2ai import track` – an alternative tracking entry point re-exported from `eco2ai.emission_track`.

### Full examples

Complete, runnable tutorials covering PyTorch and TensorFlow (MNIST training wrapped with `Tracker`/`start()`/`stop()`) are available in the `examples/` directory of the repository (`Eco2AI tutorial torch.ipynb`, `Eco2AI tutorial tensorflow.ipynb`).

---

## Examples

Runnable tutorials are available in the [`examples/`](./examples) directory:

- **`Eco2AI tutorial torch.ipynb`** – MNIST training with PyTorch, wrapped with `Tracker`/`start()`/`stop()`.
- **`Eco2AI tutorial tensorflow.ipynb`** – MNIST training with TensorFlow, wrapped with `Tracker`/`start()`/`stop()`.

---

## Contributing

Contributions are welcome.

- To report a bug or suggest a feature, open an issue in the project's issue tracker.
- To contribute code: fork the repository, create a feature branch, make your changes in line with the existing code style, and open a pull request describing the change and its motivation.
- If you change library behavior, keep the tutorial notebooks in `examples/` runnable.

---

## License

This project is licensed under the Apache 2.0 license. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

The templates below are placeholders: the author, year, and repository URL are not confirmed for this checkout. If you use this project, replace **all** placeholders with the canonical publication details before citing.

### APA format:

    <AUTHOR> (<YEAR>). Eco2AI [Computer software]. <REPOSITORY_URL>

### BibTeX format:

    @misc{eco2ai,

        author = {<AUTHOR>},

        title = {Eco2AI},

        year = {<YEAR>},

        note = {<REPOSITORY_URL>}

    }

---