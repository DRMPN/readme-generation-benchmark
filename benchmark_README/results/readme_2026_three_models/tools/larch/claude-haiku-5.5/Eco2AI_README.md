# Eco2AI

<p align="center">
  <img src="eco2ai_logo.jpg" alt="Eco2AI logo" width="250"/>
</p>

<p align="center">
  <em>Track energy consumption and CO₂ emissions of your machine learning experiments.</em>
</p>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration Reference](#configuration-reference)
- [Output Format](#output-format)
- [Carbon Intensity Data](#carbon-intensity-data)
- [Hardware Detection](#hardware-detection)
- [Tutorials](#tutorials)
- [Project Structure](#project-structure)
- [Development](#development)
- [Limitations and Accuracy](#limitations-and-accuracy)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Citation](#citation)

---

## Overview

**Eco2AI** is a lightweight Python library for estimating the energy consumption and carbon dioxide (CO₂) emissions produced by machine learning training and inference workloads. It runs alongside your code, periodically samples the power draw of your hardware (CPU, GPU, and RAM), converts the consumed energy into CO₂-equivalent emissions using the carbon intensity of your electricity grid, and logs the results to a file.

The library is framework-agnostic and has been demonstrated with both **PyTorch** and **TensorFlow**. Tutorials for both frameworks are included in this repository.

Eco2AI is developed by the [AIRI](https://airi.net/) (Artificial Intelligence Research Institute) team and is intended to help researchers and engineers make the environmental impact of AI visible and measurable.

---

## Features

- **Multi-component energy tracking**: measures CPU, GPU, and RAM power consumption.
- **Carbon emission estimation**: converts energy use to CO₂ using country- and region-specific carbon intensity values.
- **Regional configuration**: specify a country (and optionally a national subdivision) to use the appropriate grid carbon intensity.
- **Automatic hardware detection**: identifies the CPU and GPU models in use, with a lookup table for CPU specifications.
- **Periodic logging**: writes measurements to a CSV file at a configurable interval, so partial results survive interruptions.
- **Experiment labeling**: tag each run with a project name and description for easy comparison.
- **Framework-agnostic**: works with any Python code that runs on CPU or NVIDIA GPU, including PyTorch and TensorFlow.
- **Minimal overhead**: sampling runs in the background and has a small footprint on training performance.

---

## How It Works

Eco2AI follows a simple pipeline:

1. **Start tracking**: the tracker records the start time and detects the available hardware.
2. **Sample power**: at each measurement interval, the tracker reads:
   - CPU power, estimated from the processor model's thermal design power (TDP) and its utilization (see `cpu_names.csv` and `tools_cpu.py`).
   - GPU power, read from NVIDIA drivers via NVML (see `tools_gpu.py`).
   - RAM power, estimated from the installed memory and usage (see `tools_ram.py`).
3. **Integrate energy**: power samples are integrated over time to obtain energy in kilowatt-hours (kWh).
4. **Convert to emissions**: energy is multiplied by the carbon intensity of the configured region (see `carbon_index.csv`) to obtain CO₂ emissions in kilograms.
5. **Log results**: the cumulative values, along with metadata, are written to a CSV file.

---

## Installation

### From PyPI

```bash
pip install eco2ai
```

### From source

This repository uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
git clone https://github.com/sb-ai-lab/Eco2AI.git
cd Eco2AI
poetry install
```

Or, using `pip` directly with the packaging metadata in `setup.py`:

```bash
git clone https://github.com/sb-ai-lab/Eco2AI.git
cd Eco2AI
pip install .
```

### Requirements

- Python 3.7 or newer (check `pyproject.toml` for the exact supported range).
- `psutil` for CPU and RAM utilization.
- `pynvml` (or the NVIDIA driver's NVML library) for GPU monitoring. This is only needed if you want GPU tracking.
- `pandas` and related standard scientific packages for data handling.

Optional, for running the tutorials:

- `torch` (PyTorch) for the PyTorch tutorial.
- `tensorflow` for the TensorFlow tutorial.
- `jupyter` to open the notebooks.

---

## Quick Start

The basic workflow is: create a tracker, start it, run your workload, and stop it.

```python
import eco2ai

# Create a tracker
tracker = eco2ai.Tracker(
    project_name="ResNet18-CIFAR10",
    experiment_description="Training ResNet-18 on CIFAR-10 for 20 epochs",
    file_name="emissions.csv",
    region="Russia",
)

# Start tracking
tracker.start()

# ... your training or inference code ...
train_model()

# Stop tracking and write the final results
tracker.stop()
```

After the run, `emissions.csv` contains one row summarizing the energy use and emissions of the experiment.

### Example with PyTorch

```python
import eco2ai
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

tracker = eco2ai.Tracker(
    project_name="pytorch-demo",
    experiment_description="Simple MLP training",
    file_name="pytorch_emissions.csv",
    region="Germany",
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = nn.Sequential(nn.Linear(784, 256), nn.ReLU(), nn.Linear(256, 10)).to(device)
optimizer = torch.optim.Adam(model.parameters())
loss_fn = nn.CrossEntropyLoss()

tracker.start()
for epoch in range(5):
    for x, y in train_loader:  # your DataLoader
        x, y = x.view(x.size(0), -1).to(device), y.to(device)
        optimizer.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        optimizer.step()
tracker.stop()
```

For a complete example, open `Eco2AI tutorial torch.ipynb`.

### Example with TensorFlow

```python
import eco2ai
import tensorflow as tf

tracker = eco2ai.Tracker(
    project_name="tf-demo",
    experiment_description="Training a CNN on MNIST",
    file_name="tf_emissions.csv",
    region="France",
)

(x_train, y_train), _ = tf.keras.datasets.mnist.load_data()
x_train = x_train / 255.0

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(10),
])
model.compile(optimizer="adam",
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))

tracker.start()
model.fit(x_train, y_train, epochs=5, batch_size=64)
tracker.stop()
```

For a complete example, open `Eco2AI tutorial tensorflow.ipynb`.

---

## Configuration Reference

The `Tracker` class accepts the following parameters. Names and defaults may vary slightly between versions, so consult the docstrings in `emission_track.py` for the authoritative list.

| Parameter | Type | Description |
|---|---|---|
| `project_name` | `str` | Name of the project. Used to group and label runs in the output file. |
| `experiment_description` | `str` | Free-text description of the experiment. |
| `file_name` | `str` | Path to the CSV file where results are written. Created if it does not exist. |
| `region` | `str` | Country or region name used to look up carbon intensity (e.g., `"Russia"`, `"Germany"`). Must match an entry in `carbon_index.csv`. |
| `alpha_2_code` | `str` | Optional ISO 3166-1 alpha-2 country code (e.g., `"RU"`). Used as an alternative to `region`. |
| `national_subdivision_code` | `str` | Optional subdivision code (e.g., a US state code) for more precise carbon intensity. |
| `measure_power_secs` | `float` | Interval in seconds between power measurements. Default is typically `10`. |
| `ignore_warnings` | `bool` | If `True`, suppresses warnings about missing hardware or incomplete data. |

### Methods

| Method | Description |
|---|---|
| `start()` | Begins background monitoring of hardware power. |
| `stop()` | Stops monitoring and writes the final summary to the output file. |
| `flush()` | Writes the current accumulated values to the output file without stopping the tracker. Useful for long-running jobs. |

---

## Output Format

Each run appends a row to the output CSV with the following fields (names may vary by version):

| Column | Unit | Description |
|---|---|---|
| `timestamp` | ISO datetime | Time the record was written. |
| `project_name` | — | Project label supplied by the user. |
| `experiment_description` | — | Experiment description supplied by the user. |
| `duration(s)` | seconds | Total tracked duration. |
| `power_consumption(kWh)` | kWh | Total energy consumed by all tracked components. |
| `CO2_emissions(kg)` | kg | Estimated CO₂-equivalent emissions. |
| `CPU_energy(kWh)` | kWh | Energy attributed to the CPU. |
| `GPU_energy(kWh)` | kWh | Energy attributed to the GPU(s). |
| `RAM_energy(kWh)` | kWh | Energy attributed to system memory. |
| `CPU_name` | — | Detected processor model. |
| `GPU_name` | — | Detected GPU model(s). |
| `region` | — | Region used for carbon intensity lookup. |

Because each run is appended, the CSV can be loaded with pandas for comparison across experiments:

```python
import pandas as pd

df = pd.read_csv("emissions.csv")
print(df.groupby("project_name")["CO2_emissions(kg)"].sum())
```

---

## Carbon Intensity Data

Carbon intensity describes how much CO₂ is emitted per kilowatt-hour of electricity produced, and it varies widely by country and by energy mix. Eco2AI uses the values stored in `carbon_index.csv`, which map countries (and in some cases subdivisions) to average grid carbon intensity in kg CO₂ per kWh.

To check whether your region is supported, open `carbon_index.csv` or query it with pandas:

```python
import pandas as pd
df = pd.read_csv("carbon_index.csv")
print(df.head())
```

If your region is missing, you can add a row to the file, or use the closest available value. Because intensity values change over time as grids evolve, periodically reviewing this file is recommended for accurate reporting.

---

## Hardware Detection

### CPU

`tools_cpu.py` identifies the processor model and uses `cpu_names.csv` to look up its thermal design power (TDP) and related specifications. CPU power is estimated from this TDP and the measured utilization. If your processor is not in `cpu_names.csv`, the tracker will fall back to a default estimate or warn you. You can add your processor to the CSV to improve accuracy.

### GPU

`tools_gpu.py` queries NVIDIA GPUs through NVML to obtain the device name and real-time power draw. Multiple GPUs are supported and their energy is summed. GPU monitoring requires an NVIDIA driver and the NVML library; without them, GPU energy is reported as zero or omitted.

### RAM

`tools_ram.py` reads total installed memory and current usage to estimate memory power consumption. This is an approximation, since precise DRAM power measurement typically requires hardware-level instrumentation.

### Shared utilities

`utils.py` contains helper functions used across the modules, such as unit conversions, time handling, and CSV writing.

---

## Tutorials

Two Jupyter notebooks demonstrate end-to-end usage:

- **`Eco2AI tutorial torch.ipynb`**: tracking a PyTorch model training loop.
- **`Eco2AI tutorial tensorflow.ipynb`**: tracking a TensorFlow/Keras model training loop.

To run them:

```bash
pip install jupyter torch tensorflow
jupyter notebook "Eco2AI tutorial torch.ipynb"
```

---

## Project Structure

```
Eco2AI-pc96hqry/
├── eco2ai/                       # Main package
│   ├── __init__.py               # Public API exports
│   ├── emission_track.py         # Tracker class: start/stop/flush and logging
│   ├── tools_cpu.py              # CPU model detection and power estimation
│   ├── tools_gpu.py              # NVIDIA GPU monitoring via NVML
│   ├── tools_ram.py              # RAM usage and power estimation
│   ├── utils.py                  # Shared helper functions
│   ├── MLTracker.py              # Higher-level tracking utilities for ML workflows
│   ├── cpu_names.csv             # CPU models with TDP and specifications
│   ├── carbon_index.csv          # Carbon intensity by country/region
│   └── config.txt                # Package configuration
├── Eco2AI tutorial torch.ipynb   # PyTorch tutorial
├── Eco2AI tutorial tensorflow.ipynb  # TensorFlow tutorial
├── setup.py                      # Legacy packaging entry point
├── pyproject.toml                # Build system and project metadata
├── poetry.lock                   # Locked dependency versions
├── _config.yml                   # Documentation site configuration
├── LICENSE                       # License text
├── eco2ai_logo.jpg               # Project logo
├── eco2ai_logo_cut.jpg           # Cropped logo variant
├── AIRI - Full logo (2).png      # AIRI institute logo
└── photo_2022-06-14_13-02-37.jpg # Project photo
```

---

## Development

### Setting up a development environment

```bash
git clone https://github.com/sb-ai-lab/Eco2AI.git
cd Eco2AI
poetry install
poetry shell
```

### Running in editable mode with pip

```bash
pip install -e .
```

### Adding hardware support

- **New CPU**: add a row to `cpu_names.csv` with the model name and TDP.
- **New carbon intensity value**: add a row to `carbon_index.csv`.
- **New hardware backend** (e.g., AMD GPUs, Apple Silicon): implement a new module analogous to `tools_gpu.py` and integrate it in `emission_track.py`.

---

## Limitations and Accuracy

Eco2AI produces **estimates**, not certified measurements. Users should keep the following in mind:

- **CPU and RAM power are modeled**, not directly measured, so they depend on the accuracy of TDP tables and utilization-based approximations.
- **GPU power is read from NVIDIA sensors**, which are generally reliable but may not capture all board-level consumption. AMD and Intel GPUs are not covered by the GPU module.
- **Carbon intensity is an average**. Real-time grid intensity varies by hour and season, and a single annual average may not reflect your actual electricity source.
- **Cooling, networking, storage, and data-center overhead** (often captured by PUE, or Power Usage Effectiveness) are not included unless you apply a multiplier yourself.
- **Embodied emissions** from manufacturing hardware are not included.
- **Measurement overhead**: background sampling consumes a small amount of CPU. For very short runs, the estimate may be dominated by startup effects.

For regulatory or publication-grade reporting, cross-check results against dedicated tools or metered data.

---

## Contributing

Contributions are welcome. A typical workflow is:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-change`.
3. Make your changes and add tests where appropriate.
4. Commit and push: `git push origin feature/my-change`.
5. Open a pull request describing the change and its motivation.

Please keep pull requests focused, follow the existing code style, and document any new configuration options.

### Reporting issues

When filing a bug report, please include:

- Your Python version and operating system.
- Your CPU and GPU models (as reported by the tracker).
- The Eco2AI version (`pip show eco2ai`).
- A minimal code snippet that reproduces the problem.
- The contents of the output CSV, if relevant.

---

## License

This project is distributed under the terms of the license in the [LICENSE](LICENSE) file.

---

## Acknowledgements

- **AIRI** (Artificial Intelligence Research Institute) and the **SB AI Lab** for developing and maintaining Eco2AI. See the AIRI logo in `AIRI - Full logo (2).png`.
- The authors and contributors who built the hardware lookup tables and carbon intensity datasets used by the library.
- The open-source community behind `psutil`, `pynvml`, PyTorch, and TensorFlow.

---

## Citation

If you use Eco2AI in academic work, please cite the project. A suggested BibTeX entry is:

```bibtex
@software{eco2ai,
  title        = {Eco2AI: Carbon emissions tracking of machine learning models},
  author       = {{AIRI and SB AI Lab}},
  year         = {2022},
  url          = {https://github.com/sb-ai-lab/Eco2AI},
  note         = {Python library for estimating energy use and CO2 emissions of ML experiments}
}
```

Please update the author list and year to match the version you use.

---

<p align="center">
  <img src="AIRI - Full logo (2).png" alt="AIRI logo" width="200"/>
</p>
