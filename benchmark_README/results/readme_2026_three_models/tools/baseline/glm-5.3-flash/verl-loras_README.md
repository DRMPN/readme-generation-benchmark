# verl: Volcano Engine Reinforcement Learning for LLM

verl is a flexible, high-performance reinforcement learning (RL) training framework for large language models (LLMs), developed by the ByteDance Seed MLSys team. It implements RLHF-style training pipelines—such as PPO, GRPO, REINFORCE++, ReMax, RLOO, DAPO, and PRIME—on top of a Ray-based distributed architecture, with pluggable training backends (PyTorch FSDP and Megatron-LM) and pluggable rollout/inference engines (vLLM, SGLang, and HuggingFace). It also includes supervised fine-tuning (SFT) support.

## Overview

verl is organized around a "single controller, multiple workers" design:

- **Single controller** (`verl/trainer/ppo/ray_trainer.py`): A driver process (typically CPU-only) runs the training loop. It loads batches of prompts from preprocessed parquet files via the `RLHFDataset` class, dispatches data to distributed workers, computes lightweight quantities such as advantages on the driver, and orchestrates the PPO dataflow.
- **Workers** (`verl/workers/`): Each role—actor, critic, reference model, rollout, and reward model—is implemented as a worker class registered with Ray. Worker APIs are decorated with `@register(dispatch_mode=...)` transfer protocols (e.g., `ONE_TO_ALL`, `DP_COMPUTE_PROTO`, Megatron-specific protocols) defined in `verl/single_controller/base/decorator.py`, which handle data dispatch and collection across GPUs.
- **Data protocol** (`verl/protocol.py`): All data exchanged between the controller and workers is wrapped in `DataProto` objects.
- **Hybrid engine**: Actor and rollout weights are resharded between the training backend and the inference engine by sharding managers such as `FSDPVLLMShardingManager` and `MegatronVLLMShardingManager` (`verl/workers/sharding_manager/`), so the same GPUs can switch between training and generation with low overhead.

### Supported backends and engines

- **Training backends**
  - **PyTorch FSDP** (`verl/workers/fsdp_workers.py`): recommended for algorithm research and prototyping; readily supports models available in HuggingFace/transformers. Notably, FSDP hybrid shard is not supported.
  - **Megatron-LM** (`verl/workers/megatron_workers.py`): supports 3D parallelism (tensor, pipeline, data) and sequence parallelism for best scalability on large models (e.g., 70B/405B). Custom model implementations for Llama and Qwen2 are provided under `verl/models/llama/` and `verl/models/qwen2/`, with Megatron-Core model utilities in `verl/models/mcore/`.
- **Rollout engines**
  - **vLLM**: multiple versions are supported via pinned, adapted copies under `verl/third_party/vllm/` (v0.3.1 through v0.6.3), executed under SPMD to fit the WorkerGroup design. CUDA-graph and sleep-mode support are available for vLLM >= 0.7 (see `docs/README_vllm0.7.md` and `docs/README_vllm0.8.md`).
  - **SGLang**: fully supported as a rollout backend with the same feature coverage as vLLM, including memory saving and multi-node rollout. Switch by adding `actor_rollout_ref.rollout.name=sglang` to the launch command (see `docs/workers/sglang_worker.rst`).
  - **HuggingFace** (`verl/workers/rollout/hf_rollout.py`).

### Algorithms and recipes

- Core RL algorithms: PPO (`verl/trainer/ppo/core_algos.py`, entry point `verl/trainer/main_ppo.py`), GRPO, REINFORCE++, ReMax, and RLOO (example scripts under `examples/`).
- **DAPO recipe** (`recipe/dapo/`): an open-source implementation of Decoupled Clip and Dynamic sAmpling Policy Optimization, including clip-higher (`clip_ratio_low`/`clip_ratio_high`), dynamic sampling with group filtering, token-level loss aggregation (`loss_agg_mode`), and overlong reward shaping. Applying DAPO to Qwen2.5-32B reaches 50% on AIME 2024 with 50% fewer training steps.
- **PRIME recipe** (`recipe/prime/`), and **R1 distill evaluation** (`recipe/r1/`) with reward functions for math, GPQA, and LiveCodeBench tasks.
- **SFT** support via `verl/trainer/fsdp_sft_trainer.py` and `verl/trainer/config/sft_trainer.yaml`, including multi-turn SFT datasets (`verl/utils/dataset/multiturn_sft_dataset.py`).
- Rule-based reward functions for GSM8K, MATH (Geo3K), and code/math graders reused from PRIME (`verl/utils/reward_score/`).

