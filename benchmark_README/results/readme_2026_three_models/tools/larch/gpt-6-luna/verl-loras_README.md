# verl-loras

A distributed framework for training and evaluating large language models with reinforcement learning. This repository includes trainer implementations, rollout backends, data utilities, example launch scripts, and evaluation tools. It also includes a Qwen LoRA/PEFT example (`run_qwen_05_peft.sh`).

The codebase is organized around **verl**, a framework for running RL workflows across GPU workers. Depending on the configuration and installed dependencies, it supports components such as FSDP and Megatron workers, Ray-based orchestration, vLLM or SGLang rollouts, and algorithms including PPO, DAPO, and PRIME.

> **Hardware and dependencies matter.** Distributed training and inference require compatible GPU hardware and matching versions of PyTorch, CUDA, Ray, and the chosen rollout backend. Use the repository’s launch scripts and configuration files as the starting point for your environment.

## Contents

- [Overview](#overview)
- [Repository layout](#repository-layout)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running an example](#running-an-example)
- [LoRA / PEFT](#lora--peft)
- [Data preparation](#data-preparation)
- [Evaluation](#evaluation)
- [Configuration](#configuration)
- [Testing and development](#testing-and-development)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

A typical RL training run consists of:

1. Preparing training and validation data.
2. Loading a policy model and tokenizer.
3. Generating responses with a rollout backend.
4. Scoring responses with a reward function or reward model.
5. Updating the policy with the selected trainer and algorithm.
6. Saving checkpoints and evaluating the resulting model.

The repository contains several ways to configure these components. The `examples`-style launch scripts demonstrate particular combinations of model, algorithm, hardware layout, and backend. The YAML files define trainer, evaluation, and related settings. For a new run, start from the closest matching script and configuration rather than assembling a distributed command from scratch.

## Repository layout

The inventory includes the following major areas. Exact directory paths may vary by component; use the filenames in the repository to locate the corresponding files.

| Area | Representative files | Purpose |
|---|---|---|
| Training entry points | `main_ppo.py`, `main_dapo.py`, `main_prime.py`, `main_trainer.py` | Start PPO, DAPO, PRIME, or related training workflows. |
| Trainer implementations | `ray_trainer.py`, `dapo_ray_trainer.py`, `prime_ray_trainer.py` | Coordinate training, rollout, reward, and worker components. |
| Trainer configurations | `ppo_trainer.yaml`, `dapo_trainer.yaml`, `prime_trainer.yaml`, `evaluation.yaml` | Configure algorithms, models, workers, and evaluation. |
| Worker implementations | FSDP, Megatron, actor, critic, and worker-group modules | Run model training and related work across distributed workers. |
| Rollout backends | vLLM, SGLang, Hugging Face, and related rollout modules | Generate model responses during training or evaluation. |
| Data utilities | `rl_dataset.py`, `sft_dataset.py`, `rm_dataset.py`, `create_dataset.py`, `prepare_dapo_data.sh` | Load, prepare, and validate training and evaluation data. |
| Reward and evaluation | `reward_score.py`, `check_results.py`, `gsm8k.py`, `math.py`, `gpqa.py`, `livecodebench.py` | Score responses and evaluate on supported tasks. |
| Model conversion | `converter_hf_to_mcore.py`, `model_merger.py`, checkpoint utilities | Convert or merge model and checkpoint formats. |
| Example launch scripts | `run_*.sh`, `test_*.sh` | Provide runnable configurations for specific models and setups. |
| Documentation | `README.md`, `quickstart.rst`, `ppo.rst`, `ray_trainer.rst`, and other `.rst` files | Explain installation, configuration, training, and system design. |
| Tests | `test_*.py` | Exercise data, distributed workers, model operations, and integrations. |

## Requirements

Before installing, check the repository’s `pyproject.toml`, `setup.py`, requirements files, and the documentation for version-specific guidance.

In general, you will need:

- Python compatible with the project’s package metadata.
- PyTorch installed for your target accelerator and CUDA/ROCm version.
- A supported GPU environment for model training and rollout.
- Ray for distributed execution.
- A compatible rollout backend, such as vLLM or SGLang, if used by your chosen configuration.
- Access to the model weights and datasets required by the example.

Some dependencies are optional and backend-specific. Do not install every backend blindly: use the requirements file and instructions for the workflow you intend to run.

## Installation

Clone the repository, enter its root directory, and install the package in editable mode:

```bash
git clone <repository-url>
cd <repository-directory>

python -m pip install --upgrade pip
python -m pip install -e .
```

If the selected workflow requires extra dependencies, install those using the repository’s documented requirements files. For example, the inventory includes `requirements_sglang.txt`; consult it and the SGLang documentation before using an SGLang-backed run.

Verify that the package imports:

```bash
python -c "import verl; print('verl import OK')"
```

For a container-based setup, review the available Dockerfiles and choose one compatible with your GPU, CUDA version, and desired backend. The repository includes Dockerfiles for several environments, including vLLM, SGLang, Megatron, and ROCm.

## Running an example

### 1. Choose a launch script

Find a script that matches your model, algorithm, and hardware. Examples in the repository include scripts for Qwen, DeepSeek, and Gemma, as well as PPO, DAPO, PRIME, and evaluation workflows.

List the available scripts with:

```bash
find . -name 'run_*.sh' -o -name 'test_*.sh'
```

A script’s name is only a hint; read it before running. Check its model path, dataset paths, number of GPUs, distributed settings, and backend options.

### 2. Configure paths and resources

Edit the selected script or supply the settings it expects. In particular, check:

- Model and tokenizer locations.
- Training and validation dataset paths.
- Output and checkpoint directories.
- GPU count, node count, and distributed settings.
- Rollout backend and memory settings.
- Maximum prompt and response lengths.
- Logging configuration and run name.

Avoid launching a multi-GPU job until the model and data paths are valid and the requested resources are available.

### 3. Start the run

Run the chosen script from the repository environment:

```bash
bash path/to/run_example.sh
```

The script is the recommended source for the exact command-line options for that example. If you launch a Python entry point directly, use the configuration and arguments documented by the corresponding script and YAML file rather than assuming that all trainers accept the same options.

### 4. Monitor outputs

Check the console logs and configured tracking service for progress, rollout statistics, reward metrics, and checkpoint saves. Confirm that the run is writing to the intended output directory before starting a long job.

## LoRA / PEFT

The repository includes a LoRA-oriented Qwen example, `run_qwen_05_peft.sh`. Use it as the starting point for a parameter-efficient fine-tuning workflow:

1. Read the script and identify the model, data, and output paths it expects.
2. Confirm that the selected model and training configuration support the PEFT/LoRA options used by the script.
3. Install any additional PEFT-related dependencies required by that example.
4. Set the LoRA rank, target modules, and other adapter settings in the location used by the script or its configuration.
5. Run a small test first, then check that the expected adapter or checkpoint artifacts were saved.

LoRA support is configuration- and model-dependent. Do not assume that settings from one model’s example apply unchanged to another model, worker implementation, or checkpoint format.

## Data preparation

The repository provides dataset utilities and examples, including `create_dataset.py`, `data_process.py`, `prepare_dapo_data.sh`, and dataset classes such as `rl_dataset.py`, `sft_dataset.py`, and `rm_dataset.py`.

Before training:

- Review the data preparation instructions in the documentation and the relevant example script.
- Confirm that the dataset format matches the loader used by the selected trainer.
- Check that prompts, expected metadata, and any reward-related fields are present.
- Make sure train and validation data are separated as intended.
- Validate the input with a short run before launching a large distributed job.

Do not assume that every trainer uses the same schema. The required fields and serialization format depend on the dataset loader and workflow.

## Evaluation

Evaluation entry points and utilities include `main_eval.py`, `main_generation.py`, `check_results.py`, and task-specific modules such as `gsm8k.py`, `math.py`, `gpqa.py`, and `livecodebench.py`.

To evaluate a model:

1. Choose the evaluation script or launch script associated with the intended benchmark.
2. Set the model/checkpoint path, tokenizer, dataset, and generation settings.
3. Confirm that the evaluation configuration matches the model and backend.
4. Run a small sample first and inspect the generated output and score files.

Evaluation settings may differ from training settings, especially for generation limits, sampling, and reward or grading functions. See `evaluation.yaml` and the task-specific code for the relevant options.

## Configuration

Configuration is split between YAML files, Python entry points, and shell scripts. The inventory includes configurations for PPO, DAPO, PRIME, SFT, generation, and evaluation.

When adapting a configuration, verify at least:

- Algorithm and trainer implementation.
- Policy, reference, critic, or reward model settings, as applicable.
- Worker and GPU counts.
- Rollout backend and sampling settings.
- Batch sizes and gradient accumulation.
- Prompt and response length limits.
- Checkpoint, logging, and evaluation intervals.

The launch scripts show how configurations are combined for concrete workflows. When in doubt, follow a nearby working example and change one setting at a time.

## Testing and development

The repository includes many tests for components such as datasets, tensor utilities, model operations, worker groups, distributed execution, and backend integrations.

Run an individual test with:

```bash
python -m pytest path/to/test_file.py
```

Or run the test suite:

```bash
python -m pytest
```

Some tests require GPUs, Ray, external services, model files, or optional backends. Check a test’s requirements before running it in a minimal environment. The repository also includes helper scripts such as `run_test.sh`, `format.sh`, and `check_license.py`.

## Troubleshooting

- **Import or dependency errors:** Check the Python environment and install the dependencies required by the selected backend.
- **CUDA or device errors:** Verify that PyTorch, the accelerator runtime, and the installed drivers are compatible.
- **Ray worker failures:** Confirm that all nodes can reach the Ray cluster and that worker environments have the same code and dependencies.
- **Out-of-memory errors:** Reduce batch size, sequence lengths, rollout concurrency, or model size; also check backend-specific memory settings.
- **Missing model or data files:** Verify paths and access permissions on every worker node, not just the node that launches the job.
- **Checkpoint loading errors:** Confirm the checkpoint format expected by the selected model loader and worker implementation. Consult the checkpoint and model conversion documentation.
- **Unexpected evaluation results:** Check the dataset format, generation configuration, answer extraction, and task-specific grading code.

## License

See the repository’s `LICENSE` file for license terms and `Notice.txt` for applicable third-party notices.
