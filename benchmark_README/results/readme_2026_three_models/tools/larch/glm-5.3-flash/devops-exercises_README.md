# DevOps Exercises 🚀

Welcome to **devops-exercises** — a comprehensive collection of exercises, questions, and projects covering the vast world of **DevOps**. This repository is designed to help you learn, practice, and master DevOps concepts — whether you are preparing for an interview, a certification, or simply want to level up your skills.

> 💡 **Tip:** Each exercise lives in its own directory, typically containing an `exercise.md` (the task) and a `solution.md` (a reference solution). Try to solve the exercise yourself **before** peeking at the solution!

---

## 📚 Table of Contents

- [About](#about)
- [Topics Covered](#topics-covered)
- [How to Use This Repository](#how-to-use-this-repository)
- [Exercises & Questions](#exercises--questions)
- [Projects](#projects)
- [Certifications](#certifications)
- [Scripts & Tools](#scripts--tools)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)

---

## 🎯 About

DevOps is a broad field spanning operating systems, programming, cloud, containers, CI/CD, monitoring, and more. Finding structured hands-on practice can be difficult. This repository attempts to solve that by providing:

- **Hands-on exercises** for a wide range of DevOps tools and platforms
- **Interview questions** and knowledge checks
- **Full projects** to practice end-to-end workflows
- **Visual diagrams** to help you understand complex architectures

---

## 🗂️ Topics Covered

### 🐧 Linux & Shell Scripting
- Hello World, printing and checking arguments (`hello_world.md`, `print_arguments.md`, `argument_check.md`, `num_of_args.md`)
- File and directory operations (`empty_files.md`, `files_size.md`, `directories_comparison.md`)
- Text processing with `grep` (`grep_berfore_and_after.md`)
- Dates, math, and logic puzzles (`basic_date.md`, `sum.md`, `factors.md`, `count_chars.md`, `great_day.md`)
- Host inspection (`host_status.md`)

### 🐍 Python
- Data structures and algorithms (`reverse_string.md`, `compress_string.md`, `merge_sort.py`, `binary_search.py`, `advanced_data_types.md`, `sort.md`, `data_types.md`)
- Classes and OOP (`class_0x00.md`)
- Python apps and testing (`main.py`, `tests.py`, `config.py`, `requirements.txt`)

### 🐳 Containers
- Getting started with containers (`hello_world.md`, `working_with_images.md`)
- Running containers and web servers (`running_containers.md`, `containerized_web_server.md`)
- Containerized databases with persistent storage (`containerized_db.md`, `containerized_db_persistent_storage.md`)
- Building images (`write_containerfile_run_container.md`, `multi_stage_builds.md`, `image_layers.md`, `commit_image.md`, `sharing_images.md`)
- Fun exercises (`run_forest_run.md`)
- App containerization (`containerize_app.md`)

### ☸️ Kubernetes
- Pods, ReplicaSets, Services (`pods_01.md`, `replicaset_01/02/03.md`, `services_01.md` with YAML manifests)
- Killing containers (`killing_containers.md`)
- Cluster architecture (`cluster_architecture_exercise.png`, `cluster_architecture_solution.png`)
- Certification prep (`CKA.md`, `ckad.md`, `cka.md`)

### 🔄 CI/CD
- Jenkins (`jenkins_pipelines.md`, `jenkins_scripts.md`, `Jenkinsfile`, pipeline groovy scripts like `remove_builds.md`, `remove_jobs.md`, `remove_builds_solution.groovy`)
- Git workflows (`fork_101.md`, `fork_102.md`, `squashing_commits.md`, `commit_01.md`, `branch_01.md` with solutions)
- CI for open source (`ci_for_open_source_project.md`)
- GitHub Actions (`deploy.yml`)
- Deployment pipelines to Kubernetes (`pipeline_deploy_image_to_k8.md`, `deploy_to_kubernetes.md`)

### 🏗️ Terraform / Infrastructure as Code
- Multiple Terraform exercises with `main.tf`, `versions.tf`, `vars.tf`, `exercise.md` and `solution.md`
- Handling multiple Terraform versions

### ☁️ Cloud (AWS, Azure, GCP)
- AWS Lambda (`s3-lambda.py`, `aws_s3_event_trigger.sh`, `aws_lambda_direct_access.png`)
- Cloud Slack bots (`cloud_slack_bot.md`)
- Certifications (see below)

### ⚙️ Configuration Management & Automation
- Ansible (`my_first_playbook.md`, `my_first_task.md`, `update_upgrade_task.md`, `helloworld.yml`, `inventory`)
- Puppet (`puppet.png`)

### 📊 Monitoring, Logging & Observability
- ELK stack (`elk_kibana_aws.md`, `elflk.md`, `elastic.png`, `jenkins-to-kibana.png`)
- Prometheus, Grafana, Datadog diagrams and concepts

### 🌐 Networking & Web
- Web scraping (`web_scraper.md`)
- Load balancers (`identify_load_balancer.png`)
- DNS, CDN, and network diagrams

### 💾 Databases
- Data modeling (`table_for_message_board_system.md`)
- SQL and MongoDB practice

### 🧪 Miscellaneous
- Regular expressions, regex diagrams (`regex.png`)
- System design (`system_design_hero.png`, `system_design_notebook.png`, `design.png`)
- Big data, Kafka, chaos engineering, SRE checklists, OpenStack, Git internals, and more

---

## 🧭 How to Use This Repository

1. **Pick a topic** you want to practice (e.g., containers, Linux, Kubernetes).
2. **Open the exercise** (`exercise.md`) and read the requirements.
3. **Solve it on your own** — spin up a VM, container, or free cloud account as needed.
4. **Compare with the solution** (`solution.md`) and reflect on differences.
5. **Repeat** and move to more advanced topics.

Suggested learning path for beginners:

```
Linux → Shell Scripting → Python → Git → Containers → Kubernetes → CI/CD → Terraform → Cloud
```

---

## 🏆 Certifications

Preparation notes and links for popular certifications:

| Certification | File |
|---|---|
| AWS Cloud Practitioner | `aws-cloud-practitioner.md` |
| AWS Solutions Architect Associate | `aws-solutions-architect-associate.md` |
| AWS SysOps Associate | `aws-cloud-sysops-associate.md` |
| Azure Fundamentals (AZ-900) | `azure-fundamentals-az-900.md` |
| Certified Kubernetes Administrator (CKA) | `cka.md` / `CKA.md` |
| Certified Kubernetes Application Developer (CKAD) | `ckad.md` |
| AWS Certification Paths Overview | `aws-certification-paths.md` |

---

## 🛠️ Scripts & Tools

Repository utilities for managing and validating content:

| File | Purpose |
|---|---|
| `syntax_lint.py` | Lints markdown exercise files for syntax errors |
| `syntax_checker_unittest.py` | Unit tests for the syntax checker |
| `scripts_question_utils_unittest.py` | Tests for question utilities |
| `question_utils.py` | Helper functions for question handling |
| `random_question.py` | Pick a random question to answer |
| `count_questions.sh` | Counts the total number of questions/exercises |
| `update_question_number.py` | Updates question numbering |
| `run_ci.sh` | CI script to run checks |
| `prepare_for_interview.md` | Interview preparation guide |

There is also a `tests/` package (`config.py`, `__init__.py`, `tests.py`, `main.py`) for testing Python-based exercises.

---

## 📖 Interview Preparation

Start with [`prepare_for_interview.md`](prepare_for_interview.md) for guidance on structuring your study plan, then drill through the topic-specific exercises. Use `random_question.py` to quiz yourself!

---

## 🤝 Contributing

Contributions are more than welcome! 🎉

- Add new exercises, questions, or solutions
- Fix typos and improve existing explanations
- Add new topics or diagrams

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines before submitting a pull request.

---

## 🙏 Credits

Thanks to the community members who contributed exercises, solutions, and diagrams. See [`credits.md`](credits.md) for details.

---

## 📄 License

This project is licensed under the terms of the [LICENSE](LICENSE) file.

---

**Happy learning, and may the DevOps be with you!** 🖖
