# RepoLens

## 🚀 What It Does

RepoLens is a CLI tool that clones any GitHub repository, analyzes its structure, and generates a clean **Markdown architecture report** powered by LLM reasoning.

Give it a repo URL — get back a structured breakdown of the tech stack, architecture style, key components, entry points, and recommendations. No manual digging required.

```bash
python main.py https://github.com/pallets/flask -o report.md
```

## 🧠 Why I Built This

As an engineer with a product background, I constantly context-switch across unfamiliar codebases — evaluating open-source tools, onboarding onto new projects, or reviewing technical decisions. I wanted a fast, repeatable way to understand how a system is organized without spending an hour clicking through folders.

RepoLens turns that hour into seconds.

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python |
| Repo Cloning | Git (subprocess, shallow clone) |
| Structure Analysis | `os.walk`, `pathlib`, `collections.Counter` |
| LLM Integration | OpenAI API (`gpt-4o` by default) |
| Interface | CLI via `argparse` |

## 📦 Setup

```bash
# Clone this repo
git clone https://github.com/your-username/repolens.git
cd repolens

# Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="sk-..."
```

## 📖 Usage

```bash
# Analyze a repo and print the report to stdout
python main.py https://github.com/user/repo

# Use a different model
python main.py https://github.com/user/repo -m gpt-4o-mini

# Save the report to a file
python main.py https://github.com/user/repo -o report.md
```

## 📌 Example Output

> Output from running `python main.py https://github.com/pallets/flask`

---

# Architecture Report — Flask

## Overview

Flask is a lightweight WSGI web application framework for Python. It is designed as a micro-framework that provides the core essentials — routing, request handling, templating, and session management — while remaining extensible through a rich ecosystem of extensions.

## Tech Stack

- **Python** — Primary language (169 files)
- **JavaScript** — Used in documentation tooling (2 files)
- **YAML** — CI/CD workflows and configuration (5 files)
- **TOML** — Project metadata and build configuration
- **Markdown** — Documentation and changelogs
- **Frameworks/Tools:** Sphinx (docs), pytest (testing), tox (test automation), pre-commit

## Architecture Style

**Modular monolith / micro-framework.** Flask follows a single-package architecture where the core framework lives in `src/flask/` as a cohesive module. It is designed for extensibility rather than built-in complexity — users compose behavior through blueprints, extensions, and middleware.

## Key Components

| Directory | Role |
|-----------|------|
| `src/flask/` | Core framework — app, blueprints, routing, request/response, sessions, templating, JSON handling, CLI |
| `src/flask/sansio/` | Sans-I/O base classes enabling framework logic decoupled from the WSGI layer |
| `tests/` | Comprehensive test suite covering all core modules |
| `docs/` | Sphinx-based documentation (user guide, API reference, deployment) |
| `examples/` | Tutorial applications demonstrating usage patterns |
| `.github/workflows/` | CI pipeline — tests, linting, publishing |

## Entry Points

- **`src/flask/__init__.py`** — Package entry point, re-exports public API
- **`src/flask/cli.py`** — `flask` CLI command (`flask run`, `flask shell`)
- **`Dockerfile`** — Container-based deployment

## Observations & Recommendations

- Clean separation between I/O-bound and logic-only code via `sansio/` — a forward-looking pattern.
- Well-structured test suite mirrors the source layout, making it easy to find relevant tests.
- Documentation is co-located and thorough, suitable for a project of this maturity.
- The `examples/` directory provides a good onboarding path for new contributors.

---

## 🗂 Project Structure

```
repolens/
├── main.py          # CLI entry point — orchestrates the pipeline
├── analyzer.py      # Clones repos and analyzes folder structure
├── prompts.py       # LLM prompt template and formatting
├── requirements.txt # Dependencies
└── README.md
```
