# Grok-1

Source code for **Grok-1** — a 314-billion-parameter Mixture-of-Experts language model trained by **xAI** — together with utilities for downloading the released weights and running inference.

> **Announcement:** We're releasing the base model weights and network architecture of Grok-1. The weights are hosted on [Hugging Face](https://huggingface.co/xai-org/grok-1), and the accompanying announcement is available at [x.ai/blog/grok-os](https://x.ai/blog/grok-os/).

---

## Table of Contents

1. [Overview](#overview)
2. [Model specification](#model-specification)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Downloading the weights](#downloading-the-weights)
6. [Running the model](#running-the-model)
7. [Using the runner in your own code](#using-the-runner-in-your-own-code)
8. [Repository layout](#repository-layout)
9. [Implementation notes](#implementation-notes)
10. [Troubleshooting & tips](#troubleshooting--tips)
11. [License](#license)
12. [Code of Conduct](#code-of-conduct)

---

## Overview

Grok-1 is a decoder-only transformer trained by xAI on a large amount of textual data from the web, as well as data from English Wikipedia (training data cutoff: Q4 2023).

This repository contains the **base** model. It has **not** been fine-tuned on any downstream task or instruction-tuned for dialogue, so instead of answering questions it will typically *continue* the text it is given. The model is intended primarily for research purposes and as a starting point for further fine-tuning and experimentation.

Key features of this release:

- **314B-parameter** Mixture-of-Experts transformer (8 experts, 2 activated per token → ≈86B active parameters per forward pass)
- **8,192-token** context window
- A self-contained **JAX** implementation of the network that can run inference directly from the released checkpoint
- Support for **8-bit weight quantization** to reduce the memory footprint
- Includes the **SentencePiece** tokenizer used to train the model

## Model specification

| item | value |
| --- | --- |
| Parameters | 314B (≈86B active) |
| Architecture | Mixture of 8 experts (2 activated per token) |
| Layers | 48 |
| Attention heads | 48 |
| Context length | 8,192 tokens |
| Embedding size | 6,144 |
| Tokenization | SentencePiece tokenizer |
| Embeddings | 131,072 (learned positional embeddings) |
| Precision | bfloat16 (8-bit quantized weights supported) |

## Requirements

- A machine with NVIDIA GPUs — the model requires **hundreds of GB of aggregate GPU memory** (the default configuration shards the model across 8 devices, e.g. 8 × 80 GB GPUs).
- Python 3 (see `pyproject.toml` for the supported version range).
- Core Python dependencies: JAX (CUDA build), `dm-haiku`, `sentencepiece`, etc. See [`requirements.txt`](requirements.txt) for the full pinned list.

## Installation

Clone the repository and install the dependencies (a virtual environment or conda environment is recommended):

```shell
git clone <this-repository> grok-1
cd grok-1

pip install -r requirements.txt
```

## Downloading the weights

The trained weights are hosted on the Hugging Face Hub: **[xai-org/grok-1](https://huggingface.co/xai-org/grok-1)**.

**Option A — pre-download with the Hugging Face CLI:**

```shell
pip install "huggingface_hub[hf_transfer]"

# enables the fast Rust-based transfer engine
export HF_HUB_ENABLE_HF_TRANSFER=1

huggingface-cli download xai-org/grok-1 --local-dir checkpoints
```

**Option B — let the code fetch it:** the model configuration in `run.py` references the `xai-org/grok-1` repository, and the checkpoint is pulled automatically when you first run the model.

> ⚠️ **Note:** The checkpoint is large — expect **several hundred gigabytes** of download and disk usage. Make sure you have sufficient disk space and bandwidth before starting.

## Running the model

Once the dependencies are installed and the weights are available, you can test the generative capabilities of the base model:

```shell
python run.py
```

`run.py` will:

1. Build the model configuration (transformer size, MoE settings, tokenizer path, dtypes, sharding).
2. Load the checkpoint and shard the parameters across the available devices.
3. Initialize the model state and run a sample generation.

Example output:

```
Hello, my name is Elion and I'm a 19 year old...
```

Since Grok-1 is a *base* model, the output is a text continuation of the prompt rather than a conversational answer.

## Using the runner in your own code

`run.py` is a thin wrapper around the `TransformerRunner` class defined in [`runners.py`](runners.py). You can reuse it in your own scripts:

```python
# Illustrative example — see run.py and runners.py for the exact configuration options.
from runners import TransformerRunner

runner = TransformerRunner(...)   # model config, checkpoint path, number of shards, etc.
runner.load_checkpoint()          # read the released weights
runner.init_states()              # initialize the model state

output = runner.generate("Hello, my name is Elion and")
print(output)
```

The runner handles:

- Building and sharding the parameter tree across devices
- Reading and mapping the checkpoint onto the model (via [`checkpoint.py`](checkpoint.py))
- Tokenization/detokenization with the included SentencePiece model
- The decoding loop (prompt encoding, sampling, and streaming the result)

## Repository layout

| Path | Description |
| --- | --- |
| `run.py` | Command-line entry point: builds the model config, loads the checkpoint, and runs a sample generation. |
| `model.py` | The complete Grok-1 network implemented in JAX/Haiku: transformer blocks, attention, the Mixture-of-Experts feed-forward layer (8 experts, top-2 routing), and 8-bit quantized-weight support. |
| `runners.py` | Inference runner: device sharding, state initialization, and the text-generation loop built around the model. |
| `checkpoint.py` | Checkpoint utilities: reading the released checkpoint files and mapping them onto the model's parameters. |
| `tokenizer.model` | The SentencePiece tokenizer model (vocabulary of 131,072 tokens) used to encode/decode text. |
| `requirements.txt` | Python dependencies (pinned versions). |
| `pyproject.toml` | Project metadata, packaging and tooling configuration. |
| `LICENSE.txt` | License information for the code (Apache 2.0). |
| `CODE_OF_CONDUCT.md` | Contributor Code of Conduct. |
| `README.md` | This file. |

## Implementation notes

- **Framework:** the network is implemented directly on top of [JAX](https://github.com/google/jax) and [Haiku](https://github.com/deepmind/dm-haiku), so no heavyweight training framework is required for inference.
- **Mixture-of-Experts:** each feed-forward layer is split into 8 experts, of which 2 are activated per token, giving sparse activation (≈86B active of 314B total parameters).
- **Quantization:** `model.py` includes 8-bit weight quantization utilities, which can substantially reduce the GPU memory needed to serve the model.
- **Sharding:** parameters are sharded across devices using JAX's sharding primitives; make sure `jax.devices()` reports the GPUs you expect (set `CUDA_VISIBLE_DEVICES` if needed).

## Troubleshooting & tips

- **Out of memory:** you need more device memory. Add more GPUs (the default configuration assumes the model is split across multiple devices) or use the 8-bit quantized weights.
- **Slow checkpoint download:** set `HF_HUB_ENABLE_HF_TRANSFER=1` and install `huggingface_hub[hf_transfer]`.
- **JAX doesn't see your GPUs:** verify with `python -c "import jax; print(jax.devices())"` and ensure the CUDA-enabled JAX build matching your driver is installed (see `requirements.txt`).
- **Long startup time:** loading and sharding a multi-hundred-GB checkpoint takes a while — this is expected on first load.

## License

- The **code** in this repository is licensed under **Apache 2.0** — see [`LICENSE.txt`](LICENSE.txt).
- The **model weights** are released under the terms of the [Grok-1 Model License](https://x.ai/wp-content/uploads/2024/03/Grok-1-Model-License.pdf). Note that commercial entities with more than 100 million monthly active users must seek a separate license from xAI.

## Code of Conduct

Please read [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) before contributing to or interacting with this project.

## Resources

- 📝 Announcement & technical details: [x.ai/blog/grok-os](https://x.ai/blog/grok-os/)
- 🤗 Model weights: [huggingface.co/xai-org/grok-1](https://huggingface.co/xai-org/grok-1)
- 🌐 xAI: [x.ai](https://x.ai)

## Disclaimer

Grok-1 is a base language model. It can produce factually incorrect, outdated, or harmful content, and it has not been aligned for dialogue or production use. Evaluate and filter outputs appropriately before deploying any application built on top of this model, and use it in accordance with the license terms.
