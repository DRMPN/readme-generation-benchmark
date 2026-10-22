# verl: Volcano Engine Reinforcement Learning for LLMs

verl is a reinforcement learning (RL) training framework for post-training large language models (LLMs). The project describes itself as "flexible, efficient and production-ready" and is an open-source implementation of the [HybridFlow](https://arxiv.org/pdf/2409.19256) paper. The package is published as `verl` and is licensed under the Apache License 2.0.

## Overview

verl is designed around a hybrid programming model that combines single-controller and multi-controller paradigms. According to the project documentation, this allows users to express RL dataflows in a few lines of code and to extend them to other RL algorithms.

Key characteristics described in the documentation:

- **Algorithm extensibility:** The control flow of an RL algorithm (for example, PPO) runs in a single driver process, while computation runs in distributed worker groups. The repository includes PPO, GRPO, ReMax, RLOO, REINFORCE++, and DAPO-related configurations and recipes.
- **Backend integration:** Training uses PyTorch FSDP or Megatron-LM. Rollout (generation) uses vLLM, SGLang, or Hugging Face TGI.
- **Flexible device mapping:** Models can be placed onto different sets of GPUs, including co-located placement where all roles share one resource pool.
- **Hugging Face compatibility:** The FSDP backend can work with Hugging Face models, and the documentation describes weight synchronization with vLLM.
- **3D-HybridEngine:** The documentation describes efficient actor model resharding between training and generation phases.

The repository is organized into the following main areas:

- `verl/`: the core package, including the trainers (`verl/trainer`), workers (`verl/workers`), the single-controller layer (`verl/single_controller`), model integrations (`verl/models`), vLLM/SGLang adaptors (`verl/third_party`), and utilities (`verl/utils`).
- `examples/`: shell scripts and notebooks for PPO, GRPO, ReMax, RLOO, REINFORCE++, SFT, checkpoint conversion, and data preprocessing.
- `recipe/`: larger reproduction projects, including DAPO, PRIME, and an R1 (DeepSeek-R1 distillation) evaluation recipe.
- `scripts/`: utilities such as `model_merger.py`, `converter_hf_to_mcore.py`, `diagnose.py`, and `format.sh`.
- `docs/`: Sphinx documentation.
- `tests/`: unit, integration, and end-to-end tests.
- `docker/`: Dockerfiles for NGC, vLLM, SGLang, Megatron, and ROCm environments.
- `.github/workflows/`: continuous integration workflows.

## Requirements

The installation documentation lists the following requirements:

- **Python:** 3.9 or later
- **CUDA:** 12.1 or later

The `pyproject.toml` and `setup.py` files declare `requires-python >= 3.8`. The guides use Python 3.10 in their conda examples.

## Installation

### Option 1: Docker images

The documentation provides pre-built images:

- `whatcanyousee/verl:ngc-th2.6.0-cu124-vllm0.8.2-mcore0.11.0-te2.0`: recommended for the latest vLLM with Megatron or FSDP. It includes PyTorch 2.6.0, CUDA 12.4, Megatron-LM v0.11.0, vLLM 0.8.2, and Ray 2.44.0.
- `ocss884/verl-sglang:ngc-th2.5.1-cu126-sglang0.4.4.post4`: for SGLang with FSDP.
- `hiyouga/verl:ngc-th2.6.0-cu126-vllm0.8.3-flashinfer0.2.2-cxx11abi0`: a vLLM 0.8.3 image referenced in the vLLM 0.8 upgrade guide.

Start a container and install verl inside it:

```bash
docker create --runtime=nvidia --gpus all --net=host --shm-size="10g" --cap-add=SYS_ADMIN -v .:/workspace/verl --name verl <image:tag>
docker start verl
docker exec -it verl bash
```

### Option 2: Custom environment

```bash
conda create -n verl python==3.10
conda activate verl

pip3 install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu126
pip3 install flash-attn --no-build-isolation
git clone https://github.com/volcengine/verl.git
cd verl
pip3 install -e .
```

To install a rollout backend, use an extra. The `setup.py` file defines the following extras: `test`, `prime`, `geo`, `gpu`, `math`, `vllm`, and `sglang`. For example:

```bash
pip3 install -e ".[vllm]"
# or
pip3 install -e ".[sglang]"
```

The `vllm` extra pins `vllm<=0.8.2`. The `sglang` extra pins `sglang[all]==0.4.4.post4`. The installation guide says vLLM 0.6.3 and 0.8.2 have been tested for stability and advises avoiding vLLM 0.7.x.

Megatron-LM is optional. The installation guide describes installing NVIDIA Apex, TransformerEngine, and `megatron-core==0.11.0`.

### AMD GPUs

For AMD MI300 GPUs with the ROCm platform, the documentation directs users to build and run `docker/Dockerfile.rocm`. It also says to set `HIP_VISIBLE_DEVICES` and `ROCR_VISIBLE_DEVICES` when starting Ray.

## Usage

### Quickstart: PPO on GSM8K

1. **Prepare the dataset.** Data is stored in Parquet format.

   ```bash
   python3 examples/data_preprocess/gsm8k.py --local_dir ~/data/gsm8k
   ```

   Other preprocessing scripts are provided for MATH, HellaSwag, Full HH-RLHF, Geo3K, and multi-turn data in `examples/data_preprocess/`.

2. **Download the model.** The quickstart uses `Qwen/Qwen2.5-0.5B-Instruct`. Hugging Face model names can be used directly, and `VERL_USE_MODELSCOPE=True` enables ModelScope downloads.

3. **Run PPO training:**

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
    actor_rollout_ref.rollout.gpu_memory_utilization=0.4 \
    critic.optim.lr=1e-5 \
    critic.model.path=Qwen/Qwen2.5-0.5B-Instruct \
    trainer.logger=['console'] \
    trainer.n_gpus_per_node=1 \
    trainer.nnodes=1 \
    trainer.total_epochs=15
   ```

The GSM8K reward function gives a score of 1 for a correct answer, 0.1 for an incorrect answer in the correct format, and 0 for no answer. Checkpoints are saved by default to `checkpoints/${trainer.project_name}/${trainer.experiment_name}`.

### Other algorithms and example scripts

The `examples/` directory contains launch scripts for several configurations:

- `examples/ppo_trainer/`: PPO with FSDP and Megatron, including DeepSeek, Qwen2, Gemma, and reward-model variants.
- `examples/grpo_trainer/`: GRPO scripts, including Qwen2.5-VL.
- `examples/remax_trainer/`, `examples/rloo_trainer/`, `examples/reinforce_plus_plus_trainer/`: ReMax, RLOO, and REINFORCE++ scripts.
- `examples/sft/gsm8k/` and `examples/sft/multiturn/`: supervised fine-tuning scripts.
- `examples/tuning/`: resource-specific configurations for 7B, 14B, and 70B models.
- `examples/checkpoint/`: Megatron checkpoint scripts.

### Supervised fine-tuning

The FSDP SFT trainer is launched with `torchrun`:

```bash
torchrun -m verl.trainer.fsdp_sft_trainer \
    data.train_files=$HOME/data/gsm8k/train.parquet \
    data.val_files=$HOME/data/gsm8k/test.parquet \
    data.prompt_key=question \
    data.response_key=answer \
    data.micro_batch_size_per_gpu=8 \
    model.partial_pretrain=deepseek-ai/deepseek-coder-6.7b-instruct \
    trainer.project_name=gsm8k-sft \
    trainer.total_epochs=4
```

### Converting checkpoints

`scripts/model_merger.py` converts FSDP or Megatron checkpoints to Hugging Face format:

```bash
python scripts/model_merger.py \
    --backend megatron \
    --tie-word-embedding \
    --hf_model_path Qwen/Qwen2.5-0.5B \
    --local_dir checkpoints/<project>/<experiment>/global_step_1/actor
```

### Multi-node training

The documentation describes two approaches:

- **Manual Ray cluster:** Start a head node with `ray start --head --dashboard-host=0.0.0.0`, connect workers with `ray start --address=<address>`, and submit jobs with `ray job submit`, using `verl/trainer/runtime_env.yaml` as the runtime environment.
- **Slurm:** `examples/slurm/ray_on_slurm.slurm` provides a template. The documentation also includes a Slurm script that runs Ray inside Docker or Podman containers.

## Configuration

Configuration uses Hydra-style `key=value` overrides on the command line. The main configuration files are:

- `verl/trainer/config/ppo_trainer.yaml`: FSDP-based PPO
- `verl/trainer/config/ppo_megatron_trainer.yaml`: Megatron-based PPO
- `verl/trainer/config/sft_trainer.yaml`: SFT
- `verl/trainer/config/generation.yaml`: rollout generation
- `verl/trainer/config/evaluation.yaml`: evaluation of generated responses

The documentation (`docs/examples/config.rst`) describes the following main groups of options:

- **`data`**: `train_files`, `val_files`, `prompt_key`, `max_prompt_length`, `max_response_length`, `train_batch_size`, `truncation`, and `custom_cls` for custom datasets. Prompts are left-padded to `max_prompt_length`.
- **`actor_rollout_ref`**: `model.path`, `model.enable_gradient_checkpointing`, `model.use_remove_padding`, and actor settings such as `ppo_mini_batch_size`, `ppo_micro_batch_size_per_gpu`, `use_dynamic_bsz`, `use_kl_loss`, and `kl_loss_type`. Rollout settings include `name` (`vllm`, `sglang`, or `hf`), `gpu_memory_utilization`, `tensor_model_parallel_size`, `enforce_eager`, `free_cache_engine`, `load_format`, and `n` (samples per prompt, greater than 1 for GRPO and RLOO).
- **`critic`** and **`reward_model`**: similar to the actor settings. `reward_model.enable` controls whether a learned reward model is used, and `reward_manager` (default `naive`) selects the reward mechanism.
- **`custom_reward_function`**: `path` and `name` (default `compute_score`) for a user-defined reward function.
- **`algorithm`**: `gamma`, `lam`, `adv_estimator` (`gae`, `grpo`, `reinforce_plus_plus`, `reinforce_plus_plus_baseline`, or `rloo`), `use_kl_in_reward`, `kl_penalty`, and `kl_ctrl`.
- **`trainer`**: `total_epochs`, `project_name`, `experiment_name`, `logger` (console, wandb, swanlab, mlflow, or tensorboard), `nnodes`, `n_gpus_per_node`, `save_freq`, `test_freq`, `val_before_train`, `critic_warmup`, and resume settings (`resume_mode`: `disable`, `auto`, or `resume_path`).

For the `rollout.load_format` option, the documentation notes that users select among `dummy_megatron`, `dummy_dtensor`, and `dummy_hf` for initialization, and the hybrid engine chooses the matching weight loader during synchronization.

When an engine runs out of memory, the documentation suggests reducing `ppo_micro_batch_size_per_gpu` and `critic.ppo_micro_batch_size_per_gpu`, lowering `gpu_memory_utilization`, or enabling offload settings.

## Development

### Code formatting

The project uses yapf with the Google style, configured in `.style.yapf`. The documentation gives this command:

```bash
pip3 install yapf
yapf -ir -vv --style ./.style.yapf verl examples tests
```

`scripts/format.sh` is also included. Linting uses pylint (version 3.3.6 in `requirements.txt`). `pyproject.toml` contains a long list of disabled pylint checks.

### Dependencies

- `requirements.txt` records the full set of development dependencies.
- `requirements_sglang.txt` adds SGLang dependencies.
- `setup.py` and `pyproject.toml` define the installable package. The version is read from `verl/version/version`.
- `docs/requirements-docs.txt` lists documentation dependencies.

### Adding CI tests

The contribution guide asks contributors to:

1. Find the most relevant workflow in `.github/workflows/`, which usually corresponds to a Hydra default config (for example, `ppo_trainer` or `sft_trainer`).
2. Add path patterns to the workflow's `paths` section if they are not included.
3. Keep test scripts minimal.

The workflows in `.github/workflows/` include `e2e_ppo_trainer.yml`, `e2e_ppo_trainer_megatron.yml`, `e2e_dapo.yml`, `e2e_prime.yml`, `e2e_sft.yml`, `vllm.yml`, `sandbox.yml`, `pylint.yml`, `yapf_format.yml`, and `secrets_scan.yml`.

### Building the documentation

```bash
pip install -r requirements-docs.txt
make clean
make html
python -m http.server -d _build/html/
```

## Testing

The `tests/` directory contains several groups of tests:

- **Unit tests:** `tests/utility/`, `tests/verl/utils/`, `tests/distributed/test_tensor_dict.py`, `tests/gpu_utility/`, and `tests/checkpoint/test_fsdp_ckpt.py`.
- **Model tests:** `tests/model/`, including `test_transformer.py`, which the performance guide says can be run with `pytest -s tests/model/test_transformer.py`.
- **Ray tests:** `tests/ray/` covers worker groups, colocated workers, data transfer, and worker liveness checks.
- **Rollout tests:** `tests/rollout/` covers vLLM and SGLang generation.
- **Sanity tests:** `tests/sanity/` includes import tests and a license check.
- **End-to-end tests:** `tests/e2e/` contains shell scripts such as `run_ppo_trainer_megatron.sh`, `run_dapo.sh`, `run_prime.sh`, and `run_r1_distill_qwen_aime24_eval.sh`, along with a small arithmetic-sequence model and dataset.

`pytest`, `yapf`, and `py-spy` are listed under the `test` extra in `setup.py`. The `tests/kill_github_tests.sh` script is also included.

## Recipes

- **DAPO** (`recipe/dapo/`): an implementation of Decoupled Clip and Dynamic sAmpling Policy Optimization. The recipe provides separate clip epsilons, dynamic sampling with group filtering, token-level loss aggregation, and overlong reward shaping. Its README lists a reproduction result of 44% on AIME 2024 for an early version.
- **PRIME** (`recipe/prime/`): PRIME training with a run script for Qwen 0.5B.
- **R1** (`recipe/r1/`): evaluation for DeepSeek-R1-Distill-Qwen models on GPQA Diamond, LiveCodeBench, AIME 2024, and CNMO 2024.
- **Split placement** (`examples/split_placement/`): a naive implementation of placing actor/reference and critic/reward models on different GPU sets, with asynchronous updates.

## License

verl is released under the **Apache License, Version 2.0**. The `LICENSE` file contains the full text, and `setup.py` lists the license as "Apache 2.0." Source files carry the copyright notice "Copyright 2024 Bytedance Ltd. and/or its affiliates." The `Notice.txt` file is also included in the repository.

## Documentation and Community

- Documentation: the `docs/` directory, which covers quickstart, multi-node training, the HybridFlow programming guide, configuration, performance tuning, and FAQs.
- Source code: https://github.com/volcengine/verl
- Community channels listed in `docs/index.rst`: GitHub, Slack, and WeChat.
