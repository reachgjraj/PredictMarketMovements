import yfinance as yf
import requests
import feedparser
from datetime import datetime


PUBLISHER_ICONS = {
    "Reuters": "📰",
    "Bloomberg": "📊",
    "Yahoo Finance": "💼",
    "CNBC": "📺",
    "MarketWatch": "📈",
    "System": "⚠️",
}


def _clean_time(ts):
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ""


def _score_sentiment(title: str) -> float:
    if not title:
        return 0

    title = title.lower()
    positive = ["up", "beats", "strong", "growth", "bull", "surge", "rally"]
    negative = ["down", "miss", "weak", "drop", "bear", "fall", "selloff"]

    score = 0
    for p in positive:
        if p in title:
            score += 1
    for n in negative:
        if n in title:
            score -= 1
    return score


def _sentiment_category(score):
    if score > 0.5:
        return "Bullish", "🟢", "#00cc66"
    if score < -0.5:
        return "Bearish", "🔴", "#ff4b4b"
    return "Neutral", "⚪", "#cccccc"


def _fetch_marketwatch_news():
    """Fetch MarketWatch RSS feed."""
    feeds = [
        "https://www.marketwatch.com/rss/topstories",
        "https://www.marketwatch.com/rss/marketpulse",
        "https://www.marketwatch.com/rss/markets",
    ]

    items = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                items.append({
                    "title": entry.title,
                    "url": entry.link,
                    "publisher": "MarketWatch",
                    "providerPublishTime": datetime.now().timestamp(),
                })
        except Exception:
            continue

    return items


def _fetch_yahoo_trending_news():
    """Fallback: Yahoo trending news."""
    try:
        url = "https://query1.finance.yahoo.com/v1/finance/trending/US"
        data = requests.get(url, timeout=5).json()

        news = []
        for item in data.get("finance", {}).get("result", []):
            for t in item.get("quotes", []):
                sym = t.get("symbol")
                if not sym:
                    continue
                ticker = yf.Ticker(sym)
                if ticker.news:
                    return ticker.news[:5]
        return []
    except Exception:
        return []


def get_sentiment(symbol: str, top_n=3):
    """
    Multi‑source news engine:
    1. Yahoo Finance news
    2. MarketWatch RSS news
    3. Yahoo trending news
    4. Fallback system message
    """

    news_items = []
    total_score = 0

    # 1. Yahoo Finance
    try:
        ticker = yf.Ticker(symbol)
        raw_news = ticker.news or []
    except Exception:
        raw_news = []

    # 2. MarketWatch
    mw_news = _fetch_marketwatch_news()
    raw_news.extend(mw_news)

    # 3. Yahoo trending (fallback)
    if not raw_news:
        raw_news = _fetch_yahoo_trending_news()

    # 4. Still empty → fallback
    if not raw_news:
        return 0, [{
            "title": "No relevant news found for this symbol.",
            "url": None,
            "source": "System",
            "icon": "⚠️",
            "time": "",
            "sentiment_score": 0,
            "sentiment_cat": "Neutral",
            "sentiment_badge": "⚪",
            "sentiment_color": "#cccccc",
            "is_fallback": True,
        }], "Neutral", "⚪"

    # Parse + score
    for item in raw_news[:20]:
        title = item.get("title")
        source = item.get("publisher") or item.get("source") or "MarketWatch"
        url = item.get("link") or item.get("url")
        ts = item.get("providerPublishTime") or datetime.now().timestamp()

        if not title:
            continue

        sentiment_score = _score_sentiment(title)
        sentiment_cat, badge, color = _sentiment_category(sentiment_score)

        total_score += sentiment_score

        news_items.append({
            "title": title,
            "url": url,
            "source": source,
            "icon": PUBLISHER_ICONS.get(source, "📰"),
            "time": _clean_time(ts),
            "sentiment_score": sentiment_score,
            "sentiment_cat": sentiment_cat,
            "sentiment_badge": badge,
            "sentiment_color": color,
            "is_fallback": False,
        })

    # Sort by strongest sentiment
    news_items.sort(key=lambda x: abs(x["sentiment_score"]), reverse=True)

    # Top N
    news_items = news_items[:top_n]

    avg_sentiment = total_score / max(len(news_items), 1)
    summary_cat, summary_badge, _ = _sentiment_category(avg_sentiment)

    return avg_sentiment, news_items, summary_cat, summary_badge