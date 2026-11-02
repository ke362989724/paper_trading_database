import yfinance as yf

def fetch_market_cap(ticker: str):
    t = yf.Ticker(ticker)
    mc = t.info.get("marketCap")
    return mc