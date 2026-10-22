# eco4cast

**eco4cast** is a Python package designed to reduce CO2 emissions while training neural networks using Google Cloud. It does so by forecasting hourly carbon intensity for a set of electricity zones (using an Electricity Maps API key and weather data), generating training time intervals in which emissions are minimal, and automatically moving a Google Cloud VM between zones so that training happens when and where the grid is cleanest. It can also be used locally on your own hardware to train only during low-emission periods.

- Repository: https://github.com/AIRI-Institute/eco4cast
- Version: 0.0.8 (distributions available in `dist/`)
- Keywords: CO2 emission, Google Cloud, PyTorch

## How it works

The package is split into two cooperating components:

1. **Master machine** (`eco4cast.master_machine`) — runs on a control machine (e.g., your laptop, a Colab notebook, or any cloud VM) and:
   - Fetches the last 24 hours of carbon-intensity history for each supported zone from the [Electricity Maps](https://api-portal.electricitymaps.com/) API (`electricitymaps_api.py`).
   - Fetches hourly weather data (temperature, cloud cover, wind, radiation, precipitation, etc.) for measurement points in each zone from the Open-Meteo API (`weather_data_utils.py`).
   - Feeds this into a pretrained Temporal Convolutional Network (`co2_model.py`, `tcn_pytorch.py`, checkpoint bundled in `data_files/co2_model.ckpt`) that produces a **24-hour CO2 intensity forecast** for each zone (`CO2Predictor` in `interval_predictor.py`).
   - `IntervalGenerator` converts the forecast into concrete UTC training intervals per zone, using thresholds such as maximum allowed emission, the minimum CO2 delta required to justify moving a VM, and minimum interval length.
   - `Controller` (`master_machine_controller.py`) then orchestrates the run: it connects to the training VM over SSH (paramiko), starts/resumes your `vm_main.py` training script with the scheduled intervals as arguments, snapshots and moves the Google Cloud VM between zones (`google_cloud_vm_moving.py`) when a cheaper zone is available, re-predicts periodically, stops the instance at the end, and prints a summary of total CO2 emissions versus an "average" baseline.

2. **Virtual machine** (`eco4cast.virtual_machine`) — runs on the training machine and contains the `IntervalTrainer` (`smart_scheduler_concept.py`). Built on **Lightning Fabric**, it:
   - Trains your PyTorch model only inside the scheduled UTC intervals (jobs are scheduled with APScheduler), saving a full checkpoint (model, optimizer, samplers, batch indices, metrics) when an interval ends and resuming exactly where it stopped — even on a different machine/zone.
   - Supports callbacks (e.g., early stopping, best-model saving) via Fabric hooks such as `on_validation_epoch_end`.
   - Tracks energy consumption and CO2 emissions with [eco2ai](https://pypi.org/project/eco2ai/) and writes them to `emission.csv`.

### Supported zones

The CO2 forecast covers 13 Electricity Maps zones, each mapped to a Google Cloud zone:

| Electricity Maps zone | Google Cloud zone |
|---|---|
| BR-CS (Central Brazil) | southamerica-east1-b |
| CA-ON (Canada Ontario) | northamerica-northeast2-b |
| CH (Switzerland) | europe-west6-b |
| DE (Germany) | europe-west3-b |
| PL (Poland) | europe-central2-b |
| BE (Belgium) | europe-west1-b |
| IT-NO (North Italy) | europe-west8-a |
| CA-QC (Canada Quebec) | northamerica-northeast1-c |
| ES (Spain) | europe-southwest1-c |
| GB (Great Britain) | europe-west2-b |
| FI (Finland) | europe-north1-b |
| FR (France) | europe-west9-b |
| NL (Netherlands) | europe-west4-b |

The same zones are supported for local training (see the local demo notebook).

## Requirements

From `pyproject.toml`:

- Python `>= 3.9`
- `torch >= 2.0.1`, `lightning >= 2.0.2`
- `google-cloud-compute >= 1.11.0`
- `apscheduler`, `eco2ai`, `paramiko`, `numpy`, `pandas`, `scikit-learn`

For the Google Cloud mode you additionally need:

- A Google Cloud account and project; a VM to run the training.
- Application default credentials (e.g., a service-account key file passed as `credentials_path`, which sets `GOOGLE_APPLICATION_CREDENTIALS`).
- An [Electricity Maps](https://api-portal.electricitymaps.com/) API key (free tier available for non-commercial use).
- SSH access to the training VM (username, port, Python interpreter path, and path to your `vm_main.py`).

## Installation

Install from PyPI:

```bash
pip install eco4cast
```

Or build/install from source (uses [Poetry](https://python-poetry.org/) as the build backend):

```bash
pip install poetry
poetry build
pip install dist/eco4cast-0.0.8-py3-none-any.whl
```

## Usage

There are two main ways to use eco4cast:

### 1. With Google Cloud

Follow the step-by-step Colab guide: [`examples/eco4cast_demo/quick_start_guide.ipynb`](examples/eco4cast_demo/quick_start_guide.ipynb) (also available as an "Open In Colab" badge in `examples/README.md`). It covers creating a VM, signing up at electricitymaps.com, and the necessary shell setup.

Ready-to-run training scripts are provided in `examples/MNIST_google_cloud/` and `examples/ImageNet_google_cloud/`:

- **`vm_main.py`** runs on the VM. It defines your model, datasets, loss, metric, and callbacks (e.g., `EarlyStoppingCallback`, `BestModelSavingCallback`), creates an `IntervalTrainer`, and calls `trainer.train(intervals, load_states, co2_means)`. It accepts `--times`, `--co2_means`, and `--load_states` arguments that the controller passes over SSH.
- **`master_machine_main.py`** runs on the master machine. It creates a `Controller` with your credentials path, SSH settings, VM IP/zone/instance name, project ID, prediction period, and instances of `CO2Predictor` and `IntervalGenerator`, then calls:

```python
controller.start_training()
controller.stop_training()
```

### 2. Locally

Follow [`examples/eco4cast_local_demo/local_quick_start_guide.ipynb`](examples/eco4cast_local_demo/local_quick_start_guide.ipynb). On a machine located in one of the supported zones, install `eco4cast` (plus `torchvision` for the MNIST example) and use `IntervalTrainer.train_using_predictor(co2_predictor, interval_generator)`, which forecasts CO2, generates intervals, and trains only during low-emission periods, printing a final emissions-saved summary.

### Example configuration knobs

- `CO2Predictor(electricity_maps_api_key, checkpoint_file_path=None, exclude_zones=None, include_zones=None)` — optionally use a custom model checkpoint or restrict zones.
- `IntervalGenerator(max_emission_value=180, co2_delta_to_move=30, min_interval_size=1, max_window_size=3, exclude_zones=None, include_zones=None)` — control when a VM is allowed to train and when it is worth moving.
- `IntervalTrainer(model, train_dataset, val_dataset, loss_function, metric_func, optimizer, lr, epochs, val_step, batch_size, device, show_progressbar, callbacks, project_name, num_workers)` — a standard training loop that pauses/resumes across intervals.

## Bundled Google Compute Engine client library

`eco4cast/master_machine/compute/client_library/` contains Google Compute Engine code samples (derived from the Google Cloud `python-docs-samples` compute client library) organized as `ingredients/`, `recipes/`, and generated `snippets/` covering disks, firewall rules, images, instance templates, instances (creation, start/stop, suspend/resume, preemptible/spot VMs, custom machine types, delete protection), routes, snapshots, operations, and usage reports. These snippets are used internally for VM management (e.g., `google_cloud_vm_moving.py`).

To regenerate the snippets, run from the `client_library` directory:

```bash
python3 sgs.py generate
```

The SGS (Snippet Generating System) fills `# <IMPORTS/>` and `# <INGREDIENT name/>` markers in recipes with code from ingredients. See `client_library/README.md` for details on adding/removing samples and `snippets/README.md` for running the quickstart (requires `pip install -r requirements.txt` and `gcloud auth application-default login`).

## Development

- The project is packaged with Poetry (`poetry-core` build backend); metadata lives in `pyproject.toml`.
- Formatting tools are pinned in `client_library/requirements.txt` (`black`, `isort`); the SGS applies `black` to generated snippets automatically.

## Testing

The client library has a pytest test suite in `client_library/snippets/tests/` covering VM creation, disks, firewall, images, pagination, snapshots, spot/preemptible VMs, suspend/resume, custom hostnames/types, delete protection, templates, routes, and more. Test dependencies are listed in `requirements-test.txt`:

```bash
pip install -r requirements-test.txt
```

The SGS itself is tested by `test_sgs.py`, which verifies that the generated snippets match fixtures and that the `snippets/` folder is up to date (`test_snippets_freshness` — run `python sgs.py generate` if it fails). Note that `noxfile_config.py` indicates tests are expected to run against a dedicated (`BUILD_SPECIFIC_GCLOUD_PROJECT`) Cloud project, and the snippet tests exercise real Google Cloud resources.

## License

This project is licensed under the **Apache License 2.0**. See the [`LICENSE`](LICENSE) file for the full text. Copyright holders listed in the license include Vladimir Lazarev, Nikita Zakharenko, Semyon Budyonny, and Leonid Zhukov; package authors per `pyproject.toml` are Mikhail Tiutiulnikov, Vladimir Lazarev, Aleksei Korovin, and Semen Budennyi (AIRI). Portions of the bundled Compute Engine samples are Copyright Google LLC, also under Apache 2.0.
