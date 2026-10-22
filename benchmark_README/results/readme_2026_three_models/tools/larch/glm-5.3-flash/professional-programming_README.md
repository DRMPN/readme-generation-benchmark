# Professional Programming

A curated collection of articles, resources, and visual guides for becoming a better software developer. This repository gathers high-quality reading material covering software design, architecture, testing, databases, front-end development, and professional practices.

---

## 📚 About

This repository serves as a personal knowledge base and learning resource. It contains curated articles, PDFs, diagrams, and code examples focused on writing clean, maintainable, and professional software. The materials are suitable for developers at any stage of their career — from junior developers building strong foundations to senior engineers refining their craft.

---

## 🗂️ Repository Structure

### Software Design & Clean Code

| File | Description |
|------|-------------|
| `Clean-Code-V2.4.pdf` | Comprehensive guide on clean code principles |
| `Clean-Architecture-V1.0.pdf` | Guide to clean architecture concepts and patterns |
| `glossary.md` | Glossary of key software development terms |
| `code-antipatterns.md` | Common code antipatterns and how to avoid them |
| `software_architecture_pasta.png` | Visual: spaghetti vs. structured architecture |
| `decomposing problems.jpg` | Visual: strategies for problem decomposition |

### Architecture & Scalability

| File | Description |
|------|-------------|
| `scalability-antipatterns.md` | Common scalability mistakes and pitfalls |
| `mvcs-antipatterns.md` | Antipatterns in MVC-style architectures |
| `clean-architecture-cone.jpg` | Visual: the clean architecture cone of dependency |
| `uwe-friedrichsen-resilient-architecture.png` | Visual: principles of resilient architecture |
| `how-not-to-build-mvp.jpg` | Visual: common mistakes when building an MVP |
| `mvp.jpeg` | Visual: minimum viable product concepts |
| `rewrite.gif` | Visual: the "full rewrite" trap |

### Code Examples

| File | Description |
|------|-------------|
| `reraise_exceptions_bad.py` | Example of bad exception re-raising practices |
| `reraise_exceptions_good.py` | Example of proper exception re-raising practices |
| `exists.py` | Code example (file existence / data checks) |

### Error Handling & Testing

| File | Description |
|------|-------------|
| `error-handling-antipatterns.md` | Antipatterns in error handling |
| `tests-antipatterns.md` | Antipatterns in software testing |
| `test-pyramid.png` | Visual: the testing pyramid (unit / integration / E2E) |
| `what to assert.png` | Visual: guidance on what to assert in tests |
| `let-your-bugs-teach-you-julia-evans.jpg` | Visual: learning from your bugs (Julia Evans) |
| `cost-of-defects.jpg` | Visual: how the cost of defects grows over time |

### Databases & SQLAlchemy

| File | Description |
|------|-------------|
| `sqlalchemy-antipatterns.md` | Common SQLAlchemy antipatterns |
| `database-antipatterns.md` | General database design antipatterns |

### Front-End Development

The `front-end` section covers modern client-side development practices:

| File | Description |
|------|-------------|
| `README.md` | Front-end section overview |
| `01-modern-javascript.md` | Modern JavaScript features and best practices |
| `02-react.md` | React development practices |
| `03-typescript.md` | TypeScript adoption and patterns |
| `04-the-browser.md` | How the browser works |
| `05-css-html-restart.md` | Modern CSS and HTML fundamentals |
| `06-front-end-development-practices.md` | General front-end development practices |
| `hoisting.html` | Interactive example: JavaScript hoisting |
| `caniuse.png` | Visual: browser compatibility considerations |
| `learning-roadmap.png` | Visual: front-end learning roadmap |
| `js-the-good-parts.jpg` | Visual: the good parts of JavaScript |

### General Practices & Essays

| File | Description |
|------|-------------|
| `README.md` | Overview of general practices |
| `feature-flags.md` | Feature flag best practices |
| `amazon_writing_rules.jpeg` | Visual: Amazon's writing culture rules |
| `premature-optimization-flowchart.png` | Visual: when (not) to optimize |
| `premature automation.png` | Visual: the dangers of premature automation |
| `tech-debt.jpeg` | Visual: understanding technical debt |
| `waterfall-UX.jpeg` | Visual: waterfall vs. iterative UX processes |
| `us-vs-them.jpeg` | Visual: avoiding "us vs. them" team mentalities |

---

## 🎯 Topics Covered

- **Clean Code** — naming, functions, comments, formatting, and readability
- **Clean Architecture** — separation of concerns, dependency rules, layering
- **Antipatterns** — code, database, scalability, MVC, error handling, and testing antipatterns
- **SQLAlchemy & Databases** — common pitfalls in ORM usage and schema design
- **Front-End Development** — JavaScript, React, TypeScript, browser internals, and modern CSS/HTML
- **Testing** — the testing pyramid, common testing mistakes
- **Professional Practices** — feature flags, technical debt management, writing culture, and problem decomposition

---

## 🚀 Getting Started

This is a documentation-only repository — no build steps or dependencies are required.

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/professional-programming-knxt6qhe.git
   cd professional-programming-knxt6qhe
   ```

2. **Browse the content:**
   - Start with `Clean-Code-V2.4.pdf` and `Clean-Architecture-V1.0.pdf` for foundational reading.
   - Review the antipattern articles (`code-antipatterns.md`, `tests-antipatterns.md`, `error-handling-antipatterns.md`) to recognize common mistakes.
   - Work through the front-end series in numbered order (`01` through `06`).
   - Use the images and diagrams as quick visual references.

3. **Optional — run the Python examples:**

   ```bash
   python reraise_exceptions_bad.py   # see the antipattern in action
   python reraise_exceptions_good.py  # see the recommended approach
   ```

---

## 📖 Suggested Reading Path

1. **Foundations:** Clean Code → Clean Architecture
2. **Recognizing problems:** Code antipatterns → Error-handling antipatterns → Testing antipatterns
3. **Data layer:** Database antipatterns → SQLAlchemy antipatterns
4. **Scale:** Scalability antipatterns → MVC(S) antipatterns
5. **Front-end:** Modern JavaScript → React → TypeScript → The Browser → CSS/HTML → Front-end practices
6. **Craft:** Feature flags → Writing rules → Technical debt → Premature optimization

---

## 🤝 Contributing

Contributions are welcome! If you'd like to add an article, fix an error, or suggest a resource:

1. Read `CONTRIBUTING.md` for guidelines.
2. Fork the repository and create a branch for your change.
3. Submit a pull request with a clear description of what you're adding or fixing.

Please ensure any contributed material aligns with the repository's focus on clean, professional software development.

---

## 📄 License

This project is licensed under the terms described in the [`LICENSE`](LICENSE) file. Individual articles and images may have their own licenses or copyright holders — please respect the original authors' rights when sharing or reusing content.

---

## 🙏 Acknowledgments

Thanks to all the authors, bloggers, and educators whose articles and diagrams make up this collection — including contributors to the clean code and clean architecture communities, and creators of popular educational illustrations such as those by Julia Evans.
