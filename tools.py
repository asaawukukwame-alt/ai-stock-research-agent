import requests
import yfinance as yf
from langchain_core.tools import tool


SEC_USER_AGENT = "ResearchAgent asaawukukwame@gmail.com"


def _get_cik_for_ticker(ticker: str) -> str | None:
    """Map a ticker symbol to SEC CIK number."""
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {"User-Agent": SEC_USER_AGENT}

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    data = response.json()

    ticker_upper = ticker.upper()

    for entry in data.values():
        if entry["ticker"].upper() == ticker_upper:
            return str(entry["cik_str"]).zfill(10)

    return None


def _fetch_xbrl_concept(cik: str, concept: str, unit: str = "USD") -> list[dict] | None:
    """Fetch one XBRL concept for a company from SEC EDGAR."""
    url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{concept}.json"
    headers = {"User-Agent": SEC_USER_AGENT}

    try:
        response = requests.get(url, headers=headers, timeout=20)

        if response.status_code != 200:
            return None

        data = response.json()
        values = data.get("units", {}).get(unit, [])
        return values

    except Exception:
        return None


def _latest_quarterly_value(items: list[dict] | None) -> dict | None:
    """Return the latest quarterly SEC value."""
    if not items:
        return None

    quarterly_items = [
        item for item in items
        if item.get("form") == "10-Q" and item.get("val") is not None
    ]

    if not quarterly_items:
        return None

    quarterly_items = sorted(
        quarterly_items,
        key=lambda x: x.get("filed", ""),
        reverse=True
    )

    return quarterly_items[0]


@tool
def get_sec_financial_data(ticker: str) -> dict:
    """
    Get official SEC financial data for a public company ticker.

    Returns quarterly revenue, net income, and EPS when available.
    """
    cik = _get_cik_for_ticker(ticker)

    if cik is None:
        return {
            "ticker": ticker.upper(),
            "error": "Could not find SEC CIK for this ticker."
        }

    revenue_items = (
        _fetch_xbrl_concept(cik, "RevenueFromContractWithCustomerExcludingAssessedTax")
        or _fetch_xbrl_concept(cik, "Revenues")
        or _fetch_xbrl_concept(cik, "SalesRevenueNet")
    )

    net_income_items = (
        _fetch_xbrl_concept(cik, "NetIncomeLoss")
        or _fetch_xbrl_concept(cik, "ProfitLoss")
    )

    eps_items = (
        _fetch_xbrl_concept(cik, "EarningsPerShareDiluted", "USD/shares")
        or _fetch_xbrl_concept(cik, "EarningsPerShareBasic", "USD/shares")
    )

    return {
        "ticker": ticker.upper(),
        "cik": cik,
        "latest_quarterly_revenue": _latest_quarterly_value(revenue_items),
        "latest_quarterly_net_income": _latest_quarterly_value(net_income_items),
        "latest_quarterly_eps": _latest_quarterly_value(eps_items),
    }


@tool
def get_yahoo_finance_data(ticker: str) -> dict:
    """
    Get market data and analyst recommendation information from Yahoo Finance.
    """
    ticker_upper = ticker.upper()
    stock = yf.Ticker(ticker_upper)

    info = stock.info
    history = stock.history(period="1mo")

    latest_price = None
    one_month_change_percent = None

    if not history.empty:
        latest_price = float(history["Close"].iloc[-1])
        first_price = float(history["Close"].iloc[0])
        one_month_change_percent = ((latest_price - first_price) / first_price) * 100

    try:
        recommendations = stock.recommendations
        if recommendations is not None and not recommendations.empty:
            recent_recommendations = recommendations.tail(5).to_dict()
        else:
            recent_recommendations = {}
    except Exception:
        recent_recommendations = {}

    return {
        "ticker": ticker_upper,
        "company_name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "current_price": latest_price,
        "one_month_change_percent": one_month_change_percent,
        "market_cap": info.get("marketCap"),
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "recommendation_key": info.get("recommendationKey"),
        "number_of_analyst_opinions": info.get("numberOfAnalystOpinions"),
        "target_mean_price": info.get("targetMeanPrice"),
        "recent_recommendations": recent_recommendations,
    }


if __name__ == "__main__":
    ticker_input = input("Enter a ticker like AAPL, MSFT, NVDA, or TSLA: ")

    print("\nSEC Financial Data:")
    print(get_sec_financial_data.invoke({"ticker": ticker_input}))

    print("\nYahoo Finance Data:")
    print(get_yahoo_finance_data.invoke({"ticker": ticker_input}))

# Alias names expected by agent.py / NextWork
get_sec_fundamentals = get_sec_financial_data
get_market_data = get_yahoo_finance_data

@tool
def get_news_sentiment(ticker: str) -> dict:
    """Fetch recent news headlines and analyze sentiment for a stock ticker.
    Returns headlines and a narrative summary."""

    stock = yf.Ticker(ticker)
    news = stock.news

    if not news:
        return {"ticker": ticker, "headlines": [], "narrative": "No recent news found."}

    headlines = []
    for item in news[:10]:
        title = item.get("title", "")
        publisher = item.get("publisher", "")
        if title:
            headlines.append({"title": title, "publisher": publisher})

    return {"ticker": ticker, "headlines": headlines}