# DevOps Exercises and Interview Questions

This repository is a collection of DevOps, SRE, and cloud learning material. It contains interview-style questions with collapsible answers, hands-on exercises with solutions, certification study notes, small sample applications, and helper scripts. According to the FAQ, the purpose of the repository is "Learning, of course."

## Overview

The repository is organized around several kinds of content:

- **Questions and answers** on topics such as Linux, Docker, Kubernetes, Ansible, Argo CD, AWS, Azure, Chaos Engineering, CI/CD, Git, SQL, Python, and shell scripting. Most answers are written in HTML `<details>` blocks so they can be expanded and hidden.
- **Exercises and solutions** in `topics/`. Many topics have an `exercises/` or `solutions/` folder, and some topic READMEs include tables that link each exercise to its solution.
- **Certificate notes** in `certificates/` for AWS (Cloud Practitioner, SysOps Associate, Solutions Architect Associate), Azure (AZ-900), and Kubernetes (CKA, CKAD).
- **Code samples** in `coding/python/` (binary search and merge sort), `topics/flask_container_ci*/` (small Flask applications), `scripts/` (question-management helpers and an AWS S3 event trigger example), and infrastructure-as-code examples in `topics/aws/exercises/` and `topics/gcp/exercises/`.
- **Supporting documents**: `faq.md`, `prepare_for_interview.md`, `CONTRIBUTING.md`, and `credits.md`.

Some exercise examples use Terraform (`main.tf`) and Pulumi (`__main__.py`). The AWS exercise solutions are described as using the AWS console, and the README for that topic recommends infrastructure-as-code tools instead.

## Repository Structure

| Path | Contents |
|------|----------|
| `topics/` | Topic folders (e.g., `ansible`, `argo`, `aws`, `containers`, `kubernetes`, `linux`, `shell`, `terraform`) with READMEs, questions, exercises, and solutions |
| `certificates/` | Study notes for AWS, Azure, and Kubernetes certifications |
| `coding/python/` | Python examples: `binary_search.py`, `merge_sort.py` |
| `scripts/` | Helper scripts for managing questions and running CI checks, plus the AWS S3 event trigger example |
| `tests/` | Unit test files and sample question files used for testing |
| `images/` | Logos and diagrams used by the Markdown files |
| `.github/workflows/` | GitHub Actions workflow file (`ci_workflow.yml`) |
| `.travis.yml` | Travis CI configuration file |

## Setup

No single setup process covers the whole repository. Setup depends on what you want to use.

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Browse the content.** The Markdown files can be read directly on the hosting platform or in any Markdown viewer. Start with the README in a topic folder, such as `topics/linux/README.md` or `topics/kubernetes/README.md`.

3. **Run the Flask sample applications** (optional). Each Flask sample lists `flask` in its `requirements.txt`:

   ```bash
   cd topics/flask_container_ci
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run the AWS S3 Lambda example** (optional). Its dependency file pins `boto3==1.17.95`:

   ```bash
   cd "scripts/aws s3 event triggering/s3-lambda"
   pip install -r requirements.txt
   ```

Note that `topics/flask_container_ci/app/main.py` imports `flask_wtf.csrf`, but the `requirements.txt` files list only `flask`. You may need to install `flask-wtf` separately.

## Usage

### Studying with questions

Each question is wrapped in a collapsible block. The question appears as a `<summary>` and the answer is hidden until expanded. Some answers are blank placeholders, which means the question is available for you to answer.

Several topic folders contain self-assessment sections. For example, `topics/ansible/README.md` includes questions on inventories, variables, precedence, and strategies, and `topics/cicd/README.md` includes questions on CI/CD practices and Jenkins.

### Working through exercises

Exercises are listed in tables in the topic READMEs with columns for the exercise, solution, and comments. For example:

- `topics/ansible/`: "My First Task," "My First Playbook," and "Upgrade and Update Task"
- `topics/argo/`: ArgoCD app creation, sync, secrets, Helm apps, and Argo Rollouts (blue/green and canary)
- `topics/aws/`: IAM, EC2, S3, ELB, Auto Scaling, VPC, databases, DNS, containers, Lambda, and more
- `topics/kubernetes/`: labels and selectors, node selectors, taints, and Kustomize common labels

Work through an `exercise.md` file first, then compare your approach with the matching `solution.md`.

### Running the Flask sample

From the `topics/flask_container_ci` directory, run:

```bash
python app/main.py
```

The application calls `app.run(port=5000)`, so it listens on port 5000. The application opens `./users.json` relative to the current working directory, so run it from the directory that contains `users.json`. The routes defined in `main.py` are:

- `/` - lists available resources
- `/users` - returns all users from `users.json`
- `/users/<username>` - returns one user, or raises a not-found error
- `/users/<username>/something` - raises `NotImplementedError`

The `flask_container_ci2` sample contains route stubs for matrix, row, and column operations. Those functions are marked with `TODO` comments and currently return nothing. The `index` route in that sample is declared as `@app.routee`, which is not a standard Flask decorator and may need correcting before the sample can run.

### Running the S3 event trigger example

The `scripts/aws s3 event triggering/` folder contains `aws_s3_event_trigger.sh`, a Lambda function `s3-lambda.py`, and a sample image. Its README is an image reference only, so refer to the script and Python file for behavior.

## Configuration

Configuration is minimal and mostly lives in the sample code:

- **Flask port:** The sample apps use port `5000` in `app.run(port=5000)`.
- **User data:** The `flask_container_ci` sample reads user records from `users.json`.
- **CSRF protection:** Both Flask samples call `CSRFProtect(app)`. Source comments note that a separate `create_test_app()` function in the first sample also creates an app with CSRF protection.
- **Python dependencies:** Each sample's `requirements.txt` lists its packages. The S3 Lambda example pins `boto3==1.17.95`.
- **Pulumi and Terraform:** The example files contain comments such as `# Run 'pulumi up'` to create the resources. Each exercise defines its own Terraform or Pulumi configuration in its `main.tf` or `__main__.py` file. For example, the Pulumi VPC example creates a VPC with CIDR `10.0.0.0/16`, and the S3 example creates a private and a public bucket in specific regions.

