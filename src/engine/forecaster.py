import numpy as np
import yfinance as yf


# ---------------------------------------------------------
# PRICE PROJECTION (ATR‑BASED)
# ---------------------------------------------------------
def compute_price_projection(df):
    """
    Computes upside/downside projections using ATR (Average True Range).
    ATR gives a volatility-adjusted projection instead of fixed percentages.
    """

    if len(df) < 15:
        # fallback for very small datasets
        current = float(df["Close"].iloc[-1])
        return current * 0.99, current * 1.01

    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    # True Range
    tr = np.maximum(high - low, np.maximum(abs(high - close.shift()), abs(low - close.shift())))
    atr = tr.rolling(14).mean().iloc[-1]

    current = float(close.iloc[-1])

    # Projections = current ± ATR
    downside = current - atr
    upside = current + atr

    return downside, upside


# ---------------------------------------------------------
# VOLUME MOMENTUM SCORE
# ---------------------------------------------------------
def compute_volume_ratio(df):
    """
    Computes volume momentum as:
    last_volume / average_volume
    """

    vol = df["Volume"]
    last = float(vol.iloc[-1])
    avg = float(vol.mean())

    if avg <= 0:
        return 1.0

    return last / avg


# ---------------------------------------------------------
# TECHNICAL BIAS SCORE (VOLATILITY‑NORMALIZED)
# ---------------------------------------------------------
def compute_bias_score(df):
    """
    Computes a technical bias score from -1 to +1.
    Uses:
    - price position within range
    - volatility normalization
    - short-term momentum
    """

    close = df["Close"]
    high = float(df["High"].max())
    low = float(df["Low"].min())
    current = float(close.iloc[-1])

    # Price position within range (0–1)
    if high == low:
        price_pos = 0.5
    else:
        price_pos = (current - low) / (high - low)

    # Normalize to -1 to +1
    price_score = (price_pos - 0.5) * 2

    # Momentum (last 5 bars)
    if len(close) >= 6:
        momentum = float(close.iloc[-1] - close.iloc[-6]) / max(abs(close.iloc[-6]), 1)
    else:
        momentum = 0

    # Blend technicals
    tech_score = (price_score * 0.7) + (momentum * 0.3)

    # Clamp
    tech_score = max(min(tech_score, 1), -1)

    return tech_score


# ---------------------------------------------------------
# SENTIMENT IMPACT
# ---------------------------------------------------------
def compute_sentiment_impact(sent_score):
    """
    Converts sentiment score (-∞ to +∞) into a normalized -1 to +1 impact.
    """

    # Hard clamp extreme sentiment
    sent_score = max(min(sent_score, 3), -3)

    # Normalize to -1 to +1
    return sent_score / 3


# ---------------------------------------------------------
# SECTOR PERFORMANCE (UNCHANGED)
# ---------------------------------------------------------
def get_sector_performance():
    """
    Returns sector performance using SPDR ETFs.
    """

    sector_map = {
        "Tech": "XLK",
        "Finance": "XLF",
        "Energy": "XLE",
        "Health": "XLV",
        "Industrials": "XLI",
    }

    results = []

    for name, ticker in sector_map.items():
        try:
            df = yf.Ticker(ticker).history(period="1d")
            if df.empty:
                continue

            open_p = df["Open"].iloc[0]
            close_p = df["Close"].iloc[-1]
            change = ((close_p - open_p) / open_p) * 100

            results.append({"sector": name, "change": change})
        except Exception:
            continue

    return results