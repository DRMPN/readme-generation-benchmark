# ChatGLM-6B<h2>Description</h2>

<p>ChatGLM-6B is an open-source bilingual (Chinese-English) conversational language model built on the GLM (General Language Model) architecture. It is optimized for Chinese question answering and dialogue, and has also been aligned for human-instruction following through supervised fine-tuning, as well as Reinforcement Learning from Human Feedback (RLHF).</p>

<p>The model is designed to run efficiently on consumer-grade hardware. It contains approximately 6.2 billion parameters, and the repository provides quantization support (INT4/INT8), which allows the model to be deployed on GPUs with limited memory.</p>

<p>The repository includes:</p>

<ul>
<li><strong>Model code</strong> implementing the ChatGLM architecture, including custom attention, rotary position embeddings (RoPE), and GLU-based feed-forward layers.</li>
<li><strong>Inference and deployment tools</strong> such as a command-line interface (<code>cli_demo.py</code>) and a web demo (<code>web_demo.py</code> / <code>web_demo2.py</code>) built with Gradio for interacting with the trained model.</li>
<li><strong>Fine-tuning scripts</strong> (<code>finetune.py</code>, <code>ptuning/main.py</code>) that support parameter-efficient tuning methods such as P-Tuning v2, along with utilities for loading and preprocessing training data in jsonlines or csv format.</li>
<li><strong>Training data preprocessing</strong> with configurable options such as <code>max_source_length</code>, <code>max_target_length</code>, prompt/response/history column names, and support for evaluating with ROUGE metrics on validation and test files.</li>
</ul>

<p>The project is released for research purposes, and users should be aware of the model's potential limitations before deploying it in production environments.</p>
<h2>Requirements</h2>

<p>To run the code in this repository, you need to set up a Python environment with the required dependencies.</p>

<h3>Install dependencies</h3>

<p>Use <code>pip</code> to install the required packages from the <code>requirements.txt</code> file located in the repository root:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>

<p>The key dependencies include:</p>

<ul>
<li><strong>transformers</strong> — recommended version is <code>4.26.1</code> (the Hugging Face transformers library used for loading and running the GLM-based model)</li>
<li><strong>torch</strong> — PyTorch is required for model inference and training (CPU or CUDA-enabled builds)</li>
<li>Other supporting libraries such as <code>cpm_kernels</code> (used for INT4/INT8 quantized inference), <code>sentencepiece</code>, <code>gradio</code>, <code>datasets</code>, and <code>rouge_chinese</code> (used by the fine-tuning scripts)</li>
</ul>

<h3>Hardware requirements</h3>

<ul>
<li><p><strong>Inference:</strong> ChatGLM-6B can run on consumer-grade GPUs depending on the quantization level:</p>

<ul>
<li><strong>FP16:</strong> approximately 13–14 GB of GPU memory</li>
<li><strong>INT8</strong> (<code>quantization_bit=8</code>): approximately 9–10 GB of GPU memory</li>
<li><strong>INT4</strong> (<code>quantization_bit=4</code>): approximately 6–7 GB of GPU memory</li>
</ul></li>
<li><p><strong>Fine-tuning:</strong> The parameter-efficient fine-tuning approach (P-Tuning V2, via the <code>ptuning/</code> directory with <code>pre_seq_len</code> and optionally <code>prefix_projection</code>) significantly reduces the memory footprint compared to full fine-tuning, and can be combined with <code>quantization_bit=4</code> together with gradient checkpointing to fine-tune on GPUs with as little as ~6–7 GB of memory.</p></li>
</ul>
<h2>Installation</h2>

<p>Requires Python 3.6 or higher. First, clone the repository to your local machine:</p>

<p><code>bash
git clone https://github.com/THUDM/ChatGLM-6B
cd ChatGLM-6B
</code></p>

<p>Then install the required dependencies:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>

<p>The following packages are required:</p>

<ul>
<li><code>torch</code></li>
<li><code>transformers&gt;=4.26.1</code></li>
<li><code>sentencepiece</code></li>
<li><code>tqdm</code></li>
<li><code>datasets</code></li>
<li><code>accelerate</code></li>
<li><code>tensorboard</code></li>
<li><code>protobuf</code></li>
<li><code>gradio</code></li>
<li><code>mdtex2html</code></li>
</ul>

<p>For inference, <code>transformers&gt;=4.26.1</code> is required. By default, the model is loaded to GPU; this requires NVIDIA GPU memory of around 13 GB (for FP16 precision). If you want to run the model on GPUs with less memory, you can use quantization options (e.g. <code>INT4</code> requires about 6 GB of memory).</p>
<h2>Usage</h2>

<h3>Environment Setup</h3>

<p>First, install the required dependencies:</p>

<p><code>bash
pip install -r requirements.txt
</code></p>

