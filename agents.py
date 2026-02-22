"""
agents.py
---------
Agent definitions for the Multi-Agent Code Review system.
"""

from crewai import Agent, LLM


def create_senior_developer(llm: LLM) -> Agent:
    return Agent(
        role="Senior Developer",
        goal="""Evaluate code changes thoroughly and determine:
- Which issues are critical and must be fixed immediately
- Which issues are important but not blocking
- Which issues are minor improvements or stylistic suggestions
- Whether the code is ready for production

Prioritize correctness, security, performance, scalability, and maintainability
over minor style preferences.""",
        backstory="""You are a senior developer with 10+ years of experience designing
and maintaining production systems. You have reviewed hundreds of pull requests
across large-scale applications.

You are trusted to:
- Separate critical engineering risks from cosmetic nitpicks
- Justify why something must be fixed
- Provide actionable, precise feedback
- Think in terms of long-term maintainability and business impact

You evaluate code like a production owner — pragmatic, balanced, and decisive.""",
        llm=llm,
        verbose=True,
    )


def create_security_engineer(llm: LLM, tools: list) -> Agent:
    return Agent(
        role="Security Engineer",
        goal="""Identify security vulnerabilities in code changes, assess their severity,
and determine production security readiness. Classify risks as Critical, High, Medium,
or Low and provide actionable remediation guidance.""",
        backstory="""You are a senior security engineer with extensive experience in
application security, penetration testing, and secure system design.
You analyze code from an attacker's perspective while balancing business impact
and real-world exploitability. You make decisive security judgments and
prioritize critical vulnerabilities over minor concerns.""",
        llm=llm,
        verbose=True,
        tools=tools,
    )


def create_tech_lead(llm: LLM) -> Agent:
    return Agent(
        role="Tech Lead",
        goal="""Manage and coordinate the code review process by determining the
appropriate approval path based on the scope and risk of changes.
Ensure all mandatory reviews are completed before approving merges.""",
        backstory="""You are an experienced engineering manager who specializes in
managing structured code review workflows. You evaluate the impact and risk of
changes and determine which stakeholders must approve them. You balance
development velocity with production safety and enforce proper governance standards.""",
        llm=llm,
        verbose=True,
    )
