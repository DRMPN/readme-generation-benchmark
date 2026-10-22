# Grok-1

This repository contains the open-source release of **Grok-1**, the mixture-of-experts language model from **X.AI Corp.** It provides JAX/HAiku-based model code, checkpoint loading utilities, and an example inference script that you can use to load Grok-1 weights and generate text.

> **Note:** This repository contains the model source code and inference tooling. Model weights are **not** included and must be downloaded separately (see [Checkpoints](#checkpoints) below).

## Overview

Grok-1 is a large, autoregressive transformer-based language model. Key architectural characteristics, as defined in `run.py` and implemented in `model.py`, include:

- **Mixture-of-Experts (MoE):** 8 experts per MoE layer with 2 selected experts per token (`num_experts=8`, `num_selected_experts=2`), dispatched via a learned router.
- **Grouped-query attention:** 48 query heads and 8 key/value heads (`num_q_heads=48`, `num_kv_heads=8`), with a key size of 128.
- **Depth and width:** 64 decoder layers, embedding size `48 * 128` (6144), and an FFN widening factor of 8.
- **Rotary positional embeddings (RoPE)** applied to query and key projections.
- **RMSNorm** for layer normalization throughout the model.
- **Vocabulary size:** 131,072 (`128 * 1024`) tokens, tokenized with [SentencePiece](https://github.com/google/sentencepiece) using the included `tokenizer.model`.
- **Sequence length:** 8192 tokens.
- **Quantized weights:** support for 8-bit quantized weights via the `QuantizedWeight8bit` structure.
- **bfloat16** forward-pass precision (`fprop_dtype=jnp.bfloat16`), with attention softmax computed in fp32.
- **KV caching ("memory")** for efficient autoregressive decoding, including batched prefill and incremental sampling.

The model supports both dense and MoE decoder layers, sharded execution across data and model axes, and sampling with temperature and nucleus (top-p) filtering.

## Repository Structure

```
.
├── model.py              # Transformer / MoE model implementation (Haiku modules)
├── runners.py            # Inference runner, mesh setup, sampling logic
├── checkpoint.py         # Checkpoint loading/restoration utilities
├── run.py                # Example inference script
├── tokenizer.model       # SentencePiece tokenizer model
├── checkpoints/
│   └── README.md         # Where to place downloaded checkpoints
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Ruff linting configuration
├── LICENSE.txt           # Apache License 2.0
└── CODE_OF_CONDUCT.md    # Community guidelines
```

## Requirements

- **Hardware:** an NVIDIA GPU setup with CUDA 12 support. The `jax[cuda12-pip]` requirement is installed from the JAX CUDA release repository. The example configuration in `run.py` uses a local mesh of `(1, 8)`, i.e., 8 devices on a single host.
- **Software:** Python with the following pinned dependencies (`requirements.txt`):

```
dm_haiku==0.0.12
jax[cuda12-pip]==0.4.25
numpy==1.26.4
sentencepiece==0.2.0
```

The model also relies on shared memory (`/dev/shm/`) for fast checkpoint loading, so ensure your environment provides a sufficiently large `/dev/shm` mount.

## Installation

1. Clone this repository.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The JAX line includes a `-f` find-links flag pointing to the JAX CUDA releases page, so a CUDA 12-enabled JAX build will be installed automatically on supported systems.

3. Download the Grok-1 checkpoint and place it under `./checkpoints/` (see next section).

## Checkpoints

The example script loads weights from the `./checkpoints/` directory (`CKPT_PATH = "./checkpoints/"`). As described in `checkpoints/README.md`, place the downloaded Grok-1 checkpoints there so they can be loaded by the example script.

Checkpoint loading is handled by `checkpoint.py`:

- Checkpoints are unpickled quickly by first copying files into shared memory (`/dev/shm/`) via `copy_to_shm` / `fast_unpickle`.
- Tensors are loaded in parallel with a thread pool (`load_tensors`), respecting the between-hosts sharding configuration so that each process loads only the shards it needs.
- The `restore` function flattens the expected parameter tree, matches tensor files, validates that checkpoint keys match the code's parameter keys (raising a `ValueError` on mismatch when no init state is supplied), and reshards arrays onto the JAX mesh via `host_local_array_to_global_array`.
- Note that checkpoints are pickled with the `QuantizedWeight8bit` class; `checkpoint.py` registers this class in `sys.modules['__main__']` so pickles can be loaded directly.

## Usage

To run the example inference script:

```bash
python run.py
```

The script performs the following steps:

1. Defines the Grok-1 model configuration (`LanguageModelConfig` + `TransformerConfig`) with the architecture described above.
2. Creates an `InferenceRunner` with:
   - `pad_sizes=(1024,)` — prompt padding buckets for precompilation.
   - `bs_per_device=0.125` — batch size per device.
   - `checkpoint_path` and `load` both set to `./checkpoints/`.
   - `tokenizer_path="./tokenizer.model"`.
   - `local_mesh_config=(1, 8)` and `between_hosts_config=(1, 1)` — a mesh of 8 local devices split into `data` and `model` axes.
3. Initializes the runner (loads the tokenizer, builds the mesh, restores checkpoint parameters, and pre-compiles the prefill and sampling steps).
4. Runs a sample generation:

   ```python
   inp = "The answer to life the universe and everything is of course"
   print(f"Output for prompt: {inp}", sample_from_model(gen, inp, max_len=100, temperature=0.01))
   ```

### Programmatic usage

`InferenceRunner.run()` returns a generator that accepts `Request` objects and yields generated strings:

```python
gen = inference_runner.run()
next(gen)  # prime the generator

output = gen.send(Request(
    prompt="Your prompt here",
    temperature=0.8,
    nucleus_p=1.0,
    rng_seed=42,
    max_len=100,
))
```

Sampling parameters per request include:

- **`temperature`** — scales logits before sampling.
- **`nucleus_p`** — nucleus (top-p) filtering threshold via `top_p_filter`.
- **`rng_seed`** — per-request random seed for reproducible sampling.
- **`max_len`** — maximum number of generated tokens.

Each sampling step also returns the top-k (k=8) token ids and probabilities alongside the sampled token.

## Configuration

The model is configured through two dataclasses in `model.py`:

- **`TransformerConfig`** — core architecture parameters: `emb_size`, `key_size`, `num_q_heads`, `num_kv_heads`, `num_layers`, `vocab_size`, `widening_factor`, `attn_output_multiplier`, MoE settings (`num_experts`, `num_selected_experts`, `capacity_factor`), and sharding settings (`shard_activations`, `data_axis`, `model_axis`).
- **`LanguageModelConfig`** — wraps the transformer config with `vocab_size`, `pad_token`, `eos_token`, `sequence_len`, embedding/output scaling multipliers, `fprop_dtype`, and embedding sharding options.

Parameter sharding is driven by rule lists (`TRANSFORMER_PARTITION_RULES`, `LM_PARTITION_RULES`) that map parameter name patterns (regexes) to `jax.sharding.PartitionSpec` entries over the `"data"` and `"model"` mesh axes. The `apply_rules` helper applies these rules during sharding inference via `tree_map_with_path`.

The compute mesh is created by `make_mesh` in `runners.py` using `mesh_utils.create_hybrid_device_mesh`, combining the per-host local mesh with the between-hosts configuration into a two-axis (`data`, `model`) mesh.

## Development

- **Linting:** the project uses [Ruff](https://github.com/astral-sh/ruff), configured in `pyproject.toml` with an indent width of 4 and a line length of 100. A small set of lint rules are ignored (`E722`, `E731`, `E741`, `F405`, `E402`, `F403`) and `ISC001` is selected. Run:

  ```bash
  ruff check .
  ```

- **Logging:** the code uses standard Python logging. The example script enables `INFO`-level logging via `logging.basicConfig(level=logging.INFO)`. Rank-specific messages are routed to a dedicated `"rank"` logger.

## Testing

This repository does not include an automated test suite. You can verify your installation by running the example script end-to-end:

```bash
python run.py
```

If the checkpoint loads and the script prints a completion for the sample prompt, the environment, checkpoint placement, and device mesh are all configured correctly. Troubleshooting hints:

- Parameter/key mismatches between the checkpoint and code raise a descriptive `ValueError` during `restore`.
- Checkpoint files are expected under `./checkpoints/ckpt-0/` (the restore function joins `ckpt-0` to the given path).
- Ensure `/dev/shm` is large enough to hold checkpoint shards during loading.

## Code of Conduct

Contributors and users are expected to follow the guidelines in `CODE_OF_CONDUCT.md`: be excellent to each other.

## License

This project is licensed under the **Apache License, Version 2.0**. See `LICENSE.txt` for the full license text. Copyright is held by X.AI Corp. (2024).

Unless required by applicable law or agreed to in writing, the software is distributed on an "AS IS" basis, without warranties or conditions of any kind, either express or implied. See the License for the specific language governing permissions and limitations.
