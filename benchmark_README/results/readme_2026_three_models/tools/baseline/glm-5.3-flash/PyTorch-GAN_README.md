# PyTorch-GAN

A collection of standalone PyTorch implementations of generative adversarial network (GAN) variants. Every model is implemented as a self-contained script that reproduces the architecture, loss functions, and training procedure described in its original paper, making the repository a practical reference for reading, comparing, and extending GAN models. Loss logging, image sampling, and (where supported) model checkpointing are provided out of the box for each implementation.

## Implementations

| GAN | Paper | Implementation |
| --- | --- | --- |
| AAE | [Adversarial Autoencoders](https://arxiv.org/abs/1511.05644) | `implementations/aae/aae.py` |
| AC-GAN | [Conditional Image Synthesis With Auxiliary Classifier GANs](https://arxiv.org/abs/1610.09585) | `implementations/acgan/acgan.py` |
| BEGAN | [BEGAN: Boundary Equilibrium Generative Adversarial Networks](https://arxiv.org/abs/1703.10717) | `implementations/began/began.py` |
| BGAN | [Boundary-Seeking Generative Adversarial Networks](https://arxiv.org/abs/1702.08431) | `implementations/bgan/bgan.py` |
| BicycleGAN | [Toward Multimodal Image-to-Image Translation](https://arxiv.org/abs/1711.11586) | `implementations/bicyclegan/bicyclegan.py` |
| CCGAN | [Semi-Supervised Learning with Context-Conditional Generative Adversarial Networks](https://arxiv.org/abs/1611.06430) | `implementations/ccgan/ccgan.py` |
| CGAN | [Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784) | `implementations/cgan/cgan.py` |
| ClusterGAN | [ClusterGAN: Latent Space Clustering in Generative Adversarial Networks](https://arxiv.org/abs/1809.03627) | `implementations/cluster_gan/clustergan.py` |
| CoGAN | [Coupled Generative Adversarial Networks](https://arxiv.org/abs/1606.07536) | `implementations/cogan/cogan.py` |
| Context Encoder | [Context Encoders: Feature Learning by Inpainting](https://arxiv.org/abs/1604.07379) | `implementations/context_encoder/context_encoder.py` |
| CycleGAN | [Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks](https://arxiv.org/abs/1703.10593) | `implementations/cyclegan/cyclegan.py` |
| DCGAN | [Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks](https://arxiv.org/abs/1511.06434) | `implementations/dcgan/dcgan.py` |
| DiscoGAN | [Learning to Discover Cross-Domain Relations with Generative Adversarial Networks](https://arxiv.org/abs/1703.05192) | `implementations/discogan/discogan.py` |
| DRAGAN | [How to Train Your DRAGAN](https://arxiv.org/abs/1705.07215) | `implementations/dragan/dragan.py` |
| DualGAN | [DualGAN: Unsupervised Dual Learning for Image-to-Image Translation](https://arxiv.org/abs/1704.02510) | `implementations/dualgan/dualgan.py` |
| EBGAN | [Energy-based Generative Adversarial Network](https://arxiv.org/abs/1609.03126) | `implementations/ebgan/ebgan.py` |
| ESRGAN | [ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks](https://arxiv.org/abs/1809.00219) | `implementations/esrgan/esrgan.py` |
| GAN | [Generative Adversarial Networks](https://arxiv.org/abs/1406.2661) | `implementations/gan/gan.py` |
| InfoGAN | [InfoGAN: Interpretable Representation Learning by Information Maximizing Generative Adversarial Nets](https://arxiv.org/abs/1606.03657) | `implementations/infogan/infogan.py` |
| LSGAN | [Least Squares Generative Adversarial Networks](https://arxiv.org/abs/1611.04076) | `implementations/lsgan/lsgan.py` |
| MUNIT | [Multimodal Unsupervised Image-to-Image Translation](https://arxiv.org/abs/1804.04732) | `implementations/munit/munit.py` |
| Pix2Pix | [Image-to-Image Translation with Conditional Adversarial Networks](https://arxiv.org/abs/1611.07004) | `implementations/pix2pix/pix2pix.py` |
| PixelDA | [Unsupervised Pixel-Level Domain Adaptation with Generative Adversarial Networks](https://arxiv.org/abs/1612.05424) | `implementations/pixelda/pixelda.py` |
| Relativistic GAN | [Relativistic Generative Adversarial Networks](https://arxiv.org/abs/1807.00734) | `implementations/relativistic_gan/relativistic_gan.py` |
| SGAN | [Semi-Supervised Learning with Generative Adversarial Networks](https://arxiv.org/abs/1606.01583) | `implementations/sgan/sgan.py` |
| Softmax-GAN | [Softmax GAN](https://arxiv.org/abs/1704.06191) | `implementations/softmax_gan/softmax_gan.py` |
| SRGAN | [Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network](https://arxiv.org/abs/1609.04802) | `implementations/srgan/srgan.py` |
| StarGAN | [StarGAN: Unified Generative Adversarial Networks for Multi-Domain Image-to-Image Translation](https://arxiv.org/abs/1711.09020) | `implementations/stargan/stargan.py` |
| UNIT | [UNIT: UNsupervised Image-to-image Translation Networks](https://arxiv.org/abs/1703.00848) | `implementations/unit/unit.py` |
| WGAN | [Wasserstein GAN](https://arxiv.org/abs/1701.07875) | `implementations/wgan/wgan.py` |
| WGAN-GP | [Improved Training of Wasserstein GANs](https://arxiv.org/abs/1704.00028) | `implementations/wgan_gp/wgan_gp.py` |
| WGAN-DIV | [Wasserstein Divergence for GANs](https://arxiv.org/abs/1712.01026) | `implementations/wgan_div/wgan_div.py` |

The implementations fall into three rough groups:

- **Unconditional and conditional image generation** (`aae`, `acgan`, `began`, `bgan`, `cgan`, `cluster_gan`, `cogan`, `dcgan`, `dragan`, `ebgan`, `gan`, `infogan`, `lsgan`, `relativistic_gan`, `sgan`, `softmax_gan`, `wgan`, `wgan_gp`, `wgan_div`) — most train on MNIST, which is downloaded automatically on first run; `cogan` and `pixelda` additionally use MNIST-M, handled by a bundled `mnistm.py` dataset module.
- **Image-to-image translation and inpainting** (`bicyclegan`, `ccgan`, `context_encoder`, `cyclegan`, `discogan`, `dualgan`, `munit`, `pix2pix`, `pixelda`, `stargan`, `unit`) — expect paired or unpaired domain datasets under the repository's `data/` folder (see [Datasets](#datasets)).
- **Super-resolution** (`srgan`, `esrgan`) — train a low-resolution to high-resolution generator; `esrgan` additionally ships `test_on_image.py` for inference on a single image.

## Sample results

| ![GAN](assets/gan.gif) GAN | ![DCGAN](assets/dcgan.gif) DCGAN |
| --- | --- |
| ![InfoGAN](assets/infogan.gif) InfoGAN | ![ClusterGAN](assets/cluster_gan.gif) ClusterGAN |
| ![CycleGAN](assets/cyclegan.png) CycleGAN | ![Pix2Pix](assets/pix2pix.png) Pix2Pix |
| ![StarGAN](assets/stargan.png) StarGAN | ![ESRGAN](assets/esrgan.png) ESRGAN |

Sample outputs produced by every implementation are stored in `assets/`.

## Requirements

- Python 3
- PyTorch >= 0.4.0
- torchvision, matplotlib, numpy, scipy, pillow, urllib3, scikit-image

```bash
pip install -r requirements.txt
```

All implementations automatically use the GPU when CUDA is available (`torch.cuda.is_available()`) and fall back to CPU otherwise.

## Usage

Each implementation is a directly runnable script:

```bash
cd implementations/dcgan
python3 dcgan.py
```

By default this trains for 200 epochs on MNIST (auto-downloaded to `data/mnist`), printing discriminator and generator losses for every batch, and saving a grid of generated samples to `images/` every `--sample_interval` batches. Models that support checkpointing save weights to `saved_models/` every `--checkpoint_interval` epochs (disabled by default, `--checkpoint_interval -1`), and training can be resumed from a checkpoint by passing `--epoch <n>`.

Example with common overrides:

```bash
cd implementations/cyclegan
python3 cyclegan.py \
    --dataset_name horse2zebra \
    --img_height 256 --img_width 256 \
    --batch_size 1 \
    --sample_interval 200 \
    --checkpoint_interval 10
```

Generated samples are written to `implementations/<model>/images/` (for dataset-driven models, `images/<dataset_name>/`).

## Configuration

All hyperparameters are exposed through `argparse`, and each script prints the parsed configuration at startup. Commonly shared options:

| Argument | Typical default | Description |
| --- | --- | --- |
| `--n_epochs` | 200 | Number of training epochs |
| `--batch_size` | 1–64 (per model) | Batch size |
| `--lr` | 0.0002 | Adam learning rate |
| `--b1`, `--b2` | 0.5, 0.999 | Adam decay of first-order momentum |
| `--n_cpu` | 8 | Number of CPU threads for batch generation |
| `--latent_dim` | 62–100 | Dimensionality of the latent space |
| `--img_size` / `--img_height`, `--img_width` | 28–256 | Image dimensions |
| `--channels` | 1 or 3 | Number of image channels |
| `--sample_interval` | 100–1000 | Batches between saved image samples |
| `--checkpoint_interval` | -1 (disabled) | Epochs between model checkpoints |
| `--epoch` | 0 | Epoch to start/resume training from |
| `--dataset_name` | per model | Dataset folder under `data/` |

Model-specific options cover loss weights and architecture knobs, for example `--lambda_pixel` (pix2pix, default 100), `--lambda_cyc` and `--lambda_id` (cyclegan, defaults 10 and 5), `--lambda_pixel`, `--lambda_latent`, `--lambda_kl` (bicyclegan), `--warmup_batches`, `--lambda_adv`, `--lambda_pixel`, `--residual_blocks` (esrgan), `--n_critic` (dualgan, clustergan), `--wass_flag` (clustergan, enables the Wasserstein metric with gradient penalty), `--mask_size` (context_encoder, ccgan), `--n_residual_blocks`, `--style_dim`, `--dim` (munit), and `--decay_epoch` for linear learning-rate decay (cyclegan, pix2pix, munit). Run any script with `--help` for its full option list.

## Datasets

Data is stored in the repository's top-level `data/` folder; implementations reference it via `../../data/<dataset_name>` relative to their own directory.

- **MNIST** — downloaded automatically by torchvision on the first run of the MNIST-based implementations.
- **MNIST-M** — required by `cogan` and `pixelda`; downloaded and processed automatically by the bundled `mnistm.py` module.
- **CycleGAN (unpaired) datasets** — `data/download_cyclegan_dataset.sh <name>` downloads one of `apple2orange`, `summer2winter_yosemite`, `horse2zebra`, `monet2photo`, `cezanne2photo`, `ukiyoe2photo`, `vangogh2photo`, `maps`, `cityscapes`, `facades`, `iphone2dslr_flower`, `ae_photos` and rearranges it into the `train/A`, `train/B`, `test/A`, `test/B` layout expected by the unpaired implementations:

  ```bash
  cd data
  bash download_cyclegan_dataset.sh horse2zebra
  ```

- **Pix2Pix (paired) datasets** — `data/download_pix2pix_dataset.sh <name>` downloads and extracts a paired dataset (for example `facades`, the default dataset for `pix2pix`) from the Berkeley pix2pix datasets host:

  ```bash
  cd data
  bash download_pix2pix_dataset.sh facades
  ```

- **CelebA (`img_align_celeba`)** — required by `context_encoder`, `ccgan`, and `esrgan`. Download `img_align_celeba.zip` (see the link in the `context_encoder.py`/`esrgan.py` docstrings, or the CelebA project page at `http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html`) and place the `img_align_celeba` folder in `data/`.

## Project structure

```
.
├── assets/                 # sample images/GIFs produced with the implementations
├── data/                   # dataset download scripts
├── implementations/        # one folder per GAN variant
│   ├── dcgan/
│   │   └── dcgan.py        # self-contained: models, data loading, training, sampling
│   └── cyclegan/
│       ├── cyclegan.py     # training script
│       ├── models.py       # GeneratorResNet / Discriminator
│       ├── datasets.py     # ImageDataset
│       └── utils.py        # ReplayBuffer, LambdaLR helpers
├── requirements.txt
└── LICENSE
```

Smaller models are single files; larger architectures split the generator/discriminator definitions into `models.py`, dataset handling into `datasets.py`, and (for cyclegan) shared utilities into `utils.py`, all imported locally by the main script.

## Development

To add a new model, create `implementations/<model>/<model>.py` and follow the existing pattern: argparse configuration, CUDA detection, model and optimizer setup, an alternating generator/discriminator training loop with per-batch loss logging, periodic `save_image` sampling controlled by `--sample_interval`, and optional checkpointing controlled by `--checkpoint_interval`. Keeping each implementation self-contained (helpers shared only within its own folder) makes it easy to read and modify one model without touching the others. Pull requests that add new GAN implementations or fix existing ones are welcome.

## Testing

The repository does not include an automated test suite. Implementations are verified by running them and inspecting the printed losses, for example:

```
[Epoch 0/200] [Batch 0/938] [D loss: 0.692082] [G loss: 0.741319]
```

together with the generated sample grids written to `images/`. For ESRGAN, `test_on_image.py` performs single-image super-resolution with a trained checkpoint:

```bash
cd implementations/esrgan
python3 test_on_image.py --image_path path/to/image.png --checkpoint_model saved_models/generator_<epoch>.pth
```

The result is saved to `images/outputs/sr-<filename>`.

## License

This project is released under the MIT License — see [LICENSE](LICENSE). Copyright (c) 2018 Erik Linder-Norén.
