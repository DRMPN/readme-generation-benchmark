# Professional Programming

A collection of learning materials and references about professional software development. The repository covers code quality, architecture, testing, databases, scalability, error handling, and front-end development, with reading materials, example code, and supporting images.

## Who this is for

This repository is intended for people learning or practising software development who want to improve how they design, write, test, and maintain software. It can be used for self-study, as a reference, or as supporting material for a course.

## How to use this repository

The materials are primarily documents and examples; this is not a packaged application with a single setup or run command.

1. Start with the relevant `README.md` files to understand how the materials are organised.
2. Follow the suggested path below, or jump directly to a topic you want to explore.
3. Read the Markdown documents and PDFs in a viewer of your choice.
4. Run or adapt the Python examples where useful. Check any surrounding guidance before applying an example to a real project.

## Suggested reading path

1. **Foundations:** Review the glossary and introductory material.
2. **Code quality:** Explore clean-code guidance and the code and error-handling antipatterns.
3. **Testing:** Read about testing antipatterns and the test pyramid.
4. **Architecture and design:** Continue with clean architecture, MVCS, database practices, and scalability.
5. **Front-end development:** Work through the JavaScript, React, TypeScript, browser, HTML, CSS, and front-end practices materials.
6. **Practice and discussion:** Use the examples and diagrams to revisit concepts, then consult `CONTRIBUTING.md` if you want to improve the repository.

## Topics and materials

### Code quality and maintainability

- `Clean-Code-V2.4.pdf` — clean-code reference.
- `code-antipatterns.md` — code practices and patterns to recognise or avoid.
- `glossary.md` — terminology used across the materials.
- `feature-flags.md` — notes on feature flags.

### Architecture and system design

- `Clean-Architecture-V1.0.pdf` — clean-architecture reference.
- `mvcs-antipatterns.md` — MVCS-related antipatterns.
- `scalability-antipatterns.md` — scalability-related antipatterns.
- `software_architecture_pasta.png`, `clean-architecture-cone.jpg`, and `uwe-friedrichsen-resilient-architecture.png` — supporting architecture visuals.

### Testing and error handling

- `tests-antipatterns.md` — testing practices and antipatterns.
- `error-handling-antipatterns.md` — error-handling guidance.
- `reraise_exceptions_bad.py` and `reraise_exceptions_good.py` — contrasting exception re-raising examples.
- `exists.py` — a small Python example.
- `test-pyramid.png` — testing-related visual.

### Databases

- `database-antipatterns.md` — database-related antipatterns.
- `sqlalchemy-antipatterns.md` — SQLAlchemy-specific antipatterns.

### Front-end development

The front-end materials cover modern JavaScript, React, TypeScript, browser behaviour, and HTML/CSS practices. They include:

- `01-modern-javascript.md`
- `02-react.md`
- `03-typescript.md`
- `04-the-browser.md`
- `05-css-html-restart.md`
- `06-front-end-development-practices.md`

Supporting assets include `caniuse.png`, `js-the-good-parts.jpg`, and `hoisting.html`. Consult the front-end section’s `README.md` for its local organisation and any additional context.

### Software development practice

The repository also includes visual material on topics such as automation, MVPs, technical debt, defects, problem decomposition, optimisation, UX, and debugging. Examples include `how-not-to-build-mvp.jpg`, `premature-optimization-flowchart.png`, `cost-of-defects.jpg`, `tech-debt.jpeg`, and `decomposing problems.jpg`.

## Examples and assets

The Python files are small examples for learning and discussion, not a complete Python package. The image files support the written material and may be referenced from documents. Filenames with spaces are intentional; quote or escape them when using shell commands.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution guidance. When making changes, preserve the educational context of examples and update related documentation or assets when needed.

## License

See [`LICENSE`](LICENSE) for the terms under which this repository may be used and shared.
