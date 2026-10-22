# DevOps Interview Questions and Exercises

This repository is a collection of learning material for DevOps and related engineering topics. It includes interview-style questions, practical exercises, and—in some areas—solutions, certification notes, and supporting scripts. Its stated purpose is learning; it can also be used as one resource when preparing for interviews, but it does not predict what any particular interview will cover.

## Getting started

Browse the topic guides below and choose a subject. Many guides contain both questions and hands-on exercises; exercises link to their instructions and, where available, a solution. Some questions are intentionally left without answers. Follow any prerequisites stated in the individual exercise—there is no single setup procedure for the whole collection.

For interview preparation advice, see [Preparing for DevOps/SRE/Production Engineer interviews](prepare_for_interview.md). The [FAQ](faq.md) explains the project's purpose and gives guidance on using and contributing to its material.

## Topic guides

### DevOps and engineering foundations

| Topic | Guide |
| --- | --- |
| DevOps | [Questions](topics/devops/README.md) |
| Linux | [Questions and exercises](topics/linux/README.md) |
| Shell | [Questions and exercises](topics/shell/README.md) |
| Software development | [Questions](topics/software_development/README.md) |
| SRE | [Questions](topics/sre/README.md) |
| Soft skills | [Questions](topics/soft_skills/README.md) |
| Security | [Questions](topics/security/README.md) |
| Git | [Questions](topics/git/README.md) |
| Databases | [Questions and exercises](topics/databases/README.md) |
| DNS | [Questions](topics/dns/README.md) |

### Cloud and infrastructure

| Topic | Guide |
| --- | --- |
| Cloud | [Questions](topics/cloud/README.md) |
| AWS | [Questions and exercises](topics/aws/README.md) |
| Azure | [Questions](topics/azure/README.md) |
| Google Cloud Platform | [Questions and exercises](topics/gcp/README.md) |
| Ansible | [Questions and exercises](topics/ansible/README.md) |
| Terraform | [Questions and exercises](topics/terraform/README.md) |
| Containers | [Questions and exercises](topics/containers/README.md) |
| Kubernetes | [Questions, exercises, and CKA notes](topics/kubernetes/README.md) |
| OpenShift | [Questions and exercises](topics/openshift/README.md) |

### Delivery, platforms, and observability

| Topic | Guide |
| --- | --- |
| CI/CD | [Questions and exercises](topics/cicd/README.md) |
| Argo | [Questions and exercises](topics/argo/README.md) |
| CircleCI | [Questions](topics/circleci/README.md) |
| Zuul | [Questions](topics/zuul/README.md) |
| Kafka | [Questions](topics/kafka/README.md) |
| Observability | [Questions](topics/observability/README.md) |
| Grafana | [Questions](topics/grafana/README.md) |
| Datadog | [Questions](topics/datadog/README.md) |
| Chaos engineering | [Questions](topics/chaos_engineering/README.md) |

### Programming and sample applications

| Topic | Guide |
| --- | --- |
| Perl | [Questions](topics/perl/README.md) |
| Flask container CI | [Example and instructions](topics/flask_container_ci/README.md) |
| Flask container CI (second example) | [Example and instructions](topics/flask_container_ci2/README.md) |

There are also standalone materials under [`topics/`](topics/), including [Jenkins pipelines](topics/jenkins_pipelines.md), [Jenkins scripts](topics/jenkins_scripts.md), [a pipeline deploying an image to Kubernetes](topics/pipeline_deploy_image_to_k8.md), [an ELK/Kibana/AWS example](topics/misc/elk_kibana_aws.md), and [a cloud Slack bot](topics/cloud_slack_bot.md).

## Other material

- [`certificates/`](certificates/) contains notes and material for AWS, Azure, and Kubernetes certifications.
- [`coding/`](coding/) contains coding examples, including Python binary search and merge sort.
- [`exercises/`](exercises/) contains additional exercises and solutions.
- [`images/`](images/) contains diagrams and other images referenced by the material.
- [`faq.md`](faq.md) answers common questions about the collection.
- [`prepare_for_interview.md`](prepare_for_interview.md) offers interview preparation suggestions.

## Repository scripts and checks

The [`scripts/`](scripts/) directory contains small utilities, including scripts for counting questions, selecting a random question from question-and-answer markup in `README.md`, updating the question count, and running repository checks. `random_question.py` reads only the root `README.md` and expects question/answer blocks there. This README is an index and contains no such blocks, so that script does not quiz the topic guides as-is.

To run the repository checks, use:

```sh
bash scripts/run_ci.sh
```

The script runs the Markdown syntax linter over Markdown files (excluding `tests/`) and then runs `flake8` over the repository. Python and `flake8` are therefore needed for this check. The individual tests and test cases are in [`tests/`](tests/).

## Contributing

Contributions are welcome via pull requests. Follow [`CONTRIBUTING.md`](CONTRIBUTING.md): use the documented question-and-answer format, avoid copied material and installation-only questions, and ensure images you add may be used. The contribution guide also describes the local check script. See [`credits.md`](credits.md) for image credits and [`LICENSE`](LICENSE) for the repository's license terms.
