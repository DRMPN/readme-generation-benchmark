# eco4cast-l2k_9zxr

> **Note:** This README was written from the file listing alone, without access to the source code. Module purposes are inferred from file names and should be checked against the code. Items marked *(inferred)* are educated guesses. Replace placeholders such as `<PROJECT_ID>` with real values.

## Overview

**eco4cast-l2k_9zxr** appears to be a carbon-aware computing project. It combines three things:

1. **CO₂ intensity forecasting.** A temporal convolutional network (TCN) model, implemented in PyTorch, predicts the carbon intensity of electricity grids. It uses weather data and grid data from the ElectricityMaps API. A pretrained checkpoint (`co2_model.ckpt`) and a country lookup table (`country_points.pickle`) support this.
2. **Carbon-aware scheduling.** A "smart scheduler" concept and a master machine controller decide when and where to run workloads, based on forecast carbon intensity.
3. **Google Compute Engine VM orchestration.** Scripts create, start, stop, suspend, resume, and move virtual machines on Google Cloud. A large set of Compute Engine API sample snippets is included, which likely serves as reference or building blocks.

The project is also tied to the **Eco4Cast** initiative, as suggested by the `eco4cast_color.jpg` asset and the repository name.

## Repository Structure

The listing is flattened, so the directory layout below is reconstructed from file names and may not be exact.

```
eco4cast-l2k_9zxr/
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── eco4cast_color.jpg
├── master_machine_main.py          # Entry point for the master/controller (inferred)
├── vm_main.py                      # Entry point for VM-side logic (inferred)
├── quick_start_guide.ipynb         # Walkthrough notebook
├── local_quick_start_guide.ipynb   # Walkthrough for running locally
│
├── <forecasting package>/
│   ├── __init__.py
│   ├── co2_model.py                # Model definition and inference wrapper
│   ├── co2_model.ckpt              # Pretrained model weights
│   ├── tcn_pytorch.py              # TCN architecture in PyTorch
│   ├── interval_predictor.py       # Prediction intervals / uncertainty
│   ├── electricitymaps_api.py      # Client for the ElectricityMaps API
│   ├── weather_data_utils.py       # Weather data fetching and preprocessing
│   ├── country_points.pickle       # Country/region geographic reference data
│   └── utils.py                    # Shared helpers
│
├── <scheduling package>/
│   ├── smart_scheduler_concept.py  # Carbon-aware scheduling logic
│   ├── master_machine_controller.py# Coordinates VMs and scheduling decisions
│   ├── google_cloud_vm_moving.py   # Migrates workloads between VMs/regions
│   └── utils.py
│
├── config/
│   ├── noxfile_config.py           # Configuration for nox test sessions
│   └── sgs.py                      # Purpose unclear from name (inferred)
│
├── gce_samples/                    # Compute Engine API snippets (see below)
│   ├── instances/                  # create, start, stop, suspend, resume, delete, list
│   ├── disks/                      # create, attach, resize, clone, delete
│   ├── snapshots/
│   ├── images/                     # create, deprecate, delete, list
│   ├── firewalls/
│   ├── routes/                     # including KMS routes
│   ├── templates/                  # instance templates
│   ├── operations/                 # wait_for_extended_operation, operation_check
│   ├── preemptible/ and spot/
│   └── ...
│
└── tests/
    ├── test_sgs.py
    ├── test_instance_*.py, test_disks.py, test_snapshots.py, ...
    ├── requirements-test.txt
    └── experimental_recipe.pytest, ingredient1.pytest, ingredient2.pytest
```

### Notes on the layout

- **Duplicated listings.** The file list repeats several sample directories, and many sample files appear in more than one place. Deduplicate before relying on the structure.
- **Odd test file extensions.** The `.pytest` files (`experimental_recipe.pytest`, `ingredient1.pytest`, `ingredient2.pytest`) are not standard Python test files. They may be test fixtures, data, or misnamed files. Verify them before relying on them.
- **`README.md` files.** Several subdirectories contain READMEs, which likely explain the samples.

## Key Components

### 1. CO₂ Forecasting (`co2_model.py`, `tcn_pytorch.py`, `interval_predictor.py`)

- `tcn_pytorch.py` implements a **Temporal Convolutional Network** with dilated causal convolutions, suited to time-series forecasting.
- `co2_model.py` loads `co2_model.ckpt` and runs inference to forecast grid carbon intensity (typically in gCO₂eq/kWh).
- `interval_predictor.py` produces prediction intervals, so downstream schedulers can account for forecast uncertainty.

**Typical flow (inferred):**
1. Fetch recent grid carbon intensity and weather data for a region.
2. Preprocess into the model's input window.
3. Run the TCN to forecast intensity over a horizon.
4. Compute intervals and return them to the scheduler.

### 2. Data Sources (`electricitymaps_api.py`, `weather_data_utils.py`, `country_points.pickle`)

- **ElectricityMaps API** provides historical and near-real-time carbon intensity and power-mix data for many regions. An API token is required.
- **Weather data utilities** fetch and align meteorological features (for example, temperature, wind, and solar radiation), which correlate with renewable generation.
- **`country_points.pickle`** maps country or zone codes to geographic reference points, used to pull weather for each region.

### 3. Carbon-Aware Scheduling (`smart_scheduler_concept.py`, `master_machine_controller.py`)

- The **smart scheduler** concept selects the best time window or region to run a job, based on forecast intensity.
- The **master machine controller** manages worker VMs, decides when to start, stop, suspend, or move them, and records the decisions.

### 4. VM Orchestration (`google_cloud_vm_moving.py`, `master_machine_main.py`, `vm_main.py`)

