# README

## PyTorch-GAN

A collection of standalone PyTorch implementations of generative adversarial networks (GANs) and related methods for image generation, image-to-image translation, domain adaptation, and super-resolution.

Each implementation demonstrates a particular model or training objective. This is not a single unified training framework: command-line options, dataset formats, checkpoints, and output locations may differ between implementations.

## Contents

- [Implementations](#implementations)
- [Repository layout](#repository-layout)
- [Requirements and setup](#requirements-and-setup)
- [Running an implementation](#running-an-implementation)
- [Datasets](#datasets)
- [Results and images](#results-and-images)
- [Notes](#notes)
- [License](#license)

## Implementations

| Implementation | Summary |
|---|---|
| `gan.py` | A basic GAN using the original adversarial training formulation. |
| `dcgan.py` | Deep Convolutional GAN for image generation. |
| `cgan.py` | Conditional GAN, which conditions generation on a class or other label. |
| `acgan.py` | Auxiliary Classifier GAN; the discriminator also predicts class labels. |
| `sgan.py` | Semi-supervised GAN with a discriminator that classifies real examples as well as distinguishing generated examples. |
| `infogan.py` | InfoGAN, which encourages interpretable latent codes through mutual-information regularization. |
| `aae.py` | Adversarial Autoencoder, using an adversarial objective to regularize the latent distribution. |
| `bgan.py` | Boundary-Seeking GAN. |
| `began.py` | Boundary Equilibrium GAN. |
| `ebgan.py` | Energy-Based GAN. |
| `lsgan.py` | Least Squares GAN. |
| `relativistic_gan.py` | Relativistic GAN objective, which compares real and generated samples. |
| `softmax_gan.py` | GAN variant using a softmax-based adversarial objective. |
| `wgan.py` | Wasserstein GAN. |
| `wgan_gp.py` | Wasserstein GAN with gradient penalty. |
| `wgan_div.py` | Wasserstein divergence GAN. |
| `dragan.py` | DRAGAN, using a gradient penalty around real data. |
| `clustergan.py` | ClusterGAN, combining generation with a structured, cluster-oriented latent representation. |
| `bicyclegan.py` | BicycleGAN for multimodal, paired image-to-image translation. |
| `pix2pix.py` | Conditional paired image-to-image translation. |
| `cyclegan.py` | Unpaired image-to-image translation with cycle consistency. |
| `dualgan.py` | DualGAN, an approach to unpaired image-to-image translation. |
| `discogan.py` | DiscoGAN, for learning mappings between image domains. |
| `unit.py` | UNIT, an unsupervised image-to-image translation model using a shared latent space. |
| `munit.py` | MUNIT, for multimodal unsupervised image-to-image translation. |
| `cogan.py` | Coupled GANs for learning across related domains. |
| `stargan.py` | StarGAN for multi-domain image translation, including attribute-conditioned translation. |
| `context_encoder.py` | Context Encoder for image inpainting and contextual image generation. |
| `pixelda.py` | Pixel-level domain adaptation using adversarial image translation. |
| `mnistm.py` | MNIST-M-related domain adaptation example. |
| `srgan.py` | Super-Resolution GAN for image upscaling. |
| `esrgan.py` | Enhanced SRGAN for perceptual image super-resolution. |
| `ccgan.py` | CcGAN implementation; consult its source and arguments for the conditioning setup used here. |

Many implementations have their own `models.py` and/or `datasets.py`. These files are specific to their implementation rather than part of a shared model or dataset API.

The repository also includes `test_on_image.py`, a utility script for running an image-related test or inference workflow. Check its source for the required arguments and expected inputs.

## Repository layout

Repeated filenames in the repository listing, such as `models.py` and `datasets.py`, belong to different implementation directories. A typical layout is:

```text
.
├── implementations/
│   ├── dcgan/
│   │   ├── dcgan.py
│   │   ├── models.py
│   │   └── datasets.py
│   ├── pix2pix/
│   │   ├── pix2pix.py
│   │   ├── models.py
│   │   └── datasets.py
│   └── ...
├── download_pix2pix_dataset.sh
├── download_cyclegan_dataset.sh
├── requirements.txt
└── LICENSE
```

If your checkout uses a different directory layout, substitute the actual path to the implementation you want to run.

## Requirements and setup

You will need:

- Python 3
- PyTorch
- The additional packages listed in `requirements.txt`
- Optionally, a CUDA-capable GPU for faster training

Install the dependencies from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the installed PyTorch build is not suitable for your operating system or CUDA version, install an appropriate build using the [official PyTorch installation guide](https://pytorch.org/get-started/locally/).

## Running an implementation

Implementations are run independently. For example:

```bash
cd implementations/dcgan
python dcgan.py
```

To run another model, change to its directory and execute its script:

```bash
cd implementations/cyclegan
python cyclegan.py
```

Many scripts accept command-line arguments for settings such as the dataset, number of epochs, batch size, learning rate, image size, and sampling interval. Where supported, display the available options with:

```bash
python dcgan.py --help
```

Not all scripts necessarily expose the same options or implement `--help`. If needed, inspect the script’s argument parser and configuration near the top of the file. Run scripts from the directory they expect: some use relative paths for datasets, saved images, or checkpoints.

## Datasets

Dataset requirements vary by implementation:

- Some examples use built-in datasets and may download them automatically.
- Image-to-image translation models may require paired or unpaired images arranged in a particular directory structure.
- Other examples may expect you to provide or configure the data yourself.

The repository includes helper scripts for Pix2Pix and CycleGAN datasets:

```bash
bash download_pix2pix_dataset.sh
bash download_cyclegan_dataset.sh
```

Review each script before running it to confirm which dataset it downloads and where it saves the files. Check the corresponding implementation’s `datasets.py`, if present, for the expected directory structure and preprocessing steps.

Dataset providers may impose their own licensing or usage conditions. Check those terms before downloading or using a dataset.

## Results and images

The repository includes visualizations and architecture illustrations for selected implementations, including:

- `gan.gif`, `dcgan.gif`, and `infogan.gif`
- `cyclegan.png`, `pix2pix.png`, `bicyclegan.png`, and `bicyclegan_architecture.jpg`
- `stargan.png`, `munit.png`, and `context_encoder.png`
- `srgan.png`, `esrgan.png`, and `enhanced_superresgan.png`
- `wgan_div.png` and `wgan_div.gif`
- `acgan.gif`, `cgan.gif`, `cogan.gif`, `cluster_gan.gif`, and `wgan_gp.gif`

These files illustrate selected methods or example results; they do not guarantee that a fresh training run will reproduce the same output. Results depend on the dataset, hardware, random seed, and hyperparameters.

## Notes

- GAN training can be sensitive to hyperparameters and may be unstable. A completed training run does not necessarily imply that generated samples will be high quality.
- This is a collection of research-oriented examples, not a production-ready package. Review an implementation’s code, configuration, and data requirements before using it.
- Model behavior and training options may differ between implementations; there is no shared command-line interface across the repository.

## License

See [`LICENSE`](LICENSE) for the licensing terms of this repository. Third-party datasets may have separate licenses and usage conditions.
