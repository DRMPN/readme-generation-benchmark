# GENA-LM — Genomic Analysis with Language Models

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Transformers](https://img.shields.io/badge/%F0%9F%A4%97-transformers-yellow.svg)](https://huggingface.co/)

**GENA-LM** is a family of open-source foundational DNA language models (BERT-style encoders) pre-trained with masked language modeling on genomic sequences. The repository contains everything needed to reproduce the full pipeline: genome download & preprocessing, BPE tokenizer training, pre-training corpus construction, model configs (including sparse-attention and Recurrent Memory Transformer variants), and complete fine-tuning pipelines for a broad set of downstream genomics tasks (DeepSEA, SpliceAI, APARENT, Enformer/Basenji, DeepSTARR, promoter detection, ClinVar variant interpretation, and sequence clustering).

---

## Table of Contents

- [Overview](#overview)
- [Models](#models)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Tokenization](#tokenization)
- [Repository Structure](#repository-structure)
- [Data Download & Preprocessing](#data-download--preprocessing)
- [Pre-training Corpus Construction](#pre-training-corpus-construction)
- [Pre-training](#pre-training)
- [Downstream Fine-tuning](#downstream-fine-tuning)
  - [Promoter detection](#1-promoter-detection)
  - [DeepSEA](#2-deepsea--chromatin-activity-prediction)
  - [SpliceAI](#3-spliceai--splice-site-prediction)
  - [APARENT](#4-aparent--polyadenylation-prediction)
  - [Enformer / Basenji](#5-enformer--basenji--gene-expression-prediction)
  - [DeepSTARR](#6-deepstarr--enhancer-activity-prediction)
- [Notebooks & Tutorials](#notebooks--tutorials)
- [ClinVar Analyses](#clinvar-analyses)
- [Requirements](#requirements)
- [License](#license)
- [Citation](#citation)

---

## Overview

GENA-LM models operate directly on raw DNA sequences. Key features of the family:

- **Byte-Pair Encoding (BPE) over nucleotides** — a vocabulary of **32,768** learned DNA "words" (`V32k` in the config names), which packs long DNA regions into far fewer tokens than single-nucleotide tokenization.
- **BERT-style encoders** — base (`L12-H768-A12`) and large (`L24-H1024-A16`) architectures with pre-LayerNorm blocks.
- **Long-context variants** — sparse attention with Rotary Position Embeddings (RoPE) and a HuggingFace **BigBird** implementation for **4,096-token** contexts.
- **Recurrent Memory Transformer (RMT) variants** — memory tokens are passed between sequence segments, enabling processing of sequences **far beyond the standard attention window**.
- **Multi-species pre-training** — corpora built from many Ensembl/ENA genomes (human, *D. melanogaster*, *S. cerevisiae*, *A. thaliana*, and others), with carefully held-out genomic regions for evaluation.

---

## Models

Pre-trained weights are distributed via the Hugging Face Hub (see the `AIRI` organization). The config files in this repository define the corresponding architectures:

| Model | Config file | Layers / Hidden / Heads | Vocab | Context | Notes |
|---|---|---|---|---|---|
| GENA-LM BERT base | `configs/L12-H768-A12-V32k-preln.json` | 12 / 768 / 12 | 32k | 512 | pre-LayerNorm |
| GENA-LM BERT base (last-LN) | `configs/L12-H768-A12-V32k-preln-lastln.json` | 12 / 768 / 12 | 32k | 512 | + final LayerNorm |
| GENA-LM BERT large | `configs/L24-H1024-A16-V32k-preln-lastln.json` | 24 / 1024 / 16 | 32k | 512 | large encoder |
| GENA-LM BERT base 4096 (sparse + RoPE) | `configs/L12-H768-A12-V32k-L4096-preln-sparse-rope.json` | 12 / 768 / 12 | 32k | 4,096 | sparse attention, rotary embeddings |
| GENA-LM BERT base 4096 (sparse, last-LN) | `configs/L12-H768-A12-V32k-L4096-preln-lastln-sparse-ln1e-05.json` | 12 / 768 / 12 | 32k | 4,096 | sparse, tuned LN ε |
| GENA-LM BigBird (HF) | `configs/hf_bigbird_L12-H768-A12-V32k-L4096.json` | 12 / 768 / 12 | 32k | 4,096 | HuggingFace BigBird implementation |
| GENA-LM RMT | `gena_lm/modeling_rmt.py` | base backbone | 32k | long (multi-segment) | Recurrent Memory Transformer |
| GENA-LM Multi-species | see [Pre-training](#pre-training) | 12 / 768 / 12 | 32k | 512 | trained on many species |

The config naming convention encodes the architecture:
`L<layers>-H<hidden size>-A<attention heads>-V<vocab size>[-L<context length>]-<features>`,
e.g. `L12-H768-A12-V32k-L4096-preln-sparse-rope` = 12 layers, hidden size 768, 12 heads, 32k vocab, 4096-token context, pre-LayerNorm, sparse attention with RoPE.

---

## Installation

```bash
git clone <this-repository-url>
cd GENA_LM
pip install -r requirements.txt
# or install as a package:
pip install -e .
```

Requirements: Python ≥ 3.8, PyTorch, `transformers`, `tokenizers`, `numpy`, `pandas`, `h5py`, `scikit-learn`, `matplotlib`/`seaborn` (for the notebooks). See `requirements.txt` for the full pinned list.

---

## Quick Start

### Load a pre-trained model from the Hugging Face Hub

```python
import torch
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("AIRI/GENA-LM-BERT-base")
model = AutoModel.from_pretrained("AIRI/GENA-LM-BERT-base", trust_remote_code=True)

dna = "CTGACTGCAGATCACGACGTACGTAGCTAGCTAGGCATCGATCGATCGGATCGATCG"
enc = tokenizer(dna, return_tensors="pt")

with torch.no_grad():
    outputs = model(**enc)

cls_embedding     = outputs.last_hidden_state[:, 0, :]   # [CLS] embedding
token_embeddings  = outputs.last_hidden_state            # per-BPE-token embeddings
```

> **Note:** models are distributed with their custom modeling code (`modeling_bert.py`, `modeling_rmt.py`), hence `trust_remote_code=True`.

- Use `AIRI/GENA-LM-BERT-large` for the large model.
- Use the **4096 / BigBird** checkpoints for longer contexts (up to 4,096 tokens).
- Use the **RMT** checkpoints for very long sequences (memory-based processing).

For a complete worked example — fine-tuning GENA-LM for binary sequence classification — see
[`GENA_sequence_classification_example.ipynb`](./GENA_sequence_classification_example.ipynb).

---

## Tokenization

The tokenizer is a **BPE tokenizer trained on genomic sequences** (nucleotide alphabet; `N` treated as a separate/unknown token). Both legacy and HuggingFace "fast" formats are provided:

| File | Description |
|---|---|
| `tokenizer.json`, `tokenizer_config.json`, `special_tokens_map.json` | HuggingFace fast-tokenizer export (recommended) |
| `BPE.json` | original BPE tokenizer (legacy format) |
| `BPE_no_n_all_chr.json` | BPE tokenizer trained on all chromosomes with `N` excluded from merge statistics |

Special tokens follow the standard BERT set: `[CLS]`, `[SEP]`, `[PAD]`, `[UNK]`, `[MASK]`. Input sequences should be **uppercase** nucleotides (`A`, `C`, `G`, `T`, `N`).

Because a single BPE token covers several bases, use the tokenizer offsets (`return_offsets_mapping=True`) to map model outputs back to nucleotide positions.

---

## Repository Structure

```
GENA_LM/
├── configs/                                  # pre-training architecture configs
│   ├── L12-H768-A12-V32k-preln.json
│   ├── L12-H768-A12-V32k-preln-lastln.json
│   ├── L24-H1024-A16-V32k-preln-lastln.json
│   ├── L12-H768-A12-V32k-L4096-preln-sparse-rope.json
│   ├── L12-H768-A12-V32k-L4096-preln-lastln-sparse-ln1e-05.json
│   └── hf_bigbird_L12-H768-A12-V32k-L4096.json
│
├── gena_lm/                                  # core modeling package
│   ├── __init__.py
│   ├── modeling_bert.py                      # BERT encoder (pre-LN, sparse attn, RoPE, BigBird)
│   ├── modeling_rmt.py                       # Recurrent Memory Transformer wrapper
│   └── utils.py
│
├── tokenizer/                                # BPE tokenizer (HF fast + legacy formats)
│   ├── tokenizer.json / tokenizer_config.json / special_tokens_map.json
│   ├── BPE.json
│   └── BPE_no_n_all_chr.json
│
├── genome_downloading/                       # per-species download & preprocessing
│   ├── download_data.sh
│   ├── download_human.sh
│   ├── full_ensembl_genomes_metadata.cvs
│   ├── download_and_process_athaliana_data.sh
│   ├── download_and_process_fly_data.sh
│   ├── fly.genomes.txt
│   ├── download_and_process_yeast_data.sh
│   ├── ENA_PRJEB59413_assmebly_links.tsv
│   ├── GCF_000001735_4.testholdout.bed       # human hold-out regions
│   ├── D_MELANOGASTER.testholdout.bed        # fly hold-out regions
│   ├── sacCer3.testholdout.bed               # yeast hold-out regions
│   └── valid_species_stats.tsv               # statistics of species used for training
│
├── corpus/                                   # pre-training corpus construction
│   ├── tokenize_genomes.py
│   ├── create_corpus.py
│   ├── create_allele_corpus.py
│   ├── create_multigenome_corpus.sh
│   └── 1KG+HGDP.selected_samples.tsv
│
├── notebooks/                                # tutorials & analyses (see below)
│   ├── GENA_sequence_classification_example.ipynb
│   ├── gena_enformer_usage.ipynb
│   ├── gena_clusterization_example.ipynb
│   ├── public_gena_clusters.ipynb / public_gena_clusters_task.ipynb
│   ├── clinvar.ipynb / clinvar_promoter_prediction.ipynb
│   ├── clinvar_attribution_prediction.ipynb
│   ├── make_exons_bed.ipynb
│   └── splice_check.ipynb
│
├── deepsea/                                  # DeepSEA fine-tuning
├── spliceai/                                 # SpliceAI fine-tuning
├── aparent/                                  # APARENT fine-tuning
├── enformer/                                 # Enformer/Basenji fine-tuning & evaluation
├── deepstarr/                                # DeepSTARR fine-tuning
├── promoter/                                 # promoter detection fine-tuning
├── clinvar/                                  # ClinVar data (BED, significance mapping)
│
├── setup.cfg / pyproject.toml / requirements.txt
├── LICENSE
└── ReadMe.md
```

Each downstream-task directory contains its own `README.md` with dataset download links, data-format details, and step-by-step instructions, plus small `test_*.py` unit tests validating the dataset classes.

---

## Data Download & Preprocessing

Scripts fetch genomes from public sources (Ensembl / NCBI / ENA), split them into training chunks, mask held-out regions, and prepare tokenization-ready text.

| Script / File | Species / Purpose |
|---|---|
| `download_data.sh` | master entry point for data download |
| `download_human.sh` + `full_ensembl_genomes_metadata.cvs` | human genome (Ensembl assembly metadata) |
| `download_and_process_athaliana_data.sh` | *Arabidopsis thaliana* |
| `download_and_process_fly_data.sh` + `fly.genomes.txt` | *Drosophila melanogaster* |
| `download_and_process_yeast_data.sh` + `ENA_PRJEB59413_assmebly_links.tsv` | *S. cerevisiae* (yeast) assemblies from ENA project PRJEB59413 |

**Held-out (test) regions** are defined by BED files and are excluded from all training corpora:

- `GCF_000001735_4.testholdout.bed` — human
- `D_MELANOGASTER.testholdout.bed` — fly
- `sacCer3.testholdout.bed` — yeast

**Supporting metadata:**

- `valid_species_stats.tsv` — statistics of species retained for the multi-species corpus.
- `2023-08-10 species_extended_metadata.csv` — extended per-species metadata (assembly, taxonomic info).
- `Suplementary_Table_1.csv`, `Suplementary_Table_2.csv` — supplementary tables from the paper.
- `HSE.task3.table_full.csv`, `HSE.task3.table_sample.csv` — sample/metadata tables used in the notebook exercises.
- `canonical_dataset.txt`, `genes.txt` — gene/sequence lists used for dataset construction.
- `1KG+HGDP.selected_samples.tsv` — 1000 Genomes + HGDP sample selection (allele-aware corpus).
- `human_epdnew_fH7d2.bed` — EPDnew human promoter annotations.
- `clinvar_significance_mapping.txt` — ClinVar clinical-significance code mapping.

---

## Pre-training Corpus Construction

| File | Purpose |
|---|---|
| `tokenize_genomes.py` | converts processed genomes into tokenizable text chunks, respecting hold-out BEDs |
| `create_corpus.py` | builds the single-species (human) pre-training corpus |
| `create_multigenome_corpus.sh` | orchestrates the **multi-species** corpus build (human + fly + yeast + *A. thaliana* + more) |
| `create_allele_corpus.py` | builds an **allele-aware** corpus from 1000 Genomes + HGDP haplotypes (human genetic diversity) |

---

## Pre-training

Pre-training is standard masked language modeling (BERT-style) using the HuggingFace `Trainer` with the provided architecture configs and the custom modeling code:

- `gena_lm/modeling_bert.py` — BERT with **pre-LayerNorm** blocks, optional **sparse attention** and **RoPE**, and the HF BigBird variant.
- `gena_lm/modeling_rmt.py` — **Recurrent Memory Transformer**: a fixed set of memory tokens is carried across sequence segments, so the model can be trained and applied to inputs much longer than the nominal attention window.

Typical workflow:

```bash
# 1. Download and preprocess genomes (per species)
bash genome_downloading/download_human.sh
bash genome_downloading/download_and_process_fly_data.sh
...

# 2. Build the corpus
bash corpus/create_multigenome_corpus.sh

# 3. Launch masked-language-model pre-training with a chosen config
#    (distributed training, e.g. torchrun / accelerate)
torchrun ... run_mlm-style script \
    --model_config configs/L12-H768-A12-V32k-preln.json \
    --tokenizer tokenizer/ \
    --corpus <path-to-tokenized-corpus> \
    --output_dir runs/gena-lm-base
```

For RMT pre-training, the base BERT checkpoint is used as the backbone and memory-augmented training proceeds with progressively longer segment counts (see `modeling_rmt.py` and the `*_rmt*` fine-tuning scripts for reference settings).

---

## Downstream Fine-tuning

All fine-tuning pipelines follow the same pattern:

1. a **dataset class** (`*Dataset.py`) that reads task-specific data and produces tokenized model inputs,
2. a **runner** (`run_*_finetuning*.py`) that builds the model + head, trains, and reports metrics,
3. one or more **shell scripts** (`finetune_*.sh`) with ready-made hyperparameter settings — edit paths/model names inside and run `bash <script>.sh`.

The `--model_path` / checkpoint argument accepts either a HuggingFace Hub id (e.g. `AIRI/GENA-LM-BERT-base`) or a path to a local checkpoint (including RMT checkpoints).

### 1. Promoter detection

Binary classification of **human promoters (hg38)** versus matched non-promoter sequences at several sequence lengths — allowing direct comparison of models at different context sizes, including RMT for very long inputs.

- Datasets: `hg38_promoters_len_300_dataset.csv`, `hg38_len_300.fa.txt`, `hg38_len_2000.fa.txt` (lengths **300 bp**, **2,000 bp**, **16,000 bp**); `dataset_generator.py`, `dataset.py`.
- Runners: `run_promoter_finetuning.py`, `run_promoter_finetuning_rmt.py`.
- Scripts: `finetune_promoter.sh`, `finetune_promoter_large.sh`, `finetune_promoter_2000*.sh`, `finetune_promoter_16000*.sh`, and `*_nar_*` variants (an additional promoter dataset), plus `*_rmt_pretrained.sh` variants (initialize from GENA-LM RMT weights).

```bash
cd promoter
bash finetune_promoter_2000_nar_large_rmt.sh
```

### 2. DeepSEA — chromatin activity prediction

Predict **919 chromatin profiles** (TF binding, DNase I hypersensitivity, histone marks) from 1,000 bp human sequences.

- Files: `DeepSeaDataset.py`, `test_DeepSeaDataset.py`, `run_deepsea_finetuning.py`, `prepare_dataset.py`, `extend_dataset.py`, sample data `test.dataset.csv.gz`.
- Script: `finetune_deepsea.sh`.

### 3. SpliceAI — splice site prediction

Predict splice donor/acceptor (and related) annotations around splice junctions.

- Files: `SpliceAIDataset.py`, `test_SpliceAIDataset.py`, `run_spliceai_finetuning.py`, `run_spliceai_finetuning_rmt.py`, `split_train_valid.py`, sample data `test_Dataset_data.csv`.
- Scripts: `finetune_spliceai.sh` (base), `finetune_spliceai_large.sh`, `finetune_spliceai_sparse_4096.sh` (4,096-token sparse model), `finetune_spliceai_rmt.sh` / `finetune_spliceai_rmt_pretrained.sh` (RMT variants).

### 4. APARENT — polyadenylation prediction

Regression of **polyadenylation signal strength** from short 3′-UTR/ poly(A) signal sequences (APARENT task).

- Files: `AparentDataset.py`, `test_AparentDataset.py`, `run_APARENT_finetuning.py`, sample data `AparentDataset_test_data.csv`.
- Script: `run_aparent_finetuning.sh`.
- Also includes `model_and_not_used_loss_class.py` (auxiliary/alternative loss implementations kept for reference).

### 5. Enformer / Basenji — gene expression prediction

Fine-tune GENA-LM (including RMT and sparse-attention variants) on the **Basenji/Enformer** human & mouse gene-expression tracks from very long sequences (~200 kb).

- Data: `convert_basenji_dataset.py` converts the original TFRecord dataset; `enformer_dataset.py` loads it.
- Model: `enformer_model.py` adds the multi-track expression head on top of the GENA-LM backbone.
- Training: `run_enformer_finetuning.py`, `run_enformer_finetuning_rmt.py`.
- Evaluation: `run_enformer_evaluation.py`, `run_enformer_evaluation_augs.py` (shift/augmentation-averaged evaluation), `enformer_metrics.py` (Pearson R² etc.).
- Scripts: `finetune_enformer.sh`, `finetune_enformer_large.sh`, `finetune_enformer_rmt.sh`, `finetune_enformer_sparse_hf.sh`, `finetune_enformer_sparse_hf_rmt.sh`, `*_continue.sh` (resume), and matching `evaluate_*.sh` scripts.

See also the usage tutorial: `gena_enformer_usage.ipynb`.

### 6. DeepSTARR — enhancer activity prediction

Regression of **Drosophila enhancer activity** (developmental & housekeeping enhancers, 249 bp sequences).

- Files: `DeepSTARRDataset.py`, `test_DeepSTARRDataset.py`, `run_deepstarr_finetuning.py`, `dataset_fold_split.py`, sample data `test_Sequences.fa` + `test_Sequences_activity.txt`.
- Script: `finetune_deepstarr.sh`.

---

## Notebooks & Tutorials

| Notebook | Content |
|---|---|
| `GENA_sequence_classification_example.ipynb` | End-to-end example: tokenize DNA, fine-tune GENA-LM for sequence classification |
| `gena_enformer_usage.ipynb` | Using GENA-LM with the Enformer-style expression-prediction setup |
| `gena_clusterization_example.ipynb` | Clustering genomic sequences from GENA-LM embeddings (UMAP/ k-means) |
| `public_gena_clusters.ipynb` | Full public clustering analysis pipeline |
| `public_gena_clusters_task.ipynb` | Task version of the clustering notebook (exercises) |
| `splice_check.ipynb` | Sanity checks of splice-site data/annotations |
| `make_exons_bed.ipynb` | Builds exon BED files used by the ClinVar analyses |
| `clinvar.ipynb` | ClinVar variant analysis with GENA-LM |
| `clinvar_promoter_prediction.ipynb` | Prediction of pathogenic variants in human promoters |
| `clinvar_attribution_prediction.ipynb` | Attribution/saliency analysis for ClinVar promoter variants |

---

## ClinVar Analyses

The ClinVar workflow (`clinvar/` + notebooks) evaluates GENA-LM on real human genetic variation:

1. Collect promoter regions (`human_epdnew_fH7d2.bed`) and exon coordinates (`make_exons_bed.ipynb`).
2. Map ClinVar variants (`clinvar_significance_mapping.txt`) onto promoter sequences.
3. Score pathogenic vs. benign variants with GENA-LM (`clinvar_promoter_prediction.ipynb`).
4. Inspect nucleotide-level attributions of the predictions (`clinvar_attribution_prediction.ipynb`).

---

## Requirements

Core stack (see `requirements.txt` for exact versions):

```
torch
transformers
tokenizers
numpy
pandas
h5py
scikit-learn
matplotlib
jupyter
```

Fine-tuning runs were designed for multi-GPU nodes; the provided `finetune_*.sh` scripts contain reference batch sizes, learning rates, and precision settings.

---

## License

This repository is released under the [Apache 2.0 License](./LICENSE).

---

## Citation

If you use GENA-LM in your research, please cite the paper:

```bibtex
@article{GENA-LM,
  title   = {GENA-LM: A Family of Open-Source Foundational DNA Language Models
             for Long Sequences Modeling},
  author  = {GENA-LM team},
  journal = {bioRxiv},
  year    = {2023},
  note    = {Preprint — see the project page for the full author list and DOI}
}
```

Also consider citing the upstream resources used by the tasks: DeepSEA, SpliceAI, APARENT, Enformer/Basenji, and DeepSTARR.

---

## Acknowledgments

- Built on [HuggingFace Transformers](https://github.com/huggingface/transformers) and the [Recurrent Memory Transformer](https://github.com/booydar/recurrent-memory-transformer).
- Genome data from Ensembl, NCBI RefSeq, ENA, 1000 Genomes, HGDP, EPDnew, ClinVar.
- Baseline datasets: DeepSEA, SpliceAI, APARENT, Enformer/Basenji, DeepSTARR.
