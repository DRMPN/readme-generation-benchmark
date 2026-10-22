# grok-1<h2>Description</h2>

<p><strong>Grok-1</strong> is a large language model trained from scratch by xAI with 314 billion parameters. This repository contains the open-weights release of Grok-1 together with the code needed to load the model and run inference with it. The model is implemented as a decoder-only, <strong>Mixture-of-Experts (MoE)</strong> transformer using the <strong>JAX/Flax</strong> framework.</p>

<p>The repository is organized into the following main components:</p>

<ul>
<li><p><code>modeling/</code> — The core implementation of the Grok-1 model architecture. It includes the expert routing logic (<code>router.py</code>), the Mixture-of-Experts layer (<code>moe_layer.py</code>), attention mechanisms (<code>attention.py</code>, <code>multihead_attention.py</code>), feed-forward blocks (<code>feedforward.py</code>), normalization layers (<code>norms.py</code>), quantization support (<code>quantization.py</code>), and the top-level model classes (<code>grok.py</code>, <code>language_model.py</code>) that assemble these pieces into the full Grok-1 model.</p></li>
<li><p><code>pipelines/</code> — Higher-level abstractions built on top of the model that make text generation convenient. This includes the generator (<code>generator.py</code>), the text generation pipeline (<code>text_generation_pipeline.py</code>), sampling strategies (<code>samplers.py</code>), and a model runner (<code>model_runner.py</code>) that orchestrates inference.</p></li>
<li><p><code>tensor/</code> — Low-level tensor utilities (partitioning, parallelism, shapes, and other operations) that the model implementation relies on.</p></li>
<li><p><code>run.py</code> — A runnable example script that loads the model and generates sample text. It demonstrates how to drive the model through the pipeline interfaces (e.g., using the JAX implementation via a <code>JaxHook</code>, or combining it with PyTorch components via a <code>PyTorchHook</code>).</p></li>
<li><p><code>util.py</code> — Helper utilities, including functions for downloading and un-partitioning the Grok-1 checkpoint.</p></li>
<li><p><code>scripts/download_checkpoint.sh</code> — A script for downloading the model weights.</p></li>
</ul>

<p>The weights and code in this repository are provided under the <a href="http://www.apache.org/licenses/LICENSE-2.0">Apache License 2.0</a>.</p>
<h2>Requirements</h2>

<p>Make sure you download the <code>INT8</code> checkpoint (see <code>Downloading the weights</code> below) and have <code>python3.9</code> or higher, as well as a machine with enough GPU RAM to run the 8-bit quantized checkpoint (about <strong>8x 40GiB</strong>).</p>

<p>We recommend installing the dependencies via pip:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>
<h2>Installation</h2>

<p>Download the weights and install dependencies:</p>

<p><code>shell
git clone https://github.com/xai-org/grok-1 &amp;&amp; cd grok-1
pip install -r requirements.txt
</code></p>
<h2>Usage</h2>

<h3>Setup</h3>

<p>Install the dependencies listed in <code>requirements.txt</code>:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>

<h3>Checkpoints</h3>

<p>The example expects the model weights and the SentencePiece tokenizer file (<code>tokenizer.model</code>) to be placed in the <code>checkpoints</code> directory (the default location used by the scripts). Make sure you have downloaded both into that directory before running the example.</p>

<h3>Running the example</h3>

<p>Run the example script with your input:</p>

<p><code>bash
python run.py --input "What is 2 + 2?"
</code></p>

<p><code>run.py</code> loads the model with JAX, shards it across the available devices, tokenizes the input, runs the model, and prints the generated output to the terminal.</p>

<blockquote>
  <p><strong>Note:</strong> Grok-1 is a very large model (~314 billion parameters), so running the full model requires a machine with a substantial amount of GPU memory (roughly 300+ GB, e.g., a node with 8 × A100 80 GB GPUs).</p>
</blockquote>

<h3>Where to look next</h3>

<p>The entry point for this example is <code>run.py</code>, which builds the model runner from the <code>runners/</code> package and relies on the model architecture defined in the <code>modeling/</code> package. Additional command-line options can be found in the argument-parsing code used by <code>run.py</code>.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>grok-1 is released under the <a href="http://www.apache.org/licenses/LICENSE-2.0">Apache License, Version 2.0</a>.</p>

<p>The full text of the license is included in the <code>LICENSE</code> file at the root of the repository. In summary, the license grants you the right to use, reproduce, and distribute the software and its modifications, subject to the terms and conditions set out in the license, including the disclaimer of warranty: the work is provided on an "AS IS" basis, without warranties or conditions of any kind (express or implied), and you are solely responsible for determining the appropriateness of using or redistributing the work.</p>
