# SV2TTS Voice Cloning Toolbox

This repository contains a Python implementation of a three-stage speech synthesis pipeline based on SV2TTS. It has a speaker encoder, a synthesizer (Tacotron-based), and a vocoder (WaveRNN-based). It can clone a voice from a short reference recording and generate speech from text in that voice. The project provides a graphical toolbox, command-line demo, and training and preprocessing scripts.

## Overview

The system is composed of three models, each with its own package:

- **Encoder** (`encoder/`): A speaker encoder built from an LSTM followed by a linear layer and L2 normalization. It maps mel spectrogram partials of an utterance to a fixed-size speaker embedding (256 dimensions by default). It is trained with a GE2E-style softmax loss and reports an equal error rate (EER).
- **Synthesizer** (`synthesizer/`): A Tacotron-style model that converts text and a speaker embedding into a mel spectrogram. The code also includes preprocessing, GTA (ground-truth-aligned) synthesis, and dataset handling.
- **Vocoder** (`vocoder/`): A WaveRNN-style model that converts mel spectrograms into waveforms. A Griffin-Lim option is also available in the toolbox.

The `samples/` directory contains reference utterances for testing and benchmarking the toolbox. Its README states that these are the same reference utterances used by the SV2TTS authors. The samples include two VCTK-derived files and four LibriSpeech-derived files, each with its own license notice.

## Requirements and Setup

1. Clone the repository and change into its directory.
2. Install the dependencies listed in `requirements.txt`. The file's contents are not included in this README's source, so check it for exact versions. The code requires PyTorch, librosa, NumPy, SoundFile, SciPy, scikit-learn, tqdm, umap, and visdom. The toolbox also uses PyQt5, matplotlib, and sounddevice.
3. Optionally install `webrtcvad`. The encoder preprocessing script requires it unless you pass `--no_trim`. The toolbox also uses it for the "Enhance vocoder output" option, which trims excess silence and is disabled when `webrtcvad` is not installed.

### Pretrained models

`utils/default_models.py` defines three default models (encoder, synthesizer, and vocoder). Each is downloaded on startup into `saved_models/default/` if it is missing or has an unexpected file size. If automatic download fails, the code prints a manual download location: `https://drive.google.com/drive/folders/1fU6umc5uQAVR2udZdHX-lDgXYzTyqG_j`. Manually downloaded files should be placed at `saved_models/default/encoder.pt`, `synthesizer.pt`, and `vocoder.pt`.

## Usage

### Command-line demo

`demo_cli.py` tests your configuration and then runs an interactive loop. It asks for a reference audio file path, computes an embedding, and asks for text to synthesize. Each result is saved as `demo_output_XX.wav` in the current directory.

```bash
python demo_cli.py
```

Options:

| Option | Default | Description |
|---|---|---|
| `-e, --enc_model_fpath` | `saved_models/default/encoder.pt` | Encoder weights |
| `-s, --syn_model_fpath` | `saved_models/default/synthesizer.pt` | Synthesizer weights |
| `-v, --voc_model_fpath` | `saved_models/default/vocoder.pt` | Vocoder weights |
| `--cpu` | off | Run on CPU even if a GPU is available |
| `--no_sound` | off | Do not play audio |
| `--seed` | None | Random seed for deterministic output |

### Graphical toolbox

`demo_toolbox.py` launches the SV2TTS toolbox window.

```bash
python demo_toolbox.py -d <datasets_root>
```

Options:

| Option | Default | Description |
|---|---|---|
| `-d, --datasets_root` | None | Directory containing your datasets |
| `-m, --models_dir` | `saved_models` | Directory containing saved models |
| `--cpu` | off | Run all inference on CPU |
| `--seed` | None | Random seed for deterministic output |

The toolbox looks for datasets under the root directory using the names listed in `toolbox/__init__.py`, such as `LibriSpeech/train-clean-100`, `LibriTTS/dev-clean`, `VoxCeleb1/wav`, `VCTK-Corpus/wav48`, and `LJSpeech-1.1`. If none are found, it still runs, and you can record or browse audio files instead. The toolbox also supports loading individual files in mp3, flac, wav, and m4a formats. It can record five seconds of audio from an input device. The toolbox keeps up to 15 generated waveforms in memory (`MAX_WAVS = 15`).

The toolbox window lets you select an encoder, synthesizer, and vocoder. Griffin-Lim is available as a vocoder option when no vocoder weights are used.

### Training and preprocessing pipeline

Training is performed in stages. The scripts below are shown in dependency order.

1. **Encoder preprocessing** (`encoder_preprocess.py`) reads the datasets and writes mel spectrograms. The default datasets are `librispeech_other`, `voxceleb1`, and `voxceleb2`. The default output directory is `<datasets_root>/SV2TTS/encoder/`.

   ```bash
   python encoder_preprocess.py <datasets_root>
   ```

2. **Encoder training** (`encoder_train.py`) trains the speaker encoder on the preprocessed data.

   ```bash
   python encoder_train.py <run_id> <datasets_root>/SV2TTS/encoder/
   ```

