"""
tools.py
--------
Tool instances used by agents in the Multi-Agent Code Review system.
"""

import os
from crewai_tools import ScrapeWebsiteTool, SerperDevTool


def create_tools():
    """
    Instantiate and return the OWASP search and web scraping tools.

    Returns:
        tuple: (serper_search_tool, scrape_website_tool)
    """
    serper_search_tool = SerperDevTool(
        search_url="https://owasp.org",
    )
    scrape_website_tool = ScrapeWebsiteTool()

    return serper_search_tool, scrape_website_tool
