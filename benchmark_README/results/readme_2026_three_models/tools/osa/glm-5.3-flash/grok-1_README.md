# Grok-1

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This repository contains the reference inference code for the Grok-1 large language model released by X.AI, enabling researchers and ML infrastructure engineers to run text generation from the released model weights on JAX-based multi-device hardware. It is aimed at practitioners with multi-GPU environments who want to execute the model or study its implementation, rather than at end users seeking a polished product. The code implements a Mixture-of-Experts transformer with 8-bit quantized weights and bfloat16 compute, executed across a sharded SPMD device mesh, and includes a minimal example of running text generation from local checkpoints and a tokenizer. Newcomers should start with Getting Started for setup and usage instructions.

---

## Core Features

- Runs the Grok-1 Mixture-of-Experts language model (64 layers, 8 experts with 2 selected per token) for text generation from locally stored weights.
- Distributes inference across multiple devices and hosts using JAX SPMD sharding, with configurable data and model parallelism via mesh settings.
- Performs autoregressive sampling with a configurable temperature.
- Loads sharded 8-bit quantized checkpoints from a local checkpoint directory.
- Tokenizes input text with SentencePiece and supports long contexts up to an 8192-token sequence length.

---

## Installation

Install the project dependencies from the repository root:

```sh
pip install -r requirements.txt
```

---

## Getting Started

**Prerequisites**

- Python environment with the dependencies listed in `requirements.txt` (JAX, Haiku, NumPy, SentencePiece).
- A JAX runtime with 8 local devices visible — `run.py` builds a mesh with `local_mesh_config=(1, 8)`.
- Model weights and tokenizer present locally:
  - Checkpoint directory at `./checkpoints/`
  - SentencePiece tokenizer file at `./tokenizer.model`

**Steps**

1. Install the dependencies (see Installation):

```bash
   pip install -r requirements.txt
```

2. Place the model weights in `./checkpoints/` and the tokenizer at `./tokenizer.model` in the repository root.

3. Run the example inference script:

```bash
   python run.py
```

   This loads the checkpoint, initializes an 8-way device mesh (`local_mesh_config=(1, 8)`, `between_hosts_config=(1, 1)`), and generates from the fixed prompt `"The answer to life the universe and everything is of course"` with `temperature=0.01` and `max_len=100`.

4. Verify the output: the script prints the prompt and the generated sample to stdout.

Note: checkpoint loading stages tensors through `/dev/shm`, so ensure sufficient space in shared memory.

---

## Contributing

Please review and follow the [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) when contributing to this project.

---

## License

This project is licensed under the Apache License 2.0. For more details, refer to the [LICENSE](./LICENSE.txt) file.

---

## Citation

If you use this project in your work, please cite it as:

### APA format:

    X.AI Corp. (2024). Grok-1 [Computer software].

### BibTeX format:

    @misc{grok-1,

        author = {X.AI Corp.},

        title = {Grok-1},

        year = {2024},

        note = {Released under the Apache License 2.0.}

    }

---
