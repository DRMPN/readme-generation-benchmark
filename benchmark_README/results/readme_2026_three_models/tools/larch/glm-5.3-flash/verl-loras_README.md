# verl-loras-znxvxm01

> **A flexible, efficient and industrial-strength RLHF framework for large language models.**
> Built on [verl](https://github.com/volcengine/verl) / the **HybridFlow** programming model, and extended with **LoRA/PEFT training**, **DAPO**, **PRIME**, **FIRE sampling**, sandboxed code-reward execution, and **LiveCodeBench / GPQA / AIME24** evaluation pipelines.

| | |
|---|---|
| **License** | Apache 2.0 (see `LICENSE`, `Notice.txt`) |
| **Language** | Python (≥3.9), PyTorch, Ray |
| **Training backends** | FSDP, Megatron-LM v4 |
| **Inference engines** | vLLM (0.5.x / 0.6.3 / 0.7 / 0.8), SGLang, HuggingFace |
| **Package** | `verl` (via `setup.py` / `pyproject.toml`) |

---

## Table of Contents

1. [Overview](#1-overview)
2. [What's New in This Fork](#2-whats-new-in-this-fork)
3. [Key Features](#3-key-features)
4. [Supported Algorithms, Models and Backends](#4-supported-algorithms-models-and-backends)
5. [Repository Structure](#5-repository-structure)
6. [Installation](#6-installation)
7. [Quickstart](#7-quickstart)
8. [Architecture](#8-architecture)
9. [Trainers & Entry Points](#9-trainers--entry-points)
10. [Rollout / Inference Engines](#10-rollout--inference-engines)
11. [Reward Functions & Sandbox](#11-reward-functions--sandbox)
12. [Data Preparation](#12-data-preparation)
13. [Configuration System](#13-configuration-system)
14. [Evaluation Suite](#14-evaluation-suite)
15. [Checkpointing & Model Utilities](#15-checkpointing--model-utilities)
16. [Multi-Node & SLURM](#16-multi-node--slurm)
17. [Docker Images](#17-docker-images)
18. [Testing](#18-testing)
19. [Documentation](#19-documentation)
20. [Performance Tuning](#20-performance-tuning)
21. [Contributing](#21-contributing)
22. [License](#22-license)
23. [Acknowledgements & Citation](#23-acknowledgements--citation)

---

## 1. Overview

**verl-loras-znxvxm01** is a research fork of **verl** (*Volcano Engine Reinforcement Learning*), the open-source implementation of the **HybridFlow** paper. verl is designed to make RLHF / RL post-training of large language models:

- **Flexible** — RL training pipelines are expressed as a *directed acyclic graph (DAG)* over "roles" (Actor, Critic, Reward Model, Reference Policy, Rollout). New algorithms are usually a few lines of dataflow code.
- **Efficient** — a *single controller* (like `DataParallel`) programs the logic, while the heavy lifting runs as *multi-controller (SPMD)* workers using FSDP or Megatron-LM, fused with high-throughput generation via vLLM / SGLang.
- **Industrial** — multi-node Ray orchestration, resumable checkpointing, sequence balancing, removal-padding, flops counting, memory/performance instrumentation, and TensorBoard/WandB/MLFlow tracking out of the box.

This fork keeps the full upstream feature set and adds a family of **research recipes** and **training/eval extensions** (LoRA, DAPO, PRIME, FIRE sampling, LiveCodeBench/GPQA evaluation, sandboxed code rewards) described below.

---

## 2. What's New in This Fork

| Addition | Description | Key files |
|---|---|---|
| **LoRA / PEFT RL** | Parameter-efficient RLHF with LoRA adapters on FSDP; train a Qwen-0.5B policy with LoRA on a single GPU. | `run_qwen_05_peft.sh`, `run_qwen_05_sp2.sh`, `run_qwen_05_sp2_liger.sh` |
| **DAPO trainer** | *Decoupled Clip and dynamic Sampling Policy Optimization* — decoupled clip ranges (clip-higher), dynamic sampling, token-level policy-gradient loss, overlong-reward shaping. | `main_dapo.py`, `dapo_ray_trainer.py`, `dapo_trainer.yaml`, `run_dapo_qwen2.5_32b.sh`, `run_dapo_early_qwen2.5_32b.sh`, `test_dapo_7b.sh`, `prepare_dapo_data.sh` |
| **PRIME trainer** | *Process Reinforcement through IMplicit rEwards* — implicit process rewards with an online-updated implicit PRM. | `main_prime.py`, `prime_ray_trainer.py`, `prime_core_algos.py`, `prime_dp_rm.py`, `prime_fsdp_workers.py`, `prime_trainer.yaml`, `run_prime_qwen.sh`, `run_prime.sh` |
| **FIRE sampling rollout** | Alternative vLLM-based rollout implementation optimized for high-throughput / fine-grained sampling control. | `fire_vllm_rollout.py`, `run_ray_trainer_fire_sampling.sh` |
| **Benchmark evaluation suite** | End-to-end evaluation of (R1-distill) checkpoints on **LiveCodeBench**, **GPQA**, **MATH / AIME24**. | `main_eval.py`, `evaluation.yaml`, `livecodebench.py`, `gpqa.py`, `math.py`, `data_process.py`, `run_r1_distill_qwen.sh`, `run_r1_distill_qwen_aime24_eval.sh`, `run_master.sh`, `check_results.py` |
| **Sandboxed code reward server** | Client/server service for executing untrusted model-generated code safely during training. | `server.py`, `client.py`, `run.sh`, `test_sandbox.py` |
| **Extra reward functions** | `math_dapo`, `math_batch`, `math_verify` graders and a fork-level reward dispatcher. | `reward_score.py`, `verl/utils/reward_score/{math_dapo,math_batch,math_verify}.py`, `check_custom_rwd_fn.py` |

---

## 3. Key Features

- **Hybrid programming model** (single-controller + multi-controller) — write RL algorithms like standard PyTorch (`RayPPOTrainer`), execute them as distributed SPMD jobs.
- **Multiple RL algorithms** — PPO (GAE), GRPO, ReMax, ReInforce++, RLOO, plus the fork's **DAPO** and **PRIME** recipes.
- **SFT** — full-parameter and LoRA/PEFT supervised fine-tuning (`fsdp_sft_trainer.py`).
- **Multiple training backends**
  - **PyTorch FSDP** — works with any HuggingFace `transformers` model.
  - **Megatron-LM v4** — expert-parallel 3D parallelism (TP/PP/CP/SP), enabled via the included `megatron_v4.patch`; hand-written Megatron kernels for Llama, Qwen2, Qwen2-VL.
- **Multiple rollout engines** — vLLM (four supported versions, incl. SPMD mode), SGLang, HuggingFace, naive on-policy rollouts, and the fork's **FIRE** rollout.
- **Colocation & disaggregation** — share GPUs among roles via the *hybrid engine* (generate with vLLM weights, train with FSDP/Megatron weights, re-shard automatically), or place roles on separate worker groups.
- **Reward flexibility** — rule-based (function) rewards, model-based (reward model) rewards, implicit rewards (PRIME), and sandboxed code execution.
- **Sequence balancing / removal-padding / ulysses & sequence parallelism** for long-context efficiency, plus Liger-kernel support.
- **Scale** — single GPU → multi-node Ray clusters → SLURM (`ray_on_slurm.slurm`).
- **Tracking** — console, TensorBoard, WandB, MLFlow (`verl/utils/tracking.py`).

---

## 4. Supported Algorithms, Models and Backends

### Algorithms

| Algorithm | Advantage estimator | Trainer | Entry point |
|---|---|---|---|
| PPO | GAE (`gae`) | `RayPPOTrainer` | `verl/trainer/main_ppo.py` |
| GRPO | group-relative (`grpo`) | `RayPPOTrainer` | `verl/trainer/main_ppo.py` |
| ReMax | (`remax`) | `RayPPOTrainer` | `verl/trainer/main_ppo.py` |
| ReInforce++ | (`reinforce_plus_plus`, `reinforce_plus_plus_baseline`) | `RayPPOTrainer` | `verl/trainer/main_ppo.py` |
| RLOO | (`rloo`) | `RayPPOTrainer` | `verl/trainer/main_ppo.py` |
| **DAPO** | group-relative + dynamic sampling | `DAPOTrainer` | `main_dapo.py` |
| **PRIME** | implicit process rewards | `PrimeRayTrainer` | `main_prime.py` |
| DPO | — | extension guide | `docs/dpo_extension.rst` |
| SFT | — | `FSDPSFTTrainer` | `verl/trainer/fsdp_sft_trainer.py` |

Loss/advantage machinery lives in `verl/trainer/core_algos.py` (KL penalties: fixed / adaptive / absolute / low-variance KL; loss types: vanilla, clip, dual-clip) and `prime_core_algos.py` / `dapo_ray_trainer.py` for the fork's recipes.

### Models

- **FSDP backend**: any HuggingFace model — verified recipes for **Qwen2**, **Qwen2.5**, **Qwen2-VL**, **Llama**, **DeepSeek**, **Gemma**, **Mistral**.
- **Megatron backend**: `verl/models/llama`, `verl/models/qwen2`, `verl/models/qwen2_vl` (custom `parallel_attention`, `parallel_mlp`, `parallel_decoder`, `parallel_rmsnorm`, `parallel_linear` kernels + HF⇄Megatron weight loaders/savers), with a model registry in `verl/models/mcore`.
- **PEFT**: LoRA adapters for the FSDP backend.

### Backends × Engines matrix

| | FSDP | Megatron-LM |
|---|---|---|
| **vLLM rollout** | ✅ (sync & SPMD) | ✅ (0.6.3+) |
| **SGLang rollout** | ✅ | ✅ |
| **HF / naive rollout** | ✅ | — |
| **FIRE rollout** | ✅ | — |

---

## 5. Repository Structure

```text
verl-loras-znxvxm01/
├── verl/                          # core package
│   ├── trainer/
│   │   ├── main_ppo.py            #   RL entry point (PPO/GRPO/RLOO/ReMax/ReInforce++)
│   │   ├── main_ppo_split.py      #   split (disaggregated) PPO variant
│   │   ├── main_eval.py           #   evaluation entry (LiveCodeBench/GPQA/MATH)
│   │   ├── main_generation.py     #   batch generation
│   │   ├── fsdp_sft_trainer.py    #   SFT trainer (full + LoRA/PEFT)
│   │   ├── ray_trainer.py         #   RayPPOTrainer (generic PPO fit loop)
│   │   ├── core_algos.py          #   advantages, KL, losses
│   │   ├── metric_utils.py, seqlen_balancing.py, config.py
│   │   └── config/                #   ppo_trainer.yaml, ppo_megatron_trainer.yaml,
│   │                              #   generation.yaml, sft_trainer.yaml, evaluation.yaml
│   ├── workers/                   # role implementations
│   │   ├── fsdp_workers.py        #   FSDP Actor/Critic/RM/Rollout workers
│   │   ├── megatron_workers.py    #   Megatron workers
│   │   ├── actor/                 #   dp_actor.py, megatron_actor.py
│   │   ├── critic/                #   dp_critic.py, megatron_critic.py
│   │   ├── reward_model/          #   reward-model workers
│   │   ├── rollout/               #   vllm_rollout.py, vllm_rollout_spmd.py,
│   │   │                          #   fire_vllm_rollout.py, sglang_rollout.py,
│   │   │                          #   hf_rollout.py, naive_rollout.py
│   │   └── sharding_manager/      #   fsdp_vllm.py, fsdp_vllm_patch.py,
│   │                              #   fsdp_ulysses.py, fsdp_sglang.py, megatron_vllm.py
│   ├── single_controller/         # HybridFlow single-controller
│   │   ├── base/                  #   Worker, WorkerGroup, ResourcePool, decorator
│   │   └── ray/                   #   RayWorkerGroup, remote worker bindings
│   ├── models/                    # Megatron model implementations
│   │   ├── llama/  qwen2/  qwen2_vl/  mcore/
│   ├── third_party/
│   │   ├── vllm/                  #   versioned integrations (0.5.x, 0.6.3, 0.7, 0.8)
│   │   └── sglang/                #   SGLang integration
│   └── utils/
│       ├── dataset/               #   rl_dataset, sft_dataset, rm_dataset,
│       │                          #   multiturn_sft_dataset, vision_utils
│       ├── reward_score/          #   gsm8k, math, math_dapo, math_batch, math_verify,
│       │                          #   math_normalize, grader, geo3k, testing_util
│       ├── megatron_utils/, model.py, torch_functional.py, ulysses.py,
│       ├── sequence_parallel.py, fsdp_utils.py, optimizer.py, memory_buffer.py,
│       ├── tracking.py, flops_counter.py, trajectory_tracker.py, performance.py,
│       └── fs.py, hdfs_io.py, distributed.py, import_utils.py, ...
├── recipe/                        # research recipes from this fork
│   ├── dapo/                      #   main_dapo.py, dapo_ray_trainer.py,
│   │                              #   dapo_trainer.yaml, run_dapo_*.sh, prepare_dapo_data.sh
│   ├── prime/                     #   main_prime.py, prime_ray_trainer.py,
│   │                              #   prime_core_algos.py, prime_dp_rm.py,
│   │                              #   prime_fsdp_workers.py, prime_trainer.yaml
│   └── evaluation/                #   livecodebench.py, gpqa.py, math.py,
│                                  #   data_process.py, reward_score.py
├── examples/
│   ├── data_preprocess/           #   gsm8k.py, math_dataset.py, full_hh_rlhf.py,
│   │                              #   hellaswag.py, geo3k.py, multiturn.py
│   ├── ppo_trainer/               #   run_qwen2-7b.sh, run_deepseek7b_llm.sh, run_gemma.sh,
│   │                              #   run_qwen2_5_vl-7b.sh, megatron + seq-balance variants
│   ├── grpo_trainer/  rloo_trainer/  remax_trainer/  reinforce_plus_plus_trainer/
│   ├── split/                     #   main_ppo_split.py, ppo_trainer_split.yaml
│   ├── sft_trainer/               #   run_sft.sh
│   └── ...                        #   model_merger.py, tutorial.ipynb, ...
├── tests/                         # pytest suite (see §18)
├── docs/                          # Sphinx documentation (see §19)
├── run_master.sh / run_all.sh     # fork pipelines (train + eval orchestration)
├── run_sft.sh / run_r1_distill_qwen.sh / run_r1_distill_qwen_aime24_eval.sh
├── server.py / client.py / run.sh # sandbox code-execution service
├── setup.py, pyproject.toml, requirements.txt, requirements_sglang.txt
├── megatron_v4.patch              # Megatron-LM v4 compatibility patch
├── Dockerfile.*                   # see §17
├── ray_on_slurm.slurm
├── verl_getting_started.ipynb, tutorial.ipynb
└── LICENSE, Notice.txt, Makefile, format.sh
```

---

## 6. Installation

### 6.1 Requirements

- Python ≥ 3.9
- PyTorch ≥ 2.0 with CUDA (ROCm supported via `Dockerfile.rocm`)
- `ray`, `transformers`, `datasets`, `hydra-core`, and either **vLLM** or **SGLang** (see `requirements.txt`, `requirements_sglang.txt`)

### 6.2 Install from source

```bash
git clone <this-repo> verl-loras-znxvxm01
cd verl-loras-znxvxm01
pip install -r requirements.txt        # core deps
pip install -r requirements_sglang.txt # optional: SGLang rollout
pip install -e .                       # install the `verl` package
```

**Megatron-LM support (optional):** apply the provided compatibility patch to a Megatron-LM v4 checkout:

```bash
git apply megatron_v4.patch
```

### 6.3 Docker

Prebuilt environments are provided via the Dockerfiles at the repo root:

| Dockerfile | Purpose |
|---|---|
| `Dockerfile.ngc.vllm0.8` | NVIDIA NGC base + vLLM 0.8 (recommended) |
| `Dockerfile.ngc.vllm0.8.sagemaker` | Same, adapted for SageMaker |
| `Dockerfile.ngc.vllm` | NGC base + stable vLLM |
| `Dockerfile.vemlp.vllm.te` | Volcano Engine ML platform + TorchElastic |
| `Dockerfile.megatron` | Megatron-LM training stack |
| `Dockerfile.sglang` | SGLang rollout stack |
| `Dockerfile.rocm` | AMD ROCm stack |

See `docs/index.rst` and `docs/install.rst` for pinned versions per image.

---

## 7. Quickstart

### 7.1 Prepare data (GSM8K)

```bash
python examples/data_preprocess/gsm8k.py --local_dir ~/data/gsm8k
```

This downloads GSM8K, extracts `question`/`answer` fields, and stores train/test parquet files consumable by `rl_dataset.py`.

### 7.2 PPO on Qwen2-7B (FSDP + vLLM)

```bash
bash examples/ppo_trainer/run_qwen2-7b.sh
```

Or run the minimal single-node example:

```bash
bash examples/ppo_trainer/run_qwen2-7b_seq_balance.sh
```

### 7.3 GRPO / RLOO / ReMax / ReInforce++

```bash
bash examples/grpo_trainer/run_qwen2-7b.sh
bash examples/rloo_trainer/run_qwen2-7b.sh
bash examples/remax_trainer/run_qwen2-7b.sh
bash examples/reinforce_plus_plus_trainer/run_qwen2-7b.sh
```

### 7.4 LoRA / PEFT training (this fork)

```bash
bash run_qwen_05_peft.sh          # LoRA RL training on Qwen-0.5B
bash run_qwen_05_sp2.sh           # + sequence parallel
bash run_qwen_05_sp2_liger.sh     # + Liger kernels
```

### 7.5 DAPO (this fork)

```bash
bash prepare_dapo_data.sh                       # build DAPO training data
bash run_dapo_qwen2.5_32b.sh                    # full DAPO run on Qwen2.5-32B
bash run_dapo_early_qwen2.5_32b.sh              # early-stage variant
bash test_dapo_7b.sh                            # smoke test on a 7B model
```

### 7.6 PRIME (this fork)

```bash
bash run_prime_qwen.sh        # PRIME RL with implicit process rewards
```

### 7.7 SFT

```bash
bash run_sft.sh
```

SFT config: `verl/trainer/config/sft_trainer.yaml`; trainer: `verl/trainer/fsdp_sft_trainer.py` (supports LoRA/PEFT and multimodal data via `vision_utils.py`).

### 7.8 Evaluate an R1-distilled model (this fork)

```bash
bash run_r_distill_qwen.sh                     # train / setup R1-distill Qwen pipeline
bash run_r1_distill_qwen_aime24_eval.sh        # evaluate on AIME24 / MATH / GPQA / LiveCodeBench
python check_results.py                        # aggregate & verify eval outputs
```

### 7.9 One-shot pipelines

```bash
bash run_master.sh   # end-to-end: data → training → evaluation
bash run_all.sh      # run the full set of fork experiments
```

### 7.10 Interactive tutorial

Open `verl_getting_started.ipynb` or `tutorial.ipynb` for a step-by-step Colab-style walkthrough (PPO on GSM8K, inspecting the dataflow DAG, resuming from checkpoints).

---

## 8. Architecture

### 8.1 HybridFlow: a DAG of roles

An RLHF job is a dataflow graph over five roles:

```
            ┌────────────────┐
            │ Rollout (vLLM) │  generate trajectories
            └───────┬────────┘
                    │
        ┌───────────┼────────────┬─────────────┐
        ▼           ▼            ▼             ▼
┌────────────┐ ┌─────────┐ ┌──────────┐ ┌───────────────┐
│ Reference  │ │ Actor   │ │ Critic   │ │ Reward Model  │
│ Policy     │ │ (train) │ │ (train)  │ │ / rule reward │
└────────────┘ └─────────┘ └──────────┘ └───────────────┘
```

- **Single controller** (`verl/single_controller`): a Python-side controller (like `DataParallel`) that dispatches methods onto worker groups. You write normal-looking code (`batch = actor.update_critic(batch)`), and the framework handles placement, dispatch, and data sharding.
- **Multi-controller workers** (`verl/workers`): each role is an SPMD worker (FSDP or Megatron) that processes a shard of the batch.
- **Sharding managers** (`verl/workers/sharding_manager`): re-distribute weights between training and rollout formats (FSDP⇄vLLM, FSDP⇄SGLang, Megatron⇄vLLM), including Ulysses sequence-parallel sharding.
- **Hybrid engine**: colocate rollout and training on the same GPUs — generate with vLLM, free KV-cache, reshard weights, train with FSDP/Megatron, repeat.

### 8.2 Where each piece lives

| Concern | File(s) |
|---|---|
| Algorithm (advantage, KL, loss) | `verl/trainer/core_algos.py`, `prime_core_algos.py`, `dapo_ray_trainer.py` |
| Orchestration / fit loop | `verl/trainer/ray_trainer.py`, `prime_ray_trainer.py`, `dapo_ray_trainer.py` |
| Role workers (FSDP) | `verl/workers/fsdp_workers.py` |
| Role workers (Megatron) | `verl/workers/megatron_workers.py` |
| Policy gradient actors | `verl/workers/actor/{dp_actor,megatron_actor}.py` |
| Critics | `verl/workers/critic/{dp_critic,megatron_critic}.py` |
| Rollouts | `verl/workers/rollout/*` |
| Weight re-sharding | `verl/workers/sharding_manager/*` |
| Single controller core | `verl/single_controller/base/*`, `verl/single_controller/ray/*` |
| Model-specific Megatron kernels | `verl/models/{llama,qwen2,qwen2_vl}` |
| vLLM/SGLang integrations | `verl/third_party/{vllm,sglang}` |
| Datasets / rewards / metrics | `verl/utils/dataset`, `verl/utils/reward_score`, `verl/trainer/metric_utils.py` |

---

## 9. Trainers & Entry Points

| Trainer | Entry point | Config | Scripts |
|---|---|---|---|
| PPO / GRPO / RLOO / ReMax / ReInforce++ | `verl/trainer/main_ppo.py` | `verl/trainer/config/ppo_trainer.yaml` | `examples/ppo_trainer/run_*.sh`, `examples/grpo_trainer/run_*.sh` |
| PPO (Megatron backend) | `verl/trainer/main_ppo.py` | `verl/trainer/config/ppo_megatron_trainer.yaml` | `run_ppo_trainer_megatron.sh`, `run_qwen2-7b_megatron.sh`, `run_deepseek_megatron.sh` |
| Split PPO (disaggregated) | `main_ppo_split.py` | `ppo_trainer_split.yaml` | `run_deepseek7b_llm_sp2.sh` |
| **DAPO** | `main_dapo.py` | `dapo_trainer.yaml` | `run_dapo_qwen2.5_32b.sh` |
| **PRIME** | `main_prime.py` | `prime_trainer.yaml` | `run_prime_qwen.sh` |
| SFT (FSDP, LoRA-capable) | `verl/trainer/fsdp_sft_trainer.py` | `verl/trainer/config/sft_trainer.yaml` | `run_sft.sh` |
| Evaluation | `main_eval.py` | `evaluation.yaml` | `run_r1_distill_qwen_aime24_eval.sh`, `run_master.sh` |
| Batch generation | `verl/trainer/main_generation.py` | `verl/trainer/config/generation.yaml` | `run_gen_qwen05.sh` |

Function-reward vs model-reward smoke tests: `run_function_reward.sh`, `run_model_reward.sh`; removal-padding example: `run_ray_trainer_rmpad.sh`; FIRE-sampling example: `run_ray_trainer_fire_sampling.sh`.

---

## 10. Rollout / Inference Engines

Implemented in `verl/workers/rollout/`:

| Rollout | File | Notes |
|---|---|---|
| vLLM (worker-based) | `vllm_rollout.py` | classic per-worker vLLM engine |
| vLLM SPMD | `vllm_rollout_spmd.py` | every worker shares one engine; best throughput for large models (vLLM ≥ 0.6.3) |
| **FIRE sampling** | `fire_vllm_rollout.py` | fork addition — optimized sampling loop; enable via `run_ray_trainer_fire_sampling.sh` |
| SGLang | `sglang_rollout.py` | RadixAttention-based server rollout |
| HuggingFace | `hf_rollout.py` | dependency-free baseline |
| Naive | `naive_rollout.py` | simple greedy/sampling for tests |

Version-specific integration code (weight loading, SPMD engine, worker glue) lives in `verl/third_party/vllm/` (0.5.x, 0.6.3, 0.7, 0.8) and `verl/third_party/sglang/`. Migration notes: `README_vllm0.7.md`, `README_vllm0.8.md`.

---

## 11. Reward Functions & Sandbox

### 11.1 Built-in reward functions (`verl/utils/reward_score/`)

| Function | Task |
|---|---|
| `gsm8k.py` | GSM8K exact-match math |
| `math.py`, `math_normalize.py`, `grader.py` | MATH benchmark grading |
| `math_dapo.py`, `math_batch.py` | fork additions — DAPO-style & batched math rewards |
| `math_verify.py` | robust symbolic math verification |
| `geo3k.py` | geometry (Multimodal Geo3K) reward |
| `testing_util.py`, `utils.py` | helpers for code/test-case rewards |

A fork-level dispatcher lives in `reward_score.py`; validate custom reward wiring with `check_custom_rwd_fn.py`.

### 11.2 Sandbox code execution

For code RL (e.g., LiveCodeBench), untrusted generations are executed in an isolated service:

```bash
bash run.sh                 # start the sandbox server (server.py)
python client.py            # submit & fetch execution results
pytest tests/test_sandbox.py
```

### 11.3 Reward models

Model-based rewards run through `verl/workers/reward_model/` workers, and PRIME's implicit PRM through `prime_dp_rm.py`.

---

## 12. Data Preparation

All datasets are read as **parquet** with a prompt column consumed by `verl/utils/dataset/rl_dataset.py` (RL), `sft_dataset.py` (SFT), `rm_dataset.py` (reward-model training) and `multiturn_sft_dataset.py` (multi-turn SFT).

Preprocessors in `examples/data_preprocess/`:

| Script | Dataset |
|---|---|
| `gsm8k.py` | GSM8K math word problems |
| `math_dataset.py` | MATH competition problems |
| `full_hh_rlhf.py` | Full HH-RLHF preference data |
| `hellaswag.py` | HellaSwag multiple choice |
| `geo3k.py` | Multimodal geometry |
| `multiturn.py` | Multi-turn conversations |
| `prepare_dapo_data.sh` / `create_dataset.py` | DAPO-style data & generic dataset creation |

`create_model_tokenizer.py` builds a small local model + tokenizer (`config.json`, `tokenizer_config.json`, `generation_config.json`, `model.safetensors`) for quick smoke tests without downloading checkpoints.

For HDFS-backed storage, `verl/utils/fs.py` + `hdfs_io.py` provide transparent local/HDFS IO.

---

## 13. Configuration System

Configs are [Hydra](https://hydra.cc) YAMLs; every trainer accepts CLI overrides:

```bash
python -m verl.trainer.main_ppo \
    config_name=ppo_trainer \
    trainer.total_epochs=2 \
    algorithm.adv_estimator=grpo \
    actor_rollout_ref.rollout.name=vllm \
    actor_rollout_ref.rollout.gpu_memory_utilization=0.5
```

Key config groups (see `docs/config.rst`):

- `data` — train/val files, prompt keys, max lengths, dataloader batching
- `actor_rollout_ref` — actor/critic/reference/rollout models, FSDP/Megatron options, rollout engine + sampling params, LoRA options
- `critic`, `reward_model` — model paths, optimizers, sharding
- `algorithm` — advantage estimator, KL controller, gamma/lam, clip ranges (incl. DAPO clip-higher)
- `trainer` — project/experiment names, logger (console / tracking with TensorBoard / WandB / MLFlow), total epochs, checkpoint settings, nnodes & GPUs per node

Recipe configs: `dapo_trainer.yaml`, `prime_trainer.yaml`, `evaluation.yaml`.

---

## 14. Evaluation Suite

The evaluation pipeline (`main_eval.py` + `evaluation.yaml`) runs checkpoint-agnostic, batch generation + scoring over benchmark-specific loaders:

| Benchmark | Loader | Notes |
|---|---|---|
| **MATH / AIME24** | `math.py` | verified symbolic grading (`math_verify`) |
| **GPQA** | `gpqa.py` | graduate-level science QA |
| **LiveCodeBench** | `livecodebench.py` | code generation scored via the sandbox executor |
| arbitrary prompts | `data_process.py` | build eval sets from raw JSON/parquet |

Typical flow for R1-distill models:

```bash
bash run_r1_distill_qwen.sh                 # prepare/launch distill-Qwen pipeline
bash run_r1_distill_qwen_aime24_eval.sh     # AIME24 + MATH eval with vLLM generation
python check_results.py                     # collect scores, write summary tables
```

`run_master.sh` chains data preparation → training → evaluation and is the recommended entry point for full experiments; `diagnose.py` helps debug hung jobs.

---

## 15. Checkpointing & Model Utilities

- **Checkpoint managers** — `verl/utils/checkpoint_manager.py` (generic), `fsdp_checkpoint_manager.py` (FSDP sharded state), `megatron_checkpoint_manager.py` (Megatron distributed checkpoints). Automatic model/optimizer/sampler state saving with per-step recovery; correctness tests in `test_fsdp_ckpt.py`.
- **`model_merger.py`** — merge FSDP/DCP/Megatron sharded checkpoints into a single HF checkpoint for inference/upload.
- **`converter_hf_to_mcore.py`** — convert HuggingFace weights to Megatron-core format (and back), per `verl/models/mcore/{loader,saver,config_converter}.py`.
- **`verl/utils/megatron_utils.py`** — Megatron initialization helpers (TP/PP/CP/EP/SP group construction).

---

## 16. Multi-Node & SLURM

- **Ray**: set `trainer.nnodes` / `trainer.n_gpus_per_node`; the controller auto-creates a Ray multi-node placement group.
- **SLURM**: submit `ray_on_slurm.slurm` to bootstrap a Ray cluster across SLURM nodes, then run any trainer script on top.
- **Split / disaggregated PPO**: `main_ppo_split.py` demonstrates roles spread across *separate* worker groups rather than colocated.

---

## 17. Docker Images

All Dockerfiles live at the repo root (see table in §6.3). Build example:

```bash
docker build -f Dockerfile.ngc.vllm0.8 -t verl-loras:ngc-vllm0.8 .
docker run --gpus all --shm-size=32g -it verl-loras:ngc-vllm0.8 bash
```

---

## 18. Testing

The `tests/` directory is a pytest suite (`kill_github_tests.sh` provides CI cleanup; `check_license.py` validates headers; `Makefile` + `format.sh` handle lint/format).

| Area | Tests |
|---|---|
| HybridFlow core | `test_rvdz.py`, `test_driverfunc_to_worker.py`, `test_worker_group_torch.py`, `test_check_worker_alive.py`, `test_data_transfer.py`, `test_high_level_scheduling_api.py`, `test_worker_group_basics.py`, `test_colocated_workers.py`, `test_ray_local_envs.py`, `test_import_utils.py`, `test_import.py` |
| Tensor / math ops | `test_tensor_dict.py`, `test_tensor_dict_utilities.py`, `test_torch_functional.py`, `test_ops.py`, `test_memory_buffers.py` |
| Parallelism | `test_transformers_ulysses.py`, `test_transformer.py`, `test_sp_loss_match.py` |
| Engines | `test_vllm_spmd.py`, `test_sglang_spmd.py`, `test_vllm_hf_loader.py`, `run_fsdp_vllm.py` |
| Datasets | `test_rl_dataset.py`, `test_sft_dataset.py`, `test_rm_dataset.py`, `test_multiturn_sft_dataset.py` |
| Recipes | `test_dapo_7b.sh`, sandbox: `test_sandbox.py` |
| Model loader | `test_fsdp_ckpt.py`, `check_model.py`-style sanity via `model.safetensors` fixtures |

Run everything:

```bash
pytest tests/ -x
```

---

## 19. Documentation

Sphinx docs (build with `sphinx-build -b html docs/ docs/_build`):

| Document | Content |
|---|---|
| `docs/index.rst` | landing page & TOC |
| `docs/install.rst` | detailed install (incl. Megatron) |
| `docs/quickstart.rst`, `docs/gsm8k_example.rst` | first training runs |
| `docs/data.rst`, `docs/prepare_data.rst` | dataset formats & preprocessing |
| `docs/hybrid_flow.rst`, `docs/ppo.rst`, `docs/ppo_code_architecture.rst` | HybridFlow design, PPO internals |
| `docs/ray_trainer.rst`, `docs/config.rst` | trainer API & config reference |
| `docs/fsdp_workers.rst`, `docs/megatron_workers.rst`, `docs/sglang_worker.rst` | backend worker details |
| `docs/fsdp_extension.rst`, `docs/megatron_extension.rst`, `docs/dpo_extension.rst`, `docs/reward_function.rst` | extending the framework |
| `docs/placement.rst` | multi-node resource placement |
| `docs/checkpoint.rst` | checkpoint/resume semantics |
| `docs/perf_tuning.rst`, `docs/device_tuning.rst` | performance & device tuning |
| `docs/multinode.rst` | multi-node & SLURM setup |
| `docs/faq.rst` | common issues |
| `README_vllm0.7.md`, `README_vllm0.8.md` | vLLM version migration notes |

---

## 20. Performance Tuning

Quick wins (full details in `docs/perf_tuning.rst` / `docs/device_tuning.rst`):

- Use **SPMD vLLM** (`vllm_rollout_spmd`) for ≥ 7B models — avoids per-worker engine overhead.
- Enable **removal padding** (`run_ray_trainer_rmpad.sh`) to skip attention on padding tokens.
- Enable **sequence balancing** (`*_seq_balance.sh` scripts + `seqlen_balancing.py`) to even out long-sample hot spots across DP ranks.
- Use **Ulysses / sequence parallelism** for long contexts (`verl/utils/ulysses.py`, `sequence_parallel.py`).
- Try the **FIRE rollout** (this fork) or **SGLang** rollout for faster generation.
- Enable **Liger kernels** (`run_qwen_05_sp2_liger.sh`) and dynamic batch sizing for SFT.
- Monitor memory with `verl/utils/memory.py`, FLOPs with `flops_counter.py`, and use `memory_buffer.py` for FSDP memory pooling; `trajectory_tracker.py` and `performance.py` expose per-stage timings.

---

## 21. Contributing

1. Fork & branch; run `bash format.sh` (ruff/black/isort via `Makefile`).
2. Ensure headers pass `check_license.py`.
3. Add/extend tests under `tests/` and keep recipes reproducible via their `run_*.sh` scripts.
4. For new RL algorithms, prefer adding an advantage estimator / loss in `core_algos.py` and a thin trainer variant — see `docs/dpo_extension.rst` and `docs/fsdp_extension.rst` for patterns.

---

## 22. License

This project is released under the **Apache License 2.0** — see [`LICENSE`](./LICENSE). Third-party notices are collected in [`Notice.txt`](./Notice.txt).

---

## 23. Acknowledgements & Citation

This fork builds on **verl** and benefits from **Megatron-LM**, **vLLM**, **SGLang**, **Ray**, **HuggingFace Transformers**, **DAPO** and **PRIME** research. If you use this codebase, please cite:

```bibtex
@article{sheng2024hybridflow,
  title   = {HybridFlow: A Flexible and Efficient RLHF Framework},
  author  = {Sheng, Guangming and Zhang, Quan and Yin, Zefan and Zang, Ting and Lu, Chen and Xiao, Xue and Zheng, Hao and Liu, Kaixiong and Xue, Gang and Zhang, Yongbo},
  journal = {arXiv preprint arXiv:2409.19256},
  year    = {2024}
}

@article{dapo2025,
  title   = {DAPO: An Open-Source LLM Reinforcement Learning System at Scale},
  author  = {{ByteDance Seed}},
  journal = {arXiv preprint arXiv:2503.14476},
  year    = {2025}
}

@article{prime2025,
  title   = {Process Reinforcement through Implicit Rewards},
  author  = {Cui, Ganqu and Hu, Chen and Zhang, Lifan and others},
  journal = {arXiv preprint arXiv:2502.01456},
  year    = {2025}
}
```

*Happy RLHF training — and remember: start with a smoke test (`bash run_all.sh`) before scaling to 32B.* 🚀
