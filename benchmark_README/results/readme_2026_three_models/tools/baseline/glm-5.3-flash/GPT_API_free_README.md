# ChatAnywhere API 示例项目

本项目提供了基于 OpenAI 官方 SDK 调用 ChatAnywhere API 的示例代码，演示了如何以**非流式**和**流式**两种方式调用 GPT 模型（如 `gpt-3.5-turbo`）完成对话任务。仓库同时包含多款支持该 API 的第三方客户端工具的截图（如 Chatbox、BotGem、GoMoon、JetBrains 插件、Zotero GPT / PDF Translate 插件等），可用于快速了解接入该 API 的常见应用场景。

## 项目简介

ChatAnywhere 提供了一个与 OpenAI 官方接口兼容的 API 服务端点（`https://api.chatanywhere.tech/v1`）。这意味着凡是支持 OpenAI SDK 的语言和工具，只需将 `base_url` 替换为该端点并填入自己的 API Key，即可直接使用。

仓库中的 `demo.py` 使用官方 `openai` Python SDK，展示了两种最基本的调用方式：

- **非流式响应**：一次性返回完整的回答内容，适合对响应完整性要求高的场景。
- **流式响应（Streaming）**：服务端逐步返回内容，客户端逐块打印，能够显著改善交互体验（“打字机”效果）。

## 目录结构

```
.
├── demo.py                                   # Python 调用示例（非流式 / 流式）
├── images/                                   # 相关客户端与插件截图
│   ├── logo.png
│   ├── chatbox.png                           # Chatbox 客户端
│   ├── botgem.png                            # BotGem 客户端
│   ├── gomoon.png                            # GoMoon 客户端
│   ├── jet1.png / jet2.png                   # JetBrains 插件
│   ├── zotero-gpt.png / zotero7-gpt1.png 等  # Zotero GPT / 翻译插件
│   └── sidebar.png
├── .github/ISSUE_TEMPLATE/                   # Issue 模板（bug 报告 / 功能建议）
├── LICENSE                                   # MIT 许可证
└── README.md
```

## 环境要求

- Python 3.x
- `openai` Python SDK（需使用支持 `client.chat.completions.create` 新版接口的版本，即 `openai >= 1.0`）

安装依赖：

```bash
pip install --upgrade openai
```

## 快速开始

1. **获取 API Key**：在 ChatAnywhere 平台注册并获取属于你自己的 API Key。

2. **配置示例代码**：编辑 `demo.py`，将 `api_key` 替换为你的 Key：

   ```python
   client = OpenAI(
       # 默认会读取环境变量 os.environ.get("OPENAI_API_KEY")
       api_key="YOUR API KEY",
       base_url="https://api.chatanywhere.tech/v1"
   )
   ```

   > 安全提示：不建议将 API Key 硬编码在代码中并提交到版本库。推荐通过环境变量提供密钥：
   >
   > ```bash
   > export OPENAI_API_KEY="sk-xxxx"
   > ```
   > 此时可将 `api_key` 参数省略，SDK 会自动读取 `OPENAI_API_KEY` 环境变量。

3. **运行示例**：

   ```bash
   python demo.py
   ```

   默认入口执行的是流式调用，终端会逐字打印模型对问题「鲁迅和周树人的关系」的回答。

## 使用说明

### 非流式调用

`demo.py` 中的 `gpt_35_api(messages)` 函数演示了非流式调用：

```python
def gpt_35_api(messages: list):
    """为提供的对话消息创建新的回答"""
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print(completion.choices[0].message.content)
```

调用后一次性拿到完整回答，适合后端批处理等场景。在 `__main__` 中取消注释 `gpt_35_api(messages)` 即可切换为非流式模式。

### 流式调用

`gpt_35_api_stream(messages)` 函数演示了流式传输：

```python
def gpt_35_api_stream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)"""
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
```

通过设置 `stream=True`，返回值变为一个可迭代的分块流；每个分块携带增量内容（`delta.content`），客户端按顺序拼接即可实现实时输出。

### 消息格式

`messages` 参数遵循 OpenAI Chat Completions 的标准格式，每个元素包含 `role` 与 `content` 字段：

```python
messages = [
    {'role': 'user', 'content': '鲁迅和周树人的关系'},
]
```

如需多轮对话，将历史消息按顺序全部传入 `messages` 即可。

## 配置说明

| 配置项 | 说明 |
| --- | --- |
| `api_key` | ChatAnywhere 分配的 API Key；也可通过环境变量 `OPENAI_API_KEY` 提供 |
| `base_url` | API 端点，示例中使用 `https://api.chatanywhere.tech/v1` |
| `model` | 模型名称，示例使用 `gpt-3.5-turbo`，可按需更换为其他可用模型 |
| `stream` | 是否启用流式响应，`True` 为流式 |

## 相关客户端与插件

仓库 `images/` 目录收录了多种可直接配置该 API 端点的第三方工具截图，包括：

- **Chatbox**、**BotGem（AMA）**、**GoMoon** 等桌面聊天客户端；
- **JetBrains 系列 IDE 的 AI 插件**（jet1/jet2 截图）；
- **Zotero 的 GPT 与 PDF 翻译插件**（zotero-gpt、zotero-pdf-translate 等，兼容 Zotero 7）。

这些工具通常只需在设置中填入 API 地址（`https://api.chatanywhere.tech/v1`）与个人 Key 即可使用。

## 开发与贡献

- 项目包含 `.github/ISSUE_TEMPLATE` 下的两种 Issue 模板：
  - **Bug report（Bug 报告）**：请描述 Bug 现象、复现步骤、截图、所使用的工具或编程语言及其他补充信息（模板提供中英双语栏目）。
  - **Feature request（功能建议）**：标题建议以 `[Enhancement]` 开头，请说明要解决的问题、期望的解决方案、已考虑的替代方案及补充背景。
- 提交 Issue 或 Pull Request 前请先阅读相应模板，按格式填写以便更快获得反馈。

## 测试

仓库未包含自动化测试套件。验证功能最直接的方式是运行示例脚本并观察输出：

```bash
python demo.py
```

若流式输出正常逐字打印回答，说明 API Key、网络与 SDK 配置均工作正常；如遇报错，可按照 Bug 报告模板提交 Issue。

## 许可证

本项目基于 [MIT License](LICENSE) 开源。

Copyright (c) 2023-2024 牛爷爷信息技术（南京）有限公司

在遵守许可证条款的前提下，任何人可免费使用、复制、修改、合并、发布、分发、再许可及销售本软件的副本。软件按“现状”提供，作者不对软件的适用性、正确性或任何损害承担责任。
