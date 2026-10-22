# Grok-1

This repository contains a JAX/Haiku implementation of a transformer language model and an inference example configured for Grok-1. The example loads model parameters from a local checkpoint, tokenizes a prompt with SentencePiece, and generates text.

## Repository contents

- `model.py` implements the transformer, attention, Mixture-of-Experts layers, model configuration, and key/value memory used during autoregressive inference.
- `runners.py` provides checkpoint-backed model setup, batching, sampling, and the `InferenceRunner` prompt-generation interface.
- `checkpoint.py` restores parameter tensors from the checkpoint file layout expected by the runner.
- `run.py` configures the example model and runs a short generation.
- `tokenizer.model` is the SentencePiece model used by the example.
- `checkpoints/` is the expected location for model checkpoint files; checkpoint files are not included in this repository.

The example configuration in `run.py` sets a vocabulary size of 128K, a sequence length of 8,192, 64 transformer layers, 48 query heads, 8 key/value heads, and 8 experts with 2 selected per token. It also configures a local device mesh of `(1, 8)`.

## Requirements

The pinned Python dependencies are listed in `requirements.txt`:

- `dm-haiku` 0.0.12
- JAX with the CUDA 12 pip extra, version 0.4.25
- NumPy 1.26.4
- SentencePiece 0.2.0

Install them in an environment with a compatible CUDA 12 JAX setup:

```bash
python -m pip install -r requirements.txt
```

The supplied `run.py` configuration uses an eight-device local mesh. Make the required devices available to JAX before running it.

## Checkpoint setup

Place the checkpoint under `checkpoints/ckpt-0/`. The restore code reads serialized tensor files from that directory; checkpoint files are ignored by Git, while `checkpoints/README.md` is retained. The runner expects checkpoint parameter shapes and names to match the model configuration.

## Run the example

From the repository root, run:

```bash
python run.py
```

The script initializes inference, loads the checkpoint from `./checkpoints/`, uses `./tokenizer.model`, and generates up to 100 tokens for a prompt embedded in `run.py`. Its example sampling temperature is `0.01`.

The checkpoint must be present and the configured JAX devices must be available; otherwise initialization or checkpoint restoration will fail. The prompt, checkpoint path, mesh settings, and sampling parameters are currently set in `run.py` rather than exposed as command-line options.

## Using the inference runner

`InferenceRunner` in `runners.py` provides a generator-based interface for submitting requests. A request has a prompt, temperature, nucleus probability (`nucleus_p`), random seed, and maximum output length. `sample_from_model` is a small convenience helper used by `run.py`; it submits one request and returns its generated text.

## License

The source files include Apache License 2.0 notices. See [`LICENSE.txt`](LICENSE.txt) for the license text. See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) for the repository's code of conduct.
