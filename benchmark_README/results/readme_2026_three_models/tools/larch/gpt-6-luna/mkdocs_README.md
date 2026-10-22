# MkDocs

MkDocs is a static site generator for project documentation. Write pages in Markdown, configure the site in a YAML file, and build a browsable website with a command-line tool.

This repository contains the MkDocs application, its built-in themes and search assets, documentation, and test suite.

## Features

- Markdown-based documentation with configurable navigation.
- A local development server with automatic rebuilds as files change.
- Static site generation for hosting on any web server.
- Built-in themes, including the default `mkdocs` theme and `readthedocs`.
- Themes and plugins that can be configured or extended.
- Search support and options for localizing themes.
- A Python API for integrating MkDocs into other tools.

## Requirements

MkDocs runs on Python. Install it with `pip`:

```bash
pip install mkdocs
```

For installation details and supported environments, see [installation.md](installation.md).

## Quick start

Create a new documentation project:

```bash
mkdocs new my-project
cd my-project
```

This creates a project containing a `mkdocs.yml` configuration file and a `docs/` directory with an example Markdown page. Start the local server:

```bash
mkdocs serve
```

Open the address printed by the command in your browser. By default, the server is available at `http://127.0.0.1:8000/`.

When you are ready to publish, build the static site:

```bash
mkdocs build
```

The generated site is written to the `site/` directory by default. Its contents can be hosted on any static web server.

## Configuration

MkDocs is configured through `mkdocs.yml`. A minimal configuration looks like this:

```yaml
site_name: My Documentation
```

A configuration can also specify navigation, themes, plugins, Markdown extensions, and other site options:

```yaml
site_name: My Documentation
site_url: https://example.com/
docs_dir: docs
site_dir: site

nav:
  - Home: index.md
  - Getting started: getting-started.md

theme:
  name: mkdocs

plugins:
  - search
```

The `docs_dir` setting identifies the source documentation directory; `site_dir` identifies where the generated site is written. The example uses their default values.

For the full set of configuration options, see [configuration.md](configuration.md). The documentation also covers [writing pages](writing-your-docs.md), [navigation](configuration.md), [themes](choosing-your-theme.md), [plugins](plugins.md), and [Markdown extensions](writing-your-docs.md).

## Command-line commands

Common commands include:

```bash
mkdocs new [project-directory]  # Create a new documentation project
mkdocs serve                    # Preview the site locally
mkdocs build                    # Build the static site
mkdocs gh-deploy                 # Build and publish to GitHub Pages
```

Use `mkdocs --help` or `mkdocs <command> --help` to see available options. For example, `mkdocs build --help` lists options for controlling a build.

More command-line guidance is in [cli.md](cli.md).

## Themes and plugins

MkDocs separates documentation content from its presentation. Choose a built-in or third-party theme, or customize a theme with your own CSS, JavaScript, and templates. See [choosing a theme](choosing-your-theme.md) and [customizing a theme](customizing-your-theme.md).

Plugins add behavior to the build process. Configure installed plugins in `mkdocs.yml`; plugin authors can use MkDocs’ plugin API and events. See [plugins.md](plugins.md) and [plugin-events.py](plugin-events.py).

## Publishing

`mkdocs build` generates a static site suitable for hosting on services such as GitHub Pages or Read the Docs. To publish to GitHub Pages using the configured repository, run:

```bash
mkdocs gh-deploy
```

Review [deploying-your-docs.md](deploying-your-docs.md) for deployment options and configuration advice.

## Documentation

The documentation in this repository includes:

- [Getting started](getting-started.md)
- [Installation](installation.md)
- [Configuration](configuration.md)
- [Writing your documentation](writing-your-docs.md)
- [Themes](choosing-your-theme.md) and [theme customization](customizing-your-theme.md)
- [Plugins](plugins.md)
- [Localization](localizing-your-theme.md) and [translations](translations.md)
- [Command-line reference](cli.md)
- [API reference](api.md)

The project’s documentation site is configured by `mkdocs.yml`.

## Development

To work on this repository, clone it and install the project into your development environment:

```bash
git clone <repository-url>
cd <repository-directory>
python -m pip install -e .
```

The repository includes separate requirements files for documentation and style tooling. Install them when working on those parts of the project:

```bash
python -m pip install -r requirements-docs.txt
python -m pip install -r requirements-style.txt
```

Run the test suite with:

```bash
python -m pytest
```

You can preview changes to the project documentation locally with:

```bash
mkdocs serve
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

## License

MkDocs is distributed under the terms of the license in [LICENSE](LICENSE).
