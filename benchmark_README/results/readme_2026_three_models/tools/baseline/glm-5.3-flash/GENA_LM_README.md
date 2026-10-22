# GENA-LM: DNA Language Model

GENA-LM is a family of foundation language models for DNA sequences, trained on large-scale genomic data from multiple species. The models are based on BERT-style transformer architectures with masked language modeling objectives and support various attention mechanisms including standard full attention and sparse attention (BigBird-style). The package includes model implementations, tokenizers, data processing pipelines for multi-species genome corpora, and fine-tuning scripts for a range of downstream genomics tasks.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Data Preparation](#data-preparation)
  - [Single-Species Data](#single-species-data)
  - [Multi-Species Corpus](#multi-species-corpus)
  - [Variation Corpus](#variation-corpus)
  - [Model Configurations](#model-configurations)
- [Downstream Tasks](#downstream-tasks)
  - [DeepSTARR](#deepstarr)
  - [DeepSea](#deepsea)
  - [SpliceAI](#spliceai)
  - [Enformer](#enformer)
  - [APARENT](#aparent)
  - [Promoter Prediction](#promoter-prediction)
  - [ClinVar Analysis](#clinvar-analysis)
- [Notebooks](#notebooks)
- [Development](#development)
- [Testing](#testing)
- [License](#license)

## Overview

GENA-LM trains masked language models on DNA sequences using a BPE tokenizer with a 32k vocabulary. The models are evaluated on multiple benchmark tasks:

- **Splice site prediction** (SpliceAI-style)
- **Chromatin profile prediction** (DeepSea-style, 919 binary targets)
- **Enhancer activity prediction** (DeepSTARR-style)
- **Gene expression prediction** (Enformer-style, CAGE signal)
- **Promoter prediction** (EPDNew-based)
- **Polyadenylation prediction** (APARENT-style)

The core model architecture is implemented in `src/gena_lm/modeling_bert.py` (standard BERT with custom pre-layer norm and rotary embedding options) and `src/gena_lm/modeling_rmt.py` (Recurrent Memory Transformer variant for longer contexts).

## Repository Structure

```
├── data/                       # Data download, processing, model configs, tokenizers
│   ├── athaliana/              # Arabidopsis thaliana data pipeline
│   ├── fly/                    # Drosophila (298 species) data pipeline
│   ├── yeasts/                 # Yeast data pipeline
│   ├── configs/                # Model architecture JSON configs
│   ├── tokenizers/             # Pre-trained BPE tokenizers (human, multi-species)
│   ├── download_data.sh        # Generic genome download script
│   └── download_human.sh       # Human reference download script
├── downstream_tasks/           # Fine-tuning pipelines for benchmark tasks
│   ├── APARENT/
│   ├── DeepSTARR/
│   ├── DeepSea/
│   ├── SpliceAI/
│   ├── clinvar_analysis/
│   ├── enformer/
│   ├── promoter_prediction/
│   └── splicing_onemut/
├── notebooks/                  # Example usage notebooks
├── manuscript_data/            # Supplementary tables
├── src/gena_lm/                # Core package source
│   ├── modeling_bert.py        # BERT model with custom features
│   ├── modeling_rmt.py         # Recurrent Memory Transformer
│   ├── tokenizers/             # Genome tokenization utilities
│   ├── genome_tools/           # Corpus generation tools
│   └── utils.py
├── pyproject.toml
├── requirements.txt
├── setup.cfg
└── LICENSE
```

## Installation

### Prerequisites

- Python >= 3.6
- [PyTorch](https://pytorch.org/) (>=1.7.1, <=1.9.1)
- [bedtools](https://anaconda.org/bioconda/bedtools) >2.30
- [samtools](https://anaconda.org/bioconda/samtools)
- [NCBI datasets CLI](https://www.ncbi.nlm.nih.gov/datasets/) (for data download scripts)

### Install from source

```bash
pip install -e .
```

This installs the `gena-lm` package (version 0.0.1) with the following dependencies:

```
numpy
cyvcf2
tokenizers
tqdm
torch >=1.7.1, <=1.9.1
transformers==4.17.0
pysam>=0.19.1
biopython>=1.79
pandas>=1.5.0,<2.0.0
pybedtools==0.10.0
pybigwig==0.3.22
```

## Data Preparation

### Single-Species Data

The repository provides download and processing pipelines for three species groups. Each pipeline downloads genome assemblies, performs alignment (using [Progressive Cactus](https://github.com/ComparativeGenomicsToolkit/cactus)), generates test holdouts via liftover, and produces a multi-FASTA file for corpus generation.

#### Human

Download the human reference genome (GRCh38.p13):

```bash
bash data/download_human.sh
```

Or use the T2T-CHM13 v2.0 assembly:

```bash
bash data/download_data.sh human
```

#### Yeast

```bash
cd data/yeasts
bash download_and_process_yeast_data.sh
```

Generates `yeast_fasta_for_corpus_generation.fa.gz`. Then generate the corpus:

```bash
python3 src/gena_lm/genome_tools/create_corpus.py \
    --input-file data/yeasts/yeast_fasta_for_corpus_generation.fa.gz \
    --output-dir data/yeasts/yeast_corpus/ \
    --io-mode jsonl \
    --min-len 10000
```

Data size (without augmentations):
- Train: 1,345,434,353 nucleotides
- Test: 82,338,353 nucleotides

#### Fly (Drosophila)

```bash
cd data/fly
bash download_and_process_fly_data.sh
```

Uses a Progressive Cactus alignment of 298 drosophilid species. Generates `fly_fasta_for_corpus_generation.fa.gz`. Then generate the corpus with 2 augmentations:

```bash
python3 src/gena_lm/genome_tools/create_corpus.py \
    --input-file data/fly/fly_fasta_for_corpus_generation.fa.gz \
    --output-dir data/fly/fly_corpus/ \
    --io-mode jsonl \
    --min-len 10000 \
    --n_augmentations 2
```

Data size (without augmentations):
- Train: 38,208,813,984 nucleotides
- Test: 2,519,835,748 nucleotides

#### Arabidopsis thaliana

```bash
cd data/athaliana
bash download_and_process_athaliana_data.sh
```

Generates `athaliana_fasta_for_corpus_generation.fa.gz`. Then generate the corpus with 6 augmentations:

```bash
python3 src/gena_lm/genome_tools/create_corpus.py \
    --input-file data/athaliana/athaliana_fasta_for_corpus_generation.fa.gz \
    --output-dir data/athaliana/athaliana_corpus/ \
    --io-mode jsonl \
    --min-len 10000 \
    --n_augmentations 6
```

Data size (without augmentations):
- Train: 4,147,986,974 nucleotides
- Test: 346,219,192 nucleotides

### Multi-Species Corpus

To build a corpus from multiple genomes (e.g., all Ensembl Genomes):

1. Download FASTA files:
```shell
cut -f2 ensemble_genomes_metadata.tsv | xargs -L 1 wget -P fasta --no-clobber
```

2. Download and extract processed AGP information into `contigs/` folder.

3. Run the multi-genome corpus script:
```shell
bash create_multigenome_corpus.sh \
    /path/to/full_ensembl_genomes_metadata \
    /path/to/directory/with/fasta/ \
    /path/to/directory/with/contigs/ \
    /path/to/output/folder
```

### Variation Corpus

Create a corpus with genetic variants applied (from 1000 Genomes + HGDP via gnomAD):

1. Download the variant call set:
```shell
GOO=https://storage.googleapis.com/gcp-public-data--gnomad/
LINK=$GOO/release/3.1.2/vcf/genomes/gnomad.genomes.v3.1.2.hgdp_tgp.

mkdir 1KG+HGDP
for CHR in chr{1..22} chr{X,Y} ; do
    wget -P 1KG+HGDP -c $LINK.$CHR.vcf.{bgz,bgz.tbi}
done
```

2. Download and index the hg38 reference:
```shell
mkdir hg38
wget -P hg38 https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/analysisSet/hg38.analysisSet.fa.gz
gunzip hg38.analysisSet.fa.gz
samtools faidx hg38.analysisSet.fa
```

3. Apply variants to generate allele-specific sequences:
```shell
SAMPLES=$(cut -f1 1KG+HGDP.selected_samples.tsv | tr , \n)
mkdir variation_corpus
for CHR in chr{1..22} chr{X,Y} ; do
    python create_allele_corpus.py \
        --reference hg38/hg38.analysisSet.fa \
        --vcf 1KG+HGDP/gnomad.genomes.v3.1.2.hgdp_tgp.$CHR.vcf.bgz \
        --samples ${SAMPLES%?} \
        --output-dir variation_corpus
done
```

### Model Configurations

Pre-defined model architecture configurations are available in `data/configs/`:

| Config | Layers | Hidden | Heads | Max Positions | Features |
|--------|--------|--------|-------|---------------|----------|
| `L12-H768-A12-V32k-preln.json` | 12 | 768 | 12 | 512 | Pre-LN |
| `L12-H768-A12-V32k-preln-lastln.json` | 12 | 768 | 12 | 512 | Pre-LN + Last-LN |
| `L24-H1024-A16-V32k-preln-lastln.json` | 24 | 1024 | 16 | 512 | Pre-LN + Last-LN (large) |
| `L12-H768-A12-V32k-L4096-preln-lastln-sparse-ln1e-05.json` | 12 | 768 | 12 | 4096 | Pre-LN + Last-LN + BigBird sparse attention |
| `L12-H768-A12-V32k-L4096-preln-sparse-rope.json` | 12 | 768 | 12 | 4096 | Pre-LN + RoPE + BigBird sparse attention |
| `hf_bigbird_L12-H768-A12-V32k-L4096.json` | 12 | 768 | 12 | 4096 | HF BigBird (block-sparse) |

### Tokenizers

Pre-trained BPE tokenizers are included:

- `data/tokenizers/human/BPE_32k/` — BPE tokenizer (32k vocab) for human genome
- `data/tokenizers/human/BPE_32k_all_chr_10M/` — BPE tokenizer trained on all chromosomes with 10M base window
- `data/tokenizers/human/BPE_all_chr/` — BPE tokenizer for all chromosomes (no N)
- `data/tokenizers/t2t_1000h_multi_32k/` — Multi-species BPE tokenizer (32k vocab) trained on T2T + 1000 genomes + multi-species data

Tokenization of genomes can be performed with `src/gena_lm/tokenizers/tokenize_genomes.py`.

## Downstream Tasks

Each downstream task directory contains:
- A dataset class (PyTorch `Dataset`)
- A fine-tuning runner script (`run_*.py`)
- Shell scripts with example hyperparameters (`finetune_*.sh`)
- Test files for dataset validation

### DeepSTARR

Predicts Drosophila enhancer activity based on DNA sequence.

**Data:** Download from [Stark lab](https://data.starklab.org/almeida/DeepSTARR/Data/). Train/valid/test split: 402,296/40,570/41,186 samples. No preprocessing needed.

**Fine-tuning:**
```bash
CUDA_VISIBLE_DEVICES=0 NP=1 ./finetune_deepstarr.sh
```

### DeepSea

Predicts 919 chromatin profile targets (125 DNase sites, 690 transcription factors, 104 histone marks) from 1kb sequences.

**Data:** Download the [original DeepSea dataset](http://deepsea.princeton.edu/media/code/deepsea_train_bundle.v0.9.tar.gz), then convert from .mat to .csv.gz:
```bash
python prepare_dataset.py --train_path ./train.mat --valid_path ./valid.mat --test_path ./test.mat
```

Optionally extend context length:
```bash
python extend_dataset.py --path /path/to/folder/with/1kb/csv/files \
    --fasta /path/to/hg19.genome.fasta --seqlen required_output_seq_length
```
Note: `extend_dataset.py` requires [bwa](https://github.com/lh3/bwa) in PATH.

**Fine-tuning:** Each example is prefixed/appended with [CLS] and [SEP] tokens. The [CLS] output is fed to a linear layer with 919 heads. Loss is upweighted for positive examples (factor of 8) due to class imbalance.

```bash
CUDA_VISIBLE_DEVICES=0,1 NP=2 ./finetune_deepsea.sh
```

### SpliceAI

Predicts splice donor and acceptor sites based on DNA sequence.

**Data:** From the original Illumina SpliceAI dataset ([basespace project 66029966](https://basespace.illumina.com/projects/66029966/about)). Original train/test split (162,706/16,505) is preserved. 10% of the training set is used as validation:

```bash
python split_train_valid.py --data_path ./dataset_train_all.csv.gz --valid_ratio 0.1 --seed 42
```

Resulting split: train/valid/test = 146,436/16,270/16,505.

**Fine-tuning:**
```bash
CUDA_VISIBLE_DEVICES=0,1 NP=2 ./finetune_spliceai.sh
```

Multiple variant scripts are provided:
- `finetune_spliceai.sh` — base model
- `finetune_spliceai_large.sh` — large model
- `finetune_spliceai_rmt.sh` / `finetune_spliceai_rmt_pretrained.sh` — RMT variants
- `finetune_spliceai_sparse_4096.sh` — sparse attention with 4096 context

### Enformer

Predicts CAGE signal (gene expression) from DNA sequence. Input length: 196,608 bp (left context 40,960 + 896 bins × 128 bp + right context 40,960). Target: 896 × 5313 values.

**Data:** Based on the [Basenji dataset](https://console.cloud.google.com/storage/browser/basenji_barnyard/data). Convert TensorFlow records to HDF5 for GENA-LM (4kb input) or TFRecord for Enformer (393kb input):

```shell
BASENJI_BASE_DIR=/path/to/basenji
OUTPUT_BASE_DIR=/path/to/export
HUMAN_REFERENCE=/path/to/hg38.fa
MOUSE_REFERENCE=/path/to/mm39.fa

for SUBSET in train test valid ; do
  parallel -j 8 ./convert_basenji_dataset.py --base-path $BASENJI_BASE_DIR/human \
    --subset $SUBSET --genome $HUMAN_REFERENCE --tfr {} \
    --out-hdf5 $OUTPUT_BASE_DIR/human/gena-lm-4Kbp/{/.}.h5 \
    ::: $BASENJI_BASE_DIR/human/tfrecords/$SUBSET-*tfr
  # ... similarly for mouse and enformer 393Kbp format
done
```

**Fine-tuning:**
```bash
CUDA_VISIBLE_DEVICES=0,1 NP=2 ./finetune_enformer.sh
```

**Evaluation:**
```bash
./evaluate_enformer.sh
```

### APARENT

Predicts polyadenylation (alternative polyA site usage) from DNA sequence.

**Fine-tuning:**
```bash
CUDA_VISIBLE_DEVICES=0 NP=1 ./run_aparent_finetuning.sh
```

### Promoter Prediction

Binary classification of promoter vs. non-promoter sequences. Data sourced from [EPDNew](https://epd.expasy.org/epd/EPDnew_select.php) (human, hg38). Four sequence lengths are evaluated: 300 bp (-249 to +50), 2,000 bp (-1000 to +999), 8,000 bp (-5000 to +2999), and 16,000 bp (-8000 to +7999).

**Dataset preparation:**
```bash
python dataset_generator.py hg38_len_300.fa.txt      # generates positive/negative samples
python dataset_fold_split.py hg38_promoters_len_300_dataset.csv  # 5-fold cross-validation splits
```

**Fine-tuning:**
```bash
CUDA_VISIBLE_DEVICES=0 NP=1 ./finetune_promoter.sh
```

Multiple scripts for different sequence lengths and model variants (large, RMT, pretrained) are provided.

### ClinVar Analysis

Jupyter notebooks for analyzing ClinVar variants:
- `clinvar.ipynb` — general ClinVar variant analysis
- `clinvar_attribution_prediction.ipynb` — variant effect attribution and prediction
- `clinvar_promoter_prediction.ipynb` — ClinVar variants in promoter regions
- `make_exons_bed.ipynb` — exon BED file generation

## Notebooks

Example notebooks demonstrating GENA-LM usage:

- `GENA_sequence_classification_example.ipynb` — Sequence classification with GENA-LM
- `gena_enformer_usage.ipynb` — Using GENA-LM for gene expression prediction
- `gena_clusterization_example.ipynb` — Sequence clustering
- `public_gena_clusters.ipynb` / `public_gena_clusters_task.ipynb` — Working with public GENA clusters

## Development

### Package Structure

The package is installed from `src/` using setuptools:

```
src/gena_lm/
├── __init__.py
├── modeling_bert.py          # BERT model with pre-LN, rotary embeddings, custom layer norm
├── modeling_rmt.py           # Recurrent Memory Transformer implementation
├── utils.py                  # Utility functions
├── tokenizers/
│   ├── __init__.py
│   └── tokenize_genomes.py   # Tokenize genome FASTA files
└── genome_tools/
    ├── __init__.py
    ├── create_corpus.py       # Create training corpus from FASTA
    ├── create_allele_corpus.py # Create corpus with variants applied
    └── create_multigenome_corpus.sh # Multi-species corpus generation
```

### Code Style

Type checking is configured with mypy (missing imports ignored):

```toml
[tool.mypy]
ignore_missing_imports = true
```

## Testing

Each downstream task module includes test files for dataset loading:

- `downstream_tasks/DeepSTARR/test_DeepSTARRDataset.py`
- `downstream_tasks/DeepSea/test_DeepSeaDataset.py`
- `downstream_tasks/SpliceAI/test_SpliceAIDataset.py`
- `downstream_tasks/APARENT/test_AparentDataset.py`

Run tests from the repository root:

```bash
python -m pytest downstream_tasks/
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

Copyright (c) 2022 AIRI - Artificial Intelligence Research Institute
