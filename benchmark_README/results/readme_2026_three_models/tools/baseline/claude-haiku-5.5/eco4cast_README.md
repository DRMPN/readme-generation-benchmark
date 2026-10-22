# eco4cast

eco4cast is a Python package for training neural networks while reducing their CO2 emissions. It forecasts carbon intensity for a set of electricity zones, selects training windows when the grid is cleanest, and runs training in those windows. On Google Cloud, it can also move the training virtual machine to a zone with lower forecast emissions.

The package is published as version 0.0.8 and is licensed under the Apache License 2.0.

## Overview

eco4cast has two sides:

- **Master machine** (`eco4cast/master_machine/`): predicts CO2 intensity, generates training intervals, and controls the training VM over SSH. On Google Cloud it can also move the VM between zones.
- **Virtual machine** (`eco4cast/virtual_machine/`): runs the training loop. `IntervalTrainer` trains only during scheduled time intervals, saves its state when an interval ends, and resumes from that state in a later interval, possibly on a different machine.

Main components:

| Component | Location | Purpose |
|---|---|---|
| `CO2Predictor` | `master_machine/interval_predictor.py` | Loads a trained model and forecasts 24 hours of CO2 intensity for 13 zones. |
| `IntervalGenerator` | `master_machine/interval_predictor.py` | Turns forecasts into training intervals below an emission threshold. |
| `Controller` | `master_machine/master_machine_controller.py` | Starts training on a remote VM over SSH, waits for intervals, and reports estimated savings. |
| `CO2Model` | `master_machine/co2_model.py` | A PyTorch Lightning model that uses a temporal convolutional network (TCN) to forecast emissions. |
| `IntervalTrainer` | `virtual_machine/smart_scheduler_concept.py` | Interval-based training with Lightning Fabric, callbacks, and resumable state. |
| `google_cloud_move_vm` | `master_machine/google_cloud_vm_moving.py` | Snapshots a VM disk, recreates the VM in another zone, and deletes the snapshot. |
| `electricitymaps_api.py` | `master_machine/` | Retrieves 24-hour carbon intensity history from the Electricity Maps free-tier API. |
| `weather_data_utils.py` | `master_machine/` | Retrieves hourly weather data from the Open-Meteo API. |

The model input uses Open-Meteo weather parameters (temperature, humidity, pressure, cloud cover, wind, radiation, precipitation, and others) together with Electricity Maps emission history and location coordinates.

## Installation

eco4cast requires Python 3.9 or later (`python = "^3.9"`).

Install the published package:

```bash
pip install eco4cast
```

Or install from the distribution files included in the repository:

```bash
pip install dist/eco4cast-0.0.8-py3-none-any.whl
```

The main dependencies declared in `pyproject.toml` are:

- `torch` (^2.0.1)
- `lightning` (^2.0.2)
- `apscheduler` (^3.10.1)
- `eco2ai` (^0.3.9)
- `paramiko` (^3.2.0)
- `numpy` (>=1.23.5)
- `pandas` (>=1.4.3)
- `scikit-learn` (^1.2.2)
- `google-cloud-compute` (^1.11.0)

Other modules import `requests` and `tqdm`, which are not listed in `pyproject.toml`. The example notebooks also install `torchvision` for the MNIST example.

### External accounts and credentials

- **Electricity Maps API key.** `CO2Predictor` requires an API key for the Electricity Maps free-tier carbon intensity endpoint. The local and Google Cloud notebooks walk through obtaining one.
- **Google Cloud application default credentials.** The Google Cloud workflow requires a credentials JSON file. `Controller` sets the `GOOGLE_APPLICATION_CREDENTIALS` environment variable from its `credentials_path` argument.
- **SSH access to the training VM.** The controller connects to the VM with `paramiko`, using the username, port, and paths you provide.

## Usage

### Option 1: Training on Google Cloud

The example in `examples/MNIST_google_cloud/` shows the master machine side. A script like this creates a `Controller`, starts training, and stops the instance when it finishes:

