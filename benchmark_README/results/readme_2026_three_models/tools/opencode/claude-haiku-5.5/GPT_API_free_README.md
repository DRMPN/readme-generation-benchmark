# GPT_API_free

![logo](images/logo.png)

A small collection of usage notes and a Python demo for calling OpenAI-compatible chat completion APIs through the third-party relay endpoint `https://api.chatanywhere.tech/v1`. The repository also contains screenshots of third-party desktop clients and plugins configured with the same endpoint.

## Contents

- `demo.py`: a minimal Python script that sends one chat request, in either non-streaming or streaming mode, using the `openai` Python package.
- `images/`: screenshots referenced by the setup notes below.
- `LICENSE`: MIT License.

## Requirements

- Python 3
- The `openai` Python package

```bash
pip install openai
```

`demo.py` uses the `OpenAI` client class from the `openai` package (the v1+ client interface, `client.chat.completions.create`).

## Usage

1. Get an API key from the relay service. The key is a secret; do not commit it to version control.
2. Open `demo.py` and replace the placeholder:

   ```python
   client = OpenAI(
       api_key="YOUR API KEY",
       base_url="https://api.chatanywhere.tech/v1"
   )
   ```

   The code comment notes that the client defaults to reading `OPENAI_API_KEY` from the environment if `api_key` is not passed. You can instead set that environment variable and remove the hard-coded key.

3. Run the script:

   ```bash
   python demo.py
   ```

By default, `demo.py` runs the streaming example. The non-streaming example is present but commented out in the `__main__` block; to use it, swap the commented lines:

```python
if __name__ == '__main__':
    messages = [{'role': 'user', 'content': '鲁迅和周树人的关系'},]
    # gpt_35_api(messages)          # non-streaming
    gpt_35_api_stream(messages)     # streaming
```

## Functions in `demo.py`

| Function | Mode | Behavior |
| --- | --- | --- |
| `gpt_35_api(messages)` | Non-streaming | Sends the messages with `model="gpt-3.5-turbo"` and prints the full reply. |
| `gpt_35_api_stream(messages)` | Streaming | Sends the messages with `stream=True` and prints each content delta as it arrives. |

Both functions take a list of OpenAI-style message dictionaries, for example:

```python
messages = [{'role': 'user', 'content': 'Hello'}]
```

The model name is hard-coded to `gpt-3.5-turbo`. Change the `model=` argument in the functions to use another model that the endpoint supports.

## Third-party clients (screenshots)

The `images/` folder contains screenshots of clients configured with the relay endpoint. These clients are not part of this repository and their source is not included here.

- **Chatbox** (`images/chatbox.png`): the settings dialog with the provider set to "OpenAI API", the API key field, and the API host set to `https://api.chatanywhere.tech`.
- **Zotero plugin** (`images/zotero-gpt.png`, `images/zotero7-gpt1.png`, `images/zotero7-gpt2.png`, `images/zotero-pdf-translate.png`): a Zotero plugin workflow. The screenshot shows an `/api` command set to the relay URL and a `/secretKey` command used to store the key, followed by actions such as AskPDF, Translate, Improve writing, Clipboard, Annotations, Selection, Item, and Items.

Screenshot annotations (in Chinese) state that the key must be a forwarding key ("转发key") for the relay to work, and that the `sk-` prefix must be included when entering the key. The `xxxxx` in the Zotero screenshot is a placeholder.

Other images in `images/` (`sidebar.png`, `botgem.png`, `gomoon.png`, `jet1.png`, `jet2.png`) are included in the repository but are not described here.

## Notes and limitations

- This repository does not include the relay service itself, and it does not verify the service's availability, pricing, terms, or model list. Check the provider's documentation before relying on it.
- The endpoint is a third-party relay rather than OpenAI's own API. Per the Chatbox screenshot, sending a key to a non-official host means the key and message contents are transmitted to that host.
- `demo.py` has no error handling, retries, or configuration file; it is intended as a minimal example.
- The example prompt in `demo.py` is in Chinese (`鲁迅和周树人的关系`, "the relationship between Lu Xun and Zhou Shuren"). Responses will follow the language of the prompt.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for the full text. Copyright (c) 2023-2024 牛爷爷信息技术（南京）有限公司.
