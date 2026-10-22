# eco4cast

A Python package designed to reduce CO2 emissions while training neural networks using Google Cloud.

**eco4cast** forecasts regional electricity carbon intensity and schedules model training inside the periods with the lowest expected emissions. On Google Cloud it can automatically move a virtual machine between zones to follow the cleanest electricity, while on a local machine it pauses and resumes training around the low-emission intervals.

## Features

- **CO2 forecasting** – `CO2Predictor` uses a TCN-based neural network (`CO2Model`) to produce a 24-hour carbon-intensity forecast for each supported zone. Weather data and the last 24 hours of measured carbon intensity are fetched from public sources and the [ElectricityMaps API](https://api-portal.electricitymaps.com/).
- **Interval generation** – `IntervalGenerator` converts the forecast into training intervals that satisfy emission thresholds, deciding when (and, on Google Cloud, where) to train.
- **Resumable training** – `IntervalTrainer` (built on [Lightning Fabric](https://lightning.ai/docs/fabric/stable/)) can stop and resume training across intervals and even across different machines without losing progress: the current epoch, batch and sampler state are preserved.
- **Google Cloud VM migration** – the `Controller` class coordinates training over SSH and uses the Google Cloud API to move the VM to the zone with the lowest predicted emission.
- **Emission tracking** – training is tracked with [eco2ai](https://github.com/socal-nerds/eco2ai), and the total (and saved) CO2 emissions are reported at the end of a run.

## Installation

```bash
pip install eco4cast
```

The package requires Python 3.9+ and depends on PyTorch, Lightning, apscheduler, eco2ai, paramiko, NumPy, pandas, scikit-learn and `google-cloud-compute` (installed automatically).

## Usage

There are two main ways to use eco4cast:

1. [On your local machine](#usage-on-your-local-machine)
2. [With Google Cloud](#usage-with-google-cloud)

In both cases you need an [ElectricityMaps](https://api-portal.electricitymaps.com/) API key. You can apply for the free tier (non-commercial use only) or subscribe to the countries info.

### Usage on your local machine

eco4cast trains your PyTorch model during the time windows with minimal expected CO2 emission on your own hardware. A step-by-step guide is available in [`examples/eco4cast_local_demo/local_quick_start_guide.ipynb`](examples/eco4cast_local_demo/local_quick_start_guide.ipynb).

Pass `torch.utils.data.Dataset` objects (not DataLoaders) to the trainer — the DataLoaders are created inside `IntervalTrainer` with a custom resumable sampler. Callbacks receive the trainer and the current validation metric on `on_validation_epoch_end`.

```python
from torch import nn
import torch

from eco4cast.master_machine.interval_predictor import CO2Predictor, IntervalGenerator
from eco4cast.virtual_machine.smart_scheduler_concept import IntervalTrainer

# Callback example: saves the best model and stops early
class BestModelSavingCallback:
    def __init__(self, mode="max") -> None:
        assert mode in ["min", "max"]
        self.best_val_metric = 1e9 if mode == "min" else -1e9
        self.mode = mode

    def on_validation_epoch_end(self, trainer, val_metric):
        if (self.mode == "min" and val_metric < self.best_val_metric) or (
            self.mode == "max" and val_metric > self.best_val_metric
        ):
            self.best_val_metric = val_metric
            torch.save(trainer.model.state_dict(), "best_model.pth")


electricity_maps_api_key = ""  # your API key here
your_zone = "BE"  # choose a zone from the supported list below

co2_predictor = CO2Predictor(electricity_maps_api_key, include_zones=[your_zone])
interval_generator = IntervalGenerator(
    include_zones=[your_zone],
    max_emission_value=115,   # threshold for the allowed emission in a moving window
    co2_delta_to_move=30,     # minimum emission difference to consider moving a VM
    min_interval_size=1,      # minimum training interval length in hours
    max_window_size=3,        # maximum moving-average window size for thresholding
)


def accuracy(labels, logits):
    preds = logits.argmax(1)
    return (preds == labels).float().mean()


trainer = IntervalTrainer(
    model=Net(),                       # any torch.nn.Module
    train_dataset=train_dataset,       # torch Dataset
    val_dataset=val_dataset,           # torch Dataset
    loss_function=nn.CrossEntropyLoss(),
    metric_func=accuracy,
    val_step=None,                     # validate once per epoch if None
    show_progressbar=True,
    epochs=20,
    device="gpu",                      # or "cpu"
    callbacks=[BestModelSavingCallback()],
    project_name="MNIST_example",
)

trainer.train_using_predictor(co2_predictor, interval_generator)
```

### Usage with Google Cloud

On Google Cloud the training is split between two roles:

- **Master machine** – runs `Controller`, predicts CO2, generates intervals, connects to the training VM over SSH and, if needed, moves the VM between zones using the Google Cloud API.
- **Training VM (`vm_main.py`)** – contains the training logic. It initializes the model and datasets with PyTorch, uses Lightning Fabric callbacks, and parses `--times` and `--co2_means` arguments with the training intervals for the current zone.

A step-by-step guide (project setup, credentials, SSH keys and VM creation) is available in [`examples/eco4cast_demo/quick_start_guide.ipynb`](examples/eco4cast_demo/quick_start_guide.ipynb). Ready-to-run training scripts are provided in [`examples/MNIST_google_cloud`](examples/MNIST_google_cloud) and [`examples/ImageNet_google_cloud`](examples/ImageNet_google_cloud).

Master machine side (`master_machine_main.py`):

```python
import os
from pathlib import Path

from eco4cast.master_machine.master_machine_controller import Controller
from eco4cast.master_machine.interval_predictor import (
    CO2Predictor,
    IntervalGenerator,
)

electricity_maps_api_key = ""  # your API key here

controller = Controller(
    credentials_path=Path(os.getcwd()) / "application_default_credentials.json",
    ssh_username="scheduler",
    ssh_python_path="/home/scheduler/venv/bin/python",
    ssh_vm_main_path="/home/scheduler/scheduler_task/vm_main.py",
    current_vm_ip="34.155.134.116",     # external IP of your VM
    ssh_port=22,
    current_zone="europe-west9-b",      # zone of your VM
    current_instance_name="instance-1", # name of your VM instance
    project_id="test-smart-scheduler",  # your Google Cloud project id
    intervals_prediction_period=3600,   # seconds between forecasts
    co2_predictor=CO2Predictor(electricity_maps_api_key, exclude_zones=["CA-ON", "CA-QC"]),
    interval_generator=IntervalGenerator(exclude_zones=["CA-ON", "CA-QC"]),
)

controller.start_training()
# controller.stop_training()  # stops the instance via the Google Cloud API
```

When training ends, the controller fetches the `emission.csv` produced by eco2ai from the VM and prints the total CO2 emissions together with the amount saved compared with an average-intensity run.

## Supported ElectricityMaps zones

The following zones are currently supported for local usage:

| Zone code | Region |
| --- | --- |
| `BR-CS` | Central Brazil |
| `CA-ON` | Canada Ontario |
| `CA-QC` | Canada Quebec |
| `CH` | Switzerland |
| `DE` | Germany |
| `PL` | Poland |
| `BE` | Belgium |
| `IT-NO` | North Italy |
| `ES` | Spain |
| `GB` | Great Britain |
| `FI` | Finland |
| `FR` | France |
| `NL` | Netherlands |

## Examples

The [`examples/`](examples/README.md) folder contains:

- [`eco4cast_demo/quick_start_guide.ipynb`](examples/eco4cast_demo/quick_start_guide.ipynb) – step-by-step guide on using eco4cast with Google Cloud, including VM creation, ElectricityMaps registration and the necessary Linux shell commands.
- [`eco4cast_local_demo/local_quick_start_guide.ipynb`](examples/eco4cast_local_demo/local_quick_start_guide.ipynb) – step-by-step guide on training a PyTorch model with minimal CO2 emission on your own hardware.
- [`MNIST_google_cloud/`](examples/MNIST_google_cloud) and [`ImageNet_google_cloud/`](examples/ImageNet_google_cloud) – scripts for training models on these datasets with Google Cloud.

## Repository layout

```
eco4cast/
├── master_machine/         # CO2 prediction, interval generation and Google Cloud orchestration
│   ├── master_machine_controller.py
│   ├── interval_predictor.py
│   ├── co2_model.py
│   ├── electricitymaps_api.py
│   ├── weather_data_utils.py
│   ├── google_cloud_vm_moving.py
│   ├── data_files/         # pre-trained CO2 model checkpoint and zone coordinates
│   └── compute/            # Google Cloud Compute Engine client library and code samples
└── virtual_machine/        # training-side code
    └── smart_scheduler_concept.py  # IntervalTrainer (resumable training)
```

## Requirements

- Python ^3.9
- torch ^2.0.1
- lightning ^2.0.2
- apscheduler ^3.10.1
- eco2ai ^0.3.9
- paramiko ^3.2.0
- numpy >= 1.23.5
- pandas >= 1.4.3
- scikit-learn ^1.2.2
- google-cloud-compute ^1.11.0

## License

This project is licensed under the [Apache License 2.0](LICENSE).

## Authors

- Mikhail Tiutiulnikov
- Vladimir Lazarev
- Aleksei Korovin
- Semen Budennyi
