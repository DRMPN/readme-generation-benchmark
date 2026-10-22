# GPT API Examples

This repository contains a small Python example for calling Chat Completions through the ChatAnywhere API endpoint, along with screenshots showing API configuration in several applications.

## Python example

`demo.py` uses the OpenAI Python client with `https://api.chatanywhere.tech/v1` as its base URL and the `gpt-3.5-turbo` model. It defines both a regular response function and a streaming response function. When run directly, it sends a sample Chinese-language question and prints the streamed response.

### Requirements

- Python
- The OpenAI Python package
- An API key accepted by the configured endpoint

Install the package with:

```bash
python -m pip install openai
```

### Run

In `demo.py`, replace `YOUR API KEY` with your API key, then run:

```bash
python demo.py
```

The script uses streaming by default. To use the non-streaming example instead, uncomment `gpt_35_api(messages)` and comment out `gpt_35_api_stream(messages)` in the `__main__` block.

The example currently places the API key directly in the source file. Avoid committing a real key; the OpenAI client also supports reading `OPENAI_API_KEY` from the environment if you adapt the client initialization.

## Screenshots

The images directory contains configuration examples and application screenshots. These are reference images; the repository does not include the applications shown.

### Zotero

![Zotero GPT settings](images/zotero-gpt.png)

![Zotero PDF translation settings](images/zotero-pdf-translate.png)

![Zotero 7 plugin installation](images/zotero7-gpt1.png)

![Zotero 7 GPT settings](images/zotero7-gpt2.png)

### Other application settings

![Sidebar settings](images/sidebar.png)

![Chat box settings](images/chatbox.png)

![BotGem settings](images/botgem.png)

![GoMoon settings](images/gomoon.png)

![JetBrains plugin screenshot](images/jet1.png)

![JetBrains API settings](images/jet2.png)

![Project logo](images/logo.png)

## License

This repository is distributed under the MIT License. See [LICENSE](LICENSE).
