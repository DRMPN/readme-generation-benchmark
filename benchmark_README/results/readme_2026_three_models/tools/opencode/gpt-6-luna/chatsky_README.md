# Chatsky

Chatsky is an open-source Python library for building dialog systems, including chatbots and virtual assistants. Conversations are described as graphs of flows and nodes: transitions use conditions to choose the next node, and nodes can provide responses and processing callbacks. A `Pipeline` runs the script, manages per-conversation context, and connects the dialog logic to a messenger interface.

Chatsky is developed by the Chatsky team at [DeepPavlov](https://deeppavlov.ai/) and is licensed under Apache-2.0.

- **Documentation:** [deeppavlov.github.io/chatsky](https://deeppavlov.github.io/chatsky/)
- **Source and issue tracker:** [github.com/deeppavlov/chatsky](https://github.com/deeppavlov/chatsky)
- **Project template:** [deeppavlov/chatsky-template](https://github.com/deeppavlov/chatsky-template)

## Installation

Chatsky supports Python 3.9 and newer (Python 3.9.7 is excluded). Install the base package with pip:

```bash
pip install chatsky
```

The base install includes the core library. Optional dependency groups are available for integrations and features:

```bash
pip install 'chatsky[json]'        # JSON context storage
pip install 'chatsky[pickle]'      # Pickle context storage
pip install 'chatsky[sqlite]'      # SQLite context storage
pip install 'chatsky[postgresql]' # PostgreSQL context storage
pip install 'chatsky[mysql]'       # MySQL context storage
pip install 'chatsky[mongodb]'     # MongoDB context storage
pip install 'chatsky[redis]'       # Redis context storage
pip install 'chatsky[ydb]'         # Yandex Database context storage
pip install 'chatsky[telegram]'    # Telegram messenger interface
pip install 'chatsky[stats]'       # Statistics and telemetry tools
pip install 'chatsky[benchmark]'   # Database benchmarking tools
pip install 'chatsky[yaml]'        # YAML pipeline import
pip install 'chatsky[llm]'         # LangChain integration
```

Install the extra(s) corresponding to the integrations you use. For LLMs, the model-provider package may also need to be installed separately; see the [LLM integration guide](https://deeppavlov.github.io/chatsky/user_guides/llm_integration.html).

## Quick start

This small dialog runs in the command line. The default messenger interface uses standard input and output.

```python
from chatsky import Pipeline, RESPONSE, TRANSITIONS, Transition as Tr
from chatsky import conditions as cnd

script = {
    "greeting_flow": {
        "start": {
            RESPONSE: 'Say "Hi" to start the conversation.',
            TRANSITIONS: [Tr(dst="greeting", cnd=cnd.ExactMatch("Hi"))],
        },
        "greeting": {
            RESPONSE: "Hello!",
            TRANSITIONS: [Tr(dst="start")],
        },
        "fallback": {
            RESPONSE: 'Say "Hi" to start the conversation.',
            TRANSITIONS: [Tr(dst="greeting", cnd=cnd.ExactMatch("Hi"))],
        },
    }
}

pipeline = Pipeline(
    script=script,
    start_label=("greeting_flow", "start"),
    fallback_label=("greeting_flow", "fallback"),
)

if __name__ == "__main__":
    pipeline.run()
```

Save this as a Python file and run it. Enter `Hi` to receive `Hello!`; other input uses the fallback node. The greeting flow then starts again. `Pipeline.run()` connects the pipeline to its messenger interface; you can also call a pipeline with a `Message` to process one request without starting the messenger.

## How it works

- A **script** contains named **flows**, with optional global defaults.
- A **flow** contains named **nodes**, with optional local defaults.
- A **node** can define a `RESPONSE`, `TRANSITIONS`, and pre-transition or pre-response processing. A transition pairs a condition with a destination node.
- A **context** holds a conversation's request and response history, node labels, and custom data. By default, the pipeline uses in-memory context storage; optional storage integrations are available.
- A **pipeline** combines the script and start/fallback labels with context storage, a messenger interface, and optional services. The default interface is the command-line interface.

Conditions, responses, destinations, processing callbacks, and priorities can be extended with user-defined functions. The library also includes slot-extraction components and optional LLM response and condition integrations. See the guides for details and examples.

## Documentation and examples

- [Getting started](https://deeppavlov.github.io/chatsky/get_started.html) — installation and core concepts.
- [User guides](https://deeppavlov.github.io/chatsky/user_guides.html) — context, storage, LLM integration, slot extraction, telemetry, optimization, and YAML/JSON pipeline import.
- [Tutorials](https://deeppavlov.github.io/chatsky/tutorials.html) — walkthroughs for scripts, services, context storage, Telegram, and web interfaces.
- [API reference](https://deeppavlov.github.io/chatsky/reference.html) — classes and interfaces.
- [Example projects](https://github.com/deeppavlov/dialog_flow_demo) — the examples repository linked from the documentation.

## Development

The project uses Poetry and Poe the Poet for dependency management and task automation. To install the development, test, tutorial, and documentation groups with all optional dependencies:

```bash
poetry install --with lint,test,devel,tutorials,docs --all-extras
```

Useful project tasks:

```bash
poetry run poe quick_test   # quick test run
poetry run poe test_no_cov  # tests without coverage
poetry run poe test_all     # all tests; requires Docker and Docker Compose
poetry run poe lint         # style checks
poetry run poe format       # format code with Black
poetry run poe docs         # build documentation
```

The documentation build requires Pandoc. `poetry run poe docs_no_docker` builds without Docker, but tutorials that need Docker services can fail and Draw.io diagrams are not built in that mode. See [CONTRIBUTING.md](CONTRIBUTING.md) for workflow and test details.

## License

Chatsky is distributed under the [Apache License 2.0](LICENSE).
