# eco2ai

`eco2ai` is a Python library for estimating the energy use and associated CO₂ emissions of a running computation. A `Tracker` periodically samples CPU, NVIDIA GPU, and process memory usage, accumulates estimated energy consumption, and writes results to a CSV file.

The package metadata identifies this checkout as version **0.3.12**. Its estimates use CPU TDP data (with a fallback when a model is not found), NVIDIA GPU power readings through NVML when available, and a memory-use-based RAM estimate. These are estimates, not direct measurements of total facility energy.

## Installation

Install the package from PyPI:

```bash
pip install eco2ai
```

The package declares dependencies for CPU, memory, scheduling, and NVIDIA monitoring. GPU tracking is available only when NVIDIA devices are visible to NVML; without one, the tracker warns and continues with CPU and RAM estimates.

## Quick start

Create and start a tracker before the work you want to measure, then stop it afterward:

```python
from eco2ai import Tracker

tracker = Tracker(
    project_name="example",
    experiment_description="model training",
    file_name="emissions.csv",
    measure_period=1,
    alpha_2_code="US",
)

tracker.start()

# Run the computation to track here.

tracker.stop()
print("Estimated energy (kWh):", tracker.consumption())
print("Estimated emissions (kg CO2):", tracker.consumption() * tracker.emission_level() / 1000)
```

`start()` begins periodic sampling; `stop()` stops sampling and writes the final result. A tracker creates a new result entry identified by a UUID. Reusing the same output CSV appends results for separate tracker IDs.

## Output

The results CSV includes the tracker ID, project and experiment names, epoch information, start time, duration in seconds, estimated energy in kWh, estimated CO₂ emissions in kg, CPU and GPU names, operating system, country/region, and cost. During ordinary tracking, periodic samples update that tracker’s result; the final result is written when tracking stops.

By default, the emissions factor is looked up using the country and region inferred from the request to `https://ipinfo.io/` and the package’s bundled `eco2ai/data/carbon_index.csv` table. This lookup needs network access. To avoid location lookup, provide `alpha_2_code`; to provide a region, also provide its country code. You can instead pass `emission_level` directly, in kg CO₂ per MWh. The reported emissions are calculated from estimated kWh and that factor.

## Tracking a function with a decorator

The `track` decorator creates a default `Tracker`, starts it before calling the function, and stops it afterward:

```python
from eco2ai import track

@track
def train_model():
    # Run training here.
    pass

train_model()
```

For custom tracker settings or output paths, use the explicit `Tracker` interface instead.

## Tracker options

`Tracker` accepts these options:

| Option | Purpose |
| --- | --- |
| `project_name` | Project label stored with the result. If omitted, the configured default is used. |
| `experiment_description` | Description stored with the result. If omitted, the configured default is used. |
| `file_name` | Results CSV path. If omitted, the configured default is used. Use a `.csv` filename. |
| `measure_period` | Sampling interval in seconds; defaults to 10 seconds. Must be positive. |
| `emission_level` | Explicit emissions intensity in kg CO₂/MWh. If provided, it is used instead of a table lookup. |
| `alpha_2_code` | Country’s ISO 3166-1 alpha-2 code for the emissions lookup. |
| `region` | Region/state name for the lookup; requires `alpha_2_code`. |
| `cpu_processes` | CPU utilization scope: `"current"` (default) or `"all"`. |
| `pue` | Power usage effectiveness multiplier applied to estimated energy; defaults to 1. |
| `encode_file` | Optional path for an additional encoded CSV. A string path must end in `.csv`; `True` uses an `encoded_` prefix on the results filename. This is the package’s encoding format, not a security feature. |
| `electricity_pricing` | Optional mapping of daily time intervals to electricity prices. Prices are stored without a currency designation; intervals must cover 24 hours in order without gaps or overlap. |
| `ignore_warnings` | Suppresses the package’s warnings when true; defaults to false. |
| `timezone` | Time zone for the scheduler. If false (the default), the local time zone is detected. |

The checked-in `eco2ai/data/config.txt` provides defaults for project name, experiment description, result filename, sampling period, and PUE. `set_params(...)` and `get_params()` are also exported for setting and reading those package defaults. Constructor arguments take precedence when supplied. The default sampling period in the `Tracker` constructor is 10 seconds; pass `None` to use the configured period.

When `electricity_pricing` is supplied, its interval values are multiplied by estimated energy and accumulated in the CSV `cost` column. Values should use a consistent, caller-chosen currency unit.

## Epoch-based tracking

For explicit epoch boundaries, use `start_training()`, `new_epoch(parameters_dict)`, and `stop_training()`:

```python
from eco2ai import Tracker

tracker = Tracker(file_name="training.csv", alpha_2_code="US")
tracker.start_training(start_epoch=1)

for epoch in range(3):
    # Run one epoch of training here.
    tracker.new_epoch({"learning_rate": 0.001})

tracker.stop_training()
```

`new_epoch()` writes a row for the elapsed epoch and advances the epoch number. As a result, call it at each boundary you want recorded. `stop_training()` ends this tracking mode; it does not write another row for work since the last `new_epoch()` call.

## Other exported helpers

- `available_devices()` prints visible CPU and GPU device information.
- `summary(filename, write_to_file=False)` reads a results CSV and returns a pandas DataFrame with totals per project and a total across projects. Set `write_to_file` to a path to save the summary as CSV.
- `set_params(...)` and `get_params()` set and retrieve configured tracker defaults.
- `CPU`, `GPU`, `RAM`, `all_available_cpu()`, and `all_available_gpu()` are also exported; the device classes are used internally by `Tracker`.

## Examples

The repository includes Jupyter notebooks demonstrating tracking during MNIST workflows:

- [PyTorch tutorial](examples/Eco2AI%20tutorial%20torch.ipynb)
- [TensorFlow tutorial](examples/Eco2AI%20tutorial%20tensorflow.ipynb)

## License

This project is distributed under the [Apache License, Version 2.0](LICENSE).
