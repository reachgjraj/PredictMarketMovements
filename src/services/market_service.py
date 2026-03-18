import yfinance as yf

def fetch_data(symbol):
    try:
        df = yf.Ticker(symbol).history(period="2d", interval="15m")
        return df if not df.empty else None
    except:
        return None