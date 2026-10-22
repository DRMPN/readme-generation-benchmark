# MiniGPT-4<h2>Description</h2>

<p>MiniGPT-4 is an open-source project that aligns a frozen vision encoder with a frozen large language model (LLM) using a single projection layer, enabling advanced multimodal (vision-language) capabilities similar to those demonstrated by GPT-4.</p>

<p>The key idea behind MiniGPT-4 is that training the vision-language alignment on only a single projection layer keeps computational costs low while still producing high-quality results. The model is trained in two stages:</p>

<ol>
<li><strong>First stage:</strong> The model is trained on a large amount of image-text pairs using classic image captioning datasets, primarily to transfer visual knowledge to the language model.</li>
<li><strong>Second stage:</strong> A smaller, high-quality (but relatively small) curated dataset is used to teach the model to produce reliable and properly formatted outputs.</li>
</ol>

<p>After training, MiniGPT-4 exhibits a range of abilities similar to those observed in GPT-4, such as generating detailed image descriptions, explaining visual content, and answering questions about images.</p>

<p>The repository contains:
- Training and fine-tuning code for both stages
- Pretrained model checkpoints
- Inference/demo scripts for interacting with the model
- Dataset preparation utilities, including instructions to prepare various image captioning datasets (e.g., Conceptual Caption, SBU, LAION) and a curated mini dataset used in the second training stage</p>

<blockquote>
  <p><strong>Note:</strong> This repository is built on top of the <a href="https://github.com/salesforce/LAVIS">LAVIS</a> library from Salesforce, and parts of the codebase are licensed under BSD-3-Clause (see the <code>LICENSE</code> file).</p>
</blockquote>
<h2>Requirements</h2>
<h2>Installation</h2>

<ol>
<li>Clone the repository and set up the Python environment:</li>
</ol>

<p><code>bash
git clone https://github.com/.../MiniGPT-4.git
cd MiniGPT-4
conda env create -f environment.yml
conda activate minigpt4
</code></p>

<ol start="2">
<li>Install additional required packages:</li>
</ol>

<p><code>bash
pip install -r requirements.txt
</code></p>

<ol start="3">
<li><p>Prepare the pretrained model checkpoints (e.g., the pretrained MiniGPT-4 checkpoint and the underlying Vicuna LLM weights) and place them in the appropriate directory as described in the model configuration files.</p></li>
<li><p>Prepare the datasets (e.g., CC_SBU and LAION image datasets) and update the dataset storage paths in the dataset configuration files (e.g., <code>cc_sbu.yaml</code> and <code>laion.yaml</code>) to point to your local webdataset shards, for example:</p></li>
</ol>

<p><code>yaml
datasets:
  cc_sbu:
    data_type: images
    build_info:
      storage: /path/to/cc_sbu_dataset/{00000..01255}.tar
</code></p>
<h2>Usage</h2>

<h3>Prerequisites</h3>

<ul>
<li>Python 3.10</li>
<li>CUDA 11.0+</li>
</ul>

<p>Install the required dependencies:</p>

<p><code>shell
conda env create -f environment.yml
conda activate minigpt4
</code></p>

<h3>Preparing the Vicuna weights</h3>

<p>MiniGPT-4 is built on top of Vicuna. Please first download the Vicuna-13B (or Vicuna-7B) weights from the original Vicuna release, then convert the weights using the provided conversion script:</p>

<p><code>shell
python -m llama.convert_weights --model-path /path/to/vicuna/weights --output-dir /path/to/converted/weights
</code></p>

<h3>Preparing the pretrained MiniGPT-4 checkpoint</h3>

<p>Download the pretrained MiniGPT-4 checkpoint (aligned with the Vicuna weights you prepared) and place it in the <code>pretrained_minigpt4.pth</code> location expected by the demo scripts.</p>

<h3>Try the demo</h3>

<p>Run the demo with a GPU that has at least 16GB of memory (13B model):</p>

<p><code>shell
python demo.py --cfg-path eval_configs/demo.yaml --gpu-id 0
</code></p>

<p>For low GPU memory (about 12GB), use the low-resource version with 8-bit Vicuna weights:</p>

<p><code>shell
python demo.py --cfg-path eval_configs/demo.yaml --gpu-id 0 --low-resource
</code></p>

<p>In the demo you can upload an image and interact with the model in the chat interface.</p>

<h3>Training</h3>

<p>Training MiniGPT-4 happens in two stages:</p>

<ol>
<li><strong>First stage (pretraining):</strong> train the projection layer using image-text pairs. Run:</li>
</ol>

<p><code>shell
torchrun --nproc_per_node=1 train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
</code></p>

<ol start="2">
<li><strong>Second stage (fine-tuning):</strong> fine-tune on high-quality instruction-following data:</li>
</ol>

<p><code>shell
torchrun --nproc_per_node=1 train.py --cfg-path train_configs/minigpt4_stage2_finetune.yaml
</code></p>

<p>Training configuration files (e.g. <code>train_configs/minigpt4_stage1_pretrain.yaml</code> and <code>train_configs/minigpt4_stage2_finetune.yaml</code>) specify dataset paths, model paths, and hyperparameters; adjust the paths and settings according to your environment before launching.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the BSD 3-Clause License.</p>

<p>Copyright (c) 2014, Aishwarya Agrawal. All rights reserved.</p>

<p>Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:</p>

<ol>
<li>Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.</li>
<li>Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.</li>
</ol>

<p>THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.</p>

<p>For the full license text, see the LICENSE file in the repository root.</p>
