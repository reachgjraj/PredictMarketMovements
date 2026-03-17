# 📊 Market Open Intelligence Dashboard

## 🚀 Overview
The Market Open Intelligence Dashboard is a professional-grade, real-time analytics suite built in Python and Streamlit. Designed specifically to navigate the volatility of the **9:30 AM ET New York Open**, it aggregates price action, London session ranges, news sentiment, and institutional volume footprints to calculate a directional trade Bias and Conviction Score.

## ✨ Key Features
* **Lightning-Fast Ticker Selection:** Use pre-configured quick-switch buttons for major futures and tech leaders (NQ, ES, GC, TSLA, AMZN), or use the **Manual Ticker** input to analyze any asset on the fly.
* **Dual-Session Intelligence (NY & London):** * Compares live NY price action against the London Session (3:00 AM - 11:30 AM ET) Open, High, and Low.
  * Dynamically tracks if the London session is "Open" (Green) or "Closed" (Red).
* **Institutional Bias Engine:** Calculates a 0-100 conviction score and outputs a highly visible **Bullish (Deep Green)**, **Bearish (Deep Red)**, or **Neutral (Dark Gray)** bias using a brute-force HTML layout that prevents dark-mode color overriding.
* **Volume & Momentum Tracking:** * Real-time **VOL RATIO** highlights institutional participation.
  * Volume Trend sparklines visualize buying/selling acceleration.
* **Relative Strength & Sector Heat:** Benchmarks the active asset against the broader market and tracks the performance of key S&P 500 sectors (Tech, Finance, Energy).
* **Live Market Intel:** Pulls real-time, clickable news headlines relevant to the active ticker.

---

## 🛠️ Installation & Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system. You will need the following libraries:
```bash
pip install streamlit pandas yfinance plotly sqlite3