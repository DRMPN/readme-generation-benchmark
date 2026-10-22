# Eco2AI

![Eco2AI logo](images/eco2ai_logo.jpg)

Eco2AI is a Python library for estimating the energy consumption and CO2 emissions of machine learning code running on CPU, NVIDIA GPU, and RAM. It records the results to a CSV file, and can also encode them and compute electricity cost.

- Package name: `eco2ai`
- Version: 0.3.12
- Development status: Alpha
- License: Apache License 2.0 (see [LICENSE](LICENSE))
- Source: https://github.com/sb-ai-lab/Eco2AI

## Features

- Tracks CPU, GPU, and RAM power consumption over time, sampled at a configurable interval.
- Converts energy use (kWh) to CO2 emissions (kg) using a country- or region-specific emission intensity, or a value you provide.
- Supports three usage styles: explicit `start()`/`stop()`, epoch-based training tracking with `start_training()`/`new_epoch()`/`stop_training()`, and a `@track` function decorator.
- Writes results to a CSV file, one row per tracking session.
- Optionally computes electricity cost from a time-of-day price schedule.
- Optionally writes an encoded copy of the results to a second CSV file.
- Provides a `summary()` helper that aggregates a results CSV by project.

## Installation

```bash
pip install eco2ai
```

The package depends on the following libraries, which `pip` installs automatically:

- `APScheduler`
- `pynvml` (version 5.6.2 or later)
- `psutil`
- `py-cpuinfo`

The package also imports `numpy`, `pandas`, `requests`, `tzlocal`, and `setuptools` (for `pkg_resources`). These are declared in `pyproject.toml`.

No minimum Python version is pinned in the package metadata. The classifiers list Python 3.7, and the pandas constraints differ for Python 3.7 and 3.8+.

## Quick Start

```python
import eco2ai

tracker = eco2ai.Tracker(project_name="my_project", experiment_description="baseline model")
tracker.start()

# your CPU and GPU computations here

tracker.stop()
```

After `stop()`, the results are appended to `emission.csv` in the current directory (the default file name).

## Usage

### Tracking a block of code with `start()` and `stop()`

```python
import eco2ai

tracker = eco2ai.Tracker(
    project_name="mnist",
    experiment_description="convolutional model",
    file_name="emission.csv",
    measure_period=10,
    alpha_2_code="DE",
)

tracker.start()
# ... training or inference code ...
tracker.stop()

print(tracker.consumption())   # kWh measured so far
print(tracker.emission_level())  # kg CO2 per MWh used
```

Create the `Tracker` before any CPU or GPU work begins. The docstring recommends creating a new `Tracker` for each separate calculation.

### Tracking per-epoch training

```python
import eco2ai

tracker = eco2ai.Tracker(project_name="mnist", experiment_description="CNN training")
tracker.start_training(start_epoch=1)

for epoch in range(1, 4):
    # ... train for one epoch ...
    tracker.new_epoch({"epoch_accuracy": 0.97})

tracker.stop_training()
```

`new_epoch()` takes a dictionary of values to store alongside the epoch's row. Those values appear in the `epoch` column. `new_epoch()` must be called after `start_training()`; otherwise it raises `IncorrectMethodSequenceError`. Within training mode, results are written to the CSV when `new_epoch()` is called, not on a background timer.

### Tracking a function with the `@track` decorator

```python
from eco2ai import track

@track
def train_model():
    # ... training code ...
    pass

train_model()
```

The decorator creates a `Tracker` with default settings, starts it before the function runs, and stops it afterward, including when the function raises an exception.

## Tracker Parameters

`eco2ai.Tracker(...)` accepts the following arguments:

