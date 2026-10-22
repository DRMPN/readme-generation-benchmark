# Ethereum Improvement Proposals (EIPs)

This repository contains the text, supporting files, and website source for Ethereum Improvement Proposals. An EIP is a design document that informs the Ethereum community, proposes a feature or process change, or records the rationale and technical details of a proposal. EIPs are maintained as versioned Markdown files, making the repository’s history part of the record of each proposal.

The repository also contains the Jekyll source used to render proposal documents and related pages as a website. It is primarily a documentation and publishing project: proposals may include code examples, test vectors, diagrams, and other supporting material, but the repository is not itself an Ethereum client or a single software implementation.

For the process and requirements that govern proposals, read [EIP-1](EIPS/eip-1.md). New proposal drafts should follow the repository’s [EIP template](eip-template.md).

## Repository contents

- **`EIPS/`** — individual proposal documents, generally named `eip-N.md`. Documents have front matter describing proposal metadata, such as title, author, status, type, and creation date. Not every document has the same fields; consult EIP-1 for requirements.
- **`assets/`** — supporting material associated with proposals, including images, diagrams, data, test vectors, and reference files. Proposal-specific material is commonly stored in a directory such as `assets/eip-N/`.
- **`eip-template.md`** — the suggested structure for drafting an EIP, including sections such as Abstract, Specification, Security Considerations, and Copyright.
- **Jekyll site files** — `_config.yml`, `_layouts/`, `_includes/`, page files, stylesheets, and RSS feeds support rendering and organizing proposals as a site.
- **`config/`** — configuration files for repository checks and formatting tools, including `eipw.toml`, Markdown lint configuration, a codespell whitelist, and link-checker configuration.
- **`.github/`** — contribution guidance, issue and pull-request templates, ownership information, and GitHub Actions workflows.

Proposal statuses vary. The repository includes drafts and proposals at other stages, as well as living documents and files that indicate a proposal has moved elsewhere. A proposal’s status is metadata, not an indication that every proposal in the repository is a current or adopted specification.

## Setup

You can read and edit the Markdown documents without installing project dependencies. To preview or build the website locally, the repository’s `Gemfile` and Jekyll-related files indicate a Ruby and Bundler-based setup.

1. Install Ruby and Bundler if they are not already available in your environment.
2. Clone the repository and enter its directory:

   ```sh
   git clone https://github.com/ethereum/EIPs.git
   cd EIPs
   ```

3. Install the dependencies declared by the project:

   ```sh
   bundle install
   ```

4. Start a local Jekyll preview:

   ```sh
   bundle exec jekyll serve
   ```

   Jekyll reports the local address when the server starts. To generate the static site without starting the preview server, run:

   ```sh
   bundle exec jekyll build
   ```

The repository includes GitHub Actions workflows for continuous integration and Jekyll publishing. For the exact checks run by automation, consult the workflow files under `.github/workflows/` and the relevant configuration under `config/`.

## Usage

### Reading proposals

Open a proposal in `EIPS/` to read its content and front matter. For links between proposals, the repository’s guidance recommends relative Markdown links, for example:

```markdown
[EIP-1](./eip-1.md)
```

This keeps links usable in the repository and in rendered copies. Supporting files should be stored with the relevant proposal’s assets and linked using relative paths.

### Drafting a proposal

Before writing a formal draft, review EIP-1 and consider discussing the idea with the community. The repository’s issue guidance recommends using an issue for early feedback when a draft has not yet been written. If a draft is ready, submit it as a pull request using the template rather than opening an issue to submit the document.

Start from `eip-template.md`, fill in the required metadata and sections, and remove template instructions and placeholders before submitting. EIP-1 describes the expected content and metadata, including the proposal type, status, author, and—where applicable—category, discussion URL, dependencies, and last-call deadline. It also specifies conventions such as ISO 8601 dates and relative links to referenced EIPs.

When first submitting a draft, use an abbreviated title in the filename; an EIP number is assigned by an editor. Put supporting material in a proposal-specific directory under `assets/`. For detailed requirements and exceptions, follow EIP-1 rather than relying on older proposal examples, which may use different formats or reflect earlier guidance.

**ERC submissions:** The pull-request template states that ERC-related pull requests now occur in the [Ethereum ERCs repository](https://github.com/ethereum/ercs). The `EIPS/` directory contains some ERC-related documents, including files marked as moved; these should not be taken as instructions to submit new ERCs here.

## Configuration and site

Jekyll configuration is held in `_config.yml`, with page layouts and reusable includes in `_layouts/` and `_includes/`. The repository also contains category and status pages, an `all.html` page, RSS feeds, and static assets. The `assets/css/` files provide site styles.

Files under `config/` include settings for EIP validation, Markdown linting, spelling, links, and status data. These are project configuration files; edit them only when a change to the corresponding behavior or data is intended. The publishing and automation workflows are in `.github/workflows/`. The repository includes a `CNAME` file and a Jekyll publishing workflow, but deployment details should be verified in the workflow and site configuration before changing them.

## Development

Most contributions are edits to proposal Markdown, metadata, links, or supporting assets. Keep changes focused, follow EIP-1 and the template, and check that referenced local files exist. For a new proposal, preserve the template’s required sections and front matter conventions. For an update to an existing proposal, take its status and history into account; in particular, EIP-1 explains that Final proposals should generally receive only errata and non-normative clarifications.

The project provides GitHub issue and pull-request templates, contribution guidance, and code ownership information under `.github/`. Review those files before opening a contribution. The pull-request template also describes conditions under which a bot may automatically merge some changes; do not assume that every pull request is eligible.

## Testing and validation

The repository includes a CI workflow and configuration for EIP and Markdown-related checks. It also contains test vectors and other test resources alongside particular proposals. These resources are proposal-specific and do not constitute one universal test suite for all EIPs.

For local validation, build the site with Jekyll as described above and review the CI workflow and tool configuration to determine which checks apply to your change. The supplied files do not establish a single project-wide test command beyond the Jekyll build, so use the commands documented by the relevant workflow or tool rather than assuming that proposal-specific scripts apply to the entire repository. Check rendered pages for broken relative links, malformed front matter, and missing assets.

## License

The repository’s `LICENSE.md` applies the **Creative Commons CC0 1.0 Universal** dedication to the work, waiving copyright and related rights to the extent permitted by law. The EIP template specifies the corresponding copyright statement for proposal documents. Some individual documents identify separately licensed third-party implementations or materials; check those documents and their referenced files before reusing such material.
