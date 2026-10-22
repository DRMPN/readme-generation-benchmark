# eco2ai

eco2ai is a Python library for estimating the energy consumption and CO2 emissions of machine learning workloads. It measures CPU, NVIDIA GPU, and an estimated RAM contribution while your code runs, then writes the results to a CSV file.

## Overview

The package is described in its metadata as an "emission tracking library." It is developed under the `sb-ai-lab/Eco2AI` GitHub organization and is distributed under the Apache License 2.0.

The main entry point is the `Tracker` class. It:

- Samples power use at a configurable interval (`measure_period`, default 10 seconds).
- Estimates CPU power from the processor's TDP and measured utilization. TDP values come from a bundled table (`eco2ai/data/cpu_names.csv`).
- Reads GPU power through the `pynvml` library (NVIDIA devices).
- Estimates RAM power from the memory used by the current process.
- Looks up a carbon emission factor from a bundled table (`eco2ai/data/carbon_index.csv`), or uses a value you provide.
- Optionally calculates electricity cost from a time-of-day price schedule.
- Records one row per run, or one row per epoch during training, in a CSV file.

The package also includes:

- A `track` decorator that wraps a function with a tracker.
- Helper functions `available_devices()`, `set_params()`, `get_params()`, and `summary()`.
- Two Jupyter notebooks in `examples/` that demonstrate usage with TensorFlow/Keras and PyTorch.

## Installation

The example notebooks install the library with pip:

```bash
pip install eco2ai
```

To install from a source checkout, the project uses Poetry (`pyproject.toml` with `poetry-core` as the build backend):

```bash
git clone https://github.com/sb-ai-lab/Eco2AI.git
cd Eco2AI
poetry install
```

### Requirements

Dependencies declared in `setup.py`:

- `APScheduler`
- `pynvml` (>= 5.6.2)
- `psutil`
- `py-cpuinfo`

Additional dependencies declared in `pyproject.toml`:

- `pandas` (versions depend on the Python version: `>=1.2.1,<=1.3.5` for Python 3.7, `>=1.4.0` for Python 3.8 and later)
- `setuptools`
- `requests`
- `tzlocal`
- `tornado`

The `pyproject.toml` classifiers list Python 3.7, and the Python requirement is `*`. The notebooks were saved with Python 3.8.3.

Some features depend on operating system tools:

- **Linux:** CPU socket counting uses `lscpu`. If it is unavailable, the library warns (unless warnings are ignored) and assumes one CPU. The installation hint in the code refers to `util-linux`.
- **Windows:** CPU socket counting parses the output of `systeminfo`.
- **macOS:** CPU utilization is read with `top`.

GPU measurement requires an NVIDIA GPU supported by the NVML library. Without one, the tracker counts only CPU and RAM.

## Quick Start

```python
import eco2ai

tracker = eco2ai.Tracker(
    project_name="mnist",
    experiment_description="Convolutional model",
)

tracker.start()

# your CPU and GPU computations

tracker.stop()
```

After `stop()`, the results are written to `emission.csv` in the current working directory by default.

### Using the decorator

```python
from eco2ai import track

@track
def train_func():
    # your training code
    ...

train_func()
```

The decorator creates a `Tracker()` with default settings, starts it before the function runs, and stops it afterward, including when the function raises an exception.

### Tracking training by epoch

For training loops, use `start_training()`, `new_epoch()`, and `stop_training()`. The notebooks show this pattern with `epochs` in the training loop:

```python
tracker = eco2ai.Tracker(project_name="mnist", experiment_description="simple model")

tracker.start_training()
for epoch in range(2):
    # train for one epoch
    tracker.new_epoch({"epoch_loss": 0.1})  # optional parameters to save
tracker.stop_training()
```

Per the source, results are written when `new_epoch()` is called, so each epoch gets its own row. `new_epoch()` raises an error if it is called before `start_training()`.

### Utility functions

```python
import eco2ai

eco2ai.available_devices()          # prints detected CPU and GPU devices
df = eco2ai.summary("emission.csv") # per-project totals plus an "All the projects" row
```

`summary()` also accepts `write_to_file` to save its output. It requires a `.csv` file that contains a `project_name` column.

## Tracker Parameters

| Parameter | Default | Description |
|---|---|---|
| `project_name` | stored value (`"default project name"` if not set) | Project name written to the output. |
| `experiment_description` | stored value | Free-text description, such as the model type. |
| `file_name` | `"emission.csv"` | Output CSV file. Must end in `.csv`. |
| `measure_period` | `10` | Seconds between measurements. Must be positive. |
| `emission_level` | `None` | Mass of CO2 in kg per MWh of consumed energy. If set, the carbon index lookup is skipped. |
| `alpha_2_code` | `None` | ISO 3166-1 alpha-2 country code, used to select the emission factor. |
| `region` | `None` | Region, state, or district. Requires `alpha_2_code`. |
| `cpu_processes` | `"current"` | `"current"` measures only the current Python process. `"all"` measures total CPU use across processes. |
| `pue` | `1` | Power usage effectiveness multiplier applied to consumption. |
| `encode_file` | `None` | If set, also writes encoded results to a CSV file. Set to `True` to use `"encoded_" + file_name`, or pass a `.csv` file name. |
| `electricity_pricing` | `None` | Dictionary mapping time intervals to prices (see below). |
| `ignore_warnings` | `False` | Suppresses warnings when `True`. |
| `timezone` | `False` | Sets the scheduler timezone manually when automatic detection fails. |

