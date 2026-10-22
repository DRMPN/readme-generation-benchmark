# GENA-LM

GENA-LM is a DNA language model project from AIRI (Artificial Intelligence Research Institute). The repository contains the `gena_lm` Python package, model configuration files, tokenizers, data preparation scripts for several genomes, downstream task pipelines, and example notebooks. The package metadata describes it as a "DNA language model."

## Overview

The repository includes:

- **Python package (`src/gena_lm`)**: BERT-based modeling code (`modeling_bert.py`), recurrent memory transformer code (`modeling_rmt.py`), tokenization utilities (`tokenizers/tokenize_genomes.py`), general utilities (`utils.py`), and genome corpus tools (`genome_tools/`).
- **Model and tokenizer configurations (`data/configs/`)**: JSON configs for BERT-style models with 12 or 24 layers, sequence lengths of 512 or 4096, sparse attention, and rotary or absolute position embeddings. A BigBird configuration is also included.
- **Tokenizers (`data/tokenizers/`)**: Pretrained tokenizer files for human and T2T genomes, including BPE variants with a 32k vocabulary.
- **Genome data pipelines (`data/`)**: Scripts and documentation for preparing *Arabidopsis thaliana*, *Drosophila* (fly), and yeast datasets, including holdout sets.
- **Downstream tasks (`downstream_tasks/`)**: Fine-tuning pipelines and dataset classes for APARENT, DeepSTARR, DeepSEA, SpliceAI, Enformer, and promoter prediction, plus ClinVar analysis notebooks.
- **Notebooks (`notebooks/`)**: Examples for sequence classification, embedding clusterization, and Enformer-based usage.
- **Manuscript data (`manuscript_data/`)**: Supplementary tables.

## Repository Structure

```
src/gena_lm/            Python package (setuptools, src layout)
  genome_tools/         Corpus creation from genomes and variants
  tokenizers/           Genome tokenization
data/                   Configs, tokenizers, and species data pipelines
  configs/              Model architecture JSON files
  tokenizers/           Pretrained tokenizer files
  athaliana/, fly/, yeasts/
downstream_tasks/       Fine-tuning pipelines by task
notebooks/              Usage examples
manuscript_data/        Supplementary tables
```

## Setup

### Python dependencies

The package declares its dependencies in `requirements.txt`:

- numpy
- cyvcf2
- tokenizers
- tqdm
- torch (constrained to `>=1.7.1,<=1.9.1` in the file)
- transformers==4.17.0
- pysam>=0.19.1
- biopython>=1.79
- pandas>=1.5.0,<2.0.0
- pybedtools==0.10.0
- pybigwig==0.3.22

Install them with:

```bash
pip install -r requirements.txt
```

The `torch` constraint is written with quotation marks in `requirements.txt`, so check that line if installation fails.

### Packaging

`setup.cfg` defines the package `gena-lm` (version 0.0.1) with packages discovered under `src/`. It requires Python `>=3.6`. The build system is setuptools, as declared in `pyproject.toml`. The supplied files do not include a dedicated installation command beyond these declarations.

### External tools for data preparation

Data pipelines require the following command-line tools, as listed in the data READMEs:

