# grok-1-9vp9crf1

JAX example code for loading and running the Grok-1 open-weights model, a 314B-parameter Mixture-of-Experts (MoE) language model released by xAI.

---

## Table of Contents

- [Overview](#overview)
- [Model Architecture](#model-architecture)
- [Repository Structure](#repository-structure)
- [Hardware Requirements](#hardware-requirements)
- [Installation](#installation)
- [Downloading the Checkpoint](#downloading-the-checkpoint)
- [Running the Model](#running-the-model)
- [How the Code Works](#how-the-code-works)
- [Configuration](#configuration)
- [Tokenizer](#tokenizer)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [License](#license)

---

## Overview

Grok-1 is a large autoregressive language model trained from scratch by xAI. This repository provides reference code to:

- Load the Grok-1 checkpoint weights.
- Tokenize input text with the bundled SentencePiece tokenizer.
- Run autoregressive text generation (sampling) on accelerator hardware using [JAX](https://github.com/google/jax).

The code is intended as a **reference implementation** for research and experimentation. It prioritizes clarity and correctness over production-level performance, serving, or ease of use.

---

## Model Architecture

Grok-1 is a decoder-only Transformer with a Mixture-of-Experts feed-forward layer. Key hyperparameters, as defined in `run.py`, are approximately:

| Parameter | Value |
|---|---|
| Total parameters | ~314B |
| Transformer layers | 64 |
| Embedding size | 6144 (48 × 128) |
| Query attention heads | 48 |
| Key/Value attention heads | 8 (grouped-query attention) |
| Head (key) size | 128 |
| Experts per MoE layer | 8 |
| Experts selected per token | 2 |
| FFN widening factor | 8 |
| Vocabulary size | 131,072 (128 × 1024) |
| Maximum sequence length | 8,192 tokens |
| Positional encoding | Rotary embeddings (RoPE) |
| Default weight precision | bfloat16 |

**Mixture-of-Experts:** For each token, a learned router selects 2 of the 8 experts in each MoE block. Only the selected experts are computed, so the number of *active* parameters per token is much smaller than the total parameter count.

**Sharding:** Activations and weights can be partitioned across devices using a two-axis JAX device mesh (a `data` axis and a `model` axis), allowing the model to span multiple accelerators.

---

## Repository Structure

```
.
├── run.py              # Entry point: loads the model and runs sample generation
├── model.py            # Model definition: Transformer, attention, MoE layers, RoPE
├── runners.py          # Inference runner: model init, JIT compilation, sampling loop
├── checkpoint.py       # Utilities for loading sharded checkpoint weights
├── tokenizer.model     # SentencePiece tokenizer model file
├── requirements.txt    # Pinned Python dependencies
├── pyproject.toml      # Project metadata and tooling configuration
├── LICENSE.txt         # Apache License 2.0
├── CODE_OF_CONDUCT.md  # Community code of conduct
└── README.md           # This file
```

### File descriptions

- **`run.py`**: The main script. It defines the model configuration, constructs the inference runner, loads the checkpoint, and generates text from a fixed example prompt.
- **`model.py`**: Contains the model implementation, including the embedding layer, multi-head grouped-query attention with rotary embeddings, the MoE feed-forward block with a top-k router, layer normalization, and the output projection (logits).
- **`runners.py`**: Wraps the model for inference. Handles initialization, device mesh setup, compilation of the forward pass with `jax.jit`/`pjit`, and the token-by-token sampling loop with temperature and top-p controls.
- **`checkpoint.py`**: Restores model parameters from the checkpoint directory, mapping stored tensors onto the correct device shards.
- **`tokenizer.model`**: A SentencePiece model used to encode prompts into token IDs and decode generated IDs back into text.
- **`requirements.txt`**: The exact package versions needed to run the code.
- **`pyproject.toml`**: Project metadata and configuration for packaging and development tools.

---

## Hardware Requirements

Grok-1 is a very large model. Running it requires substantial accelerator memory.

- **Recommended:** A multi-GPU node with high-memory accelerators (for example, 8 × 80 GB GPUs). The weights are stored in bfloat16, and the full model is roughly 600 GB on disk.
- **Host memory:** Sufficient CPU RAM to stage checkpoint loading. Plan for several hundred GB.
- **Disk:** Approximately 600+ GB of free space for the checkpoint files.
- **Software:** A Linux environment with a CUDA-compatible GPU driver (or a TPU setup supported by JAX).

The model will not run on consumer hardware or on a single typical GPU.

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url> grok-1-9vp9crf1
cd grok-1-9vp9crf1
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If you need GPU support, install the JAX build that matches your CUDA version by following the [official JAX installation guide](https://github.com/google/jax#installation). For example:

```bash
pip install --upgrade "jax[cuda12]"
```

Verify that JAX detects your accelerators:

```bash
python -c "import jax; print(jax.devices())"
```

---

## Downloading the Checkpoint

The model weights are not included in this repository. They are distributed separately through the Hugging Face Hub under `xai-org/grok-1`.

Install the Hugging Face CLI and download the checkpoint into a `checkpoints/` directory:

```bash
pip install -U "huggingface_hub[cli]"

huggingface-cli download xai-org/grok-1 \
  --repo-type model \
  --include "ckpt-0/*" \
  --local-dir checkpoints \
  --local-dir-use-symlinks False
```

After the download completes, the directory layout should look like this:

```
checkpoints/
└── ckpt-0/
    ├── ...   # sharded checkpoint files
```

The loader in `checkpoint.py` expects this structure. If you place the weights elsewhere, update the checkpoint path in `run.py`.

---

## Running the Model

Once the dependencies and checkpoint are in place, run:

```bash
python run.py
```

The script will:

1. Build the model configuration.
2. Initialize the device mesh across the available accelerators.
3. Load and shard the checkpoint weights.
4. Compile the forward pass.
5. Generate a continuation for the built-in example prompt and print the result.

The default example prompt is:

```
The answer to life the universe and everything is of course
```

Model loading and compilation can take a long time (often many minutes) because the weights are very large. Generation speed depends heavily on your hardware.

### Customizing the prompt and sampling

To change the prompt or sampling behavior, edit the relevant section of `run.py`. Typical parameters include:

| Setting | Description | Typical value |
|---|---|---|
| `prompt` | Input text to continue | Any string |
| `max_len` | Maximum number of tokens to generate | e.g. `100` |
| `temperature` | Controls randomness; lower is more deterministic | e.g. `0.01` (near-greedy) to `1.0` |
| `top_p` | Nucleus sampling threshold | e.g. `1.0` (disabled) or `0.9` |

Example modification:

```python
prompt = "Explain the difference between a process and a thread."
max_len = 256
temperature = 0.7
top_p = 0.9
```

---

## How the Code Works

### 1. Configuration

`run.py` constructs a `LanguageModelConfig` that contains a nested `TransformerConfig`. This holds the architecture hyperparameters described in [Model Architecture](#model-architecture), along with sharding axis names and scaling constants used for embeddings and output logits.

### 2. Inference runner

`runners.py` provides an inference runner that:

- Creates the device mesh.
- Initializes the model state with the correct sharding.
- Compiles the forward pass so that subsequent steps are fast.
- Runs the autoregressive decoding loop: at each step, it feeds the current token sequence through the model, obtains logits for the next token, applies temperature and top-p filtering, samples a token, and appends it to the sequence.

### 3. Model

`model.py` implements the Transformer:

- **Embedding:** Maps token IDs to dense vectors, with a learned scale.
- **Attention:** Grouped-query attention with rotary position embeddings. The 48 query heads share 8 key/value heads, which reduces memory use for the KV cache.
- **MoE block:** A linear router computes scores over 8 experts, selects the top 2 per token, and combines their outputs weighted by the router probabilities.
- **Output:** A final normalization followed by a projection to vocabulary logits, with an output scaling constant.

### 4. Checkpoint loading

`checkpoint.py` reads the sharded tensors from `checkpoints/ckpt-0/` and places each one on the devices specified by the sharding rules. This avoids materializing the full model on a single device.

---

## Configuration

Most configuration lives in `run.py` and is passed into the model and runner. The main groups are:

- **Model config** (`LanguageModelConfig`): vocabulary size, sequence length, padding and EOS token IDs, embedding and output scaling factors.
- **Transformer config** (`TransformerConfig`): embedding size, widening factor, number of layers, attention heads, key size, expert count, number of selected experts, attention output multiplier, and sharding axis names.
- **Device mesh**: The `data` and `model` axis names determine how work is split across accelerators. The mesh shape should match your hardware topology.

Changing architectural values will make the checkpoint incompatible. Only modify them if you know the checkpoint was produced with the new values.

---

## Tokenizer

The tokenizer is a SentencePiece model stored in `tokenizer.model`, with a vocabulary of 131,072 tokens. It is used to:

- Encode the input prompt into token IDs.
- Decode generated token IDs back into readable text.

Special tokens include a padding token (ID `0`) and an end-of-sequence token (ID `2`). Generation stops when the EOS token is produced or `max_len` is reached.

To inspect the tokenizer independently:

```python
import sentencepiece as spm

sp = spm.SentencePieceProcessor(model_file="tokenizer.model")
ids = sp.encode("Hello, world!")
print(ids)
print(sp.decode(ids))
```

---

## Troubleshooting

**Out of memory (OOM) during loading or inference**
- Confirm that the total accelerator memory across all devices is sufficient for the bfloat16 weights.
- Reduce `max_len` or the sequence length.
- Make sure no other processes are using GPU memory (`nvidia-smi`).

**`jax.devices()` shows only CPU**
- Reinstall JAX with the CUDA extra that matches your driver and CUDA toolkit version.
- Check that `CUDA_VISIBLE_DEVICES` is not hiding your GPUs.

**Checkpoint not found**
- Verify the directory is `checkpoints/ckpt-0/` relative to where you run `python run.py`, or update the path in `run.py`.
- Re-run the `huggingface-cli download` command if files are missing. Partial downloads cause loading errors.

**Shape or sharding mismatch errors**
- The device mesh must be compatible with the sharding configuration. Check that the number of devices matches the mesh shape defined in `run.py`.
- Make sure the architecture config matches the released checkpoint.

**Very slow first run**
- JIT compilation and checkpoint loading are expensive. Subsequent runs in the same environment are typically faster due to cached compilation.

**Dependency conflicts**
- Use a fresh virtual environment and install from `requirements.txt` exactly as provided.

---

## Limitations

- **Not a production server.** This repository contains only a sampling script. It provides no HTTP API, batching, or streaming interface.
- **Reference-quality code.** Performance is not optimized for throughput or latency.
- **No fine-tuning code.** The repository supports inference only.
- **Base model behavior.** Grok-1 is a pretrained base model and is not instruction-tuned or aligned for chat in the way a deployed assistant would be. Expect outputs that continue text rather than follow instructions reliably.
- **Factual reliability.** Like all large language models, Grok-1 can produce incorrect or fabricated information. Verify important outputs independently.
- **Hardware barrier.** The model's size makes it impractical to run on most hardware.

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository and create a feature branch.
2. Make focused changes with clear commit messages.
3. Test your changes on hardware capable of running the model, or clearly note what you were able to test.
4. Open a pull request describing the motivation and the change.

Please follow the project's [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions.

---

## Code of Conduct

Participation in this project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing or engaging in discussions.

---

## License

The source code in this repository is licensed under the **Apache License, Version 2.0**. See [LICENSE.txt](LICENSE.txt) for the full text.

The Grok-1 model weights are distributed separately and are subject to their own license terms as published alongside the weights on the Hugging Face Hub. Review those terms before using, redistributing, or deploying the weights.

---

*Note: This README was written from the file listing and the publicly known structure of the Grok-1 open release. Specific values such as hyperparameters, file paths, and the prompt in `run.py` should be verified against the actual source files in your copy of the repository.*
