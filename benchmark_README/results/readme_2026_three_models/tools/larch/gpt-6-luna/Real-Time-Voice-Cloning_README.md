# Real-Time-Voice-Cloning

A three-stage voice-cloning pipeline that generates speech in a voice represented by a short reference recording. The project combines a speaker encoder, a text-to-speech synthesizer, and a neural vocoder.

> Use this software responsibly. Only clone voices with the speaker’s consent, and disclose when generated audio is synthetic. Do not use it to impersonate people or mislead others.

## How it works

1. **Speaker encoder** — extracts a speaker embedding from a reference audio clip.
2. **Synthesizer** — converts text and the speaker embedding into a mel spectrogram.
3. **Vocoder** — turns the spectrogram into a waveform.

The models can be used together for inference or trained separately. Good results depend on the quality of the reference recording, the text, the models, and their training data.

## Repository structure

The repository is organized into model-specific components:

- **Encoder** — model, data preparation, training, and inference code.
- **Synthesizer** — Tacotron-based text-to-speech model, audio preprocessing, training, and inference.
- **Vocoder** — WaveRNN implementations, preprocessing, training, and inference.
- **Demos** — `demo_cli.py` for command-line use and `demo_toolbox.py` for the graphical toolbox.
- **Shared utilities** — audio, plotting, logging, configuration, and dataset helpers.

The repository also includes example audio files and supporting text data. These are not a substitute for the datasets required to train the models.

## Requirements

- Python and the packages listed in `requirements.txt`
- PyTorch, with a version compatible with your Python version and CUDA installation if using a GPU
- A working audio backend and the system libraries required by the audio packages

This is a research codebase with dependencies that may not support the latest Python or PyTorch releases. If installation fails, use a clean virtual environment and consult the package versions in `requirements.txt`.

### Installation

From the repository root:

```bash
python -m venv .venv
```

Activate the environment, then install the dependencies:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
```

Install the PyTorch build appropriate for your platform and CUDA version if the requirements do not install the correct one. Verify that PyTorch can access your GPU before starting long training runs.

## Quick start: run a demo

Inference requires trained or pretrained checkpoints for the encoder, synthesizer, and vocoder. The repository’s `default_models.py` and model-loading code describe the expected model locations and defaults.

1. Obtain compatible pretrained checkpoints from the project’s model distribution or documentation.
2. Place the checkpoints in the locations expected by the demo, or provide the appropriate model-directory option.
3. Start the command-line demo:

   ```bash
   python demo_cli.py
   ```

4. For the graphical toolbox, run:

   ```bash
   python demo_toolbox.py
   ```

The demos let you provide a reference voice and text to synthesize. Run either script with `--help` to see the options available in your checkout.

### Tips for reference audio

- Use a clean recording of a single speaker, without music or overlapping speech.
- Prefer a short, natural speech sample with little background noise or reverberation.
- Avoid very quiet, clipped, or heavily compressed audio.
- A WAV file is generally a safer input choice than a compressed format.
- Try more than one reference clip if the resulting voice does not sound representative.

## Training your own models

Training is a multi-step process. Prepare datasets first, then train the encoder, synthesizer, and vocoder. Exact command-line options can vary; use `--help` for each script before running it.

### 1. Prepare datasets

Organize your audio datasets on disk and follow the expected layout for the dataset loaders. Preprocessing scripts accept dataset paths and may offer options for output directories or selected datasets:

```bash
python encoder_preprocess.py --help
python synthesizer_preprocess_audio.py --help
python synthesizer_preprocess_embeds.py --help
python vocoder_preprocess.py --help
```

A typical preparation sequence is:

```bash
python encoder_preprocess.py /path/to/datasets
python synthesizer_preprocess_audio.py /path/to/datasets
```

The synthesizer’s embedding-preparation step depends on a trained encoder, so run it after encoder training:

```bash
python synthesizer_preprocess_embeds.py /path/to/datasets
```

Prepare the vocoder’s data using its preprocessing script:

```bash
python vocoder_preprocess.py /path/to/datasets
```

Check each script’s help output for required arguments, supported dataset layouts, and output paths.

### 2. Train the encoder

The encoder learns to represent speaker identity as an embedding. Its data preparation and training scripts are `encoder_preprocess.py` and `encoder_train.py`.

```bash
python encoder_train.py --help
python encoder_train.py <run_name>
```

### 3. Train the synthesizer

The synthesizer learns to generate speech features from text and speaker embeddings. First preprocess its audio, then generate speaker embeddings using the trained encoder, and finally train the synthesizer:

```bash
python synthesizer_train.py --help
python synthesizer_train.py <run_name>
```

### 4. Train the vocoder

The vocoder learns to generate waveforms from the synthesizer’s acoustic features:

```bash
python vocoder_train.py --help
python vocoder_train.py <run_name> /path/to/datasets
```

Review the command’s help output before training; dataset paths and accepted arguments may differ depending on the configuration.

### Training notes

- Keep training data, preprocessed features, logs, and checkpoints organized. These can require substantial disk space.
- Use a GPU for practical training times. CPU training may be very slow.
- Train the stages in dependency order: encoder, synthesizer embeddings and synthesizer, then vocoder.
- Monitor training logs and generated samples rather than relying on loss values alone.
- Keep a record of dataset sources, preprocessing options, and checkpoint versions so that a complete model set can be reproduced.

## Project components

### Encoder

The encoder-related files include model and parameter definitions, audio processing, dataset handling, training, and inference. Its output is a speaker representation used to condition synthesis.

### Synthesizer

The synthesizer files include the Tacotron-based model, text processing, audio utilities, training, and inference. It converts text into acoustic features conditioned on a speaker embedding.

### Vocoder

The vocoder files include WaveRNN implementations, audio utilities, dataset preparation, training, and inference. It generates audio from acoustic features.

### Demos and utilities

- `demo_cli.py` — command-line demonstration.
- `demo_toolbox.py` — graphical demonstration toolbox.
- `argutils.py`, plotting modules, and profiler utilities — shared support for running and inspecting the project.

## Troubleshooting

- **Missing checkpoint or model-loading errors:** confirm that all three model stages are present and that their paths match the configuration used by the demo.
- **CUDA errors:** check that your installed PyTorch build matches your CUDA setup, or try running on CPU if supported.
- **Audio backend or library errors:** check the installation requirements of the audio packages in `requirements.txt` and install any required system dependencies.
- **Poor or unstable speech:** try a cleaner reference recording, verify that the text is supported by the text-processing pipeline, and use compatible checkpoints from the same model setup.
- **Preprocessing or training arguments are unclear:** run the relevant script with `--help` and inspect its configuration and parameter files.

## License and data

Review the license files included with the repository before using or redistributing the code. Model checkpoints and datasets may have separate terms. You are responsible for confirming that you have the rights to use the training data, reference recordings, and generated audio for your intended purpose.