The repository does not include a central configuration file for the question content. Question formatting is defined by the rules in `CONTRIBUTING.md`.

## Development

### Adding questions and answers

`CONTRIBUTING.md` describes the contribution process:

1. Use pull requests to propose changes.
2. Use this format for each question:

   ```html
   <details>
   <summary>[Question]</summary><br><b>

   [Answer]
   </b></details>
   ```

3. Count your questions with `scripts/count_questions.sh`.
4. Test your changes locally with `scripts/run_ci.sh` before submitting.

The contribution guidelines also ask contributors to:

- Avoid installation questions.
- Avoid copying questions and answers from other sources.
- Use only free images that can be legally used.

`faq.md` adds that questions should have educational value and that duplicate questions are considered a bug, while similar questions are intentional.

### Helper scripts

The `scripts/` folder contains:

- `count_questions.sh` - counts questions, as referenced in `CONTRIBUTING.md`
- `run_ci.sh` - runs local checks, as referenced in `CONTRIBUTING.md`
- `question_utils.py` and `update_question_number.py` - Python utilities for question handling
- `random_question.py` - a script whose name suggests it selects a random question

Review each script before running it, because this README does not describe their full behavior.

## Testing

The `tests/` folder contains:

- `scripts_question_utils_unittest.py` - unit tests for the question utilities
- `syntax_checker_unittest.py` - unit tests for a syntax checker
- `syntax_lint.py` - a lint/syntax checking script
- `testcases/testcase1.md`, `testcase2.md`, `testcase3.md` - sample Markdown files in the question format (covering Docker, Bash and SQL, and interview-style questions)

To run the checks locally, use `scripts/run_ci.sh`, as described in `CONTRIBUTING.md`. The repository also includes `.github/workflows/ci_workflow.yml` and `.travis.yml`, which suggest that continuous integration is configured. The contents of those files are not documented here, so check them directly to see which commands run in CI.

## Continuous Integration

The repository includes CI configuration in two places:

- `.github/workflows/ci_workflow.yml` (GitHub Actions)
- `.travis.yml` (Travis CI)

Use these files as the source of truth for CI behavior.

## License

The `LICENSE` file contains the text of a Creative Commons Public License (CCPL). The license grants rights to reproduce, distribute, and publicly perform the work, subject to conditions in the text, including attribution and a prohibition on uses primarily intended for commercial advantage or private monetary compensation. The license also states that the work is offered as-is, without warranties.

Read the full `LICENSE` file for the complete terms. The FAQ states that questions may not be copied to other sites without attribution and may not be used for commercial purposes.

## Credits

`credits.md` lists the authors and licenses of the logos and icons used in the repository. These include the Jenkins, Git, Terraform, Docker, Python, Puppet, Bash, OpenStack, Linux, Kubernetes, Prometheus, MongoDB, and Google Cloud logos, along with several icon sets from Flaticon, Iconfinder, and other creators. Each entry carries its own license or trademark notice.

## Additional Resources

- `faq.md` answers common questions about the project, including how to prepare for DevOps interviews and how to contribute.
- `prepare_for_interview.md` provides opinionated guidance on preparing for DevOps, SRE, and production engineering interviews.
- `certificates/` contains study notes organized by certification.
