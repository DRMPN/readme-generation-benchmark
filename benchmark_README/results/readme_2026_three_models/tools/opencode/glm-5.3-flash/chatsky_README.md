# Chatsky

Chatsky is a free and open-source software stack for creating chatbots, released under the terms of the Apache License 2.0. It is developed specifically for creating dialog systems, targeting a wide range of applications, including chatbots, virtual assistants, and other interactive systems.

Chatsky allows developers to easily create and manage complex dialog flows, integrate with natural language processing (NLP) tools, and handle user input in a flexible and efficient manner. The framework is highly customizable, allowing developers to easily adapt it to their specific needs and requirements.

## Features

* **Dialog Scripting Language (DSL):** Write dialog graphs using a specialized Python-based DSL.
* **Modular Structure:** Divide dialogs into `Script` (top-level container), `Flow` (sub-dialogs), and `Node` (smallest units of interaction).
* **Context Storages:** Supports various database backends for persisting conversation context, including PostgreSQL, MongoDB, Redis, SQLite, MySQL, YDB, JSON, and Pickle.
* **Extensible Pipeline:** Manage transitions and responses via a `Pipeline`.
* **Slots:** Extract structured data from user input.
* **LLM Integration:** Integrate with Large Language Models (via `langchain`).
* **Statistics and Benchmarking:** Built-in support for collecting stats and benchmarking.

## Installation

Chatsky requires Python 3.9 or newer. Install via pip:

```bash
pip install chatsky
```

To install optional dependencies (such as database drivers or messaging interfaces), use the extras:

```bash
pip install chatsky[json]      # dependencies for using JSON
pip install chatsky[pickle]    # dependencies for using Pickle
pip install chatsky[redis]     # dependencies for using Redis
pip install chatsky[mongodb]   # dependencies for using MongoDB
pip install chatsky[mysql]     # dependencies for using MySQL
pip install chatsky[postgresql]# dependencies for using PostgreSQL
pip install chatsky[sqlite]    # dependencies for using SQLite
pip install chatsky[ydb]       # dependencies for using Yandex Database
pip install chatsky[telegram]  # dependencies for using Telegram
pip install chatsky[benchmark] # dependencies for benchmarking
```

### Project Template

If you don't want to bother with setting up project files, you can use the [Chatsky Project Template](https://github.com/deeppavlov/chatsky-template) repository, which offers a ready-to-use simple bot that can be modified to your needs.

## Quick Start

To create a dialog agent, define a `Script`. A script is a dictionary where the keys correspond to different `flows`, which in turn contain `nodes`.

Here is a basic example of a simple greeting flow:

```python
from chatsky import (
    TRANSITIONS,
    RESPONSE,
    Pipeline,
    Transition as Tr,
    conditions as cnd,
)

# A script is a dictionary of flows. Each flow is a dictionary of nodes.
toy_script = {
    "greeting_flow": {
        "start_node": {
            TRANSITIONS: [Tr(dst="node1", cnd=cnd.ExactMatch("Hi"))],
        },
        "node1": {
            RESPONSE: "Hi, how are you?",
            TRANSITIONS: [
                Tr(dst="node2", cnd=cnd.ExactMatch("I'm fine, how are you?"))
            ],
        },
        "node2": {
            RESPONSE: "Good. What do you want to talk about?",
            TRANSITIONS: [
                Tr(dst="node3", cnd=cnd.ExactMatch("Let's talk about music."))
            ],
        },
        "node3": {
            RESPONSE: "Sorry, I can not talk about music now.",
            TRANSITIONS: [Tr(dst="node4", cnd=cnd.ExactMatch("Ok, goodbye."))],
        },
        "node4": {
            RESPONSE: "Bye",
            TRANSITIONS: [Tr(dst="node1", cnd=cnd.ExactMatch("Hi"))],
        },
        "fallback_node": {
            RESPONSE: "Ooops",
            TRANSITIONS: [Tr(dst="node1", cnd=cnd.ExactMatch("Hi"))],
        },
    }
}

# Pipeline processes user inputs and produces responses.
pipeline = Pipeline(
    script=toy_script,
    start_label=("greeting_flow", "start_node"),
    fallback_label=("greeting_flow", "fallback_node"),
)

if __name__ == "__main__":
    pipeline.run()  # Runs the pipeline with a preconfigured interface (CLI by default)
```

### Key Concepts

* **Script**: A dictionary where keys correspond to different `flows`, used to divide a dialog into sub-dialogs and process them separately.
* **Flow**: Represents a sub-dialog corresponding to the discussion of a particular topic. Each flow is also a dictionary, where the keys are `nodes`.
* **Node**: The smallest unit of a dialog flow. It contains the bot's response to a user's input as well as conditions that determine the `transition` to another node.
* **Keywords**: `RESPONSE` (the response the bot sends) and `TRANSITIONS` (conditions for moving to other nodes).

## Documentation

Comprehensive documentation, including API references, user guides, and interactive tutorials, is available at [deeppavlov.github.io/chatsky](https://deeppavlov.github.io/chatsky/).

The repository also contains a `tutorials` directory with interactive examples.

## Contributing

We will be glad to receive your pull requests (PRs) and issues. Please refer to [CONTRIBUTING.md](./CONTRIBUTING.md) for details on how to contribute, including virtual environment setup and code style guidelines.

## License

Chatsky is released under the [Apache License 2.0](./LICENSE).
