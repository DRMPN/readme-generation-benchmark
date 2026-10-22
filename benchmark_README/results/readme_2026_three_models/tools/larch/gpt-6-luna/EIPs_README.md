# EIPs

This repository contains Ethereum Improvement Proposals (EIPs), their supporting materials, and the website files used to publish and browse them. It is a documentation repository—not primarily a Python project. The Python, Go, Solidity, Yul, and other source files included here are supporting examples, tests, or research artifacts associated with particular proposals.

## What is an EIP?

An Ethereum Improvement Proposal describes a proposed change or standard for Ethereum. EIPs cover topics such as:

- Core protocol and execution-layer changes
- Networking and node behavior
- Application interfaces and token standards
- Wallet and user-facing conventions
- Informational guidance and process changes

A proposal is not automatically accepted because it is present in the repository. Its status and progress are tracked through its document metadata and the EIP review process.

## Repository contents

The repository is organized largely as a collection of files at the top level.

| Files | Purpose |
|---|---|
| `eip-<number>.md` | The proposal documents. Each file contains an EIP’s metadata and specification. |
| `eip-template.md`, `template-eip.md` | Templates and examples for preparing proposal documents. |
| `README.md` | Repository overview and contributor guidance. |
| `eip.html`, `erc.html`, `core.html`, `networking.html`, `informational.html` | Website pages for browsing proposal categories. |
| `all.html`, `erc.html`, `eip.html`, `authorlist.html`, `eiptable.html`, `eipnums.html`, `toc.html` | Website views and supporting pages for listing or navigating proposals. |
| `all.xml`, `erc.xml`, `nonerc.xml` and their `*-last-call.xml` variants | Proposal feeds and related listings. |
| `statuses.yaml`, `eip-editors.yml`, `authorlist.html` | Repository and site metadata used to organize proposals and contributors. |
| `_config.yml`, `Gemfile`, `Gemfile.lock`, `eipw.toml`, `mlc_config.json` | Site, dependency, and tooling configuration. |
| `header.html`, `head.html`, `meta.html`, `social.html`, `anchor_headings.html`, `404.html`, `style.scss`, `override.css` | Website layout, styling, metadata, and supporting pages. |
| Images, diagrams, PDFs, data files, patches, and source files | Proposal-specific illustrations, research, examples, test vectors, and implementation material. |

Many supporting files sit alongside the EIP they relate to rather than in a separate source directory. For example, a proposal may include test vectors, scripts, diagrams, or implementation examples in addition to its Markdown document.

## Reading a proposal

Open the relevant `eip-<number>.md` file. EIP documents generally include metadata such as the proposal’s title, author, status, type, and discussion or implementation links, followed by sections describing the proposal.

The metadata is important: it allows repository tooling and the website to identify and display the document correctly. When editing an existing proposal, preserve its established metadata and structure unless the change specifically requires updating them.

## Contributing

Contributions may include proposing a new EIP, improving an existing proposal, correcting supporting material, or helping review a change.

### Proposing a new EIP

1. Read the EIP process documentation and the relevant proposal template.
2. Choose an available proposal number according to the process used by the repository.
3. Create an `eip-<number>.md` document using the template.
4. Complete the required metadata and proposal sections. Include references, rationale, security considerations, and other relevant material where appropriate.
5. Add any supporting examples, diagrams, or test vectors needed to understand or validate the proposal.
6. Submit the change for review and respond to feedback.

A proposal should clearly explain the problem it addresses, the proposed solution, its compatibility implications, and any risks or trade-offs. Avoid presenting an unreviewed proposal as accepted or final.

### Editing an existing EIP

- Keep the proposal’s scope and existing metadata in mind.
- Make status, authorship, and other metadata changes only when they reflect the proposal’s actual state.
- Keep code examples, test vectors, and diagrams consistent with the written specification.
- Use clear, reviewable changes and explain substantive edits in the pull request.

### Supporting files

Keep supporting material associated with the proposal it documents. When adding scripts, test vectors, or other artifacts, provide enough context for reviewers to understand their purpose and how they relate to the proposal. Do not assume that every artifact in the repository is part of the website build.

## Local development

The website is configured with Jekyll. A Ruby installation and Bundler are therefore needed to install its site dependencies and preview or build the site.

```sh
bundle install
bundle exec jekyll serve
```

Jekyll will report a local address for viewing the site. To build the site without starting the preview server, run:

```sh
bundle exec jekyll build
```

If a command fails, check the Ruby and Bundler versions available in your environment, the dependencies recorded in `Gemfile.lock`, and the site settings in `_config.yml`.

This repository also includes `eipw.toml` and `mlc_config.json` for proposal-related tooling. Consult those files and the current contribution guidance before running or configuring additional validators. The listed Python and other source files may have their own requirements; there is no single project-wide Python test command implied by their presence.

## Review and validation

Before submitting a change:

- Check Markdown formatting and proposal metadata.
- Verify that links, references, and images resolve.
- Review any changed code examples or test vectors for consistency with the specification.
- Preview the website when your change affects rendered content or site navigation.
- Explain what changed and why in the pull request.

The EIP process and repository tooling may evolve. Follow the current process documentation and reviewer guidance for requirements that are not captured by this overview.
