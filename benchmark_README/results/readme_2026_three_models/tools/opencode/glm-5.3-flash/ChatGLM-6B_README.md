# ChatGLM-6B

*ChatGLM-6B: An Open Bilingual Dialogue Language Model | 开源双语对话语言模型*

* 🤗 Model checkpoints: [THUDM/chatglm-6b](https://huggingface.co/THUDM/chatglm-6b), [THUDM/chatglm-6b-int4](https://huggingface.co/THUDM/chatglm-6b-int4), [THUDM/chatglm-6b-int8](https://huggingface.co/THUDM/chatglm-6b-int8)
* 🏠 Official repository: [github.com/THUDM/ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)

## Introduction

ChatGLM-6B is an open bilingual (Chinese–English) conversational language model based on the [General Language Model (GLM)](https://github.com/THUDM/GLM) architecture, with 6.2 billion parameters. Combined with model quantization, it can be deployed locally on consumer-grade GPUs — only about 6 GB of GPU memory is required at the INT4 quantization level.

ChatGLM-6B uses technology similar to ChatGPT, optimized for Chinese question answering and dialogue. It was trained on about 1T tokens of Chinese and English corpora, supplemented with supervised fine-tuning, feedback bootstrap, and reinforcement learning from human feedback (RLHF).

To make it easy to adapt the model to downstream scenarios, this repository also implements a parameter-efficient tuning method based on [P-Tuning v2](https://github.com/THUDM/P-tuning-v2) — see [ptuning/README.md](ptuning/README.md) (Chinese) and [ptuning/README_en.md](ptuning/README_en.md) (English). Fine-tuning requires as little as 7 GB of GPU memory at the INT4 quantization level.

ChatGLM-6B model weights are **fully open** for academic research; **free commercial use** is also allowed after registering via this [questionnaire](https://open.bigmodel.cn/mla/form).

## News

See [UPDATE.md](UPDATE.md) for the full changelog. Recent highlights:

* **[2023/05/17]** Release of [VisualGLM-6B](https://github.com/THUDM/VisualGLM-6B), a multimodal dialogue model with image understanding. It can be run from [cli_demo_vision.py](cli_demo_vision.py) and [web_demo_vision.py](web_demo_vision.py) in this repository.
* **[2023/05/15]** Updated v1.1 checkpoint: English instruction data was added to balance the Chinese/English data ratio, fixing Chinese words mixed into English answers.
* **[2023/04/16]** Added the INT8-quantized model [ChatGLM-6B-INT8](https://huggingface.co/THUDM/chatglm-6b-int8) and multi-GPU deployment.
* **[2023/03/31]** Added parameter-efficient tuning based on P-Tuning v2 (as little as 7 GB GPU memory at INT4). See [ptuning/README.md](ptuning/README.md).
* **[2023/03/23]** Added API deployment and GPU inference on Macs with Apple Silicon.
* **[2023/03/19]** Added the streaming output interface `stream_chat` and the INT4-quantized model [ChatGLM-6B-INT4](https://huggingface.co/THUDM/chatglm-6b-int4).

## Hardware Requirements

| **Quantization level** | **Minimum GPU memory (inference)** | **Minimum GPU memory (parameter-efficient tuning)** |
| ---------------------- | ---------------------------------- | --------------------------------------------------- |
| FP16 (no quantization) | 13 GB                              | 14 GB                                               |
| INT8                   | 8 GB                               | 9 GB                                                |
| INT4                   | 6 GB                               | 7 GB                                                |

## Getting Started

### Environment installation

Install the dependencies with pip:

```shell
pip install -r requirements.txt
```

where the `transformers` library version 4.27.1 is recommended (`requirements.txt` pins it), and in theory any version not lower than 4.23.1 works.

To run the quantized model on CPU, `gcc` and `openmp` are also required. Most Linux distributions ship with them. On Windows, select `openmp` when installing [TDM-GCC](https://jmeubank.github.io/tdm-gcc/). On macOS, see [FAQ.md](FAQ.md#q1).

### Model checkpoints

The complete model implementation and parameters are downloaded automatically by `transformers` from the Hugging Face Hub when you load the model with `trust_remote_code=True`. Available checkpoints:

* [THUDM/chatglm-6b](https://huggingface.co/THUDM/chatglm-6b) — FP16 base model
* [THUDM/chatglm-6b-int4](https://huggingface.co/THUDM/chatglm-6b-int4) — INT4 quantized
* [THUDM/chatglm-6b-int8](https://huggingface.co/THUDM/chatglm-6b-int8) — INT8 quantized

### Code calling

You can call ChatGLM-6B to generate a dialogue with the following code:

```python
>>> from transformers import AutoTokenizer, AutoModel
>>> tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
>>> model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
>>> model = model.eval()
>>> response, history = model.chat(tokenizer, "你好", history=[])
>>> print(response)
你好👋!我是人工智能助手 ChatGLM-6B,很高兴见到你,欢迎问我任何问题。
```

Use `model.stream_chat(tokenizer, query, history=...)` for streaming output, as done in the demos below.

### Load the model locally

Downloading model parameters from the Hugging Face Hub can be slow or fail on poor network connections. In that case, download the model to a local directory first and load it from there.

Install [Git LFS](https://docs.github.com/zh/repositories/working-with-files/managing-large-files/installing-git-large-file-storage), then run:

```shell
git clone https://huggingface.co/THUDM/chatglm-6b
```

If the checkpoint download is slow, you can clone only the model implementation:

```shell
GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/THUDM/chatglm-6b
```

and then manually download the model parameter files and place them into the local `chatglm-6b` directory. Afterwards, replace `THUDM/chatglm-6b` in the code above with the path to your local `chatglm-6b` folder.

## Demos and API

Clone this repository first:

```shell
git clone https://github.com/THUDM/ChatGLM-6B
cd ChatGLM-6B
```

### Web demo

![web-demo](resources/web-demo.gif)

Install Gradio (`pip install gradio`) and run [web_demo.py](web_demo.py):

```shell
python web_demo.py
```

The program runs a web server and prints an address; open it in your browser to chat. The demo streams output token by token (typewriter effect). It defaults to `demo.queue().launch(share=False, inbrowser=True)`; set `share=True` if you need public access. Sliders let you adjust `max_length`, `top_p`, and `temperature`.

A Streamlit-based web demo is also provided in [web_demo2.py](web_demo2.py). It requires additional dependencies that are not in `requirements.txt`:

```shell
pip install streamlit streamlit-chat
streamlit run web_demo2.py
```

[web_demo_old.py](web_demo_old.py) is an older version of the Gradio demo that renders the conversation as plain text boxes instead of a chat interface.

### Command-line demo

![cli-demo](resources/cli-demo.png)

Run [cli_demo.py](cli_demo.py):

```shell
python cli_demo.py
```

The program runs an interactive dialogue in the command line: type an instruction and press Enter to get a reply. Input `clear` to clear the conversation history, and `stop` to terminate the program.

### API deployment

Install the extra dependencies (`pip install fastapi uvicorn`) and run [api.py](api.py):

```shell
python api.py
```

By default, the API is deployed on local port `8000` and called via POST:

```shell
curl -X POST "http://127.0.0.1:8000" \
     -H 'Content-Type: application/json' \
     -d '{"prompt": "你好", "history": []}'
```

The response contains the generated text, the updated history, a status code, and a timestamp:

```json
{
  "response": "你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。",
  "history": [["你好", "你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。"]],
  "status": 200,
  "time": "2023-03-23 21:38:40"
}
```

The request body may also include `max_length` (default 2048), `top_p` (default 0.7), and `temperature` (default 0.95).

## Low-cost deployment

### Model quantization

By default, the model is loaded in FP16 precision, which requires about 13 GB of GPU memory. If your GPU memory is limited, load the model with quantization:

```python
# Modify as needed; currently only 4/8-bit quantization is supported
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).quantize(8).half().cuda()
```

After 2–3 dialogue rounds, GPU memory usage is about 10 GB with 8-bit quantization and only about 6 GB with 4-bit quantization. As the number of dialogue rounds grows, memory usage grows accordingly. Since ChatGLM-6B uses relative position encoding, it theoretically supports an unlimited context length, but performance gradually degrades when the total length exceeds the 2048 training length.

Quantization introduces some performance loss; testing shows that ChatGLM-6B still generates natural and fluent text at 4-bit quantization.

The quantization process first loads the FP16 model into RAM (about 13 GB). If your memory is insufficient, load the pre-quantized model directly (the INT4 checkpoint needs only about 5.2 GB of memory):

```python
# For INT8, replace "THUDM/chatglm-6b-int4" with "THUDM/chatglm-6b-int8"
model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True).half().cuda()
```

### CPU deployment

If you have no GPU, inference can run on CPU, but more slowly (about 32 GB of memory required):

```python
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).float()
```

If memory is insufficient, load the quantized model instead:

```python
# For INT8, replace "THUDM/chatglm-6b-int4" with "THUDM/chatglm-6b-int8"
model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True).float()
```

If you get errors such as `Could not find module 'nvcuda.dll'` or `RuntimeError: Unknown platform: darwin` (macOS), load the model locally instead.

### Mac deployment

On Macs with Apple Silicon or an AMD GPU, the MPS backend can be used to run ChatGLM-6B on the GPU. Install PyTorch-Nightly following Apple's [official instructions](https://developer.apple.com/metal/pytorch) (the correct version is 2.1.0.dev2023xxxx, not 2.0.0).

Currently, only local model loading is supported on macOS. Change the loading code to use a local path and the `mps` backend:

```python
model = AutoModel.from_pretrained("your local path", trust_remote_code=True).half().to('mps')
```

Loading the FP16 model requires about 13 GB of memory. On machines with less free memory (e.g., a 16 GB MacBook Pro), the system may swap to disk and inference becomes very slow. In that case, use a quantized model such as `chatglm-6b-int4`; since the quantization kernels on GPU are written with CUDA, they cannot be used on macOS, so inference falls back to CPU:

```python
# For INT8, replace "THUDM/chatglm-6b-int4" with "THUDM/chatglm-6b-int8"
model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True).float()
```

If you see `clang: error: unsupported option '-fopenmp'` when loading the quantized model on a Mac, see [FAQ.md](FAQ.md#q1).

### Multi-GPU deployment

If you have multiple GPUs and none of them alone can hold the full model, the model can be split across GPUs. Install `accelerate` (`pip install accelerate`, included in `requirements.txt`) and load the model as follows:

```python
from utils import load_model_on_gpus
model = load_model_on_gpus("THUDM/chatglm-6b", num_gpus=2)
```

This deploys the model on two GPUs. `num_gpus` can be set to the number of GPUs you want to use. Splitting is even by default; you can also pass a custom `device_map`.

## Parameter-efficient fine-tuning

This repository implements fine-tuning of ChatGLM-6B based on [P-Tuning v2](https://github.com/THUDM/P-tuning-v2), which reduces the trainable parameters to 0.1% of full fine-tuning. With model quantization, gradient checkpointing, and similar techniques, at least 7 GB of GPU memory (6.7 GB in the default INT4 configuration) is enough to run it. The code lives in [ptuning/](ptuning/) and is documented in [ptuning/README.md](ptuning/README.md) (Chinese) and [ptuning/README_en.md](ptuning/README_en.md) (English). In addition to the dependencies of ChatGLM-6B, fine-tuning requires:

```shell
pip install rouge_chinese nltk jieba datasets
```

Summary of the workflow (using the [ADGEN](https://aclanthology.org/D19-1321.pdf) advertising-generation dataset as the example):

* **P-Tuning v2 training**: run `bash train.sh`. `PRE_SEQ_LEN` (soft prompt length) and `LR` (learning rate) can be adjusted; all model parameters are frozen, and `quantization_bit` controls the quantization level of the base model (FP16 if unset).
* **Full-parameter fine-tuning**: install [DeepSpeed](https://github.com/microsoft/DeepSpeed) and run `bash ds_train_finetune.sh`.
* **Evaluation**: run `bash evaluate.sh`; metrics are Chinese Rouge score and BLEU-4. For P-Tuning v2 checkpoints (which only contain PrefixEncoder weights), specify both `--model_name_or_path THUDM/chatglm-6b` and `--ptuning_checkpoint $CHECKPOINT_PATH`; full checkpoints can be loaded via `model_name_or_path` alone.
* **Multi-turn dialogue data**: provide a `history` column and set `--history_column` accordingly, then run `bash train_chat.sh`. Content exceeding `max_source_length` is truncated.
* **Demo deployment**: a web demo that supports loading P-Tuning v2 checkpoints is available via `bash web_demo.sh` (edit [ptuning/web_demo.sh](ptuning/web_demo.sh) to match your checkpoint).

Evaluation results on ADGEN under the documented experiment settings:

|               | Finetune | P-tuning v2 | LoRA  |
| ------------- | -------- | ----------- | ----- |
| BLEU-4        | 8.01     | 8.10        | 7.62  |
| Rouge-1       | 31.23    | 31.12       | 30.60 |
| Rouge-2       | 7.36     | 7.11        | 6.96  |
| Rouge-l       | 25.08    | 24.97       | 24.80 |
| Training Loss | 3.00     | 3.74        | 3.32  |

## Image conversations with VisualGLM-6B

[VisualGLM-6B](https://github.com/THUDM/VisualGLM-6B) is a multimodal conversational model that supports image understanding. You can run the command-line and web demos through [cli_demo_vision.py](cli_demo_vision.py) and [web_demo_vision.py](web_demo_vision.py) in this repository, which load the [THUDM/visualglm-6b](https://huggingface.co/THUDM/visualglm-6b) checkpoint. Note that VisualGLM-6B additionally requires [SwissArmyTransformer](https://github.com/THUDM/SwissArmyTransformer/) and torchvision.

## Examples

The following are example screenshots produced with `web_demo.py`. More possibilities are waiting for you to explore!

<details><summary><b>Self-introduction</b></summary>

![](examples/self-introduction.png)

</details>

<details><summary><b>Outline writing</b></summary>

![](examples/blog-outline.png)

</details>

<details><summary><b>Ad and comment writing</b></summary>

![](examples/ad-writing-2.png)

![](examples/comments-writing.png)

</details>

<details><summary><b>Email writing</b></summary>

![](examples/email-writing-1.png)

![](examples/email-writing-2.png)

</details>

<details><summary><b>Role play</b></summary>

![](examples/role-play.png)

</details>

<details><summary><b>Sports</b></summary>

![](examples/sport.png)

</details>

<details><summary><b>Information extraction</b></summary>

![](examples/information-extraction.png)

</details>

<details><summary><b>Tour guide</b></summary>

![](examples/tour-guide.png)

</details>

## Limitations

Due to ChatGLM-6B's relatively small size, its capabilities still have many limitations:

* **Small model capacity**: the 6B capacity results in relatively weak memorization and language ability. On many factual knowledge tasks, ChatGLM-6B may generate incorrect information, and it is not good at solving logic-heavy problems such as math and programming.

  <details><summary><b>Click to see examples</b></summary>

  ![](limitations/factual_error.png)

  ![](limitations/math_error.png)

  </details>

* **Possibly harmful or biased content**: ChatGLM-6B is only roughly aligned with human intent and may generate harmful or biased content.
* **Limited English ability**: most of the instructions/answers used in training are Chinese, with only a small amount of English. Answers to English instructions are therefore of much lower quality than Chinese ones and can be inconsistent or mix Chinese and English.
* **Easily misled, weak dialogue ability**: ChatGLM-6B's dialogue ability is still weak, and its "self-perception" is flawed — when misled, the model may claim to be a model developed by another company.

  <details><summary><b>Click to see examples</b></summary>

  ![](limitations/self-confusion_google.jpg)

  ![](limitations/self-confusion_openai.jpg)

  ![](limitations/self-confusion_tencent.jpg)

  </details>

## FAQ

Troubleshooting notes (e.g., installing OpenMP on macOS to run the quantized model) are collected in [FAQ.md](FAQ.md).

## Community and feedback

* **Badcase feedback plan**: see [improve/README.md](improve/README.md) for how to submit prompts and improved answers (JSON Lines format with `prompt`/`response` fields; a sample is provided in [improve/data_sample.jsonl](improve/data_sample.jsonl)). Submitted data is screened and used to improve future open releases of the model.
* **Related open-source projects**: acceleration and reimplementation projects, downstream applications, fine-tuning projects, and tutorials are listed in [PROJECT.md](PROJECT.md).
* **WeChat**: join the developer group via [resources/WECHAT.md](resources/WECHAT.md).

## License

* The code of this repository is released under the [Apache-2.0 License](LICENSE).
* The use of the ChatGLM-6B **model weights** is subject to the [Model License](MODEL_LICENSE). The weights are fully open for academic research, and free commercial use is allowed after registering via this [questionnaire](https://open.bigmodel.cn/mla/form).

## Citation

If you find our work helpful, please consider citing the following paper:

```
@misc{glm2024chatglm,
      title={ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools},
      author={Team GLM and Aohan Zeng and Bin Xu and Bowen Wang and Chenhui Zhang and Da Yin and Diego Rojas and Guanyu Feng and Hanlin Zhao and Hanyu Lai and Hao Yu and Hongning Wang and Jiadai Sun and Jiajie Zhang and Jiale Cheng and Jiayi Gui and Jie Tang and Jing Zhang and Juanzi Li and Lei Zhao and Lindong Wu and Lucen Zhong and Mingdao Liu and Minlie Huang and Peng Zhang and Qinkai Zheng and Rui Lu and Shuaiqi Duan and Shudan Zhang and Shulin Cao and Shuxun Yang and Weng Lam Tam and Wenyi Zhao and Xiao Liu and Xiao Xia and Xiaohan Zhang and Xiaotao Gu and Xin Lv and Xinghan Liu and Xinyi Liu and Xinyue Yang and Xixuan Song and Xunkai Zhang and Yifan An and Yifan Xu and Yilin Niu and Yuantao Yang and Yueyan Li and Yushi Bai and Yuxiao Dong and Zehan Qi and Zhaoyu Wang and Zhen Yang and Zhengxiao Du and Zhenyu Hou and Zihan Wang},
      year={2024},
      eprint={2406.12793},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
