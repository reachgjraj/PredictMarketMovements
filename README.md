# 📊 Raj Market Forecast Dashboard

## 🚀 Overview
The **Raj Market Forecast Dashboard** is a high-performance, real-time trading intelligence suite built with Python and Streamlit. Engineered for the **9:30 AM ET New York Open**, it provides a unified command center for futures and equity traders to assess market bias, volume intensity, and global session context in a single glance.

## ✨ Key Features
* **Command Center UI:** Re-engineered layout with zero top-margin waste, optimized for professional desktop monitoring.
* **Dual-Session Intelligence:** * **New York & London Panels:** Real-time status tracking with dynamic **Countdown Timers** (handled via `pytz` for perfect DST accuracy).
    * **London Data:** Automatically displays Open, High, Low, and the final Close price once the session concludes.
* **Institutional Bias Engine:** * A 0-100 conviction score visualized through high-contrast, bulletproof HTML components.
    * **Dynamic Bias:** Real-time Bullish (Deep Green), Bearish (Deep Red), or Neutral classification.
* **Market Heatmap:** Integrated **Mega-Cap Treemap** visualizing the performance of the top 20 market movers (NVDA, AAPL, TSLA, etc.) to gauge overall market breadth.
* **Smart Ticker Management:**
    * **Quick Switch:** One-click analysis for NQ, ES, GC, CL, TSLA, and AMZN.
    * **Manual Entry:** Analyze any Yahoo Finance ticker with built-in **Validation Logic** that catches and alerts on invalid symbols.
* **Volume & Momentum:** Live **VOL RATIO** tracking and sparkline trends to identify institutional participation.
* **News Intel:** Real-time, clickable headlines directly relevant to the active symbol.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.9+ and the following core libraries:
```bash
pip install streamlit pandas yfinance plotly pytz textblob nltk beautifulsoup4 requests