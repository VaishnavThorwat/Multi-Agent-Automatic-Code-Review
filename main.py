"""
main.py
-------
Entry point for the Multi-Agent Automatic Code Review system.

Usage:
    python main.py --file code_changes.txt
    python main.py --file code_changes.txt --output report.txt
"""

import argparse
import os
import sys

from dotenv import load_dotenv
from crewai import Crew, LLM

from tools import create_tools
from agents import create_senior_developer, create_security_engineer, create_tech_lead
from tasks import (
    create_quality_analysis_task,
    create_security_review_task,
    create_review_decision_task,
)


def setup_environment():
    """Load .env file and validate required API keys."""
    load_dotenv()

    missing = [v for v in ["OPENAI_API_KEY", "SERPER_API_KEY"] if not os.getenv(v)]
    if missing:
        print(f"[Error] Missing environment variables: {', '.join(missing)}")
        print("Add them to your .env file. See README for details.")
        sys.exit(1)


def build_crew(llm: LLM) -> Crew:
    """Assemble tools, agents, tasks, and return a ready Crew."""
    # Tools
    serper_tool, scrape_tool = create_tools()

    # Agents
    senior_developer = create_senior_developer(llm)
    security_engineer = create_security_engineer(llm, tools=[serper_tool, scrape_tool])
    tech_lead = create_tech_lead(llm)

    # Tasks
    quality_task = create_quality_analysis_task(agent=senior_developer)
    security_task = create_security_review_task(agent=security_engineer)
    decision_task = create_review_decision_task(
        agent=tech_lead,
        quality_task=quality_task,
        security_task=security_task,
    )

    return Crew(
        agents=[senior_developer, security_engineer, tech_lead],
        tasks=[quality_task, security_task, decision_task],
    )


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Automatic Code Review")
    parser.add_argument("--file", required=True, help="Path to code changes file.")
    parser.add_argument("--output", default=None, help="Optional path to save the report.")
    args = parser.parse_args()

    # Setup
    setup_environment()

    if not os.path.exists(args.file):
        print(f"[Error] File not found: {args.file}")
        sys.exit(1)

    with open(args.file, "r") as f:
        code_changes = f.read()

    print(f"\n[Main] Loaded {len(code_changes)} characters of code changes.")

    # LLM
    llm = LLM(model=os.getenv("MODEL", "gpt-4o-mini"))

    # Build & run
    crew = build_crew(llm)
    result = crew.kickoff(inputs={"code_changes": code_changes})

    # Display
    sep = "\n" + "=" * 60 + "\n"
    quality  = result.tasks_output[0].raw
    security = result.tasks_output[1].raw
    decision = result.tasks_output[2].raw

    print(sep + "QUALITY ANALYSIS" + sep + quality)
    print(sep + "SECURITY REVIEW"  + sep + security)
    print(sep + "FINAL DECISION"   + sep + decision)

    # Save
    if args.output:
        report = (
            "=== QUALITY ANALYSIS ===\n" + quality +
            "\n\n=== SECURITY REVIEW ===\n" + security +
            "\n\n=== FINAL DECISION ===\n" + decision
        )
        with open(args.output, "w") as f:
            f.write(report)
        print(f"\n[Main] Report saved to: {args.output}")


if __name__ == "__main__":
    main()
