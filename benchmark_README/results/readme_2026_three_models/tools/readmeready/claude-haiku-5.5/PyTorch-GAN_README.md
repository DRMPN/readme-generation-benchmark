# PyTorch-GAN<h2>Description</h2>

<p>PyTorch-GAN is a collection of PyTorch implementations of Generative Adversarial Networks (GANs). Each model is a standalone training script that defines a generator and a discriminator, trains them against each other, and exposes its settings as command-line arguments.</p>

<p>The scripts share a common pattern. Each one uses <code>argparse</code> to define hyperparameters such as the number of epochs, batch size, learning rate, latent dimension, image size, and number of image channels. Users can override these defaults when they run a script from the command line.</p>

<p>The included argument definitions show the kinds of variation across the models:</p>

<ul>
<li><strong>Adam-based training:</strong> Some scripts use Adam optimizer settings (<code>--lr</code>, <code>--b1</code>, <code>--b2</code>) with a learning rate of 0.0002.</li>
<li><strong>Weight clipping:</strong> One script adds <code>--n_critic</code> (discriminator training steps per iteration) and <code>--clip_value</code> (bounds for discriminator weights), which are parameters associated with Wasserstein-style GAN training.</li>
<li><strong>Latent codes and classes:</strong> One script adds <code>--code_dim</code> and <code>--n_classes</code> alongside a larger latent space (<code>--latent_dim</code> of 62), which suggests it learns structured latent codes in addition to noise input.</li>
</ul>

<p>The project is released under the MIT License, Copyright (c) 2018 Erik Linder-Norén.</p>
<p>I couldn't find enough information in the provided context to write a Requirements section, so I've left it blank:</p>

<h2>Requirements</h2>
<h2>Installation</h2>
<h2>Usage</h2>

<p>Each model's training script is run from the command line and accepts the options below. Every option is optional and falls back to its default if you don't pass it.</p>

<p>Common options (defaults shown):</p>

<p>| Option | Type | Default | Description |
|---|---|---|---|
| <code>--n_epochs</code> | int | 200 | Number of epochs of training |
| <code>--batch_size</code> | int | 64 | Size of the batches |
| <code>--lr</code> | float | 0.0002 | Adam: learning rate |
| <code>--b1</code> | float | 0.5 | Adam: decay of first order momentum of gradient |
| <code>--b2</code> | float | 0.999 | Adam: decay of first order momentum of gradient |
| <code>--n_cpu</code> | int | 8 | Number of CPU threads to use during batch generation |
| <code>--latent_dim</code> | int | 10 or 62 | Dimensionality of the latent code/space (depends on the script) |
| <code>--img_size</code> | int | 32 | Size of each image dimension |
| <code>--channels</code> | int | 1 | Number of image channels (in scripts that define it) |</p>

<p>Some scripts also define these options:</p>

<p>| Option | Type | Default | Description |
|---|---|---|---|
| <code>--code_dim</code> | int | 2 | Latent code dimensionality |
| <code>--n_classes</code> | int | 10 | Number of classes for the dataset |</p>

<p>For example, to train for 50 epochs with a batch size of 32:</p>

<p><code>bash
python &lt;script_name&gt;.py --n_epochs 50 --batch_size 32
</code></p>

<p>Replace <code>&lt;script_name&gt;.py</code> with the training script for the model you want to run.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the MIT License. Copyright (c) 2018 Erik Linder-Norén.</p>

<p>The software is provided "as is", without warranty of any kind. See the LICENSE file in the repository for the full license text.</p>