## Installation

Requirements: Python >= 3.8. Core dependencies include `torch` (installed transitively), `ray[default]`, `transformers`, `datasets`, `hydra-core`, `tensordict`, `flash-attn`, and `wandb` (see `requirements.txt`).

```bash
git clone https://github.com/volcengine/verl.git
cd verl
pip install -e .               # base install
```

Optional extras are defined in `setup.py`:

```bash
pip install -e .[vllm]         # vLLM rollout backend
pip install -e .[sglang]       # SGLang rollout backend (sglang[all]==0.4.4.post4, torch-memory-saver)
pip install -e .[prime]        # PRIME algorithm dependencies
pip install -e .[geo]          # Geo3K reward dependencies (mathruler)
pip install -e .[math]         # math-verify based rewards
pip install -e .[gpu]          # liger-kernel, flash-attn
pip install -e .[test]         # pytest, yapf, py-spy
```

For the vLLM >= 0.7 + FSDP setup, a dedicated conda environment is recommended:

```bash
conda create -n verl python==3.10
conda activate verl
pip3 install -e .
pip3 install vllm==0.7.3
pip3 install flash-attn --no-build-isolation
```

Older vLLM versions (0.7.0–0.7.2) require small manual patches to `parallel_state.py`, `uniproc_executor.py`, and `weight_utils.py` (documented in `docs/README_vllm0.7.md`). Docker images for various environments (Megatron, NGC+vLLM, ROCm/AMD, SGLang, Volcano Engine ML Platform) are provided under `docker/`.

## Usage

### Data preparation

Preprocess your datasets into parquet files using the scripts in `examples/data_preprocess/`, e.g.:

```bash
python3 examples/data_preprocess/gsm8k.py
```

Available preprocessing scripts cover GSM8K, Geo3K, Full HH-RLHF, HellaSwag, MATH, and multi-turn data. Set `VERL_USE_MODELSCOPE=True` to download models from ModelScope instead of HuggingFace.

### Running PPO training

PPO training is launched with Hydra-style configuration overrides:

```bash
PYTHONUNBUFFERED=1 python3 -m verl.trainer.main_ppo \
    data.train_files=$HOME/data/gsm8k/train.parquet \
    data.val_files=$HOME/data/gsm8k/test.parquet \
    data.train_batch_size=256 \
    data.max_prompt_length=512 \
    data.max_response_length=256 \
    actor_rollout_ref.model.path=Qwen/Qwen2.5-0.5B-Instruct \
    actor_rollout_ref.actor.optim.lr=1e-6 \
    actor_rollout_ref.actor.ppo_mini_batch_size=64 \
    actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=4 \
    actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=8 \
    actor_rollout_ref.rollout.tensor_model_parallel_size=1 \
    actor_rollout_ref.rollout.gpu_memory_utilization=0.4 \
    critic.optim.lr=1e-5 \
    critic.model.path=Qwen/Qwen2.5-0.5B-Instruct \
    algorithm.kl_ctrl.kl_coef=0.001 \
    trainer.logger=['console','wandb'] \
    trainer.n_gpus_per_node=1 \
    trainer.nnodes=1 \
    trainer.save_freq=10 \
    trainer.test_freq=10 \
    trainer.total_epochs=15
```

Checkpoints are saved under `checkpoints/${trainer.project_name}/${trainer.experiment_name}` by default. For low-memory GPUs (< 32GB), reduce `ppo_micro_batch_size_per_gpu` to 1 for the actor and critic.

The main configuration files live in `verl/trainer/config/` (`ppo_trainer.yaml`, `ppo_megatron_trainer.yaml`, `sft_trainer.yaml`, `generation.yaml`, `evaluation.yaml`). All settings can be overridden on the command line via Hydra dot-notation. Full documentation for every option is available in the Sphinx docs (`docs/`).

### Multi-node and cluster deployment

- Multi-node training with Ray: start a Ray cluster (`ray start --head` / `ray start --address=...`) on your nodes, then launch training with `trainer.nnodes` > 1. Cross-machine rollout with large tensor-parallel sizes (e.g., TP=16 across two machines) is supported for both IPv4 and IPv6 (see the SGLang worker docs).
- Slurm: an example Ray-on-Slurm launcher is provided at `examples/slurm/ray_on_slurm.slurm`.
- Ray job submission: set `RAY_ADDRESS`, `WORKING_DIR`, and `RUNTIME_ENV` (see `verl/trainer/runtime_env.yaml`) to submit jobs remotely, as demonstrated in the DAPO recipe.

### Other entry points

