import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
from src.services.market_service import fetch_data
from src.services.news_service import get_sentiment
from src.engine.forecaster import calculate_forecast, get_market_projections, get_sector_performance
from src.services.db_service import init_db, save_daily_log, get_history_with_validation


def render():
    # ADDED: 'page_icon' for the browser tab favicon
    st.set_page_config(
        page_title="Raj-Market-Forecast-Dashboard",
        page_icon="📈",
        layout="wide"
    )
    init_db()

    # --- CSS: BULLETPROOF STYLING & SPACING ADJUSTMENTS ---
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
        }
        button[kind="primary"] { 
            background-color: #00cc66 !important; color: #000000 !important; 
            border: 2px solid #ffffff !important; box-shadow: 0px 0px 15px #00cc66;
            font-weight: bold !important;
        }
        .bias-bullish { color: #008000 !important; }
        .bias-bearish { color: #cc0000 !important; }
        .bias-neutral { color: #222222 !important; }
        .lon-open { color: #008000 !important; }
        .lon-closed { color: #cc0000 !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- STATE MANAGEMENT ---
    if 'active_sym' not in st.session_state:
        st.session_state.active_sym = "NQ=F"
    if 'manual_entry_box' not in st.session_state:
        st.session_state.manual_entry_box = ""

    def set_active_sym(sym):
        st.session_state.active_sym = sym
        st.session_state.manual_entry_box = ""

    def handle_manual_input():
        val = st.session_state.manual_entry_box.strip().upper()
        if val:
            st.session_state.active_sym = val

    # --- QUICK SWITCHER ---
    st.write("### ⚡ Quick Switch")
    symbol_options = ["NQ=F", "ES=F", "GC=F", "CL=F", "TSLA", "AMZN"]
    cols_switch = st.columns([1, 1, 1, 1, 1, 1, 3])
    for i, opt in enumerate(symbol_options):
        b_type = "primary" if st.session_state.active_sym == opt else "secondary"
        cols_switch[i].button(opt, key=f"btn_{opt}", type=b_type, use_container_width=True, on_click=set_active_sym,
                              args=(opt,))

    with cols_switch[6]:
        st.text_input("Manual Ticker", key="manual_entry_box", placeholder="Symbol...", label_visibility="collapsed",
                      on_change=handle_manual_input)

    main_sym = st.session_state.active_sym

    if st.button("Analyze & Forecast", type="primary", use_container_width=True):
        with st.spinner(f"Analyzing {main_sym}..."):
            df1 = fetch_data(main_sym)

            if df1 is None or df1.empty:
                st.error(f"Invalid Symbol : {main_sym}")
            else:
                p1 = get_market_projections(main_sym, df1)
                sent_score, news, summary = get_sentiment(main_sym)
                score, bias, color, t_pts, s_pts = calculate_forecast(p1['current'], df1['High'].max(),
                                                                      df1['Low'].min(), sent_score)

                # --- AUDIO ALERT LOGIC ---
                # Plays a chime if Vol Ratio > 1.5
                if p1['vol_ratio'] > 1.5:
                    st.markdown("""
                        <audio autoplay>
                            <source src="https://nx9724.github.io/assets/chime.mp3" type="audio/mpeg">
                        </audio>
                    """, unsafe_allow_html=True)

                # --- TIMEZONE & SESSION LOGIC ---
                eastern = pytz.timezone('US/Eastern')
                now_et = datetime.now(eastern)

                def get_session_timer(now, hour_open, min_open, hour_close, min_close):
                    open_t = now.replace(hour=hour_open, minute=min_open, second=0, microsecond=0)
                    close_t = now.replace(hour=hour_close, minute=min_close, second=0, microsecond=0)
                    if now < open_t:
                        diff = int((open_t - now).total_seconds())
                        return f"Opens in {diff // 3600}h {(diff // 60) % 60}m"
                    elif now < close_t:
                        diff = int((close_t - now).total_seconds())
                        return f"Closes in {diff // 3600}h {(diff // 60) % 60}m"
                    else:
                        next_open = open_t + timedelta(days=1)
                        if next_open.weekday() >= 5: next_open += timedelta(days=(7 - next_open.weekday()))
                        diff = int((next_open - now).total_seconds())
                        return f"Opens in {diff // 3600}h {(diff // 60) % 60}m"

                ny_timer = get_session_timer(now_et, 9, 30, 16, 0)
                lon_timer = get_session_timer(now_et, 3, 0, 11, 30)

                # NY/London Data fetch
                l_history = yf.Ticker(main_sym).history(period="1d", interval="1h")
                l_data = l_history.between_time('03:00', '11:30')
                l_open, l_high, l_low = (l_data['Open'].iloc[0], l_data['High'].max(),
                                         l_data['Low'].min()) if not l_data.empty else (0, 0, 0)
                is_closed = now_et >= now_et.replace(hour=11, minute=30)
                l_close_html = f'<div style="color: #000000; font-weight: bold; margin: 0; font-size: 19px;">Close: ${l_data["Close"].iloc[-1]:.2f}</div>' if is_closed and not l_data.empty else ''

                # ... (Bias and Header HTML blocks remain identical to your current working code) ...
                # (Just ensure you wrap the existing HTML blocks here as before)

                # After the ribbon, continue with your rearranged lower dashboard columns
                st.info("Analysis Complete. Charts updated.")