- [bedtools](https://anaconda.org/bioconda/bedtools) (>2.30)
- [samtools](https://anaconda.org/bioconda/samtools)
- [NCBI datasets](https://www.ncbi.nlm.nih.gov/datasets/) (for *A. thaliana*)
- Docker, for the Cactus container (`quay.io/comparative-genomics-toolkit/cactus:v2.7.0`) used by the *A. thaliana* and fly pipelines
- [bwa](https://github.com/lh3/bwa), only for the optional DeepSEA context extension

## Data Preparation

Each species directory contains a `ReadMe.md` and a download script. Run the scripts from their own directories.

### *Arabidopsis thaliana*

```bash
cd data/athaliana
bash download_and_process_athaliana_data.sh
```

This creates `athaliana_fasta_for_corpus_generation.fa.gz`. The data is sourced from the study at https://doi.org/10.1038/s41467-023-42029-4 and uses a Cactus pangenome alignment. Reported nucleotide counts without augmentation are:

- train: 4,147,986,974
- test: 346,219,192

### Fly (*Drosophila*)

```bash
cd data/fly
bash download_and_process_fly_data.sh
```

This processes a Progressive Cactus alignment of 298 drosophilid species, and creates `fly_fasta_for_corpus_generation.fa.gz`. Reported counts without augmentation:

- train: 38,208,813,984
- test: 2,519,835,748

### Yeast

```bash
cd data/yeasts
bash download_and_process_yeast_data.sh
```

This creates `yeast_fasta_for_corpus_generation.fa.gz`. Reported counts without augmentation:

- train: 1,345,434,353
- test: 82,338,353

### Human and other genomes

`data/download_data.sh` takes a genome name (`human`, `mouse`, `ape`, `yeast`, or `fly`). It uses NCBI datasets to download the human genome, accession `GCA_009914755.4` (T2T-CHM13 v2.0). For the other names, the script prints "genome not supported." `data/download_human.sh` contains a curl command for the GRCh38.p13 RefSeq FASTA, with decompression commented out.

Holdout test regions for each species are stored in `*/[species]_holdouts/`.

## Usage

### Creating a pretraining corpus

`src/gena_lm/genome_tools/create_corpus.py` converts a FASTA file into a corpus. The READMEs show these examples:

```bash
python3 src/gena_lm/genome_tools/create_corpus.py \
    --input-file data/athaliana/athaliana_fasta_for_corpus_generation.fa.gz \
    --output-dir data/athaliana/athaliana_corpus/ \
    --io-mode jsonl --min-len 10000 --n_augmentations 6
```

For fly data, the README used `--n_augmentations 2`. For yeast, the example omits augmentation.

### Multi-species corpus

`src/gena_lm/genome_tools/create_multigenome_corpus.sh` builds a corpus from multiple Ensembl genomes. It takes four arguments: the metadata file, the FASTA directory, the contigs directory, and the output folder. The metadata file `full_ensembl_genomes_metadata.cvs` is included under `data/` and `src/gena_lm/genome_tools/` (the filename is spelled this way in the repository).

### Variation corpus

`create_allele_corpus.py` applies gnomAD 1000 Genomes + HGDP variants to an hg38 reference, selecting samples listed in `1KG+HGDP.selected_samples.tsv`. Its README documents the full download and processing steps.

### Tokenizing genomes

`src/gena_lm/tokenizers/tokenize_genomes.py` is included in the package. Pretrained tokenizers are available in `data/tokenizers/`:

- `human/BPE`, `human/BPE_32k`, `human/BPE_32k_all_chr_10M`, `human/BPE_all_chr`
- `t2t_1000h_multi_32k`

### Downstream fine-tuning

Each task directory has a README and example shell scripts. Dataset paths and hyperparameters are set inside the example scripts before running.

- **DeepSTARR** (Drosophila enhancer activity): `CUDA_VISIBLE_DEVICES=0 NP=1 ./finetune_deepstarr.sh`
- **DeepSEA** (chromatin profiles, 919 binary targets): `CUDA_VISIBLE_DEVICES=0,1 NP=2 ./finetune_deepsea.sh`
- **SpliceAI** (splice donor and acceptor sites): `CUDA_VISIBLE_DEVICES=0,1 NP=2 ./finetune_spliceai.sh`

Other task directories include:

- **APARENT**: `run_APARENT_finetuning.py` and `run_aparent_finetuning.sh`
- **Enformer** (CAGE signal prediction): several `finetune_enformer*.sh` and `evaluate_enformer*.sh` scripts, plus `convert_basenji_dataset.py`
- **Promoter prediction**: `dataset_generator.py`, `dataset_fold_split.py`, and multiple `finetune_promoter*.sh` scripts

The Enformer README describes the input as 196,608 bp (40,960 bp flanks on each side around 896 bins of 128 bp) and the target as 896 × 5313 values. The converter produces GENA-LM HDF5 records with 4 kbp sequences, and Enformer TFRecords with 393,216 bp sequences.

The `splicing_onemut` and `clinvar_analysis` directories contain notebooks and data files without accompanying README files.

### Notebooks

- `GENA_sequence_classification_example.ipynb`: sequence classification
- `gena_clusterization_example.ipynb` and `public_gena_clusters*.ipynb`: embedding clustering with t-SNE and UMAP across species
- `gena_enformer_usage.ipynb`: loads the `AIRI-Institute/gena-lm-bert-base-t2t` model at revision `enformer` and analyzes a TXNL4A region

Models are loaded from the Hugging Face hub under the `AIRI-Institute` organization using `AutoTokenizer` and `AutoModel` with `trust_remote_code=True`.

## Configuration

### Model architectures

The files in `data/configs/` define BERT-style architectures:

| File | Layers | Hidden size | Heads | Max positions | Notes |
|---|---|---|---|---|---|
| `L12-H768-A12-V32k-preln.json` | 12 | 768 | 12 | 512 | Pre-layer norm |
| `L12-H768-A12-V32k-preln-lastln.json` | 12 | 768 | 12 | 512 | Adds last-layer norm |
| `L24-H1024-A16-V32k-preln-lastln.json` | 24 | 1024 | 16 | 512 | Large model |
| `L12-H768-A12-V32k-L4096-preln-lastln-sparse-ln1e-05.json` | 12 | 768 | 12 | 4096 | Sparse attention, layer norm epsilon 1e-5 |
| `L12-H768-A12-V32k-L4096-preln-sparse-rope.json` | 12 | 768 | 12 | 4096 | Sparse attention, rotary embeddings |
| `hf_bigbird_L12-H768-A12-V32k-L4096.json` | 12 | 768 | 12 | 4096 | BigBird block-sparse attention |

All BERT-style configs use a vocabulary of 32,000 and pad token ID 3. Sparse configs reference `deepspeed.ops.sparse_attention:BigBirdSparsityConfig`.

### Runtime settings

Fine-tuning scripts use environment variables such as `CUDA_VISIBLE_DEVICES` (GPU selection) and `NP` (number of processes). Notebooks set `TOKENIZERS_PARALLELISM` to `false`.

## Development

- **Package layout**: The package follows a `src/` layout (`package_dir = src`). New modules belong under `src/gena_lm/`.
- **Type checking**: `pyproject.toml` configures mypy with `ignore_missing_imports = true`.
- **Dependency pins**: `transformers` is pinned to `4.17.0`, and `pybedtools` and `pybigwig` are pinned to specific versions.
- **Repository hygiene**: A `.gitignore` file is present, but its contents are not included in the supplied files.

## Testing

Test modules exist for several downstream dataset classes:

- `downstream_tasks/APARENT/test_AparentDataset.py`
- `downstream_tasks/DeepSTARR/test_DeepSTARRDataset.py`
- `downstream_tasks/DeepSea/test_DeepSeaDataset.py`
- `downstream_tasks/SpliceAI/test_SpliceAIDataset.py`

Each test file is paired with sample data where available, such as `AparentDataset_test_data.csv`, `test_Sequences.fa`, and `SpliceAI/test_Dataset_data.csv`. No test runner configuration or CI setup appears in the supplied files, so run the tests directly, for example with `python -m pytest` on the test files.

## License

This project is licensed under the MIT License. The license text states: Copyright (c) 2022 AIRI - Artificial Intelligence Research Institute.