```python
from pathlib import Path
import os
from eco4cast.master_machine.master_machine_controller import Controller
from eco4cast.master_machine.interval_predictor import CO2Predictor, IntervalGenerator

controller = Controller(
    credentials_path=Path(os.getcwd()) / "application_default_credentials.json",
    ssh_username="scheduler",
    ssh_python_path="/home/scheduler/venv/bin/python",
    ssh_vm_main_path="/home/scheduler/scheduler_task/vm_main.py",
    current_vm_ip="<VM external IP>",
    ssh_port=22,
    current_zone="northamerica-northeast1-c",
    current_instance_name="instance-3",
    project_id="<your-project-id>",
    intervals_prediction_period=3600,  # seconds
    co2_predictor=CO2Predictor("<your-electricity-maps-api-key>"),
    interval_generator=IntervalGenerator(),
)

controller.start_training()
controller.stop_training()
```

On the VM, `vm_main.py` runs the training. The controller passes it these command-line arguments:

- `--times`: comma-separated timestamps in `%Y%m%d%H%M%S` format, as start/end pairs.
- `--co2_means`: the forecast mean emission for each interval.
- `--load_states`: added after the first interval so training resumes from saved state.

The VM script must accept these arguments. The MNIST `vm_main.py` in `examples/eco4cast_demo/` parses them with `argparse`. It then builds an `IntervalTrainer` and calls `trainer.train(intervals, load_states, co2_means)`.

The ImageNet example in `examples/ImageNet_google_cloud/` follows the same pattern with a ResNet-101 model, `EarlyStoppingCallback`, and `BestModelSavingCallback`.

The Google Cloud quick start is in `examples/eco4cast_demo/quick_start_guide.ipynb`. It covers creating a VM, signing up for Electricity Maps, and the shell commands needed for setup.

### Option 2: Training on a local machine

Use `CO2Predictor` and `IntervalGenerator` without a remote VM. `IntervalTrainer.train_using_predictor` runs the forecasting and training loop together:

```python
from eco4cast.master_machine.interval_predictor import CO2Predictor, IntervalGenerator
from eco4cast.virtual_machine.smart_scheduler_concept import IntervalTrainer

trainer = IntervalTrainer(
    model=my_model,
    train_dataset=train_dataset,
    val_dataset=val_dataset,
    loss_function=loss_fn,
    metric_func=metric_fn,
    epochs=20,
    device="cpu",
)

trainer.train_using_predictor(
    co2_predictor=CO2Predictor("<your-electricity-maps-api-key>"),
    interval_generator=IntervalGenerator(),
)
```

The notebook `examples/eco4cast_local_demo/local_quick_start_guide.ipynb` walks through this workflow. It lists the zones supported for local use: BR-CS, CA-ON, CH, DE, PL, BE, IT-NO, CA-QC, ES, GB, FI, FR, and NL.

## Configuration

### CO2Predictor

`CO2Predictor(electricity_maps_api_key, checkpoint_file_path=None, exclude_zones=None, include_zones=None)`

- `electricity_maps_api_key`: the Electricity Maps API key.
- `checkpoint_file_path`: path to a model checkpoint. If omitted, the bundled `co2_model.ckpt` is used.
- `exclude_zones` / `include_zones`: zone codes to leave out or to restrict forecasting to.

The predictor uses a 24-hour lookback window and forecasts 24 hours ahead. It loads point coordinates from the bundled `country_points.pickle`. The model is built with 23 × 38 input features, TCN channels `[512, 256, 256, 256, 256]`, kernel size 3, and dropout 0.0. It runs on CPU.

### IntervalGenerator

`IntervalGenerator(max_emission_value=180, co2_delta_to_move=30, min_interval_size=1, max_window_size=3, exclude_zones=None, include_zones=None)`

- `max_emission_value`: threshold for the moving-window mean emission. Windows below this value are eligible for training.
- `co2_delta_to_move`: the minimum emission difference between zones needed before the VM switches zones.
- `min_interval_size`: the minimum training interval length, in hours.
- `max_window_size`: the largest moving-average window used when checking the threshold.
- `exclude_zones` / `include_zones`: zone filters.

### Controller

Key arguments:

- `credentials_path`: Google Cloud credentials file.
- `ssh_username`, `ssh_python_path`, `ssh_vm_main_path`, `ssh_port`: how to run `vm_main.py` on the VM.
- `current_vm_ip`, `current_zone`, `current_instance_name`: the VM's current location.
- `project_id`: the Google Cloud project.
- `intervals_prediction_period`: how often, in seconds, the forecast is refreshed.
- `co2_predictor`, `interval_generator`: instances of the classes above.

### Zone mapping

