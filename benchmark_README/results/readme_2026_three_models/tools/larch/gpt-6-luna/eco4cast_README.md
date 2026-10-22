# eco4cast-jv_ycof3

A Python project for exploring carbon-aware forecasting and scheduling. The repository includes CO₂ forecasting components, electricity and weather data utilities, controller and VM-related scripts, notebooks, and a large collection of Google Cloud Compute Engine examples.

> **Note:** This README is based on the files present in the repository. Exact command-line options, configuration keys, and supported Python versions should be confirmed in the source code and project configuration before use.

## Contents

- [Project overview](#project-overview)
- [Repository layout](#repository-layout)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration and credentials](#configuration-and-credentials)
- [Getting started](#getting-started)
- [Tests](#tests)
- [Data and model artifacts](#data-and-model-artifacts)
- [Google Cloud examples](#google-cloud-examples)
- [Security and operational notes](#security-and-operational-notes)
- [License](#license)

## Project overview

The repository appears to bring together two related areas:

1. **Carbon-aware forecasting and scheduling**
   - CO₂ model code and a saved model checkpoint
   - An Electricity Maps API integration
   - Interval prediction and weather-data utilities
   - A master machine controller and scheduler-related code

2. **Google Cloud VM and disk examples**
   - Scripts for creating, starting, stopping, and managing Compute Engine instances
   - Examples for disks, images, snapshots, templates, networking, and encryption
   - Tests and support utilities for those examples

The top-level scripts and notebooks are likely the most useful places to begin exploring the forecasting and scheduling workflow. The numerous cloud-operation scripts appear to include standalone examples; they may not all be required by the core forecasting code.

## Repository layout

Important files and directories include:

| Path | Purpose |
|---|---|
| `co2_model.py` | CO₂ modelling code |
| `co2_model.ckpt` | Saved model checkpoint |
| `electricitymaps_api.py` | Electricity Maps API integration |
| `interval_predictor.py` | Interval prediction logic |
| `weather_data_utils.py` | Weather-data utilities |
| `master_machine_controller.py` | Master-machine or scheduling controller |
| `master_machine_main.py` | Master-machine entry-point script |
| `vm_main.py` | VM-side entry-point script |
| `utils.py` | Shared utilities |
| `smart_scheduler_concept.py` | Scheduler concept or prototype |
| `country_points.pickle` | Serialized data artifact; see the security notes below |
| `quick_start_guide.ipynb` | Quick-start notebook |
| `local_quick_start_guide.ipynb` | Local quick-start notebook |
| `experimental_recipe.pytest` | Experimental or test-related file; check its contents before running |
| `requirements.txt` | Runtime dependency list |
| `requirements-test.txt` | Test dependency list |
| `pyproject.toml` | Python project and tooling configuration |
| `noxfile_config.py` | Nox-related configuration |
| `LICENSE` | License text |

The repository also contains many Google Cloud examples, including files for VM instances, disks, images, snapshots, routes, and operations. Their paths and package structure should be inspected before using them; not every example is necessarily part of the forecasting application.

## Requirements

- Python version: check `pyproject.toml` and the dependency files for the version expected by this checkout.
- Python packages: listed in `requirements.txt`; additional test dependencies are listed in `requirements-test.txt`.
- Optional external services: the forecasting and cloud-related code may require API credentials or Google Cloud configuration.

## Installation

Clone the repository and create an isolated environment:

```bash
git clone <repository-url>
cd eco4cast-jv_ycof3

python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install the declared dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For development or testing, install the test dependencies as well:

```bash
python -m pip install -r requirements-test.txt
```

If `pyproject.toml` defines an installable package, editable installation may also be available:

```bash
python -m pip install -e .
```

Check the project configuration first if editable installation fails.

## Configuration and credentials

Some components may access external APIs or Google Cloud. Before running them:

1. Read the relevant module and entry-point source to identify required settings, environment variables, and command-line arguments.
2. Provide API tokens and cloud credentials using the mechanism supported by that code.
3. Do not commit credentials, private keys, or local configuration files to the repository.

The presence of `electricitymaps_api.py` suggests that some workflows may use the Electricity Maps service. The exact token name, endpoints, and required plan or permissions are not specified by the file listing; verify them in the module before configuring a run.

Google Cloud examples generally require a configured Google Cloud project and credentials. Follow the authentication method documented by the specific example and the Google Cloud SDK for your environment.

## Getting started

A reasonable exploration order is:

1. Review `pyproject.toml`, `requirements.txt`, and `requirements-test.txt`.
2. Read `README.md` files in subdirectories, where present.
3. Open `quick_start_guide.ipynb` or `local_quick_start_guide.ipynb` in Jupyter.
4. Trace the forecasting workflow through `co2_model.py`, `electricitymaps_api.py`, `interval_predictor.py`, and `weather_data_utils.py`.
5. Inspect `master_machine_main.py` and `vm_main.py` before running them, especially for required arguments or cloud side effects.

To launch Jupyter after installing an appropriate Jupyter package:

```bash
jupyter notebook
```

Then open one of the quick-start notebooks from the repository. Notebook dependencies may not all be included in `requirements.txt`; install any additional packages indicated by the notebook.

The entry-point scripts may require arguments or cloud resources. Check their usage before running them:

```bash
python master_machine_main.py --help
python vm_main.py --help
```

If a script does not implement `--help`, inspect its source for configuration and execution requirements.

## Tests

Run the test suite with:

```bash
pytest
```

The repository contains tests for forecasting-related code and a large number of cloud sample operations. Some cloud tests may require credentials, an accessible project, permissions, or billable resources. Review the tests before running the full suite.

For a local-only check, first identify the tests that do not contact external services or modify cloud resources, then run selected tests by path:

```bash
pytest path/to/test_file.py
```

## Data and model artifacts

- `co2_model.ckpt` is a saved model artifact. The model code must be compatible with the framework and model definition used to create it.
- `country_points.pickle` is a Python pickle file. Only load it if you trust its origin: unpickling data from an untrusted source can execute arbitrary code.
- Other data files may be generated or downloaded by scripts or notebooks. Check their source and expected location before deleting or replacing them.

Do not assume that the checkpoint or other artifacts are current, portable across framework versions, or suitable for production without validating them.

## Google Cloud examples

The repository includes a substantial set of scripts with names such as `create.py`, `delete.py`, `start.py`, `stop.py`, and `create_from_snapshot.py`. These appear to demonstrate Google Cloud Compute Engine operations.

Treat these as operational examples rather than harmless local utilities:

- Creating resources can incur cloud charges.
- Deleting resources can permanently remove data.
- Scripts may use project, zone, region, or resource values defined in code or environment configuration.
- Review each script and its associated tests before executing it.
- Use a non-production project and disposable resources when experimenting.

The examples may reflect different versions or styles of the Google Cloud client libraries. Check their individual dependencies and documentation.

## Security and operational notes

- Keep API tokens and cloud credentials out of source control.
- Review scripts before running code that creates, modifies, or deletes cloud resources.
- Validate model inputs, outputs, and forecasts before using them to make operational decisions.
- Treat pickle files as trusted-code artifacts, not as a safe interchange format for untrusted data.
- Confirm the external service terms, quotas, and permissions relevant to your use.

## License

See [`LICENSE`](LICENSE) for the license terms applicable to this repository.
