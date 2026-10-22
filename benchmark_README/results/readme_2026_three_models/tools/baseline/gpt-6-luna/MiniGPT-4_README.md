# MiniGPT-4 and MiniGPT-v2

This repository contains implementations, configuration files, training and evaluation scripts, and Gradio demos for MiniGPT-4 and MiniGPT-v2. Both are image-and-language models that accept an image and a text prompt. MiniGPT-4 supports image conversation; MiniGPT-v2 also includes workflows for visual question answering and visual grounding, including referring, detection, and identifying objects.

The code is organized as the `minigpt4` Python package. Model definitions are in `minigpt4/models`, dataset loaders and builders are in `minigpt4/datasets`, and YAML configuration files are grouped under `minigpt4/configs`, `train_configs`, and `eval_configs`. The `examples` and `examples_v2` directories contain images used in the demos.

## Setup

The supplied environment file specifies Python 3.9, CUDA toolkit, and pinned versions of PyTorch and several supporting libraries.

```bash
conda env create -f environment.yml
conda activate minigptv
```

The environment includes packages such as `torch==2.0.0`, `transformers==4.30.0`, `timm==0.6.13`, `gradio==3.47.1`, `accelerate==0.20.3`, and `bitsandbytes==0.37.0`. The demo scripts place models on CUDA devices, and training configurations specify `device: "cuda"`. A working CUDA/PyTorch installation and compatible GPU are therefore needed for the workflows shown here.

Model weights and data are not bundled as project files. Before running a demo or training job, obtain the relevant language-model checkpoint, MiniGPT checkpoint, and datasets, then set their paths in the configuration you plan to use.

## Usage

### MiniGPT-4 demo

`demo.py` requires a configuration file and accepts an optional GPU index:

```bash
python demo.py --cfg-path eval_configs/minigpt4_eval.yaml --gpu-id 0
```

The configuration’s `model.ckpt` value is a placeholder and must be changed to the pretrained checkpoint path. Choose `eval_configs/minigpt4_llama2_eval.yaml` for the LLaMA 2 model type; `eval_configs/minigpt4_eval.yaml` uses the Vicuna model type. The demo opens a Gradio interface for uploading an image, chatting, and adjusting beam search and temperature.

### MiniGPT-v2 demo

`demo_v2.py` defaults to `eval_configs/minigptv2_eval.yaml`; a different configuration and GPU index can also be supplied:

```bash
python demo_v2.py --cfg-path eval_configs/minigptv2_eval.yaml --gpu-id 0
```

Set the pretrained checkpoint path in the selected YAML first. The interface includes task shortcuts for grounding, referring, detection, identifying, and visual question answering, as well as free-form chat. The identify workflow supports drawing a box on the image.

Both demo scripts launch Gradio with sharing enabled in their code. Consider this when choosing where and how to run them.

## Configuration and data

Configurations are YAML files. Model settings include the architecture and model type, language-model and MiniGPT checkpoint paths, image size, text limits, and options such as low-resource loading and LoRA. Dataset and processor settings specify data paths, image processors, batch sizes, and sampling ratios. Run settings include training schedule, output directory, seed, distributed settings, and optional Weights & Biases logging. Edit the relevant YAML rather than assuming placeholder paths will work.

### Training data

For MiniGPT-4 stage one, the dataset instructions describe filtered CC3M/CC12M/SBU and LAION data and estimate approximately `2.3T` of storage. They provide annotation download links and explain converting the downloaded JSON annotations to TSV with `dataset/convert_cc_sbu.py` and `dataset/convert_laion.py`. Update the dataset paths in `minigpt4/configs/datasets/cc_sbu/defaults.yaml` and `minigpt4/configs/datasets/laion/defaults.yaml`.

Stage two uses the separate `cc_sbu_align` dataset. After downloading and extracting it, configure its path in `minigpt4/configs/datasets/cc_sbu/align.yaml`. MiniGPT-v2 fine-tuning uses a wider set of datasets, including COCO, Visual Genome, TextCaps, RefCOCO variants, and conversation and instruction datasets. The preparation guide, `dataset/README_MINIGPTv2_FINETUNE.md`, gives download sources, expected directory layouts, and the dataset YAML files in which to set `image_path` and `ann_path`.

The stage-one dataset guide refers to `download_cc_sbu.sh` and `download_laion.sh`, but those scripts are not present in the supplied repository tree. The conversion scripts are present; prepare or obtain the download scripts separately if following that guide’s download steps.

## Training

Training is started with `train.py` and a YAML file. MiniGPT-4 uses two alignment stages: stage one aligns vision and language features using image-text pairs, and stage two fine-tunes on a smaller conversation-format dataset. For example:

```bash
torchrun --nproc-per-node NUM_GPU train.py \
  --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
```

After preparing stage-one data, run stage two with:

```bash
torchrun --nproc-per-node NUM_GPU train.py \
  --cfg-path train_configs/minigpt4_stage2_finetune.yaml
```

Before stage-two training, set its `model.ckpt` to the stage-one checkpoint and configure the output directory. The repository also includes corresponding LLaMA 2 configurations: `minigpt4_llama2_stage1_pretrain.yaml` and `minigpt4_llama2_stage2_finetune.yaml`. The training guide reports using four A100 GPUs for stage one and one A100 for stage two in its experiments; these are reported experiment settings, not guarantees about other hardware.

For MiniGPT-v2, prepare the data described above, then set the LLaMA checkpoint, pretrained checkpoint, and output path in `train_configs/minigptv2_finetune.yaml` and launch:

```bash
torchrun --nproc-per-node NUM_GPU train.py \
  --cfg-path train_configs/minigptv2_finetune.yaml
```

## Evaluation

MiniGPT-v2 benchmark configuration is in `eval_configs/minigptv2_benchmark_evaluation.yaml`. Set the language-model and MiniGPT checkpoint paths, evaluation annotation and image paths, and output `save_path` before running evaluation. The detailed dataset layout and commands are in `eval_scripts/EVAL_README.md`.

For example, from `eval_scripts`:

```bash
torchrun --master-port PORT --nproc_per_node 1 eval_ref.py \
  --cfg-path ../eval_configs/minigptv2_benchmark_evaluation.yaml \
  --dataset refcoco,refcoco+,refcocog --resample

torchrun --master-port PORT --nproc_per_node 1 eval_vqa.py \
  --cfg-path ../eval_configs/minigptv2_benchmark_evaluation.yaml \
  --dataset okvqa,vizwiz,iconvqa,gqa,vsr,hm
```

Configure the evaluation data paths before running these commands. The evaluation scripts cover referring-expression benchmarks and visual question-answering datasets.

## Development and testing

The package uses a registry to connect model, dataset builder, processor, task, runner, and learning-rate scheduler implementations. When changing behavior, check the relevant Python module and its YAML configuration together. Training and evaluation import the builders, models, processors, runners, and tasks to register implementations.

No general automated test suite or test command is included in the supplied file tree. The runnable checks documented here are the demos, training entry point, and dataset-specific evaluation scripts; they require their configuration paths, data, checkpoints, and runtime dependencies. For contributions, the repository provides GitHub issue templates for bug reports and feature requests. Please also follow `CODE_OF_CONDUCT.md`.

## License

The repository includes `LICENSE.md`, which specifies the BSD 3-Clause License with copyright 2023 Deyao Zhu, and `LICENSE_Lavis.md`, which specifies the BSD 3-Clause License with copyright 2022 Salesforce, Inc. Review both files when redistributing or modifying code; the applicable notice and conditions depend on the material being used. The dataset and pretrained-model sources have their own terms, which are not established by these repository license files.
