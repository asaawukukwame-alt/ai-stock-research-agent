import os

import streamlit as st
from dotenv import load_dotenv

from agent import build_graph


load_dotenv()

# Local mode uses .env.
# Streamlit Cloud mode can use st.secrets later.
try:
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

    if "OPENAI_MODEL" in st.secrets:
        os.environ["OPENAI_MODEL"] = st.secrets["OPENAI_MODEL"]
except Exception:
    pass


st.set_page_config(
    page_title="AI Stock Research Agent",
    page_icon="📈",
    layout="wide",
)

st.title("📈 AI Stock Research Agent")

st.write(
    "Enter a stock ticker and generate a structured tension-point research brief "
    "using SEC EDGAR data, Yahoo Finance market data, recent news headlines, "
    "LangGraph, and GPT-4o."
)

ticker = st.text_input("Stock ticker", value="AAPL").upper().strip()

run_button = st.button("Run Research Agent")

if run_button:
    if not ticker:
        st.error("Please enter a ticker symbol.")
    else:
        with st.spinner(f"Researching {ticker}..."):
            try:
                graph = build_graph()
                result = graph.invoke({"ticker": ticker})
                brief = result["research_brief"]

                st.subheader(
                    f"Tension Point Analysis: {brief.company_name} ({brief.ticker})"
                )

                col1, col2 = st.columns(2)
                col1.metric("Recommendation", brief.recommendation)
                col2.metric("Conviction", brief.conviction)

                st.markdown("## Fundamental Snapshot")
                st.write(brief.fundamental_snapshot)

                st.markdown("## Tension Points")
                for i, tp in enumerate(brief.tension_points, 1):
                    with st.expander(
                        f"Tension Point #{i}: {tp.debate}",
                        expanded=True,
                    ):
                        st.markdown("**Bull Case**")
                        st.write(tp.bull_case)

                        st.markdown("**Bear Case**")
                        st.write(tp.bear_case)

                        st.markdown("**What to Watch**")
                        st.write(tp.what_to_watch)

                st.markdown("## Final Verdict")
                st.write(brief.final_verdict)

                st.caption("Educational research only. Not financial advice.")

            except Exception as error:
                st.error("The agent failed to run.")
                st.code(str(error))