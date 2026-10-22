# GENA_LM-_gd_4ltt

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

GENA_LM is a Python research toolkit for genomic sequence language modeling, supporting work from sequence tokenization and corpus preparation through downstream model fine-tuning and evaluation. It is intended for researchers and bioinformatics or machine-learning developers working with genomic sequence data. The repository offers reusable modeling and data-processing code alongside task-oriented scripts and notebook workflows; see Getting Started for runnable entry points.

---

## Core Features

- Prepare genomic sequence corpora to create data for language-model workflows.
- Tokenize genomic sequences to make them usable as model inputs.
- Support genomic sequence language modeling and downstream model fine-tuning and evaluation.

---

## Installation

Install GENA_LM-_gd_4ltt using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/GENA_LM-_gd_4ltt
```

2. Install the project in editable mode:

```sh
pip install -e .
```

---

## Getting Started

Prerequisites: Python with `click` and `tokenizers` available, plus an input directory containing `.txt` files.

1. Run the tokenizer script, replacing the placeholders with your directories:

```bash
python src/gena_lm/tokenizers/tokenize_genomes.py --input_dir "<input-dir>" --output_dir "<output-dir>"
```

The script creates the output directory if needed and saves the tokenizer as `BPE.json` there.

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

    README Benchmark (2026). GENA_LM-_gd_4ltt repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{GENA_LM-_gd_4ltt,

        author = {README Benchmark},

        title = {GENA_LM-_gd_4ltt repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---