`eco4cast/master_machine/utils.py` maps Electricity Maps zone codes to Google Cloud zones, for example `DE` to `europe-west3-b` and `CA-QC` to `northamerica-northeast1-c`. It also lists per-zone step values in `codes_with_steps`. Update these mappings if you need zones other than those listed.

### IntervalTrainer

Key arguments:

- `model`, `train_dataset`, `val_dataset`, `loss_function`, `metric_func`: the training setup.
- `optimizer` (default `torch.optim.Adam`) and `lr` (default `1e-4`).
- `epochs` (default 3), `batch_size` (default 8), `val_step`: validate every N training steps, or after each epoch if `None`.
- `device` (default `"cpu"`), `num_workers`, `show_progressbar`.
- `callbacks`: objects with methods such as `on_validation_epoch_end(trainer, val_metric)`.
- `project_name`: used by the `eco2ai` emission tracker.

Training state is saved to `fabric_checkpoint.ckpt`. Emissions are written to `emission.csv` by `eco2ai`.

### Environment and secrets

The example scripts contain placeholder API keys and VM addresses. Replace them with your own values and avoid committing real keys to version control.

## Project structure

```
eco4cast/
  master_machine/        # Forecasting, interval generation, VM control
    compute/client_library/   # Google Compute Engine sample code and SGS tooling
    data_files/          # co2_model.ckpt, country_points.pickle
  virtual_machine/       # IntervalTrainer and resumable sampler
examples/                # MNIST, ImageNet, and notebook examples
dist/                    # Built wheel and source distribution (0.0.8)
images/                  # Project image
pyproject.toml           # Poetry metadata and dependencies
```

`eco4cast/master_machine/compute/client_library/` contains Google Compute Engine code samples, organized into `ingredients/`, `recipes/`, and `snippets/`. The `sgs.py` script (Snippet Generating System) builds the files in `snippets/` from `recipes/` and `ingredients/`.

## Development

eco4cast is built with Poetry (`build-backend = "poetry.core.masonry.api"`). To build the package locally:

```bash
pip install poetry-core
poetry build
```

Package metadata is in `pyproject.toml`. Version 0.0.8 is the current version.

### Generating Compute Engine snippets

The Compute Engine samples are generated, not written by hand. From `eco4cast/master_machine/compute/client_library/`:

- To add a sample, create a file in `recipes/`. It needs an `# <IMPORTS/>` line and at least one `# <INGREDIENT name/>` line.
- To add reusable code, create a file in `ingredients/` and wrap the code in `# <INGREDIENT name>` and `# </INGREDIENT>` markers. Put imports outside the markers.
- To regenerate `snippets/`, run `python3 sgs.py generate`.
- To move or remove a sample, change `recipes/`, delete the old generated file in `snippets/`, and regenerate.

The SGS does not interact with Git. Commit generated output together with the source changes.

## Testing

Test dependencies are listed in `eco4cast/master_machine/compute/client_library/requirements-test.txt`:

- `pytest==7.2.0`
- `pytest-xdist==3.3.1`
- `flaky==3.7.0`
- `google-cloud-storage==2.9.0`
- `google-cloud-kms==2.17.0`
- `py==1.11.0`

Install them with:

```bash
pip install -r eco4cast/master_machine/compute/client_library/requirements-test.txt
```

`test_sgs.py` in the same folder contains two tests:

- `test_sgs_generate` runs the generator on fixtures in `sgs_test_fixtures/` and compares the output with the expected files.
- `test_snippets_freshness` regenerates the snippets and fails if the committed `snippets/` differ from the output.

The `snippets/tests/` folder holds Compute Engine sample tests. Some of them require a Google Cloud project; `noxfile_config.py` sets `BUILD_SPECIFIC_GCLOUD_PROJECT` as the project environment variable. The repository does not include a test suite for the `eco4cast` core modules.

Code style tools used by the Compute Engine samples are listed in `requirements.txt`: `isort==5.12.0` and `black==23.3.0`.

## License

eco4cast is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full text.

The license file names the copyright holders as Vladimir Lazarev, Nikita Zakharenko, Semyon Budyonny, and leonid zhukov. The package metadata lists these authors: Mikhail Tiutiulnikov, Vladimir Lazarev, Aleksei Korovin, and Semen Budennyi.

The Google Compute Engine sample files under `compute/client_library/` carry their own Apache 2.0 headers with the copyright notice "Copyright Google LLC."
