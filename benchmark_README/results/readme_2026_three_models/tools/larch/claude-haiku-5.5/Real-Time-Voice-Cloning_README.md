# Real-Time-Voice-Cloning

A Python implementation of a **real-time, multi-speaker voice cloning** system based on the SV2TTS framework ("Transfer Learning from Speaker Verification to Multispeaker Text-To-Speech Synthesis"). Given a few seconds of a speaker's voice, the system can synthesize arbitrary text in that speaker's voice, including voices it never saw during training.

> **Ethical notice:** Voice cloning can be used to impersonate people and create deceptive audio. Only clone voices you have permission to use, do not use this software to deceive or defraud anyone, and disclose when synthetic speech is used. See [Responsible Use](#responsible-use).

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Repository Structure](#repository-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Pretrained Models](#pretrained-models)
- [Usage](#usage)
  - [Graphical Toolbox](#graphical-toolbox)
  - [Command-Line Demo](#command-line-demo)
  - [Using the Modules Programmatically](#using-the-modules-programmatically)
- [Training From Scratch](#training-from-scratch)
  - [Datasets](#datasets)
  - [Step 1: Speaker Encoder](#step-1-speaker-encoder)
  - [Step 2: Synthesizer](#step-2-synthesizer)
  - [Step 3: Vocoder](#step-3-vocoder)
  - [Monitoring Training](#monitoring-training)
- [Configuration and Hyperparameters](#configuration-and-hyperparameters)
- [Audio Samples](#audio-samples)
- [Troubleshooting](#troubleshooting)
- [Responsible Use](#responsible-use)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments and References](#acknowledgments-and-references)

---

## Features

- **Zero-shot voice cloning:** Clone a voice from a short reference utterance without retraining.
- **Three-stage pipeline:** A speaker encoder, a text-to-spectrogram synthesizer, and a neural vocoder, each of which can be trained or replaced independently.
- **Interactive toolbox:** A Qt-based GUI for loading models, selecting reference audio, typing text, generating speech, and inspecting embeddings and spectrograms.
- **Command-line demo:** A non-GUI interface for quick synthesis, with optional audio playback.
- **Full training pipeline:** Preprocessing scripts and training scripts for every component, with support for multiple public datasets.
- **Visualization:** Speaker embedding projections (UMAP) and attention/spectrogram plots during training and inference.
- **Noise reduction:** An optional log-MMSE denoiser for cleaning up reference audio.
- **Pluggable vocoders:** Support for WaveRNN variants, plus a Griffin-Lim fallback for the synthesizer's output.

---

## How It Works

The system is built from three independently trained neural networks:

```
 Reference audio          ┌────────────────────┐
 (3–10 s of speaker) ───► │  1. Speaker Encoder │ ──► speaker embedding (256-d)
                          │   (GE2E, LSTM)     │             │
                          └────────────────────┘             │
                                                             ▼
 Input text ──► text cleaners/phonemes ──► ┌──────────────────────────┐
                                           │ 2. Synthesizer           │ ──► mel spectrogram
                                           │   (Tacotron 2-style)     │
                                           └──────────────────────────┘
                                                             │
                                                             ▼
                                           ┌──────────────────────────┐
                                           │ 3. Vocoder (WaveRNN)     │ ──► waveform
                                           └──────────────────────────┘
```

1. **Speaker encoder.** A recurrent network trained with the Generalized End-to-End (GE2E) loss on speaker verification data. It maps any utterance to a fixed-length embedding that captures speaker identity, independent of what is said. Because it is trained for verification rather than synthesis, it generalizes to speakers it never saw during training.

2. **Synthesizer.** An attention-based sequence-to-sequence model (Tacotron 2 style) that converts text, conditioned on the speaker embedding, into a mel spectrogram. The text is normalized with cleaners and converted to a symbol sequence (optionally using CMU Pronouncing Dictionary phonemes).

3. **Vocoder.** A WaveRNN neural vocoder that converts the mel spectrogram into a raw audio waveform.

Because the encoder is trained on speaker verification data, the synthesizer only needs to be trained on a smaller set of multi-speaker TTS data, and new voices are cloned by computing an embedding from a reference clip at inference time.

---

## Repository Structure

The layout below is reconstructed from the project's file listing. Module names and locations may vary slightly between versions, so check the actual tree in your clone.

```
Real-Time-Voice-Cloning/
├── demo_toolbox.py              # Launches the graphical toolbox (GUI)
├── demo_cli.py                  # Command-line synthesis demo
├── requirements.txt             # Python dependencies
├── README.md
├── LICENSE.txt                  # Main project license (MIT)
├── LICENSE.md                   # License for bundled third-party components
│
├── encoder/                     # Stage 1: speaker encoder
│   ├── __init__.py
│   ├── config.py                # Encoder configuration
│   ├── params_data.py           # Audio/data parameters for the encoder
│   ├── params_model.py          # Model hyperparameters (layers, embedding size)
│   ├── audio.py                 # Audio loading and mel extraction
│   ├── model.py                 # SpeakerEncoder network (LSTM + GE2E loss)
│   ├── inference.py             # Load encoder and embed utterances
│   ├── preprocess.py            # Dataset preprocessing helpers
│   ├── train.py                 # Encoder training loop
│   ├── encoder_preprocess.py    # CLI: preprocess speaker verification datasets
│   ├── encoder_train.py         # CLI: train the encoder
│   ├── visualizations.py        # UMAP/embedding visualizations (Visdom)
│   └── data_objects/            # Data loading abstractions
│       ├── __init__.py
│       ├── random_cycler.py     # Shuffled round-robin sampler
│       ├── speaker.py           # Speaker: groups utterances per speaker
│       ├── speaker_batch.py     # Batch of speakers and utterances
│       ├── speaker_verification_dataset.py
│       └── utterance.py         # Single utterance with cached mel features
│
├── synthesizer/                 # Stage 2: text-to-mel synthesizer
│   ├── __init__.py
│   ├── hparams.py               # Synthesizer hyperparameters
│   ├── audio.py                 # Spectrogram utilities, Griffin-Lim
│   ├── inference.py             # Load synthesizer and generate mel spectrograms
│   ├── synthesize.py            # Batch synthesis helpers
│   ├── synthesizer_dataset.py   # Dataset for training
│   ├── preprocess.py            # Dataset preprocessing
│   ├── synthesizer_preprocess_audio.py   # CLI: extract mels and text
│   ├── synthesizer_preprocess_embeds.py  # CLI: compute speaker embeddings
│   ├── synthesizer_train.py     # CLI: train the synthesizer
│   ├── train.py                 # Training loop
│   ├── models/
│   │   ├── __init__.py
│   │   └── tacotron.py          # Tacotron model (encoder, attention, decoder)
│   └── utils/
│       ├── __init__.py
│       ├── text.py              # Text → symbol sequence conversion
│       ├── cleaners.py          # Text normalization
│       ├── numbers.py           # Number-to-words normalization
│       ├── symbols.py           # Allowed symbol set
│       ├── _cmudict.py          # CMU Pronouncing Dictionary access
│       └── plot.py              # Attention and spectrogram plotting
│
├── vocoder/                     # Stage 3: neural vocoder (WaveRNN)
│   ├── __init__.py
│   ├── hparams.py               # Vocoder hyperparameters
│   ├── audio.py                 # Audio utilities
│   ├── inference.py             # Load vocoder and generate waveforms
│   ├── gen_wavernn.py           # Generate audio from mel spectrograms
│   ├── display.py               # Progress display utilities
│   ├── distribution.py          # Output distributions (mixture of logistics, etc.)
│   ├── train.py                 # Vocoder training loop
│   ├── vocoder_dataset.py       # Dataset for training
│   ├── vocoder_preprocess.py    # CLI: preprocess data for vocoder training
│   ├── vocoder_train.py         # CLI: train the vocoder
│   └── models/
│       ├── fatchord_version.py  # WaveRNN implementation (community variant)
│       └── deepmind_version.py  # WaveRNN implementation (DeepMind-style)
│
├── toolbox/                     # GUI components (PyQt5)
│   ├── __init__.py
│   ├── ui.py                    # Main window and widgets
│   └── utterance.py             # Utterance representation for the UI
│
├── utils/
│   ├── __init__.py
│   ├── argutils.py              # Argument parsing helpers
│   ├── default_models.py        # Default model paths and download info
│   ├── logmmse.py               # Log-MMSE speech denoiser
│   └── profiler.py              # Simple timing profiler
│
└── samples/                     # Example reference audio (.mp3) and text
```

---

## Requirements

### System

- **Python:** 3.7 is the version the project was developed and tested against. Newer versions may work but are not guaranteed; check `requirements.txt` for pinned versions.
- **GPU:** An NVIDIA GPU with CUDA is strongly recommended for training and for real-time inference. The code can run on CPU (`--cpu` flag), but synthesis will be much slower.
- **OS:** Linux, Windows, and macOS are supported. Linux is the most commonly tested platform.
- **Audio:** A working audio output device if you want playback.

### Python packages

Dependencies are listed in `requirements.txt`. They typically include:

| Package | Purpose |
|---|---|
| `torch` | Neural network training and inference (install separately, see below) |
| `numpy`, `scipy` | Numerical computing |
| `librosa` | Audio loading, mel spectrograms, resampling |
| `soundfile` | Reading and writing audio files (including MP3 with recent libsndfile) |
| `sounddevice` | Audio playback |
| `PyQt5` | Graphical toolbox |
| `matplotlib` | Plotting |
| `umap-learn` | Embedding visualization |
| `visdom` | Optional live training dashboards |
| `webrtcvad` | Voice activity detection for preprocessing |
| `unidecode`, `inflect` | Text normalization |
| `multiprocess`, `numba` | Parallel preprocessing and acceleration |
| `tqdm` | Progress bars |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/CorentinJ/Real-Time-Voice-Cloning.git
cd Real-Time-Voice-Cloning
```

### 2. Create a virtual environment (recommended)

```bash
python3.7 -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install PyTorch

Install the PyTorch build that matches your CUDA version from [pytorch.org](https://pytorch.org/get-started/locally/). For example:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu117
```

For CPU-only:

```bash
pip install torch torchvision
```

### 4. Install the remaining dependencies

```bash
pip install -r requirements.txt
```

### 5. Platform-specific notes

- **Linux:** `sounddevice` needs PortAudio. Install it with:
  ```bash
  sudo apt-get install libportaudio2
  ```
  For PyQt5 issues on some distributions, you may also need `sudo apt-get install python3-pyqt5` or the Qt XCB libraries.

- **MP3 support:** The sample reference files are MP3s. Reading MP3 requires either libsndfile 1.1.0+ (bundled with recent `soundfile` wheels) or `ffmpeg` available on your PATH for the `audioread` fallback in librosa:
  ```bash
  sudo apt-get install ffmpeg      # Linux
  brew install ffmpeg              # macOS
  ```

- **webrtcvad:** This package compiles a C extension. On Windows you may need the Visual C++ Build Tools; on Linux, `python3-dev` and a C compiler are required.

- **Visdom (optional):** Only needed if you want live training plots. Start the server with `python -m visdom.server` before training.

---

## Pretrained Models

To use the toolbox or CLI without training, download the three pretrained models (speaker encoder, synthesizer, vocoder). Links are provided in the project's main README on GitHub. Place the downloaded files as follows:

```
saved_models/
└── default/
    ├── encoder.pt
    ├── synthesizer.pt
    └── vocoder.pt
```

The paths are defined in `utils/default_models.py`. If the directory is missing, the toolbox and CLI will report which model files they could not find.

> **Note:** The synthesizer pretrained model was trained on LibriSpeech-style data. Cloning quality depends heavily on the reference audio: clean, single-speaker recordings with little background noise and reverberation give the best results.

---

## Usage

### Graphical Toolbox

The toolbox is the primary interface. It provides a full workflow for voice cloning.

```bash
python demo_toolbox.py
```

To point the toolbox at a dataset directory (used to browse utterances from your local datasets):

```bash
python demo_toolbox.py -d /path/to/datasets
```

To run on CPU:

```bash
python demo_toolbox.py -c
```

**Typical workflow:**

1. **Load a reference utterance.** Choose a dataset and speaker, or open a `.wav`/`.mp3` file with a clean recording of the target voice (about 5–10 seconds of speech works well).
2. **Optionally denoise** the reference using the built-in denoising option.
3. **Compute the speaker embedding.** The toolbox displays the embedding and, optionally, its position relative to other speakers.
4. **Enter text** into the synthesis box.
5. **Synthesize.** The toolbox displays the generated mel spectrogram and attention alignment, then plays the waveform.
6. **Save or export** the generated audio.

### Command-Line Demo

For scripted or headless usage, use `demo_cli.py`:

```bash
python demo_cli.py
```

Typical options (run `python demo_cli.py --help` to see the full list):

| Option | Description |
|---|---|
| `-m, --models_dir` | Directory containing `encoder.pt`, `synthesizer.pt`, `vocoder.pt` (default: `saved_models/default`) |
| `-c, --cpu` | Force CPU inference |
| `--no_sound` | Do not play audio, only save output |
| `--seed` | Set random seed for reproducible output |

The CLI prompts for a reference audio path and the text to synthesize, then writes the result to disk.

Example session:

```text
$ python demo_cli.py
Reference audio path: samples/p240_00000.mp3
Text to synthesize: Hello, this is a test of voice cloning.
Saved output to: output.wav
```

### Using the Modules Programmatically

The three stages can be called directly from Python. The following outline shows the general flow; check the function signatures in the `inference.py` file of each module for the exact current API.

```python
from pathlib import Path
import numpy as np
import soundfile as sf

from encoder import inference as encoder
from synthesizer.inference import Synthesizer
from vocoder import inference as vocoder

# 1. Load the three models
encoder.load_model(Path("saved_models/default/encoder.pt"))
synthesizer = Synthesizer(Path("saved_models/default/synthesizer.pt"))
vocoder.load_model(Path("saved_models/default/vocoder.pt"))

# 2. Compute a speaker embedding from a reference utterance
wav = encoder.preprocess_wav(Path("samples/p240_00000.mp3"))
embed = encoder.embed_utterance(wav)

# 3. Synthesize a mel spectrogram from text, conditioned on the embedding
texts = ["Hello, this is a test of voice cloning."]
embeds = [embed]
specs = synthesizer.synthesize_spectrograms(texts, embeds)
mel = specs[0]

# 4. Convert the mel spectrogram to a waveform
generated_wav = vocoder.infer_waveform(mel)

# 5. Save the result
sample_rate = synthesizer.sample_rate
sf.write("output.wav", generated_wav, sample_rate)
```

---

## Training From Scratch

Training is only necessary if you want to use your own datasets, change the architecture, or reproduce the results. For normal use, the pretrained models are sufficient.

Training is done in three independent stages, in this order:

1. **Speaker encoder** on speaker verification data
2. **Synthesizer** on multi-speaker TTS data, using embeddings from the trained encoder
3. **Vocoder** on mel spectrograms and their audio, optionally using synthesizer outputs

### Datasets

| Dataset | Used for | Link |
|---|---|---|
| LibriSpeech (`train-clean-100`, `train-clean-360`, `train-other-500`) | Encoder, synthesizer, vocoder | [openslr.org/12](https://www.openslr.org/12) |
| VoxCeleb1 | Encoder | [robots.ox.ac.uk/~vgg/data/voxceleb](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/) |
| VoxCeleb2 | Encoder | [robots.ox.ac.uk/~vgg/data/voxceleb](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/) |
| VCTK | Optional (for experiments) | [datashare.ed.ac.uk](https://datashare.ed.ac.uk/handle/10283/3443) |

Arrange your datasets in a single root directory, for example:

```
/path/to/datasets/
├── LibriSpeech/
│   ├── train-clean-100/
│   ├── train-clean-360/
│   └── train-other-500/
├── VoxCeleb1/
└── VoxCeleb2/
```

Preprocessing writes its outputs into an `SV2TTS/` subdirectory with `encoder/`, `synthesizer/`, and `vocoder/` folders.

### Step 1: Speaker Encoder

**Preprocess** the speaker verification datasets (computes mel features and speaker-level metadata):

```bash
python encoder_preprocess.py /path/to/datasets -d librispeech_other,voxceleb1,voxceleb2
```

**Train** the encoder:

```bash
python encoder_train.py my_encoder_run /path/to/datasets/SV2TTS/encoder
```

The first argument is the run name (used for checkpoint and log folders). The second is the preprocessed encoder data directory. Checkpoints are saved under `encoder/saved_models/` by default.

### Step 2: Synthesizer

**Preprocess** the audio into mel spectrograms and text:

```bash
python synthesizer_preprocess_audio.py /path/to/datasets
```

**Compute speaker embeddings** for each utterance using the trained encoder:

```bash
python synthesizer_preprocess_embeds.py /path/to/datasets/SV2TTS/synthesizer
```

**Train** the synthesizer:

```bash
python synthesizer_train.py my_synth_run /path/to/datasets/SV2TTS/synthesizer
```

Checkpoints are written to `synthesizer/saved_models/<run_name>/`.

### Step 3: Vocoder

**Preprocess** the data for vocoder training. This step can use the synthesizer to generate mel spectrograms, so that the vocoder learns to invert the synthesizer's output rather than ground-truth mels only:

```bash
python vocoder_preprocess.py /path/to/datasets -m /path/to/synthesizer/saved_models
```

**Train** the vocoder:

```bash
python vocoder_train.py my_vocoder_run /path/to/datasets
```

Checkpoints are written to `vocoder/saved_models/<run_name>/`.

### Monitoring Training

- **Logs:** Training loss and progress are printed to the console and written to log files in each run's directory.
- **Visdom:** If `visdom` is installed and the server is running, the encoder training script reports losses and embedding projections to the dashboard at `http://localhost:8097`.
- **Plots:** The synthesizer saves attention alignment and predicted spectrogram plots periodically, so you can check whether the attention has converged (a clear diagonal alignment is the sign of a successful synthesizer).
- **Resuming:** Pass the existing checkpoint path to resume training from the last saved step, as indicated in each training script's `--help` output.

---

## Configuration and Hyperparameters

Each stage has its own configuration module. Edit these files before preprocessing or training to change behavior.

| File | Controls |
|---|---|
| `encoder/params_data.py` | Partial utterance length, number of speakers and utterances per batch, mel settings for the encoder |
| `encoder/params_model.py` | Encoder LSTM size, number of layers, embedding dimension (256 by default) |
| `encoder/config.py` | Encoder-level settings and paths |
| `synthesizer/hparams.py` | Sample rate, STFT parameters, mel bins, Tacotron encoder/decoder sizes, learning rate schedule, batch size, attention settings |
| `synthesizer/utils/symbols.py` | Symbol set the text is mapped to |
| `synthesizer/utils/cleaners.py` | Text normalization rules (e.g., ASCII conversion, number expansion, abbreviation expansion) |
| `vocoder/hparams.py` | WaveRNN sizes, bit depth, mel settings, batch size, learning rate |
| `utils/default_models.py` | Default locations of the pretrained model files |

> **Important:** The encoder, synthesizer, and vocoder must agree on audio parameters (sample rate, number of mel channels, hop length, and so on). If you change them in one stage, update the others, or the stages will produce incompatible outputs.

---

## Audio Samples

The `samples/` directory contains example reference recordings in MP3 format (for example, `p240_00000.mp3`, `p260_00000.mp3`, `3575_00000.mp3`, `1320_00000.mp3`, `8230_00000.mp3`, `6829_00000.mp3`). These are short utterances from speakers in public datasets, intended for testing the toolbox and CLI. Use them as reference audio to verify your installation before using your own recordings.

---

## Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| `Model file not found` | Pretrained models are missing from `saved_models/default/`. Download them and check the paths in `utils/default_models.py`. |
| `CUDA out of memory` | Reduce batch size in the relevant `hparams.py` or `params_data.py`, or run with `-c` to use CPU. |
| `No module named PyQt5` or toolbox fails to open | Reinstall PyQt5 (`pip install PyQt5`). On Linux, install Qt XCB system libraries. |
| `OSError: sndfile library not found` or MP3 fails to load | Upgrade `soundfile` (libsndfile ≥ 1.1.0) or install `ffmpeg`. |
| `sounddevice` errors or no audio output | Install PortAudio (`libportaudio2` on Debian/Ubuntu) and verify your default output device. Use `--no_sound` to skip playback. |
| `webrtcvad` fails to build | Install a C compiler and Python development headers, or the Visual C++ Build Tools on Windows. |
| Output is robotic, garbled, or mumbled | Check the reference audio quality (use clean, noise-free speech). Try the denoising option. Ensure the vocoder matches the synthesizer's mel settings. |
| Synthesizer attention does not align (no diagonal in plots) | Train longer, verify the preprocessed text and audio are aligned, and check that the reference transcripts are correct. |
| Visdom dashboard is empty | Start the server with `python -m visdom.server` before running training. |
| Very slow synthesis | Use a CUDA-enabled PyTorch build and make sure the GPU is actually used. CPU inference is significantly slower. |

If you encounter an issue not listed here, search the project's GitHub issues, and include your Python version, PyTorch version, OS, and the full traceback when reporting a new one.

---

## Responsible Use

Voice cloning technology can be misused for fraud, harassment, misinformation, and impersonation. If you use this project, please:

- Only clone voices with the explicit consent of the speaker, or use publicly licensed datasets and voices.
- Never use the output to deceive people, impersonate someone in a context where they would be harmed, or commit fraud.
- Clearly label synthetic speech as synthetic when it is shared publicly or used in any context where listeners could be misled.
- Be aware that detection tools and legal frameworks for synthetic audio are still evolving.

The authors and contributors provide this software as-is and are not responsible for its misuse.

---

## Contributing

Contributions are welcome, including bug fixes, documentation improvements, new vocoder or encoder variants, and dataset preprocessing support.

1. Fork the repository and create a feature branch.
2. Keep changes focused and follow the existing code style.
3. Test your changes on at least one stage of the pipeline (for example, run the CLI demo, or run a short training job).
4. Open a pull request describing what changed and why.

For larger changes, open an issue first to discuss the approach.

---

## License

The main project is released under the **MIT License** (see `LICENSE.txt`).

Some bundled components, such as parts of the synthesizer or vocoder code adapted from other open-source implementations, may be covered by their own licenses. See `LICENSE.md` and the license notices in the relevant subdirectories. Pretrained models and datasets have their own terms, which you must respect when using or redistributing them.

---

## Acknowledgments and References

This project builds on several research papers and open-source implementations.

**Papers**

- Jia, Y., et al. (2018). *Transfer Learning from Speaker Verification to Multispeaker Text-To-Speech Synthesis.* (SV2TTS framework)
- Wan, L., et al. (2018). *Generalized End-to-End Loss for Speaker Verification.* (GE2E loss used for the encoder)
- Wang, Y., et al. (2017). *Tacotron: Towards End-to-End Speech Synthesis.*
- Shen, J., et al. (2018). *Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions.* (Tacotron 2)
- Kalchbrenner, N., et al. (2018). *Efficient Neural Audio Synthesis.* (WaveRNN)
- Griffin, D., & Lim, J. (1984). *Signal estimation from modified short-time Fourier transform.* (Griffin-Lim reconstruction)

**Datasets**

- LibriSpeech (Panayotov et al., 2015)
- VoxCeleb1 and VoxCeleb2 (Nagrani et al.; Chung et al.)
- VCTK Corpus (Yamagishi et al.)
- CMU Pronouncing Dictionary

**Libraries**

PyTorch, librosa, NumPy, SciPy, PyQt5, sounddevice, soundfile, UMAP, Visdom, webrtcvad, and the other packages listed in `requirements.txt`.

Thanks to the authors of the original papers and the open-source community whose implementations and feedback shaped this project.
