# verl

---

[![PyPI](https://badge.fury.io/py/verl.svg)](https://badge.fury.io/py/verl)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white)
![Transformers](https://img.shields.io/badge/Transformers-FFCA28.svg?style=flat&logo=Hugging%20Face&logoColor=white)
![Ray](https://img.shields.io/badge/Ray-028CF0.svg?style=flat&logo=Ray&logoColor=white)
![vLLM](https://img.shields.io/badge/vLLM-1F6FEB.svg?style=flat)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Testing](#testing)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

verl is a distributed reinforcement learning framework for training large language models, designed to express RL training pipelines as dataflows executed by coordinated distributed workers. It is intended for researchers and engineers working on RLHF and related LLM training workloads. The project provides a Python library for composing such pipelines, command-line entry points for launching multi-node training jobs, and worked examples covering common RL trainers and supervised fine-tuning flows. Newcomers should start with Getting Started for installation and a first runnable training run.

---

## Core Features

- **End-to-end RL training for LLMs**: Built-in trainers implement post-training algorithms such as PPO and GRPO, letting developers fine-tune models with reward-based supervision out of the box.
- **Distributed, multi-node execution**: Ray-based master/worker orchestration coordinates training across nodes and GPUs, enabling workloads to scale beyond a single machine.
- **Composable dataflow pipelines**: The HybridFlow design represents RL training as a dataflow of high-level operators connected by a unified batched data protocol, making it easier to customize or swap individual pipeline stages.
- **High-throughput rollout generation**: Integration with accelerated inference engines such as vLLM and SGLang speeds up the sampling-heavy rollout phase, reducing end-to-end training time.
- **Configurable memory and parallelism options**: FSDP parameter and optimizer offloading, gradient checkpointing, and tensor parallelism help fit large models onto constrained GPU memory.

---

## Installation

**Prerequisites:** requires Python 3.10 (the version used in the Getting Started example below)

Install verl using pip:

```sh
pip install verl
```

---

## Getting Started

Install verl with FSDP for training and vLLM for rollout, then run the bundled GRPO-on-GSM8K example. The steps below follow `docs/README_vllm0.8.md` and the scripts `run_master.sh` / `run_worker.sh`.

**Prerequisites**

- Python 3.10 (installed via conda below)
- CUDA-enabled NVIDIA GPU(s), required by vLLM and flash-attn
- A Ray cluster for the distributed example; the sample run uses 2 nodes (`trainer.nnodes=2`) with 1 GPU per node (`trainer.n_gpus_per_node=1`)

**1. Create and activate the environment**

```bash
conda create -n verl python==3.10
conda activate verl
```

**2. Install verl from source**

```bash
git clone https://github.com/volcengine/verl.git
cd verl
pip3 install -e .
```

**3. Install vLLM and flash-attn**

```bash
pip3 install vllm==0.8.3
pip3 install flash-attn --no-build-isolation
```

A pre-built Docker image for verl + vLLM 0.8.3 is also available: `docker pull hiyouga/verl:ngc-th2.6.0-cu126-vllm0.8.3-flashinfer0.2.2-cxx11abi0`.

**4. Prepare the example inputs**

Place the training/validation parquet files at `$HOME/data/gsm8k/train.parquet` and `$HOME/data/gsm8k/test.parquet`, and point `MODEL_PATH` at the model to train (the bundled script uses `Qwen2.5-Math-1.5B`).

**5. Start the Ray head and submit the training job**

On the master node, following `run_master.sh` (adjust `trainer.nnodes` and `trainer.n_gpus_per_node` for your hardware; extra `key=value` overrides can be appended):

```bash
ray start --head --port=6379

MODEL_PATH=/from_s3/models/Qwen2.5-Math-1.5B  # replace with your model path
HOST_IP="$(hostname -I)"

export VLLM_ATTENTION_BACKEND=XFORMERS

RAY_ADDRESS="http://${HOST_IP}:6379" ray job submit \n    --runtime-env=verl/trainer/runtime_env.yaml \n    --no-wait \n    -- \n    python3 -m verl.trainer.main_ppo \n    algorithm.adv_estimator=grpo \n    data.train_files=$HOME/data/gsm8k/train.parquet \n    data.val_files=$HOME/data/gsm8k/test.parquet \n    data.train_batch_size=1024 \n    data.max_prompt_length=512 \n    data.max_response_length=1024 \n    data.filter_overlong_prompts=True \n    data.truncation='error' \n    actor_rollout_ref.model.path=$MODEL_PATH \n    actor_rollout_ref.actor.optim.lr=1e-6 \n    actor_rollout_ref.model.use_remove_padding=True \n    actor_rollout_ref.actor.ppo_mini_batch_size=256 \n    actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=40 \n    actor_rollout_ref.actor.use_kl_loss=True \n    actor_rollout_ref.actor.kl_loss_coef=0.001 \n    actor_rollout_ref.actor.kl_loss_type=low_var_kl \n    actor_rollout_ref.actor.entropy_coeff=0 \n    actor_rollout_ref.model.enable_gradient_checkpointing=True \n    actor_rollout_ref.actor.fsdp_config.param_offload=False \n    actor_rollout_ref.actor.fsdp_config.optimizer_offload=False \n    actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=40 \n    actor_rollout_ref.rollout.tensor_model_parallel_size=2 \n    actor_rollout_ref.rollout.name=vllm \n    actor_rollout_ref.rollout.gpu_memory_utilization=0.6 \n    actor_rollout_ref.rollout.n=5 \n    actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=40 \n    actor_rollout_ref.ref.fsdp_config.param_offload=True \n    algorithm.use_kl_in_reward=False \n    trainer.critic_warmup=0 \n    trainer.logger=['console','wandb'] \n    trainer.project_name='verl_grpo_example_gsm8k' \n    trainer.experiment_name='qwen2_7b_function_rm' \n    trainer.n_gpus_per_node=1 \n    trainer.nnodes=2 \n    trainer.save_freq=-1 \n    trainer.test_freq=5 \n    trainer.total_epochs=15
```

The bundled `run_master.sh` wraps these steps together with container setup (`service ssh start`, `sleep infinity`). With vLLM >= 0.8, you can remove the `VLLM_ATTENTION_BACKEND=XFORMERS` export and set `actor_rollout_ref.rollout.enforce_eager=False` and `actor_rollout_ref.rollout.free_cache_engine=False` to enable CUDA graphs and the v1 engine (see `docs/README_vllm0.8.md`).

**6. Join the worker nodes**

On each additional node, run `run_worker.sh`; it waits for `MASTER_ADDR` to resolve and then joins the cluster with `ray start --address="${MASTER_IP:=0}:6379"`.

---

## Architecture

verl implements the HybridFlow programming model: RL training is expressed as a dataflow whose nodes are high-level operators (rollout, model forward) and whose edges transfer data between distributed workers.

- **Single-controller orchestration (Ray):** A Ray-based controller layer coordinates the job. A driver such as `verl.trainer.main_ppo` is submitted as a Ray job (`run_master.sh` starts the Ray head), while `run_worker.sh` starts workers that join the head node after resolving `MASTER_ADDR`.
- **Trainer and configuration:** The `verl/trainer` package contains the training drivers and Hydra YAML configs; algorithms and hyperparameters are passed as config overrides (e.g., `algorithm.adv_estimator=grpo`). Algorithm recipes (DAPO, PRIME, R1) live in `recipe/`, and trainer examples (PPO, GRPO, RLOO, ReMax, REINFORCE++, SFT) in `examples/`.
- **Role workers:** `verl/workers` groups the RL roles — actor, critic, rollout (vLLM, SGLang, and naive implementations), reward model/reward manager, and sharding manager. In the default configuration, actor, rollout, and reference policy form one group (`actor_rollout_ref.*`), covering response generation, log-prob computation, and policy updates.
- **Execution backends:** Training runs on FSDP (with param/optimizer offloading) or Megatron-LM; rollout/generation uses vLLM or SGLang via dedicated adapters. Placement knobs such as `rollout.tensor_model_parallel_size` and `rollout.gpu_memory_utilization` control per-role resource use.
- **Data protocol:** `verl/protocol.py` defines `DataProto` — a tensor batch plus non-tensor batch and meta info — as the standard unit of data exchange between roles, with helpers for concatenation, padding, and batch reshaping.
- **Models and utilities:** `verl/models` ships Megatron-compatible model implementations (e.g., LLaMA, Qwen2); `verl/utils` provides checkpointing, datasets, reward scoring, loggers, and rendezvous helpers. Scripts are included to convert checkpoints between Hugging Face and Megatron formats.

At a high level, the Ray-based controller dispatches each training step to the role workers, and data is exchanged between rollout generation, actor/critic/reference computation, and reward scoring as `DataProto` batches.

---

## Testing

Tests live under `tests/` and are executed with **pytest**. The `test` extra in `setup.py` declares the test tooling (`pytest`, `yapf`, `py-spy`):

```bash
pip install -e ".[test]"
pytest tests/verl
```

Target the subdirectory relevant to your change; suites such as `tests/e2e` and `tests/distributed` exercise trainer and distributed behavior.

The suite is organized by scope:

- `tests/verl/` — unit tests for library internals (e.g., `tests/verl/utils/dataset`)
- `tests/e2e/` — end-to-end scenarios: `ppo_trainer`, `sft`, and `arithmetic_sequence` (with the `digit_completion` environment under `tests/e2e/envs/`)
- `tests/ray/` — Ray worker scenarios (`check_worker_alive`, `detached_worker`)
- Focused suites: `checkpoint`, `distributed`, `generation`, `gpu_utility`, `model`, `rollout`, `sandbox`, `sanity`, `utility`

Continuous integration workflows are defined in `.github/workflows/`; `tests/kill_github_tests.sh` is a helper script for GitHub-hosted test runs.

---

## Examples

Runnable trainer examples (PPO, GRPO, RLOO, ReMax, REINFORCE++, and SFT) are available in the [examples](./examples) directory.

---

## Documentation

Project documentation is available in the [docs](./docs) directory, including the HybridFlow programming guide (`docs/hybrid_flow.rst`) and vLLM integration guides (e.g., `docs/README_vllm0.8.md`), together with Sphinx-based documentation and tutorials.

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository and create a branch for your change.
2. Install the development environment: `pip install -e ".[test]"`.
3. Add or update tests for your change under the relevant `tests/` subdirectory and run them with pytest.
4. Ensure the relevant continuous integration workflows (defined in `.github/workflows/`) pass, then open a pull request with a clear description of the change.

---

## License

This project is licensed under the Apache 2.0 License. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use verl in your work, please cite the canonical repository:

### APA format:

    verl (2026). verl repository [Computer software]. https://github.com/volcengine/verl

### BibTeX format:

    @misc{verl,

        author = {verl contributors},

        title = {verl repository},

        year = {2026},

        url = {https://github.com/volcengine/verl}

    }

---