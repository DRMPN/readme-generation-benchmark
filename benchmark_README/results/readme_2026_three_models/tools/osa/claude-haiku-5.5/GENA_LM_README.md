# GENA_LM-t88wk_f4

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

GENA-LM is a genomic language model project built on a BERT-based architecture, with a recurrent memory transformer variant for processing long sequences in segments. It is intended for researchers and bioinformatics or machine learning practitioners working on genomic sequence modeling, such as splicing, promoter, and expression prediction tasks. The repository provides a Python library for model and tokenizer code, data preparation workflows, and a set of downstream task folders, along with example notebooks for exploring usage. For runnable steps, see the Getting Started section.

---

## Core Features

- **Genomic language model with long-input support:** Provides a BERT-based model with a recurrent memory variant that splits long sequences into segments and carries memory tokens across them, so longer genomic inputs can be processed without a custom pipeline.
- **Downstream genomic prediction tasks:** Includes fine-tuning pipelines for splice-site, promoter, and regulatory sequence prediction tasks, each with its own dataset and run scripts, so you can adapt the model to specific tasks.
- **Genome-to-text corpus preparation:** Converts FASTA genome files (plain or gzipped) into text documents of sampled sentences for language-model training, so you can build pretraining data directly from assemblies.
- **BPE tokenizer training:** Trains a byte-pair-encoding tokenizer from text files with BERT-style special tokens and a configurable vocabulary size, so you can create a tokenizer matched to your corpus.
- **Per-organism data preparation:** Provides download and processing scripts for A. thaliana, fly, yeast, and human datasets, so you can generate training data for these organisms.

---

## Installation

Install GENA_LM-t88wk_f4 using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/GENA_LM-t88wk_f4
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

**Prerequisites**

- **Python:** The required Python version is not specified in the provided context. Check `pyproject.toml` or `setup.cfg` before installing.
- **Dependencies:** Listed in `requirements.txt`. The first-run path uses `click` and `tokenizers`. Corpus creation uses `Biopython`, `pandas`, and `tqdm`. The model code also depends on PyTorch and HuggingFace `transformers`.
- **Input data:** A genome FASTA file (plain or `.gz`) for corpus creation.

**Quickstart**

1. Install the dependencies listed in `requirements.txt`.
2. Create a text corpus from FASTA input with `src/gena_lm/genome_tools/create_corpus.py`. By default, it writes one `<chromosome_name>_documents.txt` file per chromosome. Review the script's argument definitions before running it.
3. Train a BPE tokenizer on the `*.txt` files in the corpus directory:

```bash
python src/gena_lm/tokenizers/tokenize_genomes.py --input_dir <corpus_dir> --output_dir <tokenizer_dir>
```

   Verified options:
   - `--input_dir`: directory containing `*.txt` files.
   - `--output_dir`: output directory (default `.`; created if missing).
   - `--vocab-size`: vocabulary size (default `32000`).
   - `--tokenizer_name`: output name prefix (default `BPE`).
   - `--limit-files`: maximum number of input files to use.

4. Verify the result: `<tokenizer_dir>/BPE.json` should exist after the command completes. If `--tokenizer_name` is changed, the file is `<tokenizer_name>.json`. The file is a serialized tokenizer saved by the `tokenizers` library.

**Next steps**

- **Downstream tasks:** Each task folder contains a `run_*.py` script and a shell launcher. Use the README in that folder for arguments and run instructions.
- **Pretraining:** Training is driven by shell scripts in the repository. The specific pretraining script and its arguments are not identified in the provided context. Consult the shell launchers in the repository.

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

    README Benchmark (2026). GENA_LM-t88wk_f4 repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{GENA_LM-t88wk_f4,

        author = {README Benchmark},

        title = {GENA_LM-t88wk_f4 repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---