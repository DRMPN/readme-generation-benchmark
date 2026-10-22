# Eco2AI-25i1c9j2

---

[![PyPi](https://badge.fury.io/py/eco2ai.svg)](https://badge.fury.io/py/eco2ai)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Eco2AI is a Python library that estimates CO2 emissions produced by computation. It uses a `Tracker` class to measure CPU, GPU, and RAM usage over a run and convert the resulting energy use into emissions based on carbon intensity data. It is intended for developers, particularly those training machine learning models, who want to measure the energy and emissions footprint of their code. The library exposes a Python programmatic interface, and the repository includes tutorial notebooks for TensorFlow and PyTorch workflows; see Getting Started for installation and runnable steps.

---

## Core Features

- **Estimates CO2 emissions from hardware usage:** The `Tracker` class measures CPU, GPU, and RAM usage during computation so developers can see the estimated emissions of their workloads.
- **Periodic background measurement:** Measurements run on a background scheduler at a configurable interval, so tracking does not require manual sampling during a run.
- **Automatic or manual carbon intensity configuration:** Emission factors can be derived from a country code and optional region, or set directly with a custom emission level, so results match the user's grid.
- **GPU and CPU device discovery:** Helper functions report the CPU and NVIDIA GPU devices available on the system, helping developers confirm what will be tracked.
- **Optional electricity pricing and PUE:** Time-of-day electricity pricing and a power usage effectiveness value can be supplied to adjust cost and energy calculations for data center or tariff-based scenarios.

---

## Installation

**Prerequisites:** requires Python *

Install Eco2AI-25i1c9j2 using one of the following methods:

**Using PyPi:**

```sh
pip install eco2ai
```

---

## Getting Started

### Prerequisites

- Python with `pip`.
- Optional, for the example notebooks: TensorFlow or PyTorch, depending on the notebook you run.
- Optional, for GPU tracking: an NVIDIA GPU supported by the `pynvml` library. Without one, the tracker considers CPU usage only.

### Steps

1. Install the package:

```bash
   pip install eco2ai
```

2. Install TensorFlow or PyTorch if you plan to run the example notebooks:
   - `examples/Eco2AI tutorial tensorflow.ipynb` requires TensorFlow.
   - `examples/Eco2AI tutorial torch.ipynb` requires PyTorch.

3. Run a minimal tracking session. Create the `Tracker` before any CPU or GPU work, then call `start()` and `stop()` around your computation:

```python
   import eco2ai

   tracker = eco2ai.Tracker(project_name="mnist", experiment_description="Convolutional model")
   tracker.start()
   # your CPU and GPU computations
   tracker.stop()
```

4. Alternatively, open one of the example notebooks listed in step 2 and run its cells in order.

**Note:** If `alpha_2_code` is not set, the `Tracker` looks up your country through `https://ipinfo.io/`, which requires network access. Setting `alpha_2_code` avoids this lookup. If you use a VPN, the country lookup may be inaccurate.

---

## API Reference

Public symbols are exported from `eco2ai/__init__.py`. Import them directly from the `eco2ai` package.

### Exported symbols

| Symbol | Source | Purpose |
|---|---|---|
| `Tracker` | `eco2ai/emission_track.py` | Measures CPU, GPU, and RAM usage and estimates CO2 emissions. |
| `track` | `eco2ai/emission_track.py` | Tracking interface exported from the package. |
| `__version__` | `eco2ai/emission_track.py` | Package version string (`'0.3.12'`). |
| `CPU` | `eco2ai/tools/tools_cpu.py` | CPU measurement interface. |
| `all_available_cpu` | `eco2ai/tools/tools_cpu.py` | Lists available CPU devices. |
| `GPU` | `eco2ai/tools/tools_gpu.py` | NVIDIA GPU measurement interface (uses pynvml). |
| `all_available_gpu` | `eco2ai/tools/tools_gpu.py` | Lists available GPU devices. |
| `RAM` | `eco2ai/tools/tools_ram.py` | RAM measurement interface. |
| `available_devices` | `eco2ai/utils.py` | Prints available CPU and GPU devices. Takes no parameters. |
| `set_params` | `eco2ai/utils.py` | Parameter setter. |
| `get_params` | `eco2ai/utils.py` | Parameter getter. `Tracker` reads its defaults through it. |
| `summary` | `eco2ai/utils.py` | Summary helper. |

### `Tracker`

Create one `Tracker` per calculation. Call `start()` before your workload and `stop()` after it.

```python
from eco2ai import Tracker

tracker = Tracker(project_name='my_project')
tracker.start()
# your CPU and GPU calculations
tracker.stop()
```

**Constructor parameters**

- `project_name` (default `None`): project name stored in the results.
- `experiment_description` (default `None`): experiment description.
- `file_name` (default `None`): results file name. Must end with `.csv`.
- `measure_period` (default `10`): measurement interval in seconds. Must be positive.
- `emission_level` (default `None`): kg of CO2 per MWh of consumed energy.
- `alpha_2_code` (default `None`): ISO-Alpha-2 country code.
- `region` (default `None`): country region, state, or district. Requires `alpha_2_code`.
- `cpu_processes` (default `'current'`): `'current'` measures the current process only. `'all'` measures the sum of all running processes.
- `pue` (default `1`): power usage effectiveness.
- `encode_file` (default `None`): if set, writes encoded results. `True` uses `encoded_` plus `file_name`. A string sets the file name. Must end with `.csv`.
- `electricity_pricing` (default `None`): dictionary mapping `'hh:mm-hh:mm'` intervals to prices. Intervals must be consistent and total 24 hours.
- `ignore_warnings` (default `False`): suppresses warnings when `True`.
- `timezone` (default `False`): sets the timezone directly when automatic detection fails.

**Methods**

- `start()`: starts measurement.
- `stop()`: stops measurement.

### `GPU`

The class docstring states that `GPU` is intended for use inside `Tracker`, not separately.

| Method | Purpose |
|---|---|
| `GPU(ignore_warnings=False)` | Initializes the GPU interface and checks GPU availability. |
| `calculate_consumption()` | Calculates GPU energy consumption since the last call and returns it. |
| `get_consumption()` | Returns the accumulated GPU consumption. |
| `gpu_memory()` | Returns memory information per GPU. |
| `gpu_temperature()` | Returns the temperature per GPU. |
| `gpu_power()` | Returns the power consumption per GPU. |
| `gpu_power_limit()` | Returns the enforced power limit per GPU. |
| `name()` | Returns the GPU name, or an empty string if no GPU is visible. |
| `gpu_num()` | Returns the number of visible GPUs, or `0` on error. |

### Exceptions and warnings

- `IncorrectMethodSequenceError` (`eco2ai/emission_track.py`)
- `FileDoesNotExistsError` (`eco2ai/utils.py`)
- `NotNeededExtensionError` (`eco2ai/utils.py`)
- `NoCountryCodeError` (`eco2ai/utils.py`)
- `IncorrectPricingDict` (`eco2ai/utils.py`)
- `NoGPUWarning` (`eco2ai/tools/tools_gpu.py`)

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

    README Benchmark (2026). Eco2AI-25i1c9j2 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{Eco2AI-25i1c9j2,

        author = {README Benchmark},

        title = {Eco2AI-25i1c9j2 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---