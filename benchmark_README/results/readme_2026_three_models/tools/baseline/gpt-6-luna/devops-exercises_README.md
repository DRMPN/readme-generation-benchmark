# DevOps Exercises

A community learning repository for exploring DevOps concepts, practicing technical questions, and working through hands-on exercises. Materials cover subjects including Linux, cloud platforms, containers, Kubernetes, CI/CD, infrastructure as code, programming, databases, networking, security, observability, and system design.

This repository is intended for learning and practice—not as a prediction of what a particular interview will ask. Many questions are deliberately unanswered, so researching a topic and discussing it with others are part of the exercise. See the [FAQ](faq.md) for the project’s learning goals and interview guidance, and [How to prepare for interviews](prepare_for_interview.md) for suggestions on skills and practice.

## Repository guide

Most content is organized by topic under `topics/`. Start with the relevant topic’s `README.md` where one exists; it commonly provides a contents list, self-assessment questions, or links to exercises and solutions.

| Area | Examples |
|---|---|
| Cloud platforms | [AWS](topics/aws/README.md), [Azure](topics/azure/README.md), and GCP materials |
| Containers and orchestration | Containers, [Kubernetes](topics/kubernetes/README.md), OpenShift, Argo CD, and Argo Rollouts |
| Automation and delivery | [Ansible](topics/ansible/README.md), [CI/CD](topics/cicd/README.md), Jenkins, CircleCI, Terraform, and Zuul |
| Operations and architecture | Linux, networking, DNS, databases, distributed systems, observability, SRE, and chaos engineering |
| Programming and data | Python, SQL, Node.js, shell, Perl, and programming exercises |
| Professional preparation | Soft skills, interview questions, and [certification study notes](certificates/) |

Hands-on activities are often stored as Markdown files with a corresponding solution in a `solutions/` directory. For example, the Ansible topic links exercises and solutions, and the AWS topic groups practice by services such as IAM, EC2, S3, VPC, databases, and Lambda. Some topic directories contain code or configuration examples alongside the written exercises.

The `certificates/` directory contains study notes and question-and-answer material for AWS, Azure AZ-900, CKA, and CKAD topics. `coding/python/` contains Python algorithm examples, including binary search and merge sort. `exercises/shell/` includes a shell exercise solution. Images used throughout the learning materials are kept under `images/`.

## Using the materials

No single application or build step is required to read the primary learning content: most of it is Markdown. Open a topic file in a Markdown viewer, or browse the files directly in a repository browser.

A practical way to study is to:

1. Choose a subject and open its topic guide, if available.
2. Try to answer the self-assessment questions before reading any answers.
3. Work through exercises in their exercise files, then compare your work with a provided solution where one exists.
4. Research unanswered questions using relevant documentation and learning resources.
5. Practice by adapting exercises or explaining your reasoning to someone else.

Question and answer sections commonly use collapsible Markdown `<details>` blocks. Expand them in a renderer that supports this format. Answers are not included for every question, and the presence of an exercise does not guarantee that a solution is available. For interview preparation, treat the repository as one learning resource rather than a guide to a guaranteed interview format.

Some activities involve real cloud resources. The AWS topic explicitly warns that some exercises cost money and may not be covered by the free tier. Review the exercise and provider pricing before creating resources, and remove resources when finished. AWS solutions are described as using the console, while the topic recommends considering infrastructure-as-code tools such as Terraform or Pulumi.

## Setup

For reading and editing the Markdown, obtain a local checkout or browse the repository online. The supplied files do not specify a single repository URL or a general installation procedure, and the repository is not presented as one application that must be installed.

Requirements depend on the specific example you choose to run. For instance, the two Flask example directories each include a `requirements.txt` listing Flask, while the S3 event-triggering Lambda example pins `boto3` to version `1.17.95`. Other exercises may involve tools or cloud accounts specific to their subject; check the relevant exercise instructions before proceeding. Do not assume that one requirements file applies to the entire repository.

## Configuration and resources

There is no general project-wide configuration file or environment-variable contract documented in the supplied files. Configure tools, credentials, and cloud resources according to the instructions for the specific exercise you are using.

Cloud exercises may create billable resources or require provider access. In particular, the AWS materials call out potential costs and suggest infrastructure as code as an alternative approach to completing console-based examples. Treat any credentials and resource settings as local to your practice environment, and review an exercise before running its commands or code.

The repository also contains CI configuration files (`.github/workflows/ci_workflow.yml` and `.travis.yml`). These describe automation associated with the repository; they do not establish a general configuration interface for running the learning examples.

## Development and contributions

Contributions are welcome through pull requests. Follow the question-and-answer format used in `CONTRIBUTING.md`:

```html
<details>
<summary>[Question]</summary><br><b>

[Answer]
</b></details>
```

Before submitting, check that your question or exercise fits the learning purpose of the project. The contribution guide advises against installation questions and copying questions or answers from other sources. If you add images, make sure they are free to use. The [credits file](credits.md) records attribution and licensing information for a number of images and logos.

When adding questions, the repository’s `scripts/count_questions.sh` can help count them. To review changes locally before submitting a pull request, the contribution guide recommends the CI script described below.

## Testing

The repository includes tests under `tests/`, including unit-test files for question utilities and syntax checking, a syntax-lint script, and Markdown test cases. A local CI helper is provided at `scripts/run_ci.sh`; the contribution guide recommends using it to test changes before submitting a pull request.

From the repository root, run the helper with Bash:

```sh
bash scripts/run_ci.sh
```

For question-counting support, the script is located at `scripts/count_questions.sh`:

```sh
bash scripts/count_questions.sh
```

The repository also contains utility scripts for random-question handling and updating question numbers. Their command-line options and detailed usage are not specified here; inspect the individual scripts before using them.

## License

The supplied `LICENSE` file sets out the terms for use of the work. It grants rights to reproduce, distribute, and publicly perform the work subject to its conditions. Among other restrictions, it requires retaining license and attribution notices, limits use directed toward commercial advantage or private monetary compensation, and does not grant general rights to create adaptations (apart from technically necessary format changes). Read the complete `LICENSE` file before reusing or distributing material.

Image and logo credits are recorded separately in [`credits.md`](credits.md). Check that file and any applicable notices when reusing individual assets.