<h3>Quick Start (Code)</h3>

<p>ChatGLM-6B is available via Hugging Face Transformers (version 4.27.1 or higher is recommended). To load and chat with the model in Python:</p>

<p>```python
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from<em>pretrained("THUDM/chatglm-6b", trust</em>remote<em>code=True)
model = AutoModel.from</em>pretrained("THUDM/chatglm-6b", trust<em>remote</em>code=True).half().cuda()
model = model.eval()</p>

<p>history = []
response, history = model.chat(tokenizer, "你好", history=history)
print(response)</p>

<p>response, history = model.chat(tokenizer, "晚上睡不着应该怎么办", history=history)
print(response)
```</p>

<p>The model supports multi-turn dialogue — pass the <code>history</code> returned from previous calls into subsequent <code>model.chat()</code> invocations.</p>

<h3>Command Line Demo</h3>

<p>Run an interactive command-line chat session:</p>

<p><code>bash
python cli_demo.py
</code></p>

<p>This provides a REPL-style interface where you can type messages, see the model's replies, and maintain conversation history across turns.</p>

<h3>Web Demo</h3>

<p>Run a Gradio-based web interface:</p>

<p><code>bash
python web_demo.py
</code></p>

<p>Then open the printed URL in your browser to chat with the model through a graphical interface.</p>

<h3>API Deployment</h3>

<p>Expose the model as an HTTP service for other applications to consume:</p>

<p><code>bash
python api.py
</code></p>

<p>The API server listens on port 8000 by default. You can call it with a POST request to <code>http://127.0.0.1:8000</code> containing the prompt and conversation history, and it returns the generated response and updated history.</p>

<h3>Low-Resource Deployment (Quantization)</h3>

<p>If GPU memory is limited, load the model with quantization. Supported values are 4-bit (approximately 6 GB of GPU memory) and 8-bit (approximately 10–11 GB):</p>

<p>```python</p>

<h1>4-bit quantization</h1>

<p>model = AutoModel.from<em>pretrained("THUDM/chatglm-6b", trust</em>remote_code=True).quantize(4).half().cuda()
```</p>

<p>```python</p>

<h1>8-bit quantization</h1>

<p>model = AutoModel.from<em>pretrained("THUDM/chatglm-6b", trust</em>remote_code=True).quantize(8).half().cuda()
```</p>

<p>Note that after quantization, the second <code>model.chat()</code> call may be slower due to the quantization kernel overhead, but the effect on dialogue quality is minimal.</p>

<h3>CPU Deployment</h3>

<p>If no GPU is available, you can run the model on CPU:</p>

<p><code>python
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).float()
</code></p>

<p>Inference speed on CPU will be noticeably slower than on GPU.</p>

<h3>Model Fine-tuning</h3>

<p>The repository includes a fine-tuning pipeline based on <a href="https://github.com/THUDM/P-tuning-v2">P-Tuning v2</a>. Training data should be a JSON or JSONL file containing a <code>prompt_column</code> (the input text) and a <code>response_column</code> (the target response).</p>

<p>Run fine-tuning with:</p>

<p><code>bash
bash train.sh
</code></p>

<p>Key training arguments (defined in <code>ptuning/arguments.py</code>) include:</p>

<ul>
<li><code>train_file</code> / <code>validation_file</code> / <code>test_file</code>: paths to the training/evaluation/test data files (jsonlines or csv).</li>
<li><code>prompt_column</code>: the dataset column containing the input texts.</li>
<li><code>response_column</code>: the dataset column containing the target responses.</li>
<li><code>history_column</code>: the dataset column containing conversation history (if any).</li>
<li><code>max_source_length</code>: maximum length of the input sequences (default 1024).</li>
<li><code>quantization_bit</code>: train with the base model quantized to save memory.</li>
<li><code>pre_seq_len</code>: number of prefix tokens used by the P-Tuning v2 prefix encoder.</li>
<li><code>prefix_projection</code>: whether to use an MLP reparameterization for the prefix embeddings.</li>
</ul>

<p>After training completes, run <code>bash evaluate.sh</code> to evaluate the fine-tuned model on the test set using ROUGE metrics, and merge the trained prefix checkpoints back into the base model for deployment.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>This project is licensed under the <strong>Apache License 2.0</strong>.</p>

<p>Copyright © Zhengxiao Du</p>

<p>You may use, reproduce, and distribute this software in accordance with the terms and conditions of the Apache License, Version 2.0. A copy of the license is included in the repository, and the full text can also be found at <a href="http://www.apache.org/licenses/LICENSE-2.0">http://www.apache.org/licenses/LICENSE-2.0</a>.</p>

<p>Under this license, the software is provided on an "AS IS" basis, without warranties or conditions of any kind, either express or implied. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with your exercise of permissions under this License.</p>