3. **Synthesizer preprocessing** (`synthesizer_preprocess_audio.py`) writes mels, audio, and a `train.txt` metadata file. By default it processes `train-clean-100` and `train-clean-360` under `LibriSpeech`. Options include `--datasets_name`, `--subfolders`, and `--no_alignments`.

   ```bash
   python synthesizer_preprocess_audio.py <datasets_root>
   ```

4. **Synthesizer embedding creation** (`synthesizer_preprocess_embeds.py`) computes speaker embeddings for the synthesizer training data using a trained encoder.

   ```bash
   python synthesizer_preprocess_embeds.py <datasets_root>/SV2TTS/synthesizer/
   ```

5. **Synthesizer training** (`synthesizer_train.py`)

   ```bash
   python synthesizer_train.py <run_id> <datasets_root>/SV2TTS/synthesizer/
   ```

6. **Vocoder preprocessing** (`vocoder_preprocess.py`) generates ground-truth-aligned (GTA) mel spectrograms using a trained synthesizer.

   ```bash
   python vocoder_preprocess.py <datasets_root>
   ```

7. **Vocoder training** (`vocoder_train.py`). Pass `--ground_truth` to train on ground-truth spectrograms instead of GTA spectrograms.

   ```bash
   python vocoder_train.py <run_id> <datasets_root>
   ```

Each training script writes outputs to `saved_models/<run_id>/` by default. Training restarts from a saved checkpoint with the same run ID unless `-f` (force restart) is passed.

## Configuration

Configuration is spread across several Python modules rather than a single file.

- **Encoder audio and data parameters** (`encoder/params_data.py`): mel window length and step, number of mel channels, sampling rate (16000 Hz), partial utterance frame counts, VAD settings, and the target volume in dBFS.
- **Encoder model and training parameters** (`encoder/params_model.py`): hidden size, embedding size, number of LSTM layers, learning rate, speakers per batch, and utterances per speaker.
- **Dataset lists** (`encoder/config.py`): dataset subfolders used by the encoder, including LibriSpeech, LibriTTS, and VoxCeleb paths.
- **Synthesizer hyperparameters** (`synthesizer/hparams.py`): audio processing, Tacotron architecture, the training schedule (`tts_schedule`), and SV2TTS settings.
- **Vocoder hyperparameters** (`vocoder/hparams.py`): settings that match the synthesizer's audio parameters, plus WaveRNN architecture, training batch size, learning rate, and generation options.
- **Toolbox datasets** (`toolbox/__init__.py`): the `recognized_datasets` list.

For the synthesizer preprocessing and training scripts, `--hparams` accepts comma-separated `name=value` overrides. The values are parsed with `ast.literal_eval`.

Several scripts also accept options for output directories, save and backup intervals, visualization frequency, and Visdom. For example, `encoder_train.py` supports `--visdom_server` and `--no_visdom`. The encoder training code writes plots and UMAP projections and can send them to a Visdom server. Start a Visdom server before training if you want those visualizations.

## Development

The repository is organized into these packages:

- `encoder/`: speaker encoder model, audio processing, training, inference, and data objects (`encoder/data_objects/`)
- `synthesizer/`: Tacotron model, text cleaners and symbols (`synthesizer/utils/`), dataset, training, and synthesis
- `vocoder/`: WaveRNN models (`vocoder/models/`), distribution utilities, dataset, training, and generation
- `toolbox/`: PyQt5 user interface, utterance handling, and the toolbox controller
- `utils/`: argument printing, default model download, profiler, and log-MMSE noise reduction

The entry-point scripts are at the top level of the repository. Each one parses command-line arguments and calls into the corresponding package.

Some files state that they are derived from other projects. `utils/logmmse.py` is MIT-licensed by braindead and was extracted from the `logmmse` package. The synthesizer and vocoder code is based on work by Rayhane Mama and fatchord, as noted in their license files.

The code contains some `TODO` and `FIXME` comments. For example, `encoder/train.py` notes that the gradient is `None` if the loss device is CUDA, so the loss is computed on the CPU.

## Testing

The repository does not include a dedicated test suite. The tree contains no test files or test runner configuration.

Testing options that are present:

- **Configuration self-test:** `demo_cli.py` runs a check when it starts. It forwards a one-second array of zeros through the encoder, synthesizes two short texts with batching, and vocodes the result with reduced parameters. It prints "All test passed!" when this completes.
- **Sample audio:** The `samples/` folder contains reference utterances for toolbox testing and benchmarking.

## License

The main project is licensed under the MIT License, as stated in `LICENSE.md`. That file lists copyright notices for Corentin Jemine (2019), Rayhane Mama (2018), fatchord (2019), and braindead (2015).

Subcomponents have their own license files:

- `synthesizer/LICENSE.txt`: MIT License, with notices for Rayhane Mama, fatchord, Corentin Jemine, and blue-fish.
- `vocoder/LICENSE.txt`: MIT License, with notices for fatchord and Corentin Jemine.
- `utils/logmmse.py`: MIT License, Copyright (c) 2015 braindead.

The sample audio files have separate terms. `samples/VCTK.txt` contains the CSTR VCTK Corpus notice, which is licensed under Creative Commons Attribution 4.0 International. `samples/README.md` includes the LibriSpeech notice, which is also licensed under Creative Commons Attribution 4.0 International.
