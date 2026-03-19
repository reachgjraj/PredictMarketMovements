import streamlit as st


def _init_state():
    if "active_sym" not in st.session_state:
        st.session_state.active_sym = "NQ=F"
    if "manual_entry_box" not in st.session_state:
        st.session_state.manual_entry_box = ""


def _set_active_sym(sym: str):
    st.session_state.active_sym = sym
    st.session_state.manual_entry_box = ""


def _handle_manual_input():
    val = st.session_state.manual_entry_box.strip().upper()
    if val:
        st.session_state.active_sym = val


def render_quick_switch() -> str:
    _init_state()

    st.subheader("⚡ Quick Switch")

    # -----------------------------
    # CATEGORY MAPS
    # -----------------------------
    futures_map = {
        "NQ": "NQ=F",
        "ES": "ES=F",
        "GC": "GC=F",
        "SI": "SI=F",
        "CL": "CL=F",
    }

    fx_crypto_map = {
        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "JPYUSD": "JPYUSD=X",
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
        "XRP": "XRP-USD",
    }

    stocks_map = {
        "TSLA": "TSLA",
        "AMZN": "AMZN",
        "SPY": "SPY",
        "NVDA": "NVDA",
        "GOOG": "GOOG",
        "MSFT": "MSFT",
    }

    # -----------------------------
    # ROW 1 — FUTURES (LEFT) + FOREX/CRYPTO (RIGHT)
    # -----------------------------
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown("### 📈 Futures & Commodities")
        cols = st.columns(len(futures_map))
        for i, (label, actual) in enumerate(futures_map.items()):
            b_type = "primary" if st.session_state.active_sym == actual else "secondary"
            cols[i].button(
                label,
                key=f"fut_{label}",
                type=b_type,
                width="stretch",
                on_click=_set_active_sym,
                args=(actual,),
            )

    with row1_col2:
        st.markdown("### 💱 Forex & 🪙 Crypto")
        cols = st.columns(len(fx_crypto_map))
        for i, (label, actual) in enumerate(fx_crypto_map.items()):
            b_type = "primary" if st.session_state.active_sym == actual else "secondary"
            cols[i].button(
                label,
                key=f"fxc_{label}",
                type=b_type,
                width="stretch",
                on_click=_set_active_sym,
                args=(actual,),
            )

    # -----------------------------
    # ROW 2 — STOCKS (LEFT) + CUSTOM SYMBOL (RIGHT)
    # -----------------------------
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("### 🏦 Stocks")
        cols = st.columns(len(stocks_map))
        for i, (label, actual) in enumerate(stocks_map.items()):
            b_type = "primary" if st.session_state.active_sym == actual else "secondary"
            cols[i].button(
                label,
                key=f"stk_{label}",
                type=b_type,
                width="stretch",
                on_click=_set_active_sym,
                args=(actual,),
            )

    with row2_col2:
        st.markdown("### 🔍 Custom Symbol")
        st.text_input(
            "Manual Ticker",
            key="manual_entry_box",
            placeholder="Enter any symbol (AAPL, META, BTC-USD, EURUSD=X)...",
            label_visibility="collapsed",
            on_change=_handle_manual_input,
        )

    return st.session_state.active_sym