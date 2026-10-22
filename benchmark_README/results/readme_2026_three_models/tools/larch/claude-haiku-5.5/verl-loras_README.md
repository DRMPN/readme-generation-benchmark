# verl-loras-wv6b1kj2

A reinforcement learning training framework for large language models (LLMs), based on the **verl** (Volcano Engine Reinforcement Learning) codebase. It supports PPO, GRPO, DAPO, PRIME, and supervised fine-tuning (SFT), with FSDP and Megatron-LM training backends and vLLM and SGLang rollout engines. The `loras` suffix in the project name and the presence of a PEFT example suggest LoRA-based fine-tuning is part of this fork.

> **Note:** This README was written from the repository's file layout, not from reading each file. Commands, paths, and configuration keys follow the conventions of upstream verl and should be checked against the actual code before use.

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Repository Structure](#repository-structure)
5. [Installation](#installation)
6. [Quick Start](#quick-start)
7. [Data Preparation](#data-preparation)
8. [Training Algorithms](#training-algorithms)
9. [Training Backends and Rollout Engines](#training-backends-and-rollout-engines)
10. [Configuration](#configuration)
11. [Reward Functions](#reward-functions)
12. [Recipes](#recipes)
13. [Supervised Fine-Tuning (SFT)](#supervised-fine-tuning-sft)
14. [LoRA / PEFT](#lora--peft)
15. [Evaluation and Generation](#evaluation-and-generation)
16. [Checkpoints and Model Merging](#checkpoints-and-model-merging)
17. [Multi-Node Training](#multi-node-training)
18. [Model Support](#model-support)
19. [Testing](#testing)
20. [Documentation](#documentation)
21. [Troubleshooting](#troubleshooting)
22. [License](#license)
23. [Citation](#citation)

---

## Overview

The framework trains LLMs with reinforcement learning from verifiable rewards (RLVR) or from learned reward models. It separates the **control flow** (algorithm logic, data routing, scheduling) from the **computation** (actor/critic training, rollout generation, reward scoring). This is the HybridFlow design: a single-controller process coordinates distributed worker groups that run on Ray.

Typical use cases:

- Math and code reasoning RL (GSM8K, MATH, DAPO-Math, LiveCodeBench, AIME)
- Reward-model-based RLHF (e.g., Anthropic HH-RLHF)
- Multimodal RL (e.g., Geo3K, Qwen2.5-VL)
- Supervised fine-tuning with the same infrastructure
- Parameter-efficient fine-tuning (LoRA/PEFT) on RL objectives

---

## Key Features

- **Algorithms:** PPO (GAE), GRPO, DAPO (decoupled clip, dynamic sampling), PRIME (process reward), and SFT.
- **Training backends:** PyTorch FSDP/FSDP2 and Megatron-LM (tensor, pipeline, and sequence parallelism).
- **Rollout engines:** vLLM (multiple versions, SPMD mode), SGLang, and HuggingFace generate as a fallback.
- **Hybrid engine:** Actor training and rollout share GPUs and switch between modes to reduce memory and idle time.
- **Sequence packing and balancing:** Remove-padding (`rmpad`) training and sequence-length balancing to improve throughput.
- **Memory optimizations:** Gradient checkpointing, parameter/optimizer offloading, Ulysses sequence parallelism, and Liger kernels (referenced in `run_qwen_05_sp2_liger.sh`).
- **Custom rewards:** Rule-based reward functions per data source, sandboxed code execution, or model-based reward.
- **Hydra-style configuration:** YAML configs with command-line overrides.
- **Experiment tracking:** Pluggable logging (`tracking.py`), with aggregate logging for distributed runs.
- **Checkpointing:** FSDP, Megatron, and HuggingFace-format checkpoints, with a merger tool.
- **Hardware coverage:** NVIDIA GPUs (Docker images for vLLM 0.7/0.8 and SGLang), AMD ROCm (`Dockerfile.rocm`), and Megatron builds.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│             Driver (single controller, Ray)              │
│   RayPPOTrainer / DAPORayTrainer / PRIME trainer         │
│   - data loading, advantage estimation, scheduling       │
└───────────────┬──────────────────────┬───────────────────┘
                │                      │
      ┌─────────▼────────┐    ┌────────▼─────────┐
      │ Actor/Rollout    │    │ Critic / Ref /   │
      │ worker group     │    │ Reward worker    │
      │ (FSDP / Megatron │    │ groups           │
      │  + vLLM/SGLang)  │    │                  │
      └──────────────────┘    └──────────────────┘
```

Key abstractions:

| Component | Location | Role |
|---|---|---|
| `RayPPOTrainer` | `verl/trainer/ray_trainer.py` | Main PPO/GRPO training loop |
| `core_algos.py` | `verl/trainer/` | Advantage and policy loss functions |
| `WorkerGroup` | `verl/single_controller/` | Manages a set of distributed workers |
| `@register` / decorators | `verl/single_controller/base/decorator.py` | Dispatch and collect rules for worker methods |
| `DataProto` | `verl/protocol.py` | Batched tensor and metadata container passed between stages |
| `ActorRolloutRefWorker` | `verl/workers/fsdp_workers.py` | Combined actor, rollout, and reference model worker |
| `DataParallelPPOActor` | `verl/workers/actor/dp_actor.py` | FSDP actor update logic |
| Rollout modules | `verl/workers/rollout/` | Response generation (vLLM, SGLang, HF) |
| Reward manager | `verl/workers/reward_manager/` | Computes rewards from rule-based functions or models |

---

## Repository Structure

The layout below is inferred from the file listing. Directory names are reliable; file-level details may vary.

```
verl-loras-wv6b1kj2/
├── verl/                        # Core library
│   ├── trainer/                 # PPO/SFT entry points, trainers, configs (YAML)
│   │   ├── main_ppo.py          # PPO entry point
│   │   ├── main_generation.py   # Generation-only entry point
│   │   ├── main_eval.py         # Evaluation entry point
│   │   ├── ray_trainer.py       # RayPPOTrainer
│   │   ├── core_algos.py        # Advantage estimators, policy losses
│   │   ├── metric_utils.py      # Metric computation
│   │   ├── fsdp_sft_trainer.py  # SFT trainer
│   │   ├── ppo_trainer.yaml     # Default PPO config
│   │   ├── ppo_megatron_trainer.yaml
│   │   ├── sft_trainer.yaml
│   │   ├── generation.yaml
│   │   └── evaluation.yaml
│   ├── workers/                 # Worker implementations
│   │   ├── fsdp_workers.py
│   │   ├── megatron_workers.py
│   │   ├── actor/               # dp_actor.py, megatron_actor.py
│   │   ├── critic/              # dp_critic.py, megatron_critic.py
│   │   ├── rollout/             # vllm_rollout*, sglang_rollout, hf_rollout, naive
│   │   ├── reward_model.py
│   │   ├── reward_manager/      # naive.py, prime.py, batch.py, dapo.py
│   │   └── sharding_manager/    # fsdp_vllm, fsdp_sglang, megatron_vllm, fsdp_ulysses
│   ├── single_controller/       # Ray-based worker group abstraction
│   ├── models/                  # Megatron model definitions and loaders
│   │   ├── llama/               # Llama (megatron): parallel layers, loaders, saver
│   │   ├── qwen2/               # Qwen2 (megatron) and Qwen2-VL
│   │   ├── transformers/        # Monkey patches for HF models
│   │   └── weight_loader_registry.py
│   ├── utils/                   # Checkpointing, datasets, rewards, parallelism, logging
│   │   ├── reward_score/        # gsm8k, math, math_dapo, geo3k, sandbox, etc.
│   │   ├── dataset/             # rl_dataset, sft_dataset, rm_dataset, multiturn_sft_dataset
│   │   ├── checkpoint/          # FSDP and Megatron checkpoint managers
│   │   ├── megatron/            # Tensor/pipeline/sequence parallel utilities
│   │   ├── tracking.py
│   │   ├── flops_counter.py
│   │   └── ...
│   ├── third_party/             # vLLM integrations (multiple versions), SGLang
│   ├── protocol.py              # DataProto
│   └── version/
├── recipe/                      # Research recipes built on verl
│   ├── dapo/                    # DAPO training (main_dapo.py, dapo_ray_trainer.py)
│   ├── prime/                   # PRIME process-reward training
│   └── r1/                      # DeepSeek-R1-Distill evaluation (AIME24, GPQA, LiveCodeBench)
├── examples/                    # Launch scripts, data preprocessing, notebooks
│   ├── data_preprocess/         # gsm8k.py, math_dataset.py, geo3k.py, hellaswag.py, ...
│   ├── grpo_trainer/            # GRPO launch scripts
│   ├── ppo_trainer/             # PPO launch scripts
│   ├── sft/                     # SFT launch scripts
│   ├── ray_on_slurm.slurm
│   └── *.ipynb                  # Getting-started and tutorial notebooks
├── tests/                       # Unit, integration, and distributed tests
├── docs/                        # Sphinx documentation (.rst)
├── docker/                      # Dockerfiles (vLLM 0.7/0.8, SGLang, Megatron, ROCm)
├── scripts/                     # Utilities: model_merger.py, converter_hf_to_mcore.py, diagnose.py
├── pyproject.toml
├── setup.py
├── requirements.txt
├── requirements_sglang.txt
└── LICENSE
```

---

## Installation

### Requirements

- Linux with NVIDIA GPUs (CUDA 12.x recommended), or AMD GPUs with ROCm
- Python 3.9 or newer
- PyTorch compatible with your CUDA version
- Ray (for distributed execution)
- vLLM or SGLang (for rollout)
- Flash-Attention 2 (recommended)

### Option 1: pip (from source)

```bash
git clone <repository-url> verl-loras-wv6b1kj2
cd verl-loras-wv6b1kj2

python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

For SGLang rollout:

```bash
pip install -r requirements_sglang.txt
```

Install Flash-Attention separately if the build does not pull it in:

```bash
pip install flash-attn --no-build-isolation
```

### Option 2: Docker

Prebuilt configurations are in `docker/`:

| Dockerfile | Purpose |
|---|---|
| `Dockerfile.ngc.vllm` | NGC PyTorch image with vLLM |
| `Dockerfile.ngc.vllm0.8` | vLLM 0.8.x |
| `Dockerfile.ngc.vllm0.8.sagemaker` | AWS SageMaker variant |
| `Dockerfile.vemlp.vllm.te` | Volcano Engine ML Platform with Transformer Engine |
| `Dockerfile.sglang` | SGLang rollout |
| `Dockerfile.megatron` | Megatron-LM backend |
| `Dockerfile.rocm` | AMD ROCm |

Example:

```bash
docker build -f docker/Dockerfile.ngc.vllm0.8 -t verl:vllm08 .
docker run --gpus all -it --shm-size=32g -v $PWD:/workspace verl:vllm08 bash
```

### Megatron Patch

`megatron_v4.patch` at the repository root applies changes to Megatron-LM. Apply it to a Megatron-LM checkout before using the Megatron backend:

```bash
cd /path/to/Megatron-LM
git apply /path/to/verl-loras-wv6b1kj2/megatron_v4.patch
```

### Verify the Installation

```bash
python -c "import verl; print(verl.__file__)"
python -c "import torch, ray, vllm; print(torch.cuda.is_available(), ray.__version__, vllm.__version__)"
```

---

## Quick Start

This walkthrough trains Qwen2.5-0.5B-Instruct on GSM8K with PPO.

### 1. Prepare the data

```bash
python examples/data_preprocess/gsm8k.py --local_dir ~/data/gsm8k
```

This writes `train.parquet` and `test.parquet` with prompt, reward model, and extra-info fields.

### 2. Start a Ray cluster (optional for single node)

```bash
ray start --head --num-gpus=8
```

### 3. Launch PPO training

```bash
python3 -m verl.trainer.main_ppo \
  data.train_files=$HOME/data/gsm8k/train.parquet \
  data.val_files=$HOME/data/gsm8k/test.parquet \
  data.train_batch_size=256 \
  data.max_prompt_length=512 \
  data.max_response_length=256 \
  actor_rollout_ref.model.path=Qwen/Qwen2.5-0.5B-Instruct \
  actor_rollout_ref.actor.optim.lr=1e-6 \
  actor_rollout_ref.actor.ppo_mini_batch_size=64 \
  actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=4 \
  actor_rollout_ref.rollout.name=vllm \
  actor_rollout_ref.rollout.gpu_memory_utilization=0.5 \
  actor_rollout_ref.rollout.n=5 \
  critic.optim.lr=1e-5 \
  critic.model.path=Qwen/Qwen2.5-0.5B-Instruct \
  critic.ppo_micro_batch_size_per_gpu=4 \
  algorithm.kl_ctrl.kl_coef=0.001 \
  trainer.logger=console \
  trainer.val_before_train=False \
  trainer.n_gpus_per_node=1 \
  trainer.nnodes=1 \
  trainer.save_freq=10 \
  trainer.test_freq=10 \
  trainer.total_epochs=15
```

Launch scripts with the same settings are in `examples/ppo_trainer/` and at the repository root (e.g., `run_qwen2-7b.sh`, `run_deepseek7b_llm.sh`).

### 4. GRPO variant

Set `algorithm.adv_estimator=grpo` and drop the critic block. The example scripts in `examples/grpo_trainer/` (e.g., `qwen2-7b_grpo_2_h800_fsdp_vllm.sh`) show the full settings.

---

## Data Preparation

Training data is stored as Parquet files. Each row typically contains:

| Field | Description |
|---|---|
| `data_source` | Key used to select a reward function (e.g., `openai/gsm8k`) |
| `prompt` | Chat-format list of messages (`[{"role": "user", "content": ...}]`) |
| `ability` | Task category (for logging) |
| `reward_model` | Dict with `style` (e.g., `rule`) and `ground_truth` |
| `extra_info` | Optional metadata (split, index, and so on) |

Preprocessing scripts in `examples/data_preprocess/`:

| Script | Dataset |
|---|---|
| `gsm8k.py` | GSM8K math word problems |
| `math_dataset.py` | MATH |
| `geo3k.py` | Geometry3K (multimodal) |
| `hellaswag.py` | HellaSwag |
| `full_hh_rlhf.py` | Anthropic HH-RLHF (reward-model training) |
| `multiturn.py` | Multi-turn SFT data |

DAPO data is prepared with `recipe/dapo/prepare_dapo_data.sh`.

---

## Training Algorithms

| Algorithm | Config value | Notes |
|---|---|---|
| PPO (GAE) | `algorithm.adv_estimator=gae` | Requires a critic. Default. |
| GRPO | `algorithm.adv_estimator=grpo` | Group-relative advantage over `actor_rollout_ref.rollout.n` samples. No critic. |
| DAPO | `recipe/dapo/main_dapo.py` | Decoupled clip ratios, dynamic sampling, token-level loss, overlong reward shaping. |
| PRIME | `recipe/prime/main_prime.py` | Implicit process reward model trained online alongside the policy. |
| SFT | `verl/trainer/fsdp_sft_trainer.py` | Supervised fine-tuning with the same data and parallelism stack. |

Policy losses and advantage estimators are implemented in `verl/trainer/core_algos.py`. Add a new estimator there and register it in the trainer's dispatch.

---

## Training Backends and Rollout Engines

### Actor/Critic Backends

- **FSDP** (`verl/workers/fsdp_workers.py`): PyTorch Fully Sharded Data Parallel. Easiest to start with. Supports CPU offloading and mixed precision.
- **Megatron** (`verl/workers/megatron_workers.py`, `run_ppo_trainer_megatron.sh`): Tensor, pipeline, and context parallelism for models above ~30B parameters. Requires the Megatron patch and conversion (see [Model Support](#model-support)).

Select the backend with `actor_rollout_ref.strategy=fsdp` or `megatron` and use the matching config file (`ppo_trainer.yaml` vs. `ppo_megatron_trainer.yaml`).

### Rollout Engines

| Engine | Config | Notes |
|---|---|---|
| vLLM | `actor_rollout_ref.rollout.name=vllm` | Main engine. Versions are shimmed in `verl/third_party/vllm/` (0.4 through 0.8). |
| SGLang | `actor_rollout_ref.rollout.name=sglang` | Uses `verl/workers/rollout/sglang_rollout/`. Better for multi-turn and tool use. |
| HuggingFace | `actor_rollout_ref.rollout.name=hf` | Slow. For debugging. |

### Hybrid Engine and Sharding Managers

Sharding managers (`verl/workers/sharding_manager/`) convert weights between the training layout and the inference layout when switching between training and generation. Examples: `fsdp_vllm.py`, `fsdp_sglang.py`, `megatron_vllm.py`.

### Performance Options

| Option | Purpose |
|---|---|
| `actor_rollout_ref.model.use_remove_padding=True` | Skip padding tokens (`run_ray_trainer_rmpad.sh`) |
| `trainer.balance_batch` / seqlen balancing | Balance sequence lengths across ranks (`run_*_seq_balance.sh`) |
| `actor_rollout_ref.model.enable_gradient_checkpointing=True` | Trade compute for memory |
| `actor_rollout_ref.actor.fsdp_config.param_offload=True` | Offload parameters to CPU |
| `actor_rollout_ref.actor.ulysses_sequence_parallel_size` | Ulysses sequence parallelism for long contexts |
| `use_liger=True` | Liger kernels (`run_qwen_05_sp2_liger.sh`) |

See `docs/perf_tuning.rst` and `docs/device_tuning.rst` for tuning guidance.

---

## Configuration

Configuration uses YAML files with Hydra-style dotted overrides on the command line.

### Main Config Files

| File | Purpose |
|---|---|
| `verl/trainer/config/ppo_trainer.yaml` | PPO/GRPO with FSDP |
| `verl/trainer/config/ppo_megatron_trainer.yaml` | PPO/GRPO with Megatron |
| `verl/trainer/config/sft_trainer.yaml` | SFT |
| `verl/trainer/config/generation.yaml` | Generation only |
| `verl/trainer/config/evaluation.yaml` | Evaluation |
| `recipe/dapo/dapo_trainer.yaml` | DAPO |
| `recipe/prime/prime_trainer.yaml` | PRIME |
| `recipe/r1/evaluation.yaml` | R1-distill evaluation |

### Important Keys

```yaml
data:
  train_files: ...
  val_files: ...
  train_batch_size: 256
  max_prompt_length: 512
  max_response_length: 1024

actor_rollout_ref:
  model:
    path: Qwen/Qwen2.5-7B-Instruct
    use_remove_padding: True
    enable_gradient_checkpointing: True
  actor:
    strategy: fsdp
    ppo_mini_batch_size: 64
    ppo_micro_batch_size_per_gpu: 4
    clip_ratio: 0.2
    entropy_coeff: 0.0
    optim:
      lr: 1e-6
  rollout:
    name: vllm
    n: 5                       # samples per prompt (GRPO group size)
    temperature: 1.0
    gpu_memory_utilization: 0.5
    tensor_model_parallel_size: 1

critic:
  model:
    path: ...
  optim:
    lr: 1e-5

algorithm:
  adv_estimator: gae           # or grpo
  gamma: 1.0
  lam: 1.0
  kl_ctrl:
    kl_coef: 0.001

trainer:
  n_gpus_per_node: 8
  nnodes: 1
  logger: ['console', 'wandb']
  project_name: my_project
  experiment_name: my_run
  save_freq: 20
  test_freq: 20
  total_epochs: 15
  default_local_dir: checkpoints/
```

Run `python -m verl.trainer.main_ppo --help` or inspect the YAML files for the full set of keys.

### Runtime Environment

`verl/trainer/runtime_env.yaml` sets environment variables for Ray workers (for example, `NCCL_DEBUG`, `VLLM_ATTENTION_BACKEND`, and `HF_HOME`).

---

## Reward Functions

Rewards are selected by the `data_source` field. Built-in scorers in `verl/utils/reward_score/`:

| Module | Used for |
|---|---|
| `gsm8k.py` | Extracting `#### answer` and comparing numerically |
| `math.py` | MATH answer equivalence |
| `math_dapo.py` | DAPO-style math verification |
| `math_verify.py`, `math_normalize.py` | Symbolic verification and normalization |
| `geo3k.py` | Geometry3K |
| `sandbox_fusion/` / `testing_util.py` | Code execution for code tasks |
| `prime_code/`, `prime_math/` | PRIME verifiers |
| `grader.py` | Shared grading utilities |

### Custom Reward Function

Add a Python file that exposes a `compute_score` function and point the config at it:

```python
# my_rewards.py
def compute_score(data_source, solution_str, ground_truth, extra_info=None):
    """Return a float reward."""
    answer = solution_str.split("Answer:")[-1].strip()
    return 1.0 if answer == str(ground_truth).strip() else 0.0
```

```bash
custom_reward_function.path=/abs/path/my_rewards.py \
custom_reward_function.name=compute_score
```

`check_custom_rwd_fn.py` at the root validates a custom reward function against sample inputs.

### Reward Models

Set `reward_model.enable=True` and `reward_model.model.path=...` to use a learned reward model (see `run_qwen2-7b_rm.sh`, `run_deepseek7b_llm_rm.sh`). Reward model training uses `verl/utils/dataset/rm_dataset.py`.

---

## Recipes

### DAPO (`recipe/dapo/`)

Reproduces the DAPO algorithm on math reasoning:

```bash
bash recipe/dapo/prepare_dapo_data.sh
bash recipe/dapo/run_dapo_qwen2.5_32b.sh
bash recipe/dapo/run_dapo_early_qwen2.5_32b.sh   # early-stopping variant
bash recipe/dapo/test_dapo_7b.sh                 # small-scale test
```

Components: `main_dapo.py`, `dapo_ray_trainer.py` (dynamic sampling), `dapo_trainer.yaml`, and `verl/workers/reward_manager/dapo.py`. See `recipe/dapo/README.md`.

### PRIME (`recipe/prime/`)

Process-reward RL with an implicit PRM trained on rollouts:

```bash
bash recipe/prime/run_prime_qwen.sh
```

Components: `main_prime.py`, `prime_ray_trainer.py`, `prime_core_algos.py`, `prime_dp_rm.py`, `prime_fsdp_workers.py`, `prime_trainer.yaml`.

### R1-Distill Evaluation (`recipe/r1/`)

Evaluates DeepSeek-R1-Distill models on AIME 2024, GPQA, MATH, and LiveCodeBench:

```bash
bash recipe/r1/run_r1_distill_qwen.sh
bash recipe/r1/run_r1_distill_qwen_aime24_eval.sh
bash recipe/r1/run_master.sh          # orchestrates the evaluation suite
```

Supporting modules: `data_process.py`, `math.py`, `gpqa.py`, `livecodebench.py`, `reward_score.py`, `main_eval.py`.

---

## Supervised Fine-Tuning (SFT)

```bash
bash examples/sft/run_sft.sh
```

or directly:

```bash
torchrun --standalone --nnodes=1 --nproc_per_node=8 \
  -m verl.trainer.fsdp_sft_trainer \
  data.train_files=$HOME/data/gsm8k/train.parquet \
  data.val_files=$HOME/data/gsm8k/test.parquet \
  data.prompt_key=extra_info \
  data.response_key=extra_info \
  data.prompt_dict_keys=['question'] \
  data.response_dict_keys=['answer'] \
  data.micro_batch_size=16 \
  model.partial_pretrain=Qwen/Qwen2.5-0.5B-Instruct \
  trainer.default_local_dir=checkpoints/sft \
  trainer.project_name=gsm8k-sft \
  trainer.total_epochs=3
```

Multi-turn SFT uses `verl/utils/dataset/multiturn_sft_dataset.py`. Sequence-parallel SFT scripts are `examples/sft/run_qwen_05_sp2.sh` and related files.

---

## LoRA / PEFT

The repository includes `run_qwen_05_peft.sh`, which runs parameter-efficient training. LoRA settings are typically passed through the model configuration:

```bash
bash run_qwen_05_peft.sh
```

Expected settings (verify against the script):

```yaml
actor_rollout_ref:
  model:
    lora_rank: 16
    lora_alpha: 32
    target_modules: [q_proj, k_proj, v_proj, o_proj]
```

When LoRA is enabled:

- Only adapter weights are optimized and checkpointed.
- Adapters must be merged into the base model before exporting a standalone model (see [Checkpoints and Model Merging](#checkpoints-and-model-merging)).
- Rollout engines must load the base model plus adapters. Check that your vLLM/SGLang version supports LoRA adapters.

---

## Evaluation and Generation

### Generation

Generate responses for a dataset without training:

```bash
python3 -m verl.trainer.main_generation \
  --config-name generation \
  data.path=$HOME/data/gsm8k/test.parquet \
  data.prompt_key=prompt \
  model.path=Qwen/Qwen2.5-7B-Instruct \
  rollout.name=vllm \
  rollout.n=1 \
  output_path=outputs/gen.parquet
```

Also see `verl/trainer/main_generation.py` and `run_gen_qwen05.sh`.

### Evaluation

```bash
python3 -m verl.trainer.main_eval --config-name evaluation \
  data.path=outputs/gen.parquet
```

`check_results.py` (repository root) summarizes saved outputs. `verl/trainer/main_eval.py` computes rewards on pre-generated responses.

---

## Checkpoints and Model Merging

Checkpoints are written to `trainer.default_local_dir`:

```
checkpoints/<project>/<experiment>/global_step_<N>/
├── actor/        # FSDP or Megatron shards
├── critic/
└── ...
```

Convert to a HuggingFace-format model with `scripts/model_merger.py`:

```bash
python scripts/model_merger.py \
  --backend fsdp \
  --local_dir checkpoints/project/exp/global_step_100/actor \
  --target_dir exported/qwen2.5-7b-rl
```

For Megatron:

```bash
python scripts/model_merger.py --backend megatron ...
```

Import an existing HuggingFace model into Megatron format with `scripts/converter_hf_to_mcore.py`.

Checkpoint managers live in `verl/utils/checkpoint/`:
- `fsdp_checkpoint_manager.py`
- `megatron_checkpoint_manager.py`
- `checkpoint_manager.py` (base)

---

## Multi-Node Training

### Ray Cluster

On the head node:

```bash
ray start --head --port=6379 --dashboard-host=0.0.0.0
```

On each worker node:

```bash
ray start --address=<head_ip>:6379
```

Then set `trainer.nnodes` and `trainer.n_gpus_per_node` and run the training command on the head node.

### SLURM

```bash
sbatch examples/ray_on_slurm.slurm
```

### Multi-Node Scripts

Examples: `run_deepseek7b_mutli_node.sh`, `run_ray_trainer.sh`, `run_worker.sh` (worker bootstrapping). See `docs/multinode.rst`.

---

## Model Support

Model architectures are supported through HuggingFace Transformers, with Megatron implementations for large-scale training:

| Family | HF training (FSDP) | Megatron | Notes |
|---|---|---|---|
| Qwen2 / Qwen2.5 | Yes | Yes (`verl/models/qwen2/megatron/`) | Includes Qwen2.5-VL (`qwen2_vl.py`) |
| Llama / Llama 2 / 3 | Yes | Yes (`verl/models/llama/megatron/`) | |
| DeepSeek (7B, 67B, V2-Lite) | Yes | Yes | Scripts under root `run_deepseek*.sh` |
| Gemma (2B, 7B) | Yes | No | `run_gemma*.sh` |
| DeepSeek-R1-Distill-Qwen | Yes | Yes | Recipe `recipe/r1/` |

Megatron weight loaders and savers are in `verl/models/<family>/megatron/checkpoint_utils/` (`*_loader.py`, `*_saver.py`). `weight_loader_registry.py` maps architecture names to loaders. Monkey patches for HF models live in `verl/models/transformers/`.

Multimodal support: `geo3k.py` data preprocessing and `run_qwen2_5_vl-7b.sh`.

---

## Testing

Tests are in `tests/`. They cover:

- **Core:** `test_import.py`, `test_protocol*` tests, `test_tensor_dict*.py`, `test_torch_functional.py`, `test_ops.py`
- **Single controller / Ray:** `test_worker_group_*.py`, `test_colocated_workers.py`, `test_driverfunc_to_worker.py`, `test_high_level_scheduling_api.py`, `test_ray_local_envs.py`
- **Datasets:** `test_rl_dataset.py`, `test_sft_dataset.py`, `test_rm_dataset.py`, `test_multiturn_sft_dataset.py`
- **Models and parallelism:** `test_transformers_ulysses.py`, `test_sp_loss_match.py`, `test_module.py`
- **Rollouts:** `test_vllm_spmd.py`, `test_sglang_spmd.py`, `test_vllm_hf_loader.py`, `test_memory_buffers.py`
- **Rewards:** `test_sandbox.py`
- **Checkpoints:** `test_fsdp_ckpt.py`
- **Misc:** `check_license.py`, `test_check_worker_alive.py`

Run the test suite:

```bash
pytest tests/ -v
```

Some tests need multiple GPUs or Ray. Run `tests/run_test.sh` (or `run_all.sh`) to execute them in the configured environment. `kill_github_tests.sh` stops leftover distributed test processes.

Code style is enforced with `format.sh` (wraps formatters and linters configured in `pyproject.toml`).

---

## Documentation

Docs live in `docs/` (Sphinx, reStructuredText):

| Topic | File |
|---|---|
| Installation | `install.rst` |
| Quickstart | `quickstart.rst` |
| Multi-node | `multinode.rst` |
| Architecture (HybridFlow) | `hybrid_flow.rst`, `ppo_code_architecture.rst` |
| Configuration | `config.rst` |
| Data | `data.rst`, `prepare_data.rst` |
| Reward functions | `reward_function.rst` |
| Performance and device tuning | `perf_tuning.rst`, `device_tuning.rst` |
| Checkpoints | `checkpoint.rst` |
| Extensions (FSDP, Megatron, DPO) | `fsdp_extension.rst`, `megatron_extension.rst`, `dpo_extension.rst` |
| SGLang worker | `sglang_worker.rst` |
| vLLM version notes | `README_vllm0.7.md`, `README_vllm0.8.md` |
| FAQ | `faq.rst` |

Build the docs:

```bash
cd docs
pip install -r requirements-docs.txt
make html
```

---

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| `CUDA out of memory` during rollout | Lower `gpu_memory_utilization`, `rollout.n`, or `max_response_length`. Enable `param_offload`. |
| `CUDA out of memory` during actor update | Reduce `ppo_micro_batch_size_per_gpu`. Enable gradient checkpointing. |
| vLLM and PyTorch version mismatch | Use the Docker image for your vLLM version or check `requirements.txt`. |
| Ray workers cannot find GPUs | Check `ray status` and `trainer.n_gpus_per_node`. Restart Ray after changing GPU settings. |
| Reward always 0 | Verify `data_source` matches a reward module and that `ground_truth` is in the expected format. |
| Hangs at startup on multi-node | Check that NCCL interfaces (`NCCL_SOCKET_IFNAME`) and firewall settings allow communication. |
| Megatron import errors | Apply `megatron_v4.patch` to your Megatron-LM checkout. |
| Diagnostics | Run `python scripts/diagnose.py` to collect environment information. |

For more, see `docs/faq.rst`.

---

## License

This project is released under the **Apache License 2.0** (see `LICENSE`). Third-party components retain their own licenses; see `Notice.txt`. The `check_license.py` script verifies license headers in source files.

---

## Citation

If you use this framework in research, please cite the upstream verl paper (HybridFlow):

```bibtex
@article{sheng2024hybridflow,
  title   = {HybridFlow: A Flexible and Efficient RLHF Framework},
  author  = {Sheng, Guangming and Zhang, Chi and Ye, Zilingfeng and Wu, Xibin and Zhang, Wang and Zhang, Ru and Peng, Yanghua and Lin, Haibin and Wu, Chuan},
  journal = {arXiv preprint arXiv: 2409.19256},
  year    = {2024}
}
```

If you use the DAPO or PRIME recipes, cite their respective papers.

---

## Acknowledgements

This project builds on verl, vLLM, SGLang, Megatron-LM, PyTorch FSDP, Ray, HuggingFace Transformers, and Flash-Attention.
