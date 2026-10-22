# MkDocs

MkDocs is a static site generator for project documentation. Write pages in
Markdown, configure the site in a YAML file, and build the result as static HTML.

## Features

- A built-in development server with live reload for previewing documentation.
- Two built-in themes: `mkdocs` and `readthedocs`.
- Site configuration, Markdown extensions, themes, and plugins that can be
  customized for a project.
- A built-in search plugin.
- Static output that can be hosted on GitHub Pages or another static web host.

## Installation

MkDocs requires Python 3.8 or later. Install it from PyPI with pip:

```bash
python -m pip install mkdocs
```

## Quick start

Create a project, then start the local development server:

```bash
mkdocs new my-project
cd my-project
mkdocs serve
```

Open <http://127.0.0.1:8000/> to preview the site. The new project contains a
`mkdocs.yml` configuration file and a `docs/` directory for Markdown source
files. The `site_name` setting is required; other configuration settings are
optional.

To build the site into the `site/` directory, run:

```bash
mkdocs build
```

The generated site consists of static files. For a GitHub Pages project site,
MkDocs also provides a deployment command:

```bash
mkdocs gh-deploy
```

See the deployment guide before using this command; it builds and pushes the
site to the configured GitHub Pages branch.

## Documentation

- [Getting started](https://www.mkdocs.org/getting-started/)
- [User guide](https://www.mkdocs.org/user-guide/), including installation,
  writing documentation, themes, configuration, CLI, and deployment
- [Developer guide](https://www.mkdocs.org/dev-guide/)
- [Release notes](https://www.mkdocs.org/about/release-notes/)

For command and option details, run `mkdocs --help` or `mkdocs <command> --help`.

## Contributing

Contributions to code and documentation, bug reports, and patch reviews are
welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and checks.

For questions and support, use [GitHub Discussions](https://github.com/mkdocs/mkdocs/discussions).
To report a bug, open an [issue](https://github.com/mkdocs/mkdocs/issues).

## License

MkDocs is distributed under the [BSD 2-Clause License](LICENSE).
