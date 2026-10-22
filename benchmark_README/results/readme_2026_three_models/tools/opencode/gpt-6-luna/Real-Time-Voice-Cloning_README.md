# Real-Time Voice Cloning (SV2TTS)

This repository implements a three-part text-to-speech pipeline: a speaker encoder extracts a voice embedding from reference audio, a Tacotron synthesizer predicts a mel spectrogram from text and that embedding, and a WaveRNN vocoder converts the spectrogram to audio. It includes command-line inference, a graphical toolbox, preprocessing scripts, and training scripts for each component.

## Repository layout

- `encoder/` — speaker-embedding model, audio preprocessing, inference, and training.
- `synthesizer/` — Tacotron model, text/audio processing, inference, and training.
- `vocoder/` — WaveRNN model, waveform inference, and training.
- `toolbox/` — graphical interface for browsing reference recordings, recording audio, and generating speech.
- `demo_cli.py` — interactive, terminal-based synthesis.
- `demo_toolbox.py` — launches the graphical toolbox.
- `*_preprocess*.py`, `*_train.py` — dataset preparation and component training entry points.
- `samples/` — example reference audio and associated dataset notices; see [`samples/README.md`](samples/README.md).

## Installation

Use an environment with Python and install the pinned packages listed in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` does not install PyTorch. Install a PyTorch build suitable for your Python version and hardware separately, following the [official PyTorch installation instructions](https://pytorch.org/get-started/locally/). The toolbox also uses PyQt5 and `sounddevice`; audio playback or recording may require a working system audio/PortAudio setup.

## Inference with the pretrained models

The demo scripts look for the default checkpoints under `saved_models/default/`:

```text
saved_models/default/encoder.pt
saved_models/default/synthesizer.pt
saved_models/default/vocoder.pt
```

When these files are missing or have unexpected sizes, the scripts call `utils/default_models.py` to download the default checkpoints. This requires network access. The helper also prints a Google Drive folder link if a download fails. The checkpoints are not stored in this repository.

### Terminal demo

Run:

```bash
python demo_cli.py
```

After loading the models and running a small configuration test, the script repeatedly asks for a reference-audio path and a sentence. It writes generated results as `demo_output_00.wav`, `demo_output_01.wav`, and so on in the current directory. Playback is attempted unless disabled. Options include:

```bash
python demo_cli.py --help
python demo_cli.py --cpu --no_sound
python demo_cli.py --enc_model_fpath path/to/encoder.pt \
                   --syn_model_fpath path/to/synthesizer.pt \
                   --voc_model_fpath path/to/vocoder.pt
```

The demo uses a GPU when PyTorch reports one available; `--cpu` forces CPU inference. `--seed` accepts an optional integer seed.

### Graphical toolbox

Run the toolbox with a dataset directory and model directory:

```bash
python demo_toolbox.py --datasets_root /path/to/datasets
```

It looks for default models in `saved_models/` and allows selecting recordings in the dataset browser, loading an audio file, or recording a reference. The browser recognizes the dataset paths listed in `toolbox/__init__.py`, including LibriSpeech, LibriTTS, LJSpeech, VoxCeleb, and VCTK layouts. Use `--help` to see options such as `--models_dir`, `--cpu`, and `--seed`. In the toolbox, the vocoder can be omitted for Griffin–Lim waveform reconstruction.

## Training your own models

Training is optional; the inference demos use the default pretrained checkpoints unless other model paths are supplied. Each preprocessing and training script accepts `--help` for its complete arguments. Dataset files must be obtained separately and follow the formats expected by the scripts.

The component pipeline is:

1. **Prepare and train the speaker encoder.** The preprocessing script accepts `librispeech_other`, `voxceleb1`, and `voxceleb2` (train data). For example, it expects VoxCeleb1 audio under `VoxCeleb1/wav` with `VoxCeleb1/vox1_meta.csv`, VoxCeleb2 audio under `VoxCeleb2/dev/aac`, and the configured LibriSpeech training tree under the datasets root.

   ```bash
   python encoder_preprocess.py /path/to/datasets
   python encoder_train.py my_encoder /path/to/datasets/SV2TTS/encoder
   ```

   By default, preprocessing writes to `<datasets_root>/SV2TTS/encoder/`; training writes checkpoints under `saved_models/my_encoder/`.

2. **Prepare and train the synthesizer.** By default, audio preprocessing uses `LibriSpeech/train-clean-100` and `LibriSpeech/train-clean-360` beneath the datasets root and expects the alignment files used by this pipeline. It writes audio, mel data, and metadata to `<datasets_root>/SV2TTS/synthesizer/`. For datasets without alignment files, `--no_alignments` selects the sidecar-text path; audio files need matching `.txt` or `.normalized.txt` files in the expected speaker/book directory structure.

   ```bash
   python synthesizer_preprocess_audio.py /path/to/datasets
   python synthesizer_preprocess_embeds.py /path/to/datasets/SV2TTS/synthesizer \
       --encoder_model_fpath saved_models/my_encoder/encoder.pt
   python synthesizer_train.py my_synthesizer /path/to/datasets/SV2TTS/synthesizer
   ```

   The embedding step uses the trained encoder. Synthesizer checkpoints are written to `saved_models/my_synthesizer/synthesizer.pt` by default.

3. **Prepare and train the vocoder.** `vocoder_preprocess.py` generates ground-truth-aligned (GTA) spectrograms with a synthesizer checkpoint. The default input and output directories are `<datasets_root>/SV2TTS/synthesizer/` and `<datasets_root>/SV2TTS/vocoder/`.

   ```bash
   python vocoder_preprocess.py /path/to/datasets \
       --syn_model_fpath saved_models/my_synthesizer/synthesizer.pt
   python vocoder_train.py my_vocoder /path/to/datasets
   ```

   Alternatively, `vocoder_train.py --ground_truth` trains using the synthesizer's ground-truth mel spectrograms instead of GTA spectrograms. Vocoder checkpoints are written to `saved_models/my_vocoder/vocoder.pt` by default.

The preprocessing and training scripts expose options to change output locations, skip existing data, choose datasets, and configure training. Review each script's `--help` before adapting the examples. Training can require substantial data, storage, and compute; no particular runtime or hardware requirement is specified here.

## Samples and licensing

The source code's top-level license is [MIT](LICENSE.md). The synthesizer and vocoder directories also include license files. The sample recordings have separate dataset notices and terms described in [`samples/README.md`](samples/README.md) and [`samples/VCTK.txt`](samples/VCTK.txt); do not assume the source-code license covers those recordings or external datasets.
