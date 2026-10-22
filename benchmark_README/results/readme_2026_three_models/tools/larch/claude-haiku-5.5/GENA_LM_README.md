# GENA-LM

GENA-LM is a family of transformer-based DNA language models for long genomic sequences. This repository contains the code and resources for data preparation, tokenization, model architectures, pretraining configurations, and fine-tuning and evaluation on downstream genomics tasks. Those tasks include chromatin profile prediction, splice site detection, polyadenylation site strength, enhancer activity, promoter recognition, gene expression prediction from sequence, and clinical variant interpretation.

> **Note:** This README was written from the file listing alone. Directory boundaries in the listing were not explicit, so the structure below is inferred from file names. Check paths against the actual repository before running commands, and see the original paper and the project's own documentation for authoritative details.

---

## Table of Contents

1. [Overview](#overview)
2. [Repository Structure](#repository-structure)
3. [Installation](#installation)
4. [Data Preparation](#data-preparation)
5. [Tokenization](#tokenization)
6. [Model Architectures and Configurations](#model-architectures-and-configurations)
7. [Pretraining](#pretraining)
8. [Downstream Tasks and Fine-tuning](#downstream-tasks-and-fine-tuning)
9. [Evaluation](#evaluation)
10. [Notebooks and Analyses](#notebooks-and-analyses)
11. [Testing](#testing)
12. [Pretrained Models](#pretrained-models)
13. [Citation](#citation)
14. [License](#license)

---

## Overview

GENA-LM adapts the BERT architecture to DNA sequences, using a byte-pair encoding (BPE) tokenizer trained on genomic data. Several extensions allow it to handle sequences longer than the standard 512-token limit:

- **Sparse attention** (BigBird-style) for long-range context with sub-quadratic cost.
- **Recurrent Memory Transformer (RMT)** for processing sequences in segments while passing memory states between them.
- **Pre-LN and last-LN variants** of the architecture for training stability.

The pretrained models are fine-tuned on a range of regulatory genomics benchmarks. The repository provides scripts for each stage of this pipeline.

---

## Repository Structure

The layout below is inferred from file names and may not match the directory tree exactly.

```
GENA_LM/
├── setup.cfg, pyproject.toml, requirements.txt   # Packaging and dependencies
├── LICENSE
├── README.md
│
├── data download and corpus creation/
│   ├── download_human.sh
│   ├── download_and_process_fly_data.sh
│   ├── download_and_process_yeast_data.sh
│   ├── download_and_process_athaliana_data.sh
│   ├── download_data.sh
│   ├── create_corpus.py
│   ├── create_multigenome_corpus.sh
│   ├── create_allele_corpus.py
│   ├── full_ensembl_genomes_metadata.cvs
│   ├── fly.genomes.txt, ENA_PRJEB59413_assmebly_links.tsv
│   ├── valid_species_stats.tsv                    # Per-species statistics
│   └── *.testholdout.bed                          # Held-out test regions per genome
│
├── tokenizers/
│   ├── tokenize_genomes.py
│   ├── BPE.json, BPE_no_n_all_chr.json            # Trained BPE tokenizers
│   └── tokenizer.json, tokenizer_config.json, special_tokens_map.json
│
├── model configs/                                 # JSON architecture configs (see below)
│
├── modeling/
│   ├── modeling_bert.py                           # BERT variant for GENA-LM
│   └── modeling_rmt.py                            # Recurrent Memory Transformer wrapper
│
├── downstream tasks/
│   ├── deepsea/        # Chromatin profile prediction
│   ├── spliceai/       # Splice site prediction
│   ├── aparent/        # Alternative polyadenylation (APARENT)
│   ├── enformer/       # Gene expression from sequence (Enformer-style)
│   ├── deepstarr/      # Drosophila enhancer activity
│   └── promoter/       # Promoter prediction
│
├── notebooks/                                     # Analyses and examples (.ipynb)
│
└── tests/                                         # Unit tests for dataset classes
```

---

## Installation

### Requirements

- Python 3.8 or later (check `setup.cfg` / `pyproject.toml` for the exact range)
- PyTorch with CUDA support, recommended for training
- Hugging Face `transformers` and `tokenizers`
- A GPU with sufficient memory for the chosen model size and sequence length. Long-sequence and RMT configurations need considerably more memory.

### Steps

```bash
git clone <repository-url> GENA_LM
cd GENA_LM

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
# or, for an editable install:
pip install -e .
```

---

## Data Preparation

Genome data is downloaded and processed with shell scripts, one per organism or source:

| Script | Purpose |
|---|---|
| `download_human.sh` | Downloads human genome assemblies |
| `download_and_process_fly_data.sh` | *Drosophila melanogaster* genome and annotations |
| `download_and_process_yeast_data.sh` | *Saccharomyces cerevisiae* (sacCer3) data |
| `download_and_process_athaliana_data.sh` | *Arabidopsis thaliana* data |
| `download_data.sh` | General download helper |

Other data-related files:

- **`full_ensembl_genomes_metadata.cvs`** (sic, as named in the repo) and **`species_extended_metadata.csv`**: metadata for Ensembl genomes and species.
- **`valid_species_stats.tsv`** (one per organism directory): statistics for validation species.
- **`*.testholdout.bed`**: BED files defining held-out test regions for the human (GCF_000001735, *A. thaliana*), fly (D_MELANOGASTER), and yeast (sacCer3) assemblies. Use them so evaluation does not overlap with pretraining data.

### Corpus creation

- `create_corpus.py` builds a pretraining corpus from processed genome sequences.
- `create_multigenome_corpus.sh` builds a corpus spanning several species.
- `create_allele_corpus.py` builds a corpus of sequences with alleles, using population data such as `1KG+HGDP.selected_samples.tsv` (1000 Genomes and HGDP).

Typical workflow:

```bash
bash download_human.sh
python create_corpus.py --help          # check available arguments
bash create_multigenome_corpus.sh
```

Verify the arguments in each script before running it.

---

## Tokenization

GENA-LM uses a byte-pair encoding (BPE) tokenizer trained on DNA. Two trained variants are included:

- **`BPE.json`**: the standard tokenizer.
- **`BPE_no_n_all_chr.json`**: a variant that excludes `N` (unknown) nucleotides when training the vocabulary, and was trained on all chromosomes.

Each tokenizer directory includes `tokenizer.json`, `tokenizer_config.json`, and `special_tokens_map.json`, so it loads directly with Hugging Face:

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("path/to/tokenizer_dir")
enc = tokenizer("ACGTNACGTTGCA")
print(enc["input_ids"])
```

To tokenize a corpus or set of genomes, use `tokenize_genomes.py`:

```bash
python tokenize_genomes.py --help
```

The vocabulary size is 32k (`V32k` in the config names).

---

## Model Architectures and Configurations

Architectures are specified as JSON configuration files. The naming scheme encodes the main hyperparameters:

- `L`: number of layers
- `H`: hidden size
- `A`: number of attention heads
- `V`: vocabulary size
- `L4096`: maximum sequence length (in tokens)
- `preln` / `lastln`: layer-normalization placement
- `sparse`: sparse (BigBird-style) attention
- `rope`: rotary position embeddings
- `ln1e-05`: layer-norm epsilon

| Config file | Description |
|---|---|
| `L12-H768-A12-V32k-preln.json` | Base model (~110M parameters), pre-LN |
| `L12-H768-A12-V32k-preln-lastln.json` | Base model with last-LN placement |
| `L12-H768-A12-V32k-L4096-preln-sparse-rope.json` | Base model with 4096-token context, sparse attention, and RoPE |
| `L12-H768-A12-V32k-L4096-preln-lastln-sparse-ln1e-05.json` | 4096-token sparse variant with last-LN and LN epsilon 1e-5 |
| `L24-H1024-A16-V32k-preln-lastln.json` | Large model (~340M parameters) |
| `hf_bigbird_L12-H768-A12-V32k-L4096.json` | BigBird-style reference configuration for Hugging Face |

Parameter counts are approximate and follow standard BERT scaling.

### Model code

- **`modeling_bert.py`**: the BERT implementation with GENA-LM modifications, including the layer-norm options and sparse attention support.
- **`modeling_rmt.py`**: a wrapper implementing the Recurrent Memory Transformer. It splits long inputs into segments, carries memory tokens between them, and enables sequences longer than the model's native context.

---

## Pretraining

Pretraining uses masked language modeling over the tokenized corpus. The configuration JSON defines the architecture, and the training data comes from the corpus created in the previous step.

Typical steps:

1. Download and process genomes (see [Data Preparation](#data-preparation)).
2. Build the corpus.
3. Tokenize it.
4. Launch pretraining with the desired config.

Pretraining launch scripts and hyperparameters should be checked in the repository. Use the held-out BED files to exclude test regions from training.

---

## Downstream Tasks and Fine-tuning

Each downstream task has its own directory with a dataset class, a training script, and shell launchers for the configurations used in the experiments. The test-data files and dataset tests are included where applicable.

### DeepSEA (chromatin profile prediction)

- Files: `DeepSeaDataset.py`, `prepare_dataset.py`, `run_deepsea_finetuning.py`, `finetune_deepsea.sh`, `test.dataset.csv.gz`
- Task: multi-label prediction of chromatin features (e.g., TF binding and histone marks) from sequence.

### SpliceAI (splice site prediction)

- Files: `SpliceAIDataset.py`, `split_train_valid.py`, `run_spliceai_finetuning.py`, `run_spliceai_finetuning_rmt.py`, `make_exons_bed.ipynb`, and launch scripts for standard, large, sparse 4096-token, RMT, and RMT-pretrained variants.
- Task: classifying donor, acceptor, and non-splice positions.

### APARENT (alternative polyadenylation)

- Files: `AparentDataset.py`, `run_APARENT_finetuning.py`, `run_aparent_finetuning.sh`, `model_and_not_used_loss_class.py`
- Task: predicting polyadenylation site usage and strength.

### Enformer (gene expression)

- Files: `enformer_model.py`, `enformer_dataset.py`, `run_enformer_finetuning.py`, `run_enformer_finetuning_rmt.py`, `enformer_metrics.py`, `convert_basenji_dataset.py`, and many launch scripts for standard, large, sparse, and RMT variants, plus evaluation scripts including augmentation-based evaluation (`run_enformer_evaluation_augs.py`).
- Task: predicting gene expression tracks from long genomic sequences.
- See `README.md` in the enformer directory for dataset conversion details.

### DeepSTARR (enhancer activity)

- Files: `DeepSTARRDataset.py`, `run_deepstarr_finetuning.py`, `finetune_deepstarr.sh`, `test_Sequences.fa`, `test_Sequences_activity.txt`
- Task: regressing enhancer activity in *Drosophila* S2 cells.

### Promoter prediction

- Files: `dataset.py`, `dataset_generator.py`, `dataset_fold_split.py`, `run_promoter_finetuning.py`, `run_promoter_finetuning_rmt.py`, `hg38_promoters_len_300_dataset.csv`, and many launch scripts for lengths 300, 2000, and 16000 with standard, NAR, and RMT variants.
- Task: promoter sequence classification at several input lengths.

### Example workflow

```bash
cd <task_directory>
bash finetune_<task>.sh
```

Each launch script sets the model config, data paths, and hyperparameters. Edit them to match your environment.

---

## Evaluation

Evaluation scripts are provided for the tasks that need them:

- `evaluate_enformer.sh`, `evaluate_enformer_rmt_sparse.sh`, `evaluate_enformer_augs.sh`: Enformer evaluation, including augmentation-based and RMT/sparse variants.
- `run_enformer_evaluation.py`, `run_enformer_evaluation_augs.py`: evaluation entry points.
- `enformer_metrics.py`: metric implementations for the Enformer task.

Downstream tasks report standard metrics (for example, AUROC and AUPRC for classification, Pearson correlation for regression). Check each task's script or README for the metrics it computes.

---

## Notebooks and Analyses

The `.ipynb` notebooks cover examples and analyses:

| Notebook | Topic |
|---|---|
| `GENA_sequence_classification_example.ipynb` | Sequence classification with GENA-LM |
| `gena_enformer_usage.ipynb` | Using the Enformer-based model |
| `gena_clusterization_example.ipynb` | Clustering sequence embeddings |
| `public_gena_clusters.ipynb`, `public_gena_clusters_task.ipynb` | Clustering analysis and task setup |
| `clinvar.ipynb`, `clinvar_promoter_prediction.ipynb`, `clinvar_attribution_prediction.ipynb` | Clinical variant (ClinVar) analyses |
| `splice_check.ipynb` | Splice site checks |
| `make_exons_bed.ipynb` | Generating exon BED files |

Supporting data includes `clinvar_significance_mapping.txt`, `human_epdnew_fH7d2.bed` (EPD promoter annotations), `Suplementary_Table_1.csv`, `Suplementary_Table_2.csv`, and `HSE.task3.table_*.csv` (task 3 tables).

---

## Testing

Unit tests cover dataset classes:

- `test_DeepSeaDataset.py`
- `test_SpliceAIDataset.py`
- `test_AparentDataset.py`
- `test_DeepSTARRDataset.py`

Run them from the repository root:

```bash
pytest
```

Test fixtures are included, such as `test_Dataset_data.csv`, `AparentDataset_test_data.csv`, and `test.dataset.csv.gz`.

---

## Pretrained Models

Pretrained GENA-LM checkpoints are distributed through the Hugging Face Hub under the `AIRI-Institute` organization. Model names have included `gena-lm-bert-base-t2t` (T2T-CHM13 human genome), `gena-lm-bert-base-t2t-multi` (multi-species), and `gena-lm-bert-large-t2t`. Confirm current model names on the Hub before use.

```python
from transformers import AutoTokenizer, AutoModelForMaskedLM

name = "AIRI-Institute/gena-lm-bert-base-t2t"
tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModelForMaskedLM.from_pretrained(name, trust_remote_code=True)
```

`trust_remote_code=True` may be required because the model uses custom code from this repository.

---

## Citation

If you use GENA-LM, please cite the paper:

```bibtex
@article{fishman2023gena,
  title   = {GENA-LM: A Family of Open-Source Foundational DNA Language Models for Long Sequences},
  author  = {Fishman, Veniamin and Kuratov, Yuri and Shmelev, Aleksei and Petrov, Maxim and Penzar, Dmitry and Shepelin, Denis and Chekanov, Nikolay and Kuratov, Yuri and Oreshkin, Ivan and others},
  journal = {bioRxiv},
  year    = {2023},
  doi     = {10.1101/2023.06.12.544594}
}
```

Please verify the author list and publication details against the published version.

---

## License

The license is in the `LICENSE` file at the repository root. Check it before using the code or models in your own work.

---

## Acknowledgements

GENA-LM was developed by researchers at AIRI (Artificial Intelligence Research Institute), with collaborators at the London Institute for Mathematical Sciences, Moscow Institute of Physics and Technology, and others. Benchmark tasks build on published datasets, including DeepSEA, SpliceAI, APARENT, Enformer/Basenji, DeepSTARR, and ClinVar. Refer to the original publications for credit to those sources.
