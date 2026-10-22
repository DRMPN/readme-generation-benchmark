# PyTorch-GAN

<p align="center">
    <img src="assets/logo.png" width="360">
</p>

A collection of PyTorch implementations of Generative Adversarial Network (GAN) variants presented in research papers.

Model architectures will not always mirror the ones proposed in the papers, but the same functionalities proposed in the papers have been used for all models implemented here. Unless otherwise stated in the corresponding section, every model is implemented and trained on MNIST.

Highlights of the repository:

- **32 GAN architectures** covering generation, conditional generation, semi-supervised learning, image-to-image translation, domain adaptation, super-resolution and inpainting.
- **Single-file implementations** — every model lives in one readable training script (plus a small `datasets.py` and `models.py`).
- **Argparse-driven** — datasets, epochs, batch size, learning rate, latent dimension, image size, etc. are all configurable from the command line.
- **Reproducible outputs** — every script saves generated samples to `images/` and trained weights to `saved_models/` in its own folder.

## Table of Contents

- [Installation](#installation)
- [Datasets](#datasets)
- [Usage](#usage)
- [Generative Adversarial Networks](#generative-adversarial-networks)
  - [GAN](#gan)
  - [DCGAN](#dcgan)
  - [WGAN](#wgan)
  - [WGAN-GP](#wgan-gp)
  - [WGAN-Div](#wgan-div)
  - [LSGAN](#lsgan)
  - [DRAGAN](#dragan)
  - [BGAN](#bgan)
  - [EBGAN](#ebgan)
  - [BEGAN](#began)
  - [Relativistic GAN](#relativistic-gan)
  - [Softmax GAN](#softmax-gan)
- [Conditional & Semi-Supervised GANs](#conditional--semi-supervised-gans)
  - [CGAN](#cgan)
  - [ACGAN](#acgan)
  - [InfoGAN](#infogan)
  - [SGAN](#sgan)
  - [ClusterGAN](#clustergan)
- [Image-to-Image Translation & Domain Adaptation](#image-to-image-translation--domain-adaptation)
  - [Pix2Pix](#pix2pix)
  - [CycleGAN](#cyclegan)
  - [DiscoGAN](#discogan)
  - [DualGAN](#dualgan)
  - [UNIT](#unit)
  - [MUNIT](#munit)
  - [StarGAN](#stargan)
  - [BicycleGAN](#bicyclegan)
  - [PixelDA](#pixelda)
  - [CoGAN](#cogan)
  - [CC-GAN](#cc-gan)
- [Super-Resolution](#super-resolution)
  - [SRGAN](#srgan)
  - [ESRGAN](#esrgan)
- [Image Inpainting](#image-inpainting)
  - [Context Encoder](#context-encoder)
- [Adversarial Autoencoders](#adversarial-autoencoders)
  - [AAE](#aae)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Installation

Requires **Python 3** and **PyTorch 0.4.0+**. Install the dependencies listed in `requirements.txt` (PyTorch, torchvision, NumPy, SciPy, Pillow):

```bash
$ pip install -r requirements.txt
```

All scripts run on CPU or GPU (CUDA is used automatically if available).

## Datasets

- **MNIST / CIFAR-10** — downloaded automatically through `torchvision` the first time a script is run. Most of the models in this repository are trained on MNIST by default.
- **MNIST-M** — the color-blended MNIST variant used for domain adaptation/translation experiments. The helper module `mnistm.py` (shipped with the implementations that need it, e.g. PixelDA and MUNIT) takes care of building/loading it.
- **CelebA** — the aligned & cropped celebrity faces dataset, used by e.g. StarGAN for attribute-conditioned translation. Arrange the images as expected by the loader in the implementation's `datasets.py`.
- **Pix2Pix datasets** (paired) — `facades`, `cityscapes`, `maps`, `edges2shoes`, `edges2handbags`, `night2day`, etc.:

  ```bash
  $ bash data/download_pix2pix_dataset.sh <dataset_name>
  ```

- **CycleGAN datasets** (unpaired) — `horse2zebra`, `monet2photo`, `apple2orange`, `summer2winter_yosemite`, `cezanne2photo`, `ukiyoe2photo`, `vangogh2photo`, `iphone2dslr_flower`, `maps`, `cityscapes`, `facades`, `ae_photos`, etc.:

  ```bash
  $ bash data/download_cyclegan_dataset.sh <dataset_name>
  ```

## Usage

Every implementation is trained by executing its script from within its own directory:

```bash
$ cd implementations/<model_name>/
$ python <model_name>.py
```

The most common command-line options across implementations are:

| Option | Description |
|---|---|
| `--dataset_name` | Dataset to train on (model dependent) |
| `--epochs` | Number of training epochs |
| `--batch_size` | Batch size (defaults vary per model) |
| `--lr`, `--b1`, `--b2` | Optimizer learning rate and Adam betas (typical default: `2e-4`, `0.5`, `0.999`) |
| `--latent_dim` | Dimensionality of the generator input noise vector |
| `--img_size`, `--channels` | Resolution and number of channels of the images |
| `--n_classes` | Number of classes (conditional models) |
| `--sample_interval` | Interval (in batches) between saved sample images |
| `--checkpoint_interval` | Interval (in epochs) between saved model checkpoints |

Run `python <model_name>.py --help` inside any implementation folder to see the full list of options for that model. Generated samples are continuously written to `images/` and model weights to `saved_models/`.

---

## Generative Adversarial Networks

### GAN

[_Generative Adversarial Networks_](https://arxiv.org/abs/1406.2661)

The original GAN (Goodfellow et al., 2014): a generator maps a noise vector `z` to the data space while a discriminator is trained to tell generated samples apart from real ones; the two networks are trained simultaneously in a minimax game. Implemented with fully connected networks on MNIST.

![GAN](assets/gan.gif)

Example:

```bash
$ cd implementations/gan/
$ python gan.py
```

### DCGAN

[_Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks_](https://arxiv.org/abs/1511.06434)

Extends the vanilla GAN with the now-standard convolutional design guidelines: strided/transposed convolutions instead of pooling layers, batch normalization, ReLU in the generator and LeakyReLU in the discriminator.

![DCGAN](assets/dcgan.gif)

Example:

```bash
$ cd implementations/dcgan/
$ python dcgan.py
```

### WGAN

[_Wasserstein GAN_](https://arxiv.org/abs/1701.07875)

Replaces the Jensen-Shannon based objective with an approximation of the Wasserstein-1 (Earth-Mover) distance. The discriminator (critic) is trained towards optimality, and weight clipping is used to enforce the Lipschitz constraint — greatly reducing mode collapse and making the loss curve meaningful.

Example:

```bash
$ cd implementations/wgan/
$ python wgan.py
```

### WGAN-GP

[_Improved Training of Wasserstein GANs_](https://arxiv.org/abs/1704.00028)

Improves WGAN training by replacing weight clipping with a gradient penalty applied at randomly interpolated points between real and generated samples.

![WGAN-GP](assets/wgan_gp.gif)

Example:

```bash
$ cd implementations/wgan_gp/
$ python wgan_gp.py
```

### WGAN-Div

[_Wasserstein Divergence for GANs_](https://arxiv.org/abs/1712.01026)

Introduces the Wasserstein divergence objective with a k-th order derivative penalty (k-Penalty), which requires neither weight clipping nor a gradient penalty while keeping training stable.

![WGAN-Div](assets/wgan_div.gif)

Example:

```bash
$ cd implementations/wgan_div/
$ python wgan_div.py
```

### LSGAN

[_Least Squares Generative Adversarial Networks_](https://arxiv.org/abs/1611.04076)

Replaces the sigmoid cross-entropy adversarial loss with least-squares losses, which corresponds to minimizing the Pearson χ² divergence and yields higher-quality samples and more stable training.

Example:

```bash
$ cd implementations/lsgan/
$ python lsgan.py
```

### DRAGAN

[_On Convergence and Stability of GANs_](https://arxiv.org/abs/1705.07215)

Stabilizes GAN training with a gradient penalty evaluated at points sampled with random noise around the data manifold. The approach is architecture-agnostic and mitigates mode collapse.

Example:

```bash
$ cd implementations/dragan/
$ python dragan.py
```

### BGAN

[_Boundary-Seeking Generative Adversarial Networks_](https://arxiv.org/abs/1702.08431)

Trains the generator to match the decision boundary of a separately trained discriminator. The resulting boundary-seeking objective can also be applied to discrete data.

Example:

```bash
$ cd implementations/bgan/
$ python bgan.py
```

### EBGAN

[_Energy-Based Generative Adversarial Networks_](https://arxiv.org/abs/1609.03126)

The discriminator is an autoencoder whose reconstruction error acts as the energy. Training uses a hinge loss on the margin between the energies of real and generated samples, plus a repelling regularizer that pushes generated samples apart.

Example:

```bash
$ cd implementations/ebgan/
$ python ebgan.py
```

### BEGAN

[_BEGAN: Boundary Equilibrium Generative Adversarial Networks_](https://arxiv.org/abs/1703.10717)

Also uses an autoencoder as the discriminator, but minimizes the Wasserstein distance between the loss distributions of real and generated reconstructions. An equilibrium term (γ) balances the generator and discriminator training and controls the trade-off between image diversity and quality.

Example:

```bash
$ cd implementations/began/
$ python began.py
```

### Relativistic GAN

[_The relativistic discriminator: a key element missing from standard GAN_](https://arxiv.org/abs/1807.00734)

Instead of estimating the probability that a sample is real, the relativistic discriminator estimates the probability that a given real sample is *more real* than a given generated sample. This makes the generator benefit from better discriminators and improves stability and sample quality; the standard GAN is recovered as a special case.

Example:

```bash
$ cd implementations/relativistic_gan/
$ python relativistic_gan.py
```

### Softmax GAN

[_Softmax GAN_](https://arxiv.org/abs/1704.06191)

Reformulates the adversarial minimax game as a single maximum-likelihood problem: a softmax classifier separates N real samples (each treated as its own class) from M generated samples (a single class) using softmax cross-entropy.

Example:

```bash
$ cd implementations/softmax_gan/
$ python softmax_gan.py
```

## Conditional & Semi-Supervised GANs

### CGAN

[_Conditional Generative Adversarial Nets_](https://arxiv.org/abs/1411.1784)

Both the generator and the discriminator are conditioned on the class label (one-hot vector), enabling controllable class-conditional generation.

Example:

```bash
$ cd implementations/cgan/
$ python cgan.py
```

### ACGAN

[_Conditional Image Synthesis With Auxiliary Classifier GANs_](https://arxiv.org/abs/1610.09585)

The discriminator outputs both a real/fake probability and a class distribution, so the generator is trained to produce samples that are simultaneously realistic and correctly classifiable.

![ACGAN](assets/acgan.gif)

Example:

```bash
$ cd implementations/acgan/
$ python acgan.py
```

### InfoGAN

[_Interpretable Representation Learning by Information Maximizing Generative Adversarial Nets_](https://arxiv.org/abs/1606.03657)

Maximizes the mutual information between a compact latent code `c` and the generated samples via a variational lower bound estimated by an auxiliary network `Q`. On MNIST this discovers interpretable factors — digit identity, rotation and stroke width — without any labels. The results show latent-code traversals.

![InfoGAN](assets/infogan.gif)

![InfoGAN](assets/infogan.png)

Example:

```bash
$ cd implementations/infogan/
$ python infogan.py
```

### SGAN

[_Improved Techniques for Training GANs_](https://arxiv.org/abs/1606.03498)

Semi-supervised GAN: the discriminator doubles as a K+1-way classifier (K real classes plus one "generated" class). A small labeled dataset combined with unlabeled data and generated samples substantially improves classification accuracy on MNIST.

Example:

```bash
$ cd implementations/sgan/
$ python sgan.py
```

### ClusterGAN

[_ClusterGAN: Latent Space Clustering in Generative Adversarial Networks_](https://arxiv.org/abs/1809.03627)

Engineers the latent space for clustering by mixing discrete (one-hot) class codes with continuous noise variables and training with an explicit inverse mapping (encoder). Joint clustering and generation is then performed with k-means in the learned latent space.

![ClusterGAN](assets/cluster_gan.gif)

Example:

```bash
$ cd implementations/clustergan/
$ python clustergan.py
```

## Image-to-Image Translation & Domain Adaptation

### Pix2Pix

[_Image-to-Image Translation with Conditional Adversarial Networks_](https://arxiv.org/abs/1611.07004)

Paired image-to-image translation with a U-Net generator (skip connections) and a 70×70 PatchGAN discriminator, trained with a combination of L1 reconstruction and conditional adversarial losses. Works on the Berkeley pix2pix datasets such as `facades`, `edges2shoes`, `edges2handbags`, `maps`, `cityscapes` and `night2day`.

![Pix2Pix](assets/pix2pix.png)

Example:

```bash
$ cd data/
$ bash download_pix2pix_dataset.sh facades
$ cd ../implementations/pix2pix/
$ python pix2pix.py --dataset_name facades
```

### CycleGAN

[_Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks_](https://arxiv.org/abs/1703.10593)

Unpaired image-to-image translation: two generators and two discriminators are tied together by a cycle-consistency loss (this implementation additionally uses an identity mapping loss). Works on the Berkeley CycleGAN datasets such as `horse2zebra`, `monet2photo`, `apple2orange`, `cezanne2photo`, `ukiyoe2photo`, `vangogh2photo`, `summer2winter_yosemite`, `iphone2dslr_flower`, `maps`, `cityscapes`, `facades` and `ae_photos`.

![CycleGAN](assets/cyclegan.png)

Example:

```bash
$ cd data/
$ bash download_cyclegan_dataset.sh monet2photo
$ cd ../implementations/cyclegan/
$ python cyclegan.py --dataset_name monet2photo
```

### DiscoGAN

[_Learning to Discover Cross-Domain Relations with Generative Adversarial Networks_](https://arxiv.org/abs/1703.05192)

Discovers cross-domain relations from unpaired data: each domain has an encoder–decoder pair, and reconstruction losses encourage a representation that is shared across domains (e.g. edges-to-shoes / edges-to-handbags translation).

![DiscoGAN](assets/discogan.png)

Example:

```bash
$ cd implementations/discogan/
$ python discogan.py
```

### DualGAN

[_DualGAN: Unsupervised Dual Learning for Image-to-Image Translation_](https://arxiv.org/abs/1704.02510)

Unsupervised image-to-image translation based on dual learning: two complementary GANs translate between the two domains, and reconstruction constraints make each network's outputs consistent with the other's inputs.

Example:

```bash
$ cd implementations/dualgan/
$ python dualgan.py
```

### UNIT

[_Unsupervised Image-to-Image Translation Networks_](https://arxiv.org/abs/1703.00848)

Two VAE-GANs whose encoders and decoders are partially weight-shared, forcing a shared latent space between the two domains and enabling unpaired image-to-image translation.

Example:

```bash
$ cd data/
$ bash download_cyclegan_dataset.sh facades
$ cd ../implementations/unit/
$ python unit.py --dataset_name facades
```

### MUNIT

[_Multimodal Unsupervised Image-to-Image Translation_](https://arxiv.org/abs/1804.04732)

Disentangles content and style: content codes are shared across domains while style codes capture domain-specific appearance. Recombining a content code with randomly sampled style codes produces multimodal translations. This implementation can train on MNIST ↔ MNIST-M (see the bundled `mnistm.py`) or other translation datasets selected via `--dataset_name`.

![MUNIT](assets/munit.png)

Example:

```bash
$ cd implementations/munit/
$ python munit.py
```

### StarGAN

[_StarGAN: Unified Generative Adversarial Networks for Multi-Domain Image-to-Image Translation_](https://arxiv.org/abs/1711.09020)

A single generator performs image-to-image translation for multiple domains: the target domain label is fed to the generator, the discriminator contains an auxiliary domain classifier, and a cycle-consistency (reconstruction) loss preserves content. Trained on CelebA attributes (e.g. hair color, gender, age).

![StarGAN](assets/stargan.png)

Example:

```bash
$ cd implementations/stargan/
$ python stargan.py
```

### BicycleGAN

[_Toward Multimodal Image-to-Image Translation_](https://arxiv.org/abs/1711.11586)

Multimodal *paired* image-to-image translation: combines a conditional VAE-GAN with a latent-regressed GAN so that generated outputs remain consistent with the sampled latent code. Trained on the pix2pix datasets (e.g. `edges2shoes`). The bundled `test_on_image.py` generates the multiple translations shown below from a single input image using saved weights.

![BicycleGAN](assets/bicyclegan.png)

![BicycleGAN architecture](assets/bicyclegan_architecture.jpg)

Example:

```bash
$ cd data/
$ bash download_pix2pix_dataset.sh edges2shoes
$ cd ../implementations/bicyclegan/
$ python bicyclegan.py --dataset_name edges2shoes
```

### PixelDA

[_Unsupervised Pixel-Level Domain Adaptation with Generative Adversarial Networks_](https://arxiv.org/abs/1612.05424)

Pixel-level domain adaptation: the generator re-renders images from the labeled source domain (MNIST) in the style of the unlabeled target domain (MNIST-M) while preserving the task label, so that a classifier trained on the source can generalize to the target. See the bundled `mnistm.py` for the MNIST-M dataset.

![PixelDA](assets/pixelda.png)

Example:

```bash
$ cd implementations/pixelda/
$ python pixelda.py
```

### CoGAN

[_Coupled Generative Adversarial Networks_](https://arxiv.org/abs/1606.07536)

Coupled GANs: two generators share their upstream (high-level) weights so that the same latent vector produces corresponding images in two domains, learning the joint distribution of the domains from unpaired data.

![CoGAN](assets/cogan.gif)

Example:

```bash
$ cd implementations/cogan/
$ python cogan.py
```

### CC-GAN

[_Compositional GAN: Learning Image-Conditional Binary Distribution_](https://arxiv.org/abs/1709.07271)

Learns to compose a given object image into a given scene image (e.g. adding glasses or a mustache to a face) using a pair of generative models trained adversarially.

Example:

```bash
$ cd implementations/ccgan/
$ python ccgan.py
```

## Super-Resolution

### SRGAN

[_Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network_](https://arxiv.org/abs/1609.04802)

Single-image 4× super-resolution. A content loss computed on VGG feature maps is combined with an adversarial loss, recovering photo-realistic detail that purely MSE-optimized networks tend to miss.

![SRGAN](assets/superresgan.png)

Example:

```bash
$ cd implementations/srgan/
$ python srgan.py
```

### ESRGAN

[_ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks_](https://arxiv.org/abs/1809.00219)

Enhanced SRGAN: residual-in-residual dense blocks (RRDB) without batch normalization, a relativistic discriminator and an improved perceptual loss, yielding substantially better texture fidelity than SRGAN.

![ESRGAN](assets/enhanced_superresgan.png)

![ESRGAN](assets/esrgan.png)

Example:

```bash
$ cd implementations/esrgan/
$ python esrgan.py
```

## Image Inpainting

### Context Encoder

[_Context Encoders: Feature Learning by Inpainting_](https://arxiv.org/abs/1604.07379)

Semantic inpainting: a channel-wise fully-connected encoder–decoder network predicts the content of a masked-out region of an image, trained with a combination of reconstruction (L2) and adversarial losses.

![Context Encoder](assets/context_encoder.png)

Example:

```bash
$ cd implementations/context_encoder/
$ python context_encoder.py
```

## Adversarial Autoencoders

### AAE

[_Adversarial Autoencoders_](https://arxiv.org/abs/1511.05644)

An autoencoder whose aggregated posterior q(z) is forced to match an arbitrary prior p(z) through an adversarially trained discriminator. Supports unsupervised, semi-supervised and supervised (label-conditioned) representation learning.

Example:

```bash
$ cd implementations/aae/
$ python aae.py
```

## Project Structure

```bash
.
├── LICENSE
├── README.md
├── requirements.txt
├── data/
│   ├── download_cyclegan_dataset.sh     # downloads a CycleGAN dataset archive
│   └── download_pix2pix_dataset.sh      # downloads a Pix2Pix dataset archive
├── assets/                              # result images & animations embedded in this README
│   ├── logo.png
│   ├── gan.gif
│   ├── dcgan.gif
│   └── ...
└── implementations/
    ├── gan/
    │   ├── gan.py                       # self-contained training script
    │   ├── datasets.py                  # dataset loading
    │   └── models.py                    # generator / discriminator definitions
    ├── dcgan/
    │   ├── dcgan.py
    │   ├── datasets.py
    │   └── models.py
    ├── ...                              # 32 model folders in total
    └── wgan_gp/
        ├── wgan_gp.py
        ├── datasets.py
        └── models.py
```

Notes on the layout:

- Every implementation folder contains the model's training script plus `datasets.py` (data loading) and `models.py` (network definitions).
- Some implementations ship additional helpers, e.g. `mnistm.py` (MNIST-M dataset, used by PixelDA and MUNIT), `test_on_image.py` (single-image inference, used by BicycleGAN) and `utils.py` (shared training utilities).
- Running a script creates `images/` (sample outputs) and `saved_models/` (checkpoints) inside that implementation's folder. Trained weights are not distributed with the repository — run the scripts to reproduce the results.

## Contributing

Contributions are welcome! To add a new GAN implementation:

1. Create a folder under `implementations/<model_name>/` containing a single training script plus `datasets.py` and `models.py`, following the style of the existing implementations.
2. Make the model configurable via `argparse` and save samples/checkpoints to `images/` and `saved_models/`.
3. Add a section to this README with the paper title, an [arXiv] link, a short description, an example command and — if possible — a result image or GIF in `assets/`.
4. Submit a pull request.

Bug reports and fixes for existing implementations are equally appreciated.

## License

This repository is released under the MIT license — see [LICENSE](LICENSE).

## Acknowledgements

All credit for the ideas and research goes to the authors of the papers cited throughout this README. The reference implementations in this collection were originally written by Erik Linder-Noren. If you prefer Keras, the companion repository [Keras-GAN](https://github.com/eriklindernoren/Keras-GAN) contains many of the same models implemented in Keras.
