# Ethereum Improvement Proposals (EIPs)

This repository contains Ethereum Improvement Proposals (EIPs) and the source for the EIP website, [eips.ethereum.org](https://eips.ethereum.org). EIPs are design documents that provide information to the Ethereum community or describe proposed features, standards, or processes for Ethereum. The website organizes proposals by type and category and publishes their current status.

Read [EIP-1](EIPS/eip-1.md) for the authoritative description of the proposal process, document requirements, and style guidance.

## Proposal types and statuses

EIP-1 defines three proposal types:

- **Standards Track** proposals describe changes that affect Ethereum implementations or interoperability. Their categories are Core, Networking, Interface, and ERC.
- **Meta** proposals describe or change a process surrounding Ethereum.
- **Informational** proposals describe a design issue or provide guidance or information without proposing a new feature.

Tracked proposals progress through statuses such as Draft, Review, Last Call, and Final. Other statuses include Stagnant, Withdrawn, and Living. EIP-1 defines what each status means and how proposals move between them; an Idea is pre-draft and is not tracked in this repository.

## Repository contents

- `EIPS/` — EIP documents in Markdown. Each document has YAML front matter used for its metadata and website presentation.
- `assets/` — supporting files for proposals, generally organized in `assets/eip-N/` directories.
- `_config.yml`, `_layouts/`, `_includes/`, `_data/`, and the root-level HTML files — Jekyll configuration, templates, data, and pages used to generate the website.
- `rss/` — RSS feeds published by the website.
- `eip-template.md` — suggested template for a new EIP.
- `config/` — configuration for EIP linting, link checking, and editor metadata.
- `.github/workflows/` — continuous integration and GitHub Pages deployment workflows.

## Contributing

1. Review [EIP-1](EIPS/eip-1.md) before writing or changing a proposal. It explains EIP types, required sections and metadata, status transitions, and the authoring process.
2. For a new idea, EIP-1 recommends publicly vetting it with the community before preparing a formal draft. The preferred discussion venue named in EIP-1 is [Ethereum Magicians](https://ethereum-magicians.org/).
3. Prepare a draft using [`eip-template.md`](eip-template.md), then submit it as a pull request to this repository. The template asks new submissions to use an abbreviated draft filename (for example, `eip-draft_title_abbrev.md`); an EIP editor assigns the EIP number.
4. Put supporting images, data, and other auxiliary files in `assets/eip-N/` and link to them with relative paths. EIP references should also use relative Markdown links so they work in the repository and on the site.

ERC-related pull requests are directed to the separate [ethereum/ERCS](https://github.com/ethereum/ERCS) repository, as noted in this repository's pull request template. The Pages deployment workflow brings content from that repository together with the EIP source when building the published site.

The EIP template and EIP-1 specify a `Copyright` section waiving copyright and related rights via the repository's [CC0 license](LICENSE.md). Consult EIP-1 for the full requirements; a pull request is subject to review by EIP editors.

## Build the website locally

The site uses Jekyll. The GitHub Actions workflows set up Ruby 3.1 and install the locked Bundler dependencies.

```sh
bundle install
bundle exec jekyll serve
```

Jekyll serves the local site and rebuilds it as files change. To build the static site without serving it:

```sh
bundle exec jekyll build
```

The generated site is written to `_site/` (which is ignored by Git). These commands build the checked-out repository; the GitHub Pages workflow additionally combines the separate ERC repository's content before building for deployment.

## Validation

Pull-request CI includes a Jekyll build, HTML and site health checks, a Markdown link check, codespell, the EIP validator (`eipw` using `config/eipw.toml`), and Markdown linting for applicable changed files. The repository's `Gemfile` includes the tools used for the Jekyll, HTML, and EIP validation workflows. Run the checks in CI for the definitive validation of a proposed change.

## License

The repository includes [CC0 1.0 Universal](LICENSE.md). EIP documents use the copyright-waiver wording specified by EIP-1.
