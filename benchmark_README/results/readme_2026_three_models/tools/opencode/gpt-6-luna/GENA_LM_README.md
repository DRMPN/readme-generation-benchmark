# GENA-LM

GENA-LM is a DNA language-modeling research codebase. It contains a customized BERT implementation, recurrent-memory-transformer (RMT) wrappers, BPE tokenizer and genome-corpus utilities, model configuration/tokenizer assets, notebooks, and examples of downstream sequence-prediction tasks.

This repository does not contain a complete pretrained model checkpoint or the full datasets used by the example tasks. The notebooks and task-specific documentation describe where some external models and data can be obtained.

## Repository layout

- `src/gena_lm/modeling_bert.py` — BERT-family PyTorch models based on the Transformers 4.17 implementation, with options including pre-layer normalization, relative or rotary position encodings, and DeepSpeed sparse attention.
- `src/gena_lm/modeling_rmt.py` — RMT wrappers for sequence classification, token classification, and Enformer-style tasks. These divide long inputs into segments and carry learned memory tokens between segments.
- `src/gena_lm/tokenizers/` — utilities for training a BPE tokenizer from text files containing sequences.
- `src/gena_lm/genome_tools/` — utilities for creating genome sequence corpora, including a variation-corpus script and multi-genome workflow.
- `data/configs/` and `data/tokenizers/` — model configuration JSON files and tokenizer assets. These are not model-weight checkpoints.
- `notebooks/` — examples for sequence classification, clustering, and Enformer use.
- `downstream_tasks/` — data preparation, fine-tuning, evaluation, and task-specific READMEs for promoter prediction, DeepSea, DeepSTARR, Enformer, SpliceAI, APARENT, and other analyses.
- `manuscript_data/` — supplementary tables.

## Installation

The package metadata specifies Python 3.6 or newer. Dependencies are listed in `requirements.txt`; notable entries include PyTorch 1.7.1–1.9.1, Transformers 4.17.0, tokenizers, Biopython, pandas, and genomic-data utilities. The project uses setuptools and can be installed from the repository root:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

The dependency versions are old and may need to be matched to the CUDA, operating system, and task being used. The PyTorch requirement in the checked-in `requirements.txt` has mismatched quote characters; if pip rejects that line, install a compatible PyTorch version separately. Sparse attention also requires DeepSpeed, which is not listed in `requirements.txt`. Some downstream examples have additional system or data requirements, documented in their subdirectories.

## Load a pretrained model

The sequence-classification notebook demonstrates loading the Hugging Face checkpoint `AIRI-Institute/gena-lm-bert-base-t2t` and its tokenizer:

```python
from transformers import AutoModel, AutoTokenizer

checkpoint = "AIRI-Institute/gena-lm-bert-base-t2t"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True)
```

`trust_remote_code=True` allows Transformers to load custom model code from the checkpoint repository. The notebook at [`notebooks/GENA_sequence_classification_example.ipynb`](notebooks/GENA_sequence_classification_example.ipynb) shows an example of fine-tuning for promoter sequence classification, including initializing a classification head. Check the checkpoint repository for its current files and usage details.

## Genome corpus and tokenizer utilities

To build a genome corpus from a FASTA file, the repository's `create_corpus.py` script supports `single_txt`, `jsonl`, and `multiple_txt` output modes. For example, from the repository root:

```bash
python src/gena_lm/genome_tools/create_corpus.py \
  --input-file /path/to/genome.fa \
  --output-dir /path/to/new-output-directory \
  --io-mode jsonl \
  --min-len 10000 \
  --n_augmentations 10
```

The script processes both forward and reverse-complement sequence orientations. Its output directory must not already exist. For tokenizer training, `tokenize_genomes.py` reads `.txt` files from an input directory and writes a BPE tokenizer JSON file:

```bash
python src/gena_lm/tokenizers/tokenize_genomes.py \
  --input_dir /path/to/text-corpus \
  --output_dir /path/to/tokenizer-output \
  --vocab-size 32000
```

See [`src/gena_lm/genome_tools/README.md`](src/gena_lm/genome_tools/README.md) and the species-specific notes under `data/` for additional corpus workflows and external-tool requirements.

## Downstream tasks

Task examples are independent workflows; their datasets and training settings are not all bundled in this repository. Consult each task's README and scripts before running them. Available task directories include:

- [`downstream_tasks/promoter_prediction/`](downstream_tasks/promoter_prediction/) — promoter classification data preparation and fine-tuning.
- [`downstream_tasks/DeepSea/`](downstream_tasks/DeepSea/) — chromatin-profile prediction and dataset preparation.
- [`downstream_tasks/DeepSTARR/`](downstream_tasks/DeepSTARR/) — DeepSTARR fine-tuning example.
- [`downstream_tasks/enformer/`](downstream_tasks/enformer/) — Basenji data conversion, Enformer fine-tuning, and evaluation.
- [`downstream_tasks/SpliceAI/`](downstream_tasks/SpliceAI/) — splice-site prediction fine-tuning and split preparation.
- [`downstream_tasks/APARENT/`](downstream_tasks/APARENT/) — APARENT fine-tuning example.
- `downstream_tasks/clinvar_analysis/` and `downstream_tasks/splicing_onemut/` — analysis notebooks and supporting files.

The shell scripts generally contain task-specific paths, options, and hardware assumptions that need to be reviewed and adjusted for a local dataset and environment. For instance, some fine-tuning examples use multiple GPUs, and some data-preparation scripts rely on external datasets or bioinformatics tools.

## License

The repository includes an MIT license in [`LICENSE`](LICENSE). Some source files also include their own upstream copyright and license notices; retain those notices when redistributing the relevant files.
