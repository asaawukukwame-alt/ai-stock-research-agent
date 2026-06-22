import json
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from schemas import ResearchBrief
from tools import get_market_data, get_sec_fundamentals, get_news_sentiment

load_dotenv()


class AgentState(TypedDict, total=False):
    ticker: str
    fundamentals: dict
    market_data: dict
    news_sentiment: dict
    research_brief: ResearchBrief


ANALYSIS_SYSTEM_PROMPT = """You are an expert buy-side equity research analyst at a top hedge fund.
You produce "tension point" analyses - identifying the 1-3 core debates that drive a stock's valuation.

A tension point is NOT a generic risk. It is the specific, current question that investors are
actively debating right now. For example:
- "Can NVDA maintain 70%+ data center growth as hyperscaler capex normalizes?"
- "Will AAPL's services revenue acceleration offset iPhone unit decline?"
- "Is TSLA a car company at 60x earnings or a robotics/AI company worth 100x?"

Your job is to identify these precise debates from the financial data provided and synthesize
them into a structured research brief.

Also compare recent news headlines against the financial data. Identify where the market
narrative agrees with or diverges from the fundamentals.

Be specific. Use actual numbers from the data. Never be generic."""


def gather_data(state: AgentState) -> dict:
    """Gather financial data from SEC EDGAR, Yahoo Finance, and recent news headlines."""
    ticker = state["ticker"]

    fundamentals = get_sec_fundamentals.invoke({"ticker": ticker})
    market_data = get_market_data.invoke({"ticker": ticker})
    news_sentiment = get_news_sentiment.invoke({"ticker": ticker})

    return {
        "fundamentals": fundamentals,
        "market_data": market_data,
        "news_sentiment": news_sentiment,
    }


def analyze(state: AgentState) -> dict:
    """Analyze gathered data and produce a structured research brief."""
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o"), temperature=0.1)
    structured_llm = llm.with_structured_output(ResearchBrief)

    data_summary = f"""## SEC EDGAR Fundamentals
{json.dumps(state["fundamentals"], indent=2, default=str)}

## Yahoo Finance Market Data
{json.dumps(state["market_data"], indent=2, default=str)}

## Recent News Headlines
{json.dumps(state["news_sentiment"], indent=2, default=str)}"""

    messages = [
        SystemMessage(content=ANALYSIS_SYSTEM_PROMPT),
        HumanMessage(
            content=f"Produce a tension point analysis for {state['ticker']}.\n\n"
            f"Here is the financial data:\n\n{data_summary}"
        ),
    ]

    brief = structured_llm.invoke(messages)
    return {"research_brief": brief}


def build_graph():
    """Build and compile the research agent graph."""
    graph = StateGraph(AgentState)

    graph.add_node("gather_data", gather_data)
    graph.add_node("analyze", analyze)

    graph.add_edge(START, "gather_data")
    graph.add_edge("gather_data", "analyze")
    graph.add_edge("analyze", END)

    return graph.compile()