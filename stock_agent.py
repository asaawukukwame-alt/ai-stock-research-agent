import os
from dotenv import load_dotenv
from openai import OpenAI
import yfinance as yf

# Load API key from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4o")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing. Check your .env file.")

client = OpenAI(api_key=api_key)


def get_stock_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)

    info = ticker.info
    history = ticker.history(period="1mo")

    if history.empty:
        raise ValueError(f"No stock history found for {ticker_symbol}")

    latest_close = history["Close"].iloc[-1]
    one_month_start = history["Close"].iloc[0]
    one_month_change = ((latest_close - one_month_start) / one_month_start) * 100

    stock_summary = {
        "ticker": ticker_symbol.upper(),
        "company_name": info.get("longName", "Unknown"),
        "sector": info.get("sector", "Unknown"),
        "industry": info.get("industry", "Unknown"),
        "current_price": round(latest_close, 2),
        "one_month_change_percent": round(one_month_change, 2),
        "market_cap": info.get("marketCap", "Unknown"),
        "forward_pe": info.get("forwardPE", "Unknown"),
        "dividend_yield": info.get("dividendYield", "Unknown"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh", "Unknown"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow", "Unknown"),
    }

    return stock_summary


def analyze_stock(stock_summary):
    prompt = f"""
You are a beginner-friendly stock research assistant.

Analyze this stock data:

{stock_summary}

Give the response in this format:

1. Company Overview
2. Recent Stock Performance
3. Valuation Notes
4. Strengths
5. Risks
6. Beginner-Friendly Summary
7. Important Disclaimer

Do not give direct financial advice. Do not say "buy" or "sell."
Explain it like you are helping a student understand the stock.
"""

    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text


def main():
    ticker_symbol = input("Enter a stock ticker, like AAPL, MSFT, TSLA, or NVDA: ")

    print("\nGetting stock data...")
    stock_summary = get_stock_data(ticker_symbol)

    print("\nAsking GPT to analyze the stock...\n")
    analysis = analyze_stock(stock_summary)

    print(analysis)


if __name__ == "__main__":
    main()