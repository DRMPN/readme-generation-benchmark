# GENA-LM

GENA-LM is a family of DNA language models from the AIRI Institute, together with the code used to build genome corpora, tokenize DNA, and fine-tune models on downstream genomics tasks. This repository contains the model code, data-preparation scripts, and task-specific fine-tuning scripts. It is released under the MIT License.

## Contents

- [Repository layout](#repository-layout)
- [Installation](#installation)
- [Core library (`src/gena_lm`)](#core-library-srcgena_lm)
- [Building data](#building-data)
- [Pre-trained models](#pre-trained-models)
- [Downstream tasks](#downstream-tasks)
- [License](#license)

## Repository layout

| Path | Contents |
| --- | --- |
| `src/gena_lm/` | Core Python package: BERT model with optional pre-layer-norm and rotary embeddings (`modeling_bert.py`), recurrent memory transformer wrappers (`modeling_rmt.py`), sequence utilities (`utils.py`), BPE tokenizer training (`tokenizers/`), and corpus builders (`genome_tools/`). |
| `data/` | Download and processing scripts for genomes (human, yeast, fly, *A. thaliana*), tokenizer files, and model configuration files. |
| `data/configs/` | JSON model configurations (BERT-base and BERT-large variants, sparse attention, RoPE, and last-layer-norm options). |
| `data/tokenizers/` | Pre-built Hugging Face tokenizer files (`human/` and `t2t_1000h_multi_32k/`). |
| `downstream_tasks/` | Dataset preparation code, fine-tuning entry points, and example shell scripts for each task. |
| `notebooks/` | Example notebooks, including sequence classification, Enformer usage, and species clustering. |
| `manuscript_data/` | Supplementary tables (CSV). |

## Installation

The project is packaged with `setup.cfg` (package name `gena-lm`, version `0.0.1`, source in `src/`, requires Python 3.6 or later). Dependencies are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

Notes on the dependencies:

- `torch` is pinned to `>=1.7.1,<=1.9.1` and `transformers` to `==4.17.0`. These are older versions, so you may need to use a matching Python and CUDA environment.
- The fine-tuning scripts launch training with `horovodrun --gloo`. Horovod is not listed in `requirements.txt` and must be installed separately.
- Data-processing scripts also need external tools: [bedtools](https://anaconda.org/bioconda/bedtools) (>2.30), [samtools](https://anaconda.org/bioconda/samtools), and, for some genomes, the [NCBI datasets](https://www.ncbi.nlm.nih.gov/datasets/) command-line tool.

Most task scripts use module paths such as `src.gena_lm.utils` and `downstream_tasks.<task>.<script>`, so run them from the repository root.

## Core library (`src/gena_lm`)

- **`modeling_bert.py`**: a BERT implementation based on Hugging Face Transformers 4.17.0 (per the file header). It adds options such as pre-layer-norm (`pre_layer_norm` in the config), a final layer norm (`last_layer_norm`), sparse attention, and rotary position embeddings.
- **`modeling_rmt.py`**: wrappers for sequence classification, token classification, and Enformer-style outputs that process long inputs as a sequence of segments with memory tokens (recurrent memory transformer).
- **`utils.py`**: helpers including `reverse_complement`, service-token (CLS/SEP) encodings, encoding concatenation, and symmetric padding and truncation of left and right context around a target sequence.
- **`tokenizers/tokenize_genomes.py`**: a CLI that trains a BPE tokenizer with `[UNK]`, `[CLS]`, `[SEP]`, `[PAD]`, and `[MASK]` special tokens. The default vocabulary size is 32,000.

## Building data

### Genome corpora

`src/gena_lm/genome_tools/create_corpus.py` turns a FASTA file into training documents. For each contig at least `--min-len` long (default 10,000 bp), it writes random-offset chunks in one of three formats (`single_txt`, `jsonl`, or `multiple_txt`). It processes both strands. `--n_augmentations` sets how many random shifts are generated per sequence (default 10).

```bash
python3 src/gena_lm/genome_tools/create_corpus.py \
    --input-file path/to/genome.fa.gz \
    --output-dir path/to/output/ \
    --io-mode jsonl --min-len 10000
```

Note that `--output-dir` must not already exist, because the script calls `mkdir` without `exist_ok`.

Per-organism pipelines are documented in the `ReadMe.md` files under `data/`:

- `data/yeasts/`: yeast data (download and processing script `download_and_process_yeast_data.sh`).
- `data/fly/`: *Drosophila* data (`download_and_process_fly_data.sh`). The README uses `--n_augmentations 2`.
- `data/athaliana/`: *Arabidopsis thaliana* data (`download_and_process_athaliana_data.sh`). The README uses `--n_augmentations 6`.
- `data/download_data.sh` downloads a genome through NCBI datasets. Only `human` is implemented; the other options print "genome not supported". `data/download_human.sh` fetches the GRCh38.p13 RefSeq FASTA directly.

The yeast, fly, and *A. thaliana* READMEs list the number of nucleotides in each train and test split. Those figures come from the authors' runs and have not been recomputed here.

### Multi-species and variation corpora

`src/gena_lm/genome_tools/README.md` describes how to build:

- a **multi-species corpus** from Ensembl genome FASTA files, using `create_multigenome_corpus.sh`;
- a **variation corpus** from the 1000 Genomes + HGDP callset in gnomAD, using `create_allele_corpus.py` to apply variants to hg38.

### Tokenizer training

```bash
python src/gena_lm/tokenizers/tokenize_genomes.py \
    --input_dir path/to/txt_files/ \
    --output_dir path/to/output/ \
    --vocab-size 32000 --tokenizer_name BPE
```

The input directory is read for `*.txt` files. The script writes `<tokenizer_name>.json`.

## Pre-trained models

Pre-trained checkpoints are not included in this repository. The notebooks load the Masked Language Modeling checkpoint from the Hugging Face Hub as `AIRI-Institute/gena-lm-bert-base-t2t`:

```python
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("AIRI-Institute/gena-lm-bert-base-t2t")
model = AutoModel.from_pretrained("AIRI-Institute/gena-lm-bert-base-t2t", trust_remote_code=True)
```

The notebooks also link to a table of pre-trained models and fine-tuned checkpoints on the GitHub README. That table is not part of this repository, so this README does not list the other models.

The fine-tuning scripts expect local checkpoints (`*.pth`) under `${HOME_PATH}/t5-experiments/runs/`. Those paths are placeholders from the original environment and should be changed to match your setup.

The configuration files in `data/configs/` describe the architectures that the scripts reference, such as `L12-H768-A12-V32k-preln.json` (12 layers, hidden size 768, 12 heads, 32k vocabulary) and `L24-H1024-A16-V32k-preln-lastln.json` (24 layers, hidden size 1024, 16 heads). The configuration files are the reference for these sizes.

This repository does not include a pre-training script.

## Downstream tasks

Each task directory under `downstream_tasks/` has a README with data sources and preprocessing steps. Most tasks follow the same pattern: prepare the dataset, edit paths and hyperparameters in an example shell script, and run it with `horovodrun`.

| Task | Directory | Description |
| --- | --- | --- |
| Promoter prediction | `promoter_prediction/` | Binary classification of human promoter sequences from EPDnew (hg38). Includes dataset generation (`dataset_generator.py`) and a 5-fold split (`dataset_fold_split.py`). Compares against BigBird and DNABERT. |
| Enformer (CAGE expression) | `enformer/` | Predicts CAGE signal from DNA. Includes conversion of the Basenji dataset to GENA-LM HDF5 and to TFRecord format, plus training and evaluation scripts, including augmentation evaluation. |
| DeepSEA (chromatin profiles) | `DeepSea/` | Multi-label prediction of 919 chromatin profiles, following the BigBird setup. Includes conversion from `.mat` to `.csv.gz` and optional context extension with `extend_dataset.py`, which requires [bwa](https://github.com/lh3/bwa). |
| DeepSTARR (enhancer activity) | `DeepSTARR/` | Predicts *Drosophila* enhancer activity. Uses the Stark lab train/validation/test splits without further preprocessing. |
| SpliceAI (splice sites) | `SpliceAI/` | Predicts splice donor and acceptor sites. Includes a 10% train/validation split (`split_train_valid.py`, seed 42). The source data requires authorized access to BaseSpace project 66029966. |
| APARENT | `APARENT/` | Fine-tuning script and dataset class for APARENT (alternative polyadenylation). This directory has no README. |
| ClinVar analysis | `clinvar_analysis/` | Jupyter notebooks for ClinVar variant analysis (attribution prediction, promoter prediction, and exon BED generation), plus a significance-mapping file (`clinvar_significance_mapping.txt`). This directory has no README. |
| Splicing (one-mutation) | `splicing_onemut/` | A notebook and gene and dataset lists for splicing analysis. This directory has no README. |

Two examples of how these scripts run:

```bash
# Promoter prediction, 2000 bp, using the large model configuration
bash downstream_tasks/promoter_prediction/finetune_promoter_2000_large.sh

# DeepSTARR, one GPU
CUDA_VISIBLE_DEVICES=0 NP=1 ./downstream_tasks/DeepSTARR/finetune_deepstarr.sh
```

Several scripts have `cd ../..` at the top and expect to run from the repository root. Read each script before running it, because they contain hardcoded paths and hyperparameters.

Recurrent memory transformer (RMT) variants of several tasks are provided as separate `*_rmt*.sh` and `run_*_rmt.py` files.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details. The license is copyright AIRI - Artificial Intelligence Research Institute (2022).
