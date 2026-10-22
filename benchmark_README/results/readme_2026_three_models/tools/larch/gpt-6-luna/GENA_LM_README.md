# GENA_LM-86h_455g

GENA_LM is a repository for working with genomic sequence language models and downstream genomics tasks. It contains model and tokenizer configuration files, data-preparation utilities, task-specific fine-tuning and evaluation scripts, example notebooks, and dataset-related files.

This README is based on the files present in the repository. For exact command-line options, expected input formats, and dataset requirements, consult the relevant script’s `--help` output and nearby task-specific README files.

## Contents

- [Repository layout](#repository-layout)
- [Requirements and installation](#requirements-and-installation)
- [Data and downloads](#data-and-downloads)
- [Model and tokenizer files](#model-and-tokenizer-files)
- [Downstream tasks](#downstream-tasks)
- [Notebooks and examples](#notebooks-and-examples)
- [Typical workflow](#typical-workflow)
- [Reproducibility and troubleshooting](#reproducibility-and-troubleshooting)
- [License and data usage](#license-and-data-usage)

## Repository layout

The repository contains several groups of files:

| Area | Contents |
|---|---|
| Model and tokenizer | Model configuration JSON files, tokenizer configuration files, and BPE vocabulary files |
| Genome corpus preparation | Scripts for creating single- or multi-genome corpora and tokenizing genomes |
| Genome data downloads | Download and processing scripts and metadata for human, plant, fly, and yeast genomes |
| Fine-tuning tasks | Dataset classes, training and evaluation scripts, and shell launchers for downstream benchmarks |
| Examples | Jupyter notebooks demonstrating model usage, prediction, and clustering |
| Tests and samples | Small example inputs and tests for selected dataset classes |

Some names in the repository listing occur more than once, such as tokenizer files and `valid_species_stats.tsv`. Treat the copies in their respective directories as task- or dataset-specific unless inspection confirms otherwise.

### Genome corpus and preprocessing files

Files include:

- `create_corpus.py`
- `create_allele_corpus.py`
- `create_multigenome_corpus.sh`
- `tokenize_genomes.py`
- `full_ensembl_genomes_metadata.cvs`
- `2023-08-10 19_40_52.828317species_extended_metadata.csv`
- `1KG+HGDP.selected_samples.tsv`

The repository listing spells one metadata filename `full_ensembl_genomes_metadata.cvs`. Check the actual filename before using it; it may be an intentional `.cvs` extension or a typo.

### Genome download scripts

The listed download and processing scripts include:

- `download_human.sh`
- `download_data.sh`
- `download_and_process_athaliana_data.sh`
- `download_and_process_fly_data.sh`
- `download_and_process_yeast_data.sh`

Related data and metadata include species statistics, genome lists, assembly links, and holdout BED files. Review each script before running it: downloads may be large, may require external tools, and may write to paths defined inside the script.

### Task-specific files

Task code is grouped by benchmark. See [Downstream tasks](#downstream-tasks) for an overview.

## Requirements and installation

The repository includes `requirements.txt`, `pyproject.toml`, and `setup.cfg`. Start by reviewing these files to determine the intended Python version and dependency versions.

A standard installation in a virtual environment is:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

If the project is configured as an installable package, you can also install it in editable mode:

```bash
python -m pip install -e .
```

Check whether the project requires a particular PyTorch, CUDA, or accelerator setup before installing deep-learning dependencies. The appropriate installation may depend on your operating system and hardware.

For Jupyter notebooks, install Jupyter if it is not already included:

```bash
python -m pip install jupyter
```

## Data and downloads

Many workflows require external genomic data that may not be included in the repository. Before preparing data:

1. Read the relevant task’s README and download script.
2. Check required external tools and available disk space.
3. Confirm where the script will save files and whether it overwrites existing data.
4. Review the source dataset’s terms, citation requirements, and permitted uses.
5. Keep raw downloads separate from processed data and model outputs.

The repository includes or references files such as:

- BED files for test or holdout regions
- Genome assembly links and genome lists
- Species metadata and statistics
- Sample tables for genomic or allele-based workflows
- Example CSV and sequence files for task datasets

Do not assume these small repository files are a complete dataset. Some may be examples, test fixtures, or metadata used to obtain larger files.

## Model and tokenizer files

The repository lists several model configuration files, including configurations for different layer counts, hidden sizes, attention heads, context lengths, and model variants. Examples include:

- `L12-H768-A12-V32k-preln.json`
- `L12-H768-A12-V32k-L4096-preln-sparse-rope.json`
- `L12-H768-A12-V32k-preln-lastln.json`
- `L24-H1024-A16-V32k-preln-lastln.json`
- `hf_bigbird_L12-H768-A12-V32k-L4096.json`

Tokenizer-related files include `tokenizer.json`, `tokenizer_config.json`, `special_tokens_map.json`, `BPE.json`, and `BPE_no_n_all_chr.json`.

These files describe model or tokenizer setup; they are not necessarily trained model weights. No model checkpoint files are identifiable from the supplied repository listing. Check the task scripts and configuration files for instructions on obtaining or specifying pretrained weights.

## Downstream tasks

The repository includes data and scripts for several downstream benchmarks.

### DeepSEA

Files include:

- `DeepSeaDataset.py`
- `prepare_dataset.py`
- `extend_dataset.py`
- `run_deepsea_finetuning.py`
- `finetune_deepsea.sh`
- `test_DeepSeaDataset.py`

### SpliceAI

Files include:

- `SpliceAIDataset.py`
- `split_train_valid.py`
- `run_spliceai_finetuning.py`
- `run_spliceai_finetuning_rmt.py`
- Multiple `finetune_spliceai*.sh` launchers
- Dataset tests and sample data

### APARENT

Files include:

- `AparentDataset.py`
- `run_APARENT_finetuning.py`
- `run_aparent_finetuning.sh`
- `test_AparentDataset.py`
- Example test data

### Enformer

Files include:

- `enformer_dataset.py`
- `enformer_model.py`
- `run_enformer_finetuning.py`
- `run_enformer_finetuning_rmt.py`
- `run_enformer_evaluation.py`
- `run_enformer_evaluation_augs.py`
- `enformer_metrics.py`
- `convert_basenji_dataset.py`
- Several Enformer fine-tuning and evaluation shell scripts

### DeepSTARR

Files include:

- `DeepSTARRDataset.py`
- `run_deepstarr_finetuning.py`
- `finetune_deepstarr.sh`
- Example sequence and activity files
- `test_DeepSTARRDataset.py`

### Promoter prediction

Files include:

- `dataset.py`
- `dataset_generator.py`
- `run_promoter_finetuning.py`
- `run_promoter_finetuning_rmt.py`
- Multiple promoter fine-tuning shell scripts
- Example promoter sequence and dataset files

### Clinical variant and related analyses

The repository also contains notebooks and supporting files for ClinVar and promoter analyses, including `clinvar.ipynb`, `clinvar_attribution_prediction.ipynb`, `clinvar_promoter_prediction.ipynb`, and related data files.

### Running a task

The shell scripts are task launchers, but their required arguments, environment variables, and paths are not inferable from their filenames. Inspect a launcher and its corresponding Python script before use:

```bash
sed -n '1,240p' finetune_deepsea.sh
python run_deepsea_finetuning.py --help
```

If the script does not provide a `--help` option, inspect its argument parser and configuration-loading code. Update data, checkpoint, and output paths for your environment before launching a run.

## Notebooks and examples

The repository includes notebooks for model usage, sequence classification, clustering, Enformer usage, splice analysis, and ClinVar-related predictions. Examples include:

- `GENA_sequence_classification_example.ipynb`
- `gena_enformer_usage.ipynb`
- `gena_clusterization_example.ipynb`
- `public_gena_clusters.ipynb`
- `public_gena_clusters_task.ipynb`
- `splice_check.ipynb`
- ClinVar analysis notebooks

Launch Jupyter from the repository root:

```bash
jupyter lab
```

Notebooks may expect data or checkpoints at paths that are specific to the original development environment. Update those paths before running the notebook.

## Typical workflow

A common workflow for using the repository is:

1. **Choose a task.** Locate its dataset class, training script, launcher, and README.
2. **Set up the environment.** Install dependencies and verify the required hardware configuration.
3. **Obtain the data.** Follow the task’s download or preprocessing instructions.
4. **Configure inputs and outputs.** Set the dataset, tokenizer, checkpoint, and output paths used by the script.
5. **Check the dataset.** Run the relevant dataset tests or use the provided example inputs.
6. **Train or evaluate.** Run the task-specific Python script or shell launcher.
7. **Record the run details.** Save the code revision, configuration, data version, random seed, hardware details, and output location.

## Reproducibility and troubleshooting

- **Paths:** Search scripts and notebooks for hard-coded paths and update them for your environment.
- **Large downloads:** Confirm the destination and expected disk usage before running download scripts.
- **Checkpoints:** Verify that the checkpoint required by a fine-tuning script is actually available; configuration files alone are not weights.
- **Dependencies:** If installation fails, check the project configuration and task-specific instructions for version or accelerator requirements.
- **Dataset formats:** Inspect dataset classes and provided tests to learn the expected columns, sequence representation, labels, and preprocessing.
- **GPU memory:** Reduce batch size or sequence length only if the relevant script exposes those settings, and record any changes.
- **Tests:** Run the available tests from the repository root. For example:

  ```bash
  python -m pytest
  ```

  Tests may require optional dependencies or sample files; consult the relevant test and task README if a test cannot run.

## License and data usage

The repository includes a `LICENSE` file. Read it before using or redistributing the code.

Code licensing does not necessarily cover downloaded datasets, genome assemblies, metadata, pretrained checkpoints, or benchmark data. Check each source’s terms and citation requirements separately. When publishing results, cite the repository and the original datasets or methods used, following their respective guidance.
