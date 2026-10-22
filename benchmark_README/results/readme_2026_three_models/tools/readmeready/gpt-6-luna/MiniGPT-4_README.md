# MiniGPT-4<h2>Description</h2>

<p>MiniGPT-4 is a vision-language project for interacting with images through natural-language prompts. The repository includes prompt templates for generating short image descriptions and dataset configuration for text-based instruction data, including <code>unnatural_instruction</code>.</p>
<h2>Requirements</h2>
<h2>Installation</h2>
<h2>Usage</h2>

<p>Configure the dataset paths before using the provided dataset configurations. Replace placeholder paths such as <code>/path/to/eval/annotation/path</code> and <code>/path/to/eval/image/path</code> with paths on your system.</p>

<p>The evaluation configuration lists <code>refcoco</code>, <code>refcocog</code>, <code>refcoco+</code>, <code>gqa</code>, <code>okvqa</code>, and <code>vizwiz</code>, each with annotation and image paths, a <code>max_new_tokens</code> value, and a <code>batch_size</code>. The <code>iconvqa</code> entry specifies an annotation path.</p>

<p>The <code>unnatural_instruction</code> dataset is configured as text data. Set its <code>ann_path</code> to the instruction JSON file you want to use.</p>
<h2>Contributing</h2>
<h2>License</h2>

<p>MiniGPT-4 is released under the BSD 3-Clause License. See the <code>LICENSE</code> file in the repository root for the full license text, or read the <a href="https://opensource.org/licenses/BSD-3-Clause">BSD 3-Clause License</a>.</p>
