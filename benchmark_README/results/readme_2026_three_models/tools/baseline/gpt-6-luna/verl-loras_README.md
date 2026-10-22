# verl

**verl** (Volcano Engine Reinforcement Learning for LLM) is an open-source framework for post-training large language models. It implements the HybridFlow approach: a single controller coordinates distributed model workers, separating reinforcement-learning control flow from the underlying training and inference computations.

The framework is designed to support flexible RL workflows, reuse of existing LLM infrastructure, and placement of models across GPU resources. It integrates with Hugging Face models and provides training backends based on PyTorch FSDP and Megatron-LM, plus rollout backends including vLLM, SGLang, and Hugging Face.

For detailed guides, see the [documentation index](docs/index.rst), including installation, configuration, data preparation, distributed training, and performance tuning.

## Overview

A typical RL training job loads preprocessed prompts, generates responses, calculates rewards, and updates models. In verl, the controller runs the algorithm’s training loop and dispatches work to Ray-managed worker groups. Workers perform distributed model operations such as generation, log-probability calculation, and actor or critic updates.

`DataProto` is the data-exchange interface between the controller and workers. It combines a tensor batch with additional metadata. Worker methods use dispatch rules to split data, run computations remotely, and collect results.

The repository includes PPO training and examples for algorithms and recipes such as GRPO, RLOO, ReMax, Reinforce++, DAPO, and PRIME. It also includes an FSDP SFT trainer, evaluation and generation entry points, dataset preprocessing scripts, checkpoint utilities, and model integrations.

## Requirements

The installation guide documents **Python 3.9 or later** and **CUDA 12.1 or later** for its standard GPU setup. The package metadata declares Python `>=3.8`; compatible hardware, drivers, and library versions depend on the backend and environment.

The quickstart describes a GPU with at least **24 GB of HBM** as a prerequisite for its GSM8K example. Actual requirements vary with model size, sequence lengths, batch sizes, and parallelism.

For training, FSDP is recommended for research and prototyping; Megatron-LM is an option for larger-scale training. For inference, the documentation covers vLLM, SGLang, and Hugging Face. Consult [installation guidance](docs/start/install.rst) and the backend-specific documentation before choosing versions: support details can vary across versions.

## Installation

A common source installation in a Python environment is:

```bash
conda create -n verl python=3.10
conda activate verl

# Install PyTorch appropriate for your system. This is the CUDA 12.6
# example used in the installation guide.
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu126
pip install flash-attn --no-build-isolation

git clone https://github.com/volcengine/verl.git
cd verl
pip install -e .
```

The base install uses dependencies declared by the package. Backend-specific extras are available in `setup.py`, including `vllm`, `sglang`, `gpu`, `math`, `geo`, `prime`, and `test`. For example:

```bash
pip install -e ".[vllm]"
```

For SGLang, use `pip install -e ".[sglang]"`. The repository also provides `requirements.txt` and `requirements_sglang.txt` for development environments. These dependencies include accelerator-related packages; install them in an environment compatible with your PyTorch and hardware setup.

Prebuilt Docker images and Dockerfiles are also documented. ROCm users should follow the separate [AMD installation guide](docs/amd_tutorial/amd_build_dockerfile_page.rst) rather than the standard CUDA quickstart.

## Quickstart: PPO on GSM8K

The following commands follow the documented single-GPU example. They expect the dataset and model to be accessible and a working GPU environment.

First preprocess GSM8K into Parquet files:

```bash
python3 examples/data_preprocess/gsm8k.py --local_dir ~/data/gsm8k
```

The example uses a Hugging Face model identifier; loading it once can verify model access:

```bash
python3 -c "import transformers; transformers.pipeline('text-generation', model='Qwen/Qwen2.5-0.5B-Instruct')"
```

Start PPO training:

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
  trainer.logger='["console"]' \
  trainer.val_before_train=False \
  trainer.default_hdfs_dir=null \
  trainer.n_gpus_per_node=1 \
  trainer.nnodes=1 \
  trainer.save_freq=10 \
  trainer.test_freq=10 \
  trainer.total_epochs=15
```

Training configuration is supplied through Hydra-style `key=value` overrides. The example uses the default PPO trainer configuration; the repository also has separate configuration files for SFT, evaluation, generation, and Megatron PPO under `verl/trainer/config/`. The full set of options is described in [Configuration](docs/examples/config.rst).

By default, local checkpoints are written under `checkpoints/${trainer.project_name}/${trainer.experiment_name}`. To use Weights & Biases logging, configure `trainer.logger` to include `wandb`, and set the project and experiment names. See the [quickstart](docs/start/quickstart.rst) for more details and memory-tuning suggestions.

## Data and rewards

Training data is prepared as Parquet files. Preprocessing examples are in `examples/data_preprocess/`; documented examples include GSM8K, MATH, Hellaswag, and Full HH RLHF. For PPO, the default dataset expects a prompt field, while reward functions may also use fields such as `data_source`, `reward_model`, and `extra_info`. See [data preparation](docs/preparation/prepare_data.rst) and the dataset implementation notes in `verl/utils/dataset/README.md`.

Reward scores can come from built-in functions, a custom reward function, or a reward model. Custom functions are configured with `custom_reward_function.path` and `custom_reward_function.name`; the documented function arguments are `data_source`, `solution_str`, `ground_truth`, and `extra_info`.

## Distributed usage

For multi-node jobs, start a Ray cluster and submit work using the Ray job interface. The trainer configuration includes `trainer.nnodes` and `trainer.n_gpus_per_node`; set these to match the resources allocated to the job. See [multinode training](docs/start/multinode.rst) for cluster setup and submission examples.

Example scripts under `examples/` cover PPO, GRPO, SFT, generation, and other workflows. They provide concrete model and hardware-specific settings; adjust model paths, dataset paths, batch sizes, and parallelism for your environment.

## Development

Install the test extra with `pip install -e ".[test]"` to add the test dependencies declared by the project. The repository uses YAPF with `.style.yapf`. Format Python code from the repository root with:

```bash
pip install yapf
yapf -ir -vv --style ./.style.yapf verl examples tests
```

To build the documentation, install its requirements and use the Sphinx Makefile:

```bash
pip install -r docs/requirements-docs.txt
cd docs
make clean
make html
```

The generated site is in `docs/_build/html/`. To serve it locally:

```bash
python -m http.server -d docs/_build/html/
```

When contributing features, the project documentation recommends adding relevant CI tests where possible and keeping test workloads small. See the workflows in `.github/workflows/` for examples of CI coverage.

## Testing

Tests are organized under `tests/`, with coverage for data utilities, models, distributed and Ray behavior, GPU utilities, rollout integrations, checkpoints, and end-to-end workflows. Run the suite, or a targeted test, with pytest:

```bash
pytest
pytest -s tests/model/test_transformer.py
```

End-to-end shell scripts are available in `tests/e2e/`; for example, `tests/e2e/run_test.sh` and the scripts in `tests/e2e/ppo_trainer/` and `tests/e2e/sft/`. These tests may require GPUs, model or dataset access, and a suitable distributed environment. Check each script before running it.

## License

This project is distributed under the **Apache License, Version 2.0**. See [LICENSE](LICENSE) and [Notice.txt](Notice.txt). When redistributing the work or derivatives, follow the license terms, including retaining applicable notices and providing a copy of the license.
