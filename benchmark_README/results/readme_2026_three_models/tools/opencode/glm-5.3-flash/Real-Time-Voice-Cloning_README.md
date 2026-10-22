# Real-Time Voice Cloning

A PyTorch implementation of the **SV2TTS toolbox** — speaker encoding, text-to-speech synthesis, and waveform generation in three stages, so that arbitrary text can be spoken with the voice of a provided reference speaker.

The project implements *Transfer Learning from Speaker Verification to Multispeaker Text-To-Speech Synthesis* (SV2TTS). The reference audio samples used by the SV2TTS authors are available on the [publication page](https://google.github.io/tacotron/publications/speaker_adaptation/index.html).

## How it works

The pipeline is split into three independently trainable networks:

| Component | Model | Role |
|-----------|-------|------|
| Encoder | 3-layer LSTM (hidden size 256), producing 256-dimensional speaker embeddings from 16 kHz audio | Extracts a speaker embedding from a reference utterance |
| Synthesizer | Speaker-conditional Tacotron | Generates an 80-band mel spectrogram at 16 kHz from text and a speaker embedding |
| Vocoder | WaveRNN | Converts the mel spectrogram into an audio waveform |

Architecture and signal-processing parameters live in `encoder/params_model.py`, `encoder/params_data.py`, `synthesizer/hparams.py`, and `vocoder/hparams.py`.

## Installation

1. Install **PyTorch** following the [official instructions](https://pytorch.org/) for your platform. It is required by every script but is not listed in `requirements.txt` (so you can pick the CPU or CUDA build yourself). If no GPU is available, everything also runs on CPU.
2. Install the remaining dependencies:

   ```
   pip install -r requirements.txt
   ```

   This includes, among others: `librosa`, `numpy`, `scipy`, `PyQt5` (toolbox GUI), `sounddevice` (audio playback and recording), `SoundFile`, `matplotlib`, `tqdm`, `umap-learn` (embedding projections), `visdom` (encoder training plots), and `webrtcvad` (voice activity detection, used for silence trimming).

## Pretrained models

Three pretrained models are provided (encoder, synthesizer, vocoder). They are **downloaded automatically** the first time you run `demo_toolbox.py` or `demo_cli.py`, and are stored under `saved_models/default/`:

- `encoder.pt` (~17 MB)
- `synthesizer.pt` (~370 MB)
- `vocoder.pt` (~54 MB)

If the automatic download fails, the models can be fetched manually from this [Google Drive folder](https://drive.google.com/drive/folders/1fU6umc5uQAVR2udZdHX-lDgXYzTyqG_j) and placed in `saved_models/default/`.

## Usage

### Graphical toolbox

```
python demo_toolbox.py
```

Pass `-d <datasets_root>` if you want to browse local datasets from within the toolbox. Other options: `-m/--models_dir` (default `saved_models`), `--cpu`, and `--seed` for deterministic generation.

The toolbox lets you:

- Select utterances from supported datasets or from arbitrary audio files on disk.
- Record 5-second utterances from your microphone (requires an input audio device).
- Compute and display speaker embeddings, including a UMAP projection of all loaded utterances.
- Synthesize spectrograms from text (each line is synthesized as a separate utterance) and vocode them with WaveRNN, or fall back to Griffin-Lim.
- Play and export the generated audio, and optionally trim silences from the output using `webrtcvad`.

### Command-line demo

```
python demo_cli.py
```

This GUI-less script is also a worked example of how to interface the three models from your own code. For each iteration it asks for:

1. A reference audio file (mp3, wav, m4a, flac, ...) from which the speaker embedding is computed.
2. A sentence (~20 words) to synthesize.

The generated waveform is played (unless `--no_sound` is passed) and saved as `demo_output_XX.wav`. Additional flags: `-e`, `-s`, `-v` to point to custom encoder/synthesizer/vocoder weights, `--cpu`, and `--seed`.

In short, the programmatic API is:

```python
preprocessed_wav = encoder.preprocess_wav(fpath)   # load & preprocess reference audio
embed = encoder.embed_utterance(preprocessed_wav)  # speaker embedding
spec = synthesizer.synthesize_spectrograms([text], [embed])  # mel spectrogram
wav = vocoder.infer_waveform(spec[0])              # waveform
```

See `demo_cli.py` for a complete, commented example.

## Training your own models

### 1. Prepare the datasets

Download and extract the datasets you want into a single directory, e.g.:

```
-[datasets_root]
  -LibriSpeech
    -train-other-500
  -VoxCeleb1
    -wav
    -vox1_meta.csv
  -VoxCeleb2
    -dev
```

Preprocessing scripts write their outputs under `<datasets_root>/SV2TTS/{encoder,synthesizer,vocoder}/`.

### 2. Encoder

```
python encoder_preprocess.py <datasets_root>
python encoder_train.py <run_id> <datasets_root>/SV2TTS/encoder
```

- Preprocessing uses the train sets of `librispeech_other`, `voxceleb1`, and `voxceleb2` by default (selectable with `-d`); at least one of the three datasets is required, ideally all three.
- Training visualizes loss, plots, and UMAP projections with [visdom](https://github.com/facebookresearch/visdom) (`--no_visdom` to disable). Model weights are saved to `saved_models/<run_id>/`.

### 3. Synthesizer

```
python synthesizer_preprocess_audio.py <datasets_root>
python synthesizer_preprocess_embeds.py <datasets_root>/SV2TTS/synthesizer
python synthesizer_train.py <run_id> <datasets_root>/SV2TTS/synthesizer
```

- Audio preprocessing defaults to `LibriSpeech` with the `train-clean-100` and `train-clean-360` subfolders (override with `--datasets_name` and `--subfolders`). Use `--no_alignments` for datasets that do not include alignment files.
- Embed preprocessing computes speaker embeddings for the training utterances using an encoder checkpoint (default: `saved_models/default/encoder.pt`).

### 4. Vocoder

```
python vocoder_preprocess.py <datasets_root>
python vocoder_train.py <run_id> <datasets_root>
```

- Preprocessing creates ground-truth aligned (GTA) spectrograms with the synthesizer model (default: `saved_models/default/synthesizer.pt`).
- By default the vocoder trains on the GTA spectrograms; pass `--ground_truth` to train on ground-truth spectrograms instead.

All training scripts accept `-s/--save_every` and `-b/--backup_every` (in steps), and `-f/--force_restart`. A run resumes automatically from previously saved weights with the same run ID.

## Supported datasets

The toolbox browser recognizes the following dataset directories under `<datasets_root>`:

- `LibriSpeech/{dev-clean,dev-other,test-clean,test-other,train-clean-100,train-clean-360,train-other-500}`
- `LibriTTS/{dev-clean,dev-other,test-clean,test-other,train-clean-100,train-clean-360,train-other-500}`
- `LJSpeech-1.1`
- `VoxCeleb1/{wav,test_wav}`
- `VoxCeleb2/{dev,test}/aac`
- `VCTK-Corpus/wav48`

## Repository structure

```
├── demo_cli.py                        GUI-less demo and API example
├── demo_toolbox.py                    Launches the toolbox GUI
├── encoder_preprocess.py              Encoder data preprocessing
├── encoder_train.py                   Encoder training
├── synthesizer_preprocess_audio.py    Synthesizer audio preprocessing
├── synthesizer_preprocess_embeds.py   Speaker embedding preprocessing
├── synthesizer_train.py               Synthesizer training
├── vocoder_preprocess.py              Vocoder preprocessing (GTA mels)
├── vocoder_train.py                   Vocoder training
├── encoder/                           Speaker encoder (LSTM, GE2E-style training)
├── synthesizer/                       Tacotron synthesizer and text cleaners
├── vocoder/                           WaveRNN vocoder
├── toolbox/                           PyQt5 GUI implementation
├── utils/                             Shared utilities (model downloads, args, ...)
└── samples/                           Reference audio clips for testing
```

## Samples

The clips in [`samples/`](samples/) are provided for toolbox testing and benchmarking. They are the same reference utterances used by the SV2TTS authors. `p240_00000.mp3` and `p260_00000.mp3` are compressed versions of audio from the [VCTK corpus](https://datashare.is.ed.ac.uk/handle/10283/3443) (see `samples/VCTK.txt` for copyright notices); `1320_00000.mp3`, `3575_00000.mp3`, `6829_00000.mp3`, and `8230_00000.mp3` come from the [LibriSpeech](https://openslr.org/12) corpus (CC BY 4.0). See [`samples/README.md`](samples/README.md) for details.

## License

Released under the [MIT License](LICENSE.md). Modified and original work Copyright (c) 2019 Corentin Jemine. This repository builds on original work by Rayhane Mama (Tacotron implementation), fatchord (WaveRNN implementation), and braindead.
