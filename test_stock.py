import yfinance as yf

ticker_symbol = "AAPL"
ticker = yf.Ticker(ticker_symbol)

history = ticker.history(period="5d")

print(f"Recent stock data for {ticker_symbol}:")
print(history[["Open", "High", "Low", "Close", "Volume"]])