- Generation: `verl/trainer/main_generation.py` (config: `verl/trainer/config/generation.yaml`)
- Evaluation: `verl/trainer/main_eval.py` (used by the R1 recipe to evaluate on AIME 2024, GPQA, and LiveCodeBench)
- Checkpoint conversion: `scripts/converter_hf_to_mcore.py` and `scripts/model_merger.py` for Megatron checkpoint utilities

## Development

### Repository layout

- `verl/` — the core library: `single_controller/` (Ray-based worker group abstraction), `workers/` (actor, critic, reward manager/model, rollout, sharding managers), `trainer/` (PPO/SFT trainers, configs), `models/` (Megatron and transformers model implementations), `utils/` (datasets, reward scoring, checkpoint managers, FSDP/Megatron utilities, ulysses sequence parallelism, seqlen balancing), and `third_party/` (adapted vLLM and SGLang code).
- `examples/` — runnable shell scripts and notebooks, including `verl_getting_started.ipynb`, a Ray tutorial, split placement examples, GRPO/PPO/RLOO/ReMax/REINFORCE++ launchers, and tuning guides for 7B/14B/70B models on H800/H20 hardware.
- `recipe/` — complete algorithm implementations (DAPO, PRIME, R1 eval).
- `docs/` — Sphinx documentation; build with `pip install -r docs/requirements-docs.txt` followed by `make clean && make html` in `docs/`, then serve with `python -m http.server -d _build/html/`.
- `patches/` — Megatron v4 compatibility patch.

### Code style and linting

- Formatting uses **yapf** (`.style.yapf`); run `bash scripts/format.sh` to format code. A `yapf_format.yml` GitHub workflow enforces formatting in CI.
- Linting uses **pylint==3.3.6**, configured via `[tool.pylint.message_control]` in `pyproject.toml`.
- A license header sanity check is performed by `tests/sanity/check_license.py`; source files carry the Apache 2.0 header (Copyright 2024 Bytedance Ltd. and/or its affiliates).

### Continuous integration

The project ships a large GitHub Actions suite under `.github/workflows/`, including end-to-end tests for PPO (FSDP and Megatron), SFT, GRPO/DAPO/PRIME recipes, AIME 24 evaluation, dataset and model workflows, Ray unit tests, vLLM tests, sandbox tests, sanity/import checks, pylint, yapf formatting, secret scanning, and OpenSSF Scorecard.

## Testing

Tests are located in `tests/` and can be run with `pytest` (install the `[test]` extra first):

- **Unit tests**: tensor dictionaries, torch functional operations, memory buffers, transformers with Ulysses, FLOPs-related utilities, module imports.
- **Ray tests** (`tests/ray/`): worker group basics, torch-distributed worker groups, data transfer, colocation, high-level scheduling, detached workers, and worker liveness checks.
- **Rollout tests** (`tests/rollout/`): vLLM SPMD and HF-loader tests, SGLang SPMD tests.
- **Dataset tests** (`tests/verl/utils/dataset/`): RL, SFT, RM, and multi-turn SFT datasets.
- **End-to-end tests** (`tests/e2e/`): full training runs driven by shell scripts (e.g., `tests/e2e/run_test.sh`, `run_ray_trainer.sh`, `run_ppo_trainer_megatron.sh`, `run_sft.sh`), using a tiny arithmetic-sequence toy model/environment to validate the full RL pipeline, including custom reward functions and hybrid (function + model) rewards.
- **Distributed tests** (`tests/distributed/`): run via `tests/distributed/run_all.sh`.

Example end-to-end validation scripts live alongside the workflows so that both local and CI runs exercise the same paths.

## Extending

- **Adding a new HuggingFace model**: copy the model file from `transformers` into `verl/models/`, strip inference/KV-cache code, switch to packed inputs (`input_ids`, `cu_seqlens`, `max_seqlen_in_batch`) with flash attention, add correctness tests against the HF reference, and implement tensor/data (FSDP2) parallel wrappers (see `verl/models/README.md`).
- **Adding new RLHF algorithms** such as DPO or GRPO on top of the existing trainer is documented in `docs/advance/dpo_extension.rst` and the FSDP/Megatron extension guides.

## Documentation

Full documentation (quickstart, installation, multinode, hybrid engine architecture, backend worker internals, performance tuning, checkpointing, FAQ, and more) is built from `docs/` and published on Read the Docs (`verl.readthedocs.io`, configured via `.readthedocs.yaml`).

## License

This project is licensed under the **Apache License 2.0** (see `LICENSE`). Redistribution must comply with the terms of the license; a `Notice.txt` file is included with third-party attribution notices.
