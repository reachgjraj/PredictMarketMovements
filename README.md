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

A high‑performance, real‑time **market intelligence and forecasting system** built with Python + Streamlit.  
Engineered for traders who demand **instant clarity**, **global session awareness**, and **actionable bias scoring** — all in a clean, zero‑waste UI optimized for trading monitors.

---

## 🚀 Overview

The Raj Market Forecast Dashboard combines:

- **Global session intelligence** (New York + London)
- **Institutional bias scoring**
- **Volume momentum analytics**
- **Forecast breakdown visualization**
- **Ticker‑aware news intelligence**
- **Historical forecast logging**
- **Sector performance heatmap**
- **Quick Switch ticker control**
- **Premium loading animation (C3 Triple Pulse Rings)**

All wrapped in a **fast, responsive, trader‑optimized interface**.

---

## ✨ Key Features

### 🔥 1. Command‑Center UI
A redesigned layout built for speed and clarity:

- Minimal top margin  
- High‑contrast typography  
- Clean spacing  
- Quick Switch always visible  
- Optimized for 1080p / 1440p trading setups  

---

### 🌍 2. Dual‑Session Intelligence

#### **New York Session**
- Open/Close status  
- Countdown timer  
- Previous close  
- Current price  
- Gap %  

#### **London Session**
- Open/Close status  
- Countdown timer  
- Live OHLC (Open, High, Low)  
- Final Close price after session ends  

All session logic is timezone‑accurate using `pytz` (DST‑safe).

---

### 🎬 3. Premium Loading Animation  
**C3 — Triple Pulse Rings (Neon Green)**  
- Three independent rings  
- Smooth zoom‑in / zoom‑out  
- Randomized phase offsets  
- Radar‑like liquidity pulse  
- Runs in parallel with analysis  
- Zero dead pause  

---

### 🎯 4. Institutional Bias Engine

A proprietary scoring model combining:

- Technical position within the day’s range  
- Real‑time news sentiment  
- Volume intensity  
- ATR‑based upside/downside projections  

Outputs:

- **Bullish** (deep green)  
- **Bearish** (deep red)  
- **Neutral** (charcoal)  
- **Conviction Gauge** (0–100)  

---

### ⚡ 5. Smart Ticker Management

#### **Quick Switch**
One‑tap analysis for:
- `NQ=F`
- `ES=F`
- `GC=F`
- `CL=F`
- `TSLA`
- `AMZN`

#### **Manual Entry**
Enter any Yahoo Finance ticker.  
Invalid symbols are automatically rejected.

---

### 📈 6. Volume & Momentum
- **VOL RATIO** (current vs average volume)  
- Sparkline trend visualization  
- Auto‑highlight when volume exceeds thresholds  

---

### 📰 7. Market Intel
Real‑time, clickable headlines:

- Timestamped  
- Source‑tagged  
- Sentiment‑scored  
- Filtered to last 24 hours  

---

### 🧠 8. Forecast Breakdown
A clean bar‑chart showing:

- Technical impact  
- Sentiment impact  

---

### 🗂️ 9. History Log
Every forecast is automatically saved with:

- Symbol  
- Prev Close  
- Current Price  
- Forecasted Open  
- Upside / Downside  
- Bias  
- Volume Ratio  
- London High/Low  

Stored in `market.db` using SQLite.

---

### 📊 10. Sector Trend Heatmap
Live performance of:

- Tech  
- Finance  
- Discretionary  
- Communications  
- Healthcare  
- Industrials  

Each sector block includes:

- Color‑coded performance  
- Clean, compact layout  

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/reachgjraj/PredictMarketMovements.git
cd PredictMarketMovements