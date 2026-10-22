# PyTorch-GAN<h2>Description</h2>

<p>PyTorch-GAN is a collection of PyTorch implementations of generative adversarial network (GAN) models. The training scripts expose configuration options such as the number of epochs, batch size, learning rate, and latent-space dimensions. Some implementations also include model-specific settings, such as the critic update count and weight clipping for WGAN, or class and latent-code dimensions for InfoGAN.</p>
<p>I’ll check the repository’s dependency files and existing setup instructions to identify the project’s stated requirements.</p>

<h2>Requirements</h2>

<ul>
<li>Python 3</li>
<li>PyTorch</li>
<li>torchvision</li>
<li>NumPy</li>
<li>SciPy</li>
<li>Matplotlib</li>
<li>Pillow</li>
</ul>
<h2>Installation</h2>

<p>From the repository root, install the project dependencies with:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>
<h2>Usage</h2>

<p>Run the training script for the implementation you want to use. The scripts accept command-line options; the defaults shown in the available parsers are:</p>

<p>| Option | Default | Description |
|---|---:|---|
| <code>--n_epochs</code> | <code>200</code> | Number of training epochs |
| <code>--batch_size</code> | <code>64</code> | Batch size |
| <code>--lr</code> | <code>0.0002</code> | Adam learning rate |
| <code>--b1</code> | <code>0.5</code> | Adam first-moment decay |
| <code>--b2</code> | <code>0.999</code> | Adam second-moment decay |
| <code>--n_cpu</code> | <code>8</code> | CPU threads for batch generation |
| <code>--img_size</code> | <code>32</code> | Image dimension |</p>

<p>The latent and image options vary between scripts:</p>

<ul>
<li>One parser defaults to <code>--latent_dim 10</code> and <code>--channels 1</code>.</li>
<li>Another defaults to <code>--latent_dim 62</code>, <code>--code_dim 2</code>, and <code>--n_classes 10</code>.</li>
<li>A third defaults to <code>--latent_dim 62</code> and <code>--channels 1</code>.</li>
</ul>

<p>Pass options to the selected script to override its defaults.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>MIT License</p>

<p>Copyright (c) 2018 Erik Linder-Norén</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.</p>
