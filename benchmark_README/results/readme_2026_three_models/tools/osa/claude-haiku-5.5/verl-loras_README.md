# verl-loras-5bfh1u5r

---

[![PyPi](https://badge.fury.io/py/verl.svg)](https://badge.fury.io/py/verl)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![numpy](https://img.shields.io/badge/NumPy-013243.svg?style={0}&logo=NumPy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style={0}&logo=pandas&logoColor=white)
![ray](https://img.shields.io/badge/Ray-028CF0.svg?style={0}&logo=Ray&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

verl (Volcano Engine Reinforcement Learning for LLMs) is a Python framework for reinforcement-learning post-training of large language models. It is intended for ML researchers and ML infrastructure engineers who run LLM post-training on GPU clusters, including multi-node Ray and Slurm deployments. Developers who extend training algorithms, rollout backends, or model adapters are a secondary audience. The repository provides example workflows for reinforcement-learning and supervised fine-tuning methods, and training is launched through a module entry point. For runnable steps, see the Getting Started section.

---

## Core Features

- **RL post-training for LLMs:** Provides ready-to-run recipes for reinforcement-learning post-training of language models, including PPO, GRPO, RLOO, ReMax, and supervised fine-tuning, so you can compare or switch advantage estimators with configuration changes.
- **Multi-node distributed execution on Ray:** Coordinates training across multiple nodes through a Ray head and worker setup, with example launch scripts for multi-node runs and Slurm, so large runs can scale beyond a single machine.
- **Pluggable rollout backends:** Supports vLLM and SGLang for generating responses during training, letting you select the inference engine that fits your hardware and throughput needs.
- **FSDP-based actor training with memory offload options:** Trains actor and reference models with FSDP and exposes per-model settings to offload parameters or optimizer state, helping you fit larger models on limited GPU memory.
- **Standard data exchange between components:** Uses a common batch and metadata structure to pass data between training stages, giving developers a consistent interface when adding algorithms, rollout backends, or model adapters.

---

## Installation

**Prerequisites:** requires Python >=3.8

Install verl-loras-5bfh1u5r using one of the following methods:

**Using PyPi:**

```sh
pip install verl
```

---

## Getting Started

### Prerequisites

- Python 3.10, as used in the install steps in `docs/README_vllm0.8.md`. `pyproject.toml` requires Python `>=3.8`.
- GPU nodes for training and rollout. The example's `trainer.n_gpus_per_node=1` and `trainer.nnodes=2` settings assume two nodes with one GPU each. Adjust these for your cluster.
- A local model directory. Set `MODEL_PATH` to its location.
- Training and validation data as Parquet files at `$HOME/data/gsm8k/train.parquet` and `$HOME/data/gsm8k/test.parquet`.
- Ray, which is installed as a dependency (`ray[default]>=2.10`).

### Steps

1. Create and activate a conda environment:

```bash
conda create -n verl python==3.10
conda activate verl
```

2. Clone the repository and install verl in editable mode:

```bash
git clone https://github.com/volcengine/verl.git
cd verl
pip3 install -e .
```

3. Install vLLM and flash-attn. Follow the version-specific instructions in `docs/README_vllm0.8.md`.

4. Start the Ray head node and submit the example GRPO job. Run this from the repository root, because the `--runtime-env` path is relative. The path `verl/trainer/runtime_env.yaml` is taken from `run_master.sh`. Confirm that the file exists in your checkout before running. Replace the `MODEL_PATH` placeholder with your model directory:

```bash
ray start --head --port=6379

MODEL_PATH=/path/to/your/model  # placeholder: replace with your model directory
HOST_IP="$(hostname -I)"

RAY_ADDRESS="http://${HOST_IP}:6379" ray job submit \n    --runtime-env=verl/trainer/runtime_env.yaml \n    --no-wait \n    -- \n    python3 -m verl.trainer.main_ppo \n    algorithm.adv_estimator=grpo \n    data.train_files=$HOME/data/gsm8k/train.parquet \n    data.val_files=$HOME/data/gsm8k/test.parquet \n    data.train_batch_size=1024 \n    data.max_prompt_length=512 \n    data.max_response_length=1024 \n    data.filter_overlong_prompts=True \n    data.truncation='error' \n    actor_rollout_ref.model.path=$MODEL_PATH \n    actor_rollout_ref.actor.optim.lr=1e-6 \n    actor_rollout_ref.model.use_remove_padding=True \n    actor_rollout_ref.actor.ppo_mini_batch_size=256 \n    actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=40 \n    actor_rollout_ref.actor.use_kl_loss=True \n    actor_rollout_ref.actor.kl_loss_coef=0.001 \n    actor_rollout_ref.actor.kl_loss_type=low_var_kl \n    actor_rollout_ref.actor.entropy_coeff=0 \n    actor_rollout_ref.model.enable_gradient_checkpointing=True \n    actor_rollout_ref.actor.fsdp_config.param_offload=False \n    actor_rollout_ref.actor.fsdp_config.optimizer_offload=False \n    actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=40 \n    actor_rollout_ref.rollout.tensor_model_parallel_size=2 \n    actor_rollout_ref.rollout.name=vllm \n    actor_rollout_ref.rollout.gpu_memory_utilization=0.6 \n    actor_rollout_ref.rollout.n=5 \n    actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=40 \n    actor_rollout_ref.ref.fsdp_config.param_offload=True \n    algorithm.use_kl_in_reward=False \n    trainer.critic_warmup=0 \n    trainer.logger=['console','wandb'] \n    trainer.project_name='verl_grpo_example_gsm8k' \n    trainer.experiment_name='qwen2_7b_function_rm' \n    trainer.n_gpus_per_node=1 \n    trainer.nnodes=2 \n    trainer.save_freq=-1 \n    trainer.test_freq=5 \n    trainer.total_epochs=15
```

For the two-node layout, start each worker node with `run_worker.sh`. Set `MASTER_ADDR` to the head node's hostname or IP before running it.

---

## Architecture

verl is a Ray-based, modular framework for reinforcement-learning post-training of LLMs. Its main subsystems are the controller, workers, model adapters, and data protocol.

- **Control and orchestration:** `verl/single_controller` (with `base` and `ray` submodules) coordinates workers. Multi-node runs start a Ray head node and join workers to it (`run_master.sh`, `run_worker.sh`), then submit the training entry point `verl.trainer.main_ppo` as a Ray job.
- **Workers:** `verl/workers` is split into `actor`, `critic`, `rollout`, `reward_model`, `reward_manager`, and `sharding_manager`.
- **Rollout backends:** vLLM is selected with `actor_rollout_ref.rollout.name=vllm`, using `verl/workers/rollout/vllm_rollout` and the version-specific shims under `verl/third_party/vllm`. SGLang rollout lives under `verl/workers/rollout/sglang_rollout`. A `naive` rollout is also present under `verl/workers/rollout/naive`.
- **Training backends:** FSDP is configured through `fsdp_config` settings in the example launch script. Megatron-related adapters are under `verl/models/*/megatron` and `verl/models/mcore`.
- **Model adapters:** `verl/models` contains per-model adapters for Llama, Qwen2, and Transformers-based models.
- **Data exchange:** `verl/protocol.py` defines `DataProto`, a standard container that pairs a `TensorDict` batch with `non_tensor_batch` and `meta_info` for data exchange between functions and modules.
- **Algorithm recipes:** `recipe/` (`dapo`, `prime`, `r1`) holds algorithm-specific configuration.

---

## Examples

Examples of how this should work and how it should be used are available [here](./examples).

---

## Documentation

A detailed verl-loras-5bfh1u5r description is available [here](./docs).

---

## Contributing

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). verl-loras-5bfh1u5r repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{verl-loras-5bfh1u5r,

        author = {README Benchmark},

        title = {verl-loras-5bfh1u5r repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---