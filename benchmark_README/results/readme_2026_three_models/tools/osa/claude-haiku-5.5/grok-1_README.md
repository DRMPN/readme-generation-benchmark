# grok-1-4msxi7bo

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project provides JAX and Haiku code for running inference with a large transformer language model that uses a mixture-of-experts configuration. It is aimed at ML researchers and developers who are comfortable with multi-device JAX execution and large model checkpoints, and it requires a specific checkpoint and tokenizer to operate. The repository currently offers a command-line style entry point for generating text from a prompt, and no training workflow is visible in the reviewed code. For runnable steps, including environment preparation and checkpoint placement, see the Getting Started section.

---

## Core Features

- **Large-scale MoE transformer inference:** Runs a JAX/Haiku language model configured with 64 layers, 8 experts with top-2 routing, and an 8192-token sequence length, giving developers a working reference for serving a mixture-of-experts model.
- **Multi-device sharded execution:** Distributes model parameters and activations across a device mesh using JAX sharding and pjit partition rules, so the model can run across multiple accelerators.
- **Text generation with nucleus and top-k sampling:** Generates continuations from a prompt with configurable temperature, top-p filtering, and top-k probability reporting, letting developers control output randomness.
- **8-bit quantized weight support:** Loads checkpoint weights stored as 8-bit quantized tensors with per-tensor scales and runs the forward pass in bfloat16, reducing memory footprint for large-model inference.
- **Sharded checkpoint loading:** Loads tensor shards in parallel from a checkpoint directory, using shared-memory staging to speed up reading large pickled weight files.

---

## Installation

Install grok-1-4msxi7bo using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/grok-1-4msxi7bo
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

### Prerequisites

- Python with the dependencies listed in `requirements.txt` (the exact versions are not specified in this README).
- A checkpoint in `./checkpoints/` (see `checkpoints/README.md`).
- The tokenizer model at `./tokenizer.model`.
- Multi-device hardware: `run.py` sets `local_mesh_config=(1, 8)`, so the default run expects a mesh of 8 local devices.

### Steps

1. Install dependencies:

```bash
   pip install -r requirements.txt
```

2. Place the checkpoint files in `./checkpoints/` and the tokenizer model at `./tokenizer.model`, relative to the repository root. `run.py` uses these paths as defined.

3. Run the inference example:

```bash
   python run.py
```

   `run.py` loads the checkpoint, samples a continuation of a built-in prompt (up to 100 tokens), and prints the output. Logging is set to `INFO`.

---

## Architecture

The codebase is a single-package Python layout with no service boundaries observed. Inference is the only visible workflow; training code is not present in the provided context.

- **Entry point and configuration (`run.py`)**: Defines the model configuration, constructs an `InferenceRunner`, initializes it, and runs sampling for a prompt.
- **Inference orchestration (`runners.py`)**: `InferenceRunner` and `ModelRunner` set up the device mesh, compute batch sizes, and build forward functions. Sampling uses temperature scaling, top-p (nucleus) filtering, and top-k probability reporting.
- **Model definition (`model.py`)**: Contains the Haiku-based transformer language model, a mixture-of-experts (MoE) configuration (8 experts, 2 selected per token), 8-bit quantized weight container (`QuantizedWeight8bit`), and partition rules that map parameters to JAX sharding specs.
- **Checkpoint I/O (`checkpoint.py`)**: Loads and saves sharded tensors via pickle. Files are staged through `/dev/shm/` for faster access, and tensor loading is parallelized with a thread pool.
- **Control and data flow**: `run.py` → `InferenceRunner` → `ModelRunner` builds the mesh and forward function → `checkpoint.py` loads weights → tokenized input flows through the model via pjit/sharded execution → sampled token IDs are decoded back to text using `tokenizer.model`.

The execution target is multi-device JAX. The default local mesh configuration `(1, 8)` in `run.py` suggests an 8-device setup, though this is not confirmed by other evidence.

---

## Contributing

---

## License

This project is protected under the Apache 2.0. For more details, refer to the [LICENSE](./LICENSE.txt) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). grok-1-4msxi7bo repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{grok-1-4msxi7bo,

        author = {README Benchmark},

        title = {grok-1-4msxi7bo repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---