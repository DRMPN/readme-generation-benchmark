# verl: Volcano Engine Reinforcement Learning for LLMs

verl is a reinforcement learning (RL) training framework for post-training large language models (LLMs). It is described in the project docs as an open-source implementation of the [HybridFlow](https://arxiv.org/pdf/2409.19256) paper.

The package is currently at version `0.2.0.dev` (see `verl/version/version`) and is licensed under the Apache License 2.0.

## Features

Based on the project documentation and source code, verl provides:

- **RL algorithms** selectable with `algorithm.adv_estimator`: `gae`, `grpo`, `reinforce_plus_plus`, `reinforce_plus_plus_baseline`, `remax`, and `rloo`.
- **Training backends**: FSDP (recommended for research and prototyping) and Megatron-LM (for scalability; the docs reference Megatron-LM v0.11).
- **Rollout (inference) backends**: vLLM (`actor_rollout_ref.rollout.name=vllm`, the default), SGLang (`actor_rollout_ref.rollout.name=sglang`), and a HuggingFace `hf` rollout. The docs say vLLM 0.6.3 and 0.8.2 have been tested, and recommend avoiding vLLM 0.7.x.
- **Hydra-based configuration** through the YAML files in `verl/trainer/config/`, overridable from the command line.
- **Reward functions**, including rule-based rewards for GSM8K, MATH, and Geo3k in `verl/utils/reward_score/`, and a pluggable reward manager (`naive`, `batch`, `prime`, `dapo` in `verl/workers/reward_manager/`).
- **Experiment tracking** through the console and Weights & Biases (`trainer.logger=['console','wandb']`).
- **Ray-based distributed execution** for single-node and multi-node runs.
- **Dataset preprocessing scripts** for GSM8K, MATH, Geo3k, HellaSwag, multi-turn, and HH-RLHF under `examples/data_preprocess/`.

## Repository Layout

| Path | Contents |
| --- | --- |
| `verl/` | Core Python package: trainer, workers, rollout, sharding managers, reward functions, and utilities |
| `verl/trainer/` | Entry points (`main_ppo.py`, `main_generation.py`, `main_eval.py`, `fsdp_sft_trainer.py`) and Hydra configs |
| `verl/workers/` | Actor, critic, rollout, reward manager, and sharding manager implementations |
| `verl/third_party/` | Version-specific patches for vLLM and SGLang integration |
| `examples/` | Example launch scripts for PPO, GRPO, RLOO, and SFT, plus data preprocessing scripts |
| `docs/` | Sphinx documentation source (installation, quickstart, workers, configuration, FAQ) |
| `docker/` | Dockerfiles for NGC-based, Megatron, SGLang, vLLM, and ROCm images |
| `scripts/` | Utilities including `model_merger.py`, `converter_hf_to_mcore.py`, and `diagnose.py` |
| `tests/` | Test suites for Ray, utilities, models, datasets, generation, and sandbox code |
| `run_master.sh`, `run_worker.sh` | Example scripts for starting a Ray head node and worker nodes, and submitting a GRPO job |

## Requirements

From `docs/start/install.rst`:

- **Python**: 3.9 or newer. The install guide uses Python 3.10 in its conda example.
- **CUDA**: 12.1 or newer.

The core dependencies are listed in `setup.py` and `requirements.txt`. These include `ray[default]>=2.10`, `transformers`, `hydra-core`, `tensordict<=0.6.2`, `accelerate`, `peft`, `datasets`, and `wandb`. Backend-specific packages are provided as optional extras (see below).

## Installation

### Option 1: Docker

The install guide lists these prebuilt images:

- For vLLM with FSDP or Megatron: `whatcanyousee/verl:ngc-th2.6.0-cu124-vllm0.8.2-mcore0.11.0-te2.0`
- For SGLang with FSDP: `ocss884/verl-sglang:ngc-th2.5.1-cu126-sglang0.4.4.post4`

Start a container and install verl inside it:

```bash
docker create --runtime=nvidia --gpus all --net=host --shm-size="10g" --cap-add=SYS_ADMIN -v .:/workspace/verl --name verl <image:tag>
docker start verl
docker exec -it verl bash
```

### Option 2: From source in a custom environment

```bash
conda create -n verl python==3.10
conda activate verl

pip3 install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu126
pip3 install flash-attn --no-build-isolation
git clone https://github.com/volcengine/verl.git
cd verl
pip3 install -e .
```

### Optional extras

`setup.py` defines these extras:

| Extra | Purpose |
| --- | --- |
| `vllm` | `vllm<=0.8.2`, `tensordict<=0.6.2` |
| `sglang` | `sglang[all]==0.4.4.post4`, `torch-memory-saver>=0.0.5`, `tensordict<=0.6.2` |
| `gpu` | `liger-kernel`, `flash-attn` |
| `math` | `math-verify` |
| `geo` | `mathruler` |
| `prime` | `pyext` |
| `test` | `pytest`, `yapf`, `py-spy` |

Install an extra with, for example, `pip3 install -e ".[vllm]"`.

Megatron-LM is optional. The install guide describes installing Apex, TransformerEngine, and `megatron-core==0.11.0` separately.

For AMD MI300 GPUs, use `docker/Dockerfile.rocm`. The install guide says this path supports the FSDP training engine with vLLM or SGLang rollout.

## Quickstart: PPO on GSM8K

The quickstart trains `Qwen/Qwen2.5-0.5B-Instruct` on GSM8K using a rule-based reward. The guide recommends at least 24 GB of GPU memory.

1. Preprocess the dataset into Parquet files:

   ```bash
   python3 examples/data_preprocess/gsm8k.py --local_dir ~/data/gsm8k
   ```

2. Run PPO training:

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

Checkpoints are saved to `checkpoints/${trainer.project_name}/${trainer.experiment_name}` by default. The key validation metric is `val/test_score/openai/gsm8k`, logged every `trainer.test_freq` steps.

To log to Weights & Biases, add:

```bash
trainer.logger=['console','wandb'] \
trainer.project_name=$YOUR_PROJECT_NAME \
trainer.experiment_name=$YOUR_RUN_NAME
```

If GPU memory is limited, the quickstart suggests setting `actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=1` and `critic.ppo_micro_batch_size_per_gpu=1`.

More example scripts are in `examples/ppo_trainer/`, `examples/grpo_trainer/`, `examples/rloo_trainer/`, and `examples/sft/`.

## Using SGLang for Rollout

After installing SGLang, add `actor_rollout_ref.rollout.name=sglang` to your launch command to use it instead of vLLM. See `docs/workers/sglang_worker.rst` for the supported SGLang version and setup steps. The docs note that SGLang is under active development.

## Multi-Node Training

`docs/start/multinode.rst` covers multi-node setup. The repository root also includes two example scripts:

- `run_master.sh` starts a Ray head node on port 6379 and submits a GRPO job (`python3 -m verl.trainer.main_ppo` with `algorithm.adv_estimator=grpo`) using `verl/trainer/runtime_env.yaml`. It assumes a local model at `/from_s3/models/Qwen2.5-Math-1.5B` and GSM8K data under `~/data/gsm8k/`. Edit these paths before use.
- `run_worker.sh` resolves `MASTER_ADDR` and joins the Ray cluster at `MASTER_IP:6379`.

## Configuration

Configuration is managed with Hydra. The main configs are:

- `verl/trainer/config/ppo_trainer.yaml`: FSDP-based PPO/GRPO training
- `verl/trainer/config/ppo_megatron_trainer.yaml`: Megatron-based training
- `verl/trainer/config/sft_trainer.yaml`: supervised fine-tuning
- `verl/trainer/config/generation.yaml` and `evaluation.yaml`: generation and evaluation

Any config value can be overridden on the command line with `key=value` syntax, as shown in the examples above. See `docs/examples/config.rst` for an explanation of the options.

## Documentation

The documentation source is in `docs/` (Sphinx, configured by `docs/conf.py`). To build it locally:

```bash
pip install -r docs/requirements-docs.txt
cd docs
make clean
make html
python -m http.server -d _build/html/
```

Then open http://localhost:8000. The docs cover the programming model (`docs/hybrid_flow.rst`), worker implementations, data preparation, reward functions, performance tuning, and FAQ.

## Testing and Code Style

- Tests are under `tests/`. The `test` extra installs `pytest`.
- Code is formatted with yapf using the Google style in `.style.yapf`:

  ```bash
  pip3 install yapf
  yapf -ir -vv --style ./.style.yapf verl examples tests
  ```

- `scripts/format.sh` is also included in the repository.

## Contributing

Contributions are welcome. Community channels listed in the docs are the [GitHub repository](https://github.com/volcengine/verl), a Slack workspace, and a WeChat group. The contribution guide in `docs/index.rst` asks contributors to format code with yapf and, where possible, to add a CI test for new features.

## Citation

If you use verl, please cite the HybridFlow paper, arXiv:2409.19256: https://arxiv.org/pdf/2409.19256

## License

verl is released under the [Apache License 2.0](LICENSE). Copyright notices are in `Notice.txt`.
