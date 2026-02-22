"""
app.py
------
Streamlit interface for the Multi-Agent Automatic Code Review system.

Run with:
    streamlit run app.py
"""

import os
import sys
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CodeReview AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg:        #0c0e14;
    --surface:   #13161f;
    --border:    #1e2230;
    --accent:    #00e5ff;
    --accent2:   #7c3aed;
    --success:   #22c55e;
    --warning:   #f59e0b;
    --danger:    #ef4444;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --card:      #161b27;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Hide default header */
header[data-testid="stHeader"] { display: none; }

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,229,255,0.1) !important;
}

/* Labels */
.stTextInput label, .stTextArea label, .stFileUploader label {
    color: var(--muted) !important;
    font-size: 11px !important;
    font-family: 'JetBrains Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--card) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent2), #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.04em;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.4) !important;
}
.stButton > button:disabled {
    opacity: 0.4 !important;
    transform: none !important;
}

/* Expanders */
.streamlit-expanderHeader {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}
.streamlit-expanderContent {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Spinner */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* Custom components */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    line-height: 1.1;
    background: linear-gradient(135deg, #00e5ff 0%, #7c3aed 60%, #e879f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}

.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--muted);
    letter-spacing: 0.1em;
    margin-top: 6px;
}

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-critical { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.badge-high     { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
.badge-medium   { background: rgba(251,191,36,0.12); color: #fde68a; border: 1px solid rgba(251,191,36,0.2); }
.badge-low      { background: rgba(34,197,94,0.12);  color: #86efac; border: 1px solid rgba(34,197,94,0.2); }
.badge-approved { background: rgba(34,197,94,0.15);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.badge-block    { background: rgba(239,68,68,0.15);  color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
}

.result-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 12px;
}

.result-card.accent-cyan  { border-left: 3px solid var(--accent); }
.result-card.accent-purple { border-left: 3px solid var(--accent2); }
.result-card.accent-green  { border-left: 3px solid var(--success); }

.issue-item {
    background: rgba(30,34,48,0.6);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 14px;
    margin: 6px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    line-height: 1.6;
}

.decision-box {
    background: linear-gradient(135deg, rgba(0,229,255,0.05), rgba(124,58,237,0.08));
    border: 1px solid rgba(0,229,255,0.2);
    border-radius: 12px;
    padding: 24px;
    margin-top: 8px;
}

.metric-row {
    display: flex;
    gap: 12px;
    margin: 12px 0;
}

.metric-box {
    flex: 1;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 16px;
    text-align: center;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--accent);
}
.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <p class="section-label">⚙ Configuration</p>
    """, unsafe_allow_html=True)

    gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza...",
        value=os.getenv("GEMINI_API_KEY", ""),
    )

    serper_key = st.text_input(
        "Serper API Key",
        type="password",
        placeholder="Your Serper key",
        value=os.getenv("SERPER_API_KEY", ""),
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    model = st.selectbox(
        "Gemini Model",
        ["gemini/gemini-2.0-flash", "gemini/gemini-1.5-pro", "gemini/gemini-1.5-flash"],
        index=0,
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    keys_ok = bool(gemini_key and serper_key)
    if keys_ok:
        st.markdown("""
        <div style="background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.3);
             border-radius:8px;padding:10px 14px;font-family:'JetBrains Mono',monospace;
             font-size:11px;color:#4ade80;">
        ✓ API keys configured
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.3);
             border-radius:8px;padding:10px 14px;font-family:'JetBrains Mono',monospace;
             font-size:11px;color:#fbbf24;">
        ⚠ Enter both API keys to proceed
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:24px; font-family:'JetBrains Mono',monospace; font-size:10px; color:#334155; line-height:1.8;">
    AGENTS<br>
    ├─ Senior Developer<br>
    ├─ Security Engineer<br>
    └─ Tech Lead<br>
    <br>
    POWERED BY<br>
    └─ CrewAI + Gemini
    </div>
    """, unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 32px 0 20px 0;">
    <p class="hero-title">CodeReview AI</p>
    <p class="hero-sub">// multi-agent automated code review system</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Upload ────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">📂 Upload Code Changes</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop your code_changes.txt or diff file here",
    type=["txt", "diff", "patch", "py", "js", "ts", "java", "go"],
    label_visibility="collapsed",
)

code_preview = None
if uploaded_file:
    code_preview = uploaded_file.read().decode("utf-8", errors="replace")
    with st.expander(f"📄 Preview — {uploaded_file.name}  ({len(code_preview):,} chars)", expanded=False):
        st.code(code_preview[:3000] + ("\n\n... [truncated]" if len(code_preview) > 3000 else ""), language="diff")

st.markdown("<br>", unsafe_allow_html=True)

run_disabled = not (keys_ok and code_preview)
run_btn = st.button(
    "⚡  Run Code Review",
    disabled=run_disabled,
    use_container_width=True,
)

if not keys_ok:
    st.caption("← Add your API keys in the sidebar to get started.")
elif not code_preview:
    st.caption("Upload a file above to begin.")


# ── Run ───────────────────────────────────────────────────────────────────────
if run_btn and code_preview and keys_ok:

    # Set keys in env so CrewAI picks them up
    os.environ["GEMINI_API_KEY"]  = gemini_key
    os.environ["SERPER_API_KEY"]  = serper_key
    os.environ["OPENAI_API_KEY"]  = gemini_key   # crewai sometimes checks this
    os.environ["MODEL"]           = model

    # Import here so env vars are set before crewai initialises
    from crewai import Crew, LLM
    from tools import create_tools
    from agents import create_senior_developer, create_security_engineer, create_tech_lead
    from tasks import (
        create_quality_analysis_task,
        create_security_review_task,
        create_review_decision_task,
    )

    progress_placeholder = st.empty()
    result_placeholder   = st.empty()

    with progress_placeholder.container():
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<p class="section-label">🤖 Agent Activity</p>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            s1 = st.status("Senior Developer", expanded=True)
            s1.write("Analyzing code quality...")
        with col2:
            s2 = st.status("Security Engineer", expanded=True)
            s2.write("Scanning for vulnerabilities...")
        with col3:
            s3 = st.status("Tech Lead", expanded=True)
            s3.write("Awaiting agent reports...")

    try:
        llm = LLM(model=model, api_key=gemini_key)

        serper_tool, scrape_tool = create_tools()
        senior_developer  = create_senior_developer(llm)
        security_engineer = create_security_engineer(llm, tools=[serper_tool, scrape_tool])
        tech_lead         = create_tech_lead(llm)

        quality_task  = create_quality_analysis_task(agent=senior_developer)
        security_task = create_security_review_task(agent=security_engineer)
        decision_task = create_review_decision_task(
            agent=tech_lead,
            quality_task=quality_task,
            security_task=security_task,
        )

        crew = Crew(
            agents=[senior_developer, security_engineer, tech_lead],
            tasks=[quality_task, security_task, decision_task],
        )

        result = crew.kickoff(inputs={"code_changes": code_preview})

        # Update status badges
        with progress_placeholder.container():
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<p class="section-label">🤖 Agent Activity</p>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                s1 = st.status("Senior Developer", state="complete", expanded=False)
                s1.write("Quality analysis complete.")
            with col2:
                s2 = st.status("Security Engineer", state="complete", expanded=False)
                s2.write("Security review complete.")
            with col3:
                s3 = st.status("Tech Lead", state="complete", expanded=False)
                s3.write("Decision rendered.")

        quality_raw  = result.tasks_output[0].raw
        security_raw = result.tasks_output[1].raw
        decision_raw = result.tasks_output[2].raw

        # ── Parse JSON safely ──
        def safe_parse(raw: str) -> dict | None:
            try:
                clean = raw.strip()
                if clean.startswith("```"):
                    clean = clean.split("```")[1]
                    if clean.startswith("json"):
                        clean = clean[4:]
                return json.loads(clean.strip())
            except Exception:
                return None

        quality_json  = safe_parse(quality_raw)
        security_json = safe_parse(security_raw)

        # ── Results ──────────────────────────────────────────────────────────
        with result_placeholder.container():
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown('<p class="section-label">📊 Review Results</p>', unsafe_allow_html=True)

            # Metrics row
            n_critical = len(quality_json.get("critical_issues", [])) if quality_json else "–"
            n_minor    = len(quality_json.get("minor_issues", []))    if quality_json else "–"
            highest    = security_json.get("highest_risk", "–")       if security_json else "–"
            blocking   = security_json.get("blocking", None)          if security_json else None

            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-box">
                    <div class="metric-value" style="color:#f87171;">{n_critical}</div>
                    <div class="metric-label">Critical Issues</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value" style="color:#fbbf24;">{n_minor}</div>
                    <div class="metric-label">Minor Issues</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value" style="color:{'#f87171' if highest in ('Critical','High') else '#4ade80'};">{highest}</div>
                    <div class="metric-label">Highest Risk</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value" style="color:{'#f87171' if blocking else '#4ade80'};">{'BLOCK' if blocking else 'PASS'}</div>
                    <div class="metric-label">Security Gate</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["🧑‍💻  Quality Analysis", "🔐  Security Review", "✅  Final Decision"])

            # ── Tab 1: Quality ────────────────────────────────────────────────
            with tab1:
                if quality_json:
                    critical = quality_json.get("critical_issues", [])
                    minor    = quality_json.get("minor_issues", [])
                    reasoning = quality_json.get("reasoning", "")

                    if critical:
                        st.markdown('<p class="section-label" style="color:#f87171;">🔴 Critical Issues</p>', unsafe_allow_html=True)
                        for issue in critical:
                            st.markdown(f'<div class="issue-item" style="border-left:3px solid #ef4444;">{issue}</div>', unsafe_allow_html=True)

                    if minor:
                        st.markdown('<p class="section-label" style="color:#fbbf24;margin-top:16px;">🟡 Minor Issues</p>', unsafe_allow_html=True)
                        for issue in minor:
                            st.markdown(f'<div class="issue-item" style="border-left:3px solid #f59e0b;">{issue}</div>', unsafe_allow_html=True)

                    if reasoning:
                        st.markdown('<p class="section-label" style="margin-top:16px;">💡 Reasoning</p>', unsafe_allow_html=True)
                        st.markdown(f'<div class="result-card accent-cyan">{reasoning}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="section-label">Raw Output</p>', unsafe_allow_html=True)
                    st.code(quality_raw, language="markdown")

            # ── Tab 2: Security ───────────────────────────────────────────────
            with tab2:
                if security_json:
                    vulns = security_json.get("security_vulnerabilities", [])
                    recs  = security_json.get("security_recommendations", [])

                    if vulns:
                        st.markdown('<p class="section-label">🛡 Vulnerabilities Found</p>', unsafe_allow_html=True)
                        for v in vulns:
                            if isinstance(v, dict):
                                risk = v.get("risk_level", v.get("severity", "")).lower()
                                badge_cls = {"critical":"badge-critical","high":"badge-high","medium":"badge-medium","low":"badge-low"}.get(risk,"badge-low")
                                desc = v.get("description", v.get("issue", str(v)))
                                st.markdown(f"""
                                <div class="issue-item">
                                    <span class="badge {badge_cls}">{risk or 'unknown'}</span>
                                    <span style="margin-left:10px;">{desc}</span>
                                </div>""", unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="issue-item">{v}</div>', unsafe_allow_html=True)

                    blocking_val = security_json.get("blocking", False)
                    st.markdown(f"""
                    <div class="result-card {'accent-purple' if blocking_val else 'accent-green'}" style="margin-top:16px;">
                        <span class="badge {'badge-block' if blocking_val else 'badge-approved'}">
                            {'🚫 BLOCKING' if blocking_val else '✅ NON-BLOCKING'}
                        </span>
                        &nbsp; Highest Risk: <strong>{security_json.get('highest_risk','–')}</strong>
                    </div>""", unsafe_allow_html=True)

                    if recs:
                        st.markdown('<p class="section-label" style="margin-top:16px;">🔧 Recommendations</p>', unsafe_allow_html=True)
                        for r in recs:
                            st.markdown(f'<div class="issue-item" style="border-left:3px solid #7c3aed;">{r}</div>', unsafe_allow_html=True)
                else:
                    st.code(security_raw, language="markdown")

            # ── Tab 3: Decision ───────────────────────────────────────────────
            with tab3:
                st.markdown(f'<div class="decision-box">{decision_raw}</div>', unsafe_allow_html=True)

                # Download button
                full_report = (
                    "=== QUALITY ANALYSIS ===\n" + quality_raw +
                    "\n\n=== SECURITY REVIEW ===\n" + security_raw +
                    "\n\n=== FINAL DECISION ===\n" + decision_raw
                )
                st.download_button(
                    label="⬇  Download Full Report",
                    data=full_report,
                    file_name="code_review_report.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

    except Exception as e:
        with progress_placeholder.container():
            st.markdown("<hr>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                s = st.status("Senior Developer", state="error", expanded=False)
            with col2:
                s = st.status("Security Engineer", state="error", expanded=False)
            with col3:
                s = st.status("Tech Lead", state="error", expanded=False)

        st.error(f"**Review failed:** {str(e)}")
        with st.expander("Full traceback"):
            import traceback
            st.code(traceback.format_exc())
