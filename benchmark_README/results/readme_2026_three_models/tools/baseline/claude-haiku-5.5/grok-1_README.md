# Grok-1 JAX Inference Example

This repository contains a JAX/Haiku inference example for a Grok-1 style transformer language model. It includes the model definition, a checkpoint loader, a SentencePiece tokenizer model, and a runner that generates text from a prompt. The code is distributed under the Apache License 2.0 and carries X.AI Corp. copyright headers.

## Overview

The repository contains these files:

| File | Purpose |
| --- | --- |
| `model.py` | Model definitions: the transformer, mixture-of-experts (MoE) layers, rotary embeddings, RMSNorm, and partitioning rules for sharding. |
| `runners.py` | `ModelRunner` and `InferenceRunner`, which build the device mesh, load parameters, compile prefill and sampling steps, and generate tokens. Also provides `sample_from_model`. |
| `checkpoint.py` | Checkpoint restoring helpers, including parallel tensor loading and fast pickle read/write through `/dev/shm`. |
| `run.py` | Example entry point. It defines the Grok-1 configuration and runs one prompt. |
| `checkpoints/README.md` | Says where model checkpoints should be placed. |
| `tokenizer.model` | SentencePiece tokenizer model used by the inference runner. |
| `requirements.txt` | Python dependencies. |
| `pyproject.toml` | Ruff linter configuration. |
| `CODE_OF_CONDUCT.md` | Community guidelines. |
| `LICENSE.txt` | Apache License, Version 2.0. |

The example model is configured in `run.py` with these characteristics:

- Vocabulary size of 128 × 1024 (131,072 tokens).
- Sequence length of 8192.
- An embedding size of 48 × 128 (6144).
- 64 decoder layers.
- 48 query heads and 8 key/value heads, with a key size of 128.
- Mixture-of-experts feed-forward blocks with 8 experts, where 2 experts are selected per token.
- Activation sharding enabled, with `data` and `model` mesh axes.

## Setup

### Requirements

The `requirements.txt` file pins these packages:

```text
dm_haiku==0.0.12
jax[cuda12-pip]==0.4.25 -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
numpy==1.26.4
sentencepiece==0.2.0
```

The JAX entry installs the CUDA 12 build and uses the JAX CUDA release index. The code relies on GPU devices. It creates a device mesh with `jax.devices()` and `mesh_utils.create_hybrid_device_mesh`. The repository does not specify a Python version.

### Installation

1. Clone the repository and change into its directory.
2. Create and activate a virtual environment.
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Place the model checkpoint in the `checkpoints/` directory. As described in `checkpoints/README.md`, the directory holds Grok-1 checkpoints so the example script can load them.

No checkpoint files are included in the repository. The file tree contains only `checkpoints/README.md`.

## Usage

Run the example from the repository root:

```bash
python run.py
```

The script calls `logging.basicConfig(level=logging.INFO)`, builds the model configuration, initializes the inference runner, and generates text for this prompt:

```text
The answer to life the universe and everything is of course
```

It uses `max_len=100` and `temperature=0.01`, then prints the result with the prompt.

### Using the runners programmatically

`run.py` shows the basic workflow:

```python
from model import LanguageModelConfig, TransformerConfig
from runners import InferenceRunner, ModelRunner, sample_from_model

inference_runner = InferenceRunner(
    pad_sizes=(1024,),
    runner=ModelRunner(
        model=grok_1_model,        # a LanguageModelConfig
        bs_per_device=0.125,
        checkpoint_path="./checkpoints/",
    ),
    name="local",
    load="./checkpoints/",
    tokenizer_path="./tokenizer.model",
    local_mesh_config=(1, 8),
    between_hosts_config=(1, 1),
)
inference_runner.initialize()
gen = inference_runner.run()

output = sample_from_model(gen, "Your prompt here", max_len=100, temperature=0.01)
```

`InferenceRunner.run()` is a generator. `sample_from_model` primes it with `next()`, sends a `Request`, and returns the decoded text when generation for that request ends. The request contains the prompt, temperature, `nucleus_p` (fixed at 1.0 by `sample_from_model`), an RNG seed (fixed at 42), and `max_len`.

Generation proceeds like this:

