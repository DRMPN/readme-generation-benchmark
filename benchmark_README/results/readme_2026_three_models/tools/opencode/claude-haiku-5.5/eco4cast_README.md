# eco4cast

![eco4cast](images/eco4cast_color.jpg)

eco4cast is a Python package for training PyTorch models in the time windows when the electricity grid is forecast to be least carbon-intensive. It forecasts grid carbon intensity for supported regions, selects training intervals whose forecast emissions are below a threshold, and pauses and resumes training across those intervals. When the best region changes, it can also move a Google Cloud virtual machine to a zone in that region.

The package is described in `pyproject.toml` as "designed to reduce CO2 emissions while training neural networks using Google Cloud." It can also be used on a local machine, without Google Cloud.

## Contents

- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Local machine](#local-machine)
  - [Google Cloud](#google-cloud)
- [Configuration](#configuration)
- [Supported zones](#supported-zones)
- [Repository layout](#repository-layout)
- [Limitations](#limitations)
- [License](#license)
- [Authors](#authors)

## How it works

1. **Forecasting.** `CO2Predictor` (in `eco4cast/master_machine/interval_predictor.py`) loads a bundled PyTorch checkpoint (`eco4cast/master_machine/data_files/co2_model.ckpt`). For each supported zone it:
   - fetches the last 24 hours of carbon intensity from the [Electricity Maps](https://www.electricitymaps.com/) API (requires an API key), and
   - fetches hourly weather for a set of points in that zone from the [Open-Meteo](https://open-meteo.com/) forecast API.

   The model outputs a 24-hour carbon-intensity forecast for each zone.

2. **Interval selection.** `IntervalGenerator` uses the forecast to find hours in which a zone's moving-average intensity is below `max_emission_value`. It assigns each hour to a zone, preferring to stay in the current zone unless another zone is at least `co2_delta_to_move` lower. The output is a list of `(zone, [(start, end, mean_intensity), ...])` entries in UTC.

3. **Training.** `IntervalTrainer` (in `eco4cast/virtual_machine/smart_scheduler_concept.py`) is built on [Lightning Fabric](https://lightning.ai/docs/fabric/stable/). It schedules each training interval with APScheduler, stops training when the interval ends, and saves its state to `fabric_checkpoint.ckpt`. The next interval resumes from that state, including the sampler position and the current epoch and batch. It tracks emissions with `eco2ai` and writes them to `emission.csv`.

4. **Reporting.** When training finishes, eco4cast prints the total CO2 emissions in grams and compares them with the average forecast intensity across the zones.

### Google Cloud mode

`Controller` (in `eco4cast/master_machine/master_machine_controller.py`) runs on a "master machine" and coordinates a training VM:

- It connects to the training VM over SSH with `paramiko` and starts `vm_main.py` with the interval times and CO2 values as arguments. Training resumes from saved state after each interval.
- When the next interval's zone differs from the VM's current zone, it calls `google_cloud_move_vm`. That function snapshots the boot disk, deletes the instance and disk, creates a new disk from the snapshot in the target zone, and creates a new instance with the same machine type. The controller then uses the new instance's external IP.
- After an interval, if more than `intervals_prediction_period` seconds have passed since the last forecast, it re-runs the forecast and regenerates the schedule. The examples use 3600.
- At the end, it copies `emission.csv` from the VM over SFTP and prints the emissions summary. `stop_training()` stops the instance.

### Local mode

`IntervalTrainer.train_using_predictor(co2_predictor, interval_generator)` forecasts, generates intervals, and trains during those intervals on your own machine. It regenerates the schedule when the current interval list is used up, or when `minimum_prediction_period` seconds (default 3600) have passed since the first forecast. If no intervals are found, it stops. Otherwise it prints the emissions summary when training ends.

## Requirements

From `pyproject.toml`:

- Python `^3.9`
- `torch ^2.0.1`
- `lightning ^2.0.2`
- `apscheduler ^3.10.1`
- `eco2ai ^0.3.9`
- `paramiko ^3.2.0`
- `numpy >=1.23.5`
- `pandas >=1.4.3`
- `scikit-learn ^1.2.2`
- `google-cloud-compute ^1.11.0`

The code also imports `requests` and `tqdm`, which are not listed in `pyproject.toml`. The example notebooks and scripts import `torchvision` (for MNIST), which is installed separately.

To use the package you also need:

- An **Electricity Maps API key**. The notebooks say the free tier is for non-commercial use only.
- For Google Cloud mode: a Google Cloud project, a Compute Engine VM running in a supported zone with a Python virtual environment and `vm_main.py`, and an `application_default_credentials.json` file for the master machine.

## Installation

From PyPI:

```bash
pip install eco4cast
```

From a local checkout (the project uses `poetry-core` as its build backend):

```bash
pip install .
```

The repository also contains a built distribution for version 0.0.8 in `dist/`.

## Usage

### Local machine

The local quick-start notebook is at `examples/eco4cast_local_demo/local_quick_start_guide.ipynb`. The core steps are:

```python
from eco4cast.master_machine.interval_predictor import CO2Predictor, IntervalGenerator
from eco4cast.virtual_machine.smart_scheduler_concept import IntervalTrainer

electricity_maps_api_key = "YOUR_API_KEY"
your_zone = "BE"  # choose a zone from the supported list

co2_predictor = CO2Predictor(electricity_maps_api_key, include_zones=[your_zone])
interval_generator = IntervalGenerator(
    include_zones=[your_zone],
    max_emission_value=115,
    co2_delta_to_move=30,
    min_interval_size=1,
    max_window_size=3,
)

trainer = IntervalTrainer(
    model=model,                  # your torch.nn.Module
    train_dataset=train_dataset,  # torch Dataset, not DataLoader
    val_dataset=val_dataset,      # torch Dataset, not DataLoader
    loss_function=loss_fn,        # e.g. nn.CrossEntropyLoss()
    metric_func=metric,           # returns a float used to pick the best model
    val_step=None,                # None: validate after each training epoch
    epochs=20,
    device="cpu",                 # Lightning Fabric accelerator; the notebooks use "gpu" on GPU machines
    callbacks=[],                 # optional callback objects
    project_name="MNIST_example",
)

trainer.train_using_predictor(co2_predictor, interval_generator)
```

Pass Dataset objects, not DataLoaders. The trainer builds its own DataLoaders with a resumable sampler.

The notebook's full example trains a small CNN on MNIST and uses `BestModelSavingCallback`, which saves `best_model.pth` when the validation metric improves, and `EarlyStoppingCallback`.

### Google Cloud

The Google Cloud walkthrough is in `examples/eco4cast_demo/quick_start_guide.ipynb`. It covers creating a VM, downloading `application_default_credentials.json`, generating an SSH key, and getting an Electricity Maps key.

The master machine runs a script like this (based on `examples/MNIST_google_cloud/master_machine_main.py`):

```python
import os
from pathlib import Path

from eco4cast.master_machine.interval_predictor import CO2Predictor, IntervalGenerator
from eco4cast.master_machine.master_machine_controller import Controller

username = "scheduler"
electricity_maps_api_key = "YOUR_API_KEY"

controller = Controller(
    credentials_path=Path(os.getcwd()) / "application_default_credentials.json",
    ssh_username=username,
    ssh_python_path=f"/home/{username}/venv/bin/python",
    ssh_vm_main_path=f"/home/{username}/scheduler_task/vm_main.py",
    current_vm_ip="VM_EXTERNAL_IP",
    ssh_port=22,
    current_zone="northamerica-northeast1-c",
    current_instance_name="instance-3",
    project_id="YOUR_PROJECT_ID",
    intervals_prediction_period=3600,  # seconds
    co2_predictor=CO2Predictor(electricity_maps_api_key),
    interval_generator=IntervalGenerator(),
)

controller.start_training()
print("Successfully finished all intervals. Stopping Instance")
controller.stop_training()
```

The training VM runs a script (`vm_main.py`) that defines the model and datasets, parses `--times`, `--co2_means`, and `--load_states` arguments, and creates an `IntervalTrainer`. See `examples/MNIST_google_cloud/vm_main.py` and `examples/ImageNet_google_cloud/` for complete versions. The examples in `examples/README.md` describe how to adapt `vm_main.py` to your own dataset.

## Configuration

### `CO2Predictor(electricity_maps_api_key, checkpoint_file_path=None, exclude_zones=None, include_zones=None)`

| Parameter | Description |
|---|---|
| `electricity_maps_api_key` | Electricity Maps API key. |
| `checkpoint_file_path` | Path to a model checkpoint. If `None`, the bundled `co2_model.ckpt` is used. |
| `exclude_zones` | Zones to leave out of the forecast. |
| `include_zones` | If set, only these zones are used. Otherwise all supported zones are used. |

### `IntervalGenerator(max_emission_value=180, co2_delta_to_move=30, min_interval_size=1, max_window_size=3, exclude_zones=None, include_zones=None)`

| Parameter | Default | Description |
|---|---|---|
| `max_emission_value` | `180` | A window is eligible for training only if its mean forecast intensity is below this value. |
| `co2_delta_to_move` | `30` | How much lower another zone's intensity must be before the trainer moves to it. |
| `min_interval_size` | `1` | Minimum interval length, in hours. |
| `max_window_size` | `3` | Largest moving-average window, in hours, used for thresholding. |
| `exclude_zones` | `None` | Zones to exclude. |
| `include_zones` | `None` | If set, only these zones are used. |

### `Controller(...)`

| Parameter | Description |
|---|---|
| `credentials_path` | Path to the Google Cloud credentials file. Sets `GOOGLE_APPLICATION_CREDENTIALS`. |
| `ssh_username`, `ssh_port` | SSH login for the training VM. |
| `ssh_python_path` | Python interpreter on the VM. |
| `ssh_vm_main_path` | Path to `vm_main.py` on the VM. |
| `current_vm_ip` | External IP of the training VM. Updated after a zone move. |
| `current_zone`, `current_instance_name`, `project_id` | Identify the instance in Google Cloud. |
| `intervals_prediction_period` | How often, in seconds, the forecast is re-run. |
| `co2_predictor`, `interval_generator` | Instances of the classes above. |

### `IntervalTrainer(...)`

| Parameter | Default | Description |
|---|---|---|
| `model`, `train_dataset`, `val_dataset`, `loss_function`, `metric_func` | required | Model, datasets, loss, and a metric function that returns a float. |
| `optimizer` | `torch.optim.Adam` | Optimizer class. |
| `lr` | `1e-4` | Learning rate. |
| `epochs` | `3` | Number of epochs. |
| `val_step` | `None` | Validate every N training batches. `None` validates after each training epoch. |
| `batch_size` | `8` | Batch size. |
| `device` | `"cpu"` | Lightning Fabric accelerator. |
| `show_progressbar` | `True` | Show progress bars. |
| `callbacks` | `None` | Callback objects. Hooks are called through Lightning Fabric. |
| `project_name` | `"noname_project"` | Name passed to eco2ai. |
| `num_workers` | `1` | DataLoader workers. |

## Supported zones

Zones are [Electricity Maps](https://www.electricitymaps.com/) zone codes. The package maps each code to a Google Cloud zone for VM moves.

| Code | Region | Google Cloud zone |
|---|---|---|
| `BR-CS` | Central Brazil | `southamerica-east1-b` |
| `CA-ON` | Ontario, Canada | `northamerica-northeast2-b` |
| `CA-QC` | Quebec, Canada | `northamerica-northeast1-c` |
| `CH` | Switzerland | `europe-west6-b` |
| `DE` | Germany | `europe-west3-b` |
| `PL` | Poland | `europe-central2-b` |
| `BE` | Belgium | `europe-west1-b` |
| `IT-NO` | Northern Italy | `europe-west8-a` |
| `ES` | Spain | `europe-southwest1-c` |
| `GB` | Great Britain | `europe-west2-b` |
| `FI` | Finland | `europe-north1-b` |
| `FR` | France | `europe-west9-b` |
| `NL` | Netherlands | `europe-west4-b` |

These 13 zones are defined in `eco4cast/master_machine/utils.py`. The local notebook lists the same zones.

## Repository layout

```
eco4cast/
├── master_machine/              # Forecasting and orchestration (runs locally or on the master machine)
│   ├── interval_predictor.py    # CO2Predictor and IntervalGenerator
│   ├── co2_model.py             # Lightning model (temporal convolutional network + regression head)
│   ├── tcn_pytorch.py           # Temporal convolutional network layers (from locuslab/TCN)
│   ├── electricitymaps_api.py   # Electricity Maps history requests
│   ├── weather_data_utils.py    # Open-Meteo weather requests
│   ├── master_machine_controller.py  # Controller: SSH, VM moves, emissions summary
│   ├── google_cloud_vm_moving.py     # Snapshot-based VM move between zones
│   ├── utils.py                 # Zone codes and zone-to-Google-Cloud mapping
│   ├── data_files/              # Bundled checkpoint and country points
│   └── compute/client_library/  # Google Compute Engine sample code used by the VM-move code
├── virtual_machine/
│   ├── smart_scheduler_concept.py  # IntervalTrainer
│   └── utils.py                 # Resumable sampler and progress bar helpers
examples/
├── eco4cast_local_demo/         # Local-machine notebook
├── eco4cast_demo/               # Google Cloud quick-start notebook
├── MNIST_google_cloud/          # MNIST: master_machine_main.py and vm_main.py
└── ImageNet_google_cloud/       # ImageNet: master_machine_main.py and vm_main.py
images/                          # Logo
dist/                            # Built package (0.0.8)
```

`eco4cast/virtual_machine/smart_scheduler_concept.py` is named "concept" in the repository. Its `IntervalTrainer` is the one used by the examples.

## Limitations

- **The forecast is a model prediction.** The repository does not include accuracy or savings benchmarks. The local notebook's output shows that the example run saved about 0 g of CO2 against the average. Results depend on the zone and the forecast.
- **Google Cloud moves are destructive to the instance.** A zone move deletes the instance and its boot disk, then recreates them from a snapshot in the target zone. The controller then uses the new instance's external IP for SSH. The new disk is created as `pd-standard`.
- **The repository has no automated tests for the `eco4cast` package.** The only test files are in the vendored Compute Engine sample code under `eco4cast/master_machine/compute/client_library/snippets/tests/`.
- **The example scripts contain hardcoded Electricity Maps API keys and project and IP values** (`examples/*_google_cloud/*.py`). Replace them with your own values, keep them out of version control, and rotate any key that has been published.
- **Training can run past an interval's end.** The trainer checks the end time between batches, so a batch that started before the end finishes before training stops.
- **`pyproject.toml` does not declare `requests` or `tqdm`,** which the code imports.

## License

Apache License 2.0. See [LICENSE](LICENSE). The vendored Google Compute Engine sample code in `eco4cast/master_machine/compute/client_library/` has its own README, which links to Google's documentation.

## Authors

From `pyproject.toml`:

- Mikhail Tiutiulnikov
- Vladimir Lazarev
- Aleksei Korovin
- Semen Budennyi

Project repository: <https://github.com/AIRI-Institute/eco4cast>
