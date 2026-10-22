# PyTorch-GAN

A collection of PyTorch implementations of Generative Adversarial Networks (GANs) and related models, each as a standalone, single-file script. The implementations cover unconditional and conditional GANs, Wasserstein and other loss variants, image-to-image translation, super-resolution, and unsupervised domain adaptation.

The repository is released under the MIT License, Copyright (c) 2018 Erik Linder-Norén (see [LICENSE](LICENSE)).

![Logo](assets/logo.png)

## Contents

- [Repository layout](#repository-layout)
- [Implementations](#implementations)
- [Requirements](#requirements)
- [Getting started](#getting-started)
- [Downloading datasets](#downloading-datasets)
- [Running the examples](#running-the-examples)
- [Command-line options](#command-line-options)
- [Outputs](#outputs)
- [Notes](#notes)
- [License](#license)

## Repository layout

```
.
├── assets/            # Sample images and GIFs used for illustration
├── data/              # Dataset download scripts (datasets are stored here)
│   ├── download_cyclegan_dataset.sh
│   └── download_pix2pix_dataset.sh
├── implementations/   # One directory per model
│   ├── gan/
│   │   └── gan.py
│   ├── cyclegan/
│   │   ├── cyclegan.py
│   │   ├── datasets.py
│   │   ├── models.py
│   │   └── utils.py
│   └── ...
├── requirements.txt
└── LICENSE
```

Most implementations are a single script (for example, `implementations/gan/gan.py`). Models that need dataset loaders or network definitions in separate modules include `datasets.py`, `models.py`, and sometimes `utils.py` in the same directory.

## Implementations

Each directory under `implementations/` contains one model. The directories are:

| Directory | Model | Directory | Model |
|---|---|---|---|
| `aae` | Adversarial Autoencoder | `lsgan` | Least Squares GAN |
| `acgan` | Auxiliary Classifier GAN | `munit` | MUNIT |
| `bgan` | Boundary-Seeking GAN | `pix2pix` | pix2pix |
| `began` | BEGAN | `pixelda` | PixelDA |
| `bicyclegan` | BicycleGAN | `relativistic_gan` | Relativistic GAN |
| `ccgan` | Context-Conditional GAN | `sgan` | Semi-Supervised GAN |
| `cgan` | Conditional GAN | `softmax_gan` | Softmax GAN |
| `cluster_gan` | ClusterGAN | `srgan` | SRGAN |
| `cogan` | CoGAN | `stargan` | StarGAN |
| `context_encoder` | Context Encoder | `unit` | UNIT |
| `cyclegan` | CycleGAN | `wgan` | Wasserstein GAN |
| `dcgan` | DCGAN | `wgan_div` | WGAN-div |
| `discogan` | DiscoGAN | `wgan_gp` | WGAN-GP |
| `dragan` | DRAGAN | `gan` | Vanilla GAN |
| `dualgan` | DualGAN | `ebgan` | EBGAN |
| `esrgan` | ESRGAN | `infogan` | InfoGAN |

Some examples in the table are grouped by task:

- **Basic GANs and loss variants:** `gan`, `dcgan`, `lsgan`, `wgan`, `wgan_gp`, `wgan_div`, `dragan`, `bgan`, `began`, `ebgan`, `relativistic_gan`, `softmax_gan`
- **Conditional and structured GANs:** `cgan`, `acgan`, `infogan`, `ccgan`, `cluster_gan`, `sgan`
- **Autoencoder-based:** `aae`
- **Image-to-image translation:** `pix2pix`, `cyclegan`, `discogan`, `dualgan`, `unit`, `munit`, `bicyclegan`, `stargan`
- **Domain adaptation:** `cogan`, `pixelda`
- **Image inpainting:** `context_encoder`
- **Super-resolution:** `srgan`, `esrgan`

## Requirements

The dependencies are listed in [requirements.txt](requirements.txt):

- `torch>=0.4.0`
- `torchvision`
- `matplotlib`
- `numpy`
- `scipy`
- `pillow`
- `urllib3`
- `scikit-image`

The repository does not pin exact versions and does not include a test suite or CI configuration, so the compatibility of specific PyTorch or torchvision versions has not been verified here. Some scripts use APIs such as `Variable` and `torch.cuda.FloatTensor`. The code runs on CPU, and it uses CUDA automatically when `torch.cuda.is_available()` returns true.

The dataset download scripts require `wget` and `unzip` (CycleGAN) or `wget` and `tar` (pix2pix).

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Getting started

Clone the repository:

```bash
git clone <repository-url>
cd PyTorch-GAN
pip install -r requirements.txt
```

Scripts write outputs and read datasets using paths relative to the current working directory, so **run each script from its own implementation directory**:

```bash
cd implementations/gan
python gan.py
```

## Downloading datasets

Several models expect datasets in the `data/` directory. Data paths in the scripts are relative to the implementation directory (`../../data/<dataset_name>`), so the datasets are expected at `data/<dataset_name>` in the repository root.

The MNIST-based models (for example, `gan`, `dcgan`, `wgan`) download MNIST automatically into `data/mnist` on first run. `pixelda` and `cogan` also use MNIST-M, which is built from MNIST and downloaded by those scripts.

### CycleGAN datasets

Run from the `data/` directory:

```bash
cd data
bash download_cyclegan_dataset.sh monet2photo
```

Supported names are: `ae_photos`, `apple2orange`, `summer2winter_yosemite`, `horse2zebra`, `monet2photo`, `cezanne2photo`, `ukiyoe2photo`, `vangogh2photo`, `maps`, `cityscapes`, `facades`, and `iphone2dslr_flower`. The script downloads the archive from the CycleGAN project and rearranges it into `train/A`, `train/B`, `test/A`, and `test/B`.

### pix2pix datasets

Run from the `data/` directory:

```bash
cd data
bash download_pix2pix_dataset.sh facades
```

The script downloads the given dataset from the pix2pix project and extracts it into `data/<name>/`. It does not validate names, so pass a dataset name that exists on the pix2pix server. The target directory must not already exist, because the script runs `mkdir` on it.

### Other datasets

- **CelebA (`img_align_celeba`):** used by the `srgan` and `context_encoder` examples. These scripts' comments say to download the `img_align_celeba` folder and place it in `data/`. The dataset is not downloaded automatically.
- **Other models** (for example, `ccgan`, `discogan`, `dualgan`, `munit`, `unit`, `stargan`) read from `data/<dataset_name>`. Check each model's `datasets.py` for the exact folder layout it expects.
- **ESRGAN:** `esrgan.py` loads every file in `data/<dataset_name>` (default `img_align_celeba`) as a high-resolution image.

## Running the examples

Each example prints its options at startup and runs the training loop. Run the examples from their own directories.

### GAN on MNIST

```bash
cd implementations/gan
python gan.py --n_epochs 200 --batch_size 64
```

### CycleGAN

After downloading a dataset into `data/`:

```bash
cd implementations/cyclegan
python cyclegan.py --dataset_name monet2photo
```

Checkpoints are saved under `saved_models/<dataset_name>/` when `--checkpoint_interval` is set to a value other than `-1`. To resume training from a checkpoint, pass the epoch number with `--epoch`.

### ESRGAN (single-image super-resolution)

`test_on_image.py` runs a trained ESRGAN generator on one image:

```bash
cd implementations/esrgan
python test_on_image.py --image_path path/to/image.png --checkpoint_model path/to/generator.pth
```

The output is saved as `images/outputs/sr-<filename>`. The script requires a checkpoint file. The repository does not include pre-trained weights.

## Command-line options

Each training script defines its own options with `argparse`. The defaults are set in each script. For example, `implementations/gan/gan.py` uses:

| Option | Default | Description |
|---|---|---|
| `--n_epochs` | 200 | Number of epochs |
| `--batch_size` | 64 | Batch size |
| `--lr` | 0.0002 | Adam learning rate |
| `--b1` | 0.5 | Adam first-moment decay |
| `--b2` | 0.999 | Adam second-moment decay |
| `--latent_dim` | 100 | Dimension of the latent noise vector |
| `--img_size` | 28 | Image height and width |
| `--channels` | 1 | Number of image channels |
| `--sample_interval` | 400 | Batches between saved sample images |

`implementations/cyclegan/cyclegan.py` has additional options, including `--dataset_name` (default `monet2photo`), `--decay_epoch`, `--img_height`, `--img_width`, `--n_residual_blocks`, `--lambda_cyc`, `--lambda_id`, and `--checkpoint_interval`.

Run any script with `--help` to see its full option list.

## Outputs

Scripts create output directories on startup, relative to the current directory:

- `images/` — sample images written during training (for example, `gan.py` writes 25-image grids every `--sample_interval` batches).
- `images/<dataset_name>/` — sample grids for dataset-based models such as CycleGAN.
- `saved_models/<dataset_name>/` — model checkpoints for dataset-based models such as CycleGAN.

The `assets/` directory contains example images and GIFs for the models (for example, `cyclegan.png`, `gan.gif`). The README displays only `logo.png`.

## Notes

- Each implementation is intended as a compact reference for the model's core ideas. The code is not a benchmarked or production training framework, and this README does not report quantitative results.
- The repository has no automated tests or CI configuration. The scripts have not been verified in this README.
- Some scripts depend on other files in their own directory (`models.py`, `datasets.py`, `utils.py`, `mnistm.py`). Run them from the implementation directory so these imports and the relative data paths resolve.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for the full text.
