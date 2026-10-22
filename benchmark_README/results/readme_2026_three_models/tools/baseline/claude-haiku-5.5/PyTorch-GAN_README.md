# GAN Implementations in PyTorch

This repository contains PyTorch implementations of a collection of Generative Adversarial Network (GAN) variants and related image-to-image models. Each model is a standalone training script, so you run the one you are interested in rather than a single entry point for the whole project.

## Overview

The `implementations/` directory includes the following models, one directory each:

- **Basic GANs:** `gan`, `dcgan`, `lsgan`, `ebgan`, `began`, `bgan`, `dragan`, `relativistic_gan`, `softmax_gan`
- **Wasserstein variants:** `wgan`, `wgan_gp`, `wgan_div`
- **Conditional and auxiliary-label GANs:** `cgan`, `acgan`, `ccgan`, `sgan`
- **Representation learning:** `infogan`, `cluster_gan`, `aae`
- **Multi-domain and image-to-image translation:** `cogan`, `pixelda`, `cyclegan`, `discogan`, `dualgan`, `pix2pix`, `bicyclegan`, `munit`, `unit`, `stargan`
- **Inpainting and super-resolution:** `context_encoder`, `srgan`, `esrgan`

The repository also includes example outputs in `assets/`, such as `gan.gif`, `cyclegan.png`, `pix2pix.png`, and `esrgan.png`.

## Repository Structure

```
data/                 Shell scripts to download CycleGAN and pix2pix datasets
implementations/      One directory per model
  <model>/<model>.py  Training script (argparse options at the top)
  <model>/models.py   Network definitions (for larger models)
  <model>/datasets.py Dataset classes (for models with custom data loading)
assets/               Images and GIFs used for illustration
requirements.txt      Python dependencies
LICENSE               MIT License
```

Several larger implementations split their code into `models.py` and `datasets.py`. Smaller ones, such as `gan.py` and `dcgan.py`, define their networks and data loading inside the training script.

## Installation

The project is written in Python and depends on the packages listed in `requirements.txt`:

```
torch>=0.4.0
torchvision
matplotlib
numpy
scipy
pillow
urllib3
scikit-image
```

Install them with pip:

```bash
pip install -r requirements.txt
```

Some scripts use CUDA when it is available and fall back to the CPU otherwise. However, `cluster_gan/clustergan.py` calls `torch.cuda.FloatTensor` and `.cuda()` directly, so it requires a CUDA-capable GPU.

## Data

### MNIST

Many of the basic GAN scripts (for example `gan`, `dcgan`, `lsgan`, `infogan`, and `cgan`) download MNIST automatically with `download=True` into `../../data/mnist`. The `cogan` and `pixelda` scripts also use MNIST-M, which is provided by `mnistm.py` and is downloaded into `../../data/mnistm` by `cogan`.

### CycleGAN and pix2pix datasets

Two shell scripts in `data/` download datasets from the Berkeley project pages.

`data/download_cyclegan_dataset.sh` accepts one of the following dataset names:

`ae_photos`, `apple2orange`, `summer2winter_yosemite`, `horse2zebra`, `monet2photo`, `cezanne2photo`, `ukiyoe2photo`, `vangogh2photo`, `maps`, `cityscapes`, `facades`, `iphone2dslr_flower`

```bash
cd data
bash download_cyclegan_dataset.sh monet2photo
```

After extraction, the script moves the folders into the layout the project expects:

```
<dataset>/train/A
<dataset>/train/B
<dataset>/test/A
<dataset>/test/B
```

`data/download_pix2pix_dataset.sh` takes a dataset name and downloads the matching `.tar.gz` archive:

```bash
cd data
bash download_pix2pix_dataset.sh facades
```

### CelebA

`context_encoder` and `esrgan` expect the CelebA aligned images. According to the script docstrings, you should download the `img_align_celeba` folder and save it to `../../data/`. `ccgan` uses the same folder by default.

### Expected paths

Scripts resolve data paths relative to their own directory, so each script is designed to be run from inside its implementation folder. For example, the CycleGAN script reads from `../../data/<dataset_name>`, which means the dataset should sit in a `data/` directory two levels above `implementations/cyclegan/`.

## Usage

Change into the directory of the model you want to train and run its script:

```bash
cd implementations/gan
python3 gan.py
```

Most scripts run with default settings and then:

- create an `images/` directory in the current working directory and save generated samples there at each `--sample_interval`;
- print training losses for each batch.

Image-to-image scripts create per-dataset subdirectories:

- `images/<dataset_name>/` for sample grids;
- `saved_models/<dataset_name>/` for checkpoints.

### Example: CycleGAN

```bash
cd implementations/cyclegan
python3 cyclegan.py --dataset_name monet2photo --checkpoint_interval 10
```

### Example: pix2pix

```bash
cd implementations/pix2pix
python3 pix2pix.py --dataset_name facades
```

