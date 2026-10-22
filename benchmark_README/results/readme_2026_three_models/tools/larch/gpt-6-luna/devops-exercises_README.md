# DevOps Exercises

A hands-on collection of exercises and learning resources for software development, system administration, cloud infrastructure, and DevOps. The repository includes written challenges, example solutions, code samples, configuration files, diagrams, and interview-preparation material.

## Who this is for

This repository is useful for:

- People learning DevOps and related technologies through practice.
- Developers preparing for DevOps, cloud, and platform engineering interviews.
- Instructors or study groups looking for exercises and reference material.
- Practitioners who want to review common tools, workflows, and concepts.

## Topics covered

The materials span a broad range of subjects, including:

- **Linux and shell scripting** — command-line exercises, file and directory operations, argument handling, and basic scripting.
- **Git and collaboration** — branches, forks, commits, and squashing commits.
- **Containers** — images, running containers, Containerfiles, persistent storage, web servers, databases, and multi-stage builds.
- **CI/CD and Jenkins** — pipeline exercises, Jenkins scripts, and deployment examples.
- **Cloud and infrastructure as code** — AWS and Azure learning resources, Terraform configuration examples, and an AWS S3/Lambda example.
- **Configuration management** — Ansible playbooks and tasks.
- **Kubernetes** — pods, services, deployments, ReplicaSets, and cluster-related exercises.
- **Monitoring and logging** — ELK/Kibana and related observability material.
- **Programming and data structures** — Python examples and exercises involving sorting, searching, strings, data types, and other fundamentals.
- **System design and reliability** — diagrams and resources covering architecture, availability, distributed systems, and SRE concepts.
- **Interview preparation and certifications** — question collections and certification-path resources, including CKA and CKAD material.

The repository also contains images, diagrams, reference documents, and general learning resources. See the files themselves for the precise scope and instructions of each topic.

## How to use the repository

1. Browse the repository and choose a topic or exercise.
2. Read the relevant exercise or README before starting. Some exercises have a corresponding solution file.
3. Try to complete the exercise independently before consulting a solution.
4. Run code or configuration examples only in an environment appropriate for that tool.
5. Compare your result with the supplied solution, where one is available.

Exercises and solutions may appear alongside one another, or be organized with other topic materials. File names such as `exercise.md`, `solution.md`, and topic-specific names can help you locate related content.

## Running examples safely

Requirements vary by exercise. Some examples may need Python, a shell, Docker, Terraform, Ansible, Jenkins, or access to a cloud account. Check the exercise instructions and the files it references before running anything.

In particular:

- Review scripts and infrastructure configuration before executing them.
- Use test accounts, local environments, or sandboxes where possible.
- Check for cloud resources that may incur charges, and remove resources when finished.
- Never commit passwords, API keys, tokens, private keys, or other credentials.
- Treat deployment and destructive commands with care, especially when working in shared or production environments.

Some Python exercises include tests or helper scripts. Consult their local instructions and any `requirements.txt` file for dependencies. The repository also includes CI and validation-related scripts; inspect their contents before running them.

## Contributing

Contributions that improve the exercises or make the repository easier to use are welcome. Before submitting a change:

- Keep new material focused and include clear instructions.
- Include a solution when appropriate, while keeping it separate from the exercise prompt.
- Test code or examples where practical, and document required tools or setup.
- Avoid adding secrets, generated files, or unrelated changes.
- Check the repository’s `CONTRIBUTING.md` for contribution guidance.

## License

See [`LICENSE`](LICENSE) for the terms that apply to this repository.
