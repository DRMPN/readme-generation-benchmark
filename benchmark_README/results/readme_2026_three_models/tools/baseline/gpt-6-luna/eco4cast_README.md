# eco4cast

`eco4cast` is a Python package for reducing carbon emissions while training neural networks. It predicts carbon-intensity trends for supported Electricity Maps zones, uses those predictions to schedule training intervals, and can optionally move a Google Cloud virtual machine between zones. Its resumable training workflow is designed to let model training pause and continue across separate time windows without discarding progress.

The project supports two approaches:

- **Local training:** schedule work on your own machine during lower-carbon intervals.
- **Google Cloud training:** coordinate a remote VM over SSH and move it between configured Google Cloud zones as scheduled.

The repository includes MNIST and ImageNet examples, quick-start notebooks, a bundled CO₂ prediction checkpoint, and Google Compute Engine client-library samples.

## How it works

`CO2Predictor` gathers recent weather data and carbon-intensity history, then uses a bundled PyTorch Lightning model to forecast carbon intensity for supported zones. `IntervalGenerator` turns those forecasts into intervals based on an emissions threshold and scheduling options.

For model training, `IntervalTrainer` uses Lightning Fabric, a resumable sampler, and saved state to pause and resume training across scheduled intervals. It can also track energy use and emissions through `eco2ai`.

For Google Cloud workflows, `Controller` starts training on a remote VM over SSH and can call `google_cloud_move_vm` to recreate the VM in another zone using a disk snapshot. The Compute Engine client library also contains samples for managing instances, disks, images, snapshots, firewalls, routes, and related resources.

## Requirements

The package metadata specifies Python `^3.9` and these direct dependencies:

- PyTorch `^2.0.1` and Lightning `^2.0.2`
- APScheduler `^3.10.1`
- eco2ai `^0.3.9`
- Paramiko `^3.2.0`
- NumPy `>=1.23.5` and pandas `>=1.4.3`
- scikit-learn `^1.2.2`
- google-cloud-compute `^1.11.0`

The examples may need additional libraries such as `torchvision`, which their notebooks install separately.

## Installation

Install the published package from PyPI:

```bash
python -m pip install eco4cast
```

Or install from a local checkout:

```bash
git clone https://github.com/AIRI-Institute/eco4cast.git
cd eco4cast
python -m pip install .
```

For notebook-based local examples, install `torchvision` as well:

```bash
python -m pip install torchvision
```

## Configuration and credentials

### Electricity Maps

Carbon-intensity history is requested from the Electricity Maps API. Obtain an API key and pass it to `CO2Predictor` as `electricity_maps_api_key`. The project’s examples require an Electricity Maps account; the notebooks note that free-tier access may be limited to non-commercial use.

Do not commit API keys to source code. The example scripts contain key-shaped values in their configuration; replace those with your own securely managed credentials.

`CO2Predictor` accepts optional `checkpoint_file_path`, `include_zones`, and `exclude_zones` arguments. If no checkpoint path is supplied, it loads the bundled `co2_model.ckpt`. Supported zone codes are defined in `eco4cast/master_machine/utils.py`; they include `BR-CS`, `CA-ON`, `CH`, `DE`, `PL`, `BE`, `IT-NO`, `CA-QC`, `ES`, `GB`, `FI`, `FR`, and `NL`.

`IntervalGenerator` can be configured with `max_emission_value`, `co2_delta_to_move`, `min_interval_size`, `max_window_size`, and optional included or excluded zones. These settings influence the emission threshold, the minimum improvement needed to switch zones, and the intervals considered.

### Google Cloud

Google Cloud operations use Application Default Credentials. The Compute Engine samples recommend setting up credentials with:

```bash
gcloud auth application-default login
```

Alternatively, set `GOOGLE_APPLICATION_CREDENTIALS` to the path of a credentials file. The `Controller` also accepts a `credentials_path` and sets this environment variable when initialized.

Cloud use requires a Google Cloud project and suitable permissions for the operations you intend to perform. The controller additionally needs working SSH access to the VM, including its username, IP address, port, Python executable, and training-script path. The example scripts show these as values to configure for your own environment; they are not ready-to-use project or VM settings.

## Usage

### Local scheduled training

The local quick-start notebook is `examples/eco4cast_local_demo/local_quick_start_guide.ipynb`. It demonstrates training an MNIST model on a machine located in a supported zone. The guide’s prerequisites include an Electricity Maps account and hardware in one of the supported zones.

A typical workflow is to create a model and datasets, then pass them to `IntervalTrainer` with a loss function and metric:

```python
from eco4cast.virtual_machine.smart_scheduler_concept import IntervalTrainer

trainer = IntervalTrainer(
    model=model,
    train_dataset=train_dataset,
    val_dataset=val_dataset,
    loss_function=loss_function,
    metric_func=metric_func,
)
```

For ordinary training, call `trainer.train()` without intervals. To train during chosen windows, pass UTC datetime interval pairs to `trainer.train(...)`. The trainer can save and reload state between intervals using its `load_states` option. See the MNIST example or local notebook for a complete model-and-dataset setup.

For forecast-based scheduling, the package provides `CO2Predictor`, `IntervalGenerator`, and `IntervalTrainer.train_using_predictor(...)`. The Google Cloud examples show how these components are assembled.

### Google Cloud training

Start with `examples/eco4cast_demo/quick_start_guide.ipynb`, which walks through the Google Cloud workflow. The example structure separates responsibilities:

- `master_machine_main.py` configures a `Controller`, a predictor, and an interval generator.
- `vm_main.py` defines the training model, datasets, callbacks, and `IntervalTrainer`.

The master controller sends time-window arguments to the VM script over SSH. For zone changes, it snapshots the VM’s disk and creates a replacement VM in the destination zone. Cloud actions can create, delete, or move resources and may incur charges; review and adapt the examples before running them.

The `examples/README.md` also describes MNIST and ImageNet Google Cloud examples. Dataset paths and remote VM configuration must match your environment.

## Development

The Compute Engine samples are organized into `ingredients`, `recipes`, and generated `snippets`. Edit ingredients or recipes rather than generated snippets. From `eco4cast/master_machine/compute/client_library`, regenerate snippets with:

```bash
python3 sgs.py generate
```

The generator writes output under `snippets` by default. Review and commit generated changes yourself; the script does not interact with Git.

The root project uses Poetry metadata in `pyproject.toml` and `poetry-core` as its build backend. The repository also includes built wheel and source distribution artifacts under `dist/`.

## Testing

The Compute Engine client library specifies test and sample dependencies in:

- `eco4cast/master_machine/compute/client_library/requirements-test.txt`
- `eco4cast/master_machine/compute/client_library/requirements.txt`

Its SGS tests can be run from the client-library directory after installing those requirements:

```bash
pytest test_sgs.py
```

These tests exercise snippet generation and check that generated snippets match their ingredient and recipe sources. The broader snippet test files cover Compute Engine operations; consult the relevant sample and test before running them, since cloud-oriented samples may require Google Cloud credentials and resources.

## License

The repository includes an Apache License 2.0 license in `LICENSE`. Some bundled Google Compute Engine sample files also carry Google LLC Apache 2.0 notices. When redistributing the project or derivative works, follow the applicable license terms and retain required notices.
