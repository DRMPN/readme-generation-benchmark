# MiniGPT-4

This repository contains the MiniGPT-4 and MiniGPT-v2 codebase: PyTorch models, training and evaluation scripts, configuration files, and Gradio demos for image-and-text interaction. The MiniGPT-4 code includes image understanding and conversation; the MiniGPT-v2 demo also exposes visual grounding tasks such as referring, detection, and identifying regions in an image.

- Project pages: [MiniGPT-4](https://minigpt-4.github.io/) · [MiniGPT-v2](https://minigpt-v2.github.io/)
- Training instructions: [MiniGPT-4](MiniGPT4_Train.md) · [MiniGPT-v2](MiniGPTv2_Train.md)
- Data preparation: [MiniGPT-4 stage 1](dataset/README_1_STAGE.md) · [MiniGPT-4 stage 2](dataset/README_2_STAGE.md) · [MiniGPT-v2 fine-tuning](dataset/README_MINIGPTv2_FINETUNE.md)
- Evaluation instructions: [MiniGPT-v2 benchmarks](eval_scripts/EVAL_README.md)

## Contents

| Path | Purpose |
| --- | --- |
| `minigpt4/models/` | MiniGPT-4 and MiniGPT-v2 model implementations and shared model components |
| `minigpt4/configs/` | Model, dataset, and environment configuration |
| `train_configs/` | Training configurations for MiniGPT-4 and MiniGPT-v2 |
| `eval_configs/` | Evaluation and demo model configurations |
| `train.py` | Distributed training entry point |
| `demo.py` | MiniGPT-4 Gradio demo |
| `demo_v2.py` | MiniGPT-v2 Gradio demo |
| `eval_scripts/` | MiniGPT-v2 evaluation scripts and instructions |

## Setup

The provided Conda environment specifies Python 3.9 and the project dependencies:

```bash
conda env create -f environment.yml
conda activate minigptv
```

The included demos and training configurations use CUDA. The environment file specifies PyTorch 2.0.0 and CUDA Toolkit via Conda; install a compatible NVIDIA driver for the machine running the model.

Model weights and datasets are not included in this repository. You must obtain the relevant language-model weights and MiniGPT checkpoint, and prepare any datasets you need. Some configurations contain placeholder paths that must be replaced before running.

## Running a demo

### MiniGPT-4

Edit `eval_configs/minigpt4_eval.yaml`: set `model.llama_model` in the referenced model configuration (`minigpt4/configs/models/minigpt4_vicuna0.yaml` or `minigpt4/configs/models/minigpt4_llama2.yaml`) to your language-model directory, and set `model.ckpt` in `eval_configs/minigpt4_eval.yaml` to your MiniGPT-4 checkpoint. Then run:

```bash
python demo.py --cfg-path eval_configs/minigpt4_eval.yaml --gpu-id 0
```

The selected model configuration determines whether the run uses the Vicuna or LLaMA 2 setup. The repository includes example images and a stage-one checkpoint download reference in [the training guide](MiniGPT4_Train.md); the guide notes that stage-one-only checkpoints can produce incomplete or repeated sentences.

### MiniGPT-v2

Edit `eval_configs/minigptv2_eval.yaml` and set `model.llama_model` and `model.ckpt` to the LLaMA model directory and MiniGPT-v2 checkpoint, respectively. Then run:

```bash
python demo_v2.py --cfg-path eval_configs/minigptv2_eval.yaml --gpu-id 0
```

The MiniGPT-v2 interface supports free-form image chat and task prompts for grounding, referring, detection, identifying a selected region, and visual question answering. Both demo scripts call Gradio with `share=True`, which requests a share link when the demo starts.

## Training

`train.py` reads a YAML configuration passed with `--cfg-path`. Before training, set the model and dataset paths in the configuration files and follow the dataset-specific preparation instructions linked above. The example training commands use `torchrun`:

```bash
# MiniGPT-4: stage 1 image-text pretraining
torchrun --nproc-per-node NUM_GPU train.py \
  --cfg-path train_configs/minigpt4_stage1_pretrain.yaml

# MiniGPT-4: stage 2 alignment fine-tuning (requires a stage 1 checkpoint)
torchrun --nproc-per-node NUM_GPU train.py \
  --cfg-path train_configs/minigpt4_stage2_finetune.yaml

# MiniGPT-v2 fine-tuning
torchrun --nproc-per-node NUM_GPU train.py \
  --cfg-path train_configs/minigptv2_finetune.yaml
```

Replace `NUM_GPU` with the number of processes/GPUs to use. The MiniGPT-4 training guide describes its two alignment stages and the dataset requirements. The MiniGPT-v2 fine-tuning configuration likewise requires dataset paths, a language-model path, an initial checkpoint, and an output directory; see [MiniGPTv2_Train.md](MiniGPTv2_Train.md) and the [fine-tuning data guide](dataset/README_MINIGPTv2_FINETUNE.md).

## Evaluation

The repository's benchmark evaluation instructions cover MiniGPT-v2 visual question answering and referring-expression tasks. Prepare the datasets, then edit `eval_configs/minigptv2_benchmark_evaluation.yaml` to set the LLaMA path, checkpoint, annotation/image paths, and output path. Run the commands and dataset lists in [eval_scripts/EVAL_README.md](eval_scripts/EVAL_README.md); the entry points are `eval_scripts/eval_vqa.py` and `eval_scripts/eval_ref.py`.

## Configuration and data

Configuration files are YAML. The demo configuration selects a model architecture and checkpoint and describes image preprocessing. Training configurations additionally define the datasets, optimization settings, and output directory. Dataset-specific storage paths are configured under `minigpt4/configs/datasets/`; the preparation guides explain the expected files and directory structures.

The first MiniGPT-4 training stage uses image-text data based on LAION and CC/SBU, and the second uses a smaller image-text alignment dataset. MiniGPT-v2 fine-tuning configurations combine multiple image/text datasets; the detailed list and setup steps are in `dataset/README_MINIGPTv2_FINETUNE.md`.

## License

See [`LICENSE.md`](LICENSE.md) and [`LICENSE_Lavis.md`](LICENSE_Lavis.md) for the license terms included with this repository.
