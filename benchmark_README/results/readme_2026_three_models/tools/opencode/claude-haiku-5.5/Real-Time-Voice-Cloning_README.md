# Real-Time Voice Cloning

This repository is an implementation of SV2TTS, a three-stage system for cloning a speaker's voice from a short reference recording. It contains:

- a **speaker encoder** that turns a reference utterance into a fixed-size speaker embedding,
- a **synthesizer** (Tacotron-style) that turns text plus a speaker embedding into a mel spectrogram,
- a **vocoder** (WaveRNN-style) that turns a mel spectrogram into a waveform, with Griffin-Lim available as a non-neural alternative in the toolbox.

The repository provides a graphical toolbox, a command-line demo, and training and preprocessing scripts for each stage.

Sample reference audio used for testing is in [`samples/`](samples/README.md).

## Requirements

- Python with the packages listed in `requirements.txt`:
  `inflect==5.3.0`, `librosa==0.8.1`, `matplotlib==3.5.1`, `numpy==1.20.3`, `Pillow==8.4.0`, `PyQt5==5.15.6`, `scikit-learn==1.0.2`, `scipy==1.7.3`, `sounddevice==0.4.3`, `SoundFile==0.10.3.post1`, `tqdm==4.62.3`, `umap-learn==0.5.2`, `Unidecode==1.3.2`, `urllib3==1.26.7`, `visdom==0.1.8.9`, `webrtcvad==2.0.10`
- PyTorch. It is used throughout the code but is **not** listed in `requirements.txt`, so install it separately. No version is pinned in the repository.
- `webrtcvad` is needed for silence trimming during encoder preprocessing (use `--no_trim` to skip it) and for the toolbox's "Enhance vocoder output" option, which is disabled when it is not importable.
- A GPU is optional. The toolbox, the CLI demo, and `vocoder_preprocess.py` accept a `--cpu` flag.

Install the requirements:

```bash
pip install -r requirements.txt
```

## Pretrained models

The demo scripts download three pretrained models on first run, if they are not already present, into `saved_models/default/`:

| File | Approximate size (bytes) |
|---|---|
| `encoder.pt` | 17,090,379 |
| `synthesizer.pt` | 370,554,559 |
| `vocoder.pt` | 53,845,290 |

The files are fetched from Google Drive by `utils/default_models.py`. A file is re-downloaded if its size does not match. If a download fails, the script stops with an error that links to the manual download folder: https://drive.google.com/drive/folders/1fU6umc5uQAVR2udZdHX-lDgXYzTyqG_j

