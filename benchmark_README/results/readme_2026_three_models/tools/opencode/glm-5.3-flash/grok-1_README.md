# Grok-1

This repository contains a JAX-based implementation for running inference with the Grok-1 language model. The implementation is built on top of [JAX](https://github.com/google/jax) and DeepMind's [Haiku](https://github.com/google-deepmind/dm-haiku) library, and supports loading checkpoints, sharding model weights across devices, and performing batched text generation.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Model Configuration](#model-configuration)
  - [Checkpoints](#checkpoints)
- [Repository Structure](#repository-structure)
- [Implementation Details](#implementation-details)
- [Code of Conduct](#code-of-conduct)
- [License](#license)

## Requirements

The dependencies are specified in `requirements.txt`:

- `dm_haiku==0.0.12`
- `jax[cuda12-pip]==0.4.25`
- `numpy==1.26.4`
- `sentencepiece==0.2.0`

## Installation

1. Clone the repository.
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The JAX dependency is pinned with CUDA 12 support via the extra `cuda12-pip` and installs from [JAX's CUDA release channel](https://storage.googleapis.com/jax-releases/jax_cuda_releases.html).

## Usage

The main entry point is `run.py`, which sets up the model configuration, initializes the inference runner, and performs a sample generation:

```python
inp = "The answer to life the universe and everything is of course"
print(f"Output for prompt: {inp}", sample_from_model(gen, inp, max_len=100, temperature=0.01))
```

To run the script:

```bash
python run.py
```

### Model Configuration

The model architecture is defined in `run.py` via `LanguageModelConfig` and `TransformerConfig`:

- **Vocabulary size**: 128 * 1024 (131,072)
- **Sequence length**: 8192
- **Embedding size**: 48 * 128 (6144)
- **Widening factor**: 8
- **Key size**: 128
- **Query heads**: 48
- **Key/Value heads**: 8
- **Number of layers**: 64
- **Mixture-of-Experts (MoE)**: 8 experts with 2 selected experts per token
- **Sharding**: Activations are sharded across the `data` and `model` axes

The runner is configured with `local_mesh_config=(1, 8)` and `between_hosts_config=(1, 1)`, corresponding to a single-host mesh with 8 devices (e.g., 8 GPUs). The `bs_per_device` is set to `0.125`.

### Checkpoints

Place Grok-1 checkpoints in the `./checkpoints/` directory. The checkpoint loader in `checkpoint.py` expects the checkpoint files to be located at:

```
./checkpoints/ckpt-0/
```

The checkpoint is loaded using a pickle-based tensor loading system that reads individual tensor files (`tensor{i:05d}_{idx:03d}`) from the checkpoint directory. Loading is parallelized using a thread pool, and temporary files are copied to shared memory (`/dev/shm`) to accelerate reading.

## Repository Structure

- `run.py`: Example script that sets up the model configuration and runs a sample inference.
- `model.py`: Defines the model architecture, including `LanguageModelConfig`, `TransformerConfig`, and the `QuantizedWeight8bit` type for 8-bit quantized weights.
- `runners.py`: Implements the `InferenceRunner` and `ModelRunner` classes, handling device mesh creation, model compilation, checkpoint loading, and batched generation.
- `checkpoint.py`: Utilities for loading and saving model checkpoints.
- `tokenizer.model`: The SentencePiece tokenizer model used for encoding and decoding text.
- `checkpoints/README.md`: Instructions for placing model checkpoints.

## Implementation Details

### Inference Runner

The `InferenceRunner` class handles the end-to-end inference process:

1. **Initialization**: It sets up the JAX device mesh, initializes the model, and loads parameters from the checkpoint.
2. **Compilation**: It precompiles the model for different padding bucket sizes using the `pad_sizes` configuration.
3. **Generation**: It manages a continuous batch of requests, filling free slots with new prompts, running forward passes, and yielding completed generations.

### Sampling

The `sample_token` function implements the decoding strategy:

- Applies temperature scaling to logits.
- Applies a token mask to exclude disallowed tokens.
- Implements nucleus (top-p) filtering via `top_p_filter`.
- Samples a token and also returns the top-k (k=8) candidate tokens and their probabilities.

### Sharding

The implementation uses JAX's `pjit` (parallel jit) to shard model parameters and activations across the device mesh. The partition rules are defined in the model configuration, and the state sharding is computed automatically based on the model's partition rules.

## Code of Conduct

This project has a Code of Conduct: "Be excellent to each other." See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

## License

This project is licensed under the Apache License 2.0. See [LICENSE.txt](LICENSE.txt) for the full text.
