import os
import requests
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

SEC_USER_AGENT = os.getenv(
    "SEC_USER_AGENT",
    "stock-ai-agent-nextwork asaawukukwame@gmail.com"
)


def get_cik_from_ticker(ticker_symbol):
    ticker_symbol = ticker_symbol.upper()

    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {
        "User-Agent": SEC_USER_AGENT,
        "Accept-Encoding": "gzip, deflate",
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    companies = response.json()

    for company in companies.values():
        if company["ticker"].upper() == ticker_symbol:
            return {
                "ticker": company["ticker"],
                "company_name": company["title"],
                "cik": str(company["cik_str"]).zfill(10),
            }

    raise ValueError(f"No SEC company found for ticker: {ticker_symbol}")


def get_sec_company_facts(ticker_symbol):
    company = get_cik_from_ticker(ticker_symbol)
    cik = company["cik"]

    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    headers = {
        "User-Agent": SEC_USER_AGENT,
        "Accept-Encoding": "gzip, deflate",
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    return company, response.json()


def extract_sec_fact(facts_json, possible_concepts, unit):
    us_gaap = facts_json["facts"].get("us-gaap", {})

    for concept in possible_concepts:
        if concept in us_gaap:
            units = us_gaap[concept].get("units", {})
            if unit in units:
                rows = units[unit]
                df = pd.DataFrame(rows)
                df["concept"] = concept
                return df

    return pd.DataFrame()


def get_quarterly_financials_from_sec(ticker_symbol):
    company, facts_json = get_sec_company_facts(ticker_symbol)

    revenue_df = extract_sec_fact(
        facts_json,
        [
            "Revenues",
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "SalesRevenueNet",
        ],
        "USD",
    )

    net_income_df = extract_sec_fact(
        facts_json,
        ["NetIncomeLoss", "ProfitLoss"],
        "USD",
    )

    eps_df = extract_sec_fact(
        facts_json,
        ["EarningsPerShareDiluted", "EarningsPerShareBasic"],
        "USD/shares",
    )

    def clean_quarterly(df, value_name):
        if df.empty:
            return pd.DataFrame(columns=["fy", "fp", "end", "filed", value_name])

        df = df[df["form"].isin(["10-Q", "10-K"])].copy()
        df = df[["fy", "fp", "end", "filed", "val", "concept"]]
        df = df.rename(columns={"val": value_name, "concept": f"{value_name}_concept"})
        df = df.sort_values("filed", ascending=False)
        df = df.drop_duplicates(subset=["fy", "fp", "end"], keep="first")
        return df

    revenue = clean_quarterly(revenue_df, "revenue")
    net_income = clean_quarterly(net_income_df, "net_income")
    eps = clean_quarterly(eps_df, "eps")

    result = revenue.merge(
        net_income,
        on=["fy", "fp", "end", "filed"],
        how="left",
    )

    result = result.merge(
        eps,
        on=["fy", "fp", "end", "filed"],
        how="left",
    )

    result.insert(0, "ticker", company["ticker"])
    result.insert(1, "company_name", company["company_name"])
    result.insert(2, "cik", company["cik"])

    return result.sort_values("filed", ascending=False).head(8)


def get_yahoo_market_data(ticker_symbol):
    ticker_symbol = ticker_symbol.upper()
    ticker = yf.Ticker(ticker_symbol)

    info = ticker.info
    history = ticker.history(period="1mo")

    latest_price = None
    one_month_change_percent = None

    if not history.empty:
        latest_price = float(history["Close"].iloc[-1])
        first_price = float(history["Close"].iloc[0])
        one_month_change_percent = ((latest_price - first_price) / first_price) * 100

    market_data = {
        "ticker": ticker_symbol,
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
    }

    try:
        recommendations = ticker.recommendations
        if recommendations is not None and not recommendations.empty:
            recommendations = recommendations.tail(10)
        else:
            recommendations = pd.DataFrame()
    except Exception:
        recommendations = pd.DataFrame()

    return market_data, recommendations


def test_tools(ticker_symbol):
    print(f"\nSEC lookup for {ticker_symbol}:")
    company = get_cik_from_ticker(ticker_symbol)
    print(company)

    print(f"\nQuarterly SEC financials for {ticker_symbol}:")
    sec_financials = get_quarterly_financials_from_sec(ticker_symbol)
    print(sec_financials)

    print(f"\nYahoo Finance market data for {ticker_symbol}:")
    market_data, recommendations = get_yahoo_market_data(ticker_symbol)
    print(market_data)

    print(f"\nRecent analyst recommendations for {ticker_symbol}:")
    print(recommendations)


if __name__ == "__main__":
    ticker = input("Enter a stock ticker like AAPL, MSFT, NVDA, or TSLA: ")
    test_tools(ticker)