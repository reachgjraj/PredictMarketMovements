import streamlit as st
from src.ui import dashboard, options_view, history
from src.services.db_service import init_db

# Initialize database
init_db()

st.set_page_config(page_title="PredictMarketMovements", layout="wide")

st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Select a Screen", ["Market Dashboard", "Options Intelligence", "Trade History"])

if page == "Market Dashboard":
    dashboard.render()
elif page == "Options Intelligence":
    options_view.render()
elif page == "Trade History":
    history.render()