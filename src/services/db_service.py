import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('market.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_forecasts (
            id TEXT PRIMARY KEY, date TEXT, symbol TEXT, prev_close REAL, 
            current_price REAL, forecast_open REAL, bias TEXT, 
            expected_low REAL, expected_high REAL, tech_points REAL, 
            news_points REAL, vol_ratio REAL, london_high REAL, london_low REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pnl_tracker (
            date TEXT PRIMARY KEY, daily_pnl REAL, notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_daily_log(symbol, data):
    conn = sqlite3.connect('market.db')
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    entry_id = f"{today}_{symbol}"
    cursor.execute('''
        INSERT OR REPLACE INTO daily_forecasts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        entry_id, today, symbol,
        round(data.get('prev_close', 0), 2),
        round(data.get('current', 0), 2),
        round(data.get('open', 0), 2),
        data.get('bias', 'Neutral'),
        round(data.get('downside', 0), 2),
        round(data.get('upside', 0), 2),
        round(data.get('t_impact', 0), 2),
        round(data.get('s_impact', 0), 2),
        round(data.get('vol_ratio', 1.0), 2),
        round(data.get('london_high', 0), 2),
        round(data.get('london_low', 0), 2)
    ))
    conn.commit()
    conn.close()

def get_history_with_validation():
    conn = sqlite3.connect('market.db')
    df = pd.read_sql_query(
        "SELECT * FROM daily_forecasts ORDER BY date DESC LIMIT 15",
        conn
    )
    conn.close()
    return df