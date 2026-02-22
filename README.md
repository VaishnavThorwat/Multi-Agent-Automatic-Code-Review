# Multi-Agent Automatic Code Review

A production-style AI pipeline that automatically reviews pull requests using **three specialized agents** built with [CrewAI](https://crewai.com).

---

## Project Structure

```
code_review_crew/
├── app.py        # Streamlit web interface
├── main.py       # CLI entry point
├── agents.py     # Senior Developer, Security Engineer, Tech Lead
├── tasks.py      # Quality Analysis, Security Review, Review Decision
├── tools.py      # SerperDevTool (OWASP search) + ScrapeWebsiteTool
├── .env          # Your API keys (never commit this)
└── README.md
```

---

## Agents & Flow

```
Senior Developer  →  Quality Analysis Task  ──┐
Security Engineer →  Security Review Task   ──┼──▶  Tech Lead  →  Final Decision
                     (uses OWASP via tools)   ┘
```

---

## Setup

### 1. Install dependencies
```bash
pip install crewai[tools]==1.3.0 python-dotenv streamlit
```

### 2. Create a `.env` file (optional — keys can also be entered in the UI)
```env
GEMINI_API_KEY=your_gemini_key
SERPER_API_KEY=your_serper_key
```

### 3. Launch the Streamlit UI
```bash
streamlit run app.py
```

### 4. Or use the CLI
```bash
python main.py --file code_changes.txt --output report.txt
```

---

## Output

Each run produces three outputs:

| Task | Agent | Output Format |
|---|---|---|
| Quality Analysis | Senior Developer | JSON: `critical_issues`, `minor_issues`, `reasoning` |
| Security Review | Security Engineer | JSON: `security_vulnerabilities`, `blocking`, `highest_risk`, `security_recommendations` |
| Review Decision | Tech Lead | Markdown report: final decision, required changes, recommendations |
