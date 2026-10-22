# Grok-1

This repository contains JAX and Haiku code for running inference with Grok-1, a mixture-of-experts (MoE) transformer language model released by X.AI. The code is Apache 2.0 licensed. The model weights are **not** included in this repository and must be obtained separately.

## Contents

| Path | Description |
| --- | --- |
| `model.py` | Model definition: transformer decoder stack, multi-head attention with grouped-query heads, rotary embeddings, RMSNorm, MoE layer and router, and sharding partition rules. |
| `runners.py` | Inference runner: loads the model onto a device mesh, prefills prompts, samples tokens (temperature and nucleus/top-p sampling), and manages a batched key/value cache. Also defines `make_mesh` and `sample_from_model`. |
| `checkpoint.py` | Checkpoint restore logic. Reads per-tensor pickled files from a `ckpt-0` directory and places them onto the device mesh. |
| `run.py` | Example script that configures Grok-1, loads the checkpoint, and generates text from a single prompt. |
| `checkpoints/` | Directory where checkpoint files are expected. Contains only a placeholder `README.md`. |
| `tokenizer.model` | SentencePiece tokenizer model used to encode prompts and decode outputs. |
| `requirements.txt` | Pinned Python dependencies. |
| `pyproject.toml` | Ruff configuration (line length 100, 4-space indent). |
| `LICENSE.txt` | Apache License, Version 2.0. |
| `CODE_OF_CONDUCT.md` | Code of conduct for contributors. |

## Model configuration

The example in `run.py` uses the following configuration:

- Vocabulary size: 131,072 (`128 * 1024`)
- Layers: 64
- Embedding size: 6,144 (`48 * 128`)
- Attention: 48 query heads, 8 key/value heads, key size 128
- Feed-forward: widening factor 8, with GELU-gated linear units
- Mixture of experts: 8 experts, 2 selected per token
- Maximum sequence length: 8,192 tokens
- Attention logits are soft-capped with `30 * tanh(x / 30)`
- Position encoding: rotary embeddings (RoPE)
- Normalization: RMSNorm; input and output embeddings are tied

## Requirements

- Python with pip (the repository does not specify a Python version)
- `requirements.txt` pins:
  - `dm_haiku==0.0.12`
  - `jax[cuda12-pip]==0.4.25`, installed from the JAX CUDA release index listed in the file
  - `numpy==1.26.4`
  - `sentencepiece==0.2.0`
- The example in `run.py` builds a device mesh of shape `(1, 8)`, so it expects 8 local accelerator devices. The JAX build in `requirements.txt` targets CUDA 12.

## Installation

```bash
pip install -r requirements.txt
```

## Obtaining the checkpoint

The repository does not include the Grok-1 weights, and it does not state where they can be downloaded. Obtain the checkpoint from its source and place it in `checkpoints/`.

`checkpoint.py` expects this layout:

```
checkpoints/
└── ckpt-0/
    ├── tensor00000_000
    ├── tensor00001_000
    └── ...
```

Each file is a pickled tensor named `tensor{index:05d}_{shard:03d}`. Parameter names must match the names in the model code, or restore fails with a parameter mismatch error.

## Running the example

From the repository root, with the checkpoint in place:

```bash
python run.py
```

`run.py` loads the model and generates up to 100 tokens from the prompt `"The answer to life the universe and everything is of course"`, using temperature `0.01`. It prints the prompt and the generated output, and logs progress at the `INFO` level.

## Using the inference API

The main entry points are in `runners.py`:

1. Build a `LanguageModelConfig` and `TransformerConfig` (see `run.py`).
2. Create an `InferenceRunner` with a `ModelRunner`, the checkpoint path, the tokenizer path, and the mesh configuration.
3. Call `initialize()`, which compiles the model functions and loads parameters.
4. Call `run()` to get a generator, then use `sample_from_model(gen, prompt, max_len=..., temperature=...)` to generate text.

`InferenceRunner.run()` serves up to `batch_size` concurrent requests in slots. Prompts are padded to the buckets given by `pad_sizes`. Prompts longer than the largest bucket are left-truncated.

## Configuration notes

- `bs_per_device` in `ModelRunner` sets the batch size per device. The example uses `0.125`.
- `local_mesh_config` and `between_hosts_config` set the `(data, model)` device mesh within a host and across hosts.
- `checkpoint.py` registers `QuantizedWeight8bit` on the `__main__` module so checkpoints can be unpickled. Run the entry script directly, as `run.py` does.

## Limitations

- The repository contains no tests.
- The checkpoint is not included, so the example cannot run until you provide the weights.
- The repository does not state a Python version or hardware requirements beyond the 8-device mesh in the example and the CUDA 12 JAX build.
- The repository does not state a license for the model weights. The Apache 2.0 license in `LICENSE.txt` applies to the code.

## License

The code in this repository is licensed under the Apache License, Version 2.0. See [LICENSE.txt](LICENSE.txt).
