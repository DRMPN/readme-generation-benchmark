# Real-Time-Voice-Cloning<h2>Description</h2>

<p>Real-Time-Voice-Cloning is a voice-cloning and speech-synthesis project. It uses a reference audio clip to create a speaker representation, generates a mel spectrogram conditioned on that representation and input text, then converts the spectrogram into audio with a vocoder. The repository includes separate encoder, synthesizer, and vocoder components, along with scripts for training and using them.</p>
<h2>Requirements</h2>

<ul>
<li>Audio is processed at a sampling rate of <strong>16 kHz</strong>.</li>
<li>The voice activity detector uses <strong>30 ms</strong> windows by default; its window length must be <strong>10, 20, or 30 ms</strong>.</li>
<li>The mel filterbank is configured with a <strong>25 ms</strong> window, a <strong>10 ms</strong> step, and <strong>40 channels</strong>.</li>
</ul>
<h2>Installation</h2>

<p>From the repository root, install the project’s Python dependencies:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>
<h2>Usage</h2>

<p>Start the graphical toolbox:</p>

<p><code>bash
python demo_toolbox.py
</code></p>

<p>In the toolbox, provide a voice sample, enter text, and generate speech in that voice.</p>

<p>For a command-line workflow, run:</p>

<p><code>bash
python demo_cli.py
</code></p>

<p>Follow the prompts to provide the voice sample and text.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project includes work distributed under the MIT License. The supplied license notices list these attributions:</p>

<ul>
<li>Original work Copyright (c) 2018 Rayhane Mama</li>
<li>Original work Copyright (c) 2019 fatchord</li>
<li>Modified work Copyright (c) 2019 Corentin Jemine</li>
<li>Modified work Copyright (c) 2020 blue-fish</li>
<li>Copyright (c) 2015 braindead</li>
</ul>

<p>Permission is granted, free of charge, to anyone obtaining a copy of the software and associated documentation to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies, and to permit others to do the same, subject to including the applicable copyright and permission notices in copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR ITS USE.</p>
