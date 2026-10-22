# Eco2AI

**Eco2AI** is an open-source CO2 emission tracking library for Python. It measures the power consumption of your CPU, GPU and RAM during computations and estimates the resulting CO2 emissions, writing the results to a CSV file. It is intended primarily for tracking the carbon footprint of machine learning experiments and training runs.

Current version: **0.3.12** (development status: Alpha).

## How It Works

- The **CPU** power consumption is estimated from the CPU model's TDP (taken from a bundled database of CPU names, `data/cpu_names.csv`), the measured CPU utilization, and the number of CPU sockets. If a CPU is not found in the database, a constant TDP value is used as a fallback.
- The **GPU** power consumption is measured directly via the NVIDIA `pynvml` (NVML) library. GPU tracking is supported only for NVIDIA GPUs; if no supported GPU is present, the tracker accounts for CPU usage only.
- The **RAM** power consumption is estimated from the amount of virtual memory used by the current process.
- The **carbon index** (kg of CO2 per MWh of consumed energy) is determined automatically from your IP address (country and region), using a bundled regional carbon index database (`data/carbon_index.csv`). If the country is not found in the database, the worldwide average is used.

All measured consumption is multiplied by a configurable **PUE** (Power Usage Effectiveness) factor, which is especially relevant when running on data-center hardware.

Results are written to a CSV file with the following columns:

- `id`
- `project_name`
- `experiment_description`
- `epoch`
- `start_time`
- `duration(s)`
- `power_consumption(kWh)`
- `CO2_emissions(kg)`
- `CPU_name`
- `GPU_name`
- `OS`
- `region/country`
- `cost`

The `summary()` utility additionally aggregates these results per project and produces a total summary across all projects (total duration, total power consumption, total CO2 emissions and total electricity cost).

## Installation

Install from PyPI:

```bash
pip install eco2ai
```

Or install from source using Poetry:

```bash
git clone https://github.com/sb-ai-lab/Eco2AI
cd Eco2AI
poetry install
```

### Dependencies

Core dependencies (managed by `pyproject.toml`):

- Python 3.7+
- `pandas` (>= 1.2.1)
- `setuptools`
- `APScheduler`
- `requests`
- `pynvml` (for NVIDIA GPU tracking)
- `psutil` (>= 5.9.1)
- `tzlocal`
- `tornado`
- `py-cpuinfo`

GPU tracking additionally requires the NVIDIA driver to be available on the system.

On Linux, the `util-linux` package is recommended so the library can determine the number of CPU sockets correctly (otherwise the number of CPUs is set to 1, with a warning).

## Quick Start

The central class is `eco2ai.Tracker`. It is recommended to create a new `Tracker` object per every new calculation, and to create it before any CPU/GPU work begins.

```python
import eco2ai

tracker = eco2ai.Tracker(
    project_name="mnist",
    experiment_description="Convolutional model"
)

tracker.start()

# your CPU / GPU calculations here, e.g. model training

tracker.stop()
```

Results are appended to the output CSV file (by default `emission.csv`):

```python
import pandas as pd
df = pd.read_csv("emission.csv")
print(df)
```

### Decorator Usage

Any function can be wrapped with the `@track` decorator, which creates a `Tracker`, starts it before the function runs, and stops it afterwards (even if an exception is raised):

```python
from eco2ai import track

@track
def train_func():
    # training code
    ...

train_func()
```

### Tracking Training Epochs

For model training, the tracker provides an epoch-based interface. Results are written to the file only after each `.new_epoch()` call:

```python
tracker = eco2ai.Tracker(project_name="mnist", experiment_description="training")
tracker.start_training(start_epoch=1)

for epoch in range(num_epochs):
    # train one epoch
    tracker.new_epoch({"loss": current_loss})

tracker.stop_training()
```

The `parameters_dict` passed to `new_epoch` (e.g., the loss value) is saved in the `epoch` column of the output file.

## API Overview

### `eco2ai.Tracker`

Main tracking class.

**Key constructor parameters:**

