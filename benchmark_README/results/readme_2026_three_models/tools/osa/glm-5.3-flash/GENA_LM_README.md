# GENA_LM-jq6k16ia

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![numpy](https://img.shields.io/badge/NumPy-013243.svg?style={0}&logo=NumPy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style={0}&logo=pandas&logoColor=white)
![tqdm](https://img.shields.io/badge/tqdm-FFC107.svg?style={0}&logo=tqdm&logoColor=black)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

GENA_LM is a toolkit for building and studying genomic DNA language models. It provides Python implementations of transformer-based DNA models, tooling for preparing genome corpora and training tokenizers, and downstream genomics benchmark tasks for finetuning and evaluation. The project targets computational biology and machine-learning researchers and bioinformaticians who pretrain, finetune, and evaluate DNA language models on genomics problems. Workflows span a Python package, command-line utilities, notebook-based examples, and script-driven training and evaluation runs; see Getting Started for runnable steps.

---

## Core Features

- **DNA language models** – BERT-style transformer models for genomic sequences built on PyTorch and HuggingFace Transformers, so researchers can pretrain and finetune them with familiar, standard tooling.
- **Long-sequence modeling** – Recurrent Memory Transformer support that processes long DNA inputs as segments connected by memory tokens, letting models handle sequences longer than the base model's context window.
- **Genomics benchmark pipelines** – Ready-to-use finetuning and evaluation workflows for established tasks such as DeepSTARR, DeepSea, SpliceAI, Enformer, promoter prediction, and ClinVar variant analysis, so models can be compared on standard benchmarks without reimplementing each task.
- **Genome preprocessing and tokenization** – Tooling that turns FASTA genomes into pretraining corpora and trains custom BPE tokenizers, so you can build domain-specific pretraining data and vocabularies.
- **Multi-organism data preparation** – Download and preprocessing scripts covering human, fly, yeast, and A. thaliana, with predefined holdout regions for reproducible evaluation splits.

---

## Installation

Install GENA_LM-jq6k16ia using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/GENA_LM-jq6k16ia
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

The steps below cover the minimal path from a fresh environment to a first run: install dependencies, prepare genome data, build a corpus, and launch a downstream task.

**Prerequisites**

- A Python environment with PyTorch and HuggingFace Transformers; see `requirements.txt` for the complete dependency list.

**Steps**

1. Install the dependencies from the repository root:

```bash
   pip install -r requirements.txt
```

2. Download and preprocess genome data for your organism with the scripts under `data/` (scripts are provided for human, fly, yeast, and A. thaliana). This directory also contains holdout chromosome BED files and prebuilt tokenizer assets.

3. Build a pretraining corpus from genome FASTA files (plain or `.gz`) with `src/gena_lm/genome_tools/create_corpus.py`; see `src/gena_lm/genome_tools/README.md` for usage and output options.

4. Use the prebuilt tokenizer assets under `data/`, or train a custom BPE tokenizer over the corpus with HuggingFace `tokenizers`.

5. Run a downstream benchmark from `downstream_tasks/`. Each task (APARENT, DeepSTARR, DeepSea, SpliceAI, Enformer, promoter_prediction, clinvar_analysis, splicing_onemut) provides its own dataset class, run script, and shell configs. Follow the README in the chosen task folder (available for DeepSTARR, DeepSea, SpliceAI, Enformer, and promoter prediction); ClinVar analysis notebooks are included as worked examples.

---

## Examples

Examples of how this should work and how it should be used are available [here](./notebooks).

---

## Contributing

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). GENA_LM-jq6k16ia repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{GENA_LM-jq6k16ia,

        author = {README Benchmark},

        title = {GENA_LM-jq6k16ia repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---