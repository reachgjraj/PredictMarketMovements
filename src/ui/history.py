import streamlit as st
import sqlite3
import pandas as pd

def render():
    st.title("📜 Trade History")
    conn = sqlite3.connect("Data/market.db")
    df = pd.read_sql_query("SELECT * FROM forecasts", conn)
    st.dataframe(df)