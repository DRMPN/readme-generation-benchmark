# Grok-1 Inference Example

This repository contains a JAX and Haiku implementation of a Grok-1 language model and an example program for running text generation. The example in `run.py` configures a model, restores parameters from a local checkpoint directory, tokenizes a prompt with SentencePiece, and prints generated text.

The model code includes a transformer with multi-head attention, rotary embeddings, RMS normalization, and a mixture-of-experts (MoE) feed-forward layer. It also defines JAX sharding rules for distributing model parameters and activations across a device mesh. The example configuration uses 64 layers, 48 query heads, 8 key/value heads, and 8 experts.

## Requirements

The pinned dependencies are listed in `requirements.txt`:

- `dm_haiku==0.0.12`
- `jax[cuda12-pip]==0.4.25`
- `numpy==1.26.4`
- `sentencepiece==0.2.0`

The JAX requirement is configured for CUDA 12. The example also configures a two-axis device mesh and sets its local mesh shape to `(1, 8)`, so its settings should be reviewed for the devices and environment where you intend to run it.

## Setup

1. Create and activate a Python environment appropriate for the pinned dependencies.
2. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. Put Grok-1 checkpoint files in the `checkpoints/` directory. The checkpoint directory README instructs users to place Grok-1 checkpoints there so the example can load them.
4. Ensure `tokenizer.model` is available at the repository root. This file is included in the repository, and the example points to it by default.

The checkpoint loader looks for `ckpt-0` inside the configured checkpoint directory. Its tensor-loading code expects files named in the form `tensorNNNNN_NNN` within that directory. The supplied files do not document a checkpoint download location or a process for converting checkpoint files, so those details are not specified here.

## Usage

From the repository root, run:

```bash
python run.py
```

The script initializes the inference runner, loads the checkpoint and tokenizer, and generates text for this prompt:

> The answer to life the universe and everything is of course

It requests up to 100 generated tokens with temperature `0.01`, then prints the prompt and result. Checkpoint loading and model initialization require the configured files and a JAX environment capable of running the selected device mesh.

## Configuration

The example’s model and inference settings are defined directly in `run.py`:

- **Checkpoint directory:** `./checkpoints/`
- **Tokenizer:** `./tokenizer.model`
- **Vocabulary size:** `128 * 1024`
- **Sequence length:** `8192`
- **Embedding size:** `48 * 128`
- **Transformer layers:** `64`
- **Query and key/value heads:** `48` and `8`
- **MoE experts:** `8`, with `2` selected per token
- **Local mesh:** `(1, 8)`
- **Between-host mesh:** `(1, 1)`
- **Padding buckets:** `(1024,)`

`ModelRunner` also sets `bs_per_device=0.125` in the example. These values are source-code defaults for this example, not a general hardware recommendation.

The `InferenceRunner` accepts a list of padding sizes, a tokenizer path, and local and between-host mesh configurations. `ModelRunner` exposes checkpoint rename and exclusion rules, an RNG seed, and a `transform_forward` option. The example uses the runner’s default RNG seed and does not set checkpoint rename or exclusion rules.

Generation requests are represented by a prompt, temperature, nucleus probability (`nucleus_p`), RNG seed, and maximum length. `sample_from_model` is a convenience helper that submits a request with `nucleus_p=1.0` and RNG seed `42`. The example calls it with the prompt, maximum length, and temperature shown above.

## Project Files

- `model.py` defines model components, configuration dataclasses, memory structures, and partition rules.
- `checkpoint.py` contains checkpoint restoration and tensor-loading helpers.
- `runners.py` implements model initialization, inference batching, token sampling, and device-mesh construction.
- `run.py` is the runnable example.
- `tokenizer.model` is the SentencePiece tokenizer model used by the example.
- `checkpoints/README.md` describes where to place checkpoint files.
- `requirements.txt` pins runtime dependencies.

## Development

The repository’s `pyproject.toml` contains Ruff settings: indentation width is 4 spaces, maximum line length is 100 characters, and the configured selected lint rule is `ISC001`. Several rules are explicitly ignored there. No packaging, build, or contribution workflow is specified in the supplied files.

The code of conduct is: “Be excellent to each other.”

## Testing

No test files or test commands are included in the supplied repository contents. A practical end-to-end check is to run `python run.py` after installing dependencies and placing a compatible checkpoint in the expected location. This exercises initialization, checkpoint restoration, tokenization, and generation; it is not a substitute for a dedicated automated test suite.

## License

The repository includes `LICENSE.txt`, which contains the Apache License, Version 2.0. Refer to that file for the full license terms.