1. The prompt is encoded with SentencePiece.
2. The prompt is padded to the nearest bucket size from `pad_sizes`. The example uses only `(1024,)`.
3. A prefill step processes the prompt and writes its key/value memory into a batch slot.
4. Sampling steps generate one token per step for each active slot. Each slot stops when it reaches `max_len` tokens.

Generated tokens are decoded with the tokenizer and returned as a string.

## Configuration

Configuration is handled in code. No configuration files or command-line flags appear in the supplied files.

### Settings in `run.py`

- `CKPT_PATH = "./checkpoints/"`: the checkpoint directory. It is used for both the model runner and the `load` argument.
- `tokenizer_path="./tokenizer.model"`: path to the SentencePiece model.
- `local_mesh_config=(1, 8)`: local device mesh shape, mapped to the `("data", "model")` axes.
- `between_hosts_config=(1, 1)`: mesh shape across hosts.
- `pad_sizes=(1024,)`: prompt padding buckets. Prompts longer than the largest bucket are left-truncated by `pad_to_size`.
- `bs_per_device=0.125`: sets the global batch size as `int(bs_per_device × local GPUs × replicas)`.

### Model settings in `run.py`

`LanguageModelConfig` takes:

- `vocab_size`, `pad_token=0`, `eos_token=2`, `sequence_len=8192`.
- `embedding_multiplier_scale`, `output_multiplier_scale`, and `embedding_init_scale`.

`TransformerConfig` takes:

- `emb_size`, `key_size`, `num_q_heads`, `num_kv_heads`, `num_layers`.
- `widening_factor` and `attn_output_multiplier`.
- `num_experts` and `num_selected_experts` for the MoE layers.
- `shard_activations`, `data_axis`, and `model_axis`.

### Sampling settings

`sample_token` in `runners.py` uses:

- `temperature`: divides the logits before sampling.
- `nucleus_p`: top-p (nucleus) filtering.
- A `TOP_K = 8` constant, which controls how many top token probabilities are returned with each sample.

### Checkpoint loading

`checkpoint.py` restores a checkpoint from `<checkpoint_path>/ckpt-0`. Tensors are read from files named `tensor{index:05d}_{shard:03d}` using a thread pool of 32 workers. The loader performs these steps:

- Checks that parameter names in the checkpoint match the parameter names in the code. A mismatch raises a `ValueError` that lists the missing parameters.
- Supports rename and exclude rules through `load_rename_rules` and `load_exclude_rules` on `ModelRunner`.
- Reads and writes pickles through `/dev/shm/`, using temporary copies when needed.
- Registers `QuantizedWeight8bit` in `__main__` so pickled checkpoints can be unpickled.

Checkpoint loading is enabled by a non-empty `checkpoint_path`. When it is empty or `from_checkpoint` is `False`, the model is initialized with random parameters.

## Development

### Code layout

- `model.py` holds the transformer modules, the MoE router and layer, quantized-weight support, and partition rules (`TRANSFORMER_PARTITION_RULES`, `LM_PARTITION_RULES`).
- `runners.py` holds the inference loop and the device mesh construction in `make_mesh`.
- `checkpoint.py` holds the restore logic and file helpers.
- `run.py` is the example entry point.

Most source files start with the Apache 2.0 header. Follow that convention for new files.

### Linting

`pyproject.toml` configures Ruff:

- `indent-width = 4`
- `line-length = 100`
- Lint rule selection: `ISC001`.
- Ignored rules: `E722`, `E731`, `E741`, `E402`, `F403`, and `F405`.

The repository does not list Ruff in `requirements.txt`, so install it separately if you want to use the configuration:

```bash
pip install ruff
ruff check .
```

### Contributing

`CODE_OF_CONDUCT.md` contains the single line "Be excellent to each other." The supplied files do not include a contributing guide.

## Testing

The supplied files contain no test suite, test directory, or test runner configuration. The only automated check specified in the repository is the Ruff configuration in `pyproject.toml`. Running `python run.py` with a valid checkpoint and a suitable GPU setup is the only end-to-end check the repository describes.

## License

This project is licensed under the Apache License, Version 2.0. The full text is in `LICENSE.txt`. The Python source files carry the header:

```text
Copyright 2024 X.AI Corp.
```

Under this license, you may use, reproduce, modify, and distribute the work, subject to its conditions. The license is provided "AS IS," without warranties or conditions of any kind.
