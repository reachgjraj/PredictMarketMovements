<p align="center">
  <img src="https://img.shields.io/badge/RAJ%20MARKET%20FORECAST%20DASHBOARD-REAL--TIME%20TRADING%20INTELLIGENCE-blueviolet?style=for-the-badge&logo=chart-bar&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/STREAMLIT-APP-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/PYTHON-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/STATUS-LIVE-success?style=for-the-badge" />
</p>

<p align="center">
  <b>Session‑Aware • Volume‑Aware • Bias‑Aware</b><br>
  <i>Designed for traders who need instant clarity at the New York Open.</i>
</p>

---

# 📊 Raj Market Forecast Dashboard

A high‑performance, real‑time **market intelligence and forecasting system** built with Python + Streamlit. Engineered for traders who demand **instant clarity**, **global session awareness**, and **actionable bias scoring** — all in a clean, zero‑waste UI optimized for trading monitors.

---

## 🚀 Overview

The Raj Market Forecast Dashboard combines institutional-grade analytics with a responsive interface:

* **Global Session Intelligence:** Real-time monitoring of New York and London sessions.
* **Institutional Bias Scoring:** Advanced 3D Sentiment Globes for visual bias cues.
* **Volume Momentum:** Real-time analytics and Sparkline trends.
* **Intelligence Feed:** Ticker-aware news via custom-styled HTML feeds.
* **Persistence:** Historical forecast logging using SQLite.
* **Performance:** Premium C3 Triple Pulse Rings loading animation for a zero-lag feel.

---
## 👥 Contributors
* Lead Developer: GJ (Architecture, UI/UX, Forecasting Engine)
---

## ✨ Key Features

### 🔥 1. Command‑Center UI (v1.2.0 Overhaul)
* **Zero-Margin Layout:** Aggressive CSS overrides eliminate Streamlit's default padding for an edge-to-edge terminal feel.
* **High-Contrast Cards:** Dedicated Light Blue (NYSE) and Light Purple (London) themes.
* **Multi-Monitor Optimized:** Tuned for 1080p / 1440p high-density setups.

### 🌍 2. Dual‑Session Intelligence
* **New York Session:** Open/Close status, countdown timers, and daily High/Low tracking.
* **London Session:** Live OHLC (Open, High, Low) and Final Close price.
* *DST-safe timezone logic via `pytz`.*

### 🎯 3. Institutional Bias Engine & 3D Globes
Proprietary scoring visualized via **Dynamic 3D CSS Globes**:
* 🟢 **Bullish:** Vibrant Green Globe + Neon Aura.
* 🔴 **Bearish:** Vibrant Red Globe + Neon Aura.
* ⚪ **Neutral:** Charcoal/Grey Globe.

### 📰 4. Market Intel (Custom HTML Feed)
* **Sentiment Tinting:** Headlines wrapped in containers with 10% opacity backgrounds.
* **Visual Cues:** Miniature 3D sentiment globes paired with bold, clickable blue hyperlinks.
* **Expander-Free:** Flat, readable UI designed for quick scanning.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
Bash
git clone [https://github.com/reachgjraj/PredictMarketMovements.git](https://github.com/reachgjraj/PredictMarketMovements.git)
cd PredictMarketMovements
### 2. Install Dependencies
Bash
pip install -r requirements.txt
### 3. Run the Dashboard
Bash
streamlit run app.py

---

## 🗺 Roadmap
### v1.3: Options Intelligence (IV Rank & Profit Probabilities).
### v1.4: Interactive Economic Calendar integration.
### v2.0: Backend API deployment & Webhook sentiment alerts.

---

## 📝 Dependencies (requirements.txt)
The following packages are required to run the dashboard:

Plaintext
streamlit
pandas
numpy
plotly
yfinance
pytz
requests
feedparser
Pillow

---

## 📁 Project Structure

```text
PredictMarketMovements/
├── app.py                  # Main entry point
├── requirements.txt        # Dependencies
├── market.db               # SQLite Database
└── src/
    ├── services/           # DB, News, and API services
    ├── engine/             # Forecasting and scoring logic
    └── ui/
        ├── dashboard.py    # Main UI assembly
        └── components/
            └── layout.py   # CSS, 3D Globe styling, and core architecture

