# eco2ai

`eco2ai` is a Python library for tracking estimated energy use and CO₂ emissions during CPU, RAM, and supported GPU workloads. It records measurements to a CSV file, along with experiment and machine details. The package also offers electricity-cost estimates, a function decorator, and a training-oriented interface for recording results by epoch.

The package version in this repository is **0.3.12**. Its project metadata describes it as an alpha-stage scientific and AI tool.

## How tracking works

Create a `Tracker` before the workload you want to measure, then call `start()` and `stop()`. While running, it samples device use at a configurable interval and accumulates estimated energy consumption. Results include estimated CO₂ emissions based on an emission factor in kilograms of CO₂ per megawatt-hour.

CPU use is estimated from processor information and utilization. RAM use is based on the current process’s memory use. GPU monitoring uses NVIDIA’s NVML interface; when no supported GPU is available, the tracker records CPU and RAM use instead. These are estimates, not direct measurements of total system electricity use.

By default, the library attempts to identify the country and region from the machine’s IP address using `ipinfo.io`, then looks up an emission factor in its bundled carbon-index data. VPN use may affect location detection. You can provide a country code, region, or emission factor yourself.

## Installation

Install the published package with pip:

```bash
pip install eco2ai
```

The project metadata lists dependencies including pandas, APScheduler, requests, pynvml, psutil, tzlocal, tornado, and py-cpuinfo. GPU monitoring uses NVIDIA’s NVML library. The TensorFlow and PyTorch notebooks also require their respective machine-learning frameworks and additional plotting and image libraries; those are example-specific rather than core tracker requirements.

To use the repository’s examples, install the relevant framework and open either notebook in `examples/`:

- `Eco2AI tutorial tensorflow.ipynb`
- `Eco2AI tutorial torch.ipynb`

The notebooks demonstrate tracking MNIST training and reading the resulting CSV file.

## Basic usage

```python
import eco2ai

tracker = eco2ai.Tracker(
    project_name="image-classification",
    experiment_description="initial model run",
    file_name="emission.csv",
)

tracker.start()
try:
    # Run the workload you want to measure.
    ...
finally:
    tracker.stop()
```

`start()` begins periodic measurements. `stop()` ends tracking and writes the results to the configured CSV file. The default output filename is `emission.csv` unless changed by constructor arguments or stored configuration.

The tracker can also wrap a function with the `track` decorator:

```python
from eco2ai import track

@track
def train_model():
    # Run the workload you want to measure.
    ...

train_model()
```

The decorator creates and starts a tracker for the function call, then stops tracking when the call finishes.

For epoch-based workloads, use the training interface:

```python
tracker = eco2ai.Tracker(project_name="training-run")
tracker.start_training(start_epoch=1)

# Run one epoch of work.
tracker.new_epoch({"loss": 0.42, "learning_rate": 0.001})

# Run another epoch, then record it.
tracker.new_epoch({"loss": 0.31, "learning_rate": 0.001})

tracker.stop_training()
```

`start_training()` initializes tracking for the training workflow. Call `new_epoch()` after each epoch you want recorded; its dictionary values are stored with the epoch entry. The training API is separate from the regular `start()` / `stop()` interface.

## Configuration

`Tracker` accepts these principal options:

| Option | Purpose |
| --- | --- |
| `project_name` | Project label written to the results. |
| `experiment_description` | Description of the experiment. |
| `file_name` | CSV results filename; names must end in `.csv`. |
| `measure_period` | Measurement interval in seconds; the default is 10 seconds. |
| `emission_level` | User-supplied emission factor in kg CO₂ per MWh. |
| `alpha_2_code` | Country ISO alpha-2 code used to select an emission factor. |
| `region` | Region within the selected country, when available. |
| `cpu_processes` | `"current"` tracks the current process; `"all"` uses system-wide CPU utilization. |
| `pue` | Power usage effectiveness multiplier; defaults to 1. |
| `electricity_pricing` | Optional time-of-day electricity prices for estimating cost. |
| `encode_file` | Optional CSV output for encoded results. |
| `ignore_warnings` | Controls warning behavior. |
| `timezone` | Optional timezone override for the scheduler. |

When `emission_level` is omitted, the library uses its carbon-index data and location lookup. Setting `region` requires `alpha_2_code`. The default project name, description, filename, measurement period, and PUE can also be managed through `set_params()` and read with `get_params()`. The repository includes a bundled `eco2ai/data/config.txt` containing these defaults.

For electricity pricing, pass a dictionary mapping time intervals to numeric prices, without a currency designation. Intervals use `hh:mm-hh:mm` strings, must be ordered and non-overlapping, and must cover a full 24-hour day. For example:

```python
pricing = {
    "8:30-19:00": 0.20,
    "19:00-6:00": 0.10,
    "6:00-8:30": 0.15,
}

tracker = eco2ai.Tracker(electricity_pricing=pricing)
```

The tracker’s `consumption()`, `price()`, `id()`, `emission_level()`, and `measure_period()` methods expose values for the current tracker instance. `summary(filename)` reads a results CSV and returns totals by project and for all projects; pass `write_to_file` to save the summary. `available_devices()` prints detected CPU and GPU information.

## Results

The results CSV includes an ID, project name, experiment description, epoch information, start time, duration in seconds, energy consumption in kWh, CO₂ emissions in kg, CPU and GPU details, operating system, region or country, and estimated cost. A run writes to the configured output file, creating it if necessary or adding to it if it already exists.

The `summary()` utility expects a CSV with the tracker’s result columns and returns a pandas DataFrame with total duration, energy, emissions, and electricity cost for each project and for all projects combined.

## Development and examples

The repository includes package source under `eco2ai/`, bundled CPU-name and carbon-index data, Poetry metadata in `pyproject.toml` and `poetry.lock`, and a `setup.py` packaging entry point. The Poetry configuration declares no development dependencies. The TensorFlow and PyTorch notebooks provide end-to-end examples of model training, tracker use, and CSV inspection.

Bug reports and feature requests can be submitted using the templates in `.github/ISSUE_TEMPLATE/`. No dedicated automated test suite or test command is included in the supplied repository files. For validation, run the relevant example notebook in an environment with its required framework and dependencies, then inspect the generated CSV.

## License

This project is distributed under the **Apache License, Version 2.0**. See [`LICENSE`](LICENSE) for the full terms.
