# Real-Time-Voice-Cloning-pqufshos

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![numpy](https://img.shields.io/badge/NumPy-013243.svg?style={0}&logo=NumPy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikitlearn-F7931E.svg?style={0}&logo=scikit-learn&logoColor=white)
![scipy](https://img.shields.io/badge/SciPy-8CAAE6.svg?style={0}&logo=SciPy&logoColor=white)
![tqdm](https://img.shields.io/badge/tqdm-FFC107.svg?style={0}&logo=tqdm&logoColor=black)

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

This is a Python project for voice cloning and text-to-speech, which generates speech in a target speaker's voice from a reference audio recording and input text. The system is organized as a three-stage pipeline covering speaker encoding, spectrogram synthesis, and waveform generation. It is aimed primarily at developers and researchers who want to study or build on this approach, and it includes a graphical toolbox that end users can work with directly. The repository provides a command-line interface for interactive use, a graphical toolbox, and separate preprocessing and training flows for each stage. See Getting Started for runnable steps and prerequisites.

---

## Core Features

- **Voice cloning from a reference recording:** Generates speech in the voice of a supplied audio sample (mp3, wav, m4a, and flac inputs are accepted), so you can synthesize new speech without training a model for each speaker.
- **Three-stage synthesis pipeline:** Separates speaker embedding, spectrogram synthesis, and waveform generation into independently loadable components, so you can inspect, replace, or reuse each stage in your own code.
- **Graphical toolbox:** Launches an interactive GUI for generating speech, with options for a datasets directory, a models directory, CPU-only inference, and a random seed for reproducible output.
- **Command-line setup check and integration reference:** Accepts model paths, CPU-only inference, and a random seed, and runs a small test of all three stages to confirm the configuration before use.

---

## Installation

Install Real-Time-Voice-Cloning-pqufshos using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/Real-Time-Voice-Cloning-pqufshos
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

**Prerequisites**

- Python, with the packages listed in `requirements.txt` installed (see [Installation](#installation)).

**Steps**

1. Install the dependencies described in [Installation](#installation), using `requirements.txt`.

2. Launch the Toolbox GUI from the repository root:

```bash
   python demo_toolbox.py
```

   This script launches the Toolbox GUI. It also calls `ensure_default_models` for the models directory (`saved_models` by default).

3. To run the command-line demo instead

---

## Contributing

---

## License

This project is protected under the MIT. For more details, refer to the [LICENSE](./LICENSE.md) file.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). Real-Time-Voice-Cloning-pqufshos repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{Real-Time-Voice-Cloning-pqufshos,

        author = {README Benchmark},

        title = {Real-Time-Voice-Cloning-pqufshos repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---