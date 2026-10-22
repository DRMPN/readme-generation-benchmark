# MiniGPT-4 and MiniGPT-v2

MiniGPT-4 and MiniGPT-v2 are vision-language models that connect image understanding with large language models. This repository contains model implementations, demos, training and evaluation scripts, dataset loaders, and configuration files for both projects.

- **MiniGPT-4** is designed for image-grounded conversations and visual question answering.
- **MiniGPT-v2** extends the project toward a unified interface for vision-language tasks, including recognition, grounding, and question answering.

![Project overview](overview.png)

> **Important:** Running a model requires the appropriate pretrained model checkpoints and, depending on the configuration, access to the corresponding language-model weights. The code in this repository does not necessarily include those weights. See [Model weights](#model-weights) before starting.

## Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Model weights](#model-weights)
- [Run a demo](#run-a-demo)
- [Training and fine-tuning](#training-and-fine-tuning)
- [Evaluation](#evaluation)
- [Datasets and configuration](#datasets-and-configuration)
- [Repository layout](#repository-layout)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Requirements

The project uses Python and PyTorch and is intended to run with a CUDA-capable GPU. The required Python packages and environment setup are listed in `environment.yml`.

Memory requirements depend on the selected model, language model, image resolution, batch size, and inference settings. Use a GPU with sufficient VRAM for the checkpoint you intend to run; quantization or other memory-saving options are not guaranteed to be available in every configuration.

## Installation

Clone the repository and create the supplied Conda environment:

```bash
git clone <repository-url>
cd MiniGPT-4
conda env create -f environment.yml
conda activate minigpt4
```

If the environment name differs from `minigpt4`, use the name shown in `environment.yml`.

For distributed training or evaluation, install a compatible CUDA-enabled PyTorch build and verify that your system’s CUDA runtime, NVIDIA driver, and PyTorch versions work together. The exact setup depends on your hardware and the environment file.

## Model weights

The repository contains model definitions and YAML configurations, but model checkpoints are typically distributed separately. Obtain the required weights from the project’s official release or model source and follow the applicable model terms.

Before launching a demo or training run:

1. Identify which model and language-model variant you plan to use.
2. Open its YAML configuration and find the checkpoint and model-path settings.
3. Download the required files and update the configuration paths accordingly.
4. Confirm that you have access to the language-model weights specified by that configuration.

Configurations in this project include variants for MiniGPT-4, MiniGPT-4 with LLaMA 2, and MiniGPT-v2. These variants are not interchangeable: use checkpoints and configuration files intended for the same model variant.

> **License note:** Base-model weights and third-party components may have terms that differ from this repository’s code license. Review the applicable terms before downloading, using, or redistributing them.

## Run a demo

The repository provides separate demo scripts for MiniGPT-4 and MiniGPT-v2. From the repository root, try the corresponding command:

```bash
python demo.py --cfg-path eval_configs/minigpt4_eval.yaml --gpu-id 0
```

```bash
python demo_v2.py --cfg-path eval_configs/minigptv2_eval.yaml --gpu-id 0
```

If configuration files are stored in a different directory in your checkout, pass their actual paths. The YAML configuration must point to the model checkpoints available on your machine.

The demos provide an interactive way to ask questions about an image. Depending on the model and interface, conversation behavior and supported task prompts may vary. Example images and demo materials are included in the repository.

For other MiniGPT-4 variants, use the matching configuration, such as the LLaMA 2 evaluation configuration, rather than reusing the MiniGPT-v2 configuration.

## Training and fine-tuning

Training entry points and example configurations are included in the repository:

- `train.py` — training entry point.
- `MiniGPT4_Train.md` and `MiniGPTv2_Train.md` — training instructions.
- `README_1_STAGE.md` and `README_2_STAGE.md` — additional stage-specific guidance.
- `README_MINIGPTv2_FINETUNE.md` — MiniGPT-v2 fine-tuning guidance.
- `minigpt4_stage1_pretrain.yaml` and `minigpt4_stage2_finetune.yaml` — MiniGPT-4 training configurations.
- `minigpt4_llama2_stage1_pretrain.yaml` and `minigpt4_llama2_stage2_finetune.yaml` — LLaMA 2 variant configurations.
- `minigptv2_finetune.yaml` — MiniGPT-v2 fine-tuning configuration.

Training generally requires more GPU memory and storage than inference. Before starting:

1. Read the training guide for the model variant and training stage.
2. Check the YAML configuration for dataset locations, pretrained model paths, output directories, and optimization settings.
3. Prepare the datasets and annotations expected by that configuration.
4. Adjust batch size and distributed-training settings to match your available hardware.

A typical distributed launch has the following form; use the configuration path and options appropriate to your checkout and hardware:

```bash
torchrun --nproc_per_node=1 train.py --cfg-path <training-config.yaml>
```

For the supported settings and arguments, consult the training documentation and the script’s help output:

```bash
python train.py --help
```

The repository also contains `convert_laion.py` and `convert_cc_sbu.py` for converting relevant training data. Review those scripts and the training documentation before preparing large datasets.

## Evaluation

Evaluation scripts and configurations are provided for visual question answering, referring expressions, and other tasks:

- `eval_vqa.py` — VQA evaluation entry point.
- `eval_ref.py` — referring-expression evaluation entry point.
- `minigpt4_eval.yaml`, `minigptv2_eval.yaml`, and `minigpt4_llama2_eval.yaml` — evaluation configurations.
- `minigptv2_benchmark_evaluation.yaml` — MiniGPT-v2 benchmark configuration.
- `EVAL_README.md` — evaluation instructions.

Evaluation datasets are not necessarily bundled with the code. Download and prepare the datasets required by the task, then update the relevant YAML files with their paths.

Because command-line options can depend on the task and configuration, check the scripts’ help output and `EVAL_README.md` before running an evaluation:

```bash
python eval_vqa.py --help
python eval_ref.py --help
```

Use the configuration and dataset format intended for the benchmark you want to run. Results from different model variants or evaluation settings may not be directly comparable.

## Datasets and configuration

Dataset loading and preprocessing code is organized around dataset classes and builders. The repository includes support for data sources and tasks such as:

- Image-text pairs and captions.
- Visual question answering.
- OCR-oriented question answering.
- Referring expressions and visual grounding.
- Conversation and instruction data.
- COCO, Visual Genome, Flickr, GQA, A-OKVQA, TextCaps, and related datasets.

Configuration files describe model variants, datasets, processors, tasks, and training or evaluation settings. Before running a configuration, verify that:

- Dataset files exist at the configured paths.
- The dataset format matches the corresponding loader.
- Checkpoint paths refer to the correct model variant.
- Output paths are writable and have enough disk space.

Dataset availability, access requirements, and licenses are determined by the individual dataset providers, not by this repository.

## Repository layout

The project is organized into several main areas:

| Area | Purpose |
|---|---|
| `demo.py`, `demo_v2.py` | Interactive demos for MiniGPT-4 and MiniGPT-v2 |
| `train.py` | Training entry point |
| `eval_vqa.py`, `eval_ref.py` | Evaluation entry points |
| Model modules | MiniGPT model implementations and supporting vision, language, and Q-Former components |
| Dataset modules | Dataset definitions, data utilities, and dataset builders |
| Processor modules | Image and text preprocessing |
| Task and runner modules | Training and evaluation task orchestration |
| YAML files | Model, dataset, training, and evaluation configurations |
| `MiniGPT4_Train.md`, `MiniGPTv2_Train.md`, `EVAL_README.md` | Training and evaluation documentation |

## Troubleshooting

### A checkpoint or model path cannot be found

Open the YAML file passed to the script and check its model and checkpoint paths. Download the appropriate checkpoint and update the configuration before running the command.

### A language model fails to load

Confirm that the language-model weights match the selected configuration and that you have the access required to download them. Check the configuration for the expected model location.

### CUDA out-of-memory errors

Try a smaller batch size or reduce other memory-intensive settings in the relevant configuration. If the issue occurs during inference, check whether the selected model variant and image settings fit your GPU.

### Dataset files are missing or have the wrong format

Check the dataset paths and expected annotation format in the configuration and dataset loader. Refer to `EVAL_README.md` or the relevant training guide for task-specific preparation instructions.

### The demo or evaluation command rejects an argument

Run the script with `--help` and use the arguments supported by the version in your checkout. Also confirm that the configuration path is correct.

## License

This repository includes `LICENSE.md` and `LICENSE_Lavis.md`. Review the applicable license files before using or redistributing the code. Third-party libraries, datasets, and pretrained model weights may be subject to separate terms.
