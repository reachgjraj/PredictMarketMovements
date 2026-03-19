import streamlit as st

from src.ui.components.quick_switch import render_quick_switch
from src.ui.components.analysis import run_analysis_with_animation
from src.ui.components.layout import (
    render_header_ribbon,
    render_row_one,
    render_row_two,
    render_news_panel,
)


def _inject_css():
    st.markdown(
        """
        <style>
        .block-container { padding-top: 3rem !important; }
        button[kind="primary"] {
            background-color: #00cc66 !important;
            color: #000000 !important;
            border: 2px solid #ffffff !important;
            box-shadow: 0px 0px 15px #00cc66;
            font-weight: bold !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render():
    _inject_css()

    symbol = render_quick_switch()

    if st.button("Analyze & Forecast", type="primary", width="stretch"):
        result = run_analysis_with_animation(symbol)

        render_header_ribbon(symbol, result)
        render_row_one(symbol, result)
        render_row_two(symbol, result)
        render_news_panel(result["news"])