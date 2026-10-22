# Real-Time-Voice-Cloning<h2>Description</h2>

<p>This part of the project covers training the vocoder, the component that turns mel spectrograms into audio. The training script uses the following command-line options:</p>

<ul>
<li><strong><code>-m, --models_dir</code></strong>: Directory where model weights are saved, along with backups of those weights and WAV files generated during training. Default: <code>saved_models</code>.</li>
<li><strong><code>-g, --ground_truth</code></strong>: When passed, the model trains on ground truth spectrograms from <code>&lt;datasets_root&gt;/SV2TTS/synthesizer/mels</code>.</li>
<li><strong><code>-s, --save_every</code></strong>: Number of steps between saving the model to disk. Default: <code>1000</code>. Set to <code>0</code> to never save.</li>
<li><strong><code>-b, --backup_every</code></strong>: Number of steps between model backups. Default: <code>25000</code>. Set to <code>0</code> to never make backups.</li>
<li><strong>Vocoder data directory</strong> (the option whose help text appears in the snippet): Path to the directory containing the GTA (ground-truth-aligned) synthesized mel spectrograms. Default: <code>&lt;datasets_root&gt;/SV2TTS/vocoder/</code>. This option is ignored when <code>--ground_truth</code> is passed.</li>
</ul>

<h3>License</h3>

<p>The project is released under the MIT License. It combines work from several authors: original work by Rayhane Mama and fatchord, with modifications by Corentin Jemine and blue-fish. The license text is included in the repository.</p>
<h2>Requirements</h2>
<h2>Installation</h2>
<h2>Usage</h2>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the MIT License. The original work and later modifications are copyrighted by the following authors:</p>

<ul>
<li>Original work Copyright (c) 2018 <a href="https://github.com/Rayhane-mamah">Rayhane Mama</a></li>
<li>Original work Copyright (c) 2019 <a href="https://github.com/fatchord">fatchord</a></li>
<li>Modified work Copyright (c) 2019 <a href="https://github.com/CorentinJ">Corentin Jemine</a></li>
<li>Modified work Copyright (c) 2020 <a href="https://github.com/blue-fish">blue-fish</a></li>
</ul>

<p>The software is provided "as is", without warranty of any kind. Permission is granted, free of charge, to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, provided that the copyright notice and permission notice are included in all copies or substantial portions of the software.</p>
