import yfinance as yf

def fetch_data(symbol):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="2d", interval="15m")
    return df if not df.empty else None