Models you train yourself are saved under `saved_models/<run_id>/` (see [Training](#training)).

## Usage

### Graphical toolbox

```bash
python demo_toolbox.py -d <datasets_root>
```

Options:

- `-d, --datasets_root`: directory containing your datasets. Optional; you can also load audio files directly.
- `-m, --models_dir`: directory containing saved models (default `saved_models`). The toolbox looks for `*/encoder.pt`, `*/synthesizer.pt`, and `*/vocoder.pt` inside it. The vocoder list also includes Griffin-Lim.
- `--cpu`: run all inference on the CPU.
- `--seed`: optional random seed to make generation deterministic.

The toolbox recognizes the following dataset layouts under `<datasets_root>`:

- LibriSpeech: `dev-clean`, `dev-other`, `test-clean`, `test-other`, `train-clean-100`, `train-clean-360`, `train-other-500`
- LibriTTS: `dev-clean`, `dev-other`, `test-clean`, `test-other`, `train-clean-100`, `train-clean-360`, `train-other-500`
- `LJSpeech-1.1`
- `VoxCeleb1/wav`, `VoxCeleb1/test_wav`
- `VoxCeleb2/dev/aac`, `VoxCeleb2/test/aac`
- `VCTK-Corpus/wav48`

The toolbox can also load a file from disk and can record five seconds from a microphone. Generated audio can be replayed and exported as WAV.

### Command-line demo

```bash
python demo_cli.py
```

Options:

- `-e, --enc_model_fpath` (default `saved_models/default/encoder.pt`)
- `-s, --syn_model_fpath` (default `saved_models/default/synthesizer.pt`)
- `-v, --voc_model_fpath` (default `saved_models/default/vocoder.pt`)
- `--cpu`: run on the CPU even if a GPU is available.
- `--no_sound`: do not play audio. Audio is still saved.
- `--seed`: optional random seed for determinism.

The script first runs a self-test on dummy inputs, then loops. For each round it asks for a reference audio file path, then for a sentence (about 20 words). It saves the result as `demo_output_00.wav`, `demo_output_01.wav`, and so on in the current directory. Playback uses `sounddevice`; if the audio device fails, the script continues without playback.

## Training

Each stage has its own preprocessing and training script. Stages depend on each other, so run them in this order.

### 1. Speaker encoder

Preprocess (datasets: `librispeech_other`, `voxceleb1`, `voxceleb2`, selected with `-d`):

```bash
python encoder_preprocess.py <datasets_root>
```

Output defaults to `<datasets_root>/SV2TTS/encoder/`. The expected layout is described in the script's help text (`LibriSpeech/`, `VoxCeleb1/`, `VoxCeleb2/` side by side under `<datasets_root>`).

Train:

```bash
python encoder_train.py <run_id> <datasets_root>/SV2TTS/encoder
```

### 2. Synthesizer

Preprocess audio into mel spectrograms and copies of the audio. By default this reads `LibriSpeech/train-clean-100` and `LibriSpeech/train-clean-360` under `<datasets_root>`; use `--datasets_name` and `--subfolders` to change this:

```bash
python synthesizer_preprocess_audio.py <datasets_root>
```

Create speaker embeddings from the trained encoder (the default encoder is `saved_models/default/encoder.pt`; use `-e` to change it):

```bash
python synthesizer_preprocess_embeds.py <datasets_root>/SV2TTS/synthesizer
```

Train:

```bash
python synthesizer_train.py <run_id> <datasets_root>/SV2TTS/synthesizer
```

### 3. Vocoder

Optional: create ground-truth-aligned mel spectrograms with a trained synthesizer (default `saved_models/default/synthesizer.pt`; use `-s` to change it):

```bash
python vocoder_preprocess.py <datasets_root>
```

Train on the synthesizer's audio paired with GTA mels (default), or with ground-truth mels using `-g`:

```bash
python vocoder_train.py <run_id> <datasets_root>
```

### Training options

Each training script accepts `-m/--models_dir` (default `saved_models`), `-s/--save_every`, `-b/--backup_every`, and `-f/--force_restart`. Running again with the same `run_id` resumes from the saved state unless `-f` is passed. The encoder also has `-v`, `-u`, `--visdom_server`, and `--no_visdom` options for its visualizations.

Hyperparameters for the synthesizer and vocoder are in `synthesizer/hparams.py` and `vocoder/hparams.py`. The synthesizer and some preprocessing scripts accept overrides through `--hparams name=value,...`.

## Repository layout

| Path | Contents |
|---|---|
| `demo_toolbox.py`, `toolbox/` | Graphical toolbox (PyQt5) |
| `demo_cli.py` | Command-line demo |
| `encoder/` | Speaker encoder: model, audio preprocessing, datasets, training, inference |
| `synthesizer/` | Tacotron-style synthesizer: model, text cleaners, preprocessing, training, inference |
| `vocoder/` | WaveRNN-style vocoder: models (`fatchord_version.py`, `deepmind_version.py`), preprocessing, training, inference |
| `utils/` | Shared helpers, including default-model download (`default_models.py`) and a log-MMSE noise filter (`logmmse.py`) |
| `*_preprocess*.py`, `*_train.py` | Entry points for the training pipeline |
| `samples/` | Reference audio files and their source notices |

## License

The code is released under the MIT License. See [`LICENSE.md`](LICENSE.md). It lists the original authors of the code this project builds on. The `vocoder/` and `synthesizer/` directories also include their own `LICENSE.txt` files.

The audio in `samples/` comes from VCTK and LibriSpeech and is subject to their own licenses. See [`samples/README.md`](samples/README.md) and `samples/VCTK.txt`.
