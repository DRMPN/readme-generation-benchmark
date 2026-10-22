# PyTorch-GAN

This repository contains standalone PyTorch implementations of a range of generative adversarial networks (GANs), including unconditional generation, conditional generation, image translation, and image restoration examples. Each implementation lives in its own directory under `implementations/` and is intended to be run as a separate script.

## Implementations

| Directory | Model / task |
| --- | --- |
| `aae` | Adversarial Autoencoder (AAE) |
| `acgan` | Auxiliary Classifier GAN (ACGAN) |
| `began` | Boundary Equilibrium GAN (BEGAN) |
| `bgan` | Boundary-Seeking GAN (BGAN) |
| `bicyclegan` | BicycleGAN for multimodal image-to-image translation |
| `ccgan` | CCGAN (context-conditional image generation) |
| `cgan` | Conditional GAN (CGAN) |
| `cluster_gan` | ClusterGAN |
| `cogan` | Coupled GAN (CoGAN) |
| `context_encoder` | Context Encoder for image completion |
| `cyclegan` | CycleGAN for unpaired image-to-image translation |
| `dcgan` | Deep Convolutional GAN (DCGAN) |
| `discogan` | DiscoGAN for cross-domain image translation |
| `dualgan` | DualGAN for image-to-image translation |
| `dragan` | DRAGAN |
| `ebgan` | Energy-Based GAN (EBGAN) |
| `esrgan` | Enhanced Super-Resolution GAN (ESRGAN), including image inference script |
| `gan` | Basic fully connected GAN |
| `infogan` | InfoGAN |
| `lsgan` | Least Squares GAN (LSGAN) |
| `munit` | MUNIT for multimodal image-to-image translation |
| `pixelda` | Pixel-level Domain Adaptation (PixelDA) |
| `pix2pix` | pix2pix for paired image-to-image translation |
| `relativistic_gan` | Relativistic GAN |
| `sgan` | Semi-Supervised GAN (SGAN) |
| `softmax_gan` | Softmax GAN |
| `srgan` | Super-Resolution GAN (SRGAN) |
| `stargan` | StarGAN for multi-domain image translation |
| `unit` | UNIT for image-to-image translation |
| `wgan` | Wasserstein GAN (WGAN) |
| `wgan_div` | Wasserstein Divergence GAN (WGAN-div) |
| `wgan_gp` | Wasserstein GAN with gradient penalty (WGAN-GP) |

The `assets/` directory contains example output images, animations, and architecture illustrations.

## Repository layout

```text
assets/             Example images and animations
data/               Dataset download scripts
implementations/    One directory per model, with its training script
requirements.txt    Python package dependencies
LICENSE             MIT License
```

Many implementations also include model and dataset helper modules alongside the training script.

## Setup

Use Python with PyTorch and torchvision installed. Install the dependencies listed by the repository with:

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` specifies `torch>=0.4.0`, `torchvision`, `matplotlib`, `numpy`, `scipy`, `pillow`, `urllib3`, and `scikit-image`. The scripts detect CUDA in most cases and otherwise use CPU; `cluster_gan` directly uses CUDA. Install a PyTorch/torchvision combination appropriate for your environment. This code includes APIs from older PyTorch versions, so newer versions may require compatibility changes.

## Running an implementation

Run scripts from their own implementation directory. This matters because dataset paths and output paths are generally relative to the current working directory.

For example, the basic GAN script uses the MNIST dataset through `torchvision` and requests its download if it is not present:

```bash
cd implementations/dcgan
python dcgan.py
```

The script's default options include 200 epochs and a batch size of 64. To inspect its available command-line options:

```bash
python dcgan.py --help
```

Most training scripts expose options such as epoch count, batch size, learning rate, and sample interval; the exact options vary by implementation. A number of examples use MNIST, while image translation, completion, and super-resolution scripts expect datasets on disk.

## Datasets

MNIST-based examples load MNIST via `torchvision` and download it when requested by the script. Other examples expect data under `data/<dataset_name>` when run from their implementation directory. The required layout depends on the script:

- CycleGAN's dataset loader expects `train/A`, `train/B`, `test/A`, and `test/B` subdirectories under the dataset directory. The included downloader prepares this layout for its supported CycleGAN datasets:

  ```bash
  cd data
  bash download_cyclegan_dataset.sh monet2photo
  cd ../implementations/cyclegan
  python cyclegan.py --dataset_name monet2photo
  ```

- pix2pix reads paired images whose left and right halves are domains A and B. Its dataset loader searches a named dataset's `train` and validation directories. The included helper downloads and extracts a dataset archive; for example:

  ```bash
  cd data
  bash download_pix2pix_dataset.sh facades
  cd ../implementations/pix2pix
  python pix2pix.py --dataset_name facades
  ```

- Other image-based scripts define their own dataset expectations in the corresponding `datasets.py` or training script. For example, StarGAN uses CelebA images and an attribute annotation text file; check that implementation's source comments for its setup notes.

The download scripts require `wget` and the relevant archive utility (`unzip` for CycleGAN datasets; `tar` for pix2pix datasets), as well as network access to their configured download URLs.

## Outputs and inference

Training scripts commonly create an `images/` directory for generated samples and, where implemented, a `saved_models/` directory for checkpoints. Their exact filenames, save intervals, and directory structure vary; these paths are usually relative to the implementation directory. Generated data and these output directories are excluded from version control by `.gitignore`.

ESRGAN includes a separate script for running a trained checkpoint on one image. From `implementations/esrgan`, pass paths to the input image and model checkpoint:

```bash
python test_on_image.py \
  --image_path /path/to/input.png \
  --checkpoint_model /path/to/checkpoint.pth
```

## License

This repository is distributed under the MIT License; see [`LICENSE`](LICENSE).
