# config.py
import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

def get_llm(model: str | None = None, api_key: str | None = None) -> LLM:
    return LLM(
        model=model or os.getenv("MODEL", "gemini/gemini-2.0-flash"),
        api_key=api_key or os.getenv("GEMINI_API_KEY"),
        temperature=0.2,
    )


