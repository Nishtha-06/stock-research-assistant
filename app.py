
import streamlit as st
from datetime import date
from pipeline import run_research_pipeline
 
# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Research Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Sora:wght@600;700&display=swap');
 
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
 
/* ── Background ── */
.stApp {
    background: #0A0F1E;
    color: #E8EAF0;
}
 
/* ── Hide Streamlit defaults ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }
 
/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid #1E2740;
    margin-bottom: 2.5rem;
}
.hero-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #4AE3A0;
    border: 1px solid #1A3D2E;
    background: #0D2620;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Sora', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #F0F2F8;
    margin: 0 0 0.6rem;
    line-height: 1.15;
}
.hero h1 span { color: #4AE3A0; }
.hero p {
    font-size: 15px;
    color: #7880A0;
    margin: 0;
    max-width: 500px;
    margin: 0 auto;
}
 
/* ── Input card ── */
.input-card {
    background: #111827;
    border: 1px solid #1E2740;
    border-radius: 14px;
    padding: 2rem;
    margin-bottom: 2rem;
}
.input-card h3 {
    font-size: 13px;
    font-weight: 500;
    color: #7880A0;
    letter-spacing: .06em;
    text-transform: uppercase;
    margin: 0 0 1.2rem;
}
 
/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: #0A0F1E !important;
    border: 1px solid #1E2740 !important;
    border-radius: 8px !important;
    color: #E8EAF0 !important;
    font-size: 15px !important;
    padding: 0.6rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4AE3A0 !important;
    box-shadow: 0 0 0 2px rgba(74,227,160,0.12) !important;
}
.stTextInput label {
    color: #9AA0BC !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
 
/* ── Analyse button ── */
.stButton > button {
    background: #4AE3A0 !important;
    color: #030A14 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 2.5rem !important;
    width: 100% !important;
    transition: opacity .18s !important;
    letter-spacing: .01em !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
}
 
/* ── Step progress cards ── */
.step-card {
    background: #111827;
    border: 1px solid #1E2740;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.step-num {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #1E2740;
    color: #7880A0;
    font-size: 12px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.step-num.active { background: #0D2620; color: #4AE3A0; border: 1px solid #1A3D2E; }
.step-num.done   { background: #4AE3A0; color: #030A14; }
.step-label { font-size: 13px; color: #7880A0; }
.step-label.active { color: #E8EAF0; font-weight: 500; }
.step-label.done   { color: #4AE3A0; }
 
/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 2rem 0 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #1E2740;
}
.section-header .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #4AE3A0;
    flex-shrink: 0;
}
.section-header h2 {
    font-family: 'Sora', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: #E8EAF0;
    margin: 0;
}
.section-header .badge {
    margin-left: auto;
    font-size: 11px;
    padding: 2px 10px;
    border-radius: 20px;
    background: #0D2620;
    color: #4AE3A0;
    border: 1px solid #1A3D2E;
    font-weight: 500;
    letter-spacing: .04em;
}
 
/* ── Agent output boxes ── */

/* ── Container styling ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111827 !important;
    border: 1px solid #1E2740 !important;
    border-radius: 12px !important;
}

[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] li {
    color: #C8CCE0 !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
}

[data-testid="stVerticalBlockBorderWrapper"] h3,
[data-testid="stVerticalBlockBorderWrapper"] h4 {
    color: #4AE3A0 !important;
}

[data-testid="stVerticalBlockBorderWrapper"] strong {
    color: #F0F2F8 !important;
}

[data-testid="stVerticalBlockBorderWrapper"] ul,
[data-testid="stVerticalBlockBorderWrapper"] ol {
    margin: 0.3rem 0 !important;
    padding-left: 1.2rem !important;
}

[data-testid="stVerticalBlockBorderWrapper"] li {
    margin-bottom: 0.3rem !important;
}
 
/* ── Score badge ── */
.score-badge {
    display: inline-block;
    font-family: 'Sora', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #F5A623;
    background: #1F1608;
    border: 1px solid #4A330A;
    border-radius: 10px;
    padding: 8px 18px;
    margin-bottom: 1rem;
}
 
/* ── Error box ── */
.error-box {
    background: #1A0A0A;
    border: 1px solid #4A1515;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    color: #F87171;
    font-size: 13px;
    margin-top: 1rem;
}
 
/* ── Ticker examples ── */
.examples {
    font-size: 12px;
    color: #4A5280;
    margin-top: 6px;
}
.examples span {
    display: inline-block;
    background: #111827;
    border: 1px solid #1E2740;
    border-radius: 6px;
    padding: 2px 8px;
    margin: 2px 3px;
    color: #7880A0;
    font-family: monospace;
    cursor: pointer;
}
 
/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid #1E2740 !important;
    color: #7880A0 !important;
    font-size: 13px !important;
    border-radius: 8px !important;
    padding: 0.4rem 1.2rem !important;
    transition: border-color .18s !important;
}
.stDownloadButton > button:hover {
    border-color: #4AE3A0 !important;
    color: #4AE3A0 !important;
}
 
/* ── Divider ── */
hr { border-color: #1E2740 !important; margin: 2rem 0 !important; }
</style>
""", unsafe_allow_html=True)
 
 
# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">Multi-Agent AI · Powered by Mistral</div>
    <h1>Stock Research <span>Agent</span></h1>
    <p>Five AI agents analyse price, fundamentals, news, financials — then write a professional report in seconds.</p>
</div>
""", unsafe_allow_html=True)
 
 
# ── Input card ─────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card"><h3>Research a stock</h3>', unsafe_allow_html=True)
 
col1, col2 = st.columns([1, 1])
with col1:
    ticker = st.text_input(
        "Stock ticker",
        placeholder="e.g. AAPL, RELIANCE.NS, TCS.NS",
        help="US stocks: AAPL, MSFT, TSLA. Indian stocks: add .NS suffix — RELIANCE.NS, TCS.NS, INFY.NS"
    )
    st.markdown("""
    <div class="examples">
        Try: <span>AAPL</span><span>TSLA</span><span>RELIANCE.NS</span><span>TCS.NS</span><span>INFY.NS</span>
    </div>
    """, unsafe_allow_html=True)
 
with col2:
    company_name = st.text_input(
        "Company name",
        placeholder="e.g. Apple, Reliance Industries",
        help="Used to search for news — use the full company name for better results"
    )
 
st.markdown("</div>", unsafe_allow_html=True)
 
run_btn = st.button("Analyse Stock →", use_container_width=False)
 
 
# ── Validation ─────────────────────────────────────────────────────────────────
if run_btn:
    if not ticker.strip():
        st.markdown('<div class="error-box">⚠ Please enter a stock ticker (e.g. AAPL or RELIANCE.NS)</div>', unsafe_allow_html=True)
        st.stop()
    if not company_name.strip():
        st.markdown('<div class="error-box">⚠ Please enter the company name (e.g. Apple or Reliance Industries)</div>', unsafe_allow_html=True)
        st.stop()
 
    ticker = ticker.strip().upper()
    company_name = company_name.strip()
 
    # ── Step progress UI ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div class="section-header">
        <div class="dot"></div>
        <h2>Running analysis</h2>
    </div>
    """, unsafe_allow_html=True)
 
    steps = [
        ("Price agent", "Fetching live price and market data"),
        ("Fundamentals agent", "Analysing P/E, EPS, margins, ROE"),
        ("News agent", "Gathering latest news via web search"),
        ("Report writer", "Drafting the research report"),
        ("Critic agent", "Reviewing and scoring the report"),
    ]
 
    step_placeholders = []
    for i, (title, desc) in enumerate(steps):
        ph = st.empty()
        ph.markdown(f"""
        <div class="step-card">
            <div class="step-num">{i+1}</div>
            <div class="step-label">{title} — {desc}</div>
        </div>
        """, unsafe_allow_html=True)
        step_placeholders.append(ph)
 
    def update_step(idx, state):
        title, desc = steps[idx]
        if state == "active":
            step_placeholders[idx].markdown(f"""
            <div class="step-card">
                <div class="step-num active">{idx+1}</div>
                <div class="step-label active">⟳ {title} — {desc}...</div>
            </div>
            """, unsafe_allow_html=True)
        elif state == "done":
            step_placeholders[idx].markdown(f"""
            <div class="step-card">
                <div class="step-num done">✓</div>
                <div class="step-label done">{title} — complete</div>
            </div>
            """, unsafe_allow_html=True)
 
    # ── Run pipeline step by step ──────────────────────────────────────────────
    try:
        from agents import (
            build_price_agent, build_details_agent,
            build_news_agent, report_chain, critic_chain
        )
 
        state = {}
        today_str = date.today().strftime("%B %d, %Y")
 
        # Step 1 — Price
        update_step(0, "active")
        price_agent = build_price_agent()
        price_result = price_agent.invoke({
            "messages": [("user", f"Get current price and market data for {ticker}")]
        })
        state["price_data"] = price_result["messages"][-1].content
        update_step(0, "done")
 
        # Step 2 — Fundamentals
        update_step(1, "active")
        detail_agent = build_details_agent()
        details_result = detail_agent.invoke({
            "messages": [("user", f"Get fundamental and valuation data for {ticker}")]
        })
        state["fundamentals"] = details_result["messages"][-1].content
        update_step(1, "done")
 
        # Step 3 — News
        update_step(2, "active")
        news_agent = build_news_agent()
        news_result = news_agent.invoke({
            "messages": [("user", f"Get the latest news and sentiment about {company_name}")]
        })
        state["news"] = news_result["messages"][-1].content
        update_step(2, "done")
 
        # Step 4 — Report (date bug fixed here)
        update_step(3, "active")
        state["report"] = report_chain.invoke({
            "ticker": ticker,
            "today": today_str,        # ← fixes the date hallucination
            "price_data": state["price_data"],
            "fundamentals": state["fundamentals"],
            "news": state["news"],
        })
        update_step(3, "done")
 
        # Step 5 — Critic
        update_step(4, "active")
        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })
        update_step(4, "done")
 
        # ── Results ─────────────────────────────────────────────────────────────
        st.markdown("---")
 
        # ── Agent outputs (collapsible) ─────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <div class="dot"></div>
            <h2>Agent outputs</h2>
            <span class="badge">Raw data</span>
        </div>
        """, unsafe_allow_html=True)
 
        with st.expander("📊 Price data", expanded=False):
            st.markdown(f'<div class="agent-box">{state["price_data"]}</div>', unsafe_allow_html=True)
 
        with st.expander("📋 Fundamentals", expanded=False):
            st.markdown(f'<div class="agent-box">{state["fundamentals"]}</div>', unsafe_allow_html=True)
 
        with st.expander("📰 News & sentiment", expanded=False):
            st.markdown(f'<div class="agent-box">{state["news"]}</div>', unsafe_allow_html=True)
 
        # ── Final report ────────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="section-header">
            <div class="dot"></div>
            <h2>Research report — {ticker}</h2>
            <span class="badge">{today_str}</span>
        </div>
        """, unsafe_allow_html=True)
 
        st.markdown(f'<div class="report-box">{state["report"]}</div>', unsafe_allow_html=True)
 
        # ── Critic review ───────────────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <div class="dot"></div>
            <h2>Critic review</h2>
            <span class="badge" style="background:#1F1608;color:#F5A623;border-color:#4A330A;">AI quality check</span>
        </div>
        """, unsafe_allow_html=True)
 
        # Extract score from critic feedback for display
        feedback_text = state["feedback"]
        score_line = ""
        for line in feedback_text.split("\n"):
            if line.strip().startswith("Score:"):
                score_line = line.replace("Score:", "").strip()
                break
 
        if score_line:
            st.markdown(f'<div class="score-badge">Score: {score_line}</div>', unsafe_allow_html=True)
 
        st.markdown(f'<div class="critic-box">{feedback_text}</div>', unsafe_allow_html=True)
 
        # ── Download button ─────────────────────────────────────────────────────
        st.markdown("---")
 
        full_output = f"""# Stock Research Report: {ticker}
Date: {today_str}
 
---
 
## Research Report
 
{state['report']}
 
---
 
## Critic Feedback
 
{state['feedback']}
 
---
 
## Agent Outputs
 
### Price Data
{state['price_data']}
 
### Fundamentals
{state['fundamentals']}
 
### News & Sentiment
{state['news']}
"""
 
        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_b:
            st.download_button(
                label="⬇ Download full report (.md)",
                data=full_output,
                file_name=f"{ticker}_research_{date.today().strftime('%Y%m%d')}.md",
                mime="text/markdown",
            )
 
    except Exception as e:
        st.markdown(f"""
        <div class="error-box">
            <strong>Something went wrong:</strong><br>{str(e)}<br><br>
            Common fixes:<br>
            • Check your MISTRAL_API_KEY and TAVILY_API_KEY in .env<br>
            • For Indian stocks use .NS suffix (e.g. RELIANCE.NS)<br>
            • Check your internet connection
        </div>
        """, unsafe_allow_html=True)
 
 
# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#2E3555; font-size:12px; padding-bottom:1rem;">
    Built with Mistral AI · LangChain · yfinance · Tavily · Streamlit
</div>
""", unsafe_allow_html=True)