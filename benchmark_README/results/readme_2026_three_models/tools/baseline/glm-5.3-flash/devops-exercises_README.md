# DevOps Exercises

This repository is a collection of DevOps-related questions, exercises, solutions, and learning resources designed to help you learn and practice concepts across the DevOps ecosystem. It covers topics ranging from operating systems, networking, and scripting, through cloud providers, containers, and CI/CD, all the way to certificates preparation and system design.

Whether you are preparing for a DevOps/SRE/Production Engineer interview, studying for a cloud certification, or simply trying to deepen your understanding of DevOps practices, this repository provides hands-on exercises and self-assessment questions you can work through at your own pace.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Topics Covered](#topics-covered)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [FAQ](#faq)
- [Credits](#credits)
- [License](#license)

## Overview

The main purpose of this repository is **learning**. It is built around two primary types of content:

1. **Questions** — self-assessment questions written in a consistent `<details>/<summary>` format across topic pages, allowing you to attempt an answer before revealing the reference answer.
2. **Exercises** — hands-on tasks (with separate solution files) that you can perform in real environments such as AWS, GCP, Kubernetes clusters, or your local shell.

The repository also includes a guide on [how to prepare for DevOps/SRE/Production Engineer interviews](prepare_for_interview.md), covering recommended skills (Linux, programming, architecture and design, tooling), practical preparation scenarios, sample questions, and advice on building your own projects.

## Repository Structure

```
.
├── certificates/          # Certification preparation notes (AWS, Azure, CKA, CKAD)
├── coding/                # Coding exercises (e.g. Python binary search, merge sort)
├── exercises/             # Standalone exercises (e.g. shell scripting challenges)
├── images/                # Topic logos, diagrams, and exercise illustrations
├── prepare_for_interview.md  # Interview preparation guide
├── scripts/               # Helper scripts for contributors and users
├── tests/                 # Test suite for repository scripts and syntax
├── topics/                # The main content: questions & exercises per topic
│   ├── ansible/           # Ansible playbooks/tasks exercises + solutions
│   ├── argo/              # Argo CD exercises (app creation, rollouts, secrets)
│   ├── aws/               # AWS exercises (EC2, S3, VPC, IAM, Lambda, ...)
│   ├── azure/             # Azure questions (compute, network, storage, security)
│   ├── cicd/              # CI/CD exercises incl. Jenkins pipelines & solutions
│   ├── containers/        # Container exercises (Docker) + solutions
│   ├── flask_container_ci/    # Sample Flask app used for CI/CD exercises
│   ├── flask_container_ci2/   # Second sample Flask app for CI/CD practice
│   ├── gcp/               # GCP exercises with Terraform code
│   ├── git/               # Git exercises (branches, commits, squashing)
│   ├── kubernetes/        # Kubernetes exercises (pods, replicasets, services, ...)
│   ├── linux/             # Linux exercises (navigation, copy, unique count, ...)
│   ├── shell/             # Shell scripting exercises + solutions
│   ├── terraform/         # Terraform exercises (EC2, S3, local providers, ...)
│   └── ...                # Many more: CI/CD, chaos engineering, databases,
│                          # DNS, Grafana, Kafka, observability, OpenShift,
│                          # Perl, programming, Python, security, SRE, SQL, Zuul
└── faq.md                 # Frequently asked questions about the project
```

## Topics Covered

The `topics/` directory is organized by technology. Each topic directory typically contains a `README.md` with questions and, where applicable, exercise files (often with matching `solutions/` directories). Topics include:

- **Cloud providers:** AWS, Azure, GCP, OpenStack
- **Containers & orchestration:** Containers (Docker), Kubernetes, OpenShift, Argo
- **CI/CD & automation:** CI/CD, Jenkins pipelines and scripts, CircleCI, Zuul, Ansible, Puppet
- **Infrastructure as Code:** Terraform (with exercise directories containing `.tf` files and Pulumi Python examples for AWS resources such as VPCs, subnets, and S3 buckets)
- **Operating systems & shell:** Linux, Shell scripting, OS (fork exercises)
- **Programming:** Python (data types, string manipulation, classes), Perl, Node.js, general programming exercises (grep, web scraping)
- **Observability & monitoring:** Observability, Grafana, Datadog, ELK/Kibana (including running Kibana on AWS)
- **Data & streaming:** Databases, SQL (query improvement exercises), Kafka, MongoDB, big data
- **Networking & other areas:** DNS, Security, Chaos Engineering, SRE, Soft Skills, Software Development, Hardware, Virtualization, Storage, Distributed systems, Git

## Getting Started

No special installation is required to use the repository — it is primarily a collection of Markdown documents. Simply:

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Browse the topics that interest you in `topics/`, or start with the interview preparation guide in `prepare_for_interview.md`.

Some exercises and helper scripts use Python and shell scripting. To work with the sample Flask applications used in CI/CD exercises, you will need Python with Flask. For example:

```bash
cd topics/flask_container_ci
pip install -r requirements.txt
```

The sample app exposes JSON endpoints (`/`, `/users`, `/users/<username>`) on port 5000 and can be run with:

```bash
python app/main.py
```

A second sample app (`topics/flask_container_ci2`) provides matrix-related endpoints (`/matrix/...`, `/rows/...`, `/columns/...`) that are intentionally left as TODOs for you to implement as an exercise.

## Usage

### Working Through Questions

Each topic's `README.md` contains questions wrapped in collapsible sections. Try to answer each question yourself before expanding the answer. Some questions intentionally repeat concepts from different angles — this is done to reinforce understanding.

### Hands-On Exercises

Exercise files follow a consistent pattern:

- `exercise.md` (or a topic-specific exercise file) — describes the objective and task.
- A matching file under `solutions/` — contains one possible solution.

For example, under `topics/aws/exercises/` you will find dozens of exercises covering EC2 instance launching, AMI creation, EBS volumes, S3 buckets, IAM roles and users, VPCs and subnets, load balancers, Auto Scaling groups, Lambda functions, Route 53, ElastiCache, and more — each with Terraform and/or Pulumi reference code where relevant.

### Helper Scripts

The `scripts/` directory includes utilities for working with the repository:

- **`count_questions.sh`** — counts the number of questions in the repository. Useful if you've added several questions and want to know the new total.
- **`random_question.py`** — helps you practice by surfacing questions randomly.
- **`question_utils.py`** — shared utilities used by the question-related scripts and tests.
- **`run_ci.sh`** — run the repository's checks locally before submitting a pull request (see [Contributing](#contributing)).
- **`update_question_number.py`** — updates the question count used in the project.

### AWS S3 Event Triggering Example

Under `scripts/aws s3 event triggering/` there is a complete working example of triggering processing on new S3 objects:

- `aws_s3_event_trigger.sh` — a shell script for setting up the S3 event trigger.
- `s3-lambda/` — a Python Lambda function (`s3-lambda.py`) with its dependencies defined in `requirements.txt` (`boto3==1.17.95`).
- `README.md` and `sample.png` — documentation for the example.

### Certification Preparation

The `certificates/` directory contains study notes for cloud and Kubernetes certifications, including:

- **AWS:** Cloud Practitioner, Solutions Architect Associate, Cloud SysOps Associate, plus an overview of AWS certification paths by role
- **Azure:** AZ-900 Fundamentals
- **Kubernetes:** CKA and CKAD

Each certification file summarizes key exam concepts in question format, such as EC2 pricing models, security groups, VPCs, placement groups, launch templates, and hibernation for AWS.

## Configuration

The repository is configuration-free by design — content is consumed directly from the Markdown files. If you plan to run or extend parts of the project:

- Python scripts in `scripts/` require a Python interpreter; the Lambda example pins its AWS SDK dependency via `requirements.txt`.
- The sample Flask apps require the `flask` package (listed in their `requirements.txt`); CSRF protection is enabled via `flask_wtf` (`CSRFProtect`).
- CI configuration is defined in `.github/workflows/ci_workflow.yml` (GitHub Actions) and `.travis.yml` (legacy Travis CI configuration).

## Development

When contributing new questions or exercises:

- Follow the established format (see [Contributing](#contributing)).
- Place new topic content under the appropriate `topics/<topic>/` directory, using `solutions/` subdirectories for answers.
- Keep images free-to-use and properly attributed (see `credits.md`).
- Ensure your changes pass the repository's checks locally using `scripts/run_ci.sh`.

The repository's CI (`.github/workflows/ci_workflow.yml`) runs these checks automatically on pull requests.

## Testing

The `tests/` directory contains the project's test suite:

- **`tests/scripts_question_utils_unittest.py`** — unit tests for the question utilities used by the helper scripts.
- **`tests/syntax_checker_unittest.py`** — tests for the syntax checker.
- **`tests/syntax_lint.py`** — a linter validating the Markdown question format.
- **`tests/testcases/`** — sample Markdown test cases used by the syntax checks.

To validate your changes before submitting a pull request, run the provided script from the repository root:

```bash
./scripts/run_ci.sh
```

This runs the same validation performed in CI, including syntax checks of the question format.

## Contributing

Contributions are welcome via pull requests. To keep the repository consistent, please:

1. **Follow the question format:**

```
<details>
<summary>[Question]</summary><br><b>

[Answer]
</b></details>
```

2. **Avoid:**
   - Installation questions (e.g. "how to install X?") — they carry little educational value.
   - Copying questions and answers from other sources — original content only.
   - Adding images that are not free to use.

3. **Before submitting:**
   - Test your changes locally with `scripts/run_ci.sh`.
   - If you added several questions, you can use `scripts/count_questions.sh` to verify the question count.

More details and discussion guidelines are available in `CONTRIBUTING.md` and `faq.md`.

## FAQ

A full FAQ is available in [faq.md](faq.md). Highlights:

- **What is the purpose of the repository?** Learning.
- **Should I use it for interview preparation?** It can help you learn concepts, but don't assume your interview will contain the same questions. See `prepare_for_interview.md` for suggestions.
- **Why do many questions lack answers?** More contributors are needed, and often asking questions is easier than answering them. You are encouraged to research answers independently — that's part of being a DevOps engineer.
- **Can I copy questions to my own site?** Only with attribution and only for non-commercial use.
- **Why do some questions repeat?** Identical questions are a bug; similar questions asked from different angles are intentional to reinforce concepts.

## Credits

The logos and icons used throughout the repository are the work of various designers and are attributed in [credits.md](credits.md), including:

- Jenkins logo by Ksenia Nenasheva (jenkins.io), CC BY-SA 3.0
- Git logo by Jason Long, CC BY 3.0
- Logos from Hashicorp (Terraform), Docker, Python Software Foundation, Puppet, OpenStack Foundation, The Linux Foundation (Linux, Kubernetes, Prometheus), MongoDB, Google, and others
- Various icons from Iconfinder, Flaticon, and independent designers

## License

This project's content is made available under a Creative Commons public license (see [LICENSE](LICENSE)). Key terms of the license as provided in the repository:

- **Attribution required** — you must credit the original authors when distributing or publicly performing the work.
- **Non-commercial use** — the work may not be used primarily for commercial advantage or private monetary compensation.
- **No adaptations** — you may reproduce and distribute the work, but you do not have the right to create adaptations (derivative works), beyond modifications technically necessary to exercise the rights in other media.
- The work is provided **as-is**, with no warranties, and the licensor's liability is limited as described in the license text.

Please read the full [LICENSE](LICENSE) file before redistributing or reusing any part of this repository.