| Parameter | Description | Default |
|---|---|---|
| `project_name` | Name of your project | `None` (from config / `"default project name"`) |
| `experiment_description` | Description of the experiment (e.g., model type) | `None` |
| `file_name` | Name of the CSV file for results | `None` (from config / `"emission.csv"`) |
| `measure_period` | Period between power measurements, in seconds. Must be a positive number | `10` |
| `emission_level` | CO2 mass in kg produced per MWh; overrides automatic detection | `None` |
| `alpha_2_code` | ISO Alpha-2 country code (see https://www.iban.com/country-codes) | `None` |
| `region` | Country region/state/district; requires `alpha_2_code` | `None` |
| `cpu_processes` | `"current"` — measure utilization of the current process only; `"all"` — measure full CPU utilization | `"current"` |
| `pue` | Power Usage Effectiveness (ratio of total facility power to IT equipment energy) | `1` |
| `encode_file` | If set (str ending in `.csv`), results are also written to an encoded file (by default `encoded_` + `file_name`) | `None` |
| `electricity_pricing` | Dict mapping time intervals to electricity prices (no currency units). Intervals are formatted `"hh:mm-hh:mm"`, must not overlap, must be in chronological order, and must total exactly 24 hours | `None` |
| `ignore_warnings` | If `False`, warnings are shown | `False` |
| `timezone` | Explicitly set the timezone; useful when automatic detection fails | `False` |

**Methods:**

- `start()` — starts tracking (initializes CPU/GPU/RAM tools and the measurement scheduler).
- `stop()` — stops tracking and writes final results to the CSV file.
- `start_training(start_epoch=1)` — starts tracking in training mode.
- `new_epoch(parameters_dict)` — records the finished epoch (with the given parameters) and starts a new one.
- `stop_training()` — stops tracking in training mode.
- `consumption()` — returns accumulated power consumption.
- `price()` — returns total accumulated electricity price.
- `id()` — returns the random UUID id of this tracker run.
- `emission_level()` — returns the CO2 emission level (kg per MWh) in use.
- `measure_period()` — returns the measurement period.

### Decorator

- `eco2ai.track(func)` — decorator that wraps a function with `Tracker().start()` / `.stop()`.

### Utilities

- `eco2ai.available_devices()` — prints all visible CPU and GPU devices.
- `eco2ai.set_params(**params)` — sets default Tracker parameters (`project_name`, `experiment_description`, `file_name`, `measure_period`, `pue`) stored in the internal config file.
- `eco2ai.get_params()` — returns the current default parameter values.
- `eco2ai.summary(filename, write_to_file=False)` — aggregates a results CSV per project and overall; optionally writes the summary to another CSV file.

### Device Tools

Lower-level device interfaces (used internally by `Tracker`, but also importable):

- `eco2ai.tools.tools_cpu.CPU`, `eco2ai.tools.tools_cpu.all_available_cpu()`
- `eco2ai.tools.tools_gpu.GPU`, `eco2ai.tools.tools_gpu.all_available_gpu()` — also exposes `gpu_memory()`, `gpu_temperature()`, `gpu_power()`, `gpu_power_limit()`, `gpu_num()` and `name()` via NVML.
- `eco2ai.tools.tools_ram.RAM`

## Configuration

Default values for `project_name`, `experiment_description`, `file_name`, `measure_period` and `pue` are stored in an internal JSON config file (`eco2ai/data/config.txt`). You can change these defaults either by passing parameters to `Tracker(...)` or programmatically:

```python
import eco2ai

eco2ai.set_params(
    project_name="MyProject",
    experiment_description="training the ResNet model",
    file_name="my_emission.csv",
    measure_period=1,
    pue=1,
)
```

## Important Notes

- **VPN:** if you use a VPN, automatic country detection by IP may fail. It is recommended to disable the VPN, or manually specify the ISO Alpha-2 code of your country via the `alpha_2_code` parameter.
- **Measurement accuracy:** create the `Tracker` before any CPU/GPU usage so consumption is measured correctly.
- The library supports **Windows, Linux and MacOS** for CPU utilization measurement.
- If your CPU model is not found in the bundled TDP database, a constant TDP of 100 W is used (a warning is issued unless suppressed).

## Examples

The `examples/` directory contains Jupyter notebook tutorials demonstrating Eco2AI with both PyTorch and TensorFlow, including MNIST training with the `Tracker` class, the `@track` decorator, and inspecting the resulting `emission.csv` file:

- `examples/Eco2AI tutorial torch.ipynb`
- `examples/Eco2AI tutorial tensorflow.ipynb`

## Development

The project uses [Poetry](https://python-poetry.org/) for dependency management (`pyproject.toml`, `poetry.lock`). The package metadata declares Python 3.7+ support, OS-independent operation, and typed code.

Repository structure:

```
eco2ai/
├── MLTracker.py        # reserved for future versions
├── __init__.py         # public API (Tracker, track, tools, utils)
├── emission_track.py   # Tracker class and track decorator
├── utils.py            # utilities: config, carbon index, pricing, summary, encoding
├── tools/
│   ├── tools_cpu.py    # CPU power consumption tracking
│   ├── tools_gpu.py    # GPU power consumption tracking (NVML)
│   └── tools_ram.py    # RAM power consumption tracking
└── data/
    ├── carbon_index.csv  # regional carbon index database
    ├── cpu_names.csv     # CPU TDP database
    └── config.txt        # default parameter config
```

The package can also be built and installed with `setuptools` via the provided `setup.py`.

## Issues and Contributions

Bug reports and feature requests are welcome — the repository provides GitHub issue templates for [bug reports](.github/ISSUE_TEMPLATE/bug_report.md) and [feature requests](.github/ISSUE_TEMPLATE/feature_request.md). When filing a bug, please include a description of the bug, steps to reproduce, expected behavior, and your environment details (OS, browser/version if relevant).

## License

This project is licensed under the **Apache License, Version 2.0**. See the [LICENSE](LICENSE) file for the full license text.

Copyright © Vladimir Lazarev, Nikita Zakharenko, Semyon Budyonny, Leonid Zhukov.

The library is developed by **AI Lab** / SB AI Lab — repository: https://github.com/sb-ai-lab/Eco2AI
