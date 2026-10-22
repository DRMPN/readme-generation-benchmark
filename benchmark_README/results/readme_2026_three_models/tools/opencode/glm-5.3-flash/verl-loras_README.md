# verl: Volcano Engine Reinforcement Learning for LLM

`verl` is a flexible, efficient and production-ready RL training framework designed for large language model (LLM) post-training. It is an open-source implementation of the [HybridFlow](https://arxiv.org/pdf/2409.19256) paper (package version in this tree: `0.2.0.dev`, see `verl/version/version`; upstream project: <https://github.com/volcengine/verl>).

verl adopts a hybrid programming model that combines a **single-controller** (the RL training loop, e.g. PPO, runs as a single Ray driver process) with **multi-controller** compute engines (FSDP / Megatron-LM training, vLLM / SGLang generation), decoupling the control flow of RL algorithms from the implementation of the compute engines. This makes it easy to define new RL dataflows in a few lines of code while reusing state-of-the-art training and inference infrastructure.

This repository is a copy of verl with additional multi-node deployment files (see [Multi-node training](#multi-node-training)).

## Highlights

- **Easy extension of diverse RL algorithms**: the hybrid programming model allows users to build RL dataflows in a few lines of code.
- **Seamless integration of existing LLM infra with modular APIs**: works with PyTorch FSDP, Megatron-LM, vLLM and SGLang; users can extend to other training and inference frameworks.
- **Flexible device mapping and parallelism**: various placements of models onto different sets of GPUs for efficient resource utilization and scalability across cluster sizes.
- **Ready integration with popular HuggingFace models**.
- **State-of-the-art throughput** by integrating existing SOTA LLM training and inference frameworks.
- **Efficient actor model resharding with 3D-HybridEngine**, which eliminates memory redundancy and reduces communication overhead during transitions between the training and generation phases.

## Supported backends and features

| Component | Options |
| --- | --- |
| Training engine | PyTorch **FSDP** (default), **Megatron-LM** via Megatron-Core 0.11 (`GPTModel`; Llama and Qwen2 migrated, supports tensor / pipeline / sequence / context / virtual-pipeline parallelism and `dist_checkpointing`) |
| Rollout / generation engine | **vLLM** (0.6.3 and 0.8.x tested; vendored shims for older versions in `verl/third_party/vllm`), **SGLang** (`0.4.4.post4`), HuggingFace transformers; HF TGI for debugging / single-GPU exploration |
| RL algorithms | PPO (`adv_estimator=gae`), GRPO, RLOO, ReMax, REINFORCE++ (`verl/trainer/ppo/core_algos.py`) |
| Recipe implementations | `recipe/dapo` (DAPO), `recipe/prime` (PRIME), `recipe/r1` (R1 distillation evaluation) |
| Supervised fine-tuning | FSDP SFT trainer (`verl.trainer.fsdp_sft_trainer`) with single-turn and multi-turn datasets, optional **LoRA via PEFT** (see below), Liger kernel, Ulysses sequence parallelism, remove-padding |
| Data | Parquet-based RL / SFT / reward-model datasets (`verl/utils/dataset`), preprocessing scripts in `examples/data_preprocess` (GSM8K, MATH, Geo3K, Full-HH-RLHF, Hellaswag, multiturn) |
| Rewards | Custom reward functions (`custom_reward_function.path/name`), rule-based scorers (`verl/utils/reward_score`: `gsm8k`, `math`, `geo3k`, `math_verify`, `prime_code`, `prime_math`, ...) and reward-model workers; reward managers `naive`, `batch`, `prime`, `dapo` |
| Other | Checkpointing and resume, dynamic batch sizing (token balancing), gradient checkpointing / CPU offload, `torch.compile`, tracking backends `console`, `wandb`, `mlflow`, `swanlab`, `vemlp_wandb`, `tensorboard` (`verl/utils/tracking.py`), multimodal data fields (`image_key` / `video_key`) |

## Requirements

- Python >= 3.9
- CUDA >= 12.1

For FSDP-based training, install `flash-attn` and (optionally) `liger-kernel`. Megatron-LM support additionally needs `apex`, TransformerEngine and `megatron-core==0.11.0`.

## Installation

### Docker (recommended)

Pre-built images are documented in `docs/start/install.rst`, for example:

- FSDP/Megatron with vLLM: `whatcanyousee/verl:ngc-th2.6.0-cu124-vllm0.8.2-mcore0.11.0-te2.0`
- SGLang with FSDP: `ocss884/verl-sglang:ngc-th2.5.1-cu126-sglang0.4.4.post4`

```bash
docker create --runtime=nvidia --gpus all --net=host --shm-size="10g" --cap-add=SYS_ADMIN -v .:/workspace/verl --name verl <image:tag>
docker start verl
docker exec -it verl bash
```

Additional Dockerfiles (NGC-based images, SGLang, ROCm/AMD, Megatron, vemlp) live in `docker/`.

### From source (custom environment)

```bash
conda create -n verl python==3.10
conda activate verl

pip3 install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu126
pip3 install flash-attn --no-build-isolation

git clone https://github.com/volcengine/verl.git
cd verl
pip3 install -e .            # base install
# or: pip3 install -e .[vllm]
# or: pip3 install -e .[sglang]
```

Optional extras declared in `setup.py`: `test`, `prime`, `geo`, `gpu`, `math`, `vllm`, `sglang`. AMD ROCm usage (MI300) is documented in `docs/start/install.rst` and `docker/Dockerfile.rocm`.

## Quickstart: PPO on GSM8K

1. **Preprocess the dataset** (parquet format with fields needed for reward computation):

   ```bash
   python3 examples/data_preprocess/gsm8k.py --local_dir ~/data/gsm8k
   ```

2. **Download a model** (e.g. `Qwen/Qwen2.5-0.5B-Instruct`); a GPU with at least 24 GB HBM is required for this example.

3. **Run PPO training** (`verl/trainer/main_ppo.py` uses Hydra config `verl/trainer/config/ppo_trainer.yaml`; every option can be overridden on the command line):

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
    actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=4 \
    critic.optim.lr=1e-5 \
    critic.model.path=Qwen/Qwen2.5-0.5B-Instruct \
    critic.ppo_micro_batch_size_per_gpu=4 \
    algorithm.kl_ctrl.kl_coef=0.001 \
    trainer.logger=['console'] \
    trainer.val_before_train=False \
    trainer.default_hdfs_dir=null \
    trainer.n_gpus_per_node=1 \
    trainer.nnodes=1 \
    trainer.save_freq=10 \
    trainer.test_freq=10 \
    trainer.total_epochs=15 2>&1 | tee verl_demo.log
   ```

Checkpoints are saved to `checkpoints/${trainer.project_name}/${trainer.experiment_name}` by default. To use Weights & Biases, set `trainer.logger=['console','wandb']` plus `trainer.project_name` and `trainer.experiment_name`. For GRPO-style training, set `algorithm.adv_estimator=grpo` and `actor_rollout_ref.rollout.n` > 1 (see `examples/grpo_trainer/` and the provided `run_master.sh`).

More scripts: `examples/ppo_trainer/` (FSDP and Megatron variants, DeepSeek/Gemma/Qwen), `examples/grpo_trainer/`, `examples/rloo_trainer/`, `examples/reinforce_plus_plus_trainer/`, `examples/remax_trainer/`, `examples/generation/` (batch generation via `verl.trainer.main_generation`), `examples/checkpoint/`, `examples/split_placement/`, and the runnable notebook `examples/ppo_trainer/verl_getting_started.ipynb`.

## SFT with LoRA (PEFT)

`verl.trainer.fsdp_sft_trainer` supports parameter-efficient fine-tuning through [PEFT](https://github.com/huggingface/peft). Setting `model.lora_rank` to a positive value (e.g. `32`) enables LoRA; `model.lora_alpha` and `model.target_modules` control the scaling factor and target modules (`all-linear`, or a list such as `[q_proj,v_proj]`). A dedicated FSDP wrap policy keeps trainable LoRA parameters unsharded (`verl/utils/fsdp_utils.py`), and checkpoints are saved with `save_pretrained`.

```bash
torchrun --standalone --nnodes=1 --nproc_per_node=$NPROC \
     -m verl.trainer.fsdp_sft_trainer \
    data.train_files=$HOME/data/gsm8k/train.parquet \
    data.val_files=$HOME/data/gsm8k/test.parquet \
    model.partial_pretrain=Qwen/Qwen2.5-0.5B-Instruct \
    model.lora_rank=32 \
    model.lora_alpha=16 \
    model.target_modules=all-linear \
    trainer.total_epochs=1
```

See `examples/sft/gsm8k/run_qwen_05_peft.sh` for the full script (tested with 2 and 4 GPUs) and `examples/sft/multiturn/` for multi-turn SFT.

## Multi-node training

verl runs on a Ray cluster: start a head node (`ray start --head`), join workers (`ray start --address=<head>`), then submit the training entry point with `ray job submit ... -- python3 -m verl.trainer.main_ppo trainer.nnodes=N trainer.n_gpus_per_node=M ...`. Step-by-step instructions, the Slurm example (`examples/slurm/ray_on_slurm.slurm`) and debugging tips are in `docs/start/multinode.rst`.

This repository additionally ships three deployment files for a two-node Ray cluster:

- `run_master.sh` — starts an SSH service and the Ray head node on port 6379, then submits a **GRPO** run on the GSM8K dataset with `Qwen2.5-Math-1.5B` via `ray job submit --runtime-env=verl/trainer/runtime_env.yaml` (2 nodes, configurable through Hydra overrides appended with `$@`).
- `run_worker.sh` — starts SSH, waits until `$MASTER_ADDR` resolves with `nslookup`, and joins the Ray cluster as a worker node.
- `.ml-job-preset.yml` — a job preset (master + worker jobs) that runs the two scripts above on a distributed job platform, mounting `./verl` sources and shell scripts into the container and pulling the model/dataset from object storage. The container image, S3 buckets and regions referenced in this file are environment-specific — adapt them (or your platform's equivalents) before use.

## Documentation

The Sphinx documentation lives in `docs/` (also published via Read the Docs, see `.readthedocs.yaml`). Build it locally:

```bash
pip install -r docs/requirements-docs.txt
cd docs && make clean && make html
python -m http.server -d _build/html/   # open http://localhost:8000
```

Notable pages: installation and quickstart (`docs/start/`), the HybridFlow programming guide (`docs/hybrid_flow.rst`), data preparation (`docs/preparation/`), full config explanation (`docs/examples/config`), performance tuning (`docs/perf/`), worker guides (`docs/workers/`), FSDP/Megatron/DPO extension guides (`docs/advance/`), and the FAQ (`docs/faq/`). Notes on upgrading to vLLM >= 0.8 are in `docs/README_vllm0.8.md`.

## Repository layout

```
verl/                  Core package
├── trainer/           Entry points (main_ppo, main_generation, main_eval), FSDP SFT trainer,
│                      Hydra configs (trainer/config/*.yaml), PPO trainer and core algorithms
├── workers/           Actor / critic / reward-model / rollout workers (fsdp_workers, megatron_workers),
│                      sharding managers, reward managers, rollout backends (vllm, sglang, hf, naive)
├── single_controller/ Single-controller abstractions: worker groups, Ray-based dispatch, registration
├── models/            Parallelizable model implementations (llama, qwen2, transformers monkey patches,
│                      Megatron-Core registry and converters)
├── third_party/       Vendored vLLM versions (0.3.1 / 0.4.2 / 0.5.4 / 0.6.3) and SGLang helpers
├── utils/             Datasets, reward scorers, FSDP/Megatron utilities, checkpointing, HDFS I/O
└── protocol.py        DataProto: the data protocol exchanged between controller and workers

examples/              Ready-to-run training / generation / data-preprocessing scripts
recipe/                DAPO, PRIME and R1 recipe implementations
docs/                  Sphinx documentation
docker/                Dockerfiles (NGC, SGLang, ROCm, Megatron, vemlp)
tests/                 Unit, distributed, and end-to-end tests (ray, rollout, sft, ...)
scripts/               Utilities: HF→Megatron converter, model merger, diagnostics
.github/workflows/     CI: e2e PPO/SFT/DAPO/PRIME/Megatron, Ray tests, pylint, yapf, sanity checks
```

## Development and contributing

- Code formatting uses `yapf` (Google style, config in `.style.yapf`):

  ```bash
  pip3 install yapf
  yapf -ir -vv --style ./.style.yapf verl examples tests
  ```

- Linting uses `pylint` (config in `pyproject.toml`); tests use `pytest` (`pip install -e .[test]`).
- When contributing features, please add a CI test: find the relevant workflow in `.github/workflows/` (which maps to a Hydra config such as `ppo_trainer` or `sft_trainer`), add path patterns to its `paths` section, and keep the test scripts small.

verl is free software; you can redistribute it and/or modify it under the terms of the Apache License 2.0. We welcome contributions — discussions happen on [GitHub](https://github.com/volcengine/verl) and [Slack](https://join.slack.com/t/verlgroup/shared_invite/zt-2w5p9o4c3-yy0x2Q56s_VlGLsJ93A6vA).

## Citation

If you use verl in your research, please cite the HybridFlow paper: <https://arxiv.org/pdf/2409.19256>.

## License

This project is licensed under the [Apache License 2.0](LICENSE). Copyright 2023-2024 Bytedance Ltd. and/or its affiliates (see `Notice.txt`); verl is authored by Bytedance - Seed - MLSys.
