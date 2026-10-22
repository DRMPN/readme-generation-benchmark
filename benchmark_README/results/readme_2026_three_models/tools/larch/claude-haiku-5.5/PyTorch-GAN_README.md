# PyTorch-GAN

![Logo](logo.png)

A collection of PyTorch implementations of Generative Adversarial Networks (GANs) and related generative models, each derived from a research paper. The implementations are designed to be readable and self-contained, so you can study how each variant works, run it on common datasets, and adapt it for your own experiments.

> **Note:** The architectures are intentionally simple and are not optimized for state-of-the-art results. Their purpose is educational and as a starting point for experimentation.

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Implemented Models](#implemented-models)
- [Installation](#installation)
- [Datasets](#datasets)
- [Usage](#usage)
- [Example Outputs](#example-outputs)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

---

## Overview

Generative Adversarial Networks consist of two neural networks trained against each other:

- **Generator (G):** Takes a noise vector (or an input image, depending on the variant) and produces synthetic samples.
- **Discriminator (D):** Tries to distinguish real samples from generated ones.

Training is a minimax game in which G learns to produce samples that fool D, while D learns to get better at detecting fakes. This repository implements many variations of this idea, including conditional models, Wasserstein-based losses, image-to-image translation, super-resolution, and unsupervised domain adaptation.

Each model is provided as a single script that can be run directly. Most scripts:

- Train on a standard dataset (usually MNIST, or a dataset downloaded via the provided shell scripts).
- Periodically save sample images to an `images/` directory, creating it if necessary.
- Print losses during training so you can monitor progress.

---

## Repository Structure

The repository is organized as one folder per model. Most folders contain the following:

```
implementations/<model_name>/
├── <model_name>.py   # Training script: model setup, training loop, sampling
├── models.py         # Generator and discriminator (and other network) definitions
└── datasets.py       # Dataset loading and preprocessing
```

Some implementations include additional files:

- `test_on_image.py`: runs a trained model on a single input image (used by the pix2pix implementation).
- `utils.py`: shared helper functions for certain models.
- `mnistm.py`: a loader for the MNIST-M dataset, used by domain adaptation models such as PixelDA, CoGAN, and DualGAN.

### Top-Level Files

| File | Description |
|------|-------------|
| `download_pix2pix_dataset.sh` | Downloads paired image-to-image datasets for Pix2Pix and related models |
| `download_cyclegan_dataset.sh` | Downloads unpaired image datasets for CycleGAN and related models |
| `requirements.txt` | Python dependencies |
| `LICENSE` | Project license |
| `*.gif`, `*.png`, `*.jpg` | Result visualizations and architecture diagrams used in the documentation |

---

## Implemented Models

The table below lists the models included in this repository, grouped by category.

### Foundational and Core GANs

| Model | Script | Description |
|-------|--------|-------------|
| **GAN** | `gan.py` | The original vanilla GAN with fully connected networks |
| **DCGAN** | `dcgan.py` | Deep convolutional GAN with architectural guidelines for stable training |
| **Adversarial Autoencoder (AAE)** | `aae.py` | Combines an autoencoder with an adversarial prior on the latent space |
| **Boundary-Seeking GAN (BGAN)** | `bgan.py` | Uses a boundary-seeking objective for discrete data generation |

### Conditional and Controllable GANs

| Model | Script | Description |
|-------|--------|-------------|
| **CGAN** | `cgan.py` | Conditional GAN that conditions generation on class labels |
| **ACGAN** | `acgan.py` | Auxiliary classifier GAN, where D also predicts the class label |
| **InfoGAN** | `infogan.py` | Learns disentangled, interpretable latent codes via mutual information maximization |
| **ClusterGAN** | `clustergan.py` | Learns clustering in the latent space of a GAN |
| **Context Encoder** | `context_encoder.py` | Learns to inpaint missing image regions from surrounding context |
| **CCGAN** | `ccgan.py` | Context-conditional GAN for image inpainting |
| **Semi-supervised GAN (SGAN)** | `sgan.py` | Uses GAN training to improve classification with limited labels |

### Loss Function and Training Stability Variants

| Model | Script | Description |
|-------|--------|-------------|
| **LSGAN** | `lsgan.py` | Least-squares loss to reduce vanishing gradients |
| **WGAN** | `wgan.py` | Wasserstein GAN with weight clipping |
| **WGAN-GP** | `wgan_gp.py` | WGAN with gradient penalty instead of weight clipping |
| **WGAN-DIV** | `wgan_div.py` | WGAN with a Wasserstein divergence objective |
| **BEGAN** | `began.py` | Boundary Equilibrium GAN, balancing generator and discriminator |
| **EBGAN** | `ebgan.py` | Energy-based GAN, where D acts as an energy function |
| **DRAGAN** | `dragan.py` | Regularizes the discriminator to reduce mode collapse |
| **Relativistic GAN** | `relativistic_gan.py` | Estimates the probability that real data is more realistic than fake data |
| **Softmax GAN** | `softmax_gan.py` | Uses a softmax-based formulation of the GAN objective |

### Image-to-Image Translation

| Model | Script | Description |
|-------|--------|-------------|
| **Pix2Pix** | `pix2pix.py` | Paired image-to-image translation using a conditional GAN |
| **CycleGAN** | `cyclegan.py` | Unpaired image-to-image translation using cycle-consistency loss |
| **BicycleGAN** | `bicyclegan.py` | Multimodal paired image-to-image translation |
| **DiscoGAN** | `discogan.py` | Unpaired image translation for cross-domain discovery |
| **DualGAN** | `dualgan.py` | Unpaired image translation using dual learning |
| **UNIT** | `unit.py` | Unsupervised image-to-image translation with a shared latent space |
| **MUNIT** | `munit.py` | Multimodal unsupervised image-to-image translation |
| **StarGAN** | `stargan.py` | Multi-domain image translation with a single generator |

### Multi-Domain and Domain Adaptation

| Model | Script | Description |
|-------|--------|-------------|
| **CoGAN** | `cogan.py` | Coupled GANs that learn joint distributions across domains |
| **PixelDA** | `pixelda.py` | Pixel-level domain adaptation |

### Super-Resolution

| Model | Script | Description |
|-------|--------|-------------|
| **SRGAN** | `srgan.py` | Photo-realistic single-image super-resolution |
| **ESRGAN** | `esrgan.py` | Enhanced SRGAN with improved architecture and losses |
| **SuperresGAN** | `superresgan.py` | Super-resolution GAN implementation |

---

## Installation

### Prerequisites

- Python 3.6 or newer (3.8+ recommended)
- pip
- A CUDA-capable GPU is strongly recommended for training, though most models can run on CPU for small experiments.

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/eriklindernoren/PyTorch-GAN.git
   cd PyTorch-GAN
   ```

2. **(Optional) Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Install a PyTorch build that matches your CUDA version by following the instructions at [pytorch.org](https://pytorch.org) if the default installation does not include GPU support.

---

## Datasets

### MNIST and Other Built-in Datasets

Many implementations (e.g., GAN, DCGAN, WGAN-GP, InfoGAN) use MNIST, which is downloaded automatically through `torchvision.datasets` the first time the script runs.

### Paired Datasets (Pix2Pix, BicycleGAN)

Use the provided script to download paired image datasets:

```bash
bash download_pix2pix_dataset.sh <dataset_name>
```

Commonly used datasets include:

| Dataset Name | Description |
|--------------|-------------|
| `facades` | Building facade labels and photos |
| `maps` | Satellite images and corresponding maps |
| `edges2shoes` | Shoe edge sketches and photographs |
| `edges2handbags` | Handbag edge sketches and photographs |
| `cityscapes` | Street scene labels and photographs |

### Unpaired Datasets (CycleGAN, DiscoGAN, DualGAN, UNIT, MUNIT)

Use the provided script:

```bash
bash download_cyclegan_dataset.sh <dataset_name>
```

Commonly used datasets include:

| Dataset Name | Description |
|--------------|-------------|
| `apple2orange` | Apples and oranges |
| `horse2zebra` | Horses and zebras |
| `monet2photo` | Monet paintings and photographs |
| `summer2winter_yosemite` | Yosemite in summer and winter |
| `vangogh2photo` | Van Gogh paintings and photographs |

### Expected Directory Layout

Dataset loaders in `datasets.py` generally expect data in a directory relative to the implementation folder, such as:

```
data/
└── <dataset_name>/
    ├── train/
    └── test/
```

Some scripts use `../../data/<dataset_name>`. Check the `datasets.py` file in the relevant implementation folder if you encounter path errors.

### Domain Adaptation Data (MNIST-M)

Models such as CoGAN, PixelDA, and DualGAN use MNIST-M, which is loaded via `mnistm.py`. This is generated by blending MNIST digits with background patches and is handled automatically by the loader.

---

## Usage

### Running a Model

Navigate to the implementation folder and run the main script:

```bash
cd implementations/dcgan
python3 dcgan.py
```

Or run it from the repository root:

```bash
python3 implementations/dcgan/dcgan.py
```

### Common Command-Line Options

Most scripts use `argparse` and accept options such as:

| Option | Typical Default | Description |
|--------|-----------------|-------------|
| `--n_epochs` | 200 | Number of training epochs |
| `--batch_size` | 64 | Mini-batch size |
| `--lr` | 0.0002 | Learning rate |
| `--b1` | 0.5 | Adam beta1 |
| `--b2` | 0.999 | Adam beta2 |
| `--n_cpu` | 8 | Number of data-loading workers |
| `--latent_dim` | 100 | Dimension of the latent noise vector |
| `--img_size` | 32 | Input image size |
| `--channels` | 1 | Number of image channels |
| `--sample_interval` | 400 | Iterations between saving sample images |

Check each script's `parser.add_argument(...)` calls for the exact options available. Run the following to view them:

```bash
python3 <model_name>.py --help
```

### Example: Training WGAN-GP

```bash
cd implementations/wgan_gp
python3 wgan_gp.py --n_epochs 200 --batch_size 64 --lr 0.0001
```

### Example: Training CycleGAN

After downloading the dataset:

```bash
bash download_cyclegan_dataset.sh horse2zebra
cd implementations/cyclegan
python3 cyclegan.py --dataset_name horse2zebra --n_epochs 200
```

### Example: Pix2Pix with Testing

```bash
bash download_pix2pix_dataset.sh facades
cd implementations/pix2pix
python3 pix2pix.py --dataset_name facades
python3 test_on_image.py --dataset_name facades
```

### Output

During training, scripts typically:

- Print discriminator and generator losses to the console.
- Save generated sample grids to `images/` (for example, `images/<iteration>.png`).
- In some scripts, save model checkpoints to `saved_models/`.

---

## Example Outputs

The repository includes visualizations of results for many models, stored in the root directory:

| Model | Visualization |
|-------|---------------|
| GAN | `gan.gif` |
| DCGAN | `dcgan.gif` |
| WGAN-GP | `wgan_gp.gif` |
| WGAN-DIV | `wgan_div.gif`, `wgan_div.png` |
| InfoGAN | `infogan.gif`, `infogan.png` |
| ACGAN | `acgan.gif` |
| CGAN | `cgan.gif` |
| CoGAN | `cogan.gif` |
| ClusterGAN | `cluster_gan.gif` |
| Pix2Pix | `pix2pix.png` |
| CycleGAN | `cyclegan.png` |
| BicycleGAN | `bicyclegan.png`, `bicyclegan_architecture.jpg` |
| DiscoGAN | `discogan.png` |
| StarGAN | `stargan.png` |
| MUNIT | `munit.png` |
| Context Encoder | `context_encoder.png` |
| PixelDA | `pixelda.png` |
| SRGAN / SuperresGAN | `superresgan.png`, `enhanced_superresgan.png` |
| ESRGAN | `esrgan.png` |

Some visualizations are shown as animated GIFs, which illustrate how generated samples improve over the course of training.

---

## Customization

The modular structure makes it straightforward to adapt existing models.

### Changing the Architecture

Edit `models.py` in the relevant implementation folder. For example, to add a layer to the generator in DCGAN, modify the `Generator` class in `implementations/dcgan/models.py`.

### Using a Custom Dataset

1. Open the implementation's `datasets.py`.
2. Add or modify a `Dataset` class that returns tensors normalized to the range the model expects (commonly `[-1, 1]` for GANs with `tanh` outputs).
3. Update the `DataLoader` call in the main script to use your dataset.
4. Set `--img_size` and `--channels` to match your data.

### Changing the Loss Function

Most scripts compute losses inline in the training loop. To switch variants, modify the loss definitions in the main script. For example, to move from the standard GAN loss to least-squares, replace `BCELoss` with `MSELoss` as done in `lsgan.py`.

---

## Troubleshooting

| Problem | Possible Cause and Solution |
|---------|------------------------------|
| `FileNotFoundError` for dataset | The dataset has not been downloaded. Run the appropriate `download_*_dataset.sh` script, and verify the path in `datasets.py`. |
| CUDA out of memory | Reduce `--batch_size` or `--img_size`. |
| Generated images are all noise or collapse to one mode | Lower the learning rate, check normalization, or try a more stable variant such as WGAN-GP or LSGAN. |
| Discriminator loss goes to zero | The discriminator is overpowering the generator. Adjust the learning rate ratio or use a Wasserstein-based loss. |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in your active environment. |
| Shell scripts fail on Windows | Run them with Git Bash, WSL, or another Bash-compatible shell. |
| Images not saved | Confirm that the script has write permission in the current directory. The `images/` folder is created automatically in most scripts. |

---

## Contributing

Contributions are welcome. To add a new GAN implementation:

1. Create a folder under the appropriate location with the model name.
2. Include `<model_name>.py`, `models.py`, and `datasets.py`, following the conventions of existing implementations.
3. Use `argparse` for configurable hyperparameters, and save sample images to `images/`.
4. Keep the code readable and focused on the model's core ideas.
5. Open a pull request with a brief description of the paper being implemented and any results.

Bug reports and suggestions for improvement are also appreciated through the issue tracker.

---

## License

This project is distributed under the terms of the license found in the [LICENSE](LICENSE) file in the repository root.

---

## References

Each implementation is based on a published paper. Some of the key papers include:

- Goodfellow et al., *Generative Adversarial Nets* (2014)
- Radford et al., *Unsupervised Representation Learning with Deep Convolutional GANs* (2015)
- Mirza and Osindero, *Conditional Generative Adversarial Nets* (2014)
- Chen et al., *InfoGAN: Interpretable Representation Learning by Information Maximizing GANs* (2016)
- Odena et al., *Conditional Image Synthesis with Auxiliary Classifier GANs* (2016)
- Arjovsky et al., *Wasserstein GAN* (2017)
- Gulrajani et al., *Improved Training of Wasserstein GANs* (2017)
- Mao et al., *Least Squares Generative Adversarial Networks* (2016)
- Isola et al., *Image-to-Image Translation with Conditional Adversarial Networks* (2016)
- Zhu et al., *Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks* (2017)
- Ledig et al., *Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network* (2016)
- Wang et al., *ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks* (2018)
- Choi et al., *StarGAN: Unified Generative Adversarial Networks for Multi-Domain Image-to-Image Translation* (2018)
- Huang et al., *Multimodal Unsupervised Image-to-Image Translation* (2018)

For the complete list of papers and their links, refer to the documentation within each implementation folder or the original repository.

---

*If you find this repository useful, consider starring it and citing the relevant original papers in your work.*
