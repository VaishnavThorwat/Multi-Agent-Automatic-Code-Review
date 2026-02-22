"""
tasks.py
--------
Task definitions for the Multi-Agent Code Review system.
"""

from crewai import Task, Agent


def create_quality_analysis_task(agent: Agent) -> Task:
    return Task(
        name="Analyze Code Quality",
        description="""Review the following code changes:

{code_changes}

Perform a comprehensive code quality evaluation:
1. Identify potential logical bugs, edge cases, or incorrect implementations.
2. Detect performance concerns, scalability risks, and inefficient patterns.
3. Evaluate maintainability, readability, and adherence to clean architecture.
4. Identify violations of best practices or coding standards.
5. Classify each issue as critical (must fix before merge) or minor (non-blocking suggestion).
6. Justify your classification decisions clearly.""",
        expected_output="""A JSON object with exactly the following keys:
- critical_issues: array of issues that must be fixed
- minor_issues: array of suggested improvements
- reasoning: explanation of decisions""",
        agent=agent,
    )


def create_security_review_task(agent: Agent) -> Task:
    return Task(
        name="Review Security",
        description="""Examine the following code changes:

{code_changes}

Perform a thorough security evaluation:
1. Analyze code from an attacker's perspective.
2. Identify vulnerabilities such as injection flaws, auth weaknesses, sensitive data
   exposure, hardcoded secrets, insecure input handling, and insecure API usage.
3. Use SerperDevTool to find relevant OWASP best practices, then ScrapeWebsiteTool
   to retrieve full guidance from those URLs.
4. Compare findings against OWASP standards.
5. Classify each issue: Critical, High, Medium, or Low.
6. Determine whether any issue should block approval.
7. Provide specific, actionable remediation steps.""",
        expected_output="""A JSON object with exactly the following keys:
- security_vulnerabilities: array of identified issues with risk levels
- blocking: boolean indicating if security issues should block approval
- highest_risk: the most severe risk level found
- security_recommendations: specific fixes for vulnerabilities""",
        agent=agent,
    )


def create_review_decision_task(
    agent: Agent,
    quality_task: Task,
    security_task: Task,
) -> Task:
    return Task(
        name="Review Decision",
        description="""Review the following pull request code changes:

{code_changes}

Using the outputs from the Quality Analysis and Security Review tasks:
1. Assess critical quality issues and blocking security vulnerabilities.
2. Evaluate overall production readiness.
3. Decide whether the PR should be:
   - Approved
   - Approved with conditions
   - Request Changes
   - Escalated to human reviewer
4. Explain your reasoning and provide next steps for the developer.""",
        expected_output="""A short report containing:
- Final decision
- Required changes (if any)
- Approval comments (if approving)
- Escalation reasoning (if escalating)
- Additional recommendations""",
        agent=agent,
        context=[quality_task, security_task],
    )