- `google_cloud_vm_moving.py` moves workloads between Compute Engine instances or regions. It likely uses snapshots or disk cloning, based on the sample code available.
- `master_machine_main.py` is the entry point for the controller.
- `vm_main.py` is the entry point for code running on the worker VM. A `vm_main.py` appears in several locations, which may be copies or per-environment variants.

### 5. Compute Engine Sample Snippets (`gce_samples/`)

The bulk of the repository consists of Compute Engine API example code, following the layout of Google's `python-docs-samples`. These cover:

| Category | Examples |
|---|---|
| Instances | create, create from template or snapshot, start, stop, suspend, resume, delete, change machine type, serial port, Windows instances, encrypted instances |
| Disks | create empty, from image or snapshot, from source, regional disks, attach, resize, clone (including customer-managed encryption keys), local SSD, auto-delete change |
| Snapshots and images | create, delete, list, deprecation status, create from image or family |
| Networking | firewall rules, routes, custom hostnames, subnet-specific instance creation |
| Advanced | spot and preemptible VMs, preemption history, delete protection, bulk insert, pagination, request IDs, custom machine types, extra memory |
| Operations | `wait_for_extended_operation`, `operation_check`, `handle_extended_operation` |
| Tests | `test_*.py` files covering the above |

Each sample is a standalone script with a `create`, `get`, `list`, or `delete` function, plus a `main.py` or equivalent for CLI use. Use them as references, not as a single cohesive library.

## Installation

### Prerequisites

- Python 3.9 or later (confirm against `pyproject.toml`)
- A Google Cloud project with the Compute Engine API enabled
- An ElectricityMaps API token
- (Optional) CUDA-capable GPU for faster TCN inference

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/<ORG>/eco4cast-l2k_9zxr.git
cd eco4cast-l2k_9zxr

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
# or, if the project is packaged:
pip install -e .

# 4. For development and testing
pip install -r requirements-test.txt
```

## Configuration

Set the following environment variables. The names are inferred and should match the code.

| Variable | Purpose |
|---|---|
| `ELECTRICITYMAPS_API_TOKEN` | Authentication for the ElectricityMaps API |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to a service account JSON key |
| `GOOGLE_CLOUD_PROJECT` | Default Google Cloud project ID (`<PROJECT_ID>`) |
| `ECO4CAST_ZONE` | Default grid zone or country code, for example `DE` or `US-CAL-CISO` (inferred) |

`noxfile_config.py` holds settings for the nox test sessions, such as Python versions and environment variables used in tests.

Do not commit credentials or the API token. Use a `.env` file excluded by `.gitignore`, or a secrets manager.

## Usage

### Running the controller

```bash
python master_machine_main.py
```

This starts the master controller, which queries forecasts and manages worker VMs. Check the script's arguments with `--help` if it provides them.

### Running a worker VM

```bash
python vm_main.py
```

Run this on the Compute Engine instance that executes the workload.

### Forecasting directly

```python
from co2_model import CO2Model
from electricitymaps_api import ElectricityMapsClient

client = ElectricityMapsClient()           # reads ELECTRICITYMAPS_API_TOKEN
model = CO2Model(checkpoint="co2_model.ckpt")

history = client.get_carbon_intensity(zone="DE", hours=168)
forecast = model.predict(history, horizon_hours=24)
print(forecast)
```

*(The class and method names above are illustrative. Check the actual API in `co2_model.py` and `electricitymaps_api.py`.)*

### Using a Compute Engine sample

```bash
python gce_samples/instances/create.py \
    --project <PROJECT_ID> \
    --zone us-central1-a \
    --instance-name demo-vm
```

Samples follow the upstream conventions. Run `python <script>.py --help` to see the arguments.

### Notebooks

- **`local_quick_start_guide.ipynb`**: runs the forecasting pipeline locally, without Google Cloud.
- **`quick_start_guide.ipynb`**: covers the full pipeline, including VM creation and migration.

Start with the local guide.

## Testing

Tests use `pytest`, and `nox` orchestrates sessions.

```bash
# Run the full test suite
pytest tests/

# Run a single test file
pytest tests/test_instance_start_stop.py -v

# Run through nox
nox -s tests
```

Compute Engine tests create real resources and incur charges. Run them in a dedicated test project and clean up afterward. Some tests may be skipped unless the corresponding environment variables are set.

## Troubleshooting

- **`403 Forbidden` from Compute Engine:** Confirm the service account has the `Compute Instance Admin` and `Compute Network Admin` roles, and that the Compute Engine API is enabled.
- **ElectricityMaps returns `401`:** Check the token and its rate limits.
- **Checkpoint loading errors:** Make sure the PyTorch version matches the one used to save `co2_model.ckpt`.
- **Operations hang:** Use `wait_for_extended_operation` with a timeout, and check the operation status in the Cloud Console.

## Limitations and Open Questions

- The purpose of `sgs.py`, `test_sgs.py`, and the `.pytest` files is unclear from the file names.
- The `gce_samples` tree appears to be vendored from upstream samples. Keep track of the upstream commit it was copied from, and update it when the API changes.
- Some sample files and directories are duplicated in the listing.
- The forecasting accuracy, supported regions, and evaluation metrics are not documented in the file list. Add these once the model documentation is available.

## Contributing

1. Fork the repository and create a feature branch.
2. Install the test requirements and run `nox` before opening a pull request.
3. Follow the existing style. Format with `black` and check with `flake8` if configured in `pyproject.toml`.
4. Do not commit credentials, API tokens, or large model artifacts beyond the existing checkpoint.

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file. Vendored Compute Engine samples may carry their own Apache 2.0 license headers from the upstream project.

## Acknowledgements

- The Eco4Cast initiative
- ElectricityMaps, for carbon intensity data
- Google Cloud, for the Compute Engine API samples
- Authors of the Temporal Convolutional Network architecture (Bai, Kolter, and Koltun, 2018)
