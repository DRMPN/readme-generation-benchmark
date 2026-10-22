# devops-exercises-57yf07k3

A collection of hands-on DevOps exercises, paired solutions, and interview preparation material. The content covers Linux, scripting, version control, containers, orchestration, configuration management, infrastructure as code, CI/CD, cloud certifications, monitoring, and system design.

> **Note:** The repository was provided as a flat file listing without directory paths. The structure described below is inferred from file names. Check the actual folder layout after cloning for exact locations.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Topics Covered](#topics-covered)
- [How the Exercises Are Organized](#how-the-exercises-are-organized)
- [Python Tools and Utilities](#python-tools-and-utilities)
- [Shell Scripts](#shell-scripts)
- [Sample Applications](#sample-applications)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Suggested Learning Paths](#suggested-learning-paths)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [Known Issues](#known-issues)
- [License](#license)

## Overview

This repository is a practice resource for engineers preparing for DevOps, SRE, cloud, and platform roles, or for anyone who wants to build practical skills with common tools. Most topics follow a consistent pattern:

1. An **exercise** describes a task and its goals.
2. A **solution** shows one way to complete it, with explanation.

Some topics also include a `README.md` with an overview, supporting diagrams (`.png`), or configuration files such as Terraform (`main.tf`, `versions.tf`, `vars.tf`) or Ansible playbooks (`deploy.yml`, `helloworld.yml`).

## Repository Structure

The repository is organized by subject. Each subject folder typically contains some combination of:

| File type | Purpose |
|---|---|
| `README.md` | Overview of the topic or module |
| `exercise.md` | Task description and requirements |
| `solution.md` / `*_solution.md` | Worked solution with explanation |
| `*.md` (topic files) | Lessons, question sets, or walkthroughs |
| `*.tf`, `*.yml`, `Jenkinsfile`, `*.groovy` | Infrastructure, configuration, or pipeline code used by exercises |
| `*.py`, `*.sh` | Scripts and utilities |
| `*.png`, `*.jpeg` | Diagrams and images referenced by the documentation |

Some folders contain several exercises at once, numbered for sequencing, for example `pods_01.md`, `replicaset_01.md`, `replicaset_02.md`, and `replicaset_03.md`.

### Top-level files

| File | Description |
|---|---|
| `README.md` | Main project readme |
| `LICENSE` | Project license |
| `CONTRIBUTING.md` | Contribution guidelines |
| `credits.md` | Acknowledgments for contributors and sources |
| `faq.md` | Frequently asked questions |
| `prepare_for_interview.md` | Interview preparation guidance |
| `devops_exercises.png`, `devops.png`, and similar | Visual assets used in documentation |

## Topics Covered

### Operating Systems and Linux
- Basic and advanced Linux commands
- Hardware, OS, storage, and virtualization concepts
- Linux master-level material

### Scripting and Programming
- **Bash:** argument checking, character counting, file size comparison, directory comparison, empty file detection, factorial/factor calculations, sum and print utilities
- **Python:** data types, string manipulation (for example, `compress_string`, `reverse_string`), sorting (`merge_sort.py`, `binary_search.py`), and advanced data types
- **Go, Node.js, Perl:** introductory material and questions

### Version Control with Git
- Basic and advanced Git operations
- Branching (`branch_01.md`), commits (`commit_01.md`), and squashing commits
- Forking workflows (`fork_101.md`, `fork_102.md`)
- Git filesystem monitor (`git_fsmonitor.png`)

### Containers and Docker
- Writing Containerfiles and running containers
- Working with images, committing images, and image layers
- Multi-stage builds
- Running containers and persistent storage
- Containerized databases and web servers
- Sharing images

### Orchestration with Kubernetes
- Pods, ReplicaSets, Deployments, and Services
- Killing and recovering containers
- Services and cluster architecture
- Certification prep: CKA and CKAD

### Configuration Management
- **Ansible:** playbooks, tasks, inventories, system updates and upgrades, and host status checks
- **Puppet:** introductory material

### Infrastructure as Code
- **Terraform:** `main.tf`, `versions.tf`, and `vars.tf` configurations with exercises and solutions

### CI/CD and Pipelines
- **Jenkins:** pipelines, Jenkinsfile examples, job and build cleanup scripts (Groovy), Jenkins scripts, and deploying to Kubernetes
- **CircleCI** and general CI/CD concepts
- CI for open-source projects

### Cloud
- **AWS:** S3 event triggers with Lambda, Lambda direct access, and certification paths (Cloud Practitioner, Solutions Architect Associate, SysOps Associate)
- **Azure:** AZ-900 fundamentals
- **Google Cloud:** introductory material

### Monitoring and Observability
- **ELK stack:** Elasticsearch, Logstash, and Kibana, including AWS deployments and query improvement
- **Prometheus, Grafana, and Datadog**
- Observability and chaos engineering concepts

### Databases and Data
- SQL and MongoDB concepts
- Big data basics
- Kafka

### Networking and Security
- DNS, load balancers, CDN, and networking fundamentals
- Certificates and security basics
- Regex practice

### System Design and Reliability
- Distributed systems design
- Producer/consumer patterns
- Standby and load-balanced designs
- SRE checklist
- High-availability "hello world" examples

### Certifications
- **Kubernetes:** CKA, CKAD
- **AWS:** Cloud Practitioner, Solutions Architect Associate, SysOps Associate, and certification path guides
- **Azure:** AZ-900

## How the Exercises Are Organized

The typical workflow for a topic is:

1. Read the topic's `README.md` for context.
2. Open `exercise.md` and attempt the task without looking at the solution.
3. Compare your approach with `solution.md` (or `*_solution.md`).
4. Work through numbered exercises in order when present, such as `replicaset_01` through `replicaset_03`.

Question-based topics, such as `node_questions_basic.md` with `node_questions_basic_ans.md`, follow a question-and-answer format instead.

## Python Tools and Utilities

Several Python files support quiz-style practice and maintenance of the question sets.

| File | Purpose |
|---|---|
| `random_question.py` | Selects and prints a random interview question |
| `question_utils.py` | Shared helper functions for question handling |
| `update_question_number.py` | Renumbers questions in question files |
| `syntax_lint.py` | Checks question or solution files for syntax problems |
| `syntax_checker_unittest.py` | Unit tests for `syntax_lint.py` |
| `scripts_question_utils_unittest.py` | Unit tests for `question_utils.py` |
| `requirements.txt` | Python dependencies for the utilities |

### Example usage

```bash
# Install dependencies
pip install -r requirements.txt

# Print a random question
python random_question.py

# Lint question files for syntax problems
python syntax_lint.py

# Run the unit tests
python -m unittest syntax_checker_unittest.py
python -m unittest scripts_question_utils_unittest.py
```

> Adjust the commands above to match the scripts' actual argument handling. Run `python <script>.py --help` or read the script header if the options differ.

## Shell Scripts

| Script | Purpose |
|---|---|
| `run_ci.sh` | Runs the repository's CI checks locally |
| `count_questions.sh` | Counts questions across the repository |
| `aws_s3_event_trigger.sh` | Sets up an S3 bucket event trigger for a Lambda function |

### Example usage

```bash
chmod +x run_ci.sh count_questions.sh aws_s3_event_trigger.sh

./run_ci.sh
./count_questions.sh
```

The S3 trigger script creates AWS resources and needs configured credentials. Review it before running.

## Sample Applications

Some folders contain small applications used as exercise targets.

### Python web app
- `main.py`: application entry point
- `config.py`: configuration settings
- `tests.py`: test suite
- `__init__.py`: package marker
- `requirements.txt`: dependencies
- `README.md`: setup instructions

Typical run:

```bash
pip install -r requirements.txt
python main.py
python -m unittest tests.py
```

### Python package
- `__main__.py` (appears in several exercise folders): allows the package to run with `python -m <package>`

### Static website
- `index.html`, `skeleton.css`, `normalize.css`, `favicon.png`: a simple static site, useful for web server and container exercises

### Ansible and Jenkins examples
- `helloworld.yml`, `deploy.yml`, and `inventory`: Ansible playbook, deployment, and inventory examples
- `Jenkinsfile`: sample declarative pipeline

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/devops-exercises-57yf07k3.git
cd devops-exercises-57yf07k3
```

### 2. Choose a topic

Browse the folders, or start with one of the suggested learning paths below.

### 3. Set up the tools you need

Each topic may require different software. Common tools include:

- Git
- Docker or Podman
- kubectl and a local cluster (kind, minikube, or k3d)
- Terraform
- Ansible
- Jenkins
- Python 3.8+
- AWS CLI, Azure CLI, or gcloud

### 4. Work through an exercise

1. Open `exercise.md`.
2. Complete the task in a scratch directory or sandbox account.
3. Check your work against `solution.md`.

## Prerequisites

Requirements vary by topic. A general baseline:

- A Linux, macOS, or WSL environment
- Basic command-line familiarity
- Python 3 for the utilities and sample apps
- Accounts for cloud exercises (AWS, Azure, or Google Cloud). Use free tiers where possible and clean up resources afterward to avoid charges.

## Suggested Learning Paths

**Beginner DevOps**
1. Linux basics
2. Bash scripting
3. Git fundamentals
4. Docker and containers
5. Python basics

**Container and orchestration**
1. Docker: images, containers, layers, multi-stage builds
2. Docker: persistent storage and containerized databases
3. Kubernetes: Pods, ReplicaSets, Deployments, Services
4. CKA or CKAD preparation

**Automation and infrastructure**
1. Ansible playbooks and inventories
2. Terraform basics
3. Jenkins pipelines
4. AWS Lambda and S3 triggers

**Observability and reliability**
1. Linux and networking fundamentals
2. ELK stack or Prometheus/Grafana
3. SRE checklist and system design material

**Interview preparation**
1. `prepare_for_interview.md`
2. Random question practice with `random_question.py`
3. Topic-specific question sets

## Running Tests

Unit tests are included for the Python utilities:

```bash
python -m unittest syntax_checker_unittest.py
python -m unittest scripts_question_utils_unittest.py
```

To run the full CI check locally:

```bash
./run_ci.sh
```

## Contributing

Contributions are welcome. Please read `CONTRIBUTING.md` first. In general:

1. Fork the repository.
2. Create a branch for your change: `git checkout -b feature/your-change`.
3. Keep exercises and solutions paired, and use the existing naming conventions.
4. Run the linter and tests before opening a pull request.
5. Open a pull request with a clear description of what changed and why.

Good contribution areas include:
- Fixing typos in file names and content
- Adding exercises for underrepresented topics
- Improving solutions with clearer explanations
- Updating outdated tool versions or cloud console steps
- Adding diagrams or example output

## Known Issues

- Some file names contain typos, such as `soltuion.md` (should be `solution.md`) and `eflk.md` (likely `elk.md`). Renaming these requires updating any links that point to them.
- Several files share the same name across folders, such as `exercise.md` and `solution.md`. Always reference them by their full path.
- Duplicate or near-duplicate files exist in a few places, such as `reverse_string.md` appearing twice and `ha_hello_world.md` and `containerize_app.md` appearing in more than one folder. Review these before editing.
- Cloud exercises can incur costs. Always check the cleanup steps.

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.

## Acknowledgments

Thanks to all contributors. See [credits.md](credits.md) for attribution to the tools, courses, and resources that inspired individual exercises.
