# Real-Time-Voice-Cloning-tr52uvdb

---

[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![numpy](https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikitlearn-F7931E.svg?style=flat&logo=scikitlearn&logoColor=white)
![scipy](https://img.shields.io/badge/SciPy-8CAAE6.svg?style=flat&logo=SciPy&logoColor=white)
![tqdm](https://img.shields.io/badge/tqdm-FFC107.svg?style=flat&logo=tqdm&logoColor=black)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

This project is a Python-based text-to-speech system that clones a voice from a short audio sample and synthesizes arbitrary spoken text in that voice. It is implemented as a three-stage pipeline consisting of a speaker encoder, a synthesizer, and a vocoder, built for researchers, developers, and data scientists working on speech synthesis. The repository provides a command-line interface for interactive synthesis, a graphical toolbox for experimentation, and preprocessing and training workflows for each pipeline stage. See the Getting Started section for runnable steps.

---

## Core Features

- **Voice cloning from a short audio sample** — extracts a speaker embedding from any common audio file (wav, mp3, flac, and more) so new speech can be generated in that voice.
- **Text-to-speech synthesis pipeline** — converts text into mel spectrograms with a Tacotron-based synthesizer and renders waveforms with a vocoder, conditioned on the speaker embedding.
- **Interactive toolbox** — a graphical interface for training, experimenting with, and synthesizing voices using supported datasets.
- **GUI-less command-line demo** — provides a scriptable end-to-end example that verifies the setup and synthesizes speech from arbitrary text and reference audio.
- **CPU/GPU flexibility and reproducibility** — inference runs on CPU when no GPU is available or on request, and an optional random seed makes outputs deterministic.

---

## Installation

Install Real-Time-Voice-Cloning-tr52uvdb using one of the following methods:

**Using the current local checkout:**

1. Open the repository root:
```sh
cd path/to/Real-Time-Voice-Cloning-tr52uvdb
```

2. Install the project dependencies:

```sh
pip install -r requirements.txt
```

---

## Getting Started

**Prerequisites**

- A Python environment with the project's dependencies installed: PyTorch, NumPy, and Librosa.
- Inference runs on a GPU automatically when one is available; add `--cpu` to force CPU execution.

**Quickstart with `demo_cli.py`**

1. Run the demo:

```bash
    python demo_cli.py
```

    The script first verifies your setup with a short self-test of the encoder, synthesizer, and vocoder, then prints `All test passed! You can now synthesize speech.` before entering an interactive loop.

2. Pretrained models are handled automatically: on startup the script fetches the default weights into `saved_models/` (`saved_models/default/encoder.pt`, `saved_models/default/synthesizer.pt`, `saved_models/default/vocoder.pt`). To use other weights, override the paths with `-e`, `-s`, and `-v`.

3. When prompted, enter the path to a reference recording of the voice to clone (mp3, wav, m4a, flac, ...). The script computes the speaker embedding from it.

4. Enter a sentence (around 20 words) to synthesize. The generated audio is played back; add `--no_sound` if you do not want playback.

**Interactive toolbox (optional)**

Launch the toolbox UI with:

```bash
python demo_toolbox.py
```

Add `--cpu` if no GPU is available. The toolbox checks for the pretrained models on startup and downloads them into the directory set by `--models_dir` (default `saved_models`). Its UI lets you load a supported dataset (pass `-d/--datasets_root`; the supported datasets are listed in `toolbox/__init__.py`). You can then generate speaker embeddings from utterances and synthesize new speech through the encoder → synthesizer → vocoder pipeline.

---

## Architecture

The project implements a three-stage text-to-speech pipeline (SV2TTS), where each stage is a self-contained package with its own model, inference API, and training scripts:

- **Encoder** (`encoder/`) — turns a short reference recording into a fixed-size speaker embedding. Audio is preprocessed via `encoder.preprocess_wav`, converted to mel spectrograms, and passed through the `SpeakerEncoder` model (`encoder/model.py`); long utterances are split into overlapping partials whose embeddings are averaged (`encoder/inference.py`).
- **Synthesizer** (`synthesizer/`) — a Tacotron model (`synthesizer/models/tacotron.py`) that maps text sequences (normalized via `synthesizer/utils/`) plus a speaker embedding to mel spectrograms. Exposed through `synthesizer.inference.Synthesizer`, which supports batching multiple inputs.
- **Vocoder** (`vocoder/`) — converts mel spectrograms into audio waveforms (WaveRNN model variants in `vocoder/models/`), generating audio in chunks for efficiency (`vocoder.inference.infer_waveform`).

Data flow, as exercised in `demo_cli.py`: reference audio → `encoder.embed_utterance()` → speaker embedding; text + embedding → `Synthesizer.synthesize_spectrograms()` → mel spectrograms; mel spectrograms → `vocoder.infer_waveform()` → output waveform.

Supporting components:

- **Interactive toolbox** — `demo_toolbox.py` launches the UI in `toolbox/` for working with reference utterances, embeddings, and synthesis in one interface.
- **Per-stage training scripts** — `encoder_preprocess.py`/`encoder_train.py`, `synthesizer_preprocess_audio.py`/`synthesizer_preprocess_embeds.py`/`synthesizer_train.py`, and `vocoder_preprocess.py`/`vocoder_train.py`; each stage is preprocessed and trained independently.
- **Shared utilities** (`utils/`) — argument handling, pretrained model download (`default_models.py`), audio denoising (`logmmse.py`), and profiling.

All three models are loaded from `saved_models/` (e.g., `saved_models/default/encoder.pt`), with `ensure_default_models` fetching missing pretrained weights. Components use CUDA when available and can be forced to CPU with the `--cpu` flag.

---

## Contributing

Contributions are welcome. To propose a change:

1. Fork the repository and create a branch for your work.
2. Set up the environment as described in [Installation](#installation).
3. Run `python demo_cli.py` and confirm that the setup self-test passes before and after your changes.
4. Keep each change focused on a single stage or component (encoder, synthesizer, vocoder, toolbox, or shared `utils/`).
5. Open a pull request describing what changed and why.

For bug reports, include the command you ran, the expected behavior, the actual behavior, and any relevant console output.

---

## License

This project is licensed under the MIT License. For more details, refer to the license file in the repository root.

---

## Citation

If you use this local copy of the project, replace the placeholder below with the canonical repository URL before publishing the citation.

### APA format:

    README Benchmark (2026). Real-Time-Voice-Cloning-tr52uvdb repository [Computer software]. local repository checkout (REPOSITORY_URL)

### BibTeX format:

    @misc{Real-Time-Voice-Cloning-tr52uvdb,

        author = {README Benchmark},

        title = {Real-Time-Voice-Cloning-tr52uvdb repository},

        year = {2026},

        note = {Local repository checkout. Replace REPOSITORY_URL with the canonical repository URL before publishing.}

    }

---