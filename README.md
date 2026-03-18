# 📊 Raj Market Forecast Dashboard

A high‑performance, real‑time **market intelligence and forecasting system** built with Python + Streamlit.  
Designed for traders who need **instant clarity** at the New York Open — with global session context, volume analytics, bias scoring, and actionable insights in one unified command center.

---

## 🚀 Overview

The **Raj Market Forecast Dashboard** is engineered for fast, high‑signal decision‑making.  
It combines:

- **Global session awareness** (New York + London)
- **Institutional bias scoring**
- **Volume momentum tracking**
- **Forecast breakdown analytics**
- **Ticker‑aware news intelligence**
- **Historical forecast logging**
- **Sector performance heatmap**
- **Quick Switch ticker control**

All wrapped in a **zero‑waste, trader‑optimized UI**.

---

## ✨ Key Features

### 🔥 1. Command‑Center UI  
A redesigned layout with:
- No wasted top margin  
- High‑contrast typography  
- Clean spacing  
- Instant access to Quick Switch  
- Optimized for 1080p/1440p trading monitors  

### 🌍 2. Dual‑Session Intelligence  
Real‑time tracking of:

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
- Final Close price once session ends  

All session logic is timezone‑accurate using `pytz` (DST‑safe).

---

### 🎯 3. Institutional Bias Engine  
A proprietary scoring model combining:

- **Technical position** within the day’s range  
- **Sentiment score** from real‑time news  
- **Volume intensity**  
- **ATR‑based upside/downside projections**

Outputs:
- **Bullish** (deep green)  
- **Bearish** (deep red)  
- **Neutral** (charcoal)  
- **Conviction Gauge** (0–100)  

---

### ⚡ 4. Smart Ticker Management  
#### **Quick Switch**
One‑click analysis for:
- NQ=F  
- ES=F  
- GC=F  
- CL=F  
- TSLA  
- AMZN  

#### **Manual Entry**
Enter any Yahoo Finance ticker.  
Built‑in validation prevents invalid symbols.

---

### 📈 5. Volume & Momentum  
- **VOL RATIO** (current vs average volume)  
- Sparkline trend visualization  
- Auto‑highlight when volume exceeds thresholds  

---

### 📰 6. Market Intel  
Real‑time, clickable headlines:
- Timestamped  
- Source‑tagged  
- Sentiment‑scored  
- Filtered to last 24 hours  

---

### 🧠 7. Forecast Breakdown  
A clean bar‑chart showing:
- Technical impact  
- Sentiment impact  

---

### 🗂️ 8. History Log  
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

### 📊 9. Sector Trend Heatmap  
Live performance of:
- Tech  
- Finance  
- Discretionary  
- Communications  
- Healthcare  
- Industrials  

Each sector block uses:
- Color‑coded performance  
- Clean, compact layout  

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/reachgjraj/PredictMarketMovements.git
cd PredictMarketMovements