# verl

`verl` is an open-source framework for post-training large language models with reinforcement learning. It implements the **HybridFlow** approach, separating the RL control flow from model computation so training algorithms can use worker backends such as PyTorch FSDP and Megatron-LM, with rollout backends including vLLM and SGLang.

This repository contains the `verl` Python package (version `0.2.0.dev`), trainer and worker implementations, example configurations and scripts, recipes, tests, and documentation. The package metadata describes the project as “Volcano Engine Reinforcement Learning for LLM”; the source repository URL is [volcengine/verl](https://github.com/volcengine/verl).

## What’s included

- **RL post-training:** PPO training, with example configurations for algorithms including GRPO, RLOO, REINFORCE++, and ReMax.
- **Algorithm recipes:** DAPO and PRIME implementations under [`recipe/`](recipe/).
- **Supervised fine-tuning:** an FSDP SFT trainer, including a PEFT/LoRA example.
- **Generation and evaluation:** trainer entry points for generating responses and evaluating models.
- **Distributed execution:** Ray-based worker groups, FSDP and Megatron workers, and sharding/rollout integrations.
- **Backend-specific integrations:** versioned vLLM code under `verl/third_party/vllm/` and SGLang integration code under `verl/third_party/sglang/`.

See [`docs/hybrid_flow.rst`](docs/hybrid_flow.rst) for the control-flow and worker design, and [`verl/utils/dataset/README.md`](verl/utils/dataset/README.md) for the RL dataset format.

## Installation

Use an environment with a PyTorch build compatible with your accelerator and the backend you plan to run. From the repository root, install the package in editable mode:

```bash
pip install -e .
```

The base dependencies and optional dependency groups are declared in [`setup.py`](setup.py). Backend-specific extras are available as `vllm` and `sglang`; for example:

```bash
pip install -e '.[vllm]'
# or
pip install -e '.[sglang]'
```

These extras specify backend package versions in `setup.py`; verify they fit the versions and hardware in your environment. [`requirements.txt`](requirements.txt) lists the development dependencies, and [`requirements_sglang.txt`](requirements_sglang.txt) lists the SGLang environment dependencies. Additional environment-specific setup is described in the backend Dockerfiles under [`docker/`](docker/) and the vLLM notes in [`docs/README_vllm0.8.md`](docs/README_vllm0.8.md).

## Quick starts

The example scripts are configuration examples, not hardware-independent commands. They expect the referenced data and model to be accessible and require an environment with the specified distributed backend and sufficient GPUs.

### GRPO training

[`examples/grpo_trainer/run_qwen2-7b.sh`](examples/grpo_trainer/run_qwen2-7b.sh) launches the PPO trainer configured with the GRPO advantage estimator, Qwen2-7B-Instruct, vLLM rollout, and an example GSM8K dataset:

```bash
bash examples/grpo_trainer/run_qwen2-7b.sh
```

By default, the script reads `$HOME/data/gsm8k/train.parquet` and `$HOME/data/gsm8k/test.parquet`, configures one node with eight GPUs, and uses the model identifier `Qwen/Qwen2-7B-Instruct`. Adjust these values and the other Hydra overrides in the script for your data and setup. Training can also be launched directly with `python -m verl.trainer.main_ppo` and Hydra configuration overrides.

### SFT with LoRA

[`examples/sft/gsm8k/run_qwen_05_peft.sh`](examples/sft/gsm8k/run_qwen_05_peft.sh) runs the FSDP SFT trainer using PEFT LoRA:

```bash
bash examples/sft/gsm8k/run_qwen_05_peft.sh 2 ./checkpoints/gsm8k-lora
```

The arguments are the number of local processes (GPUs) and the save path. This example uses the GSM8K Parquet files under `$HOME/data/gsm8k/`, starts from `Qwen/Qwen2.5-0.5B-Instruct`, and sets LoRA rank 32, alpha 16, and target modules `all-linear`. The script notes it was tested with 2 and 4 GPUs. Other SFT examples are in [`examples/sft/`](examples/sft/).

## Repository layout

| Path | Contents |
| --- | --- |
| `verl/trainer/` | PPO/RL, SFT, generation, and evaluation entry points and trainer code |
| `verl/workers/` | Actor, critic, reward-model, rollout, and sharding workers |
| `verl/single_controller/` | Worker-group and controller abstractions |
| `verl/utils/dataset/` | RL, SFT, reward-model, and multi-turn dataset utilities |
| `verl/third_party/` | Backend integration code, including versioned vLLM implementations |
| `examples/` | Training, generation, checkpoint, and tuning examples |
| `recipe/` | Algorithm recipes such as DAPO, PRIME, and R1 |
| `tests/` | Unit, integration, and end-to-end tests |
| `docs/` | Sphinx documentation sources and build instructions |

## Documentation and tests

The documentation source index is [`docs/index.rst`](docs/index.rst). The docs README describes building the HTML documentation:

```bash
cd docs
pip install -r requirements-docs.txt
make clean
make html
```

Tests are organized under [`tests/`](tests/), including model, Ray, rollout, distributed, and end-to-end tests. Many test and training paths require GPU or distributed runtime dependencies; consult the specific test or script before running it.

## License

This project is distributed under the [Apache License, Version 2.0](LICENSE). Some third-party components and assets may have their own terms; see [`Notice.txt`](Notice.txt).

## Citation

The documentation identifies `verl` as an open-source implementation of the [HybridFlow paper](https://arxiv.org/abs/2409.19256).
