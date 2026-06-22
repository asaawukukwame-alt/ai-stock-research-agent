\# AI Stock Research Agent



A LangGraph-powered AI stock research agent that gathers SEC EDGAR fundamentals, Yahoo Finance market data, recent news headlines, and generates structured tension-point research briefs using GPT-4o.



\## Features



\- SEC EDGAR financial data retrieval

\- Yahoo Finance market data retrieval

\- Recent news headline collection

\- LangGraph state-machine pipeline

\- Pydantic structured output schema

\- GPT-4o analysis

\- CLI interface

\- Streamlit web app



\## Tech Stack



\- Python

\- LangGraph

\- LangChain OpenAI

\- OpenAI GPT-4o

\- Pydantic

\- yfinance

\- SEC EDGAR API

\- Streamlit



\## Project Files



\- `tools.py` — SEC, market data, and news tools

\- `schemas.py` — Pydantic output schemas

\- `agent.py` — LangGraph pipeline

\- `main.py` — command-line interface

\- `app.py` — Streamlit web app



\## Run Locally



Install dependencies:



```bash

pip install -r requirements.txt

