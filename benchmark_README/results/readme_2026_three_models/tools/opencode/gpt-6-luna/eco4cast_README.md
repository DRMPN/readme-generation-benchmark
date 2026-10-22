# eco4cast

`eco4cast` is a Python package for scheduling PyTorch model training around forecasted electricity carbon intensity. It can schedule training intervals on the local machine or coordinate training on Google Cloud virtual machines. Its package metadata describes the project as a tool for reducing CO₂ emissions during neural-network training; actual emissions and any savings depend on the workload, forecast, and infrastructure.

The package includes a bundled carbon-intensity forecasting model. `CO2Predictor` combines that model with recent Electricity Maps carbon-intensity history and weather data from Open-Meteo. `IntervalGenerator` turns forecasts into candidate time intervals. The `IntervalTrainer` can pause at interval boundaries, save training state, and resume later. For Google Cloud workflows, `Controller` can start training over SSH and move a VM between configured zones.

## Installation

The package requires Python 3.9 or newer and declares PyTorch, Lightning, APScheduler, eco2AI, Paramiko, NumPy, pandas, scikit-learn, and Google Cloud Compute among its dependencies.

Install the published package:

```bash
python -m pip install eco4cast
```

Or install this repository from its root directory:

```bash
python -m pip install .
```

The MNIST and ImageNet examples also use `torchvision`, which is not listed among the package dependencies, so install it separately when running those examples:

```bash
python -m pip install torchvision
```

## Usage

### Schedule local training

Create an `IntervalTrainer` with your PyTorch model, training and validation datasets, loss function, and metric function. To schedule training using the carbon-intensity forecast, provide an Electricity Maps API key and call `train_using_predictor`:

```python
from eco4cast.master_machine.interval_predictor import (
    CO2Predictor,
    IntervalGenerator,
)
from eco4cast.virtual_machine.smart_scheduler_concept import IntervalTrainer

# Build your model, datasets, and IntervalTrainer first.
trainer = IntervalTrainer(
    model=model,
    train_dataset=train_dataset,
    val_dataset=val_dataset,
    loss_function=loss_function,
    metric_func=metric_func,
)

predictor = CO2Predictor(electricity_maps_api_key="YOUR_ELECTRICITY_MAPS_API_KEY")
trainer.train_using_predictor(predictor, IntervalGenerator())
```

`IntervalTrainer.train()` can also be used without a forecast for uninterrupted training, or with explicit UTC datetime intervals. Training state is written to `fabric_checkpoint.ckpt` when an interval ends; the trainer accepts `load_states=True` when resuming. Emissions tracking writes to `emission.csv` using eco2AI.

### Google Cloud training

The Google Cloud workflow uses a controller process and a VM process:

1. Configure Google Cloud credentials, a VM, and SSH access.
2. Install `eco4cast` and your training dependencies on the VM, and make your VM-side training script available there.
3. On the controller machine, create a `CO2Predictor`, an `IntervalGenerator`, and a `Controller` configured with your credentials path, SSH connection details, VM and project details, and prediction period.
4. Call `controller.start_training()` to run the scheduled workflow. The example then calls `controller.stop_training()` to stop the instance when training is complete.

See the [Google Cloud quick-start notebook](examples/eco4cast_demo/quick_start_guide.ipynb) and the [MNIST Google Cloud example](examples/MNIST_google_cloud/) for working examples. Google Cloud credentials, enabled services, permissions, SSH connectivity, and applicable cloud charges are managed by the user; they are not supplied by this package.

## Forecast zones

The package currently defines these zones for forecasting and interval planning:

| Electricity Maps zone | Region |
| --- | --- |
| `BR-CS` | Central Brazil |
| `CA-ON` | Canada Ontario |
| `CH` | Switzerland |
| `DE` | Germany |
| `PL` | Poland |
| `BE` | Belgium |
| `IT-NO` | North Italy |
| `CA-QC` | Canada Quebec |
| `ES` | Spain |
| `GB` | Great Britain |
| `FI` | Finland |
| `FR` | France |
| `NL` | Netherlands |

For Google Cloud operation, the repository also maps these zones to Google Cloud Compute zones. The actual VM regions and available resources must suit your project and workload.

## Examples and documentation

- [Examples overview](examples/README.md)
- [Local MNIST quick-start notebook](examples/eco4cast_local_demo/local_quick_start_guide.ipynb)
- [Google Cloud MNIST quick-start notebook](examples/eco4cast_demo/quick_start_guide.ipynb)
- [MNIST Google Cloud scripts](examples/MNIST_google_cloud/)
- [ImageNet Google Cloud scripts](examples/ImageNet_google_cloud/)

The local notebook describes using a machine in one of the supported regions. The Google Cloud notebook walks through its cloud setup. Review the relevant tutorial before running either workflow, and provide your own Electricity Maps API key and infrastructure credentials where required.

## License

This project is distributed under the [Apache License 2.0](LICENSE).
