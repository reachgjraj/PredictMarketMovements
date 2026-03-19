import streamlit as st
import sqlite3
import pandas as pd

def render():
    st.title("📜 Trade History")

    conn = sqlite3.connect("market.db")
    df = pd.read_sql_query(
        "SELECT * FROM daily_forecasts ORDER BY date DESC LIMIT 50",
        conn
    )
    conn.close()

    if 'id' in df.columns:
        df = df.drop(columns=['id'])

    st.dataframe(df.style.format(precision=2), width="stretch", height=400)