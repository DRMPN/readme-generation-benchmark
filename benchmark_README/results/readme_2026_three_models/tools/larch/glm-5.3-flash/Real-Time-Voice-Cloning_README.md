# Real-Time Voice Cloning

This repository is an implementation of **Real-Time Voice Cloning**, based on the paper *[SV2TTS: Transfer Learning from Speaker Verification to Multispeaker-TTS Synthesis](https://arxiv.org/abs/1806.04558)* (Jia et al., 2018). The project allows you to clone a voice from a short audio sample (as little as a few seconds) and use it to synthesize arbitrary speech with a text-to-speech system.

## Overview

The system is built from three independently trainable neural networks:

1. **Encoder** (Speaker Verification)
   - Based on GE2E (Generalized End-to-End) loss.
   - Creates a fixed-dimensional **embedding** (voice fingerprint) from an utterance of a speaker.
   - Trained on speaker verification datasets (e.g., **LibriSpeech**, **VoxCeleb1/2**).

2. **Synthesizer** (Tacotron-based TTS)
   - A modified **Tacotron 2** architecture.
   - Takes a text sequence concatenated with the speaker embedding and generates a **mel spectrogram**.
   - Trained on the **VCTK** dataset (109 speakers with transcriptions).

3. **Vocoder**
   - A **WaveNet-style / WaveRNN** network.
   - Converts the mel spectrogram into raw audio waveform.
   - Trained on **LibriSpeech (other500)** or **VCTK**.

The three-stage pipeline (Embedding → Mel spectrogram → Waveform) is what enables voice cloning with only seconds of reference audio.

## Project Structure

```
├── encoder/            # Speaker embedding network
│   ├── audio.py        # Mel spectrogram / audio preprocessing
│   ├── inference.py    # Embedding extraction at inference time
│   ├── train.py        # Training script (encoder_train.py)
│   ├── preprocess.py   # Dataset preprocessing
│   └── params_*.py     # Model & data hyperparameters
├── synthesizer/        # Tacotron-based spectrogram generator
│   ├── tacotron.py     # Model architecture
│   ├── train.py        # Training script (synthesizer_train.py)
│   ├── preprocess.py   # Audio & embed preprocessing
│   └── text/           # Text cleaning, symbol mapping, number normalization
├── vocoder/            # WaveRNN vocoder
│   ├── train.py        # Training script (vocoder_train.py)
│   ├── fatchord_version.py  # Core WaveRNN implementation
│   └── inference.py    # Spectrogram-to-audio generation
├── demo_cli.py         # Command-line interface for voice cloning
├── demo_toolbox.py     # Graphical toolbox (GUI)
├── utils/              # Logging, argument parsing, profiler, etc.
└── requirements.txt
```

## Getting Started

### Requirements

- Python 3.6+ (3.7 recommended)
- A CUDA-capable GPU is strongly recommended for training and fast inference

Install dependencies:

```bash
pip install -r requirements.txt
```

For GPU support, install the appropriate PyTorch/TensorFlow builds for your CUDA version. On Windows you may also need the Visual C++ build tools for some dependencies.

### Downloading Pretrained Models

Pretrained models for all three stages are available for download (see `default_models.py` / the project release page). Place the downloaded weights in:

```
encoder/saved_models/
synthesizer/saved_models/
vocoder/saved_models/
```

### Quick Demo (CLI)

Clone a voice from a reference clip and synthesize speech:

```bash
python demo_cli.py
```

You will be prompted to:
1. Provide one or more audio files (`.wav`, `.mp3`, etc.) of the target speaker (a few seconds each).
2. Enter the sentence(s) you want synthesized.
3. Receive the generated audio with the target speaker's voice.

### Toolbox (GUI)

An interactive toolbox lets you record/load audio, visualize embeddings and spectrograms, and synthesize speech in real time:

```bash
python demo_toolbox.py
```

## Training Your Own Models

### 1. Encoder

```bash
# Preprocess a dataset (e.g., LibriSpeech)
python encoder_preprocess.py <datasets_root>

# Train
python encoder_train.py <output_dir> <datasets_root>
```

### 2. Synthesizer

```bash
# Preprocess audio (VCTK recommended)
python synthesizer_preprocess_audio.py <datasets_root>

# Generate embeddings for the preprocessed utterances
python synthesizer_preprocess_embeds.py <datasets_root>/SV2TTS/synthesizer

# Train
python synthesizer_train.py <output_dir> <datasets_root>
```

You can monitor training with TensorBoard:

```bash
tensorboard --logdir <output_dir>
```

### 3. Vocoder

```bash
# Preprocess
python vocoder_preprocess.py <datasets_root> <synthesizer_model_path>

# Train
python vocoder_train.py <output_dir> <datasets_root>
```

Datasets used during training:
- **LibriSpeech** (`train-clean-100`, `train-clean-360`) — encoder & vocoder
- **VoxCeleb1 / VoxCeleb2** — encoder (optional, improves quality)
- **VCTK** — synthesizer & vocoder

## Usage Notes & Tips

- Reference audio should be relatively **noise-free**, contain a **single speaker**, and last roughly **5–10+ seconds**.
- Longer and cleaner reference clips generally produce better voice similarity.
- Synthesis quality depends heavily on the vocoder; pretrained checkpoints give the best results.
- Text with unusual characters or very long sentences may degrade quality — keep sentences reasonable in length.
- The included sample files (`p240_00000.mp3`, `p260_00000.mp3`, etc.) are reference clips from VCTK that you can try immediately with `demo_cli.py`.

## Credits

- Paper: [*Transfer Learning from Speaker Verification to Multispeaker-TTS Synthesis*](https://arxiv.org/abs/1806.04558) (Ye Jia et al., CorentinJ implementation)
- Tacotron 2 and WaveRNN implementations are based on the work of **fatchord** and the Google **Tacotron 2** paper.
- GE2E loss: [*Generalized End-to-End Loss for Speaker Verification*](https://arxiv.org/abs/1710.10467)

## License

This project is released under the terms described in the included `LICENSE` files. Please review them before use, especially if you intend to use this for commercial purposes or with someone's voice — always obtain consent before cloning a person's voice.
