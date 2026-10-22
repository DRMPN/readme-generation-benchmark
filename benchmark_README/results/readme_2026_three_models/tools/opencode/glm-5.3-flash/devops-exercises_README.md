# DevOps Exercises

DevOps exercises, questions, and challenges designed to help you learn DevOps concepts, practice hands-on skills, and prepare for DevOps, SRE, and Production Engineer interviews.

> Note: this repository is meant for learning. Don't assume your interviews will include similar questions to those in this repository.

## Repository Structure

### topics/

The core of the repository — self-contained material organized by topic. Most topics have a `README.md` listing exercises (with links to solution files) and questions, while some topics contain standalone exercise and solution files. Topics include:

* **Operating systems & scripting:** [Linux](topics/linux/README.md), [OS](topics/os/), [Shell](topics/shell/README.md), [Perl](topics/perl/README.md)
* **Containers & orchestration:** [Containers](topics/containers/README.md), [Kubernetes](topics/kubernetes/README.md), [OpenShift](topics/openshift/README.md)
* **Cloud:** [Cloud](topics/cloud/README.md), [AWS](topics/aws/README.md), [Azure](topics/azure/README.md), [GCP](topics/gcp/README.md)
* **CI/CD & automation:** [CI/CD](topics/cicd/README.md), [Jenkins pipelines](topics/jenkins_pipelines.md), [Jenkins scripts](topics/jenkins_scripts.md), [Zuul](topics/zuul/README.md), [CircleCI](topics/circleci/README.md)
* **Configuration management & infrastructure:** [Ansible](topics/ansible/README.md), [Terraform](topics/terraform/README.md)
* **Observability:** [Observability](topics/observability/README.md), [Datadog](topics/datadog/README.md), [Grafana](topics/grafana/README.md)
* **Databases & programming:** [Databases](topics/databases/README.md), [SQL](topics/sql/), [Python](topics/python/), [Node](topics/node/), [Programming](topics/programming/), [Software development](topics/software_development/README.md)
* **Networking & other topics:** [Git](topics/git/README.md), [DNS](topics/dns/README.md), [Kafka](topics/kafka/README.md), [Security](topics/security/README.md), [Chaos engineering](topics/chaos_engineering/README.md), [Argo](topics/argo/README.md), [DevOps](topics/devops/README.md), [SRE](topics/sre/README.md), [Soft skills](topics/soft_skills/README.md)
* **Project-based topics:** [Flask container CI](topics/flask_container_ci/README.md), [Flask container CI 2](topics/flask_container_ci2/README.md)

### exercises/

Hands-on exercises, such as shell scripting tasks (e.g., comparing directories — see [exercises/shell/solutions](exercises/shell/solutions/directories_comparison.md)).

### coding/

Coding exercises, including Python implementations of [binary search](coding/python/binary_search.py) and [merge sort](coding/python/merge_sort.py).

### certificates/

Guidance and practice questions for certifications:

* [AWS certification paths](certificates/aws-certification-paths.md)
* [AWS Cloud Practitioner](certificates/aws-cloud-practitioner.md)
* [AWS Solutions Architect Associate](certificates/aws-solutions-architect-associate.md)
* [AWS SysOps Associate](certificates/aws-cloud-sysops-associate.md)
* [Azure Fundamentals (AZ-900)](certificates/azure-fundamentals-az-900.md)
* [Certified Kubernetes Administrator (CKA)](certificates/cka.md)
* [Certified Kubernetes Application Developer (CKAD)](certificates/ckad.md)

### scripts/

Helper scripts and tooling:

* [`run_ci.sh`](scripts/run_ci.sh) — runs syntax linting on all `.md` files and PEP8 (flake8) checks locally
* [`count_questions.sh`](scripts/count_questions.sh) — counts the number of questions and exercises
* [`random_question.py`](scripts/random_question.py) — quizzes you with a random question (and its answer) parsed from a `README.md` file
* [`question_utils.py`](scripts/question_utils.py) and [`update_question_number.py`](scripts/update_question_number.py) — question bookkeeping utilities
* An example of [automating notifications for objects uploaded to an S3 bucket](scripts/aws%20s3%20event%20triggering/README.md) (S3 → Lambda → SNS, via AWS CLI)

### tests/

Tests used by CI to validate the content, including [syntax_lint.py](tests/syntax_lint.py), [syntax_checker_unittest.py](tests/syntax_checker_unittest.py), and [scripts_question_utils_unittest.py](tests/scripts_question_utils_unittest.py).

## How to Use

1. Pick a topic you want to learn from its directory under [`topics/`](topics/).
2. Topic material includes **exercises** (with links to solutions) and **questions**. Questions are collapsible (implemented with HTML `<details>` tags): try to answer first, then click to reveal the answer.
3. Prefer a hands-on start? Begin with the exercises in the topic directory.
4. Note that many questions intentionally have no written answer — researching them yourself (via search engines, documentation, and communities) is part of the learning experience.

## Preparing for DevOps Interviews

See [prepare_for_interview.md](prepare_for_interview.md) for an (opinionated) guide on the skills expected from DevOps engineers — Linux, programming, architecture & design, and tooling — plus practical preparation steps such as converting job requirements into practice scenarios, starting your own DevOps project, and what to expect from interviews.

## FAQ

Answers to common questions — the purpose of the repository, how to become a better DevOps engineer, where answers come from, and more — are in [faq.md](faq.md).

## Contributing

Contributions are welcome via pull requests. Please follow the question format described in [CONTRIBUTING.md](CONTRIBUTING.md):

```html
<details>
<summary>[Question]</summary><br><b>

[Answer]
</b></details>
```

A few things to keep in mind:

* Avoid adding installation questions
* Don't copy questions and answers from other sources
* If you add new images, make sure they are free to use
* Test your changes locally with `scripts/run_ci.sh` before submitting a pull request

Continuous integration runs on pull requests (see [.github/workflows/ci_workflow.yml](.github/workflows/ci_workflow.yml) and [.travis.yml](.travis.yml)), running markdown syntax linting and flake8 (PEP8) checks.

## Credits

Logos and icons used in this repository were created by various artists and projects — attribution and license details are listed in [credits.md](credits.md).

## License

This project is licensed under a Creative Commons license — see [LICENSE](LICENSE). In summary: you must provide attribution, non-commercial use only, and any redistribution must be under the same license terms.
