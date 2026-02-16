"""Repo cloning and structure analysis."""

import os
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

EXTENSION_TO_LANGUAGE = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript (JSX)",
    ".jsx": "JavaScript (JSX)",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".c": "C",
    ".cpp": "C++",
    ".h": "C/C++ Header",
    ".cs": "C#",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".scala": "Scala",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sql": "SQL",
    ".sh": "Shell",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".json": "JSON",
    ".md": "Markdown",
    ".toml": "TOML",
    ".xml": "XML",
    ".r": "R",
    ".lua": "Lua",
    ".dart": "Dart",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".zig": "Zig",
}

ENTRY_POINT_PATTERNS = [
    "main.py",
    "app.py",
    "manage.py",
    "setup.py",
    "index.js",
    "index.ts",
    "main.go",
    "main.rs",
    "Main.java",
    "Program.cs",
    "main.c",
    "main.cpp",
    "Makefile",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
]

SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "target",
    "vendor",
}


def clone_repo(repo_url: str) -> str:
    """Clone a GitHub repo into a temporary directory. Returns the path."""
    tmp_dir = tempfile.mkdtemp(prefix="repolens_")
    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, tmp_dir],
        check=True,
        capture_output=True,
        text=True,
    )
    return tmp_dir


def analyze_repo(repo_path: str) -> dict:
    """Walk the repo and return a structured summary."""
    language_counter = Counter()
    entry_points = []
    folder_tree = []
    total_files = 0

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        rel_root = os.path.relpath(root, repo_path)
        if rel_root == ".":
            rel_root = ""

        if rel_root:
            folder_tree.append(rel_root + "/")

        for filename in files:
            total_files += 1
            ext = Path(filename).suffix.lower()
            if ext in EXTENSION_TO_LANGUAGE:
                language_counter[EXTENSION_TO_LANGUAGE[ext]] += 1

            if filename in ENTRY_POINT_PATTERNS:
                entry_points.append(
                    os.path.join(rel_root, filename) if rel_root else filename
                )

    return {
        "languages": dict(language_counter.most_common()),
        "entry_points": entry_points,
        "folder_structure": sorted(folder_tree),
        "total_files": total_files,
    }


def cleanup(repo_path: str) -> None:
    """Remove the cloned repo directory."""
    shutil.rmtree(repo_path, ignore_errors=True)
