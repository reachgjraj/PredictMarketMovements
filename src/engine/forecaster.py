import yfinance as yf
import pandas as pd

def calculate_forecast(current_price, s_high, s_low, sentiment_score):
    base_score = 50.0
    tech_impact = 0

    if current_price >= s_high:
        tech_impact = 30
    elif current_price <= s_low:
        tech_impact = -30
    else:
        price_range = s_high - s_low
        if price_range > 0:
            pos_percent = (current_price - s_low) / price_range
            tech_impact = (pos_percent - 0.5) * 40

    sent_impact = sentiment_score * 15
    final_score = round(min(100, max(0, base_score + tech_impact + sent_impact)), 1)

    if final_score >= 60:
        bias, color = "Bullish", "#00cc66"
    elif final_score <= 40:
        bias, color = "Bearish", "#ff4b4b"
    else:
        bias, color = "Neutral", "#777777"

    return final_score, bias, color, round(tech_impact, 2), round(sent_impact, 2)


def get_sector_performance():
    sectors = {"XLK": "Tech", "XLF": "Finance", "XLY": "Disc", "XLC": "Comm", "XLV": "Health", "XLI": "Indus"}
    try:
        data = yf.download(list(sectors.keys()), period="2d", interval="1d", progress=False)['Close']
        returns = data.pct_change().iloc[-1] * 100
        return [{"sector": sectors[s], "change": round(returns[s], 2)} for s in sectors.keys()]
    except:
        return []


def get_market_projections(symbol, df, vol_mult=1.0):
    tk = yf.Ticker(symbol)
    try:
        info = tk.info
    except:
        info = {}

    avg_vol = info.get('averageVolume', 1) or 1
    cur_vol = info.get('regularMarketVolume') or info.get('volume', 0) or 0
    vol_ratio = round(cur_vol / avg_vol, 2)

    prev_close = info.get('previousClose') or (df['Close'].iloc[-2] if len(df) > 1 else 0)
    current_price = info.get('regularMarketPrice') or df['Close'].iloc[-1]
    forecasted_open = info.get('preMarketPrice') or current_price

    df['tr'] = df['High'] - df['Low']
    atr = df['tr'].tail(14).mean()

    upside = forecasted_open + (atr * 0.5 * vol_mult)
    downside = forecasted_open - (atr * 0.5 * vol_mult)

    return {
        "prev_close": round(prev_close, 2),
        "current": round(current_price, 2),
        "open": round(forecasted_open, 2),
        "gap": round(((forecasted_open - prev_close) / prev_close) * 100, 2) if prev_close else 0.0,
        "upside": round(upside, 2),
        "downside": round(downside, 2),
        "vol_ratio": vol_ratio
    }