# LLM API Integration Demo

This repository provides a demonstration of how to integrate and utilize large language model (LLM) APIs, specifically showcasing interaction with a GPT-3.5-turbo compatible endpoint via Python.

## ⚙️ Features

*   **API Interaction**: Demonstrates making chat completion calls to an external LLM service.
*   **Streaming Support**: Implements a function to receive responses in a streaming fashion for a better user experience.
*   **Synchronous Mode**: Includes a function for receiving complete, non-streamed responses.

## 🚀 Getting Started

### Prerequisites

*   Python 3.x
*   An API Key for the target LLM service.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [repository-url]
    cd [repository-name]
    ```
2.  **Install dependencies:**
    This project primarily uses the `openai` library.
    ```bash
    pip install openai
    ```
3.  **Configuration:**
    Update `demo.py` with your actual API key in the client initialization block:
    ```python
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key="YOUR API KEY", # <-- Update this
        base_url="https://api.chatanywhere.tech/v1"
    )
    ```

## 💡 Usage

The core functionality is demonstrated in `demo.py`.

1.  **Run the script:**
    ```bash
    python demo.py
    ```

2.  **API Functions:**
    *   `gpt_35_api(messages)`: Executes a request and prints the full response content when the request is complete.
    *   `gpt_35_api_stream(messages)`: Executes a request and prints chunks of the response as they are received, providing real-time output.

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.
