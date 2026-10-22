# PyTorch GAN Implementations

This repository is a collection of standalone PyTorch scripts for training and experimenting with generative adversarial networks (GANs). Implementations are organized under `implementations/`, generally with one directory per model and a script that defines its training loop. Some approaches also have separate model and dataset modules.

The collection includes GAN, DCGAN, conditional and auxiliary-classifier GANs, InfoGAN, ClusterGAN, WGAN variants, CycleGAN, Pix2Pix, BicycleGAN, DiscoGAN, DualGAN, UNIT, MUNIT, Context Encoder, PixelDA, and super-resolution approaches including SRGAN and ESRGAN. The `assets/` directory contains model illustrations, architecture images, and sample animations.

![Project logo](assets/logo.png)

## Requirements

The dependencies listed in `requirements.txt` are:

- PyTorch (`torch>=0.4.0`) and `torchvision`
- `numpy`, `scipy`, `matplotlib`, and `scikit-image`
- `pillow` and `urllib3`

The repository does not specify a Python version or provide a pinned environment file. Install a compatible Python and PyTorch environment for your system, then install the listed packages:

```bash
python -m pip install -r requirements.txt
```

Training scripts commonly select CUDA when it is available and otherwise use CPU, but hardware support and training speed depend on the individual script and your installed PyTorch build.

## Repository layout

- `implementations/<model>/` — model-specific training scripts and, for some models, supporting modules.
- `data/` — shell scripts for downloading selected CycleGAN and Pix2Pix datasets.
- `assets/` — example outputs, diagrams, and the logo.
- `requirements.txt` — Python dependencies.
- `LICENSE` — MIT license.

Most image-generation scripts save samples in an `images/` directory relative to the current working directory. Some translation and super-resolution implementations also save model checkpoints under `saved_models/`.

## Setup and data

Many scripts use the MNIST dataset through `torchvision.datasets.MNIST` and request it with `download=True`. In those scripts, data is stored at a path such as `../../data/mnist`, relative to the script’s working directory.

For image-to-image translation scripts, the dataset classes generally expect data under `../../data/<dataset_name>`. Run scripts from their own implementation directory so that these relative paths resolve to the repository’s `data/` directory. For example:

```bash
cd implementations/dcgan
python dcgan.py
```

The CycleGAN and Pix2Pix download helpers should be run from `data/` to place downloaded data there. The CycleGAN helper accepts a dataset name from the list in the script, including `horse2zebra`, `apple2orange`, `monet2photo`, `maps`, and `facades`:

```bash
cd data
bash download_cyclegan_dataset.sh horse2zebra
```

The helper unpacks the archive and reorganizes its `trainA`, `trainB`, `testA`, and `testB` folders into `horse2zebra/train/A`, `horse2zebra/train/B`, `horse2zebra/test/A`, and `horse2zebra/test/B`. CycleGAN’s dataset loader expects that structure.

The Pix2Pix helper takes a dataset archive name and downloads and extracts its archive into the current directory. For example, the Pix2Pix implementation defaults to the `facades` dataset:

```bash
cd data
bash download_pix2pix_dataset.sh facades
```

Paired-image dataset loaders in this repository split each source image into an A half and a B half. Check the relevant implementation’s dataset loader and the archive contents before using a dataset with it.

Some scripts expect datasets that are not downloaded by these helpers. For example, the Context Encoder and ESRGAN scripts document CelebA image data under `../../data/img_align_celeba`; consult those scripts for their stated dataset instructions.

## Usage

Each implementation is launched independently. Run it from its own directory; scripts that import sibling modules such as `models.py` or `datasets.py` rely on that layout. For example:

```bash
cd implementations/cgan
python cgan.py
```

Most training scripts expose settings through command-line arguments parsed with `argparse`. Use `--help` from the implementation directory to inspect the options available for that script. Common options include the number of epochs, batch size, learning rate, image dimensions, channel count, and sample interval, but names and defaults vary by implementation.

For example, the DCGAN script defines `--n_epochs`, `--batch_size`, and `--sample_interval`:

```bash
cd implementations/dcgan
python dcgan.py --n_epochs 2 --batch_size 32 --sample_interval 100
```

This runs a short training session; it is not an automated correctness test. Training scripts print losses and save generated samples at their configured intervals. Implementations with checkpoint options can also save model weights under `saved_models/`; check the individual script for checkpoint flags and file locations.

ESRGAN includes a separate image-inference script. It requires paths to both an input image and a generator checkpoint:

```bash
cd implementations/esrgan
python test_on_image.py \
  --image_path /path/to/image.png \
  --checkpoint_model /path/to/checkpoint.pth
```

The inference script also accepts `--channels` and `--residual_blocks`; use values compatible with the checkpoint’s model.

## Configuration

Configuration is primarily per-script rather than centralized. Read the argument parser and data-loading code in the implementation you plan to run before starting a long job. In particular, verify:

- The expected dataset name, directory layout, and image format.
- Image size, number of channels, and any paired-image assumptions.
- Training duration, batch size, and worker count.
- Sampling and checkpoint intervals, where provided.
- Any model-specific loss weights or architecture parameters exposed as arguments.

Paths such as `../../data/<dataset_name>`, `images/`, and `saved_models/` are relative to the process’s current working directory. Running from a different directory can therefore change where data is read or outputs are written.

## Development and testing

Implementations are mostly independent. To explore or modify one, inspect its training script together with any neighboring `models.py`, `datasets.py`, or utility module. Keep the working directory in mind when importing local modules and resolving data and output paths.

No automated test suite or test-runner configuration is included in the supplied repository files. A practical manual check is to install the dependencies, confirm the selected dataset is available, inspect the script’s `--help` output, and try a short run with a small epoch count and batch size. Verify that the script starts, reports training progress, and writes sample images to its expected output directory. These checks do not guarantee that every implementation or configuration will work on every environment.

## License

This project is distributed under the MIT License. The license file credits Erik Linder-Norén and requires inclusion of the copyright and permission notice in copies or substantial portions of the software. See [`LICENSE`](LICENSE) for the full text.
