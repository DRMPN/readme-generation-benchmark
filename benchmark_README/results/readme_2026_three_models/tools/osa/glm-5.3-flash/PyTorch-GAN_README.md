# PyTorch-GAN-xr36acks

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This repository is a collection of standalone implementations of generative adversarial network (GAN) variants for tasks such as image generation, translation, and super-resolution, written in Python with PyTorch. It is intended for ML researchers and developers who want reference implementations to study, compare, or adapt, rather than an installable library or packaged API. Each model lives as an independent training script configured through command-line arguments, with sample images and optional checkpoints written locally during training. Newcomers should consult the Getting Started section for runnable steps.

---

## Core Features

- Around 30 self-contained PyTorch GAN implementations covering image generation, translation, and super-resolution, letting developers study, compare, and adapt well-known models in one place.
- Consistent command-line configuration (epochs, batch size, learning rate, sample and checkpoint intervals) across scripts, making it easy to tune and rerun experiments the same way for every model.
- Automatic dataset acquisition: basic variants download MNIST directly through torchvision, and shell scripts fetch CycleGAN and pix2pix datasets, reducing setup time before training.
- GPU support with automatic CUDA device selection, enabling practical training speeds when a GPU is available.
- Periodic saving of sample images (and optional checkpoints for some models) during training, so progress can be inspected without interrupting runs.

---

## Installation

Set up the project from your local checkout:

1. Open the repository root:

```sh
cd path/to/PyTorch-GAN-xr36acks
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

**Prerequisites**

- Python environment with the dependencies listed in `requirements.txt`.
- A CUDA-enabled GPU is used automatically when available; scripts fall back to CPU otherwise.

**Quickstart**

1. Run a basic variant from its own directory, passing any of the script's command-line arguments to customize the run. Basic variants download MNIST automatically via torchvision on first run, so no manual data setup is needed:

```bash
   cd implementations/gan
   python gan.py
```

2. Training starts as soon as the script runs. Per-batch `D loss` / `G loss` lines are printed to the console, and sample images are saved locally during training at the sample interval configured in the script's arguments.

3. For models that require external datasets (e.g., CycleGAN, pix2pix), download the data first using the shell scripts provided under `data/`, then run that model's script from its own folder.

**Notes**

- Basic variants such as `implementations/dcgan/dcgan.py` and `implementations/wgan_gp/wgan_gp.py` also download MNIST automatically on first run.
- Each script defines its own `argparse` options and per-script defaults (epochs, batch size, learning rate, sample/checkpoint intervals, etc.) at the top of the file — check them before running rather than assuming shared defaults.

---

## Contributing

Contributions are welcome. To keep the collection consistent, please follow the conventions used by the existing implementations:

- Add each new GAN variant as its own directory under `implementations/`, containing a self-contained training script for that model.
- Expose configuration through command-line arguments with defaults defined at the top of the script (epochs, batch size, learning rate, sample and checkpoint intervals), matching the style of the current scripts.
- If a model requires an external dataset, provide or reference a download script under `data/` instead of assuming manually downloaded data.
- Save sample images periodically during training (and checkpoints for models that support them) so progress can be inspected without interrupting the run.
- Verify that your script runs end-to-end before submitting changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for the full license text and terms.

---

## Citation

If you use this project in your work, replace the placeholders below with the project's actual author, year, and repository URL before publishing.

### APA format:

    <Author> (<Year>). PyTorch-GAN-xr36acks [Computer software]. <Repository URL>

### BibTeX format:

    @misc{PyTorch-GAN-xr36acks,

        author = {<Author>},

        title = {PyTorch-GAN-xr36acks},

        year = {<Year>},

        note = {Replace <Author>, <Year>, and <Repository URL> with the project's actual metadata before publishing.}

    }

---