# Eco2AI

Eco2AI is a Python library for tracking CO₂ emissions of your machine learning training runs. It estimates the carbon footprint produced by your GPU/CPU devices during model training and writes an emission report so you can understand — and reduce — the environmental impact of your experiments.

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [PyTorch](#pytorch)
  - [TensorFlow](#tensorflow)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🔎 Overview

Training large ML models consumes significant amounts of electricity, which in turn produces CO₂ emissions. Eco2AI helps researchers and engineers:

- **Measure** the energy consumption of CPU and GPU devices during training sessions
- **Estimate** the equivalent CO₂ emissions based on your regional power grid's carbon index
- **Log** all tracked sessions into a local emissions report (`emission_report.csv`)

Eco2AI works as a lightweight tracker that wraps around your existing training loop — just a couple of lines of code, no changes to your model required.

## 📦 Installation

Install from source using `setup.py`:

```bash
git clone https://github.com/sustainable-machines-learning/Eco2AI-yt25n9f1.git
cd Eco2AI-yt25n9f1
python setup.py install
```

Or with Poetry (a `pyproject.toml` and `poetry.lock` are provided):

```bash
poetry install
```

## 🚀 Quick Start

```python
import eco2ai

# Create a tracker
tracker = eco2ai.Tracker(
    project_name="My Project",
    experiment_name="baseline_model",
    file_name="emission_report.csv"
)

# Start tracking before training
tracker.start()

# ... your training code ...

# Stop tracking after training
tracker.stop()
```

That's it! After `tracker.stop()`, a record with your energy consumption and CO₂ emissions will be appended to the report file.

## 💻 Usage Examples

### PyTorch

```python
import eco2ai
import torch

tracker = eco2ai.Tracker(
    project_name="Eco2AI_Tutorial",
    experiment_name="torch_mnist"
)
tracker.start()

model = ...  # your PyTorch model
# training loop
for epoch in range(epochs):
    ...

tracker.stop()
```

A complete walkthrough is available in the repository: **`Eco2AI tutorial torch.ipynb`**.

### TensorFlow

```python
import eco2ai
import tensorflow as tf

tracker = eco2ai.Tracker(
    project_name="Eco2AI_Tutorial",
    experiment_name="tf_mnist"
)
tracker.start()

model = ...  # your TensorFlow model
model.fit(x_train, y_train, epochs=epochs)

tracker.stop()
```

A complete walkthrough is available in the repository: **`Eco2AI tutorial tensorflow.ipynb`**.

## ⚙️ Configuration

Tracker behavior can be customized via the `config.txt` file or through `Tracker` parameters, for example:

- **project_name / experiment_name** — labels used in the report
- **file_name** — path to the output CSV report
- **region / country** — used to look up the carbon intensity of your local electricity grid (from `carbon_index.csv`)
- **measure_period** — sampling interval (in seconds) for power measurements

Device power draw is measured with the bundled utility modules:

| File | Purpose |
|---|---|
| `tools_gpu.py` | GPU power/usage monitoring (NVIDIA GPUs) |
| `tools_cpu.py` | CPU power/usage monitoring |
| `tools_ram.py` | RAM usage monitoring |

CPU model names are resolved via `cpu_names.csv`, and CO₂ conversion uses regional grid carbon intensity data from `carbon_index.csv`.

## 🧠 How It Works

1. **Power measurement** — during training, Eco2AI periodically samples GPU (and CPU/RAM) utilization and power draw.
2. **Energy computation** — sampled power values are integrated over time to estimate total energy consumed (kWh).
3. **Emission estimation** — the consumed energy is multiplied by the carbon index (gCO₂/kWh) of your regional electricity grid to produce the CO₂ emission estimate.
4. **Reporting** — results are written to a CSV report containing timestamps, device info, energy consumption, and emissions per experiment.

## 📁 Project Structure

```
Eco2AI-yt25n9f1/
├── __init__.py                 # Package entry point
├── emission_track.py           # Core emission tracking logic
├── MLTracker.py                # High-level Tracker interface
├── utils.py                    # Helper utilities
├── tools_gpu.py                # GPU monitoring tools
├── tools_cpu.py                # CPU monitoring tools
├── tools_ram.py                # RAM monitoring tools
├── cpu_names.csv               # CPU model reference data
├── carbon_index.csv            # Regional grid carbon intensity data
├── config.txt                  # Default configuration
├── setup.py / pyproject.toml   # Packaging metadata
├── Eco2AI tutorial torch.ipynb # PyTorch example notebook
└── Eco2AI tutorial tensorflow.ipynb  # TensorFlow example notebook
```

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for bug fixes, new features, or improved documentation.

## 📄 License

This project is distributed under the terms of the `LICENSE` file included in this repository.
