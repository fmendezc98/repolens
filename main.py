"""RepoLens – CLI tool that analyzes a GitHub repo and generates an architecture report."""

import argparse
import sys

from openai import OpenAI

from analyzer import clone_repo, analyze_repo, cleanup
from prompts import build_prompt


def generate_report(prompt: str, model: str = "gpt-4o") -> str:
    """Send the analysis prompt to an LLM and return the markdown report."""
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content


def main() -> None:
    parser = argparse.ArgumentParser(
        description="RepoLens – Analyze a GitHub repo and generate an architecture report.",
    )
    parser.add_argument("repo_url", help="GitHub repository URL to analyze")
    parser.add_argument(
        "-m",
        "--model",
        default="gpt-4o",
        help="OpenAI model to use (default: gpt-4o)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Save the report to a file instead of printing to stdout",
    )
    args = parser.parse_args()

    # 1. Clone
    print(f"Cloning {args.repo_url} ...")
    try:
        repo_path = clone_repo(args.repo_url)
    except Exception as e:
        print(f"Error cloning repo: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        # 2. Analyze
        print("Analyzing repository structure ...")
        analysis = analyze_repo(repo_path)
        print(
            f"  Found {analysis['total_files']} files, "
            f"{len(analysis['languages'])} languages, "
            f"{len(analysis['entry_points'])} entry points."
        )

        # 3. Build prompt & call LLM
        prompt = build_prompt(analysis)
        print(f"Generating architecture report with {args.model} ...")
        report = generate_report(prompt, model=args.model)

        # 4. Output
        if args.output:
            with open(args.output, "w") as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print("\n" + report)

    finally:
        cleanup(repo_path)


if __name__ == "__main__":
    main()
