import time
import random
import streamlit as st
import yfinance as yf

from src.engine.forecaster import (
    compute_bias_score,
    compute_price_projection,
    compute_volume_ratio,
    compute_sentiment_impact,
)
from src.services.news_service import get_sentiment


# ---------------------------------------------------------
# C3 TRIPLE PULSE RINGS WITH NEON GLOW TRAIL
# ---------------------------------------------------------
def _render_c3_animation(container):
    r1 = random.randint(40, 70)
    r2 = random.randint(70, 110)
    r3 = random.randint(110, 150)

    container.markdown(
        f"""
        <style>
        .pulse-wrapper {{
            position: relative;
            width: 220px;
            height: 220px;
            margin: auto;
            margin-top: 25px;
        }}

        .pulse-ring {{
            position: absolute;
            border-radius: 50%;
            border: 4px solid #00ff88;
            opacity: 0.9;
            box-shadow: 0 0 25px #00ff88, 0 0 45px #00ff88;
            animation: pulseGlow 1.8s infinite ease-out;
        }}

        .ring1 {{
            width: {r1}px;
            height: {r1}px;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation-delay: 0s;
        }}

        .ring2 {{
            width: {r2}px;
            height: {r2}px;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation-delay: 0.35s;
        }}

        .ring3 {{
            width: {r3}px;
            height: {r3}px;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation-delay: 0.7s;
        }}

        @keyframes pulseGlow {{
            0% {{
                transform: translate(-50%, -50%) scale(0.6);
                opacity: 1;
                box-shadow: 0 0 25px #00ff88, 0 0 45px #00ff88;
            }}
            100% {{
                transform: translate(-50%, -50%) scale(1.9);
                opacity: 0;
                box-shadow: 0 0 5px #00ff88, 0 0 10px #00ff88;
            }}
        }}
        </style>

        <div class="pulse-wrapper">
            <div class="pulse-ring ring1"></div>
            <div class="pulse-ring ring2"></div>
            <div class="pulse-ring ring3"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# CORE ANALYSIS ENGINE
# ---------------------------------------------------------
def _run_core_analysis(symbol: str):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="1d", interval="1m")

    if hist.empty:
        raise ValueError(f"No data available for {symbol}")

    prev_close = float(hist["Close"].iloc[0])
    current = float(hist["Close"].iloc[-1])
    high = float(hist["High"].max())
    low = float(hist["Low"].min())

    gap = ((current - prev_close) / prev_close) * 100

    vol_ratio = compute_volume_ratio(hist)
    downside, upside = compute_price_projection(hist)

    sent_score, news, sent_summary, sent_badge = get_sentiment(symbol)

    s_pts = compute_sentiment_impact(sent_score)
    t_pts = compute_bias_score(hist)

    total_score = t_pts + s_pts

    if total_score > 0.5:
        bias = "Bullish"
        color = "#00cc66"
    elif total_score < -0.5:
        bias = "Bearish"
        color = "#ff4b4b"
    else:
        bias = "Neutral"
        color = "#ffff00"

    market_mood = round((t_pts * 0.6) + (s_pts * 0.4), 3)

    return {
        "p1": {
            "prev_close": prev_close,
            "current": current,
            "high": high,
            "low": low,
            "gap": gap,
            "vol_ratio": vol_ratio,
            "downside": downside,
            "upside": upside,
        },
        "score": total_score,
        "bias": bias,
        "color": color,
        "t_pts": t_pts,
        "s_pts": s_pts,
        "news": news,
        "sentiment_summary": sent_summary,
        "sentiment_badge": sent_badge,
        "market_mood": market_mood,
    }


# ---------------------------------------------------------
# PUBLIC WRAPPER — NO SPINNER, NO BLANK DELAY
# ---------------------------------------------------------
def run_analysis_with_animation(symbol: str):
    placeholder = st.empty()

    # Show animation immediately
    _render_c3_animation(placeholder)

    # Run analysis WHILE animation is visible
    result = _run_core_analysis(symbol)

    # Remove animation instantly when done
    placeholder.empty()

    return result