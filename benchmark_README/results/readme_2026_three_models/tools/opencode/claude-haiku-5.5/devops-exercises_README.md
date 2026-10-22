# DevOps Exercises

A collection of DevOps, SRE, cloud, and related interview-style questions and hands-on exercises, organized by topic. Questions are written with their answers in collapsible sections, and many topics include exercises with step-by-step solutions.

The repository's stated purpose, per [faq.md](faq.md), is learning. It is not a guarantee that any interview will include similar questions.

## Contents

- [What's in the repository](#whats-in-the-repository)
- [Topics](#topics)
- [Exercises](#exercises)
- [Hands-on projects](#hands-on-projects)
- [Certification guides](#certification-guides)
- [Scripts](#scripts)
- [Tests and CI](#tests-and-ci)
- [Contributing](#contributing)
- [Further reading](#further-reading)
- [License and credits](#license-and-credits)

## What's in the repository

```
.
├── topics/          # Questions, exercises, and solutions, one directory per topic
├── certificates/    # Notes for certification preparation (AWS, Azure, CKA, CKAD)
├── coding/python/   # Standalone Python examples (binary search, merge sort)
├── exercises/       # Additional exercise solutions (shell)
├── scripts/         # Helper scripts for counting and quizzing questions, and CI
├── tests/           # Unit tests and the Markdown syntax linter
├── images/          # Logos and diagrams used by the topic documents
├── faq.md           # Frequently asked questions about the project
├── prepare_for_interview.md  # Opinionated notes on interview preparation
├── CONTRIBUTING.md  # How to contribute
├── credits.md       # Attribution for logos and images
└── LICENSE          # Creative Commons license terms
```

Each question is a collapsible block in Markdown. The question is the `<summary>` and the answer is inside the block. Some questions have no answer yet.

## Topics

Most topics live under `topics/` and have a `README.md` that lists its questions and, where available, its exercises. Topics with a dedicated README include:

| Area | Location |
|------|----------|
| Linux | [topics/linux](topics/linux/README.md) |
| Shell scripting | [topics/shell](topics/shell/README.md) |
| Git | [topics/git](topics/git/README.md) |
| Containers | [topics/containers](topics/containers/README.md) |
| Kubernetes | [topics/kubernetes](topics/kubernetes/README.md) |
| OpenShift | [topics/openshift](topics/openshift/README.md) |
| Helm and Kustomize | Within [topics/kubernetes](topics/kubernetes/README.md) |
| Argo (Argo CD and Rollouts) | [topics/argo](topics/argo/README.md) |
| CI/CD | [topics/cicd](topics/cicd/README.md) |
| CircleCI | [topics/circleci](topics/circleci/README.md) |
| Jenkins | [topics/jenkins_pipelines.md](topics/jenkins_pipelines.md), [topics/jenkins_scripts.md](topics/jenkins_scripts.md) |
| Zuul | [topics/zuul](topics/zuul/README.md) |
| Ansible | [topics/ansible](topics/ansible/README.md) |
| Terraform | [topics/terraform](topics/terraform/README.md) |
| AWS | [topics/aws](topics/aws/README.md) |
| Azure | [topics/azure](topics/azure/README.md) |
| Google Cloud | [topics/gcp](topics/gcp/README.md) |
| Cloud (general) | [topics/cloud](topics/cloud/README.md) |
| Databases | [topics/databases](topics/databases/README.md) |
| SQL | [topics/sql](topics/sql/improve_query.md) |
| Kafka | [topics/kafka](topics/kafka/README.md) |
| DNS | [topics/dns](topics/dns/README.md) |
| Security | [topics/security](topics/security/README.md) |
| Observability | [topics/observability](topics/observability/README.md) |
| Grafana | [topics/grafana](topics/grafana/README.md) |
| Datadog | [topics/datadog](topics/datadog/README.md) |
| Chaos engineering | [topics/chaos_engineering](topics/chaos_engineering/README.md) |
| SRE | [topics/sre](topics/sre/README.md) |
| DevOps (general) | [topics/devops](topics/devops/README.md) |
| Software development | [topics/software_development](topics/software_development/README.md) |
| Programming and algorithms | [topics/python](topics/python/), [topics/node](topics/node/), [topics/perl](topics/perl/), [topics/programming](topics/programming/) |
| Operating systems | [topics/os](topics/os/fork_101.md) |
| Soft skills | [topics/soft_skills](topics/soft_skills/README.md) |

Some topics are single documents rather than directories with a README, such as `topics/eflk.md` and `topics/misc/elk_kibana_aws.md`.

## Exercises

Exercises ask you to do something (for example, create a resource or write a script). Each exercise is paired with a solution. Exercises are typically tracked in a table with columns for the exercise, the solution, and comments.

Exercise groups include:

- **AWS** (`topics/aws/exercises/`): IAM, EC2, S3, ELB, Auto Scaling, VPC, databases, DNS, containers, Lambda, Elastic Beanstalk, CodePipeline, CDK, and miscellaneous tasks. Several exercises include Terraform or Pulumi examples under the same directory. The solutions use the AWS console; the topic README notes that infrastructure-as-code tools are recommended for these exercises.
- **Google Cloud** (`topics/gcp/exercises/`): project creation, IAM role assignment, and instance creation, with Terraform files.
- **Kubernetes** (`topics/kubernetes/`): pods, services, ReplicaSets, labels and selectors, node selectors, taints, and Kustomize. CKA-style tasks are in [topics/kubernetes/CKA.md](topics/kubernetes/CKA.md).
- **Argo** (`topics/argo/exercises/`): creating and syncing applications, secrets, Helm apps, and blue/green and canary rollouts.
- **Terraform** (`topics/terraform/exercises/`): launching EC2 instances, renaming S3 buckets, and a local provider.
- **Containers** (`topics/containers/`): running containers, building images, volumes, multi-stage builds, and restart policies.
- **Linux** (`topics/linux/exercises/`): navigation, creating and removing files, copying, and counting unique values.
- **Shell** (`topics/shell/`): hello world, variables, arguments, loops, functions, and file checks.
- **Git** (`topics/git/`): commits, branches, and squashing commits.
- **Ansible** (`topics/ansible/`): tasks and playbooks.
- **CI/CD** (`topics/cicd/`): setting up a CI pipeline, deploying to Kubernetes, and Jenkins Groovy scripts that remove jobs and builds.
- **Databases** (`topics/databases/`): designing tables for a message board system.
- **Other**: OpenShift projects and applications (`topics/openshift/`), Python exercises (`topics/python/`), Node.js questions (`topics/node/`), and an improve-query SQL exercise (`topics/sql/`).

## Hands-on projects

These are self-contained projects, not question sets.

- **Flask container CI** ([topics/flask_container_ci](topics/flask_container_ci/README.md)): a Flask app with `tests.py` that you are asked to fix, containerize, and add CI for. The app exposes `/users` and `/users/<username>` endpoints. The README describes the expected behavior.
- **Flask container CI, matrix app** ([topics/flask_container_ci2](topics/flask_container_ci2/README.md)): a second Flask app that serves matrix data from a string such as `123n456n789` through row and column endpoints. It has the same containerize-and-CI brief.
- **Deploy to Kubernetes** ([topics/cicd/solutions/deploy_to_kubernetes](topics/cicd/solutions/deploy_to_kubernetes/README.md)): a worked example that installs Jenkins, deploys a Kubernetes cluster, and uses an Ansible playbook and Jenkinsfile to deploy a sample web page.
- **Subnets** ([topics/aws/exercises/subnets](topics/aws/exercises/subnets/)): infrastructure-as-code for the subnets exercise. The Pulumi program creates three subnets (`10.0.0.0/24`, `10.0.1.0/24`, `10.0.2.0/24`) in a VPC; a Terraform version is also included.
- **AWS S3 event triggering** ([scripts/aws s3 event triggering](scripts/aws%20s3%20event%20triggering/)): a Lambda function (`s3-lambda/s3-lambda.py`) and a shell script (`aws_s3_event_trigger.sh`) for an S3 event trigger.
- **Coding examples** ([coding/python](coding/python/)): `binary_search.py` and `merge_sort.py`.

## Certification guides

The [certificates](certificates/) directory contains notes for:

- AWS Certified Cloud Practitioner
- AWS Certified Cloud SysOps Administrator (Associate)
- AWS Certified Solutions Architect (Associate)
- AWS certification paths
- Azure Fundamentals (AZ-900)
- Certified Kubernetes Administrator (CKA)
- Certified Kubernetes Application Developer (CKAD)

## Scripts

All scripts are in [scripts/](scripts/). `count_questions.sh` and `random_question.py` read files by relative path, so run them from the repository root.

- `count_questions.sh` counts question and exercise entries in the root `README.md` and `topics/*/README.md`, prints the total, and updates the `currently **N**` text in the root `README.md`.
- `random_question.py` quizzes you on random question and answer pairs read from `README.md`. Pass `-s` to skip questions that have no answer. It requires a `README.md` that contains question blocks.
- `update_question_number.py` replaces the line containing `:bar_chart:` in `README.md` with the total question count. It imports `scripts.question_utils`, so run it as a module from the root (`python -m scripts.update_question_number`).
- `question_utils.py` contains the parsing helpers used by the scripts above.
- `run_ci.sh` is the local CI entry point (see below).

## Tests and CI

- `tests/syntax_lint.py` checks that the `<details>`, `</details>`, `<summary>`, and `</summary>` tags in a Markdown file are balanced. It takes a file path as its argument.
- `tests/scripts_question_utils_unittest.py` and `tests/syntax_checker_unittest.py` are unit tests. They use the files in `tests/testcases/`. The syntax checker test is marked work in progress in its docstring.
- `scripts/run_ci.sh` runs the syntax lint on every Markdown file outside `tests/`, then runs `flake8 --max-line-length=100` on the repository.
- `.github/workflows/ci_workflow.yml` runs `scripts/run_ci.sh` on GitHub Actions for pull requests targeting `master`.

To run the same checks locally, install `flake8` and run from the repository root:

```bash
pip install flake8
bash scripts/run_ci.sh
```

## Contributing

Pull requests are the way to contribute. See [CONTRIBUTING.md](CONTRIBUTING.md). The required format for a question is:

```
<details>
<summary>[Question]</summary><br><b>

[Answer]
</b></details>
```

The contributing guide also asks contributors to avoid installation questions, avoid copying questions from other sources, and use only free images. [faq.md](faq.md) adds that copied interview questions are not accepted.

Before submitting a pull request, run `bash scripts/run_ci.sh`.

## Further reading

- [faq.md](faq.md) covers questions about the project, its purpose, and how to use it.
- [prepare_for_interview.md](prepare_for_interview.md) has opinionated notes on preparing for DevOps, SRE, and production engineering interviews.

## License and credits

The content is released under the Creative Commons license in [LICENSE](LICENSE). The license includes noncommercial terms; read the file for the full terms.

Logos and images are credited in [credits.md](credits.md).