| Parameter | Default | Description |
|---|---|---|
| `project_name` | `None` (stored default) | Project name written to the results file. |
| `experiment_description` | `None` (stored default) | Free-text description, such as model type. |
| `file_name` | `None` (stored default, `"emission.csv"`) | Output CSV file name. Must end with `.csv`. |
| `measure_period` | `10` | Measurement interval in seconds. Must be positive. |
| `emission_level` | `None` | CO2 mass in kg produced per MWh of energy. If set, it is used instead of the value from the carbon index table. |
| `alpha_2_code` | `None` | ISO 3166-1 alpha-2 country code, such as `"US"` or `"DE"`. See [iban.com country codes](https://www.iban.com/country-codes). |
| `region` | `None` | Region, state, or district within the country. Requires `alpha_2_code`. |
| `cpu_processes` | `"current"` | `"current"` measures only the current Python process's CPU use. `"all"` measures total CPU use across all processes. |
| `pue` | `1` | Power usage effectiveness multiplier applied to total consumption. Useful for data-center calculations. |
| `encode_file` | `None` | If set, also writes an encoded copy of the results. See [Encoded output](#encoded-output). |
| `electricity_pricing` | `None` | Dictionary of time intervals to prices. See [Electricity pricing](#electricity-pricing). |
| `ignore_warnings` | `False` | If `True`, suppresses the library's warnings. |
| `timezone` | `False` | Timezone name to use instead of the automatically detected local timezone. |

Methods on a `Tracker` instance:

| Method | Description |
|---|---|
| `start()` | Starts background measurement. |
| `stop()` | Stops measurement and writes the final results. If called during training mode, it stops training. |
| `start_training(start_epoch=1)` | Starts training-mode tracking. `start_epoch` must be an `int`. |
| `new_epoch(parameters_dict)` | Records the current epoch's results and starts the next epoch. |
| `stop_training()` | Ends training-mode tracking. |
| `consumption()` | Returns the energy consumed in the current session, in kWh. |
| `price()` | Returns the electricity cost of the current session. |
| `emission_level()` | Returns the emission level in kg CO2 per MWh. |
| `measure_period()` | Returns the measurement interval in seconds. |
| `id()` | Returns the session's UUID. |

## How Emissions Are Calculated

- **CPU:** Power is estimated as the CPU's TDP multiplied by the measured CPU utilization, the number of CPU sockets, and the elapsed time. CPU utilization is read with `top` on Linux and macOS, and with `psutil` on Windows.
- **CPU TDP lookup:** The CPU model name is matched against `eco2ai/data/cpu_names.csv`. If no match is found, a constant of 100.1 W is used.
- **GPU:** On NVIDIA GPUs, the library reads per-device power draw through `pynvml` and integrates it over time. If no NVIDIA GPU is available, the GPU contributes 0 kWh and a warning is issued unless `ignore_warnings=True`.
- **RAM:** The memory used by the current Python process is converted to a power estimate using a fixed factor of 3/8 W per GB.
- **Total:** The sum of CPU, GPU, and RAM energy is multiplied by `pue`.
- **CO2:** Energy in kWh is multiplied by the emission level (kg/MWh) and divided by 1000.

The CPU, RAM, and TDP-based figures are estimates derived from the factors above, not direct hardware power readings. Only NVIDIA GPUs are measured directly.

### Emission levels

If you do not pass `emission_level`, the library looks up the emission intensity for your country (and region, if given) in `eco2ai/data/carbon_index.csv`, which lists values in kg/MWh.

- If `alpha_2_code` is not provided, the country is detected by requesting `https://ipinfo.io/`. This requires internet access. Detection can be wrong when a VPN is in use, and the library warns about this. Providing `alpha_2_code` avoids the lookup.
- If the country is not in the table, the worldwide value is used.
- If the country has several entries and no `region` is given, the whole-country value is used.

## Output Files

### Results CSV

Each session writes one row to the CSV file named by `file_name` (default `emission.csv`). If the file already exists, a row is appended or, for the same session, updated. The columns are:

| Column | Description |
|---|---|
| `id` | UUID of the tracking session. |
| `project_name` | Project name. |
| `experiment_description` | Experiment description. |
| `epoch` | `"N/A"` outside training mode. In training mode, the epoch number and the values passed to `new_epoch()`. |
| `start_time` | Session start time, `YYYY-MM-DD HH:MM:SS`. |
| `duration(s)` | Session duration in seconds. |
| `power_consumption(kWh)` | Energy consumed in kWh. |
| `CO2_emissions(kg)` | Estimated CO2 emissions in kg. |
| `CPU_name` | CPU model, number of CPU devices, and TDP. |
| `GPU_name` | GPU model and number of GPU devices. Empty if no NVIDIA GPU is detected. |
| `OS` | Operating system (`Linux`, `Windows`, or `MacOS`). |
| `region/country` | Country code and, if available, region. |
| `cost` | Electricity cost. `0` when no pricing is set. |

The file is only written when no other Python or Jupyter process has it open. If it is open, the tracker waits and retries every 0.5 seconds.

### Encoded output

If `encode_file` is set to any truthy value, each row is also written to a second CSV with values obfuscated by `eco2ai.utils.encode`. In the current code, the encoded file name is always `"encoded_" + file_name`, regardless of the string passed to `encode_file`. For example, with the default file name, the encoded file is `encoded_emission.csv`.

### Electricity pricing

Pass `electricity_pricing` as a dictionary whose keys are time intervals in the form `"hh:mm-hh:mm"` and whose values are prices per kWh, with no currency symbol:

```python
pricing = {
    "8:30-19:00": 0.30,
    "19:00-6:00": 0.12,
    "6:00-8:30": 0.30,
}

tracker = eco2ai.Tracker(electricity_pricing=pricing)
```

The intervals must cover exactly 24 hours, must not overlap, and must be in chronological order. The library validates these rules and raises `IncorrectPricingDict` on violation. The cost is computed from the price active at each measurement.

## Summarizing Results

```python
import eco2ai

summary_df = eco2ai.summary("emission.csv")
print(summary_df)
```

`summary()` returns a pandas DataFrame with one row per project and a final `All the projects` row. The columns are the project name, total duration (s), total energy (kWh), total CO2 (kg), and total electricity cost. Pass a file name as `write_to_file` to also save the table as CSV.

## Device Discovery and Configuration Helpers

```python
import eco2ai

eco2ai.available_devices()    # prints detected CPU and GPU devices
eco2ai.get_params()           # returns the stored default parameters as a dict
eco2ai.set_params(project_name="p", experiment_description="d", file_name="e.csv")
```

`available_devices()` calls `all_available_cpu()` and `all_available_gpu()` and prints the results.

Defaults are stored in `eco2ai/data/config.txt` inside the installed package. Each `Tracker(...)` call writes its parameters to that file, so values you set on one `Tracker` are used as defaults for later ones that omit them.

## Lower-level Classes

The following classes are exported by `eco2ai`. They are used internally by `Tracker`, and the library documentation says they are not intended for standalone use:

- `CPU`: CPU name, TDP, socket count, and utilization-based consumption.
- `GPU`: NVIDIA GPU power, memory, temperature, power limit, name, and device count, using `pynvml`.
- `RAM`: RAM consumption estimate for the current process.

## Examples

The `examples/` directory contains two Jupyter notebooks that train a small CNN on MNIST and track it with eco2ai:

- [`examples/Eco2AI tutorial torch.ipynb`](examples/Eco2AI%20tutorial%20torch.ipynb), using PyTorch
- [`examples/Eco2AI tutorial tensorflow.ipynb`](examples/Eco2AI%20tutorial%20tensorflow.ipynb), using TensorFlow/Keras

The notebooks also require `numpy`, `pandas`, `matplotlib`, and `pillow`, plus `torch`/`torchvision` or `tensorflow`.

## Limitations

- GPU measurement only covers NVIDIA GPUs that `pynvml` can access. Other GPUs are not measured.
- CPU and RAM consumption are estimates based on TDP and utilization, not measured power.
- Unknown CPU models fall back to a constant 100.1 W TDP.
- The default country lookup needs internet access and can be inaccurate behind a VPN.
- On Linux, the socket count comes from `lscpu`, which is part of `util-linux`. If it is missing, the count defaults to 1.
- On Windows, the socket count is parsed from the output of `systeminfo`. If parsing fails, the count defaults to 1.
- On macOS, the socket count is always 1.
- Training-mode results are written only when `new_epoch()` is called.
- The `encode_file` file name cannot be customized (see [Encoded output](#encoded-output)).

## Project Structure

```
eco2ai/
├── __init__.py          # Public API exports
├── emission_track.py    # Tracker class and track decorator
├── utils.py             # Helpers: carbon index, pricing, encoding, summary
├── tools/
│   ├── tools_cpu.py     # CPU class, TDP lookup, CPU utilization
│   ├── tools_gpu.py     # GPU class, NVIDIA power via pynvml
│   └── tools_ram.py     # RAM class
└── data/
    ├── carbon_index.csv # Emission intensity by country and region
    ├── cpu_names.csv    # CPU models and TDP values
    └── config.txt       # Stored default parameters
examples/                # Jupyter tutorials (PyTorch, TensorFlow)
images/                  # Logos
```

## Contributing

Bug reports and feature requests are welcome. Issue templates are provided in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/).

## License

Eco2AI is released under the [Apache License 2.0](LICENSE).

## Authors

Vladimir Lazarev, Nikita Zakharenko, Alexey Korovin, Semyon Budyonny, Leonid Zhukov, and the AI Lab, as listed in `pyproject.toml`.
