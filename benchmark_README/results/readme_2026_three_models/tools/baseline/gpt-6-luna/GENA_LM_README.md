# GENA-LM

GENA-LM is a DNA language-model project. It provides model implementations, genome preprocessing and tokenization tools, model configuration files, and example workflows for pretraining and downstream genomic prediction. The repository also includes datasets or dataset-preparation code for several tasks, plus notebooks demonstrating model use and DNA embedding analysis.

The Python package is named `gena-lm` (version `0.0.1`). Model code is under `src/gena_lm/`; task-specific datasets, scripts, and examples are under `downstream_tasks/`.

## Repository overview

- **`src/gena_lm/`** contains BERT and recurrent-memory-transformer modeling code, utilities, and genome tooling.
- **`src/gena_lm/genome_tools/`** includes scripts for creating genome corpora, applying variants to references, and building multi-genome corpora.
- **`src/gena_lm/tokenizers/`** contains genome tokenization code.
- **`data/`** contains tokenizer assets, model configuration JSON files, genome-related data and processing scripts.
- **`downstream_tasks/`** contains dataset classes, preprocessing scripts, and finetuning or evaluation entry points.
- **`notebooks/`** provides examples for sequence classification, Enformer usage, and clustering DNA embeddings.
- **`manuscript_data/`** contains supplementary tables.

Available task workflows include APARENT, DeepSTARR, DeepSea, SpliceAI, Enformer, and promoter prediction. The repository also contains ClinVar and one-mutation splicing analysis materials.

## Setup

The package metadata requires Python 3.6 or later. Its declared dependencies are listed in `requirements.txt`; notable version constraints include PyTorch `>=1.7.1,<=1.9.1`, Transformers `4.17.0`, pandas `>=1.5.0,<2.0.0`, pysam `>=0.19.1`, and pybedtools `0.10.0`.

Create and activate a Python environment, then install the dependencies and package:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

Some data-preparation workflows also require command-line tools that are not Python dependencies. The Arabidopsis workflow documents bedtools greater than 2.30, samtools, and NCBI Datasets. Fly and yeast workflows document bedtools greater than 2.30 and samtools. The Arabidopsis and fly scripts use Docker to run Cactus tools; the DeepSea context-extension script requires `bwa` on `PATH`. Check the relevant task or data README before running a workflow, since external tools and source datasets vary by task.

## Usage

### Build a genome corpus

`src/gena_lm/genome_tools/create_corpus.py` can build a corpus from a genome FASTA input. For example, after preparing the Arabidopsis FASTA as described in `data/athaliana/ReadMe.md`, run from the repository root:

```bash
python src/gena_lm/genome_tools/create_corpus.py \
  --input-file data/athaliana/athaliana_fasta_for_corpus_generation.fa.gz \
  --output-dir data/athaliana/athaliana_corpus/ \
  --io-mode jsonl \
  --min-len 10000 \
  --n_augmentations 6
```

The fly instructions use the same tool with `--min-len 10000` and `--n_augmentations 2`; the yeast instructions use `--min-len 10000`. For a multi-species corpus, see `src/gena_lm/genome_tools/README.md` and the `create_multigenome_corpus.sh` script. That workflow expects genome FASTA files and processed contig information.

### Explore a pretrained model

The notebooks include examples of loading models and tokenizers with Hugging Face Transformers. For instance, `notebooks/gena_enformer_usage.ipynb` loads the `AIRI-Institute/gena-lm-bert-base-t2t` tokenizer and model, using the model’s `enformer` revision and `trust_remote_code=True`:

```python
from transformers import AutoModel, AutoTokenizer

model_id = "AIRI-Institute/gena-lm-bert-base-t2t"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(
    model_id,
    trust_remote_code=True,
    revision="enformer",
)
```

The notebook demonstrates applying the model to genomic sequence in an Enformer-related example. The clustering notebooks show another workflow: generating sequence embeddings and visualizing them with dimensionality reduction.

### Finetune on a downstream task

Task scripts are examples rather than a single project-wide command. Review the task README and shell script, edit data paths and hyperparameters as directed, and then run the script. For example, the DeepSTARR instructions use:

```bash
CUDA_VISIBLE_DEVICES=0 NP=1 ./finetune_deepstarr.sh
```

The task directories include separate scripts for other setups, including multiple SpliceAI and Enformer variants. GPU count and script options differ by workflow; consult the corresponding documentation before launching training.

## Configuration

Model configuration files are stored in `data/configs/`. Their filenames describe model variants, and their JSON fields specify architecture and model parameters. The supplied configurations include BERT-style models with 12 layers, hidden size 768, 12 attention heads, and vocabulary size 32,000, as well as a 24-layer, hidden-size-1024 configuration. Some configurations set a maximum position length of 4,096 and specify sparse attention; another uses rotary position embeddings. A Hugging Face BigBird configuration is also included.

Use the configuration that matches the intended model and workflow. The repository does not define one global training configuration: downstream shell scripts and Python entry points may have their own paths and hyperparameters, which should be checked and adjusted for the local dataset and hardware.

## Data and task documentation

Data acquisition and processing instructions are distributed alongside the data and task code:

- `data/athaliana/ReadMe.md`, `data/fly/ReadMe.md`, and `data/yeasts/ReadMe.md` document genome-specific corpus preparation.
- `src/gena_lm/genome_tools/README.md` documents multi-species and 1000 Genomes + HGDP variation-corpus workflows.
- Task-specific READMEs cover DeepSTARR, DeepSea, SpliceAI, Enformer, and promoter prediction.

Several workflows depend on external datasets. For example, the SpliceAI README notes that access to the original dataset requires authorization; Enformer conversion instructions assume the Basenji dataset has already been downloaded. Verify dataset access, reference-genome versions, and paths before running preprocessing or training.

## Development and testing

Core package code uses the `src/` layout. To work against a local checkout, install it in editable mode with `python -m pip install -e .`. The project’s `pyproject.toml` configures setuptools as the build backend and sets mypy to ignore missing imports.

Dataset-focused test files are included in the APARENT, DeepSTARR, DeepSea, and SpliceAI task directories. Small test inputs accompany several of them. The supplied files do not specify a repository-wide test command or declare a test framework in the listed requirements. If using pytest, install it separately and run the relevant tests from the repository root, for example:

```bash
python -m pytest downstream_tasks/DeepSTARR/test_DeepSTARRDataset.py
```

Other task tests can be invoked by their corresponding `test_*.py` paths. These tests exercise task dataset code; they do not replace checks of external downloads, preprocessing tools, or full model-training runs.

## License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE) for the full terms. The license permits use, modification, distribution, and sublicensing subject to retaining the copyright and permission notice, and provides the software without warranty.
