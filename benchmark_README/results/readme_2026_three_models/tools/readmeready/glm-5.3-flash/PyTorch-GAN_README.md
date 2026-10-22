# PyTorch-GAN<h2>Description</h2>

<p>This repository contains PyTorch implementations of various Generative Adversarial Network (GAN) architectures, based on the <a href="https://github.com/eriklindernoren/PyTorch-GAN">PyTorch-GAN</a> collection by Erik Linder-Norén.</p>

<p>The project provides self-contained implementations of numerous GAN variants. Each implementation is a standalone script that can be trained from the command line, with hyperparameters configurable via command-line arguments, for example:</p>

<p><code>bash
python implementations/&lt;gan&gt;/&lt;gan&gt;.py \
    --n_epochs 200 \
    --batch_size 64 \
    --lr 0.0002
</code></p>

<p>Common configurable parameters across the implementations include:</p>

<ul>
<li><code>--n_epochs</code>: number of epochs of training</li>
<li><code>--batch_size</code>: size of the batches</li>
<li><code>--lr</code>: learning rate (e.g., Adam optimizer with beta parameters <code>--b1</code> and <code>--b2</code>)</li>
<li><code>--n_cpu</code>: number of CPU threads used during batch generation</li>
<li><code>--latent_dim</code>: dimensionality of the latent space</li>
<li><code>--img_size</code>: size of each image dimension</li>
<li><code>--channels</code>: number of image channels</li>
</ul>

<p>Some architectures expose additional, model-specific options, such as:</p>

<ul>
<li><code>--n_critic</code> and <code>--clip_value</code> (e.g., for Wasserstein GAN-style training, controlling discriminator steps per iteration and weight clipping)</li>
<li><code>--code_dim</code> and <code>--n_classes</code> (e.g., for models using latent codes and class conditioning)</li>
</ul>

<p>The implementations are intended to train on image datasets and produce generated samples, allowing researchers and developers to experiment with, benchmark, and extend different GAN models using PyTorch.</p>

<p>The project is released under the MIT License (Copyright (c) 2018 Erik Linder-Norén).</p>
<h2>Requirements</h2>

<p>To run the implementations in this repository you need:</p>

<ul>
<li><strong>Python 3</strong></li>
<li><a href="https://pytorch.org/"><strong>PyTorch</strong></a> (with torchvision)</li>
</ul>

<p>The training scripts also make use of common scientific/plotting Python libraries (e.g. NumPy and Matplotlib) for data loading and visualization. Install the required Python packages with:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>

<p>Then clone the repository and you are ready to run any of the GAN implementations, for example:</p>

<p><code>bash
git clone https://github.com/eriklindernoren/PyTorch-GAN
cd PyTorch-GAN/
</code></p>
<h2>Installation</h2>

<p>There is no dedicated installation script in this repository. To run the models, clone the repository and install the required dependencies (PyTorch, torchvision, etc.) in your own Python environment:</p>

<p><code>bash
git clone &lt;repository-url&gt;
cd PyTorch-GAN
pip install torch torchvision
</code></p>

<p>Then run any of the model scripts directly from their respective folders, e.g.:</p>

<p><code>bash
cd implementations/gan/
python gan.py
</code></p>
<h2>Usage</h2>

<p>Each GAN implementation is a standalone training script. To train a model, run its script from the command line and optionally override any of its command-line arguments, for example:</p>

<p><code>bash
python implementations/gan/gan.py \
    --n_epochs 200 \
    --batch_size 64 \
    --lr 0.0002 \
    --b1 0.5 \
    --b2 0.999 \
    --n_cpu 8 \
    --latent_dim 100 \
    --img_size 32 \
    --channels 1
</code></p>

<p>Common arguments shared by the implementations include:</p>

<ul>
<li><code>--n_epochs</code>: number of epochs of training</li>
<li><code>--batch_size</code>: size of the batches</li>
<li><code>--lr</code>: Adam learning rate</li>
<li><code>--b1</code>, <code>--b2</code>: Adam decay of first order momentum of gradient</li>
<li><code>--n_cpu</code>: number of CPU threads to use during batch generation</li>
<li><code>--latent_dim</code>: dimensionality of the latent space</li>
<li><code>--img_size</code>: size of each image dimension</li>
<li><code>--channels</code>: number of image channels</li>
</ul>

<p>Some implementations have additional model-specific arguments, for example:</p>

<ul>
<li><code>--n_classes</code>: number of classes for the dataset (e.g. for conditional/InfoGAN-style models)</li>
<li><code>--code_dim</code>: dimensionality of the latent code (InfoGAN)</li>
</ul>

<p>The training script will download the dataset it needs, train the model, and save sampled images during training so you can inspect the generated results.</p>
<h2>Contributing</h2>

<p>Contributions are welcome! If you would like to add an implementation of a new GAN variant, fix a bug, or improve the existing implementations, feel free to open an issue or submit a pull request to the <a href="https://github.com/eriklindernoren/PyTorch-GAN">PyTorch-GAN repository</a>.</p>

<p>This project is licensed under the MIT License, so any contributions will be covered by the same license.</p>
<h2>License</h2>

<p>This project is licensed under the MIT License.</p>

<p>```
MIT License</p>

<p>Copyright (c) 2018 Erik Linder-Norén</p>

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
SOFTWARE.
```</p>
