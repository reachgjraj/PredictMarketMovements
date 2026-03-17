import streamlit as st
from src.services.options_service import get_options
from src.engine.flow_analyzer import find_unusual

def render():
    st.title("💎 Options Flow")
    symbol = st.text_input("Symbol for Options", "TSLA")
    calls, puts = get_options(symbol)
    if calls is not None:
        st.write("🔥 Unusual Calls")
        st.dataframe(find_unusual(calls))