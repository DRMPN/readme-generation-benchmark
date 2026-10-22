# SV2TTS

SV2TTS is a speaker-conditioned speech synthesis project. It combines three components: a **speaker encoder** that creates a voice embedding from reference audio, a **Tacotron synthesizer** that generates a mel spectrogram from text and that embedding, and a **WaveRNN vocoder** that converts the spectrogram into a waveform. The repository includes inference demos, a graphical toolbox, preprocessing scripts, and training scripts for each component.

## Setup

Use an environment with the project’s Python dependencies installed. The dependency list is in [`requirements.txt`](requirements.txt):

```bash
python -m pip install -r requirements.txt
```

Some audio preprocessing and silence trimming uses `webrtcvad`. It is recommended for trimming; `encoder_preprocess.py` requires it unless you pass `--no_trim`. The toolbox also uses audio input/output devices for recording and playback, so those features depend on compatible devices and audio support in your environment.

The inference demos expect model files under `saved_models/default/`. The scripts call `ensure_default_models` to download the default encoder, synthesizer, and vocoder weights when they are missing or have unexpected sizes. This requires access to the download URLs. You can also use your own model files with the command-line options described below.

## Usage

### Interactive command-line demo

Run:

```bash
python demo_cli.py
```

The script checks that the encoder, synthesizer, and vocoder can load and process small test inputs. It then prompts for a reference audio file and text to synthesize. Reference audio can be supplied in common formats such as MP3, WAV, M4A, or FLAC. Generated speech is saved in the current directory as `demo_output_00.wav`, `demo_output_01.wav`, and so on.

Useful options include:

- `-e`, `-s`, and `-v`: paths to encoder, synthesizer, and vocoder model files.
- `--cpu`: force CPU inference, even if a GPU is available.
- `--no_sound`: save output without attempting playback.
- `--seed N`: provide a seed for repeatable generation.

For example:

```bash
python demo_cli.py --cpu --no_sound
```

### Graphical toolbox

Launch the desktop interface with:

```bash
python demo_toolbox.py
```

Use `-d` to provide a datasets directory and `-m` to choose the models directory:

```bash
python demo_toolbox.py --datasets_root /path/to/datasets --models_dir saved_models
```

The toolbox lets you load or record reference utterances, select models, enter text, and generate speech. It can display speaker embeddings and UMAP projections, play generated audio, and export it. If no vocoder model is selected, the toolbox offers Griffin–Lim spectrogram inversion instead. The `--cpu` and `--seed` options are also available.

The dataset browser recognizes LibriSpeech, LibriTTS, LJSpeech, VoxCeleb, and VCTK directory layouts listed in `toolbox/__init__.py`. A dataset directory is optional for recording or browsing files directly, but pretrained encoder and synthesizer model files must be present in the models directory for the toolbox to start.

## Training

Training is organized as a staged workflow. Dataset paths below are examples; adjust them to match your extracted data.

### 1. Prepare and train the speaker encoder

The encoder preprocessing script accepts LibriSpeech “other” training data, VoxCeleb1, and VoxCeleb2. The expected layout and defaults are described by:

```bash
python encoder_preprocess.py --help
```

For example:

```bash
python encoder_preprocess.py /path/to/datasets
python encoder_train.py encoder_run /path/to/datasets/SV2TTS/encoder
```

Preprocessing writes speaker directories containing mel-spectrogram arrays and source metadata. The default output directory is `<datasets_root>/SV2TTS/encoder`. Use `--datasets` to select a comma-separated subset of `librispeech_other`, `voxceleb1`, and `voxceleb2`; `--skip_existing` can help resume interrupted preprocessing. Encoder training outputs checkpoints and visualizations beneath `saved_models/<run_id>/`. It resumes from an existing checkpoint unless `-f` is supplied.

### 2. Prepare and train the synthesizer

The synthesizer audio preprocessor defaults to LibriSpeech `train-clean-100` and `train-clean-360` subfolders and writes data to `<datasets_root>/SV2TTS/synthesizer`:

```bash
python synthesizer_preprocess_audio.py /path/to/datasets
python synthesizer_preprocess_embeds.py /path/to/datasets/SV2TTS/synthesizer
python synthesizer_train.py synthesizer_run /path/to/datasets/SV2TTS/synthesizer
```

Embedding creation uses the encoder weights at `saved_models/default/encoder.pt` by default; override them with `-e`. Audio preprocessing can be configured with `--datasets_name`, `--subfolders`, `--n_processes`, and `--hparams`. For datasets without alignment files, use `--no_alignments`; this mode expects audio files with matching text files. Synthesizer training writes checkpoints and diagnostic outputs under the selected models directory.

### 3. Prepare and train the vocoder

Generate ground-truth-aligned (GTA) mel spectrograms with a trained synthesizer, then train the vocoder:

```bash
python vocoder_preprocess.py /path/to/datasets
python vocoder_train.py vocoder_run /path/to/datasets
```

By default, preprocessing reads synthesizer data from `<datasets_root>/SV2TTS/synthesizer` and writes GTA mels to `<datasets_root>/SV2TTS/vocoder`. Vocoder training uses those GTA mels; pass `-g` to train against the original ground-truth spectrograms instead. Training outputs are stored under `saved_models/<run_id>/`. Each training script provides `--help` for checkpoint, restart, output-directory, and other options.

## Configuration

Audio and model parameters are defined in Python modules:

- `encoder/params_data.py` contains encoder sampling, mel, silence-detection, and volume-normalization settings.
- `encoder/params_model.py` contains encoder dimensions, batch settings, and learning rate.
- `synthesizer/hparams.py` defines shared synthesizer and vocoder audio settings, text-to-speech parameters, preprocessing options, and the training schedule.
- `vocoder/hparams.py` defines WaveRNN architecture, quantization, training, and generation settings. Its audio settings are based on the synthesizer hyperparameters.

Synthesizer and vocoder preprocessing/training scripts accept `--hparams` overrides as comma-separated `name=value` pairs. The demo scripts accept explicit model paths, and the toolbox discovers model files named `encoder.pt`, `synthesizer.pt`, and `vocoder.pt` in model subdirectories.

## Development and testing

The repository is organized into `encoder/`, `synthesizer/`, `vocoder/`, `toolbox/`, and shared `utils/` packages. The top-level scripts are the main entry points for demos, preprocessing, and training. There is no separate test suite shown in the repository tree. As a practical smoke test, run `demo_cli.py`: it exercises the three inference components with small inputs before entering the interactive generation loop. The included sample audio files are provided for toolbox testing and benchmarking; their dataset notices are in `samples/README.md` and `samples/VCTK.txt`.

For encoder training visualizations, the code connects to a Visdom server by default. Start one with `visdom` before training, or use `--no_visdom` to disable Visdom.

## License

The project’s [`LICENSE.md`](LICENSE.md) applies the MIT License to the project work and includes copyright notices for the listed contributors. The synthesizer and vocoder directories also contain their own MIT license files. Sample audio has separate dataset terms: consult `samples/README.md` and `samples/VCTK.txt` before reuse.
