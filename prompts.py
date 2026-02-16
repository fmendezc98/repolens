"""Prompt templates for LLM-based architecture analysis."""

ARCHITECTURE_PROMPT = """\
You are a senior software architect. Given the following repository summary, \
produce a clean, well-structured **Markdown architecture report**.

## Repository Summary

- **Total files:** {total_files}
- **Languages detected:** {languages}
- **Likely entry points:** {entry_points}

### Folder structure
```
{folder_structure}
```

## Instructions

Based on the information above, write a report that includes:

1. **Overview** – A one-paragraph high-level description of what this project likely does.
2. **Tech Stack** – Languages, frameworks, and tooling inferred from the file structure.
3. **Architecture Style** – Identify the architectural pattern (monolith, microservices, \
monorepo, serverless, etc.) and explain why.
4. **Key Components** – Describe the major modules/directories and their probable roles.
5. **Entry Points** – Explain how the application is likely started or deployed.
6. **Observations & Recommendations** – Any notable patterns, potential issues, or \
suggestions for improvement.

Return ONLY the Markdown report, nothing else.
"""


def build_prompt(analysis: dict) -> str:
    """Format the architecture prompt with analysis data."""
    languages_str = ", ".join(
        f"{lang} ({count} files)" for lang, count in analysis["languages"].items()
    )
    entry_points_str = ", ".join(analysis["entry_points"]) or "None detected"
    folder_str = "\n".join(analysis["folder_structure"][:80])
    if len(analysis["folder_structure"]) > 80:
        folder_str += f"\n... and {len(analysis['folder_structure']) - 80} more folders"

    return ARCHITECTURE_PROMPT.format(
        total_files=analysis["total_files"],
        languages=languages_str or "None detected",
        entry_points=entry_points_str,
        folder_structure=folder_str,
    )
