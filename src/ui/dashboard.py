import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime
import pytz
from src.services.market_service import fetch_data
from src.services.news_service import get_sentiment
from src.engine.forecaster import calculate_forecast, get_market_projections, get_sector_performance
from src.services.db_service import init_db, save_daily_log, get_history_with_validation


def render():
    st.set_page_config(page_title="Raj-Market-Forecast-Dashboard", layout="wide")
    init_db()

    # --- CSS: THE BULLETPROOF SOLUTION ---
    st.markdown("""
        <style>
        button[kind="primary"] { 
            background-color: #00cc66 !important; color: #000000 !important; 
            border: 2px solid #ffffff !important; box-shadow: 0px 0px 15px #00cc66;
            font-weight: bold !important;
        }

        /* Defining the colors globally so Streamlit cannot strip them inline */
        .bias-bullish { color: #008000 !important; }
        .bias-bearish { color: #cc0000 !important; }
        .bias-neutral { color: #222222 !important; }

        .lon-open { color: #008000 !important; }
        .lon-closed { color: #cc0000 !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- TOP REFRESH ---
    t_c1, t_c2 = st.columns([9, 1])
    with t_c2:
        if st.button("🔄 Refresh"): st.rerun()

    # --- QUICK SWITCHER + MANUAL INPUT ---
    st.write("### ⚡ Quick Switch")
    symbol_options = ["NQ=F", "ES=F", "GC=F", "CL=F", "TSLA", "AMZN"]
    if 'active_sym' not in st.session_state: st.session_state.active_sym = "NQ=F"

    cols_switch = st.columns([1, 1, 1, 1, 1, 1, 2])
    for i, opt in enumerate(symbol_options):
        b_type = "primary" if st.session_state.active_sym == opt else "secondary"
        if cols_switch[i].button(opt, key=f"btn_{opt}", type=b_type, width="stretch"):
            st.session_state.active_sym = opt
            st.rerun()

    with cols_switch[6]:
        custom_input = st.text_input("Manual Ticker", key="manual_entry_box", placeholder="Symbol...",
                                     label_visibility="collapsed")
        if custom_input:
            st.session_state.active_sym = custom_input.upper()

    main_sym = st.session_state.active_sym

    if st.button("Analyze & Forecast", type="primary", width="stretch"):
        with st.spinner(f"Analyzing {main_sym}..."):
            df1 = fetch_data(main_sym)
            if df1 is not None:
                p1 = get_market_projections(main_sym, df1)
                sent_score, news, summary = get_sentiment(main_sym)
                score, bias, color, t_pts, s_pts = calculate_forecast(p1['current'], df1['High'].max(),
                                                                      df1['Low'].min(), sent_score)

                # --- LONDON DATA ---
                eastern = pytz.timezone('US/Eastern')
                now_et = datetime.now(eastern)
                london_close_time = now_et.replace(hour=11, minute=30, second=0)

                l_history = yf.Ticker(main_sym).history(period="1d", interval="1h")
                l_data = l_history.between_time('03:00', '11:00')
                l_open = l_data['Open'].iloc[0] if not l_data.empty else 0
                l_high = l_data['High'].max() if not l_data.empty else 0
                l_low = l_data['Low'].min() if not l_data.empty else 0

                is_closed = now_et > london_close_time
                l_status_label = "Session Closed" if is_closed else "Session Open"

                # DYNAMIC CSS CLASS ASSIGNMENT
                if "Bullish" in bias:
                    bias_cls = "bias-bullish"
                elif "Bearish" in bias:
                    bias_cls = "bias-bearish"
                else:
                    bias_cls = "bias-neutral"

                lon_cls = "lon-closed" if is_closed else "lon-open"
                vol_c = "#00cc66" if p1['vol_ratio'] > 1.2 else "#ffffff"

                save_daily_log(main_sym,
                               {**p1, 'bias': bias, 't_impact': t_pts, 's_impact': s_pts, 'london_high': l_high,
                                'london_low': l_low})

                # --- HEADER RIBBON ---
                html_block = f"""
                <div style="display: flex; gap: 10px; align-items: stretch; background-color: #f0f2f6; padding: 15px; border-radius: 5px; border: 3px solid blue; margin-bottom: 20px;">
                    <div style="background-color: #d1dffa; padding: 10px; border-radius: 5px; flex: 1.5; text-align: right;">
                        <div style="color: #222222; font-weight: bold; margin: 0; font-size: 13px;">New York Session</div>
                        <div style="color: #000000; font-weight: bold; margin: 0; font-size: 15px;">Prev: ${p1['prev_close']:.2f}</div>
                        <div style="color: #000000; font-weight: bold; margin: 0; font-size: 15px;">Current: ${p1['current']:.2f}</div>
                        <div style="background-color:black; color:#00cc66; display:inline-block; padding:2px 8px; border-radius:3px; font-size:14px; margin-top:5px; font-weight:bold;">↑ {p1['gap']:.2f}%</div>
                    </div>
                    <div style="flex: 3; text-align: center;">
                        <div style="background-color: #1e1e1e; padding: 10px; border-radius: 8px; border-left: 10px solid {color}; margin-bottom: 5px;">
                            <span style="font-size:18px; color:white; font-weight:bold;">💡 {main_sym} Range: <span style="color:#ff4b4b;">{p1['downside']:.2f}</span> — <span style="color:#00cc66;">{p1['upside']:.2f}</span></span>
                        </div>
                        <div style="background-color: #333333; padding: 5px; border-radius: 4px; display: inline-block;">
                             <span style="color: {vol_c}; font-weight: bold; font-size: 20px;">VOL RATIO: {p1['vol_ratio']:.2f}x</span>
                        </div>
                    </div>
                    <div style="background-color: #ffff00; padding: 15px; flex: 1.2; text-align: center; border-radius: 5px;">
                        <div style="color: #222222; font-weight: bold; margin: 0; font-size: 18px;">Bias</div>
                        <div class="{bias_cls}" style="font-size: 38px; font-weight: 900; margin: 0; padding-top: 5px; line-height: 1;">{bias}</div>
                    </div>
                    <div style="background-color: #e1d5e7; padding: 10px; border-radius: 5px; flex: 1.5; text-align: right;">
                        <div style="color: #222222; font-weight: bold; margin: 0; font-size: 13px;">London Session</div>
                        <div style="color: #000000; font-weight: bold; margin: 0; font-size: 15px;">Open: ${l_open:.2f}</div>
                        <div style="color: #000000; font-weight: bold; margin: 0; font-size: 15px;">High: ${l_high:.2f}</div>
                        <div style="color: #000000; font-weight: bold; margin: 0; font-size: 15px;">Low: ${l_low:.2f}</div>
                        <div style="font-size:13px; color: #000000; font-weight: bold; margin-top: 5px;">Status: <span class="{lon_cls}">{l_status_label}</span></div>
                    </div>
                </div>
                """
                st.markdown(html_block.replace('\n', ''), unsafe_allow_html=True)

                # --- LOWER DASHBOARD ---
                col1, col2, col3, col4 = st.columns([1, 1.2, 1.6, 1.2])
                with col1:
                    st.markdown(f"### Conviction: <span style='color:{color}'>{bias}</span>", unsafe_allow_html=True)
                    fig_g = go.Figure(go.Indicator(mode="gauge+number", value=score, gauge={'bar': {'color': color}}))
                    fig_g.update_layout(height=220, margin=dict(l=10, r=10, t=30, b=0), paper_bgcolor='rgba(0,0,0,0)',
                                        font={'color': 'white'})
                    st.plotly_chart(fig_g, width="stretch")

                with col2:
                    st.subheader("Forecast Breakdown")
                    fig_b = go.Figure(go.Bar(x=[t_pts, s_pts], y=['Price', 'News'], orientation='h', marker_color=color,
                                             text=[f"{t_pts:.2f}", f"{s_pts:.2f}"], textposition='auto'))
                    fig_b.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
                    st.plotly_chart(fig_b, width="stretch")

                with col3:
                    st.subheader("📜 History")
                    st.dataframe(get_history_with_validation().style.format(precision=2), height=300, width="stretch")

                with col4:
                    st.subheader("Market Intel")
                    for n in news:
                        st.markdown(
                            f"[{n['time']}] **{n['source']}**: <a href='{n['url']}' target='_blank' style='color: #4da3ff; font-weight: bold; text-decoration: none;'>{n['title']}</a>",
                            unsafe_allow_html=True)

                st.markdown("---")
                v_col, r_col, s_col = st.columns([1, 1, 2.5])
                with v_col:
                    st.subheader("📊 Volume Trend")
                    st.metric("Momentum", f"{p1['vol_ratio']:.2f}x", f"{round((p1['vol_ratio'] - 1) * 100, 1)}%")
                    fig_v = go.Figure(
                        go.Scatter(y=[0.8, 1.1, 0.9, p1['vol_ratio']], fill='tozeroy', line=dict(color='#00cc66')))
                    fig_v.update_layout(height=150, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False,
                                        yaxis_visible=False, paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_v, width="stretch")

                with r_col:
                    st.subheader("💪 Relative Strength")
                    try:
                        nq_r = (yf.Ticker("NQ=F").history(period="1d")['Close'].iloc[-1] /
                                yf.Ticker("NQ=F").history(period="1d")['Open'].iloc[0])
                        es_r = (yf.Ticker("ES=F").history(period="1d")['Close'].iloc[-1] /
                                yf.Ticker("ES=F").history(period="1d")['Open'].iloc[0])
                        gc_r = (yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1] /
                                yf.Ticker("GC=F").history(period="1d")['Open'].iloc[0])
                        strength = (nq_r / ((nq_r + es_r + gc_r) / 3)) * 100
                        st.metric("NQ vs Group", f"{strength:.1f}", f"{'Strong' if strength > 100 else 'Weak'}")
                        fig_rs = go.Figure(go.Indicator(mode="gauge+number", value=strength,
                                                        gauge={'axis': {'range': [98, 102]}, 'bar': {
                                                            'color': '#00cc66' if strength > 100 else '#ff4b4b'}}))
                        fig_rs.update_layout(height=150, margin=dict(l=10, r=10, t=0, b=0),
                                             paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
                        st.plotly_chart(fig_rs, width="stretch")
                    except:
                        st.warning("Strength Data Loading...")

                with s_col:
                    st.subheader("🌍 Sector Trend")
                    sec_data = get_sector_performance()
                    if sec_data:
                        cols = st.columns(len(sec_data))
                        for i, s in enumerate(sec_data):
                            s_c = "#00cc66" if s['change'] > 0 else "#ff4b4b"
                            cols[i].markdown(f"""
                            <div style="background-color: #1e1e1e; border-top: 5px solid {s_c}; padding: 15px 5px; text-align: center; border-radius: 8px;">
                                <p style="margin:0; font-size:14px; color: white; font-weight: bold; text-transform: uppercase;">{s['sector']}</p>
                                <h3 style="margin:0; color: {s_c}; font-size: 20px;">{s['change']:.2f}%</h3>
                            </div>
                            """, unsafe_allow_html=True)