`Tracker` methods include `start()`, `stop()`, `start_training(start_epoch=1)`, `new_epoch(parameters_dict)`, `stop_training()`, `consumption()`, `price()`, `id()`, `emission_level()`, and `measure_period()`. Call `start()` or `start_training()` before `stop()`. Otherwise, `stop()` raises an exception.

## Configuration

### Emission factor

Unless `emission_level` is given, the tracker determines the emission factor as follows:

1. If `alpha_2_code` is not provided, the library calls `https://ipinfo.io/` to detect the country and region from your IP address. The source warns that VPNs may cause the wrong country to be detected.
2. The library searches `eco2ai/data/carbon_index.csv` for the country. If no match exists, it uses the `World` entry.
3. When the country has several entries, the library selects the one matching `region`. If no region matches, it warns and uses the "Whole country" entry.

Passing `region` without `alpha_2_code` raises `NoCountryCodeError`.

### Electricity pricing

`electricity_pricing` maps intervals in `"hh:mm-hh:mm"` format to prices, without currency symbols. The source requires:

- Hours in the range 0 to 23 and minutes in the range 0 to 59.
- Intervals that do not overlap and appear in chronological order.
- A total duration of exactly 24 hours.

Example from the docstring of consistent intervals: `"8:30-19:00"`, `"19:00-6:00"`, `"6:00-8:30"`.

The library validates the dictionary when the tracker is created and raises `IncorrectPricingDict` if it is invalid.

### Stored defaults

`set_params()` writes default values to `eco2ai/data/config.txt`, a JSON file inside the package. `get_params()` reads it. The file in this repository currently contains:

```json
{"project_name": "YourProjectName", "experiment_description": "training the <your model> model", "file_name": "my_emission.csv", "measure_period": 1, "pue": 1}
```

When `Tracker` is created, each parameter that is not passed is taken from this file. Creating a tracker also saves its settings back to this file. Be aware of this if you rely on the default output file name.

### Output format

Each row in the output CSV contains these columns:

- `id` (UUID of the run)
- `project_name`
- `experiment_description`
- `epoch`
- `start_time`
- `duration(s)`
- `power_consumption(kWh)`
- `CO2_emissions(kg)`
- `CPU_name` (including TDP)
- `GPU_name`
- `OS`
- `region/country`
- `cost`

If `encode_file` is set, the same values are written to a second file after being passed through the library's `encode()` function. The source describes this as encoding, not encryption, and it is a simple character substitution.

### Power estimation

- **CPU:** TDP × measured utilization × CPU count × elapsed time. Processors missing from the table use a constant of 100.1 W and produce a warning.
- **GPU:** Power readings from NVML are integrated over time.
- **RAM:** Memory used by the current process, in GB, multiplied by 3/8 W per GB.

Consumption is multiplied by `pue`. Results are estimates based on these models, not direct hardware metering.

## Examples

The `examples/` directory contains two notebooks:

- `Eco2AI tutorial tensorflow.ipynb` trains MNIST models with Keras. It compares a convolutional model and a simpler model, then shows a function wrapped with `@track`.
- `Eco2AI tutorial torch.ipynb` trains a PyTorch CNN on MNIST with tracking around the training loop and a decorated function.

Both notebooks read the resulting `emission.csv` file with pandas.

## Development

### Project layout

- `eco2ai/emission_track.py`: `Tracker` class, `track` decorator, and version constant (`__version__ = '0.3.12'`).
- `eco2ai/utils.py`: carbon index lookup, pricing, encoding, parameter storage, and `summary()`.
- `eco2ai/tools/`: CPU, GPU, and RAM measurement modules.
- `eco2ai/data/`: carbon index, CPU TDP table, and default configuration.
- `eco2ai/MLTracker.py`: placeholder with a comment saying it is for future versions.

### Build configuration

The project has both `pyproject.toml` (Poetry) and `setup.py`. `pyproject.toml` defines the package metadata, the authors, and the dependencies. The `setup.py` file reads `README.md` for its long description and lists package data files, but it references `__version__` without defining it, so running it as written will fail.

### Contributing

The `.github/ISSUE_TEMPLATE/` directory contains templates for bug reports and feature requests. No separate contributing guide is included in the repository.

## Testing

The supplied repository contains no test files, test directory, or test configuration. The `pyproject.toml` dev-dependencies section is empty. Verification is currently done through the example notebooks.

## Authors

The authors listed in `pyproject.toml` are the AI Lab team, Vladimir Lazarev, Nikita Zakharenko, Semyon Budyonny, Leonid Zhukov, and Alexey Korovin.

## License

This project is licensed under the Apache License, Version 2.0. The copyright notice in the `LICENSE` file names Vladimir Lazarev, Nikita Zakharenko, Semyon Budyonny, and Leonid Zhukov. See the [LICENSE](LICENSE) file for the full terms.
