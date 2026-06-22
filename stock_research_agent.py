import os
import json
from typing import Any, TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage

from tools import get_sec_financial_data, get_yahoo_finance_data


load_dotenv()


class StockResearchState(TypedDict, total=False):
    ticker: str
    sec_data: dict[str, Any]
    yahoo_data: dict[str, Any]
    research_brief: str
    error: str


def gather_financial_data(state: StockResearchState) -> StockResearchState:
    """
    Node 1:
    Gather financial data from SEC EDGAR and Yahoo Finance.
    """
    ticker = state["ticker"].upper().strip()

    print(f"\nGathering SEC and Yahoo Finance data for {ticker}...")

    sec_data = get_sec_financial_data.invoke({"ticker": ticker})
    yahoo_data = get_yahoo_finance_data.invoke({"ticker": ticker})

    return {
        **state,
        "ticker": ticker,
        "sec_data": sec_data,
        "yahoo_data": yahoo_data,
    }


def analyze_financial_data(state: StockResearchState) -> StockResearchState:
    """
    Node 2:
    Use GPT to analyze the gathered financial data.
    """
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o")

    ticker = state["ticker"]
    sec_data = state["sec_data"]
    yahoo_data = state["yahoo_data"]

    system_prompt = """
You are a careful financial research assistant.

You analyze stock data for educational purposes only.
Do not tell the user to buy, sell, or hold.
Do not give personalized financial advice.
Explain the data clearly for a beginner.
"""

    user_prompt = f"""
Create a structured stock research brief for ticker: {ticker}

Use this official SEC filing data:
{json.dumps(sec_data, indent=2, default=str)}

Use this Yahoo Finance market data:
{json.dumps(yahoo_data, indent=2, default=str)}

Format the answer exactly like this:

# Stock Research Brief: {ticker}

## 1. Company Snapshot
Explain what the company does, its sector, and industry.

## 2. SEC Filing Highlights
Summarize revenue, net income, EPS, filing date, and what the numbers suggest.

## 3. Market Data
Summarize current price, one-month performance, market cap, P/E ratios, 52-week range, and target mean price.

## 4. Analyst Sentiment
Summarize recommendation key, analyst count, and recent recommendation mix.

## 5. Strengths
List the main positives shown by the data.

## 6. Risks
List the main risks or weaknesses shown by the data.

## 7. Beginner-Friendly Takeaway
Explain the stock in simple terms.

## 8. Disclaimer
Say this is educational research only and not financial advice.
"""

    print("\nAsking GPT to analyze the data...")

    try:
        llm = ChatOpenAI(
            model=model_name,
            temperature=0.2,
        )

        response = llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        )

        research_brief = response.content

    except Exception as error:
        research_brief = f"""
# Stock Research Brief: {ticker}

The SEC and Yahoo Finance data tools worked, but the GPT analysis step failed.

Error:
{error}

This usually means one of these issues:
1. OpenAI API billing or credits are not active.
2. The API key is missing or invalid.
3. The selected model is unavailable for the account.

The data-gathering part of the LangGraph agent still ran successfully.
"""

    return {
        **state,
        "research_brief": research_brief,
    }


def build_graph():
    """
    Build and compile the LangGraph workflow.
    """
    graph_builder = StateGraph(StockResearchState)

    graph_builder.add_node("gather_financial_data", gather_financial_data)
    graph_builder.add_node("analyze_financial_data", analyze_financial_data)

    graph_builder.add_edge(START, "gather_financial_data")
    graph_builder.add_edge("gather_financial_data", "analyze_financial_data")
    graph_builder.add_edge("analyze_financial_data", END)

    return graph_builder.compile()


def run_agent(ticker: str):
    """
    Run the stock research agent.
    """
    app = build_graph()

    final_state = app.invoke(
        {
            "ticker": ticker,
        }
    )

    return final_state


if __name__ == "__main__":
    ticker_input = input("Enter a stock ticker like AAPL, MSFT, NVDA, or TSLA: ")

    result = run_agent(ticker_input)

    print("\n" + "=" * 80)
    print(result["research_brief"])
    print("=" * 80)