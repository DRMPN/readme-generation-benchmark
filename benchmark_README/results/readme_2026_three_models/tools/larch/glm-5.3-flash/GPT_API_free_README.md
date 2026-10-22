# GPT_API_free

<div align="center">
  <img src="logo.png" width="140" alt="GPT_API_free logo" />
  <p><strong>🔥 Free, OpenAI-compatible GPT API forwarding service</strong></p>
  <p>Works with <code>gpt-3.5-turbo</code>, <code>gpt-4</code>, <code>gpt-4o</code>, <code>embeddings</code>, <code>whisper</code> and more — usable from any client that speaks the OpenAI API.</p>
  <p>
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT" />
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs welcome" />
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs welcome" />
    <img src="https://img.shields.io/badge/Python-3.7%2B-blue.svg" alt="Python 3.7+" />
  </p>
</div>

---

## 📖 Table of Contents

- [Introduction](#-introduction)
- [Features](#-features)
- [Getting Started](#-getting-started)
  - [1. Get an API key](#1-get-an-api-key)
  - [2. Choose an endpoint (base URL)](#2-choose-an-endpoint-base-url)
  - [3. Run the demo](#3-run-the-demo)
- [Supported Models & Quotas](#-supported-models--quotas)
- [Use With Your Favorite Apps](#-use-with-your-favorite-apps)
  - [Chatbox](#chatbox)
  - [BotGem (formerly AMA)](#botgem-formerly-ama)
  - [GoMoon](#gomoon)
  - [Zotero GPT](#zotero-gpt)
  - [Zotero PDF Translate](#zotero-pdf-translate)
  - [Browser Sidebar Extensions](#browser-sidebar-extensions)
  - [JetBrains IDEs](#jetbrains-ides)
- [API Usage Examples](#-api-usage-examples)
- [Project Structure](#-project-structure)
- [FAQ](#-faq)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## 🚀 Introduction

**GPT_API_free** provides a **free forwarding API** for OpenAI's GPT models. It acts as a transparent proxy in front of the official OpenAI API, exposing the exact same endpoints (`/v1/chat/completions`, `/v1/embeddings`, `/v1/models`, …), so **any tool, library, or plugin that already supports OpenAI works out of the box** — you only need to change two things:

1. The **base URL** (API host) — point it at our proxy instead of `https://api.openai.com/v1`
2. The **API key** — use a key issued by this service (keys start with `sk-` just like OpenAI's)

No VPN, no credit card, no code changes required. Ideal for students, researchers, and developers who want to plug GPT into Zotero, Chatbox, JetBrains IDEs, browser extensions, or their own Python/Node.js projects.

---

## ✨ Features

- 💸 **Free tier** — claim a free `sk-` key and start using GPT models immediately
- 🔌 **Fully OpenAI-compatible** — same request/response format as the official API
- 🌍 **Two endpoints** — a global endpoint and a mainland-China-friendly endpoint (no proxy needed)
- 🧰 **Works everywhere** — Chatbox, BotGem, GoMoon, Zotero plugins, JetBrains IDEs, browser sidebars, `openai` Python/Node SDKs, LangChain, and any custom app
- 🚄 **Streaming support** — token-by-token streaming (`stream=True`) is fully supported
- 🔒 **No data retention** — requests are forwarded as-is; nothing is stored

---

## 🏁 Getting Started

### 1. Get an API key

Free keys are distributed through the official portal and community channels announced by the project:

1. ⭐ Star this repository (it helps more people find the service).
2. Visit the official portal at <https://api.chatanywhere.tech> (or join the group chat linked in the project announcements) and follow the steps to claim a **free API key**.
3. You will receive a key in the form `sk-xxxxxxxxxxxxxxxxxxxxxxxx`.

> ⚠️ **Notes**
> - Keys issued by this service **only work with the base URLs below**, not with `api.openai.com`.
> - Never commit your key to a public repository. If it leaks, claim a new one.
> - Free keys are rate-limited. If you need higher quotas, paid keys with larger limits are also available through the same portal.

### 2. Choose an endpoint (base URL)

Depending on your network location, pick one of the following **base URLs** and append `/v1` where required:

| Base URL | Recommended for | Notes |
|---|---|---|
| `https://api.chatanywhere.tech/v1` | 🌍 Global users | Full model support, including `gpt-4` / `gpt-4o` |
| `https://api.chatanywhere.com.cn/v1` | 🇨🇳 Mainland China | Direct connection without a proxy; supports `gpt-3.5-turbo`, embeddings and other core models |

> 💡 In most clients you only paste the host part (`https://api.chatanywhere.tech`); some clients want the full path including `/v1`. Check your client's naming — it may say *API Host*, *API Domain*, *Base URL*, or *Custom API*.

### 3. Run the demo

A minimal, ready-to-run example is included in **`demo.py`**:

```bash
git clone https://github.com/chatanywhere/GPT_API_free.git
cd GPT_API_free

# Install the official OpenAI SDK
pip install --upgrade openai

# Edit demo.py and set:
#   base_url = "https://api.chatanywhere.tech/v1"
#   api_key  = "sk-你的key / your key"

python demo.py
```

---

## 📦 Supported Models & Quotas

Availability and rate limits are subject to change. Free keys are intended for **light, personal use**; paid keys offer much higher limits. You can always query the live model list:

```bash
curl https://api.chatanywhere.tech/v1/models \
  -H "Authorization: Bearer sk-你的key"
```

| Model family | Free key | Typical use |
|---|:---:|---|
| `gpt-3.5-turbo` / `gpt-3.5-turbo-16k` | ✅ | Fast chat, translation, summarization |
| `gpt-4o-mini` | ✅ | Cheap, high-quality chat |
| `gpt-4` / `gpt-4-turbo` | ⚠️ limited | Complex reasoning (paid recommended) |
| `gpt-4o` | ⚠️ limited | Latest multimodal flagship |
| `text-embedding-3-small` / `-large` / `ada-002` | ✅ | Embeddings / semantic search |
| `whisper-1` | ✅ limited | Speech-to-text |
| `dall-e` / image models | ❌ | Not available on the free tier |

> ⚠️ Free-tier limits (roughly on the order of tens of requests per minute for `gpt-3.5-turbo`, lower for `gpt-4`) are enforced per key. When you exceed them you will receive HTTP `429`; wait a moment and retry, or upgrade to a paid key.

---

## 🧰 Use With Your Favorite Apps

The general recipe is identical for **every** OpenAI-compatible app:

> 1. Find the setting named *API Host / API Domain / Base URL / Custom API*.
> 2. Replace `api.openai.com` with `api.chatanywhere.tech` (or `api.chatanywhere.com.cn`).
> 3. Paste your `sk-` key.
> 4. Pick a model, e.g. `gpt-3.5-turbo`.

Detailed guides below.

### Chatbox

A popular cross-platform (Windows/macOS/Linux/Web) chat client.

1. Download and install Chatbox.
2. Open **Settings → Model Provider → Custom Model** (or *OpenAI API*).
3. Set **API Domain** to `https://api.chatanywhere.tech`.
4. Paste your **API Key**, choose a **Model** such as `gpt-3.5-turbo`, and save.
5. Start chatting! 🎉

![Chatbox](chatbox.png)

### BotGem (formerly AMA)

1. Download BotGem from the official website.
2. Go to **Settings → OpenAI**.
3. Enable the **custom API host** option and set it to `https://api.chatanywhere.tech/v1`.
4. Paste your key, select a model, and save.

![BotGem](botgem.png)

### GoMoon

1. Install GoMoon.
2. Open **Settings → API configuration**.
3. Switch to the *custom / OpenAI-compatible* provider, enter the base URL, your key, and a model name.

![GoMoon](gomoon.png)

### Zotero GPT

Adds a ChatGPT window to [Zotero](https://www.zotero.org/) so you can chat with, summarize, and query your PDF library. Supports both **Zotero 6** and **Zotero 7**.

1. Download the latest `.xpi` from the [zotero-gpt releases](https://github.com/MuiseDestiny/zotero-gpt/releases).
2. In Zotero: **Tools → Plugins → gear icon → Install Plugin From File** and select the `.xpi`.
3. Open the plugin settings (**Edit → Preferences → zotero GPT**) and configure:
   - **Secret Key**: your `sk-` key
   - **API URL**: `https://api.chatanywhere.tech/v1/chat/completions`
   - **Model**: e.g. `gpt-3.5-turbo`
4. Restart Zotero. Press <kbd>Alt</kbd>+<kbd>/</kbd> (Windows/Linux) or <kbd>⌘</kbd>+<kbd>/</kbd> (macOS) to summon the GPT window.

**Zotero 6:**

![Zotero GPT](zotero-gpt.png)

**Zotero 7:**

![Zotero 7 GPT — step 1](zotero7-gpt1.png)

![Zotero 7 GPT — step 2](zotero7-gpt2.png)

### Zotero PDF Translate

Machine-translation for PDFs inside Zotero, powered by GPT.

1. Install the [zotero-pdf-translate](https://github.com/windingwind/zotero-pdf-translate) plugin.
2. Open **Zotero → Edit → Preferences → Translate**.
3. Under **Services**, register a **GPT** service:
   - **API URL**: `https://api.chatanywhere.tech/v1/chat/completions`
   - **API Key**: your `sk-` key
   - **Model**: `gpt-3.5-turbo`
4. Select text in the PDF reader and hit the translate button — enjoy academic-quality translation. 📚

![Zotero PDF Translate](zotero-pdf-translate.png)

### Browser Sidebar Extensions

Sidebar-style assistants (e.g., Sider / *ChatGPT Sidebar* and similar Chrome/Edge extensions) support custom OpenAI endpoints:

1. Open the extension's **Settings**.
2. Choose the **custom OpenAI API** option.
3. Set **API Host** to `https://api.chatanywhere.tech/v1`, paste your key, and select a model.
4. Pin the extension and use GPT on any page.

![Sidebar extension](sidebar.png)

### JetBrains IDEs

Works in **IntelliJ IDEA, PyCharm, WebStorm, GoLand, CLion, Android Studio**, etc. using a plugin such as **CodeGPT** (or any "OpenAI compatible" AI plugin):

1. Install **CodeGPT** from *Settings → Plugins → Marketplace*.
2. Go to *Settings → Tools → CodeGPT → Providers* and select **Custom OpenAI-compatible**.
3. Set **Base URL** to `https://api.chatanywhere.tech/v1` and paste your API key.
4. Choose a model such as `gpt-3.5-turbo`.
5. Open the tool-window chat, or select code in the editor and use **CodeGPT actions** (explain, refactor, write tests, …).

![JetBrains setup 1](jet1.png)

![JetBrains setup 2](jet2.png)

---

## 💻 API Usage Examples

### Python — official `openai` SDK (v1.x)

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-你的key",                              # your key from this service
    base_url="https://api.chatanywhere.tech/v1",       # ← the only change you need
)

# --- Normal request ---
resp = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! Who are you?"},
    ],
)
print(resp.choices[0].message.content)

# --- Streaming request ---
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Count from 1 to 10."}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

### Python — legacy SDK (`openai<1.0`, as used in `demo.py`)

```python
import openai

openai.api_base = "https://api.chatanywhere.tech/v1"
openai.api_key = "sk-你的key"

resp = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(resp.choices[0].message.content)
```

### Node.js

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "sk-你的key",
  baseURL: "https://api.chatanywhere.tech/v1",
});

const completion = await client.chat.completions.create({
  model: "gpt-3.5-turbo",
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(completion.choices[0].message.content);
```

### cURL

```bash
curl https://api.chatanywhere.tech/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-你的key" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## 📁 Project Structure

```
GPT_API_free/
├── demo.py                   # Minimal, runnable Python usage example
├── LICENSE                   # MIT license
├── logo.png                  # Project logo
├── chatbox.png               # Screenshot: Chatbox setup
├── botgem.png                # Screenshot: BotGem setup
├── gomoon.png                # Screenshot: GoMoon setup
├── sidebar.png               # Screenshot: Browser sidebar extension setup
├── zotero-gpt.png            # Screenshot: Zotero GPT (Zotero 6)
├── zotero7-gpt1.png          # Screenshot: Zotero GPT (Zotero 7), step 1
├── zotero7-gpt2.png          # Screenshot: Zotero GPT (Zotero 7), step 2
├── zotero-pdf-translate.png  # Screenshot: Zotero PDF Translate setup
├── jet1.png                  # Screenshot: JetBrains IDE setup, step 1
└── jet2.png                  # Screenshot: JetBrains IDE setup, step 2
```

---

## ❓ FAQ

<details>
<summary><b>401 Unauthorized / invalid API key</b></summary>

Make sure you are calling the **proxy base URL**, not `api.openai.com`, and that the key belongs to this service. Keys from OpenAI won't work here and vice-versa. Check for missing `/v1` or typos.
</details>

<details>
<summary><b>429 Too Many Requests</b></summary>

You've hit the free-tier rate limit. Wait a few seconds and retry with exponential backoff, batch your work, or upgrade to a paid key for higher quotas.
</details>

<details>
<summary><b>Timeouts or connection errors from mainland China</b></summary>

Use the domestic endpoint `https://api.chatanywhere.com.cn/v1`, which connects without a VPN.
</details>

<details>
<summary><b>Can I use the official OpenAI SDK / LangChain?</b></summary>

Yes — that's the whole point. The API is 100% OpenAI-compatible; just override `base_url`/`api_base` (OpenAI SDK) or `openai_api_base` (LangChain) and set your key.
</details>

<details>
<summary><b>Is my conversation data stored?</b></summary>

The service forwards requests to the upstream provider and does not retain your message content. Still, avoid sending sensitive or confidential data through any third-party API.
</details>

<details>
<summary><b>Which models can I call?</b></summary>

Query `GET /v1/models` with your key for the authoritative, always-up-to-date list. See the [models table](#-supported-models--quotas) for an overview.
</details>

---

## ⚠️ Disclaimer

- This is a **community-provided free service**. It comes with **no SLA**: rate limits may change, capacity may be restricted, and the service may be interrupted without notice.
- Free keys are for **personal, light use only**. Heavy scraping, reselling, or abuse will cause keys to be revoked.
- This project is **not affiliated with OpenAI**. "OpenAI", "GPT", "ChatGPT" and related marks are trademarks of their respective owners.
- Use the service in compliance with all applicable laws and the upstream provider's terms of service.

---

## 🤝 Contributing

Found a bug in `demo.py`? Use a client we haven't documented yet? PRs are welcome — especially new setup tutorials with screenshots. Just open a pull request.

If this project helps you, please **star ⭐ the repo** and share it — it keeps the free service alive.

---

## 📄 License

Released under the [MIT License](LICENSE). You are free to use, modify, and distribute this repository's code with attribution.
