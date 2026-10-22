# Eco2AI

Eco2AI estimates the energy use and carbon emissions associated with running Python workloads, including machine-learning training. It monitors the machine while your code runs and records an experiment summary to a file, so you can compare the estimated impact of different runs.

> **Note:** Eco2AI reports estimates, not direct measurements of electricity use or emissions. Results depend on the hardware and system information available to the library, as well as the carbon-intensity data used for the calculation.

## Features

- Track energy consumption and estimated CO₂ emissions for a Python workload.
- Record experiment names and descriptions alongside measurements.
- Monitor supported CPU and GPU resources.
- Export experiment results for later analysis.
- Explore example integrations in the included PyTorch and TensorFlow notebooks.

## Installation

Install the package from PyPI:

```bash
pip install eco2ai
```

To install from a local checkout of this repository:

```bash
pip install .
```

This project also includes Poetry configuration. If Poetry is installed, dependencies can be installed from the project configuration with:

```bash
poetry install
```

## Quick start

Create a tracker, start it before the workload, and stop it when the workload finishes:

```python
from eco2ai import Tracker

tracker = Tracker(
    project_name="example-project",
    experiment_description="Example training run",
    file_name="emissions.csv",
)

tracker.start()

try:
    # Run the workload you want to measure.
    train_model()
finally:
    # Stop the tracker even if the workload raises an exception.
    tracker.stop()
```

Replace `train_model()` with your own code. The tracker should be started before the work begins and stopped afterward. The output file is selected with `file_name`; use a path if you want to save it somewhere other than the current working directory.

A minimal script might look like this:

```python
from eco2ai import Tracker

tracker = Tracker(
    project_name="my-project",
    experiment_description="Baseline experiment",
    file_name="emissions.csv",
)

tracker.start()
try:
    run_experiment()
finally:
    tracker.stop()
```

## Using Eco2AI with machine-learning frameworks

The repository includes example notebooks for PyTorch and TensorFlow:

- `Eco2AI tutorial torch.ipynb`
- `Eco2AI tutorial tensorflow.ipynb`

They demonstrate how to apply tracking to framework-based workloads. Open the relevant notebook in Jupyter and adapt its example to your model and training loop.

For reliable comparisons, keep the workload and measurement setup consistent between runs. Record the same kind of experiment metadata, and avoid comparing results collected on substantially different hardware or under different system conditions without accounting for those differences.

## Output and interpreting results

Eco2AI writes a record for the tracked run to the output file you configure. The recorded information is intended to describe the experiment and its resource use, including the measured run and estimated emissions. The exact columns and units depend on the package version; consult the generated file and the implementation in `emission_track.py` and `MLTracker.py` when building downstream analysis around its schema.

For meaningful reporting:

- Treat emissions as estimates, not audited carbon accounting.
- Check the output headers and units before aggregating results.
- Include relevant hardware and experiment details when sharing comparisons.
- Preserve the raw output file so results can be reviewed or processed later.

## Configuration and supporting data

The repository includes supporting files used by the project:

- `config.txt` — configuration data.
- `carbon_index.csv` — carbon-intensity data used in emissions calculations.
- `cpu_names.csv` — CPU reference data.
- `tools_cpu.py`, `tools_gpu.py`, and `tools_ram.py` — resource-related utilities.

If you modify configuration or reference data, keep a copy of the original values and document the changes. Different carbon-intensity assumptions can produce different emissions estimates even when the workload and energy use are unchanged.

## Hardware and measurement considerations

- **CPU and memory:** Measurements depend on what the host operating system exposes to the process.
- **GPU:** GPU detection and monitoring depend on the GPU, installed drivers, and the monitoring support available in the environment. Check that the target device is visible to the system before relying on GPU measurements.
- **Shared machines:** Other processes running at the same time can affect resource use and make a run harder to compare.
- **Virtualized environments:** Containers, virtual machines, and managed notebook services may expose incomplete or estimated hardware information.
- **Measurement duration:** Very short workloads can be difficult to characterize consistently. For comparisons, use comparable runs and measurement conditions.

## Repository layout

| File or directory | Purpose |
|---|---|
| `setup.py`, `pyproject.toml`, `poetry.lock` | Package metadata and dependency management |
| `__init__.py` | Package initialization and public imports |
| `emission_track.py`, `MLTracker.py` | Tracking and emissions-related implementation |
| `utils.py` | Shared utility code |
| `tools_cpu.py`, `tools_gpu.py`, `tools_ram.py` | CPU, GPU, and memory-related utilities |
| `config.txt` | Configuration data |
| `carbon_index.csv` | Carbon-intensity reference data |
| `cpu_names.csv` | CPU reference data |
| `Eco2AI tutorial torch.ipynb` | PyTorch example notebook |
| `Eco2AI tutorial tensorflow.ipynb` | TensorFlow example notebook |
| `LICENSE` | Project license |
| Image files | Project artwork and documentation assets |

## Troubleshooting

### The output file is missing

Check that the tracker reached `stop()` and that the process can write to the directory containing `file_name`. Using a full path can make the output location easier to identify.

### GPU information is missing

Confirm that the machine has a supported GPU and that the relevant drivers and device-monitoring support are installed and available to the Python process. GPU visibility can differ between a host system, a container, and a managed notebook environment.

### Results differ between runs

Differences can result from changes in hardware, workload duration, background processes, or carbon-intensity assumptions. Keep these conditions as consistent as possible and treat small differences cautiously.

## License

See [`LICENSE`](LICENSE) for the terms under which this project is distributed.