Pix2pix reads paired images in which the input and target are side by side. Its `ImageDataset` splits each image in half along the width.

### Resuming training

Several image-to-image scripts accept `--epoch` to resume from a saved checkpoint. For example, `cyclegan.py`, `pix2pix.py`, `discogan.py`, `dualgan.py`, `munit.py`, and `bicyclegan.py` load weights from `saved_models/<dataset_name>/` when `--epoch` is non-zero. These scripts expect checkpoints saved at that epoch, so set `--checkpoint_interval` during training.

### Super-resolution inference

`implementations/esrgan/test_on_image.py` applies a trained ESRGAN generator to a single image:

```bash
cd implementations/esrgan
python3 test_on_image.py --image_path path/to/image.png --checkpoint_model saved_models/generator_0.pth
```

Its options are:

- `--image_path` (required): path to the input image
- `--checkpoint_model` (required): path to the generator checkpoint
- `--channels` (default `3`)
- `--residual_blocks` (default `23`)

The output is written to `images/outputs/sr-<filename>`.

## Configuration

Configuration is handled entirely through `argparse` flags defined at the top of each script. Run `python3 <script>.py --help` to see the options for a given model. Because each script defines its own defaults, the same flag can have different defaults in different models.

The following options are common across many scripts:

| Option | Typical default | Description |
|---|---|---|
| `--n_epochs` | `200` | Number of training epochs |
| `--batch_size` | varies (e.g. `64`, `1`, `8`) | Batch size |
| `--lr` | `0.0002` | Adam learning rate |
| `--b1` | `0.5` | Adam first-order momentum decay |
| `--b2` | `0.999` | Adam second-order momentum decay |
| `--n_cpu` | `8` | Number of CPU threads for batch generation |
| `--latent_dim` | varies | Dimensionality of the latent noise vector |
| `--img_size` | varies | Image size |
| `--channels` | `1` or `3` | Number of image channels |
| `--sample_interval` | `400` (varies) | Number of batches between saved samples |
| `--checkpoint_interval` | `-1` | Epochs between checkpoints; `-1` disables saving |
| `--epoch` | `0` | Epoch to start from (for models that support resuming) |

Model-specific options include:

- **CycleGAN:** `--decay_epoch`, `--n_residual_blocks`, `--lambda_cyc`, `--lambda_id`
- **pix2pix:** `--img_height`, `--img_width`, `--decay_epoch`. The L1 weight `lambda_pixel` is set to `100` in the script.
- **ESRGAN:** `--hr_height`, `--hr_width`, `--residual_blocks`, `--warmup_batches`, `--lambda_adv`, `--lambda_pixel`
- **BicycleGAN:** `--lambda_pixel`, `--lambda_latent`, `--lambda_kl`, `--latent_dim`
- **ClusterGAN:** short flags, including `-n` (epochs), `-b` (batch size), `-d` (latent dimension), `-l` (learning rate), `-c` (critic steps), and `-w` (use the Wasserstein metric)
- **Context Encoder:** `--mask_size` (default `64`)
- **CCGAN:** `--mask_size` (default `32`) and `--dataset_name` (default `img_align_celeba`)

For `implementations/bicyclegan`, the default `--dataset_name` is `edges2shoes`. For `cyclegan`, it is `monet2photo`, and for `pix2pix`, it is `facades`.

## Development

Each implementation is self-contained. To add or modify a model, create a new directory under `implementations/` with a training script that follows the existing pattern:

1. Define options with `argparse`.
2. Create output directories with `os.makedirs(..., exist_ok=True)`.
3. Define the networks, losses, and optimizers.
4. Load data through `torchvision` datasets or a custom `Dataset` class in `datasets.py`.
5. Save sample images and, optionally, checkpoints.

The scripts use these conventions:

- Adam optimizers with configurable `--b1` and `--b2`.
- Weight initialization helpers named `weights_init_normal`.
- Sample grids saved with `torchvision.utils.save_image`.

Some supplied files contain issues that may need attention during development. For example:

- `began.py`, `bgan.py`, and `dragan.py` iterate over `mnist_loader` (in `bgan.py`, `began.py`, and `dragan.py`), but no variable with that name is defined in those files.
- `began.py` uses `.data[0]`, which is an indexing pattern that fails on PyTorch versions where zero-dimensional tensors are common.
- `cyclegan/utils.py` and related files use `Variable`, and some scripts use the `pretrained=` argument of `torchvision` models. Check these against the PyTorch version you install.

## Testing

No dedicated test suite is included in the repository. The file tree contains no unit test files and no test runner configuration. The closest thing to a test is `implementations/esrgan/test_on_image.py`, which runs inference on one image using a trained checkpoint and writes the result to `images/outputs/`.

To verify a model, run its training script for a few epochs with a small `--n_epochs` value and check that the expected sample images appear in `images/`.

## License

This project is released under the MIT License. The license file is copyright (c) 2018 Erik Linder-Norén. The full text is in the `LICENSE` file.
