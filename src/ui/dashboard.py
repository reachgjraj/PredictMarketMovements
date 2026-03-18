import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import numpy as np
import time

from src.services.market_service import fetch_data
from src.services.news_service import get_sentiment
from src.engine.forecaster import (
    calculate_forecast,
    get_market_projections,
    get_sector_performance,
)
from src.services.db_service import save_daily_log, get_history_with_validation


def render():

    # --- CSS (reduced spacing + improved contrast) ---
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 0.8rem !important;
        }
        button[kind="primary"] { 
            background-color: #00cc66 !important; color: #000000 !important; 
            border: 2px solid #ffffff !important; box-shadow: 0px 0px 15px #00cc66;
            font-weight: bold !important;
        }
        .bias-bullish { color: #006400 !important; }
        .bias-bearish { color: #8B0000 !important; }
        .bias-neutral { color: #333333 !important; }
        .lon-open { color: #006400 !important; }
        .lon-closed { color: #8B0000 !important; }
        .session-title { color: #111111 !important; font-weight: 800 !important; }
        .session-sub { color: #222222 !important; font-weight: 700 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- STATE ---
    if "active_sym" not in st.session_state:
        st.session_state.active_sym = "NQ=F"
    if "manual_entry_box" not in st.session_state:
        st.session_state.manual_entry_box = ""

    def set_active_sym(sym):
        st.session_state.active_sym = sym
        st.session_state.manual_entry_box = ""

    def handle_manual_input():
        val = st.session_state.manual_entry_box.strip().upper()
        if val:
            st.session_state.active_sym = val

    # ============================================================
    # ⭐ QUICK SWITCH — ALWAYS AT TOP
    # ============================================================
    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
    st.subheader("⚡ Quick Switch")

    symbol_options = ["NQ=F", "ES=F", "GC=F", "CL=F", "TSLA", "AMZN"]
    cols_switch = st.columns([1, 1, 1, 1, 1, 1, 2])

    for i, opt in enumerate(symbol_options):
        b_type = "primary" if st.session_state.active_sym == opt else "secondary"
        cols_switch[i].button(
            opt,
            key=f"btn_{opt}",
            type=b_type,
            use_container_width=True,
            on_click=set_active_sym,
            args=(opt,),
        )

    with cols_switch[6]:
        st.text_input(
            "Manual Ticker",
            key="manual_entry_box",
            placeholder="Symbol...",
            label_visibility="collapsed",
            on_change=handle_manual_input,
        )

    main_sym = st.session_state.active_sym

    # ============================================================
    # ⭐ ANALYZE BUTTON WITH C3 TRIPLE PULSE RINGS
    # ============================================================
    if st.button("Analyze & Forecast", type="primary", use_container_width=True):

        loading_placeholder = st.empty()
        analysis_done = False
        result_container = {}

        # Precompute circle angles
        theta = np.linspace(0, 2 * np.pi, 200)

        # Random phase offsets for each ring
        phase1 = np.random.uniform(0, 2 * np.pi)
        phase2 = np.random.uniform(0, 2 * np.pi)
        phase3 = np.random.uniform(0, 2 * np.pi)

        # --- Run animation + analysis together ---
        for i in range(80):

            t = i / 6.0

            # Radii oscillations (triple pulse)
            r1 = 0.6 + 0.5 * np.sin(t + phase1)
            r2 = 0.9 + 0.6 * np.sin(t + phase2)
            r3 = 1.2 + 0.7 * np.sin(t + phase3)

            # Ensure radii stay positive
            r1 = max(r1, 0.2)
            r2 = max(r2, 0.3)
            r3 = max(r3, 0.4)

            x1 = r1 * np.cos(theta)
            y1 = r1 * np.sin(theta)
            x2 = r2 * np.cos(theta)
            y2 = r2 * np.sin(theta)
            x3 = r3 * np.cos(theta)
            y3 = r3 * np.sin(theta)

            fig_loading = go.Figure()

            fig_loading.add_trace(
                go.Scatter(
                    x=x1,
                    y=y1,
                    mode="lines",
                    line=dict(color="rgba(0,204,102,1.0)", width=3),
                    showlegend=False,
                )
            )
            fig_loading.add_trace(
                go.Scatter(
                    x=x2,
                    y=y2,
                    mode="lines",
                    line=dict(color="rgba(0,204,102,0.7)", width=2),
                    showlegend=False,
                )
            )
            fig_loading.add_trace(
                go.Scatter(
                    x=x3,
                    y=y3,
                    mode="lines",
                    line=dict(color="rgba(0,204,102,0.4)", width=2),
                    showlegend=False,
                )
            )

            fig_loading.update_layout(
                height=220,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            loading_placeholder.plotly_chart(fig_loading, use_container_width=True)

            # Run analysis once, early in the loop
            if i == 2 and not analysis_done:
                try:
                    df1 = fetch_data(main_sym)
                    if df1 is None or df1.empty:
                        loading_placeholder.empty()
                        st.error(f"Invalid Symbol : {main_sym}")
                        st.stop()

                    p1 = get_market_projections(main_sym, df1)
                    sent_score, news, summary = get_sentiment(main_sym)
                    score, bias, color, t_pts, s_pts = calculate_forecast(
                        p1["current"], df1["High"].max(), df1["Low"].min(), sent_score
                    )

                    result_container = {
                        "df1": df1,
                        "p1": p1,
                        "sent_score": sent_score,
                        "news": news,
                        "summary": summary,
                        "score": score,
                        "bias": bias,
                        "color": color,
                        "t_pts": t_pts,
                        "s_pts": s_pts,
                    }
                    analysis_done = True
                except Exception as e:
                    loading_placeholder.empty()
                    st.error(f"Analysis failed: {e}")
                    st.stop()

            # Let animation run a few extra frames after analysis for smoothness
            if analysis_done and i > 6:
                break

            time.sleep(0.03)

        loading_placeholder.empty()

        if not analysis_done:
            st.error("Analysis failed. Try again.")
            st.stop()

        # Unpack results
        df1 = result_container["df1"]
        p1 = result_container["p1"]
        sent_score = result_container["sent_score"]
        news = result_container["news"]
        summary = result_container["summary"]
        score = result_container["score"]
        bias = result_container["bias"]
        color = result_container["color"]
        t_pts = result_container["t_pts"]
        s_pts = result_container["s_pts"]

        # ============================================================
        # REAL DASHBOARD RENDERING
        # ============================================================

        eastern = pytz.timezone("US/Eastern")
        now_et = datetime.now(eastern)

        def get_session_timer(now, hour_open, min_open, hour_close, min_close):
            open_t = now.replace(
                hour=hour_open, minute=min_open, second=0, microsecond=0
            )
            close_t = now.replace(
                hour=hour_close, minute=min_close, second=0, microsecond=0
            )

            if now < open_t:
                diff = int((open_t - now).total_seconds())
                return f"Opens in {diff // 3600}h {(diff // 60) % 60}m"
            elif now < close_t:
                diff = int((close_t - now).total_seconds())
                return f"Closes in {diff // 3600}h {(diff // 60) % 60}m"
            else:
                next_open = open_t + timedelta(days=1)
                if next_open.weekday() >= 5:
                    next_open += timedelta(days=(7 - next_open.weekday()))
                diff = int((next_open - now).total_seconds())
                return f"Opens in {diff // 3600}h {(diff // 60) % 60}m"

        ny_timer = get_session_timer(now_et, 9, 30, 16, 0)
        lon_timer = get_session_timer(now_et, 3, 0, 11, 30)

        ny_open = now_et.replace(hour=9, minute=30) <= now_et < now_et.replace(
            hour=16, minute=0
        )
        lon_open = now_et.replace(hour=3, minute=0) <= now_et < now_et.replace(
            hour=11, minute=30
        )

        ny_cls = "lon-open" if ny_open else "lon-closed"
        lon_cls = "lon-open" if lon_open else "lon-closed"

        l_history = yf.Ticker(main_sym).history(period="1d", interval="1h")
        l_data = l_history.between_time("03:00", "11:30")

        l_open = l_data["Open"].iloc[0] if not l_data.empty else 0
        l_high = l_data["High"].max() if not l_data.empty else 0
        l_low = l_data["Low"].min() if not l_data.empty else 0
        l_close_val = l_data["Close"].iloc[-1] if not l_data.empty else 0

        l_close_html = (
            f'<div style="color:#111111; font-weight:900; font-size:19px;">Close: ${l_close_val:.2f}</div>'
            if not lon_open
            else ""
        )

        save_daily_log(
            main_sym,
            {
                **p1,
                "bias": bias,
                "t_impact": t_pts,
                "s_impact": s_pts,
                "london_high": l_high,
                "london_low": l_low,
            },
        )

        bias_cls = (
            "bias-bullish"
            if bias == "Bullish"
            else "bias-bearish"
            if bias == "Bearish"
            else "bias-neutral"
        )

        vol_c = "#00cc66" if p1["vol_ratio"] > 1.2 else "#ffffff"

        # ============================================================
        # HEADER RIBBON
        # ============================================================
        html_block = f"""
        <div style="display:flex; gap:10px; align-items:stretch; background-color:#f0f2f6; padding:10px; border-radius:5px; border:3px solid blue; margin-bottom:10px;">

            <div style="background-color:#d1dffa; padding:10px; border-radius:5px; flex:1.8; display:flex; justify-content:space-between;">
                <div>
                    <div class="session-title">New York Session</div>
                    <div class="session-sub">⏳ {ny_timer}</div>
                    <div style="font-size:17px; font-weight:800; margin-top:10px; color:#111111;">
                        Status: <span class="{ny_cls}">{'Open' if ny_open else 'Closed'}</span>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-weight:800; font-size:19px; color:#111111;">Prev: ${p1['prev_close']:.2f}</div>
                    <div style="font-weight:800; font-size:19px; color:#111111;">Current: ${p1['current']:.2f}</div>
                    <div style="margin-top:5px;">
                        <span style="background-color:black; color:#00cc66; padding:3px 8px; border-radius:3px; font-size:17px; font-weight:bold;">{p1['gap']:.2f}%</span>
                    </div>
                </div>
            </div>

            <div style="background-color:#e1d5e7; padding:10px; border-radius:5px; flex:1.8; display:flex; justify-content:space-between;">
                <div>
                    <div class="session-title">London Session</div>
                    <div class="session-sub">⏳ {lon_timer}</div>
                    <div style="font-size:17px; font-weight:800; margin-top:10px; color:#111111;">
                        Status: <span class="{lon_cls}">{'Open' if lon_open else 'Closed'}</span>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-weight:800; font-size:19px; color:#111111;">Open: ${l_open:.2f}</div>
                    <div style="font-weight:800; font-size:19px; color:#111111;">High: ${l_high:.2f}</div>
                    <div style="font-weight:800; font-size:19px; color:#111111;">Low: ${l_low:.2f}</div>
                    {l_close_html}
                </div>
            </div>

            <div style="flex:2.5; text-align:center;">
                <div style="background-color:#1e1e1e; padding:10px; border-radius:8px; border-left:10px solid {color}; margin-bottom:5px;">
                    <span style="font-size:18px; color:white; font-weight:bold;">💡 {main_sym} Range: <span style="color:#ff4b4b;">${p1['downside']:.2f}</span> — <span style="color:#00cc66;">${p1['upside']:.2f}</span></span>
                </div>
                <div style="background-color:#333333; padding:5px; border-radius:4px; display:inline-block;">
                    <span style="color:{vol_c}; font-weight:bold; font-size:20px;">VOL RATIO: {p1['vol_ratio']:.2f}x</span>
                </div>
            </div>

            <div style="background-color:#ffff00; padding:15px; flex:1.2; text-align:center; border-radius:5px;">
                <div style="font-weight:800; font-size:18px; color:#111111;">Bias</div>
                <div class="{bias_cls}" style="font-size:38px; font-weight:900; margin-top:5px;">{bias}</div>
            </div>

        </div>
        """
        st.markdown(html_block.replace("\n", ""), unsafe_allow_html=True)

        # ============================================================
        # LOWER DASHBOARD
        # ============================================================

        r1_c1, r1_c2, r1_c3, r1_c4 = st.columns([1, 1.2, 1, 1])

        with r1_c1:
            st.markdown(
                f"### Conviction: <span style='color:{color}'>{bias}</span>",
                unsafe_allow_html=True,
            )
            fig_g = go.Figure(
                go.Indicator(mode="gauge+number", value=score, gauge={"bar": {"color": color}})
            )
            fig_g.update_layout(
                height=220,
                margin=dict(l=10, r=10, t=30, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                font={"color": "white"},
            )
            st.plotly_chart(fig_g, use_container_width=True)

        with r1_c2:
            st.subheader("Forecast Breakdown")
            fig_b = go.Figure(
                go.Bar(
                    x=[t_pts, s_pts],
                    y=["Price", "News"],
                    orientation="h",
                    marker_color=color,
                    text=[f"{t_pts:.2f}", f"{s_pts:.2f}"],
                    textposition="auto",
                )
            )
            fig_b.update_layout(
                height=250,
                paper_bgcolor="rgba(0,0,0,0)",
                font={"color": "white"},
            )
            st.plotly_chart(fig_b, use_container_width=True)

        with r1_c3:
            st.subheader("📊 Volume Trend")
            st.metric(
                "Momentum",
                f"{p1['vol_ratio']:.2f}x",
                f"{round((p1['vol_ratio'] - 1) * 100, 1)}%",
            )
            fig_v = go.Figure(
                go.Scatter(
                    y=[0.8, 1.1, 0.9, p1["vol_ratio"]],
                    fill="tozeroy",
                    line=dict(color="#00cc66"),
                )
            )
            fig_v.update_layout(
                height=150,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_visible=False,
                yaxis_visible=False,
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_v, use_container_width=True)

        with r1_c4:
            st.subheader("💪 Relative Strength")
            try:
                nq_r = yf.Ticker("NQ=F").history(period="1d")
                es_r = yf.Ticker("ES=F").history(period="1d")
                gc_r = yf.Ticker("GC=F").history(period="1d")

                strength = (
                    (nq_r["Close"].iloc[-1] / nq_r["Open"].iloc[0])
                    / (
                        (
                            (es_r["Close"].iloc[-1] / es_r["Open"].iloc[0])
                            + (gc_r["Close"].iloc[-1] / gc_r["Open"].iloc[0])
                            + (nq_r["Close"].iloc[-1] / nq_r["Open"].iloc[0])
                        )
                        / 3
                    )
                    * 100
                )

                st.metric(
                    "NQ vs Group",
                    f"{strength:.1f}",
                    "Strong" if strength > 100 else "Weak",
                )

                fig_rs = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=strength,
                        gauge={
                            "axis": {"range": [98, 102]},
                            "bar": {
                                "color": "#00cc66" if strength > 100 else "#ff4b4b"
                            },
                        },
                    )
                )
                fig_rs.update_layout(
                    height=150,
                    margin=dict(l=10, r=10, t=0, b=0),
                    paper_bgcolor="rgba(0,0,0,0)",
                    font={"color": "white"},
                )
                st.plotly_chart(fig_rs, use_container_width=True)
            except Exception:
                st.warning("Strength Data Loading...")

        st.markdown("---")

        # ROW 2
        r2_c1, r2_c2 = st.columns([1.5, 1])

        with r2_c1:
            st.subheader("📜 History")
            hist_df = get_history_with_validation()
            if "id" in hist_df.columns:
                hist_df = hist_df.drop(columns=["id"])
            st.dataframe(
                hist_df.style.format(precision=2),
                height=250,
                use_container_width=True,
            )

        with r2_c2:
            st.subheader("🌍 Sector Trend")
            sec_data = get_sector_performance()
            if sec_data:
                cols = st.columns(len(sec_data))
                for i, s in enumerate(sec_data):
                    s_c = "#00cc66" if s["change"] > 0 else "#ff4b4b"
                    cols[i].markdown(
                        f"""<div style="background-color:#1e1e1e; border-top:5px solid {s_c}; padding:15px 5px; text-align:center; border-radius:8px;">
<p style="margin:0; font-size:14px; color:white; font-weight:bold;">{s['sector']}</p>
<h3 style="margin:0; color:{s_c}; font-size:20px;">{s['change']:.2f}%</h3>
</div>""",
                        unsafe_allow_html=True,
                    )

        st.markdown("---")

        # ROW 3 — Market Intel
        st.subheader("📰 Market Intel")
        for n in news:
            st.markdown(
                f"[{n['time']}] **{n['source']}**: "
                f"<a href='{n['url']}' target='_blank' "
                f"style='color:#4da3ff; font-weight:bold; text-decoration:none;'>"
                f"{n['title']}</a>",
                unsafe_allow_html=True,
            )