import streamlit as st

from src.ui.dashboard import render as dashboard_render
from src.ui.options_view import render as options_render
from src.ui.history import render as history_render
from src.services.db_service import init_db

# Initialize database
init_db()

st.set_page_config(
    page_title="Raj-Market-Forecast-Dashboard",
    layout="wide",
)

st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Select a Screen",
    ["Market Dashboard", "Options Intelligence", "Trade History"],
)

if page == "Market Dashboard":
    dashboard_render()
elif page == "Options Intelligence":
    options_render()
elif page == "Trade History":
    history_render()