# Real-Time-Voice-Cloning<h2>Description</h2>

<p>This project is a <strong>Real-Time Voice Cloning</strong> toolbox that aims to clone a voice from just a short audio sample of a target speaker, and then use that cloned voice to generate arbitrary speech in real time.</p>

<p>The implementation is based on the paper <em><a href="https://github.com/CorentinJ/Real-Time-Voice-Cloning">Transfer Learning from Speaker Verification to Multispeaker Text-To-Speech Synthesis</a></em> (SV2TTS). It consists of three components, trained independently:</p>

<ol>
<li><strong>Encoder</strong> — a speaker verification network that creates a fixed-dimensional embedding (a numerical "voice fingerprint") from a short utterance of a target speaker.</li>
<li><strong>Synthesizer</strong> — a text-to-speech model (based on Tacotron 2) that generates a mel spectrogram from text, conditioned on the speaker embedding produced by the encoder.</li>
<li><strong>Vocoder</strong> — a network (WaveNet-based) that converts the generated mel spectrograms into audible waveforms.</li>
</ol>

<p>The three models are chained together: a few seconds of audio from a speaker are embedded by the encoder, and the synthesizer plus vocoder then generate speech in that speaker's voice from any given text. The demo tool also supports running this pipeline in real time.</p>

<p>This repository is a fork of the original work by <a href="https://github.com/Rayhane-mamah">Rayhane-mamah</a> and <a href="https://github.com/fatchord">fatchord</a>, with modifications by <a href="https://github.com/CorentinJ">CorentinJ</a> and <a href="https://github.com/blue-fish">blue-fish</a>. It is released under the MIT License — see the license headers in the repository for full copyright and attribution details.</p>
<h2>Requirements</h2>

<p>This project is written in Python. To install the required Python packages, run:</p>

<p><code>
pip install -r requirements.txt
</code></p>

<p>The project relies on several major libraries, including:</p>

<ul>
<li><strong>PyTorch</strong> – used for training and running the neural network models (encoder, synthesizer, vocoder).</li>
<li><strong>TensorFlow</strong> – used for tensorboard logging during training.</li>
<li><strong>librosa</strong> – audio loading and processing (resampling, mel spectrograms, volume normalization).</li>
<li><strong>numpy, scipy</strong> – numerical computation and signal processing.</li>
<li><strong>webrtcvad</strong> – voice activity detection, used to segment and filter out silence in utterances.</li>
</ul>

<p>If you plan to train the models (or run inference with the vocoder), a GPU with CUDA support is strongly recommended, as inference and training on CPU is very slow.</p>
<h2>Installation</h2>

<h3>Requirements</h3>

<p>You will need Python 3 and a pip installation. The required Python packages can be installed with:</p>

<p><code>
pip install -r requirements.txt
</code></p>

<h3>GPU</h3>

<p>The models in this project are trained (and inference is typically run) on a GPU. If you intend to train the models yourself, make sure that your PyTorch installation is built with CUDA support and that your GPU drivers are properly configured.</p>

<h3>Getting the pre-trained models</h3>

<p>If you don't want to train the models yourself, you can download the pre-trained weights and place them in the <code>saved_models/</code> directory (or pass the path to your own directory via the <code>-m/--models_dir</code> argument, which defaults to <code>saved_models</code>). The tools in the toolbox will look for the encoder, synthesizer and vocoder weights in this directory.</p>

<h3>Datasets (optional)</h3>

<p>If you plan on training the models yourself, you will need to download the datasets and preprocess them. The preprocessing scripts will create the prepared data under a datasets root directory, which by default is used as <code>&lt;datasets_root&gt;/SV2TTS/</code> for the encoder/synthesizer/vocoder data (e.g. the GTA synthesized mel spectrograms used for vocoder training go in <code>&lt;datasets_root&gt;/SV2TTS/vocoder/</code>). You can pass the location of your datasets with the appropriate <code>--datasets_root</code> argument to the training scripts.</p>
<h2>Usage</h2>

<h3>1. Getting started</h3>

<p>Once you have installed the requirements (see the <a href="#installation">Installation</a> section of the repository), download the pretrained models as described in the repository, and place them in the <code>saved_models</code> directory.</p>

<h3>2. Demo Toolbox</h3>

<p>The easiest way to try out the project is to run the demo toolbox:</p>

<p><code>
python demo_toolbox.py
</code></p>

<p>This launches a graphical interface where you can:</p>

<ul>
<li>Record or load an utterance from a speaker to embed,</li>
<li>Load additional audio files to build a collection of speakers,</li>
<li>Synthesize arbitrary text using the voice of the selected speaker.</li>
</ul>

<p>If you have dataset files, you can pass their directory to the toolbox, e.g.:</p>

<p><code>
python demo_toolbox.py -d &lt;datasets_root&gt;
</code></p>

<h3>3. Training</h3>

<p>Each of the three components of the project (encoder, synthesizer, vocoder) can be trained separately. Refer to the training scripts in the corresponding modules of the repository:</p>

<ul>
<li><strong>Encoder</strong>: used to compute speaker embeddings from utterances.</li>
<li><strong>Synthesizer</strong>: trained with the Tacotron architecture to generate mel spectrograms from text.</li>
<li><strong>Vocoder</strong>: trained with WaveRNN to convert mel spectrograms to audio.</li>
</ul>

<p>Configuration for each component (audio parameters, training hyperparameters, etc.) is defined in the config files inside each module's directory.</p>

<h3>4. Inference</h3>

<p>The toolbox internally uses the pretrained models to perform the full pipeline: embedding extraction from a reference voice, text-to-spectrogram synthesis, and spectrogram-to-audio generation. Individual inference scripts are also available inside the <code>encoder</code>, <code>synthesizer</code> and <code>vocoder</code> modules for programmatic use.</p>
<h2>Contributing</h2>

<p>This project does not currently include specific contribution guidelines or a contributor code of conduct in the repository. If you would like to contribute, you can fork the repository, make your changes, and open a pull request describing the modifications you've made.</p>

<p>Note that this project builds upon the work of several other projects and is licensed under the MIT License (see the <a href="#license">License</a> section). Any contributions should respect the licensing terms of the original works.</p>
<h2>License</h2>

<p>This project is released under the <a href="https://github.com/CorentinJ/Real-Time-Voice-Cloning/blob/master/LICENSE.txt">MIT License</a>.</p>

<p>Original work Copyright (c) 2018 <a href="https://github.com/Rayhane-mamah">Rayhane Mama</a><br />
Original work Copyright (c) 2019 <a href="https://github.com/fatchord">fatchord</a><br />
Modified work Copyright (c) 2019 <a href="https://github.com/CorentinJ">Corentin Jemine</a><br />
Modified work Copyright (c) 2020 <a href="https://github.com/blue-fish">blue-fish</a></p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.</p>
